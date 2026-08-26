"""One-shot, hash-bound Google Service Usage enablement transaction.

This module can only enable ``aiplatform.googleapis.com`` for one private,
hash-bound Google Cloud project.  Dry-run validation is the default.  External
execution requires a separately approved ACTIVE authorization, consumes that
authority before ADC token refresh or provider network, and writes one private
success or failure receipt.  It cannot disable a service, mutate IAM/billing,
or invoke synthesis.
"""

from __future__ import annotations

import json
import os
import re
import stat
import subprocess
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, BinaryIO

from .core import ValidationError, sha256_bytes, sha256_file
from . import performance_transfer as pt


AUTH_SCHEMA = "oe-google-service-enablement-authorization-v2"
DRY_RUN_SCHEMA = "oe-google-service-enablement-dry-run-v2"
CONSUMPTION_SCHEMA = "oe-google-service-enablement-consumption-v2"
RUN_RECEIPT_SCHEMA = "oe-google-service-enablement-run-receipt-v2"
FAILURE_RECEIPT_SCHEMA = "oe-google-service-enablement-failure-v2"
PRIOR_AUTH_SCHEMA = "oe-google-service-enablement-authorization-v1"
PRIOR_CONSUMPTION_SCHEMA = "oe-google-service-enablement-consumption-v1"
PRIOR_FAILURE_RECEIPT_SCHEMA = "oe-google-service-enablement-failure-v1"
PRIOR_DISPOSITION_SCHEMA = "oe-google-service-enablement-failure-disposition-v1"
SCOPE = "enable_one_exact_google_service"
PROVIDER = "google_cloud_service_usage"
SERVICE = "aiplatform.googleapis.com"
READBACK_FIELDS = "name,state"
BASE_ENDPOINT = "https://serviceusage.googleapis.com/v1"
PROJECT_ENV = pt.GUIDE_QUOTA_PROJECT_ENV
PROJECT_NUMBER_ENV = "GOOGLE_CLOUD_PROJECT_NUMBER"
CREDENTIAL_MECHANISM = "gcloud_application_default_print_access_token_without_scopes_override"

MAX_PRE_ENABLE_READBACKS = 1
MAX_ENABLE_ATTEMPTS = 1
MAX_OPERATION_POLLS = 12
MAX_POST_ENABLE_READBACKS = 1
MAX_HTTP_CALLS = 15
MAX_RESPONSE_BYTES_PER_CALL = 1_000_000
MAX_TOTAL_RESPONSE_BYTES = 15_000_000
REQUEST_TIMEOUT_SECONDS = 30
POLL_INTERVAL_SECONDS = 5
MAX_OPERATION_ELAPSED_SECONDS = 120
MAX_AUTHORIZATION_WINDOW_SECONDS = 86_400
ENABLE_BODY = b""
ENABLE_BODY_SHA256 = sha256_bytes(ENABLE_BODY)

EXECUTOR_RELATIVE = (
    "operator-blueprint-v2/02-narration-production/runtime/oe_narration/"
    "google_service_enablement.py"
)
CREDENTIAL_RUNTIME_RELATIVE = (
    "operator-blueprint-v2/02-narration-production/runtime/oe_narration/"
    "performance_transfer.py"
)
CLI_RELATIVE = (
    "operator-blueprint-v2/02-narration-production/runtime/oe_narration/cli.py"
)
CORE_RELATIVE = (
    "operator-blueprint-v2/02-narration-production/runtime/oe_narration/core.py"
)
INIT_RELATIVE = (
    "operator-blueprint-v2/02-narration-production/runtime/oe_narration/__init__.py"
)
SCHEMA_RELATIVE = (
    "operator-blueprint-v2/02-narration-production/schemas/"
    "google-service-enablement-authorization.schema.json"
)

_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,159}$")
_SHA_RE = re.compile(r"^[0-9a-f]{64}$")
_GIT_COMMIT_RE = re.compile(r"^[0-9a-f]{40}(?:[0-9a-f]{24})?$")
_PROJECT_RE = re.compile(r"^(?:[a-z][a-z0-9-]{4,61}[a-z0-9]|[0-9]{6,30})$")
_PROJECT_NUMBER_RE = re.compile(r"^[0-9]{6,30}$")
_OPERATION_RE = re.compile(r"^operations/[A-Za-z0-9._-]{1,512}$")
_RESOURCE_RE = re.compile(
    r"^projects/[A-Za-z0-9._:-]{1,255}/services/aiplatform\.googleapis\.com$"
)

_ACTIVE_LIMITS = {
    "max_pre_enable_state_readbacks": MAX_PRE_ENABLE_READBACKS,
    "max_enable_attempts": MAX_ENABLE_ATTEMPTS,
    "max_operation_polls": MAX_OPERATION_POLLS,
    "max_post_enable_state_readbacks": MAX_POST_ENABLE_READBACKS,
    "max_http_calls": MAX_HTTP_CALLS,
    "max_response_bytes_per_call": MAX_RESPONSE_BYTES_PER_CALL,
    "max_total_response_bytes": MAX_TOTAL_RESPONSE_BYTES,
    "request_timeout_seconds": REQUEST_TIMEOUT_SECONDS,
    "poll_interval_seconds": POLL_INTERVAL_SECONDS,
    "max_operation_elapsed_seconds": MAX_OPERATION_ELAPSED_SECONDS,
    "max_other_service_mutations": 0,
    "max_iam_mutations": 0,
    "max_billing_mutations": 0,
    "max_project_hierarchy_mutations": 0,
    "max_synthesis_calls": 0,
}
_ZERO_LIMITS = {key: 0 for key in _ACTIVE_LIMITS}

_DRAFT_AUTHORITY = {
    "credential_access_authorized": False,
    "network_access_authorized": False,
    "service_readback_authorized": False,
    "service_enablement_authorized": False,
    "service_disablement_authorized": False,
    "other_service_mutation_authorized": False,
    "iam_mutation_authorized": False,
    "billing_mutation_authorized": False,
    "project_hierarchy_mutation_authorized": False,
    "synthetic_guide_generation_authorized": False,
    "retry_authorized": False,
    "voice_transfer_authorized": False,
    "full_capture_authorized": False,
    "step3_authorized": False,
    "sharing_authorized": False,
    "publication_authorized": False,
}
_ACTIVE_AUTHORITY = {
    **_DRAFT_AUTHORITY,
    "credential_access_authorized": True,
    "network_access_authorized": True,
    "service_readback_authorized": True,
    "service_enablement_authorized": True,
}

_ACTION = {
    "provider": PROVIDER,
    "service": SERVICE,
    "project_identity_source": "private_hash_bound_environment_value",
    "credential_mechanism": CREDENTIAL_MECHANISM,
    "pre_enable_readback": {
        "method": "GET",
        "endpoint_template": (
            f"{BASE_ENDPOINT}/projects/{{project}}/services/{SERVICE}"
            f"?fields={READBACK_FIELDS}"
        ),
        "fields": READBACK_FIELDS,
        "required_state": "DISABLED",
    },
    "enable": {
        "method": "POST",
        "endpoint_template": f"{BASE_ENDPOINT}/projects/{{project}}/services/{SERVICE}:enable",
        "body_sha256": ENABLE_BODY_SHA256,
        "body_bytes": len(ENABLE_BODY),
    },
    "operation_poll": {
        "method": "GET",
        "endpoint_template": f"{BASE_ENDPOINT}/{{operation_name}}",
        "required_terminal_done": True,
    },
    "post_enable_readback": {
        "method": "GET",
        "endpoint_template": (
            f"{BASE_ENDPOINT}/projects/{{project}}/services/{SERVICE}"
            f"?fields={READBACK_FIELDS}"
        ),
        "fields": READBACK_FIELDS,
        "required_state": "ENABLED",
    },
    "no_retry": True,
    "no_redirect": True,
    "disable_after_test": False,
    "no_other_mutation": True,
}

_PRIOR_V1_ACTION = {
    **_ACTION,
    "pre_enable_readback": {
        "method": "GET",
        "endpoint_template": f"{BASE_ENDPOINT}/projects/{{project}}/services/{SERVICE}",
        "required_state": "DISABLED",
    },
    "post_enable_readback": {
        "method": "GET",
        "endpoint_template": f"{BASE_ENDPOINT}/projects/{{project}}/services/{SERVICE}",
        "required_state": "ENABLED",
    },
}

_PRIOR_FAILURE_CALLS = {
    "pre_enable_state_readbacks": 1,
    "enable_attempts": 0,
    "operation_polls": 0,
    "post_enable_state_readbacks": 0,
    "http_calls_total": 1,
}
_PRIOR_FAILURE_RESPONSE_BYTES = MAX_RESPONSE_BYTES_PER_CALL + 1
_PRIOR_EXECUTION_SEMANTICS = (
    "fresh_transaction_after_zero_mutation_not_retry_or_resumption"
)
_PRIOR_ESTABLISHED = (
    "the single HTTP 200 pre-enable response crossed the authorized 1000000-byte "
    "read ceiling and the runtime stopped after reading the sentinel byte at 1000001 bytes"
)
_PRIOR_SAFE_CONCLUSION = (
    "a response-handling limit failed before the authorized enablement mutation; this is "
    "not evidence that the service was enabled or that the provider response was exactly "
    "1000001 bytes long"
)

_REQUIRED_SUCCESS_EVIDENCE = {
    "pre_enable_service_state": "DISABLED",
    "pre_enable_response_sha256_required": True,
    "enable_operation_response_sha256_required": True,
    "operation_completion_response_sha256_required": True,
    "post_enable_service_state": "ENABLED",
    "post_enable_response_sha256_required": True,
    "timestamps_required": True,
    "raw_project_identifier_forbidden": True,
    "raw_project_number_forbidden": True,
    "raw_credentials_forbidden": True,
    "raw_billing_identity_forbidden": True,
    "raw_provider_responses_forbidden": True,
}


@dataclass(frozen=True)
class _Contract:
    root: Path
    authorization_path: Path
    authorization: dict[str, Any]
    authorization_sha256: str
    diagnosis_path: Path
    diagnosis_sha256: str
    readiness_path: Path
    readiness_sha256: str
    prior_authorization_path: Path
    prior_authorization_sha256: str
    prior_consumption_path: Path
    prior_consumption_sha256: str
    prior_failure_path: Path
    prior_failure_sha256: str
    disposition_path: Path
    disposition_sha256: str
    consumption_relative: str
    success_relative: str
    failure_relative: str
    approved_at: datetime | None
    expires_at: datetime | None


@dataclass(frozen=True)
class _ServiceResponse:
    response_bytes: int
    response_sha256: str
    payload: dict[str, Any]
    provider_identifiers: dict[str, str]
    provider_usage: dict[str, int]


class _ServiceFailure(Exception):
    """One redacted failure carrying only explicitly safe receipt evidence."""

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
        operation_terminal: bool = False,
        operation_succeeded: bool = False,
    ) -> None:
        super().__init__(code)
        self.code = code
        self.http_status = http_status
        self.response_bytes = response_bytes
        self.response_sha256 = response_sha256
        self.provider_error = provider_error
        self.provider_identifiers = provider_identifiers or {}
        self.provider_usage = provider_usage or {}
        self.operation_terminal = operation_terminal
        self.operation_succeeded = operation_succeeded


class _NoRedirect(urllib.request.HTTPRedirectHandler):
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


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _sleep(seconds: float) -> None:
    time.sleep(seconds)


def _iso(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat()


def _exact(actual: Any, expected: Any) -> bool:
    return pt._json_exact(actual, expected)


def _require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def _strict(value: Any, keys: set[str], label: str) -> dict[str, Any]:
    return pt._strict_object(value, keys, keys, label)


def _read_fixture_json(
    root: Path,
    path: Path,
    label: str,
    *,
    max_bytes: int = 1_000_000,
    required_mode: int | None = None,
) -> tuple[dict[str, Any], bytes, str]:
    """Descriptor-bind and strict-decode one fixture-local JSON document."""

    try:
        relative = Path(path).absolute().relative_to(root).as_posix()
    except ValueError:
        raise ValidationError(f"{label} is outside the fixture root") from None
    parent_fd, name = pt._open_parent_descriptor(root, relative, create_parents=False)
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
            raise ValidationError(f"{label} is not a bounded regular file")
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
            or (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns, before.st_mode)
            != (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns, after.st_mode)
        ):
            raise ValidationError(f"{label} changed during its bound read")
        value = pt._strict_json_bytes(raw, label)
        return value, raw, sha256_bytes(raw)
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


def _parse_timestamp(value: Any, label: str, errors: list[str]) -> datetime | None:
    return pt._parse_time(value, label, errors)


def _expected_artifacts(authorization_id: str) -> dict[str, str]:
    return {
        "consumption_record_path": (
            f"authorizations/consumed/{authorization_id}.consumed.json"
        ),
        "success_receipt_path": (
            f"receipts/google-service-usage/{authorization_id}.run.json"
        ),
        "failure_receipt_path": (
            f"receipts/google-service-usage/{authorization_id}.failure.json"
        ),
    }


def _expected_runtime_bindings(*, draft: bool) -> dict[str, str]:
    pending = "pending"
    return {
        "git_commit": pending,
        "executor_path": EXECUTOR_RELATIVE,
        "executor_sha256": pending if draft else sha256_file(Path(__file__).absolute()),
        "credential_runtime_path": CREDENTIAL_RUNTIME_RELATIVE,
        "credential_runtime_sha256": (
            pending if draft else sha256_file(Path(pt.__file__).absolute())
        ),
        "cli_path": CLI_RELATIVE,
        "cli_sha256": pending if draft else sha256_file(Path(__file__).with_name("cli.py")),
        "core_path": CORE_RELATIVE,
        "core_sha256": pending if draft else sha256_file(Path(__file__).with_name("core.py")),
        "init_path": INIT_RELATIVE,
        "init_sha256": pending if draft else sha256_file(Path(__file__).with_name("__init__.py")),
        "schema_path": SCHEMA_RELATIVE,
        "schema_sha256": (
            pending
            if draft
            else sha256_file(
                Path(__file__).resolve().parents[2]
                / "schemas"
                / "google-service-enablement-authorization.schema.json"
            )
        ),
    }


