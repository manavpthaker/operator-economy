from __future__ import annotations

import copy
import json
import shutil
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

from oe_narration.bakeoff import (
    ELEVEN_ALLOWED_TAGS,
    _compile_eleven_text,
    _compile_hume_body,
    dry_run_provider_bakeoff,
    validate_performance_envelope,
    validate_provider_action_authorization,
    validate_provider_adapter,
    validate_provider_bakeoff_plan,
)
from oe_narration.core import ValidationError, canonical_w_bytes, sha256_file


class ProviderBakeoffTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.narration_root = Path(__file__).resolve().parents[2]
        fixtures = cls.narration_root / "fixtures"
        matches = sorted(fixtures.glob("step2-v0.3-*-provider-bakeoff"))
        if len(matches) != 1:
            raise AssertionError(f"expected one v0.3 provider bakeoff fixture, found {matches}")
        cls.fixture = matches[0]
        cls.base_fixture = fixtures / "step2-v0.2-ai-visibility-v1.1"
        cls.editorial_root = cls.narration_root.parent / "01-editorial"
        cls.w = cls.base_fixture / "identity" / "canonical-w.txt"
        cls.envelope = cls.fixture / "performance-envelope.json"
        cls.plan = cls.fixture / "provider-bakeoff-plan.json"
        cls.eleven_adapter = cls.fixture / "adapters" / "elevenlabs-v3.json"
        cls.hume_adapter = cls.fixture / "adapters" / "hume-octave-1.json"

    def _write_json(self, path: Path, value: dict) -> None:
        path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    def _copy_system(self) -> tuple[tempfile.TemporaryDirectory, Path, Path, Path]:
        temporary = tempfile.TemporaryDirectory()
        blueprint = Path(temporary.name) / "operator-blueprint-v2"
        copied_fixtures = blueprint / "02-narration-production" / "fixtures"
        copied_fixtures.mkdir(parents=True)
        shutil.copytree(self.fixture, copied_fixtures / self.fixture.name)
        copied_identity = copied_fixtures / self.base_fixture.name / "identity"
        copied_identity.mkdir(parents=True)
        shutil.copy2(self.w, copied_identity / self.w.name)
        source_script = (
            self.editorial_root
            / "fixtures"
            / "step1-v1.4-e2e-ai-visibility-2026-08-22"
            / "122-script-v1.1-HORIZONTAL-PITCH-CANDIDATE.md"
        )
        copied_script = (
            blueprint
            / "01-editorial"
            / "fixtures"
            / "step1-v1.4-e2e-ai-visibility-2026-08-22"
            / source_script.name
        )
        copied_script.parent.mkdir(parents=True)
        shutil.copy2(source_script, copied_script)
        fixture = copied_fixtures / self.fixture.name
        return temporary, fixture, fixture / "performance-envelope.json", copied_fixtures / self.base_fixture.name / "identity" / "canonical-w.txt"

    def _refresh_compiled_and_auth_bindings(self, fixture: Path, envelope: Path, w: Path) -> dict:
        plan = fixture / "provider-bakeoff-plan.json"
        result = dry_run_provider_bakeoff(plan, envelope, w)
        compiled = fixture / "compiled" / "provider-bakeoff-dry-run.json"
        self._write_json(compiled, result)
        plan_data = json.loads(plan.read_text(encoding="utf-8"))
        provider_hashes = {
            provider: plan_data["provider_adapters"][provider]["sha256"]
            for provider in ("elevenlabs", "hume")
        }
        for authorization_path in (fixture / "authorizations").glob("*.json"):
            authorization = json.loads(authorization_path.read_text(encoding="utf-8"))
            provider = authorization["provider"]
            authorization["bindings"]["performance_envelope_sha256"] = sha256_file(envelope)
            authorization["bindings"]["provider_adapter_sha256"] = provider_hashes[provider]
            authorization["bindings"]["provider_bakeoff_plan_sha256"] = sha256_file(plan)
            authorization["bindings"]["compiled_dry_run_sha256"] = sha256_file(compiled)
            self._write_json(authorization_path, authorization)
        return result

    def test_fixture_envelope_and_adapters_validate(self) -> None:
        envelope = validate_performance_envelope(self.envelope, self.w)
        eleven = validate_provider_adapter(self.eleven_adapter, self.envelope, self.w)
        hume = validate_provider_adapter(self.hume_adapter, self.envelope, self.w)
        plan = validate_provider_bakeoff_plan(self.plan, self.envelope, self.w)
        self.assertEqual(envelope["passage_count"], 2)
        self.assertEqual(eleven["provider"], "elevenlabs")
        self.assertEqual(hume["provider"], "hume")
        self.assertEqual(plan["candidate_count"], 8)
        self.assertFalse(plan["external_action_authorized"])

    def test_envelope_rejects_provider_fields_and_partition_drift(self) -> None:
        temporary, fixture, envelope_path, w = self._copy_system()
        self.addCleanup(temporary.cleanup)
        envelope = json.loads(envelope_path.read_text(encoding="utf-8"))
        envelope["passages"][0]["provider"] = "elevenlabs"
        envelope["passages"][0]["description"] = "synthetic actor direction"
        envelope["passages"][0]["paragraph_boundaries"][1]["start_token"] += 1
        self._write_json(envelope_path, envelope)
        with self.assertRaises(ValidationError) as caught:
            validate_performance_envelope(envelope_path, w)
        message = str(caught.exception)
        self.assertIn("provider-neutral", message)
        self.assertIn("contiguous", message)

    def test_adapter_rejects_unsupported_tags_and_description_drift(self) -> None:
        temporary, fixture, envelope, w = self._copy_system()
        self.addCleanup(temporary.cleanup)
        eleven_path = fixture / "adapters" / "elevenlabs-v3.json"
        eleven = json.loads(eleven_path.read_text(encoding="utf-8"))
        eleven["approved_tag_allowlist"][0] = "[whisper]"
        eleven["passages"][0]["tag_insertions"][0]["tag"] = "[whisper]"
        self._write_json(eleven_path, eleven)
        with self.assertRaises(ValidationError):
            validate_provider_adapter(eleven_path, envelope, w)

        hume_path = fixture / "adapters" / "hume-octave-1.json"
        hume = json.loads(hume_path.read_text(encoding="utf-8"))
        hume["passages"][0]["thought_directions"][0]["emitted_description"] += " Rewrite it."
        self._write_json(hume_path, hume)
        with self.assertRaises(ValidationError) as caught:
            validate_provider_adapter(hume_path, envelope, w)
        self.assertIn("exact approved expansion", str(caught.exception))

    def test_envelope_and_adapter_reject_unknown_material_keys(self) -> None:
        temporary, fixture, envelope_path, w = self._copy_system()
        self.addCleanup(temporary.cleanup)
        envelope = json.loads(envelope_path.read_text(encoding="utf-8"))
        envelope["external_action_authorized"] = True
        envelope["performance"]["provider_hint"] = "hume"
        envelope["passages"][0]["paragraph_boundaries"][0]["rewrite_allowed"] = True
        self._write_json(envelope_path, envelope)
        with self.assertRaises(ValidationError) as caught:
            validate_performance_envelope(envelope_path, w)
        message = str(caught.exception)
        self.assertIn("performance_envelope contains unsupported keys", message)
        self.assertIn("performance contains unsupported keys", message)
        self.assertIn("paragraph_boundaries[0] contains unsupported keys", message)

        untouched_envelope = fixture / "performance-envelope.original.json"
        shutil.copy2(self.envelope, untouched_envelope)
        adapter_path = fixture / "adapters" / "elevenlabs-v3.json"
        adapter = json.loads(adapter_path.read_text(encoding="utf-8"))
        adapter["external_action_authorized"] = True
        adapter["passages"][0]["compile_any_tag"] = True
        adapter["passages"][0]["tag_insertions"][0]["spoken"] = True
        adapter["performance_envelope"]["path"] = "../performance-envelope.original.json"
        adapter["performance_envelope"]["sha256"] = sha256_file(untouched_envelope)
        self._write_json(adapter_path, adapter)
        with self.assertRaises(ValidationError) as caught:
            validate_provider_adapter(adapter_path, untouched_envelope, w)
        message = str(caught.exception)
        self.assertIn("provider_adapter contains unsupported keys", message)
        self.assertIn("passages[0] contains unsupported keys", message)
        self.assertIn("tag_insertions[0] contains unsupported keys", message)

    def test_dry_run_preserves_paragraphs_words_and_identical_candidates(self) -> None:
        result = dry_run_provider_bakeoff(self.plan, self.envelope, self.w)
        self.assertFalse(result["network_called"])
        self.assertFalse(result["credentials_accessed"])
        self.assertEqual(result["provider_calls_made"], 0)
        self.assertEqual(result["audio_files_created"], 0)
        eleven = [request for request in result["requests"] if request["provider"] == "elevenlabs"]
        self.assertEqual(len(eleven), 4)
        for request in eleven:
            provider_text = request["request_body"]["text"]
            self.assertIn("\n\n", provider_text)
            self.assertNotEqual(" ".join(provider_text.split()), provider_text)
            stripped = provider_text
            for tag in ELEVEN_ALLOWED_TAGS:
                stripped = stripped.replace(tag, " ")
            expected = self.w.read_text(encoding="utf-8").splitlines()[
                request["start_token"] : request["end_token"]
            ]
            self.assertEqual(stripped.split(), expected)
        by_passage: dict[str, list[str]] = {}
        for request in eleven:
            by_passage.setdefault(request["passage_id"], []).append(request["request_body_sha256"])
        self.assertTrue(all(len(set(hashes)) == 1 for hashes in by_passage.values()))

    def test_hume_compilation_keeps_dialogue_and_direction_separate(self) -> None:
        result = dry_run_provider_bakeoff(self.plan, self.envelope, self.w)
        hume = [request for request in result["requests"] if request["provider"] == "hume"]
        self.assertEqual(len(hume), 2)
        canonical = self.w.read_text(encoding="utf-8").splitlines()
        for request in hume:
            self.assertEqual(request["url_path"], "/v0/tts")
            body = request["request_body"]
            self.assertEqual(body["version"], "1")
            self.assertEqual(body["format"], {"type": "wav"})
            self.assertEqual(body["num_generations"], 2)
            self.assertFalse(body["split_utterances"])
            self.assertTrue(body["strip_headers"])
            dialogue = []
            for utterance in body["utterances"]:
                self.assertEqual(set(utterance["voice"]), {"id"})
                self.assertLessEqual(len(utterance["description"]), 1000)
                self.assertNotIn(utterance["description"], utterance["text"])
                dialogue.extend(utterance["text"].split())
            self.assertEqual(dialogue, canonical[request["start_token"] : request["end_token"]])

    def test_fallback_is_precompiled_but_never_ready_and_accounted_at_maximum(self) -> None:
        result = dry_run_provider_bakeoff(self.plan, self.envelope, self.w)
        totals = result["totals"]
        self.assertEqual(totals["primary_lossless"]["planned_call_count"], 6)
        self.assertEqual(totals["primary_lossless"]["expected_output_count"], 8)
        self.assertEqual(totals["primary_lossless"]["estimated_billable_character_count"], 12818)
        maximum = totals["maximum_with_one_fallback_per_request"]
        self.assertEqual(maximum["max_call_count"], 12)
        self.assertEqual(maximum["expected_output_count"], 8)
        self.assertEqual(maximum["max_billable_character_count"], 25636)
        for request in result["requests"]:
            fallback = request["fallback_request"]
            self.assertTrue(fallback["enabled"])
            self.assertFalse(fallback["execution_ready"])
            self.assertIn("active_authorization_caps_include_fallback", fallback["requires"])
            self.assertIn("verified_actual_bitrate_at_least_192000_bps", fallback["requires"])

    def test_plan_rejects_secret_destination_escape_and_stale_adapter_hash(self) -> None:
        temporary, fixture, envelope, w = self._copy_system()
        self.addCleanup(temporary.cleanup)
        plan_path = fixture / "provider-bakeoff-plan.json"
        plan = json.loads(plan_path.read_text(encoding="utf-8"))
        plan["api_key"] = "xi-not-a-real-secret-but-forbidden"
        plan["providers"][0]["requests"][0]["destination"] = "../escape.pcm"
        plan["provider_adapters"]["elevenlabs"]["sha256"] = "0" * 64
        self._write_json(plan_path, plan)
        with self.assertRaises(ValidationError) as caught:
            validate_provider_bakeoff_plan(plan_path, envelope, w)
        message = str(caught.exception)
        self.assertIn("credentials", message)
        self.assertIn("must not be absolute", message)
        self.assertIn("sha256 mismatch", message)

    def test_plan_rejects_mutable_raw_lossy_intermediates_bad_fallback_count_and_hume_ready(self) -> None:
        temporary, fixture, envelope, w = self._copy_system()
        self.addCleanup(temporary.cleanup)
        plan_path = fixture / "provider-bakeoff-plan.json"
        plan = json.loads(plan_path.read_text(encoding="utf-8"))
        plan["providers"][0]["format_policy"]["immutable_raw"] = False
        plan["providers"][0]["format_policy"]["lossy_intermediates_after_raw"] = True
        plan["providers"][0]["format_policy"]["fallback_request_call_ceiling"] = 3
        plan["providers"][1]["execution_ready"] = True
        self._write_json(plan_path, plan)
        with self.assertRaises(ValidationError) as caught:
            validate_provider_bakeoff_plan(plan_path, envelope, w)
        message = str(caught.exception)
        self.assertIn("immutable_raw must be true", message)
        self.assertIn("lossy_intermediates_after_raw must be false", message)
        self.assertIn("one conditional fallback per primary request", message)
        self.assertIn("execution_ready must remain false", message)

    def test_provider_character_ceilings_fail_closed(self) -> None:
        tokens = ["abcdefghij"] * 501
        passage = {
            "start_token": 0,
            "end_token": len(tokens),
            "paragraph_boundaries": [
                {"start_token": 0, "end_token": len(tokens)}
            ],
            "thought_boundaries": [
                {"id": "T1", "start_token": 0, "end_token": len(tokens)}
            ],
        }
        eleven_adapter = {"tag_insertions": [{"at_token": 0, "tag": "[curious]"}]}
        with self.assertRaisesRegex(ValidationError, "5000-character"):
            _compile_eleven_text(passage, eleven_adapter, tokens)
        direction = "direction"
        hume_adapter = {
            "thought_directions": [
                {
                    "thought_id": "T1",
                    "emitted_description": direction,
                    "trailing_silence": 0.5,
                }
            ]
        }
        with self.assertRaisesRegex(ValidationError, "5000-character"):
            _compile_hume_body(passage, hume_adapter, tokens, "voice")

    def test_all_four_draft_authorizations_are_non_executable(self) -> None:
        temporary, fixture, envelope, w = self._copy_system()
        self.addCleanup(temporary.cleanup)
        self._refresh_compiled_and_auth_bindings(fixture, envelope, w)
        results = [
            validate_provider_action_authorization(path)
            for path in sorted((fixture / "authorizations").glob("*.json"))
        ]
        self.assertEqual(
            {result["scope"] for result in results},
            {
                "elevenlabs_sample_retrieval",
                "hume_clone_creation",
                "elevenlabs_calibration",
                "hume_calibration",
            },
        )
        self.assertTrue(all(result["status"] == "draft" for result in results))
        self.assertTrue(all(result["execution_ready"] is False for result in results))
        self.assertTrue(all(result["network_authorized"] is False for result in results))

        retrieval_path = fixture / "authorizations" / "01-elevenlabs-read-only-metadata-sample.DRAFT.json"
        retrieval = json.loads(retrieval_path.read_text(encoding="utf-8"))
        retrieval["action"]["rights_and_consent"] = {
            "voice_owner": "Manav",
            "provider_disclosure_approved": False,
            "record_path": "pending",
            "record_sha256": "0" * 64,
            "external_action_authorized": True,
        }
        self._write_json(retrieval_path, retrieval)
        with self.assertRaisesRegex(ValidationError, "rights_and_consent contains unsupported keys"):
            validate_provider_action_authorization(retrieval_path)

    def test_active_calibration_requires_24h_window_unconsumed_record_and_fallback_caps(self) -> None:
        temporary, fixture, envelope, w = self._copy_system()
        self.addCleanup(temporary.cleanup)
        dry_run = self._refresh_compiled_and_auth_bindings(fixture, envelope, w)
        auth_path = fixture / "authorizations" / "03-elevenlabs-calibration.DRAFT.json"
        authorization = json.loads(auth_path.read_text(encoding="utf-8"))
        now = datetime(2026, 8, 24, 16, 0, tzinfo=timezone.utc)
        authorization.update(
            {
                "status": "active",
                "approved": True,
                "execution_ready": True,
                "blockers": [],
                "approved_by": "Manav",
                "approved_at": (now - timedelta(hours=1)).isoformat(),
                "expires_at": (now + timedelta(hours=1)).isoformat(),
            }
        )
        maximum = dry_run["totals"]["by_provider"]["elevenlabs"][
            "maximum_with_one_fallback_per_request"
        ]
        authorization["authorized_limits"] = {
            "max_calls": maximum["max_call_count"],
            "max_outputs": maximum["expected_output_count"],
            "max_characters": maximum["max_billable_character_count"],
            "max_spend_usd": maximum["max_modeled_public_rate_cost_usd"],
        }
        authorization["action"].update(
            {
                "fallback_requires_capability_rejection_receipt": True,
                "fallback_requires_actual_codec_bitrate_verification": True,
            }
        )
        for key in list(authorization["consumption"]):
            if key.endswith("_used") or key.endswith("_used_usd"):
                authorization["consumption"][key] = 0
        authorization["consumption"]["status"] = "unconsumed"
        authorization["consumption"]["record_path"] = "consumed/elevenlabs-calibration.json"
        self._write_json(auth_path, authorization)
        result = validate_provider_action_authorization(auth_path, now=now)
        self.assertTrue(result["execution_ready"])
        self.assertTrue(result["consumption_record_absent"])

        underbounded = copy.deepcopy(authorization)
        underbounded["authorized_limits"]["max_characters"] //= 2
        self._write_json(auth_path, underbounded)
        with self.assertRaisesRegex(ValidationError, "fallback maximum"):
            validate_provider_action_authorization(auth_path, now=now)

        overbounded = copy.deepcopy(authorization)
        overbounded["authorized_limits"]["max_spend_usd"] += 1
        self._write_json(auth_path, overbounded)
        with self.assertRaisesRegex(ValidationError, "exactly equal"):
            validate_provider_action_authorization(auth_path, now=now)

        wrong_script = copy.deepcopy(authorization)
        wrong_script["bindings"]["script_sha256"] = "0" * 64
        self._write_json(auth_path, wrong_script)
        with self.assertRaisesRegex(ValidationError, "locked envelope script"):
            validate_provider_action_authorization(auth_path, now=now)

        wrong_fallback_count = copy.deepcopy(authorization)
        wrong_fallback_count["action"]["fallback_request_call_ceiling"] -= 1
        self._write_json(auth_path, wrong_fallback_count)
        with self.assertRaisesRegex(ValidationError, "fallback_request_call_ceiling"):
            validate_provider_action_authorization(auth_path, now=now)

        expired = copy.deepcopy(authorization)
        expired["expires_at"] = (now + timedelta(hours=25)).isoformat()
        self._write_json(auth_path, expired)
        with self.assertRaisesRegex(ValidationError, "24 hours"):
            validate_provider_action_authorization(auth_path, now=now)

        self._write_json(auth_path, authorization)
        consumed = auth_path.parent / authorization["consumption"]["record_path"]
        consumed.parent.mkdir(parents=True)
        consumed.write_text("{}\n", encoding="utf-8")
        with self.assertRaisesRegex(ValidationError, "already exists"):
            validate_provider_action_authorization(auth_path, now=now)

    def test_active_retrieval_binds_exact_endpoint_and_non_overwriting_receipts(self) -> None:
        temporary, fixture, envelope, w = self._copy_system()
        self.addCleanup(temporary.cleanup)
        self._refresh_compiled_and_auth_bindings(fixture, envelope, w)
        auth_path = fixture / "authorizations" / "01-elevenlabs-read-only-metadata-sample.DRAFT.json"
        authorization = json.loads(auth_path.read_text(encoding="utf-8"))
        now = datetime(2026, 8, 24, 16, 0, tzinfo=timezone.utc)
        voice_id = authorization["action"]["voice_id"]
        authorization.update(
            {
                "status": "active",
                "approved": True,
                "execution_ready": True,
                "blockers": [],
                "approved_by": "Manav",
                "approved_at": (now - timedelta(hours=1)).isoformat(),
                "expires_at": (now + timedelta(hours=1)).isoformat(),
            }
        )
        rights_path = fixture / "receipts" / "voice-rights.json"
        rights_path.parent.mkdir(parents=True)
        rights_path.write_text('{"approved":true}\n', encoding="utf-8")
        authorization["action"].update(
            {
                "metadata_endpoint": f"https://api.elevenlabs.io/v1/voices/{voice_id}",
                "sample_ids": [],
                "destinations": ["local-media/elevenlabs/original-sample.wav"],
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
                    "record_sha256": sha256_file(rights_path),
                },
            }
        )
        authorization["authorized_limits"] = {
            "max_calls": 2,
            "max_downloads": 1,
            "max_download_bytes": 10_000_000,
            "max_spend_usd": 0,
        }
        authorization["consumption"].update(
            {"status": "unconsumed", "record_path": "consumed/retrieval.json"}
        )
        self._write_json(auth_path, authorization)
        self.assertTrue(
            validate_provider_action_authorization(auth_path, now=now)["execution_ready"]
        )

        wrong_endpoint = copy.deepcopy(authorization)
        wrong_endpoint["action"]["metadata_endpoint"] += "/samples"
        self._write_json(auth_path, wrong_endpoint)
        with self.assertRaisesRegex(ValidationError, "exactly equal"):
            validate_provider_action_authorization(auth_path, now=now)

        mixed_speaker_drift = copy.deepcopy(authorization)
        mixed_speaker_drift["action"]["selection_fails_if_mixed_speaker"] = False
        self._write_json(auth_path, mixed_speaker_drift)
        with self.assertRaisesRegex(ValidationError, "multiple speakers"):
            validate_provider_action_authorization(auth_path, now=now)

        existing_receipt = fixture / authorization["action"]["metadata_receipt_destination"]
        existing_receipt.parent.mkdir(parents=True, exist_ok=True)
        existing_receipt.write_text("{}\n", encoding="utf-8")
        self._write_json(auth_path, authorization)
        with self.assertRaisesRegex(ValidationError, "may not overwrite"):
            validate_provider_action_authorization(auth_path, now=now)

    def test_active_hume_clone_requires_existing_hash_bound_source_rights_and_terms(self) -> None:
        temporary, fixture, envelope, w = self._copy_system()
        self.addCleanup(temporary.cleanup)
        self._refresh_compiled_and_auth_bindings(fixture, envelope, w)
        auth_path = fixture / "authorizations" / "02-hume-ui-upload-clone.DRAFT.json"
        authorization = json.loads(auth_path.read_text(encoding="utf-8"))
        now = datetime(2026, 8, 24, 16, 0, tzinfo=timezone.utc)
        authorization.update(
            {
                "status": "active",
                "approved": True,
                "execution_ready": True,
                "blockers": [],
                "approved_by": "Manav",
                "approved_at": (now - timedelta(hours=1)).isoformat(),
                "expires_at": (now + timedelta(hours=1)).isoformat(),
            }
        )
        authorization["action"].update(
            {
                "source_sample_path": "local-media/hume/manav-source.wav",
                "source_sample_sha256": "0" * 64,
                "source_sample_rights_record": "receipts/hume/rights.json",
                "source_sample_mime_type": "audio/wav",
                "source_sample_duration_seconds": 45,
                "rights_and_consent": {
                    "voice_owner": "Manav",
                    "provider_disclosure_approved": True,
                    "record_path": "receipts/hume/rights.json",
                    "record_sha256": "0" * 64,
                },
                "clone_receipt_destination": "receipts/hume/clone-created.json",
            }
        )
        authorization["account_requirements"] = {
            "account_tier": "creator",
            "commercial_use_eligibility": "verified",
            "logged_in_session_is_authorization": False,
            "commercial_terms_receipt_path": "receipts/hume/commercial-terms.json",
            "commercial_terms_receipt_sha256": "0" * 64,
        }
        authorization["authorized_limits"] = {
            "max_ui_uploads": 1,
            "max_voice_clones": 1,
            "max_spend_usd": 0,
        }
        authorization["consumption"].update(
            {"status": "unconsumed", "record_path": "consumed/hume-clone.json"}
        )
        self._write_json(auth_path, authorization)
        with self.assertRaises(ValidationError) as caught:
            validate_provider_action_authorization(auth_path, now=now)
        message = str(caught.exception)
        self.assertIn("source_sample.path is missing", message)
        self.assertIn("rights_and_consent.path is missing", message)
        self.assertIn("commercial_terms_receipt.path is missing", message)

        source = fixture / "local-media" / "hume" / "manav-source.wav"
        rights = fixture / "receipts" / "hume" / "rights.json"
        terms = fixture / "receipts" / "hume" / "commercial-terms.json"
        source.parent.mkdir(parents=True)
        rights.parent.mkdir(parents=True)
        source.write_bytes(b"human voice source")
        rights.write_text('{"owner":"Manav","approved":true}\n', encoding="utf-8")
        terms.write_text('{"commercial":true}\n', encoding="utf-8")
        self._write_json(auth_path, authorization)
        with self.assertRaisesRegex(ValidationError, "does not match the existing file"):
            validate_provider_action_authorization(auth_path, now=now)

        authorization["action"]["source_sample_sha256"] = sha256_file(source)
        authorization["action"]["rights_and_consent"]["record_sha256"] = sha256_file(rights)
        authorization["account_requirements"]["commercial_terms_receipt_sha256"] = sha256_file(terms)
        self._write_json(auth_path, authorization)
        self.assertTrue(
            validate_provider_action_authorization(auth_path, now=now)["execution_ready"]
        )

        wrong_rights_binding = copy.deepcopy(authorization)
        wrong_rights_binding["action"]["source_sample_rights_record"] = "receipts/hume/different-rights.json"
        self._write_json(auth_path, wrong_rights_binding)
        with self.assertRaisesRegex(ValidationError, "must exactly equal"):
            validate_provider_action_authorization(auth_path, now=now)

        clone_receipt = fixture / authorization["action"]["clone_receipt_destination"]
        clone_receipt.write_text("{}\n", encoding="utf-8")
        self._write_json(auth_path, authorization)
        with self.assertRaisesRegex(ValidationError, "may not overwrite"):
            validate_provider_action_authorization(auth_path, now=now)
        clone_receipt.unlink()

        outside = Path(temporary.name) / "outside-source.wav"
        outside.write_bytes(b"outside")
        source.unlink()
        source.symlink_to(outside)
        authorization["action"]["source_sample_sha256"] = sha256_file(outside)
        self._write_json(auth_path, authorization)
        with self.assertRaisesRegex(ValidationError, "symlink"):
            validate_provider_action_authorization(auth_path, now=now)

    def test_active_hume_calibration_requires_real_clone_receipt_terms_and_exact_caps(self) -> None:
        temporary, fixture, envelope, w = self._copy_system()
        self.addCleanup(temporary.cleanup)
        adapter_path = fixture / "adapters" / "hume-octave-1.json"
        adapter = json.loads(adapter_path.read_text(encoding="utf-8"))
        real_clone_id = "hume-manav-clone-verified"
        adapter["clone_voice_id"] = real_clone_id
        adapter["clone_state"] = "ready_provenance_receipted"
        self._write_json(adapter_path, adapter)

        plan_path = fixture / "provider-bakeoff-plan.json"
        plan = json.loads(plan_path.read_text(encoding="utf-8"))
        plan["provider_adapters"]["hume"]["sha256"] = sha256_file(adapter_path)
        hume_plan = next(provider for provider in plan["providers"] if provider["provider"] == "hume")
        hume_plan["voice_id"] = real_clone_id
        hume_plan["identity_state"] = "ready_provenance_receipted"
        self.assertFalse(hume_plan["execution_ready"])
        self._write_json(plan_path, plan)

        dry_run = self._refresh_compiled_and_auth_bindings(fixture, envelope, w)
        auth_path = fixture / "authorizations" / "04-hume-calibration.DRAFT.json"
        authorization = json.loads(auth_path.read_text(encoding="utf-8"))
        now = datetime(2026, 8, 24, 16, 0, tzinfo=timezone.utc)
        authorization.update(
            {
                "status": "active",
                "approved": True,
                "execution_ready": True,
                "blockers": [],
                "approved_by": "Manav",
                "approved_at": (now - timedelta(hours=1)).isoformat(),
                "expires_at": (now + timedelta(hours=1)).isoformat(),
            }
        )
        authorization["action"]["voice_id"] = real_clone_id
        maximum = dry_run["totals"]["by_provider"]["hume"][
            "maximum_with_one_fallback_per_request"
        ]
        authorization["authorized_limits"] = {
            "max_calls": maximum["max_call_count"],
            "max_outputs": maximum["expected_output_count"],
            "max_characters": maximum["max_billable_character_count"],
            "max_spend_usd": maximum["max_modeled_public_rate_cost_usd"],
        }
        authorization["bindings"].update(
            {
                "compiled_hash_state": "final_real_clone_id_bound",
                "clone_receipt_path": "receipts/hume/clone-receipt.json",
                "clone_receipt_sha256": "0" * 64,
            }
        )
        authorization["account_requirements"] = {
            "account_tier": "creator",
            "commercial_use_eligibility": "verified",
            "logged_in_session_is_authorization": False,
            "commercial_terms_receipt_path": "receipts/hume/commercial-terms.json",
            "commercial_terms_receipt_sha256": "0" * 64,
        }
        for key in list(authorization["consumption"]):
            if key.endswith("_used") or key.endswith("_used_usd") or key == "outputs_received":
                authorization["consumption"][key] = 0
        authorization["consumption"]["status"] = "unconsumed"
        authorization["consumption"]["record_path"] = "consumed/hume-calibration.json"
        self._write_json(auth_path, authorization)
        with self.assertRaises(ValidationError) as caught:
            validate_provider_action_authorization(auth_path, now=now)
        message = str(caught.exception)
        self.assertIn("bindings.clone_receipt.path is missing", message)
        self.assertIn("commercial_terms_receipt.path is missing", message)

        clone_receipt = fixture / authorization["bindings"]["clone_receipt_path"]
        terms = fixture / authorization["account_requirements"]["commercial_terms_receipt_path"]
        clone_receipt.parent.mkdir(parents=True, exist_ok=True)
        clone_receipt.write_text(
            json.dumps({"provider": "hume", "voice_id": real_clone_id}) + "\n",
            encoding="utf-8",
        )
        terms.write_text('{"commercial":true}\n', encoding="utf-8")
        self._write_json(auth_path, authorization)
        with self.assertRaisesRegex(ValidationError, "does not match the existing file"):
            validate_provider_action_authorization(auth_path, now=now)

        authorization["bindings"]["clone_receipt_sha256"] = sha256_file(clone_receipt)
        authorization["account_requirements"]["commercial_terms_receipt_sha256"] = sha256_file(terms)
        self._write_json(auth_path, authorization)
        self.assertTrue(
            validate_provider_action_authorization(auth_path, now=now)["execution_ready"]
        )

        wrong_caps = copy.deepcopy(authorization)
        wrong_caps["authorized_limits"]["max_characters"] += 1
        self._write_json(auth_path, wrong_caps)
        with self.assertRaisesRegex(ValidationError, "exactly equal"):
            validate_provider_action_authorization(auth_path, now=now)

        wrong_fallback = copy.deepcopy(authorization)
        wrong_fallback["action"]["fallback_request_call_ceiling"] -= 1
        self._write_json(auth_path, wrong_fallback)
        with self.assertRaisesRegex(ValidationError, "fallback_request_call_ceiling"):
            validate_provider_action_authorization(auth_path, now=now)

        logged_in_is_authority = copy.deepcopy(authorization)
        logged_in_is_authority["account_requirements"]["logged_in_session_is_authorization"] = True
        self._write_json(auth_path, logged_in_is_authority)
        with self.assertRaisesRegex(ValidationError, "logged-in Hume session"):
            validate_provider_action_authorization(auth_path, now=now)

    def test_authorization_rejects_unknown_scope_and_embedded_secret(self) -> None:
        temporary, fixture, envelope, w = self._copy_system()
        self.addCleanup(temporary.cleanup)
        self._refresh_compiled_and_auth_bindings(fixture, envelope, w)
        auth_path = fixture / "authorizations" / "01-elevenlabs-read-only-metadata-sample.DRAFT.json"
        authorization = json.loads(auth_path.read_text(encoding="utf-8"))
        authorization["scope"] = "all_provider_actions"
        authorization["action"]["api_key"] = "xi-not-a-real-secret-but-forbidden"
        self._write_json(auth_path, authorization)
        with self.assertRaises(ValidationError) as caught:
            validate_provider_action_authorization(auth_path)
        self.assertIn("four exact provider action enums", str(caught.exception))
        self.assertIn("credentials", str(caught.exception))

    def test_authorization_rejects_rehashed_but_tampered_compiled_dry_run(self) -> None:
        temporary, fixture, envelope, w = self._copy_system()
        self.addCleanup(temporary.cleanup)
        self._refresh_compiled_and_auth_bindings(fixture, envelope, w)
        compiled_path = fixture / "compiled" / "provider-bakeoff-dry-run.json"
        compiled = json.loads(compiled_path.read_text(encoding="utf-8"))
        compiled["requests"][0]["planned_call_count"] = 100
        self._write_json(compiled_path, compiled)
        auth_path = fixture / "authorizations" / "03-elevenlabs-calibration.DRAFT.json"
        authorization = json.loads(auth_path.read_text(encoding="utf-8"))
        authorization["bindings"]["compiled_dry_run_sha256"] = sha256_file(compiled_path)
        self._write_json(auth_path, authorization)
        with self.assertRaisesRegex(ValidationError, "deterministic compilation"):
            validate_provider_action_authorization(auth_path)

    def test_unknown_nested_request_action_limit_and_consumption_keys_fail(self) -> None:
        temporary, fixture, envelope, w = self._copy_system()
        self.addCleanup(temporary.cleanup)
        plan_path = fixture / "provider-bakeoff-plan.json"
        plan = json.loads(plan_path.read_text(encoding="utf-8"))
        plan["providers"][0]["requests"][0]["embedded_authorization"] = True
        self._write_json(plan_path, plan)
        with self.assertRaisesRegex(ValidationError, "unsupported keys"):
            validate_provider_bakeoff_plan(plan_path, envelope, w)

        shutil.copy2(self.plan, plan_path)
        self._refresh_compiled_and_auth_bindings(fixture, envelope, w)
        auth_path = fixture / "authorizations" / "03-elevenlabs-calibration.DRAFT.json"
        authorization = json.loads(auth_path.read_text(encoding="utf-8"))
        authorization["action"]["rewrite_words"] = True
        authorization["authorized_limits"]["unlimited_retry"] = True
        authorization["authorized_limits"]["max_voice_clones"] = 1
        authorization["consumption"]["ignore_existing_record"] = True
        self._write_json(auth_path, authorization)
        with self.assertRaises(ValidationError) as caught:
            validate_provider_action_authorization(auth_path)
        message = str(caught.exception)
        self.assertIn("action contains unsupported keys", message)
        self.assertIn("authorized_limits contains unsupported keys", message)
        self.assertIn("consumption contains unsupported keys", message)

    def test_published_schemas_close_material_unknown_property_surfaces(self) -> None:
        schemas = self.narration_root / "schemas"
        adapter = json.loads((schemas / "provider-adapter.schema.json").read_text(encoding="utf-8"))
        plan = json.loads((schemas / "provider-bakeoff-plan.schema.json").read_text(encoding="utf-8"))
        authorization = json.loads(
            (schemas / "provider-action-authorization.schema.json").read_text(encoding="utf-8")
        )
        envelope = json.loads((schemas / "performance-envelope.schema.json").read_text(encoding="utf-8"))
        self.assertFalse(envelope["additionalProperties"])
        self.assertFalse(adapter["additionalProperties"])
        self.assertFalse(plan["additionalProperties"])
        self.assertFalse(authorization["additionalProperties"])
        self.assertFalse(plan["$defs"]["pathHash"]["additionalProperties"])
        for definition in ("elevenPassage", "humePassage", "thoughtDirection"):
            self.assertFalse(adapter["$defs"][definition]["additionalProperties"])
        for definition in ("elevenRequest", "humeRequest", "humeCandidate", "formatPolicy"):
            self.assertFalse(plan["$defs"][definition]["additionalProperties"])
        for definition in (
            "retrievalAction",
            "cloneAction",
            "elevenCalibrationAction",
            "humeCalibrationAction",
            "requestedLimits",
            "authorizedLimits",
        ):
            self.assertFalse(authorization["$defs"][definition]["additionalProperties"])


if __name__ == "__main__":
    unittest.main()
