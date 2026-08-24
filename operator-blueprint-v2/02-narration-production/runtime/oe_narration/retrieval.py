"""One-shot, read-only ElevenLabs metadata inventory and sample retrieval.

The runners are deliberately narrower than the general provider runtime.  The
inventory path reads and normalizes only the plan-bound metadata document.  A
separate, legacy-compatible retrieval path may read one sample only when its
own stronger authorization permits that second call.  Neither path has TTS,
voice mutation, clone, upload, retry, or Hume capabilities.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, BinaryIO

from .bakeoff import (
    ELEVEN_METADATA_INVENTORY_KIND,
    ELEVEN_METADATA_INVENTORY_SCOPE,
    MAX_METADATA_INVENTORY_RESPONSE_BYTES,
    validate_provider_action_authorization,
)
from .core import ValidationError, read_json, sha256_bytes, sha256_file


RETRIEVAL_SCOPE = "elevenlabs_sample_retrieval"
RETRIEVAL_SCHEMA = "oe-elevenlabs-sample-retrieval-v1"
METADATA_INVENTORY_SCHEMA = "oe-elevenlabs-sample-metadata-inventory-v1"
CONSUMPTION_SCHEMA = "oe-provider-authorization-consumption-v1"
METADATA_API_ROOT = "https://api.elevenlabs.io/v1/voices"
MAX_AUTHORIZED_DOWNLOAD_BYTES = 50_000_000
MAX_METADATA_BYTES = 2_000_000
SINGLE_SAMPLE_SELECTOR = "only_single_original_human_sample_attached_to_bound_voice"
FFPROBE_BINARY = shutil.which("ffprobe") or "ffprobe"
_REQUEST_ID_HEADERS = (
    "request-id",
    "x-request-id",
    "xi-request-id",
    "history-item-id",
)


@dataclass(frozen=True)
class _Response:
    data: bytes
    mime_type: str
    headers: dict[str, str]
    provider_identifiers: dict[str, str]


class _ProviderFailure(Exception):
    """A deliberately redacted provider/transport failure."""

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
    """Do not forward the provider credential to any redirected origin."""

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


def _exclusive_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    try:
        descriptor = os.open(path, flags, 0o600)
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(data)
    except FileExistsError as exc:
        raise ValidationError(f"refusing to overwrite immutable retrieval artifact: {path}") from exc
    except OSError as exc:
        # Do not include provider data or credentials in filesystem errors.
        raise ValidationError(f"cannot create immutable retrieval artifact: {path}") from exc


def _reject_symlink_components(root: Path, candidate: Path, label: str) -> None:
    """Reject every pre-existing symlink between root and the destination."""

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
        resolved_candidate = candidate.resolve(strict=False)
    except OSError as exc:
        raise ValidationError(f"cannot safely resolve {label}") from exc
    if not resolved_candidate.is_relative_to(resolved_root):
        raise ValidationError(f"{label} escapes its authorized local root")


def _safe_new_path(root: Path, value: Any, label: str, required_prefix: str) -> Path:
    if not isinstance(value, str) or not value:
        raise ValidationError(f"{label} must be a non-empty relative path")
    relative = Path(value)
    if relative.is_absolute() or "." in relative.parts or ".." in relative.parts:
        raise ValidationError(f"{label} must be a safe relative path")
    if not relative.parts or relative.parts[0] != required_prefix:
        raise ValidationError(f"{label} must remain under {required_prefix}/")
    candidate = root / relative
    _reject_symlink_components(root, candidate, label)
    prefix = root / required_prefix
    if prefix.is_symlink():
        raise ValidationError(f"{label} required prefix may not be a symlink")
    if prefix.exists() and not prefix.is_dir():
        raise ValidationError(f"{label} required prefix is not a directory")
    try:
        resolved = candidate.resolve(strict=False)
        resolved_root = root.resolve(strict=True)
        resolved_prefix = prefix.resolve(strict=False)
    except OSError as exc:
        raise ValidationError(f"cannot safely resolve {label}") from exc
    if not resolved.is_relative_to(resolved_root):
        raise ValidationError(f"{label} escapes its authorized local root")
    if not resolved.is_relative_to(resolved_prefix):
        raise ValidationError(f"{label} escapes the resolved {required_prefix}/ prefix")
    if candidate.exists():
        raise ValidationError(f"{label} already exists; retrieval may not overwrite it")
    return candidate


def _safe_consumption_path(authorization_path: Path, value: Any) -> Path:
    root = authorization_path.parent.resolve(strict=True)
    if not isinstance(value, str) or not value:
        raise ValidationError("consumption.record_path must be a non-empty relative path")
    relative = Path(value)
    if relative.is_absolute() or "." in relative.parts or ".." in relative.parts:
        raise ValidationError("consumption.record_path must be a safe relative path")
    candidate = root / relative
    _reject_symlink_components(root, candidate, "consumption.record_path")
    try:
        resolved = candidate.resolve(strict=False)
    except OSError as exc:
        raise ValidationError("cannot safely resolve consumption.record_path") from exc
    if not resolved.is_relative_to(root):
        raise ValidationError("consumption.record_path escapes the authorization directory")
    if candidate.exists():
        raise ValidationError("authorization consumption record already exists")
    return candidate


def _artifact_root(authorization_path: Path) -> Path:
    try:
        return authorization_path.parent.parent.resolve(strict=True)
    except OSError as exc:
        raise ValidationError("cannot resolve the authorization artifact root") from exc


def _header_map(headers: Any) -> dict[str, str]:
    try:
        return {str(key).lower(): str(value) for key, value in headers.items()}
    except (AttributeError, TypeError, ValueError):
        return {}


def _provider_identifiers(
    headers: dict[str, str], credential: str | None = None
) -> dict[str, str]:
    identifiers: dict[str, str] = {}
    for name in _REQUEST_ID_HEADERS:
        value = headers.get(name)
        if not value:
            continue
        if credential and credential in value:
            continue
        identifiers[name] = value[:1024]
    return identifiers


def _normalized_mime(headers: dict[str, str]) -> str:
    return headers.get("content-type", "").split(";", 1)[0].strip().lower()


def _detect_audio_container(data: bytes, declared_mime: str) -> str:
    if not data:
        raise _ProviderFailure("sample_audio_empty")
    container: str | None = None
    permitted_mimes: set[str] = set()
    if len(data) >= 12 and data[:4] == b"RIFF" and data[8:12] == b"WAVE":
        container = "wav"
        permitted_mimes = {"audio/wav", "audio/x-wav", "audio/wave"}
    elif data.startswith(b"ID3") or (
        len(data) >= 2 and data[0] == 0xFF and (data[1] & 0xE0) == 0xE0
    ):
        container = "mp3_or_aac"
        permitted_mimes = {
            "audio/mpeg",
            "audio/mp3",
            "audio/aac",
            "audio/x-aac",
        }
    elif data.startswith(b"fLaC"):
        container = "flac"
        permitted_mimes = {"audio/flac", "audio/x-flac"}
    elif data.startswith(b"OggS"):
        container = "ogg"
        permitted_mimes = {"audio/ogg"}
    elif len(data) >= 12 and data[4:8] == b"ftyp":
        container = "iso_bmff_audio"
        permitted_mimes = {"audio/mp4", "audio/m4a", "audio/x-m4a"}
    elif data.startswith(b"\x1aE\xdf\xa3"):
        container = "webm"
        permitted_mimes = {"audio/webm"}
    if container is None:
        raise _ProviderFailure("sample_audio_signature_unrecognized")
    if declared_mime not in permitted_mimes:
        raise _ProviderFailure("sample_mime_signature_mismatch")
    return container


def _safe_metadata_text(value: Any, credential: str, *, maximum: int = 255) -> str | None:
    if not isinstance(value, str) or not value:
        return None
    cleaned = "".join(character for character in value if character.isprintable()).strip()
    if not cleaned or (credential and credential in cleaned):
        return None
    return cleaned[:maximum]


def _normalized_sample_metadata(sample: dict[str, Any], credential: str) -> dict[str, Any]:
    """Retain only provenance-relevant, bounded provider fields."""

    filename = _safe_metadata_text(sample.get("file_name"), credential)
    if filename is not None:
        # Provider filenames are untrusted and may use either platform's path
        # separator regardless of the host running this code.
        filename = Path(filename.replace("\\", "/")).name
    result: dict[str, Any] = {
        "sample_id": _safe_metadata_text(sample.get("sample_id"), credential),
        "original_filename": filename,
        "declared_mime_type": _safe_metadata_text(sample.get("mime_type"), credential),
        "category": _safe_metadata_text(sample.get("category"), credential),
        "source": _safe_metadata_text(sample.get("source"), credential),
        "provider_hash": _safe_metadata_text(sample.get("hash"), credential, maximum=128),
    }
    size_bytes = sample.get("size_bytes")
    result["provider_size_bytes"] = (
        size_bytes
        if isinstance(size_bytes, int) and not isinstance(size_bytes, bool) and size_bytes >= 0
        else None
    )
    for field in ("is_generated", "is_original"):
        result[field] = sample.get(field) if isinstance(sample.get(field), bool) else None
    return result


def _normalized_sample_inventory(
    samples: list[Any], credential: str
) -> list[dict[str, Any]]:
    """Preserve bounded, credential-free evidence without selecting a sample."""

    inventory: list[dict[str, Any]] = []
    for index, sample in enumerate(samples):
        if isinstance(sample, dict):
            normalized = _normalized_sample_metadata(sample, credential)
            inventory.append({"metadata_index": index, **normalized})
        else:
            inventory.append(
                {
                    "metadata_index": index,
                    "invalid_sample_entry": True,
                    "sample_id": None,
                    "original_filename": None,
                }
            )
    return inventory


def _metadata_inventory_with_completeness(
    samples: list[Any], credential: str
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Build a bounded inventory while making malformed identity data explicit."""

    inventory = _normalized_sample_inventory(samples, credential)
    malformed_indices = [
        item["metadata_index"]
        for item in inventory
        if item.get("invalid_sample_entry") is True
    ]
    missing_id_indices = [
        item["metadata_index"]
        for item in inventory
        if not isinstance(item.get("sample_id"), str) or not item.get("sample_id")
    ]
    missing_filename_indices = [
        item["metadata_index"]
        for item in inventory
        if not isinstance(item.get("original_filename"), str)
        or not item.get("original_filename")
    ]
    id_to_indices: dict[str, list[int]] = {}
    for item in inventory:
        sample_id = item.get("sample_id")
        if isinstance(sample_id, str) and sample_id:
            id_to_indices.setdefault(sample_id, []).append(item["metadata_index"])
    duplicate_groups = [
        {"sample_id": sample_id, "metadata_indices": indices}
        for sample_id, indices in sorted(id_to_indices.items())
        if len(indices) > 1
    ]
    completeness = {
        "sample_entries_well_formed": not malformed_indices,
        "all_sample_ids_present": not missing_id_indices,
        "all_original_filenames_present": not missing_filename_indices,
        "sample_ids_unique": not duplicate_groups,
        "inventory_complete": not malformed_indices
        and not missing_id_indices
        and not missing_filename_indices
        and not duplicate_groups,
        "malformed_entry_indices": malformed_indices,
        "missing_sample_id_indices": missing_id_indices,
        "missing_original_filename_indices": missing_filename_indices,
        "duplicate_sample_id_groups": duplicate_groups,
    }
    return inventory, completeness


