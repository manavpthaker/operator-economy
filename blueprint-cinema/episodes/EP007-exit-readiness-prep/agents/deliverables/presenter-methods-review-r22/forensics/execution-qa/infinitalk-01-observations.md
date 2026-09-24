# InfiniteTalk 01 native QA

Native SHA256 `01438b738bd53984650b46973737b3e3037d7355e5029b80f4524772ed56aea9` verified before and after QA.

**Technical result:** full decode passes; H.264 1280×704, 25fps, 137 frames, 5.480s picture; AAC mono 44.1kHz, 5.480s native audio. Video timestamps increase consistently. No resizing, remuxing, retiming or geometric correction was performed.

**Audio:** early/late/final-word comparison windows align at 0ms, correlations 0.999274 / 0.999762 / 0.996547; no measured inter-sentence drift. The checked 4.95–5.35s window has 0.13s picture margin. This window is not asserted to end at the exact final phoneme.

A separate ending check confirms source content through 5.48s is retained in the decoded output: source/native RMS is −39.62/−39.67dBFS for 5.35–5.40 and −51.54/−51.56dBFS for 5.40–5.48. The 5.30–5.47 window aligns at 0ms, correlation 0.98075. The omitted 5.48–5.60 source tail is near-silent (RMS −107.54dBFS, peak −90.31dBFS), independently remeasured. The native result is still 0.12s shorter than the input; no claim of full-duration equality. See [ending check](/Users/brownmanbrain/GitHub/operator-economy/blueprint-cinema/episodes/EP007-exit-readiness-prep/agents/deliverables/presenter-methods-review-r22/forensics/execution-qa/infinitalk-01/ending-audio-review.json).

**Sampled observations:** inspected the same 13 diagnostic times used for OmniHuman plus InfiniteTalk's final native frame at 5.44s. At 0.92–1.20s the head shows less dramatic forward dip than the OmniHuman sheets, but hands are more active: both palms lift/open across 0.76–1.20s, with another right-hand lift near 4.16s. At 3.60s the mouth is wide open despite the quiet source interval; this needs actual moving sync review. Shelves remain substantially straight in the checked samples, and no gross detached limb is apparent at contact-sheet scale. Moving hand contours soften; anatomy cannot be certified from these samples.

[Contact sheet](/Users/brownmanbrain/GitHub/operator-economy/blueprint-cinema/episodes/EP007-exit-readiness-prep/agents/deliverables/presenter-methods-review-r22/forensics/execution-qa/infinitalk-01/contact-sheet.jpg) · [Technical report](/Users/brownmanbrain/GitHub/operator-economy/blueprint-cinema/episodes/EP007-exit-readiness-prep/agents/deliverables/presenter-methods-review-r22/forensics/execution-qa/infinitalk-01/technical-review.json)

**Limits:** no full-speed audiovisual observation performed; actual lip sync, naturalness and owner preference remain unverified. Head-pose comments compare sparse native-frame sheets, not measured continuous motion or acceptance. InfiniteTalk 02 remains pending.

