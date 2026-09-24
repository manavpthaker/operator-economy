---
name: oe-film-direction
description: Choose context-sensitive film coverage, performance, and editing for OE documentary scenes, narrated dramatizations, generated plates, live footage, and presenter inserts. Use before shot planning, generation, or recutting; not for pure Working Model motion without filmed footage.
---

# OE Film Direction

Direct the situation, not the presence of a voiceover. Choose coverage and editing from what the
viewer must understand, whose experience matters, and what changes in the scene. Narration can
accompany observation, dramatized interaction, evidence, or explanation; it does not choose the
film grammar by itself.

Read [`references/context-and-coverage.md`](references/context-and-coverage.md) and
[`references/picture-audio-modes.md`](references/picture-audio-modes.md) before directing a scene.
For generated footage, also read
[`references/generated-plates.md`](references/generated-plates.md). The source record and the limits
of the external references are pinned in
[`references/source-ledger.json`](references/source-ledger.json).

Load the OE Boundary Ledger skill whenever the scene contains OE identity, a Working Model,
designed type, motion graphics, captions, or semantic color.

## Context to direction

1. Read the locked passage with its preceding and following beats. Identify the situation,
   relationship and stakes (or their absence), viewer knowledge, and emotional change. Do not invent
   conflict, familiarity, or a meeting history that the approved material does not establish.
2. Choose the scene form and picture/audio mode with a reason. Split a passage at meaningful mode
   changes. A visible conversation summarized by a narrator is `narrated_dramatization`, not
   automatically `sync_dialogue` or defective observation.
3. Choose only the film and editing techniques that solve this scene's needs. State why each setup
   is necessary, what motivates entry and exit, and which action or pause needs an uninterrupted
   hold. Consider a simpler alternative. Neither a five-setup package nor a cut-frequency target is
   a default.
4. Lock the master geography: actor positions, work surface, action line, screen direction, gaze,
   and the recurring object. Derive closer setups from that world.
5. Direct one primary physical action per generated clip. Specify observable behavior, what remains
   still, and the final image. Do not ask the model to perform an abstract feeling.
6. Assemble and trim for meaning before grading, effects, music, or transition polish. Cut when the
   next shot adds new information, not because a clip has remaining duration.
7. Review continuity and the selected mode's sound relationship. Treat mute viewing as a diagnostic,
   not a universal veto on conversation. Review at speed with the actual track: does the intended
   inference land, does pressure change on the right beat, and does the edit preserve the important
   performance? A schema pass or silent sample does not answer these questions.

## Non-negotiable boundaries

- A face is not automatically emotional coverage. A close-up needs a caused reaction, task focus,
  presenter delivery, or another declared function.
- Choose speech constraints by mode. Narrated dramatization may show motivated conversational
  behavior without audible character lines; it must not pretend to be synchronized dialogue,
  verbatim testimony, or evidence. Presenter and sync-dialogue delivery require their exact approved
  audio. Never reuse a talking-head take against different words.
- Camera movement must reveal, follow, reframe, or apply pressure. A slow push, pan, or close-up is
  not cinematic by itself.
- Preserve character, wardrobe, location, object, lighting, geography, and screen direction across
  generated setups. Regeneration is not permission to redesign the world.
- Never fabricate legible books, dashboards, documents, or screens when their contents are not the
  point. Frame them obliquely, shallow, partial, or out of focus while keeping the physical action
  readable.
- Generated people and reconstructed scenes are illustrative plates, not evidence. Keep factual
  proof on attributable evidence surfaces.
- External references inform this OE synthesis. They do not govern OE, choose its runtime, or
  override Boundary Ledger, the Canvas, locked narration, Blueprint Cinema, or human approval.

## Handoff

Carry `scene_context` and each shot's `editorial_intent` into the direction record, alongside the
picture/audio contract, direction facts, exact cues, and review checks. Use the Blueprint Cinema
scene-direction contract for machine field names. Generation packets retain the chosen performance
and coverage logic; build packets implement it rather than choosing again. Missing context returns
to direction, not to a generator's guesses. No skill decision expands media spend or approval.
