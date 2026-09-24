#!/usr/bin/env python3
"""One-attempt Google Algieba guides for locked EP007 Shorts 03 and 04.

``check`` and ``preflight`` are local-only. ``submit --short`` is the only
provider path. It creates an exclusive intent before one POST, preserves the
raw response, and never retries or silently advances to Original C transfer.
The historical stopped v3 batch is not resumed.
"""
from __future__ import annotations

import argparse
import base64
import datetime as dt
import hashlib
import importlib.util
import json
import math
import subprocess
import sys
from pathlib import Path
from typing import Any


sys.dont_write_bytecode = True
SELF = Path(__file__).resolve()
BASE = SELF.parent
REPO = next(path for path in (BASE, *BASE.parents) if path.name == "operator-economy")
V3 = BASE.parent / "narration-v3"
DECISIONS = REPO / "blueprint-cinema/episodes/EP007-exit-readiness-prep/review/decisions"
LOG = DECISIONS / "events.jsonl"
LOG_CLI = REPO / ".agents/skills/oe-video-direction/scripts/decision_log.py"
ENGINE_PATH = BASE.parent / "narration-v1/capture_shorts.py"
CAL_PATH = REPO / "operator-blueprint-v2/02-narration-production/tools/calibrate.py"
SCRIPT_PACKAGE = BASE.parent / "STANDALONE-SCRIPTS-V3.json"
PRIOR_HOLD = V3 / "BATCH-HOLD.json"

# Bind these to the exact fresh full-pipeline owner records before any submit.
# The local `check` command deliberately does not require authorization.
OWNER_SOURCE_NAME = "ep007-owner-authorize-shorts-02-04-full-private-production-20260923.json"
OWNER_SOURCE_SHA256 = "e6b4bf17f2eec1f258b8dc65ca060ce2262dd4eaba070bdbb59bfdf85bda9f85"
OWNER_EVENT_NAME = "ep007-shorts-02-04-full-private-production-authorized-v3.json"
OWNER_EVENT_SHA256 = "c1baa48b414d988a570cfc162bcbdc6886e9b21dbc15fe4c22dc4022b414c201"
OWNER_VERBATIM = "Go for all of them the full pipeline. I want to get them done and make edits after if necessary"
ALLOWED_STAGE = "first_pass_private_review_sound_on_video_production"
MAX_AGGREGATE_FORECAST_USD = 0.15
SHORT02_RECEIPT = BASE / "short-02-operations-business/GOOGLE-RECEIPT.json"

SHARED_PINS = {
    SCRIPT_PACKAGE: "6be1ee7c13ba6fc607d215e9a61c74fda31cc3f60026632eff6fc029f903cf6c",
    PRIOR_HOLD: "fb4cee5de2b86d7b9cd9044feee32a558b5a6785d13e82b7752cb8e46a532355",
    ENGINE_PATH: "96395c162129d971ebf9bd7f798e65422392f0cc5891d0800b4c856835bd579b",
    CAL_PATH: "d59303278dbb79bef6fe0080f1d2b6c1e701e9228e95c7b3cdea4f3eec78cc00",
    LOG_CLI: "e9f82ad651ca0d38b81ca61cb9dc16f36871e676b7e82a9907d7e2cf7ec395cc",
    SHORT02_RECEIPT: "968e53dc057931cbc3f0f0b059c66a1b6e55141558471c9bddd665006e1bf04a",
}
SHORTS = {
    "short-03-how-you-charge": {
        "script_sha256": "2a56beffef964667fbd09c934130d53171da605e23f876e75a4cb715a03efc3b",
        "style_sha256": "f0bb3a6b581764b85dcd02df9b434a27fe0066b4b6f66347905a5baca48f1c5d",
        "request_sha256": "b6d22f29b829d3c80bab7595316df85ace329c70367e379440c315f49fea4983",
        "voice_input_sha256": "5eae5bbb6ac1a80a2e5e867b75649435a76026a4f37cba7efb0f60fc1c37915c",
        "body_sha256": "1955bc25693277e5402889f5be6ced5e523060ac1091535f74253328a433cfe7",
    },
    "short-04-test-the-front-door": {
        "script_sha256": "fb1021dc78cfb7c717aacdcef665d69a3651b6db8c0b9b129dab3e6c1b6ea60f",
        "style_sha256": "f0bb3a6b581764b85dcd02df9b434a27fe0066b4b6f66347905a5baca48f1c5d",
        "request_sha256": "b8e9bcf0a36eaec8420190264813ca4162fc8f2f55581a27b74a903c0dfe0eae",
        "voice_input_sha256": "e3dee41dc0b9c6351c0712784245f8fb4baed2e07332c4d87a4e16e6c9e99a7f",
        "body_sha256": "5aafa7d6fad0b49a28d5cc307532b50d1461a8a9423bebd58ac51ad7026eae2a",
    },
}

