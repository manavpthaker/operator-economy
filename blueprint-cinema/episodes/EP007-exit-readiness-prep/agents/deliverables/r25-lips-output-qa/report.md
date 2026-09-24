# R25 lips output QA

Completed 2026-09-10. **Technically suitable for the normal-speed comparison. Sampled visual changes are restrained, but clearer articulation is not established by this audit.** Full-motion judgment and owner acceptance remain pending.

Output: `r25-subtle-lips/provider/presenter-generated-raw.mp4`, SHA-256 `72862fe581b834f4c57e4a6226963437a7dafbe63e0c69c503544e4e95031c32`. Root supplied the completed path and hash. This auditor made no provider call, upload, runtime edit, source edit, or approval change.

## Measured technical result

All three source hashes and the output hash match. The output is **1920×1080, 206 frames, 24 fps, 8.583333 seconds**, matching the input's picture coverage. First PTS is zero; all frame timestamps increase at the expected interval. Full decode completes without errors. Source, R22, and output each contain 206 distinct decoded frames with no exact adjacent duplicates.

The original audio remains pinned at 412,000 mono 16-bit PCM samples at 48 kHz. Provider audio has zero measured lag in every tested window:

| B local window | Output minus source lag | Correlation |
|---|---:|---:|
| 0–2.5 s | 0 samples | 0.9997993 |
| 2.5–5 s | 0 samples | 0.9998111 |
| 4.75–6 s, including “one number” | 0 samples | 0.9998638 |
| 6–8.583333 s | 0 samples | 0.9997985 |

Full-clip correlation is 0.9998134. There is no measured onset offset or early-to-late audio drift. Provider AAC decodes to 412,672 samples and is not sample-identical to the original PCM; codec padding/encoding differences are present. The review should continue using the exact original narration, not the diagnostic provider audio. No offset correction or retime is supported by these measurements.

## Observed sampled visual result

Inspected `full-comparison.jpg` and `face-comparison.jpg`: original performance, R22, and React output at B local 0.5, 2.5, 4.666667, 5.083333, 5.458333, and 8.5 seconds.

- Likeness remains recognizable. Sampled shirt/body placement, room, and broad head poses remain consistent with the source performance. No severe visible teeth, mouth, glasses, or facial-structure defect appears in these samples.
- Mouth shapes stay close to R22. At approximately 5.458 seconds, during “number,” the output mouth appears slightly more open and rounded. This is a local visual difference, not evidence that the spoken articulation is better across the sentence.
- The output also changes facial expression outside the lips. At 5.083 seconds, original and R22 eyes are closed while the React output eyes are open. Brow/eyelid expression also differs at 2.5 seconds. Therefore, the result must not be described as preserving every original facial movement or changing only mouth pixels.
- The final sampled frame settles into a similar neutral pose. No broad performance exaggeration is apparent in this contact sheet, but short-lived artifacts or unnatural transitions between samples remain possible.

Lower-frame similarity values in `metrics.json` include scaling and compression differences. They are supporting diagnostics, not a semantic body-motion measurement. Unique frames do not prove natural motion or exclude repeated gestures. No exact source-body preservation claim is made.

## Disposition

Use root's normal-speed playback/export to judge whether this restrained change actually improves enunciation without a distracting blink/expression change, particularly around “one number.” Retain the unchanged narration and latest owner-directed closeup cut. If improvement is absent, the technically clean file alone is not a reason to select it.

Technical audit and sampled visual inspection are complete. **Full-motion lip-sync, natural acting, and owner acceptance are unapproved.** No retry or additional generation was performed by this auditor.
