#!/usr/bin/env python3
"""Step 3 mechanical gate checks.

Implements only gate conditions that are mechanically decidable. It clears
HYGIENE. It cannot establish whether direction is any good -- that is the
separate creative decision every Step 3 gate records.

Usage:
  validate.py <fixture-dir>          # current v0.2 contract
  validate.py --legacy <fixture-dir> # preserved v0.1 evidence only
"""

import hashlib
import json
import pathlib
import re
import sys


DOCUMENTS = (
    "canvas.json",
    "engine.json",
    "world.json",
    "visual-plan.json",
    "look.json",
    "lock.json",
    "claims.json",
)


PROHIBITED_V02_KEYS = {
    "visualmechanic",
    "motionverbs",
    "localmotionvocabulary",
    "motionvocabulary",
    "motionlexicon",
    "implementationprimitives",
    "animationprimitives",
    "animationcomponents",
    "animationconstructs",
    "animationvocabulary",
    "animationlexicon",
    "sceneprimitives",
    "scenecomponents",
    "sceneconstructs",
    "scenevocabulary",
    "scenelexicon",
    "rendererprimitives",
    "renderercomponents",
    "rendererconstructs",
    "renderervocabulary",
    "rendererlexicon",
    "easingpresets",
    "audioprimitives",
}

REPOSITORY_ROOT = pathlib.Path(__file__).resolve().parents[3]
CANONICAL_SEMANTIC_CORE = (REPOSITORY_ROOT / "design-system/boundary-ledger/semantic-core.json").resolve()
CANONICAL_MOTION_BINDING = (REPOSITORY_ROOT / "design-system/boundary-ledger/bindings/motion.json").resolve()


def read_json(path):
    return json.loads(path.read_text()) if path.is_file() else None


def merge(base, patch):
    if not isinstance(base, dict) or not isinstance(patch, dict):
        return patch
    result = dict(base)
    for key, value in patch.items():
        result[key] = merge(result.get(key), value) if key in result else value
    return result


class Fixture:
    """Loads a standalone control or a small patch over a preserved baseline."""

    def __init__(self, directory):
        self.directory = pathlib.Path(directory)
        self.case = read_json(self.directory / "case.json") or {}
        base = self.case.get("base")
        self.base = (self.directory / base).resolve() if base else None
        self.patches = self.case.get("patches") or {}

    def load(self, name):
        value = read_json(self.base / name) if self.base else None
        local = read_json(self.directory / name)
        if local is not None:
            value = merge(value or {}, local)
        if name in self.patches:
            value = merge(value or {}, self.patches[name])
        return value

    def expected(self):
        if "expect_failures" in self.case:
            return self.case["expect_failures"]
        return (self.load("expect.json") or {}).get("expect_failures", [])

    def resolve_authority(self, relative_path):
        return (self.directory / relative_path).resolve()

    def resolve_source(self, relative_path):
        local = (self.directory / relative_path).resolve()
        if local.is_file() or not self.base:
            return local
        return (self.base / relative_path).resolve()


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def walk_keys(value, path="engine"):
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{path}.{key}"
            yield key, child_path
            yield from walk_keys(child, child_path)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from walk_keys(child, f"{path}[{index}]")


def normalize_key(value):
    return re.sub(r"[^a-z0-9]", "", str(value).lower())


def resolve_locator(document, locator):
    value = document
    for part in str(locator).split("."):
        if not part or not isinstance(value, dict) or part not in value:
            return None
        value = value[part]
    return value


