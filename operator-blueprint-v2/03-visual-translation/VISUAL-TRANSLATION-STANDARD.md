# Step 3 Visual Translation Standard

Status: **proposed v0.1**; not authority. Step 3 remains boundary-only until this standard, its gates, and its acceptance set are approved.

Scope boundary: `SCOPE-BOUNDARY.md` (approved 2026-09-01)

Porting manifest: `PORTING-MANIFEST.md`

Primary port: `blueprint-cinema/references/DIRECTION-SYSTEM.md` artifacts 1 to 3, and the causal grammars in `SHOT-GRAMMAR.md`.

## What Step 3 is for

Step 3 answers one question: **what should the viewer be looking at, and why that.**

It receives an episode whose words are locked and whose narration is timed, and produces a visual language complete enough that Step 4 can direct shots from it without re-deciding what the episode means.

It is a **directing** layer. It is not a screenplay, not an image-prompt list, and not a runtime.

## The four failures this standard exists to prevent

Each is drawn from something that actually happened in this repository, not from theory.

1. **Screen-by-screen coverage.** Assigning a visual to each narration line produces an animated deck. EP006's approved coverage map was invalidated for exactly this and its rubric passed it at 21/23, which is why a passing score against a bad rubric is not evidence.
2. **Direction that cannot survive motion.** EP006 reached an approved visual system, built ninety-second prototypes from it, and the prototypes were rejected as creative answers. Static approval is provisional here by rule.
3. **Runtime coupling.** The Remotion deauthorization took an approved 162-unit visual plan out of production with it. Step 3 names no runtime.
4. **A second description of the business.** If Step 3 restates the operator, buyer or offer in its own words, Step 1 and Step 3 drift apart silently. The engine's business fields are therefore derived and checkable, never authored.

## Required artifacts

Step 3 produces six. Each has an evidence label on every material field: `DERIVED` from an upstream lock, `AUTHORED` by Step 3, or `UNKNOWN`.

### 1. Episode engine

The mechanically honest model of what the business does, expressed so it can be moved.

**Business fields are `DERIVED` from the locked Operator Canvas and may not be re-decided:**

| Field | Canvas source |
|---|---|
| operator | §1 Operator |
| customer, and any distinct beneficiary | §2 Buyer and beneficiary |
| constraint | §3 Costly problem |
| counter-system | §4 Offer and §6 Delivery system |
| owned value | §5 Buyer result |
| outcome object | §5 Buyer result |

**Visual fields are `AUTHORED` by Step 3:**

- **Primary visual mechanic.** How the business behaves as a moving thing. It must be mechanically honest: use a leak and recovery loop, a queue, an assembly line, a routing network, a toll gate, a capacity system or a feedback loop **only if the business actually behaves that way.** A flywheel, a gravity field or a compounding effect are prohibited unless the economics genuinely compound.
- **Primary motion verbs.** The three to six business verbs this episode's motion expresses: capture, route, qualify, compare, assign, approve, reject, retry, escalate, hand off, price, deliver, recover, retain, measure.
- **Reality-world visual bible.** The people, places, objects and surfaces this episode's reality layer draws from.
- **Guardrails.** What this engine must never be made to depict.

A Step 3 gate fails when any derived field diverges from the Canvas.

### 2. Persistent world

Stable objects that keep their identity while their state changes.

Required: objects with IDs and material forms; zones; paths; allowed state transitions; evidence anchors bound to claim IDs; failure routes; money flows; human judgement gates; camera anchors.

**Object permanence is the governing rule.** A customer, a tool, a value or a piece of evidence stays recognisable across the episode while the relevant state changes around it. An object that changes appearance to suit a shot has broken the world.

### 3. Full-timeline visual plan

Every timed unit of narration mapped to what the viewer sees.

Timing comes from the **Step 2 word-level transcript**. Step 3 may not estimate it.

Each unit records: `in`/`out` bound to word indices; mode (reality, system, proof, outcome, identity); camera anchor; motion verb; objects carried and focused; **world state before and after**; attached evidence with its claim ID; and its narrative state.

