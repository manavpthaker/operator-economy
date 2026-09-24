from __future__ import annotations

import json
from collections import defaultdict, deque
from pathlib import Path
from typing import Any, Iterable

from jsonschema import Draft202012Validator, FormatChecker

from .hashes import sha256_file
from .input_lock import probe_duration, source_path
from .paths import (
    BLUEPRINT_ROOT,
    REPO_ROOT,
    SCHEMAS_ROOT,
    EpisodeIdentity,
)


PROHIBITED_REFERENCES = (
    "storyboard.json",
    "coverage_map.json",
    "render_data/blueprint.json",
    "build_rev_e_storyboard.py",
    "oeopeningpilot.tsx",
    "storyboard_frames",
    "storyboard_review",
    "resolve_pilot",
    "141 screens",
)

NAVIGATION_VERBS = {"cut", "reveal", "inspect", "establish", "reset", "hold", "resolve"}
STAGES = [
    "inputs_locked",
    "episode_engine_approved",
    "world_approved",
    "visual_plan_approved",
    "greybox_ready",
    "greybox_approved",
    "assets_ready",
    "rough_cut_approved",
    "fine_cut_approved",
    "delivery_validated",
]


class ValidationFailure(ValueError):
    def __init__(self, gate: str, errors: Iterable[str]):
        self.gate = gate
        self.errors = list(errors)
        message = f"{gate} blocked: " + "; ".join(self.errors)
        super().__init__(message)


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as error:
        raise ValidationFailure("file_validation", [f"missing file: {path}"]) from error
    except json.JSONDecodeError as error:
        raise ValidationFailure(
            "file_validation", [f"invalid JSON in {path}: {error}"]
        ) from error


def schema_errors(value: Any, schema_name: str) -> list[str]:
    schema_path = SCHEMAS_ROOT / schema_name
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = []
    for error in sorted(validator.iter_errors(value), key=lambda item: list(item.path)):
        location = ".".join(str(part) for part in error.absolute_path) or "$"
        errors.append(f"{schema_name}:{location}: {error.message}")
    return errors


def validate_schema(value: Any, schema_name: str, gate: str) -> None:
    errors = schema_errors(value, schema_name)
    if errors:
        raise ValidationFailure(gate, errors)


def _walk_strings(value: Any) -> Iterable[str]:
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for item in value.values():
            yield from _walk_strings(item)
    elif isinstance(value, list):
        for item in value:
            yield from _walk_strings(item)


def clean_room_errors(value: Any) -> list[str]:
    errors: list[str] = []
    for raw in _walk_strings(value):
        normalized = raw.replace("\\", "/").lower()
        for prohibited in PROHIBITED_REFERENCES:
            if prohibited in normalized:
                errors.append(f"prohibited legacy reference: {raw}")
    return sorted(set(errors))


def validate_clean_room(value: Any, gate: str = "clean_room") -> None:
    errors = clean_room_errors(value)
    if errors:
        raise ValidationFailure(gate, errors)


def identity_errors(value: dict, expected: EpisodeIdentity) -> list[str]:
    try:
        actual = EpisodeIdentity.from_dict(value)
    except (KeyError, TypeError, ValueError) as error:
        return [str(error)]
    return [] if actual == expected else ["artifact episode identity does not match project"]


def validate_episode_project(project: dict, expected: EpisodeIdentity | None = None) -> None:
    errors = schema_errors(project, "episode-project.schema.json")
    try:
        actual = EpisodeIdentity.from_dict(project)
        if expected is not None and actual != expected:
            errors.append("episode.json identity does not match the requested folder")
    except (KeyError, TypeError, ValueError) as error:
        errors.append(str(error))
    if errors:
        raise ValidationFailure("episode_identity", errors)


def validate_input_lock(lock: dict, expected: EpisodeIdentity) -> None:
    errors = schema_errors(lock, "input-lock.schema.json")
    errors.extend(identity_errors(lock, expected))
    errors.extend(clean_room_errors(lock))
    artifacts = lock.get("artifacts", [])
    roles = [item.get("role") for item in artifacts if isinstance(item, dict)]
    required_counts = {
        "script": 1,
        "assembled_vo": 1,
        "word_transcript": 1,
        "timeline": 1,
    }
    for role, count in required_counts.items():
        if roles.count(role) != count:
            errors.append(f"input lock must contain exactly {count} {role} artifact")
    if roles.count("mastered_section") < 1:
        errors.append("input lock must contain mastered section audio")

    seen_paths: set[str] = set()
    for artifact in artifacts:
        path_value = artifact.get("path")
        if path_value in seen_paths:
            errors.append(f"duplicate locked path: {path_value}")
            continue
        seen_paths.add(path_value)
        try:
            current_path = source_path(artifact)
            current_path.relative_to(REPO_ROOT.resolve())
        except (KeyError, ValueError):
            errors.append(f"locked path escapes the repository: {path_value}")
            continue
        if not current_path.is_file():
            errors.append(f"locked source is missing: {path_value}")
            continue
        if sha256_file(current_path) != artifact.get("sha256"):
            errors.append(f"locked source hash changed: {path_value}")
        if current_path.stat().st_size != artifact.get("size_bytes"):
            errors.append(f"locked source size changed: {path_value}")
        if artifact.get("role") in {"assembled_vo", "mastered_section"}:
            try:
                actual_duration = probe_duration(current_path)
                if abs(actual_duration - float(artifact.get("duration_seconds", -1))) > 0.05:
                    errors.append(f"locked audio duration changed: {path_value}")
            except (ValueError, TypeError) as error:
                errors.append(str(error))

    artifact_by_role = {item.get("role"): item for item in artifacts}
    if all(role in artifact_by_role for role in ("script", "assembled_vo", "word_transcript", "timeline")):
        if artifact_by_role["script"].get("sha256") != lock.get("approved_script_sha256"):
            errors.append("locked script does not match approved_script_sha256")
        try:
            words = load_json(source_path(artifact_by_role["word_transcript"]))
            timeline = load_json(source_path(artifact_by_role["timeline"]))
            duration = float(lock.get("audio_duration_seconds", -1))
            if abs(float(timeline.get("total_seconds", -1)) - duration) > 0.05:
                errors.append("timeline total does not match locked VO duration")
            expected_start = 0.0
            locked_sections = {
                item.get("section_id"): item
                for item in artifacts
                if item.get("role") == "mastered_section"
            }
            for section in timeline.get("sections", []):
                start = float(section.get("start", -1))
                section_duration = float(section.get("duration", -1))
                section_id = section.get("section")
                if abs(start - expected_start) > 0.01:
                    errors.append(f"timeline has a gap or overlap before {section_id}")
                expected_start = round(start + section_duration, 6)
                locked_section = locked_sections.get(section_id)
                if not locked_section:
                    errors.append(f"timeline section is not locked: {section_id}")
                elif Path(locked_section["path"]).name != section.get("audio"):
                    errors.append(f"timeline audio disagrees with lock for {section_id}")
            if abs(expected_start - duration) > 0.05:
                errors.append("timeline sections do not cover the locked VO")
            previous_end = -1.0
            valid_sections = {section.get("section") for section in timeline.get("sections", [])}
            for index, word in enumerate(words):
                start = float(word.get("start", -1))
                end = float(word.get("end", -1))
                if start < 0 or end < start or end > duration + 0.001:
                    errors.append(f"word {index} exceeds VO timing bounds")
                    break
                if start + 0.05 < previous_end:
                    errors.append(f"word {index} moves backward")
                    break
                if word.get("section") not in valid_sections:
                    errors.append(f"word {index} references an unknown section")
                    break
                previous_end = end
        except (ValidationFailure, ValueError, TypeError, KeyError) as error:
            errors.append(f"input timing validation failed: {error}")
    if errors:
        raise ValidationFailure("inputs_locked", errors)