def _probe_audio(path: Path) -> dict[str, Any]:
    """Require ffprobe to parse at least one positive-duration audio stream."""

    command = [
        FFPROBE_BINARY,
        "-v",
        "error",
        "-show_entries",
        "format=duration,format_name:stream=codec_type,codec_name,sample_rate,channels,duration",
        "-of",
        "json",
        str(path),
    ]
    try:
        completed = subprocess.run(
            command,
            check=False,
            capture_output=True,
            timeout=15,
        )
    except FileNotFoundError as exc:
        raise _ProviderFailure("audio_probe_unavailable") from exc
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise _ProviderFailure("audio_probe_failed") from exc
    if completed.returncode != 0:
        raise _ProviderFailure("sample_audio_unparseable")
    try:
        payload = json.loads(completed.stdout.decode("utf-8"))
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise _ProviderFailure("sample_audio_unparseable") from exc
    streams = payload.get("streams") if isinstance(payload, dict) else None
    if not isinstance(streams, list):
        raise _ProviderFailure("sample_audio_unparseable")
    audio_streams = [
        stream
        for stream in streams
        if isinstance(stream, dict) and stream.get("codec_type") == "audio"
    ]
    if not audio_streams:
        raise _ProviderFailure("sample_audio_stream_absent")
    durations: list[float] = []
    format_value = payload.get("format") if isinstance(payload, dict) else None
    candidates = [stream.get("duration") for stream in audio_streams]
    if isinstance(format_value, dict):
        candidates.append(format_value.get("duration"))
    for value in candidates:
        try:
            duration = float(value)
        except (TypeError, ValueError):
            continue
        if duration > 0:
            durations.append(duration)
    if not durations:
        raise _ProviderFailure("sample_audio_duration_not_positive")
    primary = audio_streams[0]
    sample_rate = primary.get("sample_rate")
    try:
        parsed_sample_rate = int(sample_rate)
    except (TypeError, ValueError):
        parsed_sample_rate = None
    channels = primary.get("channels")
    parsed_channels = (
        channels
        if isinstance(channels, int) and not isinstance(channels, bool) and channels > 0
        else None
    )
    format_name = format_value.get("format_name") if isinstance(format_value, dict) else None
    return {
        "probe": "ffprobe",
        "audio_stream_count": len(audio_streams),
        "duration_seconds": max(durations),
        "codec_name": _safe_metadata_text(primary.get("codec_name"), ""),
        "sample_rate_hz": parsed_sample_rate,
        "channels": parsed_channels,
        "format_name": _safe_metadata_text(format_name, ""),
    }


