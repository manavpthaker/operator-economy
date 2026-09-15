# EP007 R6 Kling v3 Pro preflight

Date: 2026-09-07  
Scope: read-only tooling and current-provider check; no request, upload, auth change, or spend.

## Verdict

The existing generator can make the proposed R6 as **three separate, silent, start-image-only
15-second Kling v3 Pro calls** without modification. Requested source duration would be 45 seconds;
editorial must select/trim 0.5 seconds to reach the 44.5-second cold open. Fal's current silent list
estimate is **$1.68 per call, $5.04 total**. Actual returned duration/cadence/resolution must be
inspected rather than assumed.

This is an experimental-call preflight, not production dispatch or an `inputs_locked` gate pass.

## Frozen inputs

Both assigned inputs match:

| Input | SHA-256 | Result |
|---|---|---|
| `experiments/EP007-BL-CALLBACK-ARC-001/hyperframes/scripts/generate-fal-film.mjs` | `6f72d94757c95ea87e5b6b1de4609db8ee41bc4552bd11e7d4a93be69252b43e` | MATCH |
| `experiments/EP007-NET-NEW-UNFINISHED-ANSWER-003/hyperframes/GENERATION-PROMPTS.md` | `2940abcb63260bc7b1d50c44a6a8a96d64cd700893fde93107c72b3d93ab6001` | MATCH |

`node --check` passes for the generator. A repository `.env` exists, is ignored by Git, and contains
a nonempty `FAL_KEY`; no credential value was printed or changed. The script must run from the target
HyperFrames directory because it resolves the repository `.env` as four parents above `cwd`
(`generate-fal-film.mjs:54-57`).

## Current Fal contract

Primary sources checked 2026-09-07:

- [Fal model and live pricing page](https://fal.ai/models/fal-ai/kling-video/v3/pro/image-to-video)
- [Fal model API reference](https://fal.ai/docs/model-api-reference/video-generation-api/kling-video-v3-pro)
- [Fal-linked live OpenAPI schema](https://fal.ai/api/openapi/queue/openapi.json?endpoint_id=fal-ai%2Fkling-video%2Fv3%2Fpro%2Fimage-to-video)

Current contract for `fal-ai/kling-video/v3/pro/image-to-video`:

- `start_image_url`: required; `end_image_url`: optional. Start-only calls are supported.
- `duration`: string enum `"3"` through `"15"`; 15 seconds is the maximum.
- `generate_audio`: defaults true, so the generator's explicit `false` is necessary.
- silent price: `$0.112` per requested second; 15 seconds = `$1.68`; 45 seconds = `$5.04`.
- `cfg_scale`: `0` to `1`, default `0.5`.
- prompt: maximum 2,500 characters; effective negative prompt: maximum 2,500 characters.
- start/end image: maximum 10 MB, minimum 300×300, aspect ratio 0.4–2.5. Output aspect ratio is
  inferred from the start image; this endpoint exposes no resolution, FPS, aspect-ratio, or seed
  control.
- Fal lists default concurrency as one request per user. Run the three calls serially.

The generator's Kling branch correctly sends `prompt`, base64 start image, string duration,
`generate_audio:false`, `shot_type:"customize"`, the effective negative, and CFG
(`generate-fal-film.mjs:83-96`). `--resolution provider-default` affects only console/provenance
metadata; it is not sent in the Kling body.

## Exact invocation template

Run once for each frozen prompt/reference pair, replacing `01` with `02` and `03`. Do not add
`--end-reference` or `--seed`.

```bash
cd /Users/brownmanbrain/GitHub/operator-economy/blueprint-cinema/experiments/EP007-NET-NEW-UNFINISHED-ANSWER-003/hyperframes
node ../../EP007-BL-CALLBACK-ARC-001/hyperframes/scripts/generate-fal-film.mjs \
  --model fal-ai/kling-video/v3/pro/image-to-video \
  --prompt-record R6-SHOT-01-PROMPT.md \
  --reference public/media/r6-shot-01-start.png \
  --duration 15 \
  --resolution provider-default \
  --cfg-scale 0.5 \
  --negative-append 'lip movement, visible speech, dialogue, conversational gesturing, reciprocal question-answer eyelines, direct-to-camera look, random gaze, unfocused head turns, identity drift, face morphing, age change, wardrobe change, role reversal, side switching, duplicate owner, duplicate inspecting party, additional foreground person, object teleportation, exaggerated expression' \
  --output renders/candidates/r6-shot-01.kling-v3-pro.full-generated.mp4 \
  --response renders/candidates/r6-shot-01.kling-v3-pro.full-generated.mp4.response.json
```

Preconditions for each call:

1. Prompt record has one intended `## Prompt` section and the extracted positive prompt is at most
   2,500 characters.
2. Effective negative is at most 2,500 characters. The generator's prefix is 277 characters, leaving
   2,221 characters for `--negative-append` including its separator.
3. Start image meets Fal's size/dimension/aspect constraints and freezes the intended actor identity,
   wardrobe, geography, light, and screen direction.
4. Output and response paths do not already exist. The three proposed paths above were absent during
   this preflight.
5. The one-call scope and list estimate are recorded before submission. No automatic retry.

## Character and negative-prompt safety

The built-in negative list (`generate-fal-film.mjs:49-52`) does **not** prohibit people or visible
faces. `distorted face` is an anatomy-quality constraint, and `dramatic reaction` is compatible with
the requested restrained task focus/hesitation. Its no-text, no-signing, no-handshake, and
no-celebration terms also protect this narrated pre-sale situation.

Do **not** reuse the R3 hand-only negative extension: it contains `visible face`, which conflicts
with character-first R6. Use shot-specific narrated-observation negatives, including no lip motion,
dialogue, reciprocal answer beat, random gaze, or continuity/identity drift. Preserve any intended
deep-background employee by prohibiting only additional foreground people, not every extra person.

The current generator cannot send Fal's optional `elements` character/object bindings. It is
sufficient when every shot's start image already fixes the same actors. If explicit cross-shot
element binding is required, the unchanged generator is insufficient and would need a separately
reviewed flag/payload change before any call.

## Operational hazards

- `writeFile` overwrites both checkpoint and final output unconditionally
  (`generate-fal-film.mjs:170-180`, `224-252`). Unique paths and an existence check are mandatory.
- The 20-minute timeout message says to resume from the checkpoint, but the script has no resume
  mode (`:184-189`). Never rerun a timed-out command: it would submit a second paid request. Recover
  the recorded `statusUrl`/`resultUrl` separately.
- The script performs no provider-schema, prompt-length, image-size, or duration prevalidation.
- Historical eight-second Kling output returned one extra 24 fps frame. Requested duration is not an
  exact editorial duration guarantee.
- `GENERATION-PROMPTS.md:31-50` already supplies the character/geography/light and narrated-
  observation continuity envelope. Its R3 face-cropped direction at lines 66-70 is not reusable as
  R6 character direction.

## Standing

The work-order JSON schema passes, but Blueprint Cinema semantic validation rejects the order because
its forbidden-path list omits seven exact canonical paths. The canonical EP007 Blueprint Cinema
state still does not establish `inputs_locked`. This preflight therefore remains `partial`: it
establishes a technically valid, costed experimental invocation only. It does not authorize a
provider call, retry, integration, production gate, or publication.
