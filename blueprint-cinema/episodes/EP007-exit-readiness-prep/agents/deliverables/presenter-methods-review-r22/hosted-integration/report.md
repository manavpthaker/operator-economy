# EP007: hosted performance controls and fal integration

Read-only research, checked 2026-09-08. No generation, upload, installation, account change, credential inspection, or production approval. This report assesses documented capability, not comparative output quality.

**Recommendation under the current photo-and-audio-only constraint:** use **Hedra Character 3**, endpoint `hedra-character-3`, as the explicit Hedra comparator alongside the parent's OmniHuman 1.5 test. Character 3 has a current official v3 endpoint and directly documented restraint guidance. No reviewed evidence establishes that `hedra-avatar` adds stronger steering or is better. Keep the exact existing image and audio, use one restrained prompt, and limit the first comparison to two independent outputs per model. Do not add more post-processing stabilization during this comparison.

## What is actually exposed

| Option | Verified inputs and controls | EP007 implication |
|---|---|---|
| Hedra Avatar / Character 3, current v3 | Image, audio, performance prompt, aspect ratio, resolution, optional duration; speaker positioning in Avatar | Can reuse the approved appearance and exact audio. No independently documented head, mouth, or hand amplitude slider found. |
| fal InfiniteTalk base endpoint | Image URL, audio URL, prompt, frame count, resolution, seed, acceleration | Another still-image-driven performance; not reference-motion control. |
| fal InfiniteTalk video-to-video | Video URL, audio URL, prompt, frame count, resolution, seed, acceleration | Reference footage becomes a real input. It does not expose separate motion-amplitude, lip-only, or pose-lock controls. |

Hedra's current v3 endpoints are `hedra-avatar` and `hedra-character-3`; they have separate catalog entries with largely overlapping descriptions. The older avatar guide uses `/web-app/public` and UUID model IDs, so a new integration should inspect current v3 model schema rather than mix API generations. The publicly readable catalog does not prove that the two names are interchangeable models, that one replaces the other, or that Avatar offers a special steerable mode. [Hedra Avatar API](https://www.hedra.com/develop/models/video/hedra-avatar), [Character 3 v3 API](https://www.hedra.com/docs/api-reference/v3/run-a-model/run-hedra-character-3-hedra-character-3), [legacy avatar guide](https://www.hedra.com/docs/pages/developer/guides/generate-avatar-video).

fal's base model currently documents 480p/720p and 41–721 frames. Its video-to-video page has a material inconsistency: the `num_frames` description says 81–129 while default is 145. The linked live OpenAPI's numeric constraints are **41–241**, still with default 145 and the contradictory description. Do not translate upstream “unlimited length” into a hosted-endpoint guarantee. Confirm the actual request and resulting duration in a short test. [Image endpoint](https://fal.ai/models/fal-ai/infinitalk/api), [video endpoint](https://fal.ai/models/fal-ai/infinitalk/video-to-video/api), [video endpoint OpenAPI](https://fal.ai/api/openapi/queue/openapi.json?endpoint_id=fal-ai/infinitalk/video-to-video).

InfiniteTalk's own repository says it aligns head, body, and facial motion to new audio. Its video mode approximates reference camera movement; this is not pixel-preserving dubbing. Its source inference exposes audio/text guidance controls that fal's inspected schema does not expose. A quiet source performance is a sensible hypothesis, not a guarantee of exact gesture preservation. [Official InfiniteTalk repository](https://github.com/MeiGen-AI/InfiniteTalk).

## Best practices relevant to the failure

Hedra recommends a sharp, well-lit, front-facing and unobstructed face; clean audio; explicit framing/performance/background constraints; and a short test before a long sequence. It says to review lip sync, identity, framing, and gesture, then change one bounded element while retaining working references. [Official presenter workflow](https://www.hedra.com/docs/pages/app/content-creation/create-avatar-video).

Its Character 3 page acknowledges that overly dramatic hand gestures can happen and recommends explicitly constraining motion in the text prompt. It emphasizes clean pronunciation and low noise/reverb. This is evidence that Hedra may have the same failure class, not evidence that changing provider automatically solves it. The current page lists 720p at $0.05/second and 1080p at $0.0625/second: straight multiplication for 5.6 seconds is $0.28 or $0.35 per output, respectively. Billing rounding/minimums and the exact request estimate were not verified; these are arithmetic estimates, not a quote. [Official Character 3 guidance and pricing](https://www.hedra.com/models/video/hedra/character-3).

For EP007, my proposed test direction is: “Fixed eye-level camera. Calm, matter-of-fact delivery. Head upright with slight natural adjustments. Forearms supported on the desk; hands mostly resting, with small relaxed finger and wrist changes. Natural blinking and restrained facial expression.” This is a proposed prompt, not a tested preset. Preserve the locked narration. Evaluate at normal speed with sound; mouth timing and naturalness must both pass. Do not accept a lower head-displacement statistic if facial scale, neck, hands, or background look wrong.

The InfiniteTalk video-to-video findings above explain the technical distinction only. **That route is excluded from the current next action because the user is limiting the test to the existing photo and audio.** No new recording or motion reference is requested.

## MCP versus model versus provider

InfiniteTalk is the model; fal is one hosting provider; MCP is a tool transport. Connecting MCP changes access, not generation quality.

The official **fal Run MCP** exists at `https://mcp.fal.ai/mcp`, using Streamable HTTP and a bearer fal API key. The current documentation lists 11 tools, including model search, schema, pricing, inference, asynchronous submission/status/results/cancellation, and upload. It is distinct from fal's account-operation Platform MCP. Run MCP documentation currently says OAuth is unsupported. [Official fal Run MCP](https://fal.ai/docs/documentation/setting-up/mcp).

No callable fal or Hedra MCP tool was found in this session's tool-name inventory. This is a session capability observation, not proof that no account or configuration exists elsewhere. Credentials were not inspected. The MCP could expose the hosted InfiniteTalk endpoint after connection, but only the endpoint's actual schema and limits. Direct authenticated API/SDK calls reach the same model without MCP.

## Decision boundary

Use one fixed passage, appearance, framing, and final audio for the parent's photo-only OmniHuman 1.5 versus Hedra Character 3 comparison. Review at most four initial samples before deciding. If neither improves normal-speed owner review, stop that first pass and reassess; do not silently enter another prompt lottery. No reviewed source establishes that either is the best model for this specific restrained performance; comparable owner-specific outputs are still missing.

An older Hedra Omnia model link returned “Model not found” during this review, and the current Omnia blog describes partner post-training rather than an actionable restraint-control API. Do not select it from older integration instructions without rechecking the current model catalog. [Current Omnia blog](https://www.hedra.com/blog/hedra-omnia-frontier-ai-video-model).
