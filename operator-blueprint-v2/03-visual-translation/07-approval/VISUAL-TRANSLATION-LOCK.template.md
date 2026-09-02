# Visual translation lock: [episode]

Gate: **V7 — visual translation lock and Step 4 handoff**

Template version: proposed Step 3 v0.2

Episode: EP###

Locked: YYYY-MM-DD · Locked by: [name]

This is the visual language Step 4 is authorized to direct from.

## Frozen artifacts

| Artifact | Path | SHA-256 | Gate |
|---|---|---|---|
| Input lock | | | V1 |
| Episode engine | | | V2 |
| Persistent world | | | V3 |
| Visual plan | | | V4 |
| Direction bible | | | V5a |
| Rhythm map | | | V5b |
| Look development | | | V6 (provisional) |

## Upstream locks this depends on

| Lock | SHA-256 |
|---|---|
| Step 1 editorial lock | |
| Step 2 narration lock | |
| Narration master | |
| Word-level transcript | |
| Boundary Ledger semantic core (version + SHA-256) | |
| Boundary Ledger motion binding (status + SHA-256) | |

## Mutual consistency audit

Every operation binding, object, mode, motif and evidence anchor referenced in one artifact must
exist in the others. Every semantic selection must still resolve through the exact V1 design-system
lock.

| Check | Result |
|---|---|
| Every plan business-operation ID exists in the engine | pass / fail |
| Every plan Boundary Ledger operation ID matches its engine binding | pass / fail |
| Every selected semantic role and operation exists in the pinned core | pass / fail |
| Every selected role-operation pair is permitted by the pinned motion binding | pass / fail |
| Every plan object exists in the world | pass / fail |
| Every plan mode has a bible treatment | pass / fail |
| Every world object with a motif appears in the plan | pass / fail |
| Every evidence anchor traces to a live claim ID | pass / fail |
| Every bible motif references a real world object | pass / fail |
| Rhythm map matches the approved plan | pass / fail |

## Audio-only rule

No load-bearing element exists only in a visual.

| Element | Carried in VO | Visual role |
|---|---|---|
| Buyer | yes / no | |
| Problem | yes / no | |
| Company | yes / no | |
| First offer | yes / no | |
| Human responsibility | yes / no | |
| Economics boundary | yes / no | |
| Principal risk | yes / no | |
| First action | yes / no | |

## Runtime audit

**No runtime may be named anywhere in the locked artifacts.** Toolchain choice belongs to Steps 4 through 6.

Runtimes named: none / [violation and location]

## Vocabulary and implementation-boundary audit

- Episode-local motion vocabulary: none / [violation and location]
- Renamed or widened Boundary Ledger operation: none / [violation and location]
- Animation, scene, renderer, easing, or audio implementation primitive authored by Step 3: none / [violation and location]

## Unknown classification

| Unknown | Classification |
|---|---|
| | Step 4 test question / later-stage blocker / **current lock blocker** |

A current lock blocker fails Gate V7.

## Gate V7 decision

- V1 through V6 all `passed`, hashes match: yes / no
- Every act of the visual plan approved: yes / no
- Mutual consistency audit clean: yes / no
- Boundary Ledger versions and hashes still match V1: yes / no
- Operation trace is complete from upstream state through the locked artifacts: yes / no
- No local motion vocabulary, semantic override, or implementation primitive: yes / no
- Audio-only rule holds: yes / no
- No runtime named: yes / no
- No current lock blocker: yes / no
- Look recorded as provisional with the Step 4 return path stated: yes / no

Result: **locked** / fail

Visual translation lock SHA-256: [computed after this record is complete]

Approved by: [name] on YYYY-MM-DD

## Boundary for Step 4

Step 4 may direct shots, write scene directions, build the motion test and animatic, and plan assets.

Step 4 may **not** re-decide the engine, the world, the plan's timing, the selected Boundary Ledger
semantics, or the episode's meaning. Step 4 may choose implementation primitives, but they must
implement this lock rather than become a new semantic layer. If Step 4 cannot build what Step 3
approved, that is a Step 3 defect and returns here.

The look is **provisional**. Step 4's motion test may return it, invalidating V6 only — unless the return names a bible defect, which invalidates V5a as well.
