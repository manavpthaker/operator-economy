"""Fail-closed, credential-free provider bakeoff compilation.

This module deliberately stops at request compilation.  It never reads provider
credentials, opens a network connection, uploads voice media, or creates audio.
"""

from __future__ import annotations

import json
import math
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import quote

from .core import (
    ValidationError,
    read_canonical_w,
    read_json,
    sha256_bytes,
    sha256_file,
    token_identity,
)


PERFORMANCE_ENVELOPE_SCHEMA = "oe-performance-envelope-v1"
PROVIDER_BAKEOFF_PLAN_SCHEMA = "oe-provider-bakeoff-plan-v1"
PROVIDER_ADAPTER_SCHEMA = "oe-provider-adapter-v1"
PROVIDER_BAKEOFF_DRY_RUN_SCHEMA = "oe-provider-bakeoff-dry-run-v1"
PROVIDER_ACTION_AUTHORIZATION_SCHEMA = "oe-provider-action-authorization-v1"
ELEVEN_REMIX_OWNER_SELECTION_SCHEMA = "oe-elevenlabs-voice-remix-owner-selection-v1"
ELEVEN_REMIX_SAVE_RECEIPT_SCHEMA = "oe-elevenlabs-voice-remix-save-receipt-v1"
ELEVEN_CALIBRATION_RIGHTS_SCHEMA = "oe-elevenlabs-calibration-rights-v1"
ELEVEN_VOICE_PROVENANCE_KINDS = frozenset({"saved_remix", "existing_ivc"})
ELEVEN_CALIBRATION_PROVENANCE_FIELDS = frozenset(
    {
        "voice_provenance_kind",
        "calibration_rights_receipt_path",
        "calibration_rights_receipt_sha256",
        "owner_selection_record_path",
        "owner_selection_record_sha256",
        "saved_voice_receipt_path",
        "saved_voice_receipt_sha256",
    }
)
ELEVEN_METADATA_INVENTORY_SCOPE = "elevenlabs_sample_metadata_inventory"
ELEVEN_METADATA_INVENTORY_KIND = "read_only_voice_metadata_inventory"
MAX_METADATA_INVENTORY_RESPONSE_BYTES = 2_000_000
ELEVEN_NAMED_SAMPLE_BATCH_SCOPE = "elevenlabs_named_sample_batch_retrieval"
ELEVEN_NAMED_SAMPLE_BATCH_KIND = "read_only_named_sample_batch_retrieval"
MAX_NAMED_SAMPLE_REVIEW_COUNT = 3
MAX_NAMED_SAMPLE_REVIEW_BYTES = 20_000_000

ELEVEN_ALLOWED_TAGS = frozenset(
    {"[curious]", "[sarcastic]", "[excited]", "[pause]", "[warmly]"}
)
ACTION_SCOPES = frozenset(
    {
        "elevenlabs_sample_retrieval",
        ELEVEN_METADATA_INVENTORY_SCOPE,
        ELEVEN_NAMED_SAMPLE_BATCH_SCOPE,
        "hume_clone_creation",
        "elevenlabs_calibration",
        "hume_calibration",
    }
)
HUME_CLONE_PLACEHOLDER = "__HUME_CLONE_ID_PENDING__"
HEX64_RE = re.compile(r"[0-9a-f]{64}\Z")
OPAQUE_PROVIDER_HASH_RE = re.compile(r"[0-9a-f]{32}\Z")
BRACKET_DIRECTION_RE = re.compile(r"\[[^\]\r\n]+\]")
FORBIDDEN_SECRET_KEYS = frozenset(
    {
        "api_key",
        "apikey",
        "api_token",
        "access_token",
        "auth_token",
        "authorization_header",
        "bearer_token",
        "client_secret",
        "credential",
        "credentials",
        "password",
        "private_key",
        "secret",
    }
)
FORBIDDEN_ENVELOPE_PROVIDER_KEYS = frozenset(
    {
        "provider",
        "providers",
        "provider_id",
        "model",
        "model_id",
        "voice",
        "voice_id",
        "clone_voice_id",
        "tag",
        "tags",
        "tag_insertions",
        "description",
        "descriptions",
        "elevenlabs",
        "hume",
    }
)


def _json_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def _json_sha256(value: Any) -> str:
    return sha256_bytes(_json_bytes(value))


def _is_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def _hash_value(value: Any, label: str, errors: list[str], *, allow_pending: bool = False) -> bool:
    if allow_pending and value == "pending":
        return False
    if not isinstance(value, str) or HEX64_RE.fullmatch(value) is None:
        errors.append(f"{label} must be a lowercase SHA-256")
        return False
    return True


def _safe_relative(value: Any, label: str, errors: list[str]) -> Path | None:
    if not isinstance(value, str) or not value:
        errors.append(f"{label} must be a non-empty relative path")
        return None
    path = Path(value)
    if path.is_absolute() or ".." in path.parts or "." in path.parts:
        errors.append(f"{label} must not be absolute or contain '.' or '..'")
        return None
    if any(part in {"", "~"} for part in path.parts):
        errors.append(f"{label} is not a safe relative path")
        return None
    return path


def _verify_existing_local_binding(
    root: Path,
    path_value: Any,
    hash_value: Any,
    label: str,
    errors: list[str],
    *,
    required_prefix: str | None = None,
) -> Path | None:
    """Verify a local path/hash binding without permitting traversal or symlink escape."""
    relative = _safe_relative(path_value, f"{label}.path", errors)
    hash_valid = _hash_value(hash_value, f"{label}.sha256", errors)
    if relative is None:
        return None
    if required_prefix is not None and (not relative.parts or relative.parts[0] != required_prefix):
        errors.append(f"{label}.path must remain under {required_prefix}/")
    candidate = root / relative
    try:
        resolved = candidate.resolve(strict=False)
    except OSError as exc:
        errors.append(f"cannot resolve {label}.path: {exc}")
        return None
    if not resolved.is_relative_to(root.resolve()):
        errors.append(f"{label}.path escapes the local artifact root through traversal or symlink")
        return None
    if not candidate.exists() or not candidate.is_file():
        errors.append(f"{label}.path is missing or is not a file: {candidate}")
        return None
    if hash_valid and sha256_file(candidate) != hash_value:
        errors.append(f"{label}.sha256 does not match the existing file")
    return candidate


def _load_verified_json_binding(
    root: Path,
    bindings: dict[str, Any],
    *,
    path_key: str,
    sha_key: str,
    label: str,
    errors: list[str],
) -> dict[str, Any] | None:
    """Load one immutable, receipt-rooted JSON provenance record."""
    path = _verify_existing_local_binding(
        root,
        bindings.get(path_key),
        bindings.get(sha_key),
        label,
        errors,
        required_prefix="receipts",
    )
    if path is None:
        return None
    try:
        relative_parts = path.relative_to(root).parts
    except ValueError:
        errors.append(f"{label}.path must remain inside the artifact root")
        return None
    cursor = root
    for part in relative_parts:
        cursor = cursor / part
        if cursor.is_symlink():
            errors.append(f"{label}.path must not contain symlink components")
            return None
    if path.suffix.lower() != ".json":
        errors.append(f"{label}.path must identify a JSON receipt")
        return None
    try:
        return read_json(path)
    except ValidationError as exc:
        errors.extend(f"{label}: {error}" for error in exc.errors)
        return None


def _validate_eleven_calibration_voice_provenance(
    authorization: dict[str, Any],
    action: dict[str, Any],
    plan_voice_id: Any,
    artifact_root: Path,
    errors: list[str],
    *,
    required: bool,
) -> None:
    bindings = authorization.get("bindings")
    if not isinstance(bindings, dict):
        bindings = {}
    present = ELEVEN_CALIBRATION_PROVENANCE_FIELDS.intersection(bindings)
    if not present:
        if required:
            errors.append(
                "active ElevenLabs calibration requires complete voice provenance bindings"
            )
        return

    common_fields = {
        "voice_provenance_kind",
        "calibration_rights_receipt_path",
        "calibration_rights_receipt_sha256",
    }
    missing_common = sorted(common_fields.difference(bindings))
    if missing_common:
        errors.append(
            "ElevenLabs calibration provenance bindings are incomplete: missing "
            + ", ".join(missing_common)
        )
    provenance_kind = bindings.get("voice_provenance_kind")
    if provenance_kind not in ELEVEN_VOICE_PROVENANCE_KINDS:
        errors.append(
            "ElevenLabs calibration bindings.voice_provenance_kind must be "
            "saved_remix or existing_ivc"
        )

    calibration_rights = _load_verified_json_binding(
        artifact_root,
        bindings,
        path_key="calibration_rights_receipt_path",
        sha_key="calibration_rights_receipt_sha256",
        label="bindings.calibration_rights_receipt",
        errors=errors,
    )
    if calibration_rights is not None:
        rights_keys = {
            "schema_version",
            "provider",
            "authorization_id",
            "compiled_dry_run_sha256",
            "authorized_limits",
            "voice_provenance_kind",
            "voice_owner",
            "consent_owner",
            "target_voice_id",
            "owner_approval",
            "tts_generation_permitted",
            "permitted_use",
            "full_capture_permitted",
        }
        if provenance_kind == "saved_remix":
            rights_keys.add("saved_voice_receipt_sha256")
        _reject_unknown_keys(
            calibration_rights,
            rights_keys,
            "bound calibration rights receipt",
            errors,
        )
        if calibration_rights.get("schema_version") != ELEVEN_CALIBRATION_RIGHTS_SCHEMA:
            errors.append("bound calibration rights receipt has the wrong schema")
        if calibration_rights.get("provider") != "elevenlabs":
            errors.append("bound calibration rights receipt provider must be elevenlabs")
        if calibration_rights.get("authorization_id") != authorization.get(
            "authorization_id"
        ):
            errors.append("bound calibration rights receipt authorization_id mismatch")
        if calibration_rights.get("compiled_dry_run_sha256") != bindings.get(
            "compiled_dry_run_sha256"
        ):
            errors.append(
                "bound calibration rights receipt compiled request-set hash mismatch"
            )
        rights_limits = calibration_rights.get("authorized_limits")
        _reject_unknown_keys(
            rights_limits,
            {"max_calls", "max_outputs", "max_characters", "max_spend_usd"},
            "bound calibration rights receipt authorized_limits",
            errors,
        )
        if rights_limits != authorization.get("authorized_limits"):
            errors.append(
                "bound calibration rights receipt limits must exactly equal authorization limits"
            )
        if calibration_rights.get("voice_provenance_kind") != provenance_kind:
            errors.append("bound calibration rights receipt provenance kind mismatch")
        approved_by = authorization.get("approved_by")
        if (
            not isinstance(approved_by, str)
            or not approved_by
            or calibration_rights.get("voice_owner") != approved_by
            or calibration_rights.get("consent_owner") != approved_by
        ):
            errors.append(
                "calibration voice_owner and consent_owner must equal authorization approved_by"
            )
        if (
            calibration_rights.get("target_voice_id") != plan_voice_id
            or calibration_rights.get("target_voice_id") != action.get("voice_id")
        ):
            errors.append(
                "bound calibration rights target voice must equal the plan and authorization voice ID"
            )
        if calibration_rights.get("owner_approval") is not True:
            errors.append("bound calibration rights receipt requires owner_approval true")
        if calibration_rights.get("tts_generation_permitted") is not True:
            errors.append(
                "bound calibration rights receipt requires tts_generation_permitted true"
            )
        if calibration_rights.get("permitted_use") != "bounded_calibration_only":
            errors.append("bound calibration rights receipt must permit bounded calibration only")
        if calibration_rights.get("full_capture_permitted") is not False:
            errors.append("bound calibration rights receipt must forbid full capture")

    remix_fields = {
        "owner_selection_record_path",
        "owner_selection_record_sha256",
        "saved_voice_receipt_path",
        "saved_voice_receipt_sha256",
    }
    if provenance_kind == "existing_ivc":
        present_remix = sorted(remix_fields.intersection(bindings))
        if present_remix:
            errors.append(
                "existing_ivc provenance must not carry remix receipt bindings: "
                + ", ".join(present_remix)
            )
        return
    if provenance_kind != "saved_remix":
        return

    missing_remix = sorted(remix_fields.difference(bindings))
    if missing_remix:
        errors.append(
            "saved_remix provenance bindings are incomplete: missing "
            + ", ".join(missing_remix)
        )
    owner_selection = _load_verified_json_binding(
        artifact_root,
        bindings,
        path_key="owner_selection_record_path",
        sha_key="owner_selection_record_sha256",
        label="bindings.owner_selection_record",
        errors=errors,
    )
    saved_voice = _load_verified_json_binding(
        artifact_root,
        bindings,
        path_key="saved_voice_receipt_path",
        sha_key="saved_voice_receipt_sha256",
        label="bindings.saved_voice_receipt",
        errors=errors,
    )
    if owner_selection is not None:
        _reject_unknown_keys(
            owner_selection,
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
            "bound owner selection",
            errors,
        )
        if owner_selection.get("schema_version") != ELEVEN_REMIX_OWNER_SELECTION_SCHEMA:
            errors.append("bound owner selection has the wrong schema")
        if owner_selection.get("owner_approved_save") is not True:
            errors.append("bound owner selection does not approve saving the selected voice")
        selected_voice_id = owner_selection.get("selected_generated_voice_id")
        if (
            not isinstance(selected_voice_id, str)
            or not selected_voice_id
            or selected_voice_id != plan_voice_id
            or selected_voice_id != action.get("voice_id")
        ):
            errors.append(
                "bound owner selection voice ID must equal the plan and authorization voice ID"
            )
        if (
            not isinstance(owner_selection.get("source_voice_id"), str)
            or not owner_selection.get("source_voice_id")
        ):
            errors.append("bound owner selection source_voice_id is required")
        _hash_value(
            owner_selection.get("selected_audio_sha256"),
            "bound owner selection selected_audio_sha256",
            errors,
        )
    if saved_voice is not None:
        _reject_unknown_keys(
            saved_voice,
            {
                "schema_version",
                "outcome",
                "authorization_id",
                "authorization_sha256",
                "authorization_consumption_record",
                "authorization_consumption_sha256",
                "provider",
                "scope",
                "source_voice_id",
                "selected_generated_voice_id",
                "selected_audio_sha256",
                "owner_selection_record_sha256",
                "request_body_sha256",
                "new_voice_id",
                "new_voice_name",
                "new_voice_category",
                "new_voice_is_owner",
                "new_voice_is_owner_status",
                "source_voice_modified",
                "new_voice_created",
                "provider_calls_made",
                "provider_identifiers",
                "readback",
                "provider_character_cost",
                "spend",
                "created_at",
            },
            "bound saved-voice receipt",
            errors,
        )
        if saved_voice.get("schema_version") != ELEVEN_REMIX_SAVE_RECEIPT_SCHEMA:
            errors.append("bound saved-voice receipt has the wrong schema")
        if saved_voice.get("provider") != "elevenlabs":
            errors.append("bound saved-voice receipt provider must be elevenlabs")
        if saved_voice.get("scope") != "elevenlabs_voice_remix_save":
            errors.append("bound saved-voice receipt scope mismatch")
        if saved_voice.get("provider_calls_made") != 1:
            errors.append("bound saved-voice receipt must report exactly one provider call")
        if saved_voice.get("outcome") != "new_voice_created_from_owner_selected_preview":
            errors.append("bound saved-voice receipt does not prove the selected preview was saved")
        if saved_voice.get("new_voice_created") is not True:
            errors.append("bound saved-voice receipt does not confirm creation of a new voice")
        if saved_voice.get("source_voice_modified") is not False:
            errors.append("bound saved-voice receipt must confirm source_voice_modified false")
        if saved_voice.get("new_voice_is_owner") is False:
            errors.append("bound saved-voice receipt reports the new voice is not owner-controlled")
        for field in ("new_voice_id", "selected_generated_voice_id"):
            if (
                saved_voice.get(field) != plan_voice_id
                or saved_voice.get(field) != action.get("voice_id")
            ):
                errors.append(
                    f"bound saved-voice receipt {field} must equal the plan and authorization voice ID"
                )
        if saved_voice.get("owner_selection_record_sha256") != bindings.get(
            "owner_selection_record_sha256"
        ):
            errors.append(
                "bound saved-voice receipt does not bind the exact owner-selection record"
            )
    if owner_selection is not None and saved_voice is not None:
        if saved_voice.get("selected_generated_voice_id") != owner_selection.get(
            "selected_generated_voice_id"
        ):
            errors.append("saved voice does not match the owner-selected preview voice ID")
        if saved_voice.get("selected_audio_sha256") != owner_selection.get(
            "selected_audio_sha256"
        ):
            errors.append("saved voice does not match the owner-selected preview audio")
        if saved_voice.get("source_voice_id") != owner_selection.get("source_voice_id"):
            errors.append("saved voice source does not match the owner-selection record")
    if (
        calibration_rights is not None
        and calibration_rights.get("saved_voice_receipt_sha256")
        != bindings.get("saved_voice_receipt_sha256")
    ):
        errors.append(
            "bound calibration rights receipt does not bind the exact saved-voice receipt"
        )


