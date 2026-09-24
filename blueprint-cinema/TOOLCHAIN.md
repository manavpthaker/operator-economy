# Blueprint Cinema canonical toolchain

## Decision

Blueprint Cinema is the creative and production authority. HyperFrames is the canonical designed-scene, motion-graphics, animatic, and deterministic-render runtime. DaVinci Resolve is the canonical final editorial and finishing environment.

```text
BLUEPRINT CINEMA                         HYPERFRAMES                         DAVINCI RESOLVE

truth and continuity                    visual implementation               final timeline
direction bible                         shot compositions                   footage conform
rhythm map                              deterministic motion                editorial refinement
scene directions          ->            directed animatic       ->          color correction and grade
asset and edit contracts                graphic and alpha plates            Fusion finishing
approval hashes                         review renders                      Fairlight mix
rights and disclosure                   snapshots and checks                captions and delivery masters
```

Remotion is no longer an authorized implementation target for new Blueprint Cinema work. The existing Remotion project and renders remain preserved as historical prototypes and diagnostic evidence. Do not delete, port incrementally, or continue polishing them unless an explicit archival-reproduction task requires it.

This is a documentation-canonical target. The current Blueprint Cinema v1 CLI and state schema still contain Remotion-era greybox paths and do not yet enforce this toolchain. Until the runtime migration is implemented and validated, report the new workflow as **specified**, not implemented.

## Why HyperFrames is the primary runtime

HyperFrames fits the OE production model because it provides:

- CLI-first HTML compositions that are inspectable and editable as files;
- modular sub-compositions for shot- and sequence-bounded ownership;
- deterministic, seekable animation driven from time rather than playback state;
- one paused timeline per composition;
- local lint, runtime, layout, motion, contrast, snapshot, preview, and render gates;
- a storyboard and sketch review surface;
- direct support for video, audio, captions, variables, and reusable media;
- MP4 review renders, MOV or WebM transparency, and RGBA PNG sequences for post-production handoff;
- isolated scene packets that can be assigned to bounded workers without sharing one mutable timeline;
- a thin root composition that can carry the locked narration and mount independently authored scenes.

The choice does not claim that HyperFrames automatically creates better direction. The failed Remotion prototypes were primarily failures of direction, composition, and editorial hierarchy rather than React. HyperFrames becomes useful only after the direction bible, rhythm map, scene direction, and shot board have been approved.

## Known HyperFrames risks and safeguards

HyperFrames is a newer runtime than Remotion. The production system therefore requires the following safeguards:

1. Pin the HyperFrames version in each episode project. Never let an episode silently move to a newer version.
2. Run the read-only upgrade check before the first render-affecting command in a resumed project.
3. Upgrade only when the project still passes `hyperframes check`; record the old and new versions.
4. Use a short representative motion test before directing a complete long-form episode.
5. Run a full-duration low-complexity render test before polished asset production to expose memory, browser, media, and duration problems.
6. Keep all required fonts and media local. No render-time network requests are allowed.
7. Use modular sub-compositions. A long episode must not become one enormous HTML file or one enormous animation timeline.
8. Keep the narration and episode-level audio at the root so it remains continuous across scene mounts.
9. Require midpoint snapshots for every scene and an animation-map review for the assembled episode.
10. Preserve the approved full-timeline animatic as the conform reference even after final plates are rendered.

HyperFrames requires Node.js 22 or newer and FFmpeg. The episode project records both versions before production. Use the local project pin for production commands. On resume, inspect availability with `npx hyperframes@latest upgrade --project . --check`; any accepted upgrade is explicit, recorded, followed by `npx hyperframes check`, and visually compared at representative frames before work continues.

If HyperFrames cannot render the approved full-duration animatic reproducibly, stop at the runtime gate. Do not quietly fall back to Remotion or redesign the episode to fit a renderer limitation. The operator decides whether to repair, split, preprocess, or authorize a fallback.

## OE authority over framework defaults

HyperFrames is an execution framework, not the OE creative director. The following Blueprint Cinema rules override any generic framework guidance:

- one readable primary priority is required; a second focal point is optional, not mandatory;
- stillness is permitted and often preferred after a meaningful reveal;
- decorative elements do not receive ambient motion by default;
- motion exists to express an operation, state change, relationship, camera motivation, or editorial emphasis;
- the default transition is a cut;
- backgrounds do not need glows, gradients, drifting objects, or texture merely to appear produced;
- typography labels, proves, or lands a genuine thesis; it does not repeat narration;
- scene density is determined by comprehension and the approved visual language, not a generic element-count target;
- evidence and documentary material retain their source context even when HyperFrames can stylize them;
- AI-rendered plates are never evidence;
- every shot declares its picture/audio mode before camera and coverage are designed;
- scene context and authored editorial intent choose coverage and cut/hold timing; narration alone does not select observational grammar. Explicit narrated dramatization allows illustrative interaction with narration-carried meaning, disclosure, and audiovisual review. Observation retains its no-speech/missing-line rules. Source, sync, and presenter delivery remain bound to their synchronized audible modes;
- every shot carries generator-independent, non-optional direction facts: what stays still, master/setup relationship and exact reference, action line and screen direction, typed continuity anchors, and initial and final images;
- the OE design system and episode direction bible override HyperFrames presets, palettes, typography defaults, motion recommendations, and house style.

