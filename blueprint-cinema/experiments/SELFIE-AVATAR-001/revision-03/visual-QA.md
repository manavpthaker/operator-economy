# R3 home selfie: visual QA

Date: 2026-09-12. Reviewer: `avatar_sources`, independent visual sampling.

**Native finding: the sampled sequence shows more visible upper-face variation than the reviewed r2 samples, chiefly in the brows/forehead and cheek/mouth-corner activity. Appearance, outfit, home setting and close selfie framing remain consistent. This is evidence of a visible change, not proof that the full performance now feels natural or satisfies the owner.**

## Native artifact and method

- Higgsfield job: `904f7c14-ab23-4605-b586-6c8b8ad76a84`.
- File: `../media/revision-03/home-olive-r3-native.mp4`.
- SHA-256: `22dbef6f65a857a61c0e872e01ed0993c37445282371755c1425d9ae6224fc1b`.
- Size: 5,521,087 bytes. Probe: H.264, 720 × 1280, 24 fps, 217 frames, 9.041667 seconds of picture.
- Download provenance and complete probe: `video/NATIVE-DOWNLOAD.json`.
- Full-file FFmpeg decode completed without reported errors.
- Reviewed through `view_image`: 12 frames at 0, 0.5, 1, 2, 3, 4, 5, 6, 7, 8, 8.5 and 9 seconds, including the final frame. Evidence: `../media/revision-03/visual-qa-contact.jpg`.
- Compared against the previously inspected r2 native contact sheet, r2 native/restored contact sheet and exact olive image. The performances have different durations and speech timing; equal clock positions are not treated as matching words.

## Observations

| Check | Result and limit |
|---|---|
| Brows and forehead | Noticeable raised-brow/forehead changes are visible around 0.5 and 5 seconds and release in other samples. R2's inspected sequence looked more uniform through the upper face. This supports a tentative improvement in visible engagement, without establishing its timing or naturalness in motion. |
| Eyes and gaze | Open, partly closed and blink samples occur, with generally near-lens gaze. The samples do not establish that the requested contextual look beside the lens happened or that it returned at the intended phrase. Blinking alone is not counted as expressive improvement. |
| Cheeks and expression | Cheek/mouth-corner lift is visible in speaking samples and the face ends with a softer settled expression. No held broad grin appears across the samples. Articulation and expression overlap; not every mouth change is an emotional change. |
| Head and body | Head position and angle vary modestly across samples while the supporting arm and torso remain broadly consistent. Samples cannot rule out repetitive nodding or camera jitter between them. |
| Appearance and clothes | Clear glasses, hair, stubble and visible facial features remain visually consistent with the olive reference. Muted olive open overshirt and off-white crew-neck persist. No gross deformation or wardrobe drift observed. This is visual similarity, not identity verification. |
| Setting and framing | Window/curtain at left, shelves/books at right, daylight direction and close vertical selfie composition remain consistent. Omitting the r2 performance video has not produced a gross setting/framing change in these inspected images. |
| Hands | Complete hands/fingers are outside the sampled crop; hand anatomy cannot be certified. |
| Ending | At 8.5 seconds the native mouth is still visibly open; at 9 seconds it is closed with an easy settled expression. The new supplied audio is approximately 8.173 seconds, so these pictures alone cannot establish whether the native ending follows the actual final word. Restoration and audible playback must resolve the timing. |

No blocking or major visual defect is supported by the native samples. The main unresolved question is whether the more visible expression reads as conversational at normal speed and ordinary phone size, rather than a series of prompted facial poses.

## Reference pins and review limits

- Exact olive image: SHA-256 `f407e60b8f132931c70e103f761a7e336045d8244be2e7264f19a165d0715cb0`.
- R2 native: SHA-256 `a8a2a506dff0df23ebc6d2bb3fc822f1002aeff5da9047452df5b630480faafe`.
- R2 restored: SHA-256 `d5e4e908ad7e6a134f3d2f5fd3afb178853a71fa6ee9cb345cb5de28c9197b8e`.
- Owner feedback and current request: `OWNER-DIRECTION.json` and `video/REQUEST.json`. The owner found r2's eyes/expression flat; this review does not reinterpret that verdict as approval.

This is frame-based visual QA and a technical decode only. It does not establish perceptual lip synchronization, audible pacing/voice quality, full-clip naturalness, brief defects between samples, or owner acceptance. The restored R3 output requires a separate contact check. No generation, audio edit, canonical change, commit or publication was performed by this reviewer.

## Restored R3 follow-up

File inspected: `../media/revision-03/home-olive-r3-sync.mp4`; size 9,962,885 bytes; SHA-256 `c776baa1a2b514805374f1f3aed5eb48fa8d8127da3f9dfe80987e6278252942`. Probe retains 720 × 1280, 24 fps, 217 frames and 9.041667 seconds of picture.

Displayed native and restored samples side by side at 0.5, 5, 8.25, 8.75 and 9 seconds. Evidence: `../media/revision-03/visual-qa-restored-contact.jpg`, native top row/restored bottom row; SHA-256 `a578777c6057eba4eeaf1117d4fd29c5e969932b3f2ed415dc284eb2f4acac7b`.

**The visible brow/forehead engagement at 0.5 and 5 seconds survives restoration.** Glasses, hair, outfit, setting, framing and supporting arm remain consistent in these samples; no gross new facial seam or deformation was observed. Mouth shapes change with restoration, so native articulation is not assumed preserved.

**Ending remains a playback question:** the restored mouth is visibly parted at 8.25 seconds, then closed and settled at 8.75 and 9 seconds. The orchestrator reports the current final spoken word ends around 7.84 seconds. A still frame cannot distinguish lingering speech-like motion from a natural relaxed mouth/breath. Inspect 8.0–8.75 seconds with sound before calling the ending clean; this report does not classify the parted-lip sample alone as a defect or a verified sync failure.

No gross visual drift is supported by the five restored samples. They support retention of the increased upper-face variation, while conversational naturalness, phrase alignment, the requested contextual glance and clean post-speech settling remain subject to moving playback and owner review. This follow-up adds only the requested contact sheet and report text.

## Audio-clock clarification after waveform QA

The final soundtrack places source R3 at +0.2894375 seconds, with 0.998099 waveform correlation. The final word therefore falls near 7.789–8.129 seconds in the output, and the full source ends near 8.463 seconds. The 8.25-second parted-mouth frame is about 0.12 seconds after the transcribed word ending. Preserve the earlier frame observation, but interpret it on this corrected output clock; it does not establish continued silent speech or a perceptual sync defect. The final half-second of output audio is silent.
