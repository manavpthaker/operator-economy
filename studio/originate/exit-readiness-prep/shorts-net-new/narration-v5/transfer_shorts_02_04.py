#!/usr/bin/env python3
"""One-shot Original C transfer for EP007 Shorts 02-04; no provider call on check.

This is deliberately separate from the stopped narration-v3 batch. Each short
needs a preserved Google source, exact-copy local ASR, an immutable selected
guide, and explicit resolution of any existing QC hold. The first ElevenLabs
submission intent is terminal for that short even if the outcome is uncertain.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import math
import sys
import unicodedata
import re
import wave
from pathlib import Path
from typing import Any


sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
REPO = next(path for path in (HERE, *HERE.parents) if path.name == "operator-economy")
SHORTS = REPO / "studio/originate/exit-readiness-prep/shorts-net-new"
V3 = SHORTS / "narration-v3"
HELPER = SHORTS / "narration-v1/capture_shorts.py"
CALIBRATE = REPO / "operator-blueprint-v2/02-narration-production/tools/calibrate.py"
SOURCE = REPO / "blueprint-cinema/episodes/EP007-exit-readiness-prep/review/decisions/ep007-owner-authorize-shorts-02-04-full-private-production-20260923.json"
EVENT = REPO / "blueprint-cinema/episodes/EP007-exit-readiness-prep/review/decisions/ep007-shorts-02-04-full-private-production-authorized-v3.json"
SCRIPTS = SHORTS / "STANDALONE-SCRIPTS-V3.json"
BATCH_HOLD = V3 / "BATCH-HOLD.json"
RUNNER = Path(__file__).resolve()

sys.path.insert(0, str(HELPER.parent))
import capture_shorts as cap  # noqa: E402


SHORT_IDS = (
    "short-02-operations-business",
    "short-03-how-you-charge",
    "short-04-test-the-front-door",
)
SCRIPT_HASHES = {
    "short-02-operations-business": "aee361d4542ed450365a50c70577f6b1bddd61c30de0571d770cbd91b0ed5542",
    "short-03-how-you-charge": "2a56beffef964667fbd09c934130d53171da605e23f876e75a4cb715a03efc3b",
    "short-04-test-the-front-door": "fb1021dc78cfb7c717aacdcef665d69a3651b6db8c0b9b129dab3e6c1b6ea60f",
}
PINS = {
    SOURCE: "e6b4bf17f2eec1f258b8dc65ca060ce2262dd4eaba070bdbb59bfdf85bda9f85",
    EVENT: "c1baa48b414d988a570cfc162bcbdc6886e9b21dbc15fe4c22dc4022b414c201",
    SCRIPTS: "6be1ee7c13ba6fc607d215e9a61c74fda31cc3f60026632eff6fc029f903cf6c",
    BATCH_HOLD: "fb4cee5de2b86d7b9cd9044feee32a558b5a6785d13e82b7752cb8e46a532355",
    HELPER: "96395c162129d971ebf9bd7f798e65422392f0cc5891d0800b4c856835bd579b",
    CALIBRATE: "d59303278dbb79bef6fe0080f1d2b6c1e701e9228e95c7b3cdea4f3eec78cc00",
}
TRANSFER_INPUT_HASH = "ea0f4c94ad7dd92acddf053fb581fe46f00bd936039d9f96e766e6d159c3f34b"
TRANSFER_CALL_CAP = 3
AGGREGATE_CREDIT_CEILING = 3200
CREDITS_PER_MINUTE_FORECAST = 1000


def now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def sha_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha_file(path: Path) -> str:
    return sha_bytes(path.read_bytes())


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(REPO))


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def fail(message: str) -> None:
    raise SystemExit(message)


def expect(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def bound_path(value: str, base: Path) -> Path:
    path = (REPO / value).resolve()
    expect(path.is_relative_to(base.resolve()) and path.is_file(), f"Evidence is missing or outside {rel(base)}: {value}")
    return path


def verify_ref(ref: dict[str, Any], base: Path) -> Path:
    expect(isinstance(ref, dict) and isinstance(ref.get("path"), str), "Evidence reference has no path")
    path = bound_path(ref["path"], base)
    expect(ref.get("sha256") == sha_file(path), f"Evidence hash changed: {rel(path)}")
    return path


def normalize_tokens(value: str) -> list[str]:
    value = unicodedata.normalize("NFKC", value).lower().replace("&", " and ")
    return [token.replace("'", "").replace("’", "") for token in re.findall(r"[a-z0-9]+(?:['’][a-z0-9]+)?", value)]


def work(short_id: str) -> Path:
    expect(short_id in SHORT_IDS, f"Unknown Short ID: {short_id}")
    return HERE / short_id


def assert_global_pins() -> None:
    for path, expected_hash in PINS.items():
        expect(path.is_file() and sha_file(path) == expected_hash, f"Pinned input missing or changed: {rel(path)}")
    source, event = read_json(SOURCE), read_json(EVENT)
    expected_verbatim = "Go for all of them the full pipeline. I want to get them done and make edits after if necessary"
    expect(source.get("owner_verbatim") == expected_verbatim, "Owner source no longer contains the exact instruction")
    expect(event.get("event_id") == "ep007-shorts-02-04-full-private-production-authorized-v3", "Wrong owner event")
    data = event.get("data") or {}
    expect(data.get("verbatim") == expected_verbatim and data.get("verdict") == "accept", "Owner event not accepted")
    authorized = data.get("authorized") or {}
    expect(tuple(authorized.get("short_ids") or ()) == SHORT_IDS, "Owner event Short IDs changed")
    expect("ElevenLabs Original C voice transfers" in (authorized.get("stages") or []), "Original C stage not authorized")
    expect(authorized.get("script_package_sha256") == PINS[SCRIPTS], "Owner event script package changed")
    limits = data.get("agent_execution_limits_not_owner_quoted") or {}
    expect(limits.get("elevenlabs_transfer_calls_max") == TRANSFER_CALL_CAP, "Transfer call cap changed")
    expect(limits.get("elevenlabs_credit_forecast_cap") == AGGREGATE_CREDIT_CEILING, "Credit cap changed")
    expect(limits.get("automatic_retries") == 0, "No-retry contract changed")
    expect(read_json(BATCH_HOLD).get("status") == "stopped_no_retry", "Historical narration-v3 batch was reactivated")
    expected_config = {
        "endpoint": cap.cal.TRANSFER_ENDPOINT,
        "target_voice_id": cap.cal.TRANSFER_VOICE_ID,
        "output_format": cap.cal.TRANSFER_OUTPUT_FORMAT,
        "fields": cap.transfer_fields(),
    }
    for short_id in SHORT_IDS:
        script = V3 / short_id / "SCRIPT.txt"
        config = V3 / short_id / "TRANSFER-INPUT.json"
        expect(script.is_file() and sha_file(script) == SCRIPT_HASHES[short_id], f"Locked script changed: {short_id}")
        expect(config.is_file() and sha_file(config) == TRANSFER_INPUT_HASH, f"Transfer config changed: {short_id}")
        expect(read_json(config) == expected_config, f"Original C provider parameters changed: {short_id}")


def verify_pcm_tail_repair(short_id: str, selected: Path, source: Path, repair_path: Path) -> None:
    record = read_json(repair_path)
    expect(record.get("provider_call") is False, "Tail repair record implies a provider call")
    expect(record.get("source", {}).get("path") == rel(source) and record["source"].get("sha256") == sha_file(source), "Tail repair source mismatch")
    expect(record.get("derived", {}).get("path") == rel(selected) and record["derived"].get("sha256") == sha_file(selected), "Tail repair derivative mismatch")
    operation = record.get("operation") or {}
    expect(operation.get("type") == "append_digital_silence_to_derived_copy", "Only digital silence tail repair is allowed")
    expect(operation.get("source_overwritten") is False and operation.get("provider_call") is False, "Tail repair did not preserve source")
    with wave.open(str(source), "rb") as original, wave.open(str(selected), "rb") as derived:
        params_a, params_b = original.getparams(), derived.getparams()
        expect(params_a[:3] == params_b[:3] == (1, 2, 24000), "Source/derived format mismatch")
        a = original.readframes(original.getnframes())
        b = derived.readframes(derived.getnframes())
        appended = derived.getnframes() - original.getnframes()
        expect(0 < appended <= 12000 and len(b) == len(a) + appended * 2, "Silence repair must append at most 500 ms")
        expect(b[:len(a)] == a and b[len(a):] == bytes(appended * 2), "Derived guide altered source PCM or appended nonzero audio")
        expect(operation.get("appended_frames") == appended, "Tail repair frame count mismatch")
    expect(record.get("derived", {}).get("appended_frames_all_zero") is True, "Tail repair record does not attest zero samples")


def verify_guide(short_id: str) -> dict[str, Any]:
    assert_global_pins()
    base = work(short_id)
    source = base / "media/guide.wav"
    receipt_path = base / "GOOGLE-RECEIPT.json"
    intent_path = base / "GOOGLE-SUBMISSION-INTENT.json"
    expect(source.is_file() and receipt_path.is_file() and intent_path.is_file(), "Preserved Google guide/source evidence missing")
    receipt = read_json(receipt_path)
    expect(receipt.get("http_status") == 200 and receipt.get("guide_path") == rel(source) and receipt.get("guide_sha256") == sha_file(source), "Google receipt/source mismatch")
    intent = read_json(intent_path)
    expect(intent.get("short_id") == short_id and intent.get("script_sha256") == SCRIPT_HASHES[short_id], "Google submission intent script mismatch")
    expect(intent.get("automatic_retries") == 0 and intent.get("provider_generation_attempt") == 1, "Guide attempt/retry count changed")
    owner_event = verify_ref({"path": intent.get("owner_event_path"), "sha256": intent.get("owner_event_sha256")}, REPO / "blueprint-cinema/episodes/EP007-exit-readiness-prep/review/decisions")
    verify_ref({"path": intent.get("owner_source_path"), "sha256": intent.get("owner_source_sha256")}, REPO / "blueprint-cinema/episodes/EP007-exit-readiness-prep/review/decisions")
    expect(owner_event == (EVENT if short_id != SHORT_IDS[0] else REPO / "blueprint-cinema/episodes/EP007-exit-readiness-prep/review/decisions/ep007-short02-one-google-guide-authorized-v2.json"), "Google guide owner event mismatch")
    expect(receipt.get("short_id") == short_id and receipt.get("intent_path") == rel(intent_path) and receipt.get("intent_sha256") == sha_file(intent_path), "Google receipt/intent mismatch")
    verify_ref({"path": receipt.get("raw_response_path"), "sha256": receipt.get("raw_response_sha256")}, base)
    request_path = V3 / short_id / "GOOGLE-REQUEST.json"
    expect(request_path.is_file() and intent.get("request_path") == rel(request_path) and intent.get("request_sha256") == sha_file(request_path), "Guide request changed")
    expect(read_json(request_path).get("input", {}).get("text") == (V3 / short_id / "SCRIPT.txt").read_text(encoding="utf-8").strip(), "Guide request differs from locked script")

    selection_path = base / "GUIDE-TRANSFER-SELECTION.json"
    qc_path = base / "GUIDE-ASR.json"
    expect(selection_path.is_file() and qc_path.is_file(), f"{short_id}: no immutable selected-guide and exact-copy QC pass")
    selection, qc = read_json(selection_path), read_json(qc_path)
    expect(selection.get("record_type") == "ep007_guide_transfer_selection_v1", "Wrong guide selection record type")
    expect(selection.get("short_id") == short_id and selection.get("status") == "pass_selected_for_original_c", "Guide selection not accepted")
    selected = verify_ref(selection.get("selected_guide") or {}, base)
    expect(selected.parent == (base / "media").resolve(), "Selected guide is not in this Short's media folder")
    expect(selection.get("source_guide", {}).get("path") == rel(source) and selection["source_guide"].get("sha256") == sha_file(source), "Selection does not bind preserved source")
    expect(selection.get("google_receipt", {}).get("path") == rel(receipt_path) and selection["google_receipt"].get("sha256") == sha_file(receipt_path), "Selection does not bind Google receipt")
    expect(selection.get("guide_asr", {}).get("path") == rel(qc_path) and selection["guide_asr"].get("sha256") == sha_file(qc_path), "Selection does not bind exact-copy QC")

    script = V3 / short_id / "SCRIPT.txt"
    expect(qc.get("accepted_for_transfer_preflight") is True and str(qc.get("status", "")).startswith("pass_exact_normalized_locked_words_and_timing"), "Guide QC did not pass exact copy")
    expect(qc.get("media", {}).get("path") == rel(selected) and qc["media"].get("sha256") == sha_file(selected), "Guide QC media mismatch")
    expect(qc.get("script", {}).get("path") == rel(script) and qc["script"].get("sha256") == sha_file(script), "Guide QC script mismatch")
    transcript = verify_ref(qc.get("transcript") or {}, base)
    words = read_json(transcript)
    expect(isinstance(words, list) and bool(words), "Guide ASR word transcript missing")
    expected = normalize_tokens(script.read_text(encoding="utf-8"))
    actual = normalize_tokens(" ".join(str(row.get("text", "")) for row in words))
    expect(expected == actual, "Guide transcript differs from locked spoken copy")
    expect(qc["transcript"].get("exact_normalized_word_match") is True, "Guide QC exact-copy flag missing")
    valid_times = all(isinstance(row.get("start"), (int, float)) and isinstance(row.get("end"), (int, float)) and 0 <= row["start"] <= row["end"] for row in words)
    expect(valid_times and all(words[i]["start"] >= words[i - 1]["start"] for i in range(1, len(words))), "Guide ASR timings invalid")
    probe = cap.cal.probe(selected)
    expect(probe.get("sample_rate_hz") == 24000 and probe.get("channels") == 1 and probe.get("sample_width_bits") == 16, "Guide PCM format changed")
    expect(bool(probe.get("ends_in_silence")) and float(words[-1]["end"]) <= float(probe["duration_seconds"]) + 0.05, "Guide tail/timing gate failed")
    expect(qc["transcript"].get("word_timings_monotonic") is True and qc["transcript"].get("word_timings_within_media_duration") is True, "Guide QC timing flags missing")

    if selected != source:
        repair_path = base / "DERIVED-GUIDE-REPAIR.json"
        expect(repair_path.is_file(), "Derived guide has no separately evidenced tail repair")
        expect(selection.get("derived_repair", {}).get("path") == rel(repair_path) and selection["derived_repair"].get("sha256") == sha_file(repair_path), "Guide selection does not bind tail repair")
        verify_pcm_tail_repair(short_id, selected, source, repair_path)
    else:
        expect(selection.get("derived_repair") is None, "Direct guide must not claim a derivative")

    holds = [path for path in (base / "HOLD.json", base / "GUIDE-QC-V1.json") if path.is_file() and (path.name == "HOLD.json" or str(read_json(path).get("status", "")).startswith("hold"))]
    if holds:
        resolution_path = base / "GUIDE-HOLD-RESOLUTION.json"
        expect(resolution_path.is_file(), "Earlier guide QC hold has no explicit resolution")
        resolution = read_json(resolution_path)
        expect(resolution.get("record_type") == "ep007_guide_hold_resolution_v1" and resolution.get("status") == "pass_resolved_with_preserved_evidence", "Guide hold resolution not accepted")
        expect(resolution.get("short_id") == short_id, "Guide hold resolution Short ID mismatch")
        expect(resolution.get("guide_asr", {}).get("sha256") == sha_file(qc_path), "Guide hold resolution does not bind passing ASR")
        expect({(x.get("path"), x.get("sha256")) for x in resolution.get("prior_holds", [])} == {(rel(path), sha_file(path)) for path in holds}, "Guide hold resolution does not bind every prior hold")
        expect(selection.get("hold_resolution", {}).get("path") == rel(resolution_path) and selection["hold_resolution"].get("sha256") == sha_file(resolution_path), "Selection does not bind hold resolution")
        if any(read_json(path).get("reason") == "tail" for path in holds):
            expect(selected != source and resolution.get("resolution_kind") == "lossless_silence_tail_repair", "Tail hold requires verified derived repair")
        if any(str(read_json(path).get("status", "")).startswith("hold_exact_copy") for path in holds):
            expect(resolution.get("resolution_kind") == "owner_listened_and_alternate_asr_proved_exact_copy", "Opening exact-copy hold needs owner listening and independent exact ASR")
            owner = resolution.get("owner_listening_source") or {}
            expect(bool(owner.get("verbatim")) and bool(owner.get("path")) and bool(owner.get("sha256")), "Owner listening evidence missing")
            verify_ref(owner, REPO / "blueprint-cinema/episodes/EP007-exit-readiness-prep/review/decisions")
    else:
        expect(selection.get("hold_resolution") is None, "No prior hold exists for resolution")

    return {"short_id": short_id, "selected": selected, "selection": selection_path, "qc": qc_path, "script": script, "config": V3 / short_id / "TRANSFER-INPUT.json", "probe": probe}


def prior_usage(current_id: str) -> tuple[int, int]:
    for short_id in SHORT_IDS:
        expect(not (V3 / short_id / "ELEVEN-SUBMISSION-INTENT.json").exists(), f"Stopped narration-v3 already contains an ElevenLabs intent for {short_id}")
    intents = [(short_id, work(short_id) / "ELEVEN-SUBMISSION-INTENT.json") for short_id in SHORT_IDS if (work(short_id) / "ELEVEN-SUBMISSION-INTENT.json").exists()]
    expect(len(intents) < TRANSFER_CALL_CAP and all(short_id != current_id for short_id, _ in intents), "ElevenLabs transfer call cap or no-retry rule would be violated")
    consumed = 0
    for short_id, _ in intents:
        receipt_path = work(short_id) / "ELEVEN-RECEIPT.json"
        expect(receipt_path.is_file(), f"Prior {short_id} transfer outcome uncertain; stop")
        receipt = read_json(receipt_path)
        expect(receipt.get("http_status") == 200 and receipt.get("actual_credit_cost_verified") is True, f"Prior {short_id} transfer failed or cost unknown")
        consumed += int(receipt["actual_credit_cost"])
    return len(intents), consumed


def check(short_id: str) -> dict[str, Any]:
    guide = verify_guide(short_id)
    prior_calls, prior_credits = prior_usage(short_id)
    forecast = math.ceil(float(guide["probe"]["duration_seconds"]) * CREDITS_PER_MINUTE_FORECAST / 60)
    expect(prior_credits + forecast <= AGGREGATE_CREDIT_CEILING, "Aggregate 3200-credit operational ceiling would be exceeded")
    for name in ("TRANSFER-PREFLIGHT.json", "ELEVEN-SUBMISSION-INTENT.json", "ELEVEN-RECEIPT.json", "ELEVEN-ERROR.json", "media/elevenlabs-response.pcm", "media/original-c.wav"):
        expect(not (work(short_id) / name).exists(), f"Existing transfer artifact blocks another submission: {short_id}/{name}")
    return guide | {"prior_calls": prior_calls, "prior_credits": prior_credits, "forecast_credits": forecast}


def preflight(short_id: str) -> None:
    data = check(short_id)
    account, voice, headers = cap.read_account_and_voice()
    expect(int(account["remaining_included_credits"]) >= data["forecast_credits"], "Live included credit balance insufficient")
    path = work(short_id) / "TRANSFER-PREFLIGHT.json"
    cap.save_json_x(path, {
        "record_type": "ep007_original_c_transfer_preflight_v5", "at_utc": now(), "status": "pass_one_transfer_allowed", "short_id": short_id,
        "owner_source_sha256": sha_file(SOURCE), "owner_event_sha256": sha_file(EVENT), "runner_sha256": sha_file(RUNNER),
        "selection_sha256": sha_file(data["selection"]), "guide_asr_sha256": sha_file(data["qc"]), "selected_guide_sha256": sha_file(data["selected"]),
        "script_sha256": sha_file(data["script"]), "transfer_input_sha256": sha_file(data["config"]),
        "prior_transfer_calls": data["prior_calls"], "prior_actual_credits": data["prior_credits"],
        "forecast_credits": data["forecast_credits"], "aggregate_credit_ceiling": AGGREGATE_CREDIT_CEILING,
        "automatic_retries": 0, "account": account, "voice": voice, "readback_headers": headers, "provider_generation_calls_made": 0,
    })
    print(json.dumps({"status": "pass", "short_id": short_id, "forecast_credits": data["forecast_credits"], "included_remaining": account["remaining_included_credits"]}))


def transfer(short_id: str) -> None:
    base = work(short_id)
    preflight_path = base / "TRANSFER-PREFLIGHT.json"
    expect(preflight_path.is_file(), "Run preflight before transfer")
    before = read_json(preflight_path)
    expect(before.get("status") == "pass_one_transfer_allowed" and before.get("short_id") == short_id and before.get("runner_sha256") == sha_file(RUNNER), "Preflight does not bind current runner")
    data = verify_guide(short_id)
    calls, used = prior_usage(short_id)
    forecast = math.ceil(float(data["probe"]["duration_seconds"]) * CREDITS_PER_MINUTE_FORECAST / 60)
    expect(before.get("selection_sha256") == sha_file(data["selection"]) and before.get("guide_asr_sha256") == sha_file(data["qc"]) and before.get("selected_guide_sha256") == sha_file(data["selected"]), "Guide selection changed after preflight")
    expect(before.get("prior_transfer_calls") == calls and before.get("prior_actual_credits") == used and before.get("forecast_credits") == forecast, "Transfer state changed after preflight")
    expect(used + forecast <= AGGREGATE_CREDIT_CEILING, "Credit cap exceeded")
    for name in ("ELEVEN-SUBMISSION-INTENT.json", "ELEVEN-RECEIPT.json", "ELEVEN-ERROR.json", "media/elevenlabs-response.pcm", "media/original-c.wav"):
        expect(not (base / name).exists(), f"Transfer evidence already exists; no retry: {name}")
    account, voice, headers = cap.read_account_and_voice()
    expect(int(account["remaining_included_credits"]) >= forecast, "Live included credit balance insufficient")
    account_path = base / "ELEVEN-ACCOUNT-BEFORE.json"
    cap.save_json_x(account_path, {"at_utc": now(), "account": account, "voice": voice, "response_headers": headers, "forecast_credits": forecast})

    config = read_json(data["config"])
    guide_bytes = data["selected"].read_bytes()
    body, content_type = cap.cal.multipart(config["fields"], data["selected"].name, guide_bytes)
    url = f"{config['endpoint']}?output_format={config['output_format']}&enable_logging=true"
    intent_path = base / "ELEVEN-SUBMISSION-INTENT.json"
    receipt_path = base / "ELEVEN-RECEIPT.json"
    error_path = base / "ELEVEN-ERROR.json"
    raw_path = base / "media/elevenlabs-response.pcm"
    final_path = base / "media/original-c.wav"
    cap.save_json_x(intent_path, {
        "record_type": "ep007_original_c_submission_intent_v5", "at_utc": now(), "stage": "elevenlabs_voice_transfer", "short_id": short_id,
        "owner_source_sha256": sha_file(SOURCE), "owner_event_sha256": sha_file(EVENT), "runner_sha256": sha_file(RUNNER),
        "preflight_sha256": sha_file(preflight_path), "account_before_sha256": sha_file(account_path),
        "selection_sha256": sha_file(data["selection"]), "guide_asr_sha256": sha_file(data["qc"]),
        "guide_path": rel(data["selected"]), "guide_sha256": sha_file(data["selected"]),
        "script_sha256": sha_file(data["script"]), "transfer_input_sha256": sha_file(data["config"]),
        "url": url, "fields": config["fields"], "request_body_sha256": sha_bytes(body),
        "forecast_credits": forecast, "prior_actual_credits": used, "aggregate_credit_ceiling": AGGREGATE_CREDIT_CEILING,
        "provider_generation_attempt": 1, "automatic_retries": 0,
        "uncertain_outcome_policy": "preserve all evidence and stop; no retry under this authority",
    })
    key = cap.cal.read_dotenv_key("ELEVENLABS_API_KEY")
    try:
        status, raw, response_headers = cap.safe_request(url, method="POST", headers={"xi-api-key": key, "Content-Type": content_type, "Accept": "*/*"}, body=body)
    except Exception as exc:
        cap.save_json_x(error_path, {"at_utc": now(), "status": "uncertain_no_retry", "error_class": type(exc).__name__})
        fail("ElevenLabs transport outcome uncertain; no retry")
    cap.save_bytes_x(raw_path, raw)
    receipt: dict[str, Any] = {
        "record_type": "ep007_original_c_transfer_receipt_v5", "at_utc": now(), "short_id": short_id,
        "http_status": status, "response_headers": response_headers, "raw_response_path": rel(raw_path), "raw_response_sha256": sha_bytes(raw),
        "guide_sha256": sha_file(data["selected"]), "forecast_credits": forecast, "prior_actual_credits": used,
        "calls": 1, "retries": 0,
    }
    if status != 200:
        receipt["accepted"] = False
        receipt["error"] = cap.redact_error(raw, [key])
        cap.save_json_x(receipt_path, receipt)
        fail(f"ElevenLabs HTTP {status}; no retry")
    try:
        actual_credits = cap.parse_actual_eleven_cost(receipt)
    except ValueError as exc:
        receipt["actual_credit_cost_verified"] = False
        receipt["accepted"] = False
        receipt["error"] = str(exc)
        cap.save_json_x(receipt_path, receipt)
        fail("ElevenLabs cost header missing; preserved response and stopped")
    receipt["actual_credit_cost_verified"] = True
    receipt["actual_credit_cost"] = actual_credits
    receipt["aggregate_actual_credit_cost"] = used + actual_credits
    receipt["aggregate_credit_ceiling"] = AGGREGATE_CREDIT_CEILING
    if used + actual_credits > AGGREGATE_CREDIT_CEILING:
        receipt["accepted"] = False
        cap.save_json_x(receipt_path, receipt)
        fail("Actual ElevenLabs cost exceeded the operational ceiling; stopped")
    cap.cal.wav_from_pcm(raw, cap.cal.TRANSFER_OUTPUT_RATE_HZ, final_path)
    final_path.chmod(0o600)
    probe = cap.cal.probe(final_path)
    delta = float(probe["duration_seconds"]) - float(data["probe"]["duration_seconds"])
    tail = float(probe.get("tail_energy", 1))
    tail_class = "silent" if tail < cap.cal.TAIL_ENERGY_THRESHOLD else "marginal" if tail < 0.06 else "still_sounding"
    technical_pass = abs(delta) <= 0.5 and tail_class in ("silent", "marginal")
    receipt.update({
        "voice": probe | {"path": rel(final_path)}, "duration_delta_seconds": delta,
        "transfer_tail_class": tail_class, "technical_duration_and_tail_pass": technical_pass,
        "accepted_pending_final_exact_copy_asr_and_owner_listen": technical_pass,
    })
    cap.save_json_x(receipt_path, receipt)
    if not technical_pass:
        fail("Original C technical duration/tail gate failed; no retry")
    try:
        after, after_voice, after_headers = cap.read_account_and_voice()
        cap.save_json_x(base / "ELEVEN-ACCOUNT-AFTER.json", {"at_utc": now(), "account": after, "voice": after_voice, "response_headers": after_headers, "remaining_credit_delta": int(account["remaining_included_credits"]) - int(after["remaining_included_credits"]), "receipt_actual_credit_cost": actual_credits})
    except Exception as exc:
        cap.save_json_x(base / "ELEVEN-ACCOUNT-AFTER.json", {"at_utc": now(), "status": "readback_failed_non_destructive", "error_class": type(exc).__name__, "receipt_actual_credit_cost": actual_credits})
    print(json.dumps({"short_id": short_id, "duration_seconds": probe["duration_seconds"], "tail_class": tail_class, "forecast_credits": forecast, "actual_credits": actual_credits, "accepted_pending_final_asr_and_owner_listen": technical_pass}))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("check", "preflight", "transfer"))
    parser.add_argument("short_id", choices=SHORT_IDS)
    args = parser.parse_args()
    if args.command == "check":
        data = check(args.short_id)
        print(json.dumps({"status": "pass", "short_id": args.short_id, "guide_path": rel(data["selected"]), "forecast_credits": data["forecast_credits"], "prior_actual_credits": data["prior_credits"], "provider_calls_made": 0}))
    elif args.command == "preflight":
        preflight(args.short_id)
    else:
        transfer(args.short_id)


if __name__ == "__main__":
    main()
