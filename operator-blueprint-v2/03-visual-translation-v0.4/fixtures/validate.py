#!/usr/bin/env python3
"""Mechanical checks added by the proposed Step 3 v0.4 film-layer amendment.

This validator is additive. The v0.3 validator still checks the inherited business, world,
evidence, timing, and runtime-exclusion contracts. This file checks the standalone v0.4 V1
process/upstream/application lock, typed semantic-event binding, picture/audio intent, and V7
preservation fields.

It proves structure and byte identity. It cannot prove that a picture job is useful, a mode choice
is editorially right, or a direction treatment will work on screen.
"""

import hashlib
import json
import pathlib
import sys


REPOSITORY_ROOT = pathlib.Path(__file__).resolve().parents[3]
FIXTURE_ROOT = pathlib.Path(__file__).resolve().parent

CANONICAL = {
    "manifest": REPOSITORY_ROOT / "design-system/boundary-ledger/manifest.json",
    "semantic_core": REPOSITORY_ROOT / "design-system/boundary-ledger/semantic-core.json",
    "motion_binding": REPOSITORY_ROOT / "design-system/boundary-ledger/bindings/motion.json",
    "illustration_language": REPOSITORY_ROOT / "design-system/boundary-ledger/illustration-language.md",
    "illustration_reference_manifest": REPOSITORY_ROOT / "design-system/boundary-ledger/illustration/episode-006/manifest.json",
    "scene_contract": REPOSITORY_ROOT / "design-system/boundary-ledger/scene-contracts.md",
    "production_skills": REPOSITORY_ROOT / "design-system/boundary-ledger/production-skills.md",
    "oe_skills_lock": REPOSITORY_ROOT / ".agents/oe-skills-lock.json",
}

AUTHORITY_FIELDS = {
    "manifest": ("manifest_path", "manifest_sha256"),
    "semantic_core": ("semantic_core_path", "semantic_core_sha256"),
    "motion_binding": ("motion_binding_path", "motion_binding_sha256"),
    "illustration_language": ("illustration_language_path", "illustration_language_sha256"),
    "illustration_reference_manifest": (
        "illustration_reference_manifest_path",
        "illustration_reference_manifest_sha256",
    ),
    "scene_contract": ("scene_contract_path", "scene_contract_sha256"),
    "production_skills": ("production_skills_path", "production_skills_sha256"),
}

REQUIRED_FREEZE = (
    "editorial_lock",
    "operator_canvas",
    "episode_investment_thesis",
    "narrative_spine",
    "episode_beat_sheet",
    "claims_map",
    "script",
    "canonical_w",
    "spoken_identity",
    "narration_lock",
    "narration_master",
    "word_transcript",
    "intentional_pause_map",
)

CANONICAL_PROCESS_PATH = "../../../03-visual-translation-v0.4/PROCESS-MANIFEST.json"

CANONICAL_FREEZE_PATHS = {
    "editorial_lock": "../01-editorial/editorial-lock.md",
    "operator_canvas": "../01-editorial/operator-canvas.md",
    "episode_investment_thesis": "../01-editorial/episode-investment-thesis.md",
    "narrative_spine": "../01-editorial/narrative-spine.md",
    "episode_beat_sheet": "../01-editorial/episode-beat-sheet.md",
    "claims_map": "../01-editorial/claims-map.md",
    "script": "../01-editorial/script.md",
    "canonical_w": "../01-editorial/canonical-w.txt",
    "spoken_identity": "../01-editorial/spoken-identity.json",
    "narration_lock": "../02-narration-production/narration-lock.md",
    "narration_master": "../02-narration-production/master/narration-master.v4.wav",
    "word_transcript": "../02-narration-production/word-transcript.json",
    "intentional_pause_map": "../02-narration-production/intentional-pause-map.json",
}

