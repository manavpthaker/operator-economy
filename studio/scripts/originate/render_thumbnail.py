#!/usr/bin/env python3
"""
Originate: render a thumbnail at YouTube's recommended resolution, then check it.

Why this exists (2026-08-13). Amendment A7 verified 3840x2160 as the recommended
size straight from YouTube's Help Center, and every render since has come out at
1280x720 and warned about it. The obvious fix looked like changing the
Composition in Root.tsx to 3840x2160 — and that is the wrong fix. The layout is
full of pixel constants (fontSize 76 and 196, chip base 132, top: 28) and, more
importantly, `check_thumbnail.py` shrinks to 120px to simulate browse width. Both
only mean anything relative to a 1280-wide frame. Tripling the composition would
silently change what "120px" tests.

Remotion's --scale multiplies the OUTPUT while rendering the same layout, so the
composition stays 1280x720 and the file lands at 3840x2160. Verified: the 4K
render downscaled back to 1280 differs from a native 1280 render by a mean of
1.2/255, which is antialiasing on type edges, not movement.

So this wrapper exists to make the correct thing the default thing, rather than a
flag somebody has to remember on every render.

    render_thumbnail.py <props.json> <out.png> [--scale 3] [--no-check]

Requires `npx remotion` in studio/remotion and ffmpeg for the checks.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]          # studio/
REMOTION = ROOT / "remotion"
CHECKER = Path(__file__).resolve().parent / "check_thumbnail.py"

# 1280 * 3 = 3840, which is exactly the recommended width. Not a taste setting:
# see docs/thumbnail-rubric.md amendment A7.
DEFAULT_SCALE = 3


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("props", type=Path, help="props JSON for the Thumbnail composition")
    ap.add_argument("out", type=Path, help="output PNG")
    ap.add_argument("--scale", type=int, default=DEFAULT_SCALE)
    ap.add_argument("--no-check", action="store_true",
                    help="skip check_thumbnail.py afterwards")
    a = ap.parse_args()

    if not a.props.exists():
        print(f"✗ no such props file: {a.props}", file=sys.stderr)
        return 1

    out = a.out.resolve()
    out.parent.mkdir(parents=True, exist_ok=True)

    cmd = ["npx", "remotion", "still", "src/index.ts", "Thumbnail", str(out),
           f"--props={a.props.resolve()}", f"--scale={a.scale}"]
    print(f"rendering at {1280 * a.scale}x{720 * a.scale} …")
    p = subprocess.run(cmd, cwd=REMOTION)
    if p.returncode != 0:
        return p.returncode

    if a.no_check:
        return 0

    # The checker is the point of rendering through here rather than by hand: a
    # thumbnail that is never shrunk to browse width has not been reviewed.
    return subprocess.run([sys.executable, str(CHECKER), str(out)]).returncode


if __name__ == "__main__":
    sys.exit(main())