spec = importlib.util.spec_from_file_location("ep007_shorts_03_04_utilities", ENGINE_PATH)
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


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise SystemExit(f"Expected JSON object: {rel(path)}")
    return value


def paths(short_id: str) -> dict[str, Path]:
    source = V3 / short_id
    return {
        "script": source / "SCRIPT.txt",
        "style": source / "STYLE.json",
        "request": source / "GOOGLE-REQUEST.json",
        "voice_input": source / "VOICE-INPUT.json",
        "work": BASE / short_id,
    }


def check_inputs() -> tuple[dict[str, tuple[dict[str, Any], bytes, float]], float]:
    for path, expected in SHARED_PINS.items():
        if not path.is_file() or sha_file(path) != expected:
            raise SystemExit(f"Pinned shared input unavailable or changed: {rel(path)}")
    if read_json(PRIOR_HOLD).get("status") != "stopped_no_retry":
        raise SystemExit("Historical stopped-batch state changed")
    locked = {row.get("id"): row for row in read_json(SCRIPT_PACKAGE).get("scripts", [])}
    out: dict[str, tuple[dict[str, Any], bytes, float]] = {}
    short02 = read_json(SHORT02_RECEIPT)
    if short02.get("short_id") != "short-02-operations-business" or short02.get("calls") != 1:
        raise SystemExit("Short 02 consumed-call record changed")
    aggregate = float(short02.get("estimated_cost_usd_conservative_input_tokens", float("inf")))
    for short_id, pins in SHORTS.items():
        p = paths(short_id)
        for name, key in (("script", "script_sha256"), ("style", "style_sha256"),
                          ("request", "request_sha256"), ("voice_input", "voice_input_sha256")):
            path = p[name]
            if not path.is_file() or sha_file(path) != pins[key]:
                raise SystemExit(f"Pinned {short_id} input unavailable or changed: {rel(path)}")
        spoken_copy = locked.get(short_id, {}).get("spoken_copy")
        if not isinstance(spoken_copy, str) or p["script"].read_text(encoding="utf-8") != spoken_copy:
            raise SystemExit(f"{short_id} prepared script differs from locked spoken copy")
        request = read_json(p["request"])
        style = read_json(p["style"])
        body = cal.compact_json(request)
        if request.get("input", {}).get("text") != spoken_copy:
            raise SystemExit(f"{short_id} Google request text differs from locked spoken copy")
        if request.get("input", {}).get("prompt") != style.get("style_instructions"):
            raise SystemExit(f"{short_id} Google acting direction differs from pinned style")
        if request.get("voice") != {"languageCode": "en-US", "modelName": "gemini-2.5-pro-tts", "name": "Algieba"}:
            raise SystemExit(f"{short_id} guide voice/model drifted")
        if request.get("audioConfig") != {"audioEncoding": "LINEAR16", "sampleRateHertz": 24000}:
            raise SystemExit(f"{short_id} guide format drifted")
        if sha_bytes(body) != pins["body_sha256"]:
            raise SystemExit(f"{short_id} canonical request-body hash drifted")
        voice_input = read_json(p["voice_input"])
        if voice_input.get("script_sha256") != pins["script_sha256"] or voice_input.get("google_request_body_sha256") != pins["body_sha256"]:
            raise SystemExit(f"{short_id} prepared voice-input binding drifted")
        forecast_seconds = len(spoken_copy) / cal.CHARS_PER_SECOND
        forecast_usd = engine.google_cost(request, forecast_seconds)
        out[short_id] = request, body, forecast_usd
        current_intent = p["work"] / "GOOGLE-SUBMISSION-INTENT.json"
        current_receipt = p["work"] / "GOOGLE-RECEIPT.json"
        if current_intent.exists() and not current_receipt.exists():
            raise SystemExit(f"{short_id} has an unresolved guide attempt; aggregate spend unknown")
        if current_receipt.exists():
            prior = read_json(current_receipt)
            if prior.get("short_id") != short_id or prior.get("calls") != 1 or not current_intent.is_file():
                raise SystemExit(f"{short_id} guide receipt/intention binding is inconsistent")
            observed = float(prior.get("estimated_cost_usd_conservative_input_tokens", float("inf")))
            if not math.isfinite(observed) or observed <= 0:
                raise SystemExit(f"{short_id} guide cost is unknown; cannot budget next call")
            aggregate += observed
        else:
            aggregate += forecast_usd
    if aggregate > MAX_AGGREGATE_FORECAST_USD:
        raise SystemExit("Shorts 02–04 aggregate Google forecast exceeds $0.15 execution guardrail")
    return out, aggregate