A unit whose `world_state_before` equals its `world_state_after` and which carries no evidence is doing nothing, and must be justified or merged.

**Approved per act**, against the Step 1 beat sheet's own boundaries. A rejected act returns only that act.

### 4. Direction bible

How the episode looks and feels, and what it refuses.

Required fields, ported from the direction system:

- **Visual thesis** — one sentence a builder can direct from.
- **Emotional progression** — opening tension, curiosity, recognition, proof and trust, construction and agency, friction or risk, resolution, practical confidence.
- **Mode treatments** — separate direction for reality, system, proof, outcome and identity. Each names its own camera, light, texture, movement and labelling behaviour.
- **Persistent motifs** — per world object: material form, colour and contrast role, allowed states, meaning, first appearance, evolution, final resolution, and prohibited metaphorical use.
- **Screen-direction rules** — what progress, reversal, failure, return and escalation look like directionally, held consistently.
- **Composition, camera, motion, transition and typography grammars.**
- **Surface, texture, colour and light.**
- **Documentary footage doctrine** and **AI plate doctrine.**
- **Sound identity.**
- **Negative list** — the specific things this episode will not do.

### 5. Rhythm map

The whole episode as a shape: energy, information density, visual mode, proof placement, human contact, sound and transition, across its full duration.

Its job is to catch what no single beat reveals — three dense system sequences in a row, ten minutes without a human face, proof clustered in one act.

### 6. Look development

Style frames proving the episode-specific visual language, covering at minimum: reality, system explanation, evidence, recurring-object continuity, a meaningful transition, identity, failure or reversal, and measurable outcome.

**Look approval is provisional.** Style frames cannot validate a motion format. Step 4's motion test can return the look to Step 3, and that return is expected rather than exceptional.

## Governing rules

**Motion expresses a business verb.** Every meaningful animation has a readable before state, an operation, and an after state. Motion that exists to keep the frame alive is decoration and fails review.

**The default transition is a cut.** Design a transition only when it explains a relationship: reality resolving into system geometry, evidence pinning to a node, a sourced value changing system behaviour, the camera following work through a handoff, a connection failing, or the accumulated system being revealed. Wipes, transition packs, repeated elastic motion and decorative dissolves are prohibited.

**Text labels, it does not narrate.** Typography names components and parameters. It does not reproduce the narration. Kinetic type is reserved for a genuine thesis, reversal or warning.

**AI renders are never evidence.** Generated plates establish environment. Text, interfaces, prices, documents and brand marks are composited afterwards from real sources.

**Every visual inherits its evidence label.** A polished diagram cannot resolve an `UNKNOWN`, upgrade a parallel into observed demand, or imply a capability the entry offer does not have.

**The audio-only rule.** Visuals may carry citations, secondary arithmetic, comparison detail and repeated labels. They may not be the only place the buyer, problem, company, first offer, human responsibility, economics boundary, principal risk or first action is explained.

## What Step 3 may not do

- Rewrite the editorial argument or restate a claim beyond its approved wording. A wording problem is a **change request to Step 1**, not a visual adaptation.
- Estimate narration timing. Timing is the Step 2 transcript's.
- Re-decide any derived engine field.
- Name a runtime, or shape direction around one.
- Draw shots, write scene directions, build an animatic, or plan assets. Those are Step 4.

## Resolved by the gate design pass

**The rhythm map is approved with the direction bible, as a separate decision inside one gate.** It cannot precede the visual plan, because it describes the shape of the episode that exists rather than the one intended. V5 therefore records V5a and V5b independently, and a clean finding in one cannot stand for the other.

**Look development requires a named reference stack, with an explicit non-imitation ruling.** Naming references is what makes direction communicable to a builder. The guard is that references inform vocabulary and no frame reproduces a named work's distinctive composition, palette or identity. That ruling is a V6 pass condition rather than a note.

**An act-level rejection that names a bible defect escalates to V5.** The direction bible is upstream authority for *how*; the visual plan is downstream for *what and when*. If the rejection is about treatment, the act is revised in place. If it reveals the bible cannot express the episode's actual mechanics, the bible is revised first and the act is re-reviewed after.
