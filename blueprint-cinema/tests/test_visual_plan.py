from __future__ import annotations

import copy

import pytest

from blueprint_cinema.hashes import sha256_file
from blueprint_cinema.validation import ValidationFailure, validate_asset_tickets, validate_plan


def validate(current, identity, episode_path):
    validate_asset_tickets(current["asset-tickets.json"], current["world.json"], identity)
    validate_plan(
        current["visual-plan.json"],
        current["input-lock.json"],
        current["episode-engine.json"],
        current["world.json"],
        current["asset-tickets.json"],
        identity,
        lock_hash=sha256_file(episode_path / "input-lock.json"),
        engine_hash=sha256_file(episode_path / "episode-engine.json"),
        world_hash=sha256_file(episode_path / "world.json"),
    )


def test_full_plan_covers_locked_vo_and_exact_words(current_artifacts, identity, episode_path):
    validate(current_artifacts, identity, episode_path)
    plan = current_artifacts["visual-plan.json"]
    assert plan["units"][0]["in"] == 0
    assert plan["units"][-1]["out"] == pytest.approx(915.55)
    assert len(plan["units"]) >= 150
    assert max(unit["out"] - unit["in"] for unit in plan["units"]) <= 16


def test_gap_and_overlap_are_rejected(cloned_artifacts, identity, episode_path):
    cloned_artifacts["visual-plan.json"]["units"][10]["in"] += 0.5
    with pytest.raises(ValidationFailure, match="gap"):
        validate(cloned_artifacts, identity, episode_path)
    overlap = copy.deepcopy(cloned_artifacts)
    overlap["visual-plan.json"]["units"][10]["in"] -= 1.0
    with pytest.raises(ValidationFailure, match="overlap"):
        validate(overlap, identity, episode_path)


def test_invalid_evidence_and_asset_references_are_rejected(cloned_artifacts, identity, episode_path):
    cloned_artifacts["visual-plan.json"]["units"][0]["evidence_ids"] = ["evidence-missing"]
    cloned_artifacts["visual-plan.json"]["units"][1]["asset_ticket_ids"] = ["ticket-missing"]
    with pytest.raises(ValidationFailure, match="dangling evidence|dangling asset ticket"):
        validate(cloned_artifacts, identity, episode_path)


def test_stale_approval_pins_are_rejected(cloned_artifacts, identity, episode_path):
    cloned_artifacts["visual-plan.json"]["world_sha256"] = "0" * 64
    with pytest.raises(ValidationFailure, match="stale world"):
        validate(cloned_artifacts, identity, episode_path)


def test_guest_memory_requires_resolved_affirmative_permission(cloned_artifacts, identity, episode_path):
    plan = cloned_artifacts["visual-plan.json"]
    memory_index = next(
        index
        for index, unit in enumerate(plan["units"])
        if any(
            state["object_id"] == "guest-memory-context" and state["state"] in {"active", "resolved"}
            for state in unit["world_state_after"]
        )
    )
    approval = next(
        unit
        for unit in reversed(plan["units"][:memory_index])
        if any(state["object_id"] == "permission-gate" for state in unit["world_state_after"])
    )
    approval["world_state_after"][0]["state"] = "active"
    with pytest.raises(ValidationFailure, match="guest memory before affirmative permission"):
        validate(cloned_artifacts, identity, episode_path)


def test_outbound_followup_requires_all_resolved_gates(cloned_artifacts, identity, episode_path):
    plan = cloned_artifacts["visual-plan.json"]
    followup_index = next(
        index
        for index, unit in enumerate(plan["units"])
        if any(
            state["object_id"] == "relevant-follow-up" and state["state"] in {"active", "resolved"}
            for state in unit["world_state_after"]
        )
    )
    human_approval = next(
        unit
        for unit in reversed(plan["units"][:followup_index])
        if any(state["object_id"] == "human-review-gate" for state in unit["world_state_after"])
    )
    human_approval["world_state_after"][0]["state"] = "active"
    with pytest.raises(ValidationFailure, match="outbound follow-up before resolved human approval"):
        validate(cloned_artifacts, identity, episode_path)


def test_actual_failure_and_camera_contract_are_enforced(current_artifacts, cloned_artifacts, identity, episode_path):
    plan = current_artifacts["visual-plan.json"]
    assert any(
        {item["object_id"]: item["state"] for item in unit["world_state_after"]}.get("direct-path-repair") == "failed"
        for unit in plan["units"]
    )
    assert any(
        {item["object_id"]: item["state"] for item in unit["world_state_after"]}.get("return-qualification-gate") == "suppressed"
        for unit in plan["units"]
    )
    cloned_artifacts["visual-plan.json"]["units"][0]["camera_anchor"] = "camera-proof"
    with pytest.raises(ValidationFailure, match="camera does not match"):
        validate(cloned_artifacts, identity, episode_path)