def _open_request(request: urllib.request.Request, timeout: float) -> Any:
    """Small seam for mocked tests; production uses a no-redirect stdlib opener."""

    return urllib.request.build_opener(_NoRedirect()).open(request, timeout=timeout)


def _read_response(
    response: Any,
    *,
    max_bytes: int,
    require_content_length: bool,
    expected_kind: str,
    credential: str,
) -> _Response:
    headers = _header_map(getattr(response, "headers", {}))
    identifiers = _provider_identifiers(headers, credential)
    declared = headers.get("content-length")
    declared_size: int | None = None
    if declared is not None:
        try:
            declared_size = int(declared)
        except (TypeError, ValueError) as exc:
            raise _ProviderFailure(
                "response_size_ambiguous",
                provider_identifiers=identifiers,
            ) from exc
        if declared_size < 0:
            raise _ProviderFailure(
                "response_size_ambiguous",
                provider_identifiers=identifiers,
            )
        if declared_size > max_bytes:
            raise _ProviderFailure(
                "authorized_size_ceiling_exceeded",
                provider_identifiers=identifiers,
            )
    elif require_content_length:
        raise _ProviderFailure(
            "response_size_ambiguous",
            provider_identifiers=identifiers,
        )
    try:
        data = response.read(max_bytes + 1)
    except Exception as exc:  # provider/socket details are intentionally redacted
        raise _ProviderFailure(
            "response_read_failed",
            provider_identifiers=identifiers,
        ) from exc
    if not isinstance(data, bytes):
        raise _ProviderFailure(
            "response_body_not_bytes",
            provider_identifiers=identifiers,
        )
    if len(data) > max_bytes:
        raise _ProviderFailure(
            "authorized_size_ceiling_exceeded",
            provider_identifiers=identifiers,
        )
    if declared_size is not None and declared_size != len(data):
        raise _ProviderFailure(
            "response_size_ambiguous",
            provider_identifiers=identifiers,
        )
    mime = _normalized_mime(headers)
    if expected_kind == "json":
        if mime != "application/json" and not mime.endswith("+json"):
            raise _ProviderFailure(
                "metadata_mime_type_ambiguous",
                provider_identifiers=identifiers,
            )
    elif expected_kind == "audio" and not mime.startswith("audio/"):
        raise _ProviderFailure(
            "sample_mime_type_ambiguous",
            provider_identifiers=identifiers,
        )
    return _Response(data, mime, headers, identifiers)


def _http_get(
    url: str,
    api_key: str,
    *,
    timeout: float,
    max_bytes: int,
    require_content_length: bool,
    expected_kind: str,
) -> _Response:
    request = urllib.request.Request(
        url,
        method="GET",
        headers={
            "Accept": "application/json" if expected_kind == "json" else "audio/*",
            "xi-api-key": api_key,
        },
    )
    try:
        with _open_request(request, timeout) as response:
            status = getattr(response, "status", 200)
            if status != 200:
                raise _ProviderFailure(
                    "provider_http_failure",
                    http_status=status if isinstance(status, int) else None,
                    provider_identifiers=_provider_identifiers(
                        _header_map(getattr(response, "headers", {})), api_key
                    ),
                )
            final_url_getter = getattr(response, "geturl", None)
            if callable(final_url_getter) and final_url_getter() != url:
                raise _ProviderFailure("provider_redirect_forbidden")
            return _read_response(
                response,
                max_bytes=max_bytes,
                require_content_length=require_content_length,
                expected_kind=expected_kind,
                credential=api_key,
            )
    except _ProviderFailure:
        raise
    except urllib.error.HTTPError as exc:
        raise _ProviderFailure(
            "provider_http_failure",
            http_status=exc.code,
            provider_identifiers=_provider_identifiers(_header_map(exc.headers), api_key),
        ) from exc
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        raise _ProviderFailure("provider_transport_failure") from exc
    except Exception as exc:
        # Unexpected provider object details may contain headers. Fail closed
        # without copying their text into an error or receipt.
        raise _ProviderFailure("provider_transport_failure") from exc


