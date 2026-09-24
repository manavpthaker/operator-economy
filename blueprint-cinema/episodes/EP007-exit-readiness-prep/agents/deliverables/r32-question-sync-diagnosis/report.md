# R32 question: timing and local-playback diagnosis

2026-09-11. Independent bounded QA of the issued R31 question. No production edit, provider call or approval.

**Finding:** no measured audio drift, erroneous source offset, irregular frame timestamps or repeated speech frames explains the complaint. This does not establish perceptually correct lip sync. Generated articulation and browser playback remain distinct possibilities; the local comparison is ready to distinguish them.

Play [question-local-r31-original-audio.mp4](question-local-r31-original-audio.mp4) locally in QuickTime at normal speed. It is 2.16 MB, 1280×720 H.264 with lossless ALAC narration, 307 frames at 24 fps, 12.791667 seconds. The decoded audio is sample-for-sample identical to the original master, and to the same interval of R31's actual narration track. ALAC preserves this exactness; browser audio support was not tested. SHA-256: `6a6c96c3481603781f6b98bcd17c7f6295da069fe6b77116e5055bcb4be2cb60`.

## Measured findings

- All seven issued input hashes match. Restored source, selected browser clip and standalone file fully decode without errors.
- R31 starts the question at review 131 / master 134 seconds, using restored source frame 8. Independent early, middle and late audio windows each place the source waveform at **0.3333125 seconds**. The eight-frame selection is 0.333333333 seconds: a difference of only 20.8 microseconds. Aligned correlations are 0.99718, 0.99812 and 0.99884; these measure waveform placement only.
- The restored source and selected browser clip have uninterrupted 24 fps timestamps. Their best sampled picture match is at zero frame displacement, with appreciably worse matches at ±1 and ±2 frames. No unexpected near-static frame run appears during the spoken interval. Frame uniqueness cannot certify natural motion or exclude local animation jitter.
- The only sustained near-static run is the documented **18-frame ending hold**, beginning at local 12.041667 seconds after the spoken picture. Compression causes tiny differences between its decoded frames. It cannot account for a mid-sentence interruption.
- One video element continues through the close crop at local 8.958333 seconds. The standalone preserves that same frame transition and ending hold. Its integer-pixel crop approximates the CSS geometry within one output pixel; timing is unchanged. No browser/network trace was collected, so connection trouble is not established.

## Sampled mouth evidence and limits

The face visibly closes and reopens its lips; it is not one fixed teeth-visible pose. In the enlarged samples, closure appears at local 4.375 near “professional,” at 6.833 within the first “paid,” at 9.958 before the second “paid,” and at 10.667–10.750 before “make.” These positions do **not** support one consistent global picture shift. Word-level transcript boundaries are not precise phoneme boundaries, and these samples cannot determine whether transitions sound convincingly matched at normal speed. Uneven generated articulation remains possible.

The restored endpoint is quiet: lips are gently closed in the samples at local 12 seconds and throughout the final hold. The earlier concern about the native question endpoint does not apply to this restored result. The exact accepted interval reaches master 146.791667, 11.667 ms past the transcript onset of the next “Nobody”; this inherited boundary is preserved, not newly extended.

**Next test:** if the same mouth mismatch remains in the local file, it is present in the selected audiovisual pairing and cannot be blamed solely on streaming. If local playback is smooth while the browser stutters, investigate browser delivery, decoding and scheduling. Neither result justifies an arbitrary frame shift without a consistent measured perceptual offset. Root owns the separate request for a more pensive performance.

Evidence: [early visemes](question-viseme-early.jpg), [late visemes](question-viseme-late.jpg), [pause/end](question-pause-end.jpg), [export crop/end](standalone-crop-and-end.jpg), [full metrics and exact pins](evidence.json). No uninterrupted audiovisual playback verdict or owner acceptance is claimed.
