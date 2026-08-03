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

Trailer mode (--trailer, 2026-07-14): reads content/trailer_brief.json and
stitches 2-4 NON-CONTIGUOUS beats (jump cuts, 60ms anti-click fades) into one
~25s pre-launch montage + end card. Caption groups get cumulative offsets so
the one Short composition renders it unchanged; end-card copy is overridden
with the Monday-drop announcement from the brief.

Usage:
    python scripts/originate/prepare_shorts.py originate/<slug>/script.json \
        [--video originate/<slug>/ep001-final.mp4] [--only N] [--trailer]
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
EPISODES_JSON = ROOT.parent / "site" / "data" / "episodes.json"
PAD_IN = 0.25
PAD_OUT = 0.45
END_CARD_S = 1.8   # navy end card; tag lands here
TRAILER_END_CARD_S = 2.6  # trailer card carries the drop date — needs read time
WORDS_PER_GROUP = 4


def episode_number(slug: str) -> int | None:
    """Resolve this episode's number from the site registry.

    The kicker used to be hardcoded to "№ 001" — every EP003 short shipped
    with the wrong episode number burned into the title card (found
    2026-07-31). site/data/episodes.json is the single source of truth for
    numbering, so read it rather than restating it here.
    """
    try:
        data = json.loads(EPISODES_JSON.read_text())
    except (OSError, json.JSONDecodeError) as e:
        print(f"⚠ can't read {EPISODES_JSON}: {e}", file=sys.stderr)
        return None
    for ep in data.get("episodes", []):
        if ep.get("slug") == slug:
            return ep.get("number")
    return None


def kicker_for(slug: str) -> str:
    num = episode_number(slug)
    if num is None:
        # Don't silently stamp a wrong number — that's the bug this replaced.
        print(f"⚠ no episodes.json entry for '{slug}' — kicker will omit the "
              f"episode number. Add the entry, then re-run.", file=sys.stderr)
        return "THE OPERATOR ECONOMY"
    return f"THE OPERATOR ECONOMY · № {num:03d}"


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


def prepare_trailer(base, video, tag, pub, rd_dir, fps, offset, sec_start):
    """Stitch the trailer montage: non-contiguous beats → one audio + props."""
    brief_path = base / "content" / "trailer_brief.json"
    if not brief_path.exists():
        print("⚠ no trailer_brief.json — run derive_content.py first (derivation.trailer).")
        return None
    tb = json.loads(brief_path.read_text())

    # Anchor every segment before cutting anything.
    segs = []
    for i, sg in enumerate(tb["segments"], 1):
        words = json.loads((base / "vo" / f"words-{sg['section']}.json").read_text())["words"]
        head = find_phrase(words, " ".join(sg["first_line"].split()[:4]))
        tail = find_phrase(words, " ".join(sg["last_line"].split()[-4:]), from_end=True)
        if not head or not tail:
            print(f"⚠ trailer seg {i} ({sg['section']}): couldn't anchor the "
                  f"{'first' if not head else 'last'} line — fix the brief, don't guess.")
            return None
        w0, w1 = head[0] - PAD_IN, tail[1] + PAD_OUT
        segs.append({"words": words, "w0": w0, "w1": w1,
                     "v0": w0 + sec_start[sg["section"]] + offset,
                     "dur": w1 - w0})

    total = sum(s["dur"] for s in segs)
    dur = total + TRAILER_END_CARD_S
    tag_at = int(total * 1000)

    # One ffmpeg pass: slice each beat (anti-click fades), concat as jump cuts,
    # pad the end card, land the tag over it.
    fc, labels = [], []
    for i, s in enumerate(segs):
        fade_out = max(s["dur"] - 0.06, 0)
        fc.append(f"[0:a]atrim=start={s['v0']:.3f}:end={s['v0'] + s['dur']:.3f},"
                  f"asetpts=PTS-STARTPTS,afade=t=in:d=0.06,"
                  f"afade=t=out:st={fade_out:.3f}:d=0.06[s{i}]")
        labels.append(f"[s{i}]")
    fc.append(f"{''.join(labels)}concat=n={len(segs)}:v=0:a=1,"
              f"afade=t=out:st={max(total - 0.15, 0):.2f}:d=1.4,"
              f"apad=pad_dur={TRAILER_END_CARD_S}[a0]")
    fc.append(f"[1:a]adelay={tag_at}|{tag_at},volume=-2dB[t]")
    fc.append("[a0][t]amix=inputs=2:duration=first:normalize=0[a]")
    run(["ffmpeg", "-hide_banner", "-y", "-loglevel", "error",
         "-i", str(video), "-i", str(tag),
         "-filter_complex", ";".join(fc),
         "-map", "[a]", "-c:a", "aac", "-b:a", "192k", str(pub / "trailer.m4a")])

    # Captions: segment-relative groups shifted onto the stitched timeline.
    groups, t_off = [], 0.0
    for s in segs:
        for g in group_words(s["words"], s["w0"], s["w1"]):
            groups.append({
                "text": g["text"],
                "words": [{**w, "start": round(w["start"] + t_off, 3),
                           "end": round(w["end"] + t_off, 3)} for w in g["words"]],
                "start": round(g["start"] + t_off, 3),
                "end": round(g["end"] + t_off, 3),
            })
        t_off += s["dur"]

    props = {
        "slug": f"{base.name}-trailer",
        "title": tb["title"],
        "kicker": "THE OPERATOR ECONOMY · TRAILER",
        "audio": "shorts/trailer.m4a",
        "duration_seconds": round(dur, 3),
        "fps": fps,
        "groups": groups,
        "end_card_seconds": TRAILER_END_CARD_S,
        "end_card_title": tb.get("end_card_title", "The full breakdown drops Monday"),
        "end_card_sub": tb.get("end_card_sub", "MONDAY 11 AM ET"),
    }
    pth = rd_dir / "trailer.json"
    pth.write_text(json.dumps(props))
    print(f"  ✓ trailer: {dur:.1f}s · {len(segs)} beats · {len(groups)} caption groups · {pth.name}")
    return f"npx remotion render src/index.ts Short out/trailer.mp4 --props=../originate/{base.name}/render_data/trailer.json"


def main():
    ap = argparse.ArgumentParser(description="Prepare native vertical shorts")
    ap.add_argument("script")
    ap.add_argument("--video")
    ap.add_argument("--only", type=int)
    ap.add_argument("--trailer", action="store_true",
                    help="also stitch the pre-launch montage trailer from content/trailer_brief.json")
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
            "kicker": kicker_for(base.name),
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

    if args.trailer:
        tcmd = prepare_trailer(base, video, tag, pub, rd_dir, fps, offset, sec_start)
        if tcmd:
            cmds.append(tcmd)

    if cmds:
        print("\nRender locally (from studio/remotion):")
        for c in cmds:
            print(f"  {c}")


if __name__ == "__main__":
    main()
