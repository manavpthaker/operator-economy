# Step 3 Visual Translation Standard

Status: **proposed v0.2**; not authority. Step 3 remains boundary-only until this standard, its gates, and its acceptance set are approved.

Scope boundary: `SCOPE-BOUNDARY.md` (approved 2026-09-01)

Porting manifest: `PORTING-MANIFEST.md`

Semantic authority: the hash-pinned Boundary Ledger 2.0 `semantic-core.json` and
`bindings/motion.json`. Structural references: `blueprint-cinema/references/DIRECTION-SYSTEM.md`
artifacts 1 to 3 and the causal relationships in `SHOT-GRAMMAR.md`.

## What Step 3 is for

Step 3 answers one question: **what should the viewer be looking at, and why that.**

It receives an episode whose words are locked and whose narration is timed, and produces a visual language complete enough that Step 4 can direct shots from it without re-deciding what the episode means.

It is a **directing** layer. It is not a screenplay, not an image-prompt list, and not a runtime.

## The five failures this standard exists to prevent

Each is drawn from something that actually happened in this repository, not from theory.

1. **Screen-by-screen coverage.** Assigning a visual to each narration line produces an animated deck. EP006's approved coverage map was invalidated for exactly this and its rubric passed it at 21/23, which is why a passing score against a bad rubric is not evidence.
2. **Direction that cannot survive motion.** EP006 reached an approved visual system, built ninety-second prototypes from it, and the prototypes were rejected as creative answers. Static approval is provisional here by rule.
3. **Runtime coupling.** The Remotion deauthorization took an approved 162-unit visual plan out of production with it. Step 3 names no runtime.
4. **A second description of the business.** If Step 3 restates the operator, buyer or offer in its own words, Step 1 and Step 3 drift apart silently. The engine's business fields are therefore derived and checkable, never authored.
5. **A second brand motion language.** If Step 3 invents motion verbs, metaphors, or scene
   primitives, Boundary Ledger stops being cross-media authority and every episode can drift. Step 3
   derives the business operation, selects a valid Boundary Ledger operation, and leaves
   implementation primitives to Step 4.

## Required artifacts

Step 3 produces six. Each material field is `DERIVED` from an upstream lock, `SELECTED` from a
hash-pinned external authority, `AUTHORED` by Step 3, or `UNKNOWN`.

### 1. Episode engine

The mechanically honest model of what the business does, bound to Boundary Ledger without creating
a second semantic vocabulary.

**Business fields are `DERIVED` from the locked Operator Canvas and may not be re-decided:**

| Field | Canvas source |
|---|---|
| operator | §1 Operator |
| customer, and any distinct beneficiary | §2 Buyer and beneficiary |
| constraint | §3 Costly problem |
| counter-system | §4 Offer and §6 Delivery system |
| owned value | §5 Buyer result |
| outcome object | §5 Buyer result |

**Business-operation fields are `DERIVED` from locked upstream state:**

- Exact upstream artifact path, hash, and section or field locator.
- `state_before` and `state_after`, preserving the upstream meaning.
- `business_operation`: a plain-language description of what changes in the business. It is not a
  branded motion name and may not widen the upstream state.

**Semantic bindings are `SELECTED`, not authored:**

- Boundary Ledger system version, semantic-core path and SHA-256, and motion-binding path, status,
  and SHA-256.
- `boundary_ledger_semantic_role_id`, selected from the pinned core.
- `boundary_ledger_operation_id`, selected from the pinned core and permitted for that role by the
  pinned motion binding.
- A mapping rationale showing why the selected operation's required state change matches the
  derived business operation.

The permitted operation IDs are read from the pinned core at validation time. They are not copied
into an episode-local editable vocabulary.

**Episode-direction fields are `AUTHORED` by Step 3:**

- **Episode visual model.** The mechanically honest episode-specific abstraction—persistent actors,
  zones, relationships, and approved business-operation IDs—that the persistent world expands. It
  may not rename Boundary Ledger operations or prescribe implementation primitives.
- **Reality-world visual bible.** The people, places, objects and surfaces this episode's reality layer draws from.
- **Guardrails.** What this engine must never be made to imply.

A Step 3 gate fails when a derived field diverges from upstream; either design-system hash is
stale; a selected role or operation is unknown; the role-operation pair is disallowed by the pinned
binding; or the engine introduces a local motion vocabulary or implementation primitive.

### 2. Persistent world

Stable objects that keep their identity while their state changes.

Required: objects with IDs and material forms; zones; paths; allowed state transitions; evidence anchors bound to claim IDs; failure routes; money flows; human judgement gates; camera anchors; and the engine operation-binding IDs that may act on each object.

**Object permanence is the governing rule.** A customer, a tool, a value or a piece of evidence stays recognisable across the episode while the relevant state changes around it. An object that changes appearance to suit a shot has broken the world.

### 3. Full-timeline visual plan

Every timed unit of narration mapped to what the viewer sees.

Timing comes from the **Step 2 word-level transcript**. Step 3 may not estimate it.

