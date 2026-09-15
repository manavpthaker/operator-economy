# Editing and scene-construction nuance

This reference translates the Blueprint Cinema direction into practical editorial judgment. It is episode-agnostic and subordinate to `../../docs/blueprint-cinema.md`.

## The unit of editing

The unit is a meaningful change in the viewer's understanding, not a sentence, beat, card, or transition.

A single scene may cover several narration beats while the system is actively building or running. A narration beat may also require several internal events without changing the overall camera view. The question is always: what changed in the business state, the evidence, the human stakes, or the viewer's focus?

## The visual hierarchy

At any moment the viewer should be able to identify:

1. The primary subject or object.
2. The action occurring now.
3. The consequence of that action.
4. Supporting labels or evidence.

Do not animate several unrelated ideas at once. If a value changes system behavior, show the value, its destination, and the consequence in that order.

## Avoiding the beginner motion-graphics look

The beginner look is usually not caused by weak software technique. It comes from visible effects without an underlying visual idea.

Common symptoms:

- Every noun receives an icon.
- Every sentence becomes a fresh composition.
- Text and boxes enter from arbitrary directions.
- Easing, overshoot, glow, parallax, or camera drift is applied uniformly.
- Transition packs call attention to themselves.
- Everything moves because nothing has a clear priority.
- The same card layout is reused with different nouns.
- Style changes substitute for a real narrative state change.

Corrections:

- Establish one persistent space and let objects remain.
- Animate operations: route, qualify, approve, reject, hand off, recover, suppress, retry, measure.
- Prefer a clean cut when no relationship needs explanation.
- Keep most motion restrained so a real failure, reversal, or outcome has contrast.
- Use camera movement to follow work, reveal scale, or change explanatory altitude.
- Let stillness carry confidence when the evidence or human moment deserves attention.

## Scene anatomy

A strong designed scene has:

- an established world state;
- one current action;
- persistent objects with recognizable IDs and positions;
- a motivated focus change;
- a readable before/action/after progression;
- an exit state that the next scene can inherit.

If a scene cannot name its before state and after state, it is probably decoration or illustration rather than explanation.

## Transitions

The default transition is a cut. Use a designed transition only when it communicates one of these relationships:

- reality resolves into blueprint geometry;
- evidence pins to the node it validates;
- a sourced parameter enters the model and changes behavior;
- the camera follows work through a handoff;
- a working connection fails or reroutes;
- the camera pulls back to reveal accumulated system state.

Avoid random wipes, repeated elastic motion, decorative zoom tunnels, transitions that erase object permanence, or a different transition for every section.

## Reality, system, and proof

Reality footage creates human and physical contact. The system world explains invisible mechanics. The proof bench establishes trust. A strong edit moves among them for a reason:

- Reality asks, "Who feels this and what happens?"
- System asks, "What produces it and how can it change?"
- Proof asks, "Why should I believe this parameter or claim?"

Do not use B-roll to explain a workflow or a flowchart to create human stakes. Do not use an AI render as proof.

## B-roll and archival footage

Every footage ticket gets one primary role:

- `human_context`
- `market_force`
- `proof`
- `process`
- `outcome`

Select footage by semantic need, not keyword proximity. A hotel exterior may establish place but does not prove OTA economics, show a consent handoff, or demonstrate a direct-booking path.

Prefer, in order:

1. Original capture for interfaces, proof, and process.
2. Permissioned or licensed company material for specific market forces.
3. Licensed archival for a real historical claim.
4. Specific licensed stock for human context or outcomes.
5. Synthetic environmental plates only where capture is impractical and the material is clearly non-evidentiary.

## AI-rendered scenes

Use one coherent rendered world per episode, usually for a small number of purposeful sequences. Maintain recurring people, environments, lighting, screen direction, lens behavior, and object motifs.

Generate environmental plates, not fake finished evidence. Composite accurate text, interfaces, prices, brands, documents, and UI afterward. Record synthetic status and the disclosure requirement in the asset manifest.

Weak uses include a generated clip for every sentence, generic futuristic offices, decorative data tunnels, fake app interfaces, and photoreal people presented as documentary subjects.

## Evidence treatment

Use the full evidence motion:

```text
source appears
  -> relevant element is highlighted
  -> value or claim is extracted
  -> it enters the relevant system node
  -> system behavior changes
  -> the source remains pinned as context
```

Do not flash a citation card and discard it. Do not reconstruct an interface or document without labeling the reconstruction. Never place synthetic material where the viewer would reasonably read it as evidence.

## Pacing

Cadence is a diagnostic, not a metronome:

- Opening: meaningful change every 3-6 seconds.
- Dense proof: annotation or internal change every 3-6 seconds.
- Standard explanation: meaningful change every 5-8 seconds.
- Longer holds are valid while a composition is actively building, running, or allowing a human/evidence moment to land.
- An unexplained static hold beyond 8 seconds is a warning; 16 seconds is a hard failure.

Meaningful change can be a state transition, new evidence, a changed parameter, a motivated camera move, a failure, a handoff, or a shift between reality/system/proof. It is not a decorative pulse.

## Text and legibility

Text labels components, variables, sources, and decisions. It does not repeat the narration.

At 1920x1080, use the canonical Blueprint Cinema standard as the starting point: approximately 72-108 px headlines, 140-240 px critical numbers, 44-60 px explanatory labels, and 26-34 px sources. Keep essential content within roughly 7% horizontal and 6% vertical safe margins.

Validate at 50% scale and a phone-sized preview. If the viewer must pause to understand the primary action, simplify the scene rather than adding more labels.

## Sound

Narration remains the authority. Music provides structure and emotional pressure without competing with speech. Sound design should clarify operations: a handoff, lock, failure, queue, confirmation, or state change. Avoid attaching a sound effect to every animation.

The final mix, loudness, peaks, captions, and synthetic-media disclosure remain subject to existing OE delivery contracts until the implementation records a deliberate replacement.

## Review questions

For every sequence, ask:

- What was true before this sequence?
- What operation or decision occurred?
- What is true afterward?
- Which object or idea carries into the next sequence?
- Is the evidence attached to what it proves?
- Did the motion express the business or advertise the animation software?
- Could a simpler cut or hold communicate the idea more clearly?
- Does the sequence make the blueprint more actionable?
