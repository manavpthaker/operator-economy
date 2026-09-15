# R24: subtle articulation proposal

Checked 2026-09-10 UTC. Prepared locally only; no upload, generation, approval, preview edit, or canonical change.

Recommend one **B-only React-1 lips comparison** against R22, using the original performance that produced R22 B and the unchanged original audio. This is a bounded articulation experiment, not a promised improvement. It does not satisfy a separate request for more facial emotion. Broader face rewriting would reopen the expression risk the owner rejected in R23.

## Supported control and limit

| Mode | Intended edit scope | Fit here |
|---|---|---|
| `lips` | Lip sync with minimal facial change | Narrowest supported trial |
| `face` | Lip sync and facial expression, without head movement rewriting | Broader than this proposal |
| `head` | Also rewrites head movement | Outside scope |

Fal requires one emotion enum: happy, sad, angry, disgusted, surprised, or neutral. Its endpoint exposes no freeform acting prompt. Specify `lips`, `neutral`, `cut_off`, and temperature `0.5`; otherwise the defaults include face editing and bounce duration handling. Temperature controls expressiveness, but no documented calibration maps a setting to “slightly clearer.” Keeping its default avoids inventing that relationship. Both inputs must be at most 15 seconds. [Fal schema](https://fal.ai/models/fal-ai/sync-lipsync/react-1/api), checked 2026-09-10.

Sync's direct API permits omitting the emotion prompt; Fal's required field differs. The mode descriptions specify intended regions, not pixel-identical preservation. A new result still needs full-motion comparison for mouth quality, likeness, expression, and body/head continuity. This single-speaker input fits the model's documented constraint; speaker selection and occlusion detection are unavailable. [Sync React documentation](https://sync.so/docs/models/react), checked 2026-09-10.

## Verified lineage and prepared inputs

All three assigned R22 hashes match. R15 `provider/INPUTS.json` and `prepare-inputs.mjs` bind original B to raw404 frames **[83,289)**. The recorded R15 Sync 3 B submission used this original B and pickup audio. R22 B's encoded video stream is identical to the resulting R15 picture stream: SHA-256 `ab03e9de03d35cd498f34db05afe20d2effa7f4bddb3b1ab4a0e6fa0335c83ae`.

- Proposed video: `inputs/performance-b-original.mp4`, copied byte for byte from R15 `provider/inputs/performance-b.mp4`; SHA-256 `dae03d667c44b7faf29d3d8b13317a3939ef6997885b05c0efb5dbc66eb58cf4`.
- Proposed audio: `inputs/pickup-b-original.wav`, copied byte for byte from R15 `provider/inputs/pickup-b.wav`; SHA-256 `e37976fde23e50265e7e6dde1a034d873d8b39f87d89f074d4da19ae7ac49072`.
- Comparison control: `inputs/r22-post-title-b.mp4`, copied byte for byte from accepted R22 B; SHA-256 `6bebb793f25e39b4c5577559f7e25b91a39270f904755bc6872586579935147a`.

Both pictures contain **206 frames at 24 fps, 1920×1080, first PTS zero, 8.583333 seconds**. Pickup audio contains 412,000 mono 16-bit samples at 48 kHz and is exactly equal to R22 extended-narration samples **[3,164,000,3,576,000)**. No audio sample, frame, duration, or encode was changed while preparing this packet. Media files are ignored by the existing local Git exclusions.

This establishes the same underlying performance and timing, not body-pixel equality between the unsynchronized original and R22's Sync 3 output. Using the original avoids processing already generated lips again. Preserve the original soundtrack and root's latest accepted closeup edit if a candidate is eventually selected. “One number” occupies B local **5.023333–5.693333 seconds**; natural phoneme articulation and retained subtlety there are review criteria, not supported timed API instructions.

Bounded searches including ignored JSON/Markdown/scripts in the EP007 review and controlled-source experiment found old React proposals only, with no local React result or receipt to reuse. This is a repository-evidence finding, not an account-history search.

## Exact proposed authority and acceptance

Published Fal pricing is **$10/minute**: `8.583333 / 60 × $10 = $1.430556`. Propose **one submission, $2 estimated ceiling, zero retries**. Billing rounding and account charges were not independently audited. [Fal price](https://fal.ai/models/fal-ai/sync-lipsync/react-1), checked 2026-09-10.

`PROPOSED-REQUEST.json` is nonexecuting and unapproved. All earlier grants are consumed. A new authorization must cover the pinned original video/audio upload and this one named submission. Stop on changed inputs or price exceeding the estimate ceiling, unexpected duration, rejection, failure, uncertain submission, or completion; do not switch modes, regenerate voice, or repair with another call.

Review the whole result at normal speed against R22 with the original soundtrack. Require full sentence coverage, no timing drift, no exaggerated expression, and no degraded likeness or visible motion discontinuity. Metadata or waveform equality alone cannot approve lip sync. If articulation is no better, keep R22 and reject the candidate; this proposal authorizes no fallback.

Latest owner steering moves the closeup to just after “and.” Root owns that independent local edit at review 67.583333. This paid proposal remains deferred and unapproved while that simpler change is shown; no approval question or generation is part of this work order.
