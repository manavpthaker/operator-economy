# Asset and media production contract

## Purpose

This contract turns approved shot needs into sourced, generated, captured, selected, and timeline-ready media without losing semantic purpose, rights, provenance, continuity, or disclosure.

```text
approved shot need
  -> asset ticket
  -> search / capture / generation brief
  -> candidates
  -> select
  -> technical preparation and proxy
  -> approved asset manifest
  -> HyperFrames and Resolve timeline use
  -> final rights and disclosure audit
```

An attractive file is not an asset until it is identified, licensed or authorized, technically inspected, semantically approved, and connected to an exact shot purpose.

## Asset states

Every asset moves through explicit states:

1. `needed`: a visual-plan or scene-direction need exists;
2. `ticketed`: the semantic, rights, provenance, continuity, and technical requirements are written;
3. `searching` or `producing`: candidates are being sourced, captured, designed, or generated;
4. `candidate`: a specific file or source range may satisfy the ticket;
5. `selected`: the editorial role and source range are chosen;
6. `rights_cleared`: required license, permission, release, attribution, and restrictions are recorded;
7. `technical_pass`: the file passes media inspection and is usable in the intended pipeline;
8. `approved`: the select satisfies the ticket and scene direction;
9. `staged`: a frozen local source, derivative, or proxy is placed in the canonical media structure;
10. `used`: exact HyperFrames and/or Resolve timeline uses are recorded;
11. `superseded`: retained for history but no longer authorized for new uses;
12. `rejected`: retained only when rejection history is valuable; rejection reason recorded.

No state is inferred from the existence of a file.

## Asset ticket contract

Every ticket records:

- ticket ID;
- episode and sequence IDs;
- shot IDs and exact time range when known;
- story role: `human_context`, `market_force`, `proof`, `process`, or `outcome`;
- production lane: original capture, permissioned company material, licensed archival, licensed stock, evidence capture, AI environmental plate, motion graphic, illustration, music, SFX, ambience, caption, or other authorized lane;
- required semantic content;
- specific action or state that must be visible;
- why the shot cannot be satisfied with an existing approved object or primitive;
- required subject, environment, period, geography, process, interface, document, or outcome;
- continuity requirements;
- camera, framing, movement, and handle requirements;
- crop, focal, aspect, and safe-area requirements;
- duration and source in/out expectations;
- technical requirements;
- claim and evidence IDs;
- rights and release requirements;
- provenance requirements;
- synthetic and reconstruction status;
- disclosure requirements;
- placeholder behavior;
- explicit exclusions;
- acceptance checks;
- budget, paid-generation, or licensing authorization boundary;
- status and owner.

## Canonical asset manifest

Every selected or used asset has one manifest entry with:

### Identity

- asset ID;
- ticket ID;
- episode, sequence, and shot IDs;
- asset type;
- source versus derivative relationship;
- filename and project-relative path;
- checksum;
- file size;
- created, downloaded, captured, or generated date;
- status and approval record.

### Source and provenance

- canonical source URL or acquisition locator;
- source platform or archive;
- title or source description;
- creator;
- publisher;
- rights holder;
- date created or published when relevant;
- download or capture date;
- original source filename;
- source context;
- claim and evidence relationship;
- archive snapshot or locator when required.

### Rights

- license or authorization type;
- license text or receipt locator;
- license-check date;
- permitted uses;
- territory, term, platform, and modification restrictions;
- required attribution;
- payment or purchase record locator;
- model, property, location, music, or other releases;
- face and privacy review;
- expiry or recheck date;
- reviewer and unresolved rights questions.

### Technical metadata

- container and codecs;
- duration;
- width and height;
- pixel aspect ratio;
- frame rate and time base;
- bit depth and chroma when known;
- alpha status;
- color primaries, transfer, matrix, and range when known;
- audio streams, sample rate, channels, and layout;
- variable-frame-rate status;
- embedded timecode;
- corruption, decode, missing-frame, or silence findings.

### Editorial selection

- exact source in and out;
- handles before and after;
- selected duration;
- crop and focal point;
- speed or retime instruction;
- stabilization or cleanup expectation;
- intended timeline uses;
- story job in each use;
- chosen alternative and rejected alternatives;
- semantic-fit review;
- continuity notes.

### Synthetic and reconstruction metadata

- synthetic status;
- model and version;
- prompt-package ID;
- seed, reference assets, and generation settings when supported;
- generated date;
- generation provider;
- disclosure requirement;
- reconstruction status and on-screen label;
- factual elements composited from authorized sources;
- prohibited interpretation;
- reviewer.

### Derivatives

- parent asset ID;
- operation performed;
- operation parameters;
- proxy or deliverable purpose;
- checksum and path;
- whether the derivative is reversible;
- tool and version.

## Folder contract

```text
assets/
├── manifest.json
├── tickets/
├── candidates/
│   ├── original-capture/
│   ├── company-material/
│   ├── archival/
│   ├── stock/
│   ├── evidence/
│   ├── ai-plates/
│   ├── graphics/
│   └── audio/
├── selects/
│   ├── picture/
│   ├── evidence/
│   ├── graphics/
│   └── audio/
├── source/
├── derivatives/
├── proxies/
├── contact-sheets/
└── reports/
```

Large media stays ignored. The tracked manifest preserves identity, hashes, provenance, status, and use. Do not commit licensed media, raw captures, generated video, proxies, or purchased files unless repository policy explicitly permits it.

## B-roll contract

Every B-roll candidate is evaluated against its ticket's story job.

### Human context

Must establish a specific person, environment, action, or physical consequence. Generic people smiling, walking, typing, shaking hands, or looking at dashboards are not sufficient.

### Market force

