# HyperFrames build packet: `<shot-id>`

This packet is compiled from approved Blueprint Cinema direction. The builder implements it; the builder does not redesign it.

## Control block

- Episode:
- Sequence ID:
- Shot ID:
- Work-order ID:
- Owned composition path:
- Composition ID:
- Required production state:
- Direction-bible hash:
- Rhythm-map hash:
- Shot-board hash:
- Scene-direction hash:
- Asset-manifest hash:
- Locked VO hash:
- HyperFrames version pin:
- Node version:
- FFmpeg version:
- Canvas:
- Frame rate:
- Shot start / end / duration:
- Required handles:
- Output class: `animatic | opaque_plate | alpha_plate | image_sequence | reference`

## Authority and boundaries

Read and obey, in order:

1. episode input lock and approved engine;
2. approved persistent world and visual plan;
3. approved direction bible and rhythm map;
4. approved style frames and representative motion test;
5. canonical shot board and scene direction for this shot;
6. canonical asset and evidence manifests;
7. Blueprint Cinema toolchain, direction, shot, media, finishing, and review contracts;
8. HyperFrames implementation skills, only where they do not conflict with approved direction.

Owned paths:

- `<path>`

Forbidden paths:

- `<path>`

The builder may not change narration, facts, evidence, shot purpose, text, hierarchy, camera intent, asset selection, transition meaning, sound purpose, neighboring shots, the root timeline, shared state, or approvals.

## Locked narration

- Word range:
- Exact text:
- Pre-roll words:
- Post-roll words:
- Required cue table:

| Word index | Word | Absolute time | Shot-relative time | Directional use |
|---:|---|---:|---:|---|
| `<index>` | `<word>` | `<time>` | `<time>` | `<use>` |

## Shot purpose

- Viewer knows before:
- Viewer must infer after:
- Visual sentence:
- Business state before:
- Operation shown:
- Business state after:
- Primary shot role:
- Production lane:
- Mode:
- Emotional pressure:
- Cognitive-load budget:
- Reason this is a shot rather than a continuation or cutaway:

## Continuity

- Prior shot ID:
- Prior exit frame reference:
- Layers inherited with exact states:
- Screen direction inherited:
- Motion vector inherited:
- Eye position inherited:
- Next shot ID:
- Required exit composition:
- Layers handed forward with exact states:
- Match, cut, bridge, or transformation requirement:

## Static end-state construction

Build this state before animation.

- Primary subject:
- Primary relationship:
- Primary consequence:
- Focal point:
- Eye path:
- Visual hierarchy order:
- Foreground / midground / background logic:
- Negative space purpose:
- Balance and tension:
- Safe-area requirements:
- 50% and phone-size survival requirement:

### Layer table

| Layer ID | Manifest/source ID | Visual role | Start bounds x/y/w/h | End bounds x/y/w/h | Z | Start state | End state | Crop / fit | Opacity | Blend / mask | Required? |
|---|---|---|---|---|---:|---|---|---|---:|---|---|
| `<id>` | `<id>` | `<role>` | `<bounds>` | `<bounds>` | `<z>` | `<state>` | `<state>` | `<rule>` | `<value>` | `<rule>` | `yes/no` |

## Camera

- Camera mode: `locked | human | system | evidence | transition`
- Starting frame:
- Ending frame:
- Motivating event:
- Target or crop wrapper:
- Position / scale / rotation changes:
- Parallax or depth behavior:
- Lens or perspective implication:
- Maximum motion intensity:
- Settle duration:
- Motion-sickness and legibility constraints:

## Typography

| Text ID | Exact visible string | Type role | Font token | Size | Weight | Line limit | Bounds | Alignment | Entry | Emphasis | Exit | Minimum read time |
|---|---|---|---|---:|---:|---:|---|---|---|---|---|---:|
| `<id>` | `<text>` | `<role>` | `<token>` | `<px>` | `<weight>` | `<count>` | `<bounds>` | `<rule>` | `<behavior>` | `<substring/cue/treatment>` | `<behavior>` | `<seconds>` |

No additional copy may be invented. Source labels and reconstruction or synthetic labels are factual overlays, not decoration.

## Action phases

| Phase | Absolute range | Shot-relative range | Cue | Visible action | Audience inference | Primary layer | Required settle |
|---|---|---|---|---|---|---|---|
| Entry | `<range>` | `<range>` | `<cue>` | `<action>` | `<inference>` | `<id>` | `<duration>` |
| Establish | `<range>` | `<range>` | `<cue>` | `<action>` | `<inference>` | `<id>` | `<duration>` |
| Operation | `<range>` | `<range>` | `<cue>` | `<action>` | `<inference>` | `<id>` | `<duration>` |
| Consequence | `<range>` | `<range>` | `<cue>` | `<action>` | `<inference>` | `<id>` | `<duration>` |
| Settle | `<range>` | `<range>` | `<cue>` | `<action>` | `<inference>` | `<id>` | `<duration>` |
| Handoff | `<range>` | `<range>` | `<cue>` | `<action>` | `<inference>` | `<id>` | `<duration>` |