def _validate_new_local_destination(
    root: Path,
    path_value: Any,
    label: str,
    errors: list[str],
    *,
    required_prefix: str,
) -> Path | None:
    relative = _safe_relative(path_value, label, errors)
    if relative is None:
        return None
    if not relative.parts or relative.parts[0] != required_prefix:
        errors.append(f"{label} must remain under {required_prefix}/")
    candidate = root / relative
    try:
        resolved = candidate.resolve(strict=False)
    except OSError as exc:
        errors.append(f"cannot resolve {label}: {exc}")
        return None
    if not resolved.is_relative_to(root.resolve()):
        errors.append(f"{label} escapes the local artifact root through traversal or symlink")
        return None
    if candidate.exists():
        errors.append(f"{label} already exists; authorization may not overwrite it")
    return candidate


def _resolve_declared_path(document_path: Path, value: Any, label: str, errors: list[str]) -> Path | None:
    """Resolve a read-only portable binding, including intentional sibling `..`."""
    if not isinstance(value, str) or not value or Path(value).is_absolute():
        errors.append(f"{label} must be a non-empty relative path")
        return None
    try:
        return (document_path.parent / value).resolve(strict=False)
    except OSError as exc:
        errors.append(f"cannot resolve {label}: {exc}")
        return None


def _scan_for_secrets(value: Any, label: str = "document") -> list[str]:
    errors: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            normalized = str(key).strip().lower().replace("-", "_")
            if normalized in FORBIDDEN_SECRET_KEYS or normalized.endswith("_password"):
                errors.append(f"{label}.{key} is forbidden; credentials must not appear in artifacts")
            errors.extend(_scan_for_secrets(child, f"{label}.{key}"))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            errors.extend(_scan_for_secrets(child, f"{label}[{index}]"))
    elif isinstance(value, str):
        lowered = value.lower()
        if re.search(r"\b(?:sk|xi|key)-[a-z0-9_-]{16,}\b", lowered):
            errors.append(f"{label} appears to contain a provider credential")
    return errors


def _scan_envelope_provider_fields(value: Any, label: str = "performance_envelope") -> list[str]:
    errors: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            normalized = str(key).strip().lower().replace("-", "_")
            if normalized in FORBIDDEN_ENVELOPE_PROVIDER_KEYS:
                errors.append(
                    f"{label}.{key} is forbidden; the performance envelope must remain provider-neutral"
                )
            errors.extend(_scan_envelope_provider_fields(child, f"{label}.{key}"))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            errors.extend(_scan_envelope_provider_fields(child, f"{label}[{index}]"))
    return errors


def _validate_target(target: Any, label: str, errors: list[str]) -> None:
    if (
        not isinstance(target, dict)
        or target.get("kind") not in {"fixture", "episode"}
        or not isinstance(target.get("id"), str)
        or not target.get("id")
    ):
        errors.append(f"{label} requires kind fixture|episode and a non-empty id")


def _reject_unknown_keys(
    value: Any,
    allowed: Iterable[str],
    label: str,
    errors: list[str],
) -> None:
    if not isinstance(value, dict):
        return
    unknown = sorted(set(value) - set(allowed))
    if unknown:
        errors.append(f"{label} contains unsupported keys: {', '.join(unknown)}")


def _check_exact_file_binding(
    document_path: Path,
    binding: Any,
    actual_path: Path,
    label: str,
    errors: list[str],
) -> None:
    if not isinstance(binding, dict):
        errors.append(f"{label} must be a path/hash object")
        return
    expected_hash = binding.get("sha256")
    hash_valid = _hash_value(expected_hash, f"{label}.sha256", errors)
    declared = _resolve_declared_path(document_path, binding.get("path"), f"{label}.path", errors)
    if declared is not None and declared != actual_path.resolve():
        errors.append(f"{label}.path does not resolve to the supplied canonical file")
    if not actual_path.is_file():
        errors.append(f"{label} file is missing: {actual_path}")
    elif hash_valid and sha256_file(actual_path) != expected_hash:
        errors.append(f"{label} hash mismatch")


def _validate_partition(
    parts: Any,
    label: str,
    passage_start: int,
    passage_end: int,
    tokens: list[str],
    errors: list[str],
    *,
    hume: bool = False,
) -> list[dict[str, Any]]:
    if not isinstance(parts, list) or not parts:
        errors.append(f"{label} must be a non-empty array")
        return []
    cursor = passage_start
    ids: set[str] = set()
    valid: list[dict[str, Any]] = []
    for index, part in enumerate(parts):
        item_label = f"{label}[{index}]"
        if not isinstance(part, dict):
            errors.append(f"{item_label} must be an object")
            continue
        _reject_unknown_keys(
            part,
            {"id", "start_token", "end_token", "spoken_text_sha256"},
            item_label,
            errors,
        )
        part_id = part.get("id")
        if not isinstance(part_id, str) or not part_id or part_id in ids:
            errors.append(f"{item_label}.id must be non-empty and unique")
        else:
            ids.add(part_id)
        start, end = part.get("start_token"), part.get("end_token")
        if not _is_int(start) or not _is_int(end) or start != cursor or end <= start or end > passage_end:
            errors.append(f"{item_label} does not form a contiguous half-open partition")
            continue
        cursor = end
        actual_hash = token_identity(tokens[start:end])["sha256"]
        if part.get("spoken_text_sha256") != actual_hash:
            errors.append(f"{item_label}.spoken_text_sha256 mismatch")
        if hume:
            description = part.get("description")
            if not isinstance(description, str) or not description.strip():
                errors.append(f"{item_label}.description must be non-empty")
            elif len(description) > 1000:
                errors.append(f"{item_label}.description exceeds 1000 characters")
            silence = part.get("trailing_silence")
            if not _is_number(silence) or silence < 0 or silence > 10:
                errors.append(f"{item_label}.trailing_silence must be between 0 and 10 seconds")
        valid.append(part)
    if cursor != passage_end:
        errors.append(f"{label} does not end at passage token {passage_end}")
    return valid


def validate_performance_envelope(envelope_path: Path, canonical_w_path: Path) -> dict[str, Any]:
    envelope = read_json(envelope_path)
    tokens = read_canonical_w(canonical_w_path)
    identity = token_identity(tokens)
    errors = _scan_for_secrets(envelope)
    errors.extend(_scan_envelope_provider_fields(envelope))
    _reject_unknown_keys(
        envelope,
        {
            "schema_version",
            "envelope_id",
            "status",
            "target",
            "episode_number",
            "step3_authorized",
            "script",
            "canonical_w",
            "public_fact_clearance",
            "performance",
            "passages",
        },
        "performance_envelope",
        errors,
    )
    if envelope.get("schema_version") != PERFORMANCE_ENVELOPE_SCHEMA:
        errors.append(f"schema_version must be {PERFORMANCE_ENVELOPE_SCHEMA}")
    if not isinstance(envelope.get("envelope_id"), str) or not envelope.get("envelope_id"):
        errors.append("envelope_id is required")
    if envelope.get("status") not in {"draft", "dry_run_frozen", "frozen"}:
        errors.append("status must be draft, dry_run_frozen, or frozen")
    _validate_target(envelope.get("target"), "target", errors)
    _reject_unknown_keys(envelope.get("target"), {"kind", "id"}, "target", errors)
    if envelope.get("step3_authorized") is not False:
        errors.append("performance envelopes may not authorize Step 3")
    if envelope.get("public_fact_clearance") is not False:
        errors.append("performance envelopes must not duplicate or grant public-fact clearance")

    canonical = envelope.get("canonical_w")
    _reject_unknown_keys(
        canonical,
        {
            "path",
            "sha256",
            "schema_version",
            "tokenization",
            "serialization",
            "token_count",
        },
        "canonical_w",
        errors,
    )
    _check_exact_file_binding(envelope_path, canonical, canonical_w_path, "canonical_w", errors)
    if isinstance(canonical, dict):
        if canonical.get("schema_version") != identity["schema_version"]:
            errors.append("canonical_w.schema_version mismatch")
        if canonical.get("tokenization") != "python-str-split-whitespace":
            errors.append("canonical_w.tokenization mismatch")
        if canonical.get("serialization") != "utf8-one-token-per-lf-with-terminal-lf":
            errors.append("canonical_w.serialization mismatch")
        if canonical.get("token_count") != len(tokens):
            errors.append("canonical_w.token_count mismatch")
        if canonical.get("sha256") != identity["sha256"]:
            errors.append("canonical_w.sha256 mismatch")

    script = envelope.get("script")
    if not isinstance(script, dict):
        errors.append("script must be a path/hash object")
    else:
        _reject_unknown_keys(script, {"path", "sha256"}, "script", errors)
        script_hash_ok = _hash_value(script.get("sha256"), "script.sha256", errors)
        script_path = _resolve_declared_path(envelope_path, script.get("path"), "script.path", errors)
        if script_path is not None:
            if not script_path.is_file():
                errors.append(f"script.path is missing: {script_path}")
            elif script_hash_ok and sha256_file(script_path) != script.get("sha256"):
                errors.append("script.sha256 mismatch")

    performance = envelope.get("performance")
    if not isinstance(performance, dict):
        errors.append("performance must define the listener relationship and performance target")
    else:
        _reject_unknown_keys(
            performance,
            {
                "listener",
                "relationship",
                "identity_target",
                "energy_arc",
                "must_preserve",
                "must_avoid",
                "states",
            },
            "performance",
            errors,
        )
        for field in ("listener", "relationship", "identity_target", "energy_arc"):
            if not isinstance(performance.get(field), str) or not performance.get(field).strip():
                errors.append(f"performance.{field} is required")
        for field in ("must_preserve", "must_avoid"):
            values = performance.get(field)
            if not isinstance(values, list) or not values or any(not isinstance(v, str) or not v.strip() for v in values):
                errors.append(f"performance.{field} must be a non-empty string array")
        states = performance.get("states")
        if not isinstance(states, list) or not states:
            errors.append("performance.states must be a non-empty array")
        else:
            state_ids: set[str] = set()
            for index, state in enumerate(states):
                if not isinstance(state, dict):
                    errors.append(f"performance.states[{index}] must be an object")
                    continue
                _reject_unknown_keys(
                    state, {"id", "sound"}, f"performance.states[{index}]", errors
                )
                state_id = state.get("id")
                if not isinstance(state_id, str) or not state_id or state_id in state_ids:
                    errors.append(f"performance.states[{index}].id must be non-empty and unique")
                else:
                    state_ids.add(state_id)
                if not isinstance(state.get("sound"), str) or not state.get("sound").strip():
                    errors.append(f"performance.states[{index}].sound is required")

    passages = envelope.get("passages")
    if not isinstance(passages, list) or not passages:
        errors.append("passages must be a non-empty array")
        passages = []
    passage_ids: set[str] = set()
    ranges: list[tuple[int, int]] = []
    for index, passage in enumerate(passages):
        label = f"passages[{index}]"
        if not isinstance(passage, dict):
            errors.append(f"{label} must be an object")
            continue
        _reject_unknown_keys(
            passage,
            {
                "id",
                "source_blocks",
                "start_token",
                "end_token",
                "token_count",
                "spoken_text_sha256",
                "transport_text",
                "performance_function",
                "objective",
                "state_arc",
                "energy",
                "required_anchors",
                "anti_targets",
                "paragraph_boundaries",
                "thought_boundaries",
            },
            label,
            errors,
        )
        passage_id = passage.get("id")
        if not isinstance(passage_id, str) or not passage_id or passage_id in passage_ids:
            errors.append(f"{label}.id must be non-empty and unique")
        else:
            passage_ids.add(passage_id)
        start, end = passage.get("start_token"), passage.get("end_token")
        if not _is_int(start) or not _is_int(end) or start < 0 or end <= start or end > len(tokens):
            errors.append(f"{label} has an invalid half-open token range")
            continue
        if any(not (end <= prior_start or start >= prior_end) for prior_start, prior_end in ranges):
            errors.append(f"{label} overlaps another passage")
        ranges.append((start, end))
        actual_slice = tokens[start:end]
        if passage.get("token_count") != end - start:
            errors.append(f"{label}.token_count mismatch")
        if passage.get("spoken_text_sha256") != token_identity(actual_slice)["sha256"]:
            errors.append(f"{label}.spoken_text_sha256 mismatch")
        if not isinstance(passage.get("performance_function"), str) or not passage.get("performance_function").strip():
            errors.append(f"{label}.performance_function is required")
        if not isinstance(passage.get("objective"), str) or not passage.get("objective").strip():
            errors.append(f"{label}.objective is required")
        for field in ("state_arc", "anti_targets"):
            values = passage.get(field)
            if (
                not isinstance(values, list)
                or not values
                or any(not isinstance(value, str) or not value.strip() for value in values)
            ):
                errors.append(f"{label}.{field} must be a non-empty string array")
        if isinstance(passage.get("state_arc"), list) and isinstance(performance, dict):
            known_states = {
                state.get("id")
                for state in performance.get("states", [])
                if isinstance(state, dict)
            }
            unknown_states = [state for state in passage["state_arc"] if state not in known_states]
            if unknown_states:
                errors.append(f"{label}.state_arc references unknown states: {', '.join(unknown_states)}")
        energy = passage.get("energy")
        if not isinstance(energy, dict) or energy.get("scale") != "0_to_10":
            errors.append(f"{label}.energy must use scale 0_to_10")
        else:
            _reject_unknown_keys(
                energy,
                {"scale", "start", "peak", "finish", "instruction"},
                f"{label}.energy",
                errors,
            )
            for field in ("start", "peak", "finish"):
                value = energy.get(field)
                if not _is_number(value) or value < 0 or value > 10:
                    errors.append(f"{label}.energy.{field} must be between 0 and 10")
            if not isinstance(energy.get("instruction"), str) or not energy.get("instruction").strip():
                errors.append(f"{label}.energy.instruction is required")
        anchors = passage.get("required_anchors")
        if not isinstance(anchors, list) or not anchors:
            errors.append(f"{label}.required_anchors must be a non-empty array")
        else:
            anchor_positions: set[int] = set()
            for anchor_index, anchor in enumerate(anchors):
                anchor_label = f"{label}.required_anchors[{anchor_index}]"
                if not isinstance(anchor, dict):
                    errors.append(f"{anchor_label} must be an object")
                    continue
                _reject_unknown_keys(
                    anchor,
                    {"at_token", "kind", "instruction"},
                    anchor_label,
                    errors,
                )
                at_token = anchor.get("at_token")
                if (
                    not _is_int(at_token)
                    or at_token < start
                    or at_token >= end
                    or at_token in anchor_positions
                ):
                    errors.append(f"{anchor_label}.at_token must be one unique absolute W boundary")
                else:
                    anchor_positions.add(at_token)
                if anchor.get("kind") not in {
                    "emphasis",
                    "pause",
                    "qualification",
                    "landing",
                    "transition",
                    "verdict",
                }:
                    errors.append(f"{anchor_label}.kind is not an approved neutral performance anchor")
                if not isinstance(anchor.get("instruction"), str) or not anchor.get("instruction").strip():
                    errors.append(f"{anchor_label}.instruction is required")

        plain_text = " ".join(actual_slice)
        if BRACKET_DIRECTION_RE.search(plain_text):
            errors.append(f"{label} canonical words contain bracketed direction")
        transport = passage.get("transport_text")
        if not isinstance(transport, dict):
            errors.append(f"{label}.transport_text must be a path/hash object")
        else:
            _reject_unknown_keys(
                transport,
                {"path", "serialization", "character_count", "sha256"},
                f"{label}.transport_text",
                errors,
            )
            transport_path = _resolve_declared_path(
                envelope_path, transport.get("path"), f"{label}.transport_text.path", errors
            )
            if transport.get("serialization") != "utf8-whitespace-normalized-single-space-no-terminal-lf":
                errors.append(f"{label}.transport_text.serialization mismatch")
            if transport.get("character_count") != len(plain_text):
                errors.append(f"{label}.transport_text.character_count mismatch")
            expected_transport_hash = sha256_bytes(plain_text.encode("utf-8"))
            if transport.get("sha256") != expected_transport_hash:
                errors.append(f"{label}.transport_text.sha256 mismatch")
            if transport_path is not None:
                if not transport_path.is_file():
                    errors.append(f"{label}.transport_text.path is missing")
                else:
                    try:
                        actual_bytes = transport_path.read_bytes()
                    except OSError as exc:
                        errors.append(f"cannot read {label}.transport_text.path: {exc}")
                    else:
                        if actual_bytes != plain_text.encode("utf-8"):
                            errors.append(f"{label}.transport_text does not equal its exact W slice")

        _validate_partition(
            passage.get("paragraph_boundaries"),
            f"{label}.paragraph_boundaries",
            start,
            end,
            tokens,
            errors,
        )
        _validate_partition(
            passage.get("thought_boundaries"),
            f"{label}.thought_boundaries",
            start,
            end,
            tokens,
            errors,
        )

    if errors:
        raise ValidationError(errors)
    return {
        "valid": True,
        "schema_version": PERFORMANCE_ENVELOPE_SCHEMA,
        "envelope_sha256": sha256_file(envelope_path),
        "canonical_w_sha256": identity["sha256"],
        "token_count": len(tokens),
        "passage_count": len(passages),
        "passage_ids": [passage["id"] for passage in passages],
        "step3_authorized": False,
    }


