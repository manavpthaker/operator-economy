# Direction system

## Purpose

This contract fills the gap between an approved visual plan and buildable scenes. It converts episode logic into an episode-specific visual language, then into sequences, shots, and implementation packets.

```text
episode engine
  -> persistent world
  -> full-timeline visual plan
  -> direction bible
  -> rhythm map
  -> look development
  -> sequence treatments
  -> shot board
  -> scene directions
  -> HyperFrames build packets
  -> directed animatic
```

The direction system is not a request for a longer prose prompt. It is a hierarchy of decisions. Every downstream prompt is compiled from approved upstream decisions.

## Three levels of direction

### Editorial direction

Answers:

- Why does this sequence or shot exist?
- What does the viewer believe before it?
- What must the viewer infer afterward?
- What question is answered?
- What tension, reversal, proof, instruction, or payoff occurs?
- Why is this a new shot rather than a continuation of the existing frame?

### Visual direction

Answers:

- What is the primary subject?
- What relationship is visible?
- Where does the eye begin and travel?
- What is foreground, midground, and background?
- What enters, changes, persists, and leaves?
- How do scale, position, contrast, depth, focus, and stillness establish hierarchy?
- What does the entry frame inherit and what does the exit frame hand forward?

### Implementation direction

Answers:

- Which approved IDs and assets are mounted?
- What exact text is visible?
- Which time and word cues trigger the action?
- What deterministic property changes occur?
- What camera, mask, crop, transform, or transition is used?
- What output and validation prove the shot was implemented faithfully?

Do not ask a builder to solve editorial and visual direction while writing HTML, animation, or NLE instructions.

## Artifact 1: direction bible

The creative director authors one direction bible for the episode after visual-plan approval. It applies to every department.

### Required identity and pins

- episode number, code, slug, and folder;
- workflow version;
- input-lock, engine, world, and visual-plan hashes;
- author, reviewers, status, and approval record;
- OE design-system revision or token hashes;
- HyperFrames version target;
- review canvas, frame rate, and destination.

### Required creative fields

#### Visual thesis

One sentence describing what the episode should feel like the viewer watched happen. It must describe a transformation, not a style.

Weak:

> A sophisticated documentary with Vox-style animation.

Strong:

> A real operating problem enters the frame, its hidden mechanism is exposed, a counter-system is assembled, evidence changes its parameters, the system is stressed, and control returns to the operator.

#### Emotional progression

Name the intended emotional state across the episode:

- opening tension;
- curiosity;
- recognition;
- proof and trust;
- construction and agency;
- friction or risk;
- resolution;
- practical confidence.

The episode may use a different progression, but it must be deliberate.

#### Picture/audio grammar

Declare how picture and sound divide the storytelling job before choosing angles, coverage, or performance:

First read the scene and adjacent beats: situation, viewer knowledge, relationship, stakes, and
emotional change. Choose the scene form with a reason; narration is not a genre classifier. Use
the OE film-direction skill's context-and-coverage reference for conditional technique selection.

| Mode | Language carrier | Picture responsibility | Coverage rule |
|---|---|---|---|
| `narrated_observation` | narrator | action, evidence, pressure, relationship, or consequence not merely restating the VO | observational action; no visible speech or dialogue-like exchange |
| `narrated_dramatization` | narrator | illustrative interaction whose meaning is supplied by narration | motivated conversational performance and coverage; no claim of verbatim or synchronized speech |
| `sync_dialogue` | scene participant | behavior and reactions around audible synchronized speech | dialogue exchange with coherent geography and eyelines |
| `presenter_address` | presenter | direct human explanation and purposeful returns to camera | direct address with audible synchronized delivery |
| `natural_sound_observation` | natural sound | process and environment whose source sound carries the moment | observed action with source sound; `source_delivery` only when the matching source is audible and synchronized |
| `silent_graphic` | narrator or none | a graphic operation, comparison, proof, or state change | graphic progression with no performed speech |

The visual mode—reality, system, proof, outcome, or identity—does not determine the picture/audio mode. A reality shot under voiceover is not dialogue footage simply because people are present.

