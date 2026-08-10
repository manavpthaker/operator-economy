#!/usr/bin/env python3
"""
Originate: mechanical thumbnail checks — docs/thumbnail-rubric.md §Enforcement

Why this exists (2026-08-10). EP005's thumbnail shipped alongside a note that
self-certified "Rule 6 ✓ the number dominates; 'NOT A STORY' reads at
browse-strip size." The file was 2272x1198 (not 16:9), 94% fully transparent
(no background in the file at all), and its secondary text resolved to roughly
2px of cap height at browse width.

`prepare_thumbnail.py` checks the WORDS — ≤4, no title overlap, no kicker. It
has never looked at the pixels. That is the hole this closes: EP003 shipped
with no thumbnail and drew 0.0% CTR on 142 impressions, and the guard written
in response checked everything except the image.

Checks here are mechanical only, using ffmpeg/ffprobe which are already hard
dependencies. Nothing subjective is scored: face, composition, and the
curiosity gap need eyes, and `thumbnail-rubric.md` still governs them. What
this refuses to permit is a note claiming a pass on a rule that is measurable.

    check_thumbnail.py <image.png> [--json] [--min-width N]

Exit 0 = pass, 1 = at least one FAIL. Warnings never fail the run.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

# YouTube's stated minimum is 1280x720; it flattens uploads to JPEG.
MIN_W, MIN_H = 1280, 720
TARGET_AR = 16 / 9
AR_TOLERANCE = 0.01          # 1% — 1.896 (EP005) is 6.6% off and fails
BROWSE_W = 120               # the browse-strip width the shrink test targets

# Composited on white, a thumbnail whose content vanishes at browse width
# trends toward pure white. EP005 sits at ~250. A dense thumbnail sits far
# lower. This is an emptiness floor, not a taste judgement.
MAX_BROWSE_YAVG_ON_WHITE = 245
MIN_BROWSE_YAVG_ON_BLACK = 12
MIN_BROWSE_LUMA_RANGE = 60   # YMAX-YMIN at browse width


class CheckError(RuntimeError):
    pass


def _run(cmd: list[str]) -> str:
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0:
        raise CheckError(f"{cmd[0]} failed: {p.stderr.strip()[-400:]}")
    return p.stdout


def probe_stream(path: Path) -> dict[str, str]:
    out = _run([
        "ffprobe", "-v", "error", "-select_streams", "v:0",
        "-show_entries", "stream=width,height,pix_fmt",
        "-of", "default=noprint_wrappers=1", str(path),
    ])
    return dict(
        line.split("=", 1) for line in out.strip().splitlines() if "=" in line
    )


def signalstats(graph: str) -> dict[str, float]:
    """Run a lavfi graph ending in signalstats and return its Y metrics."""
    out = _run([
        "ffprobe", "-v", "error", "-f", "lavfi", "-i", graph,
        "-show_entries", "frame_tags", "-of", "default=noprint_wrappers=1",
    ])
    stats: dict[str, float] = {}
    for m in re.finditer(r"lavfi\.signalstats\.(Y\w+)=([-\d.]+)", out):
        stats.setdefault(m.group(1), float(m.group(2)))
    return stats


def flatten(path: Path, w: int, h: int, bg: str, dest: Path) -> None:
    """Composite the image over a solid background so alpha is resolved the
    way YouTube's JPEG conversion resolves it."""
    _run([
        "ffmpeg", "-y", "-v", "error",
        "-f", "lavfi", "-i", f"color={bg}:s={w}x{h}",
        "-i", str(path),
        "-filter_complex", "[0][1]overlay",
        "-frames:v", "1", "-update", "1", str(dest),
    ])


