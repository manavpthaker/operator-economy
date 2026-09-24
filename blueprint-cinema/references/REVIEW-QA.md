# Review and quality-assurance system

## Purpose

Blueprint Cinema reviews one decision at a time using the cheapest artifact that can prove it. Review is not a single watch at the end and not a collection of subjective comments such as “make it cinematic.”

```text
logic review
  -> visual-language review
  -> static shot-board review
  -> motion-test review
  -> whole-episode directed-animatic review
  -> asset-select review
  -> rough-cut review
  -> picture-lock review
  -> color and sound review
  -> delivery QC
```

## Finding severity

Every finding is classified:

### Blocking

The artifact is dishonest, incomprehensible, unsafe, unlicensed, structurally wrong, technically unusable, or inconsistent with an approved upstream decision. The gate cannot pass.

Examples:

- evidence does not support the narration;
- AI imagery reads as real evidence;
- a customer or value takes an impossible system route;
- timing no longer matches the locked VO;
- selected footage has unresolved rights;
- the primary subject cannot be identified;
- a render contains missing or corrupt frames;
- final audio clips or drops out.

### Major

The intended meaning is recoverable but hierarchy, timing, continuity, asset fit, sound, color, or craft is below the production standard. The artifact requires revision before approval unless the showrunner records a narrow exception.

### Polish

The artifact already communicates correctly. The note improves finish without changing meaning, timing, continuity, evidence, rights, or delivery validity.

### Observation

Non-blocking context or risk to monitor. It does not request a change.

## Review evidence

Every review report records:

- artifact and version;
- exact hashes;
- reviewer role;
- review date;
- source inputs;
- playback or display environment;
- passes completed;
- findings with sequence and shot IDs;
- severity;
- evidence such as frame, timestamp, waveform, scope, or manifest entry;
- recommended owner;
- disposition;
- unresolved questions;
- approval recommendation;
- explicit limits.

“Looks good” without the artifact, version, and pass is not a review record.

## Gate 1: episode engine review

Review:

- operator and customer clarity;
- owned value;
- constraint;
- counter-system;
- measurable outcome;
- mechanical honesty;
- fairness;
- human judgment;
- failure and exception paths;
- evidence requirements;
- visual distinctiveness;
- actionable viewer promise.

Reject mechanisms chosen primarily because they are easy to animate.

## Gate 2: persistent-world review

Review:

- stable IDs;
- zones and paths;
- object meaning;
- valid states and transitions;
- ownership and permission;
- money flow;
- evidence anchors;
- failure paths;
- suppression and escalation;
- human gates;
- object permanence;
- screen-direction implications;
- whether the model can run without narration labels inventing missing logic.

## Gate 3: full-timeline visual-plan review

Review:

- complete VO coverage;
- exact timing and word ranges;
- sequence boundaries;
- business-state changes;
- carries and focus;
- reality, system, proof, and outcome modes;
- evidence and ticket dependencies;
- actionability;
- cadence warnings;
- boundary continuity;
- ending resolution.

Do not review finished composition at this gate.

## Gate 4: visual-language review

Inputs:

- direction bible;
- rhythm map;
- style frames;
- representative motion test;
- direction-bible compliance report.

Passes:

### Creative coherence

- Does the visual thesis express the episode transformation?
- Are reality, system, proof, and outcome distinct but related?
- Do recurring objects have stable meaning?
- Can the language scale across all planned sequences?
- Does the result look like OE rather than an imitation of a reference?

### Art direction

- Are composition, type, color, material, texture, depth, and contrast intentional?
- Is the frame cinematic without relying on darkness, glow, blur, or generic depth?
- Does the OE design system remain recognizable?
- Are real text and real objects used in style frames?

### Motion direction

- Do reveals follow the VO?
- Does motion express operations and consequences?
- Does movement settle?
- Is stillness deliberate?
- Do transitions preserve a real relationship?

### Technical scalability

- Does the test pass HyperFrames checks?
- Are fonts and assets local?
- Is the motion deterministic and seek-safe?
- Do phone-scale and compression checks pass?
- Can the approach render at full duration and required quality?

Visual-language approval is a human gate.

## Gate 5: shot-board review

Review the entry, action, consequence, and exit states without finish.

### Composition

- Can the primary subject be identified immediately?
- Does the eye travel in the intended order?
- Is the action spatially legible?
- Is the consequence visible?
- Are supporting layers subordinate?
- Is the frame understandable without production notes?

### Copy and typography

- Is every visible string exact and necessary?
- Does text label or prove rather than narrate?
- Is source text legible?
- Is there enough space and reading time?
- Are captions and essential graphics separated?

### Continuity

- Does the entry inherit the prior exit correctly?
- Does the exit establish the next shot's requirement?
- Are persistent objects recognizably identical?
- Is screen direction preserved or meaningfully broken?
- Do money, state, route, and evidence accumulate correctly?

### Complexity

- Is there one primary action?
- Are too many new concepts introduced?
- Can any label or object be removed?
- Would the viewer need to pause?

Shot-board approval authorizes motion implementation, not asset licensing or generation.

## Gate 6: motion-test review

Watch the representative sequence:

1. normally with sound;
2. muted for visual causality;
3. at 50-percent display scale;
4. on a phone-sized preview;
5. frame-by-frame at its key transitions;
6. after the intended review encode, not only in a browser preview.

Review:

- VO and reveal synchronization;
- action phases;
- final reading holds;
- motion consistency;
- object continuity;
- cut and transition motivation;
- text and source legibility;
- compression behavior;
- sound purpose;
- whether the scene advertises effects rather than explaining the system.

