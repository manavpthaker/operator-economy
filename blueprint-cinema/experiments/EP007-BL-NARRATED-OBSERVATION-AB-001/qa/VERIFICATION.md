# EP007 narration-led picture test

Status: **A, B1, and B2 rendered for internal review. This is not a gate pass, production select, Step 4
authorization, or publication approval.**

## What this tests

Under the exact same narration, does observational coverage make the opening feel like an
operating-system test instead of a conversation whose dialogue is missing?

- **A — silent dialogue staging:** the earlier wide and answer/stop close-up.
- **B1 — narrated-observation diagnostic:** skilled work, a staff dependency, shared inspection,
  a locked process detail, and one closed-mouth recognition beat.
- **B2 — clean narrated observation:** the same first two beats, followed by one purpose-generated
  measurement action that stops while both people remain focused on the work.

Only frames `[0,294)` differ. Frames `[294,910)` retain the same rough Boundary Ledger Working
Model and binder callback. Audio, duration, frame rate, resolution, typography, and color are
controls.

## System lock used by the test

- OE skills lock: `485594a623c58f431992882838097a38b6f129a1e464e863ac3170680f36bbb2`
- Boundary Ledger semantic core 2.0.0:
  `30a316f79bc94e017705de0823a0af5b85747a20938eb0a2723d39a1a298978e`
- Scene-direction contract 1.1.0:
  `bdffaeebef149f9caa0a58d704a4ef22b4e168063f77d29ac29b6c44245f2f3c`

The lock validates six local instruction files and four external reference records. The external
repositories are reference-only: no source code, templates, or prose were copied into OE.
Boundary Ledger remains the semantic authority; its motion and sound bindings remain provisional.

## Review artifacts

### A — control

- Phone review copy: `review/A-silent-dialogue-720p.mp4`
- Film: `../../EP007-BL-CALLBACK-IN-CONTEXT-001/hyperframes/renders/EP007-BL-CALLBACK-IN-CONTEXT-001-r2.mp4`
- SHA-256: `0dc991b4ec87a3cfdfd8f84b6fd2c05b89697aabe893f698a6e83a0e9d7fa74d`

### B1 — narrated-observation diagnostic

- Phone review copy: `review/B-narrated-observation-720p.mp4`
- Film: `../hyperframes/renders/EP007-B-NARRATED-OBSERVATION-001.mp4`
- SHA-256: `aa4cc882a560c9f25985c876160b90869bcf9f00f7f7c35b1ce7504c55677446`
- Size: 37,107,509 bytes
- Picture: H.264 High, 1920×1080, 24 fps, 910 frames, 37.916667 seconds
- Sound: AAC-LC stereo, 48 kHz

### B2 — clean narrated observation

- Phone review copy: `review/B2-purpose-observation-720p.mp4`
- Opening-only sequence: `review/AB2-opening-comparison-720p.mp4` — A first, then a 0.5-second
  oxide separator, then B2.
- Film: `../hyperframes/renders/EP007-B2-NARRATED-OBSERVATION-002.mp4`
- SHA-256: `922f0c764ca2995bf8dbf4e2e6b762063064673b45f8bc45acd01694822936fd`
- Size: 39,817,811 bytes
- Picture: H.264 High, 1920×1080, 24 fps, 910 frames, 37.916667 seconds
- Sound: AAC-LC stereo, 48 kHz
- Changed from B1: frames `[151,294)` only. B2 removes the static process crop and the
  dialogue-shaped recognition close-up.

## B2 verification

- HyperFrames 0.8.30 composition check: 0 lint errors, 0 runtime errors, 0 layout issues,
  0 motion findings, and no contrast failures.
- Strict encoded decode: passed. Frame timing: 910 frames, 0 non-monotonic timestamps, final PTS
  37.875000. Black-frame scan at 0.10 seconds: no interval reported.
- Decoded A and B2 PCM hashes match exactly:
  `bf91e2d6ea0edd9b05c28b01cc4857c1a66edf39d6ac508a00010541de486da7`.
- Controlled tail `[294,910)`: A/B2 SSIM `0.999502`; the difference is encoder noise.
- B2 audio: −16.2 LUFS integrated, −3.7 dBTP, 4.3 LU loudness range.
- Freeze detection reports `[318,588)` / `13.25–24.50` seconds. That is the unchanged rough-model
  control, not the new film plate. The B1-only 2.875-second static process crop is gone.
