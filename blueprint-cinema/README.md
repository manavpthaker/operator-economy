# Blueprint Cinema

Blueprint Cinema is The Operator Economy's greenfield, CLI-first long-form visual production workspace. It turns a locked script, final voiceover, word-level timing, evidence, and brand contracts into a directed, asset-controlled, finished documentary blueprint.

This directory begins at the visual-production handoff. It does not replace research, claim verification, script approval, voice production, Shorts, packaging, upload, or release control.

```text
content-os truth, voice, rubric, and release rules
  -> OE research and approved script
  -> final VO and word-level timing
  -> Blueprint Cinema input lock
  -> episode engine
  -> persistent world
  -> full-timeline visual plan
  -> direction bible and rhythm map
  -> look development and representative motion test
  -> shot boards and scene directions
  -> whole-episode HyperFrames directed animatic
  -> ticketed asset candidates, selects, and production
  -> HyperFrames designed scenes and plates
  -> Resolve conform, rough cut, and picture lock
  -> Resolve Fusion, color, Fairlight, captions, and online
  -> delivery validation
  -> existing Shorts, packaging, upload, links.json, and release gates
```

## Current status

The documentation-canonical production system now specifies HyperFrames as the designed-scene, motion, directed-animatic, and deterministic-render runtime, with DaVinci Resolve as the final editorial and finishing environment. `TOOLCHAIN.md` owns that boundary. `PRODUCTION-TEAM.md` and the references define the department-level decisions and artifacts required to make it professional rather than template-driven.

Most of the existing v1 CLI, state machine, tests, and isolated `renderer/` remain a Remotion-era implementation through the recorded `greybox_ready` state for EP006. The exception is the greenfield scene-direction 1.2.0 schema, semantic validation, and director/build packet compiler, which implement the bounded shot contract described below without advancing episode state. The remaining v1 controls prove input locking, sequential approval, packet isolation, deterministic compilation, and runtime experiments, but they do not implement or enforce the canonical HyperFrames-to-Resolve workflow. The map-camera and 90-second deck prototypes were rejected as creative answers. Nothing in this documentation advances an episode gate.

Do not begin new production work in the v1 Remotion renderer. Preserve it for historical reproduction until a separate implementation migration replaces the runtime, state machine, schemas, commands, and tests.

## Read order

1. Repository-level `../AGENTS.md` and `../../content-os/CLAUDE.md`.
2. This directory's `AGENTS.md`.
3. `TOOLCHAIN.md` and `PRODUCTION-TEAM.md`.
4. `ARCHITECTURE.md` and `WORKFLOW.md`.
5. `PORTING-POLICY.md` and `SOURCE-MAP.md`.
6. `AGENT-WORKFLOWS.md` before delegating parallel work.
7. `references/README.md` and every reference required for the assigned department.
8. The target episode's `README.md`, identity, input lock, and approved artifacts.

Use `CODEX-BUILD-PROMPT.md` only when the separate v2 runtime migration is authorized. It is an implementation brief, not permission to modify episode state or start production.

## Directory map

| Path | Responsibility |
|---|---|
| `bin/` | Existing v1 operator command, including bounded scene-direction validation and prompt compilation; target runtime CLI migration is not yet implemented. |
| `src/` | Existing v1 deterministic orchestration, validation, state, hashes, reports, and the greenfield scene-direction prompt compiler. |
| `schemas/` | Strict machine contracts, including the implemented scene-direction 1.2.0 contract; the complete target asset, edit, and finishing contracts remain documentation. |
| `renderer/` | Superseded isolated Remotion prototype, retained for reproduction only. |
| `tests/` | Existing v1 contract, clean-room, timing, agent, render-data, and Remotion tests. |
| `templates/` | Episode-agnostic direction, shot, asset, handoff, and review artifact templates. |
| `episodes/` | Canonical `EP###-slug` Blueprint Cinema workspaces. |
| `references/` | Detailed direction, shot, media, finishing, and QA contracts. |

## Implemented scene-direction commands

These commands implement the bounded scene-direction 1.2.0 validation and prompt-compilation layer. They do not create the full canonical direction package, advance episode state, create a HyperFrames project, or create a Resolve handoff:

```bash
# Generate one directing packet per approved visual-plan sequence.
bin/oe-cinema build-director-prompts EP006-direct-booking-recovery

# Work on one bounded sequence while the visual language is being established.
bin/oe-cinema build-director-prompts EP006-direct-booking-recovery \
  --sequence sequence-hook-01

# After scene-directions.json is authored and reviewed.
bin/oe-cinema validate-scene-directions EP006-direct-booking-recovery
bin/oe-cinema build-scene-prompts EP006-direct-booking-recovery
```

Read `references/SCENE-DIRECTION-CONTRACT.md` before authoring or compiling these packets.

## Core rules

- Voiceover is the timing authority.
- A beat is not automatically a shot.
- The episode is a persistent operating world, not a sequence of decorated slides.
- Motion must communicate a business verb or a motivated camera move.
- Evidence must remain attached to the claim or system parameter it supports.
- Assets enter only through exact tickets with rights and provenance.
- AI-rendered media can establish a world but cannot serve as evidence.
- Scene context determines the form and coverage; narration alone does not. Every sequence declares context and every shot carries editorial rationale, cut/hold motivation, and a specific review question. Explicit `narrated_dramatization` permits illustrative interaction whose essential meaning comes from narration; `narrated_observation` retains its no-speech/missing-line constraints. Source, sync, and presenter delivery remain bound to their audible synchronized modes. See `references/SCENE-DIRECTION-CONTRACT.md` for the 1.2.0 fields and deliberate reauthoring boundary.
- Every shot carries generator-independent, non-optional direction facts: what stays still, master/setup relationship and reference, action line and screen direction, typed continuity anchors, and initial and final images.
- The default transition is a cut; designed transitions must explain a relationship.
- The whole episode is directed as an animatic before polished asset production.
- HyperFrames implements approved direction; it does not invent it.
- Resolve owns the final editorial and finish but never becomes a hidden source of visual logic.
- One orchestrator owns canonical state and approvals. Parallel agents produce isolated packets.

## Episode identity

Every new workspace is named `EP###-slug`, for example `EP006-direct-booking-recovery`. The number is explicit and never inferred from directory order. The folder name, episode number, episode code, and slug must agree with `episode.json`.

The existing `studio/originate/<slug>/` folder remains the upstream editorial workspace. It is referenced through a hash-pinned input lock; it is not renamed or moved.
