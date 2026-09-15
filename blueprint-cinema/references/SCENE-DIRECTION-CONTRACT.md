# Scene direction and prompt compilation

Blueprint Cinema does not treat a prose prompt as a substitute for directing. A useful build prompt is the compiled form of explicit creative decisions.

## Why this layer exists

The episode engine defines the business mechanic. The world defines persistent objects and valid relationships. The visual plan maps business state changes to exact narration. None of those artifacts fully describes the frame the audience sees.

`scene-directions.json` supplies the missing shot-level contract:

```text
locked words and timing
  + approved business state change
  + persistent object identities
  + approved direction bible and rhythm intent
  + approved style frames and visual-language test
  + prior-shot exit and next-shot entry
  + scene context and justified editorial choices
  + picture/audio mode and language carrier
  + adjacent generator-independent direction facts
  + exact composition and hierarchy
  + exact text and emphasis
  + word-cued motion choreography
  + transition continuity
  = buildable shot recipe
```

The system uses two prompt passes because directing and implementation require different judgment.

## Pass 1: director packets

Run:

```bash
blueprint-cinema/bin/oe-cinema build-director-prompts EP006-direct-booking-recovery
```

Or generate a bounded sequence packet:

```bash
blueprint-cinema/bin/oe-cinema build-director-prompts EP006-direct-booking-recovery \
  --sequence sequence-hook-01
```

The command writes deterministic, hash-pinned packets to:

```text
episodes/EP###-slug/prompts/generated/director/
```

Each packet contains the exact VO and word table, approved units, relevant world slice, evidence, asset tickets, episode mechanic, direction bible, rhythm-map rows, approved style-frame references, prior exit state, next entry requirement, frame contract, and non-negotiable directing questions. It asks a director—human or agent—to author scene decisions, not animation code.

Director packets are generated context. They do not constitute scene direction, approval, a directed animatic, or authorization to generate media.

## Authored scene direction

The integrator merges reviewed sequence decisions into:

```text
episodes/EP###-slug/scene-directions.json
```

Every sequence must state:

- `scene_context`: situation, scene form, reason for that form, stakes (or their absence), and emotional progression;
- the audience inference;
- a visual sentence: subject, relationship, object, consequence, before, and after;
- persistent objects inherited, introduced, retired, and handed forward;
- exact shots covering the sequence without gaps or overlaps;
- at least three negative constraints;
- at least five observable animatic review checks.

Every shot must state:

- exact episode time and locked word range;
- production lane;
- purpose and mode;
- picture/audio mode, language carrier, visible-speech rule, coverage grammar, face function, concrete physical action, and mute-test result;
- `editorial_intent`: selected techniques, why this shot, entry and exit triggers, hold intent, a simpler alternative considered, and a scene-specific review question;
- adjacent `direction_facts`: what stays still; master/setup role, exact master reference, and relationship; action line, camera side, and subject direction; typed continuity anchors; initial image; and final image;
- camera framing and motivated movement;
- every layer's source, normalized and 1920x1080 reference bounds, depth, opacity, state, and visual role;
- the single primary layer and complete visual hierarchy;
- every visible text string, type role, size, line count, and timed substring emphasis;
- every motion beat's absolute time, exact cue word index and timestamp, duration, targets, property changes, easing, and explanatory purpose;
- transition in and out, including preserved layers;
- the complete evidence choreography when proof appears;
- exact ticket dependencies and explicit narration, dialogue, ambience, music, and sound-design intent.

Choose the scene form from context, not from the presence of narration. `narrated_observation` carries observed action without a performed exchange; its visible-speech and missing-line restrictions remain. `narrated_dramatization` carries an explicitly illustrative enacted situation whose essential meaning comes from the narrator. It permits reciprocal eyelines, an attempted answer, and motivated close/reverse coverage. Use `coverage_grammar: motivated_interaction`, `visible_speech: illustrative_only` (or `prohibited` for a non-speaking shot), and `face_function: dramatic_performance`, `caused_reaction`, `task_focus`, `environmental_presence`, or `none`. It requires narration and forbids added character dialogue.

Every dramatized shot also supplies `dramatization_context`: `representation: illustrative`, `essential_meaning: narration`, an explicit `disclosure_plan`, and an observable `audio_review_check`. Neither `missing_line_expected` value is automatically a failure in this mode: mute viewing is diagnostic; the actual soundtrack must supply the essential meaning without unavailable exact words. The record is a review plan, not a claim that ungenerated footage passed playback.

`scene_context` uses non-empty authored strings: `situation`, `scene_form`, `form_reason`, `stakes`, and `emotional_arc`. Scene form is not a keyword-routing enum; describe the relevant form or mixed progression. `editorial_intent` contains `techniques` (an authored list), `why_this_shot`, `entry_trigger`, `exit_trigger`, `hold_intent`, `alternative_considered`, and `review_question`. No fixed angle count, cutting interval, dramatic escalation, or particular technique is required. Use an explicit absence where stakes or a protected hold are unnecessary. Validation checks this record; it never selects the technique or evaluates its artistic merit.

