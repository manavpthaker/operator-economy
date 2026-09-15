# Step 3 v0.4 film-layer amendment

Status: **proposed; not authority**.

Base: proposed Step 3 v0.3 process manifest
`4f830d71d677efa8915429dfe35628012289c28ac988cb74f77261331519690c`.

This amendment changes only the application seam between locked narration, Boundary Ledger visual
language, and Step 4 direction. All v0.3 conditions remain unless this document explicitly
supersedes them.

## 1. V1 application-authority freeze

In addition to the v0.3 semantic core and motion binding, V1 freezes:

- the Boundary Ledger system manifest;
- the canonical Working Model illustration-language document;
- the locked EP006 visual-language reference manifest and its image hash;
- the runtime-neutral Boundary Ledger scene contract;
- the Boundary Ledger production-skill authority document; and
- `.agents/oe-skills-lock.json`, including its local files and pinned source ledger.

Any drift blocks the candidate until compatibility is reviewed and the full acceptance set is run
again. A lock file that says `locked` but whose declared bytes do not match is not locked.

The illustration freeze carries a **mark-making language**, not EP006's hotel composition or
content. New episode drawings must use short overlapping pencil strokes, broken outlines, open
corners, imperfect parallels, correction marks, uneven proportions, variable pressure, and
selective cross-hatching. Roughness is authored into the marks, never applied as uniform wobble,
paper noise, or a generic blueprint effect.

## 2. Two independent mode axes

The v0.3 V4 `mode` field remains unchanged for compatibility, but is named **visual-world mode** in
prose and templates to remove ambiguity. Its allowed values remain:

`reality`, `system`, `proof`, `outcome`, `identity`.

Every timed unit also selects one `picture_audio_mode` from the OE skill lock:

`narrated_observation`, `sync_dialogue`, `presenter_address`,
`natural_sound_observation`, `silent_graphic`.

These axes answer different questions. A `reality` unit says what visual world is present. A
`narrated_observation` unit says the narrator carries language and the picture must not solicit an
unheard exchange. Neither implies the other.

Each unit records:

- `unit_job`: what the picture contributes that the narration does not;
- `picture_audio_mode`;
- `language_carrier`;
- `visible_speech`;
- `mute_test_missing_line_expected`; and
- one typed semantic event binding.

Allowed picture/audio combinations are:

| Mode | Language carrier | Visible speech | Missing line expected on mute |
|---|---|---|---|
| `narrated_observation` | `narrator` | `prohibited` | `false` |
| `sync_dialogue` | `scene_participant` | `required` | `true` |
| `presenter_address` | `presenter` | `required` | `true` |
| `natural_sound_observation` | `natural_sound` | `prohibited`, `incidental_source_only`, or `source_synced` | `true` only for `source_synced`; otherwise `false` |
| `silent_graphic` | `narrator` or `none` | `not_applicable` | `false` |

For EP007's locked narration, `narrated_observation` is the default moving-image mode and
`silent_graphic` is the normal Working Model mode. Other modes require an explicit source-audio or
presenter reason; they are not variety devices.

## 3. Typed semantic-event binding

V4 no longer requires every unit to carry a `business_operation_id`.

Each unit carries **exactly one** of:

- `business_operation_id: BO-*`, with `world_state_before` and `world_state_after` matching the
  derived engine operation; or
- `establishment_id: EST-*`, with `viewer_state_before` and `viewer_state_after` matching the
  engine establishment row.

Both carry the matching selected `boundary_ledger_operation_id`. An establishment unit reveals an
existing actor or relationship; it does not act on an object or claim that the business changed.

The inert-unit test uses the applicable state domain. A real viewer-state change is not inert. A
unit with neither a state change nor evidence still requires a written justification or must be
merged.

## 4. V5 episode doctrine

The direction bible states which picture/audio modes the episode uses and why. For each used mode it
records what carries language, what the picture carries, the visible-speech boundary, the mute-test
expectation, and the handoff constraint Step 4 must preserve.

For `narrated_observation`, the picture carries observable action, evidence, tension, consequence,
or human stakes. It may not borrow dialogue coverage: no reciprocal question/answer eyelines, no
unheard response beat, no sustained readable speech in a generated plate, and no decorative close-up
that makes the viewer wait for a line.

For `silent_graphic`, the Working Model presents one focal change at a time and preserves the
Boundary Ledger before / operation / after / settle structure. Labels identify components or
parameters; they do not restate narration or add source-claim watermarks with no viewer job.

The rhythm map includes picture/audio mode and language carrier so a long stretch of one audio
relationship cannot hide behind varied visual-world modes.

## 5. V6 and V7

Look development identifies both mode axes for every frame. A still can demonstrate composition,
material, hierarchy, and the absence of a dialogue-shaped setup; it cannot prove performance,
motion, or a mute-test result. Those remain Step 4 tests.

V7 freezes the same application-authority hashes recorded at V1. It verifies that every plan unit
uses an allowed picture/audio combination, every used picture/audio mode has a direction-bible
treatment, and every typed semantic event resolves to the engine.

## 6. What remains Step 4

This amendment does not import the shot schema into Step 3. Step 4 still authors:

- physical action and what stays still;
- face function and performance direction;
- master geography, setup relationship, action line, screen direction, and continuity anchors;
- camera position, framing, lens, and motivated movement;
- initial image, final image, and usable sub-window;
- generator prompt and negative prompt; and
- the shot-level mute-test result.

This is the finish line for Step 3: a V7 package that tells Step 4 what every passage must show,
why it must be seen, and where language lives, while leaving every actual shot genuinely unmade.