def _sample_audio_endpoint(voice_id: str, sample_id: str) -> str:
    return (
        f"{METADATA_API_ROOT}/{urllib.parse.quote(voice_id, safe='')}/samples/"
        f"{urllib.parse.quote(sample_id, safe='')}/audio"
    )


def _write_failure_receipt(
    destination: Path,
    *,
    authorization: dict[str, Any],
    authorization_path: Path,
    stage: str,
    reason: str,
    attempted_calls: int,
    downloads_attempted: int,
    voice_id: str,
    sample_id: str | None = None,
    http_status: int | None = None,
    provider_identifiers: dict[str, str] | None = None,
    blocked_evidence: dict[str, Any] | None = None,
    metadata_evidence: dict[str, Any] | None = None,
) -> None:
    receipt = {
        "schema_version": RETRIEVAL_SCHEMA,
        "outcome": "failed_closed",
        "stage": stage,
        "reason": reason,
        "authorization_id": authorization["authorization_id"],
        "authorization_sha256": sha256_file(authorization_path),
        "voice_id": voice_id,
        "sample_id": sample_id,
        "attempted_calls": attempted_calls,
        "downloads_attempted": downloads_attempted,
        "http_status": http_status,
        "provider_identifiers": provider_identifiers or {},
        "blocked_local_evidence": blocked_evidence,
        "metadata_evidence": metadata_evidence,
        "failed_at": _utc_now(),
        "provenance_verification": "not_completed",
        "human_source_confirmed": False,
        "single_speaker_confirmed": False,
    }
    _exclusive_write(destination, _json_bytes(receipt))


def _validate_runner_contract(
    authorization_path: Path,
    authorization: dict[str, Any],
    validation: dict[str, Any],
) -> tuple[Path, Path, Path, Path]:
    errors: list[str] = []
    if validation.get("status") != "active" or validation.get("execution_ready") is not True:
        errors.append("retrieval execution requires an active, execution-ready authorization")
    if validation.get("scope") != RETRIEVAL_SCOPE or authorization.get("scope") != RETRIEVAL_SCOPE:
        errors.append(f"retrieval execution requires exact scope {RETRIEVAL_SCOPE}")
    if authorization.get("provider") != "elevenlabs":
        errors.append("retrieval execution is restricted to ElevenLabs")
    action = authorization.get("action", {})
    voice_id = action.get("voice_id")
    expected_metadata = (
        f"{METADATA_API_ROOT}/{urllib.parse.quote(str(voice_id), safe='')}"
    )
    if action.get("metadata_endpoint") != expected_metadata:
        errors.append("metadata endpoint is not the exact official endpoint for the bound voice")
    if action.get("sample_ids") != [] or action.get("sample_selection_rule") != SINGLE_SAMPLE_SELECTOR:
        errors.append("runner requires the approved bounded single-sample metadata selector")
    if action.get("selection_fails_if_zero_or_multiple_samples") is not True:
        errors.append("runner must fail on zero or multiple metadata samples")
    if action.get("selection_fails_if_mixed_speaker") is not True:
        errors.append("runner must leave mixed-speaker verification pending and fail before downstream use")
    limits = authorization.get("authorized_limits", {})
    if limits.get("max_calls") != 2:
        errors.append("authorized max_calls must be exactly 2")
    if limits.get("max_downloads") != 1:
        errors.append("authorized max_downloads must be exactly 1")
    if limits.get("max_spend_usd") != 0:
        errors.append("authorized max_spend_usd must be exactly 0 for read-only retrieval")
    max_bytes = limits.get("max_download_bytes")
    if (
        not isinstance(max_bytes, int)
        or isinstance(max_bytes, bool)
        or max_bytes <= 0
        or max_bytes > MAX_AUTHORIZED_DOWNLOAD_BYTES
    ):
        errors.append(
            f"authorized max_download_bytes must be between 1 and {MAX_AUTHORIZED_DOWNLOAD_BYTES}"
        )
    destinations = action.get("destinations")
    if not isinstance(destinations, list) or len(destinations) != 1:
        errors.append("retrieval must have exactly one raw sample destination")
    if errors:
        raise ValidationError(errors)
    root = _artifact_root(authorization_path)
    raw_path = _safe_new_path(root, destinations[0], "action.destinations[0]", "local-media")
    metadata_receipt = _safe_new_path(
        root,
        action.get("metadata_receipt_destination"),
        "action.metadata_receipt_destination",
        "receipts",
    )
    sample_receipt = _safe_new_path(
        root,
        action.get("selected_sample_receipt_destination"),
        "action.selected_sample_receipt_destination",
        "receipts",
    )
    consumption_path = _safe_consumption_path(
        authorization_path, authorization.get("consumption", {}).get("record_path")
    )
    canonical_paths = {
        path.resolve(strict=False)
        for path in (raw_path, metadata_receipt, sample_receipt, consumption_path)
    }
    if len(canonical_paths) != 4:
        raise ValidationError("retrieval artifacts and consumption record must have distinct paths")
    return raw_path, metadata_receipt, sample_receipt, consumption_path


def dry_run_retrieval(authorization_path: Path) -> dict[str, Any]:
    """Validate authority without reading a credential or calling the provider."""

    validation = validate_provider_action_authorization(authorization_path)
    authorization = read_json(authorization_path)
    preflight: dict[str, Any]
    if validation.get("status") == "active":
        raw, metadata_receipt, sample_receipt, consumption = _validate_runner_contract(
            authorization_path, authorization, validation
        )
        action = authorization["action"]
        preflight = {
            "valid": True,
            "metadata_request": {
                "method": "GET",
                "endpoint": action["metadata_endpoint"],
            },
            "sample_request": {
                "method": "GET",
                "endpoint": "derived_after_exactly_one_sample_id_is_selected",
            },
            "authorized_limits": authorization["authorized_limits"],
            "destinations": {
                "raw_sample": str(raw),
                "metadata_receipt": str(metadata_receipt),
                "selected_sample_receipt": str(sample_receipt),
                "consumption_record": str(consumption),
            },
            "unresolved": [
                "sample_id_until_metadata_selection",
                "human_source_verification",
                "single_speaker_verification",
            ],
        }
    else:
        preflight = {
            "valid": False,
            "reason": "draft_authorization_is_not_executable",
            "unresolved": authorization.get("blockers", []),
        }
    return {
        "schema_version": RETRIEVAL_SCHEMA,
        "mode": "dry-run",
        "authorization_validation": validation,
        "scope": authorization.get("scope"),
        "network_called": False,
        "credentials_accessed": False,
        "provider_calls_made": 0,
        "downloads_made": 0,
        "executor_preflight": preflight,
        "notice": "No provider action occurred. --execute requires active unconsumed authority.",
    }


