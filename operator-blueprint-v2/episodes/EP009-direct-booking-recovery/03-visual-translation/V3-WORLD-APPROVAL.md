# Gate V3 persistent world draft candidate: EP009

## Status

**UNGATED DRAFT. V3 HAS NOT BEEN ATTEMPTED OR PASSED.**

V1 is not passed, V2 has no gate decision, four engine semantics remain blocked, and proposed Step 3 v0.3 has not regained owner authority. This is review material only: it contains no owner approval, activates no gate, and authorizes no later production step.

| Artifact | SHA-256 |
|---|---|
| `world.json` | `82b6fb22bc23060f7e11a7e62c058727e64c2e4edf13be43e4c637c0dc5bb355` |
| Bound `engine.json` | `f3c9a88d683dd7a99fe5dbd1239611fac723ab8b726d4c0a7b259733c4db6373` |
| Claims map | `37f9f4727cde1b7e52fd75745117685336a28ec5f6756cf5f1be3dea1bb68798` |

## Candidate content

| World element | Count |
|---|---:|
| Objects | 28 |
| Static objects | 23 |
| Wholly unbound static objects | 4 |
| Object classes | 3 |
| Zones | 5 |
| Paths | 2 |
| Evidence anchors | 38 |
| Failure routes | 6 |
| Money flows | 4 |
| Human judgement gates | 6 |
| Camera anchors | 5 |

Engine `acts_on` and world `changed_by` pairs close in both directions. Engine `carried` and world `carried_by` pairs close in both directions. Establishment `reveals` and world `revealed_by` pairs also close in both directions. Every engine operation changes an explicit persistent object; object-class membership remains declarative rather than a shortcut for changing unrelated instances.

## Blocked-transition treatment

- DSB-001: `property-guest-record` begins only as an already existing, separately consented, eligible record. No edge creates it, and the platform relay remains a separate unchanged object.
- DSB-002: `audit-recommendation` is a static three-option form awaiting human disposition. No edge creates or selects the recommendation.
- DSB-003: the four inputs, precomputed modeled ceiling, and stable `audit-bundle` retain separate identities. No edge computes or binds them.
- DSB-004: `direct-path.findability` begins with a recorded finding so BO-003 can revise its consequence. No edge depicts the preceding test-to-finding creation. Mobile booking, policy readability, and phone fallback remain static declared test scope because Step 1 names no distinct mapped correction for them.

The stable audit bundle is a container, not a state-change substitute: it prevents the inputs, ceiling, findings, and recommendation from morphing into one another while their unsupported creation/calculation/disposition transitions remain absent.

## Approval, revocation, and reversibility

BO-005 routes an existing `queued-consented-checkout` work item only to `drafted-and-scheduled-awaiting-review`. `gate.message-approval` remains human, and the world encodes no approval or send transition.

BO-009 changes an eligible property-held record to `revoked-and-owned-eligibility-closed` and stops pending work. Both transitions are `reversible: false`; Step 1 supplies no sourced re-consent or automatic reopening path. The record remains recognizable rather than being deleted.

BO-008 follows a distinct `route.no-movement` mark: the unchanged result becomes visible before the bounded diagnosis is added. This keeps `correct` from manufacturing the failure it responds to.

## Money-flow boundary

All four flows state an explicit direction:

- platform commission: `property to platform`
- audit fee: `property to operator`
- monthly retainer: `property to operator`
- modeled direct-stack cost: `property to direct-stack providers`

The direct-stack recipient and C020 cost anchor keep 3.5–5 percent of modeled moved revenue between gross avoided commission and modeled net recoverable value. No flow implies that revenue moved, commission was saved, a vendor was paid, or the practice earned a fee.

## Static-object disclosure

Exactly **23 of 28 objects are static**. Exactly **4** are wholly unbound in the engine/establishment sense: they have no `changed_by`, `carried_by`, or `revealed_by` entry.

1. `direct-stack-cost-recipient` — a modeled aggregate recipient. It is referenced by `flow.direct-stack-cost` and the C020 cost anchor, but no business or establishment operation changes or reveals it.
2. `adjacent-market-record` — qualified comparison evidence, not demand for the proposed band.
3. `operator-capacity-model` — modeled economics, not delivered performance.
4. `validation-plan` — a planned test, not a completed result.

The remaining 19 static objects are carried or revealed context, declared test scope, source records, external systems, outcome boundaries, or human actors the proposed practice cannot transform. Static status is deliberate, but owner review may still remove an object that does not earn persistent-world status.

## Evidence boundary

Thirty-eight anchors cover every current claims-map ID from C001 through C037. C020 intentionally has two anchors: one on the ceiling and one on the direct-stack outflow. Added coverage for C006, C011, C012, C015, and C017 retains each claim's secondary, self-published, observed-absence, population-context, or modeled-transfer qualification.

The unnamed inn and returning guest remain archetypal. Global vendor data, European data, secondary programme reporting, open-R001 messaging durations, public tool prices, component capability, modeled ceiling arithmetic, modeled operator economics, acquisition hypotheses, and the editorial BUILD judgment never become evidence of a property result. No state records a service-caused booking, direct-share gain, commission saving, owner approval, recommendation, retainer sale, renewal, retained-customer count, or viable room band.

## Mechanical result

Command:

```text
python3 operator-blueprint-v2/03-visual-translation/fixtures/validate.py --through V3 operator-blueprint-v2/episodes/EP009-direct-booking-recovery/03-visual-translation
```

Result on 2026-09-04:

```text
gates failing: none | expected: none | PASS
```

This is structural hygiene only. The validator does not read the V1 Markdown decision; verify the Step 1 internal dependency chain or script status; enforce the literal E6 phrase; test the separate generic narration tools; assess the four Boundary Ledger semantic gaps; or supply process/owner authority. A clean result cannot pass V1, V2, or V3.

## Decision

Result: **NO GATE DECISION — UNGATED DRAFT; WORLD REVIEW DEPENDS ON V1, V2, AND DSB-001 THROUGH DSB-004**

Approved by: **nobody**

Formal review requires, in order: a valid V1 disposition, authority for the exact Step 3 process snapshot, resolution or explicit upstream disposition of the four engine blockers, named owner review of the exact engine hash, then named owner review of this exact world hash.
