from __future__ import annotations

import copy
import json

import pytest

from blueprint_cinema.hashes import sha256_file, write_json_atomic
from blueprint_cinema.scene_prompts import FRAME_CONTRACT, build_director_prompts, build_scene_prompts
from blueprint_cinema.validation import ValidationFailure, load_json, validate_scene_directions


def _direction_fixture(current_artifacts, identity, episode_path):
    words_artifact = next(
        item
        for item in current_artifacts["input-lock.json"]["artifacts"]
        if item["role"] == "word_transcript"
    )
    words_path = episode_path.parents[2] / words_artifact["path"]
    words = json.loads(words_path.read_text(encoding="utf-8"))
    unit = current_artifacts["visual-plan.json"]["units"][0]
    sequence_units = [
        item
        for item in current_artifacts["visual-plan.json"]["units"]
        if item["sequence_id"] == unit["sequence_id"]
    ]
    sequence_out = sequence_units[-1]["out"]
    word_start = sequence_units[0]["narration_anchor"]["word_start"]
    word_end = sequence_units[-1]["narration_anchor"]["word_end"]
    quote = " ".join(word["word"] for word in words[word_start : word_end + 1])
    cue_time = float(words[word_start]["start"])
    return {
        "$schema": "../../schemas/scene-directions.schema.json",
        "schema_version": "1.2.0",
        "workflow_version": "blueprint-cinema-1.0",
        **identity.as_dict(),
        "input_lock_sha256": sha256_file(episode_path / "input-lock.json"),
        "episode_engine_sha256": sha256_file(episode_path / "episode-engine.json"),
        "world_sha256": sha256_file(episode_path / "world.json"),
        "visual_plan_sha256": sha256_file(episode_path / "visual-plan.json"),
        "scope": {"in": 0.0, "out": sequence_out, "sequence_ids": [unit["sequence_id"]]},
        "frame_contract": FRAME_CONTRACT,
        "sequences": [
            {
                "id": unit["sequence_id"],
                "in": 0.0,
                "out": sequence_out,
                "unit_ids": [item["id"] for item in sequence_units],
                "narration_anchor": {"word_start": word_start, "word_end": word_end, "quote": quote},
                "audience_inference": "The same hotel is paying an intermediary cost to meet a guest it has already served.",
                "scene_context": {
                    "situation": "A returning guest books through an intermediary.",
                    "scene_form": "graphic explanation",
                    "form_reason": "The invisible route and its cost need a stable spatial model.",
                    "stakes": "The hotel pays an intermediary for a returning guest.",
                    "emotional_arc": "Recognition becomes understanding; no enacted conflict is needed.",
                },
                "visual_sentence": {
                    "subject_ids": ["stay-key-tag"],
                    "relationship": "travels through the useful OTA booking route",
                    "object_ids": ["ota-booking-gate", "hotel-stay-node"],
                    "consequence": "A visible commission token leaves the independent hotel after the booking.",
                    "before": "The recurring guest has not yet entered the booking route.",
                    "after": "The guest reaches the hotel and the booking has produced a visible cost.",
                },
                "continuity": {
                    "inherits_object_ids": [],
                    "introduces_object_ids": ["stay-key-tag", "ota-booking-gate", "hotel-stay-node"],
                    "retires_object_ids": [],
                    "end_frame_handoff": "Hold the same guest, OTA gate, and hotel positions for the evidence sequence that follows.",
                },
                "shots": [
                    {
                        "id": "shot-001",
                        "in": 0.0,
                        "out": sequence_out,
                        "narration_anchor": {"word_start": word_start, "word_end": word_end, "quote": quote},
                        "mode": "system",
                        "production_lane": "motion_graphics",
                        "purpose": "Show one guest moving through the OTA gate and make the resulting hotel cost visible.",
                        "editorial_intent": {
                            "techniques": ["stable explanatory wide", "continuous route"],
                            "why_this_shot": "Keep the full short route visible to connect booking and cost.",
                            "entry_trigger": "The narration introduces the returning guest.",
                            "exit_trigger": "The commission consequence has become readable.",
                            "hold_intent": "Hold the resulting cost before the next proof sequence.",
                            "alternative_considered": "Separate node close-ups would hide the relationship.",
                            "review_question": "Can the viewer follow the same guest and identify who pays?",
                        },
                        "camera": {
                            "framing": "wide",
                            "movement": "locked",
                            "start_description": "Guest left, OTA gate centered, and hotel right with generous negative space.",
                            "end_description": "The same spatial arrangement remains while the commission consequence is visible.",
                        },
                        "composition": {
                            "background": "paper",
                            "primary_layer_id": "layer-guest",
                            "visual_hierarchy": ["layer-guest", "layer-route", "layer-ota", "layer-hotel"],
                            "layers": [
                                {
                                    "id": "layer-guest",
                                    "kind": "actor",
                                    "source": {"type": "world_object", "ref_id": "stay-key-tag"},
                                    "start_bounds": {"x": 150, "y": 390, "width": 180, "height": 180},
                                    "end_bounds": {"x": 1420, "y": 390, "width": 180, "height": 180},
                                    "z_index": 3,
                                    "start_opacity": 1,
                                    "end_opacity": 1,
                                    "state_before": "initial",
                                    "state_after": "active",
                                    "visual_role": "primary_subject",
                                },
                                {
                                    "id": "layer-route",
                                    "kind": "route",
                                    "source": {"type": "primitive"},
                                    "start_bounds": {"x": 300, "y": 460, "width": 1180, "height": 20},
                                    "end_bounds": {"x": 300, "y": 460, "width": 1180, "height": 20},
                                    "z_index": 1,
                                    "start_opacity": 0.35,
                                    "end_opacity": 1,
                                    "state_before": "idle",
                                    "state_after": "traced",
                                    "visual_role": "relationship",
                                },
                                {
                                    "id": "layer-ota",
                                    "kind": "object",
                                    "source": {"type": "world_object", "ref_id": "ota-booking-gate"},
                                    "start_bounds": {"x": 830, "y": 330, "width": 260, "height": 300},
                                    "end_bounds": {"x": 830, "y": 330, "width": 260, "height": 300},
                                    "z_index": 2,
                                    "start_opacity": 1,
                                    "end_opacity": 1,
                                    "state_before": "initial",
                                    "state_after": "active",
                                    "visual_role": "relationship",
                                },
                                {
                                    "id": "layer-hotel",
                                    "kind": "object",
                                    "source": {"type": "world_object", "ref_id": "hotel-stay-node"},
                                    "start_bounds": {"x": 1500, "y": 330, "width": 280, "height": 300},
                                    "end_bounds": {"x": 1500, "y": 330, "width": 280, "height": 300},
                                    "z_index": 2,
                                    "start_opacity": 1,
                                    "end_opacity": 1,
                                    "state_before": "initial",
                                    "state_after": "active",
                                    "visual_role": "consequence",
                                },
                            ],
                        },
                        "text_elements": [],
                        "motion_beats": [
                            {
                                "id": "motion-guest-route",
                                "at_seconds": cue_time,
                                "duration_seconds": 2.0,
                                "cue": {"word_index": word_start, "word": words[word_start]["word"], "cue_time_seconds": cue_time},
                                "verb": "move",
                                "target_layer_ids": ["layer-guest", "layer-route"],
                                "changes": [
                                    {"property": "x", "from": 150, "to": 1420},
                                    {"property": "path_progress", "from": 0, "to": 1}
                                ],
                                "easing": "ease_in_out",
                                "purpose": "Make the booking relationship and direction of travel visible.",
                            }
                        ],
                        "transition_in": {"type": "cut", "duration_seconds": 0, "preserve_layer_ids": [], "description": "Open directly on the three-part route."},
                        "transition_out": {"type": "hold", "duration_seconds": 0.4, "preserve_layer_ids": ["layer-guest", "layer-ota", "layer-hotel"], "description": "Hold the route so the next proof shot can inherit its geography."},
                        "evidence_choreography": [],
                        "asset_ticket_ids": ["ticket-inn-reality"],
                        "picture_audio_contract": {
                            "mode": "silent_graphic",
                            "language_carrier": "narrator",
                            "visible_speech": "not_applicable",
                            "coverage_grammar": "graphic_progression",
                            "face_function": "none",
                            "physical_action": "The guest token crosses the route and exposes the commission consequence.",
                            "mute_test": {
                                "missing_line_expected": False,
                                "reason": "The graphic operation remains complete without performed speech.",
                            },
                        },
                        "direction_facts": {
                            "what_stays_still": "The OTA gate and hotel remain fixed while the guest token moves.",
                            "master_setup_relationship": {
                                "role": "standalone",
                                "master_reference_id": None,
                                "description": "This system composition does not derive from filmed master coverage.",
                            },
                            "screen_direction": {
                                "action_line": "not_applicable",
                                "camera_side": "not_applicable",
                                "subject_direction": "Guest moves consistently from screen left toward screen right.",
                            },
                            "continuity_anchors": [
                                {
                                    "id": "stay-key-tag",
                                    "kind": "world_object",
                                    "description": "The same guest token persists through the route.",
                                }
                            ],
                            "initial_image": "Guest token waits left of the fixed OTA gate and hotel.",
                            "final_image": "Guest reaches the hotel while the commission consequence remains visible.",
                        },
                        "sound_intent": {
                            "narration": True,
                            "dialogue": "none",
                            "ambience": "none",
                            "music": False,
                            "sound_design": False,
                            "notes": "Greybox uses locked narration only.",
                        },
                    }
                ],
                "negative_constraints": [
                    "Do not show the complete world map.",
                    "Do not add decorative camera drift.",
                    "Do not represent the guest as a new person on the return loop."
                ],
                "review_checks": [
                    "The recurring guest is the first visible priority.",
                    "The OTA is visibly a route rather than a villain.",
                    "The hotel remains recognizable on the right.",
                    "The guest movement has one clear direction.",
                    "The exit frame can carry into the next proof shot."
                ],
            }
        ],
        "status": "ready_for_prompt_compile",
    }


