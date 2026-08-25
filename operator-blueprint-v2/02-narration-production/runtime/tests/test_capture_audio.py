from __future__ import annotations

import json
import io
import struct
import subprocess
import tempfile
import unittest
import urllib.error
from pathlib import Path
from unittest import mock

from oe_narration.audio import (
    convert_working,
    inspect_audio,
    inspect_provider_raw_pcm,
    validate_pcm_failure_receipt,
)
from oe_narration.cli import build_parser
from oe_narration.core import (
    ValidationError,
    canonical_w_bytes,
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
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name).resolve()

    def tearDown(self) -> None:
        self.temp.cleanup()

    def make_mp3(self, name: str, bitrate: str) -> Path:
        path = self.root / name
        run_ffmpeg(["-f", "lavfi", "-i", "sine=frequency=440:duration=1", "-ar", "44100", "-ac", "1", "-b:a", bitrate, str(path)])
        return path

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


if __name__ == "__main__":
    unittest.main()
