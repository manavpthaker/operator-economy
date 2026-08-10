"""
Final loudness master on the rendered mp4. Two-pass ffmpeg loudnorm
locks the mixed audio (VO + bed + SFX) to broadcast delivery
targets — -14 LUFS integrated / -1.5 dBTP / LRA ~9.

Exists because the per-track masters don't guarantee the COMBINED
mix. Per-section VO lands at -14 LUFS integrated (Auphonic or the
local chain); the music bed is normalized to -16 dBFS mean via
volumedetect (dBFS-ish, not LUFS); SoundBed ducks the bed under VO
via screen.music.intensity. The mixdown Remotion writes to the mp4
is whatever falls out of that — nothing measures the combined output.
eval_edit.py PROBES final LUFS but doesn't correct. This IS the
correction step.

Video stream is passthrough (no re-encode). Only audio changes.

Usage:
    python scripts/originate/master_final.py output/<slug>.mp4
    python scripts/originate/master_final.py output/<slug>.mp4 --lufs -14 --tp -1.5 --lra 9
    python scripts/originate/master_final.py output/<slug>.mp4 --commit
"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


def measure(src: Path, lufs: float, tp: float, lra: float) -> dict:
    """Pass 1: measure. loudnorm in analyze mode emits a JSON block on
    stderr with the input's measured loudness stats — those feed the
    linear-mode second pass."""
    print("  measuring...")
    p = subprocess.run(
        ["ffmpeg", "-hide_banner", "-nostats", "-i", str(src),
         "-af", f"loudnorm=I={lufs}:TP={tp}:LRA={lra}:print_format=json",
         "-f", "null", "-"],
        capture_output=True, text=True,
    )
    m = re.search(r"\{[^{}]*input_i[^{}]*\}", p.stderr, re.DOTALL)
    if not m:
        sys.exit(f"loudnorm measurement pass failed:\n{p.stderr[-1500:]}")
    stats = json.loads(m.group(0))
    print(f"  measured: I={stats['input_i']} LUFS · TP={stats['input_tp']} "
          f"dBTP · LRA={stats['input_lra']} LU")
    return stats


def apply(src: Path, dst: Path, stats: dict,
          lufs: float, tp: float, lra: float) -> None:
    """Pass 2: linear normalization using the measured stats. Linear
    mode preserves relative dynamics — no compression, just a static
    gain + peak limit. Anything requiring dynamics changes is handled
    by the per-track masters upstream (Auphonic leveler on VO)."""
    print(f"  applying: I={lufs} · TP={tp} · LRA={lra} · linear...")
    af = (f"loudnorm=I={lufs}:TP={tp}:LRA={lra}"
          f":measured_I={stats['input_i']}"
          f":measured_TP={stats['input_tp']}"
          f":measured_LRA={stats['input_lra']}"
          f":measured_thresh={stats['input_thresh']}"
          f":offset={stats['target_offset']}"
          f":linear=true:print_format=summary")
    subprocess.run(
        ["ffmpeg", "-hide_banner", "-y", "-loglevel", "warning", "-stats",
         "-i", str(src),
         "-c:v", "copy",
         "-af", af,
         "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
         "-movflags", "+faststart",
         str(dst)],
        check=True,
    )


def verify(dst: Path) -> None:
    """Post-pass probe: confirm the output is inside the delivery
    envelope. Prints the numbers; doesn't fail — the user (or
    eval_edit.py) makes the call."""
    p = subprocess.run(
        ["ffmpeg", "-hide_banner", "-nostats", "-i", str(dst),
         "-af", "loudnorm=I=-14:TP=-1:print_format=summary",
         "-f", "null", "-"],
        capture_output=True, text=True,
    )
    for line in p.stderr.splitlines():
        if any(k in line for k in ("Input Integrated", "Input True Peak",
                                    "Input LRA", "Output Integrated",
                                    "Output True Peak", "Output LRA")):
            print(f"  {line.strip()}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("src", type=Path, help="rendered mp4 (or graded mp4)")
    ap.add_argument("--lufs", type=float, default=-14.0)
    ap.add_argument("--tp", type=float, default=-1.5)
    ap.add_argument("--lra", type=float, default=9.0)
    ap.add_argument("--commit", action="store_true",
                    help="rename source to .premaster.mp4 and mastered "
                         "output to source name")
    args = ap.parse_args()

    if not args.src.exists():
        sys.exit(f"Not found: {args.src}")

    dst = args.src.with_suffix(".master.mp4")
    print(f"→ mastering {args.src.name} → {dst.name}")

    stats = measure(args.src, args.lufs, args.tp, args.lra)
    apply(args.src, dst, stats, args.lufs, args.tp, args.lra)

    print("\nverify (input = pre-master, output = mastered):")
    verify(dst)

    if args.commit:
        premaster = args.src.with_suffix(".premaster.mp4")
        if premaster.exists():
            sys.exit(f"Refusing to overwrite existing {premaster.name}")
        args.src.rename(premaster)
        dst.rename(args.src)
        print(f"\n✓ committed. Pre-master at {premaster.name}, "
              f"mastered is now {args.src.name}")
    else:
        print(f"\n✓ done. A/B:")
        print(f"  pre-master: {args.src}")
        print(f"  mastered:   {dst}")
        print("Promote with:  --commit")


if __name__ == "__main__":
    main()