Nor is an enacted conversation defective simply because it sits under narration. Explicit
`narrated_dramatization` permits reciprocal eyelines, question/answer behavior, and close/reverse
coverage when justified by the scene. It needs illustrative disclosure and an actual-audio
comprehension review. Mute viewing is diagnostic here, not a ban on expecting speech. See
`SCENE-DIRECTION-CONTRACT.md` for exact fields and safeguards.

For `narrated_observation`, ban word-shaped mouth movement, reciprocal conversational eyelines, question-and-answer reverse shots, and close facial coverage that makes the viewer wait for an unheard line. A narrator-led close view of a face is permitted only when it reveals task focus or a reaction visibly caused inside the shot. Apply a mute test: if the picture feels incomplete because a line seems missing, redirect the performance or coverage.

Delivery face functions are mode-bound. `source_delivery` belongs only to `natural_sound_observation`, requires `visible_speech: source_synced`, `sound_intent.dialogue: sync_source`, `sound_intent.ambience: source`, audible synchronized source sound, and `mute_test.missing_line_expected: true`; other natural-sound face functions keep the missing-line expectation false. `sync_dialogue` may use `sync_delivery`; `presenter_address` uses `presenter_delivery`. None of these delivery functions is permitted in `narrated_observation`, whose missing-line expectation remains false.

#### Mode treatments

Define each mode separately:

| Mode | Required direction |
|---|---|
| Reality | environment, people, object specificity, camera height, lens character, light, texture, movement, permissible reconstruction |
| System | spatial model, object forms, routes, depth, camera altitude, labels, state changes, failure behavior |
| Proof | source dominance, locator visibility, highlight method, extraction method, pinned context, attribution |
| Outcome | human and measurable result, degree of celebration, what prior object or state resolves |
| Identity | show and episode-title treatment, timing, stillness, relationship to continuing action |

#### Persistent motifs

For each recurring object or visual motif, define:

- world object ID;
- material form;
- color and contrast role;
- allowed states;
- meaning;
- first appearance;
- evolution;
- final resolution;
- prohibited metaphorical use.

An object never changes meaning merely because a later scene needs a convenient icon.

#### Screen-direction rules

Define directional meaning for:

- progress;
- reversal;
- failure;
- return;
- escalation;
- human intervention;
- money movement;
- evidence entering the model;
- camera travel between reality, system, and proof.

These rules may be broken only when the break itself communicates a change.

#### Composition grammar

Define:

- favored framing families;
- framing families reserved for specific moments;
- maximum simultaneous meaningful objects by mode;
- primary-versus-supporting scale relationship;
- safe areas and caption keep-outs;
- permitted asymmetry and negative space;
- depth treatment;
- evidence and source-label zones;
- title and identity behavior;
- rules for when type becomes the visual subject.

The direction bible must not impose one layout on every scene.

#### Camera grammar

Define:

- human-camera behavior;
- system-camera behavior;
- proof-camera behavior;
- permitted moves;
- forbidden drift;
- maximum move intensity;
- the difference between a camera move and an object move;
- conditions for push, pull, track, reframe, rack focus, orthographic view, and continuity follow;
- lens, camera height, and parallax expectations for original, stock, archival, and AI plates.

Every move states what new information the move reveals or follows.

#### Motion grammar

Define:

- primary business verbs;
- motion character by mode;
- duration bands for snap, standard, deliberate, and settle actions;
- default easing character;
- anticipation, action, consequence, and settle rules;
- permitted idle behavior;
- stillness allocation;
- contrast between normal operations, failure, reversal, and outcome;
- the maximum number of concurrent meaningful actions;
- the difference between explanatory motion and atmosphere.

Framework motion vocabularies supply implementation techniques. The direction bible decides whether the motion belongs.

#### Transition grammar

Define:

- cut as default;
- motivated transition families allowed for this episode;
- which objects or properties may persist through a transition;
- match-cut anchors;
- reality-to-system and system-to-reality behavior;
- evidence-to-model handoff;
- audio bridges;
- hard-reset conditions;
- transitions prohibited regardless of framework capability.

