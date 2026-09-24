from __future__ import annotations

import json
import os
import tempfile
from collections import OrderedDict
from pathlib import Path
from typing import Iterable

from .hashes import sha256_file, write_json_atomic
from .input_lock import source_path
from .paths import EpisodeIdentity


FRAME_CONTRACT = {
    "width": 1920,
    "height": 1080,
    "fps": 30,
    "safe_area_px": {"top": 65, "right": 134, "bottom": 65, "left": 134},
    "type_scale_px": {
        "headline_min": 72,
        "headline_max": 108,
        "critical_number_min": 140,
        "critical_number_max": 240,
        "label_min": 44,
        "label_max": 60,
        "source_min": 26,
        "source_max": 34,
    },
    "default_transition": "cut",
}


def _write_text_atomic(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            handle.write(text.rstrip() + "\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_name, path)
    finally:
        if os.path.exists(temporary_name):
            os.unlink(temporary_name)


def _locked_words(lock: dict) -> list[dict]:
    artifact = next(
        (item for item in lock.get("artifacts", []) if item.get("role") == "word_transcript"),
        None,
    )
    if artifact is None:
        raise ValueError("input lock has no word transcript")
    path = source_path(artifact)
    if sha256_file(path) != artifact.get("sha256"):
        raise ValueError("locked word transcript hash changed")
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, list):
        raise ValueError("locked word transcript is not an array")
    return value


def _sequence_groups(plan: dict) -> OrderedDict[str, list[dict]]:
    groups: OrderedDict[str, list[dict]] = OrderedDict()
    for unit in plan.get("units", []):
        groups.setdefault(unit["sequence_id"], []).append(unit)
    return groups


def _word_table(words: list[dict], start: int, end: int) -> str:
    rows = ["| Index | In | Out | Spoken word |", "|---:|---:|---:|---|"]
    for index in range(start, end + 1):
        word = words[index]
        spoken_word = str(word["word"]).replace("|", "\\|")
        rows.append(
            f"| {index} | {float(word['start']):.3f} | {float(word['end']):.3f} | "
            f"{spoken_word} |"
        )
    return "\n".join(rows)


def _json_block(value: object) -> str:
    return "```json\n" + json.dumps(value, indent=2, ensure_ascii=False) + "\n```"


def _world_slice(world: dict, units: list[dict]) -> dict:
    object_ids: set[str] = set()
    for unit in units:
        object_ids.update(unit.get("carry", []))
        object_ids.update(unit.get("focus", []))
        object_ids.update(item.get("object_id") for item in unit.get("world_state_before", []))
        object_ids.update(item.get("object_id") for item in unit.get("world_state_after", []))
    object_ids.discard(None)

    edges = [
        edge
        for edge in world.get("edges", [])
        if edge.get("from") in object_ids or edge.get("to") in object_ids
    ]
    for edge in edges:
        object_ids.add(edge["from"])
        object_ids.add(edge["to"])
    objects = [item for item in world.get("objects", []) if item.get("id") in object_ids]
    return {"objects": objects, "edges": edges}


def _direction_rules() -> str:
    return """1. Design the audience's frame, not a view of the master world model. Never show the complete node map by default.
2. Express one visual sentence at a time: subject -> relationship or business verb -> object -> visible consequence.
3. Read the scene and adjacent beats first. Encode scene_context: situation, scene_form, form_reason, stakes or their absence, and emotional_arc. Choose the picture/audio mode from context: narrated observation, narrated dramatization, synchronized dialogue, presenter address, natural-sound observation, or silent graphic. Narration alone selects neither form nor coverage.
4. In narrated observation, the narrator carries language while the image carries action, evidence, pressure, relationship, or consequence. Prohibit visible speech, reciprocal conversational eyelines, question-and-answer reverse shots, and facial coverage that makes the viewer wait for an unheard line.
5. Narrated dramatization may show a conversation, reciprocal eyelines, and an attempted answer when narration supplies essential meaning. Use illustrative_only or prohibited speech, motivated_interaction coverage, and a mode-appropriate face function. Record dramatization_context: illustrative representation, narration-carried essential meaning, disclosure_plan, and audio_review_check. Do not claim verbatim testimony or exact character lip sync.
6. Source delivery requires natural-sound observation with synchronized audible source; sync delivery requires synchronized dialogue; presenter delivery requires exact approved presenter audio. These delivery functions are not narration workarounds. Observation's close faces need task focus or a caused reaction. Dramatization may use dramatic_performance. Review the actual track; mute viewing is diagnostic in dramatization, not a universal missing-line veto.
7. Record what stays still, whether the shot is a master, setup, or standalone, its declared master-shot or listed asset-ticket reference, screen direction, continuity anchors, and exact initial and final images. These are direction facts, not generator discretion.
8. Use only the layers needed for the scene. Two to five meaningful objects can guide an ordinary designed explanation, but a film plate or evidence source may occupy a single layer. Never add decoration to meet a count.
9. Preserve recurring object identity and screen direction. State what is inherited, introduced, retired, and handed to the next sequence.
10. Give every shot exact 1920x1080 pixel bounds for every layer at its start and end. Do not use vague placement words such as "somewhere," "roughly," or "nearby."
11. Tie every motion beat to an exact locked word index and timestamp. Motion must communicate an operation, state change, transfer, comparison, failure, or consequence.
12. Specify every visible text string exactly, including capitalization, line count, size, alignment, and timed substring emphasis. Text labels or proves; it does not repeat the VO.
13. The default transition is a cut. Use a designed transition only when it preserves an object, extracts evidence into the system, follows a handoff, reveals accumulated state, or shows a route failing or changing.
14. Evidence must follow: source appears -> relevant element highlighted -> value extracted -> value attached to the system -> behavior changes. Never synthesize evidence or branded interfaces.
15. AI environmental plates may establish non-evidentiary reality only. Documents, figures, interfaces, prices, and proof must come from an authorized source or ticket and be composited accurately.
16. Keep the OE frame to Ink + Paper or Schematic Navy + one accent. No gradients, glass, decorative glow, generic icon clouds, transition-pack flourishes, or motion merely for energy.
17. The first frame, action frame, and exit frame must each be understandable without a production caption or mini-map.
18. Encode editorial_intent for each shot: techniques, why_this_shot, entry_trigger, exit_trigger, hold_intent, alternative_considered, and review_question. Choose coverage and cuts for the information or performance change; do not impose five setups, fixed cut intervals, or manufactured escalation. Protect the crucial pause or reading hold."""


def build_director_prompts(
    identity: EpisodeIdentity,
    episode_path: Path,
    lock: dict,
    engine: dict,
    world: dict,
    plan: dict,
    tickets: dict,
    *,
    sequence_ids: Iterable[str] | None = None,
) -> list[Path]:
    words = _locked_words(lock)
    groups = _sequence_groups(plan)
    requested = list(sequence_ids or groups.keys())
    unknown = [sequence_id for sequence_id in requested if sequence_id not in groups]
    if unknown:
        raise ValueError("unknown sequence IDs: " + ", ".join(unknown))

    output_dir = episode_path / "prompts" / "generated" / "director"
    output_dir.mkdir(parents=True, exist_ok=True)
    ordered_ids = list(groups)
    outputs: list[Path] = []
    manifest_items = []
    ticket_map = {item["id"]: item for item in tickets.get("tickets", [])}
    evidence_map = {item["id"]: item for item in world.get("evidence", [])}

    source_hashes = {
        "input_lock": sha256_file(episode_path / "input-lock.json"),
        "episode_engine": sha256_file(episode_path / "episode-engine.json"),
        "world": sha256_file(episode_path / "world.json"),
        "visual_plan": sha256_file(episode_path / "visual-plan.json"),
        "asset_tickets": sha256_file(episode_path / "asset-tickets.json"),
    }

    for sequence_id in requested:
        units = groups[sequence_id]
        sequence_in = float(units[0]["in"])
        sequence_out = float(units[-1]["out"])
        word_start = int(units[0]["narration_anchor"]["word_start"])
        word_end = int(units[-1]["narration_anchor"]["word_end"])
        quote = " ".join(str(words[index]["word"]) for index in range(word_start, word_end + 1))
        world_slice = _world_slice(world, units)
        evidence_ids = sorted({item for unit in units for item in unit.get("evidence_ids", [])})
        ticket_ids = sorted({item for unit in units for item in unit.get("asset_ticket_ids", [])})
        previous_id = ordered_ids[ordered_ids.index(sequence_id) - 1] if ordered_ids.index(sequence_id) > 0 else None
        next_id = ordered_ids[ordered_ids.index(sequence_id) + 1] if ordered_ids.index(sequence_id) + 1 < len(ordered_ids) else None

        prompt = f"""# Blueprint Cinema director packet: {sequence_id}

You are the senior motion-design director for one bounded Operator Economy sequence. Author precise scene direction only. Do not write renderer code, generate media, alter the narration, change claims, or edit canonical episode state.

Your result must make the viewer understand a causal relationship against the exact locked voiceover. This is not a request for a topical illustration, a slide, a node-map camera move, or generic "Vox-style" decoration. The transferable editorial-explainer behaviors are deliberate composition, restrained annotation, progressive disclosure, parameter-to-consequence evidence motion, and motivated continuity.

## Output contract

Author exactly one sequence object for `schemas/scene-directions.schema.json` and save it only to the path assigned by the orchestrator. It must contain shot-by-shot pixel geometry, exact text, word-cued motion, evidence choreography, and transition continuity. Return no approvals and make no canonical-state changes.

Episode: `{identity.folder_name}`
Sequence: `{sequence_id}`
Previous sequence: `{previous_id or 'none; establish the opening state'}`
Next sequence: `{next_id or 'none; resolve the episode handoff'}`
Time range: `{sequence_in:.3f}-{sequence_out:.3f}` seconds
Locked word range: `{word_start}-{word_end}`
Exact VO: `{quote}`

Hash pins:
{_json_block(source_hashes)}

## Non-negotiable direction rules

{_direction_rules()}

## Required frame contract

{_json_block(FRAME_CONTRACT)}

## Exact word timing

{_word_table(words, word_start, word_end)}

## Adjacent narration context (read-only; outside this shot assignment)

{_word_table(words, max(0, word_start - 40), word_start - 1) if word_start else "Episode start; no preceding narration."}

{_word_table(words, word_end + 1, min(len(words) - 1, word_end + 40)) if word_end + 1 < len(words) else "Episode end; no following narration."}

## Approved visual-plan units

These state what must be communicated; they do not prescribe the finished layout.

{_json_block(units)}

## Available persistent-world slice

Use only these approved IDs unless the orchestrator explicitly expands the slice. A state-marker label is an internal concept; prefer showing the operation that produces it.

{_json_block(world_slice)}

## Evidence available to this sequence

{_json_block([evidence_map[item] for item in evidence_ids])}

## Asset tickets available to this sequence

{_json_block([ticket_map[item] for item in ticket_ids])}

## Episode mechanic and guardrails

{_json_block({
    "visual_mechanic": engine.get("visual_mechanic", {}),
    "motion_verbs": engine.get("motion_verbs", []),
    "guardrails": engine.get("guardrails", []),
    "reality_world": engine.get("reality_world", {}),
})}

## Required authoring decisions

Before returning the JSON, make and encode every one of these decisions:

- The single audience inference this sequence must create.
- Authored scene_context: situation, scene_form, form_reason, stakes, and emotional_arc. Do not infer conflict, familiarity, or prior meetings from a generic setting. Mark uncertainty and return material gaps upstream.
- The visual sentence: subjects, relationship, objects, visible consequence, before state, and after state.
- The minimum number of shots needed; narration units are not automatically shots.
- Each shot's production lane: motion graphics, evidence capture, B-roll edit, AI environmental plate, or hybrid composite.
- Each shot's picture/audio mode, language carrier, visible-speech rule, coverage grammar, face function, concrete physical action, and mute-test result. Select this contract before camera angle or coverage.
- Each shot's editorial_intent: techniques, why_this_shot, entry_trigger, exit_trigger, hold_intent, alternative_considered, and review_question. A planned review result is not a playback verdict.
- For narrated dramatization, explicit illustrative disclosure and an actual-audio comprehension check in dramatization_context; no added character dialogue. Conversation is permissible, unavailable exact words must not carry essential meaning.
- For narrated observation, the specific action, evidence, pressure, relationship, or consequence the picture carries without dialogue behavior. Each change of angle must reveal new information rather than imply a missing exchange.
- Each shot's direction facts: what stays still; master, setup, or standalone role; a declared master-shot or listed asset-ticket reference for every setup; action line, camera side, and subject direction; typed continuity anchors; and exact initial and final images.
- Exact start and end time for every shot, with contiguous coverage of the sequence.
- Exact layer rectangles at shot start and end, z-order, opacity, role, and state.
- Primary subject and visual hierarchy; do not distribute attention equally.
- Exact visible text and every timed word or number highlight.
- Every motion beat's cue word index, cue timestamp, duration, property change, easing, and explanatory purpose.
- Transition in and out, including which objects survive across the cut or transformation.
- Evidence source/highlight/extract/attach/change steps whenever proof appears.
- What is inherited from the prior sequence and the precise exit frame handed to the next.
- At least three explicit things this sequence must not do.
- At least five observable review checks that can pass or fail from the animatic.

If the approved inputs do not support an honest visual decision, stop and report the exact missing evidence, ticket, object, or upstream decision. Do not fill the gap with generic imagery.
"""
        output = output_dir / f"{sequence_id}.md"
        _write_text_atomic(output, prompt)
        outputs.append(output)
        manifest_items.append(
            {
                "sequence_id": sequence_id,
                "in": sequence_in,
                "out": sequence_out,
                "word_start": word_start,
                "word_end": word_end,
                "prompt_path": str(output.relative_to(episode_path)),
                "prompt_sha256": sha256_file(output),
            }
        )

    manifest = {
        "schema_version": "1.0.0",
        "kind": "blueprint_cinema_director_prompt_manifest",
        **identity.as_dict(),
        "source_hashes": source_hashes,
        "frame_contract": FRAME_CONTRACT,
        "prompts": manifest_items,
    }
    manifest_path = output_dir / "manifest.json"
    write_json_atomic(manifest_path, manifest)
    return [manifest_path, *outputs]


def build_scene_prompts(
    identity: EpisodeIdentity,
    episode_path: Path,
    directions: dict,
) -> list[Path]:
    output_dir = episode_path / "prompts" / "generated" / "build"
    output_dir.mkdir(parents=True, exist_ok=True)
    outputs: list[Path] = []
    manifest_items = []

    for sequence in directions["sequences"]:
        for shot in sequence["shots"]:
            prompt = f"""# Blueprint Cinema build packet: {sequence['id']} / {shot['id']}

Implement exactly one approved shot. Do not redesign it, parse narration to choose a layout, invent evidence, substitute assets, change text, alter timing, or modify episode approvals. The work order that invokes this packet must provide one owned implementation path; stop if that path is missing.

Episode: `{identity.folder_name}`
Sequence: `{sequence['id']}`
Shot: `{shot['id']}`
Time range: `{float(shot['in']):.3f}-{float(shot['out']):.3f}` seconds
Production lane: `{shot['production_lane']}`

## Audience result

{sequence['audience_inference']}

## Visual sentence

{_json_block(sequence['visual_sentence'])}

## Scene context (preserve the directing choice)

{_json_block(sequence['scene_context'])}

## Exact shot recipe

{_json_block(shot)}

## Continuity and constraints

{_json_block({
    "continuity": sequence["continuity"],
    "negative_constraints": sequence["negative_constraints"],
    "review_checks": sequence["review_checks"],
    "frame_contract": directions["frame_contract"],
})}

## Implementation rules

1. Treat every coordinate, timestamp, layer order, text string, cue, duration, and transition as a contract.
2. Use frame-based deterministic animation at 30 fps. Word cue times are absolute episode seconds; convert them to shot-relative frames without rounding drift.
3. Keep essential content inside the declared safe area and verify the specified text size and line count at 50 percent scale.
4. Use one visible priority. Supporting elements remain quieter until their timed action.
5. Use the declared transition. Do not add camera drift, parallax, overshoot, bounce, glow, or decorative entrances.
6. When the lane is `evidence_capture`, use the exact authorized source and preserve publisher, context, and attribution. Synthetic reconstruction is prohibited.
7. When the lane is `ai_environmental_plate`, generate only the environment or physical action described by the ticket; composite all factual text, interfaces, documents, brands, and figures separately.
8. When the lane is `broll_edit`, the selected clip must perform the ticket's semantic job rather than merely match a keyword.
9. Obey the declared picture/audio contract. Narrated observation may not introduce word-shaped mouth movement, conversational eyelines, question-and-answer cutting, or a face close-up without a visible task-focus or caused-reaction function.
10. Use `source_delivery` only for a natural-sound observation carrying synchronized source speech, and use `sync_delivery` only for synchronized dialogue. A natural-sound shot without source delivery must pass the missing-line mute test. Do not borrow either face function for narration-led footage.
11. Implement the declared direction facts exactly: preserve what stays still, derive setup coverage from its declared master-shot or listed asset-ticket reference, keep screen direction and continuity anchors stable, and land on the specified final image.
12. Preserve editorial_intent, including cut triggers and protected holds. Apply the selected mode's review: observation cannot depend on unheard dialogue; narrated dramatization may show motivated conversation but the actual narration must supply essential meaning. Review with the exact track before claiming comprehension. Mute viewing is diagnostic, not a universal veto. No added character lines or invented sync.
13. Leave a conspicuous placeholder when an approved asset is missing. Never silently replace it with a plausible-looking asset.
14. Return a short implementation report listing the owned files changed, exact checks run, missing tickets, and any contract detail that could not be represented.
"""
            output = output_dir / sequence["id"] / f"{shot['id']}.md"
            _write_text_atomic(output, prompt)
            outputs.append(output)
            manifest_items.append(
                {
                    "sequence_id": sequence["id"],
                    "shot_id": shot["id"],
                    "in": shot["in"],
                    "out": shot["out"],
                    "production_lane": shot["production_lane"],
                    "prompt_path": str(output.relative_to(episode_path)),
                    "prompt_sha256": sha256_file(output),
                }
            )

    manifest = {
        "schema_version": "1.0.0",
        "kind": "blueprint_cinema_build_prompt_manifest",
        **identity.as_dict(),
        "scene_directions_sha256": sha256_file(episode_path / "scene-directions.json"),
        "prompts": manifest_items,
    }
    manifest_path = output_dir / "manifest.json"
    write_json_atomic(manifest_path, manifest)
    return [manifest_path, *outputs]
