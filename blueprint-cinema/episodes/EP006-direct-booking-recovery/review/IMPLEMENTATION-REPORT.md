# Blueprint Cinema implementation report

Generated for the isolated EP006 greenfield foundation on 2026-08-20. This report distinguishes validation, approval, smoke rendering, and later human gates. Nothing was committed, pushed, published, uploaded, purchased, licensed, or generated through a paid media service.

## Outcome and current authority

- Canonical episode identity: number `6`, code `EP006`, slug `direct-booking-recovery`, folder `EP006-direct-booking-recovery`.
- Current production state: `greybox_ready`.
- Next blocked gate: `greybox_approved`; no smoke render or worker packet records that approval.
- Input-lock hash: `e99b847c5b5a767d74ad4208738374ac191da3d9d4c3e3654098a6c08e725691`.
- Approved engine hash: `73b22204a8a19a9a71d420d6aef69218f717cdab804486175f2929922d4af543`.
- Approved world hash: `512c8e4ac1b2648ca9d338a8a25ab2e943fc0890d71250a0c975972c2827823e`.
- Approved visual-plan hash: `1ea1182ec9240d29914666b5b6f8eafc56bd827fd1401f5118c89f4226397407`.
- Approved asset-ticket hash: `1e978e7d1c309852ac7d9ca9ad54c76ca30b856b9584f58bd97d03626b0ebd9c`.
- Hash-bound greybox-data hash: `7d4fec2ed85e9e8d621a210551696e97cd3900f2959a66a4abfd4cc41bfeaa15`.

## Starting branch and dirty worktree

The populated checkout was `/Users/brownmanbrain/GitHub/operator-economy`, not the lightweight `/Users/brownmanbrain/Documents/GitHub/operator-economy` shell in the launch context.

Starting branch:

```text
ep006-rev-e-redesign...origin/ep006-rev-e-redesign [ahead 16]
```

Starting status contained 52 modified and 17 untracked entries outside `blueprint-cinema/`. They included pre-existing repository guidance/docs, legacy EP006 contracts, production state, storyboard JSON and frames, legacy render data, staged VO, the legacy Remotion root, old footage/storyboard utilities, prior pilot/review directories, and untracked old schemas/tests. The entire pre-existing `blueprint-cinema/` scaffold was itself untracked. All 69 outside entries were preserved; none was edited, deleted, moved, renamed, reset, checked out, or overwritten by this pass.

## Files created

All implementation files are under top-level `blueprint-cinema/`:

- Packaging/operator entry: `.gitignore`, `pyproject.toml`, `bin/oe-cinema`.
- Runtime: `src/blueprint_cinema/{__init__,cli,paths,hashes,validation,state,input_lock,render_data,review}.py`.
- Contracts: episode-project, input-lock, episode-engine, world, visual-plan, asset-ticket, production-state, agent-work-order, agent-deliverable, and render-data JSON Schemas.
- Renderer: `renderer/package.json`, `package-lock.json`, `tsconfig.json`, `src/index.ts`, `Root.tsx`, `BlueprintCinema.tsx`, `DeckPrototype.tsx`, `camera.ts`, `types.ts`, `components/DeckObject.tsx`, `components/OverviewMap.tsx`, `components/WorldNode.tsx`, and `components/TicketSlate.tsx`.
- Tests: `conftest.py` plus schema, input-lock, state-machine, engine, world, plan, clean-room, render-data/Remotion, and agent-packet suites.
- EP006 canonical data: `episode.json`, `input-lock.json`, `production-state.json`, `episode-engine.json`, `world.json`, `visual-plan.json`, `asset-tickets.json`, and root-owned `author_visual_plan.py`.
- EP006 agent records: three work orders, three isolated deliverable manifests, and three read-only QA reports.
- EP006 derived/review data: `render-data/greybox.json`, six required review reports, and ignored/generated render outputs.

