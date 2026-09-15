# Blueprint Cinema workflow

## Full lifecycle

Blueprint Cinema receives an episode only after upstream editorial work is locked:

```text
research -> claims -> approved script -> final VO -> word timings
  -> input lock
  -> episode engine
  -> persistent world
  -> full-timeline visual plan
  -> direction bible and rhythm map
  -> look development and representative motion test
  -> sequence treatments, shot boards, and scene directions
  -> HyperFrames whole-episode directed animatic
  -> exact asset candidates, selects, and production
  -> HyperFrames scene and graphic plates
  -> Resolve conform and rough cut
  -> picture lock
  -> Fusion, color, Fairlight, captions, and online
  -> delivery validation
```

The target production-state sequence is:

1. `inputs_locked`
2. `episode_engine_approved`
3. `world_approved`
4. `visual_plan_approved`
5. `visual_language_approved`
6. `scene_direction_approved`
7. `directed_animatic_approved`
8. `asset_selects_ready`
9. `rough_cut_approved`
10. `picture_lock_approved`
11. `finish_approved`
12. `delivery_validated`

Each approval records the hashes it covers. Changing an approved upstream artifact invalidates dependent downstream states. The current v1 implementation still uses `greybox_ready`, `greybox_approved`, `assets_ready`, and `fine_cut_approved`; those names remain historical until the runtime and schema migration is implemented.

## Stage 0: initialize and lock inputs

Create the numbered episode identity, resolve the upstream editorial workspace, and hash the exact approved script, final audio, mastered sections, word timings, evidence indexes, and timeline. Probe media duration and verify all timing bounds.

This stage is serialized. It establishes the truth every later worker must cite. It does not copy old storyboards, coverage assignments, scene code, or visual approvals.

Exit evidence:

- matching `EP###-slug` identity;
- approved-script hash agreement;
- exact VO and word-timing hashes;
- contiguous, duration-valid timeline;
- explicit input provenance and excluded legacy paths.

## Stage 1: episode engine

Define the operator, customer or subject, owned value, constraint, counter-system, outcome object, visual mechanic, primary motion verbs, reality-world premise, and guardrails.

One author owns the engine draft. Independent critics may review mechanical honesty, editorial fairness, evidence requirements, actionable payoff, and visual cliché. Only the orchestrator merges and the showrunner approves.

The engine fails when it is only a topic, metaphor, mood, channel imitation, or list of scenes.

## Stage 2: persistent world

Define stable objects, zones, paths, state transitions, evidence anchors, failure routes, money flows, human gates, camera anchors, and object permanence. In parallel, bounded workers may produce:

- a transcript and narrative-state map;
- an evidence-to-claim index;
- a failure, consent, exception, and human-judgment audit.

The world author consumes those packets after their input hashes are verified. The world must support the failure path, counter-system, economics, stress test, and outcome without inventing new objects whenever the narration changes subject.

## Stage 3: full-timeline visual plan

Map the exact VO to coherent persistent sequences. Each timed unit states:

- viewer knowledge before and after;
- business state before, operation, and state after;
- active reality, system, proof, or outcome mode;
- objects inherited, introduced, transformed, handed forward, and retired;
- evidence and human contact requirements;
- asset requirements and sound function;
- the transition relationship to adjacent sequences.

A beat is not automatically a shot. Segment proposals may be parallelized only when workers own non-overlapping time ranges and use the same approved world IDs. One plan integrator resolves boundaries, carries, repetition, cadence, and complete timeline coverage.

## Stage 4: direction bible and rhythm map

The creative director converts the engine and visual plan into one episode-specific visual language. Author:

- `direction/direction-bible.md` from the canonical template;
- `direction/rhythm-map.md` for the entire VO;
- the approved visual hierarchy, palette roles, typography roles, surfaces, depth, texture, camera rules, motion language, transition rules, evidence treatment, footage treatment, AI-plate rules, sound world, accessibility rules, and explicit anti-rules.

The rhythm map identifies changes in energy, density, scale, visual mode, proof, human contact, sound, and breathing room. It prevents every scene from using the same composition, pace, and intensity while still preserving one coherent world.

No scene animation begins at this stage.

## Stage 5: look development and representative motion test

Select the hardest representative material rather than the prettiest opening. Create style frames that test:

- reality world;
- system world;
- proof bench and source legibility;
- economics or data;
- an exception or failure state;
- the intended relationship among footage, graphic space, typography, and texture.

Then build one 20-30 second representative HyperFrames motion test containing a persistent object, a business operation, evidence or footage, a meaningful transition, real text, and a readable settle.

Approve visual language only when the stills and motion work together at desktop, 50% scale, and phone-size review. A polished title card alone cannot approve the language.

## Stage 6: sequence treatment and static shot board

For every sequence, define the audience inference, visual sentence, production lanes, persistent carries, proof requirements, asset dependencies, sound function, and handoff.

Board the actual shots with real text and truthful placeholder geometry. Every shot needs at least:

1. entry frame;
2. key action or reveal frame;
3. consequence or settle frame;
4. exit or handoff frame when it differs materially.

Review the board as a sequence before specifying animation. It must answer what the viewer is looking at, why it matters now, what changes, where the eye goes next, and what survives the cut.

## Stage 7: scene direction and prompt compilation

Generate hash-pinned director packets from approved artifacts. Author and validate exact shot directions covering:

- episode time and word cues;
- shot purpose and audience inference;
- camera, composition, depth, hierarchy, and screen direction;
- every visible text string and timed emphasis;
- entry, action, consequence, settle, and handoff phases;
- evidence choreography and asset IDs;
- motion properties, durations, easing, and explanatory purpose;
- transition in, transition out, continuity, sound intent, and negative constraints;
- observable review checks.

