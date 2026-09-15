# R21 final presenter line: technical audit

Date: 2026-09-10 UTC. Role: read-only technical/editorial diagnosis. No source media, preview, narration, approval, or gate was changed.

## Decision

There is no supported fixed-offset correction to apply. The browser picture preserves the provider's complete video stream, its first presentation timestamp, its frame count, and its rate. The provider's audio is aligned to the exact narration used in the preview. Shifting the picture a guessed number of frames would move an already correctly conformed result away from its submitted audio without evidence that this fixes the mouth.

The user's report can still identify a real generated-articulation defect. File alignment does not prove that the model made correct mouth shapes, and this audit does not certify perceptual lip sync. Browser playback synchronization has not been measured here. Those are the remaining possibilities after the media conform checks.

## The cut before “By the end”

The cut at review **62.916667** is deliberate and was documented in R15. It joins two separately generated lip-sync pickups. Their underlying 404 performance windows were source frames 0–154 for A and 83–289 for B. They are not one continuous body performance.

“Anything” ends at review **62.800**. “By” starts at **63.380**. The cut is 0.116667 seconds after the preceding word and 0.463333 seconds before “By,” inside a 0.58-second inter-sentence interval. It loses no spoken word. This makes it technically clean but does not make the visible pose discontinuity editorially desirable. A continuous replacement performance would address that cause; a dissolve or arbitrary frame shift would not.

Evidence: R15 `REVIEW.md` lines 5 and 9; R15 `provider/INPUTS.json`; R20 `index.html` post-title definitions; locked word transcript W000165–W000168.

## Media evidence

| Check | Provider B | Browser B | Result |
|---|---|---|---|
| Picture duration | 8.583333 seconds | 8.583333 seconds | Equal |
| Picture frames | 206 | 206 | Equal |
| Rate | 24/1 | 24/1 | Equal |
| First PTS | 0 | 0 | Equal |
| Video time base | 1/12288 | 1/12288 | Equal |
| Encoded video stream SHA-256 | `ab03e9de03d35cd498f34db05afe20d2effa7f4bddb3b1ab4a0e6fa0335c83ae` | Same | Stream-identical |

The browser asset is a video-only remux; stripping provider audio did not change the picture stream. R20 plays B from source time zero at review 62.916667. The original master is played from 59.5 at review 56.5, so at the B edit it reaches master 65.916667, the exact submitted pickup start.

The 48 kHz mono pickup contains **412,000** samples, cut from source sample range **[3,164,000, 3,576,000)**. Decoded pickup samples are exactly equal to that range in R20's `review-narration-extended.wav`: maximum absolute sample difference 0.

Cross-correlation of decoded provider AAC against the pickup was searched within ±4,800 samples (±100 ms):

| B local window | Best provider-minus-pickup lag | Pearson correlation |
|---|---|---|
| Full clip | 0 samples | 0.9998134 |
| 0–3 seconds | 0 samples | 0.9997933 |
| 3–5 seconds | 0 samples | 0.9998236 |
| 5–6.5 seconds | 0 samples | 0.9998499 |
| 6.5–8.58 seconds | 0 samples | 0.9997940 |

The provider AAC decodes to 412,672 samples because of codec frame padding; the indexed audio duration is 8.583 seconds and start PTS is zero. The padding is at the tail and does not imply an onset delay. The correlation checks include the final phrase and do not show cumulative audio drift.

## “One number” direction

| Word | Master time | Review time | B local time |
|---|---|---|---|
| and | 70.18–70.58 | 67.18–67.58 | 4.263333–4.663333 |
| the | 70.64–70.84 | 67.64–67.84 | 4.723333–4.923333 |
| one | 70.94–71.16 | 67.94–68.16 | 5.023333–5.243333 |
| number | 71.28–71.61 | 68.28–68.61 | 5.363333–5.693333 |
| that | 72.04–72.20 | 69.04–69.20 | 6.123333–6.283333 |

