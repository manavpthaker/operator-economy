# EP007 Higgsfield diagnostic review

Diagnostic assembly, 2026-09-08. A live Studio visibility defect was found after the initial mechanical checks; the wrapper fix passes the complete automated check and the corrected Studio canvas has been verified. Owner playback pending. No final render or production gate advancement.

**Studio:** http://localhost:3022/#project/hyperframes

HyperFrames launched a persistent background server at3022 because the requested port was unavailable; HTTP200 verified. The active server URL, not the package's requested3020, is the review address. `reports/preview-http.json` and `reports/preview-console.txt` preserve the returned result.

## Actual assembly

975frames at24fps,40.625seconds. Existing R9 A/B/D and byte-identical native Working Model remain. New C uses source0.000–6.916667; the owner's mouth closes approximately0.257seconds before “And then,” while the gaze lowers across the narrated stop cue. This is approximate enacted timing, not synchronized character dialogue. The buyer remains seated in the reviewed source.

After an explicit one-second silent separator, the avatar test plays all145returned frames and its own5.952-second sound. **Its exact-audio fidelity failed.** The original5.600-second narration WAV is retained as a reference and is not dubbed over mismatched mouth movement. The visible label states `Avatar test · generated audio timing differs`. This branch is an honest raw failure diagnostic, not replacement narration or a publishable presenter.

## Verification

- Source hashes, exact original/reference WAV PCM, source coverage and975frame contiguous picture pass.
- All five actual video sources decode completely through FFmpeg without errors.
- HyperFrames0.8.31 remains pinned. The initial check passed lint, runtime, layout, motion and contrast with zero errors/warnings and9/9 contrast checks, but it did not catch the live Studio visibility defect. The complete check after the wrapper fix also passes all five categories with zero errors/warnings and9/9 contrast checks.
- The first motion check rejected an ambiguous class selector. The assertion was corrected to five exact label IDs; picture and timing were unchanged, and the complete check was rerun successfully.
- Inspected actual full-frame snapshots of the opening, late model and final included presenter frame, plus the targeted contact sheet showing C's answer/stop, model action, separator and speaking presenter. Labels, footage, native model and separator are visible; no missing or black plate observed in these sampled frames.
- Live Studio correctly sought C to source2.916667 at record13 but left the separator and later labels visible on top. The fix adds deterministic registered GSAP visibility gates to non-clip visual wrappers, including the provenance labels. Framework clip/media timing and the native model bytes remain unchanged. The parent verified the actual Studio canvas at13s: C and its Higgsfield label, with source time2.916667 and media readyState4; at28.5s: the native model; at37s: P and its audio-timing warning; then backward to0s: A and its existing-Kling label. The parent subsequently reported uninterrupted forward playback reaching the end with the player unmuted. This establishes live playback completion, not an independent listening or creative-acceptance judgment.
- An additional exact-zero defect appeared only after returning from the end: the initially active wrappers reverted to hidden CSS. Rapport, provenance and its A/B label now have visible initial CSS, with the redundant zero-time hide removed. The parent verified37s, then40.625→0s in the live Studio canvas: the opening A and correct existing-Kling label are visible at exact0. The automated check now includes exact0 and passes all five categories with zero errors/warnings. The exact0 snapshot was visually inspected and shows A with its correct label.
- Studio reported40.633333seconds, while the authored record remains exactly975frames at24fps/40.625seconds. This is a preview display rounding observation; no record timing was changed to match it.
- `reports/check.json` is the initial parsed browser report; `reports/live-fix-check.json` records the passing check after the visibility fix. `reports/frame-zero-check.json` and `reports/frame-zero-check-console.txt` record the passing follow-up check including exact0 after the backward-seek correction. `reports/targeted-snapshots/contact-sheet.jpg` is the inspected targeted sheet. `reports/verification.json` records the final source policy and hashes; the final full-decode and source/hash check after Studio annotations is retained in `reports/final-verification-console.json`.

Source review and sampled snapshots are not an independent continuous audiovisual listening pass or owner acceptance. The parent audio specialist owns the reported audio-fidelity comparison. Review the complete40.625-second playback with sound before judging creative quality. The server remains available; no MP4 was rendered, no source was overwritten and no publication occurred.