def fresh_authorization() -> tuple[Path, Path, str, str]:
    if not all((OWNER_SOURCE_NAME, OWNER_SOURCE_SHA256, OWNER_EVENT_NAME, OWNER_EVENT_SHA256)):
        raise SystemExit("Exact fresh full-pipeline owner source/event not bound; zero provider calls")
    source = DECISIONS / OWNER_SOURCE_NAME
    event = DECISIONS / OWNER_EVENT_NAME
    for path, expected in ((source, OWNER_SOURCE_SHA256), (event, OWNER_EVENT_SHA256)):
        if not path.is_file() or sha_file(path) != expected:
            raise SystemExit(f"Pinned owner authorization unavailable or changed: {rel(path)}")
    source_obj = read_json(source)
    event_obj = read_json(event)
    if source_obj.get("record_type") != "ep007_owner_direction_source" or source_obj.get("owner_verbatim") != OWNER_VERBATIM:
        raise SystemExit("Owner source does not contain the exact fresh full-pipeline direction")
    if event_obj.get("event_type") != "feedback" or event_obj.get("decision_id") != "ep007-shorts-02-04-production-route":
        raise SystemExit("Owner decision event has unexpected type or route")
    data = event_obj.get("data", {})
    if (data.get("actor") != "owner" or data.get("verbatim") != OWNER_VERBATIM
            or data.get("verdict") != "accept"
            or data.get("decision_event_id") != "ep007-shorts-02-04-avatar-route-v1"):
        raise SystemExit("Owner decision event does not repeat the exact owner direction")
    if (rel(source), OWNER_SOURCE_SHA256) not in {
        (row.get("path"), row.get("sha256")) for row in event_obj.get("evidence", []) if isinstance(row, dict)
    }:
        raise SystemExit("Owner decision event does not bind source hash")
    source_scope = source_obj.get("authorized", {})
    event_scope = data.get("authorized", {})
    if source_scope != event_scope or source_scope.get("scope") != ALLOWED_STAGE:
        raise SystemExit("Owner authorization scope is missing or inconsistent")
    if source_scope.get("short_ids") != ["short-02-operations-business", *SHORTS]:
        raise SystemExit("Full-pipeline authorization does not bind all exact Short IDs")
    if "Google Algieba guides" not in source_scope.get("stages", []) or source_scope.get("script_package_sha256") != SHARED_PINS[SCRIPT_PACKAGE]:
        raise SystemExit("Full-pipeline authorization does not bind locked scripts and Google guide stage")
    limits = source_obj.get("agent_execution_limits_not_owner_quoted", {})
    if limits != data.get("agent_execution_limits_not_owner_quoted"):
        raise SystemExit("Execution limits changed between owner source and event")
    if (limits.get("google_guide_calls_max_across_shorts_02_to_04") != 3
            or limits.get("google_guide_calls_already_consumed_short_02") != 1
            or limits.get("google_guide_forecast_usd_max_across_shorts_02_to_04") != MAX_AGGREGATE_FORECAST_USD
            or limits.get("automatic_retries") != 0
            or limits.get("extra_paid_retries_without_new_owner_direction") != 0):
        raise SystemExit("One-attempt Google execution limits are not explicit")
    excluded = set(source_obj.get("not_authorized", []))
    if not {"Content OS release", "upload", "publication", "unbounded model substitutions or paid retries"}.issubset(excluded):
        raise SystemExit("Public release or extra paid retries were not explicitly excluded")
    core_keys = ("event_id", "decision_id", "event_type", "tags", "data", "evidence")
    matches = [json.loads(line) for line in LOG.read_text(encoding="utf-8").splitlines()
               if json.loads(line).get("event_id") == event_obj.get("event_id")]
    if len(matches) != 1 or any(matches[0].get(key) != event_obj.get(key) for key in core_keys):
        raise SystemExit("Owner authorization event not uniquely appended to EP007 decision log")
    chain = subprocess.run(
        [sys.executable, str(LOG_CLI), "validate", "--episode", "EP007-exit-readiness-prep"],
        cwd=REPO, capture_output=True, text=True, timeout=30, check=False,
    )
    if chain.returncode != 0:
        raise SystemExit("EP007 decision chain validation failed")
    return source, event, OWNER_SOURCE_SHA256, OWNER_EVENT_SHA256


