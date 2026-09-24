# Source map

This file records source authority and actual reuse. A row marked implemented identifies the adapter or reference boundary and the verification that was executed; rows do not transfer visual decisions or legacy approvals.

## Authority map

| Source | Role | Mode | Current status |
|---|---|---|---|
| `../AGENTS.md` | OE repository boundaries and existing pipeline context | reference | read; applies |
| `../../content-os/CLAUDE.md` | truth, voice, flow, rubric, and release precedence | reference | read; applies |
| `../../content-os/facts.md` | public factual ledger | reference at public-output gates | authority retained upstream; no rules duplicated |
| `../../content-os/voice.md` | voice checks | subprocess or reference at review | authority retained upstream; no rules duplicated |
| `../../content-os/rubric.md` | editorial scoring | subprocess or reference at review | authority retained upstream; no rules duplicated |
| `../../content-os/flow.md` | downstream release sequence | reference | authority retained upstream; no release behavior imported |
| `../docs/blueprint-cinema.md` | canonical visual-production direction | reference | read; applies |
| `../docs/blueprint-cinema-migration.md` | migration decision and exclusions | reference | read; applies |
| `TOOLCHAIN.md` | canonical HyperFrames and Resolve ownership, handoff, and fallback rules | authority | documentation canonical; runtime enforcement not yet implemented |
| `PRODUCTION-TEAM.md` | department roles, review independence, parallel waves, and decision ownership | authority | documentation canonical; applies to human and agent work |
| `../design-system/README.md` | design-system authority map | reference | read; applies |
| `../design-system/boundary-ledger/{semantic-core.json,bindings/}` | cross-media semantic roles plus color, motion, and sound expression bindings | authority input | future episode `frame.md` files freeze the exact core and binding hashes, then derive treatment without importing the web layout; root Rev C tokens remain v1 compatibility input only |
| `../design-system/foundations/brand-wordmark.html` | canonical show identity contract | reference/adapted structure | confirms that no separate logo icon exists; the deck prototype uses the authorized stacked typographic wordmark and does not invent a symbol; remote font fetching remains excluded from the deterministic greybox |
| `../design-system/foundations/brand-tagline.html` | canonical identity tagline | reference | `Build. Own. Operate.` may appear only on the show identity plate; no layout component or animation was copied |
| `../site/public/fonts/{boska-700,supreme-400,supreme-500}.woff2` | canonical local OE font binaries already shipped by the repository | verified local staging input | the isolated HyperFrames experiment stages these exact local files for deterministic headless rendering; no remote font fetch, new license, or substituted typeface |
| installed HyperFrames skills including `hyperframes`, `general-video`, `hyperframes-core`, `hyperframes-creative`, `hyperframes-animation`, `hyperframes-cli`, `hyperframes-keyframes`, `hyperframes-audio`, and `media-use` | current authoring, composition, media, audio, camera, validation, render, and handoff contracts | installed tool reference | selected as the canonical execution framework; Blueprint Cinema direction overrides generic creative defaults; skills never become episode inputs, approvals, or gate writers |
| `calesthio/OpenMontage@08e2151fa02de28a5d6a312b3d575692bf147ad7` — `skills/pipelines/documentary-montage/{scene-director,edit-director,compose-director}.md` | concrete visual slots, semantic clip selection and trimming, edit rhythm, restrained transition vocabulary | pinned reference only | repository declares AGPL-3.0; no code, templates, runtime, or prose copied; OE contracts override its montage defaults |
| `smixs/visual-skills@3c554715b5eb30f54de78fac3c0df4a7105e4955` — `video/{SKILL.md,references/dramaturgy.md,references/universal-rules.md,references/role-modes.md}` | shot function, motivated camera, physical micro-action, environmental pressure, final-image discipline | pinned attributed reference only | CC BY 4.0; attribution retained to Serge Shima; dramatic escalation, dialogue assumptions, and genre treatment are not OE defaults |
| `billpar/ai-cinematic-pipeline@ed7e28652214b4f3b7fd147e2980596f02b8e2ca` — `docs/03-prompt-writing-guide.md`, `templates/prompt-template.md` | translate narrative meaning into physical blocking, keep voiceover out of generation prompts, and specify observable performance | pinned reference only | MIT; no project runtime or generation workflow imported; its dialogue coverage example does not govern narrated observation |
| `Nagacash/narrative-film-direction@4ee8b42484cb57407f4a7772216aa79e20b0971f` — `skills/narrative-film-direction/{SKILL.md,references/coverage-protocol.md,references/screen-direction.md,references/editing-grammar.md,references/shot-grammar.md}` | master geography, setup derivation, action line, screen direction, one-action clips, assembly-before-finish | pinned attributed reference only | code MIT and documentation CC BY 4.0; attribution retained to Naga Codex / Maurice Holda; five-setup coverage is not mandatory; context-selected interaction coverage may serve explicit narrated dramatization or synchronized dialogue under the separate OE safeguards |
| DaVinci Resolve 21.0.4 and its installed Developer Scripting documentation | supported timeline interchange, media-pool, markers, scripting, project export, render jobs, and delivery automation | installed application reference | inspected locally on 2026-08-20; Resolve selected as canonical final edit and finish environment; creative approval remains in Blueprint Cinema |
| `../studio/originate/<slug>/research.md` | episode research and evidence context | reference | consulted only for claim/evidence context; not used as visual routing input |
| `../studio/originate/<slug>/script.json` | approved narration and claim relationships | input lock | hash-pinned; narration remains upstream-owned |
| `../studio/originate/<slug>/script_review.md` | script gate evidence | input/reference | approval evidence inspected; not duplicated as a Blueprint Cinema gate |
| `../studio/originate/<slug>/vo/full-episode.mp3` | final timing spine | input lock and ignored staging | hash-pinned; copied locally only after verification |
| `../studio/originate/<slug>/vo/*.mp3` | mastered sections named by `vo/timeline.json` | input lock | exact seven timeline members only; raw, legacy, and backup audio excluded |
| `../studio/originate/<slug>/vo/words.json` | word-level timing | input lock | hash-pinned and timing-bounded against locked full VO |
| `../studio/originate/<slug>/vo/timeline.json` | section/timeline timing | input lock | hash-pinned and semantically checked for contiguous section assembly |
| `../studio/originate/<slug>/production_state.json` | upstream approved-script hash evidence only | narrow reference | only `script_sha256` is read; never imported as Blueprint Cinema state |
| `../studio/schemas/episode-engine.schema.json` | early engine-schema prototype | source material | inspected but not copied; superseded by the strict greenfield schema |
| `../studio/originate/direct-booking-recovery/blueprint-cinema/03-visual-plan/episode-engine.json` | EP006 engine proposal | source material, not approved input | read once as requested; revised into a new greenfield engine after lock; no approval inherited |

