"""Context is authored, preserved, and checked; it is never inferred by validation."""

from __future__ import annotations

import copy
import json

import pytest

from blueprint_cinema.hashes import sha256_file, write_json_atomic
from blueprint_cinema.scene_prompts import build_scene_prompts
from blueprint_cinema.validation import ValidationFailure, validate_scene_directions
from test_scene_prompts import _direction_fixture


def _validate(directions, artifacts, identity, episode_path):
    validate_scene_directions(
        directions,
        artifacts["input-lock.json"],
        artifacts["episode-engine.json"],
        artifacts["world.json"],
        artifacts["visual-plan.json"],
        artifacts["asset-tickets.json"],
        identity,
        lock_hash=sha256_file(episode_path / "input-lock.json"),
        engine_hash=sha256_file(episode_path / "episode-engine.json"),
        world_hash=sha256_file(episode_path / "world.json"),
        plan_hash=sha256_file(episode_path / "visual-plan.json"),
    )


def _human_fixture(artifacts, identity, episode_path):
    # Mechanical contract fixture using existing test-world IDs and locked timing.
    # It is not a production direction, approved performance, or narration-fit verdict.
    directions = _direction_fixture(artifacts, identity, episode_path)
    seq = directions["sequences"][0]
    seq["scene_context"] = {
        "situation": "An inn owner recognizes a returning guest during a booking conversation.",
        "scene_form": "narrated dramatization",
        "form_reason": "The illustrative interaction supplies human context for the booking route.",
        "stakes": "The recurring relationship matters to the independent inn.",
        "emotional_arc": "Recognition becomes attention; no hostile conflict is introduced.",
    }
    shot = seq["shots"][0]
    shot["mode"] = "reality"
    shot["production_lane"] = "ai_environmental_plate"
    shot["purpose"] = "Show recognition between an inn owner and returning guest without claiming a real case."
    shot["camera"] = {
        "framing": "close", "movement": "locked",
        "start_description": "The owner looks toward the guest across the same reception counter.",
        "end_description": "The owner's small recognition smile resolves into attentive listening.",
    }
    shot["editorial_intent"] = {
        "techniques": ["motivated owner close-up", "uninterrupted reaction"],
        "why_this_shot": "Recognition is legible in the owner's face before the explanation resumes.",
        "entry_trigger": "Enter before the owner recognizes the returning guest.",
        "exit_trigger": "Leave after the recognition and attention change can be read.",
        "hold_intent": "Preserve the small recognition change instead of cutting through it.",
        "alternative_considered": "A counter insert would remove the human relationship.",
        "review_question": "Does the actual track explain the interaction without unheard exact words?",
    }
    shot["composition"] = {
        "background": "paper", "primary_layer_id": "layer-plate",
        "visual_hierarchy": ["layer-plate"],
        "layers": [{
            "id": "layer-plate", "kind": "footage",
            "source": {"type": "asset_ticket", "ref_id": "ticket-inn-reality"},
            "start_bounds": {"x": 0, "y": 0, "width": 1920, "height": 1080},
            "end_bounds": {"x": 0, "y": 0, "width": 1920, "height": 1080},
            "z_index": 0, "start_opacity": 1, "end_opacity": 1,
            "state_before": "owner notices guest", "state_after": "owner recognizes guest",
            "visual_role": "primary_subject",
        }],
    }
    beat = shot["motion_beats"][0]
    beat.update({"id": "motion-observe-recognition", "verb": "hold", "changes": [],
                 "target_layer_ids": ["layer-plate"], "easing": "hold",
                 "purpose": "Let the generated performance carry the change without added graphic motion."})
    shot["transition_in"] = {"type": "cut", "duration_seconds": 0, "preserve_layer_ids": [],
                             "description": "Cut to the owner before recognition begins."}
    shot["transition_out"] = {"type": "cut", "duration_seconds": 0, "preserve_layer_ids": [],
                              "description": "Cut after the recognition change has resolved."}
    shot["direction_facts"] = {
        "what_stays_still": "The counter, camera, wardrobe and guest position remain stable.",
        "master_setup_relationship": {"role": "setup", "master_reference_id": "ticket-inn-reality",
                                      "description": "Derive the owner's closer setup from the ticketed inn master."},
        "screen_direction": {"action_line": "owner to guest across the counter", "camera_side": "owner-left side",
                             "subject_direction": "The owner looks screen right toward the guest."},
        "continuity_anchors": [{"id": "ticket-inn-reality", "kind": "asset_ticket",
                                "description": "Keep the same owner, guest, wardrobe and counter as the master."}],
        "initial_image": shot["camera"]["start_description"],
        "final_image": shot["camera"]["end_description"],
    }
    shot["picture_audio_contract"] = {
        "mode": "narrated_dramatization", "language_carrier": "narrator",
        "visible_speech": "illustrative_only", "coverage_grammar": "motivated_interaction",
        "face_function": "dramatic_performance",
        "physical_action": "The owner recognizes the guest, acknowledges them briefly and then listens.",
        "mute_test": {"missing_line_expected": True,
                      "reason": "The greeting may look conversational; the actual narration supplies its meaning."},
        "dramatization_context": {
            "representation": "illustrative", "essential_meaning": "narration",
            "disclosure_plan": "Identify this as an illustrative reconstruction, never a verified real case.",
            "audio_review_check": "Watch the selected window with locked VO; reject if unavailable words carry essential meaning.",
        },
    }
    return directions


