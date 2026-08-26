"""Fail-closed ElevenLabs account verification and one-call Voice Changer.

Both transports are credential-free until a separately reviewed ACTIVE
authorization is consumed.  Account verification permits exactly one GET to
``/v1/user`` and stores only domain-separated hashes.  Voice transfer permits
exactly one PCM Voice Changer POST for the frozen candidate-B -> Original-C
microtest.  Neither path retries, redirects, falls back, changes account
settings, authorizes full capture, or grants any publication authority.
"""

from __future__ import annotations

import json
import hashlib
import os
import re
import resource
import selectors
import shutil
import signal
import ssl
import stat
import struct
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from contextlib import nullcontext
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, BinaryIO

from . import performance_transfer as pt
from .core import ValidationError, sha256_bytes, sha256_file


ACCOUNT_AUTH_SCHEMA = "oe-elevenlabs-account-verification-authorization-v1"
ACCOUNT_SCOPE = "elevenlabs_account_verification"
ACCOUNT_ENDPOINT = "https://api.elevenlabs.io/v1/user"
ACCOUNT_RUN_SCHEMA = "oe-elevenlabs-account-verification-run-v1"
ACCOUNT_FAILURE_SCHEMA = "oe-elevenlabs-account-verification-failure-v1"
ACCOUNT_CONSUMPTION_SCHEMA = "oe-elevenlabs-account-verification-consumption-v1"

# Additive recovery transaction.  These names and its fixed latch are
# intentionally disjoint from the consumed legacy account-verification path.
RECOVERY_AUTH_SCHEMA = "oe-elevenlabs-account-recovery-authorization-v1"
RECOVERY_SCOPE = "elevenlabs_account_recovery_verification"
RECOVERY_RUN_SCHEMA = "oe-elevenlabs-account-recovery-run-v1"
RECOVERY_FAILURE_SCHEMA = "oe-elevenlabs-account-recovery-failure-v1"
RECOVERY_CONSUMPTION_SCHEMA = "oe-elevenlabs-account-recovery-consumption-v1"
RECOVERY_CREDENTIAL_READ_CONSUMPTION_SCHEMA = (
    "oe-elevenlabs-account-recovery-credential-read-consumption-v1"
)
RECOVERY_DRY_RUN_SCHEMA = "oe-elevenlabs-account-recovery-dry-run-v1"
RECOVERY_RESULT_SCHEMA = "oe-elevenlabs-account-recovery-execution-result-v1"
RECOVERY_DOTENV_PATH = Path("/Users/brownmanbrain/GitHub/operator-economy/.env")
RECOVERY_DOTENV_MAX_BYTES = 65_536
RECOVERY_OWNER_APPROVAL_PATH = (
    "evidence/V1-ELEVENLABS-ACCOUNT-RECOVERY-OWNER-APPROVAL.20260826T115516Z.json"
)
RECOVERY_OWNER_APPROVAL_SHA256 = (
    "549340266691d0e309e534049452b3c76e6a8674989208874d41def842779113"
)
RECOVERY_OWNER_APPROVAL_COMMIT = "32446e10cee1acd5dddd78feedffe57bbf030439"
RECOVERY_PRIOR_OUTCOME_COMMIT = "dc8fb34730c8751d3eafd0c2e86ba83db883e409"
RECOVERY_PRIOR_ACTIVE_PATH = (
    "authorizations/12-elevenlabs-account-verification.ACTIVE.20260826T105051Z.json"
)
RECOVERY_PRIOR_ACTIVE_SHA256 = (
    "328c14036caabbceb07b9516679c1518ca0689e9c6c68e974cb29c32755626a8"
)
RECOVERY_PRIOR_LATCH_PATH = (
    "authorizations/consumed/elevenlabs-account-verification-one-shot.consumed.json"
)
RECOVERY_PRIOR_LATCH_SHA256 = (
    "359bad8d5821fe45ff20febc2b06cc81df16b043404cddc7f1d46ed5bc9f2b91"
)
RECOVERY_PRIOR_FAILURE_PATH = (
    "receipts/elevenlabs-account/"
    "AUTH-ACCOUNT-ai-visibility-v1.1-read-only-user-verification-20260826T105051Z.failure.json"
)
RECOVERY_PRIOR_FAILURE_SHA256 = (
    "f3b2c461a803d1f32d58ec5b112adb1081dd1175dc6f071122b303abe7ea8deb"
)
RECOVERY_PRIOR_DISPOSITION_PATH = (
    "evidence/V1-ELEVENLABS-ACCOUNT-ZERO-NETWORK-FAILURE-DISPOSITION.20260826T110834Z.json"
)
RECOVERY_PRIOR_DISPOSITION_SHA256 = (
    "fe840ec4f510c5b261b6579c22f1a88749de7fa72de21b02d9e3a5d16d2f3d9a"
)
FIXTURE_ID = "step2-v0.5-ai-visibility-v1.1-synthetic-guide-to-saved-c-transfer-microtest"

TRANSFER_EXEC_AUTH_SCHEMA = "oe-voice-transfer-execution-authorization-v2"
TRANSFER_EXEC_SCOPE = "elevenlabs_voice_transfer_execution"
TRANSFER_RUN_SCHEMA = "oe-elevenlabs-voice-transfer-run-v1"
TRANSFER_FAILURE_SCHEMA = "oe-elevenlabs-voice-transfer-failure-v1"
TRANSFER_CONSUMPTION_SCHEMA = "oe-elevenlabs-voice-transfer-consumption-v1"

# Additive transfer authority that accepts only the terminal recovery HTTP-200
# chain as calibrated credential-authentication evidence.  It never upgrades
# the unread account body to a user/account/equality claim and cannot reuse the
# consumed GET authority.
RECOVERY_TRANSFER_AUTH_SCHEMA = (
    "oe-elevenlabs-recovery-evidence-voice-transfer-authorization-v1"
)
RECOVERY_TRANSFER_SCOPE = "elevenlabs_recovery_evidence_voice_transfer_execution"
RECOVERY_TRANSFER_DRY_RUN_SCHEMA = (
    "oe-elevenlabs-recovery-evidence-voice-transfer-dry-run-v1"
)
RECOVERY_TRANSFER_RUN_SCHEMA = "oe-elevenlabs-recovery-evidence-voice-transfer-run-v1"
RECOVERY_TRANSFER_FAILURE_SCHEMA = (
    "oe-elevenlabs-recovery-evidence-voice-transfer-failure-v1"
)
RECOVERY_TRANSFER_CONSUMPTION_SCHEMA = (
    "oe-elevenlabs-recovery-evidence-voice-transfer-consumption-v1"
)
RECOVERY_TRANSFER_RESULT_SCHEMA = (
    "oe-elevenlabs-recovery-evidence-voice-transfer-execution-result-v1"
)
RECOVERY_TRANSFER_CONVERSION_SCHEMA = (
    "oe-elevenlabs-recovery-evidence-voice-transfer-conversion-v1"
)
RECOVERY_TRANSFER_AUTHENTICATION_CONCLUSION = (
    "HTTP 200 supports, but does not independently prove, that the credential-bearing "
    "request was accepted at this endpoint."
)
RECOVERY_TRANSFER_AUTHENTICATION_INFERENCE_STATE = (
    "supported_by_http_200_not_independently_verified"
)
RECOVERY_TRANSFER_SAFE_CONCLUSION = (
    "HTTP 200 supports only the calibrated credential-authentication inference above. "
    "With zero response-body bytes read, this attempt establishes no specific user ID, "
    "account identity, account data, response schema or contents, subscription state, "
    "exact UI/API account equality, or target-voice accessibility."
)
RECOVERY_TRANSFER_OUTCOME_COMMIT = "38802d8a5bf221bbf259fcef43d93b247197320e"
RECOVERY_TRANSFER_TRANSACTION_BASIS_ID = (
    "V1-CANDIDATE-B-TO-ORIGINAL-C-RECOVERY-EVIDENCE-TRANSFER"
)
RECOVERY_TRANSFER_OWNER = "Manav Thaker"
RECOVERY_TRANSFER_DRAFT_ID = (
    "DRAFT-RECOVERY-EVIDENCE-VOICE-TRANSFER-ai-visibility-v1.1-p01"
)
RECOVERY_TRANSFER_ACTIVE_ID = (
    "AUTH-RECOVERY-EVIDENCE-VOICE-TRANSFER-ai-visibility-v1.1-p01"
)
RECOVERY_TRANSFER_DRAFT_PATH = (
    "authorizations/15-elevenlabs-recovery-evidence-voice-transfer.DRAFT.json"
)
RECOVERY_TRANSFER_ACTIVE_PATH = (
    "authorizations/16-elevenlabs-recovery-evidence-voice-transfer.ACTIVE.authorization.json"
)
RECOVERY_TRANSFER_DRAFT_BLOCKERS = [
    "evidence_baseline_r1_commit_pending",
    "separate_short_lived_active_authorization_required",
    "credential_access_and_provider_action_not_authorized",
]
RECOVERY_TRANSFER_ACCOUNT_AUTH_PATH = (
    "authorizations/14-elevenlabs-account-recovery.ACTIVE.20260826T133955Z.json"
)
RECOVERY_TRANSFER_ACCOUNT_AUTH_SHA256 = (
    "e16537a274c9b4f54a9c50c248b1757f7510f05b8092eb6d10e78a07d7cf1eae"
)
RECOVERY_TRANSFER_CREDENTIAL_LATCH_PATH = (
    "authorizations/consumed/elevenlabs-account-recovery-credential-read-one-shot."
    "consumed.json"
)
RECOVERY_TRANSFER_CREDENTIAL_LATCH_SHA256 = (
    "4992d2a318584efc7d6bf483931d4a777f659e9c5d6e1f893ef61aa620c53157"
)
RECOVERY_TRANSFER_PROVIDER_LATCH_PATH = (
    "authorizations/consumed/elevenlabs-account-recovery-provider-one-shot."
    "consumed.json"
)
RECOVERY_TRANSFER_PROVIDER_LATCH_SHA256 = (
    "dedb2de93b876fdc3a0ef6f36e68cefe7b8f99cad01b811eebe80caff6a378ca"
)
RECOVERY_TRANSFER_FAILURE_PATH = (
    "receipts/elevenlabs-account/"
    "AUTH-ACCOUNT-RECOVERY-ai-visibility-v1.1-read-only-user-verification-"
    "20260826T133955Z.recovery-failure.json"
)
RECOVERY_TRANSFER_FAILURE_SHA256 = (
    "5340db5eabe90110479001ea4b0d3f697971978fc1d83f45f3e77cf0c1a7c654"
)
RECOVERY_TRANSFER_DISPOSITION_PATH = (
    "evidence/V1-ELEVENLABS-ACCOUNT-RECOVERY-HTTP-200-ZERO-BODY-FAILURE-"
    "DISPOSITION.20260826T135047Z.json"
)
RECOVERY_TRANSFER_DISPOSITION_SHA256 = (
    "eb2db5e420fcc8ea7c19d878e781759cc6a0c874a260d0bdb2ed20e80799c877"
)
RECOVERY_TRANSFER_ACCOUNT_ASSURANCE_PATH = (
    "evidence/V1-ELEVENLABS-RECOVERY-CALIBRATED-ACCOUNT-ASSURANCE.json"
)
RECOVERY_TRANSFER_DATA_USE_ASSURANCE_PATH = (
    "evidence/V1-ELEVENLABS-RECOVERY-TRANSFER-DATA-USE-ASSURANCE.json"
)
RECOVERY_TRANSFER_TARGET_RIGHTS_PATH = (
    "evidence/V1-ELEVENLABS-RECOVERY-TRANSFER-TARGET-RIGHTS.json"
)
RECOVERY_TRANSFER_HISTORICAL_BROWSER_PATH = (
    "evidence/browser-readiness/"
    "V1-ELEVENLABS-ACCOUNT-RECOVERY-BROWSER-READINESS.20260826T132827Z.json"
)
RECOVERY_TRANSFER_HISTORICAL_BROWSER_SHA256 = (
    "35895c45441d796cf63539af6ee3761c1e087e322c4e5e60425a12c0d4d17995"
)
RECOVERY_TRANSFER_HISTORICAL_CAPTURE_PATH = (
    "evidence/browser-readiness/"
    "V1-ELEVENLABS-ACCOUNT-RECOVERY-BROWSER-READINESS.20260826T132827Z.png"
)
RECOVERY_TRANSFER_HISTORICAL_CAPTURE_SHA256 = (
    "f1da6038e674fe4313bf829bb1f9a880b334c729453b3472c22742376156a2e4"
)
RECOVERY_TRANSFER_OWNER_APPROVAL_PATH = (
    "evidence/V1-OWNER-AUDITION-AND-BOUNDED-TRANSFER-APPROVAL.20260826T061117Z.json"
)
RECOVERY_TRANSFER_OWNER_APPROVAL_SHA256 = (
    "c90783e767d6d9f8ebbd408fc4bc88ef4d69138c5547b95e99fbcacd49e216f0"
)
RECOVERY_TRANSFER_GUIDE_QA_PATH = (
    "reviews/GUIDE-QA.candidate-B.20260826T061117Z.json"
)
RECOVERY_TRANSFER_GUIDE_QA_SHA256 = (
    "aa56ed77ec7bac54c8bfe4c3f71954824ede6ffd74f9489246d031945d3e0909"
)
RECOVERY_TRANSFER_GUIDE_SELECTION_PATH = (
    "reviews/GUIDE-OWNER-SELECTION.candidate-B.20260826T061117Z.json"
)
RECOVERY_TRANSFER_GUIDE_SELECTION_SHA256 = (
    "eb1a33aa270b97f5f31c3fdaf37bfe49b242786fe29be9082a67124076443236"
)
RECOVERY_TRANSFER_ORIGINAL_C_SELECTION_PATH = (
    "02-narration-production/fixtures/step2-v0.4-ai-visibility-v1.1-saved-c-p01-calibration/"
    "receipts/provenance/AUTH-R2-owner-selection-C.json"
)
RECOVERY_TRANSFER_ORIGINAL_C_SELECTION_SHA256 = (
    "850b47a5419424fee37e9bff73a96b9e1da1c31feee13d20013869e4f3092702"
)
RECOVERY_TRANSFER_ORIGINAL_C_SAVE_PATH = (
    "02-narration-production/fixtures/step2-v0.4-ai-visibility-v1.1-saved-c-p01-calibration/"
    "receipts/provenance/AUTH-R2-remix-save.json"
)
RECOVERY_TRANSFER_ORIGINAL_C_SAVE_SHA256 = (
    "859b80a525d1d59ad531420f4c4ee496a0e41f6d91f0ee34ba895eb171dc7885"
)

API_KEY_ENV = "ELEVENLABS_API_KEY"
API_KEY_DOMAIN = b"oe-elevenlabs-api-key-v1\x00"
API_KEY_DOMAIN_TEXT = "oe-elevenlabs-api-key-v1\x00"
USER_ID_DOMAIN = b"oe-elevenlabs-user-id-v1\x00"
USER_ID_DOMAIN_TEXT = "oe-elevenlabs-user-id-v1\x00"
API_KEY_PREVIEW_DOMAIN = b"oe-elevenlabs-api-key-preview-last4-v1\x00"
API_KEY_PREVIEW_DOMAIN_TEXT = "oe-elevenlabs-api-key-preview-last4-v1\x00"
API_KEY_PREVIEW_KIND = "provider_key_last4"
API_KEY_PREVIEW_CANONICALIZATION = "exact_final_four_ascii"
ACCOUNT_IDENTITY_KIND = "elevenlabs_user_id"
ACCOUNT_IDENTITY_CANONICALIZATION = "exact_printable_ascii_no_trim"
DATA_USE_BASIS_URL = (
    "https://elevenlabs.io/docs/help-center/legal/"
    "is-my-data-used-to-improve-eleven-labs-ai-models"
)
DATA_USE_BASIS_STATEMENT = (
    "Disabling ‘Improve the models for everyone’ and saving the update means new "
    "submissions will not be used to train ElevenLabs models."
)
DATA_USE_BASIS_STATEMENT_SHA256 = "b02add24fbe7fc13630885b3ad3b97a3dca1ddcf445527c97799fa06d6ff066d"
MEDIA_CONTRACT_BASIS_SCHEMA = "oe-elevenlabs-voice-changer-pcm-media-contract-basis-v1"
MEDIA_CONTRACT_BASIS_PATH = (
    "evidence/V1-ELEVENLABS-PCM48000-MEDIA-CONTRACT-BASIS.20260826T073836Z.json"
)
MEDIA_CONTRACT_BASIS_SHA256 = "175feb4d640d48a0fa4fc4f8e8e278478e8c5bd32bb89c9087974ebb149d78a9"
MEDIA_OPENAPI_URL = "https://api.elevenlabs.io/openapi.json"
MEDIA_PCM_FORMAT_URL = "https://elevenlabs.io/docs/overview/capabilities/text-to-speech"
MEDIA_STS_URL = "https://elevenlabs.io/docs/api-reference/speech-to-speech/convert"
MEDIA_CONTRACT_INTERPRETATION = (
    "The sources do not prove the response payload codec or channel count. For the exact "
    "pcm_48000 request, runtime may interpret a declared audio/pcm or audio/mpeg response as "
    "headerless PCM S16LE with one channel only when no recognized compressed or container "
    "format is detected, byte geometry passes, and the mono-interpreted duration is within a "
    "0.8-to-1.2 ratio of the exact source duration. Codec, mono channel count, frame count, and "
    "duration remain contract interpretations, not intrinsic media verification."
)
MEDIA_CONTRACT_INTERPRETATION_SHA256 = sha256_bytes(
    MEDIA_CONTRACT_INTERPRETATION.encode("utf-8")
)
ACCOUNT_OWNER_APPROVAL_PROMPT = (
    "To avoid ambiguity, please confirm both together: **(1)** turn OFF ‘Improve the "
    "models for everyone’ and save it; **(2)** make exactly one read-only `GET /v1/user` "
    "using the existing key. No upload or paid call happens in either step."
)
# Literal owner reply to the exact prompt above.  The reply records contextual
# assent only; a separate exact ACTIVE authorization remains required.
ACCOUNT_OWNER_APPROVAL_REPLY = "Approved for both"

ACCOUNT_MAX_GET_CALLS = 1
ACCOUNT_MAX_POST_CALLS = 0
ACCOUNT_MAX_RESPONSE_BYTES = 1_000_000
ACCOUNT_MAX_ERROR_RESPONSE_BYTES = 65_536
ACCOUNT_MAX_ELAPSED_SECONDS = 30

SELECTED_GUIDE_PATH = "outputs/raw/google/P01-W0030-W0110/candidate-B.wav"
SELECTED_GUIDE_SHA256 = "04448e9fdd50c8de67912b454e8d396f5822eaa881daf18128b825260623c915"
SELECTED_GUIDE_BYTES = 1_646_010
SELECTED_GUIDE_DURATION_SECONDS = 34.290958333333336
SELECTED_GUIDE_REQUEST_ID = "gemini-guide-02"
SELECTED_GUIDE_RUN_PATH = (
    "receipts/google/AUTH-G1R2-ai-visibility-v1.1-p01-synthetic-guide-"
    "20260826T042506Z.run.json"
)
SELECTED_GUIDE_RUN_SHA256 = "2898d5f26f6523de6691782e668ab45951f4710751b78414ca8caedeb9fe0a1f"

V1_LINEAGE_PATH = "authorizations/02-elevenlabs-saved-c-transfer.DRAFT.json"
V1_LINEAGE_SHA256 = "1b6c431c9df420d44a2a8057c0a65605cbb0c584e392179d32c74d2f40431036"
V1_LINEAGE_ID = "DRAFT-V1-ai-visibility-v1.1-p01-saved-c-transfer"

TRANSFER_BODY_SHA256 = "6b57da1e6d1dc62b8ec31d34b6629da087be15f51b59998a83109f25403931dc"
TRANSFER_BODY_BYTES = 1_646_839
TRANSFER_CONTENT_TYPE = (
    "multipart/form-data; boundary=oe-v05-04448e9fdd50c8de67912b454e8d396f"
)
TRANSFER_OPT_OUT_REQUEST_SHA256 = "ccce1a1a46476c6a5b340416a7c97ccff34aac8a54edb454e9b411dcdfaa8c76"
TRANSFER_ZRM_REQUEST_SHA256 = "ff695baff6ea7ba9bd901c7091fd85701da035e614d19ebee6bde9a7a0b95773"
TRANSFER_OPT_OUT_NORMALIZED_REQUEST_SHA256 = (
    "878e7810bdddec3073cc6eee4d08072da6e312a4969bfc94a0daade19f321995"
)

TRANSFER_MAX_GENERATION_POST_CALLS = 1
TRANSFER_MAX_ACCOUNT_GET_CALLS = 0
TRANSFER_MAX_OUTPUTS = 1
TRANSFER_MAX_RESPONSE_BYTES = 4_800_000
TRANSFER_MAX_ERROR_RESPONSE_BYTES = 65_536
TRANSFER_MIN_OUTPUT_DURATION_SECONDS = 20.0
TRANSFER_MAX_OUTPUT_DURATION_SECONDS = 50.0
TRANSFER_MIN_OUTPUT_TO_SOURCE_DURATION_RATIO = 0.8
TRANSFER_MAX_OUTPUT_TO_SOURCE_DURATION_RATIO = 1.2
TRANSFER_MAX_ELAPSED_SECONDS = 300
TRANSFER_MAX_SPEND_USD = 0.12
TRANSFER_RAW_PATH = "outputs/raw/elevenlabs/P01-W0030-W0110/saved-c-transfer.pcm"
TRANSFER_WORKING_PATH = "outputs/working/elevenlabs/P01-W0030-W0110/saved-c-transfer.wav"
ACCOUNT_SCOPE_LATCH_PATH = (
    "authorizations/consumed/elevenlabs-account-verification-one-shot.consumed.json"
)
RECOVERY_SCOPE_LATCH_PATH = (
    "authorizations/consumed/elevenlabs-account-recovery-provider-one-shot.consumed.json"
)
RECOVERY_CREDENTIAL_READ_LATCH_PATH = (
    "authorizations/consumed/elevenlabs-account-recovery-credential-read-one-shot.consumed.json"
)
TRANSFER_SCOPE_LATCH_PATH = (
    "authorizations/consumed/elevenlabs-candidate-b-to-original-c-one-shot."
    "voice-transfer-execution.consumed.json"
)

# Only public/non-sensitive contract inputs are required in the local Git DAG.
# Provider media, browser captures, owner/account evidence, and private receipts
# remain descriptor/hash-bound local files and are never made Git prerequisites.
TRANSFER_COMMITTED_RECORD_NAMES = frozenset(
    {
        "plan",
        "canonical_w",
        "lineage",
        "official_data_use_basis",
        "official_media_contract",
        "account_authorization",
    }
)
TRANSFER_LOCAL_PRIVATE_RECORD_NAMES = frozenset(
    {
        "qa",
        "selection",
        "audition",
        "data_use",
        "data_evidence",
        "data_evidence_capture",
        "account_receipt",
        "account_owner_approval",
        "account_consumption",
        "rights",
        "original_c_selection",
        "original_c_save",
        "selected_guide",
        "guide_run",
    }
)

DATA_USE_MAX_AGE_SECONDS = 3_600
ACCOUNT_VERIFICATION_MAX_AGE_SECONDS = 3_600

_SHA_RE = re.compile(r"^[0-9a-f]{64}$")
_GIT_SHA_RE = re.compile(r"^[0-9a-f]{40}$")
_RECOVERY_TRANSFER_RFC3339_UTC_RE = re.compile(
    r"^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}"
    r"(?:\.[0-9]{1,6})?(?:Z|\+00:00)$"
)
_RECOVERY_TRANSFER_BROWSER_PATH_RE = re.compile(
    r"^evidence/browser-readiness/"
    r"V1-ELEVENLABS-RECOVERY-TRANSFER-BROWSER-READINESS\."
    r"[0-9]{8}T[0-9]{6}Z\.json$"
)
_SAFE_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,159}$")
_SAFE_HEADER_VALUE_RE = re.compile(r"^[A-Za-z0-9._:/;=+\-]{1,256}$")
_AUDIO_MIMES = frozenset({"audio/pcm", "audio/mpeg"})
FFPROBE_MAX_ELAPSED_SECONDS = 10.0
_MEDIA_TOOL_SEARCH_PATH = "/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin"
GIT_EXECUTABLE_PATH = "/usr/bin/git"
FFPROBE_MEDIA_PROBE_ARGUMENTS = (
    "-v",
    "error",
    "-probesize",
    "1048576",
    "-analyzeduration",
    "1000000",
    "-protocol_whitelist",
    "pipe",
    "-show_entries",
    "format=format_name:stream=codec_name",
    "-of",
    "json",
    "pipe:0",
)
FFPROBE_NO_FORMAT_STDERR = b"pipe:0: Invalid data found when processing input\n"


def _compact(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")


def _receipt_bytes(value: dict[str, Any]) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _iso(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat()


def _key_fingerprint(value: str) -> str:
    return sha256_bytes(API_KEY_DOMAIN + value.encode("utf-8"))


def _user_scope_hash(value: str) -> str:
    return sha256_bytes(USER_ID_DOMAIN + value.encode("utf-8"))


def _preview_hash(value: str) -> str:
    return sha256_bytes(API_KEY_PREVIEW_DOMAIN + value.encode("ascii", errors="strict"))


def _exact(actual: Any, expected: Any) -> bool:
    return pt._json_exact(actual, expected)


def _strict(
    value: Any,
    keys: set[str],
    label: str,
    *,
    required: set[str] | None = None,
) -> dict[str, Any]:
    return pt._strict_object(value, keys, required if required is not None else keys, label)


def _parse_time(value: Any, label: str, errors: list[str]) -> datetime | None:
    return pt._parse_time(value, label, errors)


def _parse_recovery_transfer_time(
    value: Any,
    label: str,
    errors: list[str],
) -> datetime | None:
    """Parse only the additive schema's exact UTC RFC3339 lexical form."""

    if (
        not isinstance(value, str)
        or not _RECOVERY_TRANSFER_RFC3339_UTC_RE.fullmatch(value)
    ):
        errors.append(f"{label} must use exact UTC RFC3339 syntax")
        return None
    return _parse_time(value, label, errors)


def _raise_errors(errors: list[str]) -> None:
    if errors:
        raise ValidationError(errors)


def _runtime_files() -> dict[str, tuple[str, Path]]:
    narration_root = Path(__file__).resolve().parents[2]
    package = narration_root / "runtime" / "oe_narration"
    tests = narration_root / "runtime" / "tests"
    schemas = narration_root / "schemas"
    prefix = "operator-blueprint-v2/02-narration-production/"
    return {
        "voice_transfer_runtime": (
            prefix + "runtime/oe_narration/voice_transfer.py",
            package / "voice_transfer.py",
        ),
        "performance_transfer_runtime": (
            prefix + "runtime/oe_narration/performance_transfer.py",
            package / "performance_transfer.py",
        ),
        "cli_runtime": (prefix + "runtime/oe_narration/cli.py", package / "cli.py"),
        "core_runtime": (prefix + "runtime/oe_narration/core.py", package / "core.py"),
        "audio_runtime": (prefix + "runtime/oe_narration/audio.py", package / "audio.py"),
        "init_runtime": (prefix + "runtime/oe_narration/__init__.py", package / "__init__.py"),
        "account_schema": (
            prefix + "schemas/elevenlabs-account-verification-authorization.schema.json",
            schemas / "elevenlabs-account-verification-authorization.schema.json",
        ),
        "transfer_schema": (
            prefix + "schemas/voice-transfer-execution-authorization.schema.json",
            schemas / "voice-transfer-execution-authorization.schema.json",
        ),
        "voice_transfer_tests": (
            prefix + "runtime/tests/test_voice_transfer.py",
            tests / "test_voice_transfer.py",
        ),
        "audio_tests": (
            prefix + "runtime/tests/test_capture_audio.py",
            tests / "test_capture_audio.py",
        ),
    }


def _read_media_tool_identity(tool: str, path_value: str | None = None) -> tuple[str, str]:
    """Return a descriptor-bound absolute media-tool path and SHA-256."""

    candidate = path_value
    if candidate is None:
        candidate = shutil.which(tool, path=_MEDIA_TOOL_SEARCH_PATH)
    if not isinstance(candidate, str) or not candidate or "\x00" in candidate:
        raise ValidationError(f"the local {tool} media tool is unavailable")
    try:
        path = Path(candidate)
        if path_value is None:
            path = path.resolve(strict=True)
        elif not path.is_absolute() or path.resolve(strict=True) != path:
            raise ValidationError(f"bound {tool} path must be an exact resolved absolute path")
    except (OSError, RuntimeError):
        raise ValidationError(f"the local {tool} media tool path is unsafe") from None

    parent_fd = os.open("/", os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
    descriptor: int | None = None
    chunks: list[bytes] = []
    chunk = b""
    try:
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
            or not 0 < before.st_size <= 16_000_000
        ):
            raise ValidationError(f"bound {tool} binary is not a bounded executable regular file")
        received = 0
        while True:
            chunk = os.read(descriptor, min(1_048_576, 16_000_001 - received))
            if not chunk:
                break
            chunks.append(chunk)
            received += len(chunk)
            if received > 16_000_000:
                raise ValidationError(f"bound {tool} binary exceeds its safety cap")
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
            raise ValidationError(f"bound {tool} binary changed during identity read")
        digest = sha256_bytes(raw)
        raw = b""
        return str(path), digest
    except ValidationError:
        raise
    except OSError:
        raise ValidationError(f"bound {tool} binary is missing or unsafe") from None
    finally:
        chunks = []
        chunk = b""
        if descriptor is not None:
            os.close(descriptor)
        os.close(parent_fd)


def _read_media_tool_version(
    tool: str,
    path: str,
    expected_sha256: str | None = None,
) -> str:
    result: subprocess.CompletedProcess[bytes] | None = None
    stdout = b""
    stderr = b""
    executable_fd: int | None = None
    post_fd: int | None = None
    try:
        executable_fd, executable_sha = pt._open_bound_executable_descriptor(
            path,
            expected_sha256,
            f"{tool} executable",
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
        execution_context = (
            nullcontext(None)
            if tool == "git"
            else pt._private_executable_copy(
                path,
                executable_sha,
                f"{tool} executable",
            )
        )
        with execution_context as private_executable:
            run_options: dict[str, Any] = {}
            if private_executable is not None:
                run_options["executable"] = private_executable
            result = subprocess.run(
                [path, "--version" if tool == "git" else "-version"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=5.0,
                check=False,
                close_fds=True,
                env={"PATH": "/usr/bin:/bin", "LANG": "C", "LC_ALL": "C"},
                **run_options,
            )
        post_fd, _post_digest = pt._open_bound_executable_descriptor(
            path,
            expected_sha256,
            f"{tool} executable",
        )
        after = os.fstat(post_fd)
        if before_identity != (
            after.st_dev,
            after.st_ino,
            after.st_size,
            after.st_mtime_ns,
            after.st_mode,
            after.st_uid,
        ):
            raise ValidationError(f"bound {tool} changed during version read")
        stdout = result.stdout if isinstance(result.stdout, bytes) else b""
        stderr = result.stderr if isinstance(result.stderr, bytes) else b""
        if result.returncode != 0 or stderr or not 1 <= len(stdout) <= 65_536:
            raise ValidationError(f"bound {tool} version read failed closed")
        try:
            first_line = stdout.splitlines()[0].decode("ascii", errors="strict")
        except (IndexError, UnicodeError):
            raise ValidationError(f"bound {tool} version identity is malformed") from None
        pattern = (
            r"git version ([0-9][A-Za-z0-9.+-]{0,63})(?: .*)?"
            if tool == "git"
            else rf"{re.escape(tool)} version ([0-9][A-Za-z0-9.+-]{{0,63}}) Copyright .+"
        )
        match = re.fullmatch(pattern, first_line)
        if match is None:
            raise ValidationError(f"bound {tool} version identity is malformed")
        return match.group(1)
    except subprocess.TimeoutExpired as exc:
        exc.stdout = None
        exc.stderr = None
        raise ValidationError(f"bound {tool} version read timed out") from None
    except ValidationError:
        raise
    except Exception:
        raise ValidationError(f"bound {tool} version read failed closed") from None
    finally:
        result = None
        stdout = b""
        stderr = b""
        if executable_fd is not None:
            os.close(executable_fd)
        if post_fd is not None:
            os.close(post_fd)


def _read_ffprobe_identity(path_value: str | None = None) -> tuple[str, str]:
    return _read_media_tool_identity("ffprobe", path_value)


def _read_ffprobe_version(path: str, expected_sha256: str | None = None) -> str:
    return _read_media_tool_version("ffprobe", path, expected_sha256)


def _read_ffmpeg_identity(path_value: str | None = None) -> tuple[str, str]:
    return _read_media_tool_identity("ffmpeg", path_value)


def _read_ffmpeg_version(path: str, expected_sha256: str | None = None) -> str:
    return _read_media_tool_version("ffmpeg", path, expected_sha256)


def _read_git_identity(path_value: str | None = None) -> tuple[str, str]:
    path, digest = _read_media_tool_identity(
        "git",
        GIT_EXECUTABLE_PATH if path_value is None else path_value,
    )
    try:
        metadata = os.stat(path, follow_symlinks=False)
    except OSError:
        raise ValidationError("bound Git executable is unavailable") from None
    if path != GIT_EXECUTABLE_PATH or metadata.st_uid != 0 or stat.S_IMODE(metadata.st_mode) & 0o022:
        raise ValidationError("bound Git executable must be the root-owned system binary")
    return path, digest


def _read_git_version(path: str, expected_sha256: str | None = None) -> str:
    return _read_media_tool_version("git", path, expected_sha256)


def expected_runtime_bindings(
    *,
    draft: bool,
    include_media_probe: bool = False,
) -> dict[str, str]:
    if draft:
        return {"state": "pending"}
    result = {"state": "verified", "git_commit": "pending"}
    for name, (_relative, path) in _runtime_files().items():
        result[f"{name}_sha256"] = sha256_file(path)
    git_path, git_sha = _read_git_identity()
    result["git_binary_path"] = git_path
    result["git_binary_sha256"] = git_sha
    result["git_version"] = _read_git_version(git_path, git_sha)
    if include_media_probe:
        probe_path, probe_sha = _read_ffprobe_identity()
        result["ffprobe_binary_path"] = probe_path
        result["ffprobe_binary_sha256"] = probe_sha
        result["ffprobe_version"] = _read_ffprobe_version(probe_path, probe_sha)
        ffmpeg_path, ffmpeg_sha = _read_ffmpeg_identity()
        result["ffmpeg_binary_path"] = ffmpeg_path
        result["ffmpeg_binary_sha256"] = ffmpeg_sha
        result["ffmpeg_version"] = _read_ffmpeg_version(ffmpeg_path, ffmpeg_sha)
        result["media_tool_binding_scope"] = "primary_executable_bytes_and_version_only"
        result["dynamic_library_dependency_closure_verified"] = False
        result["media_executable_private_exact_byte_copy_required"] = True
    return result


def _validate_runtime_bindings(
    value: Any,
    *,
    active: bool,
    require_media_probe: bool,
    errors: list[str],
) -> dict[str, Any]:
    expected_keys = {"state"}
    if active:
        expected_keys |= {
            "git_commit",
            "git_binary_path",
            "git_binary_sha256",
            "git_version",
            *(f"{name}_sha256" for name in _runtime_files()),
        }
        if require_media_probe:
            expected_keys |= {
                "ffprobe_binary_path",
                "ffprobe_binary_sha256",
                "ffprobe_version",
                "ffmpeg_binary_path",
                "ffmpeg_binary_sha256",
                "ffmpeg_version",
                "media_tool_binding_scope",
                "dynamic_library_dependency_closure_verified",
                "media_executable_private_exact_byte_copy_required",
            }
    item = _strict(value, expected_keys, "runtime_bindings")
    if active:
        if item.get("state") != "verified" or not isinstance(item.get("git_commit"), str) or not _GIT_SHA_RE.fullmatch(item["git_commit"]):
            errors.append("active runtime bindings require a verified Git commit")
        for name, (_relative, path) in _runtime_files().items():
            expected = item.get(f"{name}_sha256")
            if not isinstance(expected, str) or not _SHA_RE.fullmatch(expected) or not path.is_file() or sha256_file(path) != expected:
                errors.append(f"active runtime binding {name} does not match loaded bytes")
        expected_git_sha = item.get("git_binary_sha256")
        try:
            git_path, git_sha = _read_git_identity(item.get("git_binary_path"))
            git_version = _read_git_version(git_path, expected_git_sha)
        except ValidationError:
            errors.append("active runtime Git binding is unavailable or unsafe")
        else:
            if (
                git_path != item.get("git_binary_path")
                or not isinstance(expected_git_sha, str)
                or not _SHA_RE.fullmatch(expected_git_sha)
                or git_sha != expected_git_sha
                or git_version != item.get("git_version")
            ):
                errors.append("active runtime Git binding does not match loaded bytes")
        if require_media_probe:
            expected_probe_sha = item.get("ffprobe_binary_sha256")
            expected_ffmpeg_sha = item.get("ffmpeg_binary_sha256")
            try:
                probe_path, probe_sha = _read_ffprobe_identity(item.get("ffprobe_binary_path"))
                probe_version = _read_ffprobe_version(probe_path, expected_probe_sha)
                ffmpeg_path, ffmpeg_sha = _read_ffmpeg_identity(item.get("ffmpeg_binary_path"))
                ffmpeg_version = _read_ffmpeg_version(ffmpeg_path, expected_ffmpeg_sha)
            except ValidationError:
                errors.append("active runtime media-tool binding is unavailable or unsafe")
            else:
                if (
                    probe_path != item.get("ffprobe_binary_path")
                    or not isinstance(expected_probe_sha, str)
                    or not _SHA_RE.fullmatch(expected_probe_sha)
                    or probe_sha != expected_probe_sha
                    or probe_version != item.get("ffprobe_version")
                ):
                    errors.append("active runtime ffprobe binding does not match loaded bytes")
                if (
                    ffmpeg_path != item.get("ffmpeg_binary_path")
                    or not isinstance(expected_ffmpeg_sha, str)
                    or not _SHA_RE.fullmatch(expected_ffmpeg_sha)
                    or ffmpeg_sha != expected_ffmpeg_sha
                    or ffmpeg_version != item.get("ffmpeg_version")
                ):
                    errors.append("active runtime ffmpeg binding does not match loaded bytes")
            if (
                item.get("media_tool_binding_scope")
                != "primary_executable_bytes_and_version_only"
                or item.get("dynamic_library_dependency_closure_verified") is not False
                or item.get("media_executable_private_exact_byte_copy_required") is not True
            ):
                errors.append("active runtime media-tool identity scope is not fail-closed")
    elif item != {"state": "pending"}:
        errors.append("draft runtime bindings must remain pending")
    return item


def _target(value: Any, root: Path, errors: list[str]) -> dict[str, Any]:
    target = _strict(value, {"kind", "id"}, "target")
    expected_root = Path(__file__).resolve().parents[2] / "fixtures" / FIXTURE_ID
    if (
        target.get("kind") != "fixture"
        or target.get("id") != FIXTURE_ID
        or root != expected_root
    ):
        errors.append("authorization target does not match its fixture root")
    return target


def _bound_git(
    runtime_bindings: dict[str, Any],
    arguments: list[str],
    *,
    max_bytes: int = 2_000_000,
    allowed_returncodes: tuple[int, ...] = (0,),
) -> bytes:
    return pt._guide_git(
        arguments,
        max_bytes=max_bytes,
        git_path=runtime_bindings["git_binary_path"],
        git_sha256=runtime_bindings["git_binary_sha256"],
        allowed_returncodes=allowed_returncodes,
    )


def _verify_local_git_object_store(runtime_bindings: dict[str, Any]) -> None:
    shallow = _bound_git(runtime_bindings, ["rev-parse", "--is-shallow-repository"])
    if shallow.strip() != b"false":
        raise ValidationError("ElevenLabs source proof requires a non-shallow local repository")
    config = _bound_git(runtime_bindings, ["config", "--local", "--null", "--list"])
    try:
        for entry in config.split(b"\x00"):
            if not entry:
                continue
            key = entry.split(b"\n", 1)[0].decode("ascii", errors="strict").lower()
            if key == "extensions.partialclone" or (
                key.startswith("remote.")
                and (key.endswith(".promisor") or key.endswith(".partialclonefilter"))
            ):
                raise ValidationError("ElevenLabs source proof forbids partial or promisor repositories")
    except UnicodeError:
        raise ValidationError("ElevenLabs local Git configuration is malformed") from None
    finally:
        config = b""


def _parse_window(document: dict[str, Any], *, active: bool, errors: list[str]) -> tuple[datetime | None, datetime | None]:
    approved_at = _parse_time(document.get("approved_at"), "approved_at", errors) if active else None
    expires_at = _parse_time(document.get("expires_at"), "expires_at", errors) if active else None
    if active and approved_at is not None and expires_at is not None:
        if not approved_at < expires_at:
            errors.append("authorization expiry must follow approval")
        elif (expires_at - approved_at).total_seconds() > 86_400:
            errors.append("authorization window may not exceed 24 hours")
    return approved_at, expires_at


def _validate_authorization_location(
    path: Path,
    root: Path,
    status: Any,
    label: str,
    errors: list[str],
) -> None:
    if path.parent != root / "authorizations":
        errors.append(f"{label} must live directly under authorizations/")
        return
    active_name = ".ACTIVE." in path.name
    draft_name = ".DRAFT." in path.name or path.name.endswith(".DRAFT.json")
    if status == "active" and not active_name:
        errors.append(f"{label} ACTIVE status must use an .ACTIVE. filename")
    if status == "draft" and not draft_name:
        errors.append(f"{label} draft status must use a .DRAFT. filename")
    if (status == "active" and draft_name) or (status == "draft" and active_name):
        errors.append(f"{label} filename contradicts its status")


def _read_record(root: Path, relative: Any, expected_sha: Any, label: str, *, mode: int | None = None) -> tuple[Path, dict[str, Any], bytes, str]:
    path = pt._safe_relative(root, relative, f"{label} path", must_exist=True, suffix=".json")
    document, raw, actual_sha = pt._read_bound_fixture_json(
        root,
        path,
        label,
        required_mode=mode,
    )
    if not isinstance(expected_sha, str) or not _SHA_RE.fullmatch(expected_sha) or actual_sha != expected_sha:
        raise ValidationError(f"{label} SHA-256 mismatch")
    return path, document, raw, actual_sha


def _verified_prerequisite(root: Path, value: Any, label: str) -> tuple[Path, dict[str, Any], bytes, str]:
    item = _strict(value, {"state", "path", "sha256"}, label)
    if item.get("state") != "verified":
        raise ValidationError(f"{label}.state must be verified")
    return _read_record(root, item.get("path"), item.get("sha256"), label)


def _read_bound_blob(
    root: Path,
    path: Path,
    label: str,
    *,
    max_bytes: int = 5_000_000,
    required_mode: int | None = None,
    required_uid: int | None = None,
) -> tuple[bytes, str]:
    try:
        relative = path.absolute().relative_to(root).as_posix()
    except ValueError:
        raise ValidationError(f"{label} is outside the fixture root") from None
    parent_fd, name = pt._open_parent_descriptor(root, relative, create_parents=False)
    descriptor: int | None = None
    chunks: list[bytes] = []
    try:
        descriptor = os.open(name, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0), dir_fd=parent_fd)
        before = os.fstat(descriptor)
        if (
            not stat.S_ISREG(before.st_mode)
            or not 0 < before.st_size <= max_bytes
            or (required_mode is not None and stat.S_IMODE(before.st_mode) != required_mode)
            or (required_uid is not None and before.st_uid != required_uid)
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
            or (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns, before.st_mode, before.st_uid)
            != (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns, after.st_mode, after.st_uid)
        ):
            raise ValidationError(f"{label} changed during its bound read")
        return raw, sha256_bytes(raw)
    except ValidationError:
        raise
    except OSError:
        raise ValidationError(f"{label} is missing or unsafe") from None
    finally:
        chunks = []
        if descriptor is not None:
            os.close(descriptor)
        os.close(parent_fd)


def _parse_recovery_dotenv_key(raw: bytes) -> str:
    """Parse one literal, unexpanded key assignment without dotenv execution."""

    prefix = (API_KEY_ENV + "=").encode("ascii")
    ambiguous = re.compile(
        rb"^[ \t]*(?:export[ \t]+)?ELEVENLABS_API_KEY[ \t]*="
    )
    assignments: list[bytes] = []
    value_bytes = b""
    line = b""
    utf8_invalid = False
    try:
        if not isinstance(raw, bytes) or not 0 < len(raw) <= RECOVERY_DOTENV_MAX_BYTES:
            raise ValidationError("fixed recovery dotenv is empty or exceeds its byte ceiling")
        if b"\x00" in raw or b"\r" in raw:
            raise ValidationError("fixed recovery dotenv contains forbidden bytes")
        try:
            raw.decode("utf-8", errors="strict")
        except UnicodeError as exc:
            exc.__cause__ = None
            exc.__context__ = None
            exc.__suppress_context__ = True
            exc.__traceback__ = None
            utf8_invalid = True
        if utf8_invalid:
            raise ValidationError("fixed recovery dotenv is not strict UTF-8")
        for line in raw.split(b"\n"):
            if line.startswith(prefix):
                assignments.append(line[len(prefix) :])
            elif ambiguous.match(line):
                raise ValidationError(
                    "fixed recovery dotenv contains a non-literal or ambiguous ELEVENLABS_API_KEY assignment"
                )
        if len(assignments) != 1:
            raise ValidationError(
                "fixed recovery dotenv must contain exactly one literal ELEVENLABS_API_KEY assignment"
            )
        value_bytes = assignments[0]
        if (
            not 1 <= len(value_bytes) <= 512
            or value_bytes != value_bytes.strip()
            or any(byte < 33 or byte > 126 for byte in value_bytes)
        ):
            raise ValidationError("fixed recovery dotenv key assignment is malformed")
        return value_bytes.decode("ascii", errors="strict")
    finally:
        assignments = []
        value_bytes = b""
        line = b""
        utf8_invalid = False
        raw = b""


def _read_bounded_recovery_dotenv_key(path: Path) -> str:
    """Descriptor-read one current-UID, mode-0600, single-link dotenv file."""

    path = Path(path).absolute()
    if not path.is_absolute() or not path.name or "\x00" in str(path):
        raise ValidationError("fixed recovery dotenv path is invalid")
    parent_fd = os.open(
        "/",
        os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_CLOEXEC", 0),
    )
    descriptor: int | None = None
    chunks: list[bytes] = []
    chunk = b""
    raw = b""
    try:
        for component in path.parts[1:-1]:
            next_fd = os.open(
                component,
                os.O_RDONLY
                | getattr(os, "O_DIRECTORY", 0)
                | getattr(os, "O_NOFOLLOW", 0)
                | getattr(os, "O_CLOEXEC", 0),
                dir_fd=parent_fd,
            )
            os.close(parent_fd)
            parent_fd = next_fd
        descriptor = os.open(
            path.name,
            os.O_RDONLY
            | getattr(os, "O_NOFOLLOW", 0)
            | getattr(os, "O_CLOEXEC", 0)
            | getattr(os, "O_NONBLOCK", 0),
            dir_fd=parent_fd,
        )
        before = os.fstat(descriptor)
        if (
            not stat.S_ISREG(before.st_mode)
            or stat.S_IMODE(before.st_mode) != 0o600
            or before.st_uid != os.getuid()
            or before.st_nlink != 1
            or not 0 < before.st_size <= RECOVERY_DOTENV_MAX_BYTES
        ):
            raise ValidationError(
                "fixed recovery dotenv must be a bounded current-UID mode-0600 single-link regular file"
            )
        received = 0
        while True:
            chunk = os.read(
                descriptor,
                min(65_536, RECOVERY_DOTENV_MAX_BYTES + 1 - received),
            )
            if not chunk:
                break
            chunks.append(chunk)
            received += len(chunk)
            if received > RECOVERY_DOTENV_MAX_BYTES:
                raise ValidationError("fixed recovery dotenv exceeds its byte ceiling")
        raw = b"".join(chunks)
        after = os.fstat(descriptor)
        identity_fields = (
            "st_dev", "st_ino", "st_size", "st_mtime_ns", "st_ctime_ns",
            "st_mode", "st_uid", "st_gid", "st_nlink",
        )
        if (
            len(raw) != before.st_size
            or tuple(getattr(before, field) for field in identity_fields)
            != tuple(getattr(after, field) for field in identity_fields)
        ):
            raise ValidationError("fixed recovery dotenv changed during its descriptor read")
        return _parse_recovery_dotenv_key(raw)
    except ValidationError:
        raise
    except OSError:
        raise ValidationError("fixed recovery dotenv is missing or unsafe") from None
    finally:
        chunks = []
        chunk = b""
        raw = b""
        if descriptor is not None:
            os.close(descriptor)
        os.close(parent_fd)


def _read_recovery_dotenv_key() -> str:
    """The executor's only credential-delivery path; never reads the environment."""

    return _read_bounded_recovery_dotenv_key(RECOVERY_DOTENV_PATH)


def _recovery_transfer_utf8_valid(value: bytearray) -> bool:
    """Validate UTF-8 without materializing an immutable copy of dotenv bytes."""

    index = 0
    length = len(value)
    while index < length:
        first = value[index]
        if first <= 0x7F:
            index += 1
            continue
        if 0xC2 <= first <= 0xDF:
            width = 2
        elif 0xE0 <= first <= 0xEF:
            width = 3
        elif 0xF0 <= first <= 0xF4:
            width = 4
        else:
            return False
        if index + width > length:
            return False
        second = value[index + 1]
        if second < 0x80 or second > 0xBF:
            return False
        if first == 0xE0 and second < 0xA0:
            return False
        if first == 0xED and second > 0x9F:
            return False
        if first == 0xF0 and second < 0x90:
            return False
        if first == 0xF4 and second > 0x8F:
            return False
        for offset in range(2, width):
            continuation = value[index + offset]
            if continuation < 0x80 or continuation > 0xBF:
                return False
        index += width
    return True


def _recovery_transfer_segment_equals(
    value: bytearray,
    start: int,
    end: int,
    literal: bytes,
) -> bool:
    if end - start != len(literal):
        return False
    return all(value[start + offset] == byte for offset, byte in enumerate(literal))


def _parse_recovery_transfer_dotenv_key(raw: bytearray) -> bytearray:
    """Return one mutable exact assignment and erase the mutable dotenv buffer."""

    prefix = (API_KEY_ENV + "=").encode("ascii")
    variable = API_KEY_ENV.encode("ascii")
    assignment: tuple[int, int] | None = None
    held = bytearray()
    try:
        if not isinstance(raw, bytearray) or not 0 < len(raw) <= RECOVERY_DOTENV_MAX_BYTES:
            raise ValidationError("fixed recovery dotenv is empty or exceeds its byte ceiling")
        if 0 in raw or 13 in raw or not _recovery_transfer_utf8_valid(raw):
            raise ValidationError("fixed recovery dotenv is not strict UTF-8")
        start = 0
        while start <= len(raw):
            newline = raw.find(10, start)
            end = len(raw) if newline < 0 else newline
            if end - start >= len(prefix) and _recovery_transfer_segment_equals(
                raw,
                start,
                start + len(prefix),
                prefix,
            ):
                if assignment is not None:
                    raise ValidationError(
                        "fixed recovery dotenv must contain exactly one literal ELEVENLABS_API_KEY assignment"
                    )
                assignment = (start + len(prefix), end)
            else:
                cursor = start
                while cursor < end and raw[cursor] in {32, 9}:
                    cursor += 1
                export_end = cursor + len(b"export")
                if (
                    export_end < end
                    and _recovery_transfer_segment_equals(raw, cursor, export_end, b"export")
                    and raw[export_end] in {32, 9}
                ):
                    cursor = export_end
                    while cursor < end and raw[cursor] in {32, 9}:
                        cursor += 1
                variable_end = cursor + len(variable)
                if (
                    variable_end <= end
                    and _recovery_transfer_segment_equals(
                        raw,
                        cursor,
                        variable_end,
                        variable,
                    )
                ):
                    cursor = variable_end
                    while cursor < end and raw[cursor] in {32, 9}:
                        cursor += 1
                    if cursor < end and raw[cursor] == 61:
                        raise ValidationError(
                            "fixed recovery dotenv contains a non-literal or ambiguous ELEVENLABS_API_KEY assignment"
                        )
            if newline < 0:
                break
            start = newline + 1
        if assignment is None:
            raise ValidationError(
                "fixed recovery dotenv must contain exactly one literal ELEVENLABS_API_KEY assignment"
            )
        value_start, value_end = assignment
        if not 1 <= value_end - value_start <= 512:
            raise ValidationError("fixed recovery dotenv key assignment is malformed")
        for index in range(value_start, value_end):
            held.append(raw[index])
        if any(byte < 33 or byte > 126 for byte in held):
            raise ValidationError("fixed recovery dotenv key assignment is malformed")
        result = held
        held = bytearray()
        return result
    except BaseException:
        _zero_mutable_buffer(held)
        raise
    finally:
        _zero_mutable_buffer(raw)


class _RecoveryTransferCredentialReadFailure(ValidationError):
    def __init__(self, state: str) -> None:
        super().__init__("fixed recovery dotenv read stopped safely")
        self.credential_bytes_read_state = state


def _read_recovery_transfer_dotenv_key() -> bytearray:
    """Descriptor-read the fixed dotenv exactly once into mutable storage."""

    path = RECOVERY_DOTENV_PATH
    parent_fd = os.open(
        "/",
        os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_CLOEXEC", 0),
    )
    descriptor: int | None = None
    raw = bytearray()
    view: memoryview | None = None
    received = 0
    try:
        for component in path.parts[1:-1]:
            next_fd = os.open(
                component,
                os.O_RDONLY
                | getattr(os, "O_DIRECTORY", 0)
                | getattr(os, "O_NOFOLLOW", 0)
                | getattr(os, "O_CLOEXEC", 0),
                dir_fd=parent_fd,
            )
            os.close(parent_fd)
            parent_fd = next_fd
        descriptor = os.open(
            path.name,
            os.O_RDONLY
            | getattr(os, "O_NOFOLLOW", 0)
            | getattr(os, "O_CLOEXEC", 0)
            | getattr(os, "O_NONBLOCK", 0),
            dir_fd=parent_fd,
        )
        before = os.fstat(descriptor)
        if (
            not stat.S_ISREG(before.st_mode)
            or stat.S_IMODE(before.st_mode) != 0o600
            or before.st_uid != os.getuid()
            or before.st_nlink != 1
            or not 0 < before.st_size <= RECOVERY_DOTENV_MAX_BYTES
        ):
            raise ValidationError(
                "fixed recovery dotenv must be a bounded current-UID mode-0600 single-link regular file"
            )
        raw = bytearray(before.st_size)
        view = memoryview(raw)
        while received < before.st_size:
            try:
                count = os.readv(descriptor, [view[received:]])
            except InterruptedError:
                continue
            if count <= 0:
                break
            received += count
        after = os.fstat(descriptor)
        identity_fields = (
            "st_dev", "st_ino", "st_size", "st_mtime_ns", "st_ctime_ns",
            "st_mode", "st_uid", "st_gid", "st_nlink",
        )
        if (
            received != before.st_size
            or len(raw) != before.st_size
            or tuple(getattr(before, field) for field in identity_fields)
            != tuple(getattr(after, field) for field in identity_fields)
        ):
            raise ValidationError("fixed recovery dotenv changed during its descriptor read")
        return _parse_recovery_transfer_dotenv_key(raw)
    except ValidationError as exc:
        state = "bytes_read_not_accepted" if received else "no_credential_bytes_read"
        exc.__traceback__ = None
        exc.__cause__ = None
        exc.__context__ = None
        raise _RecoveryTransferCredentialReadFailure(state) from None
    except OSError as exc:
        state = "bytes_read_not_accepted" if received else "no_credential_bytes_read"
        exc.__traceback__ = None
        exc.__cause__ = None
        exc.__context__ = None
        raise _RecoveryTransferCredentialReadFailure(state) from None
    finally:
        if view is not None:
            view.release()
        view = None
        _zero_mutable_buffer(raw)
        if descriptor is not None:
            os.close(descriptor)
        os.close(parent_fd)


def _validate_browser_readiness(
    root: Path,
    value: Any,
    errors: list[str],
    *,
    expected_observer: str,
) -> tuple[
    Path,
    dict[str, Any],
    bytes,
    str,
    datetime | None,
    tuple[Path, bytes, str],
    tuple[Path, bytes, str],
]:
    path, document, raw, actual_sha = _verified_prerequisite(
        root,
        value,
        "ElevenLabs browser readiness",
    )
    _strict(
        document,
        {
            "schema_version", "provider", "source", "observed_by", "observed_at",
            "owner", "owner_authenticated_session", "same_authenticated_session",
            "data_use", "api_key", "target_voice", "official_data_use_basis",
            "capture", "raw_account_identifier_recorded", "raw_api_key_recorded",
            "raw_api_key_preview_recorded", "account_setting_changed_by_capture",
        },
        "ElevenLabs browser readiness evidence",
    )
    data_use = _strict(
        document.get("data_use"),
        {
            "setting_label", "improve_models_for_everyone", "update_completed",
            "protection_mode", "protection_effective_for_new_submissions",
        },
        "browser readiness data_use",
    )
    key = _strict(
        document.get("api_key"),
        {
            "label", "preview_kind", "preview_canonicalization", "preview_length",
            "preview_mask_shape", "preview_sha256", "preview_domain_separation",
            "preview_hash_is_non_confidential", "linkage_strength", "key_enabled",
            "provider_key_id_capture_state", "provider_key_id_sha256",
            "restrict_key_on", "speech_to_speech_access_selected", "user_access_selected",
            "auto_disable_if_leaked_on",
        },
        "browser readiness api_key",
    )
    voice = _strict(
        document.get("target_voice"),
        {"voice_id", "voice_name", "visibly_present"},
        "browser readiness target_voice",
    )
    capture = _strict(document.get("capture"), {"path", "sha256"}, "browser readiness capture")
    official_binding = _strict(
        document.get("official_data_use_basis"),
        {"state", "path", "sha256"},
        "browser readiness official data-use basis",
    )
    if official_binding.get("state") != "verified":
        errors.append("browser readiness official data-use basis must be verified")
    official_path, official, official_raw, official_sha = _read_record(
        root,
        official_binding.get("path"),
        official_binding.get("sha256"),
        "official ElevenLabs data-use basis",
    )
    _strict(
        official,
        {
            "schema_version", "provider", "url", "title", "accessed_at",
            "supported_statement", "supported_statement_sha256", "scope",
            "raw_account_data_recorded",
        },
        "official ElevenLabs data-use basis",
    )
    if (
        official.get("schema_version") != "oe-elevenlabs-data-use-official-basis-v1"
        or official.get("provider") != "elevenlabs"
        or official.get("url") != DATA_USE_BASIS_URL
        or official.get("accessed_at") != "2026-08-26"
        or official.get("supported_statement") != DATA_USE_BASIS_STATEMENT
        or official.get("supported_statement_sha256") != DATA_USE_BASIS_STATEMENT_SHA256
        or official.get("scope") != "new_submissions_after_processed_opt_out"
        or official.get("raw_account_data_recorded") is not False
    ):
        errors.append("official ElevenLabs basis does not support the exact new-submission exclusion")
    capture_path = root
    capture_bytes = b""
    capture_sha = ""
    try:
        capture_path = pt._safe_relative(
            root,
            capture.get("path"),
            "browser readiness redacted capture",
            must_exist=True,
            suffix=".png",
        )
        if capture_path.relative_to(root).parts[:2] != ("evidence", "browser-readiness"):
            raise ValidationError("browser readiness capture must remain under evidence/browser-readiness/")
        capture_bytes, capture_sha = _read_bound_blob(
            root,
            capture_path,
            "browser readiness redacted capture",
        )
        if capture_sha != capture.get("sha256"):
            errors.append("browser readiness redacted capture SHA-256 mismatch")
        if not capture_bytes.startswith(b"\x89PNG\r\n\x1a\n"):
            errors.append("browser readiness redacted capture is not PNG")
    except (OSError, ValidationError):
        raise ValidationError("browser readiness redacted capture is missing or unsafe") from None
    preview_sha = key.get("preview_sha256")
    if (
        document.get("schema_version") != "oe-elevenlabs-account-browser-readiness-v1"
        or document.get("provider") != "elevenlabs"
        or document.get("source") != "codex_agent_read_only_chrome_inspection"
        or document.get("observed_by") != "Codex"
        or document.get("owner") != expected_observer
        or document.get("owner_authenticated_session") is not True
        or document.get("same_authenticated_session") is not True
        or document.get("raw_account_identifier_recorded") is not False
        or document.get("raw_api_key_recorded") is not False
        or document.get("raw_api_key_preview_recorded") is not False
        or document.get("account_setting_changed_by_capture") is not False
        or data_use.get("setting_label") != "Improve the models for everyone"
        or data_use.get("improve_models_for_everyone") is not False
        or data_use.get("update_completed") is not True
        or data_use.get("protection_mode") != pt.ACCOUNT_TRAINING_OPT_OUT_PROTECTION
        or data_use.get("protection_effective_for_new_submissions") is not True
        or key.get("label") != "operator-economy-v1"
        or key.get("preview_kind") != API_KEY_PREVIEW_KIND
        or key.get("preview_canonicalization") != API_KEY_PREVIEW_CANONICALIZATION
        or key.get("preview_length") != 4
        or key.get("preview_mask_shape") != "masked_prefix_plus_four_ascii_suffix"
        or not isinstance(preview_sha, str)
        or not _SHA_RE.fullmatch(preview_sha)
        or key.get("preview_domain_separation") != API_KEY_PREVIEW_DOMAIN_TEXT
        or key.get("preview_hash_is_non_confidential") is not True
        or key.get("linkage_strength") != "contextual_non_cryptographic"
        or key.get("key_enabled") is not True
        or key.get("restrict_key_on") is not True
        or key.get("speech_to_speech_access_selected") is not True
        or key.get("user_access_selected") is not True
        or key.get("auto_disable_if_leaked_on") is not True
        or voice.get("voice_id") != pt.TRANSFER_TARGET_VOICE_ID
        or voice.get("voice_name") != "OE Narrator Manav C Base v1"
        or voice.get("visibly_present") is not True
    ):
        errors.append("browser readiness does not prove OFF/processed, key preview, and Original C in one session")
    key_id_state = key.get("provider_key_id_capture_state")
    key_id_sha = key.get("provider_key_id_sha256")
    if not (
        (key_id_state == "unavailable" and key_id_sha is None)
        or (
            key_id_state == "verified"
            and isinstance(key_id_sha, str)
            and bool(_SHA_RE.fullmatch(key_id_sha))
        )
    ):
        errors.append("browser readiness provider key-ID capture state is not truthful")
    observed_at = _parse_time(document.get("observed_at"), "browser readiness observed_at", errors)
    return (
        path,
        document,
        raw,
        actual_sha,
        observed_at,
        (capture_path, capture_bytes, capture_sha),
        (official_path, official_raw, official_sha),
    )


def _validate_account_owner_approval(
    root: Path,
    value: Any,
    errors: list[str],
    *,
    expected_owner: str,
) -> tuple[Path, dict[str, Any], bytes, str, datetime | None]:
    path, document, raw, actual_sha = _verified_prerequisite(
        root,
        value,
        "ElevenLabs account owner approval",
    )
    _strict(
        document,
        {
            "schema_version", "provider", "source", "recorded_by", "recorded_at",
            "owner", "approval_basis", "approved_scope", "execution_gate",
        },
        "ElevenLabs account owner approval evidence",
    )
    basis = _strict(
        document.get("approval_basis"),
        {
            "assistant_confirmation_prompt", "owner_reply",
            "approval_event_timestamp_available",
            "record_materialization_time_is_not_claimed_as_message_time",
        },
        "account owner approval basis",
    )
    scope = _strict(
        document.get("approved_scope"),
        {"action", "authorized_limits"},
        "account owner approved scope",
    )
    gate = _strict(
        document.get("execution_gate"),
        {
            "this_record_is_an_active_provider_authorization",
            "credentials_may_be_accessed_from_this_record",
            "network_may_be_called_from_this_record",
            "separate_active_authorization_required",
            "voice_transfer_authorized",
        },
        "account owner approval execution gate",
    )
    if ACCOUNT_OWNER_APPROVAL_REPLY is None:
        errors.append("literal owner reply to the account-readback prompt is not yet frozen")
    if (
        document.get("schema_version")
        != "oe-elevenlabs-account-verification-owner-approval-evidence-v1"
        or document.get("provider") != "elevenlabs"
        or document.get("source") != "current_codex_thread_contextual_assent"
        or document.get("recorded_by") != "Codex"
        or document.get("owner") != expected_owner
        or basis.get("assistant_confirmation_prompt") != ACCOUNT_OWNER_APPROVAL_PROMPT
        or basis.get("owner_reply") != ACCOUNT_OWNER_APPROVAL_REPLY
        or basis.get("approval_event_timestamp_available") is not False
        or basis.get("record_materialization_time_is_not_claimed_as_message_time") is not True
        or not _exact(scope.get("action"), _action_account())
        or not _exact(scope.get("authorized_limits"), _account_limits(True))
        or gate.get("this_record_is_an_active_provider_authorization") is not False
        or gate.get("credentials_may_be_accessed_from_this_record") is not False
        or gate.get("network_may_be_called_from_this_record") is not False
        or gate.get("separate_active_authorization_required") is not True
        or gate.get("voice_transfer_authorized") is not False
    ):
        errors.append("account owner approval does not bind the exact one-GET prompt and literal reply")
    recorded_at = _parse_time(
        document.get("recorded_at"),
        "account owner approval recorded_at",
        errors,
    )
    return path, document, raw, actual_sha, recorded_at


def _validate_media_contract_basis(
    root: Path,
    value: Any,
    errors: list[str],
) -> tuple[Path, dict[str, Any], bytes, str]:
    path, document, raw, actual_sha = _verified_prerequisite(
        root,
        value,
        "ElevenLabs official PCM media-contract basis",
    )
    _strict(
        document,
        {
            "schema_version", "provider", "endpoint", "output_format",
            "declared_mime_allowlist", "sources", "canonical_interpretation",
            "canonical_interpretation_sha256", "accessed_at",
            "raw_provider_response_recorded",
        },
        "ElevenLabs official PCM media-contract basis",
    )
    expected_sources = [
        {
            "url": MEDIA_OPENAPI_URL,
            "proposition": (
                "The current exact /v1/speech-to-speech/{voice_id} operation allows "
                "output_format=pcm_48000 and declares HTTP 200 content as audio/mpeg."
            ),
        },
        {
            "url": MEDIA_PCM_FORMAT_URL,
            "proposition": (
                "Supported output formats define PCM as S16LE, include 48 kHz, and specify "
                "16-bit depth."
            ),
        },
        {
            "url": MEDIA_STS_URL,
            "proposition": (
                "The exact Speech-to-Speech endpoint describes generated streaming audio and "
                "supports the output_format enum."
            ),
        },
    ]
    if (
        path.relative_to(root).as_posix() != MEDIA_CONTRACT_BASIS_PATH
        or actual_sha != MEDIA_CONTRACT_BASIS_SHA256
        or document.get("schema_version") != MEDIA_CONTRACT_BASIS_SCHEMA
        or document.get("provider") != "elevenlabs"
        or document.get("endpoint") != pt.TRANSFER_ENDPOINT
        or document.get("output_format") != pt.TRANSFER_PRIMARY_FORMAT
        or document.get("declared_mime_allowlist") != ["audio/pcm", "audio/mpeg"]
        or document.get("sources") != expected_sources
        or document.get("canonical_interpretation") != MEDIA_CONTRACT_INTERPRETATION
        or document.get("canonical_interpretation_sha256")
        != MEDIA_CONTRACT_INTERPRETATION_SHA256
        or document.get("accessed_at") != "2026-08-26"
        or document.get("raw_provider_response_recorded") is not False
    ):
        errors.append("official media-contract basis does not support exact pcm_48000 interpretation")
    return path, document, raw, actual_sha


def _read_selected_wav(root: Path, selected: dict[str, Any]) -> tuple[bytes, dict[str, Any]]:
    relative = selected.get("path")
    if relative != SELECTED_GUIDE_PATH:
        raise ValidationError("selected guide must be exact candidate B")
    parent_fd, name = pt._open_parent_descriptor(root, relative, create_parents=False)
    descriptor: int | None = None
    chunks: list[bytes] = []
    chunk = b""
    try:
        descriptor = os.open(name, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0), dir_fd=parent_fd)
        before = os.fstat(descriptor)
        if (
            not stat.S_ISREG(before.st_mode)
            or stat.S_IMODE(before.st_mode) != 0o600
            or before.st_size != SELECTED_GUIDE_BYTES
        ):
            raise ValidationError("candidate B byte count mismatch")
        received = 0
        while True:
            chunk = os.read(descriptor, min(65_536, SELECTED_GUIDE_BYTES + 1 - received))
            if not chunk:
                break
            chunks.append(chunk)
            received += len(chunk)
            if received > SELECTED_GUIDE_BYTES:
                raise ValidationError("candidate B exceeds its exact byte binding")
        data = b"".join(chunks)
        after = os.fstat(descriptor)
        if (
            len(data) != SELECTED_GUIDE_BYTES
            or sha256_bytes(data) != SELECTED_GUIDE_SHA256
            or (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns, before.st_mode, before.st_uid)
            != (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns, after.st_mode, after.st_uid)
        ):
            raise ValidationError("candidate B changed during its bound read")
        try:
            geometry = pt._validate_google_wav_bytes(data)
        except Exception:
            raise ValidationError("candidate B is not the exact fully decoded 24 kHz mono PCM WAV") from None
        if abs(float(geometry["duration_seconds"]) - SELECTED_GUIDE_DURATION_SECONDS) > 1e-12:
            raise ValidationError("candidate B duration mismatch")
        return data, geometry
    except ValidationError:
        raise
    except OSError:
        raise ValidationError("candidate B is missing or unsafe") from None
    finally:
        chunks = []
        chunk = b""
        if descriptor is not None:
            os.close(descriptor)
        os.close(parent_fd)


def _action_account() -> dict[str, Any]:
    return {
        "provider": "elevenlabs",
        "endpoint": ACCOUNT_ENDPOINT,
        "method": "GET",
        "credential_header_name": "xi-api-key",
        "accept": "application/json",
        "accept_encoding": "identity",
        "no_post": True,
        "no_mutation": True,
        "no_retry": True,
        "no_redirect": True,
        "raw_response_storage_forbidden": True,
    }


def _action_transfer(enable_logging: bool | str) -> dict[str, Any]:
    return {
        "provider": "elevenlabs",
        "endpoint": pt.TRANSFER_ENDPOINT,
        "method": "POST",
        "target_voice_id": pt.TRANSFER_TARGET_VOICE_ID,
        "model_id": pt.TRANSFER_MODEL,
        "seed": pt.TRANSFER_SEED,
        "query": {"enable_logging": enable_logging, "output_format": pt.TRANSFER_PRIMARY_FORMAT},
        "voice_settings": pt.TRANSFER_VOICE_SETTINGS,
        "remove_background_noise": False,
        "file_format": "other",
        "credential_header_name": "xi-api-key",
        "accept": "application/octet-stream",
        "accept_encoding": "identity",
        "no_fallback": True,
        "no_retry": True,
        "no_redirect": True,
        "disclosure": "one_private_exact_candidate_b_to_saved_original_c_voice_changer_test",
    }


def _account_limits(active: bool) -> dict[str, Any]:
    if not active:
        return {
            "max_get_calls": 0,
            "max_post_calls": 0,
            "max_response_bytes": 0,
            "max_error_response_bytes": 0,
            "max_request_elapsed_seconds": 0,
            "max_spend_usd": 0,
        }
    return {
        "max_get_calls": ACCOUNT_MAX_GET_CALLS,
        "max_post_calls": ACCOUNT_MAX_POST_CALLS,
        "max_response_bytes": ACCOUNT_MAX_RESPONSE_BYTES,
        "max_error_response_bytes": ACCOUNT_MAX_ERROR_RESPONSE_BYTES,
        "max_request_elapsed_seconds": ACCOUNT_MAX_ELAPSED_SECONDS,
        "max_spend_usd": 0,
    }


def _transfer_limits(active: bool) -> dict[str, Any]:
    if not active:
        return {
            "max_account_get_calls": 0,
            "max_generation_post_calls": 0,
            "max_outputs": 0,
            "max_source_bytes": 0,
            "max_source_duration_seconds": 0,
            "max_submitted_seconds": 0,
            "max_request_body_bytes": 0,
            "max_response_bytes": 0,
            "min_output_duration_seconds": 0,
            "max_output_duration_seconds": 0,
            "min_output_to_source_duration_ratio": 0,
            "max_output_to_source_duration_ratio": 0,
            "max_error_response_bytes": 0,
            "max_request_elapsed_seconds": 0,
            "max_spend_usd": 0,
        }
    return {
        "max_account_get_calls": TRANSFER_MAX_ACCOUNT_GET_CALLS,
        "max_generation_post_calls": TRANSFER_MAX_GENERATION_POST_CALLS,
        "max_outputs": TRANSFER_MAX_OUTPUTS,
        "max_source_bytes": SELECTED_GUIDE_BYTES,
        "max_source_duration_seconds": SELECTED_GUIDE_DURATION_SECONDS,
        "max_submitted_seconds": SELECTED_GUIDE_DURATION_SECONDS,
        "max_request_body_bytes": TRANSFER_BODY_BYTES,
        "max_response_bytes": TRANSFER_MAX_RESPONSE_BYTES,
        "min_output_duration_seconds": TRANSFER_MIN_OUTPUT_DURATION_SECONDS,
        "max_output_duration_seconds": TRANSFER_MAX_OUTPUT_DURATION_SECONDS,
        "min_output_to_source_duration_ratio": TRANSFER_MIN_OUTPUT_TO_SOURCE_DURATION_RATIO,
        "max_output_to_source_duration_ratio": TRANSFER_MAX_OUTPUT_TO_SOURCE_DURATION_RATIO,
        "max_error_response_bytes": TRANSFER_MAX_ERROR_RESPONSE_BYTES,
        "max_request_elapsed_seconds": TRANSFER_MAX_ELAPSED_SECONDS,
        "max_spend_usd": TRANSFER_MAX_SPEND_USD,
    }


def _account_artifacts(authorization_id: str) -> dict[str, str]:
    return {
        "success_receipt_path": f"receipts/elevenlabs-account/{authorization_id}.run.json",
        "failure_receipt_path": f"receipts/elevenlabs-account/{authorization_id}.failure.json",
    }


def _transfer_artifacts(authorization_id: str) -> dict[str, str]:
    return {
        "raw_output_path": TRANSFER_RAW_PATH,
        "working_output_path": TRANSFER_WORKING_PATH,
        "success_receipt_path": f"receipts/elevenlabs/{authorization_id}.run.json",
        "failure_receipt_path": f"receipts/elevenlabs/{authorization_id}.failure.json",
        "conversion_receipt_path": f"receipts/elevenlabs/{authorization_id}.conversion.json",
    }


def _recovery_transfer_artifacts(active: bool) -> dict[str, str]:
    """Return the status-bound paths for the additive one-transaction branch."""

    return _transfer_artifacts(
        RECOVERY_TRANSFER_ACTIVE_ID if active else RECOVERY_TRANSFER_DRAFT_ID
    )


def _account_consumption_path(authorization_id: str) -> str:
    del authorization_id
    return ACCOUNT_SCOPE_LATCH_PATH


def _transfer_consumption_path(authorization_id: str) -> str:
    del authorization_id
    return TRANSFER_SCOPE_LATCH_PATH


def validate_account_verification_authorization(authorization_path: Path) -> dict[str, Any]:
    """Validate one zero-mutation `/v1/user` authority without credentials."""

    authorization_path = Path(authorization_path).absolute()
    root = pt._document_root(authorization_path)
    authorization, _raw, authorization_sha256 = pt._read_bound_fixture_json(
        root,
        authorization_path,
        "ElevenLabs account-verification authorization",
    )
    keys = {
        "schema_version", "authorization_id", "status", "approved", "scope", "target",
        "owner_approval", "browser_readiness", "action", "credential_binding",
        "runtime_bindings", "authorized_limits",
        "artifacts", "consumption", "approved_by", "approved_at", "expires_at",
        "execution_ready", "blockers",
    }
    _strict(authorization, keys, "ElevenLabs account-verification authorization")
    errors: list[str] = []
    status = authorization.get("status")
    active = status == "active"
    if status not in {"draft", "active"}:
        errors.append("account-verification authorization status must be draft or active")
    _validate_authorization_location(
        authorization_path,
        root,
        status,
        "account-verification authorization",
        errors,
    )
    if authorization.get("schema_version") != ACCOUNT_AUTH_SCHEMA:
        errors.append("account-verification authorization schema mismatch")
    if authorization.get("scope") != ACCOUNT_SCOPE:
        errors.append("account-verification authorization scope mismatch")
    authorization_id = authorization.get("authorization_id")
    if not isinstance(authorization_id, str) or not _SAFE_ID_RE.fullmatch(authorization_id):
        errors.append("account-verification authorization ID is invalid")
        authorization_id = "invalid"
    _target(authorization.get("target"), root, errors)
    owner_approval_record: tuple[Path, dict[str, Any], bytes, str, datetime | None] | None = None
    browser_record: tuple[Any, ...] | None = None
    if active:
        owner_approval_record = _validate_account_owner_approval(
            root,
            authorization.get("owner_approval"),
            errors,
            expected_owner=authorization.get("approved_by"),
        )
        browser_record = _validate_browser_readiness(
            root,
            authorization.get("browser_readiness"),
            errors,
            expected_observer=authorization.get("approved_by"),
        )
    else:
        if not _exact(authorization.get("owner_approval"), {"state": "pending"}):
            errors.append("draft account owner approval must remain pending")
        if not _exact(authorization.get("browser_readiness"), {"state": "pending"}):
            errors.append("draft browser readiness must remain pending")
    if not _exact(authorization.get("action"), _action_account()):
        errors.append("account-verification action drifted")

    credential_keys = (
        {"state", "mechanism", "api_key_environment_variable", "domain_separation"}
        if active
        else {"state", "mechanism", "api_key_environment_variable"}
    )
    credential = _strict(authorization.get("credential_binding"), credential_keys, "credential_binding")
    expected_credential = (
        {
            "state": "verified",
            "mechanism": "environment_api_key",
            "api_key_environment_variable": API_KEY_ENV,
            "domain_separation": API_KEY_DOMAIN_TEXT,
        }
        if active
        else {
            "state": "pending",
            "mechanism": "environment_api_key",
            "api_key_environment_variable": API_KEY_ENV,
        }
    )
    for key, expected in expected_credential.items():
        if not _exact(credential.get(key), expected):
            errors.append(f"credential_binding.{key} drifted")
    _validate_runtime_bindings(
        authorization.get("runtime_bindings"),
        active=active,
        require_media_probe=False,
        errors=errors,
    )
    if not _exact(authorization.get("authorized_limits"), _account_limits(active)):
        errors.append("account-verification authorized limits drifted")
    if not _exact(authorization.get("artifacts"), _account_artifacts(authorization_id)):
        errors.append("account-verification artifact paths drifted")
    consumption = _strict(
        authorization.get("consumption"),
        {"status", "get_calls_used", "post_calls_used", "record_path"},
        "consumption",
    )
    expected_consumption = {
        "status": "unconsumed" if active else "not_authorized",
        "get_calls_used": 0,
        "post_calls_used": 0,
        "record_path": _account_consumption_path(authorization_id),
    }
    if not _exact(consumption, expected_consumption):
        errors.append("account-verification consumption state or path drifted")
    approved_at, expires_at = _parse_window(authorization, active=active, errors=errors)
    if active and browser_record is not None and approved_at is not None and expires_at is not None:
        owner_recorded_at = owner_approval_record[4] if owner_approval_record is not None else None
        observed_at = browser_record[4]
        if (
            owner_recorded_at is None
            or observed_at is None
            or not owner_recorded_at <= observed_at <= approved_at
        ):
            errors.append("owner approval, browser readiness, and account approval chronology is invalid")
        elif (approved_at - observed_at).total_seconds() > ACCOUNT_VERIFICATION_MAX_AGE_SECONDS:
            errors.append("browser readiness is too old at account-verification approval")
        elif expires_at > observed_at + timedelta(seconds=ACCOUNT_VERIFICATION_MAX_AGE_SECONDS):
            errors.append("account-verification expiry exceeds browser-readiness freshness")
    blockers = authorization.get("blockers")
    if not isinstance(blockers, list) or any(not isinstance(item, str) or not item for item in blockers):
        errors.append("account-verification blockers must be non-empty strings")
    if active:
        if authorization.get("approved") is not True or authorization.get("execution_ready") is not True:
            errors.append("active account verification must be approved and execution-ready")
        if not isinstance(authorization.get("approved_by"), str) or not authorization["approved_by"]:
            errors.append("active account verification requires approved_by")
        if blockers != []:
            errors.append("active account verification may not retain blockers")
    else:
        if authorization.get("approved") is not False or authorization.get("execution_ready") is not False:
            errors.append("draft account verification cannot be approved or execution-ready")
        if authorization.get("approved_by") != "" or authorization.get("approved_at") != "" or authorization.get("expires_at") != "":
            errors.append("draft account verification approval fields must be empty")
        if not blockers:
            errors.append("draft account verification must state blockers")
    _raise_errors(errors)
    return {
        "schema_version": "oe-elevenlabs-account-verification-dry-run-v1",
        "valid": True,
        "status": "active_exact_authority_validated" if active else "blocked_pending_active_account_verification",
        "authorization_status": status,
        "authorization_id": authorization_id,
        "authorization_sha256": authorization_sha256,
        "approved_at": _iso(approved_at) if approved_at else None,
        "expires_at": _iso(expires_at) if expires_at else None,
        "action": _action_account(),
        "maximum": _account_limits(active),
        "provider_action_authorized": active,
        "network_authorized": active,
        "execution_transport_available": active,
        "credentials_accessed": False,
        "network_called": False,
        "provider_calls_made": 0,
        "provider_post_calls_made": 0,
        "browser_readiness_sha256": browser_record[3] if browser_record else None,
        "owner_approval_sha256": owner_approval_record[3] if owner_approval_record else None,
        "account_settings_changed": False,
        "voice_transfer_authorized": False,
        "full_capture_authorized": False,
        "step3_authorized": False,
        "publication_authorized": False,
    }


def dry_run_account_verification(authorization_path: Path) -> dict[str, Any]:
    return validate_account_verification_authorization(authorization_path)


def _validate_lineage(root: Path, value: Any, plan_path: Path, canonical_w_path: Path) -> tuple[Path, dict[str, Any], bytes, str]:
    lineage = _strict(
        value,
        {"path", "sha256", "authorization_id", "status", "approved", "max_calls", "max_spend_usd"},
        "v1_lineage",
    )
    expected = {
        "path": V1_LINEAGE_PATH,
        "sha256": V1_LINEAGE_SHA256,
        "authorization_id": V1_LINEAGE_ID,
        "status": "draft",
        "approved": False,
        "max_calls": 0,
        "max_spend_usd": 0,
    }
    if not _exact(lineage, expected):
        raise ValidationError("historical V1 lineage drifted or carries authority")
    path, document, raw, actual_sha = _read_record(
        root,
        lineage["path"],
        lineage["sha256"],
        "historical zero-authority V1 draft",
    )
    dry = pt.validate_voice_transfer_authorization(path, plan_path, canonical_w_path)
    if (
        document.get("schema_version") != pt.TRANSFER_AUTH_SCHEMA
        or dry.get("status") != "blocked_pending_exact_selected_guide_chain"
        or dry.get("provider_action_authorized") is not False
        or dry.get("network_authorized") is not False
        or document.get("status") != "draft"
        or document.get("approved") is not False
        or document.get("authorized_limits", {}).get("max_calls") != 0
        or document.get("authorized_limits", {}).get("max_spend_usd") != 0
    ):
        raise ValidationError("historical V1 lineage is not exact zero authority")
    return path, document, raw, actual_sha


def _validate_selected_guide_and_run(
    root: Path,
    selected: dict[str, Any],
    plan_dry: dict[str, Any],
    approved_by: str,
    errors: list[str],
) -> tuple[bytes, dict[str, Any], Path, dict[str, Any], bytes, str, datetime | None]:
    expected_selected = {
        "state": "verified",
        "path": SELECTED_GUIDE_PATH,
        "sha256": SELECTED_GUIDE_SHA256,
        "byte_count": SELECTED_GUIDE_BYTES,
        "duration_seconds": SELECTED_GUIDE_DURATION_SECONDS,
        "container": "wav",
        "codec": "pcm_s16le",
        "sample_rate_hz": pt.GUIDE_SAMPLE_RATE_HZ,
        "channels": 1,
        "guide_request_id": SELECTED_GUIDE_REQUEST_ID,
        "guide_run_receipt_path": SELECTED_GUIDE_RUN_PATH,
        "guide_run_receipt_sha256": SELECTED_GUIDE_RUN_SHA256,
    }
    if not _exact(selected, expected_selected):
        errors.append("selected guide must be the exact unchanged G1R2 candidate B")
    selected_audio, geometry = _read_selected_wav(root, selected)
    run_path, run_receipt, run_raw, run_sha = _read_record(
        root,
        selected.get("guide_run_receipt_path"),
        selected.get("guide_run_receipt_sha256"),
        "selected candidate-B guide run receipt",
        mode=0o600,
    )
    if run_sha != SELECTED_GUIDE_RUN_SHA256:
        errors.append("selected guide run receipt is not the exact G1R2 success receipt")
    outputs = run_receipt.get("outputs")
    matching = []
    if isinstance(outputs, list):
        matching = [
            item for item in outputs
            if isinstance(item, dict)
            and item.get("request_id") == SELECTED_GUIDE_REQUEST_ID
            and item.get("path") == SELECTED_GUIDE_PATH
            and item.get("sha256") == SELECTED_GUIDE_SHA256
            and item.get("byte_count") == SELECTED_GUIDE_BYTES
            and item.get("duration_seconds") == SELECTED_GUIDE_DURATION_SECONDS
            and item.get("container") == "wav"
            and item.get("codec") == "pcm_s16le"
            and item.get("sample_rate_hz") == pt.GUIDE_SAMPLE_RATE_HZ
            and item.get("channels") == 1
            and item.get("bit_depth") == 16
        ]
    if (
        run_receipt.get("schema_version") != pt.GUIDE_RUN_RECEIPT_SCHEMA
        or run_receipt.get("provider") != pt.GUIDE_PROVIDER
        or run_receipt.get("outcome") != "success"
        or run_receipt.get("authorization_consumed") is not True
        or run_receipt.get("performance_transfer_plan_sha256") != plan_dry["plan_sha256"]
        or run_receipt.get("canonical_w_sha256") != plan_dry["canonical_w_sha256"]
        or run_receipt.get("spoken_text_sha256") != pt.MICROTEST_TEXT_SHA256
        or run_receipt.get("provider_calls_made") != 2
        or type(run_receipt.get("provider_calls_made")) is not int
        or run_receipt.get("provider_outputs_received") != 2
        or type(run_receipt.get("provider_outputs_received")) is not int
        or run_receipt.get("retries_made") != 0
        or run_receipt.get("redirects_followed") != 0
        or run_receipt.get("fallbacks_used") != 0
        or run_receipt.get("credentials_recorded") is not False
        or len(matching) != 1
    ):
        errors.append("selected candidate-B guide run receipt semantics are invalid")
    guide_completed_at = _parse_time(run_receipt.get("completed_at"), "guide run completed_at", errors)
    # Reuse the established G1 authority/consumption semantic validator.
    pt._validate_consumed_guide_authority(
        root,
        run_receipt,
        plan_dry,
        {"kind": "fixture", "id": root.name},
        approved_by,
        errors,
    )
    return selected_audio, geometry, run_path, run_receipt, run_raw, run_sha, guide_completed_at


def _normalized_transfer_request(primary: dict[str, Any]) -> tuple[str, dict[str, Any], str]:
    enable_logging = primary["query"]["enable_logging"]
    if enable_logging != "true":
        raise ValidationError("normalized Voice Changer request requires literal lowercase true")
    query_pairs = [
        ("enable_logging", enable_logging),
        ("output_format", primary["query"]["output_format"]),
    ]
    url = f"{pt.TRANSFER_ENDPOINT}?{urllib.parse.urlencode(query_pairs)}"
    value = {
        "method": "POST",
        "url": url,
        "headers": {
            "Accept": "application/octet-stream",
            "Accept-Encoding": "identity",
            "Content-Length": str(primary["multipart_body_bytes"]),
            "Content-Type": primary["content_type"],
            "credential_header_name": "xi-api-key",
        },
        "multipart_body_sha256": primary["multipart_body_sha256"],
        "multipart_body_bytes": primary["multipart_body_bytes"],
    }
    return url, value, sha256_bytes(_compact(value))


def _validate_persisted_provider_evidence(
    identifiers: Any,
    usage: Any,
    errors: list[str],
    label: str,
) -> None:
    allowed_identifiers = {"request-id", "x-request-id", "eleven-request-id"}
    if not isinstance(identifiers, dict):
        errors.append(f"{label} provider identifiers must be an object")
    else:
        for name, value in identifiers.items():
            if (
                name not in allowed_identifiers
                or not isinstance(value, str)
                or not _SAFE_HEADER_VALUE_RE.fullmatch(value)
                or pt._SECRET_VALUE_RE.search(value)
            ):
                errors.append(f"{label} provider identifiers contain an unsafe value")
                break
    allowed_usage = {
        "request-cost", "character-count", "x-ratelimit-limit",
        "x-ratelimit-remaining", "x-ratelimit-reset",
    }
    if not isinstance(usage, dict):
        errors.append(f"{label} provider usage must be an object")
    else:
        for name, value in usage.items():
            if name not in allowed_usage or type(value) is not int or not 0 <= value <= 10**15:
                errors.append(f"{label} provider usage contains an invalid value")
                break


def _validate_account_source_proof(
    source: Any,
    account_authorization_path: Path,
    account_authorization: dict[str, Any],
    account_authorization_raw: bytes,
    historical_records: tuple[tuple[Path, bytes, str], ...],
    execution_runtime_bindings: dict[str, Any],
    errors: list[str],
) -> None:
    value = _strict(
        source,
        {
            "git_head", "runtime_commit", "remote_state_checked", "git_network_called",
            "git_status_scope", "git_execution_by_descriptor",
            "git_absolute_path_identity_checked_pre_and_post", "git_path_swap_risk",
            "head_delta_policy", "head_delta_path",
        },
        "credential-account source_proof",
    )
    try:
        repository = pt._guide_repository_root()
        expected_path = account_authorization_path.relative_to(repository).as_posix()
    except (OSError, ValidationError, ValueError):
        errors.append("credential-account authorization is outside the exact repository")
        expected_path = "invalid"
    runtime_bindings = account_authorization.get("runtime_bindings")
    runtime_commit = runtime_bindings.get("git_commit") if isinstance(runtime_bindings, dict) else None
    if (
        not isinstance(value.get("git_head"), str)
        or not _GIT_SHA_RE.fullmatch(value["git_head"])
        or not isinstance(runtime_commit, str)
        or not _GIT_SHA_RE.fullmatch(runtime_commit)
        or value.get("runtime_commit") != runtime_commit
        or value.get("remote_state_checked") is not False
        or value.get("git_network_called") is not False
        or value.get("git_status_scope") != "repository_index_and_unignored_worktree_only"
        or value.get("git_execution_by_descriptor") is not False
        or value.get("git_absolute_path_identity_checked_pre_and_post") is not True
        or value.get("git_path_swap_risk")
        != "root_owned_system_binary_not_same_uid_writable"
        or value.get("head_delta_policy") != "exact_active_authorization_path_only"
        or value.get("head_delta_path") != expected_path
        or not isinstance(runtime_bindings, dict)
        or any(
            runtime_bindings.get(key) != execution_runtime_bindings.get(key)
            for key in ("git_binary_path", "git_binary_sha256", "git_version")
        )
    ):
        errors.append("credential-account source proof does not bind its exact ACTIVE authority")
        return
    source_head = value["git_head"]
    assert isinstance(runtime_commit, str)
    try:
        _verify_local_git_object_store(execution_runtime_bindings)
        _bound_git(execution_runtime_bindings, ["cat-file", "-e", f"{source_head}^{{commit}}"])
        _bound_git(execution_runtime_bindings, ["merge-base", "--is-ancestor", runtime_commit, source_head])
        current_runtime_commit = execution_runtime_bindings.get("git_commit")
        if not isinstance(current_runtime_commit, str) or not _GIT_SHA_RE.fullmatch(current_runtime_commit):
            raise ValidationError("current V2 runtime commit identity is invalid")
        _bound_git(execution_runtime_bindings, ["merge-base", "--is-ancestor", source_head, current_runtime_commit])
        delta = _bound_git(
            execution_runtime_bindings,
            [
                "diff", "--no-ext-diff", "--no-textconv", "--no-renames", "--name-only",
                "--diff-filter=ACDMRTUXB", "-z",
                f"{runtime_commit}..{source_head}",
            ]
        )
        if delta != expected_path.encode("utf-8") + b"\x00":
            raise ValidationError("historical account source delta drifted")
        if _bound_git(execution_runtime_bindings, ["show", f"{source_head}:{expected_path}"]) != account_authorization_raw:
            raise ValidationError("historical account ACTIVE bytes drifted")
        for name, (relative, _path) in _runtime_files().items():
            expected_sha = runtime_bindings.get(f"{name}_sha256")
            committed = _bound_git(execution_runtime_bindings, ["show", f"{runtime_commit}:{relative}"])
            if not isinstance(expected_sha, str) or sha256_bytes(committed) != expected_sha:
                raise ValidationError("historical account runtime binding drifted")
        for path, raw, expected_sha in historical_records:
            relative = path.relative_to(repository).as_posix()
            if sha256_bytes(raw) != expected_sha:
                raise ValidationError("historical account evidence hash drifted")
            if _bound_git(execution_runtime_bindings, ["show", f"{runtime_commit}:{relative}"]) != raw:
                raise ValidationError("historical account evidence is absent at its runtime commit")
    except (OSError, ValidationError, ValueError):
        errors.append("credential-account historical Git source proof is invalid")


def _validate_transfer_prerequisites(
    root: Path,
    prerequisites: dict[str, Any],
    authorization: dict[str, Any],
    plan_dry: dict[str, Any],
    selected_audio: bytes,
    guide_completed_at: datetime | None,
    errors: list[str],
) -> dict[str, Any]:
    selected_sha = SELECTED_GUIDE_SHA256
    approved_by = authorization["approved_by"]

    media_path, _media, media_raw, media_sha = _validate_media_contract_basis(
        root,
        prerequisites.get("official_media_contract"),
        errors,
    )

    qa_path, qa, qa_raw, qa_sha = _verified_prerequisite(root, prerequisites.get("guide_qa"), "guide_qa")
    _strict(
        qa,
        {
            "schema_version", "selected_guide_sha256", "spoken_text_sha256", "lexical_exact",
            "technical_pass", "performance_pass", "understandable_without_music_or_visuals",
            "reviewed_by", "reviewed_at",
        },
        "guide QA receipt",
    )
    if qa.get("schema_version") != "oe-synthetic-guide-qa-v1":
        errors.append("guide QA schema mismatch")
    if qa.get("selected_guide_sha256") != selected_sha or qa.get("spoken_text_sha256") != pt.MICROTEST_TEXT_SHA256:
        errors.append("guide QA does not bind exact candidate B words")
    for key in ("lexical_exact", "technical_pass", "performance_pass", "understandable_without_music_or_visuals"):
        if qa.get(key) is not True:
            errors.append(f"guide QA requires {key}=true")
    if not isinstance(qa.get("reviewed_by"), str) or not qa["reviewed_by"]:
        errors.append("guide QA reviewer is required")
    qa_at = _parse_time(qa.get("reviewed_at"), "guide QA reviewed_at", errors)

    selection_path, selection, selection_raw, selection_sha = _verified_prerequisite(
        root,
        prerequisites.get("owner_selection"),
        "owner_selection",
    )
    _strict(
        selection,
        {"schema_version", "selected_guide_sha256", "guide_qa_sha256", "selected_by", "selected_at", "approved_for_voice_transfer"},
        "owner-selection receipt",
    )
    if (
        selection.get("schema_version") != "oe-synthetic-guide-owner-selection-v1"
        or selection.get("selected_guide_sha256") != selected_sha
        or selection.get("guide_qa_sha256") != qa_sha
        or selection.get("selected_by") != approved_by
        or selection.get("approved_for_voice_transfer") is not True
    ):
        errors.append("owner selection does not approve exact candidate B for this transfer")
    selected_at = _parse_time(selection.get("selected_at"), "owner selection selected_at", errors)

    audition_path, audition, audition_raw, audition_sha = _verified_prerequisite(
        root,
        prerequisites.get("owner_audition_confirmation"),
        "owner_audition_confirmation",
    )
    _strict(
        audition,
        {
            "schema_version", "record_id", "status", "recorded_at", "finalized_at",
            "owner", "approval_basis", "selected_guide", "selected_guide_evidence",
            "target_voice", "approved_scope", "explicitly_not_authorized",
            "known_compiled_body_identity", "execution_gate",
        },
        "owner audition confirmation",
    )
    approval_basis = _strict(
        audition.get("approval_basis"),
        {
            "source", "event_order", "owner_statements", "assistant_confirmation_prompt",
            "approval_event_timestamp_available", "owner_approval_expiry_explicitly_stated",
            "record_materialization_time_is_not_claimed_as_message_time",
        },
        "owner audition approval_basis",
    )
    audition_guide = _strict(
        audition.get("selected_guide"),
        {
            "candidate_id", "guide_request_id", "provider", "path", "sha256", "byte_count",
            "duration_seconds", "container", "codec", "sample_rate_hz", "channels", "bit_depth",
            "frame_count", "original_provider_bytes_unchanged", "listening_derivative_selected",
            "spoken_text_sha256", "human_exact_word_confirmation", "confirmed_phrase",
            "twenty_twenty_two_pronunciation_confirmed", "approved_for_voice_changer_transfer",
        },
        "owner audition selected_guide",
    )
    audition_scope = _strict(
        audition.get("approved_scope"),
        {
            "cross_provider_disclosure_of_exact_guide_to_elevenlabs", "private_voice_changer_microtest",
            "method", "endpoint", "target_voice_id", "model_id", "seed", "voice_settings",
            "remove_background_noise", "file_format", "output_format", "max_provider_calls",
            "max_outputs", "max_source_bytes", "max_source_duration_seconds", "max_submitted_seconds",
            "no_retry", "no_redirect", "no_fallback", "fallback_authorized",
            "bounded_microtest_only",
        },
        "owner audition approved_scope",
    )
    denied = _strict(
        audition.get("explicitly_not_authorized"),
        {
            "account_setting_changes", "additional_provider_calls", "retry", "redirect",
            "fallback", "mp3_request", "guide_regeneration", "full_capture", "step2_lock",
            "step3", "external_sharing", "publication",
        },
        "owner audition explicitly_not_authorized",
    )
    audition_target = _strict(
        audition.get("target_voice"),
        {
            "provider", "voice_id", "voice_name", "voice_owner", "consent_owner",
            "owner_approval", "voice_changer_permitted", "original_c_provenance",
        },
        "owner audition target_voice",
    )
    known_body = _strict(
        audition.get("known_compiled_body_identity"),
        {
            "multipart_boundary", "multipart_body_bytes", "multipart_body_sha256",
            "primary_request_sha256", "primary_request_binding_state",
        },
        "owner audition known_compiled_body_identity",
    )
    execution_gate = _strict(
        audition.get("execution_gate"),
        {
            "this_record_is_an_active_provider_authorization", "credentials_may_be_accessed_from_this_record",
            "network_may_be_called_from_this_record", "runtime_execution_authority_conferred",
            "elevenlabs_improve_models_for_everyone_observed_on", "effective_training_opt_out_claimed",
            "zero_retention_mode_claimed", "data_use_prerequisite",
            "read_only_elevenlabs_readiness_observation", "required_before_execution",
        },
        "owner audition execution_gate",
    )
    expected_prompt = (
        "Before I run the private transfer, confirm that B audibly says ‘the search dashboard’ "
        "and pronounces ‘2022’ as ‘twenty twenty-two,’ then say: Approved for one private B → "
        "Original C Voice Changer test."
    )
    if (
        audition.get("schema_version") != "oe-elevenlabs-voice-transfer-owner-approval-evidence-v1"
        or audition.get("status") != "owner_approval_recorded_execution_blocked"
        or audition.get("owner") != approved_by
        or approval_basis.get("source") != "current_codex_thread_owner_messages"
        or approval_basis.get("owner_statements") != [
            "B is definitely better",
            "so we're going to use this in conjuction with my elevenlabs voice",
            "Approved",
        ]
        or approval_basis.get("assistant_confirmation_prompt") != expected_prompt
        or approval_basis.get("approval_event_timestamp_available") is not False
        or approval_basis.get("record_materialization_time_is_not_claimed_as_message_time") is not True
        or audition_guide.get("candidate_id") != "candidate-B"
        or audition_guide.get("path") != SELECTED_GUIDE_PATH
        or audition_guide.get("sha256") != selected_sha
        or audition_guide.get("byte_count") != SELECTED_GUIDE_BYTES
        or audition_guide.get("spoken_text_sha256") != pt.MICROTEST_TEXT_SHA256
        or audition_guide.get("human_exact_word_confirmation") is not True
        or audition_guide.get("confirmed_phrase") != "the search dashboard"
        or audition_guide.get("twenty_twenty_two_pronunciation_confirmed") is not True
        or audition_guide.get("approved_for_voice_changer_transfer") is not True
        or audition_scope.get("cross_provider_disclosure_of_exact_guide_to_elevenlabs") is not True
        or audition_scope.get("private_voice_changer_microtest") is not True
        or audition_scope.get("method") != "POST"
        or audition_scope.get("endpoint") != pt.TRANSFER_ENDPOINT
        or audition_scope.get("target_voice_id") != pt.TRANSFER_TARGET_VOICE_ID
        or audition_scope.get("model_id") != pt.TRANSFER_MODEL
        or audition_scope.get("seed") != pt.TRANSFER_SEED
        or not _exact(audition_scope.get("voice_settings"), pt.TRANSFER_VOICE_SETTINGS)
        or audition_scope.get("remove_background_noise") is not False
        or audition_scope.get("file_format") != "other"
        or audition_scope.get("max_provider_calls") != 1
        or audition_scope.get("max_outputs") != 1
        or audition_scope.get("max_source_bytes") != SELECTED_GUIDE_BYTES
        or audition_scope.get("max_source_duration_seconds") != SELECTED_GUIDE_DURATION_SECONDS
        or audition_scope.get("max_submitted_seconds") != SELECTED_GUIDE_DURATION_SECONDS
        or audition_scope.get("output_format") != pt.TRANSFER_PRIMARY_FORMAT
        or audition_scope.get("no_retry") is not True
        or audition_scope.get("no_redirect") is not True
        or audition_scope.get("no_fallback") is not True
        or audition_scope.get("fallback_authorized") is not False
        or audition_scope.get("bounded_microtest_only") is not True
        or any(value is not True for value in denied.values())
        or audition_target.get("provider") != "elevenlabs"
        or audition_target.get("voice_id") != pt.TRANSFER_TARGET_VOICE_ID
        or audition_target.get("voice_name") != "OE Narrator Manav C Base v1"
        or audition_target.get("voice_owner") != approved_by
        or audition_target.get("consent_owner") != approved_by
        or audition_target.get("owner_approval") is not True
        or audition_target.get("voice_changer_permitted") is not True
        or known_body.get("multipart_boundary")
        != "oe-v05-04448e9fdd50c8de67912b454e8d396f"
        or known_body.get("multipart_body_bytes") != TRANSFER_BODY_BYTES
        or known_body.get("multipart_body_sha256") != TRANSFER_BODY_SHA256
        or known_body.get("primary_request_sha256") is not None
        or known_body.get("primary_request_binding_state")
        != "pending_verified_data_use_mode_and_final_runtime"
        or execution_gate.get("this_record_is_an_active_provider_authorization") is not False
        or execution_gate.get("credentials_may_be_accessed_from_this_record") is not False
        or execution_gate.get("network_may_be_called_from_this_record") is not False
        or execution_gate.get("runtime_execution_authority_conferred") is not False
        or execution_gate.get("data_use_prerequisite") != "blocked"
    ):
        errors.append("owner audition evidence does not bind the prompt-context plus literal Approved reply")
    audition_at = _parse_time(audition.get("finalized_at"), "owner audition finalized_at", errors)

    data_path, data_use, data_raw, data_sha = _verified_prerequisite(
        root,
        prerequisites.get("elevenlabs_data_use"),
        "elevenlabs_data_use",
    )
    _strict(
        data_use,
        {
            "schema_version", "provider", "exact_guide_sha256", "cross_provider_upload_permitted",
            "improve_models_for_everyone", "zero_retention_mode", "chosen_enable_logging",
            "protection_mode", "opt_out_processed", "protection_effective_for_new_submissions",
            "zrm_eligible_and_confirmed", "account_scope_binding_sha256", "verified_by", "owner",
            "account_identity_kind", "account_identity_canonicalization",
            "account_identity_domain_separation", "api_key_preview_sha256",
            "browser_readiness_sha256", "credential_account_verification_sha256",
            "official_data_use_basis_sha256", "account_linkage_basis", "verified_at", "evidence",
        },
        "ElevenLabs data-use assurance",
    )
    if (
        data_use.get("schema_version") != "oe-elevenlabs-data-use-assurance-v1"
        or data_use.get("provider") != "elevenlabs"
        or data_use.get("exact_guide_sha256") != selected_sha
        or data_use.get("cross_provider_upload_permitted") is not True
        or data_use.get("verified_by") != "Codex"
        or data_use.get("owner") != approved_by
        or data_use.get("account_identity_kind") != ACCOUNT_IDENTITY_KIND
        or data_use.get("account_identity_canonicalization") != ACCOUNT_IDENTITY_CANONICALIZATION
        or data_use.get("account_identity_domain_separation") != USER_ID_DOMAIN_TEXT
        or data_use.get("account_linkage_basis")
        != "contextual_non_cryptographic_same_session_preview_plus_authenticated_user_get"
    ):
        errors.append("ElevenLabs data-use assurance does not authorize this exact guide/account")
    account_scope = data_use.get("account_scope_binding_sha256")
    if not isinstance(account_scope, str) or not _SHA_RE.fullmatch(account_scope):
        errors.append("ElevenLabs data-use assurance account binding is invalid")
    protection_mode = data_use.get("protection_mode")
    if protection_mode == pt.ACCOUNT_TRAINING_OPT_OUT_PROTECTION:
        expected_protection = {
            "improve_models_for_everyone": False,
            "zero_retention_mode": False,
            "chosen_enable_logging": True,
            "opt_out_processed": True,
            "protection_effective_for_new_submissions": True,
            "zrm_eligible_and_confirmed": False,
        }
    else:
        expected_protection = {}
        errors.append("V2 requires the observed processed account training opt-out")
    for key, expected in expected_protection.items():
        if data_use.get(key) is not expected:
            errors.append(f"ElevenLabs data-use protection requires {key}={str(expected).lower()}")
    verified_at = _parse_time(data_use.get("verified_at"), "data-use verified_at", errors)
    evidence_binding = _strict(data_use.get("evidence"), {"path", "sha256"}, "data-use evidence binding")
    (
        evidence_path, evidence, evidence_raw, evidence_sha, evidence_at,
        evidence_capture, evidence_official_basis,
    ) = _validate_browser_readiness(
        root,
        {"state": "verified", **evidence_binding},
        errors,
        expected_observer=approved_by,
    )
    evidence_preview_sha = evidence.get("api_key", {}).get("preview_sha256")
    if (
        data_use.get("browser_readiness_sha256") != evidence_sha
        or data_use.get("api_key_preview_sha256") != evidence_preview_sha
        or data_use.get("official_data_use_basis_sha256") != evidence_official_basis[2]
    ):
        errors.append("data-use assurance does not bind the same-session browser readiness preview")

    account_binding = _strict(
        prerequisites.get("credential_account_verification"),
        {"state", "path", "sha256"},
        "credential_account_verification",
    )
    if account_binding.get("state") != "verified":
        raise ValidationError("credential_account_verification.state must be verified")
    account_path, account_receipt, account_raw, account_sha = _read_record(
        root,
        account_binding.get("path"),
        account_binding.get("sha256"),
        "credential_account_verification",
        mode=0o600,
    )
    _strict(
        account_receipt,
        {
            "schema_version", "provider", "endpoint", "method", "scope", "outcome",
            "authorization_id", "authorization_path", "authorization_sha256",
            "consumption_record_path", "consumption_record_sha256", "source_proof",
            "owner_approval_path", "owner_approval_sha256",
            "api_key_fingerprint_sha256", "account_scope_binding_sha256", "response_bytes",
            "browser_readiness_path", "browser_readiness_sha256", "api_key_preview_sha256",
            "api_key_preview_kind", "api_key_preview_canonicalization",
            "api_key_preview_domain_separation", "api_key_preview_hash_is_non_confidential",
            "account_linkage_strength", "exact_ui_api_account_equality_claimed",
            "ui_key_preview_match",
            "account_identity_kind", "account_identity_canonicalization",
            "account_identity_domain_separation",
            "xi_api_key_echo_state", "xi_api_key_preview_echo_state",
            "response_sha256", "response_mime_type", "response_content_encoding",
            "provider_identifiers", "provider_usage",
            "provider_get_calls_made", "provider_post_calls_made", "started_at", "completed_at",
            "retries_made", "redirects_followed", "credentials_recorded", "raw_response_stored",
            "raw_api_key_stored", "raw_api_key_preview_stored", "raw_user_id_stored", "account_settings_changed",
            "voice_transfer_authorized", "full_capture_authorized", "step3_authorized",
            "publication_authorized",
        },
        "credential-account verification receipt",
    )
    if (
        account_receipt.get("schema_version") != ACCOUNT_RUN_SCHEMA
        or account_receipt.get("provider") != "elevenlabs"
        or account_receipt.get("endpoint") != ACCOUNT_ENDPOINT
        or account_receipt.get("method") != "GET"
        or account_receipt.get("scope") != ACCOUNT_SCOPE
        or account_receipt.get("outcome") != "success"
        or account_receipt.get("account_scope_binding_sha256") != account_scope
        or account_receipt.get("browser_readiness_sha256") != evidence_sha
        or account_receipt.get("api_key_preview_sha256") != evidence_preview_sha
        or account_receipt.get("api_key_preview_kind") != API_KEY_PREVIEW_KIND
        or account_receipt.get("api_key_preview_canonicalization") != API_KEY_PREVIEW_CANONICALIZATION
        or account_receipt.get("api_key_preview_domain_separation") != API_KEY_PREVIEW_DOMAIN_TEXT
        or account_receipt.get("api_key_preview_hash_is_non_confidential") is not True
        or account_receipt.get("account_linkage_strength") != "contextual_non_cryptographic"
        or account_receipt.get("exact_ui_api_account_equality_claimed") is not False
        or account_receipt.get("ui_key_preview_match") is not True
        or account_receipt.get("account_identity_kind") != ACCOUNT_IDENTITY_KIND
        or account_receipt.get("account_identity_canonicalization") != ACCOUNT_IDENTITY_CANONICALIZATION
        or account_receipt.get("account_identity_domain_separation") != USER_ID_DOMAIN_TEXT
        or account_receipt.get("xi_api_key_echo_state")
        not in {"absent_or_null", "present_exact_match"}
        or account_receipt.get("xi_api_key_preview_echo_state")
        not in {"absent_or_null", "present_last4_match"}
        or account_receipt.get("response_mime_type") != "application/json"
        or account_receipt.get("response_content_encoding") != "identity"
        or account_receipt.get("provider_get_calls_made") != 1
        or type(account_receipt.get("provider_get_calls_made")) is not int
        or account_receipt.get("provider_post_calls_made") != 0
        or type(account_receipt.get("provider_post_calls_made")) is not int
        or account_receipt.get("retries_made") != 0
        or account_receipt.get("redirects_followed") != 0
        or account_receipt.get("credentials_recorded") is not False
        or account_receipt.get("raw_response_stored") is not False
        or account_receipt.get("raw_api_key_stored") is not False
        or account_receipt.get("raw_api_key_preview_stored") is not False
        or account_receipt.get("raw_user_id_stored") is not False
        or account_receipt.get("account_settings_changed") is not False
        or account_receipt.get("voice_transfer_authorized") is not False
        or account_receipt.get("full_capture_authorized") is not False
        or account_receipt.get("step3_authorized") is not False
        or account_receipt.get("publication_authorized") is not False
    ):
        errors.append("credential-account verification receipt semantics are invalid")
    response_bytes = account_receipt.get("response_bytes")
    response_sha = account_receipt.get("response_sha256")
    if (
        type(response_bytes) is not int
        or not 0 < response_bytes <= ACCOUNT_MAX_RESPONSE_BYTES
        or not isinstance(response_sha, str)
        or not _SHA_RE.fullmatch(response_sha)
    ):
        errors.append("credential-account response evidence is not a bounded authenticated JSON response")
    _validate_persisted_provider_evidence(
        account_receipt.get("provider_identifiers"),
        account_receipt.get("provider_usage"),
        errors,
        "credential-account receipt",
    )
    key_fingerprint = account_receipt.get("api_key_fingerprint_sha256")
    if not isinstance(key_fingerprint, str) or not _SHA_RE.fullmatch(key_fingerprint):
        errors.append("credential-account receipt key fingerprint is invalid")
    if data_use.get("credential_account_verification_sha256") != account_sha:
        errors.append("data-use assurance does not bind the exact authenticated account receipt")
    account_completed_at = _parse_time(account_receipt.get("completed_at"), "account verification completed_at", errors)
    account_auth_path, account_auth, account_auth_raw, account_auth_sha = _read_record(
        root,
        account_receipt.get("authorization_path"),
        account_receipt.get("authorization_sha256"),
        "consumed account-verification authorization",
    )
    account_consumption_path, account_consumption, account_consumption_raw, account_consumption_sha = _read_record(
        root,
        account_receipt.get("consumption_record_path"),
        account_receipt.get("consumption_record_sha256"),
        "account-verification consumption record",
        mode=0o600,
    )
    account_owner_path, _account_owner, account_owner_raw, account_owner_sha = _read_record(
        root,
        account_receipt.get("owner_approval_path"),
        account_receipt.get("owner_approval_sha256"),
        "account-verification owner approval",
    )
    account_validation = validate_account_verification_authorization(account_auth_path)
    _strict(
        account_consumption,
        {
            "schema_version", "authorization_id", "authorization_path", "authorization_sha256",
            "scope", "owner_approval_path", "owner_approval_sha256",
            "browser_readiness_path", "browser_readiness_sha256", "status",
            "consumed_at", "consumed_before_credential_access",
            "credential_accessed_at_consumption", "network_called_at_consumption",
            "get_calls_used", "post_calls_used", "spend_used_usd",
        },
        "account-verification consumption record",
    )
    account_receipt_relative = account_path.relative_to(root).as_posix()
    account_authorization_relative = account_auth_path.relative_to(root).as_posix()
    evidence_relative = evidence_path.relative_to(root).as_posix()
    _validate_account_source_proof(
        account_receipt.get("source_proof"),
        account_auth_path,
        account_auth,
        account_auth_raw,
        (
            evidence_official_basis,
        ),
        authorization["runtime_bindings"],
        errors,
    )
    account_approved_at = _parse_time(
        account_auth.get("approved_at"),
        "account-verification authorization approved_at",
        errors,
    )
    account_expires_at = _parse_time(
        account_auth.get("expires_at"),
        "account-verification authorization expires_at",
        errors,
    )
    account_consumed_at = _parse_time(
        account_consumption.get("consumed_at"),
        "account-verification consumed_at",
        errors,
    )
    account_started_at = _parse_time(
        account_receipt.get("started_at"),
        "account verification started_at",
        errors,
    )
    if (
        account_validation.get("authorization_status") != "active"
        or account_validation.get("authorization_sha256") != account_auth_sha
        or account_auth_sha != account_receipt.get("authorization_sha256")
        or account_auth.get("schema_version") != ACCOUNT_AUTH_SCHEMA
        or account_auth.get("authorization_id") != account_receipt.get("authorization_id")
        or account_auth.get("status") != "active"
        or account_auth.get("approved") is not True
        or account_auth.get("approved_by") != approved_by
        or account_auth.get("credential_binding") != {
            "state": "verified",
            "mechanism": "environment_api_key",
            "api_key_environment_variable": API_KEY_ENV,
            "domain_separation": API_KEY_DOMAIN_TEXT,
        }
        or account_auth.get("owner_approval") != {
            "state": "verified",
            "path": account_owner_path.relative_to(root).as_posix(),
            "sha256": account_owner_sha,
        }
        or account_auth.get("browser_readiness") != {
            "state": "verified",
            "path": evidence_relative,
            "sha256": evidence_sha,
        }
        or account_auth.get("artifacts", {}).get("success_receipt_path") != account_receipt_relative
        or account_auth.get("consumption", {}).get("record_path")
        != account_receipt.get("consumption_record_path")
        or account_receipt.get("authorization_path") != account_authorization_relative
        or account_receipt.get("browser_readiness_path") != evidence_relative
        or account_consumption_sha != account_receipt.get("consumption_record_sha256")
        or account_consumption.get("schema_version") != ACCOUNT_CONSUMPTION_SCHEMA
        or account_consumption.get("authorization_id") != account_receipt.get("authorization_id")
        or account_consumption.get("authorization_path") != account_authorization_relative
        or account_consumption.get("authorization_sha256") != account_auth_sha
        or account_consumption.get("scope") != ACCOUNT_SCOPE
        or account_consumption.get("owner_approval_path")
        != account_owner_path.relative_to(root).as_posix()
        or account_consumption.get("owner_approval_sha256") != account_owner_sha
        or account_consumption.get("browser_readiness_path") != evidence_relative
        or account_consumption.get("browser_readiness_sha256") != evidence_sha
        or account_consumption.get("status") != "consumed_before_credential_and_network"
        or account_consumption.get("consumed_before_credential_access") is not True
        or account_consumption.get("credential_accessed_at_consumption") is not False
        or account_consumption.get("network_called_at_consumption") is not False
        or account_consumption.get("get_calls_used") != 0
        or type(account_consumption.get("get_calls_used")) is not int
        or account_consumption.get("post_calls_used") != 0
        or type(account_consumption.get("post_calls_used")) is not int
        or account_consumption.get("spend_used_usd") != 0
    ):
        errors.append("credential-account verification authority/consumption chain is invalid")
    account_times = (
        evidence_at,
        account_approved_at,
        account_consumed_at,
        account_started_at,
        account_completed_at,
        account_expires_at,
    )
    if all(item is not None for item in account_times):
        assert evidence_at is not None and account_approved_at is not None
        assert account_consumed_at is not None and account_started_at is not None
        assert account_completed_at is not None and account_expires_at is not None
        if not (
            evidence_at
            <= account_approved_at
            <= account_consumed_at
            <= account_started_at
            <= account_completed_at
            < account_expires_at
        ):
            errors.append("credential-account authorization, latch, and GET chronology is invalid")

    rights_path, rights, rights_raw, rights_sha = _verified_prerequisite(
        root,
        prerequisites.get("target_voice_rights"),
        "target_voice_rights",
    )
    _strict(
        rights,
        {
            "schema_version", "provider", "authorization_id", "performance_transfer_plan_sha256",
            "primary_request_sha256", "primary_multipart_body_sha256", "target_voice_id",
            "voice_owner", "consent_owner", "exact_guide_sha256", "owner_approval",
            "voice_changer_permitted", "approved_at", "bounded_microtest_only",
            "full_capture_permitted", "original_c_provenance",
        },
        "target voice rights receipt",
    )
    if (
        rights.get("schema_version") != "oe-elevenlabs-voice-transfer-rights-v1"
        or rights.get("provider") != "elevenlabs"
        or rights.get("authorization_id") != authorization.get("authorization_id")
        or rights.get("performance_transfer_plan_sha256") != plan_dry["plan_sha256"]
        or rights.get("target_voice_id") != pt.TRANSFER_TARGET_VOICE_ID
        or rights.get("voice_owner") != approved_by
        or rights.get("consent_owner") != approved_by
        or rights.get("exact_guide_sha256") != selected_sha
        or rights.get("owner_approval") is not True
        or rights.get("voice_changer_permitted") is not True
        or rights.get("bounded_microtest_only") is not True
        or rights.get("full_capture_permitted") is not False
    ):
        errors.append("target voice rights do not authorize this exact one private microtest")
    rights_at = _parse_time(rights.get("approved_at"), "target voice rights approved_at", errors)
    provenance = _strict(
        rights.get("original_c_provenance"),
        {"owner_selection_path", "owner_selection_sha256", "saved_voice_receipt_path", "saved_voice_receipt_sha256"},
        "Original C provenance",
    )
    blueprint_root = root.parents[2]
    prior_selection_path = pt._safe_relative(
        blueprint_root,
        provenance.get("owner_selection_path"),
        "Original C owner-selection path",
        must_exist=True,
        suffix=".json",
    )
    prior_selection_root = pt._document_root(prior_selection_path)
    prior_selection, prior_selection_raw, prior_selection_sha = pt._read_bound_fixture_json(
        prior_selection_root,
        prior_selection_path,
        "Original C owner-selection receipt",
    )
    prior_save_path = pt._safe_relative(
        blueprint_root,
        provenance.get("saved_voice_receipt_path"),
        "Original C saved-voice path",
        must_exist=True,
        suffix=".json",
    )
    prior_save_root = pt._document_root(prior_save_path)
    prior_save, prior_save_raw, prior_save_sha = pt._read_bound_fixture_json(
        prior_save_root,
        prior_save_path,
        "Original C saved-voice receipt",
    )
    if (
        prior_selection_sha != provenance.get("owner_selection_sha256")
        or prior_save_sha != provenance.get("saved_voice_receipt_sha256")
        or prior_selection.get("schema_version") != "oe-elevenlabs-voice-remix-owner-selection-v1"
        or prior_selection.get("selected_generated_voice_id") != pt.TRANSFER_TARGET_VOICE_ID
        or prior_selection.get("selected_by") != approved_by
        or prior_selection.get("owner_approved_save") is not True
        or prior_save.get("schema_version") != "oe-elevenlabs-voice-remix-save-receipt-v1"
        or prior_save.get("provider") != "elevenlabs"
        or prior_save.get("new_voice_id") != pt.TRANSFER_TARGET_VOICE_ID
        or prior_save.get("selected_generated_voice_id") != pt.TRANSFER_TARGET_VOICE_ID
        or prior_save.get("owner_selection_record_sha256") != prior_selection_sha
        or prior_save.get("new_voice_created") is not True
        or prior_save.get("source_voice_modified") is not False
        or prior_save.get("provider_calls_made") != 1
        or type(prior_save.get("provider_calls_made")) is not int
    ):
        errors.append("Original C provenance is not the exact owner-selected saved voice")

    timestamps = [
        guide_completed_at, qa_at, selected_at, audition_at, account_completed_at,
        evidence_at, verified_at, rights_at,
    ]
    if all(value is not None for value in timestamps):
        assert guide_completed_at is not None and qa_at is not None and selected_at is not None
        assert audition_at is not None and account_completed_at is not None
        assert evidence_at is not None and verified_at is not None and rights_at is not None
        if not guide_completed_at <= qa_at <= selected_at <= audition_at:
            errors.append("guide run, QA, owner selection, and owner audition chronology is invalid")
        if not evidence_at <= account_completed_at <= verified_at <= rights_at:
            errors.append("browser readiness, account verification, assurance, and rights chronology is invalid")

    return {
        "qa": (qa_path, qa_raw, qa_sha),
        "selection": (selection_path, selection_raw, selection_sha),
        "audition": (audition_path, audition_raw, audition_sha),
        "data_use": (data_path, data_raw, data_sha),
        "data_evidence": (evidence_path, evidence_raw, evidence_sha),
        "data_evidence_capture": evidence_capture,
        "official_data_use_basis": evidence_official_basis,
        "official_media_contract": (media_path, media_raw, media_sha),
        "account_receipt": (account_path, account_raw, account_sha),
        "account_authorization": (account_auth_path, account_auth_raw, account_auth_sha),
        "account_owner_approval": (account_owner_path, account_owner_raw, account_owner_sha),
        "account_consumption": (account_consumption_path, account_consumption_raw, account_consumption_sha),
        "rights": (rights_path, rights_raw, rights_sha),
        "original_c_selection": (prior_selection_path, prior_selection_raw, prior_selection_sha),
        "original_c_save": (prior_save_path, prior_save_raw, prior_save_sha),
        "enable_logging": data_use.get("chosen_enable_logging"),
        "browser_observed_at": evidence_at,
        "data_verified_at": verified_at,
        "account_verified_at": account_completed_at,
        "account_scope_binding_sha256": account_scope,
        "api_key_fingerprint_sha256": key_fingerprint,
        "rights_approved_at": rights_at,
    }


def _base_transfer_bindings(plan_dry: dict[str, Any]) -> dict[str, Any]:
    return {
        "performance_transfer_plan_sha256": plan_dry["plan_sha256"],
        "canonical_w_sha256": plan_dry["canonical_w_sha256"],
        "spoken_text_sha256": pt.MICROTEST_TEXT_SHA256,
        "selected_guide_sha256": SELECTED_GUIDE_SHA256,
        "selected_guide_byte_count": SELECTED_GUIDE_BYTES,
        "selected_guide_duration_seconds": SELECTED_GUIDE_DURATION_SECONDS,
        "guide_run_receipt_sha256": SELECTED_GUIDE_RUN_SHA256,
        "primary_multipart_body_sha256": TRANSFER_BODY_SHA256,
        "primary_multipart_body_bytes": TRANSFER_BODY_BYTES,
    }


def validate_voice_transfer_execution_authorization(
    authorization_path: Path,
    plan_path: Path,
    canonical_w_path: Path,
) -> dict[str, Any]:
    """Validate the additive PCM-only V2 authority without credentials/network."""

    authorization_path = Path(authorization_path).absolute()
    plan_path = Path(plan_path).absolute()
    canonical_w_path = Path(canonical_w_path).absolute()
    root = pt._document_root(authorization_path)
    if pt._document_root(plan_path) != root:
        raise ValidationError("V2 transfer authority must use the exact plan fixture root")
    authorization, _authorization_raw, authorization_sha = pt._read_bound_fixture_json(
        root,
        authorization_path,
        "V2 voice-transfer execution authorization",
    )
    _strict(
        authorization,
        {
            "schema_version", "authorization_id", "status", "approved", "scope", "target",
            "v1_lineage", "bindings", "prerequisites", "action", "credential_binding",
            "runtime_bindings", "authorized_limits", "artifacts", "consumption", "approved_by",
            "approved_at", "expires_at", "execution_ready", "blockers",
        },
        "V2 voice-transfer execution authorization",
    )
    errors: list[str] = []
    status = authorization.get("status")
    active = status == "active"
    if status not in {"draft", "active"}:
        errors.append("V2 transfer status must be draft or active")
    _validate_authorization_location(
        authorization_path,
        root,
        status,
        "V2 transfer authorization",
        errors,
    )
    if authorization.get("schema_version") != TRANSFER_EXEC_AUTH_SCHEMA:
        errors.append("V2 transfer authorization schema mismatch")
    if authorization.get("scope") != TRANSFER_EXEC_SCOPE:
        errors.append("V2 transfer authorization scope mismatch")
    authorization_id = authorization.get("authorization_id")
    if not isinstance(authorization_id, str) or not _SAFE_ID_RE.fullmatch(authorization_id):
        errors.append("V2 transfer authorization ID is invalid")
        authorization_id = "invalid"
    _target(authorization.get("target"), root, errors)

    plan_dry = pt.validate_performance_transfer_plan(plan_path, canonical_w_path)
    lineage_path, _lineage_document, lineage_raw, lineage_sha = _validate_lineage(
        root,
        authorization.get("v1_lineage"),
        plan_path,
        canonical_w_path,
    )
    expected_binding = _base_transfer_bindings(plan_dry)
    binding_keys = set(expected_binding)
    if active:
        binding_keys |= {
            "primary_request_sha256", "multipart_content_type", "enable_logging",
            "normalized_http_request_sha256",
        }
    bindings = _strict(authorization.get("bindings"), binding_keys, "bindings")
    for key, expected in expected_binding.items():
        if not _exact(bindings.get(key), expected):
            errors.append(f"V2 transfer bindings.{key} drifted")

    prerequisites = _strict(
        authorization.get("prerequisites"),
        {
            "selected_guide", "guide_qa", "owner_selection", "owner_audition_confirmation",
            "elevenlabs_data_use", "target_voice_rights", "credential_account_verification",
            "official_media_contract",
        },
        "prerequisites",
    )
    credential_keys = (
        {
            "state", "mechanism", "api_key_environment_variable", "domain_separation",
            "api_key_fingerprint_sha256", "account_scope_binding_sha256",
        }
        if active
        else {"state", "mechanism", "api_key_environment_variable"}
    )
    credential = _strict(authorization.get("credential_binding"), credential_keys, "credential_binding")
    expected_credential = (
        {
            "state": "verified",
            "mechanism": "verified_environment_api_key",
            "api_key_environment_variable": API_KEY_ENV,
            "domain_separation": API_KEY_DOMAIN_TEXT,
        }
        if active
        else {
            "state": "pending",
            "mechanism": "verified_environment_api_key",
            "api_key_environment_variable": API_KEY_ENV,
        }
    )
    for key, expected in expected_credential.items():
        if not _exact(credential.get(key), expected):
            errors.append(f"credential_binding.{key} drifted")
    if active:
        for key in ("api_key_fingerprint_sha256", "account_scope_binding_sha256"):
            if not isinstance(credential.get(key), str) or not _SHA_RE.fullmatch(credential[key]):
                errors.append(f"active credential binding requires {key}")

    _validate_runtime_bindings(
        authorization.get("runtime_bindings"),
        active=active,
        require_media_probe=True,
        errors=errors,
    )
    if not _exact(authorization.get("authorized_limits"), _transfer_limits(active)):
        errors.append("V2 transfer authorized limits drifted")
    if not _exact(authorization.get("artifacts"), _transfer_artifacts(authorization_id)):
        errors.append("V2 transfer artifact paths drifted")
    consumption = _strict(
        authorization.get("consumption"),
        {"status", "generation_post_calls_used", "outputs_received", "spend_used_usd", "record_path"},
        "consumption",
    )
    expected_consumption = {
        "status": "unconsumed" if active else "not_authorized",
        "generation_post_calls_used": 0,
        "outputs_received": 0,
        "spend_used_usd": 0,
        "record_path": _transfer_consumption_path(authorization_id),
    }
    if not _exact(consumption, expected_consumption):
        errors.append("V2 transfer consumption state or path drifted")
    blockers = authorization.get("blockers")
    if not isinstance(blockers, list) or any(not isinstance(item, str) or not item for item in blockers):
        errors.append("V2 transfer blockers must be non-empty strings")
    approved_at, expires_at = _parse_window(authorization, active=active, errors=errors)

    compiled: dict[str, Any] | None = None
    normalized: dict[str, Any] | None = None
    records: dict[str, Any] = {}
    enable_logging: bool | str = "pending"
    if not active:
        for name, item in prerequisites.items():
            if not _exact(item, {"state": "pending"}):
                errors.append(f"draft prerequisite {name} must remain pending")
        if not _exact(authorization.get("action"), _action_transfer("pending")):
            errors.append("draft V2 transfer action drifted")
        if authorization.get("approved") is not False or authorization.get("execution_ready") is not False:
            errors.append("draft V2 transfer cannot be approved or executable")
        if authorization.get("approved_by") != "" or authorization.get("approved_at") != "" or authorization.get("expires_at") != "":
            errors.append("draft V2 transfer approval fields must be empty")
        if not blockers:
            errors.append("draft V2 transfer must state blockers")
    else:
        approved_by = authorization.get("approved_by")
        if not isinstance(approved_by, str) or not approved_by:
            errors.append("active V2 transfer requires approved_by")
            approved_by = "invalid"
        if authorization.get("approved") is not True or authorization.get("execution_ready") is not True:
            errors.append("active V2 transfer must be approved and execution-ready")
        if blockers != []:
            errors.append("active V2 transfer may not retain blockers")
        selected = _strict(
            prerequisites.get("selected_guide"),
            {
                "state", "path", "sha256", "byte_count", "duration_seconds", "container", "codec",
                "sample_rate_hz", "channels", "guide_request_id", "guide_run_receipt_path",
                "guide_run_receipt_sha256",
            },
            "selected_guide",
        )
        selected_audio, _geometry, run_path, _run, run_raw, run_sha, guide_completed_at = (
            _validate_selected_guide_and_run(root, selected, plan_dry, approved_by, errors)
        )
        records = _validate_transfer_prerequisites(
            root,
            prerequisites,
            authorization,
            plan_dry,
            selected_audio,
            guide_completed_at,
            errors,
        )
        enable_logging = records["enable_logging"]
        if type(enable_logging) is not bool:
            errors.append("active V2 transfer requires an exact boolean logging mode")
            enable_logging = False
        compiled, body = pt._compile_multipart_bytes(
            selected_audio,
            SELECTED_GUIDE_SHA256,
            pt.TRANSFER_PRIMARY_FORMAT,
            enable_logging=enable_logging,
        )
        body_sha = sha256_bytes(body)
        primary_request_sha = sha256_bytes(_compact(compiled))
        _url, normalized, normalized_sha = _normalized_transfer_request(compiled)
        expected_active_bindings = {
            **expected_binding,
            "primary_request_sha256": primary_request_sha,
            "multipart_content_type": compiled["content_type"],
            "enable_logging": enable_logging,
            "normalized_http_request_sha256": normalized_sha,
        }
        if not _exact(bindings, expected_active_bindings):
            errors.append("active V2 transfer bindings do not match the exact compiled PCM request")
        if (
            body_sha != TRANSFER_BODY_SHA256
            or len(body) != TRANSFER_BODY_BYTES
            or compiled["multipart_body_sha256"] != TRANSFER_BODY_SHA256
            or compiled["multipart_body_bytes"] != TRANSFER_BODY_BYTES
            or primary_request_sha
            != (TRANSFER_OPT_OUT_REQUEST_SHA256 if enable_logging else TRANSFER_ZRM_REQUEST_SHA256)
        ):
            errors.append("compiled PCM multipart request identity drifted")
        if not _exact(authorization.get("action"), _action_transfer(enable_logging)):
            errors.append("active V2 transfer action drifted")
        if (
            credential.get("api_key_fingerprint_sha256") != records.get("api_key_fingerprint_sha256")
            or credential.get("account_scope_binding_sha256") != records.get("account_scope_binding_sha256")
        ):
            errors.append("active credential binding does not match the authenticated account receipt")
        rights_record = pt._strict_json_bytes(records["rights"][1], "target voice rights receipt")
        if (
            rights_record.get("primary_request_sha256") != primary_request_sha
            or rights_record.get("primary_multipart_body_sha256") != body_sha
        ):
            errors.append("target voice rights do not bind the exact compiled request/body")
        if approved_at is not None:
            for label, timestamp in (
                ("browser readiness", records.get("browser_observed_at")),
                ("account verification", records.get("account_verified_at")),
                ("data-use assurance", records.get("data_verified_at")),
                ("voice rights", records.get("rights_approved_at")),
            ):
                if timestamp is None or timestamp > approved_at:
                    errors.append(f"{label} must be complete before V2 approval")
            account_at = records.get("account_verified_at")
            browser_at = records.get("browser_observed_at")
            data_at = records.get("data_verified_at")
            if browser_at is not None and (approved_at - browser_at).total_seconds() > DATA_USE_MAX_AGE_SECONDS:
                errors.append("browser readiness is too old at V2 approval")
            if account_at is not None and (approved_at - account_at).total_seconds() > ACCOUNT_VERIFICATION_MAX_AGE_SECONDS:
                errors.append("credential-account verification is too old at approval")
            if data_at is not None and (approved_at - data_at).total_seconds() > DATA_USE_MAX_AGE_SECONDS:
                errors.append("ElevenLabs data-use evidence is too old at approval")
        # Keep exact source bytes for later committed-source proof.
        records["lineage"] = (lineage_path, lineage_raw, lineage_sha)
        records["guide_run"] = (run_path, run_raw, run_sha)
        body = b""
        selected_audio = b""

    _raise_errors(errors)
    return {
        "schema_version": "oe-voice-transfer-execution-dry-run-v2",
        "valid": True,
        "status": "active_exact_pcm_authority_validated" if active else "blocked_pending_active_v2_authorization",
        "authorization_status": status,
        "authorization_id": authorization_id,
        "authorization_sha256": authorization_sha,
        "approved_at": _iso(approved_at) if approved_at else None,
        "expires_at": _iso(expires_at) if expires_at else None,
        "v1_lineage": {
            "status": "draft_zero_authority",
            "authorization_id": V1_LINEAGE_ID,
            "sha256": lineage_sha,
        },
        "bindings": bindings,
        "action": authorization.get("action"),
        "compiled_request": compiled,
        "normalized_http_request": normalized,
        "maximum": _transfer_limits(active),
        "artifacts": _transfer_artifacts(authorization_id),
        "provider_action_authorized": active,
        "network_authorized": active,
        "execution_transport_available": active,
        "account_get_calls_authorized": 0,
        "generation_post_calls_authorized": 1 if active else 0,
        "fallback_authorized": False,
        "credentials_accessed": False,
        "network_called": False,
        "provider_calls_made": 0,
        "outputs_received": 0,
        "creative_approved": False,
        "full_capture_authorized": False,
        "step2_lock_authorized": False,
        "step3_authorized": False,
        "sharing_authorized": False,
        "publication_authorized": False,
    }


def dry_run_voice_transfer_execution(
    authorization_path: Path,
    plan_path: Path,
    canonical_w_path: Path,
) -> dict[str, Any]:
    return validate_voice_transfer_execution_authorization(
        authorization_path,
        plan_path,
        canonical_w_path,
    )


@dataclass(frozen=True)
class _AccountExecutionContract:
    root: Path
    authorization_path: Path
    authorization: dict[str, Any]
    authorization_raw: bytes
    authorization_sha256: str
    approved_at: datetime
    expires_at: datetime
    consumption_relative: str
    success_relative: str
    failure_relative: str
    owner_approval_path: Path
    owner_approval_raw: bytes
    owner_approval_sha256: str
    owner_approval_recorded_at: datetime
    browser_readiness_path: Path
    browser_readiness_raw: bytes
    browser_readiness_sha256: str
    expected_preview_sha256: str
    browser_observed_at: datetime
    browser_capture_path: Path
    browser_capture_raw: bytes
    browser_capture_sha256: str
    official_basis_path: Path
    official_basis_raw: bytes
    official_basis_sha256: str


@dataclass(frozen=True)
class _TransferExecutionContract:
    root: Path
    authorization_path: Path
    authorization: dict[str, Any]
    authorization_raw: bytes
    authorization_sha256: str
    plan_path: Path
    canonical_w_path: Path
    approved_at: datetime
    expires_at: datetime
    consumption_relative: str
    raw_relative: str
    working_relative: str
    success_relative: str
    failure_relative: str
    conversion_relative: str
    manifest: dict[str, Any]
    body: bytes
    normalized_request: dict[str, Any]
    records: dict[str, tuple[Path, bytes, str]]
    browser_observed_at: datetime
    account_verified_at: datetime
    data_verified_at: datetime


@dataclass(frozen=True)
class _ElevenResponse:
    response_bytes: int
    response_sha256: str
    content_type: str
    content_encoding: str
    payload: bytes
    provider_identifiers: dict[str, str]
    provider_usage: dict[str, int]


def _eleven_failure(
    code: str,
    *,
    response_received: bool = False,
    http_status: int | None = None,
    response_bytes: int = 0,
    response_sha256: str | None = None,
    provider_identifiers: dict[str, str] | None = None,
    provider_usage: dict[str, int] | None = None,
) -> pt._GuideExecutionFailure:
    failure = pt._GuideExecutionFailure(
        code,
        http_status=http_status,
        response_bytes=response_bytes,
        response_sha256=response_sha256,
        provider_identifiers=provider_identifiers,
        provider_usage=provider_usage,
    )
    failure.response_received = response_received
    return failure


def _execution_now() -> datetime:
    return datetime.now(timezone.utc)


def _monotonic() -> float:
    return time.monotonic()


def _build_account_contract(authorization_path: Path) -> _AccountExecutionContract:
    authorization_path = Path(authorization_path).absolute()
    validation = validate_account_verification_authorization(authorization_path)
    if validation.get("authorization_status") != "active":
        raise ValidationError("account verification execution requires exact ACTIVE authority")
    root = pt._document_root(authorization_path)
    authorization, raw, actual_sha = pt._read_bound_fixture_json(
        root,
        authorization_path,
        "active account-verification authorization",
    )
    if actual_sha != validation.get("authorization_sha256"):
        raise ValidationError("account-verification authorization changed after validation")
    errors: list[str] = []
    approved_at = _parse_time(authorization.get("approved_at"), "approved_at", errors)
    expires_at = _parse_time(authorization.get("expires_at"), "expires_at", errors)
    if errors or approved_at is None or expires_at is None:
        raise ValidationError(errors or "account-verification authorization window is invalid")
    now = _execution_now()
    if not approved_at <= now < expires_at:
        raise ValidationError("account-verification authorization is outside its active window")
    artifacts = authorization["artifacts"]
    owner_errors: list[str] = []
    owner_path, _owner_record, owner_raw, owner_sha, owner_recorded_at = _validate_account_owner_approval(
        root,
        authorization["owner_approval"],
        owner_errors,
        expected_owner=authorization["approved_by"],
    )
    _raise_errors(owner_errors)
    if owner_recorded_at is None:
        raise ValidationError("account owner approval timestamp is invalid")
    browser_errors: list[str] = []
    (
        browser_path, _browser, browser_raw, browser_sha, browser_at,
        browser_capture, official_basis,
    ) = _validate_browser_readiness(
        root,
        authorization["browser_readiness"],
        browser_errors,
        expected_observer=authorization["approved_by"],
    )
    _raise_errors(browser_errors)
    if browser_at is None:
        raise ValidationError("browser readiness timestamp is invalid")
    now = _execution_now()
    if now > browser_at + timedelta(seconds=ACCOUNT_VERIFICATION_MAX_AGE_SECONDS):
        raise ValidationError("browser readiness is stale at account execution")
    browser_document = pt._strict_json_bytes(browser_raw, "ElevenLabs browser readiness")
    expected_preview_sha = browser_document["api_key"]["preview_sha256"]
    return _AccountExecutionContract(
        root=root,
        authorization_path=authorization_path,
        authorization=authorization,
        authorization_raw=raw,
        authorization_sha256=actual_sha,
        approved_at=approved_at,
        expires_at=expires_at,
        consumption_relative=authorization["consumption"]["record_path"],
        success_relative=artifacts["success_receipt_path"],
        failure_relative=artifacts["failure_receipt_path"],
        owner_approval_path=owner_path,
        owner_approval_raw=owner_raw,
        owner_approval_sha256=owner_sha,
        owner_approval_recorded_at=owner_recorded_at,
        browser_readiness_path=browser_path,
        browser_readiness_raw=browser_raw,
        browser_readiness_sha256=browser_sha,
        expected_preview_sha256=expected_preview_sha,
        browser_observed_at=browser_at,
        browser_capture_path=browser_capture[0],
        browser_capture_raw=browser_capture[1],
        browser_capture_sha256=browser_capture[2],
        official_basis_path=official_basis[0],
        official_basis_raw=official_basis[1],
        official_basis_sha256=official_basis[2],
    )


def _build_transfer_contract(
    authorization_path: Path,
    plan_path: Path,
    canonical_w_path: Path,
    *,
    enforce_current_execution_window: bool = True,
) -> _TransferExecutionContract:
    authorization_path = Path(authorization_path).absolute()
    plan_path = Path(plan_path).absolute()
    canonical_w_path = Path(canonical_w_path).absolute()
    validation = validate_voice_transfer_execution_authorization(
        authorization_path,
        plan_path,
        canonical_w_path,
    )
    if validation.get("authorization_status") != "active":
        raise ValidationError("voice transfer execution requires exact ACTIVE V2 authority")
    root = pt._document_root(authorization_path)
    authorization, raw, actual_sha = pt._read_bound_fixture_json(
        root,
        authorization_path,
        "active V2 transfer authorization",
    )
    if actual_sha != validation.get("authorization_sha256"):
        raise ValidationError("V2 transfer authorization changed after validation")
    errors: list[str] = []
    approved_at = _parse_time(authorization.get("approved_at"), "approved_at", errors)
    expires_at = _parse_time(authorization.get("expires_at"), "expires_at", errors)
    if errors or approved_at is None or expires_at is None:
        raise ValidationError(errors or "V2 transfer authorization window is invalid")
    if enforce_current_execution_window:
        now = _execution_now()
        if not approved_at <= now < expires_at:
            raise ValidationError("V2 transfer authorization is outside its active window")
    plan_dry = pt.validate_performance_transfer_plan(plan_path, canonical_w_path)
    approved_by = authorization["approved_by"]
    selected_audio, _geometry, run_path, _run, run_raw, run_sha, guide_completed_at = (
        _validate_selected_guide_and_run(
            root,
            authorization["prerequisites"]["selected_guide"],
            plan_dry,
            approved_by,
            errors,
        )
    )
    prerequisite_records = _validate_transfer_prerequisites(
        root,
        authorization["prerequisites"],
        authorization,
        plan_dry,
        selected_audio,
        guide_completed_at,
        errors,
    )
    _raise_errors(errors)
    manifest, body = pt._compile_multipart_bytes(
        selected_audio,
        SELECTED_GUIDE_SHA256,
        pt.TRANSFER_PRIMARY_FORMAT,
        enable_logging=prerequisite_records["enable_logging"],
    )
    _url, normalized, normalized_sha = _normalized_transfer_request(manifest)
    if (
        sha256_bytes(body) != authorization["bindings"]["primary_multipart_body_sha256"]
        or len(body) != authorization["bindings"]["primary_multipart_body_bytes"]
        or sha256_bytes(_compact(manifest)) != authorization["bindings"]["primary_request_sha256"]
        or normalized_sha != authorization["bindings"]["normalized_http_request_sha256"]
    ):
        body = b""
        selected_audio = b""
        raise ValidationError("exact V2 request changed after authorization validation")
    lineage_path, _lineage, lineage_raw, lineage_sha = _validate_lineage(
        root,
        authorization["v1_lineage"],
        plan_path,
        canonical_w_path,
    )
    _plan_document, plan_raw, plan_sha = pt._read_bound_fixture_json(
        root,
        plan_path,
        "V2 bound performance-transfer plan",
    )
    canonical_raw, canonical_sha = _read_bound_blob(
        root,
        canonical_w_path,
        "V2 bound canonical W",
        max_bytes=1_000_000,
    )
    if plan_sha != plan_dry["plan_sha256"] or canonical_sha != plan_dry["canonical_w_sha256"]:
        body = b""
        selected_audio = b""
        canonical_raw = b""
        raise ValidationError("plan or canonical W changed after V2 validation")
    records: dict[str, tuple[Path, bytes, str]] = {
        name: value
        for name, value in prerequisite_records.items()
        if isinstance(value, tuple) and len(value) == 3 and isinstance(value[0], Path)
    }
    records.update(
        {
            "lineage": (lineage_path, lineage_raw, lineage_sha),
            "selected_guide": (
                root / SELECTED_GUIDE_PATH,
                selected_audio,
                SELECTED_GUIDE_SHA256,
            ),
            "guide_run": (run_path, run_raw, run_sha),
            "plan": (plan_path, plan_raw, plan_sha),
            "canonical_w": (canonical_w_path, canonical_raw, canonical_sha),
        }
    )
    artifacts = authorization["artifacts"]
    browser_at = prerequisite_records.get("browser_observed_at")
    account_at = prerequisite_records.get("account_verified_at")
    data_at = prerequisite_records.get("data_verified_at")
    if not all(isinstance(item, datetime) for item in (browser_at, account_at, data_at)):
        raise ValidationError("V2 evidence freshness timestamps are invalid")
    assert isinstance(browser_at, datetime) and isinstance(account_at, datetime) and isinstance(data_at, datetime)
    if enforce_current_execution_window:
        current = _execution_now()
        for label, timestamp in (
            ("browser readiness", browser_at),
            ("credential-account verification", account_at),
            ("data-use assurance", data_at),
        ):
            if current < timestamp or (current - timestamp).total_seconds() > DATA_USE_MAX_AGE_SECONDS:
                raise ValidationError(f"{label} is stale at V2 execution")
    return _TransferExecutionContract(
        root=root,
        authorization_path=authorization_path,
        authorization=authorization,
        authorization_raw=raw,
        authorization_sha256=actual_sha,
        plan_path=plan_path,
        canonical_w_path=canonical_w_path,
        approved_at=approved_at,
        expires_at=expires_at,
        consumption_relative=authorization["consumption"]["record_path"],
        raw_relative=artifacts["raw_output_path"],
        working_relative=artifacts["working_output_path"],
        success_relative=artifacts["success_receipt_path"],
        failure_relative=artifacts["failure_receipt_path"],
        conversion_relative=artifacts["conversion_receipt_path"],
        manifest=manifest,
        body=body,
        normalized_request=normalized,
        records=records,
        browser_observed_at=browser_at,
        account_verified_at=account_at,
        data_verified_at=data_at,
    )


def _verify_committed_source(
    contract: _AccountExecutionContract | _TransferExecutionContract,
    *,
    allow_consumption_latch: bool,
) -> dict[str, Any]:
    """Prove local committed code/public inputs and descriptor-bound private inputs."""

    repository = pt._guide_repository_root()
    bindings = contract.authorization["runtime_bindings"]
    runtime_commit = bindings["git_commit"]
    try:
        _verify_local_git_object_store(bindings)
        head = _bound_git(bindings, ["rev-parse", "HEAD"]).strip().decode("ascii", errors="strict")
    except (UnicodeError, ValidationError):
        raise ValidationError("ElevenLabs source proof could not read exact Git identities") from None
    if not _GIT_SHA_RE.fullmatch(head):
        raise ValidationError("ElevenLabs local execution HEAD is invalid")
    _bound_git(bindings, ["merge-base", "--is-ancestor", runtime_commit, head])
    try:
        authorization_relative = contract.authorization_path.relative_to(repository).as_posix()
    except ValueError:
        raise ValidationError("ElevenLabs ACTIVE authority is outside the repository") from None
    delta = _bound_git(
        bindings,
        [
            "diff", "--no-ext-diff", "--no-textconv", "--no-renames", "--name-only",
            "--diff-filter=ACDMRTUXB", "-z",
            f"{runtime_commit}..{head}",
        ]
    )
    if delta != authorization_relative.encode("utf-8") + b"\x00":
        raise ValidationError("runtime commit to HEAD delta must be exactly the ACTIVE authority path")
    if (
        _bound_git(bindings, ["show", f"HEAD:{authorization_relative}"]) != contract.authorization_raw
        or sha256_bytes(contract.authorization_raw) != contract.authorization_sha256
    ):
        raise ValidationError("ElevenLabs ACTIVE authority is not committed exactly")
    for name, (relative, path) in _runtime_files().items():
        current, current_sha = _read_bound_blob(
            repository,
            path,
            f"bound ElevenLabs runtime {name}",
            max_bytes=5_000_000,
        )
        committed = _bound_git(bindings, ["show", f"{runtime_commit}:{relative}"])
        expected_sha = bindings[f"{name}_sha256"]
        if (
            current_sha != expected_sha
            or sha256_bytes(committed) != expected_sha
            or current != committed
        ):
            raise ValidationError("bound ElevenLabs runtime is not exact at runtime commit")
    if isinstance(contract, _TransferExecutionContract):
        probe_path, probe_sha = _read_ffprobe_identity(bindings["ffprobe_binary_path"])
        if (
            probe_path != bindings["ffprobe_binary_path"]
            or probe_sha != bindings["ffprobe_binary_sha256"]
            or _read_ffprobe_version(probe_path, probe_sha) != bindings["ffprobe_version"]
        ):
            raise ValidationError("bound ffprobe media probe changed after authorization")
        ffmpeg_path, ffmpeg_sha = _read_ffmpeg_identity(bindings["ffmpeg_binary_path"])
        if (
            ffmpeg_path != bindings["ffmpeg_binary_path"]
            or ffmpeg_sha != bindings["ffmpeg_binary_sha256"]
            or _read_ffmpeg_version(ffmpeg_path, ffmpeg_sha) != bindings["ffmpeg_version"]
        ):
            raise ValidationError("bound ffmpeg conversion tool changed after authorization")
        record_names = set(contract.records)
        if record_names != TRANSFER_COMMITTED_RECORD_NAMES | TRANSFER_LOCAL_PRIVATE_RECORD_NAMES:
            raise ValidationError("V2 prerequisite privacy partition is incomplete")
        for name in sorted(TRANSFER_COMMITTED_RECORD_NAMES):
            path, raw, expected_sha = contract.records[name]
            try:
                relative = path.relative_to(repository).as_posix()
            except ValueError:
                raise ValidationError("V2 prerequisite is outside the repository") from None
            if sha256_bytes(raw) != expected_sha:
                raise ValidationError("V2 prerequisite in-memory hash drifted")
            current, current_sha = _read_bound_blob(
                repository,
                path,
                f"committed V2 prerequisite {name}",
                max_bytes=10_000_000,
            )
            if current_sha != expected_sha or current != raw:
                raise ValidationError("committed V2 prerequisite current bytes drifted")
            if _bound_git(bindings, ["show", f"{runtime_commit}:{relative}"]) != raw:
                raise ValidationError("public V2 prerequisite is not exact at runtime commit")
        for name in sorted(TRANSFER_LOCAL_PRIVATE_RECORD_NAMES):
            path, raw, expected_sha = contract.records[name]
            current, current_sha = _read_bound_blob(
                repository,
                path,
                f"local-private V2 prerequisite {name}",
                max_bytes=10_000_000,
                required_mode=0o600,
                required_uid=os.getuid(),
            )
            if current_sha != expected_sha or current != raw:
                raise ValidationError("local-private V2 prerequisite bytes drifted")
    else:
        for label, path, raw, expected_sha in (
            (
                "account owner approval",
                contract.owner_approval_path,
                contract.owner_approval_raw,
                contract.owner_approval_sha256,
            ),
            (
                "account browser readiness",
                contract.browser_readiness_path,
                contract.browser_readiness_raw,
                contract.browser_readiness_sha256,
            ),
            (
                "account browser capture",
                contract.browser_capture_path,
                contract.browser_capture_raw,
                contract.browser_capture_sha256,
            ),
        ):
            current, current_sha = _read_bound_blob(
                repository,
                path,
                label,
                max_bytes=10_000_000,
                required_mode=0o600,
                required_uid=os.getuid(),
            )
            if current_sha != expected_sha or current != raw:
                raise ValidationError(f"{label} local-private bytes drifted")
        try:
            official_relative = contract.official_basis_path.relative_to(repository).as_posix()
        except ValueError:
            raise ValidationError("official data-use basis is outside the repository") from None
        official_current, official_current_sha = _read_bound_blob(
            repository,
            contract.official_basis_path,
            "official data-use basis",
            max_bytes=1_000_000,
        )
        if (
            sha256_bytes(contract.official_basis_raw) != contract.official_basis_sha256
            or official_current_sha != contract.official_basis_sha256
            or official_current != contract.official_basis_raw
            or _bound_git(bindings, ["show", f"{runtime_commit}:{official_relative}"])
            != contract.official_basis_raw
        ):
            raise ValidationError("official data-use basis is not exact at runtime commit")
    dirty = _bound_git(bindings, ["status", "--porcelain=v1", "--untracked-files=all", "-z"])
    allowed_dirty = b""
    if allow_consumption_latch:
        latch = contract.root / contract.consumption_relative
        try:
            latch_relative = latch.relative_to(repository).as_posix()
        except ValueError:
            raise ValidationError("ElevenLabs consumption latch is outside the repository") from None
        allowed_dirty = b"?? " + latch_relative.encode("utf-8") + b"\x00"
    if dirty != allowed_dirty:
        raise ValidationError(
            "Git index and unignored worktree must be clean for ElevenLabs execution"
        )
    return {
        "git_head": head,
        "runtime_commit": runtime_commit,
        "remote_state_checked": False,
        "git_network_called": False,
        "git_status_scope": "repository_index_and_unignored_worktree_only",
        "git_execution_by_descriptor": False,
        "git_absolute_path_identity_checked_pre_and_post": True,
        "git_path_swap_risk": "root_owned_system_binary_not_same_uid_writable",
        "head_delta_policy": "exact_active_authorization_path_only",
        "head_delta_path": authorization_relative,
    }


def _preflight_account_paths(contract: _AccountExecutionContract) -> None:
    pt._ensure_execution_parents(
        contract.root,
        [contract.consumption_relative, contract.success_relative, contract.failure_relative],
    )
    for label, relative in (
        ("account-verification consumption", contract.consumption_relative),
        ("account-verification success receipt", contract.success_relative),
        ("account-verification failure receipt", contract.failure_relative),
    ):
        path = pt._safe_execution_relative(contract.root, relative, label, ".json")
        parts = path.relative_to(contract.root).parts
        if label.endswith("consumption"):
            if parts[:2] != ("authorizations", "consumed"):
                raise ValidationError("account-verification latch must remain under authorizations/consumed")
        elif parts[:2] != ("receipts", "elevenlabs-account"):
            raise ValidationError("account-verification receipt must remain under receipts/elevenlabs-account")


def _preflight_transfer_paths(contract: _TransferExecutionContract) -> None:
    relatives = [
        contract.consumption_relative,
        contract.raw_relative,
        contract.working_relative,
        contract.success_relative,
        contract.failure_relative,
        contract.conversion_relative,
    ]
    pt._ensure_execution_parents(contract.root, relatives)
    expected = (
        (contract.consumption_relative, ".json", ("authorizations", "consumed")),
        (contract.raw_relative, ".pcm", ("outputs", "raw", "elevenlabs")),
        (contract.working_relative, ".wav", ("outputs", "working", "elevenlabs")),
        (contract.success_relative, ".json", ("receipts", "elevenlabs")),
        (contract.failure_relative, ".json", ("receipts", "elevenlabs")),
        (contract.conversion_relative, ".json", ("receipts", "elevenlabs")),
    )
    for relative, suffix, prefix in expected:
        path = pt._safe_execution_relative(contract.root, relative, "V2 transfer destination", suffix)
        if path.relative_to(contract.root).parts[: len(prefix)] != prefix:
            raise ValidationError("V2 transfer destination escaped its exact artifact class")
    if len(set(relatives)) != len(relatives):
        raise ValidationError("V2 transfer destinations must be globally distinct")


def _load_elevenlabs_api_key(expected_fingerprint: str | None) -> tuple[str, str]:
    value = os.environ.get(API_KEY_ENV)
    failure: str | None = None
    fingerprint = ""
    if (
        not isinstance(value, str)
        or not value
        or value != value.strip()
        or len(value) > 512
        or any(ord(character) < 33 or ord(character) > 126 for character in value)
    ):
        failure = "private ElevenLabs API key is absent or malformed"
    else:
        fingerprint = _key_fingerprint(value)
        if expected_fingerprint is not None and fingerprint != expected_fingerprint:
            failure = "private ElevenLabs API key does not match the authorized account receipt"
    if failure is not None:
        value = None
        fingerprint = ""
        raise ValidationError(failure) from None
    assert isinstance(value, str)
    return value, fingerprint


def _safe_elevenlabs_provider_evidence(
    headers: dict[str, str],
    api_key: str,
) -> tuple[dict[str, str], dict[str, int]]:
    identifiers: dict[str, str] = {}
    for name in ("request-id", "x-request-id", "eleven-request-id"):
        value = headers.get(name)
        if (
            isinstance(value, str)
            and _SAFE_HEADER_VALUE_RE.fullmatch(value)
            and api_key not in value
            and not pt._SECRET_VALUE_RE.search(value)
        ):
            identifiers[name] = value
    usage: dict[str, int] = {}
    for name in (
        "request-cost", "character-count", "x-ratelimit-limit",
        "x-ratelimit-remaining", "x-ratelimit-reset",
    ):
        value = headers.get(name)
        if isinstance(value, str) and value.isascii() and value.isdigit():
            number = int(value)
            if 0 <= number <= 10**15:
                usage[name] = number
    return identifiers, usage


def _preflight_tls_environment() -> None:
    if "SSL_CERT_FILE" in os.environ or "SSL_CERT_DIR" in os.environ:
        raise ValidationError("unreviewed TLS trust-store override is forbidden")


def _open_elevenlabs_request(request: urllib.request.Request, timeout: float) -> Any:
    # Never route credential-bearing ElevenLabs traffic through environment or
    # system proxy configuration; the reviewed disclosure target is exact.
    if "SSL_CERT_FILE" in os.environ or "SSL_CERT_DIR" in os.environ:
        raise _eleven_failure("unreviewed_tls_trust_override_forbidden")
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.minimum_version = ssl.TLSVersion.TLSv1_2
    context.check_hostname = True
    context.verify_mode = ssl.CERT_REQUIRED
    context.keylog_filename = None
    context.load_default_certs(ssl.Purpose.SERVER_AUTH)
    context.keylog_filename = None
    opener = urllib.request.build_opener(
        urllib.request.ProxyHandler({}),
        urllib.request.HTTPSHandler(context=context),
        pt._NoRedirect(),
    )
    return opener.open(request, timeout=timeout)


_TRANSFER_WORKER_SOURCE_PATH = Path(__file__).with_name("elevenlabs_transfer_worker.py")
_TRANSFER_WORKER_READY_TIMEOUT_SECONDS = 10.0
_TRANSFER_WORKER_TERM_GRACE_SECONDS = 0.02
_TRANSFER_WORKER_REAP_TIMEOUT_SECONDS = 1.0
_TRANSFER_WORKER_SOURCE_MAX_BYTES = 1_000_000
_TRANSFER_WORKER_INTERPRETER_MAX_BYTES = 100_000_000
_TRANSFER_WORKER_ENV = {
    "LANG": "C",
    "LC_ALL": "C",
    "__CF_USER_TEXT_ENCODING": f"0x{os.getuid():X}:0x0:0x0",
}
_TRANSFER_WORKER_INTERPRETER_PATH = (
    "/Library/Developer/CommandLineTools/Library/Frameworks/"
    "Python3.framework/Versions/3.9/bin/python3.9"
)
_TRANSFER_WORKER_INTERPRETER_SHA256 = (
    "8e598855de9a6648bc670d5fe7a3a653f1fa967b74373ed7c4ca16fbc40c0de1"
)
_TRANSFER_WORKER_INTERPRETER_VERSION = (
    "3.9.6 (default, Dec  2 2025, 07:27:58) \n"
    "[Clang 17.0.0 (clang-1700.6.3.2)]"
)
_TRANSFER_WORKER_INTERPRETER_MODE = 0o755
_TRANSFER_WORKER_INTERPRETER_UID = 0
_TRANSFER_WORKER_INTERPRETER_NLINK = 1
_TRANSFER_WORKER_PROTOCOL = "oe-elevenlabs-exact-transfer-worker-v1"
_TRANSFER_WORKER_FRAME_LENGTH_STRUCT = struct.Struct("!I")
_TRANSFER_WORKER_READY_FRAME_MAX_BYTES = 4_096
_TRANSFER_WORKER_COMMAND_FRAME_MAX_BYTES = 2_048
_TRANSFER_WORKER_KEY_FRAME_MAX_BYTES = 512
_TRANSFER_WORKER_PHASE_FRAME_MAX_BYTES = 2_048
_TRANSFER_WORKER_RESULT_FRAME_MAX_BYTES = 8_192
_TRANSFER_WORKER_RESULT_BODY_MAX_BYTES = 4_800_000
_TRANSFER_WORKER_MAX_TRANSACTION_SECONDS = 300.0
_TRANSFER_WORKER_MAX_READY_AGE_SECONDS = 30.0
_TRANSFER_WORKER_EXCHANGE_MAX_BYTES = (
    3 * _TRANSFER_WORKER_FRAME_LENGTH_STRUCT.size
    + 2 * _TRANSFER_WORKER_PHASE_FRAME_MAX_BYTES
    + _TRANSFER_WORKER_RESULT_FRAME_MAX_BYTES
    + _TRANSFER_WORKER_FRAME_LENGTH_STRUCT.size
    + _TRANSFER_WORKER_RESULT_BODY_MAX_BYTES
)
_TRANSFER_WORKER_READY_KEYS = frozenset(
    {
        "body_bytes_read",
        "command_received",
        "core_hard_limit",
        "core_soft_limit",
        "credential_bytes_read",
        "environment_keys",
        "environment_sha256",
        "executed_source_sha256",
        "interpreter_mode",
        "interpreter_nlink",
        "interpreter_path",
        "interpreter_sha256",
        "interpreter_uid",
        "logical_source_path",
        "message",
        "monotonic_ns_at_ready",
        "network_called",
        "parent_pid",
        "pid",
        "process_group_id",
        "protocol",
        "python_version",
        "session_id",
    }
)
_TRANSFER_WORKER_COMMAND_KEYS = frozenset(
    {
        "action",
        "application_http_attempt_limit",
        "body_bytes",
        "body_sha256",
        "child_deadline_monotonic_ns",
        "protocol",
    }
)
_TRANSFER_WORKER_REQUEST_STARTING_PHASE_KEYS = frozenset(
    {
        "application_http_attempts",
        "message",
        "network_state",
        "phase",
        "protocol",
        "request_state",
        "response_state",
        "sequence",
    }
)
_TRANSFER_WORKER_RESPONSE_HEADERS_PHASE_KEYS = frozenset(
    {
        "application_http_attempts",
        "content_encoding_state",
        "content_length_state",
        "content_type",
        "http_status",
        "message",
        "network_state",
        "phase",
        "protocol",
        "request_state",
        "response_state",
        "sequence",
    }
)
_TRANSFER_WORKER_RESULT_KEYS = frozenset(
    {
        "application_fallbacks_used",
        "application_http_attempts",
        "application_redirects_followed",
        "application_retries_made",
        "content_encoding",
        "content_type",
        "failure_code",
        "http_status",
        "message",
        "network_stack_address_selection_state",
        "network_state",
        "outcome",
        "protocol",
        "provider_identifiers",
        "provider_usage",
        "request_state",
        "response_body_disposition",
        "response_byte_count_state",
        "response_bytes",
        "response_sha256",
        "response_state",
        "success_body_follows",
    }
)
_TRANSFER_WORKER_ALLOWED_FAILURE_CODES = frozenset(
    {
        "worker_command_invalid",
        "worker_command_trailing_data",
        "worker_deadline_invalid",
        "worker_deadline_expired_before_request",
        "worker_key_invalid",
        "worker_key_trailing_data",
        "worker_body_invalid",
        "worker_body_trailing_data",
        "compiled_request_body_binding_failed",
        "provider_post_timeout_ambiguous",
        "provider_transport_failure",
        "provider_http_failure",
        "provider_redirect_forbidden",
        "provider_response_headers_invalid",
        "provider_content_length_invalid",
        "provider_response_byte_cap_exceeded",
        "provider_response_truncated",
        "provider_response_stream_invalid",
        "provider_response_encoding_forbidden",
        "provider_response_mime_invalid",
        "provider_response_contains_credential",
        "worker_internal_failure",
    }
)
_PARENT_TRANSFER_WORKER_FAILURE_CODES = _TRANSFER_WORKER_ALLOWED_FAILURE_CODES | frozenset(
    {
        "isolated_worker_command_channel_failure",
        "isolated_worker_command_frame_invalid",
        "isolated_worker_deadline_invalid",
        "isolated_worker_exchange_contract_invalid",
        "isolated_worker_exit_failure",
        "isolated_worker_failure_result_invalid",
        "isolated_worker_key_invalid",
        "isolated_worker_not_ready",
        "isolated_worker_phase_sequence_invalid",
        "isolated_worker_protocol_failure",
        "isolated_worker_reap_failure",
        "isolated_worker_result_cap_exceeded",
        "isolated_worker_secret_echo_detected",
        "isolated_worker_success_body_invalid",
        "isolated_worker_success_result_invalid",
        "isolated_worker_terminal_result_missing",
        "provider_request_elapsed_cap_exceeded",
    }
)
_TRANSFER_WORKER_BOOTSTRAP = """\
import hashlib
import os
import sys
source_fd = int(sys.argv[1], 10)
logical_path = sys.argv[2]
expected_sha256 = sys.argv[3]
source = bytearray()
try:
    while len(source) <= 1000000:
        chunk = os.read(source_fd, min(65536, 1000001 - len(source)))
        if not chunk:
            break
        source.extend(chunk)
finally:
    os.close(source_fd)
if not source or len(source) > 1000000:
    raise SystemExit(126)
actual_sha256 = hashlib.sha256(source).hexdigest()
if actual_sha256 != expected_sha256:
    raise SystemExit(126)
code = compile(bytes(source), logical_path, "exec", dont_inherit=True)
for index in range(len(source)):
    source[index] = 0
source = bytearray()
sys.argv = [logical_path, *sys.argv[4:]]
namespace = {
    "__name__": "__main__",
    "__file__": logical_path,
    "__package__": None,
    "__spec__": None,
    "__cached__": None,
    "__OE_EXECUTED_SOURCE_SHA256__": actual_sha256,
    "__OE_LOGICAL_SOURCE_PATH__": logical_path,
}
exec(code, namespace, namespace)
"""


@dataclass(repr=False)
class _PreparedVoiceTransferWorker:
    process: subprocess.Popen[bytes] | None
    command_fd: int
    result_fd: int
    key_fd: int
    body_fd: int
    worker_source_path: str
    worker_source_sha256: str
    interpreter_path: str
    interpreter_sha256: str
    python_version: str
    interpreter_identity: tuple[int, int, int, int, int, int, int, int]
    pid: int
    process_group_id: int
    child_monotonic_ns_at_ready: int = 0
    parent_ready_received_ns: int = 0
    state: str = "ready"


def _read_exact_regular_file_identity(
    path: Path,
    *,
    cap: int,
    require_current_uid: bool,
    require_executable: bool,
    label: str,
) -> tuple[str, str]:
    """Hash exact resolved descriptor bytes without following a final symlink."""

    try:
        resolved = path.resolve(strict=True)
    except (OSError, RuntimeError):
        raise ValidationError(f"{label} exact path is unavailable") from None
    flags = os.O_RDONLY
    if hasattr(os, "O_CLOEXEC"):
        flags |= os.O_CLOEXEC
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    descriptor = -1
    chunks: list[bytes] = []
    try:
        descriptor = os.open(resolved, flags)
        before = os.fstat(descriptor)
        if (
            not stat.S_ISREG(before.st_mode)
            or before.st_nlink != 1
            or before.st_size < 1
            or before.st_size > cap
            or (require_current_uid and before.st_uid != os.getuid())
            or (require_executable and before.st_mode & 0o111 == 0)
            or before.st_mode & 0o022 != 0
        ):
            raise ValidationError(f"{label} descriptor shape is unsafe")
        remaining = cap + 1
        while remaining > 0:
            chunk = os.read(descriptor, min(65_536, remaining))
            if not chunk:
                break
            chunks.append(chunk)
            remaining -= len(chunk)
        raw = b"".join(chunks)
        after = os.fstat(descriptor)
        if (
            len(raw) != before.st_size
            or len(raw) > cap
            or (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns)
            != (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns)
        ):
            raise ValidationError(f"{label} changed during descriptor read")
        return str(resolved), sha256_bytes(raw)
    except ValidationError:
        raise
    except (OSError, ValueError):
        raise ValidationError(f"{label} descriptor read failed") from None
    finally:
        chunks = []
        if descriptor >= 0:
            try:
                os.close(descriptor)
            except OSError:
                pass


def _open_bound_transfer_worker_source() -> tuple[int, str, str]:
    """Open, hash, rewind, and retain the exact worker descriptor for exec."""

    try:
        resolved = _TRANSFER_WORKER_SOURCE_PATH.resolve(strict=True)
    except (OSError, RuntimeError):
        raise ValidationError("isolated transfer worker exact path is unavailable") from None
    flags = os.O_RDONLY
    if hasattr(os, "O_CLOEXEC"):
        flags |= os.O_CLOEXEC
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    descriptor = -1
    chunks: list[bytes] = []
    try:
        descriptor = os.open(resolved, flags)
        before = os.fstat(descriptor)
        if (
            not stat.S_ISREG(before.st_mode)
            or before.st_nlink != 1
            or before.st_uid != os.getuid()
            or before.st_size < 1
            or before.st_size > _TRANSFER_WORKER_SOURCE_MAX_BYTES
            or before.st_mode & 0o022 != 0
        ):
            raise ValidationError("isolated transfer worker descriptor shape is unsafe")
        remaining = _TRANSFER_WORKER_SOURCE_MAX_BYTES + 1
        while remaining > 0:
            chunk = os.read(descriptor, min(65_536, remaining))
            if not chunk:
                break
            chunks.append(chunk)
            remaining -= len(chunk)
        raw = b"".join(chunks)
        after = os.fstat(descriptor)
        if (
            len(raw) != before.st_size
            or len(raw) > _TRANSFER_WORKER_SOURCE_MAX_BYTES
            or (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns)
            != (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns)
        ):
            raise ValidationError("isolated transfer worker changed during descriptor read")
        os.lseek(descriptor, 0, os.SEEK_SET)
        return descriptor, str(resolved), sha256_bytes(raw)
    except ValidationError:
        if descriptor >= 0:
            _close_transfer_worker_fd(descriptor)
        raise
    except (OSError, ValueError):
        if descriptor >= 0:
            _close_transfer_worker_fd(descriptor)
        raise ValidationError("isolated transfer worker descriptor read failed") from None
    finally:
        chunks = []


def _system_transfer_worker_interpreter_identity(
) -> tuple[str, str, str, tuple[int, int, int, int, int, int, int, int]]:
    """Bind the root-owned system interpreter and every path ancestor."""

    path = Path(_TRANSFER_WORKER_INTERPRETER_PATH)
    try:
        if str(path.resolve(strict=True)) != _TRANSFER_WORKER_INTERPRETER_PATH:
            raise ValidationError("isolated transfer worker interpreter path is indirect")
        for ancestor in reversed(path.parents):
            info = os.stat(ancestor, follow_symlinks=False)
            if (
                not stat.S_ISDIR(info.st_mode)
                or info.st_uid != 0
                or info.st_gid != 0
                or info.st_mode & 0o022 != 0
            ):
                raise ValidationError("isolated transfer worker interpreter ancestry is unsafe")
        flags = os.O_RDONLY
        if hasattr(os, "O_CLOEXEC"):
            flags |= os.O_CLOEXEC
        if hasattr(os, "O_NOFOLLOW"):
            flags |= os.O_NOFOLLOW
        descriptor = os.open(path, flags)
    except ValidationError:
        raise
    except (OSError, RuntimeError):
        raise ValidationError("isolated transfer worker interpreter is unavailable") from None
    chunks: list[bytes] = []
    try:
        before = os.fstat(descriptor)
        if (
            not stat.S_ISREG(before.st_mode)
            or stat.S_IMODE(before.st_mode) != _TRANSFER_WORKER_INTERPRETER_MODE
            or before.st_uid != _TRANSFER_WORKER_INTERPRETER_UID
            or before.st_gid != 0
            or before.st_nlink != _TRANSFER_WORKER_INTERPRETER_NLINK
            or before.st_size < 1
            or before.st_size > _TRANSFER_WORKER_INTERPRETER_MAX_BYTES
        ):
            raise ValidationError("isolated transfer worker interpreter identity is unsafe")
        remaining = _TRANSFER_WORKER_INTERPRETER_MAX_BYTES + 1
        while remaining > 0:
            chunk = os.read(descriptor, min(65_536, remaining))
            if not chunk:
                break
            chunks.append(chunk)
            remaining -= len(chunk)
        raw = b"".join(chunks)
        after = os.fstat(descriptor)
        identity = (
            before.st_dev,
            before.st_ino,
            before.st_size,
            before.st_mtime_ns,
            before.st_mode,
            before.st_uid,
            before.st_gid,
            before.st_nlink,
        )
        if (
            len(raw) != before.st_size
            or len(raw) > _TRANSFER_WORKER_INTERPRETER_MAX_BYTES
            or sha256_bytes(raw) != _TRANSFER_WORKER_INTERPRETER_SHA256
            or identity
            != (
                after.st_dev,
                after.st_ino,
                after.st_size,
                after.st_mtime_ns,
                after.st_mode,
                after.st_uid,
                after.st_gid,
                after.st_nlink,
            )
        ):
            raise ValidationError("isolated transfer worker interpreter bytes changed")
        return (
            _TRANSFER_WORKER_INTERPRETER_PATH,
            _TRANSFER_WORKER_INTERPRETER_SHA256,
            _TRANSFER_WORKER_INTERPRETER_VERSION,
            identity,
        )
    except ValidationError:
        raise
    except OSError:
        raise ValidationError("isolated transfer worker interpreter read failed") from None
    finally:
        chunks = []
        os.close(descriptor)


def _close_transfer_worker_fd(descriptor: int) -> None:
    if descriptor < 0:
        return
    try:
        os.close(descriptor)
    except OSError:
        pass


def _signal_transfer_worker_group(
    process: subprocess.Popen[bytes],
    process_group_id: int,
    signum: int,
) -> None:
    """Signal the spawn-time verified group even if its leader already exited."""

    try:
        if process_group_id == process.pid and process_group_id > 1:
            os.killpg(process_group_id, signum)
        elif process.poll() is None:
            os.kill(process.pid, signum)
    except (OSError, ProcessLookupError):
        pass


def _kill_and_reap_transfer_worker(
    process: subprocess.Popen[bytes] | None,
    *,
    process_group_id: int | None = None,
    immediate: bool = False,
) -> bool:
    """Terminate the whole isolated process group and bound every wait."""

    if process is None:
        return True
    stored_group = process.pid if process_group_id is None else process_group_id
    if process.poll() is None and immediate:
        _signal_transfer_worker_group(process, stored_group, signal.SIGKILL)
    elif immediate:
        _signal_transfer_worker_group(process, stored_group, signal.SIGKILL)
    elif process.poll() is None:
        _signal_transfer_worker_group(process, stored_group, signal.SIGTERM)
        try:
            process.wait(timeout=_TRANSFER_WORKER_TERM_GRACE_SECONDS)
        except subprocess.TimeoutExpired:
            pass
        # TERM is only a courtesy before GO.  Always follow with a group KILL
        # so a descendant cannot survive a quickly exiting leader.
        _signal_transfer_worker_group(process, stored_group, signal.SIGKILL)
    else:
        _signal_transfer_worker_group(process, stored_group, signal.SIGKILL)
    try:
        process.wait(timeout=_TRANSFER_WORKER_REAP_TIMEOUT_SECONDS)
    except subprocess.TimeoutExpired:
        _signal_transfer_worker_group(process, stored_group, signal.SIGKILL)
        try:
            process.wait(timeout=_TRANSFER_WORKER_REAP_TIMEOUT_SECONDS)
        except subprocess.TimeoutExpired:
            return False
    return process.poll() is not None


def _dispose_prepared_transfer_worker(worker: _PreparedVoiceTransferWorker) -> bool:
    for name in ("command_fd", "result_fd", "key_fd", "body_fd"):
        descriptor = getattr(worker, name)
        _close_transfer_worker_fd(descriptor)
        setattr(worker, name, -1)
    reaped = _kill_and_reap_transfer_worker(
        worker.process,
        process_group_id=worker.process_group_id,
        immediate=worker.state == "go_consumed",
    )
    if reaped:
        worker.process = None
        worker.state = "closed"
    return reaped


def _post_go_worker_failure(
    code: str,
    *,
    response_state: str = "unknown",
    http_status: int | None = None,
    response_bytes: int = 0,
    response_sha256: str | None = None,
    provider_identifiers: dict[str, str] | None = None,
    provider_usage: dict[str, int] | None = None,
) -> pt._GuideExecutionFailure:
    """Build a conservative, permanently nonretryable post-GO failure."""

    failure = _eleven_failure(
        code,
        response_received=response_state == "confirmed",
        http_status=http_status,
        response_bytes=response_bytes,
        response_sha256=response_sha256,
        provider_identifiers=provider_identifiers,
        provider_usage=provider_usage,
    )
    failure.post_budget_consumed = True
    failure.provider_request_state = (
        "confirmed_started" if response_state == "confirmed" else "unknown_after_go"
    )
    failure.provider_response_state = response_state
    failure.provider_mutation_state = "potentially_ambiguous"
    failure.provider_output_state = "potentially_ambiguous"
    failure.retry_or_replay_permitted = False
    failure.application_http_attempt_limit = 1
    return failure


def _pre_go_worker_failure(code: str) -> pt._GuideExecutionFailure:
    failure = _eleven_failure(code, response_received=False)
    failure.post_budget_consumed = False
    failure.provider_request_state = "not_started"
    failure.provider_response_state = "none"
    failure.provider_mutation_state = "none"
    failure.provider_output_state = "none"
    failure.retry_or_replay_permitted = False
    failure.application_http_attempt_limit = 1
    return failure


def _worker_reap_failure(
    primary: pt._GuideExecutionFailure,
) -> pt._GuideExecutionFailure:
    failure = _post_go_worker_failure(
        "isolated_worker_reap_failure",
        response_state=(
            "confirmed" if getattr(primary, "response_received", False) else "unknown"
        ),
        http_status=primary.http_status,
        response_bytes=primary.response_bytes,
        response_sha256=primary.response_sha256,
        provider_identifiers=dict(primary.provider_identifiers),
        provider_usage=dict(primary.provider_usage),
    )
    failure.primary_failure_code = primary.code
    failure.provider_request_state = getattr(
        primary,
        "provider_request_state",
        "unknown_after_go",
    )
    failure.provider_response_state = getattr(
        primary,
        "provider_response_state",
        "unknown",
    )
    failure.application_http_attempts = getattr(
        primary,
        "application_http_attempts",
        0,
    )
    failure.child_containment_state = "sigkill_sent_reap_unconfirmed"
    return failure


def _canonical_worker_json(document: dict[str, Any]) -> bytes:
    return json.dumps(
        document,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    ).encode("ascii")


def _decode_strict_worker_json(
    payload: bytes | bytearray | memoryview,
    cap: int,
    label: str,
) -> dict[str, Any]:
    if not payload or len(payload) > cap:
        raise ValidationError(f"{label} frame length is invalid")

    def reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for name, value in pairs:
            if not isinstance(name, str) or name in result:
                raise ValueError("duplicate or non-string JSON key")
            result[name] = value
        return result

    def reject_constant(_value: str) -> None:
        raise ValueError("non-finite JSON number")

    try:
        payload_bytes = bytes(payload)
        document = json.loads(
            payload_bytes.decode("ascii"),
            object_pairs_hook=reject_duplicates,
            parse_constant=reject_constant,
        )
    except (UnicodeError, ValueError, TypeError):
        raise ValidationError(f"{label} frame JSON is invalid") from None
    if (
        not isinstance(document, dict)
        or _canonical_worker_json(document) != payload_bytes
    ):
        raise ValidationError(f"{label} frame is not exact canonical JSON")
    return document


def _complete_transfer_worker_frames(
    raw: bytes | bytearray,
    *,
    max_frames: int = 4,
) -> tuple[list[memoryview], bool]:
    frames: list[memoryview] = []
    view = memoryview(raw)
    offset = 0
    while len(frames) < max_frames:
        if len(raw) - offset < _TRANSFER_WORKER_FRAME_LENGTH_STRUCT.size:
            return frames, offset == len(raw)
        size = _TRANSFER_WORKER_FRAME_LENGTH_STRUCT.unpack(
            view[offset : offset + _TRANSFER_WORKER_FRAME_LENGTH_STRUCT.size]
        )[0]
        if size < 1 or size > _TRANSFER_WORKER_RESULT_BODY_MAX_BYTES:
            return frames, False
        end = offset + _TRANSFER_WORKER_FRAME_LENGTH_STRUCT.size + size
        if end > len(raw):
            return frames, False
        frames.append(view[offset + _TRANSFER_WORKER_FRAME_LENGTH_STRUCT.size : end])
        offset = end
        if offset == len(raw):
            return frames, True
    return frames, offset == len(raw)


def _request_starting_phase_valid(document: dict[str, Any]) -> bool:
    return (
        set(document) == _TRANSFER_WORKER_REQUEST_STARTING_PHASE_KEYS
        and document.get("protocol") == _TRANSFER_WORKER_PROTOCOL
        and document.get("message") == "phase"
        and document.get("phase") == "request_starting"
        and document.get("sequence") == 1
        and type(document.get("sequence")) is int
        and document.get("application_http_attempts") == 1
        and type(document.get("application_http_attempts")) is int
        and document.get("network_state") == "application_request_starting"
        and document.get("request_state") == "outcome_unknown"
        and document.get("response_state") == "none"
    )


def _response_headers_phase_valid(document: dict[str, Any]) -> bool:
    content_type = document.get("content_type")
    return (
        set(document) == _TRANSFER_WORKER_RESPONSE_HEADERS_PHASE_KEYS
        and document.get("protocol") == _TRANSFER_WORKER_PROTOCOL
        and document.get("message") == "phase"
        and document.get("phase") == "response_headers_confirmed"
        and document.get("sequence") == 2
        and type(document.get("sequence")) is int
        and document.get("application_http_attempts") == 1
        and type(document.get("application_http_attempts")) is int
        and document.get("network_state") == "application_request_started"
        and document.get("request_state") == "response_confirmed"
        and document.get("response_state") == "headers_confirmed"
        and (
            document.get("http_status") is None
            or (
                type(document.get("http_status")) is int
                and 100 <= document["http_status"] <= 599
            )
        )
        and document.get("content_encoding_state")
        in {"identity", "forbidden"}
        and document.get("content_length_state")
        in {"absent", "valid_within_cap", "invalid", "over_cap"}
        and (
            content_type is None
            or (
                isinstance(content_type, str)
                and len(content_type) <= 127
                and content_type.isascii()
                and not pt._SECRET_VALUE_RE.search(content_type)
            )
        )
    )


def _apply_partial_worker_phase_evidence(
    failure: pt._GuideExecutionFailure,
    raw: bytes | bytearray,
) -> None:
    frames, _complete = _complete_transfer_worker_frames(raw, max_frames=2)
    try:
        if not frames:
            return
        try:
            first = _decode_strict_worker_json(
                frames[0],
                _TRANSFER_WORKER_PHASE_FRAME_MAX_BYTES,
                "isolated transfer worker phase",
            )
        except ValidationError:
            return
        if not _request_starting_phase_valid(first):
            return
        failure.provider_request_state = "outcome_unknown"
        failure.application_http_attempts = 1
        if len(frames) < 2:
            return
        try:
            second = _decode_strict_worker_json(
                frames[1],
                _TRANSFER_WORKER_PHASE_FRAME_MAX_BYTES,
                "isolated transfer worker phase",
            )
        except ValidationError:
            return
        if _response_headers_phase_valid(second):
            failure.provider_request_state = "response_confirmed"
            failure.provider_response_state = "headers_confirmed"
            failure.response_received = True
            failure.http_status = second["http_status"]
    finally:
        for frame in frames:
            frame.release()


def _read_preflight_worker_frame(
    process: subprocess.Popen[bytes],
    descriptor: int,
    *,
    cap: int,
    deadline_ns: int,
) -> bytes:
    buffer = bytearray()
    expected_size: int | None = None
    selector = selectors.DefaultSelector()
    try:
        os.set_blocking(descriptor, False)
        selector.register(descriptor, selectors.EVENT_READ)
        while True:
            if process.poll() is not None:
                raise ValidationError("isolated transfer worker exited before READY")
            remaining_ns = deadline_ns - time.monotonic_ns()
            if remaining_ns <= 0:
                raise ValidationError("isolated transfer worker READY deadline expired")
            events = selector.select(min(remaining_ns / 1_000_000_000, 0.05))
            if not events:
                continue
            try:
                chunk = os.read(
                    descriptor,
                    min(
                        65_536,
                        _TRANSFER_WORKER_FRAME_LENGTH_STRUCT.size + cap + 1 - len(buffer),
                    ),
                )
            except BlockingIOError:
                continue
            except OSError:
                raise ValidationError("isolated transfer worker READY pipe failed") from None
            if not chunk:
                raise ValidationError("isolated transfer worker closed before READY")
            buffer.extend(chunk)
            if expected_size is None and len(buffer) >= _TRANSFER_WORKER_FRAME_LENGTH_STRUCT.size:
                expected_size = _TRANSFER_WORKER_FRAME_LENGTH_STRUCT.unpack(
                    buffer[: _TRANSFER_WORKER_FRAME_LENGTH_STRUCT.size]
                )[0]
                if expected_size < 1 or expected_size > cap:
                    raise ValidationError("isolated transfer worker READY frame length is invalid")
            if expected_size is not None:
                total = _TRANSFER_WORKER_FRAME_LENGTH_STRUCT.size + expected_size
                if len(buffer) > total:
                    raise ValidationError("isolated transfer worker sent pre-GO trailing data")
                if len(buffer) == total:
                    if process.poll() is not None:
                        raise ValidationError("isolated transfer worker was not waiting after READY")
                    return bytes(buffer[_TRANSFER_WORKER_FRAME_LENGTH_STRUCT.size :])
    finally:
        selector.close()
        buffer = bytearray()


def _validate_transfer_worker_ready(
    worker: _PreparedVoiceTransferWorker,
    ready: dict[str, Any],
) -> None:
    try:
        interpreter_info = os.stat(worker.interpreter_path, follow_symlinks=False)
        live_process_group = os.getpgid(worker.pid)
        live_session = os.getsid(worker.pid)
    except (OSError, ProcessLookupError):
        raise ValidationError("isolated transfer worker READY identity is unavailable") from None
    if (
        set(ready) != _TRANSFER_WORKER_READY_KEYS
        or ready.get("protocol") != _TRANSFER_WORKER_PROTOCOL
        or ready.get("message") != "ready"
        or ready.get("command_received") is not False
        or ready.get("core_soft_limit") != 0
        or type(ready.get("core_soft_limit")) is not int
        or ready.get("core_hard_limit") != 0
        or type(ready.get("core_hard_limit")) is not int
        or ready.get("environment_keys") != sorted(_TRANSFER_WORKER_ENV)
        or ready.get("environment_sha256")
        != sha256_bytes(_canonical_worker_json(dict(_TRANSFER_WORKER_ENV)))
        or type(ready.get("monotonic_ns_at_ready")) is not int
        or ready.get("monotonic_ns_at_ready") <= 0
        or ready.get("credential_bytes_read") != 0
        or type(ready.get("credential_bytes_read")) is not int
        or ready.get("body_bytes_read") != 0
        or type(ready.get("body_bytes_read")) is not int
        or ready.get("network_called") is not False
        or ready.get("executed_source_sha256") != worker.worker_source_sha256
        or ready.get("logical_source_path") != worker.worker_source_path
        or ready.get("interpreter_path") != worker.interpreter_path
        or ready.get("interpreter_sha256") != worker.interpreter_sha256
        or ready.get("python_version") != worker.python_version
        or ready.get("interpreter_mode") != stat.S_IMODE(interpreter_info.st_mode)
        or type(ready.get("interpreter_mode")) is not int
        or ready.get("interpreter_uid") != interpreter_info.st_uid
        or type(ready.get("interpreter_uid")) is not int
        or ready.get("interpreter_nlink") != interpreter_info.st_nlink
        or type(ready.get("interpreter_nlink")) is not int
        or ready.get("pid") != worker.pid
        or type(ready.get("pid")) is not int
        or ready.get("parent_pid") != os.getpid()
        or type(ready.get("parent_pid")) is not int
        or ready.get("process_group_id") != worker.process_group_id
        or type(ready.get("process_group_id")) is not int
        or ready.get("session_id") != worker.pid
        or type(ready.get("session_id")) is not int
        or live_process_group != worker.pid
        or live_session != worker.pid
        or worker.process is None
        or worker.process.poll() is not None
    ):
        raise ValidationError("isolated transfer worker READY evidence is invalid")


def _prepare_voice_transfer_worker(
    *,
    ready_timeout: float = _TRANSFER_WORKER_READY_TIMEOUT_SECONDS,
) -> _PreparedVoiceTransferWorker:
    """Spawn a credential-free exact worker and require READY before any latch."""

    if type(ready_timeout) not in {int, float} or not 0 < float(ready_timeout) <= 30.0:
        raise ValidationError("isolated transfer worker READY timeout is invalid")
    source_fd = -1
    child_command_fd = -1
    parent_command_fd = -1
    child_key_fd = -1
    parent_key_fd = -1
    child_body_fd = -1
    parent_body_fd = -1
    parent_result_fd = -1
    child_result_fd = -1
    process: subprocess.Popen[bytes] | None = None
    prepared: _PreparedVoiceTransferWorker | None = None
    try:
        source_fd, source_path, source_sha256 = _open_bound_transfer_worker_source()
        (
            interpreter_path,
            interpreter_sha256,
            interpreter_version,
            interpreter_identity,
        ) = _system_transfer_worker_interpreter_identity()
        child_command_fd, parent_command_fd = os.pipe()
        child_key_fd, parent_key_fd = os.pipe()
        child_body_fd, parent_body_fd = os.pipe()
        parent_result_fd, child_result_fd = os.pipe()
        inherited = (
            source_fd,
            child_command_fd,
            child_key_fd,
            child_body_fd,
            child_result_fd,
        )
        if len(set(inherited)) != len(inherited):
            raise ValidationError("isolated transfer worker descriptor set is not distinct")
        arguments = [
            interpreter_path,
            "-I",
            "-S",
            "-B",
            "-c",
            _TRANSFER_WORKER_BOOTSTRAP,
            str(source_fd),
            source_path,
            source_sha256,
            "--command-fd",
            str(child_command_fd),
            "--key-fd",
            str(child_key_fd),
            "--body-fd",
            str(child_body_fd),
            "--result-fd",
            str(child_result_fd),
        ]
        process = subprocess.Popen(
            arguments,
            executable=interpreter_path,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            close_fds=True,
            pass_fds=inherited,
            cwd="/",
            env=dict(_TRANSFER_WORKER_ENV),
            start_new_session=True,
            restore_signals=True,
            text=False,
            umask=0o077,
        )
        for descriptor in (
            source_fd,
            child_command_fd,
            child_key_fd,
            child_body_fd,
            child_result_fd,
        ):
            _close_transfer_worker_fd(descriptor)
        source_fd = -1
        child_command_fd = -1
        child_key_fd = -1
        child_body_fd = -1
        child_result_fd = -1
        try:
            process_group_id = os.getpgid(process.pid)
            session_id = os.getsid(process.pid)
        except (OSError, ProcessLookupError):
            raise ValidationError("isolated transfer worker session could not be verified") from None
        if process_group_id != process.pid or session_id != process.pid:
            raise ValidationError("isolated transfer worker does not own its process group")
        prepared = _PreparedVoiceTransferWorker(
            process=process,
            command_fd=parent_command_fd,
            result_fd=parent_result_fd,
            key_fd=parent_key_fd,
            body_fd=parent_body_fd,
            worker_source_path=source_path,
            worker_source_sha256=source_sha256,
            interpreter_path=interpreter_path,
            interpreter_sha256=interpreter_sha256,
            python_version=interpreter_version,
            interpreter_identity=interpreter_identity,
            pid=process.pid,
            process_group_id=process_group_id,
        )
        parent_command_fd = -1
        parent_result_fd = -1
        parent_key_fd = -1
        parent_body_fd = -1
        ready_deadline_ns = time.monotonic_ns() + int(float(ready_timeout) * 1e9)
        ready_payload = _read_preflight_worker_frame(
            process,
            prepared.result_fd,
            cap=_TRANSFER_WORKER_READY_FRAME_MAX_BYTES,
            deadline_ns=ready_deadline_ns,
        )
        parent_ready_received_ns = time.monotonic_ns()
        ready = _decode_strict_worker_json(
            ready_payload,
            _TRANSFER_WORKER_READY_FRAME_MAX_BYTES,
            "isolated transfer worker READY",
        )
        _validate_transfer_worker_ready(prepared, ready)
        prepared.child_monotonic_ns_at_ready = ready["monotonic_ns_at_ready"]
        prepared.parent_ready_received_ns = parent_ready_received_ns
        current_source_path, current_source_sha = _read_exact_regular_file_identity(
            Path(source_path),
            cap=_TRANSFER_WORKER_SOURCE_MAX_BYTES,
            require_current_uid=True,
            require_executable=False,
            label="isolated transfer worker source",
        )
        (
            current_interpreter_path,
            current_interpreter_sha,
            current_interpreter_version,
            current_interpreter_identity,
        ) = _system_transfer_worker_interpreter_identity(
        )
        if (
            current_source_path != source_path
            or current_source_sha != source_sha256
            or current_interpreter_path != interpreter_path
            or current_interpreter_sha != interpreter_sha256
            or current_interpreter_version != interpreter_version
            or current_interpreter_identity != interpreter_identity
        ):
            raise ValidationError("isolated transfer worker source changed before READY")
        return prepared
    except ValidationError:
        if prepared is not None:
            _dispose_prepared_transfer_worker(prepared)
            prepared = None
            process = None
        else:
            _kill_and_reap_transfer_worker(
                process,
                process_group_id=process.pid if process is not None else None,
            )
        raise
    except BaseException:
        if prepared is not None:
            _dispose_prepared_transfer_worker(prepared)
            prepared = None
            process = None
        else:
            _kill_and_reap_transfer_worker(
                process,
                process_group_id=process.pid if process is not None else None,
            )
        raise ValidationError("isolated transfer worker readiness failed") from None
    finally:
        for descriptor in (
            source_fd,
            child_command_fd,
            parent_command_fd,
            child_key_fd,
            parent_key_fd,
            child_body_fd,
            parent_body_fd,
            parent_result_fd,
            child_result_fd,
        ):
            _close_transfer_worker_fd(descriptor)


def _revalidate_prepared_transfer_worker(
    worker: _PreparedVoiceTransferWorker,
) -> None:
    """Recheck the exact READY process and bound source identities in place."""

    process = worker.process
    try:
        process_group_id = os.getpgid(worker.pid)
        session_id = os.getsid(worker.pid)
        current_source_path, current_source_sha = _read_exact_regular_file_identity(
            Path(worker.worker_source_path),
            cap=_TRANSFER_WORKER_SOURCE_MAX_BYTES,
            require_current_uid=True,
            require_executable=False,
            label="isolated transfer worker source",
        )
        (
            current_interpreter_path,
            current_interpreter_sha,
            current_interpreter_version,
            current_interpreter_identity,
        ) = _system_transfer_worker_interpreter_identity()
    except (OSError, ProcessLookupError, ValidationError):
        raise ValidationError("isolated transfer worker identity revalidation failed") from None
    if (
        worker.state != "ready"
        or process is None
        or process.poll() is not None
        or worker.pid <= 1
        or worker.process_group_id != worker.pid
        or process.pid != worker.pid
        or process_group_id != worker.process_group_id
        or session_id != worker.pid
        or type(worker.child_monotonic_ns_at_ready) is not int
        or worker.child_monotonic_ns_at_ready <= 0
        or type(worker.parent_ready_received_ns) is not int
        or worker.parent_ready_received_ns <= 0
        or worker.parent_ready_received_ns > time.monotonic_ns()
        or current_source_path != worker.worker_source_path
        or current_source_sha != worker.worker_source_sha256
        or current_interpreter_path != worker.interpreter_path
        or current_interpreter_sha != worker.interpreter_sha256
        or current_interpreter_version != worker.python_version
        or current_interpreter_identity != worker.interpreter_identity
    ):
        raise ValidationError("isolated transfer worker identity changed after READY")


def _map_transfer_worker_child_deadline(
    worker: _PreparedVoiceTransferWorker,
    parent_deadline_ns: int,
    *,
    parent_now_ns: int | None = None,
) -> int:
    """Map a parent deadline to the child's distinct monotonic epoch early."""

    if (
        type(parent_deadline_ns) is not int
        or type(worker.parent_ready_received_ns) is not int
        or type(worker.child_monotonic_ns_at_ready) is not int
        or worker.parent_ready_received_ns <= 0
        or worker.child_monotonic_ns_at_ready <= 0
    ):
        raise ValidationError("isolated transfer worker deadline samples are invalid")
    if parent_now_ns is None:
        parent_now_ns = time.monotonic_ns()
    if type(parent_now_ns) is not int:
        raise ValidationError("isolated transfer worker parent clock sample is invalid")
    ready_age_ns = parent_now_ns - worker.parent_ready_received_ns
    remaining_at_mapping_ns = parent_deadline_ns - parent_now_ns
    if (
        ready_age_ns < 0
        or ready_age_ns > int(_TRANSFER_WORKER_MAX_READY_AGE_SECONDS * 1_000_000_000)
        or remaining_at_mapping_ns <= 0
        or remaining_at_mapping_ns
        > int(_TRANSFER_WORKER_MAX_TRANSACTION_SECONDS * 1_000_000_000)
    ):
        raise ValidationError("isolated transfer worker deadline mapping is stale")
    remaining_from_ready_ns = parent_deadline_ns - worker.parent_ready_received_ns
    child_deadline_ns = worker.child_monotonic_ns_at_ready + remaining_from_ready_ns
    if (
        child_deadline_ns <= worker.child_monotonic_ns_at_ready
        or child_deadline_ns > (1 << 63) - 1
    ):
        raise ValidationError("isolated transfer worker deadline mapping overflowed")
    return child_deadline_ns


def _exchange_with_transfer_worker(
    worker: _PreparedVoiceTransferWorker,
    *,
    command_frame: bytes,
    key_frame: bytearray,
    body: bytearray,
    result_cap: int,
    deadline_ns: int,
) -> bytearray:
    """Nonblocking pipe exchange bounded by one original monotonic deadline."""

    process = worker.process
    if process is None or worker.state != "ready" or process.poll() is not None:
        raise _pre_go_worker_failure("isolated_worker_not_ready")
    descriptor_set = {
        worker.command_fd,
        worker.result_fd,
        worker.key_fd,
        worker.body_fd,
    }
    now_ns = time.monotonic_ns()
    if (
        type(deadline_ns) is not int
        or deadline_ns <= now_ns
        or deadline_ns - now_ns > int(TRANSFER_MAX_ELAPSED_SECONDS * 1_000_000_000)
        or result_cap != _TRANSFER_WORKER_EXCHANGE_MAX_BYTES
        or type(result_cap) is not int
        or len(descriptor_set) != 4
        or any(descriptor < 0 for descriptor in descriptor_set)
        or not isinstance(command_frame, bytes)
        or len(command_frame) < _TRANSFER_WORKER_FRAME_LENGTH_STRUCT.size
        or _TRANSFER_WORKER_FRAME_LENGTH_STRUCT.unpack(
            command_frame[: _TRANSFER_WORKER_FRAME_LENGTH_STRUCT.size]
        )[0]
        != len(command_frame) - _TRANSFER_WORKER_FRAME_LENGTH_STRUCT.size
        or len(command_frame) - _TRANSFER_WORKER_FRAME_LENGTH_STRUCT.size
        > _TRANSFER_WORKER_COMMAND_FRAME_MAX_BYTES
        or not isinstance(key_frame, bytearray)
        or len(key_frame) < _TRANSFER_WORKER_FRAME_LENGTH_STRUCT.size + 1
        or _TRANSFER_WORKER_FRAME_LENGTH_STRUCT.unpack(
            key_frame[: _TRANSFER_WORKER_FRAME_LENGTH_STRUCT.size]
        )[0]
        != len(key_frame) - _TRANSFER_WORKER_FRAME_LENGTH_STRUCT.size
        or len(key_frame) - _TRANSFER_WORKER_FRAME_LENGTH_STRUCT.size
        > _TRANSFER_WORKER_KEY_FRAME_MAX_BYTES
        or not isinstance(body, bytearray)
        or len(body) != _TRANSFER_WORKER_FRAME_LENGTH_STRUCT.size + TRANSFER_BODY_BYTES
        or _TRANSFER_WORKER_FRAME_LENGTH_STRUCT.unpack(
            body[: _TRANSFER_WORKER_FRAME_LENGTH_STRUCT.size]
        )[0]
        != TRANSFER_BODY_BYTES
    ):
        raise _pre_go_worker_failure("isolated_worker_exchange_contract_invalid")
    outbound: dict[int, tuple[str, memoryview, int]] = {}
    result = bytearray()
    selector: selectors.BaseSelector | None = None
    result_eof = False
    failure: pt._GuideExecutionFailure | None = None
    worker.state = "go_consumed"
    try:
        outbound = {
            worker.command_fd: ("command_fd", memoryview(command_frame), 0),
            worker.key_fd: ("key_fd", memoryview(key_frame), 0),
            worker.body_fd: ("body_fd", memoryview(body), 0),
        }
        selector = selectors.DefaultSelector()
        for descriptor in (*outbound, worker.result_fd):
            os.set_blocking(descriptor, False)
        selector.register(worker.result_fd, selectors.EVENT_READ, "result")
        for descriptor in outbound:
            selector.register(descriptor, selectors.EVENT_WRITE, "write")
        while True:
            remaining_ns = deadline_ns - time.monotonic_ns()
            if remaining_ns <= 0:
                failure = _post_go_worker_failure(
                    "provider_request_elapsed_cap_exceeded",
                    response_state="unknown",
                )
                break
            if result_eof and not outbound:
                return_code = process.poll()
                if return_code is not None:
                    if return_code != 0:
                        failure = _post_go_worker_failure(
                            "isolated_worker_exit_failure",
                            response_state="unknown",
                        )
                        break
                    return result
            wait_seconds = min(remaining_ns / 1_000_000_000, 0.05)
            events = selector.select(wait_seconds)
            if not events and process.poll() is not None and not result_eof:
                # Give the result pipe one final nonblocking drain; a clean
                # worker must still supply EOF after exactly one result.
                try:
                    chunk = os.read(worker.result_fd, min(65_536, result_cap + 1 - len(result)))
                except BlockingIOError:
                    chunk = None
                except OSError:
                    chunk = b""
                if chunk:
                    result.extend(chunk)
                elif chunk == b"":
                    result_eof = True
                    try:
                        selector.unregister(worker.result_fd)
                    except Exception:
                        pass
                    _close_transfer_worker_fd(worker.result_fd)
                    worker.result_fd = -1
                continue
            for key, mask in events:
                descriptor = key.fd
                if key.data == "result" and mask & selectors.EVENT_READ:
                    remaining = result_cap + 1 - len(result)
                    if remaining <= 0:
                        failure = _post_go_worker_failure(
                            "isolated_worker_result_cap_exceeded",
                            response_state="unknown",
                        )
                        break
                    try:
                        chunk = os.read(descriptor, min(65_536, remaining))
                    except BlockingIOError:
                        continue
                    except OSError:
                        chunk = b""
                    if chunk:
                        result.extend(chunk)
                        if len(result) > result_cap:
                            failure = _post_go_worker_failure(
                                "isolated_worker_result_cap_exceeded",
                                response_state="unknown",
                            )
                            break
                    else:
                        result_eof = True
                        try:
                            selector.unregister(descriptor)
                        except Exception:
                            pass
                        _close_transfer_worker_fd(descriptor)
                        worker.result_fd = -1
                elif key.data == "write" and mask & selectors.EVENT_WRITE:
                    name, view, offset = outbound[descriptor]
                    try:
                        written = os.write(descriptor, view[offset : offset + 65_536])
                    except BlockingIOError:
                        continue
                    except (BrokenPipeError, OSError):
                        failure = _post_go_worker_failure(
                            "isolated_worker_command_channel_failure",
                            response_state="unknown",
                        )
                        break
                    if written <= 0:
                        failure = _post_go_worker_failure(
                            "isolated_worker_command_channel_failure",
                            response_state="unknown",
                        )
                        break
                    offset += written
                    if offset == len(view):
                        try:
                            selector.unregister(descriptor)
                        except Exception:
                            pass
                        _close_transfer_worker_fd(descriptor)
                        setattr(worker, name, -1)
                        view.release()
                        del outbound[descriptor]
                    else:
                        outbound[descriptor] = (name, view, offset)
            if failure is not None:
                break
        assert failure is not None
        # GO permanently consumes the sole POST budget.  Any ambiguous
        # post-GO failure must stop credential-bearing activity at once; do not
        # grant a TERM grace period beyond the absolute provider deadline.
        reaped = _kill_and_reap_transfer_worker(
            process,
            process_group_id=worker.process_group_id,
            immediate=True,
        )
        _apply_partial_worker_phase_evidence(failure, result)
        if not reaped:
            raise _worker_reap_failure(failure)
        worker.process = None
        worker.state = "closed"
        raise failure
    except BaseException:
        if worker.state == "go_consumed":
            reaped = _kill_and_reap_transfer_worker(
                process,
                process_group_id=worker.process_group_id,
                immediate=True,
            )
            if reaped:
                worker.process = None
                worker.state = "closed"
        raise
    finally:
        if selector is not None:
            selector.close()
        for descriptor, (name, view, _offset) in list(outbound.items()):
            view.release()
            _close_transfer_worker_fd(descriptor)
            setattr(worker, name, -1)
        outbound = {}
        if worker.state == "closed" and worker.result_fd >= 0:
            _close_transfer_worker_fd(worker.result_fd)
            worker.result_fd = -1
        for index in range(len(key_frame)):
            key_frame[index] = 0
        if failure is not None:
            result[:] = b"\x00" * len(result)
            result.clear()


def _validate_transfer_worker_result_common(document: dict[str, Any]) -> None:
    identifiers = document.get("provider_identifiers")
    usage = document.get("provider_usage")
    evidence_errors: list[str] = []
    _validate_persisted_provider_evidence(
        identifiers,
        usage,
        evidence_errors,
        "isolated transfer worker result",
    )
    if (
        set(document) != _TRANSFER_WORKER_RESULT_KEYS
        or document.get("protocol") != _TRANSFER_WORKER_PROTOCOL
        or document.get("message") != "result"
        or document.get("application_http_attempts") not in {0, 1}
        or type(document.get("application_http_attempts")) is not int
        or document.get("application_retries_made") != 0
        or type(document.get("application_retries_made")) is not int
        or document.get("application_redirects_followed") != 0
        or type(document.get("application_redirects_followed")) is not int
        or document.get("application_fallbacks_used") != 0
        or type(document.get("application_fallbacks_used")) is not int
        or document.get("network_stack_address_selection_state")
        != "stdlib_internal_connection_selection_possible"
        or document.get("network_state")
        not in {
            "not_started",
            "application_request_starting",
            "application_request_started",
        }
        or document.get("request_state")
        not in {"not_started", "outcome_unknown", "response_confirmed"}
        or document.get("response_state")
        not in {
            "none",
            "headers_confirmed",
            "headers_rejected",
            "body_complete",
            "body_rejected",
        }
        or document.get("response_body_disposition")
        not in {"not_read", "hash_count_only", "discarded_credential_echo", "raw_success_frame"}
        or document.get("response_byte_count_state")
        not in {"none", "exact", "bounded_prefix"}
        or document.get("response_bytes") < 0
        or type(document.get("response_bytes")) is not int
        or document.get("response_bytes") > _TRANSFER_WORKER_RESULT_BODY_MAX_BYTES
        or evidence_errors
    ):
        raise ValidationError("isolated transfer worker result metadata is invalid")
    digest = document.get("response_sha256")
    if digest is not None and (not isinstance(digest, str) or not _SHA_RE.fullmatch(digest)):
        raise ValidationError("isolated transfer worker result digest is invalid")
    status = document.get("http_status")
    if status is not None and (type(status) is not int or not 100 <= status <= 599):
        raise ValidationError("isolated transfer worker result status is invalid")


def _validate_transfer_worker_result_relations(
    document: dict[str, Any],
    *,
    phase_count: int,
) -> None:
    """Reject individually safe fields whose combined evidence overclaims state."""

    attempts = document["application_http_attempts"]
    network_state = document["network_state"]
    request_state = document["request_state"]
    response_state = document["response_state"]
    disposition = document["response_body_disposition"]
    count_state = document["response_byte_count_state"]
    response_bytes = document["response_bytes"]
    response_sha = document["response_sha256"]
    outcome = document["outcome"]
    invalid = False

    if attempts == 0:
        invalid = (
            phase_count != 0
            or network_state != "not_started"
            or request_state != "not_started"
            or response_state != "none"
            or document["http_status"] is not None
            or document["content_type"] is not None
            or document["content_encoding"] is not None
            or document["provider_identifiers"]
            or document["provider_usage"]
        )
    elif phase_count == 1:
        invalid = (
            network_state != "application_request_started"
            or response_state not in {"none", "headers_rejected"}
            or (
                response_state == "none"
                and (
                    request_state != "outcome_unknown"
                    or document["http_status"] is not None
                    or document["content_type"] is not None
                    or document["content_encoding"] is not None
                    or document["provider_identifiers"]
                    or document["provider_usage"]
                )
            )
            or (
                response_state == "headers_rejected"
                and (
                    request_state != "response_confirmed"
                    or document["content_type"] is not None
                    or document["content_encoding"] is not None
                    or document["provider_identifiers"]
                    or document["provider_usage"]
                )
            )
        )
    elif phase_count == 2:
        invalid = (
            network_state != "application_request_started"
            or request_state != "response_confirmed"
            or response_state
            not in {"headers_confirmed", "body_complete", "body_rejected"}
        )
    else:
        invalid = True

    if outcome == "failure" and response_state == "body_complete":
        invalid = True
    if response_state in {"none", "headers_rejected", "headers_confirmed"} and (
        disposition != "not_read"
        or response_bytes != 0
        or response_sha is not None
    ):
        invalid = True
    if disposition == "not_read" and (response_bytes != 0 or response_sha is not None):
        invalid = True
    if disposition == "hash_count_only" and (
        response_bytes <= 0
        or response_sha is None
        or count_state not in {"exact", "bounded_prefix"}
    ):
        invalid = True
    if disposition == "discarded_credential_echo" and (
        response_sha is not None
        or response_bytes <= 0
        or count_state not in {"exact", "bounded_prefix"}
    ):
        invalid = True
    if disposition == "raw_success_frame" and (
        outcome != "success"
        or response_state != "body_complete"
        or count_state != "exact"
        or response_bytes <= 0
        or response_sha is None
    ):
        invalid = True
    if response_bytes == 0 and disposition not in {"not_read"}:
        invalid = True
    if invalid:
        raise ValidationError("isolated transfer worker result state relation is invalid")


@dataclass(frozen=True)
class _TransferWorkerFailureSnapshot:
    code: str
    post_budget_consumed: bool = True
    response_state: str = "unknown"
    request_state: str = "unknown_after_go"
    http_status: int | None = None
    response_bytes: int = 0
    response_sha256: str | None = None
    provider_identifiers: dict[str, str] | None = None
    provider_usage: dict[str, int] | None = None
    application_http_attempts: int = 0
    primary_failure_code: str | None = None
    child_containment_state: str | None = None


def _failure_from_transfer_worker_snapshot(
    snapshot: _TransferWorkerFailureSnapshot,
) -> pt._GuideExecutionFailure:
    response_confirmed = snapshot.response_state in {
        "headers_confirmed",
        "headers_rejected",
        "body_complete",
        "body_rejected",
    }
    failure = (
        _post_go_worker_failure(
            snapshot.code,
            response_state="confirmed" if response_confirmed else "unknown",
            http_status=snapshot.http_status,
            response_bytes=snapshot.response_bytes,
            response_sha256=snapshot.response_sha256,
            provider_identifiers=dict(snapshot.provider_identifiers or {}),
            provider_usage=dict(snapshot.provider_usage or {}),
        )
        if snapshot.post_budget_consumed
        else _pre_go_worker_failure(snapshot.code)
    )
    failure.provider_request_state = snapshot.request_state
    failure.provider_response_state = snapshot.response_state
    failure.application_http_attempts = snapshot.application_http_attempts
    failure.primary_failure_code = snapshot.primary_failure_code
    failure.child_containment_state = snapshot.child_containment_state
    return failure


class _TransferWorkerParseAbort(Exception):
    pass


def _snapshot_from_worker_failure(
    failure: pt._GuideExecutionFailure,
) -> _TransferWorkerFailureSnapshot:
    response_state = getattr(failure, "provider_response_state", "unknown")
    if response_state not in {
        "none",
        "unknown",
        "headers_confirmed",
        "headers_rejected",
        "body_complete",
        "body_rejected",
    }:
        response_state = "unknown"
    request_state = getattr(failure, "provider_request_state", "unknown_after_go")
    if request_state not in {
        "not_started",
        "unknown_after_go",
        "outcome_unknown",
        "response_confirmed",
    }:
        request_state = "unknown_after_go"
    attempts = getattr(failure, "application_http_attempts", 0)
    if type(attempts) is not int or attempts not in {0, 1}:
        attempts = 0
    status = failure.http_status
    if status is not None and (type(status) is not int or not 100 <= status <= 599):
        status = None
    response_bytes = failure.response_bytes
    if type(response_bytes) is not int or not 0 <= response_bytes <= _TRANSFER_WORKER_RESULT_BODY_MAX_BYTES:
        response_bytes = 0
    response_sha = failure.response_sha256
    if response_sha is not None and (
        not isinstance(response_sha, str) or not _SHA_RE.fullmatch(response_sha)
    ):
        response_sha = None
    return _TransferWorkerFailureSnapshot(
        code=(
            failure.code
            if isinstance(failure.code, str)
            and failure.code in _PARENT_TRANSFER_WORKER_FAILURE_CODES
            else "isolated_worker_protocol_failure"
        ),
        post_budget_consumed=getattr(failure, "post_budget_consumed", True) is True,
        response_state=response_state,
        request_state=request_state,
        http_status=status,
        response_bytes=response_bytes,
        response_sha256=response_sha,
        provider_identifiers=dict(failure.provider_identifiers),
        provider_usage=dict(failure.provider_usage),
        application_http_attempts=attempts,
        primary_failure_code=getattr(failure, "primary_failure_code", None),
        child_containment_state=getattr(failure, "child_containment_state", None),
    )


def _buffer_contains(
    haystack: bytearray,
    needle: bytearray,
) -> bool:
    """Scan mutable exchange storage once with CPython's linear-time C search."""

    return bool(needle) and len(needle) <= len(haystack) and haystack.find(needle) >= 0


def _zero_mutable_buffer(value: bytearray) -> None:
    if value:
        value[:] = b"\x00" * len(value)
        value.clear()


def _parse_abort_snapshot(
    code: str,
    validated_phases: list[dict[str, Any]],
) -> _TransferWorkerFailureSnapshot:
    """Preserve the last independently validated phase on terminal corruption."""

    if len(validated_phases) >= 2:
        return _TransferWorkerFailureSnapshot(
            code=code,
            response_state="headers_confirmed",
            request_state="response_confirmed",
            http_status=validated_phases[1]["http_status"],
            application_http_attempts=1,
        )
    if validated_phases:
        return _TransferWorkerFailureSnapshot(
            code=code,
            response_state="none",
            request_state="outcome_unknown",
            application_http_attempts=1,
        )
    return _TransferWorkerFailureSnapshot(code=code)


def _snapshot_with_code(
    snapshot: _TransferWorkerFailureSnapshot,
    code: str,
) -> _TransferWorkerFailureSnapshot:
    return _TransferWorkerFailureSnapshot(
        code=code,
        post_budget_consumed=snapshot.post_budget_consumed,
        response_state=snapshot.response_state,
        request_state=snapshot.request_state,
        http_status=snapshot.http_status,
        response_bytes=snapshot.response_bytes,
        response_sha256=snapshot.response_sha256,
        provider_identifiers=dict(snapshot.provider_identifiers or {}),
        provider_usage=dict(snapshot.provider_usage or {}),
        application_http_attempts=snapshot.application_http_attempts,
        primary_failure_code=snapshot.primary_failure_code,
        child_containment_state=snapshot.child_containment_state,
    )


def _snapshot_with_reap_failure(
    snapshot: _TransferWorkerFailureSnapshot,
) -> _TransferWorkerFailureSnapshot:
    return _TransferWorkerFailureSnapshot(
        code="isolated_worker_reap_failure",
        post_budget_consumed=snapshot.post_budget_consumed,
        response_state=snapshot.response_state,
        request_state=snapshot.request_state,
        http_status=snapshot.http_status,
        response_bytes=snapshot.response_bytes,
        response_sha256=snapshot.response_sha256,
        provider_identifiers=dict(snapshot.provider_identifiers or {}),
        provider_usage=dict(snapshot.provider_usage or {}),
        application_http_attempts=snapshot.application_http_attempts,
        primary_failure_code=snapshot.code,
        child_containment_state="sigkill_sent_reap_unconfirmed",
    )


def _parse_transfer_worker_exchange(
    raw: bytearray,
    *,
    key_material: bytearray,
) -> tuple[_ElevenResponse | None, _TransferWorkerFailureSnapshot | None]:
    response: _ElevenResponse | None = None
    snapshot: _TransferWorkerFailureSnapshot | None = None
    frames: list[memoryview] = []
    body_frames: list[memoryview] = []
    validated_phases: list[dict[str, Any]] = []
    result: dict[str, Any] = {}
    secret_echo = False
    try:
        if not isinstance(raw, bytearray) or not isinstance(key_material, bytearray):
            raise _TransferWorkerParseAbort("isolated_worker_protocol_failure")
        if len(raw) > _TRANSFER_WORKER_EXCHANGE_MAX_BYTES:
            raise _TransferWorkerParseAbort("isolated_worker_result_cap_exceeded")
        # Scan the whole mutable exchange exactly once before any framing.  A
        # terminal frame that echoes the held key may still follow valid phase
        # evidence, so retain only independently validated leading phases.
        secret_echo = _buffer_contains(raw, key_material)
        frames, complete = _complete_transfer_worker_frames(raw)
        if not complete or not frames:
            raise _TransferWorkerParseAbort("isolated_worker_protocol_failure")

        cursor = 0
        try:
            first = _decode_strict_worker_json(
                frames[cursor],
                _TRANSFER_WORKER_PHASE_FRAME_MAX_BYTES,
                "isolated transfer worker message",
            )
        except ValidationError:
            raise _TransferWorkerParseAbort(
                "isolated_worker_secret_echo_detected"
                if secret_echo
                else "isolated_worker_protocol_failure"
            ) from None
        if first.get("message") == "phase":
            if not _request_starting_phase_valid(first):
                raise _TransferWorkerParseAbort("isolated_worker_protocol_failure")
            validated_phases.append(first)
            cursor += 1
            if cursor >= len(frames):
                raise _TransferWorkerParseAbort("isolated_worker_terminal_result_missing")
            try:
                second = _decode_strict_worker_json(
                    frames[cursor],
                    _TRANSFER_WORKER_PHASE_FRAME_MAX_BYTES,
                    "isolated transfer worker message",
                )
            except ValidationError:
                raise _TransferWorkerParseAbort(
                    "isolated_worker_secret_echo_detected"
                    if secret_echo
                    else "isolated_worker_protocol_failure"
                ) from None
            if second.get("message") == "phase":
                if not _response_headers_phase_valid(second):
                    raise _TransferWorkerParseAbort("isolated_worker_protocol_failure")
                validated_phases.append(second)
                cursor += 1
                if cursor >= len(frames):
                    raise _TransferWorkerParseAbort("isolated_worker_terminal_result_missing")

        if secret_echo:
            raise _TransferWorkerParseAbort("isolated_worker_secret_echo_detected")

        try:
            result = _decode_strict_worker_json(
                frames[cursor],
                _TRANSFER_WORKER_RESULT_FRAME_MAX_BYTES,
                "isolated transfer worker result",
            )
        except ValidationError:
            raise _TransferWorkerParseAbort("isolated_worker_protocol_failure") from None
        if result.get("message") != "result":
            raise _TransferWorkerParseAbort("isolated_worker_terminal_result_missing")
        try:
            _validate_transfer_worker_result_common(result)
            _validate_transfer_worker_result_relations(
                result,
                phase_count=len(validated_phases),
            )
        except ValidationError:
            raise _TransferWorkerParseAbort("isolated_worker_protocol_failure") from None
        if result.get("application_http_attempts") == 1 and not validated_phases:
            raise _TransferWorkerParseAbort("isolated_worker_phase_sequence_invalid")
        if validated_phases and result.get("application_http_attempts") != 1:
            raise _TransferWorkerParseAbort("isolated_worker_phase_sequence_invalid")
        if len(validated_phases) == 2 and result.get("response_state") == "none":
            raise _TransferWorkerParseAbort("isolated_worker_phase_sequence_invalid")
        body_frames = frames[cursor + 1 :]
        outcome = result.get("outcome")
        if outcome == "success":
            if (
                len(validated_phases) != 2
                or len(body_frames) != 1
                or result.get("failure_code") is not None
                or result.get("success_body_follows") is not True
                or result.get("application_http_attempts") != 1
                or result.get("http_status") != 200
                or result.get("request_state") != "response_confirmed"
                or result.get("network_state") != "application_request_started"
                or result.get("response_state") != "body_complete"
                or result.get("response_body_disposition") != "raw_success_frame"
                or result.get("response_byte_count_state") != "exact"
                or result.get("content_type") not in _AUDIO_MIMES
                or result.get("content_encoding") not in {"", "identity"}
            ):
                raise _TransferWorkerParseAbort("isolated_worker_success_result_invalid")
            payload_view = body_frames[0]
            if (
                len(payload_view) != result["response_bytes"]
                or sha256_bytes(payload_view) != result.get("response_sha256")
            ):
                raise _TransferWorkerParseAbort("isolated_worker_success_body_invalid")
            payload = bytes(payload_view)
            response = _ElevenResponse(
                response_bytes=len(payload),
                response_sha256=result["response_sha256"],
                content_type=result["content_type"],
                content_encoding=result["content_encoding"] or "identity",
                payload=payload,
                provider_identifiers=dict(result["provider_identifiers"]),
                provider_usage=dict(result["provider_usage"]),
            )
        else:
            if (
                outcome != "failure"
                or body_frames
                or result.get("success_body_follows") is not False
            ):
                raise _TransferWorkerParseAbort("isolated_worker_failure_result_invalid")
            failure_code = result.get("failure_code")
            if (
                failure_code not in _TRANSFER_WORKER_ALLOWED_FAILURE_CODES
                or not isinstance(failure_code, str)
                or (
                    result.get("content_type") is not None
                    and (
                        not isinstance(result.get("content_type"), str)
                        or not result["content_type"].isascii()
                        or len(result["content_type"]) > 127
                        or not _SAFE_HEADER_VALUE_RE.fullmatch(result["content_type"])
                    )
                )
                or result.get("content_encoding") not in {None, "identity", "forbidden"}
                or (
                    result.get("response_body_disposition") == "discarded_credential_echo"
                    and result.get("response_sha256") is not None
                )
            ):
                raise _TransferWorkerParseAbort("isolated_worker_failure_result_invalid")
            snapshot = _TransferWorkerFailureSnapshot(
                code=failure_code,
                response_state=result["response_state"],
                request_state=result["request_state"],
                http_status=result.get("http_status"),
                response_bytes=result["response_bytes"],
                response_sha256=result.get("response_sha256"),
                provider_identifiers=dict(result["provider_identifiers"]),
                provider_usage=dict(result["provider_usage"]),
                application_http_attempts=result["application_http_attempts"],
            )
    except _TransferWorkerParseAbort as abort:
        response = None
        snapshot = _parse_abort_snapshot(str(abort), validated_phases)
        abort.__traceback__ = None
        abort.__cause__ = None
        abort.__context__ = None
    except BaseException as unexpected:
        response = None
        snapshot = _parse_abort_snapshot(
            "isolated_worker_protocol_failure",
            validated_phases,
        )
        unexpected.__traceback__ = None
        unexpected.__cause__ = None
        unexpected.__context__ = None
    finally:
        for frame in frames:
            frame.release()
        frames = []
        body_frames = []
        validated_phases = []
        result = {}
        _zero_mutable_buffer(raw)
        _zero_mutable_buffer(key_material)
    return response, snapshot


def _perform_prepared_voice_transfer(
    worker: _PreparedVoiceTransferWorker,
    *,
    api_key_material: bytearray,
    body: bytearray,
    timeout: float,
    absolute_deadline_ns: int | None = None,
) -> _ElevenResponse:
    """Release one exact POST to a READY child under a parent hard deadline."""

    response: _ElevenResponse | None = None
    snapshot: _TransferWorkerFailureSnapshot | None = None
    key_frame = bytearray()
    body_frame = bytearray()
    raw = bytearray()
    command_payload = b""
    command_frame = b""
    deadline_ns = 0
    child_deadline_ns = 0
    post_budget_consumed = False
    try:
        _revalidate_prepared_transfer_worker(worker)
        if (
            type(timeout) not in {int, float}
            or not 0 < float(timeout) <= TRANSFER_MAX_ELAPSED_SECONDS
        ):
            raise _pre_go_worker_failure("isolated_worker_deadline_invalid")
        if (
            not isinstance(api_key_material, bytearray)
            or not api_key_material
            or len(api_key_material) > _TRANSFER_WORKER_KEY_FRAME_MAX_BYTES
            or any(value < 33 or value > 126 for value in api_key_material)
        ):
            raise _pre_go_worker_failure("isolated_worker_key_invalid")
        if (
            not isinstance(body, bytearray)
            or len(body) != TRANSFER_BODY_BYTES
            or sha256_bytes(body) != TRANSFER_BODY_SHA256
        ):
            raise _pre_go_worker_failure("compiled_request_body_binding_failed")

        # The one absolute request deadline begins before any GO frame byte is
        # constructed or written.  Setup time can only shorten, never extend,
        # the provider transaction window.
        now_ns = time.monotonic_ns()
        requested_deadline_ns = now_ns + int(float(timeout) * 1_000_000_000)
        if absolute_deadline_ns is None:
            deadline_ns = requested_deadline_ns
        elif (
            type(absolute_deadline_ns) is not int
            or absolute_deadline_ns <= now_ns
            or absolute_deadline_ns > requested_deadline_ns
        ):
            raise _pre_go_worker_failure("isolated_worker_deadline_invalid")
        else:
            deadline_ns = absolute_deadline_ns
        # Different Python runtimes on macOS can expose different monotonic
        # epochs.  READY binds one sample from each process; subtracting the
        # parent READY-receipt sample makes the child's deadline conservative
        # by the READY pipe transit time instead of assuming shared epochs.
        try:
            child_deadline_ns = _map_transfer_worker_child_deadline(worker, deadline_ns)
        except ValidationError:
            raise _pre_go_worker_failure("isolated_worker_deadline_invalid")
        key_frame.extend(_TRANSFER_WORKER_FRAME_LENGTH_STRUCT.pack(len(api_key_material)))
        key_frame.extend(api_key_material)
        body_frame.extend(_TRANSFER_WORKER_FRAME_LENGTH_STRUCT.pack(len(body)))
        body_frame.extend(body)
        command_payload = _canonical_worker_json(
            {
                "action": "release_exact_transfer",
                "application_http_attempt_limit": 1,
                "body_bytes": TRANSFER_BODY_BYTES,
                "body_sha256": TRANSFER_BODY_SHA256,
                "child_deadline_monotonic_ns": child_deadline_ns,
                "protocol": _TRANSFER_WORKER_PROTOCOL,
            }
        )
        if len(command_payload) > _TRANSFER_WORKER_COMMAND_FRAME_MAX_BYTES:
            raise _pre_go_worker_failure("isolated_worker_command_frame_invalid")
        command_frame = (
            _TRANSFER_WORKER_FRAME_LENGTH_STRUCT.pack(len(command_payload))
            + command_payload
        )
        raw = _exchange_with_transfer_worker(
            worker,
            command_frame=command_frame,
            key_frame=key_frame,
            body=body_frame,
            result_cap=_TRANSFER_WORKER_EXCHANGE_MAX_BYTES,
            deadline_ns=deadline_ns,
        )
        post_budget_consumed = True
        response, snapshot = _parse_transfer_worker_exchange(
            raw,
            key_material=api_key_material,
        )
        if time.monotonic_ns() > deadline_ns:
            if snapshot is None:
                snapshot = _TransferWorkerFailureSnapshot(
                    code="provider_request_elapsed_cap_exceeded",
                    response_state="body_complete",
                    request_state="response_confirmed",
                    http_status=200,
                    response_bytes=(response.response_bytes if response is not None else 0),
                    response_sha256=(response.response_sha256 if response is not None else None),
                    provider_identifiers=(
                        dict(response.provider_identifiers) if response is not None else {}
                    ),
                    provider_usage=(
                        dict(response.provider_usage) if response is not None else {}
                    ),
                    application_http_attempts=1,
                )
            else:
                snapshot = _snapshot_with_code(
                    snapshot,
                    "provider_request_elapsed_cap_exceeded",
                )
            response = None
    except pt._GuideExecutionFailure as failure:
        response = None
        snapshot = _snapshot_from_worker_failure(failure)
        failure.__traceback__ = None
        failure.__cause__ = None
        failure.__context__ = None
    except BaseException as unexpected:
        post_budget_consumed = worker.state != "ready"
        response = None
        snapshot = _TransferWorkerFailureSnapshot(
            code="isolated_worker_protocol_failure",
            post_budget_consumed=post_budget_consumed,
            response_state="unknown" if post_budget_consumed else "none",
            request_state="unknown_after_go" if post_budget_consumed else "not_started",
        )
        unexpected.__traceback__ = None
        unexpected.__cause__ = None
        unexpected.__context__ = None
    finally:
        post_budget_consumed = post_budget_consumed or worker.state != "ready"
        try:
            if not _dispose_prepared_transfer_worker(worker):
                response = None
                if snapshot is not None:
                    snapshot = _snapshot_with_reap_failure(snapshot)
                else:
                    snapshot = _TransferWorkerFailureSnapshot(
                        code="isolated_worker_reap_failure",
                        post_budget_consumed=post_budget_consumed,
                        response_state="unknown" if post_budget_consumed else "none",
                        request_state="unknown_after_go" if post_budget_consumed else "not_started",
                        primary_failure_code="isolated_worker_protocol_failure",
                        child_containment_state="sigkill_sent_reap_unconfirmed",
                    )
        except BaseException as cleanup_error:
            response = None
            if snapshot is not None:
                snapshot = _snapshot_with_reap_failure(snapshot)
            else:
                snapshot = _TransferWorkerFailureSnapshot(
                    code="isolated_worker_reap_failure",
                    post_budget_consumed=post_budget_consumed,
                    response_state="unknown" if post_budget_consumed else "none",
                    request_state="unknown_after_go" if post_budget_consumed else "not_started",
                    primary_failure_code="isolated_worker_protocol_failure",
                    child_containment_state="sigkill_sent_reap_unconfirmed",
                )
            cleanup_error.__traceback__ = None
            cleanup_error.__cause__ = None
            cleanup_error.__context__ = None
        if isinstance(api_key_material, bytearray):
            _zero_mutable_buffer(api_key_material)
        if isinstance(body, bytearray):
            _zero_mutable_buffer(body)
        _zero_mutable_buffer(key_frame)
        _zero_mutable_buffer(body_frame)
        _zero_mutable_buffer(raw)
        command_payload = b""
        command_frame = b""
    if snapshot is not None:
        raise _failure_from_transfer_worker_snapshot(snapshot) from None
    if response is None:
        raise _failure_from_transfer_worker_snapshot(
            _TransferWorkerFailureSnapshot(code="isolated_worker_protocol_failure")
        ) from None
    return response


def _set_response_deadline_timeout(response: Any, remaining: float) -> bool:
    if remaining <= 0:
        return False
    candidates = [response]
    try:
        candidates.extend(
            [
                response.fp,
                response.fp.raw,
                response.fp.raw._sock,
                response.fp._sock,
            ]
        )
    except Exception:
        pass
    for candidate in candidates:
        setter = getattr(candidate, "settimeout", None)
        if callable(setter):
            try:
                setter(remaining)
                return True
            except Exception:
                continue
    return False


def _read_response_to_eof(
    response: Any,
    headers: dict[str, str],
    cap: int,
    deadline: float,
) -> tuple[bytes, str | None]:
    declared = headers.get("content-length")
    if declared is not None:
        if not declared.isascii() or not declared.isdigit():
            return b"", "provider_content_length_invalid"
        if int(declared) > cap:
            return b"", "provider_response_byte_cap_exceeded"
    chunks: list[bytes] = []
    chunk = b""
    received = 0
    failure: str | None = None
    try:
        while True:
            remaining_seconds = deadline - _monotonic()
            if remaining_seconds <= 0:
                failure = "provider_request_elapsed_cap_exceeded"
                break
            if not _set_response_deadline_timeout(response, remaining_seconds):
                failure = "provider_total_deadline_unenforceable"
                break
            remaining = cap + 1 - received
            if remaining <= 0:
                failure = "provider_response_byte_cap_exceeded"
                break
            chunk = response.read(min(65_536, remaining))
            if not isinstance(chunk, bytes):
                failure = "provider_response_stream_invalid"
                break
            if chunk:
                chunks.append(chunk)
                received += len(chunk)
            if _monotonic() >= deadline:
                failure = "provider_request_elapsed_cap_exceeded"
                break
            if not chunk:
                break
            if received > cap:
                failure = "provider_response_byte_cap_exceeded"
                break
    except Exception:
        failure = "provider_transport_failure"
    # Keep the bounded captured prefix even on cap/deadline/transport failure so
    # the redacted receipt can truthfully bind what the client actually read.
    raw = b"".join(chunks)
    if failure is None and declared is not None and len(raw) != int(declared):
        failure = "provider_response_truncated"
    chunks = []
    chunk = b""
    received = 0
    return raw, failure


def _perform_elevenlabs_request(
    *,
    method: str,
    url: str,
    api_key: str,
    timeout: float,
    accept: str,
    body: bytes | None,
    content_type: str | None,
    response_cap: int,
    expected_mimes: frozenset[str],
) -> _ElevenResponse:
    request: Any = None
    response: Any = None
    close: Any = None
    headers: dict[str, str] = {}
    raw = b""
    pending: pt._GuideExecutionFailure | None = None
    identifiers: dict[str, str] = {}
    usage: dict[str, int] = {}
    content_encoding = ""
    declared_mime = ""
    status_getter: Any = None
    final_getter: Any = None
    status: Any = None
    read_failure: str | None = None
    deadline = _monotonic() + timeout
    try:
        request = urllib.request.Request(url, data=body, method=method)
        request.add_header("Accept", accept)
        request.add_header("Accept-Encoding", "identity")
        request.add_header("xi-api-key", api_key)
        if body is not None:
            if content_type is None:
                raise _eleven_failure("compiled_request_content_type_missing")
            request.add_header("Content-Type", content_type)
            request.add_header("Content-Length", str(len(body)))
        remaining_timeout = deadline - _monotonic()
        if remaining_timeout <= 0:
            raise _eleven_failure("provider_request_elapsed_cap_exceeded")
        response = _open_elevenlabs_request(request, remaining_timeout)
        if _monotonic() >= deadline:
            raise _eleven_failure(
                "provider_request_elapsed_cap_exceeded",
                response_received=True,
            )
        status_getter = getattr(response, "getcode", None)
        status = status_getter() if callable(status_getter) else getattr(response, "status", None)
        headers = pt._response_headers(getattr(response, "headers", {}))
        identifiers, usage = _safe_elevenlabs_provider_evidence(headers, api_key)
        if type(status) is not int or status != 200:
            raw, read_failure = _read_response_to_eof(
                response,
                headers,
                TRANSFER_MAX_ERROR_RESPONSE_BYTES
                if method == "POST"
                else ACCOUNT_MAX_ERROR_RESPONSE_BYTES,
                deadline,
            )
            pending = _eleven_failure(
                read_failure or "provider_http_failure",
                response_received=True,
                http_status=status if type(status) is int else None,
                response_bytes=len(raw),
                response_sha256=sha256_bytes(raw) if raw else None,
                provider_identifiers=identifiers,
                provider_usage=usage,
            )
        else:
            final_getter = getattr(response, "geturl", None)
            if not callable(final_getter) or final_getter() != url:
                raw, read_failure = _read_response_to_eof(response, headers, response_cap, deadline)
                pending = _eleven_failure(
                    read_failure or "provider_redirect_forbidden",
                    response_received=True,
                    http_status=status,
                    response_bytes=len(raw),
                    response_sha256=sha256_bytes(raw) if raw else None,
                    provider_identifiers=identifiers,
                    provider_usage=usage,
                )
            else:
                content_encoding = headers.get("content-encoding", "identity").strip().lower()
                declared_mime = headers.get("content-type", "").split(";", 1)[0].strip().lower()
                raw, read_failure = _read_response_to_eof(response, headers, response_cap, deadline)
                semantic_failure = (
                    "provider_response_encoding_forbidden"
                    if content_encoding not in {"", "identity"}
                    else (
                        "provider_response_mime_invalid"
                        if declared_mime not in expected_mimes
                        else None
                    )
                )
                if read_failure is not None or semantic_failure is not None:
                    pending = _eleven_failure(
                        read_failure or semantic_failure or "provider_response_invalid",
                        response_received=True,
                        http_status=status,
                        response_bytes=len(raw),
                        response_sha256=sha256_bytes(raw) if raw else None,
                        provider_identifiers=identifiers,
                        provider_usage=usage,
                    )
                else:
                    result = _ElevenResponse(
                        response_bytes=len(raw),
                        response_sha256=sha256_bytes(raw),
                        content_type=declared_mime,
                        content_encoding=content_encoding or "identity",
                        payload=raw,
                        provider_identifiers=identifiers,
                        provider_usage=usage,
                    )
                    close = getattr(response, "close", None)
                    if callable(close):
                        try:
                            close()
                        except Exception:
                            pass
                    request = None
                    response = None
                    close = None
                    headers = {}
                    raw = b""
                    api_key = ""
                    body = b"" if body is not None else None
                    identifiers = {}
                    usage = {}
                    content_encoding = ""
                    declared_mime = ""
                    status_getter = None
                    final_getter = None
                    status = None
                    read_failure = None
                    deadline = 0.0
                    return result
    except pt._GuideExecutionFailure as exc:
        if response is not None:
            exc.response_received = True
        pending = exc
    except urllib.error.HTTPError as exc:
        try:
            try:
                headers = pt._response_headers(exc.headers)
                identifiers, usage = _safe_elevenlabs_provider_evidence(headers, api_key)
                raw, read_failure = _read_response_to_eof(
                    exc,
                    headers,
                    TRANSFER_MAX_ERROR_RESPONSE_BYTES
                    if method == "POST"
                    else ACCOUNT_MAX_ERROR_RESPONSE_BYTES,
                    deadline,
                )
                pending = _eleven_failure(
                    read_failure or ("provider_redirect_forbidden" if 300 <= exc.code < 400 else "provider_http_failure"),
                    response_received=True,
                    http_status=exc.code,
                    response_bytes=len(raw),
                    response_sha256=sha256_bytes(raw) if raw else None,
                    provider_identifiers=identifiers,
                    provider_usage=usage,
                )
            except Exception:
                pending = _eleven_failure("provider_http_failure", response_received=True)
        finally:
            try:
                exc.close()
            except Exception:
                pass
    except (urllib.error.URLError, TimeoutError, OSError):
        pending = _eleven_failure("provider_transport_failure", response_received=response is not None)
    except Exception:
        pending = _eleven_failure("provider_transport_failure", response_received=response is not None)
    finally:
        if response is not None:
            close = getattr(response, "close", None)
            if callable(close):
                try:
                    close()
                except Exception:
                    pass
    if pending is None:
        pending = _eleven_failure("provider_transport_failure", response_received=response is not None)
    pending.__cause__ = None
    pending.__context__ = None
    pending.__suppress_context__ = True
    request = None
    response = None
    close = None
    headers = {}
    raw = b""
    api_key = ""
    body = b"" if body is not None else None
    content_type = None
    identifiers = {}
    usage = {}
    content_encoding = ""
    declared_mime = ""
    status_getter = None
    final_getter = None
    status = None
    read_failure = None
    deadline = 0.0
    remaining_timeout = 0.0
    raise pending from None


def _negative_ffprobe_media_detection(
    data: bytes,
    *,
    ffprobe_path: str,
    ffprobe_sha256: str,
    ffprobe_version: str,
) -> None:
    """Fail unless the exact credential-isolated probe detects no known format."""

    result: subprocess.CompletedProcess[bytes] | None = None
    stdout = b""
    stderr = b""
    parsed_stdout: dict[str, Any] | None = None
    try:
        actual_path, actual_sha = _read_ffprobe_identity(ffprobe_path)
        if (
            actual_path != ffprobe_path
            or actual_sha != ffprobe_sha256
            or _read_ffprobe_version(actual_path, actual_sha) != ffprobe_version
        ):
            raise pt._GuideExecutionFailure("ffprobe_runtime_binding_changed")
        try:
            with pt._private_executable_copy(
                ffprobe_path,
                ffprobe_sha256,
                "ffprobe executable",
            ) as private_ffprobe:
                result = subprocess.run(
                    [ffprobe_path, *FFPROBE_MEDIA_PROBE_ARGUMENTS],
                    executable=private_ffprobe,
                    input=data,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    timeout=FFPROBE_MAX_ELAPSED_SECONDS,
                    check=False,
                    close_fds=True,
                    env={"PATH": "/usr/bin:/bin", "LANG": "C", "LC_ALL": "C"},
                )
        except subprocess.TimeoutExpired as exc:
            exc.stdout = None
            exc.stderr = None
            data = b""
            raise pt._GuideExecutionFailure("ffprobe_media_probe_timeout") from None
        stdout = result.stdout if isinstance(result.stdout, bytes) else b""
        stderr = result.stderr if isinstance(result.stderr, bytes) else b""
        if len(stdout) > 65_536 or len(stderr) > 65_536:
            raise pt._GuideExecutionFailure("ffprobe_media_probe_output_cap_exceeded")
        try:
            parsed_stdout = pt._strict_json_bytes(stdout, "ffprobe negative media probe")
        except Exception:
            raise pt._GuideExecutionFailure("ffprobe_media_probe_output_invalid") from None
        if (
            result.returncode != 1
            or parsed_stdout != {}
            or stderr != FFPROBE_NO_FORMAT_STDERR
        ):
            raise pt._GuideExecutionFailure("ffprobe_detected_or_ambiguous_media_format")
        parsed_stdout = None
    except pt._GuideExecutionFailure as exc:
        code = exc.code
        exc.__cause__ = None
        exc.__context__ = None
        exc.__suppress_context__ = True
        exc.__traceback__ = None
        result = None
        stdout = b""
        stderr = b""
        parsed_stdout = None
        data = b""
        raise pt._GuideExecutionFailure(code) from None
    except Exception:
        result = None
        stdout = b""
        stderr = b""
        parsed_stdout = None
        data = b""
        raise pt._GuideExecutionFailure("ffprobe_media_probe_failed_closed") from None
    finally:
        result = None
        stdout = b""
        stderr = b""
        parsed_stdout = None
        data = b""


def _validate_raw_pcm(
    data: bytes,
    *,
    ffprobe_path: str,
    ffprobe_sha256: str,
    ffprobe_version: str,
) -> dict[str, Any]:
    if not data or len(data) % 2 or len(data) > TRANSFER_MAX_RESPONSE_BYTES:
        raise pt._GuideExecutionFailure("provider_pcm_payload_invalid")
    if not any(data):
        raise pt._GuideExecutionFailure("provider_pcm_payload_silent")
    signatures = (
        b"RIFF", b"FORM", b"ID3", b"fLaC", b"OggS", b"\x1aE\xdf\xa3",
    )
    if any(data.startswith(signature) for signature in signatures):
        raise pt._GuideExecutionFailure("provider_pcm_container_signature_forbidden")
    if len(data) >= 12 and data[4:8] == b"ftyp":
        raise pt._GuideExecutionFailure("provider_pcm_container_signature_forbidden")
    if len(data) >= 2 and data[0] == 0xFF and data[1] & 0xE0 == 0xE0:
        raise pt._GuideExecutionFailure("provider_pcm_compressed_signature_forbidden")
    frame_count = len(data) // 2
    duration = frame_count / 48_000
    if duration < TRANSFER_MIN_OUTPUT_DURATION_SECONDS or duration > TRANSFER_MAX_OUTPUT_DURATION_SECONDS:
        raise pt._GuideExecutionFailure("provider_pcm_duration_out_of_bounds")
    duration_ratio = duration / SELECTED_GUIDE_DURATION_SECONDS
    if not (
        TRANSFER_MIN_OUTPUT_TO_SOURCE_DURATION_RATIO
        <= duration_ratio
        <= TRANSFER_MAX_OUTPUT_TO_SOURCE_DURATION_RATIO
    ):
        raise pt._GuideExecutionFailure("provider_pcm_source_duration_coherence_failed")
    _negative_ffprobe_media_detection(
        data,
        ffprobe_path=ffprobe_path,
        ffprobe_sha256=ffprobe_sha256,
        ffprobe_version=ffprobe_version,
    )
    return {
        "container_interpretation": "raw",
        "codec_interpretation": "pcm_s16le",
        "sample_rate_hz_interpretation": 48_000,
        "channel_count_interpretation": 1,
        "bit_depth_interpretation": 16,
        "frame_count_under_mono_contract_interpretation": frame_count,
        "duration_seconds_under_mono_contract_interpretation": duration,
        "output_to_source_duration_ratio_under_mono_contract_interpretation": duration_ratio,
        "format_parameters_intrinsically_verified": False,
        "channel_count_intrinsically_verified": False,
        "frame_and_duration_computed_under_mono_contract_interpretation": True,
        "lossy_interpretation": False,
    }


def _account_consumption_receipt(
    contract: _AccountExecutionContract,
    consumed_at: datetime,
) -> dict[str, Any]:
    return {
        "schema_version": ACCOUNT_CONSUMPTION_SCHEMA,
        "authorization_id": contract.authorization["authorization_id"],
        "authorization_path": contract.authorization_path.relative_to(contract.root).as_posix(),
        "authorization_sha256": contract.authorization_sha256,
        "scope": ACCOUNT_SCOPE,
        "owner_approval_path": contract.owner_approval_path.relative_to(contract.root).as_posix(),
        "owner_approval_sha256": contract.owner_approval_sha256,
        "browser_readiness_path": contract.browser_readiness_path.relative_to(contract.root).as_posix(),
        "browser_readiness_sha256": contract.browser_readiness_sha256,
        "status": "consumed_before_credential_and_network",
        "consumed_at": _iso(consumed_at),
        "consumed_before_credential_access": True,
        "credential_accessed_at_consumption": False,
        "network_called_at_consumption": False,
        "get_calls_used": 0,
        "post_calls_used": 0,
        "spend_used_usd": 0,
    }


def _parse_account_payload(
    raw: bytes,
    api_key: str,
    preview: str,
) -> tuple[str, str, str, str]:
    payload: dict[str, Any] | None = None
    user_id = ""
    key_echo_state = "absent_or_null"
    preview_echo_state = "absent_or_null"
    try:
        try:
            payload = pt._strict_json_bytes(raw, "ElevenLabs /v1/user response")
        except Exception:
            raise _eleven_failure("account_response_json_invalid", response_received=True) from None
        user_value = payload.get("user_id")
        if (
            not isinstance(user_value, str)
            or not 1 <= len(user_value) <= 256
            or user_value != user_value.strip()
            or any(ord(character) < 33 or ord(character) > 126 for character in user_value)
        ):
            raise _eleven_failure("account_user_id_invalid", response_received=True)
        user_id = user_value
        echoed_key = payload.get("xi_api_key")
        if echoed_key is not None and (not isinstance(echoed_key, str) or echoed_key != api_key):
            raise _eleven_failure("account_optional_api_key_echo_mismatch", response_received=True)
        if echoed_key is not None:
            key_echo_state = "present_exact_match"
        echoed_preview = payload.get("xi_api_key_preview")
        if echoed_preview is not None:
            if (
                not isinstance(echoed_preview, str)
                or not 1 <= len(echoed_preview) <= 256
                or any(ord(character) < 32 or ord(character) > 126 for character in echoed_preview)
                or not echoed_preview.endswith(preview)
            ):
                raise _eleven_failure("account_optional_api_key_preview_invalid", response_received=True)
            # The official contract does not define a mask prefix.  Require only
            # that a present provider preview ends in the same final four bytes
            # already matched in memory to the reviewed browser row, then discard.
            preview_echo_state = "present_last4_match"
        return user_id, _user_scope_hash(user_id), key_echo_state, preview_echo_state
    except pt._GuideExecutionFailure as exc:
        exc.__cause__ = None
        exc.__context__ = None
        exc.__suppress_context__ = True
        pending = exc
        raw = b""
        api_key = ""
        preview = ""
        payload = None
        user_id = ""
        key_echo_state = ""
        preview_echo_state = ""
        raise pending from None


def execute_account_verification(
    authorization_path: Path,
    *,
    timeout: float = 30.0,
) -> dict[str, Any]:
    """Consume one account authority, then perform exactly one authenticated GET."""

    if type(timeout) not in {int, float} or not 0 < float(timeout) <= ACCOUNT_MAX_ELAPSED_SECONDS:
        raise ValidationError("account-verification timeout must be >0 and <=30 seconds")
    contract = _build_account_contract(authorization_path)
    _preflight_tls_environment()
    _preflight_account_paths(contract)
    source_proof = _verify_committed_source(contract, allow_consumption_latch=False)
    # Close validation/action races before the irreversible latch.
    refreshed = _build_account_contract(authorization_path)
    if (
        refreshed.authorization_sha256 != contract.authorization_sha256
        or refreshed.browser_readiness_sha256 != contract.browser_readiness_sha256
    ):
        raise ValidationError("account-verification authority changed before consumption")
    _preflight_account_paths(contract)
    consumed_at = _execution_now()
    if not contract.approved_at <= consumed_at < contract.expires_at:
        raise ValidationError("account-verification authority expired before consumption")
    consumption = _account_consumption_receipt(contract, consumed_at)
    consumption_bytes = _receipt_bytes(consumption)
    if pt._scan_for_secrets(consumption):
        raise ValidationError("account-verification consumption failed secret scan")
    pt._exclusive_fixture_write(contract.root, contract.consumption_relative, consumption_bytes)
    consumption_sha = sha256_bytes(consumption_bytes)
    credential_accessed = False
    network_called = False
    get_calls = 0
    api_key = ""
    key_fingerprint = ""
    user_id = ""
    preview = ""
    response: _ElevenResponse | None = None
    started_at: datetime | None = None
    completed_at: datetime | None = None
    failure: pt._GuideExecutionFailure | None = None
    try:
        _verify_committed_source(contract, allow_consumption_latch=True)
        pt._verify_private_fixture_artifact(
            contract.root,
            contract.consumption_relative,
            consumption_bytes,
            "account-verification consumption latch",
        )
        credential_accessed = True
        api_key, key_fingerprint = _load_elevenlabs_api_key(None)
        if len(api_key) < 4 or not re.fullmatch(r"[A-Za-z0-9]{4}", api_key[-4:]):
            raise pt._GuideExecutionFailure("api_key_preview_shape_unavailable")
        preview = api_key[-4:]
        if _preview_hash(preview) != contract.expected_preview_sha256:
            raise pt._GuideExecutionFailure("api_key_preview_does_not_match_browser_readiness")
        _verify_committed_source(contract, allow_consumption_latch=True)
        pt._verify_private_fixture_artifact(
            contract.root,
            contract.consumption_relative,
            consumption_bytes,
            "account-verification consumption latch",
        )
        _preflight_account_paths_after_latch(contract)
        started_at = _execution_now()
        if (
            started_at < contract.browser_observed_at
            or (started_at - contract.browser_observed_at).total_seconds()
            > ACCOUNT_VERIFICATION_MAX_AGE_SECONDS
        ):
            raise pt._GuideExecutionFailure("browser_readiness_stale_before_account_get")
        if not consumed_at <= started_at < contract.expires_at:
            raise pt._GuideExecutionFailure("authorization_expired_before_account_get")
        get_calls = 1
        network_called = True
        response = _perform_elevenlabs_request(
            method="GET",
            url=ACCOUNT_ENDPOINT,
            api_key=api_key,
            timeout=float(timeout),
            accept="application/json",
            body=None,
            content_type=None,
            response_cap=ACCOUNT_MAX_RESPONSE_BYTES,
            expected_mimes=frozenset({"application/json"}),
        )
        completed_at = _execution_now()
        if not started_at <= completed_at < contract.expires_at:
            raise pt._GuideExecutionFailure("account_response_completed_outside_authority")
        try:
            (
                user_id,
                account_scope_sha,
                key_echo_state,
                preview_echo_state,
            ) = _parse_account_payload(response.payload, api_key, preview)
        except pt._GuideExecutionFailure as parse_failure:
            raise _eleven_failure(
                parse_failure.code,
                response_received=True,
                http_status=200,
                response_bytes=response.response_bytes,
                response_sha256=response.response_sha256,
                provider_identifiers=response.provider_identifiers,
                provider_usage=response.provider_usage,
            ) from None
        receipt = {
            "schema_version": ACCOUNT_RUN_SCHEMA,
            "provider": "elevenlabs",
            "endpoint": ACCOUNT_ENDPOINT,
            "method": "GET",
            "scope": ACCOUNT_SCOPE,
            "outcome": "success",
            "authorization_id": contract.authorization["authorization_id"],
            "authorization_path": contract.authorization_path.relative_to(contract.root).as_posix(),
            "authorization_sha256": contract.authorization_sha256,
            "consumption_record_path": contract.consumption_relative,
            "consumption_record_sha256": consumption_sha,
            "owner_approval_path": contract.owner_approval_path.relative_to(contract.root).as_posix(),
            "owner_approval_sha256": contract.owner_approval_sha256,
            "browser_readiness_path": contract.browser_readiness_path.relative_to(contract.root).as_posix(),
            "browser_readiness_sha256": contract.browser_readiness_sha256,
            "source_proof": source_proof,
            "api_key_fingerprint_sha256": key_fingerprint,
            "api_key_preview_sha256": contract.expected_preview_sha256,
            "api_key_preview_kind": API_KEY_PREVIEW_KIND,
            "api_key_preview_canonicalization": API_KEY_PREVIEW_CANONICALIZATION,
            "api_key_preview_domain_separation": API_KEY_PREVIEW_DOMAIN_TEXT,
            "api_key_preview_hash_is_non_confidential": True,
            "account_linkage_strength": "contextual_non_cryptographic",
            "exact_ui_api_account_equality_claimed": False,
            "ui_key_preview_match": True,
            "account_scope_binding_sha256": account_scope_sha,
            "account_identity_kind": ACCOUNT_IDENTITY_KIND,
            "account_identity_canonicalization": ACCOUNT_IDENTITY_CANONICALIZATION,
            "account_identity_domain_separation": USER_ID_DOMAIN_TEXT,
            "xi_api_key_echo_state": key_echo_state,
            "xi_api_key_preview_echo_state": preview_echo_state,
            "response_bytes": response.response_bytes,
            "response_sha256": response.response_sha256,
            "response_mime_type": response.content_type,
            "response_content_encoding": response.content_encoding,
            "provider_identifiers": response.provider_identifiers,
            "provider_usage": response.provider_usage,
            "provider_get_calls_made": 1,
            "provider_post_calls_made": 0,
            "started_at": _iso(started_at),
            "completed_at": _iso(completed_at),
            "retries_made": 0,
            "redirects_followed": 0,
            "credentials_recorded": False,
            "raw_response_stored": False,
            "raw_api_key_stored": False,
            "raw_api_key_preview_stored": False,
            "raw_user_id_stored": False,
            "account_settings_changed": False,
            "voice_transfer_authorized": False,
            "full_capture_authorized": False,
            "step3_authorized": False,
            "publication_authorized": False,
        }
        receipt_bytes = _receipt_bytes(receipt)
        if (
            pt._scan_for_secrets(receipt)
            or api_key.encode() in receipt_bytes
            or user_id.encode() in receipt_bytes
            or preview.encode() in receipt_bytes
        ):
            raise pt._GuideExecutionFailure("account_receipt_secret_scan_failed")
        pt._exclusive_fixture_write(contract.root, contract.success_relative, receipt_bytes)
        result = {
            "schema_version": "oe-elevenlabs-account-verification-execution-result-v1",
            "valid": True,
            "outcome": "success",
            "authorization_id": contract.authorization["authorization_id"],
            "authorization_consumed": True,
            "provider_get_calls_made": 1,
            "provider_post_calls_made": 0,
            "run_receipt": {"path": contract.success_relative, "sha256": sha256_bytes(receipt_bytes)},
            "network_called": True,
            "credentials_accessed": True,
            "account_settings_changed": False,
            "voice_transfer_authorized": False,
            "full_capture_authorized": False,
            "step3_authorized": False,
            "publication_authorized": False,
        }
        api_key = ""
        key_fingerprint = ""
        user_id = ""
        preview = ""
        key_echo_state = ""
        preview_echo_state = ""
        response = None
        receipt = {}
        receipt_bytes = b""
        return result
    except pt._GuideExecutionFailure as exc:
        failure = exc
    except ValidationError:
        failure = (
            _eleven_failure(
                "local_validation_or_filesystem_failure",
                response_received=True,
                http_status=200,
                response_bytes=response.response_bytes,
                response_sha256=response.response_sha256,
                provider_identifiers=response.provider_identifiers,
                provider_usage=response.provider_usage,
            )
            if response is not None
            else _eleven_failure("local_validation_or_filesystem_failure")
        )
    except Exception:
        failure = (
            _eleven_failure(
                "unexpected_local_failure",
                response_received=True,
                http_status=200,
                response_bytes=response.response_bytes,
                response_sha256=response.response_sha256,
                provider_identifiers=response.provider_identifiers,
                provider_usage=response.provider_usage,
            )
            if response is not None
            else _eleven_failure(
                "unexpected_local_failure",
                response_received=False,
            )
        )
    if failure is None:
        failure = _eleven_failure("unknown_failure", response_received=False)
    failed_at = _execution_now()
    failure_receipt = {
        "schema_version": ACCOUNT_FAILURE_SCHEMA,
        "outcome": "failed_closed",
        "provider": "elevenlabs",
        "scope": ACCOUNT_SCOPE,
        "authorization_id": contract.authorization["authorization_id"],
        "authorization_path": contract.authorization_path.relative_to(contract.root).as_posix(),
        "authorization_sha256": contract.authorization_sha256,
        "consumption_record_path": contract.consumption_relative,
        "consumption_record_sha256": consumption_sha,
        "owner_approval_sha256": contract.owner_approval_sha256,
        "browser_readiness_sha256": contract.browser_readiness_sha256,
        "source_proof": source_proof,
        "failure_code": failure.code,
        "http_status": failure.http_status,
        "response_bytes": failure.response_bytes,
        "response_sha256": failure.response_sha256,
        "provider_identifiers": failure.provider_identifiers,
        "provider_usage": failure.provider_usage,
        "credential_accessed": credential_accessed,
        "network_called": network_called,
        "provider_get_attempts_consumed": get_calls,
        "provider_get_receipt_state": (
            "confirmed_response"
            if getattr(failure, "response_received", False) or response is not None
            else ("ambiguous_transport" if get_calls else "not_attempted")
        ),
        "provider_post_attempts_consumed": 0,
        "provider_response_received": bool(
            getattr(failure, "response_received", False) or response is not None
        ),
        "started_at": _iso(started_at) if started_at else None,
        "failed_at": _iso(failed_at),
        "retry_permitted": False,
        "redirect_permitted": False,
        "raw_response_stored": False,
        "credentials_recorded": False,
        "account_settings_changed": False,
        "voice_transfer_authorized": False,
        "full_capture_authorized": False,
        "step3_authorized": False,
        "publication_authorized": False,
    }
    failure_bytes = _receipt_bytes(failure_receipt)
    if not pt._scan_for_secrets(failure_receipt):
        try:
            pt._exclusive_fixture_write(contract.root, contract.failure_relative, failure_bytes)
        except ValidationError:
            pass
    code = failure.code
    api_key = ""
    key_fingerprint = ""
    user_id = ""
    preview = ""
    response = None
    contract = None
    failure = None
    failure_receipt = {}
    failure_bytes = b""
    raise ValidationError(f"ElevenLabs account verification stopped without retry: {code}") from None


def _preflight_account_paths_after_latch(contract: _AccountExecutionContract) -> None:
    for label, relative in (
        ("account-verification success receipt", contract.success_relative),
        ("account-verification failure receipt", contract.failure_relative),
    ):
        pt._safe_execution_relative(contract.root, relative, label, ".json")


def _preflight_transfer_paths_after_latch(contract: _TransferExecutionContract) -> None:
    for relative, suffix in (
        (contract.raw_relative, ".pcm"),
        (contract.working_relative, ".wav"),
        (contract.success_relative, ".json"),
        (contract.failure_relative, ".json"),
        (contract.conversion_relative, ".json"),
    ):
        pt._safe_execution_relative(contract.root, relative, "V2 transfer destination", suffix)


def _transfer_consumption_receipt(
    contract: _TransferExecutionContract,
    consumed_at: datetime,
) -> dict[str, Any]:
    return {
        "schema_version": TRANSFER_CONSUMPTION_SCHEMA,
        "authorization_id": contract.authorization["authorization_id"],
        "authorization_path": contract.authorization_path.relative_to(contract.root).as_posix(),
        "authorization_sha256": contract.authorization_sha256,
        "scope": TRANSFER_EXEC_SCOPE,
        "status": "consumed_before_credential_and_network",
        "consumed_at": _iso(consumed_at),
        "consumed_before_credential_access": True,
        "credential_accessed_at_consumption": False,
        "network_called_at_consumption": False,
        "account_get_calls_used": 0,
        "generation_post_calls_used": 0,
        "outputs_received": 0,
        "spend_used_usd": 0,
        "primary_request_sha256": contract.authorization["bindings"]["primary_request_sha256"],
        "multipart_body_sha256": contract.authorization["bindings"]["primary_multipart_body_sha256"],
    }


def _require_transfer_evidence_fresh(
    contract: _TransferExecutionContract,
    current: datetime,
) -> None:
    for label, timestamp, ceiling in (
        ("browser readiness", contract.browser_observed_at, DATA_USE_MAX_AGE_SECONDS),
        (
            "credential-account verification",
            contract.account_verified_at,
            ACCOUNT_VERIFICATION_MAX_AGE_SECONDS,
        ),
        ("data-use assurance", contract.data_verified_at, DATA_USE_MAX_AGE_SECONDS),
    ):
        if current < timestamp or (current - timestamp).total_seconds() > ceiling:
            raise pt._GuideExecutionFailure(f"{label.replace('-', '_').replace(' ', '_')}_stale")


def execute_voice_transfer(
    authorization_path: Path,
    plan_path: Path,
    canonical_w_path: Path,
    *,
    timeout: float = 60.0,
) -> dict[str, Any]:
    """Consume V2 and perform one exact candidate-B -> Original-C PCM POST."""

    if type(timeout) not in {int, float} or not 0 < float(timeout) <= TRANSFER_MAX_ELAPSED_SECONDS:
        raise ValidationError("voice-transfer timeout must be >0 and <=300 seconds")
    contract = _build_transfer_contract(authorization_path, plan_path, canonical_w_path)
    _preflight_tls_environment()
    _preflight_transfer_paths(contract)
    source_proof = _verify_committed_source(contract, allow_consumption_latch=False)
    refreshed = _build_transfer_contract(authorization_path, plan_path, canonical_w_path)
    if (
        refreshed.authorization_sha256 != contract.authorization_sha256
        or sha256_bytes(refreshed.body) != sha256_bytes(contract.body)
    ):
        raise ValidationError("V2 transfer authority or body changed before consumption")
    refreshed = None
    _preflight_transfer_paths(contract)
    consumed_at = _execution_now()
    if not contract.approved_at <= consumed_at < contract.expires_at:
        raise ValidationError("V2 transfer authority expired before consumption")
    consumption = _transfer_consumption_receipt(contract, consumed_at)
    consumption_bytes = _receipt_bytes(consumption)
    if pt._scan_for_secrets(consumption):
        raise ValidationError("V2 transfer consumption failed secret scan")
    pt._exclusive_fixture_write(contract.root, contract.consumption_relative, consumption_bytes)
    consumption_sha = sha256_bytes(consumption_bytes)
    credential_accessed = False
    network_called = False
    post_calls = 0
    api_key = ""
    response: _ElevenResponse | None = None
    geometry: dict[str, Any] = {}
    raw_written = False
    run_written = False
    started_at: datetime | None = None
    completed_at: datetime | None = None
    failure: pt._GuideExecutionFailure | None = None
    try:
        _verify_committed_source(contract, allow_consumption_latch=True)
        pt._verify_private_fixture_artifact(
            contract.root,
            contract.consumption_relative,
            consumption_bytes,
            "V2 transfer consumption latch",
        )
        credential_accessed = True
        expected_fingerprint = contract.authorization["credential_binding"]["api_key_fingerprint_sha256"]
        api_key, actual_fingerprint = _load_elevenlabs_api_key(expected_fingerprint)
        if actual_fingerprint != expected_fingerprint:
            raise pt._GuideExecutionFailure("api_key_fingerprint_changed_after_consumption")
        _verify_committed_source(contract, allow_consumption_latch=True)
        pt._verify_private_fixture_artifact(
            contract.root,
            contract.consumption_relative,
            consumption_bytes,
            "V2 transfer consumption latch",
        )
        _preflight_transfer_paths_after_latch(contract)
        if (
            len(contract.body) != TRANSFER_BODY_BYTES
            or sha256_bytes(contract.body) != TRANSFER_BODY_SHA256
        ):
            raise pt._GuideExecutionFailure("compiled_request_body_binding_failed")
        started_at = _execution_now()
        _require_transfer_evidence_fresh(contract, started_at)
        if not consumed_at <= started_at < contract.expires_at:
            raise pt._GuideExecutionFailure("authorization_expired_before_voice_transfer_post")
        post_calls = 1
        network_called = True
        exact_url = contract.normalized_request["url"]
        response = _perform_elevenlabs_request(
            method="POST",
            url=exact_url,
            api_key=api_key,
            timeout=float(timeout),
            accept="application/octet-stream",
            body=contract.body,
            content_type=contract.manifest["content_type"],
            response_cap=TRANSFER_MAX_RESPONSE_BYTES,
            expected_mimes=_AUDIO_MIMES,
        )
        completed_at = _execution_now()
        if not started_at <= completed_at < contract.expires_at:
            raise pt._GuideExecutionFailure("voice_transfer_response_completed_outside_authority")
        try:
            geometry = _validate_raw_pcm(
                response.payload,
                ffprobe_path=contract.authorization["runtime_bindings"]["ffprobe_binary_path"],
                ffprobe_sha256=contract.authorization["runtime_bindings"]["ffprobe_binary_sha256"],
                ffprobe_version=contract.authorization["runtime_bindings"]["ffprobe_version"],
            )
        except pt._GuideExecutionFailure as media_failure:
            raise _eleven_failure(
                media_failure.code,
                response_received=True,
                http_status=200,
                response_bytes=response.response_bytes,
                response_sha256=response.response_sha256,
                provider_identifiers=response.provider_identifiers,
                provider_usage=response.provider_usage,
            ) from None
        _preflight_transfer_paths_after_latch(contract)
        pt._exclusive_fixture_write(contract.root, contract.raw_relative, response.payload)
        raw_written = True
        pt._verify_private_fixture_artifact(
            contract.root,
            contract.raw_relative,
            response.payload,
            "V2 raw PCM output",
        )
        prerequisite_hashes = {
            name: item["sha256"]
            for name, item in sorted(contract.authorization["prerequisites"].items())
        }
        request_evidence = {
            "part_id": "P01-W0030-W0110",
            "primary_request_sha256": contract.authorization["bindings"]["primary_request_sha256"],
            "normalized_http_request_sha256": contract.authorization["bindings"]["normalized_http_request_sha256"],
            "method": "POST",
            "exact_url": exact_url,
            "multipart_body_sha256": TRANSFER_BODY_SHA256,
            "multipart_body_bytes": TRANSFER_BODY_BYTES,
            "content_type": TRANSFER_CONTENT_TYPE,
            "credential_header_name": "xi-api-key",
            "accept": "application/octet-stream",
            "accept_encoding": "identity",
        }
        raw_sha = sha256_bytes(response.payload)
        run = {
            "schema_version": TRANSFER_RUN_SCHEMA,
            "outcome": "success",
            "provider": "elevenlabs",
            "scope": TRANSFER_EXEC_SCOPE,
            "method": "POST",
            "endpoint": pt.TRANSFER_ENDPOINT,
            "part_id": "P01-W0030-W0110",
            "authorization_id": contract.authorization["authorization_id"],
            "authorization_path": contract.authorization_path.relative_to(contract.root).as_posix(),
            "authorization_sha256": contract.authorization_sha256,
            "consumption_record_path": contract.consumption_relative,
            "consumption_record_sha256": consumption_sha,
            "source_proof": source_proof,
            "plan_sha256": contract.authorization["bindings"]["performance_transfer_plan_sha256"],
            "canonical_w_sha256": contract.authorization["bindings"]["canonical_w_sha256"],
            "spoken_text_sha256": contract.authorization["bindings"]["spoken_text_sha256"],
            "selected_guide_sha256": SELECTED_GUIDE_SHA256,
            "selected_guide_run_receipt_sha256": SELECTED_GUIDE_RUN_SHA256,
            "prerequisite_sha256s": prerequisite_hashes,
            "api_key_fingerprint_sha256": expected_fingerprint,
            "account_scope_binding_sha256": contract.authorization["credential_binding"]["account_scope_binding_sha256"],
            "request": request_evidence,
            "provider_evidence": {
                "account_get_calls_made": 0,
                "generation_post_calls_made": 1,
                "outputs_received": 1,
                "request_ids": response.provider_identifiers,
                "usage": response.provider_usage,
            },
            "response": {
                "http_status": 200,
                "response_bytes": response.response_bytes,
                "response_sha256": response.response_sha256,
                "declared_mime_type": response.content_type,
                "content_encoding": response.content_encoding,
                "media_interpretation": {
                    "classification": "interpreted_pcm_under_exact_format_contract",
                    "output_format": "pcm_48000",
                    "declared_mime_allowlist": ["audio/pcm", "audio/mpeg"],
                    "compressed_or_container_signature_detected": False,
                    "negative_ffprobe_detected_format": False,
                    "headerless_bytes_intrinsically_prove_codec_geometry": False,
                    "official_media_contract_sha256": contract.authorization[
                        "prerequisites"
                    ]["official_media_contract"]["sha256"],
                },
            },
            "raw_output": {
                "part_id": "P01-W0030-W0110",
                "path": contract.raw_relative,
                "sha256": raw_sha,
                "byte_count": len(response.payload),
                **geometry,
            },
            "working_output_path": contract.working_relative,
            "conversion_receipt_path": contract.conversion_relative,
            "started_at": _iso(started_at),
            "completed_at": _iso(completed_at),
            "retries_made": 0,
            "redirects_followed": 0,
            "fallbacks_used": 0,
            "modeled_spend_usd": TRANSFER_MAX_SPEND_USD,
            "modeled_spend_basis": "voice_changer_full_minute_worst_case",
            "modeled_spend_provider_enforced": False,
            "taxes_included": False,
            "credentials_recorded": False,
            "raw_api_key_stored": False,
            "creative_approved": False,
            "full_capture_authorized": False,
            "step2_lock_authorized": False,
            "step3_authorized": False,
            "sharing_authorized": False,
            "publication_authorized": False,
        }
        run_bytes = _receipt_bytes(run)
        if pt._scan_for_secrets(run) or api_key.encode() in run_bytes:
            raise pt._GuideExecutionFailure("voice_transfer_receipt_secret_scan_failed")
        pt._exclusive_fixture_write(contract.root, contract.success_relative, run_bytes)
        run_written = True
        # Conversion is local-only and cannot authorize another provider call.
        from .audio import convert_working

        conversion = convert_working(
            contract.root / contract.raw_relative,
            contract.root / contract.working_relative,
            receipt_path=contract.root / contract.success_relative,
            part_id="P01-W0030-W0110",
            record_path=contract.root / contract.conversion_relative,
        )
        result = {
            "schema_version": "oe-elevenlabs-voice-transfer-execution-result-v1",
            "valid": True,
            "outcome": "success",
            "authorization_id": contract.authorization["authorization_id"],
            "authorization_consumed": True,
            "account_get_calls_made": 0,
            "generation_post_calls_made": 1,
            "outputs_received": 1,
            "modeled_spend_usd": TRANSFER_MAX_SPEND_USD,
            "modeled_spend_basis": "voice_changer_full_minute_worst_case",
            "modeled_spend_provider_enforced": False,
            "taxes_included": False,
            "run_receipt": {"path": contract.success_relative, "sha256": sha256_bytes(run_bytes)},
            "raw_output": {"path": contract.raw_relative, "sha256": raw_sha},
            "working_output": {
                "path": contract.working_relative,
                "sha256": conversion["working"]["sha256"],
            },
            "conversion_receipt": {
                "path": contract.conversion_relative,
                "sha256": sha256_file(contract.root / contract.conversion_relative),
            },
            "network_called": True,
            "credentials_accessed": True,
            "retry_permitted": False,
            "fallback_permitted": False,
            "creative_approved": False,
            "full_capture_authorized": False,
            "step2_lock_authorized": False,
            "step3_authorized": False,
            "sharing_authorized": False,
            "publication_authorized": False,
        }
        api_key = ""
        response = None
        geometry = {}
        contract = None
        run = {}
        run_bytes = b""
        conversion = {}
        return result
    except pt._GuideExecutionFailure as exc:
        failure = exc
    except ValidationError:
        if run_written:
            api_key = ""
            response = None
            contract = None
            raise ValidationError(
                "Voice Changer succeeded but local conversion failed closed; provider retry is forbidden"
            ) from None
        failure = (
            _eleven_failure(
                "local_validation_or_filesystem_failure",
                response_received=True,
                http_status=200,
                response_bytes=response.response_bytes,
                response_sha256=response.response_sha256,
                provider_identifiers=response.provider_identifiers,
                provider_usage=response.provider_usage,
            )
            if response is not None
            else _eleven_failure("local_validation_or_filesystem_failure")
        )
    except Exception:
        if run_written:
            api_key = ""
            response = None
            contract = None
            raise ValidationError(
                "Voice Changer succeeded but local conversion failed closed; provider retry is forbidden"
            ) from None
        failure = (
            _eleven_failure(
                "unexpected_local_failure",
                response_received=True,
                http_status=200,
                response_bytes=response.response_bytes,
                response_sha256=response.response_sha256,
                provider_identifiers=response.provider_identifiers,
                provider_usage=response.provider_usage,
            )
            if response is not None
            else _eleven_failure(
                "unexpected_local_failure",
                response_received=False,
            )
        )
    if failure is None:
        failure = _eleven_failure("unknown_failure", response_received=False)
    failed_at = _execution_now()
    retained_raw = None
    if raw_written and response is not None and geometry:
        retained_raw = {
            "path": contract.raw_relative,
            "sha256": sha256_bytes(response.payload),
            "byte_count": len(response.payload),
            **geometry,
        }
    failure_receipt = {
        "schema_version": TRANSFER_FAILURE_SCHEMA,
        "outcome": "failed_closed",
        "provider": "elevenlabs",
        "scope": TRANSFER_EXEC_SCOPE,
        "authorization_id": contract.authorization["authorization_id"],
        "authorization_path": contract.authorization_path.relative_to(contract.root).as_posix(),
        "authorization_sha256": contract.authorization_sha256,
        "consumption_record_path": contract.consumption_relative,
        "consumption_record_sha256": consumption_sha,
        "source_proof": source_proof,
        "primary_request_sha256": contract.authorization["bindings"]["primary_request_sha256"],
        "multipart_body_sha256": TRANSFER_BODY_SHA256,
        "failure_code": failure.code,
        "http_status": failure.http_status,
        "response_bytes": failure.response_bytes,
        "response_sha256": failure.response_sha256,
        "provider_identifiers": failure.provider_identifiers,
        "provider_usage": failure.provider_usage,
        "credential_accessed": credential_accessed,
        "network_called": network_called,
        "account_get_calls_made": 0,
        "generation_post_attempts_consumed": post_calls,
        "provider_post_receipt_state": (
            "confirmed_response"
            if getattr(failure, "response_received", False) or response is not None
            else ("ambiguous_transport" if post_calls else "not_attempted")
        ),
        "provider_response_received": bool(
            getattr(failure, "response_received", False) or response is not None
        ),
        "outputs_received": 1 if response is not None and bool(geometry) else 0,
        "output_written": raw_written,
        "retained_raw_output": retained_raw,
        "run_receipt_written": run_written,
        "started_at": _iso(started_at) if started_at else None,
        "failed_at": _iso(failed_at),
        "retry_permitted": False,
        "redirect_permitted": False,
        "fallback_permitted": False,
        "reconciliation_required": bool(post_calls and not run_written),
        "modeled_spend_usd": TRANSFER_MAX_SPEND_USD if post_calls else 0,
        "modeled_spend_basis": "voice_changer_full_minute_worst_case",
        "modeled_spend_provider_enforced": False,
        "taxes_included": False,
        "credentials_recorded": False,
        "raw_provider_body_stored": raw_written,
        "creative_approved": False,
        "full_capture_authorized": False,
        "step2_lock_authorized": False,
        "step3_authorized": False,
        "sharing_authorized": False,
        "publication_authorized": False,
    }
    failure_bytes = _receipt_bytes(failure_receipt)
    if not pt._scan_for_secrets(failure_receipt):
        try:
            pt._exclusive_fixture_write(contract.root, contract.failure_relative, failure_bytes)
        except ValidationError:
            pass
    code = failure.code
    api_key = ""
    response = None
    geometry = {}
    contract = None
    failure = None
    failure_receipt = {}
    failure_bytes = b""
    raise ValidationError(f"Voice Changer execution stopped without retry or fallback: {code}") from None


# ---------------------------------------------------------------------------
# Isolated account-recovery transaction
# ---------------------------------------------------------------------------


def _recovery_runtime_files() -> dict[str, tuple[str, Path]]:
    """Runtime surface frozen only for recovery; legacy bindings stay unchanged."""

    narration_root = Path(__file__).resolve().parents[2]
    package = narration_root / "runtime" / "oe_narration"
    tests = narration_root / "runtime" / "tests"
    schemas = narration_root / "schemas"
    prefix = "operator-blueprint-v2/02-narration-production/"
    return {
        "voice_transfer_runtime": (
            prefix + "runtime/oe_narration/voice_transfer.py",
            package / "voice_transfer.py",
        ),
        "performance_transfer_runtime": (
            prefix + "runtime/oe_narration/performance_transfer.py",
            package / "performance_transfer.py",
        ),
        "cli_runtime": (prefix + "runtime/oe_narration/cli.py", package / "cli.py"),
        "core_runtime": (prefix + "runtime/oe_narration/core.py", package / "core.py"),
        "init_runtime": (prefix + "runtime/oe_narration/__init__.py", package / "__init__.py"),
        "recovery_schema": (
            prefix + "schemas/elevenlabs-account-recovery-authorization.schema.json",
            schemas / "elevenlabs-account-recovery-authorization.schema.json",
        ),
        "voice_transfer_tests": (
            prefix + "runtime/tests/test_voice_transfer.py",
            tests / "test_voice_transfer.py",
        ),
    }


def expected_recovery_runtime_bindings(*, draft: bool) -> dict[str, Any]:
    if draft:
        return {"state": "pending"}
    result: dict[str, Any] = {"state": "verified", "git_commit": "pending"}
    for name, (_relative, path) in _recovery_runtime_files().items():
        result[f"{name}_sha256"] = sha256_file(path)
    git_path, git_sha = _read_git_identity()
    result.update(
        {
            "git_binary_path": git_path,
            "git_binary_sha256": git_sha,
            "git_version": _read_git_version(git_path, git_sha),
        }
    )
    return result


def _validate_recovery_runtime_bindings(
    value: Any,
    *,
    active: bool,
    errors: list[str],
) -> dict[str, Any]:
    expected_keys = {"state"}
    if active:
        expected_keys |= {
            "git_commit",
            "git_binary_path",
            "git_binary_sha256",
            "git_version",
            *(f"{name}_sha256" for name in _recovery_runtime_files()),
        }
    item = _strict(value, expected_keys, "recovery runtime_bindings")
    if not active:
        if item != {"state": "pending"}:
            errors.append("draft recovery runtime bindings must remain pending")
        return item
    commit = item.get("git_commit")
    if item.get("state") != "verified" or not isinstance(commit, str) or not _GIT_SHA_RE.fullmatch(commit):
        errors.append("active recovery runtime bindings require a verified Git commit")
    for name, (_relative, path) in _recovery_runtime_files().items():
        expected = item.get(f"{name}_sha256")
        if (
            not isinstance(expected, str)
            or not _SHA_RE.fullmatch(expected)
            or not path.is_file()
            or sha256_file(path) != expected
        ):
            errors.append(f"active recovery runtime binding {name} does not match loaded bytes")
    expected_git_sha = item.get("git_binary_sha256")
    try:
        git_path, git_sha = _read_git_identity(item.get("git_binary_path"))
        git_version = _read_git_version(git_path, expected_git_sha)
    except ValidationError:
        errors.append("active recovery runtime Git binding is unavailable or unsafe")
    else:
        if (
            git_path != item.get("git_binary_path")
            or not isinstance(expected_git_sha, str)
            or not _SHA_RE.fullmatch(expected_git_sha)
            or git_sha != expected_git_sha
            or git_version != item.get("git_version")
        ):
            errors.append("active recovery runtime Git binding does not match loaded bytes")
    return item


def _recovery_prior_failure_chain() -> dict[str, Any]:
    return {
        "outcome_commit": RECOVERY_PRIOR_OUTCOME_COMMIT,
        "active_authorization": {
            "path": RECOVERY_PRIOR_ACTIVE_PATH,
            "sha256": RECOVERY_PRIOR_ACTIVE_SHA256,
        },
        "consumption_latch": {
            "path": RECOVERY_PRIOR_LATCH_PATH,
            "sha256": RECOVERY_PRIOR_LATCH_SHA256,
        },
        "failure_receipt": {
            "path": RECOVERY_PRIOR_FAILURE_PATH,
            "sha256": RECOVERY_PRIOR_FAILURE_SHA256,
        },
        "failure_disposition": {
            "path": RECOVERY_PRIOR_DISPOSITION_PATH,
            "sha256": RECOVERY_PRIOR_DISPOSITION_SHA256,
        },
        "prior_authority_reusable": False,
        "prior_latch_reusable": False,
        "prior_latch_deletable": False,
        "retry_or_resumption": False,
    }


def _action_recovery() -> dict[str, Any]:
    return {
        "provider": "elevenlabs",
        "endpoint": ACCOUNT_ENDPOINT,
        "method": "GET",
        "credential_header_name": "xi-api-key",
        "accept": "application/json",
        "accept_encoding": "identity",
        "read_only": True,
        "no_post": True,
        "no_mutation": True,
        "no_retry": True,
        "no_redirect": True,
        "no_fallback": True,
        "no_audio_upload": True,
        "no_paid_call": True,
        "no_voice_changer_request": True,
        "raw_response_storage_forbidden": True,
    }


def _recovery_credential_delivery(active: bool) -> dict[str, Any]:
    base = {
        "state": "verified" if active else "pending",
        "mechanism": "descriptor_read_fixed_dotenv_exact_assignment",
        "dotenv_path": str(RECOVERY_DOTENV_PATH),
        "assignment_name": API_KEY_ENV,
    }
    if not active:
        return base
    return {
        **base,
        "required_file_type": "regular",
        "required_mode": "0600",
        "current_uid_required": True,
        "required_link_count": 1,
        "max_file_bytes": RECOVERY_DOTENV_MAX_BYTES,
        "max_assignment_count": 1,
        "environment_inheritance_used": False,
        "shell_source_forbidden": True,
        "dotenv_re_read_after_latch_forbidden": True,
        "domain_separation": API_KEY_DOMAIN_TEXT,
    }


def _recovery_limits(active: bool) -> dict[str, Any]:
    if not active:
        return {
            "max_credential_preflight_reads": 0,
            "max_execution_credential_reads": 0,
            "max_get_calls": 0,
            "max_post_calls": 0,
            "max_provider_mutations": 0,
            "max_audio_uploads": 0,
            "max_voice_changer_requests": 0,
            "max_response_bytes": 0,
            "max_error_response_bytes": 0,
            "max_request_elapsed_seconds": 0,
            "max_spend_usd": 0,
        }
    return {
        "max_credential_preflight_reads": 1,
        "max_execution_credential_reads": 0,
        "max_get_calls": ACCOUNT_MAX_GET_CALLS,
        "max_post_calls": 0,
        "max_provider_mutations": 0,
        "max_audio_uploads": 0,
        "max_voice_changer_requests": 0,
        "max_response_bytes": ACCOUNT_MAX_RESPONSE_BYTES,
        "max_error_response_bytes": ACCOUNT_MAX_ERROR_RESPONSE_BYTES,
        "max_request_elapsed_seconds": ACCOUNT_MAX_ELAPSED_SECONDS,
        "max_spend_usd": 0,
    }


def _recovery_artifacts(authorization_id: str) -> dict[str, str]:
    return {
        "success_receipt_path": (
            f"receipts/elevenlabs-account/{authorization_id}.recovery-run.json"
        ),
        "failure_receipt_path": (
            f"receipts/elevenlabs-account/{authorization_id}.recovery-failure.json"
        ),
    }


def _recovery_consumption(active: bool) -> dict[str, Any]:
    return {
        "status": "unconsumed" if active else "not_authorized",
        "credential_preflight_reads_used": 0,
        "execution_credential_reads_used": 0,
        "get_calls_used": 0,
        "post_calls_used": 0,
        "credential_read_latch_path": RECOVERY_CREDENTIAL_READ_LATCH_PATH,
        "provider_call_latch_path": RECOVERY_SCOPE_LATCH_PATH,
    }


def _validate_recovery_prior_records(
    root: Path,
    chain: Any,
    errors: list[str],
) -> dict[str, tuple[Path, bytes, str]]:
    if not _exact(chain, _recovery_prior_failure_chain()):
        errors.append("recovery prior zero-network failure chain drifted")
        return {}
    records: dict[str, tuple[Path, bytes, str]] = {}
    for name, binding in (
        ("active_authorization", chain["active_authorization"]),
        ("consumption_latch", chain["consumption_latch"]),
        ("failure_receipt", chain["failure_receipt"]),
        ("failure_disposition", chain["failure_disposition"]),
    ):
        if name in {"active_authorization", "consumption_latch", "failure_receipt"}:
            path, document, raw, digest = _read_recovery_private_json_record(
                root,
                binding["path"],
                binding["sha256"],
                f"recovery prior {name}",
            )
        else:
            path, document, raw, digest = _read_record(
                root,
                binding["path"],
                binding["sha256"],
                f"recovery prior {name}",
                mode=0o644,
            )
        records[name] = (path, raw, digest)
        if name == "active_authorization" and (
            document.get("schema_version") != ACCOUNT_AUTH_SCHEMA
            or document.get("status") != "active"
            or document.get("approved") is not True
            or document.get("authorization_id")
            != "AUTH-ACCOUNT-ai-visibility-v1.1-read-only-user-verification-20260826T105051Z"
            or document.get("consumption", {}).get("record_path")
            != RECOVERY_PRIOR_LATCH_PATH
        ):
            errors.append("recovery prior ACTIVE authorization semantics drifted")
        elif name == "consumption_latch" and (
            document.get("schema_version") != ACCOUNT_CONSUMPTION_SCHEMA
            or document.get("status") != "consumed_before_credential_and_network"
            or document.get("authorization_path") != RECOVERY_PRIOR_ACTIVE_PATH
            or document.get("authorization_sha256") != RECOVERY_PRIOR_ACTIVE_SHA256
            or document.get("get_calls_used") != 0
            or document.get("post_calls_used") != 0
            or document.get("network_called_at_consumption") is not False
        ):
            errors.append("recovery prior immutable latch semantics drifted")
        elif name == "failure_receipt" and (
            document.get("schema_version") != ACCOUNT_FAILURE_SCHEMA
            or document.get("authorization_path") != RECOVERY_PRIOR_ACTIVE_PATH
            or document.get("authorization_sha256") != RECOVERY_PRIOR_ACTIVE_SHA256
            or document.get("consumption_record_path") != RECOVERY_PRIOR_LATCH_PATH
            or document.get("consumption_record_sha256") != RECOVERY_PRIOR_LATCH_SHA256
            or document.get("network_called") is not False
            or document.get("provider_get_attempts_consumed") != 0
            or document.get("provider_post_attempts_consumed") != 0
            or document.get("provider_response_received") is not False
            or document.get("retry_permitted") is not False
            or document.get("raw_response_stored") is not False
            or document.get("account_settings_changed") is not False
        ):
            errors.append("recovery prior zero-network failure semantics drifted")
        elif name == "failure_disposition" and (
            document.get("schema_version")
            != "oe-elevenlabs-account-verification-failure-disposition-v1"
            or document.get("attempt_binding", {}).get("authorization_sha256")
            != RECOVERY_PRIOR_ACTIVE_SHA256
            or document.get("attempt_binding", {}).get("consumption_sha256")
            != RECOVERY_PRIOR_LATCH_SHA256
            or document.get("attempt_binding", {}).get("failure_receipt_sha256")
            != RECOVERY_PRIOR_FAILURE_SHA256
            or document.get("observed_outcome", {}).get("network_called") is not False
            or document.get("observed_outcome", {}).get("provider_get_attempts_consumed")
            != 0
            or document.get("interpretation", {}).get("existing_authorization_reusable")
            is not False
            or document.get("interpretation", {}).get("automatic_retry_permitted")
            is not False
            or document.get("repair_gate", {}).get("prior_latch_reuse_or_deletion_permitted")
            is not False
            or document.get("repair_gate", {}).get("automatic_retry_permitted") is not False
            or document.get("repair_gate", {}).get("execution_semantics")
            != "fresh_transaction_after_zero_provider_call_not_retry_or_resumption"
        ):
            errors.append("recovery prior failure disposition semantics drifted")
    return records


def _validate_recovery_owner_approval(
    root: Path,
    value: Any,
    errors: list[str],
    *,
    expected_owner: str,
) -> tuple[Path, bytes, str, datetime | None]:
    expected = {
        "state": "verified",
        "path": RECOVERY_OWNER_APPROVAL_PATH,
        "sha256": RECOVERY_OWNER_APPROVAL_SHA256,
    }
    if not _exact(value, expected):
        errors.append("recovery owner approval binding drifted")
    path, document, raw, digest = _read_recovery_private_json_record(
        root,
        RECOVERY_OWNER_APPROVAL_PATH,
        RECOVERY_OWNER_APPROVAL_SHA256,
        "recovery owner approval",
    )
    scope = document.get("contextually_approved_recovery_scope")
    gate = document.get("execution_gate")
    prior = document.get("prior_zero_network_failure_chain")
    if (
        document.get("schema_version")
        != "oe-elevenlabs-account-verification-recovery-owner-approval-evidence-v1"
        or document.get("provider") != "elevenlabs"
        or document.get("owner") != expected_owner
        or document.get("approval_basis", {}).get("contextual_assent_accepted") is not True
        or scope is None
        or scope.get("transaction_semantics")
        != "fresh_account_verification_transaction_not_retry_or_resumption"
        or scope.get("limits", {}).get("max_credential_preflight_reads") != 1
        or scope.get("limits", {}).get("max_execution_credential_reads") != 0
        or scope.get("limits", {}).get("max_get_calls") != 1
        or scope.get("limits", {}).get("max_post_calls") != 0
        or scope.get("action", {}).get("raw_key_storage_forbidden") is not True
        or scope.get("action", {}).get("key_suffix_storage_forbidden") is not True
        or scope.get("action", {}).get("user_id_storage_forbidden") is not True
        or gate is None
        or gate.get("this_record_is_an_active_provider_authorization") is not False
        or gate.get("separate_recovery_authorization_required") is not True
        or gate.get("fresh_browser_processed_off_readback_required") is not True
        or gate.get("voice_transfer_authorized") is not False
        or prior is None
        or prior.get("outcome_commit") != RECOVERY_PRIOR_OUTCOME_COMMIT
        or prior.get("active_authorization", {}).get("sha256")
        != RECOVERY_PRIOR_ACTIVE_SHA256
        or prior.get("consumption_latch", {}).get("sha256")
        != RECOVERY_PRIOR_LATCH_SHA256
        or prior.get("failure_receipt", {}).get("sha256")
        != RECOVERY_PRIOR_FAILURE_SHA256
        or prior.get("failure_disposition", {}).get("sha256")
        != RECOVERY_PRIOR_DISPOSITION_SHA256
    ):
        errors.append("recovery owner approval does not bind the exact approved transaction")
    recorded_at = _parse_time(
        document.get("recorded_at"),
        "recovery owner approval recorded_at",
        errors,
    )
    return path, raw, digest, recorded_at


def validate_account_recovery_authorization(authorization_path: Path) -> dict[str, Any]:
    """Validate recovery authority without credential access, writes, or network."""

    authorization_path = Path(authorization_path).absolute()
    root = pt._document_root(authorization_path)
    authorization, authorization_raw, authorization_sha = pt._read_bound_fixture_json(
        root,
        authorization_path,
        "ElevenLabs account-recovery authorization",
    )
    keys = {
        "schema_version", "authorization_id", "status", "approved", "scope", "target",
        "prior_failure_chain", "owner_approval", "browser_readiness", "action",
        "credential_delivery", "runtime_bindings", "authorized_limits", "artifacts",
        "consumption", "approved_by", "approved_at", "expires_at", "execution_ready",
        "blockers",
    }
    _strict(authorization, keys, "ElevenLabs account-recovery authorization")
    errors: list[str] = []
    status = authorization.get("status")
    active = status == "active"
    if status not in {"draft", "active"}:
        errors.append("account-recovery authorization status must be draft or active")
    _validate_authorization_location(
        authorization_path,
        root,
        status,
        "account-recovery authorization",
        errors,
    )
    if authorization.get("schema_version") != RECOVERY_AUTH_SCHEMA:
        errors.append("account-recovery authorization schema mismatch")
    if authorization.get("scope") != RECOVERY_SCOPE:
        errors.append("account-recovery authorization scope mismatch")
    authorization_id = authorization.get("authorization_id")
    if not isinstance(authorization_id, str) or not _SAFE_ID_RE.fullmatch(authorization_id):
        errors.append("account-recovery authorization ID is invalid")
        authorization_id = "invalid"
    _target(authorization.get("target"), root, errors)
    chain = authorization.get("prior_failure_chain")
    if not _exact(chain, _recovery_prior_failure_chain()):
        errors.append("account-recovery prior failure chain drifted")
    if not _exact(authorization.get("action"), _action_recovery()):
        errors.append("account-recovery action drifted")
    if not _exact(
        authorization.get("credential_delivery"),
        _recovery_credential_delivery(active),
    ):
        errors.append("account-recovery credential delivery drifted")
    _validate_recovery_runtime_bindings(
        authorization.get("runtime_bindings"),
        active=active,
        errors=errors,
    )
    if not _exact(authorization.get("authorized_limits"), _recovery_limits(active)):
        errors.append("account-recovery authorized limits drifted")
    if not _exact(authorization.get("artifacts"), _recovery_artifacts(authorization_id)):
        errors.append("account-recovery artifact paths drifted")
    if not _exact(authorization.get("consumption"), _recovery_consumption(active)):
        errors.append("account-recovery consumption state or latch paths drifted")

    owner_record: tuple[Path, bytes, str, datetime | None] | None = None
    browser_record: tuple[Any, ...] | None = None
    if active:
        try:
            private_authorization_raw, private_authorization_sha = (
                _read_recovery_private_bytes(
                    root,
                    authorization_path,
                    "active ElevenLabs account-recovery authorization",
                    max_bytes=2_000_000,
                )
            )
            if (
                private_authorization_raw != authorization_raw
                or private_authorization_sha != authorization_sha
            ):
                errors.append("active account-recovery private authority bytes drifted")
        except ValidationError:
            errors.append(
                "active account-recovery authorization must be exact current-UID "
                "mode-0600 single-link private authority"
            )
        _validate_recovery_prior_records(root, chain, errors)
        approved_by = authorization.get("approved_by")
        if not isinstance(approved_by, str) or not approved_by:
            errors.append("active account recovery requires approved_by")
            approved_by = "invalid"
        owner_record = _validate_recovery_owner_approval(
            root,
            authorization.get("owner_approval"),
            errors,
            expected_owner=approved_by,
        )
        browser_record = _validate_browser_readiness(
            root,
            authorization.get("browser_readiness"),
            errors,
            expected_observer=approved_by,
        )
        try:
            browser_private, browser_private_sha = _read_recovery_private_bytes(
                root,
                browser_record[0],
                "recovery browser-readiness JSON",
                max_bytes=1_000_000,
            )
            if (
                browser_private != browser_record[2]
                or browser_private_sha != browser_record[3]
            ):
                errors.append("recovery browser-readiness private bytes drifted")
            capture_bytes, capture_sha = _read_recovery_private_capture(
                root,
                browser_record[5][0],
            )
            if (
                capture_bytes != browser_record[5][1]
                or capture_sha != browser_record[5][2]
            ):
                errors.append("recovery local-private browser capture bytes drifted")
            _verify_recovery_private_capture_git_state(
                authorization["runtime_bindings"],
                pt._guide_repository_root(),
                browser_record[5][0],
            )
        except ValidationError:
            errors.append("recovery browser capture is not exact local-only evidence")
    else:
        if not _exact(authorization.get("owner_approval"), {"state": "pending"}):
            errors.append("draft recovery owner approval must remain pending")
        if not _exact(authorization.get("browser_readiness"), {"state": "pending"}):
            errors.append("draft recovery browser readiness must remain pending")

    approved_at, expires_at = _parse_window(authorization, active=active, errors=errors)
    if active and owner_record is not None and browser_record is not None:
        owner_at = owner_record[3]
        browser_at = browser_record[4]
        if (
            owner_at is None
            or browser_at is None
            or approved_at is None
            or expires_at is None
            or not owner_at <= browser_at <= approved_at < expires_at
        ):
            errors.append("recovery owner, fresh browser, and approval chronology is invalid")
        elif (approved_at - browser_at).total_seconds() > ACCOUNT_VERIFICATION_MAX_AGE_SECONDS:
            errors.append("recovery browser readiness is stale at approval")
        elif expires_at > browser_at + timedelta(seconds=ACCOUNT_VERIFICATION_MAX_AGE_SECONDS):
            errors.append("recovery expiry exceeds fresh browser-readiness window")
    blockers = authorization.get("blockers")
    if not isinstance(blockers, list) or any(
        not isinstance(item, str) or not item for item in blockers
    ):
        errors.append("account-recovery blockers must be non-empty strings")
    if active:
        if authorization.get("approved") is not True or authorization.get("execution_ready") is not True:
            errors.append("active account recovery must be approved and execution-ready")
        if blockers != []:
            errors.append("active account recovery may not retain blockers")
    else:
        if authorization.get("approved") is not False or authorization.get("execution_ready") is not False:
            errors.append("draft account recovery has zero authority")
        if (
            authorization.get("approved_by") != ""
            or authorization.get("approved_at") != ""
            or authorization.get("expires_at") != ""
        ):
            errors.append("draft account recovery approval fields must be empty")
        if not blockers:
            errors.append("draft account recovery must state blockers")
    _raise_errors(errors)
    return {
        "schema_version": RECOVERY_DRY_RUN_SCHEMA,
        "valid": True,
        "status": (
            "active_exact_recovery_authority_validated"
            if active
            else "blocked_pending_active_recovery_authorization"
        ),
        "authorization_status": status,
        "authorization_id": authorization_id,
        "authorization_sha256": authorization_sha,
        "approved_at": _iso(approved_at) if approved_at else None,
        "expires_at": _iso(expires_at) if expires_at else None,
        "prior_failure_chain_sha256": sha256_bytes(_compact(_recovery_prior_failure_chain())),
        "action": _action_recovery(),
        "maximum": _recovery_limits(active),
        "provider_action_authorized": active,
        "credential_read_authorized": active,
        "network_authorized": active,
        "credentials_accessed": False,
        "network_called": False,
        "provider_calls_made": 0,
        "retry_permitted": False,
        "redirect_permitted": False,
        "fallback_permitted": False,
        "fallback_used": False,
        "legacy_authority_reused": False,
        "legacy_latch_reused_or_deleted": False,
        "retry_or_resumption": False,
        "account_settings_changed": False,
        "voice_transfer_authorized": False,
        "audio_upload_authorized": False,
        "full_capture_authorized": False,
        "creative_approved": False,
        "step2_lock_authorized": False,
        "step3_authorized": False,
        "sharing_authorized": False,
        "publication_authorized": False,
    }


def dry_run_account_recovery(authorization_path: Path) -> dict[str, Any]:
    return validate_account_recovery_authorization(authorization_path)


@dataclass(frozen=True)
class _RecoveryExecutionContract:
    root: Path
    authorization_path: Path
    authorization: dict[str, Any]
    authorization_raw: bytes
    authorization_sha256: str
    approved_at: datetime
    expires_at: datetime
    credential_latch_relative: str
    provider_latch_relative: str
    success_relative: str
    failure_relative: str
    owner_approval_path: Path
    owner_approval_raw: bytes
    owner_approval_sha256: str
    owner_approval_recorded_at: datetime
    browser_readiness_path: Path
    browser_readiness_raw: bytes
    browser_readiness_sha256: str
    expected_preview_sha256: str
    browser_observed_at: datetime
    browser_capture_path: Path
    browser_capture_raw: bytes
    browser_capture_sha256: str
    official_basis_path: Path
    official_basis_raw: bytes
    official_basis_sha256: str
    prior_records: dict[str, tuple[Path, bytes, str]]


def _build_recovery_contract(authorization_path: Path) -> _RecoveryExecutionContract:
    authorization_path = Path(authorization_path).absolute()
    validation = validate_account_recovery_authorization(authorization_path)
    if validation.get("authorization_status") != "active":
        raise ValidationError("account recovery execution requires exact ACTIVE authority")
    root = pt._document_root(authorization_path)
    raw, digest = _read_recovery_private_bytes(
        root,
        authorization_path,
        "active ElevenLabs account-recovery authorization",
        max_bytes=2_000_000,
    )
    authorization = pt._strict_json_bytes(
        raw,
        "active ElevenLabs account-recovery authorization",
    )
    if digest != validation.get("authorization_sha256"):
        raise ValidationError("account-recovery authorization changed after validation")
    errors: list[str] = []
    approved_at = _parse_time(authorization.get("approved_at"), "approved_at", errors)
    expires_at = _parse_time(authorization.get("expires_at"), "expires_at", errors)
    now = _execution_now()
    if (
        errors
        or approved_at is None
        or expires_at is None
        or not approved_at <= now < expires_at
    ):
        raise ValidationError(errors or "account-recovery authority is outside its active window")
    owner_path, owner_raw, owner_sha, owner_at = _validate_recovery_owner_approval(
        root,
        authorization["owner_approval"],
        errors,
        expected_owner=authorization["approved_by"],
    )
    (
        browser_path,
        _browser,
        browser_raw,
        browser_sha,
        browser_at,
        browser_capture,
        official_basis,
    ) = _validate_browser_readiness(
        root,
        authorization["browser_readiness"],
        errors,
        expected_observer=authorization["approved_by"],
    )
    prior_records = _validate_recovery_prior_records(
        root,
        authorization["prior_failure_chain"],
        errors,
    )
    _raise_errors(errors)
    if owner_at is None or browser_at is None:
        raise ValidationError("recovery evidence timestamps are invalid")
    now = _execution_now()
    if (
        now < browser_at
        or (now - browser_at).total_seconds() > ACCOUNT_VERIFICATION_MAX_AGE_SECONDS
    ):
        raise ValidationError("recovery browser readiness is stale at execution")
    browser_document = pt._strict_json_bytes(
        browser_raw,
        "ElevenLabs recovery browser readiness",
    )
    expected_preview = browser_document["api_key"]["preview_sha256"]
    artifacts = authorization["artifacts"]
    consumption = authorization["consumption"]
    return _RecoveryExecutionContract(
        root=root,
        authorization_path=authorization_path,
        authorization=authorization,
        authorization_raw=raw,
        authorization_sha256=digest,
        approved_at=approved_at,
        expires_at=expires_at,
        credential_latch_relative=consumption["credential_read_latch_path"],
        provider_latch_relative=consumption["provider_call_latch_path"],
        success_relative=artifacts["success_receipt_path"],
        failure_relative=artifacts["failure_receipt_path"],
        owner_approval_path=owner_path,
        owner_approval_raw=owner_raw,
        owner_approval_sha256=owner_sha,
        owner_approval_recorded_at=owner_at,
        browser_readiness_path=browser_path,
        browser_readiness_raw=browser_raw,
        browser_readiness_sha256=browser_sha,
        expected_preview_sha256=expected_preview,
        browser_observed_at=browser_at,
        browser_capture_path=browser_capture[0],
        browser_capture_raw=browser_capture[1],
        browser_capture_sha256=browser_capture[2],
        official_basis_path=official_basis[0],
        official_basis_raw=official_basis[1],
        official_basis_sha256=official_basis[2],
        prior_records=prior_records,
    )


def _recovery_contract_snapshot(contract: _RecoveryExecutionContract) -> tuple[Any, ...]:
    return (
        contract.authorization_sha256,
        contract.owner_approval_sha256,
        contract.browser_readiness_sha256,
        contract.browser_capture_sha256,
        contract.official_basis_sha256,
        tuple((name, item[2]) for name, item in sorted(contract.prior_records.items())),
        contract.expected_preview_sha256,
    )


def _read_recovery_private_bytes(
    root: Path,
    path: Path,
    label: str,
    *,
    max_bytes: int,
) -> tuple[bytes, str]:
    """Read one private recovery artifact with UID/mode/link/inode guards."""

    try:
        relative = path.absolute().relative_to(root).as_posix()
    except ValueError:
        raise ValidationError(f"{label} is outside the bound root") from None
    parent_fd, name = pt._open_parent_descriptor(root, relative, create_parents=False)
    descriptor: int | None = None
    chunks: list[bytes] = []
    chunk = b""
    raw = b""
    try:
        descriptor = os.open(
            name,
            os.O_RDONLY
            | getattr(os, "O_NOFOLLOW", 0)
            | getattr(os, "O_CLOEXEC", 0)
            | getattr(os, "O_NONBLOCK", 0),
            dir_fd=parent_fd,
        )
        before = os.fstat(descriptor)
        if (
            not stat.S_ISREG(before.st_mode)
            or stat.S_IMODE(before.st_mode) != 0o600
            or before.st_uid != os.getuid()
            or before.st_nlink != 1
            or not 0 < before.st_size <= max_bytes
        ):
            raise ValidationError(
                f"{label} must be a bounded current-UID mode-0600 single-link regular file"
            )
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
        identity_fields = (
            "st_dev", "st_ino", "st_size", "st_mtime_ns", "st_ctime_ns",
            "st_mode", "st_uid", "st_gid", "st_nlink",
        )
        if (
            len(raw) != before.st_size
            or tuple(getattr(before, field) for field in identity_fields)
            != tuple(getattr(after, field) for field in identity_fields)
        ):
            raise ValidationError(f"{label} changed during descriptor read")
        return raw, sha256_bytes(raw)
    except ValidationError:
        raise
    except OSError:
        raise ValidationError(f"{label} is missing or unsafe") from None
    finally:
        chunks = []
        chunk = b""
        raw = b""
        if descriptor is not None:
            os.close(descriptor)
        os.close(parent_fd)


def _read_recovery_private_json_record(
    root: Path,
    relative: Any,
    expected_sha256: Any,
    label: str,
) -> tuple[Path, dict[str, Any], bytes, str]:
    path = pt._safe_relative(
        root,
        relative,
        f"{label} path",
        must_exist=True,
        suffix=".json",
    )
    raw, digest = _read_recovery_private_bytes(
        root,
        path,
        label,
        max_bytes=2_000_000,
    )
    if (
        not isinstance(expected_sha256, str)
        or not _SHA_RE.fullmatch(expected_sha256)
        or digest != expected_sha256
    ):
        raise ValidationError(f"{label} SHA-256 mismatch")
    return path, pt._strict_json_bytes(raw, label), raw, digest


def _verify_recovery_active_authority_private(
    contract: _RecoveryExecutionContract,
) -> None:
    raw, digest = _read_recovery_private_bytes(
        contract.root,
        contract.authorization_path,
        "active ElevenLabs account-recovery authorization",
        max_bytes=2_000_000,
    )
    if raw != contract.authorization_raw or digest != contract.authorization_sha256:
        raise ValidationError("active account-recovery private authority bytes drifted")


def _verify_recovery_private_latch(
    contract: _RecoveryExecutionContract,
    relative: str,
    expected_raw: bytes,
    label: str,
) -> None:
    path = pt._safe_relative(
        contract.root,
        relative,
        f"{label} path",
        must_exist=True,
        suffix=".json",
    )
    raw, digest = _read_recovery_private_bytes(
        contract.root,
        path,
        label,
        max_bytes=2_000_000,
    )
    if raw != expected_raw or digest != sha256_bytes(expected_raw):
        raise ValidationError(f"{label} immutable bytes drifted")


def _read_recovery_private_capture(
    root: Path,
    path: Path,
) -> tuple[bytes, str]:
    raw, digest = _read_recovery_private_bytes(
        root,
        path,
        "recovery browser capture",
        max_bytes=10_000_000,
    )
    if not raw.startswith(b"\x89PNG\r\n\x1a\n"):
        raw = b""
        raise ValidationError("recovery browser capture is not PNG")
    return raw, digest


def _verify_recovery_private_capture_git_state(
    runtime_bindings: dict[str, Any],
    repository: Path,
    capture_path: Path,
) -> dict[str, Any]:
    """Prove the one redacted PNG is untracked and ignored only by info/exclude."""

    try:
        relative = capture_path.relative_to(repository).as_posix()
    except ValueError:
        raise ValidationError("recovery browser capture is outside repository") from None
    if _bound_git(runtime_bindings, ["ls-files", "--stage", "--", relative]) != b"":
        raise ValidationError("recovery browser capture must remain untracked")
    try:
        exclude_path = _bound_git(
            runtime_bindings,
            ["rev-parse", "--path-format=absolute", "--git-path", "info/exclude"],
        ).strip().decode("utf-8", errors="strict")
        ignored = _bound_git(
            runtime_bindings,
            ["check-ignore", "--no-index", "-v", "--", relative],
        ).decode("utf-8", errors="strict")
    except (UnicodeError, ValidationError):
        raise ValidationError("recovery browser capture exact local ignore proof failed") from None
    if not exclude_path or "\x00" in exclude_path or "\n" in exclude_path:
        raise ValidationError("recovery Git info/exclude path is invalid")
    prefix = exclude_path + ":"
    if not ignored.startswith(prefix) or not ignored.endswith("\t" + relative + "\n"):
        raise ValidationError("recovery browser capture is not ignored by exact Git info/exclude")
    middle = ignored[len(prefix) : -len("\t" + relative + "\n")]
    line_number, separator, pattern = middle.partition(":")
    if (
        separator != ":"
        or not line_number.isascii()
        or not line_number.isdigit()
        or int(line_number) <= 0
        or pattern != "/" + relative
    ):
        raise ValidationError("recovery browser capture ignore rule is not exact and root-anchored")
    return {
        "path": relative,
        "tracked": False,
        "committed": False,
        "ignore_source": "git_info_exclude",
        "ignore_pattern_exact_root_anchored": True,
        "local_private": True,
    }


def _verify_recovery_committed_source(
    contract: _RecoveryExecutionContract,
    *,
    allowed_latches: frozenset[str],
) -> dict[str, Any]:
    repository = pt._guide_repository_root()
    _verify_recovery_active_authority_private(contract)
    bindings = contract.authorization["runtime_bindings"]
    runtime_commit = bindings["git_commit"]
    _verify_local_git_object_store(bindings)
    try:
        head = _bound_git(bindings, ["rev-parse", "HEAD"]).strip().decode("ascii", errors="strict")
    except (UnicodeError, ValidationError):
        raise ValidationError("recovery source proof could not read exact Git identities") from None
    if not _GIT_SHA_RE.fullmatch(head):
        raise ValidationError("recovery local execution HEAD is invalid")
    _bound_git(bindings, ["merge-base", "--is-ancestor", runtime_commit, head])
    _bound_git(
        bindings,
        ["merge-base", "--is-ancestor", RECOVERY_PRIOR_OUTCOME_COMMIT, runtime_commit],
    )
    _bound_git(
        bindings,
        ["merge-base", "--is-ancestor", RECOVERY_OWNER_APPROVAL_COMMIT, runtime_commit],
    )
    try:
        authorization_relative = contract.authorization_path.relative_to(repository).as_posix()
    except ValueError:
        raise ValidationError("recovery ACTIVE authority is outside the repository") from None
    delta = _bound_git(
        bindings,
        [
            "diff", "--no-ext-diff", "--no-textconv", "--no-renames", "--name-only",
            "--diff-filter=ACDMRTUXB", "-z", f"{runtime_commit}..{head}",
        ],
    )
    if delta != authorization_relative.encode("utf-8") + b"\x00":
        raise ValidationError("recovery runtime commit to HEAD delta must be exactly the ACTIVE authority")
    if (
        _bound_git(bindings, ["show", f"HEAD:{authorization_relative}"])
        != contract.authorization_raw
        or sha256_bytes(contract.authorization_raw) != contract.authorization_sha256
    ):
        raise ValidationError("recovery ACTIVE authority is not committed exactly")
    for name, (relative, path) in _recovery_runtime_files().items():
        current, current_sha = _read_bound_blob(
            repository,
            path,
            f"bound recovery runtime {name}",
            max_bytes=5_000_000,
        )
        expected_sha = bindings[f"{name}_sha256"]
        committed = _bound_git(bindings, ["show", f"{runtime_commit}:{relative}"])
        if (
            current_sha != expected_sha
            or sha256_bytes(committed) != expected_sha
            or current != committed
        ):
            raise ValidationError("bound recovery runtime is not exact at runtime commit")
    for name, (path, raw, expected_sha) in contract.prior_records.items():
        if name in {"active_authorization", "consumption_latch", "failure_receipt"}:
            current, current_sha = _read_recovery_private_bytes(
                repository,
                path,
                f"recovery prior-chain {name}",
                max_bytes=2_000_000,
            )
        else:
            current, current_sha = _read_bound_blob(
                repository,
                path,
                f"recovery prior-chain {name}",
                max_bytes=2_000_000,
                required_mode=0o644,
                required_uid=os.getuid(),
            )
        try:
            relative = path.relative_to(repository).as_posix()
        except ValueError:
            raise ValidationError("recovery prior-chain record is outside repository") from None
        historical = _bound_git(
            bindings,
            ["show", f"{RECOVERY_PRIOR_OUTCOME_COMMIT}:{relative}"],
        )
        if (
            current_sha != expected_sha
            or current != raw
            or historical != raw
            or sha256_bytes(historical) != expected_sha
        ):
            raise ValidationError("recovery prior zero-network chain is not exact at outcome commit")
    committed_evidence = (
        (
            "recovery owner approval",
            contract.owner_approval_path,
            contract.owner_approval_raw,
            contract.owner_approval_sha256,
        ),
        (
            "recovery browser readiness",
            contract.browser_readiness_path,
            contract.browser_readiness_raw,
            contract.browser_readiness_sha256,
        ),
    )
    for label, path, raw, expected_sha in committed_evidence:
        current, current_sha = _read_recovery_private_bytes(
            repository,
            path,
            label,
            max_bytes=10_000_000,
        )
        if current_sha != expected_sha or current != raw:
            raise ValidationError(f"{label} local-private bytes drifted")
        try:
            relative = path.relative_to(repository).as_posix()
        except ValueError:
            raise ValidationError(f"{label} is outside repository") from None
        if _bound_git(bindings, ["show", f"{runtime_commit}:{relative}"]) != raw:
            raise ValidationError(f"{label} is not exact at recovery runtime commit")
        if label == "recovery owner approval" and (
            _bound_git(bindings, ["show", f"{RECOVERY_OWNER_APPROVAL_COMMIT}:{relative}"])
            != raw
        ):
            raise ValidationError("recovery owner approval baseline commit drifted")
    capture_current, capture_sha = _read_recovery_private_capture(
        repository,
        contract.browser_capture_path,
    )
    if (
        capture_current != contract.browser_capture_raw
        or capture_sha != contract.browser_capture_sha256
    ):
        raise ValidationError("recovery local-private browser capture bytes drifted")
    capture_git_state = _verify_recovery_private_capture_git_state(
        bindings,
        repository,
        contract.browser_capture_path,
    )
    capture_git_state = {
        **capture_git_state,
        "sha256": capture_sha,
        "mode": "0600",
        "current_uid": True,
        "link_count": 1,
        "descriptor_identity_stable": True,
    }
    official_current, official_sha = _read_bound_blob(
        repository,
        contract.official_basis_path,
        "recovery official data-use basis",
        max_bytes=1_000_000,
    )
    try:
        official_relative = contract.official_basis_path.relative_to(repository).as_posix()
    except ValueError:
        raise ValidationError("recovery official basis is outside repository") from None
    if (
        official_current != contract.official_basis_raw
        or official_sha != contract.official_basis_sha256
        or _bound_git(bindings, ["show", f"{runtime_commit}:{official_relative}"])
        != contract.official_basis_raw
    ):
        raise ValidationError("recovery official basis is not exact at runtime commit")
    if not allowed_latches <= {
        contract.credential_latch_relative,
        contract.provider_latch_relative,
    }:
        raise ValidationError("recovery source proof latch allowance is invalid")
    dirty = _bound_git(
        bindings,
        ["status", "--porcelain=v1", "--untracked-files=all", "-z"],
    )
    expected_dirty_paths: list[str] = []
    for relative in allowed_latches:
        try:
            expected_dirty_paths.append(
                (contract.root / relative).relative_to(repository).as_posix()
            )
        except ValueError:
            raise ValidationError(
                "recovery source proof latch path is outside repository"
            ) from None
    expected_dirty = b"".join(
        b"?? " + relative.encode("utf-8") + b"\x00"
        for relative in sorted(expected_dirty_paths)
    )
    if dirty != expected_dirty:
        raise ValidationError("Git index and unignored worktree must be exact for recovery execution")
    return {
        "git_head": head,
        "runtime_commit": runtime_commit,
        "prior_outcome_commit": RECOVERY_PRIOR_OUTCOME_COMMIT,
        "remote_state_checked": False,
        "git_network_called": False,
        "head_delta_policy": "exact_active_recovery_authorization_path_only",
        "head_delta_path": authorization_relative,
        "active_authorization_mode": "0600",
        "active_authorization_current_uid": True,
        "active_authorization_link_count": 1,
        "active_authorization_descriptor_identity_stable": True,
        "legacy_latch_reused_or_deleted": False,
        "owner_approval_baseline_commit": RECOVERY_OWNER_APPROVAL_COMMIT,
        "owner_approval_committed_at_runtime": True,
        "browser_readiness_json_committed_at_runtime": True,
        "browser_capture": capture_git_state,
    }


def _preflight_recovery_paths(
    contract: _RecoveryExecutionContract,
    *,
    allow_credential_latch: bool,
    allow_provider_latch: bool,
) -> None:
    entries = (
        (
            "recovery credential-read latch",
            contract.credential_latch_relative,
            ("authorizations", "consumed"),
        ),
        (
            "recovery provider-call latch",
            contract.provider_latch_relative,
            ("authorizations", "consumed"),
        ),
        (
            "recovery success receipt",
            contract.success_relative,
            ("receipts", "elevenlabs-account"),
        ),
        (
            "recovery failure receipt",
            contract.failure_relative,
            ("receipts", "elevenlabs-account"),
        ),
    )
    if len({relative for _label, relative, _prefix in entries}) != len(entries):
        raise ValidationError("recovery destinations must be globally distinct")
    allowed = {
        contract.credential_latch_relative if allow_credential_latch else "",
        contract.provider_latch_relative if allow_provider_latch else "",
    }
    for label, relative, prefix in entries:
        path = contract.root / relative
        if relative in allowed:
            if not path.is_file() or path.is_symlink():
                raise ValidationError(f"{label} expected immutable artifact is absent")
        else:
            path = pt._safe_execution_relative(contract.root, relative, label, ".json")
        if path.relative_to(contract.root).parts[: len(prefix)] != prefix:
            raise ValidationError(f"{label} escaped its exact artifact class")
        parent_fd, _name = pt._open_parent_descriptor(
            contract.root,
            relative,
            create_parents=False,
        )
        os.close(parent_fd)


def _recovery_credential_read_latch(
    contract: _RecoveryExecutionContract,
    consumed_at: datetime,
) -> dict[str, Any]:
    return {
        "schema_version": RECOVERY_CREDENTIAL_READ_CONSUMPTION_SCHEMA,
        "scope": RECOVERY_SCOPE,
        "authorization_id": contract.authorization["authorization_id"],
        "authorization_path": contract.authorization_path.relative_to(contract.root).as_posix(),
        "authorization_sha256": contract.authorization_sha256,
        "owner_approval_sha256": contract.owner_approval_sha256,
        "browser_readiness_sha256": contract.browser_readiness_sha256,
        "prior_failure_chain_sha256": sha256_bytes(_compact(_recovery_prior_failure_chain())),
        "status": "credential_read_attempt_consumed_before_dotenv_read",
        "consumed_at": _iso(consumed_at),
        "credential_preflight_reads_reserved": 1,
        "credential_read_completed_at_latch": False,
        "provider_call_latch_created_at_consumption": False,
        "network_called_at_consumption": False,
        "get_calls_used": 0,
        "post_calls_used": 0,
        "legacy_latch_reused_or_deleted": False,
        "retry_or_resumption": False,
    }


def _recovery_provider_latch(
    contract: _RecoveryExecutionContract,
    consumed_at: datetime,
    *,
    credential_latch_sha256: str,
    credential_fingerprint_sha256: str,
) -> dict[str, Any]:
    return {
        "schema_version": RECOVERY_CONSUMPTION_SCHEMA,
        "scope": RECOVERY_SCOPE,
        "authorization_id": contract.authorization["authorization_id"],
        "authorization_path": contract.authorization_path.relative_to(contract.root).as_posix(),
        "authorization_sha256": contract.authorization_sha256,
        "credential_read_latch_path": contract.credential_latch_relative,
        "credential_read_latch_sha256": credential_latch_sha256,
        "owner_approval_sha256": contract.owner_approval_sha256,
        "browser_readiness_sha256": contract.browser_readiness_sha256,
        "credential_fingerprint_sha256": credential_fingerprint_sha256,
        "browser_suffix_sha256": contract.expected_preview_sha256,
        "status": "provider_get_authority_consumed_after_credential_readiness",
        "consumed_at": _iso(consumed_at),
        "credential_preflight_reads_used": 1,
        "execution_credential_reads_used": 0,
        "browser_suffix_matches_held_credential": True,
        "network_called_at_consumption": False,
        "get_calls_used": 0,
        "post_calls_used": 0,
        "legacy_latch_reused_or_deleted": False,
        "retry_permitted": False,
    }


def _safe_recovery_document(
    document: dict[str, Any],
    *,
    secret_values: tuple[str, ...] = (),
) -> bytes:
    raw = _receipt_bytes(document)
    if pt._scan_for_secrets(document):
        raise ValidationError("recovery persistence document failed structural secret scan")
    for value in secret_values:
        if value and value.encode("utf-8") in raw:
            raise ValidationError("recovery persistence document contains forbidden raw material")
    return raw


def _parse_recovery_account_payload(
    raw: bytes,
    api_key: str,
    suffix: str,
) -> tuple[bool, str, str]:
    """Validate `/v1/user` without deriving any persistent account identifier."""

    payload: dict[str, Any] | None = None
    user_id = ""
    user_value: Any = None
    echoed_key: Any = None
    echoed_suffix: Any = None
    key_echo_state = "absent_or_null"
    suffix_echo_state = "absent_or_null"
    failure_code: str | None = None
    result: tuple[bool, str, str] | None = None
    try:
        try:
            payload = pt._strict_json_bytes(raw, "ElevenLabs recovery /v1/user response")
        except Exception:
            raise _eleven_failure("account_response_json_invalid", response_received=True) from None
        user_value = payload.get("user_id")
        if (
            not isinstance(user_value, str)
            or not 1 <= len(user_value) <= 256
            or user_value != user_value.strip()
            or any(ord(character) < 33 or ord(character) > 126 for character in user_value)
        ):
            raise _eleven_failure("account_user_id_invalid", response_received=True)
        user_id = user_value
        echoed_key = payload.get("xi_api_key")
        if echoed_key is not None and (not isinstance(echoed_key, str) or echoed_key != api_key):
            raise _eleven_failure("account_optional_api_key_echo_mismatch", response_received=True)
        if echoed_key is not None:
            key_echo_state = "present_exact_match"
        echoed_suffix = payload.get("xi_api_key_preview")
        if echoed_suffix is not None:
            if (
                not isinstance(echoed_suffix, str)
                or not 1 <= len(echoed_suffix) <= 256
                or any(ord(character) < 32 or ord(character) > 126 for character in echoed_suffix)
                or not echoed_suffix.endswith(suffix)
            ):
                raise _eleven_failure("account_optional_api_key_preview_invalid", response_received=True)
            suffix_echo_state = "present_last4_match"
        result = (True, key_echo_state, suffix_echo_state)
    except pt._GuideExecutionFailure as exc:
        failure_code = exc.code
        exc.__cause__ = None
        exc.__context__ = None
        exc.__suppress_context__ = True
        exc.__traceback__ = None
    finally:
        raw = b""
        api_key = ""
        suffix = ""
        payload = None
        user_id = ""
        user_value = None
        echoed_key = None
        echoed_suffix = None
        key_echo_state = ""
        suffix_echo_state = ""
    if failure_code is not None:
        pending = _eleven_failure(failure_code, response_received=True)
        pending.__cause__ = None
        pending.__context__ = None
        pending.__suppress_context__ = True
        pending.__traceback__ = None
        failure_code = None
        result = None
        raise pending from None
    if result is None:
        raise _eleven_failure("account_response_validation_failed", response_received=True) from None
    return result


def execute_account_recovery(
    authorization_path: Path,
    *,
    timeout: float = 30.0,
) -> dict[str, Any]:
    """Consume two isolated latches around one dotenv read and one `/v1/user` GET."""

    if type(timeout) not in {int, float} or not 0 < float(timeout) <= ACCOUNT_MAX_ELAPSED_SECONDS:
        raise ValidationError("account-recovery timeout must be >0 and <=30 seconds")
    contract = _build_recovery_contract(authorization_path)
    _preflight_tls_environment()
    _preflight_recovery_paths(
        contract,
        allow_credential_latch=False,
        allow_provider_latch=False,
    )
    source_proof = _verify_recovery_committed_source(contract, allowed_latches=frozenset())
    # All nonsecret gates are checked before the immutable credential-read latch.
    refreshed = _build_recovery_contract(authorization_path)
    if _recovery_contract_snapshot(refreshed) != _recovery_contract_snapshot(contract):
        raise ValidationError("account-recovery source changed before credential-read consumption")
    _verify_recovery_committed_source(refreshed, allowed_latches=frozenset())
    _preflight_recovery_paths(
        contract,
        allow_credential_latch=False,
        allow_provider_latch=False,
    )
    _verify_recovery_active_authority_private(contract)
    credential_latched_at = _execution_now()
    if not contract.approved_at <= credential_latched_at < contract.expires_at:
        raise ValidationError("account-recovery authority expired before credential-read consumption")
    credential_latch = _recovery_credential_read_latch(contract, credential_latched_at)
    credential_latch_bytes = _safe_recovery_document(credential_latch)
    pt._exclusive_fixture_write(
        contract.root,
        contract.credential_latch_relative,
        credential_latch_bytes,
    )
    credential_latch_sha = sha256_bytes(credential_latch_bytes)

    api_key = ""
    key_fingerprint = ""
    key_suffix = ""
    credential_accessed = False
    network_called = False
    get_calls = 0
    provider_latch_bytes = b""
    provider_latch_sha: str | None = None
    provider_latch_created = False
    response: _ElevenResponse | None = None
    started_at: datetime | None = None
    completed_at: datetime | None = None
    failure: pt._GuideExecutionFailure | None = None
    credential_read_failure: pt._GuideExecutionFailure | None = None
    pending_read_failure: pt._GuideExecutionFailure | None = None
    pending_parse_failure: pt._GuideExecutionFailure | None = None
    parse_failure_code: str | None = None
    provider_latch: dict[str, Any] = {}
    run: dict[str, Any] = {}
    run_bytes = b""
    failure_bytes = b""
    try:
        pt._verify_private_fixture_artifact(
            contract.root,
            contract.credential_latch_relative,
            credential_latch_bytes,
            "recovery credential-read latch",
        )
        _verify_recovery_private_latch(
            contract,
            contract.credential_latch_relative,
            credential_latch_bytes,
            "recovery credential-read latch",
        )
        _verify_recovery_committed_source(
            contract,
            allowed_latches=frozenset({contract.credential_latch_relative}),
        )
        credential_accessed = True
        try:
            api_key = _read_recovery_dotenv_key()
        except ValidationError as exc:
            exc.__cause__ = None
            exc.__context__ = None
            exc.__suppress_context__ = True
            exc.__traceback__ = None
            credential_read_failure = _eleven_failure("credential_preflight_read_failed")
        if credential_read_failure is not None:
            pending_read_failure = credential_read_failure
            credential_read_failure = None
            raise pending_read_failure from None
        key_fingerprint = _key_fingerprint(api_key)
        if len(api_key) < 4 or not re.fullmatch(r"[A-Za-z0-9]{4}", api_key[-4:]):
            raise _eleven_failure("credential_suffix_shape_unavailable")
        key_suffix = api_key[-4:]
        if _preview_hash(key_suffix) != contract.expected_preview_sha256:
            raise _eleven_failure("credential_suffix_does_not_match_fresh_browser_readiness")

        # Rebuild every authority/evidence binding without re-reading the dotenv.
        refreshed = _build_recovery_contract(authorization_path)
        if _recovery_contract_snapshot(refreshed) != _recovery_contract_snapshot(contract):
            raise _eleven_failure("recovery_source_drift_after_credential_read")
        _verify_recovery_committed_source(
            refreshed,
            allowed_latches=frozenset({contract.credential_latch_relative}),
        )
        pt._verify_private_fixture_artifact(
            contract.root,
            contract.credential_latch_relative,
            credential_latch_bytes,
            "recovery credential-read latch",
        )
        _verify_recovery_private_latch(
            contract,
            contract.credential_latch_relative,
            credential_latch_bytes,
            "recovery credential-read latch",
        )
        _preflight_recovery_paths(
            contract,
            allow_credential_latch=True,
            allow_provider_latch=False,
        )
        _verify_recovery_active_authority_private(contract)
        provider_latched_at = _execution_now()
        if not credential_latched_at <= provider_latched_at < contract.expires_at:
            raise _eleven_failure("authorization_expired_before_provider_latch")
        provider_latch = _recovery_provider_latch(
            contract,
            provider_latched_at,
            credential_latch_sha256=credential_latch_sha,
            credential_fingerprint_sha256=key_fingerprint,
        )
        provider_latch_bytes = _safe_recovery_document(
            provider_latch,
            secret_values=(api_key, key_suffix),
        )
        pt._exclusive_fixture_write(
            contract.root,
            contract.provider_latch_relative,
            provider_latch_bytes,
        )
        provider_latch_sha = sha256_bytes(provider_latch_bytes)
        provider_latch_created = True

        refreshed = _build_recovery_contract(authorization_path)
        if _recovery_contract_snapshot(refreshed) != _recovery_contract_snapshot(contract):
            raise _eleven_failure("recovery_source_drift_after_provider_latch")
        _verify_recovery_committed_source(
            refreshed,
            allowed_latches=frozenset(
                {contract.credential_latch_relative, contract.provider_latch_relative}
            ),
        )
        pt._verify_private_fixture_artifact(
            contract.root,
            contract.credential_latch_relative,
            credential_latch_bytes,
            "recovery credential-read latch",
        )
        pt._verify_private_fixture_artifact(
            contract.root,
            contract.provider_latch_relative,
            provider_latch_bytes,
            "recovery provider-call latch",
        )
        _preflight_recovery_paths(
            contract,
            allow_credential_latch=True,
            allow_provider_latch=True,
        )
        _verify_recovery_active_authority_private(contract)
        _verify_recovery_private_latch(
            contract,
            contract.credential_latch_relative,
            credential_latch_bytes,
            "recovery credential-read latch",
        )
        _verify_recovery_private_latch(
            contract,
            contract.provider_latch_relative,
            provider_latch_bytes,
            "recovery provider-call latch",
        )
        started_at = _execution_now()
        if (
            started_at < contract.browser_observed_at
            or (started_at - contract.browser_observed_at).total_seconds()
            > ACCOUNT_VERIFICATION_MAX_AGE_SECONDS
        ):
            raise _eleven_failure("fresh_browser_readiness_stale_before_recovery_get")
        if not provider_latched_at <= started_at < contract.expires_at:
            raise _eleven_failure("authorization_expired_before_recovery_get")
        get_calls = 1
        network_called = True
        response = _perform_elevenlabs_request(
            method="GET",
            url=ACCOUNT_ENDPOINT,
            api_key=api_key,
            timeout=float(timeout),
            accept="application/json",
            body=None,
            content_type=None,
            response_cap=ACCOUNT_MAX_RESPONSE_BYTES,
            expected_mimes=frozenset({"application/json"}),
        )
        completed_at = _execution_now()
        if not started_at <= completed_at < contract.expires_at:
            raise _eleven_failure("recovery_response_completed_outside_authority")
        try:
            valid_user_id_present, key_echo_state, suffix_echo_state = _parse_recovery_account_payload(
                response.payload,
                api_key,
                key_suffix,
            )
        except pt._GuideExecutionFailure as parse_failure:
            parse_failure_code = parse_failure.code
            parse_failure.__cause__ = None
            parse_failure.__context__ = None
            parse_failure.__suppress_context__ = True
            parse_failure.__traceback__ = None
        if parse_failure_code is not None:
            pending_parse_failure = _eleven_failure(
                parse_failure_code,
                response_received=True,
                http_status=200,
                response_bytes=response.response_bytes,
                response_sha256=response.response_sha256,
            )
            parse_failure_code = None
            raise pending_parse_failure from None
        run = {
            "schema_version": RECOVERY_RUN_SCHEMA,
            "provider": "elevenlabs",
            "scope": RECOVERY_SCOPE,
            "outcome": "success",
            "endpoint": ACCOUNT_ENDPOINT,
            "method": "GET",
            "accept": "application/json",
            "accept_encoding": "identity",
            "authorization_id": contract.authorization["authorization_id"],
            "authorization_path": contract.authorization_path.relative_to(contract.root).as_posix(),
            "authorization_sha256": contract.authorization_sha256,
            "credential_read_latch_path": contract.credential_latch_relative,
            "credential_read_latch_sha256": credential_latch_sha,
            "provider_call_latch_path": contract.provider_latch_relative,
            "provider_call_latch_sha256": provider_latch_sha,
            "owner_approval_sha256": contract.owner_approval_sha256,
            "browser_readiness_sha256": contract.browser_readiness_sha256,
            "prior_failure_chain_sha256": sha256_bytes(_compact(_recovery_prior_failure_chain())),
            "source_proof": source_proof,
            "credential_fingerprint_sha256": key_fingerprint,
            "browser_suffix_sha256": contract.expected_preview_sha256,
            "http_status": 200,
            "response_bytes": response.response_bytes,
            "response_mime_type": response.content_type,
            "response_content_encoding": response.content_encoding,
            "valid_user_id_present": valid_user_id_present,
            "credential_read_from_fixed_dotenv": True,
            "environment_inheritance_used": False,
            "shell_source_used": False,
            "dotenv_reread_after_credential_latch": False,
            "browser_suffix_matches_held_credential": True,
            "provider_key_echo_state": key_echo_state,
            "provider_suffix_echo_state": suffix_echo_state,
            "account_linkage_strength": "contextual_non_cryptographic",
            "exact_ui_api_account_equality_claimed": False,
            "raw_response_stored": False,
            "raw_account_data_stored": False,
            "account_data_stored": False,
            "response_hash_stored": False,
            "response_derived_identifier_stored": False,
            "raw_credential_stored": False,
            "raw_credential_suffix_stored": False,
            "raw_user_identifier_stored": False,
            "provider_get_calls_made": 1,
            "provider_post_calls_made": 0,
            "retries_made": 0,
            "redirects_followed": 0,
            "retry_permitted": False,
            "redirect_permitted": False,
            "fallback_permitted": False,
            "fallback_used": False,
            "account_settings_changed": False,
            "audio_uploaded": False,
            "spend_incurred": False,
            "voice_transfer_authorized": False,
            "audio_upload_authorized": False,
            "full_capture_authorized": False,
            "creative_approved": False,
            "step2_lock_authorized": False,
            "step3_authorized": False,
            "sharing_authorized": False,
            "publication_authorized": False,
            "started_at": _iso(started_at),
            "completed_at": _iso(completed_at),
        }
        run_bytes = _safe_recovery_document(
            run,
            secret_values=(api_key, key_suffix),
        )
        if response.payload in run_bytes:
            raise pt._GuideExecutionFailure("recovery_run_contains_raw_account_response")
        pt._exclusive_fixture_write(contract.root, contract.success_relative, run_bytes)
        result = {
            "schema_version": RECOVERY_RESULT_SCHEMA,
            "valid": True,
            "outcome": "success",
            "authorization_consumed": True,
            "credential_read_consumed": True,
            "provider_get_authority_consumed": True,
            "provider_get_calls_made": 1,
            "provider_post_calls_made": 0,
            "run_receipt": {
                "path": contract.success_relative,
                "sha256": sha256_bytes(run_bytes),
            },
            "network_called": True,
            "retry_permitted": False,
            "redirect_permitted": False,
            "fallback_permitted": False,
            "fallback_used": False,
            "raw_sensitive_material_persisted": False,
            "account_data_stored": False,
            "response_hash_stored": False,
            "response_derived_identifier_stored": False,
            "account_settings_changed": False,
            "voice_transfer_authorized": False,
            "audio_upload_authorized": False,
            "full_capture_authorized": False,
            "creative_approved": False,
            "step2_lock_authorized": False,
            "step3_authorized": False,
            "sharing_authorized": False,
            "publication_authorized": False,
        }
        api_key = ""
        key_fingerprint = ""
        key_suffix = ""
        response = None
        run = {}
        run_bytes = b""
        return result
    except pt._GuideExecutionFailure as exc:
        exc.__cause__ = None
        exc.__context__ = None
        exc.__suppress_context__ = True
        exc.__traceback__ = None
        failure = exc
    except ValidationError as exc:
        exc.__cause__ = None
        exc.__context__ = None
        exc.__suppress_context__ = True
        exc.__traceback__ = None
        failure = _eleven_failure(
            "local_validation_or_filesystem_failure",
            response_received=response is not None,
            http_status=200 if response is not None else None,
            response_bytes=response.response_bytes if response is not None else 0,
            response_sha256=response.response_sha256 if response is not None else None,
        )
    except Exception as exc:
        exc.__cause__ = None
        exc.__context__ = None
        exc.__suppress_context__ = True
        exc.__traceback__ = None
        failure = _eleven_failure(
            "unexpected_local_failure",
            response_received=response is not None,
            http_status=200 if response is not None else None,
            response_bytes=response.response_bytes if response is not None else 0,
            response_sha256=response.response_sha256 if response is not None else None,
        )
    if failure is None:
        failure = _eleven_failure("unknown_failure")
    failed_at = _execution_now()
    failure_document = {
        "schema_version": RECOVERY_FAILURE_SCHEMA,
        "provider": "elevenlabs",
        "scope": RECOVERY_SCOPE,
        "outcome": "failed_closed",
        "endpoint": ACCOUNT_ENDPOINT,
        "method": "GET",
        "authorization_id": contract.authorization["authorization_id"],
        "authorization_path": contract.authorization_path.relative_to(contract.root).as_posix(),
        "authorization_sha256": contract.authorization_sha256,
        "credential_read_latch_path": contract.credential_latch_relative,
        "credential_read_latch_sha256": credential_latch_sha,
        "provider_call_latch_created": provider_latch_created,
        "provider_call_latch_path": (
            contract.provider_latch_relative if provider_latch_created else None
        ),
        "provider_call_latch_sha256": provider_latch_sha,
        "owner_approval_sha256": contract.owner_approval_sha256,
        "browser_readiness_sha256": contract.browser_readiness_sha256,
        "prior_failure_chain_sha256": sha256_bytes(_compact(_recovery_prior_failure_chain())),
        "source_proof": source_proof,
        "failure_code": failure.code,
        "http_status": failure.http_status,
        "response_bytes": failure.response_bytes,
        "response_mime_type": response.content_type if response is not None else None,
        "response_content_encoding": response.content_encoding if response is not None else None,
        "provider_response_received": bool(
            getattr(failure, "response_received", False) or response is not None
        ),
        "provider_get_receipt_state": (
            "confirmed_response"
            if getattr(failure, "response_received", False) or response is not None
            else ("ambiguous_transport" if get_calls else "not_attempted")
        ),
        "credential_read_consumed": True,
        "credential_accessed": credential_accessed,
        "network_called": network_called,
        "provider_get_attempts_consumed": get_calls,
        "provider_post_attempts_consumed": 0,
        "retry_permitted": False,
        "redirect_permitted": False,
        "fallback_permitted": False,
        "fallback_used": False,
        "raw_response_stored": False,
        "raw_account_data_stored": False,
        "account_data_stored": False,
        "response_hash_stored": False,
        "response_derived_identifier_stored": False,
        "raw_credential_stored": False,
        "raw_credential_suffix_stored": False,
        "raw_user_identifier_stored": False,
        "account_settings_changed": False,
        "audio_uploaded": False,
        "spend_incurred": False,
        "voice_transfer_authorized": False,
        "audio_upload_authorized": False,
        "full_capture_authorized": False,
        "creative_approved": False,
        "step2_lock_authorized": False,
        "step3_authorized": False,
        "sharing_authorized": False,
        "publication_authorized": False,
        "started_at": _iso(started_at) if started_at else None,
        "failed_at": _iso(failed_at),
    }
    try:
        failure_bytes = _safe_recovery_document(
            failure_document,
            secret_values=(api_key, key_suffix),
        )
        pt._exclusive_fixture_write(contract.root, contract.failure_relative, failure_bytes)
    except ValidationError:
        pass
    code = failure.code
    api_key = ""
    key_fingerprint = ""
    key_suffix = ""
    response = None
    provider_latch_bytes = b""
    credential_latch_bytes = b""
    failure = None
    failure_document = {}
    failure_bytes = b""
    credential_latch = {}
    provider_latch = {}
    run = {}
    run_bytes = b""
    pending_read_failure = None
    pending_parse_failure = None
    credential_read_failure = None
    parse_failure_code = None
    refreshed = None
    source_proof = {}
    contract = None
    raise ValidationError(f"ElevenLabs account recovery stopped without retry: {code}") from None


# ---------------------------------------------------------------------------
# Recovery-evidence Voice Changer transaction
# ---------------------------------------------------------------------------


def _recovery_transfer_runtime_files() -> dict[str, tuple[str, Path]]:
    """Runtime surface owned only by the additive isolated-worker branch."""

    narration_root = Path(__file__).resolve().parents[2]
    package = narration_root / "runtime" / "oe_narration"
    tests = narration_root / "runtime" / "tests"
    schemas = narration_root / "schemas"
    prefix = "operator-blueprint-v2/02-narration-production/"
    return {
        "voice_transfer_runtime": (
            prefix + "runtime/oe_narration/voice_transfer.py",
            package / "voice_transfer.py",
        ),
        "transfer_worker_runtime": (
            prefix + "runtime/oe_narration/elevenlabs_transfer_worker.py",
            package / "elevenlabs_transfer_worker.py",
        ),
        "performance_transfer_runtime": (
            prefix + "runtime/oe_narration/performance_transfer.py",
            package / "performance_transfer.py",
        ),
        "cli_runtime": (prefix + "runtime/oe_narration/cli.py", package / "cli.py"),
        "core_runtime": (prefix + "runtime/oe_narration/core.py", package / "core.py"),
        "audio_runtime": (prefix + "runtime/oe_narration/audio.py", package / "audio.py"),
        "init_runtime": (prefix + "runtime/oe_narration/__init__.py", package / "__init__.py"),
        "recovery_transfer_schema": (
            prefix
            + "schemas/elevenlabs-recovery-evidence-voice-transfer-authorization.schema.json",
            schemas
            / "elevenlabs-recovery-evidence-voice-transfer-authorization.schema.json",
        ),
        "voice_transfer_tests": (
            prefix + "runtime/tests/test_voice_transfer.py",
            tests / "test_voice_transfer.py",
        ),
        "transfer_worker_tests": (
            prefix + "runtime/tests/test_elevenlabs_transfer_worker.py",
            tests / "test_elevenlabs_transfer_worker.py",
        ),
        "capture_audio_tests": (
            prefix + "runtime/tests/test_capture_audio.py",
            tests / "test_capture_audio.py",
        ),
    }


def expected_recovery_transfer_runtime_bindings(*, draft: bool) -> dict[str, Any]:
    del draft
    result: dict[str, Any] = {"state": "verified", "git_commit": "pending"}
    for name, (_relative, path) in _recovery_transfer_runtime_files().items():
        result[f"{name}_sha256"] = sha256_file(path)
    git_path, git_sha = _read_git_identity()
    ffprobe_path, ffprobe_sha = _read_ffprobe_identity()
    ffmpeg_path, ffmpeg_sha = _read_ffmpeg_identity()
    result.update(
        {
            "git_binary_path": git_path,
            "git_binary_sha256": git_sha,
            "git_version": _read_git_version(git_path, git_sha),
            "worker_interpreter_path": _TRANSFER_WORKER_INTERPRETER_PATH,
            "worker_interpreter_sha256": _TRANSFER_WORKER_INTERPRETER_SHA256,
            "worker_interpreter_version": _TRANSFER_WORKER_INTERPRETER_VERSION,
            "worker_interpreter_mode": _TRANSFER_WORKER_INTERPRETER_MODE,
            "worker_interpreter_uid": _TRANSFER_WORKER_INTERPRETER_UID,
            "worker_interpreter_nlink": _TRANSFER_WORKER_INTERPRETER_NLINK,
            "ffprobe_binary_path": ffprobe_path,
            "ffprobe_binary_sha256": ffprobe_sha,
            "ffprobe_version": _read_ffprobe_version(ffprobe_path, ffprobe_sha),
            "ffmpeg_binary_path": ffmpeg_path,
            "ffmpeg_binary_sha256": ffmpeg_sha,
            "ffmpeg_version": _read_ffmpeg_version(ffmpeg_path, ffmpeg_sha),
        }
    )
    return result


def _recovery_transfer_bindings(plan_dry: dict[str, Any]) -> dict[str, Any]:
    return {
        **_base_transfer_bindings(plan_dry),
        "primary_request_sha256": TRANSFER_OPT_OUT_REQUEST_SHA256,
        "multipart_content_type": TRANSFER_CONTENT_TYPE,
        "enable_logging": True,
        "normalized_http_request_sha256": TRANSFER_OPT_OUT_NORMALIZED_REQUEST_SHA256,
    }


def _recovery_transfer_prerequisites(active: bool) -> dict[str, Any]:
    names = (
        "selected_guide",
        "guide_qa",
        "owner_selection",
        "owner_audition_confirmation",
        "elevenlabs_data_use",
        "target_voice_rights",
        "official_media_contract",
    )
    if not active:
        return {name: {"state": "pending"} for name in names}
    # ACTIVE paths and hashes are supplied by the independently reviewed
    # authorization and then descriptor/hash/semantic checked at runtime.
    return {name: None for name in names}


def _recovery_transfer_account_evidence(
    active: bool,
    *,
    assurance_sha256: str | None = None,
) -> dict[str, Any]:
    if not active:
        return {"state": "pending"}
    return {
        "state": "verified",
        "calibrated_account_assurance": {
            "state": "verified",
            "path": RECOVERY_TRANSFER_ACCOUNT_ASSURANCE_PATH,
            "sha256": assurance_sha256,
        },
        "credential_authentication_inference": (
            RECOVERY_TRANSFER_AUTHENTICATION_INFERENCE_STATE
        ),
        "authentication_conclusion": RECOVERY_TRANSFER_AUTHENTICATION_CONCLUSION,
        "response_body_contents_state": "unknown_not_read",
        "account_data_observed": False,
        "identity_observed": False,
        "valid_user_id_observed": False,
        "subscription_state_observed": False,
        "target_voice_accessibility_state": "unknown",
        "ui_api_account_equality_state": "unknown",
        "exact_ui_api_account_equality_verified": False,
        "exact_ui_api_account_equality_claimed": False,
        "account_verified_claimed": False,
        "second_account_get_authorized": False,
    }


def _recovery_transfer_credential_delivery(
    active: bool,
    *,
    fingerprint: str | None = None,
    suffix_sha256: str | None = None,
) -> dict[str, Any]:
    base = {
        "state": "verified" if active else "pending",
        "mechanism": "post_latch_descriptor_read_fixed_dotenv_exact_assignment",
        "dotenv_path": str(RECOVERY_DOTENV_PATH),
        "assignment_name": API_KEY_ENV,
    }
    if not active:
        return base
    return {
        **base,
        "required_file_type": "regular",
        "required_mode": "0600",
        "current_uid_required": True,
        "required_link_count": 1,
        "max_file_bytes": RECOVERY_DOTENV_MAX_BYTES,
        "max_assignment_count": 1,
        "environment_inheritance_used": False,
        "shell_source_forbidden": True,
        "dotenv_reread_forbidden": True,
        "domain_separation": API_KEY_DOMAIN_TEXT,
        "api_key_fingerprint_sha256": fingerprint,
        "browser_suffix_sha256": suffix_sha256,
    }


def _recovery_transfer_consumption(active: bool) -> dict[str, Any]:
    return {
        "status": "unconsumed" if active else "not_authorized",
        "generation_post_calls_used": 0,
        "outputs_received": 0,
        "spend_used_usd": 0,
        "record_path": TRANSFER_SCOPE_LATCH_PATH,
        "shared_global_transfer_latch": True,
    }


def _recovery_transfer_zero_authority() -> dict[str, bool]:
    """Exact denial block shared by each standalone evidence record."""

    return {
        "this_record_authorizes_provider_action": False,
        "credential_access_authorized": False,
        "network_authorized": False,
        "account_get_authorized": False,
        "generation_post_authorized": False,
        "account_mutation_authorized": False,
        "audio_upload_authorized": False,
        "spend_authorized": False,
        "voice_transfer_authorized": False,
        "creative_approval_conferred": False,
        "step2_lock_authorized": False,
        "step3_authorized": False,
        "sharing_authorized": False,
        "publication_authorized": False,
    }


def _recovery_transfer_scope_approval() -> dict[str, Any]:
    """Calibrate owner scope separately from later machine materialization."""

    return {
        "owner": RECOVERY_TRANSFER_OWNER,
        "sole_exact_provider_action_authority": {
            "path": RECOVERY_TRANSFER_OWNER_APPROVAL_PATH,
            "sha256": RECOVERY_TRANSFER_OWNER_APPROVAL_SHA256,
        },
        "approval_event_timestamp_available": False,
        "later_draft_and_active_bytes_owner_reviewed": False,
        "implementation_only_narrows_or_enforces_c907": True,
        "c907_alone_confers_runtime_execution_authority": False,
        "new_owner_prompt_required": False,
    }


def _verify_recovery_transfer_selected_guide_git_state(
    runtime_bindings: dict[str, Any],
    repository: Path,
    root: Path,
    selected_path: Path,
) -> None:
    """Prove candidate B is local-only under the committed fixture ignore rule."""

    try:
        relative = selected_path.relative_to(repository).as_posix()
        ignore_path = root / ".gitignore"
        ignore_relative = ignore_path.relative_to(repository).as_posix()
    except ValueError:
        raise ValidationError("recovery-evidence selected guide is outside repository") from None
    if _bound_git(runtime_bindings, ["ls-files", "--stage", "--", relative]):
        raise ValidationError("recovery-evidence selected guide must remain untracked")
    try:
        ignored = _bound_git(
            runtime_bindings,
            ["check-ignore", "--no-index", "-v", "--", relative],
        ).decode("utf-8", errors="strict")
    except (UnicodeError, ValidationError):
        raise ValidationError("recovery-evidence selected guide ignore proof failed") from None
    if ignored != f"{ignore_relative}:1:outputs/raw/\t{relative}\n":
        raise ValidationError(
            "recovery-evidence selected guide must use exact fixture outputs/raw ignore"
        )
    ignore_raw, ignore_sha = _read_bound_blob(
        repository,
        ignore_path,
        "recovery-evidence fixture gitignore",
        max_bytes=65_536,
    )
    runtime_commit = runtime_bindings.get("git_commit")
    if not isinstance(runtime_commit, str) or not _GIT_SHA_RE.fullmatch(runtime_commit):
        raise ValidationError("recovery-evidence selected guide runtime commit is invalid")
    for commit_value in (RECOVERY_TRANSFER_OUTCOME_COMMIT, runtime_commit):
        if _bound_git(
            runtime_bindings,
            ["ls-tree", "--name-only", commit_value, "--", relative],
        ):
            raise ValidationError("recovery-evidence selected guide appears in Git history")
        committed_ignore = _bound_git(
            runtime_bindings,
            ["show", f"{commit_value}:{ignore_relative}"],
            max_bytes=65_536,
        )
        if committed_ignore != ignore_raw or sha256_bytes(committed_ignore) != ignore_sha:
            raise ValidationError("recovery-evidence fixture gitignore drifted")


def _validate_recovery_transfer_runtime_bindings(
    value: Any,
    *,
    active: bool,
    errors: list[str],
) -> dict[str, Any]:
    expected_keys = {"state"}
    if active:
        expected_keys |= {
            "git_commit",
            "git_binary_path",
            "git_binary_sha256",
            "git_version",
            "worker_interpreter_path",
            "worker_interpreter_sha256",
            "worker_interpreter_version",
            "worker_interpreter_mode",
            "worker_interpreter_uid",
            "worker_interpreter_nlink",
            "ffprobe_binary_path",
            "ffprobe_binary_sha256",
            "ffprobe_version",
            "ffmpeg_binary_path",
            "ffmpeg_binary_sha256",
            "ffmpeg_version",
            *(f"{name}_sha256" for name in _recovery_transfer_runtime_files()),
        }
    item = _strict(value, expected_keys, "recovery-evidence transfer runtime_bindings")
    if not active:
        if item != {"state": "pending"}:
            errors.append("draft recovery-evidence transfer runtime must remain pending")
        return item
    commit = item.get("git_commit")
    if (
        item.get("state") != "verified"
        or not isinstance(commit, str)
        or not _GIT_SHA_RE.fullmatch(commit)
    ):
        errors.append("active recovery-evidence transfer runtime requires a Git commit")
    try:
        repository = pt._guide_repository_root()
    except ValidationError:
        repository = Path("/invalid-recovery-transfer-repository")
        errors.append("recovery-evidence transfer repository identity is unavailable")
    for name, (_relative, path) in _recovery_transfer_runtime_files().items():
        expected_sha = item.get(f"{name}_sha256")
        try:
            _current, current_sha = _read_bound_blob(
                repository,
                path,
                f"recovery-evidence transfer runtime {name}",
                max_bytes=5_000_000,
            )
        except ValidationError:
            current_sha = None
        if (
            not isinstance(expected_sha, str)
            or not _SHA_RE.fullmatch(expected_sha)
            or current_sha != expected_sha
        ):
            errors.append(f"recovery-evidence transfer runtime {name} bytes drifted")
    try:
        interpreter = _system_transfer_worker_interpreter_identity()
        git_path, git_sha = _read_git_identity(item.get("git_binary_path"))
        ffprobe_path, ffprobe_sha = _read_ffprobe_identity(item.get("ffprobe_binary_path"))
        ffmpeg_path, ffmpeg_sha = _read_ffmpeg_identity(item.get("ffmpeg_binary_path"))
    except ValidationError:
        errors.append("recovery-evidence transfer executable binding is unavailable")
    else:
        interpreter_info = os.stat(interpreter[0], follow_symlinks=False)
        if (
            item.get("worker_interpreter_path") != interpreter[0]
            or item.get("worker_interpreter_sha256") != interpreter[1]
            or item.get("worker_interpreter_version") != interpreter[2]
            or item.get("worker_interpreter_mode") != stat.S_IMODE(interpreter_info.st_mode)
            or item.get("worker_interpreter_uid") != interpreter_info.st_uid
            or item.get("worker_interpreter_nlink") != interpreter_info.st_nlink
            or item.get("git_binary_path") != git_path
            or item.get("git_binary_sha256") != git_sha
            or item.get("git_version") != _read_git_version(git_path, git_sha)
            or item.get("ffprobe_binary_path") != ffprobe_path
            or item.get("ffprobe_binary_sha256") != ffprobe_sha
            or item.get("ffprobe_version") != _read_ffprobe_version(ffprobe_path, ffprobe_sha)
            or item.get("ffmpeg_binary_path") != ffmpeg_path
            or item.get("ffmpeg_binary_sha256") != ffmpeg_sha
            or item.get("ffmpeg_version") != _read_ffmpeg_version(ffmpeg_path, ffmpeg_sha)
        ):
            errors.append("recovery-evidence transfer executable identity drifted")
    if isinstance(commit, str) and _GIT_SHA_RE.fullmatch(commit):
        try:
            _verify_local_git_object_store(item)
            _bound_git(item, ["cat-file", "-e", f"{commit}^{{commit}}"])
            r0_parents = _bound_git(
                item,
                ["rev-list", "--parents", "-n", "1", commit],
            ).strip().split()
            if r0_parents != [
                commit.encode("ascii"),
                RECOVERY_TRANSFER_OUTCOME_COMMIT.encode("ascii"),
            ]:
                raise ValidationError(
                    "recovery-evidence transfer R0 must directly follow the outcome commit"
                )
            r0_delta = _bound_git(
                item,
                [
                    "diff", "--no-ext-diff", "--no-textconv", "--no-renames",
                    "--name-status", "--diff-filter=ACDMRTUXB", "-z",
                    f"{RECOVERY_TRANSFER_OUTCOME_COMMIT}..{commit}",
                ],
            )
            r0_parts = r0_delta.split(b"\x00")
            if not r0_parts or r0_parts[-1] != b"" or (len(r0_parts) - 1) % 2:
                raise ValidationError("recovery-evidence transfer R0 delta is malformed")
            r0_entries = list(zip(r0_parts[0:-1:2], r0_parts[1:-1:2]))
            try:
                r0_paths = [path.decode("utf-8") for _status, path in r0_entries]
            except UnicodeError:
                raise ValidationError("recovery-evidence transfer R0 paths are invalid") from None
            allowed_r0_paths = {
                relative for relative, _path in _recovery_transfer_runtime_files().values()
            }
            required_r0_paths = {
                _recovery_transfer_runtime_files()[name][0]
                for name in (
                    "voice_transfer_runtime", "transfer_worker_runtime",
                    "cli_runtime", "audio_runtime", "init_runtime",
                    "recovery_transfer_schema", "voice_transfer_tests",
                    "transfer_worker_tests", "capture_audio_tests",
                )
            }
            if (
                any(status not in {b"A", b"M"} for status, _path in r0_entries)
                or len(r0_paths) != len(set(r0_paths))
                or not set(r0_paths) <= allowed_r0_paths
                or not required_r0_paths <= set(r0_paths)
            ):
                raise ValidationError("recovery-evidence transfer R0 delta is not exact")
            head = _bound_git(item, ["rev-parse", "HEAD"]).strip()
            if not re.fullmatch(rb"[0-9a-f]{40}", head):
                raise ValidationError("recovery-evidence transfer HEAD is invalid")
            _bound_git(
                item,
                ["merge-base", "--is-ancestor", commit, head.decode("ascii")],
            )
            for name, (relative, path) in _recovery_transfer_runtime_files().items():
                committed = _bound_git(item, ["show", f"{commit}:{relative}"], max_bytes=5_000_000)
                expected_sha = item.get(f"{name}_sha256")
                current, current_sha = _read_bound_blob(
                    repository,
                    path,
                    f"recovery-evidence transfer bound R0 runtime {name}",
                    max_bytes=5_000_000,
                )
                if (
                    not isinstance(expected_sha, str)
                    or sha256_bytes(committed) != expected_sha
                    or current_sha != expected_sha
                    or current != committed
                ):
                    raise ValidationError(
                        "recovery-evidence transfer R0 runtime bytes drifted"
                    )
        except (OSError, UnicodeError, ValidationError):
            errors.append("recovery-evidence transfer R0 Git source proof is invalid")
    return item


def _recovery_transfer_runtime_baseline(bindings: dict[str, Any]) -> dict[str, Any]:
    return {
        "git_commit": bindings.get("git_commit"),
        "voice_transfer_runtime_sha256": bindings.get("voice_transfer_runtime_sha256"),
        "transfer_worker_runtime_sha256": bindings.get("transfer_worker_runtime_sha256"),
        "authorization_schema_sha256": bindings.get("recovery_transfer_schema_sha256"),
        "voice_transfer_tests_sha256": bindings.get("voice_transfer_tests_sha256"),
        "transfer_worker_tests_sha256": bindings.get("transfer_worker_tests_sha256"),
    }


def _validate_recovery_transfer_evidence_baseline(
    value: Any,
    *,
    active: bool,
    authorization_path: Path,
    authorization_raw: bytes,
    plan_path: Path,
    canonical_w_path: Path,
    active_materialized_at: datetime | None,
    root: Path,
    runtime_bindings: dict[str, Any],
    account_evidence: dict[str, Any],
    prerequisite_result: dict[str, Any],
    errors: list[str],
    allowed_generated_status_paths: frozenset[str] | None = None,
    allowed_ignored_generated_paths: frozenset[str] | None = None,
) -> dict[str, Any]:
    """Bind the later R1 evidence commit without conflating it with runtime R0."""

    if not active:
        item = _strict(value, {"state"}, "recovery-evidence transfer evidence_baseline")
        if item != {"state": "pending"}:
            errors.append("draft recovery-evidence transfer R1 baseline must remain pending")
        return item
    item = _strict(
        value,
        {
            "state", "evidence_commit", "draft_authorization",
            "calibrated_account_assurance", "data_use_assurance", "target_rights",
            "fresh_browser_readiness",
        },
        "recovery-evidence transfer evidence_baseline",
    )
    for name in (
        "draft_authorization", "calibrated_account_assurance", "data_use_assurance",
        "target_rights", "fresh_browser_readiness",
    ):
        _strict(item.get(name), {"path", "sha256"}, f"evidence_baseline {name}")
    evidence_commit = item.get("evidence_commit")
    runtime_commit = runtime_bindings.get("git_commit")
    records = prerequisite_result.get("records")
    if not isinstance(records, dict):
        records = {}
    account_records = account_evidence.get("records")
    if not isinstance(account_records, dict):
        account_records = {}

    def _record_binding(
        records_value: dict[str, Any], name: str, exact_path: str | None = None
    ) -> dict[str, Any] | None:
        record = records_value.get(name)
        if (
            not isinstance(record, tuple)
            or len(record) != 3
            or not isinstance(record[0], Path)
            or not isinstance(record[1], bytes)
            or not isinstance(record[2], str)
        ):
            return None
        try:
            relative = record[0].relative_to(root).as_posix()
        except ValueError:
            return None
        if exact_path is not None and relative != exact_path:
            return None
        return {"path": relative, "sha256": record[2]}

    expected = {
        "calibrated_account_assurance": _record_binding(
            account_records,
            "calibrated_account_assurance",
            RECOVERY_TRANSFER_ACCOUNT_ASSURANCE_PATH,
        ),
        "data_use_assurance": _record_binding(
            records,
            "elevenlabs_data_use",
            RECOVERY_TRANSFER_DATA_USE_ASSURANCE_PATH,
        ),
        "target_rights": _record_binding(
            records,
            "target_voice_rights",
            RECOVERY_TRANSFER_TARGET_RIGHTS_PATH,
        ),
        "fresh_browser_readiness": _record_binding(records, "fresh_browser_readiness"),
    }
    if (
        item.get("state") != "verified"
        or not isinstance(evidence_commit, str)
        or not _GIT_SHA_RE.fullmatch(evidence_commit)
        or not isinstance(runtime_commit, str)
        or not _GIT_SHA_RE.fullmatch(runtime_commit)
        or evidence_commit == runtime_commit
        or item.get("draft_authorization", {}).get("path")
        != RECOVERY_TRANSFER_DRAFT_PATH
        or any(expected[name] is None or item.get(name) != expected[name] for name in expected)
    ):
        errors.append("active recovery-evidence transfer R1 binding is not exact")
        return item

    try:
        repository = pt._guide_repository_root()
        _verify_local_git_object_store(runtime_bindings)
        _bound_git(runtime_bindings, ["cat-file", "-e", f"{evidence_commit}^{{commit}}"])
        _bound_git(
            runtime_bindings,
            [
                "merge-base", "--is-ancestor",
                RECOVERY_TRANSFER_OUTCOME_COMMIT, runtime_commit,
            ],
        )
        for recovery_name in (
            "recovery_authorization", "credential_read_latch", "provider_call_latch",
            "http_200_failure_receipt", "terminal_disposition",
        ):
            recovery_path, recovery_raw, recovery_sha = account_records[recovery_name]
            recovery_relative = recovery_path.relative_to(repository).as_posix()
            historical = _bound_git(
                runtime_bindings,
                ["show", f"{RECOVERY_TRANSFER_OUTCOME_COMMIT}:{recovery_relative}"],
                max_bytes=2_000_000,
            )
            if historical != recovery_raw or sha256_bytes(historical) != recovery_sha:
                raise ValidationError(
                    "recovery-evidence transfer consumed recovery chain drifted"
                )
        _bound_git(
            runtime_bindings,
            ["merge-base", "--is-ancestor", runtime_commit, evidence_commit],
        )
        evidence_parents = _bound_git(
            runtime_bindings,
            ["rev-list", "--parents", "-n", "1", evidence_commit],
        ).strip().split()
        if evidence_parents != [
            evidence_commit.encode("ascii"),
            runtime_commit.encode("ascii"),
        ]:
            raise ValidationError(
                "recovery-evidence transfer R1 must be the direct single-parent child of R0"
            )
        head = _bound_git(runtime_bindings, ["rev-parse", "HEAD"]).strip().decode("ascii")
        if not _GIT_SHA_RE.fullmatch(head) or head == evidence_commit:
            raise ValidationError("recovery-evidence transfer ACTIVE commit is invalid")
        _bound_git(
            runtime_bindings,
            ["merge-base", "--is-ancestor", evidence_commit, head],
        )
        head_parents = _bound_git(
            runtime_bindings,
            ["rev-list", "--parents", "-n", "1", head],
        ).strip().split()
        if head_parents != [head.encode("ascii"), evidence_commit.encode("ascii")]:
            raise ValidationError(
                "recovery-evidence transfer ACTIVE must be the direct single-parent child of R1"
            )

        draft_binding = item["draft_authorization"]
        draft_bytes, draft_sha = _read_bound_blob(
            root,
            root / draft_binding["path"],
            "recovery-evidence transfer R1 DRAFT",
            max_bytes=2_000_000,
        )
        if draft_sha != draft_binding["sha256"]:
            raise ValidationError("recovery-evidence transfer R1 DRAFT hash drifted")
        draft_validation = validate_recovery_evidence_voice_transfer_authorization(
            root / draft_binding["path"],
            plan_path,
            canonical_w_path,
        )
        draft_time_errors: list[str] = []
        draft_materialized_at = _parse_recovery_transfer_time(
            draft_validation.get("materialized_at"),
            "recovery-evidence transfer R1 DRAFT materialized_at",
            draft_time_errors,
        )
        if (
            draft_validation.get("valid") is not True
            or draft_validation.get("authorization_status") != "draft"
            or draft_validation.get("provider_action_authorized") is not False
            or draft_validation.get("generation_post_calls_authorized") != 0
            or draft_validation.get("authorization_sha256") != draft_sha
            or draft_time_errors
            or not isinstance(draft_materialized_at, datetime)
            or not isinstance(active_materialized_at, datetime)
            or draft_materialized_at > active_materialized_at
        ):
            raise ValidationError(
                "recovery-evidence transfer R1 DRAFT is not the validated zero-authority draft"
            )
        bound_records: dict[str, tuple[Path, bytes, str]] = {
            "draft_authorization": (
                root / draft_binding["path"],
                draft_bytes,
                draft_sha,
            ),
            "calibrated_account_assurance": account_records[
                "calibrated_account_assurance"
            ],
            "data_use_assurance": records["elevenlabs_data_use"],
            "target_rights": records["target_voice_rights"],
            "fresh_browser_readiness": records["fresh_browser_readiness"],
        }
        expected_r1_paths: dict[str, tuple[bytes, str]] = {}
        for name, (path, raw, digest) in bound_records.items():
            relative = path.relative_to(repository).as_posix()
            binding = item.get(name)
            if (
                not isinstance(binding, dict)
                or binding.get("sha256") != digest
                or sha256_bytes(raw) != digest
            ):
                raise ValidationError("recovery-evidence transfer R1 binding drifted")
            expected_r1_paths[relative] = (raw, digest)
        delta = _bound_git(
            runtime_bindings,
            [
                "diff", "--no-ext-diff", "--no-textconv", "--no-renames",
                "--name-status", "--diff-filter=ACDMRTUXB", "-z",
                f"{runtime_commit}..{evidence_commit}",
            ],
        )
        r1_parts = delta.split(b"\x00")
        if not r1_parts or r1_parts[-1] != b"" or (len(r1_parts) - 1) % 2:
            raise ValidationError("recovery-evidence transfer R1 delta is malformed")
        r1_entries = list(zip(r1_parts[0:-1:2], r1_parts[1:-1:2]))
        actual_r1_paths = [path.decode("utf-8") for status, path in r1_entries]
        if (
            any(status != b"A" for status, _path in r1_entries)
            or len(actual_r1_paths) != len(set(actual_r1_paths))
            or set(actual_r1_paths) != set(expected_r1_paths)
        ):
            raise ValidationError("recovery-evidence transfer R1 delta is not exact")
        for relative, (raw, digest) in expected_r1_paths.items():
            committed = _bound_git(
                runtime_bindings,
                ["show", f"{evidence_commit}:{relative}"],
                max_bytes=10_000_000,
            )
            if committed != raw or sha256_bytes(committed) != digest:
                raise ValidationError("recovery-evidence transfer R1 bytes drifted")
        private_capture = records["fresh_browser_capture"]
        private_capture_relative = private_capture[0].relative_to(repository).as_posix()
        selected_relative = (root / SELECTED_GUIDE_PATH).relative_to(repository).as_posix()
        for private_relative in (private_capture_relative, selected_relative):
            for commit_value in (runtime_commit, evidence_commit, head):
                if _bound_git(
                    runtime_bindings,
                    ["ls-tree", "--name-only", commit_value, "--", private_relative],
                ):
                    raise ValidationError(
                        "local-only recovery-evidence bytes must be absent from Git history"
                    )

        active_relative = authorization_path.relative_to(repository).as_posix()
        if authorization_path.relative_to(root).as_posix() != RECOVERY_TRANSFER_ACTIVE_PATH:
            raise ValidationError("recovery-evidence transfer ACTIVE path drifted")
        active_delta = _bound_git(
            runtime_bindings,
            [
                "diff", "--no-ext-diff", "--no-textconv", "--no-renames",
                "--name-status", "--diff-filter=ACDMRTUXB", "-z",
                f"{evidence_commit}..{head}",
            ],
        )
        if active_delta != b"A\x00" + active_relative.encode("utf-8") + b"\x00":
            raise ValidationError("recovery-evidence transfer ACTIVE delta is not exact")
        if _bound_git(runtime_bindings, ["show", f"{head}:{active_relative}"]) != authorization_raw:
            raise ValidationError("recovery-evidence transfer ACTIVE bytes are not exact")
        status_bytes = _bound_git(
            runtime_bindings,
            ["status", "--porcelain=v1", "--untracked-files=all", "-z"],
        )
        if allowed_generated_status_paths is None:
            if status_bytes:
                raise ValidationError("recovery-evidence transfer worktree is not clean")
        else:
            entries = status_bytes.split(b"\x00")
            if not entries or entries[-1] != b"":
                raise ValidationError("recovery-evidence generated status is malformed")
            try:
                actual_generated = {
                    entry[3:].decode("utf-8")
                    for entry in entries[:-1]
                    if entry.startswith(b"?? ")
                }
            except UnicodeError:
                raise ValidationError("recovery-evidence generated status is invalid") from None
            if (
                len(actual_generated) != len(entries) - 1
                or actual_generated != set(allowed_generated_status_paths)
            ):
                raise ValidationError("recovery-evidence generated status is not exact")
            ignored_generated = set(allowed_ignored_generated_paths or ())
            ignore_relative = (root / ".gitignore").relative_to(repository).as_posix()
            for ignored_relative in ignored_generated:
                if _bound_git(
                    runtime_bindings,
                    ["ls-files", "--stage", "--", ignored_relative],
                ):
                    raise ValidationError("recovery-evidence generated raw output is tracked")
                ignore_proof = _bound_git(
                    runtime_bindings,
                    ["check-ignore", "--no-index", "-v", "--", ignored_relative],
                )
                expected_ignore = (
                    f"{ignore_relative}:1:outputs/raw/\t{ignored_relative}\n".encode(
                        "utf-8"
                    )
                )
                if ignore_proof != expected_ignore:
                    raise ValidationError(
                        "recovery-evidence generated raw ignore proof is not exact"
                    )
    except (KeyError, OSError, UnicodeError, ValidationError, ValueError):
        errors.append("active recovery-evidence transfer R1 Git source proof is invalid")
    return item


def _validate_recovery_transfer_account_evidence(
    root: Path,
    value: Any,
    errors: list[str],
) -> dict[str, Any]:
    item = _strict(
        value,
        {
            "state", "calibrated_account_assurance",
            "credential_authentication_inference", "authentication_conclusion",
            "response_body_contents_state", "account_data_observed",
            "identity_observed", "valid_user_id_observed",
            "subscription_state_observed", "target_voice_accessibility_state",
            "ui_api_account_equality_state", "exact_ui_api_account_equality_verified",
            "exact_ui_api_account_equality_claimed", "account_verified_claimed",
            "second_account_get_authorized",
        },
        "recovery-evidence transfer account evidence",
    )
    assurance_binding = _strict(
        item.get("calibrated_account_assurance"),
        {"state", "path", "sha256"},
        "calibrated account assurance binding",
    )
    assurance_sha = assurance_binding.get("sha256")
    expected = _recovery_transfer_account_evidence(
        True,
        assurance_sha256=assurance_sha if isinstance(assurance_sha, str) else None,
    )
    if not _exact(item, expected):
        errors.append("recovery-evidence transfer account assurance binding drifted")
    records: dict[str, tuple[Path, bytes, str]] = {}
    documents: dict[str, dict[str, Any]] = {}
    try:
        assurance_path, assurance, assurance_raw, assurance_actual_sha = (
            _read_recovery_private_json_record(
            root,
            assurance_binding.get("path"),
            assurance_sha,
            "recovery calibrated account assurance",
            )
        )
    except ValidationError as exc:
        errors.extend(exc.errors)
        return {"records": records}
    records["calibrated_account_assurance"] = (
        assurance_path,
        assurance_raw,
        assurance_actual_sha,
    )
    _strict(
        assurance,
        {
            "schema_version", "record_id", "status", "provider", "recorded_at",
            "outcome_commit", "recovery_evidence", "observed_outcome",
            "calibrated_interpretation", "terminality", "authority",
        },
        "recovery calibrated account assurance",
    )
    assurance_records = _strict(
        assurance.get("recovery_evidence"),
        {
            "recovery_authorization", "credential_read_latch", "provider_call_latch",
            "http_200_failure_receipt", "terminal_disposition",
        },
        "recovery calibrated account assurance evidence",
    )
    assurance_interpretation = _strict(
        assurance.get("calibrated_interpretation"),
        {
            "credential_authentication_inference", "authentication_conclusion",
            "response_body_contents_state", "account_payload_parsed",
            "account_data_observed", "identity_observed",
            "valid_user_id_observed", "subscription_state_observed",
            "target_voice_accessibility_state", "ui_api_account_equality_state",
            "exact_ui_api_account_equality_verified",
            "exact_ui_api_account_equality_claimed", "account_verified_claimed",
            "key_verified_claimed", "account_linkage_strength", "safe_conclusion",
        },
        "recovery calibrated account assurance interpretation",
    )
    assurance_outcome = _strict(
        assurance.get("observed_outcome"),
        {
            "provider_response_received", "http_status",
            "provider_get_attempts_consumed", "provider_post_attempts_consumed",
            "failure_code", "response_body_bytes_read", "raw_response_stored",
            "response_body_stored", "response_hash_stored", "response_mime_type",
            "response_content_encoding",
        },
        "recovery calibrated account assurance outcome",
    )
    assurance_terminality = _strict(
        assurance.get("terminality"),
        {
            "automatic_retry_permitted", "retry_or_resumption",
            "recovery_authorization_reusable", "credential_read_latch_reusable",
            "provider_call_latch_reusable",
            "future_action_requires_separate_reviewed_committed_transaction_basis",
        },
        "recovery calibrated account assurance terminality",
    )
    assurance_authority = _strict(
        assurance.get("authority"),
        set(_recovery_transfer_zero_authority()),
        "recovery calibrated account assurance authority",
    )
    expected_bindings = {
        "recovery_authorization": {
            "path": RECOVERY_TRANSFER_ACCOUNT_AUTH_PATH,
            "sha256": RECOVERY_TRANSFER_ACCOUNT_AUTH_SHA256,
        },
        "credential_read_latch": {
            "path": RECOVERY_TRANSFER_CREDENTIAL_LATCH_PATH,
            "sha256": RECOVERY_TRANSFER_CREDENTIAL_LATCH_SHA256,
        },
        "provider_call_latch": {
            "path": RECOVERY_TRANSFER_PROVIDER_LATCH_PATH,
            "sha256": RECOVERY_TRANSFER_PROVIDER_LATCH_SHA256,
        },
        "http_200_failure_receipt": {
            "path": RECOVERY_TRANSFER_FAILURE_PATH,
            "sha256": RECOVERY_TRANSFER_FAILURE_SHA256,
        },
        "terminal_disposition": {
            "path": RECOVERY_TRANSFER_DISPOSITION_PATH,
            "sha256": RECOVERY_TRANSFER_DISPOSITION_SHA256,
        },
    }
    expected_interpretation = {
        "credential_authentication_inference": expected[
            "credential_authentication_inference"
        ],
        "authentication_conclusion": expected["authentication_conclusion"],
        "response_body_contents_state": expected["response_body_contents_state"],
        "account_payload_parsed": False,
        "account_data_observed": False,
        "identity_observed": False,
        "valid_user_id_observed": False,
        "subscription_state_observed": False,
        "target_voice_accessibility_state": "unknown",
        "account_linkage_strength": "contextual_non_cryptographic",
        "ui_api_account_equality_state": "unknown",
        "exact_ui_api_account_equality_verified": False,
        "exact_ui_api_account_equality_claimed": False,
        "account_verified_claimed": False,
        "key_verified_claimed": False,
        "safe_conclusion": RECOVERY_TRANSFER_SAFE_CONCLUSION,
    }
    if (
        assurance.get("schema_version")
        != "oe-elevenlabs-recovery-calibrated-account-assurance-v1"
        or assurance.get("record_id")
        != "V1-ELEVENLABS-RECOVERY-CALIBRATED-ACCOUNT-ASSURANCE"
        or assurance.get("status") != "calibrated_non_authorizing"
        or assurance.get("provider") != "elevenlabs"
        or assurance.get("outcome_commit") != RECOVERY_TRANSFER_OUTCOME_COMMIT
        or not _exact(assurance_records, expected_bindings)
        or assurance_outcome
        != {
            "provider_response_received": True,
            "http_status": 200,
            "provider_get_attempts_consumed": 1,
            "provider_post_attempts_consumed": 0,
            "failure_code": "provider_total_deadline_unenforceable",
            "response_body_bytes_read": 0,
            "raw_response_stored": False,
            "response_body_stored": False,
            "response_hash_stored": False,
            "response_mime_type": None,
            "response_content_encoding": None,
        }
        or not _exact(assurance_interpretation, expected_interpretation)
        or assurance_terminality
        != {
            "automatic_retry_permitted": False,
            "retry_or_resumption": False,
            "recovery_authorization_reusable": False,
            "credential_read_latch_reusable": False,
            "provider_call_latch_reusable": False,
            "future_action_requires_separate_reviewed_committed_transaction_basis": True,
        }
        or assurance_authority
        != _recovery_transfer_zero_authority()
    ):
        errors.append("standalone recovery account assurance is not exact and non-authorizing")
    assurance_recorded_at = _parse_recovery_transfer_time(
        assurance.get("recorded_at"),
        "recovery calibrated account assurance recorded_at",
        errors,
    )
    bindings = (
        (
            "recovery_authorization",
            RECOVERY_TRANSFER_ACCOUNT_AUTH_PATH,
            RECOVERY_TRANSFER_ACCOUNT_AUTH_SHA256,
            0o600,
        ),
        (
            "credential_read_latch",
            RECOVERY_TRANSFER_CREDENTIAL_LATCH_PATH,
            RECOVERY_TRANSFER_CREDENTIAL_LATCH_SHA256,
            0o600,
        ),
        (
            "provider_call_latch",
            RECOVERY_TRANSFER_PROVIDER_LATCH_PATH,
            RECOVERY_TRANSFER_PROVIDER_LATCH_SHA256,
            0o600,
        ),
        (
            "http_200_failure_receipt",
            RECOVERY_TRANSFER_FAILURE_PATH,
            RECOVERY_TRANSFER_FAILURE_SHA256,
            0o600,
        ),
        (
            "terminal_disposition",
            RECOVERY_TRANSFER_DISPOSITION_PATH,
            RECOVERY_TRANSFER_DISPOSITION_SHA256,
            0o644,
        ),
    )
    for name, path, digest, mode in bindings:
        bound = assurance_records.get(name)
        if not isinstance(bound, dict) or bound != {"path": path, "sha256": digest}:
            errors.append(f"standalone account assurance {name} binding drifted")
        try:
            if mode == 0o600:
                record_path, document, raw, actual = _read_recovery_private_json_record(
                    root,
                    path,
                    digest,
                    f"recovery-evidence transfer {name}",
                )
            else:
                record_path, document, raw, actual = _read_record(
                    root,
                    path,
                    digest,
                    f"recovery-evidence transfer {name}",
                    mode=mode,
                )
        except ValidationError as exc:
            errors.extend(exc.errors)
            continue
        records[name] = (record_path, raw, actual)
        documents[name] = document
    if set(documents) != {item[0] for item in bindings}:
        return {"records": records}

    authorization = documents["recovery_authorization"]
    credential_latch = documents["credential_read_latch"]
    provider_latch = documents["provider_call_latch"]
    failure = documents["http_200_failure_receipt"]
    disposition = documents["terminal_disposition"]
    interpretation = disposition.get("interpretation", {})
    outcome = disposition.get("observed_outcome", {})
    terminality = disposition.get("terminality", {})
    if (
        authorization.get("schema_version") != RECOVERY_AUTH_SCHEMA
        or authorization.get("status") != "active"
        or authorization.get("approved") is not True
        or credential_latch.get("schema_version")
        != RECOVERY_CREDENTIAL_READ_CONSUMPTION_SCHEMA
        or credential_latch.get("authorization_sha256")
        != RECOVERY_TRANSFER_ACCOUNT_AUTH_SHA256
        or credential_latch.get("network_called_at_consumption") is not False
        or provider_latch.get("schema_version") != RECOVERY_CONSUMPTION_SCHEMA
        or provider_latch.get("authorization_sha256") != RECOVERY_TRANSFER_ACCOUNT_AUTH_SHA256
        or provider_latch.get("credential_read_latch_sha256")
        != RECOVERY_TRANSFER_CREDENTIAL_LATCH_SHA256
        or provider_latch.get("browser_suffix_matches_held_credential") is not True
        or provider_latch.get("network_called_at_consumption") is not False
        or failure.get("schema_version") != RECOVERY_FAILURE_SCHEMA
        or failure.get("failure_code") != "provider_total_deadline_unenforceable"
        or failure.get("method") != "GET"
        or failure.get("endpoint") != ACCOUNT_ENDPOINT
        or failure.get("http_status") != 200
        or failure.get("provider_response_received") is not True
        or failure.get("provider_get_attempts_consumed") != 1
        or failure.get("provider_post_attempts_consumed") != 0
        or failure.get("response_bytes") != 0
        or failure.get("raw_response_stored") is not False
        or failure.get("account_data_stored") is not False
        or failure.get("retry_permitted") is not False
        or disposition.get("schema_version")
        != "oe-elevenlabs-account-recovery-http-200-zero-body-failure-disposition-v1"
        or interpretation.get("credential_authentication_inference")
        != RECOVERY_TRANSFER_AUTHENTICATION_INFERENCE_STATE
        or interpretation.get("credential_authentication_inference_statement")
        != RECOVERY_TRANSFER_AUTHENTICATION_CONCLUSION
        or interpretation.get("response_body_contents_state") != "unknown_not_read"
        or interpretation.get("account_data_observed") is not False
        or interpretation.get("identity_observed") is not False
        or interpretation.get("valid_user_id_observed") is not False
        or interpretation.get("subscription_state_observed") is not False
        or interpretation.get("target_voice_accessibility_observed_from_api") is not False
        or interpretation.get("ui_api_account_equality_state") != "unknown"
        or interpretation.get("exact_ui_api_account_equality_verified") is not False
        or interpretation.get("account_verified_claimed") is not False
        or outcome.get("provider_response_received") is not True
        or outcome.get("response_body_bytes_read") != 0
        or outcome.get("provider_get_attempts_consumed") != 1
        or outcome.get("provider_post_attempts_consumed") != 0
        or terminality.get("retry_authorized") is True
        or terminality.get("automatic_retry_permitted") is not False
        or terminality.get("provider_call_latch_reusable") is not False
        or terminality.get("credential_read_latch_reusable") is not False
        or terminality.get("this_record_authorizes_provider_action") is not False
    ):
        errors.append("recovery HTTP-200 evidence semantics are not exact and calibrated")
    recovery_chain_times = [
        _parse_time(
            credential_latch.get("consumed_at"),
            "recovery credential latch consumed_at",
            errors,
        ),
        _parse_time(
            provider_latch.get("consumed_at"),
            "recovery provider latch consumed_at",
            errors,
        ),
        _parse_time(failure.get("failed_at"), "recovery failure failed_at", errors),
        _parse_time(
            disposition.get("recorded_at"),
            "recovery disposition recorded_at",
            errors,
        ),
    ]
    if (
        isinstance(assurance_recorded_at, datetime)
        and all(isinstance(item, datetime) for item in recovery_chain_times)
        and assurance_recorded_at
        < max(item for item in recovery_chain_times if isinstance(item, datetime))
    ):
        errors.append("calibrated account assurance predates its terminal recovery chain")
    fingerprint = provider_latch.get("credential_fingerprint_sha256")
    suffix_sha = provider_latch.get("browser_suffix_sha256")
    if not isinstance(fingerprint, str) or not _SHA_RE.fullmatch(fingerprint):
        errors.append("recovery provider latch credential fingerprint is invalid")
    if not isinstance(suffix_sha, str) or not _SHA_RE.fullmatch(suffix_sha):
        errors.append("recovery provider latch browser suffix binding is invalid")
    return {
        "records": records,
        "api_key_fingerprint_sha256": fingerprint,
        "browser_suffix_sha256": suffix_sha,
        "account_assurance_sha256": assurance_actual_sha,
        "account_assurance_recorded_at": assurance_recorded_at,
    }


def _validate_recovery_transfer_prerequisites(
    root: Path,
    value: Any,
    authorization: dict[str, Any],
    plan_dry: dict[str, Any],
    account_evidence: dict[str, Any],
    runtime_bindings: dict[str, Any],
    errors: list[str],
) -> dict[str, Any]:
    expected_names = set(_recovery_transfer_prerequisites(False))
    prerequisites = _strict(value, expected_names, "recovery-evidence transfer prerequisites")
    approved_by = authorization.get("evidence_owner")
    selected = _strict(
        prerequisites.get("selected_guide"),
        {
            "state", "path", "sha256", "byte_count", "duration_seconds", "container",
            "codec", "sample_rate_hz", "channels", "guide_request_id",
            "guide_run_receipt_path", "guide_run_receipt_sha256",
        },
        "recovery-evidence selected_guide",
    )
    selected_audio, _geometry, run_path, _run, run_raw, run_sha, guide_at = (
        _validate_selected_guide_and_run(
            root,
            selected,
            plan_dry,
            approved_by,
            errors,
        )
    )
    private_run_raw = run_raw
    private_run_sha = run_sha
    try:
        private_selected_audio, private_selected_sha = _read_recovery_private_bytes(
            root,
            root / SELECTED_GUIDE_PATH,
            "recovery-evidence selected guide",
            max_bytes=50_000_000,
        )
        if (
            private_selected_audio != selected_audio
            or private_selected_sha != SELECTED_GUIDE_SHA256
        ):
            raise ValidationError(
                "recovery-evidence selected guide descriptor-bound bytes drifted"
            )
        selected_audio = private_selected_audio
        (
            private_run_path,
            _private_run,
            private_run_raw,
            private_run_sha,
        ) = _read_recovery_private_json_record(
            root,
            run_path.relative_to(root).as_posix(),
            run_sha,
            "recovery-evidence guide run receipt",
        )
        if (
            private_run_path != run_path
            or private_run_raw != run_raw
            or private_run_sha != SELECTED_GUIDE_RUN_SHA256
        ):
            raise ValidationError(
                "recovery-evidence guide run descriptor-bound bytes drifted"
            )
        repository = pt._guide_repository_root()
        _verify_recovery_transfer_selected_guide_git_state(
            runtime_bindings,
            repository,
            root,
            root / SELECTED_GUIDE_PATH,
        )
        run_relative = run_path.relative_to(repository).as_posix()
        historical_run = _bound_git(
            runtime_bindings,
            ["show", f"{RECOVERY_TRANSFER_OUTCOME_COMMIT}:{run_relative}"],
            max_bytes=2_000_000,
        )
        if (
            historical_run != private_run_raw
            or sha256_bytes(historical_run) != SELECTED_GUIDE_RUN_SHA256
        ):
            raise ValidationError(
                "recovery-evidence guide run Git source proof drifted"
            )
    except ValidationError as exc:
        errors.extend(exc.errors)
    except (KeyError, OSError, ValueError):
        errors.append("recovery-evidence guide input source proof is invalid")
    records: dict[str, tuple[Path, bytes, str]] = {
        "selected_guide": (root / SELECTED_GUIDE_PATH, selected_audio, SELECTED_GUIDE_SHA256),
        "guide_run": (run_path, private_run_raw, private_run_sha),
    }
    documents: dict[str, dict[str, Any]] = {}
    for name in sorted(expected_names - {"selected_guide"}):
        try:
            binding = _strict(
                prerequisites.get(name),
                {"state", "path", "sha256"},
                f"recovery-evidence {name}",
            )
            if binding.get("state") != "verified":
                raise ValidationError(f"recovery-evidence {name}.state must be verified")
            expected_path = {
                "guide_qa": RECOVERY_TRANSFER_GUIDE_QA_PATH,
                "owner_selection": RECOVERY_TRANSFER_GUIDE_SELECTION_PATH,
                "elevenlabs_data_use": RECOVERY_TRANSFER_DATA_USE_ASSURANCE_PATH,
                "target_voice_rights": RECOVERY_TRANSFER_TARGET_RIGHTS_PATH,
                "owner_audition_confirmation": RECOVERY_TRANSFER_OWNER_APPROVAL_PATH,
                "official_media_contract": MEDIA_CONTRACT_BASIS_PATH,
            }.get(name)
            if expected_path is not None and binding.get("path") != expected_path:
                raise ValidationError(f"recovery-evidence {name} path is not exact")
            expected_sha = {
                "guide_qa": RECOVERY_TRANSFER_GUIDE_QA_SHA256,
                "owner_selection": RECOVERY_TRANSFER_GUIDE_SELECTION_SHA256,
                "owner_audition_confirmation": RECOVERY_TRANSFER_OWNER_APPROVAL_SHA256,
                "official_media_contract": MEDIA_CONTRACT_BASIS_SHA256,
            }.get(name)
            if expected_sha is not None and binding.get("sha256") != expected_sha:
                raise ValidationError(f"recovery-evidence {name} SHA-256 is not exact")
            if name in {
                "guide_qa", "owner_selection", "owner_audition_confirmation",
                "elevenlabs_data_use", "target_voice_rights",
            }:
                path, document, raw, digest = _read_recovery_private_json_record(
                    root,
                    binding.get("path"),
                    binding.get("sha256"),
                    f"recovery-evidence {name}",
                )
            else:
                path, document, raw, digest = _read_record(
                    root,
                    binding.get("path"),
                    binding.get("sha256"),
                    f"recovery-evidence {name}",
                )
        except ValidationError as exc:
            errors.extend(exc.errors)
            continue
        records[name] = (path, raw, digest)
        documents[name] = document
    if set(documents) != expected_names - {"selected_guide"}:
        return {"records": records, "selected_audio": selected_audio}

    try:
        repository = pt._guide_repository_root()
        c907_path, c907_raw, c907_sha = records["owner_audition_confirmation"]
        c907_relative = c907_path.relative_to(repository).as_posix()
        c907_historical = _bound_git(
            runtime_bindings,
            ["show", f"{RECOVERY_TRANSFER_OUTCOME_COMMIT}:{c907_relative}"],
            max_bytes=2_000_000,
        )
        if (
            c907_sha != RECOVERY_TRANSFER_OWNER_APPROVAL_SHA256
            or c907_historical != c907_raw
            or sha256_bytes(c907_historical) != RECOVERY_TRANSFER_OWNER_APPROVAL_SHA256
        ):
            raise ValidationError("recovery-evidence transfer c907 source drifted")
    except (KeyError, OSError, ValidationError, ValueError):
        errors.append("recovery-evidence transfer c907 Git source proof is invalid")

    qa = documents["guide_qa"]
    selection = documents["owner_selection"]
    audition = documents["owner_audition_confirmation"]
    data_use = documents["elevenlabs_data_use"]
    rights = documents["target_voice_rights"]
    media = documents["official_media_contract"]
    data_top = _strict(
        data_use,
        {
            "schema_version", "record_id", "status", "provider", "recorded_at",
            "owner", "transaction_basis_id", "exact_guide", "evidence",
            "fresh_observation", "configuration_intent", "runtime_baseline",
            "authority",
        },
        "recovery-evidence data-use assurance",
    )
    data_guide = _strict(
        data_use.get("exact_guide"),
        {"path", "sha256", "byte_count", "duration_seconds"},
        "recovery-evidence data-use exact guide",
    )
    data_evidence = _strict(
        data_use.get("evidence"),
        {
            "fresh_browser_readiness", "fresh_browser_capture",
            "official_data_use_basis", "calibrated_account_assurance",
            "target_rights", "terminal_disposition",
            "owner_audition_and_bounded_transfer_approval",
        },
        "recovery-evidence data-use source chain",
    )
    for name in data_evidence:
        _strict(data_evidence.get(name), {"path", "sha256"}, f"data-use {name}")
    data_observation = _strict(
        data_use.get("fresh_observation"),
        {
            "observed_at", "improve_models_for_everyone", "update_completed",
            "protection_mode", "protection_effective_for_new_submissions",
            "fresh_at_recorded_at", "freshness_reference", "freshness_window_seconds",
            "account_linkage_strength",
            "ui_api_account_equality_state", "exact_ui_api_account_equality_verified",
        },
        "recovery-evidence fresh browser observation",
    )
    data_intent = _strict(
        data_use.get("configuration_intent"),
        {
            "chosen_enable_logging", "cross_provider_upload_owner_permission_observed",
            "zero_retention_mode_claimed", "descriptive_only_not_execution_authority",
        },
        "recovery-evidence data-use configuration intent",
    )
    data_authority = _strict(
        data_use.get("authority"),
        set(_recovery_transfer_zero_authority()),
        "recovery-evidence data-use authority",
    )
    data_runtime_baseline = _strict(
        data_use.get("runtime_baseline"),
        set(_recovery_transfer_runtime_baseline(runtime_bindings)),
        "recovery-evidence data-use runtime baseline",
    )
    rights_top = _strict(
        rights,
        {
            "schema_version", "record_id", "status", "provider", "recorded_at",
            "owner", "transaction_basis_id", "evidence", "original_c_provenance",
            "exact_scope", "owner_authority_calibration", "authority",
        },
        "recovery-evidence target-rights record",
    )
    rights_evidence = _strict(
        rights.get("evidence"),
        {
            "owner_audition_and_bounded_transfer_approval", "guide_qa",
            "owner_selection", "performance_transfer_plan", "official_media_contract",
        },
        "recovery-evidence target-rights evidence",
    )
    for name in rights_evidence:
        _strict(rights_evidence.get(name), {"path", "sha256"}, f"target-rights {name}")
    rights_provenance = _strict(
        rights.get("original_c_provenance"),
        {"owner_selection", "saved_voice_receipt"},
        "recovery-evidence Original C provenance",
    )
    for name in rights_provenance:
        _strict(rights_provenance.get(name), {"path", "sha256"}, f"Original C {name}")
    rights_scope = _strict(
        rights.get("exact_scope"),
        {
            "method", "endpoint", "target_voice_id", "voice_owner", "consent_owner",
            "exact_guide_sha256", "owner_scope_voice_changer_permitted",
            "bounded_microtest_only", "primary_request_sha256",
            "primary_multipart_body_sha256", "primary_multipart_body_bytes",
            "normalized_http_request_sha256", "model_id", "seed", "voice_settings",
            "output_format", "enable_logging", "remove_background_noise",
            "file_format", "max_provider_posts", "max_outputs", "no_retry",
            "no_redirect", "no_application_fallback", "full_capture_permitted",
        },
        "recovery-evidence target-rights exact scope",
    )
    rights_owner_authority = _strict(
        rights.get("owner_authority_calibration"),
        set(_recovery_transfer_scope_approval()),
        "recovery-evidence target-rights owner authority calibration",
    )
    rights_authority = _strict(
        rights.get("authority"),
        set(_recovery_transfer_zero_authority()),
        "recovery-evidence target-rights authority",
    )
    expected_account_assurance_sha = account_evidence.get("account_assurance_sha256")
    data_binding = prerequisites.get("elevenlabs_data_use", {})
    rights_binding = prerequisites.get("target_voice_rights", {})
    expected_data_evidence = {
        "calibrated_account_assurance": {
            "path": RECOVERY_TRANSFER_ACCOUNT_ASSURANCE_PATH,
            "sha256": expected_account_assurance_sha,
        },
        "target_rights": {
            "path": RECOVERY_TRANSFER_TARGET_RIGHTS_PATH,
            "sha256": rights_binding.get("sha256"),
        },
        "terminal_disposition": {
            "path": RECOVERY_TRANSFER_DISPOSITION_PATH,
            "sha256": RECOVERY_TRANSFER_DISPOSITION_SHA256,
        },
        "owner_audition_and_bounded_transfer_approval": {
            "path": RECOVERY_TRANSFER_OWNER_APPROVAL_PATH,
            "sha256": RECOVERY_TRANSFER_OWNER_APPROVAL_SHA256,
        },
    }
    expected_rights_evidence = {
        "owner_audition_and_bounded_transfer_approval": {
            "path": RECOVERY_TRANSFER_OWNER_APPROVAL_PATH,
            "sha256": RECOVERY_TRANSFER_OWNER_APPROVAL_SHA256,
        },
        "guide_qa": {
            "path": prerequisites.get("guide_qa", {}).get("path"),
            "sha256": prerequisites.get("guide_qa", {}).get("sha256"),
        },
        "owner_selection": {
            "path": prerequisites.get("owner_selection", {}).get("path"),
            "sha256": prerequisites.get("owner_selection", {}).get("sha256"),
        },
        "performance_transfer_plan": {
            "path": "performance-transfer-plan.json",
            "sha256": plan_dry["plan_sha256"],
        },
        "official_media_contract": {
            "path": MEDIA_CONTRACT_BASIS_PATH,
            "sha256": MEDIA_CONTRACT_BASIS_SHA256,
        },
    }
    expected_rights_provenance = {
        "owner_selection": {
            "path": RECOVERY_TRANSFER_ORIGINAL_C_SELECTION_PATH,
            "sha256": RECOVERY_TRANSFER_ORIGINAL_C_SELECTION_SHA256,
        },
        "saved_voice_receipt": {
            "path": RECOVERY_TRANSFER_ORIGINAL_C_SAVE_PATH,
            "sha256": RECOVERY_TRANSFER_ORIGINAL_C_SAVE_SHA256,
        },
    }
    if (
        data_top.get("schema_version")
        != "oe-elevenlabs-recovery-evidence-data-use-assurance-v1"
        or data_top.get("record_id")
        != "V1-ELEVENLABS-RECOVERY-TRANSFER-DATA-USE-ASSURANCE"
        or data_top.get("status") != "verified_fresh_non_authorizing"
        or data_top.get("provider") != "elevenlabs"
        or data_top.get("owner") != approved_by
        or data_top.get("transaction_basis_id") != RECOVERY_TRANSFER_TRANSACTION_BASIS_ID
        or data_guide
        != {
            "path": SELECTED_GUIDE_PATH,
            "sha256": SELECTED_GUIDE_SHA256,
            "byte_count": SELECTED_GUIDE_BYTES,
            "duration_seconds": SELECTED_GUIDE_DURATION_SECONDS,
        }
        or any(data_evidence.get(name) != binding for name, binding in expected_data_evidence.items())
        or data_observation.get("improve_models_for_everyone") is not False
        or data_observation.get("update_completed") is not True
        or data_observation.get("protection_mode") != pt.ACCOUNT_TRAINING_OPT_OUT_PROTECTION
        or data_observation.get("protection_effective_for_new_submissions") is not True
        or data_observation.get("fresh_at_recorded_at") is not True
        or data_observation.get("freshness_reference") != "recorded_at"
        or data_observation.get("freshness_window_seconds") != DATA_USE_MAX_AGE_SECONDS
        or data_observation.get("account_linkage_strength")
        != "contextual_non_cryptographic"
        or data_observation.get("ui_api_account_equality_state") != "unknown"
        or data_observation.get("exact_ui_api_account_equality_verified") is not False
        or data_intent
        != {
            "chosen_enable_logging": True,
            "cross_provider_upload_owner_permission_observed": True,
            "zero_retention_mode_claimed": False,
            "descriptive_only_not_execution_authority": True,
        }
        or data_runtime_baseline != _recovery_transfer_runtime_baseline(runtime_bindings)
        or data_authority != _recovery_transfer_zero_authority()
    ):
        errors.append("fresh data-use assurance is not exact, direct, and non-authorizing")
    if (
        rights_top.get("schema_version")
        != "oe-elevenlabs-recovery-evidence-voice-transfer-rights-v1"
        or rights_top.get("record_id")
        != "V1-ELEVENLABS-RECOVERY-TRANSFER-TARGET-RIGHTS"
        or rights_top.get("status") != "owner_scope_recorded_non_authorizing"
        or rights_top.get("provider") != "elevenlabs"
        or rights_top.get("owner") != approved_by
        or rights_top.get("transaction_basis_id") != RECOVERY_TRANSFER_TRANSACTION_BASIS_ID
        or not _exact(rights_evidence, expected_rights_evidence)
        or not _exact(rights_provenance, expected_rights_provenance)
        or rights_owner_authority != _recovery_transfer_scope_approval()
        or rights_scope
        != {
            "method": "POST",
            "endpoint": pt.TRANSFER_ENDPOINT,
            "target_voice_id": pt.TRANSFER_TARGET_VOICE_ID,
            "voice_owner": approved_by,
            "consent_owner": approved_by,
            "exact_guide_sha256": SELECTED_GUIDE_SHA256,
            "owner_scope_voice_changer_permitted": True,
            "bounded_microtest_only": True,
            "primary_request_sha256": TRANSFER_OPT_OUT_REQUEST_SHA256,
            "primary_multipart_body_sha256": TRANSFER_BODY_SHA256,
            "primary_multipart_body_bytes": TRANSFER_BODY_BYTES,
            "normalized_http_request_sha256": TRANSFER_OPT_OUT_NORMALIZED_REQUEST_SHA256,
            "model_id": pt.TRANSFER_MODEL,
            "seed": pt.TRANSFER_SEED,
            "voice_settings": pt.TRANSFER_VOICE_SETTINGS,
            "output_format": pt.TRANSFER_PRIMARY_FORMAT,
            "enable_logging": True,
            "remove_background_noise": False,
            "file_format": "other",
            "max_provider_posts": 1,
            "max_outputs": 1,
            "no_retry": True,
            "no_redirect": True,
            "no_application_fallback": True,
            "full_capture_permitted": False,
        }
        or rights_authority != _recovery_transfer_zero_authority()
    ):
        errors.append("target-rights record is not exact, cross-bound, and non-authorizing")
    blueprint_root = root.parents[2]
    try:
        original_selection_path = pt._safe_relative(
            blueprint_root,
            RECOVERY_TRANSFER_ORIGINAL_C_SELECTION_PATH,
            "recovery-evidence Original C owner selection",
            must_exist=True,
            suffix=".json",
        )
        original_selection_root = pt._document_root(original_selection_path)
        (
            original_selection_path,
            original_selection,
            original_selection_raw,
            original_selection_sha,
        ) = _read_recovery_private_json_record(
            original_selection_root,
            original_selection_path.relative_to(original_selection_root).as_posix(),
            RECOVERY_TRANSFER_ORIGINAL_C_SELECTION_SHA256,
            "recovery-evidence Original C owner selection",
        )
        original_save_path = pt._safe_relative(
            blueprint_root,
            RECOVERY_TRANSFER_ORIGINAL_C_SAVE_PATH,
            "recovery-evidence Original C saved voice",
            must_exist=True,
            suffix=".json",
        )
        original_save_root = pt._document_root(original_save_path)
        (
            original_save_path,
            original_save,
            original_save_raw,
            original_save_sha,
        ) = _read_recovery_private_json_record(
            original_save_root,
            original_save_path.relative_to(original_save_root).as_posix(),
            RECOVERY_TRANSFER_ORIGINAL_C_SAVE_SHA256,
            "recovery-evidence Original C saved voice",
        )
    except ValidationError as exc:
        errors.extend(exc.errors)
    else:
        try:
            repository = pt._guide_repository_root()
            for provenance_path, provenance_raw, provenance_sha in (
                (
                    original_selection_path,
                    original_selection_raw,
                    original_selection_sha,
                ),
                (original_save_path, original_save_raw, original_save_sha),
            ):
                provenance_relative = provenance_path.relative_to(repository).as_posix()
                historical = _bound_git(
                    runtime_bindings,
                    [
                        "show",
                        f"{RECOVERY_TRANSFER_OUTCOME_COMMIT}:{provenance_relative}",
                    ],
                    max_bytes=2_000_000,
                )
                if historical != provenance_raw or sha256_bytes(historical) != provenance_sha:
                    raise ValidationError(
                        "recovery-evidence Original C historical bytes drifted"
                    )
        except (KeyError, OSError, UnicodeError, ValidationError, ValueError):
            errors.append("recovery-evidence Original C Git source proof is invalid")
        if (
            original_selection_sha != RECOVERY_TRANSFER_ORIGINAL_C_SELECTION_SHA256
            or original_save_sha != RECOVERY_TRANSFER_ORIGINAL_C_SAVE_SHA256
            or original_selection.get("schema_version")
            != "oe-elevenlabs-voice-remix-owner-selection-v1"
            or original_selection.get("selected_generated_voice_id")
            != pt.TRANSFER_TARGET_VOICE_ID
            or original_selection.get("selected_by") != approved_by
            or original_selection.get("owner_approved_save") is not True
            or original_save.get("schema_version")
            != "oe-elevenlabs-voice-remix-save-receipt-v1"
            or original_save.get("provider") != "elevenlabs"
            or original_save.get("new_voice_id") != pt.TRANSFER_TARGET_VOICE_ID
            or original_save.get("selected_generated_voice_id")
            != pt.TRANSFER_TARGET_VOICE_ID
            or original_save.get("owner_selection_record_sha256")
            != original_selection_sha
            or original_save.get("new_voice_created") is not True
            or original_save.get("source_voice_modified") is not False
            or original_save.get("provider_calls_made") != 1
        ):
            errors.append("recovery-evidence Original C provenance is invalid")
        records["original_c_selection"] = (
            original_selection_path,
            original_selection_raw,
            original_selection_sha,
        )
        records["original_c_save"] = (
            original_save_path,
            original_save_raw,
            original_save_sha,
        )
    if (
        qa.get("schema_version") != "oe-synthetic-guide-qa-v1"
        or qa.get("selected_guide_sha256") != SELECTED_GUIDE_SHA256
        or qa.get("spoken_text_sha256") != pt.MICROTEST_TEXT_SHA256
        or any(
            qa.get(key) is not True
            for key in (
                "lexical_exact",
                "technical_pass",
                "performance_pass",
                "understandable_without_music_or_visuals",
            )
        )
        or selection.get("schema_version") != "oe-synthetic-guide-owner-selection-v1"
        or selection.get("selected_guide_sha256") != SELECTED_GUIDE_SHA256
        or selection.get("guide_qa_sha256") != records["guide_qa"][2]
        or selection.get("selected_by") != approved_by
        or selection.get("approved_for_voice_transfer") is not True
        or audition.get("schema_version")
        != "oe-elevenlabs-voice-transfer-owner-approval-evidence-v1"
        or audition.get("owner") != approved_by
        or audition.get("selected_guide", {}).get("sha256") != SELECTED_GUIDE_SHA256
        or audition.get("selected_guide", {}).get("approved_for_voice_changer_transfer")
        is not True
        or audition.get("approved_scope", {}).get("private_voice_changer_microtest")
        is not True
        or audition.get("approved_scope", {}).get("endpoint") != pt.TRANSFER_ENDPOINT
        or audition.get("approved_scope", {}).get("target_voice_id")
        != pt.TRANSFER_TARGET_VOICE_ID
        or audition.get("approved_scope", {}).get("max_provider_calls") != 1
        or audition.get("approved_scope", {}).get("no_retry") is not True
        or audition.get("approved_scope", {}).get("no_redirect") is not True
        or audition.get("approved_scope", {}).get("no_fallback") is not True
        or media.get("schema_version") != MEDIA_CONTRACT_BASIS_SCHEMA
        or records["official_media_contract"][2] != MEDIA_CONTRACT_BASIS_SHA256
    ):
        errors.append("recovery-evidence transfer non-account prerequisites are invalid")
    browser_path = root
    browser_raw = b""
    browser_sha = ""
    browser_at: datetime | None = None
    browser_capture: tuple[Path, bytes, str] = (root, b"", "")
    browser_official: tuple[Path, bytes, str] = (root, b"", "")
    fresh_binding = data_evidence.get("fresh_browser_readiness", {})
    try:
        (
            browser_path,
            browser_document,
            browser_raw,
            browser_sha,
            browser_at,
            browser_capture,
            browser_official,
        ) = _validate_browser_readiness(
            root,
            {"state": "verified", **fresh_binding},
            errors,
            expected_observer=approved_by,
        )
        browser_relative = browser_path.relative_to(root).as_posix()
        capture_relative = browser_capture[0].relative_to(root).as_posix()
        if (
            not _RECOVERY_TRANSFER_BROWSER_PATH_RE.fullmatch(browser_relative)
            or capture_relative != browser_relative.removesuffix(".json") + ".png"
        ):
            raise ValidationError(
                "fresh browser JSON/PNG paths are not the exact additive same-stem pair"
            )
        private_browser_raw, private_browser_sha = _read_recovery_private_bytes(
            root,
            browser_path,
            "fresh browser readiness JSON",
            max_bytes=2_000_000,
        )
        private_capture_raw, private_capture_sha = _read_recovery_private_capture(
            root,
            browser_capture[0],
        )
        if (
            private_browser_raw != browser_raw
            or private_browser_sha != browser_sha
            or private_capture_raw != browser_capture[1]
            or private_capture_sha != browser_capture[2]
        ):
            raise ValidationError(
                "fresh browser JSON/PNG descriptor-bound bytes drifted"
            )
        _verify_recovery_private_capture_git_state(
            runtime_bindings,
            pt._guide_repository_root(),
            browser_capture[0],
        )
        strict_browser_at = _parse_recovery_transfer_time(
            browser_document.get("observed_at"),
            "fresh browser readiness observed_at",
            errors,
        )
        if strict_browser_at != browser_at:
            raise ValidationError(
                "fresh browser readiness timestamp parsing is not exact"
            )
        browser_at = strict_browser_at
    except ValidationError as exc:
        errors.extend(exc.errors)
        browser_document = {}
    if (
        data_evidence.get("fresh_browser_capture")
        != {"path": browser_capture[0].relative_to(root).as_posix(), "sha256": browser_capture[2]}
        or data_evidence.get("official_data_use_basis")
        != {"path": browser_official[0].relative_to(root).as_posix(), "sha256": browser_official[2]}
        or browser_document.get("api_key", {}).get("preview_sha256")
        != account_evidence.get("browser_suffix_sha256")
        or data_observation.get("observed_at") != (
            browser_document.get("observed_at") if browser_document else None
        )
    ):
        errors.append("data-use assurance does not bind the exact fresh JSON/PNG/basis/account preview")
    data_recorded_at = _parse_recovery_transfer_time(
        data_use.get("recorded_at"),
        "recovery data-use assurance recorded_at",
        errors,
    )
    rights_recorded_at = _parse_recovery_transfer_time(
        rights.get("recorded_at"),
        "recovery target-rights recorded_at",
        errors,
    )
    qa_at = _parse_time(qa.get("reviewed_at"), "guide QA reviewed_at", errors)
    selection_at = _parse_time(
        selection.get("selected_at"),
        "owner selection selected_at",
        errors,
    )
    c907_finalized_at = _parse_time(
        audition.get("finalized_at"),
        "owner audition authority finalized_at",
        errors,
    )
    account_recorded_at = account_evidence.get("account_assurance_recorded_at")
    if all(
        isinstance(item, datetime)
        for item in (
            guide_at,
            qa_at,
            selection_at,
            c907_finalized_at,
            account_recorded_at,
            rights_recorded_at,
            browser_at,
            data_recorded_at,
        )
    ):
        assert isinstance(guide_at, datetime)
        assert isinstance(qa_at, datetime)
        assert isinstance(selection_at, datetime)
        assert isinstance(c907_finalized_at, datetime)
        assert isinstance(account_recorded_at, datetime)
        assert isinstance(rights_recorded_at, datetime)
        assert isinstance(browser_at, datetime)
        assert isinstance(data_recorded_at, datetime)
        if not (
            guide_at <= qa_at <= selection_at
            and c907_finalized_at <= rights_recorded_at
            and account_recorded_at <= browser_at
            and rights_recorded_at <= browser_at
            and browser_at <= data_recorded_at
        ):
            errors.append("recovery-evidence transfer record chronology is invalid")
        if not 0 <= (
            data_recorded_at - browser_at
        ).total_seconds() <= DATA_USE_MAX_AGE_SECONDS:
            errors.append(
                "fresh data-use assurance exceeds its recorded browser-evidence window"
            )
    records.update(
        {
            "fresh_browser_readiness": (browser_path, browser_raw, browser_sha),
            "fresh_browser_capture": browser_capture,
            "official_data_use_basis": browser_official,
        }
    )
    for record_name, record in records.items():
        if (
            not isinstance(record, tuple)
            or len(record) != 3
            or not isinstance(record[0], Path)
            or not isinstance(record[1], bytes)
            or not isinstance(record[2], str)
            or not _SHA_RE.fullmatch(record[2])
            or sha256_bytes(record[1]) != record[2]
        ):
            errors.append(
                f"recovery-evidence transfer {record_name} record tuple is invalid"
            )
    try:
        repository = pt._guide_repository_root()
        for record_name in (
            "guide_run", "guide_qa", "owner_selection",
            "owner_audition_confirmation", "official_media_contract",
            "original_c_selection", "original_c_save", "official_data_use_basis",
        ):
            record_path, record_raw, record_sha = records[record_name]
            relative = record_path.relative_to(repository).as_posix()
            committed = _bound_git(
                runtime_bindings,
                ["show", f"{RECOVERY_TRANSFER_OUTCOME_COMMIT}:{relative}"],
                max_bytes=2_000_000,
            )
            if committed != record_raw or sha256_bytes(committed) != record_sha:
                raise ValidationError(
                    f"recovery-evidence transfer historical {record_name} drifted"
                )
    except (KeyError, OSError, UnicodeError, ValidationError, ValueError):
        errors.append(
            "recovery-evidence transfer pre-R0 tracked source proof is invalid"
        )
    return {
        "records": records,
        "selected_audio": selected_audio,
        "guide_completed_at": guide_at,
        "browser_observed_at": browser_at,
        "data_verified_at": data_recorded_at,
        "rights_recorded_at": rights_recorded_at,
    }


def _validate_recovery_transfer_private_phase(
    *,
    root: Path,
    authorization_path: Path,
    authorization_raw: bytes,
    authorization_sha: str,
    authorization: dict[str, Any],
    plan_path: Path,
    canonical_w_path: Path,
    plan_dry: dict[str, Any],
    runtime_bindings: dict[str, Any],
    active: bool,
    blockers: Any,
    materialized_at: datetime | None,
    expires_at: datetime | None,
    errors: list[str],
    allowed_generated_status_paths: frozenset[str] | None = None,
    allowed_ignored_generated_paths: frozenset[str] | None = None,
) -> None:
    """Validate private records without retaining them in a public traceback.

    The caller receives only mutations to ``errors``.  Every exception from the
    private phase is detached and mapped to a fixed diagnostic after all raw
    record, capture, guide, and multipart references have been released.
    """

    account_evidence: dict[str, Any] = {}
    prerequisite_result: dict[str, Any] = {}
    selected_audio = b""
    body = b""
    compiled: dict[str, Any] = {}
    normalized: dict[str, Any] = {}
    private_raw = b""
    expected_delivery: dict[str, Any] = {}
    unexpected_failure = False
    try:
        try:
            account_evidence = _validate_recovery_transfer_account_evidence(
                root,
                authorization.get("account_authentication_evidence"),
                errors,
            )
        except ValidationError as exc:
            exc.__traceback__ = None
            exc.__cause__ = None
            exc.__context__ = None
            errors.append("recovery-evidence account validation stopped safely")
        try:
            prerequisite_result = _validate_recovery_transfer_prerequisites(
                root,
                authorization.get("prerequisites"),
                authorization,
                plan_dry,
                account_evidence,
                runtime_bindings,
                errors,
            )
        except ValidationError as exc:
            exc.__traceback__ = None
            exc.__cause__ = None
            exc.__context__ = None
            errors.append("recovery-evidence prerequisite validation stopped safely")
        try:
            _validate_recovery_transfer_evidence_baseline(
                authorization.get("evidence_baseline"),
                active=active,
                authorization_path=authorization_path,
                authorization_raw=authorization_raw,
                plan_path=plan_path,
                canonical_w_path=canonical_w_path,
                active_materialized_at=materialized_at,
                root=root,
                runtime_bindings=runtime_bindings,
                account_evidence=account_evidence,
                prerequisite_result=prerequisite_result,
                errors=errors,
                allowed_generated_status_paths=allowed_generated_status_paths,
                allowed_ignored_generated_paths=allowed_ignored_generated_paths,
            )
        except ValidationError as exc:
            exc.__traceback__ = None
            exc.__cause__ = None
            exc.__context__ = None
            errors.append("recovery-evidence baseline validation stopped safely")

        selected_audio = prerequisite_result.get("selected_audio", b"")
        if isinstance(selected_audio, bytes):
            compiled, body = pt._compile_multipart_bytes(
                selected_audio,
                SELECTED_GUIDE_SHA256,
                pt.TRANSFER_PRIMARY_FORMAT,
                enable_logging=True,
            )
            _url, normalized, normalized_sha = _normalized_transfer_request(compiled)
            if (
                len(body) != TRANSFER_BODY_BYTES
                or sha256_bytes(body) != TRANSFER_BODY_SHA256
                or sha256_bytes(_compact(compiled)) != TRANSFER_OPT_OUT_REQUEST_SHA256
                or normalized_sha != TRANSFER_OPT_OUT_NORMALIZED_REQUEST_SHA256
                or normalized.get("method") != "POST"
            ):
                errors.append("recovery-evidence transfer compiled request drifted")
        else:
            errors.append("recovery-evidence transfer selected guide bytes are unavailable")

        browser_at = prerequisite_result.get("browser_observed_at")
        data_at = prerequisite_result.get("data_verified_at")
        rights_at = prerequisite_result.get("rights_recorded_at")
        account_at = account_evidence.get("account_assurance_recorded_at")
        try:
            private_raw, private_sha = _read_recovery_private_bytes(
                root,
                authorization_path,
                "recovery-evidence transfer authorization",
                max_bytes=2_000_000,
            )
            if private_raw != authorization_raw or private_sha != authorization_sha:
                errors.append("recovery-evidence transfer private bytes drifted")
        except ValidationError as exc:
            exc.__traceback__ = None
            exc.__cause__ = None
            exc.__context__ = None
            errors.append("recovery-evidence authorization reread stopped safely")

        current = _execution_now()
        if not active:
            if not _exact(
                authorization.get("credential_delivery"),
                _recovery_transfer_credential_delivery(False),
            ):
                errors.append("draft recovery-evidence credential delivery must be pending")
            if (
                authorization.get("provider_action_authorized") is not False
                or authorization.get("execution_ready") is not False
                or authorization.get("expires_at") != ""
                or blockers != RECOVERY_TRANSFER_DRAFT_BLOCKERS
            ):
                errors.append("draft recovery-evidence transfer must retain zero authority")
            if (
                not isinstance(account_at, datetime)
                or not isinstance(rights_at, datetime)
                or not isinstance(browser_at, datetime)
                or not isinstance(data_at, datetime)
                or not isinstance(materialized_at, datetime)
                or max(account_at, rights_at) > browser_at
                or browser_at > data_at
                or data_at > materialized_at
            ):
                errors.append(
                    "draft recovery-evidence transfer chronology is incomplete or invalid"
                )
            if isinstance(materialized_at, datetime) and materialized_at > current:
                errors.append("draft recovery-evidence transfer materialization is in the future")
        else:
            if (
                authorization.get("provider_action_authorized") is not True
                or authorization.get("execution_ready") is not True
                or blockers != []
            ):
                errors.append("active recovery-evidence transfer is not exactly authorized")
            expected_delivery = _recovery_transfer_credential_delivery(
                True,
                fingerprint=account_evidence.get("api_key_fingerprint_sha256"),
                suffix_sha256=account_evidence.get("browser_suffix_sha256"),
            )
            if not _exact(authorization.get("credential_delivery"), expected_delivery):
                errors.append(
                    "active fixed-dotenv delivery does not bind held recovery credential"
                )
            if (
                materialized_at is None
                or expires_at is None
                or not all(
                    isinstance(item, datetime)
                    for item in (account_at, browser_at, data_at, rights_at)
                )
            ):
                errors.append(
                    "active recovery-evidence transfer freshness chain is incomplete"
                )
            else:
                assert isinstance(browser_at, datetime)
                assert isinstance(data_at, datetime)
                assert isinstance(rights_at, datetime)
                assert isinstance(account_at, datetime)
                if (
                    not isinstance(materialized_at, datetime)
                    or not (
                        max(account_at, rights_at) <= browser_at
                        <= data_at <= materialized_at < expires_at
                    )
                ):
                    errors.append(
                        "active recovery-evidence transfer materialization chronology is invalid"
                    )
                if (
                    materialized_at - browser_at
                ).total_seconds() > DATA_USE_MAX_AGE_SECONDS:
                    errors.append(
                        "fresh browser evidence was too old at additive materialization"
                    )
                if expires_at > browser_at + timedelta(seconds=DATA_USE_MAX_AGE_SECONDS):
                    errors.append(
                        "additive authority expiry exceeds the fresh browser window"
                    )
                if not materialized_at <= current < expires_at:
                    errors.append("additive authority is not current at validation")
                if (
                    current < browser_at
                    or (current - browser_at).total_seconds() > DATA_USE_MAX_AGE_SECONDS
                ):
                    errors.append("fresh browser evidence is stale at additive validation")
    except BaseException as exc:
        exc.__traceback__ = None
        exc.__cause__ = None
        exc.__context__ = None
        unexpected_failure = True
    finally:
        account_evidence.clear()
        prerequisite_result.clear()
        selected_audio = b""
        body = b""
        compiled.clear()
        normalized.clear()
        private_raw = b""
        expected_delivery.clear()
    if unexpected_failure:
        errors.append("recovery-evidence transfer private validation stopped safely")


def validate_recovery_evidence_voice_transfer_authorization(
    authorization_path: Path,
    plan_path: Path,
    canonical_w_path: Path,
    *,
    _allowed_generated_status_paths: frozenset[str] | None = None,
    _allowed_ignored_generated_paths: frozenset[str] | None = None,
) -> dict[str, Any]:
    """Validate the additive authority without credentials, writes, or network."""

    authorization_path = Path(authorization_path).absolute()
    plan_path = Path(plan_path).absolute()
    canonical_w_path = Path(canonical_w_path).absolute()
    root = pt._document_root(authorization_path)
    if pt._document_root(plan_path) != root:
        raise ValidationError("recovery-evidence transfer must use the exact plan fixture root")
    authorization, authorization_raw, authorization_sha = pt._read_bound_fixture_json(
        root,
        authorization_path,
        "recovery-evidence voice-transfer authorization",
    )
    _strict(
        authorization,
        {
            "schema_version", "authorization_id", "status",
            "provider_action_authorized", "scope",
            "target", "transaction_basis_id", "evidence_owner", "v1_lineage",
            "bindings", "prerequisites", "action",
            "account_authentication_evidence", "credential_delivery",
            "runtime_bindings", "evidence_baseline", "authorized_limits",
            "artifacts", "consumption", "scope_approval", "materialized_by",
            "materialized_at", "expires_at",
            "execution_ready", "blockers",
        },
        "recovery-evidence voice-transfer authorization",
    )
    errors: list[str] = []
    status = authorization.get("status")
    active = status == "active"
    if status not in {"draft", "active"}:
        errors.append("recovery-evidence transfer status must be draft or active")
    _validate_authorization_location(
        authorization_path,
        root,
        status,
        "recovery-evidence transfer authorization",
        errors,
    )
    if authorization.get("schema_version") != RECOVERY_TRANSFER_AUTH_SCHEMA:
        errors.append("recovery-evidence transfer schema mismatch")
    if authorization.get("scope") != RECOVERY_TRANSFER_SCOPE:
        errors.append("recovery-evidence transfer scope mismatch")
    if (
        authorization.get("transaction_basis_id")
        != RECOVERY_TRANSFER_TRANSACTION_BASIS_ID
        or authorization.get("evidence_owner") != RECOVERY_TRANSFER_OWNER
        or authorization.get("scope_approval") != _recovery_transfer_scope_approval()
        or authorization.get("materialized_by") != "Codex"
    ):
        errors.append("recovery-evidence transfer transaction/scope basis drifted")
    expected_authorization_id = (
        RECOVERY_TRANSFER_ACTIVE_ID if active else RECOVERY_TRANSFER_DRAFT_ID
    )
    expected_authorization_path = (
        RECOVERY_TRANSFER_ACTIVE_PATH if active else RECOVERY_TRANSFER_DRAFT_PATH
    )
    authorization_id = authorization.get("authorization_id")
    try:
        actual_authorization_path = authorization_path.relative_to(root).as_posix()
    except ValueError:
        actual_authorization_path = "invalid"
    if (
        authorization_id != expected_authorization_id
        or actual_authorization_path != expected_authorization_path
    ):
        errors.append("recovery-evidence transfer authorization identity is not exact")
        authorization_id = expected_authorization_id
    _target(authorization.get("target"), root, errors)
    plan_dry = pt.validate_performance_transfer_plan(plan_path, canonical_w_path)
    lineage_path, _lineage, lineage_raw, lineage_sha = _validate_lineage(
        root,
        authorization.get("v1_lineage"),
        plan_path,
        canonical_w_path,
    )
    expected_bindings = _recovery_transfer_bindings(plan_dry)
    bindings = _strict(
        authorization.get("bindings"),
        set(expected_bindings),
        "recovery-evidence transfer bindings",
    )
    if not _exact(bindings, expected_bindings):
        errors.append("recovery-evidence transfer exact request bindings drifted")
    if not _exact(authorization.get("action"), _action_transfer(True)):
        errors.append("recovery-evidence transfer exact action drifted")
    runtime_bindings = _validate_recovery_transfer_runtime_bindings(
        authorization.get("runtime_bindings"),
        active=True,
        errors=errors,
    )
    try:
        repository = pt._guide_repository_root()
        plan_raw, plan_sha = _read_bound_blob(
            repository,
            plan_path,
            "recovery-evidence transfer performance plan",
            max_bytes=2_000_000,
        )
        canonical_raw, canonical_sha = _read_bound_blob(
            repository,
            canonical_w_path,
            "recovery-evidence transfer canonical W",
            max_bytes=2_000_000,
        )
        preexisting = (
            (plan_path, plan_raw, plan_sha, expected_bindings["performance_transfer_plan_sha256"]),
            (canonical_w_path, canonical_raw, canonical_sha, expected_bindings["canonical_w_sha256"]),
            (lineage_path, lineage_raw, lineage_sha, V1_LINEAGE_SHA256),
        )
        for source_path, source_raw, source_sha, expected_sha in preexisting:
            relative = source_path.relative_to(repository).as_posix()
            historical = _bound_git(
                runtime_bindings,
                ["show", f"{RECOVERY_TRANSFER_OUTCOME_COMMIT}:{relative}"],
                max_bytes=2_000_000,
            )
            if (
                source_sha != expected_sha
                or historical != source_raw
                or sha256_bytes(historical) != expected_sha
            ):
                raise ValidationError(
                    "recovery-evidence transfer preexisting input drifted"
                )
    except (KeyError, OSError, UnicodeError, ValidationError, ValueError):
        errors.append(
            "recovery-evidence transfer plan/canonical/lineage Git proof is invalid"
        )
    if not _exact(authorization.get("authorized_limits"), _transfer_limits(active)):
        errors.append("recovery-evidence transfer limits drifted")
    if not _exact(authorization.get("artifacts"), _recovery_transfer_artifacts(active)):
        errors.append("recovery-evidence transfer artifact paths drifted")
    if not _exact(authorization.get("consumption"), _recovery_transfer_consumption(active)):
        errors.append("recovery-evidence transfer shared latch state drifted")
    blockers = authorization.get("blockers")
    if not isinstance(blockers, list) or any(
        not isinstance(item, str) or not item for item in blockers
    ):
        errors.append("recovery-evidence transfer blockers must be strings")
    materialized_at = _parse_recovery_transfer_time(
        authorization.get("materialized_at"),
        "recovery-evidence transfer materialized_at",
        errors,
    )
    expires_at = (
        _parse_recovery_transfer_time(
            authorization.get("expires_at"),
            "recovery-evidence transfer expires_at",
            errors,
        )
        if active
        else None
    )
    if (
        active
        and isinstance(materialized_at, datetime)
        and isinstance(expires_at, datetime)
        and not materialized_at < expires_at
    ):
        errors.append("recovery-evidence transfer expiry must follow materialization")

    _validate_recovery_transfer_private_phase(
        root=root,
        authorization_path=authorization_path,
        authorization_raw=authorization_raw,
        authorization_sha=authorization_sha,
        authorization=authorization,
        plan_path=plan_path,
        canonical_w_path=canonical_w_path,
        plan_dry=plan_dry,
        runtime_bindings=runtime_bindings,
        active=active,
        blockers=blockers,
        materialized_at=materialized_at,
        expires_at=expires_at,
        errors=errors,
        allowed_generated_status_paths=_allowed_generated_status_paths,
        allowed_ignored_generated_paths=_allowed_ignored_generated_paths,
    )
    if errors:
        authorization.clear()
        authorization_raw = b""
        plan_dry.clear()
        _lineage.clear()
        lineage_raw = b""
    _raise_errors(errors)
    return {
        "schema_version": RECOVERY_TRANSFER_DRY_RUN_SCHEMA,
        "valid": True,
        "status": (
            "active_exact_isolated_worker_authority_validated"
            if active
            else "blocked_pending_active_recovery_evidence_transfer_authorization"
        ),
        "authorization_status": status,
        "authorization_id": authorization_id,
        "authorization_sha256": authorization_sha,
        "materialized_at": _iso(materialized_at) if materialized_at else None,
        "expires_at": _iso(expires_at) if expires_at else None,
        "v1_lineage_sha256": lineage_sha,
        "bindings": bindings,
        "action": authorization.get("action"),
        "account_authentication_evidence": authorization.get(
            "account_authentication_evidence"
        ),
        "credential_delivery": authorization.get("credential_delivery"),
        "maximum": _transfer_limits(active),
        "artifacts": _recovery_transfer_artifacts(active),
        "provider_action_authorized": active,
        "account_get_calls_authorized": 0,
        "generation_post_calls_authorized": 1 if active else 0,
        "credentials_accessed": False,
        "network_called": False,
        "provider_calls_made": 0,
        "retry_permitted": False,
        "replay_permitted": False,
        "redirect_permitted": False,
        "application_fallback_permitted": False,
        "network_stack_address_selection_state": (
            "stdlib_internal_connection_selection_possible" if active else "not_applicable"
        ),
        "identity_observed": False,
        "ui_api_account_equality_state": "unknown",
        "exact_ui_api_account_equality_verified": False,
        "exact_ui_api_account_equality_claimed": False,
        "target_voice_accessibility_state": "unknown",
        "creative_approved": False,
        "full_capture_authorized": False,
        "step2_lock_authorized": False,
        "step3_authorized": False,
        "sharing_authorized": False,
        "publication_authorized": False,
    }


def dry_run_recovery_evidence_voice_transfer(
    authorization_path: Path,
    plan_path: Path,
    canonical_w_path: Path,
) -> dict[str, Any]:
    return validate_recovery_evidence_voice_transfer_authorization(
        authorization_path,
        plan_path,
        canonical_w_path,
    )


# ---------------------------------------------------------------------------
# Additive recovery-evidence transfer execution
# ---------------------------------------------------------------------------


RECOVERY_TRANSFER_EXECUTION_FAILURE_CODES = frozenset(
    {
        *_PARENT_TRANSFER_WORKER_FAILURE_CODES,
        "active_authority_revalidation_failed",
        "authorization_expired_before_go",
        "compiled_request_body_binding_failed",
        "core_dump_protection_failed",
        "credential_fingerprint_mismatch",
        "credential_suffix_mismatch",
        "fixed_dotenv_read_failed",
        "immutable_latch_revalidation_failed",
        "local_conversion_failed_closed",
        "local_destination_or_receipt_failure",
        "local_source_revalidation_failed",
        "provider_pcm_compressed_signature_forbidden",
        "provider_pcm_container_signature_forbidden",
        "provider_pcm_duration_out_of_bounds",
        "provider_pcm_payload_invalid",
        "provider_pcm_payload_silent",
        "provider_pcm_source_duration_coherence_failed",
        "response_completed_outside_authority",
        "unexpected_local_failure",
        "worker_identity_revalidation_failed",
    }
)


@dataclass(frozen=True, repr=False)
class _RecoveryTransferInputBinding:
    name: str
    path: Path
    sha256: str
    byte_count: int
    mode: int
    uid: int
    nlink: int
    private: bool


@dataclass(repr=False)
class _RecoveryTransferExecutionContract:
    root: Path
    authorization_path: Path
    authorization: dict[str, Any]
    authorization_sha256: str
    plan_path: Path
    canonical_w_path: Path
    body: bytearray
    normalized_request: dict[str, Any]
    inputs: tuple[_RecoveryTransferInputBinding, ...]
    materialized_at: datetime
    expires_at: datetime
    browser_observed_at: datetime
    account_recorded_at: datetime
    data_recorded_at: datetime
    rights_recorded_at: datetime
    expected_fingerprint_sha256: str
    expected_suffix_sha256: str
    git_head: str
    consumption_relative: str
    raw_relative: str
    working_relative: str
    success_relative: str
    failure_relative: str
    conversion_relative: str


@dataclass(frozen=True)
class _RecoveryTransferCoreLimit:
    soft: int
    hard: int


_RECOVERY_TRANSFER_CONTAINMENT_QUARANTINE: list[_PreparedVoiceTransferWorker] = []


def _dispose_recovery_transfer_worker(
    worker: _PreparedVoiceTransferWorker,
) -> bool:
    for _attempt in range(3):
        if _dispose_prepared_transfer_worker(worker):
            return True
    if all(item is not worker for item in _RECOVERY_TRANSFER_CONTAINMENT_QUARANTINE):
        _RECOVERY_TRANSFER_CONTAINMENT_QUARANTINE.append(worker)
    return False


def _require_recovery_transfer_containment_clear() -> None:
    pending = list(_RECOVERY_TRANSFER_CONTAINMENT_QUARANTINE)
    _RECOVERY_TRANSFER_CONTAINMENT_QUARANTINE.clear()
    retained: list[_PreparedVoiceTransferWorker] = []
    for worker in pending:
        reaped = False
        for _attempt in range(3):
            if _dispose_prepared_transfer_worker(worker):
                reaped = True
                break
        if not reaped:
            retained.append(worker)
    _RECOVERY_TRANSFER_CONTAINMENT_QUARANTINE.extend(retained)
    if retained:
        raise ValidationError("an isolated recovery-transfer worker remains containment-unconfirmed")


def _recovery_transfer_hash(domain: bytes, value: bytearray) -> str:
    digest = hashlib.sha256()
    digest.update(domain)
    digest.update(value)
    return digest.hexdigest()


def _recovery_transfer_suffix_hash(value: bytearray) -> str:
    if len(value) < 4:
        return ""
    digest = hashlib.sha256()
    digest.update(API_KEY_PREVIEW_DOMAIN)
    view = memoryview(value)
    try:
        digest.update(view[len(value) - 4 :])
    finally:
        view.release()
    return digest.hexdigest()


def _preflight_recovery_transfer_core_limit() -> _RecoveryTransferCoreLimit:
    """Prove RLIMIT_CORE can be lowered and restored before authority burns."""

    try:
        soft, hard = resource.getrlimit(resource.RLIMIT_CORE)
        resource.setrlimit(resource.RLIMIT_CORE, (0, hard))
        if resource.getrlimit(resource.RLIMIT_CORE) != (0, hard):
            raise OSError("core limit did not lower")
        resource.setrlimit(resource.RLIMIT_CORE, (soft, hard))
        if resource.getrlimit(resource.RLIMIT_CORE) != (soft, hard):
            raise OSError("core limit did not restore")
    except (OSError, ValueError):
        raise ValidationError("recovery transfer core-dump protection is unavailable") from None
    return _RecoveryTransferCoreLimit(soft=soft, hard=hard)


def _enter_recovery_transfer_core_limit(limit: _RecoveryTransferCoreLimit) -> None:
    try:
        if resource.getrlimit(resource.RLIMIT_CORE) != (limit.soft, limit.hard):
            raise OSError("core limit changed after preflight")
        resource.setrlimit(resource.RLIMIT_CORE, (0, limit.hard))
        if resource.getrlimit(resource.RLIMIT_CORE) != (0, limit.hard):
            raise OSError("core limit did not lower")
    except (OSError, ValueError):
        raise pt._GuideExecutionFailure("core_dump_protection_failed") from None


def _restore_recovery_transfer_core_limit(limit: _RecoveryTransferCoreLimit) -> bool:
    try:
        resource.setrlimit(resource.RLIMIT_CORE, (limit.soft, limit.hard))
        return resource.getrlimit(resource.RLIMIT_CORE) == (limit.soft, limit.hard)
    except (OSError, ValueError):
        return False


def _recovery_transfer_input_binding(
    name: str,
    path: Path,
    raw: bytes,
    digest: str,
) -> _RecoveryTransferInputBinding:
    try:
        metadata = os.stat(path, follow_symlinks=False)
    except OSError:
        raise ValidationError(f"recovery transfer input {name} is unavailable") from None
    if (
        not stat.S_ISREG(metadata.st_mode)
        or metadata.st_nlink != 1
        or metadata.st_uid != os.getuid()
        or not raw
        or len(raw) != metadata.st_size
        or sha256_bytes(raw) != digest
    ):
        raise ValidationError(f"recovery transfer input {name} identity is unsafe")
    mode = stat.S_IMODE(metadata.st_mode)
    if mode not in {0o600, 0o644}:
        raise ValidationError(f"recovery transfer input {name} mode is unsafe")
    return _RecoveryTransferInputBinding(
        name=name,
        path=path.absolute(),
        sha256=digest,
        byte_count=len(raw),
        mode=mode,
        uid=metadata.st_uid,
        nlink=metadata.st_nlink,
        private=mode == 0o600,
    )


def _revalidate_recovery_transfer_input(
    contract: _RecoveryTransferExecutionContract,
    binding: _RecoveryTransferInputBinding,
) -> None:
    if binding.private:
        raw, digest = _read_recovery_private_bytes(
            pt._guide_repository_root(),
            binding.path,
            f"held recovery transfer input {binding.name}",
            max_bytes=max(binding.byte_count, 1),
        )
    else:
        raw, digest = _read_bound_blob(
            pt._guide_repository_root(),
            binding.path,
            f"held recovery transfer input {binding.name}",
            max_bytes=max(binding.byte_count, 1),
            required_mode=binding.mode,
            required_uid=binding.uid,
        )
    try:
        metadata = os.stat(binding.path, follow_symlinks=False)
    except OSError:
        raw = b""
        raise ValidationError(f"held recovery transfer input {binding.name} disappeared") from None
    if (
        digest != binding.sha256
        or len(raw) != binding.byte_count
        or not stat.S_ISREG(metadata.st_mode)
        or stat.S_IMODE(metadata.st_mode) != binding.mode
        or metadata.st_uid != binding.uid
        or metadata.st_nlink != binding.nlink
        or metadata.st_size != binding.byte_count
    ):
        raw = b""
        raise ValidationError(f"held recovery transfer input {binding.name} drifted")
    raw = b""


def _build_recovery_transfer_execution_contract(
    authorization_path: Path,
    plan_path: Path,
    canonical_w_path: Path,
) -> _RecoveryTransferExecutionContract:
    """Validate, compile, and reduce private inputs to safe immutable bindings."""

    validation = validate_recovery_evidence_voice_transfer_authorization(
        authorization_path,
        plan_path,
        canonical_w_path,
    )
    if (
        validation.get("valid") is not True
        or validation.get("authorization_status") != "active"
        or validation.get("provider_action_authorized") is not True
    ):
        raise ValidationError("recovery transfer execution requires exact committed ACTIVE authority")
    authorization_path = Path(authorization_path).absolute()
    plan_path = Path(plan_path).absolute()
    canonical_w_path = Path(canonical_w_path).absolute()
    root = pt._document_root(authorization_path)
    authorization_raw = b""
    selected_audio = b""
    compiled_body = b""
    body = bytearray()
    account_evidence: dict[str, Any] = {}
    prerequisite_result: dict[str, Any] = {}
    compiled: dict[str, Any] = {}
    normalized: dict[str, Any] = {}
    authorization: dict[str, Any] = {}
    plan_dry: dict[str, Any] = {}
    all_records: dict[str, tuple[Path, bytes, str]] = {}
    records: dict[str, tuple[Path, bytes, str]] = {}
    result: dict[str, Any] = {}
    record: tuple[Path, bytes, str] | None = None
    raw = b""
    digest = ""
    draft_raw = b""
    draft_sha = ""
    contract: _RecoveryTransferExecutionContract | None = None
    inputs: list[_RecoveryTransferInputBinding] = []
    build_failed = False
    try:
        authorization_raw, authorization_sha = _read_recovery_private_bytes(
            root,
            authorization_path,
            "active recovery-evidence transfer authorization",
            max_bytes=2_000_000,
        )
        if authorization_sha != validation.get("authorization_sha256"):
            raise ValidationError("active recovery transfer authorization changed after validation")
        authorization = pt._strict_json_bytes(
            authorization_raw,
            "active recovery-evidence transfer authorization",
        )
        plan_dry = pt.validate_performance_transfer_plan(plan_path, canonical_w_path)
        errors: list[str] = []
        account_evidence = _validate_recovery_transfer_account_evidence(
            root,
            authorization.get("account_authentication_evidence"),
            errors,
        )
        prerequisite_result = _validate_recovery_transfer_prerequisites(
            root,
            authorization.get("prerequisites"),
            authorization,
            plan_dry,
            account_evidence,
            authorization["runtime_bindings"],
            errors,
        )
        _raise_errors(errors)
        selected_audio = prerequisite_result.get("selected_audio", b"")
        if not isinstance(selected_audio, bytes):
            raise ValidationError("recovery transfer selected guide bytes are unavailable")
        compiled, compiled_body = pt._compile_multipart_bytes(
            selected_audio,
            SELECTED_GUIDE_SHA256,
            pt.TRANSFER_PRIMARY_FORMAT,
            enable_logging=True,
        )
        _url, normalized, normalized_sha = _normalized_transfer_request(compiled)
        if (
            len(compiled_body) != TRANSFER_BODY_BYTES
            or sha256_bytes(compiled_body) != TRANSFER_BODY_SHA256
            or sha256_bytes(_compact(compiled)) != TRANSFER_OPT_OUT_REQUEST_SHA256
            or normalized_sha != TRANSFER_OPT_OUT_NORMALIZED_REQUEST_SHA256
        ):
            raise ValidationError("recovery transfer compiled request body drifted")
        body.extend(compiled_body)

        for prefix, result in (
            ("account", account_evidence),
            ("prerequisite", prerequisite_result),
        ):
            records = result.get("records")
            if not isinstance(records, dict):
                raise ValidationError(f"recovery transfer {prefix} records are unavailable")
            for name, record in records.items():
                if (
                    not isinstance(record, tuple)
                    or len(record) != 3
                    or not isinstance(record[0], Path)
                    or not isinstance(record[1], bytes)
                    or not isinstance(record[2], str)
                ):
                    raise ValidationError(f"recovery transfer {prefix} record shape is invalid")
                all_records[f"{prefix}:{name}"] = record
        all_records["authorization:active"] = (
            authorization_path,
            authorization_raw,
            authorization_sha,
        )
        for name, path in (("plan", plan_path), ("canonical_w", canonical_w_path)):
            raw, digest = _read_bound_blob(
                pt._guide_repository_root(),
                path,
                f"recovery transfer {name}",
                max_bytes=2_000_000,
            )
            all_records[f"source:{name}"] = (path, raw, digest)
        draft_binding = authorization["evidence_baseline"]["draft_authorization"]
        draft_path = root / draft_binding["path"]
        draft_raw, draft_sha = _read_recovery_private_bytes(
            root,
            draft_path,
            "recovery transfer R1 DRAFT",
            max_bytes=2_000_000,
        )
        if draft_sha != draft_binding["sha256"]:
            raise ValidationError("recovery transfer R1 DRAFT changed after validation")
        all_records["authorization:draft"] = (draft_path, draft_raw, draft_sha)
        for name, (path, raw, digest) in sorted(all_records.items()):
            inputs.append(_recovery_transfer_input_binding(name, path, raw, digest))
        all_records.clear()

        time_errors: list[str] = []
        materialized_at = _parse_recovery_transfer_time(
            authorization.get("materialized_at"),
            "active recovery transfer materialized_at",
            time_errors,
        )
        expires_at = _parse_recovery_transfer_time(
            authorization.get("expires_at"),
            "active recovery transfer expires_at",
            time_errors,
        )
        browser_at = prerequisite_result.get("browser_observed_at")
        data_at = prerequisite_result.get("data_verified_at")
        rights_at = prerequisite_result.get("rights_recorded_at")
        account_at = account_evidence.get("account_assurance_recorded_at")
        if (
            time_errors
            or not all(
                isinstance(item, datetime)
                for item in (
                    materialized_at,
                    expires_at,
                    browser_at,
                    data_at,
                    rights_at,
                    account_at,
                )
            )
        ):
            raise ValidationError("recovery transfer execution chronology is unavailable")
        credential_delivery = authorization["credential_delivery"]
        expected_fingerprint = credential_delivery.get("api_key_fingerprint_sha256")
        expected_suffix = credential_delivery.get("browser_suffix_sha256")
        if (
            not isinstance(expected_fingerprint, str)
            or not _SHA_RE.fullmatch(expected_fingerprint)
            or not isinstance(expected_suffix, str)
            or not _SHA_RE.fullmatch(expected_suffix)
        ):
            raise ValidationError("recovery transfer credential hash bindings are invalid")
        git_head = _bound_git(
            authorization["runtime_bindings"],
            ["rev-parse", "HEAD"],
        ).strip().decode("ascii", errors="strict")
        if not _GIT_SHA_RE.fullmatch(git_head):
            raise ValidationError("recovery transfer execution HEAD is invalid")
        artifacts = authorization["artifacts"]
        contract = _RecoveryTransferExecutionContract(
            root=root,
            authorization_path=authorization_path,
            authorization=authorization,
            authorization_sha256=authorization_sha,
            plan_path=plan_path,
            canonical_w_path=canonical_w_path,
            body=body,
            normalized_request=dict(normalized),
            inputs=tuple(inputs),
            materialized_at=materialized_at,
            expires_at=expires_at,
            browser_observed_at=browser_at,
            account_recorded_at=account_at,
            data_recorded_at=data_at,
            rights_recorded_at=rights_at,
            expected_fingerprint_sha256=expected_fingerprint,
            expected_suffix_sha256=expected_suffix,
            git_head=git_head,
            consumption_relative=authorization["consumption"]["record_path"],
            raw_relative=artifacts["raw_output_path"],
            working_relative=artifacts["working_output_path"],
            success_relative=artifacts["success_receipt_path"],
            failure_relative=artifacts["failure_receipt_path"],
            conversion_relative=artifacts["conversion_receipt_path"],
        )
        body = bytearray()
        returned_contract = contract
        contract = None
        authorization = {}
        return returned_contract
    except BaseException as exc:
        if isinstance(exc, ValidationError):
            code = "recovery transfer execution contract did not validate"
        else:
            code = "recovery transfer execution contract stopped safely"
        exc.__traceback__ = None
        exc.__cause__ = None
        exc.__context__ = None
        build_failed = True
    finally:
        authorization_raw = b""
        selected_audio = b""
        compiled_body = b""
        compiled.clear()
        normalized.clear()
        authorization.clear()
        plan_dry.clear()
        validation.clear()
        account_evidence.clear()
        prerequisite_result.clear()
        all_records.clear()
        records.clear()
        result.clear()
        record = None
        raw = b""
        digest = ""
        draft_raw = b""
        draft_sha = ""
        if contract is not None:
            _zero_mutable_buffer(contract.body)
        contract = None
        inputs = []
        if build_failed:
            _zero_mutable_buffer(body)
    raise ValidationError(code) from None


def _recovery_transfer_destination_path(
    contract: _RecoveryTransferExecutionContract,
    relative: str,
    suffix: str,
) -> Path:
    return pt._safe_relative(
        contract.root,
        relative,
        "recovery-evidence transfer destination",
        must_exist=False,
        suffix=suffix,
    )


@dataclass(frozen=True)
class _RecoveryTransferWriteState:
    created: bool
    verified_complete: bool
    sha256: str | None
    byte_count: int | None


def _exclusive_recovery_transfer_write(
    root: Path,
    relative: str,
    data: bytes,
) -> _RecoveryTransferWriteState:
    """Expose O_EXCL creation separately from full durable verification."""

    parent_fd, name = pt._open_parent_descriptor(root, relative, create_parents=False)
    descriptor: int | None = None
    created = False
    verified = False
    observed_size: int | None = None
    try:
        flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
        flags |= getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_CLOEXEC", 0)
        descriptor = os.open(name, flags, 0o600, dir_fd=parent_fd)
        created = True
        os.fchmod(descriptor, 0o600)
        view = memoryview(data)
        try:
            written = 0
            while written < len(view):
                count = os.write(descriptor, view[written:])
                if count <= 0:
                    raise OSError("short private artifact write")
                written += count
        finally:
            view.release()
        os.fsync(descriptor)
        metadata = os.fstat(descriptor)
        observed_size = metadata.st_size
        if (
            not stat.S_ISREG(metadata.st_mode)
            or stat.S_IMODE(metadata.st_mode) != 0o600
            or metadata.st_uid != os.getuid()
            or metadata.st_nlink != 1
            or metadata.st_size != len(data)
        ):
            raise OSError("created private artifact identity mismatch")
        os.fsync(parent_fd)
        verified = True
    except BaseException as write_failure:
        verified = False
        if descriptor is not None:
            try:
                observed_size = os.fstat(descriptor).st_size
            except OSError:
                observed_size = None
        write_failure.__traceback__ = None
        write_failure.__cause__ = None
        write_failure.__context__ = None
    finally:
        if descriptor is not None:
            os.close(descriptor)
        os.close(parent_fd)
    return _RecoveryTransferWriteState(
        created=created,
        verified_complete=verified,
        sha256=sha256_bytes(data) if verified else None,
        byte_count=observed_size,
    )


def _preflight_recovery_transfer_destinations(
    contract: _RecoveryTransferExecutionContract,
    *,
    latch_exists: bool,
) -> None:
    relatives = [
        contract.consumption_relative,
        contract.raw_relative,
        contract.working_relative,
        contract.success_relative,
        contract.failure_relative,
        contract.conversion_relative,
    ]
    pt._ensure_execution_parents(contract.root, relatives)
    expected = (
        (contract.consumption_relative, ".json", ("authorizations", "consumed")),
        (contract.raw_relative, ".pcm", ("outputs", "raw", "elevenlabs")),
        (contract.working_relative, ".wav", ("outputs", "working", "elevenlabs")),
        (contract.success_relative, ".json", ("receipts", "elevenlabs")),
        (contract.failure_relative, ".json", ("receipts", "elevenlabs")),
        (contract.conversion_relative, ".json", ("receipts", "elevenlabs")),
    )
    if len(set(relatives)) != len(relatives):
        raise ValidationError("recovery transfer destinations are not globally distinct")
    for relative, suffix, prefix in expected:
        path = _recovery_transfer_destination_path(contract, relative, suffix)
        if path.relative_to(contract.root).parts[: len(prefix)] != prefix:
            raise ValidationError("recovery transfer destination escaped its artifact class")
        should_exist = latch_exists and relative == contract.consumption_relative
        try:
            os.stat(path, follow_symlinks=False)
            exists = True
        except FileNotFoundError:
            exists = False
        except OSError:
            raise ValidationError("recovery transfer destination state is unsafe") from None
        if exists != should_exist:
            raise ValidationError("recovery transfer destination collision or missing latch")


def _recovery_transfer_consumption_receipt(
    contract: _RecoveryTransferExecutionContract,
    worker: _PreparedVoiceTransferWorker,
    consumed_at: datetime,
) -> dict[str, Any]:
    return {
        "schema_version": RECOVERY_TRANSFER_CONSUMPTION_SCHEMA,
        "authorization_id": contract.authorization["authorization_id"],
        "authorization_path": contract.authorization_path.relative_to(contract.root).as_posix(),
        "authorization_sha256": contract.authorization_sha256,
        "scope": RECOVERY_TRANSFER_SCOPE,
        "status": "consumed_before_credential_and_network",
        "consumed_at": _iso(consumed_at),
        "consumed_before_credential_access": True,
        "credential_accessed_at_consumption": False,
        "network_called_at_consumption": False,
        "account_get_calls_used": 0,
        "generation_post_budget_consumed": True,
        "generation_post_calls_observed": 0,
        "outputs_received": 0,
        "spend_used_usd": 0,
        "primary_request_sha256": contract.authorization["bindings"]["primary_request_sha256"],
        "multipart_body_sha256": TRANSFER_BODY_SHA256,
        "worker_ready_before_consumption": True,
        "worker_source_sha256": worker.worker_source_sha256,
        "worker_interpreter_sha256": worker.interpreter_sha256,
        "retry_or_replay_permitted": False,
    }


def _verify_recovery_transfer_latch(
    contract: _RecoveryTransferExecutionContract,
    expected: bytes,
) -> None:
    path = contract.root / contract.consumption_relative
    raw, digest = _read_recovery_private_bytes(
        contract.root,
        path,
        "recovery transfer shared global latch",
        max_bytes=2_000_000,
    )
    if raw != expected or digest != sha256_bytes(expected):
        raw = b""
        raise ValidationError("recovery transfer shared global latch drifted")
    raw = b""


def _verify_recovery_transfer_post_latch_git_scope(
    contract: _RecoveryTransferExecutionContract,
    runtime: dict[str, Any],
) -> str:
    """Require the exact untracked, nonignored latch as the sole local delta."""

    repository = pt._guide_repository_root()
    try:
        relative = (contract.root / contract.consumption_relative).relative_to(
            repository
        ).as_posix()
    except ValueError:
        raise ValidationError("recovery transfer latch is outside the repository") from None
    status = _bound_git(
        runtime,
        ["status", "--porcelain=v1", "--untracked-files=all", "-z"],
    )
    if status != b"?? " + relative.encode("utf-8") + b"\x00":
        raise ValidationError("recovery transfer post-latch worktree scope is not exact")
    if _bound_git(runtime, ["ls-files", "--stage", "--", relative]) != b"":
        raise ValidationError("recovery transfer latch unexpectedly entered the index")
    ignore_state = _bound_git(
        runtime,
        ["check-ignore", "--no-index", "-v", "--non-matching", "--", relative],
        allowed_returncodes=(1,),
    )
    if ignore_state != b"::\t" + relative.encode("utf-8") + b"\n":
        raise ValidationError("recovery transfer latch is unexpectedly ignored")
    return relative


def _verify_recovery_transfer_pre_latch_git_scope(
    contract: _RecoveryTransferExecutionContract,
    runtime: dict[str, Any],
) -> str:
    repository = pt._guide_repository_root()
    try:
        relative = (contract.root / contract.consumption_relative).relative_to(
            repository
        ).as_posix()
    except ValueError:
        raise ValidationError("recovery transfer latch is outside the repository") from None
    if _bound_git(
        runtime,
        ["status", "--porcelain=v1", "--untracked-files=all", "-z"],
    ) != b"":
        raise ValidationError("recovery transfer pre-latch worktree is not clean")
    if _bound_git(runtime, ["ls-files", "--stage", "--", relative]) != b"":
        raise ValidationError("recovery transfer latch path unexpectedly exists in the index")
    ignore_state = _bound_git(
        runtime,
        ["check-ignore", "--no-index", "-v", "--non-matching", "--", relative],
        allowed_returncodes=(1,),
    )
    if ignore_state != b"::\t" + relative.encode("utf-8") + b"\n":
        raise ValidationError("recovery transfer latch path is unexpectedly ignored")
    return relative


def _revalidate_recovery_transfer_contract(
    contract: _RecoveryTransferExecutionContract,
    worker: _PreparedVoiceTransferWorker,
    latch_bytes: bytes,
    *,
    current: datetime,
) -> dict[str, Any]:
    errors: list[str] = []
    runtime = _validate_recovery_transfer_runtime_bindings(
        contract.authorization.get("runtime_bindings"),
        active=True,
        errors=errors,
    )
    if errors:
        raise ValidationError("recovery transfer runtime binding changed after latch")
    head = _bound_git(runtime, ["rev-parse", "HEAD"]).strip().decode("ascii", errors="strict")
    if head != contract.git_head:
        raise ValidationError("recovery transfer Git HEAD changed after latch")
    _verify_recovery_transfer_latch(contract, latch_bytes)
    _revalidate_prepared_transfer_worker(worker)
    latch_repository_relative = _verify_recovery_transfer_post_latch_git_scope(
        contract,
        runtime,
    )
    for binding in contract.inputs:
        _revalidate_recovery_transfer_input(contract, binding)
    _preflight_recovery_transfer_destinations(contract, latch_exists=True)
    if (
        current < contract.browser_observed_at
        or (current - contract.browser_observed_at).total_seconds()
        > DATA_USE_MAX_AGE_SECONDS
        or not contract.materialized_at <= current < contract.expires_at
        or sha256_bytes(contract.body) != TRANSFER_BODY_SHA256
        or len(contract.body) != TRANSFER_BODY_BYTES
    ):
        raise ValidationError("recovery transfer authority or held body is no longer current")
    return {
        "runtime_commit": runtime["git_commit"],
        "evidence_commit": contract.authorization["evidence_baseline"]["evidence_commit"],
        "active_commit": head,
        "worker_source_sha256": worker.worker_source_sha256,
        "worker_interpreter_sha256": worker.interpreter_sha256,
        "input_sha256s": {
            binding.name: binding.sha256 for binding in contract.inputs
        },
        "remote_state_checked": False,
        "git_network_called": False,
        "post_latch_git_status_path": latch_repository_relative,
        "post_latch_git_status_state": "sole_untracked_nonignored_latch",
        "post_latch_revalidation_completed": True,
        "source_revalidated_after_latch": True,
    }


def _revalidate_recovery_transfer_before_latch(
    contract: _RecoveryTransferExecutionContract,
    worker: _PreparedVoiceTransferWorker,
) -> dict[str, Any]:
    errors: list[str] = []
    runtime = _validate_recovery_transfer_runtime_bindings(
        contract.authorization.get("runtime_bindings"),
        active=True,
        errors=errors,
    )
    if errors:
        raise ValidationError("recovery transfer runtime changed before latch")
    head = _bound_git(runtime, ["rev-parse", "HEAD"]).strip().decode("ascii", errors="strict")
    if head != contract.git_head:
        raise ValidationError("recovery transfer Git HEAD changed before latch")
    latch_repository_relative = _verify_recovery_transfer_pre_latch_git_scope(
        contract,
        runtime,
    )
    for binding in contract.inputs:
        _revalidate_recovery_transfer_input(contract, binding)
    _revalidate_prepared_transfer_worker(worker)
    _preflight_recovery_transfer_destinations(contract, latch_exists=False)
    current = _execution_now()
    if (
        not contract.materialized_at <= current < contract.expires_at
        or current < contract.browser_observed_at
        or (current - contract.browser_observed_at).total_seconds()
        > DATA_USE_MAX_AGE_SECONDS
        or len(contract.body) != TRANSFER_BODY_BYTES
        or sha256_bytes(contract.body) != TRANSFER_BODY_SHA256
    ):
        raise ValidationError("recovery transfer authority expired before latch")
    return {
        "runtime_commit": runtime["git_commit"],
        "evidence_commit": contract.authorization["evidence_baseline"]["evidence_commit"],
        "active_commit": head,
        "worker_source_sha256": worker.worker_source_sha256,
        "worker_interpreter_sha256": worker.interpreter_sha256,
        "input_sha256s": {
            binding.name: binding.sha256 for binding in contract.inputs
        },
        "remote_state_checked": False,
        "git_network_called": False,
        "pre_latch_git_status_path": latch_repository_relative,
        "pre_latch_git_status_state": "clean_and_latch_untracked_nonignored",
        "post_latch_revalidation_completed": False,
        "source_revalidated_before_latch": True,
    }


def _recovery_transfer_execution_failure(
    code: str,
    *,
    go_released: bool,
    response: _ElevenResponse | None = None,
) -> pt._GuideExecutionFailure:
    if code not in RECOVERY_TRANSFER_EXECUTION_FAILURE_CODES:
        code = "unexpected_local_failure"
    failure = (
        _post_go_worker_failure(
            code,
            response_state="confirmed" if response is not None else "unknown",
            http_status=200 if response is not None else None,
            response_bytes=response.response_bytes if response is not None else 0,
            response_sha256=response.response_sha256 if response is not None else None,
            provider_identifiers=(
                dict(response.provider_identifiers) if response is not None else {}
            ),
            provider_usage=dict(response.provider_usage) if response is not None else {},
        )
        if go_released
        else _pre_go_worker_failure(code)
    )
    if response is not None:
        failure.provider_request_state = "response_confirmed"
        failure.provider_response_state = "body_complete"
        failure.application_http_attempts = 1
        failure.provider_output_state = "received_not_persisted"
    else:
        failure.application_http_attempts = 0
    return failure


def _recovery_transfer_failure_receipt(
    contract: _RecoveryTransferExecutionContract,
    *,
    latch_sha256: str | None,
    latch_verified_complete: bool,
    source_proof: dict[str, Any],
    failure: pt._GuideExecutionFailure,
    credential_read_attempts: int,
    credential_access_state: str,
    started_at: datetime | None,
    failed_at: datetime | None,
    raw_state: _RecoveryTransferWriteState,
    run_state: _RecoveryTransferWriteState,
    conversion_completed: bool,
) -> dict[str, Any]:
    code = failure.code
    if code not in RECOVERY_TRANSFER_EXECUTION_FAILURE_CODES:
        code = "unexpected_local_failure"
    go_released = getattr(failure, "post_budget_consumed", False) is True
    request_state = getattr(
        failure,
        "provider_request_state",
        "unknown_after_go" if go_released else "not_started",
    )
    response_state = getattr(
        failure,
        "provider_response_state",
        "unknown" if go_released else "none",
    )
    attempts = getattr(failure, "application_http_attempts", 0)
    if type(attempts) is not int or attempts not in {0, 1}:
        attempts = 0
    response_confirmed = response_state in {
        "headers_confirmed",
        "headers_rejected",
        "body_complete",
        "body_rejected",
        "confirmed",
    }
    return {
        "schema_version": RECOVERY_TRANSFER_FAILURE_SCHEMA,
        "outcome": "failed_closed",
        "provider": "elevenlabs",
        "scope": RECOVERY_TRANSFER_SCOPE,
        "method": "POST",
        "endpoint": pt.TRANSFER_ENDPOINT,
        "part_id": "P01-W0030-W0110",
        "authorization_id": contract.authorization["authorization_id"],
        "authorization_path": contract.authorization_path.relative_to(contract.root).as_posix(),
        "authorization_sha256": contract.authorization_sha256,
        "consumption_record_path": contract.consumption_relative,
        "consumption_record_sha256": latch_sha256,
        "consumption_record_verified_complete": latch_verified_complete,
        "source_proof": source_proof,
        "primary_request_sha256": contract.authorization["bindings"]["primary_request_sha256"],
        "normalized_http_request_sha256": contract.authorization["bindings"][
            "normalized_http_request_sha256"
        ],
        "multipart_body_sha256": TRANSFER_BODY_SHA256,
        "multipart_body_bytes": TRANSFER_BODY_BYTES,
        "failure_code": code,
        "primary_failure_code": getattr(failure, "primary_failure_code", None),
        "child_containment_state": getattr(
            failure,
            "child_containment_state",
            "confirmed_reaped" if go_released else "credential_free_worker_closed",
        ),
        "credential_descriptor_read_attempts": credential_read_attempts,
        "credential_access_state": credential_access_state,
        "credential_accessed": credential_access_state
        in {"bytes_read_not_accepted", "bytes_read_held_unverified", "held_and_verified"},
        "credential_fingerprint_sha256": contract.expected_fingerprint_sha256,
        "account_get_calls_made": 0,
        "generation_post_budget_consumed": True,
        "go_released": go_released,
        "application_http_attempt_limit": 1,
        "application_http_attempts": attempts,
        "application_retries_made": 0,
        "application_redirects_followed": 0,
        "application_fallbacks_used": 0,
        "network_stack_address_selection_state": (
            "stdlib_internal_connection_selection_possible"
            if go_released
            else "not_applicable"
        ),
        "network_call_state": (
            "application_request_started"
            if attempts == 1
            else ("unknown_after_go" if go_released else "not_called")
        ),
        "provider_request_state": request_state,
        "provider_response_state": response_state,
        "provider_mutation_state": (
            "potentially_ambiguous" if go_released else "none"
        ),
        "provider_output_state": (
            "potentially_ambiguous" if go_released else "none"
        ),
        "provider_response_received": response_confirmed,
        "http_status": failure.http_status,
        "response_bytes": failure.response_bytes,
        "response_sha256": failure.response_sha256,
        "provider_identifiers": dict(failure.provider_identifiers),
        "provider_usage": dict(failure.provider_usage),
        "outputs_received": 1 if response_state == "body_complete" else 0,
        "raw_output_created": raw_state.created,
        "raw_output_verified_complete": raw_state.verified_complete,
        "raw_output_observed_byte_count": raw_state.byte_count,
        "run_receipt_created": run_state.created,
        "run_receipt_verified_complete": run_state.verified_complete,
        "working_output_and_conversion_receipt_verified_complete": conversion_completed,
        "started_at": _iso(started_at) if started_at is not None else None,
        "failed_at": _iso(failed_at) if failed_at is not None else None,
        "retry_permitted": False,
        "replay_permitted": False,
        "reconciliation_required": go_released
        and not (
            raw_state.verified_complete
            and run_state.verified_complete
            and conversion_completed
        ),
        "modeled_spend_state": "potentially_incurred" if go_released else "none",
        "modeled_spend_ceiling_usd": TRANSFER_MAX_SPEND_USD,
        "modeled_spend_provider_enforced": False,
        "credentials_recorded": False,
        "raw_credential_stored": False,
        "raw_provider_body_stored": raw_state.created,
        "creative_approved": False,
        "full_capture_authorized": False,
        "step2_lock_authorized": False,
        "step3_authorized": False,
        "sharing_authorized": False,
        "publication_authorized": False,
    }


def _recovery_transfer_success_receipt(
    contract: _RecoveryTransferExecutionContract,
    *,
    latch_sha256: str,
    source_proof: dict[str, Any],
    response: _ElevenResponse,
    geometry: dict[str, Any],
    raw_sha256: str,
    started_at: datetime,
    completed_at: datetime,
) -> dict[str, Any]:
    prerequisites = {
        name: binding["sha256"]
        for name, binding in sorted(contract.authorization["prerequisites"].items())
    }
    return {
        "schema_version": RECOVERY_TRANSFER_RUN_SCHEMA,
        "outcome": "success",
        "provider": "elevenlabs",
        "scope": RECOVERY_TRANSFER_SCOPE,
        "method": "POST",
        "endpoint": pt.TRANSFER_ENDPOINT,
        "part_id": "P01-W0030-W0110",
        "authorization_id": contract.authorization["authorization_id"],
        "authorization_path": contract.authorization_path.relative_to(contract.root).as_posix(),
        "authorization_sha256": contract.authorization_sha256,
        "consumption_record_path": contract.consumption_relative,
        "consumption_record_sha256": latch_sha256,
        "source_proof": source_proof,
        "plan_sha256": contract.authorization["bindings"]["performance_transfer_plan_sha256"],
        "canonical_w_sha256": contract.authorization["bindings"]["canonical_w_sha256"],
        "spoken_text_sha256": contract.authorization["bindings"]["spoken_text_sha256"],
        "selected_guide_sha256": SELECTED_GUIDE_SHA256,
        "selected_guide_run_receipt_sha256": SELECTED_GUIDE_RUN_SHA256,
        "prerequisite_sha256s": prerequisites,
        "account_authentication_evidence": dict(
            contract.authorization["account_authentication_evidence"]
        ),
        "credential_fingerprint_sha256": contract.expected_fingerprint_sha256,
        "browser_suffix_sha256": contract.expected_suffix_sha256,
        "credential_descriptor_read_attempts": 1,
        "credential_access_state": "held_and_verified",
        "child_containment_state": "confirmed_reaped",
        "request": {
            "part_id": "P01-W0030-W0110",
            "primary_request_sha256": contract.authorization["bindings"]["primary_request_sha256"],
            "normalized_http_request_sha256": contract.authorization["bindings"][
                "normalized_http_request_sha256"
            ],
            "method": "POST",
            "exact_url": contract.normalized_request["url"],
            "multipart_body_sha256": TRANSFER_BODY_SHA256,
            "multipart_body_bytes": TRANSFER_BODY_BYTES,
            "content_type": TRANSFER_CONTENT_TYPE,
            "credential_header_name": "xi-api-key",
            "accept": "application/octet-stream",
            "accept_encoding": "identity",
        },
        "provider_evidence": {
            "account_get_calls_made": 0,
            "generation_post_budget_consumed": True,
            "generation_post_calls_made": 1,
            "application_http_attempt_limit": 1,
            "application_http_attempts": 1,
            "application_retries_made": 0,
            "application_redirects_followed": 0,
            "application_fallbacks_used": 0,
            "network_stack_address_selection_state": (
                "stdlib_internal_connection_selection_possible"
            ),
            "outputs_received": 1,
            "request_ids": dict(response.provider_identifiers),
            "usage": dict(response.provider_usage),
        },
        "response": {
            "http_status": 200,
            "provider_request_state": "response_confirmed",
            "provider_response_state": "body_complete",
            "response_bytes": response.response_bytes,
            "response_sha256": response.response_sha256,
            "declared_mime_type": response.content_type,
            "content_encoding": response.content_encoding,
            "media_interpretation": {
                "classification": "interpreted_pcm_under_exact_format_contract",
                "output_format": "pcm_48000",
                "declared_mime_allowlist": ["audio/pcm", "audio/mpeg"],
                "compressed_or_container_signature_detected": False,
                "negative_ffprobe_detected_format": False,
                "headerless_bytes_intrinsically_prove_codec_geometry": False,
                "official_media_contract_sha256": MEDIA_CONTRACT_BASIS_SHA256,
            },
        },
        "raw_output": {
            "part_id": "P01-W0030-W0110",
            "path": contract.raw_relative,
            "sha256": raw_sha256,
            "byte_count": response.response_bytes,
            **geometry,
        },
        "working_output_path": contract.working_relative,
        "conversion_receipt_path": contract.conversion_relative,
        "started_at": _iso(started_at),
        "completed_at": _iso(completed_at),
        "modeled_spend_usd": TRANSFER_MAX_SPEND_USD,
        "modeled_spend_basis": "voice_changer_full_minute_worst_case",
        "modeled_spend_provider_enforced": False,
        "taxes_included": False,
        "credentials_recorded": False,
        "raw_credential_stored": False,
        "creative_approved": False,
        "full_capture_authorized": False,
        "step2_lock_authorized": False,
        "step3_authorized": False,
        "sharing_authorized": False,
        "publication_authorized": False,
    }


def _finalize_recovery_transfer_failure(
    contract: _RecoveryTransferExecutionContract,
    *,
    latch_sha256: str | None,
    latch_verified_complete: bool,
    source_proof: dict[str, Any],
    failure: pt._GuideExecutionFailure,
    credential_read_attempts: int,
    credential_access_state: str,
    started_at: datetime | None,
    raw_state: _RecoveryTransferWriteState,
    run_state: _RecoveryTransferWriteState,
    conversion_completed: bool,
) -> tuple[str, _RecoveryTransferWriteState]:
    """Serialize terminal evidence without exposing sensitive caller locals."""

    failure_receipt: dict[str, Any] = {}
    failure_bytes = b""
    write_state = _RecoveryTransferWriteState(False, False, None, None)
    code = (
        failure.code
        if failure.code in RECOVERY_TRANSFER_EXECUTION_FAILURE_CODES
        else "unexpected_local_failure"
    )
    try:
        try:
            failed_at = _execution_now()
        except BaseException as clock_failure:
            clock_failure.__traceback__ = None
            clock_failure.__cause__ = None
            clock_failure.__context__ = None
            failed_at = None
        failure_receipt = _recovery_transfer_failure_receipt(
            contract,
            latch_sha256=latch_sha256,
            latch_verified_complete=latch_verified_complete,
            source_proof=source_proof,
            failure=failure,
            credential_read_attempts=credential_read_attempts,
            credential_access_state=credential_access_state,
            started_at=started_at,
            failed_at=failed_at,
            raw_state=raw_state,
            run_state=run_state,
            conversion_completed=conversion_completed,
        )
        failure_bytes = _receipt_bytes(failure_receipt)
        if pt._scan_for_secrets(failure_receipt):
            return code, write_state
        write_state = _exclusive_recovery_transfer_write(
            contract.root,
            contract.failure_relative,
            failure_bytes,
        )
        return code, write_state
    except BaseException as terminal_failure:
        terminal_failure.__traceback__ = None
        terminal_failure.__cause__ = None
        terminal_failure.__context__ = None
        return code, write_state
    finally:
        failure_receipt.clear()
        failure_bytes = b""


def execute_recovery_evidence_voice_transfer(
    authorization_path: Path,
    plan_path: Path,
    canonical_w_path: Path,
    *,
    timeout: float = 60.0,
) -> dict[str, Any]:
    """Consume one shared latch and release at most one isolated POST."""

    if (
        type(timeout) not in {int, float}
        or not 0 < float(timeout) <= TRANSFER_MAX_ELAPSED_SECONDS
    ):
        raise ValidationError("recovery transfer timeout must be greater than zero and at most 300 seconds")
    _require_recovery_transfer_containment_clear()
    core_limit = _preflight_recovery_transfer_core_limit()
    contract: _RecoveryTransferExecutionContract | None = None
    worker: _PreparedVoiceTransferWorker | None = None
    key_material = bytearray()
    response: _ElevenResponse | None = None
    failure: pt._GuideExecutionFailure | None = None
    source_proof: dict[str, Any] = {}
    geometry: dict[str, Any] = {}
    conversion: dict[str, Any] = {}
    success_result: dict[str, Any] | None = None
    latch_bytes = b""
    latch_sha256: str | None = None
    run_bytes = b""
    raw_sha256 = ""
    consumed_at: datetime | None = None
    started_at: datetime | None = None
    credential_read_attempts = 0
    credential_access_state = "not_attempted"
    latch_state = _RecoveryTransferWriteState(False, False, None, None)
    raw_state = _RecoveryTransferWriteState(False, False, None, None)
    run_state = _RecoveryTransferWriteState(False, False, None, None)
    failure_write_state = _RecoveryTransferWriteState(False, False, None, None)
    conversion_completed = False
    core_limit_entered = False
    pre_latch_failure = "recovery transfer pre-latch readiness failed"
    pre_latch_containment_unconfirmed = False
    try:
        # Everything through READY and final destination/source checks is
        # credential-free and reversible.  No latch exists on any failure here.
        contract = _build_recovery_transfer_execution_contract(
            authorization_path,
            plan_path,
            canonical_w_path,
        )
        worker = _prepare_voice_transfer_worker()
        _preflight_recovery_transfer_destinations(contract, latch_exists=False)
        source_proof = _revalidate_recovery_transfer_before_latch(contract, worker)

        consumed_at = _execution_now()
        latch = _recovery_transfer_consumption_receipt(contract, worker, consumed_at)
        latch_bytes = _receipt_bytes(latch)
        if pt._scan_for_secrets(latch):
            raise ValidationError("recovery transfer latch secret scan failed")
        latch_state = _exclusive_recovery_transfer_write(
            contract.root,
            contract.consumption_relative,
            latch_bytes,
        )
        if not latch_state.created:
            raise ValidationError("recovery transfer latch could not be exclusively created")
        if not latch_state.verified_complete:
            raise _pre_go_worker_failure("immutable_latch_revalidation_failed")
        latch_sha256 = latch_state.sha256
        try:
            _verify_recovery_transfer_latch(contract, latch_bytes)
        except ValidationError:
            raise _pre_go_worker_failure("immutable_latch_revalidation_failed") from None
        try:
            _verify_recovery_transfer_post_latch_git_scope(
                contract,
                contract.authorization["runtime_bindings"],
            )
        except ValidationError:
            raise _pre_go_worker_failure("local_source_revalidation_failed") from None

        _enter_recovery_transfer_core_limit(core_limit)
        core_limit_entered = True
        try:
            credential_read_attempts = 1
            try:
                key_material = _read_recovery_transfer_dotenv_key()
                credential_access_state = "bytes_read_held_unverified"
            except _RecoveryTransferCredentialReadFailure as credential_failure:
                credential_access_state = credential_failure.credential_bytes_read_state
                credential_failure.__traceback__ = None
                credential_failure.__cause__ = None
                credential_failure.__context__ = None
                raise _pre_go_worker_failure("fixed_dotenv_read_failed") from None
            if (
                _recovery_transfer_hash(API_KEY_DOMAIN, key_material)
                != contract.expected_fingerprint_sha256
            ):
                raise _pre_go_worker_failure("credential_fingerprint_mismatch")
            if (
                _recovery_transfer_suffix_hash(key_material)
                != contract.expected_suffix_sha256
            ):
                raise _pre_go_worker_failure("credential_suffix_mismatch")
            credential_access_state = "held_and_verified"

            # The held mutable credential is never re-read.  Recheck exact
            # sources, ACTIVE freshness, latch bytes, destinations, and READY
            # process immediately before GO.
            try:
                _verify_recovery_transfer_latch(contract, latch_bytes)
            except ValidationError:
                raise _pre_go_worker_failure("immutable_latch_revalidation_failed") from None
            try:
                _revalidate_prepared_transfer_worker(worker)
            except ValidationError:
                raise _pre_go_worker_failure("worker_identity_revalidation_failed") from None
            try:
                post_latch_proof = _revalidate_recovery_transfer_contract(
                    contract,
                    worker,
                    latch_bytes,
                    current=_execution_now(),
                )
            except ValidationError:
                raise _pre_go_worker_failure("local_source_revalidation_failed") from None
            source_proof.update(post_latch_proof)
            post_latch_proof.clear()

            # Bind the parent hard deadline to the earliest caller cap, ACTIVE
            # expiry, or one-hour browser-evidence expiry.  Sampling monotonic
            # before wall time is conservative under scheduling delay.
            go_monotonic_ns = time.monotonic_ns()
            started_at = _execution_now()
            authority_deadline = min(
                contract.expires_at,
                contract.browser_observed_at
                + timedelta(seconds=DATA_USE_MAX_AGE_SECONDS),
            )
            remaining_authority = (authority_deadline - started_at).total_seconds()
            effective_timeout = min(float(timeout), remaining_authority)
            if (
                not contract.materialized_at <= started_at < authority_deadline
                or effective_timeout <= 0
            ):
                raise _pre_go_worker_failure("authorization_expired_before_go")
            absolute_deadline_ns = go_monotonic_ns + max(
                1,
                int(effective_timeout * 1_000_000_000),
            )
            response = _perform_prepared_voice_transfer(
                worker,
                api_key_material=key_material,
                body=contract.body,
                timeout=float(timeout),
                absolute_deadline_ns=absolute_deadline_ns,
            )
            worker = None
        except pt._GuideExecutionFailure as credential_or_worker_failure:
            failure = credential_or_worker_failure
            credential_or_worker_failure.__traceback__ = None
            credential_or_worker_failure.__cause__ = None
            credential_or_worker_failure.__context__ = None
        except BaseException as credential_phase_failure:
            credential_phase_failure.__traceback__ = None
            credential_phase_failure.__cause__ = None
            credential_phase_failure.__context__ = None
            failure = _recovery_transfer_execution_failure(
                "unexpected_local_failure",
                go_released=False,
            )
        finally:
            _zero_mutable_buffer(key_material)
            if contract is not None:
                _zero_mutable_buffer(contract.body)
            if core_limit_entered:
                restored = _restore_recovery_transfer_core_limit(core_limit)
                core_limit_entered = False
                if not restored:
                    primary_failure = failure
                    go_released = response is not None or (
                        primary_failure is not None
                        and getattr(primary_failure, "post_budget_consumed", False) is True
                    )
                    replacement = _recovery_transfer_execution_failure(
                        "core_dump_protection_failed",
                        go_released=go_released,
                        response=response,
                    )
                    if primary_failure is not None:
                        replacement.primary_failure_code = primary_failure.code
                        replacement.provider_request_state = getattr(
                            primary_failure,
                            "provider_request_state",
                            replacement.provider_request_state,
                        )
                        replacement.provider_response_state = getattr(
                            primary_failure,
                            "provider_response_state",
                            replacement.provider_response_state,
                        )
                        replacement.application_http_attempts = getattr(
                            primary_failure,
                            "application_http_attempts",
                            replacement.application_http_attempts,
                        )
                        replacement.http_status = primary_failure.http_status
                        replacement.response_bytes = primary_failure.response_bytes
                        replacement.response_sha256 = primary_failure.response_sha256
                        replacement.provider_identifiers = dict(
                            primary_failure.provider_identifiers
                        )
                        replacement.provider_usage = dict(primary_failure.provider_usage)
                    failure = replacement

        if failure is not None:
            raise failure

        assert contract is not None
        assert response is not None
        completed_at = _execution_now()
        authority_deadline = min(
            contract.expires_at,
            contract.browser_observed_at + timedelta(seconds=DATA_USE_MAX_AGE_SECONDS),
        )
        if started_at is None or not started_at <= completed_at <= authority_deadline:
            raise _recovery_transfer_execution_failure(
                "response_completed_outside_authority",
                go_released=True,
                response=response,
            )
        if response.content_type not in {"audio/pcm", "audio/mpeg"} or response.content_encoding != "identity":
            raise _recovery_transfer_execution_failure(
                "provider_pcm_payload_invalid",
                go_released=True,
                response=response,
            )
        try:
            geometry = _validate_raw_pcm(
                response.payload,
                ffprobe_path=contract.authorization["runtime_bindings"]["ffprobe_binary_path"],
                ffprobe_sha256=contract.authorization["runtime_bindings"]["ffprobe_binary_sha256"],
                ffprobe_version=contract.authorization["runtime_bindings"]["ffprobe_version"],
            )
        except pt._GuideExecutionFailure as media_failure:
            code = media_failure.code
            media_failure.__traceback__ = None
            raise _recovery_transfer_execution_failure(
                code,
                go_released=True,
                response=response,
            ) from None
        _preflight_recovery_transfer_destinations(contract, latch_exists=True)
        raw_state = _exclusive_recovery_transfer_write(
            contract.root,
            contract.raw_relative,
            response.payload,
        )
        if not raw_state.verified_complete:
            raise _recovery_transfer_execution_failure(
                "local_destination_or_receipt_failure",
                go_released=True,
                response=response,
            )
        pt._verify_private_fixture_artifact(
            contract.root,
            contract.raw_relative,
            response.payload,
            "recovery transfer raw PCM output",
        )
        raw_sha256 = sha256_bytes(response.payload)
        run = _recovery_transfer_success_receipt(
            contract,
            latch_sha256=latch_sha256,
            source_proof=source_proof,
            response=response,
            geometry=geometry,
            raw_sha256=raw_sha256,
            started_at=started_at,
            completed_at=completed_at,
        )
        run_bytes = _receipt_bytes(run)
        if pt._scan_for_secrets(run):
            raise _recovery_transfer_execution_failure(
                "local_destination_or_receipt_failure",
                go_released=True,
                response=response,
            )
        run_state = _exclusive_recovery_transfer_write(
            contract.root,
            contract.success_relative,
            run_bytes,
        )
        if not run_state.verified_complete:
            raise _recovery_transfer_execution_failure(
                "local_destination_or_receipt_failure",
                go_released=True,
                response=response,
            )
        from .audio import convert_recovery_evidence_working

        try:
            conversion = convert_recovery_evidence_working(
                contract.root / contract.raw_relative,
                contract.root / contract.working_relative,
                receipt_path=contract.root / contract.success_relative,
                part_id="P01-W0030-W0110",
                record_path=contract.root / contract.conversion_relative,
            )
        except ValidationError:
            raise _recovery_transfer_execution_failure(
                "local_conversion_failed_closed",
                go_released=True,
                response=response,
            ) from None
        conversion_completed = True
        success_result = {
            "schema_version": RECOVERY_TRANSFER_RESULT_SCHEMA,
            "valid": True,
            "outcome": "success",
            "authorization_id": contract.authorization["authorization_id"],
            "authorization_consumed": True,
            "credential_descriptor_read_attempts": 1,
            "account_get_calls_made": 0,
            "generation_post_budget_consumed": True,
            "generation_post_calls_made": 1,
            "application_retries_made": 0,
            "application_redirects_followed": 0,
            "application_fallbacks_used": 0,
            "network_stack_address_selection_state": (
                "stdlib_internal_connection_selection_possible"
            ),
            "outputs_received": 1,
            "modeled_spend_usd": TRANSFER_MAX_SPEND_USD,
            "modeled_spend_basis": "voice_changer_full_minute_worst_case",
            "modeled_spend_provider_enforced": False,
            "taxes_included": False,
            "run_receipt": {
                "path": contract.success_relative,
                "sha256": sha256_bytes(run_bytes),
            },
            "raw_output": {"path": contract.raw_relative, "sha256": raw_sha256},
            "working_output": {
                "path": contract.working_relative,
                "sha256": conversion["working"]["sha256"],
            },
            "conversion_receipt": {
                "path": contract.conversion_relative,
                "sha256": sha256_file(contract.root / contract.conversion_relative),
            },
            "network_called": True,
            "credential_access_state": "held_and_verified",
            "credentials_accessed": True,
            "child_containment_state": "confirmed_reaped",
            "retry_permitted": False,
            "replay_permitted": False,
            "creative_approved": False,
            "full_capture_authorized": False,
            "step2_lock_authorized": False,
            "step3_authorized": False,
            "sharing_authorized": False,
            "publication_authorized": False,
        }
    except pt._GuideExecutionFailure as execution_failure:
        failure = execution_failure
        execution_failure.__traceback__ = None
        execution_failure.__cause__ = None
        execution_failure.__context__ = None
    except ValidationError as validation_failure:
        if not latch_state.created:
            validation_failure.__traceback__ = None
            validation_failure.__cause__ = None
            validation_failure.__context__ = None
            pre_latch_failure = "recovery transfer pre-latch readiness failed"
        validation_failure.__traceback__ = None
        validation_failure.__cause__ = None
        validation_failure.__context__ = None
        if latch_state.created:
            failure = _recovery_transfer_execution_failure(
                "local_destination_or_receipt_failure",
                go_released=response is not None,
                response=response,
            )
    except BaseException as unexpected:
        unexpected.__traceback__ = None
        unexpected.__cause__ = None
        unexpected.__context__ = None
        if not latch_state.created:
            pre_latch_failure = "recovery transfer pre-latch readiness stopped safely"
        else:
            failure = _recovery_transfer_execution_failure(
                "unexpected_local_failure",
                go_released=response is not None,
                response=response,
            )
    finally:
        _zero_mutable_buffer(key_material)
        if contract is not None:
            _zero_mutable_buffer(contract.body)
        if core_limit_entered:
            _restore_recovery_transfer_core_limit(core_limit)
            core_limit_entered = False
        if worker is not None:
            worker_go_released = worker.state != "ready"
            reaped = _dispose_recovery_transfer_worker(worker)
            if not reaped and latch_state.created:
                primary_failure_code = (
                    failure.code if failure is not None else "unexpected_local_failure"
                )
                containment_failure = _recovery_transfer_execution_failure(
                    "isolated_worker_reap_failure",
                    go_released=worker_go_released
                    or (
                        failure is not None
                        and getattr(failure, "post_budget_consumed", False) is True
                    ),
                    response=response,
                )
                containment_failure.primary_failure_code = primary_failure_code
                containment_failure.child_containment_state = (
                    "sigkill_sent_reap_unconfirmed"
                )
                if failure is not None:
                    containment_failure.provider_request_state = getattr(
                        failure,
                        "provider_request_state",
                        containment_failure.provider_request_state,
                    )
                    containment_failure.provider_response_state = getattr(
                        failure,
                        "provider_response_state",
                        containment_failure.provider_response_state,
                    )
                    containment_failure.application_http_attempts = getattr(
                        failure,
                        "application_http_attempts",
                        containment_failure.application_http_attempts,
                    )
                    containment_failure.http_status = failure.http_status
                    containment_failure.response_bytes = failure.response_bytes
                    containment_failure.response_sha256 = failure.response_sha256
                    containment_failure.provider_identifiers = dict(
                        failure.provider_identifiers
                    )
                    containment_failure.provider_usage = dict(failure.provider_usage)
                failure = containment_failure
                success_result = None
                conversion_completed = False
            elif not reaped:
                pre_latch_containment_unconfirmed = True
            worker = None

    if success_result is not None:
        response = None
        geometry.clear()
        conversion.clear()
        source_proof.clear()
        run_bytes = b""
        latch_bytes = b""
        contract = None
        return success_result
    if contract is None or failure is None or not latch_state.created:
        if contract is not None:
            _zero_mutable_buffer(contract.body)
        response = None
        failure = None
        geometry.clear()
        conversion.clear()
        source_proof.clear()
        run_bytes = b""
        latch_bytes = b""
        contract = None
        if pre_latch_containment_unconfirmed:
            raise ValidationError(
                "recovery transfer pre-latch worker containment is unconfirmed"
            ) from None
        raise ValidationError(pre_latch_failure) from None
    code, failure_write_state = _finalize_recovery_transfer_failure(
        contract,
        latch_sha256=latch_sha256,
        latch_verified_complete=latch_state.verified_complete,
        source_proof=source_proof,
        failure=failure,
        credential_read_attempts=credential_read_attempts,
        credential_access_state=credential_access_state,
        started_at=started_at,
        raw_state=raw_state,
        run_state=run_state,
        conversion_completed=conversion_completed,
    )
    response = None
    failure = None
    run_bytes = b""
    latch_bytes = b""
    geometry.clear()
    conversion.clear()
    source_proof.clear()
    contract = None
    suffix = (
        "failure receipt persisted"
        if failure_write_state.verified_complete
        else (
            "failure receipt created but not verified complete"
            if failure_write_state.created
            else "failure receipt unavailable"
        )
    )
    raise ValidationError(
        f"recovery transfer stopped permanently without retry: {code}; {suffix}"
    ) from None
