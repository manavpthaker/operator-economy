# Step 3 Stage Gates

Status: **proposed v0.2**; test before approval. Step 3 remains boundary-only.

Standard: `VISUAL-TRANSLATION-STANDARD.md`

Scope boundary: `SCOPE-BOUNDARY.md` (approved 2026-09-01)

Each gate is a real decision. Creating a file does not pass a gate. A polished artifact does not pass a gate.

## States

`not_started` → `in_progress` → `passed` / `failed` / `invalidated`

Gates run in order. A later gate may not be attempted while an earlier one is `failed` or `invalidated`.

## Fixture mode

A fixture may exercise any gate's behaviour without advancing an episode. Record the real production result and the simulated test result separately. A fixture pass proves only the behaviour tested. Do not create an episode workspace, assign visual approval to a real episode, or authorize Step 4 from a fixture.

---

## Gate V1: input lock

**Decision:** Are the upstream locks current, complete, and hash-verified?

Pass only when:

- Step 1 has a current editorial lock with `Gate E6: PASSED`, and every artifact hash it records matches on disk.
- Step 2 has a current **narration lock** at N7, with a `technical_pass` and an explicit `creative_approved` naming the same master hash.
- The **word-level transcript and intentional-pause map** exist and are bound to that exact master hash and duration.
- The locked script `W` identity reproduces its recorded token count and SHA-256.
- The Operator Canvas, Episode Investment Thesis, narrative spine, beat sheet and claims map are present and current.
- Boundary Ledger's `semantic-core.json` and `bindings/motion.json` exist, their recorded versions
  and SHA-256 values match on disk, and the motion binding resolves the same semantic-core version.
- No open change request exists against Step 1 or Step 2.

An editorial or narration failure returns the package upstream. A Boundary Ledger mismatch blocks
locally until compatibility is reviewed. **Step 3 repairs neither and does not proceed on a partial
or stale lock.**

Recorded: every input path and hash, including the Boundary Ledger semantic core and motion binding,
forming the freeze this step's later gates check against.

---

## Gate V2: episode engine approved

**Decision:** Is this a mechanically honest derivation of the business, correctly bound to Boundary Ledger?

Pass only when:

- Every **derived** field matches the locked Operator Canvas: operator, customer and any distinct beneficiary, constraint, counter-system, owned value, outcome object. **Divergence fails the gate.** Step 3 may not re-decide a business field, and a disagreement is a change request to Step 1.
- Every material state change records its exact upstream artifact, hash, locator, `state_before`, and
  `state_after`; its plain-language `business_operation` preserves that locked meaning. Divergence
  or an untraceable operation fails.
- Every selected semantic role exists in the hash-pinned Boundary Ledger core.
- Every `boundary_ledger_operation_id` exists in that core and is permitted for the selected role by
  the hash-pinned motion binding.
- The mapping rationale matches the operation's canonical `requiredStateChange`; a branded label
  cannot substitute for a business-state derivation.
- The **episode visual model** names persistent actors, zones, relationships, and every approved
  business-operation ID; its mechanical-honesty statement matches the derived business state.
- The **reality-world visual bible** names the people, places, objects and surfaces the reality layer draws from.
- **Guardrails** state what this engine must never be made to depict.
- No episode-local motion vocabulary, renamed operation, or implementation primitive appears.
- Every material field carries `DERIVED`, `SELECTED`, `AUTHORED` or `UNKNOWN`.
- Named human approval.

Failure returns to the engine, or to Step 1 as a bounded change request when the defect is an
upstream business-state disagreement. A missing Boundary Ledger operation is a design-system blocker;
Step 3 may not mint a temporary substitute.

---

## Gate V3: persistent world approved

**Decision:** Do objects keep their identity while their state changes?

Pass only when:

- Objects have stable IDs and material forms; zones, paths and allowed state transitions are defined.
- **Object permanence holds.** A customer, tool, value or evidence item stays recognisable across the episode while the relevant state changes around it. An object that changes appearance to suit a shot fails.
- Evidence anchors are bound to **claim IDs from the Step 1 claims map**, and every anchored claim exists there with matching wording authority.
- Failure routes, money flows and human judgement gates are represented.
- Camera anchors are defined and each is assigned a job.
- Every object an engine operation binding acts on exists in the world. Every world object is
  reachable by at least one engine operation-binding ID, or is explicitly marked static.
- Named human approval.

Failure returns to the world, or to the engine when the world cannot express the derived operations.

---

## Gate V4: full-timeline visual plan approved

**Decision:** Does every moment of narration have a reason to be seen, and does the episode move?

**Reviewed and approved per act**, against the Step 1 beat sheet's own boundaries: opening ladder, Act I, Act II, ending. A rejected act returns only that act.

Pass only when, for the act under review:

- Every unit's `in` and `out` are bound to **word indices from the Step 2 transcript**. Step 3 may not estimate timing, and an estimated duration fails.
- The act's units cover its narration continuously, with no unexplained gap and no overlap.
- Each unit records mode, camera anchor, engine `business_operation_id`, matching
  `boundary_ledger_operation_id`, carried and focused objects, world state before and after,
  attached evidence with its claim ID, and narrative state.
- **No unit is inert.** A unit whose `world_state_before` equals its `world_state_after` and which carries no evidence is doing nothing. It must be justified in writing or merged into its neighbour.
- Every object and business-operation binding referenced exists in the approved world and engine;
  the unit's Boundary Ledger operation ID matches the engine binding.
- Every attached evidence item carries its upstream evidence label. **A visual may not upgrade a label.**
- Mode distribution is deliberate rather than incidental, and the act does not consist of one mode.
- Named human approval for that act.

Failure returns the act. **If the rejection names a defect in the direction bible rather than in the act, it escalates to V5** and the bible is revised before the act is re-reviewed.

