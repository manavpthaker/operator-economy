from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from . import WORKFLOW_VERSION
from .hashes import sha256_file, write_json_atomic
from .paths import REPO_ROOT, EpisodeIdentity
from .validation import STAGES, ValidationFailure, load_json, schema_errors, validate_input_lock


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def initial_state(folder_name: str) -> dict:
    return {
        "$schema": "../../schemas/production-state.schema.json",
        "schema_version": "1.0.0",
        "workflow_version": WORKFLOW_VERSION,
        "episode_folder": folder_name,
        "current_stage": "initialized",
        "approvals": {},
    }


def _artifact_path(key: str, episode_path: Path) -> Path:
    prefix, separator, relative = key.partition(":")
    if not separator or not relative:
        raise ValueError(f"invalid approval artifact key: {key}")
    if prefix == "episode":
        candidate = (episode_path / relative).resolve()
        candidate.relative_to(episode_path.resolve())
        return candidate
    if prefix == "repo":
        candidate = (REPO_ROOT / relative).resolve()
        candidate.relative_to(REPO_ROOT.resolve())
        return candidate
    raise ValueError(f"unknown approval artifact scope: {prefix}")


def artifact_hashes(paths: dict[str, Path]) -> dict[str, str]:
    values: dict[str, str] = {}
    for key, path in paths.items():
        if not path.is_file():
            raise ValidationFailure("approval", [f"approval artifact is missing: {path}"])
        values[key] = sha256_file(path)
    return values


def _validate_approval_hashes(state: dict, episode_path: Path, through_index: int) -> list[str]:
    errors: list[str] = []
    approvals = state.get("approvals", {})
    for index, stage in enumerate(STAGES):
        if index > through_index:
            break
        approval = approvals.get(stage)
        if not approval:
            errors.append(f"missing sequential approval: {stage}")
            continue
        if approval.get("stage") != stage:
            errors.append(f"approval record key and stage disagree: {stage}")
        for key, expected_hash in approval.get("artifact_hashes", {}).items():
            try:
                path = _artifact_path(key, episode_path)
            except ValueError as error:
                errors.append(str(error))
                continue
            if not path.is_file():
                errors.append(f"approved artifact is missing: {key}")
            elif sha256_file(path) != expected_hash:
                errors.append(f"approved artifact hash is stale: {key}")
    return errors


def validate_state_through(
    state: dict,
    episode_path: Path,
    identity: EpisodeIdentity,
    required_stage: str,
) -> None:
    if required_stage not in STAGES:
        raise ValidationFailure("production_state", [f"unknown stage: {required_stage}"])
    errors = schema_errors(state, "production-state.schema.json")
    if state.get("episode_folder") != identity.folder_name:
        errors.append("production state episode folder disagrees with project identity")
    required_index = STAGES.index(required_stage)
    errors.extend(_validate_approval_hashes(state, episode_path, required_index))
    if required_index >= 0 and (episode_path / "input-lock.json").is_file():
        try:
            validate_input_lock(load_json(episode_path / "input-lock.json"), identity)
        except ValidationFailure as error:
            errors.extend(error.errors)
    if errors:
        raise ValidationFailure(required_stage, errors)


def validate_state(state: dict, episode_path: Path, identity: EpisodeIdentity) -> None:
    errors = schema_errors(state, "production-state.schema.json")
    approvals = state.get("approvals", {})
    approval_indices = [STAGES.index(stage) for stage in approvals if stage in STAGES]
    if approval_indices:
        highest_index = max(approval_indices)
        expected = STAGES[highest_index]
        for stage in STAGES[: highest_index + 1]:
            if stage not in approvals:
                errors.append(f"production state skipped sequential approval: {stage}")
        if state.get("current_stage") != expected:
            errors.append(
                f"manual or inconsistent state advancement: current_stage is {state.get('current_stage')}, "
                f"but approvals support only {expected}"
            )
        errors.extend(_validate_approval_hashes(state, episode_path, highest_index))
        try:
            validate_input_lock(load_json(episode_path / "input-lock.json"), identity)
        except ValidationFailure as error:
            errors.extend(error.errors)
    elif state.get("current_stage") != "initialized":
        errors.append("state advanced without approval records")
    if errors:
        raise ValidationFailure("production_state", errors)


def record_approval(
    state_path: Path,
    episode_path: Path,
    identity: EpisodeIdentity,
    stage: str,
    paths: dict[str, Path],
) -> dict:
    if stage not in STAGES:
        raise ValidationFailure("production_state", [f"unknown stage: {stage}"])
    state = load_json(state_path) if state_path.is_file() else initial_state(identity.folder_name)
    stage_index = STAGES.index(stage)
    if stage_index > 0:
        validate_state_through(state, episode_path, identity, STAGES[stage_index - 1])
    approvals = {
        key: value
        for key, value in state.get("approvals", {}).items()
        if key in STAGES and STAGES.index(key) < stage_index
    }
    approvals[stage] = {
        "stage": stage,
        "approved_at": utc_now(),
        "artifact_hashes": artifact_hashes(paths),
    }
    updated = initial_state(identity.folder_name)
    updated["current_stage"] = stage
    updated["approvals"] = approvals
    write_json_atomic(state_path, updated)
    validate_state(updated, episode_path, identity)
    return updated


def next_stage(current_stage: str) -> str | None:
    if current_stage == "initialized":
        return STAGES[0]
    if current_stage not in STAGES:
        return None
    index = STAGES.index(current_stage) + 1
    return STAGES[index] if index < len(STAGES) else None

