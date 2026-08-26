"""Isolated one-shot transport for the exact ElevenLabs B-to-Original-C call.

The parent executes descriptor-bound bytes with an exact absolute interpreter
using ``-I -S -B``. This module has no import-time I/O or network behavior.
READY is emitted only after process, descriptor, environment, and interpreter
preflights pass. The worker then accepts one command, one credential, and one
request body through four anonymous pipes, performs at most one
application-level HTTP POST, emits bounded phase/result frames, and exits.

Authorization, latch creation, the authoritative deadline, kill/reap, and
receipt materialization remain parent responsibilities. This worker never
reads a dotenv file, filesystem media, proxy configuration, or credentials
from its environment. Keep this source parseable by the bound Python 3.9.6.
"""

from __future__ import annotations

import fcntl
import hashlib
import json
import os
import re
import resource
import signal
import ssl
import stat
import struct
import sys
import threading
import time
import urllib.error
import urllib.request
from typing import Any, Dict, FrozenSet, List, Optional, Set, Tuple


# Parent/child wire contract. The parent freezes these literals independently;
# importing worker-controlled bytes is never required to authorize the child.
PROTOCOL = "oe-elevenlabs-exact-transfer-worker-v1"
FRAME_LENGTH_STRUCT = struct.Struct("!I")

READY_FRAME_MAX_BYTES = 4_096
COMMAND_FRAME_MAX_BYTES = 2_048
KEY_FRAME_MAX_BYTES = 512
PHASE_FRAME_MAX_BYTES = 2_048
RESULT_FRAME_MAX_BYTES = 8_192
RESULT_BODY_MAX_BYTES = 4_800_000
ERROR_BODY_MAX_BYTES = 65_536
SOURCE_MAX_BYTES = 1_000_000
INTERPRETER_MAX_BYTES = 100_000_000
PRE_GO_SELF_DESTRUCT_SECONDS = 30.0
PARENT_DEATH_POLL_SECONDS = 0.05
MAX_TRANSACTION_SECONDS = 300.0

EXACT_METHOD = "POST"
EXACT_URL = (
    "https://api.elevenlabs.io/v1/speech-to-speech/"
    "scMbPZwQjr40V1MzL3Nj?enable_logging=true&output_format=pcm_48000"
)
EXACT_ACCEPT = "application/octet-stream"
EXACT_CONTENT_TYPE = (
    "multipart/form-data; boundary=oe-v05-04448e9fdd50c8de67912b454e8d396f"
)
EXACT_BODY_BYTES = 1_646_839
BODY_FRAME_MAX_BYTES = EXACT_BODY_BYTES
EXACT_BODY_SHA256 = "6b57da1e6d1dc62b8ec31d34b6629da087be15f51b59998a83109f25403931dc"
EXPECTED_MIMES = frozenset({"audio/mpeg", "audio/pcm"})
SPAWN_ENVIRONMENT = {"LANG": "C", "LC_ALL": "C"}
NETWORK_STACK_ADDRESS_SELECTION_STATE = "stdlib_internal_connection_selection_possible"

