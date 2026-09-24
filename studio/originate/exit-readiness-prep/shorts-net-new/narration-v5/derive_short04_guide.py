#!/usr/bin/env python3
"""Make one lossless, silence-tailed Short 04 guide candidate; never touch source."""

from __future__ import annotations

import hashlib
import wave
from pathlib import Path


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "short-04-test-the-front-door/media/guide.wav"
DERIVED = HERE / "short-04-test-the-front-door/media/guide-derived-pad500ms.wav"
SOURCE_SHA = "e93628b53423ea375c8e6a00c5015b70e085bf00d666dc13f2d767df99d9d720"
FRAMES_TO_APPEND = 12000


def sha_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    if sha_file(SOURCE) != SOURCE_SHA:
        raise SystemExit("Preserved Short 04 source hash changed")
    if DERIVED.exists():
        raise SystemExit("Derived candidate already exists; no overwrite")
    with wave.open(str(SOURCE), "rb") as src:
        params = src.getparams()
        if params[:3] != (1, 2, 24000):
            raise SystemExit(f"Unexpected source format: {params}")
        audio = src.readframes(src.getnframes())
    with DERIVED.open("xb") as output:
        with wave.open(output, "wb") as dst:
            dst.setparams(params)
            dst.writeframes(audio)
            dst.writeframes(bytes(FRAMES_TO_APPEND * 2))
    with wave.open(str(DERIVED), "rb") as out:
        if out.getparams()[:3] != params[:3]:
            raise SystemExit("Derived format changed")
        result = out.readframes(out.getnframes())
    if result != audio + bytes(FRAMES_TO_APPEND * 2):
        raise SystemExit("Derived PCM does not equal the original prefix plus zeros")
    if sha_file(SOURCE) != SOURCE_SHA:
        raise SystemExit("Source changed during derivation")
    print(f"{DERIVED}: {sha_file(DERIVED)}")


if __name__ == "__main__":
    main()
