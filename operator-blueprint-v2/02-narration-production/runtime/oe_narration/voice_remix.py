"""Fail-closed ElevenLabs voice-remix preview and selected-preview save.

Voice remixing is deliberately split into two independently authorized actions:

1. One request may generate one or more private previews.  Every returned
   preview is preserved and the receipt remains pending an owner decision.
2. A later request may save exactly one preview only when a second active
   authorization is bound to both the preview receipt and an explicit owner
   selection record.

Dry-run is the default integration surface.  Nothing in this module discovers
voices, chooses a preview, retries a request, follows a redirect, overwrites an
existing artifact, or mutates the incumbent voice.
"""

from __future__ import annotations

import base64
import binascii
import json
import math
import os
import re
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, BinaryIO

from .core import (
    ValidationError,
    read_canonical_w,
    read_json,
    sha256_bytes,
    sha256_file,
    token_identity,
)


PREVIEW_AUTH_SCHEMA = "oe-elevenlabs-voice-remix-preview-authorization-v1"
SAVE_AUTH_SCHEMA = "oe-elevenlabs-voice-remix-save-authorization-v1"
PREVIEW_RECEIPT_SCHEMA = "oe-elevenlabs-voice-remix-preview-receipt-v1"
SAVE_RECEIPT_SCHEMA = "oe-elevenlabs-voice-remix-save-receipt-v1"
OWNER_SELECTION_SCHEMA = "oe-elevenlabs-voice-remix-owner-selection-v1"
CONSUMPTION_SCHEMA = "oe-provider-authorization-consumption-v1"
PREVIEW_SCOPE = "elevenlabs_voice_remix_preview"
SAVE_SCOPE = "elevenlabs_voice_remix_save"
PREVIEW_API_ROOT = "https://api.elevenlabs.io/v1/text-to-voice"
SAVE_ENDPOINT = "https://api.elevenlabs.io/v1/text-to-voice"
OUTPUT_FORMAT = "mp3_44100_192"
MIN_PROMPT_STRENGTH = 0.20
MAX_PROMPT_STRENGTH = 0.30
MAX_PREVIEW_OUTPUTS = 4
MAX_PREVIEW_RESPONSE_BYTES = 50_000_000
MAX_PREVIEW_AUDIO_BYTES = 30_000_000
MAX_PREVIEW_DURATION_SECONDS = 300.0
MAX_SAVE_RESPONSE_BYTES = 2_000_000
MAX_AUTHORIZATION_WINDOW_SECONDS = 24 * 60 * 60
MAX_REMIX_PROMPT_CHARACTERS = 950
REQUIRED_HELD_OUT_SOURCE_ID = "C01B"
REQUIRED_HELD_OUT_START_TOKEN = 139
REQUIRED_HELD_OUT_END_TOKEN = 236
_ID_RE = re.compile(r"^[A-Za-z0-9_-]{8,160}$")
_REQUEST_ID_HEADERS = (
    "request-id",
    "x-request-id",
    "xi-request-id",
    "history-item-id",
    "trace-id",
    "x-trace-id",
    "traceparent",
)
_SECRET_KEY_RE = re.compile(
    r"(?:api[_-]?key|authorization[_-]?header|bearer|password|secret|access[_-]?token|refresh[_-]?token|credential[_-]?value)",
    re.I,
)
_SECRET_VALUE_RE = re.compile(r"(?:sk[_-][A-Za-z0-9_-]{12,}|xi[_-][A-Za-z0-9_-]{12,})")


@dataclass(frozen=True)
class _HttpResponse:
    data: bytes
    mime_type: str
    headers: dict[str, str]
    provider_identifiers: dict[str, str]


class _ProviderFailure(Exception):
    """A redacted, stable provider or transport failure."""

    def __init__(
        self,
        code: str,
        *,
        http_status: int | None = None,
        provider_identifiers: dict[str, str] | None = None,
    ) -> None:
        self.code = code
        self.http_status = http_status
        self.provider_identifiers = provider_identifiers or {}
        super().__init__(code)


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    """Never forward a provider credential to a redirected URL."""

    def redirect_request(  # type: ignore[override]
        self,
        req: urllib.request.Request,
        fp: BinaryIO,
        code: int,
        msg: str,
        headers: Any,
        newurl: str,
    ) -> None:
        return None


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _json_bytes(value: dict[str, Any]) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")


def _canonical_body(value: dict[str, Any]) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def _is_number(value: Any) -> bool:
    return (
        isinstance(value, (int, float))
        and not isinstance(value, bool)
        and math.isfinite(float(value))
    )


def _scan_for_secrets(value: Any, label: str = "authorization") -> list[str]:
    errors: list[str] = []

    def visit(current: Any, path: str) -> None:
        if isinstance(current, dict):
            for key, nested in current.items():
                key_text = str(key)
                if _SECRET_KEY_RE.search(key_text) and key_text not in {
                    "credential_env",
                    "authorization_id",
                }:
                    errors.append(f"{path}.{key_text} may contain credential material")
                visit(nested, f"{path}.{key_text}")
        elif isinstance(current, list):
            for index, nested in enumerate(current):
                visit(nested, f"{path}[{index}]")
        elif isinstance(current, str) and _SECRET_VALUE_RE.search(current):
            errors.append(f"{path} appears to contain credential material")

    visit(value, label)
    return errors


def _reject_unknown_keys(
    value: Any,
    allowed: set[str],
    label: str,
    errors: list[str],
) -> dict[str, Any]:
    if not isinstance(value, dict):
        errors.append(f"{label} must be an object")
        return {}
    unknown = sorted(set(value) - allowed)
    if unknown:
        errors.append(f"{label} contains unsupported keys: {', '.join(unknown)}")
    return value


def _parse_timestamp(value: Any, label: str, errors: list[str]) -> datetime | None:
    if not isinstance(value, str) or not value:
        errors.append(f"{label} is required")
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        errors.append(f"{label} must be an ISO-8601 timestamp")
        return None
    if parsed.tzinfo is None:
        errors.append(f"{label} must include a timezone")
        return None
    return parsed


def _valid_id(value: Any, label: str, errors: list[str]) -> str | None:
    if not isinstance(value, str) or not _ID_RE.fullmatch(value):
        errors.append(f"{label} must be a bounded provider identifier")
        return None
    return value


def _validate_target(value: Any, errors: list[str]) -> None:
    target = _reject_unknown_keys(value, {"kind", "id"}, "target", errors)
    if target.get("kind") not in {"fixture", "episode", "experiment"}:
        errors.append("target.kind must be fixture, episode, or experiment")
    if not isinstance(target.get("id"), str) or not target.get("id"):
        errors.append("target.id is required")


def _artifact_root(authorization_path: Path) -> Path:
    if authorization_path.is_symlink():
        raise ValidationError("authorization path may not be a symlink")
    try:
        return authorization_path.parent.parent.resolve(strict=True)
    except OSError as exc:
        raise ValidationError("cannot resolve the authorization artifact root") from exc


def _blueprint_root(authorization_path: Path) -> Path:
    for candidate in (authorization_path.parent, *authorization_path.parents):
        if candidate.name == "operator-blueprint-v2":
            try:
                return candidate.resolve(strict=True)
            except OSError as exc:
                raise ValidationError("cannot resolve operator-blueprint-v2 root") from exc
    raise ValidationError("authorization must live under operator-blueprint-v2")


def _reject_symlink_components(root: Path, candidate: Path, label: str) -> None:
    resolved_root = root.resolve(strict=True)
    try:
        relative = candidate.relative_to(root)
    except ValueError as exc:
        raise ValidationError(f"{label} escapes its authorized local root") from exc
    current = root
    if current.is_symlink():
        raise ValidationError(f"{label} artifact root may not be a symlink")
    for component in relative.parts:
        current = current / component
        if current.is_symlink():
            raise ValidationError(f"{label} may not traverse a symlinked path component")
        if current.exists() and current != candidate and not current.is_dir():
            raise ValidationError(f"{label} parent path is not a directory")
    try:
        resolved = candidate.resolve(strict=False)
    except OSError as exc:
        raise ValidationError(f"cannot safely resolve {label}") from exc
    if not resolved.is_relative_to(resolved_root):
        raise ValidationError(f"{label} escapes its authorized local root")