def execute_retrieval(authorization_path: Path, timeout: float = 60.0) -> dict[str, Any]:
    """Consume one authorization and perform at most two read-only GET calls."""

    if timeout <= 0:
        raise ValidationError("timeout must be positive")
    validation = validate_provider_action_authorization(authorization_path)
    authorization = read_json(authorization_path)
    raw_path, metadata_receipt_path, sample_receipt_path, consumption_path = (
        _validate_runner_contract(authorization_path, authorization, validation)
    )
    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValidationError("ELEVENLABS_API_KEY is required only for authorized --execute")

    action = authorization["action"]
    voice_id = action["voice_id"]
    max_download_bytes = authorization["authorized_limits"]["max_download_bytes"]
    authorization_hash = sha256_file(authorization_path)
    consumption = {
        "schema_version": CONSUMPTION_SCHEMA,
        "authorization_id": authorization["authorization_id"],
        "authorization_sha256": authorization_hash,
        "scope": RETRIEVAL_SCOPE,
        "status": "consumed",
        "consumed_before_network": True,
        "consumed_at": _utc_now(),
        "reason": "one-shot provider retrieval started; no retry is permitted",
        "authorized_limits": {
            "max_calls": 2,
            "max_downloads": 1,
            "max_download_bytes": max_download_bytes,
        },
    }
    # This immutable file is the point of no return. It exists before the
    # first request is constructed or opened.
    _exclusive_write(consumption_path, _json_bytes(consumption))

    attempted_calls = 1
    downloads_attempted = 0
    try:
        metadata_response = _http_get(
            action["metadata_endpoint"],
            api_key,
            timeout=timeout,
            max_bytes=MAX_METADATA_BYTES,
            require_content_length=False,
            expected_kind="json",
        )
    except _ProviderFailure as exc:
        _write_failure_receipt(
            metadata_receipt_path,
            authorization=authorization,
            authorization_path=authorization_path,
            stage="metadata",
            reason=exc.code,
            attempted_calls=attempted_calls,
            downloads_attempted=downloads_attempted,
            voice_id=voice_id,
            http_status=exc.http_status,
            provider_identifiers=exc.provider_identifiers,
        )
        raise ValidationError(f"ElevenLabs metadata retrieval failed closed: {exc.code}") from exc

    try:
        metadata = json.loads(metadata_response.data.decode("utf-8"))
    except (UnicodeError, json.JSONDecodeError) as exc:
        _write_failure_receipt(
            metadata_receipt_path,
            authorization=authorization,
            authorization_path=authorization_path,
            stage="metadata",
            reason="metadata_json_invalid",
            attempted_calls=attempted_calls,
            downloads_attempted=downloads_attempted,
            voice_id=voice_id,
            provider_identifiers=metadata_response.provider_identifiers,
        )
        raise ValidationError("ElevenLabs metadata retrieval failed closed: metadata_json_invalid") from exc
    if not isinstance(metadata, dict) or metadata.get("voice_id") != voice_id:
        reason = "metadata_voice_id_missing_or_mismatched"
        _write_failure_receipt(
            metadata_receipt_path,
            authorization=authorization,
            authorization_path=authorization_path,
            stage="metadata_selection",
            reason=reason,
            attempted_calls=attempted_calls,
            downloads_attempted=downloads_attempted,
            voice_id=voice_id,
            provider_identifiers=metadata_response.provider_identifiers,
        )
        raise ValidationError(f"ElevenLabs metadata retrieval failed closed: {reason}")
    samples = metadata.get("samples")
    if not isinstance(samples, list):
        reason = "metadata_samples_missing_or_invalid"
        _write_failure_receipt(
            metadata_receipt_path,
            authorization=authorization,
            authorization_path=authorization_path,
            stage="metadata_selection",
            reason=reason,
            attempted_calls=attempted_calls,
            downloads_attempted=downloads_attempted,
            voice_id=voice_id,
            provider_identifiers=metadata_response.provider_identifiers,
        )
        raise ValidationError(f"ElevenLabs metadata retrieval failed closed: {reason}")
    if len(samples) != 1:
        reason = "zero_samples" if len(samples) == 0 else "multiple_samples"
        metadata_evidence = {
            "voice_id": voice_id,
            "sample_count": len(samples),
            "samples": _normalized_sample_inventory(samples, api_key),
            "response": {
                "mime_type": metadata_response.mime_type,
                "byte_count": len(metadata_response.data),
                "sha256": sha256_bytes(metadata_response.data),
                "provider_identifiers": metadata_response.provider_identifiers,
            },
            "selection_made": False,
            "download_attempted": False,
            "provenance_verification": "not_completed",
        }
        _write_failure_receipt(
            metadata_receipt_path,
            authorization=authorization,
            authorization_path=authorization_path,
            stage="metadata_selection",
            reason=reason,
            attempted_calls=attempted_calls,
            downloads_attempted=downloads_attempted,
            voice_id=voice_id,
            provider_identifiers=metadata_response.provider_identifiers,
            metadata_evidence=metadata_evidence,
        )
        raise ValidationError(f"ElevenLabs metadata retrieval failed closed: {reason}")
    sample = samples[0]
    sample_id = sample.get("sample_id") if isinstance(sample, dict) else None
    if (
        not isinstance(sample_id, str)
        or not sample_id
        or "pending" in sample_id.lower()
        or api_key in sample_id
    ):
        reason = "single_sample_id_missing_or_invalid"
        _write_failure_receipt(
            metadata_receipt_path,
            authorization=authorization,
            authorization_path=authorization_path,
            stage="metadata_selection",
            reason=reason,
            attempted_calls=attempted_calls,
            downloads_attempted=downloads_attempted,
            voice_id=voice_id,
            provider_identifiers=metadata_response.provider_identifiers,
        )
        raise ValidationError(f"ElevenLabs metadata retrieval failed closed: {reason}")

    metadata_receipt = {
        "schema_version": RETRIEVAL_SCHEMA,
        "outcome": "one_sample_selected_for_download",
        "authorization_id": authorization["authorization_id"],
        "authorization_sha256": authorization_hash,
        "voice_id": voice_id,
        "sample_count": 1,
        "selected_sample_id": sample_id,
        "selector": SINGLE_SAMPLE_SELECTOR,
        "response": {
            "mime_type": metadata_response.mime_type,
            "byte_count": len(metadata_response.data),
            "sha256": sha256_bytes(metadata_response.data),
            "provider_identifiers": metadata_response.provider_identifiers,
        },
        "provider_sample_metadata": _normalized_sample_metadata(sample, api_key),
        "retrieved_at": _utc_now(),
        "provenance_verification": "pending_download_and_human_review",
        "human_source_confirmed": False,
        "single_speaker_confirmed": False,
        "notice": "Metadata count alone cannot establish human origin or single-speaker provenance.",
    }
    _exclusive_write(metadata_receipt_path, _json_bytes(metadata_receipt))

    sample_endpoint = _sample_audio_endpoint(voice_id, sample_id)
    if attempted_calls >= 2 or downloads_attempted >= 1:
        raise ValidationError("retrieval authorization ceiling exhausted before sample download")
    attempted_calls += 1
    downloads_attempted += 1
    try:
        sample_response = _http_get(
            sample_endpoint,
            api_key,
            timeout=timeout,
            max_bytes=max_download_bytes,
            require_content_length=True,
            expected_kind="audio",
        )
        detected_container = _detect_audio_container(
            sample_response.data, sample_response.mime_type
        )
    except _ProviderFailure as exc:
        _write_failure_receipt(
            sample_receipt_path,
            authorization=authorization,
            authorization_path=authorization_path,
            stage="sample_download",
            reason=exc.code,
            attempted_calls=attempted_calls,
            downloads_attempted=downloads_attempted,
            voice_id=voice_id,
            sample_id=sample_id,
            http_status=exc.http_status,
            provider_identifiers=exc.provider_identifiers,
        )
        raise ValidationError(f"ElevenLabs sample retrieval failed closed: {exc.code}") from exc

    try:
        _exclusive_write(raw_path, sample_response.data)
    except ValidationError:
        _write_failure_receipt(
            sample_receipt_path,
            authorization=authorization,
            authorization_path=authorization_path,
            stage="sample_storage",
            reason="raw_destination_unavailable",
            attempted_calls=attempted_calls,
            downloads_attempted=downloads_attempted,
            voice_id=voice_id,
            sample_id=sample_id,
            provider_identifiers=sample_response.provider_identifiers,
        )
        raise
    sample_hash = sha256_file(raw_path)
    try:
        actual_media = _probe_audio(raw_path)
    except _ProviderFailure as exc:
        blocked_evidence = {
            "path": str(raw_path),
            "mime_type": sample_response.mime_type,
            "detected_container": detected_container,
            "byte_count": len(sample_response.data),
            "sha256": sample_hash,
            "status": "blocked_not_usable",
        }
        _write_failure_receipt(
            sample_receipt_path,
            authorization=authorization,
            authorization_path=authorization_path,
            stage="sample_media_validation",
            reason=exc.code,
            attempted_calls=attempted_calls,
            downloads_attempted=downloads_attempted,
            voice_id=voice_id,
            sample_id=sample_id,
            provider_identifiers=sample_response.provider_identifiers,
            blocked_evidence=blocked_evidence,
        )
        raise ValidationError(
            f"ElevenLabs sample retrieval failed closed: {exc.code}"
        ) from exc
    selected_receipt = {
        "schema_version": RETRIEVAL_SCHEMA,
        "outcome": "downloaded_pending_provenance_review",
        "authorization_id": authorization["authorization_id"],
        "authorization_sha256": authorization_hash,
        "authorization_consumption_record": str(consumption_path),
        "authorization_consumption_sha256": sha256_file(consumption_path),
        "voice_id": voice_id,
        "sample_id": sample_id,
        "request": {
            "method": "GET",
            "endpoint": sample_endpoint,
        },
        "raw_output": {
            "path": str(raw_path),
            "mime_type": sample_response.mime_type,
            "detected_container": detected_container,
            "actual_media": actual_media,
            "byte_count": len(sample_response.data),
            "sha256": sample_hash,
        },
        "provider_identifiers": sample_response.provider_identifiers,
        "attempted_calls": attempted_calls,
        "downloads_attempted": downloads_attempted,
        "downloaded_at": _utc_now(),
        "provenance_verification": "pending_human_review",
        "human_source_confirmed": False,
        "single_speaker_confirmed": False,
        "synthetic_source_excluded": False,
        "downstream_use_authorized": False,
        "notice": "Download success does not establish human origin, speaker purity, or Hume-upload authority.",
    }
    _exclusive_write(sample_receipt_path, _json_bytes(selected_receipt))
    return {
        "schema_version": RETRIEVAL_SCHEMA,
        "mode": "execute",
        "network_called": True,
        "scope": RETRIEVAL_SCOPE,
        "provider_calls_made": attempted_calls,
        "downloads_made": 1,
        "voice_id": voice_id,
        "sample_id": sample_id,
        "raw_path": str(raw_path),
        "raw_sha256": sample_hash,
        "mime_type": sample_response.mime_type,
        "detected_container": detected_container,
        "actual_media": actual_media,
        "byte_count": len(sample_response.data),
        "metadata_receipt": str(metadata_receipt_path),
        "selected_sample_receipt": str(sample_receipt_path),
        "consumption_record": str(consumption_path),
        "provenance_verification": "pending_human_review",
        "human_source_confirmed": False,
        "single_speaker_confirmed": False,
        "hume_upload_authorized": False,
    }


