from __future__ import annotations

import copy
import json
import os
import shutil
import tempfile
import unittest
import wave
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest import mock

from oe_narration.core import ValidationError, sha256_file
from oe_narration import performance_transfer as pt


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
            "outcome": "success",
            "authorization_id": "AUTH-G1-test-exact-guide",
            "request_set_sha256": dry["guide"]["request_set_sha256"],
            "request_body_sha256": pt.GUIDE_REQUEST_BODY_SHA256,
            "provider_calls_made": 2,
            "provider_spend_usd": 0.66,
            "authorization_consumed": True,
            "guide_authorization_path": guide_auth_path.relative_to(fixture).as_posix(),
            "guide_authorization_sha256": sha256_file(guide_auth_path),
            "guide_consumption_record_path": guide_consumption_path.relative_to(fixture).as_posix(),
            "guide_consumption_record_sha256": sha256_file(guide_consumption_path),
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
                    "container": "wav",
                    "codec": "pcm_s16le",
                    "sample_rate_hz": 24000,
                    "channels": 1,
                },
                {
                    "request_id": "gemini-guide-02",
                    "path": guide_b_path.relative_to(fixture).as_posix(),
                    "sha256": sha256_file(guide_b_path),
                    "byte_count": guide_b_path.stat().st_size,
                    "duration_seconds": 25.0,
                    "provider_response_bytes": 1600100,
                    "container": "wav",
                    "codec": "pcm_s16le",
                    "sample_rate_hz": 24000,
                    "channels": 1,
                },
            ],
            "full_capture_authorized": False,
            "step3_authorized": False,
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

    def test_active_guide_authority_is_exact_but_runtime_remains_offline(self) -> None:
        temporary, fixture, plan, w = self._copy_system()
        self.addCleanup(temporary.cleanup)
        active = self._activate_guide(fixture, plan, w)
        result = pt.validate_synthetic_guide_authorization(active, plan, w)
        self.assertTrue(result["provider_action_authorized"])
        self.assertFalse(result["network_authorized"])
        self.assertFalse(result["execution_transport_available"])
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
