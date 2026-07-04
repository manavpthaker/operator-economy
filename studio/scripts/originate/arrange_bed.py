"""
Arrange the music bed against the episode structure (v3, 2026-07-03).

Market Pulse grammar — melody-forward with ONE structural build:

  melody   — the track's quiet melodic passages (intro, breakdowns),
             gently treated, looped under most of the episode. No beat.
  build    — the track's crescendo, placed so it CRESTS exactly at the
             `build_into` section start (the Blueprint reveal). Kept
             dynamically alive (light treatment) so the rise survives.
  finale   — the track's full-energy finish + natural fade, carrying
             the CTA through the outro card.

config/blueprint.json `music`:
  track, melody_pools [[s,e],...], melody_treatment {gain_db, lowpass_hz},
  build [s,e], finale [s,e], build_into "<section id>"

Voice-agnostic and idempotent: re-run after any VO regeneration.

Usage:
    python scripts/originate/arrange_bed.py originate/<slug>/script.json [--no-arrange]

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

# Full broadcast treatment: flattens dynamics — right for under-VO
# melody, WRONG for the build (it IS dynamics), which gets DYN_CHAIN.
FLAT_CHAIN = (
    "acompressor=threshold=-28dB:ratio=4:attack=40:release=800:makeup=6,"
    "anequalizer=c0 f=2800 w=2600 g=-5 t=1|c1 f=2800 w=2600 g=-5 t=1,"
    "lowpass=f=7500,"
    "loudnorm=I=-16:TP=-2:LRA=5"
)
DYN_CHAIN = (
    "anequalizer=c0 f=2800 w=2600 g=-4 t=1|c1 f=2800 w=2600 g=-4 t=1,"
    "lowpass=f=8000,"
    "loudnorm=I=-16:TP=-2:LRA=9"
)

XFADE = 1.2


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
    ap = argparse.ArgumentParser(description="Arrange the music bed (melody + build grammar)")
    ap.add_argument("script")
    ap.add_argument("--config", default=str(ROOT / "config" / "blueprint.json"))
    ap.add_argument("--no-arrange", action="store_true")
    args = ap.parse_args()

    config = json.loads(Path(args.config).read_text())
    m = config.get("music", {})
    track = ROOT / m.get("track", "")
    if not track.exists():
        print(f"Error: track not found: {track}", file=sys.stderr)
        sys.exit(1)

    base = Path(args.script).parent
    out = ROOT / "remotion" / "public" / "music" / "bed.mp3"
    out.parent.mkdir(parents=True, exist_ok=True)

    pools = m.get("melody_pools", [[0, 20]])
    mt = m.get("melody_treatment", {})
    mel_gain = mt.get("gain_db", -4)
    mel_lp = mt.get("lowpass_hz", 4500)
    build = m.get("build")            # [start, end] — crests at end
    finale = m.get("finale")          # [start, end] — includes natural fade
    build_into = m.get("build_into")  # section id

    with tempfile.TemporaryDirectory() as td:
        tdp = Path(td)

        def cut(name: str, start: float, end: float, chain: str, extra: str = "") -> Path:
            f = tdp / f"{name}.wav"
            af = chain + ("," + extra if extra else "")
            run(["ffmpeg", "-hide_banner", "-y", "-loglevel", "error",
                 "-ss", f"{start:.3f}", "-to", f"{end:.3f}", "-i", str(track),
                 "-af", af, "-ar", "44100", str(f)])
            return f

        if args.no_arrange:
            flat = tdp / "flat.mp3"
            run(["ffmpeg", "-hide_banner", "-y", "-loglevel", "error", "-i", str(track),
                 "-af", FLAT_CHAIN, "-ar", "44100", "-b:a", "192k", str(flat)])
            flat.replace(out)
            print(f"✓ Treated bed (unarranged, loops) → {out}")
            return

        timeline = json.loads((base / "vo" / "timeline.json").read_text())
        total = float(timeline["total_seconds"]) + 2.0
        target_start = None
        if build_into:
            sec = next((s for s in timeline["sections"] if s["section"] == build_into), None)
            if sec:
                target_start = sec["start"]
        if target_start is None:
            target_start = total - (finale[1] - finale[0] if finale else 15.0)

        # Segment plan (content time):
        #   [0 .. build_start)          melody loops
        #   [build_start .. target)     the build, cresting at target
        #   [target .. total]           the finale (trimmed to fit, keeps
        #                               its natural fade at the tail)
        build_len = (build[1] - build[0]) if build else 0.0
        build_start = max(target_start - build_len, 0.0)

        # Melody pool: concatenate treated pool segments, then loop.
        pool_files = [cut(f"pool{i}", s, e, FLAT_CHAIN,
                          f"lowpass=f={mel_lp},volume={mel_gain}dB")
                      for i, (s, e) in enumerate(pools)]
        pool_concat = tdp / "pool.wav"
        if len(pool_files) == 1:
            pool_concat = pool_files[0]
        else:
            inputs = []
            for f in pool_files:
                inputs += ["-i", str(f)]
            fc, prev = "", "0:a"
            for i in range(1, len(pool_files)):
                fc += f"[{prev}][{i}:a]acrossfade=d={XFADE}:c1=tri:c2=tri[p{i}];"
                prev = f"p{i}"
            run(["ffmpeg", "-hide_banner", "-y", "-loglevel", "error", *inputs,
                 "-filter_complex", fc.rstrip(";"), "-map", f"[{prev}]", str(pool_concat)])

        melody_need = build_start + XFADE
        melody = tdp / "melody.wav"
        run(["ffmpeg", "-hide_banner", "-y", "-loglevel", "error",
             "-stream_loop", "30", "-i", str(pool_concat),
             "-t", f"{melody_need:.3f}", str(melody)])

        segs = [(melody, melody_need)]
        if build:
            segs.append((cut("build", build[0], build[1], DYN_CHAIN), build_len))
        if finale:
            fin_need = total - target_start
            fin_len = finale[1] - finale[0]
            # Keep the TAIL (natural fade); trim from the front if long,
            # pad understanding: if short, it just ends early into the +2s slack.
            f_start = finale[0] + max(fin_len - fin_need, 0.0) if fin_len > fin_need else finale[0]
            segs.append((cut("finale", f_start, finale[1], DYN_CHAIN), finale[1] - f_start))

        inputs = []
        for f, _ in segs:
            inputs += ["-i", str(f)]
        fc, prev = "", "0:a"
        for i in range(1, len(segs)):
            # Short crossfade into the build so the rise reads as arriving,
            # not fading in.
            d = 0.8 if i == 1 and build else XFADE
            fc += f"[{prev}][{i}:a]acrossfade=d={d}:c1=tri:c2=tri[x{i}];"
            prev = f"x{i}"
        mixed = tdp / "mixed.mp3"
        run(["ffmpeg", "-hide_banner", "-y", "-loglevel", "error", *inputs,
             "-filter_complex", fc.rstrip(";"), "-map", f"[{prev}]",
             "-ar", "44100", "-b:a", "192k", str(mixed)])
        # Pad the tail with silence out past `total` so SoundBed's loop
        # can never wrap and restart the melody after the finale fades.
        cur = duration_of(mixed)
        pad = max(total - cur + 2.0, 0.0)
        run(["ffmpeg", "-hide_banner", "-y", "-loglevel", "error", "-i", str(mixed),
             "-af", f"apad=pad_dur={pad:.2f}", "-ar", "44100", "-b:a", "192k", str(out)])

    final = duration_of(out)
    print(f"✓ Arranged bed (melody + build) → {out}")
    print(f"  {final:.1f}s vs content {total - 2:.1f}s")
    print(f"  melody 0–{build_start:.1f}s · build {build_start:.1f}–{target_start:.1f}s "
          f"(crests at '{build_into}') · finale {target_start:.1f}s → natural fade")


if __name__ == "__main__":
    main()
