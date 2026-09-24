# EP009 r2 graphics-only draft: encoded integration check

Result: technical checks passed; the three replacement graphic plates are present at their planned frames. No new integration defect was observed in the inspected frames. This is an agent recommendation, not owner acceptance or a delivery-master verdict.

Artifact: [ep009-full-r2-graphics-only-draft.mp4](qa/ep009-full-r2-graphics-only-draft.mp4). SHA256: `9b279403e6b2c1ef365d086110b8be5b2621315cb98af6e07b257740601857e3`.

## Technical evidence

- [Full verification](VERIFICATION-r2-graphics-only-draft.json): every encoded video frame decoded successfully; 29,607 frames, 1233.625 s, 1280x720, 24 fps, stereo 48 kHz. Source and output hashes match the build manifest.
- No unplanned uniform frames. The existing one-frame navy sting entry at frame 1427 is the sole recorded exception.
- The complete locked narration matches at zero lag: minimum voiced-window correlation 0.999978, maximum absolute window RMS difference 0.00923 dB. Full-length correlation is 0.999988 in both channels. The decoded tail after the master is effectively silent.
- Measured output: -19.5 LUFS integrated, 3.7 LU loudness range, -5.6 dBTP. This check applies no normalization and does not approve the final mix.

## Encoded-frame inspection

[Frame inventory and source comparisons](qa/r2-graphics-integration/FRAME-COMPARISON.json) retain 103 unique frames selected by exact index from the encoded full cut. They cover every recorded replacement-scene cue, both sides of all nine boundaries touching the six changed segments, and all 34 frames spanning the two repaired S17 text append transitions. All 13 generated contact sheets were visually inspected.

| Area | Encoded observation | Evidence |
|---|---|---|
| S00, seg004 to seg006 | The columned booking-site drawing is present in the cold-open model. The reservation card, return path, two tags and labels remain in their intended positions. The internal seg004/005 and seg005/006 boundaries carry the same scene state. | [Cue sheet 1](qa/r2-graphics-integration/seg004__seg006-01.jpg), [cue sheet 2](qa/r2-graphics-integration/seg004__seg006-02.jpg) |
| S05, seg020 | The same columned booking-site drawing remains readable above the booking timeline. The empty job position and later tag remain unobscured. | [Cue sheet 1](qa/r2-graphics-integration/seg020-01.jpg), [cue sheet 2](qa/r2-graphics-integration/seg020-02.jpg) |
| S17, seg057/058 | The fixed prefix stays in place while the hours and audit phrases appear to its right. No overlapping old/new phrase or horizontal prefix jump is visible in the inspected transition frames. The model caveat and later economics cards remain present. | [Eight-hour append](qa/r2-graphics-integration/transition-eight-01.jpg), [audit-hours append](qa/r2-graphics-integration/transition-twelve-01.jpg), [later cue sheet](qa/r2-graphics-integration/seg057__seg058-04.jpg) |
| Entry, internal and exit boundaries | The replacement clips begin/end on the mapped source frames. Following unchanged seg007, seg021 and seg059 appear on frames 872, 5429 and 23437 respectively. No blank, displaced picture or missing following shot is visible at these inspected boundaries. | [Boundaries 1](qa/r2-graphics-integration/boundaries-01.jpg), [boundaries 2](qa/r2-graphics-integration/boundaries-02.jpg), [boundaries 3](qa/r2-graphics-integration/boundaries-03.jpg) |

Each inspected encoded frame was also compared with its exact mapped source frame. Maximum mean absolute RGB difference was 1.584/255; the largest fraction of pixels with mean channel difference above 20 was 0.00456%. These are small re-encode differences consistent with the inspected images, not a claim of lossless identity.

## Method and limits

Run with the retained syncenv Python: `_tools/verify_r2.py BUILD-r2-graphics-only-draft.json`, followed by `_tools/inspect_r2_frames.py`. The extraction script records the full-cut hash, source path, source frame, output frame, cue label and comparison metric for each retained frame. It refuses to overwrite existing evidence.

This inspection supports carrying B-26 and B-R1-01's graphic repairs into the assembled review draft. It does not clear unrelated findings or certify comprehension at playback speed. No normal-speed audiovisual watch-through, audio listening assessment, mouth-sync judgment, or owner review occurred. All 15 presenter segments in this graphics-only draft remain the r1 versions; the regeneration batch is not represented here. Publication and canonical episode gates remain unchanged.
