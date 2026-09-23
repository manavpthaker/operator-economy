#!/usr/bin/env python3
"""One authorized replacement Google guide for EP007 Short 02; never retry.

`check` is local-only. `submit` writes an exclusive intent before one POST and
preserves even a failed/uncertain provider response. It cannot promote a guide.
"""
from __future__ import annotations

import argparse
import base64
import datetime as dt
import hashlib
import importlib.util
import json
import sys
from pathlib import Path


sys.dont_write_bytecode = True
SELF = Path(__file__).resolve()
REPO = next(p for p in SELF.parents if p.name == "operator-economy")
SHORT_ID = "short-02-operations-business"
WORK = SELF.parent / SHORT_ID
V5 = SELF.parent.parent / "narration-v5" / SHORT_ID
OLD_RUNNER = SELF.parent.parent / "narration-v5/capture_short02_guide.py"
OWNER = REPO / "blueprint-cinema/episodes/EP007-exit-readiness-prep/review/decisions/ep007-owner-approve-two-bounded-recovery-calls-20260923.json"
SCRIPT = REPO / "studio/originate/exit-readiness-prep/shorts-net-new/narration-v3/short-02-operations-business/SCRIPT.txt"
REQUEST = REPO / "studio/originate/exit-readiness-prep/shorts-net-new/narration-v3/short-02-operations-business/GOOGLE-REQUEST.json"
OLD_QC = V5 / "GUIDE-QC-V1.json"
OLD_RECEIPT = V5 / "GOOGLE-RECEIPT.json"
SCRIPT_SHA = "aee361d4542ed450365a50c70577f6b1bddd61c30de0571d770cbd91b0ed5542"
REQUEST_SHA = "51d3d17749feaab1f9c9ccb1ddafe3dce81c90b92a17f23892c34a867a97c36e"
OWNER_SHA = "8aa69611a23acdfa7c76b5a5fbb0f89c688ab29dcc40fc19d1a9d7bbb3c7a64e"
OLD_QC_SHA = "d269e77082239c0cbc628ec1d876a033d7467b385ecd2defd3d7efa1f6b844dc"
OLD_RECEIPT_SHA = "968e53dc057931cbc3f0f0b059c66a1b6e55141558471c9bddd665006e1bf04a"
CAP_USD = 0.05

spec = importlib.util.spec_from_file_location("ep007_short02_prior_runner", OLD_RUNNER)
if spec is None or spec.loader is None:
    raise SystemExit("Prior pinned guide runner unavailable")
old = importlib.util.module_from_spec(spec)
spec.loader.exec_module(old)
engine, cal = old.engine, old.cal


def now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path: Path) -> str:
    return str(path.relative_to(REPO))


def verify() -> tuple[dict, bytes, float]:
    pins = {OWNER: OWNER_SHA, SCRIPT: SCRIPT_SHA, REQUEST: REQUEST_SHA,
            OLD_QC: OLD_QC_SHA, OLD_RECEIPT: OLD_RECEIPT_SHA}
    for path, expected in pins.items():
        if not path.is_file() or sha(path) != expected:
            raise SystemExit(f"Pinned evidence changed or missing: {rel(path)}")
    source = json.loads(OWNER.read_text())
    if (source.get("owner_verbatim") != "approved" or
            source.get("authorized", {}).get("short02_replacement_google_guide_calls_max") != 1 or
            source.get("authorized", {}).get("short02_google_guide_forecast_usd_max") != CAP_USD or
            "additional paid retries" not in source.get("not_authorized", [])):
        raise SystemExit("Exact bounded replacement approval changed")
    if json.loads(OLD_QC.read_text()).get("status") != "hold_exact_copy_failure_at_opening":
        raise SystemExit("Prior guide is not the expected preserved exact-copy hold")
    old_receipt = json.loads(OLD_RECEIPT.read_text())
    if old_receipt.get("http_status") != 200 or old_receipt.get("guide_sha256") != "dd7d5de978d1bc0357c033befc73011ec5e09a58a2148426df2f65a96d1e3a23":
        raise SystemExit("Prior guide receipt changed")
    request, body, forecast = old.check_inputs()
    if request != json.loads(REQUEST.read_text()) or sha(SCRIPT) != SCRIPT_SHA:
        raise SystemExit("Locked request/script changed")
    if forecast > CAP_USD:
        raise SystemExit("Forecast exceeds approved ceiling")
    for name in ("GOOGLE-SUBMISSION-INTENT.json", "GOOGLE-RECEIPT.json", "HOLD.json"):
        if (WORK / name).exists():
            raise SystemExit(f"Replacement attempt already exists: {name}; no retry")
    if WORK.exists() and any(WORK.iterdir()):
        raise SystemExit("Replacement work directory is nonempty; inspect before call")
    return request, body, forecast


def hold(status: str, reason: str) -> None:
    path = WORK / "HOLD.json"
    if not path.exists():
        engine.save_json_x(path, {
            "record_type": "ep007_short02_replacement_google_hold_v6", "at_utc": now(),
            "status": status, "reason": reason, "attempts": 1, "retries": 0,
            "policy": "preserve_and_stop; no transfer from an uncertain or failed guide",
        })


