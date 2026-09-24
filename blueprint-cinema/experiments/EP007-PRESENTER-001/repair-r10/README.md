# Test J — blend the presenter into the study

Owner instruction: “okay but i looks overlayed on the bacgkround so lets blend it together but keep whats working”. Test I and its editable R9 project remain preserved.

## Selected treatment

The main mismatch was the crisp, directional room behind the softer, broadly front-lit presenter. Two candidates were inspected at 0.4, 16.4, and 30.56 seconds, with the CLI also providing 29.682 seconds.

- A softened the original room and reduced contrast/highlights. It helped focus but retained the hard sun patches that implied a different light source.
- B, selected for rendering, uses a lighting-only edit of the same empty study: soft overcast daylight and broad ambient fill. The window, wall, bookcase, props, chair, framing, and perspective remain recognizably the same. The generated edit is a replacement background plate, not a regenerated presenter. See `room-lighting-prompt.md` for the built-in image-generation prompt.

Final room treatment uses canonical HyperFrames controls on the isolated `#room` image: `effects.blur=0.28`, `adjust.contrast=-0.04`, `adjust.highlights=-0.08`. Other room adjustments remain neutral. The room's focus is reduced to match the source's photographic softness. No generic LUT, warm tint, glow outline, grain overlay, or exposure change is applied to the person.

The narrow foreground fringe is reduced by deriving the alpha from the original Vision matte with three one-pixel erosions and Gaussian smoothing sigma 0.85. R9 used two erosions and sigma 0.6. This changes only the cutout boundary. `foreground-qa.json` verifies all 765 RGB frame hashes and timestamps still match G's original center crop; the shoulder-motion asset is byte-identical to R9. Shirt treatment, framing, scale, position, shoulder tracking, and bottom overscan are preserved.

## Inputs and output

- Source G: `media/repair-r7/test-g-full-scope-avatar-iii-1080p.mp4`, SHA256 `6bfc0bd9190448e4a41d7ea694797ee48135d6ece85467a90bfb3e11926c749f`.
- Working project: `study-composite-r10/`.
- New project-bound room plate: `study-composite-r10/assets/study-diffuse.png`.
- Built-in generated original: `/Users/brownmanbrain/.codex/generated_images/01a07aa0-5764-78b1-a4e8-5f56cbe3ae34/exec-705fd848-bb26-4aa8-bd2d-01448ff94bcd.png`.
- Review video: `media/repair-r10/test-j-landscape-study-blended-1080p.mp4`.

The isolated working project was upgraded from HyperFrames 0.8.27 to 0.8.31 under the current skill's maintenance instruction. `upgrade-check.json` records a passing compatibility check before visual edits, and `snapshots/treatment-before/` captures its initial appearance. R9's source and pin were left unchanged.

## Verification

`hyperframes-check.json` records the final lint/runtime/layout check. The foreground RGB and shoulder-motion preservation check is `foreground-qa.json`. Final render geometry, full decode, exact returned G AAC bitstream and decoded PCM equality are recorded in `technical-review.json` by `verify_render.py`. `status.json` binds the selected assets and current output with SHA256.

The same narration and facial movement remain the performance authority. Full playback is required to judge naturalness; frame checks do not approve acting or final episode placement. Fine hair/ear boundaries and synthetic fabric deformation remain limits of this source-based composite. No cinematic work, narration master, canonical episode state, release gate, or publication was changed.
