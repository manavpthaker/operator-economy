#!/usr/bin/env python3
"""Governed one-shot narration capture for the four locked EP007 Shorts.

Every provider submission is preceded by an immutable intent. Provider calls
are never retried. Google guides must all pass local exact-copy ASR and fit the
aggregate ElevenLabs credit cap before any voice-transfer call is allowed.
"""
from __future__ import annotations

import argparse
import base64
import datetime as dt
import hashlib
import json
import math
import os
import re
import subprocess
import sys
import unicodedata
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


sys.dont_write_bytecode = True
SOURCE_DIR = Path(__file__).resolve().parent
BASE = SOURCE_DIR.parent / "narration-v2"
REPO = next(path for path in (SOURCE_DIR, *SOURCE_DIR.parents) if path.name == "operator-economy")
TOOLS = REPO / "operator-blueprint-v2/02-narration-production/tools"
sys.path.insert(0, str(TOOLS))
import calibrate as cal  # noqa: E402


SCRIPT_AUTHORITY = REPO / "studio/originate/exit-readiness-prep/shorts-net-new/STANDALONE-SCRIPTS-V3.json"
PROPOSAL = REPO / "studio/originate/exit-readiness-prep/shorts-net-new/NARRATION-CAPTURE-PROPOSAL-V1.json"
PRODUCTION_MANIFEST = REPO / "studio/originate/exit-readiness-prep/shorts-net-new/PRODUCTION-MANIFEST-V2.json"
AUTHORIZATION = REPO / "blueprint-cinema/episodes/EP007-exit-readiness-prep/review/decisions/ep007-owner-authorize-shorts-narration-20260922.json"
STYLE_SOURCE = REPO / "operator-blueprint-v2/02-narration-production/prompts/NARRATOR-REGISTER.candidate-C4.google-gemini-tts.style-instructions.json"
CALIBRATE_SOURCE = REPO / "operator-blueprint-v2/02-narration-production/tools/calibrate.py"
CAPTURE_SOURCE = REPO / "operator-blueprint-v2/02-narration-production/tools/capture_n4b.py"

PINS = {
    SCRIPT_AUTHORITY: "6be1ee7c13ba6fc607d215e9a61c74fda31cc3f60026632eff6fc029f903cf6c",
    PROPOSAL: "c8404afd3b31153558a83c66e6f32a0d6a44a60570f237b8584bddddeb44e100",
    PRODUCTION_MANIFEST: "cc925469a415e7d0405a21c6874d63586635d5fbb1c4ac5b2d7f82ab0fd0d4ad",
    AUTHORIZATION: "93f402d0ce7594af5205727731b846b37962015cd5943e0048ef12ae121d0751",
    STYLE_SOURCE: "b747d7b0afa4469b2be05c20eb16306a25bb5185b9fa8b12e2d4aa4ddd8d3efc",
    CALIBRATE_SOURCE: "d59303278dbb79bef6fe0080f1d2b6c1e701e9228e95c7b3cdea4f3eec78cc00",
    CAPTURE_SOURCE: "5e1093bc0f0113fa998bd5e99359f90b098342cc83c19997ed77ab0f02a15493",
}

GUIDE_VOICE = "Algieba"
GUIDE_CALL_CAP = 4
TRANSFER_CALL_CAP = 4
TOTAL_CALL_CAP = 8
GOOGLE_SPEND_CAP_USD = 0.15
ELEVEN_CREDIT_CAP = 3200
ELEVEN_CREDITS_PER_MINUTE = 1000
ELEVEN_SUBSCRIPTION_URL = "https://api.elevenlabs.io/v1/user/subscription"
ELEVEN_VOICE_URL = f"https://api.elevenlabs.io/v1/voices/{cal.TRANSFER_VOICE_ID}"
ALLOWED_HOSTS = {"us-texttospeech.googleapis.com", "api.elevenlabs.io"}
SAFE_RESPONSE_HEADERS = {
    "content-type",
    "content-length",
    "date",
    "request-id",
    "x-request-id",
    "x-elevenlabs-request-id",
    "character-cost",
    "x-character-cost",
}


def now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha_file(path: Path) -> str:
    return sha_bytes(path.read_bytes())


def rel(path: Path) -> str:
    return str(path.relative_to(REPO))


