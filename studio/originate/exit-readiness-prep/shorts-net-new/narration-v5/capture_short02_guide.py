#!/usr/bin/env python3
"""One-call, no-retry EP007 Short 02 Google guide continuation.

``check`` is a local input audit. ``preflight`` and ``submit`` require a fresh,
exact owner source record plus its appended decision event. Neither exists yet.
Only ``submit`` can reach Google; it writes an exclusive immutable intent before
the one POST. A transport error or uncertain QC is a no-retry hold.
"""
from __future__ import annotations

import argparse
import base64
import datetime as dt
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


sys.dont_write_bytecode = True
SELF = Path(__file__).resolve()
BASE = SELF.parent
REPO = next(path for path in (BASE, *BASE.parents) if path.name == "operator-economy")
SHORT_ID = "short-02-operations-business"
WORK = BASE / SHORT_ID
DECISIONS = REPO / "blueprint-cinema/episodes/EP007-exit-readiness-prep/review/decisions"
LOG = DECISIONS / "events.jsonl"
LOG_CLI = REPO / ".agents/skills/oe-video-direction/scripts/decision_log.py"
ENGINE_PATH = REPO / "studio/originate/exit-readiness-prep/shorts-net-new/narration-v1/capture_shorts.py"
CAL_PATH = REPO / "operator-blueprint-v2/02-narration-production/tools/calibrate.py"
V3 = REPO / "studio/originate/exit-readiness-prep/shorts-net-new/narration-v3"

SCRIPT_PACKAGE = REPO / "studio/originate/exit-readiness-prep/shorts-net-new/STANDALONE-SCRIPTS-V3.json"
SCRIPT = V3 / SHORT_ID / "SCRIPT.txt"
STYLE = V3 / SHORT_ID / "STYLE.json"
REQUEST = V3 / SHORT_ID / "GOOGLE-REQUEST.json"
VOICE_INPUT = V3 / SHORT_ID / "VOICE-INPUT.json"
PRIOR_HOLD = V3 / "BATCH-HOLD.json"
QC_PACKET = REPO / "studio/originate/exit-readiness-prep/shorts-net-new/SHORT-02-NARRATION-SHOT-QC-PACKET-V1.json"

PINS = {
    SCRIPT_PACKAGE: "6be1ee7c13ba6fc607d215e9a61c74fda31cc3f60026632eff6fc029f903cf6c",
    SCRIPT: "aee361d4542ed450365a50c70577f6b1bddd61c30de0571d770cbd91b0ed5542",
    STYLE: "f0bb3a6b581764b85dcd02df9b434a27fe0066b4b6f66347905a5baca48f1c5d",
    REQUEST: "51d3d17749feaab1f9c9ccb1ddafe3dce81c90b92a17f23892c34a867a97c36e",
    VOICE_INPUT: "92b23a35a74427d14ec2c6b9fef56fd5816e30122ae9500f3b450fe505c108c5",
    PRIOR_HOLD: "fb4cee5de2b86d7b9cd9044feee32a558b5a6785d13e82b7752cb8e46a532355",
    QC_PACKET: "abda0ea77fc2aabf85327a898b3f241469098e19be94c377fe988df57a536a17",
    ENGINE_PATH: "96395c162129d971ebf9bd7f798e65422392f0cc5891d0800b4c856835bd579b",
    CAL_PATH: "d59303278dbb79bef6fe0080f1d2b6c1e701e9228e95c7b3cdea4f3eec78cc00",
    LOG_CLI: "e9f82ad651ca0d38b81ca61cb9dc16f36871e676b7e82a9907d7e2cf7ec395cc",
}
REQUEST_BODY_SHA = "206595eb555fa9f474dfb72efb89f6cebb152e8a7f86f76c273acfb8875502a0"
CAP_USD = 0.05
ONE_CALL = 1
ROUTE_EVENT_ID = "ep007-shorts-02-04-avatar-route-v1"
ROUTE_CAPTURED_AT = dt.datetime.fromisoformat("2026-09-22T23:19:35.250319+00:00")
APPROVAL_PROMPT = (
    "I’ll keep the avatar. May I run one Google Algieba guide for Short 02’s locked script, "
    "with no retry and a $0.05 operational spend ceiling? I’ll stop after voice QC; this "
    "does not authorize Original C transfer, avatar clips, or rendering. The ceiling is a "
    "preflight limit, not a provider-enforced billing cap."
)
EXCLUSIONS = {
    "Original C transfer", "avatar generation", "lip-sync", "render", "release", "upload", "publication"
}

