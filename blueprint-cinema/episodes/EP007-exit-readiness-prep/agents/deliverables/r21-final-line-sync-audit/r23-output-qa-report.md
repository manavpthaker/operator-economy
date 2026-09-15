# R23 generated-output QA

Status: technical media checks passed; contact sheet reviewed; full-motion/perceptual review remains with root and the owner. Root owns output selection and the R23 preview. This worker measured and inspected the completed candidate after the output-ready signal.

Run once after root reports the output ready:

```sh
/Users/brownmanbrain/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 blueprint-cinema/episodes/EP007-exit-readiness-prep/agents/deliverables/r21-final-line-sync-audit/r23-output-qa.py
```

The script makes no provider or network calls. It exits immediately if the expected raw output is absent. All generated diagnostics remain in this deliverable folder.

Acceptance checklist:

- Match proposal photo, handled-audio and original-audio hashes.
- Verify the handled input contains the exact first 720,000 original PCM samples plus exactly 5,760 zero-valued samples.
- Probe usable picture duration, frame count, rate, dimensions and start timestamps; expected 377 frames at 25 fps, with at least 15 seconds of picture.
- Decode the complete raw file with FFmpeg error escalation.
- Compare provider audio to the exact first 15 seconds of original narration. Record full-clip and six window correlations, lag and drift, especially the last phrase. Do not infer perceptual lip synchronization from those metrics.
- Inspect an early/middle/late contact sheet for severe identity, anatomy, text, expression or posture defects. Still samples can reject a conspicuously broken candidate; they cannot establish that all movement is smooth or nonrepeating.
- Review the full original-audio playback at normal speed for relaxed articulation, synchronization, restrained head motion, no repeated nodding/swaying, and a complete final word before integration.
- Retain the original narration in the preview. The appended silence is generation-only; trim excess picture at unchanged speed. Any interpretation of the output as selected or approved remains with root and the owner.

Preparing this checklist does not establish that a generated output exists or passes QA.

## Completed output measurements

Raw output SHA-256: `852c3450c632beee9242587187ad1c32513b30f5c4be4cff5155a08b51ecf1e7`, matching root's pin. Proposal SHA-256: `72d35aa3a30585634096f4efbec125998dbfa6fd764e88b6769d425b3744ad60`.

| Check | Observed result |
|---|---|
| Usable picture | 15.08 seconds, 377 decoded frames, 25 fps, first PTS zero |
| Native dimensions | **1280×704**; do not assume a literal 1280×720 canvas |
| Decoder integrity | Full FFmpeg decode passed with error escalation |
| Exact repeated frames | 377 unique decoded pixel frames; no consecutive or nonconsecutive exact repeats |
| Input preservation | Exact 720,000 original PCM samples plus 5,760 zero-valued handle samples |
| Original narration reference | Staged 15-second audio is sample-identical to R22 source samples [2,856,000,3,576,000), master59.5–74.5; max difference zero |
| Provider audio | 44.1 kHz, 15.08 seconds, start PTS zero; diagnostic only |
| Full first-15-second audio alignment | Zero measured lag, correlation0.999739 |
| Six window alignments | Zero measured lag in every window; correlation0.999581–0.999805; zero measured lag spread |

The audio measurements rule out a detected provider-audio timing change or drift. They do not establish phoneme-correct mouth movement. Exact pixel-frame uniqueness rules out literal frame replay, not recurring physical gestures. The preview must retain the original soundtrack, independent of the provider's AAC track.

## R23 contact-sheet assessment

Fifteen samples cover local0–15 seconds, including local11.44 and12.11 around “one number.” Compared with the R22 baseline, several R23 samples show visibly freer jaw opening and a broader range of mouth shapes. No invented text, finger gesture, gross facial/anatomical defect, or conspicuous identity/set discontinuity was found in these samples. Clear glasses, navy shirt and the study remain recognizable against the supplied reference.

The new performance also moves more: the presenter leans forward early and again around “one number,” with additional head tilts. This is not the old source-motion replay, but it may still be more movement than the owner wants. Still samples cannot prove that the complete motion is restrained or nonrepeating, nor establish likeness stability between sampled frames. The final samples settle into a relaxed pose. A normal-speed review must decide whether the broader articulation looks natural or exaggerated and whether the physical emphasis serves the sentence.

Disposition: technically suitable for root's audiovisual comparison and private review, with the native704-pixel height explicitly handled. No full lip-sync or performance approval is issued by this worker. Retain the original R22 source until the replacement is judged in motion.

## R22 comparison baseline

`r22-baseline-contact.jpg` samples A at local0,1,2,3,4,5,6 seconds and B at local0,1,2,3,4,5,6,7,8 seconds. SHA-256 `fcf9e8cfd8d9a698ac47106318077749b479aeb2c43cbc7e331e7d7a39a8f859`. Source A/B hashes match the pinned R22 assets.

Visual inspection finds mouth-shape variation: rounded openings at A0/A4/A5, a wider opening at A6/B4, and shallower teeth-visible shapes in several B samples. The baseline is not a permanently clenched jaw in these stills. Whether teeth-visible shapes persist unnaturally through speech requires continuous phoneme-aware viewing; sampled stills neither dismiss the user's report nor prove correct articulation. The repeated head posture/blink phases are consistent with the independently established shared source-motion lineage. No visible image-text artifact or gross anatomy defect appeared in this baseline contact sheet.