READY_KEYS = frozenset(
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
COMMAND_KEYS = frozenset(
    {
        "action",
        "application_http_attempt_limit",
        "body_bytes",
        "body_sha256",
        "child_deadline_monotonic_ns",
        "protocol",
    }
)
REQUEST_STARTING_PHASE_KEYS = frozenset(
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
RESPONSE_HEADERS_PHASE_KEYS = frozenset(
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
RESULT_KEYS = frozenset(
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

_SHA_RE = re.compile(r"^[0-9a-f]{64}$")
_SAFE_LOGICAL_PATH_RE = re.compile(r"^/[A-Za-z0-9._/+-]{1,4095}$")
_SAFE_HEADER_NAME_RE = re.compile(r"^[!#$%&'*+.^_`|~0-9A-Za-z-]{1,64}$")
_SAFE_HEADER_VALUE_RE = re.compile(r"^[\x20-\x7e]{0,4096}$")
_SAFE_PROVIDER_VALUE_RE = re.compile(r"^[A-Za-z0-9._:/;=+\-]{1,256}$")
_SAFE_MIME_RE = re.compile(r"^[a-z0-9!#$&^_.+\-]+/[a-z0-9!#$&^_.+\-]+$")
_SECRET_VALUE_RE = re.compile(
    r"(?:xi[_-][0-9A-Za-z_-]{12,}|sk[_-][0-9A-Za-z_-]{12,})",
    re.I,
)
_CONTENT_LENGTH_MAX_DIGITS = 20
_MAX_HEADER_COUNT = 128
_MAX_HEADER_BYTES = 65_536
_INSPECTED_RESPONSE_HEADERS = frozenset(
    {
        "content-length",
        "content-type",
        "content-encoding",
        "request-id",
        "x-request-id",
        "eleven-request-id",
        "request-cost",
        "character-count",
        "x-ratelimit-limit",
        "x-ratelimit-remaining",
        "x-ratelimit-reset",
    }
)

ALLOWED_FAILURE_CODES = frozenset(
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

_NETWORK_STATES = frozenset(
    {"not_started", "application_request_starting", "application_request_started"}
)
_REQUEST_STATES = frozenset({"not_started", "outcome_unknown", "response_confirmed"})
_RESPONSE_STATES = frozenset(
    {
        "none",
        "headers_confirmed",
        "headers_rejected",
        "body_complete",
        "body_rejected",
    }
)
_BODY_DISPOSITIONS = frozenset(
    {"not_read", "hash_count_only", "discarded_credential_echo", "raw_success_frame"}
)
_BYTE_COUNT_STATES = frozenset({"none", "exact", "bounded_prefix"})


class _WorkerFailure(Exception):
    """A fixed-enum failure whose serialized form never contains exception text."""

    def __init__(
        self,
        code: str,
        *,
        application_http_attempts: int = 0,
        network_state: str = "not_started",
        request_state: str = "not_started",
        response_state: str = "none",
        http_status: Optional[int] = None,
        response_bytes: int = 0,
        response_sha256: Optional[str] = None,
        response_byte_count_state: str = "none",
        response_body_disposition: str = "not_read",
        content_type: Optional[str] = None,
        content_encoding: Optional[str] = None,
        provider_identifiers: Optional[Dict[str, str]] = None,
        provider_usage: Optional[Dict[str, int]] = None,
    ) -> None:
        safe_code = code if code in ALLOWED_FAILURE_CODES else "worker_internal_failure"
        super().__init__(safe_code)
        self.code = safe_code
        self.application_http_attempts = application_http_attempts if application_http_attempts in {0, 1} else 0
        self.network_state = network_state if network_state in _NETWORK_STATES else "not_started"
        self.request_state = request_state if request_state in _REQUEST_STATES else "not_started"
        self.response_state = response_state if response_state in _RESPONSE_STATES else "none"
        self.http_status = http_status if type(http_status) is int and 100 <= http_status <= 599 else None
        self.response_bytes = response_bytes if type(response_bytes) is int and response_bytes >= 0 else 0
        self.response_sha256 = (
            response_sha256
            if isinstance(response_sha256, str) and _SHA_RE.fullmatch(response_sha256)
            else None
        )
        self.response_byte_count_state = (
            response_byte_count_state
            if response_byte_count_state in _BYTE_COUNT_STATES
            else "none"
        )
        self.response_body_disposition = (
            response_body_disposition
            if response_body_disposition in _BODY_DISPOSITIONS
            else "not_read"
        )
        self.content_type = content_type if isinstance(content_type, str) else None
        self.content_encoding = content_encoding if isinstance(content_encoding, str) else None
        self.provider_identifiers = dict(provider_identifiers or {})
        self.provider_usage = dict(provider_usage or {})


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    """Make urllib surface every redirect as an HTTPError without following it."""

    def redirect_request(
        self,
        req: Any,
        fp: Any,
        code: int,
        msg: str,
        headers: Any,
        newurl: str,
    ) -> None:
        del req, fp, code, msg, headers, newurl
        return None


class _SelfDestructDeadline:
    """Kill only the worker-owned process group on deadline or parent death."""

    def __init__(self, parent_pid: int) -> None:
        self._condition = threading.Condition()
        self._parent_pid = parent_pid
        self._deadline_ns = time.monotonic_ns() + int(PRE_GO_SELF_DESTRUCT_SECONDS * 1e9)
        self._stopped = False
        self._thread = threading.Thread(
            target=self._watch,
            name="oe-elevenlabs-transfer-worker-self-destruct",
            daemon=True,
        )

    def start(self) -> None:
        self._thread.start()

    def bind(self, deadline_ns: int) -> bool:
        with self._condition:
            if self._stopped or time.monotonic_ns() >= deadline_ns:
                return False
            self._deadline_ns = deadline_ns
            self._condition.notify_all()
            return True

    def stop(self) -> None:
        with self._condition:
            self._stopped = True
            self._condition.notify_all()
        if self._thread.ident is not None and self._thread is not threading.current_thread():
            self._thread.join(timeout=0.25)

    def _watch(self) -> None:
        while True:
            with self._condition:
                if self._stopped:
                    return
                remaining_ns = self._deadline_ns - time.monotonic_ns()
                if remaining_ns <= 0 or os.getppid() != self._parent_pid:
                    break
                self._condition.wait(
                    min(PARENT_DEATH_POLL_SECONDS, remaining_ns / 1_000_000_000)
                )
        try:
            os.killpg(os.getpgrp(), signal.SIGKILL)
        except BaseException:
            os._exit(124)


def canonical_json_bytes(document: Dict[str, Any]) -> bytes:
    """Return the one accepted ASCII JSON representation for protocol objects."""

    return json.dumps(
        document,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    ).encode("ascii")


def _reject_duplicate_pairs(pairs: List[Tuple[str, Any]]) -> Dict[str, Any]:
    result: Dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON key")
        result[key] = value
    return result


def _reject_nonfinite(_value: str) -> None:
    raise ValueError("non-finite JSON number")


def _strict_json(payload: bytes, expected_keys: FrozenSet[str]) -> Dict[str, Any]:
    try:
        document = json.loads(
            payload.decode("ascii"),
            object_pairs_hook=_reject_duplicate_pairs,
            parse_constant=_reject_nonfinite,
        )
    except (UnicodeError, ValueError, TypeError):
        raise _WorkerFailure("worker_command_invalid") from None
    if (
        not isinstance(document, dict)
        or set(document) != expected_keys
        or canonical_json_bytes(document) != payload
    ):
        raise _WorkerFailure("worker_command_invalid")
    return document


def _write_all(descriptor: int, data: bytes) -> None:
    view = memoryview(data)
    offset = 0
    while offset < len(view):
        written = os.write(descriptor, view[offset:])
        if written <= 0:
            raise OSError("worker result descriptor closed")
        offset += written


def _write_frame(descriptor: int, payload: bytes, cap: int) -> None:
    if not isinstance(payload, bytes) or len(payload) > cap:
        raise OSError("worker frame exceeds cap")
    _write_all(descriptor, FRAME_LENGTH_STRUCT.pack(len(payload)))
    _write_all(descriptor, payload)


def _read_exact(descriptor: int, size: int, failure_code: str) -> bytearray:
    result = bytearray()
    while len(result) < size:
        chunk = os.read(descriptor, size - len(result))
        if not chunk:
            result.clear()
            raise _WorkerFailure(failure_code)
        result.extend(chunk)
        chunk = b""
    return result


def _read_single_frame(
    descriptor: int,
    cap: int,
    invalid_code: str,
    trailing_code: str,
) -> bytearray:
    header = _read_exact(descriptor, FRAME_LENGTH_STRUCT.size, invalid_code)
    try:
        size = FRAME_LENGTH_STRUCT.unpack(bytes(header))[0]
    finally:
        header.clear()
    if size > cap:
        raise _WorkerFailure(invalid_code)
    payload = _read_exact(descriptor, size, invalid_code)
    if os.read(descriptor, 1):
        payload.clear()
        raise _WorkerFailure(trailing_code)
    return payload


def _open_fd_set() -> Set[int]:
    flags = os.O_RDONLY
    if hasattr(os, "O_DIRECTORY"):
        flags |= os.O_DIRECTORY
    if hasattr(os, "O_CLOEXEC"):
        flags |= os.O_CLOEXEC
    scan_fd = os.open("/dev/fd", flags)
    try:
        names = os.listdir(scan_fd)
    finally:
        os.close(scan_fd)
    result: Set[int] = set()
    for name in names:
        if isinstance(name, str) and name.isascii() and name.isdigit():
            descriptor = int(name)
            try:
                os.fstat(descriptor)
            except OSError:
                # ``/dev/fd`` enumeration can expose its own already-closed
                # directory descriptors. They are not inherited live FDs.
                continue
            result.add(descriptor)
    result.discard(scan_fd)
    return result


def _close_unintended_descriptors(allowed: FrozenSet[int]) -> None:
    for descriptor in sorted(_open_fd_set() - set(allowed)):
        try:
            os.close(descriptor)
        except OSError:
            pass
    if _open_fd_set() != set(allowed):
        raise OSError("worker inherited descriptor set is not exact")


def _require_devnull(descriptor: int) -> None:
    current = os.fstat(descriptor)
    expected = os.stat("/dev/null", follow_symlinks=False)
    if (
        not stat.S_ISCHR(current.st_mode)
        or not stat.S_ISCHR(expected.st_mode)
        or current.st_rdev != expected.st_rdev
    ):
        raise OSError("standard descriptor is not /dev/null")


def _require_pipe(descriptor: int, access_mode: int) -> os.stat_result:
    info = os.fstat(descriptor)
    if not stat.S_ISFIFO(info.st_mode):
        raise OSError("worker IPC descriptor is not an anonymous pipe")
    flags = fcntl.fcntl(descriptor, fcntl.F_GETFL)
    if flags & os.O_ACCMODE != access_mode:
        raise OSError("worker IPC descriptor direction is invalid")
    return info


def _preflight_descriptors(command_fd: int, key_fd: int, body_fd: int, result_fd: int) -> None:
    allowed = frozenset({0, 1, 2, command_fd, key_fd, body_fd, result_fd})
    if len(allowed) != 7 or min(command_fd, key_fd, body_fd, result_fd) < 3:
        raise OSError("worker descriptors are not distinct")
    _close_unintended_descriptors(allowed)
    for descriptor in (0, 1, 2):
        _require_devnull(descriptor)
    identities: List[Tuple[int, int]] = []
    for descriptor in (command_fd, key_fd, body_fd):
        info = _require_pipe(descriptor, os.O_RDONLY)
        identities.append((info.st_dev, info.st_ino))
    info = _require_pipe(result_fd, os.O_WRONLY)
    identities.append((info.st_dev, info.st_ino))
    if len(set(identities)) != 4:
        raise OSError("worker IPC pipes are not distinct")
    for descriptor in (command_fd, key_fd, body_fd, result_fd):
        descriptor_flags = fcntl.fcntl(descriptor, fcntl.F_GETFD)
        fcntl.fcntl(descriptor, fcntl.F_SETFD, descriptor_flags | fcntl.FD_CLOEXEC)


def _preflight_environment() -> Dict[str, str]:
    environment = dict(os.environ)
    cf_value = environment.pop("__CF_USER_TEXT_ENCODING", None)
    if environment != SPAWN_ENVIRONMENT:
        raise OSError("worker environment is not exact")
    expected_cf_value = f"0x{os.getuid():X}:0x0:0x0"
    if cf_value is not None and cf_value != expected_cf_value:
        raise OSError("worker platform locale environment is invalid")
    flags = sys.flags
    if (
        flags.isolated != 1
        or flags.no_site != 1
        or flags.dont_write_bytecode != 1
        or flags.ignore_environment != 1
        or getattr(flags, "safe_path", True) is False
    ):
        raise OSError("worker interpreter flags are not exact")
    safe_environment = dict(SPAWN_ENVIRONMENT)
    if cf_value is not None:
        safe_environment["__CF_USER_TEXT_ENCODING"] = cf_value
    return safe_environment


def _disable_core_dumps() -> Tuple[int, int]:
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
    limits = resource.getrlimit(resource.RLIMIT_CORE)
    if limits != (0, 0):
        raise OSError("worker core dump limit is not disabled")
    return limits


def _hash_interpreter() -> Dict[str, Any]:
    path = os.path.realpath(sys.executable)
    if not os.path.isabs(sys.executable) or path != sys.executable:
        raise OSError("worker interpreter path is not canonical")
    flags = os.O_RDONLY
    if hasattr(os, "O_CLOEXEC"):
        flags |= os.O_CLOEXEC
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    descriptor = os.open(path, flags)
    digest = hashlib.sha256()
    total = 0
    try:
        before = os.fstat(descriptor)
        mode = stat.S_IMODE(before.st_mode)
        if (
            not stat.S_ISREG(before.st_mode)
            or before.st_uid not in {0, os.getuid()}
            or not 1 <= before.st_nlink <= 256
            or mode & 0o022
            or not mode & 0o111
            or not 0 < before.st_size <= INTERPRETER_MAX_BYTES
        ):
            raise OSError("worker interpreter shape is invalid")
        while total < before.st_size:
            chunk = os.read(descriptor, min(65_536, before.st_size - total))
            if not chunk:
                raise OSError("worker interpreter read was truncated")
            total += len(chunk)
            digest.update(chunk)
        if os.read(descriptor, 1):
            raise OSError("worker interpreter grew during read")
        after = os.fstat(descriptor)
        fields = (
            "st_dev",
            "st_ino",
            "st_size",
            "st_mtime_ns",
            "st_ctime_ns",
            "st_mode",
            "st_uid",
            "st_nlink",
        )
        if any(getattr(before, field) != getattr(after, field) for field in fields):
            raise OSError("worker interpreter changed during read")
    finally:
        os.close(descriptor)
    return {
        "interpreter_mode": mode,
        "interpreter_nlink": before.st_nlink,
        "interpreter_path": path,
        "interpreter_sha256": digest.hexdigest(),
        "interpreter_uid": before.st_uid,
    }


def _executed_source_identity() -> Tuple[str, str]:
    source_sha = globals().get("__OE_EXECUTED_SOURCE_SHA256__")
    logical_path = globals().get("__OE_LOGICAL_SOURCE_PATH__")
    if not isinstance(source_sha, str) or not _SHA_RE.fullmatch(source_sha):
        raise OSError("descriptor-executed worker SHA is absent")
    if (
        not isinstance(logical_path, str)
        or not _SAFE_LOGICAL_PATH_RE.fullmatch(logical_path)
        or not logical_path.endswith("/elevenlabs_transfer_worker.py")
    ):
        raise OSError("logical worker source path is invalid")
    return source_sha, logical_path


def _ready_payload(
    parent_pid: int,
    safe_environment: Dict[str, str],
    core_limits: Tuple[int, int],
) -> bytes:
    source_sha, logical_path = _executed_source_identity()
    value: Dict[str, Any] = {
        "body_bytes_read": 0,
        "command_received": False,
        "core_hard_limit": core_limits[1],
        "core_soft_limit": core_limits[0],
        "credential_bytes_read": 0,
        "environment_keys": sorted(safe_environment),
        "environment_sha256": hashlib.sha256(
            canonical_json_bytes(safe_environment)
        ).hexdigest(),
        "executed_source_sha256": source_sha,
        "logical_source_path": logical_path,
        "message": "ready",
        "network_called": False,
        "parent_pid": parent_pid,
        "pid": os.getpid(),
        "process_group_id": os.getpgrp(),
        "protocol": PROTOCOL,
        "python_version": sys.version,
        "session_id": os.getsid(0),
    }
    value.update(_hash_interpreter())
    # The bound CLT Python and the parent runtime can expose different
    # monotonic epochs on macOS. The parent maps its remaining interval onto
    # this child-clock sample; no parent-clock absolute value is accepted.
    value["monotonic_ns_at_ready"] = time.monotonic_ns()
    if set(value) != READY_KEYS:
        raise OSError("worker READY shape drifted")
    payload = canonical_json_bytes(value)
    if len(payload) > READY_FRAME_MAX_BYTES:
        raise OSError("worker READY frame exceeds cap")
    return payload


def _parse_command(payload: bytes, watchdog: _SelfDestructDeadline) -> int:
    document = _strict_json(payload, COMMAND_KEYS)
    if (
        document.get("protocol") != PROTOCOL
        or document.get("action") != "release_exact_transfer"
        or type(document.get("application_http_attempt_limit")) is not int
        or document.get("application_http_attempt_limit") != 1
        or type(document.get("body_bytes")) is not int
        or document.get("body_bytes") != EXACT_BODY_BYTES
        or document.get("body_sha256") != EXACT_BODY_SHA256
    ):
        raise _WorkerFailure("worker_command_invalid")
    deadline_ns = document.get("child_deadline_monotonic_ns")
    now_ns = time.monotonic_ns()
    if (
        type(deadline_ns) is not int
        or deadline_ns <= now_ns
        or deadline_ns - now_ns > int(MAX_TRANSACTION_SECONDS * 1_000_000_000)
    ):
        raise _WorkerFailure("worker_deadline_invalid")
    if not watchdog.bind(deadline_ns):
        raise _WorkerFailure("worker_deadline_expired_before_request")
    return deadline_ns


def _parse_key(payload: bytearray) -> bytearray:
    if (
        not payload
        or len(payload) > KEY_FRAME_MAX_BYTES
        or any(value < 33 or value > 126 for value in payload)
    ):
        payload.clear()
        raise _WorkerFailure("worker_key_invalid")
    return payload


def _strict_headers(value: Any) -> Dict[str, str]:
    try:
        raw_items = getattr(value, "raw_items", None)
        items = raw_items() if callable(raw_items) else value.items()
        iterator = iter(items)
    except BaseException:
        raise _WorkerFailure("provider_response_headers_invalid") from None
    result: Dict[str, str] = {}
    total = 2  # terminating CRLF
    count = 0
    try:
        for pair in iterator:
            count += 1
            if count > _MAX_HEADER_COUNT:
                raise _WorkerFailure("provider_response_headers_invalid")
            if not isinstance(pair, (tuple, list)) or len(pair) != 2:
                raise _WorkerFailure("provider_response_headers_invalid")
            name, item = pair
            if (
                not isinstance(name, str)
                or not isinstance(item, str)
                or not name.isascii()
                or not item.isascii()
                or not _SAFE_HEADER_NAME_RE.fullmatch(name)
                or not _SAFE_HEADER_VALUE_RE.fullmatch(item)
            ):
                raise _WorkerFailure("provider_response_headers_invalid")
            lowered = name.lower()
            total += len(name) + len(item) + 4  # colon, space, and CRLF
            if total > _MAX_HEADER_BYTES:
                raise _WorkerFailure("provider_response_headers_invalid")
            if lowered in _INSPECTED_RESPONSE_HEADERS:
                if lowered in result:
                    raise _WorkerFailure("provider_response_headers_invalid")
                result[lowered] = item
    except _WorkerFailure:
        raise
    except BaseException:
        raise _WorkerFailure("provider_response_headers_invalid") from None
    return result


def _safe_provider_evidence(
    headers: Dict[str, str],
    key: str,
) -> Tuple[Dict[str, str], Dict[str, int]]:
    identifiers: Dict[str, str] = {}
    for name in ("request-id", "x-request-id", "eleven-request-id"):
        value = headers.get(name)
        if (
            isinstance(value, str)
            and _SAFE_PROVIDER_VALUE_RE.fullmatch(value)
            and key not in value
            and not _SECRET_VALUE_RE.search(value)
        ):
            identifiers[name] = value
    usage: Dict[str, int] = {}
    for name in (
        "request-cost",
        "character-count",
        "x-ratelimit-limit",
        "x-ratelimit-remaining",
        "x-ratelimit-reset",
    ):
        value = headers.get(name)
        if (
            isinstance(value, str)
            and value.isascii()
            and value.isdigit()
            and len(value) <= 16
        ):
            number = int(value)
            if 0 <= number <= 10**15:
                usage[name] = number
    return identifiers, usage


def _content_length_state(headers: Dict[str, str], cap: int) -> str:
    declared = headers.get("content-length")
    if declared is None:
        return "absent"
    if (
        not declared.isascii()
        or not declared.isdigit()
        or len(declared) > _CONTENT_LENGTH_MAX_DIGITS
    ):
        return "invalid"
    return "over_cap" if int(declared) > cap else "valid_within_cap"


def _safe_content_type(headers: Dict[str, str]) -> Optional[str]:
    value = headers.get("content-type", "").split(";", 1)[0].strip().lower()
    return value if _SAFE_MIME_RE.fullmatch(value) else None


def _content_encoding_state(headers: Dict[str, str]) -> str:
    value = headers.get("content-encoding", "identity").strip().lower()
    return "identity" if value in {"", "identity"} else "forbidden"


def _phase_request_starting(result_fd: int) -> None:
    value = {
        "application_http_attempts": 1,
        "message": "phase",
        "network_state": "application_request_starting",
        "phase": "request_starting",
        "protocol": PROTOCOL,
        "request_state": "outcome_unknown",
        "response_state": "none",
        "sequence": 1,
    }
    if set(value) != REQUEST_STARTING_PHASE_KEYS:
        raise OSError("request phase shape drifted")
    _write_frame(result_fd, canonical_json_bytes(value), PHASE_FRAME_MAX_BYTES)


def _phase_response_headers(
    result_fd: int,
    status: Optional[int],
    headers: Dict[str, str],
    cap: int,
) -> None:
    value = {
        "application_http_attempts": 1,
        "content_encoding_state": _content_encoding_state(headers),
        "content_length_state": _content_length_state(headers, cap),
        "content_type": _safe_content_type(headers),
        "http_status": status,
        "message": "phase",
        "network_state": "application_request_started",
        "phase": "response_headers_confirmed",
        "protocol": PROTOCOL,
        "request_state": "response_confirmed",
        "response_state": "headers_confirmed",
        "sequence": 2,
    }
    if set(value) != RESPONSE_HEADERS_PHASE_KEYS:
        raise OSError("response phase shape drifted")
    _write_frame(result_fd, canonical_json_bytes(value), PHASE_FRAME_MAX_BYTES)


def _bounded_failure(
    code: str,
    captured: bytearray,
    secret: bytearray,
    *,
    byte_count_state: str,
) -> _WorkerFailure:
    contains_secret = bool(secret) and captured.find(secret) >= 0
    digest = None if contains_secret or not captured else hashlib.sha256(captured).hexdigest()
    return _WorkerFailure(
        "provider_response_contains_credential" if contains_secret else code,
        response_state="body_rejected",
        response_bytes=len(captured),
        response_sha256=digest,
        response_byte_count_state=byte_count_state,
        response_body_disposition=(
            "discarded_credential_echo"
            if contains_secret
            else ("hash_count_only" if captured else "not_read")
        ),
    )


def _read_bounded(
    response: Any,
    headers: Dict[str, str],
    cap: int,
    secret: bytearray,
) -> bytes:
    declared_state = _content_length_state(headers, cap)
    if declared_state == "invalid":
        raise _WorkerFailure("provider_content_length_invalid", response_state="headers_confirmed")
    if declared_state == "over_cap":
        raise _WorkerFailure("provider_response_byte_cap_exceeded", response_state="headers_confirmed")
    captured = bytearray()
    chunk = b""
    try:
        while True:
            # Read at most one byte beyond the retained prefix as an over-cap
            # sentinel, but never retain or hash more than the authorized cap.
            probe_remaining = cap + 1 - len(captured)
            try:
                chunk = response.read(min(65_536, max(1, probe_remaining)))
            except BaseException as error:
                chunk = b""
                raise _bounded_failure(
                    (
                        "provider_post_timeout_ambiguous"
                        if _timeout_like(error)
                        else "provider_transport_failure"
                    ),
                    captured,
                    secret,
                    byte_count_state="bounded_prefix",
                ) from None
            if not isinstance(chunk, bytes):
                chunk = b""
                raise _bounded_failure(
                    "provider_response_stream_invalid",
                    captured,
                    secret,
                    byte_count_state="bounded_prefix",
                )
            if not chunk:
                break
            retained_remaining = max(0, cap - len(captured))
            take = min(len(chunk), retained_remaining)
            if take:
                captured.extend(memoryview(chunk)[:take])
            over_cap_observed = len(chunk) > take
            chunk = b""
            if over_cap_observed:
                raise _bounded_failure(
                    "provider_response_byte_cap_exceeded",
                    captured,
                    secret,
                    byte_count_state="bounded_prefix",
                )
        raw = bytes(captured)
        declared = headers.get("content-length")
        if declared is not None and len(raw) != int(declared):
            failure = _bounded_failure(
                "provider_response_truncated",
                captured,
                secret,
                byte_count_state="exact",
            )
            raw = b""
            raise failure
        return raw
    finally:
        captured.clear()
        chunk = b""


def _augment_response_failure(
    failure: _WorkerFailure,
    *,
    status: Optional[int],
    headers: Dict[str, str],
    key: str,
) -> _WorkerFailure:
    identifiers, usage = _safe_provider_evidence(headers, key)
    failure.application_http_attempts = 1
    failure.network_state = "application_request_started"
    failure.request_state = "response_confirmed"
    if failure.response_state == "none":
        failure.response_state = "headers_confirmed"
    failure.http_status = status if type(status) is int and 100 <= status <= 599 else None
    failure.content_type = _safe_content_type(headers)
    failure.content_encoding = (
        "identity" if _content_encoding_state(headers) == "identity" else "forbidden"
    )
    failure.provider_identifiers = identifiers
    failure.provider_usage = usage
    return failure


def _close_response(response: Any) -> None:
    if response is None:
        return
    try:
        close = getattr(response, "close")
    except BaseException:
        return
    if callable(close):
        try:
            close()
        except BaseException:
            pass


def _timeout_like(error: BaseException) -> bool:
    candidate: Any = error
    seen: Set[int] = set()
    for _ in range(4):
        if id(candidate) in seen:
            break
        seen.add(id(candidate))
        if isinstance(candidate, TimeoutError):
            return True
        if isinstance(candidate, urllib.error.URLError):
            candidate = candidate.reason
            continue
        break
    return False


def _build_exact_opener() -> urllib.request.OpenerDirector:
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
        _NoRedirect(),
    )
    opener.addheaders = []
    return opener


def _perform_exact_request(
    key_bytes: bytearray,
    body: bytearray,
    deadline_ns: int,
    result_fd: int,
) -> Tuple[Dict[str, Any], bytes]:
    if time.monotonic_ns() >= deadline_ns:
        raise _WorkerFailure("worker_deadline_expired_before_request")
    key = ""
    request = None
    opener = None
    response = None
    request_started = False
    headers_confirmed = False
    safe_status: Optional[int] = None
    headers: Dict[str, str] = {}
    try:
        key = key_bytes.decode("ascii", errors="strict")
        request = urllib.request.Request(EXACT_URL, data=body, method=EXACT_METHOD)
        request.add_header("Accept", EXACT_ACCEPT)
        request.add_header("Accept-Encoding", "identity")
        request.add_header("Content-Length", str(EXACT_BODY_BYTES))
        request.add_header("Content-Type", EXACT_CONTENT_TYPE)
        request.add_header("xi-api-key", key)
        opener = _build_exact_opener()
        remaining_seconds = (deadline_ns - time.monotonic_ns()) / 1_000_000_000
        if remaining_seconds <= 0:
            raise _WorkerFailure("worker_deadline_expired_before_request")
        _phase_request_starting(result_fd)
        request_started = True
        try:
            response = opener.open(request, timeout=remaining_seconds)
        except urllib.error.HTTPError as http_error:
            response = http_error
        except BaseException as error:
            code = "provider_post_timeout_ambiguous" if _timeout_like(error) else "provider_transport_failure"
            raise _WorkerFailure(
                code,
                application_http_attempts=1,
                network_state="application_request_started",
                request_state="outcome_unknown",
            ) from None

        status_getter = getattr(response, "getcode", None)
        status = status_getter() if callable(status_getter) else getattr(response, "status", None)
        safe_status = status if type(status) is int and 100 <= status <= 599 else None
        try:
            headers = _strict_headers(getattr(response, "headers", {}))
        except _WorkerFailure as failure:
            failure.application_http_attempts = 1
            failure.network_state = "application_request_started"
            failure.request_state = "response_confirmed"
            failure.response_state = "headers_rejected"
            failure.http_status = safe_status
            raise
        response_cap = RESULT_BODY_MAX_BYTES if safe_status == 200 else ERROR_BODY_MAX_BYTES
        _phase_response_headers(result_fd, safe_status, headers, response_cap)
        headers_confirmed = True
        identifiers, usage = _safe_provider_evidence(headers, key)

        if safe_status is None or safe_status != 200:
            try:
                raw = _read_bounded(response, headers, ERROR_BODY_MAX_BYTES, key_bytes)
            except _WorkerFailure as failure:
                raise _augment_response_failure(
                    failure,
                    status=safe_status,
                    headers=headers,
                    key=key,
                )
            contains_secret = bool(key_bytes) and raw.find(key_bytes) >= 0
            digest = None if contains_secret or not raw else hashlib.sha256(raw).hexdigest()
            raw_length = len(raw)
            raw = b""
            raise _WorkerFailure(
                "provider_response_contains_credential" if contains_secret else (
                    "provider_redirect_forbidden"
                    if safe_status is not None and 300 <= safe_status < 400
                    else "provider_http_failure"
                ),
                application_http_attempts=1,
                network_state="application_request_started",
                request_state="response_confirmed",
                response_state="body_rejected",
                http_status=safe_status,
                response_bytes=raw_length,
                response_sha256=digest,
                response_byte_count_state="exact" if raw_length else "none",
                response_body_disposition=(
                    "discarded_credential_echo"
                    if contains_secret
                    else ("hash_count_only" if raw_length else "not_read")
                ),
                content_type=_safe_content_type(headers),
                content_encoding=(
                    "identity" if _content_encoding_state(headers) == "identity" else "forbidden"
                ),
                provider_identifiers=identifiers,
                provider_usage=usage,
            )

        final_getter = getattr(response, "geturl", None)
        if not callable(final_getter) or final_getter() != EXACT_URL:
            raise _WorkerFailure(
                "provider_redirect_forbidden",
                application_http_attempts=1,
                network_state="application_request_started",
                request_state="response_confirmed",
                response_state="headers_confirmed",
                http_status=safe_status,
                content_type=_safe_content_type(headers),
                content_encoding=(
                    "identity" if _content_encoding_state(headers) == "identity" else "forbidden"
                ),
                provider_identifiers=identifiers,
                provider_usage=usage,
            )
        encoding_state = _content_encoding_state(headers)
        content_type = _safe_content_type(headers)
        if encoding_state != "identity":
            raise _WorkerFailure(
                "provider_response_encoding_forbidden",
                application_http_attempts=1,
                network_state="application_request_started",
                request_state="response_confirmed",
                response_state="headers_confirmed",
                http_status=safe_status,
                content_encoding="forbidden",
                content_type=content_type,
                provider_identifiers=identifiers,
                provider_usage=usage,
            )
        if content_type not in EXPECTED_MIMES:
            raise _WorkerFailure(
                "provider_response_mime_invalid",
                application_http_attempts=1,
                network_state="application_request_started",
                request_state="response_confirmed",
                response_state="headers_confirmed",
                http_status=safe_status,
                content_encoding="identity",
                content_type=content_type,
                provider_identifiers=identifiers,
                provider_usage=usage,
            )
        try:
            raw = _read_bounded(response, headers, RESULT_BODY_MAX_BYTES, key_bytes)
        except _WorkerFailure as failure:
            raise _augment_response_failure(
                failure,
                status=safe_status,
                headers=headers,
                key=key,
            )
        if bool(key_bytes) and raw.find(key_bytes) >= 0:
            raw_length = len(raw)
            raw = b""
            raise _WorkerFailure(
                "provider_response_contains_credential",
                application_http_attempts=1,
                network_state="application_request_started",
                request_state="response_confirmed",
                response_state="body_rejected",
                http_status=safe_status,
                response_bytes=raw_length,
                response_byte_count_state="exact",
                response_body_disposition="discarded_credential_echo",
                content_type=content_type,
                content_encoding="identity",
                provider_identifiers=identifiers,
                provider_usage=usage,
            )
        metadata = _success_metadata(
            status=safe_status,
            raw=raw,
            content_type=content_type,
            identifiers=identifiers,
            usage=usage,
        )
        return metadata, raw
    except _WorkerFailure:
        raise
    except BaseException as error:
        if not request_started:
            raise _WorkerFailure("worker_internal_failure") from None
        identifiers, usage = _safe_provider_evidence(headers, key) if headers_confirmed else ({}, {})
        raise _WorkerFailure(
            (
                "provider_transport_failure"
                if headers_confirmed
                else (
                    "provider_post_timeout_ambiguous"
                    if _timeout_like(error)
                    else "provider_transport_failure"
                )
            ),
            application_http_attempts=1,
            network_state="application_request_started",
            request_state="response_confirmed" if headers_confirmed else "outcome_unknown",
            response_state="headers_confirmed" if headers_confirmed else "none",
            http_status=safe_status,
            content_type=_safe_content_type(headers) if headers_confirmed else None,
            content_encoding=(
                (
                    "identity"
                    if _content_encoding_state(headers) == "identity"
                    else "forbidden"
                )
                if headers_confirmed
                else None
            ),
            provider_identifiers=identifiers,
            provider_usage=usage,
        ) from None
    finally:
        _close_response(response)
        response = None
        request = None
        opener = None
        key = ""


def _success_metadata(
    *,
    status: int,
    raw: bytes,
    content_type: str,
    identifiers: Dict[str, str],
    usage: Dict[str, int],
) -> Dict[str, Any]:
    value = {
        "application_fallbacks_used": 0,
        "application_http_attempts": 1,
        "application_redirects_followed": 0,
        "application_retries_made": 0,
        "content_encoding": "identity",
        "content_type": content_type,
        "failure_code": None,
        "http_status": status,
        "message": "result",
        "network_stack_address_selection_state": NETWORK_STACK_ADDRESS_SELECTION_STATE,
        "network_state": "application_request_started",
        "outcome": "success",
        "protocol": PROTOCOL,
        "provider_identifiers": identifiers,
        "provider_usage": usage,
        "request_state": "response_confirmed",
        "response_body_disposition": "raw_success_frame",
        "response_byte_count_state": "exact",
        "response_bytes": len(raw),
        "response_sha256": hashlib.sha256(raw).hexdigest(),
        "response_state": "body_complete",
        "success_body_follows": True,
    }
    if set(value) != RESULT_KEYS:
        raise _WorkerFailure("worker_internal_failure")
    return value


def _failure_metadata(failure: _WorkerFailure) -> Dict[str, Any]:
    value = {
        "application_fallbacks_used": 0,
        "application_http_attempts": failure.application_http_attempts,
        "application_redirects_followed": 0,
        "application_retries_made": 0,
        "content_encoding": failure.content_encoding,
        "content_type": failure.content_type,
        "failure_code": failure.code,
        "http_status": failure.http_status,
        "message": "result",
        "network_stack_address_selection_state": NETWORK_STACK_ADDRESS_SELECTION_STATE,
        "network_state": failure.network_state,
        "outcome": "failure",
        "protocol": PROTOCOL,
        "provider_identifiers": failure.provider_identifiers,
        "provider_usage": failure.provider_usage,
        "request_state": failure.request_state,
        "response_body_disposition": failure.response_body_disposition,
        "response_byte_count_state": failure.response_byte_count_state,
        "response_bytes": failure.response_bytes,
        "response_sha256": failure.response_sha256,
        "response_state": failure.response_state,
        "success_body_follows": False,
    }
    if set(value) != RESULT_KEYS:
        raise _WorkerFailure("worker_internal_failure")
    return value


def _parse_fd_value(value: str) -> int:
    if not value.isascii() or not value.isdigit():
        raise ValueError("invalid worker descriptor")
    descriptor = int(value)
    if str(descriptor) != value or descriptor < 3:
        raise ValueError("invalid worker descriptor")
    return descriptor


def _parse_fd_args(arguments: List[str]) -> Tuple[int, int, int, int]:
    if (
        len(arguments) != 8
        or arguments[0] != "--command-fd"
        or arguments[2] != "--key-fd"
        or arguments[4] != "--body-fd"
        or arguments[6] != "--result-fd"
    ):
        raise ValueError("invalid worker invocation")
    values = tuple(_parse_fd_value(arguments[index]) for index in (1, 3, 5, 7))
    if len(set(values)) != 4:
        raise ValueError("worker descriptors are not distinct")
    return values  # type: ignore[return-value]


def _run(command_fd: int, key_fd: int, body_fd: int, result_fd: int) -> int:
    pid = os.getpid()
    parent_pid = os.getppid()
    if parent_pid <= 1 or os.getpgrp() != pid or os.getsid(0) != pid:
        raise OSError("worker does not own its process group and session")
    core_limits = _disable_core_dumps()
    safe_environment = _preflight_environment()
    _preflight_descriptors(command_fd, key_fd, body_fd, result_fd)
    watchdog = _SelfDestructDeadline(parent_pid)
    watchdog.start()
    _write_frame(
        result_fd,
        _ready_payload(parent_pid, safe_environment, core_limits),
        READY_FRAME_MAX_BYTES,
    )

    key_bytes = bytearray()
    body = bytearray()
    result_body = b""
    metadata: Dict[str, Any] = {}
    try:
        command_payload = _read_single_frame(
            command_fd,
            COMMAND_FRAME_MAX_BYTES,
            "worker_command_invalid",
            "worker_command_trailing_data",
        )
        try:
            deadline_ns = _parse_command(bytes(command_payload), watchdog)
        finally:
            command_payload.clear()
        key_bytes = _parse_key(
            _read_single_frame(
                key_fd,
                KEY_FRAME_MAX_BYTES,
                "worker_key_invalid",
                "worker_key_trailing_data",
            )
        )
        body = _read_single_frame(
            body_fd,
            BODY_FRAME_MAX_BYTES,
            "worker_body_invalid",
            "worker_body_trailing_data",
        )
        if len(body) != EXACT_BODY_BYTES or hashlib.sha256(body).hexdigest() != EXACT_BODY_SHA256:
            raise _WorkerFailure("compiled_request_body_binding_failed")
        if time.monotonic_ns() >= deadline_ns:
            raise _WorkerFailure("worker_deadline_expired_before_request")
        metadata, result_body = _perform_exact_request(
            key_bytes,
            body,
            deadline_ns,
            result_fd,
        )
    except _WorkerFailure as failure:
        failure.__cause__ = None
        failure.__context__ = None
        failure.__suppress_context__ = True
        failure.__traceback__ = None
        metadata = _failure_metadata(failure)
        result_body = b""
        failure = None  # type: ignore[assignment]
    except BaseException:
        metadata = _failure_metadata(_WorkerFailure("worker_internal_failure"))
        result_body = b""
    finally:
        key_bytes[:] = b"\x00" * len(key_bytes)
        key_bytes.clear()
        body[:] = b"\x00" * len(body)
        body.clear()

    result_payload = canonical_json_bytes(metadata)
    _write_frame(result_fd, result_payload, RESULT_FRAME_MAX_BYTES)
    if metadata.get("success_body_follows") is True:
        _write_frame(result_fd, result_body, RESULT_BODY_MAX_BYTES)
    result_body = b""
    metadata = {}
    result_payload = b""
    os.close(result_fd)
    watchdog.stop()
    return 0


def main(arguments: Optional[List[str]] = None) -> int:
    try:
        values = _parse_fd_args(list(sys.argv[1:] if arguments is None else arguments))
        return _run(*values)
    except BaseException:
        return 125


if __name__ == "__main__":
    raise SystemExit(main())