spec = importlib.util.spec_from_file_location("ep007_short02_v5_utilities", ENGINE_PATH)
if spec is None or spec.loader is None:
    raise SystemExit("Pinned narration utility module unavailable")
engine = importlib.util.module_from_spec(spec)
spec.loader.exec_module(engine)
cal = engine.cal


def sha_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha_file(path: Path) -> str:
    return sha_bytes(path.read_bytes())


def rel(path: Path) -> str:
    return str(path.relative_to(REPO))


def now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise SystemExit(f"Expected JSON object: {rel(path)}")
    return value


def check_inputs() -> tuple[dict[str, Any], bytes, float]:
    for path, expected in PINS.items():
        if not path.is_file() or sha_file(path) != expected:
            raise SystemExit(f"Pinned input unavailable or changed: {rel(path)}")
    old = read_json(PRIOR_HOLD)
    if old.get("status") != "stopped_no_retry":
        raise SystemExit("Historical stopped-batch state changed")
    locked = next(
        (row for row in read_json(SCRIPT_PACKAGE).get("scripts", []) if row.get("id") == SHORT_ID), None
    )
    if not locked or SCRIPT.read_text(encoding="utf-8") != locked.get("spoken_copy"):
        raise SystemExit("Prepared Short 02 script no longer equals locked spoken copy")
    request = read_json(REQUEST)
    style = read_json(STYLE)
    body = cal.compact_json(request)
    if request.get("input", {}).get("text") != locked["spoken_copy"]:
        raise SystemExit("Google request text differs from locked Short 02 copy")
    if request.get("input", {}).get("prompt") != style.get("style_instructions"):
        raise SystemExit("Google request acting direction differs from pinned style")
    if request.get("voice") != {"languageCode": "en-US", "modelName": "gemini-2.5-pro-tts", "name": "Algieba"}:
        raise SystemExit("Guide model/voice drifted")
    if request.get("audioConfig") != {"audioEncoding": "LINEAR16", "sampleRateHertz": 24000}:
        raise SystemExit("Guide format request drifted")
    if sha_bytes(body) != REQUEST_BODY_SHA:
        raise SystemExit("Canonical request body hash drifted")
    voice = read_json(VOICE_INPUT)
    if voice.get("script_sha256") != PINS[SCRIPT] or voice.get("google_request_body_sha256") != REQUEST_BODY_SHA:
        raise SystemExit("Prepared voice-input binding drifted")
    forecast_seconds = len(locked["spoken_copy"]) / cal.CHARS_PER_SECOND
    forecast_usd = engine.google_cost(request, forecast_seconds)
    if forecast_usd > CAP_USD:
        raise SystemExit("Guide forecast exceeds the proposed $0.05 operational ceiling")
    return request, body, forecast_usd


def expected_authorization() -> dict[str, Any]:
    return {
        "short_id": SHORT_ID,
        "script_sha256": PINS[SCRIPT],
        "google_request_sha256": PINS[REQUEST],
        "google_request_body_sha256": REQUEST_BODY_SHA,
        "guide_model": "gemini-2.5-pro-tts",
        "guide_voice": "Algieba",
        "google_guide_calls_max": ONE_CALL,
        "google_spend_forecast_cap_usd": CAP_USD,
        "automatic_retries": 0,
        "manual_retries": 0,
        "scope": "short02_google_guide_only",
    }


def scoped_file(path_text: str | None, label: str) -> Path:
    if not path_text:
        raise SystemExit(f"Missing fresh exact owner {label}; no provider submission allowed")
    path = Path(path_text).resolve()
    if path.parent != DECISIONS.resolve() or not path.is_file() or path.suffix != ".json":
        raise SystemExit(f"Fresh owner {label} must be an existing EP007 decision JSON file")
    return path


