from __future__ import annotations

import copy

import pytest

from blueprint_cinema.validation import ValidationFailure, validate_engine


def test_current_engine_is_substantive_and_valid(current_artifacts, identity):
    engine = current_artifacts["episode-engine.json"]
    validate_engine(engine, identity)
    assert "capture" not in engine["motion_verbs"]
    assert {"audit", "repair", "request_permission", "qualify", "suppress", "escalate"}.issubset(engine["motion_verbs"])


def test_engine_unknown_fields_and_hollow_strings_fail(current_artifacts, identity):
    unknown = copy.deepcopy(current_artifacts["episode-engine.json"])
    unknown["legacy_layout"] = "card"
    with pytest.raises(ValidationFailure, match="Additional properties"):
        validate_engine(unknown, identity)
    hollow = copy.deepcopy(current_artifacts["episode-engine.json"])
    hollow["owned_value"] = "thin"
    with pytest.raises(ValidationFailure, match="too short"):
        validate_engine(hollow, identity)