def test_director_packets_are_deterministic_and_contain_production_precision(
    tmp_path, current_artifacts, identity, episode_path
):
    copied_episode = tmp_path / identity.folder_name
    copied_episode.mkdir()
    for name, value in current_artifacts.items():
        write_json_atomic(copied_episode / name, value)
    first = build_director_prompts(
        identity,
        copied_episode,
        current_artifacts["input-lock.json"],
        current_artifacts["episode-engine.json"],
        current_artifacts["world.json"],
        current_artifacts["visual-plan.json"],
        current_artifacts["asset-tickets.json"],
        sequence_ids=["sequence-hook-01"],
    )
    first_hashes = [sha256_file(path) for path in first]
    second = build_director_prompts(
        identity,
        copied_episode,
        current_artifacts["input-lock.json"],
        current_artifacts["episode-engine.json"],
        current_artifacts["world.json"],
        current_artifacts["visual-plan.json"],
        current_artifacts["asset-tickets.json"],
        sequence_ids=["sequence-hook-01"],
    )
    assert first_hashes == [sha256_file(path) for path in second]
    prompt = first[1].read_text(encoding="utf-8")
    assert "exact 1920x1080 pixel bounds" in prompt
    assert "timed word or number highlight" in prompt
    assert "Every motion beat's cue word index" in prompt
    assert "The default transition is a cut" in prompt
    assert "picture/audio mode" in prompt
    assert "scene_context" in prompt and "editorial_intent" in prompt
    assert "what stays still" in prompt
    assert "declared master-shot or listed asset-ticket reference" in prompt
    assert "exact initial and final images" in prompt
    assert "Hotels keep paying to meet the SAME guest" in prompt