Generated local-only files are ignored: `.venv/`, Python caches, `renderer/node_modules/`, verified staged VO, representative frames, and whole-review media.

## Pre-existing files touched

Pre-existing files outside `blueprint-cinema/`: **none**.

Intentional scaffold-document updates inside `blueprint-cinema/`: `README.md`, `AGENT-WORKFLOWS.md`, `PORTING-POLICY.md`, `SOURCE-MAP.md`, boundary READMEs in `bin/`, `schemas/`, `renderer/`, `tests/`, and `templates/episode/`, plus the EP006 and agent READMEs. These updates retain the authority rules and replace obsolete documentation-only status statements with the implemented, verified boundary. No scaffold documentation file was deleted or relocated.

## Locked upstream inputs

Every artifact below is repo-relative, size-recorded, and SHA-256 pinned in `input-lock.json`; audio entries also record probed durations.

| Role | Source | SHA-256 | Duration |
|---|---|---|---:|
| approved script | `studio/originate/direct-booking-recovery/script.json` | `15b2f1b3cc1e66488135cd876c6f019bcbb3a08ac425866bffc570de0c3bccf6` | n/a |
| assembled VO | `studio/originate/direct-booking-recovery/vo/full-episode.mp3` | `95e90a1ebb5dfbc6e13bc2efd12915cea9f15807199b0301cd3f63d59cb8e468` | 915.55s |
| hook | `vo/hook.mp3` | `db01e7100574f4b4d0273cf95db1864430a7357432ba08e9e1b1f9e32f497f4c` | 28.13s |
| thesis | `vo/thesis.mp3` | `3d2e0c878a1ba8bfa9ce7cc7c181850079af5f1449476effa6dc6d35336ab241` | 110.69s |
| evidence | `vo/evidence.mp3` | `0d8306b1aaf4c5c45865c83dc4a533011e8c637c3c9f3b1952f0b66b859293f9` | 239.49s |
| stack | `vo/stack.mp3` | `54dd73901f9e6b1caf1b93f6c5626679e4a13f898327f25ff37ff14cfd957db5` | 146.85s |
| playbook | `vo/playbook.mp3` | `25381687fc6c6c65d92623dabeee4fd85ff2a7c7ac3ad2c4bd7da604c477b80b` | 199.09s |
| economics | `vo/economics.mp3` | `7beb05beb203c4719dd25b3e134a56d54278302f2fd1170bb25d8b63222c53ae` | 156.05s |
| CTA | `vo/cta.mp3` | `69d56687be3db28d3f0eb52fa58dbcf1f73bf9b5c8bb275a2a00154531527d13` | 35.25s |
| word transcript | `vo/words.json` | `00151975a93c818fe51dbf83feeb04bc7997bb0d9d8b424f8d1fa2539a927b76` | bounded to VO |
| timeline | `vo/timeline.json` | `fcb9ad96667304544f8bb8d830268bca50ab2cf1f6c6102e9f819e32c6f52b6d` | 915.55s |

The approved-script hash matched the upstream approval record. The 1,922 transcript words, section assembly, and timeline remain within the locked audio. Evidence context used by the persistent world was independently pinned to `research.md` hash `61a1ed53bafa657266c7ad6b27af9069d2a75ad05f885f987776f9d781e6076e` and content-os `facts.md` hash `fd337d4013d5d2d8ed83f1ba02e9e211c1263c5e3e8d5f119ff1bc5c7e5a4309`. The renderer's minimal palette adapts values from `design-system/tokens/colors.css` hash `d4f86fe4e6ae2ebbf500dd51fbb94b1a454a28ad7238e1f8dbce0a36648c4cb2`. The show-identity plate adapts only the canonical typographic structure from `design-system/foundations/brand-wordmark.html` hash `10e202be001c52af53dd28cd57d83933858d3dccdb36c56c574f8441b8fea61b` and the `Build. Own. Operate.` wording from `brand-tagline.html` hash `8741586b3e6960a646f588787bff198979f146a663efc58ce9b7f6c5767bd799`; no logo icon exists in that contract, and no legacy component, animation, or layout rule was consumed.

