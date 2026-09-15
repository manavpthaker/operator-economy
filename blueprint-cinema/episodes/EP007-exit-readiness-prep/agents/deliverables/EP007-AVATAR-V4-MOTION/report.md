# EP007 avatar V4 native and restored motion review

Work order: EP007-AVATAR-V4-MOTION. Episode: EP007-exit-readiness-prep. Reviewer: visual motion reviewer, agent rebecca_reference. Review date: 2026-09-11.

**No blocking visual defect was found in the sampled native frames.** The face remains consistent with the wider still. The visible hand gesture has plausible anatomy and returns to a resting pose. This is a sampled visual review, not full audiovisual playback or a lip-sync verdict.

## Bound inputs

- Native video: `blueprint-cinema/experiments/EP007-PRESENTER-001/avatar-v4-wide/media/generated-native.mp4`; SHA-256 `74ea3bebd95321a39e7a6f1620574886ffe1f90964650096970375bf51ff273c`.
- Wider still: `blueprint-cinema/experiments/EP007-PRESENTER-001/avatar-v4-wide/media/wide-study-reference.png`; SHA-256 `5c282925447ff8227ea66dcafa60e5b9cf5913aa5cbb565037fb4e0a2d1cbb82`.

Both match the assigned inputs. `ffprobe` reports HEVC, 1920 × 1080, 24 fps, 505 video frames, yuv420p10le, video duration 21.041667 seconds, AAC audio, and container duration 21.050000 seconds. Source frame 504 is at 21.000 seconds.

## Observations

| Area | Direct evidence | Disposition |
|---|---|---|
| Identity | Hair, glasses, facial proportions, short facial hair, navy shirt, and study remain coherent across the face samples from 0–21 seconds. Head angle and eyelids change without an obvious identity discontinuity. | No sampled blocker. |
| Hands and wrists | In the 11–15-second closeups, the hand at screen-right retains plausible finger/thumb structure and wrist connection through lifting, rotating, and lowering. The other hand remains near its starting rest position. No obvious fused/extra digit or detached wrist appears. | No sampled blocker; partly occluded digits limit anatomical certainty. |
| Gesture and settling | Rest at 11.00–11.25; clear lift by 11.50; lowered near the tabletop at 12.50; smaller follow-up lift at 12.75–13.00; resting again by 13.25. Subsequent sampled frames show both hands resting. | The movement resolves rather than continuing as an unending gesture. |
| Table contact | Returning fingertips, hand silhouette, and contact shadow read coherently in the sampled 12.50 and 13.25–15.00 frames. No obvious penetration through the table is visible. | No sampled blocker; contact between sampled frames was not inspected exhaustively. |
| Mouth shapes | Open, rounded, teeth-visible, and closed configurations occur across the face sheets. No obvious detached lips, duplicated mouth, or severe mouth-shape discontinuity is visible in these samples. | Shape observation only. Phoneme accuracy and restored-audio synchronization remain unverified. |
| Ending | The mouth is active at 20.00, then closes in the samples from approximately 20.25 through the final frame at 21.00. Both hands remain on the table and the ending image is intact. | A settled ending is visible; no audio-tail or final-word alignment claim. |

## Sampling evidence

Contact sheets read left to right, top to bottom. Empty trailing cells are padding, not missing video frames.

- `overview-every-1s-and-end.jpg`: full frame, frames 0, 24, …, 504; times 0, 1, …, 21 seconds.
- `face-00s-to-07s-every-half-second.jpg`: face crop, 0–7 seconds inclusive at 0.5-second intervals.
- `face-07_5s-to-14_5s-every-half-second.jpg`: face crop, 7.5–14.5 seconds inclusive at 0.5-second intervals.
- `face-15s-to-21s-every-half-second.jpg`: face crop, 15–21 seconds inclusive at 0.5-second intervals.
- `hands-11s-to-15s-every-quarter-second.jpg`: both forearms/hands/table crop, 11–15 seconds inclusive at 0.25-second intervals.
- `ending-20s-to-21s-every-eighth-second.jpg`: full frame, 20–21 seconds inclusive at 0.125-second intervals.

These sheets cover 57 distinct source frames out of 505. FFmpeg selected source-frame numbers directly; no interpolation was used. Image-only contact sheets and analysis crops were displayed using `view_image`. Color management was not calibrated, and some sheets were resized by the tool for display.

## Native-pass limits

No audio was listened to. Short defects between sampled frames, motion smoothness at playback speed, eye-movement rhythm, exact articulation, and naturalness against the restored narration are not established by this review. The restored video was unavailable at native-pass completion; the follow-on review below covers the subsequently supplied restored source. The final closer crop also requires its own framing check against the actual output.

Recommendation to the orchestrator: no sampled native defect requires another generation on this evidence. Continue the already authorized restoration and final audiovisual review. This is not a production approval, a release verdict, or an attempt to revise the accepted V3 identity.

Only this report, its contact sheets, and its deliverable manifest were produced inside the assigned directory. No source media, canonical file, approval, UI, provider, or paid service was changed.

## Follow-on: restored source

The orchestrator subsequently supplied `blueprint-cinema/experiments/EP007-PRESENTER-001/avatar-v4-wide/media/generated-original-audio.mp4`, SHA-256 `19f57219ec8a75fe49880c560ad556006699e79ec4a2b9884ed5bae20f215f02`. The hash matches. Local probe confirms H.264, 1920 × 1080, 24 fps, 505 frames, yuv420p10le, video duration 21.041667 seconds, AAC audio, and container duration 21.042000 seconds.

**No blocking visual regression was found in the selective restored/native comparison.** Hands, wrist connections, table contact, hair, glasses, face identity, and broad pose remain visually coherent in the compared frames. Restoration changes visible mouth shapes and some eye details; it must not be described as picture-identical audio muxing.

- At 17.00 seconds both sources show a closed mouth. At 17.25 the restored lips are slightly parted while native is closed. At 17.50, 17.75, and 18.00, mouth configurations are active in both sources. These frames do not establish a continuous 17–18-second silent pause. A silence/articulation judgment requires the actual approved-audio boundaries.
- At 20.25 the restored lips remain slightly parted while native is closed. By 20.50, and at 20.75 and 21.00, the restored mouth is closed. The final restored image retains the settled pose and table contact.
- The selected hand comparisons show no obvious restoration-induced change in anatomy or gesture trajectory. No further dense hand sampling was warranted by those pairs.

The paired contact sheets place **native on the left and restored on the right within each pair**. Pairs read left to right, top to bottom:

- `native-left-restored-right-face-comparison.jpg`: 0.00, 2.50, 7.00, 12.00, 13.50, 15.50, 17.00, 17.25, 17.50, 17.75, 18.00, 20.25, 20.50, 20.75, 21.00 seconds.
- `native-left-restored-right-hand-comparison.jpg`: 0.00, 11.50, 12.00, 13.00, 13.25, 20.75 seconds.

This adds two previously uninspected native frame times and covers 18 distinct restored frames. Across both passes, 59 distinct native frames were inspected. The orchestrator separately reports full-audio correlation 0.998346 with a +0.04725-second insertion and a successful full decode. Those are supplied technical results, not independently repeated here, and correlation does not measure mouth-to-phoneme synchronization.

Final disposition: no sampled visual finding requires another source generation. Full audiovisual playback, the approved-audio pause relationship, exact synchronization, and the rendered closer crop remain outside this frame-review verdict. Review is complete for the assigned native/restored visual scope; no production approval is claimed.