def validate_engine(engine: dict, expected: EpisodeIdentity) -> None:
    errors = schema_errors(engine, "episode-engine.schema.json")
    errors.extend(identity_errors(engine, expected))
    errors.extend(clean_room_errors(engine))
    required_verbs = {
        "audit", "repair", "request_permission", "qualify", "suppress", "escalate",
        "route", "book", "welcome", "remember", "follow_up", "recover", "measure",
    }
    verbs = set(engine.get("motion_verbs", []))
    missing = sorted(required_verbs - verbs)
    if missing:
        errors.append(f"engine is missing required motion verbs: {', '.join(missing)}")
    if "capture" in verbs:
        errors.append("capture may not be used as shorthand for permission")
    combined = " ".join(_walk_strings(engine)).lower()
    for required_phrase in (
        "completed an ota-acquired stay",
        "appropriate",
        "permission",
        "audit",
        "repair",
        "human",
        "settlement",
        "direct booking confirmation",
    ):
        if required_phrase not in combined:
            errors.append(f"engine does not substantively address: {required_phrase}")
    if engine.get("status") != "ready_for_approval":
        errors.append("engine status must be ready_for_approval before approval")
    if errors:
        raise ValidationFailure("episode_engine_approved", errors)


def _has_path(adjacency: dict[str, set[str]], start: str, end: str, blocked: str | None = None) -> bool:
    if start == blocked or end == blocked:
        return False
    queue = deque([start])
    seen = {start}
    while queue:
        current = queue.popleft()
        if current == end:
            return True
        for target in adjacency.get(current, set()):
            if target == blocked or target in seen:
                continue
            seen.add(target)
            queue.append(target)
    return False


def validate_world(world: dict, expected: EpisodeIdentity) -> None:
    errors = schema_errors(world, "world.schema.json")
    errors.extend(identity_errors(world, expected))
    errors.extend(clean_room_errors(world))
    objects = world.get("objects", [])
    edges = world.get("edges", [])
    claims = world.get("claims", [])
    parameters = world.get("parameters", [])
    evidence = world.get("evidence", [])
    cameras = world.get("cameras", [])
    failures = world.get("failures", [])

    all_records = objects + edges + claims + parameters + evidence + cameras + failures
    ids = [record.get("id") for record in all_records if isinstance(record, dict)]
    duplicates = sorted({record_id for record_id in ids if ids.count(record_id) > 1})
    if duplicates:
        errors.append(f"duplicate world IDs: {', '.join(duplicates)}")
    object_map = {item.get("id"): item for item in objects}
    object_ids = set(object_map)
    edge_pairs: set[tuple[str, str]] = set()
    adjacency: dict[str, set[str]] = defaultdict(set)

    for item in objects:
        zone_id = item.get("zone_id")
        if zone_id not in object_ids:
            errors.append(f"object {item.get('id')} has dangling zone {zone_id}")
        elif object_map[zone_id].get("kind") != "zone":
            errors.append(f"object {item.get('id')} zone_id is not a zone")
        state_ids = [state.get("id") for state in item.get("states", [])]
        if len(state_ids) != len(set(state_ids)):
            errors.append(f"object {item.get('id')} has duplicate state IDs")
        if item.get("initial_state") not in state_ids:
            errors.append(f"object {item.get('id')} has dangling initial state")

    visible_objects = [item for item in objects if item.get("kind") != "zone"]
    for index, first in enumerate(visible_objects):
        for second in visible_objects[index + 1 :]:
            if first.get("zone_id") != second.get("zone_id"):
                continue
            dx = float(first.get("position", {}).get("x", 0)) - float(second.get("position", {}).get("x", 0))
            dy = float(first.get("position", {}).get("y", 0)) - float(second.get("position", {}).get("y", 0))
            if (dx * dx + dy * dy) ** 0.5 < 140:
                errors.append(f"world objects are too close for labelled greybox primitives: {first.get('id')} and {second.get('id')}")

    for edge in edges:
        start, end = edge.get("from"), edge.get("to")
        if start not in object_ids or end not in object_ids:
            errors.append(f"edge {edge.get('id')} has a dangling object reference")
        else:
            adjacency[start].add(end)
            edge_pairs.add((start, end))
        state_ids = [state.get("id") for state in edge.get("states", [])]
        if edge.get("initial_state") not in state_ids:
            errors.append(f"edge {edge.get('id')} has dangling initial state")

    evidence_ids = {item.get("id") for item in evidence}
    claim_ids = {item.get("id") for item in claims}
    parameter_ids = {item.get("id") for item in parameters}
    for claim in claims:
        for evidence_id in claim.get("evidence_ids", []):
            if evidence_id not in evidence_ids:
                errors.append(f"claim {claim.get('id')} has dangling evidence {evidence_id}")
    for parameter in parameters:
        if parameter.get("evidence_id") not in evidence_ids:
            errors.append(f"parameter {parameter.get('id')} has dangling evidence {parameter.get('evidence_id')}")
    for pin in evidence:
        for target in pin.get("target_ids", []):
            if target not in object_ids:
                errors.append(f"evidence {pin.get('id')} has dangling target {target}")
        for claim_id in pin.get("claim_ids", []):
            if claim_id not in claim_ids:
                errors.append(f"evidence {pin.get('id')} has dangling claim {claim_id}")
        for parameter_id in pin.get("parameter_ids", []):
            if parameter_id not in parameter_ids:
                errors.append(f"evidence {pin.get('id')} has dangling parameter {parameter_id}")
        source_value = pin.get("source_path")
        source_candidate = (REPO_ROOT / source_value).resolve() if isinstance(source_value, str) else None
        try:
            if source_candidate is None:
                raise ValueError
            source_candidate.relative_to(REPO_ROOT.resolve().parent)
        except ValueError:
            errors.append(f"evidence {pin.get('id')} source escapes the allowed repository authority roots")
            source_candidate = None
        if source_candidate is None or not source_candidate.is_file():
            errors.append(f"evidence {pin.get('id')} source is missing: {source_value}")
        elif sha256_file(source_candidate) != pin.get("source_sha256"):
            errors.append(f"evidence {pin.get('id')} source hash is stale")
    camera_ids = {item.get("id") for item in cameras}
    for camera in cameras:
        if camera.get("zone_id") not in object_ids:
            errors.append(f"camera {camera.get('id')} has dangling zone")
        for target in camera.get("target_ids", []):
            if target not in object_ids:
                errors.append(f"camera {camera.get('id')} has dangling target {target}")
    for failure in failures:
        for field in ("at_id", "retry_to_id", "escalation_to_id"):
            if failure.get(field) not in object_ids:
                errors.append(f"failure {failure.get('id')} has dangling {field}")
        at_object = object_map.get(failure.get("at_id"), {})
        if failure.get("failed_state") not in {
            state.get("id") for state in at_object.get("states", [])
        }:
            errors.append(f"failure {failure.get('id')} has dangling failed_state")
        if (failure.get("at_id"), failure.get("retry_to_id")) not in edge_pairs:
            errors.append(f"failure {failure.get('id')} retry destination lacks a directed edge")
        if (failure.get("at_id"), failure.get("escalation_to_id")) not in edge_pairs:
            errors.append(f"failure {failure.get('id')} escalation destination lacks a directed edge")

    roles = world.get("required_roles", {})
    for role, object_id in roles.items():
        if object_id not in object_ids:
            errors.append(f"required role {role} has dangling object {object_id}")
    zone_bounds = {
        roles.get("reality_zone"): (0, 600),
        roles.get("system_zone"): (600, 1450),
        roles.get("proof_zone"): (1450, 1920),
    }
    for item in visible_objects:
        bounds = zone_bounds.get(item.get("zone_id"))
        x = float(item.get("position", {}).get("x", -1))
        if bounds and not (bounds[0] <= x <= bounds[1]):
            errors.append(f"object {item.get('id')} is outside its declared spatial zone")
    for camera in cameras:
        for target in camera.get("target_ids", []):
            if object_map.get(target, {}).get("zone_id") != camera.get("zone_id"):
                errors.append(f"camera {camera.get('id')} has an undeclared cross-zone target {target}")
    for path_name, path in world.get("paths", {}).items():
        for object_id in path:
            if object_id not in object_ids:
                errors.append(f"path {path_name} has dangling object {object_id}")
        for start, end in zip(path, path[1:]):
            if (start, end) not in edge_pairs:
                errors.append(f"path {path_name} has no edge {start} -> {end}")

    try:
        first_path = world["paths"]["first_booking"]
        recovery_path = world["paths"]["recovery"]
        required_first = [roles["ota_gate"], roles["hotel_node"]]
        if any(item not in first_path for item in required_first):
            errors.append("first-booking path must preserve the useful OTA route")
        required_recovery = [
            roles["guest_token"], roles["audit_node"], roles["repair_node"],
            roles["permission_gate"], roles["guest_memory"], roles["qualification_gate"],
            roles["human_review_gate"], roles["direct_destination"], roles["direct_confirmation"],
        ]
        positions = [recovery_path.index(item) for item in required_recovery]
        if positions != sorted(positions):
            errors.append("recovery path does not enforce audit, repair, consent, qualification, and human review order")
        start, end = roles["guest_token"], roles["direct_confirmation"]
        if not _has_path(adjacency, start, end):
            errors.append("no required path exists from the OTA-acquired stay to direct confirmation")
        for gate_role in ("audit_node", "repair_node", "permission_gate", "qualification_gate", "human_review_gate"):
            gate_id = roles[gate_role]
            if _has_path(adjacency, start, end, blocked=gate_id):
                errors.append(f"outbound path can bypass required {gate_role}")
        if roles["settlement_ledger"] == roles["direct_confirmation"]:
            errors.append("operator settlement proof must be separate from guest confirmation")
        if object_map.get(roles["settlement_ledger"], {}).get("kind") != "ledger":
            errors.append("economic consequence must use an operator-side ledger")
        if object_map.get(roles["direct_confirmation"], {}).get("kind") != "outcome":
            errors.append("direct confirmation must be the visible outcome object")
    except (KeyError, ValueError):
        errors.append("required world paths or roles are incomplete")
    if world.get("status") != "ready_for_approval":
        errors.append("world status must be ready_for_approval before approval")
    if errors:
        raise ValidationFailure("world_approved", errors)


