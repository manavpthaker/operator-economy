"""
Cut vertical shorts from the finished long-form render (2026-07-06).

Each brief in content/shorts_briefs.json names a section + beat window.
The cutter anchors the window in the ElevenLabs alignment (same
phrase-matching approach as layout_vo — never proportion guessing),
adds the bookend offset, and cuts 9:16 clips from the long-form mp4:
the 16:9 frame centered on a blurred self-fill, brand tag stamped on
the tail so every short ends on "operator."

Usage:
    python scripts/originate/cut_shorts.py originate/<slug>/script.json \
        [--video remotion/out/ep001.mp4] [--out-dir originate/<slug>/shorts]
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
PAD_IN = 0.25   # breath before the hook line
PAD_OUT = 0.45  # beat after the cliffhanger line
FADE = 0.4


def run(cmd):
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0:
        print(p.stderr[-800:], file=sys.stderr)
        sys.exit(1)


def _norm(t: str) -> str:
    return re.sub(r"[^\w']", "", t).strip("'").lower()


def find_phrase(words, phrase, from_end=False):
    """Locate a phrase's (start, end) in the aligned words."""
    toks = [_norm(t) for t in phrase.split() if _norm(t)]
    normed = [_norm(w["word"]) for w in words]
    rng = range(len(normed) - len(toks), -1, -1) if from_end else range(len(normed) - len(toks) + 1)
    for i in rng:
        if normed[i:i + len(toks)] == toks:
            return words[i]["start"], words[i + len(toks) - 1]["end"]
    return None


def main():
    ap = argparse.ArgumentParser(description="Cut vertical shorts from the long-form render")
    ap.add_argument("script")
    ap.add_argument("--video", default=str(ROOT / "remotion" / "out" / "ep001.mp4"))
    ap.add_argument("--out-dir")
    ap.add_argument("--only", type=int, help="cut just brief N (1-based)")
    ap.add_argument("--config", default=str(ROOT / "config" / "blueprint.json"))
    args = ap.parse_args()

    base = Path(args.script).parent
    config = json.loads(Path(args.config).read_text())
    bk = config["render"]["bookends"]
    offset = bk.get("brand_seconds", 0) + bk.get("title_seconds", 0) - bk.get("j_cut_seconds", 0)

    briefs = json.loads((base / "content" / "shorts_briefs.json").read_text())
    video = Path(args.video)
    if not video.exists():
        print(f"Error: {video} not found — render the long-form first.", file=sys.stderr)
        sys.exit(1)
    out_dir = Path(args.out_dir) if args.out_dir else base / "shorts"
    out_dir.mkdir(exist_ok=True)

    # Section-relative → episode-relative word times.
    timeline = json.loads((base / "vo" / "timeline.json").read_text())
    sec_start = {s["section"]: s["start"] for s in timeline["sections"]}
    tag = ROOT / "music-src" / "kit-oe" / "OE-tag-alt2.wav"  # short "operator" stamp

    made = []
    for n, br in enumerate(briefs, 1):
        if args.only and n != args.only:
            continue
        words = json.loads((base / "vo" / f"words-{br['section']}.json").read_text())["words"]
        head = find_phrase(words, " ".join(br["hook_line"].split()[:4]))
        tail = find_phrase(words, " ".join(br["cliffhanger_line"].split()[-4:]), from_end=True)
        if not head or not tail:
            print(f"⚠ short {n}: couldn't anchor "
                  f"{'hook' if not head else 'cliffhanger'} line in the alignment — skipped "
                  f"(fix the brief lines to match the performed VO; don't guess).")
            continue
        t0 = max(head[0] - PAD_IN + sec_start[br["section"]] + offset, 0)
        t1 = tail[1] + PAD_OUT + sec_start[br["section"]] + offset
        dur = t1 - t0
        if not 10 <= dur <= 179:
            print(f"⚠ short {n}: {dur:.1f}s outside Shorts limits — skipped.")
            continue
        slug = re.sub(r"[^a-z0-9]+", "-", br["title"].lower()).strip("-")[:48]
        out = out_dir / f"short-{n:02d}-{slug}.mp4"
        # 9:16: blurred self-fill behind the centered 16:9 frame; tag on
        # the tail (video fades as "operator" stamps the end).
        tag_at = int(max((dur - 1.6), 0) * 1000)
        run(["ffmpeg", "-hide_banner", "-y", "-loglevel", "error",
             "-ss", f"{t0:.3f}", "-t", f"{dur + 1.0:.3f}", "-i", str(video),
             "-i", str(tag),
             "-filter_complex",
             "[0:v]split=2[bg][fg];"
             "[bg]scale=270:480:force_original_aspect_ratio=increase,crop=270:480,"
             "gblur=sigma=8,eq=brightness=-0.12,scale=1080:1920[bgb];"
             "[fg]scale=1080:-2[fgs];[bgb][fgs]overlay=(W-w)/2:(H-h)/2,"
             f"fade=t=out:st={dur + 0.2:.2f}:d={FADE}[v];"
             f"[0:a]afade=t=out:st={dur - 0.2:.2f}:d=1.2[a0];"
             f"[1:a]adelay={tag_at}|{tag_at},volume=-2dB[t];"
             "[a0][t]amix=inputs=2:duration=first:normalize=0[a]",
             "-map", "[v]", "-map", "[a]",
             "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
             "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(out)])
        made.append((out, dur))
        print(f"  ✓ short {n}: {out.name} ({dur:.1f}s @ {t0:.1f}s)")

    print(f"\n{len(made)}/{len(briefs)} shorts → {out_dir}")


if __name__ == "__main__":
    main()