def test_unknown_director_sequence_is_rejected(tmp_path, current_artifacts, identity):
    with pytest.raises(ValueError, match="unknown sequence"):
        build_director_prompts(
            identity,
            tmp_path,
            current_artifacts["input-lock.json"],
            current_artifacts["episode-engine.json"],
            current_artifacts["world.json"],
            current_artifacts["visual-plan.json"],
            current_artifacts["asset-tickets.json"],
            sequence_ids=["sequence-missing-99"],
        )


def test_scene_direction_validation_and_build_prompt_compile(
    tmp_path, current_artifacts, identity, episode_path
):
    directions = _direction_fixture(current_artifacts, identity, episode_path)
    validate_scene_directions(
        directions,
        current_artifacts["input-lock.json"],
        current_artifacts["episode-engine.json"],
        current_artifacts["world.json"],
        current_artifacts["visual-plan.json"],
        current_artifacts["asset-tickets.json"],
        identity,
        lock_hash=sha256_file(episode_path / "input-lock.json"),
        engine_hash=sha256_file(episode_path / "episode-engine.json"),
        world_hash=sha256_file(episode_path / "world.json"),
        plan_hash=sha256_file(episode_path / "visual-plan.json"),
    )
    write_json_atomic(tmp_path / "scene-directions.json", directions)
    outputs = build_scene_prompts(identity, tmp_path, directions)
    assert len(outputs) == 2
    prompt = outputs[1].read_text(encoding="utf-8")
    assert "Treat every coordinate, timestamp" in prompt
    assert "motion-guest-route" in prompt
    assert "150" in prompt and "1420" in prompt
    assert "Production lane: `motion_graphics`" in prompt
    assert '"mode": "silent_graphic"' in prompt
    assert "Obey the declared picture/audio contract" in prompt
    assert '"what_stays_still"' in prompt
    assert "Implement the declared direction facts exactly" in prompt