#### Typography grammar

Define:

- display, body, label, mono, source, number, caption, and identity roles;
- case, weight, line behavior, and alignment;
- emphasis methods;
- reading-time expectations;
- when kinetic type is justified;
- prohibited narration duplication;
- source and caveat treatment;
- number formatting and tabular behavior;
- phone-scale and 50-percent review rules.

#### Surface, texture, color, and light

Define:

- palette roles inherited from the OE design system;
- mode-specific background use;
- material and texture;
- line, border, shadow, and grain behavior;
- color meaning for active, failed, suppressed, verified, human-reviewed, and outcome states;
- reality and AI-plate light continuity;
- color-grade target and protection rules.

#### Documentary footage doctrine

Define:

- when real footage is necessary;
- the difference between human context, process, market force, proof, and outcome;
- shot specificity;
- observational versus illustrative footage;
- archival date and place requirements;
- acceptable camera and grade variation;
- unacceptable stock tropes;
- whether faces, hands, screens, documents, locations, or branded objects are needed.
- the picture/audio mode governing each use of human footage;
- the concrete action, evidence, pressure, relationship, or consequence that narrator-led footage carries;
- any audible, synchronized source delivery required by a `natural_sound_observation` shot;
- the mode-specific mute diagnostic, actual-audio review, and why each change of angle adds meaning.

#### AI plate doctrine

Define:

- the limited sequences where synthetic plates are justified;
- world, recurring person, wardrobe, environment, light, screen direction, camera, and lens continuity;
- what must be composited later;
- prohibited factual or evidentiary content;
- disclosure and metadata requirements;
- degree of photorealism or stylization;
- what visual cues must prevent synthetic material from being misread as documentary evidence.
- the declared picture/audio mode, visible-speech rule, face function, and mute-test requirement;
- one primary physical action per generated clip, with speech constraints chosen by mode rather than imposed on all narrator-led plates;
- the generator-independent direction facts: what stays still, master/setup relationship, action line and screen direction, typed continuity anchors, and initial and final images.

#### Sound identity

Define:

- music character and structural job;
- recurring sonic motifs;
- operation sounds;
- reality ambience;
- proof interaction sounds;
- quiet zones;
- sections where sound should recede;
- prohibited trailer, corporate, technology, or novelty clichés.

#### Negative list

At minimum prohibit:

- slideshow front-loading;
- screensaver motion;
- full world-map default views;
- icon-per-noun illustration;
- repeated card grids;
- decorative camera drift;
- uniform easing and entrance direction;
- effect-pack transitions;
- fake sources, documents, interfaces, people, or evidence;
- generic AI imagery;
- narration duplicated as paragraphs of text;
- changing style to simulate a state change.

## Artifact 2: rhythm map

The rhythm map evaluates the episode as one experience. The editorial producer authors it after the direction-bible draft and before look development.

Every sequence records:

- sequence ID and exact time range;
- story function;
- viewer knowledge before and after;
- question answered;
- dominant visual mode and any mode transition;
- dominant business verb;
- primary object or motif;
- new object introduced;
- accumulated state recalled;
- energy level from 1 to 5;
- information density from 1 to 5;
- emotional pressure;
- approximate shot count range, not a mandated count;
- expected meaningful-change interval;
- intended hold, breather, or stillness;
- proof load;
- audio pressure and quiet opportunity;
- entry responsibility;
- exit responsibility;
- why the sequence is necessary.

### Whole-episode rhythm checks

Reject or revise when:

- the episode stays at one energy level;
- every sequence begins with a reset;
- system mode dominates so completely that the viewer loses human reality;
- proof is isolated into a citation chapter rather than attached to the mechanism;
- several adjacent sequences reuse the same framing and action shape;
- the viewer receives no stillness before or after a major reveal;
- an important object disappears before its consequence;
- the completed system is never shown or run;
- the ending introduces rather than resolves the primary mechanic.