def _safe_new_path(
    root: Path,
    value: Any,
    label: str,
    required_prefix: str,
    required_suffix: str,
) -> Path:
    if not isinstance(value, str) or not value:
        raise ValidationError(f"{label} must be a non-empty relative path")
    relative = Path(value)
    if relative.is_absolute() or "." in relative.parts or ".." in relative.parts:
        raise ValidationError(f"{label} must be a safe relative path")
    if not relative.parts or relative.parts[0] != required_prefix:
        raise ValidationError(f"{label} must remain under {required_prefix}/")
    if relative.suffix.lower() != required_suffix:
        raise ValidationError(f"{label} must end in {required_suffix}")
    candidate = root / relative
    _reject_symlink_components(root, candidate, label)
    if candidate.exists():
        raise ValidationError(f"{label} already exists; immutable output may not be overwritten")
    return candidate


def _safe_existing_path(
    root: Path,
    value: Any,
    expected_sha256: Any,
    label: str,
    required_prefix: str,
    required_suffix: str,
) -> Path:
    if not isinstance(value, str) or not value:
        raise ValidationError(f"{label} must be a non-empty relative path")
    relative = Path(value)
    if relative.is_absolute() or "." in relative.parts or ".." in relative.parts:
        raise ValidationError(f"{label} must be a safe relative path")
    if not relative.parts or relative.parts[0] != required_prefix:
        raise ValidationError(f"{label} must remain under {required_prefix}/")
    if relative.suffix.lower() != required_suffix:
        raise ValidationError(f"{label} must end in {required_suffix}")
    candidate = root / relative
    _reject_symlink_components(root, candidate, label)
    if not candidate.is_file() or candidate.is_symlink():
        raise ValidationError(f"{label} must be an existing regular file")
    if not isinstance(expected_sha256, str) or sha256_file(candidate) != expected_sha256:
        raise ValidationError(f"{label} SHA-256 binding mismatch")
    return candidate


def _safe_existing_blueprint_path(
    authorization_path: Path,
    value: Any,
    expected_sha256: Any,
    label: str,
    required_suffix: str,
) -> Path:
    root = _blueprint_root(authorization_path)
    if not isinstance(value, str) or not value:
        raise ValidationError(f"{label} must be a non-empty operator-blueprint-v2-relative path")
    relative = Path(value)
    if relative.is_absolute() or "." in relative.parts or ".." in relative.parts:
        raise ValidationError(f"{label} must be a safe operator-blueprint-v2-relative path")
    if relative.suffix.lower() != required_suffix:
        raise ValidationError(f"{label} must end in {required_suffix}")
    candidate = root / relative
    _reject_symlink_components(root, candidate, label)
    if not candidate.is_file() or candidate.is_symlink():
        raise ValidationError(f"{label} must be an existing regular file")
    if not isinstance(expected_sha256, str) or sha256_file(candidate) != expected_sha256:
        raise ValidationError(f"{label} SHA-256 binding mismatch")
    return candidate


def _safe_consumption_path(authorization_path: Path, value: Any) -> Path:
    root = authorization_path.parent.resolve(strict=True)
    if not isinstance(value, str) or not value:
        raise ValidationError("consumption.record_path must be a non-empty relative path")
    relative = Path(value)
    if (
        relative.is_absolute()
        or "." in relative.parts
        or ".." in relative.parts
        or not relative.parts
        or relative.parts[0] != "consumed"
        or relative.suffix.lower() != ".json"
    ):
        raise ValidationError("consumption.record_path must be a safe consumed/*.json path")
    candidate = root / relative
    _reject_symlink_components(root, candidate, "consumption.record_path")
    if candidate.exists():
        raise ValidationError("authorization consumption record already exists")
    return candidate


def _exclusive_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    try:
        descriptor = os.open(path, flags, 0o600)
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(data)
    except FileExistsError as exc:
        raise ValidationError(f"refusing to overwrite immutable artifact: {path}") from exc
    except OSError as exc:
        raise ValidationError(f"cannot create immutable artifact: {path}") from exc


def _preview_endpoint(voice_id: str) -> str:
    encoded = urllib.parse.quote(voice_id, safe="")
    query = urllib.parse.urlencode({"output_format": OUTPUT_FORMAT})
    return f"{PREVIEW_API_ROOT}/{encoded}/remix?{query}"


def _preview_request_body(action: dict[str, Any]) -> dict[str, Any]:
    settings = action["settings"]
    return {
        "auto_generate_text": False,
        "guidance_scale": settings["guidance_scale"],
        "loudness": settings["loudness"],
        "prompt_strength": settings["prompt_strength"],
        "seed": settings["seed"],
        "stream_previews": False,
        "text": action["preview_text"],
        "voice_description": action["voice_description"],
    }


def _load_ownership_receipt(
    root: Path,
    binding: dict[str, Any],
    voice_id: str | None,
    owner: Any,
    errors: list[str],
) -> None:
    try:
        path = _safe_existing_path(
            root,
            binding.get("path"),
            binding.get("sha256"),
            "bindings.source_voice_ownership_receipt",
            "receipts",
            ".json",
        )
        receipt = read_json(path)
    except ValidationError as exc:
        errors.extend(exc.errors)
        return
    if receipt.get("target_voice_id") != voice_id:
        errors.append("ownership receipt is not bound to the incumbent voice")
    if receipt.get("voice_owner") != owner or receipt.get("consent_owner") != owner:
        errors.append("ownership receipt does not identify the approving owner")
    if receipt.get("owner_approval") is not True:
        errors.append("ownership receipt lacks owner approval")


def _validate_held_out_preview_source(
    authorization_path: Path,
    value: Any,
    preview_text: str,
    errors: list[str],
) -> None:
    source = _reject_unknown_keys(
        value,
        {
            "source_id",
            "canonical_w_path",
            "canonical_w_sha256",
            "start_token",
            "end_token",
            "token_count",
            "token_slice_sha256",
            "held_out",
            "excluded_from_scored_bakeoff",
        },
        "action.preview_source",
        errors,
    )
    if source.get("source_id") != REQUIRED_HELD_OUT_SOURCE_ID:
        errors.append(f"preview source must be held-out {REQUIRED_HELD_OUT_SOURCE_ID}")
    if source.get("start_token") != REQUIRED_HELD_OUT_START_TOKEN:
        errors.append(
            f"preview source start_token must be {REQUIRED_HELD_OUT_START_TOKEN}"
        )
    if source.get("end_token") != REQUIRED_HELD_OUT_END_TOKEN:
        errors.append(f"preview source end_token must be {REQUIRED_HELD_OUT_END_TOKEN}")
    expected_count = REQUIRED_HELD_OUT_END_TOKEN - REQUIRED_HELD_OUT_START_TOKEN
    if source.get("token_count") != expected_count:
        errors.append(f"preview source token_count must be {expected_count}")
    if source.get("held_out") is not True:
        errors.append("preview source must be explicitly held out")
    if source.get("excluded_from_scored_bakeoff") is not True:
        errors.append("preview source must be excluded from the scored provider bakeoff")
    try:
        canonical_w_path = _safe_existing_blueprint_path(
            authorization_path,
            source.get("canonical_w_path"),
            source.get("canonical_w_sha256"),
            "action.preview_source.canonical_w_path",
            ".txt",
        )
        tokens = read_canonical_w(canonical_w_path)
    except ValidationError as exc:
        errors.extend(exc.errors)
        return
    if len(tokens) < REQUIRED_HELD_OUT_END_TOKEN:
        errors.append("canonical W is shorter than the held-out preview range")
        return
    expected_tokens = tokens[
        REQUIRED_HELD_OUT_START_TOKEN:REQUIRED_HELD_OUT_END_TOKEN
    ]
    if preview_text.split() != expected_tokens:
        errors.append("preview_text does not exactly recover held-out C01B tokens [139,236)")
    identity = token_identity(expected_tokens)
    if source.get("token_slice_sha256") != identity["sha256"]:
        errors.append("held-out preview token-slice SHA-256 mismatch")


