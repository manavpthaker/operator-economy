from __future__ import annotations

import copy
import io
import json
import os
import shutil
import tempfile
import unittest
import urllib.error
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest import mock

from oe_narration.bakeoff import (
    dry_run_provider_bakeoff,
    validate_provider_action_authorization,
)
from oe_narration.core import ValidationError, sha256_file
from oe_narration.directed_bakeoff import (
    _HttpFailure,
    _HttpResponse,
    _character_cost,
    _post_once,
    _provider_identifiers,
    _validate_mp3_signature,
    _validate_pcm_response,
    execute_directed_bakeoff,
    validate_directed_bakeoff_execution,
)


class DirectedBakeoffTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.narration_root = Path(__file__).resolve().parents[2]
        fixtures = cls.narration_root / "fixtures"
        matches = sorted(fixtures.glob("step2-v0.3-*-provider-bakeoff"))
        if len(matches) != 1:
            raise AssertionError(f"expected one v0.3 bakeoff fixture, found {matches}")
        cls.source_fixture = matches[0]
        cls.base_fixture = fixtures / "step2-v0.2-ai-visibility-v1.1"
        cls.source_w = cls.base_fixture / "identity" / "canonical-w.txt"
        cls.editorial_root = cls.narration_root.parent / "01-editorial"

    def _write_json(self, path: Path, value: dict) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    def _copy_system(self) -> tuple[tempfile.TemporaryDirectory, Path, Path]:
        temporary = tempfile.TemporaryDirectory()
        blueprint = Path(temporary.name) / "operator-blueprint-v2"
        fixtures = blueprint / "02-narration-production" / "fixtures"
        fixtures.mkdir(parents=True)
        fixture = fixtures / self.source_fixture.name
        shutil.copytree(
            self.source_fixture,
            fixture,
            ignore=shutil.ignore_patterns(
                "local-media",
                "outputs",
                "receipts",
                "consumed",
                "*.ACTIVE.*",
            ),
        )
        copied_identity = fixtures / self.base_fixture.name / "identity"
        copied_identity.mkdir(parents=True)
        shutil.copy2(self.source_w, copied_identity / self.source_w.name)
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
        w = copied_identity / self.source_w.name
        compiled = dry_run_provider_bakeoff(
            fixture / "provider-bakeoff-plan.json",
            fixture / "performance-envelope.json",
            w,
        )
        self._write_json(fixture / "compiled" / "provider-bakeoff-dry-run.json", compiled)
        return temporary, fixture, w

    def _activate(self, fixture: Path) -> Path:
        draft_path = fixture / "authorizations" / "03-elevenlabs-calibration.DRAFT.json"
        authorization = json.loads(draft_path.read_text(encoding="utf-8"))
        compiled_path = fixture / "compiled" / "provider-bakeoff-dry-run.json"
        dry_run = json.loads(compiled_path.read_text(encoding="utf-8"))
        now = datetime.now(timezone.utc)
        maximum = dry_run["totals"]["by_provider"]["elevenlabs"][
            "maximum_with_one_fallback_per_request"
        ]
        authorization.update(
            {
                "authorization_id": "AUTH-test-directed-bakeoff",
                "status": "active",
                "approved": True,
                "approved_by": "Owner",
                "approved_at": (now - timedelta(minutes=1)).isoformat(),
                "expires_at": (now + timedelta(hours=1)).isoformat(),
                "execution_ready": True,
                "blockers": [],
            }
        )
        authorization["bindings"]["compiled_dry_run_sha256"] = sha256_file(compiled_path)
        authorization["authorized_limits"] = {
            "max_calls": maximum["max_call_count"],
            "max_outputs": maximum["expected_output_count"],
            "max_characters": maximum["max_billable_character_count"],
            "max_spend_usd": maximum["max_modeled_public_rate_cost_usd"],
        }
        authorization["consumption"] = {
            "status": "unconsumed",
            "calls_used": 0,
            "characters_used": 0,
            "outputs_received": 0,
            "spend_used_usd": 0,
            "record_path": "consumed/AUTH-test-directed-bakeoff.consumed.json",
        }
        voice_id = authorization["action"]["voice_id"]
        source_voice_id = "test-owner-source-voice"
        audio_sha256 = "a" * 64
        selection_path = fixture / "receipts" / "elevenlabs" / "test-owner-selection.json"
        selection = {
            "schema_version": "oe-elevenlabs-voice-remix-owner-selection-v1",
            "preview_receipt_sha256": "b" * 64,
            "source_voice_id": source_voice_id,
            "selected_generated_voice_id": voice_id,
            "selected_audio_sha256": audio_sha256,
            "selected_by": "Owner",
            "selected_at": (now - timedelta(minutes=2)).isoformat(),
            "owner_approved_save": True,
            "voice_name": "Test saved voice",
            "voice_description": "Synthetic test provenance only.",
        }
        self._write_json(selection_path, selection)
        selection_sha256 = sha256_file(selection_path)
        saved_path = fixture / "receipts" / "elevenlabs" / "test-saved-voice.json"
        saved = {
            "schema_version": "oe-elevenlabs-voice-remix-save-receipt-v1",
            "outcome": "new_voice_created_from_owner_selected_preview",
            "provider": "elevenlabs",
            "scope": "elevenlabs_voice_remix_save",
            "source_voice_id": source_voice_id,
            "selected_generated_voice_id": voice_id,
            "selected_audio_sha256": audio_sha256,
            "owner_selection_record_sha256": selection_sha256,
            "new_voice_id": voice_id,
            "new_voice_created": True,
            "source_voice_modified": False,
            "provider_calls_made": 1,
        }
        self._write_json(saved_path, saved)
        saved_sha256 = sha256_file(saved_path)
        rights_path = fixture / "receipts" / "elevenlabs" / "test-calibration-rights.json"
        rights = {
            "schema_version": "oe-elevenlabs-calibration-rights-v1",
            "provider": "elevenlabs",
            "authorization_id": authorization["authorization_id"],
            "compiled_dry_run_sha256": authorization["bindings"][
                "compiled_dry_run_sha256"
            ],
            "authorized_limits": copy.deepcopy(authorization["authorized_limits"]),
            "voice_provenance_kind": "saved_remix",
            "voice_owner": authorization["approved_by"],
            "consent_owner": authorization["approved_by"],
            "target_voice_id": voice_id,
            "owner_approval": True,
            "tts_generation_permitted": True,
            "permitted_use": "bounded_calibration_only",
            "full_capture_permitted": False,
            "saved_voice_receipt_sha256": saved_sha256,
        }
        self._write_json(rights_path, rights)
        authorization["bindings"].update(
            {
                "voice_provenance_kind": "saved_remix",
                "calibration_rights_receipt_path": rights_path.relative_to(fixture).as_posix(),
                "calibration_rights_receipt_sha256": sha256_file(rights_path),
                "owner_selection_record_path": selection_path.relative_to(fixture).as_posix(),
                "owner_selection_record_sha256": selection_sha256,
                "saved_voice_receipt_path": saved_path.relative_to(fixture).as_posix(),
                "saved_voice_receipt_sha256": saved_sha256,
            }
        )
        active = fixture / "authorizations" / "03-elevenlabs-calibration.ACTIVE.test.json"
        self._write_json(active, authorization)
        return active

    @staticmethod
    def _pcm() -> _HttpResponse:
        return _HttpResponse(
            data=b"\x00\x00" * 480,
            mime_type="application/octet-stream",
            headers={},
            provider_identifiers={"request-id": "provider-test"},
            character_cost={
                "header": "character-cost",
                "present": True,
                "value": 842,
                "unit": "provider_reported_character_cost",
            },
        )

    def test_validate_exact_active_contract_is_credential_free(self) -> None:
        temporary, fixture, _w = self._copy_system()
        self.addCleanup(temporary.cleanup)
        active = self._activate(fixture)
        with mock.patch.dict(os.environ, {"ELEVENLABS_API_KEY": "secret-that-must-not-be-read"}), mock.patch(
            "oe_narration.directed_bakeoff._post_once"
        ) as post:
            contract = validate_directed_bakeoff_execution(active)
        post.assert_not_called()
        public = contract.public_dict()
        self.assertFalse(public["credentials_accessed"])
        self.assertFalse(public["network_called"])
        self.assertEqual(public["primary_request_count"], 4)
        self.assertEqual(public["passage_count"], 2)
        self.assertIsNotNone(public["seed_map_sha256"])

    def test_schema_valid_draft_cannot_enter_directed_execution_preflight(self) -> None:
        temporary, fixture, _w = self._copy_system()
        self.addCleanup(temporary.cleanup)
        authorization_path = self._activate(fixture)
        authorization = json.loads(authorization_path.read_text(encoding="utf-8"))
        authorization.update(
            {
                "status": "draft",
                "approved": False,
                "approved_by": "",
                "approved_at": "",
                "expires_at": "",
                "execution_ready": False,
                "blockers": ["Owner authorization is intentionally absent."],
            }
        )
        authorization["consumption"]["status"] = "not_authorized"
        authorization["consumption"]["record_path"] = "consumed/draft-placeholder.json"
        for field in (
            "voice_provenance_kind",
            "calibration_rights_receipt_path",
            "calibration_rights_receipt_sha256",
            "owner_selection_record_path",
            "owner_selection_record_sha256",
            "saved_voice_receipt_path",
            "saved_voice_receipt_sha256",
        ):
            authorization["bindings"].pop(field)
        self.assertGreater(authorization["authorized_limits"]["max_calls"], 0)
        self._write_json(authorization_path, authorization)

        provider_result = validate_provider_action_authorization(authorization_path)
        self.assertEqual(provider_result["status"], "draft")
        self.assertFalse(provider_result["execution_ready"])
        self.assertFalse(provider_result["network_authorized"])

        with mock.patch(
            "oe_narration.directed_bakeoff._safe_consumption_path"
        ) as consumption_path, mock.patch(
            "oe_narration.directed_bakeoff._safe_new_relative"
        ) as output_path:
            with self.assertRaisesRegex(
                ValidationError,
                "active, execution-ready, network-authorized",
            ):
                validate_directed_bakeoff_execution(authorization_path)
        consumption_path.assert_not_called()
        output_path.assert_not_called()
        self.assertFalse((authorization_path.parent / "consumed").exists())
        self.assertFalse((fixture / "outputs").exists())

    def test_draft_tamper_unknown_field_and_token_drift_fail_before_network(self) -> None:
        for mutation in ("draft", "unknown", "token_drift"):
            with self.subTest(mutation=mutation):
                temporary, fixture, _w = self._copy_system()
                self.addCleanup(temporary.cleanup)
                active = self._activate(fixture)
                if mutation == "draft":
                    authorization = json.loads(active.read_text(encoding="utf-8"))
                    authorization["status"] = "draft"
                    self._write_json(active, authorization)
                else:
                    compiled_path = fixture / "compiled" / "provider-bakeoff-dry-run.json"
                    compiled = json.loads(compiled_path.read_text(encoding="utf-8"))
                    eleven = next(r for r in compiled["requests"] if r["provider"] == "elevenlabs")
                    if mutation == "unknown":
                        eleven["rewrite_allowed"] = True
                    else:
                        eleven["request_body"]["text"] += " drift"
                    self._write_json(compiled_path, compiled)
                    authorization = json.loads(active.read_text(encoding="utf-8"))
                    authorization["bindings"]["compiled_dry_run_sha256"] = sha256_file(compiled_path)
                    self._write_json(active, authorization)
                with mock.patch("oe_narration.directed_bakeoff._post_once") as post:
                    with self.assertRaises(ValidationError):
                        validate_directed_bakeoff_execution(active)
                post.assert_not_called()

    def test_fixed_seed_contract_rejects_missing_range_and_unpaired_values(self) -> None:
        temporary, fixture, _w = self._copy_system()
        self.addCleanup(temporary.cleanup)
        plan_path = fixture / "provider-bakeoff-plan.json"
        original = json.loads(plan_path.read_text(encoding="utf-8"))
        mutations = [
            (0, None, "remove"),
            (0, -1, "set"),
            (2, 303, "set"),
            (1, 2026082401, "set"),
        ]
        for index, value, operation in mutations:
            with self.subTest(index=index, value=value, operation=operation):
                plan = copy.deepcopy(original)
                requests = next(
                    provider["requests"]
                    for provider in plan["providers"]
                    if provider["provider"] == "elevenlabs"
                )
                if operation == "remove":
                    requests[index].pop("fixed_seed")
                else:
                    requests[index]["fixed_seed"] = value
                self._write_json(plan_path, plan)
                with self.assertRaises(ValidationError):
                    dry_run_provider_bakeoff(
                        plan_path,
                        fixture / "performance-envelope.json",
                        _w,
                    )
        self._write_json(plan_path, original)

    def test_missing_credential_does_not_consume_or_create_outputs(self) -> None:
        temporary, fixture, _w = self._copy_system()
        self.addCleanup(temporary.cleanup)
        active = self._activate(fixture)
        consumption = active.parent / "consumed" / "AUTH-test-directed-bakeoff.consumed.json"
        with mock.patch.dict(os.environ, {}, clear=True), mock.patch(
            "oe_narration.directed_bakeoff._post_once"
        ) as post:
            with self.assertRaisesRegex(ValidationError, "ELEVENLABS_API_KEY"):
                execute_directed_bakeoff(active)
        post.assert_not_called()
        self.assertFalse(consumption.exists())
        self.assertFalse((fixture / "outputs").exists())

    def test_consumption_exists_before_first_network_and_seed_is_in_body(self) -> None:
        temporary, fixture, _w = self._copy_system()
        self.addCleanup(temporary.cleanup)
        active = self._activate(fixture)
        consumption = active.parent / "consumed" / "AUTH-test-directed-bakeoff.consumed.json"
        bodies: list[dict] = []

        def fake_post(**kwargs):
            self.assertTrue(consumption.is_file())
            bodies.append(json.loads(kwargs["body"]))
            return self._pcm()

        with mock.patch.dict(os.environ, {"ELEVENLABS_API_KEY": "test-only-key"}), mock.patch(
            "oe_narration.directed_bakeoff._post_once", side_effect=fake_post
        ) as post:
            result = execute_directed_bakeoff(active)
        self.assertEqual(post.call_count, 4)
        self.assertEqual(
            [body["seed"] for body in bodies],
            [2026082401, 2026082402, 2026082401, 2026082402],
        )
        self.assertEqual(result["attempted_calls"], 4)
        self.assertEqual(result["outputs_received"], 4)
        self.assertTrue(result["blind_comparison_eligible"])
        self.assertEqual(result["redirects_followed"], 0)
        self.assertEqual(result["retries_made"], 0)

    def test_success_receipt_keeps_spoken_tag_and_creative_gates_pending(self) -> None:
        temporary, fixture, _w = self._copy_system()
        self.addCleanup(temporary.cleanup)
        active = self._activate(fixture)
        with mock.patch.dict(os.environ, {"ELEVENLABS_API_KEY": "test-only-key"}), mock.patch(
            "oe_narration.directed_bakeoff._post_once", return_value=self._pcm()
        ):
            result = execute_directed_bakeoff(active)
        receipt = json.loads((fixture / result["receipt"]).read_text(encoding="utf-8"))
        self.assertEqual(receipt["lexical_hard_gate"]["status"], "pending")
        self.assertEqual(
            receipt["lexical_hard_gate"]["spoken_direction_tag_risk"], "unresolved"
        )
        self.assertTrue(
            all(item["lexical_hard_gate"]["status"] == "pending" for item in receipt["results"])
        )
        self.assertFalse(receipt["creative_approved"])
        self.assertFalse(receipt["step3_authorized"])
        self.assertFalse(receipt["full_episode_authorized"])

    def test_authorization_is_one_shot(self) -> None:
        temporary, fixture, _w = self._copy_system()
        self.addCleanup(temporary.cleanup)
        active = self._activate(fixture)
        with mock.patch.dict(os.environ, {"ELEVENLABS_API_KEY": "test-only-key"}), mock.patch(
            "oe_narration.directed_bakeoff._post_once", return_value=self._pcm()
        ) as post:
            execute_directed_bakeoff(active)
            with self.assertRaises(ValidationError):
                execute_directed_bakeoff(active)
        self.assertEqual(post.call_count, 4)

    def test_cap_tamper_fails_without_consuming(self) -> None:
        temporary, fixture, _w = self._copy_system()
        self.addCleanup(temporary.cleanup)
        active = self._activate(fixture)
        authorization = json.loads(active.read_text(encoding="utf-8"))
        authorization["authorized_limits"]["max_calls"] = 99
        self._write_json(active, authorization)
        consumption = active.parent / "consumed" / "AUTH-test-directed-bakeoff.consumed.json"
        with mock.patch("oe_narration.directed_bakeoff._post_once") as post:
            with self.assertRaises(ValidationError):
                validate_directed_bakeoff_execution(active)
        post.assert_not_called()
        self.assertFalse(consumption.exists())

    def test_existing_output_and_output_symlink_fail_before_consumption(self) -> None:
        for kind in ("existing", "symlink"):
            with self.subTest(kind=kind):
                temporary, fixture, _w = self._copy_system()
                self.addCleanup(temporary.cleanup)
                active = self._activate(fixture)
                output_root = fixture / "outputs"
                if kind == "existing":
                    path = output_root / "raw" / "elevenlabs" / "P01-S00" / "candidate-A.pcm"
                    path.parent.mkdir(parents=True)
                    path.write_bytes(b"old")
                else:
                    outside = Path(temporary.name) / "outside"
                    outside.mkdir()
                    output_root.mkdir()
                    (output_root / "raw").symlink_to(outside, target_is_directory=True)
                with mock.patch("oe_narration.directed_bakeoff._post_once") as post:
                    with self.assertRaises(ValidationError):
                        validate_directed_bakeoff_execution(active)
                post.assert_not_called()
                self.assertFalse(
                    (active.parent / "consumed" / "AUTH-test-directed-bakeoff.consumed.json").exists()
                )

    def test_consumption_symlink_is_rejected(self) -> None:
        temporary, fixture, _w = self._copy_system()
        self.addCleanup(temporary.cleanup)
        active = self._activate(fixture)
        outside = Path(temporary.name) / "outside"
        outside.mkdir()
        (active.parent / "consumed").symlink_to(outside, target_is_directory=True)
        with self.assertRaises(ValidationError):
            validate_directed_bakeoff_execution(active)

    def test_non_capability_failure_never_falls_back_or_retries(self) -> None:
        temporary, fixture, _w = self._copy_system()
        self.addCleanup(temporary.cleanup)
        active = self._activate(fixture)
        with mock.patch.dict(os.environ, {"ELEVENLABS_API_KEY": "test-only-key"}), mock.patch(
            "oe_narration.directed_bakeoff._post_once",
            side_effect=_HttpFailure("provider_transport_failure"),
        ) as post:
            with self.assertRaisesRegex(ValidationError, "provider_transport_failure"):
                execute_directed_bakeoff(active)
        self.assertEqual(post.call_count, 1)
        failure = fixture / "receipts" / "elevenlabs" / (
            "AUTH-test-directed-bakeoff-directed-bakeoff-failure.json"
        )
        receipt = json.loads(failure.read_text(encoding="utf-8"))
        self.assertEqual(receipt["attempted_calls"], 1)
        self.assertEqual(receipt["retries_made"], 0)

    def test_pcm_capability_receipt_exists_before_sole_mp3_fallback(self) -> None:
        temporary, fixture, _w = self._copy_system()
        self.addCleanup(temporary.cleanup)
        active = self._activate(fixture)
        fallback_receipt = fixture / "receipts" / "elevenlabs" / (
            "AUTH-test-directed-bakeoff-EL-P01-A-pcm-capability-rejection.json"
        )
        calls = 0

        def fake_post(**_kwargs):
            nonlocal calls
            calls += 1
            if calls == 1:
                raise _HttpFailure(
                    "pcm_capability_unavailable",
                    http_status=422,
                    provider_code="unsupported_output_format",
                    response_sha256="a" * 64,
                    pcm_capability_unavailable=True,
                )
            if calls == 2:
                self.assertTrue(fallback_receipt.is_file())
                return _HttpResponse(
                    b"ID3test",
                    "audio/mpeg",
                    {},
                    {},
                    {
                        "header": "character-cost",
                        "present": True,
                        "value": 842,
                        "unit": "provider_reported_character_cost",
                    },
                )
            return self._pcm()

        approved_probe = {
            "is_approved_mp3_fallback": True,
            "container": "mp3",
            "sample_rate_hz": 44_100,
            "channels": 1,
            "bit_rate_bps": 192_000,
        }
        with mock.patch.dict(os.environ, {"ELEVENLABS_API_KEY": "test-only-key"}), mock.patch(
            "oe_narration.directed_bakeoff._post_once", side_effect=fake_post
        ), mock.patch("oe_narration.directed_bakeoff.inspect_audio", return_value=approved_probe):
            result = execute_directed_bakeoff(active)
        self.assertEqual(calls, 5)
        self.assertEqual(result["attempted_calls"], 5)
        self.assertTrue(result["results"][0]["lossy_origin"])
        self.assertFalse(result["results"][0]["comparison_eligible"])
        self.assertFalse(result["blind_comparison_eligible"])
        self.assertEqual(
            result["results"][0]["pcm_capability_failure_receipt"]["state"],
            "documented_before_fallback",
        )

    def test_pcm_mime_alignment_and_container_signatures_fail_closed(self) -> None:
        bad = [
            _HttpResponse(b"\x00\x00", "audio/mpeg", {}, {}, {}),
            _HttpResponse(b"\x00", "application/octet-stream", {}, {}, {}),
            _HttpResponse(b"ID3x", "application/octet-stream", {}, {}, {}),
            _HttpResponse(b"RIFFxxxxWAVE", "application/octet-stream", {}, {}, {}),
        ]
        for response in bad:
            with self.subTest(response=response):
                with self.assertRaises(_HttpFailure):
                    _validate_pcm_response(response)
        _validate_pcm_response(self._pcm())

    def test_mp3_mime_and_signature_fail_closed(self) -> None:
        with self.assertRaises(_HttpFailure):
            _validate_mp3_signature(_HttpResponse(b"ID3x", "application/octet-stream", {}, {}, {}))
        with self.assertRaises(_HttpFailure):
            _validate_mp3_signature(_HttpResponse(b"not-mp3", "audio/mpeg", {}, {}, {}))
        _validate_mp3_signature(_HttpResponse(b"ID3x", "audio/mpeg", {}, {}, {}))

    def test_redirect_is_not_followed_and_http_call_is_not_retried(self) -> None:
        redirect = urllib.error.HTTPError(
            "https://api.elevenlabs.io/v1/text-to-speech/voice",
            302,
            "redirect",
            {"Location": "https://evil.invalid/steal"},
            io.BytesIO(b""),
        )
        opener = mock.Mock()
        opener.open.side_effect = redirect
        with mock.patch("urllib.request.build_opener", return_value=opener):
            with self.assertRaises(_HttpFailure) as caught:
                _post_once(
                    url_path="/v1/text-to-speech/voice",
                    query={"output_format": "pcm_48000"},
                    body=b"{}",
                    api_key="test-only-key",
                    timeout=1,
                )
        self.assertEqual(caught.exception.code, "provider_http_failure")
        self.assertEqual(opener.open.call_count, 1)

    def test_provider_identifiers_and_receipts_never_expose_secret(self) -> None:
        secret = "xi-super-sensitive-test-key"
        identifiers = _provider_identifiers(
            {
                "request-id": f"leak-{secret}",
                "x-request-id": "safe-id",
                "authorization": secret,
            },
            secret,
        )
        self.assertEqual(identifiers, {"x-request-id": "safe-id"})

        temporary, fixture, _w = self._copy_system()
        self.addCleanup(temporary.cleanup)
        active = self._activate(fixture)
        with mock.patch.dict(os.environ, {"ELEVENLABS_API_KEY": secret}), mock.patch(
            "oe_narration.directed_bakeoff._post_once", return_value=self._pcm()
        ):
            result = execute_directed_bakeoff(active)
        receipt_text = (fixture / result["receipt"]).read_text(encoding="utf-8")
        consumption_text = (
            active.parent / "consumed" / "AUTH-test-directed-bakeoff.consumed.json"
        ).read_text(encoding="utf-8")
        self.assertNotIn(secret, receipt_text)
        self.assertNotIn(secret, consumption_text)

    def test_character_cost_is_the_only_recorded_usage_header(self) -> None:
        evidence = _character_cost(
            {
                "character-cost": "3270",
                "x-ratelimit-remaining": "99",
                "authorization": "not-recorded",
            },
            "test-only-key",
        )
        self.assertEqual(
            evidence,
            {
                "header": "character-cost",
                "present": True,
                "value": 3270,
                "unit": "provider_reported_character_cost",
            },
        )
        with self.assertRaises(_HttpFailure):
            _character_cost({"character-cost": "3.5"}, "test-only-key")
        with self.assertRaises(_HttpFailure):
            _character_cost({"character-cost": "test-only-key"}, "test-only-key")

    def test_episode_target_is_refused_as_full_episode_scope(self) -> None:
        temporary, fixture, _w = self._copy_system()
        self.addCleanup(temporary.cleanup)
        active = self._activate(fixture)
        authorization = json.loads(active.read_text(encoding="utf-8"))
        authorization["target"]["kind"] = "episode"
        self._write_json(active, authorization)
        with self.assertRaises(ValidationError):
            validate_directed_bakeoff_execution(active)


if __name__ == "__main__":
    unittest.main()
