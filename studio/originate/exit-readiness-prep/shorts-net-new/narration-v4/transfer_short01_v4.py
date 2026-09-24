#!/usr/bin/env python3
"""One-shot, no-retry Short 1 transfer to the approved Original C voice.

This runner is intentionally scoped to EP007 Short 1. It binds the owner's
through-render authority, the selected/repaired guide, the exact locked copy,
and the inherited provider caps before making one ElevenLabs Voice Changer
request. A submission intent is written before the request; an existing intent
always stops execution so an uncertain response can never be retried blindly.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import math
import os
import re
import subprocess
import sys
import unicodedata
from pathlib import Path
from typing import Any


sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
REPO = next(path for path in (HERE, *HERE.parents) if path.name == "operator-economy")
HELPER_DIR = REPO / "studio/originate/exit-readiness-prep/shorts-net-new/narration-v1"
sys.path.insert(0, str(HELPER_DIR))
import capture_shorts as cap  # noqa: E402


SHORT_ID = "short-01-thirty-day-map"
WORK = HERE / SHORT_ID
GUIDE = WORK / "media/guide-derived-pad500ms.wav"
SCRIPT = REPO / "studio/originate/exit-readiness-prep/shorts-net-new/narration-v3/short-01-thirty-day-map/SCRIPT.txt"
TRANSFER_INPUT = REPO / "studio/originate/exit-readiness-prep/shorts-net-new/narration-v3/short-01-thirty-day-map/TRANSFER-INPUT.json"
REPAIR = WORK / "DERIVED-GUIDE-REPAIR.json"
GUIDE_ASR = WORK / "GUIDE-ASR.json"
GUIDE_TRANSCRIPT = WORK / "diagnostic-asr-derived/transcript.json"
AUTHORITY = REPO / "blueprint-cinema/episodes/EP007-exit-readiness-prep/review/decisions/ep007-short01-through-video-generation-authorized-v15.json"
BATCH_HOLD = REPO / "studio/originate/exit-readiness-prep/shorts-net-new/narration-v3/BATCH-HOLD.json"
CAPTURE_HELPER = HELPER_DIR / "capture_shorts.py"
CALIBRATE_HELPER = REPO / "operator-blueprint-v2/02-narration-production/tools/calibrate.py"
RUNNER = Path(__file__).resolve()

PINS = {
    AUTHORITY: "7dbe6c3726017c4b2722f8678d5a6a8c96b97026e83b0e84f293ea3f667253b4",
    SCRIPT: "9b27c85c9e532c414f4d888045531e082b32b0bbf54b9141d129f9cc5a2aebc0",
    TRANSFER_INPUT: "ea0f4c94ad7dd92acddf053fb581fe46f00bd936039d9f96e766e6d159c3f34b",
    GUIDE: "e1a43df65bc685e479c778adf80d18d5319008d28490f47ece50d9bac0277278",
    REPAIR: "fdb5a0337e5372c0c34a103cebdafd61c265c490869292afacefd15f1e1e27d2",
    GUIDE_ASR: "ca489283f72e7c8dd734815847a61253e3c1c3aabfd4b2f7b0290e4e2ed0c32f",
    GUIDE_TRANSCRIPT: "8a2f17dcfff3e5b7bb625618d4b227fe3af30099c4fcaf54730d8d47f4032338",
    BATCH_HOLD: "fb4cee5de2b86d7b9cd9044feee32a558b5a6785d13e82b7752cb8e46a532355",
    CAPTURE_HELPER: "96395c162129d971ebf9bd7f798e65422392f0cc5891d0800b4c856835bd579b",
    CALIBRATE_HELPER: "d59303278dbb79bef6fe0080f1d2b6c1e701e9228e95c7b3cdea4f3eec78cc00",
}

GOOGLE_CALL_CAP = 5
ELEVEN_CALL_CAP = 4
TOTAL_CALL_CAP = 9
ELEVEN_CREDIT_CAP = 3200
ELEVEN_CREDITS_PER_MINUTE = 1000
NUMBER_WORDS = {"30": "thirty"}


def now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha_file(path: Path) -> str:
    return sha_bytes(path.read_bytes())


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(REPO))


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def assert_pins() -> None:
    for path, expected in PINS.items():
        if not path.is_file():
            raise SystemExit(f"Missing pinned input: {rel(path)}")
        actual = sha_file(path)
        if actual != expected:
            raise SystemExit(f"Pinned input changed: {rel(path)} expected {expected}, got {actual}")

    authority = read_json(AUTHORITY)
    data = authority.get("data") or {}
    if authority.get("event_id") != "ep007-short01-through-video-generation-authorized-v15":
        raise SystemExit("Short 1 authority event ID changed")
    if data.get("verdict") != "accept" or data.get("verbatim") != "approved. you're approved through the video generation for short 1 just keep going":
        raise SystemExit("Short 1 authority does not contain the owner's exact approval")
    if "Short 1 production through a verified video render only" not in str(data.get("scope", "")):
        raise SystemExit("Short 1 through-render scope is missing")

    hold = read_json(BATCH_HOLD)
    counts = hold.get("provider_calls") or {}
    if counts != {
        "google_guide_calls_cumulative": 2,
        "elevenlabs_transfer_calls_cumulative": 0,
        "provider_generation_calls_cumulative": 2,
        "retries": 0,
    }:
        raise SystemExit("Inherited provider-call baseline changed")

    transfer_input = read_json(TRANSFER_INPUT)
    expected_input = {
        "endpoint": cap.cal.TRANSFER_ENDPOINT,
        "target_voice_id": cap.cal.TRANSFER_VOICE_ID,
        "output_format": cap.cal.TRANSFER_OUTPUT_FORMAT,
        "fields": {
            "model_id": cap.cal.TRANSFER_MODEL,
            "remove_background_noise": "false",
            "seed": str(cap.cal.TRANSFER_SEED),
            "voice_settings": json.dumps(cap.cal.TRANSFER_VOICE_SETTINGS, sort_keys=True),
            "file_format": "other",
        },
    }
    if transfer_input != expected_input:
        raise SystemExit("Pinned Voice Changer request configuration changed")

    guide_probe = cap.cal.probe(GUIDE)
    if (
        guide_probe.get("sample_rate_hz") != 24000
        or guide_probe.get("channels") != 1
        or guide_probe.get("sample_width_bits") != 16
        or abs(float(guide_probe.get("duration_seconds", 0)) - 41.471) > 0.002
        or not guide_probe.get("ends_in_silence")
    ):
        raise SystemExit(f"Repaired guide technical gate failed: {guide_probe}")

    asr = read_json(GUIDE_ASR)
    transcript = read_json(GUIDE_TRANSCRIPT)
    if (
        asr.get("status") != "pass_exact_normalized_locked_words_and_timing_within_derived_media"
        or asr.get("accepted_for_transfer_preflight") is not True
        or len(transcript) != 97
    ):
        raise SystemExit("Repaired guide exact-copy ASR gate failed")


def global_intent_counts() -> dict[str, int]:
    root = REPO / "studio/originate/exit-readiness-prep/shorts-net-new"
    google = len(list(root.glob("narration-v*/**/GOOGLE-SUBMISSION-INTENT.json")))
    eleven = len(list(root.glob("narration-v*/**/ELEVEN-SUBMISSION-INTENT.json")))
    return {"google": google, "elevenlabs": eleven, "total": google + eleven}


def estimated_credits() -> int:
    seconds = float(cap.cal.probe(GUIDE)["duration_seconds"])
    return math.ceil(seconds * ELEVEN_CREDITS_PER_MINUTE / 60)


def preflight() -> None:
    assert_pins()
    output = WORK / "TRANSFER-PREFLIGHT.json"
    if output.exists():
        raise SystemExit(f"Preflight already exists: {rel(output)}")
    for path in (
        WORK / "ELEVEN-SUBMISSION-INTENT.json",
        WORK / "ELEVEN-RECEIPT.json",
        WORK / "ELEVEN-ERROR.json",
        WORK / "media/original-c.wav",
        WORK / "media/elevenlabs-response.pcm",
    ):
        if path.exists():
            raise SystemExit(f"Transfer output already exists: {rel(path)}")

    counts = global_intent_counts()
    if counts != {"google": 2, "elevenlabs": 0, "total": 2}:
        raise SystemExit(f"Unexpected cumulative provider intent state: {counts}")
    forecast = estimated_credits()
    if counts["google"] > GOOGLE_CALL_CAP or counts["elevenlabs"] + 1 > ELEVEN_CALL_CAP or counts["total"] + 1 > TOTAL_CALL_CAP:
        raise SystemExit("Inherited provider call cap would be exceeded")
    if forecast > ELEVEN_CREDIT_CAP:
        raise SystemExit("Short 1 transfer forecast exceeds the inherited ElevenLabs cap")

    account, voice, headers = cap.read_account_and_voice()
    if int(account["remaining_included_credits"]) < forecast:
        raise SystemExit("Live ElevenLabs balance does not cover the one authorized transfer")
    cap.save_json_x(output, {
        "record_type": "ep007_short01_original_c_transfer_preflight_v4",
        "at_utc": now(),
        "status": "pass_one_short01_transfer_allowed",
        "authority_path": rel(AUTHORITY),
        "authority_sha256": sha_file(AUTHORITY),
        "pinned_inputs": [{"path": rel(path), "sha256": expected} for path, expected in PINS.items()],
        "runner_path": rel(RUNNER),
        "runner_sha256": sha_file(RUNNER),
        "call_counts_before": counts,
        "call_counts_after_if_submitted": {"google": counts["google"], "elevenlabs": counts["elevenlabs"] + 1, "total": counts["total"] + 1},
        "caps": {"google": GOOGLE_CALL_CAP, "elevenlabs": ELEVEN_CALL_CAP, "total": TOTAL_CALL_CAP, "automatic_retries": 0},
        "estimated_credits_ceiling": forecast,
        "elevenlabs_credit_cap": ELEVEN_CREDIT_CAP,
        "account": account,
        "voice": voice,
        "response_headers": headers,
        "generation_calls_made": 0,
    })
    print(json.dumps({"status": "pass", "estimated_credits": forecast, "remaining_credits": account["remaining_included_credits"], "voice": voice.get("name")}))


def transfer() -> None:
    assert_pins()
    preflight_path = WORK / "TRANSFER-PREFLIGHT.json"
    if not preflight_path.is_file():
        raise SystemExit("Run preflight first")
    preflight_record = read_json(preflight_path)
    if (
        preflight_record.get("status") != "pass_one_short01_transfer_allowed"
        or preflight_record.get("runner_sha256") != sha_file(RUNNER)
        or preflight_record.get("authority_sha256") != sha_file(AUTHORITY)
    ):
        raise SystemExit("Transfer preflight no longer binds the current runner or authority")

    intent = WORK / "ELEVEN-SUBMISSION-INTENT.json"
    receipt_path = WORK / "ELEVEN-RECEIPT.json"
    error_path = WORK / "ELEVEN-ERROR.json"
    raw_path = WORK / "media/elevenlabs-response.pcm"
    final_path = WORK / "media/original-c.wav"
    for path in (intent, receipt_path, error_path, raw_path, final_path):
        if path.exists():
            raise SystemExit(f"Transfer evidence already exists; no retry authorized: {rel(path)}")

    counts = global_intent_counts()
    if counts != preflight_record.get("call_counts_before"):
        raise SystemExit(f"Provider intent state changed after preflight: {counts}")
    forecast = estimated_credits()
    if forecast != preflight_record.get("estimated_credits_ceiling") or forecast > ELEVEN_CREDIT_CAP:
        raise SystemExit("Credit forecast changed or exceeds cap")

    account, voice, account_headers = cap.read_account_and_voice()
    if int(account["remaining_included_credits"]) < forecast:
        raise SystemExit("Live ElevenLabs balance no longer covers the authorized transfer")
    account_before = WORK / "ELEVEN-ACCOUNT-BEFORE.json"
    cap.save_json_x(account_before, {
        "at_utc": now(),
        "account": account,
        "voice": voice,
        "response_headers": account_headers,
        "estimated_credits_ceiling": forecast,
        "credit_cap": ELEVEN_CREDIT_CAP,
    })

    transfer_input = read_json(TRANSFER_INPUT)
    body, content_type = cap.cal.multipart(transfer_input["fields"], GUIDE.name, GUIDE.read_bytes())
    url = f"{transfer_input['endpoint']}?output_format={transfer_input['output_format']}&enable_logging=true"
    cap.save_json_x(intent, {
        "record_type": "ep007_short01_original_c_submission_intent_v4",
        "at_utc": now(),
        "stage": "elevenlabs_voice_transfer",
        "short_id": SHORT_ID,
        "authority_sha256": sha_file(AUTHORITY),
        "runner_sha256": sha_file(RUNNER),
        "preflight_sha256": sha_file(preflight_path),
        "account_before_sha256": sha_file(account_before),
        "url": url,
        "fields": transfer_input["fields"],
        "request_body_sha256": sha_bytes(body),
        "guide_path": rel(GUIDE),
        "guide_sha256": sha_file(GUIDE),
        "guide_asr_sha256": sha_file(GUIDE_ASR),
        "script_sha256": sha_file(SCRIPT),
        "transfer_input_sha256": sha_file(TRANSFER_INPUT),
        "provider_generation_attempt": 1,
        "automatic_retries": 0,
        "estimated_credits_ceiling": forecast,
        "credit_cap": ELEVEN_CREDIT_CAP,
        "cumulative_call_counts_after_submission": {"google": counts["google"], "elevenlabs": counts["elevenlabs"] + 1, "total": counts["total"] + 1},
        "submission_outcome_policy": "uncertain or failed outcome stops Short 1 production and cannot be retried without new authority",
    })

    key = cap.cal.read_dotenv_key("ELEVENLABS_API_KEY")
    try:
        status, raw, response_headers = cap.safe_request(
            url,
            method="POST",
            headers={"xi-api-key": key, "Content-Type": content_type, "Accept": "*/*"},
            body=body,
        )
    except Exception as exc:
        cap.save_json_x(error_path, {
            "at_utc": now(),
            "error_class": type(exc).__name__,
            "submission_outcome": "uncertain_no_retry",
        })
        raise SystemExit("ElevenLabs transport outcome uncertain; no retry authorized") from exc

    cap.save_bytes_x(raw_path, raw)
    receipt: dict[str, Any] = {
        "record_type": "ep007_short01_original_c_transfer_receipt_v4",
        "at_utc": now(),
        "http_status": status,
        "response_headers": response_headers,
        "raw_response_path": rel(raw_path),
        "raw_response_sha256": sha_bytes(raw),
        "guide_sha256": sha_file(GUIDE),
        "estimated_credits_ceiling": forecast,
        "calls": 1,
        "retries": 0,
    }
    if status != 200:
        receipt["error"] = cap.redact_error(raw, [key])
        receipt["accepted"] = False
        cap.save_json_x(receipt_path, receipt)
        raise SystemExit(f"ElevenLabs HTTP {status}; no retry authorized")

    try:
        actual_credits = cap.parse_actual_eleven_cost(receipt)
    except ValueError as exc:
        receipt["actual_credit_cost_verified"] = False
        receipt["accepted_pending_exact_final_asr_and_owner_listen"] = False
        receipt["error"] = str(exc)
        cap.save_json_x(receipt_path, receipt)
        raise SystemExit(f"{exc}; no retry authorized") from exc
    if actual_credits > ELEVEN_CREDIT_CAP:
        receipt["actual_credit_cost_verified"] = True
        receipt["actual_credit_cost"] = actual_credits
        receipt["accepted_pending_exact_final_asr_and_owner_listen"] = False
        cap.save_json_x(receipt_path, receipt)
        raise SystemExit("Actual ElevenLabs cost exceeded the inherited cap; stopped")

    cap.cal.wav_from_pcm(raw, cap.cal.TRANSFER_OUTPUT_RATE_HZ, final_path)
    final_path.chmod(0o600)
    probe = cap.cal.probe(final_path)
    guide_probe = cap.cal.probe(GUIDE)
    delta = float(probe["duration_seconds"]) - float(guide_probe["duration_seconds"])
    tail = float(probe.get("tail_energy", 1))
    tail_class = "silent" if tail < cap.cal.TAIL_ENERGY_THRESHOLD else "marginal" if tail < 0.06 else "still_sounding"
    technical_pass = abs(delta) <= 0.5 and tail_class in ("silent", "marginal")
    receipt |= {
        "voice": probe | {"path": rel(final_path)},
        "duration_delta_seconds": delta,
        "transfer_tail_class": tail_class,
        "transfer_marginal_ceiling": 0.06,
        "technical_duration_and_tail_pass": technical_pass,
        "actual_credit_cost_verified": True,
        "actual_credit_cost": actual_credits,
        "cumulative_actual_credit_cost": actual_credits,
        "credit_cap": ELEVEN_CREDIT_CAP,
        "accepted_pending_exact_final_asr_and_owner_listen": technical_pass,
    }
    cap.save_json_x(receipt_path, receipt)
    if not technical_pass:
        raise SystemExit("Transferred audio failed the duration/tail gate; no retry authorized")

    account_after_path = WORK / "ELEVEN-ACCOUNT-AFTER.json"
    try:
        after, after_voice, after_headers = cap.read_account_and_voice()
        cap.save_json_x(account_after_path, {
            "at_utc": now(),
            "account": after,
            "voice": after_voice,
            "response_headers": after_headers,
            "remaining_credit_delta": int(account["remaining_included_credits"]) - int(after["remaining_included_credits"]),
            "receipt_actual_credit_cost": actual_credits,
        })
    except Exception as exc:
        cap.save_json_x(account_after_path, {
            "at_utc": now(),
            "status": "readback_failed_non_destructive",
            "error_class": type(exc).__name__,
            "receipt_actual_credit_cost": actual_credits,
        })

    print(json.dumps({
        "short_id": SHORT_ID,
        "duration_seconds": probe["duration_seconds"],
        "tail_energy": probe.get("tail_energy"),
        "tail_class": tail_class,
        "duration_delta_seconds": delta,
        "estimated_credits": forecast,
        "actual_credits": actual_credits,
    }))


def normalize_tokens(text: str) -> list[str]:
    text = unicodedata.normalize("NFKC", text).lower().replace("&", " and ")
    tokens = re.findall(r"[a-z0-9]+(?:['’][a-z0-9]+)?", text)
    return [NUMBER_WORDS.get(token, token).replace("'", "").replace("’", "") for token in tokens]


def asr() -> None:
    assert_pins()
    final_path = WORK / "media/original-c.wav"
    receipt_path = WORK / "ELEVEN-RECEIPT.json"
    if not final_path.is_file() or not receipt_path.is_file():
        raise SystemExit("Missing transferred Original C media or receipt")
    receipt = read_json(receipt_path)
    if (
        receipt.get("http_status") != 200
        or receipt.get("accepted_pending_exact_final_asr_and_owner_listen") is not True
        or receipt.get("voice", {}).get("sha256") != sha_file(final_path)
    ):
        raise SystemExit("Transferred media is not technically accepted and receipt-bound")

    intent = WORK / "FINAL-ASR-INTENT.json"
    canonical = WORK / "FINAL-ASR.json"
    run_path = WORK / "FINAL-ASR-RUN.json"
    asr_dir = WORK / "asr-final"
    for path in (intent, canonical, run_path, asr_dir):
        if path.exists():
            raise SystemExit(f"Final ASR evidence already exists: {rel(path)}")
    command = [
        "npx", "--yes", "hyperframes@0.8.59", "transcribe", str(final_path),
        "--engine", "whisper", "--model", "small.en", "--language", "en",
        "--dir", str(asr_dir), "--json",
    ]
    cap.save_json_x(intent, {
        "at_utc": now(),
        "stage": "final",
        "short_id": SHORT_ID,
        "source_media_path": rel(final_path),
        "source_media_sha256": sha_file(final_path),
        "provider_receipt_path": rel(receipt_path),
        "provider_receipt_sha256": sha_file(receipt_path),
        "script_path": rel(SCRIPT),
        "script_sha256": sha_file(SCRIPT),
        "tool": "hyperframes@0.8.59",
        "engine": "whisper",
        "model": "small.en",
        "language": "en",
        "command": command,
        "network_transcription_provider": False,
    })
    asr_dir.mkdir()
    env = dict(os.environ)
    env["HYPERFRAMES_NO_TELEMETRY"] = "1"
    try:
        completed = subprocess.run(command, cwd=REPO, env=env, capture_output=True, text=True, timeout=900, check=False)
    except Exception as exc:
        cap.save_json_x(WORK / "FINAL-ASR-ERROR.json", {"at_utc": now(), "error_class": type(exc).__name__, "status": "local_asr_failed"})
        raise SystemExit("Local final ASR failed") from exc

    envelope = None
    for line in reversed([line for line in completed.stdout.splitlines() if line.strip()]):
        try:
            candidate = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(candidate, dict):
            envelope = candidate
            break
    transcript_path = asr_dir / "transcript.json"
    if completed.returncode != 0 or envelope is None or not transcript_path.is_file():
        cap.save_json_x(WORK / "FINAL-ASR-ERROR.json", {
            "at_utc": now(),
            "returncode": completed.returncode,
            "stdout_tail": completed.stdout[-4000:],
            "stderr_tail": completed.stderr[-4000:],
            "status": "local_asr_command_failed",
        })
        raise SystemExit("Local final ASR command failed")

    words = read_json(transcript_path)
    if not isinstance(words, list) or not words:
        raise SystemExit("Final ASR transcript is not a non-empty word array")
    expected_tokens = normalize_tokens(SCRIPT.read_text(encoding="utf-8"))
    actual_tokens = normalize_tokens(" ".join(str(word.get("text", "")) for word in words))
    exact = expected_tokens == actual_tokens
    values_valid = all(
        isinstance(word.get("start"), (int, float))
        and isinstance(word.get("end"), (int, float))
        and float(word["start"]) >= 0
        and float(word["end"]) >= float(word["start"])
        for word in words
    )
    order_valid = values_valid and all(float(words[i]["start"]) >= float(words[i - 1]["start"]) for i in range(1, len(words)))
    duration = float(receipt["voice"]["duration_seconds"])
    within_duration = values_valid and float(words[-1]["end"]) <= duration + 0.05
    accepted = exact and values_valid and order_valid and within_duration and len(expected_tokens) == 97
    cap.save_json_x(run_path, {
        "at_utc": now(),
        "intent_sha256": sha_file(intent),
        "source_media_sha256": sha_file(final_path),
        "command": command,
        "returncode": completed.returncode,
        "stdout_envelope": envelope,
        "stderr_tail": completed.stderr[-4000:],
        "transcript_path": rel(transcript_path),
        "transcript_sha256": sha_file(transcript_path),
    })
    cap.save_json_x(canonical, {
        "record_type": "ep007_short01_original_c_local_asr_v4",
        "at_utc": now(),
        "status": "pass" if accepted else "fail",
        "stage": "final",
        "tool": "hyperframes@0.8.59",
        "engine": "whisper",
        "model": "small.en",
        "language": "en",
        "asr_run_path": rel(run_path),
        "asr_run_sha256": sha_file(run_path),
        "transcript_path": rel(transcript_path),
        "transcript_sha256": sha_file(transcript_path),
        "media_path": rel(final_path),
        "media_sha256": sha_file(final_path),
        "script_path": rel(SCRIPT),
        "script_sha256": sha_file(SCRIPT),
        "expected_token_count": len(expected_tokens),
        "asr_token_count": len(actual_tokens),
        "exact_normalized_word_match": exact,
        "word_timing_values_valid": values_valid,
        "word_timing_order_valid": order_valid,
        "word_timing_within_media_duration": within_duration,
        "last_word": words[-1].get("text"),
        "last_word_start_seconds": words[-1].get("start"),
        "last_word_end_seconds": words[-1].get("end"),
        "media_duration_seconds": duration,
        "accepted_for_picture_production": accepted,
        "limitation": "Local ASR verifies exact normalized words and timing bounds; it does not replace owner listening acceptance of the finished candidate.",
    })
    print(json.dumps({"short_id": SHORT_ID, "exact_match": exact, "token_count": len(actual_tokens), "timings_valid": values_valid and order_valid and within_duration, "accepted": accepted}))
    if not accepted:
        raise SystemExit("Final Original C ASR did not pass exact-copy/timing gates")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("preflight", "transfer", "asr"))
    args = parser.parse_args()
    {"preflight": preflight, "transfer": transfer, "asr": asr}[args.command]()


if __name__ == "__main__":
    main()
