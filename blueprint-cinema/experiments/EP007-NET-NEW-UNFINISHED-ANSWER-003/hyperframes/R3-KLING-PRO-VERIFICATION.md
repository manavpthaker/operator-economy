# R3 Kling Pro comparison verification — r3-route-c02

Status: **technically valid; preferred of the two tested takes for paper continuity; rejected against the current R3 timing/action contract; preserved unmounted.**

Reviewer: primary agent, media integrity and shot-contract review. Review date: 2026-09-06 EDT. No owner select or production approval is recorded.

## Request and provenance

- User authority: "Let's try another model", followed by "continue"; one comparison request.
- Provider / endpoint: `fal.ai / fal-ai/kling-video/v3/pro/image-to-video`.
- Request ID: `01a079bf-683a-75c2-a73b-5959ee7e18f0`.
- Submitted: `2026-09-07T02:43:02.428Z`; completed/downloaded: `2026-09-07T02:46:09.845Z`.
- Model version: UNKNOWN; no version was exposed.
- Actual parameters: duration `"8"`; audio false; shot type customize; CFG `0.5`; one positive prompt; start and end images; negative prompt.
- Seed, resolution, FPS, hard camera lock, and aspect-ratio fields were not sent because this endpoint does not expose them. Local response metadata `resolution: provider-default` is descriptive, not a provider parameter.
- Current Fal list price: `$0.112/s × 8 = $0.896`, within the agent-selected `$0.90` cap. The response did not return an account-debit receipt. Sources: [model and pricing](https://fal.ai/models/fal-ai/kling-video/v3/pro/image-to-video), [API schema](https://fal.ai/models/fal-ai/kling-video/v3/pro/image-to-video/api), and its linked OpenAPI schema.
- Submitted packet: `R3-KLING-PRO-PROMPT.md`; pre-review SHA-256 `6f038477f8207adc854257d7fe7b5ff938187b1551d8bc56c0b0b73ad0c628ab`.
- Positive prompt: 1,583 characters; SHA-256 `d953c4d3b1ee60e48d5856fbe99c111340d969712b060df4cf772f42161eeedd`.
- Effective negative prompt: 1,046 characters; SHA-256 `6d5b2a4302095ad5ea9cee91d08d92e507e20783c704644953757bfb8627bf88`.
- Generator: unchanged `../../EP007-BL-CALLBACK-ARC-001/hyperframes/scripts/generate-fal-film.mjs`; SHA-256 `6f72d94757c95ea87e5b6b1de4609db8ee41bc4552bd11e7d4a93be69252b43e`.
- Direction SHA-256 `4100737d6210577ed25838b49265b693d90433055edbfecc046037c17939650c`; storyboard SHA-256 `36a0beee3d6e7db7b04e22455df1b2837d5c1bff1aa1b90c00a06e50a768b03e`.
- Start `public/media/r3-route-start.png`; SHA-256 `5e13a9a45965a39d260dc7a25bd7d713c671619fa76dc5e8b384b6419bc639a7`.
- End `public/media/r3-route-end.png`; SHA-256 `6becc345680fa00281e56aedb56528aa04bf5fd958fe44cc93994154a8db1ac4`.
- Untouched source `renders/candidates/r3-route.kling-pro.full-generated.mp4`; SHA-256 `f9023d50357b645e016d1cc54825ccd60091dff6557065a4849d7496e4631f76`.
- Response `renders/candidates/r3-route.kling-pro.full-generated.mp4.response.json`; SHA-256 `23730c1b2f33f213d060b629ba37e6375e70edd5b0a340cc2ffd89490115652a`.

## Comparison design and limits

The image bytes, positive prompt, effective negative prompt, and requested eight-second silent duration exactly match the Veo trial. Kling uses its native default CFG 0.5 and has no exposed seed. This is a controlled comparison of these two outputs under the same image/prompt constraints, not a statistical model ranking. The endpoint images contain differences outside the moving ticket and anatomy, including page geometry. Those are a known shared input risk.

The earlier statement that the Veo failure proved the pair unsuitable was too strong. Kling's cleaner paper behavior demonstrates that the conspicuous ragged-edge failure was not inevitable under the same inputs. It does not prove the pair is production-ready or identify the internal cause of either model's motion.

## Technical verification

- Container: MP4 / ISO BMFF.
- Video: H.264 Constrained Baseline, progressive 8-bit yuv420p.
- Dimensions: **1916×1080**, not 1920×1080.
- Cadence: 24 fps CFR; 193 frames; timestamp steps 0.041666–0.041667 seconds.
- Duration: **8.041667 seconds**; one extra frame relative to an exact eight-second 24 fps source.
- Audio: absent.
- Size: 24,632,661 bytes.
- Strict decode: PASS.
- Black detection: no interval reported at d=0.04, pix_th=0.1.
- Freeze detection: no interval of at least 0.5 seconds at -50 dB. This is a pixel-level scan; a valid low-motion handle need not be mathematically frozen.
- Decoded frame identity: 193 frames, 193 unique hashes, zero exact duplicates.
- Delivery compatibility remains unresolved: the experiment's canonical frame is 1920×1080 at 30 fps. No conform, padding, retiming, or integration was performed on the source.

## Visual findings

| Requirement | Result and evidence |
| --- | --- |
| Opening handle | PASS for approximately one second; the route does not begin immediately. The first 0–60-frame strip shows a broadly held starting pose, with small natural/model motion. |
| Ticket returns to owner | PASS in broad visual meaning; one blank ticket travels from work/right to owner/left. The path first descends toward the near edge, then continues left. |
| Blankness and non-evidence | PASS in reviewed frames; no readable text, route drawing, or factual content is generated. |
| Faces and buyer behavior | PASS in reviewed frames; faces remain cropped and the buyer stays passive. |
| Major prop and camera continuity | Binder, keys, buyer, table, and overall view remain materially stable. |
| Page integrity | Improved over Veo: no comparable ragged/lifted extra edge appears in the reviewed transition. The page geometry still migrates toward the nonidentical end frame; continuous planar tracking is not validated. |
| One coordinated pencil action | FAIL against the requested choreography: the pencil is initially left behind, then sweeps low over the ticket before lifting/repositioning into the endpoint. Frames 128–175 show the added motion. This reads as a corrective beat after the primary route, not one pointer follow and stop. |
| Pencil contact | UNRESOLVED at the lowest pass. It looks writing-like in some frames, but these images do not establish physical contact and no mark appears. Do not report invented writing as a fact. |
| Final 1.5-second settle | FAIL. Frames 152–175 (6.33–7.29s) show conspicuous pencil/ticket repositioning; later frames retain smaller settling motion. Even the more stable last approximately 0.7 seconds is shorter than the required handle. |
| Full ticket select | FAIL on choreography and final hold. Technical improvement does not waive those requirements. |

Severity: **major** for action/timing. The scene's meaning is recoverable, but the current shot requirements are unmet. No production select was made.

## Review evidence

All sheets read left-to-right, top-to-bottom:

- `snapshots/r3-kling-pro-c02/contact-sheet-24f.png`: whole clip sampled at 3 frames/second, 6×4.
- `snapshots/r3-kling-pro-c02/contact-sheet-f000-060.png`: frames 0–60 every 4, 4×4.
- `snapshots/r3-kling-pro-c02/contact-sheet-f064-124.png`: frames 64–124 every 4, 4×4.
- `snapshots/r3-kling-pro-c02/contact-sheet-f128-188.png`: frames 128–188 every 4, 4×4.
- `snapshots/r3-kling-pro-c02/late-every-frame-f152-175.png`: every frame from 152 to 175; crop x=280, y=50, width=1150, height=700; scaled to 575×350 per cell, 6×4.
- `snapshots/r3-kling-pro-c02/final-every-frame-f176-192.png`: same crop and scale, every frame 176–192, 6×3; last cell is unused white padding, not source video.
- `snapshots/r3-kling-pro-c02/frame-136.png` and `frame-192.png`: untouched full-resolution source-frame extractions.

The review decoded the full source and inspected its phases, four-frame strips, and every late-transition frame. This supports the stated shot-contract rejection; it is not owner approval or a claim that full-speed playback with the narration has passed.

## Side-by-side review derivative

- File: `renders/candidates/r3-model-comparison.veo-left-kling-right.review.mp4`.
- Left: Veo `r3-route-c01`, parent SHA-256 `a8525034600f2837f0e01476f6dc82726a9e2789e15c9cbd10abdab0085c6b5e`.
- Right: Kling `r3-route-c02`, parent SHA-256 `f9023d50357b645e016d1cc54825ccd60091dff6557065a4849d7496e4631f76`.
- Operation: start-aligned, same-time hstack; each source fitted/padded to 960×540 preserving aspect; no time warp; stop at shortest input.
- Encoding: 1920×540, 24 fps, 192 frames, 8.000 seconds, H.264, silent; strict decode PASS.
- Size: 4,082,853 bytes; SHA-256 `bac7ab41ccff56e256c42974653a9085da9f5f03de20f029e8bc8295a28a2cbd`.
- The last extra Kling frame is omitted only in this review derivative. The full 193-frame source is preserved.
- Codex returned `queued` when asked to open the comparison; visible playback was not independently confirmed.

## Disposition and next decision

- Attempt count under this request: one; completed.
- Comparative judgment: Kling is the more promising of these two takes for the next R3 iteration because the paper remains cleaner and the opening handle is present.
- Candidate status: rejected against the current ticket; preserve unmounted.
- Approved source range: none. Planar track / hand occlusion: not started.
- Suggested next iteration: retain Kling, explicitly time the one ticket movement and pencil follow earlier, and leave the last 1.5 seconds still. A corrected endpoint pair with a fixed page plane would remove a shared input inconsistency.
- No further paid call, integration, Step 3 advancement, commit, push, or publication was performed.

