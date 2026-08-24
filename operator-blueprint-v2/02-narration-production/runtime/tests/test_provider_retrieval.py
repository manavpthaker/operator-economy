from __future__ import annotations

import json
import io
import os
import stat
import shutil
import tempfile
import unittest
import urllib.error
import wave
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest import mock

from oe_narration.core import ValidationError, sha256_bytes, sha256_file
from oe_narration.cli import build_parser, dispatch
from oe_narration.retrieval import (
    MAX_AUTHORIZED_DOWNLOAD_BYTES,
    dry_run_metadata_inventory,
    dry_run_retrieval,
    execute_metadata_inventory,
    execute_retrieval,
)


class _FakeResponse:
    def __init__(
        self,
        data: bytes,
        *,
        content_type: str,
        url: str = "",
        content_length: int | None = None,
        headers: dict[str, str] | None = None,
        status: int = 200,
    ) -> None:
        self._data = data
        self._url = url
        self.status = status
        self.headers = {
            "Content-Type": content_type,
            **({"Content-Length": str(len(data) if content_length is None else content_length)}),
            **(headers or {}),
        }

    def __enter__(self) -> _FakeResponse:
        return self

    def __exit__(self, exc_type, exc, traceback) -> bool:
        return False

    def read(self, size: int = -1) -> bytes:
        return self._data if size < 0 else self._data[:size]

    def geturl(self) -> str:
        return self._url


class ProviderRetrievalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.narration_root = Path(__file__).resolve().parents[2]
        matches = sorted(
            (cls.narration_root / "fixtures").glob("step2-v0.3-*-provider-bakeoff")
        )
        if len(matches) != 1:
            raise AssertionError(f"expected one v0.3 provider bakeoff fixture, found {matches}")
        cls.source_fixture = matches[0]
        cls.source_w = (
            cls.narration_root
            / "fixtures"
            / "step2-v0.2-ai-visibility-v1.1"
            / "identity"
            / "canonical-w.txt"
        )
        cls.source_script = (
            cls.narration_root.parent
            / "01-editorial"
            / "fixtures"
            / "step1-v1.4-e2e-ai-visibility-2026-08-22"
            / "122-script-v1.1-HORIZONTAL-PITCH-CANDIDATE.md"
        )

    def _write_json(self, path: Path, value: dict) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    def _active_authorization(self) -> tuple[tempfile.TemporaryDirectory, Path, Path]:
        temporary = tempfile.TemporaryDirectory()
        blueprint = Path(temporary.name) / "operator-blueprint-v2"
        fixture = (
            blueprint
            / "02-narration-production"
            / "fixtures"
            / self.source_fixture.name
        )
        fixture.parent.mkdir(parents=True)
        # The canonical fixture may contain ignored, post-execution local
        # evidence. Tests must never inspect, copy into assertions, or mutate
        # those records, so build from the tracked contract surface only.
        shutil.copytree(
            self.source_fixture,
            fixture,
            ignore=shutil.ignore_patterns(
                "local-media", "receipts", "consumed", "*.ACTIVE.*"
            ),
        )
        identity = (
            blueprint
            / "02-narration-production"
            / "fixtures"
            / "step2-v0.2-ai-visibility-v1.1"
            / "identity"
        )
        identity.mkdir(parents=True)
        shutil.copy2(self.source_w, identity / "canonical-w.txt")
        script = (
            blueprint
            / "01-editorial"
            / "fixtures"
            / "step1-v1.4-e2e-ai-visibility-2026-08-22"
            / self.source_script.name
        )
        script.parent.mkdir(parents=True)
        shutil.copy2(self.source_script, script)

        auth_path = (
            fixture
            / "authorizations"
            / "01-elevenlabs-read-only-metadata-sample.DRAFT.json"
        )
        authorization = json.loads(auth_path.read_text(encoding="utf-8"))
        voice_id = authorization["action"]["voice_id"]
        now = datetime.now(timezone.utc)
        authorization.update(
            {
                "authorization_id": "AUTH-01-test-one-shot-retrieval",
                "status": "active",
                "approved": True,
                "execution_ready": True,
                "blockers": [],
                "approved_by": "Manav",
                "approved_at": (now - timedelta(minutes=1)).isoformat(),
                "expires_at": (now + timedelta(hours=1)).isoformat(),
            }
        )
        rights = fixture / "receipts" / "voice-rights.json"
        rights.parent.mkdir(parents=True)
        rights.write_text('{"owner":"Manav","retrieval":true}\n', encoding="utf-8")
        authorization["action"].update(
            {
                "metadata_endpoint": f"https://api.elevenlabs.io/v1/voices/{voice_id}",
                "sample_ids": [],
                "destinations": ["local-media/elevenlabs/original-source.bin"],
                "sample_selection_rule": "only_single_original_human_sample_attached_to_bound_voice",
                "selection_fails_if_zero_or_multiple_samples": True,
                "selection_fails_if_mixed_speaker": True,
                "metadata_must_confirm_original_human_source": True,
                "metadata_receipt_destination": "receipts/elevenlabs/metadata.json",
                "selected_sample_receipt_destination": "receipts/elevenlabs/selected-sample.json",
                "rights_and_consent": {
                    "voice_owner": "Manav",
                    "provider_disclosure_approved": True,
                    "record_path": "receipts/voice-rights.json",
                    "record_sha256": sha256_file(rights),
                },
            }
        )
        authorization["authorized_limits"] = {
            "max_calls": 2,
            "max_downloads": 1,
            "max_download_bytes": MAX_AUTHORIZED_DOWNLOAD_BYTES,
            "max_spend_usd": 0,
        }
        authorization["consumption"].update(
            {
                "status": "unconsumed",
                "calls_used": 0,
                "downloads_used": 0,
                "spend_used_usd": 0,
                "record_path": "consumed/AUTH-01.json",
            }
        )
        self._write_json(auth_path, authorization)
        return temporary, fixture, auth_path

    def _active_inventory_authorization(
        self,
    ) -> tuple[tempfile.TemporaryDirectory, Path, Path]:
        temporary, fixture, auth_path = self._active_authorization()
        authorization = json.loads(auth_path.read_text(encoding="utf-8"))
        voice_id = authorization["action"]["voice_id"]
        authorization["authorization_id"] = "AUTH-01B-test-metadata-inventory"
        authorization["scope"] = "elevenlabs_sample_metadata_inventory"
        authorization["action"] = {
            "kind": "read_only_voice_metadata_inventory",
            "voice_id": voice_id,
            "metadata_endpoint": f"https://api.elevenlabs.io/v1/voices/{voice_id}",
            "metadata_receipt_destination": "receipts/elevenlabs/inventory.json",
            "selection_permitted": False,
            "download_permitted": False,
            "raw_payload_storage_permitted": False,
        }
        authorization["requested_limits"] = {
            "max_metadata_calls": 1,
            "max_sample_download_calls": 0,
            "max_metadata_response_bytes": 2_000_000,
            "max_spend_usd": 0,
        }
        authorization["authorized_limits"] = {
            "max_calls": 1,
            "max_downloads": 0,
            "max_metadata_response_bytes": 2_000_000,
            "max_spend_usd": 0,
        }
        authorization["consumption"] = {
            "status": "unconsumed",
            "calls_used": 0,
            "downloads_used": 0,
            "spend_used_usd": 0,
            "record_path": "consumed/AUTH-01B.json",
        }
        self._write_json(auth_path, authorization)
        return temporary, fixture, auth_path

    @staticmethod
    def _metadata_bytes(samples: list[dict], voice_id: str) -> bytes:
        return json.dumps({"voice_id": voice_id, "samples": samples}).encode("utf-8")

    @staticmethod
    def _wav_bytes() -> bytes:
        buffer = io.BytesIO()
        with wave.open(buffer, "wb") as output:
            output.setnchannels(1)
            output.setsampwidth(2)
            output.setframerate(48_000)
            output.writeframes(b"\x00\x00" * 16)
        return buffer.getvalue()

    def _success_responses(self, auth_path: Path, audio: bytes | None = None):
        authorization = json.loads(auth_path.read_text(encoding="utf-8"))
        metadata_url = authorization["action"]["metadata_endpoint"]
        sample_id = "sample-original-001"
        sample_url = f"{metadata_url}/samples/{sample_id}/audio"
        if audio is None:
            audio = self._wav_bytes()
        metadata = self._metadata_bytes(
            [{"sample_id": sample_id, "file_name": "owner.wav"}],
            authorization["action"]["voice_id"],
        )
        return [
            _FakeResponse(
                metadata,
                content_type="application/json",
                url=metadata_url,
                headers={"xi-request-id": "meta-request-1"},
            ),
            _FakeResponse(
                audio,
                content_type="audio/wav",
                url=sample_url,
                headers={"request-id": "sample-request-1"},
            ),
        ]

    def test_default_is_credential_free_dry_run(self) -> None:
        temporary, fixture, auth_path = self._active_authorization()
        self.addCleanup(temporary.cleanup)
        with mock.patch.dict(os.environ, {}, clear=True), mock.patch(
            "oe_narration.retrieval._open_request"
        ) as opened:
            result = dry_run_retrieval(auth_path)
        self.assertEqual(result["mode"], "dry-run")
        self.assertFalse(result["network_called"])
        self.assertFalse(result["credentials_accessed"])
        self.assertEqual(result["provider_calls_made"], 0)
        opened.assert_not_called()
        self.assertFalse((auth_path.parent / "consumed" / "AUTH-01.json").exists())

    def test_execute_missing_key_does_not_consume_or_call(self) -> None:
        temporary, fixture, auth_path = self._active_authorization()
        self.addCleanup(temporary.cleanup)
        with mock.patch.dict(os.environ, {}, clear=True), mock.patch(
            "oe_narration.retrieval._open_request"
        ) as opened:
            with self.assertRaisesRegex(ValidationError, "required only for authorized"):
                execute_retrieval(auth_path)
        opened.assert_not_called()
        self.assertFalse((auth_path.parent / "consumed" / "AUTH-01.json").exists())

    def test_cli_defaults_to_same_credential_free_executor_preflight(self) -> None:
        temporary, fixture, auth_path = self._active_authorization()
        self.addCleanup(temporary.cleanup)
        args = build_parser().parse_args(
            ["retrieve-elevenlabs-sample", "--authorization", str(auth_path)]
        )
        self.assertFalse(args.execute)
        with mock.patch.dict(os.environ, {}, clear=True), mock.patch(
            "oe_narration.retrieval._open_request"
        ) as opened:
            result = dispatch(args)
        self.assertTrue(result["executor_preflight"]["valid"])
        self.assertEqual(
            result["executor_preflight"]["authorized_limits"]["max_calls"], 2
        )
        self.assertEqual(
            result["executor_preflight"]["sample_request"]["endpoint"],
            "derived_after_exactly_one_sample_id_is_selected",
        )
        opened.assert_not_called()

    def test_consumed_gate_and_wrong_endpoint_fail_before_network(self) -> None:
        for mutation in ("consumed", "wrong_endpoint"):
            with self.subTest(mutation=mutation):
                temporary, fixture, auth_path = self._active_authorization()
                self.addCleanup(temporary.cleanup)
                authorization = json.loads(auth_path.read_text(encoding="utf-8"))
                if mutation == "consumed":
                    authorization["consumption"]["status"] = "consumed"
                else:
                    authorization["action"]["metadata_endpoint"] += "/samples"
                self._write_json(auth_path, authorization)
                with mock.patch.dict(
                    os.environ, {"ELEVENLABS_API_KEY": "test-secret"}, clear=True
                ), mock.patch("oe_narration.retrieval._open_request") as opened:
                    with self.assertRaises(ValidationError):
                        execute_retrieval(auth_path)
                opened.assert_not_called()

    def test_zero_or_multiple_samples_stops_after_one_call_with_receipt(self) -> None:
        multiple = [
            {
                "sample_id": "a",
                "file_name": "../../owner-a.wav",
                "mime_type": "audio/wav",
                "category": "cloned",
                "source": "user_upload",
                "hash": "provider-hash-a",
                "size_bytes": 123,
                "is_generated": False,
                "is_original": True,
            },
            {
                "sample_id": "b",
                "file_name": "test-secret-do-not-store.wav",
                "source": "test-secret-do-not-store",
            },
        ]
        for samples, expected_reason in (([], "zero_samples"), (multiple, "multiple_samples")):
            with self.subTest(expected_reason=expected_reason):
                temporary, fixture, auth_path = self._active_authorization()
                self.addCleanup(temporary.cleanup)
                authorization = json.loads(auth_path.read_text(encoding="utf-8"))
                metadata_url = authorization["action"]["metadata_endpoint"]
                data = self._metadata_bytes(samples, authorization["action"]["voice_id"])
                response = _FakeResponse(
                    data,
                    content_type="application/json",
                    url=metadata_url,
                    headers={"x-request-id": "selection-request"},
                )
                with mock.patch.dict(
                    os.environ, {"ELEVENLABS_API_KEY": "test-secret"}, clear=True
                ), mock.patch(
                    "oe_narration.retrieval._open_request", return_value=response
                ) as opened:
                    with self.assertRaisesRegex(ValidationError, expected_reason):
                        execute_retrieval(auth_path)
                self.assertEqual(opened.call_count, 1)
                receipt_path = fixture / authorization["action"]["metadata_receipt_destination"]
                receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
                self.assertEqual(receipt["reason"], expected_reason)
                self.assertEqual(receipt["attempted_calls"], 1)
                self.assertEqual(receipt["provider_identifiers"]["x-request-id"], "selection-request")
                self.assertEqual(receipt["outcome"], "failed_closed")
                evidence = receipt["metadata_evidence"]
                self.assertEqual(evidence["voice_id"], authorization["action"]["voice_id"])
                self.assertEqual(evidence["sample_count"], len(samples))
                self.assertEqual(evidence["response"]["mime_type"], "application/json")
                self.assertEqual(evidence["response"]["byte_count"], len(data))
                self.assertEqual(evidence["response"]["sha256"], sha256_bytes(data))
                self.assertFalse(evidence["selection_made"])
                self.assertFalse(evidence["download_attempted"])
                self.assertEqual(len(evidence["samples"]), len(samples))
                if expected_reason == "multiple_samples":
                    self.assertEqual(
                        [item["sample_id"] for item in evidence["samples"]], ["a", "b"]
                    )
                    self.assertEqual(
                        evidence["samples"][0]["original_filename"], "owner-a.wav"
                    )
                    self.assertEqual(evidence["samples"][0]["category"], "cloned")
                    self.assertEqual(evidence["samples"][0]["source"], "user_upload")
                    self.assertEqual(evidence["samples"][0]["declared_mime_type"], "audio/wav")
                    self.assertEqual(evidence["samples"][0]["provider_size_bytes"], 123)
                    self.assertFalse(evidence["samples"][0]["is_generated"])
                    self.assertTrue(evidence["samples"][0]["is_original"])
                    self.assertIsNone(evidence["samples"][1]["original_filename"])
                    self.assertIsNone(evidence["samples"][1]["source"])
                    self.assertNotIn(
                        "test-secret-do-not-store",
                        receipt_path.read_text(encoding="utf-8"),
                    )
                self.assertFalse((fixture / authorization["action"]["destinations"][0]).exists())

    def test_download_cap_overrun_and_size_ambiguity_fail_closed(self) -> None:
        for mode in ("cap", "ambiguous"):
            with self.subTest(mode=mode):
                temporary, fixture, auth_path = self._active_authorization()
                self.addCleanup(temporary.cleanup)
                authorization = json.loads(auth_path.read_text(encoding="utf-8"))
                authorization["authorized_limits"]["max_download_bytes"] = 10
                self._write_json(auth_path, authorization)
                responses = self._success_responses(auth_path, b"short")
                if mode == "cap":
                    responses[1].headers["Content-Length"] = "11"
                    expected = "authorized_size_ceiling_exceeded"
                else:
                    responses[1].headers.pop("Content-Length")
                    expected = "response_size_ambiguous"
                with mock.patch.dict(
                    os.environ, {"ELEVENLABS_API_KEY": "test-secret"}, clear=True
                ), mock.patch(
                    "oe_narration.retrieval._open_request", side_effect=responses
                ) as opened:
                    with self.assertRaisesRegex(ValidationError, expected):
                        execute_retrieval(auth_path)
                self.assertEqual(opened.call_count, 2)
                failure_path = fixture / authorization["action"]["selected_sample_receipt_destination"]
                failure = json.loads(failure_path.read_text(encoding="utf-8"))
                self.assertEqual(failure["reason"], expected)
                self.assertFalse((fixture / authorization["action"]["destinations"][0]).exists())

    def test_cap_above_absolute_ceiling_and_existing_destination_never_call(self) -> None:
        for mutation in ("oversized_cap", "existing_destination"):
            with self.subTest(mutation=mutation):
                temporary, fixture, auth_path = self._active_authorization()
                self.addCleanup(temporary.cleanup)
                authorization = json.loads(auth_path.read_text(encoding="utf-8"))
                if mutation == "oversized_cap":
                    authorization["authorized_limits"]["max_download_bytes"] = MAX_AUTHORIZED_DOWNLOAD_BYTES + 1
                    self._write_json(auth_path, authorization)
                else:
                    destination = fixture / authorization["action"]["destinations"][0]
                    destination.parent.mkdir(parents=True)
                    destination.write_bytes(b"do-not-overwrite")
                with mock.patch.dict(
                    os.environ, {"ELEVENLABS_API_KEY": "test-secret"}, clear=True
                ), mock.patch("oe_narration.retrieval._open_request") as opened:
                    with self.assertRaises(ValidationError):
                        execute_retrieval(auth_path)
                opened.assert_not_called()

    def test_dry_run_rejects_oversized_cap_and_nonzero_spend_like_execute(self) -> None:
        for field, value, expected in (
            ("max_download_bytes", MAX_AUTHORIZED_DOWNLOAD_BYTES + 1, "between 1"),
            ("max_spend_usd", 99, "exactly 0"),
        ):
            with self.subTest(field=field):
                temporary, fixture, auth_path = self._active_authorization()
                self.addCleanup(temporary.cleanup)
                authorization = json.loads(auth_path.read_text(encoding="utf-8"))
                authorization["authorized_limits"][field] = value
                self._write_json(auth_path, authorization)
                with mock.patch.dict(os.environ, {}, clear=True), mock.patch(
                    "oe_narration.retrieval._open_request"
                ) as opened:
                    with self.assertRaisesRegex(ValidationError, expected):
                        dry_run_retrieval(auth_path)
                opened.assert_not_called()

    def test_symlinked_authorized_prefix_is_rejected_before_consumption(self) -> None:
        temporary, fixture, auth_path = self._active_authorization()
        self.addCleanup(temporary.cleanup)
        escape = fixture / "receipts" / "media-escape"
        escape.mkdir(parents=True)
        (fixture / "local-media").symlink_to(escape, target_is_directory=True)
        with mock.patch.dict(
            os.environ, {"ELEVENLABS_API_KEY": "test-secret"}, clear=True
        ), mock.patch("oe_narration.retrieval._open_request") as opened:
            with self.assertRaisesRegex(ValidationError, "symlink"):
                execute_retrieval(auth_path)
        opened.assert_not_called()
        self.assertFalse((auth_path.parent / "consumed" / "AUTH-01.json").exists())
        self.assertEqual(list(escape.iterdir()), [])

    def test_empty_or_fake_audio_body_is_blocked_and_receipted(self) -> None:
        for audio, expected in (
            (b"", "sample_audio_empty"),
            (b"<html>not audio</html>", "sample_audio_signature_unrecognized"),
        ):
            with self.subTest(expected=expected):
                temporary, fixture, auth_path = self._active_authorization()
                self.addCleanup(temporary.cleanup)
                authorization = json.loads(auth_path.read_text(encoding="utf-8"))
                responses = self._success_responses(auth_path, audio)
                with mock.patch.dict(
                    os.environ, {"ELEVENLABS_API_KEY": "test-secret"}, clear=True
                ), mock.patch(
                    "oe_narration.retrieval._open_request", side_effect=responses
                ) as opened:
                    with self.assertRaisesRegex(ValidationError, expected):
                        execute_retrieval(auth_path)
                self.assertEqual(opened.call_count, 2)
                failure_path = fixture / authorization["action"]["selected_sample_receipt_destination"]
                failure = json.loads(failure_path.read_text(encoding="utf-8"))
                self.assertEqual(failure["reason"], expected)
                self.assertFalse((fixture / authorization["action"]["destinations"][0]).exists())

    def test_truncated_audio_header_is_retained_only_as_blocked_evidence(self) -> None:
        temporary, fixture, auth_path = self._active_authorization()
        self.addCleanup(temporary.cleanup)
        authorization = json.loads(auth_path.read_text(encoding="utf-8"))
        truncated = b"RIFF\x10\x00\x00\x00WAVE"
        responses = self._success_responses(auth_path, truncated)
        with mock.patch.dict(
            os.environ, {"ELEVENLABS_API_KEY": "test-secret"}, clear=True
        ), mock.patch(
            "oe_narration.retrieval._open_request", side_effect=responses
        ) as opened:
            with self.assertRaisesRegex(ValidationError, "sample_audio_unparseable"):
                execute_retrieval(auth_path)
        self.assertEqual(opened.call_count, 2)
        raw = fixture / authorization["action"]["destinations"][0]
        self.assertEqual(raw.read_bytes(), truncated)
        self.assertEqual(stat.S_IMODE(raw.stat().st_mode), 0o600)
        failure_path = fixture / authorization["action"]["selected_sample_receipt_destination"]
        failure = json.loads(failure_path.read_text(encoding="utf-8"))
        self.assertEqual(failure["reason"], "sample_audio_unparseable")
        self.assertEqual(failure["blocked_local_evidence"]["status"], "blocked_not_usable")
        self.assertEqual(failure["blocked_local_evidence"]["sha256"], sha256_file(raw))

    def test_redirect_is_not_followed_or_retried(self) -> None:
        temporary, fixture, auth_path = self._active_authorization()
        self.addCleanup(temporary.cleanup)
        authorization = json.loads(auth_path.read_text(encoding="utf-8"))
        data = self._metadata_bytes([], authorization["action"]["voice_id"])
        redirected = _FakeResponse(
            data,
            content_type="application/json",
            url="https://example.invalid/redirected",
        )
        with mock.patch.dict(
            os.environ, {"ELEVENLABS_API_KEY": "test-secret"}, clear=True
        ), mock.patch(
            "oe_narration.retrieval._open_request", return_value=redirected
        ) as opened:
            with self.assertRaisesRegex(ValidationError, "provider_redirect_forbidden"):
                execute_retrieval(auth_path)
        self.assertEqual(opened.call_count, 1)

    def test_transport_failure_has_no_retry_and_never_leaks_secret(self) -> None:
        temporary, fixture, auth_path = self._active_authorization()
        self.addCleanup(temporary.cleanup)
        secret = "AUTH01-SUPER-SECRET-VALUE"
        with mock.patch.dict(os.environ, {"ELEVENLABS_API_KEY": secret}, clear=True), mock.patch(
            "oe_narration.retrieval._open_request",
            side_effect=urllib.error.URLError(f"transport included {secret}"),
        ) as opened:
            with self.assertRaises(ValidationError) as caught:
                execute_retrieval(auth_path)
        self.assertEqual(opened.call_count, 1)
        self.assertNotIn(secret, str(caught.exception))
        artifacts = list(fixture.rglob("*.json"))
        for artifact in artifacts:
            self.assertNotIn(secret, artifact.read_text(encoding="utf-8"))
        failure = json.loads(
            (fixture / "receipts" / "elevenlabs" / "metadata.json").read_text(encoding="utf-8")
        )
        self.assertEqual(failure["reason"], "provider_transport_failure")
        self.assertTrue((auth_path.parent / "consumed" / "AUTH-01.json").exists())

    def test_exact_two_get_success_preserves_raw_and_marks_provenance_pending(self) -> None:
        temporary, fixture, auth_path = self._active_authorization()
        self.addCleanup(temporary.cleanup)
        secret = "AUTH01-SUPER-SECRET-VALUE"
        responses = self._success_responses(auth_path)
        responses[0].headers["X-Request-Id"] = secret
        requests = []

        def open_response(request, timeout):
            requests.append(request)
            return responses[len(requests) - 1]

        with mock.patch.dict(os.environ, {"ELEVENLABS_API_KEY": secret}, clear=True), mock.patch(
            "oe_narration.retrieval._open_request", side_effect=open_response
        ) as opened:
            result = execute_retrieval(auth_path)
        self.assertEqual(opened.call_count, 2)
        self.assertEqual(result["provider_calls_made"], 2)
        self.assertEqual(result["downloads_made"], 1)
        self.assertEqual(result["provenance_verification"], "pending_human_review")
        self.assertFalse(result["human_source_confirmed"])
        self.assertFalse(result["single_speaker_confirmed"])
        self.assertFalse(result["hume_upload_authorized"])
        self.assertEqual([request.method for request in requests], ["GET", "GET"])
        authorization = json.loads(auth_path.read_text(encoding="utf-8"))
        voice_id = authorization["action"]["voice_id"]
        self.assertEqual(requests[0].full_url, authorization["action"]["metadata_endpoint"])
        self.assertEqual(
            requests[1].full_url,
            f"https://api.elevenlabs.io/v1/voices/{voice_id}/samples/sample-original-001/audio",
        )
        self.assertEqual(requests[0].get_header("Xi-api-key"), secret)
        raw = Path(result["raw_path"])
        self.assertEqual(raw.read_bytes(), self._wav_bytes())
        self.assertEqual(result["raw_sha256"], sha256_bytes(raw.read_bytes()))
        metadata_receipt = json.loads(Path(result["metadata_receipt"]).read_text(encoding="utf-8"))
        selected_receipt = json.loads(Path(result["selected_sample_receipt"]).read_text(encoding="utf-8"))
        self.assertEqual(metadata_receipt["response"]["provider_identifiers"]["xi-request-id"], "meta-request-1")
        self.assertNotIn("x-request-id", metadata_receipt["response"]["provider_identifiers"])
        self.assertEqual(selected_receipt["provider_identifiers"]["request-id"], "sample-request-1")
        self.assertEqual(selected_receipt["raw_output"]["mime_type"], "audio/wav")
        self.assertEqual(selected_receipt["raw_output"]["detected_container"], "wav")
        self.assertGreater(
            selected_receipt["raw_output"]["actual_media"]["duration_seconds"], 0
        )
        self.assertEqual(
            selected_receipt["raw_output"]["actual_media"]["audio_stream_count"], 1
        )
        self.assertEqual(selected_receipt["raw_output"]["byte_count"], len(raw.read_bytes()))
        self.assertEqual(selected_receipt["raw_output"]["sha256"], sha256_file(raw))
        self.assertFalse(selected_receipt["downstream_use_authorized"])
        self.assertEqual(
            metadata_receipt["provider_sample_metadata"]["original_filename"],
            "owner.wav",
        )
        self.assertEqual(stat.S_IMODE(raw.stat().st_mode), 0o600)
        for artifact in (
            Path(result["metadata_receipt"]),
            Path(result["selected_sample_receipt"]),
            Path(result["consumption_record"]),
        ):
            self.assertNotIn(secret, artifact.read_text(encoding="utf-8"))
            self.assertEqual(stat.S_IMODE(artifact.stat().st_mode), 0o600)

    def test_metadata_inventory_dry_run_and_cli_have_no_sample_or_credential_path(self) -> None:
        temporary, fixture, auth_path = self._active_inventory_authorization()
        self.addCleanup(temporary.cleanup)
        with mock.patch.dict(os.environ, {}, clear=True), mock.patch(
            "oe_narration.retrieval._open_request"
        ) as opened, mock.patch(
            "oe_narration.retrieval._sample_audio_endpoint",
            side_effect=AssertionError("sample endpoint must be unreachable"),
        ) as sample_endpoint:
            result = dry_run_metadata_inventory(auth_path)
            cli_result = dispatch(
                build_parser().parse_args(
                    ["inventory-elevenlabs-samples", "--authorization", str(auth_path)]
                )
            )
        for candidate in (result, cli_result):
            self.assertFalse(candidate["network_called"])
            self.assertFalse(candidate["credentials_accessed"])
            self.assertEqual(candidate["scope"], "elevenlabs_sample_metadata_inventory")
            preflight = candidate["executor_preflight"]
            self.assertEqual(preflight["authorized_limits"]["max_calls"], 1)
            self.assertEqual(preflight["authorized_limits"]["max_downloads"], 0)
            self.assertFalse(preflight["selection_permitted"])
            self.assertFalse(preflight["download_permitted"])
            self.assertFalse(preflight["sample_audio_endpoint_constructed"])
            self.assertFalse(preflight["raw_provider_payload_storage_permitted"])
            self.assertNotIn("sample_request", preflight)
            self.assertNotIn("raw_sample", preflight["destinations"])
        opened.assert_not_called()
        sample_endpoint.assert_not_called()
        self.assertFalse((auth_path.parent / "consumed" / "AUTH-01B.json").exists())

    def test_metadata_inventory_one_get_records_normalized_inventory_without_stdout_payload(self) -> None:
        temporary, fixture, auth_path = self._active_inventory_authorization()
        self.addCleanup(temporary.cleanup)
        authorization = json.loads(auth_path.read_text(encoding="utf-8"))
        endpoint = authorization["action"]["metadata_endpoint"]
        secret = "AUTH01B-SUPER-SECRET"
        samples = [
            {
                "sample_id": "sample-a",
                "file_name": "../../owner-a.wav",
                "mime_type": "audio/wav",
                "category": "cloned",
                "source": "user_upload",
                "hash": "provider-a",
                "size_bytes": 123,
                "is_generated": False,
                "is_original": True,
            },
            {
                "sample_id": "sample-a",
                "file_name": "..\\..\\private\\owner-b.mp3",
            },
            {"file_name": f"{secret}.wav", "source": secret},
            "malformed-entry",
            {"sample_id": "sample-c"},
        ]
        data = json.dumps(
            {"voice_id": authorization["action"]["voice_id"], "samples": samples}
        ).encode("utf-8")
        response = _FakeResponse(
            data,
            content_type="application/json",
            url=endpoint,
            headers={"x-request-id": "inventory-request-1"},
        )
        requests = []

        def open_response(request, timeout):
            consumption = auth_path.parent / "consumed" / "AUTH-01B.json"
            self.assertTrue(consumption.exists(), "authorization must be consumed before network")
            requests.append(request)
            return response

        with mock.patch.dict(
            os.environ, {"ELEVENLABS_API_KEY": secret}, clear=True
        ), mock.patch(
            "oe_narration.retrieval._open_request", side_effect=open_response
        ) as opened, mock.patch(
            "oe_narration.retrieval._sample_audio_endpoint",
            side_effect=AssertionError("sample endpoint must be unreachable"),
        ) as sample_endpoint:
            result = execute_metadata_inventory(auth_path)
        self.assertEqual(opened.call_count, 1)
        sample_endpoint.assert_not_called()
        self.assertEqual(len(requests), 1)
        self.assertEqual(requests[0].method, "GET")
        self.assertEqual(requests[0].full_url, endpoint)
        self.assertEqual(result["provider_calls_made"], 1)
        self.assertEqual(result["downloads_made"], 0)
        self.assertEqual(result["sample_count"], 5)
        self.assertFalse(result["inventory_complete"])
        self.assertNotIn("samples", result)
        self.assertNotIn("sample-a", json.dumps(result))
        self.assertFalse(result["sample_audio_endpoint_constructed"])
        self.assertFalse(result["raw_provider_payload_stored"])
        receipt_path = Path(result["metadata_receipt"])
        receipt_text = receipt_path.read_text(encoding="utf-8")
        self.assertNotIn(secret, receipt_text)
        receipt = json.loads(receipt_text)
        self.assertEqual(receipt["response"]["provider_identifiers"]["x-request-id"], "inventory-request-1")
        self.assertEqual(receipt["samples"][0]["sample_id"], "sample-a")
        self.assertEqual(receipt["samples"][0]["original_filename"], "owner-a.wav")
        self.assertEqual(receipt["samples"][1]["original_filename"], "owner-b.mp3")
        self.assertFalse(receipt["provider_metadata_is_provenance_proof"])
        completeness = receipt["inventory_completeness"]
        self.assertFalse(completeness["sample_entries_well_formed"])
        self.assertFalse(completeness["all_sample_ids_present"])
        self.assertFalse(completeness["all_original_filenames_present"])
        self.assertFalse(completeness["sample_ids_unique"])
        self.assertFalse(completeness["inventory_complete"])
        self.assertEqual(completeness["malformed_entry_indices"], [3])
        self.assertEqual(completeness["missing_sample_id_indices"], [2, 3])
        self.assertEqual(
            completeness["missing_original_filename_indices"], [2, 3, 4]
        )
        self.assertEqual(
            completeness["duplicate_sample_id_groups"],
            [{"sample_id": "sample-a", "metadata_indices": [0, 1]}],
        )
        self.assertFalse(receipt["selection_made"])
        self.assertFalse(receipt["download_permitted"])
        self.assertFalse(receipt["raw_provider_payload_stored"])
        self.assertFalse((fixture / "local-media").exists())
        self.assertEqual(stat.S_IMODE(receipt_path.stat().st_mode), 0o600)

    def test_metadata_inventory_contract_mutations_fail_before_credential_or_network(self) -> None:
        mutations = {
            "wrong_scope": lambda document: document.update(
                {"scope": "elevenlabs_sample_retrieval"}
            ),
            "wrong_endpoint": lambda document: document["action"].update(
                {"metadata_endpoint": "https://api.elevenlabs.io/v1/voices/wrong"}
            ),
            "selection_enabled": lambda document: document["action"].update(
                {"selection_permitted": True}
            ),
            "download_enabled": lambda document: document["action"].update(
                {"download_permitted": True}
            ),
            "raw_storage_enabled": lambda document: document["action"].update(
                {"raw_payload_storage_permitted": True}
            ),
            "two_calls": lambda document: document["authorized_limits"].update(
                {"max_calls": 2}
            ),
            "boolean_call_cap": lambda document: document["authorized_limits"].update(
                {"max_calls": True}
            ),
            "one_download": lambda document: document["authorized_limits"].update(
                {"max_downloads": 1}
            ),
            "oversized_metadata": lambda document: document["authorized_limits"].update(
                {"max_metadata_response_bytes": 2_000_001}
            ),
            "requested_authorized_mismatch": lambda document: document[
                "requested_limits"
            ].update({"max_metadata_response_bytes": 1_000_000}),
            "missing_consumption_count": lambda document: document["consumption"].pop(
                "downloads_used"
            ),
            "sample_field": lambda document: document["action"].update(
                {"sample_ids": ["forbidden"]}
            ),
            "local_media_receipt": lambda document: document["action"].update(
                {"metadata_receipt_destination": "local-media/inventory.json"}
            ),
        }
        for name, mutation in mutations.items():
            with self.subTest(name=name):
                temporary, fixture, auth_path = self._active_inventory_authorization()
                self.addCleanup(temporary.cleanup)
                authorization = json.loads(auth_path.read_text(encoding="utf-8"))
                mutation(authorization)
                self._write_json(auth_path, authorization)
                with mock.patch.dict(os.environ, {}, clear=True), mock.patch(
                    "oe_narration.retrieval._open_request"
                ) as opened:
                    with self.assertRaises(ValidationError):
                        dry_run_metadata_inventory(auth_path)
                opened.assert_not_called()
                self.assertFalse((auth_path.parent / "consumed" / "AUTH-01B.json").exists())

    def test_metadata_inventory_transport_and_size_failures_consume_once_without_retry(self) -> None:
        for mode in ("transport", "oversized"):
            with self.subTest(mode=mode):
                temporary, fixture, auth_path = self._active_inventory_authorization()
                self.addCleanup(temporary.cleanup)
                authorization = json.loads(auth_path.read_text(encoding="utf-8"))
                endpoint = authorization["action"]["metadata_endpoint"]
                secret = "AUTH01B-DO-NOT-LEAK"
                if mode == "transport":
                    side_effect = urllib.error.URLError(f"transport contained {secret}")
                    expected_reason = "provider_transport_failure"
                else:
                    side_effect = _FakeResponse(
                        b"{}",
                        content_type="application/json",
                        content_length=2_000_001,
                        url=endpoint,
                    )
                    expected_reason = "authorized_size_ceiling_exceeded"
                open_kwargs = (
                    {"side_effect": side_effect}
                    if mode == "transport"
                    else {"return_value": side_effect}
                )
                with mock.patch.dict(
                    os.environ, {"ELEVENLABS_API_KEY": secret}, clear=True
                ), mock.patch(
                    "oe_narration.retrieval._open_request", **open_kwargs
                ) as opened, mock.patch(
                    "oe_narration.retrieval._sample_audio_endpoint",
                    side_effect=AssertionError("sample endpoint must be unreachable"),
                ) as sample_endpoint:
                    with self.assertRaisesRegex(ValidationError, expected_reason) as caught:
                        execute_metadata_inventory(auth_path)
                self.assertEqual(opened.call_count, 1)
                sample_endpoint.assert_not_called()
                self.assertNotIn(secret, str(caught.exception))
                consumption = auth_path.parent / "consumed" / "AUTH-01B.json"
                self.assertTrue(consumption.exists())
                failure_path = fixture / authorization["action"]["metadata_receipt_destination"]
                failure_text = failure_path.read_text(encoding="utf-8")
                self.assertNotIn(secret, failure_text)
                failure = json.loads(failure_text)
                self.assertEqual(failure["reason"], expected_reason)
                self.assertEqual(failure["attempted_calls"], 1)
                self.assertEqual(failure["downloads_attempted"], 0)
                self.assertFalse(failure["sample_audio_endpoint_constructed"])
                self.assertFalse(failure["raw_provider_payload_stored"])

    def test_metadata_inventory_missing_credential_does_not_consume(self) -> None:
        temporary, fixture, auth_path = self._active_inventory_authorization()
        self.addCleanup(temporary.cleanup)
        with mock.patch.dict(os.environ, {}, clear=True), mock.patch(
            "oe_narration.retrieval._open_request"
        ) as opened:
            with self.assertRaisesRegex(ValidationError, "required only for authorized"):
                execute_metadata_inventory(auth_path)
        opened.assert_not_called()
        self.assertFalse((auth_path.parent / "consumed" / "AUTH-01B.json").exists())


if __name__ == "__main__":
    unittest.main()