@pytest.mark.parametrize(
    ("picture_audio", "sound_intent"),
    [
        (
            {
                "mode": "narrated_observation",
                "language_carrier": "narrator",
                "visible_speech": "prohibited",
                "coverage_grammar": "observational_action",
                "face_function": "task_focus",
                "physical_action": "The operator checks one record while the buyer observes the process.",
                "mute_test": {
                    "missing_line_expected": False,
                    "reason": "The visible task resolves without an unheard exchange.",
                },
            },
            {
                "narration": True,
                "dialogue": "none",
                "ambience": "designed_post",
                "music": False,
                "sound_design": True,
                "notes": "Narration leads while restrained room tone supports the task.",
            },
        ),
        (
            {
                "mode": "sync_dialogue",
                "language_carrier": "scene_participant",
                "visible_speech": "required",
                "coverage_grammar": "dialogue_exchange",
                "face_function": "sync_delivery",
                "physical_action": "The owner answers the buyer while both remain across the same table.",
                "mute_test": {
                    "missing_line_expected": True,
                    "reason": "The exchange intentionally depends on audible synchronized speech.",
                },
            },
            {
                "narration": False,
                "dialogue": "sync_scripted",
                "ambience": "source",
                "music": False,
                "sound_design": False,
                "notes": "The approved synchronized exchange carries the shot.",
            },
        ),
        (
            {
                "mode": "presenter_address",
                "language_carrier": "presenter",
                "visible_speech": "required",
                "coverage_grammar": "direct_address",
                "face_function": "presenter_delivery",
                "physical_action": "The presenter addresses camera and completes the approved explanation.",
                "mute_test": {
                    "missing_line_expected": True,
                    "reason": "Direct address intentionally depends on audible synchronized delivery.",
                },
            },
            {
                "narration": False,
                "dialogue": "presenter",
                "ambience": "source",
                "music": False,
                "sound_design": False,
                "notes": "The presenter voice is the primary language source.",
            },
        ),
        (
            {
                "mode": "natural_sound_observation",
                "language_carrier": "natural_sound",
                "visible_speech": "source_synced",
                "coverage_grammar": "natural_sound_action",
                "face_function": "source_delivery",
                "physical_action": "The operator describes the record while keeping one finger on its unresolved line.",
                "mute_test": {
                    "missing_line_expected": True,
                    "reason": "The source interview line is intentionally audible and synchronized.",
                },
            },
            {
                "narration": False,
                "dialogue": "sync_source",
                "ambience": "source",
                "music": False,
                "sound_design": False,
                "notes": "Synchronized source delivery and room sound carry the moment.",
            },
        ),
        (
            {
                "mode": "natural_sound_observation",
                "language_carrier": "natural_sound",
                "visible_speech": "prohibited",
                "coverage_grammar": "natural_sound_action",
                "face_function": "task_focus",
                "physical_action": "The operator turns one page while room tone and paper movement carry the moment.",
                "mute_test": {
                    "missing_line_expected": False,
                    "reason": "The observed task remains complete without any structurally required line.",
                },
            },
            {
                "narration": False,
                "dialogue": "none",
                "ambience": "source",
                "music": False,
                "sound_design": False,
                "notes": "Only the observed page turn and room source sound are audible.",
            },
        ),
        (
            {
                "mode": "silent_graphic",
                "language_carrier": "none",
                "visible_speech": "not_applicable",
                "coverage_grammar": "graphic_progression",
                "face_function": "none",
                "physical_action": "The resolved route remains still long enough for the relationship to register.",
                "mute_test": {
                    "missing_line_expected": False,
                    "reason": "No performed language or missing exchange is implied.",
                },
            },
            {
                "narration": False,
                "dialogue": "none",
                "ambience": "none",
                "music": False,
                "sound_design": False,
                "notes": "The deliberate graphic hold is silent.",
            },
        ),
    ],
)
def test_scene_direction_accepts_each_picture_audio_mode(
    picture_audio,
    sound_intent,
    current_artifacts,
    identity,
    episode_path,
):
    directions = _direction_fixture(current_artifacts, identity, episode_path)
    shot = directions["sequences"][0]["shots"][0]
    shot["picture_audio_contract"] = picture_audio
    shot["sound_intent"] = sound_intent
    validate_scene_directions(
        directions,
        current_artifacts["input-lock.json"],
        current_artifacts["episode-engine.json"],
        current_artifacts["world.json"],
        current_artifacts["visual-plan.json"],
        current_artifacts["asset-tickets.json"],
        identity,
        lock_hash=sha256_file(episode_path / "input-lock.json"),
        engine_hash=sha256_file(episode_path / "episode-engine.json"),
        world_hash=sha256_file(episode_path / "world.json"),
        plan_hash=sha256_file(episode_path / "visual-plan.json"),
    )


