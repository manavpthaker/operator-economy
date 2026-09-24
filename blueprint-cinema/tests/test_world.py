from __future__ import annotations

import copy

import pytest

from blueprint_cinema.validation import ValidationFailure, validate_world


def test_current_world_structural_and_semantic_validity(current_artifacts, identity):
    validate_world(current_artifacts["world.json"], identity)


def test_duplicate_and_dangling_world_ids_are_rejected(current_artifacts, identity):
    duplicate = copy.deepcopy(current_artifacts["world.json"])
    duplicate["objects"][1]["id"] = duplicate["objects"][0]["id"]
    with pytest.raises(ValidationFailure, match="duplicate world IDs|dangling"):
        validate_world(duplicate, identity)
    dangling = copy.deepcopy(current_artifacts["world.json"])
    dangling["edges"][0]["to"] = "missing-node"
    with pytest.raises(ValidationFailure, match="dangling"):
        validate_world(dangling, identity)


def test_consent_and_human_review_cannot_be_bypassed(current_artifacts, identity):
    bypass = copy.deepcopy(current_artifacts["world.json"])
    edge = copy.deepcopy(bypass["edges"][0])
    edge.update({"id": "edge-repair-memory-bypass", "from": "direct-path-repair", "to": "guest-memory-context", "kind": "outbound", "label": "invalid bypass"})
    bypass["edges"].append(edge)
    with pytest.raises(ValidationFailure, match="bypass required permission_gate"):
        validate_world(bypass, identity)


def test_direct_return_cannot_activate_before_audit_and_repair(current_artifacts, identity):
    bypass = copy.deepcopy(current_artifacts["world.json"])
    edge = copy.deepcopy(bypass["edges"][0])
    edge.update({"id": "edge-stay-direct-bypass", "from": "stay-key-tag", "to": "direct-booking-destination", "kind": "return", "label": "invalid early return"})
    bypass["edges"].append(edge)
    with pytest.raises(ValidationFailure, match="bypass required audit_node|bypass required repair_node"):
        validate_world(bypass, identity)


def test_failure_routes_evidence_registry_and_spatial_contract_are_enforced(current_artifacts, identity):
    invalid = copy.deepcopy(current_artifacts["world.json"])
    invalid["failures"][0]["retry_to_id"] = "human-review-gate"
    invalid["evidence"][0]["source_sha256"] = "0" * 64
    invalid["objects"][3]["position"] = invalid["objects"][6]["position"]
    with pytest.raises(ValidationFailure, match="lacks a directed edge|source hash is stale|too close"):
        validate_world(invalid, identity)

