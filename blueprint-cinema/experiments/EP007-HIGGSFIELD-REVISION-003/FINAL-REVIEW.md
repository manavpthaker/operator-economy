# EP007 revised opening test

[Watch the finished 59.87-second review video](review-media/ep007-revised-higgsfield-hyperframes-test.mp4).

The full opening test was revised. The meeting now follows two people reviewing an open folder: a shared wide view, a paperwork insert during the buyer's question, and a two-shot through the owner's answer and pause. The wider presenter adds modest head motion and low hand gestures. The Working Model animation, show identity, narration words and audio timing are unchanged.

## Selected output

- Native HyperFrames 0.8.31 high-quality export, 1280 × 720, 30 fps, 1,796 frames, 59.866667 seconds, 35,741,066 bytes.
- SHA-256: `cdd0effd6d5969c522d62015bbb1351e10533ab28d71303682a827ce86afc7d8`.
- Higgsfield video jobs 202, 203, 204 and avatar retry 205. The first avatar take, 201, remains rejected for missing visible opening articulation.
- This revision used 98 Higgsfield credits, including the rejected avatar take. No further generation was needed for the export corrections.

## Verification

The corrected source passed HyperFrames checks. Full encoded video/audio decode passed. Exact outgoing/incoming frames at all four cuts and final frame 1795 were inspected independently and by the lead. The four blank boundary frames in the initial export are fixed by extending outgoing coverage beneath the unchanged wrapper cuts. The selected native export contains no post-render frame cloning.

All seven animation files and the source narration WAV remain byte-identical to experiment 002. The final AAC packets match the prior reference-verified export exactly; that analysis measured zero timing shift and 0.999825 waveform correlation. See `generated/export-audio-review.json`, `generated/preserved-elements-review.json` and `review-media/independent-native-verification.json`.

The selected file also completed browser playback at normal speed with audio enabled, reaching 59.866667 seconds and retaining the final presenter picture. Playback completion and sampled frame inspection do not certify every lip movement against its phoneme.

## Remaining performance limits

The owner settles her answer roughly one second earlier than directed; her later lips are slightly parted in a quiet hold. The buyer keeps a soft gaze toward her more than requested. The avatar visibly articulates both sentences and uses restrained motion, but sampled articulation does not establish perfect phoneme synchronization.

This is a private review cut of the opening, not completion or release approval of the full episode. The prior failed export and temporary repaired fallback remain preserved as historical evidence. This file and `GENERATION-RUN.json` identify the current selected result.
