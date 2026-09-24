# Parallel agent workflows

## Decision

Blueprint Cinema supports parallel agents, but not as several editors changing the same episode at once. It uses a root orchestrator, machine-readable work orders, isolated deliverable directories, explicit path ownership, and serialized approval gates.

The useful unit of delegation is a bounded production packet—not an entire episode and not a vague role such as "make this cinematic."

## Topology

```text
                         ORCHESTRATOR
                  owns state, merges, approvals
                              |
              +---------------+---------------+
              |               |               |
          worker A         worker B         worker C
       isolated packet  isolated packet  isolated packet
              |               |               |
              +---------------+---------------+
                              |
                    validation and merge gate
```

A practical default is one orchestrator plus no more than three concurrent workers. The implementation may expose a configurable limit, but correctness cannot depend on concurrency.

## Why this boundary exists

Parallel agents are valuable when tasks divide into independent, bounded workstreams. They become counterproductive when steps form one ordered creative chain or several agents contend over shared mutable state. Blueprint Cinema therefore parallelizes discovery, packet production, and independent review while serializing canonical authorship, integration, and approval.

## Roles

### Orchestrator

Owns identity, hashes, work orders, canonical JSON, shared implementation files, state transitions, merges, approvals, and the final operator report. It verifies every packet against current input hashes before use.

### Engine critic

Reviews a proposed episode engine for mechanical honesty, fairness, actionable viewer promise, missing human judgment, and visual cliché. Writes a report; never edits the canonical engine.

### Editorial producer / transcript mapper

Maps word ranges to narrative states, candidate persistent sequences, and timing pressure. It does not invent finished layouts or reuse the old storyboard.

### Evidence editor / mapper

Maps approved claims and sources to world parameters and proof-bench requirements. It preserves provenance and identifies gaps without changing public claims.

### World integrity reviewer

Checks object IDs, paths, failure states, consent, suppression, escalation, economics, and camera anchors. Writes a report or isolated proposal.

### Creative director

Authors or reviews the episode direction bible, rhythm map, visual thesis, style-frame brief, and representative motion-test brief. It does not implement scenes while the visual language is undecided.

### Documentary director

Directs human reality, B-roll, archival, original capture, observation, reconstruction, and documentary continuity. It reads scene context before choosing picture/audio mode, coverage, and cut/hold motivation, and defines shot jobs without choosing unlicensed media. It records scene_context and editorial_intent and reviews the mode-specific relationship with the actual track. It also authors the adjacent direction facts: what stays still, master/setup role and exact reference, action line and screen direction, typed continuity anchors, and initial and final images. Under narrated observation it directs non-speaking action; under explicit narrated dramatization it may direct illustrative conversation, rapport, and attempted answers when narration supplies essential meaning. Mute viewing is diagnostic in dramatization; disclosure and audiovisual comprehension checks are required. Narrated modes cannot borrow synchronized delivery face functions. `source_delivery` is reserved for natural-sound observation with audible synchronized source; `sync_delivery` stays in sync dialogue; `presenter_delivery` stays in presenter address.

### Motion director / storyboard artist

Authors sequence treatments, shot boards, entry-action-consequence-settle-handoff phases, visual hierarchy, word-cued motion, and transition continuity. For designed and graphic shots, it authors the same adjacent direction facts required of documentary shots. The direction integrator confirms those facts exist and resolve across every shot before compilation. It returns exact direction; it does not write HyperFrames code in the same packet.

### Production and art direction reviewers

Review world material, composition, typography, information hierarchy, design-system fidelity, evidence treatment, and avoidance of generic presentation, web-page, motion-template, and AI aesthetics. Each review is isolated by lens.

### Asset producer

Owns one or more exact ticket IDs within one media lane: evidence capture, licensed footage, archival, rendered plate, graphics, sound, or captions. It cannot broaden the ticket or select generic footage merely because it is available.

### HyperFrames technical director

Owns the pinned runtime, root composition, local media, shared interfaces, render configuration, validation, and handoff manifest. It integrates bounded scene outputs but does not redesign them.

### HyperFrames scene builder

Implements a bounded, approved shot or sequence packet in an explicitly owned composition path. It builds the static end state first, then approved motion, snapshots, checks, and its sidecar. Only the technical director changes the root composition or shared runtime.

### Resolve assistant / conform editor

Prepares deterministic media ingest, proxy and source relink, markers, interchange, track layout, plate alignment, and conform reports. It does not make unrecorded creative edits or approve picture lock.

### Finishing specialist

Owns one isolated read-only recommendation or approved finishing lane: Fusion composite, color, Fairlight mix, captions/accessibility, or online QC. Canonical timeline writes remain serialized by the lead editor or finishing integrator.

