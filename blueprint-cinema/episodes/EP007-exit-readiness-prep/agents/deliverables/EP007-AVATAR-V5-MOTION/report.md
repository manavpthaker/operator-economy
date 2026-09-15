# EP007 avatar V5 gesture review

Work order: EP007-AVATAR-V5-MOTION. Episode: EP007-exit-readiness-prep. Reviewer: performance reviewer, agent rebecca_reference. Date: 2026-09-11.

**The request for meaningful hand movement is visibly fulfilled.** V5 has early, middle, and question-period gestures with genuine returns to rest. No obvious hand-anatomy or identity failure was found in the inspected frames. The main craft concern is the sustained, somewhat repetitive middle passage; more movement is established, but greater overall naturalness still requires playback with the selected voice.

## Inputs

- V5 native: `blueprint-cinema/experiments/EP007-PRESENTER-001/avatar-v5-gestures/media/generated-native.mp4`; SHA-256 `83370157093045564bc0212884f5f6ec3d0e42444f9c39975767c429858a471d`. Hash matches. Probe: HEVC 1920 × 1080, yuv420p10le, 24 fps, 505 frames, video 21.041667 seconds, container 21.050000 seconds, AAC audio.
- Prior V4 review: `blueprint-cinema/episodes/EP007-exit-readiness-prep/agents/deliverables/EP007-AVATAR-V4-MOTION/report.md`; SHA-256 `1a2cd2d7c49f7ce5a23190ceb4d117bbc3f780db1c8902a7d21ce87500b5f19f`. It records V4's isolated hand action around 11.50–13.25 seconds.

## Observed native-source timing

Times are sampled boundaries, not exact onset measurements. Left/right refer to the image.

| Interval | Observed movement or rest |
|---|---|
| 0.00–0.50 | Both hands resting. |
| 0.75–2.00 | Both hands rise into a modest open gesture, then lower; resting by 2.25. |
| 2.25–3.00 | Both hands resting. |
| 3.25–5.25 | Another two-hand phrase with palms facing roughly inward; resting by 5.50. |
| 5.50–6.50 | Both hands resting in the overview samples. |
| By 7.00–12.75 | Screen-left hand leads, then both hands remain active through several inward/outward and palm-presentation beats. Both return to rest by 13.00. Exact onset lies between the 6.50 rest sample and 7.00 active sample. |
| 13.00–17.25 | Both hands resting in the available samples. |
| 17.50–19.25 | Screen-left hand lifts and rotates palm-up/inward while the other remains resting; lowered to the table by 19.50. This is the late/question-period gesture, not a verified word-level alignment claim. |
| 19.50–21.00 | Both hands resting; final sampled face is settled with closed lips. |

## Anatomy, repetition and face

Visible fingers/thumbs keep plausible structure through the inspected lifts and rotations. Wrists remain attached to the forearms, and returns to the table read as coherent contact. No obvious duplicated/fused finger, broken wrist, or table penetration appears. Occlusion and sampling gaps prevent exhaustive anatomical certification.

**Observation for performance review:** the early two-hand phrases use similar upright, inward-facing palms. The middle approximately 7–12.75-second passage contains repeated related beats without a complete rest. This could read as rehearsed presenter emphasis when played at speed. It is not continuous waving across the whole take, and it is not an established blocking defect from frames alone. If the owner finds it too busy, the narrow adjustment is one genuine rest within this middle passage; do not reduce V5 back to V4's single gesture merely to solve that concern.

The face/head samples retain consistent identity, glasses, hair and wardrobe. Small head-angle, eyebrow and eyelid changes occur; no large posture excursion or obvious identity discontinuity appears in the sampled pass. Brief tooth visibility is present during articulation. Smoothness, micro-expression rhythm and exact lip synchronization were not judged from stills.

## Evidence and limits

Five FFmpeg contact sheets were displayed through `view_image`. All frames were selected directly from source frame numbers without interpolation. Sheets read left to right, top to bottom; blank trailing cells are padding.

- `overview-0s-to-21s-every-half-second.jpg`: whole take, 0–21 seconds every 0.5 seconds.
- `hands-0_5s-to-5_5s-quarter-second.jpg`: 0.5–5.5 seconds every 0.25 seconds.
- `hands-7s-to-13s-quarter-second.jpg`: 7–13 seconds every 0.25 seconds.
- `hands-17s-to-19_75s-quarter-second.jpg`: 17–19.75 seconds every 0.25 seconds.
- `face-0s-to-21s-every-second.jpg`: 0–21 seconds every second.

Coverage is 71 distinct source frames out of 505. Some sheets were resized for display. No audio was listened to; the native generated voice is not selected. The restored source was not reviewed here. This report supports showing the already authorized restored result for performance evaluation; it does not claim full audiovisual review, improved naturalness, owner acceptance, or production approval.
