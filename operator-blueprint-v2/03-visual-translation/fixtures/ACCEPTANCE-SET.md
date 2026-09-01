# Step 3 acceptance set

Status: **proposed v0.1**. Frozen when Step 3 is approved.

Standard under test: `VISUAL-TRANSLATION-STANDARD.md` · Gates: `STAGE-GATES.md`

Validator: `validate.py` — SHA-256 `0d87a65b317a2dfb396ab374e7bf19c456427c337cb3ebb520f0f06566d7b3c0`

Fixtures are test-only. They cannot create an episode workspace, approve any episode's visuals, or authorize Step 4.

## What the validator does and does not establish

It implements only the gate conditions that are **mechanically decidable**. It clears **hygiene**.

It cannot establish whether the direction is any good. Whether a visual mechanic is honest, whether motion expresses meaning, whether a style frame is worth looking at — those are the creative decisions each gate records separately. A clean validator run is readiness for that judgement, never a substitute for it.

This mirrors the distinction Step 2's E5V draws between mechanical support and positive identity, and it exists for the same reason: a passing structural check is exactly the evidence that misled the EP006 coverage review at 21 out of 23.

## Controls

Ten controls. One positive baseline, nine adversarial. Every adversarial control must fail **exactly** its target gate, not merely fail.

| Control | Injected defect | Must fail | Result |
|---|---|---|---|
| `positive/clean-baseline` | none | nothing | **PASS** |
| `adversarial/a1-engine-diverges` | engine restates the customer differently from the Canvas | **V2** | **PASS** |
| `adversarial/a2-inert-unit` | plan unit with no state change and no evidence, unjustified | **V4** | **PASS** |
| `adversarial/a3-look-final` | look recorded as final rather than provisional | **V6** | **PASS** |
| `adversarial/a4-runtime-named` | a runtime named inside a locked artifact | **V7** | **PASS** |
| `adversarial/a5-estimated-timing` | unit timing estimated rather than transcript-bound | **V4** | **PASS** |
| `adversarial/a6-orphan-claim` | evidence anchor bound to a claim ID that does not exist | **V3** | **PASS** |
| `adversarial/a7-label-upgrade` | a visual upgrades an evidence label from MODELED to OBSERVED | **V4** | **PASS** |
| `adversarial/a8-unreachable-object` | world object neither verb-reachable nor marked static | **V3** | **PASS** |
| `adversarial/a9-compounding-metaphor` | mechanic named a compounding flywheel with no compounding evidence | **V2** | **PASS** |

Run: `for d in positive/* adversarial/*; do python3 validate.py "$d"; done`

## Required behaviours

Step 3 must continue to satisfy all of the following:

1. A derived engine field that diverges from the locked Canvas fails. Step 3 cannot produce a second description of the business.
2. A visual mechanic implying compounding fails without evidence that the economics compound.
3. Motion verbs number three to six and are business verbs.
4. Every object a verb acts on exists, and every world object is verb-reachable or explicitly static.
5. An evidence anchor bound to a nonexistent claim fails.
6. Plan timing that is estimated rather than transcript-bound fails.
7. A plan unit with no state change and no evidence fails unless justified in writing.
8. A visual that upgrades an evidence label fails.
9. A look recorded as anything but provisional fails.
10. A runtime named in any locked artifact fails.
11. A broken audio-only element fails.
12. A structural pass never implies creative approval.

## Change control

- A semantic change to any gate condition, the derived-versus-authored split, the act-approval rule, the provisional-look rule, or the runtime exclusion requires a new Step 3 version.
- Rerun the full acceptance set before approving that version.
- Preserve these controls. **Do not edit a control to conform to a new rule.** If a control's expected outcome changes, add a dated fixture and state whether it changed because the rule changed or because the input changed.

## Known gaps

The validator does not yet cover:

- V1 upstream hash verification, which needs a real episode with both locks.
- V5a and V5b entirely. Rhythm and direction are judgement gates with no mechanical surface, and no fixture here tests them.
- Continuous act coverage and gap detection in V4, which needs a real transcript.
- Object permanence in V3, which is a visual judgement rather than a data property.

**These gaps are recorded rather than hidden.** A clean run across ten controls proves the mechanical conditions bite. It does not prove Step 3 is complete.

## Scope boundary

Passing this set would approve Step 3 behaviour only. It does not approve an episode's visuals, populate any workspace, choose a runtime, or make Steps 4 through 8 authoritative.