## Gate 7: whole-episode directed-animatic review

The directed animatic is the first complete editorial visual test. It uses locked narration, approved shot timing, real text, truthful placeholders, and approximate sound cues.

Run separate passes. Do not attempt to diagnose everything during one watch.

### Pass A: comprehension

- What did the viewer understand in each sequence?
- Is every before, operation, and after state clear?
- Is the episode actionable?
- Does the viewer understand operator, customer, value, constraint, counter-system, human judgment, failure, economics, and outcome?

### Pass B: full-episode rhythm

- Where does attention rise and fall?
- Are dense passages followed by relief?
- Are holds long enough to read but not dead?
- Does the opening move quickly enough?
- Is the middle monotonous?
- Does the ending resolve accumulated state?

### Pass C: continuity

- persistent objects;
- world geography;
- screen direction;
- route logic;
- state and value accumulation;
- evidence pins;
- mode transitions;
- audio bridges.

### Pass D: visual hierarchy

- one primary priority;
- eye path;
- legibility;
- text density;
- repeated framing;
- empty or overloaded frames;
- caption and source collisions.

### Pass E: motion

- meaningful versus decorative changes;
- front-loading;
- unresolved motion;
- excessive ambient movement;
- uniform easing;
- camera and object conflict;
- transition overuse;
- meaningful-change intervals.

### Pass F: evidence and honesty

- source context;
- claim relationship;
- extraction and attachment;
- estimate and caveat visibility;
- reconstruction labels;
- AI boundaries;
- no fake UI, document, price, or proof.

Directed-animatic approval is a human gate. It authorizes asset production and final motion construction against the approved shots.

## Gate 8: asset-select review

Review candidates against exact tickets, not in isolation.

Passes:

- semantic fit;
- specificity;
- continuity;
- rights and releases;
- provenance;
- synthetic and reconstruction status;
- source range and handles;
- technical integrity;
- crop and graphics compatibility;
- color recoverability;
- alternatives and rejection reasons.

An asset can be technically excellent and still fail because it performs the wrong editorial job.

## Gate 9: rough-cut review

Run separate:

- narrative pass;
- coverage pass;
- continuity pass;
- evidence pass;
- rhythm pass;
- motion and transition pass;
- preliminary sound pass;
- caption and safe-area pass.

The rough cut must be watched from beginning to end at least once without stopping before approval. Spot checks cannot reveal episode-level rhythm or accumulated-state failures.

## Gate 10: picture-lock review

Confirm:

- no blocking or major editorial findings;
- exact shot order and record timing;
- final selected media and source ranges;
- final factual text and evidence treatment;
- final transition decisions;
- all placeholders closed or accepted;
- rights and disclosure blockers closed;
- edit manifest and Resolve timeline agree;
- picture-lock reference and checksum exist.

Picture-lock approval is a human gate and invalidates when any meaningful picture timing or content changes.

## Gate 11: color review

Review:

- color-management configuration;
- normalization;
- exposure and white-balance consistency;
- shot matching;
- skin, paper, screen, source, and brand-color integrity;
- AI, archival, stock, original, graphic, and Fusion integration;
- black and highlight behavior;
- creative intent;
- compression and banding;
- scopes and viewing limits.

Compare before/after frames and at least one continuous review render. A gallery still cannot reveal every temporal grade mismatch.

## Gate 12: sound review

Review:

- narration clarity and consistency;
- music relationship;
- ambience continuity;
- SFX purpose;
- transition bridges;
- quiet passages;
- dynamic consistency;
- phase and mono compatibility;
- loudness, true peak, clipping, silence, dropouts, and tails;
- final rendered mix.

Listen at normal, quiet, and practical consumer playback levels when possible.

## Gate 13: caption and accessibility review

Review:

- transcript accuracy;
- names, numbers, and terminology;
- segmentation;
- reading speed;
- line breaks;
- contrast;
- safe areas;
- graphic and source collisions;
- subtitle file encoding and timing;
- burned-caption consistency when delivered.

## Gate 14: delivery validation

Validate the rendered master, not the timeline.

### Media probe

- path and checksum;
- container and codec;
- duration;
- dimensions and aspect;
- frame rate and time base;
- pixel format and bit depth;
- color tags;
- audio codec, sample rate, channels, and layout;
- caption streams when applicable.

### Playback

- first and final frames;
- opening, identity, title, and ending;
- every chapter boundary;
- every high-risk evidence, alpha, transition, AI, archival, and caption shot;
- several random midpoints;
- full audio listen;
- no offline media, review overlays, or stale slate.

### Compliance and archive

- rights and releases;
- attribution;
- synthetic disclosure;
- reconstruction labels;
- captions;
- project and source manifests;
- Resolve export or archive;
- HyperFrames sources and version;
- final checksums;
- downstream handoff.

Delivery validation does not publish the episode.

## Review comparison methods

Use:

- contact sheets for episode-wide composition and repetition;
- entry/action/exit strips for shot construction;
- time-matched A/B frames for renderer or grade comparisons;
- difference or overlay inspection for conform drift;
- waveform and meters for audio events;
- scopes for color and level;
- media probes for technical facts;
- full-length playback for rhythm and sound;
- hashes for artifact identity.

Do not use a single representative frame to approve a timeline.

## Exception rule

An exception records:

- exact finding;
- severity;
- affected artifact and hash;
- reason it cannot or should not be fixed;
- audience and production risk;
- compensating control;
- owner;
- expiry or re-review condition;
- approver.

Exceptions do not silently weaken future episodes.
