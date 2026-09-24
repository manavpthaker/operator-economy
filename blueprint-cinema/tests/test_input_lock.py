from __future__ import annotations

import copy

import pytest

from blueprint_cinema.validation import ValidationFailure, schema_errors, validate_input_lock


def test_current_input_lock_schema_and_sources_are_valid(current_artifacts, identity):
    lock = current_artifacts["input-lock.json"]
    assert not schema_errors(lock, "input-lock.schema.json")
    validate_input_lock(lock, identity)
    assert lock["approved_script_sha256"] == next(
        item["sha256"] for item in lock["artifacts"] if item["role"] == "script"
    )
    assert lock["audio_duration_seconds"] == pytest.approx(915.55, abs=0.001)


def test_changed_hash_and_missing_role_fail_closed(current_artifacts, identity):
    changed = copy.deepcopy(current_artifacts["input-lock.json"])
    changed["artifacts"][0]["sha256"] = "0" * 64
    with pytest.raises(ValidationFailure, match="hash changed"):
        validate_input_lock(changed, identity)

    missing = copy.deepcopy(current_artifacts["input-lock.json"])
    missing["artifacts"] = [
        item for item in missing["artifacts"] if item["role"] != "word_transcript"
    ]
    with pytest.raises(ValidationFailure, match="word_transcript"):
        validate_input_lock(missing, identity)


def test_vo_transcript_and_timeline_bounds_are_enforced(current_artifacts, identity):
    invalid = copy.deepcopy(current_artifacts["input-lock.json"])
    invalid["audio_duration_seconds"] = 100.0
    with pytest.raises(ValidationFailure, match="timeline total|timing bounds|VO duration"):
        validate_input_lock(invalid, identity)


def test_only_timeline_mastered_sections_are_locked(current_artifacts):
    lock = current_artifacts["input-lock.json"]
    mastered = [item for item in lock["artifacts"] if item["role"] == "mastered_section"]
    assert [item["section_id"] for item in mastered] == [
        "hook", "thesis", "evidence", "stack", "playbook", "economics", "cta"
    ]
    assert all(".raw." not in item["path"] and ".legacy." not in item["path"] for item in mastered)

