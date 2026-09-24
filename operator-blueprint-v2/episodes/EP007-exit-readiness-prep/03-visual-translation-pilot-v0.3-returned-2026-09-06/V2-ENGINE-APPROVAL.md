# Gate V2: episode engine — EP007

## Status

**AWAITING OWNER REVIEW as a PILOT CANDIDATE against `engine.json` `880d0e22e8c25e8e…`.**

Not a gate pass. Step 3 v0.3 authority was returned on 2026-09-02 and has not been re-granted.

| Artifact | SHA-256 |
|---|---|
| `engine.json` | `880d0e22e8c25e8ec806864575155bfd65e8e20eed66619c8e49a083bb5a376d` |

## What changed since the returned review

- **BO-006 withdrawn.** Assembling a deliverable is not a claim gaining source context, and no permitted role/operation pair expresses it. `pin` had been reverse-fitted across two revisions. Recorded in `excluded_operations` with the reasoning, rather than bent to fit. `pin` and `accountableEvidence` are now unused at engine level, which is correct — pinning is how evidence *appears*, which is direction (V5a), not a business-state change.
- **Class-wide targeting replaced with instance targets.** Each operation now names the instances its own source covers, with a rationale. `customer-concentration` is excluded from BO-002 and BO-005: it is neither an owner-held relationship nor something only the owner does, and the Canvas offers analysis of it rather than reduction.
- **BO-003 retargeted to the path.** What changes is `path.transfer`, not the parts. The parts and the buyer are carried unchanged — repricing is a state of the route toward a buyer, and the engagement never alters the buyer.
- **`carried` added** so an operation distinguishes what it changes from what is merely present.
- **V1 freeze completed** to all 13 governing inputs.

## Machine conditions

```
validate.py --through V2 episodes/EP007-exit-readiness-prep/03-visual-translation
-> gates failing: none
```

54 acceptance controls; per-control results frozen in `fixtures/ACCEPTANCE-EVIDENCE.md`.

## Known weakness carried into review

The engine now carries **five** operations, not seven. Two were withdrawn or absorbed rather than made to fit. If that leaves the episode under-described, the fix is upstream — a Canvas that states the missing change — not a sixth operation reverse-fitted to a spare Boundary Ledger verb.

## Boundary

Reviewing this as a pilot candidate does not grant Step 3 authority, activate any gate, or authorize
Step 4. Only V7 authorizes Step 4, and only under an approved process.
