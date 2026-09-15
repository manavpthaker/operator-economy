# Step 3 tandem design-language register — EP007 / EP008 / EP009

**Status:** non-gate coordination register. It records no process, episode, visual, production, delivery, or release approval.

**Snapshot:** `step2-integration` at `e4b4f26fee302f7252820835efcc90e730daf18d` on 2026-09-04. Uncommitted work is not made authoritative by this register.

## Portable authority

| Authority | Status | Exact SHA-256 | Source |
| --- | --- | --- | --- |
| Boundary Ledger manifest | `canonical-semantic-authority` | `ea0adb6da7403365d0d6f0bd82b167cdeeb7f40b8c8dbfc634ef92fa414c58aa` | `design-system/boundary-ledger/manifest.json` |
| Boundary Ledger semantic core | `canonical` | `30a316f79bc94e017705de0823a0af5b85747a20938eb0a2723d39a1a298978e` | `design-system/boundary-ledger/semantic-core.json` |
| Color binding | `canonical` | `6b3e4727c3592b02fe23c34d2a865a85c47865c438d48526d1762b93e9a669c3` | `design-system/boundary-ledger/bindings/color.json` |
| Motion binding | `provisional` | `b2ca3e3295ef2f1dd676732b6b9c7bdefbcfbf55ff642cdf1ab90dc9c84fb450` | `design-system/boundary-ledger/bindings/motion.json` |
| Sound binding | `provisional` | `3c81a029d6fd98ea8fb88100ff6209cc86f6ba7c1558bdd194d73db1ac5d294b` | `design-system/boundary-ledger/bindings/sound.json` |
| EP006 Working Model reference | `locked-reference`; owner-approved `visual-language-only` | `083533f79798ef04d66b112fa1a2275e1e181074c6e80c22591fc67ea54c6712` | `design-system/boundary-ledger/illustration/episode-006/hotel-working-model.jpg` |

The canonical semantic roles, operations, and universal invariants are portable. Episode objects,
layouts, timing, media, copy, evidence, and finished compositions are episode-local. The EP006
approval is a visual-language reference only; it does not approve its facts or composition for reuse,
and it does not approve EP007, EP008, or EP009.

## Episode-local state

| Episode | Step 3 state recorded here |
| --- | --- |
| EP007 V1 | Mechanically passed inside the current pilot; this does not approve the Step 3 process. |
| EP007 V2 | **Returned by tandem semantic audit; file unchanged.** Candidate SHA-256 `880d0e22e8c25e8ec806864575155bfd65e8e20eed66619c8e49a083bb5a376d` must not proceed to owner approval in its current form. |
| EP007 V3 | **Consequentially returned; file unchanged.** World SHA-256 `7c45b90857989f99b2657a5aa8f54a013f9888f275f94a1fa765c521b9e1563b` depends on the returned engine and also contains independent route/state defects. |
| EP007 V4–V7 | Absent / not started. |
| EP008 V1 | **Returned.** The 13 candidate inputs close mechanically, but the E6 literal, Step 1 internal chain/status, and process-authority conditions do not. |
| EP008 V2/V3 | **Ungated repaired drafts; no approval.** Engine `314c1a0d185e67c56cbbd6bbdef16f6cafd9fdcb9406df410ad0ab2ed9fef7c0`; world `302af15ca1459af98b0fab386571168f2c1c127c95c92dd4487b9cb2741e545c`; nine semantic gaps remain explicit. |
| EP008 V4–V7 | Absent / not started. |
| EP009 V1 | **Not passed.** The 13 candidate inputs close mechanically, but the E6 literal, Step 1 internal chain/status, and process-authority conditions do not. |
| EP009 V2/V3 | **Ungated repaired drafts; no approval.** Engine `f3c9a88d683dd7a99fe5dbd1239611fac723ab8b726d4c0a7b259733c4db6373`; world `82b6fb22bc23060f7e11a7e62c058727e64c2e4edf13be43e4c637c0dc5bb355`; four semantic gaps remain explicit. |
| EP009 V4–V7 | Absent / not started. |

**EP007 V3 review-record defect:** `V3-WORLD-APPROVAL.md` says four of fourteen objects are static and three carry nothing. The hash-bound `world.json` has six static objects and four objects with empty `changed_by`, `carried_by`, and `revealed_by`. Correct and rebind that review record before any owner decision.

**EP007 tandem semantic finding:** BO-004 uses `correct` to create a remediation plan without the
required legible prior mark; BO-005 combines a true movement branch with a documentation branch under
`return`; and BO-007 uses `settle` to create dispositions and a signature. The world then compounds
those mismatches. Preserve only the mappings that satisfy the exact canonical state change, record any
missing operation as a Boundary Ledger change request, and rebuild V3 after V2 is repaired.

## Process standing

