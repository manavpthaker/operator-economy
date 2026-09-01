# Step 3: visual translation

Status: **boundary only; not authoritative.** Scope boundary approved 2026-09-01. Standard proposed
v0.1. Gates, templates, authority map and acceptance set are not yet written.

Step 3 receives an episode whose words are locked and whose narration is timed, and produces a
visual language complete enough that Step 4 can direct shots from it without re-deciding what the
episode means.

It answers one question: **what should the viewer be looking at, and why that.**

## Documents

| File | Status |
|---|---|
| `SCOPE-BOUNDARY.md` | **approved** 2026-09-01 |
| `PORTING-MANIFEST.md` | frozen v0.1 source hashes |
| `VISUAL-TRANSLATION-STANDARD.md` | **proposed v0.1** |
| `STAGE-GATES.md` | **proposed v0.1** — V1 to V7 |
| templates | not written |
| `AUTHORITY-MAP.md` | not written |
| fixtures and acceptance set | not written |

## Owns

Episode engine, persistent world, full-timeline visual plan, direction bible, rhythm map, look
development, and the episode's shot-grammar selection.

## Consumes

From Step 2 at narration lock: the narration master and its hash, the **word-level transcript and
intentional-pause map**, and the duration. From Step 1 at editorial lock: the Operator Canvas,
Episode Investment Thesis, narrative spine, beat sheet, claims map, and the locked script identity.

## Does not own

Sequence treatments, shot boards, scene directions, motion test, animatic and asset plan are Step 4.
Assets and rights are Step 5. Conform and finishing are Step 6. **Runtime and toolchain choice
belongs to Steps 4 through 6; Step 3 is deliberately tool-agnostic.**

## Dependency

Step 3 cannot run on a real episode until Step 2 closes for that episode, because it consumes the
word-level transcript produced at N6. EP007 has N5 through N7 open. Step 3 can be designed and
fixture-tested before then.
