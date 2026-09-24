# Boundary Ledger scene contracts

These contracts are runtime-neutral. They describe what a scene means and what a builder must prove;
they do not prescribe HTML, React, HyperFrames, Resolve, or another implementation.

## `ModelField`

The stable paper world containing persistent actors, objects, routes, revisions, and evidence
anchors. Roughness is authored into marks. The field never jitters as ambient texture.

Required: aspect-specific composition, persistent object IDs, current and owned routes, one declared
commitment locus, stable start and end states, and a reduced-motion end state.

The locked EP006 JPEG is a flattened still reference. It cannot by itself prove object permanence,
rough-stroke reveal, or independent route motion. A production scene needs a derivative that passes
[`motion-ready-asset.schema.json`](./motion-ready-asset.schema.json): separately authored object,
steel-route, oxide-route, evidence, and correction layers or masks. Preserve the locked source still;
never overwrite it to create a motion asset.

## `DependencyRoute`

The current path through an external or rented capability. It must identify what moves, what the
dependency supplies, what it costs or constrains, and where accountability transfers. It is steel,
not automatically risk.

## `DecisionPath`

The single operator-controlled path or exception active in the scene. It becomes oxide only when the
decision or route is actually available. It cannot run concurrently with a second oxide locus.

## `PersistentObject`

A recognizable customer, key, case, payment, claim, task, or outcome object whose identity survives
handoffs and aspect-ratio recompositions. Do not replace the “before” object with a new success icon.

## `EvidencePin`

A source, date, claim state, and supported value attached to the exact object or parameter it informs.
It cannot convert `UNKNOWN`, estimate, or reported evidence into a verified claim.

## `AccountableRecord`

The temporal family derived from the web docket: identity docket, evidence receipt, decision record,
chapter rail, or lower third. It enters, attaches, and holds. It is not a persistent HUD.

## `ThesisType`

Typeset phrase used only when the thesis, reversal, warning, exact quote, or critical number is the
visual subject. It declares its embedded thesis phrase so caption validation can reject duplication.

The caption state for that phrase is `embed`, following the canonical `drop / rail / embed` model.
“Promote” describes the editorial decision, not a fourth caption state.

## `VoiceTrace`

A deterministic temporal index derived from a hashed audio asset. It records source checksum,
extraction settings, derived checksum, time range, semantic purpose, silent behavior, and whether a
literal waveform is justified.

## `PictureAudioContract`

A moving-image binding that declares where language lives before coverage is designed. It is not a
semantic-core role or operation. Scene context determines the form and coverage; narration alone
does not. Every shot selects exactly one mode:

- `narrated_observation` — the narrator carries language; the picture carries observable
  action, evidence, tension, consequence, or human stakes. Generated plates prohibit readable
  speech, angles do not simulate a dialogue exchange, and a muted viewer must not wait for a missing
  line.
- `narrated_dramatization` — an explicitly illustrative enacted situation. The narrator supplies
  essential meaning; motivated conversational performance, reciprocal eyelines, and answer/reaction
  coverage are allowed. No character dialogue is added or exact sync claimed. Disclosure and
  actual-audio comprehension review are required; mute viewing is diagnostic.
- `sync_dialogue` — a participant carries approved or sourced dialogue. Visible speech is required
  and synchronized; action line, eyelines, and reactions remain coherent.
- `presenter_address` — the presenter speaks to the audience. Visible speech is required and
  synchronized; presenter returns mark authored structural turns rather than periodic activity.
- `natural_sound_observation` — a sourced audible event carries the moment. Visible speech is
  allowed only with its corresponding source sound.
- `silent_graphic` — a finite graphic progression carries a bounded explanation without visible
  speech. It declares before state, operation, after state, and settle.

Required for each shot: mode, language carrier, narration or source-audio range, shot job, primary
physical action, what stays still, face function, visible-speech rule, master/setup relationship,
screen direction, continuity anchors, initial image, final image, and mute diagnostic with reason.
Also record scene context, technique selection, entry/exit motivation, protected hold or its
absence, a simpler alternative considered, and a scene-specific audiovisual review question.
Unknown values remain explicit; a generator may not decide them silently. The allowed behavior is
locked in the OE film-direction skill's `picture-audio-modes.md` reference.

## `SceneManifest`

Every designed scene or audio-led clip should record:

- system and binding version;
- surface and exact aspect ratio;
- semantic state before and after;
- primary persistent object and business/editorial operation;
- role IDs for human context, dependency, evidence, commitment, risk, and outcome when present;
- one commitment locus or an explicit `none`;
- exact visible text, transcript hash, and word/time cues;
- finite motion events with purpose and property changes;
- carrier identity for any designed transition;
- evidence/source IDs for factual values;
- audio checksum, derived-data checksum, and extraction settings for audio-linked behavior;
- caption policy and any embedded thesis phrase;
- picture/audio mode, language carrier, visible-speech rule, face function, shot job, continuity
  anchors, and mute-test result for every moving-image shot;
- aspect-specific model asset or explicit unsupported format;
- reduced-motion end state;
- review state and failed checks.

Static validation rejects unknown role IDs, more than one active commitment, ambient or infinite
loops, motion without an operation and state change, audio reactivity without frozen source data,
evidence without provenance, embedded text duplicated in captions, crop-based adaptation, or a
transition whose carrier identity changes. Moving-image validation also rejects an undeclared
picture/audio mode, readable generated speech under `narrated_observation`, incompatible dialogue
and language carriers, or a missing-line expectation in narrated observation. Narrated dramatization
requires illustrative disclosure and narration-carried essential meaning; it is not a loophole for
source testimony, exact lip sync, or invented evidence.

Human review remains required for relationship comprehension, false implication, roughness,
caption judgment, encoded quality, and whether the drama comes from causality rather than effects.
