#!/usr/bin/env python3
"""Verify the completed EP007 Short 1 transfer and forced word alignment.

The first local Whisper pass recognized all 97 words but interpolated its final
timestamp past EOF. This verifier preserves that failed evidence and validates a
second, local WhisperX 3.8.6 + wav2vec2 forced alignment against the untouched
Original C WAV. It also records the cap-authority pin omitted from the paid-call
preflight without rewriting any completed submission evidence.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import re
import unicodedata
import wave
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
REPO = next(path for path in (HERE, *HERE.parents) if path.name == "operator-economy")
WORK = HERE / "short-01-thirty-day-map"
SCRIPT = REPO / "studio/originate/exit-readiness-prep/shorts-net-new/narration-v3/short-01-thirty-day-map/SCRIPT.txt"
MEDIA = WORK / "media/original-c.wav"
RAW_PCM = WORK / "media/elevenlabs-response.pcm"
WHISPERX_RAW = WORK / "diagnostic-whisperx-direct/original-c.json"
FAILED_ASR = WORK / "FINAL-ASR.json"
FAILED_ASR_RUN = WORK / "FINAL-ASR-RUN.json"
FAILED_TRANSCRIPT = WORK / "asr-final/transcript.json"
PREFLIGHT = WORK / "TRANSFER-PREFLIGHT.json"
ACCOUNT_BEFORE = WORK / "ELEVEN-ACCOUNT-BEFORE.json"
INTENT = WORK / "ELEVEN-SUBMISSION-INTENT.json"
RECEIPT = WORK / "ELEVEN-RECEIPT.json"
ACCOUNT_AFTER = WORK / "ELEVEN-ACCOUNT-AFTER.json"
RUNNER = HERE / "transfer_short01_v4.py"
AUTHORITY = REPO / "blueprint-cinema/episodes/EP007-exit-readiness-prep/review/decisions/ep007-short01-through-video-generation-authorized-v15.json"
CAP_AUTHORITY = REPO / "blueprint-cinema/episodes/EP007-exit-readiness-prep/review/decisions/ep007-short01-guide-replacement-authorized-v11.json"
VERIFIER = Path(__file__).resolve()

PINS = {
    AUTHORITY: "7dbe6c3726017c4b2722f8678d5a6a8c96b97026e83b0e84f293ea3f667253b4",
    CAP_AUTHORITY: "2491451ab40b4ec1fdec61fba89844a827ef630ba12b9364fbd2fbad1b8929de",
    SCRIPT: "9b27c85c9e532c414f4d888045531e082b32b0bbf54b9141d129f9cc5a2aebc0",
    RUNNER: "0a825740ef40a5caefe952b7697c933f925262a04736f81499f7054162c2aa8f",
    PREFLIGHT: "26e6799445326b7bd3d714071fc66de9142dad0c5cdf67cb34bf1c3ccde934ce",
    ACCOUNT_BEFORE: "0dcafea0bcc02788ed3f880e4404737fce755f6cd92cb1b4f1e8a35d5b0334e0",
    INTENT: "251b9f62537495066fe160bee42432c4c906f031345f325c73e809c152c61a1f",
    RECEIPT: "94bd4931f0f93430fc2846d2ab5458a3b961a63acbd3f028e0da1b381c2bfbf3",
    ACCOUNT_AFTER: "b069e6c945afbb9bfbcd011dae25bbbeb8ec708946c8d8c97a6f233e4c401fc8",
    RAW_PCM: "03daf16edb6687e12014069820b801a5c6f8cd8074ad984eaa9960ae47e59823",
    MEDIA: "973c715d273055e1bcac3be16c167cf87b4fe44abb772b63ca72751e06ead1f7",
    FAILED_ASR: "5b4754c4bac38adae540507e767faedb5534cdb4698d86737efdfeb85cfce3bf",
    FAILED_ASR_RUN: "8e57b77a204506f5d9d362e29f00cd0788dbad1ba2fbb8684583643fb43d1ed4",
    FAILED_TRANSCRIPT: "ca2c07480d39a18f446c0d329394ac832c69b6a94b1461db5df45b2239dc9b09",
    WHISPERX_RAW: "05d28d9d88c117c157b5b1ea61448fd6f452df2c83b02e5c5c9be3e4f63c5c60",
}
NUMBER_WORDS = {"30": "thirty"}


def now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def sha_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(REPO))


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def save_json_x(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as handle:
        json.dump(value, handle, indent=2, ensure_ascii=False)
        handle.write("\n")


def normalize_tokens(text: str) -> list[str]:
    text = unicodedata.normalize("NFKC", text).lower().replace("&", " and ")
    tokens = re.findall(r"[a-z0-9]+(?:['’][a-z0-9]+)?", text)
    return [NUMBER_WORDS.get(token, token).replace("'", "").replace("’", "") for token in tokens]


def main() -> None:
    for path, expected in PINS.items():
        actual = sha_file(path)
        if actual != expected:
            raise SystemExit(f"Pinned evidence changed: {rel(path)} expected {expected}, got {actual}")

    authority = read_json(AUTHORITY)
    cap_authority = read_json(CAP_AUTHORITY)
    if authority.get("data", {}).get("verdict") != "accept":
        raise SystemExit("Through-render authority is not accepted")
    cap_text = str(cap_authority.get("data", {}).get("interpretation", ""))
    for required in ("five Google guide calls", "four ElevenLabs transfers", "nine provider calls", "zero further retries", "3200-credit ElevenLabs cap"):
        if required not in cap_text:
            raise SystemExit(f"Cap authority missing: {required}")

    receipt = read_json(RECEIPT)
    intent = read_json(INTENT)
    preflight = read_json(PREFLIGHT)
    if (
        receipt.get("http_status") != 200
        or receipt.get("calls") != 1
        or receipt.get("retries") != 0
        or receipt.get("actual_credit_cost") != 503
        or receipt.get("credit_cap") != 3200
        or receipt.get("voice", {}).get("sha256") != sha_file(MEDIA)
        or receipt.get("raw_response_sha256") != sha_file(RAW_PCM)
        or intent.get("preflight_sha256") != sha_file(PREFLIGHT)
        or intent.get("runner_sha256") != sha_file(RUNNER)
        or intent.get("automatic_retries") != 0
        or preflight.get("estimated_credits_ceiling") != 692
    ):
        raise SystemExit("Completed transfer evidence chain failed")

    failed = read_json(FAILED_ASR)
    failed_run = read_json(FAILED_ASR_RUN)
    if (
        failed.get("exact_normalized_word_match") is not True
        or failed.get("word_timing_within_media_duration") is not False
        or failed.get("accepted_for_picture_production") is not False
        or failed_run.get("stdout_envelope", {}).get("ok") is not True
        or failed_run.get("stdout_envelope", {}).get("engine") != "whisper"
        or failed_run.get("stdout_envelope", {}).get("model") != "small.en"
        or failed_run.get("stdout_envelope", {}).get("wordCount") != 97
        or Path(failed_run.get("stdout_envelope", {}).get("transcriptPath", "")).resolve() != FAILED_TRANSCRIPT.resolve()
        or failed_run.get("source_media_sha256") != sha_file(MEDIA)
    ):
        raise SystemExit("Preserved first-pass ASR evidence is not the expected edge-timing failure")

    raw = read_json(WHISPERX_RAW)
    raw_words = [word for segment in raw.get("segments", []) for word in segment.get("words", []) if str(word.get("word", "")).strip()]
    words = [
        {
            "text": str(word["word"]).strip(),
            "start": float(word["start"]),
            "end": float(word["end"]),
            "score": float(word["score"]),
            "id": f"w{index}",
        }
        for index, word in enumerate(raw_words)
    ]
    with wave.open(str(MEDIA), "rb") as handle:
        duration = handle.getnframes() / handle.getframerate()
        audio_contract = {
            "sample_rate_hz": handle.getframerate(),
            "channels": handle.getnchannels(),
            "sample_width_bits": handle.getsampwidth() * 8,
            "sample_frames": handle.getnframes(),
            "duration_seconds": duration,
        }
    expected = normalize_tokens(SCRIPT.read_text(encoding="utf-8"))
    actual = normalize_tokens(" ".join(word["text"] for word in words))
    values_valid = all(0 <= word["start"] <= word["end"] <= duration for word in words)
    order_valid = all(words[i]["start"] >= words[i - 1]["start"] for i in range(1, len(words)))
    score_valid = all(0 <= word["score"] <= 1 for word in words)
    exact = expected == actual and len(expected) == len(words) == 97
    accepted = exact and values_valid and order_valid and score_valid and words[-1]["end"] <= duration
    if not accepted:
        raise SystemExit("WhisperX forced alignment did not pass exact-copy and media-bound timing gates")

    flat_path = WORK / "asr-final-whisperx/transcript.json"
    result_path = WORK / "FINAL-ASR-WHISPERX.json"
    audit_path = WORK / "TRANSFER-EVIDENCE-AUDIT.json"
    for path in (flat_path, result_path, audit_path):
        if path.exists():
            raise SystemExit(f"Verification output already exists: {rel(path)}")
    save_json_x(flat_path, words)
    flat_sha = sha_file(flat_path)
    save_json_x(result_path, {
        "record_type": "ep007_short01_original_c_forced_alignment_v4",
        "at_utc": now(),
        "status": "pass_exact_normalized_locked_words_and_forced_timings_within_original_media",
        "stage": "final",
        "tool": "whisperx==3.8.6",
        "model": "small",
        "alignment": "wav2vec2",
        "device": "cpu",
        "compute_type": "int8",
        "language": raw.get("language"),
        "source_media": {"path": rel(MEDIA), "sha256": sha_file(MEDIA), **audio_contract},
        "script": {"path": rel(SCRIPT), "sha256": sha_file(SCRIPT)},
        "raw_alignment": {"path": rel(WHISPERX_RAW), "sha256": sha_file(WHISPERX_RAW)},
        "transcript": {
            "path": rel(flat_path),
            "sha256": flat_sha,
            "recognized_words": len(words),
            "locked_normalized_words": len(expected),
            "exact_normalized_word_match": exact,
            "word_timing_values_valid": values_valid,
            "word_timing_order_valid": order_valid,
            "word_timings_within_original_media_duration": values_valid,
            "last_word": words[-1]["text"],
            "last_word_start_seconds": words[-1]["start"],
            "last_word_end_seconds": words[-1]["end"],
            "post_speech_silence_seconds": duration - words[-1]["end"],
            "minimum_word_score": min(word["score"] for word in words),
        },
        "supersedes_for_timing_only": {
            "path": rel(FAILED_ASR),
            "sha256": sha_file(FAILED_ASR),
            "reason": "The first pass recognized the exact words but used segment-interpolated timestamps that extended past EOF; the preserved failure remains evidence of that diagnostic path.",
        },
        "accepted_for_picture_production": True,
        "limitation": "Local forced alignment verifies exact normalized words and media-bound timing. It does not constitute owner listening acceptance of the unseen finished video.",
    })
    save_json_x(audit_path, {
        "record_type": "ep007_short01_transfer_evidence_audit_v4",
        "at_utc": now(),
        "status": "pass_single_call_with_cap_authority_and_post_call_alignment_hardening",
        "verifier_path": rel(VERIFIER),
        "verifier_sha256": sha_file(VERIFIER),
        "through_render_authority": {"path": rel(AUTHORITY), "sha256": sha_file(AUTHORITY)},
        "numeric_cap_authority": {"path": rel(CAP_AUTHORITY), "sha256": sha_file(CAP_AUTHORITY)},
        "caps": {"google_calls": 5, "elevenlabs_calls": 4, "total_provider_calls": 9, "automatic_retries": 0, "elevenlabs_credits": 3200},
        "observed_call": {"elevenlabs_calls": 1, "retries": 0, "http_status": 200, "actual_credits": 503},
        "evidence": [{"path": rel(path), "sha256": sha_file(path)} for path in (RUNNER, PREFLIGHT, ACCOUNT_BEFORE, INTENT, RECEIPT, ACCOUNT_AFTER, RAW_PCM, MEDIA, FAILED_ASR, FAILED_ASR_RUN, FAILED_TRANSCRIPT, WHISPERX_RAW, flat_path, result_path)],
        "result": "Original C is exact-copy, technically complete, and word-timed for picture production. No provider retry occurred or is authorized.",
    })
    print(json.dumps({
        "status": "pass",
        "words": len(words),
        "last_word_end_seconds": words[-1]["end"],
        "media_duration_seconds": duration,
        "post_speech_silence_seconds": duration - words[-1]["end"],
        "actual_credits": receipt["actual_credit_cost"],
    }))


if __name__ == "__main__":
    main()
