# R3 c03: narration-relevant editorial test

Status: generated once; technically valid; context review assembled; **not an exact prompt-conformance pass or a production selection**. The user selected Kling as the model and requested a relevant edit. Original Revision C remains unchanged.

## Provenance

- Direction at submission: R3-RELEVANT-EDIT.md, SHA-256 cf495ee37d0bf7bbc5ad8c996a2a640da1ae16200dc40cbc99c1453fa4b7080b.
- Immutable prompt packet: R3-KLING-RELEVANT-PROMPT.md, SHA-256 7c44058cb2c3627891d7870e528ed10fec96b23627f709f48e247c99ab4f0fc5. Positive section 1,595 characters; negative extension 531 characters plus the generator's standard prefix.
- Provider/model: fal.ai, fal-ai/kling-video/v3/pro/image-to-video. Model version/seed not exposed.
- Request: 01a079d4-052b-7ee0-9bb2-524cc253d29c; submitted 2026-09-07T03:05:33.353Z; generated/downloaded 2026-09-07T03:09:58.732Z. These are September 6 locally.
- One start reference only, r3-route-start.png, SHA-256 5e13a9a45965a39d260dc7a25bd7d713c671619fa76dc5e8b384b6419bc639a7. No end frame, no generation retry.
- Parameters: duration "8", generate_audio false, shot_type customize, cfg_scale 0.5. Resolution/FPS/aspect ratio are not sent. The generator's provider-default label is metadata only.
- Untouched source: renders/candidates/r3-unfinished-gesture.kling-pro.c03.full-generated.mp4, SHA-256 7c71e1feba373fae1e3710038e42eb734814945e35865fa486f0571099429ac2.
- Full response: source filename plus .response.json, SHA-256 a9506fa5be16c3ad13b6d751f1823efe5876b95244f940843f33108dcad44e4b.
- Cost: one silent eight-second request, list estimate $0.896 within the agent's $0.90 cap. Endpoint did not return an account debit. Session-verified [model/pricing page](https://fal.ai/models/fal-ai/kling-video/v3/pro/image-to-video) and [API schema](https://fal.ai/models/fal-ai/kling-video/v3/pro/image-to-video/api).

## Observed source

H.264 Main, 1916×1080, yuv420p, 24 fps CFR, 193 frames, 8.041667 seconds, 10,573,229 bytes. No audio. Complete strict decode passed. All 193 decoded frame hashes are distinct: final stillness is a held performance, not duplicated freeze frames.

The main sheet, held ticket, binder, keys and buyer remain substantially stable. No generated writing or visible speech was observed. The pencil makes several explanatory sweeps and returns nearer the owner's side, rather than performing exactly the one suspended unfinished gesture in the prompt. Large movement arrests around source frame 136 (5.667s); finer hand/pencil settling continues afterward. Do not call the final image perfectly motionless.

An extra white paper fragment appears at the extreme right edge during the source. This violates the original object-count contract. The review excludes that edge with a constant crop: scale 1.093, source left anchored, displayed top -24px. It does not repair or alter the untouched source, and is not proof that the generation followed its prompt.

The c03 source therefore does not pass the strict single-gesture/object-count generation brief. It is retained as a conditional **editorial review**, because the broad start/stop behavior can be judged against the actual narration. This does not silently waive the production gate or authorize another request.

## Actual review edit

Project: reviews/r3-relevant-edit; 1920×1080, 30 fps preview, 17.12 seconds. Episode excerpt: 17.96–35.08. Studio: http://localhost:3012/#project/r3-relevant-edit.

| Local review time | Episode time | Actual edit |
| --- | --- | --- |
| 0–3.32 | 17.96–21.28 | Original full-frame question and type styling; held for the entire question. |
| 3.32–9.96 | 21.28–27.92 | c03 source 0.625–7.265, 1×, fixed crop, no freeze, no animated zoom, no speed ramp. |
| about 8.362 | about 26.322 | Source f136 gross arrest, approximately 18ms before stops begins at 26.34; this is visual judgment, not automatic event detection. Fine settling remains. |
| 8.84–9.96 | 26.80–27.92 | Same real source held performance through the deliberate narration pause. |
| 9.96–17.12 | 27.92–35.08 | Hard cut on Because into copied authored arithmetic, not a geometric page match. |

Only the locked narration plays: public/audio/opening-narration.wav, SHA-256 120c7a64ae8582f55f9bb4338c9ec276d763d79d88718aac482fc81c48ddbfb1; media start 17.96, duration 17.12, volume 1. No audio re-generation, rewritten words, timing change, music, or added dialogue.

The copied model removes the old incoming carrier and its scale/fade; evidence anchor is present on the cut. Original business/owner/equation/condition timings remain. Later envelope/oxide actions beyond the excerpt are removed only in the copy. No old page-fill matte, ticket graphic, hand patch, route overlay, or page-push sits over c03.

## Verification and limits

- HyperFrames 0.8.30 is current per read-only upgrade probe. No version change.
- Full check at 13 samples: lint/runtime/layout/motion zero findings; 16/16 visible text contrast checks passed before the last fixed-crop cleanup. Final verification is recorded in the review's REVIEW.md.
- Source contacts: snapshots/r3-kling-gesture-c03/contact-sheet-24f.png; action-f000-108.png; stop-every-frame-f112-159.png; frame-136-settle.png. The dense stop sheet contains every frame 112–159, chronological row-major.
- Studio was loaded with a 17-second duration, Play enabled, audio unmuted at 100%, and playback advanced. This is not an encoded-master or human watch-down approval.
- Native 24 fps in the established 30 fps review is diagnostic. No optical flow or production cadence decision has been approved.
- No final render, production integration, Step 3 advance, publication, commit, or push.

Preserved Revision C checksums: index.html 2b1e501a0102dbbf3df3d2f89872b5579b9ad01113784c18053e493bcda19692; compositions/sequences/02-question-answer.html 13cf504de5b3ec37245c257aa959fdc33d6dd778e6d62fdb131448c0d5606b57; compositions/sequences/03-model-exposure.html daa513b6979b7a754ee553204fcdbcfd1af90e3afc231d579e18a05f13cdfd6f. Verified unchanged at handoff.