Each unit records: `in`/`out` bound to word indices; mode (reality, system, proof, outcome,
identity); camera anchor; engine `business_operation_id`; selected
`boundary_ledger_operation_id`; objects carried and focused; **world state before and after**;
attached evidence with its claim ID; and its narrative state.

A unit whose `world_state_before` equals its `world_state_after` and which carries no evidence is doing nothing, and must be justified or merged.

**Approved per act**, against the Step 1 beat sheet's own boundaries. A rejected act returns only that act.

### 4. Direction bible

How the episode looks and feels, and what it refuses.

Required fields, ported from the direction system:

- **Visual thesis** — one sentence a builder can direct from.
- **Emotional progression** — opening tension, curiosity, recognition, proof and trust, construction and agency, friction or risk, resolution, practical confidence.
- **Mode treatments** — separate direction for reality, system, proof, outcome and identity. Each names its own camera, light, texture, movement and labelling behaviour.
- **Persistent motifs** — per world object: material form, Boundary Ledger semantic role, allowed
  states, meaning, first appearance, evolution, final resolution, and prohibited metaphorical use.
- **Screen-direction rules** — how the selected operations preserve spatial continuity, held consistently.
- **Composition, camera, transition and typography direction.**
- **Boundary Ledger operation application** — how each selected operation acts on this episode's
  persistent objects while preserving its core meaning and the motion-binding rules. This is
  episode application, not a new motion grammar.
- **Surface, texture, colour and light**, with semantic meaning resolved through the applicable
  Boundary Ledger binding rather than reassigned by the episode.
- **Documentary footage doctrine** and **AI plate doctrine.**
- **Sound intent** — episode-specific use of silence and semantic events, without defining a
  replacement Boundary Ledger sound vocabulary or implementation primitive.
- **Negative list** — the specific things this episode will not do.

### 5. Rhythm map

The whole episode as a shape: energy, information density, visual mode, proof placement, human contact, sound and transition, across its full duration.

Its job is to catch what no single beat reveals — three dense system sequences in a row, ten minutes without a human face, proof clustered in one act.

### 6. Look development

Style frames proving the episode-specific visual language, covering at minimum: reality, system explanation, evidence, recurring-object continuity, a meaningful transition, identity, failure or reversal, and measurable outcome.

**Look approval is provisional.** Style frames cannot validate a motion format. Step 4's motion test can return the look to Step 3, and that return is expected rather than exceptional.

## Governing rules

**Motion expresses a derived business operation through Boundary Ledger.** Every meaningful change
must trace `upstream state -> business_operation -> boundary_ledger_operation_id -> plan unit`, with
a readable before state, operation, after state, and settle. Motion that exists to keep the frame
alive is decoration and fails review.

**The default transition is a cut.** Preserve continuity only when it explains a relationship:
reality resolving into a system model, evidence pinning to an accountable object, a sourced value
changing system behaviour, work persisting through a handoff, a connection failing, or accumulated
state being revealed. Wipes, transition packs, repeated elastic motion and decorative dissolves are
prohibited.

**Text labels, it does not narrate.** Typography names components and parameters. It does not reproduce the narration. Kinetic type is reserved for a genuine thesis, reversal or warning.

**AI renders are never evidence.** Generated plates establish environment. Text, interfaces, prices, documents and brand marks are composited afterwards from real sources.

**Every visual inherits its evidence label.** A polished diagram cannot resolve an `UNKNOWN`, upgrade a parallel into observed demand, or imply a capability the entry offer does not have.

**The audio-only rule.** Visuals may carry citations, secondary arithmetic, comparison detail and repeated labels. They may not be the only place the buyer, problem, company, first offer, human responsibility, economics boundary, principal risk or first action is explained.

## What Step 3 may not do

- Rewrite the editorial argument or restate a claim beyond its approved wording. A wording problem is a **change request to Step 1**, not a visual adaptation.
- Estimate narration timing. Timing is the Step 2 transcript's.
- Re-decide any derived engine field.
- Author a local motion verb, rename a Boundary Ledger operation, widen its required state change,
  or use a role-operation pair the pinned motion binding does not permit.
- Define animation components, scene primitives, easing presets, renderer constructs, or other
  implementation vocabulary. Those are Step 4 through Step 6 decisions.
- Name a runtime, or shape direction around one.
- Draw shots, write scene directions, build an animatic, or plan assets. Those are Step 4.

## Resolved by the gate design pass

**The rhythm map is approved with the direction bible, as a separate decision inside one gate.** It cannot precede the visual plan, because it describes the shape of the episode that exists rather than the one intended. V5 therefore records V5a and V5b independently, and a clean finding in one cannot stand for the other.

**Look development requires a named reference stack, with an explicit non-imitation ruling.** Naming references is what makes direction communicable to a builder. The guard is that references inform treatment, not brand semantics or implementation vocabulary, and no frame reproduces a named work's distinctive composition, palette or identity. That ruling is a V6 pass condition rather than a note.

**An act-level rejection that names a bible defect escalates to V5.** The direction bible is upstream authority for *how*; the visual plan is downstream for *what and when*. If the rejection is about treatment, the act is revised in place. If it reveals the bible cannot express the episode's actual mechanics, the bible is revised first and the act is re-reviewed after.