## Explicit clean-room exclusions

Not read as visual input, imported, referenced by episode configuration, or compiled into render data: `storyboard.json`, `coverage_map.json`, `render_data/blueprint.json`, storyboard frames/review boards, `build_rev_e_storyboard.py`, `OEOpeningPilot.tsx`, Resolve pilots, prior full renders, old scene assignments, prior coverage/asset decisions, old visual approvals, and the legacy 141-screen plan. No stock search, automatic first-result choice, polished asset, AI render, final music, transition, or generated interface/evidence work began.

The one old EP006 episode-engine proposal was consulted only as explicitly authorized source material. Its approval was not inherited; the greenfield engine was revised, validated, independently critiqued, and approved under a new hash.

## Agent work and serial synthesis

Three bounded workers ran concurrently in disjoint deliverable directories. All work orders were validated before dispatch; all packets are schema-valid, use their historical declared hashes, claim no approval, and report no production-state change.

- `engine-honesty-critique`: accepted as review evidence. It found the engine mechanically honest and required affirmative consent—not merely a request—before memory/outreach, plus mandatory human judgment on every outbound route. Root integrated those conditions into plan semantics and tests.
- `world-integrity-review`: packet accepted, but its verdict rejected the reviewed world hash for approval. Root added real failure edges, hash-pinned evidence sources and registries, corrected spatial/camera ambiguity, revalidated the complete world, and approved the corrected current hash.
- `visual-plan-qa`: packet accepted, but its verdict rejected the reviewed 138-unit plan hash for approval. It found early outbound/value activation, memory before consent, missing proof tickets, unexecuted failure definitions, the wrong opening proof, and ambiguous cameras. Root serially rebuilt the plan to 162 explicit actions, added exact proof tickets, declared sequence/camera semantics, enforced accumulated gate preconditions, ran configured failure routes, then revalidated and approved the complete timeline across all boundaries.

No packet was schema-rejected, no worker wrote a canonical artifact, and no worker advanced a gate. No serial fallback was required because all three bounded workers completed. Root integration and approvals were serial.

## Commands implemented

`oe-cinema` implements:

```text
init
status
lock-inputs
validate-engine
approve-engine
validate-world
approve-world
validate-plan
approve-plan
build-greybox-data
smoke-render
validate-work-order
validate-deliverable
work-status
review
test
```

Every episode command prints the resolved identity/path, returns nonzero on validation failure, names the blocking gate, and refuses to repair authored creative data. Approval commands record the exact covered hashes; status detects staleness; regenerated upstream artifacts invalidate dependent approvals; issued worker hashes must be current; completed historical packets remain auditable but cannot be used to advance state.

## Validation and render results

