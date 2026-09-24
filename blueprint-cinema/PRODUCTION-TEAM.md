# Blueprint Cinema production team operating model

## Purpose

Blueprint Cinema is designed to behave like a coordinated documentary, design, animation, editorial, and post-production team even when many roles are performed by agents or by one operator at different times.

A role is a decision boundary, not necessarily a separate person. One person or agent may perform several roles, but the artifacts, approvals, and conflicts of interest remain distinct. Nobody approves their own work merely because the team is small.

## Leadership and authority

### Showrunner / executive producer

Owns:

- the viewer promise;
- episode scope;
- audience and commercial purpose;
- the final creative decision when valid options remain;
- explicit approval at human gates;
- expansion of budget, licensing, paid generation, or delivery scope.

Does not:

- rewrite verified facts from memory;
- bypass evidence, rights, or disclosure gates;
- treat a render as approved merely because it looks polished.

### Blueprint Cinema orchestrator / post supervisor

Owns:

- canonical paths, identity, hashes, state, manifests, and approvals;
- work orders and output ownership;
- validation and merge decisions;
- the production schedule and dependency graph;
- the HyperFrames-to-Resolve handoff;
- the final production report.

The orchestrator is the only writer to shared canonical state during coordinated work. It does not substitute orchestration authority for creative expertise; it requests and reconciles the appropriate role's recommendation.

## Editorial and directing roles

### Editorial producer

Owns the downstream interpretation of the locked script and VO:

- narrative waveform;
- sequence purpose;
- viewer knowledge before and after each sequence;
- pacing pressure, breathers, callbacks, reversals, and payoff;
- deciding when several narration units belong in one scene;
- identifying narration that cannot be visualized honestly from approved inputs.

The editorial producer cannot change script wording or claim meaning inside Blueprint Cinema.

### Creative director

Owns:

- the episode direction bible;
- the visual thesis;
- episode-specific reality, system, proof, and outcome treatments;
- visual cohesion across departments;
- the look-development brief;
- approval recommendation for style frames and the representative motion test;
- resolution of conflicts between art direction, motion, footage, evidence, and post.

The creative director establishes the ceiling. Builders implement within that ceiling; they do not rediscover it shot by shot.

### Documentary director

Owns:

- human and physical reality;
- the meaning of B-roll and archival coverage;
- truthful representation of people, places, processes, and market context;
- shot purpose, framing, screen direction, and editorial handles for real footage;
- distinguishing observation, reconstruction, metaphor, and proof;
- avoiding generic stock and synthetic documentary theater.

### Visual / motion director

Owns:

- sequence treatments and shot grammar;
- the relationship among frame composition, motion, camera, and VO;
- entry, action, consequence, settle, and handoff states;
- motivated transitions;
- the motion-language and intensity system;
- the scene-direction artifact and review recommendation.

The motion director does not write implementation code while still deciding the shot. Direction and build are separate passes.

### Evidence editor

Owns:

- source-to-claim mapping inside the film;
- exact evidence locator and display context;
- source, highlight, extract, attach, parameter-change choreography;
- legibility and attribution requirements;
- reconstruction labels;
- rejection of synthetic or fabricated proof.

The evidence editor can block a beautiful scene that misstates, overstates, obscures, or detaches a source from its claim.

## Design and image roles

### Production designer

Owns the episode world as a designed environment:

- spatial rules;
- recurring objects and their material treatment;
- persistent zones and scale relationships;
- the relationship of reality and system worlds;
- environmental continuity;
- what the world looks like before animation.

### Art director

Owns:

- application of the OE design system to the episode;
- palette roles, typography roles, surface, texture, contrast, depth, and graphic detail;
- style frames;
- graphic asset quality;
- cross-scene design adherence;
- eliminating generic AI, web-page, presentation, and template-pack aesthetics.

### Storyboard and animatic artist

Owns:

- the shot board with real text and truthful placeholder geometry;
- entry, key-action, consequence, and exit frames;
- shot-to-shot spatial continuity;
- the directed animatic's readable construction;
- exposing composition problems before finish work.

### Information designer

Owns:

- diagrams, flows, routes, decision gates, variables, charts, and operational labels;
- visible causal structure;
- cognitive-load control;
- truthful comparisons and data scales;
- making a blueprint actionable rather than merely attractive.

### Typography director

Owns:

- type hierarchy and role application;
- exact text, line behavior, emphasis, and reading time;
- source-label legibility;
- number treatment;
- title, identity, caption, and annotation collision avoidance;
- typography integrity after render and compression.

### AI plate director

Owns only ticketed non-evidentiary synthetic material:

- character and environment continuity;
- shot prompt compilation from approved direction;
- camera, lens, lighting, action, and screen-direction instructions;
- reference images, seeds, model/version metadata, and negative constraints when supported;
- generation review and rejection;
- synthetic status and disclosure metadata;
- clean plates for later factual compositing.

The AI plate director never generates evidence, interfaces, branded documents, public figures, factual prices, or synthetic people presented as real participants.

## Asset and production roles

### Archival and footage producer

Owns:

- searches derived from ticket semantics rather than narration keywords;
- candidate logs;
- rights holder, license, check date, download date, releases, restrictions, and provenance;
- exact source in/out points and handles;
- recommendation of selects and alternatives;
- rejection reasons.

### Original-capture producer

Owns:

- capture briefs;
- accurate interface, document, process, and object capture;
- privacy and credential hygiene;
- repeatable recording settings;
- clean plates and handles;
- capture logs and checksums.

### Media manager / assistant editor

Owns:

- asset IDs, filenames, checksums, proxies, relinking, and folder consistency;
- source/select/use status;
- frame rate, duration, resolution, codec, color, and audio metadata;
- interchange and conform packages;
- ensuring raw URLs and ad-hoc downloads never enter the timeline.

## HyperFrames roles

### HyperFrames technical director

Owns:

- project scaffold, pinned version, local dependencies, fonts, and media paths;
- `BRIEF.md`, `frame.md`, root composition, scene mounting, and deterministic runtime contract;
- shared component and registry decisions;
- output formats and render settings;
- lint, check, snapshot, animation-map, preview, and render gates;
- the plate and reference-render manifest.

### HyperFrames scene builder

Owns one or more bounded, approved shot or sequence packets:

- static end-state construction;
- exact scene-local composition;
- approved motion and text choreography;
- scene-local media and audio placement when assigned;
- scene-local checks and motion sidecar;
- implementation report.

The builder does not alter narration, direction, evidence, asset selection, scene order, or shared state.

### Motion systems designer

Owns reusable, episode-agnostic primitives:

- actor tokens;
- flow connectors;
- evidence pins;
- human gates;
- cost meters;
- failure and exception states;
- caption and source treatments;
- shared motion rules and transition primitives.

Reusable means behavior and interface, not a finished scene or generic template.

## Resolve and finishing roles

### Lead editor

Owns the canonical Resolve timeline after directed-animatic approval:

- conform;
- selected-media assembly;
- editorial trims within approved intent;
- B-roll and archival pacing;
- J- and L-cuts;
- sequence and chapter rhythm;
- picture-lock recommendation;
- logging any change that must return to Blueprint Cinema.

### Online / conform editor

Owns:

- relinking full-resolution assets;
- replacing animatic placeholders with approved selects and plates;
- alpha, scaling, frame-rate, timecode, and color-pipeline correctness;
- validating the Resolve timeline against the approved reference;
- final title, caption, and legal/disclosure placement;
- missing-media and render-health reports.

### Fusion finishing artist

Owns finish-level composites:

- cleanup;
- tracked masks;
- screen and document replacements using accurate sources;
- roto and keying;
- integration of graphics with footage;
- grain, blur, light-wrap, and texture matching where justified.