def no_prior_attempt(short_id: str) -> None:
    work = paths(short_id)["work"]
    for prior in BASE.parent.glob(f"narration-v*/{short_id}/GOOGLE-SUBMISSION-INTENT.json"):
        if prior.parent != work:
            raise SystemExit(f"Prior {short_id} guide intent exists: {rel(prior)}")
    if work.exists() and any(work.iterdir()):
        raise SystemExit(f"{short_id} v5 work directory already contains material; no retry")


def preflight(short_id: str) -> tuple[dict[str, Any], bytes, float, float, Path, Path, str, str]:
    checked, aggregate = check_inputs()
    source, event, source_sha, event_sha = fresh_authorization()
    no_prior_attempt(short_id)
    request, body, forecast = checked[short_id]
    return request, body, forecast, aggregate, source, event, source_sha, event_sha


def write_hold(work: Path, status: str, reason: str) -> None:
    path = work / "HOLD.json"
    if path.exists():
        return
    engine.save_json_x(path, {
        "record_type": "ep007_google_guide_no_retry_hold_v5",
        "at_utc": utc_now(),
        "status": status,
        "reason": reason,
        "attempt_count": 1,
        "automatic_retries": 0,
        "decision": "stop_and_preserve_input_response_and_receipt; no retry or automatic transfer",
    })


