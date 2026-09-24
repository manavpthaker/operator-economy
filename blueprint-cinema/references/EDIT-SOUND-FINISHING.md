# Edit, sound, color, and finishing contract

## Purpose

This contract governs the transition from an approved directed animatic and approved media selects into the final DaVinci Resolve timeline and delivery masters.

```text
directed animatic approved
  -> assets and plates approved
  -> Resolve conform
  -> rough cut
  -> editorial and evidence review
  -> picture lock
  -> online and Fusion finish
  -> color correction and grade
  -> Fairlight sound mix
  -> captions and accessibility
  -> master and platform exports
  -> final QC and archive
```

Resolve is the finishing environment. Blueprint Cinema remains the authority for meaning, timing contracts, evidence, continuity, assets, and approvals.

## Canonical edit plan

The edit plan exists outside Resolve so the approved timeline can be inspected, diffed, validated, and reconstructed.

Every timeline event records:

- event ID;
- episode, sequence, and shot IDs;
- track role;
- record in and out;
- source asset or plate ID;
- source in and out;
- playback rate and retime method;
- crop, scale, position, and focal instruction;
- opacity, blend, mask, and alpha expectation;
- transition type and duration;
- narration word range;
- graphic, evidence, title, and caption overlays;
- music, ambience, and SFX cues;
- continuity anchor;
- version status;
- review notes;
- approval dependency.

Track roles are explicit:

- `picture_primary`;
- `picture_broll`;
- `picture_archival`;
- `picture_ai_plate`;
- `graphics_opaque`;
- `graphics_alpha`;
- `evidence`;
- `titles_identity`;
- `captions`;
- `vo`;
- `dialogue_sync`;
- `music`;
- `ambience`;
- `sfx`;
- `mix_print`;
- `review_only`.

## HyperFrames handoff outputs

The HyperFrames technical director exports only what the Resolve conform needs:

### Directed-animatic reference

- full-length MP4;
- exact locked VO;
- shot and sequence timing;
- approved edit structure;
- optional review-only burn-ins for shot ID, sequence ID, source ticket, and timecode;
- checksum and media probe.

### Opaque scene plates

Use when the scene is picture-complete inside HyperFrames. Deliver one high-quality scene or sequence plate per approved range with documented frame rate, duration, color interpretation, and handles.

### Alpha graphic plates

Use when graphics must be composited over Resolve footage. HyperFrames supports transparent MOV or WebM and RGBA PNG sequences. Every plate declares:

- expected premultiplication or straight-alpha interpretation when known;
- frame rate;
- exact first and last record frame;
- handles;
- canvas dimensions;
- color and transfer expectations;
- plate ID and shot IDs;
- whether text and evidence are already baked.

Use an RGBA PNG sequence when alpha, edge quality, or frame-level recoverability is more important than storage. Use a transparent movie when the pipeline has verified its codec, alpha, and decode behavior.

### Audio guides and stems

Deliver:

- locked narration;
- HyperFrames reference mix when present;
- music guide;
- SFX guide;
- ambience guide;
- cue sheet.

HyperFrames audio remains a creative and timing reference unless it has been explicitly approved as a final stem.

### Interchange

Prefer OTIO as the inspectable timeline interchange and FCPXML as a Resolve-compatible alternative. EDL may accompany them for simple picture events. The handoff manifest states which interchange is authoritative and any unsupported effects or transforms that require manual conform.

The installed Resolve scripting API supports importing AAF, EDL, XML, FCPXML, DRT, ADL, and OTIO. Interchange capability does not prove a correct conform; compare the imported timeline with the animatic reference.

## Resolve project contract

Every episode uses a dedicated project or clearly isolated project folder and timeline naming scheme.

Recommended structure:

```text
EP###-SLUG
├── 00_REFERENCE
├── 01_VO
├── 02_BROLL
├── 03_ARCHIVAL
├── 04_EVIDENCE
├── 05_AI_PLATES
├── 06_HF_OPAQUE
├── 07_HF_ALPHA
├── 08_AUDIO
├── 09_CAPTIONS
├── 10_SEQUENCES
├── 11_TIMELINES
└── 12_EXPORTS
```

Timeline versions use explicit semantic stages:

```text
EP###_CONFORM_v001
EP###_ROUGH_v001
EP###_PICTURELOCK_v001
EP###_FINISH_v001
EP###_MASTER_v001
```

Do not use names such as `final`, `final2`, or `latest`.

Resolve markers carry Blueprint Cinema IDs and review status. At minimum:

- sequence boundaries;
- shot IDs;
- evidence events;
- synthetic or reconstruction disclosures;
- missing asset or rights blockers;
- review findings;
- approved change notes.

