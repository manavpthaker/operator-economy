"""Fail-closed audio inspection and the single permitted working conversion."""

from __future__ import annotations

import json
import math
import os
import re
import secrets
import selectors
import signal
import stat
import subprocess
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from .core import ValidationError, read_json, sha256_bytes, sha256_file


_CAPTURE_RUN_SCHEMA = "oe-provider-capture-run-v1"
_DIRECTED_RUN_SCHEMA = "oe-elevenlabs-directed-bakeoff-run-v1"
_TRANSFER_RUN_SCHEMA = "oe-elevenlabs-voice-transfer-run-v1"
_TRANSFER_AUTH_SCHEMA = "oe-voice-transfer-execution-authorization-v2"
_TRANSFER_CONSUMPTION_SCHEMA = "oe-elevenlabs-voice-transfer-consumption-v1"
_TRANSFER_SCOPE = "elevenlabs_voice_transfer_execution"
_TRANSFER_PART_ID = "P01-W0030-W0110"
_TRANSFER_RAW_PATH = "outputs/raw/elevenlabs/P01-W0030-W0110/saved-c-transfer.pcm"
_TRANSFER_WORKING_PATH = (
    "outputs/working/elevenlabs/P01-W0030-W0110/saved-c-transfer.wav"
)
_TRANSFER_SAMPLE_RATE_HZ = 48_000
_TRANSFER_MIN_DURATION_SECONDS = 20.0
_TRANSFER_MAX_DURATION_SECONDS = 50.0
_TRANSFER_SELECTED_GUIDE_DURATION_SECONDS = 34.290958333333336
_TRANSFER_MIN_OUTPUT_TO_SOURCE_DURATION_RATIO = 0.8
_TRANSFER_MAX_OUTPUT_TO_SOURCE_DURATION_RATIO = 1.2
_TRANSFER_MEDIA_CONTRACT_PATH = (
    "evidence/"
    "V1-ELEVENLABS-PCM48000-MEDIA-CONTRACT-BASIS.20260826T073836Z.json"
)
_TRANSFER_MEDIA_CONTRACT_SHA256 = (
    "175feb4d640d48a0fa4fc4f8e8e278478e8c5bd32bb89c9087974ebb149d78a9"
)
_TRANSFER_DECLARED_MIME_ALLOWLIST = ("audio/pcm", "audio/mpeg")
_TRANSFER_PROVIDER_ID_KEYS = frozenset(
    {"request-id", "x-request-id", "eleven-request-id"}
)
_TRANSFER_USAGE_KEYS = frozenset(
    {
        "request-cost",
        "character-count",
        "x-ratelimit-limit",
        "x-ratelimit-remaining",
        "x-ratelimit-reset",
    }
)
_TRANSFER_PREREQUISITE_KEYS = frozenset(
    {
        "selected_guide",
        "guide_qa",
        "owner_selection",
        "owner_audition_confirmation",
        "elevenlabs_data_use",
        "target_voice_rights",
        "credential_account_verification",
        "official_media_contract",
    }
)
_TRANSFER_SOURCE_RECORD_KEYS = frozenset(
    {
        "qa",
        "selection",
        "audition",
        "data_use",
        "data_evidence",
        "data_evidence_capture",
        "official_data_use_basis",
        "official_media_contract",
        "account_receipt",
        "account_authorization",
        "account_owner_approval",
        "account_consumption",
        "rights",
        "original_c_selection",
        "original_c_save",
        "lineage",
        "selected_guide",
        "guide_run",
        "plan",
        "canonical_w",
    }
)
_TRANSFER_COMMITTED_SOURCE_RECORD_KEYS = frozenset(
    {
        "plan",
        "canonical_w",
        "lineage",
        "official_data_use_basis",
        "official_media_contract",
        "account_authorization",
    }
)
_TRANSFER_LOCAL_PRIVATE_SOURCE_RECORD_KEYS = frozenset(
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
_TRANSFER_SELECTED_GUIDE_KEYS = frozenset(
    {
        "state",
        "path",
        "sha256",
        "byte_count",
        "duration_seconds",
        "container",
        "codec",
        "sample_rate_hz",
        "channels",
        "guide_request_id",
        "guide_run_receipt_path",
        "guide_run_receipt_sha256",
    }
)
_SAFE_PROVIDER_VALUE_RE = re.compile(r"^[A-Za-z0-9._:/;=+\-]{1,256}$")
_SECRET_PROVIDER_VALUE_RE = re.compile(
    r"(?:AIza[0-9A-Za-z_-]{20,}|ya29\.[0-9A-Za-z._-]+|xi[_-][0-9A-Za-z_-]{12,}|sk[_-][0-9A-Za-z_-]{12,})"
)
_HEX_40_RE = re.compile(r"^[0-9a-f]{40}$")
_HEX_64_RE = re.compile(r"^[0-9a-f]{64}$")
_TRANSFER_JSON_BYTE_CAP = 4_000_000
_TRANSFER_SOURCE_RECORD_BYTE_CAP = 16_000_000
_TRANSFER_RAW_BYTE_CAP = int(
    _TRANSFER_MAX_DURATION_SECONDS * _TRANSFER_SAMPLE_RATE_HZ * 2
)
_TRANSFER_MEDIA_TOOL_BYTE_CAP = 16_000_000
_TRANSFER_MEDIA_STDOUT_CAP = 65_536
_TRANSFER_MEDIA_STDERR_CAP = 65_536
_TRANSFER_FFPROBE_TIMEOUT_SECONDS = 10.0
_TRANSFER_FFMPEG_TIMEOUT_SECONDS = 60.0
_MEDIA_SUBPROCESS_PATH = "/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin"


@dataclass
class _BoundInput:
    path: Path
    descriptor: int
    data: bytes
    sha256: str
    label: str
    byte_cap: int
    required_mode: int | None


def _media_subprocess_environment() -> dict[str, str]:
    """Return a fixed minimal child environment with no caller-controlled PATH."""

    return {
        "PATH": _MEDIA_SUBPROCESS_PATH,
        "LANG": "C",
        "LC_ALL": "C",
    }

def _terminate_media_process(process: subprocess.Popen[bytes]) -> None:
    if process.poll() is None:
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except (OSError, ProcessLookupError):
            try:
                process.kill()
            except OSError:
                pass
    try:
        process.wait(timeout=5.0)
    except (OSError, subprocess.TimeoutExpired):
        pass


def _run_bounded_media_process(
    command: list[str],
    *,
    executable: str,
    pass_fds: tuple[int, ...],
    timeout_seconds: float,
) -> subprocess.CompletedProcess[str]:
    if (
        not command
        or not Path(command[0]).is_absolute()
        or not Path(executable).is_absolute()
        or type(timeout_seconds) not in {int, float}
        or not 0 < float(timeout_seconds) <= _TRANSFER_FFMPEG_TIMEOUT_SECONDS
    ):
        raise ValidationError("voice-transfer media subprocess contract is invalid")
    process: subprocess.Popen[bytes] | None = None
    selector = selectors.DefaultSelector()
    streams: dict[int, tuple[str, bytearray, int]] = {}
    deadline = time.monotonic() + float(timeout_seconds)
    try:
        process = subprocess.Popen(
            command,
            executable=executable,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=False,
            bufsize=0,
            close_fds=True,
            pass_fds=pass_fds,
            env=_media_subprocess_environment(),
            start_new_session=True,
        )
        assert process.stdout is not None
        assert process.stderr is not None
        for name, stream, cap in (
            ("stdout", process.stdout, _TRANSFER_MEDIA_STDOUT_CAP),
            ("stderr", process.stderr, _TRANSFER_MEDIA_STDERR_CAP),
        ):
            descriptor = stream.fileno()
            os.set_blocking(descriptor, False)
            buffer = bytearray()
            streams[descriptor] = (name, buffer, cap)
            selector.register(descriptor, selectors.EVENT_READ)
        while selector.get_map():
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise ValidationError("voice-transfer media subprocess timed out")
            events = selector.select(remaining)
            if not events:
                raise ValidationError("voice-transfer media subprocess timed out")
            for key, _mask in events:
                descriptor = int(key.fd)
                name, buffer, cap = streams[descriptor]
                try:
                    chunk = os.read(descriptor, min(65_536, cap + 1 - len(buffer)))
                except BlockingIOError:
                    continue
                if not chunk:
                    selector.unregister(descriptor)
                    continue
                buffer.extend(chunk)
                if len(buffer) > cap:
                    raise ValidationError(
                        f"voice-transfer media subprocess {name} exceeded its byte cap"
                    )
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise ValidationError("voice-transfer media subprocess timed out")
        returncode = process.wait(timeout=remaining)
        try:
            stdout = bytes(
                next(buffer for name, buffer, _cap in streams.values() if name == "stdout")
            ).decode("utf-8", errors="strict")
            stderr = bytes(
                next(buffer for name, buffer, _cap in streams.values() if name == "stderr")
            ).decode("utf-8", errors="strict")
        except UnicodeError:
            raise ValidationError(
                "voice-transfer media subprocess returned non-UTF-8 diagnostics"
            ) from None
        return subprocess.CompletedProcess(command, returncode, stdout, stderr)
    except subprocess.TimeoutExpired:
        raise ValidationError("voice-transfer media subprocess timed out") from None
    except ValidationError:
        raise
    except OSError as exc:
        raise ValidationError(
            f"cannot run bound voice-transfer media executable: {exc}"
        ) from exc
    finally:
        if process is not None and process.poll() is None:
            _terminate_media_process(process)
        for descriptor in list(selector.get_map()):
            try:
                selector.unregister(descriptor)
            except Exception:
                pass
        selector.close()
        if process is not None:
            for stream in (process.stdout, process.stderr):
                if stream is not None:
                    try:
                        stream.close()
                    except OSError:
                        pass


def _run_transfer_media_tool(
    tool: str,
    arguments: list[str],
    runtime_bindings: dict[str, Any],
    *,
    pass_fds: tuple[int, ...] = (),
    timeout_seconds: float,
) -> subprocess.CompletedProcess[str]:
    from . import performance_transfer as pt
    from . import voice_transfer as vt

    if tool not in {"ffmpeg", "ffprobe"}:
        raise ValidationError("unsupported voice-transfer media executable")
    if (
        runtime_bindings.get("media_tool_binding_scope")
        != "primary_executable_bytes_and_version_only"
        or runtime_bindings.get("dynamic_library_dependency_closure_verified")
        is not False
        or runtime_bindings.get("media_executable_private_exact_byte_copy_required")
        is not True
    ):
        raise ValidationError(
            "voice-transfer media-tool binding policy is missing or overclaims dependency closure"
        )
    path_value = runtime_bindings.get(f"{tool}_binary_path")
    expected_sha = runtime_bindings.get(f"{tool}_binary_sha256")
    expected_version = runtime_bindings.get(f"{tool}_version")
    if (
        not isinstance(path_value, str)
        or not isinstance(expected_sha, str)
        or not _HEX_64_RE.fullmatch(expected_sha)
        or not isinstance(expected_version, str)
        or not expected_version
    ):
        raise ValidationError(f"voice-transfer bound {tool} identity is invalid")
    identity_reader = (
        vt._read_ffmpeg_identity
        if tool == "ffmpeg"
        else vt._read_ffprobe_identity
    )
    version_reader = (
        vt._read_ffmpeg_version
        if tool == "ffmpeg"
        else vt._read_ffprobe_version
    )
    resolved_path, actual_sha = identity_reader(path_value)
    if (
        resolved_path != path_value
        or actual_sha != expected_sha
        or version_reader(resolved_path, expected_sha) != expected_version
    ):
        raise ValidationError(f"voice-transfer bound {tool} identity drifted")
    with pt._private_executable_copy(
        resolved_path,
        expected_sha,
        f"{tool} executable",
    ) as private_executable:
        result = _run_bounded_media_process(
            [resolved_path, *arguments],
            executable=private_executable,
            pass_fds=pass_fds,
            timeout_seconds=timeout_seconds,
        )
    post_path, post_sha = identity_reader(path_value)
    if (
        post_path != resolved_path
        or post_sha != expected_sha
        or version_reader(post_path, expected_sha) != expected_version
    ):
        raise ValidationError(
            f"voice-transfer bound {tool} identity changed during subprocess"
        )
    return result


def _open_bound_read_descriptor(
    path: Path,
    label: str,
    *,
    required_mode: int | None,
) -> tuple[Path, int]:
    """Open one regular file through no-follow directory descriptors."""

    if not hasattr(os, "O_NOFOLLOW") or not hasattr(os, "O_DIRECTORY"):
        raise ValidationError(f"{label} requires O_NOFOLLOW/O_DIRECTORY support")
    absolute = Path(os.path.abspath(path))
    components = absolute.parts[1:]
    if not components:
        raise ValidationError(f"{label} must name a file")
    directory_flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
    file_flags = os.O_RDONLY | os.O_NOFOLLOW
    if hasattr(os, "O_CLOEXEC"):
        directory_flags |= os.O_CLOEXEC
        file_flags |= os.O_CLOEXEC
    directory_descriptor: int | None = None
    file_descriptor: int | None = None
    try:
        directory_descriptor = os.open(absolute.anchor, directory_flags)
        for component in components[:-1]:
            next_descriptor = os.open(
                component,
                directory_flags,
                dir_fd=directory_descriptor,
            )
            metadata = os.fstat(next_descriptor)
            if not stat.S_ISDIR(metadata.st_mode):
                os.close(next_descriptor)
                raise ValidationError(f"{label} parent must remain a real directory")
            os.close(directory_descriptor)
            directory_descriptor = next_descriptor
        file_descriptor = os.open(
            components[-1],
            file_flags,
            dir_fd=directory_descriptor,
        )
        descriptor_stat = os.fstat(file_descriptor)
        path_stat = os.stat(
            components[-1],
            dir_fd=directory_descriptor,
            follow_symlinks=False,
        )
        if (
            not stat.S_ISREG(descriptor_stat.st_mode)
            or not stat.S_ISREG(path_stat.st_mode)
            or (descriptor_stat.st_dev, descriptor_stat.st_ino)
            != (path_stat.st_dev, path_stat.st_ino)
        ):
            raise ValidationError(f"{label} must remain the exact regular file opened")
        if required_mode is not None and (
            stat.S_IMODE(descriptor_stat.st_mode) != required_mode
            or stat.S_IMODE(path_stat.st_mode) != required_mode
        ):
            raise ValidationError(
                f"{label} must be a regular owner-only {required_mode:04o} file"
            )
    except ValidationError:
        if file_descriptor is not None:
            os.close(file_descriptor)
        raise
    except OSError as exc:
        if file_descriptor is not None:
            os.close(file_descriptor)
        raise ValidationError(f"cannot descriptor-bind {label}: {exc}") from exc
    finally:
        if directory_descriptor is not None:
            os.close(directory_descriptor)
    assert file_descriptor is not None
    return absolute, file_descriptor


def _read_bound_descriptor_bytes(
    descriptor: int,
    label: str,
    byte_cap: int,
    *,
    required_mode: int | None,
) -> bytes:
    before = os.fstat(descriptor)
    if not stat.S_ISREG(before.st_mode):
        raise ValidationError(f"{label} descriptor is not a regular file")
    if required_mode is not None and stat.S_IMODE(before.st_mode) != required_mode:
        raise ValidationError(
            f"{label} must be a regular owner-only {required_mode:04o} file"
        )
    if before.st_size < 0 or before.st_size > byte_cap:
        raise ValidationError(f"{label} exceeds its byte cap")
    os.lseek(descriptor, 0, os.SEEK_SET)
    chunks: list[bytes] = []
    received = 0
    while True:
        chunk = os.read(descriptor, min(1_048_576, byte_cap + 1 - received))
        if not chunk:
            break
        chunks.append(chunk)
        received += len(chunk)
        if received > byte_cap:
            raise ValidationError(f"{label} exceeds its byte cap")
    after = os.fstat(descriptor)
    data = b"".join(chunks)
    stable_fields = (
        "st_dev",
        "st_ino",
        "st_size",
        "st_mtime_ns",
        "st_ctime_ns",
    )
    if (
        any(getattr(before, field) != getattr(after, field) for field in stable_fields)
        or len(data) != after.st_size
        or not stat.S_ISREG(after.st_mode)
        or (
            required_mode is not None
            and stat.S_IMODE(after.st_mode) != required_mode
        )
    ):
        raise ValidationError(f"{label} changed during descriptor-bound read")
    os.lseek(descriptor, 0, os.SEEK_SET)
    return data


def _open_bound_input(
    path: Path,
    label: str,
    *,
    byte_cap: int,
    required_mode: int | None = None,
) -> _BoundInput:
    absolute, descriptor = _open_bound_read_descriptor(
        path,
        label,
        required_mode=required_mode,
    )
    try:
        data = _read_bound_descriptor_bytes(
            descriptor,
            label,
            byte_cap,
            required_mode=required_mode,
        )
    except BaseException:
        os.close(descriptor)
        raise
    return _BoundInput(
        path=absolute,
        descriptor=descriptor,
        data=data,
        sha256=sha256_bytes(data),
        label=label,
        byte_cap=byte_cap,
        required_mode=required_mode,
    )


def _revalidate_bound_input(bound: _BoundInput) -> None:
    data = _read_bound_descriptor_bytes(
        bound.descriptor,
        bound.label,
        bound.byte_cap,
        required_mode=bound.required_mode,
    )
    if data != bound.data or sha256_bytes(data) != bound.sha256:
        raise ValidationError(f"{bound.label} bytes changed during validation")
    _absolute, probe_descriptor = _open_bound_read_descriptor(
        bound.path,
        bound.label,
        required_mode=bound.required_mode,
    )
    try:
        expected = os.fstat(bound.descriptor)
        current = os.fstat(probe_descriptor)
        if (expected.st_dev, expected.st_ino) != (current.st_dev, current.st_ino):
            raise ValidationError(
                f"{bound.label} path no longer names the validated file"
            )
    finally:
        os.close(probe_descriptor)


def _close_bound_input(bound: _BoundInput | None) -> None:
    if bound is None or bound.descriptor < 0:
        return
    os.close(bound.descriptor)
    bound.descriptor = -1


def _strict_json(path: Path, label: str) -> dict[str, Any]:
    """Read bounded UTF-8 JSON while rejecting duplicate members at any depth."""

    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise ValidationError(f"cannot read {label}: {exc}") from exc
    return _strict_json_bytes(raw, label)


def _strict_json_bytes(raw: bytes, label: str) -> dict[str, Any]:
    if not raw or len(raw) > _TRANSFER_JSON_BYTE_CAP:
        raise ValidationError(f"{label} is empty or exceeds its JSON byte cap")
    try:
        text = raw.decode("utf-8")
    except UnicodeError as exc:
        raise ValidationError(f"{label} is not UTF-8 JSON") from exc

    def reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        value: dict[str, Any] = {}
        for key, item in pairs:
            if key in value:
                raise ValidationError(f"{label} contains duplicate JSON member {key}")
            value[key] = item
        return value

    def reject_constant(value: str) -> None:
        raise ValidationError(f"{label} contains non-standard JSON constant {value}")

    try:
        value = json.loads(
            text,
            object_pairs_hook=reject_duplicates,
            parse_constant=reject_constant,
        )
    except ValidationError:
        raise
    except json.JSONDecodeError as exc:
        raise ValidationError(f"cannot parse {label}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValidationError(f"{label} root must be an object")
    return value


def _strict_object(
    value: Any,
    expected_keys: set[str],
    label: str,
) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValidationError(f"{label} must be an object")
    actual = set(value)
    if actual != expected_keys:
        missing = sorted(expected_keys - actual)
        extra = sorted(actual - expected_keys)
        raise ValidationError(f"{label} keys mismatch: missing={missing}, extra={extra}")
    return value


def _private_regular_file(path: Path, label: str) -> os.stat_result:
    safe = _no_symlink_path(path, label, must_exist=True)
    metadata = os.stat(safe, follow_symlinks=False)
    if not stat.S_ISREG(metadata.st_mode) or stat.S_IMODE(metadata.st_mode) != 0o600:
        raise ValidationError(f"{label} must be a regular owner-only 0600 file")
    return metadata


def _aware_time(value: Any, label: str) -> datetime:
    if not isinstance(value, str) or not value:
        raise ValidationError(f"{label} must be an ISO-8601 timestamp")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValidationError(f"{label} must be an ISO-8601 timestamp") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValidationError(f"{label} must include a timezone")
    return parsed


def _fixture_json_path(
    root: Path,
    relative_value: Any,
    label: str,
    *,
    parent: str,
) -> Path:
    path = _bound_existing_file(
        root,
        relative_value,
        label,
        prefix=parent,
        suffix=".json",
    )
    if path.parent != root / parent:
        raise ValidationError(f"{label} must be directly under {parent}/")
    return path


def _fixture_bound_file(root: Path, relative_value: Any, label: str) -> Path:
    if not isinstance(relative_value, str) or not relative_value:
        raise ValidationError(f"{label} must be a non-empty relative path")
    relative = Path(relative_value)
    if (
        relative.is_absolute()
        or not relative.parts
        or any(part in {"", ".", "..", "~"} for part in relative.parts)
    ):
        raise ValidationError(f"{label} escapes the fixture boundary")
    path = _no_symlink_path(root / relative, label, must_exist=True)
    if not path.is_relative_to(root):
        raise ValidationError(f"{label} escapes the fixture boundary")
    return path


def _no_symlink_path(path: Path, label: str, *, must_exist: bool) -> Path:
    """Return a lexical absolute path only when no component is a symlink."""

    absolute = Path(os.path.abspath(path))
    current = Path(absolute.anchor)
    for component in absolute.parts[1:]:
        current = current / component
        if current.is_symlink():
            raise ValidationError(f"{label} may not contain a symlink component")
        if must_exist and not current.exists():
            raise ValidationError(f"{label} does not exist")
    if must_exist and not absolute.is_file():
        raise ValidationError(f"{label} must be a regular file")
    return absolute


def _bound_existing_file(
    root: Path,
    relative_value: Any,
    label: str,
    *,
    prefix: str,
    suffix: str,
) -> Path:
    if not isinstance(relative_value, str) or not relative_value:
        raise ValidationError(f"{label} must be a non-empty relative path")
    relative = Path(relative_value)
    if (
        relative.is_absolute()
        or not relative.parts
        or relative.parts[0] != prefix
        or any(part in {"", ".", "..", "~"} for part in relative.parts)
        or relative.suffix.lower() != suffix
    ):
        raise ValidationError(f"{label} escapes its authorized boundary")
    candidate = _no_symlink_path(root / relative, label, must_exist=True)
    if not candidate.is_relative_to(root):
        raise ValidationError(f"{label} escapes its authorized boundary")
    return candidate


def _same_open_regular_file(path: Path, descriptor: int, label: str) -> None:
    """Prove the path still names the exact regular file held by descriptor."""

    safe_path = _no_symlink_path(path, label, must_exist=True)
    path_stat = os.stat(safe_path, follow_symlinks=False)
    descriptor_stat = os.fstat(descriptor)
    if (
        not stat.S_ISREG(path_stat.st_mode)
        or not stat.S_ISREG(descriptor_stat.st_mode)
        or (path_stat.st_dev, path_stat.st_ino)
        != (descriptor_stat.st_dev, descriptor_stat.st_ino)
    ):
        raise ValidationError(f"{label} changed after exclusive reservation")


def _unlink_reserved_if_same(path: Path | None, descriptor: int | None) -> None:
    if path is None or descriptor is None:
        return
    try:
        path_stat = os.stat(path, follow_symlinks=False)
        descriptor_stat = os.fstat(descriptor)
    except OSError:
        return
    if (path_stat.st_dev, path_stat.st_ino) == (
        descriptor_stat.st_dev,
        descriptor_stat.st_ino,
    ):
        try:
            path.unlink()
        except OSError:
            pass


def _unlink_at_if_same(
    directory_descriptor: int | None,
    name: str | None,
    file_descriptor: int | None,
) -> None:
    if directory_descriptor is None or name is None or file_descriptor is None:
        return
    try:
        path_stat = os.stat(
            name, dir_fd=directory_descriptor, follow_symlinks=False
        )
        descriptor_stat = os.fstat(file_descriptor)
    except OSError:
        return
    if (path_stat.st_dev, path_stat.st_ino) == (
        descriptor_stat.st_dev,
        descriptor_stat.st_ino,
    ):
        try:
            os.unlink(name, dir_fd=directory_descriptor)
        except OSError:
            pass


def _prepare_private_destination(path: Path, label: str) -> tuple[Path, int]:
    absolute = _no_symlink_path(path, label, must_exist=False)
    if absolute.exists() or absolute.is_symlink():
        raise ValidationError(f"refusing to overwrite {label}: {absolute}")
    absolute.parent.mkdir(parents=True, exist_ok=True)
    absolute = _no_symlink_path(absolute, label, must_exist=False)
    if absolute.exists() or absolute.is_symlink() or not absolute.parent.is_dir():
        raise ValidationError(f"refusing unsafe {label}: {absolute}")
    flags = os.O_RDONLY
    if hasattr(os, "O_DIRECTORY"):
        flags |= os.O_DIRECTORY
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    try:
        directory_descriptor = os.open(absolute.parent, flags)
    except OSError as exc:
        raise ValidationError(f"cannot open {label} parent securely") from exc
    descriptor_stat = os.fstat(directory_descriptor)
    try:
        parent_stat = os.stat(absolute.parent, follow_symlinks=False)
    except OSError as exc:
        os.close(directory_descriptor)
        raise ValidationError(f"cannot verify {label} parent securely") from exc
    if (
        not stat.S_ISDIR(descriptor_stat.st_mode)
        or not stat.S_ISDIR(parent_stat.st_mode)
        or (descriptor_stat.st_dev, descriptor_stat.st_ino)
        != (parent_stat.st_dev, parent_stat.st_ino)
    ):
        os.close(directory_descriptor)
        raise ValidationError(f"{label} parent changed during secure open")
    return absolute, directory_descriptor


def _reserve_private_temp(
    directory: Path,
    directory_descriptor: int,
    destination_name: str,
) -> tuple[Path, str, int]:
    flags = os.O_RDWR | os.O_CREAT | os.O_EXCL
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    for _attempt in range(16):
        name = f".{destination_name}.{secrets.token_hex(16)}.tmp"
        try:
            descriptor = os.open(
                name,
                flags,
                0o600,
                dir_fd=directory_descriptor,
            )
        except FileExistsError:
            continue
        except OSError as exc:
            raise ValidationError("cannot reserve private working-audio temp file") from exc
        os.fchmod(descriptor, 0o600)
        path = directory / name
        _same_open_regular_file(path, descriptor, "working-audio temp file")
        return path, name, descriptor
    raise ValidationError("cannot reserve a unique working-audio temp file")


def _validate_full_decode(
    path: Path,
    *,
    _transfer_runtime_bindings: dict[str, Any] | None = None,
) -> None:
    with path.open("rb") as handle:
        header = handle.read(12)
    if (
        len(header) != 12
        or header[:4] != b"RIFF"
        or header[8:12] != b"WAVE"
        or int.from_bytes(header[4:8], "little") != path.stat().st_size - 8
    ):
        raise ValidationError("working WAV lacks a normal seekable RIFF size")
    arguments = [
            "-nostdin",
            "-v",
            "error",
            "-xerror",
            "-i",
            str(path),
            "-f",
            "null",
            "-",
        ]
    if _transfer_runtime_bindings is None:
        result = _run(["ffmpeg", *arguments])
    else:
        result = _run_transfer_media_tool(
            "ffmpeg",
            arguments,
            _transfer_runtime_bindings,
            timeout_seconds=_TRANSFER_FFMPEG_TIMEOUT_SECONDS,
        )
    if result.returncode != 0 or result.stderr.strip():
        raise ValidationError(
            f"working WAV failed full strict decode: {result.stderr.strip()}"
        )


def _validate_directed_authorization_chain(
    artifact_root: Path,
    receipt_path: Path,
    receipt: dict[str, Any],
    bindings: dict[str, Any],
    request_ids: list[Any],
) -> None:
    authorization_hash = receipt.get("authorization_sha256")
    authorization_root = artifact_root / "authorizations"
    _no_symlink_path(authorization_root, "directed authorization root", must_exist=False)
    if not authorization_root.is_dir():
        raise ValidationError("directed authorization root does not exist")
    matches: list[Path] = []
    for candidate in authorization_root.glob("*.json"):
        safe_candidate = _no_symlink_path(
            candidate, "directed authorization", must_exist=True
        )
        if sha256_file(safe_candidate) == authorization_hash:
            matches.append(safe_candidate)
    if len(matches) != 1:
        raise ValidationError(
            "directed receipt must match exactly one local authorization file"
        )
    authorization_path = matches[0]
    authorization = read_json(authorization_path)
    action = authorization.get("action")
    authorization_bindings = authorization.get("bindings")
    authorization_consumption = authorization.get("consumption")
    authorization_id = authorization.get("authorization_id")
    if (
        authorization.get("schema_version") != "oe-provider-action-authorization-v1"
        or authorization.get("scope") != "elevenlabs_calibration"
        or authorization.get("provider") != "elevenlabs"
        or authorization.get("approved") is not True
        or authorization.get("execution_ready") is not True
        or not isinstance(action, dict)
        or action.get("kind") != "bounded_tts_calibration"
        or action.get("request_ids") != request_ids
        or action.get("preferred_output_format") != "pcm_48000"
        or not isinstance(authorization_bindings, dict)
        or authorization_bindings.get("compiled_dry_run_sha256")
        != bindings["compiled_dry_run_sha256"]
        or authorization.get("authorized_limits") != receipt.get("authorization_limits")
        or not isinstance(authorization_consumption, dict)
        or not isinstance(authorization_id, str)
        or receipt_path.name != f"{authorization_id}-directed-bakeoff-run.json"
    ):
        raise ValidationError("directed authorization does not semantically bind the run")

    consumption_binding = receipt.get("authorization_consumption")
    assert isinstance(consumption_binding, dict)
    if consumption_binding.get("path") != authorization_consumption.get("record_path"):
        raise ValidationError("directed consumption path differs from its authorization")
    consumption_path = _bound_existing_file(
        authorization_root,
        consumption_binding.get("path"),
        "directed authorization consumption",
        prefix="consumed",
        suffix=".json",
    )
    if sha256_file(consumption_path) != consumption_binding.get("sha256"):
        raise ValidationError("directed authorization-consumption hash mismatch")
    consumption = read_json(consumption_path)
    if (
        consumption.get("schema_version")
        != "oe-provider-authorization-consumption-v1"
        or consumption.get("authorization_id") != authorization_id
        or consumption.get("authorization_sha256") != authorization_hash
        or consumption.get("scope") != "elevenlabs_calibration"
        or consumption.get("status") != "consumed"
        or consumption.get("request_set_sha256") != bindings["request_set_sha256"]
        or consumption.get("seed_map_sha256") != bindings["seed_map_sha256"]
    ):
        raise ValidationError(
            "directed authorization consumption does not semantically bind the run"
        )


def _inspect_directed_raw_pcm(
    path: Path,
    receipt_path: Path,
    receipt: dict[str, Any],
    raw_hash: str,
    part_id: str | None,
) -> dict[str, Any]:
    if part_id is None:
        raise ValidationError("directed raw PCM requires its exact request_id")
    resolved_receipt = _no_symlink_path(
        receipt_path, "directed PCM receipt", must_exist=True
    )
    if (
        resolved_receipt.parent.name != "elevenlabs"
        or resolved_receipt.parent.parent.name != "receipts"
    ):
        raise ValidationError("directed PCM receipt must remain under receipts/elevenlabs/")
    artifact_root = resolved_receipt.parents[2]
    if (
        receipt.get("network_called") is not True
        or receipt.get("retries_made") != 0
        or not isinstance(receipt.get("results"), list)
        or receipt.get("outputs_received") != len(receipt["results"])
    ):
        raise ValidationError("directed PCM receipt is not an exact successful run")

    bindings = receipt.get("bindings")
    consumption = receipt.get("authorization_consumption")
    if (
        not isinstance(bindings, dict)
        or any(
            not isinstance(bindings.get(field), str)
            or len(bindings[field]) != 64
            for field in (
                "compiled_dry_run_sha256",
                "request_set_sha256",
                "seed_map_sha256",
            )
        )
        or not isinstance(receipt.get("authorization_sha256"), str)
        or len(receipt["authorization_sha256"]) != 64
        or not isinstance(consumption, dict)
        or not isinstance(consumption.get("sha256"), str)
        or len(consumption["sha256"]) != 64
    ):
        raise ValidationError("directed PCM receipt lacks request bindings")
    compiled_path = _no_symlink_path(
        artifact_root / "compiled" / "provider-bakeoff-dry-run.json",
        "directed compiled request",
        must_exist=True,
    )
    if (
        sha256_file(compiled_path) != bindings["compiled_dry_run_sha256"]
    ):
        raise ValidationError("directed compiled-request hash does not match the receipt")
    compiled = read_json(compiled_path)
    compiled_requests = compiled.get("requests")
    if (
        compiled.get("schema_version") != "oe-provider-bakeoff-dry-run-v1"
        or compiled.get("request_set_sha256") != bindings["request_set_sha256"]
        or not isinstance(compiled_requests, list)
    ):
        raise ValidationError("directed compiled request set does not match the receipt")
    compiled_request_ids = [
        request.get("request_id")
        for request in compiled_requests
        if isinstance(request, dict) and request.get("provider") == "elevenlabs"
    ]
    receipt_request_ids = [
        item.get("request_id") for item in receipt["results"] if isinstance(item, dict)
    ]
    if compiled_request_ids != receipt_request_ids:
        raise ValidationError("directed receipt does not contain the exact compiled request set")
    _validate_directed_authorization_chain(
        artifact_root,
        resolved_receipt,
        receipt,
        bindings,
        compiled_request_ids,
    )

    resolved_raw = _no_symlink_path(path, "directed PCM source", must_exist=True)
    if not resolved_raw.is_relative_to(artifact_root):
        raise ValidationError("directed PCM source is outside its artifact root")
    relative_raw = resolved_raw.relative_to(artifact_root).as_posix()
    relative = Path(relative_raw)
    if (
        not relative.parts
        or relative.parts[0] != "outputs"
        or any(component in {"", ".", "..", "~"} for component in relative.parts)
        or relative.suffix.lower() != ".pcm"
    ):
        raise ValidationError("directed PCM source is outside outputs/ or is not .pcm")
    matches = []
    for item in receipt["results"]:
        if not isinstance(item, dict):
            continue
        raw_output = item.get("raw_output")
        if (
            isinstance(raw_output, dict)
            and raw_output.get("path") == relative_raw
            and raw_output.get("sha256") == raw_hash
            and item.get("request_id") == part_id
        ):
            matches.append(item)
    if len(matches) != 1:
        raise ValidationError(
            "directed raw PCM source/hash/request does not match exactly one receipt result"
        )
    item = matches[0]
    requests = [
        request
        for request in compiled_requests
        if isinstance(request, dict) and request.get("request_id") == part_id
    ]
    if len(requests) != 1:
        raise ValidationError("directed PCM request is not unique in the compiled run")
    request = requests[0]
    expected_result = {
        "requested_output_format": "pcm_48000",
        "actual_output_format": "pcm_48000",
        "actual_codec": "pcm_s16le",
        "container": "raw",
        "sample_rate_hz": 48_000,
        "channels": 1,
        "bit_depth": 16,
        "lossy_origin": False,
        "comparison_eligible": True,
        "pcm_capability_failure_receipt": None,
    }
    errors = [
        f"directed PCM receipt {key} mismatch"
        for key, value in expected_result.items()
        if item.get(key) != value
    ]
    if (
        not isinstance(item.get("candidate_ids"), list)
        or not item["candidate_ids"]
        or not isinstance(item.get("spoken_text_sha256"), str)
        or len(item["spoken_text_sha256"]) != 64
        or not isinstance(item.get("compiled_request_body_sha256"), str)
        or len(item["compiled_request_body_sha256"]) != 64
        or item.get("execution_request_body_sha256")
        != item.get("compiled_request_body_sha256")
    ):
        errors.append("directed PCM receipt request binding mismatch")
    request_body = request.get("request_body")
    if (
        request.get("provider") != "elevenlabs"
        or request.get("query") != {"output_format": "pcm_48000"}
        or request.get("destinations") != [relative_raw]
        or not isinstance(request_body, dict)
        or sha256_bytes(
            json.dumps(
                request_body,
                ensure_ascii=False,
                separators=(",", ":"),
                sort_keys=True,
            ).encode("utf-8")
        )
        != request.get("request_body_sha256")
        or any(
            item.get(field) != request.get(field)
            for field in (
                "passage_id",
                "candidate_ids",
                "start_token",
                "end_token",
                "spoken_text_sha256",
            )
        )
        or item.get("compiled_request_body_sha256")
        != request.get("request_body_sha256")
        or item.get("fixed_seed") != request_body.get("seed")
    ):
        errors.append("directed PCM receipt does not match the compiled request")
    if item.get("raw_output", {}).get("byte_count") != resolved_raw.stat().st_size:
        errors.append("directed PCM receipt byte count mismatch")
    if errors:
        raise ValidationError(errors)
    return item


def _validate_transfer_provider_evidence(value: Any) -> None:
    evidence = _strict_object(
        value,
        {
            "account_get_calls_made",
            "generation_post_calls_made",
            "outputs_received",
            "request_ids",
            "usage",
        },
        "voice-transfer provider evidence",
    )
    if (
        type(evidence["account_get_calls_made"]) is not int
        or evidence["account_get_calls_made"] != 0
        or type(evidence["generation_post_calls_made"]) is not int
        or evidence["generation_post_calls_made"] != 1
        or type(evidence["outputs_received"]) is not int
        or evidence["outputs_received"] != 1
    ):
        raise ValidationError(
            "voice-transfer run must record exactly one generation POST, one output, and no account GET"
        )
    request_ids = evidence["request_ids"]
    if not isinstance(request_ids, dict) or not set(request_ids).issubset(
        _TRANSFER_PROVIDER_ID_KEYS
    ):
        raise ValidationError("voice-transfer provider request IDs are not allowlisted")
    for key, item in request_ids.items():
        if (
            not isinstance(key, str)
            or not isinstance(item, str)
            or not _SAFE_PROVIDER_VALUE_RE.fullmatch(item)
            or _SECRET_PROVIDER_VALUE_RE.search(item)
        ):
            raise ValidationError("voice-transfer provider request ID is unsafe")
    usage = evidence["usage"]
    if not isinstance(usage, dict) or not set(usage).issubset(_TRANSFER_USAGE_KEYS):
        raise ValidationError("voice-transfer provider usage keys are not allowlisted")
    if any(
        type(item) is not int or item < 0 or item > 1_000_000_000_000_000
        for item in usage.values()
    ):
        raise ValidationError("voice-transfer provider usage values are invalid")


def _replay_transfer_source_proof(
    source_proof: dict[str, Any],
    runtime_bindings: dict[str, Any],
    authorization_bound: _BoundInput,
    plan_bound: _BoundInput,
    canonical_w_bound: _BoundInput,
    prerequisite_bounds: dict[str, _BoundInput],
) -> None:
    """Replay exact source bytes and allow only this transfer's generated Git dirt."""

    from . import performance_transfer as pt
    from . import voice_transfer as vt

    repository = pt._guide_repository_root()
    git_path_value = runtime_bindings.get("git_binary_path")
    git_sha_value = runtime_bindings.get("git_binary_sha256")
    git_version_value = runtime_bindings.get("git_version")
    if (
        not isinstance(git_path_value, str)
        or not isinstance(git_sha_value, str)
        or not _HEX_64_RE.fullmatch(git_sha_value)
        or not isinstance(git_version_value, str)
        or not git_version_value
    ):
        raise ValidationError("voice-transfer bound Git identity is invalid")
    git_path, git_sha = vt._read_git_identity(git_path_value)
    if (
        git_path != git_path_value
        or git_sha != git_sha_value
        or vt._read_git_version(git_path, git_sha_value) != git_version_value
    ):
        raise ValidationError("voice-transfer bound Git identity drifted")
    vt._verify_local_git_object_store(runtime_bindings)

    def git_read(arguments: list[str], *, max_bytes: int = 2_000_000) -> bytes:
        return pt._guide_git(
            arguments,
            max_bytes=max_bytes,
            git_path=git_path_value,
            git_sha256=git_sha_value,
        )

    try:
        authorization_relative = authorization_bound.path.relative_to(
            repository
        ).as_posix()
    except ValueError:
        raise ValidationError(
            "voice-transfer ACTIVE authorization is outside the runtime repository"
        ) from None
    if source_proof["head_delta_path"] != authorization_relative:
        raise ValidationError(
            "voice-transfer source proof ACTIVE path differs from the repository path"
        )
    try:
        head = git_read(["rev-parse", "HEAD"]).strip().decode(
            "ascii",
            errors="strict",
        )
    except (UnicodeError, ValidationError):
        raise ValidationError(
            "voice-transfer source proof could not replay exact Git identities"
        ) from None
    runtime_commit = source_proof["runtime_commit"]
    if (
        not _HEX_40_RE.fullmatch(head)
        or not isinstance(runtime_commit, str)
        or not _HEX_40_RE.fullmatch(runtime_commit)
        or head != source_proof["git_head"]
    ):
        raise ValidationError(
            "voice-transfer source proof HEAD/runtime identity mismatch"
        )
    git_read(["merge-base", "--is-ancestor", runtime_commit, head])
    delta = git_read(
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
            "voice-transfer source proof runtime-to-HEAD delta is not exact ACTIVE-only"
        )
    committed_authorization = git_read(
        ["show", f"HEAD:{authorization_relative}"],
        max_bytes=_TRANSFER_JSON_BYTE_CAP,
    )
    if (
        committed_authorization != authorization_bound.data
        or sha256_bytes(committed_authorization) != authorization_bound.sha256
    ):
        raise ValidationError(
            "voice-transfer source proof committed ACTIVE bytes or SHA-256 mismatch"
        )

    contract = vt._build_transfer_contract(
        authorization_bound.path,
        plan_bound.path,
        canonical_w_bound.path,
        enforce_current_execution_window=False,
    )
    if (
        contract.authorization_path != authorization_bound.path
        or contract.authorization_raw != authorization_bound.data
        or contract.authorization_sha256 != authorization_bound.sha256
    ):
        raise ValidationError(
            "voice-transfer reconstructed contract changed the ACTIVE authority"
        )
    reconstructed_runtime_bindings = contract.authorization.get("runtime_bindings")
    if (
        not isinstance(reconstructed_runtime_bindings, dict)
        or reconstructed_runtime_bindings != runtime_bindings
        or reconstructed_runtime_bindings.get("git_commit") != runtime_commit
    ):
        raise ValidationError(
            "voice-transfer reconstructed contract runtime binding drifted"
    )

    for name, (relative, path) in vt._runtime_files().items():
        try:
            current_relative = path.relative_to(repository).as_posix()
        except ValueError:
            raise ValidationError(
                f"voice-transfer runtime source {name} is outside the repository"
            ) from None
        if current_relative != relative:
            raise ValidationError(
                f"voice-transfer runtime source {name} repository path drifted"
            )
        expected_sha = reconstructed_runtime_bindings.get(f"{name}_sha256")
        if not isinstance(expected_sha, str) or not _HEX_64_RE.fullmatch(expected_sha):
            raise ValidationError(
                f"voice-transfer runtime binding {name} SHA-256 is invalid"
            )
        current_bound = _open_bound_input(
            path,
            f"voice-transfer runtime source {name}",
            byte_cap=_TRANSFER_SOURCE_RECORD_BYTE_CAP,
        )
        try:
            committed = git_read(
                ["show", f"{runtime_commit}:{relative}"],
                max_bytes=_TRANSFER_SOURCE_RECORD_BYTE_CAP,
            )
            if (
                current_bound.sha256 != expected_sha
                or sha256_bytes(committed) != expected_sha
                or current_bound.data != committed
            ):
                raise ValidationError(
                    f"voice-transfer runtime source {name} differs from its binding or runtime commit"
                )
            _revalidate_bound_input(current_bound)
        finally:
            _close_bound_input(current_bound)

    probe_path, probe_sha = vt._read_ffprobe_identity(
        reconstructed_runtime_bindings.get("ffprobe_binary_path")
    )
    if (
        probe_path != reconstructed_runtime_bindings.get("ffprobe_binary_path")
        or probe_sha
        != reconstructed_runtime_bindings.get("ffprobe_binary_sha256")
        or vt._read_ffprobe_version(probe_path, probe_sha)
        != reconstructed_runtime_bindings.get("ffprobe_version")
    ):
        raise ValidationError(
            "voice-transfer bound ffprobe path, SHA-256, or version drifted"
        )
    ffmpeg_path, ffmpeg_sha = vt._read_ffmpeg_identity(
        reconstructed_runtime_bindings.get("ffmpeg_binary_path")
    )
    if (
        ffmpeg_path
        != reconstructed_runtime_bindings.get("ffmpeg_binary_path")
        or ffmpeg_sha
        != reconstructed_runtime_bindings.get("ffmpeg_binary_sha256")
        or vt._read_ffmpeg_version(ffmpeg_path, ffmpeg_sha)
        != reconstructed_runtime_bindings.get("ffmpeg_version")
        or reconstructed_runtime_bindings.get("media_tool_binding_scope")
        != "primary_executable_bytes_and_version_only"
        or reconstructed_runtime_bindings.get(
            "dynamic_library_dependency_closure_verified"
        )
        is not False
        or reconstructed_runtime_bindings.get(
            "media_executable_private_exact_byte_copy_required"
        )
        is not True
    ):
        raise ValidationError(
            "voice-transfer bound ffmpeg identity or media-tool policy drifted"
        )

    already_bound = {
        "plan": plan_bound,
        "canonical_w": canonical_w_bound,
        **{f"prerequisite:{name}": bound for name, bound in prerequisite_bounds.items()},
    }
    for bound in already_bound.values():
        _revalidate_bound_input(bound)

    if (
        not isinstance(contract.records, dict)
        or set(contract.records) != _TRANSFER_SOURCE_RECORD_KEYS
        or _TRANSFER_COMMITTED_SOURCE_RECORD_KEYS
        != vt.TRANSFER_COMMITTED_RECORD_NAMES
        or _TRANSFER_LOCAL_PRIVATE_SOURCE_RECORD_KEYS
        != vt.TRANSFER_LOCAL_PRIVATE_RECORD_NAMES
        or _TRANSFER_COMMITTED_SOURCE_RECORD_KEYS
        | _TRANSFER_LOCAL_PRIVATE_SOURCE_RECORD_KEYS
        != _TRANSFER_SOURCE_RECORD_KEYS
        or _TRANSFER_COMMITTED_SOURCE_RECORD_KEYS
        & _TRANSFER_LOCAL_PRIVATE_SOURCE_RECORD_KEYS
    ):
        raise ValidationError(
            "voice-transfer reconstructed source-record set is incomplete or drifted"
        )
    for name, record in sorted(contract.records.items()):
        if (
            not isinstance(record, tuple)
            or len(record) != 3
            or not isinstance(record[0], Path)
            or not isinstance(record[1], bytes)
            or not isinstance(record[2], str)
            or not _HEX_64_RE.fullmatch(record[2])
        ):
            raise ValidationError(
                f"voice-transfer reconstructed source record {name} is invalid"
            )
        path, recorded_bytes, expected_sha = record
        if (
            len(recorded_bytes) > _TRANSFER_SOURCE_RECORD_BYTE_CAP
            or sha256_bytes(recorded_bytes) != expected_sha
        ):
            raise ValidationError(
                f"voice-transfer reconstructed source record {name} hash drifted"
            )
        try:
            relative = path.relative_to(repository).as_posix()
        except ValueError:
            raise ValidationError(
                f"voice-transfer reconstructed source record {name} is outside the repository"
            ) from None
        local_private = name in _TRANSFER_LOCAL_PRIVATE_SOURCE_RECORD_KEYS
        current_bound = _open_bound_input(
            path,
            f"voice-transfer reconstructed source record {name}",
            byte_cap=_TRANSFER_SOURCE_RECORD_BYTE_CAP,
            required_mode=0o600 if local_private else None,
        )
        try:
            if (
                current_bound.data != recorded_bytes
                or current_bound.sha256 != expected_sha
            ):
                raise ValidationError(
                    f"voice-transfer reconstructed source record {name} differs from its exact local binding"
                )
            if local_private:
                if os.fstat(current_bound.descriptor).st_uid != os.getuid():
                    raise ValidationError(
                        f"voice-transfer local-private source record {name} is not owned by the executing user"
                    )
            else:
                committed = git_read(
                    ["show", f"{runtime_commit}:{relative}"],
                    max_bytes=_TRANSFER_SOURCE_RECORD_BYTE_CAP,
                )
                if (
                    committed != recorded_bytes
                    or sha256_bytes(committed) != expected_sha
                ):
                    raise ValidationError(
                        f"voice-transfer committed source record {name} differs from its runtime-commit bytes"
                    )
            _revalidate_bound_input(current_bound)
        finally:
            _close_bound_input(current_bound)

    generated_relatives: set[bytes] = set()
    for label, relative in (
        ("consumption latch", contract.consumption_relative),
        ("success receipt", contract.success_relative),
        ("raw output", contract.raw_relative),
        ("working output", contract.working_relative),
        ("conversion receipt", contract.conversion_relative),
    ):
        if not isinstance(relative, str) or not relative:
            raise ValidationError(
                f"voice-transfer generated {label} path is invalid"
            )
        try:
            repository_relative = (contract.root / relative).relative_to(
                repository
            ).as_posix()
        except ValueError:
            raise ValidationError(
                f"voice-transfer generated {label} is outside the repository"
            ) from None
        encoded = repository_relative.encode("utf-8")
        if encoded in generated_relatives:
            raise ValidationError(
                "voice-transfer generated Git-status paths are not distinct"
            )
        generated_relatives.add(encoded)

    status = git_read(
        [
            "status",
            "--porcelain=v1",
            "--untracked-files=all",
            "--no-renames",
            "-z",
        ],
        max_bytes=_TRANSFER_SOURCE_RECORD_BYTE_CAP,
    )
    if status:
        if not status.endswith(b"\x00"):
            raise ValidationError(
                "voice-transfer Git status is not exact NUL-delimited porcelain"
            )
        seen: set[bytes] = set()
        for entry in status[:-1].split(b"\x00"):
            if (
                not entry.startswith(b"?? ")
                or len(entry) <= 3
                or entry[3:] not in generated_relatives
                or entry[3:] in seen
            ):
                raise ValidationError(
                    "voice-transfer Git status contains non-authorized worktree changes"
                )
            seen.add(entry[3:])

    post_git_path, post_git_sha = vt._read_git_identity(git_path_value)
    if (
        post_git_path != git_path_value
        or post_git_sha != git_sha_value
        or vt._read_git_version(post_git_path, post_git_sha)
        != git_version_value
    ):
        raise ValidationError("voice-transfer bound Git identity changed during replay")


def _transfer_canonical_w_inputs(
    artifact_root: Path,
    held: list[_BoundInput],
) -> tuple[_BoundInput, _BoundInput]:
    plan_bound = _open_bound_input(
        artifact_root / "performance-transfer-plan.json",
        "voice-transfer plan",
        byte_cap=_TRANSFER_JSON_BYTE_CAP,
    )
    held.append(plan_bound)
    plan = _strict_json_bytes(plan_bound.data, "voice-transfer plan")
    canonical = plan.get("canonical_w")
    if not isinstance(canonical, dict):
        raise ValidationError("voice-transfer plan lacks canonical W binding")
    relative = canonical.get("path")
    if not isinstance(relative, str) or not relative:
        raise ValidationError("voice-transfer canonical W path is invalid")
    relative_path = Path(relative)
    if relative_path.is_absolute() or any(part in {"", ".", "~"} for part in relative_path.parts):
        raise ValidationError("voice-transfer canonical W path is unsafe")
    canonical_path = Path(os.path.abspath(artifact_root / relative_path))
    if not canonical_path.is_relative_to(artifact_root.parent):
        raise ValidationError("voice-transfer canonical W escapes the fixtures boundary")
    canonical_bound = _open_bound_input(
        canonical_path,
        "voice-transfer canonical W",
        byte_cap=_TRANSFER_JSON_BYTE_CAP,
    )
    held.append(canonical_bound)
    return plan_bound, canonical_bound


def _inspect_voice_transfer_raw_pcm(
    path: Path,
    receipt_path: Path,
    part_id: str | None,
    raw_bound: _BoundInput | None,
    runtime_bindings_out: dict[str, Any] | None,
) -> tuple[dict[str, Any], str, int, str]:
    held: list[_BoundInput] = []
    try:
        return _inspect_voice_transfer_raw_pcm_impl(
            path,
            receipt_path,
            part_id,
            raw_bound,
            runtime_bindings_out,
            held,
        )
    finally:
        for bound in reversed(held):
            _close_bound_input(bound)


def _inspect_voice_transfer_raw_pcm_impl(
    path: Path,
    receipt_path: Path,
    part_id: str | None,
    raw_bound: _BoundInput | None,
    runtime_bindings_out: dict[str, Any] | None,
    held: list[_BoundInput],
) -> tuple[dict[str, Any], str, int, str]:
    if part_id != _TRANSFER_PART_ID:
        raise ValidationError(
            f"voice-transfer raw PCM requires exact part_id {_TRANSFER_PART_ID}"
        )
    receipt_bound = _open_bound_input(
        receipt_path,
        "voice-transfer run receipt",
        byte_cap=_TRANSFER_JSON_BYTE_CAP,
        required_mode=0o600,
    )
    held.append(receipt_bound)
    resolved_receipt = receipt_bound.path
    receipt = _strict_json_bytes(
        receipt_bound.data,
        "voice-transfer run receipt",
    )
    receipt_hash = receipt_bound.sha256
    if (
        resolved_receipt.parent.name != "elevenlabs"
        or resolved_receipt.parent.parent.name != "receipts"
    ):
        raise ValidationError(
            "voice-transfer run receipt must remain under receipts/elevenlabs/"
        )
    artifact_root = resolved_receipt.parents[2]
    _strict_object(
        receipt,
        {
            "schema_version",
            "outcome",
            "provider",
            "scope",
            "method",
            "endpoint",
            "part_id",
            "authorization_id",
            "authorization_path",
            "authorization_sha256",
            "consumption_record_path",
            "consumption_record_sha256",
            "source_proof",
            "plan_sha256",
            "canonical_w_sha256",
            "spoken_text_sha256",
            "selected_guide_sha256",
            "selected_guide_run_receipt_sha256",
            "prerequisite_sha256s",
            "api_key_fingerprint_sha256",
            "account_scope_binding_sha256",
            "request",
            "provider_evidence",
            "response",
            "raw_output",
            "working_output_path",
            "conversion_receipt_path",
            "started_at",
            "completed_at",
            "modeled_spend_usd",
            "modeled_spend_basis",
            "modeled_spend_provider_enforced",
            "taxes_included",
            "retries_made",
            "redirects_followed",
            "fallbacks_used",
            "credentials_recorded",
            "raw_api_key_stored",
            "creative_approved",
            "full_capture_authorized",
            "step2_lock_authorized",
            "step3_authorized",
            "sharing_authorized",
            "publication_authorized",
        },
        "voice-transfer run receipt",
    )
    if (
        receipt["schema_version"] != _TRANSFER_RUN_SCHEMA
        or receipt["outcome"] != "success"
        or receipt["provider"] != "elevenlabs"
        or receipt["scope"] != _TRANSFER_SCOPE
        or receipt["method"] != "POST"
        or receipt["part_id"] != _TRANSFER_PART_ID
        or type(receipt["modeled_spend_usd"]) not in {int, float}
        or receipt["modeled_spend_usd"] != 0.12
        or receipt["modeled_spend_basis"]
        != "voice_changer_full_minute_worst_case"
        or receipt["modeled_spend_provider_enforced"] is not False
        or receipt["taxes_included"] is not False
        or type(receipt["retries_made"]) is not int
        or receipt["retries_made"] != 0
        or type(receipt["redirects_followed"]) is not int
        or receipt["redirects_followed"] != 0
        or type(receipt["fallbacks_used"]) is not int
        or receipt["fallbacks_used"] != 0
        or receipt["credentials_recorded"] is not False
        or receipt["raw_api_key_stored"] is not False
        or receipt["creative_approved"] is not False
        or receipt["full_capture_authorized"] is not False
        or receipt["step2_lock_authorized"] is not False
        or receipt["step3_authorized"] is not False
        or receipt["sharing_authorized"] is not False
        or receipt["publication_authorized"] is not False
    ):
        raise ValidationError(
            "voice-transfer run outcome, transport, privacy, or authority boundary is invalid"
        )

    authorization_relative = receipt["authorization_path"]
    authorization_path = _fixture_json_path(
        artifact_root,
        authorization_relative,
        "voice-transfer ACTIVE authorization",
        parent="authorizations",
    )
    authorization_bound = _open_bound_input(
        authorization_path,
        "voice-transfer ACTIVE authorization",
        byte_cap=_TRANSFER_JSON_BYTE_CAP,
    )
    held.append(authorization_bound)
    authorization_sha = authorization_bound.sha256
    if (
        not isinstance(receipt["authorization_sha256"], str)
        or not _HEX_64_RE.fullmatch(receipt["authorization_sha256"])
        or authorization_sha != receipt["authorization_sha256"]
    ):
        raise ValidationError("voice-transfer ACTIVE authorization SHA-256 mismatch")
    authorization = _strict_json_bytes(
        authorization_bound.data,
        "voice-transfer ACTIVE authorization",
    )
    if (
        authorization.get("schema_version") != _TRANSFER_AUTH_SCHEMA
        or authorization.get("scope") != _TRANSFER_SCOPE
        or authorization.get("status") != "active"
        or authorization.get("approved") is not True
        or authorization.get("execution_ready") is not True
        or receipt["authorization_id"] != authorization.get("authorization_id")
    ):
        raise ValidationError("voice-transfer run does not bind an exact ACTIVE V2 authorization")

    artifacts = _strict_object(
        authorization.get("artifacts"),
        {
            "raw_output_path",
            "working_output_path",
            "success_receipt_path",
            "failure_receipt_path",
            "conversion_receipt_path",
        },
        "voice-transfer ACTIVE artifacts",
    )
    receipt_relative = resolved_receipt.relative_to(artifact_root).as_posix()
    if (
        artifacts["raw_output_path"] != _TRANSFER_RAW_PATH
        or artifacts["working_output_path"] != _TRANSFER_WORKING_PATH
        or artifacts["success_receipt_path"] != receipt_relative
        or receipt["working_output_path"] != artifacts["working_output_path"]
        or receipt["conversion_receipt_path"] != artifacts["conversion_receipt_path"]
    ):
        raise ValidationError("voice-transfer receipt or ACTIVE artifact path drifted")

    plan_bound, canonical_w_bound = _transfer_canonical_w_inputs(
        artifact_root,
        held,
    )
    plan_path = plan_bound.path
    canonical_w_path = canonical_w_bound.path
    from .voice_transfer import (
        _negative_ffprobe_media_detection,
        validate_voice_transfer_execution_authorization,
    )

    validation = validate_voice_transfer_execution_authorization(
        authorization_path,
        plan_path,
        canonical_w_path,
    )
    if not isinstance(validation, dict) or validation.get("valid") is not True:
        raise ValidationError("voice-transfer ACTIVE authorization did not revalidate")

    bindings = authorization.get("bindings")
    action = authorization.get("action")
    credential = authorization.get("credential_binding")
    runtime_bindings = authorization.get("runtime_bindings")
    prerequisites = authorization.get("prerequisites")
    consumption_binding = authorization.get("consumption")
    authorized_limits = authorization.get("authorized_limits")
    for value, label in (
        (bindings, "voice-transfer ACTIVE bindings"),
        (action, "voice-transfer ACTIVE action"),
        (credential, "voice-transfer ACTIVE credential binding"),
        (runtime_bindings, "voice-transfer ACTIVE runtime bindings"),
        (prerequisites, "voice-transfer ACTIVE prerequisites"),
        (consumption_binding, "voice-transfer ACTIVE consumption"),
        (authorized_limits, "voice-transfer ACTIVE limits"),
    ):
        if not isinstance(value, dict):
            raise ValidationError(f"{label} must be an object")
    assert isinstance(bindings, dict)
    assert isinstance(action, dict)
    assert isinstance(credential, dict)
    assert isinstance(runtime_bindings, dict)
    assert isinstance(prerequisites, dict)
    assert isinstance(consumption_binding, dict)
    assert isinstance(authorized_limits, dict)
    if (
        type(authorized_limits.get("max_source_duration_seconds"))
        not in {int, float}
        or authorized_limits.get("max_source_duration_seconds")
        != _TRANSFER_SELECTED_GUIDE_DURATION_SECONDS
        or type(authorized_limits.get("min_output_duration_seconds"))
        not in {int, float}
        or authorized_limits.get("min_output_duration_seconds")
        != _TRANSFER_MIN_DURATION_SECONDS
        or type(authorized_limits.get("max_output_duration_seconds"))
        not in {int, float}
        or authorized_limits.get("max_output_duration_seconds")
        != _TRANSFER_MAX_DURATION_SECONDS
        or type(authorized_limits.get("min_output_to_source_duration_ratio"))
        not in {int, float}
        or authorized_limits.get("min_output_to_source_duration_ratio")
        != _TRANSFER_MIN_OUTPUT_TO_SOURCE_DURATION_RATIO
        or type(authorized_limits.get("max_output_to_source_duration_ratio"))
        not in {int, float}
        or authorized_limits.get("max_output_to_source_duration_ratio")
        != _TRANSFER_MAX_OUTPUT_TO_SOURCE_DURATION_RATIO
    ):
        raise ValidationError(
            "voice-transfer ACTIVE duration and source-coherence limits drifted"
        )

    expected_receipt_bindings = {
        "plan_sha256": bindings.get("performance_transfer_plan_sha256"),
        "canonical_w_sha256": bindings.get("canonical_w_sha256"),
        "spoken_text_sha256": bindings.get("spoken_text_sha256"),
        "selected_guide_sha256": bindings.get("selected_guide_sha256"),
        "selected_guide_run_receipt_sha256": bindings.get(
            "guide_run_receipt_sha256"
        ),
        "api_key_fingerprint_sha256": credential.get(
            "api_key_fingerprint_sha256"
        ),
        "account_scope_binding_sha256": credential.get(
            "account_scope_binding_sha256"
        ),
    }
    for key, expected in expected_receipt_bindings.items():
        if (
            not isinstance(expected, str)
            or not _HEX_64_RE.fullmatch(expected)
            or receipt[key] != expected
        ):
            raise ValidationError(f"voice-transfer receipt {key} binding mismatch")

    if set(prerequisites) != _TRANSFER_PREREQUISITE_KEYS:
        raise ValidationError("voice-transfer ACTIVE prerequisite set drifted")
    expected_prerequisite_hashes: dict[str, str] = {}
    prerequisite_bounds: dict[str, _BoundInput] = {}
    for key in sorted(_TRANSFER_PREREQUISITE_KEYS):
        item = prerequisites[key]
        expected_keys = (
            _TRANSFER_SELECTED_GUIDE_KEYS
            if key == "selected_guide"
            else frozenset({"state", "path", "sha256"})
        )
        if (
            not isinstance(item, dict)
            or set(item) != expected_keys
            or item.get("state") != "verified"
            or not isinstance(item.get("sha256"), str)
            or not _HEX_64_RE.fullmatch(item["sha256"])
        ):
            raise ValidationError(f"voice-transfer prerequisite {key} is not verified")
        if key == "official_media_contract" and (
            item.get("path") != _TRANSFER_MEDIA_CONTRACT_PATH
            or item["sha256"] != _TRANSFER_MEDIA_CONTRACT_SHA256
        ):
            raise ValidationError(
                "voice-transfer official media contract path or SHA-256 drifted"
            )
        expected_prerequisite_hashes[key] = item["sha256"]
        prerequisite_path = _fixture_bound_file(
            artifact_root,
            item.get("path"),
            f"voice-transfer prerequisite {key}",
        )
        prerequisite_bound = _open_bound_input(
            prerequisite_path,
            f"voice-transfer prerequisite {key}",
            byte_cap=_TRANSFER_JSON_BYTE_CAP,
        )
        held.append(prerequisite_bound)
        prerequisite_bounds[key] = prerequisite_bound
        if prerequisite_bound.sha256 != item["sha256"]:
            raise ValidationError(
                f"voice-transfer prerequisite {key} SHA-256 mismatch"
            )
    if receipt["prerequisite_sha256s"] != expected_prerequisite_hashes:
        raise ValidationError("voice-transfer prerequisite SHA-256 set mismatch")

    source_proof = _strict_object(
        receipt["source_proof"],
        {
            "git_head",
            "runtime_commit",
            "remote_state_checked",
            "git_network_called",
            "git_status_scope",
            "git_execution_by_descriptor",
            "git_absolute_path_identity_checked_pre_and_post",
            "git_path_swap_risk",
            "head_delta_policy",
            "head_delta_path",
        },
        "voice-transfer source proof",
    )
    expected_delta_path = (
        "operator-blueprint-v2/02-narration-production/fixtures/"
        f"{artifact_root.name}/{authorization_relative}"
    )
    if (
        not isinstance(source_proof["git_head"], str)
        or not _HEX_40_RE.fullmatch(source_proof["git_head"])
        or source_proof["runtime_commit"] != runtime_bindings.get("git_commit")
        or source_proof["remote_state_checked"] is not False
        or source_proof["git_network_called"] is not False
        or source_proof["git_status_scope"]
        != "repository_index_and_unignored_worktree_only"
        or source_proof["git_execution_by_descriptor"] is not False
        or source_proof[
            "git_absolute_path_identity_checked_pre_and_post"
        ]
        is not True
        or source_proof["git_path_swap_risk"]
        != "root_owned_system_binary_not_same_uid_writable"
        or source_proof["head_delta_policy"]
        != "exact_active_authorization_path_only"
        or source_proof["head_delta_path"] != expected_delta_path
    ):
        raise ValidationError("voice-transfer source proof does not bind the ACTIVE/runtime boundary")
    _replay_transfer_source_proof(
        source_proof,
        runtime_bindings,
        authorization_bound,
        plan_bound,
        canonical_w_bound,
        prerequisite_bounds,
    )
    if runtime_bindings_out is not None:
        runtime_bindings_out.clear()
        runtime_bindings_out.update(runtime_bindings)

    request = _strict_object(
        receipt["request"],
        {
            "part_id",
            "primary_request_sha256",
            "normalized_http_request_sha256",
            "method",
            "exact_url",
            "multipart_body_sha256",
            "multipart_body_bytes",
            "content_type",
            "credential_header_name",
            "accept",
            "accept_encoding",
        },
        "voice-transfer request evidence",
    )
    action_query = action.get("query")
    if not isinstance(action_query, dict) or type(action_query.get("enable_logging")) is not bool:
        raise ValidationError("voice-transfer ACTIVE logging mode is not final")
    logging_value = "true" if action_query["enable_logging"] else "false"
    expected_url = (
        f"{action.get('endpoint')}?enable_logging={logging_value}"
        f"&output_format={action_query.get('output_format')}"
    )
    expected_request = {
        "part_id": _TRANSFER_PART_ID,
        "primary_request_sha256": bindings.get("primary_request_sha256"),
        "normalized_http_request_sha256": bindings.get(
            "normalized_http_request_sha256"
        ),
        "method": action.get("method"),
        "exact_url": expected_url,
        "multipart_body_sha256": bindings.get("primary_multipart_body_sha256"),
        "multipart_body_bytes": bindings.get("primary_multipart_body_bytes"),
        "content_type": bindings.get("multipart_content_type"),
        "credential_header_name": action.get("credential_header_name"),
        "accept": action.get("accept"),
        "accept_encoding": action.get("accept_encoding"),
    }
    if request != expected_request:
        raise ValidationError("voice-transfer request/body/part identity mismatch")
    if receipt["method"] != action.get("method") or receipt["endpoint"] != action.get("endpoint"):
        raise ValidationError("voice-transfer top-level endpoint or method drifted")

    _validate_transfer_provider_evidence(receipt["provider_evidence"])
    response = _strict_object(
        receipt["response"],
        {
            "http_status",
            "response_bytes",
            "response_sha256",
            "declared_mime_type",
            "content_encoding",
            "media_interpretation",
        },
        "voice-transfer response evidence",
    )
    media_interpretation = _strict_object(
        response["media_interpretation"],
        {
            "classification",
            "output_format",
            "declared_mime_allowlist",
            "compressed_or_container_signature_detected",
            "negative_ffprobe_detected_format",
            "headerless_bytes_intrinsically_prove_codec_geometry",
            "official_media_contract_sha256",
        },
        "voice-transfer media interpretation",
    )
    if (
        type(response["http_status"]) is not int
        or response["http_status"] != 200
        or response["declared_mime_type"]
        not in _TRANSFER_DECLARED_MIME_ALLOWLIST
        or response["content_encoding"] != "identity"
        or media_interpretation
        != {
            "classification": "interpreted_pcm_under_exact_format_contract",
            "output_format": "pcm_48000",
            "declared_mime_allowlist": ["audio/pcm", "audio/mpeg"],
            "compressed_or_container_signature_detected": False,
            "negative_ffprobe_detected_format": False,
            "headerless_bytes_intrinsically_prove_codec_geometry": False,
            "official_media_contract_sha256": _TRANSFER_MEDIA_CONTRACT_SHA256,
        }
    ):
        raise ValidationError(
            "voice-transfer response is outside the exact HTTP 200 identity PCM interpretation contract"
        )

    consumption_relative = receipt["consumption_record_path"]
    if consumption_relative != consumption_binding.get("record_path"):
        raise ValidationError("voice-transfer latch path differs from ACTIVE authorization")
    consumption_path = _bound_existing_file(
        artifact_root,
        consumption_relative,
        "voice-transfer consumption latch",
        prefix="authorizations",
        suffix=".json",
    )
    if consumption_path.parent != artifact_root / "authorizations" / "consumed":
        raise ValidationError("voice-transfer consumption latch must remain under authorizations/consumed/")
    consumption_bound = _open_bound_input(
        consumption_path,
        "voice-transfer consumption latch",
        byte_cap=_TRANSFER_JSON_BYTE_CAP,
        required_mode=0o600,
    )
    held.append(consumption_bound)
    consumption_sha = consumption_bound.sha256
    if (
        not isinstance(receipt["consumption_record_sha256"], str)
        or not _HEX_64_RE.fullmatch(receipt["consumption_record_sha256"])
        or receipt["consumption_record_sha256"] != consumption_sha
    ):
        raise ValidationError("voice-transfer consumption-latch SHA-256 mismatch")
    consumption = _strict_json_bytes(
        consumption_bound.data,
        "voice-transfer consumption latch",
    )
    _strict_object(
        consumption,
        {
            "schema_version",
            "authorization_id",
            "authorization_path",
            "authorization_sha256",
            "scope",
            "status",
            "consumed_at",
            "consumed_before_credential_access",
            "credential_accessed_at_consumption",
            "network_called_at_consumption",
            "account_get_calls_used",
            "generation_post_calls_used",
            "outputs_received",
            "spend_used_usd",
            "primary_request_sha256",
            "multipart_body_sha256",
        },
        "voice-transfer consumption latch",
    )
    if (
        consumption["schema_version"] != _TRANSFER_CONSUMPTION_SCHEMA
        or consumption["authorization_id"] != authorization.get("authorization_id")
        or consumption["authorization_path"] != authorization_relative
        or consumption["authorization_sha256"] != authorization_sha
        or consumption["scope"] != _TRANSFER_SCOPE
        or consumption["status"] != "consumed_before_credential_and_network"
        or consumption["consumed_before_credential_access"] is not True
        or consumption["credential_accessed_at_consumption"] is not False
        or consumption["network_called_at_consumption"] is not False
        or type(consumption["account_get_calls_used"]) is not int
        or consumption["account_get_calls_used"] != 0
        or type(consumption["generation_post_calls_used"]) is not int
        or consumption["generation_post_calls_used"] != 0
        or type(consumption["outputs_received"]) is not int
        or consumption["outputs_received"] != 0
        or type(consumption["spend_used_usd"]) not in {int, float}
        or consumption["spend_used_usd"] != 0
        or consumption["primary_request_sha256"]
        != bindings.get("primary_request_sha256")
        or consumption["multipart_body_sha256"]
        != bindings.get("primary_multipart_body_sha256")
    ):
        raise ValidationError("voice-transfer consumption latch semantics are invalid")

    started_at = _aware_time(receipt["started_at"], "voice-transfer started_at")
    completed_at = _aware_time(receipt["completed_at"], "voice-transfer completed_at")
    consumed_at = _aware_time(consumption["consumed_at"], "voice-transfer consumed_at")
    if not consumed_at <= started_at <= completed_at:
        raise ValidationError("voice-transfer latch/run chronology is invalid")

    raw_output = _strict_object(
        receipt["raw_output"],
        {
            "part_id",
            "path",
            "sha256",
            "byte_count",
            "container_interpretation",
            "codec_interpretation",
            "sample_rate_hz_interpretation",
            "channel_count_interpretation",
            "bit_depth_interpretation",
            "frame_count_under_mono_contract_interpretation",
            "duration_seconds_under_mono_contract_interpretation",
            "output_to_source_duration_ratio_under_mono_contract_interpretation",
            "format_parameters_intrinsically_verified",
            "channel_count_intrinsically_verified",
            "frame_and_duration_computed_under_mono_contract_interpretation",
            "lossy_interpretation",
        },
        "voice-transfer raw output",
    )
    requested_raw = Path(os.path.abspath(path))
    expected_raw = Path(os.path.abspath(artifact_root / _TRANSFER_RAW_PATH))
    if requested_raw != expected_raw:
        raise ValidationError("voice-transfer raw PCM path is not the fixed ACTIVE destination")
    if raw_bound is None:
        raw_bound = _open_bound_input(
            expected_raw,
            "voice-transfer raw PCM",
            byte_cap=_TRANSFER_RAW_BYTE_CAP,
            required_mode=0o600,
        )
        held.append(raw_bound)
    else:
        if raw_bound.path != expected_raw or raw_bound.required_mode != 0o600:
            raise ValidationError(
                "voice-transfer raw descriptor is not bound to the fixed private destination"
            )
        _revalidate_bound_input(raw_bound)
    resolved_raw = raw_bound.path
    raw_hash = raw_bound.sha256
    raw_size = len(raw_bound.data)
    if raw_size == 0 or raw_size % 2:
        raise ValidationError("voice-transfer raw PCM is empty or not signed-16-bit aligned")
    if not any(raw_bound.data):
        raise ValidationError("voice-transfer raw PCM is silent")
    frame_count = raw_size // 2
    duration = frame_count / _TRANSFER_SAMPLE_RATE_HZ
    if not _TRANSFER_MIN_DURATION_SECONDS <= duration <= _TRANSFER_MAX_DURATION_SECONDS:
        raise ValidationError("voice-transfer raw PCM duration is outside 20 to 50 seconds")
    duration_ratio = duration / _TRANSFER_SELECTED_GUIDE_DURATION_SECONDS
    if not (
        _TRANSFER_MIN_OUTPUT_TO_SOURCE_DURATION_RATIO
        <= duration_ratio
        <= _TRANSFER_MAX_OUTPUT_TO_SOURCE_DURATION_RATIO
    ):
        raise ValidationError(
            "voice-transfer raw PCM is outside the 0.8 to 1.2 source-duration ratio"
        )
    header = raw_bound.data[:12]
    if (
        header.startswith(
            (
                b"RIFF",
                b"FORM",
                b"ID3",
                b"fLaC",
                b"OggS",
                b"\x1aE\xdf\xa3",
                b"\x00\x00\x01\xba",
            )
        )
        or (len(header) >= 2 and header[0] == 0xFF and header[1] & 0xE0 == 0xE0)
        or (len(header) >= 12 and header[4:8] == b"ftyp")
    ):
        raise ValidationError("voice-transfer raw PCM contains a container or lossy header")
    from . import performance_transfer as pt

    _revalidate_bound_input(raw_bound)
    try:
        _negative_ffprobe_media_detection(
            raw_bound.data,
            ffprobe_path=runtime_bindings.get("ffprobe_binary_path"),
            ffprobe_sha256=runtime_bindings.get("ffprobe_binary_sha256"),
            ffprobe_version=runtime_bindings.get("ffprobe_version"),
        )
    except pt._GuideExecutionFailure as exc:
        raise ValidationError(
            f"voice-transfer negative ffprobe failed closed: {exc.code}"
        ) from None
    finally:
        _revalidate_bound_input(raw_bound)
    if (
        raw_output["part_id"] != _TRANSFER_PART_ID
        or raw_output["path"] != _TRANSFER_RAW_PATH
        or raw_output["sha256"] != raw_hash
        or type(raw_output["byte_count"]) is not int
        or raw_output["byte_count"] != raw_size
        or raw_output["container_interpretation"] != "raw"
        or raw_output["codec_interpretation"] != "pcm_s16le"
        or type(raw_output["sample_rate_hz_interpretation"]) is not int
        or raw_output["sample_rate_hz_interpretation"]
        != _TRANSFER_SAMPLE_RATE_HZ
        or type(raw_output["channel_count_interpretation"]) is not int
        or raw_output["channel_count_interpretation"] != 1
        or type(raw_output["bit_depth_interpretation"]) is not int
        or raw_output["bit_depth_interpretation"] != 16
        or type(raw_output["frame_count_under_mono_contract_interpretation"])
        is not int
        or raw_output["frame_count_under_mono_contract_interpretation"]
        != frame_count
        or type(
            raw_output["duration_seconds_under_mono_contract_interpretation"]
        )
        not in {int, float}
        or not math.isclose(
            float(
                raw_output[
                    "duration_seconds_under_mono_contract_interpretation"
                ]
            ),
            duration,
            rel_tol=0.0,
            abs_tol=1e-12,
        )
        or type(
            raw_output[
                "output_to_source_duration_ratio_under_mono_contract_interpretation"
            ]
        )
        not in {int, float}
        or not math.isclose(
            float(
                raw_output[
                    "output_to_source_duration_ratio_under_mono_contract_interpretation"
                ]
            ),
            duration_ratio,
            rel_tol=0.0,
            abs_tol=1e-12,
        )
        or raw_output["format_parameters_intrinsically_verified"] is not False
        or raw_output["channel_count_intrinsically_verified"] is not False
        or raw_output[
            "frame_and_duration_computed_under_mono_contract_interpretation"
        ]
        is not True
        or raw_output["lossy_interpretation"] is not False
        or type(response["response_bytes"]) is not int
        or response["response_bytes"] != raw_size
        or response["response_sha256"] != raw_hash
    ):
        raise ValidationError("voice-transfer raw PCM hash, geometry, or response binding mismatch")

    if (
        plan_bound.sha256 != receipt["plan_sha256"]
        or canonical_w_bound.sha256 != receipt["canonical_w_sha256"]
    ):
        raise ValidationError("voice-transfer plan or canonical W SHA-256 mismatch")
    for bound in held:
        _revalidate_bound_input(bound)
    if all(bound is not raw_bound for bound in held):
        _revalidate_bound_input(raw_bound)

    return ({
        "requested_output_format": "pcm_48000",
        "container_interpretation": "raw",
        "codec_interpretation": "pcm_s16le",
        "sample_rate_hz_interpretation": _TRANSFER_SAMPLE_RATE_HZ,
        "channel_count_interpretation": 1,
        "bit_depth_interpretation": 16,
        "frame_count_under_mono_contract_interpretation": frame_count,
        "duration_seconds_under_mono_contract_interpretation": duration,
        "output_to_source_duration_ratio_under_mono_contract_interpretation": duration_ratio,
        "format_parameters_intrinsically_verified": False,
        "channel_count_intrinsically_verified": False,
        "frame_and_duration_computed_under_mono_contract_interpretation": True,
        "lossy_interpretation": False,
        "part_id": _TRANSFER_PART_ID,
        "authorization_sha256": authorization_sha,
        "consumption_record_sha256": consumption_sha,
        "authorized_working_output_path": str(
            _no_symlink_path(
                artifact_root / artifacts["working_output_path"],
                "voice-transfer authorized working output",
                must_exist=False,
            )
        ),
        "authorized_conversion_receipt_path": str(
            _no_symlink_path(
                artifact_root / artifacts["conversion_receipt_path"],
                "voice-transfer authorized conversion receipt",
                must_exist=False,
            )
        ),
    }, raw_hash, raw_size, receipt_hash)


def _reserve_private_file(path: Path, label: str) -> tuple[Path, int]:
    """Reserve one new owner-only file without following symlinks."""

    requested = _no_symlink_path(path, label, must_exist=False)
    if requested.exists() or requested.is_symlink():
        raise ValidationError(f"refusing to overwrite {label}: {requested}")
    requested.parent.mkdir(parents=True, exist_ok=True)
    absolute = _no_symlink_path(requested, label, must_exist=False)
    if not absolute.parent.is_dir():
        raise ValidationError(f"{label} parent is not a directory")
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    descriptor: int | None = None
    try:
        descriptor = os.open(absolute, flags, 0o600)
        os.fchmod(descriptor, 0o600)
    except FileExistsError as exc:
        raise ValidationError(f"refusing to overwrite {label}: {absolute}") from exc
    except OSError as exc:
        if descriptor is not None:
            os.close(descriptor)
        if absolute.exists() and not absolute.is_symlink():
            absolute.unlink()
        raise ValidationError(f"cannot reserve {label}: {absolute}") from exc
    assert descriptor is not None
    return absolute, descriptor


def _run(
    command: list[str], *, pass_fds: tuple[int, ...] = ()
) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(
            command,
            text=True,
            capture_output=True,
            check=False,
            pass_fds=pass_fds,
            env=_media_subprocess_environment(),
        )
    except OSError as exc:
        raise ValidationError(f"cannot run {command[0]}: {exc}") from exc


def inspect_audio(
    path: Path,
    *,
    _transfer_runtime_bindings: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if not path.is_file():
        raise ValidationError(f"audio file does not exist: {path}")
    arguments = [
            "-v",
            "error",
            "-show_streams",
            "-show_format",
            "-of",
            "json",
            str(path),
        ]
    if _transfer_runtime_bindings is None:
        result = _run(["ffprobe", *arguments])
    else:
        result = _run_transfer_media_tool(
            "ffprobe",
            arguments,
            _transfer_runtime_bindings,
            timeout_seconds=_TRANSFER_FFPROBE_TIMEOUT_SECONDS,
        )
    if result.returncode != 0:
        raise ValidationError(f"ffprobe rejected {path}: {result.stderr.strip()}")
    try:
        probe = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise ValidationError(f"ffprobe returned invalid JSON for {path}") from exc
    streams = [stream for stream in probe.get("streams", []) if stream.get("codec_type") == "audio"]
    if len(streams) != 1:
        raise ValidationError(f"expected exactly one audio stream, got {len(streams)}")
    stream = streams[0]
    codec = str(stream.get("codec_name", ""))
    try:
        sample_rate = int(stream.get("sample_rate"))
        channels = int(stream.get("channels"))
        duration = float(stream.get("duration") or probe.get("format", {}).get("duration"))
    except (TypeError, ValueError) as exc:
        raise ValidationError("ffprobe omitted required sample-rate, channel, or duration data") from exc
    bit_rate_raw = stream.get("bit_rate") or probe.get("format", {}).get("bit_rate")
    try:
        bit_rate = int(bit_rate_raw) if bit_rate_raw is not None else None
    except (TypeError, ValueError):
        bit_rate = None
    bits_raw = stream.get("bits_per_raw_sample") or stream.get("bits_per_sample")
    try:
        bit_depth = int(bits_raw) if bits_raw else None
    except (TypeError, ValueError):
        bit_depth = None
    codec_depths = {
        "pcm_s16le": 16,
        "pcm_s24le": 24,
        "pcm_s32le": 32,
        "pcm_f32le": 32,
        "pcm_f64le": 64,
    }
    bit_depth = bit_depth or codec_depths.get(codec)
    format_name = str(probe.get("format", {}).get("format_name", ""))
    if codec.startswith("pcm_"):
        origin_class = "native_pcm"
    elif codec == "mp3":
        origin_class = "lossy_mp3"
    else:
        origin_class = "unsupported"
    is_approved_mp3 = (
        codec == "mp3"
        and sample_rate == 44_100
        and channels == 1
        and bit_rate is not None
        and 190_000 <= bit_rate <= 194_000
    )
    is_working_master = (
        codec == "pcm_s24le"
        and sample_rate == 48_000
        and channels == 1
        and "wav" in format_name.split(",")
    )
    result = {
        "path": str(path.resolve()),
        "sha256": sha256_file(path),
        "codec_name": codec,
        "container": format_name,
        "sample_rate_hz": sample_rate,
        "channels": channels,
        "bit_depth": bit_depth,
        "bit_rate_bps": bit_rate,
        "duration_seconds": duration,
        "origin_class": origin_class,
        "is_approved_mp3_fallback": is_approved_mp3,
        "is_working_master": is_working_master,
    }
    return result


def inspect_provider_raw_pcm(
    path: Path,
    receipt_path: Path,
    part_id: str | None = None,
    *,
    _transfer_raw_bound: _BoundInput | None = None,
    _transfer_runtime_bindings: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Inspect headerless provider PCM only when bound to a capture receipt.

    Raw S16LE has no self-describing header. Its byte geometry and immutable
    hash are checked here; codec/rate/channel claims must also match the
    credential-free provider receipt generated by this runtime.
    """
    path = _no_symlink_path(path, "raw PCM source", must_exist=True)
    receipt_path = _no_symlink_path(
        receipt_path, "raw PCM receipt", must_exist=True
    )
    receipt_hash = sha256_file(receipt_path)
    receipt = _strict_json(receipt_path, "raw PCM receipt")
    if sha256_file(receipt_path) != receipt_hash:
        raise ValidationError("raw PCM receipt changed during validation")
    schema_version = receipt.get("schema_version")
    if schema_version not in {
        _CAPTURE_RUN_SCHEMA,
        _DIRECTED_RUN_SCHEMA,
        _TRANSFER_RUN_SCHEMA,
    }:
        raise ValidationError(
            "raw PCM requires an exact provider-capture, directed-bakeoff, or voice-transfer run receipt"
        )
    transfer_raw_parts = Path(_TRANSFER_RAW_PATH).parts
    fixed_transfer_path = (
        len(path.parts) >= len(transfer_raw_parts)
        and path.parts[-len(transfer_raw_parts) :] == transfer_raw_parts
        and receipt_path.parent.name == "elevenlabs"
        and receipt_path.parent.parent.name == "receipts"
    )
    transfer_receipt = schema_version == _TRANSFER_RUN_SCHEMA or fixed_transfer_path
    if transfer_receipt:
        item, raw_hash, size, receipt_hash = _inspect_voice_transfer_raw_pcm(
            path,
            receipt_path,
            part_id,
            _transfer_raw_bound,
            _transfer_runtime_bindings,
        )
        schema_version = _TRANSFER_RUN_SCHEMA
    else:
        raw_hash = sha256_file(path)
        size = path.stat().st_size
    if schema_version == _DIRECTED_RUN_SCHEMA:
        item = _inspect_directed_raw_pcm(path, receipt_path, receipt, raw_hash, part_id)
    elif schema_version == _CAPTURE_RUN_SCHEMA:
        matches = [
            item
            for item in receipt.get("results", [])
            if isinstance(item, dict)
            and item.get("raw_sha256") == raw_hash
            and (part_id is None or item.get("part_id") == part_id)
        ]
        if len(matches) != 1:
            raise ValidationError(
                "raw PCM hash/part does not match exactly one provider receipt result"
            )
        item = matches[0]
    expected = {
        "requested_output_format": "pcm_48000",
        "actual_codec": "pcm_s16le",
        "container": "raw",
        "sample_rate_hz": 48_000,
        "channels": 1,
        "bit_depth": 16,
        "lossy_origin": False,
    }
    errors = [] if transfer_receipt else [
        f"raw PCM receipt {key} mismatch"
        for key, value in expected.items()
        if item.get(key) != value
    ]
    if size == 0 or size % 2:
        errors.append("raw PCM byte length is empty or not aligned to signed 16-bit samples")
    if errors:
        raise ValidationError(errors)
    if not transfer_receipt:
        if sha256_file(path) != raw_hash:
            raise ValidationError("raw PCM source changed during validation")
        if sha256_file(receipt_path) != receipt_hash:
            raise ValidationError("raw PCM receipt changed during validation")
    if schema_version == _TRANSFER_RUN_SCHEMA:
        result = {
            "path": str(path),
            "sha256": raw_hash,
            "byte_count": size,
            "requested_output_format": "pcm_48000",
            **{
                key: item[key]
                for key in (
                    "container_interpretation",
                    "codec_interpretation",
                    "sample_rate_hz_interpretation",
                    "channel_count_interpretation",
                    "bit_depth_interpretation",
                    "frame_count_under_mono_contract_interpretation",
                    "duration_seconds_under_mono_contract_interpretation",
                    "output_to_source_duration_ratio_under_mono_contract_interpretation",
                    "format_parameters_intrinsically_verified",
                    "channel_count_intrinsically_verified",
                    "frame_and_duration_computed_under_mono_contract_interpretation",
                    "lossy_interpretation",
                )
            },
            "capture_receipt_schema_version": schema_version,
            "capture_receipt_sha256": receipt_hash,
            "part_id": item["part_id"],
            "authorization_sha256": item["authorization_sha256"],
            "consumption_record_sha256": item["consumption_record_sha256"],
            "authorized_working_output_path": item[
                "authorized_working_output_path"
            ],
            "authorized_conversion_receipt_path": item[
                "authorized_conversion_receipt_path"
            ],
        }
    else:
        result = {
            "path": str(path),
            "sha256": raw_hash,
            "codec_name": "pcm_s16le",
            "container": "raw",
            "sample_rate_hz": 48_000,
            "channels": 1,
            "bit_depth": 16,
            "bit_rate_bps": 768_000,
            "duration_seconds": size / (48_000 * 2),
            "origin_class": "native_pcm",
            "is_approved_mp3_fallback": False,
            "is_working_master": False,
            "capture_receipt_schema_version": schema_version,
            "capture_receipt_sha256": receipt_hash,
            "part_id": item.get("part_id") or item.get("request_id"),
        }
    return result


def validate_pcm_failure_receipt(receipt_path: Path, raw_path: Path) -> dict[str, Any]:
    receipt = read_json(receipt_path)
    errors: list[str] = []
    if receipt.get("schema_version") != "oe-pcm-capability-failure-v1":
        errors.append("fallback receipt must use oe-pcm-capability-failure-v1")
    if receipt.get("provider") != "elevenlabs":
        errors.append("fallback receipt provider must be elevenlabs")
    if receipt.get("attempted_output_format") != "pcm_48000":
        errors.append("fallback receipt must document a pcm_48000 attempt")
    if receipt.get("fallback_output_format") != "mp3_44100_192":
        errors.append("fallback receipt must authorize only mp3_44100_192")
    failure = receipt.get("failure")
    if not isinstance(failure, dict):
        errors.append("fallback receipt.failure must be an object")
        failure = {}
    status = failure.get("http_status")
    if status not in {400, 404, 422}:
        errors.append("fallback requires an explicit non-retryable 400, 404, or 422 PCM capability response")
    if failure.get("kind") != "pcm_capability_unavailable":
        errors.append("fallback failure.kind must be pcm_capability_unavailable")
    if failure.get("retryable") is not False:
        errors.append("fallback failure must explicitly be non-retryable")
    for field in ("provider_code", "message", "occurred_at"):
        if not isinstance(failure.get(field), str) or not failure.get(field):
            errors.append(f"fallback receipt.failure.{field} is required")
    raw = receipt.get("raw_output")
    if not isinstance(raw, dict):
        errors.append("fallback receipt.raw_output must be an object")
        raw = {}
    if raw.get("sha256") != sha256_file(raw_path):
        errors.append("fallback receipt raw-output hash does not match the immutable MP3")
    if errors:
        raise ValidationError(errors)
    return receipt


def convert_working(
    raw_path: Path,
    output_path: Path,
    receipt_path: Path | None = None,
    part_id: str | None = None,
    record_path: Path | None = None,
) -> dict[str, Any]:
    held_inputs: list[_BoundInput] = []
    try:
        return _convert_working_impl(
            raw_path,
            output_path,
            receipt_path,
            part_id,
            record_path,
            held_inputs,
        )
    finally:
        for bound in reversed(held_inputs):
            _close_bound_input(bound)


def _convert_working_impl(
    raw_path: Path,
    output_path: Path,
    receipt_path: Path | None = None,
    part_id: str | None = None,
    record_path: Path | None = None,
    held_inputs: list[_BoundInput] | None = None,
) -> dict[str, Any]:
    if held_inputs is None:
        held_inputs = []
    raw_path = _no_symlink_path(raw_path, "raw audio source", must_exist=True)
    if receipt_path is not None:
        receipt_path = _no_symlink_path(
            receipt_path, "audio provenance receipt", must_exist=True
        )
    output_path = _no_symlink_path(output_path, "working audio", must_exist=False)
    if record_path is not None:
        record_path = _no_symlink_path(
            record_path, "conversion record", must_exist=False
        )
    if output_path.exists() or output_path.is_symlink():
        raise ValidationError(f"refusing to overwrite working audio: {output_path}")
    if record_path is not None and (record_path.exists() or record_path.is_symlink()):
        raise ValidationError(f"refusing to overwrite conversion record: {record_path}")
    raw_pcm = False
    transfer_raw_bound: _BoundInput | None = None
    transfer_runtime_bindings: dict[str, Any] = {}
    transfer_raw_parts = Path(_TRANSFER_RAW_PATH).parts
    fixed_transfer_conversion = (
        receipt_path is not None
        and len(raw_path.parts) >= len(transfer_raw_parts)
        and raw_path.parts[-len(transfer_raw_parts) :] == transfer_raw_parts
        and receipt_path.parent.name == "elevenlabs"
        and receipt_path.parent.parent.name == "receipts"
    )
    if fixed_transfer_conversion:
        transfer_raw_bound = _open_bound_input(
            raw_path,
            "voice-transfer raw PCM",
            byte_cap=_TRANSFER_RAW_BYTE_CAP,
            required_mode=0o600,
        )
        held_inputs.append(transfer_raw_bound)
        source = inspect_provider_raw_pcm(
            raw_path,
            receipt_path,
            part_id,
            _transfer_raw_bound=transfer_raw_bound,
            _transfer_runtime_bindings=transfer_runtime_bindings,
        )
        raw_pcm = True
    else:
        try:
            source = inspect_audio(raw_path)
        except ValidationError as probe_error:
            if receipt_path is None:
                raise probe_error
            source = inspect_provider_raw_pcm(
                raw_path,
                receipt_path,
                part_id,
                _transfer_runtime_bindings=transfer_runtime_bindings,
            )
            raw_pcm = True
        if source.get("capture_receipt_schema_version") == _TRANSFER_RUN_SCHEMA:
            transfer_raw_bound = _open_bound_input(
                raw_path,
                "voice-transfer raw PCM",
                byte_cap=_TRANSFER_RAW_BYTE_CAP,
                required_mode=0o600,
            )
            held_inputs.append(transfer_raw_bound)
            source = inspect_provider_raw_pcm(
                raw_path,
                receipt_path,
                part_id,
                _transfer_raw_bound=transfer_raw_bound,
                _transfer_runtime_bindings=transfer_runtime_bindings,
            )
    before_hash = (
        transfer_raw_bound.sha256
        if transfer_raw_bound is not None
        else sha256_file(raw_path)
    )
    transfer_conversion = (
        source.get("capture_receipt_schema_version") == _TRANSFER_RUN_SCHEMA
    )
    if transfer_conversion and not transfer_runtime_bindings:
        raise ValidationError(
            "voice-transfer conversion lacks exact ACTIVE runtime bindings"
        )
    lossy_origin = (
        False
        if transfer_conversion
        else source["origin_class"] == "lossy_mp3"
    )
    fallback_receipt_hash: str | None = None
    if lossy_origin:
        if not source["is_approved_mp3_fallback"]:
            raise ValidationError("lossy input must be mono MP3 at exactly 44.1 kHz and 192 kbps")
        if receipt_path is None:
            raise ValidationError("MP3 fallback requires an actual PCM-capability-failure receipt")
        validate_pcm_failure_receipt(receipt_path, raw_path)
        fallback_receipt_hash = sha256_file(receipt_path)
    elif not transfer_conversion and source["origin_class"] != "native_pcm":
        raise ValidationError(f"unsupported source codec: {source['codec_name']}")
    if (
        source.get("capture_receipt_schema_version") == _DIRECTED_RUN_SCHEMA
        and record_path is None
    ):
        raise ValidationError("directed PCM conversion requires an immutable conversion record")
    if transfer_conversion:
        if record_path is None:
            raise ValidationError(
                "voice-transfer PCM conversion requires its exact immutable conversion record"
            )
        expected_output = Path(source["authorized_working_output_path"])
        expected_record = Path(source["authorized_conversion_receipt_path"])
        if Path(os.path.abspath(output_path)) != expected_output:
            raise ValidationError(
                "voice-transfer working output differs from the ACTIVE fixed destination"
            )
        if Path(os.path.abspath(record_path)) != expected_record:
            raise ValidationError(
                "voice-transfer conversion record differs from the ACTIVE fixed destination"
            )
    if record_path is not None and Path(os.path.abspath(record_path)) == Path(
        os.path.abspath(output_path)
    ):
        raise ValidationError("working audio and conversion record must be different files")

    destination_output: Path | None = None
    output_directory_descriptor: int | None = None
    output_temp_path: Path | None = None
    output_temp_name: str | None = None
    output_finalized = False
    reserved_record: Path | None = None
    output_descriptor: int | None = None
    record_descriptor: int | None = None
    try:
        if record_path is not None:
            reserved_record, record_descriptor = _reserve_private_file(
                record_path, "conversion record"
            )
        destination_output, output_directory_descriptor = _prepare_private_destination(
            output_path, "working audio"
        )
        output_temp_path, output_temp_name, output_descriptor = _reserve_private_temp(
            destination_output.parent,
            output_directory_descriptor,
            destination_output.name,
        )
        arguments = [
            "-nostdin",
            "-y",
            "-v",
            "error",
        ]
        if raw_pcm:
            arguments.extend(["-f", "s16le", "-ar", "48000", "-ac", "1"])
        if transfer_raw_bound is not None:
            _revalidate_bound_input(transfer_raw_bound)
            input_source = f"/dev/fd/{transfer_raw_bound.descriptor}"
            inherited_descriptors = (
                output_descriptor,
                transfer_raw_bound.descriptor,
            )
        else:
            input_source = str(raw_path)
            inherited_descriptors = (output_descriptor,)
        arguments.extend([
            "-i",
            input_source,
            "-map_metadata",
            "-1",
            "-vn",
            "-ac",
            "1",
            "-ar",
            "48000",
            "-c:a",
            "pcm_s24le",
            "-f",
            "wav",
            f"/dev/fd/{output_descriptor}",
        ])
        if transfer_conversion:
            result = _run_transfer_media_tool(
                "ffmpeg",
                arguments,
                transfer_runtime_bindings,
                pass_fds=inherited_descriptors,
                timeout_seconds=_TRANSFER_FFMPEG_TIMEOUT_SECONDS,
            )
        else:
            result = _run(
                ["ffmpeg", *arguments],
                pass_fds=inherited_descriptors,
            )
        if result.returncode != 0:
            raise ValidationError(f"ffmpeg conversion failed: {result.stderr.strip()}")
        os.fsync(output_descriptor)
        _same_open_regular_file(
            output_temp_path, output_descriptor, "working-audio temp file"
        )
        if transfer_raw_bound is not None:
            _revalidate_bound_input(transfer_raw_bound)
            if transfer_raw_bound.sha256 != before_hash:
                raise ValidationError("voice-transfer raw source changed during conversion")
        elif sha256_file(raw_path) != before_hash:
            raise ValidationError("raw source changed during conversion")
        converted = inspect_audio(
            output_temp_path,
            _transfer_runtime_bindings=(
                transfer_runtime_bindings if transfer_conversion else None
            ),
        )
        if not converted["is_working_master"]:
            raise ValidationError("converted output is not 48 kHz, 24-bit, mono PCM WAV")
        _validate_full_decode(
            output_temp_path,
            _transfer_runtime_bindings=(
                transfer_runtime_bindings if transfer_conversion else None
            ),
        )
        _same_open_regular_file(
            output_temp_path, output_descriptor, "working-audio temp file"
        )
        converted["path"] = str(destination_output)
        conversion = {
            "schema_version": "oe-working-conversion-v1",
            "raw": source,
            "raw_immutable_sha256": before_hash,
            "fallback_receipt_sha256": fallback_receipt_hash,
            "conversion_count_from_raw": 1,
            "working": converted,
        }
        if transfer_conversion:
            conversion.update(
                {
                    "lossy_interpretation": False,
                    "lossy_origin_intrinsically_verified": False,
                }
            )
        else:
            conversion["lossy_origin"] = lossy_origin
        _no_symlink_path(destination_output, "working audio", must_exist=False)
        if destination_output.exists() or destination_output.is_symlink():
            raise ValidationError(f"refusing to overwrite working audio: {destination_output}")
        try:
            os.link(
                output_temp_name,
                destination_output.name,
                src_dir_fd=output_directory_descriptor,
                dst_dir_fd=output_directory_descriptor,
                follow_symlinks=False,
            )
        except FileExistsError as exc:
            raise ValidationError(
                f"refusing to overwrite working audio: {destination_output}"
            ) from exc
        except OSError as exc:
            raise ValidationError("cannot exclusively finalize working audio") from exc
        output_finalized = True
        _same_open_regular_file(destination_output, output_descriptor, "working audio")
        os.unlink(output_temp_name, dir_fd=output_directory_descriptor)
        output_temp_name = None
        output_temp_path = None
        if record_descriptor is not None and reserved_record is not None:
            _same_open_regular_file(
                reserved_record, record_descriptor, "conversion record"
            )
            payload = (json.dumps(conversion, indent=2, sort_keys=True) + "\n").encode(
                "utf-8"
            )
            written = 0
            while written < len(payload):
                written += os.write(record_descriptor, payload[written:])
            os.fsync(record_descriptor)
            _same_open_regular_file(
                reserved_record, record_descriptor, "conversion record"
            )
            conversion["record"] = str(reserved_record)
        _same_open_regular_file(destination_output, output_descriptor, "working audio")
        if transfer_conversion:
            if stat.S_IMODE(os.fstat(output_descriptor).st_mode) != 0o600:
                raise ValidationError("voice-transfer working output must remain mode 0600")
            if record_descriptor is None or stat.S_IMODE(
                os.fstat(record_descriptor).st_mode
            ) != 0o600:
                raise ValidationError(
                    "voice-transfer conversion record must remain mode 0600"
                )
        os.close(output_descriptor)
        output_descriptor = None
        os.close(output_directory_descriptor)
        output_directory_descriptor = None
        if record_descriptor is not None:
            os.close(record_descriptor)
            record_descriptor = None
        return conversion
    except BaseException:
        if output_finalized and destination_output is not None:
            _unlink_at_if_same(
                output_directory_descriptor,
                destination_output.name,
                output_descriptor,
            )
        _unlink_at_if_same(
            output_directory_descriptor,
            output_temp_name,
            output_descriptor,
        )
        _unlink_reserved_if_same(reserved_record, record_descriptor)
        if output_descriptor is not None:
            os.close(output_descriptor)
        if output_directory_descriptor is not None:
            os.close(output_directory_descriptor)
        if record_descriptor is not None:
            os.close(record_descriptor)
        raise


# ---------------------------------------------------------------------------
# Additive recovery-evidence Voice Changer conversion
# ---------------------------------------------------------------------------


_RECOVERY_TRANSFER_RUN_SCHEMA = (
    "oe-elevenlabs-recovery-evidence-voice-transfer-run-v1"
)
_RECOVERY_TRANSFER_CONVERSION_SCHEMA = (
    "oe-elevenlabs-recovery-evidence-voice-transfer-conversion-v1"
)
_RECOVERY_TRANSFER_SCOPE = "elevenlabs_recovery_evidence_voice_transfer_execution"
_RECOVERY_TRANSFER_RAW_PATH = (
    "outputs/raw/elevenlabs/P01-W0030-W0110/saved-c-transfer-post-read-repair.pcm"
)
_RECOVERY_TRANSFER_WORKING_PATH = (
    "outputs/working/elevenlabs/P01-W0030-W0110/"
    "saved-c-transfer-post-read-repair.wav"
)


def _require_recovery_transfer_private_bound(bound: _BoundInput) -> None:
    metadata = os.fstat(bound.descriptor)
    if (
        stat.S_IMODE(metadata.st_mode) != 0o600
        or metadata.st_uid != os.getuid()
        or metadata.st_nlink != 1
    ):
        raise ValidationError(f"{bound.label} must remain current-UID mode-0600 single-link")


def _replay_recovery_evidence_source_proof(
    receipt: dict[str, Any],
    receipt_bound: _BoundInput,
    held_inputs: list[_BoundInput],
) -> tuple[Path, dict[str, Any], dict[str, Any], _BoundInput, _BoundInput]:
    """Replay the ACTIVE, latch, runtime, and committed-head bindings locally."""

    from . import performance_transfer as pt
    from . import voice_transfer as vt

    root = pt._document_root(receipt_bound.path)
    authorization_path = _bound_existing_file(
        root,
        receipt.get("authorization_path"),
        "recovery transfer ACTIVE authorization",
        prefix="authorizations",
        suffix=".json",
    )
    authorization_bound = _open_bound_input(
        authorization_path,
        "recovery transfer ACTIVE authorization",
        byte_cap=_TRANSFER_JSON_BYTE_CAP,
        required_mode=0o600,
    )
    held_inputs.append(authorization_bound)
    _require_recovery_transfer_private_bound(authorization_bound)
    authorization = _strict_json_bytes(
        authorization_bound.data,
        "recovery transfer ACTIVE authorization",
    )
    if (
        receipt.get("authorization_sha256") != authorization_bound.sha256
        or authorization.get("schema_version") != vt.RECOVERY_TRANSFER_AUTH_SCHEMA
        or authorization.get("status") != "active"
        or authorization.get("provider_action_authorized") is not True
        or authorization.get("authorization_id") != receipt.get("authorization_id")
        or authorization.get("scope") != _RECOVERY_TRANSFER_SCOPE
        or authorization.get("artifacts") != vt._recovery_transfer_artifacts(True)
        or authorization.get("consumption") != vt._recovery_transfer_consumption(True)
    ):
        raise ValidationError("recovery transfer ACTIVE source binding is invalid")
    errors: list[str] = []
    runtime = vt._validate_recovery_transfer_runtime_bindings(
        authorization.get("runtime_bindings"),
        active=True,
        errors=errors,
    )
    if errors:
        raise ValidationError("recovery transfer runtime source binding drifted")
    source_proof = receipt.get("source_proof")
    if not isinstance(source_proof, dict):
        raise ValidationError("recovery transfer run source proof is unavailable")
    head = vt._bound_git(runtime, ["rev-parse", "HEAD"]).strip().decode(
        "ascii", errors="strict"
    )
    if (
        head != source_proof.get("active_commit")
        or runtime.get("git_commit") != source_proof.get("runtime_commit")
        or authorization.get("evidence_baseline", {}).get("evidence_commit")
        != source_proof.get("evidence_commit")
        or source_proof.get("source_revalidated_after_latch") is not True
        or source_proof.get("post_latch_revalidation_completed") is not True
        or source_proof.get("remote_state_checked") is not False
        or source_proof.get("git_network_called") is not False
    ):
        raise ValidationError("recovery transfer run source proof did not replay")
    latch_path = _bound_existing_file(
        root,
        receipt.get("consumption_record_path"),
        "recovery transfer shared latch",
        prefix="authorizations",
        suffix=".json",
    )
    latch_bound = _open_bound_input(
        latch_path,
        "recovery transfer shared latch",
        byte_cap=_TRANSFER_JSON_BYTE_CAP,
        required_mode=0o600,
    )
    held_inputs.append(latch_bound)
    _require_recovery_transfer_private_bound(latch_bound)
    latch = _strict_json_bytes(latch_bound.data, "recovery transfer shared latch")
    if (
        latch_bound.sha256 != receipt.get("consumption_record_sha256")
        or latch.get("schema_version") != vt.RECOVERY_TRANSFER_CONSUMPTION_SCHEMA
        or latch.get("authorization_id") != receipt.get("authorization_id")
        or latch.get("generation_post_budget_consumed") is not True
        or latch.get("retry_or_replay_permitted") is not False
    ):
        raise ValidationError("recovery transfer shared latch binding is invalid")
    repository = pt._guide_repository_root()
    try:
        authorization_relative = authorization_path.relative_to(repository).as_posix()
        latch_relative = latch_path.relative_to(repository).as_posix()
        run_relative = receipt_bound.path.relative_to(repository).as_posix()
        raw_relative = (root / _RECOVERY_TRANSFER_RAW_PATH).relative_to(
            repository
        ).as_posix()
    except ValueError:
        raise ValidationError("recovery transfer generated evidence left the repository") from None
    evidence_commit = authorization.get("evidence_baseline", {}).get("evidence_commit")
    parents = vt._bound_git(
        runtime,
        ["rev-list", "--parents", "-n", "1", head],
    ).strip().split()
    active_delta = vt._bound_git(
        runtime,
        [
            "diff", "--no-ext-diff", "--no-textconv", "--no-renames",
            "--name-status", "--diff-filter=ACDMRTUXB", "-z",
            f"{evidence_commit}..{head}",
        ],
    )
    committed_active = vt._bound_git(
        runtime,
        ["show", f"{head}:{authorization_relative}"],
        max_bytes=_TRANSFER_JSON_BYTE_CAP,
    )
    if (
        not isinstance(evidence_commit, str)
        or parents != [head.encode("ascii"), evidence_commit.encode("ascii")]
        or active_delta
        != b"A\x00" + authorization_relative.encode("utf-8") + b"\x00"
        or committed_active != authorization_bound.data
        or sha256_bytes(committed_active) != authorization_bound.sha256
    ):
        raise ValidationError("recovery transfer committed ACTIVE proof did not replay")
    plan_bound, canonical_w_bound = _transfer_canonical_w_inputs(root, held_inputs)
    semantic = vt.validate_recovery_evidence_voice_transfer_authorization(
        authorization_path,
        plan_bound.path,
        canonical_w_bound.path,
        _allowed_generated_status_paths=frozenset({latch_relative, run_relative}),
        _allowed_ignored_generated_paths=frozenset({raw_relative}),
    )
    if (
        semantic.get("valid") is not True
        or semantic.get("authorization_status") != "active"
        or semantic.get("provider_action_authorized") is not True
        or semantic.get("authorization_sha256") != authorization_bound.sha256
    ):
        semantic.clear()
        raise ValidationError("recovery transfer committed ACTIVE semantics did not replay")
    semantic.clear()
    _revalidate_bound_input(authorization_bound)
    _revalidate_bound_input(latch_bound)
    return root, authorization, runtime, authorization_bound, latch_bound


def inspect_recovery_evidence_raw_pcm(
    path: Path,
    receipt_path: Path,
    part_id: str | None = None,
    *,
    _raw_bound: _BoundInput | None = None,
    _runtime_bindings_out: dict[str, Any] | None = None,
    _held_inputs: list[_BoundInput] | None = None,
) -> dict[str, Any]:
    """Inspect exact recovery-transfer raw PCM without entering legacy routing."""

    own_inputs = _held_inputs is None
    held_inputs = [] if _held_inputs is None else _held_inputs
    raw_bound = _raw_bound
    receipt_bound: _BoundInput | None = None
    authorization: dict[str, Any] = {}
    receipt: dict[str, Any] = {}
    try:
        if raw_bound is None:
            raw_bound = _open_bound_input(
                path,
                "recovery transfer raw PCM",
                byte_cap=_TRANSFER_RAW_BYTE_CAP,
                required_mode=0o600,
            )
            held_inputs.append(raw_bound)
        _require_recovery_transfer_private_bound(raw_bound)
        receipt_bound = _open_bound_input(
            receipt_path,
            "recovery transfer run receipt",
            byte_cap=_TRANSFER_JSON_BYTE_CAP,
            required_mode=0o600,
        )
        held_inputs.append(receipt_bound)
        _require_recovery_transfer_private_bound(receipt_bound)
        receipt = _strict_json_bytes(receipt_bound.data, "recovery transfer run receipt")
        root, authorization, runtime, _authorization_bound, _latch_bound = (
            _replay_recovery_evidence_source_proof(receipt, receipt_bound, held_inputs)
        )
        raw_output = receipt.get("raw_output")
        provider = receipt.get("provider_evidence")
        response = receipt.get("response")
        if not isinstance(raw_output, dict) or not isinstance(provider, dict) or not isinstance(response, dict):
            raise ValidationError("recovery transfer run evidence is incomplete")
        expected_raw = root / _RECOVERY_TRANSFER_RAW_PATH
        if (
            receipt.get("schema_version") != _RECOVERY_TRANSFER_RUN_SCHEMA
            or receipt.get("outcome") != "success"
            or receipt.get("provider") != "elevenlabs"
            or receipt.get("scope") != _RECOVERY_TRANSFER_SCOPE
            or receipt.get("method") != "POST"
            or receipt.get("part_id") != _TRANSFER_PART_ID
            or part_id not in {None, _TRANSFER_PART_ID}
            or raw_bound.path != expected_raw.absolute()
            or raw_output.get("path") != _RECOVERY_TRANSFER_RAW_PATH
            or raw_output.get("sha256") != raw_bound.sha256
            or raw_output.get("byte_count") != len(raw_bound.data)
            or response.get("http_status") != 200
            or response.get("provider_request_state") != "response_confirmed"
            or response.get("provider_response_state") != "body_complete"
            or response.get("response_sha256") != raw_bound.sha256
            or response.get("response_bytes") != len(raw_bound.data)
            or response.get("declared_mime_type") not in _TRANSFER_DECLARED_MIME_ALLOWLIST
            or response.get("content_encoding") != "identity"
            or provider.get("account_get_calls_made") != 0
            or provider.get("generation_post_budget_consumed") is not True
            or provider.get("generation_post_calls_made") != 1
            or provider.get("application_http_attempts") != 1
            or provider.get("application_retries_made") != 0
            or provider.get("application_redirects_followed") != 0
            or provider.get("application_fallbacks_used") != 0
            or provider.get("outputs_received") != 1
            or receipt.get("working_output_path") != _RECOVERY_TRANSFER_WORKING_PATH
            or receipt.get("conversion_receipt_path")
            != authorization["artifacts"]["conversion_receipt_path"]
        ):
            raise ValidationError("recovery transfer run/raw binding is invalid")
        _validate_transfer_provider_evidence(
            {
                "account_get_calls_made": provider["account_get_calls_made"],
                "generation_post_calls_made": provider["generation_post_calls_made"],
                "outputs_received": provider["outputs_received"],
                "request_ids": provider.get("request_ids"),
                "usage": provider.get("usage"),
            }
        )
        if not raw_bound.data or len(raw_bound.data) % 2:
            raise ValidationError("recovery transfer raw PCM is empty or misaligned")
        frame_count = len(raw_bound.data) // 2
        duration = len(raw_bound.data) / (_TRANSFER_SAMPLE_RATE_HZ * 2)
        if not _TRANSFER_MIN_DURATION_SECONDS <= duration <= _TRANSFER_MAX_DURATION_SECONDS:
            raise ValidationError("recovery transfer raw PCM duration is outside its bound")
        expected_interpretation = {
            "container_interpretation": "raw",
            "codec_interpretation": "pcm_s16le",
            "sample_rate_hz_interpretation": 48_000,
            "channel_count_interpretation": 1,
            "bit_depth_interpretation": 16,
            "frame_count_under_mono_contract_interpretation": frame_count,
            "duration_seconds_under_mono_contract_interpretation": duration,
            "output_to_source_duration_ratio_under_mono_contract_interpretation": (
                duration / _TRANSFER_SELECTED_GUIDE_DURATION_SECONDS
            ),
            "format_parameters_intrinsically_verified": False,
            "channel_count_intrinsically_verified": False,
            "frame_and_duration_computed_under_mono_contract_interpretation": True,
            "lossy_interpretation": False,
        }
        if any(raw_output.get(key) != value for key, value in expected_interpretation.items()):
            raise ValidationError("recovery transfer PCM interpretation evidence drifted")
        _revalidate_bound_input(raw_bound)
        _revalidate_bound_input(receipt_bound)
        if _runtime_bindings_out is not None:
            _runtime_bindings_out.update(runtime)
        return {
            "path": str(raw_bound.path),
            "sha256": raw_bound.sha256,
            "byte_count": len(raw_bound.data),
            "requested_output_format": "pcm_48000",
            "container_interpretation": raw_output["container_interpretation"],
            "codec_interpretation": raw_output["codec_interpretation"],
            "sample_rate_hz_interpretation": raw_output[
                "sample_rate_hz_interpretation"
            ],
            "channel_count_interpretation": raw_output[
                "channel_count_interpretation"
            ],
            "bit_depth_interpretation": raw_output["bit_depth_interpretation"],
            "frame_count_under_mono_contract_interpretation": raw_output[
                "frame_count_under_mono_contract_interpretation"
            ],
            "duration_seconds_under_mono_contract_interpretation": raw_output[
                "duration_seconds_under_mono_contract_interpretation"
            ],
            "output_to_source_duration_ratio_under_mono_contract_interpretation": raw_output[
                "output_to_source_duration_ratio_under_mono_contract_interpretation"
            ],
            "format_parameters_intrinsically_verified": False,
            "channel_count_intrinsically_verified": False,
            "frame_and_duration_computed_under_mono_contract_interpretation": True,
            "lossy_interpretation": False,
            "capture_receipt_schema_version": _RECOVERY_TRANSFER_RUN_SCHEMA,
            "capture_receipt_sha256": receipt_bound.sha256,
            "part_id": _TRANSFER_PART_ID,
            "authorization_sha256": receipt["authorization_sha256"],
            "consumption_record_sha256": receipt["consumption_record_sha256"],
            "authorized_working_output_path": str(root / _RECOVERY_TRANSFER_WORKING_PATH),
            "authorized_conversion_receipt_path": str(
                root / authorization["artifacts"]["conversion_receipt_path"]
            ),
        }
    finally:
        authorization.clear()
        receipt.clear()
        if own_inputs:
            for bound in reversed(held_inputs):
                _close_bound_input(bound)
                bound.data = b""
            held_inputs.clear()


def convert_recovery_evidence_working(
    raw_path: Path,
    output_path: Path,
    *,
    receipt_path: Path,
    part_id: str,
    record_path: Path,
) -> dict[str, Any]:
    """Convert one recovery-transfer raw PCM result through its own provenance path."""

    held_inputs: list[_BoundInput] = []
    result: dict[str, Any] | None = None
    code: str | None = None
    try:
        result = _convert_recovery_evidence_working_impl(
            raw_path,
            output_path,
            receipt_path=receipt_path,
            part_id=part_id,
            record_path=record_path,
            held_inputs=held_inputs,
        )
    except BaseException as failure:
        code = "recovery transfer conversion failed closed"
        failure.__traceback__ = None
        failure.__cause__ = None
        failure.__context__ = None
    finally:
        for bound in reversed(held_inputs):
            _close_bound_input(bound)
            bound.data = b""
        held_inputs.clear()
    if result is None:
        raise ValidationError(code or "recovery transfer conversion failed closed") from None
    return result


def _convert_recovery_evidence_working_impl(
    raw_path: Path,
    output_path: Path,
    *,
    receipt_path: Path,
    part_id: str,
    record_path: Path,
    held_inputs: list[_BoundInput],
) -> dict[str, Any]:
    raw_path = _no_symlink_path(raw_path, "recovery transfer raw PCM", must_exist=True)
    receipt_path = _no_symlink_path(
        receipt_path, "recovery transfer run receipt", must_exist=True
    )
    output_path = _no_symlink_path(
        output_path, "recovery transfer working audio", must_exist=False
    )
    record_path = _no_symlink_path(
        record_path, "recovery transfer conversion record", must_exist=False
    )
    if output_path.exists() or output_path.is_symlink() or record_path.exists() or record_path.is_symlink():
        raise ValidationError("recovery transfer conversion destination already exists")
    raw_bound = _open_bound_input(
        raw_path,
        "recovery transfer raw PCM",
        byte_cap=_TRANSFER_RAW_BYTE_CAP,
        required_mode=0o600,
    )
    held_inputs.append(raw_bound)
    _require_recovery_transfer_private_bound(raw_bound)
    runtime: dict[str, Any] = {}
    source = inspect_recovery_evidence_raw_pcm(
        raw_path,
        receipt_path,
        part_id,
        _raw_bound=raw_bound,
        _runtime_bindings_out=runtime,
        _held_inputs=held_inputs,
    )
    if Path(source["authorized_working_output_path"]) != Path(os.path.abspath(output_path)):
        raise ValidationError("recovery transfer working output path is not authorized")
    if Path(source["authorized_conversion_receipt_path"]) != Path(os.path.abspath(record_path)):
        raise ValidationError("recovery transfer conversion record path is not authorized")

    destination_output: Path | None = None
    output_directory_descriptor: int | None = None
    output_temp_path: Path | None = None
    output_temp_name: str | None = None
    output_descriptor: int | None = None
    reserved_record: Path | None = None
    record_descriptor: int | None = None
    output_finalized = False
    try:
        reserved_record, record_descriptor = _reserve_private_file(
            record_path, "recovery transfer conversion record"
        )
        destination_output, output_directory_descriptor = _prepare_private_destination(
            output_path, "recovery transfer working audio"
        )
        output_temp_path, output_temp_name, output_descriptor = _reserve_private_temp(
            destination_output.parent,
            output_directory_descriptor,
            destination_output.name,
        )
        _revalidate_bound_input(raw_bound)
        arguments = [
            "-nostdin", "-y", "-v", "error",
            "-f", "s16le", "-ar", "48000", "-ac", "1",
            "-i", f"/dev/fd/{raw_bound.descriptor}",
            "-map_metadata", "-1", "-vn", "-ac", "1", "-ar", "48000",
            "-c:a", "pcm_s24le", "-f", "wav", f"/dev/fd/{output_descriptor}",
        ]
        process = _run_transfer_media_tool(
            "ffmpeg",
            arguments,
            runtime,
            pass_fds=(output_descriptor, raw_bound.descriptor),
            timeout_seconds=_TRANSFER_FFMPEG_TIMEOUT_SECONDS,
        )
        if process.returncode != 0:
            raise ValidationError("recovery transfer ffmpeg conversion failed")
        os.fsync(output_descriptor)
        _same_open_regular_file(output_temp_path, output_descriptor, "recovery working temp")
        _revalidate_bound_input(raw_bound)
        converted = inspect_audio(
            output_temp_path,
            _transfer_runtime_bindings=runtime,
        )
        if not converted["is_working_master"]:
            raise ValidationError("recovery transfer working output geometry is invalid")
        _validate_full_decode(output_temp_path, _transfer_runtime_bindings=runtime)
        _same_open_regular_file(output_temp_path, output_descriptor, "recovery working temp")
        converted["path"] = str(destination_output)
        conversion = {
            "schema_version": _RECOVERY_TRANSFER_CONVERSION_SCHEMA,
            "scope": _RECOVERY_TRANSFER_SCOPE,
            "part_id": _TRANSFER_PART_ID,
            "run_receipt_sha256": source["capture_receipt_sha256"],
            "authorization_sha256": source["authorization_sha256"],
            "consumption_record_sha256": source["consumption_record_sha256"],
            "raw": source,
            "raw_immutable_sha256": raw_bound.sha256,
            "conversion_count_from_raw": 1,
            "working": converted,
            "lossy_interpretation": False,
            "lossy_origin_intrinsically_verified": False,
            "creative_approved": False,
            "step2_lock_authorized": False,
            "step3_authorized": False,
            "sharing_authorized": False,
            "publication_authorized": False,
        }
        os.link(
            output_temp_name,
            destination_output.name,
            src_dir_fd=output_directory_descriptor,
            dst_dir_fd=output_directory_descriptor,
            follow_symlinks=False,
        )
        output_finalized = True
        _same_open_regular_file(destination_output, output_descriptor, "recovery working audio")
        os.unlink(output_temp_name, dir_fd=output_directory_descriptor)
        output_temp_name = None
        output_temp_path = None
        payload = (json.dumps(conversion, indent=2, sort_keys=True) + "\n").encode("utf-8")
        written = 0
        while written < len(payload):
            count = os.write(record_descriptor, payload[written:])
            if count <= 0:
                raise OSError("short recovery conversion record write")
            written += count
        os.fsync(record_descriptor)
        _same_open_regular_file(reserved_record, record_descriptor, "recovery conversion record")
        _same_open_regular_file(destination_output, output_descriptor, "recovery working audio")
        if (
            stat.S_IMODE(os.fstat(output_descriptor).st_mode) != 0o600
            or stat.S_IMODE(os.fstat(record_descriptor).st_mode) != 0o600
        ):
            raise ValidationError("recovery transfer conversion outputs must remain mode 0600")
        conversion["record"] = str(reserved_record)
        conversion["record_sha256"] = sha256_bytes(payload)
        return conversion
    except BaseException:
        if output_finalized and destination_output is not None:
            _unlink_at_if_same(
                output_directory_descriptor,
                destination_output.name,
                output_descriptor,
            )
        _unlink_at_if_same(
            output_directory_descriptor,
            output_temp_name,
            output_descriptor,
        )
        _unlink_reserved_if_same(reserved_record, record_descriptor)
        raise
    finally:
        if output_descriptor is not None:
            os.close(output_descriptor)
        if output_directory_descriptor is not None:
            os.close(output_directory_descriptor)
        if record_descriptor is not None:
            os.close(record_descriptor)
