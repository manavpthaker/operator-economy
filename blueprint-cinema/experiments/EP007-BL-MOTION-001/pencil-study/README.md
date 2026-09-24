# Pencil linework A/B study

An isolated redraw of the existing 28-second EP007 animation, requested by the user. The original
`../hyperframes/` source and render are preserved. This does not approve a production gate or change
the Boundary Ledger authority files.

## Visual change

- Hand-authored uneven silhouettes for the owner and three customers.
- Irregular document and folder geometry, open corners and overshooting marks.
- 2,920 fixed, short vector pencil strokes with varying width and opacity, overlapping retraces and
  real gaps; sparse cross-hatching on figures, corners and the folder tab.
- Slightly heavier oxide marks preserve the single active cue.
- No wobble, noise filter, per-frame randomization, new movement or new sound.

Typography, palette, all visible words, narration, object identity, outer transforms and timeline
code are unchanged. The 27 original timed paths are reveal masks, not the visible contours; this
preserves every existing draw duration and stagger. Geometry is compiled once into static SVG.

## Comparison

- `renders/EP007-BL-PENCIL-001.mp4`: full-size revised 28-second animation.
- `renders/EP007-BL-PENCIL-comparison.mp4`: time-aligned original left / redraw right, one unchanged
  narration track.
- `renders/pencil-detail-comparison.png`: original / redraw crops from the encoded videos at 3.9s.
- `qa/render-verification.json`: actual file hashes, frame count, duration, audio equivalence and
  black-frame detection. Not an aesthetic approval.
- `qa/hyperframes-check.json`: full strict check tied to the checked source hash.

## Rebuild

From the parent experiment directory:

```sh
node build-pencil-study.mjs
node check-pencil-study.mjs
```

After explicit authorization to render, from this directory:

```sh
HYPERFRAMES_NO_TELEMETRY=1 HYPERFRAMES_RUN_ID=ep007-pencil-ab-01 npx --yes hyperframes@0.8.27 render --quality high --workers 2 --strict --output renders/EP007-BL-PENCIL-001.mp4
```

Then from the parent experiment directory:

```sh
node compare-pencil-renders.mjs
```

The compiler fails if the original source hash changes. It does not modify the original. This is a
landscape style test, not evidence of a recomposed 9:16 or 1:1 deliverable.
