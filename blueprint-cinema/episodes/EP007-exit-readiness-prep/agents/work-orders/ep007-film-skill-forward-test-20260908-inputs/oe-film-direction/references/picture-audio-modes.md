# Picture/audio modes

Choose the mode from scene context before choosing coverage. It states where language lives and
how performance relates to that track. Narration alone does not select a mode.

## `narrated_observation`

The narrator carries language. The picture carries action, evidence, tension, consequence, and
human stakes.

- Visible speech: prohibited in generated plates. In real source footage, avoid sustained readable
  speech unless the source audio will be heard.
- Coverage: observational action, process, hands, objects, spatial relations, reactions caused by a
  visible event, and faces occupied by real tasks.
- Faces: `caused_reaction`, `task_focus`, `environmental_presence`, or `none`.
- Edit: every new angle must reveal a new action, object, spatial relationship, or consequence. Do
  not build a question/answer exchange under narration.
- Mute test: on mute, the viewer should not wait for a missing line. If a shot looks like someone is
  about to speak, answer, or listen to unheard dialogue, redesign or shorten it.

Natural ambience and precise foley may support the scene. They must not compete with the narration
or imply a factual event that did not occur.

## `narrated_dramatization`

The narrator carries the meaning of an illustrative enacted situation. The picture may show a
conversation, relationship, or attempted answer without audible character dialogue.

- Visible speech: `illustrative_only` permits motivated conversational mouth movement, not required
  constant talking or a claim of exact lip sync. Use `prohibited` for non-speaking shots.
- Coverage: `motivated_interaction`; choose two-shots, singles, OTS, reactions, details, or holds
  according to what changes. Reciprocal eyelines and an answer beat are allowed.
- Faces: `dramatic_performance`, `caused_reaction`, `task_focus`, `environmental_presence`, or `none`.
- Edit: coordinate the enacted turn with the approved narration. Protect important pauses; do not
  manufacture extra words, reactions, familiarity, or stakes.
- Mute test: record honestly whether unheard speech appears expected. Either result is possible;
  the decisive check is whether the actual narration supplies all essential meaning.

This mode requires explicit illustrative/non-evidentiary framing and a scene-specific audiovisual
comprehension check. No character dialogue is added (`sound_intent.dialogue: none`). Exact heard
lines require `sync_dialogue`; direct address requires `presenter_address`. Do not present a
dramatized exchange as an authentic case, verbatim testimony, or source recording.

## `sync_dialogue`

A scene participant carries language and the audience is meant to hear it.

- Visible speech: required and synchronized to the approved dialogue or source recording.
- Coverage: dialogue exchange with a locked action line, reciprocal eyelines, and coherent reaction
  shots.
- Faces: `sync_delivery` or `caused_reaction`.
- Edit: a reaction may land before, during, or after the line, but it cannot fabricate a response the
  audio does not contain.
- Mute test: missing dialogue should be expected. That is correct in this mode.

Do not generate dialogue merely to make a narrated plate feel alive. Use this mode only when the
heard exchange is part of the episode evidence or authored scene.

## `presenter_address`

The presenter, including a recurring talking-head avatar, speaks directly to the audience.

- Visible speech: required and synchronized to the approved presenter audio.
- Coverage: direct address. The eye line belongs at or deliberately adjacent to lens.
- Faces: `presenter_delivery`.
- Edit: use presenter returns as authored structural turns—opening, reframing, exception, or close—
  not as periodic proof of life.
- Mute test: missing speech should be expected. That is correct in this mode.

Treat presenter identity, voice, wardrobe, and set as continuity anchors. Do not disguise a
presenter segment as observational documentary footage.

## `natural_sound_observation`

Location sound, an interview fragment, or an observable event carries the moment.

- Visible speech: allowed only when the corresponding source sound is present; otherwise avoid it.
- Coverage: the physical event and its audible cause.
- Faces: `caused_reaction`, `task_focus`, `source_delivery`, or `environmental_presence`.
- Edit: preserve enough sound lead or tail for the event to read. A J- or L-cut is permitted when it
  makes causality clearer.
- Mute test: the missing sound event may be noticeable, but the picture must still identify the
  action.

This is not permission to add generic chatter or room activity to generated scenes.

## `silent_graphic`

The graphic carries a bounded visual explanation without dialogue. It may sit under narration or a
deliberate quiet beat.

- Visible speech: not applicable.
- Coverage: a finite graphic progression with a declared before state, operation, after state, and
  settle.
- Faces: `none` unless a real human image is itself the accountable subject.
- Edit: one focal change at a time. Follow Boundary Ledger's motion and scene contracts.
- Mute test: no human line should appear missing. The model must remain intelligible without sound;
  narration must remain intelligible without the graphic.

## Required direction record

For every shot, record:

- mode and language carrier;
- exact narration/source-audio range;
- shot job;
- primary physical action and what stays still;
- face function;
- visible-speech rule;
- master/setup relationship, screen direction, and continuity anchors;
- initial and final image;
- mute-test result and reason.

Also carry the sequence context and shot-specific editorial choices described in
[`context-and-coverage.md`](context-and-coverage.md). For canonical machine records, follow
`blueprint-cinema/references/SCENE-DIRECTION-CONTRACT.md`, including the dramatization safeguards.

If any value is unknown, mark it unknown. Do not let the generator decide it silently.