def fresh_owner_authorization(source_arg: str | None, event_arg: str | None) -> tuple[Path, Path, str, str]:
    source_path = scoped_file(source_arg, "source record")
    event_path = scoped_file(event_arg, "decision event")
    if source_path == event_path:
        raise SystemExit("Owner source record and decision event must be different files")
    source = read_json(source_path)
    event = read_json(event_path)
    if source.get("record_type") != "ep007_owner_direction_source" or source.get("prompt_presented_for_approval") != APPROVAL_PROMPT:
        raise SystemExit("Owner source does not bind the exact question already presented")
    reply = str(source.get("owner_verbatim", "")).strip()
    affirmative = re.fullmatch(r"(?i)(yes—one guide only|yes|approved|approve|go|go ahead|okay|ok|sure|do it)[.!]?", reply)
    if affirmative is None:
        raise SystemExit("Fresh owner response is not an unqualified affirmative")
    captured = source.get("captured_at_utc")
    try:
        captured_at = dt.datetime.fromisoformat(str(captured).replace("Z", "+00:00"))
    except ValueError as exc:
        raise SystemExit("Owner source has no valid capture time") from exc
    if captured_at.tzinfo is None or captured_at <= ROUTE_CAPTURED_AT:
        raise SystemExit("Owner source is not fresh relative to the avatar-route choice")
    if source.get("authorized") != expected_authorization():
        raise SystemExit("Owner source does not exactly authorize this one-guide input/cap")
    if not EXCLUSIONS.issubset(set(source.get("not_authorized", []))):
        raise SystemExit("Owner source does not retain all excluded later stages")
    data = event.get("data", {})
    if (
        event.get("event_type") != "feedback"
        or event.get("decision_id") != "ep007-shorts-02-04-production-route"
        or data.get("decision_event_id") != ROUTE_EVENT_ID
        or data.get("actor") != "owner"
        or data.get("verdict") != "accept"
        or data.get("verbatim") != reply
        or data.get("authorized") != expected_authorization()
        or not EXCLUSIONS.issubset(set(data.get("not_authorized", [])))
    ):
        raise SystemExit("Decision event does not match the exact fresh guide authorization")
    source_sha = sha_file(source_path)
    needed_evidence = {
        (rel(source_path), source_sha),
        (rel(SCRIPT_PACKAGE), PINS[SCRIPT_PACKAGE]),
        (rel(SCRIPT), PINS[SCRIPT]),
        (rel(REQUEST), PINS[REQUEST]),
    }
    actual_evidence = {
        (row.get("path"), row.get("sha256")) for row in event.get("evidence", []) if isinstance(row, dict)
    }
    if not needed_evidence.issubset(actual_evidence):
        raise SystemExit("Decision event omits required source and exact-input hashes")
    core_keys = ("event_id", "decision_id", "event_type", "tags", "data", "evidence")
    matching = []
    for line in LOG.read_text(encoding="utf-8").splitlines():
        row = json.loads(line)
        if row.get("event_id") == event.get("event_id"):
            matching.append(row)
    if len(matching) != 1 or any(matching[0].get(key) != event.get(key) for key in core_keys):
        raise SystemExit("Owner authorization event is not uniquely appended to EP007 decision log")
    try:
        event_captured_at = dt.datetime.fromisoformat(str(matching[0].get("captured_at", "")).replace("Z", "+00:00"))
    except ValueError as exc:
        raise SystemExit("Owner authorization event has no valid capture time") from exc
    if event_captured_at.tzinfo is None or event_captured_at <= ROUTE_CAPTURED_AT:
        raise SystemExit("Owner authorization event precedes the route choice")
    chain = subprocess.run(
        [sys.executable, str(LOG_CLI), "validate", "--episode", "EP007-exit-readiness-prep"],
        cwd=REPO, capture_output=True, text=True, timeout=30, check=False,
    )
    if chain.returncode != 0:
        raise SystemExit("EP007 decision chain validation failed")
    return source_path, event_path, source_sha, sha_file(event_path)


def no_prior_attempt() -> None:
    for prior in BASE.parent.glob(f"narration-v*/{SHORT_ID}/GOOGLE-SUBMISSION-INTENT.json"):
        if prior.parent != WORK:
            raise SystemExit(f"Short 02 guide intent exists in another narration version: {rel(prior)}")
    for name in ("GOOGLE-SUBMISSION-INTENT.json", "GOOGLE-RECEIPT.json", "HOLD.json"):
        if (WORK / name).exists():
            raise SystemExit(f"Existing Short 02 v5 {name}; no retry or resubmission")
    if WORK.exists() and any(WORK.iterdir()):
        raise SystemExit("Short 02 v5 work directory already contains material; inspect before any call")


