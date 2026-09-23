#!/usr/bin/env python3
"""Prepare two exact Short 04 presenter reference-audio slices without uploads."""

from __future__ import annotations

import hashlib
import subprocess
import wave
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO = next(path for path in (HERE, *HERE.parents) if path.name == "operator-economy")
MASTER = REPO / "studio/originate/exit-readiness-prep/shorts-net-new/narration-v5/short-04-test-the-front-door/media/original-c.wav"
MASTER_SHA = "f25347fae0f78e5ecfaa4b16da55825640fdbc134eab9c5c9abde08ada2171df"
RATE = 48000
SAMPLE_WIDTH = 2
SPECS = (
    ("segment-a", "original-c-opening", 0, 413520, 432000),
    ("segment-b", "original-c-return", 1857360, 2213512, 384000),
)


def sha_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    if sha_file(MASTER) != MASTER_SHA:
        raise SystemExit("Final Original C master changed")
    with wave.open(str(MASTER), "rb") as source:
        params = source.getparams()
        if params[:3] != (1, SAMPLE_WIDTH, RATE):
            raise SystemExit(f"Unexpected master format: {params}")
        frame_count = source.getnframes()
        pcm = source.readframes(frame_count)
    if len(pcm) != frame_count * SAMPLE_WIDTH:
        raise SystemExit("Master PCM length mismatch")

    for folder, stem, start, end, target in SPECS:
        if not (0 <= start < end <= frame_count and end - start <= target):
            raise SystemExit(f"Invalid source range or target for {folder}")
        media = HERE / folder / "media"
        media.mkdir(parents=True, exist_ok=True)
        wav = media / f"{stem}.wav"
        mp3 = media / f"{stem}.mp3"
        if wav.exists() or mp3.exists():
            raise SystemExit(f"No overwrite allowed: {folder}")
        prefix = pcm[start * SAMPLE_WIDTH:end * SAMPLE_WIDTH]
        pad = bytes((target - (end - start)) * SAMPLE_WIDTH)
        with wav.open("xb") as output:
            with wave.open(output, "wb") as destination:
                destination.setparams(params)
                destination.writeframes(prefix)
                destination.writeframes(pad)
        with wave.open(str(wav), "rb") as verify:
            if verify.getparams()[:3] != params[:3] or verify.getnframes() != target:
                raise SystemExit(f"Bad WAV format or duration: {folder}")
            if verify.readframes(target) != prefix + pad:
                raise SystemExit(f"Original PCM or zero handle changed: {folder}")
        subprocess.run(
            ["ffmpeg", "-hide_banner", "-loglevel", "error", "-n", "-i", str(wav),
             "-codec:a", "libmp3lame", "-b:a", "192k", "-ar", str(RATE), "-ac", "1", str(mp3)],
            check=True,
        )
        print(f"{folder}: wav={sha_file(wav)} mp3={sha_file(mp3)} source_frames={end-start} zero_handle_frames={target-(end-start)}")
    if sha_file(MASTER) != MASTER_SHA:
        raise SystemExit("Final Original C master changed during preparation")


if __name__ == "__main__":
    main()
