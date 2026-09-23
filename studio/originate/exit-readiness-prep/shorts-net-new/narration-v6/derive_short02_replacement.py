#!/usr/bin/env python3
"""Append 500 ms of zero PCM to a separate Short 02 guide copy; no synthesis."""
from __future__ import annotations

import hashlib
import io
import wave
from pathlib import Path


MEDIA = Path(__file__).resolve().parent / "short-02-operations-business/media"
SOURCE = MEDIA / "guide.wav"
DESTINATION = MEDIA / "guide-derived-pad500ms.wav"
EXPECTED_SHA = "aa64af5193083c9a905aac0794b43be2a49d9248c7e31c87e5fab1ee674ed497"
APPENDED_FRAMES = 12000


def main() -> None:
    assert SOURCE.is_file() and not DESTINATION.exists(), "Source missing or derivative already exists"
    before = SOURCE.read_bytes()
    assert hashlib.sha256(before).hexdigest() == EXPECTED_SHA, "Source guide changed"
    with wave.open(io.BytesIO(before), "rb") as reader:
        params = reader.getparams()
        assert params[:3] == (1, 2, 24000) and params.comptype == "NONE", "Unexpected source format"
        original_frames = reader.getnframes()
        pcm = reader.readframes(original_frames)
    assert len(pcm) == original_frames * 2, "Source PCM length changed"
    with DESTINATION.open("xb") as stream:
        with wave.open(stream, "wb") as writer:
            writer.setnchannels(1)
            writer.setsampwidth(2)
            writer.setframerate(24000)
            writer.writeframes(pcm + bytes(APPENDED_FRAMES * 2))
    with wave.open(str(DESTINATION), "rb") as reader:
        assert reader.getnframes() == original_frames + APPENDED_FRAMES
        derived_pcm = reader.readframes(reader.getnframes())
    assert derived_pcm[:len(pcm)] == pcm
    assert derived_pcm[len(pcm):] == bytes(APPENDED_FRAMES * 2)
    assert SOURCE.read_bytes() == before
    print(f"source_frames={original_frames} appended_frames={APPENDED_FRAMES}")
    print(f"source_pcm_sha256={hashlib.sha256(pcm).hexdigest()}")
    print(f"derived_sha256={hashlib.sha256(DESTINATION.read_bytes()).hexdigest()}")


if __name__ == "__main__":
    main()
