# Porting policy

## Principle

Port proven inputs, validation rules, provenance, brand primitives, and low-level utilities. Do not port the legacy visual organizing system or its downstream approvals.

Prefer stable path adapters and small isolated wrappers. Copy code only when wrapping is impractical, the copied behavior is independently testable, and the source and removed dependencies are recorded in `SOURCE-MAP.md`.

## Consume as authority

- Content-os facts, flow, voice, rubric, and release rules.
- OE research, claim registry, citations, and evidence originals.
- Approved script plus script-evaluation, POV-token, attribution, and caveat gates.
- Final assembled VO, mastered sections, word-level transcript, and authoritative timeline.
- OE design tokens, approved font definitions, logo assets, and semantic color roles.
- Rights, provenance, captions, synthetic-media disclosure, audio, upload, `links.json`, and release contracts.
- Existing Shorts derivation only after a new Blueprint Cinema final master exists.

## Reuse selectively

These behaviors may be wrapped or adapted only after inspection and tests:

- SHA-256 and artifact verification.
- `ffprobe` duration, codec, resolution, and bounds checks.
- Decoupled FFmpeg loudness probing or mastering.
- Provenance manifest fields and checks.
- Footage search/download clients after an exact approved ticket; never automatic selection or old beat assignments.
- Source-document and interface capture that preserves canonical URLs and evidence context.
- HyperFrames CLI, composition, deterministic timing, local-media, snapshot, validation, render, and output-format contracts, while overriding generic creative defaults with Blueprint Cinema direction.
- DaVinci Resolve-supported interchange, media-pool, marker, project-export, render-job, and delivery automation as deterministic handoff utilities.
- Remotion version and low-level staging knowledge only when reproducing the preserved v1 prototype; never for new production implementation.
- Brand-token loading, font loading, captions, audio playback, and other decoupled primitives.

For each reused utility, `SOURCE-MAP.md` must record source path, role, reuse mode (`reference`, `adapter`, `wrapper`, or `copy`), why it remains valid, tests, and removed legacy dependencies.

## Prohibited imports

- Legacy production stages after `vo_complete`.
- `storyboard.json`, its schema, or any screen/beat decisions.
- `coverage_map.json` or existing coverage assignments.
- Legacy `assets.json` entries generated from old layouts.
- `render_data/blueprint.json`.
- `prepare_longform.py` as the new render-data compiler.
- Storyboard generators, pacing scripts, or hand-tuned storyboard builders.
- Routing by narration text, `asset_type`, or section name.
- Legacy full-screen card, sheet, chapter, proof-card, or list compositions as the default world.
- Existing EP006 frames, reviews, opening pilots, Resolve pilots, full renders, or visual approvals.
- Existing Blueprint Cinema Remotion scene source copied, translated, or cosmetically adapted into HyperFrames as a shortcut.
- The finished composition from the isolated HyperFrames runtime experiment.
- Generic B-roll searches or automatic first-result choices.

Legacy media can be reconsidered later only when a new approved asset ticket names the exact story job and the asset independently passes relevance, rights, provenance, and integrity review.

## Import record

Every adapter or reused behavior must be added to the source map before the implementation gate is considered complete. An unrecorded dependency is a validation failure.

## Existing v1 implementation record

The preserved v1 implementation wrapped the system `ffprobe` duration fact, used standard-library streaming SHA-256, referenced only the legacy renderer's Remotion version fields, and adapted the named OE color-token values as a minimal orientation palette. It copied no legacy pipeline or renderer code. Input lock, state, semantic validation, render-data compilation, review generation, schemas, and the persistent-world composition were original implementations under this folder. `SOURCE-MAP.md` records the exact paths, removed dependencies, verification, and status.

No storyboard, coverage map, legacy render data, storyboard builder, scene component, prior frame, pilot, render, visual approval, automatic media choice, or legacy production state after `vo_complete` was imported. Automated clean-room tests cover configuration, compiled render data, and worker packets.

The documentation-canonical HyperFrames-to-Resolve production target is not yet implemented. Its migration must add new source-map rows, contracts, tests, and validation evidence without reclassifying the v1 prototypes as active production code.
