# R7 Kling preflight — 2026-09-07

Read-only QA/tooling review. Both work-order input SHA-256 values match current files. This is an isolated look-development preflight, not an asset select, performance verdict, production dispatch approval or gate advancement.

## Result

No blocking tooling conflict found for two serial, start-image-only requests to `fal-ai/kling-video/v3/pro/image-to-video`, using duration strings `"11"` and `"8"`, `generate_audio: false`, `shot_type: "customize"`, and `cfg_scale: 0.5`. The end image is optional. Current public list price is **$0.112 per requested second with audio off**: A $1.232 + B $0.896 = **$2.128, approximately $2.13 video-only**. Reference-image generation, taxes, discounts, account credits and actual invoice reconciliation are outside this estimate. [Fal model and pricing](https://fal.ai/models/fal-ai/kling-video/v3/pro/image-to-video), [API documentation](https://fal.ai/models/fal-ai/kling-video/v3/pro/image-to-video/api).

Current raw schema additionally confirms: prompt and negative prompt each maximum 2,500 characters; start image maximum 10,485,760 bytes, minimum 300px each dimension, aspect ratio 0.4–2.5; CFG range 0–1. Data URIs are documented input support. Do not confuse this endpoint with Turbo or the other model schemas displayed on the same API page. [Exact endpoint OpenAPI schema](https://fal.ai/api/openapi/queue/openapi.json?endpoint_id=fal-ai/kling-video/v3/pro/image-to-video).

## Invocation safeguards

- The helper's 277-character default negative string does not prohibit eye contact, acknowledgment, restrained smiles or a small explanatory gesture. Its prohibitions on dramatic reaction, celebration, handshake and signing do not conflict with this trial. Do not append R6's blanket no-eye-contact/no-smile/no-nod restrictions.
- Explicitly pass `--cfg-scale 0.5`; the helper otherwise defaults to 0.7. `--resolution` is only recorded metadata for the Kling branch, not an actual model control. Aspect derives from the start image. No seed or FPS is sent by this branch.
- Invoke from the experiment's parent `hyperframes` directory so the helper resolves the intended repository credential location. Never print credential contents. Its prompt record must contain a `## Prompt` section.
- Check output and response paths are absent before each submission: the helper has no overwrite or idempotency protection. It sends one POST, writes the request checkpoint, then polls. A rerun creates another paid request. On timeout or uncertain completion, inspect/recover the existing request ID, status URL and result URL; never resubmit automatically.
- Use separate candidate paths, serial requests, no automatic retries. Verify B's new reference visually and by hash before its request. Probe the actual output duration and streams rather than assuming request duration or silence guarantees.

## Direction risk and limits

No serious contradiction found inside the scoped nonverbal-interaction exception. The owner must remain engaged at A's exit and B's start for her confidence break to have visible contrast. This is a performance risk, not a provider guarantee: prompted timestamps may drift, and the key gesture arrest must be tested against the unchanged narration before accepting a select. Technical validity cannot establish rapport.

No media generated or uploaded, paid calls, auth changes, canonical changes, invoice checks, actual prompt-record validation or candidate playback occurred. Canonical episode identity/input-lock files are absent in this workspace; the work order already marks `inputs_locked` unestablished. This report does not repair that state or authorize canonical production.