def _validate_diagnosis(root: Path, binding: dict[str, Any]) -> tuple[Path, str]:
    path = pt._safe_relative(
        root,
        binding["path"],
        "diagnosis_binding.path",
        must_exist=True,
        suffix=".json",
    )
    if path.relative_to(root).parts[0] != "evidence":
        raise ValidationError("diagnosis_binding.path must remain below evidence/")
    diagnosis, _diagnosis_bytes, actual_sha = _read_fixture_json(
        root,
        path,
        "diagnosis record",
    )
    if actual_sha != binding["sha256"]:
        raise ValidationError("diagnosis_binding.sha256 does not match the diagnosis record")
    _strict(
        diagnosis,
        {
            "schema_version",
            "record_id",
            "status",
            "recorded_at",
            "evidence_boundary",
            "prior_attempt_bindings",
            "live_readback",
            "diagnosis",
            "authority",
        },
        "diagnosis record",
    )
    errors: list[str] = []
    _require(
        diagnosis.get("schema_version") == "oe-google-g1-403-diagnosis-v1",
        "diagnosis schema_version drifted",
        errors,
    )
    _require(
        diagnosis.get("status") == "operator_reported_live_readback",
        "diagnosis status drifted",
        errors,
    )
    recorded = _parse_timestamp(diagnosis.get("recorded_at"), "diagnosis.recorded_at", errors)
    _require(recorded is not None and recorded <= _now(), "diagnosis timestamp is in the future", errors)
    live = diagnosis.get("live_readback")
    if not isinstance(live, dict):
        errors.append("diagnosis.live_readback must be an object")
    else:
        project = live.get("project")
        services = live.get("services")
        _require(
            isinstance(project, dict)
            and project.get("project_sha256") == binding["project_sha256"]
            and project.get("lifecycle_state") == "ACTIVE",
            "diagnosis project binding is not active and exact",
            errors,
        )
        _require(
            isinstance(services, dict)
            and services.get(SERVICE) == "DISABLED"
            and services.get("serviceusage.googleapis.com") == "ENABLED",
            "diagnosis does not bind the exact disabled target and enabled Service Usage API",
            errors,
        )
    diagnosis_value = diagnosis.get("diagnosis")
    _require(
        isinstance(diagnosis_value, dict)
        and diagnosis_value.get("only_confirmed_configuration_anomaly")
        == "aiplatform.googleapis.com is DISABLED"
        and diagnosis_value.get("aiplatform_service_disablement_is_proven_403_cause") is False
        and diagnosis_value.get("blind_retry_permitted") is False,
        "diagnosis conclusion does not preserve the non-causal, no-blind-retry boundary",
        errors,
    )
    authority = diagnosis.get("authority")
    _require(
        isinstance(authority, dict)
        and all(value is False for value in authority.values()),
        "diagnosis must carry no execution authority",
        errors,
    )
    if errors:
        raise ValidationError(errors)
    return path, actual_sha


def _validate_readiness(root: Path, binding: dict[str, Any]) -> tuple[Path, str]:
    path = pt._safe_relative(
        root,
        binding["path"],
        "readiness_binding.path",
        must_exist=True,
        suffix=".json",
    )
    if path.relative_to(root).parts[0] != "evidence":
        raise ValidationError("readiness_binding.path must remain below evidence/")
    evidence, _evidence_bytes, actual_sha = _read_fixture_json(
        root,
        path,
        "service enablement readiness evidence",
    )
    if actual_sha != binding["sha256"]:
        raise ValidationError("readiness_binding.sha256 does not match readiness evidence")
    _strict(
        evidence,
        {
            "schema_version",
            "record_id",
            "status",
            "recorded_at",
            "target",
            "readiness",
            "evidence_boundary",
            "authority",
        },
        "service enablement readiness evidence",
    )
    errors: list[str] = []
    _require(
        evidence.get("schema_version") == "oe-google-service-enablement-readiness-v1",
        "readiness schema_version drifted",
        errors,
    )
    _require(
        evidence.get("status") == "operator_reported_live_readback",
        "readiness status drifted",
        errors,
    )
    recorded = _parse_timestamp(evidence.get("recorded_at"), "readiness.recorded_at", errors)
    _require(recorded is not None and recorded <= _now(), "readiness timestamp is in the future", errors)
    expected_target = {
        "project_sha256": binding["project_sha256"],
        "project_number_sha256": binding["project_number_sha256"],
        "service": SERVICE,
    }
    _require(_exact(evidence.get("target"), expected_target), "readiness target drifted", errors)
    expected_readiness = {
        "service_usage_api_state": "ENABLED",
        "target_service_state": "DISABLED",
        "test_iam_permissions_method": "projects.testIamPermissions",
        "permission": "serviceusage.services.enable",
        "permission_granted": True,
        "same_live_adc_used": True,
    }
    _require(
        _exact(evidence.get("readiness"), expected_readiness),
        "readiness permission or service state drifted",
        errors,
    )
    expected_boundary = {
        "underlying_provider_responses_stored": False,
        "raw_access_token_stored": False,
        "raw_adc_material_stored": False,
        "raw_principal_stored": False,
        "raw_project_identifier_stored": False,
        "raw_project_number_stored": False,
        "raw_billing_account_stored": False,
        "credentials_accessed_during_record_materialization": False,
        "network_called_during_record_materialization": False,
        "cloud_state_mutated_during_record_materialization": False,
    }
    _require(
        _exact(evidence.get("evidence_boundary"), expected_boundary),
        "readiness evidence boundary drifted",
        errors,
    )
    _require(
        _exact(evidence.get("authority"), _DRAFT_AUTHORITY),
        "readiness evidence must carry no authority",
        errors,
    )
    if errors:
        raise ValidationError(errors)
    return path, actual_sha


