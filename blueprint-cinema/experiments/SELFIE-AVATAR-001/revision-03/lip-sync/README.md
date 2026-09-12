# Revision 03 voice restoration

Fresh runner for the new 9-second home/olive performance from Higgsfield job `904f7c14-ab23-4605-b586-6c8b8ad76a84`. It uses only the new 8.173416667-second R3 Original C WAV, hash-pinned in `INPUT.json`. No earlier navy test, voice-B audio, or previous submission intent is reused.

`restore.py` permits one new `fal-ai/sync-lipsync/v3` submission with `sync_mode: silence`. It checks local and hosted source hashes, writes the intent exclusively before POST, refuses duplicate intents, restricts credential requests to `queue.fal.run`, and blocks authentication redirects. Uncertain submissions must be inspected rather than repeated.

The untouched returned video is saved as `media/revision-03/home-olive-r3-sync.mp4`. Root or the native-QA agent owns `home-olive-r3-native.mp4`; root owns any video-first remux and mobile hosting. This task will not duplicate that upload.

Completion checks cover the new R3 waveform over early, middle and final-sentence windows, exact dimensions/frame count/duration, and strict full decoding. Those checks do not establish perceptual lip-sync quality, face naturalness or the success of the expressive direction; actual viewing and listening remain necessary.

Completed with one fresh request, `01a09748-dff7-7381-84c3-6f63b8895cc9`; provider inference time was 118.525 seconds. The result is retained at `https://v3b.fal.media/files/b/0aaa2bb0/t8p6hnMujcIPY4f7IOJs9_TzGBxEDO.mp4` and downloaded byte-for-byte to the planned local media path (9,962,885 bytes; SHA-256 `c776baa1a2b514805374f1f3aed5eb48fa8d8127da3f9dfe80987e6278252942`). Actual billed cost was not returned in the completion receipt.

The returned picture preserves 720 × 1280, 24 fps, 217 decoded frames, and 9.041667 seconds of video duration. Strict full decoding passed. `MEDIA-QA.json` records these checks against the native input.

The restored soundtrack matches the new R3 source with aligned correlation 0.998099; early, middle and final-sentence correlations remain 0.99748, 0.99836 and 0.99812. The provider places the original waveform approximately 0.2894375 seconds into the result. Keep that placement when remuxing: it is soundtrack insertion, not a measured audiovisual sync error. The full source remains present, with silence in the final half-second. The independently transcribed source final word (7.50–7.84 seconds) consequently falls at approximately 7.789–8.129 seconds in the restored video. The analysis resamples to 16 kHz, so its 8.1734375-second reference length differs by rounding from the original WAV's 8.173416667 seconds.

The native soundtrack has only 0.06266 aligned correlation with the source, so its fitted lag cannot reliably establish speech timing. `RESTORED-AUDIO-QA.json` and `NATIVE-AUDIO-QA.json` preserve the measurements. No perceptual listening or facial-performance approval is asserted by this audio worker.