@pytest.mark.parametrize("missing_line", [False, True])
@pytest.mark.parametrize("speech", ["illustrative_only", "prohibited"])
def test_dramatization_accepts_motivated_human_close_and_honest_mute_diagnostic(
    missing_line, speech, current_artifacts, identity, episode_path
):
    directions = _human_fixture(current_artifacts, identity, episode_path)
    audio = directions["sequences"][0]["shots"][0]["picture_audio_contract"]
    audio["visible_speech"] = speech
    audio["mute_test"]["missing_line_expected"] = missing_line
    before = copy.deepcopy(directions)
    _validate(directions, current_artifacts, identity, episode_path)
    assert directions == before  # validation must not choose or repair direction


@pytest.mark.parametrize("field,value", [
    ("language_carrier", "scene_participant"),
    ("visible_speech", "required"), ("visible_speech", "source_synced"),
    ("coverage_grammar", "dialogue_exchange"),
    ("face_function", "source_delivery"), ("face_function", "sync_delivery"),
    ("face_function", "presenter_delivery"),
])
def test_dramatization_rejects_sync_and_source_escape_hatches(
    field, value, current_artifacts, identity, episode_path
):
    directions = _human_fixture(current_artifacts, identity, episode_path)
    directions["sequences"][0]["shots"][0]["picture_audio_contract"][field] = value
    with pytest.raises(ValidationFailure):
        _validate(directions, current_artifacts, identity, episode_path)


@pytest.mark.parametrize("field,value", [
    ("narration", False), ("dialogue", "sync_scripted"),
    ("dialogue", "sync_source"), ("dialogue", "presenter"),
])
def test_dramatization_keeps_narrator_and_no_character_dialogue(
    field, value, current_artifacts, identity, episode_path
):
    directions = _human_fixture(current_artifacts, identity, episode_path)
    directions["sequences"][0]["shots"][0]["sound_intent"][field] = value
    with pytest.raises(ValidationFailure):
        _validate(directions, current_artifacts, identity, episode_path)


@pytest.mark.parametrize("path", [
    ("scene_context",), ("scene_context", "form_reason"), ("scene_context", "stakes"),
    ("shots", 0, "editorial_intent"), ("shots", 0, "editorial_intent", "hold_intent"),
    ("shots", 0, "editorial_intent", "alternative_considered"),
    ("shots", 0, "picture_audio_contract", "dramatization_context"),
    ("shots", 0, "picture_audio_contract", "dramatization_context", "disclosure_plan"),
    ("shots", 0, "picture_audio_contract", "dramatization_context", "audio_review_check"),
])
def test_required_context_is_not_guessed(path, current_artifacts, identity, episode_path):
    directions = _human_fixture(current_artifacts, identity, episode_path)
    target = directions["sequences"][0]
    for key in path[:-1]:
        target = target[key]
    del target[path[-1]]
    before = copy.deepcopy(directions)
    with pytest.raises(ValidationFailure):
        _validate(directions, current_artifacts, identity, episode_path)
    assert directions == before


@pytest.mark.parametrize("field,value", [("representation", "evidence"), ("essential_meaning", "unheard_dialogue")])
def test_dramatization_cannot_claim_evidence_or_depend_on_unheard_words(
    field, value, current_artifacts, identity, episode_path
):
    directions = _human_fixture(current_artifacts, identity, episode_path)
    directions["sequences"][0]["shots"][0]["picture_audio_contract"]["dramatization_context"][field] = value
    with pytest.raises(ValidationFailure):
        _validate(directions, current_artifacts, identity, episode_path)


def test_context_and_editorial_choices_survive_deterministic_compile(
    tmp_path, current_artifacts, identity, episode_path
):
    directions = _human_fixture(current_artifacts, identity, episode_path)
    _validate(directions, current_artifacts, identity, episode_path)
    write_json_atomic(tmp_path / "scene-directions.json", directions)
    first = build_scene_prompts(identity, tmp_path, directions)
    hashes = [sha256_file(path) for path in first]
    second = build_scene_prompts(identity, tmp_path, directions)
    assert hashes == [sha256_file(path) for path in second]
    prompt = first[1].read_text(encoding="utf-8")
    blocks = [json.loads(part.split("\n```", 1)[0]) for part in prompt.split("```json\n")[1:]]
    seq = directions["sequences"][0]
    assert seq["scene_context"] in blocks
    assert seq["shots"][0] in blocks
    assert next(block for block in blocks if block.get("id") == "shot-001")["editorial_intent"] == seq["shots"][0]["editorial_intent"]


@pytest.mark.parametrize("malformed", [None, [], "not an object"])
def test_malformed_dramatization_returns_controlled_validation_error(
    malformed, current_artifacts, identity, episode_path
):
    directions = _human_fixture(current_artifacts, identity, episode_path)
    directions["sequences"][0]["shots"][0]["picture_audio_contract"]["dramatization_context"] = malformed
    with pytest.raises(ValidationFailure, match="dramatization_context"):
        _validate(directions, current_artifacts, identity, episode_path)


def test_legacy_direction_needs_deliberate_reauthoring(current_artifacts, identity, episode_path):
    legacy = _direction_fixture(current_artifacts, identity, episode_path)
    legacy["schema_version"] = "1.1.0"
    del legacy["sequences"][0]["scene_context"]
    del legacy["sequences"][0]["shots"][0]["editorial_intent"]
    before = copy.deepcopy(legacy)
    with pytest.raises(ValidationFailure, match="1.2.0"):
        _validate(legacy, current_artifacts, identity, episode_path)
    assert legacy == before
