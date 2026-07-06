"""
launch.py — one command that schedules the YouTube week and emits the launch package.

Publishing-flow Phase 1, dependency-ordered: episode first (link in hand), then
shorts, then the LinkedIn/DM package is written with real URLs baked in.

Usage (from studio/):
    python launch.py <slug> --monday 2026-07-13 --title "How ... Makes Money"   # dry run: prints plan, writes package with placeholders
    python launch.py <slug> --monday 2026-07-13 --title "..." --go              # actually uploads/schedules via YouTube API

What it does:
  1. Computes publish-at times (episode Mon 11:00 ET, shorts Tue–Fri 8:30 ET) in UTC.
  2. Rubric-lints every LinkedIn copy file (scripts/originate/rubric_check.py) — hard fails abort.
  3. --go: uploads episode via scripts/originate/upload_youtube.py (privacy=private + publishAt),
     captures the youtu.be link, then uploads the 4 shorts with the episode link
     substituted into their descriptions/pinned-comment text.
  4. Writes originate/<slug>/launch/: checklist.md (the week, with dates + links),
     links.json (machine-readable manifest for the scheduled tasks / Chrome runs),
     dm_shortlist.md (template seeded with the standing list).

Manual steps it CANNOT do (listed in the checklist it writes): SRT + thumbnail +
end screen in YT Studio, LinkedIn scheduling (Chrome), newsletter send, site flip
(scripts/originate/publish.py).
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import date, datetime, time, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

STUDIO = Path(__file__).parent
ET = ZoneInfo("America/New_York")

EPISODE_TIME = time(11, 0)   # Mon 11:00 ET
SHORT_TIME = time(8, 30)     # Tue–Fri 8:30 ET

STANDING_DM_LIST = ["Henry", "Joni"]  # Tier 3 seeds — expand from relationship notes


def utc_iso(d: date, t: time) -> str:
    return datetime.combine(d, t, tzinfo=ET).astimezone(ZoneInfo("UTC")).strftime(
        "%Y-%m-%dT%H:%M:%SZ")


def run_upload(video: Path, title: str, desc: str, publish_at: str, go: bool) -> str:
    """Upload one video, return the youtu.be URL (placeholder on dry run)."""
    cmd = [sys.executable, str(STUDIO / "scripts/originate/upload_youtube.py"),
           str(video), "--title", title, "--privacy", "private",
           "--publish-at", publish_at, "--description", desc]
    if not go:
        print(f"  DRY RUN: {video.name!r} → publishAt {publish_at}")
        return "[PENDING_UPLOAD]"
    out = subprocess.run(cmd, capture_output=True, text=True)
    print(out.stdout.strip())
    if out.returncode != 0:
        print(out.stderr, file=sys.stderr)
        sys.exit(f"upload failed for {video.name}")
    for ln in out.stdout.splitlines():
        if ln.startswith("UPLOADED: "):
            return ln.split("UPLOADED: ")[1].strip()
    sys.exit(f"no UPLOADED line in output for {video.name}")


def rubric_gate(files: list[tuple[Path, str]]) -> None:
    bad = False
    for f, surface in files:
        if not f.exists():
            print(f"  (skip rubric: {f.name} missing)")
            continue
        r = subprocess.run([sys.executable,
                            str(STUDIO / "scripts/originate/rubric_check.py"),
                            str(f), "--surface", surface],
                           capture_output=True, text=True)
        status = "PASS" if r.returncode == 0 else "FAIL"
        print(f"  rubric {status}: {f.name}")
        if r.returncode != 0:
            print("\n".join("    " + ln for ln in r.stdout.splitlines()))
            bad = True
    if bad:
        sys.exit("Rubric hard-fails above — revise, don't rationalize (post-rubric §5).")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("slug")
    ap.add_argument("--monday", required=True, help="episode Monday, YYYY-MM-DD")
    ap.add_argument("--title", required=True, help="episode YouTube title (search-packaged)")
    ap.add_argument("--video", help="episode mp4 (default: originate/<slug>/ep*-final.mp4)")
    ap.add_argument("--go", action="store_true", help="actually upload (default: dry run)")
    ap.add_argument("--rubric-waiver", metavar="REASON",
                    help="skip the rubric gate; reason is stamped into checklist.md")
    args = ap.parse_args()

    ep_dir = STUDIO / "originate" / args.slug
    if not ep_dir.exists():
        sys.exit(f"no such episode dir: {ep_dir}")
    monday = date.fromisoformat(args.monday)
    if monday.weekday() != 0:
        sys.exit(f"{args.monday} is not a Monday (site promise: ships every Monday)")

    video = Path(args.video) if args.video else next(
        iter(sorted(ep_dir.glob("ep*-final.mp4"))), None)
    if video is None or not video.exists():
        sys.exit("episode video not found — pass --video")
    shorts = sorted((ep_dir / "shorts").glob("short-*.mp4"))
    briefs = json.loads((ep_dir / "content" / "shorts_briefs.json").read_text()) \
        if (ep_dir / "content" / "shorts_briefs.json").exists() else []
    desc_file = ep_dir / "content" / "youtube_description.txt"
    ep_desc = desc_file.read_text() if desc_file.exists() else ""

    # ---- Rubric gate before anything ships ----
    if args.rubric_waiver:
        print(f"⚠ RUBRIC GATE WAIVED: {args.rubric_waiver}")
    else:
        print("Rubric gate:")
        rubric_gate([
            (ep_dir / "content" / "launch_linkedin.md", "feed"),
            (ep_dir / "content" / "linkedin_posts.md", "feed"),
            (ep_dir / "content" / "newsletter.md", "carousel"),  # doc surface: em dash ok, lexicon still banned
        ])

    # ---- 1. Episode ----
    print("\nEpisode:")
    ep_publish = utc_iso(monday, EPISODE_TIME)
    ep_url = run_upload(video, args.title, ep_desc, ep_publish, args.go)

    # ---- 2. Shorts (episode link baked into descriptions) ----
    print("\nShorts:")
    short_entries = []
    for i, sv in enumerate(shorts[:4]):
        day = monday + timedelta(days=i + 1)  # Tue..Fri
        brief = briefs[i] if i < len(briefs) else {}
        title = brief.get("title", sv.stem)[:95]
        pinned = brief.get("pinned_comment", "Full breakdown: [long-form link]") \
            .replace("[long-form link]", ep_url)
        desc = (f"{pinned}\n\nThe Operator Blueprint (free): "
                f"https://theoperatoreconomy.com/episodes/{args.slug}")
        url = run_upload(sv, title, desc, utc_iso(day, SHORT_TIME), args.go)
        short_entries.append({"file": sv.name, "title": title, "url": url,
                              "publish_et": f"{day} 08:30 ET",
                              "pinned_comment": pinned})

    # ---- 3. Launch package ----
    launch_dir = ep_dir / "launch"
    launch_dir.mkdir(exist_ok=True)
    manifest = {
        "slug": args.slug, "monday": str(monday), "title": args.title,
        "episode_url": ep_url, "episode_publish_et": f"{monday} 11:00 ET",
        "blueprint_url": f"https://theoperatoreconomy.com/episodes/{args.slug}",
        "carousel_pdf": next((str(p) for p in ep_dir.glob("carousel-*.pdf")), None),
        "shorts": short_entries,
        "generated": datetime.now(ET).isoformat(),
        "dry_run": not args.go,
    }
    (launch_dir / "links.json").write_text(json.dumps(manifest, indent=2))

    checklist = f"""# Launch week — {args.title} ({monday})

