from __future__ import annotations

import json
import subprocess
from pathlib import Path

from .hashes import sha256_file
from .state import next_stage
from .validation import ValidationFailure, load_json, validate_deliverable, validate_work_order


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def _hash_line(path: Path) -> str:
    return sha256_file(path) if path.is_file() else "missing"


def _media_probe_lines(path: Path, label: str = "Whole-episode") -> list[str]:
    if not path.is_file():
        return [f"- {label} review MP4 rendered: no"]
    result = subprocess.run(
        [
            "ffprobe", "-v", "error", "-show_entries",
            "format=duration,size:stream=codec_type,codec_name,width,height,r_frame_rate,sample_rate,channels",
            "-of", "json", str(path),
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return [
            f"- {label} review MP4 rendered: yes",
            f"- {label} media probe: failed; rerun `ffprobe` before relying on media properties",
            f"- {label} SHA-256: `{sha256_file(path)}`",
        ]
    payload = json.loads(result.stdout)
    video = next((item for item in payload.get("streams", []) if item.get("codec_type") == "video"), {})
    audio = next((item for item in payload.get("streams", []) if item.get("codec_type") == "audio"), {})
    media_format = payload.get("format", {})
    return [
        f"- {label} review MP4 rendered: yes",
        (
            f"- {label} media: {video.get('codec_name', 'unknown')} "
            f"{video.get('width', '?')}x{video.get('height', '?')} at {video.get('r_frame_rate', '?')}, "
            f"{audio.get('codec_name', 'unknown')} {audio.get('channels', '?')} channels at "
            f"{audio.get('sample_rate', '?')} Hz, {media_format.get('duration', '?')}s container duration, "
            f"{media_format.get('size', '?')} bytes"
        ),
        f"- {label} SHA-256: `{sha256_file(path)}`",
    ]


def generate_reviews(episode_path: Path) -> list[Path]:
    review_dir = episode_path / "review"
    engine_path = episode_path / "episode-engine.json"
    world_path = episode_path / "world.json"
    plan_path = episode_path / "visual-plan.json"
    tickets_path = episode_path / "asset-tickets.json"
    state_path = episode_path / "production-state.json"
    render_path = episode_path / "render-data" / "greybox.json"
    engine = load_json(engine_path) if engine_path.is_file() else {}
    world = load_json(world_path) if world_path.is_file() else {}
    plan = load_json(plan_path) if plan_path.is_file() else {}
    tickets = load_json(tickets_path) if tickets_path.is_file() else {"tickets": []}
    state = load_json(state_path) if state_path.is_file() else {"current_stage": "initialized"}

    outputs: list[Path] = []
    engine_review = review_dir / "ENGINE-REVIEW.md"
    _write(
        engine_review,
        f"""# EP006 engine review

Status: validated and hash-approved only when `production-state.json` records the matching hash.

- Engine: `{_hash_line(engine_path)}`
- Mechanic: {engine.get('visual_mechanic', {}).get('name', 'missing')}
- Operator: {engine.get('operator', {}).get('description', 'missing')}
- Input customer: {engine.get('input_customer', {}).get('description', 'missing')}
- Qualified subset: {engine.get('eligible_return_customer', {}).get('description', 'missing')}
- Outcome: {engine.get('outcome_object', 'missing')}

## Honesty test

{engine.get('visual_mechanic', {}).get('why_honest', 'Not yet authored.')}

## Guardrails and risks

""" + "\n".join(f"- {item}" for item in engine.get("guardrails", [])) + "\n",
    )
    outputs.append(engine_review)

    world_review = review_dir / "WORLD-REVIEW.md"
    _write(
        world_review,
        f"""# EP006 persistent-world review

- World hash: `{_hash_line(world_path)}`
- Stable objects: {len(world.get('objects', []))}
- Directed edges: {len(world.get('edges', []))}
- Evidence pins: {len(world.get('evidence', []))}
- Camera anchors: {len(world.get('cameras', []))}
- Failure/retry definitions: {len(world.get('failures', []))}

The canonical validator checks duplicate IDs, every semantic reference, explicit path and failure edges, evidence-source hashes and claim/parameter registries, spatial label clearance, the useful first OTA booking, audit and repair before return activation, non-bypassable permission/qualification/human-review gates, suppression, retries, escalation, and separation of the operator settlement ledger from the guest-facing direct confirmation. Camera target IDs are representative zone anchors, while plan modes still require the matching human, system, or proof camera.
""",
    )
    outputs.append(world_review)

    modes: dict[str, int] = {}
    for unit in plan.get("units", []):
        modes[unit.get("mode", "unknown")] = modes.get(unit.get("mode", "unknown"), 0) + 1
    plan_review = review_dir / "VISUAL-PLAN-REVIEW.md"
    _write(
        plan_review,
        f"""# EP006 full-timeline visual-plan review

- Plan hash: `{_hash_line(plan_path)}`
- Timed units: {len(plan.get('units', []))}
- Locked duration covered: {plan.get('audio_duration_seconds', 'missing')} seconds
- Modes: `{json.dumps(modes, sort_keys=True)}`
- Explicit asset tickets: {len(tickets.get('tickets', []))}

Every unit carries an exact word range and quote, explicit sequence identity, a business action, an approved motion verb, persistent object carry/focus, accumulated before/after states, a mode-matched camera anchor, evidence/ticket references, and an intentionally narration-only greybox audio state. Validation rejects gaps, overlaps, out-of-bounds timing, dangling IDs, state discontinuity, unexplained within-sequence regression, decorative motion, and missing consent, qualification, suppression, judgment, economics, configured failure, or outcome coverage.

Guest memory cannot activate before affirmative permission. Outbound follow-up, the direct return route, recorded return value, and final confirmation are checked against the accumulated audit, repair, permission, qualification, suppression-disposition, and human-approval states rather than merely checking that those objects appear somewhere.
""",
    )
    outputs.append(plan_review)

    frame_path = review_dir / "generated" / "representative-frame.png"
    whole_path = episode_path / "delivery" / "generated" / "EP006-greybox-camera-review.mp4"
    deck_path = episode_path / "delivery" / "generated" / "EP006-greybox-deck-brand-title-prototype.mp4"
    media_lines = _media_probe_lines(whole_path, "Superseded map-camera")
    deck_media_lines = _media_probe_lines(deck_path, "90-second deck prototype")
    greybox_review = review_dir / "GREYBOX-REVIEW.md"
    _write(
        greybox_review,
        f"""# EP006 greybox review

- Render-data hash: `{_hash_line(render_path)}`
- Representative frame rendered: {'yes' if frame_path.is_file() else 'no'}
{chr(10).join(deck_media_lines)}
{chr(10).join(media_lines)}
- Current production state: `{state.get('current_stage', 'missing')}`

The full map-camera render is retained as a rejected diagnostic: it preserved the system correctly but asked the viewer to decode a network diagram. The 90-second deck prototype is also retained as a rejected diagnostic: it improved object continuity but still treated the episode as arranged boxes rather than precisely directed causal scenes. Neither is the current creative direction.

The next candidate must be compiled from validated shot-level scene direction. Director packets expose the exact VO, word timings, approved world slice, evidence, and tickets. Authored directions must then specify the audience inference, visual sentence, pixel geometry, exact text and emphasis, word-cued motion, evidence choreography, and transition handoff before another renderer pass.

Container duration can include frame or muxing padding beyond the locked narration. Neither prototype nor the superseded whole-episode render records `greybox_approved`.
""",
    )
    outputs.append(greybox_review)

    deck_review = review_dir / "DECK-PROTOTYPE-REVIEW.md"
    _write(
        deck_review,
        f"""# EP006 deck-style greybox rejected diagnostic

- Scope: locked VO opening, 0.000-90.000 seconds
- Composition: `BlueprintCinemaDeckPrototype`
- Render-data hash: `{_hash_line(render_path)}`
{chr(10).join(deck_media_lines)}
- Current production state: `{state.get('current_stage', 'missing')}`

## What it proved

Press **Play**. The test is whether the same few objects remain recognizable while their relationship changes:

`guest/stay -> OTA -> hotel -> commission -> broken return relationship -> guarded direct route`

Ignore drawing quality. You should not need to decode a network map or read a technical caption to understand which route works, which relationship is broken, and why the direct path is not open until audit, permission, and human review occur.

The opening now includes two deliberate bookends:

- `27.733-32.558`: **The Operator Economy** show-identity screen with the canonical typographic wordmark and `Build. Own. Operate.` tagline.
- `32.558-40.090`: **EP006 - Direct Booking Recovery** title screen with the fair first-booking/return-booking thesis.

There is no separate icon because the canonical design system does not define one. These screens are structural greybox plates, not polished title animation.

The last slides deliberately switch to the fragmented operator handoffs described by the VO. They were useful for testing object persistence, bookend timing, and the difference between a complete network map and a smaller composition.

## Why it was rejected

The boxes still function as labeled concepts rather than observable operations. Their spatial relationship does not consistently express what the VO says at that moment, and the renderer lacks exact shot-level composition, text-emphasis, motion-cue, evidence, and transition decisions.

## Decision boundary

This is a rejected 90-second diagnostic, not a whole-episode deck, an approved greybox, polished asset work, generated evidence, a production master, or a release artifact. It must not be extended or used as a visual input. The next bounded review begins with validated `scene-directions.json`; no prompt or prototype advances `production-state.json` automatically.
""",
    )
    outputs.append(deck_review)

    agent_lines = []
    work_dir = episode_path / "agents" / "work-orders"
    for work_path in sorted(work_dir.glob("*.json")) if work_dir.is_dir() else []:
        work = load_json(work_path)
        try:
            validate_work_order(work, episode_path)
            work_result = "valid"
        except ValidationFailure as error:
            work_result = "rejected: " + "; ".join(error.errors)
        deliverable_path = episode_path / "agents" / "deliverables" / work["work_order_id"] / "deliverable.json"
        if deliverable_path.is_file():
            deliverable = load_json(deliverable_path)
            try:
                validate_deliverable(deliverable, work, episode_path)
                packet_result = f"accepted packet ({deliverable.get('status')}); no gate advanced"
            except ValidationFailure as error:
                packet_result = "rejected packet: " + "; ".join(error.errors)
        else:
            packet_result = "no packet received"
        agent_lines.append(f"- `{work['work_order_id']}`: work order {work_result}; {packet_result}.")
    if not agent_lines:
        agent_lines = ["- No work orders have been issued."]
    agent_report = review_dir / "AGENT-WORK-REPORT.md"
    if not agent_report.is_file():
        _write(
            agent_report,
            "# EP006 agent-work report\n\n" + "\n".join(agent_lines) +
            "\n\nWorkers are isolated to their deliverable packet and cannot edit canonical episode JSON, record approvals, or advance production state.\n",
        )
    outputs.append(agent_report)

    implementation_path = review_dir / "IMPLEMENTATION-REPORT.md"
    if not implementation_path.is_file():
        _write(
            implementation_path,
            f"""# Blueprint Cinema implementation report

This report is finalized after tests and renderer checks. Current stage: `{state.get('current_stage', 'initialized')}`. Next gate: `{next_stage(state.get('current_stage', 'initialized')) or 'none'}`.
""",
        )
    outputs.append(implementation_path)
    return outputs
