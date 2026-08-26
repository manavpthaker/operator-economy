from __future__ import annotations

import ast
import copy
import json
import io
import os
import stat
import struct
import subprocess
import tempfile
import unittest
import urllib.error
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

import oe_narration.audio as audio_module
import oe_narration.performance_transfer as performance_transfer_module
import oe_narration.voice_transfer as voice_transfer_module
from oe_narration.audio import (
    convert_recovery_evidence_working,
    convert_working,
    inspect_audio,
    inspect_recovery_evidence_raw_pcm,
    inspect_provider_raw_pcm,
    validate_pcm_failure_receipt,
)
from oe_narration.cli import build_parser
from oe_narration.core import (
    ValidationError,
    canonical_w_bytes,
    sha256_bytes,
    sha256_file,
    token_identity,
    validate_capture_plan,
)
from oe_narration.provider import dry_run_capture, execute_capture, request_url, validate_execution_authorization


class CapturePlanTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name).resolve()
        self.tokens = ["Cold", "open.", "Evidence", "matters.", "Model", "not", "forecast.", "McKinsey"]
        self.w_path = self.root / "canonical-w.txt"
        self.w_path.write_bytes(canonical_w_bytes(self.tokens))
        identity = token_identity(self.tokens)
        self.bound_files = {}
        for name, content in (
            ("package.json", "package"),
            ("direction.md", "direction"),
            ("voice-lock.md", "voice lock"),
        ):
            path = self.root / name
            path.write_text(content, encoding="utf-8")
            self.bound_files[name] = path
        self.plan = {
            "schema_version": "oe-capture-plan-v1",
            "capture_phase": "calibration",
            "target": {"kind": "fixture", "id": "ai-visibility-v1.1"},
            "script_sha256": "a" * 64,
            "spoken_identity": identity,
            "bindings": {
                "package_manifest": {
                    "path": "package.json",
                    "sha256": sha256_file(self.bound_files["package.json"]),
                },
                "performance_direction": {
                    "path": "direction.md",
                    "sha256": sha256_file(self.bound_files["direction.md"]),
                },
                "voice_capture_lock": {
                    "path": "voice-lock.md",
                    "sha256": sha256_file(self.bound_files["voice-lock.md"]),
                },
            },
            "provider": {
                "name": "elevenlabs",
                "voice_id": "voice-1",
                "model_id": "eleven_v3",
                "voice_settings": {"stability": 0.5, "similarity_boost": 0.6, "style": 0.1},
            },
            "format_policy": {
                "preferred": "pcm_48000",
                "fallback": "mp3_44100_192",
                "fallback_requires": "pcm_capability_unavailable",
            },
            "parts": [],
        }
        modes = ["cold_open", "evidence", "economics", "pronunciation"]
        for index, mode in enumerate(modes):
            start, end = index * 2, index * 2 + 2
            self.plan["parts"].append(
                {
                    "id": mode,
                    "calibration_mode": mode,
                    "start_token": start,
                    "end_token": end,
                    "spoken_text_sha256": token_identity(self.tokens[start:end])["sha256"],
                }
            )
        self.plan_path = self.root / "plan.json"
        self.write_plan()

    def tearDown(self) -> None:
        self.temp.cleanup()

    def write_plan(self) -> None:
        self.plan_path.write_text(json.dumps(self.plan), encoding="utf-8")

    def test_valid_calibration_and_default_dry_run(self) -> None:
        self.assertTrue(validate_capture_plan(self.plan_path, self.w_path)["valid"])
        with mock.patch("urllib.request.urlopen") as urlopen:
            result = dry_run_capture(self.plan_path, self.w_path)
        urlopen.assert_not_called()
        self.assertFalse(result["network_called"])
        first = result["requests"][0]
        self.assertIn("?output_format=pcm_48000", first["url"])

    def test_output_format_is_query_only(self) -> None:
        result = dry_run_capture(self.plan_path, self.w_path)
        self.assertEqual(request_url("voice id", "pcm_48000"), "https://api.elevenlabs.io/v1/text-to-speech/voice%20id?output_format=pcm_48000")
        from oe_narration.provider import build_requests

        request = build_requests(self.plan, self.tokens)[0]
        body = json.loads(request.body)
        self.assertNotIn("output_format", body)
        self.assertEqual(body["text"], "Cold open.")
        self.assertIn("output_format=pcm_48000", request.url)

    def test_embedded_authorization_is_rejected(self) -> None:
        self.plan["authorization"] = {"approved": True}
        self.write_plan()
        with self.assertRaisesRegex(ValidationError, "separate hashed artifact"):
            validate_capture_plan(self.plan_path, self.w_path)

    def test_bound_n1_n2_n3_artifact_tamper_fails(self) -> None:
        self.bound_files["direction.md"].write_text("changed", encoding="utf-8")
        with self.assertRaisesRegex(ValidationError, "performance_direction hash mismatch"):
            validate_capture_plan(self.plan_path, self.w_path)

    def authorization(self) -> dict:
        return {
            "schema_version": "oe-provider-authorization-v1",
            "authorization_id": "auth-cal-001",
            "status": "active",
            "approved": True,
            "scope": "calibration",
            "target": {"kind": "fixture", "id": "ai-visibility-v1.1"},
            "capture_plan_sha256": sha256_file(self.plan_path),
            "script_sha256": "a" * 64,
            "spoken_text_sha256": token_identity(self.tokens)["sha256"],
            "provider": "elevenlabs",
            "model_id": "eleven_v3",
            "voice_id": "voice-1",
            "preferred_output_format": "pcm_48000",
            "fallback_output_format": "mp3_44100_192",
            "max_calls": 4,
            "max_characters": 1000,
            "consumption": {"status": "unconsumed", "calls_used": 0, "record_path": "auth-cal-001.consumed.json"},
            "approved_by": "Owner",
            "approved_at": "2026-08-23T12:00:00Z",
            "expires_at": "2099-08-24T12:00:00Z",
        }

    def test_separate_authorization_is_bound_to_plan(self) -> None:
        auth = self.authorization()
        path = self.root / "auth.json"
        path.write_text(json.dumps(auth), encoding="utf-8")
        self.assertTrue(validate_execution_authorization(path, self.plan_path, self.plan, token_identity(self.tokens)["sha256"], self.tokens)["approved"])
        self.plan_path.write_text(self.plan_path.read_text() + "\n", encoding="utf-8")
        with self.assertRaisesRegex(ValidationError, "capture-plan hash"):
            validate_execution_authorization(path, self.plan_path, self.plan, token_identity(self.tokens)["sha256"], self.tokens)

    def test_expired_or_underbounded_authorization_fails(self) -> None:
        for mutation, pattern in (
            ({"expires_at": "2020-01-01T00:00:00Z"}, "expired"),
            ({"max_characters": 1}, "below the first-attempt payload"),
            ({"max_calls": 9}, "twice planned parts"),
        ):
            auth = self.authorization()
            auth.update(mutation)
            path = self.root / "auth.json"
            path.write_text(json.dumps(auth), encoding="utf-8")
            with self.assertRaisesRegex(ValidationError, pattern):
                validate_execution_authorization(path, self.plan_path, self.plan, token_identity(self.tokens)["sha256"], self.tokens)

    def test_execute_without_key_never_calls_network_or_consumes_authorization(self) -> None:
        auth = self.authorization()
        path = self.root / "auth.json"
        path.write_text(json.dumps(auth), encoding="utf-8")
        with mock.patch.dict("os.environ", {}, clear=True), mock.patch("urllib.request.urlopen") as urlopen:
            with self.assertRaisesRegex(ValidationError, "ELEVENLABS_API_KEY"):
                execute_capture(self.plan_path, self.w_path, self.root / "capture", path)
        urlopen.assert_not_called()
        self.assertFalse((self.root / "auth-cal-001.consumed.json").exists())

    def test_fallback_counts_as_a_second_call_and_ceiling_stops_before_network(self) -> None:
        auth = self.authorization()
        auth["max_calls"] = 4
        auth["max_characters"] = 10_000
        auth_path = self.root / "auth.json"
        auth_path.write_text(json.dumps(auth), encoding="utf-8")
        mp3 = self.root / "fixture.mp3"
        run_ffmpeg(["-f", "lavfi", "-i", "sine=frequency=440:duration=1", "-ar", "44100", "-ac", "1", "-b:a", "192k", str(mp3)])
        pcm = b"\x00\x00" * 100
        error_body = json.dumps(
            {"detail": {"status": "unsupported_output_format", "message": "pcm_48000 is not available"}}
        ).encode()
        first_error = urllib.error.HTTPError(
            "https://example.invalid", 422, "unprocessable", {}, io.BytesIO(error_body)
        )
        calls = [first_error, (mp3.read_bytes(), {"request-id": "fallback"}), (pcm, {}), (pcm, {})]

        def fake_post(*_args):
            value = calls.pop(0)
            if isinstance(value, Exception):
                raise value
            return value

        with mock.patch.dict("os.environ", {"ELEVENLABS_API_KEY": "test-only"}, clear=False), mock.patch(
            "oe_narration.provider._http_post", side_effect=fake_post
        ) as post:
            with self.assertRaisesRegex(ValidationError, "call ceiling exhausted"):
                execute_capture(self.plan_path, self.w_path, self.root / "capture", auth_path)
        self.assertEqual(post.call_count, 4)
        failure = json.loads((self.root / "capture" / "capture-failure-receipt.json").read_text())
        self.assertEqual(failure["attempted_calls"], 4)

    def test_fallback_repeated_payload_counts_against_character_ceiling(self) -> None:
        auth = self.authorization()
        auth["max_calls"] = 8
        auth["max_characters"] = sum(
            len(" ".join(self.tokens[part["start_token"] : part["end_token"]]))
            for part in self.plan["parts"]
        )
        auth_path = self.root / "auth.json"
        auth_path.write_text(json.dumps(auth), encoding="utf-8")
        mp3 = self.root / "fixture.mp3"
        run_ffmpeg(["-f", "lavfi", "-i", "sine=frequency=440:duration=1", "-ar", "44100", "-ac", "1", "-b:a", "192k", str(mp3)])
        error_body = json.dumps(
            {"detail": {"status": "unsupported_output_format", "message": "pcm_48000 is unavailable"}}
        ).encode()
        first_error = urllib.error.HTTPError(
            "https://example.invalid", 422, "unprocessable", {}, io.BytesIO(error_body)
        )
        pcm = b"\x00\x00" * 100
        calls = [first_error, (mp3.read_bytes(), {}), (pcm, {}), (pcm, {})]

        def fake_post(*_args):
            value = calls.pop(0)
            if isinstance(value, Exception):
                raise value
            return value

        with mock.patch.dict("os.environ", {"ELEVENLABS_API_KEY": "test-only"}, clear=False), mock.patch(
            "oe_narration.provider._http_post", side_effect=fake_post
        ) as post:
            with self.assertRaisesRegex(ValidationError, "character ceiling exhausted"):
                execute_capture(self.plan_path, self.w_path, self.root / "capture", auth_path)
        self.assertEqual(post.call_count, 4)
        failure = json.loads((self.root / "capture" / "capture-failure-receipt.json").read_text())
        self.assertEqual(failure["attempted_calls"], 4)
        self.assertLessEqual(failure["attempted_characters"], auth["max_characters"])


