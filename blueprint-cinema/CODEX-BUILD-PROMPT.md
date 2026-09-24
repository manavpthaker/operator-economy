# Codex prompt: implement the Blueprint Cinema v2 production system

Copy the prompt below into a new Codex task when implementation is authorized. It is episode-agnostic and assumes this documentation scaffold already exists.

---

You are implementing the documentation-canonical Blueprint Cinema v2 production system in the populated Operator Economy repository.

## Repository and safety

- Canonical repository: `/Users/brownmanbrain/GitHub/operator-economy`.
- Confirm that path is populated before substantive work. Do not work in the lightweight `Documents/GitHub/operator-economy` shell.
- Read the repository `AGENTS.md` and `../content-os/CLAUDE.md` before changes.
- Then read, completely and in order:
  1. `blueprint-cinema/AGENTS.md`
  2. `docs/blueprint-cinema.md`
  3. `docs/blueprint-cinema-migration.md`
  4. `blueprint-cinema/TOOLCHAIN.md`
  5. `blueprint-cinema/PRODUCTION-TEAM.md`
  6. `blueprint-cinema/ARCHITECTURE.md`
  7. `blueprint-cinema/WORKFLOW.md`
  8. `blueprint-cinema/PORTING-POLICY.md`
  9. `blueprint-cinema/SOURCE-MAP.md`
  10. `blueprint-cinema/AGENT-WORKFLOWS.md`
  11. `blueprint-cinema/references/README.md` and every reference it lists
  12. `blueprint-cinema/templates/episode/README.md` and every template it lists
- Treat the surrounding worktree as dirty. Inspect first. Preserve all unrelated tracked and untracked work.
- Do not delete, rename, reset, move, or overwrite the current v1 runtime, Remotion prototypes, experiments, episode artifacts, review renders, or upstream editorial work.
- Do not commit, push, publish, upload, purchase, license, or run paid generation without explicit authorization.
- Use `apply_patch` for authored edits and `rg` for discovery.

## Objective

Implement the episode-agnostic Blueprint Cinema v2 runtime described by the documentation. Blueprint Cinema owns creative authority, direction, continuity, manifests, review, and approvals. HyperFrames is the only authorized new-production runtime for designed scenes, motion graphics, directed animatics, and render plates. DaVinci Resolve is the canonical final editorial and finishing environment.

Do not build an EP006 scene, polished opening, asset, AI render, or final edit merely to demonstrate progress. First implement the reusable contracts, state, scaffold, adapters, validation, prompt compilation, HyperFrames project boundary, Resolve handoff boundary, and tests. Use temporary fixtures and the least expensive representative media needed for verification.

The current v1 CLI, state schema, render-data compiler, tests, and isolated Remotion renderer are historical implementation. They are evidence and migration inputs, not the target. Do not maintain two active renderer paths and do not translate the rejected Remotion compositions into HyperFrames.

## Canonical tool routing

Before HyperFrames implementation work, read the installed `hyperframes` entry skill completely. Route long-form OE episodes through `general-video`; use the faceless-explainer materials only as borrowed story and shot technique, not as the owning short-form workflow.

Use:

- `hyperframes-core` for the composition contract;
- `hyperframes-creative` for `BRIEF.md`, `frame.md`, storyboard, design, and composition decisions subordinate to approved Blueprint Cinema direction;
- `hyperframes-animation` for approved motion behavior;
- `hyperframes-keyframes` before any camera, zoom, pan, crop, reframe, path, or keyframe work;
- `hyperframes-audio` for placed-track mixing, ducking, carving, automation, or effects;
- `hyperframes-registry` and `npx hyperframes catalog --query "<approved move>"` before hand-authoring a motion primitive;
- `hyperframes-cli` for lint, check, snapshots, animation maps, preview, and render;
- `media-use` for every asset, image, icon, logo, font, footage, audio, caption, grade, LUT, treatment, generation, or media-operation need.

Blueprint Cinema overrides generic framework creative defaults. Do not add ambient motion, template transitions, gratuitous gradients, generic marketing density, duplicated narration text, multiple competing focal points, or decorative animation unless approved direction explicitly calls for it.

For Resolve, inspect the installed application version, edition/license, developer scripting documentation, scripting availability, supported interchange formats, and headless/external-script limitations before implementation. Use supported Python or Lua APIs only for deterministic ingest, conform, markers, project export, render jobs, delivery, and reports. Never automate creative approval or hide editorial changes inside the Resolve project.

## Target state machine

Implement and test this exact target order:

1. `inputs_locked`
2. `episode_engine_approved`
3. `world_approved`
4. `visual_plan_approved`
5. `visual_language_approved`
6. `scene_direction_approved`
7. `directed_animatic_approved`
8. `asset_selects_ready`
9. `rough_cut_approved`
10. `picture_lock_approved`
11. `finish_approved`
12. `delivery_validated`