Must show the actual platform, category, infrastructure, behavior, place, or period relevant to the market force. A generic city or office does not prove market dynamics.

### Process

Must show the actual work, sequence, tool, handoff, or physical operation. If the process cannot be captured truthfully, use system graphics and label any reconstruction.

### Proof

Must be an authorized source, original capture, document, interface, or archival record. Stock and AI are not proof.

### Outcome

Must show the real human, operational, or physical result. Avoid generic celebration imagery.

### B-roll selection checklist

- Does the action occur, or is the clip merely topically related?
- Is the subject specific to the episode?
- Is the era, geography, environment, and scale correct?
- Is the camera movement compatible with adjacent shots?
- Does screen direction support continuity?
- Is there enough pre- and post-action handle?
- Can the frame accept required graphics or captions?
- Does the clip create an unintended claim?
- Is the license valid for the intended use?
- Is the grade recoverable and technically compatible?

## Archival contract

Every archival use records:

- event or claim supported;
- date and location;
- source archive and locator;
- creator or rights holder;
- original caption or metadata;
- editorial context;
- whether the item is primary evidence, illustrative history, or atmosphere;
- modifications and crop;
- attribution;
- rights and restrictions;
- any uncertainty about identity, date, or location.

Never imply that an archival clip depicts the specific company, person, or event being narrated when it is only general historical context.

## Evidence and interface capture

Prefer original, accurate capture for proof and process.

Every capture brief specifies:

- exact source or environment;
- account and permission boundary;
- privacy, PII, credential, and customer-data precautions;
- exact page, state, field, document passage, or interaction;
- required browser or application dimensions;
- cursor visibility policy;
- capture frame rate and codec;
- crop and annotation plan;
- reconstruction labeling if a clean-room mock is required;
- version and capture date;
- source context that must remain visible;
- cleanup permitted after capture.

Do not fabricate a clean interface when the claim depends on the real interface. If privacy or access prevents real capture, change the visual plan or label the reconstruction.

## AI environmental plate contract

AI-generated media is limited to non-evidentiary environments, metaphors, impossible views, or physical actions that cannot reasonably be captured.

Every generation packet includes:

- ticket and shot IDs;
- story job;
- exact approved action;
- character and environment continuity references;
- recurring object continuity;
- starting and ending composition;
- screen direction;
- camera height, lens character, movement, and speed;
- lighting, time of day, weather, texture, and color target;
- duration and handles;
- expected clean compositing zones;
- factual elements to omit for later composite;
- negative prompt and failure cases;
- seed, model, version, and provider when available;
- synthetic disclosure requirement;
- review contact sheet or strip;
- selected generation and rejection reasons.

Use `../templates/episode/AI-PLATE-GENERATION-PACKET.template.md` so camera, action, continuity, negative constraints, model settings, candidate history, synthetic status, and selection evidence remain reviewable rather than disappearing inside a prompt box.

Prohibited:

- generated text, prices, statistics, interfaces, documents, logos, or source material presented as accurate;
- synthetic people presented as real case-study subjects;
- generic dark technology worlds, futuristic offices, data tunnels, glowing brains, or corporate wallpaper;
- a generated clip for every sentence;
- changing recurring people, objects, environment, light, wardrobe, or screen direction without narrative reason;
- using visual plausibility as a substitute for provenance.

## Graphic and illustration asset contract

Graphics and illustrations inherit:

- OE design-system tokens;
- direction-bible palette and material rules;
- persistent object IDs;
- approved geometry and hierarchy;
- exact text and source labels;
- required alpha and output dimensions;
- motion-safe edge and handle requirements;
- reconstruction and synthetic labels;
- creator and license metadata for external elements.

Reusable primitives remain semantically neutral. A finished diagram or shot composition is episode-specific and must not be reused as a generic template.

## Audio asset contract

Music, SFX, and ambience follow the same manifest discipline.

Record:

- track or sound ID;
- source, creator, rights holder, license, and check date;
- duration, sample rate, channels, loudness measurements when relevant;
- intended sequence, cue, and story job;
- source in/out and edit points;
- loop or extension method;
- music stem availability;
- synthetic or generated status;
- attribution and restrictions;
- final timeline uses.

Use `/media-use` to resolve, adopt, generate, and preprocess audio for HyperFrames. Placed-track mixing belongs to `/hyperframes-audio`; final episode mixing belongs to Fairlight.

## Candidate review

Review candidates as contact sheets or short labeled reels whenever possible. Each candidate shows:

- asset and ticket ID;
- thumbnail or representative frames;
- source range;
- duration;
- story-role assessment;
- continuity assessment;
- rights status;
- technical warnings;
- synthetic or reconstruction status;
- recommendation and rejection reason.

Do not inspect candidates without their semantic requirement. Visual taste without the ticket is not asset review.

## Technical preparation

Preparation may include:

- checksum and media probe;
- proxy generation;
- constant-frame-rate conversion when required;
- color-space normalization metadata;
- audio extraction;
- alpha verification;
- conform-safe filename sanitation;
- privacy redaction;
- stabilization or cleanup test;
- still extraction or contact sheet;
- shot handles;
- slate or burn-in for review only.

Every derivative records its parent and operation. Never overwrite the source.

## Final asset gate

`assets_ready` or `asset_selects_ready` means:

- every required shot has an approved select or an explicit approved placeholder;
- every used file has a manifest ID and checksum;
- every proof asset maps to approved evidence;
- rights and release requirements are closed or explicitly escalated;
- synthetic and reconstruction statuses are complete;
- technical probes pass;
- HyperFrames and Resolve can relink through project-relative or mapped paths;
- rejected and superseded files cannot be mistaken for approved selects;
- no raw URL or untracked download appears in the edit.
