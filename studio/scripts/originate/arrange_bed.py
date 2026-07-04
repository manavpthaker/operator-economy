"""
Arrange the music bed against the episode structure (v4, 2026-07-04).

The bed now covers the WHOLE VIDEO (bookends included — SoundBed is
hoisted above the bookends with a time offset):

  chords   — the track's soft piano/electro intro, from FRAME 0, under
             the brand sting + title card + self-intro
  DROP     — the track's entrance lands exactly on the hook's gap
             screen (the $5.9B slam); beat runs through the opening
             argument and dissolves right after the first quote card's
             silence — so the cut-out is FELT, then melody emerges
  melody   — quiet melodic pools under the body (no beat)
  build    — crescendo cresting at the cta ("The Blueprint")
  finale   — full-energy finish + natural fade under the outro card

Video-time math: content t=0 sits at (brand + title − j_cut) seconds.
Storyboard times are content-relative; everything here shifts by that
offset. Reads storyboard.json for the gap screen + first quote.

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

FLAT_CHAIN = (
    "acompressor=threshold=-28dB:ratio=4:attack=40:release=800:makeup=6,"
    "anequalizer=c0 f=2800 w=2600 g=-5 t=1|c1 f=2800 w=2600 g=-5 t=1,"
    "lowpass=f=7500,"
    "loudnorm=I=-16:TP=-2:LRA=5"
)
# Build/drop/finale keep their dynamics — flattening kills the arrival.
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
    ap = argparse.ArgumentParser(description="Arrange the music bed (video-time, chords→drop→melody→build)")
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

    chords = m.get("chords", [0.0, 20.0])
    drop_time = m.get("drop_time_s", 22.0)
    pools = m.get("melody_pools", [[0, 20]])
    mt = m.get("melody_treatment", {})
    mel_gain, mel_lp = mt.get("gain_db", -4), mt.get("lowpass_hz", 4500)
    build = m.get("build")
    finale = m.get("finale")
    build_into = m.get("build_into", "cta")

    with tempfile.TemporaryDirectory() as td:
        tdp = Path(td)

        def cut(name: str, start: float, end: float, chain: str, extra: str = "") -> Path:
            f = tdp / f"{name}.wav"
            af = chain + ("," + extra if extra else "")
            run(["ffmpeg", "-hide_banner", "-y", "-loglevel", "error",
                 "-ss", f"{start:.3f}", "-to", f"{end:.3f}", "-i", str(track),
                 "-af", af, "-ar", "44100", str(f)])
            return f

        def looped(name: str, src: Path, need: float) -> Path:
            f = tdp / f"{name}.wav"
            run(["ffmpeg", "-hide_banner", "-y", "-loglevel", "error",
                 "-stream_loop", "30", "-i", str(src), "-t", f"{need:.3f}", str(f)])
            return f

        if args.no_arrange:
            flat = tdp / "flat.mp3"
            run(["ffmpeg", "-hide_banner", "-y", "-loglevel", "error", "-i", str(track),
                 "-af", FLAT_CHAIN, "-ar", "44100", "-b:a", "192k", str(flat)])
            flat.replace(out)
            print(f"✓ Treated bed (unarranged, loops) → {out}")
            return

        timeline = json.loads((base / "vo" / "timeline.json").read_text())
        storyboard = json.loads((base / "storyboard.json").read_text())
        render_data = json.loads((base / "render_data" / "blueprint.json").read_text())

        # Video-time offset for content t=0.
        bk = config.get("render", {}).get("bookends", {})
        offset = bk.get("brand_seconds", 0) + bk.get("title_seconds", 0) - bk.get("j_cut_seconds", 0)
        total = render_data["total_frames"] / render_data["fps"] + 1.0  # +1s slack, silence-padded

        screens = storyboard["screens"]
        gap_screen = next((s for s in screens if s["layout"] == "gap"), None)
        first_quote = next((s for s in screens if s["layout"] == "quote"), None)
        drop_at = offset + (gap_screen["start"] if gap_screen else 12.0)
        beat_until = offset + ((first_quote["end"] + 0.4) if first_quote else drop_at + 30.0)

        cta = next((s for s in timeline["sections"] if s["section"] == build_into), None)
        target = offset + (cta["start"] if cta else total - 16.0)
        build_len = (build[1] - build[0]) if build else 0.0
        build_start = max(target - build_len, beat_until + 8.0)

        segs: list[tuple[Path, float]] = []

        # 1) chords from frame 0 → drop (loop the intro pool if short).
        chords_src = cut("chords_src", chords[0], chords[1], DYN_CHAIN, "volume=-2dB")
        need = drop_at + XFADE
        segs.append((looped("chords", chords_src, need), need))

        # 2) THE DROP → beat runs until just past the first quote card.
        beat_need = beat_until - drop_at + XFADE
        segs.append((cut("beat", drop_time, drop_time + beat_need, DYN_CHAIN), beat_need))

        # 3) melody pools → build_start.
        pool_files = [cut(f"pool{i}", s, e, FLAT_CHAIN, f"lowpass=f={mel_lp},volume={mel_gain}dB")
                      for i, (s, e) in enumerate(pools)]
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
            pool_concat = tdp / "pool.wav"
            run(["ffmpeg", "-hide_banner", "-y", "-loglevel", "error", *inputs,
                 "-filter_complex", fc.rstrip(";"), "-map", f"[{prev}]", str(pool_concat)])
        mel_need = build_start - beat_until + XFADE
        segs.append((looped("melody", pool_concat, mel_need), mel_need))

        # 4) build → 5) finale (tail-aligned, natural fade).
        if build:
            segs.append((cut("build", build[0], build[1], DYN_CHAIN), build_len))
        if finale:
            fin_need = total - target
            fin_len = finale[1] - finale[0]
            f_start = finale[0] + max(fin_len - fin_need, 0.0)
            segs.append((cut("finale", f_start, finale[1], DYN_CHAIN), finale[1] - f_start))

        inputs = []
        for f, _ in segs:
            inputs += ["-i", str(f)]
        fc, prev = "", "0:a"
        for i in range(1, len(segs)):
            # Hard-ish arrival into the drop (0.35s), musical everywhere else.
            d = 0.35 if i == 1 else (0.8 if i == len(segs) - 2 and build else XFADE)
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
    print(f"✓ Arranged bed v4 (video-time) → {out}")
    print(f"  {final:.1f}s vs video {total - 1:.1f}s · offset {offset:.1f}s")
    print(f"  chords 0–{drop_at:.1f} · DROP @ {drop_at:.1f} (gap screen) · beat → {beat_until:.1f} "
          f"(first quote release) · melody → {build_start:.1f} · build crests @ {target:.1f} ('{build_into}') · finale → fade")


if __name__ == "__main__":
    main()
