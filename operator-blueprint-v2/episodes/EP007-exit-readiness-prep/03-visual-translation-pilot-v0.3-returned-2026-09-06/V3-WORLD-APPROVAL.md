# Gate V3: persistent world — EP007

## Status

**AWAITING OWNER REVIEW as a PILOT CANDIDATE against `world.json` `7c45b90857989f99…`.**

Not a gate pass. Step 3 v0.3 authority was returned on 2026-09-02 and has not been re-granted.

| Artifact | SHA-256 |
|---|---|
| `world.json` | `7c45b90857989f99b2657a5aa8f54a013f9888f275f94a1fa765c521b9e1563b` |

## What changed since the returned review

- **`operator` contradiction resolved.** It was simultaneously static and given operation-triggered transitions. Its phases were production phases, not world state, and no operation acts on it. States and transitions removed; it is static and carried by all five operations.
- **Paths are routes, not state lists.** `path.transfer` and `path.remediation` now declare a traveler and typed edges with `from`, `to`, `condition` and trigger — eight edges total.
- **Every transition reconciled with `changed_by`.** A transition may only be triggered by an operation that changes that object, or by a declared failure route. Five transitions that could not occur were removed, including BO-006's after its withdrawal.
- **`customer-concentration` given its own state machine** — unanalysed → analysed → recorded-as-structural / recorded-as-remediable. It can no longer be surfaced by interviews or reduced by owner-dependence work.
- **`diligence-package` is now static**, with the reason stated: BO-006's withdrawal means the engine no longer models its assembly. It remains in the world as an inspectable object and evidence carrier.
- **Anchors carry their upstream must-not-imply verbatim** from the claims map — C001 may not imply preparation changes the sale rate; C005 may not imply an unprepared business attracts the same interest; and so on for all seven.

## Machine conditions

```
validate.py --through V3 episodes/EP007-exit-readiness-prep/03-visual-translation
-> gates failing: none
```

54 acceptance controls; per-control results frozen in `fixtures/ACCEPTANCE-EVIDENCE.md`.

## Known weakness carried into review

Four of fourteen objects are static, and three carry nothing at all — `net-worth-mass`, `adviser`, `engagement-scope`. That is deliberate: each marks something the engagement does not change. But a world where a quarter of the objects never move is worth reading with the question of whether they earn their place on screen.

## Boundary

Reviewing this as a pilot candidate does not grant Step 3 authority, activate any gate, or authorize
Step 4. Only V7 authorizes Step 4, and only under an approved process.
