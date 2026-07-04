"""
Arrange the music bed against the episode structure (2026-07-03).

Not a loop — an ARRANGEMENT. Reads storyboard.json to find the episode's
first quote card (the silence-riser moment) and places the track so its
drop lands exactly as that quote releases. Layout:

  [filtered crate-dust loop]  → under the hook (low-passed, -5dB)
  [track 0 → drop]            → natural run-up under the opening argument
  [DROP at first-quote end]   → music returns from the quote silence
                                WITH the drop — the edit IS the moment
  [body loops, 1s crossfades] → steady under the middle sections
  [track's own outro/fade]    → lands at content end

Voice-agnostic: re-run after any VO regeneration (timings come from
storyboard.json + render_data). The treatment chain (flatten dynamics,
carve the speech band, normalize) is applied first — generate/export
tracks raw and loud; this script makes them broadcast-shaped.

Usage:
    python scripts/originate/arrange_bed.py originate/<slug>/script.json \
        [--track music-src/crate-grit-v1.mp3] [--drop 10.0] \
        [--body 40 136] [--outro 155] [--no-arrange]  # --no-arrange = treat+loop only

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

TREAT_CHAIN = (
    "acompressor=threshold=-28dB:ratio=4:attack=40:release=800:makeup=6,"
    "anequalizer=c0 f=2800 w=2600 g=-5 t=1|c1 f=2800 w=2600 g=-5 t=1,"
    "lowpass=f=7500,"
    "loudnorm=I=-16:TP=-2:LRA=5"
)

XFADE = 1.0  # seconds between body loops


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
    ap = argparse.ArgumentParser(description="Arrange the music bed against the storyboard")
    ap.add_argument("script")
    ap.add_argument("--track", default=None, help="Raw track (defaults to config music.track)")
    ap.add_argument("--drop", type=float, default=None, help="Drop time in the track (s)")
    ap.add_argument("--body", nargs=2, type=float, default=None, help="Loopable body region [start end]")
    ap.add_argument("--outro", type=float, default=None, help="Track outro start (s); plays to track end")
    ap.add_argument("--config", default=str(ROOT / "config" / "blueprint.json"))
    ap.add_argument("--no-arrange", action="store_true", help="Treat + install only (bed loops as-is)")
    args = ap.parse_args()

    config = json.loads(Path(args.config).read_text())
    m_cfg = config.get("music", {})
    track = Path(args.track or (ROOT / m_cfg.get("track", "")))
    if not track.is_absolute():
        track = ROOT / track
    if not track.exists():
        print(f"Error: track not found: {track}", file=sys.stderr)
        sys.exit(1)
    drop = args.drop if args.drop is not None else m_cfg.get("drop_time_s", 10.0)
    body = args.body or m_cfg.get("body", [40.0, 136.0])
    outro_start = args.outro if args.outro is not None else m_cfg.get("outro_start_s", 155.0)

    base = Path(args.script).parent
    out = ROOT / "remotion" / "public" / "music" / "bed.mp3"
    out.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory() as td:
        tdp = Path(td)
        flat = tdp / "flat.mp3"
        print(f"Treating {track.name} (flatten + carve + normalize)…")
        run(["ffmpeg", "-hide_banner", "-y", "-loglevel", "error", "-i", str(track),
             "-af", TREAT_CHAIN, "-ar", "44100", "-b:a", "192k", str(flat)])
        track_len = duration_of(flat)

        if args.no_arrange:
            flat.replace(out)
            print(f"✓ Treated bed (unarranged, will loop) → {out}")
            return

        storyboard = json.loads((base / "storyboard.json").read_text())
        render_data = json.loads((base / "render_data" / "blueprint.json").read_text())
        total = float(render_data["duration_seconds"]) + 2.0  # +2s so SoundBed's loop never wraps

        first_quote = next((s for s in storyboard["screens"] if s["layout"] == "quote"), None)
        anchor = (first_quote["end"] + 0.15) if first_quote else 12.0
        print(f"  drop lands at content t={anchor:.2f}s "
              f"({'after ' + first_quote['id'] if first_quote else 'default'})")

        segs: list[tuple[Path, float]] = []  # (file, duration)

        def cut(name: str, start: float, end: float, extra_af: str | None = None) -> Path:
            f = tdp / f"{name}.wav"
            af = extra_af or "anull"
            run(["ffmpeg", "-hide_banner", "-y", "-loglevel", "error",
                 "-ss", f"{start:.3f}", "-to", f"{end:.3f}", "-i", str(flat),
                 "-af", af, str(f)])
            return f

        pre_gap = anchor - drop
        if pre_gap > 0.5:
            # Filtered crate-dust under the hook, looped to length.
            dust_src = cut("dust_src", 0.0, min(7.5, drop - 1.0),
                           "lowpass=f=1000,volume=-5dB")
            dust = tdp / "dust.wav"
            run(["ffmpeg", "-hide_banner", "-y", "-loglevel", "error",
                 "-stream_loop", "8", "-i", str(dust_src),
                 "-t", f"{pre_gap + XFADE:.3f}", str(dust)])
            segs.append((dust, pre_gap + XFADE))
            main_start = 0.0
        else:
            main_start = drop - anchor  # trim the track head so the drop still lands

        main = cut("main", main_start, outro_start)
        segs.append((main, outro_start - main_start))

        outro = cut("outro", outro_start, track_len)
        outro_len = track_len - outro_start

        # Fill the middle with body loops until the outro closes at `total`.
        placed = sum(d for _, d in segs) - XFADE * (len(segs) - 1)
        body_len = body[1] - body[0]
        fill = total - placed - outro_len + XFADE
        n_loops = 0
        while fill > XFADE + 4.0:
            n_loops += 1
            seg_len = min(body_len, fill)
            segs.append((cut(f"body{n_loops}", body[0], body[0] + seg_len), seg_len))
            fill -= seg_len - XFADE
        segs.append((outro, outro_len))

        # Chain with acrossfades.
        inputs: list[str] = []
        for f, _ in segs:
            inputs += ["-i", str(f)]
        fc, prev = "", "0:a"
        for i in range(1, len(segs)):
            label = f"x{i}"
            fc += f"[{prev}][{i}:a]acrossfade=d={XFADE}:c1=tri:c2=tri[{label}];"
            prev = label
        fc = fc.rstrip(";")
        run(["ffmpeg", "-hide_banner", "-y", "-loglevel", "error", *inputs,
             "-filter_complex", fc, "-map", f"[{prev}]",
             "-ar", "44100", "-b:a", "192k", str(out)])

    final = duration_of(out)
    print(f"✓ Arranged bed → {out}")
    print(f"  {final:.1f}s (content {total - 2:.1f}s) · dust {max(pre_gap, 0):.1f}s · "
          f"drop @ {anchor:.1f}s · {n_loops} body loop(s) · natural outro")


if __name__ == "__main__":
    main()
