# Blueprint Cinema agent instructions

These instructions apply to every file under `blueprint-cinema/`. Repository-level `../AGENTS.md` and `../../content-os/CLAUDE.md` still apply. When instructions conflict, content-os controls truth, voice, and release; repository guidance controls the broader OE workspace; this file controls the isolated Blueprint Cinema implementation and episode workspaces.

## Scope

Blueprint Cinema begins after the script, final narration, and word-level timings are locked. Do not use this subtree to change research, public claims, script wording, VO, canonical episode URLs, Shorts, publishing state, or content-os rules.

All new implementation and episode visual-production work stays under this directory until an explicit integration migration is approved.

## Required reading

Before any task, read:

1. `README.md`.
2. `TOOLCHAIN.md` and `PRODUCTION-TEAM.md`.
3. `ARCHITECTURE.md` and `WORKFLOW.md`.
4. `PORTING-POLICY.md` and `SOURCE-MAP.md` if upstream material may be consumed or reused.
5. `AGENT-WORKFLOWS.md` if delegating, receiving, reviewing, or merging agent work.
6. `references/README.md`, then every reference required by the assigned role.
7. The target episode's `README.md`, `episode.json`, input lock, and approved upstream artifacts.

Read `references/DIRECTION-SYSTEM.md`, `references/SHOT-GRAMMAR.md`, and `references/SCENE-DIRECTION-CONTRACT.md` before generating director packets, authoring direction, reviewing a shot board, compiling build packets, or implementing a scene.

Read `references/ASSET-MEDIA-CONTRACT.md` before searching, capturing, licensing, downloading, generating, selecting, staging, or placing media. Read `references/EDIT-SOUND-FINISHING.md` before edit, audio, HyperFrames plate, Resolve, color, caption, or delivery work. Read `references/REVIEW-QA.md` before issuing or resolving review findings.

Read only the additional reference documents needed for the assigned decision.

## Continuing directing decisions

Use [`oe-video-direction`](../.agents/skills/oe-video-direction/SKILL.md) before choosing or
revising visual form, animation, coverage, cuts, transitions or performance, and when interpreting
owner video feedback. It supplies the context-sensitive decision and learning procedure; existing
Boundary Ledger, film-direction, scene-direction and implementation contracts retain their roles.

Keep one continuing log at `episodes/<episode>/review/decisions/events.jsonl`, using that skill's
helper. Append meaningful choices with alternatives, rationale, cue/continuity details and reuse
limits; then append actual verification and feedback against the exact decision revision. Preserve
accepted artifact pins, rejected approaches and deferred triggers. Do not log every inspection or
turn a single episode choice into a global style rule. A worker returns proposed events in its
owned deliverable; the orchestrator appends after checking them. This records decisions within
existing authorization and creates no additional approval gate.

## Worktree safety

- The surrounding repository may be dirty. Preserve every pre-existing change and untracked artifact.
- Do not delete, rename, move, reset, checkout, or overwrite legacy episode work.
- Do not edit files outside `blueprint-cinema/` unless the user explicitly authorizes an integration change.
- Do not commit, push, upload, publish, purchase, license, or invoke paid generation without separate authorization.
- Use `rg` for discovery and `apply_patch` for authored file changes.
- Large or generated media must remain in ignored paths. Never add copied upstream VO, raw footage, rendered video, or caches to Git.

## Clean-room rule

Permitted upstream inputs and prohibited legacy visual inputs are defined in `PORTING-POLICY.md`. When uncertain, do not import the item. Record the question in the episode review folder and continue with independent work.

## Model provider direction

Keep the existing Higgsfield connection for Seedance avatar generation, with fal.ai for narration restoration when needed. The owner's later instruction, "lets keep the existing connetion," supersedes the earlier fal-only direction for this workflow. Preserve existing provider receipts and media provenance.

## Canonical tool rule