def test_scene_direction_accepts_setup_bound_to_listed_master_ticket(
    current_artifacts, identity, episode_path
):
    directions = _direction_fixture(current_artifacts, identity, episode_path)
    shot = directions["sequences"][0]["shots"][0]
    shot["direction_facts"]["master_setup_relationship"] = {
        "role": "setup",
        "master_reference_id": "ticket-inn-reality",
        "description": "This setup derives its geography from the listed master plate ticket.",
    }
    validate_scene_directions(
        directions,
        current_artifacts["input-lock.json"],
        current_artifacts["episode-engine.json"],
        current_artifacts["world.json"],
        current_artifacts["visual-plan.json"],
        current_artifacts["asset-tickets.json"],
        identity,
        lock_hash=sha256_file(episode_path / "input-lock.json"),
        engine_hash=sha256_file(episode_path / "episode-engine.json"),
        world_hash=sha256_file(episode_path / "world.json"),
        plan_hash=sha256_file(episode_path / "visual-plan.json"),
    )


def test_scene_direction_rejects_source_delivery_under_narration(
    current_artifacts, identity, episode_path
):
    directions = _direction_fixture(current_artifacts, identity, episode_path)
    shot = directions["sequences"][0]["shots"][0]
    shot["picture_audio_contract"]["mode"] = "narrated_observation"
    shot["picture_audio_contract"]["language_carrier"] = "narrator"
    shot["picture_audio_contract"]["visible_speech"] = "prohibited"
    shot["picture_audio_contract"]["coverage_grammar"] = "observational_action"
    shot["picture_audio_contract"]["face_function"] = "source_delivery"
    shot["picture_audio_contract"]["mute_test"] = {
        "missing_line_expected": False,
        "reason": "The narrator is the only approved language carrier in this shot.",
    }
    with pytest.raises(
        ValidationFailure,
        match="source_delivery is permitted only for natural_sound_observation",
    ):
        validate_scene_directions(
            directions,
            current_artifacts["input-lock.json"],
            current_artifacts["episode-engine.json"],
            current_artifacts["world.json"],
            current_artifacts["visual-plan.json"],
            current_artifacts["asset-tickets.json"],
            identity,
            lock_hash=sha256_file(episode_path / "input-lock.json"),
            engine_hash=sha256_file(episode_path / "episode-engine.json"),
            world_hash=sha256_file(episode_path / "world.json"),
            plan_hash=sha256_file(episode_path / "visual-plan.json"),
        )


def test_scene_direction_rejects_source_delivery_without_source_audio(
    current_artifacts, identity, episode_path
):
    directions = _direction_fixture(current_artifacts, identity, episode_path)
    shot = directions["sequences"][0]["shots"][0]
    shot["picture_audio_contract"] = {
        "mode": "natural_sound_observation",
        "language_carrier": "natural_sound",
        "visible_speech": "source_synced",
        "coverage_grammar": "natural_sound_action",
        "face_function": "source_delivery",
        "physical_action": "The operator names the unresolved line while holding the source record.",
        "mute_test": {
            "missing_line_expected": True,
            "reason": "The approved source line is intentionally missing when the shot is muted.",
        },
    }
    shot["sound_intent"] = {
        "narration": False,
        "dialogue": "none",
        "ambience": "source",
        "music": False,
        "sound_design": False,
        "notes": "This deliberately broken case omits the synchronized source line.",
    }
    with pytest.raises(
        ValidationFailure,
        match="source_synced visible speech requires sound_intent.dialogue='sync_source'",
    ):
        validate_scene_directions(
            directions,
            current_artifacts["input-lock.json"],
            current_artifacts["episode-engine.json"],
            current_artifacts["world.json"],
            current_artifacts["visual-plan.json"],
            current_artifacts["asset-tickets.json"],
            identity,
            lock_hash=sha256_file(episode_path / "input-lock.json"),
            engine_hash=sha256_file(episode_path / "episode-engine.json"),
            world_hash=sha256_file(episode_path / "world.json"),
            plan_hash=sha256_file(episode_path / "visual-plan.json"),
        )


