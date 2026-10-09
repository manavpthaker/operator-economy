# EP009 Short 04 r2 · private review

## Result

The r2 hook is a 23.708-second, 1080×1920 private review MP4. It opens with the modeled
`$105K–$130K` total over the locked presenter and the exact line `It's the wrong number`. It then
states the full spoken 18–22% qualification, identifies that percentage as the narrator's
assumption from reported bands, and stops before the recoverable-share calculation.

The end card holds for 2.25 seconds:

- `What can this inn actually afford?`
- `The full calculation in EP009`
- `Tap the related video`

The related-video target is deliberately unbound. It must be configured against the exact new r8
release at publication; no legacy launch URL is used.

## Exact edit

The audio uses four whole-phrase ranges from the locked r8 carrier, in this order:

1. `[12495,12618)` — wrong-number correction and `It needs the sites.`
2. `[12150,12409)` — full 18–22% assumption and `$105K–$130K` modeled annual total.
3. `[12426,12487)` — `That's where the old version of this argument stops.`
4. `[12618,12690)` — `The real question is what a recovery service can shift.`

No new spoken word, number, synthetic performance, provider state, or result was introduced. The
locked episode and `EP009-SHORTS-001` were not changed.

## Verification

- HyperFrames 0.8.51 final gate: pass.
- Lint: 0 errors; 7 non-blocking structural warnings from keeping the six authored states in one
  inspectable root composition.
- Runtime: 0 errors, 0 warnings.
- Layout and media frame geometry: 0 errors, 0 warnings.
- Motion assertions: enabled; 0 errors, 0 warnings.
- Contrast: 30 of 30 tested text states pass.
- Motion map: 16 registered, seek-safe GSAP tweens.
- Render: standard quality, 24 fps, one worker, 569 frames.
- Output: H.264 1080×1920 video with 48 kHz stereo AAC, 23.708333 seconds.
- Integrated loudness: −19.3 LUFS; loudness range 3.7 LU.
- Presenter-motion check: 123/123 unique frames in the cold open and 72/72 unique frames in the
  closing question. This clears the source sparse-keyframe warning against the rendered artifact.
- Rendered contact sheet was inspected; captions, spoken qualification, model labels, presenter,
  question, and full CTA are visible at phone scale. No black-frame interval was detected.

## Review boundary

This MP4 exists only for private timing and composition review. It does not approve upload,
release, publication, public title/copy, pinned comment, or related-video binding.
