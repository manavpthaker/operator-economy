# EP009 Short 03 — private review report

Status: **private review only**. The edit is unbound to a launch URL. A YouTube
Related Video must be attached before release so the final instruction is truthful.

## Review artifact

- MP4: `review/ep009-short03-guest-book-hook-REVIEW.mp4`
- SHA-256: `130136d3b7b0acf0cff72387049bf556e895e318df288a19068e3f0d851838de`
- Video: H.264, 1080×1920, 24 fps, `yuv420p`
- Audio: AAC, 48 kHz, stereo
- Duration: 22.708333 seconds / 545 frames
- Render: HyperFrames 0.8.51, one worker, strict-all, no-best-effort

## Editorial contract

The narration uses five whole locked phrases from the owner-locked r8 carrier. Their
source word and frame ranges are recorded in `SOURCE-EDL.json`; no narration was
rewritten. The open is the exact line “The inn served the guest and doesn't have his
email.” The payoff—the permissioned first-party guest book and the front-desk operating
job—is withheld. The final spoken line is “What the inn needs first isn't an email
tool.” The text-only end card asks “What has to come first?” and points to EP009 through
the Related Video control.

The relay address is visibly marked **illustrative**, and the restriction remains
qualified as the site's rules. No production-status label appears in the picture.

## Verification

- `hyperframes lint`: 0 errors, 0 warnings.
- `hyperframes check --frame-check`: lint, runtime, layout, and contrast all pass with
  zero findings; motion assertions are enabled and pass 300 samples.
- Source carrier SHA-256:
  `cc5805a990d10812b5349568e50a74dc0e21b09ed402b49250f9796640ed710e`.
- Encoded output probe: 1080×1920, 24 fps, H.264/AAC, 22.708333 seconds.
- Decoded-audio comparison: `review/qa/audio-source-comparison.json`. All five source
  ranges correlate at 0.9963–0.9998 after cut-local alignment of 0 to −0.375 ms. The
  expected narration is 20.208375 seconds; the remaining 2.511625 decoded seconds are
  the intentionally silent CTA tail.
- Encoded contact sheet inspected:
  `review/qa/render-contact-sheet.png`.
- HyperFrames scene contact sheet inspected:
  `snapshots/final/contact-sheet.jpg`.
- Audio is active through 20.208 seconds. The final 2.5 seconds are intentionally silent
  for the CTA card. Two shorter pauses at 16.562–16.945 and 18.646–18.932 seconds are
  inherited from the locked phrasing.

No upload, publication, canonical episode edit, or launch-link mutation was performed.