- The final 12 generated-source frames were inspected: the tool, hands, faces, gaze, and camera
  remain stable through the endpoint. Seam packets around frames 96, 151, and 294 show no blank,
  duplicate, or out-of-order frame.
- The animation map was reviewed. It finds one authored oxide-opacity reveal in the bridge; the two
  collision flags are duplicate assembled registrations of that same selector and time span, not
  two authored motions. `bridge.html` contains one timeline and one tween. B2 adds no post camera
  move or graphic animation.
- The renderer repeats the existing sparse-keyframe warning for the rough-model control source.
  Extraction still reports complete frame coverage and the encoded file passes timing and decode
  checks. Re-encode that source before production rather than treating this test render as delivery.
- The generated recognition repair was rejected before assembly because its gaze crossed the buyer
  and recreated a missing-dialogue expectation. It is recorded in `direction/edit-contract-b2.json`
  and is not used by the composition.
- Both the B2 phone copy and 25-second opening comparison decode cleanly. The comparison contains A
  first and B2 second; the oxide separator is review-only and not part of either film.
- OE's local skill lock checks all 6 locked local files and all 4 source-ledger records with no
  findings. The two OE skills pass package validation. The external reference checkouts were not
  re-downloaded in this run, so this is not a fresh upstream-byte audit.
- Boundary Ledger validation checks 55 paths with 0 errors. Its two existing warnings remain:
  audio-first has no encoded-media specimen, and a flattened illustration does not prove a layered
  motion-ready source.
- Focused scene-direction/schema tests pass 27/27. The complete Blueprint Cinema suite passes
  62/63; the sole failure remains the pre-existing stale EP006 `evidence-operator-history` source
  hash, outside this experiment.

## B1 verification record

- HyperFrames 0.8.29 composition check: 0 lint errors, 0 runtime errors, 0 layout
  issues, and 0 motion findings.
- Five opening snapshots: 0 layout or motion findings.
- Strict encoded decode: passed.
- Both 720p phone review copies decode cleanly, retain 910 frames at 24 fps, and reuse the
  unchanged AAC audio stream.
- Frame timing: 910 frames, 0 non-monotonic timestamps, final PTS 37.875000.
- Black-frame scan at 0.10 seconds: no interval reported.
- Audio control: decoded A and B PCM hashes match exactly:
  `bf91e2d6ea0edd9b05c28b01cc4857c1a66edf39d6ac508a00010541de486da7`.
- B audio: −16.35 LUFS integrated, −3.66 dBTP, 3.90 LU loudness range.
- Controlled tail `[294,910)`: A/B SSIM `0.999502`; the small difference is encode noise.
- OE skill-lock validation: passed locally and against the four pinned upstream commits.
- Both OE skills pass the skill-package validator.
- Boundary Ledger validation: 55 paths checked, 0 errors. Its two existing warnings remain:
  audio-first has no encoded-media specimen, and a flattened illustration does not prove a
  layered motion-ready source.
- Focused Blueprint Cinema contract tests: 27/27 passed.
- Full Blueprint Cinema suite: 62/63 passed. The sole failure is the pre-existing stale EP006
  `evidence-operator-history` source hash; it is unrelated to this contract or render and was not
  changed here.

## B1 deliberate limitation

The process-detail insert at frames `[195,264)` is a static crop of older generated material.
Freeze detection correctly reports that 2.875-second hold; it is not a dropped-frame or seek
failure. One other insert also uses older 1024×576 material. The diagnostic can therefore answer
the coverage question, but it cannot approve final image quality or pacing.

That limitation motivated B2. B1 remains preserved as diagnostic evidence rather than silently
overwritten.

## Human decision

Watch A, then B2, once each at normal speed. Answer only this:

> Does B2 turn the buyer's question into a test of the operation, or does it still make you wait for
> someone to speak?

Do not score the palette, rough illustration, binder ending, typography, or narration performance;
those are controlled or outside this test.

## Boundary

No approval was inferred, no gate changed status, nothing was committed, and V4 was not advanced.
Generated people remain illustrative context, never evidence.