- `npm run typecheck`: pass.
- `blueprint-cinema/.venv/bin/python -m pytest blueprint-cinema/tests -q`: **39 passed**.
- `blueprint-cinema/bin/oe-cinema validate-plan EP006-direct-booking-recovery`: pass; 162 units, exact 0.000-915.550s coverage, all 1,922 words exactly once, no unintended gap/overlap.
- `blueprint-cinema/bin/oe-cinema work-status EP006-direct-booking-recovery`: all three orders and packets valid; no gate advanced by a packet.
- `blueprint-cinema/bin/oe-cinema smoke-render EP006-direct-booking-recovery`: pass; representative focus frame rendered from approved render data and hash-verified staged VO.
- Overview-to-focus regression: pass. Separate overview and focus frames render with different hashes, and a source-contract test confirms the camera uses authored `focus` IDs and `camera_anchor` data without narration routing.
- Whole-episode low-resolution map-camera render: **technically passed, creatively rejected**. Remotion rendered all 27,467 frames, but operator review found that the complete moving network map was not understandable enough to approve. It remains preserved as a diagnostic, not the current direction. `ffprobe` reports H.264, 960x540, 30 fps, AAC stereo at 48 kHz, 915.605333 seconds, and 61,507,359 bytes. SHA-256: `adb0777cc9693f1ed3830c9da45d2cbb0aa26815122fa721e9ce91b0f23b66de`.
- Deck-style opening regression: pass. Five distinct slide states render with stable guest/stay, OTA, and hotel IDs plus explicit show-identity and episode-title bookends; the deck source contains no complete network-map rendering or overview component. Eight representative frames were visually checked across the stay, OTA introduction, leak, show identity, episode title, audit, guarded second-booking route, and fragmented handoffs.
- Revised 90-second deck-style review render: **pass**. `BlueprintCinemaDeckPrototype` rendered all 2,700 frames with the locked opening narration. `ffprobe` reports H.264, 960x540, 30 fps, AAC stereo at 48 kHz, 90.048 seconds, and 4,598,932 bytes. SHA-256: `0665fc2261723b5587a6e3babc765b62c61e84fdc7297109c4e5660d1b751048`. The prior no-bookend deck render remains preserved at its original path and is superseded for review.

The current creative candidate is the revised 90-second deck prototype. It presents the guest/stay, OTA, hotel, commission, broken relationship, and guarded direct route as large slide elements whose relationships change over time. At the current approved VO handoff, it cuts to **The Operator Economy** identity from 27.733-32.558 seconds, then **EP006 - Direct Booking Recovery** from 32.558-40.090 seconds before returning to the operating story. The approved persistent world remains the hidden integrity model; the viewer is no longer asked to decode it as a full map.

The representative frames are intentionally plain structural review artifacts. They are not an approved greybox, polished frames, a production master, or release assets.

## Remaining blocker and exact next command

The runtime remains at `greybox_ready`. The full map-camera direction was explicitly rejected for comprehension, and the new 90-second deck visual language has been rendered but not yet accepted for extension across the episode. Eleven tickets remain placeholders and no asset may be sourced from them until the applicable greybox review decision.

Exact next operator command:

```bash
open blueprint-cinema/episodes/EP006-direct-booking-recovery/delivery/generated/EP006-greybox-deck-brand-title-prototype.mp4
```

Inspect `review/DECK-PROTOTYPE-REVIEW.md` and the ignored 90-second deck MP4. Do not edit `production-state.json` manually or claim `greybox_approved` from a prototype render.

## 90-second runtime-comparison addendum

After the deck prototype, the operator requested a same-window HyperFrames/Remotion test. The isolated native HyperFrames candidate was implemented under `experiments/EP006-90s-runtime-comparison/hyperframes/` using the exact locked 0-90 second narration. It does not port the Remotion scene tree, consult legacy visuals, or alter canonical Blueprint Cinema data.

Nine hash-pinned frame work orders ran in three waves and were integrated serially by root. All nine packets validated; none claimed approval or a production-state change. HyperFrames lint and full checks pass, 11 representative snapshots were visually inspected, and the full 2,700-frame candidate rendered at 1920x1080. The generated MP4 is exactly 90.000 seconds with H.264 video and AAC stereo audio, 10,094,247 bytes, SHA-256 `4eb40bfc8a264150035963830a0b5ef96999447656eb1045a3f2b6eba1163b81`. The matched visual sheet and full decision record are in `review/HYPERFRAMES-REMOTION-90S-COMPARISON.md`.

The broader Blueprint Cinema suite now reports **43 passed**, and the existing Remotion renderer TypeScript check still passes. The HyperFrames treatment is the stronger look-and-feel candidate, but neither opening render is a greybox approval, canonical renderer migration, full-episode implementation, production master, or release asset. State remains `greybox_ready`; the blocking gate remains `greybox_approved`.