def check(directory, legacy=False):
    fixture = Fixture(directory)
    findings = []
    canvas = fixture.load("canvas.json") or {}
    engine = fixture.load("engine.json") or {}
    world = fixture.load("world.json") or {}
    plan = fixture.load("visual-plan.json") or {}
    look = fixture.load("look.json") or {}
    lock = fixture.load("lock.json") or {}
    claims = set((fixture.load("claims.json") or {}).get("claim_ids", []))
    contract_v02 = not legacy

    core = {}
    motion_binding = {}
    boundary_lock = engine.get("boundary_ledger_lock") or {}

    # V1 -- current validation is fail-closed; legacy validation is explicit.
    if contract_v02:
        if engine.get("contract_version") != "0.2":
            findings.append(("V1", f"current artifact contract_version is {engine.get('contract_version')!r}; expected '0.2'"))
        required = (
            "system_version",
            "semantic_core_path",
            "semantic_core_sha256",
            "motion_binding_path",
            "motion_binding_sha256",
        )
        for key in required:
            if not boundary_lock.get(key):
                findings.append(("V1", f"Boundary Ledger lock is missing '{key}'"))

        core_path = fixture.resolve_authority(boundary_lock.get("semantic_core_path", "missing"))
        motion_path = fixture.resolve_authority(boundary_lock.get("motion_binding_path", "missing"))
        if core_path != CANONICAL_SEMANTIC_CORE:
            findings.append(("V1", f"semantic core is not the canonical Boundary Ledger path: {core_path}"))
        if motion_path != CANONICAL_MOTION_BINDING:
            findings.append(("V1", f"motion binding is not the canonical Boundary Ledger path: {motion_path}"))
        for label, path, expected_hash in (
            ("semantic core", core_path, boundary_lock.get("semantic_core_sha256")),
            ("motion binding", motion_path, boundary_lock.get("motion_binding_sha256")),
        ):
            if not path.is_file():
                findings.append(("V1", f"Boundary Ledger {label} does not exist: {path}"))
                continue
            actual_hash = sha256(path)
            if expected_hash != actual_hash:
                findings.append(("V1", f"Boundary Ledger {label} hash drift: recorded={expected_hash} actual={actual_hash}"))
            if label == "semantic core":
                core = read_json(path) or {}
            else:
                motion_binding = read_json(path) or {}

        system_version = boundary_lock.get("system_version")
        if core and (core.get("system") != "Boundary Ledger" or core.get("version") != system_version):
            findings.append(("V1", "Boundary Ledger semantic-core identity/version does not match the lock"))
        if motion_binding and (
            motion_binding.get("medium") != "motion"
            or motion_binding.get("systemVersion") != system_version
        ):
            findings.append(("V1", "Boundary Ledger motion-binding medium/version does not match the lock"))

    # V2 -- derived business fields must match the Canvas.
    for key, value in (engine.get("derived") or {}).items():
        if canvas.get(key) != value:
            findings.append(("V2", f"derived field '{key}' diverges from Canvas: engine={value!r} canvas={canvas.get(key)!r}"))

    if contract_v02:
        # V2 -- derive business operations; select Boundary Ledger semantics.
        authored_artifacts = {
            "engine.json": engine,
            "world.json": world,
            "visual-plan.json": plan,
            "look.json": look,
            "lock.json": lock,
        }
        for artifact_name, artifact in authored_artifacts.items():
            for key, path in walk_keys(artifact, path=artifact_name):
                if normalize_key(key) in PROHIBITED_V02_KEYS:
                    findings.append(("V2", f"Step 3 authors prohibited field '{path}'"))

        states = canvas.get("state_changes") or {}
        roles = {item.get("id") for item in core.get("roles", [])}
        operations = {item.get("id"): item for item in core.get("operations", [])}
        permitted = {
            role: set((spec or {}).get("expression") or [])
            for role, spec in (motion_binding.get("roles") or {}).items()
        }
        business_operations = engine.get("business_operations") or []
        if not business_operations:
            findings.append(("V2", "engine has no derived business_operations"))
        operation_map = {}
        for item in business_operations:
            operation_id = item.get("id")
            if not operation_id:
                findings.append(("V2", "business operation is missing an episode-local ID"))
                continue
            if operation_id in operation_map:
                findings.append(("V2", f"business operation ID '{operation_id}' is duplicated"))
            operation_map[operation_id] = item

            upstream_id = item.get("upstream_state_id")
            upstream = states.get(upstream_id)
            if not upstream:
                findings.append(("V2", f"business operation '{operation_id}' has unknown upstream state '{upstream_id}'"))
            else:
                for field in ("state_before", "state_after", "business_operation"):
                    if item.get(field) != upstream.get(field):
                        findings.append(("V2", f"business operation '{operation_id}' field '{field}' diverges from upstream state '{upstream_id}'"))
            if item.get("label") != "DERIVED":
                findings.append(("V2", f"business operation '{operation_id}' is not labelled DERIVED"))
            if item.get("selection_label") != "SELECTED":
                findings.append(("V2", f"business operation '{operation_id}' Boundary Ledger choice is not labelled SELECTED"))

            source_artifact = item.get("source_artifact")
            source_hash = item.get("source_sha256")
            source_locator = item.get("source_locator")
            rationale = item.get("mapping_rationale")
            if not source_artifact or not source_hash or not source_locator:
                findings.append(("V2", f"business operation '{operation_id}' is missing source artifact/hash/locator provenance"))
            else:
                source_path = fixture.resolve_source(source_artifact)
                if not source_path.is_file():
                    findings.append(("V2", f"business operation '{operation_id}' source artifact does not exist: {source_path}"))
                else:
                    if sha256(source_path) != source_hash:
                        findings.append(("V2", f"business operation '{operation_id}' source artifact hash drift"))
                    source_document = read_json(source_path)
                    located = resolve_locator(source_document, source_locator) if source_document is not None else None
                    if not isinstance(located, dict):
                        findings.append(("V2", f"business operation '{operation_id}' source locator '{source_locator}' does not resolve"))
                    elif upstream and any(located.get(field) != upstream.get(field) for field in ("state_before", "state_after", "business_operation")):
                        findings.append(("V2", f"business operation '{operation_id}' source locator does not resolve to upstream state '{upstream_id}'"))
            if not isinstance(rationale, str) or len(rationale.strip()) < 24:
                findings.append(("V2", f"business operation '{operation_id}' lacks a substantive Boundary Ledger mapping rationale"))

            role_id = item.get("boundary_ledger_semantic_role_id")
            boundary_operation_id = item.get("boundary_ledger_operation_id")
            if role_id not in roles:
                findings.append(("V2", f"business operation '{operation_id}' selects unknown Boundary Ledger role '{role_id}'"))
            if boundary_operation_id not in operations:
                findings.append(("V2", f"business operation '{operation_id}' selects unknown Boundary Ledger operation '{boundary_operation_id}'"))
            elif boundary_operation_id not in permitted.get(role_id, set()):
                findings.append(("V2", f"Boundary Ledger binding does not permit '{boundary_operation_id}' for role '{role_id}'"))

        visual_model = engine.get("episode_visual_model")
        if not isinstance(visual_model, dict):
            findings.append(("V2", "engine has no authored episode_visual_model"))
        else:
            if visual_model.get("label") != "AUTHORED":
                findings.append(("V2", "episode_visual_model is not labelled AUTHORED"))
            if not visual_model.get("name"):
                findings.append(("V2", "episode_visual_model has no name"))
            if not isinstance(visual_model.get("mechanical_honesty"), str) or len(visual_model.get("mechanical_honesty", "").strip()) < 32:
                findings.append(("V2", "episode_visual_model lacks a substantive mechanical-honesty statement"))
            bound_operations = set(visual_model.get("business_operation_ids") or [])
            if bound_operations != set(operation_map):
                findings.append(("V2", f"episode_visual_model operation bindings {sorted(bound_operations)} do not match engine operations {sorted(operation_map)}"))
            if not visual_model.get("persistent_actors"):
                findings.append(("V2", "episode_visual_model has no persistent actors"))
            if not visual_model.get("zones_and_relationships"):
                findings.append(("V2", "episode_visual_model has no zones or relationships"))
    else:
        # Preserved v0.1 controls remain executable history.
        mechanic = engine.get("visual_mechanic") or {}
        if re.search(r"flywheel|gravity|compound", str(mechanic.get("name", "")), re.I) and not mechanic.get("compounding_evidence"):
            findings.append(("V2", f"mechanic '{mechanic.get('name')}' implies compounding with no evidence"))
        verbs = {item["verb"] for item in (engine.get("motion_verbs") or [])}
        if verbs and not 3 <= len(verbs) <= 6:
            findings.append(("V2", f"{len(verbs)} motion verbs; must be 3 to 6"))
        operation_map = {}

    # V3 -- world integrity.
    objects = {item["id"]: item for item in (world.get("objects") or [])}
    if contract_v02:
        operation_ids = set(operation_map)
        for item in objects.values():
            if not item.get("static") and not (set(item.get("operation_bindings") or []) & operation_ids):
                findings.append(("V3", f"object '{item['id']}' is neither operation-reachable nor marked static"))
        for operation_id, operation in operation_map.items():
            for target in operation.get("acts_on") or []:
                if target not in objects:
                    findings.append(("V3", f"business operation '{operation_id}' acts on unknown object '{target}'"))
    else:
        verbs = {item["verb"] for item in (engine.get("motion_verbs") or [])}
        for item in objects.values():
            if not item.get("static") and not (set(item.get("verbs") or []) & verbs):
                findings.append(("V3", f"object '{item['id']}' is neither verb-reachable nor marked static"))
        for verb in engine.get("motion_verbs") or []:
            for target in verb.get("acts_on") or []:
                if target not in objects:
                    findings.append(("V3", f"verb '{verb['verb']}' acts on unknown object '{target}'"))
    for anchor in world.get("evidence_anchors") or []:
        if anchor.get("claim_id") not in claims:
            findings.append(("V3", f"evidence anchor '{anchor.get('id')}' binds to unknown claim '{anchor.get('claim_id')}'"))

    # V4 -- plan integrity.
    for unit in plan.get("units") or []:
        unit_id = unit.get("id")
        if "in_word" not in unit or "out_word" not in unit:
            findings.append(("V4", f"unit '{unit_id}' timing is not bound to word indices"))
        if unit.get("timing_source") and unit["timing_source"] != "transcript":
            findings.append(("V4", f"unit '{unit_id}' timing_source is '{unit['timing_source']}', not transcript"))
        inert = unit.get("world_state_before") == unit.get("world_state_after") and not unit.get("evidence")
        if inert and not unit.get("inert_justification"):
            findings.append(("V4", f"unit '{unit_id}' is inert: no state change and no evidence, unjustified"))

        if contract_v02:
            if "motion_verb" in unit:
                findings.append(("V4", f"unit '{unit_id}' authors legacy motion_verb instead of selecting an engine binding"))
            operation_id = unit.get("business_operation_id")
            operation = operation_map.get(operation_id)
            if not operation:
                findings.append(("V4", f"unit '{unit_id}' references unknown business operation '{operation_id}'"))
            else:
                if unit.get("boundary_ledger_operation_id") != operation.get("boundary_ledger_operation_id"):
                    findings.append(("V4", f"unit '{unit_id}' Boundary Ledger operation does not match engine binding '{operation_id}'"))
                for state_field in ("world_state_before", "world_state_after"):
                    operation_field = state_field.removeprefix("world_")
                    if unit.get(state_field) != operation.get(operation_field):
                        findings.append(("V4", f"unit '{unit_id}' {state_field} diverges from engine operation '{operation_id}'"))
        else:
            verbs = {item["verb"] for item in (engine.get("motion_verbs") or [])}
            if unit.get("motion_verb") and verbs and unit["motion_verb"] not in verbs:
                findings.append(("V4", f"unit '{unit_id}' uses verb '{unit['motion_verb']}' not in the engine"))

        for object_id in (unit.get("carry") or []) + (unit.get("focus") or []):
            if object_id not in objects:
                findings.append(("V4", f"unit '{unit_id}' references unknown object '{object_id}'"))
        for evidence in unit.get("evidence") or []:
            upstream = evidence.get("upstream_label")
            current = evidence.get("label")
            rank = {"UNKNOWN": 0, "MODELED": 1, "PARALLEL": 2, "OBSERVED": 3}
            if upstream and current and rank.get(current, 0) > rank.get(upstream, 0):
                findings.append(("V4", f"unit '{unit_id}' upgrades evidence label {upstream} -> {current}"))

    # V6 -- look must be provisional and v0.2 intent must trace to the engine.
    if look and look.get("approval") not in (None, "provisional"):
        findings.append(("V6", f"look approval is '{look['approval']}'; must be provisional"))
    if contract_v02:
        for intent in look.get("motion_intents") or []:
            operation_id = intent.get("business_operation_id")
            operation = operation_map.get(operation_id)
            if not operation:
                findings.append(("V6", f"look intent references unknown business operation '{operation_id}'"))
            elif intent.get("boundary_ledger_operation_id") != operation.get("boundary_ledger_operation_id"):
                findings.append(("V6", f"look intent Boundary Ledger operation does not match engine binding '{operation_id}'"))

    # V7 -- no runtime named and Boundary Ledger hashes remain consistent.
    runtimes = r"\b(hyperframes|remotion|after ?effects|davinci|resolve|fusion|blender|unreal)\b"
    for name in DOCUMENTS + ("direction-bible.md",):
        value = fixture.load(name)
        if value is not None:
            content = value if isinstance(value, str) else json.dumps(value, sort_keys=True)
        else:
            path = fixture.directory / name
            content = path.read_text() if path.is_file() else ""
        for match in set(re.findall(runtimes, content, re.I)):
            findings.append(("V7", f"runtime '{match}' named in {name}"))

    if contract_v02:
        locked_boundary = lock.get("boundary_ledger_lock") or {}
        for key in ("semantic_core_sha256", "motion_binding_sha256"):
            if locked_boundary.get(key) != boundary_lock.get(key):
                findings.append(("V7", f"visual-translation lock does not preserve Boundary Ledger '{key}'"))
    for key, value in (lock.get("audio_only") or {}).items():
        if value is False:
            findings.append(("V7", f"audio-only rule broken: '{key}' exists only in a visual"))
    return findings


if __name__ == "__main__":
    args = sys.argv[1:]
    legacy = bool(args and args[0] == "--legacy")
    if legacy:
        args = args[1:]
    if len(args) != 1:
        print("Usage: validate.py [--legacy] <fixture-dir>", file=sys.stderr)
        sys.exit(2)
    directory = args[0]
    failures = check(directory, legacy=legacy)
    expected = Fixture(directory).expected()
    got = sorted({gate for gate, _ in failures})
    print(pathlib.Path(directory).name)
    for gate, message in failures:
        print(f"   {gate}  {message}")
    ok = got == sorted(set(expected))
    print(f"   -> gates failing: {got or 'none'} | expected: {sorted(set(expected)) or 'none'} | {'PASS' if ok else 'MISMATCH'}\n")
    sys.exit(0 if ok else 1)