def validate_asset_tickets(tickets: dict, world: dict, expected: EpisodeIdentity) -> None:
    errors = schema_errors(tickets, "asset-ticket.schema.json")
    errors.extend(identity_errors(tickets, expected))
    errors.extend(clean_room_errors(tickets))
    ticket_ids = [item.get("id") for item in tickets.get("tickets", [])]
    duplicates = sorted({ticket_id for ticket_id in ticket_ids if ticket_ids.count(ticket_id) > 1})
    if duplicates:
        errors.append(f"duplicate asset ticket IDs: {', '.join(duplicates)}")
    evidence_ids = {item.get("id") for item in world.get("evidence", [])}
    for ticket in tickets.get("tickets", []):
        for evidence_id in ticket.get("evidence_ids", []):
            if evidence_id not in evidence_ids:
                errors.append(f"ticket {ticket.get('id')} has dangling evidence {evidence_id}")
    if errors:
        raise ValidationFailure("visual_plan_approved", errors)


def _word_artifact(lock: dict) -> dict:
    for artifact in lock.get("artifacts", []):
        if artifact.get("role") == "word_transcript":
            return artifact
    raise ValidationFailure("visual_plan_approved", ["input lock has no word transcript"])


def validate_plan(
    plan: dict,
    lock: dict,
    engine: dict,
    world: dict,
    tickets: dict,
    expected: EpisodeIdentity,
    *,
    lock_hash: str,
    engine_hash: str,
    world_hash: str,
) -> None:
    errors = schema_errors(plan, "visual-plan.schema.json")
    errors.extend(identity_errors(plan, expected))
    errors.extend(clean_room_errors(plan))
    if plan.get("input_lock_sha256") != lock_hash:
        errors.append("visual plan is pinned to a stale input lock")
    if plan.get("episode_engine_sha256") != engine_hash:
        errors.append("visual plan is pinned to a stale episode engine")
    if plan.get("world_sha256") != world_hash:
        errors.append("visual plan is pinned to a stale world")
    duration = float(lock.get("audio_duration_seconds", -1))
    if abs(float(plan.get("audio_duration_seconds", -1)) - duration) > 0.01:
        errors.append("visual plan duration does not match the locked VO")

    object_map = {item.get("id"): item for item in world.get("objects", [])}
    object_ids = set(object_map)
    evidence_ids = {item.get("id") for item in world.get("evidence", [])}
    camera_ids = {item.get("id") for item in world.get("cameras", [])}
    ticket_ids = {item.get("id") for item in tickets.get("tickets", [])}
    allowed_verbs = set(engine.get("motion_verbs", [])) | NAVIGATION_VERBS
    words = load_json(source_path(_word_artifact(lock)))
    units = plan.get("units", [])
    unit_ids = [unit.get("id") for unit in units]
    if len(unit_ids) != len(set(unit_ids)):
        errors.append("visual plan contains duplicate unit IDs")
    current_states = {
        object_id: item.get("initial_state") for object_id, item in object_map.items()
    }
    state_sequences: dict[str, str | None] = {object_id: None for object_id in object_map}
    mode_cameras = {
        "reality": "camera-human",
        "system": "camera-system",
        "proof": "camera-proof",
        "reset": "camera-system",
    }
    activated_failures: list[tuple[int, dict]] = []
    expected_in = 0.0
    for index, unit in enumerate(units):
        unit_in = float(unit.get("in", -1))
        unit_out = float(unit.get("out", -1))
        if index == 0 and unit_in > 0.5:
            errors.append("visual plan does not start at or near zero")
        if abs(unit_in - expected_in) > 0.01:
            relation = "gap" if unit_in > expected_in else "overlap"
            errors.append(f"{relation} before {unit.get('id')}: expected {expected_in:.3f}, got {unit_in:.3f}")
        if unit_out <= unit_in:
            errors.append(f"unit {unit.get('id')} has non-positive duration")
        if unit_out - unit_in > 16.0:
            errors.append(f"unit {unit.get('id')} exceeds the 16-second hard hold limit")
        if unit_out > duration + 0.01:
            errors.append(f"unit {unit.get('id')} exceeds the audio duration")
        expected_in = unit_out
        if unit.get("motion_verb") not in allowed_verbs:
            errors.append(f"unit {unit.get('id')} uses unapproved motion verb {unit.get('motion_verb')}")
        for field in ("carry", "focus"):
            for object_id in unit.get(field, []):
                if object_id not in object_ids:
                    errors.append(f"unit {unit.get('id')} has dangling {field} object {object_id}")
        if unit.get("camera_anchor") not in camera_ids:
            errors.append(f"unit {unit.get('id')} has dangling camera anchor")
        expected_camera = mode_cameras.get(unit.get("mode"))
        if expected_camera and unit.get("camera_anchor") != expected_camera:
            errors.append(
                f"unit {unit.get('id')} camera does not match its {unit.get('mode')} view"
            )
        for evidence_id in unit.get("evidence_ids", []):
            if evidence_id not in evidence_ids:
                errors.append(f"unit {unit.get('id')} has dangling evidence {evidence_id}")
        for ticket_id in unit.get("asset_ticket_ids", []):
            if ticket_id not in ticket_ids:
                errors.append(f"unit {unit.get('id')} has dangling asset ticket {ticket_id}")
        before_items = unit.get("world_state_before", [])
        after_items = unit.get("world_state_after", [])
        before = {(item.get("object_id"), item.get("state")) for item in before_items}
        after = {(item.get("object_id"), item.get("state")) for item in after_items}
        before_map = {item.get("object_id"): item.get("state") for item in before_items}
        after_map = {item.get("object_id"): item.get("state") for item in after_items}
        if len(before_map) != len(before_items) or len(after_map) != len(after_items):
            errors.append(f"unit {unit.get('id')} repeats a world-state object")
        if set(before_map) != set(after_map):
            errors.append(f"unit {unit.get('id')} before/after objects disagree")
        for object_id, state_id in before | after:
            if object_id not in object_ids:
                errors.append(f"unit {unit.get('id')} has dangling world-state object {object_id}")
            elif state_id not in {state.get("id") for state in object_map[object_id].get("states", [])}:
                errors.append(f"unit {unit.get('id')} has dangling state {state_id} for {object_id}")
        if unit.get("mode") == "system" and before == after:
            errors.append(f"system unit {unit.get('id')} does not change business state")
        for object_id, declared_before in before_map.items():
            if current_states.get(object_id) != declared_before:
                errors.append(
                    f"unit {unit.get('id')} has discontinuous state for {object_id}: "
                    f"expected {current_states.get(object_id)}, got {declared_before}"
                )
            declared_after = after_map.get(object_id)
            if (
                state_sequences.get(object_id) == unit.get("sequence_id")
                and declared_before in {"resolved", "failed", "suppressed"}
                and declared_after == "active"
            ):
                errors.append(
                    f"unit {unit.get('id')} regresses {object_id} inside one sequence without a reset"
                )
        current_states.update(after_map)
        for object_id in after_map:
            state_sequences[object_id] = unit.get("sequence_id")
        roles = world.get("required_roles", {})
        permission_id = roles.get("permission_gate")
        memory_id = roles.get("guest_memory")
        qualification_id = roles.get("qualification_gate")
        suppression_id = roles.get("suppression_node")
        human_id = roles.get("human_review_gate")
        audit_id = roles.get("audit_node")
        repair_id = roles.get("repair_node")
        follow_up_id = roles.get("relevant_follow_up")
        destination_id = roles.get("direct_destination")
        return_money_id = roles.get("return_booking_money_flow")
        confirmation_id = roles.get("direct_confirmation")

        if memory_id in after_map and after_map[memory_id] in {"active", "resolved"}:
            if current_states.get(permission_id) != "resolved":
                errors.append(
                    f"unit {unit.get('id')} activates guest memory before affirmative permission"
                )

        outbound_requirements = {
            audit_id: "direct-path audit",
            repair_id: "direct-path repair",
            permission_id: "affirmative permission",
            qualification_id: "appropriate qualification",
            suppression_id: "suppression disposition",
            human_id: "human approval",
        }

        def require_resolved(label: str) -> None:
            for object_id, requirement in outbound_requirements.items():
                if current_states.get(object_id) != "resolved":
                    errors.append(
                        f"unit {unit.get('id')} activates {label} before resolved {requirement}"
                    )

        if follow_up_id in after_map and after_map[follow_up_id] in {"active", "resolved"}:
            require_resolved("outbound follow-up")
        if (
            destination_id in after_map
            and after_map[destination_id] in {"active", "resolved"}
            and unit.get("motion_verb") in {"route", "recover", "confirm", "follow_up"}
        ):
            require_resolved("direct return route")
        if return_money_id in after_map and after_map[return_money_id] in {"active", "resolved"}:
            require_resolved("return-booking value")
            if current_states.get(destination_id) != "resolved":
                errors.append(
                    f"unit {unit.get('id')} records return value before the direct destination resolves"
                )
        if confirmation_id in after_map and after_map[confirmation_id] in {"active", "resolved"}:
            require_resolved("direct confirmation")
            if current_states.get(destination_id) != "resolved":
                errors.append(
                    f"unit {unit.get('id')} confirms a booking before the direct destination resolves"
                )
            if current_states.get(return_money_id) != "resolved":
                errors.append(
                    f"unit {unit.get('id')} confirms a booking before return value is recorded"
                )
        for failure in world.get("failures", []):
            if after_map.get(failure.get("at_id")) == failure.get("failed_state"):
                activated_failures.append((index, failure))
        if "add energy" in unit.get("action", "").lower():
            errors.append(f"unit {unit.get('id')} exists only to add energy")
        anchor = unit.get("narration_anchor", {})
        start_index, end_index = anchor.get("word_start", -1), anchor.get("word_end", -1)
        if not isinstance(start_index, int) or not isinstance(end_index, int) or start_index < 0 or end_index < start_index or end_index >= len(words):
            errors.append(f"unit {unit.get('id')} has an invalid word range")
        else:
            exact_quote = " ".join(str(word.get("word", "")) for word in words[start_index : end_index + 1])
            if anchor.get("quote") != exact_quote:
                errors.append(f"unit {unit.get('id')} narration quote is not exact")
            anchor_start = float(words[start_index].get("start", -1))
            anchor_end = float(words[end_index].get("end", -1))
            if anchor_start < unit_in - 1.0 or anchor_end > unit_out + 1.0:
                errors.append(f"unit {unit.get('id')} word range is outside its timing window")
    if units and abs(expected_in - duration) > 0.01:
        errors.append(f"visual plan ends at {expected_in:.3f}s, not locked VO {duration:.3f}s")

    first_thirty = [unit for unit in units if float(unit.get("in", 9999)) < 30.0]
    roles = world.get("required_roles", {})
    if not any(unit.get("mode") == "reality" for unit in first_thirty):
        errors.append("first 30 seconds lack human or physical reality")
    if not any(unit.get("mode") == "proof" or unit.get("evidence_ids") for unit in first_thirty):
        errors.append("first 30 seconds lack a market force or proof object")
    counter_ids = {roles.get("audit_node"), roles.get("repair_node"), roles.get("direct_destination")}
    if not any(counter_ids.intersection(unit.get("focus", [])) for unit in first_thirty):
        errors.append("first 30 seconds lack a glimpse of the counter-system")
    all_focus = {object_id for unit in units for object_id in unit.get("focus", [])}
    semantic_roles = {
        "consent": "permission_gate",
        "qualification": "qualification_gate",
        "suppression": "suppression_node",
        "human judgment": "human_review_gate",
        "economics": "settlement_ledger",
        "outcome": "direct_confirmation",
    }
    for label, role_name in semantic_roles.items():
        if roles.get(role_name) not in all_focus:
            errors.append(f"visual plan never shows required semantic: {label}")
    if not activated_failures:
        errors.append("visual plan never activates a configured failure state")
    elif not any(
        any(
            failure.get(field) in later.get("focus", [])
            for later in units[index + 1 :]
            for field in ("retry_to_id", "escalation_to_id")
        )
        for index, failure in activated_failures
    ):
        errors.append("visual plan activates failure without a later retry or escalation route")
    if plan.get("status") != "ready_for_approval":
        errors.append("visual plan status must be ready_for_approval before approval")
    if errors:
        raise ValidationFailure("visual_plan_approved", errors)


