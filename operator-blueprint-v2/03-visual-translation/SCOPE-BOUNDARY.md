# Step 3 scope boundary

Status: **approved boundary**, 2026-09-01, with a proposed Boundary Ledger derivation correction
dated 2026-09-02. Step 3 itself remains boundary-only until a full design pass is approved.

Porting manifest: `PORTING-MANIFEST.md`

This document decides what Step 3 owns, what it consumes, what it hands on, and what it must never do. It exists before the standard and the gates deliberately, because Blueprint Cinema's own documentation sprawled across Steps 3 through 6 and that is the failure this boundary prevents.

## The one-line charter

Step 3 turns a locked episode into a **coherent visual language**: what the episode means visually, what world it happens in, what each moment of narration is doing, and how the whole thing should look and feel.

It does not draw shots, build scenes, source footage, or choose a runtime.

## Owns

| Artifact | What it decides |
|---|---|
| **Episode engine** | Operator, customer, owned value, constraint, counter-system, and outcome object derived from Step 1; material `business_operation` state changes derived from locked upstream artifacts; semantic roles and `boundary_ledger_operation_id` values selected from a hash-pinned Boundary Ledger core and motion binding |
| **Persistent world** | Stable objects, zones, paths, state transitions, evidence anchors, failure routes, money flows, human gates, camera anchors, object permanence |
| **Full-timeline visual plan** | Every timed unit against the word-level transcript: mode, camera anchor, business-operation binding, carried and focused objects, world state before and after, evidence attachment |
| **Direction bible** | Visual thesis, reality treatment, system treatment, proof treatment, typography, camera, episode-specific application of Boundary Ledger operations, footage policy, sound intent, and negative rules |
| **Rhythm map** | Whole-episode energy, information density, visual mode, proof placement, human contact, sound, and transitions |
| **Look development** | Style frames proving the episode-specific visual language |
| **Causal-relationship selection** | Which episode relationships Step 4 must preserve and why. It cannot create brand motion vocabulary or apply an implementation primitive to a shot |
| **Continuity and cognitive-load contracts** | The rules Step 4 must satisfy |

## Consumes, and may not change

From Step 2 at narration lock:

- final narration master and its hash
- **word-level transcript and intentional-pause map**
- narration duration

From Step 1 at editorial lock:

- Operator Canvas, Episode Investment Thesis, narrative spine, beat sheet, claims map
- the locked script and its `W` identity

From Boundary Ledger at design-system lock:

- `semantic-core.json`, its Boundary Ledger version, and its SHA-256
- `bindings/motion.json`, its status, and its SHA-256
- the permitted semantic-role-to-operation relationships in that exact binding

**Step 3 may not rewrite the editorial argument, restate a claim beyond its approved wording, or estimate narration timing.** Timing comes from the Step 2 transcript. If Step 3 believes a claim needs different wording, it raises a change request to Step 1 rather than adapting it visually.

**Step 3 may not copy, rename, widen, or replace Boundary Ledger semantics.** It derives what the
business does from an exact upstream before/after state, then selects the compatible role and
operation from the pinned design-system authority.

## Hands to Step 4

An approved engine, world, visual plan, direction bible, rhythm map, style frames, causal-relationship
selection, and Boundary Ledger operation bindings, with hashes. Step 4 then produces sequence
treatments, shot boards, scene directions, the motion test, the animatic and the asset plan.

## Does not own

| Not Step 3 | Where it lives |
|---|---|
| Sequence treatments, shot boards, scene directions | Step 4 |
| Representative motion test and directed animatic | Step 4 |
| Asset tickets, candidates, selects, rights and provenance | Step 5 |
| Conform, picture lock, colour, Fusion, mix, captions, delivery | Step 6 |
| **Runtime and toolchain choice** | Steps 4-6 |
| **Cross-media semantic roles and operation vocabulary** | Boundary Ledger |
| **Animation, scene, renderer, easing, or audio implementation primitives** | Steps 4-6 |

## Proposed amendment to the V2 lifecycle

The V2 README currently lists **persistent world** under Step 4 preproduction. That ordering cannot hold, because a direction bible describes how a world looks and feels and therefore requires the world to exist first.

`blueprint-cinema/WORKFLOW.md` orders it engine, then world, then visual plan, then direction bible. EP006 validated that order in practice with an approved engine, an approved world and a 162-unit visual plan.

**Approved by the owner 2026-09-01 and applied.** `persistent world` moved from the Step 4 lifecycle line to Step 3. Step 4 is restated as sequence treatments, shot boards, scene direction, motion test, animatic and asset plan.