## Canonical HyperFrames route

OE long-form episodes use the HyperFrames `general-video` workflow because they are long, custom, multi-scene compositions. The `faceless-explainer` workflow can supply useful story, shot, and invented-visual methods, but it is not the owning workflow for an episode that substantially exceeds its short-form operating range.

Before any HyperFrames production task:

1. Read the installed `/hyperframes` entry skill.
2. Read `/general-video` and the required domain skills for the assigned work.
3. Read the episode's approved Blueprint Cinema inputs.
4. Treat the Blueprint Cinema direction bible and scene directions as higher authority than generic HyperFrames creative guidance.
5. Use `/media-use` for every asset, grade, LUT, audio, caption, or media-operation requirement.
6. Use `/hyperframes-keyframes` before camera, zoom, pan, crop, reframe, or other keyframe work.
7. Use `/hyperframes-audio` for placed-track gain, carve, ducking, automation, and effects.
8. Use `/hyperframes-cli` for lint, check, snapshots, preview, and render.

When an approved shot needs a motion primitive, search the local registry by the intended visual action with `npx hyperframes catalog --query "<approved move>"` before hand-authoring it. Installing a primitive never authorizes a new movement, layout, or surface style; the primitive must implement the approved direction and pass the episode checks.

## HyperFrames project contract

Each episode receives one canonical project under:

```text
episodes/EP###-slug/hyperframes/
├── BRIEF.md
├── frame.md
├── STORYBOARD.md
├── hyperframes.json
├── package.json
├── index.html
├── compositions/
│   ├── sequences/
│   └── shared/
├── public/
│   ├── audio/
│   ├── media/
│   ├── fonts/
│   └── generated/
├── snapshots/
└── renders/
```

Responsibilities:

- `BRIEF.md` binds the HyperFrames project to the approved Blueprint Cinema episode, scope, and workflow. It is not a substitute for the episode engine or direction bible.
- `frame.md` is the renderer-facing translation of the OE design system plus the approved episode visual language.
- `STORYBOARD.md` is the scene dispatch and review index. It does not replace `visual-plan.json` or `scene-directions.json`.
- `index.html` is a thin episode orchestrator: timing slots, root audio, captions, and episode-level tracks.
- `compositions/sequences/` contains bounded sequence or shot compositions. Shared objects live in `compositions/shared/` only when they preserve approved identity and state.
- `public/` contains frozen local media referenced by manifest ID. Raw URLs and untracked downloads are forbidden.
- `snapshots/` and `renders/` are generated review evidence, not approvals by themselves.

Composition IDs, shot IDs, sequence IDs, asset IDs, and evidence IDs must remain traceable across Blueprint Cinema, HyperFrames, and Resolve.

## HyperFrames review and render ladder

Use the cheapest artifact capable of answering the current question:

| Artifact | Question | Typical output |
|---|---|---|
| Static shot board | Is composition and hierarchy correct? | entry, action, and exit PNGs |
| Motion test | Is the episode visual language correct? | one representative 20-30 second sequence |
| Directed animatic | Does the whole episode work against the locked VO? | full-length draft MP4 |
| Rough visual render | Do selected media and graphics work together? | full-length review MP4 |
| Graphic plate | Can Resolve conform the designed layer at full quality? | MOV with transparency or RGBA PNG sequence |
| Opaque scene plate | Is the scene self-contained and picture-complete? | high-quality MOV |
| Conform reference | Does Resolve reproduce the approved timing? | full-length reference MP4 with IDs/timecode as needed |

Required HyperFrames verification before a handoff:

1. `npx hyperframes lint` during authoring after the first HTML pass and structural changes.
2. `npx hyperframes check` as the final automated gate; it reruns lint, so do not run a redundant lint immediately before it.
3. midpoint snapshots for every mounted sequence or shot composition;
4. first-action-exit snapshots for complex or high-risk scenes;
5. animation-map review for the assembled multi-scene episode;
6. final Studio preview with `npx hyperframes preview --background` after checks pass;
7. explicit approval before render;
8. a recorded render command and quality target, normally `npx hyperframes render --quality high --output <path>` for a final local handoff;
9. media probe of every rendered handoff for duration, dimensions, frame rate, streams, and alpha expectation;
10. source-hash and tool-version recording in the handoff manifest.

## DaVinci Resolve role

DaVinci Resolve owns the final post-production timeline. Resolve Studio is preferred when the licensed workflow needs its external-scripting or Studio-only finishing capabilities, but the project must probe the installed edition and supported features before relying on them. The application is not a second source of visual logic and it must not become an undocumented alternate edit.

