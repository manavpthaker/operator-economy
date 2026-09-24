from __future__ import annotations

import ast
import copy
import json
import os
import re
import shutil
import stat
import subprocess
import tempfile
import time
import unittest
import urllib.request
import uuid
from contextlib import nullcontext
from datetime import datetime, timedelta, timezone
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

from oe_narration.core import ValidationError, sha256_bytes, sha256_file
from oe_narration import cli
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


def _worker_json_frame(document: dict) -> bytes:
    payload = vt._canonical_worker_json(document)
    return vt._TRANSFER_WORKER_FRAME_LENGTH_STRUCT.pack(len(payload)) + payload


def _worker_body_frame(payload: bytes) -> bytes:
    return vt._TRANSFER_WORKER_FRAME_LENGTH_STRUCT.pack(len(payload)) + payload


def _worker_request_phase() -> dict:
    return {
        "application_http_attempts": 1,
        "message": "phase",
        "network_state": "application_request_starting",
        "phase": "request_starting",
        "protocol": vt._TRANSFER_WORKER_PROTOCOL,
        "request_state": "outcome_unknown",
        "response_state": "none",
        "sequence": 1,
    }


def _worker_headers_phase(*, status: int = 200, content_type: str = "audio/pcm") -> dict:
    return {
        "application_http_attempts": 1,
        "content_encoding_state": "identity",
        "content_length_state": "valid_within_cap",
        "content_type": content_type,
        "http_status": status,
        "message": "phase",
        "network_state": "application_request_started",
        "phase": "response_headers_confirmed",
        "protocol": vt._TRANSFER_WORKER_PROTOCOL,
        "request_state": "response_confirmed",
        "response_state": "headers_confirmed",
        "sequence": 2,
    }


def _json_value_equal(left: object, right: object) -> bool:
    if (
        type(left) in {int, float}
        and type(right) in {int, float}
        and not isinstance(left, bool)
        and not isinstance(right, bool)
    ):
        return left == right
    if type(left) is not type(right):
        return False
    if isinstance(right, dict):
        return set(left) == set(right) and all(
            _json_value_equal(left[key], right[key]) for key in right
        )
    if isinstance(right, list):
        return len(left) == len(right) and all(
            _json_value_equal(a, b) for a, b in zip(left, right, strict=True)
        )
    return left == right