def _find_passage(envelope: dict[str, Any], passage_id: str) -> dict[str, Any]:
    return next(passage for passage in envelope["passages"] if passage["id"] == passage_id)


def _bound_adapter_path(
    plan_path: Path,
    binding: Any,
    provider: str,
    errors: list[str],
) -> Path | None:
    if not isinstance(binding, dict):
        errors.append(f"provider_adapters.{provider} must be a path/hash object")
        return None
    _reject_unknown_keys(
        binding,
        {"path", "sha256"},
        f"provider_adapters.{provider}",
        errors,
    )
    expected_hash = binding.get("sha256")
    valid_hash = _hash_value(expected_hash, f"provider_adapters.{provider}.sha256", errors)
    path = _resolve_declared_path(
        plan_path, binding.get("path"), f"provider_adapters.{provider}.path", errors
    )
    if path is not None:
        if not path.is_file():
            errors.append(f"provider_adapters.{provider}.path is missing: {path}")
        elif valid_hash and sha256_file(path) != expected_hash:
            errors.append(f"provider_adapters.{provider}.sha256 mismatch")
    return path


def _adapter_passage(adapter: dict[str, Any], passage_id: str) -> dict[str, Any]:
    return next(passage for passage in adapter["passages"] if passage["passage_id"] == passage_id)


def validate_provider_adapter(
    adapter_path: Path,
    envelope_path: Path,
    canonical_w_path: Path,
) -> dict[str, Any]:
    validate_performance_envelope(envelope_path, canonical_w_path)
    adapter = read_json(adapter_path)
    envelope = read_json(envelope_path)
    tokens = read_canonical_w(canonical_w_path)
    errors = _scan_for_secrets(adapter)
    if adapter.get("schema_version") != PROVIDER_ADAPTER_SCHEMA:
        errors.append(f"schema_version must be {PROVIDER_ADAPTER_SCHEMA}")
    if not isinstance(adapter.get("adapter_id"), str) or not adapter.get("adapter_id"):
        errors.append("adapter_id is required")
    if adapter.get("status") not in {"draft", "dry_run_frozen", "frozen"}:
        errors.append("adapter status must be draft, dry_run_frozen, or frozen")
    _validate_target(adapter.get("target"), "target", errors)
    _reject_unknown_keys(adapter.get("target"), {"kind", "id"}, "target", errors)
    if adapter.get("target") != envelope.get("target"):
        errors.append("adapter target does not match the performance envelope")
    provider = adapter.get("provider")
    if provider not in {"elevenlabs", "hume"}:
        errors.append("provider must be elevenlabs or hume")
    common_adapter_keys = {
        "schema_version",
        "adapter_id",
        "status",
        "target",
        "provider",
        "performance_envelope",
        "canonical_w",
        "model_id",
        "passages",
    }
    provider_adapter_keys = (
        {
            "voice_id",
            "approved_tag_allowlist",
            "paragraph_separator",
            "exact_word_recovery",
            "tag_policy",
            "voice_settings",
        }
        if provider == "elevenlabs"
        else {"clone_voice_id", "clone_state", "description_policy"}
    )
    _reject_unknown_keys(
        adapter,
        common_adapter_keys | provider_adapter_keys,
        "provider_adapter",
        errors,
    )
    _reject_unknown_keys(
        adapter.get("performance_envelope"),
        {"path", "sha256"},
        "performance_envelope",
        errors,
    )
    _reject_unknown_keys(
        adapter.get("canonical_w"),
        {"path", "sha256"},
        "canonical_w",
        errors,
    )
    _check_exact_file_binding(
        adapter_path,
        adapter.get("performance_envelope"),
        envelope_path,
        "performance_envelope",
        errors,
    )
    _check_exact_file_binding(
        adapter_path,
        adapter.get("canonical_w"),
        canonical_w_path,
        "canonical_w",
        errors,
    )
    passage_ids = [passage["id"] for passage in envelope["passages"]]
    adapter_passages = adapter.get("passages")
    if not isinstance(adapter_passages, list):
        errors.append("adapter passages must be an array")
        adapter_passages = []
    actual_ids = [passage.get("passage_id") for passage in adapter_passages if isinstance(passage, dict)]
    if actual_ids != passage_ids:
        errors.append("adapter passages must exactly match the ordered envelope passages")

    if provider == "elevenlabs":
        if adapter.get("model_id") != "eleven_v3":
            errors.append("ElevenLabs adapter model_id must be eleven_v3")
        if not isinstance(adapter.get("voice_id"), str) or not adapter.get("voice_id"):
            errors.append("ElevenLabs adapter voice_id is required")
        if adapter.get("paragraph_separator") != "\n\n":
            errors.append("ElevenLabs adapter paragraph_separator must be exactly double LF")
        if not isinstance(adapter.get("exact_word_recovery"), str) or not adapter.get("exact_word_recovery"):
            errors.append("ElevenLabs adapter exact_word_recovery contract is required")
        if not isinstance(adapter.get("tag_policy"), str) or not adapter.get("tag_policy"):
            errors.append("ElevenLabs adapter tag_policy is required")
        adapter_settings = adapter.get("voice_settings")
        if not isinstance(adapter_settings, dict) or set(adapter_settings) != {
            "stability",
            "similarity_boost",
            "style",
        }:
            errors.append("ElevenLabs adapter voice_settings must contain only the three frozen controls")
        elif any(
            not _is_number(value) or value < 0 or value > 1
            for value in adapter_settings.values()
        ):
            errors.append("ElevenLabs adapter voice settings must be finite values from 0 through 1")
        _reject_unknown_keys(
            adapter_settings,
            {"stability", "similarity_boost", "style"},
            "voice_settings",
            errors,
        )
        allowlist = adapter.get("approved_tag_allowlist")
        if (
            not isinstance(allowlist, list)
            or len(allowlist) != len(set(allowlist))
            or set(allowlist) != ELEVEN_ALLOWED_TAGS
        ):
            errors.append("ElevenLabs adapter allowlist must contain exactly the five approved tags")
        for index, adapter_passage in enumerate(adapter_passages):
            if not isinstance(adapter_passage, dict) or adapter_passage.get("passage_id") not in passage_ids:
                continue
            _reject_unknown_keys(
                adapter_passage,
                {"passage_id", "tag_insertions"},
                f"passages[{index}]",
                errors,
            )
            envelope_passage = _find_passage(envelope, adapter_passage["passage_id"])
            insertions = adapter_passage.get("tag_insertions")
            if not isinstance(insertions, list) or not insertions:
                errors.append(f"passages[{index}].tag_insertions must be a non-empty array")
                continue
            anchors: set[int] = set()
            for tag_index, insertion in enumerate(insertions):
                label = f"passages[{index}].tag_insertions[{tag_index}]"
                if not isinstance(insertion, dict):
                    errors.append(f"{label} must be an object")
                    continue
                _reject_unknown_keys(
                    insertion, {"at_token", "tag"}, label, errors
                )
                anchor, tag = insertion.get("at_token"), insertion.get("tag")
                if (
                    not _is_int(anchor)
                    or anchor < envelope_passage["start_token"]
                    or anchor >= envelope_passage["end_token"]
                    or anchor in anchors
                ):
                    errors.append(f"{label}.at_token must be one unique absolute W boundary")
                else:
                    anchors.add(anchor)
                if tag not in ELEVEN_ALLOWED_TAGS or tag not in set(allowlist or []):
                    errors.append(f"{label}.tag is outside the exact allowlist")

    if provider == "hume":
        if adapter.get("model_id") != "octave-1":
            errors.append("Hume adapter model_id must be octave-1")
        if not isinstance(adapter.get("clone_voice_id"), str) or not adapter.get("clone_voice_id"):
            errors.append("Hume adapter clone_voice_id is required")
        if not isinstance(adapter.get("clone_state"), str) or not adapter.get("clone_state"):
            errors.append("Hume adapter clone_state is required")
        if not isinstance(adapter.get("description_policy"), str) or not adapter.get("description_policy"):
            errors.append("Hume adapter description_policy is required")
        for index, adapter_passage in enumerate(adapter_passages):
            if not isinstance(adapter_passage, dict) or adapter_passage.get("passage_id") not in passage_ids:
                continue
            _reject_unknown_keys(
                adapter_passage,
                {
                    "passage_id",
                    "passage_description",
                    "passage_description_sha256",
                    "description_expansion_sha256",
                    "thought_directions",
                },
                f"passages[{index}]",
                errors,
            )
            envelope_passage = _find_passage(envelope, adapter_passage["passage_id"])
            passage_description = adapter_passage.get("passage_description")
            if not isinstance(passage_description, str) or not passage_description.strip():
                errors.append(f"passages[{index}].passage_description is required")
                passage_description = ""
            elif len(passage_description) > 1000:
                errors.append(f"passages[{index}].passage_description exceeds 1000 characters")
            expected_passage_hash = sha256_bytes(passage_description.encode("utf-8"))
            if adapter_passage.get("passage_description_sha256") != expected_passage_hash:
                errors.append(f"passages[{index}].passage_description_sha256 mismatch")
            directions = adapter_passage.get("thought_directions")
            if not isinstance(directions, list):
                errors.append(f"passages[{index}].thought_directions must be an array")
                directions = []
            thought_boundaries = envelope_passage["thought_boundaries"]
            expected_thought_ids = [thought["id"] for thought in thought_boundaries]
            actual_thought_ids = [
                direction.get("thought_id") for direction in directions if isinstance(direction, dict)
            ]
            if actual_thought_ids != expected_thought_ids:
                errors.append(
                    f"passages[{index}].thought_directions must exactly match neutral thought boundaries"
                )
            emitted_hashes: list[str] = []
            for direction_index, direction_record in enumerate(directions):
                label = f"passages[{index}].thought_directions[{direction_index}]"
                if not isinstance(direction_record, dict):
                    errors.append(f"{label} must be an object")
                    continue
                _reject_unknown_keys(
                    direction_record,
                    {
                        "thought_id",
                        "direction",
                        "direction_sha256",
                        "emitted_description",
                        "emitted_description_sha256",
                        "trailing_silence",
                    },
                    label,
                    errors,
                )
                direction = direction_record.get("direction")
                if not isinstance(direction, str) or not direction.strip():
                    errors.append(f"{label}.direction is required")
                    continue
                direction_hash = sha256_bytes(direction.encode("utf-8"))
                if direction_record.get("direction_sha256") != direction_hash:
                    errors.append(f"{label}.direction_sha256 mismatch")
                emitted = f"{passage_description} Thought direction: {direction}"
                if direction_record.get("emitted_description") != emitted:
                    errors.append(f"{label}.emitted_description is not the exact approved expansion")
                if len(emitted) > 1000:
                    errors.append(f"{label}.emitted_description exceeds 1000 characters")
                emitted_hash = sha256_bytes(emitted.encode("utf-8"))
                emitted_hashes.append(emitted_hash)
                if direction_record.get("emitted_description_sha256") != emitted_hash:
                    errors.append(f"{label}.emitted_description_sha256 mismatch")
                silence = direction_record.get("trailing_silence")
                if not _is_number(silence) or silence < 0 or silence > 10:
                    errors.append(f"{label}.trailing_silence must be between 0 and 10 seconds")
            expansion_hash = sha256_bytes(("\n".join(emitted_hashes) + ("\n" if emitted_hashes else "")).encode("utf-8"))
            if adapter_passage.get("description_expansion_sha256") != expansion_hash:
                errors.append(f"passages[{index}].description_expansion_sha256 mismatch")

    if errors:
        raise ValidationError(errors)
    return {
        "valid": True,
        "schema_version": PROVIDER_ADAPTER_SCHEMA,
        "adapter_sha256": sha256_file(adapter_path),
        "provider": provider,
        "passage_count": len(adapter_passages),
        "canonical_w_sha256": token_identity(tokens)["sha256"],
    }


def _compile_eleven_text(
    passage: dict[str, Any],
    adapter_passage: dict[str, Any],
    tokens: list[str],
) -> str:
    insertions = {
        insertion["at_token"]: insertion["tag"]
        for insertion in adapter_passage["tag_insertions"]
    }
    paragraphs: list[str] = []
    for paragraph in passage["paragraph_boundaries"]:
        rendered: list[str] = []
        for absolute_index in range(paragraph["start_token"], paragraph["end_token"]):
            if absolute_index in insertions:
                rendered.append(insertions[absolute_index])
            rendered.append(tokens[absolute_index])
        paragraphs.append(" ".join(rendered))
    compiled = "\n\n".join(paragraphs)
    found_directions = BRACKET_DIRECTION_RE.findall(compiled)
    if any(direction not in ELEVEN_ALLOWED_TAGS for direction in found_directions):
        raise ValidationError("compiled ElevenLabs text contains unsupported bracketed direction")
    stripped = compiled
    for tag in ELEVEN_ALLOWED_TAGS:
        stripped = stripped.replace(tag, " ")
    if stripped.split() != tokens[passage["start_token"] : passage["end_token"]]:
        raise ValidationError("compiled ElevenLabs transport changes canonical W")
    if len(compiled) > 5000:
        raise ValidationError("compiled ElevenLabs text exceeds the 5000-character request ceiling")
    return compiled


def _compile_hume_body(
    passage: dict[str, Any],
    adapter_passage: dict[str, Any],
    tokens: list[str],
    voice_id: str,
) -> dict[str, Any]:
    utterances: list[dict[str, Any]] = []
    assembled: list[str] = []
    text_characters = 0
    directions = {
        direction["thought_id"]: direction
        for direction in adapter_passage["thought_directions"]
    }
    for thought in passage["thought_boundaries"]:
        direction = directions[thought["id"]]
        text = " ".join(tokens[thought["start_token"] : thought["end_token"]])
        assembled.extend(text.split())
        text_characters += len(text)
        utterance = {
            "text": text,
            "description": direction["emitted_description"],
            "voice": {"id": voice_id},
            "trailing_silence": direction["trailing_silence"],
        }
        if set(utterance["voice"]) != {"id"}:
            raise ValidationError("Hume custom voice selector may contain only id")
        utterances.append(utterance)
    expected = tokens[passage["start_token"] : passage["end_token"]]
    if assembled != expected:
        raise ValidationError("compiled Hume utterances change canonical W")
    if text_characters > 5000:
        raise ValidationError("compiled Hume dialogue exceeds the 5000-character request ceiling")
    return {
        "version": "1",
        "utterances": utterances,
        "format": {"type": "wav"},
        "num_generations": 2,
        "split_utterances": False,
        "strip_headers": True,
    }


def _validate_destination(value: Any, label: str, suffix: str, errors: list[str]) -> str | None:
    path = _safe_relative(value, label, errors)
    if path is None:
        return None
    if path.suffix.lower() != suffix:
        errors.append(f"{label} must end in {suffix}")
    if not path.parts or path.parts[0] != "outputs":
        errors.append(f"{label} must remain under the local outputs/ area")
    return path.as_posix()