def _write_inventory_failure_receipt(
    destination: Path,
    *,
    authorization: dict[str, Any],
    authorization_path: Path,
    reason: str,
    voice_id: str,
    http_status: int | None = None,
    provider_identifiers: dict[str, str] | None = None,
    response_evidence: dict[str, Any] | None = None,
) -> None:
    receipt = {
        "schema_version": METADATA_INVENTORY_SCHEMA,
        "outcome": "failed_closed",
        "reason": reason,
        "authorization_id": authorization["authorization_id"],
        "authorization_sha256": sha256_file(authorization_path),
        "voice_id": voice_id,
        "attempted_calls": 1,
        "downloads_attempted": 0,
        "selection_made": False,
        "sample_audio_endpoint_constructed": False,
        "raw_provider_payload_stored": False,
        "http_status": http_status,
        "provider_identifiers": provider_identifiers or {},
        "response_evidence": response_evidence,
        "failed_at": _utc_now(),
    }
    _exclusive_write(destination, _json_bytes(receipt))


def _validate_inventory_runner_contract(
    authorization_path: Path,
    authorization: dict[str, Any],
    validation: dict[str, Any],
) -> tuple[Path, Path]:
    errors: list[str] = []
    if validation.get("status") != "active" or validation.get("execution_ready") is not True:
        errors.append("metadata inventory execution requires an active, execution-ready authorization")
    if (
        validation.get("scope") != ELEVEN_METADATA_INVENTORY_SCOPE
        or authorization.get("scope") != ELEVEN_METADATA_INVENTORY_SCOPE
    ):
        errors.append(
            f"metadata inventory execution requires exact scope {ELEVEN_METADATA_INVENTORY_SCOPE}"
        )
    if authorization.get("provider") != "elevenlabs":
        errors.append("metadata inventory execution is restricted to ElevenLabs")
    action = authorization.get("action", {})
    if action.get("kind") != ELEVEN_METADATA_INVENTORY_KIND:
        errors.append("metadata inventory action kind mismatch")
    voice_id = action.get("voice_id")
    expected_metadata = f"{METADATA_API_ROOT}/{urllib.parse.quote(str(voice_id), safe='')}"
    if action.get("metadata_endpoint") != expected_metadata:
        errors.append("metadata inventory endpoint is not the exact official endpoint for the bound voice")
    for field in (
        "selection_permitted",
        "download_permitted",
        "raw_payload_storage_permitted",
    ):
        if action.get(field) is not False:
            errors.append(f"metadata inventory action.{field} must be false")
    limits = authorization.get("authorized_limits", {})
    if (
        not isinstance(limits.get("max_calls"), int)
        or isinstance(limits.get("max_calls"), bool)
        or limits.get("max_calls") != 1
    ):
        errors.append("metadata inventory authorized max_calls must be exactly 1")
    if (
        not isinstance(limits.get("max_downloads"), int)
        or isinstance(limits.get("max_downloads"), bool)
        or limits.get("max_downloads") != 0
    ):
        errors.append("metadata inventory authorized max_downloads must be exactly 0")
    if (
        not isinstance(limits.get("max_spend_usd"), (int, float))
        or isinstance(limits.get("max_spend_usd"), bool)
        or limits.get("max_spend_usd") != 0
    ):
        errors.append("metadata inventory authorized max_spend_usd must be exactly 0")
    max_metadata_bytes = limits.get("max_metadata_response_bytes")
    if (
        not isinstance(max_metadata_bytes, int)
        or isinstance(max_metadata_bytes, bool)
        or max_metadata_bytes <= 0
        or max_metadata_bytes > MAX_METADATA_INVENTORY_RESPONSE_BYTES
    ):
        errors.append(
            "metadata inventory max_metadata_response_bytes must be between 1 and 2000000"
        )
    if errors:
        raise ValidationError(errors)
    root = _artifact_root(authorization_path)
    metadata_receipt = _safe_new_path(
        root,
        action.get("metadata_receipt_destination"),
        "action.metadata_receipt_destination",
        "receipts",
    )
    consumption_path = _safe_consumption_path(
        authorization_path, authorization.get("consumption", {}).get("record_path")
    )
    if metadata_receipt.resolve(strict=False) == consumption_path.resolve(strict=False):
        raise ValidationError("metadata inventory receipt and consumption record must be distinct")
    return metadata_receipt, consumption_path


