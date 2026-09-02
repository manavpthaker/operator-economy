# Step 3: visual translation

Status: **boundary only; not authoritative.** Scope boundary approved 2026-09-01. Boundary Ledger
derivation correction proposed as Step 3 v0.2 on 2026-09-02. The standard, gates, templates,
authority map, and acceptance set exist but remain proposed until approved.

Step 3 receives an episode whose words are locked and whose narration is timed, and produces a
visual language complete enough that Step 4 can direct shots from it without re-deciding what the
episode means.

It answers one question: **what should the viewer be looking at, and why that.**

## Documents

| File | Status |
|---|---|
| `SCOPE-BOUNDARY.md` | **approved** 2026-09-01 |
| `PORTING-MANIFEST.md` | frozen v0.2 source hashes and Boundary Ledger pins |
| `VISUAL-TRANSLATION-STANDARD.md` | **proposed v0.2** |
| `STAGE-GATES.md` | **proposed v0.2** — V1 to V7 |
| templates | **proposed v0.2** — eight, one per gate |
| `AUTHORITY-MAP.md` | **proposed v0.2** |
| fixtures and acceptance set | **proposed v0.2** — preserved v0.1 controls plus Boundary Ledger derivation controls |

## Templates

```text
01-input-lock/  INPUT-LOCK.template.md              V1
02-engine/      EPISODE-ENGINE.template.md          V2
03-world/       PERSISTENT-WORLD.template.md        V3
04-visual-plan/ VISUAL-PLAN.template.md             V4
05-direction/   DIRECTION-BIBLE.template.md         V5a
                RHYTHM-MAP.template.md              V5b
06-look/        LOOK-DEVELOPMENT.template.md        V6
07-approval/    VISUAL-TRANSLATION-LOCK.template.md V7
```

## Owns

Episode engine, persistent world, full-timeline visual plan, direction bible, rhythm map, look
development, and the episode's application of Boundary Ledger operations.

## Consumes

From Step 2 at narration lock: the narration master and its hash, the **word-level transcript and
intentional-pause map**, and the duration. From Step 1 at editorial lock: the Operator Canvas,
Episode Investment Thesis, narrative spine, beat sheet, claims map, and the locked script identity.

From Boundary Ledger 2.0: the hash-pinned semantic core and motion binding. Step 3 derives each
plain-language `business_operation` from locked upstream state, then selects a valid
`boundary_ledger_operation_id`. It does not author a replacement motion vocabulary.

## Does not own

Sequence treatments, shot boards, scene directions, motion test, animatic and asset plan are Step 4.
Assets and rights are Step 5. Conform and finishing are Step 6. **Runtime and toolchain choice
belongs to Steps 4 through 6; Step 3 is deliberately tool-agnostic.**

Brand semantics, medium bindings, and implementation primitives also remain external. Boundary
Ledger owns the first two; Steps 4 through 6 own the last.

## Dependency

Step 3 cannot run on a real episode until Step 2 closes for that episode, because it consumes the
word-level transcript produced at N6. EP007 has N5 through N7 open. Step 3 can be designed and
fixture-tested before then.