def _validate_prior_attempt(
    root: Path,
    binding_value: Any,
    *,
    target: dict[str, Any],
    diagnosis_relative: str,
    diagnosis_sha256: str,
    readiness_relative: str,
    readiness_sha256: str,
) -> tuple[Path, str, Path, str, Path, str, Path, str]:
    """Validate the immutable, zero-mutation v1 attempt that justifies this repair."""

    binding = _strict(
        binding_value,
        {
            "authorization_id",
            "authorization_path",
            "authorization_sha256",
            "authorization_commit",
            "consumption_record_path",
            "consumption_record_sha256",
            "failure_receipt_path",
            "failure_receipt_sha256",
            "disposition_path",
            "disposition_sha256",
            "prior_runtime_commit",
            "outcome",
            "reason_code",
            "failed_phase",
            "http_status",
            "bounded_response_bytes_read",
            "captured_cap_plus_one_prefix_sha256",
            "mutation_attempted",
            "service_enable_request_sent",
            "service_mutation_occurred",
            "full_provider_response_length_known",
            "execution_semantics",
        },
        "prior_attempt_binding",
    )
    errors: list[str] = []
    prior_id = binding.get("authorization_id")
    _require(
        isinstance(prior_id, str) and bool(_ID_RE.fullmatch(prior_id)),
        "prior attempt authorization_id is invalid",
        errors,
    )
    for key in (
        "authorization_sha256",
        "consumption_record_sha256",
        "failure_receipt_sha256",
        "disposition_sha256",
        "captured_cap_plus_one_prefix_sha256",
    ):
        _require(
            isinstance(binding.get(key), str) and bool(_SHA_RE.fullmatch(binding[key])),
            f"prior_attempt_binding.{key} must be exact",
            errors,
        )
    for key in ("authorization_commit", "prior_runtime_commit"):
        _require(
            isinstance(binding.get(key), str)
            and bool(_GIT_COMMIT_RE.fullmatch(binding[key])),
            f"prior_attempt_binding.{key} must be exact",
            errors,
        )
    expected_summary = {
        "outcome": "failed_closed",
        "reason_code": "provider_response_byte_cap_exceeded",
        "failed_phase": "pre_enable_readback",
        "http_status": 200,
        "bounded_response_bytes_read": _PRIOR_FAILURE_RESPONSE_BYTES,
        "mutation_attempted": False,
        "service_enable_request_sent": False,
        "service_mutation_occurred": False,
        "full_provider_response_length_known": False,
        "execution_semantics": _PRIOR_EXECUTION_SEMANTICS,
    }
    for key, expected in expected_summary.items():
        _require(
            _exact(binding.get(key), expected),
            f"prior_attempt_binding.{key} drifted",
            errors,
        )
    if errors:
        raise ValidationError(errors)

    path_specs = (
        (
            "authorization_path",
            "authorization_sha256",
            ("authorizations",),
            "prior service authorization",
        ),
        (
            "consumption_record_path",
            "consumption_record_sha256",
            ("authorizations", "consumed"),
            "prior service consumption",
        ),
        (
            "failure_receipt_path",
            "failure_receipt_sha256",
            ("receipts", "google-service-usage"),
            "prior service failure receipt",
        ),
        (
            "disposition_path",
            "disposition_sha256",
            ("evidence",),
            "prior failure disposition",
        ),
    )
    documents: dict[str, tuple[Path, dict[str, Any], str]] = {}
    for path_key, sha_key, prefix, label in path_specs:
        path = pt._safe_relative(
            root,
            binding[path_key],
            f"prior_attempt_binding.{path_key}",
            must_exist=True,
            suffix=".json",
        )
        relative_parts = path.relative_to(root).parts
        if relative_parts[: len(prefix)] != prefix:
            raise ValidationError(f"prior_attempt_binding.{path_key} is outside its exact directory")
        value, _raw, actual_sha = _read_fixture_json(
            root,
            path,
            label,
            required_mode=(0o600 if path_key in {"consumption_record_path", "failure_receipt_path"} else None),
        )
        if actual_sha != binding[sha_key]:
            raise ValidationError(f"prior_attempt_binding.{sha_key} does not match {label}")
        documents[path_key] = (path, value, actual_sha)

    authorization_path, authorization, authorization_sha = documents["authorization_path"]
    consumption_path, consumption, consumption_sha = documents["consumption_record_path"]
    failure_path, failure, failure_sha = documents["failure_receipt_path"]
    disposition_path, disposition, disposition_sha = documents["disposition_path"]

    if authorization_path.relative_to(root).parts[:2] == ("authorizations", "consumed"):
        raise ValidationError("prior authorization cannot be a consumption record")
    if ".ACTIVE." not in authorization_path.name:
        raise ValidationError("prior authorization path must identify the consumed ACTIVE authority")
    expected_prior_artifacts = _expected_artifacts(prior_id)
    if (
        binding["consumption_record_path"]
        != expected_prior_artifacts["consumption_record_path"]
        or binding["failure_receipt_path"]
        != expected_prior_artifacts["failure_receipt_path"]
    ):
        raise ValidationError("prior consumption and failure paths must derive from prior authorization_id")

    _strict(
        authorization,
        {
            "schema_version",
            "authorization_id",
            "status",
            "approved",
            "scope",
            "target",
            "diagnosis_binding",
            "readiness_binding",
            "runtime_bindings",
            "action",
            "prospective_active_limits",
            "authorized_limits",
            "artifacts",
            "required_success_evidence",
            "approved_by",
            "approved_at",
            "expires_at",
            "execution_ready",
            "blockers",
            "authority",
        },
        "prior service authorization",
    )
    prior_errors: list[str] = []
    _require(authorization.get("schema_version") == PRIOR_AUTH_SCHEMA, "prior authorization schema drifted", prior_errors)
    _require(authorization.get("authorization_id") == prior_id, "prior authorization ID drifted", prior_errors)
    _require(authorization.get("status") == "active", "prior authorization was not active", prior_errors)
    _require(authorization.get("approved") is True, "prior authorization was not approved", prior_errors)
    _require(authorization.get("execution_ready") is True, "prior authorization was not execution-ready", prior_errors)
    _require(authorization.get("scope") == SCOPE, "prior authorization scope drifted", prior_errors)
    _require(_exact(authorization.get("target"), target), "prior authorization target drifted", prior_errors)
    _require(_exact(authorization.get("action"), _PRIOR_V1_ACTION), "prior authorization action drifted", prior_errors)
    _require(_exact(authorization.get("prospective_active_limits"), _ACTIVE_LIMITS), "prior prospective limits drifted", prior_errors)
    _require(_exact(authorization.get("authorized_limits"), _ACTIVE_LIMITS), "prior authorized limits drifted", prior_errors)
    _require(_exact(authorization.get("artifacts"), expected_prior_artifacts), "prior artifact paths drifted", prior_errors)
    _require(_exact(authorization.get("required_success_evidence"), _REQUIRED_SUCCESS_EVIDENCE), "prior success-evidence contract drifted", prior_errors)
    _require(_exact(authorization.get("authority"), _ACTIVE_AUTHORITY), "prior authority drifted", prior_errors)
    _require(authorization.get("blockers") == [], "prior authorization had blockers", prior_errors)
    _require(isinstance(authorization.get("approved_by"), str) and bool(authorization["approved_by"]), "prior approved_by is missing", prior_errors)
    prior_diagnosis = _strict(
        authorization.get("diagnosis_binding"),
        {"path", "sha256", "project_sha256", "reported_current_state", "causal_status"},
        "prior diagnosis_binding",
    )
    prior_readiness = _strict(
        authorization.get("readiness_binding"),
        {"path", "sha256", "project_sha256", "project_number_sha256", "permission", "permission_granted"},
        "prior readiness_binding",
    )
    _require(
        _exact(
            prior_diagnosis,
            {
                "path": diagnosis_relative,
                "sha256": diagnosis_sha256,
                "project_sha256": target["project_sha256"],
                "reported_current_state": "DISABLED",
                "causal_status": "only_confirmed_configuration_anomaly_not_proven_403_cause",
            },
        ),
        "prior diagnosis binding drifted",
        prior_errors,
    )
    _require(
        _exact(
            prior_readiness,
            {
                "path": readiness_relative,
                "sha256": readiness_sha256,
                "project_sha256": target["project_sha256"],
                "project_number_sha256": target["project_number_sha256"],
                "permission": "serviceusage.services.enable",
                "permission_granted": True,
            },
        ),
        "prior readiness binding drifted",
        prior_errors,
    )
    prior_runtime = _strict(
        authorization.get("runtime_bindings"),
        set(_expected_runtime_bindings(draft=True)),
        "prior runtime_bindings",
    )
    _require(prior_runtime.get("git_commit") == binding["prior_runtime_commit"], "prior runtime commit drifted", prior_errors)
    for key in ("executor_sha256", "credential_runtime_sha256", "cli_sha256", "core_sha256", "init_sha256", "schema_sha256"):
        _require(isinstance(prior_runtime.get(key), str) and bool(_SHA_RE.fullmatch(prior_runtime[key])), f"prior runtime {key} is invalid", prior_errors)
    prior_approved = _parse_timestamp(authorization.get("approved_at"), "prior approved_at", prior_errors)
    prior_expires = _parse_timestamp(authorization.get("expires_at"), "prior expires_at", prior_errors)
    if prior_errors:
        raise ValidationError(prior_errors)

    consumption_keys = {
        "schema_version", "authorization_id", "authorization_sha256", "scope", "provider",
        "service", "project_sha256", "project_number_sha256", "diagnosis_path",
        "diagnosis_sha256", "readiness_path", "readiness_sha256", "runtime_bindings",
        "status", "consumed_at", "consumed_before_network", "network_called_at_consumption",
        "reserved_limits", "credentials_recorded", *_authority_false_fields().keys(),
    }
    _strict(consumption, consumption_keys, "prior service consumption")
    consumed_errors: list[str] = []
    _require(consumption.get("schema_version") == PRIOR_CONSUMPTION_SCHEMA, "prior consumption schema drifted", consumed_errors)
    _require(consumption.get("authorization_id") == prior_id, "prior consumption authorization ID drifted", consumed_errors)
    _require(consumption.get("authorization_sha256") == authorization_sha, "prior consumption authorization hash drifted", consumed_errors)
    _require(consumption.get("scope") == SCOPE and consumption.get("provider") == PROVIDER and consumption.get("service") == SERVICE, "prior consumption provider scope drifted", consumed_errors)
    _require(consumption.get("project_sha256") == target["project_sha256"] and consumption.get("project_number_sha256") == target["project_number_sha256"], "prior consumption target drifted", consumed_errors)
    _require(consumption.get("diagnosis_path") == diagnosis_relative and consumption.get("diagnosis_sha256") == diagnosis_sha256, "prior consumption diagnosis binding drifted", consumed_errors)
    _require(consumption.get("readiness_path") == readiness_relative and consumption.get("readiness_sha256") == readiness_sha256, "prior consumption readiness binding drifted", consumed_errors)
    _require(_exact(consumption.get("runtime_bindings"), prior_runtime), "prior consumption runtime binding drifted", consumed_errors)
    _require(consumption.get("status") == "consumed_before_network" and consumption.get("consumed_before_network") is True and consumption.get("network_called_at_consumption") is False, "prior authority was not consumed before network", consumed_errors)
    _require(_exact(consumption.get("reserved_limits"), _ACTIVE_LIMITS), "prior consumption limits drifted", consumed_errors)
    _require(consumption.get("credentials_recorded") is False, "prior consumption recorded credentials", consumed_errors)
    _require(all(consumption.get(key) is False for key in _authority_false_fields()), "prior consumption leaked downstream authority", consumed_errors)
    consumed_at = _parse_timestamp(consumption.get("consumed_at"), "prior consumed_at", consumed_errors)
    if prior_approved is not None and prior_expires is not None and consumed_at is not None:
        _require(prior_approved <= consumed_at < prior_expires, "prior consumption was outside its authority window", consumed_errors)
    if consumed_errors:
        raise ValidationError(consumed_errors)

    failure_keys = {
        "schema_version", "outcome", "reason_code", "failed_phase", "http_status",
        "authorization_id", "authorization_path", "authorization_sha256",
        "authorization_consumed", "consumption_record_path", "consumption_record_sha256",
        "diagnosis_path", "diagnosis_sha256", "readiness_path", "readiness_sha256",
        "provider", "service", "project_sha256", "project_number_sha256",
        "runtime_bindings", "source_proof", "credential_mechanism",
        "credential_refresh_attempted", "network_called", "calls",
        "provider_response_bytes_total", "failed_response_bytes", "failed_response_sha256",
        "provider_error", "provider_identifiers", "provider_usage", "primary_failure",
        "pre_enable_readback", "enable_operation", "operation_completion",
        "post_enable_readback", "resolution_readback_failure", "mutation_attempted",
        "service_state_resolution", "enablement_may_have_completed",
        "operation_may_still_be_running", "manual_readback_required", "consumed_at",
        "started_at", "failed_at", "retries_made", "redirects_followed",
        "credentials_recorded", "raw_provider_responses_recorded",
        *_authority_false_fields().keys(),
    }
    _strict(failure, failure_keys, "prior service failure receipt")
    primary = _strict(
        failure.get("primary_failure"),
        {
            "phase", "http_status", "response_bytes", "response_sha256",
            "provider_error", "provider_identifiers", "provider_usage",
            "request_started_at", "request_completed_at",
        },
        "prior primary_failure",
    )
    source_proof = _strict(
        failure.get("source_proof"),
        {"git_head", "runtime_commit", "head_delta_policy", "head_delta_path"},
        "prior source_proof",
    )
    try:
        prior_head_delta_path = authorization_path.relative_to(_repository_root()).as_posix()
    except ValueError:
        prior_head_delta_path = authorization_path.relative_to(root).as_posix()
    failure_errors: list[str] = []
    _require(failure.get("schema_version") == PRIOR_FAILURE_RECEIPT_SCHEMA, "prior failure schema drifted", failure_errors)
    _require(failure.get("outcome") == "failed_closed" and failure.get("reason_code") == "provider_response_byte_cap_exceeded" and failure.get("failed_phase") == "pre_enable_readback" and failure.get("http_status") == 200, "prior failure classification drifted", failure_errors)
    _require(failure.get("authorization_id") == prior_id and failure.get("authorization_path") == binding["authorization_path"] and failure.get("authorization_sha256") == authorization_sha and failure.get("authorization_consumed") is True, "prior failure authorization binding drifted", failure_errors)
    _require(failure.get("consumption_record_path") == binding["consumption_record_path"] and failure.get("consumption_record_sha256") == consumption_sha, "prior failure consumption binding drifted", failure_errors)
    _require(failure.get("diagnosis_path") == diagnosis_relative and failure.get("diagnosis_sha256") == diagnosis_sha256 and failure.get("readiness_path") == readiness_relative and failure.get("readiness_sha256") == readiness_sha256, "prior failure evidence binding drifted", failure_errors)
    _require(failure.get("provider") == PROVIDER and failure.get("service") == SERVICE and failure.get("project_sha256") == target["project_sha256"] and failure.get("project_number_sha256") == target["project_number_sha256"], "prior failure target drifted", failure_errors)
    _require(_exact(failure.get("runtime_bindings"), prior_runtime), "prior failure runtime binding drifted", failure_errors)
    _require(source_proof.get("git_head") == binding["authorization_commit"] and source_proof.get("runtime_commit") == binding["prior_runtime_commit"] and source_proof.get("head_delta_policy") == "exact_active_authorization_path_only" and source_proof.get("head_delta_path") == prior_head_delta_path, "prior failure source proof drifted", failure_errors)
    _require(failure.get("credential_mechanism") == CREDENTIAL_MECHANISM and failure.get("credential_refresh_attempted") is True and failure.get("network_called") is True, "prior failure provider boundary drifted", failure_errors)
    _require(_exact(failure.get("calls"), _PRIOR_FAILURE_CALLS), "prior failure call counts do not prove zero mutation", failure_errors)
    prefix_sha = failure.get("failed_response_sha256")
    _require(failure.get("provider_response_bytes_total") == _PRIOR_FAILURE_RESPONSE_BYTES and failure.get("failed_response_bytes") == _PRIOR_FAILURE_RESPONSE_BYTES and isinstance(prefix_sha, str) and bool(_SHA_RE.fullmatch(prefix_sha)) and prefix_sha == binding["captured_cap_plus_one_prefix_sha256"], "prior bounded cap-plus-one prefix evidence drifted", failure_errors)
    _require(failure.get("provider_error") is None and failure.get("provider_identifiers") == {} and failure.get("provider_usage") == {}, "prior failure safe provider evidence drifted", failure_errors)
    _require(failure.get("pre_enable_readback") is None and failure.get("enable_operation") is None and failure.get("operation_completion") is None and failure.get("post_enable_readback") is None and failure.get("resolution_readback_failure") is None, "prior failure contains ineligible service evidence", failure_errors)
    _require(failure.get("mutation_attempted") is False and failure.get("service_state_resolution") == "not_attempted" and failure.get("enablement_may_have_completed") is False and failure.get("operation_may_still_be_running") is False and failure.get("manual_readback_required") is False, "prior failure does not prove a pre-mutation stop", failure_errors)
    _require(_exact(failure.get("retries_made"), 0) and _exact(failure.get("redirects_followed"), 0) and failure.get("credentials_recorded") is False and failure.get("raw_provider_responses_recorded") is False, "prior failure containment drifted", failure_errors)
    _require(all(failure.get(key) is False for key in _authority_false_fields()), "prior failure leaked downstream authority", failure_errors)
    _require(primary.get("phase") == "pre_enable_readback" and primary.get("http_status") == 200 and primary.get("response_bytes") == _PRIOR_FAILURE_RESPONSE_BYTES and primary.get("response_sha256") == prefix_sha and primary.get("provider_error") is None and primary.get("provider_identifiers") == {} and primary.get("provider_usage") == {}, "prior primary failure evidence drifted", failure_errors)
    failure_consumed = _parse_timestamp(failure.get("consumed_at"), "prior failure consumed_at", failure_errors)
    failure_started = _parse_timestamp(failure.get("started_at"), "prior failure started_at", failure_errors)
    request_started = _parse_timestamp(primary.get("request_started_at"), "prior request_started_at", failure_errors)
    request_completed = _parse_timestamp(primary.get("request_completed_at"), "prior request_completed_at", failure_errors)
    failed_at = _parse_timestamp(failure.get("failed_at"), "prior failed_at", failure_errors)
    if all(value is not None for value in (consumed_at, failure_consumed, failure_started, request_started, request_completed, failed_at, prior_expires)):
        assert consumed_at is not None and failure_consumed is not None and failure_started is not None
        assert request_started is not None and request_completed is not None and failed_at is not None and prior_expires is not None
        _require(consumed_at == failure_consumed <= failure_started == request_started <= request_completed <= failed_at < prior_expires, "prior failure timestamps are incoherent", failure_errors)
    if failure_errors:
        raise ValidationError(failure_errors)

    _strict(
        disposition,
        {"schema_version", "record_id", "status", "recorded_at", "attempt_binding", "observed_outcome", "interpretation", "repair_gate", "authority"},
        "prior failure disposition",
    )
    attempt = _strict(
        disposition.get("attempt_binding"),
        {"authorization_path", "authorization_sha256", "authorization_commit", "runtime_commit", "consumption_path", "consumption_sha256", "failure_receipt_path", "failure_receipt_sha256"},
        "prior disposition attempt_binding",
    )
    observed = _strict(
        disposition.get("observed_outcome"),
        {"authorization_consumed", "outcome", "reason_code", "failed_phase", "http_status", "calls", "bounded_response_bytes_read", "provider_response_bytes_total_recorded", "captured_cap_plus_one_prefix_sha256", "mutation_attempted", "service_state_resolution", "enablement_may_have_completed", "operation_may_still_be_running", "manual_readback_required", "retries_made", "redirects_followed", "raw_provider_response_stored"},
        "prior disposition observed_outcome",
    )
    interpretation = _strict(
        disposition.get("interpretation"),
        {"established", "safe_conclusion", "cause_of_large_response", "full_provider_response_length_known", "service_state_parsed_from_this_attempt", "target_service_state_after_this_attempt", "service_enable_request_sent", "service_mutation_occurred", "provider_managed_enablement_side_effect_possible_for_this_attempt", "direct_iam_api_call_or_mutation_occurred"},
        "prior disposition interpretation",
    )
    repair_gate = _strict(
        disposition.get("repair_gate"),
        {"repair_class", "execution_semantics", "existing_authorization_reusable", "automatic_retry_permitted", "new_active_authorization_required", "prior_outcome_commit_required", "new_runtime_and_adversarial_audit_required", "g1r2_synthetic_guide_authorized"},
        "prior disposition repair_gate",
    )
    disposition_errors: list[str] = []
    _require(disposition.get("schema_version") == PRIOR_DISPOSITION_SCHEMA and disposition.get("status") == "immutable_local_disposition" and isinstance(disposition.get("record_id"), str) and bool(disposition["record_id"]), "prior disposition identity drifted", disposition_errors)
    expected_attempt = {
        "authorization_path": binding["authorization_path"],
        "authorization_sha256": authorization_sha,
        "authorization_commit": binding["authorization_commit"],
        "runtime_commit": binding["prior_runtime_commit"],
        "consumption_path": binding["consumption_record_path"],
        "consumption_sha256": consumption_sha,
        "failure_receipt_path": binding["failure_receipt_path"],
        "failure_receipt_sha256": failure_sha,
    }
    _require(_exact(attempt, expected_attempt), "prior disposition artifact chain drifted", disposition_errors)
    expected_observed = {
        "authorization_consumed": True,
        "outcome": "failed_closed",
        "reason_code": "provider_response_byte_cap_exceeded",
        "failed_phase": "pre_enable_readback",
        "http_status": 200,
        "calls": _PRIOR_FAILURE_CALLS,
        "bounded_response_bytes_read": _PRIOR_FAILURE_RESPONSE_BYTES,
        "provider_response_bytes_total_recorded": _PRIOR_FAILURE_RESPONSE_BYTES,
        "captured_cap_plus_one_prefix_sha256": prefix_sha,
        "mutation_attempted": False,
        "service_state_resolution": "not_attempted",
        "enablement_may_have_completed": False,
        "operation_may_still_be_running": False,
        "manual_readback_required": False,
        "retries_made": 0,
        "redirects_followed": 0,
        "raw_provider_response_stored": False,
    }
    _require(_exact(observed, expected_observed), "prior disposition observed outcome drifted", disposition_errors)
    expected_interpretation = {
        "established": _PRIOR_ESTABLISHED,
        "safe_conclusion": _PRIOR_SAFE_CONCLUSION,
        "cause_of_large_response": "unknown",
        "full_provider_response_length_known": False,
        "service_state_parsed_from_this_attempt": False,
        "target_service_state_after_this_attempt": "unknown_from_this_attempt",
        "service_enable_request_sent": False,
        "service_mutation_occurred": False,
        "provider_managed_enablement_side_effect_possible_for_this_attempt": False,
        "direct_iam_api_call_or_mutation_occurred": False,
    }
    _require(_exact(interpretation, expected_interpretation), "prior disposition interpretation drifted", disposition_errors)
    expected_gate = {
        "repair_class": "bounded_partial_response_handling",
        "execution_semantics": _PRIOR_EXECUTION_SEMANTICS,
        "existing_authorization_reusable": False,
        "automatic_retry_permitted": False,
        "new_active_authorization_required": True,
        "prior_outcome_commit_required": True,
        "new_runtime_and_adversarial_audit_required": True,
        "g1r2_synthetic_guide_authorized": False,
    }
    _require(_exact(repair_gate, expected_gate), "prior disposition repair gate drifted", disposition_errors)
    _require(_exact(disposition.get("authority"), _DRAFT_AUTHORITY), "prior disposition carries authority", disposition_errors)
    disposition_recorded = _parse_timestamp(disposition.get("recorded_at"), "prior disposition recorded_at", disposition_errors)
    if disposition_recorded is not None and failed_at is not None:
        _require(failed_at <= disposition_recorded <= _now(), "prior disposition timestamp is incoherent", disposition_errors)
    if disposition_errors:
        raise ValidationError(disposition_errors)

    return (
        authorization_path,
        authorization_sha,
        consumption_path,
        consumption_sha,
        failure_path,
        failure_sha,
        disposition_path,
        disposition_sha,
    )