### QA reviewer

Performs one independent read-only review: editorial/comprehension, continuity/cadence, provenance/rights, synthetic-media disclosure, or technical delivery. It writes findings and never advances state.

## Parallel waves

| Wave | Required gate | Safe parallel packets | Serialized result |
|---|---|---|---|
| 0 | none | repository/source inspection only | orchestrator creates identity and input lock |
| 1 | `inputs_locked` | engine critics with different review lenses | orchestrator merges and approves engine |
| 2 | `episode_engine_approved` | transcript map, evidence map, failure/human-gate audit | orchestrator authors and approves world |
| 3 | `world_approved` | non-overlapping timeline segments, boundary review | one integrator completes and approves visual plan |
| 4 | `visual_plan_approved` | direction-bible critique, rhythm review, bounded lookdev proposals | one creative director integrates visual language |
| 5 | direction draft complete | independent art, documentary, evidence, information-design, typography, and motion reviews | showrunner approves visual language after style frames and motion test |
| 6 | `visual_language_approved` | non-overlapping sequence treatments and shot boards | one motion director integrates boundaries and scene directions |
| 7 | `scene_direction_approved` | bounded HyperFrames scene builds, runtime checks, animatic QA | technical director assembles; orchestrator approves full directed animatic |
| 8 | `directed_animatic_approved` | ticket-scoped evidence, footage, capture, AI plates, graphics, music, sound, and captions | media manager and editors accept exact selects |
| 9 | `asset_selects_ready` | bounded HyperFrames production scenes, plate QA, proxy and interchange preparation | one technical director and lead editor perform handoff and conform |
| 10 | conform passed | ticket replacements, isolated composite fixes, read-only editorial reviews | one lead editor owns rough cut and picture-lock timeline |
| 11 | `picture_lock_approved` | isolated color, Fairlight, Fusion, caption, online, rights, disclosure, and technical reviews | one finishing integrator produces finish; orchestrator validates delivery |

## Work-order contract

Every work order is stored at:

`episodes/<episode>/agents/work-orders/<work-order-id>.json`

It includes:

- stable work-order ID and episode folder;
- role and objective;
- required production gate;
- exact inputs with SHA-256 hashes;
- owned output paths;
- forbidden paths;
- ticket IDs or non-overlapping timeline range when applicable;
- dependencies;
- acceptance checks;
- permission boundary;
- maximum retries and stopping conditions.

`schemas/agent-work-order.schema.json` and the runtime semantic checks implement this contract, including hash freshness for issued orders, isolated owned paths, forbidden paths, permissions, retry limits, and stopping conditions.

## Deliverable contract

Every worker writes:

`episodes/<episode>/agents/deliverables/<work-order-id>/deliverable.json`

The manifest records:

- the matching work-order ID;
- input hashes actually used;
- files produced;
- validation commands and outcomes;
- sources and provenance touched;
- assumptions and unresolved questions;
- whether external writes, paid services, or synthetic generation occurred;
- a status of `complete`, `partial`, or `blocked`.

`schemas/agent-deliverable.schema.json` and the runtime packet validator implement this contract. They reject stale declared hashes, files outside the owned packet, approval claims, state-change claims, and unsupported completion records.

`complete` means the packet satisfies its work order. It never means a production gate is approved.

## Merge protocol

1. Confirm work-order and deliverable schemas.
2. Recompute and compare every input hash.
3. Confirm all outputs are within owned paths and no forbidden path changed.
4. Run packet acceptance checks.
5. Review provenance and synthetic status.
6. Merge or copy the proposal into canonical authored data through the orchestrator.
7. Validate the complete canonical artifact, including cross-packet boundaries.
8. Record an approval only through the appropriate CLI gate.

## Never parallelize

- Input-lock creation or approval recording.
- Simultaneous edits to `production-state.json` or canonical authored JSON.
- Two workers selecting different visual systems for the same sequence.
- Adjacent timeline segments without an assigned boundary integrator.
- The canonical HyperFrames root composition or shared runtime.
- The canonical Resolve rough-cut, picture-lock, or finishing timeline.
- Direction and implementation of the same shot in one unreviewed packet.
- Asset search, selection, rights approval, and timeline acceptance by one unchecked worker.
- Publication, upload, licensing, purchases, or paid generation.

## Failure handling

A blocked packet does not block unrelated packets. The orchestrator reports the narrow dependency, completes independent work, and does not fabricate missing evidence or silently relax a ticket. If an upstream hash changes, affected work orders become stale and must be reissued.