REQUIRED_LOCKED_SKILL_FILES = {
    ".agents/skills/oe-boundary-ledger/SKILL.md",
    ".agents/skills/oe-film-direction/SKILL.md",
    ".agents/skills/oe-film-direction/references/generated-plates.md",
    ".agents/skills/oe-film-direction/references/picture-audio-modes.md",
    ".agents/skills/oe-film-direction/references/source-ledger.json",
    ".agents/scripts/validate-oe-skills-lock.mjs",
}

EXPECTED_SOURCE_IDS = {
    "openmontage",
    "visual-skills",
    "ai-cinematic-pipeline",
    "narrative-film-direction",
}

VISUAL_MODES = {"reality", "system", "proof", "outcome", "identity"}


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else None


def merge(base, patch):
    if not isinstance(base, dict) or not isinstance(patch, dict):
        return patch
    result = dict(base)
    for key, value in patch.items():
        result[key] = merge(result.get(key), value) if key in result else value
    return result


class Fixture:
    def __init__(self, directory):
        self.directory = pathlib.Path(directory).resolve()
        self.is_test_fixture = self.directory == FIXTURE_ROOT or FIXTURE_ROOT in self.directory.parents
        self.case_file_present = (self.directory / "case.json").is_file()
        self.case = read_json(self.directory / "case.json") or {} if self.is_test_fixture else {}
        base = self.case.get("base")
        self.base = (self.directory / base).resolve() if base else None
        self.base_case = read_json(self.base / "case.json") if self.base else {}
        self.base_case = self.base_case or {}
        self.patches = self.case.get("patches") or {}

    def load(self, name):
        value = read_json(self.base / name) if self.base else None
        local = read_json(self.directory / name)
        if local is not None:
            value = merge(value or {}, local)
        if name in self.patches:
            value = merge(value or {}, self.patches[name])
        return value or {}

    def expected(self):
        return sorted(set(self.case.get("expect_failures") or []))

    def setting(self, name, default=None):
        if name in self.case:
            return self.case[name]
        return self.base_case.get(name, default)

    def resolve(self, relative_path):
        local = (self.directory / str(relative_path)).resolve()
        if local.exists() or not self.base:
            return local
        return (self.base / str(relative_path)).resolve()


def check_pinned_file(findings, fixture, gate, label, path_value, hash_value, canonical):
    if not path_value or not hash_value:
        findings.append((gate, f"application lock is missing {label} path/hash"))
        return None
    path = fixture.resolve(path_value)
    if path != canonical.resolve():
        findings.append((gate, f"{label} is not the canonical path: {path}"))
    if not path.is_file():
        findings.append((gate, f"{label} does not exist: {path}"))
        return None
    actual = sha256(path)
    if actual != hash_value:
        findings.append((gate, f"{label} hash drift: recorded={hash_value} actual={actual}"))
    return path


def validate_picture_audio(unit):
    """Yield structural errors for one Step 3 picture/audio intent."""
    uid = unit.get("id", "?")
    required = (
        "picture_audio_mode",
        "language_carrier",
        "visible_speech",
        "mute_test_missing_line_expected",
    )
    for field in required:
        if field not in unit:
            yield f"unit '{uid}' is missing picture/audio field '{field}'"
    if any(field not in unit for field in required):
        return

    mode = unit["picture_audio_mode"]
    carrier = unit["language_carrier"]
    speech = unit["visible_speech"]
    missing = unit["mute_test_missing_line_expected"]

    if mode == "narrated_observation":
        allowed = carrier == "narrator" and speech == "prohibited" and missing is False
    elif mode == "sync_dialogue":
        allowed = carrier == "scene_participant" and speech == "required" and missing is True
    elif mode == "presenter_address":
        allowed = carrier == "presenter" and speech == "required" and missing is True
    elif mode == "natural_sound_observation":
        allowed_speech = {"prohibited", "incidental_source_only", "source_synced"}
        expected_missing = speech == "source_synced"
        allowed = (
            carrier == "natural_sound"
            and speech in allowed_speech
            and missing is expected_missing
        )
    elif mode == "silent_graphic":
        allowed = carrier in {"narrator", "none"} and speech == "not_applicable" and missing is False
    else:
        yield f"unit '{uid}' selects unknown picture/audio mode '{mode}'"
        return

    if not allowed:
        yield (
            f"unit '{uid}' has an incompatible picture/audio tuple: "
            f"{mode}/{carrier}/{speech}/missing_line={missing!r}"
        )


