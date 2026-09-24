# EP007 fal comparison — September 8, 2026

**Four native clips are ready for owner review.** [Open the new comparison](comparison.html).

All four outputs are archived under `../media/repair-r23/`, bound to their exact request IDs and SHA256 hashes in `native-outputs.json`. All pass full decode and measured audio alignment checks. There is no measured early-to-late audio drift. These checks establish file integrity and audio provenance; visual lip sync, naturalness and owner acceptance remain unverified.

The owner supplied the FAL_KEY location for the four-sample comparison and explicitly selected InfiniteTalk through fal for the two slots originally proposed for Hedra Character 3. The exact existing image, exact 5.600-second WAV and common motion prompt are preserved. No new photo, voice, reference performance or geometric head correction is included.

| Samples | Model | Settings | Estimated pair cost |
|---|---|---|---|
| OmniHuman 01–02 | fal-ai/bytedance/omnihuman/v1.5 | 720p; turbo off; no seed field exposed | $1.792 |
| InfiniteTalk 01–02 | fal-ai/infinitalk | 720p; 137 frames; acceleration none; seeds 42 and 173 | $4.384 |

Estimated successful-output total: **$6.176**, before unverified billing rounding and possible failed-request charges. InfiniteTalk's $0.20/second base price doubles at 720p. This is an estimate, not recorded spend; billing reads were not permitted by the supplied key.

## Native results

| Samples | Native picture | Native audio | Measured early / late audio lag |
|---|---|---|---|
| OmniHuman 01–02 | 1248×704; 25fps; 141 frames; 5.640s | 48kHz mono AAC; 5.600s | 0ms / 0ms |
| InfiniteTalk 01–02 | 1280×704; 25fps; 137 frames; 5.480s | 5.480s | 0ms / 0ms |

All cover the checked final-word window through 5.35s. InfiniteTalk omits source audio from 5.48–5.60s: a near-silent tail, measured at RMS −107.5dBFS and peak −90.3dBFS. The supplied source WAV and native returned media are unchanged. No respeeding, audio replacement or head correction was performed.

Sampled observations, not full-speed verdicts: OmniHuman retains a forward head dip near “straight.” InfiniteTalk 01 has less first-sentence head dip but more two-handed movement. InfiniteTalk 02 emphasizes a right-hand lift and develops more side/head lean toward the end; later room/window details also change. All need normal-speed review, especially the mouth during the pause and second sentence. No sample is declared a restrained-motion winner from stills.

Sources: [OmniHuman pricing and API](https://fal.ai/models/fal-ai/bytedance/omnihuman/v1.5), [InfiniteTalk pricing](https://fal.ai/models/fal-ai/infinitalk), [InfiniteTalk API](https://fal.ai/models/fal-ai/infinitalk/api). Exact authenticated schemas and base prices are stored alongside this file. The upstream duration investigation is in `../../../episodes/EP007-exit-readiness-prep/agents/deliverables/presenter-methods-review-r22/hosted-integration/execution-readiness/`.

## Actual request state

Before top-up, the first OmniHuman submission returned HTTP 403. A single diagnostic retry of that known rejected request captured this provider response:

> User is locked. Reason: Exhausted balance. Top up your balance at fal.ai/dashboard/billing.

The original failures remain in each sample's `prior_attempts`. After top-up, one request failed to download inline audio; fal CDN uploads resolved this with exact-byte readback verification. InfiniteTalk rejected both initial 145-frame requests because they required 5.80s of audio; one 140-frame request was rounded to a 5.64s window and also rejected. Its compatible 137-frame requests produced the two final clips. In total: 11 submission attempts, three HTTP 403 rejections, four terminal input failures, and four successful native clips. Actual charges remain unverified: fal's [FAQ](https://fal.ai/docs/documentation/model-apis/faq) says some HTTP 422 errors can incur GPU charges. No assumption of free failed requests or automatic refunds is made.

## Current follow-through

1. The four-output comparison is complete. No more generation is part of this round.
2. Local preparation verifies hashes, CDN manifest and schema fields. It does not load credentials or call a provider:
   `python3 blueprint-cinema/experiments/EP007-PRESENTER-001/repair-r23/fal_benchmark.py prepare`
3. Request records preserve prior attempts. Retries are permitted only for explicitly inspected terminal input failures or known HTTP 403 rejections, never accepted or uncertain jobs.
4. The returned media files and hashes have been verified. Technical reports and contact sheets are in `../../../episodes/EP007-exit-readiness-prep/agents/deliverables/presenter-methods-review-r22/forensics/execution-qa/`.
5. Review full 1x playback with sound, then muted motion. Do not inherit Q's timing measurements or M's acceptance. The app's request to open the comparison page returned `queued`; this does not establish that the panel was visible or that playback occurred.

Stop after four initial results for owner review. All episode production and release gates remain unchanged. No short sample is final episode approval.