def submit(short_id: str) -> None:
    request, body, forecast, aggregate, source, event, source_sha, event_sha = preflight(short_id)
    token = cal.google_access_token()
    project = cal.google_quota_project()
    if not token or not project:
        raise SystemExit("Google ADC token or quota project unavailable; zero POSTs")
    checked_again, aggregate_again = check_inputs()
    if checked_again[short_id][1] != body or aggregate_again != aggregate:
        raise SystemExit("Locked request or aggregate forecast changed during credential preflight; zero POSTs")
    if fresh_authorization() != (source, event, source_sha, event_sha):
        raise SystemExit("Owner authorization changed during credential preflight; zero POSTs")
    no_prior_attempt(short_id)
    p = paths(short_id)
    work = p["work"]
    work.mkdir(parents=True, exist_ok=True)
    (work / "media").mkdir(exist_ok=True)
    intent = work / "GOOGLE-SUBMISSION-INTENT.json"
    engine.save_json_x(intent, {
        "record_type": "ep007_google_guide_submission_intent_v5",
        "at_utc": utc_now(),
        "short_id": short_id,
        "stage": "google_guide_only",
        "runner_path": rel(SELF),
        "runner_sha256": sha_file(SELF),
        "owner_source_path": rel(source),
        "owner_source_sha256": source_sha,
        "owner_event_path": rel(event),
        "owner_event_sha256": event_sha,
        "script_path": rel(p["script"]),
        "script_sha256": SHORTS[short_id]["script_sha256"],
        "request_path": rel(p["request"]),
        "request_sha256": SHORTS[short_id]["request_sha256"],
        "request_body_sha256": sha_bytes(body),
        "provider_generation_attempt": 1,
        "google_guide_call_cap_for_this_short": 1,
        "automatic_retries": 0,
        "operational_forecast_usd": forecast,
        "short02_04_aggregate_forecast_usd": aggregate,
        "aggregate_operational_forecast_cap_usd": MAX_AGGREGATE_FORECAST_USD,
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
        write_hold(work, "transport_outcome_uncertain", "Provider outcome unknown after exclusive intent")
        raise SystemExit("Google submission outcome uncertain; no retry. Inspect intent and hold.")
    try:
        raw_path = work / "media/google-response.bin"
        engine.save_bytes_x(raw_path, raw)
    except Exception:
        write_hold(work, "response_persistence_uncertain", "Provider returned but raw response could not be preserved")
        raise SystemExit("Google response persistence uncertain; no retry. Inspect intent and hold.")
    receipt: dict[str, Any] = {
        "record_type": "ep007_google_guide_receipt_v5",
        "at_utc": utc_now(),
        "short_id": short_id,
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
        engine.save_json_x(work / "GOOGLE-RECEIPT.json", receipt)
        write_hold(work, "http_failure", f"HTTP {status}; raw response preserved")
        raise SystemExit(f"Google HTTP {status}; no retry. Raw response and receipt preserved.")
    try:
        payload = json.loads(raw)
        audio = base64.b64decode(payload["audioContent"], validate=True)
        if not audio:
            raise ValueError("empty audioContent")
        guide = work / "media/guide.wav"
        engine.save_bytes_x(guide, audio)
        probe = cal.probe(guide)
        duration = float(probe["duration_seconds"])
    except Exception:
        receipt["status"] = "decode_or_probe_failure_no_retry"
        engine.save_json_x(work / "GOOGLE-RECEIPT.json", receipt)
        write_hold(work, "decode_or_probe_failure", "Raw response preserved; guide unusable or uncertain")
        raise SystemExit("Google audio decode or probe failed; no retry. Raw response preserved.")
    actual_estimate = engine.google_cost(request, duration)
    format_pass = (
        probe.get("sample_rate_hz") == 24000
        and probe.get("channels") == 1
        and probe.get("sample_width_bits") == 16
    )
    tail_pass = probe.get("ends_in_silence") is True
    post_call_aggregate_estimate = aggregate - forecast + actual_estimate
    cap_pass = post_call_aggregate_estimate <= MAX_AGGREGATE_FORECAST_USD
    receipt.update({
        "guide_path": rel(guide),
        "guide_sha256": sha_file(guide),
        "guide_probe": probe,
        "estimated_cost_usd_conservative_input_tokens": actual_estimate,
        "cost_is_invoice": False,
        "format_pass": format_pass,
        "tail_energy_less_than_0_02": tail_pass,
        "post_call_aggregate_estimate_usd": post_call_aggregate_estimate,
        "aggregate_cap_pass": cap_pass,
        "exact_copy_asr": "not_run",
        "owner_listening": "pending",
        "status": (
            "pending_exact_copy_asr_and_owner_listening"
            if format_pass and tail_pass and cap_pass else "hold_pending_inspection_no_retry"
        ),
    })
    engine.save_json_x(work / "GOOGLE-RECEIPT.json", receipt)
    if not format_pass or not tail_pass or not cap_pass:
        reasons = [name for name, passed in (("format", format_pass), ("tail", tail_pass), ("estimate_cap", cap_pass)) if not passed]
        write_hold(work, "qc_hold_pending_inspection", ", ".join(reasons))
        raise SystemExit(f"{short_id} guide on hold; source preserved, no retry or transfer.")
    print(json.dumps({
        "status": "guide_captured_pending_exact_copy_asr_and_owner_listening",
        "short_id": short_id,
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
    parser.add_argument("--short", choices=tuple(SHORTS), help="Short to preflight or submit")
    args = parser.parse_args()
    if args.command == "check":
        checked, aggregate = check_inputs()
        print(json.dumps({
            "status": "locked_inputs_pass_no_authority_checked",
            "shorts": {key: {"script_sha256": SHORTS[key]["script_sha256"],
                             "request_sha256": SHORTS[key]["request_sha256"],
                             "operational_forecast_usd": value[2]} for key, value in checked.items()},
            "short02_04_aggregate_forecast_usd": aggregate,
            "aggregate_forecast_cap_usd": MAX_AGGREGATE_FORECAST_USD,
            "provider_calls": 0,
        }))
        return
    if args.short is None:
        parser.error("--short is required for preflight or submit")
    if args.command == "preflight":
        _, _, forecast, aggregate, source, event, _, _ = preflight(args.short)
        print(json.dumps({
            "status": "exact_fresh_authority_and_inputs_pass_no_provider_call",
            "short_id": args.short,
            "owner_source": rel(source),
            "owner_event": rel(event),
            "operational_forecast_usd": forecast,
            "short02_04_aggregate_forecast_usd": aggregate,
            "provider_calls": 0,
        }))
    else:
        submit(args.short)


if __name__ == "__main__":
    main()
