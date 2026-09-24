#!/usr/bin/env python3
"""Losslessly append a 500 ms zero tail to Short 03's preserved Google guide.

This is a local mechanical operation, not synthesis or a provider call.
"""
from __future__ import annotations

import hashlib
import io
import wave
from pathlib import Path


BASE = Path(__file__).resolve().parent / "short-03-how-you-charge" / "media"
SOURCE = BASE / "guide.wav"
DESTINATION = BASE / "guide-derived-pad500ms.wav"
EXPECTED_SHA256 = "91b6658fca45a6ccb9e834d2a806b338d073bf8bafe856c7ec4850a9842035a0"
APPENDED_FRAMES = 12_000


def main() -> None:
    assert SOURCE.is_file() and not DESTINATION.exists(), "Source missing or derivative already exists"
    before = SOURCE.read_bytes()
    assert hashlib.sha256(before).hexdigest() == EXPECTED_SHA256, "Source guide changed"
    with wave.open(io.BytesIO(before), "rb") as reader:
        params = reader.getparams()
        assert params[:3] == (1, 2, 24_000) and params.comptype == "NONE", "Unexpected source format"
        original_frames = reader.getnframes()
        pcm = reader.readframes(original_frames)
    assert len(pcm) == original_frames * 2, "Source PCM length changed"

    with DESTINATION.open("xb") as stream:
        with wave.open(stream, "wb") as writer:
            writer.setnchannels(1)
            writer.setsampwidth(2)
            writer.setframerate(24_000)
            writer.writeframes(pcm + bytes(APPENDED_FRAMES * 2))

    with wave.open(str(DESTINATION), "rb") as reader:
        assert reader.getnframes() == original_frames + APPENDED_FRAMES
        derived_pcm = reader.readframes(reader.getnframes())
    assert derived_pcm[: len(pcm)] == pcm
    assert derived_pcm[len(pcm) :] == bytes(APPENDED_FRAMES * 2)
    assert SOURCE.read_bytes() == before, "Source modified"
    print(f"source_frames={original_frames} appended_frames={APPENDED_FRAMES}")
    print(f"source_pcm_sha256={hashlib.sha256(pcm).hexdigest()}")
    print(f"derived_sha256={hashlib.sha256(DESTINATION.read_bytes()).hexdigest()}")


if __name__ == "__main__":
    main()
