# Revision 03 quality checks

The owner liked revision 02's voice better and requested quicker, more varied delivery plus livelier eyes and facial expression. The new image-and-audio reference choice is a bounded performance test; it is not evidence that the prior video caused flatness.

## Voice

- New source uses the same Algieba-to-Original-C identity route and unchanged transfer settings.
- Actual source length is 8.173417 seconds, versus 9.984583 seconds for revision 02 B. This is 1.81 seconds shorter and a larger pace change than the initial 8.6–9.1-second target. No speech speed processing, cropping or retiming occurred.
- Independent ASR verifies all 23 exact words. The final sentence runs near 7.24–7.84 seconds; the endpoint is quiet.
- Directed pitch/pace variation and subjective naturalness require listening. They are not established by ASR or duration.

## Picture, synchronization and delivery

- Native and restored picture preserve 720 by 1280, 24 fps, 217 frames and 9.041667 seconds; strict full decoding passed.
- Native and restored samples show more brow/forehead and cheek variation than reviewed revision-02 samples. This upper-face variation survives restoration; appearance, wardrobe and home framing remain consistent. The exact requested contextual glance is not established by still sampling. See `visual-QA.md`.
- Restored soundtrack correlation with source R3 is 0.998099, stable across early, middle and final-sentence windows. Source insertion is +0.2894375 seconds. Thus the last word falls around 7.789–8.129 seconds in the output, not the unshifted source time. The final half-second is silent. This is audio-placement evidence, not a perceptual mouth-sync verdict.
- The restored mouth is parted at 8.25 seconds, about 0.12 seconds after the transcribed final word; it is closed/settled at 8.75 and 9.0 seconds. Do not infer continuing silent speech from one parted-lips frame.
- The phone delivery uses a lossless video-first remux with fast-start layout on CloudFront. Both decoded video and audio hashes match the raw Sync result, including its soundtrack placement. Hosted readback is byte-identical and byte-range requests return HTTP 206.
- Desktop browser playback reached the end at 9.042 seconds, with no media error and a full-height 405 by 720 portrait player. The route matches the previous phone delivery that the owner confirmed works. Current owner iPhone playback and subjective expressivity still await review.

No new-take owner acceptance is recorded. Canonical avatar, narration and publication states are unchanged.
