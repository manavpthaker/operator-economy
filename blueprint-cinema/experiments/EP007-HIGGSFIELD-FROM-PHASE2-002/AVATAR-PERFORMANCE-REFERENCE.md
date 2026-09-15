# Presenter performance reference

Research checked 2026-09-08. This is an experiment-specific direction note, not a change to canonical production gates or a provider migration.

## Owner feedback and baseline

The owner judged the avatar a good starting point, slightly flat, and preferable to an exaggerated performance. Requested change: subtle expression plus a little head and hand movement.

Retain the Wan 2.7 take as the comparison baseline: Higgsfield job `6faef977-72b1-4633-b7a6-a8e94a3f8870`, `generated/avatar-raw.mp4`, SHA-256 `9b8b91bfe39451bbebfef73efffd9e5ebabe5446f2f47bc695c3d821c7293a2a`. The reviewed assembled MP4 SHA-256 is `3616b7afaad51097fa1e2b3951e6bf093923fe5047df05c1e54fbffa9706d96c`.

The existing prompt explicitly requested a still torso, subtle head movement only, no emphatic nodding and no added hand gestures. These constraints likely contributed to flatness; the result alone does not establish a model limitation. The approved portrait and generated take are chest-up with hands outside frame. Hand performance has not yet been tested.

## Performance target

Calm, attentive explanation to one person. Most of the body stays settled. Motion follows a meaningful phrase and returns to rest; it does not continuously accompany every syllable.

| Element | Target for the next controlled test |
| --- | --- |
| Head | One small, irregular tilt or settling movement on a phrase emphasis, returning naturally to center. Avoid repeated nodding or lateral sway. |
| Face | Slight brow and eye engagement on a meaningful phrase; relaxed mouth corners and natural blinks. No sustained sales smile. Lips remain driven by the exact approved audio. |
| Hands | One small open-hand gesture low in frame during an explanatory phrase, then rest. No counting gesture, pointing, repeated pulses or hands near the face. |
| Shoulders | Quiet breathing and a small natural settling response, with no rocking or repeated lean. |
| Camera | Locked. Apparent liveliness should come from the performer. |

These are test directions, not physiological measurements or a universal gesture quota. The public research does not establish a calibrated micro-expression or motion-amplitude control shared across providers.

## Reference roles

Use three separate references: the approved portrait for identity/set; the exact 11.34-second WAV for language and timing; an observed short performance clip for movement quality. A model catalogue helps choose a generator but cannot specify the desired performance on its own. A performance example is an editorial reference unless the selected model actually supports a separate motion driver. Do not treat another speaker's identity or voice as part of the requested reference.

