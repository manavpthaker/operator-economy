"""
Post-upload verifier for YouTube schedule.

upload_youtube.py returns as soon as the resumable-upload PUT completes.
YouTube still needs minutes to transcode. During that window YT Studio
UI often does NOT show the "Scheduled" chip even if `publishAt` was
accepted at insert time. Worse: some accounts/quota states silently
drop `publishAt` and leave the video plain-private, which reads
identically in the UI until you check.

This script closes the loop:
  1. Poll processingStatus every N seconds until "succeeded" (or timeout)
  2. Read status.publishAt from the API — source of truth, not the UI
  3. If publishAt is missing but --publish-at was requested, PATCH the
     video via videos.update to set it
  4. Re-read + report final state

Usage:
    python scripts/originate/verify_youtube_schedule.py <video_id> \\
        [--publish-at 2026-08-03T15:00:00Z] [--wait 1800] [--interval 30]

Exit codes:
  0 = video is scheduled correctly (or no --publish-at requested and privacy is fine)
  1 = processing timeout / API error
  2 = schedule verification failed (publishAt still not set after patch)
"""

import argparse
import json
import sys
import time
from pathlib import Path

import requests

ROOT = Path(__file__).parent.parent.parent
TOKEN_PATH = ROOT / ".secrets" / "token.json"
API = "https://www.googleapis.com/youtube/v3"


def access_token() -> str:
    t = json.loads(TOKEN_PATH.read_text())
    r = requests.post(t["token_uri"], data={
        "client_id": t["client_id"],
        "client_secret": t["client_secret"],
        "refresh_token": t["refresh_token"],
        "grant_type": "refresh_token",
    }, timeout=30)
    r.raise_for_status()
    return r.json()["access_token"]


def get_video(tok: str, vid: str) -> dict | None:
    r = requests.get(
        f"{API}/videos?part=snippet,status,processingDetails&id={vid}",
        headers={"Authorization": f"Bearer {tok}"}, timeout=30)
    r.raise_for_status()
    items = r.json().get("items", [])
    return items[0] if items else None


def patch_publish_at(tok: str, vid: str, publish_at: str, title: str,
                     category_id: str) -> dict:
    """videos.update with status.publishAt. YT requires the snippet+status
    blocks to be fully specified on update; missing fields get cleared."""
    body = {
        "id": vid,
        "snippet": {"title": title, "categoryId": category_id},
        "status": {
            "privacyStatus": "private",
            "publishAt": publish_at,
            "selfDeclaredMadeForKids": False,
            "containsSyntheticMedia": True,
        },
    }
    r = requests.put(
        f"{API}/videos?part=snippet,status",
        headers={"Authorization": f"Bearer {tok}",
                 "Content-Type": "application/json; charset=UTF-8"},
        json=body, timeout=60)
    if r.status_code >= 300:
        sys.exit(f"videos.update failed [{r.status_code}]: {r.text[:500]}")
    return r.json()


def print_state(v: dict, prefix: str = "") -> None:
    snip = v.get("snippet", {})
    stat = v.get("status", {})
    proc = v.get("processingDetails", {})
    prog = proc.get("processingProgress", {}) or {}
    print(f"{prefix}title:            {snip.get('title', '')[:80]}")
    print(f"{prefix}privacyStatus:    {stat.get('privacyStatus')}")
    print(f"{prefix}publishAt:        {stat.get('publishAt', '(NONE)')}")
    print(f"{prefix}uploadStatus:     {stat.get('uploadStatus')}")
    print(f"{prefix}processingStatus: {proc.get('processingStatus')}")
    if prog.get("timeLeftMs"):
        print(f"{prefix}                  {prog.get('partsProcessed','?')}/"
              f"{prog.get('partsTotal','?')} parts · "
              f"{int(prog['timeLeftMs'])/1000:.0f}s left")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("video_id", help="YouTube video ID (e.g. MsbBfVRndu8)")
    ap.add_argument("--publish-at",
                    help="ISO8601 UTC — required schedule time; if missing "
                         "from the video after processing, patched via "
                         "videos.update")
    ap.add_argument("--wait", type=int, default=1800,
                    help="seconds to wait for processing (default 1800 = 30 min)")
    ap.add_argument("--interval", type=int, default=30,
                    help="poll interval seconds (default 30)")
    args = ap.parse_args()

    tok = access_token()

    print(f"→ polling {args.video_id} every {args.interval}s (up to {args.wait}s)")
    started = time.time()
    v = None
    last_status = ""
    while time.time() - started < args.wait:
        v = get_video(tok, args.video_id)
        if v is None:
            sys.exit(f"video {args.video_id} not found (deleted? wrong id?)")
        proc_status = v.get("processingDetails", {}).get("processingStatus", "?")
        if proc_status != last_status:
            elapsed = int(time.time() - started)
            print(f"  [{elapsed:4}s] processingStatus = {proc_status}")
            last_status = proc_status
        if proc_status == "succeeded":
            break
        if proc_status in {"failed", "terminated"}:
            print_state(v, "  ")
            sys.exit(f"processing {proc_status} — video is unusable")
        time.sleep(args.interval)
    else:
        print(f"⚠ timed out waiting for processing after {args.wait}s")
        print_state(v, "  ")
        return 1

    print("\n=== post-processing state ===")
    print_state(v, "  ")

    stat = v.get("status", {})
    current_pa = stat.get("publishAt")

    if not args.publish_at:
        print("\n(no --publish-at requested; verifier stops here)")
        return 0

    if current_pa == args.publish_at:
        print(f"\n✓ publishAt matches requested {args.publish_at}")
        return 0

    print(f"\n⚠ publishAt is {current_pa!r}, expected {args.publish_at!r}")
    print("  patching via videos.update...")
    snip = v.get("snippet", {})
    patch_publish_at(tok, args.video_id, args.publish_at,
                     snip.get("title", ""), snip.get("categoryId", "27"))

    time.sleep(2)
    v2 = get_video(tok, args.video_id)
    print("\n=== after patch ===")
    print_state(v2, "  ")
    if v2.get("status", {}).get("publishAt") == args.publish_at:
        print(f"\n✓ patched. publishAt = {args.publish_at}")
        return 0
    print("\n✗ patch did not stick. Set schedule manually in YT Studio.")
    return 2


if __name__ == "__main__":
    sys.exit(main())