def dry_run_metadata_inventory(authorization_path: Path) -> dict[str, Any]:
    """Validate metadata-only authority without reading credentials or networking."""

    validation = validate_provider_action_authorization(authorization_path)
    authorization = read_json(authorization_path)
    if validation.get("status") == "active":
        metadata_receipt, consumption = _validate_inventory_runner_contract(
            authorization_path, authorization, validation
        )
        action = authorization["action"]
        preflight: dict[str, Any] = {
            "valid": True,
            "metadata_request": {
                "method": "GET",
                "endpoint": action["metadata_endpoint"],
            },
            "authorized_limits": authorization["authorized_limits"],
            "destinations": {
                "normalized_metadata_receipt": str(metadata_receipt),
                "consumption_record": str(consumption),
            },
            "selection_permitted": False,
            "download_permitted": False,
            "sample_audio_endpoint_constructed": False,
            "raw_provider_payload_storage_permitted": False,
        }
    else:
        preflight = {
            "valid": False,
            "reason": "draft_authorization_is_not_executable",
            "unresolved": authorization.get("blockers", []),
        }
    return {
        "schema_version": METADATA_INVENTORY_SCHEMA,
        "mode": "dry-run",
        "authorization_validation": validation,
        "scope": authorization.get("scope"),
        "network_called": False,
        "credentials_accessed": False,
        "provider_calls_made": 0,
        "downloads_made": 0,
        "executor_preflight": preflight,
        "notice": "No provider action occurred. --execute requires active unconsumed metadata-inventory authority.",
    }