Fusion does not become a second motion-design system. Rebuilding an approved HyperFrames scene in Fusion requires an explicit exception.

### Colorist

Owns:

- color-management setup;
- normalization and primary correction;
- shot matching;
- skin and key-object protection;
- archival and AI-plate integration;
- the approved creative grade;
- scopes-based and visual QC;
- grade notes and review exports.

### Sound supervisor and Fairlight mixer

Owns:

- dialogue cleanup and consistency;
- ambience and room-tone continuity;
- music edit and VO relationship;
- operation-focused SFX;
- automation, spectral carving, dynamics, and final mix;
- loudness, true peak, channel, phase, and artifact checks;
- mix stems and delivery report.

### Caption and accessibility editor

Owns:

- transcript accuracy;
- segmentation and reading cadence;
- line breaks and safe areas;
- speaker and sound identifiers when required;
- subtitle and burned-caption exports;
- caption collision and contrast review.

### Finishing producer / delivery QC

Owns:

- picture, sound, color, caption, rights, disclosure, and technical checklists;
- final master and platform export verification;
- comparison to picture lock;
- media probes;
- archive completeness;
- delivery-validation recommendation.

## Review independence

At minimum, the following recommendations require an independent reviewer who did not perform the primary build being reviewed:

- engine honesty;
- direction-bible cohesion;
- evidence integrity;
- whole-episode animatic comprehension;
- picture lock;
- rights and synthetic-media compliance;
- final audio and technical delivery.

For a one-person production, independence can be temporal and procedural: perform the review as a separate named role, use a fresh pass and checklist, do not edit while reviewing, and record findings before fixing them.

## Work waves

| Wave | Serialized owner | Safe parallel roles | Required merged result |
|---|---|---|---|
| Input | orchestrator | read-only source and timing audit | hash-pinned input lock |
| Engine | engine author | honesty, fairness, evidence, and distinctiveness critics | approved episode engine |
| World | production designer | transcript mapper, evidence mapper, failure/human-gate audit | approved persistent world |
| Visual plan | editorial producer | non-overlapping sequence proposals and boundary critic | approved full-timeline plan |
| Direction | creative and motion directors | reference research, typography, evidence, documentary, sound, and accessibility consultants | direction bible and rhythm map |
| Look development | creative director | style-frame artists for distinct modes, motion-test builder, design-adherence critic | approved visual language |
| Scene direction | motion director and storyboard artist | non-overlapping sequence direction packets after language lock | validated canonical scene directions and shot board |
| Animatic | HyperFrames technical director | bounded scene builders plus read-only continuity and timing QA | whole-episode directed animatic |
| Assets | archival/footage producer and media manager | ticket-bounded footage, evidence, original capture, AI plates, graphics, music, SFX, captions | approved selects and asset manifest |
| Rough cut | lead editor | plate replacement, asset prep, mix prep, caption prep | coherent Resolve rough cut |
| Picture lock | lead editor | editorial, continuity, evidence, rights, and accessibility review | approved picture lock and updated edit manifest |
| Finish | post supervisor | conform, Fusion, color, Fairlight, captions | finish candidate |
| Delivery | finishing producer | independent technical, rights, disclosure, caption, audio, and image QC | validated master and archive |

## Never parallelize

- Two directors establishing competing visual languages for the same episode.
- Adjacent sequence direction without one boundary owner.
- Multiple builders modifying the same composition, root index, direction file, or Resolve timeline.
- Asset selection before the ticket and shot purpose are approved.
- Canonical timeline integration.
- Approval recording.
- Publication, licensing, purchases, paid generation, or disclosure decisions without authorization.

## Professional stopping rule

Every role stops when an upstream decision is missing. It reports the exact absent fact, object, ticket, source, right, direction, or approval. Nobody fills a production gap with generic imagery, invented evidence, decorative motion, or an undocumented editor judgment.
