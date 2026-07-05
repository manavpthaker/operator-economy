"""
Arrange the music bed from BAR-EXACT LOOPS (v6, 2026-07-04).

Manav's diagnosis of v5: slicing a finished song at arbitrary timestamps
cuts mid-phrase — joins and loop-backs sound chopped. v6 assembles from
a loop KIT cut on the track's own bar grid (99.4 BPM, 2.415s bars,
downbeat-aligned — see music.loops in config):

  chords-8bar   — soft intro melody (opens the video, loops cleanly)
  build-8bar    — the crescendo one-shot (crests at its END)
  beatA-8bar    — main groove (THE DROP, loops)
  beatB-8bar    — variation groove (the n8n screen switch, loops)
  body-16bar    — settled groove for the long middle (loops)
  finale-tail   — the finish + natural fade (one-shot)

Assembly rules:
  - loops repeat WHOLE; same-loop repeats butt-join on the bar (10ms
    declick) — seamless by construction
  - family switches happen on the bar boundary nearest the visual
    anchor (±half a bar tolerance — SoundBed's quote-silences do the
    frame-exact work)
  - the DROP is placed exactly at the first quote's release: the chords
    span is END-ALIGNED by trimming whole bars off its FRONT
  - crescendos are one-shots whose END lands on the crest anchor

Anchors from storyboard.json; re-fits after any VO regen.

Usage:
    python scripts/originate/arrange_bed.py originate/<slug>/script.json

Writes: remotion/public/music/bed.mp3
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
LOOPS = ROOT / "music-src" / "loops"

BAR = 2.415          # seconds (99.38 BPM, 4/4 — Market Pulse grid)
DECLICK = 0.012      # butt-join fade between repeats of the same loop
SWITCH_FADE = 0.35   # family switches, on a bar boundary
DROP_FADE = 0.05     # the drop arrival


def run(cmd: list[str]):
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0:
        print(p.stderr[-1200:], file=sys.stderr)
        sys.exit(1)


def duration_of(path: Path) -> float:
    p = subprocess.run(["ffprobe", "-hide_banner", "-show_entries", "format=duration",
                        "-of", "csv=p=0", str(path)], capture_output=True, text=True)
    return float(p.stdout.strip())


def main():
    ap = argparse.ArgumentParser(description="Arrange the bed from bar-exact loops (v6)")
    ap.add_argument("script")
    ap.add_argument("--config", default=str(ROOT / "config" / "blueprint.json"))
    args = ap.parse_args()

    config = json.loads(Path(args.config).read_text())
    base = Path(args.script).parent
    out = ROOT / "remotion" / "public" / "music" / "bed.mp3"
    out.parent.mkdir(parents=True, exist_ok=True)

    kit = {name: LOOPS / f"{name}.wav" for name in
           ["chords-8bar", "build-8bar", "beatA-8bar", "beatB-8bar", "body-16bar", "finale-tail"]}
    for n, p in kit.items():
        if not p.exists():
            print(f"Error: loop kit incomplete — missing {p}", file=sys.stderr)
            sys.exit(1)
    L = {n: duration_of(p) for n, p in kit.items()}

    timeline = json.loads((base / "vo" / "timeline.json").read_text())
    storyboard = json.loads((base / "storyboard.json").read_text())
    render_data = json.loads((base / "render_data" / "blueprint.json").read_text())

    bk = config.get("render", {}).get("bookends", {})
    offset = bk.get("brand_seconds", 0) + bk.get("title_seconds", 0) - bk.get("j_cut_seconds", 0)
    total = render_data["total_frames"] / render_data["fps"] + 1.0

    screens = storyboard["screens"]
    quotes = [s for s in screens if s["layout"] == "quote"]
    q1 = quotes[0] if quotes else None
    thesis_quotes = [s for s in quotes if s["section"] == "thesis"]
    q_bill = thesis_quotes[-1] if thesis_quotes else None
    sim1 = next((s for s in screens
                 if (s.get("custom") or {}).get("sim", {}).get("kind") == "workflow"), None)
    q1_start = offset + (q1["start"] if q1 else 55.0)
    q1_end = offset + (q1["end"] if q1 else 58.0)
    sim_start = offset + (sim1["start"] if sim1 else q1_end + 25.0)
    bill_start = offset + (q_bill["start"] if q_bill else sim_start + 40.0)
    cta = next((s for s in timeline["sections"] if s["section"] == build_into_id(config)), None)
    target = offset + (cta["start"] if cta else total - 16.0)

    with tempfile.TemporaryDirectory() as td:
        tdp = Path(td)
        segs: list[tuple[Path, float, float]] = []  # (file, dur, join_fade)

        def rep(name: str, loop: str, n_whole: int, front_trim_bars: int = 0) -> Path:
            """n_whole repeats of a loop, optionally trimming whole BARS
            off the front of the first repeat (end-alignment). Length is
            EXPLICIT (-t) — stream_loop output is otherwise unbounded-ish
            (learned the 62-minute way, 2026-07-04)."""
            f = tdp / f"{name}.wav"
            trim = front_trim_bars * BAR
            need = n_whole * duration_of(kit[loop]) - trim
            run(["ffmpeg", "-hide_banner", "-y", "-loglevel", "error",
                 "-stream_loop", str(n_whole + 1), "-i", str(kit[loop]),
                 "-af", f"atrim=start={trim:.3f},asetpts=PTS-STARTPTS,afade=t=in:d={DECLICK}",
                 "-t", f"{need:.3f}", str(f)])
            return f

        # ---- span 1: chords, END-ALIGNED so build crest hits q1_start.
        pre = q1_start - L["build-8bar"]
        n_bars = max(int(round(pre / BAR)), 1)
        n_loops = (n_bars + 7) // 8
        trim_bars = n_loops * 8 - n_bars
        segs.append((rep("chords", "chords-8bar", n_loops, trim_bars), n_bars * BAR, SWITCH_FADE))
        segs.append((kit["build-8bar"], L["build-8bar"], SWITCH_FADE))

        # ---- under the quote (ducked to silence anyway): one quiet bar-fill.
        gap = max(q1_end - q1_start, 0.3)
        uq = tdp / "underq.wav"
        run(["ffmpeg", "-hide_banner", "-y", "-loglevel", "error", "-i", str(kit["chords-8bar"]),
             "-t", f"{gap:.3f}", "-af", "volume=-9dB", str(uq)])
        segs.append((uq, gap, DROP_FADE))

        # ---- THE DROP: beatA whole loops until the bar nearest sim_start.
        n_a = max(int(round((sim_start - q1_end) / L["beatA-8bar"])), 1)
        segs.append((rep("beatA", "beatA-8bar", n_a), n_a * L["beatA-8bar"], SWITCH_FADE))
        t_now = q1_end + n_a * L["beatA-8bar"]

        # ---- variation: beatB until the bar nearest (bill crest - build).
        c2_start = bill_start - L["build-8bar"]
        n_b = max(int(round((c2_start - t_now) / L["beatB-8bar"])), 1)
        segs.append((rep("beatB", "beatB-8bar", n_b), n_b * L["beatB-8bar"], SWITCH_FADE))
        segs.append((kit["build-8bar"], L["build-8bar"], SWITCH_FADE))
        t_now = t_now + n_b * L["beatB-8bar"] + L["build-8bar"]

        # ---- settled body until build3 (end-aligned to cta crest).
        b3_start = target - L["build-8bar"]
        n_body = max(int(round((b3_start - t_now) / L["body-16bar"])), 1)
        segs.append((rep("body", "body-16bar", n_body), n_body * L["body-16bar"], SWITCH_FADE))
        segs.append((kit["build-8bar"], L["build-8bar"], SWITCH_FADE))

        # ---- finale one-shot, then silence to cover total.
        segs.append((kit["finale-tail"], L["finale-tail"], 0.0))

        inputs = []
        for f, _, _ in segs:
            inputs += ["-i", str(f)]
        fc, prev = "", "0:a"
        for i in range(1, len(segs)):
            d = max(segs[i - 1][2], 0.01)
            fc += f"[{prev}][{i}:a]acrossfade=d={d}:c1=tri:c2=tri[x{i}];"
            prev = f"x{i}"
        mixed = tdp / "mixed.mp3"
        run(["ffmpeg", "-hide_banner", "-y", "-loglevel", "error", *inputs,
             "-filter_complex", fc.rstrip(";"), "-map", f"[{prev}]",
             "-ar", "44100", "-b:a", "192k", str(mixed)])
        cur = duration_of(mixed)
        pad = max(total - cur + 2.0, 0.0)
        run(["ffmpeg", "-hide_banner", "-y", "-loglevel", "error", "-i", str(mixed),
             "-af", f"apad=pad_dur={pad:.2f}", "-ar", "44100", "-b:a", "192k", str(out)])

    final = duration_of(out)
    drop_at = q1_end
    print(f"✓ Bed v6 (bar-exact loop assembly) → {out}  ({final:.1f}s vs video {total - 1:.1f}s)")
    print(f"  chords ({n_bars} bars) → crest @ {q1_start:.1f} · DROP @ {drop_at:.1f} · "
          f"beatA ×{n_a} → beatB ×{n_b} @ ~{sim_start:.1f} · crest2 ~{bill_start:.1f} · "
          f"body ×{n_body} → crest3 ~{target:.1f} · finale")


def build_into_id(config) -> str:
    return config.get("music", {}).get("build_into", "cta")


if __name__ == "__main__":
    main()