def submit() -> None:
    request, body, forecast = verify()
    token, project = cal.google_access_token(), cal.google_quota_project()
    if not token or not project:
        raise SystemExit("Google credential or quota project unavailable; zero POSTs")
    # Recheck after credential preflight; the output directory remains empty.
    verify()
    WORK.mkdir(parents=True, exist_ok=True)
    (WORK / "media").mkdir(exist_ok=True)
    intent = WORK / "GOOGLE-SUBMISSION-INTENT.json"
    engine.save_json_x(intent, {
        "record_type": "ep007_short02_replacement_google_intent_v6", "at_utc": now(),
        "short_id": SHORT_ID, "runner_path": rel(SELF), "runner_sha256": sha(SELF),
        "owner_source_path": rel(OWNER), "owner_source_sha256": OWNER_SHA,
        "prior_failed_guide_qc_path": rel(OLD_QC), "prior_failed_guide_qc_sha256": OLD_QC_SHA,
        "prior_google_receipt_path": rel(OLD_RECEIPT), "prior_google_receipt_sha256": OLD_RECEIPT_SHA,
        "script_path": rel(SCRIPT), "script_sha256": SCRIPT_SHA,
        "request_path": rel(REQUEST), "request_sha256": REQUEST_SHA,
        "request_body_sha256": hashlib.sha256(body).hexdigest(),
        "provider_generation_attempt": 2, "new_calls_under_this_approval": 1,
        "automatic_retries": 0, "forecast_usd": forecast, "forecast_cap_usd": CAP_USD,
        "provider_enforced_billing_cap": False,
        "uncertain_outcome_policy": "preserve_and_stop_no_retry",
    })
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json; charset=utf-8", "x-goog-user-project": project}
    try:
        status, raw, response_headers = engine.safe_request(cal.GUIDE_ENDPOINT, method="POST", headers=headers, body=body)
    except Exception as exc:
        hold("transport_outcome_uncertain", type(exc).__name__)
        raise SystemExit("Google submission outcome uncertain; no retry")
    raw_path = WORK / "media/google-response.bin"
    engine.save_bytes_x(raw_path, raw)
    receipt = {
        "record_type": "ep007_short02_replacement_google_receipt_v6", "at_utc": now(),
        "short_id": SHORT_ID, "http_status": status, "response_headers": response_headers,
        "intent_path": rel(intent), "intent_sha256": sha(intent),
        "raw_response_path": rel(raw_path), "raw_response_sha256": sha(raw_path),
        "calls_under_this_approval": 1, "retries": 0,
        "provider_enforced_billing_cap": False,
        "accepted_for_transfer": False,
    }
    if status != 200:
        receipt["status"] = "http_failure_no_retry"
        engine.save_json_x(WORK / "GOOGLE-RECEIPT.json", receipt)
        hold("http_failure", f"HTTP {status}")
        raise SystemExit(f"Google HTTP {status}; no retry")
    try:
        payload = json.loads(raw)
        audio = base64.b64decode(payload["audioContent"], validate=True)
        if not audio:
            raise ValueError("empty audio")
        guide = WORK / "media/guide.wav"
        engine.save_bytes_x(guide, audio)
        probe = cal.probe(guide)
    except Exception as exc:
        receipt["status"] = "decode_or_probe_failure_no_retry"
        engine.save_json_x(WORK / "GOOGLE-RECEIPT.json", receipt)
        hold("decode_or_probe_failure", type(exc).__name__)
        raise SystemExit("Google guide decode/probe failed; no retry")
    estimate = engine.google_cost(request, float(probe["duration_seconds"]))
    format_pass = (probe.get("sample_rate_hz"), probe.get("channels"), probe.get("sample_width_bits")) == (24000, 1, 16)
    tail_pass = probe.get("ends_in_silence") is True
    cap_pass = estimate <= CAP_USD
    receipt.update({
        "guide_path": rel(guide), "guide_sha256": sha(guide), "guide_probe": probe,
        "estimated_cost_usd_conservative_input_tokens": estimate,
        "cost_is_invoice": False, "format_pass": format_pass,
        "tail_energy_less_than_0_02": tail_pass, "operational_cap_pass": cap_pass,
        "exact_copy_asr": "not_run", "owner_listening": "pending",
        "status": "pending_exact_copy_asr" if (format_pass and tail_pass and cap_pass) else "technical_qc_hold_no_retry",
    })
    engine.save_json_x(WORK / "GOOGLE-RECEIPT.json", receipt)
    if not (format_pass and tail_pass and cap_pass):
        hold("technical_qc_hold", "format, tail or cost estimate outside gate")
        raise SystemExit("Replacement guide technical QC hold; no retry")
    print(json.dumps({"status": "pending_exact_copy_asr", "guide_sha256": sha(guide),
                      "duration_seconds": probe["duration_seconds"], "estimated_usd_not_invoice": estimate,
                      "calls": 1, "retries": 0}))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("check", "submit"))
    args = parser.parse_args()
    if args.command == "check":
        _, _, forecast = verify()
        print(json.dumps({"status": "pass_local_only", "forecast_usd": forecast, "cap_usd": CAP_USD,
                          "provider_calls": 0}))
    else:
        submit()
