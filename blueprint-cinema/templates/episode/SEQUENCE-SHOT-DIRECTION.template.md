# `<sequence-id>` — sequence and shot direction

## Control

- Episode:
- Input hashes:
- Direction-bible version:
- Rhythm-map entry:
- Sequence time:
- Locked word range:
- Exact VO:
- Previous exit state:
- Next entry responsibility:
- Status:

## Sequence treatment

- Story function:
- Audience inference:
- Viewer state before:
- Viewer state after:
- Question answered:
- Dominant business verb:
- Emotional tone:
- Energy, 1-5:
- Information density, 1-5:
- Mode progression:
- Picture/audio progression:
- Visual sentence:
- Concept / experience:
- Objects inherited:
- Objects introduced:
- Objects changed:
- Objects retired:
- Evidence requirement:
- Documentary requirement:
- AI or rendered-plate requirement:
- Sound intention:
- Entry frame responsibility:
- Action and payoff:
- Exit frame responsibility:
- Complexity budget:
- Approximate shot plan:
- Scene context — situation / scene form / form reason / stakes or absence / emotional arc:
- Why this sequence needs these film/editing tools:
- Important turn, reading hold, or pause to protect:

## Negative constraints

1. Do not:
2. Do not:
3. Do not:

## Sequence review checks

1. The viewer can observe:
2. The viewer can observe:
3. The viewer can observe:
4. The viewer can observe:
5. The viewer can observe:

---

## `<shot-id>` — `<shot title>`

### Identity and purpose

- Record time:
- Locked word range:
- Exact VO:
- Shot role:
- Purpose:
- Mode:
- Production lanes:
- Shot grammar:
- Style-frame reference:

### Picture/audio contract

- Mode: `narrated_observation | narrated_dramatization | sync_dialogue | presenter_address | natural_sound_observation | silent_graphic`
- Language carrier: `narrator | scene_participant | presenter | natural_sound | none`
- Visible speech: `prohibited | illustrative_only | required | incidental_source_only | source_synced | not_applicable`
- Coverage grammar: `observational_action | motivated_interaction | dialogue_exchange | direct_address | natural_sound_action | graphic_progression`
- Face function: `none | task_focus | caused_reaction | dramatic_performance | dialogue_exchange | sync_delivery | source_delivery | presenter_delivery | environmental_presence`
- Concrete physical action:
- What the picture carries that the audio does not:
- New information revealed by this angle:
- Mute test — would the viewer expect a missing line? `yes/no`
- Mute-test reason:

For `narrated_observation`, the narrator carries language and the image carries action, evidence, pressure, relationship, or consequence. Visible speech, reciprocal conversational eyelines, question-and-answer reverse shots, and facial coverage that implies an unheard line are prohibited. A close view of a face is valid only for task focus or a reaction visibly caused inside the shot.

`source_delivery` belongs only to `natural_sound_observation`. It requires synchronized source speech and a mute-test acknowledgement that the line will be missing on mute. Without `source_delivery`, natural-sound footage must not imply a structurally missing line and the mute result remains `no`. `sync_delivery` belongs only to `sync_dialogue`. Neither is an escape hatch for narrator-led footage.

### Editorial intent

- Techniques selected:
- Why this shot / attention owner:
- Entry trigger:
- Exit trigger:
- Hold intent (or why no protected hold is needed):
- Simpler alternative considered:
- Scene-specific review question:
- For narrated dramatization — illustrative representation, narration-carried essential meaning, disclosure plan, and actual-audio review check:

Do not impose a fixed number of setups or cuts. In narrated dramatization, reciprocal eyelines and
an attempted answer may be the scene's action; mute viewing is diagnostic, not a universal veto.
The actual narration must supply essential meaning. No extra character dialogue or invented sync.

### Direction facts

- What stays still:
- Master/setup role: `master | setup | standalone`
- Declared master shot ID or asset-ticket ID listed on this setup, required for `setup` and otherwise `null`:
- Master/setup relationship:
- Action line:
- Camera side:
- Subject screen direction:
- Initial image:
- Final image:

| Continuity anchor ID | Kind | Exact property or state that persists |
|---|---|---|
| `<id>` | `world_object | asset_ticket | shot_layer | identity | wardrobe | prop | lighting | spatial` | `<description>` |

### Audience attention

- Primary subject:
- Focal point:
- Eye starts:
- Eye path:
- Primary action:
- Consequence:
- Final read:
- Maximum simultaneous meaningful actions:

### Action phases