def check(path: Path, min_width: int) -> tuple[list[str], list[str], dict]:
    fails: list[str] = []
    warns: list[str] = []

    stream = probe_stream(path)
    w, h = int(stream["width"]), int(stream["height"])
    pix_fmt = stream.get("pix_fmt", "")
    facts: dict = {"width": w, "height": h, "pix_fmt": pix_fmt}

    # 1. Alpha. YouTube flattens to JPEG; transparency becomes black, so the
    #    design that was reviewed is not the design that ships.
    if "a" in re.sub(r"\d|le|be|p$", "", pix_fmt):
        alpha = signalstats(f"movie={path},alphaextract,signalstats")
        a_min = alpha.get("YMIN", 255)
        a_avg = alpha.get("YAVG", 255)
        facts["alpha_min"] = a_min
        facts["alpha_mean"] = a_avg
        if a_min < 255:
            opaque_pct = 100 * a_avg / 255
            fails.append(
                f"has an alpha channel ({pix_fmt}); only ~{opaque_pct:.0f}% opaque. "
                f"YouTube flattens to JPEG and transparency composites to black, "
                f"so what ships is not what you reviewed. Export on a real background."
            )

    # 2. Aspect ratio.
    ar = w / h
    facts["aspect"] = round(ar, 4)
    if abs(ar - TARGET_AR) / TARGET_AR > AR_TOLERANCE:
        off = 100 * abs(ar - TARGET_AR) / TARGET_AR
        fails.append(
            f"aspect {ar:.3f} is {off:.1f}% off 16:9 ({TARGET_AR:.3f}). "
            f"YouTube pads or crops it. Export {min_width}x{round(min_width * 9 / 16)}."
        )

    # 3. Dimensions.
    if w < min_width or h < round(min_width * 9 / 16):
        fails.append(f"{w}x{h} is under the {min_width}x{round(min_width*9/16)} minimum")

    # 4 + 5. What survives the shrink, resolved on both backgrounds because a
    #        transparent or near-white thumbnail behaves differently on each.
    with tempfile.TemporaryDirectory() as td:
        for bg in ("white", "black"):
            flat = Path(td) / f"flat-{bg}.png"
            flatten(path, w, h, bg, flat)
            s = signalstats(f"movie={flat},scale={BROWSE_W}:-1,signalstats")
            y_avg = s.get("YAVG", 0.0)
            y_rng = s.get("YMAX", 0.0) - s.get("YMIN", 0.0)
            facts[f"browse_yavg_on_{bg}"] = round(y_avg, 1)
            facts[f"browse_range_on_{bg}"] = round(y_rng, 1)

            if bg == "white" and y_avg > MAX_BROWSE_YAVG_ON_WHITE:
                fails.append(
                    f"at {BROWSE_W}px on white the image averages {y_avg:.0f}/255 — "
                    f"effectively blank. Content is not surviving the shrink."
                )
            if bg == "black" and y_avg < MIN_BROWSE_YAVG_ON_BLACK:
                fails.append(
                    f"at {BROWSE_W}px on black the image averages {y_avg:.0f}/255 — "
                    f"effectively blank."
                )
            if y_rng < MIN_BROWSE_LUMA_RANGE:
                warns.append(
                    f"luma range {y_rng:.0f} on {bg} at {BROWSE_W}px is below "
                    f"{MIN_BROWSE_LUMA_RANGE}; low separation against YouTube's UI"
                )

    return fails, warns, facts


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("image", type=Path)
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    ap.add_argument("--min-width", type=int, default=MIN_W)
    a = ap.parse_args()

    if not a.image.exists():
        print(f"✗ no such file: {a.image}", file=sys.stderr)
        return 1

    try:
        fails, warns, facts = check(a.image, a.min_width)
    except CheckError as e:
        print(f"✗ {e}", file=sys.stderr)
        return 1

    if a.json:
        print(json.dumps({"pass": not fails, "fails": fails,
                          "warns": warns, "facts": facts}, indent=2))
        return 1 if fails else 0

    print(f"thumbnail check — {a.image.name}")
    print(f"  {facts['width']}x{facts['height']}  ar={facts['aspect']}  {facts['pix_fmt']}")
    for w_ in warns:
        print(f"  warn  {w_}")
    for f_ in fails:
        print(f"  FAIL  {f_}")
    if fails:
        print(f"\n{len(fails)} failure(s). The rubric's subjective rules still "
              f"need your eyes; these were only the measurable ones.")
        return 1
    print("\nok — mechanical checks pass. Composition still needs a human read.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
