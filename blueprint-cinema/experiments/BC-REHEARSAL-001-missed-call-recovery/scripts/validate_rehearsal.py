#!/usr/bin/env python3
"""Fail-closed, experiment-local validation for BC-REHEARSAL-001.

This deliberately does not extend Blueprint Cinema's shared v1 runtime. It enforces
the rehearsal contracts over isolated files and prints every check it performs.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_ID = "BC-REHEARSAL-001"
EXPECTED_WARNING = "SYNTHETIC TEST FIXTURE — NOT EVIDENCE"
PROHIBITED_RUNTIME_REFERENCES = (
    "coverage_map.json",
    "render_data/blueprint.json",
    "OEOpeningPilot",
    "BlueprintComposition",
    "prepare_longform.py",
    "build_rev_e_storyboard.py",
    "studio/originate/direct-booking-recovery/blueprint-cinema",
    "EP006-direct-booking-recovery",
)


class Failure(Exception):
    pass


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise Failure(f"cannot read valid JSON at {path.relative_to(ROOT)}: {exc}") from exc


def require(condition: bool, message: str) -> None:
    if not condition:
        raise Failure(message)


def check(label: str, fn) -> None:
    try:
        fn()
    except Failure:
        raise
    except Exception as exc:  # fail closed on unanticipated validation errors
        raise Failure(f"{label}: validator error: {exc}") from exc
    print(f"PASS  {label}")


def ffprobe_duration(path: Path) -> float:
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return float(result.stdout.strip())


def ffprobe_json(path: Path) -> dict:
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_format", "-show_streams", "-of", "json", str(path)],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(result.stdout)


def validate_identity() -> None:
    experiment = load_json(ROOT / "experiment.json")
    lock = load_json(ROOT / "input-lock.json")
    require(experiment.get("experiment_id") == EXPECTED_ID, "experiment identity mismatch")
    require(experiment.get("frame_rate") == 30, "frame rate must be 30")
    require((experiment.get("width"), experiment.get("height")) == (1920, 1080), "resolution must be 1920x1080")
    require(60 <= float(lock.get("duration_seconds", 0)) <= 75, "duration must be 60–75 seconds")
    require(experiment.get("status") in {"inputs_locked", "direction_reviewed", "build_validated", "render_reviewed"}, "invalid rehearsal status")


def validate_input_lock() -> None:
    lock = load_json(ROOT / "input-lock.json")
    require(lock.get("experiment_id") == EXPECTED_ID, "input-lock identity mismatch")
    require(lock.get("status") == "inputs_locked", "input lock is not locked")
    require(lock.get("frame_rate") == 30, "input lock frame rate mismatch")
    artifacts = lock.get("artifacts")
    require(isinstance(artifacts, list) and len(artifacts) >= 5, "input lock needs at least five artifacts")
    for artifact in artifacts:
        path = ROOT / artifact["path"]
        require(path.is_file(), f"locked artifact missing: {artifact['path']}")
        require(sha256(path) == artifact["sha256"], f"locked hash stale: {artifact['path']}")
        require(path.stat().st_size == artifact["size_bytes"], f"locked size stale: {artifact['path']}")
    narration_artifact = next((item for item in artifacts if item.get("role") == "exact_locked_synthetic_narration"), None)
    require(narration_artifact is not None and narration_artifact["sha256"] == sha256(ROOT / "inputs/narration.txt"), "narration is not hash-locked")
    audio_path = ROOT / lock["timing_authority"]["audio_path"]
    actual_duration = ffprobe_duration(audio_path)
    require(abs(actual_duration - lock["duration_seconds"]) < 0.001, "VO duration differs from probe")
    require("whisper.cpp 1.8.5" in lock["generation"]["alignment_method"], "unapproved or unversioned alignment method")
    words = load_json(ROOT / lock["timing_authority"]["word_table_path"])
    entries = words.get("words")
    require(isinstance(entries, list) and len(entries) == 158, "word table must contain 158 canonical words")
    previous = 0.0
    for index, word in enumerate(entries):
        require(word["index"] == index, f"word index mismatch at {index}")
        require(0 <= word["start"] <= word["end"] <= actual_duration + 1e-6, f"word {index} timing out of bounds")
        require(word["start"] + 1e-6 >= previous, f"word {index} begins before prior word")
        previous = word["end"]
    report = load_json(ROOT / "inputs/alignment-report.json")
    require(report.get("undeclared_mismatches") == [], "alignment has undeclared mismatches")
    require(report.get("status") == "matched_with_declared_asr_corrections", "alignment mismatch report is not approved for rehearsal")


def validate_fixture() -> None:
    path = ROOT / "assets/fixtures/fixture-missed-call-log.csv"
    rows = path.read_text(encoding="utf-8").splitlines()
    require(len(rows) >= 3, "fixture needs header and multiple fictional rows")
    require("fixture_notice" in rows[0], "fixture notice column missing")
    for number, row in enumerate(rows[1:], start=2):
        require(EXPECTED_WARNING in row, f"fixture row {number} lacks exact synthetic warning")
    forbidden_realism = ("@", "+1", "http://", "https://", "$", "LLC", "Inc.")
    joined = "\n".join(rows)
    require(not any(token in joined for token in forbidden_realism), "fixture contains a real-company/contact/result signal")


def validate_engine() -> None:
    engine = load_json(ROOT / "direction/episode-engine.json")
    require(engine.get("experiment_id") == EXPECTED_ID, "engine identity mismatch")
    for key in ("operator", "customer", "owned_value", "constraint", "outcome_object", "primary_visual_mechanic", "human_gate", "guardrail"):
        require(len(str(engine.get(key, ""))) >= 24, f"engine {key} is not substantive")
    operations = engine.get("counter_system", [])
    require([item.get("id") for item in operations] == ["capture", "classify", "acknowledge", "human_review", "offer_slot", "stop_or_book"], "counter-system order changed")
    verbs = set(engine.get("motion_verbs", []))
    require({"capture", "classify", "acknowledge", "hold", "review", "release", "offer", "stop", "book", "measure"} <= verbs, "engine lacks required motion verbs")
    require(len(engine.get("honesty_tests", [])) >= 6, "engine needs six honesty tests")
    require("Prezi map tour" in engine.get("prohibited_framings", []), "Prezi prohibition missing")


def validate_world() -> None:
    world = load_json(ROOT / "direction/world.json")
    require(world.get("experiment_id") == EXPECTED_ID, "world identity mismatch")
    objects = world.get("objects", [])
    object_ids = [item.get("id") for item in objects]
    require(len(object_ids) == len(set(object_ids)), "duplicate world object IDs")
    require({"call-tag-red", "work-order-card", "human-review-gate", "fixture-missed-call-log", "one-week-measure"} <= set(object_ids), "required persistent world objects missing")
    edge_ids = [edge.get("id") for edge in world.get("edges", [])]
    require(len(edge_ids) == len(set(edge_ids)), "duplicate world edge IDs")
    for edge in world.get("edges", []):
        require(edge.get("from") in object_ids and edge.get("to") in object_ids, f"dangling edge {edge.get('id')}")
    evidence_ids = [entry.get("id") for entry in world.get("evidence", [])]
    require(len(evidence_ids) == len(set(evidence_ids)), "duplicate evidence IDs")
    for entry in world.get("evidence", []):
        require(entry.get("object_id") in object_ids, f"evidence {entry.get('id')} has dangling object")
        require(entry.get("synthetic") is True and entry.get("public_claim") is False, f"evidence {entry.get('id')} honesty flags invalid")
    camera_ids = [camera.get("id") for camera in world.get("camera_anchors", [])]
    require(len(camera_ids) == len(set(camera_ids)), "duplicate camera IDs")
    for camera in world.get("camera_anchors", []):
        require(camera.get("target") in object_ids, f"camera {camera.get('id')} has dangling target")
    paths = world.get("required_paths", {})
    for name, path in paths.items():
        require(all(object_id in object_ids for object_id in path), f"required path {name} has dangling object")
    uncertain = paths.get("uncertain_recovery", [])
    require(uncertain.index("human-review-gate") < uncertain.index("slot-offer-node"), "uncertain route bypasses human review")
    require(paths.get("decline_stop", [])[-1:] == ["stop-terminal"], "decline route is not terminal")


def validate_plan() -> None:
    plan = load_json(ROOT / "direction/visual-plan.json")
    lock = load_json(ROOT / "input-lock.json")
    words_doc = load_json(ROOT / "inputs/words.json")
    world = load_json(ROOT / "direction/world.json")
    engine = load_json(ROOT / "direction/episode-engine.json")
    tickets = load_json(ROOT / "direction/asset-tickets.json")
    units = plan.get("units", [])
    require(len(units) == 7, "visual plan must have seven shots")
    duration = float(lock["duration_seconds"])
    require(abs(float(plan.get("duration_seconds", 0)) - duration) < 1e-6, "plan duration differs from locked VO")
    require(abs(units[0]["in"]) < 1e-9, "plan does not start at zero")
    require(abs(units[-1]["out"] - duration) < 1e-6, "plan does not end at locked VO")
    object_ids = {item["id"] for item in world["objects"]}
    evidence_ids = {item["id"] for item in world["evidence"]}
    camera_ids = {item["id"] for item in world["camera_anchors"]}
    ticket_ids = {item["id"] for item in tickets["tickets"]}
    verbs = set(engine["motion_verbs"])
    all_words = words_doc["words"]
    expected_word = 0
    previous_out = 0.0
    designed_transitions = 0
    for unit in units:
        require(abs(unit["in"] - previous_out) < 1e-6, f"gap/overlap before {unit['id']}")
        require(unit["out"] > unit["in"], f"non-positive shot duration {unit['id']}")
        require(unit["out"] <= duration + 1e-6, f"shot beyond VO {unit['id']}")
        start = unit["word_range"]["from"]
        end = unit["word_range"]["to"]
        require(start == expected_word and end >= start, f"word gap/overlap at {unit['id']}")
        require(end < len(all_words), f"word range beyond table at {unit['id']}")
        require(unit["focus"] in object_ids, f"invalid focus in {unit['id']}")
        require(unit["camera_anchor"] in camera_ids, f"invalid camera in {unit['id']}")
        require(set(unit.get("carry", [])) <= object_ids, f"invalid carried object in {unit['id']}")
        require(set(unit.get("world_state_before", {})) <= object_ids, f"invalid before-state object in {unit['id']}")
        require(set(unit.get("world_state_after", {})) <= object_ids, f"invalid after-state object in {unit['id']}")
        require(set(unit.get("evidence_ids", [])) <= evidence_ids, f"invalid evidence in {unit['id']}")
        require(set(unit.get("asset_ticket_ids", [])) <= ticket_ids, f"invalid ticket in {unit['id']}")
        require(unit["motion_verb"] in verbs, f"invalid motion verb in {unit['id']}")
        for event in unit.get("events", []):
            require(unit["in"] - 1e-6 <= event["at"] <= unit["out"] + 1e-6, f"event outside {unit['id']}")
            require(event["verb"] in verbs, f"event verb invalid in {unit['id']}")
            require(start <= event["word"] <= end, f"event word outside {unit['id']}")
        if unit.get("transition") not in (None, "cut"):
            designed_transitions += 1
        expected_word = end + 1
        previous_out = unit["out"]
    require(expected_word == len(all_words), "plan does not cover every locked word")
    require(designed_transitions <= 2, "more than two designed transitions")
    combined = json.dumps(units).lower()
    for concept in ("permission", "voicemail", "human-review-gate", "stop-terminal", "scheduled", "one-week"):
        require(concept in combined, f"plan omits required concept: {concept}")


def validate_tickets() -> None:
    document = load_json(ROOT / "direction/asset-tickets.json")
    tickets = document.get("tickets", [])
    require(len(tickets) == 6, "six rehearsal asset tickets required")
    ids = [ticket.get("id") for ticket in tickets]
    require(len(ids) == len(set(ids)), "duplicate ticket IDs")
    required = (
        "editorial_job", "required_shots", "required_duration_seconds", "semantic_requirements",
        "exclusions", "rights_and_release_requirements", "source_preference", "technical_requirements",
        "crop_and_focal_needs", "handles_seconds", "synthetic_reconstruction_policy",
        "acceptance_tests", "placeholder_behavior", "status",
    )
    for ticket in tickets:
        for key in required:
            require(key in ticket and ticket[key] not in (None, "", [], {}), f"ticket {ticket.get('id')} missing {key}")
        require(ticket["status"] in {"placeholder_only", "ticket_only"}, f"ticket {ticket.get('id')} was improperly sourced")


def validate_direction_documents() -> None:
    required = (
        "direction/DIRECTION-BIBLE.md",
        "direction/RHYTHM-MAP.md",
        "direction/SEQUENCE-TREATMENT.md",
        "direction/SEQUENCE-SHOT-DIRECTION.md",
        "hyperframes/style-frames/01-reality.png",
        "hyperframes/style-frames/02-system-proof.png",
        "hyperframes/style-frames/03-gate-outcome.png",
        "hyperframes/shot-board/static-shot-board.png",
        "hyperframes/style-frames/01-reality-v2.png",
        "hyperframes/style-frames/02-system-proof-v2.png",
        "hyperframes/style-frames/03-gate-outcome-v2.png",
        "hyperframes/shot-board/approved-direction-board.png",
        "review/WAVE1-DIRECTION-INTEGRATION.md",
    )
    for relative in required:
        require((ROOT / relative).is_file(), f"direction artifact missing: {relative}")
    bible = (ROOT / "direction/DIRECTION-BIBLE.md").read_text(encoding="utf-8")
    for heading in ("Visual thesis", "Reality-world treatment", "System-world treatment", "Proof-bench treatment", "Palette roles", "Typography roles", "Camera grammar", "Screen direction", "Motion verbs", "Transition rules", "Sound intent", "Visual anti-rules"):
        require(heading.lower() in bible.lower(), f"direction bible missing {heading}")
    require(len(re.findall(r"(?m)^\d+\. No ", bible)) >= 10, "direction bible has fewer than ten anti-rules")
    rhythm = (ROOT / "direction/RHYTHM-MAP.md").read_text(encoding="utf-8").lower()
    for dimension in ("energy", "information density", "visual mode", "scale", "proof", "human contact", "tension", "sound", "breathing room", "transition responsibility"):
        require(dimension in rhythm, f"rhythm map missing {dimension}")
    shots = (ROOT / "direction/SEQUENCE-SHOT-DIRECTION.md").read_text(encoding="utf-8")
    require(sum(1 for line in shots.splitlines() if line.startswith("## Shot ")) == 7, "scene directions must contain seven shots")
    required_fields = ("Absolute time", "Locked words", "Viewer knowledge before", "Viewer knowledge after", "Business state before", "Operation shown", "Business state after", "Shot grammar", "Primary subject", "Primary relationship", "Consequence", "Visual hierarchy", "Entry frame", "Action frame", "Consequence frame", "Settle frame", "Exit / handoff frame", "Prior-shot continuity", "Next-shot responsibility", "Layer geometry", "Typography", "Word-cued motion", "Camera behavior", "Evidence behavior", "Sound intent", "Negative constraints", "Observable review tests")
    for field in required_fields:
        require(shots.count(f"**{field}:**") == 7, f"scene directions missing repeated field: {field}")


def validate_clean_room() -> None:
    paths = [ROOT / "experiment.json", ROOT / "input-lock.json"]
    paths += list((ROOT / "direction").glob("*"))
    paths += [ROOT / "hyperframes/BRIEF.md", ROOT / "hyperframes/SCRIPT.md", ROOT / "hyperframes/frame.md"]
    for path in paths:
        if not path.is_file() or path.suffix not in {".json", ".md", ".html"}:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for prohibited in PROHIBITED_RUNTIME_REFERENCES:
            require(prohibited not in text, f"prohibited legacy reference {prohibited!r} in {path.relative_to(ROOT)}")


def validate_no_network_runtime() -> None:
    runtime_paths = [ROOT / "hyperframes/index.html"]
    runtime_paths += list((ROOT / "hyperframes/compositions").rglob("*.html"))
    for path in runtime_paths:
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        require("http://" not in text and "https://" not in text, f"render-time network URL in {path.relative_to(ROOT)}")


def validate_agent_contracts() -> None:
    orders_dir = ROOT / "agents/work-orders"
    deliverables_dir = ROOT / "agents/deliverables"
    if not orders_dir.exists():
        return
    orders = []
    owned = []
    for path in sorted(orders_dir.glob("*.json")):
        order = load_json(path)
        orders.append(order)
        require(order.get("experiment_id") == EXPECTED_ID, f"work order identity mismatch: {path.name}")
        require(order.get("permissions") == ["read_pinned_inputs", "write_owned_deliverable_only"], f"unsafe permissions in {path.name}")
        require(order.get("may_approve_gate") is False and order.get("may_change_state") is False, f"worker authority leak in {path.name}")
        worker_owned = order.get("owned_output_paths", [])
        require(worker_owned, f"no owned paths in {path.name}")
        for relative in worker_owned:
            require(relative.startswith(f"agents/deliverables/{order['work_order_id']}/"), f"owned path escapes packet: {relative}")
            require(relative not in owned, f"overlapping worker path: {relative}")
            owned.append(relative)
        packet = deliverables_dir / order["work_order_id"] / "deliverable.json"
        if packet.exists():
            deliverable = load_json(packet)
            require(deliverable.get("work_order_id") == order["work_order_id"], f"deliverable ID mismatch: {packet}")
            require(deliverable.get("approval_claimed") is False and deliverable.get("production_state_changed") is False, f"worker claimed gate/state: {packet}")
            verified = set()
            for item in deliverable.get("input_hashes_verified", []):
                actual = item.get("actual_sha256", item.get("sha256"))
                expected = item.get("expected_sha256", actual)
                require(item.get("status", "pass") == "pass", f"worker reported a failed pin: {order['work_order_id']}:{item.get('path')}")
                require(actual and actual == expected, f"worker pin report is internally inconsistent: {order['work_order_id']}:{item.get('path')}")
                verified.add((item.get("path"), actual))
            ordered = {(item["path"], item["sha256"]) for item in order.get("input_hashes", [])}
            require(verified == ordered, f"worker did not verify the issued hashes: {order['work_order_id']}")
            for output in deliverable.get("outputs", []):
                output_path = ROOT / output["path"]
                require(output_path.is_file(), f"declared worker output is missing: {output['path']}")
                require(sha256(output_path) == output["sha256"], f"declared worker output hash is stale: {output['path']}")
            actual_files = sorted(str(item.relative_to(ROOT)) for item in packet.parent.iterdir() if item.is_file())
            require(set(actual_files) <= set(worker_owned), f"worker wrote outside owned files: {order['work_order_id']}")
        else:
            for pinned in order.get("input_hashes", []):
                source = ROOT / pinned["path"]
                require(source.is_file() and sha256(source) == pinned["sha256"], f"stale unstarted worker input: {pinned['path']}")


def validate_hyperframes_build() -> None:
    index_path = ROOT / "hyperframes/index.html"
    text = index_path.read_text(encoding="utf-8")
    require('data-composition-id="main"' in text, "HyperFrames root composition is missing")
    require('data-duration="61.411354"' in text, "HyperFrames root duration differs from lock")
    require(text.count('class="clip scene-slot"') == 7, "HyperFrames root must mount exactly seven shot slots")
    require(text.count('id="call-tag-red"') == 1, "persistent call tag must have one root owner")
    require(text.count('id="work-order-card"') == 1, "persistent work-order card must have one root owner")
    require(text.count('id="proof-pin"') == 1, "persistent proof pin must have one root owner")
    require('src="assets/audio/vo.wav"' in text, "root does not use the staged locked VO")
    require(sha256(ROOT / "hyperframes/assets/audio/vo.wav") == "af1ad4ebcf7cac540299ad048505ba67dd6eaa6f2396ad6f83238fa6658785df", "staged VO hash differs from lock")
    for number in range(1, 8):
        shot = ROOT / f"hyperframes/compositions/shots/shot-{number:02d}.html"
        motion = ROOT / f"hyperframes/compositions/shots/motion/shot-{number:02d}-motion.json"
        require(shot.is_file(), f"canonical shot composition missing: {shot.relative_to(ROOT)}")
        require(motion.is_file(), f"canonical shot motion map missing: {motion.relative_to(ROOT)}")
        shot_text = shot.read_text(encoding="utf-8")
        require("http://" not in shot_text and "https://" not in shot_text, f"runtime network URL in {shot.relative_to(ROOT)}")
        require("paused: true" in shot_text, f"shot timeline is not seek-safe paused construction: {shot.relative_to(ROOT)}")
        snapshots = ROOT / f"hyperframes/snapshots/review/shot-{number:02d}"
        require(snapshots.is_dir(), f"snapshot directory missing for shot {number:02d}")
        review_frames = list(snapshots.glob("frame-*.png")) + list(snapshots.glob("frame-*.jpg"))
        require(len(review_frames) >= 5, f"required snapshot views missing for shot {number:02d}")
        require((snapshots / "contact-sheet.jpg").is_file(), f"shot contact sheet missing for shot {number:02d}")
    storyboard = (ROOT / "hyperframes/STORYBOARD.md").read_text(encoding="utf-8")
    require(storyboard.count("animated") >= 7, "storyboard does not mark every bounded shot animated")
    require((ROOT / "review/animation-map/animation-map.json").is_file(), "assembled animation map missing")
    require((ROOT / "review/ANIMATION-MAP-REVIEW.md").is_file(), "animation-map review missing")


def validate_render() -> None:
    render = ROOT / "hyperframes/renders/BC-REHEARSAL-001-directed-animatic-final.mp4"
    contact = ROOT / "hyperframes/renders/BC-REHEARSAL-001-contact-sheet-final.jpg"
    phone = ROOT / "review/phone-legibility-final/contact-sheet-480.jpg"
    require(render.is_file() and render.stat().st_size > 1_000_000, "full review MP4 missing or implausibly small")
    require(sha256(render) == "a9f21223385ff12dd60b7c0f3572d1cd14e70e5fb72907ddc76ebe85cbe824b3", "review MP4 hash changed")
    require(contact.is_file() and sha256(contact) == "683d084e547fc6ef16b842337d8e0fcf5f748311d8d6246490d95d983cce955f", "render contact sheet missing or changed")
    require(phone.is_file() and sha256(phone) == "06495e0892015b32033430328f04a8164696aef81d79a2359345bbb16933a2fc", "phone-scale contact sheet missing or changed")
    probe = ffprobe_json(render)
    streams = probe.get("streams", [])
    video = next((stream for stream in streams if stream.get("codec_type") == "video"), None)
    audio = next((stream for stream in streams if stream.get("codec_type") == "audio"), None)
    require(video is not None and audio is not None, "render must contain video and audio")
    require((video.get("width"), video.get("height")) == (1920, 1080), "render dimensions differ from experiment")
    require(video.get("avg_frame_rate") == "30/1" and int(video.get("nb_frames", 0)) == 1843, "render frame rate/count mismatch")
    require(audio.get("sample_rate") == "48000", "render audio sample rate mismatch")
    lock = load_json(ROOT / "input-lock.json")
    require(abs(float(probe["format"]["duration"]) - float(lock["duration_seconds"])) <= 1 / 30 + 1e-6, "render duration differs from lock by more than one frame")
    recorded = load_json(ROOT / "handoff/media-probe.json")
    require(recorded.get("sha256") == sha256(render), "recorded media probe points at a stale render")
    require(recorded.get("status") == "implemented_and_validated", "media probe is not validated")


def validate_handoff() -> None:
    manifest = load_json(ROOT / "handoff/handoff-manifest.json")
    require(manifest.get("experiment_id") == EXPECTED_ID, "handoff identity mismatch")
    require(manifest.get("resolve_was_launched") is False, "handoff improperly claims Resolve was launched")
    require(manifest.get("interchange_claimed") is False, "handoff improperly claims interchange")
    require(manifest.get("public_delivery_allowed") is False, "handoff improperly allows public delivery")
    allowed = {"implemented_and_validated", "manually_assembled_and_structurally_checked", "documentation_only", "blocked"}
    for item in manifest.get("package", []):
        require(item.get("classification") in allowed, f"invalid package classification: {item.get('path')}")
        path = ROOT / item["path"]
        require(path.is_file(), f"handoff package item missing: {item['path']}")
        require(sha256(path) == item["sha256"], f"handoff package hash stale: {item['path']}")
    for capability in manifest.get("capabilities", []):
        require(capability.get("classification") in allowed, f"invalid capability classification: {capability.get('capability')}")
    events = load_json(ROOT / "handoff/timeline-events.json")
    plan = load_json(ROOT / "direction/visual-plan.json")
    require(len(events.get("events", [])) == 7, "handoff must contain seven timeline events")
    previous_frame = 0
    for event, unit in zip(events["events"], plan["units"]):
        require(event["shot_id"] == unit["id"], f"handoff event/plan shot mismatch: {event['event_id']}")
        require(abs(event["record_in_seconds"] - unit["in"]) < 1e-6 and abs(event["record_out_seconds"] - unit["out"]) < 1e-6, f"handoff source seconds changed: {event['event_id']}")
        require(event["record_in_frame"] == previous_frame, f"handoff frame gap/overlap at {event['event_id']}")
        require(event["record_out_frame_exclusive"] > event["record_in_frame"], f"non-positive handoff event: {event['event_id']}")
        previous_frame = event["record_out_frame_exclusive"]
    require(previous_frame == 1843, "handoff does not cover complete rendered frame extent")
    marker_rows = (ROOT / "handoff/markers.csv").read_text(encoding="utf-8").splitlines()
    require(len(marker_rows) == 8, "marker CSV must contain header plus seven markers")
    placeholders = load_json(ROOT / "handoff/placeholder-asset-manifest.json")
    ticket_ids = {item["id"] for item in load_json(ROOT / "direction/asset-tickets.json")["tickets"]}
    require({item["ticket_id"] for item in placeholders.get("items", [])} == ticket_ids, "placeholder manifest does not cover every ticket")
    require(placeholders.get("public_delivery_blocked") is True, "synthetic placeholders must block public delivery")
    require(not list((ROOT / "handoff").glob("*.otio")) and not list((ROOT / "handoff").glob("*.fcpxml")), "unsupported interchange file was fabricated")


def validate_final_reviews() -> None:
    required = (
        "review/HYPERFRAMES-TECHNICAL-REPORT.md",
        "review/ANIMATION-MAP-REVIEW.md",
        "review/DIRECTED-ANIMATIC-REVIEW.md",
        "review/AGENT-REHEARSAL-REPORT.md",
        "review/FINAL-EXPERIMENT-REPORT.md",
        "handoff/EDIT-RESOLVE-HANDOFF.md",
        "handoff/MISSING-IMPLEMENTATION.md",
    )
    for relative in required:
        require((ROOT / relative).is_file(), f"final review artifact missing: {relative}")
    animatic = (ROOT / "review/DIRECTED-ANIMATIC-REVIEW.md").read_text(encoding="utf-8").lower()
    for review_pass in ("comprehension", "rhythm", "continuity", "visual hierarchy", "motion", "evidence and honesty", "phone-sized legibility", "rendered compression"):
        require(review_pass in animatic, f"directed-animatic review missing separate pass: {review_pass}")
    report = (ROOT / "review/FINAL-EXPERIMENT-REPORT.md").read_text(encoding="utf-8")
    require("PARTIAL — the visual rehearsal worked, but specified production controls remain manual" in report, "final verdict missing or inflated")
    require("14" in report and "Resolve handoff readiness" in report, "final report does not record all rehearsal gates")
    experiment = load_json(ROOT / "experiment.json")
    require(experiment.get("status") == "render_reviewed", "experiment status is not render_reviewed")


def validate_completed_agent_wave() -> None:
    orders = sorted((ROOT / "agents/work-orders").glob("*.json"))
    require(len(orders) == 9, "expected two Wave 1, three Wave 2, two initial Wave 3, and two post-correction verification work orders")
    for order_path in orders:
        order = load_json(order_path)
        packet = ROOT / "agents/deliverables" / order["work_order_id"] / "deliverable.json"
        require(packet.is_file(), f"worker packet incomplete: {order['work_order_id']}")
        deliverable = load_json(packet)
        require(deliverable.get("status") == "complete", f"worker packet not complete: {order['work_order_id']}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", choices=("direction", "agents", "build", "final"), default="direction")
    args = parser.parse_args()
    checks = [
        ("experiment identity", validate_identity),
        ("input-lock integrity", validate_input_lock),
        ("synthetic fixture honesty", validate_fixture),
        ("engine honesty", validate_engine),
        ("persistent-world integrity", validate_world),
        ("full-timeline visual-plan coverage", validate_plan),
        ("asset-ticket completeness", validate_tickets),
        ("direction artifact completeness", validate_direction_documents),
        ("clean-room isolation", validate_clean_room),
        ("render-time network prohibition", validate_no_network_runtime),
    ]
    if args.phase in {"agents", "build", "final"}:
        checks.append(("bounded agent contracts", validate_agent_contracts))
    if args.phase in {"build", "final"}:
        checks.extend([
            ("HyperFrames bounded build", validate_hyperframes_build),
            ("whole-render media integrity", validate_render),
            ("Resolve handoff structure", validate_handoff),
        ])
    if args.phase == "final":
        checks.extend([
            ("all agent waves complete", validate_completed_agent_wave),
            ("final review package", validate_final_reviews),
        ])
    try:
        for label, fn in checks:
            check(label, fn)
    except Failure as exc:
        print(f"FAIL  {exc}", file=sys.stderr)
        return 1
    print(f"RESULT PASS phase={args.phase} root={ROOT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
