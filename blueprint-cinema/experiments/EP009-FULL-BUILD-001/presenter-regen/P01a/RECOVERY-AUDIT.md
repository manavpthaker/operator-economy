# P01 timing recovery audit

The first sentence can be reused at original speed. The full take cannot currently clear the unchanged 0.30-second native-drift gate.

- Original native offsets: 0.25, 0.34, 1.17 seconds, with correlations 0.828, 0.667, 0.343. The early offset is reliable. The late offset has competing weak peaks and should not be read as an exact correction.
- Local whisper small.en transcribed both tracks to the same 26 words. Word timing and the native speech endpoint show progressive slowing in the second sentence. Across 4 to 12 percent envelope thresholds, native speech ends at 10.50 to 10.67 seconds; master speech ends at 8.92 to 8.95 seconds. ASR timing was not used for exact cuts.
- Root's constant-speed scan also fails the existing gate. Nonlinear retiming would require a separate justified experiment and performance review; it is unnecessary for this bounded source-window recovery.
- First-sentence-only measurements on the encoded prefix are 0.25/0.25/0.25 seconds, correlations 0.781/0.945/0.833, spread 0.00. Prefix picture is original source frames [0,108), 4.50 seconds, at unchanged speed. Native speech has faded by about 3.90 seconds and the next sentence starts about 4.80 seconds.
- Exact master split: frame 1306, sample 2612000, 54.4166667 seconds. P01a is 99 frames / 198000 samples. P01b is 121 frames / 242000 samples. The entire 220-frame segment and all 440000 audio samples remain in their original order. P01a PCM is exactly equal to the corresponding original master prefix.
- Recommended six-frame head trim leaves 102 source frames, 4.25 seconds, for the 4.125-second first sentence. This retains a 0.125-second handle. A seven-second P01b generation costs 45.5 credits; with the bound P11a 12-second correction, projected generation plus look/diagnostic spend is 1798 of 1800 credits.

The root selected W-to-M coverage at the sentence boundary in the active plan. This edit needs normal-speed audiovisual review once both restored parts exist. Timing diagnostics and still-frame review do not establish lip sync, natural performance, or owner acceptance. The full original P01 and its failed measurement remain preserved. See RECOVERY-PLAN.json for hashes, exact ranges, retained ASR evidence, method, budget arithmetic, and limits.