def _validate_authorization(
    authorization_path: Path,
    *,
    require_active: bool,
) -> _Contract:
    authorization_path = Path(authorization_path).absolute()
    root = pt._document_root(authorization_path)
    authorization, _authorization_bytes, authorization_sha = _read_fixture_json(
        root,
        authorization_path,
        "service-enablement authorization",
    )
    _strict(
        authorization,
        {
            "schema_version",
            "authorization_id",
            "status",
            "approved",
            "scope",
            "target",
            "diagnosis_binding",
            "readiness_binding",
            "prior_attempt_binding",
            "runtime_bindings",
            "action",
            "prospective_active_limits",
            "authorized_limits",
            "artifacts",
            "required_success_evidence",
            "approved_by",
            "approved_at",
            "expires_at",
            "execution_ready",
            "blockers",
            "authority",
        },
        "service-enablement authorization",
    )
    errors = [
        item
        for item in pt._scan_for_secrets(
            authorization,
            "service_enablement_authorization",
        )
        if ".action.project_identity_source " not in item
        and ".required_success_evidence.raw_project_identifier_forbidden " not in item
    ]
    _require(authorization.get("schema_version") == AUTH_SCHEMA, "schema_version drifted", errors)
    auth_id = authorization.get("authorization_id")
    _require(
        isinstance(auth_id, str) and bool(_ID_RE.fullmatch(auth_id)),
        "authorization_id is invalid",
        errors,
    )
    status = authorization.get("status")
    _require(status in {"draft", "active"}, "status must be draft or active", errors)
    _require(authorization.get("scope") == SCOPE, "scope drifted", errors)
    target = _strict(
        authorization.get("target"),
        {"project_sha256", "project_number_sha256", "service"},
        "target",
    )
    _require(
        isinstance(target.get("project_sha256"), str)
        and bool(_SHA_RE.fullmatch(target["project_sha256"])),
        "target.project_sha256 must be an exact SHA-256",
        errors,
    )
    _require(target.get("service") == SERVICE, "target.service drifted", errors)
    _require(
        isinstance(target.get("project_number_sha256"), str)
        and bool(_SHA_RE.fullmatch(target["project_number_sha256"])),
        "target.project_number_sha256 must be exact",
        errors,
    )

    diagnosis_binding = _strict(
        authorization.get("diagnosis_binding"),
        {"path", "sha256", "project_sha256", "reported_current_state", "causal_status"},
        "diagnosis_binding",
    )
    _require(
        diagnosis_binding.get("project_sha256") == target.get("project_sha256"),
        "diagnosis_binding.project_sha256 drifted",
        errors,
    )
    _require(
        isinstance(diagnosis_binding.get("sha256"), str)
        and bool(_SHA_RE.fullmatch(diagnosis_binding["sha256"])),
        "diagnosis_binding.sha256 must be exact",
        errors,
    )
    _require(
        diagnosis_binding.get("reported_current_state") == "DISABLED",
        "diagnosis must report DISABLED",
        errors,
    )
    _require(
        diagnosis_binding.get("causal_status")
        == "only_confirmed_configuration_anomaly_not_proven_403_cause",
        "diagnosis causal boundary drifted",
        errors,
    )

    readiness_binding = _strict(
        authorization.get("readiness_binding"),
        {
            "path",
            "sha256",
            "project_sha256",
            "project_number_sha256",
            "permission",
            "permission_granted",
        },
        "readiness_binding",
    )
    _require(
        readiness_binding.get("project_sha256") == target.get("project_sha256")
        and readiness_binding.get("project_number_sha256")
        == target.get("project_number_sha256"),
        "readiness project bindings drifted",
        errors,
    )
    _require(
        isinstance(readiness_binding.get("sha256"), str)
        and bool(_SHA_RE.fullmatch(readiness_binding["sha256"])),
        "readiness_binding.sha256 must be exact",
        errors,
    )
    _require(
        readiness_binding.get("permission") == "serviceusage.services.enable"
        and readiness_binding.get("permission_granted") is True,
        "readiness permission must be exact and granted",
        errors,
    )
    prior_attempt_binding = authorization.get("prior_attempt_binding")

    runtime_bindings = _strict(
        authorization.get("runtime_bindings"),
        {
            "git_commit",
            "executor_path",
            "executor_sha256",
            "credential_runtime_path",
            "credential_runtime_sha256",
            "cli_path",
            "cli_sha256",
            "core_path",
            "core_sha256",
            "init_path",
            "init_sha256",
            "schema_path",
            "schema_sha256",
        },
        "runtime_bindings",
    )
    _require(
        runtime_bindings.get("executor_path") == EXECUTOR_RELATIVE
        and runtime_bindings.get("credential_runtime_path") == CREDENTIAL_RUNTIME_RELATIVE
        and runtime_bindings.get("cli_path") == CLI_RELATIVE
        and runtime_bindings.get("core_path") == CORE_RELATIVE
        and runtime_bindings.get("init_path") == INIT_RELATIVE
        and runtime_bindings.get("schema_path") == SCHEMA_RELATIVE,
        "runtime binding paths drifted",
        errors,
    )

    _require(_exact(authorization.get("action"), _ACTION), "authorized action drifted", errors)
    _require(
        _exact(authorization.get("prospective_active_limits"), _ACTIVE_LIMITS),
        "prospective active limits drifted",
        errors,
    )
    required_evidence = authorization.get("required_success_evidence")
    _require(
        _exact(required_evidence, _REQUIRED_SUCCESS_EVIDENCE),
        "required success evidence drifted",
        errors,
    )
    blockers = authorization.get("blockers")
    _require(
        isinstance(blockers, list)
        and all(isinstance(item, str) and bool(item) for item in blockers),
        "blockers must be non-empty strings",
        errors,
    )

    approved_at: datetime | None = None
    expires_at: datetime | None = None
    if status == "draft":
        _require(authorization.get("approved") is False, "draft approved must be false", errors)
        _require(
            authorization.get("execution_ready") is False,
            "draft execution_ready must be false",
            errors,
        )
        _require(authorization.get("approved_by") == "", "draft approved_by must be empty", errors)
        _require(authorization.get("approved_at") == "", "draft approved_at must be empty", errors)
        _require(authorization.get("expires_at") == "", "draft expires_at must be empty", errors)
        _require(bool(blockers), "draft requires blockers", errors)
        _require(
            _exact(authorization.get("authorized_limits"), _ZERO_LIMITS),
            "draft authorized limits must all be zero",
            errors,
        )
        _require(
            _exact(authorization.get("authority"), _DRAFT_AUTHORITY),
            "draft must carry no authority",
            errors,
        )
        expected_runtime = _expected_runtime_bindings(draft=True)
        _require(
            _exact(runtime_bindings, expected_runtime),
            "draft runtime bindings must be pending and path-exact",
            errors,
        )
    elif status == "active":
        _require(authorization.get("approved") is True, "active approved must be true", errors)
        _require(
            authorization.get("execution_ready") is True,
            "active execution_ready must be true",
            errors,
        )
        _require(
            isinstance(authorization.get("approved_by"), str)
            and bool(authorization["approved_by"]),
            "active approved_by is required",
            errors,
        )
        approved_at = _parse_timestamp(authorization.get("approved_at"), "approved_at", errors)
        expires_at = _parse_timestamp(authorization.get("expires_at"), "expires_at", errors)
        now = _now()
        if approved_at is not None and expires_at is not None:
            _require(approved_at <= now < expires_at, "active authorization is outside its window", errors)
            _require(
                (expires_at - approved_at).total_seconds() <= MAX_AUTHORIZATION_WINDOW_SECONDS,
                "active authorization window exceeds 24 hours",
                errors,
            )
        _require(blockers == [], "active authorization blockers must be empty", errors)
        _require(
            _exact(authorization.get("authorized_limits"), _ACTIVE_LIMITS),
            "active authorized limits drifted",
            errors,
        )
        _require(
            _exact(authorization.get("authority"), _ACTIVE_AUTHORITY),
            "active authority drifted",
            errors,
        )
        for key in (
            "executor_sha256",
            "credential_runtime_sha256",
            "cli_sha256",
            "core_sha256",
            "init_sha256",
            "schema_sha256",
        ):
            _require(
                isinstance(runtime_bindings.get(key), str)
                and bool(_SHA_RE.fullmatch(runtime_bindings[key])),
                f"runtime_bindings.{key} must be exact",
                errors,
            )
        _require(
            isinstance(runtime_bindings.get("git_commit"), str)
            and bool(_GIT_COMMIT_RE.fullmatch(runtime_bindings["git_commit"])),
            "runtime_bindings.git_commit must be exact",
            errors,
        )
        if all(
            isinstance(runtime_bindings.get(key), str)
            and bool(_SHA_RE.fullmatch(runtime_bindings[key]))
            for key in (
                "executor_sha256",
                "credential_runtime_sha256",
                "cli_sha256",
                "core_sha256",
                "init_sha256",
                "schema_sha256",
            )
        ):
            _require(
                runtime_bindings["executor_sha256"] == sha256_file(Path(__file__).absolute())
                and runtime_bindings["credential_runtime_sha256"]
                == sha256_file(Path(pt.__file__).absolute())
                and runtime_bindings["cli_sha256"]
                == sha256_file(Path(__file__).with_name("cli.py"))
                and runtime_bindings["core_sha256"]
                == sha256_file(Path(__file__).with_name("core.py"))
                and runtime_bindings["init_sha256"]
                == sha256_file(Path(__file__).with_name("__init__.py"))
                and runtime_bindings["schema_sha256"]
                == sha256_file(
                    Path(__file__).resolve().parents[2]
                    / "schemas"
                    / "google-service-enablement-authorization.schema.json"
                ),
                "active runtime hashes do not match loaded runtime bytes",
                errors,
            )
        _require(
            isinstance(approved_at, datetime)
            and isinstance(expires_at, datetime)
            and approved_at <= expires_at,
            "active authorization timestamps are incoherent",
            errors,
        )

    if not isinstance(auth_id, str):
        auth_id = "invalid"
    artifacts = _strict(
        authorization.get("artifacts"),
        {"consumption_record_path", "success_receipt_path", "failure_receipt_path"},
        "artifacts",
    )
    expected_artifacts = _expected_artifacts(auth_id)
    _require(_exact(artifacts, expected_artifacts), "artifact paths must derive exactly from authorization_id", errors)
    for key, prefix in (
        ("consumption_record_path", ("authorizations", "consumed")),
        ("success_receipt_path", ("receipts", "google-service-usage")),
        ("failure_receipt_path", ("receipts", "google-service-usage")),
    ):
        value = artifacts.get(key)
        if isinstance(value, str):
            try:
                path = pt._safe_relative(root, value, f"artifacts.{key}", must_exist=False, suffix=".json")
                _require(
                    path.relative_to(root).parts[:2] == prefix,
                    f"artifacts.{key} is outside its exact directory",
                    errors,
                )
                _require(
                    not path.exists() and not path.is_symlink(),
                    f"artifacts.{key} must not already exist",
                    errors,
                )
            except (ValidationError, ValueError) as exc:
                errors.extend(exc.errors if isinstance(exc, ValidationError) else [f"artifacts.{key} is unsafe"])

    if errors:
        raise ValidationError(errors)
    diagnosis_path, diagnosis_sha = _validate_diagnosis(root, diagnosis_binding)
    readiness_path, readiness_sha = _validate_readiness(root, readiness_binding)
    (
        prior_authorization_path,
        prior_authorization_sha,
        prior_consumption_path,
        prior_consumption_sha,
        prior_failure_path,
        prior_failure_sha,
        disposition_path,
        disposition_sha,
    ) = _validate_prior_attempt(
        root,
        prior_attempt_binding,
        target=target,
        diagnosis_relative=diagnosis_path.relative_to(root).as_posix(),
        diagnosis_sha256=diagnosis_sha,
        readiness_relative=readiness_path.relative_to(root).as_posix(),
        readiness_sha256=readiness_sha,
    )
    if require_active and status != "active":
        raise ValidationError("service enablement execution requires an exact active authorization")
    return _Contract(
        root=root,
        authorization_path=authorization_path,
        authorization=authorization,
        authorization_sha256=authorization_sha,
        diagnosis_path=diagnosis_path,
        diagnosis_sha256=diagnosis_sha,
        readiness_path=readiness_path,
        readiness_sha256=readiness_sha,
        prior_authorization_path=prior_authorization_path,
        prior_authorization_sha256=prior_authorization_sha,
        prior_consumption_path=prior_consumption_path,
        prior_consumption_sha256=prior_consumption_sha,
        prior_failure_path=prior_failure_path,
        prior_failure_sha256=prior_failure_sha,
        disposition_path=disposition_path,
        disposition_sha256=disposition_sha,
        consumption_relative=artifacts["consumption_record_path"],
        success_relative=artifacts["success_receipt_path"],
        failure_relative=artifacts["failure_receipt_path"],
        approved_at=approved_at,
        expires_at=expires_at,
    )


