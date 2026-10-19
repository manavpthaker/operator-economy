#!/usr/bin/env python3
"""Build the private, phone-readable EP009 Shorts contact-sheet review package."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path


REPO = Path(__file__).resolve().parents[3]
ROOT = Path(__file__).resolve().parent
QA_ROOT = REPO / "blueprint-cinema/experiments/EP009-FULL-BUILD-001/assembly/qa"
OUTPUT = QA_ROOT / "ep009-shorts-r1"
PAGE_SOURCE = REPO / "blueprint-cinema/episodes/EP009-direct-booking-recovery/agents/deliverables/ep009-shorts-review-page/index.html"
SHORT02 = REPO / "blueprint-cinema/episodes/EP009-direct-booking-recovery/agents/deliverables/ep009-short02-hyperframes-prototype/project"

SOURCES = {
    "short-01.png": ROOT / "01-second-commission/snapshots",
    "short-02.png": SHORT02 / "review/final-frames-r1",
    "short-03.png": ROOT / "03-guest-book/snapshots",
    "short-04.png": ROOT / "04-wrong-number/snapshots",
}


def frames(folder: Path) -> list[Path]:
    found = sorted(folder.glob("frame-*-at-*.png"))
    if not found:
        raise SystemExit(f"no review frames found in {folder}")
    return found


def build_sheet(source_frames: list[Path], output: Path) -> None:
    tile_w, tile_h = 360, 640
    rows = (len(source_frames) + 1) // 2
    args = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y"]
    for frame in source_frames:
        args.extend(["-i", str(frame)])

    filters = []
    labels = []
    positions = []
    for index in range(len(source_frames)):
        label = f"v{index}"
        filters.append(
            f"[{index}:v]scale={tile_w}:{tile_h}:force_original_aspect_ratio=decrease,"
            f"pad={tile_w}:{tile_h}:(ow-iw)/2:(oh-ih)/2:color=0x111713[{label}]"
        )
        labels.append(f"[{label}]")
        positions.append(f"{(index % 2) * tile_w}_{(index // 2) * tile_h}")
    filters.append(
        f"{''.join(labels)}xstack=inputs={len(source_frames)}:layout={'|'.join(positions)}:"
        f"fill=0x111713:shortest=1[sheet]"
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    args.extend(
        [
            "-filter_complex",
            ";".join(filters),
            "-map",
            "[sheet]",
            "-frames:v",
            "1",
            str(output),
        ]
    )
    subprocess.run(args, check=True)
    expected_height = rows * tile_h
    probe = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-select_streams",
            "v:0",
            "-show_entries",
            "stream=width,height",
            "-of",
            "csv=p=0:s=x",
            str(output),
        ],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    if probe != f"720x{expected_height}":
        raise SystemExit(f"unexpected sheet size for {output}: {probe}")


def main() -> None:
    if not PAGE_SOURCE.exists():
        raise SystemExit(f"missing review page source: {PAGE_SOURCE}")
    OUTPUT.mkdir(parents=True, exist_ok=True)
    shutil.copy2(PAGE_SOURCE, OUTPUT / "index.html")
    for name, source in SOURCES.items():
        selected = frames(source)
        build_sheet(selected, OUTPUT / "contact-sheets" / name)
        print(f"built {name}: {len(selected)} frames")
    print(f"review package: {OUTPUT.relative_to(REPO)}")


if __name__ == "__main__":
    main()
