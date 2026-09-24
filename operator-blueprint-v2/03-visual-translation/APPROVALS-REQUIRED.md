# Step 3 approvals in plain English

Status: **guide only**. This file explains the approvals in `STAGE-GATES.md`; it does not add a
gate, record a decision, or replace the governing standard.

## The two kinds of approval

1. **Process approval** answers: “Are these the rules Step 3 will use?” It applies once to an exact
   version of the Step 3 standard, gates, templates, validator, and acceptance evidence.
2. **Episode approval** answers: “Did this episode satisfy those rules?” It is repeated for every
   episode and is always bound to exact artifact hashes.

A process approval is not episode approval. An episode approval made while the process is still
proposed does not automatically become a gate pass unless the process-approval record explicitly
says it activates that exact pre-reviewed artifact and hash.

## Approval needed before Step 3 becomes authority

### Step 3 v0.3 process approval

In plain English, the approver is confirming:

- These are the governing rules for turning locked narration into visual direction.
- Boundary Ledger supplies the semantic roles and operations; an episode may not invent its own.
- Machines check structure, hashes, provenance, and consistency. People still judge whether the
  translation is truthful, understandable, and worth making.
- The listed templates and acceptance controls are part of the same versioned process.
- Approving the process does not approve an episode, authorize Step 4, or approve publication.

The approval record must name:

- the process version;
- the exact hashes of the standard, gates, templates, validator, and acceptance record;
- the approver and date;
- any accepted limitation or unresolved question;
- whether any pre-authority episode reviews are activated or must be repeated, naming each artifact
  and hash individually.

Suggested approval statement:

> I approve Step 3 v0.3 as the governing visual-translation process, against the hashes recorded in
> this approval. This approves the process only. It does not by itself approve an episode, authorize
> Step 4, or approve publication. The record separately states whether any pre-authority episode
> review becomes effective.

## Approvals required for each episode

```text
V1 input lock
  -> V2 episode engine
  -> V3 persistent world
  -> V4 visual plan, approved one act at a time
  -> V5a direction bible + V5b rhythm map, approved separately
  -> V6 look, approved provisionally
  -> V7 final Step 3 lock and authorization for Step 4
```

### V1 — lock the inputs

**Plain question:** Are we using the final editorial material, final narration, final timing, and
current Boundary Ledger files?

This is a technical pass, not a taste decision. Every required path and hash must match. A stale or
partial input blocks the episode before visual interpretation begins.

**Does not approve:** the engine, the visual world, or any creative direction.

### V2 — approve the episode engine

**Plain question:** Is this a truthful model of the business described upstream, without invented
claims or a new episode-specific motion language?

The machine confirms provenance and valid Boundary Ledger bindings. The named human approver judges
whether the derived states actually preserve the source meaning and whether the authored
establishment reveals the right people and relationship without pretending to change the business.

**Approval must name:** the exact engine hash, approver, date, and any disclosed judgment call.

**Does not approve:** specific scenes, imagery, pacing, or Step 4.

### V3 — approve the persistent world

**Plain question:** Do the same people, objects, paths, evidence, and boundaries remain recognisable
while their states change?

The approver is accepting the object identities, allowed transitions, evidence attachments, failure
routes, money relationships, human decisions, and camera jobs. Evidence must retain its upstream
qualification and must not become stronger because of the visual treatment.

**Approval must name:** the exact world hash, bound engine hash, approver, date, and any disclosed
judgment call.

**Does not approve:** the full episode sequence or Step 4.

### V4 — approve the complete visual plan, one act at a time

**Plain question:** For this act, does every part of the locked narration have the right visual job,
with no unexplained gap, filler, or false implication?

The opening ladder, Act I, Act II, and ending each receive their own named approval. Rejecting one act
returns that act rather than silently approving the whole timeline.

**Approval must name:** the act, exact plan hash, approver, and date.

**Does not approve:** the direction bible, overall rhythm, final look, or Step 4.

### V5a — approve the direction bible

**Plain question:** Could a director or builder make coherent scenes from these instructions without
having to reinterpret the episode?

This approves the visual thesis, emotional progression, mode treatments, motifs, spatial rules,
typography behavior, evidence treatment, sound intent, and negative rules.

**Approval must name:** the exact direction-bible hash, approver, and date.

### V5b — approve the rhythm map

**Plain question:** Does the whole episode have the right movement, density, proof placement, human
contact, and variation when viewed across its full duration?

This is separate from V5a. A usable direction bible does not prove the episode has good rhythm, and
good rhythm does not prove the direction is complete.

**Approval must name:** the exact rhythm-map hash, the visual-plan hash it describes, approver, and
date.

**V5a and V5b do not approve:** the final look or Step 4.

### V6 — approve the look provisionally

**Plain question:** Is this episode-specific visual language worth testing in motion?

The approval covers representative style frames and their written motion intent. It is provisional
because still images cannot prove that motion works. Step 4's motion test may return the look.

**Approval must name:** the exact look-development hash, approver, date, and the Step 4 return path.

**Does not approve:** final motion, final assets, or publication.

### V7 — approve the Step 3 lock and authorize Step 4

**Plain question:** Is the entire visual-translation package consistent, complete, traceable, and
ready for someone to direct from without changing its meaning?

This is the only Step 3 approval that authorizes Step 4. It confirms that all earlier gates passed,
their hashes still match, the artifacts agree with one another, no load-bearing idea exists only in
the visuals, and no current blocker remains.

**Approval must name:** the visual-translation lock hash, approver, and date.

**Does not approve:** the Step 4 motion test, animatic, final assets, finished edit, release, or
publication. Those remain later decisions.

## What is not an approval

- A validator pass proves only the mechanical checks it actually ran.
- A fixture pass proves test behavior, not an episode.
- Creating an approval file does not approve its contents.
- A verbal preference without an artifact hash does not survive a later change.
- A Git commit preserves a decision; it does not create one.
- Approval of a still frame does not prove motion.
- Approval of Step 3 does not approve release or publication.

## Minimum approval record

Every human approval should be recorded in this form:

```text
Decision: approve / return / reject
Artifact and SHA-256:
Process or gate version:
Scope of this decision:
Known limitations accepted:
What this does not authorize:
Approved by:
Approved on:
```

If the named artifact changes, the approval no longer applies unless the governing invalidation
rules explicitly say otherwise and that ruling is recorded.

## Commit boundary

After an approval is recorded, commit the approved artifacts and the approval record together so
other jobs can see the same state. The commit should exclude unrelated dirty work. Committing before
approval freezes a candidate; committing after approval preserves the decision. Neither order turns
a commit into approval.
