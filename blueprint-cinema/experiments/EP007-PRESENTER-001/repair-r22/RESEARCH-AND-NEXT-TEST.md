# EP007 presenter: methods review and bounded next test

Date: 2026-09-08. Status: research and proposed benchmark, no new generation.

The owner wants small, natural head and hand movement and explicitly requires **only the existing photo and audio**. No new recording, performance-reference video, image edit, wardrobe/set change, or replacement voice is part of the next test.

## Recommendation

Stop the Q stabilization route. Compare OmniHuman 1.5 and Hedra Character 3 using the same existing wide study image, same 5.600-second WAV, and one unchanged restrained direction. Generate two samples per model, then stop for normal-speed owner comparison. This is a small capability test, not evidence that either model is best or a promise that switching will solve the performance.

The owner's [reference repository](https://github.com/harlanhong/awesome-talking-head-generation) is a useful research index. It is not a ranking or a benchmark of understated head and hand motion on this identity, image and audio.

## What our own evidence establishes

- M and Q requests use `type: image`, an image asset and audio asset. Neither request supplies the original avatar training recording or a performance reference. Both already set `expressiveness: low`. The exact requests are `../repair-r14/video-request.json` and `../repair-r18/video-request.json`. These failures do not establish that the user's original recording was bad.
- M is the historically owner-accepted mouth/head reference. Q uses the same motion prompt but a wider, different source image. Q is only a partial improvement, not an accepted final performance. O also changed source posture/composition and prompting, so it did not isolate one cause.
- The current source image shows an open right hand above the desk. That may encourage a gesturing performance; this is a hypothesis, not an isolated finding. Keep the image fixed for the model comparison instead of silently adding another variable.
- S reduced tracked head movement but introduced a scale pulse. The owner's rejection overrides its numeric review. T removed added scale/rotation but retained the source nod and forward movement; it did not become a micro-expression-only performance. See `../repair-r21/prior-s-zoom-diagnosis.json` and `../repair-r21/status.json`.
- Audio equality and landmark measurements establish particular technical facts. Neither proves that the mouth looks synchronized, gestures feel natural, or a moving face is acceptable at normal speed. Still-frame checks were insufficient for S's temporal defect.

## Model fit, based on current primary sources

| Candidate | Relevant documented capability | Important limit for EP007 | Decision |
| --- | --- | --- | --- |
| OmniHuman 1.5 | Image + audio + optional text guidance for behavior. | Its research emphasizes expressive audio-correlated performance; no documented independent head/hand amplitude slider in the inspected fal endpoint. Hosted limits differ from research demos. | First comparator. |
| Hedra Character 3 | Image + audio + text; official guidance addresses restraining gestures. | Hedra explicitly documents exaggerated hand movement as a possible problem. Its reputation is not a guarantee on this shot. | Second comparator with explicit model identity. |
| InfiniteTalk | Image-to-video and a distinct video-to-video route; upstream long-video generation. | Long duration is not a control for subtle gestures. Video conditioning is outside the owner's current input constraint. Hosted input controls and duration must be checked independently of upstream claims. | Reserve, not an additional first-round model. |
| HunyuanVideo-Avatar | Audio-driven animation with emotion conditioning and internal head/expression bucket conditioning. | Internal controls are not a documented, calibrated user setting for subtle motion, and no separate hand control was established. Self-hosting adds setup without first establishing a better performance. | Reserve, not first-round setup work. |