## Conform pass

The conform editor must:

1. create or load the correct project;
2. set frame rate, resolution, color management, audio sample rate, and timecode before importing media;
3. ingest the locked VO and animatic reference;
4. import the approved interchange or rebuild from the edit manifest;
5. relink approved selects and HyperFrames plates by manifest ID;
6. verify every event against the reference;
7. confirm shot order, duration, transitions, alpha, text, and evidence timing;
8. report missing media, unsupported interchange features, frame offsets, color mismatches, and audio drift;
9. save and export a conform report before editorial refinement.

The conform report lists every difference from the reference. A difference is not accepted merely because the imported timeline plays.

## Rough-cut passes

### Pass 1: narrative and causal comprehension

Review:

- does each sequence answer its intended question;
- does the visual explain rather than decorate the narration;
- is the before, operation, and consequence readable;
- are reality, system, and proof used for the correct jobs;
- does the viewer retain the operator, customer, owned value, constraint, counter-system, and outcome;
- can any shot or sequence be removed without losing meaning.

### Pass 2: coverage and asset semantics

Review:

- does each footage select perform its ticketed role;
- are there enough handles and clean edit points;
- does B-roll create an unintended claim;
- is archival accurately contextualized;
- do AI plates remain non-evidentiary;
- are placeholders conspicuous;
- are source and reconstruction labels present.

### Pass 3: continuity

Review:

- persistent object identity;
- route and screen direction;
- movement vector;
- position, scale, depth, and state;
- wardrobe, light, environment, lens, and camera height;
- accumulated economics and system state;
- audio tails and ambience;
- title, source, and caption safe areas.

### Pass 4: rhythm

Review:

- meaningful-change intervals;
- shot length and information density;
- reveal timing against VO;
- reading holds;
- breathers;
- section entry and exit energy;
- repeated framing or motion;
- excessive transitions;
- whether stillness is intentional;
- whether the visual resolves before the narration moves on.

### Pass 5: evidence

Review the full evidence chain:

```text
source
  -> context
  -> highlight
  -> extraction
  -> attachment
  -> changed model
  -> pinned provenance
```

The evidence editor signs off separately from general editorial review.

## Picture-lock contract

Picture lock means:

- shot order and record timing are approved;
- selected media and source ranges are approved;
- all text, evidence, titles, reconstructions, and disclosures are present in final wording;
- transitions and speed changes are approved;
- placeholders are closed or explicitly accepted;
- rights and synthetic-media status are not blocking;
- the edit plan matches the Resolve timeline;
- an approved picture-lock reference render and checksum exist;
- downstream color, Fusion, sound, and captions can proceed without changing meaning or duration.

Picture lock does not mean final color, mix, cleanup, captions, compression, or delivery.

Any later change to shot order, duration, evidence timing, text meaning, or causal state breaks picture lock and returns to editorial approval.

## Fusion finishing

Use Fusion for:

- tracked masks;
- paint and cleanup;
- screen replacements from accurate sources;
- keying;
- roto;
- stabilization refinements;
- local light-wrap, grain, blur, and depth integration;
- compositing HyperFrames graphics with footage;
- shot-specific fixes that are more reliable in the NLE finishing environment.

Do not use Fusion to:

- redesign an approved scene;
- invent missing evidence;
- rebuild the episode motion system;
- add unapproved effects;
- hide continuity or asset defects that should be fixed upstream;
- change factual text or interface state.

Each Fusion comp with substantive work receives a comp or shot note describing the purpose, source assets, and any limitations.

## Color correction and grade

### Color-management setup

Record:

- Resolve version;
- project color-management mode;
- timeline color space and transfer;
- output color space and transfer;
- data-level assumptions;
- HDR or SDR intent;
- display and review environment;
- source overrides;
- LUT and DCTL use;
- render-tag behavior.

Do not change color management mid-project without a documented migration and comparison.

### Correction pass

Correct before styling:

- exposure;
- white balance;
- contrast placement;
- saturation;
- channel casts;
- highlight and shadow recovery;
- shot-to-shot matching;
- skin, paper, screen, and key-object consistency;
- legal or delivery range problems.

### Integration pass

Match:

- original footage;
- stock;
- archival;
- AI plates;
- evidence captures;
- HyperFrames graphics;
- Fusion composites.

Integration does not erase provenance differences. Archival may retain appropriate material character; AI imagery must not be graded to masquerade as evidence.

### Creative grade

The grade follows the direction bible:

