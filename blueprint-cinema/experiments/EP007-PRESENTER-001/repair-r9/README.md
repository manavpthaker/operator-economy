# Test I — landscape study refinement

Owner instruction: “keep going.” This is a local refinement of H, retaining G's Avatar III performance and narration. H remains preserved in `repair-r8/` and `study-composite-r8/`.

## Changes

- Alpha edge: two one-pixel minimum erosions and Gaussian smoothing, sigma 0.6. Only the matte changes; all 765 RGB foreground frames and timestamps match G's original 608×1080 center crop exactly before composition. See `foreground-qa.json`.
- Synthetic outer shirt: HyperFrames `effects.blur=0.14`, isolated on `#shirt`. Two conservative blur candidates were inspected. No color or exposure change was justified.
- Outer shoulders follow four shirt-only patches measured from G. Direct reference matching avoids accumulated tracking drift. The final smooth similarity transform uses translation, rotation, and scale; frame 10 at 0.4 seconds is the exact identity reference. The source performance is not warped or retimed.
- Extra shirt coverage below the frame prevents a moving lower edge from becoming visible. The first render was stopped after a frame-zero strip was found. Static shirt mapping now uses `translateY(27.28px) scaleY(1.22)` about its bottom, preserving the prior mapping at reference y=600 and adding 27.28 design pixels below the frame.

## Provenance and composition

Source: `media/repair-r7/test-g-full-scope-avatar-iii-1080p.mp4`, SHA256 `6bfc0bd9190448e4a41d7ea694797ee48135d6ece85467a90bfb3e11926c749f`.

G's image is cropped at x=656, y=0, 608×1080. Its unchanged RGB is combined with the existing Vision matte, adjusted as above, in a lossless alpha VP9 asset. The original generated study and shoulder reference are reused from R8. No new provider generation or voice synthesis occurred.

Measured motion packet: `blueprint-cinema/episodes/EP007-exit-readiness-prep/agents/deliverables/presenter-study-motion-r9/`. Final `tracking.json` SHA256 `ee1f1dd6e043138ad6009da0e06534e820a6428f20df0f7ccf9983ea36622c01`. All 765 frames are contiguous at 25fps. Median patch correlations are 0.959–0.986; median similarity-fit error is 1.027 source pixels. The confidence, continuity, and independent visual checks live in that packet.

Editable project: `study-composite-r9/`. HyperFrames 0.8.27 owns the composition and render. `assets/shirt-motion.js` contains the measured poses, built synchronously into a paused GSAP timeline; a wrapper outside the shirt mask receives the transforms. Pivot: (835.3697776, 766.5905659) in the 1672×941 design space. Translations are multiplied by 0.9821018813; rotation and scale retain their measured values. The separate design-space transform scales the complete scene to 1920×1080.

## Verification and limits

`hyperframes-check.json` records zero lint, runtime, or layout findings at 0, 0.4, 3.4, 16.4, 23.2, and 30.56 seconds. Those snapshots were visually checked. The keyframe strip is diagnostic only: the CLI's text parser reports unresolved loop values; actual painted snapshots verify distinct measured poses. Debug markings are absent from the composition.

Final output is `media/repair-r9/test-i-landscape-study-refined-1080p.mp4`. `verify_render.py` checks the full decode, 765 frames at 1920×1080 and 25fps, and AAC bitstream plus decoded PCM equality with G. `technical-review.json` records the output hash and verification results when complete.

The room and outer shirt remain synthetic. Rigid tracking improves coordination but does not recover missing original shoulders or natural fabric deformation. A faint edge around hair/ears and some shirt texture difference can remain. Sampled visual and technical checks do not establish full perceptual naturalness; this remains a review candidate for owner playback. No narration master, cinematic work, episode placement, release gate, or publication was changed.
