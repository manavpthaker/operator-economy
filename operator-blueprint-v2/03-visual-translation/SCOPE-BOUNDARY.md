# Step 3 scope boundary

Status: **approved boundary**, 2026-09-01. Step 3 itself remains boundary-only until a full design pass is approved; this document fixes what that pass may cover.

Porting manifest: `PORTING-MANIFEST.md`

This document decides what Step 3 owns, what it consumes, what it hands on, and what it must never do. It exists before the standard and the gates deliberately, because Blueprint Cinema's own documentation sprawled across Steps 3 through 6 and that is the failure this boundary prevents.

## The one-line charter

Step 3 turns a locked episode into a **coherent visual language**: what the episode means visually, what world it happens in, what each moment of narration is doing, and how the whole thing should look and feel.

It does not draw shots, build scenes, source footage, or choose a runtime.

## Owns

| Artifact | What it decides |
|---|---|
| **Episode engine** | Operator, customer, owned value, constraint, counter-system, outcome object, primary visual mechanic, motion verbs. The mechanically honest model of what the business actually does |
| **Persistent world** | Stable objects, zones, paths, state transitions, evidence anchors, failure routes, money flows, human gates, camera anchors, object permanence |
| **Full-timeline visual plan** | Every timed unit against the word-level transcript: mode, camera anchor, motion verb, carried and focused objects, world state before and after, evidence attachment |
| **Direction bible** | Visual thesis, reality treatment, system treatment, proof treatment, typography, camera, motion, footage policy, sound, and negative rules |
| **Rhythm map** | Whole-episode energy, information density, visual mode, proof placement, human contact, sound, and transitions |
| **Look development** | Style frames proving the episode-specific visual language |
| **Shot-grammar selection** | Which causal grammars this episode uses and why. Not their application to specific shots |
| **Continuity and cognitive-load contracts** | The rules Step 4 must satisfy |

## Consumes, and may not change

From Step 2 at narration lock:

- final narration master and its hash
- **word-level transcript and intentional-pause map**
- narration duration

From Step 1 at editorial lock:

- Operator Canvas, Episode Investment Thesis, narrative spine, beat sheet, claims map
- the locked script and its `W` identity

**Step 3 may not rewrite the editorial argument, restate a claim beyond its approved wording, or estimate narration timing.** Timing comes from the Step 2 transcript. If Step 3 believes a claim needs different wording, it raises a change request to Step 1 rather than adapting it visually.

## Hands to Step 4

An approved engine, world, visual plan, direction bible, rhythm map, style frames and grammar selection, with hashes. Step 4 then produces sequence treatments, shot boards, scene directions, the motion test, the animatic and the asset plan.

## Does not own

| Not Step 3 | Where it lives |
|---|---|
| Sequence treatments, shot boards, scene directions | Step 4 |
| Representative motion test and directed animatic | Step 4 |
| Asset tickets, candidates, selects, rights and provenance | Step 5 |
| Conform, picture lock, colour, Fusion, mix, captions, delivery | Step 6 |
| **Runtime and toolchain choice** | Steps 4-6 |

## Proposed amendment to the V2 lifecycle

The V2 README currently lists **persistent world** under Step 4 preproduction. That ordering cannot hold, because a direction bible describes how a world looks and feels and therefore requires the world to exist first.

`blueprint-cinema/WORKFLOW.md` orders it engine, then world, then visual plan, then direction bible. EP006 validated that order in practice with an approved engine, an approved world and a 162-unit visual plan.

**Approved by the owner 2026-09-01 and applied.** `persistent world` moved from the Step 4 lifecycle line to Step 3. Step 4 is restated as sequence treatments, shot boards, scene direction, motion test, animatic and asset plan.

The V2 README lifecycle table now reflects this. Blueprint Cinema's production order is therefore the order V2 follows: engine, world, visual plan, direction bible, rhythm map, look development, then Step 4.

## Why Step 3 is tool-agnostic

Recorded here because it is a boundary decision, not an implementation preference.

Blueprint Cinema names HyperFrames canonical for motion and Resolve canonical for finishing. Step 3 does not adopt that and does not depend on it.

The Remotion deauthorization took an approved 162-unit visual plan out of production with it, because the plan was coupled to a runtime that was later withdrawn. A direction layer that survives a runtime change is worth more than one optimised for a runtime that is currently installed nowhere and appears in zero code files.

Step 3 therefore produces direction any runtime could execute. Steps 4 through 6 own the runtime.

## Dependency that gates any real Step 3 run

**Step 3 consumes the word-level transcript, which Step 2 produces at N6.**

EP007 has passed N1 and captured N4B, but N5, N6 and N7 remain open, so no word-level transcript exists yet. Step 3 can therefore be designed and fixture-tested now, but cannot run on a real episode until Step 2 closes for that episode.

This mirrors how Steps 1 and 2 were built, and is recorded so it is a planned sequence rather than a late discovery.

## Resolved design questions

### 1. The episode engine is derived, not authored

Owner direction, 2026-09-01: *the episode engine is just nomenclature. Whatever has been built out already can build the engine and Step 3 can build the visual model on top of that.*

Checked against EP006's approved engine. Its ten substantive fields split cleanly:

| Engine field | Source | Step 3 treatment |
|---|---|---|
| `operator` | Canvas §1 | **derived** |
| `input_customer`, `eligible_return_customer` | Canvas §2 | **derived** |
| `constraint` | Canvas §3 | **derived** |
| `counter_system` | Canvas §4 and §6 | **derived** |
| `owned_value`, `outcome_object` | Canvas §5 | **derived** |
| `visual_mechanic` | — | **authored by Step 3** |
| `motion_verbs` | — | **authored by Step 3** |
| `reality_world` | — | **authored by Step 3** |
| `guardrails` | — | **authored by Step 3** |

Six of ten fields restate decisions Step 1 already locked. Only four are visual.

**Rule: Step 3 derives the business fields from the locked Canvas and may not re-decide them.** Divergence between the engine and the Canvas is drift, and a Step 3 gate must fail on it rather than tolerate a second description of the same business. Step 3 authors only the visual mechanic, the motion vocabulary, the reality-world bible, and the guardrails.

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