- HyperFrames is the only authorized implementation target for new Blueprint Cinema motion, designed scenes, directed animatics, and render plates.
- DaVinci Resolve is the canonical final timeline, conform, editorial, Fusion, color, Fairlight, caption, online, and delivery environment. Use Studio-only features only when the installed edition and license have been verified.
- The existing `renderer/` Remotion project is a superseded prototype. Preserve it for historical reproduction; do not add new production scenes, features, or polish there.
- Do not maintain dual HyperFrames and Remotion production paths. A fallback requires explicit operator approval and a recorded exception.
- The v1 CLI and state machine do not yet enforce the target toolchain. Always distinguish documentation-canonical requirements from implemented runtime behavior.

For every HyperFrames task, start with the installed `hyperframes` entry skill, route to `general-video`, then use the relevant domain skills. Use `media-use` for every media, font, audio, grade, LUT, caption, or media-operation requirement. Use `hyperframes-keyframes` for camera and keyframe work, `hyperframes-audio` for placed-track mixing, and `hyperframes-cli` for validation and rendering.

Blueprint Cinema overrides generic HyperFrames creative defaults. Do not introduce ambient drift, gratuitous gradients, template transitions, multiple competing focal points, duplicated narration text, decorative motion, or generic marketing-video density unless approved direction explicitly requires it.

## Canonical-state rule

The orchestrator is the only writer to:

- `episode.json` identity or status fields.
- `input-lock.json`.
- `production-state.json`.
- approval records and approval hashes.
- shared runtime code, shared schemas, and renderer integration points during a coordinated multi-agent run.
- merged canonical `episode-engine.json`, `world.json`, `visual-plan.json`, `asset-tickets.json`, asset manifest, edit manifest, and finishing manifest.
- merged canonical `scene-directions.json` when that optional authored layer is present.
- the HyperFrames root composition and canonical Resolve timeline during integration.

Worker agents never advance a gate. They return proposed artifacts and a manifest to their assigned deliverable path. The orchestrator validates and merges those outputs.

## Parallel-agent rule

Parallelize only work that is concrete, bounded, and independently writable. Every delegated task requires a work order that names:

- one episode;
- one role;
- exact input artifacts and hashes;
- owned output paths;
- forbidden paths;
- dependencies and required gate;
- acceptance checks;
- stopping conditions.

No two active workers may own the same output path. Do not delegate a single ordered creative decision to several agents that will overwrite one another. Parallel critique is allowed because each critic writes a separate report.

If subagents are unavailable, execute the same work orders serially. Artifact contracts and gates must not change based on agent availability.

## Agent deliverables

Each worker writes only under:

`episodes/<EP###-slug>/agents/deliverables/<work-order-id>/`

The packet must include `deliverable.json` plus the proposed files or report named by the work order. It must record input hashes, files created, checks run, unresolved questions, and whether any external source or generated media was used.

The orchestrator rejects a packet when:

- an input hash is stale;
- the worker touched a forbidden path;
- required provenance is absent;
- output is outside the owned path;
- the packet claims an approval or completed gate;
- acceptance checks are missing or fail.

## Creative rules

- Preserve the approved episode engine and persistent object identities.
- Show state changes, handoffs, evidence, economics, human judgment, exceptions, and outcomes.
- Do not infer finished layouts from narration text, section name, or asset type.
- Do not add motion merely for energy.
- Do not create generated platform interfaces, fake documents, fake evidence, or synthetic people presented as real cases.
- Do not source or generate polished assets before the approved directed animatic emits exact asset tickets.
- Do not compile shot-build packets from prose notes or an unvalidated `scene-directions.json`.
- Do not let HyperFrames or Resolve silently become a directing surface. Changes to meaning, evidence timing, business state, continuity, or transition purpose return upstream.
- Do not use AI renders as evidence or as synthetic documentary footage presented as a real person, place, process, or case.

## Reporting truth

Distinguish scaffolded, authored, validated, approved, selected, generated, rendered, conformed, picture-locked, finished, reviewed, delivered, uploaded, published, and independently verified. Documentation is not implementation; a schema-shaped JSON file is not an approval; a representative frame is not a whole-episode render; a Resolve timeline is not a validated delivery master.