Step 3 v0.3 remains proposed. Its exact process manifest (`4f830d71d677efa8915429dfe35628012289c28ac988cb74f77261331519690c`) says authority was returned on 2026-09-02 and has not been re-granted. Candidate artifacts may be developed and mechanically tested, but no episode gate advances under this register.

The acceptance evidence also names a different fixture-tree digest from the current frozen tree. Reconcile and rebind that evidence before asking for process approval; a clean episode-validator run does not repair the process-evidence mismatch.

Two V1 contract gaps currently block EP008 and EP009 from being called passed: both editorial locks record E6 as `LOCKED` but omit the exact `Gate E6: PASSED` phrase required by `STAGE-GATES.md`, while the mechanical validator does not check that phrase. Separately, the V1 input-lock template omits `canonical_w` and `spoken_identity`, although the validator requires both. Episode candidates must bind all thirteen real inputs and keep the gate state explicit until those contract differences are ruled.

Both repository package verifiers accept their exact locked Step 2 packages, but the generic
`validate-transcript` and `validate-state` commands reject both bespoke packages under the current
generic schema and 24-bit master contract. EP008 reports 17,006 transcript and 11 state findings;
EP009 reports 17,001 transcript and 11 state findings. This is not evidence that either narration
lock drifted. The proposed V1 gate does not name those commands, schemas, or the 24-bit contract, so
the mismatch is not independently a V1 failure and creates no Step 2 change request. Before process
approval, decide whether those commands remain separate diagnostics or require an approved adapter.

The current through-V3 validator also does not compare `world.json.engine_sha256` with the current engine bytes or inspect the hashes written into the Markdown review records. A stale EP009 world/review binding temporarily returned `PASS` during this tandem build and was caught only by a separate closure check. Add that check to the process acceptance set before process approval.

The tandem input audit found another validator blind spot: EP008 and EP009 editorial locks bind the
current files, but their dependent Step 1 documents still cite earlier Canvas, thesis, spine, and beat
hashes, and both script headers still describe review or owner approval as pending. Those references
may have been intended as historical draft identities, but each artifact instructs downstream files to
store its post-approval hash. V1 therefore needs a Step 1 ruling and a recursive internal-chain/status
check; the outer editorial-lock table alone is insufficient evidence of a coherent upstream freeze.

## Cross-episode promotion rule

A rule discovered in EP007 does not become shared design language through reuse or episode approval. To become portable, it must first be promoted into the applicable Boundary Ledger medium binding or contract, assigned an exact hash and status, and explicitly locked there. EP007, EP008, and EP009 must then each adopt that exact rule independently in their own hash-bound Step 3 artifacts. No episode inherits another episode's approval.

## Contract finding from the tandem replay

The current V2 shape asks one Boundary Ledger operation to do two jobs: cause the upstream business
change and describe how that change becomes legible. That is what allowed `settle` to appear to sign
an acceptance, `pin` to appear to compute a value, `correct` to appear to create a document, and
`return` to appear to create an additional consented relationship.

Before adding a long list of new canonical operations, test a narrower contract repair:

1. keep the upstream-derived business transition as the factual before/after authority;
2. name its actual causal trigger separately — human decision, consent, payment, test result, system
   action, or operator action;
3. bind an ordered visual-expression sequence to that transition, with every Boundary Ledger
   operation satisfying its own canonical required state change; and
4. prohibit `pin` and `settle` from masquerading as the cause of a calculation, decision, signature,
   payment, delivery, or record creation.

Only gaps that remain after that replay should be proposed as new cross-media Boundary Ledger
operations. This is a process-design finding, not an approved amendment; the shared Step 3 files and
Boundary Ledger are unchanged.

## What may actually carry across the three episodes now

- **Canonical now:** the six Boundary Ledger role meanings; the eight operation meanings; the
  semantic color binding; one primary focal point; one active commitment; attributable evidence;
  evidence status never upgraded by design; causal motion followed by settle; stillness as authored
  state; and relationship-equivalent recomposition rather than cropping.
- **Provisional only:** motion and sound expression bindings. They may be pinned and tested, but this
  register does not upgrade their status.
- **Episode-local:** actors, objects, zones, routes, evidence, money values, timing, composition,
  motifs, camera, media, and original-video references.
- **Not reusable:** any returned EP007 mapping, any EP008/EP009 draft mapping, or any episode gate
  decision. Reuse requires the promotion rule above.

## Original-video reference boundary

Original-video visuals may enter only as a named V6 reference stack under the Step 3 non-imitation
rule. They may inform treatment after V1–V5 are valid; they do not carry brand semantics, episode
approval, facts, timing, composition, scene assignments, media choices, or implementation vocabulary
into a new episode. No legacy storyboard, coverage map, render-data record, scene component, or prior
approval is imported into the new production path.

This V1–V3 tandem pass did not inspect or derive a visual conclusion from the legacy frames or
renders. Before V6, the exact references must be named, their provenance and permitted use recorded,
and the review must state what treatment is being learned and what distinctive composition or identity
will not be copied.