def save_json_x(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as handle:
        json.dump(value, handle, indent=2, ensure_ascii=False)
        handle.write("\n")


def save_text_x(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as handle:
        handle.write(value)


def save_bytes_x(path: Path, value: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as handle:
        handle.write(value)
    path.chmod(0o600)


def assert_pins() -> None:
    for path, expected in PINS.items():
        actual = sha_file(path)
        if actual != expected:
            raise SystemExit(f"Pinned input changed: {rel(path)} expected {expected}, got {actual}")
    auth = json.loads(AUTHORIZATION.read_text(encoding="utf-8"))
    exact = {
        "locked_script_count": 4,
        "google_guide_calls_max": 4,
        "elevenlabs_transfer_calls_max": 4,
        "provider_calls_max": 8,
        "automatic_retries": 0,
        "google_spend_cap_usd": 0.15,
        "elevenlabs_credit_cap": 3200,
        "guide_model": "gemini-2.5-pro-tts",
        "guide_voice": "Algieba",
        "transfer_model": "eleven_multilingual_sts_v2",
        "transfer_voice": "Original C",
        "transfer_voice_id": "scMbPZwQjr40V1MzL3Nj",
    }
    for key, expected in exact.items():
        if auth["authorized"].get(key) != expected:
            raise SystemExit(f"Authorization mismatch for {key}")
    if auth.get("owner_verbatim") != "Approved":
        raise SystemExit("Owner authorization source does not contain exact approval")


def scripts() -> list[dict[str, Any]]:
    data = json.loads(SCRIPT_AUTHORITY.read_text(encoding="utf-8"))
    rows = sorted(data["scripts"], key=lambda item: item["production_order"])
    expected = [
        "short-01-thirty-day-map",
        "short-02-operations-business",
        "short-03-how-you-charge",
        "short-04-test-the-front-door",
    ]
    if [row["id"] for row in rows] != expected:
        raise SystemExit("Locked Short IDs or order changed")
    return rows


def short(short_id: str) -> dict[str, Any]:
    return next((row for row in scripts() if row["id"] == short_id), None) or sys.exit(f"Unknown Short: {short_id}")


def short_dir(short_id: str) -> Path:
    return BASE / short_id


def safe_headers(headers: Any) -> dict[str, str]:
    return {key.lower(): value for key, value in headers.items() if key.lower() in SAFE_RESPONSE_HEADERS}


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args: Any, **kwargs: Any) -> None:
        return None


def safe_request(
    url: str,
    *,
    method: str = "GET",
    headers: dict[str, str] | None = None,
    body: bytes | None = None,
) -> tuple[int, bytes, dict[str, str]]:
    from urllib.parse import urlparse

    parsed = urlparse(url)
    if parsed.scheme != "https" or parsed.hostname not in ALLOWED_HOSTS:
        raise RuntimeError(f"Provider URL outside allowlist: {url}")
    request = urllib.request.Request(url, data=body, headers=headers or {}, method=method)
    try:
        with urllib.request.build_opener(NoRedirect).open(request, timeout=600) as response:
            payload = response.read()
            return response.status, payload, safe_headers(response.headers)
    except urllib.error.HTTPError as exc:
        payload = exc.read()
        return exc.code, payload, safe_headers(exc.headers)


def redact_error(payload: bytes, secrets: list[str]) -> str:
    text = payload.decode("utf-8", "replace")[:4000]
    for secret in secrets:
        if secret:
            text = text.replace(secret, "[REDACTED]")
    return text


def filtered_account(payload: bytes) -> dict[str, Any]:
    data = json.loads(payload)
    selected = {
        key: data.get(key)
        for key in (
            "tier",
            "status",
            "character_count",
            "character_limit",
            "can_extend_character_limit",
            "next_character_count_reset_unix",
        )
    }
    count = selected.get("character_count")
    limit = selected.get("character_limit")
    if not isinstance(count, (int, float)) or not isinstance(limit, (int, float)):
        raise RuntimeError("ElevenLabs account response lacks numeric character_count/character_limit")
    selected["remaining_included_credits"] = int(limit - count)
    return selected


def filtered_voice(payload: bytes) -> dict[str, Any]:
    data = json.loads(payload)
    sharing = data.get("sharing")
    if isinstance(sharing, dict):
        sharing = {
            key: sharing.get(key)
            for key in ("status", "rate", "financial_rewards_enabled", "is_rate_allowed", "enabled_in_library", "original_voice_id")
        }
    return {
        key: value
        for key, value in {
            "voice_id": data.get("voice_id"),
            "name": data.get("name"),
            "category": data.get("category"),
            "sharing": sharing,
            "credit_cost_multiplier": data.get("credit_cost_multiplier"),
            "rate_multiplier": data.get("rate_multiplier"),
        }.items()
    }


def read_account_and_voice() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    key = cal.read_dotenv_key("ELEVENLABS_API_KEY")
    account_status, account_raw, account_headers = safe_request(
        ELEVEN_SUBSCRIPTION_URL, headers={"xi-api-key": key}
    )
    if account_status != 200:
        raise RuntimeError(f"ElevenLabs subscription read HTTP {account_status}: {redact_error(account_raw, [key])}")
    voice_status, voice_raw, voice_headers = safe_request(ELEVEN_VOICE_URL, headers={"xi-api-key": key})
    if voice_status != 200:
        raise RuntimeError(f"ElevenLabs voice read HTTP {voice_status}: {redact_error(voice_raw, [key])}")
    account = filtered_account(account_raw)
    voice = filtered_voice(voice_raw)
    if voice.get("voice_id") != cal.TRANSFER_VOICE_ID:
        raise RuntimeError("Live ElevenLabs voice ID mismatch")
    if voice.get("category") != "generated" or voice.get("sharing") not in (None, {}):
        raise RuntimeError("Original C is no longer an unshared generated voice; standard-rate assumption is invalid")
    for field in ("credit_cost_multiplier", "rate_multiplier"):
        value = voice.get(field)
        if value not in (None, 1, 1.0):
            raise RuntimeError(f"Unexpected ElevenLabs {field}: {value}")
    status = account.get("status")
    if status is not None and status not in ("active", "trialing"):
        raise RuntimeError(f"ElevenLabs account status is {status!r}, not active")
    headers = {"account": account_headers, "voice": voice_headers}
    return account, voice, headers


def lexical_count(text: str) -> int:
    # Proposal convention: hyphenated compounds are one lexical word, while
    # ampersand forms such as M&A contribute the two visible letter tokens.
    return len(re.findall(r"[A-Za-z0-9]+(?:[-’'][A-Za-z0-9]+)*", text))


def transfer_fields() -> dict[str, str]:
    return {
        "model_id": cal.TRANSFER_MODEL,
        "remove_background_noise": "false",
        "seed": str(cal.TRANSFER_SEED),
        "voice_settings": json.dumps(cal.TRANSFER_VOICE_SETTINGS, sort_keys=True),
        "file_format": "other",
    }


def prepare() -> None:
    assert_pins()
    BASE.mkdir(parents=True, exist_ok=True)
    if (BASE / "RUN-INPUT.json").exists():
        raise SystemExit("RUN-INPUT.json already exists; preparation is immutable")
    style_base, style_label, aliases = cal.load_style(STYLE_SOURCE)
    rows = scripts()
    if sum(lexical_count(row["spoken_copy"]) for row in rows) != 423:
        raise SystemExit("Locked lexical word total no longer equals approved 423")
    run = {
        "record_type": "ep007_shorts_narration_run_input",
        "prepared_at_utc": now(),
        "status": "prepared_not_submitted",
        "script_count": 4,
        "pins": [{"path": rel(path), "sha256": expected} for path, expected in PINS.items()],
        "capture_runner": {"path": rel(Path(__file__)), "sha256": sha_file(Path(__file__))},
        "approved_caps": {
            "google_guide_calls": GUIDE_CALL_CAP,
            "elevenlabs_transfer_calls": TRANSFER_CALL_CAP,
            "provider_generation_calls": TOTAL_CALL_CAP,
            "automatic_retries": 0,
            "google_spend_usd": GOOGLE_SPEND_CAP_USD,
            "elevenlabs_credits": ELEVEN_CREDIT_CAP,
        },
        "guide": {"model": cal.GUIDE_MODEL, "voice": GUIDE_VOICE, "language": cal.GUIDE_LANGUAGE},
        "transfer": {
            "model": cal.TRANSFER_MODEL,
            "target_voice": "Original C",
            "target_voice_id": cal.TRANSFER_VOICE_ID,
            "output_format": cal.TRANSFER_OUTPUT_FORMAT,
            "seed": cal.TRANSFER_SEED,
            "voice_settings": cal.TRANSFER_VOICE_SETTINGS,
            "remove_background_noise": False,
        },
        "artifact_bindings": [],
        "google_cost_control": {
            "type": "forecast_before_each_call_and_measured_estimate_after_each_call",
            "caveat": "Google exposes no request-side output-cost limiter and the estimate is not an invoice; a literal provider-side hard stop cannot be proven.",
            "authorized_estimated_aggregate_cap_usd": GOOGLE_SPEND_CAP_USD,
        },
        "failure_policy": "stop after any failure or uncertain provider outcome; never retry under this authorization",
    }
    for row in rows:
        work = short_dir(row["id"])
        work.mkdir(exist_ok=False)
        (work / "media").mkdir()
        text = row["spoken_copy"]
        style = cal.compose_style(style_base, aliases, text)
        request = cal.guide_body(text, style, GUIDE_VOICE)
        request_body = cal.compact_json(request)
        if len(text.encode("utf-8")) > 4000 or len(style.encode("utf-8")) > 4000:
            raise SystemExit(f"Google prompt or text limit exceeded for {row['id']}")
        save_text_x(work / "SCRIPT.txt", text)
        save_json_x(
            work / "STYLE.json",
            {
                "source_path": rel(STYLE_SOURCE),
                "source_sha256": PINS[STYLE_SOURCE],
                "style_label": style_label,
                "style_instructions": style,
                "style_instructions_sha256": sha_bytes(style.encode("utf-8")),
            },
        )
        save_json_x(work / "GOOGLE-REQUEST.json", request)
        save_json_x(work / "TRANSFER-INPUT.json", {
            "endpoint": cal.TRANSFER_ENDPOINT,
            "target_voice_id": cal.TRANSFER_VOICE_ID,
            "output_format": cal.TRANSFER_OUTPUT_FORMAT,
            "fields": transfer_fields(),
        })
        save_json_x(
            work / "VOICE-INPUT.json",
            {
                "id": row["id"],
                "title": row["title"],
                "script_path": rel(work / "SCRIPT.txt"),
                "script_sha256": sha_bytes(text.encode("utf-8")),
                "whitespace_word_count": len(text.split()),
                "lexical_word_count": lexical_count(text),
                "character_count": len(text),
                "google_request_body_sha256": sha_bytes(request_body),
                "maximum_provider_attempts_per_stage": 1,
                "automatic_retries": 0,
            },
        )
        run["artifact_bindings"].append({
            "short_id": row["id"],
            "files": [
                {"path": rel(work / name), "sha256": sha_file(work / name)}
                for name in ("SCRIPT.txt", "STYLE.json", "GOOGLE-REQUEST.json", "TRANSFER-INPUT.json", "VOICE-INPUT.json")
            ],
        })
    save_json_x(BASE / "RUN-INPUT.json", run)
    print(json.dumps({"status": "prepared", "shorts": [row["id"] for row in rows], "generation_calls": 0}))


def require_prepared() -> dict[str, Any]:
    assert_pins()
    record = json.loads((BASE / "RUN-INPUT.json").read_text(encoding="utf-8"))
    if record["capture_runner"]["sha256"] != sha_file(Path(__file__)):
        raise SystemExit("Capture runner changed after preparation")
    for row in scripts():
        validate_short_inputs(row["id"], record)
    return record


def validate_short_inputs(short_id: str, run: dict[str, Any]) -> None:
    row = short(short_id)
    work = short_dir(short_id)
    names = ("SCRIPT.txt", "STYLE.json", "GOOGLE-REQUEST.json", "TRANSFER-INPUT.json", "VOICE-INPUT.json")
    binding = next((item for item in run.get("artifact_bindings", []) if item.get("short_id") == short_id), None)
    if not binding:
        raise SystemExit(f"Missing immutable artifact binding for {short_id}")
    expected_bindings = {item["path"]: item["sha256"] for item in binding.get("files", [])}
    for name in names:
        path = work / name
        if expected_bindings.get(rel(path)) != sha_file(path):
            raise SystemExit(f"Prepared artifact binding failed: {rel(path)}")
    text = (work / "SCRIPT.txt").read_text(encoding="utf-8")
    if text != row["spoken_copy"]:
        raise SystemExit(f"Prepared script no longer equals locked spoken copy: {short_id}")
    style_base, _, aliases = cal.load_style(STYLE_SOURCE)
    expected_style = cal.compose_style(style_base, aliases, text)
    style = json.loads((work / "STYLE.json").read_text(encoding="utf-8"))
    if style.get("style_instructions") != expected_style or style.get("style_instructions_sha256") != sha_bytes(expected_style.encode("utf-8")):
        raise SystemExit(f"Prepared style no longer equals pinned composed style: {short_id}")
    request = json.loads((work / "GOOGLE-REQUEST.json").read_text(encoding="utf-8"))
    expected_request = cal.guide_body(text, expected_style, GUIDE_VOICE)
    if request != expected_request:
        raise SystemExit(f"Prepared Google request no longer equals locked text/style/configuration: {short_id}")
    voice_input = json.loads((work / "VOICE-INPUT.json").read_text(encoding="utf-8"))
    if voice_input.get("id") != short_id or voice_input.get("script_sha256") != sha_file(work / "SCRIPT.txt"):
        raise SystemExit(f"Prepared voice input script binding failed: {short_id}")
    if voice_input.get("google_request_body_sha256") != sha_bytes(cal.compact_json(request)):
        raise SystemExit(f"Prepared voice input request binding failed: {short_id}")
    expected_transfer = {
        "endpoint": cal.TRANSFER_ENDPOINT,
        "target_voice_id": cal.TRANSFER_VOICE_ID,
        "output_format": cal.TRANSFER_OUTPUT_FORMAT,
        "fields": transfer_fields(),
    }
    if json.loads((work / "TRANSFER-INPUT.json").read_text(encoding="utf-8")) != expected_transfer:
        raise SystemExit(f"Prepared transfer request no longer equals approved configuration: {short_id}")


def assert_batch_clear() -> None:
    """Global fail-closed latch checked before every provider submission."""
    for row in scripts():
        work = short_dir(row["id"])
        for error_name in ("GOOGLE-ERROR.json", "ELEVEN-ERROR.json"):
            if (work / error_name).exists():
                raise SystemExit(f"Batch stopped by existing {rel(work / error_name)}")
        guide_receipt = work / "GOOGLE-RECEIPT.json"
        if guide_receipt.exists():
            data = json.loads(guide_receipt.read_text(encoding="utf-8"))
            if data.get("http_status") != 200 or not data.get("accepted"):
                raise SystemExit(f"Batch stopped by failed guide receipt for {row['id']}")
        transfer_receipt = work / "ELEVEN-RECEIPT.json"
        if transfer_receipt.exists():
            data = json.loads(transfer_receipt.read_text(encoding="utf-8"))
            if data.get("http_status") != 200 or not data.get("accepted_pending_exact_final_asr_and_owner_listen"):
                raise SystemExit(f"Batch stopped by failed transfer receipt for {row['id']}")
        for asr_name in ("GUIDE-ASR.json", "FINAL-ASR.json"):
            path = work / asr_name
            if path.exists() and not json.loads(path.read_text(encoding="utf-8")).get("accepted"):
                raise SystemExit(f"Batch stopped by failed exact-copy record {rel(path)}")
        for intent_name, receipt_name, error_name in (
            ("GOOGLE-SUBMISSION-INTENT.json", "GOOGLE-RECEIPT.json", "GOOGLE-ERROR.json"),
            ("ELEVEN-SUBMISSION-INTENT.json", "ELEVEN-RECEIPT.json", "ELEVEN-ERROR.json"),
        ):
            if (work / intent_name).exists() and not (work / receipt_name).exists() and not (work / error_name).exists():
                raise SystemExit(f"Batch stopped by unresolved submission intent {rel(work / intent_name)}")


def validate_asr_binding(short_id: str, stage: str, media: Path) -> dict[str, Any]:
    work = short_dir(short_id)
    prefix = "GUIDE" if stage == "guide" else "FINAL"
    provider_receipt_path = work / ("GOOGLE-RECEIPT.json" if stage == "guide" else "ELEVEN-RECEIPT.json")
    canonical_path = work / f"{prefix}-ASR.json"
    run_path = work / f"{stage.upper()}-ASR-RUN.json"
    intent_path = work / f"{stage.upper()}-ASR-INTENT.json"
    if not canonical_path.exists() or not run_path.exists() or not intent_path.exists() or not provider_receipt_path.exists() or not media.exists():
        raise SystemExit(f"Incomplete {stage} ASR evidence for {short_id}")
    canonical = json.loads(canonical_path.read_text(encoding="utf-8"))
    run_record = json.loads(run_path.read_text(encoding="utf-8"))
    intent = json.loads(intent_path.read_text(encoding="utf-8"))
    transcript_path = REPO / canonical.get("transcript_path", "")
    if not transcript_path.is_file():
        raise SystemExit(f"Missing {stage} transcript for {short_id}")
    media_sha = sha_file(media)
    if (
        not canonical.get("accepted")
        or canonical.get("media_sha256") != media_sha
        or canonical.get("script_sha256") != sha_file(work / "SCRIPT.txt")
        or canonical.get("asr_run_sha256") != sha_file(run_path)
        or canonical.get("transcript_sha256") != sha_file(transcript_path)
        or run_record.get("intent_sha256") != sha_file(intent_path)
        or run_record.get("source_media_sha256") != media_sha
        or run_record.get("transcript_sha256") != sha_file(transcript_path)
        or intent.get("source_media_sha256") != media_sha
        or intent.get("provider_receipt_sha256") != sha_file(provider_receipt_path)
        or intent.get("tool") != "hyperframes@0.8.59"
        or intent.get("engine") != "whisper"
        or intent.get("model") != "small.en"
    ):
        raise SystemExit(f"{stage} ASR evidence binding drifted for {short_id}")
    return canonical


def validate_guide_evidence(short_id: str) -> None:
    work = short_dir(short_id)
    media = work / "media/guide.wav"
    receipt_path = work / "GOOGLE-RECEIPT.json"
    if not receipt_path.exists() or not media.exists():
        raise SystemExit(f"Missing guide evidence for {short_id}")
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    if receipt.get("http_status") != 200 or not receipt.get("accepted") or receipt.get("guide", {}).get("sha256") != sha_file(media):
        raise SystemExit(f"Guide receipt/media binding failed for {short_id}")
    validate_asr_binding(short_id, "guide", media)


def validate_final_evidence(short_id: str) -> None:
    work = short_dir(short_id)
    media = work / "media/original-c.wav"
    guide = work / "media/guide.wav"
    receipt_path = work / "ELEVEN-RECEIPT.json"
    if not receipt_path.exists() or not media.exists() or not guide.exists():
        raise SystemExit(f"Missing final voice evidence for {short_id}")
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    if (
        receipt.get("http_status") != 200
        or not receipt.get("accepted_pending_exact_final_asr_and_owner_listen")
        or receipt.get("voice", {}).get("sha256") != sha_file(media)
        or receipt.get("guide_sha256") != sha_file(guide)
        or not receipt.get("actual_credit_cost_verified")
        or receipt.get("actual_credit_cost") != parse_actual_eleven_cost(receipt)
    ):
        raise SystemExit(f"Final receipt/media/credit binding failed for {short_id}")
    validate_asr_binding(short_id, "final", media)


def prior_rows(short_id: str) -> list[dict[str, Any]]:
    rows = scripts()
    index = next((i for i, row in enumerate(rows) if row["id"] == short_id), None)
    if index is None:
        raise SystemExit(f"Unknown Short: {short_id}")
    return rows[:index]


def assert_guide_order(short_id: str) -> None:
    for row in prior_rows(short_id):
        validate_guide_evidence(row["id"])


def assert_transfer_order(short_id: str) -> None:
    for row in prior_rows(short_id):
        validate_final_evidence(row["id"])


def preflight() -> None:
    require_prepared()
    path = BASE / "PROVIDER-PREFLIGHT.json"
    if path.exists():
        raise SystemExit("Provider preflight already recorded")
    token = cal.google_access_token()
    project = cal.google_quota_project()
    if not token or not project:
        raise SystemExit("Google ADC token or quota project unavailable")
    account, voice, headers = read_account_and_voice()
    if account["remaining_included_credits"] < ELEVEN_CREDIT_CAP:
        raise SystemExit("ElevenLabs has fewer than 3,200 included credits available")
    save_json_x(
        path,
        {
            "at_utc": now(),
            "status": "pass",
            "google": {"adc_token_minted": True, "quota_project_configured": True},
            "elevenlabs": {"account": account, "voice": voice, "response_headers": headers},
            "required_remaining_credits": ELEVEN_CREDIT_CAP,
            "generation_calls_made": 0,
        },
    )
    print(json.dumps({"status": "pass", "eleven_remaining": account["remaining_included_credits"], "voice": voice["name"]}))


def count_intents(name: str) -> int:
    return sum(1 for row in scripts() if (short_dir(row["id"]) / name).exists())


def parse_actual_eleven_cost(receipt: dict[str, Any]) -> int:
    headers = receipt.get("response_headers") or {}
    raw = headers.get("character-cost") or headers.get("x-character-cost")
    if raw is None or not re.fullmatch(r"\d+(?:\.\d+)?", str(raw).strip()):
        raise ValueError("ElevenLabs response did not provide a numeric character-cost header")
    return math.ceil(float(raw))


def prior_actual_eleven_cost(short_id: str) -> int:
    total = 0
    for row in prior_rows(short_id):
        path = short_dir(row["id"]) / "ELEVEN-RECEIPT.json"
        if not path.exists():
            raise SystemExit(f"Missing prior transfer receipt for {row['id']}")
        try:
            total += parse_actual_eleven_cost(json.loads(path.read_text(encoding="utf-8")))
        except ValueError as exc:
            raise SystemExit(str(exc)) from exc
    return total


def google_cost(request: dict[str, Any], duration_seconds: float) -> float:
    chars = len(request["input"]["prompt"]) + len(request["input"]["text"])
    return duration_seconds * 25 * 20 / 1_000_000 + chars / 1_000_000


def current_google_cost() -> float:
    total = 0.0
    for row in scripts():
        receipt = short_dir(row["id"]) / "GOOGLE-RECEIPT.json"
        if receipt.exists():
            total += float(json.loads(receipt.read_text(encoding="utf-8")).get("estimated_cost_usd_conservative_input_tokens", 0))
    return total


def generate_guide(short_id: str) -> None:
    run = require_prepared()
    assert_batch_clear()
    assert_guide_order(short_id)
    validate_short_inputs(short_id, run)
    if not (BASE / "PROVIDER-PREFLIGHT.json").exists():
        raise SystemExit("Run provider preflight first")
    work = short_dir(short_id)
    intent = work / "GOOGLE-SUBMISSION-INTENT.json"
    if intent.exists():
        raise SystemExit(f"Google intent already exists for {short_id}; no retry authorized")
    if count_intents("GOOGLE-SUBMISSION-INTENT.json") >= GUIDE_CALL_CAP:
        raise SystemExit("Google call cap already reached")
    if count_intents("GOOGLE-SUBMISSION-INTENT.json") + count_intents("ELEVEN-SUBMISSION-INTENT.json") >= TOTAL_CALL_CAP:
        raise SystemExit("Total provider generation call cap already reached")
    request = json.loads((work / "GOOGLE-REQUEST.json").read_text(encoding="utf-8"))
    body = cal.compact_json(request)
    if request["voice"] != {"languageCode": "en-US", "modelName": "gemini-2.5-pro-tts", "name": GUIDE_VOICE}:
        raise SystemExit("Google voice request changed")
    forecast = len(request["input"]["text"]) / cal.CHARS_PER_SECOND
    forecast_cost = google_cost(request, forecast)
    if current_google_cost() + forecast_cost > GOOGLE_SPEND_CAP_USD:
        raise SystemExit("Expected next Google guide would exceed the approved spend cap")
    save_json_x(
        intent,
        {
            "at_utc": now(),
            "stage": "google_guide",
            "short_id": short_id,
            "request_path": rel(work / "GOOGLE-REQUEST.json"),
            "request_body_sha256": sha_bytes(body),
            "script_sha256": sha_file(work / "SCRIPT.txt"),
            "provider_generation_attempt": 1,
            "automatic_retries": 0,
            "aggregate_google_calls_after_submission": count_intents("GOOGLE-SUBMISSION-INTENT.json") + 1,
            "spend_cap_usd": GOOGLE_SPEND_CAP_USD,
            "submission_outcome_policy": "uncertain or failed outcome stops the batch and cannot be retried",
        },
    )
    token = cal.google_access_token()
    project = cal.google_quota_project()
    if not project:
        raise SystemExit("Google quota project unavailable after intent; outcome not submitted and no retry without inspection")
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json; charset=utf-8",
        "x-goog-user-project": project,
    }
    try:
        status, raw, response_headers = safe_request(
            cal.GUIDE_ENDPOINT, method="POST", headers=headers, body=body
        )
    except Exception as exc:
        save_json_x(work / "GOOGLE-ERROR.json", {
            "at_utc": now(),
            "error_class": type(exc).__name__,
            "submission_outcome": "uncertain_no_retry",
        })
        raise SystemExit(f"Google transport outcome uncertain for {short_id}; no retry")
    save_bytes_x(work / "media/google-response.bin", raw)
    receipt: dict[str, Any] = {
        "at_utc": now(),
        "http_status": status,
        "response_headers": response_headers,
        "raw_response_path": rel(work / "media/google-response.bin"),
        "raw_response_sha256": sha_bytes(raw),
        "calls": 1,
        "retries": 0,
    }
    if status != 200:
        receipt["error"] = redact_error(raw, [token])
        receipt["accepted"] = False
        save_json_x(work / "GOOGLE-RECEIPT.json", receipt)
        raise SystemExit(f"Google HTTP {status} for {short_id}; no retry")
    try:
        parsed = json.loads(raw)
        audio = base64.b64decode(parsed["audioContent"], validate=True)
    except Exception as exc:
        receipt["decode_error"] = type(exc).__name__
        receipt["accepted"] = False
        save_json_x(work / "GOOGLE-RECEIPT.json", receipt)
        raise SystemExit(f"Google response decode failed for {short_id}; no retry")
    guide = work / "media/guide.wav"
    save_bytes_x(guide, audio)
    probe = cal.probe(guide)
    cost = google_cost(request, float(probe["duration_seconds"]))
    receipt |= {
        "guide": probe | {"path": rel(guide)},
        "estimated_cost_usd_conservative_input_tokens": cost,
        "cost_is_invoice": False,
        "technical_tail_pass": bool(probe.get("ends_in_silence")),
        "accepted": bool(probe.get("ends_in_silence")),
    }
    save_json_x(work / "GOOGLE-RECEIPT.json", receipt)
    if current_google_cost() > GOOGLE_SPEND_CAP_USD:
        raise SystemExit("Measured Google aggregate exceeded cap; batch stopped")
    if not receipt["accepted"]:
        raise SystemExit(f"Guide tail did not decay for {short_id}; no retry")
    print(json.dumps({"short_id": short_id, "duration_seconds": probe["duration_seconds"], "tail_energy": probe.get("tail_energy"), "estimated_usd": cost}))


def guide_summary() -> None:
    require_prepared()
    assert_batch_clear()
    output = BASE / "GUIDE-BATCH-SUMMARY.json"
    if output.exists():
        raise SystemExit("Guide summary already exists")
    rows: list[dict[str, Any]] = []
    for item in scripts():
        validate_guide_evidence(item["id"])
        path = short_dir(item["id"]) / "GOOGLE-RECEIPT.json"
        if not path.exists():
            raise SystemExit(f"Missing guide receipt for {item['id']}")
        receipt = json.loads(path.read_text(encoding="utf-8"))
        if receipt.get("http_status") != 200 or not receipt.get("accepted"):
            raise SystemExit(f"Guide not accepted for {item['id']}")
        asr_path = short_dir(item["id"]) / "GUIDE-ASR.json"
        if not asr_path.exists() or not json.loads(asr_path.read_text(encoding="utf-8")).get("accepted"):
            raise SystemExit(f"Guide exact-copy ASR not accepted for {item['id']}")
        rows.append({
            "short_id": item["id"],
            "duration_seconds": receipt["guide"]["duration_seconds"],
            "sha256": receipt["guide"]["sha256"],
            "tail_energy": receipt["guide"].get("tail_energy"),
            "estimated_cost_usd": receipt["estimated_cost_usd_conservative_input_tokens"],
            "guide_receipt_sha256": sha_file(path),
            "guide_asr_sha256": sha_file(asr_path),
            "script_sha256": sha_file(short_dir(item["id"]) / "SCRIPT.txt"),
            "transfer_input_sha256": sha_file(short_dir(item["id"]) / "TRANSFER-INPUT.json"),
        })
    duration = sum(float(row["duration_seconds"]) for row in rows)
    cost = sum(float(row["estimated_cost_usd"]) for row in rows)
    per_call_credits = [math.ceil(float(row["duration_seconds"]) * ELEVEN_CREDITS_PER_MINUTE / 60) for row in rows]
    credits = sum(per_call_credits)
    save_json_x(output, {
        "at_utc": now(),
        "status": "guides_complete_exact_local_asr_passed",
        "guides": rows,
        "aggregate_duration_seconds": duration,
        "google_estimated_cost_usd": cost,
        "google_spend_cap_usd": GOOGLE_SPEND_CAP_USD,
        "elevenlabs_estimated_credits_per_call_ceiling": per_call_credits,
        "elevenlabs_estimated_credits_total_ceiling": credits,
        "elevenlabs_credit_cap": ELEVEN_CREDIT_CAP,
        "duration_cap_equivalent_seconds": 192.0,
        "duration_and_credit_gate": "pass" if duration <= 192 and credits <= ELEVEN_CREDIT_CAP else "hold_zero_transfers",
        "generation_calls_made": 4,
    })
    print(json.dumps({"duration_seconds": duration, "estimated_credits_ceiling": credits, "google_estimated_usd": cost, "gate": "pass" if duration <= 192 and credits <= ELEVEN_CREDIT_CAP else "hold_zero_transfers"}))


NUMBER_WORDS = {"30": "thirty"}


def normalize_tokens(text: str) -> list[str]:
    text = unicodedata.normalize("NFKC", text).lower().replace("&", " and ")
    tokens = re.findall(r"[a-z0-9]+(?:['’][a-z0-9]+)?", text)
    return [NUMBER_WORDS.get(token, token).replace("'", "").replace("’", "") for token in tokens]


def run_asr(short_id: str, stage: str) -> None:
    run = require_prepared()
    assert_batch_clear()
    validate_short_inputs(short_id, run)
    if stage not in ("guide", "final"):
        raise SystemExit("ASR stage must be guide or final")
    work = short_dir(short_id)
    if stage == "guide":
        media = work / "media/guide.wav"
        receipt_path = work / "GOOGLE-RECEIPT.json"
        receipt_key = "guide"
    else:
        media = work / "media/original-c.wav"
        receipt_path = work / "ELEVEN-RECEIPT.json"
        receipt_key = "voice"
    canonical = work / ("GUIDE-ASR.json" if stage == "guide" else "FINAL-ASR.json")
    intent = work / f"{stage.upper()}-ASR-INTENT.json"
    asr_dir = work / f"asr-{stage}"
    if intent.exists() or canonical.exists() or asr_dir.exists():
        raise SystemExit(f"{stage} ASR already attempted for {short_id}")
    if not receipt_path.exists() or not media.exists():
        raise SystemExit(f"Missing accepted {stage} media or receipt for {short_id}")
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    if receipt.get("http_status") != 200 or receipt.get(receipt_key, {}).get("sha256") != sha_file(media):
        raise SystemExit(f"{stage} media is not bound to its provider receipt")
    if stage == "guide" and not receipt.get("accepted"):
        raise SystemExit("Guide receipt is not accepted")
    if stage == "final" and not receipt.get("accepted_pending_exact_final_asr_and_owner_listen"):
        raise SystemExit("Final transfer receipt is not technically accepted")
    command = [
        "npx",
        "--yes",
        "hyperframes@0.8.59",
        "transcribe",
        str(media),
        "--engine",
        "whisper",
        "--model",
        "small.en",
        "--language",
        "en",
        "--dir",
        str(asr_dir),
        "--json",
    ]
    media_sha = sha_file(media)
    save_json_x(intent, {
        "at_utc": now(),
        "stage": stage,
        "short_id": short_id,
        "source_media_path": rel(media),
        "source_media_sha256": media_sha,
        "provider_receipt_path": rel(receipt_path),
        "provider_receipt_sha256": sha_file(receipt_path),
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
        completed = subprocess.run(
            command,
            cwd=REPO,
            env=env,
            capture_output=True,
            text=True,
            timeout=900,
            check=False,
        )
    except Exception as exc:
        save_json_x(work / f"{stage.upper()}-ASR-ERROR.json", {
            "at_utc": now(),
            "error_class": type(exc).__name__,
            "status": "local_asr_failed_batch_stopped",
        })
        raise SystemExit(f"Local {stage} ASR failed for {short_id}")
    stdout_lines = [line for line in completed.stdout.splitlines() if line.strip()]
    envelope = None
    for line in reversed(stdout_lines):
        try:
            candidate = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(candidate, dict):
            envelope = candidate
            break
    transcript_path = asr_dir / "transcript.json"
    if completed.returncode != 0 or envelope is None or not transcript_path.exists():
        save_json_x(work / f"{stage.upper()}-ASR-ERROR.json", {
            "at_utc": now(),
            "returncode": completed.returncode,
            "stdout_tail": completed.stdout[-4000:],
            "stderr_tail": completed.stderr[-4000:],
            "status": "local_asr_failed_batch_stopped",
        })
        raise SystemExit(f"Local {stage} ASR command failed for {short_id}")
    expected_transcript_path = transcript_path.resolve()
    if (
        envelope.get("ok") is not True
        or envelope.get("engine") != "whisper"
        or envelope.get("model") != "small.en"
        or Path(str(envelope.get("transcriptPath", ""))).resolve() != expected_transcript_path
        or sha_file(media) != media_sha
    ):
        save_json_x(work / f"{stage.upper()}-ASR-ERROR.json", {
            "at_utc": now(),
            "status": "local_asr_envelope_or_media_binding_failed_batch_stopped",
            "envelope": envelope,
        })
        raise SystemExit(f"Local {stage} ASR provenance binding failed for {short_id}")
    save_json_x(asr_dir / "result.json", envelope)
    words = json.loads(transcript_path.read_text(encoding="utf-8"))
    if not isinstance(words, list) or not words or envelope.get("wordCount") != len(words):
        raise SystemExit("ASR transcript/envelope is not a consistent non-empty flat word array")
    transcript = " ".join(str(word.get("text", "")) for word in words)
    expected = (work / "SCRIPT.txt").read_text(encoding="utf-8")
    expected_tokens = normalize_tokens(expected)
    actual_tokens = normalize_tokens(transcript)
    match = expected_tokens == actual_tokens
    mismatch_index = next(
        (index for index, pair in enumerate(zip(expected_tokens, actual_tokens)) if pair[0] != pair[1]),
        min(len(expected_tokens), len(actual_tokens)) if len(expected_tokens) != len(actual_tokens) else None,
    )
    timing_values_valid = all(
        isinstance(word.get("start"), (int, float))
        and isinstance(word.get("end"), (int, float))
        and float(word["start"]) >= 0
        and float(word["end"]) >= float(word["start"])
        for word in words
    )
    timing_order_valid = timing_values_valid and all(
        float(words[index]["start"]) >= float(words[index - 1]["start"])
        for index in range(1, len(words))
    )
    media_duration = float(receipt[receipt_key]["duration_seconds"])
    timing_duration_valid = timing_values_valid and float(words[-1]["end"]) <= media_duration + 0.5
    asr_run = {
        "at_utc": now(),
        "intent_sha256": sha_file(intent),
        "source_media_path": rel(media),
        "source_media_sha256": media_sha,
        "command": command,
        "returncode": completed.returncode,
        "stdout_envelope": envelope,
        "stderr_tail": completed.stderr[-4000:],
        "transcript_path": rel(transcript_path),
        "transcript_sha256": sha_file(transcript_path),
    }
    run_record = work / f"{stage.upper()}-ASR-RUN.json"
    save_json_x(run_record, asr_run)
    result = {
        "at_utc": now(),
        "stage": stage,
        "tool": "hyperframes@0.8.59",
        "engine": "whisper",
        "model": "small.en",
        "language": "en",
        "asr_run_path": rel(run_record),
        "asr_run_sha256": sha_file(run_record),
        "transcript_path": rel(transcript_path),
        "transcript_sha256": sha_file(transcript_path),
        "media_sha256": media_sha,
        "script_sha256": sha_file(work / "SCRIPT.txt"),
        "expected_normalized_tokens": expected_tokens,
        "asr_normalized_tokens": actual_tokens,
        "expected_token_count": len(expected_tokens),
        "asr_token_count": len(actual_tokens),
        "exact_normalized_word_match": match,
        "word_timing_values_valid": timing_values_valid,
        "word_timing_order_valid": timing_order_valid,
        "word_timing_within_media_duration": timing_duration_valid,
        "first_mismatch_index": mismatch_index,
        "first_mismatch_expected_context": expected_tokens[max(0, (mismatch_index or 0) - 4):(mismatch_index or 0) + 5] if mismatch_index is not None else None,
        "first_mismatch_asr_context": actual_tokens[max(0, (mismatch_index or 0) - 4):(mismatch_index or 0) + 5] if mismatch_index is not None else None,
        "accepted": match and timing_values_valid and timing_order_valid and timing_duration_valid,
    }
    save_json_x(canonical, result)
    print(json.dumps({"short_id": short_id, "stage": stage, "exact_match": match, "timings_valid": timing_values_valid and timing_order_valid and timing_duration_valid, "mismatch_index": mismatch_index}))
    if not result["accepted"]:
        raise SystemExit(f"{stage} ASR did not exactly match locked normalized words for {short_id}")


def transfer_preflight() -> None:
    require_prepared()
    assert_batch_clear()
    output = BASE / "TRANSFER-BATCH-PREFLIGHT.json"
    if output.exists():
        raise SystemExit("Transfer preflight already exists")
    summary = json.loads((BASE / "GUIDE-BATCH-SUMMARY.json").read_text(encoding="utf-8"))
    if summary["duration_and_credit_gate"] != "pass":
        raise SystemExit("Guide batch exceeds approved duration/credit cap; zero transfers allowed")
    bindings = []
    for row in scripts():
        validate_guide_evidence(row["id"])
        work = short_dir(row["id"])
        path = work / "GUIDE-ASR.json"
        receipt_path = work / "GOOGLE-RECEIPT.json"
        guide_path = work / "media/guide.wav"
        if not path.exists():
            raise SystemExit(f"Missing exact guide ASR for {row['id']}")
        record = json.loads(path.read_text(encoding="utf-8"))
        if not record.get("accepted") or record.get("media_sha256") != sha_file(guide_path):
            raise SystemExit(f"Guide ASR failed for {row['id']}")
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        summary_row = next((item for item in summary.get("guides", []) if item.get("short_id") == row["id"]), None)
        expected_summary_binding = {
            "short_id": row["id"],
            "duration_seconds": receipt["guide"]["duration_seconds"],
            "sha256": sha_file(guide_path),
            "tail_energy": receipt["guide"].get("tail_energy"),
            "estimated_cost_usd": receipt["estimated_cost_usd_conservative_input_tokens"],
            "guide_receipt_sha256": sha_file(receipt_path),
            "guide_asr_sha256": sha_file(path),
            "script_sha256": sha_file(work / "SCRIPT.txt"),
            "transfer_input_sha256": sha_file(work / "TRANSFER-INPUT.json"),
        }
        if summary_row is None or any(summary_row.get(key) != value for key, value in expected_summary_binding.items()):
            raise SystemExit(f"Guide summary no longer binds current evidence for {row['id']}")
        bindings.append({
            "short_id": row["id"],
            "guide_receipt_sha256": sha_file(receipt_path),
            "guide_asr_sha256": sha_file(path),
            "guide_media_sha256": sha_file(guide_path),
            "script_sha256": sha_file(work / "SCRIPT.txt"),
            "transfer_input_sha256": sha_file(work / "TRANSFER-INPUT.json"),
        })
    current_durations = [
        float(json.loads((short_dir(row["id"]) / "GOOGLE-RECEIPT.json").read_text(encoding="utf-8"))["guide"]["duration_seconds"])
        for row in scripts()
    ]
    current_cost = sum(
        float(json.loads((short_dir(row["id"]) / "GOOGLE-RECEIPT.json").read_text(encoding="utf-8"))["estimated_cost_usd_conservative_input_tokens"])
        for row in scripts()
    )
    current_per_call_credits = [math.ceil(duration * ELEVEN_CREDITS_PER_MINUTE / 60) for duration in current_durations]
    if (
        float(summary.get("aggregate_duration_seconds", -1)) != sum(current_durations)
        or float(summary.get("google_estimated_cost_usd", -1)) != current_cost
        or summary.get("elevenlabs_estimated_credits_per_call_ceiling") != current_per_call_credits
        or summary.get("elevenlabs_estimated_credits_total_ceiling") != sum(current_per_call_credits)
        or current_cost > GOOGLE_SPEND_CAP_USD
    ):
        raise SystemExit("Guide batch aggregate summary no longer equals current receipts")
    account, voice, headers = read_account_and_voice()
    credits = int(summary["elevenlabs_estimated_credits_total_ceiling"])
    if credits > ELEVEN_CREDIT_CAP or account["remaining_included_credits"] < credits:
        raise SystemExit("Live ElevenLabs balance or approved cap does not cover this batch")
    save_json_x(output, {
        "at_utc": now(),
        "status": "pass_transfer_submission_allowed_once_per_short",
        "guide_summary_sha256": sha_file(BASE / "GUIDE-BATCH-SUMMARY.json"),
        "short_bindings": bindings,
        "estimated_credits_ceiling": credits,
        "approved_credit_cap": ELEVEN_CREDIT_CAP,
        "duration_seconds": summary["aggregate_duration_seconds"],
        "account": account,
        "voice": voice,
        "response_headers": headers,
        "transfer_rate_multiplier": 1,
        "generation_calls_before_transfer": 4,
        "automatic_retries": 0,
    })
    print(json.dumps({"status": "pass", "duration_seconds": summary["aggregate_duration_seconds"], "estimated_credits": credits, "available": account["remaining_included_credits"]}))


def transfer(short_id: str) -> None:
    run = require_prepared()
    assert_batch_clear()
    assert_transfer_order(short_id)
    validate_short_inputs(short_id, run)
    validate_guide_evidence(short_id)
    preflight_path = BASE / "TRANSFER-BATCH-PREFLIGHT.json"
    if not preflight_path.exists():
        raise SystemExit("Transfer batch preflight has not passed")
    preflight = json.loads(preflight_path.read_text(encoding="utf-8"))
    if preflight.get("status") != "pass_transfer_submission_allowed_once_per_short":
        raise SystemExit("Transfer batch preflight is not a pass")
    summary_path = BASE / "GUIDE-BATCH-SUMMARY.json"
    if preflight.get("guide_summary_sha256") != sha_file(summary_path):
        raise SystemExit("Guide batch summary changed after transfer preflight")
    if preflight.get("approved_credit_cap") != ELEVEN_CREDIT_CAP or preflight.get("transfer_rate_multiplier") != 1:
        raise SystemExit("Transfer preflight cap or rate binding changed")
    work = short_dir(short_id)
    intent = work / "ELEVEN-SUBMISSION-INTENT.json"
    if intent.exists():
        raise SystemExit(f"ElevenLabs intent already exists for {short_id}; no retry authorized")
    if count_intents("ELEVEN-SUBMISSION-INTENT.json") >= TRANSFER_CALL_CAP:
        raise SystemExit("ElevenLabs transfer call cap already reached")
    if count_intents("GOOGLE-SUBMISSION-INTENT.json") != GUIDE_CALL_CAP:
        raise SystemExit("All four guide submissions must be complete before any transfer")
    if count_intents("GOOGLE-SUBMISSION-INTENT.json") + count_intents("ELEVEN-SUBMISSION-INTENT.json") >= TOTAL_CALL_CAP:
        raise SystemExit("Total provider generation call cap already reached")
    guide = work / "media/guide.wav"
    guide_receipt_path = work / "GOOGLE-RECEIPT.json"
    guide_asr_path = work / "GUIDE-ASR.json"
    guide_receipt = json.loads(guide_receipt_path.read_text(encoding="utf-8"))
    guide_asr = json.loads(guide_asr_path.read_text(encoding="utf-8"))
    binding = next((item for item in preflight.get("short_bindings", []) if item.get("short_id") == short_id), None)
    expected_binding = {
        "short_id": short_id,
        "guide_receipt_sha256": sha_file(guide_receipt_path),
        "guide_asr_sha256": sha_file(guide_asr_path),
        "guide_media_sha256": sha_file(guide),
        "script_sha256": sha_file(work / "SCRIPT.txt"),
        "transfer_input_sha256": sha_file(work / "TRANSFER-INPUT.json"),
    }
    if binding != expected_binding:
        raise SystemExit("Short evidence changed after transfer preflight")
    if (
        guide_receipt["guide"]["sha256"] != sha_file(guide)
        or not guide_asr.get("accepted")
        or guide_asr.get("media_sha256") != sha_file(guide)
        or guide_asr.get("script_sha256") != sha_file(work / "SCRIPT.txt")
    ):
        raise SystemExit("Guide binding or exact-copy ASR gate failed")
    estimated_credits = math.ceil(float(guide_receipt["guide"]["duration_seconds"]) * ELEVEN_CREDITS_PER_MINUTE / 60)
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    if int(summary["elevenlabs_estimated_credits_total_ceiling"]) > ELEVEN_CREDIT_CAP:
        raise SystemExit("Aggregate credit cap failed")
    transfer_input = json.loads((work / "TRANSFER-INPUT.json").read_text(encoding="utf-8"))
    fields = transfer_input["fields"]
    body, content_type = cal.multipart(fields, guide.name, guide.read_bytes())
    url = f"{transfer_input['endpoint']}?output_format={transfer_input['output_format']}&enable_logging=true"
    remaining_rows = scripts()[len(prior_rows(short_id)):]
    remaining_credits = sum(
        math.ceil(
            float(json.loads((short_dir(row["id"]) / "GOOGLE-RECEIPT.json").read_text(encoding="utf-8"))["guide"]["duration_seconds"])
            * ELEVEN_CREDITS_PER_MINUTE
            / 60
        )
        for row in remaining_rows
    )
    prior_actual_credits = prior_actual_eleven_cost(short_id)
    if prior_actual_credits + remaining_credits > ELEVEN_CREDIT_CAP:
        raise SystemExit("Cumulative actual cost plus estimated unsubmitted transfers would exceed the 3,200-credit cap")
    account, voice, account_headers = read_account_and_voice()
    if account["remaining_included_credits"] < remaining_credits:
        raise SystemExit("Live ElevenLabs balance no longer covers the unsubmitted transfers")
    account_before_path = work / "ELEVEN-ACCOUNT-BEFORE.json"
    save_json_x(account_before_path, {
        "at_utc": now(),
        "account": account,
        "voice": voice,
        "response_headers": account_headers,
        "remaining_batch_estimated_credits_ceiling": remaining_credits,
        "prior_transfers_actual_credits": prior_actual_credits,
        "authorization_cap_check": prior_actual_credits + remaining_credits,
    })
    save_json_x(intent, {
        "at_utc": now(),
        "stage": "elevenlabs_voice_transfer",
        "short_id": short_id,
        "url": url,
        "fields": fields,
        "request_body_sha256": sha_bytes(body),
        "guide_path": rel(guide),
        "guide_sha256": sha_file(guide),
        "guide_asr_sha256": sha_file(work / "GUIDE-ASR.json"),
        "transfer_input_sha256": sha_file(work / "TRANSFER-INPUT.json"),
        "transfer_batch_preflight_sha256": sha_file(preflight_path),
        "account_before_sha256": sha_file(account_before_path),
        "provider_generation_attempt": 1,
        "automatic_retries": 0,
        "estimated_credits_ceiling": estimated_credits,
        "prior_transfers_actual_credits": prior_actual_credits,
        "remaining_unsubmitted_estimated_credits_including_this_call": remaining_credits,
        "aggregate_credits_ceiling": summary["elevenlabs_estimated_credits_total_ceiling"],
        "credit_cap": ELEVEN_CREDIT_CAP,
        "aggregate_provider_generation_calls_after_submission": 4 + count_intents("ELEVEN-SUBMISSION-INTENT.json") + 1,
        "submission_outcome_policy": "uncertain or failed outcome stops the batch and cannot be retried",
    })
    key = cal.read_dotenv_key("ELEVENLABS_API_KEY")
    try:
        status, raw, response_headers = safe_request(
            url,
            method="POST",
            headers={"xi-api-key": key, "Content-Type": content_type, "Accept": "*/*"},
            body=body,
        )
    except Exception as exc:
        save_json_x(work / "ELEVEN-ERROR.json", {
            "at_utc": now(),
            "error_class": type(exc).__name__,
            "submission_outcome": "uncertain_no_retry",
        })
        raise SystemExit(f"ElevenLabs transport outcome uncertain for {short_id}; no retry")
    save_bytes_x(work / "media/elevenlabs-response.pcm", raw)
    receipt: dict[str, Any] = {
        "at_utc": now(),
        "http_status": status,
        "response_headers": response_headers,
        "raw_response_path": rel(work / "media/elevenlabs-response.pcm"),
        "raw_response_sha256": sha_bytes(raw),
        "guide_sha256": sha_file(guide),
        "estimated_credits_ceiling": estimated_credits,
        "calls": 1,
        "retries": 0,
    }
    if status != 200:
        receipt["error"] = redact_error(raw, [key])
        receipt["accepted"] = False
        save_json_x(work / "ELEVEN-RECEIPT.json", receipt)
        raise SystemExit(f"ElevenLabs HTTP {status} for {short_id}; no retry")
    try:
        actual_credits = parse_actual_eleven_cost(receipt)
    except ValueError as exc:
        receipt["actual_credit_cost_verified"] = False
        receipt["accepted_pending_exact_final_asr_and_owner_listen"] = False
        receipt["error"] = str(exc)
        save_json_x(work / "ELEVEN-RECEIPT.json", receipt)
        raise SystemExit(f"{exc}; batch stopped") from exc
    future_rows = scripts()[len(prior_rows(short_id)) + 1:]
    future_estimated_credits = sum(
        math.ceil(
            float(json.loads((short_dir(row["id"]) / "GOOGLE-RECEIPT.json").read_text(encoding="utf-8"))["guide"]["duration_seconds"])
            * ELEVEN_CREDITS_PER_MINUTE
            / 60
        )
        for row in future_rows
    )
    cumulative_actual_credits = prior_actual_credits + actual_credits
    budget_allows_remaining = (
        cumulative_actual_credits <= ELEVEN_CREDIT_CAP
        and cumulative_actual_credits + future_estimated_credits <= ELEVEN_CREDIT_CAP
    )
    final = work / "media/original-c.wav"
    cal.wav_from_pcm(raw, cal.TRANSFER_OUTPUT_RATE_HZ, final)
    final.chmod(0o600)
    probe = cal.probe(final)
    delta = float(probe["duration_seconds"]) - float(guide_receipt["guide"]["duration_seconds"])
    tail = float(probe.get("tail_energy", 1))
    tail_class = "silent" if tail < cal.TAIL_ENERGY_THRESHOLD else "marginal" if tail < 0.06 else "still_sounding"
    technical_pass = abs(delta) <= 0.5 and tail_class in ("silent", "marginal")
    receipt |= {
        "voice": probe | {"path": rel(final)},
        "duration_delta_seconds": delta,
        "transfer_tail_class": tail_class,
        "transfer_marginal_ceiling": 0.06,
        "technical_duration_and_tail_pass": technical_pass,
        "actual_credit_cost_verified": True,
        "actual_credit_cost": actual_credits,
        "cumulative_actual_credit_cost": cumulative_actual_credits,
        "future_unsubmitted_estimated_credits_ceiling": future_estimated_credits,
        "budget_allows_remaining": budget_allows_remaining,
        "accepted_pending_exact_final_asr_and_owner_listen": technical_pass and budget_allows_remaining,
    }
    save_json_x(work / "ELEVEN-RECEIPT.json", receipt)
    if not technical_pass or not budget_allows_remaining:
        raise SystemExit(f"Transferred audio failed technical or credit-cap gate for {short_id}; no retry")
    print(json.dumps({"short_id": short_id, "duration_seconds": probe["duration_seconds"], "tail_energy": probe.get("tail_energy"), "duration_delta_seconds": delta, "estimated_credits": estimated_credits, "actual_credits": actual_credits, "cumulative_actual_credits": cumulative_actual_credits}))


def account_after() -> None:
    require_prepared()
    assert_batch_clear()
    output = BASE / "ACCOUNT-AFTER.json"
    if output.exists():
        raise SystemExit("Account-after record already exists")
    if count_intents("ELEVEN-SUBMISSION-INTENT.json") != TRANSFER_CALL_CAP:
        raise SystemExit("Not all four transfer intents exist")
    for row in scripts():
        validate_final_evidence(row["id"])
    account, voice, headers = read_account_and_voice()
    before = json.loads((BASE / "TRANSFER-BATCH-PREFLIGHT.json").read_text(encoding="utf-8"))["account"]
    delta = account["character_count"] - before["character_count"]
    actual_header_total = sum(
        parse_actual_eleven_cost(json.loads((short_dir(row["id"]) / "ELEVEN-RECEIPT.json").read_text(encoding="utf-8")))
        for row in scripts()
    )
    if actual_header_total > ELEVEN_CREDIT_CAP:
        raise SystemExit("Verified ElevenLabs response-header total exceeds authorization cap")
    save_json_x(output, {
        "at_utc": now(),
        "account": account,
        "voice": voice,
        "response_headers": headers,
        "usage_delta_since_transfer_preflight": delta,
        "verified_response_header_credit_total": actual_header_total,
        "authorized_credit_cap": ELEVEN_CREDIT_CAP,
        "delta_attribution": "May include concurrent account use; exact response cost headers take precedence when present.",
    })
    print(json.dumps({"account_usage_delta": delta, "remaining": account["remaining_included_credits"]}))


def finalize() -> None:
    require_prepared()
    assert_batch_clear()
    output = BASE / "BATCH-STATUS.json"
    if output.exists():
        raise SystemExit("Batch status already exists")
    items = []
    for row in scripts():
        validate_guide_evidence(row["id"])
        validate_final_evidence(row["id"])
        work = short_dir(row["id"])
        paths = {
            "guide_receipt": work / "GOOGLE-RECEIPT.json",
            "guide_asr": work / "GUIDE-ASR.json",
            "transfer_receipt": work / "ELEVEN-RECEIPT.json",
            "final_asr": work / "FINAL-ASR.json",
        }
        if not all(path.exists() for path in paths.values()):
            raise SystemExit(f"Missing final evidence for {row['id']}")
        guide = json.loads(paths["guide_receipt"].read_text(encoding="utf-8"))
        transfer_receipt = json.loads(paths["transfer_receipt"].read_text(encoding="utf-8"))
        final_asr = json.loads(paths["final_asr"].read_text(encoding="utf-8"))
        if not guide.get("accepted") or not transfer_receipt.get("accepted_pending_exact_final_asr_and_owner_listen") or not final_asr.get("accepted"):
            raise SystemExit(f"Final gates failed for {row['id']}")
        items.append({
            "short_id": row["id"],
            "guide": guide["guide"],
            "final": transfer_receipt["voice"],
            "guide_asr_sha256": sha_file(paths["guide_asr"]),
            "final_asr_sha256": sha_file(paths["final_asr"]),
            "owner_perceptual_listen": "pending",
        })
    if not (BASE / "ACCOUNT-AFTER.json").exists():
        raise SystemExit("Missing account-after record")
    save_json_x(output, {
        "at_utc": now(),
        "status": "four_original_c_narrations_technically_complete_owner_perceptual_listen_pending",
        "items": items,
        "generation_calls": {"google": 4, "elevenlabs": 4, "total": 8, "retries": 0},
        "google_estimated_cost_usd": json.loads((BASE / "GUIDE-BATCH-SUMMARY.json").read_text(encoding="utf-8"))["google_estimated_cost_usd"],
        "elevenlabs_verified_response_header_credits": json.loads((BASE / "ACCOUNT-AFTER.json").read_text(encoding="utf-8"))["verified_response_header_credit_total"],
        "elevenlabs_account_usage_delta": json.loads((BASE / "ACCOUNT-AFTER.json").read_text(encoding="utf-8"))["usage_delta_since_transfer_preflight"],
        "next_gate": "owner listening approval, then audio-derived scene retiming; avatar generation remains separately unauthorized",
    })
    print(json.dumps({"status": "complete_pending_owner_listen", "shorts": 4, "provider_calls": 8, "retries": 0}))


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

    if args.command == "prepare":
        prepare()
    elif args.command == "preflight":
        preflight()
    elif args.command == "guide":
        generate_guide(args.short_id)
    elif args.command == "guide-summary":
        guide_summary()
    elif args.command == "asr":
        run_asr(args.short_id, args.stage)
    elif args.command == "transfer-preflight":
        transfer_preflight()
    elif args.command == "transfer":
        transfer(args.short_id)
    elif args.command == "account-after":
        account_after()
    elif args.command == "finalize":
        finalize()


if __name__ == "__main__":
    main()
