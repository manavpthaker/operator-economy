#!/usr/bin/env python3
"""Governed EP007 narration continuation after the rejected Short 1 guide.

This runner preserves narration-v2 as immutable failed evidence, permits exactly
four new Google submissions (one Short 1 replacement plus Shorts 2-4), and then
permits four Original C transfers only if every guide passes. The prior failed
Google call and its estimated cost count against the cumulative authorization.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import math
import sys
from pathlib import Path
from typing import Any


sys.dont_write_bytecode = True
WRAPPER = Path(__file__).resolve()
BASE = WRAPPER.parent
REPO = next(path for path in (BASE, *BASE.parents) if path.name == "operator-economy")
ENGINE_PATH = REPO / "studio/originate/exit-readiness-prep/shorts-net-new/narration-v1/capture_shorts.py"
V2 = REPO / "studio/originate/exit-readiness-prep/shorts-net-new/narration-v2"
FRESH_AUTH = REPO / "blueprint-cinema/episodes/EP007-exit-readiness-prep/review/decisions/ep007-owner-authorize-short01-guide-replacement-20260922.json"
FRESH_EVENT = REPO / "blueprint-cinema/episodes/EP007-exit-readiness-prep/review/decisions/ep007-short01-guide-replacement-authorized-v11.json"

spec = importlib.util.spec_from_file_location("ep007_narration_engine_v2", ENGINE_PATH)
if spec is None or spec.loader is None:
    raise SystemExit("Could not load the pinned narration engine")
engine = importlib.util.module_from_spec(spec)
spec.loader.exec_module(engine)


PRIOR_GOOGLE_CALLS = 1
PRIOR_ELEVEN_CALLS = 0
PRIOR_PROVIDER_CALLS = 1
PRIOR_GOOGLE_ESTIMATED_USD = 0.0197845
AGGREGATE_GOOGLE_CALL_CAP = 5
AGGREGATE_ELEVEN_CALL_CAP = 4
AGGREGATE_PROVIDER_CALL_CAP = 9
AGGREGATE_GOOGLE_ESTIMATED_USD_CAP = 0.15
AGGREGATE_ELEVEN_CREDIT_CAP = 3200

PIN_MAP = {
    REPO / "studio/originate/exit-readiness-prep/shorts-net-new/STANDALONE-SCRIPTS-V3.json": "6be1ee7c13ba6fc607d215e9a61c74fda31cc3f60026632eff6fc029f903cf6c",
    REPO / "studio/originate/exit-readiness-prep/shorts-net-new/NARRATION-CAPTURE-PROPOSAL-V1.json": "c8404afd3b31153558a83c66e6f32a0d6a44a60570f237b8584bddddeb44e100",
    REPO / "studio/originate/exit-readiness-prep/shorts-net-new/PRODUCTION-MANIFEST-V2.json": "cc925469a415e7d0405a21c6874d63586635d5fbb1c4ac5b2d7f82ab0fd0d4ad",
    REPO / "blueprint-cinema/episodes/EP007-exit-readiness-prep/review/decisions/ep007-owner-authorize-shorts-narration-20260922.json": "93f402d0ce7594af5205727731b846b37962015cd5943e0048ef12ae121d0751",
    FRESH_AUTH: "b1543594cfe65f63a011afeb69add2faa98cc88a90bac17566ade3fb77f791a7",
    REPO / "blueprint-cinema/episodes/EP007-exit-readiness-prep/review/decisions/ep007-shorts-narration-authorized-v9.json": "4dec13834c073cbd4a6c2488230a259d310734be9be5df31b325381372efd971",
    REPO / "blueprint-cinema/episodes/EP007-exit-readiness-prep/review/decisions/ep007-shorts-narration-batch-hold-v10.json": "638c10e27cdc462d759b1955043dea076f1925e41a79f8e11413965a19efb8e4",
    FRESH_EVENT: "2491451ab40b4ec1fdec61fba89844a827ef630ba12b9364fbd2fbad1b8929de",
    REPO / "operator-blueprint-v2/02-narration-production/prompts/NARRATOR-REGISTER.candidate-C4.google-gemini-tts.style-instructions.json": "b747d7b0afa4469b2be05c20eb16306a25bb5185b9fa8b12e2d4aa4ddd8d3efc",
    REPO / "operator-blueprint-v2/02-narration-production/tools/calibrate.py": "d59303278dbb79bef6fe0080f1d2b6c1e701e9228e95c7b3cdea4f3eec78cc00",
    REPO / "operator-blueprint-v2/02-narration-production/tools/capture_n4b.py": "5e1093bc0f0113fa998bd5e99359f90b098342cc83c19997ed77ab0f02a15493",
    ENGINE_PATH: "96395c162129d971ebf9bd7f798e65422392f0cc5891d0800b4c856835bd579b",
    V2 / "RUN-INPUT.json": "8b5caad5c4efd49cbee28ccdc4de4c1f7dc78a22df1ef8c6c555c355fd55fa9d",
    V2 / "BATCH-HOLD.json": "39b2cf50d6b995f15c18282b633739888fe768c1cec25c75151a0ffc976e9cd8",
    V2 / "short-01-thirty-day-map/GOOGLE-SUBMISSION-INTENT.json": "5d86f0c216a25b1142fa55a7be767c2545e08cd00e3ed5ce57e25f7d1be62430",
    V2 / "short-01-thirty-day-map/GOOGLE-RECEIPT.json": "b0421bed901afde1571459868a38bc7579a3378fb0a86373599523406684734d",
    V2 / "short-01-thirty-day-map/media/guide.wav": "e0f3b2dcbb1a6ec16f63268845be8151cd94f96612156a898bc559234507d089",
    V2 / "short-01-thirty-day-map/media/google-response.bin": "7b2ff7b4b5544970e08f639f0fb1ce0b0245bdde0e55fdfa2af73f60c740c484",
    V2 / "short-01-thirty-day-map/diagnostic-asr-guide/transcript.json": "be2f41374de2e69da05df01a5ce5dba95fa5c7a2decfbc4a36e8544a07521b81",
}

V2_INPUT_PINS = {
    "short-01-thirty-day-map": {
        "GOOGLE-REQUEST.json": "7401a413a73ac4a371cb4a9987ba25de14e07f49048bcf1d8ed047daf27b407f",
        "SCRIPT.txt": "9b27c85c9e532c414f4d888045531e082b32b0bbf54b9141d129f9cc5a2aebc0",
        "STYLE.json": "f0bb3a6b581764b85dcd02df9b434a27fe0066b4b6f66347905a5baca48f1c5d",
        "TRANSFER-INPUT.json": "ea0f4c94ad7dd92acddf053fb581fe46f00bd936039d9f96e766e6d159c3f34b",
        "VOICE-INPUT.json": "87ba8b3d42b692e50f8a9fb7ed232cf209eb7947202bebc2c9c9881a2309fec7",
    },
    "short-02-operations-business": {
        "GOOGLE-REQUEST.json": "51d3d17749feaab1f9c9ccb1ddafe3dce81c90b92a17f23892c34a867a97c36e",
        "SCRIPT.txt": "aee361d4542ed450365a50c70577f6b1bddd61c30de0571d770cbd91b0ed5542",
        "STYLE.json": "f0bb3a6b581764b85dcd02df9b434a27fe0066b4b6f66347905a5baca48f1c5d",
        "TRANSFER-INPUT.json": "ea0f4c94ad7dd92acddf053fb581fe46f00bd936039d9f96e766e6d159c3f34b",
        "VOICE-INPUT.json": "640d1b2e0563158e5a8d8da2499d04a5f3a39138c84ade4819394516cd1588a5",
    },
    "short-03-how-you-charge": {
        "GOOGLE-REQUEST.json": "b6d22f29b829d3c80bab7595316df85ace329c70367e379440c315f49fea4983",
        "SCRIPT.txt": "2a56beffef964667fbd09c934130d53171da605e23f876e75a4cb715a03efc3b",
        "STYLE.json": "f0bb3a6b581764b85dcd02df9b434a27fe0066b4b6f66347905a5baca48f1c5d",
        "TRANSFER-INPUT.json": "ea0f4c94ad7dd92acddf053fb581fe46f00bd936039d9f96e766e6d159c3f34b",
        "VOICE-INPUT.json": "1581240ce8529124b9a9eb28b3837ff0f723dbdb49ad09a6a3ff61b39d25075a",
    },
    "short-04-test-the-front-door": {
        "GOOGLE-REQUEST.json": "b8e9bcf0a36eaec8420190264813ca4162fc8f2f55581a27b74a903c0dfe0eae",
        "SCRIPT.txt": "fb1021dc78cfb7c717aacdcef665d69a3651b6db8c0b9b129dab3e6c1b6ea60f",
        "STYLE.json": "f0bb3a6b581764b85dcd02df9b434a27fe0066b4b6f66347905a5baca48f1c5d",
        "TRANSFER-INPUT.json": "ea0f4c94ad7dd92acddf053fb581fe46f00bd936039d9f96e766e6d159c3f34b",
        "VOICE-INPUT.json": "799ae423a3babb4d04ec8a171799ab3aa398f99bf8620c2c28ea106bac149cc9",
    },
}


def assert_pins_v3() -> None:
    for path, expected in PIN_MAP.items():
        actual = engine.sha_file(path)
        if actual != expected:
            raise SystemExit(f"Pinned input changed: {engine.rel(path)} expected {expected}, got {actual}")
    for short_id, files in V2_INPUT_PINS.items():
        for name, expected in files.items():
            path = V2 / short_id / name
            if engine.sha_file(path) != expected:
                raise SystemExit(f"Pinned v2 prepared input changed: {engine.rel(path)}")
    auth = json.loads(FRESH_AUTH.read_text(encoding="utf-8"))
    exact = {
        "replacement_short_id": "short-01-thirty-day-map",
        "replacement_google_guide_calls_max": 1,
        "google_guide_calls_max_aggregate": AGGREGATE_GOOGLE_CALL_CAP,
        "elevenlabs_transfer_calls_max_aggregate": AGGREGATE_ELEVEN_CALL_CAP,
        "provider_calls_max_aggregate": AGGREGATE_PROVIDER_CALL_CAP,
        "additional_retries": 0,
        "automatic_retries": 0,
        "google_spend_cap_usd_aggregate_estimate": AGGREGATE_GOOGLE_ESTIMATED_USD_CAP,
        "elevenlabs_credit_cap_aggregate": AGGREGATE_ELEVEN_CREDIT_CAP,
        "guide_model": "gemini-2.5-pro-tts",
        "guide_voice": "Algieba",
        "transfer_model": "eleven_multilingual_sts_v2",
        "transfer_voice": "Original C",
        "transfer_voice_id": "scMbPZwQjr40V1MzL3Nj",
    }
    if auth.get("owner_verbatim") != "Approved":
        raise SystemExit("Fresh owner authorization does not contain exact approval")
    for key, expected in exact.items():
        if auth.get("authorized", {}).get(key) != expected:
            raise SystemExit(f"Fresh authorization mismatch for {key}")
    consumed = auth.get("authorization_context", {}).get("already_consumed", {})
    expected_consumed = {
        "google_guide_calls": PRIOR_GOOGLE_CALLS,
        "elevenlabs_transfer_calls": PRIOR_ELEVEN_CALLS,
        "provider_generation_calls": PRIOR_PROVIDER_CALLS,
        "estimated_google_usd": PRIOR_GOOGLE_ESTIMATED_USD,
    }
    if consumed != expected_consumed:
        raise SystemExit("Fresh authorization does not bind the consumed failed call exactly")
    rejected = json.loads((V2 / "short-01-thirty-day-map/GOOGLE-RECEIPT.json").read_text(encoding="utf-8"))
    if rejected.get("accepted") is not False or rejected.get("guide", {}).get("sha256") != PIN_MAP[V2 / "short-01-thirty-day-map/media/guide.wav"]:
        raise SystemExit("Rejected v2 Short 1 guide disposition drifted")


original_save_json_x = engine.save_json_x
original_require_prepared = engine.require_prepared
original_assert_batch_clear = engine.assert_batch_clear
original_normalize_tokens = engine.normalize_tokens
original_transfer_preflight = engine.transfer_preflight


def input_bindings() -> list[dict[str, Any]]:
    bindings = []
    for short_id, files in V2_INPUT_PINS.items():
        rows = []
        for name, expected in files.items():
            v2_path = V2 / short_id / name
            v3_path = BASE / short_id / name
            if engine.sha_file(v2_path) != expected:
                raise SystemExit(f"Pinned v2 prepared input changed: {short_id}/{name}")
            v3_sha = engine.sha_file(v3_path)
            binding_type = "byte_identical"
            if name == "VOICE-INPUT.json":
                v2_voice = json.loads(v2_path.read_text(encoding="utf-8"))
                v3_voice = json.loads(v3_path.read_text(encoding="utf-8"))
                expected_v3_voice = dict(v2_voice)
                expected_v3_voice["script_path"] = engine.rel(BASE / short_id / "SCRIPT.txt")
                if v3_voice != expected_v3_voice:
                    raise SystemExit(f"v3 voice input does not equal v2 semantics with corrected provenance: {short_id}")
                binding_type = "semantic_identity_with_v3_script_path"
            elif v3_sha != expected:
                raise SystemExit(f"v3 prepared input is not byte-identical to v2: {short_id}/{name}")
            rows.append({
                "name": name,
                "v2_path": engine.rel(v2_path),
                "v3_path": engine.rel(v3_path),
                "v2_sha256": expected,
                "v3_sha256": v3_sha,
                "binding_type": binding_type,
            })
        bindings.append({"short_id": short_id, "files": rows})
    return bindings


def current_google_cost_v3() -> float:
    total = PRIOR_GOOGLE_ESTIMATED_USD
    for row in engine.scripts():
        receipt = BASE / row["id"] / "GOOGLE-RECEIPT.json"
        if receipt.exists():
            total += float(json.loads(receipt.read_text(encoding="utf-8")).get("estimated_cost_usd_conservative_input_tokens", 0))
    return total


def strict_asr_fields(value: dict[str, Any]) -> None:
    transcript_path = REPO / str(value["transcript_path"])
    words = json.loads(transcript_path.read_text(encoding="utf-8"))
    transcript = " ".join(str(word.get("text", "")) for word in words)
    media_path = next(
        path for path in BASE.rglob("*.wav") if engine.sha_file(path) == value.get("media_sha256")
    )
    script_path = media_path.parent.parent / "SCRIPT.txt"
    expected = original_normalize_tokens(script_path.read_text(encoding="utf-8"))
    actual = original_normalize_tokens(transcript)
    strict_match = expected == actual
    allowed = []
    acoustic_match = len(expected) == len(actual)
    if acoustic_match:
        for index, (left, right) in enumerate(zip(expected, actual)):
            if left == right:
                continue
            if {left, right} == {"write", "right"}:
                allowed.append({"index": index, "expected": left, "asr": right, "basis": "acoustically identical closed homophone pair"})
                continue
            acoustic_match = False
            break
    first_mismatch = next(
        (index for index, pair in enumerate(zip(expected, actual)) if pair[0] != pair[1]),
        min(len(expected), len(actual)) if len(expected) != len(actual) else None,
    )
    timing_pass = bool(
        value.get("word_timing_values_valid")
        and value.get("word_timing_order_valid")
        and value.get("word_timing_within_media_duration")
    )
    value.update({
        "expected_normalized_tokens": expected,
        "asr_normalized_tokens": actual,
        "expected_token_count": len(expected),
        "asr_token_count": len(actual),
        "strict_orthographic_normalized_word_match": strict_match,
        "exact_normalized_word_match": strict_match,
        "closed_homophone_equivalence_policy": [{"expected": "write", "asr": "right"}, {"expected": "right", "asr": "write"}],
        "closed_homophone_equivalences_used": allowed,
        "spoken_copy_acoustic_sequence_match": acoustic_match,
        "first_mismatch_index": first_mismatch,
        "first_mismatch_expected_context": expected[max(0, (first_mismatch or 0) - 4):(first_mismatch or 0) + 5] if first_mismatch is not None else None,
        "first_mismatch_asr_context": actual[max(0, (first_mismatch or 0) - 4):(first_mismatch or 0) + 5] if first_mismatch is not None else None,
        "spoken_copy_verdict": "strict_exact_pass" if strict_match else "pass_with_closed_homophone_equivalence" if acoustic_match else "fail",
        "accepted": acoustic_match and timing_pass,
        "limitation": "Local ASR is an acoustic verification aid and cannot establish orthographic identity or replace owner listening.",
    })


def governed_save_json_x(path: Path, value: Any) -> None:
    if isinstance(value, dict) and path == BASE / "RUN-INPUT.json":
        forecast = PRIOR_GOOGLE_ESTIMATED_USD
        for row in engine.scripts():
            request = json.loads((BASE / row["id"] / "GOOGLE-REQUEST.json").read_text(encoding="utf-8"))
            seconds = len(request["input"]["text"]) / engine.cal.CHARS_PER_SECOND
            forecast += engine.google_cost(request, seconds)
        if forecast > AGGREGATE_GOOGLE_ESTIMATED_USD_CAP:
            raise SystemExit("Full continuation forecast exceeds the cumulative Google cap")
        value.update({
            "record_type": "ep007_shorts_narration_continuation_run_input",
            "status": "prepared_replacement_not_submitted",
            "continuation_runner": {"path": engine.rel(WRAPPER), "sha256": engine.sha_file(WRAPPER)},
            "fresh_authorization": {"path": engine.rel(FRESH_AUTH), "sha256": PIN_MAP[FRESH_AUTH], "event_id": "ep007-short01-guide-replacement-authorized-v11"},
            "prior_consumed": {
                "google_guide_calls": PRIOR_GOOGLE_CALLS,
                "elevenlabs_transfer_calls": PRIOR_ELEVEN_CALLS,
                "provider_generation_calls": PRIOR_PROVIDER_CALLS,
                "estimated_google_usd": PRIOR_GOOGLE_ESTIMATED_USD,
            },
            "approved_caps": {
                "continuation_google_guide_calls": 4,
                "continuation_elevenlabs_transfer_calls": 4,
                "continuation_provider_generation_calls": 8,
                "aggregate_google_guide_calls": AGGREGATE_GOOGLE_CALL_CAP,
                "aggregate_elevenlabs_transfer_calls": AGGREGATE_ELEVEN_CALL_CAP,
                "aggregate_provider_generation_calls": AGGREGATE_PROVIDER_CALL_CAP,
                "automatic_retries": 0,
                "additional_manual_retries": 0,
                "aggregate_google_estimated_spend_usd": AGGREGATE_GOOGLE_ESTIMATED_USD_CAP,
                "aggregate_elevenlabs_credits": AGGREGATE_ELEVEN_CREDIT_CAP,
            },
            "prior_rejected_attempt": {
                "batch_hold_path": engine.rel(V2 / "BATCH-HOLD.json"),
                "batch_hold_sha256": PIN_MAP[V2 / "BATCH-HOLD.json"],
                "guide_path": engine.rel(V2 / "short-01-thirty-day-map/media/guide.wav"),
                "guide_sha256": PIN_MAP[V2 / "short-01-thirty-day-map/media/guide.wav"],
                "disposition": "immutable rejected evidence; excluded from ElevenLabs transfer",
            },
            "v2_prepared_input_bindings": input_bindings(),
            "full_continuation_google_forecast_usd_including_rejected_call": forecast,
            "replacement_failure_policy": "Any failed or uncertain replacement outcome stops the batch; no second replacement or other retry is authorized.",
        })
        value["google_cost_control"] = {
            "type": "forecast_before_each call and measured estimate after each call, cumulative across v2 and v3",
            "caveat": "Google exposes no request-side monetary hard stop; the 0.15 USD limit is a conservative forecast and post-response estimate, not an invoice or provider-side hard limiter.",
            "prior_rejected_estimated_usd": PRIOR_GOOGLE_ESTIMATED_USD,
            "full_continuation_forecast_usd": forecast,
            "authorized_cumulative_estimated_cap_usd": AGGREGATE_GOOGLE_ESTIMATED_USD_CAP,
        }
    elif isinstance(value, dict) and path.name == "PROVIDER-PREFLIGHT.json":
        value["continuation_generation_calls_made"] = 0
        value["cumulative_generation_calls_made"] = PRIOR_PROVIDER_CALLS
        value["fresh_authorization_sha256"] = PIN_MAP[FRESH_AUTH]
    elif isinstance(value, dict) and path.name == "GOOGLE-SUBMISSION-INTENT.json":
        local_after = int(value.get("aggregate_google_calls_after_submission", 0))
        value["continuation_google_calls_after_submission"] = local_after
        value["aggregate_google_calls_after_submission"] = PRIOR_GOOGLE_CALLS + local_after
        value["aggregate_provider_generation_calls_after_submission"] = PRIOR_PROVIDER_CALLS + local_after
        value["provider_generation_attempt"] = 2 if value.get("short_id") == "short-01-thirty-day-map" else 1
        value["replacement_attempt"] = value.get("short_id") == "short-01-thirty-day-map"
        value["prior_rejected_guide_sha256"] = PIN_MAP[V2 / "short-01-thirty-day-map/media/guide.wav"]
        value["fresh_authorization_sha256"] = PIN_MAP[FRESH_AUTH]
    elif isinstance(value, dict) and path.name == "GOOGLE-RECEIPT.json":
        guide = value.get("guide") or {}
        if guide:
            format_pass = (
                guide.get("sample_rate_hz") == 24000
                and guide.get("channels") == 1
                and guide.get("sample_width_bits") == 16
            )
            value["guide_format_pass"] = format_pass
            value["accepted"] = bool(value.get("accepted") and format_pass)
        value["cumulative_google_estimated_cost_usd_after_receipt"] = (
            PRIOR_GOOGLE_ESTIMATED_USD
            + sum(
                float(json.loads(receipt.read_text(encoding="utf-8")).get("estimated_cost_usd_conservative_input_tokens", 0))
                for receipt in BASE.glob("short-*/GOOGLE-RECEIPT.json")
                if receipt != path
            )
            + float(value.get("estimated_cost_usd_conservative_input_tokens", 0))
        )
        value["fresh_authorization_sha256"] = PIN_MAP[FRESH_AUTH]
    elif isinstance(value, dict) and path.name in {"GUIDE-ASR.json", "FINAL-ASR.json"}:
        strict_asr_fields(value)
    elif isinstance(value, dict) and path.name == "GUIDE-BATCH-SUMMARY.json":
        accepted_cost = float(value.get("google_estimated_cost_usd", 0))
        value["google_accepted_guides_estimated_cost_usd"] = accepted_cost
        value["google_rejected_attempt_estimated_cost_usd"] = PRIOR_GOOGLE_ESTIMATED_USD
        value["google_cumulative_estimated_cost_usd"] = accepted_cost + PRIOR_GOOGLE_ESTIMATED_USD
        value["google_cumulative_estimated_cost_cap_usd"] = AGGREGATE_GOOGLE_ESTIMATED_USD_CAP
        value["continuation_google_calls_made"] = 4
        value["cumulative_google_calls_made"] = 5
    elif isinstance(value, dict) and path.name == "TRANSFER-BATCH-PREFLIGHT.json":
        value["generation_calls_before_transfer"] = 5
        value["continuation_generation_calls_before_transfer"] = 4
        value["prior_rejected_google_call_count"] = 1
        value["google_cumulative_estimated_cost_usd"] = current_google_cost_v3()
    elif isinstance(value, dict) and path.name == "ELEVEN-SUBMISSION-INTENT.json":
        local_provider_after = int(value.get("aggregate_provider_generation_calls_after_submission", 0))
        value["continuation_provider_generation_calls_after_submission"] = local_provider_after
        value["aggregate_provider_generation_calls_after_submission"] = PRIOR_PROVIDER_CALLS + local_provider_after
        value["aggregate_google_calls"] = AGGREGATE_GOOGLE_CALL_CAP
        value["aggregate_elevenlabs_calls_after_submission"] = local_provider_after - 4
        value["fresh_authorization_sha256"] = PIN_MAP[FRESH_AUTH]
    elif isinstance(value, dict) and path.name == "ELEVEN-RECEIPT.json":
        voice = value.get("voice") or {}
        if voice:
            format_pass = (
                voice.get("sample_rate_hz") == 48000
                and voice.get("channels") == 1
                and voice.get("sample_width_bits") == 16
            )
            value["voice_format_pass"] = format_pass
            value["accepted_pending_exact_final_asr_and_owner_listen"] = bool(
                value.get("accepted_pending_exact_final_asr_and_owner_listen") and format_pass
            )
        value["fresh_authorization_sha256"] = PIN_MAP[FRESH_AUTH]
    elif isinstance(value, dict) and path.name == "BATCH-STATUS.json":
        accepted_cost = float(value.get("google_estimated_cost_usd", 0))
        value["generation_calls"] = {
            "google": 5,
            "elevenlabs": 4,
            "total": 9,
            "retries": 0,
            "prior_rejected_google_calls": 1,
            "continuation_google_calls": 4,
            "continuation_elevenlabs_calls": 4,
        }
        value["google_accepted_guides_estimated_cost_usd"] = accepted_cost
        value["google_rejected_attempt_estimated_cost_usd"] = PRIOR_GOOGLE_ESTIMATED_USD
        value["google_estimated_cost_usd"] = accepted_cost + PRIOR_GOOGLE_ESTIMATED_USD
        value["rejected_v2_guide_preserved"] = {
            "path": engine.rel(V2 / "short-01-thirty-day-map/media/guide.wav"),
            "sha256": PIN_MAP[V2 / "short-01-thirty-day-map/media/guide.wav"],
        }
    original_save_json_x(path, value)


def require_prepared_v3() -> dict[str, Any]:
    record = original_require_prepared()
    continuation = record.get("continuation_runner", {})
    if continuation.get("path") != engine.rel(WRAPPER) or continuation.get("sha256") != engine.sha_file(WRAPPER):
        raise SystemExit("Continuation runner changed after immutable preparation")
    if record.get("fresh_authorization", {}).get("sha256") != PIN_MAP[FRESH_AUTH]:
        raise SystemExit("Fresh authorization binding changed after preparation")
    if record.get("prior_consumed", {}).get("provider_generation_calls") != PRIOR_PROVIDER_CALLS:
        raise SystemExit("Prior failed provider call is not counted")
    input_bindings()
    return record


def assert_batch_clear_v3() -> None:
    if (BASE / "BATCH-HOLD.json").exists():
        raise SystemExit("Continuation batch is on immutable hold")
    original_assert_batch_clear()


def transfer_preflight_v3() -> None:
    if current_google_cost_v3() > AGGREGATE_GOOGLE_ESTIMATED_USD_CAP:
        raise SystemExit("Cumulative Google estimate exceeds the fresh authorization cap")
    original_transfer_preflight()


def write_hold(command: str, message: str) -> None:
    path = BASE / "BATCH-HOLD.json"
    if path.exists() or not (BASE / "RUN-INPUT.json").exists():
        return
    google_local = len(list(BASE.glob("short-*/GOOGLE-SUBMISSION-INTENT.json")))
    eleven_local = len(list(BASE.glob("short-*/ELEVEN-SUBMISSION-INTENT.json")))
    evidence = []
    for candidate in sorted(BASE.glob("short-*/*.json")):
        if candidate.name.endswith(("INTENT.json", "RECEIPT.json", "ERROR.json", "ASR.json")):
            evidence.append({"path": engine.rel(candidate), "sha256": engine.sha_file(candidate)})
    original_save_json_x(path, {
        "record_type": "ep007_shorts_narration_continuation_hold",
        "at_utc": engine.now(),
        "status": "stopped_no_retry",
        "failed_command": command,
        "message": message[:1000],
        "authorization_event_id": "ep007-short01-guide-replacement-authorized-v11",
        "provider_calls": {
            "google_guide_calls_cumulative": PRIOR_GOOGLE_CALLS + google_local,
            "elevenlabs_transfer_calls_cumulative": PRIOR_ELEVEN_CALLS + eleven_local,
            "provider_generation_calls_cumulative": PRIOR_PROVIDER_CALLS + google_local + eleven_local,
            "retries": 0,
        },
        "google_cumulative_estimated_cost_usd": current_google_cost_v3(),
        "policy_result": "Stop the batch. No additional retry is authorized.",
        "rejected_v2_guide_preserved": {
            "path": engine.rel(V2 / "short-01-thirty-day-map/media/guide.wav"),
            "sha256": PIN_MAP[V2 / "short-01-thirty-day-map/media/guide.wav"],
        },
        "evidence": evidence,
    })


# Configure the pinned engine for this isolated continuation.
engine.BASE = BASE
engine.AUTHORIZATION = FRESH_AUTH
engine.PINS = PIN_MAP
engine.GUIDE_CALL_CAP = 4
engine.TRANSFER_CALL_CAP = 4
engine.TOTAL_CALL_CAP = 8
engine.GOOGLE_SPEND_CAP_USD = AGGREGATE_GOOGLE_ESTIMATED_USD_CAP
engine.ELEVEN_CREDIT_CAP = AGGREGATE_ELEVEN_CREDIT_CAP
engine.assert_pins = assert_pins_v3
engine.save_json_x = governed_save_json_x
engine.require_prepared = require_prepared_v3
engine.assert_batch_clear = assert_batch_clear_v3
engine.current_google_cost = current_google_cost_v3
engine.transfer_preflight = transfer_preflight_v3


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("prepare")
    sub.add_parser("preflight")
    guide_parser = sub.add_parser("guide")
    guide_parser.add_argument("short_id")
    sub.add_parser("guide-summary")
    asr_parser = sub.add_parser("asr")
    asr_parser.add_argument("short_id")
    asr_parser.add_argument("stage", choices=("guide", "final"))
    sub.add_parser("transfer-preflight")
    transfer_parser = sub.add_parser("transfer")
    transfer_parser.add_argument("short_id")
    sub.add_parser("account-after")
    sub.add_parser("finalize")
    args = parser.parse_args()
    routes = {
        "prepare": lambda: engine.prepare(),
        "preflight": lambda: engine.preflight(),
        "guide": lambda: engine.generate_guide(args.short_id),
        "guide-summary": lambda: engine.guide_summary(),
        "asr": lambda: engine.run_asr(args.short_id, args.stage),
        "transfer-preflight": lambda: engine.transfer_preflight(),
        "transfer": lambda: engine.transfer(args.short_id),
        "account-after": lambda: engine.account_after(),
        "finalize": lambda: engine.finalize(),
    }
    try:
        routes[args.command]()
    except SystemExit as exc:
        if args.command not in {"prepare", "preflight"}:
            write_hold(args.command, str(exc))
        raise
    except Exception as exc:
        if args.command not in {"prepare", "preflight"}:
            write_hold(args.command, f"{type(exc).__name__}: {exc}")
        raise


if __name__ == "__main__":
    main()
