"""Contract for a directed synthetic guide and one later voice transfer.

It freezes the P01 words, compiles the exact Google Cloud TTS request, and
validates a separately authorized guide-generation scope.  The sole external
transport is the fail-closed G1 Google guide microtest.  It is unavailable
without an exact active authorization, consumes that authorization before
credential refresh or provider network, performs exactly two one-shot POSTs,
and never records a token or raw quota-project identifier.  The later
ElevenLabs Voice Changer scope remains validation-only and blocked until one
exact guide has passed lexical, technical, creative, ownership, data-use, and
voice-rights gates.

The two authorities are intentionally non-fungible: a guide authorization can
never authorize disclosure to ElevenLabs, and a voice-transfer authorization
can never generate or select a guide.
"""

from __future__ import annotations

import base64
import binascii
import json
import math
import os
import re
import shutil
import stat
import subprocess
import urllib.error
import urllib.request
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
import tempfile
from typing import Any, BinaryIO

from .core import (
    ValidationError,
    read_canonical_w,
    read_json,
    sha256_bytes,
    sha256_file,
    token_identity,
)


PLAN_SCHEMA = "oe-performance-transfer-plan-v1"
GUIDE_AUTH_SCHEMA = "oe-synthetic-guide-authorization-v1"
GUIDE_RECOVERY_AUTH_SCHEMA = "oe-synthetic-guide-authorization-v2"
TRANSFER_AUTH_SCHEMA = "oe-voice-transfer-authorization-v1"
GUIDE_SCOPE = "synthetic_guide_generation"
TRANSFER_SCOPE = "elevenlabs_voice_transfer"

GUIDE_PROVIDER = "google_cloud_text_to_speech"
GUIDE_ENDPOINT = "https://us-texttospeech.googleapis.com/v1/text:synthesize"
GUIDE_MODEL = "gemini-2.5-pro-tts"
GUIDE_VOICE = "Achird"
GUIDE_LANGUAGE = "en-US"
GUIDE_AUDIO_ENCODING = "LINEAR16"
GUIDE_SAMPLE_RATE_HZ = 24_000
GUIDE_REQUEST_COUNT = 2
GUIDE_MAX_CALLS = 2
GUIDE_MAX_OUTPUTS = 2
GUIDE_MAX_SPEND_USD = 0.66
GUIDE_MAX_REQUEST_BODY_BYTES = 1_440
GUIDE_MAX_TOTAL_REQUEST_BYTES = 2_880
GUIDE_MAX_OUTPUT_DURATION_SECONDS = 50
GUIDE_MAX_OUTPUT_WAV_BYTES = 2_500_000
GUIDE_MAX_TOTAL_AUDIO_BYTES = 5_000_000
GUIDE_MAX_RESPONSE_BYTES_PER_CALL = 4_000_000
GUIDE_MODELED_SPEND_PER_CALL_USD = 0.33
GUIDE_COMBINED_INPUT_LIMIT_BYTES = 5_000
GUIDE_COMPONENT_INPUT_LIMIT_BYTES = 4_000
GUIDE_DESTINATIONS = (
    "outputs/raw/google/P01-W0030-W0110/candidate-A.wav",
    "outputs/raw/google/P01-W0030-W0110/candidate-B.wav",
)
GUIDE_CONSUMPTION_SCHEMA = "oe-provider-authorization-consumption-v1"
GUIDE_RECOVERY_CONSUMPTION_SCHEMA = "oe-provider-authorization-consumption-v2"
GUIDE_RUN_RECEIPT_SCHEMA = "oe-synthetic-guide-run-receipt-v1"
GUIDE_FAILURE_RECEIPT_SCHEMA = "oe-synthetic-guide-run-failure-v1"
GUIDE_QUOTA_PROJECT_ENV = "GOOGLE_CLOUD_QUOTA_PROJECT"
GUIDE_GCLOUD_TOKEN_COMMAND = (
    "auth",
    "application-default",
    "print-access-token",
    "--quiet",
)

MICROTEST_PASSAGE_ID = "P01"
MICROTEST_START_TOKEN = 30
MICROTEST_END_TOKEN = 110
MICROTEST_TOKEN_COUNT = 80
MICROTEST_TOKEN_SLICE_SHA256 = (
    "790a8176c5085968bd24c8572dacc5539b4e686f6b9b269cba2fd330c08d4a4a"
)
MICROTEST_TEXT_SHA256 = (
    "db3ccbb400f6bde4099f08b79b4402c374577cae4e622b0087649482e4f7d1cb"
)
MICROTEST_TEXT_CHARACTER_COUNT = 465
MICROTEST_TEXT = (
    "Your company is missing from the answer. Or worse, it is there, confidently "
    "described by someone who apparently met the company in 2022 and never checked "
    "back. You open the search dashboard. Everything is green. And the dashboard may "
    "be right. It is just watching a different doorway. That missing view is where "
    "this business starts. One experienced operator can use AI to map the answers, "
    "check the sources, and give the buyer a clear call on what deserves action."
)
GUIDE_ACTING_PROMPT = (
    "An experienced operator sits across a table from one smart peer. He is camera-ready, "
    "personally engaged, and working through a real puzzle, not reading copy. Speak the "
    "text exactly as written: add, omit, repeat, or paraphrase nothing. Start with the "
    "consequence. Let \"Or worse\" carry dry, knowing irritation; make \"Everything is "
    "green\" briefly deadpan; then turn at \"That missing view\" into genuine curiosity "
    "and practical excitement. Keep forward momentum, with thought-space at each turn. "
    "Energy eight of ten. Natural American conversation; emphasis follows meaning. Never "
    "sound like an announcer, trailer, podcast host, stage pitch, or motivational speaker. "
    "Pronounce \"2022\" as \"twenty twenty-two.\" Do not vocalize these directions."
)
GUIDE_ACTING_PROMPT_SHA256 = (
    "8cfe0391324bce56cb6bf6d83ef0e781479de14c08a7861716e9716f9017b416"
)
GUIDE_REQUEST_BODY_SHA256 = (
    "4acd99a738125e942fc1a6c2e4ef8df9c819397c9a2627fb494e73d63d004c53"
)
GUIDE_REQUEST_SET_SHA256 = (
    "ed1aa73a04db602b8ed2611731346e3f0bfae9d48d55a4f94bb5110da85c0cba"
)
GUIDE_SAFE_ERROR_CAPTURE_RUNTIME_SHA256 = (
    "27cf742ac8c169c05474269f6a40af642091c8180e8412cc410d2b8ab72ae6d9"
)
GUIDE_RUNTIME_RELATIVE = (
    "operator-blueprint-v2/02-narration-production/runtime/oe_narration/"
    "performance_transfer.py"
)
GUIDE_CLI_RELATIVE = (
    "operator-blueprint-v2/02-narration-production/runtime/oe_narration/cli.py"
)
GUIDE_CORE_RELATIVE = (
    "operator-blueprint-v2/02-narration-production/runtime/oe_narration/core.py"
)
GUIDE_INIT_RELATIVE = (
    "operator-blueprint-v2/02-narration-production/runtime/oe_narration/__init__.py"
)
GUIDE_SCHEMA_RELATIVE = (
    "operator-blueprint-v2/02-narration-production/schemas/"
    "synthetic-guide-authorization.schema.json"
)
GUIDE_TESTS_RELATIVE = (
    "operator-blueprint-v2/02-narration-production/runtime/tests/"
    "test_performance_transfer.py"
)
GUIDE_RECOVERY_BINDING = {
    "recovery_id": "G1R2-AIPLATFORM-SERVICE-ENABLED",
    "execution_semantics": "fresh_authorization_not_retry_or_resumption",
    "prior_failures": [
        {
            "attempt_id": "G1",
            "failure_receipt_path": (
                "receipts/google/AUTH-G1-ai-visibility-v1.1-p01-synthetic-guide-"
                "20260825T233757Z.failure.json"
            ),
            "failure_receipt_sha256": (
                "3cf567c2b8947f11166112ae63c7c652010f97d5095f7d042cd3f0f354d25ee1"
            ),
        },
        {
            "attempt_id": "G1R1",
            "failure_receipt_path": (
                "receipts/google/AUTH-G1R1-ai-visibility-v1.1-p01-synthetic-guide-"
                "20260826T003835Z.failure.json"
            ),
            "failure_receipt_sha256": (
                "df00adefe5e3215ff0c60ed19fe7835d2056a78ba2130e46b18a0d66de2161af"
            ),
        },
    ],
    "diagnosis": {
        "path": "evidence/G1R2-403-DIAGNOSIS.20260826T014109Z.json",
        "sha256": "335c7d6e29052f179dac19f868acea2430d3c99fcaedd6baf2c69cff7f7496d0",
        "cause_before_service_enablement": "unknown",
    },
    "service_enablement": {
        "authorization_path": (
            "authorizations/08-google-aiplatform-service-enablement-partial-response-"
            "repair.ACTIVE.20260826T033333Z.json"
        ),
        "authorization_sha256": (
            "c98d4ec1e12485fedda5f87df46e52b66bac99a916fb8a00632108efc3311d4b"
        ),
        "consumption_record_path": (
            "authorizations/consumed/AUTH-SVC-G1R2-AIPLATFORM-PARTIAL-REPAIR-"
            "20260826T033333Z.consumed.json"
        ),
        "consumption_record_sha256": (
            "45ee119e1ee5e258152226be72a435c1d0bd61e851295b4d311f5c24a20ee246"
        ),
        "run_receipt_path": (
            "receipts/google-service-usage/AUTH-SVC-G1R2-AIPLATFORM-PARTIAL-REPAIR-"
            "20260826T033333Z.run.json"
        ),
        "run_receipt_sha256": (
            "a439c64c0b58f6bc7eee22ee15f21bfe5d77da5d0f88712797f7f9b0c2f98b60"
        ),
        "success_disposition_path": (
            "evidence/G1R2-AIPLATFORM-SERVICE-SUCCESS-AND-GUIDE-READINESS."
            "20260826T034027Z.json"
        ),
        "success_disposition_sha256": (
            "4497327fd3bac9c751f56c325ebf27d41b5413b92b05206177cf05fa73df86f6"
        ),
        "service": "aiplatform.googleapis.com",
        "final_state": "ENABLED",
    },
    "safe_error_capture_runtime_sha256": GUIDE_SAFE_ERROR_CAPTURE_RUNTIME_SHA256,
    "request_body_sha256": GUIDE_REQUEST_BODY_SHA256,
    "request_set_sha256": GUIDE_REQUEST_SET_SHA256,
    "fresh_output_paths": list(GUIDE_DESTINATIONS),
    "prior_outputs_received": 0,
    "prior_authorizations_reusable": False,
    "retry_or_resumption_authorized": False,
}

TRANSFER_PROVIDER = "elevenlabs"
TRANSFER_TARGET_VOICE_ID = "scMbPZwQjr40V1MzL3Nj"
TRANSFER_ENDPOINT_PATH = f"/v1/speech-to-speech/{TRANSFER_TARGET_VOICE_ID}"
TRANSFER_ENDPOINT = f"https://api.elevenlabs.io{TRANSFER_ENDPOINT_PATH}"
TRANSFER_MODEL = "eleven_multilingual_sts_v2"
TRANSFER_SEED = 2_026_082_501
TRANSFER_PRIMARY_FORMAT = "pcm_48000"
TRANSFER_FALLBACK_FORMAT = "mp3_44100_192"
TRANSFER_DESTINATION = "outputs/raw/elevenlabs/P01-W0030-W0110/saved-c-transfer.pcm"
TRANSFER_MAX_CALLS = 2
TRANSFER_MAX_OUTPUTS = 1
TRANSFER_MAX_SOURCE_BYTES = 50_000_000
TRANSFER_MAX_SOURCE_DURATION_SECONDS = 50
TRANSFER_MAX_SUBMITTED_SECONDS = 100
TRANSFER_MAX_SPEND_USD = 0.24
TRANSFER_VOICE_SETTINGS = {
    "similarity_boost": 0.80,
    "speed": 1.0,
    "stability": 0.40,
    "style": 0.0,
    "use_speaker_boost": True,
}
ACCOUNT_TRAINING_OPT_OUT_PROTECTION = "account_training_opt_out_processed"
ENTERPRISE_ZRM_PROTECTION = "enterprise_zrm"

_SHA_RE = re.compile(r"^[0-9a-f]{64}$")
_GIT_SHA_RE = re.compile(r"^[0-9a-f]{40}$")
_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,159}$")
_SECRET_KEY_RE = re.compile(
    r"(?:api[_-]?key|authorization[_-]?header|bearer|password|secret|access[_-]?token|refresh[_-]?token|credential[_-]?value|project[_-]?id|account[_-]?id)",
    re.I,
)
_SECRET_VALUE_RE = re.compile(
    r"(?:AIza[0-9A-Za-z_-]{20,}|ya29\.[0-9A-Za-z._-]+|xi[_-][0-9A-Za-z_-]{12,}|sk[_-][0-9A-Za-z_-]{12,})"
)
_GOOGLE_ERROR_STATUSES = frozenset(
    {
        "ABORTED",
        "ALREADY_EXISTS",
        "CANCELLED",
        "DATA_LOSS",
        "DEADLINE_EXCEEDED",
        "FAILED_PRECONDITION",
        "INTERNAL",
        "INVALID_ARGUMENT",
        "NOT_FOUND",
        "OUT_OF_RANGE",
        "PERMISSION_DENIED",
        "RESOURCE_EXHAUSTED",
        "UNAUTHENTICATED",
        "UNAVAILABLE",
        "UNIMPLEMENTED",
        "UNKNOWN",
    }
)
_GOOGLE_ERROR_INFO_REASONS = frozenset(
    {
        "ACCESS_TOKEN_EXPIRED",
        "ACCESS_TOKEN_SCOPE_INSUFFICIENT",
        "ACCOUNT_STATE_INVALID",
        "BILLING_DISABLED",
        "CONSUMER_INVALID",
        "CONSUMER_SUSPENDED",
        "IAM_PERMISSION_DENIED",
        "LOCATION_POLICY_VIOLATED",
        "ORG_RESTRICTION_VIOLATION",
        "RESOURCE_QUOTA_EXCEEDED",
        "SECURITY_POLICY_VIOLATED",
        "SERVICE_DISABLED",
        "SERVICE_USAGE_DENIED",
        "USER_PROJECT_DENIED",
    }
)
_GOOGLE_ERROR_INFO_DOMAINS = frozenset(
    {
        "googleapis.com",
        "iam.googleapis.com",
        "serviceusage.googleapis.com",
    }
)
_GOOGLE_ERROR_SERVICES = frozenset(
    {
        "aiplatform.googleapis.com",
        "cloudresourcemanager.googleapis.com",
        "serviceusage.googleapis.com",
        "texttospeech.googleapis.com",
        "us-texttospeech.googleapis.com",
    }
)
_GOOGLE_ERROR_PERMISSIONS = frozenset(
    {
        "aiplatform.endpoints.predict",
        "serviceusage.services.enable",
        "serviceusage.services.use",
        "texttospeech.synthesize",
    }
)
_GOOGLE_ERROR_INFO_TYPE = "type.googleapis.com/google.rpc.ErrorInfo"


def _compact_json_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def _json_exact(actual: Any, expected: Any) -> bool:
    """Compare JSON-like values without Python's bool/int numeric coercion."""

    if type(actual) is not type(expected):
        return False
    if isinstance(expected, dict):
        return set(actual) == set(expected) and all(
            _json_exact(actual[key], expected[key]) for key in expected
        )
    if isinstance(expected, (list, tuple)):
        return len(actual) == len(expected) and all(
            _json_exact(left, right)
            for left, right in zip(actual, expected, strict=True)
        )
    return actual == expected