- reality-world warmth, neutrality, or tension;
- system-world graphic color integrity;
- proof-world legibility and source fidelity;
- outcome resolution;
- protected brand accents;
- controlled grain, halation, vignette, texture, or diffusion only when approved.

No generic cinematic LUT is accepted as a grade.

### Color review

Review:

- calibrated or documented display conditions;
- scopes;
- skin and neutral references;
- source documents and interfaces;
- brand colors;
- black, white, and highlight behavior;
- banding and compression risk;
- alpha-edge contamination;
- final platform encode.

## Sound plan

The sound plan is authored before the rough cut and updated through picture lock.

### Episode-level fields

- sonic thesis;
- music strategy;
- motif list;
- reality ambience strategy;
- system sound palette;
- proof sound palette;
- silence and breather plan;
- narration-treatment approach;
- transition-bridge rules;
- prohibited clichés;
- delivery targets to be measured and recorded.

### Sequence-level fields

- sequence ID and time range;
- music state and cue;
- ambience and perspective;
- SFX events and exact purpose;
- silence or reduction point;
- transition bridge;
- narration emphasis or risk;
- mix-density expectation;
- asset IDs and rights status.

### Shot-level cue fields

- cue ID;
- exact time or word cue;
- source asset ID;
- action supported;
- onset and tail;
- perspective and intensity;
- track assignment;
- whether it is diegetic, explanatory, transitional, or editorial;
- conflict with VO, music, or another cue;
- final status.

## Fairlight mix passes

### Dialogue / narration

- remove or reduce technical noise without damaging speech;
- correct distracting tonal or dynamic inconsistency;
- maintain natural breaths and cadence unless editorially removed;
- preserve intelligibility across the full episode;
- do not use processing as a substitute for a bad source without reporting the limitation.

### Music

- edit structure to the episode rather than looping arbitrarily;
- preserve purposeful quiet;
- use spectral and level space for narration;
- avoid music changes at every chapter unless the direction calls for it;
- record source and license IDs.

### Ambience

- create continuity across real footage;
- support location and perspective;
- bridge cuts when useful;
- avoid generic room tone under system graphics unless it serves the scene.

### SFX

Use SFX to clarify:

- handoff;
- lock;
- qualification;
- rejection;
- failure;
- reroute;
- queue;
- extraction;
- evidence attachment;
- confirmation;
- completion.

Do not attach a sound to every animation.

### Mix verification

- listen in full, not only in isolated scenes;
- listen on appropriate speakers and headphones when available;
- check quiet playback intelligibility;
- check mono compatibility and phase;
- inspect loudness, true peak, clipping, silence, dropouts, and tails;
- listen to the rendered master;
- record actual measured results and settings in the delivery report.

## Captions and accessibility

Caption work verifies:

- transcript accuracy against final narration;
- names, brands, technical terms, and numbers;
- segmentation and reading speed;
- line breaks;
- punctuation and casing;
- source and graphic collisions;
- bottom-band and mobile safety;
- speaker or sound labels when required;
- subtitle and burned-caption consistency;
- delivery-file encoding and timing.

Captions do not become a substitute for readable diagram labels or source attribution.

## Delivery masters

The finishing producer defines and records the exact deliverables. The minimum expected set is:

- picture-lock reference;
- mezzanine master;
- platform upload master;
- caption files;
- final mix and stems when required;
- review proxy;
- thumbnail or representative frames when required downstream;
- Resolve project export or archive outside Git;
- tracked archive manifest;
- media-probe report;
- QC report;
- rights, provenance, synthetic-media, and reconstruction report;
- tool versions and source hashes.

## Final QC passes

### Editorial

- correct episode and version;
- no missing, duplicated, or misordered content;
- correct opening, identity, title, and ending;
- no stale placeholder, marker, slate, or review burn-in.

### Picture

- no black, frozen, corrupt, offline, repeated, or dropped frames;
- no unintended flash, alpha halo, edge, crop, or scale defect;
- text and sources legible;
- captions safe;
- color and luminance consistent;
- graphics survive compression.

### Sound

- correct streams and channel layout;
- no clipping, dropout, drift, truncated word, or cut tail;
- narration intelligible;
- music and SFX intentional;
- measured loudness and peak recorded.

### Evidence and rights

- every source and claim relationship correct;
- required attribution visible;
- licenses, releases, and restrictions closed;
- reconstructions labeled;
- synthetic media recorded and disclosed as required.

### Technical

- filename and version correct;
- container, codecs, duration, frame rate, dimensions, aspect, color tags, audio, and captions verified;
- master checksum recorded;
- playback tested outside Resolve;
- delivery and archive paths recorded;
- publication state remains unchanged until downstream release gates pass.