@pytest.mark.parametrize(
    "missing_field",
    [
        "what_stays_still",
        "master_setup_relationship",
        "screen_direction",
        "continuity_anchors",
        "initial_image",
        "final_image",
    ],
)
def test_scene_direction_rejects_missing_required_direction_fact(
    missing_field, current_artifacts, identity, episode_path
):
    directions = _direction_fixture(current_artifacts, identity, episode_path)
    del directions["sequences"][0]["shots"][0]["direction_facts"][missing_field]
    with pytest.raises(
        ValidationFailure,
        match=rf"'{missing_field}' is a required property",
    ):
        validate_scene_directions(
            directions,
            current_artifacts["input-lock.json"],
            current_artifacts["episode-engine.json"],
            current_artifacts["world.json"],
            current_artifacts["visual-plan.json"],
            current_artifacts["asset-tickets.json"],
            identity,
            lock_hash=sha256_file(episode_path / "input-lock.json"),
            engine_hash=sha256_file(episode_path / "episode-engine.json"),
            world_hash=sha256_file(episode_path / "world.json"),
            plan_hash=sha256_file(episode_path / "visual-plan.json"),
        )


def test_scene_direction_rejects_unknown_setup_master_reference(
    current_artifacts, identity, episode_path
):
    directions = _direction_fixture(current_artifacts, identity, episode_path)
    directions["sequences"][0]["shots"][0]["direction_facts"][
        "master_setup_relationship"
    ] = {
        "role": "setup",
        "master_reference_id": "master-missing",
        "description": "This setup claims a master reference that does not exist.",
    }
    with pytest.raises(
        ValidationFailure,
        match="setup has unknown master reference master-missing",
    ):
        validate_scene_directions(
            directions,
            current_artifacts["input-lock.json"],
            current_artifacts["episode-engine.json"],
            current_artifacts["world.json"],
            current_artifacts["visual-plan.json"],
            current_artifacts["asset-tickets.json"],
            identity,
            lock_hash=sha256_file(episode_path / "input-lock.json"),
            engine_hash=sha256_file(episode_path / "episode-engine.json"),
            world_hash=sha256_file(episode_path / "world.json"),
            plan_hash=sha256_file(episode_path / "visual-plan.json"),
        )


def test_scene_direction_rejects_setup_reference_that_is_not_a_master(
    current_artifacts, identity, episode_path
):
    directions = _direction_fixture(current_artifacts, identity, episode_path)
    directions["sequences"][0]["shots"][0]["direction_facts"][
        "master_setup_relationship"
    ] = {
        "role": "setup",
        "master_reference_id": "shot-001",
        "description": "This invalid setup points to itself instead of a declared master shot.",
    }
    with pytest.raises(
        ValidationFailure,
        match="setup references shot shot-001 that is not declared as a master",
    ):
        validate_scene_directions(
            directions,
            current_artifacts["input-lock.json"],
            current_artifacts["episode-engine.json"],
            current_artifacts["world.json"],
            current_artifacts["visual-plan.json"],
            current_artifacts["asset-tickets.json"],
            identity,
            lock_hash=sha256_file(episode_path / "input-lock.json"),
            engine_hash=sha256_file(episode_path / "episode-engine.json"),
            world_hash=sha256_file(episode_path / "world.json"),
            plan_hash=sha256_file(episode_path / "visual-plan.json"),
        )