def check(directory):
    fixture = Fixture(directory)
    findings = []
    if fixture.case_file_present and not fixture.is_test_fixture:
        findings.append(("V1", "production episode directory may not contain fixture case.json"))
    engine = fixture.load("engine.json")
    input_record = fixture.load("input-lock.json")
    v1_record = input_record or engine
    plan = fixture.load("visual-plan.json")
    final_lock = fixture.load("lock.json")

    # V1: the complete standalone input record plus exact Boundary Ledger application bytes and
    # the OE-owned skill package. Process fixtures without input-lock.json continue to exercise
    # the additive application fields on engine.json.
    if input_record:
        process_lock = input_record.get("process_lock") or {}
        process_path = process_lock.get("path")
        process_hash = process_lock.get("sha256")
        expected_process_path = fixture.setting("canonical_process_path", CANONICAL_PROCESS_PATH)
        if not process_path or not process_hash:
            findings.append(("V1", "standalone input lock is missing process path/hash"))
        else:
            if process_path != expected_process_path:
                findings.append(("V1", f"process lock is not the canonical path: {process_path}"))
            resolved_process = fixture.resolve(process_path)
            if not resolved_process.is_file():
                findings.append(("V1", f"process lock does not exist: {resolved_process}"))
            elif sha256(resolved_process) != process_hash:
                findings.append(("V1", "process-lock hash drift"))
            else:
                process_doc = read_json(resolved_process) or {}
                if process_doc.get("process_version") != input_record.get("process_version"):
                    findings.append(("V1", "process-lock version differs from the standalone input lock"))

        freeze = input_record.get("input_lock") or {}
        expected_freeze_paths = fixture.setting("canonical_input_paths", CANONICAL_FREEZE_PATHS)
        if not freeze:
            findings.append(("V1", "standalone input lock records no upstream freeze"))
        else:
            for key in REQUIRED_FREEZE:
                entry = freeze.get(key)
                if not isinstance(entry, dict) or not entry.get("path") or not entry.get("sha256"):
                    findings.append(("V1", f"input_lock is missing a path/hash for '{key}'"))
                    continue
                if entry["path"] != expected_freeze_paths.get(key):
                    findings.append(("V1", f"input_lock '{key}' is not the canonical path: {entry['path']}"))
                frozen_path = fixture.resolve(entry["path"])
                if not frozen_path.is_file():
                    findings.append(("V1", f"input_lock '{key}' does not exist: {frozen_path}"))
                elif sha256(frozen_path) != entry["sha256"]:
                    findings.append(("V1", f"input_lock '{key}' hash drift"))
            duration = freeze.get("narration_duration_seconds")
            if not isinstance(duration, (int, float)) or duration <= 0:
                findings.append(("V1", "input_lock does not record a positive narration duration"))

    boundary = v1_record.get("boundary_ledger_lock") or {}
    resolved = {}
    for label, (path_field, hash_field) in AUTHORITY_FIELDS.items():
        resolved[label] = check_pinned_file(
            findings,
            fixture,
            "V1",
            label.replace("_", " "),
            boundary.get(path_field),
            boundary.get(hash_field),
            CANONICAL[label],
        )

    skills = v1_record.get("oe_skills_lock") or {}
    skill_path = check_pinned_file(
        findings,
        fixture,
        "V1",
        "OE skills lock",
        skills.get("path"),
        skills.get("sha256"),
        CANONICAL["oe_skills_lock"],
    )
    if skills.get("status") != "locked":
        findings.append(("V1", "engine does not record OE skills lock status as 'locked'"))

    skill_doc = read_json(skill_path) if skill_path else None
    if skill_doc:
        if skill_doc.get("status") != "locked":
            findings.append(("V1", "canonical OE skills lock is not locked"))
        declared = {entry.get("path"): entry.get("sha256") for entry in skill_doc.get("files") or []}
        if set(declared) != REQUIRED_LOCKED_SKILL_FILES:
            findings.append(("V1", "OE skills lock membership differs from the required six files"))
        for relative_path, expected_hash in declared.items():
            path = (REPOSITORY_ROOT / str(relative_path)).resolve()
            if not path.is_file() or sha256(path) != expected_hash:
                findings.append(("V1", f"OE skills lock member drift: {relative_path}"))
        source_ledger = skill_doc.get("sourceLedger") or {}
        source_path = (REPOSITORY_ROOT / str(source_ledger.get("path", "missing"))).resolve()
        if not source_path.is_file() or sha256(source_path) != source_ledger.get("sha256"):
            findings.append(("V1", "OE source-ledger hash drift"))
        else:
            source_doc = read_json(source_path) or {}
            ids = {entry.get("id") for entry in source_doc.get("sources") or []}
            if source_doc.get("authority") != "reference-only" or ids != EXPECTED_SOURCE_IDS:
                findings.append(("V1", "OE source ledger authority or source membership changed"))

    manifest_path = resolved.get("manifest")
    manifest = read_json(manifest_path) if manifest_path else None
    if manifest:
        production = manifest.get("productionInstructions") or {}
        if production.get("status") != "locked":
            findings.append(("V1", "Boundary Ledger production instructions are not locked"))
        if (production.get("lock") or {}).get("sha256") != skills.get("sha256"):
            findings.append(("V1", "Boundary Ledger manifest does not pin the recorded OE skills lock"))
        if production.get("motionBindingStatus") != "provisional" or production.get("soundBindingStatus") != "provisional":
            findings.append(("V1", "Boundary Ledger motion/sound implementation status was upgraded"))

    reference_path = resolved.get("illustration_reference_manifest")
    reference = read_json(reference_path) if reference_path else None
    if reference:
        if reference.get("status") != "locked-reference":
            findings.append(("V1", "illustration reference manifest is not a locked reference"))
        asset = reference.get("asset") or {}
        asset_path = (reference_path.parent / str(asset.get("file", "missing"))).resolve()
        if not asset_path.is_file() or sha256(asset_path) != asset.get("sha256"):
            findings.append(("V1", "illustration reference asset does not match its manifest"))
        recorded_asset_hash = boundary.get("illustration_reference_asset_sha256")
        if not recorded_asset_hash:
            findings.append(("V1", "application lock is missing illustration reference asset hash"))
        elif recorded_asset_hash != asset.get("sha256"):
            findings.append(("V1", "illustration reference asset hash differs from its manifest"))

    semantic = read_json(resolved.get("semantic_core")) if resolved.get("semantic_core") else None
    motion = read_json(resolved.get("motion_binding")) if resolved.get("motion_binding") else None
    system_version = boundary.get("system_version")
    if semantic and (semantic.get("system") != "Boundary Ledger" or semantic.get("version") != system_version):
        findings.append(("V1", "Boundary Ledger semantic-core identity/version differs from the lock"))
    if motion:
        if motion.get("medium") != "motion" or motion.get("systemVersion") != system_version:
            findings.append(("V1", "Boundary Ledger motion-binding identity/version differs from the lock"))
        upstream_status = motion.get("implementationStatus") or motion.get("status")
        if boundary.get("motion_binding_status") != upstream_status:
            findings.append(("V1", "Boundary Ledger motion-binding status differs from the lock"))

    # V4: two mode axes and one honest semantic event per unit.
    business = {item.get("id"): item for item in engine.get("business_operations") or []}
    establishments = {item.get("id"): item for item in engine.get("establishment") or []}
    for unit in plan.get("units") or []:
        uid = unit.get("id", "?")
        if unit.get("mode") not in VISUAL_MODES:
            findings.append(("V4", f"unit '{uid}' has unknown visual-world mode '{unit.get('mode')}'"))
        if not isinstance(unit.get("unit_job"), str) or len(unit.get("unit_job", "").strip()) < 24:
            findings.append(("V4", f"unit '{uid}' has no substantive unit_job"))
        findings.extend(("V4", error) for error in validate_picture_audio(unit))

        bo_id = unit.get("business_operation_id")
        est_id = unit.get("establishment_id")
        if bool(bo_id) == bool(est_id):
            findings.append(("V4", f"unit '{uid}' must bind exactly one business operation or establishment"))
            continue
        if bo_id:
            operation = business.get(bo_id)
            if not operation:
                findings.append(("V4", f"unit '{uid}' references unknown business operation '{bo_id}'"))
                continue
            if "viewer_state_before" in unit or "viewer_state_after" in unit:
                findings.append(("V4", f"unit '{uid}' mixes viewer state into a business operation"))
            for unit_field, operation_field in (
                ("world_state_before", "state_before"),
                ("world_state_after", "state_after"),
                ("boundary_ledger_operation_id", "boundary_ledger_operation_id"),
            ):
                if unit.get(unit_field) != operation.get(operation_field):
                    findings.append(("V4", f"unit '{uid}' field '{unit_field}' diverges from '{bo_id}'"))
        else:
            establishment = establishments.get(est_id)
            if not establishment:
                findings.append(("V4", f"unit '{uid}' references unknown establishment '{est_id}'"))
                continue
            if "world_state_before" in unit or "world_state_after" in unit:
                findings.append(("V4", f"unit '{uid}' gives establishment a business/world state change"))
            for unit_field in (
                "viewer_state_before",
                "viewer_state_after",
                "boundary_ledger_operation_id",
            ):
                if unit.get(unit_field) != establishment.get(unit_field):
                    findings.append(("V4", f"unit '{uid}' field '{unit_field}' diverges from '{est_id}'"))

    # V7: exact application pins survive the final Step 3 lock.
    locked = final_lock.get("application_authority_lock") or {}
    expected_v7 = {
        "manifest_sha256": boundary.get("manifest_sha256"),
        "semantic_core_sha256": boundary.get("semantic_core_sha256"),
        "motion_binding_sha256": boundary.get("motion_binding_sha256"),
        "illustration_language_sha256": boundary.get("illustration_language_sha256"),
        "illustration_reference_manifest_sha256": boundary.get("illustration_reference_manifest_sha256"),
        "illustration_reference_asset_sha256": boundary.get("illustration_reference_asset_sha256"),
        "scene_contract_sha256": boundary.get("scene_contract_sha256"),
        "production_skills_sha256": boundary.get("production_skills_sha256"),
        "oe_skills_lock_sha256": skills.get("sha256"),
    }
    for field, expected in expected_v7.items():
        if locked.get(field) != expected:
            findings.append(("V7", f"visual-translation lock does not preserve '{field}'"))

    return findings


def main():
    args = sys.argv[1:]
    through = None
    if args[:1] == ["--through"]:
        if len(args) < 2 or args[1] not in {f"V{i}" for i in range(1, 8)}:
            print("Usage: validate.py [--through V1..V7] <fixture-or-episode-directory>", file=sys.stderr)
            return 2
        through = int(args[1][1:])
        args = args[2:]
    if len(args) != 1:
        print("Usage: validate.py [--through V1..V7] <fixture-or-episode-directory>", file=sys.stderr)
        return 2
    fixture = Fixture(args[0])
    findings = check(args[0])
    if through is not None:
        findings = [(gate, message) for gate, message in findings if int(gate[1:]) <= through]
    got = sorted({gate for gate, _ in findings})
    expected = fixture.expected()
    print(fixture.directory.name)
    for gate, message in findings:
        print(f"   {gate}  {message}")
    ok = got == expected
    print(f"   -> gates failing: {got or 'none'} | expected: {expected or 'none'} | {'PASS' if ok else 'MISMATCH'}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
