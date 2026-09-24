# Public execution-readiness check

Checked 2026-09-08. Public documents only. This worker did not inspect credentials, upload inputs, submit jobs, or authorize a substitute.

**Hedra Character 3 on fal is not verified.** Targeted official-domain searches returned no fal model page for Hedra or Character 3. The previously verified `hedra-character-3` endpoint belongs to `api.hedra.com`; it is not a fal endpoint. A fal key is not a Hedra API credential. Root should use its authorized fal catalog search for a definitive current catalog result rather than infer availability from public search absence. [Hedra API](https://www.hedra.com/docs/api-reference/v3/run-a-model/run-hedra-character-3-hedra-character-3), [fal model discovery through Run MCP](https://fal.ai/docs/documentation/setting-up/mcp).

## InfiniteTalk photo contingency only

Endpoint: `fal-ai/infinitalk`. Do not use `/single-text` (it generates speech) or `/video-to-video` (requires video). The root image endpoint's title misleadingly says Video to Video, but the schema explicitly requires `image_url`, `audio_url`, and `prompt`. [Official API](https://fal.ai/models/fal-ai/infinitalk/api).

Live linked OpenAPI confirms:

- `image_url`: required. The documentation warns about resize/center-crop if the source does not match the selected ratio, although this schema exposes no aspect-ratio field.
- `audio_url`: required. Reuse the exact existing audio.
- `prompt`: required, **no schema default**. The playground's colorful-haired-podcaster sentence is only an example; replace it with the root's fixed restrained-performance prompt.
- `num_frames`: 41–721, default 145.
- `resolution`: `480p` default or `720p`.
- `seed`: default 42, unsigned 32-bit range.
- `acceleration`: `regular` default; alternatives `none`, `high`.

No duration, fps, hand-amplitude, head-amplitude, or mouth-only control is exposed. This public hosted schema does not guarantee how a 145-frame request is reconciled with 5.6 seconds of audio. Probe the result rather than assume exact duration. [Live OpenAPI](https://fal.ai/api/openapi/queue/openapi.json?endpoint_id=fal-ai/infinitalk).

Current posted price is $0.20/second at 480p, doubled at 720p. Arithmetic for **5.6 seconds** is **$1.12 at 480p or $2.24 at 720p per output**. These are contingencies, not accepted quotes: duration reconciliation, billing rounding/minimums, and exact preflight estimate remain unverified. [Official pricing on the model page](https://fal.ai/models/fal-ai/infinitalk).

## HTTP integration

Submit JSON directly to `POST https://queue.fal.run/{endpoint_id}`, using `Authorization: Key <FAL_KEY>` and `Content-Type: application/json`. Save the returned `request_id`, `status_url`, and `response_url`; use those returned URLs for authenticated GET status/result rather than reconstructing nested model paths. `COMPLETED` means inspect the result/error, not automatically successful generation. A client timeout does not imply the remote job stopped, so do not blindly resubmit. [Official queue documentation](https://fal.ai/docs/documentation/model-apis/inference/queue).

Current official JS SDK source uses `POST https://rest.fal.ai/storage/upload/initiate?storage_type=fal-cdn-v3`, body containing `file_name` and `content_type`, then `PUT` binary bytes to the returned `upload_url` with the matching content type. Pass the returned `file_url` as model input. The current REST base is `rest.fal.ai`, not the older `rest.alpha.fal.ai` found in third-party snippets. [Official storage source](https://github.com/fal-ai/fal-js/blob/main/libs/client/src/storage.ts), [official REST-base definition](https://github.com/fal-ai/fal-js/blob/main/libs/client/src/config.ts).

The official CDN documentation recommends uploading once and reusing the URL. Use the actual binary image upload rather than a helper that converts it to JPEG if keeping exact input bytes is part of the comparison. [Official CDN documentation](https://fal.ai/docs/documentation/model-apis/fal-cdn).
