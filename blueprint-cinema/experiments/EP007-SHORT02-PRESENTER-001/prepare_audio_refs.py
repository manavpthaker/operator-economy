#!/usr/bin/env python3
"""Create lossless Short02 Original C slices plus digital-zero provider handles.

This prepares local reference WAVs only; final program audio remains the full
unaltered Original C master. It does not upload or generate anything.
"""
from __future__ import annotations

import hashlib
import json
import wave
from pathlib import Path


REPO = next(p for p in Path(__file__).resolve().parents if p.name == "operator-economy")
HERE = Path(__file__).resolve().parent
MASTER = REPO / "studio/originate/exit-readiness-prep/shorts-net-new/narration-v6/short-02-operations-business/media/original-c.wav"
MASTER_SHA = "fc3a7508c0c17c2d882fa0b9333e57d2eb8ab775b9e1e2d826363f7f9d764eb3"
RATE = 48000
SEGMENTS = (
    ("segment-a", 0, 402000, 0, 9 * RATE),       # master 0.000–8.375; cut 201/24
    ("segment-b", 1457280, 1824000, RATE // 4, 9 * RATE),  # 30.360–38.000, 0.25s head
)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    assert MASTER.is_file() and sha(MASTER) == MASTER_SHA, "Original C master changed"
    with wave.open(str(MASTER), "rb") as stream:
        assert (stream.getnchannels(), stream.getsampwidth(), stream.getframerate()) == (1, 2, RATE)
        frames = stream.getnframes()
        pcm = stream.readframes(frames)
    assert len(pcm) == frames * 2 and frames == 2081994
    report = []
    for name, start, end, head, total in SEGMENTS:
        assert 0 <= start < end <= frames and total >= head + (end - start)
        chosen = pcm[start * 2:end * 2]
        tail = total - head - (end - start)
        out = HERE / name / "media/original-c-reference.wav"
        assert not out.exists(), f"Already prepared; no overwrite: {out}"
        out.parent.mkdir(parents=True, exist_ok=True)
        with out.open("xb") as file:
            with wave.open(file, "wb") as writer:
                writer.setnchannels(1)
                writer.setsampwidth(2)
                writer.setframerate(RATE)
                writer.writeframes(bytes(head * 2) + chosen + bytes(tail * 2))
        with wave.open(str(out), "rb") as stream:
            built = stream.readframes(stream.getnframes())
            assert stream.getnframes() == total
        assert built[head * 2:(head + end - start) * 2] == chosen
        assert built[:head * 2] == bytes(head * 2)
        assert built[(head + end - start) * 2:] == bytes(tail * 2)
        report.append({"segment": name, "path": str(out.relative_to(REPO)), "sha256": sha(out),
                       "master_sample_start": start, "master_sample_end_exclusive": end,
                       "head_zero_frames": head, "tail_zero_frames": tail,
                       "total_frames": total, "duration_seconds": total / RATE,
                       "selected_master_pcm_sha256": hashlib.sha256(chosen).hexdigest()})
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
