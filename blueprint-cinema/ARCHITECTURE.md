# Blueprint Cinema architecture

## Boundary

Blueprint Cinema is a downstream visual-production system with two neighboring systems:

```text
UPSTREAM EDITORIAL                         BLUEPRINT CINEMA                         DOWNSTREAM RELEASE

research                                  hash-pinned input lock                  final long-form master
claims and evidence            ->         episode engine              ->         Shorts derivation
approved script                           persistent world                        packaging
final VO                                  visual plan                             upload and disclosure
word-level transcript                     direction and directed animatic         links.json
                                          assets, edit, finish, validation         content-os gate
```

Upstream artifacts are read through explicit adapters and hashes. Downstream systems receive only validated deliverables and never infer publication state from a local render.

## Production layers

```text
operator CLI
  -> identity and path resolution
  -> schema and semantic validation
  -> hash-bound state machine
  -> direction and asset contracts
  -> HyperFrames project and deterministic render gates
  -> Resolve interchange, conform, edit, finish, and delivery
  -> independent review and delivery reports
```

Blueprint Cinema owns meaning, direction, continuity, and approval. HyperFrames owns the deterministic implementation of designed scenes and the whole-episode directed animatic. Resolve owns final editorial, media conform, Fusion finishing, color, Fairlight, captions, online, and masters. `TOOLCHAIN.md` is the canonical ownership contract.

Authored creative data and generated data are kept separate:

- Authored: episode engine, world, visual plan, direction bible, rhythm map, sequence treatments, shot-level scene directions, asset tickets, asset selects, edit plan, sound plan, and deliberate review decisions.
- Generated: locks, indexes, director/build packets, HyperFrames snapshots and renders, proxies, interchange files, diagnostics, media probes, and reports that can be reproduced.
- Approval records: immutable evidence of what exact authored and input hashes passed a gate.

Generated code must never silently repair authored creative data. Validation reports the defect and exits nonzero.

## Episode workspace

The intended episode shape is:

```text
episodes/EP###-slug/
├── README.md
├── episode.json
├── input-lock.json                 # generated later by the CLI
├── production-state.json           # generated and advanced only by the CLI
├── episode-engine.json              # canonical authored artifact
├── world.json                       # canonical authored artifact
├── visual-plan.json                 # canonical authored artifact
├── scene-directions.json            # authored shot recipes; absent until direction work begins
├── asset-tickets.json               # canonical authored artifact
├── inputs/                           # ignored staged copies and input diagnostics
├── direction/                        # bible, rhythm, lookdev, treatments, and shot boards
├── hyperframes/                      # canonical episode motion project and review outputs
├── assets/                           # manifests, candidates, selects, source, derivatives, and proxies
├── edit/                             # plan, sound, handoff, Resolve, reports, and delivery metadata
├── agents/                           # work orders and isolated worker deliverables
├── prompts/generated/                # deterministic director and shot-build packets
├── render-data/                      # v1 generated props; superseded after runtime migration
├── review/                           # human-readable gate and QA reports
└── delivery/                         # ignored review/final media plus tracked manifests
```

Canonical authored JSON files stay at the episode root so CLI commands and approvals have stable, obvious targets. `scene-directions.json` is introduced only after the visual plan and is not inferred by the renderer. Media and generated working files live below their functional directories.

## Identity

`episode.json` is the project identity record. The runtime must verify:

```text
episode_number = 6
episode_code   = EP006
slug           = direct-booking-recovery
folder_name    = EP006-direct-booking-recovery
```

The upstream workspace remains `studio/originate/direct-booking-recovery/`; the relationship is stored as a repo-relative pointer and later hash-pinned by `input-lock.json`.

## Clean-room adapters

Adapters may read the approved script, final audio, timing, evidence, and design tokens. They may not read legacy storyboards, coverage maps, render data, scene assignments, or visual approvals. The clean-room validator inspects configuration and compiled provenance for prohibited references.

## HyperFrames boundary

HyperFrames consumes only approved greenfield artifacts compiled into bounded build packets and local manifests. Compositions render explicit object IDs, coordinates, states, timing, and behavior. They do not select layouts by parsing narration strings.

The prompt compiler sits before implementation. Director packets expose exact VO, world, evidence, visual-plan, direction-bible, rhythm-map, lookdev, continuity, and asset constraints. Reviewed `scene-directions.json` supplies authored sequence context, shot-level editorial intent, and an explicit picture/audio contract and adjacent `direction_facts`: what stays still, master/setup relationship and reference, action line and screen direction, typed continuity anchors, and initial and final images. It also supplies frame geometry, typography, motion cues, sound intent, and transition continuity. These shot facts are generator-independent and required before compilation. Build packets carry those decisions to bounded compositions without asking the builder to redesign the shot.

The first whole-timeline renderer target is a directed animatic: unfinished but compositionally, editorially, and temporally specific. Polished components and selected media are later substitutions against approved tickets, not reasons to restructure the episode.

The episode uses one thin root composition for locked narration, captions, timeline slots, and episode-level tracks. Bounded sequence and shot compositions live below it. All fonts and media are frozen locally. Version, checks, snapshots, animation maps, render settings, and media probes are recorded in the handoff manifest.

## Resolve boundary

Resolve receives the approved animatic reference, edit manifest, approved selects, source media, proxies, HyperFrames opaque and alpha plates, captions, audio, color metadata, markers, and interchange files. Resolve may automate deterministic ingest, conform, markers, rendering, and project export. Editorial, grade, and mix choices remain reviewable human judgments.

Changes that alter shot purpose, evidence timing, business state, object continuity, transition meaning, or locked VO return upstream. Picture lock requires agreement among the Blueprint Cinema edit manifest, Resolve timeline, HyperFrames plate manifest, and approved reference.

## Concurrency boundary

Parallel workers write isolated proposals and reports. Only the orchestrator mutates shared canonical state. This avoids the shared-mutable-state failure mode while still allowing evidence mapping, transcript segmentation, look development, ticket-scoped asset work, bounded HyperFrames scenes, and independent QA to run concurrently. Direction integration, root composition, canonical Resolve timeline, approvals, and delivery remain single-writer.

## Implementation status

The architecture above is canonical documentation. The scene-direction 1.2.0 schema, semantic validation, and director/build packet compiler implement the bounded picture/audio and direction-facts contract. The rest of the v1 CLI, state machine, `render-data/`, `renderer/`, and runtime tests still describe a Remotion-era greybox prototype. They must be migrated deliberately; no document should claim the bounded scene-direction controls already enforce the complete target architecture.
