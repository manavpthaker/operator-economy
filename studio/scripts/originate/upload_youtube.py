"""
Upload a video to the channel via YouTube Data API v3 (resumable upload).
Dependency-light: requests only. Reads .secrets/token.json (from
tools/youtube_auth.py). Sets the AI-disclosure flag on every upload.

Usage:
    python scripts/originate/upload_youtube.py video.mp4 \
        --title "..." --description-file desc.txt \
        [--privacy private|unlisted|public] [--publish-at 2026-07-07T13:00:00Z] \
        [--tags "a,b,c"] [--no-synthetic]

Defaults: privacy=private, containsSyntheticMedia=true.
"""

import argparse
import json
import sys
from pathlib import Path

import requests

ROOT = Path(__file__).parent.parent.parent
TOKEN_PATH = ROOT / ".secrets" / "token.json"


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


def main():
    p = argparse.ArgumentParser(description="Upload video via YouTube Data API")
    p.add_argument("video")
    p.add_argument("--title", required=True)
    p.add_argument("--description", default="")
    p.add_argument("--description-file")
    p.add_argument("--tags", default="")
    p.add_argument("--privacy", default="private", choices=["private", "unlisted", "public"])
    p.add_argument("--publish-at", help="ISO8601 UTC; only valid with --privacy private")
    p.add_argument("--category", default="27", help="27 = Education")
    p.add_argument("--no-synthetic", action="store_true",
                   help="UNSET the AI-disclosure flag (default is SET)")
    args = p.parse_args()

    desc = args.description
    if args.description_file:
        desc = Path(args.description_file).read_text()

    status = {
        "privacyStatus": args.privacy,
        "selfDeclaredMadeForKids": False,
        "containsSyntheticMedia": not args.no_synthetic,
    }
    if args.publish_at:
        status["publishAt"] = args.publish_at

    body = {
        "snippet": {
            "title": args.title,
            "description": desc,
            "tags": [t.strip() for t in args.tags.split(",") if t.strip()],
            "categoryId": args.category,
        },
        "status": status,
    }

    tok = access_token()
    video = Path(args.video)
    size = video.stat().st_size

    # Start resumable session
    r = requests.post(
        "https://www.googleapis.com/upload/youtube/v3/videos"
        "?uploadType=resumable&part=snippet,status",
        headers={"Authorization": f"Bearer {tok}",
                 "Content-Type": "application/json; charset=UTF-8",
                 "X-Upload-Content-Length": str(size),
                 "X-Upload-Content-Type": "video/mp4"},
        json=body, timeout=60)
    if r.status_code != 200:
        print("SESSION ERROR:", r.status_code, r.text[:400]); sys.exit(1)
    upload_url = r.headers["Location"]

    with open(video, "rb") as f:
        r2 = requests.put(upload_url,
                          headers={"Authorization": f"Bearer {tok}",
                                   "Content-Type": "video/mp4",
                                   "Content-Length": str(size)},
                          data=f, timeout=600)
    if r2.status_code not in (200, 201):
        print("UPLOAD ERROR:", r2.status_code, r2.text[:400]); sys.exit(1)

    v = r2.json()
    vid = v["id"]
    st = v.get("status", {})
    print(f"UPLOADED: https://youtu.be/{vid}")
    print(f"  privacyStatus: {st.get('privacyStatus')}  (requested: {args.privacy})")
    print(f"  uploadStatus:  {st.get('uploadStatus')}")
    print(f"  containsSyntheticMedia: {st.get('containsSyntheticMedia')}")
    if st.get("privacyStatus") != args.privacy:
        print("  NOTE: privacy was overridden — expected for unaudited API projects (locked private until compliance audit).")


if __name__ == "__main__":
    main()
