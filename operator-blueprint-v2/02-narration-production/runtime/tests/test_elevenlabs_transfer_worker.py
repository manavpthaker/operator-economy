from __future__ import annotations

import ast
import fcntl
import hashlib
import json
import os
import re
import select
import signal
import stat
import struct
import subprocess
import sys
import time
import unittest
import urllib.error
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Dict, List, Optional, Sequence, Tuple
from unittest import mock

from oe_narration import elevenlabs_transfer_worker as worker


RUNTIME_ROOT = Path(__file__).resolve().parents[1]
WORKER_PATH = RUNTIME_ROOT / "oe_narration" / "elevenlabs_transfer_worker.py"
BOUND_PYTHON = Path(
    "/Library/Developer/CommandLineTools/Library/Frameworks/"
    "Python3.framework/Versions/3.9/bin/python3.9"
)
BOUND_PYTHON_SHA256 = (
    "8e598855de9a6648bc670d5fe7a3a653f1fa967b74373ed7c4ca16fbc40c0de1"
)


BOOTSTRAP = """\
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


def _source_bytes() -> bytes:
    return WORKER_PATH.read_bytes()


def _source_sha256() -> str:
    return hashlib.sha256(_source_bytes()).hexdigest()


def _frame(payload: bytes) -> bytes:
    return worker.FRAME_LENGTH_STRUCT.pack(len(payload)) + payload


def _write_all(descriptor: int, payload: bytes) -> None:
    offset = 0
    while offset < len(payload):
        written = os.write(descriptor, payload[offset:])
        if written <= 0:
            raise OSError("test pipe closed")
        offset += written


def _read_exact(descriptor: int, size: int, timeout: float = 5.0) -> bytes:
    deadline = time.monotonic() + timeout
    value = bytearray()
    while len(value) < size:
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise TimeoutError("test frame read timed out")
        readable, _, _ = select.select([descriptor], [], [], remaining)
        if not readable:
            raise TimeoutError("test frame read timed out")
        chunk = os.read(descriptor, size - len(value))
        if not chunk:
            raise EOFError("test frame ended early")
        value.extend(chunk)
    return bytes(value)


def _read_frame(descriptor: int, timeout: float = 5.0) -> bytes:
    prefix = _read_exact(descriptor, worker.FRAME_LENGTH_STRUCT.size, timeout)
    size = worker.FRAME_LENGTH_STRUCT.unpack(prefix)[0]
    return _read_exact(descriptor, size, timeout)


def _decode_frames(payload: bytes) -> List[bytes]:
    frames: List[bytes] = []
    offset = 0
    while offset < len(payload):
        if len(payload) - offset < worker.FRAME_LENGTH_STRUCT.size:
            raise AssertionError("truncated test frame prefix")
        size = worker.FRAME_LENGTH_STRUCT.unpack_from(payload, offset)[0]
        offset += worker.FRAME_LENGTH_STRUCT.size
        end = offset + size
        if end > len(payload):
            raise AssertionError("truncated test frame")
        frames.append(payload[offset:end])
        offset = end
    return frames


def _drain(descriptor: int) -> bytes:
    value = bytearray()
    while True:
        chunk = os.read(descriptor, 65_536)
        if not chunk:
            return bytes(value)
        value.extend(chunk)


def _local_open_fds() -> set:
    directory_fd = os.open("/dev/fd", os.O_RDONLY)
    try:
        names = os.listdir(directory_fd)
    finally:
        os.close(directory_fd)
    result = set()
    for name in names:
        if isinstance(name, str) and name.isdigit():
            descriptor = int(name)
            try:
                os.fstat(descriptor)
            except OSError:
                continue
            result.add(descriptor)
    result.discard(directory_fd)
    return result


class _WorkerProcess:
    def __init__(
        self,
        *,
        start_new_session: bool = True,
        extra_pass_fds: Sequence[int] = (),
    ) -> None:
        if not BOUND_PYTHON.is_file():
            raise unittest.SkipTest("bound Python 3.9 interpreter is unavailable")
        source_fd = os.open(str(WORKER_PATH), os.O_RDONLY)
        command_read, self.command_write = os.pipe()
        key_read, self.key_write = os.pipe()
        body_read, self.body_write = os.pipe()
        self.result_read, result_write = os.pipe()
        self.start_new_session = start_new_session
        child_descriptors = (source_fd, command_read, key_read, body_read, result_write)
        self.child_ipc_fds = (command_read, key_read, body_read, result_write)
        argv = [
            str(BOUND_PYTHON),
            "-I",
            "-S",
            "-B",
            "-c",
            BOOTSTRAP,
            str(source_fd),
            str(WORKER_PATH),
            _source_sha256(),
            "--command-fd",
            str(command_read),
            "--key-fd",
            str(key_read),
            "--body-fd",
            str(body_read),
            "--result-fd",
            str(result_write),
        ]
        try:
            self.process = subprocess.Popen(
                argv,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                env=dict(worker.SPAWN_ENVIRONMENT),
                close_fds=True,
                pass_fds=tuple(child_descriptors) + tuple(extra_pass_fds),
                start_new_session=start_new_session,
            )
        finally:
            for descriptor in child_descriptors:
                os.close(descriptor)

    def read_json(self, timeout: float = 5.0) -> Dict[str, Any]:
        return json.loads(_read_frame(self.result_read, timeout).decode("ascii"))

    def send_command_payload(self, payload: bytes) -> None:
        _write_all(self.command_write, _frame(payload))
        os.close(self.command_write)
        self.command_write = -1

    def send_key_payload(self, payload: bytes) -> None:
        _write_all(self.key_write, _frame(payload))
        os.close(self.key_write)
        self.key_write = -1

    def send_body_payload(self, payload: bytes) -> None:
        _write_all(self.body_write, _frame(payload))
        os.close(self.body_write)
        self.body_write = -1

    def finish_with_invalid_command(self) -> Dict[str, Any]:
        self.send_command_payload(b"{}")
        result = self.read_json()
        self.process.wait(timeout=5.0)
        return result

    def close(self) -> None:
        for name in ("command_write", "key_write", "body_write", "result_read"):
            descriptor = getattr(self, name, -1)
            if descriptor >= 0:
                try:
                    os.close(descriptor)
                except OSError:
                    pass
                setattr(self, name, -1)
        if self.process.poll() is None:
            try:
                if self.start_new_session:
                    os.killpg(self.process.pid, signal.SIGKILL)
                else:
                    self.process.kill()
            except ProcessLookupError:
                pass
            self.process.wait(timeout=5.0)


class _Headers:
    def __init__(self, pairs: Sequence[Tuple[str, str]]) -> None:
        self._pairs = list(pairs)

    def raw_items(self) -> List[Tuple[str, str]]:
        return list(self._pairs)


class _Response:
    def __init__(
        self,
        *,
        status: int = 200,
        url: str = worker.EXACT_URL,
        headers: Optional[Sequence[Tuple[str, str]]] = None,
        data: bytes = b"result",
        events: Optional[Sequence[Any]] = None,
    ) -> None:
        self.status = status
        self.url = url
        self.headers = _Headers(
            headers
            if headers is not None
            else [
                ("Content-Type", "audio/pcm"),
                ("Content-Encoding", "identity"),
                ("Content-Length", str(len(data))),
            ]
        )
        self.data = data
        self.offset = 0
        self.events = list(events) if events is not None else None
        self.closed = False

    def getcode(self) -> int:
        return self.status

    def geturl(self) -> str:
        return self.url

    def read(self, size: int = -1) -> bytes:
        if self.events is not None:
            if not self.events:
                return b""
            event = self.events.pop(0)
            if isinstance(event, BaseException):
                raise event
            return event
        if size < 0:
            size = len(self.data) - self.offset
        value = self.data[self.offset : self.offset + size]
        self.offset += len(value)
        return value

    def close(self) -> None:
        self.closed = True


class _Opener:
    def __init__(self, value: Any) -> None:
        self.value = value
        self.requests: List[Tuple[Any, float]] = []

    def open(self, request: Any, timeout: float) -> Any:
        self.requests.append((request, timeout))
        if isinstance(self.value, BaseException):
            raise self.value
        return self.value


def _call_transport(
    opener: _Opener,
    *,
    key: bytes = b"TEST_CREDENTIAL_VALUE_123456",
) -> Tuple[Optional[Dict[str, Any]], bytes, Optional[worker._WorkerFailure], List[Dict[str, Any]]]:
    result_read, result_write = os.pipe()
    metadata: Optional[Dict[str, Any]] = None
    raw = b""
    failure: Optional[worker._WorkerFailure] = None
    try:
        with mock.patch.object(worker, "_build_exact_opener", return_value=opener):
            try:
                metadata, raw = worker._perform_exact_request(
                    bytearray(key),
                    bytearray(b"test-body"),
                    time.monotonic_ns() + 5_000_000_000,
                    result_write,
                )
            except worker._WorkerFailure as error:
                failure = error
    finally:
        os.close(result_write)
    phases = [json.loads(value.decode("ascii")) for value in _decode_frames(_drain(result_read))]
    os.close(result_read)
    return metadata, raw, failure, phases


class ElevenLabsTransferWorkerTests(unittest.TestCase):
    def test_protocol_contract_is_exact_and_python39_parseable(self) -> None:
        self.assertEqual(worker.PROTOCOL, "oe-elevenlabs-exact-transfer-worker-v1")
        self.assertEqual(worker.FRAME_LENGTH_STRUCT.format, "!I")
        self.assertEqual(worker.EXACT_METHOD, "POST")
        self.assertEqual(
            worker.EXACT_URL,
            "https://api.elevenlabs.io/v1/speech-to-speech/"
            "scMbPZwQjr40V1MzL3Nj?enable_logging=true&output_format=pcm_48000",
        )
        self.assertEqual(worker.EXACT_BODY_BYTES, 1_646_839)
        self.assertEqual(
            worker.EXACT_BODY_SHA256,
            "6b57da1e6d1dc62b8ec31d34b6629da087be15f51b59998a83109f25403931dc",
        )
        self.assertEqual(worker.RESULT_BODY_MAX_BYTES, 4_800_000)
        self.assertEqual(worker.ERROR_BODY_MAX_BYTES, 65_536)
        self.assertIn("child_deadline_monotonic_ns", worker.COMMAND_KEYS)
        self.assertNotIn("deadline_monotonic_ns", worker.COMMAND_KEYS)
        self.assertIn("provider_post_timeout_ambiguous", worker.ALLOWED_FAILURE_CODES)
        if not BOUND_PYTHON.is_file():
            self.skipTest("bound Python 3.9 interpreter is unavailable")
        completed = subprocess.run(
            [
                str(BOUND_PYTHON),
                "-I",
                "-S",
                "-B",
                "-c",
                "import pathlib; compile(pathlib.Path(__import__('sys').argv[1]).read_bytes(), __import__('sys').argv[1], 'exec', dont_inherit=True)",
                str(WORKER_PATH),
            ],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=dict(worker.SPAWN_ENVIRONMENT),
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr.decode("utf-8", "replace"))

    def test_imported_source_has_no_process_or_shell_escape(self) -> None:
        source = _source_bytes().decode("utf-8")
        tree = ast.parse(source, str(WORKER_PATH))
        forbidden_imports = {"subprocess", "multiprocessing", "pty"}
        forbidden_calls = {
            "fork",
            "forkpty",
            "popen",
            "system",
            "execv",
            "execve",
            "execvp",
            "execvpe",
            "spawnl",
            "spawnle",
            "spawnlp",
            "spawnlpe",
            "spawnv",
            "spawnve",
            "spawnvp",
            "spawnvpe",
        }
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                self.assertFalse({item.name.split(".", 1)[0] for item in node.names} & forbidden_imports)
            elif isinstance(node, ast.ImportFrom):
                self.assertNotIn((node.module or "").split(".", 1)[0], forbidden_imports)
            elif isinstance(node, ast.Call):
                name = getattr(node.func, "attr", getattr(node.func, "id", ""))
                self.assertNotIn(name, forbidden_calls)
        run_function = next(
            node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "_run"
        )
        calls = [
            getattr(node.func, "id", getattr(node.func, "attr", ""))
            for node in ast.walk(run_function)
            if isinstance(node, ast.Call)
        ]
        self.assertIn("_read_single_frame", calls)
        self.assertIn("_perform_exact_request", calls)

    def test_ready_is_descriptor_bound_and_worker_holds_before_go(self) -> None:
        process = _WorkerProcess()
        self.addCleanup(process.close)
        ready = process.read_json()
        self.assertEqual(set(ready), worker.READY_KEYS)
        self.assertEqual(ready["message"], "ready")
        self.assertEqual(ready["executed_source_sha256"], _source_sha256())
        self.assertEqual(ready["logical_source_path"], str(WORKER_PATH))
        self.assertEqual(ready["interpreter_path"], str(BOUND_PYTHON))
        self.assertEqual(ready["interpreter_sha256"], BOUND_PYTHON_SHA256)
        self.assertEqual(ready["interpreter_mode"], 0o755)
        self.assertEqual(ready["interpreter_uid"], 0)
        self.assertEqual(ready["interpreter_nlink"], 1)
        safe_environment = dict(worker.SPAWN_ENVIRONMENT)
        safe_environment["__CF_USER_TEXT_ENCODING"] = "0x{:X}:0x0:0x0".format(os.getuid())
        self.assertEqual(ready["environment_keys"], sorted(safe_environment))
        self.assertEqual(
            ready["environment_sha256"],
            hashlib.sha256(worker.canonical_json_bytes(safe_environment)).hexdigest(),
        )
        self.assertEqual(ready["core_soft_limit"], 0)
        self.assertEqual(ready["core_hard_limit"], 0)
        self.assertIs(type(ready["monotonic_ns_at_ready"]), int)
        self.assertGreater(ready["monotonic_ns_at_ready"], 0)
        self.assertEqual(ready["pid"], ready["process_group_id"])
        self.assertEqual(ready["pid"], ready["session_id"])
        self.assertFalse(ready["network_called"])
        self.assertFalse(ready["command_received"])
        self.assertEqual(ready["credential_bytes_read"], 0)
        self.assertEqual(ready["body_bytes_read"], 0)
        time.sleep(0.1)
        self.assertIsNone(process.process.poll())
        result = process.finish_with_invalid_command()
        self.assertEqual(result["failure_code"], "worker_command_invalid")
        self.assertEqual(result["application_http_attempts"], 0)
        self.assertEqual(result["network_state"], "not_started")
        self.assertEqual(process.process.returncode, 0)

    def test_worker_refuses_to_arm_without_own_session(self) -> None:
        process = _WorkerProcess(start_new_session=False)
        self.addCleanup(process.close)
        process.process.wait(timeout=5.0)
        self.assertEqual(process.process.returncode, 125)
        with self.assertRaises(EOFError):
            _read_frame(process.result_read, 0.5)

    def test_unintended_inherited_fd_is_closed_before_ready(self) -> None:
        extra_read, extra_write = os.pipe()
        process = _WorkerProcess(extra_pass_fds=(extra_read,))
        os.close(extra_read)
        self.addCleanup(process.close)
        self.addCleanup(lambda: os.close(extra_write) if extra_write >= 0 else None)
        ready = process.read_json()
        self.assertEqual(ready["message"], "ready")
        with self.assertRaises(BrokenPipeError):
            os.write(extra_write, b"x")
        os.close(extra_write)
        extra_write = -1
        result = process.finish_with_invalid_command()
        self.assertEqual(result["failure_code"], "worker_command_invalid")

    def test_ipc_descriptors_are_marked_close_on_exec(self) -> None:
        pipes = [os.pipe() for _ in range(4)]
        descriptors = [pipes[0][0], pipes[1][0], pipes[2][0], pipes[3][1]]
        self.addCleanup(lambda: [os.close(fd) for pair in pipes for fd in pair])
        original = fcntl.fcntl
        with (
            mock.patch.object(worker, "_close_unintended_descriptors"),
            mock.patch.object(worker, "_require_devnull"),
            mock.patch.object(worker.fcntl, "fcntl", wraps=original) as wrapped,
        ):
            worker._preflight_descriptors(*descriptors)
        setfd_calls = [
            call
            for call in wrapped.call_args_list
            if len(call.args) >= 2 and call.args[1] == fcntl.F_SETFD
        ]
        self.assertEqual({call.args[0] for call in setfd_calls}, set(descriptors))
        for descriptor in descriptors:
            self.assertTrue(original(descriptor, fcntl.F_GETFD) & fcntl.FD_CLOEXEC)

    def test_environment_accepts_only_exact_optional_platform_value(self) -> None:
        flags = SimpleNamespace(
            isolated=1,
            no_site=1,
            dont_write_bytecode=1,
            ignore_environment=1,
            safe_path=True,
        )
        exact_cf = "0x{:X}:0x0:0x0".format(os.getuid())
        with mock.patch.object(worker.sys, "flags", flags):
            with mock.patch.dict(os.environ, dict(worker.SPAWN_ENVIRONMENT), clear=True):
                worker._preflight_environment()
            allowed = dict(worker.SPAWN_ENVIRONMENT)
            allowed["__CF_USER_TEXT_ENCODING"] = exact_cf
            with mock.patch.dict(os.environ, allowed, clear=True):
                worker._preflight_environment()
            wrong = dict(worker.SPAWN_ENVIRONMENT)
            wrong["__CF_USER_TEXT_ENCODING"] = "0xDEAD:0x0:0x0"
            with mock.patch.dict(os.environ, wrong, clear=True):
                with self.assertRaises(OSError):
                    worker._preflight_environment()

    def test_strict_json_rejects_duplicates_nonfinite_and_noncanonical(self) -> None:
        for payload in (
            b'{"action":1,"action":2}',
            b'{"value":NaN}',
            b'{"value":Infinity}',
            b'{"value":1 }',
            b'\xff',
        ):
            with self.subTest(payload=payload):
                with self.assertRaises(worker._WorkerFailure) as raised:
                    worker._strict_json(payload, worker.COMMAND_KEYS)
                self.assertEqual(raised.exception.code, "worker_command_invalid")

    def test_single_frame_rejects_oversize_trailing_and_truncation(self) -> None:
        cases = [
            (struct.pack("!I", 11), 10, "worker_command_invalid"),
            (_frame(b"ok") + b"x", 10, "worker_command_trailing_data"),
            (struct.pack("!I", 4) + b"no", 10, "worker_command_invalid"),
        ]
        for payload, cap, expected in cases:
            with self.subTest(expected=expected):
                read_fd, write_fd = os.pipe()
                _write_all(write_fd, payload)
                os.close(write_fd)
                try:
                    with self.assertRaises(worker._WorkerFailure) as raised:
                        worker._read_single_frame(
                            read_fd,
                            cap,
                            "worker_command_invalid",
                            "worker_command_trailing_data",
                        )
                    self.assertEqual(raised.exception.code, expected)
                finally:
                    os.close(read_fd)

    def test_invalid_command_is_one_shot_and_emits_no_phase(self) -> None:
        process = _WorkerProcess()
        self.addCleanup(process.close)
        self.assertEqual(process.read_json()["message"], "ready")
        result = process.finish_with_invalid_command()
        self.assertEqual(result["message"], "result")
        self.assertEqual(result["failure_code"], "worker_command_invalid")
        self.assertFalse(result["success_body_follows"])
        with self.assertRaises(EOFError):
            _read_frame(process.result_read, 0.5)
        self.assertEqual(process.process.returncode, 0)

    def test_valid_go_and_key_remain_anonymous_while_body_is_withheld(self) -> None:
        secret = b"LIVE_ANONYMOUS_FD_CREDENTIAL_123456"
        withheld_body = b"invalid-bound-body"
        baseline_fds = _local_open_fds()
        process = _WorkerProcess()
        self.addCleanup(process.close)
        ready = process.read_json()
        self.assertEqual(ready["message"], "ready")
        command = {
            "action": "release_exact_transfer",
            "application_http_attempt_limit": 1,
            "body_bytes": worker.EXACT_BODY_BYTES,
            "body_sha256": worker.EXACT_BODY_SHA256,
            "child_deadline_monotonic_ns": (
                ready["monotonic_ns_at_ready"] + 20_000_000_000
            ),
            "protocol": worker.PROTOCOL,
        }
        process.send_command_payload(worker.canonical_json_bytes(command))
        process.send_key_payload(secret)
        time.sleep(0.1)
        self.assertIsNone(process.process.poll())
        readable, _, _ = select.select([process.result_read], [], [], 0)
        self.assertEqual(readable, [])

        argv = subprocess.check_output(
            ["/bin/ps", "-p", str(process.process.pid), "-ww", "-o", "command="],
            stdin=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        self.assertNotIn(secret, argv)
        self.assertNotIn(withheld_body, argv)
        self.assertNotIn(b"ELEVENLABS_API_KEY", argv)

        lsof_output = subprocess.check_output(
            [
                "/usr/sbin/lsof",
                "-a",
                "-p",
                str(process.process.pid),
                "-d",
                "0-999",
                "-Fn",
            ],
            stdin=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        self.assertNotIn(secret, lsof_output)
        self.assertNotIn(withheld_body, lsof_output)
        records: Dict[int, bytes] = {}
        current_fd: Optional[int] = None
        for line in lsof_output.splitlines():
            match = re.fullmatch(br"f([0-9]+)", line)
            if match:
                current_fd = int(match.group(1))
            elif line.startswith(b"n") and current_fd is not None:
                records[current_fd] = line[1:]
                current_fd = None
        self.assertEqual(set(records), {0, 1, 2, *process.child_ipc_fds})
        self.assertEqual(records[0], b"/dev/null")
        self.assertEqual(records[1], b"/dev/null")
        self.assertEqual(records[2], b"/dev/null")
        for descriptor in process.child_ipc_fds:
            # macOS lsof reports EOF-side anonymous pipes with an empty name;
            # live peer sides use the kernel arrow identity.
            self.assertTrue(
                records[descriptor] == b"" or records[descriptor].startswith(b"->"),
                records[descriptor],
            )
        self.assertFalse(any(b".env" in target.lower() for target in records.values()))

        process.send_body_payload(withheld_body)
        result_payload = _read_frame(process.result_read)
        self.assertNotIn(secret, result_payload)
        result = json.loads(result_payload.decode("ascii"))
        self.assertEqual(result["failure_code"], "compiled_request_body_binding_failed")
        self.assertEqual(result["application_http_attempts"], 0)
        self.assertEqual(result["network_state"], "not_started")
        self.assertEqual(result["response_state"], "none")
        process.process.wait(timeout=5.0)
        self.assertEqual(process.process.returncode, 0)
        with self.assertRaises(EOFError):
            _read_frame(process.result_read, 0.5)
        child_pid = process.process.pid
        process.close()
        with self.assertRaises(ProcessLookupError):
            os.kill(child_pid, 0)
        self.assertEqual(_local_open_fds(), baseline_fds)

    def test_child_clock_deadline_expires_within_mapped_parent_cap(self) -> None:
        process = _WorkerProcess()
        self.addCleanup(process.close)
        ready = process.read_json()
        parent_ready_received_ns = time.monotonic_ns()
        child_ready_ns = ready["monotonic_ns_at_ready"]
        if Path(sys.executable).resolve() != BOUND_PYTHON.resolve():
            # Homebrew 3.14 and the bound CLT 3.9 use materially different
            # monotonic epochs on this macOS boundary. The protocol must map
            # a remaining interval, never forward the parent's absolute value.
            self.assertGreater(
                abs(parent_ready_received_ns - child_ready_ns),
                int(worker.MAX_TRANSACTION_SECONDS * 1_000_000_000),
            )
        mapped_interval_ns = 250_000_000
        command = {
            "action": "release_exact_transfer",
            "application_http_attempt_limit": 1,
            "body_bytes": worker.EXACT_BODY_BYTES,
            "body_sha256": worker.EXACT_BODY_SHA256,
            "child_deadline_monotonic_ns": child_ready_ns + mapped_interval_ns,
            "protocol": worker.PROTOCOL,
        }
        started = time.monotonic()
        process.send_command_payload(worker.canonical_json_bytes(command))
        process.send_key_payload(b"MAPPED_DEADLINE_TEST_CREDENTIAL")
        with self.assertRaises(EOFError):
            _read_frame(process.result_read, 1.0)
        elapsed = time.monotonic() - started
        process.process.wait(timeout=2.0)
        self.assertEqual(process.process.returncode, -signal.SIGKILL)
        self.assertGreater(elapsed, 0.02)
        self.assertLess(elapsed, 0.75)

    def test_irrelevant_duplicate_headers_are_ignored(self) -> None:
        headers = worker._strict_headers(
            _Headers(
                [
                    ("Content-Type", "audio/pcm"),
                    ("Set-Cookie", "a=1"),
                    ("set-cookie", "b=2"),
                    ("Vary", "Accept"),
                    ("vary", "Origin"),
                ]
            )
        )
        self.assertEqual(headers, {"content-type": "audio/pcm"})

    def test_duplicate_inspected_headers_are_rejected(self) -> None:
        for name in sorted(worker._INSPECTED_RESPONSE_HEADERS):
            with self.subTest(name=name):
                with self.assertRaises(worker._WorkerFailure) as raised:
                    worker._strict_headers(_Headers([(name, "1"), (name.upper(), "1")]))
                self.assertEqual(raised.exception.code, "provider_response_headers_invalid")

    def test_header_iteration_stops_at_count_cap(self) -> None:
        observed = {"count": 0}

        class EndlessHeaders:
            def raw_items(self) -> Any:
                while True:
                    observed["count"] += 1
                    yield ("Set-Cookie", "a=1")

        with self.assertRaises(worker._WorkerFailure) as raised:
            worker._strict_headers(EndlessHeaders())
        self.assertEqual(raised.exception.code, "provider_response_headers_invalid")
        self.assertEqual(observed["count"], worker._MAX_HEADER_COUNT + 1)

    def test_content_length_digit_bomb_is_rejected_without_integer_conversion(self) -> None:
        self.assertEqual(
            worker._content_length_state({"content-length": "9" * 5000}, 65_536),
            "invalid",
        )

    def test_exact_request_headers_body_and_success_result(self) -> None:
        response = _Response(data=b"audio")
        opener = _Opener(response)
        metadata, raw, failure, phases = _call_transport(opener)
        self.assertIsNone(failure)
        self.assertEqual(raw, b"audio")
        self.assertTrue(response.closed)
        self.assertIsNotNone(metadata)
        assert metadata is not None
        self.assertEqual(metadata["outcome"], "success")
        self.assertEqual(metadata["application_http_attempts"], 1)
        self.assertEqual(metadata["application_retries_made"], 0)
        self.assertEqual(metadata["application_redirects_followed"], 0)
        self.assertEqual(metadata["application_fallbacks_used"], 0)
        self.assertEqual(metadata["response_state"], "body_complete")
        self.assertEqual([phase["phase"] for phase in phases], ["request_starting", "response_headers_confirmed"])
        self.assertEqual(len(opener.requests), 1)
        request, timeout = opener.requests[0]
        self.assertEqual(request.get_method(), "POST")
        self.assertEqual(request.full_url, worker.EXACT_URL)
        self.assertEqual(request.get_header("Accept"), worker.EXACT_ACCEPT)
        self.assertEqual(request.get_header("Accept-encoding"), "identity")
        self.assertEqual(request.get_header("Content-length"), str(worker.EXACT_BODY_BYTES))
        self.assertEqual(request.get_header("Content-type"), worker.EXACT_CONTENT_TYPE)
        self.assertEqual(request.get_header("Xi-api-key"), "TEST_CREDENTIAL_VALUE_123456")
        self.assertEqual(bytes(request.data), b"test-body")
        self.assertGreater(timeout, 0)
        self.assertLessEqual(timeout, 5.0)

    def test_strict_header_failure_records_confirmed_response_without_raw_headers(self) -> None:
        response = _Response(
            status=200,
            headers=[("Content-Type", "audio/pcm"), ("content-type", "audio/mpeg")],
        )
        metadata, raw, failure, phases = _call_transport(_Opener(response))
        self.assertIsNone(metadata)
        self.assertEqual(raw, b"")
        self.assertIsNotNone(failure)
        assert failure is not None
        self.assertEqual(failure.code, "provider_response_headers_invalid")
        self.assertEqual(failure.application_http_attempts, 1)
        self.assertEqual(failure.request_state, "response_confirmed")
        self.assertEqual(failure.response_state, "headers_rejected")
        self.assertEqual(failure.http_status, 200)
        self.assertEqual([phase["phase"] for phase in phases], ["request_starting"])
        self.assertTrue(response.closed)

    def test_open_timeout_is_ambiguous_and_redacted(self) -> None:
        private = "PRIVATE_EXCEPTION_SENTINEL"
        metadata, raw, failure, phases = _call_transport(
            _Opener(urllib.error.URLError(TimeoutError(private)))
        )
        self.assertIsNone(metadata)
        self.assertEqual(raw, b"")
        self.assertIsNotNone(failure)
        assert failure is not None
        self.assertEqual(failure.code, "provider_post_timeout_ambiguous")
        self.assertEqual(failure.application_http_attempts, 1)
        self.assertEqual(failure.request_state, "outcome_unknown")
        self.assertEqual(failure.response_state, "none")
        self.assertEqual([phase["phase"] for phase in phases], ["request_starting"])
        self.assertNotIn(private, json.dumps(worker._failure_metadata(failure)))

    def test_generic_open_exception_is_fixed_and_redacted(self) -> None:
        private = "PRIVATE_EXCEPTION_SENTINEL"
        _, _, failure, phases = _call_transport(_Opener(RuntimeError(private)))
        self.assertIsNotNone(failure)
        assert failure is not None
        self.assertEqual(failure.code, "provider_transport_failure")
        self.assertEqual(failure.application_http_attempts, 1)
        self.assertEqual(failure.request_state, "outcome_unknown")
        self.assertEqual([phase["phase"] for phase in phases], ["request_starting"])
        self.assertNotIn(private, json.dumps(worker._failure_metadata(failure)))

    def test_body_timeout_preserves_ambiguous_code_and_bounded_prefix(self) -> None:
        response = _Response(
            headers=[("Content-Type", "audio/pcm"), ("Content-Encoding", "identity")],
            events=[b"abc", TimeoutError("PRIVATE_BODY_TIMEOUT")],
        )
        _, _, failure, phases = _call_transport(_Opener(response))
        self.assertIsNotNone(failure)
        assert failure is not None
        self.assertEqual(failure.code, "provider_post_timeout_ambiguous")
        self.assertEqual(failure.application_http_attempts, 1)
        self.assertEqual(failure.request_state, "response_confirmed")
        self.assertEqual(failure.response_state, "body_rejected")
        self.assertEqual(failure.response_bytes, 3)
        self.assertEqual(failure.response_byte_count_state, "bounded_prefix")
        self.assertEqual([phase["phase"] for phase in phases], ["request_starting", "response_headers_confirmed"])
        self.assertTrue(response.closed)
        self.assertNotIn("PRIVATE_BODY_TIMEOUT", json.dumps(worker._failure_metadata(failure)))

    def test_generic_body_read_exception_remains_post_attempt(self) -> None:
        response = _Response(
            headers=[("Content-Type", "audio/pcm"), ("Content-Encoding", "identity")],
            events=[RuntimeError("PRIVATE_READ_SENTINEL")],
        )
        _, _, failure, _ = _call_transport(_Opener(response))
        self.assertIsNotNone(failure)
        assert failure is not None
        self.assertEqual(failure.code, "provider_transport_failure")
        self.assertEqual(failure.application_http_attempts, 1)
        self.assertEqual(failure.request_state, "response_confirmed")
        self.assertEqual(failure.response_state, "body_rejected")
        self.assertEqual(failure.response_byte_count_state, "bounded_prefix")
        self.assertTrue(response.closed)

    def test_nonbyte_body_chunk_records_only_a_bounded_prefix(self) -> None:
        response = _Response(
            headers=[("Content-Type", "audio/pcm"), ("Content-Encoding", "identity")],
            events=[b"abc", "PRIVATE_NONBYTE_SENTINEL"],
        )
        _, _, failure, _ = _call_transport(_Opener(response))
        self.assertIsNotNone(failure)
        assert failure is not None
        self.assertEqual(failure.code, "provider_response_stream_invalid")
        self.assertEqual(failure.response_bytes, 3)
        self.assertEqual(failure.response_byte_count_state, "bounded_prefix")
        self.assertNotIn(
            "PRIVATE_NONBYTE_SENTINEL",
            json.dumps(worker._failure_metadata(failure)),
        )

    def test_http_error_credential_echo_is_never_hashed_or_serialized(self) -> None:
        key = b"TEST_CREDENTIAL_VALUE_123456"
        body = b"error echoed " + key + b" end"
        response = _Response(
            status=401,
            headers=[("Content-Type", "application/json"), ("Content-Length", str(len(body)))],
            data=body,
        )
        _, _, failure, phases = _call_transport(_Opener(response), key=key)
        self.assertIsNotNone(failure)
        assert failure is not None
        self.assertEqual(failure.code, "provider_response_contains_credential")
        self.assertIsNone(failure.response_sha256)
        self.assertEqual(failure.response_bytes, len(body))
        self.assertEqual(failure.response_body_disposition, "discarded_credential_echo")
        serialized = worker.canonical_json_bytes(worker._failure_metadata(failure))
        self.assertNotIn(key, serialized)
        self.assertNotIn(body, serialized)
        self.assertEqual([phase["phase"] for phase in phases], ["request_starting", "response_headers_confirmed"])
        self.assertTrue(response.closed)

    def test_http_error_safe_body_is_hash_count_only(self) -> None:
        body = b'{"detail":"denied"}'
        response = _Response(
            status=403,
            headers=[("Content-Type", "application/json"), ("Content-Length", str(len(body)))],
            data=body,
        )
        _, _, failure, _ = _call_transport(_Opener(response))
        self.assertIsNotNone(failure)
        assert failure is not None
        self.assertEqual(failure.code, "provider_http_failure")
        self.assertEqual(failure.response_sha256, hashlib.sha256(body).hexdigest())
        self.assertEqual(failure.response_bytes, len(body))
        self.assertEqual(failure.response_body_disposition, "hash_count_only")
        self.assertNotIn(body, worker.canonical_json_bytes(worker._failure_metadata(failure)))

    def test_read_cap_exact_boundary_succeeds(self) -> None:
        cap = 8
        response = _Response(headers=[], events=[b"12345678", b""])
        raw = worker._read_bounded(response, {}, cap, bytearray(b"secret"))
        self.assertEqual(raw, b"12345678")

    def test_read_cap_plus_one_retains_at_most_cap(self) -> None:
        cap = 8
        for events in ([b"123456789"], [b"12345678", b"9"]):
            with self.subTest(events=events):
                response = _Response(headers=[], events=events)
                with self.assertRaises(worker._WorkerFailure) as raised:
                    worker._read_bounded(response, {}, cap, bytearray(b"secret"))
                failure = raised.exception
                self.assertEqual(failure.code, "provider_response_byte_cap_exceeded")
                self.assertEqual(failure.response_bytes, cap)
                self.assertEqual(failure.response_byte_count_state, "bounded_prefix")
                self.assertEqual(
                    failure.response_sha256,
                    hashlib.sha256(b"12345678").hexdigest(),
                )

    def test_declared_cap_plus_one_is_rejected_before_body_read(self) -> None:
        response = _Response(events=[AssertionError("body must not be read")])
        with self.assertRaises(worker._WorkerFailure) as raised:
            worker._read_bounded(
                response,
                {"content-length": "9"},
                8,
                bytearray(b"secret"),
            )
        self.assertEqual(raised.exception.code, "provider_response_byte_cap_exceeded")
        self.assertEqual(raised.exception.response_bytes, 0)

    def test_misbehaving_read_cannot_retain_more_than_cap(self) -> None:
        response = _Response(headers=[], events=[b"x" * 1_000_000])
        with self.assertRaises(worker._WorkerFailure) as raised:
            worker._read_bounded(response, {}, 8, bytearray(b"secret"))
        self.assertEqual(raised.exception.response_bytes, 8)
        self.assertEqual(raised.exception.response_sha256, hashlib.sha256(b"x" * 8).hexdigest())

    def test_exact_opener_disables_proxy_redirect_and_default_user_agent(self) -> None:
        opener = worker._build_exact_opener()
        self.assertEqual(opener.addheaders, [])
        proxy_handlers = [
            item for item in opener.handlers if isinstance(item, urllib.request.ProxyHandler)
        ]
        # Passing an explicit empty ProxyHandler makes build_opener suppress its
        # environment-backed default; an empty handler has no methods and is
        # therefore not retained in the director on Python 3.9.
        self.assertEqual(proxy_handlers, [])
        self.assertTrue(any(isinstance(item, worker._NoRedirect) for item in opener.handlers))

    def test_parent_death_self_destructs_only_isolated_worker_group(self) -> None:
        if not hasattr(os, "fork") or not BOUND_PYTHON.is_file():
            self.skipTest("fork and bound interpreter are required")
        source_fd = os.open(str(WORKER_PATH), os.O_RDONLY)
        command_read, command_write = os.pipe()
        key_read, key_write = os.pipe()
        body_read, body_write = os.pipe()
        result_read, result_write = os.pipe()
        control_read, control_write = os.pipe()
        release_read, release_write = os.pipe()
        worker_pid = -1
        launcher_pid = os.fork()
        if launcher_pid == 0:
            try:
                os.close(command_write)
                os.close(key_write)
                os.close(body_write)
                os.close(result_read)
                os.close(control_read)
                os.close(release_write)
                process = subprocess.Popen(
                    [
                        str(BOUND_PYTHON),
                        "-I",
                        "-S",
                        "-B",
                        "-c",
                        BOOTSTRAP,
                        str(source_fd),
                        str(WORKER_PATH),
                        _source_sha256(),
                        "--command-fd",
                        str(command_read),
                        "--key-fd",
                        str(key_read),
                        "--body-fd",
                        str(body_read),
                        "--result-fd",
                        str(result_write),
                    ],
                    stdin=subprocess.DEVNULL,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    env=dict(worker.SPAWN_ENVIRONMENT),
                    close_fds=True,
                    pass_fds=(source_fd, command_read, key_read, body_read, result_write),
                    start_new_session=True,
                )
                _write_all(control_write, struct.pack("!I", process.pid))
                os.read(release_read, 1)
            except BaseException:
                pass
            finally:
                os._exit(0)
        try:
            os.close(source_fd)
            os.close(command_read)
            os.close(key_read)
            os.close(body_read)
            os.close(result_write)
            os.close(control_write)
            os.close(release_read)
            worker_pid = struct.unpack("!I", _read_exact(control_read, 4))[0]
            ready = json.loads(_read_frame(result_read, 5.0).decode("ascii"))
            self.assertEqual(ready["message"], "ready")
            _write_all(release_write, b"x")
            os.close(release_write)
            release_write = -1
            os.close(control_read)
            control_read = -1
            _, launcher_status = os.waitpid(launcher_pid, 0)
            self.assertTrue(os.WIFEXITED(launcher_status))
            deadline = time.monotonic() + 3.0
            while time.monotonic() < deadline:
                readable, _, _ = select.select([result_read], [], [], 0.05)
                if readable and os.read(result_read, 1) == b"":
                    break
            else:
                self.fail("orphaned worker did not self-destruct")
            self.assertNotEqual(worker_pid, os.getpgrp())
        finally:
            for descriptor in (
                command_write,
                key_write,
                body_write,
                result_read,
                control_read,
                release_read,
                release_write,
            ):
                try:
                    os.close(descriptor)
                except OSError:
                    pass
            if worker_pid > 0:
                try:
                    os.killpg(worker_pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass


if __name__ == "__main__":
    unittest.main()
