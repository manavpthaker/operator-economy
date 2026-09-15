# Episode initialization and production templates

`oe-cinema init EP### <slug>` uses the deterministic episode structure documented in `../../ARCHITECTURE.md`.

Initialization must require an explicit episode number and slug, derive the zero-padded code and folder name, reject mismatches, and write only new Blueprint Cinema files. It must not rename or copy the upstream `studio/originate/<slug>/` workspace.

The current v1 initializer represents identity and initial production state in code. It does not yet create the documentation-canonical direction, HyperFrames, asset-select, edit, sound, or Resolve artifacts below. Until the runtime migration is implemented, create them deliberately and report them as authored documentation rather than CLI-enforced state.

## Reusable templates

| Template | Use |
|---|---|
| `DIRECTION-BIBLE.template.md` | Episode-specific visual, camera, motion, typography, documentary, AI, sound, and negative rules. |
| `RHYTHM-MAP.template.md` | Whole-episode energy, density, mode, proof, human-contact, and handoff plan. |
| `SEQUENCE-SHOT-DIRECTION.template.md` | Sequence treatment, static shot board, action phases, exact shot direction, assets, sound, and checks. |
| `HYPERFRAMES-BUILD-PACKET.template.md` | Compiled, bounded implementation brief with exact continuity, frame, text, motion, media, sound, output, and verification requirements. |
| `AI-PLATE-GENERATION-PACKET.template.md` | Ticket-bound prompt and candidate record for non-evidentiary AI plates, continuity, disclosure, and rejection criteria. |
| `ASSET-SELECT.template.md` | Ticket, candidate, rights, provenance, technical probe, editorial selection, and synthetic metadata. |
| `EDIT-RESOLVE-HANDOFF.template.md` | Edit manifest, HyperFrames plate package, Resolve conform, track map, sound, color, and delivery plan. |
| `REVIEW-REPORT.template.md` | Artifact-hash-bound review findings, severity, evidence, decision, and approval record. |

Templates are starting shapes, not schemas or approvals. Episode artifacts replace every placeholder, cite exact approved IDs and hashes, and are reviewed under `../../references/REVIEW-QA.md`.

## Target episode scaffold

```text
episodes/EP###-slug/
├── episode.json
├── input-lock.json
├── production-state.json
├── episode-engine.json
├── world.json
├── visual-plan.json
├── scene-directions.json
├── asset-tickets.json
├── direction/
│   ├── direction-bible.md
│   ├── rhythm-map.md
│   ├── lookdev/
│   └── shot-board/
├── hyperframes/
│   ├── BRIEF.md
│   ├── frame.md
│   ├── STORYBOARD.md
│   ├── hyperframes.json
│   ├── index.html
│   ├── compositions/
│   ├── public/
│   ├── snapshots/
│   └── renders/
├── assets/
│   ├── manifest.json
│   ├── candidates/
│   ├── selects/
│   ├── source/
│   ├── derivatives/
│   ├── proxies/
│   └── reports/
├── edit/
│   ├── edit-plan.json
│   ├── sound-plan.json
│   ├── handoff/
│   ├── resolve/
│   └── reports/
├── agents/
├── prompts/generated/
├── review/
└── delivery/
```

Large and licensed media, generated frames, HyperFrames renders, Resolve project archives, caches, and proxies remain ignored. Their tracked manifests preserve identity, hashes, provenance, versions, status, and use.

After the visual plan and visual language are approved, use deterministic director packets to author shot-level `scene-directions.json`. Validate that file before compiling HyperFrames build packets or starting the directed animatic. Generated prompt packets, storyboard files, successful checks, renders, Resolve timelines, and delivery exports never become approvals merely because they exist.