---

## Gate V5: direction bible and rhythm map approved

**Decision:** Can a builder direct from this, and does the whole episode hold as a shape?

This gate records **two separate decisions**. A clean finding in one cannot stand for the other.

### V5a — direction bible

Pass only when:

- A **visual thesis** exists in one sentence a builder can direct from.
- **Emotional progression** is mapped across the episode.
- **Mode treatments** give separate direction for reality, system, proof, outcome and identity, each naming its own camera, light, texture, movement and labelling behaviour.
- **Persistent motifs** are recorded per world object, including prohibited metaphorical use.
- **Screen-direction rules** define how selected Boundary Ledger operations preserve spatial continuity and hold consistently.
- Composition, camera, transition and typography direction are defined.
- **Boundary Ledger operation application** is defined for every selected engine operation: the
  persistent object, stable context, before state, canonical operation, after state, and settle are
  legible. Step 3 does not create new motion names or implementation primitives.
- **The default transition is a cut.** Every designed transition names the relationship it explains. Wipes, transition packs, repeated elastic motion and decorative dissolves fail.
- **Typography labels rather than narrates.** Kinetic type is reserved for a genuine thesis, reversal or warning.
- Documentary footage doctrine and **AI plate doctrine** are stated. AI renders are never evidence.
- Sound intent references Boundary Ledger semantic roles without defining a replacement sound vocabulary.
- A **negative list** states what this episode will not do.

### V5b — rhythm map

Pass only when:

- Energy, information density, visual mode, proof placement, human contact, sound and transition are mapped across the **full duration**, not per beat.
- The map is built from the **approved visual plan**, so it describes the episode that exists rather than an intention.
- Whole-episode checks are run and their findings dispositioned: consecutive dense system sequences, long stretches without human contact, proof clustered into one act, mode monotony, and transition repetition.
- Any finding is accepted, modified, rejected or preserved with a reason. **A finding may not be left unresolved.**

Failure returns to the bible, the rhythm map, or the visual plan, depending on which the finding names.

---

## Gate V6: look development approved, provisionally

**Decision:** Does the episode-specific visual language exist as something you can look at?

Pass only when:

- Style frames cover at minimum: reality, system explanation, evidence, recurring-object continuity, a meaningful transition, identity, failure or reversal, and measurable outcome.
- Each frame is traceable to the direction bible's mode treatments and motifs.
- Frames use the episode's **real text and truthful placeholder geometry**. A frame containing invented data, an invented interface or an unattributed figure fails.
- A **reference stack** is named, with an explicit non-imitation ruling: references inform treatment,
  not brand semantics or implementation vocabulary, and no frame reproduces a named work's
  distinctive composition, palette or identity.
- Written **motion intent** accompanies the frames, because a still cannot carry it.
- Every motion intent names an approved engine `business_operation_id` and its matching Boundary
  Ledger operation ID. An authored motion label or renderer primitive fails.

**This approval is provisional by rule.** Style frames cannot validate a motion format. Step 4's motion test may return the look to Step 3, and that return is expected rather than exceptional. Recording a look as finally approved at V6 is itself a defect.

---

## Gate V7: visual translation lock and Step 4 handoff

**Decision:** Is this the visual language Step 4 is authorized to direct from?

Pass only when:

- V1 through V6 are `passed` and every recorded hash matches.
- Every act of the visual plan is approved.
- Engine, world, plan, bible, rhythm map and look are mutually consistent: every operation binding,
  object, mode, motif and evidence anchor referenced in one exists in the others.
- The Boundary Ledger semantic-core and motion-binding versions and hashes still match the V1 lock.
- Every operation trace is intact from upstream state through engine binding, plan unit, direction,
  and look intent; no artifact authors a replacement motion vocabulary or implementation primitive.
- The **audio-only rule** holds: no load-bearing element of buyer, problem, company, first offer, human responsibility, economics boundary, principal risk or first action exists only in a visual.
- **No runtime is named anywhere in the locked artifacts.** Toolchain choice belongs to Steps 4 through 6.
- Every `UNKNOWN` is classified as a Step 4 test question, a later-stage blocker, or a current lock blocker. A current lock blocker fails the gate.
- The look is recorded as **provisional**, with the Step 4 return path stated.
- Named human approval, and the visual-translation lock hash.

After this gate, Step 4 may direct shots. Step 4 may not re-decide the engine, the world, the plan's
timing, the selected Boundary Ledger semantics, or the episode's meaning.

---

## Amendment and invalidation rules

- A **new Step 1 editorial lock** invalidates every Step 3 artifact.
- A **new Step 2 narration lock, or any change to the narration master** invalidates the visual plan and the rhythm map, because both are bound to word-level timing. Engine, world and bible survive if no meaning changed, and that must be written down rather than assumed.
- A **new Boundary Ledger semantic-core or motion-binding hash** invalidates V1 through V7 until a
  compatibility ruling is recorded. An unchanged operation ID is not assumed semantically unchanged.
- A **changed engine** invalidates the world, plan, bible and rhythm map.
- A **changed world** invalidates the plan and the rhythm map.
- A **changed direction bible** invalidates look development, and invalidates any act of the plan whose direction depended on the changed field.
- A **changed act of the visual plan** invalidates the rhythm map, which describes the whole.
- A **look returned by Step 4's motion test** invalidates V6 only, unless the return names a bible defect, in which case V5a is invalidated too.
- Visual-production pressure never authorizes a Step 3 exception. If Step 4 cannot build what Step 3 approved, that is a Step 3 defect and returns here.

## Decision-state rule

A structural or completeness pass is a technical state. It cannot imply that the visual language is any good. Approval of an artifact's completeness and approval of its creative direction are separate decisions, and neither implies the other.
