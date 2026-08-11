#!/usr/bin/env python3
"""
Research: fetch the banded comp-set thumbnails and tile them for reading.

`contact-sheet.html` renders every tile in a browser by hot-linking
i.ytimg.com. That is the right instrument for a human. It is the wrong one for
anything that has to read the images itself or record what it saw, which is why
`findings.md` shipped as title-only analysis with the images declared the
missing half.

This builds the same comparison as flat PNGs: one grid per channel per band, so
top quartile and bottom quartile can be held side by side, plus a 120px
browse-width simulation (downscale to the real browse width, then nearest-
neighbour back up) that shows what actually survives the shrink.

Findings are in `research/thumbnails/visual-findings.md`.

    build_contact_grids.py --out /tmp/grids [--compset research/thumbnails/compset.json]

Needs ffmpeg on PATH and egress to i.ytimg.com.
"""

from __future__ import annotations

import argparse
import collections
import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]

# Excluded for the reasons findings.md gives: Company Man's pull returned
# 16-year-old personal uploads rather than the documentaries, and Growth in
# Reverse carries no performance claim (219-4,900 views is a newsletter brand's
# incidental YouTube presence).
EXCLUDE = {"Company Man", "Growth in Reverse"}

# The three channels whose register OE is actually in. Kept as a group because
# the hero-number result splits on exactly this line — see visual-findings V2.
REGISTER_LANE = {"Modern MBA", "How Money Works", "MagnatesMedia"}

TILE_W, TILE_H = 560, 315
BROWSE_W = 120               # the width check_thumbnail.py measures
BAND_COLOUR = {"top": "0x2E7D32", "bottom": "0xC62828"}


def run(cmd: list[str]) -> None:
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0:
        raise SystemExit(f"{cmd[0]} failed: {p.stderr.strip()[-400:]}")


def fetch(item: dict, dest: Path) -> bool:
    if dest.exists() and dest.stat().st_size > 5000:
        return True
    # maxresdefault is absent on some older uploads; hqdefault always exists.
    for url in (item["thumb"], item["thumb"].replace("maxresdefault", "hqdefault")):
        subprocess.run(["curl", "-sS", "--max-time", "25", "-o", str(dest), url],
                       capture_output=True)
        if dest.exists() and dest.stat().st_size > 5000:
            return True
    return False


def tile(pattern: str, grid: str, out: Path) -> None:
    run(["ffmpeg", "-y", "-v", "error", "-f", "image2", "-pattern_type", "glob",
         "-i", pattern, "-vf", f"tile={grid}:color=0x101010", "-frames:v", "1", str(out)])


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--compset", type=Path,
                    default=REPO / "research/thumbnails/compset.json")
    a = ap.parse_args()

    rows = [x for x in json.loads(a.compset.read_text())
            if x["band"] in ("top", "bottom") and x["channel"] not in EXCLUDE]
    # Slot order is index-descending so position in the grid means something:
    # the best performer of its band is always the top-left tile.
    rows.sort(key=lambda x: (x["channel"], x["band"], -x["index"]))

    for d in ("thumbs", "labeled", "shrunk", "grids"):
        (a.out / d).mkdir(parents=True, exist_ok=True)

    groups: dict = collections.defaultdict(list)
    slots: dict = collections.Counter()
    missing = []
    for x in rows:
        key = (x["channel"], x["band"])
        slots[key] += 1
        x["slot"] = slots[key]
        x["file"] = a.out / "thumbs" / f"{x['channel'].replace(' ', '')}_{x['band']}_{x['slot']}.jpg"
        if not fetch(x, x["file"]):
            missing.append(x["video_id"])
            continue
        groups[key].append(x)

    if missing:
        print(f"could not fetch {len(missing)}: {missing}", file=sys.stderr)

    # 1. Per-channel banded grids at reading size.
    for (channel, band), items in sorted(groups.items()):
        key = f"{channel.replace(' ', '')}_{band}"
        for x in items:
            run(["ffmpeg", "-y", "-v", "error", "-i", str(x["file"]), "-vf",
                 f"scale={TILE_W}:{TILE_H}:force_original_aspect_ratio=increase,"
                 f"crop={TILE_W}:{TILE_H},pad=iw+12:ih+12:6:6:{BAND_COLOUR[band]}",
                 "-frames:v", "1", str(a.out / "labeled" / f"{key}_{x['slot']}.png")])
        tile(str(a.out / "labeled" / f"{key}_*.png"), "4x2", a.out / "grids" / f"{key}.png")
        print(f"grids/{key}.png  ({len(items)})")

    # 2. Browse-width simulation for the register lane, which is the one that
    #    matters for OE. Nearest-neighbour on the way back up so the upscale
    #    invents nothing that the 120px render did not contain.
    for band in ("top", "bottom"):
        items = sorted((x for (c, b), g in groups.items() if b == band and c in REGISTER_LANE
                        for x in g), key=lambda x: (x["channel"], x["slot"]))
        for i, x in enumerate(items, 1):
            run(["ffmpeg", "-y", "-v", "error", "-i", str(x["file"]), "-vf",
                 f"scale={BROWSE_W}:-2,scale={TILE_W}:{TILE_H}:flags=neighbor,"
                 f"pad=iw+12:ih+12:6:6:0x505050",
                 "-frames:v", "1", str(a.out / "shrunk" / f"{band}_{i:02d}.png")])
        tile(str(a.out / "shrunk" / f"{band}_*.png"), "5x4",
             a.out / "grids" / f"SHRUNK_register_{band}.png")
        print(f"grids/SHRUNK_register_{band}.png  ({len(items)})")

    # 3. The legend. Grid position is the only label — ffmpeg is commonly built
    #    without libfreetype, so drawtext cannot be relied on.
    for (channel, band), items in sorted(groups.items()):
        print(f"\n## {channel} — {band.upper()}  (reading order: 1-4 top row, 5-8 second)")
        for x in items:
            print(f"  {x['slot']}. x{x['index']:.2f}  {x['views']:>9,}  {x['title'][:88]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