Compile bounded HyperFrames build packets only from approved direction. Prompt generation never records approval. A coordinate list is not direction unless it expresses the intended relationship, hierarchy, and action.

## Stage 8: whole-episode directed animatic

Build the entire episode in HyperFrames against the locked VO. Use actual typography, composition, timing, camera, motion intent, evidence placeholders, asset IDs, and transition handoffs. Use simple shapes, low-cost proxies, or conspicuous placeholders where final media is unavailable.

The animatic answers:

- Can the audience follow the causal system without reading production notes?
- Does every sequence change viewer understanding?
- Are shot relationships, screen direction, and object continuity coherent?
- Does visual density track narrative density?
- Are the evidence moments comprehensible and long enough to read?
- Do reality, system, and proof modes alternate with intention?
- Are there real holds and breaths after important reveals?
- Does the episode work as a complete film rather than a chain of animated cards?

Run `npx hyperframes lint` during authoring, `npx hyperframes check` as the final automated gate, scene snapshots, assembled animation-map review, Studio preview, full-duration technical render, media probe, and independent creative review. The animatic is unfinished, but it must not be vague.

## Stage 9: exact asset candidates, selects, and production

After animatic approval, issue exact asset tickets. Ticket lanes may include:

- original evidence or interface capture;
- permissioned or licensed B-roll and archival;
- original documentary capture;
- AI-rendered environmental or metaphorical plates;
- diagrams, charts, maps, typography, and motion components;
- music, ambience, SFX, and captions.

Searches produce candidates, not assets. A producer recommends a select; an authorized reviewer accepts it; the media manager freezes it locally, calculates hashes, creates derivatives and proxies, and records rights, provenance, technical metadata, synthetic status, restrictions, source in/out points, handles, crop, focal position, and intended timeline use.

No raw URL, generic download, or attractive substitute enters the canonical edit.

## Stage 10: HyperFrames production render

Replace animatic placeholders with approved media and finished designed elements. Scene builders work only on bounded sequence or shot compositions. The HyperFrames technical director owns the thin root composition, shared runtime, local media, pinned version, checks, and render settings.

Render:

- opaque scene plates for self-contained scenes;
- alpha MOV, WebM, or RGBA image sequences for graphics that Resolve must composite;
- a full reference render preserving exact approved timing;
- handles where the edit plan authorizes them;
- a manifest connecting every output to sequence, shot, asset, evidence, version, and source hash.

Do not render text into a plate that the finishing plan requires to remain editable unless the exception is recorded.

## Stage 11: Resolve conform and rough cut

Create the Resolve project from the handoff manifest, approved animatic reference, interchange files, markers, selects, proxies, source media, HyperFrames plates, VO, music, SFX, ambience, captions, and color metadata.

The lead editor owns one canonical timeline. Conform checks include duration, timebase, source mapping, missing media, in/out points, handles, scale, alpha, color interpretation, VO sync, markers, and agreement with the animatic reference.

The rough cut establishes story, coverage, source readability, J- and L-cuts, documentary rhythm, graphic-to-footage relationships, and sound structure. It may refine timing within approved intent. It may not silently change meaning.

## Stage 12: picture lock

Picture lock is an editorial approval, not a render milestone. It requires:

- no open blocking editorial, evidence, rights, continuity, disclosure, or asset findings;
- agreed shot order, duration, transition meaning, source display, title, caption, and disclosure placement;
- agreement among Blueprint Cinema edit manifest, Resolve timeline, HyperFrames plate manifest, and approved reference;
- explicit logging of every permitted trim and every returned direction change.

After picture lock, changes that affect duration or composition require controlled reopening and downstream invalidation.

## Stage 13: finish in Resolve

Finish departments work from picture lock:

- **Online and Fusion:** relink full-resolution media, repair composites, track, mask, key, clean up, and integrate approved graphics.
- **Color:** establish color management, normalize, correct, match, protect factual color and skin, integrate source types, apply the creative grade, and review scopes plus compressed outputs.
- **Fairlight:** clean and level VO, shape ambience, edit music, place operation-focused SFX, automate, carve competing frequencies, verify phase, loudness, and true peak, and print required stems.
- **Captions and accessibility:** verify words, segmentation, reading speed, safe placement, collisions, and delivery formats.
- **Online:** confirm titles, sources, legal/disclosure slates, frame edges, fine lines, gradients, and compression behavior.

Each department produces a report bound to the exact timeline and media hashes it reviewed.

## Stage 14: delivery validation and handoff

Render and inspect the high-quality mezzanine, platform upload master, captions, final mix or stems, and archival package. Validate duration, frame rate, resolution, codec, color tags, audio streams, loudness, true peak, caption sync, black frames, freezes, flash frames, missing media, truncated text, source legibility, and synthetic disclosure.

Watch the rendered master from beginning to end. Timeline playback is not delivery QC.

The validated master then returns to the existing OE Shorts, packaging, upload, `links.json`, and content-os release process. A local render never implies scheduled, uploaded, published, or independently verified.

## Review and stopping rule

Use the cheapest artifact that can answer the open question. Stop when a blocking ambiguity appears upstream: missing claim evidence, unresolved scene purpose, unapproved visual language, unlicensed media, stale hashes, failed full-duration render, broken conform, or a Resolve change that alters meaning. Record the narrow blocker and continue only with independent work that cannot be invalidated by it.

Detailed gates and severity rules live in `references/REVIEW-QA.md`.