def _validate_plan_and_compile(
    plan_path: Path,
    envelope_path: Path,
    canonical_w_path: Path,
) -> tuple[dict[str, Any], dict[str, Any], list[str], list[dict[str, Any]]]:
    envelope_validation = validate_performance_envelope(envelope_path, canonical_w_path)
    plan = read_json(plan_path)
    envelope = read_json(envelope_path)
    tokens = read_canonical_w(canonical_w_path)
    errors = _scan_for_secrets(plan)
    _reject_unknown_keys(
        plan,
        {
            "schema_version",
            "plan_id",
            "status",
            "target",
            "performance_envelope",
            "provider_adapters",
            "canonical_w",
            "passage_ids",
            "candidates_per_passage_per_provider",
            "expected_candidate_count",
            "providers",
            "external_action_authorized",
            "credentials_may_be_accessed",
            "audio_may_be_generated",
        },
        "plan",
        errors,
    )
    if plan.get("schema_version") != PROVIDER_BAKEOFF_PLAN_SCHEMA:
        errors.append(f"schema_version must be {PROVIDER_BAKEOFF_PLAN_SCHEMA}")
    if not isinstance(plan.get("plan_id"), str) or not plan.get("plan_id"):
        errors.append("plan_id is required")
    if plan.get("status") != "dry_run_only":
        errors.append("provider bakeoff plan status must be dry_run_only")
    _validate_target(plan.get("target"), "target", errors)
    _reject_unknown_keys(plan.get("target"), {"kind", "id"}, "target", errors)
    if plan.get("target") != envelope.get("target"):
        errors.append("plan target does not match performance envelope target")
    if plan.get("external_action_authorized") is not False:
        errors.append("provider bakeoff plans may not authorize external action")
    if plan.get("credentials_may_be_accessed") is not False:
        errors.append("provider bakeoff plans may not permit credential access")
    if plan.get("audio_may_be_generated") is not False:
        errors.append("provider bakeoff plans may not authorize audio generation")

    _check_exact_file_binding(plan_path, plan.get("performance_envelope"), envelope_path, "performance_envelope", errors)
    _reject_unknown_keys(
        plan.get("performance_envelope"),
        {"path", "sha256"},
        "performance_envelope",
        errors,
    )
    canonical_binding = plan.get("canonical_w")
    _check_exact_file_binding(plan_path, canonical_binding, canonical_w_path, "canonical_w", errors)
    _reject_unknown_keys(
        canonical_binding,
        {"path", "sha256", "token_count"},
        "canonical_w",
        errors,
    )
    if isinstance(canonical_binding, dict):
        if canonical_binding.get("token_count") != len(tokens):
            errors.append("canonical_w.token_count mismatch")

    adapter_bindings = plan.get("provider_adapters")
    if not isinstance(adapter_bindings, dict) or set(adapter_bindings) != {"elevenlabs", "hume"}:
        errors.append("provider_adapters must bind exactly elevenlabs and hume")
        adapter_bindings = {}
    else:
        _reject_unknown_keys(
            adapter_bindings,
            {"elevenlabs", "hume"},
            "provider_adapters",
            errors,
        )
    adapter_paths: dict[str, Path] = {}
    adapters: dict[str, dict[str, Any]] = {}
    for provider_name in ("elevenlabs", "hume"):
        adapter_path = _bound_adapter_path(
            plan_path, adapter_bindings.get(provider_name), provider_name, errors
        )
        if adapter_path is None or not adapter_path.is_file():
            continue
        adapter_paths[provider_name] = adapter_path
        try:
            validate_provider_adapter(adapter_path, envelope_path, canonical_w_path)
            adapters[provider_name] = read_json(adapter_path)
        except ValidationError as exc:
            errors.extend(exc.errors)

    passage_ids = [passage["id"] for passage in envelope["passages"]]
    if plan.get("passage_ids") != passage_ids:
        errors.append("passage_ids must exactly match the ordered performance-envelope passages")
    if plan.get("candidates_per_passage_per_provider") != 2:
        errors.append("candidates_per_passage_per_provider must be exactly 2")
    if plan.get("expected_candidate_count") != len(passage_ids) * 4:
        errors.append("expected_candidate_count must equal two candidates per passage per provider")

    providers = plan.get("providers")
    if not isinstance(providers, list) or len(providers) != 2:
        errors.append("providers must contain exactly one ElevenLabs and one Hume plan")
        providers = []
    provider_map: dict[str, dict[str, Any]] = {}
    for index, provider in enumerate(providers):
        if not isinstance(provider, dict):
            errors.append(f"providers[{index}] must be an object")
            continue
        name = provider.get("provider")
        if name not in {"elevenlabs", "hume"} or name in provider_map:
            errors.append(f"providers[{index}].provider must be unique and elevenlabs|hume")
            continue
        provider_map[name] = provider
        common = {
            "provider_id",
            "provider",
            "model_id",
            "voice_id",
            "identity_state",
            "request_mode",
            "generation_variance",
            "same_direction_for_both_candidates",
            "format_policy",
            "requests",
            "pricing_model",
        }
        provider_specific = (
            {"voice_settings"}
            if name == "elevenlabs"
            else {
                "execution_ready",
                "account_tier",
                "commercial_use_eligibility",
            }
        )
        _reject_unknown_keys(provider, common | provider_specific, f"providers[{index}]", errors)
    if set(provider_map) != {"elevenlabs", "hume"}:
        errors.append("plan must define both elevenlabs and hume")

    compiled_requests: list[dict[str, Any]] = []
    eleven = provider_map.get("elevenlabs", {})
    if eleven:
        eleven_adapter = adapters.get("elevenlabs", {})
        if eleven.get("model_id") != "eleven_v3" or eleven.get("model_id") != eleven_adapter.get("model_id"):
            errors.append("ElevenLabs model must be adapter-bound eleven_v3")
        if eleven.get("voice_id") != eleven_adapter.get("voice_id"):
            errors.append("ElevenLabs voice_id does not match its provider adapter")
        if eleven.get("request_mode") != "one_call_per_candidate":
            errors.append("ElevenLabs request_mode must be one_call_per_candidate")
        if eleven.get("generation_variance") != "paired_fixed_seed_separate_generation":
            errors.append(
                "ElevenLabs generation_variance must be paired_fixed_seed_separate_generation"
            )
        if eleven.get("same_direction_for_both_candidates") is not True:
            errors.append("ElevenLabs candidates must use identical direction")
        settings = eleven.get("voice_settings")
        if not isinstance(settings, dict) or set(settings) != {"stability", "similarity_boost", "style"}:
            errors.append("ElevenLabs voice_settings must contain only stability, similarity_boost, and style")
            settings = {}
        elif any(not _is_number(value) or value < 0 or value > 1 for value in settings.values()):
            errors.append("ElevenLabs voice settings must be finite values from 0 through 1")
        if settings != eleven_adapter.get("voice_settings"):
            errors.append("ElevenLabs plan voice_settings do not match the frozen provider adapter")
        eleven_pricing = eleven.get("pricing_model")
        if not isinstance(eleven_pricing, dict):
            errors.append("ElevenLabs pricing_model is required")
            eleven_pricing = {}
        _reject_unknown_keys(
            eleven_pricing,
            {
                "status",
                "currency",
                "public_rate_per_1000_text_characters",
                "billable_character_convention",
                "authorized_spend_usd",
            },
            "providers[elevenlabs].pricing_model",
            errors,
        )
        if eleven_pricing.get("currency") != "USD":
            errors.append("ElevenLabs pricing_model.currency must be USD")
        if eleven_pricing.get("authorized_spend_usd") != 0:
            errors.append("ElevenLabs dry-run pricing may not authorize spend")
        policy = eleven.get("format_policy")
        if not isinstance(policy, dict):
            errors.append("ElevenLabs format_policy is required")
            policy = {}
        _reject_unknown_keys(
            policy,
            {
                "requested",
                "raw_origin_if_returned",
                "fallback_policy_enabled",
                "only_permitted_fallback",
                "fallback_reason_required",
                "fallback_requires_new_bound_request",
                "fallback_requires_capability_rejection_receipt",
                "fallback_requires_actual_codec_bitrate_verification",
                "fallback_request_call_ceiling",
                "immutable_raw",
                "fallback_audible_artifact_review",
                "delivery_conversion",
                "lossy_intermediates_after_raw",
            },
            "providers[elevenlabs].format_policy",
            errors,
        )
        if policy.get("requested") != "pcm_48000":
            errors.append("ElevenLabs preferred format must be pcm_48000")
        if policy.get("immutable_raw") is not True:
            errors.append("ElevenLabs format_policy.immutable_raw must be true")
        if policy.get("lossy_intermediates_after_raw") is not False:
            errors.append("ElevenLabs format_policy.lossy_intermediates_after_raw must be false")
        fallback_enabled = policy.get("fallback_policy_enabled")
        if fallback_enabled not in {True, False}:
            errors.append("ElevenLabs format_policy.fallback_policy_enabled must be explicit")
            fallback_enabled = False
        if fallback_enabled:
            if policy.get("only_permitted_fallback") != "mp3_44100_192":
                errors.append("ElevenLabs only permitted fallback must be mp3_44100_192")
            if policy.get("fallback_reason_required") != "pcm_capability_unavailable":
                errors.append("ElevenLabs fallback must require pcm_capability_unavailable")
            if policy.get("fallback_requires_new_bound_request") is not True:
                errors.append("ElevenLabs fallback must require a new bound request")
            if policy.get("fallback_requires_capability_rejection_receipt") is not True:
                errors.append("ElevenLabs fallback requires a capability-rejection receipt")
            if policy.get("fallback_requires_actual_codec_bitrate_verification") is not True:
                errors.append("ElevenLabs fallback requires actual codec and bitrate verification")
        elif any(
            policy.get(field) not in (None, False)
            for field in (
                "only_permitted_fallback",
                "fallback_reason_required",
                "fallback_requires_new_bound_request",
                "fallback_requires_capability_rejection_receipt",
                "fallback_requires_actual_codec_bitrate_verification",
            )
        ):
            errors.append("disabled ElevenLabs fallback policy may not retain fallback claims")
        requests = eleven.get("requests")
        if not isinstance(requests, list) or len(requests) != len(passage_ids) * 2:
            errors.append("ElevenLabs must define exactly two requests per passage")
            requests = []
        expected_fallback_calls = len(requests) if fallback_enabled else 0
        if policy.get("fallback_request_call_ceiling") != expected_fallback_calls:
            errors.append(
                "ElevenLabs fallback_request_call_ceiling must equal one conditional fallback per primary request"
            )
        seen_request_ids: set[str] = set()
        passage_counts = {passage_id: 0 for passage_id in passage_ids}
        bodies_by_passage: dict[str, list[str]] = {passage_id: [] for passage_id in passage_ids}
        indexes_by_passage: dict[str, set[int]] = {passage_id: set() for passage_id in passage_ids}
        seeds_by_candidate_index: dict[int, set[int]] = {0: set(), 1: set()}
        for index, request in enumerate(requests):
            label = f"providers[elevenlabs].requests[{index}]"
            if not isinstance(request, dict):
                errors.append(f"{label} must be an object")
                continue
            _reject_unknown_keys(
                request,
                {
                    "request_id",
                    "passage_id",
                    "candidate_id",
                    "candidate_index",
                    "fixed_seed",
                    "direction_variant",
                    "destination",
                },
                label,
                errors,
            )
            request_id = request.get("request_id")
            if not isinstance(request_id, str) or not request_id or request_id in seen_request_ids:
                errors.append(f"{label}.request_id must be non-empty and unique")
            else:
                seen_request_ids.add(request_id)
            passage_id = request.get("passage_id")
            if passage_id not in passage_counts:
                errors.append(f"{label}.passage_id is not envelope-bound")
                continue
            passage_counts[passage_id] += 1
            candidate_index = request.get("candidate_index")
            if candidate_index not in {0, 1} or isinstance(candidate_index, bool):
                errors.append(f"{label}.candidate_index must be 0 or 1")
            else:
                indexes_by_passage[passage_id].add(candidate_index)
            fixed_seed = request.get("fixed_seed")
            if (
                not _is_int(fixed_seed)
                or fixed_seed < 0
                or fixed_seed > 4_294_967_295
            ):
                errors.append(f"{label}.fixed_seed must be an integer from 0 through 4294967295")
            elif candidate_index in {0, 1}:
                seeds_by_candidate_index[candidate_index].add(fixed_seed)
            if request.get("direction_variant") != "approved_identical":
                errors.append(f"{label}.direction_variant must be approved_identical")
            destination = _validate_destination(request.get("destination"), f"{label}.destination", ".pcm", errors)
            passage = _find_passage(envelope, passage_id)
            try:
                provider_text = _compile_eleven_text(
                    passage, _adapter_passage(eleven_adapter, passage_id), tokens
                )
            except ValidationError as exc:
                errors.extend(exc.errors)
                continue
            body = {
                "model_id": "eleven_v3",
                "seed": fixed_seed,
                "text": provider_text,
                "voice_settings": settings,
            }
            body_hash = _json_sha256(body)
            bodies_by_passage[passage_id].append(body_hash)
            rate = eleven_pricing.get("public_rate_per_1000_text_characters")
            if not _is_number(rate) or rate < 0:
                errors.append("ElevenLabs pricing rate must be a non-negative finite estimate")
                rate = 0
            compiled_request = {
                    "request_id": request_id,
                    "provider": "elevenlabs",
                    "provider_id": eleven.get("provider_id"),
                    "passage_id": passage_id,
                    "candidate_ids": [request.get("candidate_id")],
                    "method": "POST",
                    "url_path": f"/v1/text-to-speech/{quote(str(eleven.get('voice_id')), safe='')}",
                    "query": {"output_format": "pcm_48000"},
                    "required_header_names": ["Content-Type", "xi-api-key"],
                    "start_token": passage["start_token"],
                    "end_token": passage["end_token"],
                    "spoken_text_sha256": passage["spoken_text_sha256"],
                    "tag_insertions": _adapter_passage(eleven_adapter, passage_id)["tag_insertions"],
                    "provider_text_sha256": sha256_bytes(provider_text.encode("utf-8")),
                    "provider_text_character_count": len(provider_text),
                    "request_body": body,
                    "request_body_serialization": "utf8-json-sort-keys-compact-ensure-ascii-false-no-terminal-lf",
                    "request_body_sha256": body_hash,
                    "planned_call_count": 1,
                    "planned_output_count": 1,
                    "estimated_billable_character_count": len(provider_text),
                    "estimated_public_rate_usd_per_1000_characters": rate,
                    "estimated_public_rate_cost_usd": round(len(provider_text) / 1000 * rate, 6),
                    "destinations": [destination] if destination else [],
                    "execution_ready": False,
                    "blockers": ["separate_active_calibration_authorization_absent"],
                }
            if fallback_enabled and destination:
                fallback_destination = str(Path(destination).with_suffix(".mp3"))
                compiled_request["fallback_request"] = {
                    "enabled": True,
                    "method": "POST",
                    "url_path": compiled_request["url_path"],
                    "query": {"output_format": "mp3_44100_192"},
                    "request_body": body,
                    "request_body_sha256": body_hash,
                    "destination": fallback_destination,
                    "planned_additional_call_count": 1,
                    "estimated_additional_billable_character_count": len(provider_text),
                    "estimated_additional_public_rate_cost_usd": round(
                        len(provider_text) / 1000 * rate, 6
                    ),
                    "requires": [
                        "documented_pcm_capability_rejection_receipt",
                        "new_hash_bound_fallback_request",
                        "verified_actual_mp3_codec",
                        "verified_actual_bitrate_at_least_192000_bps",
                        "active_authorization_caps_include_fallback",
                    ],
                    "execution_ready": False,
                }
            else:
                compiled_request["fallback_request"] = {"enabled": False}
            compiled_requests.append(compiled_request)
        for passage_id in passage_ids:
            if passage_counts[passage_id] != 2 or indexes_by_passage[passage_id] != {0, 1}:
                errors.append(f"ElevenLabs passage {passage_id} must define candidate indexes 0 and 1 exactly once")
            if len(set(bodies_by_passage[passage_id])) != 2:
                errors.append(
                    f"ElevenLabs passage {passage_id} candidates must use two distinct fixed-seed bodies"
                )
        if any(len(seeds) != 1 for seeds in seeds_by_candidate_index.values()):
            errors.append(
                "ElevenLabs candidate A and B must each reuse one fixed seed across passages"
            )
        elif next(iter(seeds_by_candidate_index[0])) == next(iter(seeds_by_candidate_index[1])):
            errors.append("ElevenLabs candidate A and B fixed seeds must differ")

    hume = provider_map.get("hume", {})
    if hume:
        hume_adapter = adapters.get("hume", {})
        if hume.get("model_id") != "octave-1" or hume.get("model_id") != hume_adapter.get("model_id"):
            errors.append("Hume model must be adapter-bound octave-1")
        if hume.get("voice_id") != hume_adapter.get("clone_voice_id"):
            errors.append("Hume voice_id does not match its provider adapter")
        if hume.get("execution_ready") is not False:
            errors.append("Hume bakeoff plan execution_ready must remain false")
        if hume.get("request_mode") != "one_call_per_passage_two_generations":
            errors.append("Hume request_mode must be one_call_per_passage_two_generations")
        if hume.get("same_direction_for_both_candidates") is not True:
            errors.append("Hume candidates must use identical direction")
        if hume.get("generation_variance") != "num_generations_2":
            errors.append("Hume generation variance must be num_generations_2")
        hume_pricing = hume.get("pricing_model")
        if not isinstance(hume_pricing, dict):
            errors.append("Hume pricing_model is required")
            hume_pricing = {}
        _reject_unknown_keys(
            hume_pricing,
            {
                "status",
                "currency",
                "public_creator_overage_rate_per_1000_text_characters",
                "billable_character_convention",
                "authorized_spend_usd",
            },
            "providers[hume].pricing_model",
            errors,
        )
        if hume_pricing.get("currency") != "USD":
            errors.append("Hume pricing_model.currency must be USD")
        if hume_pricing.get("authorized_spend_usd") != 0:
            errors.append("Hume dry-run pricing may not authorize spend")
        hume_policy = hume.get("format_policy")
        if not isinstance(hume_policy, dict):
            errors.append("Hume format_policy is required")
            hume_policy = {}
        _reject_unknown_keys(
            hume_policy,
            {
                "requested",
                "actual_container_and_codec_inspection_required",
                "fallback_policy_enabled",
                "only_permitted_fallback",
                "fallback_reason_required",
                "fallback_requires_new_bound_request",
                "fallback_requires_capability_rejection_receipt",
                "fallback_requires_actual_codec_bitrate_verification",
                "fallback_request_call_ceiling",
                "fallback_audible_artifact_review",
                "immutable_raw",
                "delivery_conversion",
                "lossy_intermediates_after_raw",
            },
            "providers[hume].format_policy",
            errors,
        )
        if hume_policy.get("requested") != "wav":
            errors.append("Hume requested format must be wav")
        if hume_policy.get("immutable_raw") is not True:
            errors.append("Hume format_policy.immutable_raw must be true")
        if hume_policy.get("lossy_intermediates_after_raw") is not False:
            errors.append("Hume format_policy.lossy_intermediates_after_raw must be false")
        hume_fallback_enabled = hume_policy.get("fallback_policy_enabled")
        if hume_fallback_enabled not in {True, False}:
            errors.append("Hume format_policy.fallback_policy_enabled must be explicit")
            hume_fallback_enabled = False
        if hume_fallback_enabled:
            if hume_policy.get("only_permitted_fallback") != "mp3_44100_192":
                errors.append("Hume only permitted fallback must be mp3_44100_192")
            if hume_policy.get("fallback_reason_required") != "lossless_capability_unavailable":
                errors.append("Hume fallback must require lossless_capability_unavailable")
            if hume_policy.get("fallback_requires_new_bound_request") is not True:
                errors.append("Hume fallback must require a new bound request")
            if hume_policy.get("fallback_requires_capability_rejection_receipt") is not True:
                errors.append("Hume fallback requires a capability-rejection receipt")
            if hume_policy.get("fallback_requires_actual_codec_bitrate_verification") is not True:
                errors.append("Hume fallback requires actual codec and bitrate verification")
        elif any(
            hume_policy.get(field) not in (None, False)
            for field in (
                "only_permitted_fallback",
                "fallback_reason_required",
                "fallback_requires_new_bound_request",
                "fallback_requires_capability_rejection_receipt",
                "fallback_requires_actual_codec_bitrate_verification",
            )
        ):
            errors.append("disabled Hume fallback policy may not retain fallback claims")
        requests = hume.get("requests")
        if not isinstance(requests, list) or len(requests) != len(passage_ids):
            errors.append("Hume must define exactly one request per passage")
            requests = []
        expected_hume_fallback_calls = len(requests) if hume_fallback_enabled else 0
        if hume_policy.get("fallback_request_call_ceiling") != expected_hume_fallback_calls:
            errors.append(
                "Hume fallback_request_call_ceiling must equal one conditional fallback per primary request"
            )
        seen_request_ids: set[str] = set()
        seen_passages: set[str] = set()
        for index, request in enumerate(requests):
            label = f"providers[hume].requests[{index}]"
            if not isinstance(request, dict):
                errors.append(f"{label} must be an object")
                continue
            _reject_unknown_keys(
                request,
                {"request_id", "passage_id", "candidate_outputs"},
                label,
                errors,
            )
            request_id = request.get("request_id")
            if not isinstance(request_id, str) or not request_id or request_id in seen_request_ids:
                errors.append(f"{label}.request_id must be non-empty and unique")
            else:
                seen_request_ids.add(request_id)
            passage_id = request.get("passage_id")
            if passage_id not in passage_ids or passage_id in seen_passages:
                errors.append(f"{label}.passage_id must bind one unique envelope passage")
                continue
            seen_passages.add(passage_id)
            outputs = request.get("candidate_outputs")
            if not isinstance(outputs, list) or len(outputs) != 2:
                errors.append(f"{label}.candidate_outputs must contain exactly two outputs")
                outputs = []
            generation_indexes: set[int] = set()
            candidate_ids: list[Any] = []
            destinations: list[str] = []
            for output_index, output in enumerate(outputs):
                output_label = f"{label}.candidate_outputs[{output_index}]"
                if not isinstance(output, dict):
                    errors.append(f"{output_label} must be an object")
                    continue
                _reject_unknown_keys(
                    output,
                    {"candidate_id", "generation_index", "destination"},
                    output_label,
                    errors,
                )
                generation_index = output.get("generation_index")
                if generation_index not in {0, 1} or isinstance(generation_index, bool):
                    errors.append(f"{output_label}.generation_index must be 0 or 1")
                else:
                    generation_indexes.add(generation_index)
                candidate_ids.append(output.get("candidate_id"))
                destination = _validate_destination(output.get("destination"), f"{output_label}.destination", ".wav", errors)
                if destination:
                    destinations.append(destination)
            if generation_indexes != {0, 1}:
                errors.append(f"{label} must define generation indexes 0 and 1 exactly once")
            passage = _find_passage(envelope, passage_id)
            try:
                body = _compile_hume_body(
                    passage,
                    _adapter_passage(hume_adapter, passage_id),
                    tokens,
                    str(hume.get("voice_id")),
                )
            except ValidationError as exc:
                errors.extend(exc.errors)
                continue
            body_hash = _json_sha256(body)
            billable_once = sum(len(utterance["text"]) for utterance in body["utterances"])
            billed_chars = billable_once * body["num_generations"]
            rate = hume_pricing.get("public_creator_overage_rate_per_1000_text_characters")
            if not _is_number(rate) or rate < 0:
                errors.append("Hume pricing rate must be a non-negative finite estimate")
                rate = 0
            blockers = ["separate_active_calibration_authorization_absent"]
            voice_id = hume.get("voice_id")
            if voice_id == HUME_CLONE_PLACEHOLDER or not isinstance(voice_id, str) or not voice_id:
                blockers.insert(0, "hume_clone_id_and_provenance_receipt_absent")
            if hume.get("account_tier") in {None, "unverified"}:
                blockers.insert(-1, "hume_account_tier_unverified")
            if hume.get("commercial_use_eligibility") not in {True, "verified"}:
                blockers.insert(-1, "hume_commercial_use_eligibility_unverified")
            compiled_request = {
                    "request_id": request_id,
                    "provider": "hume",
                    "provider_id": hume.get("provider_id"),
                    "passage_id": passage_id,
                    "candidate_ids": candidate_ids,
                    "method": "POST",
                    "url_path": "/v0/tts",
                    "query": {},
                    "required_header_names": ["Content-Type", "X-Hume-Api-Key"],
                    "start_token": passage["start_token"],
                    "end_token": passage["end_token"],
                    "spoken_text_sha256": passage["spoken_text_sha256"],
                    "dialogue_text_sha256": sha256_bytes(
                        "\n".join(utterance["text"] for utterance in body["utterances"]).encode("utf-8")
                    ),
                    "acting_description_sha256": sha256_bytes(
                        "\n".join(utterance["description"] for utterance in body["utterances"]).encode("utf-8")
                    ),
                    "request_body": body,
                    "request_body_serialization": "utf8-json-sort-keys-compact-ensure-ascii-false-no-terminal-lf",
                    "request_body_sha256": body_hash,
                    "planned_call_count": 1,
                    "planned_output_count": 2,
                    "estimated_billable_character_count": billed_chars,
                    "estimated_public_rate_usd_per_1000_characters": rate,
                    "estimated_public_rate_cost_usd": round(billed_chars / 1000 * rate, 6),
                    "destinations": destinations,
                    "execution_ready": False,
                    "blockers": blockers,
                }
            if hume_fallback_enabled and destinations:
                fallback_body = dict(body)
                fallback_body["format"] = {"type": "mp3"}
                fallback_destinations = [
                    str(Path(destination).with_suffix(".mp3")) for destination in destinations
                ]
                compiled_request["fallback_request"] = {
                    "enabled": True,
                    "method": "POST",
                    "url_path": "/v0/tts",
                    "query": {},
                    "request_body": fallback_body,
                    "request_body_sha256": _json_sha256(fallback_body),
                    "destinations": fallback_destinations,
                    "planned_additional_call_count": 1,
                    "estimated_additional_billable_character_count": billed_chars,
                    "estimated_additional_public_rate_cost_usd": round(
                        billed_chars / 1000 * rate, 6
                    ),
                    "requires": [
                        "documented_lossless_capability_rejection_receipt",
                        "new_hash_bound_fallback_request",
                        "verified_actual_mp3_codec",
                        "verified_actual_bitrate_at_least_192000_bps",
                        "active_authorization_caps_include_fallback",
                    ],
                    "execution_ready": False,
                }
            else:
                compiled_request["fallback_request"] = {"enabled": False}
            compiled_requests.append(compiled_request)
        if seen_passages != set(passage_ids):
            errors.append("Hume requests must cover every envelope passage exactly once")

    if errors:
        raise ValidationError(errors)
    return plan, envelope, tokens, compiled_requests


