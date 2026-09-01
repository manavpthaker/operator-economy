# Step 3 authority map

Status: **proposed v0.1**. Step 3 is not yet authority. This map states what would become canonical if the design pass is approved.

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
| `design-system/tokens/` | Design system | The brand token layer is the source of truth for colour, type and surface. Step 3 references tokens; it does not redefine brand values |

Operator Economy owns visual direction. Content OS still owns public fact authority, voice, rubric and release. The design system still owns brand primitives.

## Reference material, not authority

| Source | Status |
|---|---|
| `blueprint-cinema/references/*` | Reference and prior art. Ported selectively per `PORTING-MANIFEST.md`. **No Blueprint Cinema approval carries into V2** |
| `blueprint-cinema/episodes/EP006-*/` | Worked examples and fixture material. EP006's `greybox_ready` state is historical evidence, not a V2 gate pass |
| `blueprint-cinema/TOOLCHAIN.md` | Deliberately **not adopted**. Step 3 names no runtime |
| `docs/blueprint-cinema.md`, `docs/pipeline.md`, `docs/storyboard-stage.md` | V1 history. Reference only |
| `studio/` and the Blueprint Cinema v1 CLI, state machine and renderer | V1 systems. Not authority, not a port target |

## Change control

- A semantic change to an artifact contract, a gate pass condition, the derived-versus-authored split, the act-approval rule, the provisional-look rule, or the runtime exclusion requires a new Step 3 version.
- Rerun the full acceptance set before approving that version.
- Preserve dated controls and their decision artifacts. Do not edit a control to conform to a new rule.

## Boundary

Approving this map would make Step 3 authoritative for visual translation only. It would not authorize Step 4, choose a runtime, approve any episode's visuals, or make Steps 4 through 8 authoritative.
