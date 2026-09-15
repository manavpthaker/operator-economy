# EP006 visual-plan QA

**Packet:** `visual-plan-qa`  
**Review result:** complete packet; **do not approve the visual plan yet**  
**Canonical gate observed:** `world_approved`  
**Authority:** read-only QA. This report records no approval and changes no production state.

## Input integrity

All five work-order inputs were recomputed before review and match their declared SHA-256 values:

| Input | SHA-256 |
|---|---|
| `input-lock.json` | `e99b847c5b5a767d74ad4208738374ac191da3d9d4c3e3654098a6c08e725691` |
| `episode-engine.json` | `e07ed63476684bc3e3a2757e1e30c651322859a9f27b4f25bc7a08d15ddc4b36` |
| `world.json` | `cf55980b1930d2150a578f9e23663bfb4f7c6ed7157141c24c7496550cf249af` |
| `visual-plan.json` | `eb8501b60dc72a158c69027622645290b7c4122502422bf8d870c2da9f6e313b` |
| `asset-tickets.json` | `ee0f8e8490a4ed35ca2c7b3ea94c5e1db546aaec0c8f4de38ef68dc7718fb919` |

The locked `vo/words.json` was independently rehashed as `00151975a93c818fe51dbf83feeb04bc7997bb0d9d8b424f8d1fa2539a927b76`, matching `input-lock.json`.

## What passes

### Full-timeline and word continuity

- 138 units cover exactly `0.000` through `915.550` seconds.
- There are zero timeline gaps, zero overlaps, and zero units beyond the locked VO.
- The plan covers all 1,922 locked words exactly once: first range `0-13`, last range `1907-1921`, with zero word-range gaps or overlaps.
- All 138 narration quotes exactly match their locked word ranges.
- Every anchor stays inside the runtime's allowed one-second timing tolerance. Unit starts precede their first anchored word by `0.010-0.746s`; unit ends follow their last anchored word by `0.010-0.844s`.

### Cadence and persistent sequences

- Unit duration: minimum `4.229s`, p25 `5.707s`, median `6.527s`, mean `6.634s`, p75 `7.416s`, maximum `10.871s`.
- Duration distribution: 47 units at `3-6s`, 71 above `6s` through `8s`, and 20 above `8s` through `16s`. No unit reaches the 16-second hard failure.
- The 20 units above eight seconds are review warnings, not automatic failures. The longest are `unit-080` at `10.871s` and `unit-105` at `10.650s`; both carry dense measurement/comparison work that needs greybox comprehension review.
- Camera continuity is strong: nine camera runs and only eight camera-anchor changes across the episode; the median camera run is 16 units / `110.860s`.
- Modes change 53 times across 54 runs, including 29 single-unit runs. This creates frequent reality/system/proof layering, but it does not reset the camera every unit.
- Every system-mode unit changes a declared business state. There are 24 same-state units, all in proof, reality, or reset modes; most establish evidence/reality or hold accumulated state. The unsupported proof units identified below are exceptions.
- Across all 137 unit boundaries, every `carry` object comes from the immediately prior unit's carry or focus set. The first unit deliberately seeds the operator and stay token.

### Structural references and placeholder honesty

- No dangling world-object, state, evidence, asset-ticket, or camera IDs were found.
- All five evidence IDs and all eight ticket IDs are used at least once.
- All eight asset tickets remain `ticketed_placeholder`. Seven prohibit synthetic substitution and the inn-reality ticket is `not_planned` for synthetic media.
- Every ticket's placeholder instructions require an explicit neutral slate and prohibit attractive proxies, invented interfaces, invented documents, invented figures, or fake identities as applicable.
- The first 30 seconds structurally contain physical reality (`unit-001`), a proof object (`unit-002`), the relationship leak (`unit-003`), the direct-path audit (`unit-004`), and the useful OTA gate beginning at `27.733s` (`unit-005`). The proof-to-claim mismatch in that opening is nevertheless blocking, as described below.