def validate_provider_bakeoff_plan(
    plan_path: Path,
    envelope_path: Path,
    canonical_w_path: Path,
) -> dict[str, Any]:
    plan, _envelope, tokens, requests = _validate_plan_and_compile(
        plan_path, envelope_path, canonical_w_path
    )
    return {
        "valid": True,
        "schema_version": PROVIDER_BAKEOFF_PLAN_SCHEMA,
        "plan_sha256": sha256_file(plan_path),
        "performance_envelope_sha256": sha256_file(envelope_path),
        "canonical_w_sha256": token_identity(tokens)["sha256"],
        "provider_count": 2,
        "request_count": len(requests),
        "candidate_count": sum(request["planned_output_count"] for request in requests),
        "external_action_authorized": False,
    }


def dry_run_provider_bakeoff(
    plan_path: Path,
    envelope_path: Path,
    canonical_w_path: Path,
) -> dict[str, Any]:
    plan, _envelope, tokens, requests = _validate_plan_and_compile(
        plan_path, envelope_path, canonical_w_path
    )
    adapter_bindings = plan["provider_adapters"]
    adapter_hashes = {
        provider: adapter_bindings[provider]["sha256"]
        for provider in ("elevenlabs", "hume")
    }
    by_provider: dict[str, dict[str, Any]] = {}
    for provider_name in ("elevenlabs", "hume"):
        provider_requests = [request for request in requests if request["provider"] == provider_name]
        primary_calls = sum(request["planned_call_count"] for request in provider_requests)
        primary_characters = sum(
            request["estimated_billable_character_count"] for request in provider_requests
        )
        primary_cost = round(
            sum(request["estimated_public_rate_cost_usd"] for request in provider_requests), 6
        )
        fallback_calls = sum(
            request["fallback_request"].get("planned_additional_call_count", 0)
            for request in provider_requests
        )
        fallback_characters = sum(
            request["fallback_request"].get("estimated_additional_billable_character_count", 0)
            for request in provider_requests
        )
        fallback_cost = round(
            sum(
                request["fallback_request"].get(
                    "estimated_additional_public_rate_cost_usd", 0
                )
                for request in provider_requests
            ),
            6,
        )
        by_provider[provider_name] = {
            "primary_lossless": {
                "planned_call_count": primary_calls,
                "expected_output_count": sum(
                    request["planned_output_count"] for request in provider_requests
                ),
                "estimated_billable_character_count": primary_characters,
                "estimated_public_rate_cost_usd": primary_cost,
            },
            "maximum_with_one_fallback_per_request": {
                "max_call_count": primary_calls + fallback_calls,
                "expected_output_count": sum(
                    request["planned_output_count"] for request in provider_requests
                ),
                "max_billable_character_count": primary_characters + fallback_characters,
                "max_modeled_public_rate_cost_usd": round(primary_cost + fallback_cost, 6),
            },
            "execution_ready": False,
        }
    primary_totals = {
        "planned_call_count": sum(
            value["primary_lossless"]["planned_call_count"] for value in by_provider.values()
        ),
        "expected_output_count": sum(
            value["primary_lossless"]["expected_output_count"] for value in by_provider.values()
        ),
        "estimated_billable_character_count": sum(
            value["primary_lossless"]["estimated_billable_character_count"]
            for value in by_provider.values()
        ),
        "estimated_public_rate_cost_usd": round(
            sum(
                value["primary_lossless"]["estimated_public_rate_cost_usd"]
                for value in by_provider.values()
            ),
            6,
        ),
    }
    maximum_totals = {
        "max_call_count": sum(
            value["maximum_with_one_fallback_per_request"]["max_call_count"]
            for value in by_provider.values()
        ),
        "expected_output_count": primary_totals["expected_output_count"],
        "max_billable_character_count": sum(
            value["maximum_with_one_fallback_per_request"]["max_billable_character_count"]
            for value in by_provider.values()
        ),
        "max_modeled_public_rate_cost_usd": round(
            sum(
                value["maximum_with_one_fallback_per_request"][
                    "max_modeled_public_rate_cost_usd"
                ]
                for value in by_provider.values()
            ),
            6,
        ),
    }
    return {
        "schema_version": PROVIDER_BAKEOFF_DRY_RUN_SCHEMA,
        "compilation_id": f"{plan['plan_id']}-compiled",
        "mode": "dry_run",
        "status": "non_executable",
        "network_called": False,
        "credentials_accessed": False,
        "provider_calls_made": 0,
        "audio_files_created": 0,
        "bindings": {
            "performance_envelope": {"sha256": sha256_file(envelope_path)},
            "provider_bakeoff_plan": {"sha256": sha256_file(plan_path)},
            "provider_adapters": {
                provider: {"sha256": adapter_hashes[provider]}
                for provider in ("elevenlabs", "hume")
            },
            "canonical_w": {
                "token_count": len(tokens),
                "sha256": token_identity(tokens)["sha256"],
            },
        },
        "compiler_contract": {
            "request_body_hash_serialization": "utf8-json-sort-keys-compact-ensure-ascii-false-no-terminal-lf",
            "token_ranges": "absolute_half_open_canonical_w",
            "eleven_candidate_rule": "same_words_same_tags_paired_fixed_seeds_separate_generation",
            "hume_candidate_rule": "same_request_num_generations_2",
            "hume_endpoint": "/v0/tts",
            "hume_clone_method": "manual_platform_ui_only_no_upload_api_asserted",
            "hume_placeholder": HUME_CLONE_PLACEHOLDER,
            "hume_recompile_rule": "Bind a real clone/provenance receipt, then regenerate and rehash before authorization.",
        },
        "requests": requests,
        "totals": {
            "by_provider": by_provider,
            "primary_lossless": primary_totals,
            "maximum_with_one_fallback_per_request": maximum_totals,
        },
        "request_set_sha256": _json_sha256(
            [
                {
                    "request_id": request["request_id"],
                    "request_body_sha256": request["request_body_sha256"],
                    "fallback_request_body_sha256": request["fallback_request"].get(
                        "request_body_sha256"
                    ),
                    "destinations": request["destinations"],
                }
                for request in requests
            ]
        ),
        "notices": [
            "No provider request was made.",
            "No credential was read.",
            "No voice sample was retrieved or uploaded.",
            "No clone or audio was created.",
            "Each external action requires its own active, unconsumed, hash-bound authorization.",
        ],
    }