def run_ffmpeg(args: list[str]) -> None:
    completed = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", *args], capture_output=True, text=True)
    if completed.returncode:
        raise RuntimeError(completed.stderr)


class AudioTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.transfer_runtime_bindings = {
            "state": "verified",
            "git_commit": "c" * 40,
        }
        for name, (_relative, path) in voice_transfer_module._runtime_files().items():
            cls.transfer_runtime_bindings[f"{name}_sha256"] = (
                sha256_file(path) if path.is_file() else "0" * 64
            )
        probe_path, probe_sha = voice_transfer_module._read_ffprobe_identity()
        ffmpeg_path, ffmpeg_sha = voice_transfer_module._read_ffmpeg_identity()
        git_path, git_sha = voice_transfer_module._read_git_identity()
        cls.transfer_runtime_bindings.update(
            {
                "ffprobe_binary_path": probe_path,
                "ffprobe_binary_sha256": probe_sha,
                "ffprobe_version": voice_transfer_module._read_ffprobe_version(
                    probe_path,
                    probe_sha,
                ),
                "ffmpeg_binary_path": ffmpeg_path,
                "ffmpeg_binary_sha256": ffmpeg_sha,
                "ffmpeg_version": voice_transfer_module._read_ffmpeg_version(
                    ffmpeg_path,
                    ffmpeg_sha,
                ),
                "git_binary_path": git_path,
                "git_binary_sha256": git_sha,
                "git_version": voice_transfer_module._read_git_version(
                    git_path,
                    git_sha,
                ),
                "media_tool_binding_scope": (
                    "primary_executable_bytes_and_version_only"
                ),
                "dynamic_library_dependency_closure_verified": False,
                "media_executable_private_exact_byte_copy_required": True,
            }
        )

    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name).resolve()
        self.source_proof_patcher = mock.patch.object(
            audio_module,
            "_replay_transfer_source_proof",
            return_value=None,
        )
        self.source_proof_patcher.start()
        self.addCleanup(self.source_proof_patcher.stop)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def make_mp3(self, name: str, bitrate: str) -> Path:
        path = self.root / name
        run_ffmpeg(["-f", "lavfi", "-i", "sine=frequency=440:duration=1", "-ar", "44100", "-ac", "1", "-b:a", bitrate, str(path)])
        return path

    def test_media_subprocesses_receive_only_a_minimal_noncredential_environment(self) -> None:
        secret = "test-provider-secret-must-not-reach-child"
        injected = {
            "PATH": f"/tmp/{secret}/bin:/usr/bin:/bin",
            "LANG": "en_US.UTF-8",
            "ELEVENLABS_API_KEY": secret,
            "GOOGLE_APPLICATION_CREDENTIALS": f"/tmp/{secret}",
            "OPENAI_API_KEY": secret,
            "ANTHROPIC_API_KEY": secret,
            "AWS_SECRET_ACCESS_KEY": secret,
            "AZURE_CLIENT_SECRET": secret,
            "HTTP_PROXY": f"https://user:{secret}@proxy.invalid",
            "HTTPS_PROXY": f"https://user:{secret}@proxy.invalid",
            "FFREPORT": f"file=/tmp/{secret}.log",
            "HOME": f"/tmp/{secret}",
            "XDG_CONFIG_HOME": f"/tmp/{secret}",
        }
        completed = subprocess.CompletedProcess(
            args=["ffprobe", "-version"],
            returncode=0,
            stdout="ok",
            stderr="",
        )
        with mock.patch.dict(os.environ, injected, clear=True), mock.patch.object(
            audio_module.subprocess,
            "run",
            return_value=completed,
        ) as child:
            result = audio_module._run(["ffprobe", "-version"])
        self.assertIs(result, completed)
        child_environment = child.call_args.kwargs["env"]
        self.assertEqual(
            child_environment,
            {
                "PATH": audio_module._MEDIA_SUBPROCESS_PATH,
                "LANG": "C",
                "LC_ALL": "C",
            },
        )
        self.assertNotIn(secret, json.dumps(child_environment, sort_keys=True))

    def test_transfer_bound_input_rejects_parent_path_swap_and_symlink(self) -> None:
        for replacement_kind in ("directory", "symlink"):
            with self.subTest(replacement_kind=replacement_kind):
                parent = self.root / f"bound-{replacement_kind}"
                parent.mkdir()
                document = parent / "run.json"
                document.write_text('{"schema_version":"test"}\n', encoding="utf-8")
                document.chmod(0o600)
                bound = audio_module._open_bound_input(
                    document,
                    "voice-transfer test run",
                    byte_cap=4_000_000,
                    required_mode=0o600,
                )
                original_parent = parent.with_name(f"{parent.name}-original")
                replacement_parent = parent.with_name(f"{parent.name}-replacement")
                parent.rename(original_parent)
                replacement_parent.mkdir()
                replacement = replacement_parent / document.name
                replacement.write_bytes(bound.data)
                replacement.chmod(0o600)
                if replacement_kind == "directory":
                    replacement_parent.rename(parent)
                else:
                    parent.symlink_to(replacement_parent, target_is_directory=True)
                try:
                    with self.assertRaisesRegex(
                        ValidationError,
                        "descriptor-bind|no longer names",
                    ):
                        audio_module._revalidate_bound_input(bound)
                finally:
                    audio_module._close_bound_input(bound)

    def test_transfer_replays_git_source_proof_and_rejects_forged_private_run(self) -> None:
        chain = self.make_voice_transfer_chain(
            "transfer-source-proof",
            repository_layout=True,
        )
        authorization_relative = chain["authorization"].relative_to(self.root).as_posix()
        runtime_relative = (
            "operator-blueprint-v2/02-narration-production/"
            "runtime/oe_narration/audio.py"
        )
        runtime_path = self.root / runtime_relative
        runtime_path.parent.mkdir(parents=True)
        actual_runtime = Path(audio_module.__file__).read_bytes()
        runtime_path.write_bytes(actual_runtime)
        self.assertEqual(
            sha256_file(runtime_path),
            chain["authorization_value"]["runtime_bindings"][
                "audio_runtime_sha256"
            ],
        )
        committed_path = chain["fixture"] / "evidence" / "public-source-record.json"
        committed_bytes = b'{"kind":"public-source-record"}\n'
        committed_path.write_bytes(committed_bytes)
        private_path = chain["fixture"] / "evidence" / "private-source-record.json"
        private_bytes = b'{"kind":"private-source-record"}\n'
        private_path.write_bytes(private_bytes)
        private_path.chmod(0o600)
        records = {}
        for name in audio_module._TRANSFER_SOURCE_RECORD_KEYS:
            if name == "plan":
                record_path = chain["plan"]
                record_bytes = chain["plan"].read_bytes()
            elif name == "canonical_w":
                record_path = chain["canonical"]
                record_bytes = chain["canonical"].read_bytes()
            elif name in audio_module._TRANSFER_COMMITTED_SOURCE_RECORD_KEYS:
                record_path = committed_path
                record_bytes = committed_bytes
            else:
                record_path = private_path
                record_bytes = private_bytes
            records[name] = (
                record_path,
                record_bytes,
                audio_module.sha256_bytes(record_bytes),
            )
        contract = mock.Mock(
            root=chain["fixture"],
            authorization_path=chain["authorization"],
            authorization_raw=chain["authorization"].read_bytes(),
            authorization_sha256=sha256_file(chain["authorization"]),
            authorization=chain["authorization_value"],
            records=records,
            consumption_relative=chain["consumption"].relative_to(
                chain["fixture"]
            ).as_posix(),
            success_relative=chain["receipt"].relative_to(
                chain["fixture"]
            ).as_posix(),
            raw_relative=chain["raw"].relative_to(chain["fixture"]).as_posix(),
            working_relative=chain["working"].relative_to(
                chain["fixture"]
            ).as_posix(),
            conversion_relative=chain["conversion"].relative_to(
                chain["fixture"]
            ).as_posix(),
        )
        committed_sources = {
            runtime_relative: actual_runtime,
            chain["plan"].relative_to(self.root).as_posix(): chain[
                "plan"
            ].read_bytes(),
            chain["canonical"].relative_to(self.root).as_posix(): chain[
                "canonical"
            ].read_bytes(),
            committed_path.relative_to(self.root).as_posix(): committed_bytes,
        }
        git_state = {"head": "d" * 40, "status_extra": b""}
        git_calls: list[list[str]] = []

        def fake_git(
            arguments,
            *,
            max_bytes=2_000_000,
            git_path=None,
            git_sha256=None,
        ):
            del max_bytes
            self.assertEqual(
                git_path,
                chain["authorization_value"]["runtime_bindings"][
                    "git_binary_path"
                ],
            )
            self.assertEqual(
                git_sha256,
                chain["authorization_value"]["runtime_bindings"][
                    "git_binary_sha256"
                ],
            )
            git_calls.append(list(arguments))
            if arguments == ["rev-parse", "HEAD"]:
                return (git_state["head"] + "\n").encode("ascii")
            if arguments[:2] == ["merge-base", "--is-ancestor"]:
                return b""
            if arguments[:2] == ["diff", "--no-ext-diff"]:
                self.assertIn("--no-textconv", arguments)
                self.assertIn("--no-renames", arguments)
                return authorization_relative.encode("utf-8") + b"\x00"
            if arguments == ["show", f"HEAD:{authorization_relative}"]:
                return chain["authorization"].read_bytes()
            if arguments == [
                "status",
                "--porcelain=v1",
                "--untracked-files=all",
                "--no-renames",
                "-z",
            ]:
                return b"".join(
                    b"?? "
                    + path.relative_to(self.root).as_posix().encode("utf-8")
                    + b"\x00"
                    for path in (
                        chain["consumption"],
                        chain["receipt"],
                        chain["raw"],
                    )
                ) + git_state["status_extra"]
            if arguments[0] == "show" and arguments[1].startswith("c" * 40 + ":"):
                relative = arguments[1].split(":", 1)[1]
                if relative in committed_sources:
                    return committed_sources[relative]
            raise AssertionError(f"unexpected git call: {arguments}")

        self.assertEqual(os.stat(chain["receipt"]).st_mode & 0o777, 0o600)
        self.assertEqual(os.stat(chain["raw"]).st_mode & 0o777, 0o600)
        self.source_proof_patcher.stop()
        try:
            with mock.patch.object(
                performance_transfer_module,
                "_guide_repository_root",
                return_value=self.root,
            ), mock.patch.object(
                performance_transfer_module,
                "_guide_git",
                side_effect=fake_git,
            ), mock.patch.object(
                voice_transfer_module,
                "_runtime_files",
                return_value={
                    "audio_runtime": (runtime_relative, runtime_path),
                },
            ), mock.patch.object(
                voice_transfer_module,
                "_verify_local_git_object_store",
            ) as verify_object_store, mock.patch.object(
                voice_transfer_module,
                "_build_transfer_contract",
                return_value=contract,
            ) as build_contract, mock.patch(
                "oe_narration.voice_transfer.validate_voice_transfer_execution_authorization",
                return_value={"valid": True},
                create=True,
            ):
                inspected = inspect_provider_raw_pcm(
                    chain["raw"],
                    chain["receipt"],
                    chain["part_id"],
                )
                self.assertEqual(
                    inspected["capture_receipt_schema_version"],
                    "oe-elevenlabs-voice-transfer-run-v1",
                )
                private_relative = private_path.relative_to(self.root).as_posix()
                self.assertFalse(
                    any(
                        arguments
                        and arguments[0] == "show"
                        and private_relative in arguments[-1]
                        for arguments in git_calls
                    ),
                    "local-private media/evidence must not require a Git blob",
                )
                build_contract.assert_called_with(
                    chain["authorization"],
                    chain["plan"],
                    chain["canonical"],
                    enforce_current_execution_window=False,
                )
                verify_object_store.assert_called_with(
                    chain["authorization_value"]["runtime_bindings"]
                )

                runtime_path.write_bytes(b"dirty runtime bytes")
                with self.assertRaisesRegex(
                    ValidationError,
                    "runtime source audio_runtime differs",
                ):
                    inspect_provider_raw_pcm(
                        chain["raw"],
                        chain["receipt"],
                        chain["part_id"],
                    )
                runtime_path.write_bytes(actual_runtime)

                private_path.write_bytes(b'{"kind":"dirty-private-source"}\n')
                private_path.chmod(0o600)
                with self.assertRaisesRegex(
                    ValidationError,
                    "reconstructed source record .* differs",
                ):
                    inspect_provider_raw_pcm(
                        chain["raw"],
                        chain["receipt"],
                        chain["part_id"],
                    )
                private_path.write_bytes(private_bytes)
                private_path.chmod(0o600)

                git_state["status_extra"] = (
                    b"?? operator-blueprint-v2/unrelated-private-output.json\x00"
                )
                with self.assertRaisesRegex(
                    ValidationError,
                    "non-authorized worktree changes",
                ):
                    inspect_provider_raw_pcm(
                        chain["raw"],
                        chain["receipt"],
                        chain["part_id"],
                    )
                git_state["status_extra"] = b""

                private_path.chmod(0o644)
                with self.assertRaisesRegex(ValidationError, "0600"):
                    inspect_provider_raw_pcm(
                        chain["raw"],
                        chain["receipt"],
                        chain["part_id"],
                    )
                private_path.chmod(0o600)

                git_state["head"] = "e" * 40
                with self.assertRaisesRegex(
                    ValidationError,
                    "source proof HEAD/runtime identity mismatch",
                ):
                    inspect_provider_raw_pcm(
                        chain["raw"],
                        chain["receipt"],
                        chain["part_id"],
                    )
        finally:
            self.source_proof_patcher.start()

    def test_audio_cli_preserves_symlink_components_for_runtime_rejection(self) -> None:
        real = self.root / "real"
        real.mkdir()
        linked = self.root / "linked"
        linked.symlink_to(real, target_is_directory=True)
        requested = linked / "raw.pcm"
        args = build_parser().parse_args(
            ["inspect-audio", "--input", str(requested)]
        )
        self.assertEqual(args.input, requested)
        self.assertNotEqual(args.input, requested.resolve(strict=False))

    def failure_receipt(self, raw: Path, status: int = 422, kind: str = "pcm_capability_unavailable") -> Path:
        path = self.root / f"{raw.stem}-failure.json"
        value = {
            "schema_version": "oe-pcm-capability-failure-v1",
            "provider": "elevenlabs",
            "attempted_output_format": "pcm_48000",
            "fallback_output_format": "mp3_44100_192",
            "failure": {
                "http_status": status,
                "kind": kind,
                "retryable": False,
                "provider_code": "unsupported_output_format",
                "message": "pcm_48000 is not available for this account",
                "occurred_at": "2026-08-23T12:00:00Z",
            },
            "raw_output": {"path": str(raw), "sha256": sha256_file(raw)},
        }
        path.write_text(json.dumps(value), encoding="utf-8")
        return path

    def write_private_json(self, path: Path, value: dict) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        path.chmod(0o600)

    def runtime_bindings_with_tool(self, tool: str, path: Path) -> dict:
        bindings = copy.deepcopy(self.transfer_runtime_bindings)
        resolved = str(path.resolve(strict=True))
        digest = sha256_file(path)
        version_reader = (
            voice_transfer_module._read_ffmpeg_version
            if tool == "ffmpeg"
            else voice_transfer_module._read_ffprobe_version
        )
        bindings[f"{tool}_binary_path"] = resolved
        bindings[f"{tool}_binary_sha256"] = digest
        bindings[f"{tool}_version"] = version_reader(resolved, digest)
        return bindings

    def make_voice_transfer_chain(
        self,
        name: str = "voice-transfer",
        *,
        duration_seconds: float = 34.0,
        repository_layout: bool = False,
        runtime_bindings: dict | None = None,
    ) -> dict[str, object]:
        fixture_parent = self.root
        if repository_layout:
            fixture_parent = (
                self.root
                / "operator-blueprint-v2"
                / "02-narration-production"
                / "fixtures"
            )
        fixture = fixture_parent / name
        fixture.mkdir(parents=True)
        canonical = fixture / "canonical-w.txt"
        canonical.write_text("exact words\n", encoding="utf-8")
        plan = fixture / "performance-transfer-plan.json"
        plan.write_text(
            json.dumps({"canonical_w": {"path": "canonical-w.txt"}}),
            encoding="utf-8",
        )

        part_id = "P01-W0030-W0110"
        authorization_id = "AUTH-V2-test-one-private-transfer"
        authorization_relative = f"authorizations/{authorization_id}.ACTIVE.json"
        authorization_path = fixture / authorization_relative
        raw_relative = "outputs/raw/elevenlabs/P01-W0030-W0110/saved-c-transfer.pcm"
        working_relative = "outputs/working/elevenlabs/P01-W0030-W0110/saved-c-transfer.wav"
        success_relative = f"receipts/elevenlabs/{authorization_id}.run.json"
        failure_relative = f"receipts/elevenlabs/{authorization_id}.failure.json"
        conversion_relative = f"receipts/elevenlabs/{authorization_id}.conversion.json"
        consumption_relative = (
            f"authorizations/consumed/{authorization_id}.voice-transfer-execution.consumed.json"
        )
        raw = fixture / raw_relative
        raw.parent.mkdir(parents=True)
        raw.write_bytes(b"\x01\x00" * int(48_000 * duration_seconds))
        raw.chmod(0o600)
        raw_size = raw.stat().st_size
        raw_frames = raw_size // 2
        raw_duration = raw_frames / 48_000

        plan_sha = sha256_file(plan)
        canonical_sha = sha256_file(canonical)
        spoken_sha = "3" * 64
        guide = fixture / "outputs" / "raw" / "vertex" / "candidate-B.wav"
        guide.parent.mkdir(parents=True)
        guide.write_bytes(b"test-guide-bytes")
        guide_sha = sha256_file(guide)
        guide_run = fixture / "receipts" / "vertex" / "guide-run.json"
        self.write_private_json(guide_run, {"schema_version": "test-guide-run"})
        guide_run_sha = sha256_file(guide_run)
        primary_request_sha = "6" * 64
        normalized_request_sha = "7" * 64
        multipart_sha = "8" * 64
        multipart_bytes = 1_646_839
        content_type = (
            "multipart/form-data; boundary="
            "oe-v05-04448e9fdd50c8de67912b454e8d396f"
        )
        api_key_fingerprint = "a" * 64
        account_scope = "b" * 64
        runtime_commit = "c" * 40
        prerequisite_names = (
            "selected_guide",
            "guide_qa",
            "owner_selection",
            "owner_audition_confirmation",
            "elevenlabs_data_use",
            "target_voice_rights",
            "credential_account_verification",
            "official_media_contract",
        )
        prerequisites = {}
        for key in prerequisite_names:
            if key == "selected_guide":
                prerequisites[key] = {
                    "state": "verified",
                    "path": guide.relative_to(fixture).as_posix(),
                    "sha256": guide_sha,
                    "byte_count": guide.stat().st_size,
                    "duration_seconds": 21.0,
                    "container": "wav",
                    "codec": "pcm_s16le",
                    "sample_rate_hz": 48_000,
                    "channels": 1,
                    "guide_request_id": "G1R2",
                    "guide_run_receipt_path": guide_run.relative_to(fixture).as_posix(),
                    "guide_run_receipt_sha256": guide_run_sha,
                }
                continue
            if key == "official_media_contract":
                evidence_path = fixture / audio_module._TRANSFER_MEDIA_CONTRACT_PATH
                source_path = (
                    Path(__file__).resolve().parents[2]
                    / "fixtures"
                    / "step2-v0.5-ai-visibility-v1.1-synthetic-guide-to-saved-c-transfer-microtest"
                    / audio_module._TRANSFER_MEDIA_CONTRACT_PATH
                )
                self.assertEqual(
                    sha256_file(source_path),
                    audio_module._TRANSFER_MEDIA_CONTRACT_SHA256,
                )
                evidence_path.parent.mkdir(parents=True, exist_ok=True)
                evidence_path.write_bytes(source_path.read_bytes())
                prerequisites[key] = {
                    "state": "verified",
                    "path": audio_module._TRANSFER_MEDIA_CONTRACT_PATH,
                    "sha256": sha256_file(evidence_path),
                }
                continue
            evidence_path = fixture / "evidence" / f"{key}.json"
            self.write_private_json(evidence_path, {"kind": key})
            prerequisites[key] = {
                "state": "verified",
                "path": evidence_path.relative_to(fixture).as_posix(),
                "sha256": sha256_file(evidence_path),
            }
        prerequisite_sha256s = {
            key: value["sha256"] for key, value in prerequisites.items()
        }
        artifacts = {
            "raw_output_path": raw_relative,
            "working_output_path": working_relative,
            "success_receipt_path": success_relative,
            "failure_receipt_path": failure_relative,
            "conversion_receipt_path": conversion_relative,
        }
        action = {
            "provider": "elevenlabs",
            "endpoint": "https://api.elevenlabs.io/v1/speech-to-speech/scMbPZwQjr40V1MzL3Nj",
            "method": "POST",
            "query": {"enable_logging": True, "output_format": "pcm_48000"},
            "credential_header_name": "xi-api-key",
            "accept": "application/octet-stream",
            "accept_encoding": "identity",
        }
        bindings = {
            "performance_transfer_plan_sha256": plan_sha,
            "canonical_w_sha256": canonical_sha,
            "spoken_text_sha256": spoken_sha,
            "selected_guide_sha256": guide_sha,
            "guide_run_receipt_sha256": guide_run_sha,
            "primary_request_sha256": primary_request_sha,
            "normalized_http_request_sha256": normalized_request_sha,
            "primary_multipart_body_sha256": multipart_sha,
            "primary_multipart_body_bytes": multipart_bytes,
            "multipart_content_type": content_type,
        }
        authorization = {
            "schema_version": "oe-voice-transfer-execution-authorization-v2",
            "authorization_id": authorization_id,
            "status": "active",
            "approved": True,
            "scope": "elevenlabs_voice_transfer_execution",
            "bindings": bindings,
            "prerequisites": prerequisites,
            "action": action,
            "credential_binding": {
                "state": "verified",
                "api_key_fingerprint_sha256": api_key_fingerprint,
                "account_scope_binding_sha256": account_scope,
            },
            "runtime_bindings": copy.deepcopy(
                self.transfer_runtime_bindings
                if runtime_bindings is None
                else runtime_bindings
            ),
            "authorized_limits": voice_transfer_module._transfer_limits(True),
            "artifacts": artifacts,
            "consumption": {
                "status": "unconsumed",
                "record_path": consumption_relative,
            },
            "approved_by": "Manav Thaker",
            "approved_at": "2026-08-26T06:30:00Z",
            "expires_at": "2026-08-26T07:30:00Z",
            "execution_ready": True,
            "blockers": [],
        }
        authorization_path.parent.mkdir(parents=True)
        authorization_path.write_text(
            json.dumps(authorization, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        authorization_sha = sha256_file(authorization_path)

        consumption_path = fixture / consumption_relative
        consumption = {
            "schema_version": "oe-elevenlabs-voice-transfer-consumption-v1",
            "authorization_id": authorization_id,
            "authorization_path": authorization_relative,
            "authorization_sha256": authorization_sha,
            "scope": "elevenlabs_voice_transfer_execution",
            "status": "consumed_before_credential_and_network",
            "consumed_at": "2026-08-26T06:31:00Z",
            "consumed_before_credential_access": True,
            "credential_accessed_at_consumption": False,
            "network_called_at_consumption": False,
            "account_get_calls_used": 0,
            "generation_post_calls_used": 0,
            "outputs_received": 0,
            "spend_used_usd": 0,
            "primary_request_sha256": primary_request_sha,
            "multipart_body_sha256": multipart_sha,
        }
        self.write_private_json(consumption_path, consumption)
        consumption_sha = sha256_file(consumption_path)

        exact_url = (
            f"{action['endpoint']}?enable_logging=true&output_format=pcm_48000"
        )
        receipt = {
            "schema_version": "oe-elevenlabs-voice-transfer-run-v1",
            "outcome": "success",
            "provider": "elevenlabs",
            "scope": "elevenlabs_voice_transfer_execution",
            "method": "POST",
            "endpoint": action["endpoint"],
            "part_id": part_id,
            "authorization_id": authorization_id,
            "authorization_path": authorization_relative,
            "authorization_sha256": authorization_sha,
            "consumption_record_path": consumption_relative,
            "consumption_record_sha256": consumption_sha,
            "source_proof": {
                "git_head": "d" * 40,
                "runtime_commit": runtime_commit,
                "remote_state_checked": False,
                "git_network_called": False,
                "git_status_scope": "repository_index_and_unignored_worktree_only",
                "git_execution_by_descriptor": False,
                "git_absolute_path_identity_checked_pre_and_post": True,
                "git_path_swap_risk": (
                    "root_owned_system_binary_not_same_uid_writable"
                ),
                "head_delta_policy": "exact_active_authorization_path_only",
                "head_delta_path": (
                    "operator-blueprint-v2/02-narration-production/fixtures/"
                    f"{fixture.name}/{authorization_relative}"
                ),
            },
            "plan_sha256": plan_sha,
            "canonical_w_sha256": canonical_sha,
            "spoken_text_sha256": spoken_sha,
            "selected_guide_sha256": guide_sha,
            "selected_guide_run_receipt_sha256": guide_run_sha,
            "prerequisite_sha256s": prerequisite_sha256s,
            "api_key_fingerprint_sha256": api_key_fingerprint,
            "account_scope_binding_sha256": account_scope,
            "request": {
                "part_id": part_id,
                "primary_request_sha256": primary_request_sha,
                "normalized_http_request_sha256": normalized_request_sha,
                "method": "POST",
                "exact_url": exact_url,
                "multipart_body_sha256": multipart_sha,
                "multipart_body_bytes": multipart_bytes,
                "content_type": content_type,
                "credential_header_name": "xi-api-key",
                "accept": "application/octet-stream",
                "accept_encoding": "identity",
            },
            "provider_evidence": {
                "account_get_calls_made": 0,
                "generation_post_calls_made": 1,
                "outputs_received": 1,
                "request_ids": {"request-id": "req-test-001"},
                "usage": {"request-cost": 1},
            },
            "response": {
                "http_status": 200,
                "response_bytes": raw_size,
                "response_sha256": sha256_file(raw),
                "declared_mime_type": "audio/pcm",
                "content_encoding": "identity",
                "media_interpretation": {
                    "classification": "interpreted_pcm_under_exact_format_contract",
                    "output_format": "pcm_48000",
                    "declared_mime_allowlist": ["audio/pcm", "audio/mpeg"],
                    "compressed_or_container_signature_detected": False,
                    "negative_ffprobe_detected_format": False,
                    "headerless_bytes_intrinsically_prove_codec_geometry": False,
                    "official_media_contract_sha256": audio_module._TRANSFER_MEDIA_CONTRACT_SHA256,
                },
            },
            "raw_output": {
                "part_id": part_id,
                "path": raw_relative,
                "sha256": sha256_file(raw),
                "byte_count": raw_size,
                "container_interpretation": "raw",
                "codec_interpretation": "pcm_s16le",
                "sample_rate_hz_interpretation": 48_000,
                "channel_count_interpretation": 1,
                "bit_depth_interpretation": 16,
                "frame_count_under_mono_contract_interpretation": raw_frames,
                "duration_seconds_under_mono_contract_interpretation": raw_duration,
                "output_to_source_duration_ratio_under_mono_contract_interpretation": (
                    raw_duration
                    / audio_module._TRANSFER_SELECTED_GUIDE_DURATION_SECONDS
                ),
                "format_parameters_intrinsically_verified": False,
                "channel_count_intrinsically_verified": False,
                "frame_and_duration_computed_under_mono_contract_interpretation": True,
                "lossy_interpretation": False,
            },
            "working_output_path": working_relative,
            "conversion_receipt_path": conversion_relative,
            "started_at": "2026-08-26T06:31:01Z",
            "completed_at": "2026-08-26T06:31:25Z",
            "modeled_spend_usd": 0.12,
            "modeled_spend_basis": "voice_changer_full_minute_worst_case",
            "modeled_spend_provider_enforced": False,
            "taxes_included": False,
            "retries_made": 0,
            "redirects_followed": 0,
            "fallbacks_used": 0,
            "credentials_recorded": False,
            "raw_api_key_stored": False,
            "creative_approved": False,
            "full_capture_authorized": False,
            "step2_lock_authorized": False,
            "step3_authorized": False,
            "sharing_authorized": False,
            "publication_authorized": False,
        }
        receipt_path = fixture / success_relative
        self.write_private_json(receipt_path, receipt)
        return {
            "fixture": fixture,
            "plan": plan,
            "canonical": canonical,
            "raw": raw,
            "working": fixture / working_relative,
            "conversion": fixture / conversion_relative,
            "authorization": authorization_path,
            "authorization_value": authorization,
            "consumption": consumption_path,
            "consumption_value": consumption,
            "receipt": receipt_path,
            "receipt_value": receipt,
            "prerequisites": prerequisites,
            "part_id": part_id,
        }

    def test_voice_transfer_pcm_positive_conversion_is_one_time_and_private(self) -> None:
        chain = self.make_voice_transfer_chain()
        with mock.patch(
            "oe_narration.voice_transfer.validate_voice_transfer_execution_authorization",
            return_value={"valid": True},
            create=True,
        ) as validate_active:
            result = convert_working(
                chain["raw"],
                chain["working"],
                chain["receipt"],
                chain["part_id"],
                chain["conversion"],
            )
        validate_active.assert_called_once_with(
            chain["authorization"],
            chain["plan"],
            chain["canonical"],
        )
        self.assertEqual(result["raw"]["capture_receipt_schema_version"], "oe-elevenlabs-voice-transfer-run-v1")
        self.assertEqual(result["raw"]["part_id"], chain["part_id"])
        self.assertEqual(result["raw"]["codec_interpretation"], "pcm_s16le")
        self.assertEqual(result["raw"]["channel_count_interpretation"], 1)
        self.assertFalse(result["raw"]["format_parameters_intrinsically_verified"])
        self.assertFalse(result["raw"]["channel_count_intrinsically_verified"])
        self.assertNotIn("actual_codec", result["raw"])
        self.assertNotIn("codec_name", result["raw"])
        self.assertNotIn("duration_seconds", result["raw"])
        self.assertEqual(
            result["raw"]["authorization_sha256"],
            sha256_file(chain["authorization"]),
        )
        self.assertEqual(
            result["raw"]["consumption_record_sha256"],
            sha256_file(chain["consumption"]),
        )
        self.assertEqual(
            result["raw"]["authorized_working_output_path"],
            str(chain["working"]),
        )
        self.assertEqual(
            result["raw"]["authorized_conversion_receipt_path"],
            str(chain["conversion"]),
        )
        self.assertFalse(result["lossy_interpretation"])
        self.assertFalse(result["lossy_origin_intrinsically_verified"])
        self.assertNotIn("lossy_origin", result)
        self.assertTrue(result["working"]["is_working_master"])
        self.assertEqual(os.stat(chain["working"]).st_mode & 0o777, 0o600)
        self.assertEqual(os.stat(chain["conversion"]).st_mode & 0o777, 0o600)
        record = json.loads(chain["conversion"].read_text(encoding="utf-8"))
        self.assertEqual(record["raw_immutable_sha256"], sha256_file(chain["raw"]))
        with self.assertRaisesRegex(ValidationError, "refusing to overwrite working audio"):
            convert_working(
                chain["raw"],
                chain["working"],
                chain["receipt"],
                chain["part_id"],
                chain["conversion"],
            )

    def test_voice_transfer_uses_private_exact_bound_tools_despite_hostile_path(self) -> None:
        chain = self.make_voice_transfer_chain("transfer-bound-tools")
        hostile = self.root / "hostile-path"
        hostile.mkdir()
        sentinels = []
        for tool in ("ffmpeg", "ffprobe"):
            sentinel = self.root / f"{tool}-path-shim-ran"
            sentinels.append(sentinel)
            shim = hostile / tool
            shim.write_text(
                "#!/bin/sh\n"
                f"/usr/bin/touch '{sentinel}'\n"
                "exit 99\n",
                encoding="utf-8",
            )
            shim.chmod(0o500)
        original_bounded_run = audio_module._run_bounded_media_process
        observed: list[tuple[list[str], str]] = []
        observed_private_directories: set[Path] = set()

        def observe_bound_run(
            command,
            *,
            executable,
            pass_fds=(),
            timeout_seconds,
        ):
            executable_path = Path(executable)
            executable_stat = executable_path.stat()
            directory_stat = executable_path.parent.stat()
            observed_private_directories.add(executable_path.parent)
            self.assertEqual(stat.S_IMODE(directory_stat.st_mode), 0o700)
            self.assertEqual(stat.S_IMODE(executable_stat.st_mode), 0o500)
            self.assertEqual(executable_stat.st_nlink, 1)
            self.assertEqual(executable_stat.st_uid, os.getuid())
            tool = Path(command[0]).name
            self.assertEqual(
                sha256_file(executable_path),
                chain["authorization_value"]["runtime_bindings"][
                    f"{tool}_binary_sha256"
                ],
            )
            observed.append((list(command), executable))
            return original_bounded_run(
                command,
                executable=executable,
                pass_fds=pass_fds,
                timeout_seconds=timeout_seconds,
            )

        real_popen = subprocess.Popen
        injected_secret = "provider-secret-must-not-reach-v2-media-child"
        with mock.patch.dict(
            os.environ,
            {
                "PATH": str(hostile),
                "ELEVENLABS_API_KEY": injected_secret,
                "GOOGLE_APPLICATION_CREDENTIALS": f"/tmp/{injected_secret}",
            },
            clear=False,
        ), mock.patch(
            "oe_narration.voice_transfer.validate_voice_transfer_execution_authorization",
            return_value={"valid": True},
            create=True,
        ), mock.patch.object(
            audio_module,
            "_run_bounded_media_process",
            side_effect=observe_bound_run,
        ), mock.patch.object(
            audio_module.subprocess,
            "Popen",
            wraps=real_popen,
        ) as popen:
            result = convert_working(
                chain["raw"],
                chain["working"],
                chain["receipt"],
                chain["part_id"],
                chain["conversion"],
            )
        self.assertTrue(result["working"]["is_working_master"])
        self.assertEqual(
            [Path(command[0]).name for command, _executable in observed],
            ["ffmpeg", "ffprobe", "ffmpeg"],
        )
        for command, executable in observed:
            tool = Path(command[0]).name
            self.assertEqual(
                command[0],
                chain["authorization_value"]["runtime_bindings"][
                    f"{tool}_binary_path"
                ],
            )
            self.assertEqual(Path(executable).parent.parent, Path("/private/tmp"))
            self.assertFalse(Path(executable).exists())
        for call in popen.call_args_list:
            if call.kwargs.get("start_new_session") is not True:
                continue
            child_environment = call.kwargs["env"]
            self.assertEqual(
                child_environment,
                {
                    "PATH": audio_module._MEDIA_SUBPROCESS_PATH,
                    "LANG": "C",
                    "LC_ALL": "C",
                },
            )
            self.assertNotIn(
                injected_secret,
                json.dumps(child_environment, sort_keys=True),
            )
        self.assertFalse(any(path.exists() for path in sentinels))
        self.assertTrue(observed_private_directories)
        self.assertFalse(
            any(path.exists() for path in observed_private_directories)
        )

    def test_voice_transfer_rejects_bound_media_binary_path_swap(self) -> None:
        for tool in ("ffmpeg", "ffprobe"):
            with self.subTest(tool=tool):
                original_tool = Path(
                    self.transfer_runtime_bindings[f"{tool}_binary_path"]
                )
                bound_tool = self.root / f"bound-{tool}"
                bound_tool.write_bytes(original_tool.read_bytes())
                bound_tool.chmod(0o500)
                bindings = self.runtime_bindings_with_tool(tool, bound_tool)
                chain = self.make_voice_transfer_chain(
                    f"transfer-{tool}-path-swap",
                    runtime_bindings=bindings,
                )
                original_bounded_run = audio_module._run_bounded_media_process
                swapped = False
                observed_private_directories: set[Path] = set()

                def swap_bound_path(
                    command,
                    *,
                    executable,
                    pass_fds=(),
                    timeout_seconds,
                ):
                    nonlocal swapped
                    observed_private_directories.add(Path(executable).parent)
                    should_swap = (
                        tool == "ffmpeg" and command[0] == str(bound_tool)
                    ) or (
                        tool == "ffprobe"
                        and Path(command[0]).name == "ffmpeg"
                    )
                    result = original_bounded_run(
                        command,
                        executable=executable,
                        pass_fds=pass_fds,
                        timeout_seconds=timeout_seconds,
                    )
                    if should_swap and not swapped:
                        original = bound_tool.with_suffix(".validated-original")
                        bound_tool.rename(original)
                        bound_tool.write_text(
                            "#!/bin/sh\nexit 98\n",
                            encoding="utf-8",
                        )
                        bound_tool.chmod(0o500)
                        swapped = True
                    return result

                with mock.patch(
                    "oe_narration.voice_transfer.validate_voice_transfer_execution_authorization",
                    return_value={"valid": True},
                    create=True,
                ), mock.patch.object(
                    audio_module,
                    "_run_bounded_media_process",
                    side_effect=swap_bound_path,
                ):
                    with self.assertRaisesRegex(
                        ValidationError,
                        "bound executable|SHA-256|identity|cleanup failed",
                    ):
                        convert_working(
                            chain["raw"],
                            chain["working"],
                            chain["receipt"],
                            chain["part_id"],
                            chain["conversion"],
                        )
                self.assertTrue(swapped)
                self.assertFalse(chain["working"].exists())
                self.assertFalse(chain["conversion"].exists())
                self.assertTrue(observed_private_directories)
                self.assertFalse(
                    any(path.exists() for path in observed_private_directories)
                )

    def test_bounded_v2_media_process_rejects_hang_and_output_flood(self) -> None:
        script = self.root / "bounded-media-adversary"
        script.write_text(
            "#!/bin/sh\n"
            "case \"$1\" in\n"
            "  hang) while :; do /bin/sleep 1; done ;;\n"
            "  flood-stdout) while :; do printf 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'; done ;;\n"
            "  flood-stderr) while :; do printf 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx' >&2; done ;;\n"
            "esac\n",
            encoding="utf-8",
        )
        script.chmod(0o500)
        with self.assertRaisesRegex(ValidationError, "timed out"):
            audio_module._run_bounded_media_process(
                [str(script), "hang"],
                executable=str(script),
                pass_fds=(),
                timeout_seconds=0.2,
            )
        for stream in ("stdout", "stderr"):
            with self.subTest(stream=stream), mock.patch.object(
                audio_module,
                f"_TRANSFER_MEDIA_{stream.upper()}_CAP",
                1_024,
            ):
                with self.assertRaisesRegex(
                    ValidationError,
                    f"{stream} exceeded its byte cap",
                ):
                    audio_module._run_bounded_media_process(
                        [str(script), f"flood-{stream}"],
                        executable=str(script),
                        pass_fds=(),
                        timeout_seconds=2.0,
                    )

    def test_voice_transfer_ffmpeg_uses_raw_fd_and_rejects_pathname_swap(self) -> None:
        chain = self.make_voice_transfer_chain("transfer-raw-path-swap")
        original_run = audio_module._run_bounded_media_process
        observed: dict[str, object] = {}

        def swap_before_child(
            command,
            *,
            executable,
            pass_fds=(),
            timeout_seconds,
        ):
            if Path(command[0]).name == "ffmpeg" and not observed:
                input_value = command[command.index("-i") + 1]
                observed["input"] = input_value
                observed["pass_fds"] = pass_fds
                raw_descriptor = int(input_value.rsplit("/", 1)[1])
                self.assertIn(raw_descriptor, pass_fds)
                original_raw = chain["raw"].with_name("original-provider-response.pcm")
                chain["raw"].rename(original_raw)
                chain["raw"].write_bytes(b"\x01\x00" * (48_000 * 20))
                chain["raw"].chmod(0o600)
            return original_run(
                command,
                executable=executable,
                pass_fds=pass_fds,
                timeout_seconds=timeout_seconds,
            )

        with mock.patch(
            "oe_narration.voice_transfer.validate_voice_transfer_execution_authorization",
            return_value={"valid": True},
            create=True,
        ), mock.patch.object(
            audio_module,
            "_run_bounded_media_process",
            side_effect=swap_before_child,
        ):
            with self.assertRaisesRegex(ValidationError, "path no longer names"):
                convert_working(
                    chain["raw"],
                    chain["working"],
                    chain["receipt"],
                    chain["part_id"],
                    chain["conversion"],
                )
        self.assertRegex(str(observed["input"]), r"^/dev/fd/[0-9]+$")
        self.assertNotIn(str(chain["raw"]), str(observed["input"]))
        self.assertFalse(chain["working"].exists())
        self.assertFalse(chain["conversion"].exists())

    def test_voice_transfer_accepts_official_generic_mime_after_negative_probe(self) -> None:
        chain = self.make_voice_transfer_chain("transfer-generic-mime")
        receipt = copy.deepcopy(chain["receipt_value"])
        receipt["response"]["declared_mime_type"] = "audio/mpeg"
        self.write_private_json(chain["receipt"], receipt)
        with mock.patch(
            "oe_narration.voice_transfer.validate_voice_transfer_execution_authorization",
            return_value={"valid": True},
            create=True,
        ):
            inspected = inspect_provider_raw_pcm(
                chain["raw"],
                chain["receipt"],
                chain["part_id"],
            )
        self.assertEqual(inspected["codec_interpretation"], "pcm_s16le")
        self.assertEqual(inspected["container_interpretation"], "raw")
        self.assertFalse(inspected["format_parameters_intrinsically_verified"])
        self.assertFalse(inspected["channel_count_intrinsically_verified"])
        self.assertNotIn("codec_name", inspected)
        self.assertNotIn("channels", inspected)

    def test_voice_transfer_uses_exact_shared_bound_probe_and_rejects_detection(self) -> None:
        chain = self.make_voice_transfer_chain("transfer-positive-probe-detection")
        with mock.patch(
            "oe_narration.voice_transfer.validate_voice_transfer_execution_authorization",
            return_value={"valid": True},
            create=True,
        ), mock.patch.object(
            voice_transfer_module,
            "_negative_ffprobe_media_detection",
            side_effect=performance_transfer_module._GuideExecutionFailure(
                "ffprobe_detected_or_ambiguous_media_format"
            ),
        ) as probe:
            with self.assertRaisesRegex(
                ValidationError,
                "ffprobe_detected_or_ambiguous_media_format",
            ):
                inspect_provider_raw_pcm(
                    chain["raw"],
                    chain["receipt"],
                    chain["part_id"],
                )
        probe.assert_called_once_with(
            chain["raw"].read_bytes(),
            ffprobe_path=chain["authorization_value"]["runtime_bindings"][
                "ffprobe_binary_path"
            ],
            ffprobe_sha256=chain["authorization_value"]["runtime_bindings"][
                "ffprobe_binary_sha256"
            ],
            ffprobe_version=chain["authorization_value"]["runtime_bindings"][
                "ffprobe_version"
            ],
        )

    def test_voice_transfer_rejects_transport_request_part_and_geometry_tamper(self) -> None:
        chain = self.make_voice_transfer_chain("transfer-tamper")
        baseline = copy.deepcopy(chain["receipt_value"])
        mutations = (
            (("response", "declared_mime_type"), "application/octet-stream"),
            (("response", "content_encoding"), "gzip"),
            (("response", "media_interpretation", "headerless_bytes_intrinsically_prove_codec_geometry"), True),
            (("response", "media_interpretation", "compressed_or_container_signature_detected"), True),
            (("response", "media_interpretation", "negative_ffprobe_detected_format"), True),
            (("response", "media_interpretation", "official_media_contract_sha256"), "0" * 64),
            (("response", "http_status"), 201),
            (("provider_evidence", "generation_post_calls_made"), 2),
            (("provider_evidence", "outputs_received"), 2),
            (("provider_evidence", "request_ids", "request-id"), "xi_abcdefghijklmnopqrst"),
            (("provider_evidence", "usage", "request-cost"), True),
            (("retries_made",), 1),
            (("redirects_followed",), 1),
            (("fallbacks_used",), 1),
            (("modeled_spend_usd",), 0.13),
            (("modeled_spend_provider_enforced",), True),
            (("part_id",), "wrong-part"),
            (("request", "part_id"), "wrong-part"),
            (("raw_output", "part_id"), "wrong-part"),
            (("request", "primary_request_sha256"), "f" * 64),
            (("request", "multipart_body_sha256"), "e" * 64),
            (("raw_output", "byte_count"), 2),
            (("raw_output", "sample_rate_hz_interpretation"), 44_100),
            (("raw_output", "channel_count_intrinsically_verified"), True),
            (("raw_output", "format_parameters_intrinsically_verified"), True),
            (("raw_output", "output_to_source_duration_ratio_under_mono_contract_interpretation"), 1.3),
            (("response", "response_sha256"), "0" * 64),
            (("raw_output", "path"), "outputs/raw/elevenlabs/wrong.pcm"),
            (("working_output_path",), "outputs/working/elevenlabs/wrong.wav"),
        )
        for key_path, replacement in mutations:
            with self.subTest(key_path=key_path):
                mutated = copy.deepcopy(baseline)
                target = mutated
                for key in key_path[:-1]:
                    target = target[key]
                target[key_path[-1]] = replacement
                self.write_private_json(chain["receipt"], mutated)
                with mock.patch(
                    "oe_narration.voice_transfer.validate_voice_transfer_execution_authorization",
                    return_value={"valid": True},
                    create=True,
                ):
                    with self.assertRaises(ValidationError):
                        inspect_provider_raw_pcm(
                            chain["raw"],
                            chain["receipt"],
                            chain["part_id"],
                        )
        self.write_private_json(chain["receipt"], baseline)
        with mock.patch(
            "oe_narration.voice_transfer.validate_voice_transfer_execution_authorization",
            return_value={"valid": True},
            create=True,
        ):
            with self.assertRaisesRegex(ValidationError, "exact part_id"):
                inspect_provider_raw_pcm(chain["raw"], chain["receipt"], None)

    def test_voice_transfer_rejects_mode_and_symlink_tamper(self) -> None:
        chain = self.make_voice_transfer_chain("transfer-files")
        guarded = (
            (chain["receipt"], "run receipt"),
            (chain["consumption"], "consumption latch"),
            (chain["raw"], "raw PCM"),
        )
        for path, label in guarded:
            with self.subTest(label=label):
                path.chmod(0o644)
                with mock.patch(
                    "oe_narration.voice_transfer.validate_voice_transfer_execution_authorization",
                    return_value={"valid": True},
                    create=True,
                ):
                    with self.assertRaisesRegex(ValidationError, "0600"):
                        inspect_provider_raw_pcm(
                            chain["raw"], chain["receipt"], chain["part_id"]
                        )
                path.chmod(0o600)

        raw_alias = chain["fixture"] / "raw-alias.pcm"
        raw_alias.symlink_to(chain["raw"])
        with self.assertRaisesRegex(ValidationError, "symlink"):
            inspect_provider_raw_pcm(raw_alias, chain["receipt"], chain["part_id"])
        receipt_alias = chain["fixture"] / "receipt-alias.json"
        receipt_alias.symlink_to(chain["receipt"])
        with self.assertRaisesRegex(ValidationError, "symlink"):
            inspect_provider_raw_pcm(chain["raw"], receipt_alias, chain["part_id"])

        latch_path = chain["consumption"]
        real_latch = latch_path.with_name("real-latch.json")
        latch_path.rename(real_latch)
        latch_path.symlink_to(real_latch)
        try:
            with mock.patch(
                "oe_narration.voice_transfer.validate_voice_transfer_execution_authorization",
                return_value={"valid": True},
                create=True,
            ):
                with self.assertRaisesRegex(ValidationError, "symlink"):
                    inspect_provider_raw_pcm(
                        chain["raw"], chain["receipt"], chain["part_id"]
                    )
        finally:
            latch_path.unlink()
            real_latch.rename(latch_path)

    def test_voice_transfer_revalidates_active_and_consumed_before_network_latch(self) -> None:
        chain = self.make_voice_transfer_chain("transfer-authority")
        with mock.patch(
            "oe_narration.voice_transfer.validate_voice_transfer_execution_authorization",
            side_effect=ValidationError("ACTIVE V2 tamper"),
            create=True,
        ):
            with self.assertRaisesRegex(ValidationError, "ACTIVE V2 tamper"):
                inspect_provider_raw_pcm(
                    chain["raw"], chain["receipt"], chain["part_id"]
                )

        chain = self.make_voice_transfer_chain("transfer-mid-validation-tamper")

        def mutate_active(*_args):
            authorization = copy.deepcopy(chain["authorization_value"])
            authorization["approved"] = False
            chain["authorization"].write_text(
                json.dumps(authorization, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )
            return {"valid": True}

        with mock.patch(
            "oe_narration.voice_transfer.validate_voice_transfer_execution_authorization",
            side_effect=mutate_active,
            create=True,
        ):
            with self.assertRaisesRegex(ValidationError, "changed during validation"):
                inspect_provider_raw_pcm(
                    chain["raw"], chain["receipt"], chain["part_id"]
                )

        chain = self.make_voice_transfer_chain("transfer-prerequisite-tamper")
        qa_path = chain["fixture"] / chain["prerequisites"]["guide_qa"]["path"]
        qa_path.write_text('{"tampered":true}\n', encoding="utf-8")
        qa_path.chmod(0o600)
        with mock.patch(
            "oe_narration.voice_transfer.validate_voice_transfer_execution_authorization",
            return_value={"valid": True},
            create=True,
        ):
            with self.assertRaisesRegex(
                ValidationError,
                "prerequisite guide_qa (?:changed|SHA-256 mismatch)",
            ):
                inspect_provider_raw_pcm(
                    chain["raw"], chain["receipt"], chain["part_id"]
                )

        chain = self.make_voice_transfer_chain("transfer-authority-bindings")
        authorization = copy.deepcopy(chain["authorization_value"])
        authorization["approved"] = False
        chain["authorization"].write_text(
            json.dumps(authorization, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        with self.assertRaisesRegex(ValidationError, "authorization SHA-256"):
            inspect_provider_raw_pcm(chain["raw"], chain["receipt"], chain["part_id"])
        chain["authorization"].write_text(
            json.dumps(chain["authorization_value"], indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

        consumption = copy.deepcopy(chain["consumption_value"])
        consumption["status"] = "consumed_after_network"
        self.write_private_json(chain["consumption"], consumption)
        receipt = copy.deepcopy(chain["receipt_value"])
        receipt["consumption_record_sha256"] = sha256_file(chain["consumption"])
        self.write_private_json(chain["receipt"], receipt)
        with mock.patch(
            "oe_narration.voice_transfer.validate_voice_transfer_execution_authorization",
            return_value={"valid": True},
            create=True,
        ):
            with self.assertRaisesRegex(ValidationError, "latch semantics"):
                inspect_provider_raw_pcm(
                    chain["raw"], chain["receipt"], chain["part_id"]
                )

    def test_voice_transfer_rejects_non_headerless_and_out_of_envelope_pcm(self) -> None:
        for name, seconds, header in (
            ("under", 19, None),
            ("over", 51, None),
            ("ratio-low", 27, None),
            ("ratio-high", 42, None),
            ("riff", 34, b"RIFF"),
            ("aiff", 34, b"FORM"),
            ("id3", 34, b"ID3"),
            ("mpeg-frame", 34, b"\xff\xfb"),
            ("flac", 34, b"fLaC"),
            ("ogg", 34, b"OggS"),
            ("matroska", 34, b"\x1aE\xdf\xa3"),
            ("mpeg-program", 34, b"\x00\x00\x01\xba"),
            ("isobmff", 34, b"\x00\x00\x00\x18ftyp"),
        ):
            with self.subTest(name=name):
                chain = self.make_voice_transfer_chain(
                    f"transfer-envelope-{name}",
                    duration_seconds=seconds,
                )
                if header is not None:
                    with chain["raw"].open("r+b") as handle:
                        handle.write(header)
                chain["raw"].chmod(0o600)
                receipt = copy.deepcopy(chain["receipt_value"])
                size = chain["raw"].stat().st_size
                frames = size // 2
                digest = sha256_file(chain["raw"])
                receipt["response"]["response_bytes"] = size
                receipt["response"]["response_sha256"] = digest
                receipt["raw_output"].update(
                    {
                        "sha256": digest,
                        "byte_count": size,
                        "frame_count_under_mono_contract_interpretation": frames,
                        "duration_seconds_under_mono_contract_interpretation": frames
                        / 48_000,
                        "output_to_source_duration_ratio_under_mono_contract_interpretation": (
                            (frames / 48_000)
                            / audio_module._TRANSFER_SELECTED_GUIDE_DURATION_SECONDS
                        ),
                    }
                )
                self.write_private_json(chain["receipt"], receipt)
                with mock.patch(
                    "oe_narration.voice_transfer.validate_voice_transfer_execution_authorization",
                    return_value={"valid": True},
                    create=True,
                ):
                    with self.assertRaises(ValidationError):
                        inspect_provider_raw_pcm(
                            chain["raw"], chain["receipt"], chain["part_id"]
                        )

    def test_voice_transfer_requires_exact_working_and_conversion_destinations(self) -> None:
        for field in ("working", "conversion"):
            with self.subTest(field=field):
                chain = self.make_voice_transfer_chain(f"transfer-path-{field}")
                output = chain["working"]
                record = chain["conversion"]
                if field == "working":
                    output = chain["fixture"] / "wrong-working.wav"
                else:
                    record = chain["fixture"] / "wrong-conversion.json"
                with mock.patch(
                    "oe_narration.voice_transfer.validate_voice_transfer_execution_authorization",
                    return_value={"valid": True},
                    create=True,
                ):
                    with self.assertRaisesRegex(ValidationError, "fixed destination"):
                        convert_working(
                            chain["raw"],
                            output,
                            chain["receipt"],
                            chain["part_id"],
                            record,
                        )

        for field in ("working", "conversion"):
            with self.subTest(symlink=field):
                chain = self.make_voice_transfer_chain(f"transfer-symlink-{field}")
                target = chain["fixture"] / f"existing-{field}"
                target.write_bytes(b"do-not-touch")
                destination = chain[field]
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.symlink_to(target)
                with self.assertRaisesRegex(ValidationError, "symlink"):
                    convert_working(
                        chain["raw"],
                        chain["working"],
                        chain["receipt"],
                        chain["part_id"],
                        chain["conversion"],
                    )
                self.assertEqual(target.read_bytes(), b"do-not-touch")

    def test_voice_transfer_receipt_rejects_duplicate_json_members(self) -> None:
        chain = self.make_voice_transfer_chain("transfer-duplicate-json")
        original = chain["receipt"].read_text(encoding="utf-8")
        duplicated = original.replace(
            '"schema_version": "oe-elevenlabs-voice-transfer-run-v1",',
            '"schema_version": "oe-elevenlabs-voice-transfer-run-v1",\n'
            '  "schema_version": "oe-elevenlabs-voice-transfer-run-v1",',
            1,
        )
        chain["receipt"].write_text(duplicated, encoding="utf-8")
        chain["receipt"].chmod(0o600)
        with self.assertRaisesRegex(ValidationError, "duplicate JSON member"):
            inspect_provider_raw_pcm(chain["raw"], chain["receipt"], chain["part_id"])

    def test_renamed_mp3_is_detected_by_codec(self) -> None:
        actual = self.make_mp3("actual.mp3", "192k")
        renamed = self.root / "renamed.wav"
        renamed.write_bytes(actual.read_bytes())
        info = inspect_audio(renamed)
        self.assertEqual(info["codec_name"], "mp3")
        self.assertFalse(info["is_working_master"])

    def test_128k_mp3_is_rejected(self) -> None:
        raw = self.make_mp3("raw-128.mp3", "128k")
        with self.assertRaisesRegex(ValidationError, "exactly 44.1 kHz and 192 kbps"):
            convert_working(raw, self.root / "working.wav", self.failure_receipt(raw))

    def test_192k_mp3_requires_capability_receipt_and_persists_lossy_origin(self) -> None:
        raw = self.make_mp3("raw-192.mp3", "192k")
        with self.assertRaisesRegex(ValidationError, "requires an actual PCM"):
            convert_working(raw, self.root / "no-receipt.wav")
        receipt = self.failure_receipt(raw)
        result = convert_working(raw, self.root / "working.wav", receipt)
        self.assertTrue(result["lossy_origin"])
        self.assertEqual(result["conversion_count_from_raw"], 1)
        self.assertTrue(result["working"]["is_working_master"])
        self.assertEqual(sha256_file(raw), result["raw_immutable_sha256"])

    def test_directed_run_receipt_does_not_replace_mp3_capability_receipt(self) -> None:
        raw = self.make_mp3("directed-fallback.mp3", "192k")
        directed = self.root / "directed-run.json"
        directed.write_text(
            json.dumps(
                {"schema_version": "oe-elevenlabs-directed-bakeoff-run-v1"}
            ),
            encoding="utf-8",
        )
        with self.assertRaisesRegex(ValidationError, "fallback receipt must use"):
            convert_working(raw, self.root / "working.wav", directed, "EL-P01-A")

    def test_auth_rate_limit_timeout_or_server_receipt_cannot_enable_fallback(self) -> None:
        raw = self.make_mp3("raw.mp3", "192k")
        for status, kind in ((401, "auth"), (408, "timeout"), (429, "rate_limit"), (500, "server")):
            receipt = self.failure_receipt(raw, status, kind)
            with self.assertRaises(ValidationError, msg=f"{status}/{kind}"):
                validate_pcm_failure_receipt(receipt, raw)

    def test_native_headerless_pcm_converts_with_hashed_capture_receipt(self) -> None:
        raw = self.root / "part.provider-raw.pcm"
        samples = [int(8000 * ((index % 50) / 50.0 - 0.5)) for index in range(48_000)]
        raw.write_bytes(b"".join(struct.pack("<h", sample) for sample in samples))
        receipt = self.root / "capture-run-receipt.json"
        receipt.write_text(
            json.dumps(
                {
                    "schema_version": "oe-provider-capture-run-v1",
                    "results": [
                        {
                            "part_id": "part",
                            "requested_output_format": "pcm_48000",
                            "actual_codec": "pcm_s16le",
                            "container": "raw",
                            "sample_rate_hz": 48000,
                            "channels": 1,
                            "bit_depth": 16,
                            "raw_sha256": sha256_file(raw),
                            "lossy_origin": False,
                        }
                    ],
                }
            ),
            encoding="utf-8",
        )
        inspected = inspect_provider_raw_pcm(raw, receipt, "part")
        self.assertEqual(inspected["codec_name"], "pcm_s16le")
        result = convert_working(raw, self.root / "native-working.wav", receipt, "part")
        self.assertFalse(result["lossy_origin"])
        self.assertTrue(result["working"]["is_working_master"])

    def test_recovery_evidence_conversion_is_distinct_one_time_and_private(self) -> None:
        raw = self.root / "saved-c-transfer.pcm"
        raw.write_bytes(b"\x01\x00" * (48_000 * 30))
        raw.chmod(0o600)
        run = self.root / "run.json"
        run.write_text("{}\n", encoding="utf-8")
        run.chmod(0o600)
        working = self.root / "saved-c-transfer.wav"
        record = self.root / "conversion.json"
        source = {
            "path": str(raw),
            "sha256": sha256_file(raw),
            "byte_count": raw.stat().st_size,
            "requested_output_format": "pcm_48000",
            "container_interpretation": "raw",
            "codec_interpretation": "pcm_s16le",
            "sample_rate_hz_interpretation": 48_000,
            "channel_count_interpretation": 1,
            "bit_depth_interpretation": 16,
            "frame_count_under_mono_contract_interpretation": 48_000 * 30,
            "duration_seconds_under_mono_contract_interpretation": 30.0,
            "output_to_source_duration_ratio_under_mono_contract_interpretation": 1.0,
            "format_parameters_intrinsically_verified": False,
            "channel_count_intrinsically_verified": False,
            "frame_and_duration_computed_under_mono_contract_interpretation": True,
            "lossy_interpretation": False,
            "capture_receipt_schema_version": (
                "oe-elevenlabs-recovery-evidence-voice-transfer-run-v1"
            ),
            "capture_receipt_sha256": sha256_file(run),
            "part_id": "P01-W0030-W0110",
            "authorization_sha256": "a" * 64,
            "consumption_record_sha256": "b" * 64,
            "authorized_working_output_path": str(working),
            "authorized_conversion_receipt_path": str(record),
        }
        runtime = {
            "ffmpeg_binary_path": "/usr/bin/false",
            "ffmpeg_binary_sha256": "c" * 64,
            "ffmpeg_version": "unit",
            "ffprobe_binary_path": "/usr/bin/false",
            "ffprobe_binary_sha256": "d" * 64,
            "ffprobe_version": "unit",
        }

        def inspect_raw(*_args, _runtime_bindings_out=None, **_kwargs):
            _runtime_bindings_out.update(runtime)
            return copy.deepcopy(source)

        def media_run(tool, command, _runtime, *, pass_fds=(), **_kwargs):
            if tool == "ffmpeg":
                os.write(pass_fds[0], b"unit-private-working-wave")
            return subprocess.CompletedProcess(command, 0, "", "")

        def inspect_converted(path, **_kwargs):
            return {
                "path": str(path),
                "sha256": sha256_file(path),
                "codec_name": "pcm_s24le",
                "container": "wav",
                "sample_rate_hz": 48_000,
                "channels": 1,
                "bit_depth": 24,
                "bit_rate_bps": 1_152_000,
                "duration_seconds": 30.0,
                "origin_class": "native_pcm",
                "is_approved_mp3_fallback": False,
                "is_working_master": True,
            }

        with (
            mock.patch.object(
                audio_module,
                "inspect_recovery_evidence_raw_pcm",
                side_effect=inspect_raw,
            ) as inspect_source,
            mock.patch.object(
                audio_module,
                "_run_transfer_media_tool",
                side_effect=media_run,
            ),
            mock.patch.object(audio_module, "inspect_audio", side_effect=inspect_converted),
            mock.patch.object(audio_module, "_validate_full_decode"),
        ):
            result = convert_recovery_evidence_working(
                raw,
                working,
                receipt_path=run,
                part_id="P01-W0030-W0110",
                record_path=record,
            )
            with self.assertRaisesRegex(ValidationError, "failed closed"):
                convert_recovery_evidence_working(
                    raw,
                    working,
                    receipt_path=run,
                    part_id="P01-W0030-W0110",
                    record_path=record,
                )

        inspect_source.assert_called_once()
        self.assertEqual(
            result["schema_version"],
            "oe-elevenlabs-recovery-evidence-voice-transfer-conversion-v1",
        )
        self.assertEqual(result["conversion_count_from_raw"], 1)
        self.assertEqual(result["raw_immutable_sha256"], sha256_file(raw))
        self.assertFalse(result["lossy_interpretation"])
        for path in (working, record):
            self.assertTrue(path.is_file())
            self.assertEqual(stat.S_IMODE(path.stat().st_mode), 0o600)
        persisted = json.loads(record.read_text(encoding="utf-8"))
        self.assertEqual(persisted["schema_version"], result["schema_version"])
        self.assertFalse(persisted["creative_approved"])
        self.assertFalse(persisted["step2_lock_authorized"])
        self.assertFalse(persisted["step3_authorized"])
        self.assertFalse(persisted["sharing_authorized"])
        self.assertFalse(persisted["publication_authorized"])

    def test_recovery_evidence_source_replay_binds_committed_active_and_semantics(self) -> None:
        repository = performance_transfer_module._guide_repository_root()
        temporary = tempfile.TemporaryDirectory(dir=repository)
        self.addCleanup(temporary.cleanup)
        fixture = Path(temporary.name).resolve()
        authorization_path = fixture / "authorizations" / "unit.ACTIVE.json"
        latch_path = fixture / voice_transfer_module.TRANSFER_SCOPE_LATCH_PATH
        run_path = fixture / "receipts" / "elevenlabs" / "unit.run.json"
        for path in (authorization_path, latch_path, run_path):
            path.parent.mkdir(parents=True, exist_ok=True)
        evidence_commit = "c" * 40
        active_commit = "d" * 40
        runtime_commit = "e" * 40
        authorization_id = voice_transfer_module.RECOVERY_TRANSFER_ACTIVE_ID
        authorization = {
            "schema_version": voice_transfer_module.RECOVERY_TRANSFER_AUTH_SCHEMA,
            "authorization_id": authorization_id,
            "status": "active",
            "provider_action_authorized": True,
            "scope": "elevenlabs_recovery_evidence_voice_transfer_execution",
            "artifacts": voice_transfer_module._recovery_transfer_artifacts(True),
            "consumption": voice_transfer_module._recovery_transfer_consumption(True),
            "runtime_bindings": {"state": "verified"},
            "evidence_baseline": {"evidence_commit": evidence_commit},
        }
        authorization_path.write_text(
            json.dumps(authorization, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        authorization_path.chmod(0o600)
        latch = {
            "schema_version": voice_transfer_module.RECOVERY_TRANSFER_CONSUMPTION_SCHEMA,
            "authorization_id": authorization_id,
            "generation_post_budget_consumed": True,
            "retry_or_replay_permitted": False,
        }
        latch_path.write_text(json.dumps(latch, sort_keys=True) + "\n", encoding="utf-8")
        latch_path.chmod(0o600)
        receipt = {
            "authorization_path": authorization_path.relative_to(fixture).as_posix(),
            "authorization_id": authorization_id,
            "authorization_sha256": sha256_file(authorization_path),
            "consumption_record_path": latch_path.relative_to(fixture).as_posix(),
            "consumption_record_sha256": sha256_file(latch_path),
            "source_proof": {
                "active_commit": active_commit,
                "runtime_commit": runtime_commit,
                "evidence_commit": evidence_commit,
                "source_revalidated_after_latch": True,
                "post_latch_revalidation_completed": True,
                "remote_state_checked": False,
                "git_network_called": False,
            },
        }
        run_path.write_text(json.dumps(receipt, sort_keys=True) + "\n", encoding="utf-8")
        run_path.chmod(0o600)
        receipt_bound = audio_module._open_bound_input(
            run_path,
            "unit recovery run",
            byte_cap=audio_module._TRANSFER_JSON_BYTE_CAP,
            required_mode=0o600,
        )
        held = [receipt_bound]
        runtime = {"git_commit": runtime_commit}
        authorization_relative = authorization_path.relative_to(repository).as_posix()
        latch_relative = latch_path.relative_to(repository).as_posix()
        run_relative = run_path.relative_to(repository).as_posix()
        raw_relative = (fixture / audio_module._TRANSFER_RAW_PATH).relative_to(
            repository
        ).as_posix()

        def bound_git(_runtime, arguments, **_kwargs):
            if arguments == ["rev-parse", "HEAD"]:
                return (active_commit + "\n").encode()
            if arguments[:3] == ["rev-list", "--parents", "-n"]:
                return f"{active_commit} {evidence_commit}\n".encode()
            if arguments and arguments[0] == "diff":
                return b"A\x00" + authorization_relative.encode() + b"\x00"
            if arguments and arguments[0] == "show":
                return authorization_path.read_bytes()
            raise AssertionError(arguments)

        plan_bound = SimpleNamespace(path=fixture / "performance-transfer-plan.json")
        canonical_bound = SimpleNamespace(
            path=fixture / "passages" / "P01-W0030-W0110.locked.txt"
        )
        semantic_result = {
            "valid": True,
            "authorization_status": "active",
            "provider_action_authorized": True,
            "authorization_sha256": sha256_file(authorization_path),
        }
        try:
            with (
                mock.patch.object(
                    performance_transfer_module,
                    "_document_root",
                    return_value=fixture,
                ),
                mock.patch.object(
                    voice_transfer_module,
                    "_validate_recovery_transfer_runtime_bindings",
                    return_value=runtime,
                ),
                mock.patch.object(
                    voice_transfer_module,
                    "_bound_git",
                    side_effect=bound_git,
                ),
                mock.patch.object(
                    audio_module,
                    "_transfer_canonical_w_inputs",
                    return_value=(plan_bound, canonical_bound),
                ),
                mock.patch.object(
                    voice_transfer_module,
                    "validate_recovery_evidence_voice_transfer_authorization",
                    return_value=semantic_result,
                ) as validate_active,
            ):
                root, _authorization, _runtime, _active_bound, _latch_bound = (
                    audio_module._replay_recovery_evidence_source_proof(
                        receipt,
                        receipt_bound,
                        held,
                    )
                )
            self.assertEqual(root, fixture)
            validate_active.assert_called_once_with(
                authorization_path,
                plan_bound.path,
                canonical_bound.path,
                _allowed_generated_status_paths=frozenset(
                    {latch_relative, run_relative}
                ),
                _allowed_ignored_generated_paths=frozenset({raw_relative}),
            )

            forged_bound = audio_module._open_bound_input(
                run_path,
                "unit forged recovery run",
                byte_cap=audio_module._TRANSFER_JSON_BYTE_CAP,
                required_mode=0o600,
            )
            forged_held = [forged_bound]

            def forged_git(_runtime, arguments, **kwargs):
                if arguments and arguments[0] == "show":
                    return b"{}\n"
                return bound_git(_runtime, arguments, **kwargs)

            try:
                with (
                    mock.patch.object(
                        performance_transfer_module,
                        "_document_root",
                        return_value=fixture,
                    ),
                    mock.patch.object(
                        voice_transfer_module,
                        "_validate_recovery_transfer_runtime_bindings",
                        return_value=runtime,
                    ),
                    mock.patch.object(
                        voice_transfer_module,
                        "_bound_git",
                        side_effect=forged_git,
                    ),
                ):
                    with self.assertRaisesRegex(
                        ValidationError,
                        "committed ACTIVE proof",
                    ):
                        audio_module._replay_recovery_evidence_source_proof(
                            receipt,
                            forged_bound,
                            forged_held,
                        )
            finally:
                for bound in reversed(forged_held):
                    audio_module._close_bound_input(bound)
        finally:
            for bound in reversed(held):
                audio_module._close_bound_input(bound)

    def test_recovery_additions_preserve_frozen_legacy_audio_functions(self) -> None:
        expected = {
            "_validate_transfer_provider_evidence": "bec29f295052b10cbb835d43b0d10084bd0ea6c4809ec0da8a578b6d8346aa46",
            "_replay_transfer_source_proof": "c2818c8d4bc4aebf3568344a772569635aaf4f9c2dfd7c17029d2ff5ec68463f",
            "_transfer_canonical_w_inputs": "c7ff45761cca05606c2123a92434d8fc3fc765b7431c37a443234ae29e151171",
            "_inspect_voice_transfer_raw_pcm": "44be09b928220b2aa8638a670c7df4fe764512d71fb613275f72b1af40b613e2",
            "_inspect_voice_transfer_raw_pcm_impl": "db73fd30248b358d575f6b356692cc4526093661c8c2d428c396ae44efa4cf3f",
            "inspect_provider_raw_pcm": "1a34031e89cb31098794d44e9a1d96fc88e552615b7dd66ca24617b65cd68fca",
            "convert_working": "a15b21b15cc47c0749ac0e4f1dad2e467b9cea822faf976a1bc7cece9e72db39",
            "_convert_working_impl": "f24530cf46be6529c7270386e0fd986c063fb214f79d102e2651e11a2e0d5571",
        }
        source = Path(audio_module.__file__).read_text(encoding="utf-8")
        nodes = {
            node.name: node
            for node in ast.parse(source).body
            if isinstance(node, ast.FunctionDef)
        }
        actual = {
            name: sha256_bytes(ast.get_source_segment(source, nodes[name]).encode())
            for name in expected
        }
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
