# EP009 Short 02 — private review r2

Status: **local private review only; not release/export approval**

- Duration: **19.5 seconds** at 24 fps (468 frames), 1080 × 1920.
- Hook: native portrait card using the locked line, “The drafting got cheap. The judgment didn’t.”
- Proof: real locked Node-RED footage; the full `OpenAI · genuine thank-you draft` and `Checkout + one day → queued draft` nodes remain visible at readable scale.
- Human boundary: fictional fixture, awaiting human review, no sending available. No result, send action, or full judgment checklist is shown.
- CTA: 3.0 seconds of silence with “What makes the message hospitality?”, “Full workflow in EP009”, and “Tap the related video.”

## Verification

- Source contract: `review/source-contract-verification.json` — 51/51 checks passed.
- HyperFrames: `qa/check-final.json` — lint, runtime, layout, motion, and contrast all passed with zero findings. Motion was enabled and sampled 300 times; frame geometry was sampled across all scenes.
- Encoded media: `review/render-probe-r2.json` — H.264/AAC, 1080 × 1920, 24 fps, stereo 48 kHz, exactly 19.500 seconds.
- Encoded audio: `review/audio-silence-r2.log` confirms the CTA is silent from 16.500854 through the end.
- Encoded-frame inspection: `review/contact-sheet-r2.png` covers the hook, operator footage, overview, OpenAI node, drafting, checkout node, human boundary, and CTA.
- MP4 SHA-256: `a8cf2031976cf8d7e0df8ba32689b6e0a856c7b01265c3c5416e7227069c9563`.

## Review artifact

`renders/ep009-short02-machine-judgment-private-review-r2.mp4`

The YouTube Related Video target remains intentionally unbound. Bind it only after the exact locked EP009 r8 upload exists in `studio/originate/<slug>/launch/links.json`; do not reuse a legacy launch URL.
