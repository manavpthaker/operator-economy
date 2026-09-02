# Step 3 authority map

Status: **proposed v0.2**. Step 3 is not yet authority. This map states what would become canonical if the design pass is approved.

## Proposed local Step 3 authority

The following files would be canonical for V2 visual translation. Approving them does not make Steps 4 through 8 authoritative.

1. `SCOPE-BOUNDARY.md` — what Step 3 owns, consumes, hands on, and may never do. **Approved 2026-09-01.**
2. `VISUAL-TRANSLATION-STANDARD.md` — the directing standard, its required artifacts, and the governing rules.
3. `STAGE-GATES.md` — gates V1 through V7, their pass conditions, and the invalidation rules.
4. `PORTING-MANIFEST.md` — frozen source hashes and the ported-versus-new-doctrine boundary.
5. `01-input-lock/INPUT-LOCK.template.md`
6. `02-engine/EPISODE-ENGINE.template.md`
7. `03-world/PERSISTENT-WORLD.template.md`
8. `04-visual-plan/VISUAL-PLAN.template.md`
9. `05-direction/DIRECTION-BIBLE.template.md` and `05-direction/RHYTHM-MAP.template.md`
10. `06-look/LOOK-DEVELOPMENT.template.md`
11. `07-approval/VISUAL-TRANSLATION-LOCK.template.md`
12. `fixtures/ACCEPTANCE-SET.md` — the frozen behavioural controls.

## Upstream authorities that stay external

Do not duplicate these into Step 3. Step 3 consumes them and may not change them.

| Authority | Owner | What Step 3 may do |
|---|---|---|
| Operator Canvas, Episode Investment Thesis, narrative spine, beat sheet, claims map | **Step 1** | Derive from. Never restate a business field differently, never widen a claim's wording |
| Locked script and `W` identity | **Step 1** | Reference. Never alter |
| Narration master, word-level transcript, intentional-pause map, duration | **Step 2** | Read timing from. **Never estimate timing** |
| `content-os/facts.md` | Content OS | Public numbers, names, dates, URLs. Step 3 introduces no new public fact |
| `content-os/voice.md`, `rubric.md`, `flow.md` | Content OS | Voice, scoring and release remain external |
| `design-system/boundary-ledger/semantic-core.json` | Boundary Ledger | Canonical cross-media roles, operations, and universal invariants. Step 3 pins and consumes it; it does not redefine it |
| `design-system/boundary-ledger/bindings/motion.json` | Boundary Ledger | Medium expression binding. Step 3 selects a permitted operation for an episode state change; it does not author another motion vocabulary |
| `design-system/boundary-ledger/bindings/color.json` and `bindings/sound.json` | Boundary Ledger | Other medium bindings. Step 3 may reference semantic roles but may not replace their meanings or values |

Operator Economy owns episode-specific visual direction. Content OS still owns public fact authority,
voice, rubric and release. Boundary Ledger owns cross-media brand semantics and bindings.

## Derived, selected, and authored

| Step 3 field | Status | Authority |
|---|---|---|
| `business_operation` and its before/after state | **DERIVED** | Exact Step 1 Canvas, narrative, beat, or claim state named by path and hash |
| `boundary_ledger_operation_id` and semantic role | **SELECTED** | Hash-pinned Boundary Ledger core and motion binding |
| Episode visual model, world, continuity, direction, rhythm, and operation sequencing | **AUTHORED** | Step 3, without creating new brand semantics or implementation primitives |

`SELECTED` is not `AUTHORED`: Step 3 chooses from the pinned authority and records why the operation
fits the upstream state change. It may not rename an operation, widen its meaning, or mint a local
motion verb.

## Reference material, not authority

| Source | Status |
|---|---|
| `blueprint-cinema/references/*` | Causal direction and prior art. Ported selectively per `PORTING-MANIFEST.md`; no source supplies brand motion semantics. **No Blueprint Cinema approval carries into V2** |
| `blueprint-cinema/episodes/EP006-*/` | Worked examples and fixture material. EP006's `greybox_ready` state is historical evidence, not a V2 gate pass |
| `blueprint-cinema/TOOLCHAIN.md` | External implementation authority; deliberately **not part of the Step 3 lock**. Step 3 names no runtime |
| `docs/blueprint-cinema.md`, `docs/pipeline.md`, `docs/storyboard-stage.md` | V1 history. Reference only |
| `studio/` and the Blueprint Cinema v1 CLI, state machine and renderer | V1 systems. Not authority, not a port target |

## Change control

- A semantic change to an artifact contract, a gate pass condition, the derived-selected-authored split, the Boundary Ledger pin, the act-approval rule, the provisional-look rule, or the runtime exclusion requires a new Step 3 version.
- Rerun the full acceptance set before approving that version.
- Preserve dated controls and their decision artifacts. Do not edit a control to conform to a new rule.

## Boundary

Approving this map would make Step 3 authoritative for visual translation only. It would not authorize Step 4, choose a runtime, approve any episode's visuals, or make Steps 4 through 8 authoritative.