def validate_scene_directions(
    directions: dict,
    lock: dict,
    engine: dict,
    world: dict,
    plan: dict,
    tickets: dict,
    expected: EpisodeIdentity,
    *,
    lock_hash: str,
    engine_hash: str,
    world_hash: str,
    plan_hash: str,
) -> None:
    errors = schema_errors(directions, "scene-directions.schema.json")
    errors.extend(identity_errors(directions, expected))
    errors.extend(clean_room_errors(directions))
    expected_hashes = {
        "input_lock_sha256": (lock_hash, "input lock"),
        "episode_engine_sha256": (engine_hash, "episode engine"),
        "world_sha256": (world_hash, "world"),
        "visual_plan_sha256": (plan_hash, "visual plan"),
    }
    for field, (digest, label) in expected_hashes.items():
        if directions.get(field) != digest:
            errors.append(f"scene directions are pinned to a stale {label}")

    try:
        words = load_json(source_path(_word_artifact(lock)))
    except ValidationFailure as error:
        errors.extend(error.errors)
        words = []

    plan_groups: dict[str, list[dict]] = defaultdict(list)
    for unit in plan.get("units", []):
        plan_groups[unit.get("sequence_id")].append(unit)
    object_ids = {item.get("id") for item in world.get("objects", [])}
    evidence_ids = {item.get("id") for item in world.get("evidence", [])}
    ticket_ids = {item.get("id") for item in tickets.get("tickets", [])}
    scope = directions.get("scope", {})
    sequences = directions.get("sequences", [])
    sequence_ids = [sequence.get("id") for sequence in sequences]
    declared_shot_map = {
        shot.get("id"): shot
        for sequence in sequences
        for shot in sequence.get("shots", [])
        if isinstance(shot, dict) and shot.get("id")
    }
    if len(sequence_ids) != len(set(sequence_ids)):
        errors.append("scene directions contain duplicate sequence IDs")
    if sequence_ids != scope.get("sequence_ids", []):
        errors.append("scene direction sequence order does not match scope.sequence_ids")
    if any(sequence_id not in plan_groups for sequence_id in sequence_ids):
        errors.append("scene directions reference an unknown visual-plan sequence")

    expected_sequence_in = float(scope.get("in", -1))
    all_shot_ids: list[str] = []
    for sequence in sequences:
        sequence_id = sequence.get("id")
        units = plan_groups.get(sequence_id, [])
        sequence_in = float(sequence.get("in", -1))
        sequence_out = float(sequence.get("out", -1))
        if abs(sequence_in - expected_sequence_in) > 0.01:
            relation = "gap" if sequence_in > expected_sequence_in else "overlap"
            errors.append(f"{relation} before scene direction {sequence_id}")
        expected_sequence_in = sequence_out
        if not units:
            continue
        if sequence.get("unit_ids") != [unit.get("id") for unit in units]:
            errors.append(f"{sequence_id} unit_ids do not exactly match the visual plan")
        if abs(sequence_in - float(units[0].get("in", -1))) > 0.01:
            errors.append(f"{sequence_id} starts outside its visual-plan sequence")
        if abs(sequence_out - float(units[-1].get("out", -1))) > 0.01:
            errors.append(f"{sequence_id} ends outside its visual-plan sequence")

        anchor = sequence.get("narration_anchor", {})
        expected_word_start = int(units[0].get("narration_anchor", {}).get("word_start", -1))
        expected_word_end = int(units[-1].get("narration_anchor", {}).get("word_end", -1))
        if anchor.get("word_start") != expected_word_start or anchor.get("word_end") != expected_word_end:
            errors.append(f"{sequence_id} narration word range does not match its visual-plan units")
        if words and 0 <= expected_word_start <= expected_word_end < len(words):
            exact_quote = " ".join(str(words[index].get("word", "")) for index in range(expected_word_start, expected_word_end + 1))
            if anchor.get("quote") != exact_quote:
                errors.append(f"{sequence_id} narration quote is not exact")

        visual_sentence = sequence.get("visual_sentence", {})
        for field in ("subject_ids", "object_ids"):
            for object_id in visual_sentence.get(field, []):
                if object_id not in object_ids:
                    errors.append(f"{sequence_id} visual sentence has dangling {field} object {object_id}")
        continuity = sequence.get("continuity", {})
        for field in ("inherits_object_ids", "introduces_object_ids", "retires_object_ids"):
            for object_id in continuity.get(field, []):
                if object_id not in object_ids:
                    errors.append(f"{sequence_id} continuity has dangling {field} object {object_id}")

        shots = sequence.get("shots", [])
        expected_shot_in = sequence_in
        for shot in shots:
            shot_id = shot.get("id")
            all_shot_ids.append(shot_id)
            shot_in = float(shot.get("in", -1))
            shot_out = float(shot.get("out", -1))
            if abs(shot_in - expected_shot_in) > 0.01:
                relation = "gap" if shot_in > expected_shot_in else "overlap"
                errors.append(f"{relation} before {sequence_id}/{shot_id}")
            if shot_out <= shot_in:
                errors.append(f"{sequence_id}/{shot_id} has non-positive duration")
            if shot_out > sequence_out + 0.01:
                errors.append(f"{sequence_id}/{shot_id} exceeds its sequence")
            expected_shot_in = shot_out

            shot_anchor = shot.get("narration_anchor", {})
            word_start = shot_anchor.get("word_start", -1)
            word_end = shot_anchor.get("word_end", -1)
            if not isinstance(word_start, int) or not isinstance(word_end, int) or not words or word_start < 0 or word_end < word_start or word_end >= len(words):
                errors.append(f"{sequence_id}/{shot_id} has an invalid narration word range")
            else:
                exact_quote = " ".join(str(words[index].get("word", "")) for index in range(word_start, word_end + 1))
                if shot_anchor.get("quote") != exact_quote:
                    errors.append(f"{sequence_id}/{shot_id} narration quote is not exact")
                if float(words[word_start].get("start", -1)) < shot_in - 1.0:
                    errors.append(f"{sequence_id}/{shot_id} first cue word begins before the shot")
                if float(words[word_end].get("end", -1)) > shot_out + 1.0:
                    errors.append(f"{sequence_id}/{shot_id} last cue word ends after the shot")

            picture_audio = shot.get("picture_audio_contract", {})
            picture_audio_mode = picture_audio.get("mode")
            sound_intent = shot.get("sound_intent", {})
            exact_picture_audio_rules = {
                "narrated_observation": {
                    "language_carrier": "narrator",
                    "visible_speech": "prohibited",
                    "coverage_grammar": "observational_action",
                    "missing_line_expected": False,
                },
                "narrated_dramatization": {
                    "language_carrier": "narrator",
                    "coverage_grammar": "motivated_interaction",
                },
                "sync_dialogue": {
                    "language_carrier": "scene_participant",
                    "visible_speech": "required",
                    "coverage_grammar": "dialogue_exchange",
                    "missing_line_expected": True,
                },
                "presenter_address": {
                    "language_carrier": "presenter",
                    "visible_speech": "required",
                    "coverage_grammar": "direct_address",
                    "missing_line_expected": True,
                },
                "natural_sound_observation": {
                    "language_carrier": "natural_sound",
                    "coverage_grammar": "natural_sound_action",
                },
            }
            for field, expected_value in exact_picture_audio_rules.get(
                picture_audio_mode, {}
            ).items():
                actual_value = (
                    picture_audio.get("mute_test", {}).get(field)
                    if field == "missing_line_expected"
                    else picture_audio.get(field)
                )
                if actual_value != expected_value:
                    errors.append(
                        f"{sequence_id}/{shot_id} {picture_audio_mode} requires "
                        f"{field}={expected_value!r}"
                    )

            if picture_audio_mode == "natural_sound_observation" and picture_audio.get(
                "visible_speech"
            ) not in {"prohibited", "incidental_source_only", "source_synced"}:
                errors.append(
                    f"{sequence_id}/{shot_id} natural_sound_observation permits only "
                    "prohibited, incidental_source_only, or source_synced visible speech"
                )

            if picture_audio_mode == "narrated_dramatization":
                if picture_audio.get("visible_speech") not in {"prohibited", "illustrative_only"}:
                    errors.append(
                        f"{sequence_id}/{shot_id} narrated_dramatization permits only "
                        "prohibited or illustrative_only visible speech"
                    )
                dramatization = picture_audio.get("dramatization_context", {})
                if not isinstance(dramatization, dict):
                    # The schema already reports the wrong type; continue diagnostics safely.
                    dramatization = {}
                if (
                    dramatization.get("representation") != "illustrative"
                    or dramatization.get("essential_meaning") != "narration"
                ):
                    errors.append(
                        f"{sequence_id}/{shot_id} narrated_dramatization requires illustrative "
                        "representation and narration-carried essential meaning"
                    )

            face_function = picture_audio.get("face_function")
            if face_function == "dramatic_performance" and picture_audio_mode != "narrated_dramatization":
                errors.append(
                    f"{sequence_id}/{shot_id} dramatic_performance is permitted only for "
                    "narrated_dramatization"
                )
            if face_function == "source_delivery":
                if picture_audio_mode != "natural_sound_observation":
                    errors.append(
                        f"{sequence_id}/{shot_id} source_delivery is permitted only for "
                        "natural_sound_observation"
                    )
                if picture_audio.get("visible_speech") != "source_synced":
                    errors.append(
                        f"{sequence_id}/{shot_id} source_delivery requires "
                        "visible_speech='source_synced'"
                    )
                if picture_audio.get("mute_test", {}).get("missing_line_expected") is not True:
                    errors.append(
                        f"{sequence_id}/{shot_id} source_delivery must acknowledge the "
                        "missing synchronized line in its mute test"
                    )
            if face_function == "sync_delivery" and picture_audio_mode != "sync_dialogue":
                errors.append(
                    f"{sequence_id}/{shot_id} sync_delivery is permitted only for sync_dialogue"
                )
            if (
                picture_audio_mode == "natural_sound_observation"
                and face_function != "source_delivery"
                and picture_audio.get("mute_test", {}).get("missing_line_expected") is not False
            ):
                errors.append(
                    f"{sequence_id}/{shot_id} natural_sound_observation without source delivery "
                    "must pass the missing-line mute test"
                )

            if picture_audio_mode == "silent_graphic":
                language_carrier = picture_audio.get("language_carrier")
                if language_carrier not in {"narrator", "none"}:
                    errors.append(
                        f"{sequence_id}/{shot_id} silent_graphic requires "
                        "language_carrier='narrator' or 'none'"
                    )
                if picture_audio.get("visible_speech") != "not_applicable":
                    errors.append(
                        f"{sequence_id}/{shot_id} silent_graphic requires "
                        "visible_speech='not_applicable'"
                    )
                if picture_audio.get("coverage_grammar") != "graphic_progression":
                    errors.append(
                        f"{sequence_id}/{shot_id} silent_graphic requires "
                        "coverage_grammar='graphic_progression'"
                    )
                if picture_audio.get("face_function") != "none":
                    errors.append(
                        f"{sequence_id}/{shot_id} silent_graphic requires face_function='none'"
                    )
                if picture_audio.get("mute_test", {}).get("missing_line_expected") is not False:
                    errors.append(
                        f"{sequence_id}/{shot_id} silent_graphic must pass the mute test"
                    )

            sound_rules = {
                "narrated_observation": (True, {"none"}),
                "narrated_dramatization": (True, {"none"}),
                "sync_dialogue": (False, {"sync_scripted", "sync_source"}),
                "presenter_address": (False, {"presenter"}),
                "natural_sound_observation": (False, {"none", "sync_source"}),
            }
            if picture_audio_mode == "silent_graphic":
                sound_rules[picture_audio_mode] = (
                    picture_audio.get("language_carrier") == "narrator",
                    {"none"},
                )
            if picture_audio_mode in sound_rules:
                expected_narration, allowed_dialogue = sound_rules[picture_audio_mode]
                if sound_intent.get("narration") is not expected_narration:
                    errors.append(
                        f"{sequence_id}/{shot_id} {picture_audio_mode} requires "
                        f"sound_intent.narration={expected_narration!r}"
                    )
                if sound_intent.get("dialogue") not in allowed_dialogue:
                    errors.append(
                        f"{sequence_id}/{shot_id} {picture_audio_mode} has incompatible dialogue"
                    )
            if (
                picture_audio_mode == "natural_sound_observation"
                and sound_intent.get("ambience") != "source"
            ):
                errors.append(
                    f"{sequence_id}/{shot_id} natural_sound_observation requires source ambience"
                )
            if picture_audio_mode == "natural_sound_observation":
                visible_speech = picture_audio.get("visible_speech")
                expected_dialogue = (
                    "none" if visible_speech == "prohibited" else "sync_source"
                )
                if sound_intent.get("dialogue") != expected_dialogue:
                    errors.append(
                        f"{sequence_id}/{shot_id} {visible_speech} visible speech requires "
                        f"sound_intent.dialogue={expected_dialogue!r}"
                    )
            if (
                picture_audio_mode == "narrated_observation"
                and shot.get("camera", {}).get("framing") == "close"
                and picture_audio.get("face_function")
                not in {"none", "task_focus", "caused_reaction"}
            ):
                errors.append(
                    f"{sequence_id}/{shot_id} narrated_observation close framing may use a face only "
                    "for task focus or a caused reaction"
                )

            composition = shot.get("composition", {})
            layers = composition.get("layers", [])
            layer_map = {layer.get("id"): layer for layer in layers}
            if len(layer_map) != len(layers):
                errors.append(f"{sequence_id}/{shot_id} contains duplicate layer IDs")
            primary = composition.get("primary_layer_id")
            if primary not in layer_map:
                errors.append(f"{sequence_id}/{shot_id} primary layer is missing")
            hierarchy = composition.get("visual_hierarchy", [])
            if set(hierarchy) != set(layer_map):
                errors.append(f"{sequence_id}/{shot_id} visual hierarchy must order every layer exactly once")

            direction_facts = shot.get("direction_facts", {})
            master_setup = direction_facts.get("master_setup_relationship", {})
            master_role = master_setup.get("role")
            master_reference_id = master_setup.get("master_reference_id")
            if master_role == "setup":
                if master_reference_id in declared_shot_map:
                    referenced_role = (
                        declared_shot_map[master_reference_id]
                        .get("direction_facts", {})
                        .get("master_setup_relationship", {})
                        .get("role")
                    )
                    if referenced_role != "master":
                        errors.append(
                            f"{sequence_id}/{shot_id} setup references shot "
                            f"{master_reference_id} that is not declared as a master"
                        )
                elif master_reference_id in ticket_ids:
                    if master_reference_id not in shot.get("asset_ticket_ids", []):
                        errors.append(
                            f"{sequence_id}/{shot_id} setup master ticket "
                            f"{master_reference_id} is not listed in asset_ticket_ids"
                        )
                else:
                    errors.append(
                        f"{sequence_id}/{shot_id} setup has unknown master reference "
                        f"{master_reference_id}"
                    )
            elif master_reference_id is not None:
                errors.append(
                    f"{sequence_id}/{shot_id} {master_role} shot must not name a master reference"
                )

            for anchor in direction_facts.get("continuity_anchors", []):
                anchor_id = anchor.get("id")
                anchor_kind = anchor.get("kind")
                if anchor_kind == "world_object" and anchor_id not in object_ids:
                    errors.append(
                        f"{sequence_id}/{shot_id} has dangling world-object continuity "
                        f"anchor {anchor_id}"
                    )
                elif anchor_kind == "asset_ticket" and anchor_id not in ticket_ids:
                    errors.append(
                        f"{sequence_id}/{shot_id} has dangling asset-ticket continuity "
                        f"anchor {anchor_id}"
                    )
                elif anchor_kind == "shot_layer" and anchor_id not in layer_map:
                    errors.append(
                        f"{sequence_id}/{shot_id} has dangling shot-layer continuity "
                        f"anchor {anchor_id}"
                    )

            for layer in layers:
                layer_id = layer.get("id")
                source = layer.get("source", {})
                source_type = source.get("type")
                ref_id = source.get("ref_id")
                literal = source.get("literal")
                if source_type == "world_object" and ref_id not in object_ids:
                    errors.append(f"{sequence_id}/{shot_id}/{layer_id} has a dangling world object")
                elif source_type == "evidence" and ref_id not in evidence_ids:
                    errors.append(f"{sequence_id}/{shot_id}/{layer_id} has dangling evidence")
                elif source_type == "asset_ticket" and ref_id not in ticket_ids:
                    errors.append(f"{sequence_id}/{shot_id}/{layer_id} has a dangling asset ticket")
                elif source_type == "literal_text" and not literal:
                    errors.append(f"{sequence_id}/{shot_id}/{layer_id} has no literal text")
                elif source_type == "primitive" and (ref_id or literal):
                    errors.append(f"{sequence_id}/{shot_id}/{layer_id} primitive source must not carry ref_id or literal")
                for label in ("start_bounds", "end_bounds"):
                    bounds = layer.get(label, {})
                    if float(bounds.get("x", 0)) + float(bounds.get("width", 0)) > 1920.01:
                        errors.append(f"{sequence_id}/{shot_id}/{layer_id} exceeds frame width at {label}")
                    if float(bounds.get("y", 0)) + float(bounds.get("height", 0)) > 1080.01:
                        errors.append(f"{sequence_id}/{shot_id}/{layer_id} exceeds frame height at {label}")

            for text in shot.get("text_elements", []):
                layer_id = text.get("layer_id")
                layer = layer_map.get(layer_id)
                if not layer or layer.get("kind") != "text":
                    errors.append(f"{sequence_id}/{shot_id}/{text.get('id')} does not reference a text layer")
                    continue
                exact_text = text.get("exact_text", "")
                source = layer.get("source", {})
                if source.get("type") != "literal_text" or source.get("literal") != exact_text:
                    errors.append(f"{sequence_id}/{shot_id}/{text.get('id')} disagrees with its literal layer")
                size = int(text.get("font_size_px", 0))
                ranges = {
                    "headline": (72, 108),
                    "critical_number": (140, 240),
                    "label": (44, 60),
                    "source": (26, 34),
                    "annotation": (26, 60),
                    "show_identity": (72, 108),
                    "episode_title": (72, 108),
                }
                minimum, maximum = ranges.get(text.get("type_role"), (26, 240))
                if not minimum <= size <= maximum:
                    errors.append(f"{sequence_id}/{shot_id}/{text.get('id')} violates its type scale")
                for event in text.get("emphasis_events", []):
                    if event.get("target_substring") not in exact_text:
                        errors.append(f"{sequence_id}/{shot_id}/{text.get('id')} emphasizes missing text")
                    at = float(event.get("at_seconds", -1))
                    duration = float(event.get("duration_seconds", -1))
                    if at < shot_in - 0.01 or at + duration > shot_out + 0.01:
                        errors.append(f"{sequence_id}/{shot_id}/{text.get('id')} emphasis exceeds the shot")

            for beat in shot.get("motion_beats", []):
                beat_id = beat.get("id")
                at = float(beat.get("at_seconds", -1))
                duration = float(beat.get("duration_seconds", -1))
                if at < shot_in - 0.01 or at + duration > shot_out + 0.01:
                    errors.append(f"{sequence_id}/{shot_id}/{beat_id} exceeds the shot")
                for layer_id in beat.get("target_layer_ids", []):
                    if layer_id not in layer_map:
                        errors.append(f"{sequence_id}/{shot_id}/{beat_id} targets a missing layer {layer_id}")
                cue = beat.get("cue", {})
                word_index = cue.get("word_index", -1)
                if not isinstance(word_index, int) or not 0 <= word_index < len(words):
                    errors.append(f"{sequence_id}/{shot_id}/{beat_id} has an invalid cue word")
                else:
                    exact_word = str(words[word_index].get("word", ""))
                    exact_time = float(words[word_index].get("start", -1))
                    if cue.get("word") != exact_word:
                        errors.append(f"{sequence_id}/{shot_id}/{beat_id} cue word is not exact")
                    if abs(float(cue.get("cue_time_seconds", -1)) - exact_time) > 0.01:
                        errors.append(f"{sequence_id}/{shot_id}/{beat_id} cue time is not exact")
                    if not word_start <= word_index <= word_end:
                        errors.append(f"{sequence_id}/{shot_id}/{beat_id} cue word is outside the shot anchor")
                if beat.get("verb") not in {"hold", "cut"} and not beat.get("changes"):
                    errors.append(f"{sequence_id}/{shot_id}/{beat_id} has no explicit property change")

            for transition_name in ("transition_in", "transition_out"):
                transition = shot.get(transition_name, {})
                if transition.get("type") == "cut" and float(transition.get("duration_seconds", -1)) != 0:
                    errors.append(f"{sequence_id}/{shot_id} cut transition must have zero duration")
                for layer_id in transition.get("preserve_layer_ids", []):
                    if layer_id not in layer_map:
                        errors.append(f"{sequence_id}/{shot_id} {transition_name} preserves missing layer {layer_id}")

            for choreography in shot.get("evidence_choreography", []):
                if choreography.get("evidence_id") not in evidence_ids:
                    errors.append(f"{sequence_id}/{shot_id} has dangling evidence choreography")
                if choreography.get("source_layer_id") not in layer_map:
                    errors.append(f"{sequence_id}/{shot_id} evidence source layer is missing")
                ordered_stages = [step.get("stage") for step in choreography.get("steps", [])]
                required_order = ["source_appears", "highlight", "extract", "attach", "parameter_changes"]
                positions = [ordered_stages.index(stage) for stage in required_order if stage in ordered_stages]
                if positions != sorted(positions) or len(positions) < 3:
                    errors.append(f"{sequence_id}/{shot_id} evidence choreography is incomplete or out of order")
                for step in choreography.get("steps", []):
                    if step.get("target_layer_id") not in layer_map:
                        errors.append(f"{sequence_id}/{shot_id} evidence step targets a missing layer")
                    at = float(step.get("at_seconds", -1))
                    duration = float(step.get("duration_seconds", -1))
                    if at < shot_in - 0.01 or at + duration > shot_out + 0.01:
                        errors.append(f"{sequence_id}/{shot_id} evidence step exceeds the shot")
            for ticket_id in shot.get("asset_ticket_ids", []):
                if ticket_id not in ticket_ids:
                    errors.append(f"{sequence_id}/{shot_id} has dangling asset ticket {ticket_id}")

        if abs(expected_shot_in - sequence_out) > 0.01:
            errors.append(f"shots do not cover {sequence_id} through its exact end")

    if len(all_shot_ids) != len(set(all_shot_ids)):
        errors.append("shot IDs must be unique across the scene-direction scope")
    if sequences and abs(float(scope.get("out", -1)) - expected_sequence_in) > 0.01:
        errors.append("scene directions do not cover their declared scope")
    if directions.get("status") != "ready_for_prompt_compile":
        errors.append("scene directions must be ready_for_prompt_compile before build prompts")
    if errors:
        raise ValidationFailure("scene_directions", errors)