Cadence warnings remain diagnostic:

- opening and dense proof usually need meaningful development every 3-6 seconds;
- standard explanation usually needs meaningful development every 5-8 seconds;
- an unexplained static hold beyond 8 seconds is a warning;
- 16 seconds without a meaningful change is a hard failure.

Meaningful development is a new state, relationship, parameter, proof, handoff, failure, consequence, or motivated focus change. Decorative movement does not reset the clock.

## Artifact 3: look development

Look development proves the direction bible before the whole episode is directed.

### Required style frames

Create at least:

1. one reality-world frame;
2. one system-world frame;
3. one proof-bench frame;
4. one outcome or resolution frame.

Each uses real episode objects and real text. A mood board alone is not a style frame.

### Required motion test

Choose one 20-30 second passage that contains at least three of:

- reality;
- system explanation;
- evidence;
- recurring object continuity;
- meaningful transition;
- title or identity;
- failure or reversal;
- measurable outcome.

Use the locked VO. The test must demonstrate:

- one clear visual sentence at a time;
- VO-paced reveals across the sequence rather than front-loading;
- stillness after resolution;
- the approved motion grammar;
- at least one shot-to-shot handoff;
- the intended relationship between typography and imagery;
- the actual phone-scale and compression behavior.

Look development is approved only when the direction can plausibly scale across the episode. An impressive one-off effect that cannot support the remaining sequences is a failed test.

## Artifact 4: sequence treatment

Every visual-plan sequence receives a treatment before individual shots are specified.

Required fields:

- exact sequence ID, time, VO, and word range;
- story function;
- audience inference;
- viewer state before and after;
- dominant question and business verb;
- emotional tone;
- mode progression;
- picture/audio progression and the language carrier for each planned shot;
- visual sentence;
- object inheritance, introduction, change, retirement, and handoff;
- evidence requirement;
- documentary or synthetic requirement;
- sound intention;
- sequence concept in experiential language;
- approximate shot plan;
- scene context and justified choice of form, including stakes or their absence and emotional progression;
- entry frame responsibility;
- action and payoff;
- exit frame responsibility;
- complexity budget;
- at least three negative constraints;
- observable review checks.

The sequence concept describes the experience before it describes pixels. It is then translated into the shot board and exact directions.

## Artifact 5: shot board

The shot board is the cheapest visual approval surface. It uses real text and truthful placeholders but no finish.

Every shot displays:

- shot and sequence IDs;
- exact time range;
- exact VO excerpt;
- shot role;
- entry frame;
- key action frame or frames;
- consequence frame;
- exit frame;
- primary subject;
- supporting layers;
- evidence and source labels;
- asset placeholders and ticket IDs;
- what stays still, the master/setup relationship, and screen direction;
- typed continuity anchors and the initial and final image;
- incoming and outgoing transition handoff;
- one review question.

For a simple shot, entry, key action, and exit may be sufficient. A complex evidence or transformation shot may require additional key states.

The shot board approves composition, hierarchy, copy, and continuity. It does not approve motion quality, asset quality, color, or sound.

## Artifact 6: scene directions

`scene-directions.json` is the machine-readable compilation of approved direction and shot-board decisions.

### Required sequence direction

- audience inference;
- visual sentence;
- story function;
- viewer state before and after;
- dominant verb;
- energy and density;
- emotional tone;
- mode progression;
- persistent-object continuity;
- exact shot coverage;
- `scene_context` as defined in `SCENE-DIRECTION-CONTRACT.md`;
- negative constraints;
- observable animatic checks.

### Required shot direction

#### Identity and timing

- unique shot ID;
- exact episode in and out;
- exact locked word range and quote;
- shot role;
- purpose;
- visual mode;
- production lane or lanes;
- direction-bible and style-frame references.

#### Picture and audio

- picture/audio mode;
- language carrier;
- visible-speech rule;
- coverage grammar;
- face function;
- the concrete physical action;
- what the picture contributes beyond the soundtrack;
- the new information revealed by the angle;
- the mute-test result and reason.

