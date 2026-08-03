"""
launch.py — one command that schedules the YouTube week and emits the launch package.

Publishing-flow Phase 1, dependency-ordered: episode first (link in hand), then
shorts, then the LinkedIn/DM package is written with real URLs baked in.

Usage (from studio/):
    python launch.py <slug> --monday 2026-07-13 --title "How ... Makes Money"   # dry run: prints plan, writes package with placeholders
    python launch.py <slug> --monday 2026-07-13 --title "..." --go              # actually uploads/schedules via YouTube API

What it does:
  1. Computes publish-at times (trailer Sun 18:00 ET, episode Mon 11:00 ET, shorts Tue–Fri 8:30 ET) in UTC.
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
TRAILER_TIME = time(18, 0)   # Sun 6:00 PM ET — pre-launch montage teaser

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
    # Renders land in remotion/out/ (canonical output), fall back to originate/<slug>/shorts/.
    render_out = STUDIO / "remotion" / "out"
    short_src = render_out if list(render_out.glob("short-*.mp4")) else (ep_dir / "shorts")
    shorts = sorted(short_src.glob("short-*.mp4"))
    # Idempotency: reuse anything already uploaded so re-runs never duplicate.
    links_path = ep_dir / "launch" / "links.json"
    existing = json.loads(links_path.read_text()) if links_path.exists() else {}
    existing_ep = existing.get("episode_url", "") if not existing.get("dry_run", True) else ""
    existing_shorts = {s.get("file"): s.get("url") for s in existing.get("shorts", [])
                       if str(s.get("url", "")).startswith("http")}
    briefs = json.loads((ep_dir / "content" / "shorts_briefs.json").read_text()) \
        if (ep_dir / "content" / "shorts_briefs.json").exists() else []
    desc_file = ep_dir / "content" / "youtube_description.txt"
    ep_desc = desc_file.read_text() if desc_file.exists() else ""

    # ---- Blueprint PDF gate: it's what email signups receive ----
    bp_pdf = next(iter(ep_dir.glob("Operator-Blueprint-*.pdf")), None)
    if bp_pdf is None:
        print("⚠ No designed blueprint PDF found. The blueprint IS the lead magnet — render it:\n"
              f"  python scripts/originate/render_blueprint.py originate/{args.slug}/script.json "
              "--hero '...' --hero-caption '...'")
        if args.go:
            sys.exit("Refusing --go without the blueprint PDF (signups would get nothing).")

    # ---- Rubric gate before anything ships ----
    if args.rubric_waiver:
        print(f"⚠ RUBRIC GATE WAIVED: {args.rubric_waiver}")
    else:
        print("Rubric gate:")
        rubric_gate([
            (ep_dir / "content" / "launch_linkedin.md", "feed"),
            (ep_dir / "content" / "linkedin_posts.md", "feed"),
            (ep_dir / "content" / "trailer_linkedin.md", "feed"),
            (ep_dir / "content" / "newsletter.md", "carousel"),  # doc surface: em dash ok, lexicon still banned
        ])

    # ---- 1. Episode (idempotent: reuse an already-uploaded URL) ----
    print("\nEpisode:")
    ep_publish = utc_iso(monday, EPISODE_TIME)
    if args.go and existing_ep.startswith("http"):
        print(f"  reusing already-uploaded episode: {existing_ep}")
        ep_url = existing_ep
    else:
        ep_url = run_upload(video, args.title, ep_desc, ep_publish, args.go)

    # ---- 2. Trailer (Sunday evening, episode link baked in) ----
    trailer_entry = None
    trailer_video = short_src / "trailer.mp4"
    trailer_brief = json.loads((ep_dir / "content" / "trailer_brief.json").read_text()) \
        if (ep_dir / "content" / "trailer_brief.json").exists() else {}
    sunday = monday - timedelta(days=1)
    trailer_past = args.go and datetime.now(ET) > datetime.combine(sunday, TRAILER_TIME, tzinfo=ET)
    if existing.get("trailer"):
        trailer_entry = existing["trailer"]
        print(f"\n  reusing already-uploaded trailer: {trailer_entry.get('url')}")
    elif trailer_video.exists() and trailer_brief and not trailer_past:
        print("\nTrailer:")
        t_title = trailer_brief.get("title", f"{args.title} — trailer")[:95]
        t_desc = (trailer_brief.get("youtube_description", "Full breakdown drops Monday 11 AM ET: [long-form link]")
                  .replace("[long-form link]", ep_url)
                  + f"\n\nThe Operator Blueprint (free): https://theoperatoreconomy.com/episodes/{args.slug}")
        t_url = run_upload(trailer_video, t_title, t_desc, utc_iso(sunday, TRAILER_TIME), args.go)
        trailer_entry = {"file": trailer_video.name, "title": t_title, "url": t_url,
                         "publish_et": f"{sunday} 18:00 ET"}
    elif trailer_past:
        print("\n(trailer slot Sun 18:00 ET already passed — skipping. Use teaser.mp4 as an evergreen post-launch driver.)")
    else:
        print("\n(no trailer — need trailer.mp4 + content/trailer_brief.json; "
              "see prepare_shorts.py --trailer)")

    # ---- 3. Shorts (episode link baked into descriptions) ----
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
        if sv.name in existing_shorts:
            url = existing_shorts[sv.name]
            print(f"  reusing short {sv.name}: {url}")
        elif args.go and datetime.now(ET) > datetime.combine(day, SHORT_TIME, tzinfo=ET):
            print(f"  short {i+1} ({day} 08:30 ET) already passed — skipping upload")
            continue
        else:
            url = run_upload(sv, title, desc, utc_iso(day, SHORT_TIME), args.go)
        short_entries.append({"file": sv.name, "title": title, "url": url,
                              "publish_et": f"{day} 08:30 ET",
                              "pinned_comment": pinned})

    # ---- 4. Launch package ----
    launch_dir = ep_dir / "launch"
    launch_dir.mkdir(exist_ok=True)
    manifest = {
        "slug": args.slug, "monday": str(monday), "title": args.title,
        "episode_url": ep_url, "episode_publish_et": f"{monday} 11:00 ET",
        "blueprint_url": f"https://theoperatoreconomy.com/episodes/{args.slug}",
        "carousel_pdf": next((str(p) for p in ep_dir.glob("carousel-*.pdf")), None),
        "blueprint_pdf": str(bp_pdf) if bp_pdf else None,
        "trailer": trailer_entry,
        "shorts": short_entries,
        "generated": datetime.now(ET).isoformat(),
        "dry_run": not args.go,
    }
    (launch_dir / "links.json").write_text(json.dumps(manifest, indent=2))

    checklist = f"""# Launch week — {args.title} ({monday})

Generated by launch.py ({'LIVE' if args.go else 'DRY RUN'}). Flow: docs/publishing-flow.md. Every post rubric-gated.
{f"⚠ RUBRIC WAIVED: {args.rubric_waiver}" if args.rubric_waiver else ""}

## Scheduled by this script
{f"- [{'x' if args.go else ' '}] YT trailer — Sun {monday - timedelta(days=1)} 18:00 ET — {trailer_entry['url']}" if trailer_entry else "- [ ] (no trailer this week)"}
- [{'x' if args.go else ' '}] YT episode — Mon {monday} 11:00 ET — {ep_url}
""" + "".join(
        f"- [{'x' if args.go else ' '}] YT short {i+1} — {s['publish_et']} — {s['url']}\n"
        for i, s in enumerate(short_entries)) + f"""
## Manual — YT Studio (with upload, before Monday)
- [ ] SRT captions (drag ep .srt into Subtitles)
- [ ] Thumbnail = title-card frame
- [ ] End screen last 6s: Subscribe + best-for-viewer

## Manual — Sunday night (Chrome / scheduled task drives)
- [ ] OE page trailer post — Sun evening, right after the YT trailer is live (native vertical video, copy from content/trailer_linkedin.md, link in first comment)
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