Every approval is hash-bound. An upstream change invalidates all dependent states. Generated files, valid schemas, snapshots, renders, HyperFrames checks, Resolve timelines, and successful exports never approve themselves.

Write an explicit migration for existing v1 state names. Do not reinterpret or silently rewrite real episode state. Test migration behavior on fixtures before offering a real-episode migration command. A real episode migration requires a separate operator decision.

## Required implementation areas

### 1. Episode initialization

Extend the initializer so a new `EP###-slug` workspace creates the documentation-canonical structure in `blueprint-cinema/templates/episode/README.md`, including direction, HyperFrames, asset, edit, handoff, Resolve, review, prompt, and delivery locations.

Initialization must:

- require explicit number and slug;
- validate number, code, slug, and folder agreement;
- reject collisions and mismatches;
- never infer episode order;
- never rename or copy the upstream editorial workspace;
- create placeholders and metadata only, never generated media;
- preserve ignored large-media boundaries.

### 2. Schemas and semantic validation

Create strict schemas and semantic validators for the target artifacts, including:

- direction bible identity and approval pins;
- rhythm map with complete, non-overlapping timeline coverage;
- style-frame and motion-test review records;
- sequence treatments and shot-board references;
- scene directions with exact words, timing, geometry, hierarchy, action phases, evidence choreography, continuity, sound intent, and observable checks;
- asset tickets, candidates, selects, manifests, rights, provenance, technical metadata, synthetic status, derivatives, and timeline uses;
- edit plan and sound plan;
- HyperFrames render and plate manifest;
- Resolve handoff and conform manifest;
- picture-lock, finishing, color, mix, caption, delivery, and QC reports;
- artifact-bound review findings and approvals.

Schema validity is necessary but not sufficient. Add cross-file semantic checks for IDs, hashes, timing, frame coverage, word cues, transition handoffs, evidence IDs, asset versions, rights status, local files, duration, handles, alpha, color metadata, and downstream invalidation.

### 3. Direction and prompt compilation

Extend the deterministic compiler so director packets include every canonical input in `references/DIRECTION-SYSTEM.md` and `references/SCENE-DIRECTION-CONTRACT.md`.

Compile approved direction into:

- one bounded HyperFrames build packet per shot using `templates/episode/HYPERFRAMES-BUILD-PACKET.template.md`;
- exact ticket-specific search, capture, archival, B-roll, music, SFX, graphic, or caption packets;
- AI plate packets using `templates/episode/AI-PLATE-GENERATION-PACKET.template.md`;
- a Resolve edit and handoff package using `templates/episode/EDIT-RESOLVE-HANDOFF.template.md`.

Packets must be deterministic, hash-pinned, path-bounded, non-approving, and forbidden from asking a builder to invent the creative direction.

### 4. HyperFrames project contract

Implement an episode-local HyperFrames project under `episodes/EP###-slug/hyperframes/`.

Requirements:

- Node.js 22 or newer and FFmpeg probes;
- explicit HyperFrames version pin and recorded upgrade history;
- read-only resume check with `npx hyperframes@latest upgrade --project . --check`;
- local frozen fonts and media only;
- no render-time network request;
- thin root composition owning locked VO, captions, timeline slots, and episode-level tracks;
- bounded sequence and shot compositions;
- explicit composition, sequence, shot, asset, evidence, and world IDs;
- deterministic seek-safe timing;
- static end-state construction before animation;
- no narration parsing to choose layout, motion, or assets;
- required lint, final check, snapshots, animation-map review, Studio preview, render approval, media probe, and manifest output;
- MP4 reference renders, opaque plates, alpha MOV or WebM, and RGBA image-sequence paths as required by the handoff;
- full-duration low-complexity technical render before production-scale asset work.

Do not build a monolithic long-form HTML file. Preserve continuous narration at the root while scenes mount modularly.

### 5. Asset and media control

Implement the states and manifests in `references/ASSET-MEDIA-CONTRACT.md`.

Search output is a candidate, not a select. Recommendation is not approval. A selected asset must be local, hash-addressed, rights-reviewed, provenance-complete, technically probed, versioned, and attached to exact timeline uses before it enters HyperFrames or Resolve.

AI generation must remain separately authorized, non-evidentiary, continuity-controlled, disclosure-recorded, candidate-reviewed, and capped by retry and stopping conditions.

### 6. Resolve handoff and finishing boundary

Implement a deterministic handoff package containing the manifest, approved animatic reference, supported interchange files, markers, plates, selects, proxies, VO, music, SFX, ambience, captions, color metadata, and reports described in `TOOLCHAIN.md`.

Where supported and validated, implement optional scripts for:

- project and bin setup;
- media import and relink;
- timeline import;
- markers and track naming;
- reference and plate placement;
- missing-media and conform reports;
- render settings and jobs;
- project export and delivery reports.

Fail clearly when Resolve is closed, unavailable, not licensed for a required feature, or returns an unsupported operation. Provide a manifest-driven manual handoff path; do not silently degrade or fabricate success.