Each shot also records `editorial_intent`: techniques, why this shot, entry/exit triggers, hold
intent, a simpler alternative considered, and an observable scene-specific review question.
Protect important actions, reactions, and pauses; cut frequency is not a quality measure.

Picture/audio mode follows scene context and precedes camera and coverage. Observational coverage
must remain complete without unheard dialogue. Narrated dramatization may show conversation when
the narrator supplies essential meaning. A close-up needs a mode-appropriate task, caused reaction,
or dramatic turn; facial presence alone is not a shot purpose.

`source_delivery` is valid only in `natural_sound_observation` with `visible_speech: source_synced`, `sound_intent.dialogue: sync_source`, `sound_intent.ambience: source`, audible synchronized source sound, and a mute test that expects the source line to be missing when muted; other natural-sound face functions keep the missing-line expectation false. `sync_dialogue` may use `sync_delivery`; `presenter_address` uses `presenter_delivery`. `narrated_observation` cannot use any delivery face function and keeps `missing_line_expected: false`.

#### Direction facts

These required shot-level facts sit adjacent to, not inside, the picture/audio contract:

- `what_stays_still`;
- `master_setup_relationship`, including role (`master`, `setup`, or `standalone`), `master_reference_id`, and a description of the relationship;
- `screen_direction`, including the action line, camera side, and subject direction;
- `continuity_anchors`, each with an ID, a typed kind (`world_object`, `asset_ticket`, `shot_layer`, `identity`, `wardrobe`, `prop`, `lighting`, or `spatial`), and a concrete description;
- `initial_image`;
- `final_image`.

A setup must reference a declared master shot or a declared asset ticket included in that shot's exact ticket dependencies. A master or standalone shot records a null master reference. World-object, asset-ticket, and shot-layer anchors must resolve to declared IDs.

Direction facts are generator-independent and non-optional. They apply equally to captured footage, selected source footage, generated plates, designed scenes, and composites. Unknown facts must be resolved or explicitly authored before a build packet is compiled; the generator or builder does not choose them.

Machine validation proves required structure and resolvable-reference integrity, not whether the authored facts are truthful or effective direction. That remains a review judgment.

#### Viewer attention

- primary subject;
- focal point;
- eye-start and eye-path;
- primary action;
- consequence;
- maximum concurrent meaningful actions;
- intended final read.

#### Action phases

Every non-trivial shot defines:

1. `establish`: minimum state required for orientation;
2. `anticipate`: optional preparation for the operation;
3. `act`: business verb or editorial reveal;
4. `consequence`: visible state change or inference;
5. `settle`: motion resolves and hierarchy stabilizes;
6. `hold`: explicit reading time;
7. `handoff`: outgoing state for the next shot.

A phase may have zero duration only when a hard cut or immediate state is intentional. Not every shot requires separate anticipate and hold phases, but their absence must not be accidental.

#### Composition

- frame and safe-area contract;
- composition family;
- visual hierarchy;
- background, midground, and foreground roles;
- layout anchors and relative proportions;
- exact implementation geometry;
- depth and occlusion;
- layer states and visibility windows;
- text and caption collision zones;
- evidence context zone;
- primary and secondary color roles.

Exact coordinates do not prove good composition. They are accepted only after the shot board proves the frame.

#### Camera

- framing;
- camera start and end framing as implementations of, not substitutes for, the complete `direction_facts.initial_image` and `direction_facts.final_image` descriptions;
- camera target;
- movement;
- purpose;
- camera implementation of `direction_facts.screen_direction`;
- lens and camera-height expectation for photographic or synthetic material;
- parallax and focus behavior;
- static alternative when the move is unnecessary.

#### Typography

- exact string;
- semantic type role;
- hierarchy;
- maximum lines;
- alignment;
- emphasis substring;
- reveal timing;
- reading hold;
- source/caveat behavior;
- caption-safe behavior.

#### Motion