def _local_schema_errors(
    document: object,
    schema: dict,
    *,
    root_schema: dict | None = None,
    path: str = "$",
) -> list[str]:
    """Small dependency-free evaluator for every keyword used by this schema."""

    root_schema = schema if root_schema is None else root_schema
    errors: list[str] = []
    reference = schema.get("$ref")
    if reference is not None:
        if not isinstance(reference, str) or not reference.startswith("#/"):
            return [f"{path}: unsupported reference"]
        target: object = root_schema
        for token in reference[2:].split("/"):
            token = token.replace("~1", "/").replace("~0", "~")
            if not isinstance(target, dict) or token not in target:
                return [f"{path}: unresolved reference"]
            target = target[token]
        if not isinstance(target, dict):
            return [f"{path}: reference is not a schema"]
        errors.extend(
            _local_schema_errors(document, target, root_schema=root_schema, path=path)
        )
    expected_type = schema.get("type")
    type_ok = {
        "object": isinstance(document, dict),
        "array": isinstance(document, list),
        "string": isinstance(document, str),
        "boolean": isinstance(document, bool),
        "integer": type(document) is int,
        "number": type(document) in {int, float},
        "null": document is None,
    }.get(expected_type, True)
    if not type_ok:
        errors.append(f"{path}: expected {expected_type}")
        return errors
    if "const" in schema and not _json_value_equal(document, schema["const"]):
        errors.append(f"{path}: const mismatch")
    if "enum" in schema and not any(
        _json_value_equal(document, candidate) for candidate in schema["enum"]
    ):
        errors.append(f"{path}: enum mismatch")
    if isinstance(document, dict):
        required = schema.get("required", [])
        for key in required:
            if key not in document:
                errors.append(f"{path}: missing {key}")
        properties = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            for key in set(document) - set(properties):
                errors.append(f"{path}: extra {key}")
        for key, subschema in properties.items():
            if key in document:
                errors.extend(
                    _local_schema_errors(
                        document[key],
                        subschema,
                        root_schema=root_schema,
                        path=f"{path}.{key}",
                    )
                )
    if isinstance(document, list):
        if isinstance(schema.get("maxItems"), int) and len(document) > schema["maxItems"]:
            errors.append(f"{path}: too many items")
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for index, item in enumerate(document):
                errors.extend(
                    _local_schema_errors(
                        item,
                        item_schema,
                        root_schema=root_schema,
                        path=f"{path}[{index}]",
                    )
                )
    if isinstance(document, str):
        if isinstance(schema.get("minLength"), int) and len(document) < schema["minLength"]:
            errors.append(f"{path}: too short")
        if isinstance(schema.get("maxLength"), int) and len(document) > schema["maxLength"]:
            errors.append(f"{path}: too long")
        pattern = schema.get("pattern")
        if isinstance(pattern, str) and re.search(pattern, document) is None:
            errors.append(f"{path}: pattern mismatch")
    for subschema in schema.get("allOf", []):
        errors.extend(
            _local_schema_errors(document, subschema, root_schema=root_schema, path=path)
        )
    branches = schema.get("oneOf")
    if isinstance(branches, list):
        matches = sum(
            not _local_schema_errors(document, branch, root_schema=root_schema, path=path)
            for branch in branches
        )
        if matches != 1:
            errors.append(f"{path}: oneOf matched {matches} branches")
    condition = schema.get("if")
    if isinstance(condition, dict) and not _local_schema_errors(
        document, condition, root_schema=root_schema, path=path
    ):
        consequence = schema.get("then")
        if isinstance(consequence, dict):
            errors.extend(
                _local_schema_errors(
                    document, consequence, root_schema=root_schema, path=path
                )
            )
    return errors


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

    def _recovery_draft(self) -> dict:
        authorization_id = "DRAFT-ACCOUNT-RECOVERY-unit-readback"
        return {
            "schema_version": vt.RECOVERY_AUTH_SCHEMA,
            "authorization_id": authorization_id,
            "status": "draft",
            "approved": False,
            "scope": vt.RECOVERY_SCOPE,
            "target": {"kind": "fixture", "id": vt.FIXTURE_ID},
            "prior_failure_chain": vt._recovery_prior_failure_chain(),
            "owner_approval": {"state": "pending"},
            "browser_readiness": {"state": "pending"},
            "action": vt._action_recovery(),
            "credential_delivery": vt._recovery_credential_delivery(False),
            "runtime_bindings": {"state": "pending"},
            "authorized_limits": vt._recovery_limits(False),
            "artifacts": vt._recovery_artifacts(authorization_id),
            "consumption": vt._recovery_consumption(False),
            "approved_by": "",
            "approved_at": "",
            "expires_at": "",
            "execution_ready": False,
            "blockers": ["fresh browser evidence and frozen runtime remain pending"],
        }

    def _recovery_contract(self, root: Path, secret: str) -> SimpleNamespace:
        now = datetime.now(timezone.utc)
        authorization_path = root / "authorizations/recovery.ACTIVE.20260826T120000Z.json"
        authorization_raw = b"{}\n"
        authorization_path.parent.mkdir(parents=True, exist_ok=True)
        authorization_path.write_bytes(authorization_raw)
        authorization_path.chmod(0o600)
        return SimpleNamespace(
            root=root,
            authorization_path=authorization_path,
            authorization={"authorization_id": "AUTH-RECOVERY-unit"},
            authorization_raw=authorization_raw,
            authorization_sha256=sha256_bytes(authorization_raw),
            approved_at=now.replace(year=now.year - 1),
            expires_at=now.replace(year=now.year + 1),
            credential_latch_relative=vt.RECOVERY_CREDENTIAL_READ_LATCH_PATH,
            provider_latch_relative=vt.RECOVERY_SCOPE_LATCH_PATH,
            success_relative="receipts/elevenlabs-account/AUTH-RECOVERY-unit.recovery-run.json",
            failure_relative="receipts/elevenlabs-account/AUTH-RECOVERY-unit.recovery-failure.json",
            owner_approval_path=root / "evidence/owner.json",
            owner_approval_raw=b"{}\n",
            owner_approval_sha256="b" * 64,
            owner_approval_recorded_at=now.replace(year=now.year - 1),
            browser_readiness_path=root / "evidence/browser.json",
            browser_readiness_raw=b"{}\n",
            browser_readiness_sha256="c" * 64,
            expected_preview_sha256=vt._preview_hash(secret[-4:]),
            browser_observed_at=now,
            browser_capture_path=root / "evidence/browser.png",
            browser_capture_raw=b"png",
            browser_capture_sha256="d" * 64,
            official_basis_path=root / "evidence/official.json",
            official_basis_raw=b"{}\n",
            official_basis_sha256="e" * 64,
            prior_records={
                "active_authorization": (root / "prior-active.json", b"{}\n", "1" * 64),
                "consumption_latch": (root / "prior-latch.json", b"{}\n", "2" * 64),
                "failure_receipt": (root / "prior-failure.json", b"{}\n", "3" * 64),
                "failure_disposition": (root / "prior-disposition.json", b"{}\n", "4" * 64),
            },
        )

    def _prepare_recovery_destinations(self, root: Path) -> None:
        (root / "authorizations/consumed").mkdir(parents=True, mode=0o700)
        (root / "receipts/elevenlabs-account").mkdir(parents=True, mode=0o700)

    def test_recovery_additions_leave_frozen_account_v1_functions_exact(self) -> None:
        expected = {
            "_action_account": "13a387b2f5879652b87740b3f8b6f76aa403d38f50779e6bfe2b8dba770152c3",
            "_account_limits": "c1a0d4c1c23a7ccddbda8bf53bd431e0607edbe9c84c9f0bcd0bb2226a70f5f1",
            "_account_consumption_path": "cc2d0f1bcc703740aec1732f3e511c6e4df25f22c7d58a780218c4b80ca23159",
            "validate_account_verification_authorization": "afb72b50bcccb3ae4877fde165b22c62c02e96c9ac61475f8f64f10b6246a52e",
            "_build_account_contract": "c212653b17017a47680e6c0841f7209d8b564b68f05263de8785b99726ec8cba",
            "_verify_committed_source": "a71ab1f03f5507d5ed9a29e501a162c93f69ba03b165ceb006b3b717d1e4e538",
            "_preflight_account_paths": "6115811295e59f026548fb6908e2a9d42ab2d47dc09e13857e75514e2220bb85",
            "_load_elevenlabs_api_key": "faf9538ef984da193e306ad06fa3e5f88dcef5104c0dccfc6746ecadc3de0ef3",
            "_perform_elevenlabs_request": "cf5930432ae42ef35a0958371b0c8033575c414762534ce175c193677d0f0f48",
            "execute_account_verification": "dace0a18a68b21645971724fc4bb8d7f77c532b8aad2128570e0c0bc56789668",
        }
        source = Path(vt.__file__).read_text(encoding="utf-8")
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

    def test_draft_recovery_is_zero_authority_and_never_reads_credentials(self) -> None:
        path = self._temporary_authorization(self._recovery_draft(), "account-recovery")
        with (
            mock.patch.object(vt, "_read_recovery_dotenv_key", side_effect=AssertionError("credential")),
            mock.patch.object(vt, "_open_elevenlabs_request", side_effect=AssertionError("network")),
            mock.patch.object(vt, "_validate_recovery_prior_records") as prior_records,
        ):
            result = vt.validate_account_recovery_authorization(path)
        prior_records.assert_not_called()
        self.assertTrue(result["valid"])
        self.assertEqual(result["authorization_status"], "draft")
        self.assertFalse(result["provider_action_authorized"])
        self.assertFalse(result["credential_read_authorized"])
        self.assertFalse(result["credentials_accessed"])
        self.assertFalse(result["network_called"])
        self.assertEqual(result["maximum"]["max_credential_preflight_reads"], 0)
        self.assertEqual(result["maximum"]["max_get_calls"], 0)
        self.assertTrue(result["action"]["no_fallback"])
        self.assertFalse(result["fallback_permitted"])
        self.assertFalse(result["fallback_used"])
        for field in (
            "voice_transfer_authorized", "audio_upload_authorized",
            "full_capture_authorized", "creative_approved", "step2_lock_authorized",
            "step3_authorized", "sharing_authorized", "publication_authorized",
            "account_settings_changed",
        ):
            self.assertIn(field, result)
            self.assertFalse(result[field])

    def test_recovery_schema_binds_exact_prior_chain_fixed_dotenv_and_two_latches(self) -> None:
        schema = json.loads(
            (self.root / "schemas/elevenlabs-account-recovery-authorization.schema.json").read_text()
        )
        self.assertEqual(
            schema["properties"]["schema_version"]["const"],
            vt.RECOVERY_AUTH_SCHEMA,
        )
        prior = schema["$defs"]["priorFailureChain"]["properties"]
        self.assertEqual(prior["outcome_commit"]["const"], vt.RECOVERY_PRIOR_OUTCOME_COMMIT)
        self.assertEqual(
            prior["active_authorization"]["allOf"][1]["properties"]["sha256"]["const"],
            vt.RECOVERY_PRIOR_ACTIVE_SHA256,
        )
        credential = schema["$defs"]["verifiedCredential"]["properties"]
        self.assertEqual(credential["dotenv_path"]["const"], str(vt.RECOVERY_DOTENV_PATH))
        self.assertEqual(credential["required_mode"]["const"], "0600")
        self.assertEqual(credential["required_link_count"]["const"], 1)
        self.assertTrue(credential["dotenv_re_read_after_latch_forbidden"]["const"])
        consumption = schema["$defs"]["consumption"]["properties"]
        self.assertEqual(
            consumption["credential_read_latch_path"]["const"],
            vt.RECOVERY_CREDENTIAL_READ_LATCH_PATH,
        )
        self.assertEqual(
            consumption["provider_call_latch_path"]["const"],
            vt.RECOVERY_SCOPE_LATCH_PATH,
        )
        self.assertTrue(schema["$defs"]["action"]["properties"]["no_fallback"]["const"])
        self.assertNotEqual(vt.RECOVERY_SCOPE_LATCH_PATH, vt.ACCOUNT_SCOPE_LATCH_PATH)

    def test_recovery_dotenv_parser_requires_one_literal_unexpanded_assignment(self) -> None:
        secret = "sk_private_unit_abcd"
        self.assertEqual(
            vt._parse_recovery_dotenv_key(
                b"OTHER=value\n# comment\nELEVENLABS_API_KEY=" + secret.encode() + b"\n"
            ),
            secret,
        )
        bad_values = (
            b"OTHER=value\n",
            b"ELEVENLABS_API_KEY=one\nELEVENLABS_API_KEY=two\n",
            b"export ELEVENLABS_API_KEY=value\n",
            b" ELEVENLABS_API_KEY=value\n",
            b"ELEVENLABS_API_KEY =value\n",
            b"ELEVENLABS_API_KEY= value\n",
            b"ELEVENLABS_API_KEY=value \n",
            b"ELEVENLABS_API_KEY=value\r\n",
            b"ELEVENLABS_API_KEY=\xff\n",
        )
        for raw in bad_values:
            with self.subTest(raw=raw), self.assertRaises(ValidationError):
                vt._parse_recovery_dotenv_key(raw)

    def test_recovery_dotenv_descriptor_enforces_mode_owner_link_type_and_race(self) -> None:
        secret = "sk_private_unit_abcd"
        with tempfile.TemporaryDirectory(dir=self.root) as temporary:
            root = Path(temporary)
            dotenv = root / ".env"
            dotenv.write_bytes(f"ELEVENLABS_API_KEY={secret}\n".encode())
            dotenv.chmod(0o600)
            self.assertEqual(vt._read_bounded_recovery_dotenv_key(dotenv), secret)

            dotenv.chmod(0o644)
            with self.assertRaisesRegex(ValidationError, "mode-0600"):
                vt._read_bounded_recovery_dotenv_key(dotenv)
            dotenv.chmod(0o600)

            symlink = root / "symlink.env"
            symlink.symlink_to(dotenv)
            with self.assertRaises(ValidationError):
                vt._read_bounded_recovery_dotenv_key(symlink)

            hardlink = root / "hardlink.env"
            os.link(dotenv, hardlink)
            with self.assertRaisesRegex(ValidationError, "single-link"):
                vt._read_bounded_recovery_dotenv_key(dotenv)
            hardlink.unlink()

            fifo = root / "fifo.env"
            os.mkfifo(fifo, 0o600)
            with self.assertRaisesRegex(ValidationError, "regular file"):
                vt._read_bounded_recovery_dotenv_key(fifo)

            before = os.stat(dotenv, follow_symlinks=False)
            after_values = {
                field: getattr(before, field)
                for field in (
                    "st_dev", "st_ino", "st_size", "st_mtime_ns", "st_ctime_ns",
                    "st_mode", "st_uid", "st_gid", "st_nlink",
                )
            }
            after_values["st_mtime_ns"] += 1
            after = SimpleNamespace(**after_values)
            with (
                mock.patch.object(os, "fstat", side_effect=[before, after]),
                self.assertRaisesRegex(ValidationError, "changed during"),
            ):
                vt._read_bounded_recovery_dotenv_key(dotenv)

    def test_recovery_fixed_wrapper_has_no_arbitrary_path_or_environment_fallback(self) -> None:
        secret = "sk_fixed_dotenv_abcd"
        with (
            mock.patch.object(vt, "_read_bounded_recovery_dotenv_key", return_value=secret) as reader,
            mock.patch.dict(os.environ, {vt.API_KEY_ENV: "host-environment-wxyz"}, clear=False),
        ):
            self.assertEqual(vt._read_recovery_dotenv_key(), secret)
        reader.assert_called_once_with(vt.RECOVERY_DOTENV_PATH)

    def test_recovery_response_parser_derives_no_account_identifier_hash(self) -> None:
        secret = "sk_private_unit_abcd"
        raw = b'{"user_id":"private-user","xi_api_key_preview":"...abcd"}'
        with mock.patch.object(
            vt,
            "_user_scope_hash",
            side_effect=AssertionError("recovery must not hash the user ID"),
        ):
            result = vt._parse_recovery_account_payload(raw, secret, "abcd")
        self.assertEqual(result, (True, "absent_or_null", "present_last4_match"))
        self.assertNotIn("private-user", repr(result))

    def test_recovery_response_and_dotenv_parser_failures_scrub_traceback_locals(self) -> None:
        sentinels = (
            "SENSITIVE_USER_SENTINEL",
            "SENSITIVE_EXPECTED_KEY_SENTINEL_abcd",
            "SENSITIVE_ECHOED_KEY_SENTINEL",
        )
        raw = json.dumps(
            {
                "user_id": sentinels[0],
                "xi_api_key": sentinels[2],
            },
            separators=(",", ":"),
        ).encode()
        try:
            vt._parse_recovery_account_payload(raw, sentinels[1], "abcd")
        except pt._GuideExecutionFailure as exc:
            self.assertIsNone(exc.__cause__)
            self.assertIsNone(exc.__context__)
            current = exc
            while current is not None:
                traceback = current.__traceback__
                while traceback is not None:
                    if traceback.tb_frame.f_code.co_name == "_parse_recovery_account_payload":
                        values = repr(traceback.tb_frame.f_locals)
                        for sentinel in sentinels:
                            self.assertNotIn(sentinel, values)
                    traceback = traceback.tb_next
                current = current.__context__
        else:
            self.fail("mismatched echoed key was accepted")

        dotenv_secret = "SENSITIVE_DOTENV_KEY_SENTINEL"
        try:
            vt._parse_recovery_dotenv_key(
                f"ELEVENLABS_API_KEY={dotenv_secret}\nELEVENLABS_API_KEY=duplicate\n".encode()
            )
        except ValidationError as exc:
            traceback = exc.__traceback__
            while traceback is not None:
                if traceback.tb_frame.f_code.co_name == "_parse_recovery_dotenv_key":
                    self.assertNotIn(dotenv_secret, repr(traceback.tb_frame.f_locals))
                traceback = traceback.tb_next
        else:
            self.fail("duplicate dotenv assignment was accepted")

        for label, unsafe in (
            (
                "carriage-return",
                f"ELEVENLABS_API_KEY={dotenv_secret}\r\n".encode(),
            ),
            (
                "invalid-utf8",
                f"ELEVENLABS_API_KEY={dotenv_secret}".encode() + b"\xff\n",
            ),
        ):
            with self.subTest(label=label):
                try:
                    vt._parse_recovery_dotenv_key(unsafe)
                except ValidationError as exc:
                    self.assertIsNone(exc.__cause__)
                    self.assertIsNone(exc.__context__)
                    traceback = exc.__traceback__
                    while traceback is not None:
                        if traceback.tb_frame.f_code.co_name == "_parse_recovery_dotenv_key":
                            self.assertNotIn(dotenv_secret, repr(traceback.tb_frame.f_locals))
                        traceback = traceback.tb_next
                else:
                    self.fail(f"{label} dotenv was accepted")

    def test_recovery_private_capture_enforces_png_mode_link_and_descriptor_identity(self) -> None:
        png = b"\x89PNG\r\n\x1a\nredacted-unit"
        with tempfile.TemporaryDirectory(dir=self.root) as temporary:
            root = Path(temporary)
            path = root / "evidence/browser.png"
            path.parent.mkdir(parents=True)
            path.write_bytes(png)
            path.chmod(0o600)
            self.assertEqual(vt._read_recovery_private_capture(root, path), (png, sha256_bytes(png)))
            path.chmod(0o644)
            with self.assertRaisesRegex(ValidationError, "mode-0600"):
                vt._read_recovery_private_capture(root, path)
            path.chmod(0o600)
            hardlink = root / "evidence/browser-hardlink.png"
            os.link(path, hardlink)
            with self.assertRaisesRegex(ValidationError, "single-link"):
                vt._read_recovery_private_capture(root, path)
            hardlink.unlink()
            before = os.stat(path, follow_symlinks=False)
            values = {
                field: getattr(before, field)
                for field in (
                    "st_dev", "st_ino", "st_size", "st_mtime_ns", "st_ctime_ns",
                    "st_mode", "st_uid", "st_gid", "st_nlink",
                )
            }
            values["st_ctime_ns"] += 1
            real_fstat = os.fstat
            file_fstats = {"count": 0}

            def racing_fstat(descriptor):
                observed = real_fstat(descriptor)
                if stat.S_ISREG(observed.st_mode) and observed.st_ino == before.st_ino:
                    file_fstats["count"] += 1
                    return before if file_fstats["count"] == 1 else SimpleNamespace(**values)
                return observed

            with (
                mock.patch.object(os, "fstat", side_effect=racing_fstat),
                self.assertRaisesRegex(ValidationError, "changed during"),
            ):
                vt._read_recovery_private_capture(root, path)

    def test_recovery_active_authority_requires_private_mode_and_single_link(self) -> None:
        secret = "sk_private_unit_abcd"
        with tempfile.TemporaryDirectory(dir=self.root) as temporary:
            root = Path(temporary)
            contract = self._recovery_contract(root, secret)
            vt._verify_recovery_active_authority_private(contract)

            contract.authorization_path.chmod(0o644)
            with self.assertRaisesRegex(ValidationError, "mode-0600"):
                vt._verify_recovery_active_authority_private(contract)

            contract.authorization_path.chmod(0o600)
            hardlink = root / "active-authority-hardlink.json"
            os.link(contract.authorization_path, hardlink)
            with self.assertRaisesRegex(ValidationError, "single-link"):
                vt._verify_recovery_active_authority_private(contract)
            hardlink.unlink()
            vt._verify_recovery_active_authority_private(contract)

    def test_recovery_private_capture_git_state_requires_exact_info_exclude_and_untracked(self) -> None:
        repository = Path("/repo")
        relative = "fixture/evidence/browser.png"
        capture = repository / relative
        exclude = "/repo/.git/info/exclude"

        def good(_bindings, arguments, **_kwargs):
            if arguments[0] == "ls-files":
                return b""
            if arguments[:2] == ["rev-parse", "--path-format=absolute"]:
                return (exclude + "\n").encode()
            if arguments[0] == "check-ignore":
                return f"{exclude}:7:/{relative}\t{relative}\n".encode()
            raise AssertionError(arguments)

        with mock.patch.object(vt, "_bound_git", side_effect=good):
            result = vt._verify_recovery_private_capture_git_state({}, repository, capture)
        self.assertFalse(result["tracked"])
        self.assertFalse(result["committed"])
        self.assertEqual(result["ignore_source"], "git_info_exclude")

        def tracked(_bindings, arguments, **kwargs):
            if arguments[0] == "ls-files":
                return b"100644 deadbeef 0\t" + relative.encode() + b"\n"
            return good(_bindings, arguments, **kwargs)

        with (
            mock.patch.object(vt, "_bound_git", side_effect=tracked),
            self.assertRaisesRegex(ValidationError, "untracked"),
        ):
            vt._verify_recovery_private_capture_git_state({}, repository, capture)

        def wrong_ignore(_bindings, arguments, **kwargs):
            if arguments[0] == "check-ignore":
                return f"/repo/.gitignore:2:{relative}\t{relative}\n".encode()
            return good(_bindings, arguments, **kwargs)

        with (
            mock.patch.object(vt, "_bound_git", side_effect=wrong_ignore),
            self.assertRaisesRegex(ValidationError, "exact Git info/exclude"),
        ):
            vt._verify_recovery_private_capture_git_state({}, repository, capture)

    def test_recovery_active_prior_chain_reads_exact_private_records_and_rejects_mode_missing_tamper(self) -> None:
        chain = vt._recovery_prior_failure_chain()
        with tempfile.TemporaryDirectory(dir=self.root) as temporary:
            root = Path(temporary)
            for name in (
                "active_authorization", "consumption_latch", "failure_receipt", "failure_disposition"
            ):
                binding = chain[name]
                source = self.fixture / binding["path"]
                target = root / binding["path"]
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(source, target)
                target.chmod(0o644 if name == "failure_disposition" else 0o600)
            errors: list[str] = []
            records = vt._validate_recovery_prior_records(root, chain, errors)
            self.assertEqual(errors, [])
            self.assertEqual(set(records), {
                "active_authorization", "consumption_latch", "failure_receipt", "failure_disposition"
            })

            private = root / chain["failure_receipt"]["path"]
            private.chmod(0o644)
            with self.assertRaisesRegex(ValidationError, "mode-0600"):
                vt._validate_recovery_prior_records(root, chain, [])
            private.chmod(0o600)
            private.unlink()
            with self.assertRaises(ValidationError):
                vt._validate_recovery_prior_records(root, chain, [])

            shutil.copyfile(self.fixture / chain["failure_receipt"]["path"], private)
            private.chmod(0o600)
            private.write_bytes(private.read_bytes() + b" ")
            with self.assertRaisesRegex(ValidationError, "SHA-256 mismatch"):
                vt._validate_recovery_prior_records(root, chain, [])

    def test_recovery_source_proof_binds_evidence_and_nested_latch_status_paths(self) -> None:
        secret = "sk_private_unit_abcd"
        with tempfile.TemporaryDirectory(dir=self.root) as temporary:
            repository = Path(temporary)
            fixture_root = (
                repository
                / "operator-blueprint-v2/02-narration-production/fixtures/nested-recovery"
            )
            contract = self._recovery_contract(fixture_root, secret)
            runtime_path = repository / "runtime.py"
            runtime_raw = b"runtime\n"
            runtime_sha = sha256_bytes(runtime_raw)
            runtime_commit = "1" * 40
            head = "2" * 40
            contract.authorization_raw = b'{"active":true}\n'
            contract.authorization_sha256 = sha256_bytes(contract.authorization_raw)
            contract.authorization_path.write_bytes(contract.authorization_raw)
            contract.authorization_path.chmod(0o600)
            contract.owner_approval_sha256 = sha256_bytes(contract.owner_approval_raw)
            contract.browser_readiness_sha256 = sha256_bytes(contract.browser_readiness_raw)
            contract.official_basis_sha256 = sha256_bytes(contract.official_basis_raw)
            prior_records = {}
            for index, (name, value) in enumerate(contract.prior_records.items(), start=1):
                raw = json.dumps({"record": name}, sort_keys=True).encode() + b"\n"
                prior_records[name] = (value[0], raw, sha256_bytes(raw))
            contract.prior_records = prior_records
            bindings = {
                "git_commit": runtime_commit,
                "git_binary_path": "/usr/bin/git",
                "git_binary_sha256": "f" * 64,
                "git_version": "2.50.1",
                "executor_sha256": runtime_sha,
            }
            contract.authorization = {
                "authorization_id": "AUTH-RECOVERY-unit",
                "runtime_bindings": bindings,
            }
            authorization_relative = contract.authorization_path.relative_to(repository).as_posix()
            owner_relative = contract.owner_approval_path.relative_to(repository).as_posix()
            browser_relative = contract.browser_readiness_path.relative_to(repository).as_posix()
            official_relative = contract.official_basis_path.relative_to(repository).as_posix()
            runtime_relative = "runtime.py"
            prior_by_relative = {
                path.relative_to(repository).as_posix(): raw
                for path, raw, _sha in prior_records.values()
            }
            state = {"missing_browser": False, "wrong_owner": False, "dirty": b""}

            def git_read(_bindings, arguments, **_kwargs):
                if arguments == ["rev-parse", "HEAD"]:
                    return (head + "\n").encode()
                if arguments[0] == "merge-base":
                    return b""
                if arguments[0] == "diff":
                    return authorization_relative.encode() + b"\x00"
                if arguments[0] == "status":
                    return state["dirty"]
                if arguments[0] == "show":
                    commit, relative = arguments[1].split(":", 1)
                    if commit == "HEAD" and relative == authorization_relative:
                        return contract.authorization_raw
                    if commit == runtime_commit and relative == runtime_relative:
                        return runtime_raw
                    if commit == vt.RECOVERY_PRIOR_OUTCOME_COMMIT and relative in prior_by_relative:
                        return prior_by_relative[relative]
                    if commit == runtime_commit and relative == owner_relative:
                        return contract.owner_approval_raw
                    if commit == vt.RECOVERY_OWNER_APPROVAL_COMMIT and relative == owner_relative:
                        return b"wrong\n" if state["wrong_owner"] else contract.owner_approval_raw
                    if commit == runtime_commit and relative == browser_relative:
                        return b"" if state["missing_browser"] else contract.browser_readiness_raw
                    if commit == runtime_commit and relative == official_relative:
                        return contract.official_basis_raw
                raise AssertionError(arguments)

            def private_read(_root, path, _label, **_kwargs):
                if path == contract.authorization_path:
                    return contract.authorization_raw, contract.authorization_sha256
                for record_path, raw, digest in prior_records.values():
                    if path == record_path:
                        return raw, digest
                if path == contract.owner_approval_path:
                    return contract.owner_approval_raw, contract.owner_approval_sha256
                if path == contract.browser_readiness_path:
                    return contract.browser_readiness_raw, contract.browser_readiness_sha256
                raise AssertionError(path)

            def public_read(_root, path, _label, **_kwargs):
                if path == runtime_path:
                    return runtime_raw, runtime_sha
                for name, (record_path, raw, digest) in prior_records.items():
                    if name == "failure_disposition" and path == record_path:
                        return raw, digest
                if path == contract.official_basis_path:
                    return contract.official_basis_raw, contract.official_basis_sha256
                raise AssertionError(path)

            patches = (
                mock.patch.object(pt, "_guide_repository_root", return_value=repository),
                mock.patch.object(vt, "_recovery_runtime_files", return_value={
                    "executor": (runtime_relative, runtime_path)
                }),
                mock.patch.object(vt, "_verify_local_git_object_store"),
                mock.patch.object(vt, "_bound_git", side_effect=git_read),
                mock.patch.object(vt, "_read_recovery_private_bytes", side_effect=private_read),
                mock.patch.object(vt, "_read_bound_blob", side_effect=public_read),
                mock.patch.object(
                    vt,
                    "_read_recovery_private_capture",
                    return_value=(contract.browser_capture_raw, contract.browser_capture_sha256),
                ),
                mock.patch.object(
                    vt,
                    "_verify_recovery_private_capture_git_state",
                    return_value={"tracked": False, "committed": False},
                ),
            )
            with patches[0], patches[1], patches[2], patches[3], patches[4], patches[5], patches[6], patches[7]:
                proof = vt._verify_recovery_committed_source(
                    contract,
                    allowed_latches=frozenset(),
                )
            self.assertEqual(proof["owner_approval_baseline_commit"], vt.RECOVERY_OWNER_APPROVAL_COMMIT)
            self.assertTrue(proof["browser_readiness_json_committed_at_runtime"])

            credential_status_path = (
                (contract.root / contract.credential_latch_relative)
                .relative_to(repository)
                .as_posix()
            )
            provider_status_path = (
                (contract.root / contract.provider_latch_relative)
                .relative_to(repository)
                .as_posix()
            )
            state["dirty"] = b"?? " + credential_status_path.encode() + b"\x00"
            with patches[0], patches[1], patches[2], patches[3], patches[4], patches[5], patches[6], patches[7]:
                credential_proof = vt._verify_recovery_committed_source(
                    contract,
                    allowed_latches=frozenset({contract.credential_latch_relative}),
                )
            self.assertEqual(credential_proof["head_delta_path"], authorization_relative)

            state["dirty"] = b"".join(
                b"?? " + relative.encode() + b"\x00"
                for relative in sorted((credential_status_path, provider_status_path))
            )
            with patches[0], patches[1], patches[2], patches[3], patches[4], patches[5], patches[6], patches[7]:
                both_proof = vt._verify_recovery_committed_source(
                    contract,
                    allowed_latches=frozenset(
                        {
                            contract.credential_latch_relative,
                            contract.provider_latch_relative,
                        }
                    ),
                )
            self.assertEqual(both_proof["head_delta_path"], authorization_relative)
            state["dirty"] = b""

            state["missing_browser"] = True
            with (
                patches[0], patches[1], patches[2], patches[3], patches[4], patches[5], patches[6], patches[7],
                self.assertRaisesRegex(ValidationError, "browser readiness.*runtime commit"),
            ):
                vt._verify_recovery_committed_source(contract, allowed_latches=frozenset())
            state["missing_browser"] = False
            state["wrong_owner"] = True
            with (
                patches[0], patches[1], patches[2], patches[3], patches[4], patches[5], patches[6], patches[7],
                self.assertRaisesRegex(ValidationError, "baseline commit drifted"),
            ):
                vt._verify_recovery_committed_source(contract, allowed_latches=frozenset())
            state["wrong_owner"] = False
            state["dirty"] = b"?? unrelated.json\x00"
            with (
                patches[0], patches[1], patches[2], patches[3], patches[4], patches[5], patches[6], patches[7],
                self.assertRaisesRegex(ValidationError, "worktree must be exact"),
            ):
                vt._verify_recovery_committed_source(contract, allowed_latches=frozenset())

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

    def test_recovery_nonsecret_source_drift_creates_no_latch_and_reads_no_key(self) -> None:
        secret = "sk_private_unit_abcd"
        with tempfile.TemporaryDirectory(dir=self.root) as temporary:
            root = Path(temporary)
            self._prepare_recovery_destinations(root)
            contract = self._recovery_contract(root, secret)
            drifted = copy.copy(contract)
            drifted.browser_readiness_sha256 = "9" * 64
            with (
                mock.patch.object(vt, "_build_recovery_contract", side_effect=[contract, drifted]),
                mock.patch.object(vt, "_preflight_tls_environment"),
                mock.patch.object(vt, "_verify_recovery_committed_source", return_value={}),
                mock.patch.object(vt, "_read_recovery_dotenv_key") as reader,
                mock.patch.object(vt, "_perform_elevenlabs_request") as network,
                self.assertRaisesRegex(ValidationError, "source changed before"),
            ):
                vt.execute_account_recovery(contract.authorization_path)
            self.assertFalse((root / vt.RECOVERY_CREDENTIAL_READ_LATCH_PATH).exists())
            self.assertFalse((root / vt.RECOVERY_SCOPE_LATCH_PATH).exists())
            reader.assert_not_called()
            network.assert_not_called()

    def test_recovery_preview_mismatch_consumes_only_credential_read_latch(self) -> None:
        expected_secret = "sk_private_unit_abcd"
        wrong_secret = "sk_private_unit_wxyz"
        with tempfile.TemporaryDirectory(dir=self.root) as temporary:
            root = Path(temporary)
            self._prepare_recovery_destinations(root)
            contract = self._recovery_contract(root, expected_secret)
            with (
                mock.patch.object(vt, "_build_recovery_contract", return_value=contract),
                mock.patch.object(vt, "_preflight_tls_environment"),
                mock.patch.object(vt, "_verify_recovery_committed_source", return_value={}),
                mock.patch.object(vt, "_read_recovery_dotenv_key", return_value=wrong_secret) as reader,
                mock.patch.object(vt, "_perform_elevenlabs_request") as network,
                self.assertRaisesRegex(ValidationError, "without retry"),
            ):
                vt.execute_account_recovery(contract.authorization_path)
            self.assertTrue((root / vt.RECOVERY_CREDENTIAL_READ_LATCH_PATH).is_file())
            self.assertFalse((root / vt.RECOVERY_SCOPE_LATCH_PATH).exists())
            self.assertTrue((root / contract.failure_relative).is_file())
            persisted = (root / contract.failure_relative).read_bytes()
            self.assertNotIn(wrong_secret.encode(), persisted)
            self.assertNotIn(wrong_secret[-4:].encode(), persisted)
            reader.assert_called_once_with()
            network.assert_not_called()

            with (
                mock.patch.object(vt, "_build_recovery_contract", return_value=contract),
                mock.patch.object(vt, "_preflight_tls_environment"),
                mock.patch.object(vt, "_read_recovery_dotenv_key") as second_reader,
                mock.patch.object(vt, "_perform_elevenlabs_request") as second_network,
                self.assertRaises(ValidationError),
            ):
                vt.execute_account_recovery(contract.authorization_path)
            second_reader.assert_not_called()
            second_network.assert_not_called()

    def test_recovery_source_drift_after_read_consumes_read_but_not_provider_latch(self) -> None:
        secret = "sk_private_unit_abcd"
        with tempfile.TemporaryDirectory(dir=self.root) as temporary:
            root = Path(temporary)
            self._prepare_recovery_destinations(root)
            contract = self._recovery_contract(root, secret)
            drifted = copy.copy(contract)
            drifted.browser_capture_sha256 = "8" * 64
            with (
                mock.patch.object(
                    vt,
                    "_build_recovery_contract",
                    side_effect=[contract, contract, drifted],
                ),
                mock.patch.object(vt, "_preflight_tls_environment"),
                mock.patch.object(vt, "_verify_recovery_committed_source", return_value={}),
                mock.patch.object(vt, "_read_recovery_dotenv_key", return_value=secret) as reader,
                mock.patch.object(vt, "_perform_elevenlabs_request") as network,
                self.assertRaisesRegex(ValidationError, "without retry"),
            ):
                vt.execute_account_recovery(contract.authorization_path)
            self.assertTrue((root / vt.RECOVERY_CREDENTIAL_READ_LATCH_PATH).is_file())
            self.assertFalse((root / vt.RECOVERY_SCOPE_LATCH_PATH).exists())
            reader.assert_called_once_with()
            network.assert_not_called()

    def test_recovery_success_orders_two_latches_one_read_and_one_get_without_env_mutation(self) -> None:
        secret = "sk_private_unit_abcd"
        host_value = "host-environment-must-not-be-used-wxyz"
        user_id = "private-user-123"
        response_body = json.dumps({"user_id": user_id}, separators=(",", ":")).encode()
        response = vt._ElevenResponse(
            response_bytes=len(response_body),
            response_sha256=sha256_bytes(response_body),
            content_type="application/json",
            content_encoding="identity",
            payload=response_body,
            provider_identifiers={"request-id": "safe-id"},
            provider_usage={"request-cost": 0},
        )
        with tempfile.TemporaryDirectory(dir=self.root) as temporary:
            root = Path(temporary)
            self._prepare_recovery_destinations(root)
            contract = self._recovery_contract(root, secret)
            events: list[str] = []
            real_write = pt._exclusive_fixture_write

            def write(root_value, relative, data):
                events.append(f"write:{relative}")
                return real_write(root_value, relative, data)

            def read_key():
                events.append("read:fixed-dotenv")
                return secret

            def perform(**kwargs):
                events.append("network:GET")
                self.assertEqual(kwargs["method"], "GET")
                self.assertEqual(kwargs["url"], vt.ACCOUNT_ENDPOINT)
                self.assertIsNone(kwargs["body"])
                self.assertEqual(kwargs["api_key"], secret)
                return response

            with (
                mock.patch.object(vt, "_build_recovery_contract", return_value=contract),
                mock.patch.object(vt, "_preflight_tls_environment"),
                mock.patch.object(
                    vt,
                    "_verify_recovery_committed_source",
                    return_value={"git_head": "f" * 40},
                ),
                mock.patch.object(vt, "_read_recovery_dotenv_key", side_effect=read_key) as reader,
                mock.patch.object(vt, "_perform_elevenlabs_request", side_effect=perform) as network,
                mock.patch.object(pt, "_exclusive_fixture_write", side_effect=write),
                mock.patch.dict(os.environ, {vt.API_KEY_ENV: host_value}, clear=False),
            ):
                before = dict(os.environ)
                result = vt.execute_account_recovery(contract.authorization_path)
                self.assertEqual(dict(os.environ), before)
            self.assertTrue(result["valid"])
            self.assertEqual(result["provider_get_calls_made"], 1)
            self.assertEqual(result["provider_post_calls_made"], 0)
            reader.assert_called_once_with()
            network.assert_called_once()
            self.assertEqual(
                events[:4],
                [
                    f"write:{vt.RECOVERY_CREDENTIAL_READ_LATCH_PATH}",
                    "read:fixed-dotenv",
                    f"write:{vt.RECOVERY_SCOPE_LATCH_PATH}",
                    "network:GET",
                ],
            )
            run_path = root / contract.success_relative
            self.assertTrue(run_path.is_file())
            persisted = run_path.read_bytes()
            for forbidden in (secret.encode(), secret[-4:].encode(), user_id.encode(), response_body):
                self.assertNotIn(forbidden, persisted)
            run = json.loads(persisted)
            self.assertEqual(run["schema_version"], vt.RECOVERY_RUN_SCHEMA)
            self.assertEqual(run["endpoint"], vt.ACCOUNT_ENDPOINT)
            self.assertEqual(run["method"], "GET")
            self.assertEqual(run["accept"], "application/json")
            self.assertEqual(run["accept_encoding"], "identity")
            self.assertEqual(run["credential_fingerprint_sha256"], vt._key_fingerprint(secret))
            self.assertNotIn("user_scope_binding_sha256", run)
            self.assertNotIn("response_sha256", run)
            self.assertTrue(run["valid_user_id_present"])
            self.assertEqual(run["response_bytes"], len(response_body))
            self.assertFalse(run["environment_inheritance_used"])
            self.assertFalse(run["dotenv_reread_after_credential_latch"])
            self.assertFalse(run["raw_response_stored"])
            self.assertFalse(run["raw_account_data_stored"])
            self.assertFalse(run["account_data_stored"])
            self.assertFalse(run["response_hash_stored"])
            self.assertFalse(run["response_derived_identifier_stored"])
            self.assertEqual(run["account_linkage_strength"], "contextual_non_cryptographic")
            self.assertFalse(run["exact_ui_api_account_equality_claimed"])
            for field in (
                "retry_permitted", "redirect_permitted", "fallback_permitted", "fallback_used"
            ):
                self.assertIn(field, run)
                self.assertFalse(run[field])
                self.assertIn(field, result)
                self.assertFalse(result[field])
            for field in (
                "voice_transfer_authorized", "audio_upload_authorized",
                "full_capture_authorized", "creative_approved", "step2_lock_authorized",
                "step3_authorized", "sharing_authorized", "publication_authorized",
                "account_settings_changed",
            ):
                self.assertIn(field, run)
                self.assertFalse(run[field])
                self.assertIn(field, result)
                self.assertFalse(result[field])

    def test_recovery_transport_failure_consumes_provider_latch_forever_without_retry(self) -> None:
        secret = "sk_private_unit_abcd"
        with tempfile.TemporaryDirectory(dir=self.root) as temporary:
            root = Path(temporary)
            self._prepare_recovery_destinations(root)
            contract = self._recovery_contract(root, secret)
            with (
                mock.patch.object(vt, "_build_recovery_contract", return_value=contract),
                mock.patch.object(vt, "_preflight_tls_environment"),
                mock.patch.object(vt, "_verify_recovery_committed_source", return_value={}),
                mock.patch.object(vt, "_read_recovery_dotenv_key", return_value=secret) as reader,
                mock.patch.object(
                    vt,
                    "_perform_elevenlabs_request",
                    side_effect=vt._eleven_failure("provider_transport_failure"),
                ) as network,
                self.assertRaisesRegex(ValidationError, "without retry"),
            ):
                vt.execute_account_recovery(contract.authorization_path)
            self.assertTrue((root / vt.RECOVERY_CREDENTIAL_READ_LATCH_PATH).is_file())
            self.assertTrue((root / vt.RECOVERY_SCOPE_LATCH_PATH).is_file())
            self.assertTrue((root / contract.failure_relative).is_file())
            failure = json.loads((root / contract.failure_relative).read_text())
            self.assertEqual(failure["endpoint"], vt.ACCOUNT_ENDPOINT)
            self.assertEqual(failure["method"], "GET")
            self.assertEqual(failure["provider_get_receipt_state"], "ambiguous_transport")
            self.assertFalse(failure["provider_response_received"])
            self.assertFalse(failure["account_data_stored"])
            self.assertFalse(failure["response_hash_stored"])
            self.assertFalse(failure["response_derived_identifier_stored"])
            self.assertFalse(failure["fallback_permitted"])
            self.assertFalse(failure["fallback_used"])
            for field in (
                "voice_transfer_authorized", "audio_upload_authorized",
                "full_capture_authorized", "creative_approved", "step2_lock_authorized",
                "step3_authorized", "sharing_authorized", "publication_authorized",
                "account_settings_changed",
            ):
                self.assertIn(field, failure)
                self.assertFalse(failure[field])
            reader.assert_called_once_with()
            network.assert_called_once()

            with (
                mock.patch.object(vt, "_build_recovery_contract", return_value=contract),
                mock.patch.object(vt, "_preflight_tls_environment"),
                mock.patch.object(vt, "_read_recovery_dotenv_key") as second_reader,
                mock.patch.object(vt, "_perform_elevenlabs_request") as second_network,
                self.assertRaises(ValidationError),
            ):
                vt.execute_account_recovery(contract.authorization_path)
            second_reader.assert_not_called()
            second_network.assert_not_called()

    def test_recovery_external_hardlink_after_provider_latch_blocks_get(self) -> None:
        secret = "sk_private_unit_abcd"
        with (
            tempfile.TemporaryDirectory(dir=self.root) as temporary,
            tempfile.TemporaryDirectory() as outside_temporary,
        ):
            root = Path(temporary)
            outside = Path(outside_temporary)
            self._prepare_recovery_destinations(root)
            contract = self._recovery_contract(root, secret)
            real_write = pt._exclusive_fixture_write
            external_hardlink = outside / "provider-latch-hardlink.json"

            def write(root_value, relative, data):
                real_write(root_value, relative, data)
                if relative == contract.provider_latch_relative:
                    os.link(root_value / relative, external_hardlink)

            with (
                mock.patch.object(vt, "_build_recovery_contract", return_value=contract),
                mock.patch.object(vt, "_preflight_tls_environment"),
                mock.patch.object(vt, "_verify_recovery_committed_source", return_value={}),
                mock.patch.object(vt, "_read_recovery_dotenv_key", return_value=secret) as reader,
                mock.patch.object(vt, "_perform_elevenlabs_request") as network,
                mock.patch.object(pt, "_exclusive_fixture_write", side_effect=write),
                self.assertRaisesRegex(ValidationError, "without retry"),
            ):
                vt.execute_account_recovery(contract.authorization_path)
            self.assertTrue(external_hardlink.is_file())
            self.assertTrue((root / vt.RECOVERY_CREDENTIAL_READ_LATCH_PATH).is_file())
            self.assertTrue((root / vt.RECOVERY_SCOPE_LATCH_PATH).is_file())
            reader.assert_called_once_with()
            network.assert_not_called()

    def test_recovery_terminal_failure_traceback_drops_private_contract_and_response(self) -> None:
        secret = "sk_private_unit_abcd"
        capture_sentinel = b"PRIVATE_LOCAL_BROWSER_CAPTURE_SENTINEL"
        user_sentinel = "PRIVATE_PROVIDER_USER_SENTINEL"
        echoed_key_sentinel = "PRIVATE_PROVIDER_ECHOED_KEY_SENTINEL"
        response_hash_sentinel = "PRIVATE_RESPONSE_HASH_SENTINEL"
        response_body = json.dumps(
            {
                "user_id": user_sentinel,
                "xi_api_key": echoed_key_sentinel,
            },
            separators=(",", ":"),
        ).encode()
        response = vt._ElevenResponse(
            response_bytes=len(response_body),
            response_sha256=response_hash_sentinel,
            content_type="application/json",
            content_encoding="identity",
            payload=response_body,
            provider_identifiers={},
            provider_usage={},
        )
        with tempfile.TemporaryDirectory(dir=self.root) as temporary:
            root = Path(temporary)
            self._prepare_recovery_destinations(root)
            contract = self._recovery_contract(root, secret)
            contract.browser_capture_raw = capture_sentinel
            caught: ValidationError | None = None
            try:
                with (
                    mock.patch.object(vt, "_build_recovery_contract", return_value=contract),
                    mock.patch.object(vt, "_preflight_tls_environment"),
                    mock.patch.object(vt, "_verify_recovery_committed_source", return_value={}),
                    mock.patch.object(vt, "_read_recovery_dotenv_key", return_value=secret),
                    mock.patch.object(vt, "_perform_elevenlabs_request", return_value=response),
                ):
                    vt.execute_account_recovery(contract.authorization_path)
            except ValidationError as exc:
                caught = exc
            self.assertIsNotNone(caught)
            assert caught is not None
            seen_execute_frame = False
            pending: BaseException | None = caught
            visited: set[int] = set()
            while pending is not None and id(pending) not in visited:
                visited.add(id(pending))
                traceback = pending.__traceback__
                while traceback is not None:
                    if traceback.tb_frame.f_code.co_name == "execute_account_recovery":
                        seen_execute_frame = True
                        locals_snapshot = traceback.tb_frame.f_locals
                        rendered = repr(locals_snapshot)
                        for sentinel in (
                            secret,
                            secret[-4:],
                            capture_sentinel.decode(),
                            user_sentinel,
                            echoed_key_sentinel,
                            response_hash_sentinel,
                            response_body.decode(),
                        ):
                            self.assertNotIn(sentinel, rendered)
                        self.assertIsNone(locals_snapshot["contract"])
                        self.assertIsNone(locals_snapshot["refreshed"])
                        self.assertIsNone(locals_snapshot["response"])
                        self.assertIsNone(locals_snapshot["failure"])
                        self.assertIsNone(locals_snapshot["pending_parse_failure"])
                        self.assertEqual(locals_snapshot["credential_latch_bytes"], b"")
                        self.assertEqual(locals_snapshot["provider_latch_bytes"], b"")
                    traceback = traceback.tb_next
                pending = pending.__context__ or pending.__cause__
            self.assertTrue(seen_execute_frame)

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
            "elevenlabs-account-recovery-authorization.schema.json",
            "voice-transfer-execution-authorization.schema.json",
        ):
            json.loads((self.root / "schemas" / name).read_text())
        tree = ast.parse((self.root / "runtime/oe_narration/voice_transfer.py").read_text())
        for node in ast.walk(tree):
            if isinstance(node, ast.Dict):
                keys = [key.value for key in node.keys if isinstance(key, ast.Constant) and isinstance(key.value, str)]
                self.assertEqual(len(keys), len(set(keys)), f"duplicate dict key near line {node.lineno}")

    def test_recovery_cli_is_isolated_from_legacy_account_command(self) -> None:
        parser = cli.build_parser()
        authorization = self.fixture / "authorizations/recovery.DRAFT.json"
        dry_args = parser.parse_args(
            ["elevenlabs-account-recover", "--authorization", str(authorization)]
        )
        with mock.patch.object(
            cli,
            "dry_run_account_recovery",
            return_value={"schema_version": vt.RECOVERY_DRY_RUN_SCHEMA},
        ) as dry:
            result = cli.dispatch(dry_args)
        self.assertEqual(result["schema_version"], vt.RECOVERY_DRY_RUN_SCHEMA)
        dry.assert_called_once_with(authorization.absolute())

        execute_args = parser.parse_args(
            [
                "elevenlabs-account-recover", "--authorization", str(authorization),
                "--execute", "--timeout", "12",
            ]
        )
        with (
            mock.patch.object(cli, "execute_account_recovery", return_value={"valid": True}) as execute,
            mock.patch.object(cli, "execute_account_verification") as legacy,
        ):
            self.assertEqual(cli.dispatch(execute_args), {"valid": True})
        execute.assert_called_once_with(authorization.absolute(), timeout=12.0)
        legacy.assert_not_called()

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

    def _blocked_prepared_worker(
        self,
        *,
        script: str = "import time; time.sleep(30)",
        extra_pass_fds: tuple[int, ...] = (),
    ) -> tuple[vt._PreparedVoiceTransferWorker, subprocess.Popen[bytes]]:
        child_command, parent_command = os.pipe()
        child_key, parent_key = os.pipe()
        child_body, parent_body = os.pipe()
        parent_result, child_result = os.pipe()
        inherited = (child_command, child_key, child_body, child_result, *extra_pass_fds)
        script = script.format(
            command_fd=child_command,
            key_fd=child_key,
            body_fd=child_body,
            result_fd=child_result,
            extra_fd=extra_pass_fds[0] if extra_pass_fds else -1,
        )
        process = subprocess.Popen(
            [
                vt._TRANSFER_WORKER_INTERPRETER_PATH,
                "-I",
                "-S",
                "-B",
                "-c",
                script,
            ],
            executable=vt._TRANSFER_WORKER_INTERPRETER_PATH,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            close_fds=True,
            pass_fds=inherited,
            env=dict(vt._TRANSFER_WORKER_ENV),
            start_new_session=True,
            text=False,
        )
        for descriptor in (child_command, child_key, child_body, child_result):
            os.close(descriptor)
        interpreter = vt._system_transfer_worker_interpreter_identity()
        worker = vt._PreparedVoiceTransferWorker(
            process=process,
            command_fd=parent_command,
            result_fd=parent_result,
            key_fd=parent_key,
            body_fd=parent_body,
            worker_source_path="/bound/worker.py",
            worker_source_sha256="a" * 64,
            interpreter_path=interpreter[0],
            interpreter_sha256=interpreter[1],
            python_version=interpreter[2],
            interpreter_identity=interpreter[3],
            pid=process.pid,
            process_group_id=process.pid,
        )
        self.addCleanup(vt._dispose_prepared_transfer_worker, worker)
        return worker, process

    def _valid_exchange_inputs(
        self,
        key: str = "unit-secret-abcd",
    ) -> tuple[bytes, bytearray, bytearray]:
        command = _worker_json_frame(
            {
                "action": "release_exact_transfer",
                "application_http_attempt_limit": 1,
                "body_bytes": vt.TRANSFER_BODY_BYTES,
                "body_sha256": vt.TRANSFER_BODY_SHA256,
                "child_deadline_monotonic_ns": time.monotonic_ns() + 1_000_000_000,
                "protocol": vt._TRANSFER_WORKER_PROTOCOL,
            }
        )
        key_frame = bytearray(_worker_body_frame(key.encode("ascii")))
        body_frame = bytearray(_worker_body_frame(b"\x00" * vt.TRANSFER_BODY_BYTES))
        return command, key_frame, body_frame

    def _worker_failure_result(self, **overrides: object) -> dict:
        value: dict[str, object] = {
            "application_fallbacks_used": 0,
            "application_http_attempts": 1,
            "application_redirects_followed": 0,
            "application_retries_made": 0,
            "content_encoding": None,
            "content_type": None,
            "failure_code": "provider_transport_failure",
            "http_status": None,
            "message": "result",
            "network_stack_address_selection_state": (
                "stdlib_internal_connection_selection_possible"
            ),
            "network_state": "application_request_started",
            "outcome": "failure",
            "protocol": vt._TRANSFER_WORKER_PROTOCOL,
            "provider_identifiers": {},
            "provider_usage": {},
            "request_state": "outcome_unknown",
            "response_body_disposition": "not_read",
            "response_byte_count_state": "none",
            "response_bytes": 0,
            "response_sha256": None,
            "response_state": "none",
            "success_body_follows": False,
        }
        value.update(overrides)
        return value

    def test_exact_worker_ready_is_pre_go_credential_free_and_reaped(self) -> None:
        before_fds = set(os.listdir("/dev/fd"))
        worker = vt._prepare_voice_transfer_worker(ready_timeout=3.0)
        process = worker.process
        self.assertIsNotNone(process)
        assert process is not None
        self.assertEqual(worker.state, "ready")
        self.assertEqual(worker.worker_source_sha256, sha256_file(vt._TRANSFER_WORKER_SOURCE_PATH))
        self.assertEqual(worker.interpreter_path, vt._TRANSFER_WORKER_INTERPRETER_PATH)
        self.assertEqual(worker.interpreter_sha256, vt._TRANSFER_WORKER_INTERPRETER_SHA256)
        self.assertEqual(worker.process_group_id, worker.pid)
        self.assertEqual(os.getsid(worker.pid), worker.pid)
        serialized_arguments = " ".join(str(item) for item in process.args)
        self.assertNotIn(vt.API_KEY_ENV, serialized_arguments)
        self.assertNotIn("xi-api-key", serialized_arguments)
        self.assertNotIn(vt.TRANSFER_BODY_SHA256, str(vt._TRANSFER_WORKER_ENV))
        self.assertTrue(vt._dispose_prepared_transfer_worker(worker))
        self.assertIsNotNone(process.poll())
        self.assertEqual(worker.state, "closed")
        self.assertEqual(set(os.listdir("/dev/fd")), before_fds)

    def test_parent_does_not_import_worker_before_descriptor_execution(self) -> None:
        source = Path(vt.__file__).read_text(encoding="utf-8")
        tree = ast.parse(source)
        imported = {
            alias.name
            for node in ast.walk(tree)
            if isinstance(node, (ast.Import, ast.ImportFrom))
            for alias in node.names
        }
        self.assertNotIn("elevenlabs_transfer_worker", imported)
        self.assertNotIn("oe_narration.elevenlabs_transfer_worker", imported)

    def test_worker_source_cannot_spawn_or_exec_descendants(self) -> None:
        source = vt._TRANSFER_WORKER_SOURCE_PATH.read_text(encoding="utf-8")
        tree = ast.parse(source)
        imported = {
            alias.name
            for node in ast.walk(tree)
            if isinstance(node, (ast.Import, ast.ImportFrom))
            for alias in node.names
        }
        called_names = {
            node.func.attr if isinstance(node.func, ast.Attribute) else node.func.id
            for node in ast.walk(tree)
            if isinstance(node, ast.Call)
            and isinstance(node.func, (ast.Attribute, ast.Name))
        }
        self.assertTrue({"subprocess", "multiprocessing"}.isdisjoint(imported))
        self.assertTrue(
            {
                "exec",
                "execv",
                "execve",
                "execl",
                "fork",
                "forkpty",
                "posix_spawn",
                "posix_spawnp",
                "Popen",
                "system",
            }.isdisjoint(called_names)
        )

    def test_worker_protocol_success_round_trip_uses_exact_shared_vocabulary(self) -> None:
        payload = b"safe-pcm"
        result = {
            "application_fallbacks_used": 0,
            "application_http_attempts": 1,
            "application_redirects_followed": 0,
            "application_retries_made": 0,
            "content_encoding": "identity",
            "content_type": "audio/pcm",
            "failure_code": None,
            "http_status": 200,
            "message": "result",
            "network_stack_address_selection_state": (
                "stdlib_internal_connection_selection_possible"
            ),
            "network_state": "application_request_started",
            "outcome": "success",
            "protocol": vt._TRANSFER_WORKER_PROTOCOL,
            "provider_identifiers": {"request-id": "safe-1"},
            "provider_usage": {"request-cost": 1},
            "request_state": "response_confirmed",
            "response_body_disposition": "raw_success_frame",
            "response_byte_count_state": "exact",
            "response_bytes": len(payload),
            "response_sha256": sha256_bytes(payload),
            "response_state": "body_complete",
            "success_body_follows": True,
        }
        raw = bytearray(b"".join(
            (
                _worker_json_frame(_worker_request_phase()),
                _worker_json_frame(_worker_headers_phase()),
                _worker_json_frame(result),
                _worker_body_frame(payload),
            )
        ))
        key_material = bytearray(b"unit-secret-abcd")
        response, snapshot = vt._parse_transfer_worker_exchange(
            raw,
            key_material=key_material,
        )
        self.assertIsNone(snapshot)
        assert response is not None
        self.assertEqual(response.payload, payload)
        self.assertEqual(response.response_sha256, sha256_bytes(payload))
        self.assertEqual(raw, bytearray())
        self.assertEqual(key_material, bytearray())

    def test_worker_protocol_failure_preserves_safe_header_evidence_without_body(self) -> None:
        body_digest = sha256_bytes(b"private-provider-error")
        result = {
            "application_fallbacks_used": 0,
            "application_http_attempts": 1,
            "application_redirects_followed": 0,
            "application_retries_made": 0,
            "content_encoding": "identity",
            "content_type": "text/plain",
            "failure_code": "provider_http_failure",
            "http_status": 401,
            "message": "result",
            "network_stack_address_selection_state": (
                "stdlib_internal_connection_selection_possible"
            ),
            "network_state": "application_request_started",
            "outcome": "failure",
            "protocol": vt._TRANSFER_WORKER_PROTOCOL,
            "provider_identifiers": {"request-id": "safe-2"},
            "provider_usage": {},
            "request_state": "response_confirmed",
            "response_body_disposition": "hash_count_only",
            "response_byte_count_state": "exact",
            "response_bytes": len(b"private-provider-error"),
            "response_sha256": body_digest,
            "response_state": "body_rejected",
            "success_body_follows": False,
        }
        raw = bytearray(b"".join(
            (
                _worker_json_frame(_worker_request_phase()),
                _worker_json_frame(
                    _worker_headers_phase(status=401, content_type="text/plain")
                ),
                _worker_json_frame(result),
            )
        ))
        key_material = bytearray(b"unit-secret-abcd")
        response, snapshot = vt._parse_transfer_worker_exchange(
            raw,
            key_material=key_material,
        )
        self.assertIsNone(response)
        assert snapshot is not None
        failure = vt._failure_from_transfer_worker_snapshot(snapshot)
        self.assertEqual(failure.code, "provider_http_failure")
        self.assertEqual(failure.provider_response_state, "body_rejected")
        self.assertEqual(failure.response_sha256, body_digest)
        self.assertTrue(failure.response_received)
        self.assertEqual(raw, bytearray())
        self.assertEqual(key_material, bytearray())

    def test_post_go_blocked_write_hits_absolute_deadline_and_immediate_kill(self) -> None:
        worker, process = self._blocked_prepared_worker()
        command, key_frame, body_frame = self._valid_exchange_inputs()
        started = time.monotonic()
        with self.assertRaises(pt._GuideExecutionFailure) as captured:
            vt._exchange_with_transfer_worker(
                worker,
                command_frame=command,
                key_frame=key_frame,
                body=body_frame,
                result_cap=vt._TRANSFER_WORKER_EXCHANGE_MAX_BYTES,
                deadline_ns=time.monotonic_ns() + 50_000_000,
            )
        elapsed = time.monotonic() - started
        self.assertEqual(captured.exception.code, "provider_request_elapsed_cap_exceeded")
        self.assertTrue(captured.exception.post_budget_consumed)
        self.assertEqual(captured.exception.provider_request_state, "unknown_after_go")
        self.assertEqual(captured.exception.provider_response_state, "unknown")
        self.assertFalse(captured.exception.retry_or_replay_permitted)
        self.assertLess(elapsed, 0.35)
        self.assertIsNotNone(process.poll())
        self.assertIsNone(worker.process)
        self.assertTrue(all(value == 0 for value in key_frame))
        self.assertEqual(
            (worker.command_fd, worker.key_fd, worker.body_fd, worker.result_fd),
            (-1, -1, -1, -1),
        )

    def test_post_go_selector_allocation_failure_kills_locally_and_zeros_key(self) -> None:
        worker, process = self._blocked_prepared_worker()
        command, key_frame, body_frame = self._valid_exchange_inputs()
        with (
            mock.patch.object(vt.selectors, "DefaultSelector", side_effect=MemoryError),
            self.assertRaises(MemoryError),
        ):
            vt._exchange_with_transfer_worker(
                worker,
                command_frame=command,
                key_frame=key_frame,
                body=body_frame,
                result_cap=vt._TRANSFER_WORKER_EXCHANGE_MAX_BYTES,
                deadline_ns=time.monotonic_ns() + 1_000_000_000,
            )
        self.assertIsNotNone(process.poll())
        self.assertIsNone(worker.process)
        self.assertTrue(all(value == 0 for value in key_frame))
        self.assertEqual(
            (worker.command_fd, worker.key_fd, worker.body_fd, worker.result_fd),
            (-1, -1, -1, -1),
        )

    def test_unconfirmed_reap_preserves_live_handle_and_surfaces_containment_failure(self) -> None:
        worker, process = self._blocked_prepared_worker()
        command, key_frame, body_frame = self._valid_exchange_inputs()
        with (
            mock.patch.object(vt, "_kill_and_reap_transfer_worker", return_value=False) as reap,
            self.assertRaises(pt._GuideExecutionFailure) as captured,
        ):
            vt._exchange_with_transfer_worker(
                worker,
                command_frame=command,
                key_frame=key_frame,
                body=body_frame,
                result_cap=vt._TRANSFER_WORKER_EXCHANGE_MAX_BYTES,
                deadline_ns=time.monotonic_ns() + 20_000_000,
            )
        self.assertEqual(captured.exception.code, "isolated_worker_reap_failure")
        self.assertEqual(
            captured.exception.child_containment_state,
            "sigkill_sent_reap_unconfirmed",
        )
        self.assertTrue(captured.exception.post_budget_consumed)
        self.assertIs(worker.process, process)
        self.assertEqual(worker.state, "go_consumed")
        self.assertGreaterEqual(reap.call_count, 2)
        self.assertTrue(all(value == 0 for value in key_frame))

    def test_headers_rejected_is_received_without_claiming_validated_headers(self) -> None:
        result = self._worker_failure_result(
            failure_code="provider_response_headers_invalid",
            http_status=200,
            request_state="response_confirmed",
            response_state="headers_rejected",
        )
        raw = bytearray(
            _worker_json_frame(_worker_request_phase()) + _worker_json_frame(result)
        )
        response, snapshot = vt._parse_transfer_worker_exchange(
            raw,
            key_material=bytearray(b"unit-secret-abcd"),
        )
        self.assertIsNone(response)
        assert snapshot is not None
        failure = vt._failure_from_transfer_worker_snapshot(snapshot)
        self.assertTrue(failure.response_received)
        self.assertEqual(failure.http_status, 200)
        self.assertEqual(failure.provider_request_state, "response_confirmed")
        self.assertEqual(failure.provider_response_state, "headers_rejected")

    def test_unknown_worker_state_never_implies_response_received(self) -> None:
        failure = vt._failure_from_transfer_worker_snapshot(
            vt._TransferWorkerFailureSnapshot(
                code="isolated_worker_protocol_failure",
                response_state="unknown",
                request_state="unknown_after_go",
            )
        )
        self.assertFalse(failure.response_received)
        self.assertEqual(failure.provider_response_state, "unknown")

    def test_malformed_terminal_preserves_last_validated_phase_and_status(self) -> None:
        malformed_terminal = _worker_json_frame(
            {"message": "not-a-result", "protocol": vt._TRANSFER_WORKER_PROTOCOL}
        )
        raw = bytearray(
            _worker_json_frame(_worker_request_phase())
            + _worker_json_frame(_worker_headers_phase(status=202))
            + malformed_terminal
        )
        response, snapshot = vt._parse_transfer_worker_exchange(
            raw,
            key_material=bytearray(b"unit-secret-abcd"),
        )
        self.assertIsNone(response)
        assert snapshot is not None
        self.assertEqual(snapshot.application_http_attempts, 1)
        self.assertEqual(snapshot.request_state, "response_confirmed")
        self.assertEqual(snapshot.response_state, "headers_confirmed")
        self.assertEqual(snapshot.http_status, 202)

    def test_secret_terminal_preserves_phase_one_but_never_secret(self) -> None:
        secret = bytearray(b"unit-secret-never-serialize")
        raw = bytearray(
            _worker_json_frame(_worker_request_phase())
            + _worker_body_frame(b"malformed-terminal-" + bytes(secret))
        )
        response, snapshot = vt._parse_transfer_worker_exchange(
            raw,
            key_material=secret,
        )
        self.assertIsNone(response)
        assert snapshot is not None
        self.assertEqual(snapshot.code, "isolated_worker_secret_echo_detected")
        self.assertEqual(snapshot.application_http_attempts, 1)
        self.assertEqual(snapshot.request_state, "outcome_unknown")
        self.assertEqual(snapshot.response_state, "none")
        self.assertEqual(raw, bytearray())
        self.assertEqual(secret, bytearray())

    def test_worker_key_scan_is_bounded_on_large_adversarial_near_match(self) -> None:
        raw = bytearray(b"a" * vt._TRANSFER_WORKER_RESULT_BODY_MAX_BYTES)
        key = bytearray(b"a" * (vt._TRANSFER_WORKER_KEY_FRAME_MAX_BYTES - 1) + b"b")
        started = time.monotonic()
        self.assertFalse(vt._buffer_contains(raw, key))
        self.assertLess(time.monotonic() - started, 0.5)
        vt._zero_mutable_buffer(raw)
        vt._zero_mutable_buffer(key)

    def test_child_deadline_mapping_is_conservative_across_offset_epochs(self) -> None:
        child_ready_before_send = 16_000_000
        ready_transit_ns = 5_000_000
        parent_ready_received = 95_000_000_000_000
        parent_deadline = parent_ready_received + 1_000_000_000
        worker = SimpleNamespace(
            child_monotonic_ns_at_ready=child_ready_before_send,
            parent_ready_received_ns=parent_ready_received,
        )
        mapped = vt._map_transfer_worker_child_deadline(
            worker,
            parent_deadline,
            parent_now_ns=parent_ready_received,
        )
        true_child_clock_at_parent_deadline = (
            child_ready_before_send + ready_transit_ns + 1_000_000_000
        )
        self.assertEqual(mapped, child_ready_before_send + 1_000_000_000)
        self.assertLessEqual(mapped, true_child_clock_at_parent_deadline)
        with self.assertRaises(ValidationError):
            vt._map_transfer_worker_child_deadline(
                worker,
                parent_ready_received,
                parent_now_ns=parent_ready_received,
            )
        inclusive_now = parent_ready_received + 29_000_000_000
        inclusive_deadline = inclusive_now + 300_000_000_000
        self.assertEqual(
            vt._map_transfer_worker_child_deadline(
                worker,
                inclusive_deadline,
                parent_now_ns=inclusive_now,
            ),
            child_ready_before_send + 329_000_000_000,
        )
        with self.assertRaises(ValidationError):
            vt._map_transfer_worker_child_deadline(
                worker,
                inclusive_deadline + 1,
                parent_now_ns=inclusive_now,
            )
        with self.assertRaises(ValidationError):
            vt._map_transfer_worker_child_deadline(
                worker,
                parent_ready_received + 32_000_000_000,
                parent_now_ns=parent_ready_received + 31_000_000_000,
            )
        worker.child_monotonic_ns_at_ready = 0
        with self.assertRaises(ValidationError):
            vt._map_transfer_worker_child_deadline(
                worker,
                parent_deadline,
                parent_now_ns=parent_ready_received,
            )

    def test_parent_exchange_keeps_parent_deadline_and_sends_mapped_child_deadline(self) -> None:
        parent_ready_received = time.monotonic_ns() - 1_000_000
        child_ready = 16_000_000
        worker = SimpleNamespace(
            state="ready",
            process=object(),
            child_monotonic_ns_at_ready=child_ready,
            parent_ready_received_ns=parent_ready_received,
        )
        terminal = self._worker_failure_result(
            application_http_attempts=0,
            failure_code="worker_internal_failure",
            network_state="not_started",
            request_state="not_started",
        )
        captured: dict[str, object] = {}

        def release(*_args: object, **kwargs: object) -> bytearray:
            captured["parent_deadline_ns"] = kwargs["deadline_ns"]
            command_frame = kwargs["command_frame"]
            assert isinstance(command_frame, bytes)
            captured["command"] = vt._decode_strict_worker_json(
                command_frame[vt._TRANSFER_WORKER_FRAME_LENGTH_STRUCT.size :],
                vt._TRANSFER_WORKER_COMMAND_FRAME_MAX_BYTES,
                "test command",
            )
            worker.state = "go_consumed"
            return bytearray(_worker_json_frame(terminal))

        key = bytearray(b"unit-key-offset-clock")
        body = bytearray(b"x" * vt.TRANSFER_BODY_BYTES)
        with (
            mock.patch.object(vt, "_revalidate_prepared_transfer_worker"),
            mock.patch.object(vt, "sha256_bytes", return_value=vt.TRANSFER_BODY_SHA256),
            mock.patch.object(vt, "_exchange_with_transfer_worker", side_effect=release),
            mock.patch.object(vt, "_dispose_prepared_transfer_worker", return_value=True),
            self.assertRaises(pt._GuideExecutionFailure) as failure,
        ):
            vt._perform_prepared_voice_transfer(
                worker,
                api_key_material=key,
                body=body,
                timeout=1.0,
            )
        self.assertEqual(failure.exception.code, "worker_internal_failure")
        command = captured["command"]
        assert isinstance(command, dict)
        self.assertEqual(set(command), vt._TRANSFER_WORKER_COMMAND_KEYS)
        parent_deadline = captured["parent_deadline_ns"]
        assert isinstance(parent_deadline, int)
        self.assertEqual(
            command["child_deadline_monotonic_ns"],
            child_ready + (parent_deadline - parent_ready_received),
        )
        self.assertGreater(parent_deadline, time.monotonic_ns() - 2_000_000_000)

    def test_result_state_relations_reject_overclaim_after_phase_one(self) -> None:
        result = self._worker_failure_result(
            request_state="response_confirmed",
            response_state="headers_confirmed",
        )
        raw = bytearray(
            _worker_json_frame(_worker_request_phase()) + _worker_json_frame(result)
        )
        _response, snapshot = vt._parse_transfer_worker_exchange(
            raw,
            key_material=bytearray(b"unit-secret-abcd"),
        )
        assert snapshot is not None
        self.assertEqual(snapshot.code, "isolated_worker_protocol_failure")
        self.assertEqual(snapshot.application_http_attempts, 1)
        self.assertEqual(snapshot.request_state, "outcome_unknown")
        self.assertEqual(snapshot.response_state, "none")

    def test_unexpected_child_exit_after_go_is_terminal_and_reaped(self) -> None:
        worker, process = self._blocked_prepared_worker(
            script=(
                "import os\n"
                "for descriptor in ({command_fd}, {key_fd}, {body_fd}):\n"
                "    while os.read(descriptor, 65536):\n"
                "        pass\n"
                "os._exit(7)\n"
            )
        )
        command, key_frame, body_frame = self._valid_exchange_inputs()
        with self.assertRaises(pt._GuideExecutionFailure) as captured:
            vt._exchange_with_transfer_worker(
                worker,
                command_frame=command,
                key_frame=key_frame,
                body=body_frame,
                result_cap=vt._TRANSFER_WORKER_EXCHANGE_MAX_BYTES,
                deadline_ns=time.monotonic_ns() + 1_000_000_000,
            )
        self.assertEqual(captured.exception.code, "isolated_worker_exit_failure")
        self.assertTrue(captured.exception.post_budget_consumed)
        self.assertIsNotNone(process.poll())
        self.assertIsNone(worker.process)
        self.assertTrue(all(value == 0 for value in key_frame))

    def test_immediate_cleanup_kills_same_group_descendant(self) -> None:
        pid_reader, pid_writer = os.pipe()
        self.addCleanup(vt._close_transfer_worker_fd, pid_reader)
        self.addCleanup(vt._close_transfer_worker_fd, pid_writer)
        worker, _process = self._blocked_prepared_worker(
            script=(
                "import os, time\n"
                "child = os.fork()\n"
                "if child == 0:\n"
                "    time.sleep(30)\n"
                "else:\n"
                "    os.write({extra_fd}, str(child).encode('ascii'))\n"
                "    time.sleep(30)\n"
            ),
            extra_pass_fds=(pid_writer,),
        )
        os.close(pid_writer)
        pid_writer = -1
        descendant_pid = int(os.read(pid_reader, 32).decode("ascii"))
        os.close(pid_reader)
        pid_reader = -1
        command, key_frame, body_frame = self._valid_exchange_inputs()
        with self.assertRaises(pt._GuideExecutionFailure):
            vt._exchange_with_transfer_worker(
                worker,
                command_frame=command,
                key_frame=key_frame,
                body=body_frame,
                result_cap=vt._TRANSFER_WORKER_EXCHANGE_MAX_BYTES,
                deadline_ns=time.monotonic_ns() + 50_000_000,
            )
        descendant_gone = False
        for _ in range(100):
            try:
                os.kill(descendant_pid, 0)
            except ProcessLookupError:
                descendant_gone = True
                break
            time.sleep(0.01)
        self.assertTrue(descendant_gone, "same-group descendant survived immediate cleanup")

    def test_sensitive_wrapper_traceback_holds_only_scrubbed_buffers(self) -> None:
        key = bytearray(b"unit-key-traceback-sentinel-9876")
        output = b"private-output-traceback-sentinel-5432"
        raw = bytearray(
            _worker_json_frame(_worker_request_phase())
            + _worker_body_frame(output + bytes(key))
        )
        body = bytearray(b"x" * vt.TRANSFER_BODY_BYTES)
        parent_ready_ns = time.monotonic_ns()
        worker = SimpleNamespace(
            state="ready",
            process=object(),
            child_monotonic_ns_at_ready=10_000_000,
            parent_ready_received_ns=parent_ready_ns,
        )

        def release(*_args: object, **_kwargs: object) -> bytearray:
            worker.state = "go_consumed"
            return raw

        with (
            mock.patch.object(vt, "_revalidate_prepared_transfer_worker"),
            mock.patch.object(vt, "sha256_bytes", return_value=vt.TRANSFER_BODY_SHA256),
            mock.patch.object(vt, "_exchange_with_transfer_worker", side_effect=release),
            mock.patch.object(vt, "_dispose_prepared_transfer_worker", return_value=True),
            self.assertRaises(pt._GuideExecutionFailure) as captured,
        ):
            vt._perform_prepared_voice_transfer(
                worker,
                api_key_material=key,
                body=body,
                timeout=1.0,
            )
        self.assertEqual(captured.exception.code, "isolated_worker_secret_echo_detected")
        self.assertEqual(key, bytearray())
        self.assertEqual(body, bytearray())
        self.assertEqual(raw, bytearray())
        traceback_frame = captured.exception.__traceback__
        while traceback_frame is not None:
            if Path(traceback_frame.tb_frame.f_code.co_filename) == Path(vt.__file__):
                local_text = repr(traceback_frame.tb_frame.f_locals)
                self.assertNotIn("unit-key-traceback-sentinel", local_text)
                self.assertNotIn("private-output-traceback-sentinel", local_text)
            traceback_frame = traceback_frame.tb_next

    @staticmethod
    def _write_private_json(path: Path, document: dict, *, mode: int = 0o600) -> str:
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = (
            json.dumps(document, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
        ).encode("utf-8")
        path.write_bytes(payload)
        path.chmod(mode)
        return sha256_bytes(payload)

    def _recovery_transfer_source_proof(
        self,
        bundle: SimpleNamespace,
        *,
        override: object | None = None,
    ):
        runtime_commit = bundle.runtime_bindings["git_commit"]
        head_commit = "b" * 40
        repository = pt._guide_repository_root()
        runtime_paths = {
            relative: path
            for relative, path in vt._recovery_transfer_runtime_files().values()
        }

        def bound_git(_bindings: dict, arguments: list[str], **_kwargs: object) -> bytes:
            if callable(override):
                overridden = override(arguments)
                if overridden is not None:
                    return overridden
            if arguments[:2] == ["cat-file", "-e"]:
                return b""
            if arguments[:3] == ["rev-list", "--parents", "-n"]:
                commit = arguments[-1]
                if commit == runtime_commit:
                    return f"{runtime_commit} {vt.RECOVERY_TRANSFER_OUTCOME_COMMIT}\n".encode()
                raise AssertionError(arguments)
            if arguments and arguments[0] == "diff":
                revision = arguments[-1]
                if revision != f"{vt.RECOVERY_TRANSFER_OUTCOME_COMMIT}..{runtime_commit}":
                    raise AssertionError(arguments)
                return b"".join(
                    b"M\x00" + relative.encode("utf-8") + b"\x00"
                    for relative in sorted(runtime_paths)
                )
            if arguments == ["rev-parse", "HEAD"]:
                return (head_commit + "\n").encode()
            if arguments[:2] == ["merge-base", "--is-ancestor"]:
                return b""
            if arguments[:2] == ["ls-files", "--stage"]:
                return b""
            if arguments[:3] == ["check-ignore", "--no-index", "-v"]:
                relative = arguments[-1]
                selected_path = repository / relative
                fixture_root = pt._document_root(selected_path)
                ignore_relative = (fixture_root / ".gitignore").relative_to(repository).as_posix()
                return f"{ignore_relative}:1:outputs/raw/\t{relative}\n".encode()
            if arguments and arguments[0] == "ls-tree":
                return b""
            if arguments and arguments[0] == "show":
                _commit, separator, relative = arguments[-1].partition(":")
                if not separator:
                    raise AssertionError(arguments)
                path = runtime_paths.get(relative, repository / relative)
                return path.read_bytes()
            raise AssertionError(arguments)

        return (
            mock.patch.object(vt, "_verify_local_git_object_store"),
            mock.patch.object(vt, "_bound_git", side_effect=bound_git),
            mock.patch.object(vt, "_verify_recovery_private_capture_git_state"),
        )

    def _validate_recovery_transfer_bundle(
        self,
        bundle: SimpleNamespace,
        *,
        git_override: object | None = None,
    ) -> dict:
        source_patches = self._recovery_transfer_source_proof(
            bundle,
            override=git_override,
        )
        with (
            source_patches[0],
            source_patches[1],
            source_patches[2],
            mock.patch.object(
                vt,
                "_target",
                return_value=bundle.authorization["target"],
            ),
            mock.patch.object(
                vt,
                "_read_recovery_dotenv_key",
                side_effect=AssertionError("validation read a credential"),
            ),
            mock.patch.object(
                urllib.request,
                "build_opener",
                side_effect=AssertionError("validation attempted network"),
            ),
        ):
            return vt.validate_recovery_evidence_voice_transfer_authorization(
                bundle.authorization_path,
                bundle.plan,
                bundle.canonical,
            )

    def _rewrite_recovery_transfer_data_and_authorization(
        self,
        bundle: SimpleNamespace,
    ) -> None:
        data_sha = self._write_private_json(bundle.data_path, bundle.data_document)
        bundle.authorization["prerequisites"]["elevenlabs_data_use"]["sha256"] = data_sha
        self._write_private_json(bundle.authorization_path, bundle.authorization)

    def _rewrite_recovery_transfer_account_chain(
        self,
        bundle: SimpleNamespace,
    ) -> None:
        account_sha = self._write_private_json(bundle.account_path, bundle.account_document)
        bundle.authorization["account_authentication_evidence"][
            "calibrated_account_assurance"
        ]["sha256"] = account_sha
        bundle.data_document["evidence"]["calibrated_account_assurance"][
            "sha256"
        ] = account_sha
        self._rewrite_recovery_transfer_data_and_authorization(bundle)

    def _rewrite_recovery_transfer_rights_chain(
        self,
        bundle: SimpleNamespace,
    ) -> None:
        rights_sha = self._write_private_json(bundle.rights_path, bundle.rights_document)
        bundle.authorization["prerequisites"]["target_voice_rights"][
            "sha256"
        ] = rights_sha
        bundle.data_document["evidence"]["target_rights"]["sha256"] = rights_sha
        self._rewrite_recovery_transfer_data_and_authorization(bundle)

    def _activate_recovery_transfer_bundle(
        self,
        bundle: SimpleNamespace,
    ) -> SimpleNamespace:
        draft_sha = sha256_file(bundle.authorization_path)
        provider_latch = pt._strict_json_bytes(
            (bundle.fixture / vt.RECOVERY_TRANSFER_PROVIDER_LATCH_PATH).read_bytes(),
            "unit provider latch",
        )
        bundle.authorization.update(
            {
                "authorization_id": vt.RECOVERY_TRANSFER_ACTIVE_ID,
                "status": "active",
                "provider_action_authorized": True,
                "credential_delivery": vt._recovery_transfer_credential_delivery(
                    True,
                    fingerprint=provider_latch["credential_fingerprint_sha256"],
                    suffix_sha256=provider_latch["browser_suffix_sha256"],
                ),
                "evidence_baseline": {
                    "state": "verified",
                    "evidence_commit": "c" * 40,
                    "draft_authorization": {
                        "path": vt.RECOVERY_TRANSFER_DRAFT_PATH,
                        "sha256": draft_sha,
                    },
                    "calibrated_account_assurance": {
                        "path": vt.RECOVERY_TRANSFER_ACCOUNT_ASSURANCE_PATH,
                        "sha256": sha256_file(bundle.account_path),
                    },
                    "data_use_assurance": {
                        "path": vt.RECOVERY_TRANSFER_DATA_USE_ASSURANCE_PATH,
                        "sha256": sha256_file(bundle.data_path),
                    },
                    "target_rights": {
                        "path": vt.RECOVERY_TRANSFER_TARGET_RIGHTS_PATH,
                        "sha256": sha256_file(bundle.rights_path),
                    },
                    "fresh_browser_readiness": {
                        "path": bundle.browser_path.relative_to(bundle.fixture).as_posix(),
                        "sha256": sha256_file(bundle.browser_path),
                    },
                },
                "authorized_limits": vt._transfer_limits(True),
                "artifacts": vt._recovery_transfer_artifacts(True),
                "consumption": vt._recovery_transfer_consumption(True),
                "materialized_at": "2026-08-26T14:22:00Z",
                "expires_at": "2026-08-26T14:50:00Z",
                "execution_ready": True,
                "blockers": [],
            }
        )
        active_path = bundle.fixture / vt.RECOVERY_TRANSFER_ACTIVE_PATH
        self._write_private_json(active_path, bundle.authorization)
        bundle.authorization_path = active_path.resolve(strict=True)
        return bundle

    def _assert_recovery_transfer_traceback_scrubbed(
        self,
        error: BaseException,
        bundle: SimpleNamespace,
    ) -> None:
        selected_raw = (bundle.fixture / vt.SELECTED_GUIDE_PATH).read_bytes()
        selected_chunk = next(
            selected_raw[offset : offset + 32]
            for offset in range(44, len(selected_raw) - 32, 997)
            if len(set(selected_raw[offset : offset + 32])) >= 12
        )
        selected_probe = repr(selected_chunk)[2:-1]
        self.assertIn(selected_probe, repr(selected_raw))
        probes = (
            selected_probe,
            "unit-redacted-browser-capture",
            "V1-ELEVENLABS-RECOVERY-TRANSFER-DATA-USE-ASSURANCE",
        )
        traceback_frame = error.__traceback__
        runtime_frames = 0
        while traceback_frame is not None:
            if Path(traceback_frame.tb_frame.f_code.co_filename) == Path(vt.__file__):
                runtime_frames += 1
                local_text = repr(traceback_frame.tb_frame.f_locals)
                for index, probe in enumerate(probes):
                    if probe in local_text:
                        self.fail(
                            "private traceback probe "
                            f"{index} retained in {traceback_frame.tb_frame.f_code.co_name}"
                        )
            traceback_frame = traceback_frame.tb_next
        self.assertGreater(runtime_frames, 0, "injected failure exposed no runtime traceback frame")

    def _recovery_transfer_draft_bundle(self) -> SimpleNamespace:
        # Keep the disposable fixture below the repository so descriptor-bound
        # Git-path proofs can still express every copied record as a repo-relative path.
        temporary = tempfile.TemporaryDirectory(dir=pt._guide_repository_root())
        self.addCleanup(temporary.cleanup)
        blueprint = Path(temporary.name) / "operator-blueprint-v2"
        narration = blueprint / "02-narration-production"
        fixtures = narration / "fixtures"
        fixture = fixtures / vt.FIXTURE_ID
        shutil.copytree(self.fixture, fixture, copy_function=shutil.copy2)

        canonical = fixtures / "step2-v0.2-ai-visibility-v1.1" / "identity" / "canonical-w.txt"
        canonical.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(self.canonical_w, canonical)
        for relative in (
            vt.RECOVERY_TRANSFER_ORIGINAL_C_SELECTION_PATH,
            vt.RECOVERY_TRANSFER_ORIGINAL_C_SAVE_PATH,
        ):
            source = self.root.parent / relative
            destination = blueprint / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)

        source_envelope = self.fixture / "performance-envelope.json"
        envelope_document = pt._strict_json_bytes(
            source_envelope.read_bytes(),
            "unit performance envelope",
        )
        script_relative = envelope_document["script"]["path"]
        source_script = (source_envelope.parent / script_relative).resolve(strict=True)
        destination_script = fixture / script_relative
        destination_script.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_script, destination_script)

        plan = fixture / "performance-transfer-plan.json"
        plan_dry = pt.validate_performance_transfer_plan(plan, canonical)
        runtime_bindings = vt.expected_recovery_transfer_runtime_bindings(draft=True)
        runtime_bindings["git_commit"] = "a" * 40
        authority = vt._recovery_transfer_zero_authority()
        scope_approval = vt._recovery_transfer_scope_approval()

        account_recorded_at = "2026-08-26T14:10:00Z"
        rights_recorded_at = "2026-08-26T14:10:00Z"
        browser_observed_at = "2026-08-26T14:20:00Z"
        data_recorded_at = "2026-08-26T14:21:00Z"
        materialized_at = "2026-08-26T14:22:00Z"

        account_document = {
            "schema_version": "oe-elevenlabs-recovery-calibrated-account-assurance-v1",
            "record_id": "V1-ELEVENLABS-RECOVERY-CALIBRATED-ACCOUNT-ASSURANCE",
            "status": "calibrated_non_authorizing",
            "provider": "elevenlabs",
            "recorded_at": account_recorded_at,
            "outcome_commit": vt.RECOVERY_TRANSFER_HISTORICAL_ACCOUNT_OUTCOME_COMMIT,
            "recovery_evidence": {
                "recovery_authorization": {
                    "path": vt.RECOVERY_TRANSFER_ACCOUNT_AUTH_PATH,
                    "sha256": vt.RECOVERY_TRANSFER_ACCOUNT_AUTH_SHA256,
                },
                "credential_read_latch": {
                    "path": vt.RECOVERY_TRANSFER_CREDENTIAL_LATCH_PATH,
                    "sha256": vt.RECOVERY_TRANSFER_CREDENTIAL_LATCH_SHA256,
                },
                "provider_call_latch": {
                    "path": vt.RECOVERY_TRANSFER_PROVIDER_LATCH_PATH,
                    "sha256": vt.RECOVERY_TRANSFER_PROVIDER_LATCH_SHA256,
                },
                "http_200_failure_receipt": {
                    "path": vt.RECOVERY_TRANSFER_FAILURE_PATH,
                    "sha256": vt.RECOVERY_TRANSFER_FAILURE_SHA256,
                },
                "terminal_disposition": {
                    "path": vt.RECOVERY_TRANSFER_DISPOSITION_PATH,
                    "sha256": vt.RECOVERY_TRANSFER_DISPOSITION_SHA256,
                },
            },
            "observed_outcome": {
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
            },
            "calibrated_interpretation": {
                "credential_authentication_inference": (
                    vt.RECOVERY_TRANSFER_AUTHENTICATION_INFERENCE_STATE
                ),
                "authentication_conclusion": vt.RECOVERY_TRANSFER_AUTHENTICATION_CONCLUSION,
                "response_body_contents_state": "unknown_not_read",
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
                "safe_conclusion": vt.RECOVERY_TRANSFER_SAFE_CONCLUSION,
            },
            "terminality": {
                "automatic_retry_permitted": False,
                "retry_or_resumption": False,
                "recovery_authorization_reusable": False,
                "credential_read_latch_reusable": False,
                "provider_call_latch_reusable": False,
                "future_action_requires_separate_reviewed_committed_transaction_basis": True,
            },
            "authority": copy.deepcopy(authority),
        }
        account_path = fixture / vt.RECOVERY_TRANSFER_ACCOUNT_ASSURANCE_PATH
        account_sha = self._write_private_json(account_path, account_document)

        png_path = (
            fixture
            / "evidence/browser-readiness/"
            "V1-ELEVENLABS-RECOVERY-TRANSFER-BROWSER-READINESS.20260826T142000Z.png"
        )
        png_path.parent.mkdir(parents=True, exist_ok=True)
        png_bytes = b"\x89PNG\r\n\x1a\nunit-redacted-browser-capture"
        png_path.write_bytes(png_bytes)
        png_path.chmod(0o600)
        png_sha = sha256_bytes(png_bytes)

        historical_browser = fixture / vt.RECOVERY_TRANSFER_HISTORICAL_BROWSER_PATH
        browser_document = pt._strict_json_bytes(
            historical_browser.read_bytes(),
            "unit historical browser readiness",
        )
        browser_document["observed_at"] = browser_observed_at
        browser_document["capture"] = {
            "path": png_path.relative_to(fixture).as_posix(),
            "sha256": png_sha,
        }
        browser_path = png_path.with_suffix(".json")
        browser_sha = self._write_private_json(browser_path, browser_document)

        rights_document = {
            "schema_version": "oe-elevenlabs-recovery-evidence-voice-transfer-rights-v1",
            "record_id": "V1-ELEVENLABS-RECOVERY-TRANSFER-TARGET-RIGHTS",
            "status": "owner_scope_recorded_non_authorizing",
            "provider": "elevenlabs",
            "recorded_at": rights_recorded_at,
            "owner": vt.RECOVERY_TRANSFER_OWNER,
            "transaction_basis_id": vt.RECOVERY_TRANSFER_RIGHTS_TRANSACTION_BASIS_ID,
            "evidence": {
                "owner_audition_and_bounded_transfer_approval": {
                    "path": vt.RECOVERY_TRANSFER_OWNER_APPROVAL_PATH,
                    "sha256": vt.RECOVERY_TRANSFER_OWNER_APPROVAL_SHA256,
                },
                "guide_qa": {
                    "path": vt.RECOVERY_TRANSFER_GUIDE_QA_PATH,
                    "sha256": vt.RECOVERY_TRANSFER_GUIDE_QA_SHA256,
                },
                "owner_selection": {
                    "path": vt.RECOVERY_TRANSFER_GUIDE_SELECTION_PATH,
                    "sha256": vt.RECOVERY_TRANSFER_GUIDE_SELECTION_SHA256,
                },
                "performance_transfer_plan": {
                    "path": "performance-transfer-plan.json",
                    "sha256": plan_dry["plan_sha256"],
                },
                "official_media_contract": {
                    "path": vt.MEDIA_CONTRACT_BASIS_PATH,
                    "sha256": vt.MEDIA_CONTRACT_BASIS_SHA256,
                },
            },
            "original_c_provenance": {
                "owner_selection": {
                    "path": vt.RECOVERY_TRANSFER_ORIGINAL_C_SELECTION_PATH,
                    "sha256": vt.RECOVERY_TRANSFER_ORIGINAL_C_SELECTION_SHA256,
                },
                "saved_voice_receipt": {
                    "path": vt.RECOVERY_TRANSFER_ORIGINAL_C_SAVE_PATH,
                    "sha256": vt.RECOVERY_TRANSFER_ORIGINAL_C_SAVE_SHA256,
                },
            },
            "exact_scope": {
                "method": "POST",
                "endpoint": pt.TRANSFER_ENDPOINT,
                "target_voice_id": pt.TRANSFER_TARGET_VOICE_ID,
                "voice_owner": vt.RECOVERY_TRANSFER_OWNER,
                "consent_owner": vt.RECOVERY_TRANSFER_OWNER,
                "exact_guide_sha256": vt.SELECTED_GUIDE_SHA256,
                "owner_scope_voice_changer_permitted": True,
                "bounded_microtest_only": True,
                "primary_request_sha256": vt.TRANSFER_OPT_OUT_REQUEST_SHA256,
                "primary_multipart_body_sha256": vt.TRANSFER_BODY_SHA256,
                "primary_multipart_body_bytes": vt.TRANSFER_BODY_BYTES,
                "normalized_http_request_sha256": (
                    vt.TRANSFER_OPT_OUT_NORMALIZED_REQUEST_SHA256
                ),
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
            },
            "owner_authority_calibration": copy.deepcopy(scope_approval),
            "authority": copy.deepcopy(authority),
        }
        rights_path = fixture / vt.RECOVERY_TRANSFER_TARGET_RIGHTS_PATH
        rights_sha = self._write_private_json(rights_path, rights_document)

        official_path = fixture / "evidence/V1-ELEVENLABS-DATA-USE-OFFICIAL-BASIS.20260826T104709Z.json"
        data_document = {
            "schema_version": "oe-elevenlabs-recovery-evidence-data-use-assurance-v1",
            "record_id": vt.RECOVERY_TRANSFER_DATA_USE_ASSURANCE_ID,
            "status": "verified_fresh_non_authorizing",
            "provider": "elevenlabs",
            "recorded_at": data_recorded_at,
            "owner": vt.RECOVERY_TRANSFER_OWNER,
            "transaction_basis_id": vt.RECOVERY_TRANSFER_TRANSACTION_BASIS_ID,
            "exact_guide": {
                "path": vt.SELECTED_GUIDE_PATH,
                "sha256": vt.SELECTED_GUIDE_SHA256,
                "byte_count": vt.SELECTED_GUIDE_BYTES,
                "duration_seconds": vt.SELECTED_GUIDE_DURATION_SECONDS,
            },
            "evidence": {
                "fresh_browser_readiness": {
                    "path": browser_path.relative_to(fixture).as_posix(),
                    "sha256": browser_sha,
                },
                "fresh_browser_capture": {
                    "path": png_path.relative_to(fixture).as_posix(),
                    "sha256": png_sha,
                },
                "official_data_use_basis": {
                    "path": official_path.relative_to(fixture).as_posix(),
                    "sha256": sha256_file(official_path),
                },
                "calibrated_account_assurance": {
                    "path": vt.RECOVERY_TRANSFER_ACCOUNT_ASSURANCE_PATH,
                    "sha256": account_sha,
                },
                "target_rights": {
                    "path": vt.RECOVERY_TRANSFER_TARGET_RIGHTS_PATH,
                    "sha256": rights_sha,
                },
                "terminal_disposition": {
                    "path": vt.RECOVERY_TRANSFER_DISPOSITION_PATH,
                    "sha256": vt.RECOVERY_TRANSFER_DISPOSITION_SHA256,
                },
                "prior_zero_provider_transfer_disposition": {
                    "path": vt.RECOVERY_TRANSFER_PRIOR_DISPOSITION_PATH,
                    "sha256": vt.RECOVERY_TRANSFER_PRIOR_DISPOSITION_SHA256,
                },
                "owner_audition_and_bounded_transfer_approval": {
                    "path": vt.RECOVERY_TRANSFER_OWNER_APPROVAL_PATH,
                    "sha256": vt.RECOVERY_TRANSFER_OWNER_APPROVAL_SHA256,
                },
            },
            "fresh_observation": {
                "observed_at": browser_observed_at,
                "improve_models_for_everyone": False,
                "update_completed": True,
                "protection_mode": pt.ACCOUNT_TRAINING_OPT_OUT_PROTECTION,
                "protection_effective_for_new_submissions": True,
                "fresh_at_recorded_at": True,
                "freshness_reference": "recorded_at",
                "freshness_window_seconds": vt.DATA_USE_MAX_AGE_SECONDS,
                "account_linkage_strength": "contextual_non_cryptographic",
                "ui_api_account_equality_state": "unknown",
                "exact_ui_api_account_equality_verified": False,
            },
            "configuration_intent": {
                "chosen_enable_logging": True,
                "cross_provider_upload_owner_permission_observed": True,
                "zero_retention_mode_claimed": False,
                "descriptive_only_not_execution_authority": True,
            },
            "runtime_baseline": vt._recovery_transfer_runtime_baseline(runtime_bindings),
            "authority": copy.deepcopy(authority),
        }
        data_path = fixture / vt.RECOVERY_TRANSFER_DATA_USE_ASSURANCE_PATH
        data_sha = self._write_private_json(data_path, data_document)

        authorization = {
            "schema_version": vt.RECOVERY_TRANSFER_AUTH_SCHEMA,
            "authorization_id": vt.RECOVERY_TRANSFER_DRAFT_ID,
            "status": "draft",
            "provider_action_authorized": False,
            "scope": vt.RECOVERY_TRANSFER_SCOPE,
            "target": {"kind": "fixture", "id": vt.FIXTURE_ID},
            "transaction_basis_id": vt.RECOVERY_TRANSFER_TRANSACTION_BASIS_ID,
            "evidence_owner": vt.RECOVERY_TRANSFER_OWNER,
            "v1_lineage": {
                "path": vt.V1_LINEAGE_PATH,
                "sha256": vt.V1_LINEAGE_SHA256,
                "authorization_id": vt.V1_LINEAGE_ID,
                "status": "draft",
                "approved": False,
                "max_calls": 0,
                "max_spend_usd": 0,
            },
            "bindings": vt._recovery_transfer_bindings(plan_dry),
            "prerequisites": {
                "selected_guide": {
                    "state": "verified",
                    "path": vt.SELECTED_GUIDE_PATH,
                    "sha256": vt.SELECTED_GUIDE_SHA256,
                    "byte_count": vt.SELECTED_GUIDE_BYTES,
                    "duration_seconds": vt.SELECTED_GUIDE_DURATION_SECONDS,
                    "container": "wav",
                    "codec": "pcm_s16le",
                    "sample_rate_hz": 24000,
                    "channels": 1,
                    "guide_request_id": vt.SELECTED_GUIDE_REQUEST_ID,
                    "guide_run_receipt_path": vt.SELECTED_GUIDE_RUN_PATH,
                    "guide_run_receipt_sha256": vt.SELECTED_GUIDE_RUN_SHA256,
                },
                "guide_qa": {
                    "state": "verified",
                    "path": vt.RECOVERY_TRANSFER_GUIDE_QA_PATH,
                    "sha256": vt.RECOVERY_TRANSFER_GUIDE_QA_SHA256,
                },
                "owner_selection": {
                    "state": "verified",
                    "path": vt.RECOVERY_TRANSFER_GUIDE_SELECTION_PATH,
                    "sha256": vt.RECOVERY_TRANSFER_GUIDE_SELECTION_SHA256,
                },
                "owner_audition_confirmation": {
                    "state": "verified",
                    "path": vt.RECOVERY_TRANSFER_OWNER_APPROVAL_PATH,
                    "sha256": vt.RECOVERY_TRANSFER_OWNER_APPROVAL_SHA256,
                },
                "elevenlabs_data_use": {
                    "state": "verified",
                    "path": vt.RECOVERY_TRANSFER_DATA_USE_ASSURANCE_PATH,
                    "sha256": data_sha,
                },
                "target_voice_rights": {
                    "state": "verified",
                    "path": vt.RECOVERY_TRANSFER_TARGET_RIGHTS_PATH,
                    "sha256": rights_sha,
                },
                "prior_zero_provider_transfer_disposition": {
                    "state": "verified",
                    "path": vt.RECOVERY_TRANSFER_PRIOR_DISPOSITION_PATH,
                    "sha256": vt.RECOVERY_TRANSFER_PRIOR_DISPOSITION_SHA256,
                },
                "official_media_contract": {
                    "state": "verified",
                    "path": vt.MEDIA_CONTRACT_BASIS_PATH,
                    "sha256": vt.MEDIA_CONTRACT_BASIS_SHA256,
                },
            },
            "action": vt._action_transfer(True),
            "account_authentication_evidence": vt._recovery_transfer_account_evidence(
                True,
                assurance_sha256=account_sha,
            ),
            "credential_delivery": vt._recovery_transfer_credential_delivery(False),
            "runtime_bindings": runtime_bindings,
            "evidence_baseline": {"state": "pending"},
            "authorized_limits": vt._transfer_limits(False),
            "artifacts": vt._recovery_transfer_artifacts(False),
            "consumption": vt._recovery_transfer_consumption(False),
            "scope_approval": copy.deepcopy(scope_approval),
            "materialized_by": "Codex",
            "materialized_at": materialized_at,
            "expires_at": "",
            "execution_ready": False,
            "blockers": list(vt.RECOVERY_TRANSFER_DRAFT_BLOCKERS),
        }
        authorization_path = fixture / vt.RECOVERY_TRANSFER_DRAFT_PATH
        self._write_private_json(authorization_path, authorization)
        schema_path = self.root / "schemas/elevenlabs-recovery-evidence-voice-transfer-authorization.schema.json"
        schema = pt._strict_json_bytes(schema_path.read_bytes(), "recovery transfer schema")
        return SimpleNamespace(
            temporary=temporary,
            blueprint=blueprint,
            fixture=fixture.resolve(strict=True),
            plan=plan.resolve(strict=True),
            canonical=canonical.resolve(strict=True),
            authorization=authorization,
            authorization_path=authorization_path.resolve(strict=True),
            schema=schema,
            runtime_bindings=runtime_bindings,
            account_document=account_document,
            account_path=account_path,
            rights_document=rights_document,
            rights_path=rights_path,
            data_document=data_document,
            data_path=data_path,
            browser_document=browser_document,
            browser_path=browser_path,
            png_path=png_path,
        )

    def test_recovery_evidence_draft_is_schema_valid_and_zero_authority(self) -> None:
        bundle = self._recovery_transfer_draft_bundle()
        self.assertEqual(_local_schema_errors(bundle.authorization, bundle.schema), [])
        capture_relative, capture_path = vt._recovery_transfer_runtime_files()[
            "capture_audio_tests"
        ]
        self.assertEqual(
            capture_relative,
            "operator-blueprint-v2/02-narration-production/runtime/tests/test_capture_audio.py",
        )
        self.assertEqual(
            bundle.runtime_bindings["capture_audio_tests_sha256"],
            sha256_file(capture_path),
        )
        self.assertIn(
            "capture_audio_tests_sha256",
            bundle.schema["$defs"]["verifiedRuntime"]["required"],
        )
        dry = self._validate_recovery_transfer_bundle(bundle)
        self.assertTrue(dry["valid"])
        self.assertEqual(dry["authorization_status"], "draft")
        self.assertFalse(dry["provider_action_authorized"])
        self.assertEqual(dry["generation_post_calls_authorized"], 0)
        self.assertFalse(dry["credentials_accessed"])
        self.assertFalse(dry["network_called"])
        self.assertEqual(bundle.authorization["authorized_limits"], vt._transfer_limits(False))
        self.assertTrue(all(value is False for value in vt._recovery_transfer_zero_authority().values()))

    def test_recovery_evidence_schema_rejects_authority_and_scope_mutations(self) -> None:
        bundle = self._recovery_transfer_draft_bundle()
        mutations = (
            ("provider authority", ("provider_action_authorized",), True),
            ("post budget", ("authorized_limits", "max_generation_post_calls"), 1),
            ("credential state", ("credential_delivery", "state"), "verified"),
            ("owner review", ("scope_approval", "later_draft_and_active_bytes_owner_reviewed"), True),
            ("c907 runtime authority", ("scope_approval", "c907_alone_confers_runtime_execution_authority"), True),
            (
                "alternate c907 prerequisite",
                ("prerequisites", "owner_audition_confirmation", "sha256"),
                "0" * 64,
            ),
            (
                "alternate media prerequisite",
                ("prerequisites", "official_media_contract", "sha256"),
                "0" * 64,
            ),
            ("extra key", ("unexpected",), False),
        )
        for label, keys, value in mutations:
            with self.subTest(label=label):
                document = copy.deepcopy(bundle.authorization)
                target = document
                for key in keys[:-1]:
                    target = target[key]
                target[keys[-1]] = value
                self.assertTrue(_local_schema_errors(document, bundle.schema))

    def test_recovery_evidence_strict_json_rejects_duplicates_nonfinite_and_secret_values(self) -> None:
        corruptions = (
            (
                "duplicate",
                lambda raw: raw.replace(
                    b'"status": "draft",',
                    b'"status": "draft",\n  "status": "active",',
                    1,
                ),
            ),
            (
                "nonfinite",
                lambda raw: raw.replace(
                    b'"provider_action_authorized": false,',
                    b'"provider_action_authorized": false,\n  "numeric_probe": NaN,',
                    1,
                ),
            ),
            (
                "secret",
                lambda raw: raw.replace(
                    b'"provider_action_authorized": false,',
                    b'"provider_action_authorized": false,\n  "api_key": "unit-secret-sentinel",',
                    1,
                ),
            ),
        )
        for label, corrupt in corruptions:
            with self.subTest(label=label):
                bundle = self._recovery_transfer_draft_bundle()
                bundle.authorization_path.write_bytes(
                    corrupt(bundle.authorization_path.read_bytes())
                )
                bundle.authorization_path.chmod(0o600)
                with self.assertRaises(ValidationError) as captured:
                    self._validate_recovery_transfer_bundle(bundle)
                self.assertNotIn("unit-secret-sentinel", str(captured.exception))

    def test_recovery_evidence_record_results_are_canonical_three_tuples(self) -> None:
        bundle = self._recovery_transfer_draft_bundle()
        captured: dict[str, dict] = {}
        account_validator = vt._validate_recovery_transfer_account_evidence
        prerequisite_validator = vt._validate_recovery_transfer_prerequisites

        def capture_account(*args: object, **kwargs: object) -> dict:
            result = account_validator(*args, **kwargs)
            captured["account"] = copy.deepcopy(result)
            return result

        def capture_prerequisites(*args: object, **kwargs: object) -> dict:
            result = prerequisite_validator(*args, **kwargs)
            captured["prerequisites"] = copy.deepcopy(result)
            return result

        with (
            mock.patch.object(
                vt,
                "_validate_recovery_transfer_account_evidence",
                side_effect=capture_account,
            ),
            mock.patch.object(
                vt,
                "_validate_recovery_transfer_prerequisites",
                side_effect=capture_prerequisites,
            ),
        ):
            self._validate_recovery_transfer_bundle(bundle)
        for result in captured.values():
            for record in result["records"].values():
                self.assertIsInstance(record, tuple)
                self.assertEqual(len(record), 3)
                self.assertIsInstance(record[0], Path)
                self.assertIsInstance(record[1], bytes)
                self.assertRegex(record[2], r"^[0-9a-f]{64}$")

    def test_recovery_evidence_draft_rejects_historical_browser_as_fresh(self) -> None:
        bundle = self._recovery_transfer_draft_bundle()
        historical_path = bundle.fixture / vt.RECOVERY_TRANSFER_HISTORICAL_BROWSER_PATH
        historical = pt._strict_json_bytes(
            historical_path.read_bytes(),
            "historical recovery browser evidence",
        )
        bundle.data_document["evidence"]["fresh_browser_readiness"] = {
            "path": vt.RECOVERY_TRANSFER_HISTORICAL_BROWSER_PATH,
            "sha256": vt.RECOVERY_TRANSFER_HISTORICAL_BROWSER_SHA256,
        }
        bundle.data_document["evidence"]["fresh_browser_capture"] = {
            "path": historical["capture"]["path"],
            "sha256": historical["capture"]["sha256"],
        }
        bundle.data_document["fresh_observation"]["observed_at"] = historical[
            "observed_at"
        ]
        self._rewrite_recovery_transfer_data_and_authorization(bundle)
        with self.assertRaisesRegex(
            ValidationError,
            "historical|fresh browser|fresh data-use|record chronology",
        ):
            self._validate_recovery_transfer_bundle(bundle)

    def test_recovery_evidence_draft_rejects_data_recorded_after_freshness_window(self) -> None:
        bundle = self._recovery_transfer_draft_bundle()
        bundle.data_document["recorded_at"] = "2026-08-26T15:20:01Z"
        bundle.authorization["materialized_at"] = "2026-08-26T15:21:00Z"
        self._rewrite_recovery_transfer_data_and_authorization(bundle)
        with self.assertRaisesRegex(ValidationError, "fresh|window|stale"):
            self._validate_recovery_transfer_bundle(bundle)

    def test_recovery_evidence_draft_rejects_rights_before_c907_finalization(self) -> None:
        bundle = self._recovery_transfer_draft_bundle()
        bundle.rights_document["recorded_at"] = "2026-08-26T06:20:52Z"
        self._rewrite_recovery_transfer_rights_chain(bundle)
        with self.assertRaisesRegex(ValidationError, "rights|c907|chronology"):
            self._validate_recovery_transfer_bundle(bundle)

    def test_recovery_evidence_draft_rejects_future_materialization(self) -> None:
        bundle = self._recovery_transfer_draft_bundle()
        bundle.authorization["materialized_at"] = "2099-01-01T00:00:00Z"
        self._write_private_json(bundle.authorization_path, bundle.authorization)
        with self.assertRaisesRegex(ValidationError, "materialized|future|current"):
            self._validate_recovery_transfer_bundle(bundle)

    def test_recovery_evidence_authorization_times_require_exact_utc_rfc3339(self) -> None:
        malformed_draft_times = (
            "2026-08-26 14:22:00+00:00",
            "2026-08-26T10:22:00-04:00",
            "2026-08-26T14:22:00.1234567Z",
        )
        for value in malformed_draft_times:
            with self.subTest(status="draft", value=value):
                bundle = self._recovery_transfer_draft_bundle()
                bundle.authorization["materialized_at"] = value
                self.assertTrue(_local_schema_errors(bundle.authorization, bundle.schema))
                self._write_private_json(bundle.authorization_path, bundle.authorization)
                with self.assertRaisesRegex(ValidationError, "exact UTC RFC3339"):
                    self._validate_recovery_transfer_bundle(bundle)

        def validate_active(bundle: SimpleNamespace) -> None:
            source_patches = self._recovery_transfer_source_proof(bundle)
            with (
                source_patches[0],
                source_patches[1],
                source_patches[2],
                mock.patch.object(
                    vt,
                    "_target",
                    return_value=bundle.authorization["target"],
                ),
                mock.patch.object(
                    vt,
                    "_validate_recovery_transfer_evidence_baseline",
                    return_value=bundle.authorization["evidence_baseline"],
                ),
                mock.patch.object(
                    vt,
                    "_execution_now",
                    return_value=datetime(2026, 8, 26, 14, 30, tzinfo=timezone.utc),
                ),
                mock.patch.object(
                    vt,
                    "_read_recovery_dotenv_key",
                    side_effect=AssertionError("ACTIVE validation read a credential"),
                ),
                mock.patch.object(
                    urllib.request,
                    "build_opener",
                    side_effect=AssertionError("ACTIVE validation attempted network"),
                ),
            ):
                vt.validate_recovery_evidence_voice_transfer_authorization(
                    bundle.authorization_path,
                    bundle.plan,
                    bundle.canonical,
                )

        malformed_active_times = (
            "2026-08-26 14:50:00+00:00",
            "2026-08-26T10:50:00-04:00",
            "2026-08-26T14:50:00.1234567Z",
        )
        for value in malformed_active_times:
            with self.subTest(status="active", value=value):
                bundle = self._activate_recovery_transfer_bundle(
                    self._recovery_transfer_draft_bundle()
                )
                bundle.authorization["expires_at"] = value
                self.assertTrue(_local_schema_errors(bundle.authorization, bundle.schema))
                self._write_private_json(bundle.authorization_path, bundle.authorization)
                with self.assertRaisesRegex(ValidationError, "exact UTC RFC3339"):
                    validate_active(bundle)

    def test_recovery_evidence_record_times_require_exact_utc_rfc3339(self) -> None:
        cases = (
            (
                "account assurance",
                "2026-08-26 14:10:00+00:00",
                lambda bundle, value: bundle.account_document.__setitem__(
                    "recorded_at", value
                ),
                self._rewrite_recovery_transfer_account_chain,
            ),
            (
                "data-use assurance",
                "2026-08-26T10:21:00-04:00",
                lambda bundle, value: bundle.data_document.__setitem__(
                    "recorded_at", value
                ),
                self._rewrite_recovery_transfer_data_and_authorization,
            ),
            (
                "target rights",
                "2026-08-26T14:10:00.0000000Z",
                lambda bundle, value: bundle.rights_document.__setitem__(
                    "recorded_at", value
                ),
                self._rewrite_recovery_transfer_rights_chain,
            ),
        )
        for label, value, mutate, rewrite in cases:
            with self.subTest(label=label, value=value):
                bundle = self._recovery_transfer_draft_bundle()
                mutate(bundle, value)
                rewrite(bundle)
                with self.assertRaisesRegex(ValidationError, "exact UTC RFC3339"):
                    self._validate_recovery_transfer_bundle(bundle)

        bundle = self._recovery_transfer_draft_bundle()
        noncanonical_browser_time = "2026-08-26T10:20:00-04:00"
        bundle.browser_document["observed_at"] = noncanonical_browser_time
        browser_sha = self._write_private_json(
            bundle.browser_path,
            bundle.browser_document,
        )
        bundle.data_document["evidence"]["fresh_browser_readiness"][
            "sha256"
        ] = browser_sha
        bundle.data_document["fresh_observation"][
            "observed_at"
        ] = noncanonical_browser_time
        self._rewrite_recovery_transfer_data_and_authorization(bundle)
        with self.assertRaisesRegex(ValidationError, "exact UTC RFC3339"):
            self._validate_recovery_transfer_bundle(bundle)

    def test_recovery_evidence_fresh_browser_paths_require_exact_same_stem(self) -> None:
        def rewrite_paths(
            bundle: SimpleNamespace,
            *,
            json_name: str,
            png_name: str,
        ) -> None:
            old_browser = bundle.browser_path
            old_png = bundle.png_path
            new_browser = old_browser.with_name(json_name)
            new_png = old_png.with_name(png_name)
            png_bytes = old_png.read_bytes()
            new_png.write_bytes(png_bytes)
            new_png.chmod(0o600)
            bundle.browser_document["capture"] = {
                "path": new_png.relative_to(bundle.fixture).as_posix(),
                "sha256": sha256_bytes(png_bytes),
            }
            browser_sha = self._write_private_json(
                new_browser,
                bundle.browser_document,
            )
            if new_browser != old_browser:
                old_browser.unlink()
            if new_png != old_png:
                old_png.unlink()
            bundle.browser_path = new_browser.resolve(strict=True)
            bundle.png_path = new_png.resolve(strict=True)
            bundle.data_document["evidence"]["fresh_browser_readiness"] = {
                "path": new_browser.relative_to(bundle.fixture).as_posix(),
                "sha256": browser_sha,
            }
            bundle.data_document["evidence"]["fresh_browser_capture"] = {
                "path": new_png.relative_to(bundle.fixture).as_posix(),
                "sha256": sha256_bytes(png_bytes),
            }
            self._rewrite_recovery_transfer_data_and_authorization(bundle)

        def validate_active(bundle: SimpleNamespace) -> None:
            source_patches = self._recovery_transfer_source_proof(bundle)
            with (
                source_patches[0],
                source_patches[1],
                source_patches[2],
                mock.patch.object(
                    vt,
                    "_target",
                    return_value=bundle.authorization["target"],
                ),
                mock.patch.object(
                    vt,
                    "_validate_recovery_transfer_evidence_baseline",
                    return_value=bundle.authorization["evidence_baseline"],
                ),
                mock.patch.object(
                    vt,
                    "_execution_now",
                    return_value=datetime(2026, 8, 26, 14, 30, tzinfo=timezone.utc),
                ),
            ):
                vt.validate_recovery_evidence_voice_transfer_authorization(
                    bundle.authorization_path,
                    bundle.plan,
                    bundle.canonical,
                )

        alias_bundle = self._recovery_transfer_draft_bundle()
        rewrite_paths(
            alias_bundle,
            json_name="fresh-browser-alias.json",
            png_name="fresh-browser-alias.png",
        )
        with self.assertRaisesRegex(ValidationError, "same-stem pair"):
            self._validate_recovery_transfer_bundle(alias_bundle)
        alias_active = self._activate_recovery_transfer_bundle(alias_bundle)
        self.assertTrue(
            _local_schema_errors(alias_active.authorization, alias_active.schema)
        )
        with self.assertRaisesRegex(ValidationError, "same-stem pair"):
            validate_active(alias_active)

        mismatch_bundle = self._recovery_transfer_draft_bundle()
        rewrite_paths(
            mismatch_bundle,
            json_name=mismatch_bundle.browser_path.name,
            png_name="V1-ELEVENLABS-RECOVERY-TRANSFER-BROWSER-READINESS.20260826T142001Z.png",
        )
        with self.assertRaisesRegex(ValidationError, "same-stem pair"):
            self._validate_recovery_transfer_bundle(mismatch_bundle)
        mismatch_active = self._activate_recovery_transfer_bundle(mismatch_bundle)
        self.assertEqual(
            _local_schema_errors(mismatch_active.authorization, mismatch_active.schema),
            [],
        )
        with self.assertRaisesRegex(ValidationError, "same-stem pair"):
            validate_active(mismatch_active)

    def test_recovery_evidence_validator_rejects_account_overclaims(self) -> None:
        mutations = (
            (
                "body bytes read",
                lambda document: document["observed_outcome"].__setitem__(
                    "response_body_bytes_read", 1
                ),
            ),
            (
                "account equality verified",
                lambda document: document["calibrated_interpretation"].__setitem__(
                    "exact_ui_api_account_equality_verified", True
                ),
            ),
            (
                "identity observed",
                lambda document: document["calibrated_interpretation"].__setitem__(
                    "identity_observed", True
                ),
            ),
            (
                "retry allowed",
                lambda document: document["terminality"].__setitem__(
                    "automatic_retry_permitted", True
                ),
            ),
            (
                "record grants transfer authority",
                lambda document: document["authority"].__setitem__(
                    "voice_transfer_authorized", True
                ),
            ),
        )
        for label, mutate in mutations:
            with self.subTest(label=label):
                bundle = self._recovery_transfer_draft_bundle()
                mutate(bundle.account_document)
                self._rewrite_recovery_transfer_account_chain(bundle)
                with self.assertRaises(ValidationError):
                    self._validate_recovery_transfer_bundle(bundle)

    def test_recovery_evidence_validator_rejects_rights_authority_drift(self) -> None:
        mutations = (
            (
                "alternate c907 hash",
                lambda document: document["owner_authority_calibration"][
                    "sole_exact_provider_action_authority"
                ].__setitem__("sha256", "0" * 64),
            ),
            (
                "unseen bytes called reviewed",
                lambda document: document["owner_authority_calibration"].__setitem__(
                    "later_draft_and_active_bytes_owner_reviewed", True
                ),
            ),
            (
                "c907 called runtime authority",
                lambda document: document["owner_authority_calibration"].__setitem__(
                    "c907_alone_confers_runtime_execution_authority", True
                ),
            ),
            (
                "recovery-only 549 context reused",
                lambda document: document["owner_authority_calibration"].__setitem__(
                    "recovery_only_context_evidence",
                    {
                        "path": vt.RECOVERY_OWNER_APPROVAL_PATH,
                        "sha256": vt.RECOVERY_OWNER_APPROVAL_SHA256,
                    },
                ),
            ),
            (
                "rights record grants provider action",
                lambda document: document["authority"].__setitem__(
                    "this_record_authorizes_provider_action", True
                ),
            ),
        )
        for label, mutate in mutations:
            with self.subTest(label=label):
                bundle = self._recovery_transfer_draft_bundle()
                mutate(bundle.rights_document)
                self._rewrite_recovery_transfer_rights_chain(bundle)
                with self.assertRaises(ValidationError):
                    self._validate_recovery_transfer_bundle(bundle)

    def test_recovery_evidence_validator_rejects_data_use_and_chronology_drift(self) -> None:
        cases = (
            (
                "data record grants network",
                lambda bundle: bundle.data_document["authority"].__setitem__(
                    "network_authorized", True
                ),
                "data",
            ),
            (
                "UI API equality upgraded",
                lambda bundle: bundle.data_document["fresh_observation"].__setitem__(
                    "ui_api_account_equality_state", "verified"
                ),
                "data",
            ),
            (
                "data predates browser",
                lambda bundle: bundle.data_document.__setitem__(
                    "recorded_at", "2026-08-26T14:19:59Z"
                ),
                "data",
            ),
            (
                "rights follows browser",
                lambda bundle: bundle.rights_document.__setitem__(
                    "recorded_at", "2026-08-26T14:20:01Z"
                ),
                "rights",
            ),
            (
                "account follows browser",
                lambda bundle: bundle.account_document.__setitem__(
                    "recorded_at", "2026-08-26T14:20:01Z"
                ),
                "account",
            ),
        )
        for label, mutate, chain in cases:
            with self.subTest(label=label):
                bundle = self._recovery_transfer_draft_bundle()
                mutate(bundle)
                if chain == "account":
                    self._rewrite_recovery_transfer_account_chain(bundle)
                elif chain == "rights":
                    self._rewrite_recovery_transfer_rights_chain(bundle)
                else:
                    self._rewrite_recovery_transfer_data_and_authorization(bundle)
                with self.assertRaises(ValidationError):
                    self._validate_recovery_transfer_bundle(bundle)

    def test_recovery_evidence_private_records_reject_mode_and_hardlinks(self) -> None:
        bundle = self._recovery_transfer_draft_bundle()
        private_paths = (
            bundle.fixture / vt.SELECTED_GUIDE_PATH,
            bundle.fixture / vt.SELECTED_GUIDE_RUN_PATH,
            bundle.fixture / vt.RECOVERY_TRANSFER_GUIDE_QA_PATH,
            bundle.fixture / vt.RECOVERY_TRANSFER_GUIDE_SELECTION_PATH,
            bundle.fixture / vt.RECOVERY_TRANSFER_OWNER_APPROVAL_PATH,
            bundle.account_path,
            bundle.rights_path,
            bundle.data_path,
            bundle.browser_path,
            bundle.png_path,
            bundle.blueprint / vt.RECOVERY_TRANSFER_ORIGINAL_C_SELECTION_PATH,
            bundle.blueprint / vt.RECOVERY_TRANSFER_ORIGINAL_C_SAVE_PATH,
        )
        for path in private_paths:
            root = pt._document_root(path.resolve(strict=True))
            relative = path.resolve(strict=True).relative_to(root).as_posix()
            with self.subTest(path=relative, attack="mode"):
                path.chmod(0o644)
                with self.assertRaises(ValidationError):
                    vt._read_recovery_private_bytes(
                        root,
                        path.resolve(strict=True),
                        "unit private record",
                        max_bytes=50_000_000,
                    )
                path.chmod(0o600)
            with self.subTest(path=relative, attack="hardlink"):
                link = path.with_name(path.name + ".unit-hardlink")
                os.link(path, link)
                try:
                    with self.assertRaises(ValidationError):
                        vt._read_recovery_private_bytes(
                            root,
                            path.resolve(strict=True),
                            "unit private record",
                            max_bytes=50_000_000,
                        )
                finally:
                    link.unlink()

    def test_recovery_evidence_selected_guide_rejects_symlink_and_identity_swap(self) -> None:
        bundle = self._recovery_transfer_draft_bundle()
        selected = bundle.fixture / vt.SELECTED_GUIDE_PATH
        backup = selected.with_name("candidate-B.unit-backup.wav")
        selected.rename(backup)
        selected.symlink_to(backup.name)
        try:
            with self.assertRaises(ValidationError):
                vt._read_recovery_private_bytes(
                    bundle.fixture,
                    selected,
                    "unit selected guide",
                    max_bytes=50_000_000,
                )
        finally:
            selected.unlink()
            backup.rename(selected)

        original_fstat = os.fstat
        target_inode = selected.stat(follow_symlinks=False).st_ino
        target_calls = 0

        def changed_fstat(descriptor: int):
            nonlocal target_calls
            result = original_fstat(descriptor)
            if result.st_ino != target_inode:
                return result
            target_calls += 1
            if target_calls != 2:
                return result
            values = {
                name: getattr(result, name)
                for name in (
                    "st_dev", "st_ino", "st_size", "st_mtime_ns", "st_ctime_ns",
                    "st_mode", "st_uid", "st_gid", "st_nlink",
                )
            }
            values["st_ctime_ns"] += 1
            return SimpleNamespace(**values)

        with (
            mock.patch.object(os, "fstat", side_effect=changed_fstat),
            self.assertRaisesRegex(ValidationError, "changed during descriptor read"),
        ):
            vt._read_recovery_private_bytes(
                bundle.fixture,
                selected,
                "unit selected guide",
                max_bytes=50_000_000,
            )

    def test_recovery_evidence_execution_destinations_are_absent_and_reject_symlinks(self) -> None:
        artifacts = vt._recovery_transfer_artifacts(True)
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            contract = SimpleNamespace(
                root=root,
                consumption_relative=vt.TRANSFER_SCOPE_LATCH_PATH,
                raw_relative=artifacts["raw_output_path"],
                working_relative=artifacts["working_output_path"],
                success_relative=artifacts["success_receipt_path"],
                failure_relative=artifacts["failure_receipt_path"],
                conversion_relative=artifacts["conversion_receipt_path"],
            )
            relatives = (
                contract.consumption_relative,
                contract.raw_relative,
                contract.working_relative,
                contract.success_relative,
                contract.failure_relative,
                contract.conversion_relative,
            )
            vt._preflight_transfer_paths(contract)
            for relative in relatives:
                destination = root / relative
                self.assertFalse(destination.exists())
                self.assertFalse(destination.is_symlink())

            target = root / "unit-existing-destination"
            target.write_bytes(b"unit")
            for relative in relatives:
                destination = root / relative
                destination.symlink_to(target)
                try:
                    with self.subTest(relative=relative), self.assertRaisesRegex(
                        ValidationError,
                        "must not already exist|may not traverse a symlink",
                    ):
                        vt._preflight_transfer_paths(contract)
                finally:
                    destination.unlink()

    def test_recovery_evidence_selected_guide_git_privacy_attacks_fail(self) -> None:
        bundle = self._recovery_transfer_draft_bundle()
        repository = pt._guide_repository_root()
        selected = bundle.fixture / vt.SELECTED_GUIDE_PATH
        relative = selected.relative_to(repository).as_posix()
        ignore = bundle.fixture / ".gitignore"
        ignore_relative = ignore.relative_to(repository).as_posix()
        exact_ignore = f"{ignore_relative}:1:outputs/raw/\t{relative}\n".encode()

        def check(attack: str, arguments: list[str]) -> bytes:
            if arguments[:2] == ["ls-files", "--stage"]:
                return b"100600 tracked\n" if attack == "tracked" else b""
            if arguments[:3] == ["check-ignore", "--no-index", "-v"]:
                if attack == "global-ignore":
                    return f"/Users/unit/.config/git/ignore:1:outputs/raw/\t{relative}\n".encode()
                if attack == "info-exclude":
                    return f"/unit/.git/info/exclude:1:{relative}\t{relative}\n".encode()
                if attack == "unrelated-rule":
                    return f"{ignore_relative}:2:*.wav\t{relative}\n".encode()
                return exact_ignore
            if arguments and arguments[0] == "ls-tree":
                return relative.encode() if attack == "historically-tracked" else b""
            if arguments and arguments[0] == "show":
                return ignore.read_bytes()
            raise AssertionError(arguments)

        for attack in (
            "tracked",
            "global-ignore",
            "info-exclude",
            "unrelated-rule",
            "historically-tracked",
        ):
            with self.subTest(attack=attack), mock.patch.object(
                vt,
                "_bound_git",
                side_effect=lambda bindings, arguments, **kwargs: check(attack, arguments),
            ), self.assertRaises(ValidationError):
                vt._verify_recovery_transfer_selected_guide_git_state(
                    bundle.runtime_bindings,
                    repository,
                    bundle.fixture,
                    selected,
                )

    def test_recovery_evidence_r0_requires_direct_parent_exact_delta_and_bytes(self) -> None:
        bundle = self._recovery_transfer_draft_bundle()
        runtime_commit = bundle.runtime_bindings["git_commit"]
        voice_relative = vt._recovery_transfer_runtime_files()[
            "voice_transfer_runtime"
        ][0]

        def wrong_parent(arguments: list[str]) -> bytes | None:
            if arguments[:3] == ["rev-list", "--parents", "-n"]:
                return f"{runtime_commit} {'c' * 40}\n".encode()
            return None

        def deleted_delta(arguments: list[str]) -> bytes | None:
            if arguments and arguments[0] == "diff":
                return b"D\x00" + voice_relative.encode() + b"\x00"
            return None

        def tampered_blob(arguments: list[str]) -> bytes | None:
            if arguments == ["show", f"{runtime_commit}:{voice_relative}"]:
                return b"tampered runtime bytes"
            return None

        for label, override in (
            ("non-direct parent", wrong_parent),
            ("deletion in delta", deleted_delta),
            ("committed blob drift", tampered_blob),
        ):
            with self.subTest(label=label):
                errors: list[str] = []
                patches = self._recovery_transfer_source_proof(
                    bundle,
                    override=override,
                )
                with patches[0], patches[1]:
                    vt._validate_recovery_transfer_runtime_bindings(
                        bundle.runtime_bindings,
                        active=True,
                        errors=errors,
                    )
                self.assertIn(
                    "recovery-evidence transfer R0 Git source proof is invalid",
                    errors,
                )

    def test_recovery_evidence_r1_and_active_commit_boundaries_fail_closed(self) -> None:
        bundle = self._recovery_transfer_draft_bundle()
        repository = pt._guide_repository_root()
        runtime_commit = bundle.runtime_bindings["git_commit"]
        evidence_commit = "c" * 40
        active_commit = "d" * 40
        active_path = bundle.fixture / vt.RECOVERY_TRANSFER_ACTIVE_PATH
        active_raw = b"{}\n"
        active_path.write_bytes(active_raw)
        active_path.chmod(0o600)

        def record(path: Path) -> tuple[Path, bytes, str]:
            resolved = path.resolve(strict=True)
            raw = resolved.read_bytes()
            return resolved, raw, sha256_bytes(raw)

        account_records = {
            "calibrated_account_assurance": record(bundle.account_path),
            "recovery_authorization": record(
                bundle.fixture / vt.RECOVERY_TRANSFER_ACCOUNT_AUTH_PATH
            ),
            "credential_read_latch": record(
                bundle.fixture / vt.RECOVERY_TRANSFER_CREDENTIAL_LATCH_PATH
            ),
            "provider_call_latch": record(
                bundle.fixture / vt.RECOVERY_TRANSFER_PROVIDER_LATCH_PATH
            ),
            "http_200_failure_receipt": record(
                bundle.fixture / vt.RECOVERY_TRANSFER_FAILURE_PATH
            ),
            "terminal_disposition": record(
                bundle.fixture / vt.RECOVERY_TRANSFER_DISPOSITION_PATH
            ),
        }
        prerequisite_records = {
            "elevenlabs_data_use": record(bundle.data_path),
            "target_voice_rights": record(bundle.rights_path),
            "fresh_browser_readiness": record(bundle.browser_path),
            "fresh_browser_capture": record(bundle.png_path),
        }
        draft = record(bundle.authorization_path)
        baseline = {
            "state": "verified",
            "evidence_commit": evidence_commit,
            "draft_authorization": {
                "path": vt.RECOVERY_TRANSFER_DRAFT_PATH,
                "sha256": draft[2],
            },
            "calibrated_account_assurance": {
                "path": vt.RECOVERY_TRANSFER_ACCOUNT_ASSURANCE_PATH,
                "sha256": account_records["calibrated_account_assurance"][2],
            },
            "data_use_assurance": {
                "path": vt.RECOVERY_TRANSFER_DATA_USE_ASSURANCE_PATH,
                "sha256": prerequisite_records["elevenlabs_data_use"][2],
            },
            "target_rights": {
                "path": vt.RECOVERY_TRANSFER_TARGET_RIGHTS_PATH,
                "sha256": prerequisite_records["target_voice_rights"][2],
            },
            "fresh_browser_readiness": {
                "path": bundle.browser_path.relative_to(bundle.fixture).as_posix(),
                "sha256": prerequisite_records["fresh_browser_readiness"][2],
            },
        }
        r1_records = {
            bundle.authorization_path.resolve(strict=True),
            bundle.data_path.resolve(strict=True),
            bundle.browser_path.resolve(strict=True),
        }
        r1_delta = b"".join(
            b"A\x00"
            + path.relative_to(repository).as_posix().encode("utf-8")
            + b"\x00"
            for path in sorted(r1_records)
        )
        active_relative = active_path.relative_to(repository).as_posix()
        png_relative = bundle.png_path.relative_to(repository).as_posix()

        def bound_git(arguments: list[str], attack: str | None) -> bytes:
            if arguments[:2] == ["cat-file", "-e"]:
                return b""
            if arguments[:2] == ["merge-base", "--is-ancestor"]:
                return b""
            if arguments[:3] == ["rev-list", "--parents", "-n"]:
                commit = arguments[-1]
                if commit == evidence_commit:
                    parents = (
                        f"{evidence_commit} {runtime_commit} {'e' * 40}\n"
                        if attack == "R1 merge"
                        else f"{evidence_commit} {runtime_commit}\n"
                    )
                    return parents.encode()
                if commit == active_commit:
                    parents = (
                        f"{active_commit} {runtime_commit}\n"
                        if attack == "A parent"
                        else f"{active_commit} {evidence_commit}\n"
                    )
                    return parents.encode()
                raise AssertionError(arguments)
            if arguments == ["rev-parse", "HEAD"]:
                value = evidence_commit if attack == "uncommitted ACTIVE" else active_commit
                return (value + "\n").encode()
            if arguments and arguments[0] == "diff":
                revision = arguments[-1]
                if revision == f"{runtime_commit}..{evidence_commit}":
                    if attack == "R1 modified path":
                        first = next(iter(sorted(r1_records)))
                        return (
                            b"M\x00"
                            + first.relative_to(repository).as_posix().encode()
                            + b"\x00"
                            + b"".join(
                                b"A\x00"
                                + path.relative_to(repository).as_posix().encode()
                                + b"\x00"
                                for path in sorted(r1_records - {first})
                            )
                        )
                    if attack == "R1 extra path":
                        return r1_delta + b"A\x00unexpected.json\x00"
                    return r1_delta
                if revision == f"{evidence_commit}..{active_commit}":
                    status = b"M" if attack == "A modified path" else b"A"
                    return status + b"\x00" + active_relative.encode() + b"\x00"
                raise AssertionError(arguments)
            if arguments and arguments[0] == "ls-tree":
                return png_relative.encode() if attack == "PNG tracked" else b""
            if arguments and arguments[0] == "status":
                return b" M unrelated\x00" if attack == "dirty A" else b""
            if arguments and arguments[0] == "show":
                _commit, separator, relative = arguments[-1].partition(":")
                if not separator:
                    raise AssertionError(arguments)
                return (repository / relative).read_bytes()
            raise AssertionError(arguments)

        def validate(
            attack: str | None,
            *,
            active_materialized_at: datetime = datetime(
                2026, 8, 26, 14, 23, tzinfo=timezone.utc
            ),
        ) -> list[str]:
            errors: list[str] = []
            def override(arguments: list[str]) -> bytes | None:
                try:
                    return bound_git(arguments, attack)
                except AssertionError:
                    return None

            source_patches = self._recovery_transfer_source_proof(
                bundle,
                override=override,
            )
            with (
                source_patches[0],
                source_patches[1],
                source_patches[2],
                mock.patch.object(
                    vt,
                    "_target",
                    return_value=bundle.authorization["target"],
                ),
            ):
                vt._validate_recovery_transfer_evidence_baseline(
                    baseline,
                    active=True,
                    authorization_path=active_path,
                    authorization_raw=active_raw,
                    root=bundle.fixture,
                    plan_path=bundle.plan,
                    canonical_w_path=bundle.canonical,
                    active_materialized_at=active_materialized_at,
                    runtime_bindings=bundle.runtime_bindings,
                    account_evidence={"records": account_records},
                    prerequisite_result={"records": prerequisite_records},
                    errors=errors,
                )
            return errors

        self.assertEqual(validate(None), [])
        for attack in (
            "R1 merge",
            "R1 modified path",
            "R1 extra path",
            "PNG tracked",
            "uncommitted ACTIVE",
            "A parent",
            "A modified path",
            "dirty A",
        ):
            with self.subTest(attack=attack):
                self.assertIn(
                    "active recovery-evidence transfer R1 Git source proof is invalid",
                    validate(attack),
                )
        invalid_draft = {
            "status": "active",
            "provider_action_authorized": True,
            "execution_ready": True,
        }
        invalid_draft_sha = self._write_private_json(
            bundle.authorization_path,
            invalid_draft,
        )
        baseline["draft_authorization"]["sha256"] = invalid_draft_sha
        with self.subTest(attack="schema-invalid committed DRAFT bytes"):
            self.assertIn(
                "active recovery-evidence transfer R1 Git source proof is invalid",
                validate(None),
            )

        chronological_bundle = self._recovery_transfer_draft_bundle()
        chronological_draft = record(chronological_bundle.authorization_path)
        bundle.authorization_path.write_bytes(chronological_draft[1])
        bundle.authorization_path.chmod(0o600)
        baseline["draft_authorization"]["sha256"] = chronological_draft[2]
        with self.subTest(attack="DRAFT materialized after ACTIVE"):
            self.assertIn(
                "active recovery-evidence transfer R1 Git source proof is invalid",
                validate(
                    None,
                    active_materialized_at=datetime(
                        2026, 8, 26, 14, 21, 59, tzinfo=timezone.utc
                    ),
                ),
            )

    def test_recovery_evidence_active_rejects_future_materialization_and_expiry(self) -> None:
        baseline_now = datetime(2026, 8, 26, 14, 30, tzinfo=timezone.utc)

        def active_bundle() -> SimpleNamespace:
            bundle = self._recovery_transfer_draft_bundle()
            draft_raw = bundle.authorization_path.read_bytes()
            draft_sha = sha256_bytes(draft_raw)
            provider_latch = pt._strict_json_bytes(
                (
                    bundle.fixture / vt.RECOVERY_TRANSFER_PROVIDER_LATCH_PATH
                ).read_bytes(),
                "unit provider latch",
            )
            bundle.authorization.update(
                {
                    "authorization_id": vt.RECOVERY_TRANSFER_ACTIVE_ID,
                    "status": "active",
                    "provider_action_authorized": True,
                    "credential_delivery": vt._recovery_transfer_credential_delivery(
                        True,
                        fingerprint=provider_latch["credential_fingerprint_sha256"],
                        suffix_sha256=provider_latch["browser_suffix_sha256"],
                    ),
                    "evidence_baseline": {
                        "state": "verified",
                        "evidence_commit": "c" * 40,
                        "draft_authorization": {
                            "path": vt.RECOVERY_TRANSFER_DRAFT_PATH,
                            "sha256": draft_sha,
                        },
                        "calibrated_account_assurance": {
                            "path": vt.RECOVERY_TRANSFER_ACCOUNT_ASSURANCE_PATH,
                            "sha256": sha256_file(bundle.account_path),
                        },
                        "data_use_assurance": {
                            "path": vt.RECOVERY_TRANSFER_DATA_USE_ASSURANCE_PATH,
                            "sha256": sha256_file(bundle.data_path),
                        },
                        "target_rights": {
                            "path": vt.RECOVERY_TRANSFER_TARGET_RIGHTS_PATH,
                            "sha256": sha256_file(bundle.rights_path),
                        },
                        "fresh_browser_readiness": {
                            "path": bundle.browser_path.relative_to(bundle.fixture).as_posix(),
                            "sha256": sha256_file(bundle.browser_path),
                        },
                    },
                    "authorized_limits": vt._transfer_limits(True),
                    "artifacts": vt._recovery_transfer_artifacts(True),
                    "consumption": vt._recovery_transfer_consumption(True),
                    "materialized_at": "2026-08-26T14:22:00Z",
                    "expires_at": "2026-08-26T14:50:00Z",
                    "execution_ready": True,
                    "blockers": [],
                }
            )
            active_path = bundle.fixture / vt.RECOVERY_TRANSFER_ACTIVE_PATH
            self._write_private_json(active_path, bundle.authorization)
            bundle.authorization_path = active_path.resolve(strict=True)
            return bundle

        def validate(bundle: SimpleNamespace) -> dict:
            source_patches = self._recovery_transfer_source_proof(bundle)
            with (
                source_patches[0],
                source_patches[1],
                source_patches[2],
                mock.patch.object(
                    vt,
                    "_target",
                    return_value=bundle.authorization["target"],
                ),
                mock.patch.object(
                    vt,
                    "_validate_recovery_transfer_evidence_baseline",
                    return_value=bundle.authorization["evidence_baseline"],
                ),
                mock.patch.object(vt, "_execution_now", return_value=baseline_now),
                mock.patch.object(
                    vt,
                    "_read_recovery_dotenv_key",
                    side_effect=AssertionError("ACTIVE validation read a credential"),
                ),
                mock.patch.object(
                    urllib.request,
                    "build_opener",
                    side_effect=AssertionError("ACTIVE validation attempted network"),
                ),
            ):
                return vt.validate_recovery_evidence_voice_transfer_authorization(
                    bundle.authorization_path,
                    bundle.plan,
                    bundle.canonical,
                )

        valid = active_bundle()
        self.assertEqual(_local_schema_errors(valid.authorization, valid.schema), [])
        self.assertTrue(validate(valid)["provider_action_authorized"])

        future = active_bundle()
        future.authorization["materialized_at"] = "2026-08-26T14:31:00Z"
        self._write_private_json(future.authorization_path, future.authorization)
        with self.assertRaisesRegex(ValidationError, "current"):
            validate(future)

        expired = active_bundle()
        expired.authorization["expires_at"] = "2026-08-26T14:29:59Z"
        self._write_private_json(expired.authorization_path, expired.authorization)
        with self.assertRaisesRegex(ValidationError, "current"):
            validate(expired)

    def test_recovery_evidence_late_failures_scrub_private_traceback_locals(self) -> None:
        def assert_draft_failure(patcher: mock._patch) -> None:
            bundle = self._recovery_transfer_draft_bundle()
            with patcher:
                try:
                    self._validate_recovery_transfer_bundle(bundle)
                except Exception as error:
                    self._assert_recovery_transfer_traceback_scrubbed(error, bundle)
                else:
                    self.fail("injected late failure did not propagate")

        assert_draft_failure(
            mock.patch.object(
                pt,
                "_compile_multipart_bytes",
                side_effect=RuntimeError("unit late compile failure"),
            )
        )
        assert_draft_failure(
            mock.patch.object(
                vt,
                "_normalized_transfer_request",
                side_effect=RuntimeError("unit late normalization failure"),
            )
        )

        private_bundle = self._recovery_transfer_draft_bundle()
        private_reader = vt._read_recovery_private_bytes

        def fail_private_authorization(
            root: Path,
            path: Path,
            label: str,
            *,
            max_bytes: int,
        ) -> tuple[bytes, str]:
            if Path(path).resolve(strict=True) == private_bundle.authorization_path:
                raise RuntimeError("unit late private authorization reread failure")
            return private_reader(root, path, label, max_bytes=max_bytes)

        with mock.patch.object(
            vt,
            "_read_recovery_private_bytes",
            side_effect=fail_private_authorization,
        ):
            try:
                self._validate_recovery_transfer_bundle(private_bundle)
            except Exception as error:
                self._assert_recovery_transfer_traceback_scrubbed(error, private_bundle)
            else:
                self.fail("private authorization reread failure did not propagate")

        accumulated_bundle = self._recovery_transfer_draft_bundle()
        accumulated_bundle.account_document["observed_outcome"][
            "response_body_bytes_read"
        ] = 1
        self._rewrite_recovery_transfer_account_chain(accumulated_bundle)
        try:
            self._validate_recovery_transfer_bundle(accumulated_bundle)
        except ValidationError as error:
            self._assert_recovery_transfer_traceback_scrubbed(error, accumulated_bundle)
        else:
            self.fail("accumulated semantic failure did not propagate")

        active_bundle = self._activate_recovery_transfer_bundle(
            self._recovery_transfer_draft_bundle()
        )
        source_patches = self._recovery_transfer_source_proof(active_bundle)
        with (
            source_patches[0],
            source_patches[1],
            source_patches[2],
            mock.patch.object(
                vt,
                "_target",
                return_value=active_bundle.authorization["target"],
            ),
            mock.patch.object(
                vt,
                "_validate_recovery_transfer_evidence_baseline",
                return_value=active_bundle.authorization["evidence_baseline"],
            ),
            mock.patch.object(
                vt,
                "_execution_now",
                side_effect=RuntimeError("unit late clock failure"),
            ),
            mock.patch.object(
                vt,
                "_read_recovery_dotenv_key",
                side_effect=AssertionError("validation read a credential"),
            ),
            mock.patch.object(
                urllib.request,
                "build_opener",
                side_effect=AssertionError("validation attempted network"),
            ),
        ):
            try:
                vt.validate_recovery_evidence_voice_transfer_authorization(
                    active_bundle.authorization_path,
                    active_bundle.plan,
                    active_bundle.canonical,
                )
            except Exception as error:
                self._assert_recovery_transfer_traceback_scrubbed(error, active_bundle)
            else:
                self.fail("late clock failure did not propagate")

    def _recovery_executor_fixture(
        self,
        *,
        credential_binding: str = "valid",
    ) -> SimpleNamespace:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name).resolve()
        authorization_path = root / "authorizations" / "unit.ACTIVE.json"
        authorization_path.parent.mkdir(parents=True)
        authorization_path.write_text("{}\n", encoding="utf-8")
        authorization_path.chmod(0o600)
        plan_path = root / "performance-transfer-plan.json"
        canonical_path = root / "passages" / "P01-W0030-W0110.locked.txt"
        plan_path.write_text("{}\n", encoding="utf-8")
        canonical_path.parent.mkdir(parents=True)
        canonical_path.write_text("unit\n", encoding="utf-8")

        selected_audio = (self.fixture / vt.SELECTED_GUIDE_PATH).read_bytes()
        _manifest, body_bytes = pt._compile_multipart_bytes(
            selected_audio,
            vt.SELECTED_GUIDE_SHA256,
            pt.TRANSFER_PRIMARY_FORMAT,
            enable_logging=True,
        )
        self.assertEqual(len(body_bytes), vt.TRANSFER_BODY_BYTES)
        self.assertEqual(sha256_bytes(body_bytes), vt.TRANSFER_BODY_SHA256)

        secret = b"unit-executor-private-key-1234"
        fingerprint = vt._recovery_transfer_hash(
            vt.API_KEY_DOMAIN,
            bytearray(secret),
        )
        suffix = vt._recovery_transfer_suffix_hash(bytearray(secret))
        if credential_binding == "fingerprint":
            fingerprint = "0" * 64
        elif credential_binding == "suffix":
            suffix = "0" * 64
        elif credential_binding != "valid":
            raise AssertionError(credential_binding)

        artifacts = vt._recovery_transfer_artifacts(True)
        authorization = {
            "authorization_id": vt.RECOVERY_TRANSFER_ACTIVE_ID,
            "bindings": {
                "primary_request_sha256": vt.TRANSFER_OPT_OUT_REQUEST_SHA256,
                "normalized_http_request_sha256": (
                    vt.TRANSFER_OPT_OUT_NORMALIZED_REQUEST_SHA256
                ),
                "performance_transfer_plan_sha256": "1" * 64,
                "canonical_w_sha256": "2" * 64,
                "spoken_text_sha256": "3" * 64,
            },
            "runtime_bindings": {
                "git_commit": "a" * 40,
                "ffprobe_binary_path": "/usr/bin/false",
                "ffprobe_binary_sha256": "4" * 64,
                "ffprobe_version": "unit",
            },
            "prerequisites": {
                "selected_guide": {"sha256": vt.SELECTED_GUIDE_SHA256},
            },
            "account_authentication_evidence": {},
            "evidence_baseline": {"evidence_commit": "c" * 40},
        }
        now = datetime(2026, 8, 26, 14, 30, tzinfo=timezone.utc)

        def contract_factory() -> vt._RecoveryTransferExecutionContract:
            return vt._RecoveryTransferExecutionContract(
                root=root,
                authorization_path=authorization_path,
                authorization=copy.deepcopy(authorization),
                authorization_sha256=sha256_file(authorization_path),
                plan_path=plan_path,
                canonical_w_path=canonical_path,
                body=bytearray(body_bytes),
                normalized_request={
                    "url": (
                        f"{pt.TRANSFER_ENDPOINT}?enable_logging=true"
                        f"&output_format={pt.TRANSFER_PRIMARY_FORMAT}"
                    )
                },
                inputs=(),
                materialized_at=now - timedelta(minutes=20),
                expires_at=now + timedelta(minutes=30),
                browser_observed_at=now - timedelta(minutes=10),
                account_recorded_at=now - timedelta(minutes=20),
                data_recorded_at=now - timedelta(minutes=9),
                rights_recorded_at=now - timedelta(minutes=20),
                expected_fingerprint_sha256=fingerprint,
                expected_suffix_sha256=suffix,
                git_head="b" * 40,
                consumption_relative=vt.TRANSFER_SCOPE_LATCH_PATH,
                raw_relative=artifacts["raw_output_path"],
                working_relative=artifacts["working_output_path"],
                success_relative=artifacts["success_receipt_path"],
                failure_relative=artifacts["failure_receipt_path"],
                conversion_relative=artifacts["conversion_receipt_path"],
            )

        return SimpleNamespace(
            root=root,
            authorization_path=authorization_path,
            plan_path=plan_path,
            canonical_path=canonical_path,
            contract_factory=contract_factory,
            secret=secret,
            body_bytes=body_bytes,
            now=now,
            artifacts=artifacts,
        )

    @staticmethod
    def _recovery_executor_worker() -> SimpleNamespace:
        return SimpleNamespace(
            worker_source_sha256="5" * 64,
            interpreter_sha256="6" * 64,
            state="ready",
        )

    @staticmethod
    def _recovery_executor_source_proof() -> dict:
        return {
            "runtime_commit": "a" * 40,
            "evidence_commit": "c" * 40,
            "active_commit": "b" * 40,
            "worker_source_sha256": "5" * 64,
            "worker_interpreter_sha256": "6" * 64,
            "input_sha256s": {},
            "remote_state_checked": False,
            "git_network_called": False,
            "post_latch_revalidation_completed": True,
            "source_revalidated_before_latch": True,
            "source_revalidated_after_latch": True,
        }

    def test_recovery_executor_revalidates_private_sibling_fixture_input(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        repository = Path(temporary.name).resolve()
        contract_root = repository / "fixture-v05"
        sibling = (
            repository
            / "fixture-v04"
            / "receipts"
            / "provenance"
            / "AUTH-R2-remix-save.json"
        )
        contract_root.mkdir()
        sibling.parent.mkdir(parents=True)
        raw = b'{"schema_version":"unit-private-provenance"}\n'
        sibling.write_bytes(raw)
        sibling.chmod(0o600)
        binding = vt._recovery_transfer_input_binding(
            "prerequisite:original_c_save",
            sibling,
            raw,
            sha256_bytes(raw),
        )
        contract = SimpleNamespace(root=contract_root)

        with mock.patch.object(pt, "_guide_repository_root", return_value=repository):
            vt._revalidate_recovery_transfer_input(contract, binding)
            sibling.write_bytes(b"x" * len(raw))
            sibling.chmod(0o600)
            with self.assertRaisesRegex(ValidationError, "drifted"):
                vt._revalidate_recovery_transfer_input(contract, binding)

    def test_recovery_transfer_dotenv_reader_releases_view_and_calibrates_failure(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        dotenv = Path(temporary.name).resolve() / ".env"
        dotenv.write_bytes(b"ELEVENLABS_API_KEY=unit-private-key-1234\n")
        dotenv.chmod(0o600)
        captured: list[bytearray] = []
        parser = vt._parse_recovery_transfer_dotenv_key

        def observe(raw: bytearray) -> bytearray:
            captured.append(raw)
            return parser(raw)

        with (
            mock.patch.object(vt, "RECOVERY_DOTENV_PATH", dotenv),
            mock.patch.object(
                vt,
                "_parse_recovery_transfer_dotenv_key",
                side_effect=observe,
            ),
        ):
            held = vt._read_recovery_transfer_dotenv_key()
        self.assertEqual(held, bytearray(b"unit-private-key-1234"))
        self.assertEqual(captured, [bytearray()])
        vt._zero_mutable_buffer(held)

        captured.clear()

        def fail_after_read(raw: bytearray) -> bytearray:
            captured.append(raw)
            raise RuntimeError("unit parser failure after descriptor read")

        with (
            mock.patch.object(vt, "RECOVERY_DOTENV_PATH", dotenv),
            mock.patch.object(
                vt,
                "_parse_recovery_transfer_dotenv_key",
                side_effect=fail_after_read,
            ),
        ):
            with self.assertRaises(vt._RecoveryTransferCredentialReadFailure) as stopped:
                vt._read_recovery_transfer_dotenv_key()
        self.assertEqual(
            stopped.exception.credential_bytes_read_state,
            "bytes_read_not_accepted",
        )
        self.assertEqual(captured, [bytearray()])

    def test_recovery_executor_records_post_read_dotenv_failure_truthfully(self) -> None:
        fixture = self._recovery_executor_fixture()
        with (
            mock.patch.object(vt, "_require_recovery_transfer_containment_clear"),
            mock.patch.object(
                vt,
                "_preflight_recovery_transfer_core_limit",
                return_value=vt._RecoveryTransferCoreLimit(0, 0),
            ),
            mock.patch.object(vt, "_enter_recovery_transfer_core_limit"),
            mock.patch.object(
                vt,
                "_restore_recovery_transfer_core_limit",
                return_value=True,
            ),
            mock.patch.object(
                vt,
                "_build_recovery_transfer_execution_contract",
                side_effect=lambda *_args: fixture.contract_factory(),
            ),
            mock.patch.object(
                vt,
                "_prepare_voice_transfer_worker",
                side_effect=lambda: self._recovery_executor_worker(),
            ),
            mock.patch.object(
                vt,
                "_revalidate_recovery_transfer_before_latch",
                return_value=self._recovery_executor_source_proof(),
            ),
            mock.patch.object(vt, "_verify_recovery_transfer_post_latch_git_scope"),
            mock.patch.object(
                vt,
                "_read_recovery_transfer_dotenv_key",
                side_effect=vt._RecoveryTransferCredentialReadFailure(
                    "bytes_read_not_accepted"
                ),
            ),
            mock.patch.object(
                vt,
                "_dispose_recovery_transfer_worker",
                return_value=True,
            ),
            mock.patch.object(vt, "_execution_now", return_value=fixture.now),
            mock.patch.object(
                vt,
                "_perform_prepared_voice_transfer",
                side_effect=AssertionError("dotenv failure released GO"),
            ) as post,
        ):
            with self.assertRaisesRegex(ValidationError, "fixed_dotenv_read_failed"):
                vt.execute_recovery_evidence_voice_transfer(
                    fixture.authorization_path,
                    fixture.plan_path,
                    fixture.canonical_path,
                )
        post.assert_not_called()
        failure = pt._strict_json_bytes(
            (fixture.root / fixture.artifacts["failure_receipt_path"]).read_bytes(),
            "unit post-read dotenv failure",
        )
        self.assertEqual(failure["credential_descriptor_read_attempts"], 1)
        self.assertEqual(failure["credential_access_state"], "bytes_read_not_accepted")
        self.assertTrue(failure["credential_accessed"])
        self.assertFalse(failure["go_released"])
        self.assertEqual(failure["application_http_attempts"], 0)
        self.assertEqual(failure["network_call_state"], "not_called")

    def test_recovery_executor_one_exact_post_and_complete_private_outputs(self) -> None:
        fixture = self._recovery_executor_fixture()
        events: list[str] = []
        key_reference: bytearray | None = None
        body_reference: bytearray | None = None
        payload = b"\x01\x00" * 128

        def prepare_worker() -> SimpleNamespace:
            events.append("ready")
            return self._recovery_executor_worker()

        def before_latch(contract, _worker):
            self.assertEqual(events, ["ready"])
            self.assertFalse((contract.root / contract.consumption_relative).exists())
            events.append("before_latch")
            return self._recovery_executor_source_proof()

        def read_key() -> bytearray:
            self.assertTrue(
                (fixture.root / vt.TRANSFER_SCOPE_LATCH_PATH).is_file(),
                "credential read occurred before the shared latch",
            )
            events.append("key")
            return bytearray(fixture.secret)

        def perform(worker, *, api_key_material, body, timeout, absolute_deadline_ns):
            nonlocal key_reference, body_reference
            events.append("post")
            self.assertEqual(worker.state, "ready")
            self.assertEqual(bytes(api_key_material), fixture.secret)
            self.assertEqual(bytes(body), fixture.body_bytes)
            self.assertEqual(timeout, 30.0)
            self.assertEqual(absolute_deadline_ns, 31_000_000_000)
            key_reference = api_key_material
            body_reference = body
            worker.state = "closed"
            return vt._ElevenResponse(
                response_bytes=len(payload),
                response_sha256=sha256_bytes(payload),
                content_type="audio/pcm",
                content_encoding="identity",
                payload=payload,
                provider_identifiers={"request-id": "unit-request"},
                provider_usage={"character-count": 1},
            )

        def convert(raw_path, output_path, *, receipt_path, part_id, record_path):
            events.append("convert")
            self.assertEqual(raw_path.read_bytes(), payload)
            self.assertEqual(part_id, "P01-W0030-W0110")
            self.assertTrue(receipt_path.is_file())
            output_path.write_bytes(b"unit-working-wave")
            output_path.chmod(0o600)
            record_path.write_text('{"schema_version":"unit-conversion"}\n', encoding="utf-8")
            record_path.chmod(0o600)
            return {"working": {"sha256": sha256_file(output_path)}}

        geometry = {
            "container_interpretation": "raw",
            "codec_interpretation": "pcm_s16le",
            "sample_rate_hz_interpretation": 48_000,
            "channel_count_interpretation": 1,
            "bit_depth_interpretation": 16,
            "frame_count_under_mono_contract_interpretation": len(payload) // 2,
            "duration_seconds_under_mono_contract_interpretation": len(payload) / 96_000,
            "output_to_source_duration_ratio_under_mono_contract_interpretation": 1.0,
            "format_parameters_intrinsically_verified": False,
            "channel_count_intrinsically_verified": False,
            "frame_and_duration_computed_under_mono_contract_interpretation": True,
            "lossy_interpretation": False,
        }
        with (
            mock.patch.object(vt, "_require_recovery_transfer_containment_clear"),
            mock.patch.object(
                vt,
                "_preflight_recovery_transfer_core_limit",
                return_value=vt._RecoveryTransferCoreLimit(0, 0),
            ),
            mock.patch.object(vt, "_enter_recovery_transfer_core_limit"),
            mock.patch.object(vt, "_restore_recovery_transfer_core_limit", return_value=True),
            mock.patch.object(
                vt,
                "_build_recovery_transfer_execution_contract",
                side_effect=lambda *_args: fixture.contract_factory(),
            ),
            mock.patch.object(vt, "_prepare_voice_transfer_worker", side_effect=prepare_worker),
            mock.patch.object(
                vt,
                "_revalidate_recovery_transfer_before_latch",
                side_effect=before_latch,
            ),
            mock.patch.object(vt, "_verify_recovery_transfer_post_latch_git_scope"),
            mock.patch.object(vt, "_read_recovery_transfer_dotenv_key", side_effect=read_key) as key_read,
            mock.patch.object(vt, "_revalidate_prepared_transfer_worker"),
            mock.patch.object(
                vt,
                "_revalidate_recovery_transfer_contract",
                return_value=self._recovery_executor_source_proof(),
            ),
            mock.patch.object(vt, "_execution_now", return_value=fixture.now),
            mock.patch.object(vt.time, "monotonic_ns", return_value=1_000_000_000),
            mock.patch.object(vt, "_perform_prepared_voice_transfer", side_effect=perform) as post,
            mock.patch.object(vt, "_validate_raw_pcm", return_value=geometry),
            mock.patch(
                "oe_narration.audio.convert_recovery_evidence_working",
                side_effect=convert,
            ),
            mock.patch.object(
                urllib.request,
                "build_opener",
                side_effect=AssertionError("executor used a legacy or direct network path"),
            ),
        ):
            result = vt.execute_recovery_evidence_voice_transfer(
                fixture.authorization_path,
                fixture.plan_path,
                fixture.canonical_path,
                timeout=30.0,
            )

        self.assertEqual(events, ["ready", "before_latch", "key", "post", "convert"])
        self.assertEqual(key_read.call_count, 1)
        self.assertEqual(post.call_count, 1)
        self.assertIsNotNone(key_reference)
        self.assertIsNotNone(body_reference)
        self.assertTrue(all(value == 0 for value in key_reference))
        self.assertTrue(all(value == 0 for value in body_reference))
        self.assertEqual(result["account_get_calls_made"], 0)
        self.assertEqual(result["generation_post_calls_made"], 1)
        self.assertEqual(result["application_retries_made"], 0)
        self.assertEqual(result["outputs_received"], 1)
        self.assertFalse(result["retry_permitted"])
        self.assertFalse(result["replay_permitted"])
        for relative in (
            vt.TRANSFER_SCOPE_LATCH_PATH,
            fixture.artifacts["raw_output_path"],
            fixture.artifacts["working_output_path"],
            fixture.artifacts["success_receipt_path"],
            fixture.artifacts["conversion_receipt_path"],
        ):
            path = fixture.root / relative
            self.assertTrue(path.is_file(), relative)
            self.assertEqual(stat.S_IMODE(path.stat().st_mode), 0o600)
        run = pt._strict_json_bytes(
            (fixture.root / fixture.artifacts["success_receipt_path"]).read_bytes(),
            "unit recovery transfer run",
        )
        self.assertEqual(run["provider_evidence"]["account_get_calls_made"], 0)
        self.assertEqual(run["provider_evidence"]["generation_post_calls_made"], 1)
        self.assertEqual(run["provider_evidence"]["application_retries_made"], 0)

    def test_recovery_executor_credential_binding_burns_latch_and_blocks_replay(self) -> None:
        for binding in ("fingerprint", "suffix"):
            with self.subTest(binding=binding):
                fixture = self._recovery_executor_fixture(credential_binding=binding)
                key_references: list[bytearray] = []

                def read_key() -> bytearray:
                    self.assertTrue((fixture.root / vt.TRANSFER_SCOPE_LATCH_PATH).is_file())
                    value = bytearray(fixture.secret)
                    key_references.append(value)
                    return value

                with (
                    mock.patch.object(vt, "_require_recovery_transfer_containment_clear"),
                    mock.patch.object(
                        vt,
                        "_preflight_recovery_transfer_core_limit",
                        return_value=vt._RecoveryTransferCoreLimit(0, 0),
                    ),
                    mock.patch.object(vt, "_enter_recovery_transfer_core_limit"),
                    mock.patch.object(vt, "_restore_recovery_transfer_core_limit", return_value=True),
                    mock.patch.object(
                        vt,
                        "_build_recovery_transfer_execution_contract",
                        side_effect=lambda *_args: fixture.contract_factory(),
                    ),
                    mock.patch.object(
                        vt,
                        "_prepare_voice_transfer_worker",
                        side_effect=lambda: self._recovery_executor_worker(),
                    ),
                    mock.patch.object(
                        vt,
                        "_revalidate_recovery_transfer_before_latch",
                        return_value=self._recovery_executor_source_proof(),
                    ),
                    mock.patch.object(vt, "_verify_recovery_transfer_post_latch_git_scope"),
                    mock.patch.object(
                        vt,
                        "_read_recovery_transfer_dotenv_key",
                        side_effect=read_key,
                    ) as key_read,
                    mock.patch.object(vt, "_dispose_recovery_transfer_worker", return_value=True),
                    mock.patch.object(vt, "_execution_now", return_value=fixture.now),
                    mock.patch.object(
                        vt,
                        "_perform_prepared_voice_transfer",
                        side_effect=AssertionError("credential mismatch released GO"),
                    ) as post,
                ):
                    with self.assertRaisesRegex(
                        ValidationError,
                        f"credential_{binding}_mismatch",
                    ):
                        vt.execute_recovery_evidence_voice_transfer(
                            fixture.authorization_path,
                            fixture.plan_path,
                            fixture.canonical_path,
                        )
                    failure = pt._strict_json_bytes(
                        (fixture.root / fixture.artifacts["failure_receipt_path"]).read_bytes(),
                        "unit credential-binding failure",
                    )
                    self.assertFalse(failure["go_released"])
                    self.assertEqual(failure["application_http_attempts"], 0)
                    self.assertEqual(failure["account_get_calls_made"], 0)
                    self.assertTrue(failure["generation_post_budget_consumed"])
                    with self.assertRaisesRegex(ValidationError, "pre-latch readiness"):
                        vt.execute_recovery_evidence_voice_transfer(
                            fixture.authorization_path,
                            fixture.plan_path,
                            fixture.canonical_path,
                        )
                self.assertEqual(key_read.call_count, 1)
                post.assert_not_called()
                self.assertEqual(len(key_references), 1)
                self.assertTrue(all(value == 0 for value in key_references[0]))

    def test_recovery_executor_deadline_failure_is_reaped_and_nonretryable(self) -> None:
        fixture = self._recovery_executor_fixture()
        observed_deadlines: list[int] = []
        disposed: list[str] = []

        def timeout_failure(worker, **kwargs):
            observed_deadlines.append(kwargs["absolute_deadline_ns"])
            worker.state = "closed"
            failure = vt._post_go_worker_failure(
                "provider_request_elapsed_cap_exceeded",
                response_state="unknown",
            )
            failure.application_http_attempts = 1
            failure.child_containment_state = "confirmed_reaped"
            raise failure

        def dispose(worker) -> bool:
            disposed.append(worker.state)
            return True

        with (
            mock.patch.object(vt, "_require_recovery_transfer_containment_clear"),
            mock.patch.object(
                vt,
                "_preflight_recovery_transfer_core_limit",
                return_value=vt._RecoveryTransferCoreLimit(0, 0),
            ),
            mock.patch.object(vt, "_enter_recovery_transfer_core_limit"),
            mock.patch.object(vt, "_restore_recovery_transfer_core_limit", return_value=True),
            mock.patch.object(
                vt,
                "_build_recovery_transfer_execution_contract",
                side_effect=lambda *_args: fixture.contract_factory(),
            ),
            mock.patch.object(
                vt,
                "_prepare_voice_transfer_worker",
                side_effect=lambda: self._recovery_executor_worker(),
            ),
            mock.patch.object(
                vt,
                "_revalidate_recovery_transfer_before_latch",
                return_value=self._recovery_executor_source_proof(),
            ),
            mock.patch.object(vt, "_verify_recovery_transfer_post_latch_git_scope"),
            mock.patch.object(
                vt,
                "_read_recovery_transfer_dotenv_key",
                return_value=bytearray(fixture.secret),
            ),
            mock.patch.object(vt, "_revalidate_prepared_transfer_worker"),
            mock.patch.object(
                vt,
                "_revalidate_recovery_transfer_contract",
                return_value=self._recovery_executor_source_proof(),
            ),
            mock.patch.object(vt, "_execution_now", return_value=fixture.now),
            mock.patch.object(vt.time, "monotonic_ns", return_value=2_000_000_000),
            mock.patch.object(
                vt,
                "_perform_prepared_voice_transfer",
                side_effect=timeout_failure,
            ) as post,
            mock.patch.object(
                vt,
                "_dispose_recovery_transfer_worker",
                side_effect=dispose,
            ),
        ):
            with self.assertRaisesRegex(
                ValidationError,
                "provider_request_elapsed_cap_exceeded",
            ):
                vt.execute_recovery_evidence_voice_transfer(
                    fixture.authorization_path,
                    fixture.plan_path,
                    fixture.canonical_path,
                    timeout=7.0,
                )
        self.assertEqual(observed_deadlines, [9_000_000_000])
        self.assertEqual(post.call_count, 1)
        self.assertEqual(disposed, ["closed"])
        failure = pt._strict_json_bytes(
            (fixture.root / fixture.artifacts["failure_receipt_path"]).read_bytes(),
            "unit deadline failure",
        )
        self.assertTrue(failure["go_released"])
        self.assertEqual(failure["application_http_attempts"], 1)
        self.assertEqual(failure["child_containment_state"], "confirmed_reaped")
        self.assertFalse(failure["retry_permitted"])
        self.assertFalse(failure["replay_permitted"])

    def test_recovery_executor_cli_is_dry_by_default_and_execute_is_explicit(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        paths = []
        for name in ("authorization.json", "plan.json", "canonical.txt"):
            path = root / name
            path.write_text("{}\n", encoding="utf-8")
            paths.append(path)
        base = [
            "elevenlabs-voice-transfer-recovery",
            "--authorization", str(paths[0]),
            "--plan", str(paths[1]),
            "--canonical-w", str(paths[2]),
        ]
        parser = cli.build_parser()
        with (
            mock.patch.object(
                cli,
                "dry_run_recovery_evidence_voice_transfer",
                return_value={"valid": True, "network_called": False},
            ) as dry,
            mock.patch.object(
                cli,
                "execute_recovery_evidence_voice_transfer",
                return_value={"valid": True, "network_called": True},
            ) as execute,
        ):
            dry_result = cli.dispatch(parser.parse_args(base))
            self.assertFalse(dry_result["network_called"])
            dry.assert_called_once_with(*paths)
            execute.assert_not_called()

            execute_result = cli.dispatch(
                parser.parse_args([*base, "--execute", "--timeout", "12"])
            )
            self.assertTrue(execute_result["network_called"])
            execute.assert_called_once_with(*paths, timeout=12.0)
            with self.assertRaisesRegex(ValidationError, "--record is for dry runs"):
                cli.dispatch(
                    parser.parse_args(
                        [*base, "--execute", "--record", str(root / "record.json")]
                    )
                )
            with self.assertRaisesRegex(ValidationError, "at most 300"):
                cli.dispatch(parser.parse_args([*base, "--execute", "--timeout", "301"]))

    def test_recovery_capture_audio_test_binding_is_required_and_exact(self) -> None:
        bundle = self._recovery_transfer_draft_bundle()
        missing = copy.deepcopy(bundle.authorization)
        missing["runtime_bindings"].pop("capture_audio_tests_sha256")
        self.assertTrue(_local_schema_errors(missing, bundle.schema))

        bundle.authorization["runtime_bindings"]["capture_audio_tests_sha256"] = "0" * 64
        self._write_private_json(bundle.authorization_path, bundle.authorization)
        with self.assertRaises(ValidationError):
            self._validate_recovery_transfer_bundle(bundle)

    def test_additive_branch_preserves_frozen_legacy_transfer_functions(self) -> None:
        expected = {
            "_action_transfer": "e2823bac58a75d76d7afdc245938602cb17e7023e11cad0b753320dbd2666495",
            "_transfer_limits": "8a773e877022301208408a568b0d80ee55ea1926e78967ad3c64bdbc19b102c0",
            "_transfer_artifacts": "95b319bd487c4cdb812771cb796f1097947520685ee2e16959dbb774b50b7434",
            "validate_voice_transfer_execution_authorization": "fc4af9b7411def297d7b09324986a8923482e43904503da515791d368dbbaa6f",
            "dry_run_voice_transfer_execution": "7ab8fcc38853d43f171fecf1b9a5d5478bdf82d393bc3cb3d8e3818bf06015b0",
            "_build_transfer_contract": "7de62617c622cb4c9d34ea69ad6e32c502a0d89d1bbb3792e75e7cce022de61a",
            "_require_transfer_evidence_fresh": "7ac17d2578c985f52d688fe7b7cf550f67070c7257b6b1fb29353f4159353b9c",
            "_preflight_transfer_paths": "60283f73ce773662759ea4a084000aaebfd12abc9ec4c4167d20e346f7d76554",
            "execute_voice_transfer": "a7acc718fb02cabd7f743cab62a0379350cf7dbb761268e03d5f0b5cdca6862d",
            "_perform_elevenlabs_request": "cf5930432ae42ef35a0958371b0c8033575c414762534ce175c193677d0f0f48",
        }
        source = Path(vt.__file__).read_text(encoding="utf-8")
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