## Prohibited visual sources

The runtime, episode configuration, work orders, and agent deliverables must not reference:

- legacy storyboard or coverage JSON;
- legacy render data;
- storyboard frames or review HTML;
- legacy storyboard builders or automatic layout routers;
- prior Remotion/Resolve opening pilots and renders;
- prior visual approvals or old asset-to-beat assignments.

The clean-room test must inspect both configured paths and compiled provenance.

## Utility-adoption ledger

Add one row before reusing any existing utility:

| New module | Source path | Reuse mode | Why valid | Legacy dependencies removed | Tests | Status |
|---|---|---|---|---|---|---|
| `src/blueprint_cinema/hashes.py` | Python standard library `hashlib` | adapter | deterministic streaming SHA-256 has no legacy visual coupling | all legacy pipeline and state dependencies | stable/changed hash, lock, state, and renderer-pin tests | implemented and passing |
| `src/blueprint_cinema/input_lock.py` | system `ffprobe` executable | wrapper | duration probing is a media fact independent of storyboard logic | legacy media selection, staging, and render preparation | audio duration, transcript bounds, section continuity, and staged-hash tests | implemented and passing |
| `renderer/package.json` | `../studio/remotion/package.json` version fields only | historical reference | kept a compatible Remotion toolchain without importing scene code | all legacy React components, props, layouts, pilots, and public assets | TypeScript check and representative Remotion frame render | v1 implemented and passing; superseded for new work |
| `renderer/src/BlueprintCinema.tsx`, `renderer/src/camera.ts`, and `renderer/src/components/OverviewMap.tsx` | `../design-system/tokens/colors.css` semantic color values | historical adapted values | the v1 prototype tested minimal orientation colors and overview-to-focus camera behavior | design-system components, screen templates, decorative behaviors, narration routing, and all legacy camera/layout decisions | renderer typecheck, source clean-room scan, authored-focus contract test, distinct overview/focus frames, and whole-episode camera render | v1 implemented and passing; creatively rejected and superseded |
| `renderer/src/DeckPrototype.tsx` and `renderer/src/components/DeckObject.tsx` | greenfield v1 implementation over approved Blueprint Cinema IDs, with wordmark/tagline structure adapted from the listed design-system foundations | historical prototype | tested stable objects and VO-timed identity/title bookends | complete world-map display, narration parsing, legacy templates, platform UI, invented marks, third-party logos, remote fonts, and fake evidence | typecheck, source-contract assertions, five frames, and 90-second review render | v1 implemented; creatively rejected and superseded |
| `experiments/EP006-90s-runtime-comparison/hyperframes/` | approved v1 greybox data, locked first 90 seconds of VO, OE tokens, and local OE fonts | runtime-evaluation candidate only | proved local HyperFrames lint, check, snapshot, preview, and 90-second render viability; its composition and short-form workflow do not define production direction | Remotion translation, full-episode plan changes, legacy visual inputs, network media, third-party UI, generated VO/BGM, canonical JSON, approvals, and state mutation | HyperFrames lint/check/snapshots/preview, 90-second render, matching media probe, and time-matched review | preserved experiment; not a canonical composition, visual language, or production project |
| `src/blueprint_cinema/render_data.py` | new greenfield implementation | original | compiler is defined entirely by approved Blueprint Cinema artifacts | `prepare_longform.py`, `render_data/blueprint.json`, narration routing, and legacy scene assignments | deterministic equality, approval-pin, schema, and clean-room tests | implemented and passing |
| `src/blueprint_cinema/scene_prompts.py` and `schemas/scene-directions.schema.json` | new greenfield implementation | original | separates shot direction from implementation while binding both to locked words, approved world IDs, evidence, tickets, hashes, a narration-aware picture/audio contract, and adjacent generator-independent direction facts | narration-based layout inference, unclassified dialogue grammar under VO, legacy storyboard decisions, generic style prompts, unbound master/setup geography, unbounded builder discretion, and automatic media generation | deterministic director packets, strict schema validation, six picture/audio modes, required authored context and editorial intent, illustrative dramatization safeguards, mode-bound source/sync/presenter delivery, observation-mode dialogue rejection, required direction facts, setup-reference integrity and resolvable-anchor checks, exact cue rejection, and shot-build packet compilation | implemented and tested; does not advance production state |

## External references

Creative inspirations and the four pinned film-direction method inputs are cataloged in `references/CREATIVE-REFERENCE-STACK.md`. They are behaviors to study, not templates, assets, runtimes, or substitute authorities. Exact local file hashes belong in the OE skills source lock; this map records repository identity, source path, reuse boundary, attribution, and license.