- exact cue or editorial beat;
- targets;
- operation verb;
- deterministic property changes;
- start, duration, and settle;
- easing or named approved motion rule;
- explanatory purpose;
- collision with other actions;
- required rest state.

#### Transition

- default cut or motivated alternative;
- incoming and outgoing anchor;
- preserved object or property;
- outgoing vector and speed when relevant;
- incoming vector and speed when relevant;
- audio bridge;
- exact duration;
- why the transition expresses a real relationship.

#### Assets and evidence

- asset ticket IDs;
- selected asset IDs when available;
- placeholder behavior;
- source in/out requirements;
- handles;
- crop and focal point;
- evidence choreography;
- reconstruction and synthetic labels;
- provenance display requirements.

#### Sound

- narration authority;
- dialogue state: none, synchronized scripted, synchronized source, or presenter;
- music state;
- ambience state: none, source, designed post, or temporary reference;
- operational SFX;
- accent and silence moments;
- transition bridge;
- no-sound rationale when deliberately silent.

#### Review checks

Every shot has observable pass/fail statements covering:

- comprehension;
- hierarchy;
- timing;
- continuity;
- evidence or asset correctness;
- readability;
- motion purpose;
- handoff.
- picture/audio coherence, including the mute test and any narrator-led face function.
- completeness and reference integrity of the adjacent direction facts.

## Continuity contract

Continuity must be validated across adjacent shots, not only described inside each shot.

For every handoff, compare:

- persistent object ID;
- visible state;
- material appearance;
- color role;
- screen position;
- size and depth;
- movement vector and speed;
- route direction;
- text or value;
- evidence pin;
- sound tail;
- whether the object persists, transforms, exits, or is intentionally reset.

A transition's `preserve` list is incomplete unless the receiving shot confirms the same object or a declared transformation target.

## Cognitive-load contract

Every shot states a complexity budget:

- number of meaningful objects;
- number of simultaneous actions;
- number of visible labels;
- number of new concepts;
- reading time;
- evidence density;
- caption collision risk.

Default guidance:

- one primary action at a time;
- two to five meaningful objects in an ordinary designed composition;
- fewer when text or evidence is dense;
- a real source may fill the frame;
- supporting atmosphere does not compete for attention;
- if the viewer must pause to identify the primary action, simplify before adding labels.

## Prompt compilation contract

### Director packet inputs

A director packet must include:

- locked VO and word timings;
- approved plan units;
- relevant world slice;
- direction bible;
- rhythm-map entry;
- approved style-frame and motion-test references;
- prior exit state and next entry responsibility;
- evidence;
- asset tickets;
- shot-grammar options;
- the required picture/audio mode output contract and mute-test rules;
- the scene-context and editorial-intent output contract, including conditional dramatization safeguards;
- the required direction-facts output contract, available upstream anchor IDs, and in-artifact master-shot and shot-layer reference rules;
- exact output contract;
- negative constraints and stopping conditions.

### Build packet inputs

A HyperFrames build packet must include:

- the approved shot recipe;
- the approved sequence context and each shot's editorial rationale, without rerouting by narration keywords;
- the approved direction facts, including exact master and continuity references;
- the approved static key frames;
- `frame.md` and relevant design tokens;
- required local assets by manifest ID;
- named HyperFrames blueprints or rules when selected;
- composition ID, owned paths, and timing contract;
- expected motion sidecar;
- exact checks;
- continuity inputs and required exit state;
- forbidden creative changes.

Compile this packet using `../templates/episode/HYPERFRAMES-BUILD-PACKET.template.md`; do not reduce it to a generic style prompt.

### Asset-generation packet inputs

An archival, B-roll, original-capture, AI, music, SFX, or graphic packet is compiled only from an approved ticket plus the relevant shot direction. It does not receive the entire episode and guess what might look good. AI plates use `../templates/episode/AI-PLATE-GENERATION-PACKET.template.md`.

## Approval rule

No prose prompt, schema-valid JSON, static board, HyperFrames project, render, or Resolve timeline is automatically approved. Approval is a separate recorded decision over exact artifact hashes and review evidence.