| Phase | Time | VO cue | Visible state | Action | Purpose |
|---|---:|---|---|---|---|
| Establish | `<range>` | `<cue>` | `<state>` | `<action or hold>` | `<why>` |
| Anticipate | `<range>` | `<cue>` | `<state>` | `<action or hold>` | `<why>` |
| Act | `<range>` | `<cue>` | `<state>` | `<action>` | `<why>` |
| Consequence | `<range>` | `<cue>` | `<state>` | `<action>` | `<why>` |
| Settle | `<range>` | `<cue>` | `<state>` | `<settle>` | `<why>` |
| Hold | `<range>` | `<cue>` | `<resolved state>` | `still` | `<reading need>` |
| Handoff | `<range>` | `<cue>` | `<exit state>` | `<cut or transition>` | `<next responsibility>` |

### Static shot board

#### Entry frame

- Background:
- Midground:
- Foreground:
- Primary hierarchy:
- Exact text:
- Evidence:
- Placeholder assets:
- Incoming continuity anchor:

#### Key action frame

- Background:
- Midground:
- Foreground:
- Primary hierarchy:
- Exact text:
- Evidence:
- Placeholder assets:

#### Consequence frame

- Background:
- Midground:
- Foreground:
- Changed state:
- Final read:

#### Exit frame

- Preserved objects:
- Position / scale / depth:
- Movement vector:
- State:
- Evidence pin:
- Outgoing continuity anchor:
- Next shot requirement:

### Camera

- Framing:
- Start view:
- End view:
- Target:
- Movement:
- Purpose:
- Screen direction:
- Lens / camera height:
- Focus / parallax:
- Static alternative:

### Composition and layers

| Layer ID | Source / ref | Role | Start state | End state | Geometry / anchor | Depth | Visibility |
|---|---|---|---|---|---|---:|---|
| `<id>` | `<source>` | `<role>` | `<state>` | `<state>` | `<bounds>` | `<z>` | `<range>` |

### Typography

| Text ID | Exact text | Role | Lines | Alignment | Emphasis | Cue | Read hold |
|---|---|---|---:|---|---|---|---:|
| `<id>` | `<text>` | `<role>` | `<n>` | `<alignment>` | `<substring/treatment>` | `<word/time>` | `<seconds>` |

### Motion

| Motion ID | Cue | Target | Verb | Property change | Duration | Settle | Purpose |
|---|---|---|---|---|---:|---|---|
| `<id>` | `<word/time>` | `<layer>` | `<verb>` | `<from/to>` | `<seconds>` | `<state>` | `<why>` |

### Transition

- Type:
- Duration:
- Outgoing anchor:
- Incoming anchor:
- Preserved property or object:
- Outgoing vector / speed:
- Incoming vector / speed:
- Audio bridge:
- Relationship explained:

### Assets and evidence

- Asset tickets:
- Selected assets:
- Source ranges:
- Handles:
- Crop and focal:
- Placeholder behavior:
- Evidence source / locator:
- Highlight:
- Extract:
- Attach:
- Parameter change:
- Pinned context:
- Reconstruction / synthetic label:

### Sound

- Narration present: `yes/no`
- Dialogue: `none | sync_scripted | sync_source | presenter`
- Music:
- Ambience: `none | source | designed_post | temporary_reference`
- SFX:
- Accent:
- Silence:
- Transition bridge:

### Complexity budget

- Meaningful objects:
- Simultaneous actions:
- Visible labels:
- New concepts:
- Evidence density:
- Caption collision risk:

### Shot review checks

- [ ] Primary subject is immediately identifiable.
- [ ] Action occurs after orientation.
- [ ] Consequence is visible before the next shot.
- [ ] Motion follows exact cues and settles.
- [ ] Text is exact, necessary, legible, and held.
- [ ] Continuity matches incoming and outgoing shots.
- [ ] Direction facts name what stays still, bind every setup to a declared master shot or listed asset ticket, preserve screen direction and continuity anchors, and define exact initial and final images.
- [ ] Evidence or assets satisfy their semantic role.
- [ ] Picture and audio follow the declared mode; the actual track supplies essential meaning without unavailable words.
- [ ] The mode-specific mute diagnostic and actual-audio review are recorded honestly; a planned check is not a playback verdict.
- [ ] Any face close-up serves the selected mode: task focus, caused reaction, motivated dramatic turn, or exact synchronized delivery.
- [ ] The master/setup reference, screen direction, continuity anchors, still elements, initial image, and final image are explicit and agree with adjacent shots.
- [ ] No decorative motion or transition has been added.
