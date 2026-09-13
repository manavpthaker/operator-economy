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

The initial Higgsfield preflight balance was 122.38 credits. Following two seven-second tests, the fresh account read on 2026-09-13 reports 31.38 credits, Ultra plan, and no available MCP unlimited allowance. The user's actual credit purchase rate is unknown, so no dollar conversion or percentage savings against Higgsfield is claimed.

## After owner accepted test-02

The exact delivered test is now the quality baseline; see test-02/OWNER-REVIEW.json. A cheaper renderer must preserve its likeness, ordinary delivery and original voice timing in playback. Approval of this clip is not evidence that another provider can match it.

Current public prices were rechecked on 2026-09-13. Add HeyGen Avatar IV Photo Avatar API as the second bounded challenger: $3/minute, billed by actual generated seconds, with supplied audio and a photo supported directly. That is approximately $2 for 40 seconds or $0.35 for the same seven-second sample. Pay-as-you-go API funding is separate from HeyGen's web subscription. Any avatar-creation calls, top-up requirements, voice generation, retries and postproduction are additional; the proposed comparison reuses the existing image directly.

Recommended next decision: compare one identical seven-second sample using the approved V12 PNG and Original C WAV on WaveSpeed InfiniteTalk 720p (published estimate $0.42) and HeyGen Avatar IV (published estimate $0.35). Combined generation estimate $0.77, subject to live estimates and account funding. Do not open a broad model search or tune away from the accepted baseline. Prefer the lowest cost per accepted take including failed renders and repairs. Neither test is submitted or authorized by the cost question.

For recurring production, lock the exact script and voice first, reuse accepted nearly frontal wardrobe/room references, generate from the approved audio, review the full spoken take, and only then apply the existing Counterproof captions. Avoid routine full-video lip-sync repair when an audio-driven model already passes review. Keep Seedance plus Sync as the proven short-test fallback until an alternative passes.

Higgsfield's official help states that normal web Unlimited does not cover MCP/CLI generation. The current browser is signed out, so active web Unlimited models and expiry were not verified. If the owner already has active Seedance 2.5 web Unlimited, manual web generation could retain the model while changing generation cost; do not infer that entitlement from the Ultra plan alone.

Same-model price checks do not reveal an obvious large saving: WaveSpeed lists Seedance 2.5 at $0.36/sec for 720p without reference video, and Runway API lists $0.30/sec. These still leave potential Sync costs and require their own supported reference/likeness workflow. No provider switch or portrait-access workaround was attempted.

Additional official sources:
- https://help.heygen.com/en/articles/10060327-heygen-api-pricing-explained — use the specific Photo Avatar IV table ($3/min), not the generic introductory $4/min statement.
- https://developers.heygen.com/audio-to-video — existing image and audio accepted; length follows supplied audio.
- https://developers.heygen.com/avatar-iv — image-driven controls and expressiveness.
- https://higgsfield.ai/creator-hub/help-center/ai-models/how-do-i-use-seedance — web Unlimited versus MCP/CLI billing.
- https://wavespeed.ai/models/bytedance/seedance-2.5/text-to-video — published same-model rates; exact reference support still needs preflight.
- https://docs.dev.runwayml.com/guides/pricing/ — Seedance 2.5 720p is 30 credits/sec, $0.01/credit.
