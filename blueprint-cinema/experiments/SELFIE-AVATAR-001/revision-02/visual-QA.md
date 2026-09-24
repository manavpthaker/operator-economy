# Home olive revision: native visual QA

Reviewer: `avatar_sources`, independent visual sampling. Date: 2026-09-12.

**Result: the sampled native frames preserve the requested olive overshirt/off-white T-shirt, visible appearance, home setting, and close selfie composition. No material visual defect was observed in these samples. This supports proceeding to review the restored output; it is not a playback, lip-sync, naturalness, or owner-acceptance verdict.**

## Artifact and method

- Higgsfield job: `4ca5df2c-61f8-42b5-8c2c-f3be896622ab`.
- Native file: `../media/revision-02/home-olive-native.mp4`.
- Native SHA-256: `a8a2a506dff0df23ebc6d2bb3fc822f1002aeff5da9047452df5b630480faafe`.
- Probe: H.264, 720 × 1280, 24 fps, 241 picture frames, 10.041667 seconds. Native AAC duration: 9.952 seconds. Native audio was not listened to in this review.
- Full-file FFmpeg decode completed without reported errors.
- Reviewed 12 labeled native frame samples at 0, 0.5, 1, 2, 3, 4, 5, 6, 7, 8, 9, and 10 seconds through `view_image`.
- Compared the exact original home frame, edited olive reference, and native frame 0 side by side at equal image dimensions.
- Evidence: `../media/revision-02/visual-qa-contact.jpg`, `../media/revision-02/visual-qa-comparison.jpg`, `../media/revision-02/visual-qa-samples.json`, and `video/NATIVE-DOWNLOAD.json`.

## Observations

| Check | Observed result |
|---|---|
| Wardrobe | Muted olive open overshirt over off-white crew-neck remains present in all samples. Collar, opening, buttons, pocket and fabric remain visually coherent at inspected scale. |
| Face, hair and glasses | Facial features, short dark hairstyle, stubble and clear glasses remain visually consistent with the supplied reference across sampled expressions. No gross facial or glasses deformation observed. This is visual similarity assessment, not identity verification. |
| Room and lighting | Window/curtain stays at frame left; pale wall, wood shelves and books stay at frame right. Soft daylight direction is consistent. |
| Selfie framing | Near-lens close composition and supporting arm at the lower-left edge remain plausible for a handheld phone. The native result has slight framing/background-placement variation from the exact still, including somewhat different shelf alignment and visible couch area. This does not change the setting or the basic composition. |
| Hands | Complete hands and fingers are outside the sampled crop. No exposed limb deformation observed; hand/finger anatomy cannot be certified. |
| Beginning and ending | Initial frame is a speaking expression; final samples show a closed-mouth settled expression. Static samples do not establish whether the ending hold or movement feels natural. |

The slight shelf/couch placement variation is an **observation**, not a requested correction. No blocking or major visual finding is supported by these samples.

## Reference pins

- Exact olive reference: `../media/revision-02/olive-reference.png`, SHA-256 `f407e60b8f132931c70e103f761a7e336045d8244be2e7264f19a165d0715cb0`.
- Selected home source frame: `../media/revision-02/home-source-frame.png`, SHA-256 `2432d1e82102c2e33ddddd57c1dd3ee9286da8c03f9b3eaa837689288a640eb5`.
- Selected home native video: `../media/native-home.mp4`, SHA-256 `57fb3a6213d94aa8efd886e9cc45801d53325df64f885c7d583645994ef63d2f`.

## Limits

This review covers isolated displayed frames and a technical decode. It does not establish whole-clip movement, momentary defects between samples, perceptual mouth synchronization, voice identity, audible quality, or casual delivery. Any Fal-restored output requires its own inspection because restoration may alter the face. No generation, canonical episode mutation, approval-state change, commit, or publication was performed by this reviewer.

## Restored output follow-up

Reviewed 2026-09-12. File: `../media/revision-02/home-olive-voice-b-sync.mp4`; size 10,785,661 bytes; SHA-256 `d5e4e908ad7e6a134f3d2f5fd3afb178853a71fa6ee9cb345cb5de28c9197b8e`. Probe retains 720 × 1280, 24 fps, 241 frames and 10.041667 seconds of picture.

Compared restored samples at 0.5, 4.5, 8.9 and 9.5 seconds with native samples at the same requested times. Evidence: `../media/revision-02/visual-qa-restored-contact.jpg` (native top row, restored bottom row), SHA-256 `6e7f73a46098b3e7cd79bffcf423e0050ec5686fc50759e5982b16571262b062`.

**No new gross visual defect is visible in these four restored samples.** Wardrobe, glasses, hair, supporting arm, window/shelves, framing and lighting remain visually stable relative to the native output. Mouth and lower-face shapes change, as expected from restoration; no obvious facial seam or gross deformation appears at inspected scale. In the later samples the restored mouth is slightly open where the native mouth was closed. Whether that movement matches the new words and final silence requires audible moving playback and is not decided by this frame comparison. Complete hands remain outside the crop.

This follow-up only inspects the displayed frames. It does not establish temporal stability between them, perceptual lip synchronization, voice quality, or owner acceptance.
