#!/usr/bin/env python3
"""Prepare corrected Short 04 return slice at the measured zero crossing."""

from __future__ import annotations

import hashlib
import subprocess
import wave
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO = next(path for path in (HERE, *HERE.parents) if path.name == "operator-economy")
MASTER = REPO / "studio/originate/exit-readiness-prep/shorts-net-new/narration-v5/short-04-test-the-front-door/media/original-c.wav"
MASTER_SHA = "f25347fae0f78e5ecfaa4b16da55825640fdbc134eab9c5c9abde08ada2171df"
START = 1856836
END = 2213512
TARGET = 384000


def sha_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    if sha_file(MASTER) != MASTER_SHA:
        raise SystemExit("Final Original C master changed")
    with wave.open(str(MASTER), "rb") as source:
        params = source.getparams()
        if params[:3] != (1, 2, 48000) or source.getnframes() != END:
            raise SystemExit("Unexpected final Original C media format or duration")
        pcm = source.readframes(END)
    if pcm[START * 2:START * 2 + 2] != bytes(2):
        raise SystemExit("Selected cut no longer begins at a zero sample")
    media = HERE / "segment-b-v2/media"
    media.mkdir(parents=True, exist_ok=True)
    wav = media / "original-c-return-v2.wav"
    mp3 = media / "original-c-return-v2.mp3"
    if wav.exists() or mp3.exists():
        raise SystemExit("Corrected segment already exists; no overwrite")
    prefix = pcm[START * 2:END * 2]
    tail = bytes((TARGET - (END - START)) * 2)
    with wav.open("xb") as output:
        with wave.open(output, "wb") as destination:
            destination.setparams(params)
            destination.writeframes(prefix)
            destination.writeframes(tail)
    with wave.open(str(wav), "rb") as verify:
        if verify.getparams()[:3] != params[:3] or verify.getnframes() != TARGET:
            raise SystemExit("Corrected WAV format/duration changed")
        if verify.readframes(TARGET) != prefix + tail:
            raise SystemExit("Corrected WAV changed original PCM or nonzero tail")
    subprocess.run(
        ["ffmpeg", "-hide_banner", "-loglevel", "error", "-n", "-i", str(wav),
         "-codec:a", "libmp3lame", "-b:a", "192k", "-ar", "48000", "-ac", "1", str(mp3)],
        check=True,
    )
    if sha_file(MASTER) != MASTER_SHA:
        raise SystemExit("Final Original C master changed during preparation")
    print(f"wav={sha_file(wav)} mp3={sha_file(mp3)} source_frames={END-START} zero_tail_frames={TARGET-(END-START)}")


if __name__ == "__main__":
    main()
