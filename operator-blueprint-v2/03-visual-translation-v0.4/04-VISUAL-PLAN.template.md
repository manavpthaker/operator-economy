# Full-timeline visual plan: [episode]

Gate: **V4 — visual plan approved, per act**

Process version: proposed Step 3 v0.4

Use the v0.3 timing, act-boundary, continuous-coverage, evidence-label, reference-integrity, and
inert-unit rules unchanged.

## Units

One row per timed unit. Repeat per act.

| ID | In word | Out word | Visual-world mode | Unit job | Picture/audio mode | Language carrier | Visible speech | Missing line expected on mute | BO ID or EST ID | BL operation | Carry | Focus | Applicable state before | Applicable state after | Evidence | Narrative state |
|---|---:|---:|---|---|---|---|---|---|---|---|---|---|---|---|---|---|

`visual_world_mode` is one of `reality`, `system`, `proof`, `outcome`, `identity`.

`picture_audio_mode` is one of `narrated_observation`, `sync_dialogue`, `presenter_address`,
`natural_sound_observation`, `silent_graphic`.

Each unit binds exactly one semantic event:

- a `business_operation_id`, in which case the applicable state is world/business state; or
- an `establishment_id`, in which case the applicable state is viewer state.

## Picture/audio audit, per act

- Every unit has a specific picture job not supplied by narration: yes / no
- Every mode/carrier/speech/mute combination is permitted by the OE skill lock: yes / no
- `narrated_observation` units avoid a missing-line expectation: yes / no
- Any non-default mode has an explicit editorial or source-audio reason: yes / no
- Establishment units change viewer knowledge without claiming a business change: yes / no
- Shot-level direction remains unmade: yes / no

## Gate V4 decision, per act

| Act | Transcript timing | Continuous coverage | No inert units | Typed events valid | Picture/audio intent valid | Labels intact | Result |
|---|---|---|---|---|---|---|---|

Named human approval remains required per act.