### Required semantic presence

Consent, qualification, suppression, human judgment, economics, audit, repair, failure-related objects, and the direct-confirmation outcome all appear in focus fields. The useful first-booking OTA path remains present, and the operator-side settlement ledger remains a different object and ticket from the guest-facing confirmation.

## Blocking findings

### 1. The timed state sequence bypasses the approved outbound gates

The world graph is ordered correctly, and every `world_state_before` matches the accumulated preceding state. The problem is semantic: the continuous state sequence activates downstream work before the prerequisite states are resolved.

- `unit-020` (`129.649-138.593s`) changes `return-booking-money-flow` from `initial` to `active` (`Direct value routed`) while `direct-path-repair` is still `active` (`Repair in progress`), `direct-booking-destination` is `failed`, and permission, qualification, and human review have not passed.
- `unit-042` (`275.364-282.644s`) changes `relevant-follow-up` from `suppressed` (`Stopped`) to `active` (`Approved follow-up`) even though its action says to keep follow-up inactive and permission/relevance have not been established. At that moment repair is not resolved, permission is `initial`, qualification is `initial`, and human review is `initial`.
- `unit-068` (`446.273-453.458s`) creates `guest-memory-context: active` (`Permissioned context`) while `permission-gate` is only `active` (`Permission requested`). Affirmative consent is the `resolved` state and does not occur until `unit-089`.
- `unit-093` (`614.467-619.332s`) resolves follow-up as delivered while qualification is still `active` (`Qualification running`), suppression is `active` (`Evaluating`), and human review was just changed back to `active` (`Human reviewing`) in `unit-092`.
- `unit-097` (`641.444-647.996s`) routes a return visit to the direct destination while qualification remains `active`, not `resolved` as an appropriate return.
- In the final recovery pass, `unit-129` changes permission from `resolved` (`Affirmative consent`) back to `active` (`Permission requested`) while its action claims that affirmative permission is recorded. `unit-132` changes human review from `resolved` (`Approved to send`) back to `active` (`Human reviewing`) while its action claims approval. `unit-133` then resolves the direct confirmation while those two gates are not in their approved states.

These are not cosmetic label issues. They visually contradict the engine's permission, qualification, suppression, human-review, and audit-before-return guardrails. The plan should remain unapproved until the canonical state transitions themselves enforce the outbound order.

### 2. The plan references failure machinery without running the defined failures

The runtime's current semantic check treats focus on any failure target as proof that a failure appears. The authored plan does not actually activate the four failures defined in `world.json`:

| Defined failure target | Required failed/suppressed state | Observed plan behavior |
|---|---|---|
| `direct-path-repair` | `failed` | Alternates between `active` and `resolved`; never fails |
| `permission-gate` | `failed` | Moves `initial -> active -> resolved -> active`; never declines or becomes ambiguous |
| `return-qualification-gate` | `suppressed` | Moves `initial -> active -> resolved`; never shows an irrelevant/sensitive case |
| `relevant-follow-up` | `failed` | Moves `initial -> suppressed -> active -> resolved`; never shows delivery failure |

Retry, suppression, and escalation objects do appear, but they are not causally entered from the configured failure states. At least one honest failure path should run end to end, and the stress-test section should make clear which branch is being demonstrated.

### 3. Opening proof is attached to the wrong claim

The opening narration states the vendor-published OTA-share figure across `unit-001` and `unit-002`.

- `unit-001` contains the beginning of the claim and has no evidence ID.
- `unit-002` contains the rest of the claim but attaches `evidence-commission-model` and `ticket-settlement-ledger`, which concern commission economics, not OTA booking share.
- The matching `evidence-ota-share` and `ticket-cloudbeds-source` do not appear until `unit-021` at `138.593s`.

