#!/usr/bin/env python3
"""Create two Short03 avatar audio references from the locked Original C PCM.

WAV outputs preserve the selected source samples byte for byte and append only
digital silence to whole-second request durations. MP3s are lossy upload
companions, never the final program-audio authority. No provider calls.
"""
from __future__ import annotations

import hashlib
import io
import json
import subprocess
import sys
import wave
from pathlib import Path


sys.dont_write_bytecode = True
REPO = next(path for path in Path(__file__).resolve().parents if path.name == "operator-economy")
HERE = Path(__file__).resolve().parent
SOURCE = REPO / "studio/originate/exit-readiness-prep/shorts-net-new/narration-v5/short-03-how-you-charge/media/original-c.wav"
EXPECTED_SHA256 = "c62c09057d6cf1e91b895b485b0cc0114d52707e337b1970112811e9d48ccd83"
SAMPLE_RATE = 48_000
SEGMENTS = {
    "a": {"start_frame": 0, "end_frame": 410_880, "request_frames": 9 * SAMPLE_RATE},
    "b": {"start_frame": 1_490_400, "end_frame": 1_805_584, "request_frames": 7 * SAMPLE_RATE},
}


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    before = SOURCE.read_bytes()
    assert sha(before) == EXPECTED_SHA256, "Original C source changed"
    with wave.open(io.BytesIO(before), "rb") as source:
        assert (source.getnchannels(), source.getsampwidth(), source.getframerate()) == (1, 2, SAMPLE_RATE)
        master_frames = source.getnframes()
        pcm = source.readframes(master_frames)
    assert master_frames == 1_805_584 and len(pcm) == master_frames * 2
    for label, spec in SEGMENTS.items():
        folder = HERE / f"segment-{label}" / "media"
        wav = folder / f"original-c-segment-{label}.wav"
        mp3 = folder / f"original-c-segment-{label}.mp3"
        assert not folder.exists() and not wav.exists() and not mp3.exists(), f"Segment {label} output exists"
        start, end, request = spec["start_frame"], spec["end_frame"], spec["request_frames"]
        assert 0 <= start < end <= master_frames and request >= end - start
        selected = pcm[start * 2:end * 2]
        zeros = bytes((request - (end - start)) * 2)
        folder.mkdir(parents=True)
        with wav.open("xb") as stream:
            with wave.open(stream, "wb") as writer:
                writer.setnchannels(1)
                writer.setsampwidth(2)
                writer.setframerate(SAMPLE_RATE)
                writer.writeframes(selected + zeros)
        with wave.open(str(wav), "rb") as output:
            assert (output.getnchannels(), output.getsampwidth(), output.getframerate(), output.getnframes()) == (1, 2, SAMPLE_RATE, request)
            out_pcm = output.readframes(output.getnframes())
        assert out_pcm[: len(selected)] == selected and out_pcm[len(selected):] == zeros, "WAV no longer losslessly preserves source slice"
        subprocess.run([
            "ffmpeg", "-nostdin", "-n", "-hide_banner", "-loglevel", "error", "-i", str(wav),
            "-map_metadata", "-1", "-ac", "1", "-ar", str(SAMPLE_RATE), "-c:a", "libmp3lame", "-b:a", "192k", str(mp3),
        ], check=True)
        assert mp3.is_file() and mp3.stat().st_size > 0, "MP3 companion missing"
        print(json.dumps({
            "segment": label,
            "source_sample_range_end_exclusive": [start, end],
            "source_seconds": [start / SAMPLE_RATE, end / SAMPLE_RATE],
            "source_frames": end - start,
            "digital_zero_pad_frames": request - (end - start),
            "request_duration_seconds": request / SAMPLE_RATE,
            "wav_path": str(wav.relative_to(REPO)),
            "wav_sha256": sha(wav.read_bytes()),
            "mp3_path": str(mp3.relative_to(REPO)),
            "mp3_sha256": sha(mp3.read_bytes()),
        }))
    assert SOURCE.read_bytes() == before, "Original C source was modified"


if __name__ == "__main__":
    main()