def _validate_common_authorization(
    authorization_path: Path,
    authorization: dict[str, Any],
    *,
    schema: str,
    scope: str,
    now: datetime | None,
) -> tuple[list[str], dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    errors = _scan_for_secrets(authorization)
    _reject_unknown_keys(
        authorization,
        {
            "schema_version",
            "authorization_id",
            "status",
            "approved",
            "execution_ready",
            "scope",
            "provider",
            "target",
            "action",
            "bindings",
            "requested_limits",
            "authorized_limits",
            "consumption",
            "approved_by",
            "approved_at",
            "expires_at",
            "blockers",
        },
        "authorization",
        errors,
    )
    if authorization.get("schema_version") != schema:
        errors.append(f"schema_version must be {schema}")
    if not isinstance(authorization.get("authorization_id"), str) or not authorization.get(
        "authorization_id"
    ):
        errors.append("authorization_id is required")
    if authorization.get("scope") != scope:
        errors.append(f"scope must be {scope}")
    if authorization.get("provider") != "elevenlabs":
        errors.append("provider must be elevenlabs")
    status = authorization.get("status")
    if status not in {"draft", "active"}:
        errors.append("status must be draft or active")
    _validate_target(authorization.get("target"), errors)
    action = _reject_unknown_keys(authorization.get("action"), set(), "action", [])
    bindings = _reject_unknown_keys(authorization.get("bindings"), set(), "bindings", [])
    requested = _reject_unknown_keys(
        authorization.get("requested_limits"), set(), "requested_limits", []
    )
    authorized = _reject_unknown_keys(
        authorization.get("authorized_limits"), set(), "authorized_limits", []
    )
    consumption = _reject_unknown_keys(
        authorization.get("consumption"), set(), "consumption", []
    )
    blockers = authorization.get("blockers")
    if not isinstance(blockers, list) or any(not isinstance(item, str) for item in blockers):
        errors.append("blockers must be an array of strings")
        blockers = []
    approved_at = _parse_timestamp(authorization.get("approved_at"), "approved_at", errors)
    expires_at = _parse_timestamp(authorization.get("expires_at"), "expires_at", errors)
    if approved_at is not None and expires_at is not None:
        if expires_at <= approved_at:
            errors.append("expires_at must be later than approved_at")
        if (expires_at - approved_at).total_seconds() > MAX_AUTHORIZATION_WINDOW_SECONDS:
            errors.append("authorization window may not exceed 24 hours")
    effective_now = now or datetime.now(timezone.utc)
    if effective_now.tzinfo is None:
        errors.append("validation time must include a timezone")
    elif status == "active" and expires_at is not None and expires_at <= effective_now:
        errors.append("active authorization is expired")
    owner = authorization.get("approved_by")
    if not isinstance(owner, str) or not owner:
        errors.append("approved_by is required")
    if status == "active":
        if authorization.get("approved") is not True:
            errors.append("active authorization must be explicitly approved")
        if authorization.get("execution_ready") is not True:
            errors.append("active authorization must be execution_ready")
        if blockers != []:
            errors.append("active authorization may not have unresolved blockers")
    else:
        if authorization.get("approved") is not False:
            errors.append("draft authorization must not be approved")
        if authorization.get("execution_ready") is not False:
            errors.append("draft authorization must not be execution_ready")
    return errors, action, bindings, requested, authorized | {"_consumption": consumption}


def _validate_consumption(
    authorization_path: Path,
    consumption: dict[str, Any],
    *,
    output_key: str,
    errors: list[str],
) -> Path | None:
    _reject_unknown_keys(
        consumption,
        {"status", "calls_used", output_key, "spend_used_usd", "record_path"},
        "consumption",
        errors,
    )
    if consumption.get("status") != "unconsumed":
        errors.append("authorization must be unconsumed")
    if consumption.get("calls_used") != 0 or consumption.get(output_key) != 0:
        errors.append("authorization consumption counters must be zero")
    if consumption.get("spend_used_usd") != 0:
        errors.append("authorization spend counter must be zero")
    try:
        return _safe_consumption_path(authorization_path, consumption.get("record_path"))
    except ValidationError as exc:
        errors.extend(exc.errors)
        return None


def _validate_preview_authorization(
    authorization_path: Path,
    *,
    now: datetime | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    authorization = read_json(authorization_path)
    errors, action, bindings, requested, common = _validate_common_authorization(
        authorization_path,
        authorization,
        schema=PREVIEW_AUTH_SCHEMA,
        scope=PREVIEW_SCOPE,
        now=now,
    )
    authorized = {key: value for key, value in common.items() if key != "_consumption"}
    consumption = common.get("_consumption", {})
    _reject_unknown_keys(
        action,
        {
            "kind",
            "source_voice_id",
            "source_voice_owner",
            "source_voice_owned_by_approver",
            "endpoint",
            "voice_description",
            "preview_text",
            "preview_source",
            "settings",
            "eligibility_check",
            "preview_destinations",
            "preview_receipt_destination",
            "failure_receipt_destination",
            "automatic_preview_selection_permitted",
            "voice_save_permitted",
            "source_voice_mutation_permitted",
            "retries_permitted",
            "redirects_permitted",
            "credential_env",
        },
        "action",
        errors,
    )
    _reject_unknown_keys(
        bindings,
        {
            "voice_description_sha256",
            "preview_text_sha256",
            "request_body_sha256",
            "source_voice_ownership_receipt",
        },
        "bindings",
        errors,
    )
    limit_keys = {
        "max_calls",
        "max_prompt_characters",
        "max_preview_text_characters",
        "max_billable_characters",
        "max_outputs",
        "max_response_bytes",
        "max_total_audio_bytes",
        "max_total_duration_seconds",
        "max_spend_usd",
    }
    _reject_unknown_keys(requested, limit_keys, "requested_limits", errors)
    _reject_unknown_keys(authorized, limit_keys, "authorized_limits", errors)
    if requested != authorized:
        errors.append("requested_limits and authorized_limits must be exactly equal")

    if action.get("kind") != "remix_owned_voice_preview":
        errors.append("action.kind must be remix_owned_voice_preview")
    voice_id = _valid_id(action.get("source_voice_id"), "action.source_voice_id", errors)
    owner = authorization.get("approved_by")
    if action.get("source_voice_owner") != owner:
        errors.append("source voice owner must be the approving owner")
    if action.get("source_voice_owned_by_approver") is not True:
        errors.append("source voice must be explicitly owned by the approving owner")
    expected_endpoint = _preview_endpoint(voice_id or "invalid")
    if action.get("endpoint") != expected_endpoint:
        errors.append("preview endpoint must exactly match the official bound-voice remix endpoint")
    prompt = action.get("voice_description")
    text = action.get("preview_text")
    if (
        not isinstance(prompt, str)
        or not (5 <= len(prompt) <= MAX_REMIX_PROMPT_CHARACTERS)
        or not prompt.strip()
    ):
        errors.append(
            f"voice_description must contain 5 through {MAX_REMIX_PROMPT_CHARACTERS} exact characters"
        )
        prompt = ""
    if not isinstance(text, str) or not (100 <= len(text) <= 1000) or not text.strip():
        errors.append("preview_text must contain 100 through 1000 exact characters")
        text = ""
    if bindings.get("voice_description_sha256") != sha256_bytes(prompt.encode("utf-8")):
        errors.append("voice_description SHA-256 binding mismatch")
    if bindings.get("preview_text_sha256") != sha256_bytes(text.encode("utf-8")):
        errors.append("preview_text SHA-256 binding mismatch")
    _validate_held_out_preview_source(authorization_path, action.get("preview_source"), text, errors)
    ownership_binding = _reject_unknown_keys(
        bindings.get("source_voice_ownership_receipt"),
        {"path", "sha256"},
        "bindings.source_voice_ownership_receipt",
        errors,
    )
    try:
        root = _artifact_root(authorization_path)
    except ValidationError as exc:
        errors.extend(exc.errors)
        root = authorization_path.parent.parent
    _load_ownership_receipt(root, ownership_binding, voice_id, owner, errors)

    settings = _reject_unknown_keys(
        action.get("settings"),
        {
            "auto_generate_text",
            "loudness",
            "seed",
            "guidance_scale",
            "stream_previews",
            "prompt_strength",
            "output_format",
        },
        "action.settings",
        errors,
    )
    if settings.get("auto_generate_text") is not False:
        errors.append("auto_generate_text must be false for exact preview text")
    if settings.get("stream_previews") is not False:
        errors.append("stream_previews must be false so all previews are preserved atomically")
    if settings.get("output_format") != OUTPUT_FORMAT:
        errors.append(f"output_format must be {OUTPUT_FORMAT}")
    strength = settings.get("prompt_strength")
    if not _is_number(strength) or not MIN_PROMPT_STRENGTH <= float(strength) <= MAX_PROMPT_STRENGTH:
        errors.append("prompt_strength must be between 0.20 and 0.30 inclusive")
    seed = settings.get("seed")
    if not isinstance(seed, int) or isinstance(seed, bool) or not 0 <= seed <= 2_147_483_647:
        errors.append("seed must be a fixed integer from 0 through 2147483647")
    loudness = settings.get("loudness")
    if not _is_number(loudness) or not -1 <= float(loudness) <= 1:
        errors.append("loudness must be between -1 and 1")
    guidance = settings.get("guidance_scale")
    if not _is_number(guidance) or not 0 <= float(guidance) <= 100:
        errors.append("guidance_scale must be between 0 and 100")

    required_false = (
        "automatic_preview_selection_permitted",
        "voice_save_permitted",
        "source_voice_mutation_permitted",
        "retries_permitted",
        "redirects_permitted",
    )
    for field in required_false:
        if action.get(field) is not False:
            errors.append(f"action.{field} must be false")
    if action.get("credential_env") != "ELEVENLABS_API_KEY":
        errors.append("credential_env must be ELEVENLABS_API_KEY")
    eligibility = _reject_unknown_keys(
        action.get("eligibility_check"),
        {
            "mode",
            "voice_metadata_get_permitted",
            "subscription_get_permitted",
            "user_get_permitted",
        },
        "action.eligibility_check",
        errors,
    )
    if eligibility != {
        "mode": "provider_post_rejection_only",
        "voice_metadata_get_permitted": False,
        "subscription_get_permitted": False,
        "user_get_permitted": False,
    }:
        errors.append(
            "eligibility_check must make no GET calls and must rely only on remix POST rejection"
        )

    destinations = action.get("preview_destinations")
    if not isinstance(destinations, list) or not destinations:
        errors.append("preview_destinations must be a non-empty array")
        destinations = []
    if len(destinations) != len(set(item for item in destinations if isinstance(item, str))):
        errors.append("preview_destinations must be unique")
    max_outputs = authorized.get("max_outputs")
    if (
        not isinstance(max_outputs, int)
        or isinstance(max_outputs, bool)
        or not 1 <= max_outputs <= MAX_PREVIEW_OUTPUTS
    ):
        errors.append(f"max_outputs must be between 1 and {MAX_PREVIEW_OUTPUTS}")
    elif len(destinations) != max_outputs:
        errors.append("preview_destinations must exactly match max_outputs")

    exact_caps = {
        "max_calls": 1,
        "max_prompt_characters": len(prompt),
        "max_preview_text_characters": len(text),
        "max_billable_characters": len(text),
    }
    for field, expected in exact_caps.items():
        if authorized.get(field) != expected:
            errors.append(f"authorized_limits.{field} must be exactly {expected}")
    bounded_limits = (
        ("max_response_bytes", 1, MAX_PREVIEW_RESPONSE_BYTES),
        ("max_total_audio_bytes", 1, MAX_PREVIEW_AUDIO_BYTES),
    )
    for field, minimum, maximum in bounded_limits:
        value = authorized.get(field)
        if not isinstance(value, int) or isinstance(value, bool) or not minimum <= value <= maximum:
            errors.append(f"authorized_limits.{field} must be between {minimum} and {maximum}")
    if (
        isinstance(authorized.get("max_response_bytes"), int)
        and isinstance(authorized.get("max_total_audio_bytes"), int)
        and authorized["max_total_audio_bytes"] > authorized["max_response_bytes"]
    ):
        errors.append("max_total_audio_bytes may not exceed max_response_bytes")
    duration_cap = authorized.get("max_total_duration_seconds")
    if not _is_number(duration_cap) or not 0 < float(duration_cap) <= MAX_PREVIEW_DURATION_SECONDS:
        errors.append(
            f"max_total_duration_seconds must be positive and at most {MAX_PREVIEW_DURATION_SECONDS:g}"
        )
    spend_cap = authorized.get("max_spend_usd")
    if not _is_number(spend_cap) or not 0 <= float(spend_cap) <= 25:
        errors.append("max_spend_usd must be a finite exact cap from 0 through 25")

    preview_paths: list[Path] = []
    for index, destination in enumerate(destinations):
        try:
            preview_paths.append(
                _safe_new_path(
                    root,
                    destination,
                    f"action.preview_destinations[{index}]",
                    "local-media",
                    ".mp3",
                )
            )
        except ValidationError as exc:
            errors.extend(exc.errors)
    receipt_path: Path | None = None
    failure_path: Path | None = None
    try:
        receipt_path = _safe_new_path(
            root,
            action.get("preview_receipt_destination"),
            "action.preview_receipt_destination",
            "receipts",
            ".json",
        )
    except ValidationError as exc:
        errors.extend(exc.errors)
    try:
        failure_path = _safe_new_path(
            root,
            action.get("failure_receipt_destination"),
            "action.failure_receipt_destination",
            "receipts",
            ".json",
        )
    except ValidationError as exc:
        errors.extend(exc.errors)
    consumption_path = _validate_consumption(
        authorization_path,
        consumption,
        output_key="outputs_used",
        errors=errors,
    )
    all_paths = [*preview_paths]
    all_paths.extend(path for path in (receipt_path, failure_path, consumption_path) if path)
    if len({path.resolve(strict=False) for path in all_paths}) != len(all_paths):
        errors.append("preview outputs, receipts, and consumption record must use distinct paths")
    if errors:
        raise ValidationError(errors)
    body = _preview_request_body(action)
    body_bytes = _canonical_body(body)
    if bindings.get("request_body_sha256") != sha256_bytes(body_bytes):
        raise ValidationError("full canonical preview request body SHA-256 binding mismatch")
    return authorization, {
        "root": root,
        "preview_paths": preview_paths,
        "preview_receipt_path": receipt_path,
        "failure_receipt_path": failure_path,
        "consumption_path": consumption_path,
        "request_body": body,
        "request_bytes": body_bytes,
    }


def validate_voice_remix_preview_authorization(
    authorization_path: Path,
    *,
    now: datetime | None = None,
) -> dict[str, Any]:
    """Validate and compile one preview authorization without reading credentials."""

    authorization, preflight = _validate_preview_authorization(authorization_path, now=now)
    action = authorization["action"]
    return {
        "valid": True,
        "schema_version": PREVIEW_AUTH_SCHEMA,
        "authorization_id": authorization["authorization_id"],
        "status": authorization["status"],
        "execution_ready": authorization["status"] == "active",
        "scope": PREVIEW_SCOPE,
        "source_voice_id": action["source_voice_id"],
        "request": {
            "method": "POST",
            "endpoint": action["endpoint"],
            "body": preflight["request_body"],
            "body_sha256": sha256_bytes(preflight["request_bytes"]),
            "prompt_characters": len(action["voice_description"]),
            "preview_text_characters": len(action["preview_text"]),
            "billable_characters": len(action["preview_text"]),
        },
        "authorized_limits": authorization["authorized_limits"],
        "preview_destinations": [str(path) for path in preflight["preview_paths"]],
        "preview_receipt": str(preflight["preview_receipt_path"]),
        "failure_receipt": str(preflight["failure_receipt_path"]),
        "consumption_record": str(preflight["consumption_path"]),
        "automatic_selection_permitted": False,
        "voice_save_permitted": False,
        "source_voice_mutation_permitted": False,
        "eligibility_check": {
            "mode": "provider_post_rejection_only",
            "provider_get_calls_permitted": 0,
            "user_endpoint_permitted": False,
            "notice": (
                "Voice ownership and plan eligibility are not discovered here; "
                "the single remix POST must reject an ineligible source or account."
            ),
        },
    }


def dry_run_voice_remix_preview(
    authorization_path: Path,
    *,
    now: datetime | None = None,
) -> dict[str, Any]:
    """Return the exact bounded preview request; never read a credential or call a provider."""

    validation = validate_voice_remix_preview_authorization(authorization_path, now=now)
    return {
        "schema_version": PREVIEW_RECEIPT_SCHEMA,
        "mode": "dry-run",
        "network_called": False,
        "credentials_accessed": False,
        "provider_calls_made": 0,
        "audio_files_created": 0,
        "authorization_validation": validation,
        "selection_status": "not_generated",
        "notice": (
            "No provider action occurred. Execution requires this exact active, unconsumed "
            "preview authorization; saving any result requires a different authorization."
        ),
    }


def _header_map(headers: Any) -> dict[str, str]:
    try:
        return {str(key).lower(): str(value) for key, value in headers.items()}
    except (AttributeError, TypeError, ValueError):
        return {}


def _provider_identifiers(headers: dict[str, str], credential: str) -> dict[str, str]:
    identifiers: dict[str, str] = {}
    for name in _REQUEST_ID_HEADERS:
        value = headers.get(name)
        if not value or credential in value:
            continue
        identifiers[name] = value[:1024]
    return identifiers


def _credential_from_environment() -> str:
    credential = os.environ.get("ELEVENLABS_API_KEY")
    if credential is None:
        raise ValidationError("ELEVENLABS_API_KEY is required only for authorized execution")
    if (
        not credential
        or credential != credential.strip()
        or any(character in credential for character in ("\r", "\n", "\x00"))
        or any(not character.isprintable() for character in credential)
        or not 16 <= len(credential) <= 1024
    ):
        raise ValidationError("ELEVENLABS_API_KEY is malformed; authorization remains unconsumed")
    return credential


def _post_json(
    endpoint: str,
    body: bytes,
    credential: str,
    *,
    timeout: float,
    max_response_bytes: int,
) -> _HttpResponse:
    request = urllib.request.Request(
        endpoint,
        data=body,
        method="POST",
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "xi-api-key": credential,
        },
    )
    opener = urllib.request.build_opener(_NoRedirect())
    try:
        with opener.open(request, timeout=timeout) as response:
            final_url = response.geturl()
            if final_url != endpoint:
                raise _ProviderFailure("redirect_or_endpoint_drift")
            headers = _header_map(response.headers)
            mime = headers.get("content-type", "").split(";", 1)[0].strip().lower()
            if mime != "application/json":
                raise _ProviderFailure("response_content_type_not_json")
            content_length = headers.get("content-length")
            if content_length is not None:
                try:
                    declared = int(content_length)
                except ValueError as exc:
                    raise _ProviderFailure("response_content_length_invalid") from exc
                if declared < 0 or declared > max_response_bytes:
                    raise _ProviderFailure("response_size_cap_exceeded")
            data = response.read(max_response_bytes + 1)
            if len(data) > max_response_bytes:
                raise _ProviderFailure("response_size_cap_exceeded")
            if not data:
                raise _ProviderFailure("response_empty")
            return _HttpResponse(
                data=data,
                mime_type=mime,
                headers=headers,
                provider_identifiers=_provider_identifiers(headers, credential),
            )
    except _ProviderFailure:
        raise
    except urllib.error.HTTPError as exc:
        identifiers = _provider_identifiers(_header_map(exc.headers), credential)
        code = "redirect_forbidden" if 300 <= exc.code < 400 else f"http_{exc.code}"
        raise _ProviderFailure(
            code,
            http_status=exc.code,
            provider_identifiers=identifiers,
        ) from exc
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        raise _ProviderFailure("transport_failure") from exc


def _validated_character_cost(
    headers: dict[str, str],
    *,
    maximum: int | None,
    required: bool,
) -> int | None:
    raw = headers.get("character-cost")
    if raw is None:
        if required:
            raise _ProviderFailure("character_cost_header_missing")
        return None
    if not raw.isascii() or not raw.isdecimal():
        raise _ProviderFailure("character_cost_header_invalid")
    value = int(raw)
    if value < 0:
        raise _ProviderFailure("character_cost_header_invalid")
    if maximum is not None and value > maximum:
        raise _ProviderFailure("character_cost_cap_exceeded")
    return value


def _consume_authorization(
    authorization_path: Path,
    authorization: dict[str, Any],
    consumption_path: Path,
    *,
    scope: str,
    authorized_limits: dict[str, Any],
) -> None:
    record = {
        "schema_version": CONSUMPTION_SCHEMA,
        "authorization_id": authorization["authorization_id"],
        "authorization_sha256": sha256_file(authorization_path),
        "scope": scope,
        "status": "consumed",
        "consumed_before_network": True,
        "consumed_at": _utc_now(),
        "reason": "one-shot provider action started; retry requires new authorization",
        "authorized_limits": authorized_limits,
    }
    _exclusive_write(consumption_path, _json_bytes(record))


def _write_failure_receipt(
    path: Path,
    *,
    authorization_path: Path,
    authorization: dict[str, Any],
    scope: str,
    stage: str,
    reason: str,
    attempted_calls: int,
    http_status: int | None = None,
    provider_identifiers: dict[str, str] | None = None,
) -> None:
    receipt = {
        "schema_version": (
            PREVIEW_RECEIPT_SCHEMA if scope == PREVIEW_SCOPE else SAVE_RECEIPT_SCHEMA
        ),
        "outcome": "failed_closed",
        "stage": stage,
        "reason": reason,
        "authorization_id": authorization["authorization_id"],
        "authorization_sha256": sha256_file(authorization_path),
        "scope": scope,
        "attempted_calls": attempted_calls,
        "http_status": http_status,
        "provider_identifiers": provider_identifiers or {},
        "failed_at": _utc_now(),
        "retry_permitted": False,
        "source_voice_modified": False,
        "voice_created": False,
        "owner_decision": "pending" if scope == PREVIEW_SCOPE else "not_completed",
        "raw_provider_payload_stored": False,
    }
    _exclusive_write(path, _json_bytes(receipt))


def _decode_preview_response(
    response: _HttpResponse,
    authorization: dict[str, Any],
) -> list[dict[str, Any]]:
    try:
        payload = json.loads(response.data.decode("utf-8"))
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise _ProviderFailure("preview_response_json_invalid") from exc
    if not isinstance(payload, dict) or set(payload) != {"previews", "text"}:
        raise _ProviderFailure("preview_response_schema_drift")
    if payload.get("text") != authorization["action"]["preview_text"]:
        raise _ProviderFailure("preview_response_text_mismatch")
    previews = payload.get("previews")
    max_outputs = authorization["authorized_limits"]["max_outputs"]
    if not isinstance(previews, list) or not previews:
        raise _ProviderFailure("preview_response_has_no_previews")
    if len(previews) > max_outputs:
        raise _ProviderFailure("preview_output_cap_exceeded")
    decoded: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    total_bytes = 0
    total_duration = 0.0
    for index, preview in enumerate(previews):
        if not isinstance(preview, dict):
            raise _ProviderFailure("preview_entry_invalid")
        required = {
            "audio_base_64",
            "generated_voice_id",
            "media_type",
            "duration_secs",
        }
        if not required.issubset(preview) or not set(preview).issubset(required | {"language"}):
            raise _ProviderFailure("preview_entry_schema_drift")
        generated_id = preview.get("generated_voice_id")
        if not isinstance(generated_id, str) or not _ID_RE.fullmatch(generated_id):
            raise _ProviderFailure("preview_generated_voice_id_invalid")
        if generated_id in seen_ids:
            raise _ProviderFailure("preview_generated_voice_id_duplicate")
        seen_ids.add(generated_id)
        media_type = preview.get("media_type")
        if media_type not in {"audio/mpeg", "audio/mp3"}:
            raise _ProviderFailure("preview_media_type_not_mp3")
        encoded = preview.get("audio_base_64")
        if not isinstance(encoded, str) or not encoded:
            raise _ProviderFailure("preview_audio_base64_missing")
        try:
            audio = base64.b64decode(encoded, validate=True)
        except (binascii.Error, ValueError) as exc:
            raise _ProviderFailure("preview_audio_base64_invalid") from exc
        if not audio or not (
            audio.startswith(b"ID3")
            or (len(audio) >= 2 and audio[0] == 0xFF and (audio[1] & 0xE0) == 0xE0)
        ):
            raise _ProviderFailure("preview_audio_signature_not_mp3")
        duration = preview.get("duration_secs")
        if not _is_number(duration) or float(duration) <= 0:
            raise _ProviderFailure("preview_duration_invalid")
        language = preview.get("language")
        if language is not None and (
            not isinstance(language, str)
            or len(language) > 32
            or any(not character.isprintable() for character in language)
        ):
            raise _ProviderFailure("preview_language_invalid")
        total_bytes += len(audio)
        total_duration += float(duration)
        if total_bytes > authorization["authorized_limits"]["max_total_audio_bytes"]:
            raise _ProviderFailure("preview_audio_byte_cap_exceeded")
        if total_duration > authorization["authorized_limits"]["max_total_duration_seconds"]:
            raise _ProviderFailure("preview_duration_cap_exceeded")
        decoded.append(
            {
                "index": index,
                "generated_voice_id": generated_id,
                "media_type": media_type,
                "duration_seconds": float(duration),
                "language": language,
                "audio": audio,
            }
        )
    return decoded


def execute_voice_remix_preview(
    authorization_path: Path,
    *,
    timeout: float = 60.0,
) -> dict[str, Any]:
    """Consume one active authorization and make exactly one remix-preview request."""

    if not _is_number(timeout) or float(timeout) <= 0 or float(timeout) > 300:
        raise ValidationError("timeout must be positive and no greater than 300 seconds")
    authorization, preflight = _validate_preview_authorization(authorization_path)
    if authorization["status"] != "active":
        raise ValidationError("preview execution requires an active authorization")
    credential = _credential_from_environment()
    _consume_authorization(
        authorization_path,
        authorization,
        preflight["consumption_path"],
        scope=PREVIEW_SCOPE,
        authorized_limits=authorization["authorized_limits"],
    )
    attempted_calls = 1
    try:
        response = _post_json(
            authorization["action"]["endpoint"],
            preflight["request_bytes"],
            credential,
            timeout=float(timeout),
            max_response_bytes=authorization["authorized_limits"]["max_response_bytes"],
        )
        character_cost = _validated_character_cost(
            response.headers,
            maximum=authorization["authorized_limits"]["max_billable_characters"],
            required=False,
        )
        previews = _decode_preview_response(response, authorization)
    except _ProviderFailure as exc:
        _write_failure_receipt(
            preflight["failure_receipt_path"],
            authorization_path=authorization_path,
            authorization=authorization,
            scope=PREVIEW_SCOPE,
            stage="provider_response",
            reason=exc.code,
            attempted_calls=attempted_calls,
            http_status=exc.http_status,
            provider_identifiers=exc.provider_identifiers,
        )
        raise ValidationError(f"ElevenLabs remix preview failed closed: {exc.code}") from exc

    written: list[dict[str, Any]] = []
    try:
        for index, preview in enumerate(previews):
            path = preflight["preview_paths"][index]
            destination = authorization["action"]["preview_destinations"][index]
            _exclusive_write(path, preview["audio"])
            written.append(
                {
                    "index": preview["index"],
                    "generated_voice_id": preview["generated_voice_id"],
                    "audio_path": destination,
                    "audio_sha256": sha256_file(path),
                    "byte_count": len(preview["audio"]),
                    "media_type": preview["media_type"],
                    "container": "mp3",
                    "requested_output_format": OUTPUT_FORMAT,
                    "duration_seconds": preview["duration_seconds"],
                    "language": preview["language"],
                    "owner_only_mode": "0600",
                }
            )
    except (ValidationError, ValueError) as exc:
        _write_failure_receipt(
            preflight["failure_receipt_path"],
            authorization_path=authorization_path,
            authorization=authorization,
            scope=PREVIEW_SCOPE,
            stage="local_storage",
            reason="preview_storage_incomplete",
            attempted_calls=attempted_calls,
            provider_identifiers=response.provider_identifiers,
        )
        raise ValidationError("ElevenLabs remix preview failed closed: preview_storage_incomplete") from exc

    receipt = {
        "schema_version": PREVIEW_RECEIPT_SCHEMA,
        "outcome": "generated_pending_owner_selection",
        "authorization_id": authorization["authorization_id"],
        "authorization_sha256": sha256_file(authorization_path),
        "authorization_consumption_record": authorization["consumption"]["record_path"],
        "authorization_consumption_sha256": sha256_file(preflight["consumption_path"]),
        "provider": "elevenlabs",
        "scope": PREVIEW_SCOPE,
        "source_voice_id": authorization["action"]["source_voice_id"],
        "source_voice_owner": authorization["action"]["source_voice_owner"],
        "request": {
            "method": "POST",
            "endpoint": authorization["action"]["endpoint"],
            "body_sha256": sha256_bytes(preflight["request_bytes"]),
            "voice_description_sha256": authorization["bindings"]["voice_description_sha256"],
            "preview_text_sha256": authorization["bindings"]["preview_text_sha256"],
            "prompt_characters": len(authorization["action"]["voice_description"]),
            "preview_text_characters": len(authorization["action"]["preview_text"]),
            "billable_characters": len(authorization["action"]["preview_text"]),
            "settings": authorization["action"]["settings"],
        },
        "provider_identifiers": response.provider_identifiers,
        "provider_character_cost": {
            "header": "character-cost",
            "value": character_cost,
            "unit": "provider_character_units" if character_cost is not None else "not_reported",
            "is_usd": False,
        },
        "provider_calls_made": 1,
        "preview_count": len(written),
        "previews": written,
        "selection": {
            "status": "owner_decision_pending",
            "selected_generated_voice_id": None,
            "automatic_selection_permitted": False,
            "all_provider_previews_preserved": True,
        },
        "source_voice_modified": False,
        "voice_created": False,
        "save_authorized": False,
        "eligibility_verification": {
            "mode": "provider_post_rejection_only",
            "metadata_get_called": False,
            "subscription_get_called": False,
            "user_get_called": False,
            "is_owner_preflight_confirmed_by_provider": False,
        },
        "owner_review_required": True,
        "spend": {
            "authorized_max_usd": authorization["authorized_limits"]["max_spend_usd"],
            "actual_usd": None,
            "provider_response_reported_spend": False,
            "provider_enforced_usd_cap": False,
            "status": "modeled_or_unknown",
            "hard_bounds": (
                "one_call_and_exact_preview_text; character-cost validated when reported"
            ),
        },
        "generated_at": _utc_now(),
    }
    _exclusive_write(preflight["preview_receipt_path"], _json_bytes(receipt))
    return {
        "schema_version": PREVIEW_RECEIPT_SCHEMA,
        "mode": "execute",
        "network_called": True,
        "provider_calls_made": 1,
        "provider_character_cost": character_cost,
        "preview_count": len(written),
        "preview_receipt": str(preflight["preview_receipt_path"]),
        "preview_receipt_sha256": sha256_file(preflight["preview_receipt_path"]),
        "previews": written,
        "selection_status": "owner_decision_pending",
        "selected_generated_voice_id": None,
        "source_voice_modified": False,
        "voice_created": False,
        "save_authorized": False,
        "consumption_record": str(preflight["consumption_path"]),
    }


def _load_preview_and_selection(
    root: Path,
    action: dict[str, Any],
    authorization: dict[str, Any],
    errors: list[str],
) -> tuple[dict[str, Any], dict[str, Any]]:
    try:
        preview_path = _safe_existing_path(
            root,
            action.get("preview_receipt_path"),
            action.get("preview_receipt_sha256"),
            "action.preview_receipt_path",
            "receipts",
            ".json",
        )
        preview = read_json(preview_path)
    except ValidationError as exc:
        errors.extend(exc.errors)
        return {}, {}
    try:
        selection_path = _safe_existing_path(
            root,
            action.get("owner_selection_record_path"),
            action.get("owner_selection_record_sha256"),
            "action.owner_selection_record_path",
            "receipts",
            ".json",
        )
        selection = read_json(selection_path)
    except ValidationError as exc:
        errors.extend(exc.errors)
        return preview, {}
    if preview.get("schema_version") != PREVIEW_RECEIPT_SCHEMA:
        errors.append("bound preview receipt has the wrong schema")
    if preview.get("outcome") != "generated_pending_owner_selection":
        errors.append("bound preview receipt is not awaiting owner selection")
    if preview.get("source_voice_id") != action.get("source_voice_id"):
        errors.append("bound preview receipt source voice mismatch")
    preview_selection = preview.get("selection")
    if not isinstance(preview_selection, dict) or preview_selection.get("status") != "owner_decision_pending":
        errors.append("bound preview receipt is not in owner_decision_pending state")
    if preview.get("voice_created") is not False or preview.get("source_voice_modified") is not False:
        errors.append("bound preview receipt has unsafe voice state")
    previews = preview.get("previews")
    if not isinstance(previews, list) or not previews:
        errors.append("bound preview receipt contains no previews")
        previews = []
    selected_id = action.get("selected_generated_voice_id")
    matches = [item for item in previews if isinstance(item, dict) and item.get("generated_voice_id") == selected_id]
    if len(matches) != 1:
        errors.append("selected_generated_voice_id must match exactly one preserved preview")
    elif matches[0].get("audio_sha256") != action.get("selected_audio_sha256"):
        errors.append("selected preview audio SHA-256 binding mismatch")
    elif isinstance(matches[0].get("audio_path"), str):
        try:
            audio_path = _safe_existing_path(
                root,
                matches[0]["audio_path"],
                matches[0]["audio_sha256"],
                "selected preview audio",
                "local-media",
                ".mp3",
            )
            if audio_path.stat().st_mode & 0o077:
                errors.append("selected preview audio is not owner-only")
        except ValidationError as exc:
            errors.extend(exc.errors)
    else:
        errors.append("selected preview audio path is invalid")

    _reject_unknown_keys(
        selection,
        {
            "schema_version",
            "preview_receipt_sha256",
            "source_voice_id",
            "selected_generated_voice_id",
            "selected_audio_sha256",
            "selected_by",
            "selected_at",
            "owner_approved_save",
            "voice_name",
            "voice_description",
        },
        "owner_selection_record",
        errors,
    )
    if selection.get("schema_version") != OWNER_SELECTION_SCHEMA:
        errors.append(f"owner selection schema must be {OWNER_SELECTION_SCHEMA}")
    if selection.get("preview_receipt_sha256") != action.get("preview_receipt_sha256"):
        errors.append("owner selection is not bound to the preview receipt")
    exact_selection_fields = {
        "source_voice_id": action.get("source_voice_id"),
        "selected_generated_voice_id": selected_id,
        "selected_audio_sha256": action.get("selected_audio_sha256"),
        "selected_by": authorization.get("approved_by"),
        "owner_approved_save": True,
        "voice_name": action.get("voice_name"),
        "voice_description": action.get("voice_description"),
    }
    for field, expected in exact_selection_fields.items():
        if selection.get(field) != expected:
            errors.append(f"owner selection {field} mismatch")
    selected_at = _parse_timestamp(selection.get("selected_at"), "owner_selection_record.selected_at", errors)
    approved_at = _parse_timestamp(authorization.get("approved_at"), "approved_at", [])
    if selected_at is not None and approved_at is not None and selected_at > approved_at:
        errors.append("save authorization must be approved after the owner selection")
    return preview, selection


def _save_request_body(action: dict[str, Any]) -> dict[str, Any]:
    body: dict[str, Any] = {
        "generated_voice_id": action["selected_generated_voice_id"],
        "voice_description": action["voice_description"],
        "voice_name": action["voice_name"],
    }
    if action.get("labels"):
        body["labels"] = action["labels"]
    if action.get("played_not_selected_voice_ids"):
        body["played_not_selected_voice_ids"] = action["played_not_selected_voice_ids"]
    return body


def _validate_save_authorization(
    authorization_path: Path,
    *,
    now: datetime | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    authorization = read_json(authorization_path)
    errors, action, bindings, requested, common = _validate_common_authorization(
        authorization_path,
        authorization,
        schema=SAVE_AUTH_SCHEMA,
        scope=SAVE_SCOPE,
        now=now,
    )
    authorized = {key: value for key, value in common.items() if key != "_consumption"}
    consumption = common.get("_consumption", {})
    _reject_unknown_keys(
        action,
        {
            "kind",
            "source_voice_id",
            "source_voice_owner",
            "source_voice_owned_by_approver",
            "endpoint",
            "preview_receipt_path",
            "preview_receipt_sha256",
            "owner_selection_record_path",
            "owner_selection_record_sha256",
            "selected_generated_voice_id",
            "selected_audio_sha256",
            "voice_name",
            "voice_description",
            "labels",
            "played_not_selected_voice_ids",
            "save_receipt_destination",
            "failure_receipt_destination",
            "new_voice_required",
            "source_voice_mutation_permitted",
            "retries_permitted",
            "redirects_permitted",
            "credential_env",
        },
        "action",
        errors,
    )
    _reject_unknown_keys(
        bindings,
        {"source_voice_ownership_receipt", "request_body_sha256"},
        "bindings",
        errors,
    )
    limit_keys = {"max_calls", "max_voices_created", "max_response_bytes", "max_spend_usd"}
    _reject_unknown_keys(requested, limit_keys, "requested_limits", errors)
    _reject_unknown_keys(authorized, limit_keys, "authorized_limits", errors)
    if requested != authorized:
        errors.append("requested_limits and authorized_limits must be exactly equal")
    if action.get("kind") != "create_new_voice_from_owner_selected_preview":
        errors.append("action.kind must be create_new_voice_from_owner_selected_preview")
    source_voice_id = _valid_id(action.get("source_voice_id"), "action.source_voice_id", errors)
    _valid_id(
        action.get("selected_generated_voice_id"),
        "action.selected_generated_voice_id",
        errors,
    )
    owner = authorization.get("approved_by")
    if action.get("source_voice_owner") != owner:
        errors.append("source voice owner must be the approving owner")
    if action.get("source_voice_owned_by_approver") is not True:
        errors.append("source voice must be explicitly owned by the approving owner")
    if action.get("endpoint") != SAVE_ENDPOINT:
        errors.append("save endpoint must exactly match the official create-from-preview endpoint")
    voice_name = action.get("voice_name")
    description = action.get("voice_description")
    if not isinstance(voice_name, str) or not 1 <= len(voice_name) <= 100 or not voice_name.strip():
        errors.append("voice_name must contain 1 through 100 exact characters")
    if not isinstance(description, str) or not 20 <= len(description) <= 1000 or not description.strip():
        errors.append("voice_description must contain 20 through 1000 exact characters")
    labels = action.get("labels")
    if not isinstance(labels, dict) or len(labels) > 10:
        errors.append("labels must be an object with at most 10 entries")
        labels = {}
    for key, value in labels.items():
        if (
            not isinstance(key, str)
            or not isinstance(value, str)
            or not key
            or not value
            or len(key) > 64
            or len(value) > 128
            or _SECRET_KEY_RE.search(key)
            or _SECRET_VALUE_RE.search(value)
        ):
            errors.append("labels must contain only bounded, credential-free strings")
            break
    played = action.get("played_not_selected_voice_ids")
    if played != []:
        errors.append("played_not_selected_voice_ids must be empty; review telemetry disclosure is prohibited")
        played = []
    for field in ("source_voice_mutation_permitted", "retries_permitted", "redirects_permitted"):
        if action.get(field) is not False:
            errors.append(f"action.{field} must be false")
    if action.get("new_voice_required") is not True:
        errors.append("new_voice_required must be true")
    if action.get("credential_env") != "ELEVENLABS_API_KEY":
        errors.append("credential_env must be ELEVENLABS_API_KEY")
    ownership_binding = _reject_unknown_keys(
        bindings.get("source_voice_ownership_receipt"),
        {"path", "sha256"},
        "bindings.source_voice_ownership_receipt",
        errors,
    )
    try:
        root = _artifact_root(authorization_path)
    except ValidationError as exc:
        errors.extend(exc.errors)
        root = authorization_path.parent.parent
    _load_ownership_receipt(root, ownership_binding, source_voice_id, owner, errors)
    preview, selection = _load_preview_and_selection(root, action, authorization, errors)

    exact_limits = {"max_calls": 1, "max_voices_created": 1}
    for field, expected in exact_limits.items():
        if authorized.get(field) != expected:
            errors.append(f"authorized_limits.{field} must be exactly {expected}")
    response_cap = authorized.get("max_response_bytes")
    if (
        not isinstance(response_cap, int)
        or isinstance(response_cap, bool)
        or not 1 <= response_cap <= MAX_SAVE_RESPONSE_BYTES
    ):
        errors.append(
            f"max_response_bytes must be between 1 and {MAX_SAVE_RESPONSE_BYTES}"
        )
    spend_cap = authorized.get("max_spend_usd")
    if not _is_number(spend_cap) or not 0 <= float(spend_cap) <= 25:
        errors.append("max_spend_usd must be a finite exact cap from 0 through 25")

    receipt_path: Path | None = None
    failure_path: Path | None = None
    try:
        receipt_path = _safe_new_path(
            root,
            action.get("save_receipt_destination"),
            "action.save_receipt_destination",
            "receipts",
            ".json",
        )
    except ValidationError as exc:
        errors.extend(exc.errors)
    try:
        failure_path = _safe_new_path(
            root,
            action.get("failure_receipt_destination"),
            "action.failure_receipt_destination",
            "receipts",
            ".json",
        )
    except ValidationError as exc:
        errors.extend(exc.errors)
    consumption_path = _validate_consumption(
        authorization_path,
        consumption,
        output_key="voices_created",
        errors=errors,
    )
    paths = [path for path in (receipt_path, failure_path, consumption_path) if path]
    if len({path.resolve(strict=False) for path in paths}) != len(paths):
        errors.append("save receipts and consumption record must use distinct paths")
    if errors:
        raise ValidationError(errors)
    body = _save_request_body(action)
    body_bytes = _canonical_body(body)
    if bindings.get("request_body_sha256") != sha256_bytes(body_bytes):
        raise ValidationError("full canonical save request body SHA-256 binding mismatch")
    return authorization, {
        "root": root,
        "preview": preview,
        "selection": selection,
        "save_receipt_path": receipt_path,
        "failure_receipt_path": failure_path,
        "consumption_path": consumption_path,
        "request_body": body,
        "request_bytes": body_bytes,
    }


def validate_voice_remix_save_authorization(
    authorization_path: Path,
    *,
    now: datetime | None = None,
) -> dict[str, Any]:
    """Validate the separate save authority and exact owner-selected preview."""

    authorization, preflight = _validate_save_authorization(authorization_path, now=now)
    action = authorization["action"]
    return {
        "valid": True,
        "schema_version": SAVE_AUTH_SCHEMA,
        "authorization_id": authorization["authorization_id"],
        "status": authorization["status"],
        "execution_ready": authorization["status"] == "active",
        "scope": SAVE_SCOPE,
        "source_voice_id": action["source_voice_id"],
        "selected_generated_voice_id": action["selected_generated_voice_id"],
        "selected_audio_sha256": action["selected_audio_sha256"],
        "owner_selection_record_sha256": action["owner_selection_record_sha256"],
        "request": {
            "method": "POST",
            "endpoint": action["endpoint"],
            "body": preflight["request_body"],
            "body_sha256": sha256_bytes(preflight["request_bytes"]),
        },
        "authorized_limits": authorization["authorized_limits"],
        "save_receipt": str(preflight["save_receipt_path"]),
        "failure_receipt": str(preflight["failure_receipt_path"]),
        "consumption_record": str(preflight["consumption_path"]),
        "new_voice_required": True,
        "source_voice_mutation_permitted": False,
    }


def dry_run_voice_remix_save(
    authorization_path: Path,
    *,
    now: datetime | None = None,
) -> dict[str, Any]:
    """Compile a selected-preview save without reading credentials or creating a voice."""

    validation = validate_voice_remix_save_authorization(authorization_path, now=now)
    return {
        "schema_version": SAVE_RECEIPT_SCHEMA,
        "mode": "dry-run",
        "network_called": False,
        "credentials_accessed": False,
        "provider_calls_made": 0,
        "voices_created": 0,
        "authorization_validation": validation,
        "notice": (
            "No voice was created. Execution requires this separate active authorization "
            "and its exact owner-selection binding."
        ),
    }


def _decode_save_response(
    response: _HttpResponse,
    authorization: dict[str, Any],
) -> dict[str, Any]:
    try:
        payload = json.loads(response.data.decode("utf-8"))
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise _ProviderFailure("save_response_json_invalid") from exc
    if not isinstance(payload, dict):
        raise _ProviderFailure("save_response_schema_invalid")
    voice_id = payload.get("voice_id")
    if not isinstance(voice_id, str) or not _ID_RE.fullmatch(voice_id):
        raise _ProviderFailure("saved_voice_id_invalid")
    if voice_id == authorization["action"]["source_voice_id"]:
        raise _ProviderFailure("provider_returned_incumbent_voice_id")
    name = payload.get("name")
    if name is not None and name != authorization["action"]["voice_name"]:
        raise _ProviderFailure("saved_voice_name_mismatch")
    category = payload.get("category")
    if category is not None and (
        not isinstance(category, str)
        or len(category) > 64
        or any(not character.isprintable() for character in category)
    ):
        raise _ProviderFailure("saved_voice_category_invalid")
    is_owner = payload.get("is_owner")
    if is_owner is False:
        raise _ProviderFailure("saved_voice_not_owned_by_requester")
    if is_owner is not None and not isinstance(is_owner, bool):
        raise _ProviderFailure("saved_voice_is_owner_invalid")
    return {
        "voice_id": voice_id,
        "name": name,
        "category": category,
        "is_owner": is_owner,
    }


def execute_voice_remix_save(
    authorization_path: Path,
    *,
    timeout: float = 60.0,
) -> dict[str, Any]:
    """Create one new voice from an explicitly owner-selected preview."""

    if not _is_number(timeout) or float(timeout) <= 0 or float(timeout) > 300:
        raise ValidationError("timeout must be positive and no greater than 300 seconds")
    authorization, preflight = _validate_save_authorization(authorization_path)
    if authorization["status"] != "active":
        raise ValidationError("voice save requires a separate active authorization")
    credential = _credential_from_environment()
    _consume_authorization(
        authorization_path,
        authorization,
        preflight["consumption_path"],
        scope=SAVE_SCOPE,
        authorized_limits=authorization["authorized_limits"],
    )
    attempted_calls = 1
    try:
        response = _post_json(
            authorization["action"]["endpoint"],
            preflight["request_bytes"],
            credential,
            timeout=float(timeout),
            max_response_bytes=authorization["authorized_limits"]["max_response_bytes"],
        )
        character_cost = _validated_character_cost(
            response.headers,
            maximum=None,
            required=False,
        )
        saved = _decode_save_response(response, authorization)
    except _ProviderFailure as exc:
        _write_failure_receipt(
            preflight["failure_receipt_path"],
            authorization_path=authorization_path,
            authorization=authorization,
            scope=SAVE_SCOPE,
            stage="provider_response",
            reason=exc.code,
            attempted_calls=attempted_calls,
            http_status=exc.http_status,
            provider_identifiers=exc.provider_identifiers,
        )
        raise ValidationError(f"ElevenLabs voice save failed closed: {exc.code}") from exc
    receipt = {
        "schema_version": SAVE_RECEIPT_SCHEMA,
        "outcome": "new_voice_created_from_owner_selected_preview",
        "authorization_id": authorization["authorization_id"],
        "authorization_sha256": sha256_file(authorization_path),
        "authorization_consumption_record": authorization["consumption"]["record_path"],
        "authorization_consumption_sha256": sha256_file(preflight["consumption_path"]),
        "provider": "elevenlabs",
        "scope": SAVE_SCOPE,
        "source_voice_id": authorization["action"]["source_voice_id"],
        "selected_generated_voice_id": authorization["action"]["selected_generated_voice_id"],
        "selected_audio_sha256": authorization["action"]["selected_audio_sha256"],
        "owner_selection_record_sha256": authorization["action"][
            "owner_selection_record_sha256"
        ],
        "request_body_sha256": sha256_bytes(preflight["request_bytes"]),
        "new_voice_id": saved["voice_id"],
        "new_voice_name": saved["name"],
        "new_voice_category": saved["category"],
        "new_voice_is_owner": saved["is_owner"],
        "new_voice_is_owner_status": (
            "provider_confirmed" if saved["is_owner"] is True else "provider_not_reported"
        ),
        "source_voice_modified": False,
        "new_voice_created": True,
        "provider_calls_made": 1,
        "provider_identifiers": response.provider_identifiers,
        "readback": {
            "status": "pending_separate_authorization",
            "provider_calls_made": 0,
            "endpoint": f"https://api.elevenlabs.io/v1/voices/{saved['voice_id']}",
            "user_endpoint_permitted": False,
        },
        "provider_character_cost": {
            "header": "character-cost",
            "value": character_cost,
            "unit": "provider_character_units" if character_cost is not None else "not_reported",
            "is_usd": False,
        },
        "spend": {
            "authorized_max_usd": authorization["authorized_limits"]["max_spend_usd"],
            "actual_usd": None,
            "provider_response_reported_spend": False,
            "provider_enforced_usd_cap": False,
            "status": "modeled_or_unknown",
            "hard_bounds": "one_create_call",
        },
        "created_at": _utc_now(),
    }
    _exclusive_write(preflight["save_receipt_path"], _json_bytes(receipt))
    return {
        "schema_version": SAVE_RECEIPT_SCHEMA,
        "mode": "execute",
        "network_called": True,
        "provider_calls_made": 1,
        "voices_created": 1,
        "source_voice_id": authorization["action"]["source_voice_id"],
        "source_voice_modified": False,
        "new_voice_id": saved["voice_id"],
        "save_receipt": str(preflight["save_receipt_path"]),
        "save_receipt_sha256": sha256_file(preflight["save_receipt_path"]),
        "consumption_record": str(preflight["consumption_path"]),
    }