The first 30 seconds therefore pass the coarse reality/proof/counter-system presence test while failing the stronger evidence-honesty test: the proof object shown does not prove the spoken claim.

### 4. Three proof sequences lack the evidence/ticket contract their actions claim

- `unit-050` and `unit-051` narrate the Mews funding round and valuation. Both have empty `evidence_ids` and `asset_ticket_ids`; `unit-050` explicitly says it opens a neutral proof ticket, but no ticket is referenced.
- `unit-099` narrates the reviewed providers' lack of simple public per-property pricing and calls this an evidence gap. It has neither an evidence ID nor an exact asset ticket.
- `unit-114` through `unit-117` correctly reference `evidence-labor-value`, but no ticket requests the exact salary-source capture. The existing human-review ticket is a process ticket, not a source-proof ticket.

These missing contracts would let the greybox present proof-mode claims without conspicuous exact placeholders for the proof still required.

### 5. Camera targets are materially under-specified relative to plan focus

The stable nine-run camera structure is a continuity strength. However:

- 33 non-reset units pair `reality`, `system`, or `proof` mode with a camera named for a different view.
- 86 of 138 units focus on an object not listed in the selected camera anchor's `target_ids`.

Examples include `unit-002` using `camera-human` for the settlement ledger, `unit-038` using `camera-proof` for the direct-path audit, and `unit-138` using `camera-system` for the reality-mode direct confirmation. If `target_ids` are exhaustive framing contracts, these are invalid. If they are only illustrative, the world contract should say so and the renderer should not imply exact target coverage. Resolve this ambiguity before relying on the greybox to prove focus and legibility.

### 6. Persistent state is technically continuous but frequently regresses without explicit replay semantics

There are zero raw before/after continuity mismatches, but 33 units transition an object from `resolved` back to `active` or `failed`. Some can represent another operating cycle, yet the plan does not identify a new cycle, branch, simulation reset, or replay. The most consequential regressions are the final permission and human-review examples above. Other repeated audit/proof operations may be defensible if the plan explicitly distinguishes a new run from a reversal of accumulated state.

## Required corrections before root approval

1. Keep direct value and outbound follow-up inactive until repair, affirmative permission, appropriate qualification, suppression disposition, and human approval are visibly satisfied in order.
2. Make the final agency sequence end with `permission-gate: resolved` and `human-review-gate: resolved` before direct confirmation.
3. Run at least one configured failure through its actual failed/suppressed state, retry or escalation route, and disposition; label any later replay/new cycle explicitly.
4. Attach `evidence-ota-share` and its exact source ticket to the opening claim rather than commission evidence.
5. Add explicit evidence/ticket contracts for the Mews investment claim and provider-pricing review; add an exact source-proof ticket for the salary evidence or document why the evidence pin alone is sufficient.
6. Either align focus with each camera's declared targets or make the camera target contract explicitly non-exhaustive and validate the intended framing another way.
7. Re-run the complete timeline, word, reference, state-order, and boundary audit after revision. Do not patch isolated units without validating the accumulated state through all 138 boundaries.

## Checks executed

- Recomputed all work-order input SHA-256 hashes: pass.
- Recomputed the locked word-transcript SHA-256: pass.
- `blueprint-cinema/bin/oe-cinema validate-work-order EP006-direct-booking-recovery visual-plan-qa`: pass.
- `blueprint-cinema/bin/oe-cinema validate-plan EP006-direct-booking-recovery`: formal runtime validation passes, but it does not detect the blocking temporal/evidence findings above.
- `blueprint-cinema/.venv/bin/python -m pytest -q blueprint-cinema/tests/test_visual_plan.py`: `4 passed`.
- Independent full-plan coverage, exact-quote, word-range, duration-distribution, accumulated-state, carry, camera/mode, evidence/ticket, required-semantic, and placeholder audit: completed; blocking findings recorded above.

No internet, external write, paid service, synthetic generation, canonical edit, approval, or production-state change occurred.
