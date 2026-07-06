"""
Prepare native 9:16 shorts for the Short composition (2026-07-06,
replaces cut_shorts.py's letterboxed crops — "we need new videos in
that vertical ratio").

Per brief in content/shorts_briefs.json:
  1. anchors the hook/cliffhanger window in the ElevenLabs alignment
     (phrase-matched, never proportioned),
  2. slices the window's PRE-MIXED audio (VO + bed) from the long-form
     render, fades the tail, stamps the "operator" tag over the end card,
  3. writes window-relative caption groups + props JSON,
  4. prints the render commands (Remotion renders happen locally).

Usage:
    python scripts/originate/prepare_shorts.py originate/<slug>/script.json \
        [--video originate/<slug>/ep001-final.mp4] [--only N]
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
PAD_IN = 0.25
PAD_OUT = 0.45
END_CARD_S = 1.8   # navy end card; tag lands here
WORDS_PER_GROUP = 4


def run(cmd):
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0:
        print(p.stderr[-800:], file=sys.stderr)
        sys.exit(1)


def _norm(t: str) -> str:
    return re.sub(r"[^\w']", "", t).strip("'").lower()


def find_phrase(words, phrase, from_end=False):
    toks = [_norm(t) for t in phrase.split() if _norm(t)]
    normed = [_norm(w["word"]) for w in words]
    rng = range(len(normed) - len(toks), -1, -1) if from_end else range(len(normed) - len(toks) + 1)
    for i in rng:
        if normed[i:i + len(toks)] == toks:
            return words[i]["start"], words[i + len(toks) - 1]["end"]
    return None


def group_words(words, t0, t1):
    """Window-relative caption groups; numbers/money stay gold."""
    win = [w for w in words if w["start"] >= t0 - 0.02 and w["end"] <= t1 + 0.02]
    groups, cur = [], []
    for w in win:
        cur.append({
            "word": w["word"],
            "start": round(w["start"] - t0, 3),
            "end": round(w["end"] - t0, 3),
            "highlight": bool(re.search(r"[\d$%]", w["word"])),
        })
        if len(cur) >= WORDS_PER_GROUP or re.search(r"[.!?]$", w["word"]):
            groups.append(cur)
            cur = []
    if cur:
        groups.append(cur)
    return [{
        "text": " ".join(w["word"] for w in g),
        "words": g,
        "start": g[0]["start"],
        "end": g[-1]["end"],
    } for g in groups]


def main():
    ap = argparse.ArgumentParser(description="Prepare native vertical shorts")
    ap.add_argument("script")
    ap.add_argument("--video")
    ap.add_argument("--only", type=int)
    ap.add_argument("--config", default=str(ROOT / "config" / "blueprint.json"))
    args = ap.parse_args()

    base = Path(args.script).parent
    config = json.loads(Path(args.config).read_text())
    bk = config["render"]["bookends"]
    offset = bk.get("brand_seconds", 0) + bk.get("title_seconds", 0) - bk.get("j_cut_seconds", 0)
    fps = config["render"].get("fps", 30)

    video = Path(args.video) if args.video else base / "ep001-final.mp4"
    if not video.exists():
        video = ROOT / "remotion" / "out" / "ep001.mp4"
    if not video.exists():
        print("Error: no long-form render found.", file=sys.stderr)
        sys.exit(1)

    briefs = json.loads((base / "content" / "shorts_briefs.json").read_text())
    timeline = json.loads((base / "vo" / "timeline.json").read_text())
    sec_start = {s["section"]: s["start"] for s in timeline["sections"]}
    tag = ROOT / "music-src" / "kit-oe" / "OE-tag-alt2.wav"

    pub = ROOT / "remotion" / "public" / "shorts"
    pub.mkdir(parents=True, exist_ok=True)
    rd_dir = base / "render_data"
    rd_dir.mkdir(exist_ok=True)

    cmds = []
    for n, br in enumerate(briefs, 1):
        if args.only and n != args.only:
            continue
        words = json.loads((base / "vo" / f"words-{br['section']}.json").read_text())["words"]
        head = find_phrase(words, " ".join(br["hook_line"].split()[:4]))
        tail = find_phrase(words, " ".join(br["cliffhanger_line"].split()[-4:]), from_end=True)
        if not head or not tail:
            print(f"⚠ short {n}: couldn't anchor the "
                  f"{'hook' if not head else 'cliffhanger'} line — fix the brief, don't guess.")
            continue
        # Section-relative window (for captions) and video-absolute (for audio).
        w0, w1 = head[0] - PAD_IN, tail[1] + PAD_OUT
        v0, v1 = w0 + sec_start[br["section"]] + offset, w1 + sec_start[br["section"]] + offset
        dur = (v1 - v0) + END_CARD_S

        audio_rel = f"shorts/short-{n:02d}.m4a"
        tag_at = int((v1 - v0) * 1000)
        run(["ffmpeg", "-hide_banner", "-y", "-loglevel", "error",
             "-ss", f"{v0:.3f}", "-t", f"{dur:.3f}", "-i", str(video),
             "-i", str(tag),
             "-filter_complex",
             f"[0:a]afade=t=out:st={(v1 - v0) - 0.15:.2f}:d=1.4[a0];"
             f"[1:a]adelay={tag_at}|{tag_at},volume=-2dB[t];"
             "[a0][t]amix=inputs=2:duration=first:normalize=0[a]",
             "-map", "[a]", "-c:a", "aac", "-b:a", "192k", str(pub / f"short-{n:02d}.m4a")])

        props = {
            "slug": f"{base.name}-short-{n:02d}",
            "title": br["title"],
            "kicker": "THE OPERATOR ECONOMY · № 001",
            "audio": audio_rel,
            "duration_seconds": round(dur, 3),
            "fps": fps,
            "groups": group_words(words, w0, w1),
            "end_card_seconds": END_CARD_S,
        }
        pth = rd_dir / f"short-{n:02d}.json"
        pth.write_text(json.dumps(props))
        out = f"out/short-{n:02d}.mp4"
        cmds.append(f"npx remotion render src/index.ts Short {out} --props=../originate/{base.name}/render_data/short-{n:02d}.json")
        print(f"  ✓ short {n}: {dur:.1f}s · {len(props['groups'])} caption groups · {pth.name}")

    if cmds:
        print("\nRender locally (from studio/remotion):")
        for c in cmds:
            print(f"  {c}")


if __name__ == "__main__":
    main()
