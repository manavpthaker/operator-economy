# EP007 V4 opening edit

Status: corrected review render complete; technical checks pass. Root retains ownership of phone playback and final perceptual/audio QA.

The isolated review retains the complete 505-frame opening at 1920×1080 / 24 fps. It stays wide through frame 428, then changes immediately to a 1.30× upper-anchored crop on frame 429 (17.875 seconds), held through frame 504. No narration, pause, picture time, or playback speed is changed. No captions, graphics, music, or audio fades are added.

The provider-restored source has corrupted final image rows. FFmpeg extraction confirms the defect is in the source itself. The wide view receives a minimal 1.004× top-anchored overscan to remove approximately four bottom pixels; the closer view remains 1.30×. This is a source-edge cleanup, not a decoder repair. The first export is retained under rejected-first-render/ with its reason.

Picture is sourced from root's verified 8-bit derivative (SHA256 4729bf2cc362e68ef62ea5d095cd5fbe9e94521d35b862f19588c98f58083494), staged locally before root made further derivatives. The original restored authority remains SHA256 19f57219ec8a75fe49880c560ad556006699e79ec4a2b9884ed5bae20f215f02. Root reported source BT.709, TV range, and SDR; the HyperFrames export explicitly uses SDR. The final container copies the original restored AAC and the rendered H.264 picture without another encode. Packet hashes confirm both streams are unchanged by the remux.

Cue timing uses the master buyer-question word at 17.96 seconds and root's measured +0.04725-second WAV insertion placement. The original 20.9 seconds overlap fully; root's restored-source waveform correlation was 0.9983461822071354. Insertion placement is not a measured audiovisual-sync error. The GSAP set is placed one microsecond before the frame boundary so the first intended close frame is unambiguous; rendered-frame inspection is the timing proof.

All acceptance/reference/WAV hashes match. HyperFrames 0.8.34 pins are current, root refreshed the general-video skill, all runtime assets are local, and the final composition passes canonical lint/runtime/layout/contrast checks with zero errors or warnings. The narrow scene uses explicit pose snapshots and output-frame checks; no generic motion assertion is presented as proof of natural performance. The keyframes --shot diagnostic cannot statically resolve its zero-duration hard set; its canvas-only ghost fallback is inapplicable.

Root owns final waveform/audio and phone playback checks, moving naturalness assessment, and any user-facing review handoff. This deliverable changes no canonical episode state and makes no new provider call.

Final technical result:

- File: EP007-avatar-v4-wide-to-close-review.mp4
- SHA256: f08a09bbd49ed8dd39a7686ad35470e9fc2dd5e421383779627327aac8904535
- 16,584,474 bytes; 1920×1080 H.264 yuv420p (8-bit); 24 fps; 505 frames; picture 21.041667 seconds; container 21.042 seconds.
- Mono AAC, 48 kHz. Original and final encoded AAC packet SHA256: fe94cfcbf4348498fd5823844aba8494e7de4c22006e07fa63492b1a3fbffe0f.
- Encoded picture packet hash matches the canonical HyperFrames output after remux. MP4 moov precedes mdat; faststart passes. Full video/audio decode exits successfully with an empty error log.
- Viewed output frames 12, 428, 429, and 504 in output-framing-contact.png. Frame 428 is wide; frame 429 is close. Hair/eyes remain inside the frame through the tail. The final bottom-edge detail is clean; the corrupted source rows no longer appear.
- No moving-performance or lip-sync pass is implied by the frame/contact-sheet inspection. Root performs that final review.

The render command and original-AAC stream-copy remux are reproducible in render_review.sh; render-plan.json records the operation and source chain. Source authorities, the rejected first export, corrected premux output, and final review are retained separately.