def _parse_time(value: Any, label: str, errors: list[str]) -> datetime | None:
    if not isinstance(value, str) or not value:
        errors.append(f"{label} is required")
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        errors.append(f"{label} must be an ISO-8601 timestamp")
        return None
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        errors.append(f"{label} must include a timezone")
        return None
    return parsed.astimezone(timezone.utc)


def _positive_limit(limits: dict[str, Any], field: str, errors: list[str], *, allow_zero: bool = False) -> float | None:
    value = limits.get(field)
    minimum = 0 if allow_zero else 0
    if not _is_number(value) or value < minimum or (not allow_zero and value == 0):
        adjective = "non-negative" if allow_zero else "positive"
        errors.append(f"authorized_limits.{field} must be {adjective}")
        return None
    return float(value)


def _artifact_root(authorization_path: Path) -> Path:
    return authorization_path.parent.parent.resolve()


def _validate_bound_artifacts(
    authorization_path: Path,
    authorization: dict[str, Any],
    errors: list[str],
) -> tuple[dict[str, Any] | None, dict[str, Any] | None, dict[str, Any] | None]:
    root = _artifact_root(authorization_path)
    paths = {
        "performance_envelope_sha256": root / "performance-envelope.json",
        "provider_bakeoff_plan_sha256": root / "provider-bakeoff-plan.json",
        "compiled_dry_run_sha256": root / "compiled" / "provider-bakeoff-dry-run.json",
    }
    bindings = authorization.get("bindings")
    if not isinstance(bindings, dict):
        errors.append("bindings must bind the performance envelope, plan, and compiled dry run")
        return None, None, None
    loaded: list[dict[str, Any] | None] = []
    for field, path in paths.items():
        expected = bindings.get(field)
        valid_hash = _hash_value(expected, f"bindings.{field}", errors)
        if not path.is_file():
            errors.append(f"bound artifact is missing: {path}")
            loaded.append(None)
            continue
        if valid_hash and sha256_file(path) != expected:
            errors.append(f"bindings.{field} does not match {path.name}")
        try:
            loaded.append(read_json(path))
        except ValidationError as exc:
            errors.extend(exc.errors)
            loaded.append(None)
    envelope, plan, dry_run = loaded
    if isinstance(dry_run, dict):
        if dry_run.get("schema_version") != PROVIDER_BAKEOFF_DRY_RUN_SCHEMA:
            errors.append("bound compiled dry run has the wrong schema")
        for field, expected in (
            ("network_called", False),
            ("credentials_accessed", False),
            ("provider_calls_made", 0),
            ("audio_files_created", 0),
        ):
            if dry_run.get(field) != expected:
                errors.append(f"bound compiled dry run must keep {field}={expected!r}")
    if isinstance(envelope, dict) and isinstance(plan, dict) and isinstance(dry_run, dict):
        canonical_binding = envelope.get("canonical_w")
        canonical_path = _resolve_declared_path(
            paths["performance_envelope_sha256"],
            canonical_binding.get("path") if isinstance(canonical_binding, dict) else None,
            "bound performance_envelope.canonical_w.path",
            errors,
        )
        if canonical_path is not None and canonical_path.is_file():
            try:
                validate_performance_envelope(
                    paths["performance_envelope_sha256"], canonical_path
                )
                validate_provider_bakeoff_plan(
                    paths["provider_bakeoff_plan_sha256"],
                    paths["performance_envelope_sha256"],
                    canonical_path,
                )
                expected_dry_run = dry_run_provider_bakeoff(
                    paths["provider_bakeoff_plan_sha256"],
                    paths["performance_envelope_sha256"],
                    canonical_path,
                )
            except ValidationError as exc:
                errors.extend(
                    f"bound bakeoff artifact validation: {error}" for error in exc.errors
                )
            else:
                if dry_run != expected_dry_run:
                    errors.append(
                        "bound compiled dry run does not equal deterministic compilation of the bound plan"
                    )
        elif canonical_path is not None:
            errors.append(f"bound canonical W is missing: {canonical_path}")
    return envelope, plan, dry_run


def _provider_from_plan(plan: dict[str, Any] | None, name: str) -> dict[str, Any] | None:
    if not isinstance(plan, dict) or not isinstance(plan.get("providers"), list):
        return None
    return next((provider for provider in plan["providers"] if provider.get("provider") == name), None)


def _requests_from_dry_run(dry_run: dict[str, Any] | None, provider: str) -> list[dict[str, Any]]:
    if not isinstance(dry_run, dict) or not isinstance(dry_run.get("requests"), list):
        return []
    return [request for request in dry_run["requests"] if request.get("provider") == provider]


def _active_rights_record(
    action: dict[str, Any],
    artifact_root: Path,
    errors: list[str],
) -> dict[str, Any] | None:
    rights = action.get("rights_and_consent")
    if not isinstance(rights, dict):
        errors.append("action.rights_and_consent must bind the voice owner, permitted disclosure, path, and hash")
        return None
    _reject_unknown_keys(
        rights,
        {"voice_owner", "provider_disclosure_approved", "record_path", "record_sha256"},
        "action.rights_and_consent",
        errors,
    )
    if not isinstance(rights.get("voice_owner"), str) or not rights.get("voice_owner"):
        errors.append("action.rights_and_consent.voice_owner is required")
    if rights.get("provider_disclosure_approved") is not True:
        errors.append("voice-sample provider disclosure is not approved")
    _verify_existing_local_binding(
        artifact_root,
        rights.get("record_path"),
        rights.get("record_sha256"),
        "action.rights_and_consent",
        errors,
        required_prefix="receipts",
    )
    return rights


