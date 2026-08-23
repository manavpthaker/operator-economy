"""Bounded ElevenLabs capture with dry-run default and no text rewriting."""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .audio import inspect_audio
from .core import (
    ValidationError,
    read_canonical_w,
    read_json,
    sha256_bytes,
    sha256_file,
    token_identity,
    validate_capture_plan,
)


API_ROOT = "https://api.elevenlabs.io/v1/text-to-speech"


@dataclass(frozen=True)
class RequestSpec:
    part_id: str
    start_token: int
    end_token: int
    text: str
    url: str
    body: bytes

    def public_dict(self) -> dict[str, Any]:
        return {
            "part_id": self.part_id,
            "start_token": self.start_token,
            "end_token": self.end_token,
            "url": self.url,
            "body_sha256": sha256_bytes(self.body),
            "text_sha256": sha256_bytes(self.text.encode("utf-8")),
            "character_count": len(self.text),
        }


def request_url(voice_id: str, output_format: str) -> str:
    encoded_voice = urllib.parse.quote(voice_id, safe="")
    query = urllib.parse.urlencode({"output_format": output_format})
    return f"{API_ROOT}/{encoded_voice}?{query}"


def build_requests(plan: dict[str, Any], tokens: list[str], output_format: str = "pcm_48000") -> list[RequestSpec]:
    provider = plan["provider"]
    specs: list[RequestSpec] = []
    for part in plan["parts"]:
        start, end = part["start_token"], part["end_token"]
        # This is a transport representation of W, not a rewrite. Token identity
        # remains authoritative; acoustic/context parts are subordinate.
        text = " ".join(tokens[start:end])
        payload = {
            "text": text,
            "model_id": provider["model_id"],
            "voice_settings": provider["voice_settings"],
        }
        body = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        specs.append(
            RequestSpec(
                part_id=part["id"],
                start_token=start,
                end_token=end,
                text=text,
                url=request_url(provider["voice_id"], output_format),
                body=body,
            )
        )
    return specs


def validate_execution_authorization(
    authorization_path: Path,
    plan_path: Path,
    plan: dict[str, Any],
    spoken_sha256: str,
    tokens: list[str],
) -> dict[str, Any]:
    authorization = read_json(authorization_path)
    errors: list[str] = []
    if authorization.get("schema_version") != "oe-provider-authorization-v1":
        errors.append("execution authorization must use oe-provider-authorization-v1")
    if not isinstance(authorization.get("authorization_id"), str) or not authorization.get("authorization_id"):
        errors.append("execution authorization requires authorization_id")
    if authorization.get("status") != "active":
        errors.append("execution authorization status must be active")
    if authorization.get("approved") is not True:
        errors.append("execution authorization is not approved")
    if authorization.get("scope") != plan.get("capture_phase"):
        errors.append("execution authorization scope does not match the capture phase")
    if authorization.get("capture_plan_sha256") != sha256_file(plan_path):
        errors.append("execution authorization is not bound to the current capture-plan hash")
    if authorization.get("spoken_text_sha256") != spoken_sha256:
        errors.append("execution authorization is not bound to canonical W")
    if authorization.get("script_sha256") != plan.get("script_sha256"):
        errors.append("execution authorization is not bound to the capture plan's locked script")
    provider = plan.get("provider", {})
    if authorization.get("provider") != "elevenlabs" or authorization.get("voice_id") != provider.get("voice_id"):
        errors.append("execution authorization provider or voice does not match the plan")
    if authorization.get("model_id") != provider.get("model_id"):
        errors.append("execution authorization model does not match the plan")
    if authorization.get("target") != plan.get("target"):
        errors.append("execution authorization target does not match the plan")
    policy = plan.get("format_policy", {})
    if authorization.get("preferred_output_format") != policy.get("preferred"):
        errors.append("execution authorization preferred format does not match the plan")
    if authorization.get("fallback_output_format") != policy.get("fallback"):
        errors.append("execution authorization fallback format does not match the plan")
    part_count = len(plan.get("parts", []))
    max_calls = authorization.get("max_calls")
    if not isinstance(max_calls, int) or isinstance(max_calls, bool) or not (part_count <= max_calls <= 2 * part_count):
        errors.append("execution authorization max_calls must be between planned parts and twice planned parts")
    if "max_credits" in authorization:
        errors.append("max_credits is ambiguous; use the enforceable max_characters field")
    character_cap = authorization.get("max_characters")
    spend_cap = authorization.get("max_spend_usd")
    if not (
        (isinstance(character_cap, int) and not isinstance(character_cap, bool) and character_cap > 0)
        or (isinstance(spend_cap, (int, float)) and not isinstance(spend_cap, bool) and spend_cap > 0)
    ):
        errors.append("execution authorization requires a positive max_characters or max_spend_usd ceiling")
    exact_characters_once = sum(len(" ".join(tokens[part["start_token"] : part["end_token"]])) for part in plan.get("parts", []))
    if isinstance(character_cap, int) and character_cap < exact_characters_once:
        errors.append(
            f"max_characters {character_cap} is below the first-attempt payload total {exact_characters_once}"
        )
    consumption = authorization.get("consumption")
    if not isinstance(consumption, dict):
        errors.append("execution authorization requires consumption state")
        consumption = {}
    if consumption.get("status") != "unconsumed" or consumption.get("calls_used") != 0:
        errors.append("execution authorization must be unconsumed with calls_used=0")
    try:
        record_value = consumption.get("record_path")
        if not isinstance(record_value, str) or not record_value:
            raise ValueError
        record_path = Path(record_value)
        if record_path.is_absolute() or ".." in record_path.parts:
            raise ValueError
    except (TypeError, ValueError):
        errors.append("consumption.record_path must be a safe relative path")
    for field in ("approved_by", "approved_at", "expires_at"):
        if not isinstance(authorization.get(field), str) or not authorization.get(field):
            errors.append(f"execution authorization {field} is required")
    expires_at = authorization.get("expires_at")
    if isinstance(expires_at, str) and expires_at:
        try:
            expires = datetime.fromisoformat(expires_at.replace("Z", "+00:00"))
            if expires.tzinfo is None or expires <= datetime.now(timezone.utc):
                errors.append("execution authorization is expired or lacks a timezone")
        except ValueError:
            errors.append("execution authorization expires_at must be an ISO-8601 timestamp")
    if errors:
        raise ValidationError(errors)
    return authorization