def execute_metadata_inventory(
    authorization_path: Path, timeout: float = 60.0
) -> dict[str, Any]:
    """Consume one authorization and perform exactly one metadata-only GET."""

    if timeout <= 0:
        raise ValidationError("timeout must be positive")
    validation = validate_provider_action_authorization(authorization_path)
    authorization = read_json(authorization_path)
    metadata_receipt_path, consumption_path = _validate_inventory_runner_contract(
        authorization_path, authorization, validation
    )
    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValidationError("ELEVENLABS_API_KEY is required only for authorized --execute")

    action = authorization["action"]
    voice_id = action["voice_id"]
    max_metadata_bytes = authorization["authorized_limits"]["max_metadata_response_bytes"]
    authorization_hash = sha256_file(authorization_path)
    consumption = {
        "schema_version": CONSUMPTION_SCHEMA,
        "authorization_id": authorization["authorization_id"],
        "authorization_sha256": authorization_hash,
        "scope": ELEVEN_METADATA_INVENTORY_SCOPE,
        "status": "consumed",
        "consumed_before_network": True,
        "consumed_at": _utc_now(),
        "reason": "one-shot metadata inventory started; no retry is permitted",
        "authorized_limits": {
            "max_calls": 1,
            "max_downloads": 0,
            "max_metadata_response_bytes": max_metadata_bytes,
            "max_spend_usd": 0,
        },
    }
    _exclusive_write(consumption_path, _json_bytes(consumption))

    try:
        metadata_response = _http_get(
            action["metadata_endpoint"],
            api_key,
            timeout=timeout,
            max_bytes=max_metadata_bytes,
            require_content_length=False,
            expected_kind="json",
        )
    except _ProviderFailure as exc:
        _write_inventory_failure_receipt(
            metadata_receipt_path,
            authorization=authorization,
            authorization_path=authorization_path,
            reason=exc.code,
            voice_id=voice_id,
            http_status=exc.http_status,
            provider_identifiers=exc.provider_identifiers,
        )
        raise ValidationError(
            f"ElevenLabs metadata inventory failed closed: {exc.code}"
        ) from exc

    response_evidence = {
        "mime_type": metadata_response.mime_type,
        "byte_count": len(metadata_response.data),
        "sha256": sha256_bytes(metadata_response.data),
        "provider_identifiers": metadata_response.provider_identifiers,
    }
    try:
        metadata = json.loads(metadata_response.data.decode("utf-8"))
    except (UnicodeError, json.JSONDecodeError) as exc:
        _write_inventory_failure_receipt(
            metadata_receipt_path,
            authorization=authorization,
            authorization_path=authorization_path,
            reason="metadata_json_invalid",
            voice_id=voice_id,
            provider_identifiers=metadata_response.provider_identifiers,
            response_evidence=response_evidence,
        )
        raise ValidationError(
            "ElevenLabs metadata inventory failed closed: metadata_json_invalid"
        ) from exc
    if not isinstance(metadata, dict) or metadata.get("voice_id") != voice_id:
        reason = "metadata_voice_id_missing_or_mismatched"
        _write_inventory_failure_receipt(
            metadata_receipt_path,
            authorization=authorization,
            authorization_path=authorization_path,
            reason=reason,
            voice_id=voice_id,
            provider_identifiers=metadata_response.provider_identifiers,
            response_evidence=response_evidence,
        )
        raise ValidationError(f"ElevenLabs metadata inventory failed closed: {reason}")
    samples = metadata.get("samples")
    if not isinstance(samples, list):
        reason = "metadata_samples_missing_or_invalid"
        _write_inventory_failure_receipt(
            metadata_receipt_path,
            authorization=authorization,
            authorization_path=authorization_path,
            reason=reason,
            voice_id=voice_id,
            provider_identifiers=metadata_response.provider_identifiers,
            response_evidence=response_evidence,
        )
        raise ValidationError(f"ElevenLabs metadata inventory failed closed: {reason}")

    inventory, completeness = _metadata_inventory_with_completeness(samples, api_key)
    receipt = {
        "schema_version": METADATA_INVENTORY_SCHEMA,
        "outcome": "normalized_inventory_recorded",
        "authorization_id": authorization["authorization_id"],
        "authorization_sha256": authorization_hash,
        "authorization_consumption_record": str(consumption_path),
        "authorization_consumption_sha256": sha256_file(consumption_path),
        "voice_id": voice_id,
        "request": {"method": "GET", "endpoint": action["metadata_endpoint"]},
        "response": response_evidence,
        "sample_count": len(samples),
        "samples": inventory,
        "inventory_completeness": completeness,
        "selection_made": False,
        "selection_permitted": False,
        "downloads_attempted": 0,
        "download_permitted": False,
        "sample_audio_endpoint_constructed": False,
        "raw_provider_payload_stored": False,
        "provider_metadata_is_provenance_proof": False,
        "recorded_at": _utc_now(),
        "next_external_action_authorized": False,
    }
    _exclusive_write(metadata_receipt_path, _json_bytes(receipt))
    return {
        "schema_version": METADATA_INVENTORY_SCHEMA,
        "mode": "execute",
        "network_called": True,
        "scope": ELEVEN_METADATA_INVENTORY_SCOPE,
        "provider_calls_made": 1,
        "downloads_made": 0,
        "voice_id": voice_id,
        "sample_count": len(samples),
        "inventory_complete": completeness["inventory_complete"],
        "selection_made": False,
        "sample_audio_endpoint_constructed": False,
        "raw_provider_payload_stored": False,
        "metadata_receipt": str(metadata_receipt_path),
        "metadata_receipt_sha256": sha256_file(metadata_receipt_path),
        "consumption_record": str(consumption_path),
        "next_external_action_authorized": False,
    }
