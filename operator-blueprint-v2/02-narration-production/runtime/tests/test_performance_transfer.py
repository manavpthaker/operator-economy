from __future__ import annotations

import base64
import copy
import io
import json
import os
import shutil
import tempfile
import unittest
import urllib.error
import wave
from datetime import datetime, timedelta, timezone
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

from oe_narration.core import ValidationError, sha256_file
from oe_narration import performance_transfer as pt


class _FakeGoogleResponse:
    def __init__(
        self,
        data: bytes,
        *,
        status: int = 200,
        url: str = pt.GUIDE_ENDPOINT,
        content_type: str = "application/json; charset=UTF-8",
        declared_length: int | None = None,
        extra_headers: dict[str, str] | None = None,
    ) -> None:
        self._data = data
        self._offset = 0
        self._status = status
        self._url = url
        self.closed = False
        self.headers = {
            "Content-Type": content_type,
            "Content-Length": str(len(data) if declared_length is None else declared_length),
            **(extra_headers or {}),
        }

    def read(self, size: int = -1) -> bytes:
        if size < 0:
            size = len(self._data) - self._offset
        result = self._data[self._offset : self._offset + size]
        self._offset += len(result)
        return result

    def getcode(self) -> int:
        return self._status

    def geturl(self) -> str:
        return self._url

    def close(self) -> None:
        self.closed = True


class PerformanceTransferTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.narration_root = Path(__file__).resolve().parents[2]
        cls.fixture_name = (
            "step2-v0.5-ai-visibility-v1.1-"
            "synthetic-guide-to-saved-c-transfer-microtest"
        )
        cls.source_fixture = cls.narration_root / "fixtures" / cls.fixture_name
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
        provenance = (
            cls.narration_root
            / "fixtures"
            / "step2-v0.4-ai-visibility-v1.1-saved-c-p01-calibration"
            / "receipts"
            / "provenance"
        )
        cls.source_original_c_selection = provenance / "AUTH-R2-owner-selection-C.json"
        cls.source_original_c_save = provenance / "AUTH-R2-remix-save.json"

    @staticmethod
    def _write_json(path: Path, value: dict) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(value, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

    @staticmethod
    def _traceback_locals(exception: BaseException, function_name: str) -> dict:
        """Return only the named runtime frame; callers intentionally hold test secrets."""

        traceback = exception.__traceback__
        while traceback is not None:
            if traceback.tb_frame.f_code.co_name == function_name:
                return dict(traceback.tb_frame.f_locals)
            traceback = traceback.tb_next
        raise AssertionError(f"traceback does not contain {function_name}")

    @classmethod
    def _capture_failure(cls, operation, expected_type, function_name: str) -> tuple[BaseException, dict]:
        """Capture traceback locals before unittest strips the traceback from an exception."""

        try:
            operation()
        except expected_type as exception:
            return exception, cls._traceback_locals(exception, function_name)
        raise AssertionError(f"operation did not raise {expected_type.__name__}")

    def _copy_system(self) -> tuple[tempfile.TemporaryDirectory, Path, Path, Path]:
        temporary = tempfile.TemporaryDirectory()
        blueprint = Path(temporary.name).resolve() / "operator-blueprint-v2"
        fixtures = blueprint / "02-narration-production" / "fixtures"
        fixtures.mkdir(parents=True)
        fixture = fixtures / self.fixture_name
        shutil.copytree(
            self.source_fixture,
            fixture,
            ignore=shutil.ignore_patterns("outputs", "compiled", "receipts", "consumed"),
        )
        copied_w = (
            fixtures
            / "step2-v0.2-ai-visibility-v1.1"
            / "identity"
            / "canonical-w.txt"
        )
        copied_w.parent.mkdir(parents=True)
        shutil.copy2(self.source_w, copied_w)
        copied_script = (
            blueprint
            / "01-editorial"
            / "fixtures"
            / "step1-v1.4-e2e-ai-visibility-2026-08-22"
            / self.source_script.name
        )
        copied_script.parent.mkdir(parents=True)
        shutil.copy2(self.source_script, copied_script)
        copied_provenance = (
            fixtures
            / "step2-v0.4-ai-visibility-v1.1-saved-c-p01-calibration"
            / "receipts"
            / "provenance"
        )
        copied_provenance.mkdir(parents=True)
        shutil.copy2(self.source_original_c_selection, copied_provenance / self.source_original_c_selection.name)
        shutil.copy2(self.source_original_c_save, copied_provenance / self.source_original_c_save.name)
        return temporary, fixture, fixture / "performance-transfer-plan.json", copied_w

    def _refresh_draft_hashes(self, fixture: Path, plan: Path, w: Path) -> None:
        dry = pt.validate_performance_transfer_plan(plan, w)
        guide_path = fixture / "authorizations" / "01-google-synthetic-guide.DRAFT.json"
        guide = json.loads(guide_path.read_text(encoding="utf-8"))
        guide["bindings"]["performance_transfer_plan_sha256"] = dry["plan_sha256"]
        guide["bindings"]["request_set_sha256"] = dry["guide"]["request_set_sha256"]
        guide["authorized_limits"] = {
            "max_calls": 0,
            "max_outputs": 0,
            "max_request_body_bytes": 0,
            "max_total_request_bytes": 0,
            "max_output_duration_seconds": 0,
            "max_output_wav_bytes": 0,
            "max_total_audio_bytes": 0,
            "max_response_bytes_per_call": 0,
            "max_spend_usd": 0,
        }
        self._write_json(guide_path, guide)
        transfer_path = fixture / "authorizations" / "02-elevenlabs-saved-c-transfer.DRAFT.json"
        transfer = json.loads(transfer_path.read_text(encoding="utf-8"))
        transfer["bindings"]["performance_transfer_plan_sha256"] = dry["plan_sha256"]
        transfer["authorized_limits"] = {
            "max_calls": 0,
            "max_outputs": 0,
            "max_source_bytes": 0,
            "max_source_duration_seconds": 0,
            "max_submitted_seconds": 0,
            "max_spend_usd": 0,
        }
        self._write_json(transfer_path, transfer)

    def _activate_guide(self, fixture: Path, plan: Path, w: Path) -> Path:
        self._refresh_draft_hashes(fixture, plan, w)
        draft = fixture / "authorizations" / "01-google-synthetic-guide.DRAFT.json"
        value = json.loads(draft.read_text(encoding="utf-8"))
        now = datetime.now(timezone.utc)
        value.update(
            {
                "authorization_id": "AUTH-G1-test-exact-guide",
                "status": "active",
                "approved": True,
                "approved_by": "Manav Thaker",
                "approved_at": (now - timedelta(minutes=1)).isoformat(),
                "expires_at": (now + timedelta(hours=1)).isoformat(),
                "execution_ready": True,
                "blockers": [],
            }
        )
        value["billing_project_binding"]["quota_project_sha256"] = "a" * 64
        value["authorized_limits"] = {
            "max_calls": 2,
            "max_outputs": 2,
            "max_request_body_bytes": 1440,
            "max_total_request_bytes": 2880,
            "max_output_duration_seconds": 50,
            "max_output_wav_bytes": 2500000,
            "max_total_audio_bytes": 5000000,
            "max_response_bytes_per_call": 4000000,
            "max_spend_usd": 0.66,
        }
        value["consumption"]["status"] = "unconsumed"
        value["consumption"]["record_path"] = (
            "authorizations/consumed/AUTH-G1-test-exact-guide.consumed.json"
        )
        active = fixture / "authorizations" / "01-google-synthetic-guide.ACTIVE.test.json"
        self._write_json(active, value)
        return active

    def _activate_executable_guide(
        self,
        fixture: Path,
        plan: Path,
        w: Path,
        *,
        quota_project: str = "oe-test-quota-project",
    ) -> Path:
        active = self._activate_guide(fixture, plan, w)
        value = json.loads(active.read_text(encoding="utf-8"))
        value["billing_project_binding"]["quota_project_sha256"] = pt.sha256_bytes(
            quota_project.encode("utf-8")
        )
        self._write_json(active, value)
        return active

    @staticmethod
    def _wav_bytes(
        duration_seconds: float = 25.0,
        *,
        sample_rate: int = 24000,
        channels: int = 1,
        sample_width: int = 2,
    ) -> bytes:
        buffer = io.BytesIO()
        with wave.open(buffer, "wb") as handle:
            handle.setnchannels(channels)
            handle.setsampwidth(sample_width)
            handle.setframerate(sample_rate)
            frame_count = round(duration_seconds * sample_rate)
            handle.writeframes(b"\x00" * frame_count * channels * sample_width)
        return buffer.getvalue()

    @classmethod
    def _google_json_response(
        cls,
        wav_bytes: bytes | None = None,
        *,
        extra: dict | None = None,
    ) -> bytes:
        value = {
            "audioContent": base64.b64encode(
                wav_bytes if wav_bytes is not None else cls._wav_bytes()
            ).decode("ascii")
        }
        if extra:
            value.update(extra)
        return json.dumps(value, separators=(",", ":")).encode("utf-8")

    @staticmethod
    def _execution_artifacts(fixture: Path) -> dict[str, Path]:
        authorization_id = "AUTH-G1-test-exact-guide"
        return {
            "consumption": fixture / "authorizations" / "consumed" / f"{authorization_id}.consumed.json",
            "success": fixture / "receipts" / "google" / f"{authorization_id}.run.json",
            "failure": fixture / "receipts" / "google" / f"{authorization_id}.failure.json",
            "a": fixture / pt.GUIDE_DESTINATIONS[0],
            "b": fixture / pt.GUIDE_DESTINATIONS[1],
        }

    def _activate_transfer(
        self,
        fixture: Path,
        plan: Path,
        w: Path,
        *,
        zrm: bool = False,
    ) -> tuple[Path, dict[str, Path]]:
        self._refresh_draft_hashes(fixture, plan, w)
        timeline_now = datetime.now(timezone.utc)
        guide_approved_at = timeline_now - timedelta(minutes=15)
        guide_consumed_at = timeline_now - timedelta(minutes=12)
        guide_started_at = timeline_now - timedelta(minutes=11)
        guide_completed_at = timeline_now - timedelta(minutes=10)
        qa_reviewed_at = timeline_now - timedelta(minutes=8)
        guide_selected_at = timeline_now - timedelta(minutes=7)
        evidence_captured_at = timeline_now - timedelta(minutes=6)
        data_verified_at = timeline_now - timedelta(minutes=5)
        rights_approved_at = timeline_now - timedelta(minutes=2)
        transfer_approved_at = timeline_now - timedelta(minutes=1)
        outputs = fixture / "outputs" / "raw" / "google" / "P01-W0030-W0110"
        guide_path = outputs / "candidate-A.wav"
        guide_path.parent.mkdir(parents=True)
        with wave.open(str(guide_path), "wb") as handle:
            handle.setnchannels(1)
            handle.setsampwidth(2)
            handle.setframerate(24000)
            handle.writeframes(b"\x00\x00" * (24000 * 25))
        guide_sha = sha256_file(guide_path)
        guide_bytes = guide_path.stat().st_size
        guide_b_path = outputs / "candidate-B.wav"
        shutil.copy2(guide_path, guide_b_path)

        dry = pt.validate_performance_transfer_plan(plan, w)
        guide_auth_path = self._activate_guide(fixture, plan, w)
        guide_auth = json.loads(guide_auth_path.read_text(encoding="utf-8"))
        guide_auth["approved_at"] = guide_approved_at.isoformat()
        guide_auth["expires_at"] = (timeline_now + timedelta(minutes=30)).isoformat()
        self._write_json(guide_auth_path, guide_auth)
        guide_consumption_path = (
            fixture
            / "authorizations"
            / "consumed"
            / "AUTH-G1-test-exact-guide.consumed.json"
        )
        guide_consumption = {
            "schema_version": "oe-provider-authorization-consumption-v1",
            "authorization_id": "AUTH-G1-test-exact-guide",
            "authorization_sha256": sha256_file(guide_auth_path),
            "scope": pt.GUIDE_SCOPE,
            "provider": pt.GUIDE_PROVIDER,
            "status": "consumed_before_network",
            "consumed_at": guide_consumed_at.isoformat(),
            "consumed_before_network": True,
            "network_called_at_consumption": False,
            "performance_transfer_plan_sha256": dry["plan_sha256"],
            "request_set_sha256": dry["guide"]["request_set_sha256"],
            "reserved_limits": {
                "max_calls": 2,
                "max_outputs": 2,
                "max_request_body_bytes": 1440,
                "max_total_request_bytes": 2880,
                "max_output_duration_seconds": 50,
                "max_output_wav_bytes": 2500000,
                "max_total_audio_bytes": 5000000,
                "max_response_bytes_per_call": 4000000,
                "max_spend_usd": 0.66,
            },
            "credentials_recorded": False,
        }
        self._write_json(guide_consumption_path, guide_consumption)
        receipt_path = fixture / "receipts" / "google" / "guide-run.json"
        receipt = {
            "schema_version": "oe-synthetic-guide-run-receipt-v1",
            "provider": pt.GUIDE_PROVIDER,
            "endpoint": pt.GUIDE_ENDPOINT,
            "model_id": pt.GUIDE_MODEL,
            "voice_name": pt.GUIDE_VOICE,
            "language_code": pt.GUIDE_LANGUAGE,
            "outcome": "success",
            "authorization_id": "AUTH-G1-test-exact-guide",
            "authorization_consumed": True,
            "guide_authorization_path": guide_auth_path.relative_to(fixture).as_posix(),
            "guide_authorization_sha256": sha256_file(guide_auth_path),
            "guide_consumption_record_path": guide_consumption_path.relative_to(fixture).as_posix(),
            "guide_consumption_record_sha256": sha256_file(guide_consumption_path),
            "performance_transfer_plan_sha256": dry["plan_sha256"],
            "canonical_w_sha256": dry["canonical_w_sha256"],
            "microtest_token_slice_sha256": pt.MICROTEST_TOKEN_SLICE_SHA256,
            "spoken_text_sha256": pt.MICROTEST_TEXT_SHA256,
            "acting_prompt_sha256": pt.GUIDE_ACTING_PROMPT_SHA256,
            "request_set_sha256": dry["guide"]["request_set_sha256"],
            "request_body_sha256": pt.GUIDE_REQUEST_BODY_SHA256,
            "request_body_bytes": 1440,
            "total_request_bytes": 2880,
            "provider_calls_made": 2,
            "provider_outputs_received": 2,
            "provider_response_bytes_total": 3200200,
            "provider_spend_usd": 0.66,
            "provider_spend_semantics": "modeled_authorized_ceiling_per_attempt_not_provider_invoice",
            "credential_mechanism": "gcloud_application_default_print_access_token",
            "credential_refresh_attempted": True,
            "quota_project_sha256": "a" * 64,
            "started_at": guide_started_at.isoformat(),
            "completed_at": guide_completed_at.isoformat(),
            "outputs": [
                {
                    "request_id": "gemini-guide-01",
                    "path": guide_path.relative_to(fixture).as_posix(),
                    "sha256": guide_sha,
                    "byte_count": guide_bytes,
                    "duration_seconds": 25.0,
                    "provider_response_bytes": 1600100,
                    "response_sha256": "c" * 64,
                    "request_started_at": guide_started_at.isoformat(),
                    "request_completed_at": (guide_started_at + timedelta(seconds=25)).isoformat(),
                    "provider_identifiers": {},
                    "provider_usage": {},
                    "container": "wav",
                    "codec": "pcm_s16le",
                    "sample_rate_hz": 24000,
                    "channels": 1,
                    "bit_depth": 16,
                    "frame_count": 600000,
                },
                {
                    "request_id": "gemini-guide-02",
                    "path": guide_b_path.relative_to(fixture).as_posix(),
                    "sha256": sha256_file(guide_b_path),
                    "byte_count": guide_b_path.stat().st_size,
                    "duration_seconds": 25.0,
                    "provider_response_bytes": 1600100,
                    "response_sha256": "d" * 64,
                    "request_started_at": (guide_started_at + timedelta(seconds=26)).isoformat(),
                    "request_completed_at": guide_completed_at.isoformat(),
                    "provider_identifiers": {},
                    "provider_usage": {},
                    "container": "wav",
                    "codec": "pcm_s16le",
                    "sample_rate_hz": 24000,
                    "channels": 1,
                    "bit_depth": 16,
                    "frame_count": 600000,
                },
            ],
            "retries_made": 0,
            "redirects_followed": 0,
            "fallbacks_used": 0,
            "credentials_recorded": False,
            "network_called": True,
            "creative_approved": False,
            "cross_provider_transfer_authorized": False,
            "voice_transfer_authorized": False,
            "full_capture_authorized": False,
            "step3_authorized": False,
            "publication_authorized": False,
        }
        self._write_json(receipt_path, receipt)

        qa_path = fixture / "reviews" / "guide-qa.json"
        qa = {
            "schema_version": "oe-synthetic-guide-qa-v1",
            "selected_guide_sha256": guide_sha,
            "spoken_text_sha256": pt.MICROTEST_TEXT_SHA256,
            "lexical_exact": True,
            "technical_pass": True,
            "performance_pass": True,
            "understandable_without_music_or_visuals": True,
            "reviewed_by": "Manav Thaker",
            "reviewed_at": qa_reviewed_at.isoformat(),
        }
        self._write_json(qa_path, qa)

        selection_path = fixture / "reviews" / "guide-owner-selection.json"
        selection = {
            "schema_version": "oe-synthetic-guide-owner-selection-v1",
            "selected_guide_sha256": guide_sha,
            "guide_qa_sha256": sha256_file(qa_path),
            "selected_by": "Manav Thaker",
            "selected_at": guide_selected_at.isoformat(),
            "approved_for_voice_transfer": True,
        }
        self._write_json(selection_path, selection)

        evidence_path = fixture / "receipts" / "elevenlabs" / "data-use-evidence.json"
        evidence = {
            "schema_version": "oe-elevenlabs-account-data-use-evidence-v1",
            "provider": "elevenlabs",
            "account_scope_binding_sha256": "b" * 64,
            "captured_at": evidence_captured_at.isoformat(),
            "improve_models_for_everyone": False if not zrm else True,
            "zero_retention_mode": zrm,
            "chosen_enable_logging": not zrm,
            "protection_mode": (
                pt.ENTERPRISE_ZRM_PROTECTION
                if zrm
                else pt.ACCOUNT_TRAINING_OPT_OUT_PROTECTION
            ),
            "opt_out_processed": not zrm,
            "protection_effective_for_new_submissions": True,
            "zrm_eligible_and_confirmed": zrm,
        }
        self._write_json(evidence_path, evidence)
        data_path = fixture / "receipts" / "elevenlabs" / "data-use.json"
        data_use = {
            "schema_version": "oe-elevenlabs-data-use-assurance-v1",
            "provider": "elevenlabs",
            "exact_guide_sha256": guide_sha,
            "cross_provider_upload_permitted": True,
            "improve_models_for_everyone": False if not zrm else True,
            "zero_retention_mode": zrm,
            "protection_mode": (
                pt.ENTERPRISE_ZRM_PROTECTION
                if zrm
                else pt.ACCOUNT_TRAINING_OPT_OUT_PROTECTION
            ),
            "opt_out_processed": not zrm,
            "protection_effective_for_new_submissions": True,
            "zrm_eligible_and_confirmed": zrm,
            "chosen_enable_logging": not zrm,
            "account_scope_binding_sha256": "b" * 64,
            "verified_by": "Manav Thaker",
            "verified_at": data_verified_at.isoformat(),
            "evidence": {
                "path": evidence_path.relative_to(fixture).as_posix(),
                "sha256": sha256_file(evidence_path),
            },
        }
        self._write_json(data_path, data_use)

        primary = pt._compile_multipart(
            guide_path.read_bytes(), guide_sha, pt.TRANSFER_PRIMARY_FORMAT,
            enable_logging=not zrm,
        )
        fallback = pt._compile_multipart(
            guide_path.read_bytes(), guide_sha, pt.TRANSFER_FALLBACK_FORMAT,
            enable_logging=not zrm,
        )
        prior_root = (
            fixture.parent
            / "step2-v0.4-ai-visibility-v1.1-saved-c-p01-calibration"
            / "receipts"
            / "provenance"
        )
        prior_selection = prior_root / "AUTH-R2-owner-selection-C.json"
        prior_save = prior_root / "AUTH-R2-remix-save.json"

        rights_path = fixture / "receipts" / "elevenlabs" / "voice-rights.json"
        rights = {
            "schema_version": "oe-elevenlabs-voice-transfer-rights-v1",
            "provider": "elevenlabs",
            "authorization_id": "AUTH-V1-test-exact-transfer",
            "performance_transfer_plan_sha256": dry["plan_sha256"],
            "primary_request_sha256": pt.sha256_bytes(pt._compact_json_bytes(primary)),
            "primary_multipart_body_sha256": primary["multipart_body_sha256"],
            "target_voice_id": pt.TRANSFER_TARGET_VOICE_ID,
            "voice_owner": "Manav Thaker",
            "consent_owner": "Manav Thaker",
            "exact_guide_sha256": guide_sha,
            "owner_approval": True,
            "voice_changer_permitted": True,
            "approved_at": rights_approved_at.isoformat(),
            "bounded_microtest_only": True,
            "full_capture_permitted": False,
            "original_c_provenance": {
                "owner_selection_path": prior_selection.relative_to(fixture.parents[2]).as_posix(),
                "owner_selection_sha256": sha256_file(prior_selection),
                "saved_voice_receipt_path": prior_save.relative_to(fixture.parents[2]).as_posix(),
                "saved_voice_receipt_sha256": sha256_file(prior_save),
            },
        }
        self._write_json(rights_path, rights)

        draft = fixture / "authorizations" / "02-elevenlabs-saved-c-transfer.DRAFT.json"
        auth = json.loads(draft.read_text(encoding="utf-8"))
        auth.update(
            {
                "authorization_id": "AUTH-V1-test-exact-transfer",
                "status": "active",
                "approved": True,
                "approved_by": "Manav Thaker",
                "approved_at": transfer_approved_at.isoformat(),
                "expires_at": (timeline_now + timedelta(hours=1)).isoformat(),
                "execution_ready": True,
                "blockers": [],
            }
        )
        auth["authorized_limits"] = {
            "max_calls": 2,
            "max_outputs": 1,
            "max_source_bytes": 50000000,
            "max_source_duration_seconds": 50,
            "max_submitted_seconds": 100,
            "max_spend_usd": 0.24,
        }
        auth["consumption"]["status"] = "unconsumed"
        auth["consumption"]["record_path"] = (
            "authorizations/consumed/AUTH-V1-test-exact-transfer.consumed.json"
        )
        auth["bindings"].update(
            {
                "selected_guide_sha256": guide_sha,
                "primary_request_sha256": pt.sha256_bytes(pt._compact_json_bytes(primary)),
                "primary_multipart_body_sha256": primary["multipart_body_sha256"],
                "primary_multipart_body_bytes": primary["multipart_body_bytes"],
                "conditional_fallback_request_sha256": pt.sha256_bytes(pt._compact_json_bytes(fallback)),
                "conditional_fallback_multipart_body_sha256": fallback["multipart_body_sha256"],
                "conditional_fallback_multipart_body_bytes": fallback["multipart_body_bytes"],
                "enable_logging": not zrm,
            }
        )
        auth["prerequisites"] = {
            "selected_guide": {
                "state": "verified",
                "path": guide_path.relative_to(fixture).as_posix(),
                "sha256": guide_sha,
                "byte_count": guide_bytes,
                "duration_seconds": 25.0,
                "container": "wav",
                "codec": "pcm_s16le",
                "sample_rate_hz": 24000,
                "channels": 1,
                "guide_request_id": "gemini-guide-01",
                "guide_run_receipt_path": receipt_path.relative_to(fixture).as_posix(),
                "guide_run_receipt_sha256": sha256_file(receipt_path),
            },
            "guide_qa": {
                "state": "verified",
                "path": qa_path.relative_to(fixture).as_posix(),
                "sha256": sha256_file(qa_path),
            },
            "owner_selection": {
                "state": "verified",
                "path": selection_path.relative_to(fixture).as_posix(),
                "sha256": sha256_file(selection_path),
            },
            "elevenlabs_data_use": {
                "state": "verified",
                "path": data_path.relative_to(fixture).as_posix(),
                "sha256": sha256_file(data_path),
            },
            "target_voice_rights": {
                "state": "verified",
                "path": rights_path.relative_to(fixture).as_posix(),
                "sha256": sha256_file(rights_path),
            },
        }
        active = fixture / "authorizations" / "02-elevenlabs-saved-c-transfer.ACTIVE.test.json"
        self._write_json(active, auth)
        return active, {
            "guide": guide_path,
            "receipt": receipt_path,
            "qa": qa_path,
            "selection": selection_path,
            "data": data_path,
            "evidence": evidence_path,
            "rights": rights_path,
            "guide_auth": guide_auth_path,
            "guide_consumption": guide_consumption_path,
        }

    def test_frozen_plan_compiles_two_identical_unseeded_google_requests(self) -> None:
        temporary, fixture, plan, w = self._copy_system()
        self.addCleanup(temporary.cleanup)
        dry = pt.validate_performance_transfer_plan(plan, w)
        requests = dry["guide"]["requests"]
        self.assertEqual(len(requests), 2)
        self.assertEqual(requests[0]["request_body"], requests[1]["request_body"])
        self.assertEqual(requests[0]["request_body_sha256"], pt.GUIDE_REQUEST_BODY_SHA256)
        self.assertEqual(requests[0]["request_body_bytes"], 1440)
        self.assertNotIn("seed", requests[0]["request_body"])
        self.assertEqual(requests[0]["request_body"]["input"]["text"], pt.MICROTEST_TEXT)
        self.assertFalse(dry["network_called"])
        self.assertFalse(dry["credentials_accessed"])
        self.assertFalse(dry["full_capture_authorized"])

    def test_plan_rejects_word_prompt_provider_and_hash_drift(self) -> None:
        mutations = [
            ("microtest", "start_token", 31),
            ("guide", "acting_prompt", pt.GUIDE_ACTING_PROMPT + " drift"),
            ("guide", "model_id", "gemini-2.5-flash-tts"),
            ("guide", "voice_name", "wrong"),
            ("guide", "endpoint", "https://example.invalid"),
            ("guide", "request_body_sha256", "0" * 64),
            ("voice_transfer", "target_voice_id", "wrong"),
            ("voice_transfer", "seed", 1),
        ]
        for section, key, value in mutations:
            with self.subTest(section=section, key=key):
                temporary, _fixture, plan, w = self._copy_system()
                self.addCleanup(temporary.cleanup)
                data = json.loads(plan.read_text(encoding="utf-8"))
                data[section][key] = value
                self._write_json(plan, data)
                with self.assertRaises(ValidationError):
                    pt.validate_performance_transfer_plan(plan, w)

    def test_plan_and_envelope_reject_bool_numeric_coercion(self) -> None:
        plan_mutations = (
            ("guide", "identical_unseeded_requests", 1),
            ("authority", "external_action_authorized", 0),
            ("voice_transfer", "remove_background_noise", 0),
        )
        for section, key, value in plan_mutations:
            with self.subTest(section=section, key=key):
                temporary, _fixture, plan, w = self._copy_system()
                self.addCleanup(temporary.cleanup)
                document = json.loads(plan.read_text(encoding="utf-8"))
                document[section][key] = value
                self._write_json(plan, document)
                with self.assertRaises(ValidationError):
                    pt.validate_performance_transfer_plan(plan, w)

        temporary, fixture, plan, w = self._copy_system()
        self.addCleanup(temporary.cleanup)
        envelope_path = fixture / "performance-envelope.json"
        envelope = json.loads(envelope_path.read_text(encoding="utf-8"))
        envelope["passages"][0]["energy"]["start"] = True
        self._write_json(envelope_path, envelope)
        document = json.loads(plan.read_text(encoding="utf-8"))
        document["performance_envelope"]["sha256"] = sha256_file(envelope_path)
        self._write_json(plan, document)
        with self.assertRaises(ValidationError):
            pt.validate_performance_transfer_plan(plan, w)

    def test_envelope_canonical_w_rejects_symlink_alias_after_rehash(self) -> None:
        temporary, fixture, plan, w = self._copy_system()
        self.addCleanup(temporary.cleanup)
        alias = fixture / "canonical-w-link.txt"
        alias.symlink_to(w)
        envelope_path = fixture / "performance-envelope.json"
        envelope = json.loads(envelope_path.read_text(encoding="utf-8"))
        envelope["canonical_w"]["path"] = alias.name
        self._write_json(envelope_path, envelope)
        document = json.loads(plan.read_text(encoding="utf-8"))
        document["performance_envelope"]["sha256"] = sha256_file(envelope_path)
        self._write_json(plan, document)
        with self.assertRaises(ValidationError):
            pt.validate_performance_transfer_plan(plan, w)

    def test_provider_adapters_remain_semantically_bound_after_rehash(self) -> None:
        mutations = (
            ("google", "google-cloud-gemini-tts.json", "network_called"),
            (
                "elevenlabs_voice_changer",
                "elevenlabs-voice-changer-saved-c.BLOCKED.json",
                "request_compiled",
            ),
        )
        for binding_name, filename, key in mutations:
            with self.subTest(adapter=binding_name):
                temporary, fixture, plan, w = self._copy_system()
                self.addCleanup(temporary.cleanup)
                adapter = fixture / "adapters" / filename
                value = json.loads(adapter.read_text(encoding="utf-8"))
                value[key] = True
                self._write_json(adapter, value)
                plan_value = json.loads(plan.read_text(encoding="utf-8"))
                plan_value["provider_adapters"][binding_name]["sha256"] = sha256_file(adapter)
                self._write_json(plan, plan_value)
                with self.assertRaises(ValidationError):
                    pt.validate_performance_transfer_plan(plan, w)

    def test_envelope_rejects_unknown_keys_anchor_and_boundary_drift(self) -> None:
        mutations = ("unknown", "anchor", "boundary")
        for mutation in mutations:
            with self.subTest(mutation=mutation):
                temporary, fixture, plan, w = self._copy_system()
                self.addCleanup(temporary.cleanup)
                envelope_path = fixture / "performance-envelope.json"
                envelope = json.loads(envelope_path.read_text(encoding="utf-8"))
                if mutation == "unknown":
                    envelope["rewrite_allowed"] = True
                elif mutation == "anchor":
                    envelope["passages"][0]["required_anchors"][1]["at_token"] = 38
                else:
                    envelope["passages"][0]["paragraph_boundaries"][-1]["end_token"] = 109
                self._write_json(envelope_path, envelope)
                plan_data = json.loads(plan.read_text(encoding="utf-8"))
                plan_data["performance_envelope"]["sha256"] = sha256_file(envelope_path)
                self._write_json(plan, plan_data)
                with self.assertRaises(ValidationError):
                    pt.validate_performance_transfer_plan(plan, w)

    def test_transport_and_canonical_source_swap_fail(self) -> None:
        temporary, fixture, plan, w = self._copy_system()
        self.addCleanup(temporary.cleanup)
        transport = fixture / "passages" / "P01-W0030-W0110.locked.txt"
        transport.write_text(pt.MICROTEST_TEXT + " drift", encoding="utf-8")
        with self.assertRaises(ValidationError):
            pt.validate_performance_transfer_plan(plan, w)

        temporary2, _fixture2, plan2, w2 = self._copy_system()
        self.addCleanup(temporary2.cleanup)
        w2.write_text(w2.read_text(encoding="utf-8").replace("Your\n", "A\n", 1), encoding="utf-8")
        with self.assertRaises(ValidationError):
            pt.validate_performance_transfer_plan(plan2, w2)

    def test_draft_authorizations_are_zero_authority_and_credential_free(self) -> None:
        temporary, fixture, plan, w = self._copy_system()
        self.addCleanup(temporary.cleanup)
        self._refresh_draft_hashes(fixture, plan, w)
        guide_auth = fixture / "authorizations" / "01-google-synthetic-guide.DRAFT.json"
        transfer_auth = fixture / "authorizations" / "02-elevenlabs-saved-c-transfer.DRAFT.json"
        with mock.patch.dict(
            os.environ,
            {
                "GOOGLE_CLOUD_QUOTA_PROJECT": "must-not-be-read",
                "ELEVENLABS_API_KEY": "must-not-be-read",
            },
            clear=True,
        ):
            guide = pt.validate_synthetic_guide_authorization(guide_auth, plan, w)
            transfer = pt.dry_run_voice_transfer(plan, w, transfer_auth)
        self.assertFalse(guide["provider_action_authorized"])
        self.assertFalse(guide["network_authorized"])
        self.assertFalse(guide["execution_transport_available"])
        self.assertFalse(transfer["provider_action_authorized"])
        self.assertFalse(transfer["request_compiled"])

    def test_draft_nonzero_limits_unknown_field_and_scope_swap_fail(self) -> None:
        for mutation in ("nonzero", "unknown", "scope"):
            with self.subTest(mutation=mutation):
                temporary, fixture, plan, w = self._copy_system()
                self.addCleanup(temporary.cleanup)
                self._refresh_draft_hashes(fixture, plan, w)
                auth_path = fixture / "authorizations" / "01-google-synthetic-guide.DRAFT.json"
                auth = json.loads(auth_path.read_text(encoding="utf-8"))
                if mutation == "nonzero":
                    auth["authorized_limits"]["max_calls"] = 2
                elif mutation == "unknown":
                    auth["also_authorizes_voice_transfer"] = True
                else:
                    auth["scope"] = pt.TRANSFER_SCOPE
                self._write_json(auth_path, auth)
                with self.assertRaises(ValidationError):
                    pt.validate_synthetic_guide_authorization(auth_path, plan, w)

    def test_active_guide_authority_is_exact_and_transport_available(self) -> None:
        temporary, fixture, plan, w = self._copy_system()
        self.addCleanup(temporary.cleanup)
        active = self._activate_guide(fixture, plan, w)
        result = pt.validate_synthetic_guide_authorization(active, plan, w)
        self.assertTrue(result["provider_action_authorized"])
        self.assertTrue(result["network_authorized"])
        self.assertTrue(result["execution_transport_available"])
        self.assertTrue(result["quota_project_runtime_check_required"])
        self.assertEqual(result["maximum"]["output_duration_seconds"], 50)
        self.assertEqual(result["maximum"]["output_wav_bytes"], 2500000)
        self.assertEqual(result["maximum"]["total_audio_bytes"], 5000000)
        self.assertEqual(result["maximum"]["response_bytes_per_call"], 4000000)

    def test_active_guide_rejects_response_and_audio_ceiling_tamper(self) -> None:
        for key, value in (
            ("max_output_duration_seconds", 51),
            ("max_output_wav_bytes", 2500001),
            ("max_total_audio_bytes", 5000001),
            ("max_response_bytes_per_call", 4000001),
        ):
            with self.subTest(limit=key):
                temporary, fixture, plan, w = self._copy_system()
                self.addCleanup(temporary.cleanup)
                active = self._activate_guide(fixture, plan, w)
                auth = json.loads(active.read_text(encoding="utf-8"))
                auth["authorized_limits"][key] = value
                self._write_json(active, auth)
                with self.assertRaises(ValidationError):
                    pt.validate_synthetic_guide_authorization(active, plan, w)

    def test_g1_execution_consumes_before_token_and_makes_exactly_two_posts(self) -> None:
        temporary, fixture, plan, w = self._copy_system()
        self.addCleanup(temporary.cleanup)
        quota_project = "oe-test-quota-project"
        access_token = "ya29.private-test-access-token"
        eleven_secret = "xi-unrelated-eleven-secret"
        active = self._activate_executable_guide(
            fixture,
            plan,
            w,
            quota_project=quota_project,
        )
        paths = self._execution_artifacts(fixture)
        response_body = self._google_json_response()
        calls: list = []

        def token_loader(executable: str, timeout: float) -> str:
            self.assertEqual(executable, "/test/gcloud")
            self.assertTrue(paths["consumption"].is_file())
            self.assertFalse(paths["a"].exists())
            return access_token

        def open_once(request, timeout: float):
            self.assertTrue(paths["consumption"].is_file())
            calls.append(request)
            self.assertEqual(request.full_url, pt.GUIDE_ENDPOINT)
            self.assertEqual(request.get_method(), "POST")
            self.assertEqual(len(request.data), 1440)
            self.assertEqual(pt.sha256_bytes(request.data), pt.GUIDE_REQUEST_BODY_SHA256)
            headers = {key.lower(): value for key, value in request.header_items()}
            self.assertEqual(headers["authorization"], f"Bearer {access_token}")
            self.assertEqual(headers["content-type"], "application/json")
            self.assertEqual(headers["x-goog-user-project"], quota_project)
            return _FakeGoogleResponse(
                response_body,
                extra_headers={
                    "X-Goog-Request-Id": (
                        "ya29.another-provider-secret-value"
                        if len(calls) == 1
                        else "safe-request-2"
                    ),
                    "X-RateLimit-Remaining": "7",
                },
            )

        with mock.patch.dict(
            os.environ,
            {
                pt.GUIDE_QUOTA_PROJECT_ENV: quota_project,
                "ELEVENLABS_API_KEY": eleven_secret,
            },
            clear=True,
        ), mock.patch.object(pt, "_preflight_google_adc", return_value="/test/gcloud"), mock.patch.object(
            pt, "_load_google_access_token", side_effect=token_loader
        ), mock.patch.object(pt, "_open_google_request", side_effect=open_once):
            result = pt.execute_synthetic_guide(active, plan, w)

        self.assertEqual(len(calls), 2)
        self.assertEqual(calls[0].data, calls[1].data)
        self.assertEqual(result["provider_calls_made"], 2)
        self.assertEqual(result["outputs_received"], 2)
        self.assertTrue(paths["success"].is_file())
        self.assertFalse(paths["failure"].exists())
        for key in ("consumption", "success", "a", "b"):
            self.assertEqual(paths[key].stat().st_mode & 0o777, 0o600)

        receipt = json.loads(paths["success"].read_text(encoding="utf-8"))
        self.assertEqual(receipt["provider_calls_made"], 2)
        self.assertEqual(receipt["provider_outputs_received"], 2)
        self.assertEqual(receipt["total_request_bytes"], 2880)
        self.assertEqual(receipt["retries_made"], 0)
        self.assertEqual(receipt["redirects_followed"], 0)
        self.assertEqual(receipt["fallbacks_used"], 0)
        self.assertFalse(receipt["voice_transfer_authorized"])
        self.assertFalse(receipt["full_capture_authorized"])
        self.assertEqual(receipt["outputs"][0]["provider_identifiers"], {})
        self.assertEqual(
            receipt["outputs"][1]["provider_identifiers"],
            {"x-goog-request-id": "safe-request-2"},
        )
        for output in receipt["outputs"]:
            self.assertGreaterEqual(output["duration_seconds"], 20)
            self.assertLessEqual(output["duration_seconds"], 50)
            self.assertEqual(output["sample_rate_hz"], 24000)
            self.assertEqual(output["channels"], 1)
            self.assertEqual(output["bit_depth"], 16)
        self.assertLessEqual(
            datetime.fromisoformat(receipt["outputs"][0]["request_completed_at"]),
            datetime.fromisoformat(receipt["outputs"][1]["request_started_at"]),
        )

        public_bytes = json.dumps(result, sort_keys=True).encode("utf-8")
        artifact_bytes = paths["consumption"].read_bytes() + paths["success"].read_bytes()
        for forbidden in (
            access_token.encode(),
            quota_project.encode(),
            eleven_secret.encode(),
            pt.GUIDE_ACTING_PROMPT.encode(),
            response_body[:80],
        ):
            self.assertNotIn(forbidden, public_bytes)
            self.assertNotIn(forbidden, artifact_bytes)

        with mock.patch.dict(os.environ, {pt.GUIDE_QUOTA_PROJECT_ENV: quota_project}, clear=True), mock.patch.object(
            pt, "_preflight_google_adc"
        ) as credential_preflight:
            with self.assertRaises(ValidationError):
                pt.execute_synthetic_guide(active, plan, w)
        credential_preflight.assert_not_called()

    def test_actual_g1_success_receipt_requires_separate_v1_owner_chain(self) -> None:
        temporary, fixture, plan, w = self._copy_system()
        self.addCleanup(temporary.cleanup)
        quota_project = "oe-test-quota-project"
        active_g1 = self._activate_executable_guide(fixture, plan, w, quota_project=quota_project)
        actual = self._execution_artifacts(fixture)
        response_body = self._google_json_response()
        with mock.patch.dict(os.environ, {pt.GUIDE_QUOTA_PROJECT_ENV: quota_project}, clear=True), mock.patch.object(
            pt, "_preflight_google_adc", return_value="/test/gcloud"
        ), mock.patch.object(pt, "_load_google_access_token", return_value="ya29.private-test-access-token"), mock.patch.object(
            pt,
            "_open_google_request",
            side_effect=[_FakeGoogleResponse(response_body), _FakeGoogleResponse(response_body)],
        ):
            pt.execute_synthetic_guide(active_g1, plan, w)

        draft_v1 = fixture / "authorizations" / "02-elevenlabs-saved-c-transfer.DRAFT.json"
        blocked = pt.dry_run_voice_transfer(plan, w, draft_v1)
        self.assertFalse(blocked["request_compiled"])
        self.assertFalse(blocked["provider_action_authorized"])
        self.assertFalse(blocked["network_authorized"])

        preserved = {
            "guide_auth": active_g1.read_bytes(),
            "consumption": actual["consumption"].read_bytes(),
            "receipt": actual["success"].read_bytes(),
            "a": actual["a"].read_bytes(),
            "b": actual["b"].read_bytes(),
        }
        actual["a"].unlink()
        actual["b"].unlink()
        actual["a"].parent.rmdir()
        active_v1, chain = self._activate_transfer(fixture, plan, w)
        active_g1.write_bytes(preserved["guide_auth"])
        actual["consumption"].write_bytes(preserved["consumption"])
        actual["success"].write_bytes(preserved["receipt"])
        actual["a"].write_bytes(preserved["a"])
        actual["b"].write_bytes(preserved["b"])
        self.assertEqual(sha256_file(chain["guide"]), sha256_file(actual["a"]))

        post_at = datetime.now(timezone.utc).isoformat()
        qa = json.loads(chain["qa"].read_text(encoding="utf-8"))
        qa["reviewed_at"] = post_at
        self._write_json(chain["qa"], qa)
        selection = json.loads(chain["selection"].read_text(encoding="utf-8"))
        selection["guide_qa_sha256"] = sha256_file(chain["qa"])
        selection["selected_at"] = post_at
        self._write_json(chain["selection"], selection)
        evidence = json.loads(chain["evidence"].read_text(encoding="utf-8"))
        evidence["captured_at"] = post_at
        self._write_json(chain["evidence"], evidence)
        data_use = json.loads(chain["data"].read_text(encoding="utf-8"))
        data_use["verified_at"] = post_at
        data_use["evidence"]["sha256"] = sha256_file(chain["evidence"])
        self._write_json(chain["data"], data_use)
        rights = json.loads(chain["rights"].read_text(encoding="utf-8"))
        rights["approved_at"] = post_at
        self._write_json(chain["rights"], rights)
        v1 = json.loads(active_v1.read_text(encoding="utf-8"))
        v1["approved_at"] = post_at
        v1["expires_at"] = (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat()
        v1["prerequisites"]["selected_guide"]["guide_run_receipt_path"] = actual[
            "success"
        ].relative_to(fixture).as_posix()
        v1["prerequisites"]["selected_guide"]["guide_run_receipt_sha256"] = sha256_file(
            actual["success"]
        )
        for key, path_key in (
            ("guide_qa", "qa"),
            ("owner_selection", "selection"),
            ("elevenlabs_data_use", "data"),
            ("target_voice_rights", "rights"),
        ):
            v1["prerequisites"][key]["sha256"] = sha256_file(chain[path_key])
        self._write_json(active_v1, v1)

        validated = pt.validate_voice_transfer_authorization(active_v1, plan, w)
        self.assertTrue(validated["request_compiled"])
        self.assertTrue(validated["provider_action_authorized"])
        self.assertFalse(validated["network_authorized"])

    def test_g1_preflight_failures_do_not_consume_or_access_credentials(self) -> None:
        cases = ("draft", "quota_mismatch", "adc_missing", "existing_output", "symlink_parent", "expired")
        for case in cases:
            with self.subTest(case=case):
                temporary, fixture, plan, w = self._copy_system()
                self.addCleanup(temporary.cleanup)
                quota_project = "oe-test-quota-project"
                if case == "draft":
                    self._refresh_draft_hashes(fixture, plan, w)
                    active = fixture / "authorizations" / "01-google-synthetic-guide.DRAFT.json"
                else:
                    active = self._activate_executable_guide(
                        fixture,
                        plan,
                        w,
                        quota_project=quota_project,
                    )
                paths = self._execution_artifacts(fixture)
                if case == "existing_output":
                    paths["a"].parent.mkdir(parents=True)
                    paths["a"].write_bytes(b"collision")
                elif case == "symlink_parent":
                    outside = Path(temporary.name) / "outside-output"
                    outside.mkdir()
                    (fixture / "outputs").symlink_to(outside, target_is_directory=True)
                elif case == "expired":
                    value = json.loads(active.read_text(encoding="utf-8"))
                    value["approved_at"] = (datetime.now(timezone.utc) - timedelta(hours=2)).isoformat()
                    value["expires_at"] = (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat()
                    self._write_json(active, value)

                adc = mock.Mock(
                    side_effect=(
                        ValidationError("gcloud is unavailable for the authorized ADC credential mechanism")
                        if case == "adc_missing"
                        else None
                    ),
                    return_value="/test/gcloud",
                )
                token_loader = mock.Mock(return_value="ya29.private-test-access-token")
                provider = mock.Mock()
                supplied_project = "wrong-project" if case == "quota_mismatch" else quota_project
                with mock.patch.dict(
                    os.environ,
                    {pt.GUIDE_QUOTA_PROJECT_ENV: supplied_project},
                    clear=True,
                ), mock.patch.object(pt, "_preflight_google_adc", adc), mock.patch.object(
                    pt, "_load_google_access_token", token_loader
                ), mock.patch.object(pt, "_open_google_request", provider):
                    with self.assertRaises(ValidationError):
                        pt.execute_synthetic_guide(active, plan, w)
                self.assertFalse(paths["consumption"].exists())
                self.assertFalse(paths["success"].exists())
                self.assertFalse(paths["failure"].exists())
                token_loader.assert_not_called()
                provider.assert_not_called()
                if case in {"draft", "quota_mismatch", "existing_output", "symlink_parent", "expired"}:
                    adc.assert_not_called()

    def test_gcloud_token_refresh_uses_minimal_environment_and_rejects_malformed_output(self) -> None:
        access_token = "ya29.private-test-access-token"
        completed = SimpleNamespace(returncode=0, stdout=(access_token + "\n").encode(), stderr=b"ignored")
        with mock.patch.dict(
            os.environ,
            {
                "PATH": "/safe/bin",
                "HOME": "/safe/home",
                "LANG": "C",
                "CLOUDSDK_CONFIG": "/safe/config",
                "ELEVENLABS_API_KEY": "xi-secret-not-for-google",
                "GOOGLE_CLOUD_QUOTA_PROJECT": "raw-project-not-for-subprocess",
                "GOOGLE_APPLICATION_CREDENTIALS": "/secret/other-provider.json",
            },
            clear=True,
        ), mock.patch.object(pt.subprocess, "run", return_value=completed) as runner:
            self.assertEqual(pt._load_google_access_token("/safe/bin/gcloud", 30), access_token)
        args, kwargs = runner.call_args
        self.assertEqual(
            args[0],
            [
                "/safe/bin/gcloud",
                "auth",
                "application-default",
                "print-access-token",
                "--quiet",
            ],
        )
        self.assertFalse(any(argument.startswith("--scopes=") for argument in args[0]))
        self.assertFalse(kwargs["text"])
        self.assertEqual(kwargs["timeout"], 30)
        self.assertNotIn("ELEVENLABS_API_KEY", kwargs["env"])
        self.assertNotIn("GOOGLE_CLOUD_QUOTA_PROJECT", kwargs["env"])
        self.assertNotIn("GOOGLE_APPLICATION_CREDENTIALS", kwargs["env"])

        for stdout in (b"", b"short", b"token with whitespace", b"\xff" * 32):
            with self.subTest(stdout=stdout[:8]):
                malformed = SimpleNamespace(returncode=0, stdout=stdout, stderr=b"private provider detail")
                with mock.patch.object(pt.subprocess, "run", return_value=malformed):
                    raised, locals_at_failure = self._capture_failure(
                        lambda: pt._load_google_access_token("/safe/bin/gcloud", 30),
                        pt._GuideExecutionFailure,
                        "_load_google_access_token",
                    )
                self.assertEqual(raised.code, "google_adc_access_token_malformed")
                self.assertIsNone(locals_at_failure["result"])
                self.assertEqual(locals_at_failure["raw"], b"")
                self.assertEqual(locals_at_failure["stripped"], b"")
                self.assertIsNone(locals_at_failure["token"])

        failed_refresh = SimpleNamespace(
            returncode=1,
            stdout=b"ya29.private-failed-refresh-token",
            stderr=b"oe-private-failed-refresh-project",
        )
        with mock.patch.object(pt.subprocess, "run", return_value=failed_refresh):
            raised, refresh_locals = self._capture_failure(
                lambda: pt._load_google_access_token("/safe/bin/gcloud", 30),
                pt._GuideExecutionFailure,
                "_load_google_access_token",
            )
        self.assertEqual(raised.code, "google_adc_token_refresh_failed")
        self.assertIsNone(refresh_locals["result"])
        self.assertEqual(refresh_locals["raw"], b"")
        self.assertEqual(refresh_locals["stripped"], b"")
        self.assertIsNone(refresh_locals["token"])

        private_timeout = pt.subprocess.TimeoutExpired(
            cmd=["gcloud"],
            timeout=30,
            output=b"ya29.private-timeout-token",
            stderr=b"oe-private-quota-project",
        )
        with mock.patch.object(pt.subprocess, "run", side_effect=private_timeout):
            raised, timeout_locals = self._capture_failure(
                lambda: pt._load_google_access_token("/safe/bin/gcloud", 30),
                pt._GuideExecutionFailure,
                "_load_google_access_token",
            )
        self.assertIsNone(raised.__cause__)
        self.assertIsNone(raised.__context__)
        self.assertIsNone(timeout_locals["result"])
        self.assertEqual(timeout_locals["raw"], b"")
        self.assertEqual(timeout_locals["stripped"], b"")
        self.assertIsNone(timeout_locals["token"])

    def test_gcloud_adc_preflight_rejects_symlink_components(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        base = Path(temporary.name).resolve()
        real = base / "real-config"
        real.mkdir()
        self._write_json(real / "application_default_credentials.json", {"type": "authorized_user"})
        linked = base / "linked-config"
        linked.symlink_to(real, target_is_directory=True)
        with mock.patch.dict(os.environ, {"CLOUDSDK_CONFIG": str(linked)}, clear=True), mock.patch.object(
            pt.shutil, "which", return_value="/test/gcloud"
        ):
            with self.assertRaisesRegex(ValidationError, "unavailable or unsafe"):
                pt._preflight_google_adc()

        with mock.patch.dict(os.environ, {"CLOUDSDK_CONFIG": str(real)}, clear=True), mock.patch.object(
            pt.shutil, "which", return_value="/test/gcloud"
        ):
            self.assertEqual(pt._preflight_google_adc(), "/test/gcloud")

    def test_gcloud_adc_descriptor_walk_rejects_parent_swap_race(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        base = Path(temporary.name).resolve()
        config = base / "config"
        outside = base / "outside"
        config.mkdir()
        outside.mkdir()
        self._write_json(config / "application_default_credentials.json", {"type": "authorized_user"})
        self._write_json(outside / "application_default_credentials.json", {"type": "authorized_user"})
        moved = base / "moved-original"
        original_open = pt.os.open
        swapped = False

        def racing_open(path, flags, mode=0o777, *, dir_fd=None):
            nonlocal swapped
            if path == "application_default_credentials.json" and dir_fd is not None and not swapped:
                swapped = True
                config.rename(moved)
                config.symlink_to(outside, target_is_directory=True)
            return original_open(path, flags, mode, dir_fd=dir_fd)

        with mock.patch.dict(os.environ, {"CLOUDSDK_CONFIG": str(config)}, clear=True), mock.patch.object(
            pt.shutil, "which", return_value="/test/gcloud"
        ), mock.patch.object(pt.os, "open", side_effect=racing_open):
            with self.assertRaises(ValidationError):
                pt._preflight_google_adc()
        self.assertTrue(swapped)

    def test_gcloud_adc_parse_failure_scrubs_private_material_from_traceback(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        config = Path(temporary.name).resolve() / "private-adc-config"
        config.mkdir()
        adc_secret = "private-adc-client-secret"
        adc_path = config / "application_default_credentials.json"
        self._write_json(
            adc_path,
            {
                "type": "unsupported_private_credential",
                "client_id": "private-client-id",
                "client_secret": adc_secret,
            },
        )
        with mock.patch.dict(os.environ, {"CLOUDSDK_CONFIG": str(config)}, clear=True), mock.patch.object(
            pt.shutil,
            "which",
            return_value="/test/gcloud",
        ):
            raised, adc_locals = self._capture_failure(
                pt._preflight_google_adc,
                ValidationError,
                "_preflight_google_adc",
            )
        self.assertIsNone(raised.__cause__)
        self.assertIsNone(raised.__context__)
        self.assertIsNone(adc_locals["config_value"])
        self.assertIsNone(adc_locals["config_root"])
        self.assertEqual(adc_locals["config_parts"], ())
        self.assertEqual(adc_locals["data"], b"")
        self.assertEqual(adc_locals["chunk"], b"")
        self.assertEqual(adc_locals["chunks"], [])
        self.assertIsNone(adc_locals["value"])
        self.assertIsNone(adc_locals["credential_type"])
        self.assertNotIn(adc_secret, repr(adc_locals))

    def test_private_preconsumption_failures_scrub_quota_project_from_traceback(self) -> None:
        for case in ("quota_mismatch", "adc_failure"):
            with self.subTest(case=case):
                temporary, fixture, plan, w = self._copy_system()
                self.addCleanup(temporary.cleanup)
                authorized_project = "oe-private-authorized-project"
                supplied_project = (
                    "oe-private-mismatched-project"
                    if case == "quota_mismatch"
                    else authorized_project
                )
                active = self._activate_executable_guide(
                    fixture,
                    plan,
                    w,
                    quota_project=authorized_project,
                )
                paths = self._execution_artifacts(fixture)
                adc = mock.Mock(
                    side_effect=(
                        ValidationError("private ADC detail must not escape")
                        if case == "adc_failure"
                        else None
                    ),
                    return_value="/test/gcloud",
                )
                with mock.patch.dict(
                    os.environ,
                    {pt.GUIDE_QUOTA_PROJECT_ENV: supplied_project},
                    clear=True,
                ), mock.patch.object(pt, "_preflight_google_adc", adc):
                    raised, execution_locals = self._capture_failure(
                        lambda: pt.execute_synthetic_guide(active, plan, w),
                        ValidationError,
                        "execute_synthetic_guide",
                    )
                self.assertEqual(execution_locals["quota_project"], "")
                self.assertEqual(execution_locals["gcloud_executable"], "")
                self.assertIsNone(execution_locals["contract"])
                self.assertNotIn(supplied_project, repr(execution_locals))
                self.assertFalse(paths["consumption"].exists())
                if case == "quota_mismatch":
                    adc.assert_not_called()

    def test_malformed_token_consumes_once_but_never_calls_provider(self) -> None:
        temporary, fixture, plan, w = self._copy_system()
        self.addCleanup(temporary.cleanup)
        quota_project = "oe-test-quota-project"
        active = self._activate_executable_guide(fixture, plan, w, quota_project=quota_project)
        paths = self._execution_artifacts(fixture)

        def malformed_after_consumption(executable: str, timeout: float) -> str:
            self.assertTrue(paths["consumption"].is_file())
            raise pt._GuideExecutionFailure("google_adc_access_token_malformed")

        provider = mock.Mock()
        with mock.patch.dict(os.environ, {pt.GUIDE_QUOTA_PROJECT_ENV: quota_project}, clear=True), mock.patch.object(
            pt, "_preflight_google_adc", return_value="/test/gcloud"
        ), mock.patch.object(pt, "_load_google_access_token", side_effect=malformed_after_consumption), mock.patch.object(
            pt, "_open_google_request", provider
        ):
            raised, execution_locals = self._capture_failure(
                lambda: pt.execute_synthetic_guide(active, plan, w),
                ValidationError,
                "execute_synthetic_guide",
            )
        self.assertIn("google_adc_access_token_malformed", str(raised))
        self.assertEqual(execution_locals["quota_project"], "")
        self.assertEqual(execution_locals["access_token"], "")
        self.assertIsNone(execution_locals["contract"])
        provider.assert_not_called()
        self.assertTrue(paths["consumption"].is_file())
        self.assertTrue(paths["failure"].is_file())
        self.assertFalse(paths["a"].exists())
        receipt = json.loads(paths["failure"].read_text(encoding="utf-8"))
        self.assertEqual(receipt["provider_calls_made"], 0)
        self.assertTrue(receipt["network_called"])
        self.assertTrue(receipt["credential_refresh_attempted"])

    def test_provider_failures_never_retry_and_partial_a_is_preserved(self) -> None:
        for failure_on_call, status in ((1, 302), (1, 408), (1, 429), (1, 500), (2, 503)):
            with self.subTest(failure_on_call=failure_on_call, status=status):
                temporary, fixture, plan, w = self._copy_system()
                self.addCleanup(temporary.cleanup)
                quota_project = "oe-test-quota-project"
                access_token = "ya29.private-test-access-token"
                active = self._activate_executable_guide(fixture, plan, w, quota_project=quota_project)
                paths = self._execution_artifacts(fixture)
                response_body = self._google_json_response()
                calls = 0

                def open_once(request, timeout: float):
                    nonlocal calls
                    calls += 1
                    self.assertTrue(paths["consumption"].is_file())
                    if calls == failure_on_call:
                        raise urllib.error.HTTPError(
                            pt.GUIDE_ENDPOINT,
                            status,
                            "private provider error",
                            {"X-Goog-Request-Id": "safe-failure-id"},
                            io.BytesIO(b"raw provider body ya29.private-test-access-token oe-test-quota-project"),
                        )
                    return _FakeGoogleResponse(response_body)

                with mock.patch.dict(os.environ, {pt.GUIDE_QUOTA_PROJECT_ENV: quota_project}, clear=True), mock.patch.object(
                    pt, "_preflight_google_adc", return_value="/test/gcloud"
                ), mock.patch.object(pt, "_load_google_access_token", return_value=access_token), mock.patch.object(
                    pt, "_open_google_request", side_effect=open_once
                ):
                    raised, execution_locals = self._capture_failure(
                        lambda: pt.execute_synthetic_guide(active, plan, w),
                        ValidationError,
                        "execute_synthetic_guide",
                    )
                self.assertEqual(execution_locals["quota_project"], "")
                self.assertEqual(execution_locals["access_token"], "")
                self.assertEqual(execution_locals["body"], b"")
                self.assertIsNone(execution_locals["response"])
                self.assertIsNone(execution_locals["contract"])
                self.assertNotIn(access_token, repr(execution_locals))
                self.assertNotIn(quota_project, repr(execution_locals))
                self.assertEqual(calls, failure_on_call)
                self.assertTrue(paths["failure"].is_file())
                self.assertFalse(paths["success"].exists())
                self.assertEqual(paths["a"].exists(), failure_on_call == 2)
                self.assertFalse(paths["b"].exists())
                failure_bytes = paths["failure"].read_bytes()
                self.assertNotIn(access_token.encode(), failure_bytes)
                self.assertNotIn(quota_project.encode(), failure_bytes)
                receipt = json.loads(failure_bytes)
                self.assertEqual(receipt["provider_calls_made"], failure_on_call)
                self.assertEqual(receipt["retries_made"], 0)
                self.assertEqual(receipt["redirects_followed"], 0)
                self.assertEqual(receipt["fallbacks_used"], 0)

    def test_provider_exception_chain_does_not_retain_error_body_or_headers(self) -> None:
        raw_token = "ya29.private-provider-token"
        raw_project = "oe-private-provider-project"
        provider_error = urllib.error.HTTPError(
            pt.GUIDE_ENDPOINT,
            500,
            "private provider error",
            {"X-Goog-Request-Id": raw_token},
            io.BytesIO(f"{raw_token}:{raw_project}".encode()),
        )
        with mock.patch.object(pt, "_open_google_request", side_effect=provider_error):
            raised, provider_locals = self._capture_failure(
                lambda: pt._perform_google_post(
                    pt._compact_json_bytes(pt._guide_body(pt.MICROTEST_TEXT)),
                    raw_token,
                    raw_project,
                    30,
                ),
                pt._GuideExecutionFailure,
                "_perform_google_post",
            )
        self.assertIsNone(raised.__cause__)
        self.assertIsNone(raised.__context__)
        self.assertEqual(raised.provider_identifiers, {})
        self.assertEqual(provider_locals["access_token"], "")
        self.assertEqual(provider_locals["quota_project"], "")
        self.assertEqual(provider_locals["body"], b"")
        self.assertIsNone(provider_locals["request"])
        self.assertIsNone(provider_locals["response"])
        self.assertIsNone(provider_locals["status_getter"])
        self.assertIsNone(provider_locals["final_url_getter"])
        self.assertIsNone(provider_locals["close"])
        self.assertEqual(provider_locals["headers"], {})
        self.assertEqual(provider_locals["chunks"], [])
        self.assertEqual(provider_locals["chunk"], b"")
        self.assertEqual(provider_locals["raw"], b"")
        self.assertIsNone(provider_locals["payload"])
        self.assertEqual(provider_locals["encoded"], b"")
        self.assertEqual(provider_locals["wav_bytes"], b"")
        self.assertIsNone(provider_locals["geometry"])
        self.assertNotIn(raw_token, repr(provider_locals))
        self.assertNotIn(raw_project, repr(provider_locals))

        response_secret = "ya29.private-response-alias-secret"
        response = _FakeGoogleResponse(response_secret.encode())
        response.private_attribute = response_secret
        with mock.patch.object(pt, "_open_google_request", return_value=response):
            raised, alias_locals = self._capture_failure(
                lambda: pt._perform_google_post(
                    pt._compact_json_bytes(pt._guide_body(pt.MICROTEST_TEXT)),
                    raw_token,
                    raw_project,
                    30,
                ),
                pt._GuideExecutionFailure,
                "_perform_google_post",
            )
        self.assertIsNone(alias_locals["response"])
        self.assertIsNone(alias_locals["status_getter"])
        self.assertIsNone(alias_locals["final_url_getter"])
        self.assertIsNone(alias_locals["close"])
        self.assertEqual(alias_locals["chunk"], b"")
        self.assertEqual(alias_locals["raw"], b"")
        self.assertNotIn(response_secret, repr(alias_locals))

    def test_google_response_decoder_fails_closed_on_adversarial_payloads(self) -> None:
        valid_wav = self._wav_bytes()
        encoded = base64.b64encode(valid_wav).decode("ascii")
        cases: list[tuple[str, _FakeGoogleResponse]] = [
            (
                "oversize_response",
                _FakeGoogleResponse(b"", declared_length=pt.GUIDE_MAX_RESPONSE_BYTES_PER_CALL + 1),
            ),
            ("malformed_json", _FakeGoogleResponse(b"{")),
            (
                "duplicate_audio",
                _FakeGoogleResponse(
                    (f'{{"audioContent":"{encoded}","audioContent":"{encoded}"}}').encode()
                ),
            ),
            (
                "extra_audio_member",
                _FakeGoogleResponse(self._google_json_response(valid_wav, extra={"usage": 1})),
            ),
            ("invalid_base64", _FakeGoogleResponse(b'{"audioContent":"%%%%"}')),
            (
                "wrong_mime",
                _FakeGoogleResponse(self._google_json_response(valid_wav), content_type="audio/wav"),
            ),
            (
                "final_url_changed",
                _FakeGoogleResponse(
                    self._google_json_response(valid_wav),
                    url="https://example.invalid/redirected",
                ),
            ),
            (
                "forbidden_content_encoding",
                _FakeGoogleResponse(
                    self._google_json_response(valid_wav),
                    extra_headers={"Content-Encoding": "gzip"},
                ),
            ),
            (
                "declared_length_mismatch",
                _FakeGoogleResponse(
                    self._google_json_response(valid_wav),
                    declared_length=len(self._google_json_response(valid_wav)) + 1,
                ),
            ),
            (
                "truncated_wav",
                _FakeGoogleResponse(self._google_json_response(valid_wav[:44])),
            ),
            (
                "trailing_wav_bytes",
                _FakeGoogleResponse(self._google_json_response(valid_wav + b"trailing")),
            ),
            (
                "wrong_rate",
                _FakeGoogleResponse(self._google_json_response(self._wav_bytes(sample_rate=22050))),
            ),
            (
                "wrong_channels",
                _FakeGoogleResponse(self._google_json_response(self._wav_bytes(channels=2))),
            ),
            (
                "wrong_sample_width",
                _FakeGoogleResponse(self._google_json_response(self._wav_bytes(sample_width=1))),
            ),
            (
                "too_short",
                _FakeGoogleResponse(self._google_json_response(self._wav_bytes(19.999))),
            ),
            (
                "too_long",
                _FakeGoogleResponse(self._google_json_response(self._wav_bytes(50.001))),
            ),
            (
                "decoded_wav_oversize",
                _FakeGoogleResponse(
                    json.dumps(
                        {
                            "audioContent": base64.b64encode(
                                b"R" * (pt.GUIDE_MAX_OUTPUT_WAV_BYTES + 1)
                            ).decode("ascii")
                        },
                        separators=(",", ":"),
                    ).encode()
                ),
            ),
        ]
        for name, response in cases:
            with self.subTest(case=name):
                opened = mock.Mock(return_value=response)
                with mock.patch.object(pt, "_open_google_request", opened):
                    with self.assertRaises(pt._GuideExecutionFailure):
                        pt._perform_google_post(
                            pt._compact_json_bytes(pt._guide_body(pt.MICROTEST_TEXT)),
                            "ya29.private-test-access-token",
                            "oe-test-quota-project",
                            30,
                        )
                opened.assert_called_once()
                self.assertTrue(response.closed)

        for boundary in (20.0, 50.0):
            with self.subTest(accepted_boundary=boundary):
                response = _FakeGoogleResponse(
                    self._google_json_response(self._wav_bytes(boundary))
                )
                with mock.patch.object(pt, "_open_google_request", return_value=response):
                    decoded = pt._perform_google_post(
                        pt._compact_json_bytes(pt._guide_body(pt.MICROTEST_TEXT)),
                        "ya29.private-test-access-token",
                        "oe-test-quota-project",
                        30,
                    )
                self.assertEqual(decoded.geometry["duration_seconds"], boundary)

        stream_oversize = _FakeGoogleResponse(
            b"x" * (pt.GUIDE_MAX_RESPONSE_BYTES_PER_CALL + 1)
        )
        del stream_oversize.headers["Content-Length"]
        with mock.patch.object(pt, "_open_google_request", return_value=stream_oversize):
            with self.assertRaisesRegex(pt._GuideExecutionFailure, "provider_response_byte_cap_exceeded"):
                pt._perform_google_post(
                    pt._compact_json_bytes(pt._guide_body(pt.MICROTEST_TEXT)),
                    "ya29.private-test-access-token",
                    "oe-test-quota-project",
                    30,
                )

        short_chunk_response = mock.Mock()
        short_chunk_response.getcode.return_value = 200
        short_chunk_response.geturl.return_value = pt.GUIDE_ENDPOINT
        short_chunk_response.headers = {"Content-Type": "application/json"}
        short_chunk_response.read.side_effect = [
            self._google_json_response(valid_wav),
            b"forbidden-trailing-bytes",
            b"",
        ]
        with mock.patch.object(pt, "_open_google_request", return_value=short_chunk_response):
            with self.assertRaises(pt._GuideExecutionFailure):
                pt._perform_google_post(
                    pt._compact_json_bytes(pt._guide_body(pt.MICROTEST_TEXT)),
                    "ya29.private-test-access-token",
                    "oe-test-quota-project",
                    30,
                )
        self.assertGreaterEqual(short_chunk_response.read.call_count, 2)

        class DuplicateHeaders:
            @staticmethod
            def items():
                return [
                    ("Content-Type", "application/json"),
                    ("Content-Length", "1"),
                    ("Content-Length", "2"),
                ]

        duplicate_header_response = mock.Mock()
        duplicate_header_response.getcode.return_value = 200
        duplicate_header_response.geturl.return_value = pt.GUIDE_ENDPOINT
        duplicate_header_response.headers = DuplicateHeaders()
        with mock.patch.object(pt, "_open_google_request", return_value=duplicate_header_response):
            with self.assertRaisesRegex(pt._GuideExecutionFailure, "provider_response_headers_duplicated"):
                pt._perform_google_post(
                    pt._compact_json_bytes(pt._guide_body(pt.MICROTEST_TEXT)),
                    "ya29.private-test-access-token",
                    "oe-test-quota-project",
                    30,
                )
        duplicate_header_response.read.assert_not_called()

    def test_partial_failure_counts_each_response_exactly_once(self) -> None:
        temporary, fixture, plan, w = self._copy_system()
        self.addCleanup(temporary.cleanup)
        quota_project = "oe-test-quota-project"
        active = self._activate_executable_guide(fixture, plan, w, quota_project=quota_project)
        paths = self._execution_artifacts(fixture)
        first_body = self._google_json_response()
        responses = [
            _FakeGoogleResponse(first_body),
            _FakeGoogleResponse(b"{"),
        ]
        with mock.patch.dict(os.environ, {pt.GUIDE_QUOTA_PROJECT_ENV: quota_project}, clear=True), mock.patch.object(
            pt, "_preflight_google_adc", return_value="/test/gcloud"
        ), mock.patch.object(pt, "_load_google_access_token", return_value="ya29.private-test-access-token"), mock.patch.object(
            pt, "_open_google_request", side_effect=responses
        ):
            with self.assertRaises(ValidationError):
                pt.execute_synthetic_guide(active, plan, w)
        receipt = json.loads(paths["failure"].read_text(encoding="utf-8"))
        self.assertEqual(receipt["provider_calls_made"], 2)
        self.assertEqual(receipt["provider_response_bytes_total"], len(first_body) + 1)
        self.assertEqual(receipt["failed_response_bytes"], 1)
        self.assertTrue(paths["a"].exists())
        self.assertFalse(paths["b"].exists())

    def test_g1_path_races_fail_after_consumption_without_provider_retry(self) -> None:
        for race_stage in ("after_token", "after_response"):
            with self.subTest(race_stage=race_stage):
                temporary, fixture, plan, w = self._copy_system()
                self.addCleanup(temporary.cleanup)
                quota_project = "oe-test-quota-project"
                active = self._activate_executable_guide(fixture, plan, w, quota_project=quota_project)
                paths = self._execution_artifacts(fixture)
                outside = Path(temporary.name) / "outside-race.wav"
                outside.write_bytes(b"outside")
                provider_calls = 0

                def token_loader(executable: str, timeout: float) -> str:
                    self.assertTrue(paths["consumption"].exists())
                    if race_stage == "after_token":
                        paths["a"].symlink_to(outside)
                    return "ya29.private-test-access-token"

                def provider(request, timeout: float):
                    nonlocal provider_calls
                    provider_calls += 1
                    if race_stage == "after_response":
                        paths["a"].symlink_to(outside)
                    return _FakeGoogleResponse(self._google_json_response())

                with mock.patch.dict(os.environ, {pt.GUIDE_QUOTA_PROJECT_ENV: quota_project}, clear=True), mock.patch.object(
                    pt, "_preflight_google_adc", return_value="/test/gcloud"
                ), mock.patch.object(pt, "_load_google_access_token", side_effect=token_loader), mock.patch.object(
                    pt, "_open_google_request", side_effect=provider
                ):
                    with self.assertRaises(ValidationError):
                        pt.execute_synthetic_guide(active, plan, w)
                self.assertTrue(paths["consumption"].exists())
                self.assertTrue(paths["failure"].exists())
                self.assertEqual(provider_calls, 0 if race_stage == "after_token" else 1)
                self.assertTrue(paths["a"].is_symlink())
                self.assertEqual(outside.read_bytes(), b"outside")

    def test_consumption_latch_tamper_stops_before_the_next_network_action(self) -> None:
        for tamper_stage in ("after_consume", "after_a"):
            with self.subTest(tamper_stage=tamper_stage):
                temporary, fixture, plan, w = self._copy_system()
                self.addCleanup(temporary.cleanup)
                quota_project = "oe-test-quota-project"
                active = self._activate_executable_guide(fixture, plan, w, quota_project=quota_project)
                paths = self._execution_artifacts(fixture)
                provider_calls = 0
                original_writer = pt._exclusive_fixture_write

                def token_loader(executable: str, timeout: float) -> str:
                    if tamper_stage == "after_consume":
                        paths["consumption"].unlink()
                    return "ya29.private-test-access-token"

                def provider(request, timeout: float):
                    nonlocal provider_calls
                    provider_calls += 1
                    return _FakeGoogleResponse(self._google_json_response())

                def writer(root: Path, relative: str, data: bytes) -> Path:
                    result = original_writer(root, relative, data)
                    if tamper_stage == "after_a" and relative == pt.GUIDE_DESTINATIONS[0]:
                        paths["consumption"].write_bytes(b"tampered-consumption")
                        paths["consumption"].chmod(0o600)
                    return result

                with mock.patch.dict(os.environ, {pt.GUIDE_QUOTA_PROJECT_ENV: quota_project}, clear=True), mock.patch.object(
                    pt, "_preflight_google_adc", return_value="/test/gcloud"
                ), mock.patch.object(pt, "_load_google_access_token", side_effect=token_loader), mock.patch.object(
                    pt, "_open_google_request", side_effect=provider
                ), mock.patch.object(pt, "_exclusive_fixture_write", side_effect=writer):
                    with self.assertRaises(ValidationError):
                        pt.execute_synthetic_guide(active, plan, w)
                self.assertEqual(provider_calls, 0 if tamper_stage == "after_consume" else 1)
                self.assertTrue(paths["failure"].exists())
                self.assertFalse(paths["b"].exists())
                if tamper_stage == "after_a":
                    self.assertTrue(paths["a"].exists())

    def test_g1_expiry_after_a_stops_before_b_and_late_response_is_ineligible(self) -> None:
        for late_stage in ("before_b", "after_a_response"):
            with self.subTest(late_stage=late_stage):
                temporary, fixture, plan, w = self._copy_system()
                self.addCleanup(temporary.cleanup)
                quota_project = "oe-test-quota-project"
                active = self._activate_executable_guide(fixture, plan, w, quota_project=quota_project)
                value = json.loads(active.read_text(encoding="utf-8"))
                base = datetime.now(timezone.utc)
                expiry = base + timedelta(minutes=5)
                value["approved_at"] = (base - timedelta(minutes=1)).isoformat()
                value["expires_at"] = expiry.isoformat()
                self._write_json(active, value)
                paths = self._execution_artifacts(fixture)
                count = 0

                def clock() -> datetime:
                    nonlocal count
                    count += 1
                    threshold = 6 if late_stage == "before_b" else 5
                    return base if count <= threshold else expiry + timedelta(seconds=1)

                provider_calls = 0

                def provider(request, timeout: float):
                    nonlocal provider_calls
                    provider_calls += 1
                    return _FakeGoogleResponse(self._google_json_response())

                with mock.patch.dict(os.environ, {pt.GUIDE_QUOTA_PROJECT_ENV: quota_project}, clear=True), mock.patch.object(
                    pt, "_preflight_google_adc", return_value="/test/gcloud"
                ), mock.patch.object(pt, "_load_google_access_token", return_value="ya29.private-test-access-token"), mock.patch.object(
                    pt, "_open_google_request", side_effect=provider
                ), mock.patch.object(pt, "_execution_now", side_effect=clock):
                    with self.assertRaises(ValidationError):
                        pt.execute_synthetic_guide(active, plan, w)
                self.assertTrue(paths["failure"].exists())
                self.assertFalse(paths["b"].exists())
                if late_stage == "before_b":
                    self.assertEqual(provider_calls, 1)
                    self.assertTrue(paths["a"].exists())
                else:
                    self.assertEqual(provider_calls, 1)
                    self.assertFalse(paths["a"].exists())

    def test_authorizations_reject_bool_numeric_coercion(self) -> None:
        temporary, fixture, plan, w = self._copy_system()
        self.addCleanup(temporary.cleanup)
        guide = self._activate_guide(fixture, plan, w)
        document = json.loads(guide.read_text(encoding="utf-8"))
        document["action"]["no_retry"] = 1
        self._write_json(guide, document)
        with self.assertRaises(ValidationError):
            pt.validate_synthetic_guide_authorization(guide, plan, w)

        temporary2, fixture2, plan2, w2 = self._copy_system()
        self.addCleanup(temporary2.cleanup)
        transfer, _paths = self._activate_transfer(fixture2, plan2, w2)
        document2 = json.loads(transfer.read_text(encoding="utf-8"))
        document2["action"]["remove_background_noise"] = 0
        document2["authorized_limits"]["max_outputs"] = True
        self._write_json(transfer, document2)
        with self.assertRaises(ValidationError):
            pt.validate_voice_transfer_authorization(transfer, plan2, w2)

    def test_authority_document_rejects_symlinked_parent_and_foreign_fixture(self) -> None:
        temporary, fixture, plan, w = self._copy_system()
        self.addCleanup(temporary.cleanup)
        active = self._activate_guide(fixture, plan, w)
        authorization_dir = fixture / "authorizations"
        outside = Path(temporary.name) / "outside-authorizations"
        authorization_dir.rename(outside)
        authorization_dir.symlink_to(outside, target_is_directory=True)
        with self.assertRaises(ValidationError):
            pt.validate_synthetic_guide_authorization(active, plan, w)
        from oe_narration.cli import build_parser

        parsed = build_parser().parse_args(
            [
                "synthetic-guide",
                "--plan", str(plan),
                "--canonical-w", str(w),
                "--authorization", str(active),
            ]
        )
        self.assertEqual(parsed.authorization, active.absolute())
        self.assertNotEqual(parsed.authorization, active.resolve())

        temporary2, fixture2, plan2, w2 = self._copy_system()
        temporary3, fixture3, plan3, w3 = self._copy_system()
        self.addCleanup(temporary2.cleanup)
        self.addCleanup(temporary3.cleanup)
        foreign_guide = self._activate_guide(fixture2, plan2, w2)
        with self.assertRaisesRegex(ValidationError, "exact plan fixture root"):
            pt.validate_synthetic_guide_authorization(foreign_guide, plan3, w3)

        foreign_transfer, _foreign_paths = self._activate_transfer(fixture2, plan2, w2)
        with self.assertRaisesRegex(ValidationError, "exact plan fixture root"):
            pt.validate_voice_transfer_authorization(foreign_transfer, plan3, w3)

    def test_unconsumed_authority_rejects_traversal_and_existing_record(self) -> None:
        for mutation in ("traversal", "collision"):
            with self.subTest(mutation=mutation):
                temporary, fixture, plan, w = self._copy_system()
                self.addCleanup(temporary.cleanup)
                active = self._activate_guide(fixture, plan, w)
                auth = json.loads(active.read_text(encoding="utf-8"))
                if mutation == "traversal":
                    auth["consumption"]["record_path"] = "../../outside/consumed.json"
                else:
                    collision = fixture / auth["consumption"]["record_path"]
                    self._write_json(collision, {"already": "exists"})
                self._write_json(active, auth)
                with self.assertRaises(ValidationError):
                    pt.validate_synthetic_guide_authorization(active, plan, w)

    def test_active_guide_rejects_expiry_quota_hash_and_request_tamper(self) -> None:
        for mutation in ("expiry", "quota", "request"):
            with self.subTest(mutation=mutation):
                temporary, fixture, plan, w = self._copy_system()
                self.addCleanup(temporary.cleanup)
                active = self._activate_guide(fixture, plan, w)
                auth = json.loads(active.read_text(encoding="utf-8"))
                if mutation == "expiry":
                    auth["expires_at"] = (datetime.now(timezone.utc) - timedelta(seconds=1)).isoformat()
                elif mutation == "quota":
                    auth["billing_project_binding"]["quota_project_sha256"] = "pending"
                else:
                    auth["bindings"]["request_body_sha256"] = "0" * 64
                self._write_json(active, auth)
                with self.assertRaises(ValidationError):
                    pt.validate_synthetic_guide_authorization(active, plan, w)

    def test_voice_transfer_draft_cannot_select_or_compile_a_request(self) -> None:
        temporary, fixture, plan, w = self._copy_system()
        self.addCleanup(temporary.cleanup)
        self._refresh_draft_hashes(fixture, plan, w)
        auth = fixture / "authorizations" / "02-elevenlabs-saved-c-transfer.DRAFT.json"
        result = pt.validate_voice_transfer_authorization(auth, plan, w)
        self.assertEqual(result["status"], "blocked_pending_exact_selected_guide_chain")
        self.assertFalse(result["request_compiled"])
        self.assertFalse(result["network_authorized"])

    def test_active_transfer_compiles_exact_original_24k_guide_without_network(self) -> None:
        temporary, fixture, plan, w = self._copy_system()
        self.addCleanup(temporary.cleanup)
        active, paths = self._activate_transfer(fixture, plan, w)
        result = pt.validate_voice_transfer_authorization(active, plan, w)
        primary = result["primary_request"]
        self.assertTrue(result["provider_action_authorized"])
        self.assertFalse(result["network_authorized"])
        self.assertFalse(result["execution_transport_available"])
        self.assertEqual(primary["query"]["enable_logging"], "true")
        self.assertEqual(primary["source_audio_sha256"], sha256_file(paths["guide"]))
        self.assertGreater(primary["multipart_body_bytes"], paths["guide"].stat().st_size)
        self.assertEqual(primary["fields"]["model_id"], pt.TRANSFER_MODEL)
        self.assertFalse(result["conditional_fallback_request"]["enabled"])
        self.assertEqual(result["maximum"]["max_source_duration_seconds"], 50)
        self.assertEqual(result["maximum"]["max_submitted_seconds"], 100)
        self.assertFalse(result["full_capture_authorized"])
        self.assertFalse(result["step3_authorized"])

    def test_zrm_forces_enable_logging_false(self) -> None:
        temporary, fixture, plan, w = self._copy_system()
        self.addCleanup(temporary.cleanup)
        active, _paths = self._activate_transfer(fixture, plan, w, zrm=True)
        result = pt.validate_voice_transfer_authorization(active, plan, w)
        self.assertEqual(result["primary_request"]["query"]["enable_logging"], "false")
        self.assertEqual(
            result["conditional_fallback_request"]["query"]["enable_logging"],
            "false",
        )

    def test_transfer_fails_closed_on_every_required_chain_gate(self) -> None:
        mutations = [
            ("qa", "lexical_exact", False),
            ("selection", "approved_for_voice_transfer", False),
            ("data", "cross_provider_upload_permitted", False),
            ("rights", "voice_changer_permitted", False),
        ]
        for artifact, key, value in mutations:
            with self.subTest(artifact=artifact, key=key):
                temporary, fixture, plan, w = self._copy_system()
                self.addCleanup(temporary.cleanup)
                active, paths = self._activate_transfer(fixture, plan, w)
                document = json.loads(paths[artifact].read_text(encoding="utf-8"))
                document[key] = value
                self._write_json(paths[artifact], document)
                auth = json.loads(active.read_text(encoding="utf-8"))
                prereq_name = {
                    "qa": "guide_qa",
                    "selection": "owner_selection",
                    "data": "elevenlabs_data_use",
                    "rights": "target_voice_rights",
                }[artifact]
                auth["prerequisites"][prereq_name]["sha256"] = sha256_file(paths[artifact])
                self._write_json(active, auth)
                with self.assertRaises(ValidationError):
                    pt.validate_voice_transfer_authorization(active, plan, w)

    def test_transfer_rejects_ambiguous_training_state_and_guide_source_swap(self) -> None:
        temporary, fixture, plan, w = self._copy_system()
        self.addCleanup(temporary.cleanup)
        active, paths = self._activate_transfer(fixture, plan, w)
        data = json.loads(paths["data"].read_text(encoding="utf-8"))
        data["improve_models_for_everyone"] = True
        data["zero_retention_mode"] = False
        self._write_json(paths["data"], data)
        auth = json.loads(active.read_text(encoding="utf-8"))
        auth["prerequisites"]["elevenlabs_data_use"]["sha256"] = sha256_file(paths["data"])
        self._write_json(active, auth)
        with self.assertRaises(ValidationError):
            pt.validate_voice_transfer_authorization(active, plan, w)

        temporary2, fixture2, plan2, w2 = self._copy_system()
        self.addCleanup(temporary2.cleanup)
        active2, paths2 = self._activate_transfer(fixture2, plan2, w2)
        with paths2["guide"].open("ab") as handle:
            handle.write(b"swap")
        with self.assertRaises(ValidationError):
            pt.validate_voice_transfer_authorization(active2, plan2, w2)

    def test_no_training_protection_must_be_processed_and_effective(self) -> None:
        for mutation, zrm in (
            ("pending_account_opt_out", False),
            ("not_effective", False),
            ("unconfirmed_zrm", True),
        ):
            with self.subTest(mutation=mutation):
                temporary, fixture, plan, w = self._copy_system()
                self.addCleanup(temporary.cleanup)
                active, paths = self._activate_transfer(fixture, plan, w, zrm=zrm)
                evidence = json.loads(paths["evidence"].read_text(encoding="utf-8"))
                data = json.loads(paths["data"].read_text(encoding="utf-8"))
                if mutation == "pending_account_opt_out":
                    evidence["opt_out_processed"] = False
                    data["opt_out_processed"] = False
                elif mutation == "not_effective":
                    evidence["protection_effective_for_new_submissions"] = False
                    data["protection_effective_for_new_submissions"] = False
                else:
                    evidence["zrm_eligible_and_confirmed"] = False
                    data["zrm_eligible_and_confirmed"] = False
                self._write_json(paths["evidence"], evidence)
                data["evidence"]["sha256"] = sha256_file(paths["evidence"])
                self._write_json(paths["data"], data)
                auth = json.loads(active.read_text(encoding="utf-8"))
                auth["prerequisites"]["elevenlabs_data_use"]["sha256"] = sha256_file(paths["data"])
                self._write_json(active, auth)
                with self.assertRaises(ValidationError):
                    pt.validate_voice_transfer_authorization(active, plan, w)

    def test_future_qa_timestamp_fails_after_hash_chain_is_refreshed(self) -> None:
        temporary, fixture, plan, w = self._copy_system()
        self.addCleanup(temporary.cleanup)
        active, paths = self._activate_transfer(fixture, plan, w)
        qa = json.loads(paths["qa"].read_text(encoding="utf-8"))
        qa["reviewed_at"] = (datetime.now(timezone.utc) + timedelta(days=30)).isoformat()
        self._write_json(paths["qa"], qa)
        selection = json.loads(paths["selection"].read_text(encoding="utf-8"))
        selection["guide_qa_sha256"] = sha256_file(paths["qa"])
        self._write_json(paths["selection"], selection)
        auth = json.loads(active.read_text(encoding="utf-8"))
        auth["prerequisites"]["guide_qa"]["sha256"] = sha256_file(paths["qa"])
        auth["prerequisites"]["owner_selection"]["sha256"] = sha256_file(paths["selection"])
        self._write_json(active, auth)
        with self.assertRaises(ValidationError):
            pt.validate_voice_transfer_authorization(active, plan, w)

    def test_selected_guide_must_use_its_compiled_destination(self) -> None:
        temporary, fixture, plan, w = self._copy_system()
        self.addCleanup(temporary.cleanup)
        active, paths = self._activate_transfer(fixture, plan, w)
        renamed = paths["guide"].with_name("not-the-compiled-destination.wav")
        paths["guide"].rename(renamed)
        receipt = json.loads(paths["receipt"].read_text(encoding="utf-8"))
        receipt["outputs"][0]["path"] = renamed.relative_to(fixture).as_posix()
        self._write_json(paths["receipt"], receipt)
        auth = json.loads(active.read_text(encoding="utf-8"))
        auth["prerequisites"]["selected_guide"]["path"] = renamed.relative_to(fixture).as_posix()
        auth["prerequisites"]["selected_guide"]["guide_run_receipt_sha256"] = sha256_file(paths["receipt"])
        self._write_json(active, auth)
        with self.assertRaises(ValidationError):
            pt.validate_voice_transfer_authorization(active, plan, w)

    def test_consumed_g1_provenance_rejects_missing_or_forged_record(self) -> None:
        for mutation in ("missing", "forged_semantics"):
            with self.subTest(mutation=mutation):
                temporary, fixture, plan, w = self._copy_system()
                self.addCleanup(temporary.cleanup)
                active, paths = self._activate_transfer(fixture, plan, w)
                receipt = json.loads(paths["receipt"].read_text(encoding="utf-8"))
                if mutation == "missing":
                    paths["guide_consumption"].unlink()
                else:
                    consumption = json.loads(paths["guide_consumption"].read_text(encoding="utf-8"))
                    consumption["consumed_before_network"] = False
                    self._write_json(paths["guide_consumption"], consumption)
                    receipt["guide_consumption_record_sha256"] = sha256_file(paths["guide_consumption"])
                    self._write_json(paths["receipt"], receipt)
                    auth = json.loads(active.read_text(encoding="utf-8"))
                    auth["prerequisites"]["selected_guide"]["guide_run_receipt_sha256"] = sha256_file(paths["receipt"])
                    self._write_json(active, auth)
                with self.assertRaises(ValidationError):
                    pt.validate_voice_transfer_authorization(active, plan, w)

    def test_guide_generation_must_finish_before_g1_expiry(self) -> None:
        temporary, fixture, plan, w = self._copy_system()
        self.addCleanup(temporary.cleanup)
        active, paths = self._activate_transfer(fixture, plan, w)
        receipt = json.loads(paths["receipt"].read_text(encoding="utf-8"))
        consumption = json.loads(paths["guide_consumption"].read_text(encoding="utf-8"))
        consumed_at = datetime.fromisoformat(consumption["consumed_at"])
        started_at = datetime.fromisoformat(receipt["started_at"])
        expiry = consumed_at + ((started_at - consumed_at) / 2)

        guide_auth = json.loads(paths["guide_auth"].read_text(encoding="utf-8"))
        guide_auth["expires_at"] = expiry.isoformat()
        self._write_json(paths["guide_auth"], guide_auth)
        consumption["authorization_sha256"] = sha256_file(paths["guide_auth"])
        self._write_json(paths["guide_consumption"], consumption)
        receipt["guide_authorization_sha256"] = sha256_file(paths["guide_auth"])
        receipt["guide_consumption_record_sha256"] = sha256_file(paths["guide_consumption"])
        self._write_json(paths["receipt"], receipt)
        authorization = json.loads(active.read_text(encoding="utf-8"))
        authorization["prerequisites"]["selected_guide"]["guide_run_receipt_sha256"] = sha256_file(paths["receipt"])
        self._write_json(active, authorization)
        with self.assertRaisesRegex(ValidationError, "inside the consumed G1 authorization window"):
            pt.validate_voice_transfer_authorization(active, plan, w)

    def test_guide_run_receipt_cannot_exceed_consumed_output_ceiling(self) -> None:
        for key, value in (
            ("duration_seconds", 50.001),
            ("byte_count", 2500001),
            ("provider_response_bytes", 4000001),
        ):
            with self.subTest(field=key):
                temporary, fixture, plan, w = self._copy_system()
                self.addCleanup(temporary.cleanup)
                active, paths = self._activate_transfer(fixture, plan, w)
                receipt = json.loads(paths["receipt"].read_text(encoding="utf-8"))
                receipt["outputs"][1][key] = value
                self._write_json(paths["receipt"], receipt)
                auth = json.loads(active.read_text(encoding="utf-8"))
                auth["prerequisites"]["selected_guide"]["guide_run_receipt_sha256"] = sha256_file(paths["receipt"])
                self._write_json(active, auth)
                with self.assertRaises(ValidationError):
                    pt.validate_voice_transfer_authorization(active, plan, w)

    def test_transfer_rejects_48k_derivative_and_symlink_input(self) -> None:
        temporary, fixture, plan, w = self._copy_system()
        self.addCleanup(temporary.cleanup)
        active, paths = self._activate_transfer(fixture, plan, w)
        with wave.open(str(paths["guide"]), "wb") as handle:
            handle.setnchannels(1)
            handle.setsampwidth(2)
            handle.setframerate(48000)
            handle.writeframes(b"\x00\x00" * 48000)
        new_sha = sha256_file(paths["guide"])
        auth = json.loads(active.read_text(encoding="utf-8"))
        auth["prerequisites"]["selected_guide"].update(
            {"sha256": new_sha, "byte_count": paths["guide"].stat().st_size}
        )
        self._write_json(active, auth)
        with self.assertRaises(ValidationError):
            pt.validate_voice_transfer_authorization(active, plan, w)

        temporary2, fixture2, plan2, w2 = self._copy_system()
        self.addCleanup(temporary2.cleanup)
        active2, paths2 = self._activate_transfer(fixture2, plan2, w2)
        real = paths2["guide"].with_name("real.wav")
        paths2["guide"].rename(real)
        paths2["guide"].symlink_to(real)
        with self.assertRaises(ValidationError):
            pt.validate_voice_transfer_authorization(active2, plan2, w2)

    def test_selected_guide_rejects_header_only_truncated_wav(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        complete = Path(temporary.name) / "complete.wav"
        with wave.open(str(complete), "wb") as handle:
            handle.setnchannels(1)
            handle.setsampwidth(2)
            handle.setframerate(24000)
            handle.writeframes(b"\x00\x00" * 24000)
        truncated = Path(temporary.name) / "truncated.wav"
        truncated.write_bytes(complete.read_bytes()[:44])
        with self.assertRaisesRegex(ValidationError, "PCM payload is truncated"):
            pt._read_bound_wav(
                truncated,
                truncated.stat().st_size,
                sha256_file(truncated),
                1.0,
            )

    def test_selected_guide_rejects_outside_exact_duration_window(self) -> None:
        for duration in (19.999, 50.001):
            with self.subTest(duration=duration):
                temporary = tempfile.TemporaryDirectory()
                self.addCleanup(temporary.cleanup)
                wav_path = Path(temporary.name) / "outside-window.wav"
                frames = round(duration * pt.GUIDE_SAMPLE_RATE_HZ)
                with wave.open(str(wav_path), "wb") as handle:
                    handle.setnchannels(1)
                    handle.setsampwidth(2)
                    handle.setframerate(pt.GUIDE_SAMPLE_RATE_HZ)
                    handle.writeframes(b"\x00\x00" * frames)
                with self.assertRaisesRegex(ValidationError, "between 20 and 50"):
                    pt._read_bound_wav(
                        wav_path,
                        wav_path.stat().st_size,
                        sha256_file(wav_path),
                        duration,
                    )

    def test_voice_transfer_rejects_multipart_boundary_collision(self) -> None:
        selected_sha = "a" * 64
        boundary = f"oe-v05-{selected_sha[:32]}".encode("ascii")
        hostile_audio = b"pcm-prefix\r\n--" + boundary + b"\r\npayload"
        with self.assertRaisesRegex(ValidationError, "multipart boundary"):
            pt._compile_multipart(
                hostile_audio,
                selected_sha,
                pt.TRANSFER_PRIMARY_FORMAT,
                enable_logging=True,
            )

    def test_transfer_rejects_multipart_action_and_limit_tamper(self) -> None:
        for mutation in ("field", "format", "limit", "fallback"):
            with self.subTest(mutation=mutation):
                temporary, fixture, plan, w = self._copy_system()
                self.addCleanup(temporary.cleanup)
                active, _paths = self._activate_transfer(fixture, plan, w)
                auth = json.loads(active.read_text(encoding="utf-8"))
                if mutation == "field":
                    auth["action"]["voice_settings"]["speed"] = 1.1
                elif mutation == "format":
                    auth["action"]["file_format"] = "wav"
                elif mutation == "limit":
                    auth["authorized_limits"]["max_calls"] = 3
                else:
                    auth["action"]["conditional_fallback_output_format"] = "mp3_44100_128"
                self._write_json(active, auth)
                with self.assertRaises(ValidationError):
                    pt.validate_voice_transfer_authorization(active, plan, w)

    def test_active_transfer_rejects_exact_body_owner_and_receipt_schema_tamper(self) -> None:
        mutations = ("request_hash", "body_hash", "owner", "run_unknown", "rights_unknown")
        for mutation in mutations:
            with self.subTest(mutation=mutation):
                temporary, fixture, plan, w = self._copy_system()
                self.addCleanup(temporary.cleanup)
                active, paths = self._activate_transfer(fixture, plan, w)
                auth = json.loads(active.read_text(encoding="utf-8"))
                if mutation == "request_hash":
                    auth["bindings"]["primary_request_sha256"] = "0" * 64
                elif mutation == "body_hash":
                    auth["bindings"]["primary_multipart_body_sha256"] = "0" * 64
                elif mutation == "owner":
                    selection = json.loads(paths["selection"].read_text(encoding="utf-8"))
                    selection["selected_by"] = "Different Owner"
                    self._write_json(paths["selection"], selection)
                    auth["prerequisites"]["owner_selection"]["sha256"] = sha256_file(paths["selection"])
                elif mutation == "run_unknown":
                    receipt = json.loads(paths["receipt"].read_text(encoding="utf-8"))
                    receipt["retry_allowed"] = True
                    self._write_json(paths["receipt"], receipt)
                    auth["prerequisites"]["selected_guide"]["guide_run_receipt_sha256"] = sha256_file(paths["receipt"])
                else:
                    rights = json.loads(paths["rights"].read_text(encoding="utf-8"))
                    rights["also_authorizes_full_capture"] = True
                    self._write_json(paths["rights"], rights)
                    auth["prerequisites"]["target_voice_rights"]["sha256"] = sha256_file(paths["rights"])
                self._write_json(active, auth)
                with self.assertRaises(ValidationError):
                    pt.validate_voice_transfer_authorization(active, plan, w)

    def test_data_use_evidence_and_original_c_provenance_are_hash_bound(self) -> None:
        for mutation in ("evidence_unknown", "provenance_hash"):
            with self.subTest(mutation=mutation):
                temporary, fixture, plan, w = self._copy_system()
                self.addCleanup(temporary.cleanup)
                active, paths = self._activate_transfer(fixture, plan, w)
                auth = json.loads(active.read_text(encoding="utf-8"))
                if mutation == "evidence_unknown":
                    evidence = json.loads(paths["evidence"].read_text(encoding="utf-8"))
                    evidence["raw_account_id"] = "forbidden"
                    self._write_json(paths["evidence"], evidence)
                    data = json.loads(paths["data"].read_text(encoding="utf-8"))
                    data["evidence"]["sha256"] = sha256_file(paths["evidence"])
                    self._write_json(paths["data"], data)
                    auth["prerequisites"]["elevenlabs_data_use"]["sha256"] = sha256_file(paths["data"])
                else:
                    rights = json.loads(paths["rights"].read_text(encoding="utf-8"))
                    rights["original_c_provenance"]["saved_voice_receipt_sha256"] = "0" * 64
                    self._write_json(paths["rights"], rights)
                    auth["prerequisites"]["target_voice_rights"]["sha256"] = sha256_file(paths["rights"])
                self._write_json(active, auth)
                with self.assertRaises(ValidationError):
                    pt.validate_voice_transfer_authorization(active, plan, w)

    def test_secret_material_and_symlink_destinations_fail_closed(self) -> None:
        temporary, fixture, plan, w = self._copy_system()
        self.addCleanup(temporary.cleanup)
        data = json.loads(plan.read_text(encoding="utf-8"))
        data["api_key"] = "AIza" + "A" * 24
        self._write_json(plan, data)
        with self.assertRaises(ValidationError):
            pt.validate_performance_transfer_plan(plan, w)

        temporary2, fixture2, plan2, w2 = self._copy_system()
        self.addCleanup(temporary2.cleanup)
        destination = fixture2 / "outputs" / "raw" / "google" / "P01-W0030-W0110" / "candidate-A.wav"
        destination.parent.mkdir(parents=True)
        destination.symlink_to(fixture2 / "performance-transfer-plan.json")
        with self.assertRaises(ValidationError):
            pt.validate_performance_transfer_plan(plan2, w2)

    def test_execute_flags_fail_before_credentials_or_side_effects(self) -> None:
        from oe_narration.cli import main

        temporary, fixture, plan, w = self._copy_system()
        self.addCleanup(temporary.cleanup)
        before = sorted(path.relative_to(fixture) for path in fixture.rglob("*"))
        with mock.patch.dict(
            os.environ,
            {"GOOGLE_APPLICATION_CREDENTIALS": "/must/not/read", "ELEVENLABS_API_KEY": "must-not-read"},
            clear=True,
        ):
            guide_rc = main(
                [
                    "synthetic-guide", "--plan", str(plan), "--canonical-w", str(w),
                    "--execute",
                ]
            )
            transfer_rc = main(
                [
                    "elevenlabs-voice-transfer", "--plan", str(plan), "--canonical-w", str(w),
                    "--execute",
                ]
            )
        after = sorted(path.relative_to(fixture) for path in fixture.rglob("*"))
        self.assertEqual(guide_rc, 2)
        self.assertEqual(transfer_rc, 2)
        self.assertEqual(before, after)

    def test_published_schemas_close_top_level_unknown_properties(self) -> None:
        schemas = self.narration_root / "schemas"
        for name in (
            "performance-transfer-plan.schema.json",
            "synthetic-guide-authorization.schema.json",
            "voice-transfer-authorization.schema.json",
        ):
            with self.subTest(name=name):
                schema = json.loads((schemas / name).read_text(encoding="utf-8"))
                self.assertFalse(schema["additionalProperties"])
                self.assertEqual(schema["$schema"], "https://json-schema.org/draft/2020-12/schema")


if __name__ == "__main__":
    unittest.main()
