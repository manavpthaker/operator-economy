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
import os
import re
import shutil
import ssl
import stat
import subprocess
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
FIXTURE_ID = "step2-v0.5-ai-visibility-v1.1-synthetic-guide-to-saved-c-transfer-microtest"

TRANSFER_EXEC_AUTH_SCHEMA = "oe-voice-transfer-execution-authorization-v2"
TRANSFER_EXEC_SCOPE = "elevenlabs_voice_transfer_execution"
TRANSFER_RUN_SCHEMA = "oe-elevenlabs-voice-transfer-run-v1"
TRANSFER_FAILURE_SCHEMA = "oe-elevenlabs-voice-transfer-failure-v1"
TRANSFER_CONSUMPTION_SCHEMA = "oe-elevenlabs-voice-transfer-consumption-v1"

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
) -> bytes:
    return pt._guide_git(
        arguments,
        max_bytes=max_bytes,
        git_path=runtime_bindings["git_binary_path"],
        git_sha256=runtime_bindings["git_binary_sha256"],
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
