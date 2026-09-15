# EP007 R8 generation preflight — 2026-09-08

Read-only tooling QA for the isolated 17-second test. All three work-order input hashes match. No request, upload, credential access, installation, media selection, or canonical state change occurred in this review. This report is not a performance verdict or production-gate approval.

## Result

The retained `fal-ai/kling-video/v3/pro/image-to-video` route is listed on the current official pages. Silent public list pricing is **$0.112 per generated second**: buyer B, 8 seconds = $0.896; owner C, 9 seconds = $1.008; **two-request total $1.904, approximately $1.90 video-only**. Start-image generation, taxes, discounts, account credits, retries, and actual invoice reconciliation are excluded. The page describes aspect ratio as determined by the start image and default concurrency as one. [Fal model and pricing](https://fal.ai/models/fal-ai/kling-video/v3/pro/image-to-video).

API support is explicit: duration is a string enum including `"8"` and `"9"`; `start_image_url` is required; end image is optional; `generate_audio` defaults to true, so false must be explicit; CFG defaults to 0.5. Use one prompt, not multi-prompt, for each fixed-camera plate. Base64 data-URI image input is documented. Public documentation establishes capability, not current account balance, entitlement, queue capacity, or a successful paid request. [Fal API documentation](https://fal.ai/models/fal-ai/kling-video/v3/pro/image-to-video/api).

The exact endpoint schema additionally limits positive and negative prompts to 2,500 characters each; start image maximum is 10,485,760 bytes, minimum 300 pixels per dimension, aspect ratio 0.4–2.5. CFG range is 0–1. [Exact endpoint OpenAPI schema](https://fal.ai/api/openapi/queue/openapi.json?endpoint_id=fal-ai/kling-video/v3/pro/image-to-video).

## Existing helper and invocation

Helper, Blueprint Cinema-relative:

`experiments/EP007-BL-CALLBACK-ARC-001/hyperframes/scripts/generate-fal-film.mjs`

Current SHA-256: `6f72d94757c95ea87e5b6b1de4609db8ee41bc4552bd11e7d4a93be69252b43e`. This matches the earlier R7 preflight pin. Actual R7 candidate provenance confirms the same Kling route, silent settings, CFG 0.5, and 11/8-second requests.

Run from `experiments/EP007-NET-NEW-UNFINISHED-ANSWER-003/hyperframes/`, not its nested review directory: the helper resolves repository root from cwd `../../../..` and reads the repository `.env`. It prefers an existing process `FAL_KEY`, otherwise parses that key from the file, but it reads the file unconditionally before choosing. No key value was read or printed for this review.

Invocation shape only; placeholders below are not submitted commands:

```sh
node ../../EP007-BL-CALLBACK-ARC-001/hyperframes/scripts/generate-fal-film.mjs \
  --model fal-ai/kling-video/v3/pro/image-to-video \
  --reference <reviewed-start-frame.png> \
  --prompt-record <shot-record.md> \
  --output <new-ignored-candidate.mp4> \
  --response <new-ignored-candidate.response.json> \
  --duration <8-or-9> \
  --cfg-scale 0.5
```

The prompt record must contain an exact `## Prompt` heading. The helper uses only that section as the positive prompt. It forces `generate_audio: false` and `shot_type: "customize"` in the Kling branch. Its own CFG default is 0.7, so pass 0.5. Its `--resolution` value is only provenance/log metadata in the Kling branch, not a sent request control. No seed or FPS control is sent by this branch.

**Do not reuse R7's negative append.** Actual R7 provenance prohibits speaking/talking/word-shaped mouth movements. Those restrictions conflict with R8's explicit illustrative conversation. The helper's base negative string does not prohibit ordinary speaking; its restriction on dramatic reactions remains compatible with the restrained performance. Build R8-specific negatives without trying to force exact lip-sync or audible dialogue.

## Persistence and recovery

Before each invocation, ensure the exact output and response targets are absent. The helper has no overwrite or idempotency guard. It sends one POST, verifies the queue response has request ID/status URL/result URL, then writes a checkpoint at the requested response path. It polls status with GET every five seconds, for up to twenty minutes. On completion it retrieves the result, downloads the returned video, and replaces the checkpoint with final provenance containing request ID, references and hashes, returned response, output hash, and byte count.

A rerun submits another paid job. A timeout, interrupted process, failed poll, or uncertain response is **not** permission to rerun. Recover the existing `requestId`, `statusUrl`, and `resultUrl` from the checkpoint and use read-only status/result retrieval. There is no implemented `--resume` mode despite the timeout message saying “resume from.” If failure occurred after POST but before checkpoint persistence, use known queue/account request evidence to resolve the uncertain submission before authorizing another; do not assume nothing was charged.

Previous R7 persistence locations are `hyperframes/reviews/r7-rapport-pause/renders/candidates/shot-a.mp4.response.json` and `shot-b.mp4.response.json`, with corresponding local MP4 files. Preserve those; R8 needs unique candidate paths in its own ignored output folder. Root orchestrator owns the final path choices, invocation, and local selection. Keep requests serial and no automatic retries.

## Acceptance boundaries

- Newly generated start frames and executable prompt records require root's visual/length/hash checks; they were not part of this frozen packet.
- Prompted timestamps are performance targets, not deterministic motion guarantees. B must fit the 6.250-second selected span; C must fit the 6.916667-second span and stop during the narrated break without a premature gaze drop.
- Probe actual duration, frame rate, dimensions and streams after generation. The helper's request and metadata cannot prove delivered duration, silence or performance.
- Review the assembled 17-second cut with the unchanged narration and inspect both seams. This preflight does not authorize a four-second pre-roll, a longer opening, another avatar take, unlimited regeneration, or any canonical gate.

## Checks and limits

Passed: all frozen input hashes; current primary-page capability/rate check; exact raw schema constraints; helper request/persistence behavior; safe field-only R7 provenance inspection; direct work-order and deliverable schema/semantic validation. No provider submission, live billing query, account entitlement check, credential-value inspection, new-start-frame review or generated-motion playback was performed.