Resolve owns:

- ingest and relink of approved selected media;
- conform of the approved animatic and edit plan;
- B-roll and archival source in/out points;
- editorial trims that do not change the approved meaning;
- assembly of HyperFrames opaque and alpha plates;
- Fusion cleanup, masks, tracking, paint, and final composites when needed;
- primary correction, shot matching, and creative color grade;
- Fairlight dialogue treatment, ambience, music, SFX, automation, mix, and loudness verification;
- caption placement and delivery-format preparation;
- final titles or legal/disclosure slates already authorized by Blueprint Cinema;
- review exports, mezzanine masters, upload masters, and archival packages.

Resolve does not own:

- research, facts, claims, or narration wording;
- episode engine or persistent-world logic;
- unapproved scene redesign;
- regenerated evidence;
- untracked stock, archival, music, or AI media;
- new synthetic scenes without tickets and disclosure;
- silent timing changes that detach graphics or evidence from the locked VO;
- publication status or canonical episode URLs.

## Resolve interoperability contract

The canonical handoff package is:

```text
edit/handoff/<version>/
├── manifest.json
├── reference/
│   └── directed-animatic-reference.mp4
├── interchange/
│   ├── timeline.otio
│   ├── timeline.fcpxml
│   └── markers.csv
├── plates/
│   ├── opaque/
│   └── alpha/
├── media/
│   ├── selects/
│   └── proxies/
├── audio/
│   ├── vo/
│   ├── music/
│   ├── sfx/
│   └── ambience/
├── captions/
├── color/
└── reports/
```

The handoff may omit a format only when the receiving Resolve workflow does not require it. `manifest.json` always exists and records what is present.

The locally inspected Resolve 21 developer documentation exposes Python and Lua scripting, command-line invocation while Resolve is running, headless `-nogui` operation, timeline import including AAF, EDL, XML, FCPXML, DRT, ADL, and OTIO, media-pool operations, markers, render settings, render jobs, project export, and delivery automation. Some external-scripting and finishing capabilities can depend on edition, operating mode, or configuration, so the handoff must probe them before use. Automate only deterministic assembly and reporting. Creative editorial, color, and mix judgments still require review.

## Round-trip rule

Resolve may refine the approved edit, but every meaningful deviation must be returned to Blueprint Cinema.

Classify changes as:

| Change | Resolve action | Blueprint Cinema consequence |
|---|---|---|
| Color, cleanup, mix, or sub-frame polish with unchanged meaning and timing | proceed and record | finishing manifest update only |
| Small trim inside available handles with unchanged word, claim, and state alignment | proceed provisionally | update edit manifest before approval |
| Shot order, shot purpose, evidence timing, business state, object continuity, or transition meaning changes | stop and propose | revise scene direction and invalidate dependent approval |
| Script or VO timing changes | stop | return upstream; rebuild every timing-bound artifact |
| New source, new claim, new synthetic media, or changed rights status | stop | create or revise ticket, provenance, evidence, and disclosure records |

The Resolve project is never the only record of an approved change. Picture lock means the Blueprint Cinema edit manifest, Resolve timeline, HyperFrames plate manifest, and approved reference render agree.

## Color-management and finishing rules

- Record the source color space, transfer function, bit depth, and alpha handling for every plate and selected clip when known.
- Choose one Resolve color-management strategy for the episode and record it in the finishing manifest.
- Normalize mixed footage before applying the creative grade.
- Preserve factual color when color itself is evidentiary or operationally meaningful.
- Match AI plates, stock, archival, original capture, and graphics into one episode world without disguising their provenance.
- Do not apply a generic LUT as a substitute for correction, matching, and intent.
- Check titles, sources, fine lines, grids, and accent colors after final encoding; motion-design frames can break under compression even when the grade is correct.
- Color approval uses a calibrated or documented review environment when available and must state its limits when it is not.

## Audio finishing rules

- Locked narration remains the authority.
- Use a dialogue-first Fairlight mix.
- Music and ambience support structure and continuity without masking narration.
- Use spectral and/or level carving when a bed competes with the voice; do not solve every conflict with global attenuation.
- Sound effects clarify operations and important transitions. Do not sonify every animation.
- Record the final loudness, true peak, channel layout, sample rate, and export settings in the delivery report rather than relying on an undocumented preset.
- Listen to the rendered master, not only the Resolve timeline.

## Canonical delivery outputs

At minimum, final delivery includes:

- a Resolve project archive or project export stored outside Git with a tracked manifest;
- an approved picture-lock reference;
- a high-quality mezzanine master;
- a platform upload master;
- caption deliverables;
- final audio or stems when required;
- provenance, rights, synthetic-media, and reconstruction records;
- a media-probe report;
- a final QC report;
- the source hashes and tool versions that produced the master.

No render, Resolve timeline, or delivery file changes publication state. The validated master returns to the existing OE packaging, upload, `links.json`, and content-os release gates.