def consume_authorization(authorization_path: Path, authorization: dict[str, Any], plan_path: Path) -> Path:
    consumption = authorization["consumption"]
    record_rel = Path(consumption["record_path"])
    record_path = (authorization_path.parent / record_rel).resolve()
    if not record_path.is_relative_to(authorization_path.parent.resolve()):
        raise ValidationError("consumption record escapes the authorization directory")
    record = {
        "schema_version": "oe-provider-authorization-consumption-v1",
        "authorization_id": authorization["authorization_id"],
        "authorization_sha256": sha256_file(authorization_path),
        "capture_plan_sha256": sha256_file(plan_path),
        "status": "consumed",
        "consumed_at": _utc_now(),
        "reason": "provider execution started; retries require new authorization",
    }
    _exclusive_write(record_path, (json.dumps(record, indent=2, sort_keys=True) + "\n").encode("utf-8"))
    return record_path


def dry_run_capture(plan_path: Path, canonical_w_path: Path) -> dict[str, Any]:
    validation = validate_capture_plan(plan_path, canonical_w_path)
    plan = read_json(plan_path)
    tokens = read_canonical_w(canonical_w_path)
    specs = build_requests(plan, tokens, "pcm_48000")
    return {
        "mode": "dry-run",
        "network_called": False,
        "plan_validation": validation,
        "requested_output_format": "pcm_48000",
        "requests": [spec.public_dict() for spec in specs],
        "notice": "No provider request was made. Use --execute with a separately hashed authorization receipt.",
    }


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _http_post(spec: RequestSpec, api_key: str, timeout: float) -> tuple[bytes, dict[str, str]]:
    request = urllib.request.Request(
        spec.url,
        data=spec.body,
        method="POST",
        headers={"Content-Type": "application/json", "xi-api-key": api_key},
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            headers = {key.lower(): value for key, value in response.headers.items()}
            return response.read(), headers
    except urllib.error.HTTPError:
        raise
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        # Network, timeout, TLS, and DNS failures are never PCM capability failures.
        raise ValidationError(f"provider transport failed; MP3 fallback forbidden: {exc}") from exc


def _parse_http_error(exc: urllib.error.HTTPError) -> tuple[str, str, bytes]:
    data = exc.read()
    code = "unknown"
    message = data.decode("utf-8", errors="replace")
    try:
        payload = json.loads(message)
        detail = payload.get("detail", payload) if isinstance(payload, dict) else payload
        if isinstance(detail, dict):
            code = str(detail.get("status") or detail.get("code") or "unknown")
            message = str(detail.get("message") or detail)
    except json.JSONDecodeError:
        pass
    return code, message, data


def _is_explicit_pcm_capability_failure(status: int, code: str, message: str) -> bool:
    if status not in {400, 404, 422}:
        return False
    haystack = f"{code} {message}".lower()
    mentions_pcm = "pcm" in haystack or "output_format" in haystack or "output format" in haystack
    unavailable = any(term in haystack for term in ("unsupported", "not supported", "unavailable", "not available", "not allowed", "invalid output"))
    return mentions_pcm and unavailable


def _exclusive_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with path.open("xb") as handle:
            handle.write(data)
    except FileExistsError as exc:
        raise ValidationError(f"refusing to overwrite immutable provider output: {path}") from exc


def _provider_identifiers(headers: dict[str, str]) -> dict[str, str]:
    allowed = ("request-id", "x-request-id", "xi-request-id", "history-item-id")
    return {key: headers[key] for key in allowed if headers.get(key)}


def execute_capture(
    plan_path: Path,
    canonical_w_path: Path,
    output_dir: Path,
    authorization_path: Path,
    timeout: float = 60.0,
) -> dict[str, Any]:
    validate_capture_plan(plan_path, canonical_w_path)
    plan = read_json(plan_path)
    tokens = read_canonical_w(canonical_w_path)
    identity = token_identity(tokens)
    authorization = validate_execution_authorization(
        authorization_path, plan_path, plan, identity["sha256"], tokens
    )
    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValidationError("ELEVENLABS_API_KEY is required only for --execute")
    if output_dir.exists() and any(output_dir.iterdir()):
        raise ValidationError(f"capture output directory is not empty: {output_dir}")
    output_dir.mkdir(parents=True, exist_ok=True)
    consumption_record_path = consume_authorization(authorization_path, authorization, plan_path)
    pcm_specs = build_requests(plan, tokens, "pcm_48000")
    results: list[dict[str, Any]] = []
    attempted_calls = 0
    attempted_characters = 0
    max_calls = authorization["max_calls"]
    max_characters = authorization.get("max_characters")

    def authorized_post(spec: RequestSpec) -> tuple[bytes, dict[str, str]]:
        nonlocal attempted_calls, attempted_characters
        next_calls = attempted_calls + 1
        next_characters = attempted_characters + len(spec.text)
        if next_calls > max_calls:
            raise ValidationError(
                f"authorization call ceiling exhausted before {spec.part_id}: {next_calls}>{max_calls}"
            )
        if isinstance(max_characters, int) and next_characters > max_characters:
            raise ValidationError(
                f"authorization character ceiling exhausted before {spec.part_id}: {next_characters}>{max_characters}"
            )
        attempted_calls = next_calls
        attempted_characters = next_characters
        return _http_post(spec, api_key, timeout)

    def write_failure(reason: str, spec: RequestSpec) -> None:
        failure_path = output_dir / "capture-failure-receipt.json"
        if failure_path.exists():
            return
        failure = {
            "schema_version": "oe-provider-capture-failure-v1",
            "authorization_sha256": sha256_file(authorization_path),
            "plan_sha256": sha256_file(plan_path),
            "request_envelope": spec.public_dict(),
            "attempted_calls": attempted_calls,
            "attempted_characters": attempted_characters,
            "reason": reason,
            "failed_at": _utc_now(),
            "creative_approved": False,
        }
        _exclusive_write(failure_path, (json.dumps(failure, indent=2, sort_keys=True) + "\n").encode("utf-8"))

    for spec in pcm_specs:
        fallback_failure: dict[str, Any] | None = None
        try:
            data, headers = authorized_post(spec)
            raw_path = output_dir / f"{spec.part_id}.provider-raw.pcm"
            _exclusive_write(raw_path, data)
            # ElevenLabs PCM is raw S16LE. Preserve the provider bytes and bind
            # their declared transport format instead of pretending it is WAV.
            if len(data) == 0 or len(data) % 2:
                raise ValidationError(f"provider PCM for {spec.part_id} is empty or not S16LE-aligned")
            result = {
                "part_id": spec.part_id,
                "request_envelope": spec.public_dict(),
                "requested_output_format": "pcm_48000",
                "actual_codec": "pcm_s16le",
                "container": "raw",
                "sample_rate_hz": 48_000,
                "channels": 1,
                "bit_depth": 16,
                "raw_path": str(raw_path),
                "raw_sha256": sha256_file(raw_path),
                "lossy_origin": False,
                "response_content_type": headers.get("content-type"),
                "provider_identifiers": _provider_identifiers(headers),
            }
        except urllib.error.HTTPError as exc:
            code, message, response_body = _parse_http_error(exc)
            if not _is_explicit_pcm_capability_failure(exc.code, code, message):
                write_failure(f"HTTP {exc.code}: {code}: {message}", spec)
                raise ValidationError(
                    f"PCM request failed with HTTP {exc.code}; MP3 fallback forbidden: {code}: {message}"
                ) from exc
            fallback_failure = {
                "http_status": exc.code,
                "kind": "pcm_capability_unavailable",
                "retryable": False,
                "provider_code": code,
                "message": message,
                "occurred_at": _utc_now(),
                "response_sha256": sha256_bytes(response_body),
                "attempted_call_number": attempted_calls,
            }
            mp3_spec = build_requests(
                {
                    **plan,
                    "parts": [
                        {
                            "id": spec.part_id,
                            "start_token": spec.start_token,
                            "end_token": spec.end_token,
                        }
                    ],
                },
                tokens,
                "mp3_44100_192",
            )[0]
            try:
                data, headers = authorized_post(mp3_spec)
            except urllib.error.HTTPError as fallback_exc:
                fallback_code, fallback_message, _ = _parse_http_error(fallback_exc)
                write_failure(
                    f"MP3 fallback HTTP {fallback_exc.code}: {fallback_code}: {fallback_message}",
                    mp3_spec,
                )
                raise ValidationError(
                    f"MP3 fallback failed with HTTP {fallback_exc.code}: {fallback_code}: {fallback_message}"
                ) from fallback_exc
            except ValidationError as fallback_exc:
                write_failure(str(fallback_exc), mp3_spec)
                raise
            raw_path = output_dir / f"{spec.part_id}.provider-raw.mp3"
            _exclusive_write(raw_path, data)
            try:
                audio = inspect_audio(raw_path)
                if not audio["is_approved_mp3_fallback"]:
                    raise ValidationError("fallback response is not actual mono mp3_44100_192 audio")
            except ValidationError as fallback_audio_error:
                write_failure(str(fallback_audio_error), mp3_spec)
                raise
            receipt = {
                "schema_version": "oe-pcm-capability-failure-v1",
                "provider": "elevenlabs",
                "attempted_output_format": "pcm_48000",
                "fallback_output_format": "mp3_44100_192",
                "failure": fallback_failure,
                "raw_output": {"path": str(raw_path), "sha256": sha256_file(raw_path)},
            }
            receipt_path = output_dir / f"{spec.part_id}.pcm-capability-failure.json"
            _exclusive_write(receipt_path, (json.dumps(receipt, indent=2, sort_keys=True) + "\n").encode("utf-8"))
            result = {
                "part_id": spec.part_id,
                "request_envelope": mp3_spec.public_dict(),
                "failed_pcm_request_envelope": spec.public_dict(),
                "requested_output_format": "pcm_48000",
                "actual_output_format": "mp3_44100_192",
                "raw_path": str(raw_path),
                "raw_sha256": sha256_file(raw_path),
                "lossy_origin": True,
                "pcm_failure_receipt": str(receipt_path),
                "response_content_type": headers.get("content-type"),
                "provider_identifiers": _provider_identifiers(headers),
            }
        except ValidationError as exc:
            write_failure(str(exc), spec)
            raise
        results.append(result)
    run_receipt = {
        "schema_version": "oe-provider-capture-run-v1",
        "created_at": _utc_now(),
        "plan_sha256": sha256_file(plan_path),
        "authorization_sha256": sha256_file(authorization_path),
        "authorization_consumption_record": str(consumption_record_path),
        "authorization_consumption_sha256": sha256_file(consumption_record_path),
        "authorized_by": authorization["approved_by"],
        "authorization_limits": {
            "max_calls": max_calls,
            "max_characters": max_characters,
            "max_spend_usd": authorization.get("max_spend_usd"),
            "max_spend_note": "authorization ceiling only; not observed provider billing",
        },
        "attempted_calls": attempted_calls,
        "attempted_characters": attempted_characters,
        "spoken_identity": identity,
        "results": results,
        "creative_approved": False,
    }
    receipt_path = output_dir / "capture-run-receipt.json"
    _exclusive_write(receipt_path, (json.dumps(run_receipt, indent=2, sort_keys=True) + "\n").encode("utf-8"))
    return {"mode": "execute", "network_called": True, "receipt": str(receipt_path), **run_receipt}