Generated by launch.py ({'LIVE' if args.go else 'DRY RUN'}). Flow: docs/publishing-flow.md. Every post rubric-gated.
{f"⚠ RUBRIC WAIVED: {args.rubric_waiver}" if args.rubric_waiver else ""}

## Scheduled by this script
- [{'x' if args.go else ' '}] YT episode — Mon {monday} 11:00 ET — {ep_url}
""" + "".join(
        f"- [{'x' if args.go else ' '}] YT short {i+1} — {s['publish_et']} — {s['url']}\n"
        for i, s in enumerate(short_entries)) + f"""
## Manual — YT Studio (with upload, before Monday)
- [ ] SRT captions (drag ep .srt into Subtitles)
- [ ] Thumbnail = title-card frame
- [ ] End screen last 6s: Subscribe + best-for-viewer

## Manual — Sunday night (Chrome / scheduled task drives)
- [ ] OE page episode post scheduled Mon 11:00 (carousel attached LAST, then Schedule)
- [ ] OE page shorts posts ×4 scheduled Tue–Fri 8:30 (native vertical video)

## Hour one — Monday 11:00–12:00
- [ ] Sources comment under OE post (episode + blueprint links, confidence flags)
- [ ] Newsletter send (content/newsletter.md)
- [ ] Personal repost of OE carousel post + one-line analyst comment (rubric-gated)
- [ ] Site flip: python scripts/originate/publish.py {args.slug}

## The week
- [ ] Mon–Tue: DM sends from launch/dm_shortlist.md (no ask, analyst register)
- [ ] Tue–Wed: Product of One group — carousel + genuine question (neutral citation)
- [ ] Tue–Fri: verify shorts live; pin episode-link comments; 2–3 personal analyst posts
"""
    (launch_dir / "checklist.md").write_text(checklist)

    dm = f"""# DM shortlist — {args.slug} ({monday})

Register: friend who saw something relevant. No ask. Ever. One msg per person per episode.
Episode: {ep_url} · Blueprint: {manifest['blueprint_url']}

## Tier 1 — direct relevance (5–10)
| Who | Why this episode is theirs | Draft | Sent |
|---|---|---|---|
|  |  |  |  |

## Tier 2 — operators/amplifiers (3–5) — ask for a REACTION to the thesis
| Who | Runs/knows | Draft | Sent | Reaction (→ growth-strategy ladder) |
|---|---|---|---|---|
|  |  |  |  |  |

## Tier 3 — standing list (stop after 2 no-replies)
{chr(10).join(f"- [ ] {n}" for n in STANDING_DM_LIST)}
- [ ] (active pitches: separate message, only if relevant, never inside the pitch thread)
"""
    (launch_dir / "dm_shortlist.md").write_text(dm)

    print(f"\nLaunch package → {launch_dir}/ (checklist.md, links.json, dm_shortlist.md)")
    if not args.go:
        print("Dry run. Re-run with --go to upload/schedule.")


if __name__ == "__main__":
    main()