Implement the round-trip rule: changes to shot purpose, evidence timing, business state, object continuity, transition meaning, script, or VO stop and return upstream. The Resolve project can never be the only record of a canonical change.

### 7. Review and QA

Implement review reports and gates from `references/REVIEW-QA.md` with blocking, major, polish, and observation severity. Reports must identify exact artifact hashes, time ranges, sequence and shot IDs, frames or evidence, expected behavior, observed behavior, owner, disposition, and retest evidence.

At minimum, independently verify:

- engine honesty;
- world integrity;
- full-timeline plan coverage;
- visual-language cohesion;
- shot-board composition and continuity;
- representative motion behavior;
- whole-episode animatic comprehension and rhythm;
- asset semantics, rights, provenance, and disclosure;
- Resolve conform and rough cut;
- picture lock;
- color;
- sound;
- captions and accessibility;
- rendered delivery master.

### 8. Parallel agents

Preserve the existing work-order and deliverable model. Expand role and acceptance contracts to match `PRODUCTION-TEAM.md` and `AGENT-WORKFLOWS.md`.

Parallel workers may own isolated critiques, non-overlapping direction proposals, exact ticket candidates, bounded HyperFrames compositions, or read-only QA. They may not share output paths, write canonical state, approve gates, integrate the root composition, integrate the Resolve timeline, choose conflicting visual languages, or perform an unchecked search-select-approve chain.

If agents are unavailable, run the same packets serially. Do not weaken contracts based on concurrency.

## Implementation sequence

Use small, reversible phases and report after each:

1. Audit v1 implementation, documentation, dirty worktree, installed HyperFrames, installed Resolve, and current test baseline.
2. Write the migration design and exact file-change map. Resolve contradictions before code.
3. Implement target identity, scaffold, schemas, state migration, and tests without touching real episode state.
4. Implement direction artifacts, prompt compilers, semantic checks, and tests.
5. Implement asset manifests, selection gates, local-media checks, and tests.
6. Implement a minimal episode-local HyperFrames fixture, tool probes, root/scene contract, validation ladder, render manifests, and tests.
7. Run a short representative fixture and a full-duration low-complexity technical fixture; do not use polished EP006 work.
8. Implement Resolve handoff manifests, interchange, feature probes, optional deterministic scripts, failure behavior, and tests.
9. Implement review, picture-lock, finish, and delivery contracts and tests.
10. Run clean-room, state, schema, prompt, media, HyperFrames, handoff, and failure-path validation.
11. Update documentation only where implementation truth now differs, marking exact capabilities as implemented and leaving unresolved work explicit.

Do not move to a later phase while a foundational gate is invalid. Continue with independent work only when it cannot be invalidated by the blocker.

## Required tests

Tests must use temporary fixtures and cover at least:

- identity mismatch and collision;
- canonical scaffold creation;
- stale hashes and downstream invalidation;
- prohibited legacy path detection;
- complete timing and word coverage;
- direction, hierarchy, motion-cue, evidence, continuity, and asset reference failures;
- overlapping and gapped rhythm, shot, and edit ranges;
- unapproved visual language, scene direction, animatic, select, rough cut, picture lock, or finish;
- raw URL, missing local asset, changed checksum, absent rights, and missing disclosure;
- generated evidence rejection;
- HyperFrames version, Node, FFmpeg, network, lint, check, snapshot, duration, alpha, and media-probe failures;
- stale or mismatched HyperFrames plate manifests;
- Resolve unavailable, edition/feature unavailable, unsupported interchange, missing media, frame offset, alpha mismatch, and color interpretation failures;
- unreturned Resolve editorial changes;
- incomplete captions, loudness, true peak, master probe, and full-playback QC;
- worker path conflicts, stale packets, approval claims, and state mutation attempts;
- no mutation of real episode state during tests.

## Completion contract

Do not call the migration complete unless:

- the canonical docs and implementation agree;
- all target artifacts have strict and semantic validation;
- the state machine and invalidation behavior are tested;
- a new numbered fixture initializes cleanly;
- prompt packets compile deterministically from approved hashes;
- a representative HyperFrames fixture passes lint, check, snapshots, animation-map review, preview validation, render, and media probe;
- a full-duration low-complexity fixture renders reproducibly;
- the Resolve handoff validates, or exact installed-edition limitations and a tested manual path are documented;
- all new tests pass and the preserved v1 suite still passes or has an explicit migration disposition;
- no real episode gate, publication state, licensed asset, paid generation, or external system was changed without authorization;
- the final report distinguishes scaffolded, authored, implemented, validated, rendered, reviewed, approved, conformed, picture-locked, finished, delivered, uploaded, published, and independently verified.

Lead the final report with what is genuinely implemented, what remains documentation-only, exact validation evidence, paths changed, preserved historical artifacts, and the next safe operator decision.

---
