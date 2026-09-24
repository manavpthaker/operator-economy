# V5 question native-performance review

Reviewed 2026-09-11 as independent QA reviewer under `avatar-v5-question-output-review`. **No blocking identity, framing, anatomy, or decode defect was observed in the inspected samples.** The native take is suitable to continue through root's original-audio restoration and review. This is not owner acceptance or a final lip-sync verdict.

## Artifact and comparison

- New question: `r31-avatar-v5-wide/provider/v5-question/native.mp4`, SHA-256 `62872b9d467b6b6591cea5e37ce93fb4387e77b26efd3675ba3877690e0475cd`.
- Accepted V5 comparison: `avatar-v5-gestures/media/gesture-review.mp4`, SHA-256 `b896fcd06c0b2b15dfd16dad18e80f9aa1971e916b5a9b06d52ee09874f3f918`.
- Every issued input hash matched, including V5 acceptance, native QA, and the exact question prompt. The accepted baseline's middle gesture and brief eye movement remain accepted; they were not reopened as defects or generalized into prohibitions.
- Native probe: **1920×1080, 313 frames at 24 fps, 13.041667 seconds, HEVC 10-bit, first PTS zero**. Full decoding passes without errors. Its regenerated AAC audio is 32 kHz stereo and is not the final original-narration track.

## Observations and findings

**Identity/framing — no material concern observed.** Compared with accepted V5, the question retains the recognizable face, glasses, navy shirt, table, daylit study, and wide seated composition. Forearms and complete hands stay within the inspected native frame. No unintended camera crop or conspicuous room/wardrobe transfer from the behavioral references appears.

**Hand anatomy and contact — no material concern observed.** The detailed samples show plausibly distinct curved fingers, ordinary wrist/elbow relationships, and credible tabletop contact. No obvious additional digit, fused palm, broken wrist, or object intersection appears. Motion blur and occlusion prevent certifying every finger in every frame.

**Gesture/rest — observation, owner: root playback review.** A compact two-hand explanatory gesture develops around 0.5–2 seconds and settles by approximately 3 seconds. Smaller paired lifts recur around 4.5–6.5, 7.5–8.5, and 10–11.5 seconds, with intervening tabletop rest. The rests are visible; this is not continuous waving. The later bilateral shape is similar across those bursts, so normal-speed viewing should check whether the repeated lifts feel conversational or beat-like. Sampled poses alone do not establish excessive rhythmic pumping, and no revision is requested solely because both hands participate.

**Face/body — no severe artifact observed.** Head-angle and brow changes remain modest, with recognizable face structure and ordinary blinks. No prolonged dramatic lean or stretched held grin is apparent across the sample series. The new words require different mouth activity from the accepted opening; mismatched mouth poses between these two passages are not a defect by themselves.

**Future outgoing hold — observation, owner: root restoration/conform.** By approximately source 12 seconds, both hands are back on the tabletop and the head/body provide a plausible quiet outgoing pose. The native mouth remains active in samples at 12.000, 12.250, and 12.500 seconds. Clearly closed lips first appear in the sampled endpoint at **12.750–13.000 seconds**. Therefore the native source does **not** establish a fully settled face hold at 12 seconds. Recheck the restored result around the actual outgoing cut; do not extend or retime the locked narration based on this native mouth activity.

## Evidence and review limits

Inspection environment: locally decoded FFmpeg frames displayed as JPEG contact sheets. Compared nine accepted-V5 positions, 29 native positions at 0.5-second spacing with denser endpoint sampling, and 15 enlarged hand positions. Evidence files are `accepted-v5-overview.jpg`, `question-early-middle.jpg`, `question-late-ending.jpg`, and `question-hand-detail.jpg`; exact sample times and hashes are in `evidence.json`.

This is a dense sequential-position review, not uninterrupted real-time audiovisual playback. It can expose anatomy, framing, action phases, and endpoint risks; it cannot prove natural movement between every sample or final synchronization. No waveform comparison against native regenerated speech was used to infer final timing.

Disposition: **native technical and sampled visual review complete; original-audio restoration, final endpoint, and full-motion performance review pending with root.** No provider action, spend, runtime edit, canonical change, or approval claim occurred.