def _strict_object(value: Any, allowed: set[str], required: set[str], label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValidationError(f"{label} must be an object")
    unknown = sorted(set(value) - allowed)
    missing = sorted(required - set(value))
    errors: list[str] = []
    if unknown:
        errors.append(f"{label} contains unsupported keys: {', '.join(unknown)}")
    if missing:
        errors.append(f"{label} is missing required keys: {', '.join(missing)}")
    if errors:
        raise ValidationError(errors)
    return value


def _require(value: bool, message: str, errors: list[str]) -> None:
    if not value:
        errors.append(message)


def _is_number(value: Any) -> bool:
    return (
        isinstance(value, (int, float))
        and not isinstance(value, bool)
        and math.isfinite(float(value))
    )


def _scan_for_secrets(value: Any, label: str = "document") -> list[str]:
    errors: list[str] = []

    def visit(current: Any, path: str) -> None:
        if isinstance(current, dict):
            for key, nested in current.items():
                key_text = str(key)
                if _SECRET_KEY_RE.search(key_text) and key_text not in {
                    "quota_project_sha256",
                    "credential_source",
                }:
                    errors.append(f"{path}.{key_text} may disclose protected account or credential material")
                visit(nested, f"{path}.{key_text}")
        elif isinstance(current, list):
            for index, nested in enumerate(current):
                visit(nested, f"{path}[{index}]")
        elif isinstance(current, str) and _SECRET_VALUE_RE.search(current):
            errors.append(f"{path} appears to contain credential material")

    visit(value, label)
    return errors


def _parse_time(value: Any, label: str, errors: list[str]) -> datetime | None:
    if not isinstance(value, str) or not value:
        errors.append(f"{label} is required")
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        errors.append(f"{label} must be ISO-8601")
        return None
    if parsed.tzinfo is None:
        errors.append(f"{label} must include a timezone")
        return None
    return parsed.astimezone(timezone.utc)


def _document_root(document_path: Path) -> Path:
    """Return the fixture root for a document below it."""

    document_path = Path(document_path).absolute()

    def checked(root: Path) -> Path:
        try:
            relative = document_path.relative_to(root)
        except ValueError as exc:
            raise ValidationError("document path is not below its fixture root") from exc
        current = root
        if current.is_symlink():
            raise ValidationError("fixture root may not be a symlink")
        for component in relative.parts:
            current = current / component
            if current.is_symlink():
                raise ValidationError("document path may not traverse a symlink")
        if not document_path.is_file():
            raise ValidationError("document path must be an existing regular file")
        return root.resolve(strict=True)

    for candidate in (document_path.parent, *document_path.parents):
        if candidate.parent.name == "fixtures":
            return checked(candidate)
    # Temporary unit fixtures may not reproduce the complete repository tree.
    if document_path.parent.name in {"authorizations", "compiled", "reviews"}:
        return checked(document_path.parent.parent)
    return checked(document_path.parent)


def _safe_relative(
    root: Path,
    value: Any,
    label: str,
    *,
    must_exist: bool,
    suffix: str | None = None,
) -> Path:
    if not isinstance(value, str) or not value:
        raise ValidationError(f"{label} must be a non-empty relative path")
    relative = Path(value)
    if relative.is_absolute() or any(part in {"", ".", "..", "~"} for part in relative.parts):
        raise ValidationError(f"{label} must be a safe relative path")
    if suffix is not None and relative.suffix.lower() != suffix:
        raise ValidationError(f"{label} must end in {suffix}")
    candidate = root / relative
    resolved_root = root.resolve(strict=True)
    current = root
    for component in relative.parts:
        current = current / component
        if current.is_symlink():
            raise ValidationError(f"{label} may not traverse a symlink")
    try:
        resolved = candidate.resolve(strict=must_exist)
    except OSError as exc:
        raise ValidationError(f"cannot resolve {label}") from exc
    if not resolved.is_relative_to(resolved_root):
        raise ValidationError(f"{label} escapes the fixture root")
    if must_exist and (not candidate.is_file() or candidate.is_symlink()):
        raise ValidationError(f"{label} must be an existing regular file")
    return candidate


def _canonical_w_binding(plan_path: Path, value: Any, supplied_path: Path) -> dict[str, Any]:
    """Resolve the one canonical W across sibling fixtures, never outside fixtures/."""

    binding = _strict_object(
        value,
        {"path", "sha256", "token_count"},
        {"path", "sha256", "token_count"},
        "canonical_w",
    )
    raw = binding.get("path")
    if not isinstance(raw, str) or not raw or Path(raw).is_absolute():
        raise ValidationError("canonical_w.path must be a non-empty relative path")
    fixture_root = _document_root(plan_path)
    fixtures_root = fixture_root.parent
    current = plan_path.parent
    for component in Path(raw).parts:
        current = current / component
        if current.is_symlink():
            raise ValidationError("canonical_w.path may not traverse a symlink")
    try:
        resolved = (plan_path.parent / raw).resolve(strict=True)
        supplied = supplied_path.resolve(strict=True)
        allowed = fixtures_root.resolve(strict=True)
    except OSError as exc:
        raise ValidationError("cannot resolve canonical_w.path") from exc
    if not resolved.is_relative_to(allowed):
        raise ValidationError("canonical_w.path escapes the narration fixtures root")
    if resolved != supplied or not resolved.is_file() or resolved.is_symlink():
        raise ValidationError("canonical_w.path does not bind the supplied canonical W")
    return binding


def _path_hash(
    root: Path,
    value: Any,
    label: str,
    *,
    suffix: str | None = None,
) -> tuple[Path, dict[str, Any]]:
    binding = _strict_object(value, {"path", "sha256"}, {"path", "sha256"}, label)
    path = _safe_relative(root, binding["path"], f"{label}.path", must_exist=True, suffix=suffix)
    if not isinstance(binding["sha256"], str) or not _SHA_RE.fullmatch(binding["sha256"]):
        raise ValidationError(f"{label}.sha256 must be lowercase SHA-256")
    if sha256_file(path) != binding["sha256"]:
        raise ValidationError(f"{label} SHA-256 mismatch")
    return path, binding


def _target(value: Any, label: str = "target") -> dict[str, Any]:
    target = _strict_object(value, {"kind", "id"}, {"kind", "id"}, label)
    errors: list[str] = []
    _require(target.get("kind") in {"fixture", "experiment"}, f"{label}.kind must be fixture or experiment", errors)
    _require(isinstance(target.get("id"), str) and bool(target["id"]), f"{label}.id is required", errors)
    if errors:
        raise ValidationError(errors)
    return target


def _guide_body(text: str) -> dict[str, Any]:
    return {
        "advancedVoiceOptions": {"enableTextnorm": False},
        "audioConfig": {
            "audioEncoding": GUIDE_AUDIO_ENCODING,
            "sampleRateHertz": GUIDE_SAMPLE_RATE_HZ,
        },
        "input": {"prompt": GUIDE_ACTING_PROMPT, "text": text},
        "voice": {
            "languageCode": GUIDE_LANGUAGE,
            "modelName": GUIDE_MODEL,
            "name": GUIDE_VOICE,
        },
    }


def _validate_frozen_guide_body(text: str) -> tuple[dict[str, Any], bytes]:
    body = _guide_body(text)
    body_bytes = _compact_json_bytes(body)
    errors: list[str] = []
    _require(sha256_bytes(GUIDE_ACTING_PROMPT.encode("utf-8")) == GUIDE_ACTING_PROMPT_SHA256, "frozen guide prompt constant drifted", errors)
    _require(len(body_bytes) == GUIDE_MAX_REQUEST_BODY_BYTES, "frozen guide request byte count drifted", errors)
    _require(sha256_bytes(body_bytes) == GUIDE_REQUEST_BODY_SHA256, "frozen guide request body hash drifted", errors)
    prompt_bytes = len(GUIDE_ACTING_PROMPT.encode("utf-8"))
    text_bytes = len(text.encode("utf-8"))
    _require(prompt_bytes <= GUIDE_COMPONENT_INPUT_LIMIT_BYTES, "guide prompt exceeds component input cap", errors)
    _require(text_bytes <= GUIDE_COMPONENT_INPUT_LIMIT_BYTES, "guide text exceeds component input cap", errors)
    _require(prompt_bytes + text_bytes <= GUIDE_COMBINED_INPUT_LIMIT_BYTES, "guide prompt plus text exceeds combined input cap", errors)
    if errors:
        raise ValidationError(errors)
    return body, body_bytes


def _blueprint_root(path: Path) -> Path:
    for candidate in (path.parent, *path.parents):
        if candidate.name == "operator-blueprint-v2":
            return candidate.resolve(strict=True)
    raise ValidationError("performance envelope must live below operator-blueprint-v2")


def _safe_blueprint_file(
    document_path: Path,
    value: Any,
    expected_sha256: Any,
    label: str,
) -> Path:
    if not isinstance(value, str) or not value or Path(value).is_absolute():
        raise ValidationError(f"{label}.path must be relative")
    blueprint = _blueprint_root(document_path)
    current = document_path.parent
    for component in Path(value).parts:
        current = current / component
        if current.is_symlink():
            raise ValidationError(f"{label}.path may not traverse a symlink")
    try:
        resolved = (document_path.parent / value).resolve(strict=True)
    except OSError as exc:
        raise ValidationError(f"cannot resolve {label}.path") from exc
    if not resolved.is_relative_to(blueprint) or not resolved.is_file() or resolved.is_symlink():
        raise ValidationError(f"{label}.path must be a regular file below operator-blueprint-v2")
    if not isinstance(expected_sha256, str) or sha256_file(resolved) != expected_sha256:
        raise ValidationError(f"{label} SHA-256 mismatch")
    return resolved


def _safe_blueprint_relative_file(
    document_path: Path,
    value: Any,
    expected_sha256: Any,
    label: str,
) -> Path:
    if not isinstance(value, str) or not value or Path(value).is_absolute():
        raise ValidationError(f"{label}.path must be operator-blueprint-v2-relative")
    relative = Path(value)
    if any(part in {"", ".", "..", "~"} for part in relative.parts):
        raise ValidationError(f"{label}.path contains an unsafe component")
    blueprint = _blueprint_root(document_path)
    candidate = blueprint / relative
    current = blueprint
    for component in relative.parts:
        current = current / component
        if current.is_symlink():
            raise ValidationError(f"{label}.path may not traverse a symlink")
    try:
        resolved = candidate.resolve(strict=True)
    except OSError as exc:
        raise ValidationError(f"cannot resolve {label}.path") from exc
    if not resolved.is_relative_to(blueprint) or not resolved.is_file() or resolved.is_symlink():
        raise ValidationError(f"{label}.path must be a regular file below operator-blueprint-v2")
    if not isinstance(expected_sha256, str) or sha256_file(resolved) != expected_sha256:
        raise ValidationError(f"{label} SHA-256 mismatch")
    return resolved


def _validate_partition_map(
    values: Any,
    label: str,
    expected: list[tuple[int, int, str]],
) -> None:
    if not isinstance(values, list) or len(values) != len(expected):
        raise ValidationError(f"{label} must contain the exact frozen partition count")
    errors: list[str] = []
    for index, (value, frozen) in enumerate(zip(values, expected, strict=True)):
        try:
            item = _strict_object(
                value,
                {"id", "start_token", "end_token", "spoken_text_sha256"},
                {"id", "start_token", "end_token", "spoken_text_sha256"},
                f"{label}[{index}]",
            )
        except ValidationError as exc:
            errors.extend(exc.errors)
            continue
        start, end, digest = frozen
        _require(isinstance(item.get("id"), str) and bool(item["id"]), f"{label}[{index}].id is required", errors)
        _require(
            _json_exact(
                (item.get("start_token"), item.get("end_token"), item.get("spoken_text_sha256")),
                (start, end, digest),
            ),
            f"{label}[{index}] does not match frozen W[{start},{end})",
            errors,
        )
    if errors:
        raise ValidationError(errors)


def _validate_performance_envelope(
    envelope_path: Path,
    canonical_w_path: Path,
    tokens: list[str],
    target: dict[str, Any],
) -> None:
    envelope = read_json(envelope_path)
    _strict_object(
        envelope,
        {
            "schema_version", "envelope_id", "status", "target", "episode_number",
            "public_fact_clearance", "step3_authorized", "script", "canonical_w",
            "performance", "passages",
        },
        {
            "schema_version", "envelope_id", "status", "target", "episode_number",
            "public_fact_clearance", "step3_authorized", "script", "canonical_w",
            "performance", "passages",
        },
        "performance envelope",
    )
    errors = _scan_for_secrets(envelope, "performance_envelope")
    _require(envelope.get("schema_version") == "oe-performance-envelope-v1", "performance envelope schema drifted", errors)
    _require(envelope.get("status") == "dry_run_frozen", "performance envelope must be dry_run_frozen", errors)
    _require(envelope.get("target") == target, "performance envelope target mismatch", errors)
    _require(envelope.get("episode_number") is None, "microtest envelope must not assign an episode number", errors)
    _require(envelope.get("public_fact_clearance") is False, "public fact clearance must remain false", errors)
    _require(envelope.get("step3_authorized") is False, "Step 3 must remain unauthorized", errors)
    script = _strict_object(envelope.get("script"), {"path", "sha256"}, {"path", "sha256"}, "performance envelope script")
    try:
        _safe_blueprint_file(envelope_path, script.get("path"), script.get("sha256"), "performance envelope script")
    except ValidationError as exc:
        errors.extend(exc.errors)
    canonical = _strict_object(
        envelope.get("canonical_w"),
        {"path", "schema_version", "tokenization", "serialization", "token_count", "sha256"},
        {"path", "schema_version", "tokenization", "serialization", "token_count", "sha256"},
        "performance envelope canonical_w",
    )
    expected_canonical = {
        "schema_version": "oe-spoken-text-v1",
        "tokenization": "python-str-split-whitespace",
        "serialization": "utf8-one-token-per-lf-with-terminal-lf",
        "token_count": len(tokens),
        "sha256": sha256_file(canonical_w_path),
    }
    for key, expected in expected_canonical.items():
        _require(_json_exact(canonical.get(key), expected), f"performance envelope canonical_w.{key} mismatch", errors)
    try:
        raw_w_path = canonical.get("path")
        if not isinstance(raw_w_path, str) or not raw_w_path or Path(raw_w_path).is_absolute():
            raise ValidationError("performance envelope canonical_w.path must be relative")
        current_w_path = envelope_path.parent
        for component in Path(raw_w_path).parts:
            current_w_path = current_w_path / component
            if current_w_path.is_symlink():
                raise ValidationError("performance envelope canonical_w.path may not traverse a symlink")
        resolved_w = (envelope_path.parent / raw_w_path).resolve(strict=True)
        _require(resolved_w == canonical_w_path.resolve(strict=True), "performance envelope canonical_w.path mismatch", errors)
    except ValidationError as exc:
        errors.extend(exc.errors)
    except OSError:
        errors.append("cannot resolve performance envelope canonical_w.path")

    performance = _strict_object(
        envelope.get("performance"),
        {"listener", "relationship", "identity_target", "energy_arc", "must_preserve", "must_avoid", "states"},
        {"listener", "relationship", "identity_target", "energy_arc", "must_preserve", "must_avoid", "states"},
        "performance envelope performance",
    )
    for key in ("listener", "relationship", "identity_target", "energy_arc"):
        _require(isinstance(performance.get(key), str) and bool(performance[key]), f"performance.{key} is required", errors)
    for key in ("must_preserve", "must_avoid"):
        value = performance.get(key)
        _require(isinstance(value, list) and bool(value) and all(isinstance(item, str) and item for item in value), f"performance.{key} must be non-empty strings", errors)
    states = performance.get("states")
    if not isinstance(states, list) or len(states) != 4:
        errors.append("performance.states must contain the four frozen acting states")
    else:
        state_ids: list[Any] = []
        for index, state in enumerate(states):
            try:
                state = _strict_object(state, {"id", "sound"}, {"id", "sound"}, f"performance.states[{index}]")
                state_ids.append(state.get("id"))
                _require(isinstance(state.get("sound"), str) and bool(state["sound"]), f"performance.states[{index}].sound is required", errors)
            except ValidationError as exc:
                errors.extend(exc.errors)
        _require(_json_exact(state_ids, ["consequence", "dry_recognition", "diagnostic_reset", "possibility"]), "performance state order drifted", errors)

    passages = envelope.get("passages")
    if not isinstance(passages, list) or len(passages) != 1:
        errors.append("performance envelope must contain exactly one P01 microtest passage")
        if errors:
            raise ValidationError(errors)
        return
    passage = _strict_object(
        passages[0],
        {
            "id", "source_blocks", "start_token", "end_token", "token_count", "spoken_text_sha256",
            "transport_text", "performance_function", "objective", "state_arc", "energy",
            "required_anchors", "anti_targets", "paragraph_boundaries", "thought_boundaries",
        },
        {
            "id", "source_blocks", "start_token", "end_token", "token_count", "spoken_text_sha256",
            "transport_text", "performance_function", "objective", "state_arc", "energy",
            "required_anchors", "anti_targets", "paragraph_boundaries", "thought_boundaries",
        },
        "performance envelope passage",
    )
    _require(passage.get("id") == "P01-W0030-W0110", "performance envelope passage ID drifted", errors)
    _require(_json_exact(passage.get("source_blocks"), ["S00"]), "performance envelope source block drifted", errors)
    _require(_json_exact((passage.get("start_token"), passage.get("end_token"), passage.get("token_count")), (30, 110, 80)), "performance envelope passage range drifted", errors)
    _require(passage.get("spoken_text_sha256") == MICROTEST_TOKEN_SLICE_SHA256, "performance envelope passage token hash drifted", errors)
    for key in ("performance_function", "objective"):
        _require(isinstance(passage.get(key), str) and bool(passage[key]), f"passage.{key} is required", errors)
    _require(_json_exact(passage.get("state_arc"), ["consequence", "dry_recognition", "diagnostic_reset", "possibility"]), "passage state arc drifted", errors)
    anti_targets = passage.get("anti_targets")
    _require(isinstance(anti_targets, list) and bool(anti_targets) and all(isinstance(item, str) and item for item in anti_targets), "passage anti-targets are required", errors)
    energy = _strict_object(
        passage.get("energy"),
        {"scale", "start", "peak", "finish", "instruction"},
        {"scale", "start", "peak", "finish", "instruction"},
        "passage.energy",
    )
    _require(_json_exact((energy.get("scale"), energy.get("start"), energy.get("peak"), energy.get("finish")), ("0_to_10", 8, 8, 8)), "passage energy binding drifted", errors)
    _require(isinstance(energy.get("instruction"), str) and bool(energy["instruction"]), "passage energy instruction is required", errors)

    transport = _strict_object(
        passage.get("transport_text"),
        {"path", "serialization", "character_count", "sha256"},
        {"path", "serialization", "character_count", "sha256"},
        "passage.transport_text",
    )
    _require(transport.get("serialization") == "utf8-whitespace-normalized-single-space-no-terminal-lf", "transport serialization drifted", errors)
    _require(transport.get("character_count") == 465 and transport.get("sha256") == MICROTEST_TEXT_SHA256, "transport text binding drifted", errors)
    try:
        transport_path = _safe_relative(_document_root(envelope_path), transport.get("path"), "transport_text.path", must_exist=True, suffix=".txt")
        transport_bytes = transport_path.read_bytes()
        _require(transport_bytes == MICROTEST_TEXT.encode("utf-8"), "transport text bytes drifted", errors)
    except (ValidationError, OSError) as exc:
        errors.extend(exc.errors if isinstance(exc, ValidationError) else ["cannot read transport text"])

    anchors = passage.get("required_anchors")
    expected_anchors = [(30, "landing"), (37, "emphasis"), (57, "transition"), (65, "landing"), (78, "transition")]
    if not isinstance(anchors, list) or len(anchors) != len(expected_anchors):
        errors.append("passage anchors must equal the frozen 30/37/57/65/78 map")
    else:
        for index, (anchor, expected) in enumerate(zip(anchors, expected_anchors, strict=True)):
            try:
                anchor = _strict_object(anchor, {"at_token", "kind", "instruction"}, {"at_token", "kind", "instruction"}, f"required_anchors[{index}]")
                _require(_json_exact((anchor.get("at_token"), anchor.get("kind")), expected), f"required_anchors[{index}] drifted", errors)
                _require(isinstance(anchor.get("instruction"), str) and bool(anchor["instruction"]), f"required_anchors[{index}].instruction is required", errors)
            except ValidationError as exc:
                errors.extend(exc.errors)

    try:
        _validate_partition_map(
            passage.get("paragraph_boundaries"),
            "paragraph_boundaries",
            [
                (30, 37, "ed9fca4fe6b739dec4e383e8e3d39d0ee2abd41e9680e857ce2b9d8583e0f5e9"),
                (37, 57, "4b6d93aee26659cb693486ba3c7585fb7f6cd7d1c828737f2d487a60c76f9d14"),
                (57, 65, "39109a971904a8361aaefcd63ee7d36ca5b496c3268f0a1dab188e5a2930fa2c"),
                (65, 78, "60993213b04479fe5e8965c3d5089124285e67ba842bb60eae9f903c56fc0e41"),
                (78, 110, "38844419a0bf1b8014636678a01f8d83570aa68e88f5e9746ed1c85663280439"),
            ],
        )
        _validate_partition_map(
            passage.get("thought_boundaries"),
            "thought_boundaries",
            [
                (30, 57, "2cdd9b822f348c88d23990cc5647829fe31bdd2f2566c52dfc131004fdbad19c"),
                (57, 78, "15beee36c709f70955779f944bb32fbff61aad44a20b392fee26aba7ddf2b575"),
                (78, 110, "38844419a0bf1b8014636678a01f8d83570aa68e88f5e9746ed1c85663280439"),
            ],
        )
    except ValidationError as exc:
        errors.extend(exc.errors)
    if errors:
        raise ValidationError(errors)


def _validate_provider_adapters(
    root: Path,
    value: Any,
) -> dict[str, dict[str, str]]:
    bindings = _strict_object(
        value,
        {"google", "elevenlabs_voice_changer"},
        {"google", "elevenlabs_voice_changer"},
        "provider_adapters",
    )
    google_path, google_binding = _path_hash(
        root,
        bindings["google"],
        "provider_adapters.google",
        suffix=".json",
    )
    eleven_path, eleven_binding = _path_hash(
        root,
        bindings["elevenlabs_voice_changer"],
        "provider_adapters.elevenlabs_voice_changer",
        suffix=".json",
    )
    google = read_json(google_path)
    expected_google = {
        "record_type": "credential_free_provider_adapter",
        "status": "dry_run_only",
        "provider": GUIDE_PROVIDER,
        "endpoint": GUIDE_ENDPOINT,
        "method": "POST",
        "model_id": GUIDE_MODEL,
        "voice": {"name": GUIDE_VOICE, "language_code": GUIDE_LANGUAGE},
        "dialogue": {
            "canonical_range": "W[30,110)",
            "token_count": MICROTEST_TOKEN_COUNT,
            "path": "../passages/P01-W0030-W0110.locked.txt",
            "sha256": MICROTEST_TEXT_SHA256,
        },
        "acting_prompt": {
            "utf8_bytes": len(GUIDE_ACTING_PROMPT.encode("utf-8")),
            "sha256": GUIDE_ACTING_PROMPT_SHA256,
            "location": "request_body.input.prompt",
        },
        "request": {
            "canonical_serialization": "utf8-json-sort-keys-compact-ensure-ascii-false-no-terminal-lf",
            "body_bytes": GUIDE_MAX_REQUEST_BODY_BYTES,
            "body_sha256": GUIDE_REQUEST_BODY_SHA256,
            "count": GUIDE_REQUEST_COUNT,
            "identical_unseeded_stochastic": True,
            "retry": False,
            "redirect": False,
            "fallback": None,
        },
        "output": {
            "audio_encoding": GUIDE_AUDIO_ENCODING,
            "container": "wav",
            "sample_rate_hz": GUIDE_SAMPLE_RATE_HZ,
            "channels": 1,
            "preserve_original_bytes_for_qa_selection_and_transfer": True,
            "listening_derivative_transfer_eligible": False,
        },
        "credentials_accessed": False,
        "network_called": False,
        "audio_generated": False,
    }
    if not _json_exact(google, expected_google):
        raise ValidationError("Google provider adapter semantics drifted")
    dialogue_path = (google_path.parent / google["dialogue"]["path"]).resolve(strict=True)
    expected_dialogue = (root / "passages" / "P01-W0030-W0110.locked.txt").resolve(strict=True)
    if (
        dialogue_path != expected_dialogue
        or dialogue_path.is_symlink()
        or sha256_file(dialogue_path) != MICROTEST_TEXT_SHA256
        or dialogue_path.read_bytes() != MICROTEST_TEXT.encode("utf-8")
    ):
        raise ValidationError("Google provider adapter dialogue binding mismatch")

    eleven = read_json(eleven_path)
    expected_eleven = {
        "record_type": "blocked_future_provider_adapter",
        "status": "blocked_pending_exact_selected_guide_chain",
        "provider": TRANSFER_PROVIDER,
        "endpoint": TRANSFER_ENDPOINT,
        "method": "POST",
        "target_voice_id": TRANSFER_TARGET_VOICE_ID,
        "model_id": TRANSFER_MODEL,
        "seed": TRANSFER_SEED,
        "query_policy": {
            "enable_logging": "false_for_zrm_otherwise_true_only_with_account_training_opt_out",
            "output_format": TRANSFER_PRIMARY_FORMAT,
        },
        "multipart_fields": {
            "audio": "__EXACT_SELECTED_ORIGINAL_PROVIDER_WAV_PENDING__",
            "file_format": "other",
            "model_id": TRANSFER_MODEL,
            "remove_background_noise": False,
            "seed": TRANSFER_SEED,
            "voice_settings": TRANSFER_VOICE_SETTINGS,
        },
        "source_guide": {
            "path": None,
            "sha256": None,
            "byte_count": None,
            "duration_seconds": None,
            "required_container": "wav",
            "required_codec": "pcm_s16le",
            "required_sample_rate_hz": GUIDE_SAMPLE_RATE_HZ,
            "required_channels": 1,
            "must_be_original_provider_bytes": True,
        },
        "conditional_fallback": {
            "output_format": TRANSFER_FALLBACK_FORMAT,
            "enabled": False,
            "requires": "documented_unambiguous_pcm_capability_rejection_before_any_audio_is_accepted",
            "forbidden_for_timeout_disconnect_dns_tls_authentication_408_429_5xx_malformed_or_ambiguous_outcome": True,
            "comparison_eligible": False,
        },
        "blockers": [
            "exact selected original-provider guide absent",
            "guide lexical technical and performance QA absent",
            "owner guide selection absent",
            "ElevenLabs no-training or ZRM evidence absent",
            "cross-provider guide disclosure and target-voice rights absent",
            "separate active AUTH-V1 absent",
        ],
        "request_compiled": False,
        "network_authorized": False,
        "network_called": False,
        "audio_generated": False,
    }
    if not _json_exact(eleven, expected_eleven):
        raise ValidationError("ElevenLabs Voice Changer adapter semantics drifted")
    return {
        "google": {
            "path": str(google_path),
            "sha256": google_binding["sha256"],
        },
        "elevenlabs_voice_changer": {
            "path": str(eleven_path),
            "sha256": eleven_binding["sha256"],
        },
    }


def validate_performance_transfer_plan(plan_path: Path, canonical_w_path: Path) -> dict[str, Any]:
    """Validate and compile the frozen, credential-free two-stage plan."""

    plan_path = Path(plan_path).absolute()
    canonical_w_path = Path(canonical_w_path).absolute()
    root = _document_root(plan_path)
    plan = read_json(plan_path)
    _strict_object(
        plan,
        {
            "schema_version", "plan_id", "status", "target", "canonical_w",
            "microtest", "performance_envelope", "provider_adapters", "guide", "voice_transfer", "authority",
        },
        {
            "schema_version", "plan_id", "status", "target", "canonical_w",
            "microtest", "performance_envelope", "provider_adapters", "guide", "voice_transfer", "authority",
        },
        "performance-transfer plan",
    )
    errors = _scan_for_secrets(plan, "plan")
    _require(plan.get("schema_version") == PLAN_SCHEMA, f"schema_version must be {PLAN_SCHEMA}", errors)
    _require(isinstance(plan.get("plan_id"), str) and bool(plan["plan_id"]), "plan_id is required", errors)
    _require(plan.get("status") == "dry_run_only", "plan.status must be dry_run_only", errors)
    target = _target(plan.get("target"))

    try:
        canonical = _canonical_w_binding(plan_path, plan.get("canonical_w"), canonical_w_path)
        same_file = True
    except ValidationError as exc:
        errors.extend(exc.errors if isinstance(exc, ValidationError) else ["cannot resolve canonical W"])
        canonical = {}
        same_file = False
    _require(same_file, "canonical_w.path does not bind the supplied canonical W", errors)
    tokens = read_canonical_w(canonical_w_path)
    actual_w_sha = sha256_file(canonical_w_path)
    _require(canonical.get("sha256") == actual_w_sha, "canonical_w.sha256 mismatch", errors)
    _require(canonical.get("token_count") == len(tokens), "canonical_w.token_count mismatch", errors)
    if len(tokens) < MICROTEST_END_TOKEN:
        errors.append("canonical W is too short for frozen P01 range")
        passage_tokens: list[str] = []
    else:
        passage_tokens = tokens[MICROTEST_START_TOKEN:MICROTEST_END_TOKEN]
    spoken_text = " ".join(passage_tokens)
    _require(spoken_text == MICROTEST_TEXT, "frozen P01 spoken text drifted", errors)
    if passage_tokens:
        _require(token_identity(passage_tokens)["sha256"] == MICROTEST_TOKEN_SLICE_SHA256, "frozen P01 token hash drifted", errors)
    _require(sha256_bytes(spoken_text.encode("utf-8")) == MICROTEST_TEXT_SHA256, "frozen P01 transport hash drifted", errors)

    micro = _strict_object(
        plan.get("microtest"),
        {"passage_id", "start_token", "end_token", "token_count", "token_slice_sha256", "spoken_text_sha256", "spoken_text_character_count"},
        {"passage_id", "start_token", "end_token", "token_count", "token_slice_sha256", "spoken_text_sha256", "spoken_text_character_count"},
        "microtest",
    )
    frozen_micro = {
        "passage_id": MICROTEST_PASSAGE_ID,
        "start_token": MICROTEST_START_TOKEN,
        "end_token": MICROTEST_END_TOKEN,
        "token_count": MICROTEST_TOKEN_COUNT,
        "token_slice_sha256": MICROTEST_TOKEN_SLICE_SHA256,
        "spoken_text_sha256": MICROTEST_TEXT_SHA256,
        "spoken_text_character_count": MICROTEST_TEXT_CHARACTER_COUNT,
    }
    _require(_json_exact(micro, frozen_micro), "microtest must equal the frozen P01 binding", errors)

    try:
        envelope_path, envelope_binding = _path_hash(root, plan.get("performance_envelope"), "performance_envelope", suffix=".json")
        _validate_performance_envelope(
            envelope_path,
            canonical_w_path,
            tokens,
            target,
        )
    except ValidationError as exc:
        errors.extend(exc.errors)
        envelope_path = root / "missing"
        envelope_binding = {}

    try:
        provider_adapters = _validate_provider_adapters(
            root,
            plan.get("provider_adapters"),
        )
    except ValidationError as exc:
        errors.extend(exc.errors)
        provider_adapters = {}

    guide = _strict_object(
        plan.get("guide"),
        {
            "provider", "endpoint", "method", "model_id", "voice_name", "language_code",
            "acting_prompt", "acting_prompt_sha256", "request_body_sha256", "request_body_bytes",
            "request_count", "identical_unseeded_requests", "input_limits", "format", "destinations",
        },
        {
            "provider", "endpoint", "method", "model_id", "voice_name", "language_code",
            "acting_prompt", "acting_prompt_sha256", "request_body_sha256", "request_body_bytes",
            "request_count", "identical_unseeded_requests", "input_limits", "format", "destinations",
        },
        "guide",
    )
    expected_guide_scalars = {
        "provider": GUIDE_PROVIDER, "endpoint": GUIDE_ENDPOINT, "method": "POST",
        "model_id": GUIDE_MODEL, "voice_name": GUIDE_VOICE, "language_code": GUIDE_LANGUAGE,
        "acting_prompt": GUIDE_ACTING_PROMPT, "acting_prompt_sha256": GUIDE_ACTING_PROMPT_SHA256,
        "request_body_sha256": GUIDE_REQUEST_BODY_SHA256, "request_body_bytes": GUIDE_MAX_REQUEST_BODY_BYTES,
        "request_count": GUIDE_REQUEST_COUNT, "identical_unseeded_requests": True,
    }
    for key, expected in expected_guide_scalars.items():
        _require(_json_exact(guide.get(key), expected), f"guide.{key} must equal the frozen value", errors)
    input_limits = _strict_object(
        guide.get("input_limits"), {"combined_utf8_bytes", "prompt_utf8_bytes", "text_utf8_bytes"}, {"combined_utf8_bytes", "prompt_utf8_bytes", "text_utf8_bytes"}, "guide.input_limits"
    )
    _require(_json_exact(input_limits, {"combined_utf8_bytes": 5000, "prompt_utf8_bytes": 4000, "text_utf8_bytes": 4000}), "guide.input_limits drifted", errors)
    guide_format = _strict_object(
        guide.get("format"), {"audio_encoding", "sample_rate_hz", "container", "channels"}, {"audio_encoding", "sample_rate_hz", "container", "channels"}, "guide.format"
    )
    _require(_json_exact(guide_format, {"audio_encoding": "LINEAR16", "sample_rate_hz": 24000, "container": "wav", "channels": 1}), "guide.format drifted", errors)
    destinations = guide.get("destinations")
    if destinations != list(GUIDE_DESTINATIONS):
        errors.append("guide.destinations must equal the frozen candidate-A/B paths")
        destinations = []
    else:
        for index, destination in enumerate(destinations):
            try:
                path = _safe_relative(root, destination, f"guide.destinations[{index}]", must_exist=False, suffix=".wav")
                _require(path.relative_to(root).parts[0] == "outputs", f"guide.destinations[{index}] must remain under outputs/", errors)
                _require(not path.is_symlink(), f"guide.destinations[{index}] may not be a symlink", errors)
            except (ValidationError, ValueError) as exc:
                errors.extend(exc.errors if isinstance(exc, ValidationError) else [f"guide.destinations[{index}] is unsafe"])

    transfer = _strict_object(
        plan.get("voice_transfer"),
        {
            "provider", "status", "endpoint", "method", "target_voice_id", "model_id", "seed",
            "query_policy", "voice_settings", "remove_background_noise", "file_format",
            "preferred_output_format", "conditional_fallback_output_format", "source_limits", "destination",
        },
        {
            "provider", "status", "endpoint", "method", "target_voice_id", "model_id", "seed",
            "query_policy", "voice_settings", "remove_background_noise", "file_format",
            "preferred_output_format", "conditional_fallback_output_format", "source_limits", "destination",
        },
        "voice_transfer",
    )
    expected_transfer = {
        "provider": TRANSFER_PROVIDER,
        "status": "blocked_pending_selected_guide",
        "endpoint": TRANSFER_ENDPOINT,
        "method": "POST",
        "target_voice_id": TRANSFER_TARGET_VOICE_ID,
        "model_id": TRANSFER_MODEL,
        "seed": TRANSFER_SEED,
        "query_policy": {
            "enable_logging": "false_for_zrm_otherwise_true_only_with_account_training_opt_out",
            "output_format": TRANSFER_PRIMARY_FORMAT,
        },
        "voice_settings": TRANSFER_VOICE_SETTINGS,
        "remove_background_noise": False,
        "file_format": "other",
        "preferred_output_format": TRANSFER_PRIMARY_FORMAT,
        "conditional_fallback_output_format": TRANSFER_FALLBACK_FORMAT,
        "source_limits": {"max_bytes": TRANSFER_MAX_SOURCE_BYTES, "max_duration_seconds": 300},
    }
    for key, expected in expected_transfer.items():
        _require(_json_exact(transfer.get(key), expected), f"voice_transfer.{key} must equal the frozen value", errors)
    try:
        transfer_destination = _safe_relative(root, transfer.get("destination"), "voice_transfer.destination", must_exist=False, suffix=".pcm")
        _require(transfer.get("destination") == TRANSFER_DESTINATION, "voice_transfer.destination must equal the frozen path", errors)
        _require(transfer_destination.relative_to(root).parts[0] == "outputs", "voice_transfer.destination must remain under outputs/", errors)
        _require(not transfer_destination.is_symlink(), "voice_transfer.destination may not be a symlink", errors)
    except (ValidationError, ValueError) as exc:
        errors.extend(exc.errors if isinstance(exc, ValidationError) else ["voice_transfer.destination is unsafe"])

    authority = _strict_object(
        plan.get("authority"),
        {
            "guide_authorization_required", "voice_transfer_authorization_required", "joint_authorization_forbidden",
            "guide_must_be_selected_and_pass_qa", "external_action_authorized", "credentials_may_be_accessed",
            "audio_may_be_generated", "full_capture_authorized", "step3_authorized", "publication_authorized",
        },
        {
            "guide_authorization_required", "voice_transfer_authorization_required", "joint_authorization_forbidden",
            "guide_must_be_selected_and_pass_qa", "external_action_authorized", "credentials_may_be_accessed",
            "audio_may_be_generated", "full_capture_authorized", "step3_authorized", "publication_authorized",
        },
        "authority",
    )
    expected_authority = {
        "guide_authorization_required": True,
        "voice_transfer_authorization_required": True,
        "joint_authorization_forbidden": True,
        "guide_must_be_selected_and_pass_qa": True,
        "external_action_authorized": False,
        "credentials_may_be_accessed": False,
        "audio_may_be_generated": False,
        "full_capture_authorized": False,
        "step3_authorized": False,
        "publication_authorized": False,
    }
    _require(_json_exact(authority, expected_authority), "authority must remain credential-free and non-authorizing", errors)
    if errors:
        raise ValidationError(errors)

    body, body_bytes = _validate_frozen_guide_body(spoken_text)
    compiled_requests = []
    for index, destination in enumerate(destinations, start=1):
        compiled_requests.append(
            {
                "request_id": f"gemini-guide-{index:02d}",
                "generation_index": index - 1,
                "provider": GUIDE_PROVIDER,
                "method": "POST",
                "endpoint": GUIDE_ENDPOINT,
                "required_header_names": ["Authorization", "Content-Type", "X-Goog-User-Project"],
                "request_body": body,
                "request_body_bytes": len(body_bytes),
                "request_body_sha256": sha256_bytes(body_bytes),
                "destination": destination,
            }
        )
    request_set_sha256 = sha256_bytes(_compact_json_bytes(compiled_requests))
    return {
        "schema_version": "oe-performance-transfer-dry-run-v1",
        "valid": True,
        "plan_sha256": sha256_file(plan_path),
        "target": target,
        "canonical_w_sha256": actual_w_sha,
        "performance_envelope": {"path": str(envelope_path), "sha256": envelope_binding["sha256"]},
        "provider_adapters": provider_adapters,
        "microtest": frozen_micro,
        "guide": {
            "requests": compiled_requests,
            "request_set_sha256": request_set_sha256,
            "maximum": {
                "calls": GUIDE_MAX_CALLS,
                "outputs": GUIDE_MAX_OUTPUTS,
                "output_duration_seconds": GUIDE_MAX_OUTPUT_DURATION_SECONDS,
                "output_wav_bytes": GUIDE_MAX_OUTPUT_WAV_BYTES,
                "total_audio_bytes": GUIDE_MAX_TOTAL_AUDIO_BYTES,
                "response_bytes_per_call": GUIDE_MAX_RESPONSE_BYTES_PER_CALL,
                "total_request_bytes": GUIDE_MAX_TOTAL_REQUEST_BYTES,
                "modeled_spend_usd": GUIDE_MAX_SPEND_USD,
            },
            "fallback": None,
            "stochastic_unseeded": True,
        },
        "voice_transfer": {
            "status": "blocked_pending_exact_selected_guide_chain",
            "blockers": [
                "one generated guide has not been selected by the owner",
                "the exact selected guide has not passed lexical, technical, and performance QA",
                "ElevenLabs no-training/account handling has not been verified for the exact upload",
                "a separate exact voice-transfer authorization does not exist",
            ],
            "request_compiled": False,
            "network_authorized": False,
        },
        "network_called": False,
        "credentials_accessed": False,
        "audio_files_created": 0,
        "creative_approved": False,
        "full_capture_authorized": False,
        "step3_authorized": False,
        "publication_authorized": False,
    }


def dry_run_synthetic_guide(plan_path: Path, canonical_w_path: Path) -> dict[str, Any]:
    """Compile the two frozen guide requests without validating execution authority."""

    result = validate_performance_transfer_plan(plan_path, canonical_w_path)
    return {
        "schema_version": "oe-synthetic-guide-dry-run-v1",
        "valid": True,
        "plan_sha256": result["plan_sha256"],
        "canonical_w_sha256": result["canonical_w_sha256"],
        "microtest": result["microtest"],
        "requests": result["guide"]["requests"],
        "request_set_sha256": result["guide"]["request_set_sha256"],
        "maximum": result["guide"]["maximum"],
        "fallback": None,
        "provider_action_authorized": False,
        "network_authorized": False,
        "execution_transport_available": False,
        "network_called": False,
        "credentials_accessed": False,
        "audio_files_created": 0,
    }


def _guide_runtime_files() -> dict[str, tuple[str, Path]]:
    module = Path(__file__).absolute()
    narration_root = module.resolve().parents[2]
    return {
        "executor": (GUIDE_RUNTIME_RELATIVE, module),
        "cli": (GUIDE_CLI_RELATIVE, module.with_name("cli.py")),
        "core": (GUIDE_CORE_RELATIVE, module.with_name("core.py")),
        "init": (GUIDE_INIT_RELATIVE, module.with_name("__init__.py")),
        "schema": (
            GUIDE_SCHEMA_RELATIVE,
            narration_root / "schemas" / "synthetic-guide-authorization.schema.json",
        ),
        "tests": (
            GUIDE_TESTS_RELATIVE,
            narration_root / "runtime" / "tests" / "test_performance_transfer.py",
        ),
    }


def _expected_guide_runtime_bindings(*, draft: bool) -> dict[str, str]:
    pending = "pending"
    result = {"git_commit": pending}
    for name, (relative, path) in _guide_runtime_files().items():
        result[f"{name}_path"] = relative
        result[f"{name}_sha256"] = pending if draft else sha256_file(path)
    return result


def _validate_guide_runtime_bindings(
    value: Any,
    *,
    status: str,
    errors: list[str],
) -> dict[str, Any]:
    expected_keys = set(_expected_guide_runtime_bindings(draft=True))
    bindings = _strict_object(
        value,
        expected_keys,
        expected_keys,
        "runtime_bindings",
    )
    expected_paths = _expected_guide_runtime_bindings(draft=True)
    for key, expected in expected_paths.items():
        if key.endswith("_path"):
            _require(bindings.get(key) == expected, f"runtime_bindings.{key} drifted", errors)
    if status == "draft":
        _require(
            _json_exact(bindings, expected_paths),
            "draft recovery runtime bindings must be pending and path-exact",
            errors,
        )
        return bindings
    _require(
        isinstance(bindings.get("git_commit"), str)
        and bool(_GIT_SHA_RE.fullmatch(bindings["git_commit"])),
        "active recovery runtime_bindings.git_commit must be exact",
        errors,
    )
    for name, (_relative, path) in _guide_runtime_files().items():
        key = f"{name}_sha256"
        value_sha = bindings.get(key)
        _require(
            isinstance(value_sha, str)
            and bool(_SHA_RE.fullmatch(value_sha))
            and value_sha == sha256_file(path),
            f"active recovery runtime_bindings.{key} does not match loaded bytes",
            errors,
        )
    return bindings


def _validate_common_authorization(
    authorization: dict[str, Any],
    *,
    authorization_path: Path,
    schema: str,
    scope: str,
    target: dict[str, Any],
) -> tuple[str, list[str]]:
    errors = _scan_for_secrets(authorization, "authorization")
    _require(authorization.get("schema_version") == schema, f"schema_version must be {schema}", errors)
    auth_id = authorization.get("authorization_id")
    _require(isinstance(auth_id, str) and bool(_ID_RE.fullmatch(auth_id)), "authorization_id is invalid", errors)
    _require(authorization.get("scope") == scope, f"scope must be {scope}", errors)
    try:
        _require(_target(authorization.get("target")) == target, "authorization target does not match plan", errors)
    except ValidationError as exc:
        errors.extend(exc.errors)
    status = authorization.get("status")
    _require(status in {"draft", "active"}, "status must be draft or active", errors)
    approved = authorization.get("approved")
    execution_ready = authorization.get("execution_ready")
    blockers = authorization.get("blockers")
    _require(isinstance(blockers, list) and all(isinstance(item, str) and item for item in blockers), "blockers must be an array of non-empty strings", errors)
    consumption = authorization.get("consumption")
    if not isinstance(consumption, dict):
        errors.append("consumption must be an object")
    else:
        _strict_object(consumption, {"status", "calls_used", "outputs_received", "spend_used_usd", "record_path"}, {"status", "calls_used", "outputs_received", "spend_used_usd", "record_path"}, "consumption")
        _require(type(consumption.get("calls_used")) is int and consumption["calls_used"] == 0, "consumption.calls_used must be integer zero", errors)
        _require(type(consumption.get("outputs_received")) is int and consumption["outputs_received"] == 0, "consumption.outputs_received must be integer zero", errors)
        _require(type(consumption.get("spend_used_usd")) in {int, float} and consumption["spend_used_usd"] == 0, "consumption.spend_used_usd must be numeric zero", errors)
        _require(isinstance(consumption.get("record_path"), str) and bool(consumption["record_path"]), "consumption.record_path is required", errors)
        if isinstance(consumption.get("record_path"), str) and consumption["record_path"]:
            try:
                fixture_root = _document_root(authorization_path)
                consumption_path = _safe_relative(
                    fixture_root,
                    consumption["record_path"],
                    "consumption.record_path",
                    must_exist=False,
                    suffix=".json",
                )
                relative = consumption_path.relative_to(fixture_root)
                _require(
                    len(relative.parts) == 3
                    and relative.parts[:2] == ("authorizations", "consumed"),
                    "consumption.record_path must be authorizations/consumed/*.json",
                    errors,
                )
                _require(
                    not consumption_path.exists(),
                    "unconsumed authorization may not have an existing consumption record",
                    errors,
                )
                if status == "active" and isinstance(auth_id, str):
                    _require(
                        relative.name == f"{auth_id}.consumed.json",
                        "active consumption record filename must match authorization_id",
                        errors,
                    )
            except (ValidationError, ValueError) as exc:
                errors.extend(
                    exc.errors
                    if isinstance(exc, ValidationError)
                    else ["consumption.record_path is unsafe"]
                )
    if status == "draft":
        _require(approved is False, "draft authorization must not be approved", errors)
        _require(execution_ready is False, "draft authorization must not be execution-ready", errors)
        _require(isinstance(blockers, list) and len(blockers) > 0, "draft authorization requires blockers", errors)
        if isinstance(consumption, dict):
            _require(consumption.get("status") == "not_authorized", "draft consumption must be not_authorized", errors)
    elif status == "active":
        _require(approved is True, "active authorization must be approved", errors)
        _require(execution_ready is True, "active authorization must be execution-ready", errors)
        _require(blockers == [], "active authorization must have no blockers", errors)
        if isinstance(consumption, dict):
            _require(consumption.get("status") == "unconsumed", "active consumption must be unconsumed", errors)
        approved_at = _parse_time(authorization.get("approved_at"), "approved_at", errors)
        expires_at = _parse_time(authorization.get("expires_at"), "expires_at", errors)
        now = datetime.now(timezone.utc)
        if approved_at and expires_at:
            _require(approved_at <= now < expires_at, "active authorization is not within its validity window", errors)
            _require((expires_at - approved_at).total_seconds() <= 86_400, "authorization window may not exceed 24 hours", errors)
        _require(isinstance(authorization.get("approved_by"), str) and bool(authorization["approved_by"]), "approved_by is required for active authorization", errors)
    if errors:
        raise ValidationError(errors)
    return str(status), []


def _recovery_record(
    root: Path,
    relative: str,
    expected_sha256: str,
    label: str,
    *,
    directory_prefix: tuple[str, ...],
    required_mode: int | None = None,
) -> tuple[Path, dict[str, Any]]:
    path = _safe_relative(root, relative, f"{label}.path", must_exist=True, suffix=".json")
    if path.relative_to(root).parts[: len(directory_prefix)] != directory_prefix:
        raise ValidationError(f"{label} is outside its exact directory")
    value, _raw, actual_sha256 = _read_bound_fixture_json(
        root,
        path,
        label,
        required_mode=required_mode,
    )
    if actual_sha256 != expected_sha256:
        raise ValidationError(f"{label} SHA-256 mismatch")
    return path, value


def _validate_prior_guide_failure(
    root: Path,
    item: dict[str, Any],
    *,
    dry: dict[str, Any],
    target: dict[str, Any],
) -> tuple[datetime, str]:
    _path, receipt = _recovery_record(
        root,
        item["failure_receipt_path"],
        item["failure_receipt_sha256"],
        f"{item['attempt_id']} failure receipt",
        directory_prefix=("receipts", "google"),
        required_mode=0o600,
    )
    receipt_keys = {
        "schema_version", "provider", "endpoint", "model_id", "voice_name",
        "language_code", "outcome", "reason_code", "failed_request_id", "http_status",
        "authorization_id", "authorization_consumed", "guide_authorization_path",
        "guide_authorization_sha256", "guide_consumption_record_path",
        "guide_consumption_record_sha256", "performance_transfer_plan_sha256",
        "canonical_w_sha256", "microtest_token_slice_sha256", "spoken_text_sha256",
        "acting_prompt_sha256", "request_set_sha256", "request_body_sha256",
        "request_body_bytes", "total_request_bytes", "provider_calls_made",
        "provider_outputs_received", "provider_response_bytes_total",
        "failed_response_bytes", "provider_spend_usd", "provider_spend_semantics",
        "credential_mechanism", "credential_refresh_attempted", "quota_project_sha256",
        "provider_identifiers", "provider_usage", "outputs", "started_at", "failed_at",
        "retries_made", "redirects_followed", "fallbacks_used", "credentials_recorded",
        "network_called", "creative_approved", "cross_provider_transfer_authorized",
        "voice_transfer_authorized", "full_capture_authorized", "step3_authorized",
        "publication_authorized",
    }
    _strict_object(receipt, receipt_keys, receipt_keys, f"{item['attempt_id']} failure receipt")
    errors: list[str] = []
    expected_identity = {
        "schema_version": GUIDE_FAILURE_RECEIPT_SCHEMA,
        "provider": GUIDE_PROVIDER,
        "endpoint": GUIDE_ENDPOINT,
        "model_id": GUIDE_MODEL,
        "voice_name": GUIDE_VOICE,
        "language_code": GUIDE_LANGUAGE,
        "outcome": "failed_closed",
        "reason_code": "provider_http_failure",
        "failed_request_id": "gemini-guide-01",
        "http_status": 403,
        "authorization_consumed": True,
        "performance_transfer_plan_sha256": dry["plan_sha256"],
        "canonical_w_sha256": dry["canonical_w_sha256"],
        "microtest_token_slice_sha256": MICROTEST_TOKEN_SLICE_SHA256,
        "spoken_text_sha256": MICROTEST_TEXT_SHA256,
        "acting_prompt_sha256": GUIDE_ACTING_PROMPT_SHA256,
        "request_set_sha256": GUIDE_REQUEST_SET_SHA256,
        "request_body_sha256": GUIDE_REQUEST_BODY_SHA256,
        "request_body_bytes": GUIDE_MAX_REQUEST_BODY_BYTES,
        "total_request_bytes": GUIDE_MAX_REQUEST_BODY_BYTES,
        "provider_calls_made": 1,
        "provider_outputs_received": 0,
        "provider_response_bytes_total": 0,
        "failed_response_bytes": 0,
        "provider_spend_usd": GUIDE_MODELED_SPEND_PER_CALL_USD,
        "provider_spend_semantics": "modeled_authorized_ceiling_per_attempt_not_provider_invoice",
        "credential_mechanism": "gcloud_application_default_print_access_token",
        "credential_refresh_attempted": True,
        "provider_identifiers": {},
        "provider_usage": {},
        "outputs": [],
        "retries_made": 0,
        "redirects_followed": 0,
        "fallbacks_used": 0,
        "credentials_recorded": False,
        "network_called": True,
        "creative_approved": False,
        "cross_provider_transfer_authorized": False,
        "voice_transfer_authorized": False,
        "full_capture_authorized": False,
        "step3_authorized": False,
        "publication_authorized": False,
    }
    for key, expected in expected_identity.items():
        _require(
            _json_exact(receipt.get(key), expected),
            f"{item['attempt_id']} failure {key} drifted",
            errors,
        )
    _require(
        isinstance(receipt.get("quota_project_sha256"), str)
        and bool(_SHA_RE.fullmatch(receipt["quota_project_sha256"])),
        f"{item['attempt_id']} failure quota-project binding is invalid",
        errors,
    )
    auth_id = receipt.get("authorization_id")
    _require(
        isinstance(auth_id, str) and bool(_ID_RE.fullmatch(auth_id)),
        f"{item['attempt_id']} failure authorization ID is invalid",
        errors,
    )
    started = _parse_time(receipt.get("started_at"), f"{item['attempt_id']} started_at", errors)
    failed = _parse_time(receipt.get("failed_at"), f"{item['attempt_id']} failed_at", errors)
    if started is not None and failed is not None:
        _require(started <= failed <= datetime.now(timezone.utc), f"{item['attempt_id']} failure time order drifted", errors)
    if errors:
        raise ValidationError(errors)

    auth_path, prior_auth = _recovery_record(
        root,
        receipt["guide_authorization_path"],
        receipt["guide_authorization_sha256"],
        f"{item['attempt_id']} authorization",
        directory_prefix=("authorizations",),
    )
    if auth_path.relative_to(root).parts[:2] == ("authorizations", "consumed"):
        raise ValidationError(f"{item['attempt_id']} authorization path is invalid")
    _strict_object(
        prior_auth,
        {
            "schema_version", "authorization_id", "status", "approved", "scope", "target",
            "bindings", "action", "billing_project_binding", "authorized_limits", "consumption",
            "approved_by", "approved_at", "expires_at", "execution_ready", "blockers",
        },
        {
            "schema_version", "authorization_id", "status", "approved", "scope", "target",
            "bindings", "action", "billing_project_binding", "authorized_limits", "consumption",
            "approved_by", "approved_at", "expires_at", "execution_ready", "blockers",
        },
        f"{item['attempt_id']} authorization",
    )
    prior_errors: list[str] = []
    _require(prior_auth.get("schema_version") == GUIDE_AUTH_SCHEMA, f"{item['attempt_id']} authorization schema drifted", prior_errors)
    _require(prior_auth.get("authorization_id") == auth_id, f"{item['attempt_id']} authorization ID drifted", prior_errors)
    _require(prior_auth.get("status") == "active" and prior_auth.get("approved") is True and prior_auth.get("execution_ready") is True, f"{item['attempt_id']} authorization was not active", prior_errors)
    _require(prior_auth.get("scope") == GUIDE_SCOPE and _json_exact(prior_auth.get("target"), target), f"{item['attempt_id']} target drifted", prior_errors)
    _require(prior_auth.get("bindings", {}).get("performance_transfer_plan_sha256") == dry["plan_sha256"] and prior_auth.get("bindings", {}).get("request_set_sha256") == GUIDE_REQUEST_SET_SHA256, f"{item['attempt_id']} request binding drifted", prior_errors)
    _require(prior_auth.get("consumption", {}).get("record_path") == receipt["guide_consumption_record_path"], f"{item['attempt_id']} consumption path drifted", prior_errors)
    _require(prior_auth.get("billing_project_binding", {}).get("quota_project_sha256") == receipt["quota_project_sha256"], f"{item['attempt_id']} quota-project hash drifted", prior_errors)
    if prior_errors:
        raise ValidationError(prior_errors)

    _consumption_path, consumption = _recovery_record(
        root,
        receipt["guide_consumption_record_path"],
        receipt["guide_consumption_record_sha256"],
        f"{item['attempt_id']} consumption",
        directory_prefix=("authorizations", "consumed"),
        required_mode=0o600,
    )
    consumption_keys = {
        "schema_version", "authorization_id", "authorization_sha256", "scope", "provider",
        "status", "consumed_at", "consumed_before_network", "network_called_at_consumption",
        "performance_transfer_plan_sha256", "request_set_sha256", "reserved_limits",
        "credentials_recorded",
    }
    _strict_object(consumption, consumption_keys, consumption_keys, f"{item['attempt_id']} consumption")
    consumed_errors: list[str] = []
    _require(consumption.get("schema_version") == GUIDE_CONSUMPTION_SCHEMA, f"{item['attempt_id']} consumption schema drifted", consumed_errors)
    _require(consumption.get("authorization_id") == auth_id and consumption.get("authorization_sha256") == receipt["guide_authorization_sha256"], f"{item['attempt_id']} consumption authorization drifted", consumed_errors)
    _require(consumption.get("scope") == GUIDE_SCOPE and consumption.get("provider") == GUIDE_PROVIDER and consumption.get("status") == "consumed_before_network", f"{item['attempt_id']} consumption identity drifted", consumed_errors)
    _require(consumption.get("consumed_before_network") is True and consumption.get("network_called_at_consumption") is False and consumption.get("credentials_recorded") is False, f"{item['attempt_id']} consumption boundary drifted", consumed_errors)
    _require(consumption.get("performance_transfer_plan_sha256") == dry["plan_sha256"] and consumption.get("request_set_sha256") == GUIDE_REQUEST_SET_SHA256, f"{item['attempt_id']} consumption request binding drifted", consumed_errors)
    consumed = _parse_time(consumption.get("consumed_at"), f"{item['attempt_id']} consumed_at", consumed_errors)
    if consumed is not None and started is not None:
        _require(consumed <= started, f"{item['attempt_id']} consumed-after-start drifted", consumed_errors)
    if consumed_errors:
        raise ValidationError(consumed_errors)
    assert failed is not None
    return failed, receipt["quota_project_sha256"]


def _validate_guide_recovery_binding(
    root: Path,
    value: Any,
    *,
    dry: dict[str, Any],
    target: dict[str, Any],
) -> dict[str, Any]:
    if not _json_exact(value, GUIDE_RECOVERY_BINDING):
        raise ValidationError("guide recovery_binding drifted")
    binding = value
    prior_results = [
        _validate_prior_guide_failure(root, item, dry=dry, target=target)
        for item in binding["prior_failures"]
    ]
    if not prior_results[0][0] < prior_results[1][0]:
        raise ValidationError("G1 and G1R1 failure chronology drifted")
    quota_hashes = {result[1] for result in prior_results}
    if len(quota_hashes) != 1:
        raise ValidationError("prior guide attempts used different quota-project bindings")

    _diagnosis_path, diagnosis = _recovery_record(
        root,
        binding["diagnosis"]["path"],
        binding["diagnosis"]["sha256"],
        "G1R2 diagnosis",
        directory_prefix=("evidence",),
    )
    diagnosis_keys = {
        "schema_version", "record_id", "status", "recorded_at", "evidence_boundary",
        "prior_attempt_bindings", "live_readback", "diagnosis", "authority",
    }
    _strict_object(diagnosis, diagnosis_keys, diagnosis_keys, "G1R2 diagnosis")
    errors: list[str] = []
    _require(diagnosis.get("schema_version") == "oe-google-g1-403-diagnosis-v1" and diagnosis.get("status") == "operator_reported_live_readback", "G1R2 diagnosis identity drifted", errors)
    prior = diagnosis.get("prior_attempt_bindings")
    _require(
        isinstance(prior, dict)
        and prior.get("canonical_request_body_sha256") == GUIDE_REQUEST_BODY_SHA256
        and prior.get("canonical_two_request_set_sha256") == GUIDE_REQUEST_SET_SHA256
        and prior.get("g1", {}).get("failure_receipt_sha256") == binding["prior_failures"][0]["failure_receipt_sha256"]
        and prior.get("g1r1", {}).get("failure_receipt_sha256") == binding["prior_failures"][1]["failure_receipt_sha256"],
        "G1R2 diagnosis prior-attempt binding drifted",
        errors,
    )
    conclusion = diagnosis.get("diagnosis")
    _require(
        isinstance(conclusion, dict)
        and conclusion.get("current_cause") == "unknown"
        and conclusion.get("blind_retry_permitted") is False
        and conclusion.get("aiplatform_service_disablement_is_proven_403_cause") is False,
        "G1R2 diagnosis causal boundary drifted",
        errors,
    )
    live = diagnosis.get("live_readback")
    _require(
        isinstance(live, dict)
        and live.get("services", {}).get("aiplatform.googleapis.com") == "DISABLED"
        and live.get("project", {}).get("project_sha256") in quota_hashes,
        "G1R2 diagnosis project or service state drifted",
        errors,
    )
    authority = diagnosis.get("authority")
    _require(isinstance(authority, dict) and all(item is False for item in authority.values()), "G1R2 diagnosis carries authority", errors)
    diagnosed_at = _parse_time(diagnosis.get("recorded_at"), "G1R2 diagnosis recorded_at", errors)
    if diagnosed_at is not None:
        _require(prior_results[-1][0] <= diagnosed_at <= datetime.now(timezone.utc), "G1R2 diagnosis chronology drifted", errors)
    if errors:
        raise ValidationError(errors)

    service = binding["service_enablement"]
    _service_auth_path, service_auth = _recovery_record(
        root,
        service["authorization_path"],
        service["authorization_sha256"],
        "service-enablement authorization",
        directory_prefix=("authorizations",),
    )
    _service_consumption_path, service_consumption = _recovery_record(
        root,
        service["consumption_record_path"],
        service["consumption_record_sha256"],
        "service-enablement consumption",
        directory_prefix=("authorizations", "consumed"),
        required_mode=0o600,
    )
    _service_run_path, service_run = _recovery_record(
        root,
        service["run_receipt_path"],
        service["run_receipt_sha256"],
        "service-enablement run receipt",
        directory_prefix=("receipts", "google-service-usage"),
        required_mode=0o600,
    )
    _service_disposition_path, service_disposition = _recovery_record(
        root,
        service["success_disposition_path"],
        service["success_disposition_sha256"],
        "service-success disposition",
        directory_prefix=("evidence",),
    )
    service_errors: list[str] = []
    _require(service_auth.get("schema_version") == "oe-google-service-enablement-authorization-v2" and service_auth.get("status") == "active" and service_auth.get("approved") is True, "service-enablement authorization drifted", service_errors)
    _require(service_auth.get("target", {}).get("service") == service["service"] and service_auth.get("target", {}).get("project_sha256") in quota_hashes, "service-enablement target drifted", service_errors)
    _require(service_auth.get("runtime_bindings", {}).get("credential_runtime_sha256") == GUIDE_SAFE_ERROR_CAPTURE_RUNTIME_SHA256, "safe-error capture runtime binding drifted", service_errors)
    _require(service_consumption.get("schema_version") == "oe-google-service-enablement-consumption-v2" and service_consumption.get("authorization_id") == service_auth.get("authorization_id") and service_consumption.get("authorization_sha256") == service["authorization_sha256"], "service-enablement consumption authorization drifted", service_errors)
    _require(service_consumption.get("status") == "consumed_before_network" and service_consumption.get("consumed_before_network") is True and service_consumption.get("network_called_at_consumption") is False and service_consumption.get("credentials_recorded") is False, "service-enablement consumption boundary drifted", service_errors)
    _require(service_run.get("schema_version") == "oe-google-service-enablement-run-receipt-v2" and service_run.get("outcome") == "success", "service-enablement run identity drifted", service_errors)
    _require(service_run.get("authorization_id") == service_auth.get("authorization_id") and service_run.get("authorization_sha256") == service["authorization_sha256"] and service_run.get("consumption_record_path") == service["consumption_record_path"] and service_run.get("consumption_record_sha256") == service["consumption_record_sha256"], "service-enablement run provenance drifted", service_errors)
    _require(service_run.get("diagnosis_path") == binding["diagnosis"]["path"] and service_run.get("diagnosis_sha256") == binding["diagnosis"]["sha256"], "service-enablement diagnosis binding drifted", service_errors)
    _require(service_run.get("service") == service["service"] and service_run.get("service_state_resolution") == "enabled_confirmed" and service_run.get("post_enable_readback", {}).get("state") == service["final_state"], "service-enablement final state drifted", service_errors)
    _require(_json_exact(service_run.get("calls"), {"pre_enable_state_readbacks": 1, "enable_attempts": 1, "operation_polls": 1, "post_enable_state_readbacks": 1, "http_calls_total": 4}), "service-enablement call counts drifted", service_errors)
    _require(service_run.get("mutation_attempted") is True and service_run.get("enablement_may_have_completed") is True and service_run.get("operation_may_still_be_running") is False and service_run.get("manual_readback_required") is False, "service-enablement resolution drifted", service_errors)
    _require(_json_exact(service_run.get("retries_made"), 0) and _json_exact(service_run.get("redirects_followed"), 0) and service_run.get("credentials_recorded") is False and service_run.get("raw_provider_responses_recorded") is False, "service-enablement containment drifted", service_errors)
    _require(service_run.get("runtime_bindings", {}).get("credential_runtime_sha256") == GUIDE_SAFE_ERROR_CAPTURE_RUNTIME_SHA256, "service run safe-error runtime drifted", service_errors)
    for key in (
        "service_disablement_authorized", "other_service_mutation_authorized",
        "iam_mutation_authorized", "billing_mutation_authorized",
        "project_hierarchy_mutation_authorized", "synthetic_guide_generation_authorized",
        "retry_authorized", "voice_transfer_authorized", "full_capture_authorized",
        "step3_authorized", "sharing_authorized", "publication_authorized",
    ):
        _require(service_run.get(key) is False, f"service-enablement run {key} drifted", service_errors)
    service_consumed_at = _parse_time(service_consumption.get("consumed_at"), "service consumed_at", service_errors)
    service_started_at = _parse_time(service_run.get("started_at"), "service started_at", service_errors)
    service_completed_at = _parse_time(service_run.get("completed_at"), "service completed_at", service_errors)
    if all(item is not None for item in (diagnosed_at, service_consumed_at, service_started_at, service_completed_at)):
        assert diagnosed_at is not None and service_consumed_at is not None and service_started_at is not None and service_completed_at is not None
        _require(diagnosed_at <= service_consumed_at <= service_started_at <= service_completed_at <= datetime.now(timezone.utc), "service-enablement chronology drifted", service_errors)

    disposition_keys = {
        "schema_version", "record_id", "status", "recorded_at",
        "service_transaction_binding", "service_outcome", "mutation_boundary",
        "synthetic_guide_readiness", "authority",
    }
    _strict_object(
        service_disposition,
        disposition_keys,
        disposition_keys,
        "service-success disposition",
    )
    _require(
        service_disposition.get("schema_version")
        == "oe-google-service-success-and-synthetic-guide-readiness-v1"
        and service_disposition.get("status")
        == "immutable_local_disposition_and_zero_authority_readiness",
        "service-success disposition identity drifted",
        service_errors,
    )
    transaction_binding = _strict_object(
        service_disposition.get("service_transaction_binding"),
        {
            "authorization_path", "authorization_sha256", "authorization_commit",
            "runtime_commit", "consumption_record_path", "consumption_record_sha256",
            "run_receipt_path", "run_receipt_sha256",
        },
        {
            "authorization_path", "authorization_sha256", "authorization_commit",
            "runtime_commit", "consumption_record_path", "consumption_record_sha256",
            "run_receipt_path", "run_receipt_sha256",
        },
        "service-success disposition transaction binding",
    )
    _require(
        _json_exact(
            {
                "authorization_path": transaction_binding.get("authorization_path"),
                "authorization_sha256": transaction_binding.get("authorization_sha256"),
                "consumption_record_path": transaction_binding.get("consumption_record_path"),
                "consumption_record_sha256": transaction_binding.get("consumption_record_sha256"),
                "run_receipt_path": transaction_binding.get("run_receipt_path"),
                "run_receipt_sha256": transaction_binding.get("run_receipt_sha256"),
            },
            {
                "authorization_path": service["authorization_path"],
                "authorization_sha256": service["authorization_sha256"],
                "consumption_record_path": service["consumption_record_path"],
                "consumption_record_sha256": service["consumption_record_sha256"],
                "run_receipt_path": service["run_receipt_path"],
                "run_receipt_sha256": service["run_receipt_sha256"],
            },
        )
        and isinstance(transaction_binding.get("authorization_commit"), str)
        and bool(_GIT_SHA_RE.fullmatch(transaction_binding["authorization_commit"]))
        and isinstance(transaction_binding.get("runtime_commit"), str)
        and bool(_GIT_SHA_RE.fullmatch(transaction_binding["runtime_commit"])),
        "service-success disposition transaction binding drifted",
        service_errors,
    )
    disposition_outcome = _strict_object(
        service_disposition.get("service_outcome"),
        {
            "outcome", "authorization_consumed", "calls", "pre_enable_readback",
            "enable_operation", "operation_completion", "post_enable_readback",
            "provider_response_bytes_total", "mutation_attempted",
            "service_state_resolution", "enablement_may_have_completed",
            "operation_may_still_be_running", "manual_readback_required",
            "retries_made", "redirects_followed", "raw_provider_responses_stored",
        },
        {
            "outcome", "authorization_consumed", "calls", "pre_enable_readback",
            "enable_operation", "operation_completion", "post_enable_readback",
            "provider_response_bytes_total", "mutation_attempted",
            "service_state_resolution", "enablement_may_have_completed",
            "operation_may_still_be_running", "manual_readback_required",
            "retries_made", "redirects_followed", "raw_provider_responses_stored",
        },
        "service-success disposition outcome",
    )
    _require(
        disposition_outcome.get("outcome") == "success"
        and disposition_outcome.get("authorization_consumed") is True
        and _json_exact(disposition_outcome.get("calls"), service_run.get("calls"))
        and disposition_outcome.get("post_enable_readback", {}).get("state")
        == service["final_state"]
        and disposition_outcome.get("mutation_attempted") is True
        and disposition_outcome.get("service_state_resolution") == "enabled_confirmed"
        and disposition_outcome.get("enablement_may_have_completed") is True
        and disposition_outcome.get("operation_may_still_be_running") is False
        and disposition_outcome.get("manual_readback_required") is False
        and _json_exact(disposition_outcome.get("retries_made"), 0)
        and _json_exact(disposition_outcome.get("redirects_followed"), 0)
        and disposition_outcome.get("raw_provider_responses_stored") is False,
        "service-success disposition outcome drifted",
        service_errors,
    )
    mutation_boundary = _strict_object(
        service_disposition.get("mutation_boundary"),
        {
            "exact_service_enabled", "other_service_mutation_requested",
            "service_disablement_requested", "direct_iam_api_call_or_mutation_by_executor",
            "provider_managed_service_agent_or_role_side_effects_observed",
            "billing_mutation_requested", "project_hierarchy_mutation_requested",
            "synthetic_guide_call_made",
        },
        {
            "exact_service_enabled", "other_service_mutation_requested",
            "service_disablement_requested", "direct_iam_api_call_or_mutation_by_executor",
            "provider_managed_service_agent_or_role_side_effects_observed",
            "billing_mutation_requested", "project_hierarchy_mutation_requested",
            "synthetic_guide_call_made",
        },
        "service-success disposition mutation boundary",
    )
    _require(
        mutation_boundary.get("exact_service_enabled") == service["service"]
        and mutation_boundary.get("provider_managed_service_agent_or_role_side_effects_observed")
        == "unknown"
        and all(
            mutation_boundary.get(key) is False
            for key in (
                "other_service_mutation_requested", "service_disablement_requested",
                "direct_iam_api_call_or_mutation_by_executor", "billing_mutation_requested",
                "project_hierarchy_mutation_requested", "synthetic_guide_call_made",
            )
        ),
        "service-success disposition mutation boundary drifted",
        service_errors,
    )
    guide_readiness = _strict_object(
        service_disposition.get("synthetic_guide_readiness"),
        {
            "execution_semantics", "service_prerequisite", "service_success_receipt_sha256",
            "performance_transfer_plan_path", "performance_transfer_plan_sha256",
            "compiled_synthetic_guide_path", "compiled_synthetic_guide_sha256",
            "canonical_w_sha256", "microtest_token_slice_sha256", "spoken_text_sha256",
            "acting_prompt_sha256", "request_body_sha256", "request_body_bytes",
            "request_set_sha256", "request_count", "maximum_modeled_spend_usd",
            "safe_error_runtime", "safe_error_tests", "cli",
            "machine_authorization_schema", "service_evidence_commit_required",
            "independent_service_evidence_audit_required",
            "fresh_active_synthetic_guide_authorization_required",
            "quota_project_hash_binding_required_at_activation",
        },
        {
            "execution_semantics", "service_prerequisite", "service_success_receipt_sha256",
            "performance_transfer_plan_path", "performance_transfer_plan_sha256",
            "compiled_synthetic_guide_path", "compiled_synthetic_guide_sha256",
            "canonical_w_sha256", "microtest_token_slice_sha256", "spoken_text_sha256",
            "acting_prompt_sha256", "request_body_sha256", "request_body_bytes",
            "request_set_sha256", "request_count", "maximum_modeled_spend_usd",
            "safe_error_runtime", "safe_error_tests", "cli",
            "machine_authorization_schema", "service_evidence_commit_required",
            "independent_service_evidence_audit_required",
            "fresh_active_synthetic_guide_authorization_required",
            "quota_project_hash_binding_required_at_activation",
        },
        "service-success disposition guide readiness",
    )
    _require(
        guide_readiness.get("execution_semantics")
        == "fresh_execution_of_original_two_candidate_plan_not_resumption_or_automatic_retry"
        and guide_readiness.get("service_prerequisite")
        == "aiplatform.googleapis.com_enabled_confirmed"
        and guide_readiness.get("service_success_receipt_sha256")
        == service["run_receipt_sha256"]
        and guide_readiness.get("performance_transfer_plan_path")
        == "performance-transfer-plan.json"
        and guide_readiness.get("performance_transfer_plan_sha256") == dry["plan_sha256"]
        and guide_readiness.get("canonical_w_sha256") == dry["canonical_w_sha256"]
        and guide_readiness.get("microtest_token_slice_sha256")
        == MICROTEST_TOKEN_SLICE_SHA256
        and guide_readiness.get("spoken_text_sha256") == MICROTEST_TEXT_SHA256
        and guide_readiness.get("acting_prompt_sha256") == GUIDE_ACTING_PROMPT_SHA256
        and guide_readiness.get("request_body_sha256") == GUIDE_REQUEST_BODY_SHA256
        and _json_exact(guide_readiness.get("request_body_bytes"), GUIDE_MAX_REQUEST_BODY_BYTES)
        and guide_readiness.get("request_set_sha256") == GUIDE_REQUEST_SET_SHA256
        and _json_exact(guide_readiness.get("request_count"), GUIDE_REQUEST_COUNT)
        and _json_exact(guide_readiness.get("maximum_modeled_spend_usd"), GUIDE_MAX_SPEND_USD)
        and _json_exact(
            guide_readiness.get("safe_error_runtime"),
            {
                "path": "runtime/oe_narration/performance_transfer.py",
                "sha256": GUIDE_SAFE_ERROR_CAPTURE_RUNTIME_SHA256,
            },
        )
        and guide_readiness.get("service_evidence_commit_required") is True
        and guide_readiness.get("independent_service_evidence_audit_required") is True
        and guide_readiness.get("fresh_active_synthetic_guide_authorization_required") is True
        and guide_readiness.get("quota_project_hash_binding_required_at_activation") is True,
        "service-success disposition guide readiness drifted",
        service_errors,
    )
    disposition_authority = _strict_object(
        service_disposition.get("authority"),
        {
            "credential_access_authorized", "network_access_authorized",
            "provider_action_authorized", "synthetic_guide_generation_authorized",
            "retry_authorized", "service_enablement_authorized",
            "service_disablement_authorized", "iam_mutation_authorized",
            "voice_transfer_authorized", "full_capture_authorized", "step3_authorized",
            "sharing_authorized", "publication_authorized",
        },
        {
            "credential_access_authorized", "network_access_authorized",
            "provider_action_authorized", "synthetic_guide_generation_authorized",
            "retry_authorized", "service_enablement_authorized",
            "service_disablement_authorized", "iam_mutation_authorized",
            "voice_transfer_authorized", "full_capture_authorized", "step3_authorized",
            "sharing_authorized", "publication_authorized",
        },
        "service-success disposition authority",
    )
    _require(
        all(item is False for item in disposition_authority.values()),
        "service-success disposition carries authority",
        service_errors,
    )
    disposition_recorded_at = _parse_time(
        service_disposition.get("recorded_at"),
        "service-success disposition recorded_at",
        service_errors,
    )
    if service_completed_at is not None and disposition_recorded_at is not None:
        _require(
            service_completed_at <= disposition_recorded_at <= datetime.now(timezone.utc),
            "service-success disposition chronology drifted",
            service_errors,
        )
    if service_errors:
        raise ValidationError(service_errors)
    return {
        "state": "verified",
        "recovery_id": binding["recovery_id"],
        "diagnosis_sha256": binding["diagnosis"]["sha256"],
        "service_run_receipt_sha256": service["run_receipt_sha256"],
        "service_success_disposition_sha256": service["success_disposition_sha256"],
        "safe_error_capture_runtime_sha256": GUIDE_SAFE_ERROR_CAPTURE_RUNTIME_SHA256,
    }


def validate_synthetic_guide_authorization(
    authorization_path: Path,
    plan_path: Path,
    canonical_w_path: Path,
) -> dict[str, Any]:
    """Validate one exact guide-only authority without reading credentials."""

    authorization_path = Path(authorization_path).absolute()
    plan_path = Path(plan_path).absolute()
    authorization_root = _document_root(authorization_path)
    plan_root = _document_root(plan_path)
    if authorization_root != plan_root:
        raise ValidationError("guide authorization must live in the exact plan fixture root")
    authorization, _authorization_bytes, authorization_sha256 = _read_bound_fixture_json(
        authorization_root,
        authorization_path,
        "synthetic-guide authorization",
    )
    schema_version = authorization.get("schema_version")
    if schema_version not in {GUIDE_AUTH_SCHEMA, GUIDE_RECOVERY_AUTH_SCHEMA}:
        raise ValidationError("synthetic-guide authorization schema is unsupported")
    recovery_keys = (
        {"recovery_binding", "runtime_bindings"}
        if schema_version == GUIDE_RECOVERY_AUTH_SCHEMA
        else set()
    )
    authorization_keys = {
        "schema_version", "authorization_id", "status", "approved", "scope", "target",
        "bindings", "action", "billing_project_binding", "authorized_limits", "consumption",
        "approved_by", "approved_at", "expires_at", "execution_ready", "blockers",
        *recovery_keys,
    }
    _strict_object(
        authorization,
        authorization_keys,
        authorization_keys,
        "synthetic-guide authorization",
    )
    dry = dry_run_synthetic_guide(plan_path, canonical_w_path)
    plan = read_json(Path(plan_path))
    status, _ = _validate_common_authorization(
        authorization,
        authorization_path=authorization_path,
        schema=schema_version,
        scope=GUIDE_SCOPE,
        target=plan["target"],
    )
    errors: list[str] = []
    bindings = _strict_object(
        authorization.get("bindings"),
        {
            "performance_transfer_plan_sha256", "canonical_w_sha256", "microtest_token_slice_sha256",
            "spoken_text_sha256", "acting_prompt_sha256", "request_body_sha256", "request_set_sha256",
        },
        {
            "performance_transfer_plan_sha256", "canonical_w_sha256", "microtest_token_slice_sha256",
            "spoken_text_sha256", "acting_prompt_sha256", "request_body_sha256", "request_set_sha256",
        },
        "bindings",
    )
    expected_bindings = {
        "performance_transfer_plan_sha256": dry["plan_sha256"],
        "canonical_w_sha256": dry["canonical_w_sha256"],
        "microtest_token_slice_sha256": MICROTEST_TOKEN_SLICE_SHA256,
        "spoken_text_sha256": MICROTEST_TEXT_SHA256,
        "acting_prompt_sha256": GUIDE_ACTING_PROMPT_SHA256,
        "request_body_sha256": GUIDE_REQUEST_BODY_SHA256,
        "request_set_sha256": dry["request_set_sha256"],
    }
    _require(_json_exact(bindings, expected_bindings), "guide authorization bindings do not match compiled requests", errors)
    action = _strict_object(
        authorization.get("action"),
        {
            "provider", "endpoint", "method", "model_id", "voice_name", "language_code", "request_count",
            "identical_unseeded_requests", "output_encoding", "sample_rate_hz", "no_retry", "no_redirect",
            "no_fallback", "disclosure",
        },
        {
            "provider", "endpoint", "method", "model_id", "voice_name", "language_code", "request_count",
            "identical_unseeded_requests", "output_encoding", "sample_rate_hz", "no_retry", "no_redirect",
            "no_fallback", "disclosure",
        },
        "action",
    )
    expected_action = {
        "provider": GUIDE_PROVIDER, "endpoint": GUIDE_ENDPOINT, "method": "POST", "model_id": GUIDE_MODEL,
        "voice_name": GUIDE_VOICE, "language_code": GUIDE_LANGUAGE, "request_count": 2,
        "identical_unseeded_requests": True, "output_encoding": "LINEAR16", "sample_rate_hz": 24000,
        "no_retry": True, "no_redirect": True, "no_fallback": True,
        "disclosure": "exact_locked_words_and_nonlexical_acting_prompt_to_google_cloud_tts",
    }
    _require(_json_exact(action, expected_action), "guide authorization action drifted", errors)
    billing = _strict_object(
        authorization.get("billing_project_binding"),
        {"required", "raw_identifier_stored", "quota_project_sha256", "credential_source"},
        {"required", "raw_identifier_stored", "quota_project_sha256", "credential_source"},
        "billing_project_binding",
    )
    _require(billing.get("required") is True, "billing project binding is required", errors)
    _require(billing.get("raw_identifier_stored") is False, "raw billing project identifier must not be stored", errors)
    _require(billing.get("credential_source") == "local_untracked_google_adc", "credential_source must be local_untracked_google_adc", errors)
    if status == "active":
        _require(isinstance(billing.get("quota_project_sha256"), str) and bool(_SHA_RE.fullmatch(billing["quota_project_sha256"])), "active guide authorization requires a hashed quota project binding", errors)
    else:
        _require(billing.get("quota_project_sha256") == "pending", "draft quota project binding must be pending", errors)
    limits = _strict_object(
        authorization.get("authorized_limits"),
        {
            "max_calls", "max_outputs", "max_request_body_bytes", "max_total_request_bytes",
            "max_output_duration_seconds", "max_output_wav_bytes", "max_total_audio_bytes",
            "max_response_bytes_per_call", "max_spend_usd",
        },
        {
            "max_calls", "max_outputs", "max_request_body_bytes", "max_total_request_bytes",
            "max_output_duration_seconds", "max_output_wav_bytes", "max_total_audio_bytes",
            "max_response_bytes_per_call", "max_spend_usd",
        },
        "authorized_limits",
    )
    expected_limits = (
        {
            "max_calls": 2,
            "max_outputs": 2,
            "max_request_body_bytes": GUIDE_MAX_REQUEST_BODY_BYTES,
            "max_total_request_bytes": GUIDE_MAX_TOTAL_REQUEST_BYTES,
            "max_output_duration_seconds": GUIDE_MAX_OUTPUT_DURATION_SECONDS,
            "max_output_wav_bytes": GUIDE_MAX_OUTPUT_WAV_BYTES,
            "max_total_audio_bytes": GUIDE_MAX_TOTAL_AUDIO_BYTES,
            "max_response_bytes_per_call": GUIDE_MAX_RESPONSE_BYTES_PER_CALL,
            "max_spend_usd": GUIDE_MAX_SPEND_USD,
        }
        if status == "active"
        else {
            "max_calls": 0,
            "max_outputs": 0,
            "max_request_body_bytes": 0,
            "max_total_request_bytes": 0,
            "max_output_duration_seconds": 0,
            "max_output_wav_bytes": 0,
            "max_total_audio_bytes": 0,
            "max_response_bytes_per_call": 0,
            "max_spend_usd": 0,
        }
    )
    _require(_json_exact(limits, expected_limits), "guide authorized limits do not match authorization status", errors)
    if errors:
        raise ValidationError(errors)
    recovery_validation = None
    runtime_validation = None
    if schema_version == GUIDE_RECOVERY_AUTH_SCHEMA:
        runtime_validation = _validate_guide_runtime_bindings(
            authorization["runtime_bindings"],
            status=status,
            errors=errors,
        )
        recovery_validation = _validate_guide_recovery_binding(
            authorization_root,
            authorization["recovery_binding"],
            dry=dry,
            target=plan["target"],
        )
        if errors:
            raise ValidationError(errors)
    return {
        **dry,
        "authorization_id": authorization["authorization_id"],
        "authorization_sha256": authorization_sha256,
        "authorization_status": status,
        "provider_action_authorized": status == "active",
        "network_authorized": status == "active",
        "execution_transport_available": status == "active",
        "quota_project_runtime_check_required": status == "active",
        "recovery_binding": recovery_validation,
        "runtime_bindings": runtime_validation,
        "committed_source_proof_required": (
            status == "active" and schema_version == GUIDE_RECOVERY_AUTH_SCHEMA
        ),
        "credentials_accessed": False,
        "network_called": False,
    }


@dataclass(frozen=True)
class _GuideExecutionContract:
    root: Path
    authorization_path: Path
    authorization: dict[str, Any]
    authorization_sha256: str
    plan_path: Path
    canonical_w_path: Path
    dry_run: dict[str, Any]
    consumption_relative: str
    success_receipt_relative: str
    failure_receipt_relative: str
    approved_at: datetime
    expires_at: datetime


@dataclass(frozen=True)
class _GoogleResponse:
    response_bytes: int
    response_sha256: str
    wav_bytes: bytes
    geometry: dict[str, Any]
    provider_identifiers: dict[str, str]
    provider_usage: dict[str, int]


class _GuideExecutionFailure(Exception):
    """A provider or local execution failure with only redacted metadata."""

    def __init__(
        self,
        code: str,
        *,
        http_status: int | None = None,
        response_bytes: int = 0,
        response_sha256: str | None = None,
        provider_error: dict[str, Any] | None = None,
        provider_identifiers: dict[str, str] | None = None,
        provider_usage: dict[str, int] | None = None,
    ) -> None:
        super().__init__(code)
        self.code = code
        self.http_status = http_status
        self.response_bytes = response_bytes
        self.response_sha256 = response_sha256
        self.provider_error = provider_error
        self.provider_identifiers = provider_identifiers or {}
        self.provider_usage = provider_usage or {}


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    """Make every redirect terminal; a redirected request is never authorized."""

    def redirect_request(  # type: ignore[override]
        self,
        request: urllib.request.Request,
        file_pointer: BinaryIO,
        code: int,
        message: str,
        headers: Any,
        new_url: str,
    ) -> None:
        return None


def _execution_now() -> datetime:
    """Clock seam used by adversarial expiry tests."""

    return datetime.now(timezone.utc)


def _iso_utc(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat()


def _receipt_bytes(value: dict[str, Any]) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")


def _strict_json_bytes(data: bytes, label: str) -> dict[str, Any]:
    """Decode an RFC 8259 object, rejecting duplicate names and JSON constants."""

    def reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError("duplicate member")
            result[key] = value
        return result

    def reject_constant(_value: str) -> None:
        raise ValueError("non-standard JSON constant")

    invalid = False
    value: Any = None
    try:
        text = data.decode("utf-8", errors="strict")
        value = json.loads(
            text,
            object_pairs_hook=reject_duplicates,
            parse_constant=reject_constant,
        )
    except (UnicodeError, json.JSONDecodeError, ValueError):
        invalid = True
    if invalid:
        raise ValidationError(f"{label} is not strict UTF-8 JSON") from None
    if not isinstance(value, dict):
        raise ValidationError(f"{label} must be a JSON object")
    return value


def _read_bound_fixture_json(
    root: Path,
    path: Path,
    label: str,
    *,
    required_mode: int | None = None,
    max_bytes: int = 1_000_000,
) -> tuple[dict[str, Any], bytes, str]:
    """Descriptor-bind and strict-decode one bounded fixture-local JSON record."""

    try:
        relative = Path(path).absolute().relative_to(root).as_posix()
    except ValueError:
        raise ValidationError(f"{label} is outside the fixture root") from None
    parent_fd, name = _open_parent_descriptor(root, relative, create_parents=False)
    descriptor: int | None = None
    chunks: list[bytes] = []
    chunk = b""
    try:
        flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
        descriptor = os.open(name, flags, dir_fd=parent_fd)
        before = os.fstat(descriptor)
        if (
            not stat.S_ISREG(before.st_mode)
            or before.st_size <= 1
            or before.st_size > max_bytes
            or (
                required_mode is not None
                and stat.S_IMODE(before.st_mode) != required_mode
            )
        ):
            raise ValidationError(f"{label} is not a bounded regular file with exact permissions")
        received = 0
        while True:
            chunk = os.read(descriptor, min(65_536, max_bytes + 1 - received))
            if not chunk:
                break
            chunks.append(chunk)
            received += len(chunk)
            if received > max_bytes:
                raise ValidationError(f"{label} exceeds its byte ceiling")
        raw = b"".join(chunks)
        after = os.fstat(descriptor)
        if (
            len(raw) != before.st_size
            or (
                before.st_dev,
                before.st_ino,
                before.st_size,
                before.st_mtime_ns,
                before.st_mode,
            )
            != (
                after.st_dev,
                after.st_ino,
                after.st_size,
                after.st_mtime_ns,
                after.st_mode,
            )
        ):
            raise ValidationError(f"{label} changed during its bound read")
        return _strict_json_bytes(raw, label), raw, sha256_bytes(raw)
    except ValidationError:
        raise
    except OSError:
        raise ValidationError(f"{label} is missing or unsafe") from None
    finally:
        chunks = []
        chunk = b""
        if descriptor is not None:
            os.close(descriptor)
        os.close(parent_fd)


def _safe_execution_relative(root: Path, value: str, label: str, suffix: str) -> Path:
    path = _safe_relative(root, value, label, must_exist=False, suffix=suffix)
    if path.exists() or path.is_symlink():
        raise ValidationError(f"{label} must not already exist")
    return path


def _preflight_execution_paths(contract: _GuideExecutionContract) -> None:
    """Prove every possible execution destination is new and fixture-local."""

    output_relatives = [request["destination"] for request in contract.dry_run["requests"]]
    if output_relatives != list(GUIDE_DESTINATIONS):
        raise ValidationError("compiled guide destinations drifted")
    for index, relative in enumerate(output_relatives):
        path = _safe_execution_relative(
            contract.root,
            relative,
            f"guide output {index + 1}",
            ".wav",
        )
        if path.relative_to(contract.root).parts[0] != "outputs":
            raise ValidationError("guide output must remain below outputs/")
    consumption = _safe_execution_relative(
        contract.root,
        contract.consumption_relative,
        "guide consumption record",
        ".json",
    )
    if consumption.relative_to(contract.root).parts[:2] != ("authorizations", "consumed"):
        raise ValidationError("guide consumption record must remain below authorizations/consumed/")
    for label, relative in (
        ("guide success receipt", contract.success_receipt_relative),
        ("guide failure receipt", contract.failure_receipt_relative),
    ):
        path = _safe_execution_relative(contract.root, relative, label, ".json")
        if path.relative_to(contract.root).parts[:2] != ("receipts", "google"):
            raise ValidationError(f"{label} must remain below receipts/google/")


def _open_parent_descriptor(
    root: Path,
    relative: str,
    *,
    create_parents: bool,
) -> tuple[int, str]:
    """Open a path's parent through O_NOFOLLOW directory descriptors."""

    parts = Path(relative).parts
    if (
        not parts
        or Path(relative).is_absolute()
        or any(part in {"", ".", "..", "~"} for part in parts)
    ):
        raise ValidationError("execution destination is not a safe relative path")
    directory_flags = os.O_RDONLY
    if hasattr(os, "O_DIRECTORY"):
        directory_flags |= os.O_DIRECTORY
    if hasattr(os, "O_NOFOLLOW"):
        directory_flags |= os.O_NOFOLLOW
    try:
        current_fd = os.open(root, directory_flags)
    except OSError as exc:
        raise ValidationError("cannot safely open execution fixture root") from exc
    try:
        root_stat = os.fstat(current_fd)
        if not stat.S_ISDIR(root_stat.st_mode):
            raise ValidationError("execution fixture root is not a directory")
        for component in parts[:-1]:
            try:
                next_fd = os.open(component, directory_flags, dir_fd=current_fd)
            except FileNotFoundError:
                if not create_parents:
                    raise ValidationError("execution destination parent does not exist")
                try:
                    os.mkdir(component, mode=0o700, dir_fd=current_fd)
                    os.fsync(current_fd)
                except FileExistsError:
                    pass
                except OSError as exc:
                    raise ValidationError("cannot safely create execution destination parent") from exc
                try:
                    next_fd = os.open(component, directory_flags, dir_fd=current_fd)
                except OSError as exc:
                    raise ValidationError("cannot safely open execution destination parent") from exc
            except OSError as exc:
                raise ValidationError("execution destination may not traverse a symlink") from exc
            os.close(current_fd)
            current_fd = next_fd
            opened = os.fstat(current_fd)
            if not stat.S_ISDIR(opened.st_mode):
                raise ValidationError("execution destination parent is not a directory")
        return current_fd, parts[-1]
    except Exception:
        os.close(current_fd)
        raise


def _ensure_execution_parents(root: Path, relatives: list[str]) -> None:
    for relative in relatives:
        descriptor, _name = _open_parent_descriptor(
            root,
            relative,
            create_parents=True,
        )
        os.close(descriptor)


def _exclusive_fixture_write(root: Path, relative: str, data: bytes) -> Path:
    """Create one immutable private artifact without following a symlink."""

    parent_fd, name = _open_parent_descriptor(root, relative, create_parents=False)
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    descriptor: int | None = None
    try:
        descriptor = os.open(name, flags, 0o600, dir_fd=parent_fd)
        os.fchmod(descriptor, 0o600)
        view = memoryview(data)
        written = 0
        while written < len(view):
            count = os.write(descriptor, view[written:])
            if count <= 0:
                raise OSError("short write")
            written += count
        os.fsync(descriptor)
        created = os.fstat(descriptor)
        if not stat.S_ISREG(created.st_mode) or created.st_size != len(data):
            raise OSError("created artifact geometry mismatch")
        os.fsync(parent_fd)
    except FileExistsError as exc:
        raise ValidationError("execution destination collision") from exc
    except OSError as exc:
        raise ValidationError("cannot create immutable execution artifact") from exc
    finally:
        if descriptor is not None:
            os.close(descriptor)
        os.close(parent_fd)
    return root / relative


def _verify_private_fixture_artifact(
    root: Path,
    relative: str,
    expected_bytes: bytes,
    label: str,
) -> None:
    """Re-read an immutable latch/output path through a no-follow descriptor."""

    parent_fd, name = _open_parent_descriptor(root, relative, create_parents=False)
    flags = os.O_RDONLY
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    descriptor: int | None = None
    try:
        descriptor = os.open(name, flags, dir_fd=parent_fd)
        before = os.fstat(descriptor)
        if (
            not stat.S_ISREG(before.st_mode)
            or stat.S_IMODE(before.st_mode) != 0o600
            or before.st_size != len(expected_bytes)
        ):
            raise ValidationError(f"{label} geometry or permissions drifted")
        chunks: list[bytes] = []
        received = 0
        while True:
            chunk = os.read(descriptor, min(65_536, len(expected_bytes) + 1 - received))
            if not chunk:
                break
            chunks.append(chunk)
            received += len(chunk)
            if received > len(expected_bytes):
                raise ValidationError(f"{label} content drifted")
        actual = b"".join(chunks)
        after = os.fstat(descriptor)
        if (
            actual != expected_bytes
            or (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns)
            != (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns)
        ):
            raise ValidationError(f"{label} content drifted")
    except ValidationError:
        raise
    except OSError:
        raise ValidationError(f"{label} is missing or unsafe") from None
    finally:
        if descriptor is not None:
            os.close(descriptor)
        os.close(parent_fd)


def _verify_execution_output(root: Path, item: dict[str, Any]) -> None:
    path = _safe_relative(
        root,
        item.get("path"),
        "written guide output",
        must_exist=True,
        suffix=".wav",
    )
    try:
        mode = stat.S_IMODE(path.lstat().st_mode)
    except OSError as exc:
        raise ValidationError("cannot inspect written guide output") from exc
    if mode != 0o600:
        raise ValidationError("written guide output permissions drifted")
    _read_bound_wav(
        path,
        item["byte_count"],
        item["sha256"],
        float(item["duration_seconds"]),
    )


def _build_guide_execution_contract(
    authorization_path: Path,
    plan_path: Path,
    canonical_w_path: Path,
) -> _GuideExecutionContract:
    authorization_path = Path(authorization_path).absolute()
    plan_path = Path(plan_path).absolute()
    canonical_w_path = Path(canonical_w_path).absolute()
    validation = validate_synthetic_guide_authorization(
        authorization_path,
        plan_path,
        canonical_w_path,
    )
    if validation.get("authorization_status") != "active":
        raise ValidationError("synthetic-guide execution requires an exact active G1 authorization")
    root = _document_root(authorization_path)
    authorization, _authorization_bytes, authorization_sha256 = _read_bound_fixture_json(
        root,
        authorization_path,
        "active synthetic-guide authorization",
    )
    if authorization_sha256 != validation.get("authorization_sha256"):
        raise ValidationError(
            "active synthetic-guide authorization changed after validation"
        )
    errors: list[str] = []
    approved_at = _parse_time(authorization.get("approved_at"), "approved_at", errors)
    expires_at = _parse_time(authorization.get("expires_at"), "expires_at", errors)
    if errors or approved_at is None or expires_at is None:
        raise ValidationError(errors or "active G1 authorization window is invalid")
    now = _execution_now()
    if not approved_at <= now < expires_at:
        raise ValidationError("active G1 authorization is outside its execution window")
    auth_id = authorization["authorization_id"]
    consumption_relative = authorization["consumption"]["record_path"]
    success_relative = f"receipts/google/{auth_id}.run.json"
    failure_relative = f"receipts/google/{auth_id}.failure.json"
    contract = _GuideExecutionContract(
        root=root,
        authorization_path=authorization_path,
        authorization=authorization,
        authorization_sha256=authorization_sha256,
        plan_path=plan_path,
        canonical_w_path=canonical_w_path,
        dry_run=dry_run_synthetic_guide(plan_path, canonical_w_path),
        consumption_relative=consumption_relative,
        success_receipt_relative=success_relative,
        failure_receipt_relative=failure_relative,
        approved_at=approved_at,
        expires_at=expires_at,
    )
    _preflight_execution_paths(contract)
    return contract


def _guide_repository_root() -> Path:
    return Path(__file__).resolve().parents[4]


def _open_bound_executable_descriptor(
    path_value: str,
    expected_sha256: str | None,
    label: str,
    *,
    max_bytes: int = 16_000_000,
) -> tuple[int, str]:
    """Open and hash one exact executable inode without following path symlinks."""

    if (
        not isinstance(path_value, str)
        or not path_value
        or "\x00" in path_value
        or not isinstance(label, str)
        or not label
        or type(max_bytes) is not int
        or not 0 < max_bytes <= 64_000_000
        or (
            expected_sha256 is not None
            and (
                not isinstance(expected_sha256, str)
                or not _SHA_RE.fullmatch(expected_sha256)
            )
        )
    ):
        raise ValidationError("bound executable identity contract is invalid")
    try:
        path = Path(path_value)
        if not path.is_absolute() or path.resolve(strict=True) != path:
            raise ValidationError(f"bound {label} path must be an exact resolved absolute path")
    except (OSError, RuntimeError):
        raise ValidationError(f"bound {label} path is missing or unsafe") from None

    parent_fd: int | None = None
    descriptor: int | None = None
    chunks: list[bytes] = []
    chunk = b""
    try:
        parent_fd = os.open("/", os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
        for component in path.parts[1:-1]:
            next_fd = os.open(
                component,
                os.O_RDONLY
                | getattr(os, "O_DIRECTORY", 0)
                | getattr(os, "O_NOFOLLOW", 0),
                dir_fd=parent_fd,
            )
            os.close(parent_fd)
            parent_fd = next_fd
        descriptor = os.open(
            path.name,
            os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0),
            dir_fd=parent_fd,
        )
        before = os.fstat(descriptor)
        if (
            not stat.S_ISREG(before.st_mode)
            or not stat.S_IMODE(before.st_mode) & 0o111
            or not 0 < before.st_size <= max_bytes
        ):
            raise ValidationError(f"bound {label} is not a bounded executable regular file")
        received = 0
        while True:
            chunk = os.read(descriptor, min(1_048_576, max_bytes + 1 - received))
            if not chunk:
                break
            chunks.append(chunk)
            received += len(chunk)
            if received > max_bytes:
                raise ValidationError(f"bound {label} exceeds its executable byte cap")
        raw = b"".join(chunks)
        after = os.fstat(descriptor)
        if (
            len(raw) != before.st_size
            or (
                before.st_dev,
                before.st_ino,
                before.st_size,
                before.st_mtime_ns,
                before.st_mode,
                before.st_uid,
            )
            != (
                after.st_dev,
                after.st_ino,
                after.st_size,
                after.st_mtime_ns,
                after.st_mode,
                after.st_uid,
            )
        ):
            raise ValidationError(f"bound {label} changed during executable identity read")
        digest = sha256_bytes(raw)
        raw = b""
        if expected_sha256 is not None and digest != expected_sha256:
            raise ValidationError(f"bound {label} SHA-256 drifted")
        os.lseek(descriptor, 0, os.SEEK_SET)
        returned = descriptor
        descriptor = None
        return returned, digest
    except ValidationError:
        raise
    except OSError:
        raise ValidationError(f"bound {label} is missing or unsafe") from None
    finally:
        chunks = []
        chunk = b""
        if descriptor is not None:
            os.close(descriptor)
        if parent_fd is not None:
            os.close(parent_fd)


@contextmanager
def _private_executable_copy(
    path_value: str,
    expected_sha256: str,
    label: str,
):
    """Yield a 0500 private exact-byte executable copy in a fresh 0700 directory."""

    source_fd: int | None = None
    post_source_fd: int | None = None
    copy_fd: int | None = None
    verify_fd: int | None = None
    directory: str | None = None
    copy_path: str | None = None
    chunk = b""
    source_identity: tuple[int, int, int, int, int, int] | None = None
    post_verified = False
    try:
        source_fd, _source_sha = _open_bound_executable_descriptor(
            path_value,
            expected_sha256,
            label,
        )
        source_before = os.fstat(source_fd)
        source_identity = (
            source_before.st_dev,
            source_before.st_ino,
            source_before.st_size,
            source_before.st_mtime_ns,
            source_before.st_mode,
            source_before.st_uid,
        )
        temporary_root = str(Path("/tmp").resolve(strict=True))
        directory = tempfile.mkdtemp(prefix="oe-bound-media-tool-", dir=temporary_root)
        os.chmod(directory, 0o700)
        directory_stat = os.stat(directory, follow_symlinks=False)
        if (
            not stat.S_ISDIR(directory_stat.st_mode)
            or stat.S_IMODE(directory_stat.st_mode) != 0o700
            or directory_stat.st_uid != os.getuid()
        ):
            raise ValidationError("private executable-copy directory is unsafe")
        copy_path = str(Path(directory) / "tool")
        copy_fd = os.open(
            copy_path,
            os.O_WRONLY
            | os.O_CREAT
            | os.O_EXCL
            | getattr(os, "O_NOFOLLOW", 0),
            0o500,
        )
        while True:
            chunk = os.read(source_fd, 1_048_576)
            if not chunk:
                break
            offset = 0
            while offset < len(chunk):
                written = os.write(copy_fd, chunk[offset:])
                if written <= 0:
                    raise ValidationError("private executable copy short-write failed")
                offset += written
        os.fchmod(copy_fd, 0o500)
        os.fsync(copy_fd)
        os.close(copy_fd)
        copy_fd = None
        verify_fd, copy_sha = _open_bound_executable_descriptor(
            copy_path,
            expected_sha256,
            f"private {label} copy",
        )
        copy_stat = os.fstat(verify_fd)
        if (
            copy_sha != expected_sha256
            or stat.S_IMODE(copy_stat.st_mode) != 0o500
            or copy_stat.st_uid != os.getuid()
            or copy_stat.st_nlink != 1
        ):
            raise ValidationError("private executable copy identity is unsafe")
        os.close(verify_fd)
        verify_fd = None
        yield copy_path
        verify_fd, copy_sha = _open_bound_executable_descriptor(
            copy_path,
            expected_sha256,
            f"private {label} copy",
        )
        copy_stat = os.fstat(verify_fd)
        post_source_fd, _post_source_sha = _open_bound_executable_descriptor(
            path_value,
            expected_sha256,
            label,
        )
        source_after = os.fstat(post_source_fd)
        if (
            copy_sha != expected_sha256
            or stat.S_IMODE(copy_stat.st_mode) != 0o500
            or copy_stat.st_uid != os.getuid()
            or copy_stat.st_nlink != 1
            or source_identity
            != (
                source_after.st_dev,
                source_after.st_ino,
                source_after.st_size,
                source_after.st_mtime_ns,
                source_after.st_mode,
                source_after.st_uid,
            )
        ):
            raise ValidationError("bound executable or private copy changed during execution")
        post_verified = True
    except ValidationError:
        raise
    except OSError:
        raise ValidationError("private executable copy failed closed") from None
    finally:
        chunk = b""
        cleanup_failed = False
        if not post_verified and copy_path is not None and source_identity is not None:
            try:
                if verify_fd is not None:
                    os.close(verify_fd)
                    verify_fd = None
                if post_source_fd is not None:
                    os.close(post_source_fd)
                    post_source_fd = None
                verify_fd, copy_sha = _open_bound_executable_descriptor(
                    copy_path,
                    expected_sha256,
                    f"private {label} copy",
                )
                copy_stat = os.fstat(verify_fd)
                post_source_fd, _post_source_sha = _open_bound_executable_descriptor(
                    path_value,
                    expected_sha256,
                    label,
                )
                source_after = os.fstat(post_source_fd)
                if (
                    copy_sha != expected_sha256
                    or stat.S_IMODE(copy_stat.st_mode) != 0o500
                    or copy_stat.st_uid != os.getuid()
                    or copy_stat.st_nlink != 1
                    or source_identity
                    != (
                        source_after.st_dev,
                        source_after.st_ino,
                        source_after.st_size,
                        source_after.st_mtime_ns,
                        source_after.st_mode,
                        source_after.st_uid,
                    )
                ):
                    cleanup_failed = True
            except (OSError, ValidationError):
                cleanup_failed = True
        for descriptor in (verify_fd, copy_fd, post_source_fd, source_fd):
            if descriptor is not None:
                try:
                    os.close(descriptor)
                except OSError:
                    cleanup_failed = True
        if copy_path is not None:
            try:
                os.unlink(copy_path)
            except FileNotFoundError:
                pass
            except OSError:
                cleanup_failed = True
        if directory is not None:
            try:
                os.rmdir(directory)
            except OSError:
                cleanup_failed = True
        if cleanup_failed:
            raise ValidationError("private executable-copy cleanup failed closed") from None


def _guide_git(
    arguments: list[str],
    *,
    max_bytes: int = 2_000_000,
    git_path: str | None = None,
    git_sha256: str | None = None,
    allowed_returncodes: tuple[int, ...] = (0,),
) -> bytes:
    """Run one bounded, local-only Git read with no inherited provider secrets."""

    candidate = git_path
    if candidate is None:
        candidate = shutil.which("git", path="/usr/bin:/bin:/opt/homebrew/bin:/usr/local/bin")
        if candidate is not None:
            try:
                candidate = str(Path(candidate).resolve(strict=True))
            except (OSError, RuntimeError):
                candidate = None
    if not isinstance(candidate, str):
        raise ValidationError("committed synthetic-guide runtime preflight failed") from None
    executable_fd: int | None = None
    post_fd: int | None = None
    before_identity: tuple[int, int, int, int, int, int] | None = None
    try:
        executable_fd, _digest = _open_bound_executable_descriptor(
            candidate,
            git_sha256,
            "Git executable",
        )
        before = os.fstat(executable_fd)
        before_identity = (
            before.st_dev,
            before.st_ino,
            before.st_size,
            before.st_mtime_ns,
            before.st_mode,
            before.st_uid,
        )
    except ValidationError:
        raise ValidationError("committed synthetic-guide runtime preflight failed") from None

    environment: dict[str, str] = {
        "PATH": "/usr/bin:/bin",
        "TMPDIR": "/tmp",
        "LC_ALL": "C",
        "LANG": "C",
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_CONFIG_GLOBAL": "/dev/null",
        "GIT_NO_REPLACE_OBJECTS": "1",
        "GIT_NO_LAZY_FETCH": "1",
        "GIT_OPTIONAL_LOCKS": "0",
        "GIT_PAGER": "cat",
        "GIT_TERMINAL_PROMPT": "0",
    }
    result: Any = None
    stdout = b""
    failed = False
    try:
        result = subprocess.run(
            [
                candidate,
                "-c",
                "core.fsmonitor=false",
                "-c",
                "core.untrackedCache=false",
                "-c",
                "core.hooksPath=/dev/null",
                *arguments,
            ],
            cwd=_guide_repository_root(),
            check=False,
            capture_output=True,
            text=False,
            timeout=15,
            env=environment,
            close_fds=True,
        )
        stdout = result.stdout if isinstance(result.stdout, bytes) else b""
        stderr = result.stderr if isinstance(result.stderr, bytes) else b""
        failed = (
            type(result.returncode) is not int
            or result.returncode not in allowed_returncodes
            or len(stdout) > max_bytes
            or len(stderr) > max_bytes
        )
        post_fd, _post_digest = _open_bound_executable_descriptor(
            candidate,
            git_sha256,
            "Git executable",
        )
        after = os.fstat(post_fd)
        failed = failed or before_identity != (
            after.st_dev,
            after.st_ino,
            after.st_size,
            after.st_mtime_ns,
            after.st_mode,
            after.st_uid,
        )
    except Exception:
        failed = True
    result = None
    stderr = b""
    environment = {}
    if executable_fd is not None:
        os.close(executable_fd)
        executable_fd = None
    if post_fd is not None:
        os.close(post_fd)
        post_fd = None
    if failed:
        stdout = b""
        raise ValidationError("committed synthetic-guide runtime preflight failed") from None
    return stdout


def _verify_guide_recovery_source(
    contract: _GuideExecutionContract,
    *,
    allow_consumption_latch: bool = False,
) -> dict[str, Any]:
    """Prove v2 executes exact reviewed bytes from a pushed ACTIVE-only DAG."""

    if contract.authorization.get("schema_version") != GUIDE_RECOVERY_AUTH_SCHEMA:
        return {}
    bindings = contract.authorization["runtime_bindings"]
    repository = _guide_repository_root()
    head = _guide_git(["rev-parse", "HEAD"]).strip().decode("ascii", errors="strict")
    upstream = _guide_git(["rev-parse", "@{upstream}"]).strip().decode(
        "ascii",
        errors="strict",
    )
    runtime_commit = bindings["git_commit"]
    if (
        not _GIT_SHA_RE.fullmatch(head)
        or not _GIT_SHA_RE.fullmatch(upstream)
        or head != upstream
    ):
        raise ValidationError("synthetic-guide HEAD must equal its configured upstream")
    _guide_git(["merge-base", "--is-ancestor", runtime_commit, head])
    try:
        authorization_relative = contract.authorization_path.relative_to(repository).as_posix()
    except ValueError:
        raise ValidationError("synthetic-guide authority is outside the committed repository") from None
    delta = _guide_git(
        [
            "diff",
            "--no-ext-diff",
            "--no-textconv",
            "--no-renames",
            "--name-only",
            "--diff-filter=ACDMRTUXB",
            "-z",
            f"{runtime_commit}..{head}",
        ]
    )
    if delta != authorization_relative.encode("utf-8") + b"\x00":
        raise ValidationError(
            "recovery runtime commit to HEAD delta must be exactly the active authorization path"
        )
    _active_value, active_bytes, active_sha256 = _read_bound_fixture_json(
        contract.root,
        contract.authorization_path,
        "active recovery guide authorization",
    )
    if (
        active_sha256 != contract.authorization_sha256
        or _guide_git(["show", f"HEAD:{authorization_relative}"]) != active_bytes
    ):
        raise ValidationError("active recovery guide authorization is not committed exactly")

    evidence_paths: list[Path] = [contract.plan_path, contract.canonical_w_path]
    recovery = contract.authorization["recovery_binding"]
    for item in recovery["prior_failures"]:
        failure_path = _safe_relative(
            contract.root,
            item["failure_receipt_path"],
            f"{item['attempt_id']} committed failure",
            must_exist=True,
            suffix=".json",
        )
        failure, _failure_bytes, _failure_sha = _read_bound_fixture_json(
            contract.root,
            failure_path,
            f"{item['attempt_id']} committed failure",
            required_mode=0o600,
        )
        evidence_paths.extend(
            [
                failure_path,
                _safe_relative(
                    contract.root,
                    failure["guide_authorization_path"],
                    f"{item['attempt_id']} committed authorization",
                    must_exist=True,
                    suffix=".json",
                ),
                _safe_relative(
                    contract.root,
                    failure["guide_consumption_record_path"],
                    f"{item['attempt_id']} committed consumption",
                    must_exist=True,
                    suffix=".json",
                ),
            ]
        )
    service = recovery["service_enablement"]
    for relative, label in (
        (recovery["diagnosis"]["path"], "committed G1R2 diagnosis"),
        (service["authorization_path"], "committed service authorization"),
        (service["consumption_record_path"], "committed service consumption"),
        (service["run_receipt_path"], "committed service run receipt"),
        (service["success_disposition_path"], "committed service-success disposition"),
    ):
        evidence_paths.append(
            _safe_relative(
                contract.root,
                relative,
                label,
                must_exist=True,
                suffix=".json",
            )
        )

    seen: set[str] = set()
    for path in evidence_paths:
        try:
            relative = path.relative_to(repository).as_posix()
        except ValueError:
            raise ValidationError("recovery authority evidence is outside the repository") from None
        if relative in seen:
            continue
        seen.add(relative)
        try:
            current = path.read_bytes()
        except OSError:
            raise ValidationError("recovery authority evidence is unavailable") from None
        if _guide_git(["show", f"{runtime_commit}:{relative}"]) != current:
            raise ValidationError("recovery authority evidence is not exact at runtime commit")

    for name, (relative, path) in _guide_runtime_files().items():
        expected_sha256 = bindings[f"{name}_sha256"]
        try:
            current = path.read_bytes()
        except OSError:
            raise ValidationError("bound recovery runtime is unavailable") from None
        committed = _guide_git(["show", f"{runtime_commit}:{relative}"])
        if (
            sha256_bytes(current) != expected_sha256
            or sha256_bytes(committed) != expected_sha256
            or committed != current
        ):
            raise ValidationError("bound recovery runtime is not exact at runtime commit")
    dirty = _guide_git(
        ["status", "--porcelain=v1", "--untracked-files=all", "-z"]
    )
    allowed_dirty = b""
    if allow_consumption_latch:
        consumption_path = contract.root / contract.consumption_relative
        try:
            consumption_relative = consumption_path.relative_to(repository).as_posix()
        except ValueError:
            raise ValidationError("G1R2 consumption latch is outside the repository") from None
        allowed_dirty = b"?? " + consumption_relative.encode("utf-8") + b"\x00"
    if dirty != allowed_dirty:
        raise ValidationError("repository worktree must be globally clean before G1R2")
    return {
        "git_head": head,
        "runtime_commit": runtime_commit,
        "upstream_equal": True,
        "head_delta_policy": "exact_active_authorization_path_only",
        "head_delta_path": authorization_relative,
    }


def _quota_project_for_execution(authorization: dict[str, Any]) -> str:
    """Read and hash-match the private quota-project value without exposing it."""

    value = os.environ.get(GUIDE_QUOTA_PROJECT_ENV)
    failure_message: str | None = None
    malformed = (
        not isinstance(value, str)
        or not value
        or value != value.strip()
        or len(value) > 255
        or any(character.isspace() or ord(character) < 33 or ord(character) > 126 for character in value)
    )
    if malformed:
        failure_message = "the private Google quota-project binding is absent or malformed"
    elif sha256_bytes(value.encode("utf-8")) != authorization["billing_project_binding"]["quota_project_sha256"]:
        failure_message = "the private Google quota-project binding does not match AUTH-G1"
    if failure_message is not None:
        # Keep the raw project identifier out of the raised exception's frame.
        value = None
        raise ValidationError(failure_message) from None
    assert isinstance(value, str)
    return value


def _open_absolute_directory_no_symlink(path: Path) -> int:
    """Descriptor-walk an absolute directory without following any component."""

    absolute = Path(path).absolute()
    parts = absolute.parts
    if not absolute.is_absolute() or not parts:
        raise ValidationError("local gcloud ADC path is unsafe")
    flags = os.O_RDONLY
    if hasattr(os, "O_DIRECTORY"):
        flags |= os.O_DIRECTORY
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    try:
        current_fd = os.open(absolute.anchor, flags)
    except OSError:
        raise ValidationError("local gcloud ADC path is unavailable or unsafe") from None
    try:
        for component in parts[1:]:
            try:
                next_fd = os.open(component, flags, dir_fd=current_fd)
            except OSError:
                raise ValidationError("local gcloud ADC path is unavailable or unsafe") from None
            os.close(current_fd)
            current_fd = next_fd
        info = os.fstat(current_fd)
        if not stat.S_ISDIR(info.st_mode):
            raise ValidationError("local gcloud ADC path is unavailable or unsafe")
        return current_fd
    except Exception:
        os.close(current_fd)
        raise


def _preflight_google_adc() -> str:
    """Check local gcloud ADC material without refreshing a token or using network."""

    executable = shutil.which("gcloud")
    if not executable:
        raise ValidationError("gcloud is unavailable for the authorized ADC credential mechanism")
    config_value = os.environ.get("CLOUDSDK_CONFIG")
    config_parts: tuple[str, ...] = ()
    if isinstance(config_value, str) and config_value:
        config_parts = Path(config_value).expanduser().parts
        if any(part in {"", ".", "..", "~"} for part in config_parts):
            config_value = None
            config_parts = ()
            raise ValidationError("local gcloud ADC path is unsafe")
    config_root = (
        Path(config_value).expanduser().absolute()
        if isinstance(config_value, str) and config_value
        else Path.home() / ".config" / "gcloud"
    )
    adc_name = "application_default_credentials.json"
    flags = os.O_RDONLY
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    failure_message: str | None = None
    config_descriptor: int | None = None
    descriptor: int | None = None
    recheck_descriptor: int | None = None
    config_identity: Any = None
    chunks: list[bytes] = []
    chunk = b""
    data = b""
    value: Any = None
    credential_type: Any = None
    try:
        config_descriptor = _open_absolute_directory_no_symlink(config_root)
        config_identity = os.fstat(config_descriptor)
        descriptor = os.open(adc_name, flags, dir_fd=config_descriptor)
        try:
            info = os.fstat(descriptor)
            if not stat.S_ISREG(info.st_mode) or info.st_size <= 1 or info.st_size > 1_000_000:
                raise ValidationError("local gcloud ADC material is unavailable or malformed")
            received = 0
            while True:
                chunk = os.read(descriptor, min(65_536, 1_000_001 - received))
                if not chunk:
                    break
                chunks.append(chunk)
                received += len(chunk)
                if received > 1_000_000:
                    raise ValidationError("local gcloud ADC material is unavailable or malformed")
            data = b"".join(chunks)
            after = os.fstat(descriptor)
            if (
                (info.st_dev, info.st_ino, info.st_size, info.st_mtime_ns)
                != (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns)
                or len(data) != info.st_size
            ):
                raise ValidationError("local gcloud ADC material changed during preflight")
        finally:
            os.close(descriptor)
            descriptor = None
        recheck_descriptor = _open_absolute_directory_no_symlink(config_root)
        try:
            rechecked = os.fstat(recheck_descriptor)
            if (config_identity.st_dev, config_identity.st_ino) != (
                rechecked.st_dev,
                rechecked.st_ino,
            ):
                raise ValidationError("local gcloud ADC path changed during preflight")
        finally:
            os.close(recheck_descriptor)
            recheck_descriptor = None
        value = _strict_json_bytes(data, "local gcloud ADC material")
        credential_type = value.get("type")
        if credential_type not in {
            "authorized_user",
            "service_account",
            "external_account",
            "impersonated_service_account",
        }:
            raise ValidationError("local gcloud ADC material is unavailable or malformed")
    except (ValidationError, OSError, UnicodeError):
        # ADC JSON can contain client secrets or private keys. Convert every
        # parse/path failure into one fresh generic error after clearing locals.
        failure_message = "local gcloud ADC material or path is unavailable or unsafe or malformed"
    finally:
        if descriptor is not None:
            try:
                os.close(descriptor)
            except OSError:
                failure_message = "local gcloud ADC material or path is unavailable or unsafe or malformed"
        if recheck_descriptor is not None:
            try:
                os.close(recheck_descriptor)
            except OSError:
                failure_message = "local gcloud ADC material or path is unavailable or unsafe or malformed"
        if config_descriptor is not None:
            try:
                os.close(config_descriptor)
            except OSError:
                failure_message = "local gcloud ADC material or path is unavailable or unsafe or malformed"
    if failure_message is not None:
        config_value = None
        config_parts = ()
        config_root = None
        adc_name = ""
        chunks = []
        chunk = b""
        data = b""
        value = None
        credential_type = None
        config_identity = None
        raise ValidationError(failure_message) from None
    return executable


def _minimal_gcloud_environment() -> dict[str, str]:
    """Allow only non-secret process settings required by the gcloud wrapper."""

    allowed = ("PATH", "HOME", "CLOUDSDK_CONFIG", "LANG", "LC_ALL", "LC_CTYPE")
    environment = {
        key: value
        for key in allowed
        if isinstance((value := os.environ.get(key)), str) and value
    }
    environment["CLOUDSDK_CORE_DISABLE_PROMPTS"] = "1"
    return environment


def _load_google_access_token(gcloud_executable: str, timeout: float) -> str:
    """Refresh one ADC token after authority consumption; never expose output."""

    command = [gcloud_executable, *GUIDE_GCLOUD_TOKEN_COMMAND]
    failure_code: str | None = None
    result: Any = None
    raw = b""
    stripped = b""
    token: str | None = None
    try:
        result = subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=False,
            timeout=timeout,
            env=_minimal_gcloud_environment(),
        )
    except Exception:
        failure_code = "google_adc_token_refresh_failed"
    if failure_code is None:
        try:
            if type(result.returncode) is not int or result.returncode != 0:
                failure_code = "google_adc_token_refresh_failed"
            else:
                raw = result.stdout
                if not isinstance(raw, bytes) or len(raw) > 8_194:
                    failure_code = "google_adc_access_token_malformed"
                else:
                    stripped = raw.rstrip(b"\r\n")
                    try:
                        token = stripped.decode("ascii", errors="strict")
                    except UnicodeError:
                        token = None
                    if (
                        token is None
                        or len(token) < 16
                        or len(token) > 8_192
                        or token != token.strip()
                        or any(
                            character.isspace() or ord(character) < 33 or ord(character) > 126
                            for character in token
                        )
                    ):
                        failure_code = "google_adc_access_token_malformed"
        except Exception:
            failure_code = "google_adc_access_token_malformed"
    if failure_code is not None:
        # CompletedProcess and TimeoutExpired can both retain stdout/stderr.
        # Discard every provider-controlled local before raising the safe code.
        result = None
        raw = b""
        stripped = b""
        token = None
        raise _GuideExecutionFailure(failure_code) from None
    assert isinstance(token, str)
    return token


def _open_google_request(request: urllib.request.Request, timeout: float) -> Any:
    """One no-redirect opener seam. It performs no retry."""

    opener = urllib.request.build_opener(_NoRedirect())
    return opener.open(request, timeout=timeout)


def _validate_google_wav_bytes(data: bytes) -> dict[str, Any]:
    """Strictly decode the exact provider WAV; never trust declared geometry."""

    if len(data) > GUIDE_MAX_OUTPUT_WAV_BYTES:
        raise _GuideExecutionFailure("provider_wav_byte_cap_exceeded")
    if len(data) < 44 or data[:4] != b"RIFF" or data[8:12] != b"WAVE":
        raise _GuideExecutionFailure("provider_wav_container_invalid")
    declared_riff_size = int.from_bytes(data[4:8], "little")
    if declared_riff_size + 8 != len(data):
        raise _GuideExecutionFailure("provider_wav_payload_truncated_or_trailing")

    offset = 12
    chunks: list[tuple[bytes, bytes]] = []
    while offset < len(data):
        if offset + 8 > len(data):
            raise _GuideExecutionFailure("provider_wav_chunk_header_truncated")
        chunk_id = data[offset : offset + 4]
        chunk_size = int.from_bytes(data[offset + 4 : offset + 8], "little")
        offset += 8
        end = offset + chunk_size
        if end > len(data):
            raise _GuideExecutionFailure("provider_wav_payload_truncated_or_trailing")
        chunks.append((chunk_id, data[offset:end]))
        offset = end
        if chunk_size % 2:
            if offset >= len(data) or data[offset] != 0:
                raise _GuideExecutionFailure("provider_wav_chunk_padding_invalid")
            offset += 1
    if offset != len(data) or [chunk_id for chunk_id, _chunk in chunks] != [b"fmt ", b"data"]:
        raise _GuideExecutionFailure("provider_wav_chunk_layout_invalid")

    format_bytes = chunks[0][1]
    pcm = chunks[1][1]
    if len(format_bytes) != 16:
        raise _GuideExecutionFailure("provider_wav_format_invalid")
    audio_format = int.from_bytes(format_bytes[0:2], "little")
    channels = int.from_bytes(format_bytes[2:4], "little")
    sample_rate = int.from_bytes(format_bytes[4:8], "little")
    byte_rate = int.from_bytes(format_bytes[8:12], "little")
    block_align = int.from_bytes(format_bytes[12:14], "little")
    bits_per_sample = int.from_bytes(format_bytes[14:16], "little")
    if (
        audio_format != 1
        or channels != 1
        or sample_rate != GUIDE_SAMPLE_RATE_HZ
        or byte_rate != GUIDE_SAMPLE_RATE_HZ * 2
        or block_align != 2
        or bits_per_sample != 16
    ):
        raise _GuideExecutionFailure("provider_wav_media_geometry_invalid")
    if not pcm or len(pcm) % block_align:
        raise _GuideExecutionFailure("provider_wav_pcm_payload_invalid")
    frame_count = len(pcm) // block_align
    duration = frame_count / sample_rate
    if duration < 20.0 or duration > 50.0:
        raise _GuideExecutionFailure("provider_wav_duration_out_of_bounds")
    return {
        "container": "wav",
        "codec": "pcm_s16le",
        "sample_rate_hz": sample_rate,
        "channels": channels,
        "bit_depth": bits_per_sample,
        "frame_count": frame_count,
        "duration_seconds": duration,
    }


def _response_headers(value: Any) -> dict[str, str]:
    result: dict[str, str] = {}
    try:
        items = value.items()
    except Exception:
        return result
    for key, item in items:
        if isinstance(key, str) and isinstance(item, str):
            lowered = key.lower()
            if lowered in result and lowered in {
                "content-length",
                "content-type",
                "content-encoding",
            }:
                raise _GuideExecutionFailure("provider_response_headers_duplicated")
            result[lowered] = item
    return result


def _read_google_http_error_body(
    response: Any,
    headers: dict[str, str],
) -> tuple[bytes, str | None]:
    """Read one HTTP error body to EOF under the existing response ceiling.

    The raw bytes remain ephemeral.  A safe failure code is returned rather
    than raised so a provider exception cannot retain the response through an
    exception chain.
    """

    declared_length = headers.get("content-length")
    if declared_length is not None:
        if not declared_length.isascii() or not declared_length.isdigit():
            return b"", "provider_content_length_invalid"
        if int(declared_length) > GUIDE_MAX_RESPONSE_BYTES_PER_CALL:
            return b"", "provider_response_byte_cap_exceeded"

    chunks: list[bytes] = []
    received = 0
    failure_code: str | None = None
    try:
        while True:
            remaining = GUIDE_MAX_RESPONSE_BYTES_PER_CALL + 1 - received
            if remaining <= 0:
                failure_code = "provider_response_byte_cap_exceeded"
                break
            chunk = response.read(min(65_536, remaining))
            if not isinstance(chunk, bytes):
                failure_code = "provider_response_stream_invalid"
                break
            if not chunk:
                break
            chunks.append(chunk)
            received += len(chunk)
            if received > GUIDE_MAX_RESPONSE_BYTES_PER_CALL:
                failure_code = "provider_response_byte_cap_exceeded"
                break
    except Exception:
        failure_code = "provider_response_stream_invalid"

    raw = b"".join(chunks)
    chunks = []
    chunk = b""
    if failure_code is None and declared_length is not None and len(raw) != int(declared_length):
        failure_code = "provider_response_truncated"
    return raw, failure_code


def _safe_google_error_diagnostic(
    raw: bytes,
    headers: dict[str, str],
) -> dict[str, Any] | None:
    """Reduce a Google JSON error to explicitly allowlisted non-secret fields."""

    content_type = headers.get("content-type", "").split(";", 1)[0].strip().lower()
    content_encoding = headers.get("content-encoding", "identity").strip().lower()
    if not raw or content_type != "application/json" or content_encoding not in {"", "identity"}:
        return None
    try:
        payload = _strict_json_bytes(raw, "Google Cloud TTS error response")
    except ValidationError:
        return None
    if not isinstance(payload, dict) or not isinstance(payload.get("error"), dict):
        return None

    error = payload["error"]
    diagnostic: dict[str, Any] = {}
    code = error.get("code")
    if type(code) is int and 100 <= code <= 599:
        diagnostic["code"] = code
    status = error.get("status")
    if isinstance(status, str) and status in _GOOGLE_ERROR_STATUSES:
        diagnostic["status"] = status

    safe_details: list[dict[str, str]] = []
    details = error.get("details")
    if isinstance(details, list) and len(details) <= 32:
        for detail in details:
            if not isinstance(detail, dict) or detail.get("@type") != _GOOGLE_ERROR_INFO_TYPE:
                continue
            safe_detail: dict[str, str] = {}
            reason = detail.get("reason")
            if isinstance(reason, str) and reason in _GOOGLE_ERROR_INFO_REASONS:
                safe_detail["reason"] = reason
            domain = detail.get("domain")
            if isinstance(domain, str) and domain in _GOOGLE_ERROR_INFO_DOMAINS:
                safe_detail["domain"] = domain
            metadata = detail.get("metadata")
            if isinstance(metadata, dict):
                service = metadata.get("service")
                if isinstance(service, str) and service in _GOOGLE_ERROR_SERVICES:
                    safe_detail["service"] = service
                permission = metadata.get("permission")
                if isinstance(permission, str) and permission in _GOOGLE_ERROR_PERMISSIONS:
                    safe_detail["permission"] = permission
            if safe_detail and safe_detail not in safe_details:
                safe_details.append(safe_detail)
    if safe_details:
        diagnostic["error_info"] = safe_details
    return diagnostic or None


def _safe_provider_evidence(
    headers: dict[str, str],
    access_token: str,
    quota_project: str,
) -> tuple[dict[str, str], dict[str, int]]:
    identifiers: dict[str, str] = {}
    for name in ("x-goog-request-id", "x-request-id", "x-cloud-trace-context"):
        value = headers.get(name)
        if (
            isinstance(value, str)
            and 0 < len(value) <= 256
            and bool(re.fullmatch(r"[A-Za-z0-9._:/;=+\-]+", value))
            and not _SECRET_VALUE_RE.search(value)
            and access_token not in value
            and quota_project not in value
        ):
            identifiers[name] = value
    usage: dict[str, int] = {}
    for name in (
        "x-goog-quota-used",
        "x-ratelimit-limit",
        "x-ratelimit-remaining",
        "x-ratelimit-reset",
    ):
        value = headers.get(name)
        if isinstance(value, str) and value.isascii() and value.isdigit():
            number = int(value)
            if 0 <= number <= 10**15:
                usage[name] = number
    return identifiers, usage


def _perform_google_post(
    body: bytes,
    access_token: str,
    quota_project: str,
    timeout: float,
) -> _GoogleResponse:
    request: Any = None
    response: Any = None
    pending_failure: _GuideExecutionFailure | None = None
    status_getter: Any = None
    final_url_getter: Any = None
    close: Any = None
    headers: dict[str, str] = {}
    chunks: list[bytes] = []
    chunk = b""
    raw = b""
    payload: Any = None
    encoded = b""
    wav_bytes = b""
    geometry: Any = None
    content_type = ""
    content_encoding = ""
    error_raw = b""
    error_response_sha256: str | None = None
    error_diagnostic: dict[str, Any] | None = None
    error_read_failure: str | None = None
    if len(body) != GUIDE_MAX_REQUEST_BODY_BYTES or sha256_bytes(body) != GUIDE_REQUEST_BODY_SHA256:
        pending_failure = _GuideExecutionFailure("compiled_request_body_binding_failed")
    else:
        try:
            request = urllib.request.Request(GUIDE_ENDPOINT, data=body, method="POST")
            request.add_header("Authorization", f"Bearer {access_token}")
            request.add_header("Content-Type", "application/json")
            request.add_header("X-Goog-User-Project", quota_project)
            response = _open_google_request(request, timeout)
            status_getter = getattr(response, "getcode", None)
            status = status_getter() if callable(status_getter) else getattr(response, "status", None)
            headers = _response_headers(getattr(response, "headers", {}))
            identifiers, usage = _safe_provider_evidence(headers, access_token, quota_project)
            if type(status) is not int or status != 200:
                error_raw, error_read_failure = _read_google_http_error_body(response, headers)
                if error_read_failure in {None, "provider_response_truncated"}:
                    error_response_sha256 = sha256_bytes(error_raw)
                if error_read_failure is None:
                    error_diagnostic = _safe_google_error_diagnostic(error_raw, headers)
                raise _GuideExecutionFailure(
                    error_read_failure or "provider_http_failure",
                    http_status=status if type(status) is int else None,
                    response_bytes=len(error_raw),
                    response_sha256=error_response_sha256,
                    provider_error=error_diagnostic,
                    provider_identifiers=identifiers,
                    provider_usage=usage,
                )
            final_url_getter = getattr(response, "geturl", None)
            if not callable(final_url_getter) or final_url_getter() != GUIDE_ENDPOINT:
                raise _GuideExecutionFailure(
                    "provider_redirect_forbidden",
                    http_status=status,
                    provider_identifiers=identifiers,
                    provider_usage=usage,
                )
            content_type = headers.get("content-type", "").split(";", 1)[0].strip().lower()
            if content_type != "application/json":
                raise _GuideExecutionFailure(
                    "provider_response_mime_invalid",
                    http_status=status,
                    provider_identifiers=identifiers,
                    provider_usage=usage,
                )
            content_encoding = headers.get("content-encoding", "identity").strip().lower()
            if content_encoding not in {"", "identity"}:
                raise _GuideExecutionFailure(
                    "provider_response_encoding_forbidden",
                    http_status=status,
                    provider_identifiers=identifiers,
                    provider_usage=usage,
                )
            declared_length = headers.get("content-length")
            if declared_length is not None:
                if not declared_length.isascii() or not declared_length.isdigit():
                    raise _GuideExecutionFailure("provider_content_length_invalid")
                if int(declared_length) > GUIDE_MAX_RESPONSE_BYTES_PER_CALL:
                    raise _GuideExecutionFailure("provider_response_byte_cap_exceeded")
            received = 0
            while True:
                remaining = GUIDE_MAX_RESPONSE_BYTES_PER_CALL + 1 - received
                if remaining <= 0:
                    raise _GuideExecutionFailure("provider_response_byte_cap_exceeded")
                chunk = response.read(min(65_536, remaining))
                if not isinstance(chunk, bytes):
                    raise _GuideExecutionFailure("provider_response_stream_invalid")
                if not chunk:
                    break
                chunks.append(chunk)
                received += len(chunk)
                if received > GUIDE_MAX_RESPONSE_BYTES_PER_CALL:
                    raise _GuideExecutionFailure("provider_response_byte_cap_exceeded")
            raw = b"".join(chunks)
            if declared_length is not None and len(raw) != int(declared_length):
                raise _GuideExecutionFailure(
                    "provider_response_truncated",
                    response_bytes=len(raw),
                    provider_identifiers=identifiers,
                    provider_usage=usage,
                )
            try:
                payload = _strict_json_bytes(raw, "Google Cloud TTS response")
            except ValidationError:
                raise _GuideExecutionFailure(
                    "provider_response_json_invalid",
                    response_bytes=len(raw),
                    provider_identifiers=identifiers,
                    provider_usage=usage,
                ) from None
            if set(payload) != {"audioContent"} or not isinstance(payload.get("audioContent"), str) or not payload["audioContent"]:
                raise _GuideExecutionFailure(
                    "provider_audio_content_invalid",
                    response_bytes=len(raw),
                    provider_identifiers=identifiers,
                    provider_usage=usage,
                )
            try:
                encoded = payload["audioContent"].encode("ascii", errors="strict")
                wav_bytes = base64.b64decode(encoded, validate=True)
            except (UnicodeError, binascii.Error, ValueError):
                raise _GuideExecutionFailure(
                    "provider_audio_base64_invalid",
                    response_bytes=len(raw),
                    provider_identifiers=identifiers,
                    provider_usage=usage,
                ) from None
            if len(wav_bytes) > GUIDE_MAX_OUTPUT_WAV_BYTES:
                raise _GuideExecutionFailure(
                    "provider_wav_byte_cap_exceeded",
                    response_bytes=len(raw),
                    provider_identifiers=identifiers,
                    provider_usage=usage,
                )
            try:
                geometry = _validate_google_wav_bytes(wav_bytes)
            except _GuideExecutionFailure as exc:
                raise _GuideExecutionFailure(
                    exc.code,
                    response_bytes=len(raw),
                    provider_identifiers=identifiers,
                    provider_usage=usage,
                ) from None
            return _GoogleResponse(
                response_bytes=len(raw),
                response_sha256=sha256_bytes(raw),
                wav_bytes=wav_bytes,
                geometry=geometry,
                provider_identifiers=identifiers,
                provider_usage=usage,
            )
        except _GuideExecutionFailure as exc:
            exc.__cause__ = None
            exc.__context__ = None
            exc.__suppress_context__ = True
            pending_failure = exc
        except urllib.error.HTTPError as exc:
            try:
                try:
                    headers = _response_headers(exc.headers)
                    identifiers, usage = _safe_provider_evidence(headers, access_token, quota_project)
                    code = "provider_redirect_forbidden" if 300 <= exc.code < 400 else "provider_http_failure"
                    error_raw, error_read_failure = _read_google_http_error_body(exc, headers)
                    if error_read_failure in {None, "provider_response_truncated"}:
                        error_response_sha256 = sha256_bytes(error_raw)
                    if error_read_failure is None:
                        error_diagnostic = _safe_google_error_diagnostic(error_raw, headers)
                    pending_failure = _GuideExecutionFailure(
                        error_read_failure or code,
                        http_status=exc.code,
                        response_bytes=len(error_raw),
                        response_sha256=error_response_sha256,
                        provider_error=error_diagnostic,
                        provider_identifiers=identifiers,
                        provider_usage=usage,
                    )
                except _GuideExecutionFailure as header_failure:
                    pending_failure = _GuideExecutionFailure(header_failure.code)
            finally:
                try:
                    exc.close()
                except Exception:
                    pass
        except (urllib.error.URLError, TimeoutError, OSError):
            pending_failure = _GuideExecutionFailure("provider_transport_failure")
        except Exception:
            # Provider objects can carry credential-bearing headers. Never copy an
            # arbitrary exception or response body into an error or receipt.
            pending_failure = _GuideExecutionFailure("provider_transport_failure")
        finally:
            if response is not None:
                close = getattr(response, "close", None)
                if callable(close):
                    try:
                        close()
                    except Exception:
                        pass
    if pending_failure is None:
        raise _GuideExecutionFailure("provider_transport_failure") from None
    pending_failure.__cause__ = None
    pending_failure.__context__ = None
    pending_failure.__suppress_context__ = True
    # The raised redacted failure must not retain credentials or raw provider
    # material through traceback-frame locals inspected by a crash collector.
    body = b""
    access_token = ""
    quota_project = ""
    request = None
    response = None
    status_getter = None
    final_url_getter = None
    close = None
    headers = {}
    chunks = []
    chunk = b""
    raw = b""
    payload = None
    encoded = b""
    wav_bytes = b""
    geometry = None
    content_type = ""
    content_encoding = ""
    error_raw = b""
    error_response_sha256 = None
    error_diagnostic = None
    error_read_failure = None
    raise pending_failure from None


def _guide_authority_false_fields() -> dict[str, bool]:
    return {
        "creative_approved": False,
        "cross_provider_transfer_authorized": False,
        "voice_transfer_authorized": False,
        "full_capture_authorized": False,
        "step3_authorized": False,
        "publication_authorized": False,
    }


def execute_synthetic_guide(
    authorization_path: Path,
    plan_path: Path,
    canonical_w_path: Path,
    *,
    timeout: float = 60.0,
) -> dict[str, Any]:
    """Consume one exact AUTH-G1 and perform its two one-shot Google POSTs.

    No fallback, redirect, retry, alternate model, alternate voice, or resume is
    possible.  Quota-project and credential-source failures happen before any
    write.  Token refresh happens only after the immutable consumption record.
    """

    if not _is_number(timeout) or float(timeout) <= 0 or float(timeout) > 300:
        raise ValidationError("timeout must be greater than zero and at most 300 seconds")

    # Authority and every possible destination are proven before any private
    # quota-project or ADC material is accessed.
    contract = _build_guide_execution_contract(
        authorization_path,
        plan_path,
        canonical_w_path,
    )
    source_proof: dict[str, Any] = {}
    try:
        source_proof = _verify_guide_recovery_source(contract)
    except Exception:
        contract = None
        source_proof = {}
        raise ValidationError(
            "committed G1R2 source preflight failed before private access"
        ) from None
    quota_project = ""
    gcloud_executable = ""
    private_preflight_failed = False
    try:
        quota_project = _quota_project_for_execution(contract.authorization)
        gcloud_executable = _preflight_google_adc()
    except Exception:
        private_preflight_failed = True
    if private_preflight_failed:
        quota_project = ""
        gcloud_executable = ""
        contract = None
        raise ValidationError("private Google execution binding or ADC preflight failed") from None

    # Revalidate after private preflight and before the first write.  Any auth,
    # plan, W, or destination race remains non-consuming. The whole span is a
    # scrub boundary because it necessarily holds the private project value.
    setup_failed = False
    refreshed: _GuideExecutionContract | None = None
    consumed_at: datetime | None = None
    reserved_limits: dict[str, Any] = {}
    consumption: dict[str, Any] = {}
    consumption_bytes = b""
    consumption_sha256 = ""
    try:
        refreshed = _build_guide_execution_contract(
            authorization_path,
            plan_path,
            canonical_w_path,
        )
        if (
            refreshed.authorization_sha256 != contract.authorization_sha256
            or refreshed.dry_run["request_set_sha256"] != contract.dry_run["request_set_sha256"]
            or refreshed.root != contract.root
        ):
            raise ValidationError("AUTH-G1 execution bindings changed during preflight")
        contract = refreshed
        refreshed_source_proof = _verify_guide_recovery_source(contract)
        if not _json_exact(refreshed_source_proof, source_proof):
            raise ValidationError("committed G1R2 source proof changed during preflight")
        _ensure_execution_parents(
            contract.root,
            [
                contract.consumption_relative,
                contract.success_receipt_relative,
                contract.failure_receipt_relative,
                *[request["destination"] for request in contract.dry_run["requests"]],
            ],
        )
        _preflight_execution_paths(contract)
        if (
            sha256_file(contract.authorization_path) != contract.authorization_sha256
            or sha256_file(contract.plan_path) != contract.dry_run["plan_sha256"]
            or sha256_file(contract.canonical_w_path) != contract.dry_run["canonical_w_sha256"]
        ):
            raise ValidationError("AUTH-G1 execution bindings changed before consumption")

        consumed_at = _execution_now()
        if not contract.approved_at <= consumed_at < contract.expires_at:
            raise ValidationError("AUTH-G1 expired before authority consumption")
        reserved_limits = contract.authorization["authorized_limits"]
        recovery_consumption_fields = (
            {
                "authorization_path": contract.authorization_path.relative_to(
                    contract.root
                ).as_posix(),
                "authorization_schema_version": GUIDE_RECOVERY_AUTH_SCHEMA,
            }
            if contract.authorization.get("schema_version")
            == GUIDE_RECOVERY_AUTH_SCHEMA
            else {}
        )
        consumption = {
            "schema_version": (
                GUIDE_RECOVERY_CONSUMPTION_SCHEMA
                if recovery_consumption_fields
                else GUIDE_CONSUMPTION_SCHEMA
            ),
            "authorization_id": contract.authorization["authorization_id"],
            "authorization_sha256": contract.authorization_sha256,
            **recovery_consumption_fields,
            "scope": GUIDE_SCOPE,
            "provider": GUIDE_PROVIDER,
            "status": "consumed_before_network",
            "consumed_at": _iso_utc(consumed_at),
            "consumed_before_network": True,
            "network_called_at_consumption": False,
            "performance_transfer_plan_sha256": contract.dry_run["plan_sha256"],
            "request_set_sha256": contract.dry_run["request_set_sha256"],
            "reserved_limits": reserved_limits,
            "credentials_recorded": False,
        }
        consumption_bytes = _receipt_bytes(consumption)
        _exclusive_fixture_write(
            contract.root,
            contract.consumption_relative,
            consumption_bytes,
        )
        consumption_sha256 = sha256_bytes(consumption_bytes)
        _verify_private_fixture_artifact(
            contract.root,
            contract.consumption_relative,
            consumption_bytes,
            "AUTH-G1 consumption latch",
        )
    except Exception:
        setup_failed = True
    if setup_failed or contract is None or consumed_at is None:
        quota_project = ""
        gcloud_executable = ""
        contract = None
        refreshed = None
        consumed_at = None
        reserved_limits = {}
        consumption = {}
        consumption_bytes = b""
        consumption_sha256 = ""
        source_proof = {}
        raise ValidationError("AUTH-G1 execution setup failed closed before provider access") from None

    attempted_calls = 0
    total_request_bytes = 0
    total_response_bytes = 0
    modeled_spend = 0.0
    outputs: list[dict[str, Any]] = []
    run_started_at: datetime | None = None
    current_request_id: str | None = None
    current_identifiers: dict[str, str] = {}
    current_usage: dict[str, int] = {}
    current_http_status: int | None = None
    current_response_bytes = 0
    current_response_sha256: str | None = None
    current_provider_error: dict[str, Any] | None = None
    current_response_counted = False
    previous_call_completed_at: datetime | None = None
    credential_refresh_attempted = False
    final_failure_message: str | None = None

    def write_failure(reason_code: str) -> None:
        failed_at = _execution_now()
        failure = {
            "schema_version": GUIDE_FAILURE_RECEIPT_SCHEMA,
            "provider": GUIDE_PROVIDER,
            "endpoint": GUIDE_ENDPOINT,
            "model_id": GUIDE_MODEL,
            "voice_name": GUIDE_VOICE,
            "language_code": GUIDE_LANGUAGE,
            "outcome": "failed_closed",
            "reason_code": reason_code,
            "failed_request_id": current_request_id,
            "http_status": current_http_status,
            "authorization_id": contract.authorization["authorization_id"],
            "authorization_consumed": True,
            "guide_authorization_path": contract.authorization_path.relative_to(contract.root).as_posix(),
            "guide_authorization_sha256": contract.authorization_sha256,
            "guide_consumption_record_path": contract.consumption_relative,
            "guide_consumption_record_sha256": consumption_sha256,
            "performance_transfer_plan_sha256": contract.dry_run["plan_sha256"],
            "canonical_w_sha256": contract.dry_run["canonical_w_sha256"],
            "microtest_token_slice_sha256": MICROTEST_TOKEN_SLICE_SHA256,
            "spoken_text_sha256": MICROTEST_TEXT_SHA256,
            "acting_prompt_sha256": GUIDE_ACTING_PROMPT_SHA256,
            "request_set_sha256": contract.dry_run["request_set_sha256"],
            "request_body_sha256": GUIDE_REQUEST_BODY_SHA256,
            "request_body_bytes": GUIDE_MAX_REQUEST_BODY_BYTES,
            "total_request_bytes": total_request_bytes,
            "provider_calls_made": attempted_calls,
            "provider_outputs_received": len(outputs),
            "provider_response_bytes_total": total_response_bytes,
            "failed_response_bytes": current_response_bytes,
            "failed_response_sha256": current_response_sha256,
            "provider_error": current_provider_error,
            "provider_spend_usd": modeled_spend,
            "provider_spend_semantics": "modeled_authorized_ceiling_per_attempt_not_provider_invoice",
            "credential_mechanism": "gcloud_application_default_print_access_token",
            "credential_refresh_attempted": credential_refresh_attempted,
            "quota_project_sha256": contract.authorization["billing_project_binding"]["quota_project_sha256"],
            "provider_identifiers": current_identifiers,
            "provider_usage": current_usage,
            "outputs": outputs,
            "started_at": _iso_utc(run_started_at or consumed_at),
            "failed_at": _iso_utc(failed_at),
            "retries_made": 0,
            "redirects_followed": 0,
            "fallbacks_used": 0,
            "credentials_recorded": False,
            "network_called": credential_refresh_attempted or attempted_calls > 0,
            **_guide_authority_false_fields(),
        }
        secret_errors = _scan_for_secrets(failure, "synthetic_guide_failure_receipt")
        if secret_errors:
            raise ValidationError("refusing to serialize a credential-bearing guide failure receipt")
        _exclusive_fixture_write(
            contract.root,
            contract.failure_receipt_relative,
            _receipt_bytes(failure),
        )

    try:
        if not _json_exact(
            _verify_guide_recovery_source(
                contract,
                allow_consumption_latch=True,
            ),
            source_proof,
        ):
            raise _GuideExecutionFailure("committed_source_proof_changed_before_token_refresh")
        _verify_private_fixture_artifact(
            contract.root,
            contract.consumption_relative,
            consumption_bytes,
            "AUTH-G1 consumption latch",
        )
        credential_refresh_attempted = True
        access_token = _load_google_access_token(gcloud_executable, float(timeout))
        after_refresh = _execution_now()
        if after_refresh < consumed_at or after_refresh >= contract.expires_at:
            raise _GuideExecutionFailure("authorization_expired_after_token_refresh")

        for index, compiled in enumerate(contract.dry_run["requests"]):
            current_request_id = compiled["request_id"]
            current_identifiers = {}
            current_usage = {}
            current_http_status = None
            current_response_bytes = 0
            current_response_sha256 = None
            current_provider_error = None
            current_response_counted = False
            for existing_output in outputs:
                _verify_execution_output(contract.root, existing_output)
            _verify_private_fixture_artifact(
                contract.root,
                contract.consumption_relative,
                consumption_bytes,
                "AUTH-G1 consumption latch",
            )
            if current_request_id != f"gemini-guide-{index + 1:02d}":
                raise _GuideExecutionFailure("compiled_request_order_invalid")
            destination = compiled["destination"]
            _safe_execution_relative(
                contract.root,
                destination,
                f"{current_request_id} destination",
                ".wav",
            )
            _safe_execution_relative(
                contract.root,
                contract.success_receipt_relative,
                "guide success receipt",
                ".json",
            )
            _safe_execution_relative(
                contract.root,
                contract.failure_receipt_relative,
                "guide failure receipt",
                ".json",
            )
            body = _compact_json_bytes(compiled["request_body"])
            if (
                compiled["endpoint"] != GUIDE_ENDPOINT
                or compiled["method"] != "POST"
                or compiled["provider"] != GUIDE_PROVIDER
                or compiled["request_body_bytes"] != GUIDE_MAX_REQUEST_BODY_BYTES
                or compiled["request_body_sha256"] != GUIDE_REQUEST_BODY_SHA256
                or len(body) != GUIDE_MAX_REQUEST_BODY_BYTES
                or sha256_bytes(body) != GUIDE_REQUEST_BODY_SHA256
            ):
                raise _GuideExecutionFailure("compiled_request_binding_failed")
            next_calls = attempted_calls + 1
            next_request_bytes = total_request_bytes + len(body)
            next_spend = round(modeled_spend + GUIDE_MODELED_SPEND_PER_CALL_USD, 2)
            if (
                next_calls > reserved_limits["max_calls"]
                or next_calls > GUIDE_MAX_CALLS
                or next_request_bytes > reserved_limits["max_total_request_bytes"]
                or next_request_bytes > GUIDE_MAX_TOTAL_REQUEST_BYTES
                or next_spend > float(reserved_limits["max_spend_usd"]) + 1e-9
            ):
                raise _GuideExecutionFailure("authorization_ceiling_exhausted_before_network")
            if not _json_exact(
                _verify_guide_recovery_source(
                    contract,
                    allow_consumption_latch=True,
                ),
                source_proof,
            ):
                raise _GuideExecutionFailure("committed_source_proof_changed_before_provider_call")
            _verify_private_fixture_artifact(
                contract.root,
                contract.consumption_relative,
                consumption_bytes,
                "AUTH-G1 consumption latch",
            )
            call_started_at = _execution_now()
            if (
                call_started_at < consumed_at
                or (
                    previous_call_completed_at is not None
                    and call_started_at < previous_call_completed_at
                )
                or call_started_at >= contract.expires_at
            ):
                raise _GuideExecutionFailure("authorization_expired_before_provider_call")
            if run_started_at is None:
                run_started_at = call_started_at
            attempted_calls = next_calls
            total_request_bytes = next_request_bytes
            modeled_spend = next_spend
            response = _perform_google_post(
                body,
                access_token,
                quota_project,
                float(timeout),
            )
            call_completed_at = _execution_now()
            current_identifiers = response.provider_identifiers
            current_usage = response.provider_usage
            current_response_bytes = response.response_bytes
            total_response_bytes += response.response_bytes
            current_response_counted = True
            if call_completed_at < call_started_at or call_completed_at >= contract.expires_at:
                raise _GuideExecutionFailure(
                    "authorization_expired_before_provider_response_completed",
                    response_bytes=response.response_bytes,
                    provider_identifiers=response.provider_identifiers,
                    provider_usage=response.provider_usage,
                )
            next_audio_total = sum(item["byte_count"] for item in outputs) + len(response.wav_bytes)
            if (
                len(outputs) + 1 > reserved_limits["max_outputs"]
                or len(outputs) + 1 > GUIDE_MAX_OUTPUTS
                or len(response.wav_bytes) > reserved_limits["max_output_wav_bytes"]
                or next_audio_total > reserved_limits["max_total_audio_bytes"]
                or next_audio_total > GUIDE_MAX_TOTAL_AUDIO_BYTES
            ):
                raise _GuideExecutionFailure("authorization_audio_ceiling_exceeded")
            _safe_execution_relative(
                contract.root,
                destination,
                f"{current_request_id} destination",
                ".wav",
            )
            _exclusive_fixture_write(contract.root, destination, response.wav_bytes)
            output = {
                "request_id": current_request_id,
                "path": destination,
                "sha256": sha256_bytes(response.wav_bytes),
                "byte_count": len(response.wav_bytes),
                "duration_seconds": response.geometry["duration_seconds"],
                "provider_response_bytes": response.response_bytes,
                "response_sha256": response.response_sha256,
                "request_started_at": _iso_utc(call_started_at),
                "request_completed_at": _iso_utc(call_completed_at),
                "provider_identifiers": response.provider_identifiers,
                "provider_usage": response.provider_usage,
                "container": response.geometry["container"],
                "codec": response.geometry["codec"],
                "sample_rate_hz": response.geometry["sample_rate_hz"],
                "channels": response.geometry["channels"],
                "bit_depth": response.geometry["bit_depth"],
                "frame_count": response.geometry["frame_count"],
            }
            outputs.append(output)
            previous_call_completed_at = call_completed_at

        if attempted_calls != 2 or len(outputs) != 2 or total_request_bytes != GUIDE_MAX_TOTAL_REQUEST_BYTES:
            raise _GuideExecutionFailure("guide_execution_incomplete")
        for completed_output in outputs:
            _verify_execution_output(contract.root, completed_output)
        _verify_private_fixture_artifact(
            contract.root,
            contract.consumption_relative,
            consumption_bytes,
            "AUTH-G1 consumption latch",
        )
        completed_at = datetime.fromisoformat(outputs[-1]["request_completed_at"])
        if not contract.approved_at <= consumed_at <= (run_started_at or consumed_at) <= completed_at < contract.expires_at:
            raise _GuideExecutionFailure("guide_execution_time_order_invalid")
        success = {
            "schema_version": GUIDE_RUN_RECEIPT_SCHEMA,
            "provider": GUIDE_PROVIDER,
            "endpoint": GUIDE_ENDPOINT,
            "model_id": GUIDE_MODEL,
            "voice_name": GUIDE_VOICE,
            "language_code": GUIDE_LANGUAGE,
            "outcome": "success",
            "authorization_id": contract.authorization["authorization_id"],
            "authorization_consumed": True,
            "guide_authorization_path": contract.authorization_path.relative_to(contract.root).as_posix(),
            "guide_authorization_sha256": contract.authorization_sha256,
            "guide_consumption_record_path": contract.consumption_relative,
            "guide_consumption_record_sha256": consumption_sha256,
            "performance_transfer_plan_sha256": contract.dry_run["plan_sha256"],
            "canonical_w_sha256": contract.dry_run["canonical_w_sha256"],
            "microtest_token_slice_sha256": MICROTEST_TOKEN_SLICE_SHA256,
            "spoken_text_sha256": MICROTEST_TEXT_SHA256,
            "acting_prompt_sha256": GUIDE_ACTING_PROMPT_SHA256,
            "request_set_sha256": contract.dry_run["request_set_sha256"],
            "request_body_sha256": GUIDE_REQUEST_BODY_SHA256,
            "request_body_bytes": GUIDE_MAX_REQUEST_BODY_BYTES,
            "total_request_bytes": total_request_bytes,
            "provider_calls_made": attempted_calls,
            "provider_outputs_received": len(outputs),
            "provider_response_bytes_total": total_response_bytes,
            "provider_spend_usd": modeled_spend,
            "provider_spend_semantics": "modeled_authorized_ceiling_per_attempt_not_provider_invoice",
            "credential_mechanism": "gcloud_application_default_print_access_token",
            "credential_refresh_attempted": True,
            "quota_project_sha256": contract.authorization["billing_project_binding"]["quota_project_sha256"],
            "outputs": outputs,
            "started_at": _iso_utc(run_started_at or consumed_at),
            "completed_at": _iso_utc(completed_at),
            "retries_made": 0,
            "redirects_followed": 0,
            "fallbacks_used": 0,
            "credentials_recorded": False,
            "network_called": True,
            **_guide_authority_false_fields(),
        }
        secret_errors = _scan_for_secrets(success, "synthetic_guide_run_receipt")
        if secret_errors:
            raise _GuideExecutionFailure("receipt_secret_scan_failed")
        success_bytes = _receipt_bytes(success)
        _exclusive_fixture_write(
            contract.root,
            contract.success_receipt_relative,
            success_bytes,
        )
        return {
            "schema_version": "oe-synthetic-guide-execution-result-v1",
            "valid": True,
            "outcome": "success",
            "authorization_id": contract.authorization["authorization_id"],
            "authorization_consumed": True,
            "provider_calls_made": attempted_calls,
            "outputs_received": len(outputs),
            "run_receipt": {
                "path": contract.success_receipt_relative,
                "sha256": sha256_bytes(success_bytes),
            },
            "network_called": True,
            "credentials_accessed": True,
            **_guide_authority_false_fields(),
        }
    except _GuideExecutionFailure as exc:
        failed_response_was_counted = current_response_counted
        current_identifiers = exc.provider_identifiers or current_identifiers
        current_usage = exc.provider_usage or current_usage
        current_http_status = exc.http_status
        current_response_bytes = exc.response_bytes or current_response_bytes
        current_response_sha256 = exc.response_sha256 or current_response_sha256
        current_provider_error = exc.provider_error or current_provider_error
        if exc.response_bytes and not failed_response_was_counted:
            total_response_bytes += exc.response_bytes
        try:
            write_failure(exc.code)
            final_failure_message = (
                f"synthetic-guide execution stopped without retry: {exc.code}"
            )
        except ValidationError:
            final_failure_message = (
                "synthetic-guide execution stopped without retry: failure_receipt_write_failed"
            )
    except ValidationError:
        try:
            write_failure("local_validation_or_filesystem_failure")
            final_failure_message = (
                "synthetic-guide execution stopped without retry: local_validation_or_filesystem_failure"
            )
        except ValidationError:
            final_failure_message = (
                "synthetic-guide execution stopped without retry: failure_receipt_write_failed"
            )

    if final_failure_message is None:
        final_failure_message = "synthetic-guide execution stopped without retry: unknown_failure"
    quota_project = ""
    access_token = ""
    gcloud_executable = ""
    body = b""
    response = None
    compiled = {}
    output = {}
    outputs = []
    current_identifiers = {}
    current_usage = {}
    current_response_sha256 = None
    current_provider_error = None
    contract = None
    refreshed = None
    consumption = {}
    consumption_bytes = b""
    source_proof = {}
    success = {}
    success_bytes = b""
    write_failure = None
    raise ValidationError(final_failure_message) from None


def _read_bound_wav(
    path: Path,
    expected_bytes: int,
    expected_sha256: str,
    expected_duration: float,
) -> tuple[bytes, dict[str, Any]]:
    """Read one immutable descriptor and validate the exact original guide bytes."""

    flags = os.O_RDONLY
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    try:
        descriptor = os.open(path, flags)
    except OSError as exc:
        raise ValidationError("cannot safely open selected guide") from exc
    try:
        before = os.fstat(descriptor)
        if not stat.S_ISREG(before.st_mode):
            raise ValidationError("selected guide must be a regular file")
        if before.st_size != expected_bytes or before.st_size > GUIDE_MAX_OUTPUT_WAV_BYTES:
            raise ValidationError("selected guide byte count mismatch")
        with os.fdopen(descriptor, "rb", closefd=False) as handle:
            data = handle.read(GUIDE_MAX_OUTPUT_WAV_BYTES + 1)
        after = os.fstat(descriptor)
        if (
            before.st_dev,
            before.st_ino,
            before.st_size,
            before.st_mtime_ns,
        ) != (
            after.st_dev,
            after.st_ino,
            after.st_size,
            after.st_mtime_ns,
        ):
            raise ValidationError("selected guide changed while it was being read")
    finally:
        os.close(descriptor)
    if len(data) != expected_bytes or sha256_bytes(data) != expected_sha256:
        raise ValidationError("selected guide content binding mismatch")
    try:
        geometry = _validate_google_wav_bytes(data)
    except _GuideExecutionFailure as exc:
        if exc.code in {
            "provider_wav_payload_truncated_or_trailing",
            "provider_wav_chunk_header_truncated",
        }:
            message = "selected guide PCM payload is truncated or inconsistent with its WAV header"
        elif exc.code == "provider_wav_duration_out_of_bounds":
            message = "selected guide duration must be between 20 and 50 seconds"
        else:
            message = "selected guide is not an exact 24 kHz mono PCM WAV"
        raise ValidationError(message) from exc
    if abs(float(geometry["duration_seconds"]) - expected_duration) > 0.001:
        raise ValidationError("selected guide duration binding mismatch")
    return data, geometry


def _verified_prerequisite(
    root: Path,
    value: Any,
    label: str,
    *,
    expected_schema: str,
) -> tuple[Path, dict[str, Any]]:
    item = _strict_object(value, {"state", "path", "sha256"}, {"state", "path", "sha256"}, label)
    if item.get("state") != "verified":
        raise ValidationError(f"{label}.state must be verified")
    path = _safe_relative(root, item.get("path"), f"{label}.path", must_exist=True, suffix=".json")
    if not isinstance(item.get("sha256"), str) or not _SHA_RE.fullmatch(item["sha256"]) or sha256_file(path) != item["sha256"]:
        raise ValidationError(f"{label} SHA-256 mismatch")
    document = read_json(path)
    if document.get("schema_version") != expected_schema:
        raise ValidationError(f"{label} has the wrong schema")
    return path, document


def _compile_multipart_bytes(
    selected_audio: bytes,
    selected_sha: str,
    output_format: str,
    *,
    enable_logging: bool,
) -> tuple[dict[str, Any], bytes]:
    """Compile one exact deterministic multipart manifest and its bound body.

    Dry-run callers discard the returned body.  The separately authorized
    one-shot transfer executor sends these exact bytes without reconstructing
    the multipart request after authority validation.
    """

    boundary = f"oe-v05-{selected_sha[:32]}"
    delimiter = b"\r\n--" + boundary.encode("ascii")
    if delimiter in selected_audio or (b"--" + boundary.encode("ascii")) in selected_audio:
        raise ValidationError("selected guide collides with the deterministic multipart boundary")
    fields = [
        ("model_id", TRANSFER_MODEL),
        ("voice_settings", json.dumps(TRANSFER_VOICE_SETTINGS, sort_keys=True, separators=(",", ":"))),
        ("seed", str(TRANSFER_SEED)),
        ("remove_background_noise", "false"),
        ("file_format", "other"),
    ]
    chunks: list[bytes] = []
    for name, value in fields:
        chunks.extend(
            [
                f"--{boundary}\r\n".encode(),
                f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode(),
                value.encode("utf-8"),
                b"\r\n",
            ]
        )
    chunks.extend(
        [
            f"--{boundary}\r\n".encode(),
            b'Content-Disposition: form-data; name="audio"; filename="selected-guide.wav"\r\n',
            b"Content-Type: audio/wav\r\n\r\n",
            selected_audio,
            b"\r\n",
            f"--{boundary}--\r\n".encode(),
        ]
    )
    body = b"".join(chunks)
    query = {
        "enable_logging": "true" if enable_logging else "false",
        "output_format": output_format,
    }
    manifest = {
        "method": "POST",
        "endpoint": TRANSFER_ENDPOINT,
        "query": query,
        "content_type": f"multipart/form-data; boundary={boundary}",
        "multipart_body_bytes": len(body),
        "multipart_body_sha256": sha256_bytes(body),
        "source_audio_sha256": selected_sha,
        "fields": {
            "model_id": TRANSFER_MODEL,
            "voice_settings": TRANSFER_VOICE_SETTINGS,
            "seed": TRANSFER_SEED,
            "remove_background_noise": False,
            "file_format": "other",
        },
    }
    return manifest, body


def _compile_multipart(
    selected_audio: bytes,
    selected_sha: str,
    output_format: str,
    *,
    enable_logging: bool,
) -> dict[str, Any]:
    """Compile the existing review-only manifest without exposing body bytes."""

    manifest, _body = _compile_multipart_bytes(
        selected_audio,
        selected_sha,
        output_format,
        enable_logging=enable_logging,
    )
    return manifest


def _validate_consumed_guide_authority(
    root: Path,
    run_receipt: dict[str, Any],
    plan_dry: dict[str, Any],
    target: dict[str, Any],
    active_owner: str,
    errors: list[str],
) -> tuple[datetime | None, datetime | None, datetime | None]:
    """Bind a guide run to one exact G1 authority consumed before its first call."""

    guide_auth_path = _safe_relative(
        root,
        run_receipt.get("guide_authorization_path"),
        "guide run authorization path",
        must_exist=True,
        suffix=".json",
    )
    _require(
        guide_auth_path.relative_to(root).parts[0] == "authorizations",
        "guide authorization must remain under authorizations/",
        errors,
    )
    guide_auth, _guide_auth_bytes, guide_auth_sha256 = _read_bound_fixture_json(
        root,
        guide_auth_path,
        "consumed guide authorization",
    )
    _require(
        run_receipt.get("guide_authorization_sha256") == guide_auth_sha256,
        "guide authorization SHA-256 mismatch",
        errors,
    )
    guide_schema = guide_auth.get("schema_version")
    recovery_keys = (
        {"recovery_binding", "runtime_bindings"}
        if guide_schema == GUIDE_RECOVERY_AUTH_SCHEMA
        else set()
    )
    guide_authorization_keys = {
        "schema_version", "authorization_id", "status", "approved", "scope", "target",
        "bindings", "action", "billing_project_binding", "authorized_limits", "consumption",
        "approved_by", "approved_at", "expires_at", "execution_ready", "blockers",
        *recovery_keys,
    }
    _strict_object(
        guide_auth,
        guide_authorization_keys,
        guide_authorization_keys,
        "consumed guide authorization",
    )
    errors.extend(_scan_for_secrets(guide_auth, "consumed_guide_authorization"))
    _require(
        guide_schema in {GUIDE_AUTH_SCHEMA, GUIDE_RECOVERY_AUTH_SCHEMA},
        "consumed guide authorization schema mismatch",
        errors,
    )
    _require(guide_auth.get("authorization_id") == run_receipt.get("authorization_id"), "guide run authorization ID mismatch", errors)
    _require(guide_auth.get("status") == "active" and guide_auth.get("approved") is True, "guide authorization was not active and approved", errors)
    _require(guide_auth.get("scope") == GUIDE_SCOPE, "guide authorization scope mismatch", errors)
    _require(guide_auth.get("target") == target, "guide authorization target mismatch", errors)
    _require(guide_auth.get("approved_by") == active_owner, "guide and transfer authorizers must match", errors)
    _require(guide_auth.get("execution_ready") is True and guide_auth.get("blockers") == [], "guide authorization was not execution-ready", errors)
    expected_bindings = {
        "performance_transfer_plan_sha256": plan_dry["plan_sha256"],
        "canonical_w_sha256": plan_dry["canonical_w_sha256"],
        "microtest_token_slice_sha256": MICROTEST_TOKEN_SLICE_SHA256,
        "spoken_text_sha256": MICROTEST_TEXT_SHA256,
        "acting_prompt_sha256": GUIDE_ACTING_PROMPT_SHA256,
        "request_body_sha256": GUIDE_REQUEST_BODY_SHA256,
        "request_set_sha256": plan_dry["guide"]["request_set_sha256"],
    }
    _require(_json_exact(guide_auth.get("bindings"), expected_bindings), "consumed guide authorization bindings mismatch", errors)
    expected_action = {
        "provider": GUIDE_PROVIDER, "endpoint": GUIDE_ENDPOINT, "method": "POST", "model_id": GUIDE_MODEL,
        "voice_name": GUIDE_VOICE, "language_code": GUIDE_LANGUAGE, "request_count": 2,
        "identical_unseeded_requests": True, "output_encoding": "LINEAR16", "sample_rate_hz": 24000,
        "no_retry": True, "no_redirect": True, "no_fallback": True,
        "disclosure": "exact_locked_words_and_nonlexical_acting_prompt_to_google_cloud_tts",
    }
    _require(_json_exact(guide_auth.get("action"), expected_action), "consumed guide authorization action mismatch", errors)
    billing = guide_auth.get("billing_project_binding")
    _require(
        isinstance(billing, dict)
        and set(billing) == {"required", "raw_identifier_stored", "quota_project_sha256", "credential_source"}
        and billing.get("required") is True
        and billing.get("raw_identifier_stored") is False
        and isinstance(billing.get("quota_project_sha256"), str)
        and bool(_SHA_RE.fullmatch(billing["quota_project_sha256"]))
        and billing.get("credential_source") == "local_untracked_google_adc",
        "consumed guide authorization billing-project binding is invalid",
        errors,
    )
    if isinstance(billing, dict):
        _require(
            run_receipt.get("quota_project_sha256")
            == billing.get("quota_project_sha256"),
            "guide run quota-project binding mismatch",
            errors,
        )
    reserved_limits = {
        "max_calls": 2,
        "max_outputs": 2,
        "max_request_body_bytes": GUIDE_MAX_REQUEST_BODY_BYTES,
        "max_total_request_bytes": GUIDE_MAX_TOTAL_REQUEST_BYTES,
        "max_output_duration_seconds": GUIDE_MAX_OUTPUT_DURATION_SECONDS,
        "max_output_wav_bytes": GUIDE_MAX_OUTPUT_WAV_BYTES,
        "max_total_audio_bytes": GUIDE_MAX_TOTAL_AUDIO_BYTES,
        "max_response_bytes_per_call": GUIDE_MAX_RESPONSE_BYTES_PER_CALL,
        "max_spend_usd": GUIDE_MAX_SPEND_USD,
    }
    _require(_json_exact(guide_auth.get("authorized_limits"), reserved_limits), "consumed guide authorization limits mismatch", errors)
    if guide_schema == GUIDE_RECOVERY_AUTH_SCHEMA:
        recorded_runtime = _strict_object(
            guide_auth["runtime_bindings"],
            set(_expected_guide_runtime_bindings(draft=True)),
            set(_expected_guide_runtime_bindings(draft=True)),
            "consumed guide runtime_bindings",
        )
        expected_runtime_paths = _expected_guide_runtime_bindings(draft=True)
        for key, expected in expected_runtime_paths.items():
            if key.endswith("_path"):
                _require(
                    recorded_runtime.get(key) == expected,
                    f"consumed guide runtime_bindings.{key} drifted",
                    errors,
                )
            elif key == "git_commit":
                _require(
                    isinstance(recorded_runtime.get(key), str)
                    and bool(_GIT_SHA_RE.fullmatch(recorded_runtime[key])),
                    "consumed guide runtime commit is invalid",
                    errors,
                )
            else:
                _require(
                    isinstance(recorded_runtime.get(key), str)
                    and bool(_SHA_RE.fullmatch(recorded_runtime[key])),
                    f"consumed guide runtime_bindings.{key} is invalid",
                    errors,
                )
        _validate_guide_recovery_binding(
            root,
            guide_auth["recovery_binding"],
            dry={
                "plan_sha256": plan_dry["plan_sha256"],
                "canonical_w_sha256": plan_dry["canonical_w_sha256"],
                "request_set_sha256": plan_dry["guide"]["request_set_sha256"],
            },
            target=target,
        )
    guide_approved_at = _parse_time(guide_auth.get("approved_at"), "guide authorization approved_at", errors)
    guide_expires_at = _parse_time(guide_auth.get("expires_at"), "guide authorization expires_at", errors)
    if guide_approved_at and guide_expires_at:
        _require((guide_expires_at - guide_approved_at).total_seconds() <= 86_400, "guide authorization window exceeded 24 hours", errors)

    guide_consumption_path = _safe_relative(
        root,
        run_receipt.get("guide_consumption_record_path"),
        "guide consumption record path",
        must_exist=True,
        suffix=".json",
    )
    relative_consumption = guide_consumption_path.relative_to(root)
    _require(
        len(relative_consumption.parts) == 3
        and relative_consumption.parts[:2] == ("authorizations", "consumed")
        and relative_consumption.name
        == f"{guide_auth.get('authorization_id')}.consumed.json",
        "guide consumption record path is not authorization-ID-bound",
        errors,
    )
    guide_consumption, _guide_consumption_bytes, guide_consumption_sha256 = (
        _read_bound_fixture_json(
            root,
            guide_consumption_path,
            "guide consumption record",
        )
    )
    _require(
        run_receipt.get("guide_consumption_record_sha256")
        == guide_consumption_sha256,
        "guide consumption record SHA-256 mismatch",
        errors,
    )
    recovery_consumption_keys = (
        {"authorization_path", "authorization_schema_version"}
        if guide_schema == GUIDE_RECOVERY_AUTH_SCHEMA
        else set()
    )
    guide_consumption_keys = {
        "schema_version", "authorization_id", "authorization_sha256", "scope", "provider",
        "status", "consumed_at", "consumed_before_network", "network_called_at_consumption",
        "performance_transfer_plan_sha256", "request_set_sha256", "reserved_limits",
        "credentials_recorded", *recovery_consumption_keys,
    }
    _strict_object(
        guide_consumption,
        guide_consumption_keys,
        guide_consumption_keys,
        "guide consumption record",
    )
    expected_consumption_schema = (
        GUIDE_RECOVERY_CONSUMPTION_SCHEMA
        if guide_schema == GUIDE_RECOVERY_AUTH_SCHEMA
        else GUIDE_CONSUMPTION_SCHEMA
    )
    _require(guide_consumption.get("schema_version") == expected_consumption_schema, "guide consumption record schema mismatch", errors)
    if guide_schema == GUIDE_RECOVERY_AUTH_SCHEMA:
        _require(
            guide_consumption.get("authorization_path")
            == run_receipt.get("guide_authorization_path")
            and guide_consumption.get("authorization_schema_version")
            == GUIDE_RECOVERY_AUTH_SCHEMA,
            "guide recovery consumption does not bind the exact v2 authorization path",
            errors,
        )
    _require(guide_consumption.get("authorization_id") == guide_auth.get("authorization_id"), "guide consumption authorization ID mismatch", errors)
    _require(guide_consumption.get("authorization_sha256") == guide_auth_sha256, "guide consumption authorization hash mismatch", errors)
    _require(guide_consumption.get("scope") == GUIDE_SCOPE and guide_consumption.get("provider") == GUIDE_PROVIDER, "guide consumption scope/provider mismatch", errors)
    _require(guide_consumption.get("status") == "consumed_before_network", "guide authorization was not consumed before network", errors)
    _require(guide_consumption.get("consumed_before_network") is True and guide_consumption.get("network_called_at_consumption") is False, "guide consumption ordering assertion is invalid", errors)
    _require(guide_consumption.get("performance_transfer_plan_sha256") == plan_dry["plan_sha256"], "guide consumption plan mismatch", errors)
    _require(guide_consumption.get("request_set_sha256") == plan_dry["guide"]["request_set_sha256"], "guide consumption request set mismatch", errors)
    _require(_json_exact(guide_consumption.get("reserved_limits"), reserved_limits), "guide consumption reserved limits mismatch", errors)
    _require(guide_consumption.get("credentials_recorded") is False, "guide consumption record may not contain credentials", errors)
    guide_consumed_at = _parse_time(guide_consumption.get("consumed_at"), "guide authorization consumed_at", errors)
    auth_consumption = guide_auth.get("consumption")
    _require(
        isinstance(auth_consumption, dict)
        and set(auth_consumption)
        == {"status", "calls_used", "outputs_received", "spend_used_usd", "record_path"}
        and auth_consumption.get("status") == "unconsumed"
        and type(auth_consumption.get("calls_used")) is int
        and auth_consumption.get("calls_used") == 0
        and type(auth_consumption.get("outputs_received")) is int
        and auth_consumption.get("outputs_received") == 0
        and type(auth_consumption.get("spend_used_usd")) in {int, float}
        and auth_consumption.get("spend_used_usd") == 0
        and auth_consumption.get("record_path")
        == relative_consumption.as_posix(),
        "guide authorization does not bind its exact consumption record path",
        errors,
    )
    if guide_approved_at and guide_consumed_at and guide_expires_at:
        _require(guide_approved_at <= guide_consumed_at < guide_expires_at, "guide authorization was consumed outside its active window", errors)
    return guide_consumed_at, guide_approved_at, guide_expires_at


def dry_run_voice_transfer(
    plan_path: Path,
    canonical_w_path: Path,
    authorization_path: Path | None = None,
) -> dict[str, Any]:
    """Return a blocked manifest, or compile one exact authorized transfer request."""

    plan_dry = validate_performance_transfer_plan(plan_path, canonical_w_path)
    if authorization_path is None:
        return {
            "schema_version": "oe-elevenlabs-voice-transfer-dry-run-v1",
            "valid": True,
            "status": "blocked_pending_exact_selected_guide_chain",
            "plan_sha256": plan_dry["plan_sha256"],
            "blockers": plan_dry["voice_transfer"]["blockers"],
            "request_compiled": False,
            "provider_action_authorized": False,
            "network_authorized": False,
            "execution_transport_available": False,
            "network_called": False,
            "credentials_accessed": False,
            "audio_files_created": 0,
        }
    return validate_voice_transfer_authorization(authorization_path, plan_path, canonical_w_path)


def validate_voice_transfer_authorization(
    authorization_path: Path,
    plan_path: Path,
    canonical_w_path: Path,
) -> dict[str, Any]:
    """Validate the exact selected-guide chain and compile one Voice Changer POST."""

    authorization_path = Path(authorization_path).absolute()
    plan_path = Path(plan_path).absolute()
    authorization_root = _document_root(authorization_path)
    plan_root = _document_root(plan_path)
    if authorization_root != plan_root:
        raise ValidationError("voice-transfer authorization must live in the exact plan fixture root")
    authorization = read_json(authorization_path)
    _strict_object(
        authorization,
        {
            "schema_version", "authorization_id", "status", "approved", "scope", "target",
            "bindings", "prerequisites", "action", "authorized_limits", "consumption",
            "approved_by", "approved_at", "expires_at", "execution_ready", "blockers",
        },
        {
            "schema_version", "authorization_id", "status", "approved", "scope", "target",
            "bindings", "prerequisites", "action", "authorized_limits", "consumption",
            "approved_by", "approved_at", "expires_at", "execution_ready", "blockers",
        },
        "voice-transfer authorization",
    )
    plan_dry = validate_performance_transfer_plan(plan_path, canonical_w_path)
    plan = read_json(Path(plan_path))
    status, _ = _validate_common_authorization(
        authorization,
        authorization_path=authorization_path,
        schema=TRANSFER_AUTH_SCHEMA,
        scope=TRANSFER_SCOPE,
        target=plan["target"],
    )
    bindings = _strict_object(
        authorization.get("bindings"),
        {
            "performance_transfer_plan_sha256", "canonical_w_sha256", "spoken_text_sha256",
            "selected_guide_sha256", "primary_request_sha256", "primary_multipart_body_sha256",
            "primary_multipart_body_bytes", "conditional_fallback_request_sha256",
            "conditional_fallback_multipart_body_sha256", "conditional_fallback_multipart_body_bytes",
            "enable_logging",
        },
        {"performance_transfer_plan_sha256", "canonical_w_sha256", "spoken_text_sha256"},
        "bindings",
    )
    errors: list[str] = []
    for key, expected in {
        "performance_transfer_plan_sha256": plan_dry["plan_sha256"],
        "canonical_w_sha256": plan_dry["canonical_w_sha256"],
        "spoken_text_sha256": MICROTEST_TEXT_SHA256,
    }.items():
        _require(_json_exact(bindings.get(key), expected), f"voice-transfer bindings.{key} mismatch", errors)
    if status == "draft":
        _require(
            set(bindings)
            == {"performance_transfer_plan_sha256", "canonical_w_sha256", "spoken_text_sha256"},
            "draft voice-transfer bindings may not pre-authorize an unknown multipart body",
            errors,
        )
    action = _strict_object(
        authorization.get("action"),
        {
            "provider", "endpoint", "method", "target_voice_id", "model_id", "seed", "query_policy",
            "voice_settings", "remove_background_noise", "file_format", "primary_output_format",
            "conditional_fallback_output_format", "fallback_requires_documented_pcm_capability_rejection",
            "no_retry", "no_redirect", "disclosure",
        },
        {
            "provider", "endpoint", "method", "target_voice_id", "model_id", "seed", "query_policy",
            "voice_settings", "remove_background_noise", "file_format", "primary_output_format",
            "conditional_fallback_output_format", "fallback_requires_documented_pcm_capability_rejection",
            "no_retry", "no_redirect", "disclosure",
        },
        "action",
    )
    expected_action = {
        "provider": "elevenlabs", "endpoint": TRANSFER_ENDPOINT, "method": "POST",
        "target_voice_id": TRANSFER_TARGET_VOICE_ID, "model_id": TRANSFER_MODEL, "seed": TRANSFER_SEED,
        "query_policy": {
            "enable_logging": "false_for_zrm_otherwise_true_only_with_account_training_opt_out",
            "output_format": TRANSFER_PRIMARY_FORMAT,
        },
        "voice_settings": TRANSFER_VOICE_SETTINGS, "remove_background_noise": False, "file_format": "other",
        "primary_output_format": TRANSFER_PRIMARY_FORMAT,
        "conditional_fallback_output_format": TRANSFER_FALLBACK_FORMAT,
        "fallback_requires_documented_pcm_capability_rejection": True,
        "no_retry": True, "no_redirect": True,
        "disclosure": "one_exact_owner_selected_google_guide_to_elevenlabs_voice_changer",
    }
    _require(_json_exact(action, expected_action), "voice-transfer action drifted", errors)
    limits = _strict_object(
        authorization.get("authorized_limits"),
        {"max_calls", "max_outputs", "max_source_bytes", "max_source_duration_seconds", "max_submitted_seconds", "max_spend_usd"},
        {"max_calls", "max_outputs", "max_source_bytes", "max_source_duration_seconds", "max_submitted_seconds", "max_spend_usd"},
        "authorized_limits",
    )
    expected_limits = (
        {
            "max_calls": TRANSFER_MAX_CALLS,
            "max_outputs": TRANSFER_MAX_OUTPUTS,
            "max_source_bytes": TRANSFER_MAX_SOURCE_BYTES,
            "max_source_duration_seconds": TRANSFER_MAX_SOURCE_DURATION_SECONDS,
            "max_submitted_seconds": TRANSFER_MAX_SUBMITTED_SECONDS,
            "max_spend_usd": TRANSFER_MAX_SPEND_USD,
        }
        if status == "active"
        else {"max_calls": 0, "max_outputs": 0, "max_source_bytes": 0, "max_source_duration_seconds": 0, "max_submitted_seconds": 0, "max_spend_usd": 0}
    )
    _require(_json_exact(limits, expected_limits), "voice-transfer authorized limits do not match authorization status", errors)
    prerequisites = _strict_object(
        authorization.get("prerequisites"),
        {"selected_guide", "guide_qa", "owner_selection", "elevenlabs_data_use", "target_voice_rights"},
        {"selected_guide", "guide_qa", "owner_selection", "elevenlabs_data_use", "target_voice_rights"},
        "prerequisites",
    )
    if status == "draft":
        for name, value in prerequisites.items():
            if not isinstance(value, dict) or value != {"state": "pending"}:
                errors.append(f"draft prerequisites.{name} must be exactly pending")
        if errors:
            raise ValidationError(errors)
        return {
            "schema_version": "oe-elevenlabs-voice-transfer-dry-run-v1",
            "valid": True,
            "status": "blocked_pending_exact_selected_guide_chain",
            "authorization_id": authorization["authorization_id"],
            "authorization_sha256": sha256_file(authorization_path),
            "plan_sha256": plan_dry["plan_sha256"],
            "blockers": authorization["blockers"],
            "request_compiled": False,
            "provider_action_authorized": False,
            "network_authorized": False,
            "execution_transport_available": False,
            "network_called": False,
            "credentials_accessed": False,
            "audio_files_created": 0,
        }
    if errors:
        raise ValidationError(errors)

    root = _document_root(authorization_path)
    active_approved_at = _parse_time(
        authorization.get("approved_at"),
        "active voice-transfer approved_at",
        errors,
    )
    selected = _strict_object(
        prerequisites.get("selected_guide"),
        {
            "state", "path", "sha256", "byte_count", "duration_seconds", "container", "codec",
            "sample_rate_hz", "channels", "guide_request_id", "guide_run_receipt_path", "guide_run_receipt_sha256",
        },
        {
            "state", "path", "sha256", "byte_count", "duration_seconds", "container", "codec",
            "sample_rate_hz", "channels", "guide_request_id", "guide_run_receipt_path", "guide_run_receipt_sha256",
        },
        "prerequisites.selected_guide",
    )
    _require(selected.get("state") == "verified", "selected guide must be verified", errors)
    selected_path = _safe_relative(root, selected.get("path"), "selected guide path", must_exist=True, suffix=".wav")
    _require(
        selected_path.relative_to(root).parts[:3] == ("outputs", "raw", "google"),
        "selected guide must be the original Google provider WAV under outputs/raw/google/",
        errors,
    )
    selected_sha = selected.get("sha256")
    _require(isinstance(selected_sha, str) and bool(_SHA_RE.fullmatch(selected_sha)), "selected guide SHA-256 is invalid", errors)
    _require(type(selected.get("byte_count")) is int and 0 < selected["byte_count"] <= TRANSFER_MAX_SOURCE_BYTES, "selected guide byte count is invalid", errors)
    _require(_is_number(selected.get("duration_seconds")) and 20.0 <= float(selected["duration_seconds"]) <= 50.0, "selected guide duration declaration must be between 20 and 50 seconds", errors)
    _require(selected.get("container") == "wav" and selected.get("codec") == "pcm_s16le", "selected guide format declaration is invalid", errors)
    _require(_json_exact((selected.get("sample_rate_hz"), selected.get("channels")), (24000, 1)), "selected guide geometry declaration is invalid", errors)
    _require(selected.get("guide_request_id") in {"gemini-guide-01", "gemini-guide-02"}, "selected guide request ID is not in the compiled set", errors)
    compiled_guide_destinations = {
        request["request_id"]: request["destination"]
        for request in plan_dry["guide"]["requests"]
    }
    selected_relative = selected_path.relative_to(root).as_posix()
    _require(
        compiled_guide_destinations.get(selected.get("guide_request_id"))
        == selected_relative,
        "selected guide path does not equal its compiled request destination",
        errors,
    )
    selected_audio = b""
    if not errors:
        selected_audio, _selected_geometry = _read_bound_wav(
            selected_path,
            selected["byte_count"],
            selected_sha,
            float(selected["duration_seconds"]),
        )

    run_binding = {"state": "verified", "path": selected.get("guide_run_receipt_path"), "sha256": selected.get("guide_run_receipt_sha256")}
    _run_path, run_receipt = _verified_prerequisite(root, run_binding, "selected guide run receipt", expected_schema="oe-synthetic-guide-run-receipt-v1")
    _strict_object(
        run_receipt,
        {
            "schema_version", "provider", "endpoint", "model_id", "voice_name", "language_code",
            "outcome", "authorization_id", "authorization_consumed", "outputs",
            "guide_authorization_path", "guide_authorization_sha256",
            "guide_consumption_record_path", "guide_consumption_record_sha256",
            "performance_transfer_plan_sha256", "canonical_w_sha256",
            "microtest_token_slice_sha256", "spoken_text_sha256", "acting_prompt_sha256",
            "request_set_sha256", "request_body_sha256", "request_body_bytes",
            "total_request_bytes", "provider_calls_made", "provider_outputs_received",
            "provider_response_bytes_total", "provider_spend_usd", "provider_spend_semantics",
            "credential_mechanism", "credential_refresh_attempted", "quota_project_sha256", "started_at", "completed_at",
            "retries_made", "redirects_followed", "fallbacks_used", "credentials_recorded",
            "network_called", "creative_approved", "cross_provider_transfer_authorized",
            "voice_transfer_authorized", "full_capture_authorized", "step3_authorized",
            "publication_authorized",
        },
        {
            "schema_version", "provider", "endpoint", "model_id", "voice_name", "language_code",
            "outcome", "authorization_id", "authorization_consumed", "outputs",
            "guide_authorization_path", "guide_authorization_sha256",
            "guide_consumption_record_path", "guide_consumption_record_sha256",
            "performance_transfer_plan_sha256", "canonical_w_sha256",
            "microtest_token_slice_sha256", "spoken_text_sha256", "acting_prompt_sha256",
            "request_set_sha256", "request_body_sha256", "request_body_bytes",
            "total_request_bytes", "provider_calls_made", "provider_outputs_received",
            "provider_response_bytes_total", "provider_spend_usd", "provider_spend_semantics",
            "credential_mechanism", "credential_refresh_attempted", "quota_project_sha256", "started_at", "completed_at",
            "retries_made", "redirects_followed", "fallbacks_used", "credentials_recorded",
            "network_called", "creative_approved", "cross_provider_transfer_authorized",
            "voice_transfer_authorized", "full_capture_authorized", "step3_authorized",
            "publication_authorized",
        },
        "selected guide run receipt",
    )
    errors.extend(_scan_for_secrets(run_receipt, "selected_guide_run_receipt"))
    _require(
        _json_exact(
            (
                run_receipt.get("provider"), run_receipt.get("endpoint"),
                run_receipt.get("model_id"), run_receipt.get("voice_name"),
                run_receipt.get("language_code"), run_receipt.get("outcome"),
            ),
            (GUIDE_PROVIDER, GUIDE_ENDPOINT, GUIDE_MODEL, GUIDE_VOICE, GUIDE_LANGUAGE, "success"),
        ),
        "guide run receipt must record the exact successful Google generation",
        errors,
    )
    _require(run_receipt.get("performance_transfer_plan_sha256") == plan_dry["plan_sha256"], "guide run receipt plan mismatch", errors)
    _require(run_receipt.get("canonical_w_sha256") == plan_dry["canonical_w_sha256"], "guide run receipt canonical W mismatch", errors)
    _require(run_receipt.get("microtest_token_slice_sha256") == MICROTEST_TOKEN_SLICE_SHA256, "guide run receipt token-slice mismatch", errors)
    _require(run_receipt.get("spoken_text_sha256") == MICROTEST_TEXT_SHA256, "guide run receipt spoken-text mismatch", errors)
    _require(run_receipt.get("acting_prompt_sha256") == GUIDE_ACTING_PROMPT_SHA256, "guide run receipt acting-prompt mismatch", errors)
    _require(run_receipt.get("request_set_sha256") == plan_dry["guide"]["request_set_sha256"], "guide run receipt request set mismatch", errors)
    _require(run_receipt.get("request_body_sha256") == GUIDE_REQUEST_BODY_SHA256, "guide run receipt body mismatch", errors)
    _require(type(run_receipt.get("request_body_bytes")) is int and run_receipt["request_body_bytes"] == GUIDE_MAX_REQUEST_BODY_BYTES, "guide run receipt request-body byte count mismatch", errors)
    _require(type(run_receipt.get("total_request_bytes")) is int and run_receipt["total_request_bytes"] == GUIDE_MAX_TOTAL_REQUEST_BYTES, "guide run receipt total request-byte count mismatch", errors)
    _require(type(run_receipt.get("provider_calls_made")) is int and run_receipt["provider_calls_made"] == 2, "guide run receipt must record exactly two provider calls", errors)
    _require(type(run_receipt.get("provider_outputs_received")) is int and run_receipt["provider_outputs_received"] == 2, "guide run receipt must record exactly two provider outputs", errors)
    _require(type(run_receipt.get("provider_response_bytes_total")) is int and 0 < run_receipt["provider_response_bytes_total"] <= 2 * GUIDE_MAX_RESPONSE_BYTES_PER_CALL, "guide run receipt total response-byte count is invalid", errors)
    _require(
        _is_number(run_receipt.get("provider_spend_usd"))
        and float(run_receipt["provider_spend_usd"]) == GUIDE_MAX_SPEND_USD,
        "guide run receipt modeled spend mismatch",
        errors,
    )
    _require(run_receipt.get("provider_spend_semantics") == "modeled_authorized_ceiling_per_attempt_not_provider_invoice", "guide run receipt spend semantics mismatch", errors)
    _require(run_receipt.get("credential_mechanism") == "gcloud_application_default_print_access_token", "guide run receipt credential mechanism mismatch", errors)
    _require(run_receipt.get("credential_refresh_attempted") is True, "guide run receipt must record the consumed credential refresh", errors)
    _require(run_receipt.get("authorization_consumed") is True, "guide authorization must have been consumed", errors)
    _require(
        all(
            run_receipt.get(key) is False
            for key in (
                "creative_approved", "cross_provider_transfer_authorized",
                "voice_transfer_authorized", "full_capture_authorized",
                "step3_authorized", "publication_authorized",
            )
        ),
        "guide receipt may not authorize creative approval or downstream production",
        errors,
    )
    _require(
        run_receipt.get("retries_made") == 0
        and type(run_receipt.get("retries_made")) is int
        and run_receipt.get("redirects_followed") == 0
        and type(run_receipt.get("redirects_followed")) is int
        and run_receipt.get("fallbacks_used") == 0
        and type(run_receipt.get("fallbacks_used")) is int
        and run_receipt.get("credentials_recorded") is False
        and run_receipt.get("network_called") is True,
        "guide receipt transport controls are invalid",
        errors,
    )
    guide_started_at = _parse_time(
        run_receipt.get("started_at"),
        "guide run started_at",
        errors,
    )
    guide_completed_at = _parse_time(
        run_receipt.get("completed_at"),
        "guide run completed_at",
        errors,
    )
    guide_consumed_at, guide_approved_at, guide_expires_at = _validate_consumed_guide_authority(
        root,
        run_receipt,
        plan_dry,
        plan["target"],
        str(authorization.get("approved_by")),
        errors,
    )
    if (
        guide_approved_at
        and guide_consumed_at
        and guide_started_at
        and guide_completed_at
        and guide_expires_at
    ):
        _require(
            guide_approved_at
            <= guide_consumed_at
            <= guide_started_at
            <= guide_completed_at
            < guide_expires_at,
            "guide generation must start and finish inside the consumed G1 authorization window",
            errors,
        )
    outputs = run_receipt.get("outputs")
    if not isinstance(outputs, list) or len(outputs) != 2:
        errors.append("guide run receipt must contain exactly two outputs")
        outputs = []
    else:
        output_ids: list[Any] = []
        declared_total_audio_bytes = 0
        output_times: list[tuple[datetime, datetime]] = []
        for index, entry in enumerate(outputs):
            try:
                item = _strict_object(
                    entry,
                    {
                        "request_id", "path", "sha256", "byte_count", "duration_seconds",
                        "provider_response_bytes", "response_sha256", "request_started_at",
                        "request_completed_at", "provider_identifiers", "provider_usage",
                        "container", "codec", "sample_rate_hz", "channels", "bit_depth", "frame_count",
                    },
                    {
                        "request_id", "path", "sha256", "byte_count", "duration_seconds",
                        "provider_response_bytes", "response_sha256", "request_started_at",
                        "request_completed_at", "provider_identifiers", "provider_usage",
                        "container", "codec", "sample_rate_hz", "channels", "bit_depth", "frame_count",
                    },
                    f"guide run receipt outputs[{index}]",
                )
                output_ids.append(item.get("request_id"))
                _require(item.get("request_id") in {"gemini-guide-01", "gemini-guide-02"}, f"guide output {index} request ID is invalid", errors)
                _require(
                    compiled_guide_destinations.get(item.get("request_id"))
                    == item.get("path"),
                    f"guide output {index} path does not equal its compiled destination",
                    errors,
                )
                _require(isinstance(item.get("sha256"), str) and bool(_SHA_RE.fullmatch(item["sha256"])), f"guide output {index} SHA-256 is invalid", errors)
                byte_count = item.get("byte_count")
                _require(
                    type(byte_count) is int
                    and 0 < byte_count <= GUIDE_MAX_OUTPUT_WAV_BYTES,
                    f"guide output {index} exceeds its WAV-byte authority",
                    errors,
                )
                if type(byte_count) is int and byte_count > 0:
                    declared_total_audio_bytes += byte_count
                _require(
                    _is_number(item.get("duration_seconds"))
                    and 0 < float(item["duration_seconds"]) <= GUIDE_MAX_OUTPUT_DURATION_SECONDS,
                    f"guide output {index} exceeds its duration authority",
                    errors,
                )
                _require(
                    type(item.get("provider_response_bytes")) is int
                    and 0 < item["provider_response_bytes"] <= GUIDE_MAX_RESPONSE_BYTES_PER_CALL,
                    f"guide output {index} exceeds its provider-response authority",
                    errors,
                )
                _require(isinstance(item.get("response_sha256"), str) and bool(_SHA_RE.fullmatch(item["response_sha256"])), f"guide output {index} response hash is invalid", errors)
                output_started_at = _parse_time(item.get("request_started_at"), f"guide output {index} request_started_at", errors)
                output_completed_at = _parse_time(item.get("request_completed_at"), f"guide output {index} request_completed_at", errors)
                if output_started_at and output_completed_at:
                    _require(output_started_at <= output_completed_at, f"guide output {index} request time order is invalid", errors)
                    output_times.append((output_started_at, output_completed_at))
                identifiers = item.get("provider_identifiers")
                _require(
                    isinstance(identifiers, dict)
                    and set(identifiers).issubset({"x-goog-request-id", "x-request-id", "x-cloud-trace-context"})
                    and all(
                        isinstance(value, str)
                        and 0 < len(value) <= 256
                        and all(32 <= ord(character) <= 126 for character in value)
                        for value in identifiers.values()
                    ),
                    f"guide output {index} provider identifiers are invalid",
                    errors,
                )
                usage = item.get("provider_usage")
                _require(
                    isinstance(usage, dict)
                    and set(usage).issubset({"x-goog-quota-used", "x-ratelimit-limit", "x-ratelimit-remaining", "x-ratelimit-reset"})
                    and all(type(value) is int and 0 <= value <= 10**15 for value in usage.values()),
                    f"guide output {index} provider usage is invalid",
                    errors,
                )
                _require(
                    _json_exact(
                        (item.get("container"), item.get("codec"), item.get("sample_rate_hz"), item.get("channels"), item.get("bit_depth")),
                        ("wav", "pcm_s16le", 24000, 1, 16),
                    ),
                    f"guide output {index} media geometry is invalid",
                    errors,
                )
                _require(type(item.get("frame_count")) is int and item["frame_count"] > 0, f"guide output {index} frame count is invalid", errors)
                output_path = _safe_relative(
                    root,
                    item.get("path"),
                    f"guide run receipt outputs[{index}].path",
                    must_exist=True,
                    suffix=".wav",
                )
                if (
                    type(byte_count) is int
                    and byte_count > 0
                    and isinstance(item.get("sha256"), str)
                    and bool(_SHA_RE.fullmatch(item["sha256"]))
                    and _is_number(item.get("duration_seconds"))
                ):
                    _read_bound_wav(
                        output_path,
                        byte_count,
                        item["sha256"],
                        float(item["duration_seconds"]),
                    )
            except ValidationError as exc:
                errors.extend(exc.errors)
        _require(set(output_ids) == {"gemini-guide-01", "gemini-guide-02"}, "guide run receipt output set is incomplete", errors)
        _require(
            declared_total_audio_bytes <= GUIDE_MAX_TOTAL_AUDIO_BYTES,
            "guide run receipt exceeds total audio-byte authority",
            errors,
        )
        _require(
            sum(
                entry.get("provider_response_bytes", 0)
                for entry in outputs
                if isinstance(entry, dict) and type(entry.get("provider_response_bytes")) is int
            )
            == run_receipt.get("provider_response_bytes_total"),
            "guide run receipt response-byte total does not match its outputs",
            errors,
        )
        if len(output_times) == 2:
            _require(
                output_times[0][1] <= output_times[1][0],
                "guide provider calls overlap or run out of order",
                errors,
            )
            if guide_started_at and guide_completed_at:
                _require(
                    output_times[0][0] == guide_started_at
                    and output_times[-1][1] == guide_completed_at,
                    "guide run top-level times do not bind its exact provider calls",
                    errors,
                )
    matching = [] if not isinstance(outputs, list) else [
        entry
        for entry in outputs
        if isinstance(entry, dict)
        and entry.get("request_id") == selected.get("guide_request_id")
        and entry.get("sha256") == selected_sha
        and entry.get("path") == selected_relative
        and _json_exact(entry.get("byte_count"), selected.get("byte_count"))
        and _json_exact(entry.get("duration_seconds"), selected.get("duration_seconds"))
        and entry.get("container") == selected.get("container")
        and entry.get("codec") == selected.get("codec")
        and _json_exact(entry.get("sample_rate_hz"), selected.get("sample_rate_hz"))
        and _json_exact(entry.get("channels"), selected.get("channels"))
    ]
    _require(len(matching) == 1, "selected guide is not bound to exactly one guide run output", errors)

    qa_path, qa = _verified_prerequisite(root, prerequisites.get("guide_qa"), "prerequisites.guide_qa", expected_schema="oe-synthetic-guide-qa-v1")
    _strict_object(
        qa,
        {
            "schema_version", "selected_guide_sha256", "spoken_text_sha256", "lexical_exact",
            "technical_pass", "performance_pass", "understandable_without_music_or_visuals",
            "reviewed_by", "reviewed_at",
        },
        {
            "schema_version", "selected_guide_sha256", "spoken_text_sha256", "lexical_exact",
            "technical_pass", "performance_pass", "understandable_without_music_or_visuals",
            "reviewed_by", "reviewed_at",
        },
        "guide QA receipt",
    )
    _require(qa.get("selected_guide_sha256") == selected_sha, "guide QA selected-guide hash mismatch", errors)
    _require(qa.get("spoken_text_sha256") == MICROTEST_TEXT_SHA256, "guide QA spoken-text hash mismatch", errors)
    for key in ("lexical_exact", "technical_pass", "performance_pass", "understandable_without_music_or_visuals"):
        _require(qa.get(key) is True, f"guide QA requires {key}=true", errors)
    _require(isinstance(qa.get("reviewed_by"), str) and bool(qa["reviewed_by"]), "guide QA reviewer is required", errors)
    qa_reviewed_at = _parse_time(qa.get("reviewed_at"), "guide QA reviewed_at", errors)

    selection_path, selection = _verified_prerequisite(root, prerequisites.get("owner_selection"), "prerequisites.owner_selection", expected_schema="oe-synthetic-guide-owner-selection-v1")
    _strict_object(
        selection,
        {"schema_version", "selected_guide_sha256", "guide_qa_sha256", "selected_by", "selected_at", "approved_for_voice_transfer"},
        {"schema_version", "selected_guide_sha256", "guide_qa_sha256", "selected_by", "selected_at", "approved_for_voice_transfer"},
        "guide owner-selection receipt",
    )
    _require(selection.get("selected_guide_sha256") == selected_sha, "owner selection guide hash mismatch", errors)
    _require(selection.get("guide_qa_sha256") == sha256_file(qa_path), "owner selection QA hash mismatch", errors)
    _require(selection.get("approved_for_voice_transfer") is True, "owner did not approve the exact guide for voice transfer", errors)
    _require(selection.get("selected_by") == authorization.get("approved_by"), "guide owner selection must match the active authorizer", errors)
    guide_selected_at = _parse_time(
        selection.get("selected_at"),
        "guide owner selection selected_at",
        errors,
    )

    data_path, data_use = _verified_prerequisite(root, prerequisites.get("elevenlabs_data_use"), "prerequisites.elevenlabs_data_use", expected_schema="oe-elevenlabs-data-use-assurance-v1")
    _strict_object(
        data_use,
        {
            "schema_version", "provider", "exact_guide_sha256", "cross_provider_upload_permitted",
            "improve_models_for_everyone", "zero_retention_mode", "chosen_enable_logging",
            "protection_mode", "opt_out_processed", "protection_effective_for_new_submissions",
            "zrm_eligible_and_confirmed",
            "account_scope_binding_sha256", "verified_by", "verified_at", "evidence",
        },
        {
            "schema_version", "provider", "exact_guide_sha256", "cross_provider_upload_permitted",
            "improve_models_for_everyone", "zero_retention_mode", "chosen_enable_logging",
            "protection_mode", "opt_out_processed", "protection_effective_for_new_submissions",
            "zrm_eligible_and_confirmed",
            "account_scope_binding_sha256", "verified_by", "verified_at", "evidence",
        },
        "ElevenLabs data-use assurance",
    )
    _require(data_use.get("provider") == "elevenlabs", "data-use assurance provider mismatch", errors)
    _require(data_use.get("exact_guide_sha256") == selected_sha, "data-use assurance guide hash mismatch", errors)
    _require(data_use.get("cross_provider_upload_permitted") is True, "cross-provider upload is not permitted", errors)
    _require(isinstance(data_use.get("improve_models_for_everyone"), bool), "training setting must be boolean", errors)
    _require(isinstance(data_use.get("zero_retention_mode"), bool), "ZRM setting must be boolean", errors)
    protection_mode = data_use.get("protection_mode")
    _require(
        protection_mode in {ACCOUNT_TRAINING_OPT_OUT_PROTECTION, ENTERPRISE_ZRM_PROTECTION},
        "ElevenLabs protection mode is not recognized",
        errors,
    )
    _require(
        data_use.get("protection_effective_for_new_submissions") is True,
        "ElevenLabs protection is not effective for new submissions",
        errors,
    )
    if protection_mode == ACCOUNT_TRAINING_OPT_OUT_PROTECTION:
        _require(data_use.get("improve_models_for_everyone") is False, "account training opt-out setting is not disabled", errors)
        _require(data_use.get("zero_retention_mode") is False, "account opt-out mode may not claim ZRM", errors)
        _require(data_use.get("opt_out_processed") is True, "account training opt-out has not been processed", errors)
        _require(data_use.get("zrm_eligible_and_confirmed") is False, "account opt-out mode may not claim enterprise ZRM confirmation", errors)
        enable_logging = True
    elif protection_mode == ENTERPRISE_ZRM_PROTECTION:
        _require(data_use.get("zero_retention_mode") is True, "enterprise ZRM mode is not enabled", errors)
        _require(data_use.get("opt_out_processed") is False, "enterprise ZRM mode may not masquerade as an account opt-out", errors)
        _require(data_use.get("zrm_eligible_and_confirmed") is True, "enterprise ZRM eligibility is not confirmed", errors)
        enable_logging = False
    else:
        enable_logging = False
    _require(isinstance(data_use.get("account_scope_binding_sha256"), str) and bool(_SHA_RE.fullmatch(data_use["account_scope_binding_sha256"])), "data-use assurance needs a hashed account binding", errors)
    _require(isinstance(data_use.get("verified_by"), str) and bool(data_use["verified_by"]), "data-use verifier is required", errors)
    data_verified_at = _parse_time(
        data_use.get("verified_at"),
        "data-use verified_at",
        errors,
    )
    _require(data_use.get("chosen_enable_logging") is enable_logging, "data-use assurance chosen logging mode is inconsistent", errors)
    evidence_binding = _strict_object(
        data_use.get("evidence"), {"path", "sha256"}, {"path", "sha256"}, "data-use evidence binding"
    )
    evidence_path = _safe_relative(root, evidence_binding.get("path"), "data-use evidence path", must_exist=True, suffix=".json")
    _require(evidence_binding.get("sha256") == sha256_file(evidence_path), "data-use evidence SHA-256 mismatch", errors)
    evidence = read_json(evidence_path)
    _strict_object(
        evidence,
        {
            "schema_version", "provider", "account_scope_binding_sha256", "captured_at",
            "improve_models_for_everyone", "zero_retention_mode", "chosen_enable_logging",
            "protection_mode", "opt_out_processed", "protection_effective_for_new_submissions",
            "zrm_eligible_and_confirmed",
        },
        {
            "schema_version", "provider", "account_scope_binding_sha256", "captured_at",
            "improve_models_for_everyone", "zero_retention_mode", "chosen_enable_logging",
            "protection_mode", "opt_out_processed", "protection_effective_for_new_submissions",
            "zrm_eligible_and_confirmed",
        },
        "data-use evidence",
    )
    _require(evidence.get("schema_version") == "oe-elevenlabs-account-data-use-evidence-v1", "data-use evidence schema mismatch", errors)
    _require(evidence.get("provider") == "elevenlabs", "data-use evidence provider mismatch", errors)
    _require(evidence.get("account_scope_binding_sha256") == data_use.get("account_scope_binding_sha256"), "data-use evidence account binding mismatch", errors)
    _require(_json_exact(evidence.get("improve_models_for_everyone"), data_use.get("improve_models_for_everyone")), "data-use evidence training setting mismatch", errors)
    _require(_json_exact(evidence.get("zero_retention_mode"), data_use.get("zero_retention_mode")), "data-use evidence ZRM setting mismatch", errors)
    _require(_json_exact(evidence.get("chosen_enable_logging"), data_use.get("chosen_enable_logging")), "data-use evidence chosen logging mode mismatch", errors)
    for key in (
        "protection_mode",
        "opt_out_processed",
        "protection_effective_for_new_submissions",
        "zrm_eligible_and_confirmed",
    ):
        _require(_json_exact(evidence.get(key), data_use.get(key)), f"data-use evidence {key} mismatch", errors)
    evidence_captured_at = _parse_time(
        evidence.get("captured_at"),
        "data-use evidence captured_at",
        errors,
    )

    primary = _compile_multipart(
        selected_audio,
        selected_sha,
        TRANSFER_PRIMARY_FORMAT,
        enable_logging=enable_logging,
    )
    fallback = _compile_multipart(
        selected_audio,
        selected_sha,
        TRANSFER_FALLBACK_FORMAT,
        enable_logging=enable_logging,
    )
    compiled_bindings = {
        "selected_guide_sha256": selected_sha,
        "primary_request_sha256": sha256_bytes(_compact_json_bytes(primary)),
        "primary_multipart_body_sha256": primary["multipart_body_sha256"],
        "primary_multipart_body_bytes": primary["multipart_body_bytes"],
        "conditional_fallback_request_sha256": sha256_bytes(_compact_json_bytes(fallback)),
        "conditional_fallback_multipart_body_sha256": fallback["multipart_body_sha256"],
        "conditional_fallback_multipart_body_bytes": fallback["multipart_body_bytes"],
        "enable_logging": enable_logging,
    }
    for key, expected in compiled_bindings.items():
        _require(_json_exact(bindings.get(key), expected), f"active voice-transfer bindings.{key} mismatch", errors)
    _require(set(bindings) == {
        "performance_transfer_plan_sha256", "canonical_w_sha256", "spoken_text_sha256",
        *compiled_bindings.keys(),
    }, "active voice-transfer bindings must authorize the exact multipart bodies", errors)

    rights_path, rights = _verified_prerequisite(root, prerequisites.get("target_voice_rights"), "prerequisites.target_voice_rights", expected_schema="oe-elevenlabs-voice-transfer-rights-v1")
    _strict_object(
        rights,
        {
            "schema_version", "provider", "authorization_id", "performance_transfer_plan_sha256",
            "primary_request_sha256", "primary_multipart_body_sha256", "target_voice_id", "voice_owner", "consent_owner",
            "exact_guide_sha256", "owner_approval", "voice_changer_permitted",
            "approved_at", "bounded_microtest_only", "full_capture_permitted", "original_c_provenance",
        },
        {
            "schema_version", "provider", "authorization_id", "performance_transfer_plan_sha256",
            "primary_request_sha256", "primary_multipart_body_sha256", "target_voice_id", "voice_owner", "consent_owner",
            "exact_guide_sha256", "owner_approval", "voice_changer_permitted",
            "approved_at", "bounded_microtest_only", "full_capture_permitted", "original_c_provenance",
        },
        "target voice rights receipt",
    )
    _require(rights.get("provider") == "elevenlabs" and rights.get("target_voice_id") == TRANSFER_TARGET_VOICE_ID, "target voice rights binding mismatch", errors)
    _require(rights.get("authorization_id") == authorization.get("authorization_id"), "target voice rights authorization ID mismatch", errors)
    _require(rights.get("performance_transfer_plan_sha256") == plan_dry["plan_sha256"], "target voice rights plan mismatch", errors)
    _require(rights.get("primary_request_sha256") == compiled_bindings["primary_request_sha256"], "target voice rights compiled request mismatch", errors)
    _require(rights.get("primary_multipart_body_sha256") == primary["multipart_body_sha256"], "target voice rights multipart body mismatch", errors)
    _require(rights.get("voice_owner") == authorization.get("approved_by") and rights.get("consent_owner") == authorization.get("approved_by"), "voice owner, consent owner, and active authorizer must match", errors)
    _require(rights.get("exact_guide_sha256") == selected_sha, "target voice rights guide hash mismatch", errors)
    _require(rights.get("owner_approval") is True and rights.get("voice_changer_permitted") is True, "voice transfer rights are not approved", errors)
    _require(rights.get("bounded_microtest_only") is True and rights.get("full_capture_permitted") is False, "voice rights must remain microtest-only", errors)
    rights_approved_at = _parse_time(
        rights.get("approved_at"),
        "target voice rights approved_at",
        errors,
    )
    provenance = _strict_object(
        rights.get("original_c_provenance"),
        {"owner_selection_path", "owner_selection_sha256", "saved_voice_receipt_path", "saved_voice_receipt_sha256"},
        {"owner_selection_path", "owner_selection_sha256", "saved_voice_receipt_path", "saved_voice_receipt_sha256"},
        "Original C provenance",
    )
    prior_selection_path = _safe_blueprint_relative_file(
        rights_path,
        provenance.get("owner_selection_path"),
        provenance.get("owner_selection_sha256"),
        "Original C owner selection",
    )
    prior_selection = read_json(prior_selection_path)
    _strict_object(
        prior_selection,
        {
            "schema_version", "preview_receipt_sha256", "source_voice_id",
            "selected_generated_voice_id", "selected_audio_sha256", "selected_by", "selected_at",
            "owner_approved_save", "voice_name", "voice_description",
        },
        {
            "schema_version", "preview_receipt_sha256", "source_voice_id",
            "selected_generated_voice_id", "selected_audio_sha256", "selected_by", "selected_at",
            "owner_approved_save", "voice_name", "voice_description",
        },
        "Original C owner selection receipt",
    )
    _require(prior_selection.get("schema_version") == "oe-elevenlabs-voice-remix-owner-selection-v1", "Original C owner selection schema mismatch", errors)
    _require(prior_selection.get("selected_generated_voice_id") == TRANSFER_TARGET_VOICE_ID, "Original C owner selection voice mismatch", errors)
    _require(prior_selection.get("selected_by") == authorization.get("approved_by") and prior_selection.get("owner_approved_save") is True, "Original C was not selected by the active authorizer", errors)
    original_c_selected_at = _parse_time(
        prior_selection.get("selected_at"),
        "Original C selected_at",
        errors,
    )

    prior_save_path = _safe_blueprint_relative_file(
        rights_path,
        provenance.get("saved_voice_receipt_path"),
        provenance.get("saved_voice_receipt_sha256"),
        "Original C saved voice receipt",
    )
    prior_save = read_json(prior_save_path)
    _strict_object(
        prior_save,
        {
            "schema_version", "authorization_consumption_record", "authorization_consumption_sha256",
            "authorization_id", "authorization_sha256", "created_at", "new_voice_category",
            "new_voice_created", "new_voice_id", "new_voice_is_owner", "new_voice_is_owner_status",
            "new_voice_name", "outcome", "owner_selection_record_sha256", "provider",
            "provider_calls_made", "provider_character_cost", "provider_identifiers", "readback",
            "request_body_sha256", "scope", "selected_audio_sha256", "selected_generated_voice_id",
            "source_voice_id", "source_voice_modified", "spend",
        },
        {
            "schema_version", "new_voice_created", "new_voice_id", "outcome",
            "owner_selection_record_sha256", "provider", "provider_calls_made",
            "selected_generated_voice_id", "source_voice_modified",
        },
        "Original C saved voice receipt",
    )
    _require(prior_save.get("schema_version") == "oe-elevenlabs-voice-remix-save-receipt-v1", "Original C save receipt schema mismatch", errors)
    _require(prior_save.get("provider") == "elevenlabs" and prior_save.get("new_voice_id") == TRANSFER_TARGET_VOICE_ID, "Original C save receipt voice mismatch", errors)
    _require(prior_save.get("selected_generated_voice_id") == TRANSFER_TARGET_VOICE_ID, "Original C saved selection mismatch", errors)
    _require(prior_save.get("owner_selection_record_sha256") == sha256_file(prior_selection_path), "Original C save receipt does not bind owner selection", errors)
    _require(
        prior_save.get("new_voice_created") is True
        and prior_save.get("source_voice_modified") is False
        and type(prior_save.get("provider_calls_made")) is int
        and prior_save.get("provider_calls_made") == 1,
        "Original C save outcome is invalid",
        errors,
    )
    original_c_saved_at = _parse_time(
        prior_save.get("created_at"),
        "Original C saved voice created_at",
        errors,
    )
    ordered_times = (
        guide_completed_at,
        qa_reviewed_at,
        guide_selected_at,
        evidence_captured_at,
        data_verified_at,
        rights_approved_at,
        active_approved_at,
        original_c_selected_at,
        original_c_saved_at,
    )
    if all(value is not None for value in ordered_times):
        assert guide_completed_at is not None
        assert qa_reviewed_at is not None
        assert guide_selected_at is not None
        assert evidence_captured_at is not None
        assert data_verified_at is not None
        assert rights_approved_at is not None
        assert active_approved_at is not None
        assert original_c_selected_at is not None
        assert original_c_saved_at is not None
        _require(guide_completed_at <= qa_reviewed_at <= guide_selected_at, "guide run, QA, and owner-selection timestamps are incoherent", errors)
        _require(evidence_captured_at <= data_verified_at, "data-use evidence must precede verification", errors)
        _require(max(guide_selected_at, data_verified_at) <= rights_approved_at <= active_approved_at, "selection, data-use, rights, and active authorization timestamps are incoherent", errors)
        _require(original_c_selected_at <= original_c_saved_at <= active_approved_at, "Original C provenance timestamps are incoherent", errors)
    if errors:
        raise ValidationError(errors)
    return {
        "schema_version": "oe-elevenlabs-voice-transfer-dry-run-v1",
        "valid": True,
        "status": "active_exact_authority_validated",
        "authorization_id": authorization["authorization_id"],
        "authorization_sha256": sha256_file(authorization_path),
        "plan_sha256": plan_dry["plan_sha256"],
        "selected_guide_sha256": selected_sha,
        "guide_qa_sha256": sha256_file(qa_path),
        "owner_selection_sha256": sha256_file(selection_path),
        "primary_request": primary,
        "conditional_fallback_request": {
            **fallback,
            "enabled": False,
            "requires": "documented_unambiguous_pcm_capability_rejection_before_any_audio_is_accepted",
            "forbidden_on": ["timeout", "disconnect", "429", "5xx", "malformed_response", "ambiguous_charge"],
        },
        "maximum": limits,
        "request_compiled": True,
        "provider_action_authorized": True,
        "network_authorized": False,
        "execution_transport_available": False,
        "network_called": False,
        "credentials_accessed": False,
        "audio_files_created": 0,
        "creative_approved": False,
        "full_capture_authorized": False,
        "step3_authorized": False,
        "publication_authorized": False,
    }


__all__ = [
    "dry_run_synthetic_guide",
    "dry_run_voice_transfer",
    "execute_synthetic_guide",
    "validate_performance_transfer_plan",
    "validate_synthetic_guide_authorization",
    "validate_voice_transfer_authorization",
]