def validate_google_service_enablement_authorization(authorization_path: Path) -> dict[str, Any]:
    """Validate an inert DRAFT or exact ACTIVE authority without credentials/network."""

    contract = _validate_authorization(authorization_path, require_active=False)
    status = contract.authorization["status"]
    return {
        "schema_version": DRY_RUN_SCHEMA,
        "valid": True,
        "authorization_id": contract.authorization["authorization_id"],
        "authorization_sha256": contract.authorization_sha256,
        "authorization_status": status,
        "scope": SCOPE,
        "provider": PROVIDER,
        "service": SERVICE,
        "project_sha256": contract.authorization["target"]["project_sha256"],
        "project_number_sha256": contract.authorization["target"]["project_number_sha256"],
        "diagnosis_binding": {
            "path": contract.diagnosis_path.relative_to(contract.root).as_posix(),
            "sha256": contract.diagnosis_sha256,
            "reported_current_state": "DISABLED",
            "causal_status": "only_confirmed_configuration_anomaly_not_proven_403_cause",
        },
        "readiness_binding": {
            "path": contract.readiness_path.relative_to(contract.root).as_posix(),
            "sha256": contract.readiness_sha256,
            "project_sha256": contract.authorization["target"]["project_sha256"],
            "project_number_sha256": contract.authorization["target"]["project_number_sha256"],
            "permission": "serviceusage.services.enable",
            "permission_granted": True,
        },
        "prior_attempt_binding": contract.authorization["prior_attempt_binding"],
        "runtime_bindings": contract.authorization["runtime_bindings"],
        "action": _ACTION,
        "authorized_limits": contract.authorization["authorized_limits"],
        "artifacts": contract.authorization["artifacts"],
        "provider_action_authorized": status == "active",
        "network_authorized": status == "active",
        "execution_transport_available": status == "active",
        "credentials_accessed": False,
        "network_called": False,
        "service_mutations_made": 0,
        "synthetic_guide_calls_made": 0,
        "authority": contract.authorization["authority"],
    }


def dry_run_google_service_enablement(authorization_path: Path) -> dict[str, Any]:
    return validate_google_service_enablement_authorization(authorization_path)


def _private_project_bindings(authorization: dict[str, Any]) -> tuple[str, str]:
    value = os.environ.get(PROJECT_ENV)
    number = os.environ.get(PROJECT_NUMBER_ENV)
    failure: str | None = None
    if (
        not isinstance(value, str)
        or not bool(_PROJECT_RE.fullmatch(value))
        or value != value.strip()
    ):
        failure = "private Google project binding is absent or malformed"
    elif sha256_bytes(value.encode("utf-8")) != authorization["target"]["project_sha256"]:
        failure = "private Google project binding does not match service authority"
    elif (
        not isinstance(number, str)
        or not bool(_PROJECT_NUMBER_RE.fullmatch(number))
        or sha256_bytes(number.encode("ascii"))
        != authorization["target"]["project_number_sha256"]
    ):
        failure = "private Google project-number binding does not match service authority"
    if failure is not None:
        value = None
        number = None
        raise ValidationError(failure) from None
    assert isinstance(value, str)
    assert isinstance(number, str)
    return value, number


def _repository_root() -> Path:
    return Path(__file__).resolve().parents[4]


def _git(command: list[str], *, max_bytes: int = 2_000_000) -> bytes:
    result: Any = None
    stdout = b""
    failure = False
    try:
        result = subprocess.run(
            ["git", *command],
            cwd=_repository_root(),
            check=False,
            capture_output=True,
            text=False,
            timeout=15,
            env=pt._minimal_gcloud_environment(),
        )
        stdout = result.stdout if isinstance(result.stdout, bytes) else b""
        failure = (
            type(result.returncode) is not int
            or result.returncode != 0
            or len(stdout) > max_bytes
            or not isinstance(result.stderr, bytes)
            or len(result.stderr) > max_bytes
        )
    except Exception:
        failure = True
    if failure:
        result = None
        stdout = b""
        raise ValidationError("committed runtime preflight failed") from None
    result = None
    return stdout


def _verify_committed_runtime(contract: _Contract) -> dict[str, str]:
    """Prove the loaded runtime and authority are exact committed bytes."""

    bindings = contract.authorization["runtime_bindings"]
    repository = _repository_root()
    paths = {
        "executor": (EXECUTOR_RELATIVE, bindings["executor_sha256"]),
        "credential_runtime": (
            CREDENTIAL_RUNTIME_RELATIVE,
            bindings["credential_runtime_sha256"],
        ),
        "cli": (CLI_RELATIVE, bindings["cli_sha256"]),
        "core": (CORE_RELATIVE, bindings["core_sha256"]),
        "init": (INIT_RELATIVE, bindings["init_sha256"]),
        "schema": (SCHEMA_RELATIVE, bindings["schema_sha256"]),
    }
    head = _git(["rev-parse", "HEAD"]).strip().decode("ascii", errors="strict")
    commit = bindings["git_commit"]
    try:
        auth_relative = contract.authorization_path.relative_to(repository).as_posix()
        diagnosis_relative = contract.diagnosis_path.relative_to(repository).as_posix()
        readiness_relative = contract.readiness_path.relative_to(repository).as_posix()
        prior_authorization_relative = contract.prior_authorization_path.relative_to(repository).as_posix()
        prior_consumption_relative = contract.prior_consumption_path.relative_to(repository).as_posix()
        prior_failure_relative = contract.prior_failure_path.relative_to(repository).as_posix()
        disposition_relative = contract.disposition_path.relative_to(repository).as_posix()
    except ValueError:
        raise ValidationError("authority chain is outside the committed repository") from None
    _git(["merge-base", "--is-ancestor", commit, head])
    prior_binding = contract.authorization["prior_attempt_binding"]
    prior_runtime_commit = prior_binding["prior_runtime_commit"]
    prior_authorization_commit = prior_binding["authorization_commit"]
    _git(["merge-base", "--is-ancestor", prior_runtime_commit, prior_authorization_commit])
    _git(["merge-base", "--is-ancestor", prior_authorization_commit, commit])
    prior_delta = _git(
        [
            "diff",
            "--name-only",
            "--diff-filter=ACDMRTUXB",
            "-z",
            f"{prior_runtime_commit}..{prior_authorization_commit}",
        ]
    )
    if prior_delta != prior_authorization_relative.encode("utf-8") + b"\x00":
        raise ValidationError(
            "prior runtime-to-authorization delta must be exactly the prior ACTIVE path"
        )
    prior_committed_authorization = _git(
        ["show", f"{prior_authorization_commit}:{prior_authorization_relative}"]
    )
    _prior_value, prior_authorization_bytes, prior_authorization_sha = _read_fixture_json(
        contract.root,
        contract.prior_authorization_path,
        "prior active service authorization",
    )
    if (
        prior_committed_authorization != prior_authorization_bytes
        or prior_authorization_sha != contract.prior_authorization_sha256
    ):
        raise ValidationError("prior ACTIVE authorization history is not exact")
    head_delta = _git(
        [
            "diff",
            "--name-only",
            "--diff-filter=ACDMRTUXB",
            "-z",
            f"{commit}..{head}",
        ]
    )
    if head_delta != auth_relative.encode("utf-8") + b"\x00":
        raise ValidationError(
            "runtime commit to HEAD delta must be exactly the active authorization path"
        )
    _auth_value, auth_bytes, auth_sha = _read_fixture_json(
        contract.root,
        contract.authorization_path,
        "active service authorization",
    )
    committed_auth = _git(["show", f"HEAD:{auth_relative}"])
    if committed_auth != auth_bytes or auth_sha != contract.authorization_sha256:
        raise ValidationError("active authorization is not committed exactly")
    for path, relative, expected_sha, label in (
        (
            contract.diagnosis_path,
            diagnosis_relative,
            contract.diagnosis_sha256,
            "diagnosis evidence",
        ),
        (
            contract.readiness_path,
            readiness_relative,
            contract.readiness_sha256,
            "readiness evidence",
        ),
        (
            contract.prior_authorization_path,
            prior_authorization_relative,
            contract.prior_authorization_sha256,
            "prior active service authorization",
        ),
        (
            contract.prior_consumption_path,
            prior_consumption_relative,
            contract.prior_consumption_sha256,
            "prior service consumption",
        ),
        (
            contract.prior_failure_path,
            prior_failure_relative,
            contract.prior_failure_sha256,
            "prior service failure receipt",
        ),
        (
            contract.disposition_path,
            disposition_relative,
            contract.disposition_sha256,
            "prior failure disposition",
        ),
    ):
        _value, current_bytes, current_sha = _read_fixture_json(
            contract.root,
            path,
            label,
        )
        committed_bytes = _git(["show", f"{commit}:{relative}"])
        if current_sha != expected_sha or current_bytes != committed_bytes:
            raise ValidationError(f"{label} is not committed exactly at the runtime commit")
    for relative, expected_sha in paths.values():
        current = repository / relative
        try:
            if sha256_file(current) != expected_sha:
                raise ValidationError("loaded runtime binding drifted")
        except OSError:
            raise ValidationError("loaded runtime binding is unavailable") from None
        committed = _git(["show", f"{commit}:{relative}"])
        if sha256_bytes(committed) != expected_sha or committed != current.read_bytes():
            raise ValidationError("loaded runtime is not the exact committed binding")
    dirty = _git(["status", "--porcelain=v1", "--untracked-files=all"])
    if dirty:
        raise ValidationError("repository worktree must be globally clean before service mutation")
    return {
        "git_head": head,
        "runtime_commit": commit,
        "head_delta_policy": "exact_active_authorization_path_only",
        "head_delta_path": auth_relative,
    }


def _preflight_paths(contract: _Contract) -> None:
    for label, relative in (
        ("consumption record", contract.consumption_relative),
        ("success receipt", contract.success_relative),
        ("failure receipt", contract.failure_relative),
    ):
        pt._safe_execution_relative(contract.root, relative, label, ".json")


def _safe_headers(value: Any) -> dict[str, str]:
    return pt._response_headers(value)


def _read_capped(response: Any, headers: dict[str, str]) -> tuple[bytes, str | None]:
    declared = headers.get("content-length")
    if declared is not None:
        if not declared.isascii() or not declared.isdigit():
            return b"", "provider_content_length_invalid"
        if int(declared) > MAX_RESPONSE_BYTES_PER_CALL:
            return b"", "provider_response_byte_cap_exceeded"
    chunks: list[bytes] = []
    chunk = b""
    received = 0
    failure: str | None = None
    try:
        while True:
            remaining = MAX_RESPONSE_BYTES_PER_CALL + 1 - received
            if remaining <= 0:
                failure = "provider_response_byte_cap_exceeded"
                break
            chunk = response.read(min(65_536, remaining))
            if not isinstance(chunk, bytes):
                failure = "provider_response_stream_invalid"
                break
            if not chunk:
                break
            chunks.append(chunk)
            received += len(chunk)
            if received > MAX_RESPONSE_BYTES_PER_CALL:
                failure = "provider_response_byte_cap_exceeded"
                break
    except Exception:
        failure = "provider_response_stream_invalid"
    raw = b"".join(chunks)
    chunks = []
    chunk = b""
    if failure is None and declared is not None and len(raw) != int(declared):
        failure = "provider_response_truncated"
    return raw, failure