## Motion instructions

| Motion ID | Cue time / word | Duration | Targets | Property from -> to | Easing | Stagger | Path / anchor | Explanatory job | Interrupt / settle rule |
|---|---|---:|---|---|---|---:|---|---|---|
| `<id>` | `<cue>` | `<seconds>` | `<ids>` | `<properties>` | `<ease>` | `<seconds>` | `<rule>` | `<job>` | `<rule>` |

- Allowed motion verbs:
- Maximum simultaneous moving groups:
- Objects that must remain still:
- Objects that must preserve identity:
- Required before state:
- Required after state:
- Forbidden ambient or decorative movement:

## Transition contract

- Incoming transition type:
- Incoming semantic relationship:
- Preserved layers:
- Incoming duration and cue:
- Outgoing transition type:
- Outgoing semantic relationship:
- Exit layers and exact states:
- Outgoing duration and cue:
- Cut remains preferred unless the specified relationship requires otherwise.

## Evidence contract

- Claim ID:
- Evidence ID:
- Exact source frame or locator:
- Source-context frame:
- Highlight target:
- Extracted value or passage:
- Attachment target in the system:
- Parameter or behavior changed:
- Source pinned after extraction:
- Attribution string:
- Reconstruction or synthetic label:
- Minimum legible duration:
- Prohibited crop, restatement, or implication:

## Media contract

| Use ID | Asset ID | Version/hash | Source or select range | Timeline range | Crop/focal rule | Color/alpha | Audio use | Rights/disclosure constraint | Placeholder behavior |
|---|---|---|---|---|---|---|---|---|---|
| `<id>` | `<id>` | `<value>` | `<range>` | `<range>` | `<rule>` | `<rule>` | `<rule>` | `<constraint>` | `<behavior>` |

All media is local and manifest-addressed. Do not fetch, substitute, restyle, or regenerate a selected asset inside this packet.

## Sound intent

- Narration behavior:
- Music state:
- Ambience state:
- SFX cue and operational meaning:
- Silence or breath:
- Transition bridge:
- Tail required for Resolve:
- Prohibited sound clichés:

Scene-local audio is a guide unless the handoff explicitly designates it as a final stem. Resolve and Fairlight own the final mix.

## HyperFrames implementation contract

- Root composition supplies:
- This composition supplies:
- Required shared components:
- Registry search query for each approved move:
- Installed primitive and justification, or recorded search miss:
- Required `data-*` timing and clip attributes:
- Seek-safety constraints:
- Static end-state snapshot path:
- Required first/action/consequence/exit snapshot times:
- Motion sidecar path:
- Variables:
- Local font and media paths:
- Expected alpha behavior:
- Expected output codec/container:
- Render command:

## Acceptance checks

Automated:

- [ ] `npx hyperframes lint` passed after structural work.
- [ ] `npx hyperframes check` passed as the final automated gate.
- [ ] Shot duration and frame coverage match the packet.
- [ ] No render-time network request exists.
- [ ] Every visible asset resolves to the manifest and approved version.
- [ ] Every motion is seek-safe and deterministic.
- [ ] Required snapshots exist.
- [ ] Render probe matches duration, dimensions, frame rate, streams, and alpha expectation.

Visual and editorial:

- [ ] Entry frame matches continuity contract.
- [ ] Primary hierarchy is readable without narration notes.
- [ ] Operation and consequence are visually distinct.
- [ ] Text is exact, legible, and on screen long enough.
- [ ] Motion occurs on the approved cue and performs the approved explanatory job.
- [ ] Evidence choreography preserves context and attribution.
- [ ] Exit frame satisfies the next-shot handoff.
- [ ] Frame survives 50% and phone-size review.
- [ ] No generic template, deck, web-page, HUD, or decorative-motion language has appeared.

## Negative constraints

1. `<constraint>`
2. `<constraint>`
3. `<constraint>`
4. `<constraint>`
5. `<constraint>`

## Deliverable report

- Files created:
- Commands run:
- HyperFrames and dependency versions:
- Snapshot paths:
- Render path and hash:
- Media-probe result:
- Differences from packet:
- Open findings:
- Status: `complete | partial | blocked`

`complete` means the bounded implementation satisfies this packet. It does not approve the shot, sequence, animatic, asset, plate, or production gate.
