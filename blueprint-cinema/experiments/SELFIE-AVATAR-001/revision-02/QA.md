# Revision 02 review

## Scope and source

- Owner chose the home selfie and a muted olive casual overshirt. This is a separate private test; it does not replace the accepted EP007 avatar or narration.
- The wardrobe still was edited from an actual frame of the selected home video. Its hosted bytes match the local generated image (see `reference/FAL-UPLOAD-READBACK.json`).
- The native motion request combines that exact wardrobe image, the selected home video, and current voice B. Its receipt is `video/SUBMISSION.json`.

## Voice selection

- Both auditions use the existing Algieba guide to Original C identity-transfer route with unchanged transfer settings. Only performance direction changes.
- B was selected for this video because its direction emphasizes more pitch/pace variation and its verified final word has a quiet ending. This is not a claim that a listening comparison established B as more natural.
- Independent ASR of transferred B verifies all 23 source words. The final word ends near 9.62 seconds within the 9.984583-second source. Speech was not accelerated, stretched, or cut to fit the old video.
- The alternative A is retained separately and carries a possible abrupt-ending caution. It is not used in the finished video.

## Completion checks

- A single fresh Sync v3 request completed after the owner's balance top-up. The final file is `../media/revision-02/home-olive-voice-b-sync.mp4`; its SHA-256 is `d5e4e908ad7e6a134f3d2f5fd3afb178853a71fa6ee9cb345cb5de28c9197b8e`.
- Native and final picture both measure 720 by 1280, 24 fps, 241 frames, and 10.041667 seconds. Strict full decoding passed.
- The final soundtrack matches source B with 0.998316 aligned waveform correlation, with stable early, middle, and final-sentence matches. Its approximately 19 ms insertion offset is a soundtrack measurement, not a perceptual mouth-sync verdict. See `lip-sync/RESTORED-AUDIO-QA.json`.
- Native and restored frame samples preserve the olive/off-white outfit, glasses, hair, home setting, lighting, and close selfie composition. No gross visual defect was observed in the samples; see `visual-QA.md` for scope and minor background variation.
- The local comparison page loaded both videos and both auditions with `readyState=4`, correct dimensions/durations, and no media error. The in-app browser crashed on the playback-control click, so normal-speed playback was not verified there. Direct MP4 and local file links are supplied; QuickTime control also timed out. No audible-quality or perceptual naturalness claim follows from the technical checks.

Normal-speed human review is still needed for delivery, likeness, and perceptual mouth sync. No owner acceptance of this new take is recorded.
