#!/usr/bin/env python3
"""Step 3 mechanical gate checks.

Implements only gate conditions that are mechanically decidable. It clears
HYGIENE. It cannot establish whether direction is any good -- that is the
separate creative decision every Step 3 gate records.

Usage:
  validate.py <fixture-dir>          # current v0.2 contract
  validate.py --legacy <fixture-dir> # preserved v0.1 evidence only
  validate.py --through V2 <dir>     # stage-scoped: report only gates V1..V2
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


def read_text(path):
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None


def normalize_prose(value):
    return re.sub(r"\s+", " ", str(value)).strip().lower()


def _md_provenance(fixture, entry):
    """Verify path -> hash -> section -> verbatim quote. Yields problem strings."""
    art = entry.get("source_artifact"); sha = entry.get("source_sha256")
    loc = entry.get("source_locator"); quote = entry.get("source_quote")
    if not art or not sha or not loc:
        yield "is missing source artifact/hash/locator provenance"; return
    path = fixture.resolve_source(art)
    if not path.is_file():
        yield f"source artifact does not exist: {path}"; return
    if sha256(path) != sha:
        yield "source artifact hash drift"
    if path.suffix.lower() != ".md":
        yield "derived provenance expects a Markdown source"; return
    section = resolve_markdown_locator(read_text(path) or "", loc)
    if section is None:
        yield f"source locator '{loc}' does not resolve to a section"
    elif not isinstance(quote, str) or not quote.strip():
        yield "cites a Markdown section without a verbatim source_quote"
    elif normalize_prose(quote) not in normalize_prose(section):
        yield f"source_quote does not appear in section '{loc}'"


def resolve_markdown_locator(text, locator):
    """Resolve a ' > ' separated heading path to that section's body.

    A section runs from its heading to the next heading of the same or a
    higher level. Returns None when the path does not resolve, so a bad
    locator fails closed rather than matching the whole document.
    """
    wanted = [normalize_key(part) for part in str(locator).split(">") if part.strip()]
    if not wanted:
        return None

    lines = text.splitlines()
    headings = []
    for index, line in enumerate(lines):
        match = re.match(r"^(#{1,6})\s+(.*\S)\s*$", line)
        if match:
            headings.append((index, len(match.group(1)), normalize_key(match.group(2))))

    for position, (line_index, level, title) in enumerate(headings):
        if title != wanted[-1]:
            continue
        # Confirm the ancestor chain, nearest enclosing heading first.
        remaining = list(wanted[:-1])
        current = level
        for prev_index, prev_level, prev_title in reversed(headings[:position]):
            if not remaining:
                break
            if prev_level < current:
                current = prev_level
                if prev_title == remaining[-1]:
                    remaining.pop()
        if remaining:
            continue
        end = len(lines)
        for next_index, next_level, _ in headings[position + 1:]:
            if next_level <= level:
                end = next_index
                break
        return "\n".join(lines[line_index + 1:end])
    return None


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
        if engine.get("contract_version") != "0.3":
            findings.append(("V1", f"current artifact contract_version is {engine.get('contract_version')!r}; expected '0.3'"))
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

        # The motion binding is provisional in Boundary Ledger's own record. The engine must
        # acknowledge that status explicitly, so a downstream reader cannot mistake a selected
        # operation for a proven implementation.
        motion_doc = read_json(motion_path) if motion_path.is_file() else None
        upstream_status = (motion_doc or {}).get("implementationStatus") or (motion_doc or {}).get("status")
        declared_status = boundary_lock.get("motion_binding_status")
        if not declared_status:
            findings.append(("V1", "Boundary Ledger lock does not record the motion binding's implementation status"))
        elif upstream_status and declared_status != upstream_status:
            findings.append(("V1", f"motion binding status recorded as {declared_status!r} but Boundary Ledger says {upstream_status!r}"))

        # The V1 freeze must be complete: every upstream artifact a later gate reads from is
        # named and hashed here, or the freeze cannot invalidate anything.
        # The complete governing input set V1 names -- not a convenience subset.
        REQUIRED_FREEZE = ("editorial_lock", "operator_canvas", "episode_investment_thesis",
                           "narrative_spine", "episode_beat_sheet", "claims_map", "script",
                           "canonical_w", "spoken_identity", "narration_lock", "narration_master",
                           "word_transcript", "intentional_pause_map")
        freeze = engine.get("input_lock") or {}
        if not freeze:
            findings.append(("V1", "engine records no input_lock; the upstream freeze is not machine-checkable"))
        else:
            for key in REQUIRED_FREEZE:
                entry = freeze.get(key)
                if not isinstance(entry, dict) or not entry.get("path") or not entry.get("sha256"):
                    findings.append(("V1", f"input_lock is missing a path/hash for '{key}'"))
                    continue
                fp = fixture.resolve_source(entry["path"])
                if not fp.is_file():
                    findings.append(("V1", f"input_lock '{key}' does not exist: {fp}"))
                elif sha256(fp) != entry["sha256"]:
                    findings.append(("V1", f"input_lock '{key}' hash drift"))
            if not freeze.get("narration_duration_seconds"):
                findings.append(("V1", "input_lock does not record the narration duration later gates bind timing to"))

        system_version = boundary_lock.get("system_version")
        if core and (core.get("system") != "Boundary Ledger" or core.get("version") != system_version):
            findings.append(("V1", "Boundary Ledger semantic-core identity/version does not match the lock"))
        if motion_binding and (
            motion_binding.get("medium") != "motion"
            or motion_binding.get("systemVersion") != system_version
        ):
            findings.append(("V1", "Boundary Ledger motion-binding medium/version does not match the lock"))

    # V2 -- derived business fields must match the Canvas.
    # A JSON Canvas is compared field-for-field. A real episode's Canvas is Markdown, so each
    # derived field instead cites a section and a verbatim quote; the approver judges the
    # paraphrase, exactly as for a business operation.
    derived = engine.get("derived") or {}
    derived_prov = engine.get("derived_provenance") or {}
    if canvas:
        for key, value in derived.items():
            if canvas.get(key) != value:
                findings.append(("V2", f"derived field '{key}' diverges from Canvas: engine={value!r} canvas={canvas.get(key)!r}"))
    elif derived_prov:
        for key, value in derived.items():
            entry = derived_prov.get(key)
            if not isinstance(entry, dict):
                findings.append(("V2", f"derived field '{key}' has no upstream provenance"))
                continue
            findings.extend(("V2", f"derived field '{key}' {m}") for m in _md_provenance(fixture, entry))
    elif derived:
        findings.append(("V2", "derived fields cannot be checked: no canvas.json and no derived_provenance"))

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
            # A Markdown source carries its binding as section + verbatim quote, so the
            # upstream_states indirection a JSON canvas needs does not apply. The quote is
            # checked below and is a stronger tie than an ID pointing at a local block.
            md_sourced = str(item.get("source_artifact", "")).lower().endswith(".md")
            if not upstream and not md_sourced:
                findings.append(("V2", f"business operation '{operation_id}' has unknown upstream state '{upstream_id}'"))
            elif upstream:
                for field in ("state_before", "state_after", "business_operation"):
                    if item.get(field) != upstream.get(field):
                        findings.append(("V2", f"business operation '{operation_id}' field '{field}' diverges from upstream state '{upstream_id}'"))
            else:
                for field in ("state_before", "state_after", "business_operation"):
                    if not str(item.get(field) or "").strip():
                        findings.append(("V2", f"business operation '{operation_id}' is missing '{field}'"))
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
                    if source_path.suffix.lower() == ".md":
                        # Markdown upstream: provenance is path -> hash -> section
                        # -> verbatim quote. A machine can prove the quote is
                        # real and from that section; whether the derived state
                        # faithfully represents it is the named V2 approval.
                        source_quote = item.get("source_quote")
                        source_text = read_text(source_path)
                        section = (
                            resolve_markdown_locator(source_text, source_locator)
                            if source_text is not None
                            else None
                        )
                        if section is None:
                            findings.append(("V2", f"business operation '{operation_id}' source locator '{source_locator}' does not resolve to a section"))
                        elif not isinstance(source_quote, str) or not source_quote.strip():
                            findings.append(("V2", f"business operation '{operation_id}' cites a Markdown section without a verbatim source_quote"))
                        elif normalize_prose(source_quote) not in normalize_prose(section):
                            findings.append(("V2", f"business operation '{operation_id}' source_quote does not appear in section '{source_locator}'"))
                    else:
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

        # Establishment is AUTHORED viewer-knowledge, held apart from derived business state.
        for est in engine.get("establishment") or []:
            eid = est.get("id", "?")
            if not str(eid).startswith("EST-"):
                findings.append(("V2", f"establishment row '{eid}' is not in the EST- id space"))
            if est.get("label") != "AUTHORED":
                findings.append(("V2", f"establishment row '{eid}' is not labelled AUTHORED"))
            for banned in ("state_before", "state_after", "business_operation"):
                if banned in est:
                    findings.append(("V2", f"establishment row '{eid}' carries business-state field '{banned}'; nothing in the business changes"))
            if "acts_on" in est:
                findings.append(("V2", f"establishment row '{eid}' uses acts_on; establishment reveals objects, it does not change them"))
            for req in ("viewer_state_before", "viewer_state_after"):
                if not est.get(req):
                    findings.append(("V2", f"establishment row '{eid}' is missing '{req}'"))
            if not est.get("reveals"):
                findings.append(("V2", f"establishment row '{eid}' reveals nothing"))
            findings.extend(("V2", f"establishment row '{eid}' {m}") for m in _md_provenance(fixture, est))
            r, b = est.get("boundary_ledger_semantic_role_id"), est.get("boundary_ledger_operation_id")
            if r not in roles:
                findings.append(("V2", f"establishment row '{eid}' selects unknown Boundary Ledger role '{r}'"))
            if b not in operations:
                findings.append(("V2", f"establishment row '{eid}' selects unknown Boundary Ledger operation '{b}'"))
            elif b not in permitted.get(r, set()):
                findings.append(("V2", f"Boundary Ledger binding does not permit '{b}' for role '{r}'"))

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
        classes = {c.get("id"): (c.get("instances") or []) for c in (world.get("object_classes") or [])}
        establishment_ids = {e.get("id") for e in (engine.get("establishment") or [])}
        # v0.3 splits the single operation_bindings field into three, because an object that
        # an operation changes, one it merely carries, and one an establishment row reveals
        # are different relationships and were being conflated.
        def bindings(item):
            legacy = set(item.get("operation_bindings") or [])
            return legacy | set(item.get("changed_by") or []) | set(item.get("carried_by") or []) | set(item.get("revealed_by") or [])
        for item in objects.values():
            if not item.get("static") and not (bindings(item) & (operation_ids | establishment_ids)):
                findings.append(("V3", f"object '{item['id']}' is neither operation-reachable nor marked static"))
            for field in ("changed_by", "carried_by"):
                for ref in item.get(field) or []:
                    if ref not in operation_ids:
                        findings.append(("V3", f"object '{item['id']}' {field} names unknown operation '{ref}'"))
            for ref in item.get("revealed_by") or []:
                if ref not in establishment_ids:
                    findings.append(("V3", f"object '{item['id']}' revealed_by names unknown establishment row '{ref}'"))
        # A transition may only be triggered by an operation that changes this object, or by a
        # declared failure route. Anything else describes a change that cannot occur.
        route_ids = {r.get("id") for r in (world.get("failure_routes") or [])}
        for item in objects.values():
            allowed = set(item.get("changed_by") or []) | route_ids
            for t in item.get("allowed_transitions") or []:
                if isinstance(t, dict) and t.get("triggered_by") and t["triggered_by"] not in allowed:
                    findings.append(("V3", f"object '{item['id']}' transition {t.get('from')}->{t.get('to')} is triggered by '{t['triggered_by']}', which neither changes it nor is a declared failure route"))
            if item.get("static") and item.get("allowed_transitions"):
                findings.append(("V3", f"object '{item['id']}' is marked static but declares state transitions"))
            if item.get("static") and item.get("changed_by"):
                findings.append(("V3", f"object '{item['id']}' is marked static but records changed_by {item['changed_by']}"))
            if not item.get("static") and not item.get("changed_by"):
                findings.append(("V3", f"object '{item['id']}' is not static yet no operation changes it"))

        # Paths are routes, not state lists: every edge needs from, to and a condition, and the
        # path must name what travels it.
        for path in world.get("paths") or []:
            if not path.get("traveler"):
                findings.append(("V3", f"path '{path.get('id')}' does not name what travels it"))
            edges = path.get("edges")
            if not edges:
                findings.append(("V3", f"path '{path.get('id')}' declares no edges; a list of states is not a route"))
                continue
            for edge in edges:
                if not edge.get("from") or not edge.get("to"):
                    findings.append(("V3", f"path '{path.get('id')}' has an edge without from/to"))
                if not edge.get("condition"):
                    findings.append(("V3", f"path '{path.get('id')}' edge {edge.get('from')}->{edge.get('to')} states no condition"))

        # An evidence anchor must carry the upstream limit on what it may imply.
        for a in world.get("evidence_anchors") or []:
            if not a.get("must_not_imply"):
                findings.append(("V3", f"evidence anchor '{a.get('id')}' does not carry its upstream must-not-imply qualification"))

        # v0.3: a transition must name what triggers it and whether it reverses. The legacy
        # ["from","to"] pair form asserts neither and is no longer sufficient.
        for item in objects.values():
            for t in item.get("allowed_transitions") or []:
                if not isinstance(t, dict):
                    findings.append(("V3", f"object '{item['id']}' uses the legacy transition pair form; a transition must name triggered_by and reversible"))
                    continue
                if not t.get("triggered_by"):
                    findings.append(("V3", f"object '{item['id']}' transition {t.get('from')}->{t.get('to')} names no trigger"))
                if "reversible" not in t:
                    findings.append(("V3", f"object '{item['id']}' transition {t.get('from')}->{t.get('to')} does not state reversibility"))
                st = set(item.get("states") or [])
                if t.get("from") not in st or t.get("to") not in st:
                    findings.append(("V3", f"object '{item['id']}' transition {t.get('from')}->{t.get('to')} uses an undeclared state"))

        # Paths are required: a route through the world that is not an object's own state.
        paths = world.get("paths") or []
        if not paths:
            findings.append(("V3", "world declares no paths; the routes objects travel are not traceable"))
        for path in paths:
            if not path.get("id"): findings.append(("V3", "a path has no id"))

        # Evidence anchors must target something real and carry their upstream qualification.
        flow_ids = {m.get("id") for m in (world.get("money_flows") or [])}
        path_ids = {p.get("id") for p in paths}
        for a in world.get("evidence_anchors") or []:
            tgt = a.get("attaches_to")
            if tgt not in objects and tgt not in flow_ids and tgt not in path_ids:
                findings.append(("V3", f"evidence anchor '{a.get('id')}' attaches to unknown entity '{tgt}'"))
            if not a.get("label"):
                findings.append(("V3", f"evidence anchor '{a.get('id')}' carries no upstream evidence label"))
            if not a.get("attachment_note"):
                findings.append(("V3", f"evidence anchor '{a.get('id')}' states no qualification for what it may and may not imply"))

        # Engine acts_on and world changed_by must agree in both directions.
        for operation_id, operation in operation_map.items():
            targets = set(operation.get("acts_on") or [])
            expanded = set()
            for t in targets:
                expanded |= set(classes.get(t, [t])) if t in classes else {t}
            for oid, item in objects.items():
                in_world = operation_id in set(item.get("changed_by") or [])
                in_engine = oid in expanded
                if in_world and not in_engine:
                    findings.append(("V3", f"object '{oid}' claims changed_by '{operation_id}' but that operation does not act on it"))
                if in_engine and not in_world:
                    findings.append(("V3", f"operation '{operation_id}' acts on '{oid}' but that object does not record it in changed_by"))

        # An operation may act on an object class when the world declares that class with at
        # least one instance. Instances keep separate identities; the class is not an object.
        for operation_id, operation in operation_map.items():
            for target in operation.get("acts_on") or []:
                if target in objects:
                    continue
                if target in {p.get("id") for p in (world.get("paths") or [])}:
                    continue
                if target in classes:
                    missing = [i for i in classes[target] if i not in objects]
                    if not classes[target]:
                        findings.append(("V3", f"business operation '{operation_id}' acts on class '{target}' which declares no instances"))
                    elif missing:
                        findings.append(("V3", f"object class '{target}' declares instances absent from the world: {missing}"))
                    continue
                findings.append(("V3", f"business operation '{operation_id}' acts on unknown object '{target}'"))
        for est in engine.get("establishment") or []:
            for target in est.get("reveals") or []:
                if target not in objects and target not in classes:
                    findings.append(("V3", f"establishment row '{est.get('id')}' reveals unknown object '{target}'"))
    else:
        verbs = {item["verb"] for item in (engine.get("motion_verbs") or [])}
        for item in objects.values():
            if not item.get("static") and not (set(item.get("verbs") or []) & verbs):
                findings.append(("V3", f"object '{item['id']}' is neither verb-reachable nor marked static"))
        for verb in engine.get("motion_verbs") or []:
            for target in verb.get("acts_on") or []:
                if target not in objects:
                    findings.append(("V3", f"verb '{verb['verb']}' acts on unknown object '{target}'"))
    claims_map = (world.get("claims_map") or {}) if isinstance(world, dict) else {}
    if not claims and claims_map:
        cm_path = fixture.resolve_source(claims_map.get("source_artifact", ""))
        if not cm_path.is_file():
            findings.append(("V3", f"claims map does not exist: {cm_path}"))
        elif sha256(cm_path) != claims_map.get("source_sha256"):
            findings.append(("V3", "claims map hash drift"))
        else:
            claims = set(re.findall(r"^\|\s*(C\d{3})\s*\|", read_text(cm_path) or "", re.M))
            if not claims:
                findings.append(("V3", "claims map declared but no claim IDs parsed"))
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
    runtimes = r"\b(hyperframes|remotion|after ?effects|davinci(?: ?resolve)?|blackmagic|fusion|blender|unreal)\b"
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
    through = None
    if args and args[0] == "--through":
        if len(args) < 2 or not re.fullmatch(r"V[1-7]", args[1]):
            print("Usage: validate.py [--legacy] [--through V1..V7] <fixture-dir>", file=sys.stderr)
            sys.exit(2)
        through = int(args[1][1:]); args = args[2:]
    if len(args) != 1:
        print("Usage: validate.py [--legacy] [--through V1..V7] <fixture-dir>", file=sys.stderr)
        sys.exit(2)
    directory = args[0]
    failures = check(directory, legacy=legacy)
    if through is not None:
        failures = [(g, m) for g, m in failures if int(g[1:]) <= through]
    expected = Fixture(directory).expected()
    got = sorted({gate for gate, _ in failures})
    print(pathlib.Path(directory).name)
    for gate, message in failures:
        print(f"   {gate}  {message}")
    ok = got == sorted(set(expected))
    print(f"   -> gates failing: {got or 'none'} | expected: {sorted(set(expected)) or 'none'} | {'PASS' if ok else 'MISMATCH'}\n")
    sys.exit(0 if ok else 1)
