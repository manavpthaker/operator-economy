#!/usr/bin/env python3
"""Convert local whisper.cpp DTW tokens into the locked narration word table.

This script never invents timestamps. Each locked word receives the exact time
span of one or more observed whisper.cpp tokens. Known ASR lexical differences
are declared and reported; any undeclared mismatch fails closed.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


WORD_RE = re.compile(r"[A-Za-z0-9]+(?:[.:'][A-Za-z0-9]+)*")


def normalize(value: str) -> str:
    token = re.sub(r"[^a-z0-9]", "", value.lower())
    aliases = {
        "acknowledgement": "acknowledgment",
    }
    return aliases.get(token, token)


def canonical_words(text: str) -> list[dict[str, object]]:
    words: list[dict[str, object]] = []
    for index, match in enumerate(WORD_RE.finditer(text)):
        words.append(
            {
                "index": index,
                "word": match.group(0),
                "normalized": normalize(match.group(0)),
                "char_in": match.start(),
                "char_out": match.end(),
            }
        )
    return words


def observed_tokens(payload: dict[str, object]) -> list[dict[str, object]]:
    tokens: list[dict[str, object]] = []
    for item in payload["transcription"]:
        raw = item["text"].strip()
        if not raw:
            continue
        tokens.append(
            {
                "text": raw,
                "normalized": normalize(raw),
                "start": item["offsets"]["from"] / 1000,
                "end": item["offsets"]["to"] / 1000,
            }
        )
    return tokens


def align(locked: list[dict[str, object]], observed: list[dict[str, object]]) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    aligned: list[dict[str, object]] = []
    corrections: list[dict[str, object]] = []
    i = 0
    j = 0
    while i < len(locked) and j < len(observed):
        expected = locked[i]
        actual = observed[j]
        expected_norm = expected["normalized"]
        actual_norm = actual["normalized"]
        source = [actual]
        mode = "exact"

        if expected_norm == actual_norm:
            if expected["word"].lower() != actual["text"].lower():
                mode = "orthographic_alias"
            j += 1
        elif (
            expected_norm == "a"
            and actual_norm == "our"
            and i + 1 < len(locked)
            and locked[i + 1]["normalized"] == "recovery"
        ):
            mode = "asr_substitution"
            corrections.append(
                {
                    "locked_word_index": i,
                    "locked": expected["word"],
                    "observed": actual["text"],
                    "reason": "connected local TTS speech was recognized as 'Our recovery'",
                    "observed_start": actual["start"],
                    "observed_end": actual["end"],
                }
            )
            j += 1
        elif (
            expected_norm == "is"
            and actual_norm == "does"
            and i + 1 < len(locked)
            and j + 1 < len(observed)
            and locked[i + 1]["normalized"] == "not"
            and observed[j + 1]["normalized"] == "not"
        ):
            mode = "asr_substitution"
            corrections.append(
                {
                    "locked_word_index": i,
                    "locked": expected["word"],
                    "observed": actual["text"],
                    "reason": "ASR paraphrased 'is not automate' as 'does not automate'",
                    "observed_start": actual["start"],
                    "observed_end": actual["end"],
                }
            )
            j += 1
        elif (
            expected_norm == "uncertain"
            and actual_norm == "on"
            and j + 1 < len(observed)
            and observed[j + 1]["normalized"] == "certain"
        ):
            source = [actual, observed[j + 1]]
            mode = "asr_merge"
            corrections.append(
                {
                    "locked_word_index": i,
                    "locked": expected["word"],
                    "observed": " ".join(token["text"] for token in source),
                    "reason": "one spoken word was split into two ASR tokens",
                    "observed_start": source[0]["start"],
                    "observed_end": source[-1]["end"],
                }
            )
            j += 2
        else:
            raise SystemExit(
                f"undeclared alignment mismatch at locked[{i}]={expected['word']!r} "
                f"and observed[{j}]={actual['text']!r}"
            )

        aligned.append(
            {
                **expected,
                "start": source[0]["start"],
                "end": source[-1]["end"],
                "observed_tokens": [token["text"] for token in source],
                "alignment": mode,
            }
        )
        i += 1

    if i != len(locked) or j != len(observed):
        raise SystemExit(
            f"alignment length mismatch: locked {i}/{len(locked)}, observed {j}/{len(observed)}"
        )
    return aligned, corrections


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--narration", type=Path, required=True)
    parser.add_argument("--whisper-json", type=Path, required=True)
    parser.add_argument("--words-out", type=Path, required=True)
    parser.add_argument("--report-out", type=Path, required=True)
    parser.add_argument("--audio-duration", type=float, required=True)
    args = parser.parse_args()

    narration = args.narration.read_text(encoding="utf-8")
    whisper = json.loads(args.whisper_json.read_text(encoding="utf-8"))
    locked = canonical_words(narration)
    observed = observed_tokens(whisper)
    words, corrections = align(locked, observed)

    if words and words[-1]["end"] > args.audio_duration:
        overrun = words[-1]["end"] - args.audio_duration
        if overrun > 0.25:
            raise SystemExit(
                f"final DTW token exceeds the waveform by {overrun:.3f}s; refusing to clamp"
            )
        corrections.append(
            {
                "locked_word_index": words[-1]["index"],
                "locked": words[-1]["word"],
                "observed": " ".join(words[-1]["observed_tokens"]),
                "reason": "final DTW boundary was clamped to the exact ffprobe waveform duration",
                "observed_start": words[-1]["start"],
                "observed_end": words[-1]["end"],
                "clamped_end": args.audio_duration,
            }
        )
        words[-1]["end"] = args.audio_duration

    if not words or words[0]["start"] < 0 or words[-1]["end"] > args.audio_duration:
        raise SystemExit("aligned words fall outside the probed audio bounds")
    for left, right in zip(words, words[1:]):
        if left["end"] > right["start"]:
            raise SystemExit(
                f"word timing overlap at {left['index']}->{right['index']}: "
                f"{left['end']} > {right['start']}"
            )

    args.words_out.write_text(
        json.dumps(
            {
                "version": 1,
                "authority": "locked local VO aligned with whisper.cpp DTW token timestamps",
                "audio_duration_seconds": args.audio_duration,
                "word_count": len(words),
                "words": words,
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    args.report_out.write_text(
        json.dumps(
            {
                "version": 1,
                "status": "matched_with_declared_asr_corrections" if corrections else "exact_match",
                "locked_word_count": len(locked),
                "observed_token_count": len(observed),
                "aligned_word_count": len(words),
                "undeclared_mismatches": [],
                "declared_corrections": corrections,
                "timing_source": "whisper.cpp small.en DTW attention alignment; no uniform timing division",
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