def preflight(source_arg: str | None, event_arg: str | None) -> tuple[dict[str, Any], bytes, float, Path, Path, str, str]:
    request, body, forecast = check_inputs()
    source, event, source_sha, event_sha = fresh_owner_authorization(source_arg, event_arg)
    no_prior_attempt()
    return request, body, forecast, source, event, source_sha, event_sha


def write_hold(status: str, reason: str) -> None:
    path = WORK / "HOLD.json"
    if path.exists():
        return
    engine.save_json_x(path, {
        "record_type": "ep007_short02_google_guide_hold_v5",
        "at_utc": now(),
        "status": status,
        "reason": reason,
        "attempt_count": 1,
        "automatic_retries": 0,
        "manual_retries_authorized": 0,
        "decision": "stop_and_preserve_input_response_and_receipt; no transfer or retry",
    })


def submit(source_arg: str | None, event_arg: str | None) -> None:
    request, body, forecast, source, event, source_sha, event_sha = preflight(source_arg, event_arg)
    # Credentials and quota project are checked before the intent; no provider POST occurs here.
    token = cal.google_access_token()
    project = cal.google_quota_project()
    if not token or not project:
        raise SystemExit("Google ADC token or quota project unavailable; zero POSTs")
    if check_inputs()[1] != body:
        raise SystemExit("Locked Google request changed during credential preflight; zero POSTs")
    fresh_source, fresh_event, fresh_source_sha, fresh_event_sha = fresh_owner_authorization(source_arg, event_arg)
    if (fresh_source, fresh_event, fresh_source_sha, fresh_event_sha) != (source, event, source_sha, event_sha):
        raise SystemExit("Fresh owner authorization changed during credential preflight; zero POSTs")
    no_prior_attempt()
    WORK.mkdir(parents=True, exist_ok=True)
    (WORK / "media").mkdir(exist_ok=True)
    intent = WORK / "GOOGLE-SUBMISSION-INTENT.json"
    engine.save_json_x(intent, {
        "record_type": "ep007_short02_google_guide_submission_intent_v5",
        "at_utc": now(),
        "short_id": SHORT_ID,
        "stage": "google_guide_only",
        "runner_path": rel(SELF),
        "runner_sha256": sha_file(SELF),
        "owner_source_path": rel(source),
        "owner_source_sha256": source_sha,
        "owner_event_path": rel(event),
        "owner_event_sha256": event_sha,
        "script_path": rel(SCRIPT),
        "script_sha256": PINS[SCRIPT],
        "request_path": rel(REQUEST),
        "request_sha256": PINS[REQUEST],
        "request_body_sha256": sha_bytes(body),
        "provider_generation_attempt": 1,
        "google_guide_call_cap": 1,
        "automatic_retries": 0,
        "operational_forecast_usd": forecast,
        "operational_forecast_cap_usd": CAP_USD,
        "provider_enforced_billing_cap": False,
        "uncertain_outcome_policy": "hold_and_never_retry_under_this_authorization",
    })
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json; charset=utf-8",
        "x-goog-user-project": project,
    }
    try:
        status, raw, response_headers = engine.safe_request(
            cal.GUIDE_ENDPOINT, method="POST", headers=headers, body=body
        )
    except Exception:
        write_hold("transport_outcome_uncertain", "Provider outcome unknown after exclusive intent")
        raise SystemExit("Google submission outcome uncertain; no retry. Inspect v5 intent and hold.")
    try:
        raw_path = WORK / "media/google-response.bin"
        engine.save_bytes_x(raw_path, raw)
    except Exception:
        write_hold("response_persistence_uncertain", "Provider returned but raw response could not be preserved")
        raise SystemExit("Google response persistence uncertain; no retry. Inspect v5 intent and hold.")
    receipt: dict[str, Any] = {
        "record_type": "ep007_short02_google_guide_receipt_v5",
        "at_utc": now(),
        "short_id": SHORT_ID,
        "http_status": status,
        "response_headers": response_headers,
        "intent_path": rel(intent),
        "intent_sha256": sha_file(intent),
        "raw_response_path": rel(raw_path),
        "raw_response_sha256": sha_file(raw_path),
        "calls": 1,
        "retries": 0,
        "provider_enforced_billing_cap": False,
        "guide_accepted_for_transfer": False,
    }
    if status != 200:
        receipt["status"] = "http_failure_no_retry"
        engine.save_json_x(WORK / "GOOGLE-RECEIPT.json", receipt)
        write_hold("http_failure", f"HTTP {status}; raw response preserved")
        raise SystemExit(f"Google HTTP {status}; no retry. Raw response and receipt preserved.")
    try:
        payload = json.loads(raw)
        audio = base64.b64decode(payload["audioContent"], validate=True)
        if not audio:
            raise ValueError("empty audioContent")
        guide = WORK / "media/guide.wav"
        engine.save_bytes_x(guide, audio)
        probe = cal.probe(guide)
        duration = float(probe["duration_seconds"])
    except Exception:
        receipt["status"] = "decode_or_probe_failure_no_retry"
        engine.save_json_x(WORK / "GOOGLE-RECEIPT.json", receipt)
        write_hold("decode_or_probe_failure", "Raw provider response preserved; guide unusable or uncertain")
        raise SystemExit("Google audio decode or probe failed; no retry. Raw response preserved.")
    actual_estimate = engine.google_cost(request, duration)
    format_pass = (
        probe.get("sample_rate_hz") == 24000
        and probe.get("channels") == 1
        and probe.get("sample_width_bits") == 16
    )
    tail_pass = probe.get("ends_in_silence") is True
    cap_pass = actual_estimate <= CAP_USD
    receipt.update({
        "guide_path": rel(guide),
        "guide_sha256": sha_file(guide),
        "guide_probe": probe,
        "estimated_cost_usd_conservative_input_tokens": actual_estimate,
        "cost_is_invoice": False,
        "format_pass": format_pass,
        "tail_energy_less_than_0_02": tail_pass,
        "operational_cap_pass": cap_pass,
        "exact_copy_asr": "not_run",
        "owner_listening": "pending",
        "status": (
            "pending_exact_copy_asr_and_owner_listening"
            if format_pass and tail_pass and cap_pass else "hold_pending_inspection_no_retry"
        ),
    })
    engine.save_json_x(WORK / "GOOGLE-RECEIPT.json", receipt)
    if not format_pass or not tail_pass or not cap_pass:
        reasons = [name for name, passed in (("format", format_pass), ("tail", tail_pass), ("forecast_cap", cap_pass)) if not passed]
        write_hold("qc_hold_pending_inspection", ", ".join(reasons))
        raise SystemExit("Short 02 guide on hold pending inspection; source preserved, no retry or transfer.")
    print(json.dumps({
        "status": "guide_captured_pending_exact_copy_asr_and_owner_listening",
        "short_id": SHORT_ID,
        "guide_sha256": sha_file(guide),
        "duration_seconds": duration,
        "tail_energy": probe.get("tail_energy"),
        "estimated_usd_not_invoice": actual_estimate,
        "provider_calls": 1,
        "retries": 0,
    }))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("check", "preflight", "submit"))
    parser.add_argument("--owner-source", help="Fresh owner source record in the EP007 decisions directory")
    parser.add_argument("--owner-event", help="Matching appended owner/accept event JSON in the EP007 decisions directory")
    args = parser.parse_args()
    if args.command == "check":
        _, _, forecast = check_inputs()
        print(json.dumps({
            "status": "locked_inputs_pass_no_authority_checked",
            "short_id": SHORT_ID,
            "script_sha256": PINS[SCRIPT],
            "google_request_sha256": PINS[REQUEST],
            "operational_forecast_usd": forecast,
            "operational_cap_usd": CAP_USD,
            "provider_calls": 0,
        }))
    elif args.command == "preflight":
        _, _, forecast, source, event, _, _ = preflight(args.owner_source, args.owner_event)
        print(json.dumps({
            "status": "exact_fresh_authority_and_inputs_pass_no_provider_call",
            "short_id": SHORT_ID,
            "owner_source": rel(source),
            "owner_event": rel(event),
            "operational_forecast_usd": forecast,
            "provider_calls": 0,
        }))
    else:
        submit(args.owner_source, args.owner_event)


if __name__ == "__main__":
    main()
