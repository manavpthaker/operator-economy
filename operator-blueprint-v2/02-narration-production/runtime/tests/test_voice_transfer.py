from __future__ import annotations

import ast
import copy
import json
import os
import shutil
import stat
import subprocess
import tempfile
import unittest
import urllib.request
import uuid
from contextlib import nullcontext
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

from oe_narration.core import ValidationError, sha256_bytes, sha256_file
from oe_narration import performance_transfer as pt
from oe_narration import voice_transfer as vt


class _FakeResponse:
    def __init__(
        self,
        data: bytes,
        *,
        status: int = 200,
        url: str = vt.ACCOUNT_ENDPOINT,
        content_type: str = "application/json",
        content_encoding: str = "identity",
        declared_length: int | None | object = object(),
        chunks: list[bytes] | None = None,
        headers: object | None = None,
    ) -> None:
        self._data = data
        self._offset = 0
        self._status = status
        self._url = url
        self._chunks = list(chunks) if chunks is not None else None
        self.closed = False
        self.timeouts: list[float] = []
        if headers is not None:
            self.headers = headers
        else:
            value: dict[str, str] = {
                "Content-Type": content_type,
                "Content-Encoding": content_encoding,
            }
            if declared_length.__class__ is object:
                value["Content-Length"] = str(len(data))
            elif declared_length is not None:
                value["Content-Length"] = str(declared_length)
            self.headers = value

    def read(self, size: int = -1) -> bytes:
        if self._chunks is not None:
            return self._chunks.pop(0) if self._chunks else b""
        if size < 0:
            size = len(self._data) - self._offset
        result = self._data[self._offset : self._offset + size]
        self._offset += len(result)
        return result

    def getcode(self) -> int:
        return self._status

    def geturl(self) -> str:
        return self._url

    def settimeout(self, timeout: float) -> None:
        self.timeouts.append(timeout)

    def close(self) -> None:
        self.closed = True


class _DuplicateHeaders:
    def items(self):
        return [
            ("Content-Type", "application/json"),
            ("content-type", "text/plain"),
        ]


class VoiceTransferTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.root = Path(__file__).resolve().parents[2]
        cls.fixture = cls.root / "fixtures" / vt.FIXTURE_ID
        cls.plan = cls.fixture / "performance-transfer-plan.json"
        cls.canonical_w = (
            cls.root
            / "fixtures"
            / "step2-v0.2-ai-visibility-v1.1"
            / "identity"
            / "canonical-w.txt"
        )

    def _temporary_authorization(self, document: dict, stem: str) -> Path:
        path = (
            self.fixture
            / "authorizations"
            / f"{stem}.DRAFT.{uuid.uuid4().hex}.json"
        )
        path.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        self.addCleanup(path.unlink, missing_ok=True)
        return path

    def _transfer_draft(self) -> dict:
        plan_dry = pt.validate_performance_transfer_plan(self.plan, self.canonical_w)
        authorization_id = "DRAFT-V2-unit-candidate-b-original-c"
        return {
            "schema_version": vt.TRANSFER_EXEC_AUTH_SCHEMA,
            "authorization_id": authorization_id,
            "status": "draft",
            "approved": False,
            "scope": vt.TRANSFER_EXEC_SCOPE,
            "target": {"kind": "fixture", "id": vt.FIXTURE_ID},
            "v1_lineage": {
                "path": vt.V1_LINEAGE_PATH,
                "sha256": vt.V1_LINEAGE_SHA256,
                "authorization_id": vt.V1_LINEAGE_ID,
                "status": "draft",
                "approved": False,
                "max_calls": 0,
                "max_spend_usd": 0,
            },
            "bindings": vt._base_transfer_bindings(plan_dry),
            "prerequisites": {
                name: {"state": "pending"}
                for name in (
                    "selected_guide",
                    "guide_qa",
                    "owner_selection",
                    "owner_audition_confirmation",
                    "elevenlabs_data_use",
                    "target_voice_rights",
                    "credential_account_verification",
                    "official_media_contract",
                )
            },
            "action": vt._action_transfer("pending"),
            "credential_binding": {
                "state": "pending",
                "mechanism": "verified_environment_api_key",
                "api_key_environment_variable": vt.API_KEY_ENV,
            },
            "runtime_bindings": {"state": "pending"},
            "authorized_limits": vt._transfer_limits(False),
            "artifacts": vt._transfer_artifacts(authorization_id),
            "consumption": {
                "status": "not_authorized",
                "generation_post_calls_used": 0,
                "outputs_received": 0,
                "spend_used_usd": 0,
                "record_path": vt.TRANSFER_SCOPE_LATCH_PATH,
            },
            "approved_by": "",
            "approved_at": "",
            "expires_at": "",
            "execution_ready": False,
            "blockers": ["owner account-readback assent and processed opt-out remain pending"],
        }

    def _account_draft(self) -> dict:
        authorization_id = "DRAFT-ACCOUNT-unit-readback"
        return {
            "schema_version": vt.ACCOUNT_AUTH_SCHEMA,
            "authorization_id": authorization_id,
            "status": "draft",
            "approved": False,
            "scope": vt.ACCOUNT_SCOPE,
            "target": {"kind": "fixture", "id": vt.FIXTURE_ID},
            "owner_approval": {"state": "pending"},
            "browser_readiness": {"state": "pending"},
            "action": vt._action_account(),
            "credential_binding": {
                "state": "pending",
                "mechanism": "environment_api_key",
                "api_key_environment_variable": vt.API_KEY_ENV,
            },
            "runtime_bindings": {"state": "pending"},
            "authorized_limits": vt._account_limits(False),
            "artifacts": vt._account_artifacts(authorization_id),
            "consumption": {
                "status": "not_authorized",
                "get_calls_used": 0,
                "post_calls_used": 0,
                "record_path": vt.ACCOUNT_SCOPE_LATCH_PATH,
            },
            "approved_by": "",
            "approved_at": "",
            "expires_at": "",
            "execution_ready": False,
            "blockers": ["literal owner reply is pending"],
        }

    def test_draft_account_is_credential_and_network_free(self) -> None:
        path = self._temporary_authorization(self._account_draft(), "account")
        with (
            mock.patch.object(vt, "_load_elevenlabs_api_key", side_effect=AssertionError("credential")),
            mock.patch.object(vt, "_open_elevenlabs_request", side_effect=AssertionError("network")),
        ):
            result = vt.validate_account_verification_authorization(path)
        self.assertTrue(result["valid"])
        self.assertFalse(result["provider_action_authorized"])
        self.assertFalse(result["credentials_accessed"])
        self.assertFalse(result["network_called"])

    def test_draft_transfer_is_credential_network_and_probe_free(self) -> None:
        path = self._temporary_authorization(self._transfer_draft(), "transfer")
        with (
            mock.patch.object(vt, "_load_elevenlabs_api_key", side_effect=AssertionError("credential")),
            mock.patch.object(vt, "_open_elevenlabs_request", side_effect=AssertionError("network")),
            mock.patch.object(vt, "_read_ffprobe_identity", side_effect=AssertionError("probe")),
        ):
            result = vt.validate_voice_transfer_execution_authorization(
                path,
                self.plan,
                self.canonical_w,
            )
        self.assertTrue(result["valid"])
        self.assertFalse(result["provider_action_authorized"])
        self.assertEqual(result["maximum"]["max_generation_post_calls"], 0)

    def _account_owner_approval_evidence(self) -> dict:
        return {
            "schema_version": "oe-elevenlabs-account-verification-owner-approval-evidence-v1",
            "provider": "elevenlabs",
            "source": "current_codex_thread_contextual_assent",
            "recorded_by": "Codex",
            "recorded_at": "2026-08-26T08:00:00+00:00",
            "owner": "Manav",
            "approval_basis": {
                "assistant_confirmation_prompt": vt.ACCOUNT_OWNER_APPROVAL_PROMPT,
                "owner_reply": vt.ACCOUNT_OWNER_APPROVAL_REPLY,
                "approval_event_timestamp_available": False,
                "record_materialization_time_is_not_claimed_as_message_time": True,
            },
            "approved_scope": {
                "action": vt._action_account(),
                "authorized_limits": vt._account_limits(True),
            },
            "execution_gate": {
                "this_record_is_an_active_provider_authorization": False,
                "credentials_may_be_accessed_from_this_record": False,
                "network_may_be_called_from_this_record": False,
                "separate_active_authorization_required": True,
                "voice_transfer_authorized": False,
            },
        }

    def _validate_account_owner_approval_evidence(self, document: dict) -> list[str]:
        raw = json.dumps(document, sort_keys=True, separators=(",", ":")).encode()
        errors: list[str] = []
        with mock.patch.object(
            vt,
            "_verified_prerequisite",
            return_value=(Path("/tmp/owner.json"), document, raw, sha256_bytes(raw)),
        ):
            vt._validate_account_owner_approval(
                Path("/tmp"),
                {"state": "verified", "path": "owner.json", "sha256": sha256_bytes(raw)},
                errors,
                expected_owner="Manav",
            )
        return errors

    def test_exact_literal_account_owner_prompt_and_reply_are_accepted(self) -> None:
        self.assertEqual(vt.ACCOUNT_OWNER_APPROVAL_REPLY, "Approved for both")
        self.assertEqual(
            self._validate_account_owner_approval_evidence(
                self._account_owner_approval_evidence()
            ),
            [],
        )

    def test_account_owner_prompt_or_reply_drift_is_rejected(self) -> None:
        cases = {
            "prompt": ("assistant_confirmation_prompt", vt.ACCOUNT_OWNER_APPROVAL_PROMPT + " "),
            "reply": ("owner_reply", "Approved"),
            "null_reply": ("owner_reply", None),
        }
        for label, (field, value) in cases.items():
            with self.subTest(label=label):
                document = self._account_owner_approval_evidence()
                document["approval_basis"][field] = value
                errors = self._validate_account_owner_approval_evidence(document)
                self.assertIn(
                    "does not bind the exact one-GET prompt and literal reply",
                    " ".join(errors),
                )

    def test_fixed_scope_latches_ignore_fresh_authorization_ids(self) -> None:
        self.assertEqual(vt._account_consumption_path("first"), vt._account_consumption_path("fresh"))
        self.assertEqual(vt._transfer_consumption_path("first"), vt._transfer_consumption_path("fresh"))
        self.assertEqual(vt._account_consumption_path("first"), vt.ACCOUNT_SCOPE_LATCH_PATH)
        self.assertEqual(vt._transfer_consumption_path("first"), vt.TRANSFER_SCOPE_LATCH_PATH)

    def test_existing_scope_latch_fails_before_credential_or_network(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            contract = SimpleNamespace(
                root=root,
                consumption_relative=vt.ACCOUNT_SCOPE_LATCH_PATH,
                success_relative="receipts/elevenlabs-account/fresh.run.json",
                failure_relative="receipts/elevenlabs-account/fresh.failure.json",
            )
            pt._ensure_execution_parents(
                root,
                [contract.consumption_relative, contract.success_relative, contract.failure_relative],
            )
            pt._exclusive_fixture_write(root, contract.consumption_relative, b"consumed")
            with (
                mock.patch.object(vt, "_build_account_contract", return_value=contract),
                mock.patch.object(vt, "_preflight_tls_environment"),
                mock.patch.object(vt, "_load_elevenlabs_api_key") as credential,
                mock.patch.object(vt, "_open_elevenlabs_request") as network,
                self.assertRaises(ValidationError),
            ):
                vt.execute_account_verification(root / "authorizations/fresh.ACTIVE.json")
            credential.assert_not_called()
            network.assert_not_called()

    def test_existing_transfer_scope_latch_blocks_fresh_authorization_id_before_secret_or_post(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            contract = SimpleNamespace(
                root=root,
                consumption_relative=vt.TRANSFER_SCOPE_LATCH_PATH,
                raw_relative=vt.TRANSFER_RAW_PATH,
                working_relative=vt.TRANSFER_WORKING_PATH,
                success_relative="receipts/elevenlabs/fresh.run.json",
                failure_relative="receipts/elevenlabs/fresh.failure.json",
                conversion_relative="receipts/elevenlabs/fresh.conversion.json",
            )
            pt._ensure_execution_parents(
                root,
                [
                    contract.consumption_relative,
                    contract.raw_relative,
                    contract.working_relative,
                    contract.success_relative,
                    contract.failure_relative,
                    contract.conversion_relative,
                ],
            )
            pt._exclusive_fixture_write(root, contract.consumption_relative, b"consumed")
            with (
                mock.patch.object(vt, "_build_transfer_contract", return_value=contract),
                mock.patch.object(vt, "_preflight_tls_environment"),
                mock.patch.object(vt, "_load_elevenlabs_api_key") as credential,
                mock.patch.object(vt, "_open_elevenlabs_request") as network,
                self.assertRaises(ValidationError),
            ):
                vt.execute_voice_transfer(
                    root / "authorizations/fresh.ACTIVE.json",
                    root / "performance-transfer-plan.json",
                    root / "canonical-w.txt",
                )
            credential.assert_not_called()
            network.assert_not_called()

    def test_schema_active_fields_are_exact_and_draft_fields_pending(self) -> None:
        schema = json.loads((self.root / "schemas/voice-transfer-execution-authorization.schema.json").read_text())
        verified_runtime = schema["$defs"]["verifiedRuntime"]
        self.assertTrue(
            {
                "git_binary_path", "git_binary_sha256", "git_version",
                "ffprobe_binary_path", "ffprobe_binary_sha256", "ffprobe_version",
                "ffmpeg_binary_path", "ffmpeg_binary_sha256", "ffmpeg_version",
                "media_tool_binding_scope", "dynamic_library_dependency_closure_verified",
                "media_executable_private_exact_byte_copy_required",
            }
            <= set(verified_runtime["required"])
        )
        self.assertEqual(verified_runtime["properties"]["git_binary_path"]["const"], "/usr/bin/git")
        self.assertEqual(
            verified_runtime["properties"]["media_tool_binding_scope"]["const"],
            "primary_executable_bytes_and_version_only",
        )
        self.assertFalse(
            verified_runtime["properties"]["dynamic_library_dependency_closure_verified"]["const"]
        )
        account_schema = json.loads(
            (self.root / "schemas/elevenlabs-account-verification-authorization.schema.json").read_text()
        )
        self.assertTrue(
            {"git_binary_path", "git_binary_sha256", "git_version"}
            <= set(account_schema["$defs"]["verifiedRuntime"]["required"])
        )
        self.assertEqual(
            schema["$defs"]["bindings"]["properties"]["normalized_http_request_sha256"]["const"],
            "878e7810bdddec3073cc6eee4d08072da6e312a4969bfc94a0daade19f321995",
        )
        self.assertEqual(
            schema["$defs"]["mediaContract"]["properties"]["sha256"]["const"],
            vt.MEDIA_CONTRACT_BASIS_SHA256,
        )
        active_bindings = schema["allOf"][1]["then"]["properties"]["bindings"]["allOf"]
        self.assertIn({"properties": {"enable_logging": {"const": True}}}, active_bindings)
        draft = schema["allOf"][0]["then"]["properties"]
        self.assertEqual(draft["runtime_bindings"], {"$ref": "#/$defs/pendingRuntime"})
        self.assertEqual(draft["authorized_limits"], {"$ref": "#/$defs/zeroLimits"})

    def test_schema_files_parse_and_have_no_duplicate_literal_constructor_keys(self) -> None:
        for name in (
            "elevenlabs-account-verification-authorization.schema.json",
            "voice-transfer-execution-authorization.schema.json",
        ):
            json.loads((self.root / "schemas" / name).read_text())
        tree = ast.parse((self.root / "runtime/oe_narration/voice_transfer.py").read_text())
        for node in ast.walk(tree):
            if isinstance(node, ast.Dict):
                keys = [key.value for key in node.keys if isinstance(key, ast.Constant) and isinstance(key.value, str)]
                self.assertEqual(len(keys), len(set(keys)), f"duplicate dict key near line {node.lineno}")

    def test_strict_json_rejects_nonstandard_numeric_constants(self) -> None:
        for constant in (b"NaN", b"Infinity", b"-Infinity"):
            with self.subTest(constant=constant):
                with self.assertRaisesRegex(ValidationError, "not strict UTF-8 JSON"):
                    pt._strict_json_bytes(
                        b'{"user_id":"bounded-user","uninspected":' + constant + b"}",
                        "ElevenLabs /v1/user response",
                    )

    def test_account_payload_rejects_nonstandard_numeric_constants_without_key_leak(self) -> None:
        secret = "sk_" + "x" * 40 + "abcd"
        for constant in (b"NaN", b"Infinity", b"-Infinity"):
            with self.subTest(constant=constant):
                with self.assertRaisesRegex(pt._GuideExecutionFailure, "account_response_json_invalid") as caught:
                    vt._parse_account_payload(
                        b'{"user_id":"bounded-user","uninspected":' + constant + b"}",
                        secret,
                        "abcd",
                    )
                self.assertNotIn(secret, str(caught.exception))
                self.assertIsNone(caught.exception.__cause__)
                self.assertIsNone(caught.exception.__context__)

    def test_media_contract_basis_is_exact_final_record(self) -> None:
        errors: list[str] = []
        path, document, _raw, digest = vt._validate_media_contract_basis(
            self.fixture,
            {
                "state": "verified",
                "path": vt.MEDIA_CONTRACT_BASIS_PATH,
                "sha256": vt.MEDIA_CONTRACT_BASIS_SHA256,
            },
            errors,
        )
        self.assertEqual(errors, [])
        self.assertEqual(path.relative_to(self.fixture).as_posix(), vt.MEDIA_CONTRACT_BASIS_PATH)
        self.assertEqual(digest, vt.MEDIA_CONTRACT_BASIS_SHA256)
        self.assertEqual(document["canonical_interpretation_sha256"], vt.MEDIA_CONTRACT_INTERPRETATION_SHA256)

    def test_normalized_request_is_exact_lowercase_url_and_hash(self) -> None:
        selected = (self.fixture / vt.SELECTED_GUIDE_PATH).read_bytes()
        manifest, body = pt._compile_multipart_bytes(
            selected,
            vt.SELECTED_GUIDE_SHA256,
            pt.TRANSFER_PRIMARY_FORMAT,
            enable_logging=True,
        )
        url, normalized, digest = vt._normalized_transfer_request(manifest)
        self.assertEqual(
            url,
            pt.TRANSFER_ENDPOINT + "?enable_logging=true&output_format=pcm_48000",
        )
        self.assertNotIn("True", url)
        self.assertEqual(digest, "878e7810bdddec3073cc6eee4d08072da6e312a4969bfc94a0daade19f321995")
        self.assertEqual(len(body), vt.TRANSFER_BODY_BYTES)
        self.assertEqual(sha256_bytes(body), vt.TRANSFER_BODY_SHA256)
        self.assertEqual(normalized["url"], url)

    def test_selected_guide_requires_private_mode(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            target = root / vt.SELECTED_GUIDE_PATH
            target.parent.mkdir(parents=True)
            shutil.copyfile(self.fixture / vt.SELECTED_GUIDE_PATH, target)
            os.chmod(target, 0o644)
            with self.assertRaisesRegex(ValidationError, "byte count mismatch"):
                vt._read_selected_wav(root, {"path": vt.SELECTED_GUIDE_PATH})
            os.chmod(target, 0o600)
            data, geometry = vt._read_selected_wav(root, {"path": vt.SELECTED_GUIDE_PATH})
            self.assertEqual(sha256_bytes(data), vt.SELECTED_GUIDE_SHA256)
            self.assertEqual(geometry["channels"], 1)

    def test_account_payload_absent_optional_echoes_is_accepted(self) -> None:
        user_id, digest, key_state, preview_state = vt._parse_account_payload(
            b'{"user_id":"user-123"}',
            "key-abcd",
            "abcd",
        )
        self.assertEqual(digest, vt._user_scope_hash(user_id))
        self.assertEqual(key_state, "absent_or_null")
        self.assertEqual(preview_state, "absent_or_null")

    def test_account_payload_present_optional_echoes_must_match(self) -> None:
        value = b'{"user_id":"user-123","xi_api_key":"key-abcd","xi_api_key_preview":"...abcd"}'
        _user_id, _digest, key_state, preview_state = vt._parse_account_payload(
            value,
            "key-abcd",
            "abcd",
        )
        self.assertEqual(key_state, "present_exact_match")
        self.assertEqual(preview_state, "present_last4_match")
        for bad in (
            b'{"user_id":"user-123","xi_api_key":"wrong"}',
            b'{"user_id":"user-123","xi_api_key_preview":"...wxyz"}',
        ):
            with self.assertRaises(pt._GuideExecutionFailure):
                vt._parse_account_payload(bad, "key-abcd", "abcd")

    def test_account_payload_duplicate_keys_fail_and_traceback_locals_are_scrubbed(self) -> None:
        secret = "secret-key-abcd"
        raw = b'{"user_id":"first","user_id":"second"}'
        try:
            vt._parse_account_payload(raw, secret, "abcd")
        except pt._GuideExecutionFailure as exc:
            frame = exc.__traceback__
            found = None
            while frame is not None:
                if frame.tb_frame.f_code.co_name == "_parse_account_payload":
                    found = frame.tb_frame.f_locals
                    break
                frame = frame.tb_next
            self.assertIsNotNone(found)
            assert found is not None
            self.assertEqual(found.get("raw"), b"")
            self.assertEqual(found.get("api_key"), "")
            self.assertEqual(found.get("preview"), "")
            self.assertNotIn(secret, repr(found))
        else:
            self.fail("duplicate account response keys were accepted")

    def test_safe_provider_evidence_omits_secret_shaped_identifiers(self) -> None:
        identifiers, usage = vt._safe_elevenlabs_provider_evidence(
            {
                "request-id": "ya29.secret-shaped",
                "x-request-id": "safe-request-1",
                "request-cost": "123",
            },
            "real-key",
        )
        self.assertEqual(identifiers, {"x-request-id": "safe-request-1"})
        self.assertEqual(usage, {"request-cost": 123})

    def test_transport_reads_short_chunks_to_eof_and_closes_response(self) -> None:
        response = _FakeResponse(
            b"ignored",
            chunks=[b'{"user_id":', b'"user-123"}', b""],
            declared_length=None,
        )
        seen: list[urllib.request.Request] = []

        def opener(request, timeout):
            seen.append(request)
            self.assertGreater(timeout, 0)
            return response

        with mock.patch.object(vt, "_open_elevenlabs_request", side_effect=opener):
            result = vt._perform_elevenlabs_request(
                method="GET",
                url=vt.ACCOUNT_ENDPOINT,
                api_key="private-key",
                timeout=5,
                accept="application/json",
                body=None,
                content_type=None,
                response_cap=vt.ACCOUNT_MAX_RESPONSE_BYTES,
                expected_mimes=frozenset({"application/json"}),
            )
        self.assertEqual(result.payload, b'{"user_id":"user-123"}')
        self.assertTrue(response.closed)
        self.assertEqual(seen[0].full_url, vt.ACCOUNT_ENDPOINT)
        headers = {name.lower(): value for name, value in seen[0].header_items()}
        self.assertEqual(headers["xi-api-key"], "private-key")
        self.assertEqual(headers["accept-encoding"], "identity")

    def test_transport_accepts_only_two_declared_audio_mimes(self) -> None:
        for mime in sorted(vt._AUDIO_MIMES):
            response = _FakeResponse(
                b"\x01\x00" * 10,
                url=pt.TRANSFER_ENDPOINT,
                content_type=mime,
            )
            with mock.patch.object(vt, "_open_elevenlabs_request", return_value=response):
                result = vt._perform_elevenlabs_request(
                    method="POST",
                    url=pt.TRANSFER_ENDPOINT,
                    api_key="private-key",
                    timeout=5,
                    accept="application/octet-stream",
                    body=b"request",
                    content_type="multipart/form-data; boundary=x",
                    response_cap=100,
                    expected_mimes=vt._AUDIO_MIMES,
                )
            self.assertEqual(result.content_type, mime)
        bad = _FakeResponse(b"private-response", url=pt.TRANSFER_ENDPOINT, content_type="audio/l16")
        with (
            mock.patch.object(vt, "_open_elevenlabs_request", return_value=bad),
            self.assertRaises(pt._GuideExecutionFailure) as captured,
        ):
            vt._perform_elevenlabs_request(
                method="POST",
                url=pt.TRANSFER_ENDPOINT,
                api_key="private-key",
                timeout=5,
                accept="application/octet-stream",
                body=b"request",
                content_type="multipart/form-data; boundary=x",
                response_cap=100,
                expected_mimes=vt._AUDIO_MIMES,
            )
        self.assertEqual(captured.exception.response_bytes, len(b"private-response"))
        self.assertNotIn("private-response", str(captured.exception))

    def test_transport_duplicate_headers_and_redirect_fail_closed(self) -> None:
        duplicate = _FakeResponse(
            b"{}",
            headers=_DuplicateHeaders(),
        )
        with (
            mock.patch.object(vt, "_open_elevenlabs_request", return_value=duplicate),
            self.assertRaises(pt._GuideExecutionFailure) as captured,
        ):
            vt._perform_elevenlabs_request(
                method="GET",
                url=vt.ACCOUNT_ENDPOINT,
                api_key="private-key",
                timeout=5,
                accept="application/json",
                body=None,
                content_type=None,
                response_cap=100,
                expected_mimes=frozenset({"application/json"}),
            )
        self.assertTrue(getattr(captured.exception, "response_received", False))
        redirected = _FakeResponse(b"{}", url="https://example.invalid/")
        with (
            mock.patch.object(vt, "_open_elevenlabs_request", return_value=redirected),
            self.assertRaises(pt._GuideExecutionFailure) as redirected_failure,
        ):
            vt._perform_elevenlabs_request(
                method="GET",
                url=vt.ACCOUNT_ENDPOINT,
                api_key="private-key",
                timeout=5,
                accept="application/json",
                body=None,
                content_type=None,
                response_cap=100,
                expected_mimes=frozenset({"application/json"}),
            )
        self.assertEqual(redirected_failure.exception.code, "provider_redirect_forbidden")

    def test_late_read_bytes_are_bound_in_deadline_failure(self) -> None:
        response = _FakeResponse(b"late", declared_length=None)
        with mock.patch.object(vt, "_monotonic", side_effect=[0.0, 2.0]):
            raw, failure = vt._read_response_to_eof(response, {}, 100, 1.0)
        self.assertEqual(raw, b"late")
        self.assertEqual(failure, "provider_request_elapsed_cap_exceeded")

    def test_tls_proxy_and_keylog_environment_are_not_inherited(self) -> None:
        request = urllib.request.Request(vt.ACCOUNT_ENDPOINT, method="GET")
        opener = mock.Mock()
        opener.open.return_value = object()
        context = mock.Mock()
        with (
            mock.patch.dict(
                os.environ,
                {
                    "HTTPS_PROXY": "http://proxy.invalid:8080",
                    "HTTP_PROXY": "http://proxy.invalid:8080",
                    "SSLKEYLOGFILE": "/tmp/forbidden-keylog",
                },
                clear=False,
            ),
            mock.patch.object(vt.ssl, "SSLContext", return_value=context),
            mock.patch.object(vt.urllib.request, "build_opener", return_value=opener) as build,
        ):
            vt._open_elevenlabs_request(request, 5)
        handlers = build.call_args.args
        self.assertIsInstance(handlers[0], urllib.request.ProxyHandler)
        self.assertEqual(handlers[0].proxies, {})
        self.assertIsNone(context.keylog_filename)
        opener.open.assert_called_once_with(request, timeout=5)

    def test_tls_trust_overrides_fail_before_transport(self) -> None:
        for variable in ("SSL_CERT_FILE", "SSL_CERT_DIR"):
            with (
                mock.patch.dict(os.environ, {variable: "/tmp/unreviewed"}, clear=False),
                self.assertRaises(ValidationError),
            ):
                vt._preflight_tls_environment()

    def test_negative_probe_accepts_only_exact_no_format_outcome(self) -> None:
        result = subprocess.CompletedProcess(
            ["ffprobe"],
            1,
            stdout=b"{\n\n}\n",
            stderr=vt.FFPROBE_NO_FORMAT_STDERR,
        )
        with (
            mock.patch.object(vt, "_read_ffprobe_identity", return_value=("/bound/ffprobe", "a" * 64)),
            mock.patch.object(vt, "_read_ffprobe_version", return_value="8.1.1"),
            mock.patch.object(pt, "_private_executable_copy", return_value=nullcontext("/private/ffprobe")),
            mock.patch.object(vt.subprocess, "run", return_value=result) as runner,
        ):
            vt._negative_ffprobe_media_detection(
                b"\x01\x00" * 100,
                ffprobe_path="/bound/ffprobe",
                ffprobe_sha256="a" * 64,
                ffprobe_version="8.1.1",
            )
        call = runner.call_args
        self.assertEqual(call.args[0], ["/bound/ffprobe", *vt.FFPROBE_MEDIA_PROBE_ARGUMENTS])
        self.assertEqual(call.kwargs["env"], {"PATH": "/usr/bin:/bin", "LANG": "C", "LC_ALL": "C"})
        self.assertEqual(call.kwargs["timeout"], vt.FFPROBE_MAX_ELAPSED_SECONDS)
        self.assertEqual(call.kwargs["executable"], "/private/ffprobe")

    def test_negative_probe_rejects_tool_detection_partial_and_timeout(self) -> None:
        cases = (
            subprocess.CompletedProcess(["ffprobe"], 2, stdout=b"{}", stderr=vt.FFPROBE_NO_FORMAT_STDERR),
            subprocess.CompletedProcess(["ffprobe"], 1, stdout=b'{"format":{"format_name":"mp3"}}', stderr=vt.FFPROBE_NO_FORMAT_STDERR),
            subprocess.CompletedProcess(["ffprobe"], 1, stdout=b"{}", stderr=b"unexpected\n"),
        )
        for result in cases:
            with (
                self.subTest(returncode=result.returncode, stdout=result.stdout),
                mock.patch.object(vt, "_read_ffprobe_identity", return_value=("/bound/ffprobe", "a" * 64)),
                mock.patch.object(vt, "_read_ffprobe_version", return_value="8.1.1"),
                mock.patch.object(pt, "_private_executable_copy", return_value=nullcontext("/private/ffprobe")),
                mock.patch.object(vt.subprocess, "run", return_value=result),
                self.assertRaises(pt._GuideExecutionFailure),
            ):
                vt._negative_ffprobe_media_detection(
                    b"\x01\x00" * 100,
                    ffprobe_path="/bound/ffprobe",
                    ffprobe_sha256="a" * 64,
                    ffprobe_version="8.1.1",
                )
        timeout = subprocess.TimeoutExpired(["ffprobe"], 10, output=b"private", stderr=b"private")
        with (
            mock.patch.object(vt, "_read_ffprobe_identity", return_value=("/bound/ffprobe", "a" * 64)),
            mock.patch.object(vt, "_read_ffprobe_version", return_value="8.1.1"),
            mock.patch.object(pt, "_private_executable_copy", return_value=nullcontext("/private/ffprobe")),
            mock.patch.object(vt.subprocess, "run", side_effect=timeout),
            self.assertRaises(pt._GuideExecutionFailure) as captured,
        ):
            vt._negative_ffprobe_media_detection(
                b"\x01\x00" * 100,
                ffprobe_path="/bound/ffprobe",
                ffprobe_sha256="a" * 64,
                ffprobe_version="8.1.1",
            )
        self.assertEqual(captured.exception.code, "ffprobe_media_probe_timeout")
        self.assertIsNone(timeout.output)
        self.assertIsNone(timeout.stderr)

    def test_raw_pcm_interpretation_and_duration_ratio_boundaries(self) -> None:
        def pcm(seconds: float) -> bytes:
            frames = int(seconds * 48_000)
            return b"\x01\x00" * frames

        with mock.patch.object(vt, "_negative_ffprobe_media_detection"):
            for seconds in (28.0, 34.0, 41.0):
                geometry = vt._validate_raw_pcm(
                    pcm(seconds),
                    ffprobe_path="/bound/ffprobe",
                    ffprobe_sha256="a" * 64,
                    ffprobe_version="8.1.1",
                )
                self.assertFalse(geometry["format_parameters_intrinsically_verified"])
                self.assertFalse(geometry["channel_count_intrinsically_verified"])
                self.assertTrue(geometry["frame_and_duration_computed_under_mono_contract_interpretation"])
                self.assertNotIn("channels", geometry)
                self.assertNotIn("duration_seconds", geometry)
            for seconds in (27.0, 42.0):
                with self.assertRaises(pt._GuideExecutionFailure):
                    vt._validate_raw_pcm(
                        pcm(seconds),
                        ffprobe_path="/bound/ffprobe",
                        ffprobe_sha256="a" * 64,
                        ffprobe_version="8.1.1",
                    )

    def test_raw_pcm_rejects_silence_and_compressed_container_signatures(self) -> None:
        payload_size = 48_000 * 30 * 2
        bad_payloads = [
            b"\x00" * payload_size,
            b"RIFF" + b"\x00" * (payload_size - 4),
            b"ID3" + b"\x00" * (payload_size - 3),
            b"fLaC" + b"\x00" * (payload_size - 4),
            b"OggS" + b"\x00" * (payload_size - 4),
            b"\x1aE\xdf\xa3" + b"\x00" * (payload_size - 4),
            b"\x00\x00\x00\x18ftyp" + b"\x00" * (payload_size - 8),
            b"\xff\xf1" + b"\x00" * (payload_size - 2),
        ]
        with mock.patch.object(vt, "_negative_ffprobe_media_detection"):
            for payload in bad_payloads:
                with self.subTest(prefix=payload[:8]), self.assertRaises(pt._GuideExecutionFailure):
                    vt._validate_raw_pcm(
                        payload,
                        ffprobe_path="/bound/ffprobe",
                        ffprobe_sha256="a" * 64,
                        ffprobe_version="8.1.1",
                    )

    def test_runtime_bindings_include_exact_external_probe_identity(self) -> None:
        bindings = vt.expected_runtime_bindings(draft=False, include_media_probe=True)
        self.assertEqual(bindings["state"], "verified")
        self.assertEqual(bindings["git_binary_path"], "/usr/bin/git")
        self.assertRegex(bindings["git_binary_sha256"], r"^[0-9a-f]{64}$")
        self.assertRegex(bindings["ffprobe_binary_sha256"], r"^[0-9a-f]{64}$")
        self.assertTrue(Path(bindings["ffprobe_binary_path"]).is_absolute())
        self.assertRegex(bindings["ffmpeg_binary_sha256"], r"^[0-9a-f]{64}$")
        self.assertTrue(Path(bindings["ffmpeg_binary_path"]).is_absolute())
        self.assertEqual(
            bindings["media_tool_binding_scope"],
            "primary_executable_bytes_and_version_only",
        )
        self.assertFalse(bindings["dynamic_library_dependency_closure_verified"])
        self.assertTrue(bindings["media_executable_private_exact_byte_copy_required"])
        self.assertEqual(
            vt._read_ffprobe_version(bindings["ffprobe_binary_path"]),
            bindings["ffprobe_version"],
        )

    def test_local_git_object_store_rejects_shallow_partial_and_promisor_state(self) -> None:
        bindings = {
            "git_binary_path": "/usr/bin/git",
            "git_binary_sha256": "a" * 64,
        }
        with (
            mock.patch.object(vt, "_bound_git", return_value=b"true\n"),
            self.assertRaisesRegex(ValidationError, "non-shallow"),
        ):
            vt._verify_local_git_object_store(bindings)
        for config in (
            b"extensions.partialclone\norigin\x00",
            b"remote.origin.promisor\ntrue\x00",
            b"remote.origin.partialclonefilter\nblob:none\x00",
        ):
            with (
                self.subTest(config=config),
                mock.patch.object(vt, "_bound_git", side_effect=[b"false\n", config]),
                self.assertRaisesRegex(ValidationError, "partial or promisor"),
            ):
                vt._verify_local_git_object_store(bindings)
        calls: list[list[str]] = []

        def safe_read(_bindings, arguments, **_kwargs):
            calls.append(arguments)
            return b"false\n" if arguments == ["rev-parse", "--is-shallow-repository"] else b""

        with mock.patch.object(vt, "_bound_git", side_effect=safe_read):
            vt._verify_local_git_object_store(bindings)
        self.assertEqual(
            calls,
            [
                ["rev-parse", "--is-shallow-repository"],
                ["config", "--local", "--null", "--list"],
            ],
        )

    def test_bound_git_ignores_hostile_path_and_detects_path_swap(self) -> None:
        git_path, git_sha = vt._read_git_identity()
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            marker = root / "fake-git-called"
            fake = root / "git"
            fake.write_text(f"#!/bin/sh\ntouch '{marker}'\nexit 99\n", encoding="utf-8")
            fake.chmod(0o700)
            with mock.patch.dict(os.environ, {"PATH": str(root)}, clear=False):
                head = pt._guide_git(
                    ["rev-parse", "HEAD"],
                    git_path=git_path,
                    git_sha256=git_sha,
                )
            self.assertRegex(head.decode("ascii").strip(), r"^[0-9a-f]{40}$")
            self.assertFalse(marker.exists())

            swapped = root / "bound-git"
            swapped.write_bytes(b"#!/bin/sh\nprintf original\n")
            swapped.chmod(0o700)

            def swap_during_run(*_args, **_kwargs):
                replacement = root / "replacement"
                replacement.write_bytes(b"#!/bin/sh\nprintf replaced\n")
                replacement.chmod(0o700)
                os.replace(replacement, swapped)
                return SimpleNamespace(returncode=0, stdout=b"a" * 40 + b"\n", stderr=b"")

            with (
                mock.patch.object(pt.subprocess, "run", side_effect=swap_during_run),
                self.assertRaises(ValidationError),
            ):
                pt._guide_git(["rev-parse", "HEAD"], git_path=str(swapped))

    def test_source_proof_commits_only_public_records_and_never_uses_remote_git(self) -> None:
        now = datetime(2026, 8, 26, 12, 0, tzinfo=timezone.utc)
        with tempfile.TemporaryDirectory() as temporary:
            repository = Path(temporary).resolve()
            authorization_path = repository / "authorizations" / "exact.ACTIVE.json"
            authorization_path.parent.mkdir(parents=True)
            authorization_raw = b'{"status":"active"}\n'
            authorization_path.write_bytes(authorization_raw)
            runtime_path = repository / "runtime.py"
            runtime_raw = b"runtime = True\n"
            runtime_path.write_bytes(runtime_raw)
            records: dict[str, tuple[Path, bytes, str]] = {}
            for name in sorted(vt.TRANSFER_COMMITTED_RECORD_NAMES):
                path = repository / "public" / f"{name}.json"
                path.parent.mkdir(parents=True, exist_ok=True)
                raw = (f'{{"name":"{name}"}}\n').encode()
                path.write_bytes(raw)
                records[name] = (path, raw, sha256_bytes(raw))
            for name in sorted(vt.TRANSFER_LOCAL_PRIVATE_RECORD_NAMES):
                path = repository / "ignored-private" / f"{name}.bin"
                path.parent.mkdir(parents=True, exist_ok=True)
                raw = (f"private-{name}\n").encode()
                path.write_bytes(raw)
                path.chmod(0o600)
                records[name] = (path, raw, sha256_bytes(raw))
            runtime_commit = "a" * 40
            head = "b" * 40
            bindings = {
                "git_commit": runtime_commit,
                "git_binary_path": "/usr/bin/git",
                "git_binary_sha256": "1" * 64,
                "git_version": "2.50.1",
                "executor_sha256": sha256_bytes(runtime_raw),
                "ffprobe_binary_path": "/bound/ffprobe",
                "ffprobe_binary_sha256": "2" * 64,
                "ffprobe_version": "8.1.1",
                "ffmpeg_binary_path": "/bound/ffmpeg",
                "ffmpeg_binary_sha256": "3" * 64,
                "ffmpeg_version": "8.1.1",
            }
            contract = vt._TransferExecutionContract(
                root=repository,
                authorization_path=authorization_path,
                authorization={"runtime_bindings": bindings},
                authorization_raw=authorization_raw,
                authorization_sha256=sha256_bytes(authorization_raw),
                plan_path=records["plan"][0],
                canonical_w_path=records["canonical_w"][0],
                approved_at=now,
                expires_at=now,
                consumption_relative=vt.TRANSFER_SCOPE_LATCH_PATH,
                raw_relative=vt.TRANSFER_RAW_PATH,
                working_relative=vt.TRANSFER_WORKING_PATH,
                success_relative="receipts/elevenlabs/exact.run.json",
                failure_relative="receipts/elevenlabs/exact.failure.json",
                conversion_relative="receipts/elevenlabs/exact.conversion.json",
                manifest={},
                body=b"",
                normalized_request={},
                records=records,
                browser_observed_at=now,
                account_verified_at=now,
                data_verified_at=now,
            )
            git_calls: list[list[str]] = []
            status_output = {"value": b""}
            authorization_relative = authorization_path.relative_to(repository).as_posix()
            public_by_relative = {
                path.relative_to(repository).as_posix(): raw
                for name, (path, raw, _sha) in records.items()
                if name in vt.TRANSFER_COMMITTED_RECORD_NAMES
            }

            def git_read(_bindings, arguments, **_kwargs):
                git_calls.append(arguments)
                if arguments == ["rev-parse", "--is-shallow-repository"]:
                    return b"false\n"
                if arguments == ["config", "--local", "--null", "--list"]:
                    return b""
                if arguments == ["rev-parse", "HEAD"]:
                    return (head + "\n").encode()
                if arguments[:2] == ["merge-base", "--is-ancestor"]:
                    return b""
                if arguments[0] == "diff":
                    return authorization_relative.encode() + b"\x00"
                if arguments[0] == "status":
                    return status_output["value"]
                if arguments[0] == "show":
                    commit, relative = arguments[1].split(":", 1)
                    if commit == "HEAD" and relative == authorization_relative:
                        return authorization_raw
                    if commit == runtime_commit and relative == "runtime.py":
                        return runtime_raw
                    if commit == runtime_commit and relative in public_by_relative:
                        return public_by_relative[relative]
                raise AssertionError(f"unexpected Git read: {arguments}")

            patches = (
                mock.patch.object(pt, "_guide_repository_root", return_value=repository),
                mock.patch.object(vt, "_runtime_files", return_value={"executor": ("runtime.py", runtime_path)}),
                mock.patch.object(vt, "_bound_git", side_effect=git_read),
                mock.patch.object(vt, "_read_ffprobe_identity", return_value=("/bound/ffprobe", "2" * 64)),
                mock.patch.object(vt, "_read_ffprobe_version", return_value="8.1.1"),
                mock.patch.object(vt, "_read_ffmpeg_identity", return_value=("/bound/ffmpeg", "3" * 64)),
                mock.patch.object(vt, "_read_ffmpeg_version", return_value="8.1.1"),
            )
            with patches[0], patches[1], patches[2], patches[3], patches[4], patches[5], patches[6]:
                proof = vt._verify_committed_source(contract, allow_consumption_latch=False)
            self.assertFalse(proof["remote_state_checked"])
            self.assertFalse(proof["git_network_called"])
            self.assertTrue(any(call[0] == "diff" and "--no-renames" in call for call in git_calls))
            self.assertFalse(any(call and call[0] in {"fetch", "pull", "push", "ls-remote"} for call in git_calls))
            shown = {
                call[1].split(":", 1)[1]
                for call in git_calls
                if call and call[0] == "show"
            }
            private_relatives = {
                path.relative_to(repository).as_posix()
                for name, (path, _raw, _sha) in records.items()
                if name in vt.TRANSFER_LOCAL_PRIVATE_RECORD_NAMES
            }
            self.assertTrue(private_relatives.isdisjoint(shown))
            latch_relative = contract.consumption_relative
            status_output["value"] = b"?? " + latch_relative.encode() + b"\x00"
            git_calls.clear()
            with patches[0], patches[1], patches[2], patches[3], patches[4], patches[5], patches[6]:
                latched_proof = vt._verify_committed_source(contract, allow_consumption_latch=True)
            self.assertEqual(latched_proof, proof)
            status_output["value"] = b"?? unrelated-private.json\x00"
            git_calls.clear()
            with (
                patches[0], patches[1], patches[2], patches[3], patches[4], patches[5], patches[6],
                self.assertRaisesRegex(ValidationError, "unignored worktree"),
            ):
                vt._verify_committed_source(contract, allow_consumption_latch=True)
            status_output["value"] = b""
            widened = records["qa"][0]
            widened.chmod(0o644)
            git_calls.clear()
            with (
                patches[0], patches[1], patches[2], patches[3], patches[4], patches[5], patches[6],
                self.assertRaisesRegex(ValidationError, "local-private"),
            ):
                vt._verify_committed_source(contract, allow_consumption_latch=False)

    def test_api_key_binding_never_returns_raw_value_in_failure(self) -> None:
        secret = "private-key-abcd"
        with (
            mock.patch.dict(os.environ, {vt.API_KEY_ENV: secret}, clear=False),
            self.assertRaises(ValidationError) as captured,
        ):
            vt._load_elevenlabs_api_key("0" * 64)
        self.assertNotIn(secret, str(captured.exception))


if __name__ == "__main__":
    unittest.main()