def _safe_relative(path_value: str) -> Path | None:
    path = Path(path_value)
    if path.is_absolute() or ".." in path.parts:
        return None
    return path


def validate_work_order(work_order: dict, episode_path: Path) -> None:
    errors = schema_errors(work_order, "agent-work-order.schema.json")
    errors.extend(clean_room_errors(work_order))
    work_id = work_order.get("work_order_id", "")
    folder = work_order.get("episode_folder", "")
    if folder != episode_path.name:
        errors.append("work order episode does not match the resolved episode")
    required_prefix = f"episodes/{folder}/agents/deliverables/{work_id}/"
    owned = work_order.get("owned_output_paths", [])
    for path_value in owned:
        if _safe_relative(path_value) is None or not path_value.startswith(required_prefix):
            errors.append(f"owned output escapes isolated deliverable directory: {path_value}")
    for path_value in work_order.get("forbidden_paths", []):
        if _safe_relative(path_value) is None:
            errors.append(f"forbidden path is not Blueprint Cinema-relative: {path_value}")
    for item in work_order.get("inputs", []):
        relative = _safe_relative(item.get("path", ""))
        if relative is None:
            errors.append(f"work-order input escapes Blueprint Cinema: {item.get('path')}")
            continue
        if work_order.get("status") == "issued":
            current = (BLUEPRINT_ROOT / relative).resolve()
            if not current.is_file():
                errors.append(f"work-order input is missing: {item.get('path')}")
            elif sha256_file(current) != item.get("sha256"):
                errors.append(f"work-order input hash is stale: {item.get('path')}")
    work_orders_dir = episode_path / "agents" / "work-orders"
    if work_orders_dir.is_dir() and work_order.get("status") == "issued":
        for other_path in work_orders_dir.glob("*.json"):
            try:
                other = load_json(other_path)
            except ValidationFailure:
                continue
            if other.get("work_order_id") == work_id or other.get("status") != "issued":
                continue
            for current_path in owned:
                for other_owned in other.get("owned_output_paths", []):
                    if current_path.startswith(other_owned) or other_owned.startswith(current_path):
                        errors.append(
                            f"owned path overlaps active work order {other.get('work_order_id')}: {current_path}"
                        )
    canonical_forbidden = {
        f"episodes/{folder}/episode.json",
        f"episodes/{folder}/input-lock.json",
        f"episodes/{folder}/production-state.json",
        f"episodes/{folder}/episode-engine.json",
        f"episodes/{folder}/world.json",
        f"episodes/{folder}/visual-plan.json",
        f"episodes/{folder}/asset-tickets.json",
        "src/",
        "schemas/",
        "renderer/src/Root.tsx",
        "renderer/src/index.ts",
    }
    forbidden = set(work_order.get("forbidden_paths", []))
    missing_forbidden = sorted(canonical_forbidden - forbidden)
    if missing_forbidden:
        errors.append("work order omits canonical forbidden paths: " + ", ".join(missing_forbidden))
    if errors:
        raise ValidationFailure("agent_work_order", errors)