Delivery face functions are mode-bound. `source_delivery` is allowed only in `natural_sound_observation` with `visible_speech: source_synced`, `sound_intent.dialogue: sync_source`, `sound_intent.ambience: source`, audible synchronized source sound, and `mute_test.missing_line_expected: true`; other natural-sound face functions keep the missing-line expectation false. `sync_dialogue` may use `sync_delivery`; `presenter_address` uses `presenter_delivery`. `narrated_observation` cannot use any delivery face function and keeps `missing_line_expected: false`. `silent_graphic` may sit under narration or deliberate silence but contains no performed speech. The visual mode—reality, system, proof, identity, or outcome—remains independent of this contract.

`direction_facts` is adjacent to, not nested inside, `picture_audio_contract`. Every shot must name `what_stays_still`; a `master_setup_relationship` with role `master`, `setup`, or `standalone`; `screen_direction` with action line, camera side, and subject direction; one or more typed `continuity_anchors`; and concrete `initial_image` and `final_image` descriptions. A setup references a declared master shot or a declared asset ticket included in that shot's exact ticket dependencies; master and standalone shots use a null master reference. Anchor kinds are `world_object`, `asset_ticket`, `shot_layer`, `identity`, `wardrobe`, `prop`, `lighting`, and `spatial`; the first three must resolve to declared IDs.

These facts are non-optional and generator-independent. Captured footage, source footage, generated plates, designed scenes, and composites all use the same record. A generator, editor, or builder may implement the facts but may not supply or reinterpret missing ones.

Coordinates make direction testable, but they do not replace the approved shot board. The shot board establishes the audience frame, relationship, hierarchy, screen direction, and handoff. The coordinates encode that decision for implementation.

Validation rejects stale hashes, invented IDs, inexact VO, loose timing, incomplete frame coverage, missing layers, out-of-frame geometry, dangling tickets or evidence, incoherent picture/audio combinations, invalid delivery face functions, observation-mode speech or missing-line expectations, missing context/editorial rationale or dramatization safeguards, missing direction facts, unresolved setup references, dangling resolvable continuity anchors, inexact cue times, unbound text emphasis, incomplete evidence motion, and decorative motion without an explicit property change.

The validator proves required presence, allowed structure, and reference integrity. It does not prove that the authored descriptions are truthful or effective direction; that remains a review judgment.

## Pass 2: build packets

After the authored file validates:

```bash
blueprint-cinema/bin/oe-cinema validate-scene-directions EP006-direct-booking-recovery
blueprint-cinema/bin/oe-cinema build-scene-prompts EP006-direct-booking-recovery
```

The compiler writes one implementation packet per shot to:

```text
episodes/EP###-slug/prompts/generated/build/<sequence-id>/<shot-id>.md
```

The build packet does not ask the implementer to make new layout decisions. It carries the approved shot recipe, continuity, constraints, and checks into a bounded HyperFrames composition, evidence-capture, B-roll, AI-plate, audio, Resolve-handoff, or composite task.

For a HyperFrames composition, the packet additionally specifies the owned composition path, composition ID, timing slot, local manifest IDs, root-versus-scene responsibilities, static end-state snapshot, motion phases, required first/action/consequence/exit snapshots, lint/check expectations, output format, handles, alpha expectation, and sidecar report path.

## What this prevents

- A model choosing layouts from narration nouns.
- “Highlight the number” without naming the text, substring, cue, duration, and treatment.
- “Move the guest through the system” without start/end geometry and timing.
- A transition that erases recurring object identity.
- AI media being used as evidence.
- A builder making unreviewed directing choices while writing code.
- An exchange forced into observational grammar, or dramatization mistaken for synchronized dialogue or evidence.
- A facial close-up used as generic cinematic emphasis rather than a motivated performance, task, or caused reaction.
- Source delivery shown without its audible synchronized source.
- A closer setup that silently invents its master, screen direction, continuity, start image, or end image.
- Polished assets being produced before the causal scene works in the animatic.

## Current gate boundary

The existing v1 command and scene-direction schema 1.2.0 implement this bounded authoring and compilation layer, not the complete production system. Version 1.2.0 adds required scene context, shot editorial intent, and explicit narrated dramatization. Prior 1.1.0 packets are preserved historical artifacts; they must be deliberately reauthored and revalidated before new compilation. Do not auto-fill rationale, silently bump a version, rewrite old generated prompts, or inherit approval. These commands do not add or advance a production-state approval. EP006 remains at its recorded state; R7 and other experiments remain separate. The full HyperFrames/Resolve state-machine migration is still unimplemented.