Sources: [OmniHuman research](https://omnihuman-lab.github.io/v1_5/), [actual fal OmniHuman input schema](https://fal.ai/models/fal-ai/bytedance/omnihuman/v1.5/api), [Hedra Character 3](https://www.hedra.com/models/video/hedra/character-3), [InfiniteTalk repository](https://github.com/MeiGen-AI/InfiniteTalk), [HunyuanVideo-Avatar repository](https://github.com/Tencent-Hunyuan/HunyuanVideo-Avatar). These document capabilities and limitations; they are not an independent comparison establishing which is best for restrained delivery.

## Best practices applied to this shot

1. **Direct visible behavior concretely.** Use supported forearms, hands close to the tabletop, small finger movement, and tiny head adjustments. Avoid adding nod/lean/gesture sequences or dramatic emotion. Do not direct microscopic mouth opening; let the exact audio drive articulation, then judge it.
2. **Keep the direction short and specific to the model.** HeyGen recommends one gesture and short clauses; its custom-motion workflow has different behavior from OmniHuman. Do not copy engine-specific advice indiscriminately. We will use one common visual intention for the initial two-model comparison. [HeyGen motion guidance](https://help.heygen.com/en/articles/12805098-fine-tune-avatar-gestures-and-movements-with-custom-motion-prompts-avatar-iv-v), [fal OmniHuman prompting guide](https://fal.ai/learn/devs/omnihuman-1-5-prompt-guide).
3. **Preserve the audio input.** The user identified visual emphasis, not the voice, as the problem. Keep the supplied clean narration, pauses and timing. Do not flatten, slow, re-synthesize or replace it to influence a model. Changing models will regenerate mouth motion, so M's accepted mouth performance must be rechecked rather than assumed to transfer.
4. **Evaluate the complete clip at 1x with sound.** Include the quiet interval, “straight,” “never,” final word and hand return. Follow with muted playback for distracting movement and selective frame checks for deformation. Do not use a still montage or reduced motion statistic as the acceptance decision.
5. **Limit sampling before changing strategy.** Two samples per model expose obvious variability but cannot establish a success rate. If the four clips yield no acceptable result, stop; do not continue synonymous prompts or repair the head with scaling/warping. Reassess the input constraint and supported control method with the owner.

Photo quality, pose and framing matter, but this test must preserve the current photo. HeyGen itself distinguishes generated photo movement from motion learned through a video avatar; that explains why the original recording is not the relevant input for M/Q. [HeyGen photo-avatar guidance](https://help.heygen.com/en/articles/10034438-how-to-get-started-with-photo-avatars).

## Exact initial direction

> Locked-off, eye-level medium shot. He speaks matter-of-factly with natural blinks and tiny head adjustments; his forearms stay supported on the desk while his fingers make small, relaxed movements close to the tabletop.

This is a proposed visual direction, not a guaranteed control. It requests some natural movement without demanding rigid stillness or adding word-specific accents. Use the identical direction in both models for the first round. Only adapt request syntax to the documented endpoint; record any mandatory prompt transformation.

## Fixed-input benchmark

- Image: `../media/repair-r16/study-visible-hands-source.png`; SHA256 `2abb05079084198c21a33802e6e0aa6373027a65f2163ea5a9114f77c1c4da24`.
- Audio: `../media/repair-r2/scope-two-sentences.wav`; SHA256 `c565f1dfe8c218f156e9d0b76d0515a264be26cc1d0cea7d1ea8977a3c565566`; 48kHz mono, 5.600 seconds.
- Q is the existing comparison using the same image. M is a differently framed reference for the owner's accepted mouth/head quality, not a matched experimental control.
- Four new clips maximum: two OmniHuman 1.5 and two Hedra Character 3. Keep 16:9, use a common supported native resolution (proposed 720p), exact audio and unchanged prompt; avoid speed-optimized modes for the quality test. Use different recorded seeds if supported; otherwise independent jobs and their request IDs. Do not invent a seed field in an endpoint that lacks one.
- Show actual unmodified provider results in one clearly labeled comparison, with model, sample, duration and exact result identity. Verify that the displayed result is current before describing it; earlier R10/T preview confusion is not acceptable delivery verification.
- Fail a sample on conspicuous head dips/forward thrust, repeated or sweeping hand accents, head-size pulses, face/glasses/finger deformation, frozen expression, obvious lip mismatch, or drift after the pause. Judge against the owner's reference style rather than invented numerical thresholds.
- If at least one sample is acceptable, validate the preferred route on a longer continuous section of the existing narration before episode use. A short winning sample alone does not establish production readiness. If outputs are inconsistent, record that rather than selecting one and claiming reliability.

## Access and execution boundary

This review made no uploads, purchases, installations or generation calls. The current callable catalog has no fal inference MCP tool. fal's official inference MCP exists, but model access/credentials, live request schema and estimated charges must be verified before execution. MCP is the connection mechanism; it does not improve motion quality or guarantee a model's availability in a particular connected service.

The installed Higgsfield catalog returned no OmniHuman match in the read-only query used for this review. That finding is specific to this catalog/query; it does not mean OmniHuman is unavailable through other providers. The official [fal Run MCP](https://fal.ai/docs/documentation/setting-up/mcp) and [Hedra Character 3 API](https://www.hedra.com/docs/api-reference/v3/run-a-model/run-hedra-character-3-hedra-character-3) document execution routes, but those are not currently callable model tools in this session.

OmniHuman 1.5's current fal model page lists $0.16 per generated second, so two 5.6-second clips are about $1.79. Hedra's Character 3 page lists $0.05 per second for 720p, about $0.56 for two clips. Combined arithmetic is about $2.35 before unverified rounding, minimums or other charges. This is a research estimate, not an executed quote, subscription price, approved budget or charge. Confirm the actual request estimate before submission. [Current fal model price](https://fal.ai/models/fal-ai/bytedance/omnihuman/v1.5), [Hedra model price](https://www.hedra.com/models/video/hedra/character-3).

No canonical episode approvals or production/release state changed. M's historical acceptance is retained; T is now owner-requested further refinement because movement remains excessive.

## Supporting review packets

- [Local experiment forensics](../../../episodes/EP007-exit-readiness-prep/agents/deliverables/presenter-methods-review-r22/forensics/report.md): exact M–T provenance, confounds and owner decisions.
- [Open-model source inspection](../../../episodes/EP007-exit-readiness-prep/agents/deliverables/presenter-methods-review-r22/open-models/report.md): InfiniteTalk/Hunyuan code-level control distinctions and implementation constraints.
- [Hosted models and access](../../../episodes/EP007-exit-readiness-prep/agents/deliverables/presenter-methods-review-r22/hosted-integration/report.md): explicit Hedra model identity, fal MCP and endpoint constraints.

`benchmark-plan.json` fixes the proposed inputs, prompt, model identities, sample count and review order. Root verification confirmed the current image/audio/Q hashes, four-sample count, photo/audio-only constraints and zero submitted jobs. The supporting packets are research evidence; none establishes a generated-model quality winner.
