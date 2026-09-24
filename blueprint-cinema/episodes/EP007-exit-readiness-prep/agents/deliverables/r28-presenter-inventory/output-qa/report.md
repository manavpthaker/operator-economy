# R28 generated question: independent output QA

**No blocking technical defect found. Suitable for root's normal-speed playback review.** Sampled likeness and performance continuity are plausible; full-motion lip sync and owner acceptance remain unapproved.

Raw output SHA-256: `754c51ee1ee904cc4bb57ca4c3d0ece45d5ac36499169f145529db38ce4d1f28`. Root reports the single completed request `01a08dc8-6e07-77d0-a175-b0d58fff1c77`. No provider operation was performed by this auditor.

## Measured

- Output and submitted source are **1920×1080, 289 frames at 24 fps, 12.041667 seconds**, starting at PTS zero. Full output decoding completes without errors. Every decoded source/output frame is distinct; no exact adjacent duplicates occur.
- Submitted video SHA `4f2e9ad00c68a603fc76761306eb7156823d2bd42e2aadae486c3e9a04f3b2b0` and WAV SHA `cec8a10ed92d88264aff9c289a330b3d02007ffa599b72589b8ff127a14e8262` match the prepared request.
- Submitted audio is exactly equal to locked-master samples **[6,432,000,7,010,000)**: 578,000 original PCM samples. No voice replacement or sample edit was introduced in that input.
- Output audio lag is **zero samples** in all four windows: local 0–3, 3–6, 6–9, and 9–12.041667 seconds. Correlations are respectively **0.999530, 0.999781, 0.999808, and 0.999795**; full-clip correlation is **0.999747**. No measured onset offset or early-to-late drift supports a timing correction.
- Provider audio decodes to 578,560 samples because it is encoded; this is not sample-identical master audio. Root should retain the exact original narration as the review soundtrack.

## Observed sampled picture

Inspected source/output full-frame and central-face comparisons at local **0, 3, 6, 9, 11.5, and 12 seconds**, including the first and final output frames.

Recognizable likeness, shirt, background, shoulder placement, and broad head poses remain consistent. No severe mouth, teeth, glasses, or face-structure deformation appears in these samples. Mouth shapes change as required for different dialogue. Brow and eyelid expression also changes slightly, particularly at 3 and 6 seconds; the result cannot be described as literally changing only lip pixels.

The final sampled frame at local **12.000** still has slightly parted lips, 120 ms after the transcript's final-word endpoint at local 11.880. This is a playback watch point, not proof of lost speech or a bad ending: the original audio and picture cover the word. Check that the outgoing cut feels finished with the actual narration.

## Limits and disposition

These checks establish file integrity, original input samples, audio alignment, and sampled visual plausibility. They do not certify every phoneme, blink, movement transition, or exact body-pixel preservation. No source, raw output, runtime, narration, approval, or external service was modified.

Technical and contact-sheet review are complete. Root owns the browser derivative, actual cut timing, full-motion playback, and any owner selection. No retry or additional generation occurred.
