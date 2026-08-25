from __future__ import annotations

import base64
import copy
import json
import os
import stat
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest import mock

from oe_narration.core import (
    ValidationError,
    canonical_w_bytes,
    sha256_bytes,
    sha256_file,
    token_identity,
)
from oe_narration import voice_remix as vr


class VoiceRemixTests(unittest.TestCase):
    def _write_json(self, path: Path, value: dict) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    def _fixture(self) -> tuple[tempfile.TemporaryDirectory, Path, Path, dict]:
        temporary = tempfile.TemporaryDirectory()
        blueprint = Path(temporary.name) / "operator-blueprint-v2"
        fixture = (
            blueprint
            / "02-narration-production"
            / "fixtures"
            / "step2-v0.4-voice-remix-test"
        )
        auth_path = fixture / "authorizations" / "preview.json"
        auth_path.parent.mkdir(parents=True)

        tokens = [f"word{index}" for index in range(320)]
        canonical_w = (
            blueprint
            / "02-narration-production"
            / "fixtures"
            / "step2-v0.2-base"
            / "identity"
            / "canonical-w.txt"
        )
        canonical_w.parent.mkdir(parents=True)
        canonical_w.write_bytes(canonical_w_bytes(tokens))
        preview_tokens = tokens[
            vr.REQUIRED_HELD_OUT_START_TOKEN:vr.REQUIRED_HELD_OUT_END_TOKEN
        ]
        preview_text = " ".join(preview_tokens)
        prompt = (
            "Preserve Manav's recognizable identity, American accent, age, timbre, and "
            "conversational rhythm. Make this a camera-ready version of his normal voice: "
            "more intentional and alert, with energy from curiosity, contrast, and earned "
            "conviction. He is an experienced operator speaking across the table to one capable "
            "person. Use dry understatement for broken systems, plain confidence for evidence, "
            "and constructive momentum for instructions. Avoid announcer, trailer, motivational, "
            "sales, corporate-training, theatrical, sing-song, and artificially cheerful delivery."
        )
        ownership = fixture / "receipts" / "ownership.json"
        self._write_json(
            ownership,
            {
                "schema_version": "oe-voice-source-rights-and-consent-v1",
                "target_voice_id": "yUXeTfC1IFOCSjGc96sQ",
                "voice_owner": "Manav Thaker",
                "consent_owner": "Manav Thaker",
                "owner_approval": True,
            },
        )
        now = datetime.now(timezone.utc)
        action = {
            "kind": "remix_owned_voice_preview",
            "source_voice_id": "yUXeTfC1IFOCSjGc96sQ",
            "source_voice_owner": "Manav Thaker",
            "source_voice_owned_by_approver": True,
            "endpoint": (
                "https://api.elevenlabs.io/v1/text-to-voice/"
                "yUXeTfC1IFOCSjGc96sQ/remix?output_format=mp3_44100_192"
            ),
            "voice_description": prompt,
            "preview_text": preview_text,
            "preview_source": {
                "source_id": "C01B",
                "canonical_w_path": (
                    "02-narration-production/fixtures/step2-v0.2-base/"
                    "identity/canonical-w.txt"
                ),
                "canonical_w_sha256": sha256_file(canonical_w),
                "start_token": 139,
                "end_token": 236,
                "token_count": 97,
                "token_slice_sha256": token_identity(preview_tokens)["sha256"],
                "held_out": True,
                "excluded_from_scored_bakeoff": True,
            },
            "settings": {
                "auto_generate_text": False,
                "loudness": 0.5,
                "seed": 1_907_202_026,
                "guidance_scale": 2.0,
                "stream_previews": False,
                "prompt_strength": 0.25,
                "output_format": "mp3_44100_192",
            },
            "eligibility_check": {
                "mode": "provider_post_rejection_only",
                "voice_metadata_get_permitted": False,
                "subscription_get_permitted": False,
                "user_get_permitted": False,
            },
            "preview_destinations": [
                "local-media/elevenlabs/voice-remix/preview-01.mp3",
                "local-media/elevenlabs/voice-remix/preview-02.mp3",
                "local-media/elevenlabs/voice-remix/preview-03.mp3",
            ],
            "preview_receipt_destination": "receipts/elevenlabs/remix-preview.json",
            "failure_receipt_destination": "receipts/elevenlabs/remix-preview-failure.json",
            "automatic_preview_selection_permitted": False,
            "voice_save_permitted": False,
            "source_voice_mutation_permitted": False,
            "retries_permitted": False,
            "redirects_permitted": False,
            "credential_env": "ELEVENLABS_API_KEY",
        }
        body_hash = sha256_bytes(vr._canonical_body(vr._preview_request_body(action)))
        limits = {
            "max_calls": 1,
            "max_prompt_characters": len(prompt),
            "max_preview_text_characters": len(preview_text),
            "max_billable_characters": len(preview_text),
            "max_outputs": 3,
            "max_response_bytes": 200_000,
            "max_total_audio_bytes": 10_000,
            "max_total_duration_seconds": 90.0,
            "max_spend_usd": 1.0,
        }
        authorization = {
            "schema_version": vr.PREVIEW_AUTH_SCHEMA,
            "authorization_id": "AUTH-VOICE-REMIX-PREVIEW-TEST",
            "status": "active",
            "approved": True,
            "execution_ready": True,
            "scope": vr.PREVIEW_SCOPE,
            "provider": "elevenlabs",
            "target": {"kind": "fixture", "id": "step2-v0.4-voice-remix-test"},
            "action": action,
            "bindings": {
                "voice_description_sha256": sha256_bytes(prompt.encode("utf-8")),
                "preview_text_sha256": sha256_bytes(preview_text.encode("utf-8")),
                "request_body_sha256": body_hash,
                "source_voice_ownership_receipt": {
                    "path": "receipts/ownership.json",
                    "sha256": sha256_file(ownership),
                },
            },
            "requested_limits": copy.deepcopy(limits),
            "authorized_limits": copy.deepcopy(limits),
            "consumption": {
                "status": "unconsumed",
                "calls_used": 0,
                "outputs_used": 0,
                "spend_used_usd": 0,
                "record_path": "consumed/preview.json",
            },
            "approved_by": "Manav Thaker",
            "approved_at": (now - timedelta(minutes=1)).isoformat(),
            "expires_at": (now + timedelta(hours=1)).isoformat(),
            "blockers": [],
        }
        self._write_json(auth_path, authorization)
        return temporary, fixture, auth_path, authorization

    def _response(self, authorization: dict, count: int = 3) -> vr._HttpResponse:
        previews = []
        for index in range(count):
            audio = b"ID3" + bytes([index + 1]) * 32
            previews.append(
                {
                    "audio_base_64": base64.b64encode(audio).decode("ascii"),
                    "generated_voice_id": f"GeneratedVoice{index + 1:02d}",
                    "media_type": "audio/mpeg",
                    "duration_secs": 8.5 + index,
                    "language": "en",
                }
            )
        payload = {
            "previews": previews,
            "text": authorization["action"]["preview_text"],
        }
        return vr._HttpResponse(
            data=json.dumps(payload).encode("utf-8"),
            mime_type="application/json",
            headers={
                "content-type": "application/json",
                "character-cost": str(len(authorization["action"]["preview_text"])),
                "request-id": "request-safe-123",
                "trace-id": "trace-safe-123",
            },
            provider_identifiers={
                "request-id": "request-safe-123",
                "trace-id": "trace-safe-123",
            },
        )

    def _execute_preview(
        self,
        fixture: Path,
        auth_path: Path,
        authorization: dict,
        *,
        count: int = 3,
    ) -> dict:
        consumption = fixture / "authorizations" / "consumed" / "preview.json"

        def provider_call(*args, **kwargs):
            self.assertTrue(consumption.is_file(), "authorization must be consumed before network")
            return self._response(authorization, count=count)

        with mock.patch.dict(os.environ, {"ELEVENLABS_API_KEY": "valid-eleven-key-123456"}, clear=True):
            with mock.patch.object(vr, "_post_json", side_effect=provider_call) as post:
                result = vr.execute_voice_remix_preview(auth_path)
        post.assert_called_once()
        return result

    def test_preview_dry_run_is_exact_and_side_effect_free(self) -> None:
        temporary, fixture, auth_path, authorization = self._fixture()
        self.addCleanup(temporary.cleanup)
        with mock.patch.object(vr, "_post_json") as post:
            result = vr.dry_run_voice_remix_preview(auth_path)
        post.assert_not_called()
        self.assertFalse(result["network_called"])
        self.assertFalse(result["credentials_accessed"])
        self.assertEqual(result["provider_calls_made"], 0)
        validation = result["authorization_validation"]
        self.assertEqual(validation["request"]["body"]["text"], authorization["action"]["preview_text"])
        self.assertEqual(validation["request"]["body"]["seed"], 1_907_202_026)
        self.assertEqual(validation["request"]["body_sha256"], authorization["bindings"]["request_body_sha256"])
        self.assertEqual(validation["eligibility_check"]["provider_get_calls_permitted"], 0)
        self.assertFalse((fixture / "local-media").exists())
        self.assertFalse((fixture / "authorizations" / "consumed").exists())

    def test_active_preview_rejects_future_dated_approval(self) -> None:
        temporary, fixture, auth_path, authorization = self._fixture()
        self.addCleanup(temporary.cleanup)
        validation_now = datetime.now(timezone.utc)
        authorization["approved_at"] = (
            validation_now + timedelta(minutes=5)
        ).isoformat()
        authorization["expires_at"] = (
            validation_now + timedelta(hours=1)
        ).isoformat()
        self._write_json(auth_path, authorization)

        with self.assertRaisesRegex(ValidationError, "approved_at may not be in the future"):
            vr.validate_voice_remix_preview_authorization(
                auth_path,
                now=validation_now,
            )
        self.assertFalse((fixture / "authorizations" / "consumed").exists())

    def test_preview_preserves_every_returned_candidate_without_selecting_or_saving(self) -> None:
        temporary, fixture, auth_path, authorization = self._fixture()
        self.addCleanup(temporary.cleanup)
        result = self._execute_preview(fixture, auth_path, authorization)
        self.assertEqual(result["preview_count"], 3)
        self.assertEqual(result["selection_status"], "owner_decision_pending")
        self.assertIsNone(result["selected_generated_voice_id"])
        self.assertFalse(result["voice_created"])
        self.assertFalse(result["save_authorized"])
        receipt = json.loads(Path(result["preview_receipt"]).read_text(encoding="utf-8"))
        self.assertEqual(receipt["selection"]["status"], "owner_decision_pending")
        self.assertTrue(receipt["selection"]["all_provider_previews_preserved"])
        self.assertEqual(receipt["provider_character_cost"]["value"], len(authorization["action"]["preview_text"]))
        self.assertFalse(receipt["provider_character_cost"]["is_usd"])
        self.assertEqual(receipt["provider_identifiers"]["trace-id"], "trace-safe-123")
        self.assertFalse(receipt["eligibility_verification"]["metadata_get_called"])
        self.assertFalse(receipt["spend"]["provider_enforced_usd_cap"])
        for preview in receipt["previews"]:
            audio = fixture / preview["audio_path"]
            self.assertTrue(audio.is_file())
            self.assertEqual(stat.S_IMODE(audio.stat().st_mode), 0o600)

    def test_provider_may_return_fewer_than_output_cap_and_all_are_preserved(self) -> None:
        temporary, fixture, auth_path, authorization = self._fixture()
        self.addCleanup(temporary.cleanup)
        result = self._execute_preview(fixture, auth_path, authorization, count=2)
        self.assertEqual(result["preview_count"], 2)
        self.assertFalse(
            (fixture / authorization["action"]["preview_destinations"][2]).exists()
        )

    def test_missing_character_cost_is_recorded_not_retried_or_treated_as_usd(self) -> None:
        temporary, fixture, auth_path, authorization = self._fixture()
        self.addCleanup(temporary.cleanup)
        response = self._response(authorization, count=1)
        response = vr._HttpResponse(
            data=response.data,
            mime_type=response.mime_type,
            headers={"content-type": "application/json", "request-id": "request-safe-123"},
            provider_identifiers={"request-id": "request-safe-123"},
        )
        with mock.patch.dict(os.environ, {"ELEVENLABS_API_KEY": "valid-eleven-key-123456"}, clear=True):
            with mock.patch.object(vr, "_post_json", return_value=response) as post:
                result = vr.execute_voice_remix_preview(auth_path)
        post.assert_called_once()
        receipt = json.loads(Path(result["preview_receipt"]).read_text())
        self.assertIsNone(receipt["provider_character_cost"]["value"])
        self.assertEqual(receipt["provider_character_cost"]["unit"], "not_reported")
        self.assertFalse(receipt["provider_character_cost"]["is_usd"])
        self.assertEqual(receipt["spend"]["status"], "modeled_or_unknown")

    def test_malformed_credential_never_consumes_authorization(self) -> None:
        for credential in (" short", "valid-eleven-key-123456\n"):
            with self.subTest(credential=repr(credential)):
                temporary, fixture, auth_path, _ = self._fixture()
                self.addCleanup(temporary.cleanup)
                with mock.patch.dict(os.environ, {"ELEVENLABS_API_KEY": credential}, clear=True):
                    with mock.patch.object(vr, "_post_json") as post:
                        with self.assertRaisesRegex(ValidationError, "malformed"):
                            vr.execute_voice_remix_preview(auth_path)
                post.assert_not_called()
                self.assertFalse((fixture / "authorizations" / "consumed").exists())

        temporary, fixture, auth_path, _ = self._fixture()
        self.addCleanup(temporary.cleanup)
        with mock.patch.object(os.environ, "get", return_value="valid\x00eleven-key-123456"):
            with mock.patch.object(vr, "_post_json") as post:
                with self.assertRaisesRegex(ValidationError, "malformed"):
                    vr.execute_voice_remix_preview(auth_path)
        post.assert_not_called()
        self.assertFalse((fixture / "authorizations" / "consumed").exists())

    def test_missing_credential_never_consumes_authorization(self) -> None:
        temporary, fixture, auth_path, _ = self._fixture()
        self.addCleanup(temporary.cleanup)
        with mock.patch.dict(os.environ, {}, clear=True):
            with self.assertRaisesRegex(ValidationError, "ELEVENLABS_API_KEY"):
                vr.execute_voice_remix_preview(auth_path)
        self.assertFalse((fixture / "authorizations" / "consumed").exists())

    def test_request_body_prompt_strength_and_held_out_source_are_authorization_bound(self) -> None:
        mutations = (
            ("request_hash", lambda auth: auth["bindings"].__setitem__("request_body_sha256", "0" * 64)),
            ("strength", lambda auth: auth["action"]["settings"].__setitem__("prompt_strength", 0.31)),
            ("range", lambda auth: auth["action"]["preview_source"].__setitem__("start_token", 0)),
            ("source", lambda auth: auth["action"]["preview_source"].__setitem__("source_id", "S00")),
        )
        for label, mutate in mutations:
            with self.subTest(label=label):
                temporary, _, auth_path, authorization = self._fixture()
                self.addCleanup(temporary.cleanup)
                mutate(authorization)
                self._write_json(auth_path, authorization)
                with self.assertRaises(ValidationError):
                    vr.dry_run_voice_remix_preview(auth_path)

    def test_prompt_must_leave_headroom_below_provider_ceiling(self) -> None:
        temporary, _, auth_path, authorization = self._fixture()
        self.addCleanup(temporary.cleanup)
        prompt = "p" * 951
        authorization["action"]["voice_description"] = prompt
        authorization["bindings"]["voice_description_sha256"] = sha256_bytes(prompt.encode())
        authorization["authorized_limits"]["max_prompt_characters"] = len(prompt)
        authorization["requested_limits"] = copy.deepcopy(authorization["authorized_limits"])
        authorization["bindings"]["request_body_sha256"] = sha256_bytes(
            vr._canonical_body(vr._preview_request_body(authorization["action"]))
        )
        self._write_json(auth_path, authorization)
        with self.assertRaisesRegex(ValidationError, "950"):
            vr.dry_run_voice_remix_preview(auth_path)

    def test_preview_get_preflight_and_user_endpoint_cannot_be_enabled(self) -> None:
        temporary, _, auth_path, authorization = self._fixture()
        self.addCleanup(temporary.cleanup)
        authorization["action"]["eligibility_check"]["user_get_permitted"] = True
        self._write_json(auth_path, authorization)
        with self.assertRaisesRegex(ValidationError, "make no GET calls"):
            vr.dry_run_voice_remix_preview(auth_path)

    def test_path_traversal_and_symlink_destinations_fail_before_consumption(self) -> None:
        temporary, fixture, auth_path, authorization = self._fixture()
        self.addCleanup(temporary.cleanup)
        authorization["action"]["preview_destinations"][0] = "../escape.mp3"
        self._write_json(auth_path, authorization)
        with self.assertRaises(ValidationError):
            vr.dry_run_voice_remix_preview(auth_path)

        temporary2, fixture2, auth_path2, _ = self._fixture()
        self.addCleanup(temporary2.cleanup)
        outside = Path(temporary2.name) / "outside"
        outside.mkdir()
        local_media = fixture2 / "local-media"
        local_media.symlink_to(outside, target_is_directory=True)
        with self.assertRaisesRegex(ValidationError, "symlink"):
            vr.dry_run_voice_remix_preview(auth_path2)

    def test_existing_output_blocks_before_credential_or_network(self) -> None:
        temporary, fixture, auth_path, authorization = self._fixture()
        self.addCleanup(temporary.cleanup)
        output = fixture / authorization["action"]["preview_destinations"][0]
        output.parent.mkdir(parents=True)
        output.write_bytes(b"existing")
        with mock.patch.dict(os.environ, {"ELEVENLABS_API_KEY": "valid-eleven-key-123456"}, clear=True):
            with mock.patch.object(vr, "_post_json") as post:
                with self.assertRaisesRegex(ValidationError, "already exists"):
                    vr.execute_voice_remix_preview(auth_path)
        post.assert_not_called()
        self.assertFalse((fixture / "authorizations" / "consumed").exists())

    def test_failure_is_consumed_once_without_retry_and_writes_redacted_receipt(self) -> None:
        temporary, fixture, auth_path, _ = self._fixture()
        self.addCleanup(temporary.cleanup)
        with mock.patch.dict(os.environ, {"ELEVENLABS_API_KEY": "valid-eleven-key-123456"}, clear=True):
            with mock.patch.object(
                vr,
                "_post_json",
                side_effect=vr._ProviderFailure("redirect_forbidden", http_status=302),
            ) as post:
                with self.assertRaisesRegex(ValidationError, "redirect_forbidden"):
                    vr.execute_voice_remix_preview(auth_path)
        post.assert_called_once()
        self.assertTrue((fixture / "authorizations" / "consumed" / "preview.json").is_file())
        failure = json.loads(
            (fixture / "receipts" / "elevenlabs" / "remix-preview-failure.json").read_text()
        )
        self.assertEqual(failure["reason"], "redirect_forbidden")
        self.assertFalse(failure["retry_permitted"])
        self.assertFalse(failure["voice_created"])
        self.assertNotIn("voice_creation_status", failure)
        self.assertNotIn("reconciliation_required", failure)
        self.assertFalse(failure["raw_provider_payload_stored"])
        self.assertNotIn("valid-eleven-key", json.dumps(failure))

    def test_text_codec_output_and_character_cost_drift_fail_before_audio_storage(self) -> None:
        cases = []
        temporary, fixture, auth_path, authorization = self._fixture()
        self.addCleanup(temporary.cleanup)
        response = self._response(authorization)
        payload = json.loads(response.data)
        payload["text"] += " drift"
        cases.append(("text", fixture, auth_path, authorization, copy.copy(response), payload))

        for label in ("codec", "character-cost"):
            temporary_case, fixture_case, auth_case, auth_value = self._fixture()
            self.addCleanup(temporary_case.cleanup)
            response_case = self._response(auth_value)
            payload_case = json.loads(response_case.data)
            if label == "codec":
                payload_case["previews"][0]["media_type"] = "audio/wav"
            else:
                response_case = vr._HttpResponse(
                    data=response_case.data,
                    mime_type=response_case.mime_type,
                    headers={"content-type": "application/json", "character-cost": "not-an-int"},
                    provider_identifiers={},
                )
            cases.append((label, fixture_case, auth_case, auth_value, response_case, payload_case))

        for label, fixture_case, auth_case, _, response_case, payload_case in cases:
            with self.subTest(label=label):
                response_case = vr._HttpResponse(
                    data=json.dumps(payload_case).encode(),
                    mime_type=response_case.mime_type,
                    headers=response_case.headers,
                    provider_identifiers=response_case.provider_identifiers,
                )
                with mock.patch.dict(os.environ, {"ELEVENLABS_API_KEY": "valid-eleven-key-123456"}, clear=True):
                    with mock.patch.object(vr, "_post_json", return_value=response_case):
                        with self.assertRaises(ValidationError):
                            vr.execute_voice_remix_preview(auth_case)
                self.assertFalse((fixture_case / "local-media").exists())
                self.assertTrue(
                    (fixture_case / "receipts" / "elevenlabs" / "remix-preview-failure.json").is_file()
                )

    def _save_authorization(
        self,
        fixture: Path,
        preview_result: dict,
        preview_authorization: dict,
    ) -> tuple[Path, dict]:
        preview_receipt = json.loads(Path(preview_result["preview_receipt"]).read_text())
        selected = preview_receipt["previews"][0]
        now = datetime.now(timezone.utc)
        selection = {
            "schema_version": vr.OWNER_SELECTION_SCHEMA,
            "preview_receipt_sha256": preview_result["preview_receipt_sha256"],
            "source_voice_id": preview_authorization["action"]["source_voice_id"],
            "selected_generated_voice_id": selected["generated_voice_id"],
            "selected_audio_sha256": selected["audio_sha256"],
            "selected_by": "Manav Thaker",
            "selected_at": (now - timedelta(minutes=2)).isoformat(),
            "owner_approved_save": True,
            "voice_name": "Manav - OE Performance v1",
            "voice_description": "A camera-ready Operator Economy performance variant of Manav.",
        }
        selection_path = fixture / "receipts" / "elevenlabs" / "owner-selection.json"
        self._write_json(selection_path, selection)
        ownership = fixture / "receipts" / "ownership.json"
        action = {
            "kind": "create_new_voice_from_owner_selected_preview",
            "source_voice_id": preview_authorization["action"]["source_voice_id"],
            "source_voice_owner": "Manav Thaker",
            "source_voice_owned_by_approver": True,
            "endpoint": vr.SAVE_ENDPOINT,
            "preview_receipt_path": "receipts/elevenlabs/remix-preview.json",
            "preview_receipt_sha256": preview_result["preview_receipt_sha256"],
            "owner_selection_record_path": "receipts/elevenlabs/owner-selection.json",
            "owner_selection_record_sha256": sha256_file(selection_path),
            "selected_generated_voice_id": selected["generated_voice_id"],
            "selected_audio_sha256": selected["audio_sha256"],
            "voice_name": selection["voice_name"],
            "voice_description": selection["voice_description"],
            "labels": {"use": "operator-economy", "version": "v1"},
            "played_not_selected_voice_ids": [],
            "save_receipt_destination": "receipts/elevenlabs/remix-save.json",
            "failure_receipt_destination": "receipts/elevenlabs/remix-save-failure.json",
            "new_voice_required": True,
            "source_voice_mutation_permitted": False,
            "retries_permitted": False,
            "redirects_permitted": False,
            "credential_env": "ELEVENLABS_API_KEY",
        }
        body_hash = sha256_bytes(vr._canonical_body(vr._save_request_body(action)))
        limits = {
            "max_calls": 1,
            "max_voices_created": 1,
            "max_response_bytes": 200_000,
            "max_spend_usd": 1.0,
        }
        authorization = {
            "schema_version": vr.SAVE_AUTH_SCHEMA,
            "authorization_id": "AUTH-VOICE-REMIX-SAVE-TEST",
            "status": "active",
            "approved": True,
            "execution_ready": True,
            "scope": vr.SAVE_SCOPE,
            "provider": "elevenlabs",
            "target": {"kind": "fixture", "id": "step2-v0.4-voice-remix-test"},
            "action": action,
            "bindings": {
                "request_body_sha256": body_hash,
                "source_voice_ownership_receipt": {
                    "path": "receipts/ownership.json",
                    "sha256": sha256_file(ownership),
                },
            },
            "requested_limits": copy.deepcopy(limits),
            "authorized_limits": copy.deepcopy(limits),
            "consumption": {
                "status": "unconsumed",
                "calls_used": 0,
                "voices_created": 0,
                "spend_used_usd": 0,
                "record_path": "consumed/save.json",
            },
            "approved_by": "Manav Thaker",
            "approved_at": (now - timedelta(minutes=1)).isoformat(),
            "expires_at": (now + timedelta(hours=1)).isoformat(),
            "blockers": [],
        }
        path = fixture / "authorizations" / "save.json"
        self._write_json(path, authorization)
        return path, authorization

    def test_save_is_separate_owner_selected_new_voice_action(self) -> None:
        temporary, fixture, preview_auth_path, preview_authorization = self._fixture()
        self.addCleanup(temporary.cleanup)
        preview_result = self._execute_preview(
            fixture, preview_auth_path, preview_authorization
        )
        save_path, save_authorization = self._save_authorization(
            fixture, preview_result, preview_authorization
        )
        dry_run = vr.dry_run_voice_remix_save(save_path)
        self.assertFalse(dry_run["network_called"])
        self.assertEqual(dry_run["voices_created"], 0)
        consumption = fixture / "authorizations" / "consumed" / "save.json"

        def provider_call(*args, **kwargs):
            self.assertTrue(consumption.is_file())
            data = json.dumps(
                {
                    "voice_id": "NewOperatorVoice001",
                    "name": save_authorization["action"]["voice_name"],
                    "category": "generated",
                }
            ).encode()
            return vr._HttpResponse(
                data=data,
                mime_type="application/json",
                headers={"content-type": "application/json"},
                provider_identifiers={"request-id": "save-request-safe"},
            )

        with mock.patch.dict(os.environ, {"ELEVENLABS_API_KEY": "valid-eleven-key-123456"}, clear=True):
            with mock.patch.object(vr, "_post_json", side_effect=provider_call) as post:
                result = vr.execute_voice_remix_save(save_path)
        post.assert_called_once()
        self.assertEqual(result["new_voice_id"], "NewOperatorVoice001")
        self.assertFalse(result["source_voice_modified"])
        self.assertNotEqual(result["new_voice_id"], result["source_voice_id"])

    def test_active_save_rejects_future_dated_approval(self) -> None:
        temporary, fixture, preview_auth_path, preview_authorization = self._fixture()
        self.addCleanup(temporary.cleanup)
        preview_result = self._execute_preview(
            fixture, preview_auth_path, preview_authorization
        )
        save_path, save_authorization = self._save_authorization(
            fixture, preview_result, preview_authorization
        )
        validation_now = datetime.now(timezone.utc)
        save_authorization["approved_at"] = (
            validation_now + timedelta(minutes=5)
        ).isoformat()
        save_authorization["expires_at"] = (
            validation_now + timedelta(hours=1)
        ).isoformat()
        self._write_json(save_path, save_authorization)

        with self.assertRaisesRegex(ValidationError, "approved_at may not be in the future"):
            vr.validate_voice_remix_save_authorization(
                save_path,
                now=validation_now,
            )
        self.assertFalse((fixture / "authorizations" / "consumed" / "save.json").exists())

    def test_save_rejects_review_telemetry_or_selection_drift_before_network(self) -> None:
        mutations = (
            lambda auth: auth["action"].__setitem__(
                "played_not_selected_voice_ids", ["GeneratedVoice02"]
            ),
            lambda auth: auth["action"].__setitem__("selected_audio_sha256", "0" * 64),
            lambda auth: auth["bindings"].__setitem__("request_body_sha256", "0" * 64),
        )
        for mutate in mutations:
            with self.subTest(mutation=mutate):
                temporary, fixture, preview_auth_path, preview_authorization = self._fixture()
                self.addCleanup(temporary.cleanup)
                preview_result = self._execute_preview(
                    fixture, preview_auth_path, preview_authorization
                )
                save_path, save_authorization = self._save_authorization(
                    fixture, preview_result, preview_authorization
                )
                mutate(save_authorization)
                self._write_json(save_path, save_authorization)
                with mock.patch.object(vr, "_post_json") as post:
                    with self.assertRaises(ValidationError):
                        vr.execute_voice_remix_save(save_path)
                post.assert_not_called()
                self.assertFalse((fixture / "authorizations" / "consumed" / "save.json").exists())

    def test_save_rejects_provider_returning_incumbent_id(self) -> None:
        temporary, fixture, preview_auth_path, preview_authorization = self._fixture()
        self.addCleanup(temporary.cleanup)
        preview_result = self._execute_preview(
            fixture, preview_auth_path, preview_authorization
        )
        save_path, save_authorization = self._save_authorization(
            fixture, preview_result, preview_authorization
        )
        response = vr._HttpResponse(
            data=json.dumps(
                {
                    "voice_id": preview_authorization["action"]["source_voice_id"],
                    "name": save_authorization["action"]["voice_name"],
                }
            ).encode(),
            mime_type="application/json",
            headers={"content-type": "application/json"},
            provider_identifiers={},
        )
        with mock.patch.dict(os.environ, {"ELEVENLABS_API_KEY": "valid-eleven-key-123456"}, clear=True):
            with mock.patch.object(vr, "_post_json", return_value=response) as post:
                with self.assertRaisesRegex(ValidationError, "incumbent"):
                    vr.execute_voice_remix_save(save_path)
        post.assert_called_once()
        self.assertTrue((fixture / "authorizations" / "consumed" / "save.json").exists())
        failure_path = (
            fixture / "receipts" / "elevenlabs" / "remix-save-failure.json"
        )
        self.assertTrue(failure_path.exists())
        failure = json.loads(failure_path.read_text(encoding="utf-8"))
        self.assertEqual(failure["attempted_calls"], 1)
        self.assertFalse(failure["retry_permitted"])
        self.assertNotIn("voice_created", failure)
        self.assertEqual(
            failure["voice_creation_status"],
            "indeterminate_after_attempt",
        )
        self.assertTrue(failure["reconciliation_required"])


if __name__ == "__main__":
    unittest.main()