def validate_provider_action_authorization(
    authorization_path: Path,
    *,
    now: datetime | None = None,
) -> dict[str, Any]:
    authorization = read_json(authorization_path)
    errors = _scan_for_secrets(authorization)
    if authorization.get("schema_version") != PROVIDER_ACTION_AUTHORIZATION_SCHEMA:
        errors.append(f"schema_version must be {PROVIDER_ACTION_AUTHORIZATION_SCHEMA}")
    if not isinstance(authorization.get("authorization_id"), str) or not authorization.get("authorization_id"):
        errors.append("authorization_id is required")
    scope = authorization.get("scope")
    if scope not in ACTION_SCOPES:
        errors.append("scope must be one of the exact provider action enums")
    _validate_target(authorization.get("target"), "target", errors)
    expected_provider = "elevenlabs" if str(scope).startswith("elevenlabs_") else "hume"
    if authorization.get("provider") != expected_provider:
        errors.append("provider does not match the exact action scope")
    status = authorization.get("status")
    if status not in {"draft", "active"}:
        errors.append("status must be draft or active")
    _reject_unknown_keys(authorization.get("target"), {"kind", "id"}, "target", errors)
    action = authorization.get("action")
    if not isinstance(action, dict):
        errors.append("action must be an object")
        action = {}
    limits = authorization.get("authorized_limits")
    if not isinstance(limits, dict):
        errors.append("authorized_limits must be an object")
        limits = {}
    consumption = authorization.get("consumption")
    if not isinstance(consumption, dict):
        errors.append("consumption must be an object")
        consumption = {}

    _reject_unknown_keys(
        authorization,
        {
            "schema_version",
            "authorization_id",
            "status",
            "approved",
            "scope",
            "target",
            "provider",
            "action",
            "purpose",
            "bindings",
            "account_requirements",
            "requested_limits",
            "authorized_limits",
            "consumption",
            "approved_by",
            "approved_at",
            "expires_at",
            "execution_ready",
            "blockers",
        },
        "authorization",
        errors,
    )
    action_keys = {
        "elevenlabs_sample_retrieval": {
            "kind",
            "voice_id",
            "metadata_endpoint",
            "sample_ids",
            "destinations",
            "sample_selection_rule",
            "selection_fails_if_zero_or_multiple_samples",
            "selection_fails_if_mixed_speaker",
            "metadata_must_confirm_original_human_source",
            "metadata_receipt_destination",
            "selected_sample_receipt_destination",
            "rights_and_consent",
        },
        ELEVEN_METADATA_INVENTORY_SCOPE: {
            "kind",
            "voice_id",
            "metadata_endpoint",
            "metadata_receipt_destination",
            "selection_permitted",
            "download_permitted",
            "raw_payload_storage_permitted",
        },
        ELEVEN_NAMED_SAMPLE_BATCH_SCOPE: {
            "kind",
            "voice_id",
            "source_inventory_receipt_path",
            "source_inventory_receipt_sha256",
            "samples",
            "batch_receipt_destination",
            "metadata_call_permitted",
            "discovery_permitted",
            "selection_permitted",
            "retries_permitted",
            "redirects_permitted",
            "stop_on_first_failure",
            "preserve_exact_returned_bytes",
            "provenance_review_required",
            "downstream_use_permitted",
            "tts_generation_permitted",
            "voice_mutation_permitted",
            "hume_disclosure_permitted",
            "hume_clone_creation_permitted",
            "rights_and_consent",
        },
        "hume_clone_creation": {
            "kind",
            "interface",
            "api_upload_endpoint",
            "source_sample_path",
            "source_sample_sha256",
            "source_sample_rights_record",
            "source_sample_mime_type",
            "source_sample_duration_seconds",
            "rights_and_consent",
            "clone_display_name",
            "expected_clone_id",
            "clone_receipt_destination",
        },
        "elevenlabs_calibration": {
            "kind",
            "voice_id",
            "model_id",
            "request_ids",
            "preferred_output_format",
            "only_permitted_fallback",
            "fallback_reason_required",
            "fallback_request_call_ceiling",
            "fallback_requires_capability_rejection_receipt",
            "fallback_requires_actual_codec_bitrate_verification",
        },
        "hume_calibration": {
            "kind",
            "voice_id",
            "model_id",
            "request_ids",
            "num_generations_per_request",
            "requested_format",
            "only_permitted_fallback",
            "fallback_reason_required",
            "fallback_request_call_ceiling",
            "fallback_requires_capability_rejection_receipt",
            "fallback_requires_actual_codec_bitrate_verification",
        },
    }
    _reject_unknown_keys(action, action_keys.get(scope, set()), "action", errors)
    draft_or_active_rights = action.get("rights_and_consent")
    if draft_or_active_rights is not None:
        if not isinstance(draft_or_active_rights, dict):
            errors.append("action.rights_and_consent must be an object")
        else:
            _reject_unknown_keys(
                draft_or_active_rights,
                {"voice_owner", "provider_disclosure_approved", "record_path", "record_sha256"},
                "action.rights_and_consent",
                errors,
            )
    base_bindings = {
        "performance_envelope_sha256",
        "provider_adapter_sha256",
        "provider_bakeoff_plan_sha256",
        "compiled_dry_run_sha256",
    }
    binding_keys = {
        "elevenlabs_sample_retrieval": base_bindings,
        ELEVEN_METADATA_INVENTORY_SCOPE: base_bindings,
        ELEVEN_NAMED_SAMPLE_BATCH_SCOPE: base_bindings,
        "hume_clone_creation": base_bindings,
        "elevenlabs_calibration": base_bindings
        | {
            "script_sha256",
            "spoken_text_sha256",
            "voice_provenance_kind",
            "calibration_rights_receipt_path",
            "calibration_rights_receipt_sha256",
            "owner_selection_record_path",
            "owner_selection_record_sha256",
            "saved_voice_receipt_path",
            "saved_voice_receipt_sha256",
        },
        "hume_calibration": base_bindings
        | {
            "script_sha256",
            "spoken_text_sha256",
            "compiled_hash_state",
            "clone_receipt_sha256",
            "clone_receipt_path",
        },
    }
    _reject_unknown_keys(
        authorization.get("bindings"),
        binding_keys.get(scope, set()),
        "bindings",
        errors,
    )
    requested_limit_keys = {
        "elevenlabs_sample_retrieval": {
            "max_metadata_calls",
            "max_sample_download_calls",
            "max_download_bytes",
            "max_spend_usd",
        },
        ELEVEN_METADATA_INVENTORY_SCOPE: {
            "max_metadata_calls",
            "max_sample_download_calls",
            "max_metadata_response_bytes",
            "max_spend_usd",
        },
        ELEVEN_NAMED_SAMPLE_BATCH_SCOPE: {
            "max_metadata_calls",
            "max_sample_download_calls",
            "max_download_bytes",
            "max_spend_usd",
        },
        "hume_clone_creation": {"max_ui_uploads", "max_voice_clones", "max_spend_usd"},
        "elevenlabs_calibration": {
            "max_calls",
            "max_characters",
            "max_outputs",
            "max_spend_usd",
            "primary_lossless_calls",
            "primary_lossless_characters",
            "primary_lossless_outputs",
            "primary_modeled_public_rate_cost_usd",
        },
        "hume_calibration": {
            "max_calls",
            "max_characters",
            "max_outputs",
            "max_spend_usd",
            "primary_lossless_calls",
            "primary_lossless_characters",
            "primary_lossless_outputs",
            "primary_modeled_public_rate_cost_usd",
        },
    }
    _reject_unknown_keys(
        authorization.get("requested_limits"),
        requested_limit_keys.get(scope, set()),
        "requested_limits",
        errors,
    )
    authorized_limit_keys = {
        "elevenlabs_sample_retrieval": {
            "max_calls",
            "max_downloads",
            "max_download_bytes",
            "max_spend_usd",
        },
        ELEVEN_METADATA_INVENTORY_SCOPE: {
            "max_calls",
            "max_downloads",
            "max_metadata_response_bytes",
            "max_spend_usd",
        },
        ELEVEN_NAMED_SAMPLE_BATCH_SCOPE: {
            "max_calls",
            "max_downloads",
            "max_download_bytes",
            "max_spend_usd",
        },
        "hume_clone_creation": {"max_ui_uploads", "max_voice_clones", "max_spend_usd"},
        "elevenlabs_calibration": {
            "max_calls",
            "max_characters",
            "max_outputs",
            "max_spend_usd",
        },
        "hume_calibration": {
            "max_calls",
            "max_characters",
            "max_outputs",
            "max_spend_usd",
        },
    }
    _reject_unknown_keys(
        limits,
        authorized_limit_keys.get(scope, set()),
        "authorized_limits",
        errors,
    )
    consumption_keys = {
        "elevenlabs_sample_retrieval": {
            "status",
            "calls_used",
            "downloads_used",
            "spend_used_usd",
            "record_path",
        },
        ELEVEN_METADATA_INVENTORY_SCOPE: {
            "status",
            "calls_used",
            "downloads_used",
            "spend_used_usd",
            "record_path",
        },
        ELEVEN_NAMED_SAMPLE_BATCH_SCOPE: {
            "status",
            "calls_used",
            "downloads_used",
            "spend_used_usd",
            "record_path",
        },
        "hume_clone_creation": {
            "status",
            "uploads_used",
            "clones_created",
            "spend_used_usd",
            "record_path",
        },
        "elevenlabs_calibration": {
            "status",
            "calls_used",
            "characters_used",
            "outputs_received",
            "spend_used_usd",
            "record_path",
        },
        "hume_calibration": {
            "status",
            "calls_used",
            "characters_used",
            "outputs_received",
            "spend_used_usd",
            "record_path",
        },
    }
    _reject_unknown_keys(
        consumption,
        consumption_keys.get(scope, set()),
        "consumption",
        errors,
    )
    _reject_unknown_keys(
        authorization.get("account_requirements"),
        {
            "account_tier",
            "commercial_use_eligibility",
            "logged_in_session_is_authorization",
            "commercial_terms_receipt_path",
            "commercial_terms_receipt_sha256",
        },
        "account_requirements",
        errors,
    )
    if expected_provider == "elevenlabs" and "account_requirements" in authorization:
        errors.append("ElevenLabs authorization may not carry Hume account requirements")

    envelope, plan, dry_run = _validate_bound_artifacts(authorization_path, authorization, errors)
    if isinstance(plan, dict) and authorization.get("target") != plan.get("target"):
        errors.append("authorization target does not match the provider bakeoff plan")
    if isinstance(plan, dict):
        adapter_binding = plan.get("provider_adapters", {}).get(expected_provider)
        expected_adapter_hash = (
            adapter_binding.get("sha256") if isinstance(adapter_binding, dict) else None
        )
        bound_adapter_hash = authorization.get("bindings", {}).get("provider_adapter_sha256")
        if bound_adapter_hash != expected_adapter_hash:
            errors.append(
                f"bindings.provider_adapter_sha256 does not bind the {expected_provider} adapter"
            )

    artifact_root = _artifact_root(authorization_path)
    if status == "draft" and scope == "elevenlabs_calibration":
        draft_provider_plan = _provider_from_plan(plan, "elevenlabs")
        draft_plan_voice_id = (
            draft_provider_plan.get("voice_id") if isinstance(draft_provider_plan, dict) else None
        )
        _validate_eleven_calibration_voice_provenance(
            authorization,
            action,
            draft_plan_voice_id,
            artifact_root,
            errors,
            required=False,
        )

    if status == "draft":
        if authorization.get("approved") is not False:
            errors.append("draft authorization approved must be false")
        if authorization.get("execution_ready") is not False:
            errors.append("draft authorization execution_ready must be false")
        if consumption.get("status") != "not_authorized":
            errors.append("draft authorization consumption.status must be not_authorized")
        if not isinstance(authorization.get("blockers"), list) or not authorization.get("blockers"):
            errors.append("draft authorization must list at least one blocker")
        if errors:
            raise ValidationError(errors)
        return {
            "valid": True,
            "schema_version": PROVIDER_ACTION_AUTHORIZATION_SCHEMA,
            "authorization_sha256": sha256_file(authorization_path),
            "scope": scope,
            "status": "draft",
            "execution_ready": False,
            "network_authorized": False,
            "blocker_count": len(authorization["blockers"]),
        }

    if authorization.get("approved") is not True:
        errors.append("active authorization approved must be true")
    if authorization.get("execution_ready") is not True:
        errors.append("active authorization execution_ready must be true")
    if authorization.get("blockers") not in ([], None):
        errors.append("active authorization must not have unresolved blockers")
    if not isinstance(authorization.get("approved_by"), str) or not authorization.get("approved_by"):
        errors.append("active authorization approved_by is required")
    approved_at = _parse_time(authorization.get("approved_at"), "approved_at", errors)
    expires_at = _parse_time(authorization.get("expires_at"), "expires_at", errors)
    current = (now or datetime.now(timezone.utc)).astimezone(timezone.utc)
    if approved_at is not None and expires_at is not None:
        if approved_at > current:
            errors.append("approved_at may not be in the future")
        if expires_at <= current:
            errors.append("active authorization is expired")
        if expires_at - approved_at > timedelta(hours=24):
            errors.append("active authorization window may not exceed 24 hours")
        if expires_at <= approved_at:
            errors.append("expires_at must be later than approved_at")
    if consumption.get("status") != "unconsumed":
        errors.append("active authorization must be unconsumed")
    record_path = _safe_relative(consumption.get("record_path"), "consumption.record_path", errors)
    if record_path is not None:
        resolved_record = (authorization_path.parent / record_path).resolve()
        if not resolved_record.is_relative_to(authorization_path.parent.resolve()):
            errors.append("consumption.record_path escapes the authorization directory")
        elif resolved_record.exists():
            errors.append("authorization consumption record already exists")
    for key, value in consumption.items():
        if key.endswith("_used") or key.endswith("_used_usd"):
            if value != 0:
                errors.append(f"consumption.{key} must be zero before the action begins")

    if scope in {"elevenlabs_calibration", "hume_calibration"} and isinstance(envelope, dict):
        bindings = authorization.get("bindings", {})
        if bindings.get("script_sha256") != envelope.get("script", {}).get("sha256"):
            errors.append("calibration bindings.script_sha256 does not match the locked envelope script")
        if bindings.get("spoken_text_sha256") != envelope.get("canonical_w", {}).get("sha256"):
            errors.append("calibration bindings.spoken_text_sha256 does not match canonical W")

    if scope == ELEVEN_METADATA_INVENTORY_SCOPE:
        if action.get("kind") != ELEVEN_METADATA_INVENTORY_KIND:
            errors.append("metadata inventory action.kind mismatch")
        provider_plan = _provider_from_plan(plan, "elevenlabs")
        if not provider_plan or action.get("voice_id") != provider_plan.get("voice_id"):
            errors.append("metadata inventory voice_id does not match the bakeoff plan")
        endpoint = action.get("metadata_endpoint")
        expected_endpoint = (
            f"https://api.elevenlabs.io/v1/voices/"
            f"{quote(str(action.get('voice_id')), safe='')}"
        )
        if endpoint != expected_endpoint:
            errors.append(
                "metadata inventory endpoint must exactly equal the official endpoint for the bound voice_id"
            )
        for field in (
            "selection_permitted",
            "download_permitted",
            "raw_payload_storage_permitted",
        ):
            if action.get(field) is not False:
                errors.append(f"metadata inventory action.{field} must be false")
        _validate_new_local_destination(
            artifact_root,
            action.get("metadata_receipt_destination"),
            "action.metadata_receipt_destination",
            errors,
            required_prefix="receipts",
        )
        requested = authorization.get("requested_limits")
        if not isinstance(requested, dict):
            errors.append("metadata inventory requested_limits must be an object")
            requested = {}
        if not _is_int(requested.get("max_metadata_calls")) or requested.get("max_metadata_calls") != 1:
            errors.append("metadata inventory requested_limits.max_metadata_calls must be exactly 1")
        if not _is_int(requested.get("max_sample_download_calls")) or requested.get("max_sample_download_calls") != 0:
            errors.append(
                "metadata inventory requested_limits.max_sample_download_calls must be exactly 0"
            )
        if not _is_number(requested.get("max_spend_usd")) or requested.get("max_spend_usd") != 0:
            errors.append("metadata inventory requested_limits.max_spend_usd must be exactly 0")
        requested_bytes = requested.get("max_metadata_response_bytes")
        if (
            not _is_int(requested_bytes)
            or requested_bytes <= 0
            or requested_bytes > MAX_METADATA_INVENTORY_RESPONSE_BYTES
        ):
            errors.append(
                "metadata inventory requested_limits.max_metadata_response_bytes must be an integer between 1 and 2000000"
            )
        if not _is_int(limits.get("max_calls")) or limits.get("max_calls") != 1:
            errors.append("metadata inventory authorized_limits.max_calls must be exactly 1")
        if not _is_int(limits.get("max_downloads")) or limits.get("max_downloads") != 0:
            errors.append("metadata inventory authorized_limits.max_downloads must be exactly 0")
        if not _is_number(limits.get("max_spend_usd")) or limits.get("max_spend_usd") != 0:
            errors.append("metadata inventory authorized_limits.max_spend_usd must be exactly 0")
        authorized_bytes = limits.get("max_metadata_response_bytes")
        if (
            not _is_int(authorized_bytes)
            or authorized_bytes <= 0
            or authorized_bytes > MAX_METADATA_INVENTORY_RESPONSE_BYTES
        ):
            errors.append(
                "metadata inventory authorized_limits.max_metadata_response_bytes must be an integer between 1 and 2000000"
            )
        if (
            _is_int(requested_bytes)
            and _is_int(authorized_bytes)
            and requested_bytes != authorized_bytes
        ):
            errors.append(
                "metadata inventory requested and authorized metadata byte ceilings must match"
            )
        if not _is_int(consumption.get("calls_used")) or consumption.get("calls_used") != 0:
            errors.append("metadata inventory consumption.calls_used must be exactly 0 before execution")
        if not _is_int(consumption.get("downloads_used")) or consumption.get("downloads_used") != 0:
            errors.append(
                "metadata inventory consumption.downloads_used must be exactly 0 before execution"
            )
        if not _is_number(consumption.get("spend_used_usd")) or consumption.get("spend_used_usd") != 0:
            errors.append(
                "metadata inventory consumption.spend_used_usd must be exactly 0 before execution"
            )

    elif scope == ELEVEN_NAMED_SAMPLE_BATCH_SCOPE:
        if action.get("kind") != ELEVEN_NAMED_SAMPLE_BATCH_KIND:
            errors.append("named-sample local-review action.kind mismatch")
        provider_plan = _provider_from_plan(plan, "elevenlabs")
        voice_id = action.get("voice_id")
        if not provider_plan or voice_id != provider_plan.get("voice_id"):
            errors.append("named-sample local-review voice_id does not match the bakeoff plan")
        for field in (
            "metadata_call_permitted",
            "discovery_permitted",
            "selection_permitted",
            "retries_permitted",
            "redirects_permitted",
            "downstream_use_permitted",
            "tts_generation_permitted",
            "voice_mutation_permitted",
            "hume_disclosure_permitted",
            "hume_clone_creation_permitted",
        ):
            if action.get(field) is not False:
                errors.append(f"named-sample local-review action.{field} must be false")
        for field in ("stop_on_first_failure", "preserve_exact_returned_bytes"):
            if action.get(field) is not True:
                errors.append(f"named-sample local-review action.{field} must be true")
        if action.get("provenance_review_required") is not True:
            errors.append("named-sample local review must require unresolved human provenance review")

        inventory_path = _verify_existing_local_binding(
            artifact_root,
            action.get("source_inventory_receipt_path"),
            action.get("source_inventory_receipt_sha256"),
            "action.source_inventory_receipt",
            errors,
            required_prefix="receipts",
        )
        inventory: dict[str, Any] | None = None
        if inventory_path is not None:
            try:
                loaded_inventory = read_json(inventory_path)
            except ValidationError as exc:
                errors.extend(
                    f"bound source inventory: {error}" for error in exc.errors
                )
            else:
                if isinstance(loaded_inventory, dict):
                    inventory = loaded_inventory
                else:
                    errors.append("bound source inventory must be a JSON object")

        descriptors = action.get("samples")
        if not isinstance(descriptors, list) or len(descriptors) != MAX_NAMED_SAMPLE_REVIEW_COUNT:
            errors.append(
                f"named-sample local review must bind exactly {MAX_NAMED_SAMPLE_REVIEW_COUNT} ordered samples"
            )
            descriptors = []
        descriptor_keys = {
            "sample_id",
            "original_filename",
            "endpoint",
            "destination",
            "receipt_destination",
            "expected_mime_type",
            "expected_size_bytes",
            "expected_provider_hash",
        }
        sample_ids: list[str] = []
        endpoints: list[str] = []
        output_paths: list[str] = []
        expected_total_bytes = 0
        for index, descriptor in enumerate(descriptors):
            label = f"action.samples[{index}]"
            if not isinstance(descriptor, dict):
                errors.append(f"{label} must be an object")
                continue
            _reject_unknown_keys(descriptor, descriptor_keys, label, errors)
            sample_id = descriptor.get("sample_id")
            if (
                not isinstance(sample_id, str)
                or not sample_id
                or "pending" in sample_id.lower()
            ):
                errors.append(f"{label}.sample_id must be an exact non-pending provider sample ID")
                sample_id = ""
            sample_ids.append(sample_id)
            expected_endpoint = (
                f"https://api.elevenlabs.io/v1/voices/{quote(str(voice_id), safe='')}/"
                f"samples/{quote(sample_id, safe='')}/audio"
            )
            endpoint = descriptor.get("endpoint")
            if endpoint != expected_endpoint:
                errors.append(f"{label}.endpoint must exactly equal the official bound sample endpoint")
            if isinstance(endpoint, str):
                endpoints.append(endpoint)
            original_filename = descriptor.get("original_filename")
            if (
                not isinstance(original_filename, str)
                or not original_filename
                or Path(original_filename.replace("\\", "/")).name != original_filename
            ):
                errors.append(f"{label}.original_filename must be one safe provider basename")
            expected_mime = descriptor.get("expected_mime_type")
            if not isinstance(expected_mime, str) or not expected_mime.startswith("audio/"):
                errors.append(f"{label}.expected_mime_type must identify audio")
            expected_size = descriptor.get("expected_size_bytes")
            if not _is_int(expected_size) or expected_size <= 0:
                errors.append(f"{label}.expected_size_bytes must be a positive integer")
            else:
                expected_total_bytes += expected_size
            provider_hash = descriptor.get("expected_provider_hash")
            if (
                not isinstance(provider_hash, str)
                or OPAQUE_PROVIDER_HASH_RE.fullmatch(provider_hash) is None
            ):
                errors.append(
                    f"{label}.expected_provider_hash must preserve the 32-hex opaque provider value"
                )
            for field, prefix in (
                ("destination", "local-media"),
                ("receipt_destination", "receipts"),
            ):
                value = descriptor.get(field)
                _validate_new_local_destination(
                    artifact_root,
                    value,
                    f"{label}.{field}",
                    errors,
                    required_prefix=prefix,
                )
                if isinstance(value, str):
                    output_paths.append(value)

        batch_receipt = action.get("batch_receipt_destination")
        _validate_new_local_destination(
            artifact_root,
            batch_receipt,
            "action.batch_receipt_destination",
            errors,
            required_prefix="receipts",
        )
        if isinstance(batch_receipt, str):
            output_paths.append(batch_receipt)

        if len(sample_ids) != len(set(sample_ids)):
            errors.append("named-sample local-review sample IDs must be unique")
        if len(endpoints) != len(set(endpoints)):
            errors.append("named-sample local-review endpoints must be unique")
        if len(output_paths) != len(set(output_paths)):
            errors.append("named-sample local-review raw and receipt destinations must all be distinct")

        if inventory is not None:
            inventory_samples = inventory.get("samples")
            completeness = inventory.get("inventory_completeness")
            if inventory.get("schema_version") != "oe-elevenlabs-sample-metadata-inventory-v1":
                errors.append("bound source inventory has the wrong schema")
            if inventory.get("outcome") != "normalized_inventory_recorded":
                errors.append("bound source inventory is not a completed normalized inventory")
            if inventory.get("voice_id") != voice_id:
                errors.append("bound source inventory voice_id does not match the action")
            if inventory.get("sample_count") != len(descriptors):
                errors.append("bound source inventory sample_count does not match the complete batch")
            if inventory.get("selection_made") is not False:
                errors.append("bound source inventory must not contain a prior selection")
            if inventory.get("provider_metadata_is_provenance_proof") not in (False, None):
                errors.append("bound source inventory may not assert provider metadata as provenance proof")
            if not isinstance(completeness, dict) or completeness.get("inventory_complete") is not True:
                errors.append("bound source inventory is incomplete")
            if not isinstance(inventory_samples, list) or len(inventory_samples) != len(descriptors):
                errors.append("action samples must cover the complete bound source inventory")
            else:
                for index, (descriptor, source) in enumerate(zip(descriptors, inventory_samples)):
                    if not isinstance(descriptor, dict) or not isinstance(source, dict):
                        errors.append(f"source inventory sample {index} is malformed")
                        continue
                    comparisons = (
                        ("sample_id", "sample_id"),
                        ("original_filename", "original_filename"),
                        ("expected_mime_type", "declared_mime_type"),
                        ("expected_size_bytes", "provider_size_bytes"),
                        ("expected_provider_hash", "provider_hash"),
                    )
                    for descriptor_field, source_field in comparisons:
                        if descriptor.get(descriptor_field) != source.get(source_field):
                            errors.append(
                                f"action.samples[{index}].{descriptor_field} does not match the bound inventory"
                            )

        requested = authorization.get("requested_limits")
        if not isinstance(requested, dict):
            errors.append("named-sample local review requires requested_limits")
            requested = {}
        if not _is_int(requested.get("max_metadata_calls")) or requested.get("max_metadata_calls") != 0:
            errors.append("named-sample local review requested max_metadata_calls must be exactly 0")
        if (
            not _is_int(requested.get("max_sample_download_calls"))
            or requested.get("max_sample_download_calls") != len(descriptors)
        ):
            errors.append("named-sample local review requested download calls must equal the sample count")
        if (
            not _is_int(requested.get("max_download_bytes"))
            or requested.get("max_download_bytes") != MAX_NAMED_SAMPLE_REVIEW_BYTES
        ):
            errors.append(
                f"named-sample local review requested max_download_bytes must be exactly {MAX_NAMED_SAMPLE_REVIEW_BYTES}"
            )
        if not _is_number(requested.get("max_spend_usd")) or requested.get("max_spend_usd") != 0:
            errors.append("named-sample local review requested max_spend_usd must be exactly 0")
        if not _is_int(limits.get("max_calls")) or limits.get("max_calls") != len(descriptors):
            errors.append("named-sample local review authorized max_calls must equal the sample count")
        if not _is_int(limits.get("max_downloads")) or limits.get("max_downloads") != len(descriptors):
            errors.append("named-sample local review authorized max_downloads must equal the sample count")
        if (
            not _is_int(limits.get("max_download_bytes"))
            or limits.get("max_download_bytes") != MAX_NAMED_SAMPLE_REVIEW_BYTES
        ):
            errors.append(
                f"named-sample local review authorized max_download_bytes must be exactly {MAX_NAMED_SAMPLE_REVIEW_BYTES}"
            )
        if not _is_number(limits.get("max_spend_usd")) or limits.get("max_spend_usd") != 0:
            errors.append("named-sample local review authorized max_spend_usd must be exactly 0")
        if expected_total_bytes > MAX_NAMED_SAMPLE_REVIEW_BYTES:
            errors.append("bound provider sample sizes exceed the total authorized byte ceiling")
        if not _is_int(consumption.get("calls_used")) or consumption.get("calls_used") != 0:
            errors.append("named-sample local review consumption.calls_used must be exactly 0")
        if not _is_int(consumption.get("downloads_used")) or consumption.get("downloads_used") != 0:
            errors.append("named-sample local review consumption.downloads_used must be exactly 0")
        if not _is_number(consumption.get("spend_used_usd")) or consumption.get("spend_used_usd") != 0:
            errors.append("named-sample local review consumption.spend_used_usd must be exactly 0")
        _active_rights_record(action, artifact_root, errors)

    elif scope == "elevenlabs_sample_retrieval":
        if action.get("kind") != "read_only_voice_metadata_and_named_sample_retrieval":
            errors.append("sample retrieval action.kind mismatch")
        provider_plan = _provider_from_plan(plan, "elevenlabs")
        if not provider_plan or action.get("voice_id") != provider_plan.get("voice_id"):
            errors.append("sample retrieval voice_id does not match the bakeoff plan")
        endpoint = action.get("metadata_endpoint")
        expected_endpoint = (
            f"https://api.elevenlabs.io/v1/voices/"
            f"{quote(str(action.get('voice_id')), safe='')}"
        )
        if endpoint != expected_endpoint:
            errors.append(
                "sample retrieval metadata_endpoint must exactly equal the official endpoint for the bound voice_id"
            )
        sample_ids = action.get("sample_ids")
        destinations = action.get("destinations")
        dynamic_selector = action.get("sample_selection_rule")
        if isinstance(sample_ids, list) and len(sample_ids) == 1:
            if not isinstance(sample_ids[0], str) or not sample_ids[0] or "pending" in sample_ids[0].lower():
                errors.append("sample retrieval may not activate with a fake or pending sample_id")
            if dynamic_selector not in (None, False):
                errors.append("sample retrieval may use either one exact sample_id or the bounded selector, not both")
        elif sample_ids == []:
            if dynamic_selector != "only_single_original_human_sample_attached_to_bound_voice":
                errors.append("unknown sample ID requires the exact single-original-human-sample selection rule")
            if action.get("selection_fails_if_zero_or_multiple_samples") is not True:
                errors.append("dynamic sample selection must stop on zero or multiple metadata samples")
            if action.get("metadata_must_confirm_original_human_source") is not True:
                errors.append("dynamic sample selection must fail unless provenance confirms original human audio")
        else:
            errors.append("sample retrieval must bind one exact sample_id or the bounded metadata selection rule")
        if action.get("selection_fails_if_mixed_speaker") is not True:
            errors.append("sample retrieval must stop when the selected sample contains multiple speakers")
        for field in ("metadata_receipt_destination", "selected_sample_receipt_destination"):
            _validate_new_local_destination(
                artifact_root,
                action.get(field),
                f"action.{field}",
                errors,
                required_prefix="receipts",
            )
        receipt_destinations = [
            action.get("metadata_receipt_destination"),
            action.get("selected_sample_receipt_destination"),
        ]
        if all(isinstance(value, str) and value for value in receipt_destinations) and len(
            set(receipt_destinations)
        ) != len(receipt_destinations):
            errors.append("sample retrieval receipt destinations must be distinct")
        if not isinstance(destinations, list) or len(destinations) != 1:
            errors.append("sample retrieval must bind exactly one local destination")
        else:
            _validate_new_local_destination(
                artifact_root,
                destinations[0],
                "action.destinations[0]",
                errors,
                required_prefix="local-media",
            )
        if _positive_limit(limits, "max_calls", errors) != 2:
            errors.append("sample retrieval authorized_limits.max_calls must be exactly 2")
        if _positive_limit(limits, "max_downloads", errors) != 1:
            errors.append("sample retrieval authorized_limits.max_downloads must be exactly 1")
        _positive_limit(limits, "max_download_bytes", errors)
        _positive_limit(limits, "max_spend_usd", errors, allow_zero=True)
        _active_rights_record(action, artifact_root, errors)

    elif scope == "hume_clone_creation":
        if action.get("kind") != "manual_platform_ui_sample_upload_and_voice_clone":
            errors.append("Hume clone action.kind mismatch")
        if action.get("interface") != "hume_platform_ui":
            errors.append("Hume clone creation must use the documented Platform UI")
        if action.get("api_upload_endpoint") is not None:
            errors.append("Hume human-sample upload API must not be asserted")
        _verify_existing_local_binding(
            artifact_root,
            action.get("source_sample_path"),
            action.get("source_sample_sha256"),
            "action.source_sample",
            errors,
            required_prefix="local-media",
        )
        mime = action.get("source_sample_mime_type")
        if not isinstance(mime, str) or not mime.startswith("audio/"):
            errors.append("action.source_sample_mime_type must identify audio")
        if not _is_number(action.get("source_sample_duration_seconds")) or action.get("source_sample_duration_seconds", 0) <= 0:
            errors.append("action.source_sample_duration_seconds must be positive")
        rights = _active_rights_record(action, artifact_root, errors)
        if isinstance(rights, dict) and action.get("source_sample_rights_record") != rights.get("record_path"):
            errors.append(
                "action.source_sample_rights_record must exactly equal the verified rights_and_consent record_path"
            )
        _validate_new_local_destination(
            artifact_root,
            action.get("clone_receipt_destination"),
            "action.clone_receipt_destination",
            errors,
            required_prefix="receipts",
        )
        requirements = authorization.get("account_requirements")
        if not isinstance(requirements, dict):
            errors.append("Hume clone authorization requires account_requirements")
        else:
            if requirements.get("account_tier") in {None, "unverified", "free", "starter"}:
                errors.append("Hume commercial account tier is not verified")
            if requirements.get("commercial_use_eligibility") not in {True, "verified"}:
                errors.append("Hume commercial-use eligibility is not verified")
            if requirements.get("logged_in_session_is_authorization") is not False:
                errors.append("a logged-in Hume session must not be treated as authorization")
            _verify_existing_local_binding(
                artifact_root,
                requirements.get("commercial_terms_receipt_path"),
                requirements.get("commercial_terms_receipt_sha256"),
                "account_requirements.commercial_terms_receipt",
                errors,
                required_prefix="receipts",
            )
        if _positive_limit(limits, "max_ui_uploads", errors) != 1:
            errors.append("Hume clone authorization permits exactly one UI upload")
        if _positive_limit(limits, "max_voice_clones", errors) != 1:
            errors.append("Hume clone authorization permits exactly one clone")
        _positive_limit(limits, "max_spend_usd", errors, allow_zero=True)

    elif scope == "elevenlabs_calibration":
        if action.get("kind") != "bounded_tts_calibration":
            errors.append("ElevenLabs calibration action.kind mismatch")
        requests = _requests_from_dry_run(dry_run, "elevenlabs")
        provider_plan = _provider_from_plan(plan, "elevenlabs")
        plan_voice_id: str | None = None
        if not provider_plan:
            errors.append("bound plan is missing ElevenLabs")
        else:
            plan_voice_id = provider_plan.get("voice_id")
            if action.get("voice_id") != provider_plan.get("voice_id") or action.get("model_id") != "eleven_v3":
                errors.append("ElevenLabs calibration voice/model mismatch")

        _validate_eleven_calibration_voice_provenance(
            authorization,
            action,
            plan_voice_id,
            artifact_root,
            errors,
            required=True,
        )
        if action.get("request_ids") != [request.get("request_id") for request in requests]:
            errors.append("ElevenLabs calibration request_ids do not match the compiled dry run")
        if action.get("preferred_output_format") != "pcm_48000":
            errors.append("ElevenLabs calibration must request pcm_48000 first")
        fallback_enabled = any(
            request.get("fallback_request", {}).get("enabled") is True for request in requests
        )
        if fallback_enabled:
            if action.get("only_permitted_fallback") != "mp3_44100_192":
                errors.append("ElevenLabs calibration fallback must be mp3_44100_192")
            if action.get("fallback_reason_required") != "pcm_capability_unavailable":
                errors.append("ElevenLabs calibration fallback reason mismatch")
            if action.get("fallback_requires_capability_rejection_receipt") is not True:
                errors.append("ElevenLabs fallback requires a capability-rejection receipt")
            if action.get("fallback_requires_actual_codec_bitrate_verification") is not True:
                errors.append("ElevenLabs fallback requires actual codec and bitrate verification")
        elif any(
            action.get(field) not in (None, False)
            for field in (
                "only_permitted_fallback",
                "fallback_reason_required",
                "fallback_requires_capability_rejection_receipt",
                "fallback_requires_actual_codec_bitrate_verification",
            )
        ):
            errors.append("disabled ElevenLabs fallback may not be claimed in authorization")
        primary_calls = sum(request.get("planned_call_count", 0) for request in requests)
        fallback_calls = sum(
            request.get("fallback_request", {}).get("planned_additional_call_count", 0)
            for request in requests
        )
        maximum_calls = primary_calls + fallback_calls
        if action.get("fallback_request_call_ceiling") != fallback_calls:
            errors.append(
                f"ElevenLabs fallback_request_call_ceiling must be exactly {fallback_calls}"
            )
        exact_outputs = sum(request.get("planned_output_count", 0) for request in requests)
        maximum_characters = sum(
            request.get("estimated_billable_character_count", 0)
            + request.get("fallback_request", {}).get(
                "estimated_additional_billable_character_count", 0
            )
            for request in requests
        )
        maximum_spend = sum(
            request.get("estimated_public_rate_cost_usd", 0)
            + request.get("fallback_request", {}).get(
                "estimated_additional_public_rate_cost_usd", 0
            )
            for request in requests
        )
        if _positive_limit(limits, "max_calls", errors) != maximum_calls:
            errors.append(
                f"ElevenLabs max_calls must be exactly {maximum_calls}, including one fallback per request"
            )
        if _positive_limit(limits, "max_outputs", errors) != exact_outputs:
            errors.append(f"ElevenLabs max_outputs must be exactly {exact_outputs}")
        char_cap = _positive_limit(limits, "max_characters", errors)
        if char_cap is not None and char_cap != maximum_characters:
            errors.append("ElevenLabs max_characters must exactly equal the compiled fallback maximum")
        spend_cap = _positive_limit(limits, "max_spend_usd", errors)
        if spend_cap is not None and abs(spend_cap - maximum_spend) > 1e-9:
            errors.append("ElevenLabs max_spend_usd must exactly equal the modeled fallback maximum")

    elif scope == "hume_calibration":
        if action.get("kind") != "bounded_tts_calibration":
            errors.append("Hume calibration action.kind mismatch")
        requests = _requests_from_dry_run(dry_run, "hume")
        provider_plan = _provider_from_plan(plan, "hume")
        voice_id = action.get("voice_id")
        if (
            not provider_plan
            or voice_id != provider_plan.get("voice_id")
            or not isinstance(voice_id, str)
            or not voice_id
            or voice_id == HUME_CLONE_PLACEHOLDER
        ):
            errors.append("Hume calibration requires the real plan-bound clone voice_id")
        if action.get("model_id") != "octave-1":
            errors.append("Hume calibration model must be octave-1")
        if action.get("request_ids") != [request.get("request_id") for request in requests]:
            errors.append("Hume calibration request_ids do not match the compiled dry run")
        if action.get("num_generations_per_request") != 2:
            errors.append("Hume calibration requires exactly two generations per request")
        if action.get("requested_format") != "wav":
            errors.append("Hume calibration must request wav")
        fallback_enabled = any(
            request.get("fallback_request", {}).get("enabled") is True for request in requests
        )
        if fallback_enabled:
            if action.get("only_permitted_fallback") != "mp3_44100_192":
                errors.append("Hume calibration fallback must be mp3_44100_192")
            if action.get("fallback_reason_required") != "lossless_capability_unavailable":
                errors.append("Hume calibration fallback reason mismatch")
            if action.get("fallback_requires_capability_rejection_receipt") is not True:
                errors.append("Hume fallback requires a capability-rejection receipt")
            if action.get("fallback_requires_actual_codec_bitrate_verification") is not True:
                errors.append("Hume fallback requires actual codec and bitrate verification")
        elif any(
            action.get(field) not in (None, False)
            for field in (
                "only_permitted_fallback",
                "fallback_reason_required",
                "fallback_requires_capability_rejection_receipt",
                "fallback_requires_actual_codec_bitrate_verification",
            )
        ):
            errors.append("disabled Hume fallback may not be claimed in authorization")
        authorization_bindings = authorization.get("bindings", {})
        if authorization_bindings.get("compiled_hash_state") != "final_real_clone_id_bound":
            errors.append("Hume calibration compiled_hash_state must be final_real_clone_id_bound")
        _verify_existing_local_binding(
            artifact_root,
            authorization_bindings.get("clone_receipt_path"),
            authorization_bindings.get("clone_receipt_sha256"),
            "bindings.clone_receipt",
            errors,
            required_prefix="receipts",
        )
        requirements = authorization.get("account_requirements")
        if not isinstance(requirements, dict):
            errors.append("Hume calibration requires account_requirements")
        else:
            if requirements.get("account_tier") in {None, "unverified", "free", "starter"}:
                errors.append("Hume calibration commercial account tier is not verified")
            if requirements.get("commercial_use_eligibility") not in {True, "verified"}:
                errors.append("Hume calibration commercial-use eligibility is not verified")
            if requirements.get("logged_in_session_is_authorization") is not False:
                errors.append("a logged-in Hume session must not be treated as calibration authorization")
            _verify_existing_local_binding(
                artifact_root,
                requirements.get("commercial_terms_receipt_path"),
                requirements.get("commercial_terms_receipt_sha256"),
                "account_requirements.commercial_terms_receipt",
                errors,
                required_prefix="receipts",
            )
        primary_calls = sum(request.get("planned_call_count", 0) for request in requests)
        fallback_calls = sum(
            request.get("fallback_request", {}).get("planned_additional_call_count", 0)
            for request in requests
        )
        maximum_calls = primary_calls + fallback_calls
        if action.get("fallback_request_call_ceiling") != fallback_calls:
            errors.append(f"Hume fallback_request_call_ceiling must be exactly {fallback_calls}")
        exact_outputs = sum(request.get("planned_output_count", 0) for request in requests)
        maximum_characters = sum(
            request.get("estimated_billable_character_count", 0)
            + request.get("fallback_request", {}).get(
                "estimated_additional_billable_character_count", 0
            )
            for request in requests
        )
        maximum_spend = sum(
            request.get("estimated_public_rate_cost_usd", 0)
            + request.get("fallback_request", {}).get(
                "estimated_additional_public_rate_cost_usd", 0
            )
            for request in requests
        )
        if _positive_limit(limits, "max_calls", errors) != maximum_calls:
            errors.append(
                f"Hume max_calls must be exactly {maximum_calls}, including one fallback per request"
            )
        if _positive_limit(limits, "max_outputs", errors) != exact_outputs:
            errors.append(f"Hume max_outputs must be exactly {exact_outputs}")
        char_cap = _positive_limit(limits, "max_characters", errors)
        if char_cap is not None and char_cap != maximum_characters:
            errors.append("Hume max_characters must exactly equal the compiled fallback maximum")
        spend_cap = _positive_limit(limits, "max_spend_usd", errors)
        if spend_cap is not None and abs(spend_cap - maximum_spend) > 1e-9:
            errors.append("Hume max_spend_usd must exactly equal the modeled fallback maximum")

    if errors:
        raise ValidationError(errors)
    return {
        "valid": True,
        "schema_version": PROVIDER_ACTION_AUTHORIZATION_SCHEMA,
        "authorization_sha256": sha256_file(authorization_path),
        "scope": scope,
        "status": "active",
        "execution_ready": True,
        "network_authorized_for_scope_only": True,
        "expires_at": authorization["expires_at"],
        "consumption_record_absent": True,
    }