def _safe_error(raw: bytes, headers: dict[str, str]) -> dict[str, Any] | None:
    """Reduce Google Status/ErrorInfo to service-specific safe fields only."""

    content_type = headers.get("content-type", "").split(";", 1)[0].strip().lower()
    content_encoding = headers.get("content-encoding", "identity").strip().lower()
    if not raw or content_type != "application/json" or content_encoding not in {"", "identity"}:
        return None
    try:
        payload = pt._strict_json_bytes(raw, "Google Service Usage error")
    except ValidationError:
        return None
    error = payload.get("error")
    if not isinstance(error, dict):
        return None
    result: dict[str, Any] = {}
    code = error.get("code")
    if type(code) is int and 100 <= code <= 599:
        result["code"] = code
    status = error.get("status")
    if isinstance(status, str) and status in pt._GOOGLE_ERROR_STATUSES:
        result["status"] = status
    safe_details: list[dict[str, str]] = []
    details = error.get("details")
    if isinstance(details, list) and len(details) <= 32:
        for detail in details:
            if not isinstance(detail, dict) or detail.get("@type") != pt._GOOGLE_ERROR_INFO_TYPE:
                continue
            safe: dict[str, str] = {}
            reason = detail.get("reason")
            if isinstance(reason, str) and reason in pt._GOOGLE_ERROR_INFO_REASONS:
                safe["reason"] = reason
            domain = detail.get("domain")
            if isinstance(domain, str) and domain in pt._GOOGLE_ERROR_INFO_DOMAINS:
                safe["domain"] = domain
            metadata = detail.get("metadata")
            if isinstance(metadata, dict):
                service = metadata.get("service")
                if isinstance(service, str) and service in pt._GOOGLE_ERROR_SERVICES:
                    safe["service"] = service
                permission = metadata.get("permission")
                if permission in {
                    "serviceusage.services.enable",
                    "serviceusage.services.get",
                    "serviceusage.operations.get",
                }:
                    safe["permission"] = permission
            if safe and safe not in safe_details:
                safe_details.append(safe)
    if safe_details:
        result["error_info"] = safe_details
    return result or None


def _open_service_usage_request(request: urllib.request.Request, timeout: float) -> Any:
    return urllib.request.build_opener(_NoRedirect()).open(request, timeout=timeout)


def _perform_request(
    *,
    method: str,
    url: str,
    expected_url: str,
    body: bytes | None,
    token: str,
    project: str,
    timeout: float,
) -> _ServiceResponse:
    request: Any = None
    response: Any = None
    pending: _ServiceFailure | None = None
    headers: dict[str, str] = {}
    raw = b""
    payload: Any = None
    error_raw = b""
    identifiers: dict[str, str] = {}
    usage: dict[str, int] = {}
    final_url_getter: Any = None
    status_getter: Any = None
    close: Any = None
    if method not in {"GET", "POST"} or url != expected_url:
        pending = _ServiceFailure("request_binding_failed")
    elif method == "POST" and body != ENABLE_BODY:
        pending = _ServiceFailure("enable_body_binding_failed")
    elif method == "GET" and body is not None:
        pending = _ServiceFailure("readback_body_forbidden")
    else:
        try:
            request = urllib.request.Request(url, data=body, method=method)
            request.add_header("Authorization", f"Bearer {token}")
            request.add_header("Accept", "application/json")
            request.add_header("X-Goog-User-Project", project)
            if method == "POST":
                request.add_header("Content-Type", "application/json")
            response = _open_service_usage_request(request, timeout)
            status_getter = getattr(response, "getcode", None)
            status = status_getter() if callable(status_getter) else getattr(response, "status", None)
            headers = _safe_headers(getattr(response, "headers", {}))
            identifiers, usage = pt._safe_provider_evidence(headers, token, project)
            if type(status) is not int or status != 200:
                error_raw, error_code = _read_capped(response, headers)
                digest = sha256_bytes(error_raw) if error_raw else None
                diagnostic = _safe_error(error_raw, headers) if error_code is None else None
                raise _ServiceFailure(
                    error_code or "provider_http_failure",
                    http_status=status if type(status) is int else None,
                    response_bytes=len(error_raw),
                    response_sha256=digest,
                    provider_error=diagnostic,
                    provider_identifiers=identifiers,
                    provider_usage=usage,
                )
            final_url_getter = getattr(response, "geturl", None)
            if not callable(final_url_getter) or final_url_getter() != expected_url:
                raise _ServiceFailure("provider_redirect_forbidden", http_status=status)
            content_type = headers.get("content-type", "").split(";", 1)[0].strip().lower()
            content_encoding = headers.get("content-encoding", "identity").strip().lower()
            if content_type != "application/json":
                raise _ServiceFailure("provider_response_mime_invalid", http_status=status)
            if content_encoding not in {"", "identity"}:
                raise _ServiceFailure("provider_response_encoding_forbidden", http_status=status)
            raw, read_error = _read_capped(response, headers)
            if read_error is not None:
                raise _ServiceFailure(
                    read_error,
                    http_status=status,
                    response_bytes=len(raw),
                    response_sha256=sha256_bytes(raw) if raw else None,
                    provider_identifiers=identifiers,
                    provider_usage=usage,
                )
            try:
                payload = pt._strict_json_bytes(raw, "Google Service Usage response")
            except ValidationError:
                raise _ServiceFailure(
                    "provider_response_json_invalid",
                    http_status=status,
                    response_bytes=len(raw),
                    response_sha256=sha256_bytes(raw),
                    provider_identifiers=identifiers,
                    provider_usage=usage,
                ) from None
            return _ServiceResponse(
                response_bytes=len(raw),
                response_sha256=sha256_bytes(raw),
                payload=payload,
                provider_identifiers=identifiers,
                provider_usage=usage,
            )
        except _ServiceFailure as exc:
            exc.__cause__ = None
            exc.__context__ = None
            exc.__suppress_context__ = True
            pending = exc
        except urllib.error.HTTPError as exc:
            try:
                try:
                    headers = _safe_headers(exc.headers)
                    identifiers, usage = pt._safe_provider_evidence(headers, token, project)
                    error_raw, error_code = _read_capped(exc, headers)
                    digest = sha256_bytes(error_raw) if error_raw else None
                    diagnostic = _safe_error(error_raw, headers) if error_code is None else None
                    code = "provider_redirect_forbidden" if 300 <= exc.code < 400 else "provider_http_failure"
                    pending = _ServiceFailure(
                        error_code or code,
                        http_status=exc.code,
                        response_bytes=len(error_raw),
                        response_sha256=digest,
                        provider_error=diagnostic,
                        provider_identifiers=identifiers,
                        provider_usage=usage,
                    )
                except Exception:
                    pending = _ServiceFailure("provider_http_failure")
            finally:
                try:
                    exc.close()
                except Exception:
                    pass
        except (urllib.error.URLError, TimeoutError, OSError):
            pending = _ServiceFailure("provider_transport_failure")
        except Exception:
            pending = _ServiceFailure("provider_transport_failure")
        finally:
            if response is not None:
                close = getattr(response, "close", None)
                if callable(close):
                    try:
                        close()
                    except Exception:
                        pass
    if pending is None:
        pending = _ServiceFailure("provider_transport_failure")
    pending.__cause__ = None
    pending.__context__ = None
    pending.__suppress_context__ = True
    method = ""
    url = ""
    expected_url = ""
    body = b""
    token = ""
    project = ""
    request = None
    response = None
    headers = {}
    raw = b""
    payload = None
    error_raw = b""
    identifiers = {}
    usage = {}
    final_url_getter = None
    status_getter = None
    close = None
    raise pending from None


def _service_urls(project_number: str) -> tuple[str, str]:
    encoded = urllib.parse.quote(project_number, safe="")
    resource_url = f"{BASE_ENDPOINT}/projects/{encoded}/services/{SERVICE}"
    readback_url = f"{resource_url}?fields={READBACK_FIELDS}"
    return readback_url, f"{resource_url}:enable"


def _observed_service_state(
    response: _ServiceResponse,
    *,
    expected_resource_name: str,
) -> dict[str, Any]:
    payload = response.payload
    name = payload.get("name")
    state = payload.get("state")
    if set(payload) != {"name", "state"}:
        payload = {}
        raise _ServiceFailure(
            "service_readback_fields_invalid",
            response_bytes=response.response_bytes,
            response_sha256=response.response_sha256,
            provider_identifiers=response.provider_identifiers,
            provider_usage=response.provider_usage,
        ) from None
    if (
        not isinstance(name, str)
        or not bool(_RESOURCE_RE.fullmatch(name))
        or name != expected_resource_name
    ):
        payload = {}
        raise _ServiceFailure(
            "service_readback_resource_invalid",
            response_bytes=response.response_bytes,
            response_sha256=response.response_sha256,
            provider_identifiers=response.provider_identifiers,
            provider_usage=response.provider_usage,
        ) from None
    if state not in {"DISABLED", "ENABLED"}:
        payload = {}
        raise _ServiceFailure(
            "service_readback_state_invalid",
            response_bytes=response.response_bytes,
            response_sha256=response.response_sha256,
            provider_identifiers=response.provider_identifiers,
            provider_usage=response.provider_usage,
        ) from None
    payload = {}
    return {
        "state": state,
        "response_bytes": response.response_bytes,
        "response_sha256": response.response_sha256,
        "provider_identifiers": response.provider_identifiers,
        "provider_usage": response.provider_usage,
    }


def _service_state(
    response: _ServiceResponse,
    required: str,
    *,
    expected_resource_name: str,
) -> dict[str, Any]:
    evidence = _observed_service_state(
        response,
        expected_resource_name=expected_resource_name,
    )
    if evidence["state"] != required:
        raise _ServiceFailure(
            "service_readback_state_unexpected",
            response_bytes=response.response_bytes,
            response_sha256=response.response_sha256,
            provider_identifiers=response.provider_identifiers,
            provider_usage=response.provider_usage,
        ) from None
    return evidence


def _operation_state(
    response: _ServiceResponse,
    *,
    expected_name: str | None,
    expected_resource_name: str,
) -> tuple[str, bool, bool, dict[str, Any]]:
    payload = response.payload
    name = payload.get("name")
    done = payload.get("done", False)
    invalid = (
        not isinstance(name, str)
        or not bool(_OPERATION_RE.fullmatch(name))
        or (expected_name is not None and name != expected_name)
        or type(done) is not bool
    )
    has_error = "error" in payload
    has_response = "response" in payload
    union_invalid = (
        (done is False and (has_error or has_response))
        or (done is True and (has_error == has_response))
    )
    if invalid or union_invalid:
        payload = {}
        raise _ServiceFailure(
            "enable_operation_response_invalid",
            response_bytes=response.response_bytes,
            response_sha256=response.response_sha256,
            provider_identifiers=response.provider_identifiers,
            provider_usage=response.provider_usage,
        ) from None
    if done and has_error:
        provider_error = None
        if isinstance(payload.get("error"), dict):
            safe_error_bytes = pt._compact_json_bytes({"error": payload["error"]})
            provider_error = _safe_error(
                safe_error_bytes,
                {"content-type": "application/json", "content-encoding": "identity"},
            )
            safe_error_bytes = b""
        payload = {}
        raise _ServiceFailure(
            "enable_operation_failed",
            response_bytes=response.response_bytes,
            response_sha256=response.response_sha256,
            provider_error=provider_error,
            provider_identifiers=response.provider_identifiers,
            provider_usage=response.provider_usage,
            operation_terminal=True,
            operation_succeeded=False,
        ) from None
    if done:
        result = payload.get("response")
        service = result.get("service") if isinstance(result, dict) else None
        if (
            not isinstance(result, dict)
            or result.get("@type")
            != "type.googleapis.com/google.api.serviceusage.v1.EnableServiceResponse"
            or not isinstance(service, dict)
            or service.get("name") != expected_resource_name
            or service.get("state") != "ENABLED"
        ):
            payload = {}
            result = None
            service = None
            raise _ServiceFailure(
                "enable_operation_success_response_invalid",
                response_bytes=response.response_bytes,
                response_sha256=response.response_sha256,
                provider_identifiers=response.provider_identifiers,
                provider_usage=response.provider_usage,
                operation_terminal=True,
                operation_succeeded=False,
            ) from None
    summary = {
        "response_bytes": response.response_bytes,
        "response_sha256": response.response_sha256,
        "done": done,
        "terminal_result": "success" if done else None,
        "provider_identifiers": response.provider_identifiers,
        "provider_usage": response.provider_usage,
    }
    payload = {}
    return name, done, done, summary


def _authority_false_fields() -> dict[str, bool]:
    return {
        "service_disablement_authorized": False,
        "other_service_mutation_authorized": False,
        "iam_mutation_authorized": False,
        "billing_mutation_authorized": False,
        "project_hierarchy_mutation_authorized": False,
        "synthetic_guide_generation_authorized": False,
        "retry_authorized": False,
        "voice_transfer_authorized": False,
        "full_capture_authorized": False,
        "step3_authorized": False,
        "sharing_authorized": False,
        "publication_authorized": False,
    }


def _with_request_times(
    evidence: dict[str, Any],
    started_at: datetime,
    completed_at: datetime,
) -> dict[str, Any]:
    return {
        **evidence,
        "request_started_at": _iso(started_at),
        "request_completed_at": _iso(completed_at),
    }


def _failure_timestamp(value: datetime, anchors: tuple[datetime | None, ...]) -> datetime:
    """Reject a failure receipt timestamp that moves behind transaction evidence."""

    floor = max((item for item in anchors if item is not None), default=None)
    if floor is not None and value < floor:
        raise ValidationError("failure receipt clock moved backwards")
    return value