The supplied [awesome-talking-head-generation repository](https://github.com/harlanhong/awesome-talking-head-generation) is a useful research index. Its paper list does not establish a current model ranking or an OE performance standard.

**Selected candidate viewing reference:** [official InfiniteTalk image-to-video demo 0, 2.50–6.50 seconds](https://meigen-ai.github.io/InfiniteTalk/videos/i2v/0.mp4#t=2.5,6.5). Across half-second samples, the torso/shoulder line remains mostly stable; the hands begin together near the lower chest, make a modest opening/lift around 4.5 seconds, and return near rest by 5.0–6.5 seconds. Head position shifts slightly. This provides an observable rest–gesture–rest pattern. Do not borrow the demo's off-camera eyeline or brighter expression. Exclude 7–9 seconds, where the gestures grow. These are sampled-frame observations, not a continuous-playback motion verdict or an owner-approved performance target.

This reference was selected over the more emphatic `video_dubbing/3.mp4` and `i2v/3.mp4`, which does not show hands. The [official project page](https://meigen-ai.github.io/InfiniteTalk/) restricts its generated demos to academic use. Use this clip as a viewing/directing reference only, not an episode asset or a commercial generation input. Any motion-driver input should instead be a suitable authorized performance, ideally a short recording of the owner.

## Verified model research

| Candidate | Established capability | Implication for this test |
| --- | --- | --- |
| [InfiniteTalk](https://github.com/MeiGen-AI/InfiniteTalk) | Audio-driven image-to-video and video-to-video; the latter can carry source head/body motion and camera trajectory. Its own README warns of increasing color shift beyond about one minute for image-to-video. | Relevant to performance reference and longer sequences. Unlimited sequence support does not mean unlimited stable identity/color. |
| [HunyuanVideo-Avatar](https://github.com/Tencent-Hunyuan/HunyuanVideo-Avatar) | Open code/weights for audio-driven animation and emotion conditioning; official setup requires CUDA/Linux. | Technically relevant, but high expressiveness and emotion control are not evidence of restrained performance. Local installation on this Mac is not the simplest next test. |
| [OmniHuman 1.5 on fal](https://fal.ai/models/fal-ai/bytedance/omnihuman/v1.5/api) | Image and audio input, optional direction prompt; under 60 seconds at 720p, under 30 seconds at 1080p. | A suitable short comparison candidate using the same approved portrait and audio. Public provider claims do not establish superiority on subtle expression. |
| [Hedra Character 3](https://www.hedra.com/develop/models/video/hedra-character-3) | Hosted image-and-audio avatar generation; direct provider API. | A candidate for a later controlled comparison; no tested advantage for this portrait or soundtrack has been established. |
| [LongCat-Video-Avatar 1.5](https://meigen-ai.github.io/LongCat-Video-Avatar-1.5-Page/) | The InfiniteTalk maintainers now direct readers to this May 2026 release. | The suggested 2025 shortlist should not be presented as a verified current ranking. No need to expand this small experiment into a broad model benchmark. |

Read-only searches of the connected Higgsfield catalogue returned no matches for InfiniteTalk, OmniHuman, Hedra or Hunyuan. Those models are not confirmed callable through this Higgsfield connection. No fal MCP tools are exposed in this session. No new provider installation, media upload or paid generation was performed for this reference review.

The [official fal MCP documentation](https://fal.ai/docs/documentation/setting-up/mcp) confirms both discovery and execution, including `get_model_schema`, `run_model`, `submit_job` and `check_job`. A configured fal connection would provide access; a research link alone does not connect the account. Its current [InfiniteTalk catalogue](https://api.fal.ai/v1/models?q=infinitalk&limit=50) and [OmniHuman catalogue](https://api.fal.ai/v1/models?q=omnihuman&limit=50) list active endpoints. The [Hunyuan avatar search](https://api.fal.ai/v1/models?q=hunyuanvideo-avatar&limit=50) returned deprecated entries, and no Hedra endpoint was found. Hosted InfiniteTalk has finite endpoint frame limits; the research project's unlimited-length claim is not a hosted API contract.

## Controlled next comparison

1. Keep the current portrait, audio, framing and Wan model; relax only the head/face performance direction. This checks whether the suppression came from the prompt.
2. For visible hands, derive a slightly wider seated reference preserving the accepted face, wardrobe and study, with hands resting low in frame. Evaluate framing separately before combining it with a model change. Hands entering the existing tight crop are possible but make anatomy and edge entry less predictable.
3. Compare the same portrait/audio with one hosted alternative, preferably OmniHuman 1.5, if Wan cannot supply the restrained motion. Keep HyperFrames assembly constant.

Suggested head/face direction, appended after unchanged identity and exact-audio requirements:

> Deliver this as a calm explanation to one person. Keep the torso relaxed and mostly settled. Allow a small natural head tilt and return on one meaningful phrase, with a slight brow lift and attentive eyes. Let the expression soften briefly, then settle. Use ordinary breathing and irregular natural blinks. Preserve the supplied speech, pauses and lip synchronization exactly. Avoid repeated nodding, swaying or a sustained smile. Keep the camera fixed.

Hand direction for the wider-reference version:

> Begin with both hands resting low in frame. On the phrase about building, owning and operating, make one small open-hand explanatory gesture below chest level, then return that hand to rest. Keep the other hand relaxed. Do not enumerate the three words with separate gestures.

Judge the takes at normal speed with identical audio, then inspect fingers, eye/head movement, identity, mouth timing and the return to rest. A winner must feel more engaged than the baseline without drawing attention to the movement. Do not use more movement, a waveform match or a static-frame check as a substitute for that performance judgment.