A replacement should have one deliberate emphasis event: prepare just before “one,” peak on “one number,” then settle before the next clause. If a finger is used, it rises once, remains below the face, holds through “number,” and lowers once. This is a performance instruction; a lip-only remap cannot reliably author a new hand gesture. The previously rejected generation is not evidence that further identical retries would improve it.

Relaxed articulation means letting jaw and lips follow the actual phonemes, not instructing constant open-mouth speech. Avoid a permanent smile or teeth display. Review the complete sentence at normal speed with the locked track, especially the transitions through “one,” the /m/ and /b/ shapes in “number,” and the clause after it. A phrase-only mouth test can identify whether errors are local or consistent before any broader edit.

A camera punch-in can give the phrase editorial emphasis, but it cannot repair lip sync or add vocal stress. A volume bump also cannot create the desired natural prosody. If audible stress needs changing, that is a newly directed voice performance and its corresponding lip sync must be reviewed together; do not disguise an audio rewrite as a picture correction.

## Scope and limits

- Input hashes supplied by the orchestrator all matched.
- No normal-speed audiovisual playback verdict was issued in this audit. All conclusions above are file, timestamp, sample, and source-contract checks.
- Missing canonical EP007 `README.md`, `episode.json`, and `input-lock.json` under this episode folder were observed; this is an existing isolated experimental review lineage, not a new canonical episode approval.
- No external sources, paid calls, uploads, synthetic generation, source edits, or approval changes occurred.
- Recommended disposition: retain the current timing until perceptual review supports a specific correction. Treat generated articulation and intentional emphasis as unresolved performance work, not a known conform offset.

## Follow-up: narrow next step for articulation and stress

**Recommendation:** settle the intended final-sentence vocal delivery before another paid lip-sync pass. If the requested stress is audible, prepare one isolated final-sentence audition, using the existing two-stage voice chain and exact words, with one deliberate emphasis on “one number.” Review that audio first; synchronize the selected result once. Generating new lips against unchanged audio before deciding vocal emphasis risks paying twice. This does not require rewriting the sentence or rerendering the episode, and the existing master stays intact while the audition is reviewed.

A local amplitude envelope could make these words louder, but it cannot add natural changes in pitch, vowel duration, attack, or phrasing. It is a mix accent, not a new vocal performance. Likewise, a picture punch-in can mark importance but is not an articulation repair.

### What React-1 can test

React-1's `lips` mode is a rational **bounded comparison for articulation only**, because it edits the mouth while minimizing other facial changes. It is not proven superior to Sync 3 on this presenter, and there is no local React-1 result establishing improvement. It cannot create audible stress, or a timed hand gesture; the broader `face` and `head` modes would reopen expression and movement risks that the user already disliked. These limits follow from the [Fal API schema](https://fal.ai/models/fal-ai/sync-lipsync/react-1/api) and [Sync model modes](https://sync.so/docs/models/react), checked 2026-09-10.

If retaining the current audio, the narrow trial is one B-only generation using the **original unsynchronized performance source**, not a pass over already altered Sync 3 lips:

- Video: `r15-post-title/provider/inputs/performance-b.mp4`, SHA `dae03d667c44b7faf29d3d8b13317a3939ef6997885b05c0efb5dbc66eb58cf4`.
- Audio: `r15-post-title/provider/inputs/pickup-b.wav`, SHA `e37976fde23e50265e7e6dde1a034d873d8b39f87d89f074d4da19ae7ac49072`.
- Duration 8.583333 seconds; proposed model `fal-ai/sync-lipsync/react-1`, `model_mode: lips`, `emotion: neutral`, `lipsync_mode: cut_off`. Explicitly override the API's default `bounce`; no looping, remapping, or automatic repair pass.
- Current [Fal price](https://fal.ai/models/fal-ai/sync-lipsync/react-1): $10 per minute. Nominal 8.583333 seconds is $1.430556 before output padding. A separately authorized $2 estimated ceiling, one submission, zero retries would be a concrete experiment boundary, not a guaranteed final invoice or promised fix.

These relative video/audio paths resolve under `blueprint-cinema/experiments/EP007-NET-NEW-UNFINISHED-ANSWER-003/hyperframes/reviews/`.

### Existing voice capability

The actual EP007 configuration is `n3-two-stage-acted-guide-v2`: Google `gemini-2.5-pro-tts`, voice **Algieba**, candidate-C4 register; then `eleven_multilingual_sts_v2` onto Original C `scMbPZwQjr40V1MzL3Nj`. Read-only source inspection confirms the implementation exists in:

- `operator-blueprint-v2/02-narration-production/tools/capture_n4b.py`.
- `operator-blueprint-v2/02-narration-production/tools/calibrate.py`.
- `operator-blueprint-v2/02-narration-production/prompts/NARRATOR-REGISTER.candidate-C4.google-gemini-tts.style-instructions.json`.

The capture code explicitly chooses Algieba; the lower-level calibration tool defaults to **Achird**, so a new guide must specify Algieba rather than inherit the default. Transfer settings are similarity 0.8, speed 1.0, stability 0.4, style 0.0, speaker boost true, seed 2026082501, PCM 48 kHz. This is implementation capability, not current provider-account or budget authorization. No credential or account check was performed.

Use the pinned v4 master and the verified pickup B as continuity references. The present `raw/c02.guide.wav` and `raw/c02.saved-c.wav` hashes differ from the original take-register entries, consistent with the later recapture lineage but not independently reconciled in this audit; do not present those older registered hashes as current. Do not call the full-capture script against the canonical episode as a shortcut for a bounded audition: it can write episode state and has an automatic-attempt mechanism.

### Precise authority

The user requested stronger emphasis and articulation repair. That provides creative direction for preparing the next candidate; it does not revive the exhausted paid grant.

`r19-tagline-restored/provider/GENERATION-AUTHORIZATION.json` allowed **one** Kling Avatar submission, **zero** retries, a **$2 estimated ceiling**, and expressly excluded a narration rewrite and extra lip-sync pass. `provider/GENERATION-REVIEW.json` records that submission as completed, rejected, and authorization exhausted. The earlier R15 grant allowed two Sync 3 submissions, both consumed, with no additional submission after failure or uncertainty. Neither covers React-1, a new voice guide, or a new voice transfer.

`blueprint-cinema/AGENTS.md` requires separate authorization before paid generation. A new paid proposal must name the selected path, exact inputs and model(s), maximum submissions, cost ceiling, and stop condition; an audio audition would need both guide and transfer accounted for before optional lip-sync. This audit has not priced a fresh voice audition and does not invent that budget.

The current `narration-lock.md` binds v4 master SHA `d8f7cb9630ae12ad427dca2c7bd1f29611f56c7985ce900ea312df3b9fec8da9` and states: “Any sample-level change to this master invalidates the transcript, the pause map, the technical pass, this lock, and the Step 3 handoff.” Therefore preserve the master and review any new delivery as an isolated candidate. If selected, record new timing/conform provenance rather than claiming it remains byte-identical under the old lock.

### Combined proposal budget, checked 2026-09-10

Use **$3 estimated cash ceiling plus up to 250 existing ElevenLabs credits**, at most one guide, one transfer, and one React-1 submission; zero retries at every stage. This is a proposed authorization boundary, not a current grant. No credit purchase, account change, top-up, or overage is included.

| Stage | Published unit price | Rough 9-second use |
|---|---|---|
| Google Cloud Gemini 2.5 Pro TTS | $1 per million input text tokens; $20 per million audio tokens; 25 audio tokens/second | $0.0045 output plus prompt tokens; normally below $0.01 total |
| ElevenLabs Voice Changer | 1,000 credits/minute | 150 existing credits |
| Fal React-1 | $10/minute | $1.50 |

Sources: [Google Cloud TTS pricing](https://cloud.google.com/text-to-speech/pricing), [ElevenLabs current pricing FAQ](https://elevenlabs.io/pricing), [Fal React-1 pricing](https://fal.ai/models/fal-ai/sync-lipsync/react-1). The nominal total is approximately **$1.51 cash plus 150 existing credits**. The maximum 250-credit allowance corresponds to 15 seconds; the footage limit below is stricter.

The [Google model documentation](https://docs.cloud.google.com/text-to-speech/docs/gemini-tts) lists 8,192 input and 16,384 output tokens for Pro TTS. Even reserving the entire listed token ceilings for a malformed single guide gives $0.008192 + $0.327680 = **$0.335872**. The generic 15-second React-1 allowance is $2.50, so these two stages total $2.835872 before tax at published rates. This provides margin within the proposed $3 estimated cash boundary without assuming a perfect guide duration. A failed or too-long guide still stops the chain; this reserve does not authorize reuse, a retry, or downstream work on an unusable take.

ElevenLabs' current [billing guidance](https://elevenlabs.io/docs/overview/administration/billing) says credit conversion depends on the account's plan/PAYG arrangement. The legacy $0.30 per 1,000-credit article is not a universal current account rate. An exact all-in dollar equivalent cannot be certified without checking the account. Therefore explicitly authorize consumption of existing credits as a separate unit and stop if sufficient existing credits are unavailable. No subscription or billing change is necessary to prepare this proposal.

### Actual source-duration ceiling

The eligible original performance source is:

`blueprint-cinema/experiments/EP007-PREMIUM-CONTROLLED-004/review-media/404.mp4`

SHA-256 `a0de31c36bde22219a1e067178b86cf750e7da1f11a69a775c370c82df6f29dd`. Live `ffprobe` confirms **289 frames at 24 fps, 12.041667 seconds**, 1920×1080, first PTS zero.

The existing B source starts at frame 83. Only frames **[83,289)** remain: **206 frames, 8.583333 seconds**. That source cannot supply 9 seconds or 15 seconds without changing the starting window or manufacturing duration.

- **Exact B performance-window boundary:** keep source frame 83 and stop if the usable new voiced sentence plus required handles exceeds 8.583333 seconds. Do not force it shorter by retiming, cut off its final word, or fill missing picture.
- **If the new proposal explicitly permits a different contiguous window of the same 404 take:** a 9-second candidate can use frames **[73,289)**, or another 216-frame contiguous select reviewed for performance. The total available source can never exceed 12.041667 seconds. That is the stricter ceiling than React-1's 15-second model limit.

**Orchestrator's selected proposal policy:** use a contiguous tail window from the original 404 take, sized to the final accepted audio, with final audio duration **at most 12.0 seconds**. End at exclusive frame 289; start at `289 - ceil(audio_seconds * 24)`. Target approximately 9 seconds and retain 0.1–0.2 seconds of natural handles where the available window allows. Account for any retained audio handles inside the final accepted audio duration. This explicitly proposes an earlier source start when needed; the changed performance window must be reviewed. No retime, repetition, synthetic extension, or cut-off words. Stop if the audio exceeds the available source or cannot fit complete speech and necessary handles.

Absolute source path: `/Users/brownmanbrain/GitHub/operator-economy/blueprint-cinema/experiments/EP007-PREMIUM-CONTROLLED-004/review-media/404.mp4`.

New voiced duration is unknown until the guide/transfer exists. Stage each next call only after complete words, natural stress, duration, and sufficient picture coverage pass. The submitted audio and video should have matching complete coverage; `cut_off` is a guard against looping, not permission to truncate the sentence. The proposed $3 cash plus 250 existing-credit boundary conservatively covers this stricter 12-second source policy at published rates, without top-up or overage.
