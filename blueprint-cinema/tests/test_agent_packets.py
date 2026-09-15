from __future__ import annotations

import copy

import pytest

from blueprint_cinema.validation import (
    ValidationFailure,
    load_json,
    validate_deliverable,
    validate_work_order,
)


def test_current_work_orders_and_packets_validate_without_gate_claims(episode_path):
    for work_path in sorted((episode_path / "agents" / "work-orders").glob("*.json")):
        work = load_json(work_path)
        validate_work_order(work, episode_path)
        packet = load_json(episode_path / "agents" / "deliverables" / work["work_order_id"] / "deliverable.json")
        validate_deliverable(packet, work, episode_path)
        assert packet["approval_claimed"] is False
        assert packet["production_state_changed"] is False


def test_stale_issued_worker_hash_is_rejected(episode_path):
    work = load_json(episode_path / "agents" / "work-orders" / "visual-plan-qa.json")
    stale = copy.deepcopy(work)
    stale["status"] = "issued"
    stale["inputs"][0]["sha256"] = "0" * 64
    with pytest.raises(ValidationFailure, match="stale"):
        validate_work_order(stale, episode_path)


def test_overlapping_or_outside_owned_path_is_rejected(episode_path):
    work = load_json(episode_path / "agents" / "work-orders" / "visual-plan-qa.json")
    invalid = copy.deepcopy(work)
    invalid["status"] = "issued"
    invalid["owned_output_paths"] = [
        "episodes/EP006-direct-booking-recovery/agents/deliverables/world-integrity-review/stolen.md"
    ]
    with pytest.raises(ValidationFailure, match="escapes isolated deliverable directory"):
        validate_work_order(invalid, episode_path)


def test_deliverable_outside_packet_and_approval_claim_are_rejected(episode_path):
    work = load_json(episode_path / "agents" / "work-orders" / "engine-honesty-critique.json")
    packet = load_json(episode_path / "agents" / "deliverables" / "engine-honesty-critique" / "deliverable.json")
    outside = copy.deepcopy(packet)
    outside["files_produced"].append("episodes/EP006-direct-booking-recovery/production-state.json")
    with pytest.raises(ValidationFailure, match="outside its packet"):
        validate_deliverable(outside, work, episode_path)
    claimed = copy.deepcopy(packet)
    claimed["approval_claimed"] = True
    claimed["production_state_changed"] = True
    with pytest.raises(ValidationFailure, match="cannot claim approvals|cannot change production state|False was expected"):
        validate_deliverable(claimed, work, episode_path)

