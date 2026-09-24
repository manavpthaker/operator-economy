# Superseded Remotion prototype

This directory is the preserved v1 isolated Blueprint Cinema Remotion project. It is no longer an authorized implementation target for new production work. HyperFrames is the canonical motion, designed-scene, directed-animatic, and render-plate runtime; DaVinci Resolve is the final editorial and finishing environment. See `../TOOLCHAIN.md`.

Keep this directory and its review renders reproducible as historical diagnostics. Do not add new production scenes, migrate the new visual language into it, incrementally polish EP006 here, or maintain a dual renderer path without explicit operator approval.

Everything below documents historical v1 behavior only.

The renderer consumes only validated, approved greenfield `render-data/greybox.json`. It does not import legacy OE scene components, storyboards, coverage maps, render data, or prior pilots. Its target is a plain, whole-episode greybox with stable object IDs, simple paths, readable labels, explicit asset-ticket placeholders, and locked narration.

The greybox uses an overview-to-focus camera grammar. It opens or resets on the persistent world, travels to the `focus` object explicitly named by the active visual-plan unit, enlarges the immediate connected route, and dims unrelated objects. A fixed overview inset shows the whole map and the main camera window. Camera motion is derived only from authored object IDs, coordinates, modes, and camera anchors; it never parses narration text to choose a view.

The separate `BlueprintCinemaDeckPrototype` composition was an operator-review candidate. It covers the locked opening 90 seconds as a sequence of presentation slides. It was rejected as the creative direction because it still failed to specify and reveal the right causal relationships against the VO. It remains evidence of that finding, not a candidate for repair.

The renderer does not infer layouts from narration text. Run `npm run typecheck` here, or use `../bin/oe-cinema smoke-render EP006-direct-booking-recovery` from the Blueprint Cinema root after `greybox_ready`. Generated audio and renders are ignored.

The low-resolution whole-episode camera-review command is:

```bash
npx remotion render src/index.ts BlueprintCinema ../episodes/EP006-direct-booking-recovery/delivery/generated/EP006-greybox-camera-review.mp4 --props=../episodes/EP006-direct-booking-recovery/render-data/greybox.json --codec=h264 --crf=28 --scale=0.5 --concurrency=4 --overwrite
```

Rendering this file never records `greybox_approved`.

Render the 90-second deck prototype with:

```bash
npx remotion render src/index.ts BlueprintCinemaDeckPrototype ../episodes/EP006-direct-booking-recovery/delivery/generated/EP006-greybox-deck-brand-title-prototype.mp4 --props=../episodes/EP006-direct-booking-recovery/render-data/greybox.json --codec=h264 --crf=24 --scale=0.5 --concurrency=4 --overwrite
```
