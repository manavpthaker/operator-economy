"""
VO layout stage (2026-07-05) — learned from Manav's EP001 GarageBand
session (decoded via cross-correlation against his mix).

His voice grammar, formalized: sections run back-to-back (the 0.85s
breath pads already in the audio), with ONE structural device — a
MUSIC-ONLY BRIDGE inside the hook, right after the series line
("This week?") and before the hook proper. He cut it at 3.5 bars
(~8.45s at 99.4 BPM) — the music steps forward, then the episode starts.

Config (voiceover.layout):
    {"bridges": [{"section": "hook", "after_beat": 0, "bars": 3.5}]}

Runs AFTER generate_vo (per-section caches exist), BEFORE hand_tune:
inserts silence+room-tone into the section audio at the beat boundary,
shifts the cached word timings, then generate_vo's cached path
reassembles words.json/timeline.json with the bridge carried through.
Idempotent via a marker in the section's words cache.

Usage:
    python scripts/originate/layout_vo.py originate/<slug>/script.json
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
BAR = 2.4242424  # 99.00 BPM (OE Theme grid)


def run(cmd):
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0:
        print(p.stderr[-800:], file=sys.stderr)
        sys.exit(1)


def main():
    ap = argparse.ArgumentParser(description="Apply VO layout rules (bridges)")
    ap.add_argument("script")
    ap.add_argument("--config", default=str(ROOT / "config" / "blueprint.json"))
    args = ap.parse_args()

    config = json.loads(Path(args.config).read_text())
    layout = config.get("voiceover", {}).get("layout", {})
    bridges = layout.get("bridges", [])
    if not bridges:
        print("(no layout rules configured — nothing to do)")
        return

    base = Path(args.script).parent
    script = json.loads(Path(args.script).read_text())
    vo_dir = base / "vo"

    for br in bridges:
        sid = br["section"]
        after_beat = br["after_beat"]
        gap = br["bars"] * BAR
        cache_p = vo_dir / f"words-{sid}.json"
        audio_p = vo_dir / f"{sid}.mp3"
        if not cache_p.exists() or not audio_p.exists():
            print(f"⚠ {sid}: caches missing — run generate_vo first")
            continue
        cache = json.loads(cache_p.read_text())
        if cache.get("_bridge_applied"):
            print(f"  {sid}: bridge already applied — skipping")
            continue

        # Where does the beat end? Words are proportioned by beat word
        # counts (same rule as prepare_longform).
        sec = next(s for s in script["sections"] if s["id"] == sid)
        beats = sec["beats"]
        words = cache["words"]
        total_w = sum(len(b["vo_text"].split()) for b in beats) or 1
        cursor = 0
        cut_t = None
        for b in beats:
            n = max(round(len(b["vo_text"].split()) / total_w * len(words)), 1)
            cursor += n
            if b["beat"] == after_beat:
                cut_t = words[min(cursor, len(words)) - 1]["end"] + 0.15
                break
        if cut_t is None:
            print(f"⚠ {sid}: beat {after_beat} not found")
            continue

        # Splice silence into the audio (room tone keeps the air alive).
        pre, post, out = vo_dir / "_pre.mp3", vo_dir / "_post.mp3", vo_dir / "_joined.mp3"
        run(["ffmpeg", "-hide_banner", "-y", "-loglevel", "error", "-i", str(audio_p),
             "-to", f"{cut_t:.3f}", "-af", f"apad=pad_dur={gap:.3f}", "-ar", "44100",
             "-b:a", "192k", str(pre)])
        run(["ffmpeg", "-hide_banner", "-y", "-loglevel", "error", "-i", str(audio_p),
             "-ss", f"{cut_t:.3f}", "-ar", "44100", "-b:a", "192k", str(post)])
        lst = vo_dir / "_concat.txt"
        lst.write_text(f"file '{pre.resolve()}'\nfile '{post.resolve()}'\n")
        run(["ffmpeg", "-hide_banner", "-y", "-loglevel", "error", "-f", "concat",
             "-safe", "0", "-i", str(lst), "-c", "copy", str(out)])
        out.replace(audio_p)
        for f in (pre, post, lst):
            f.unlink(missing_ok=True)

        # Shift the cached words after the cut; grow the duration.
        for w in words:
            if w["start"] >= cut_t:
                w["start"] = round(w["start"] + gap, 3)
                w["end"] = round(w["end"] + gap, 3)
        cache["duration"] = round(cache["duration"] + gap, 3)
        cache["_bridge_applied"] = {"after_beat": after_beat, "bars": br["bars"], "at": round(cut_t, 2)}
        cache_p.write_text(json.dumps(cache))
        print(f"  {sid}: bridge inserted — {br['bars']} bars ({gap:.2f}s) after beat "
              f"{after_beat} @ {cut_t:.2f}s (music steps forward here)")

    print("Re-run generate_vo to reassemble words.json/timeline.json, then the chain.")


if __name__ == "__main__":
    main()