def validate_deliverable(deliverable: dict, work_order: dict, episode_path: Path) -> None:
    errors = schema_errors(deliverable, "agent-deliverable.schema.json")
    errors.extend(clean_room_errors(deliverable))
    work_id = work_order.get("work_order_id")
    if deliverable.get("work_order_id") != work_id:
        errors.append("deliverable work_order_id does not match")
    if deliverable.get("episode_folder") != episode_path.name:
        errors.append("deliverable episode does not match")
    expected_inputs = {item.get("path"): item.get("sha256") for item in work_order.get("inputs", [])}
    used_inputs = {item.get("path"): item.get("sha256") for item in deliverable.get("input_hashes_used", [])}
    if used_inputs != expected_inputs:
        errors.append("deliverable input hashes do not exactly match its work order")
    if work_order.get("status") == "issued":
        for path_value, expected_hash in expected_inputs.items():
            relative = _safe_relative(path_value)
            current = (BLUEPRINT_ROOT / relative).resolve() if relative else None
            if current is None or not current.is_file() or sha256_file(current) != expected_hash:
                errors.append(f"deliverable input is stale: {path_value}")
    owned = work_order.get("owned_output_paths", [])
    packet_prefix = f"episodes/{episode_path.name}/agents/deliverables/{work_id}/"
    for path_value in deliverable.get("files_produced", []):
        relative = _safe_relative(path_value)
        if relative is None or not path_value.startswith(packet_prefix):
            errors.append(f"deliverable reports an output outside its packet: {path_value}")
            continue
        if not any(path_value == allowed or path_value.startswith(allowed.rstrip("/") + "/") for allowed in owned):
            errors.append(f"deliverable reports an unowned output: {path_value}")
        current = BLUEPRINT_ROOT / relative
        if not current.is_file():
            errors.append(f"deliverable output is missing: {path_value}")
    if deliverable.get("approval_claimed"):
        errors.append("worker packets cannot claim approvals")
    if deliverable.get("production_state_changed"):
        errors.append("worker packets cannot change production state")
    if errors:
        raise ValidationFailure("agent_deliverable", errors)