def execute_google_service_enablement(
    authorization_path: Path,
    *,
    timeout: float = REQUEST_TIMEOUT_SECONDS,
) -> dict[str, Any]:
    """Consume one exact ACTIVE authority and enable only the frozen service."""

    if type(timeout) not in {int, float} or isinstance(timeout, bool) or timeout <= 0 or timeout > REQUEST_TIMEOUT_SECONDS:
        raise ValidationError("timeout must be greater than zero and at most 30 seconds")

    contract: _Contract | None = None
    project = ""
    project_number = ""
    gcloud = ""
    source_proof: dict[str, str] = {}
    consumption: dict[str, Any] = {}
    consumption_bytes = b""
    consumption_sha = ""
    consumed_at: datetime | None = None
    setup_failed = False
    try:
        contract = _validate_authorization(authorization_path, require_active=True)
        _preflight_paths(contract)
        project, project_number = _private_project_bindings(contract.authorization)
        source_proof = _verify_committed_runtime(contract)
        gcloud = pt._preflight_google_adc()
        refreshed = _validate_authorization(authorization_path, require_active=True)
        if (
            refreshed.authorization_sha256 != contract.authorization_sha256
            or refreshed.root != contract.root
            or refreshed.diagnosis_sha256 != contract.diagnosis_sha256
            or refreshed.readiness_sha256 != contract.readiness_sha256
            or refreshed.prior_authorization_sha256 != contract.prior_authorization_sha256
            or refreshed.prior_consumption_sha256 != contract.prior_consumption_sha256
            or refreshed.prior_failure_sha256 != contract.prior_failure_sha256
            or refreshed.disposition_sha256 != contract.disposition_sha256
        ):
            raise ValidationError("service authority bindings changed during preflight")
        contract = refreshed
        pt._ensure_execution_parents(
            contract.root,
            [contract.consumption_relative, contract.success_relative, contract.failure_relative],
        )
        _preflight_paths(contract)
        if sha256_file(contract.authorization_path) != contract.authorization_sha256:
            raise ValidationError("service authority changed before consumption")
        consumed_at = _now()
        if (
            contract.approved_at is None
            or contract.expires_at is None
            or not contract.approved_at <= consumed_at < contract.expires_at
        ):
            raise ValidationError("service authority expired before consumption")
        consumption = {
            "schema_version": CONSUMPTION_SCHEMA,
            "authorization_id": contract.authorization["authorization_id"],
            "authorization_sha256": contract.authorization_sha256,
            "scope": SCOPE,
            "provider": PROVIDER,
            "service": SERVICE,
            "project_sha256": contract.authorization["target"]["project_sha256"],
            "project_number_sha256": contract.authorization["target"]["project_number_sha256"],
            "diagnosis_path": contract.diagnosis_path.relative_to(contract.root).as_posix(),
            "diagnosis_sha256": contract.diagnosis_sha256,
            "readiness_path": contract.readiness_path.relative_to(contract.root).as_posix(),
            "readiness_sha256": contract.readiness_sha256,
            "prior_attempt_binding": contract.authorization["prior_attempt_binding"],
            "runtime_bindings": contract.authorization["runtime_bindings"],
            "status": "consumed_before_network",
            "consumed_at": _iso(consumed_at),
            "consumed_before_network": True,
            "network_called_at_consumption": False,
            "reserved_limits": contract.authorization["authorized_limits"],
            "credentials_recorded": False,
            **_authority_false_fields(),
        }
        if pt._scan_for_secrets(consumption, "service_enablement_consumption"):
            raise ValidationError("refusing credential-bearing consumption record")
        consumption_bytes = pt._receipt_bytes(consumption)
        if (
            project.encode("utf-8") in consumption_bytes
            or project_number.encode("ascii") in consumption_bytes
        ):
            raise ValidationError("refusing raw project material in consumption record")
        pt._exclusive_fixture_write(contract.root, contract.consumption_relative, consumption_bytes)
        consumption_sha = sha256_bytes(consumption_bytes)
        pt._verify_private_fixture_artifact(
            contract.root,
            contract.consumption_relative,
            consumption_bytes,
            "service enablement consumption latch",
        )
    except Exception:
        setup_failed = True
    if setup_failed or contract is None or consumed_at is None:
        project = ""
        project_number = ""
        gcloud = ""
        contract = None
        consumption = {}
        consumption_bytes = b""
        source_proof = {}
        raise ValidationError("service enablement setup failed closed before provider access") from None

    calls = {
        "pre_enable_state_readbacks": 0,
        "enable_attempts": 0,
        "operation_polls": 0,
        "post_enable_state_readbacks": 0,
        "http_calls_total": 0,
    }
    total_response_bytes = 0
    pre_evidence: dict[str, Any] | None = None
    enable_evidence: dict[str, Any] | None = None
    operation_evidence: dict[str, Any] | None = None
    final_evidence: dict[str, Any] | None = None
    credential_refresh_attempted = False
    network_called = False
    started_at: datetime | None = None
    last_completed_at: datetime | None = consumed_at
    current_phase: str | None = None
    current_http_status: int | None = None
    current_response_bytes = 0
    current_response_sha256: str | None = None
    current_response_counted = False
    current_call_started_at: datetime | None = None
    current_call_completed_at: datetime | None = None
    current_provider_error: dict[str, Any] | None = None
    current_identifiers: dict[str, str] = {}
    current_usage: dict[str, int] = {}
    token = ""
    response: _ServiceResponse | None = None
    operation_name = ""
    operation_terminal = False
    operation_succeeded = False
    service_state_resolution = "not_attempted"
    enablement_may_have_completed = False
    operation_may_still_be_running = False
    manual_readback_required = False
    resolution_readback_failure: dict[str, Any] | None = None
    primary_failure: dict[str, Any] | None = None
    service_url = ""
    enable_url = ""

    def _verify_latch() -> None:
        pt._verify_private_fixture_artifact(
            contract.root,
            contract.consumption_relative,
            consumption_bytes,
            "service enablement consumption latch",
        )

    def _before_call(
        phase: str,
        *,
        operation_started_at: datetime | None = None,
    ) -> datetime:
        nonlocal started_at, current_phase, network_called
        nonlocal current_http_status, current_response_bytes, current_response_sha256
        nonlocal current_response_counted, current_provider_error
        nonlocal current_identifiers, current_usage
        nonlocal current_call_started_at, current_call_completed_at
        current_http_status = None
        current_response_bytes = 0
        current_response_sha256 = None
        current_response_counted = False
        current_provider_error = None
        current_identifiers = {}
        current_usage = {}
        current_call_started_at = None
        current_call_completed_at = None
        _verify_latch()
        _preflight_paths_after_consumption(contract)
        moment = _now()
        if (
            contract.expires_at is None
            or moment < consumed_at
            or (last_completed_at is not None and moment < last_completed_at)
            or moment >= contract.expires_at
        ):
            raise _ServiceFailure("authorization_expired_before_provider_call")
        if (
            operation_started_at is not None
            and (moment - operation_started_at).total_seconds()
            >= MAX_OPERATION_ELAPSED_SECONDS
        ):
            raise _ServiceFailure("operation_elapsed_ceiling_exhausted")
        if calls["http_calls_total"] >= MAX_HTTP_CALLS:
            raise _ServiceFailure("authorization_http_call_ceiling_exhausted")
        current_phase = phase
        calls["http_calls_total"] += 1
        network_called = True
        if started_at is None:
            started_at = moment
        current_call_started_at = moment
        return moment

    def _after_call(start: datetime, result: _ServiceResponse) -> datetime:
        nonlocal total_response_bytes, last_completed_at
        nonlocal current_response_bytes, current_response_sha256, current_response_counted
        nonlocal current_identifiers, current_usage
        nonlocal current_call_completed_at
        moment = _now()
        total_response_bytes += result.response_bytes
        current_response_bytes = result.response_bytes
        current_response_sha256 = result.response_sha256
        current_response_counted = True
        current_identifiers = result.provider_identifiers
        current_usage = result.provider_usage
        current_call_completed_at = moment
        if (
            moment < start
            or contract.expires_at is None
            or moment >= contract.expires_at
            or total_response_bytes > MAX_TOTAL_RESPONSE_BYTES
        ):
            raise _ServiceFailure(
                "authorization_or_response_ceiling_exceeded_after_provider_call",
                response_bytes=result.response_bytes,
                response_sha256=result.response_sha256,
                provider_identifiers=result.provider_identifiers,
                provider_usage=result.provider_usage,
            )
        last_completed_at = moment
        return moment

    def _failure_receipt(reason: str) -> None:
        failed_at = _failure_timestamp(
            _now(),
            (
                consumed_at,
                started_at,
                last_completed_at,
                current_call_started_at,
                current_call_completed_at,
            ),
        )
        _verify_latch()
        receipt = {
            "schema_version": FAILURE_RECEIPT_SCHEMA,
            "outcome": "failed_closed",
            "reason_code": reason,
            "failed_phase": primary_failure.get("phase") if primary_failure else current_phase,
            "http_status": primary_failure.get("http_status") if primary_failure else current_http_status,
            "authorization_id": contract.authorization["authorization_id"],
            "authorization_path": contract.authorization_path.relative_to(contract.root).as_posix(),
            "authorization_sha256": contract.authorization_sha256,
            "authorization_consumed": True,
            "consumption_record_path": contract.consumption_relative,
            "consumption_record_sha256": consumption_sha,
            "diagnosis_path": contract.diagnosis_path.relative_to(contract.root).as_posix(),
            "diagnosis_sha256": contract.diagnosis_sha256,
            "readiness_path": contract.readiness_path.relative_to(contract.root).as_posix(),
            "readiness_sha256": contract.readiness_sha256,
            "prior_attempt_binding": contract.authorization["prior_attempt_binding"],
            "provider": PROVIDER,
            "service": SERVICE,
            "project_sha256": contract.authorization["target"]["project_sha256"],
            "project_number_sha256": contract.authorization["target"]["project_number_sha256"],
            "runtime_bindings": contract.authorization["runtime_bindings"],
            "source_proof": source_proof,
            "credential_mechanism": CREDENTIAL_MECHANISM,
            "credential_refresh_attempted": credential_refresh_attempted,
            "network_called": credential_refresh_attempted or network_called,
            "calls": calls,
            "provider_response_bytes_total": total_response_bytes,
            "failed_response_bytes": primary_failure.get("response_bytes", 0) if primary_failure else 0,
            "failed_response_sha256": primary_failure.get("response_sha256") if primary_failure else None,
            "provider_error": primary_failure.get("provider_error") if primary_failure else None,
            "provider_identifiers": primary_failure.get("provider_identifiers", {}) if primary_failure else {},
            "provider_usage": primary_failure.get("provider_usage", {}) if primary_failure else {},
            "primary_failure": primary_failure,
            "pre_enable_readback": pre_evidence,
            "enable_operation": enable_evidence,
            "operation_completion": operation_evidence,
            "post_enable_readback": final_evidence,
            "resolution_readback_failure": resolution_readback_failure,
            "mutation_attempted": calls["enable_attempts"] == 1,
            "service_state_resolution": service_state_resolution,
            "enablement_may_have_completed": enablement_may_have_completed,
            "operation_may_still_be_running": operation_may_still_be_running,
            "manual_readback_required": manual_readback_required,
            "consumed_at": _iso(consumed_at),
            "started_at": _iso(started_at or consumed_at),
            "failed_at": _iso(failed_at),
            "retries_made": 0,
            "redirects_followed": 0,
            "credentials_recorded": False,
            "raw_provider_responses_recorded": False,
            **_authority_false_fields(),
        }
        if pt._scan_for_secrets(receipt, "service_enablement_failure_receipt"):
            raise ValidationError("refusing credential-bearing failure receipt")
        receipt_bytes = pt._receipt_bytes(receipt)
        if (
            project.encode("utf-8") in receipt_bytes
            or project_number.encode("ascii") in receipt_bytes
            or (token and token.encode("ascii") in receipt_bytes)
        ):
            raise ValidationError("refusing raw private material in failure receipt")
        pt._exclusive_fixture_write(contract.root, contract.failure_relative, receipt_bytes)

    try:
        credential_refresh_attempted = True
        _verify_latch()
        token = pt._load_google_access_token(gcloud, float(timeout))
        after_refresh = _now()
        if contract.expires_at is None or after_refresh < consumed_at or after_refresh >= contract.expires_at:
            raise _ServiceFailure("authorization_expired_after_token_refresh")
        service_url, enable_url = _service_urls(project_number)

        call_start = _before_call("pre_enable_readback")
        calls["pre_enable_state_readbacks"] += 1
        response = _perform_request(
            method="GET", url=service_url, expected_url=service_url, body=None,
            token=token, project=project, timeout=float(timeout),
        )
        call_completed = _after_call(call_start, response)
        expected_resource_name = f"projects/{project_number}/services/{SERVICE}"
        pre_evidence = _with_request_times(
            _service_state(
                response,
                "DISABLED",
                expected_resource_name=expected_resource_name,
            ),
            call_start,
            call_completed,
        )

        call_start = _before_call("enable")
        calls["enable_attempts"] += 1
        response = _perform_request(
            method="POST", url=enable_url, expected_url=enable_url, body=ENABLE_BODY,
            token=token, project=project, timeout=float(timeout),
        )
        enable_completed_at = _after_call(call_start, response)
        operation_name, done, operation_succeeded, enable_evidence = _operation_state(
            response,
            expected_name=None,
            expected_resource_name=expected_resource_name,
        )
        operation_terminal = done
        operation_name_sha = sha256_bytes(operation_name.encode("utf-8"))
        enable_evidence = _with_request_times(
            {**enable_evidence, "operation_name_sha256": operation_name_sha},
            call_start,
            enable_completed_at,
        )
        operation_started = enable_completed_at

        last_operation_summary = enable_evidence
        while not done:
            if calls["operation_polls"] >= MAX_OPERATION_POLLS:
                raise _ServiceFailure("operation_poll_ceiling_exhausted")
            elapsed = (_now() - operation_started).total_seconds()
            if elapsed >= MAX_OPERATION_ELAPSED_SECONDS:
                raise _ServiceFailure("operation_elapsed_ceiling_exhausted")
            _sleep(POLL_INTERVAL_SECONDS)
            poll_url = f"{BASE_ENDPOINT}/{operation_name}"
            call_start = _before_call(
                "operation_poll",
                operation_started_at=operation_started,
            )
            calls["operation_polls"] += 1
            response = _perform_request(
                method="GET", url=poll_url, expected_url=poll_url, body=None,
                token=token, project=project, timeout=float(timeout),
            )
            poll_completed_at = _after_call(call_start, response)
            if (
                poll_completed_at - operation_started
            ).total_seconds() >= MAX_OPERATION_ELAPSED_SECONDS:
                raise _ServiceFailure("operation_elapsed_ceiling_exhausted")
            operation_name, done, operation_succeeded, last_operation_summary = _operation_state(
                response,
                expected_name=operation_name,
                expected_resource_name=expected_resource_name,
            )
            operation_terminal = done
            last_operation_summary = _with_request_times(
                {
                    **last_operation_summary,
                    "operation_name_sha256": operation_name_sha,
                },
                call_start,
                poll_completed_at,
            )
            operation_evidence = {
                **last_operation_summary,
                "operation_name_sha256": operation_name_sha,
                "poll_count": calls["operation_polls"],
            }
        operation_evidence = {
            **last_operation_summary,
            "operation_name_sha256": operation_name_sha,
            "poll_count": calls["operation_polls"],
        }

        call_start = _before_call("post_enable_readback")
        calls["post_enable_state_readbacks"] += 1
        response = _perform_request(
            method="GET", url=service_url, expected_url=service_url, body=None,
            token=token, project=project, timeout=float(timeout),
        )
        completed_at = _after_call(call_start, response)
        final_evidence = _with_request_times(
            _observed_service_state(
                response,
                expected_resource_name=expected_resource_name,
            ),
            call_start,
            completed_at,
        )
        if final_evidence["state"] != "ENABLED":
            raise _ServiceFailure(
                "service_readback_state_unexpected",
                response_bytes=response.response_bytes,
                response_sha256=response.response_sha256,
                provider_identifiers=response.provider_identifiers,
                provider_usage=response.provider_usage,
            )
        service_state_resolution = "enabled_confirmed"
        enablement_may_have_completed = True
        operation_may_still_be_running = False
        manual_readback_required = False
        if (
            calls["pre_enable_state_readbacks"] != 1
            or calls["enable_attempts"] != 1
            or calls["post_enable_state_readbacks"] != 1
            or calls["operation_polls"] > MAX_OPERATION_POLLS
            or calls["http_calls_total"]
            != 3 + calls["operation_polls"]
            or contract.expires_at is None
            or completed_at >= contract.expires_at
        ):
            raise _ServiceFailure("service_enablement_transaction_incomplete")
        _verify_latch()
        receipt = {
            "schema_version": RUN_RECEIPT_SCHEMA,
            "outcome": "success",
            "authorization_id": contract.authorization["authorization_id"],
            "authorization_path": contract.authorization_path.relative_to(contract.root).as_posix(),
            "authorization_sha256": contract.authorization_sha256,
            "authorization_consumed": True,
            "consumption_record_path": contract.consumption_relative,
            "consumption_record_sha256": consumption_sha,
            "diagnosis_path": contract.diagnosis_path.relative_to(contract.root).as_posix(),
            "diagnosis_sha256": contract.diagnosis_sha256,
            "readiness_path": contract.readiness_path.relative_to(contract.root).as_posix(),
            "readiness_sha256": contract.readiness_sha256,
            "prior_attempt_binding": contract.authorization["prior_attempt_binding"],
            "provider": PROVIDER,
            "service": SERVICE,
            "project_sha256": contract.authorization["target"]["project_sha256"],
            "project_number_sha256": contract.authorization["target"]["project_number_sha256"],
            "runtime_bindings": contract.authorization["runtime_bindings"],
            "source_proof": source_proof,
            "credential_mechanism": CREDENTIAL_MECHANISM,
            "credential_refresh_attempted": True,
            "network_called": True,
            "calls": calls,
            "provider_response_bytes_total": total_response_bytes,
            "pre_enable_readback": pre_evidence,
            "enable_operation": enable_evidence,
            "operation_completion": operation_evidence,
            "post_enable_readback": final_evidence,
            "mutation_attempted": True,
            "service_state_resolution": service_state_resolution,
            "enablement_may_have_completed": enablement_may_have_completed,
            "operation_may_still_be_running": operation_may_still_be_running,
            "manual_readback_required": manual_readback_required,
            "consumed_at": _iso(consumed_at),
            "started_at": _iso(started_at or consumed_at),
            "completed_at": _iso(completed_at),
            "retries_made": 0,
            "redirects_followed": 0,
            "credentials_recorded": False,
            "raw_provider_responses_recorded": False,
            **_authority_false_fields(),
        }
        if pt._scan_for_secrets(receipt, "service_enablement_run_receipt"):
            raise _ServiceFailure("receipt_secret_scan_failed")
        receipt_bytes = pt._receipt_bytes(receipt)
        if (
            project.encode("utf-8") in receipt_bytes
            or project_number.encode("ascii") in receipt_bytes
            or token.encode("ascii") in receipt_bytes
        ):
            raise _ServiceFailure("receipt_private_value_scan_failed")
        pt._exclusive_fixture_write(contract.root, contract.success_relative, receipt_bytes)
        pt._verify_private_fixture_artifact(
            contract.root,
            contract.success_relative,
            receipt_bytes,
            "service enablement success receipt",
        )
        result = {
            "schema_version": "oe-google-service-enablement-execution-result-v2",
            "valid": True,
            "outcome": "success",
            "authorization_id": contract.authorization["authorization_id"],
            "authorization_consumed": True,
            "service": SERVICE,
            "project_sha256": contract.authorization["target"]["project_sha256"],
            "project_number_sha256": contract.authorization["target"]["project_number_sha256"],
            "prior_attempt_binding": contract.authorization["prior_attempt_binding"],
            "calls": calls,
            "run_receipt": {
                "path": contract.success_relative,
                "sha256": sha256_bytes(receipt_bytes),
            },
            "credentials_accessed": True,
            "network_called": True,
            "service_enablement_completed": True,
            "service_state_resolution": service_state_resolution,
            "manual_readback_required": manual_readback_required,
            **_authority_false_fields(),
        }
        project = ""
        project_number = ""
        token = ""
        service_url = ""
        enable_url = ""
        operation_name = ""
        expected_resource_name = ""
        response = None
        return result
    except _ServiceFailure as exc:
        operation_terminal = operation_terminal or exc.operation_terminal
        operation_succeeded = operation_succeeded or exc.operation_succeeded
        if current_call_started_at is not None and current_call_completed_at is None:
            observed_completion = _now()
            if observed_completion >= current_call_started_at:
                current_call_completed_at = observed_completion
        if (
            current_call_started_at is not None
            and current_call_completed_at is not None
            and current_call_completed_at < current_call_started_at
        ):
            current_call_completed_at = None
        if current_call_started_at is not None:
            last_completed_at = current_call_completed_at or current_call_started_at
        current_http_status = exc.http_status
        current_response_bytes = exc.response_bytes
        current_response_sha256 = exc.response_sha256
        current_provider_error = exc.provider_error
        current_identifiers = exc.provider_identifiers
        current_usage = exc.provider_usage
        if exc.response_bytes and not current_response_counted:
            total_response_bytes += exc.response_bytes
        primary_failure = {
            "phase": current_phase,
            "http_status": current_http_status,
            "response_bytes": current_response_bytes,
            "response_sha256": current_response_sha256,
            "provider_error": current_provider_error,
            "provider_identifiers": current_identifiers,
            "provider_usage": current_usage,
            "request_started_at": (
                _iso(current_call_started_at) if current_call_started_at is not None else None
            ),
            "request_completed_at": (
                _iso(current_call_completed_at) if current_call_completed_at is not None else None
            ),
        }
        reason = exc.code
    except ValidationError:
        current_response_bytes = 0
        current_response_sha256 = None
        current_provider_error = None
        current_identifiers = {}
        current_usage = {}
        primary_failure = {
            "phase": current_phase,
            "http_status": None,
            "response_bytes": 0,
            "response_sha256": None,
            "provider_error": None,
            "provider_identifiers": {},
            "provider_usage": {},
            "request_started_at": (
                _iso(current_call_started_at) if current_call_started_at is not None else None
            ),
            "request_completed_at": None,
        }
        reason = "local_validation_or_filesystem_failure"
    except Exception:
        current_response_bytes = 0
        current_response_sha256 = None
        current_provider_error = None
        current_identifiers = {}
        current_usage = {}
        primary_failure = {
            "phase": current_phase,
            "http_status": None,
            "response_bytes": 0,
            "response_sha256": None,
            "provider_error": None,
            "provider_identifiers": {},
            "provider_usage": {},
            "request_started_at": (
                _iso(current_call_started_at) if current_call_started_at is not None else None
            ),
            "request_completed_at": None,
        }
        reason = "unexpected_sanitized_failure"

    mutation_attempted = calls["enable_attempts"] == 1
    service_state_resolution = "not_attempted"
    enablement_may_have_completed = False
    operation_may_still_be_running = False
    manual_readback_required = False
    if mutation_attempted:
        service_state_resolution = "indeterminate_after_attempt"
        enablement_may_have_completed = True
        operation_may_still_be_running = not operation_terminal
        manual_readback_required = True
        if final_evidence is not None and final_evidence.get("state") == "ENABLED":
            service_state_resolution = "enabled_confirmed"
            manual_readback_required = False
        elif (
            final_evidence is not None
            and final_evidence.get("state") == "DISABLED"
            and operation_terminal
            and not operation_succeeded
        ):
            service_state_resolution = "disabled_confirmed"
            enablement_may_have_completed = False
            operation_may_still_be_running = False
            manual_readback_required = False
        if (
            calls["post_enable_state_readbacks"] == 0
            and bool(token)
            and bool(service_url)
            and bool(expected_resource_name)
        ):
            try:
                resolution_started = _before_call("post_enable_resolution_readback")
                calls["post_enable_state_readbacks"] += 1
                response = _perform_request(
                    method="GET",
                    url=service_url,
                    expected_url=service_url,
                    body=None,
                    token=token,
                    project=project,
                    timeout=float(timeout),
                )
                resolution_completed = _after_call(resolution_started, response)
                final_evidence = _with_request_times(
                    _observed_service_state(
                        response,
                        expected_resource_name=expected_resource_name,
                    ),
                    resolution_started,
                    resolution_completed,
                )
                if final_evidence["state"] == "ENABLED":
                    service_state_resolution = "enabled_confirmed"
                    enablement_may_have_completed = True
                    manual_readback_required = False
                elif operation_terminal and not operation_succeeded:
                    service_state_resolution = "disabled_confirmed"
                    enablement_may_have_completed = False
                    operation_may_still_be_running = False
                    manual_readback_required = False
            except _ServiceFailure as resolution_exc:
                if current_call_started_at is not None and current_call_completed_at is None:
                    observed_completion = _now()
                    if observed_completion >= current_call_started_at:
                        current_call_completed_at = observed_completion
                if (
                    current_call_started_at is not None
                    and current_call_completed_at is not None
                    and current_call_completed_at < current_call_started_at
                ):
                    current_call_completed_at = None
                if resolution_exc.response_bytes and not current_response_counted:
                    total_response_bytes += resolution_exc.response_bytes
                resolution_readback_failure = {
                    "code": resolution_exc.code,
                    "http_status": resolution_exc.http_status,
                    "response_bytes": resolution_exc.response_bytes,
                    "response_sha256": resolution_exc.response_sha256,
                    "provider_error": resolution_exc.provider_error,
                    "provider_identifiers": resolution_exc.provider_identifiers,
                    "provider_usage": resolution_exc.provider_usage,
                    "request_started_at": (
                        _iso(current_call_started_at)
                        if current_call_started_at is not None
                        else None
                    ),
                    "request_completed_at": (
                        _iso(current_call_completed_at)
                        if current_call_completed_at is not None
                        else None
                    ),
                }
            except ValidationError:
                resolution_readback_failure = {
                    "code": "resolution_readback_local_validation_failed",
                    "http_status": None,
                    "response_bytes": 0,
                    "response_sha256": None,
                    "provider_error": None,
                    "provider_identifiers": {},
                    "provider_usage": {},
                    "request_started_at": (
                        _iso(current_call_started_at)
                        if current_call_started_at is not None
                        else None
                    ),
                    "request_completed_at": None,
                }
            except Exception:
                resolution_readback_failure = {
                    "code": "resolution_readback_unexpected_failure",
                    "http_status": None,
                    "response_bytes": 0,
                    "response_sha256": None,
                    "provider_error": None,
                    "provider_identifiers": {},
                    "provider_usage": {},
                    "request_started_at": (
                        _iso(current_call_started_at)
                        if current_call_started_at is not None
                        else None
                    ),
                    "request_completed_at": None,
                }

    try:
        _failure_receipt(reason)
        final_reason = reason
    except Exception:
        final_reason = "failure_receipt_write_failed"
    project = ""
    project_number = ""
    token = ""
    gcloud = ""
    service_url = ""
    enable_url = ""
    operation_name = ""
    expected_resource_name = ""
    response = None
    contract = None
    consumption = {}
    consumption_bytes = b""
    pre_evidence = None
    enable_evidence = None
    operation_evidence = None
    final_evidence = None
    resolution_readback_failure = None
    current_provider_error = None
    current_identifiers = {}
    current_usage = {}
    _failure_receipt = None
    raise ValidationError(
        f"service enablement stopped without retry: {final_reason}"
    ) from None


def _preflight_paths_after_consumption(contract: _Contract) -> None:
    """Require the mutually exclusive success/failure destinations to remain new."""

    for label, relative in (
        ("success receipt", contract.success_relative),
        ("failure receipt", contract.failure_relative),
    ):
        pt._safe_execution_relative(contract.root, relative, label, ".json")
