# Week 2 cost comparison

Checked 2026-09-13 in response to the owner asking for a more cost-effective route than Higgsfield. These are generation estimates, excluding voice, image generation and retries. Final Original C audio is 38.870208 seconds, which rounds to 39 billed seconds on WaveSpeed: estimated $2.34 at 720p. A live provider estimate governs any submission. The comparison below uses an even 40 seconds for readability.

| Route | Verified public rate / current preflight | Illustrative 40-second video |
|---|---|---|
| WaveSpeed InfiniteTalk, 720p | Published $0.06 per second, input duration rounded up to a whole second | $2.40 |
| fal InfiniteTalk, 720p | $0.20 per second with a 2x 720p multiplier | $16.00 |
| Existing Higgsfield Seedance 2.5, 720p high bitrate | Read-only current preflight: 21 seconds = 136.5 credits, equivalent to 6.5 credits per second | 260 credits before lip-sync repair |
| fal Sync v3 repair, if needed | $8 per minute | $5.33 in addition to source video generation |

Sources:
- https://wavespeed.ai/models/wavespeed-ai/infinitetalk
- https://wavespeed.ai/docs/how-pricing-works
- https://fal.ai/models/fal-ai/infinitalk
- https://fal.ai/models/fal-ai/sync-lipsync/v3
- Higgsfield estimate_video_cost, seedance_2_5, omni_reference, 21 seconds, 9:16, 720p, high bitrate, generated audio enabled: 136.5 credits exact, no job submitted.

WaveSpeed requires an account and prepaid balance, with no subscription required. Its documentation says final pricing can differ from the published rate; obtain a live estimate before submission. No WaveSpeed connector or key was found in the current runtime or the scoped Content OS / OE environment files. No account was created or topped up.

Recommendation: first test about ten seconds of the approved voice against the new fixed desk reference, approximately $0.60 at the published 720p rate. Evaluate the mouth, face texture, eyes and restrained expression at normal speed. A dedicated audio-driven model can avoid generating native speech and then paying separately to restore the desired clock, but naturalness and actual sync remain unverified until playback. Do not infer quality from provider marketing or treat the cost question as approval to open a new paid account.

The existing Higgsfield preflight balance was 122.38 credits. There is insufficient balance for the illustrative full Seedance take. The user's actual credit purchase rate is unknown, so no dollar conversion or percentage savings against Higgsfield is claimed.