The V2 README lifecycle table now reflects this. Blueprint Cinema's production order is therefore the order V2 follows: engine, world, visual plan, direction bible, rhythm map, look development, then Step 4.

## Why Step 3 is tool-agnostic

Recorded here because it is a boundary decision, not an implementation preference.

Blueprint Cinema names HyperFrames canonical for motion and Resolve canonical for finishing. Step 3 does not adopt that and does not depend on it.

The Remotion deauthorization took an approved 162-unit visual plan out of production with it because
the plan was coupled to a runtime that was later withdrawn. The current production toolchain can be
authoritative for implementation without becoming part of an episode's semantic lock. Direction
must survive a compatible runtime change.

Step 3 therefore produces direction any runtime could execute. Steps 4 through 6 own the runtime.

## Dependency that gates any real Step 3 run

**Step 3 consumes the word-level transcript, which Step 2 produces at N6.**

EP007 has passed N1 and captured N4B, but N5, N6 and N7 remain open, so no word-level transcript exists yet. Step 3 can therefore be designed and fixture-tested now, but cannot run on a real episode until Step 2 closes for that episode.

This mirrors how Steps 1 and 2 were built, and is recorded so it is a planned sequence rather than a late discovery.

## Resolved design questions

### 1. The episode engine derives business state and selects brand operations

Owner direction, 2026-09-01: *the episode engine is just nomenclature. Whatever has been built out already can build the engine and Step 3 can build the visual model on top of that.*

Checked against EP006's approved engine. The original ten substantive fields split into upstream
business state, brand semantics, and episode direction:

| Engine field | Source | Step 3 treatment |
|---|---|---|
| `operator` | Canvas §1 | **derived** |
| `input_customer`, `eligible_return_customer` | Canvas §2 | **derived** |
| `constraint` | Canvas §3 | **derived** |
| `counter_system` | Canvas §4 and §6 | **derived** |
| `owned_value`, `outcome_object` | Canvas §5 | **derived** |
| `business_operation` with before/after state | Canvas §6, narrative spine, beat sheet, or claims map | **derived** with exact source locator |
| `boundary_ledger_semantic_role_id` | Boundary Ledger semantic core | **selected** from the hash-pinned authority |
| `boundary_ledger_operation_id` | Boundary Ledger semantic core plus motion binding | **selected** from the hash-pinned authority |
| `episode_visual_model` | Derived business operations plus episode visual judgment | **authored by Step 3**; persistent actors, zones, and relationships only |
| `reality_world` | — | **authored by Step 3** |
| `guardrails` | — | **authored by Step 3** |

The ambiguous old `visual_mechanic` field is replaced by the narrower `episode_visual_model`. The
old `motion_verbs` field is removed. The replacement preserves Step 3's authority to design the
episode-specific model while preventing it from creating a parallel brand motion vocabulary or
smuggling implementation ideas into the semantic layer.

**Rule: Step 3 derives business fields and operations from the locked upstream state and may not
re-decide them. It then selects, but does not author, a Boundary Ledger semantic role and operation
ID.** Divergence from upstream, an unknown operation ID, a role-operation pair disallowed by the
pinned binding, a stale hash, or a local motion verb all fail the gate.

Step 3 still authors the episode visual model, persistent world, continuity, direction, rhythm, and
sequencing. Those decisions apply the semantic core; they do not create renderer components or
animation primitives for Step 4.

This shrinks Step 3's authored surface and removes the most likely source of Step 1 to Step 3 drift.

### 2. The visual plan is approved per act, not whole

EP006 approved 162 units in a single decision. That is not reviewable: a reviewer cannot hold 162 timed units in mind well enough for the approval to mean anything. Per-unit approval is the opposite failure.

**Rule: the visual plan is reviewed and approved against the Step 1 beat sheet's own act boundaries** — opening ladder, Act I, Act II, ending. That is roughly four review units, and it inherits a structure already approved at Gate E4B rather than inventing a new one for visuals.

A rejected act returns only that act, not the whole plan.

### 3. Look approval is provisional until motion-tested

Style frames cannot validate a motion format. A motion test can, but it needs a runtime, and Step 3 is deliberately tool-agnostic.

This repository already has the worked failure. EP006 reached an approved visual system, built ninety-second prototypes from it, and the prototypes were **rejected as creative answers**. Look approval that has not survived motion has already failed here once.

**Rule: Step 3 approves the look on style frames plus written motion intent, recorded as provisional. Step 4's motion test can return the look to Step 3.** The return path is explicit and expected rather than exceptional.

This keeps Step 3 tool-agnostic while admitting what a static frame cannot settle, instead of pretending the question is closed.
