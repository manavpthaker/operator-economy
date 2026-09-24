# R4: original video look control

The owner authorized inspection of the original recording/motion reference and a test of the original video look with the same two-sentence narration. This follows rejected generated study-look performance: the mouth is timed plausibly but does not look natural. It does not establish that the owner's original acting is faulty.

## Verified source and limits

The signed-in avatar group `cc6abe9744e74df7a103b7a37262d2f7` shows one video look (`brown Man`) and three generated photo looks. Selecting the original video look through “Use in a video” produced an AI Studio URL with `defaultLookId=b495d299cea544608fc2fc249d055b87`.

The original-look preview is a provider-processed 37.401-second file, not verified raw training footage. It is archived as `../media/repair-r4/original-look-provider-preview.mp4`, SHA-256 `3107b4f8f26fb3fd2bb3f9121bd236d21ef555e4c1300177c9149e930097defe`. The observed asset is `https://resource2.heygen.ai/avatar/v3/b495d299cea544608fc2fc249d055b87/half/2.2/preview_video_target.mp4`. Technical inspection: 720×1280, 30fps, 1122 frames, H.264, AAC48k stereo; full decode passes. Metadata shows processing, without camera or source-provenance information. The preview UI displays a HeyGen watermark; that does not establish the file's raw-versus-generated provenance. The original uploaded recording's local location was requested from the owner and remains unknown.

AI Studio's Avatar V advanced panel exposes More expressive motion and custom-motion controls; no separate motion-reference selector is visible. The original video look is explicitly selected, but the provider's internal reference selection is not independently observable. Do not imply that the motion-reference ID used in earlier A/B/C runs was verified.

## Comparison

Matched A's Avatar V model, exact 5.600-second WAV, More Expressive off, Voice Mirroring off, landscape1080p, Single Scene entry point, and motion prompt. Original look ID was verified again from the selected Quick create thumbnail path. The final settings were read back immediately before Generate. The returned video retains the original portrait, centered on a white 1920×1080 canvas. This is a diagnostic source/look comparison, not a finished presenter composition.

Exactly one generation was submitted: [Test D](https://app.heygen.com/videos/31e481cc4f3f445ca92a2591504d5a31). AI Studio draft `6f08266bdc404521b8f29cd0c294e099` was used only to inspect advanced controls. A browser disconnection left a draft-editor lock; no audio was attached or generation submitted there. Its centered portrait framing is not evidence of the eventual Single Scene output.

Prompt: **Calm, candid delivery with restrained facial movement and relaxed eyebrows. Steady eye contact with the camera. Hands remain still below frame.**

Audio: `../media/repair-r2/scope-two-sentences.wav`, SHA-256 `c565f1dfe8c218f156e9d0b76d0515a264be26cc1d0cea7d1ea8977a3c565566`; full source lock and word IDs in `../repair-r2/input-manifest.json`.

Confounds: original versus generated appearance, pose, framing/face scale, video-look versus photo-look conditioning, and generation variability. Better performance supports a look/reference effect but does not isolate one cause. Worse performance does not prove the owner's raw recording was poor. Full playback is needed; sampled frames and waveform correlation do not establish a performance pass.

No narration, separate film work, episode approval, or production gate is changed. Generation/provenance status is recorded in `status.json`.

## Returned result

Test D is archived as `../media/repair-r4/test-d-original-video-look-1080p.mp4`, SHA-256 `242a562c45f4ccb004eed9ec838889db30cec66afb7923f40ead8e3c34d41bec`. Title was verified on the provider result page. Full decode passes; 1920×1080, 25fps, 139 frames, 5.560s picture and 5.591s audio/container. Returned audio has the same +23.021ms delay and 0.999428 aligned correlation measured in A/B/C. Independent sentence delays agree; the last word is covered. These audio checks do not prove visual synchronization.

Exact 200ms frame samples show a broad mouth opening at 3.2–3.6s. Returned audio is very quiet across that interval (RMS −64.96dBFS, roughly 48dB below adjacent speech). Audio rises within 3.8–3.9s, earlier than the transcript-derived onset; the quiet-interval observation is limited to 3.2–3.6s. This remains a visible performance concern, although samples alone cannot exclude breathing or anticipation. The original look has not established a solution to the owner's complaint, and the raw recording has not been assessed. Do not recommend rerecording based on this output alone. Full owner playback review remains pending. Detailed technical evidence is in `technical-review.json`.