def test_scene_direction_rejects_dangling_continuity_anchor(
    current_artifacts, identity, episode_path
):
    directions = _direction_fixture(current_artifacts, identity, episode_path)
    directions["sequences"][0]["shots"][0]["direction_facts"]["continuity_anchors"] = [
        {
            "id": "missing-object",
            "kind": "world_object",
            "description": "The claimed persistent object is absent from the approved world.",
        }
    ]
    with pytest.raises(
        ValidationFailure,
        match="dangling world-object continuity anchor missing-object",
    ):
        validate_scene_directions(
            directions,
            current_artifacts["input-lock.json"],
            current_artifacts["episode-engine.json"],
            current_artifacts["world.json"],
            current_artifacts["visual-plan.json"],
            current_artifacts["asset-tickets.json"],
            identity,
            lock_hash=sha256_file(episode_path / "input-lock.json"),
            engine_hash=sha256_file(episode_path / "episode-engine.json"),
            world_hash=sha256_file(episode_path / "world.json"),
            plan_hash=sha256_file(episode_path / "visual-plan.json"),
        )


def test_scene_direction_rejects_dialogue_grammar_under_narration(
    current_artifacts, identity, episode_path
):
    directions = _direction_fixture(current_artifacts, identity, episode_path)
    shot = directions["sequences"][0]["shots"][0]
    shot["picture_audio_contract"] = {
        "mode": "narrated_observation",
        "language_carrier": "narrator",
        "visible_speech": "required",
        "coverage_grammar": "dialogue_exchange",
        "face_function": "dialogue_exchange",
        "physical_action": "The owner silently appears to answer a buyer across the table.",
        "mute_test": {
            "missing_line_expected": True,
            "reason": "The reverse angle makes the viewer wait for an unheard answer.",
        },
    }
    with pytest.raises(
        ValidationFailure,
        match="narrated_observation requires visible_speech='prohibited'",
    ):
        validate_scene_directions(
            directions,
            current_artifacts["input-lock.json"],
            current_artifacts["episode-engine.json"],
            current_artifacts["world.json"],
            current_artifacts["visual-plan.json"],
            current_artifacts["asset-tickets.json"],
            identity,
            lock_hash=sha256_file(episode_path / "input-lock.json"),
            engine_hash=sha256_file(episode_path / "episode-engine.json"),
            world_hash=sha256_file(episode_path / "world.json"),
            plan_hash=sha256_file(episode_path / "visual-plan.json"),
        )


def test_scene_direction_rejects_unmotivated_face_close_under_narration(
    current_artifacts, identity, episode_path
):
    directions = _direction_fixture(current_artifacts, identity, episode_path)
    shot = directions["sequences"][0]["shots"][0]
    shot["camera"]["framing"] = "close"
    shot["picture_audio_contract"] = {
        "mode": "narrated_observation",
        "language_carrier": "narrator",
        "visible_speech": "prohibited",
        "coverage_grammar": "observational_action",
        "face_function": "environmental_presence",
        "physical_action": "The owner remains present without a task or an on-screen trigger.",
        "mute_test": {
            "missing_line_expected": False,
            "reason": "No dialogue is implied, but the close view has no causal function.",
        },
    }
    with pytest.raises(
        ValidationFailure,
        match="narrated_observation close framing may use a face only",
    ):
        validate_scene_directions(
            directions,
            current_artifacts["input-lock.json"],
            current_artifacts["episode-engine.json"],
            current_artifacts["world.json"],
            current_artifacts["visual-plan.json"],
            current_artifacts["asset-tickets.json"],
            identity,
            lock_hash=sha256_file(episode_path / "input-lock.json"),
            engine_hash=sha256_file(episode_path / "episode-engine.json"),
            world_hash=sha256_file(episode_path / "world.json"),
            plan_hash=sha256_file(episode_path / "visual-plan.json"),
        )


def test_scene_direction_rejects_inexact_word_cue(
    current_artifacts, identity, episode_path
):
    directions = _direction_fixture(current_artifacts, identity, episode_path)
    broken = copy.deepcopy(directions)
    broken["sequences"][0]["shots"][0]["motion_beats"][0]["cue"]["cue_time_seconds"] += 0.25
    with pytest.raises(ValidationFailure, match="cue time is not exact"):
        validate_scene_directions(
            broken,
            current_artifacts["input-lock.json"],
            current_artifacts["episode-engine.json"],
            current_artifacts["world.json"],
            current_artifacts["visual-plan.json"],
            current_artifacts["asset-tickets.json"],
            identity,
            lock_hash=sha256_file(episode_path / "input-lock.json"),
            engine_hash=sha256_file(episode_path / "episode-engine.json"),
            world_hash=sha256_file(episode_path / "world.json"),
            plan_hash=sha256_file(episode_path / "visual-plan.json"),
        )
