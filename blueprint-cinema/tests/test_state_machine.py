from __future__ import annotations

import copy

import pytest

import blueprint_cinema.state as state_module
from blueprint_cinema.hashes import write_json_atomic
from blueprint_cinema.state import initial_state, record_approval, validate_state
from blueprint_cinema.validation import ValidationFailure


def prepared_episode(tmp_path, identity, monkeypatch):
    episode = tmp_path / identity.folder_name
    episode.mkdir()
    for name, value in (
        ("input-lock.json", {"fixture": "input"}),
        ("episode-engine.json", {"fixture": "engine"}),
        ("world.json", {"fixture": "world"}),
    ):
        write_json_atomic(episode / name, value)
    state_path = episode / "production-state.json"
    write_json_atomic(state_path, initial_state(identity.folder_name))
    monkeypatch.setattr(state_module, "validate_input_lock", lambda *_: None)
    return episode, state_path


def test_sequential_transitions_and_manual_advancement_rejected(tmp_path, identity, monkeypatch):
    episode, state_path = prepared_episode(tmp_path, identity, monkeypatch)
    first = record_approval(
        state_path, episode, identity, "inputs_locked",
        {"episode:input-lock.json": episode / "input-lock.json"},
    )
    assert first["current_stage"] == "inputs_locked"
    second = record_approval(
        state_path, episode, identity, "episode_engine_approved",
        {
            "episode:input-lock.json": episode / "input-lock.json",
            "episode:episode-engine.json": episode / "episode-engine.json",
        },
    )
    assert second["current_stage"] == "episode_engine_approved"
    manual = copy.deepcopy(second)
    manual["current_stage"] = "world_approved"
    with pytest.raises(ValidationFailure, match="manual or inconsistent"):
        validate_state(manual, episode, identity)


def test_upstream_change_detects_stale_and_reapproval_invalidates_downstream(tmp_path, identity, monkeypatch):
    episode, state_path = prepared_episode(tmp_path, identity, monkeypatch)
    record_approval(state_path, episode, identity, "inputs_locked", {"episode:input-lock.json": episode / "input-lock.json"})
    record_approval(
        state_path, episode, identity, "episode_engine_approved",
        {"episode:input-lock.json": episode / "input-lock.json", "episode:episode-engine.json": episode / "episode-engine.json"},
    )
    state = record_approval(
        state_path, episode, identity, "world_approved",
        {
            "episode:input-lock.json": episode / "input-lock.json",
            "episode:episode-engine.json": episode / "episode-engine.json",
            "episode:world.json": episode / "world.json",
        },
    )
    assert state["current_stage"] == "world_approved"
    write_json_atomic(episode / "episode-engine.json", {"fixture": "changed-engine"})
    with pytest.raises(ValidationFailure, match="stale"):
        validate_state(state, episode, identity)
    repaired = record_approval(
        state_path, episode, identity, "episode_engine_approved",
        {"episode:input-lock.json": episode / "input-lock.json", "episode:episode-engine.json": episode / "episode-engine.json"},
    )
    assert repaired["current_stage"] == "episode_engine_approved"
    assert "world_approved" not in repaired["approvals"]


def test_skipped_stage_cannot_be_recorded(tmp_path, identity, monkeypatch):
    episode, state_path = prepared_episode(tmp_path, identity, monkeypatch)
    with pytest.raises(ValidationFailure, match="missing sequential approval"):
        record_approval(
            state_path, episode, identity, "world_approved",
            {"episode:world.json": episode / "world.json"},
        )

