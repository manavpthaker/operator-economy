# One continuous post-title presenter audition

Status at proposal: prepared; awaiting separate paid-generation authorization. Subsequently authorized by the owner's "approve"; execution is recorded separately in provider/GENERATION-AUTHORIZATION.json and provider/SUBMISSION-ATTEMPT.json. The proposed parameters below are preserved.

## Selected route

Use `fal-ai/infinitalk` image-and-audio generation for one new performance. This endpoint accepts a still image, the supplied audio and a freeform performance prompt. Unlike a head-region edit of reused footage, it can generate a new continuous body performance for the full passage. The earlier local InfiniteTalk comparison establishes that this route runs at720p/25fps; it does not establish that this new take will look better. The earlier failed Kling Avatar take remains rejected.

Settings:720p,377frames,acceleration `none`, seed42. Expected native duration15.08seconds. One submission maximum, zero retries, no follow-on lip-sync pass or voice generation. The expected price is about$6.03 at the [published720p rate](https://fal.ai/models/fal-ai/infinitalk) of$0.40/second. Proposed estimated spending ceiling:$7. No top-up, purchase, paid overage or account changes. Verify the current estimate before submission; stop if it exceeds the cap or cannot be bounded.

## Exact input and timing

Use the original presenter reference pinned in `provider/PROPOSED-REQUEST.json`. The generation audio preserves every PCM sample of the existing15.0-second post-title excerpt and appends0.12seconds of zeros solely as a generation handle. The original source file and final R22 soundtrack remain unchanged. This handle is necessary because previous InfiniteTalk requests were rejected when the requested picture exceeded the audio duration.377frames is an8n+1 count and fits within the15.12-second derivative.

Do not extend the upstream master excerpt past74.5: the next sentence begins thereabouts. The handle must be zeros, never leaked next-sentence audio. If successful, trim the returned picture to the original15-second interval without retiming. The final soundtrack uses the unchanged original excerpt. If the provider returns insufficient picture coverage or shifts the speaking performance, reject it rather than freezing, stretching, repeating or repairing automatically.

## Direction

The exact supported text prompt is stored in `provider/PROPOSED-REQUEST.json`. It asks for a relaxed speaking jaw, naturally changing lip shapes, stillness between small head adjustments and one subtle forward inclination at the viewing promise. It preserves the existing face, glasses, shirt, study and light. It does not request a finger gesture, a new voice, an exaggerated expression or another camera move.

R22's approved crop changes stay at review62.916667 and67.916667. They become visual reframes of one continuous take, eliminating the old performance restart at the first cut and retaining the continuous-playback refinement at the second. Earlier scenes and the tagline remain as reviewed.

## Acceptance

Review all15seconds at normal speed with the original audio, then inspect motion without sound. Compare against R22 in the same crop states. Accept only if mouth timing remains at least as convincing as the accepted version, jaw/lip articulation is less restricted, head movement avoids repeated nod/sway/reset patterns, and the face remains recognizable without warping, extra text or drifting background. Verify open vowels and closed consonants rather than asking for constant mouth opening. Check headroom at all three crop levels.

Stop after this one result, including any failure or ambiguous submission outcome. No unused budget authorizes another model or another take. This is an isolated private review, not a canonical narration change or release approval. The last paid grant was consumed; [Blueprint Cinema's project rules](../../../../../AGENTS.md) require separate authorization before another paid generation.

Provider source: [InfiniteTalk API schema](https://fal.ai/models/fal-ai/infinitalk/api). These are supported controls and price estimates, not a quality guarantee. The generation-handle constraint is grounded in local prior provider error receipts.
