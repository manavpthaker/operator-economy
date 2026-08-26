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


if __name__ == "__main__":
    unittest.main()
