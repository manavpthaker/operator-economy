#!/usr/bin/env python3
"""Align Short 03's locked words to the transferred Original C waveform.

Two independent local Whisper models already recovered the exact copy. The
separate WhisperX ASR transcript made one substitution ("the" for "to") in the
last sentence, so this alignment supplies the locked word there explicitly.
It is timing evidence, not another claim of independent recognition.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
import unicodedata
import wave
from pathlib import Path


sys.dont_write_bytecode = True
REPO = next(path for path in Path(__file__).resolve().parents if path.name == "operator-economy")
BASE = Path(__file__).resolve().parent
SHORT = BASE / "short-03-how-you-charge"
SCRIPT = BASE.parent / "narration-v3/short-03-how-you-charge/SCRIPT.txt"
AUDIO = SHORT / "media/original-c.wav"
RAW = SHORT / "diagnostic-whisperx-final/original-c.json"
OUT = SHORT / "diagnostic-forced-final/transcript.json"
PINS = {
    SCRIPT: "2a56beffef964667fbd09c934130d53171da605e23f876e75a4cb715a03efc3b",
    AUDIO: "c62c09057d6cf1e91b895b485b0cc0114d52707e337b1970112811e9d48ccd83",
    RAW: "47d5872a87673be4b9471ca8e0f9cbf2ca832dfe2e93ddd00125594d42cf42b9",
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalize(value: str) -> list[str]:
    value = unicodedata.normalize("NFKC", value).lower().replace("&", " and ")
    return [part.replace("'", "").replace("’", "") for part in re.findall(r"[a-z0-9]+(?:['’][a-z0-9]+)?", value)]


def main() -> None:
    for path, digest in PINS.items():
        assert path.is_file() and sha(path) == digest, f"Pinned input changed: {path}"
    assert not OUT.exists(), "Alignment output already exists"
    with wave.open(str(AUDIO), "rb") as stream:
        assert (stream.getnchannels(), stream.getsampwidth(), stream.getframerate()) == (1, 2, 48_000)
        duration = stream.getnframes() / stream.getframerate()

    original = json.loads(RAW.read_text(encoding="utf-8"))
    segments = original["segments"]
    assert len(segments) == 8, "Unexpected segmentation"
    assert segments[-1]["text"].count("take the local counsel.") == 1, "Expected one exact WhisperX substitution"
    aligned_input = [
        {"start": float(s["start"]), "end": float(s["end"]), "text": str(s["text"])}
        for s in segments
    ]
    aligned_input[-1]["text"] = aligned_input[-1]["text"].replace("take the local counsel.", "take to local counsel.")
    expected = normalize(SCRIPT.read_text(encoding="utf-8"))
    assert normalize(" ".join(s["text"] for s in aligned_input)) == expected, "Alignment text differs from locked copy"

    import whisperx

    model, metadata = whisperx.load_align_model(language_code="en", device="cpu", model_cache_only=True)
    result = whisperx.align(aligned_input, model, metadata, str(AUDIO), "cpu", interpolate_method="nearest")
    raw_words = [w for s in result["segments"] for w in s.get("words", []) if str(w.get("word", "")).strip()]
    words = [
        {"id": f"w{i}", "text": str(w["word"]).strip(), "start": float(w["start"]), "end": float(w["end"]), "score": float(w["score"])}
        for i, w in enumerate(raw_words)
    ]
    assert len(words) == len(expected) == 98, "Wrong aligned word count"
    assert normalize(" ".join(w["text"] for w in words)) == expected, "Aligned copy differs from locked script"
    assert all(0 <= w["start"] <= w["end"] <= duration for w in words), "Aligned time outside waveform"
    assert all(words[i]["start"] >= words[i - 1]["start"] for i in range(1, len(words))), "Non-monotonic alignment"
    assert all(0 <= w["score"] <= 1 for w in words), "Invalid alignment score"
    OUT.parent.mkdir(exist_ok=False)
    with OUT.open("x", encoding="utf-8") as stream:
        json.dump(words, stream, indent=2, ensure_ascii=False)
        stream.write("\n")
    print(json.dumps({"path": str(OUT.relative_to(REPO)), "sha256": sha(OUT), "words": len(words), "first": words[0], "last": words[-1], "minimum_score": min(w["score"] for w in words)}))


if __name__ == "__main__":
    main()
