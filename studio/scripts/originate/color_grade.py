"""
Color-grade a rendered episode via ffmpeg. Documentary look: lifted
shadows (Ink #0E0E0E stays deep but not crushed on YouTube compression),
warm midtones tied to the ledger-gold accent, subtle desat, mild film
grain. Optional: bring your own .cube 3D LUT for a print emulation
(Kodak 2383, FilmConvert, etc.) — the built-in curve is the fallback.

Writes `output/<slug>.graded.mp4`. Original untouched.

Usage:
    python scripts/originate/color_grade.py output/<slug>.mp4
    python scripts/originate/color_grade.py output/<slug>.mp4 --lut path/to/kodak2383.cube
    python scripts/originate/color_grade.py output/<slug>.mp4 --grain 12 --contrast 1.08
    python scripts/originate/color_grade.py output/<slug>.mp4 --stills
    python scripts/originate/color_grade.py output/<slug>.mp4 --commit
"""

import argparse
import subprocess
import sys
from pathlib import Path


def build_filter(lut: Path | None, contrast: float, saturation: float,
                 warmth: float, shadow_lift: float, grain: int) -> str:
    """Chain: [optional LUT] → curves (shadow lift + midtone warmth) →
    eq (contrast + sat) → colorbalance (subtle teal-shadows/warm-highs) →
    grain. Every step is subtle by design — the goal is 'shot on real
    equipment,' not 'graded to death.'"""
    parts: list[str] = []
    if lut:
        parts.append(f"lut3d=file='{lut}'")

    lift = shadow_lift  # 0..0.2 typical
    curve_r = f"0/{lift:.3f} 0.5/{0.5 + warmth*0.02:.3f} 1/1"
    curve_g = f"0/{lift:.3f} 0.5/0.5 1/1"
    curve_b = f"0/{lift:.3f} 0.5/{0.5 - warmth*0.015:.3f} 1/{1 - warmth*0.01:.3f}"
    parts.append(f"curves=r='{curve_r}':g='{curve_g}':b='{curve_b}'")

    parts.append(f"eq=contrast={contrast}:saturation={saturation}")

    # Teal-in-shadows / warm-in-highlights, muted — the doc-channel look.
    parts.append("colorbalance=rs=-0.03:bs=0.04:rh=0.04:bh=-0.03")

    if grain > 0:
        parts.append(f"noise=alls={grain}:allf=t+u")

    return ",".join(parts)


def grade(src: Path, dst: Path, vf: str, crf: int) -> None:
    print(f"→ grading {src.name} → {dst.name}")
    print(f"  filter: {vf}")
    subprocess.run(
        ["ffmpeg", "-hide_banner", "-y", "-loglevel", "warning", "-stats",
         "-i", str(src),
         "-vf", vf,
         "-c:v", "libx264", "-preset", "medium", "-crf", str(crf),
         "-pix_fmt", "yuv420p",
         "-c:a", "copy",
         "-movflags", "+faststart",
         str(dst)],
        check=True,
    )


def extract_stills(src: Path, dst: Path, out_dir: Path,
                   times: list[str]) -> None:
    """Pull matching frames from src and dst at the same timestamps for
    A/B review. Named <base>_<time>_before.png / _after.png."""
    out_dir.mkdir(parents=True, exist_ok=True)
    for t in times:
        tag = t.replace(":", "").replace(".", "")
        for label, mp4 in (("before", src), ("after", dst)):
            png = out_dir / f"{src.stem}_{tag}_{label}.png"
            subprocess.run(
                ["ffmpeg", "-hide_banner", "-y", "-loglevel", "error",
                 "-ss", t, "-i", str(mp4), "-frames:v", "1", str(png)],
                check=True,
            )
    print(f"  A/B stills → {out_dir}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("src", type=Path, help="rendered mp4 (e.g. output/<slug>.mp4)")
    ap.add_argument("--lut", type=Path, default=None,
                    help="optional .cube 3D LUT file")
    ap.add_argument("--contrast", type=float, default=1.06)
    ap.add_argument("--saturation", type=float, default=0.94)
    ap.add_argument("--warmth", type=float, default=1.0,
                    help="0..2, midtone warm push (1 = default)")
    ap.add_argument("--shadow-lift", type=float, default=0.02,
                    help="0..0.1, lifts crushed blacks (YouTube compression)")
    ap.add_argument("--grain", type=int, default=8,
                    help="0..30, ffmpeg noise=alls (8 = subtle film)")
    ap.add_argument("--crf", type=int, default=17,
                    help="x264 quality (17 = visually lossless)")
    ap.add_argument("--stills", action="store_true",
                    help="also extract paired before/after PNGs for A/B")
    ap.add_argument("--still-times", nargs="+",
                    default=["00:00:03", "00:01:30", "00:04:00", "00:07:30"],
                    help="timestamps for --stills (HH:MM:SS)")
    ap.add_argument("--commit", action="store_true",
                    help="after grading, rename .mp4 → .ungraded.mp4 and "
                         ".graded.mp4 → .mp4")
    args = ap.parse_args()

    if not args.src.exists():
        sys.exit(f"Not found: {args.src}")
    if args.lut and not args.lut.exists():
        sys.exit(f"LUT not found: {args.lut}")

    dst = args.src.with_suffix(".graded.mp4")
    vf = build_filter(args.lut, args.contrast, args.saturation,
                      args.warmth, args.shadow_lift, args.grain)

    grade(args.src, dst, vf, args.crf)

    if args.stills:
        extract_stills(args.src, dst, dst.parent / f"{args.src.stem}_ab",
                       args.still_times)

    if args.commit:
        ungraded = args.src.with_suffix(".ungraded.mp4")
        if ungraded.exists():
            sys.exit(f"Refusing to overwrite existing {ungraded.name}")
        args.src.rename(ungraded)
        dst.rename(args.src)
        print(f"\n✓ committed. Original at {ungraded.name}, graded is now {args.src.name}")
    else:
        print(f"\n✓ done. A/B:")
        print(f"  original:  {args.src}")
        print(f"  graded:    {dst}")
        print("Promote with:  --commit")


if __name__ == "__main__":
    main()
