# Boundary Ledger

Boundary Ledger is The Operator Economy’s cross-media design-language authority. Its durable asset
is semantic grammar—not a palette or a landing-page layout.

> **The surface stays composed. The model stays provisional.**

- Web: **The page stays composed. The model stays rough.**
- Motion: **The frame establishes a stable world. Only the accountable change moves.**
- Audio-first: **The voice sets the clock. Sound and motion mark the argument, not the beat.**

## Authority and implementation

Boundary Ledger governs new OE web, static editorial artifacts, episode identity, thumbnails,
designed video scenes, motion graphics, audio-led clips, and social video. It does not own the
episode argument, claim status, runtime, final edit, or publication.

This promotion changes forward design authority. It does **not** claim that existing consumers have
migrated:

- the web reference is verified;
- the static episode-art language has one locked hospitality reference;
- motion and sound bindings are specified but not encoded or mixed as production references;
- the audio-led browser specimen is reviewable, not a delivered master;
- production site, studio, video, newsletter, Canvas, and PDF consumers remain compatibility
  implementations until individually migrated and verified.

The full authority stack, Rev C/Rev D disposition, and named migration blockers are in
[cross-media-authority.md](./cross-media-authority.md) and
[retirement-manifest.json](./retirement-manifest.json).

## Semantic architecture

[semantic-core.json](./semantic-core.json) defines six roles:

1. human context and unresolved work;
2. accountable evidence and institutional records;
3. one active commitment, exception, correction, or owned path;
4. rented capability, dependency, and the current route;
5. verified status only;
6. actual contradiction or risk only.

The core also defines eight operations: establish, trace, route, interrupt, correct, return, pin,
and settle.

Per-medium values live in separate bindings:

- [bindings/color.json](./bindings/color.json) — canonical color/material expression;
- [bindings/motion.json](./bindings/motion.json) — provisional temporal expression using only
  semantic-core operation IDs;
- [bindings/sound.json](./bindings/sound.json) — provisional sonic expression.

The dependency-free validator checks referential integrity, versions, hashes, specimen timing,
caption policy, commitment overlap, audio provenance, and retirement paths:

    node design-system/boundary-ledger/qa/validate-system.mjs

## Field manuals and contracts

- [index.html](./index.html) — browsable cross-media field manual and static reference.
- [specimens/motion-and-audio.html](./specimens/motion-and-audio.html) — actual-audio,
  model-led/text-led, 9:16/1:1/16:9 browser reference.
- [invariants.md](./invariants.md) — universal, surface-specific, and translated rules.
- [motion-language.md](./motion-language.md) — causal operations, scene archetypes, transitions,
  timing, roughness, and aspect ratios.
- [audio-led-clips.md](./audio-led-clips.md) — caption, thesis type, voice trace, and sound contract.
- [scene-contracts.md](./scene-contracts.md) — runtime-neutral designed-scene primitives.
- [motion-ready-asset.schema.json](./motion-ready-asset.schema.json) — layered Working Model
  contract; the locked EP006 JPEG is explicitly not motion-ready by itself.
- [component-contracts.md](./component-contracts.md) — web DOM bindings plus scene-component map.
- [illustration-language.md](./illustration-language.md) — generation, adaptation, and rejection
  contract for rough Working Models.

## Web binding

Link one stylesheet and apply the scoped CSS binding:

    <link rel="stylesheet" href="/design-system/boundary-ledger/styles.css" />
    <body data-oe-theme="boundary-ledger">

The .bl-system class remains a compatibility selector for isolated prototypes. The selector is a
web implementation detail—not the scope of Boundary Ledger’s design authority.

The local font URLs resolve inside [fonts/](./fonts/). The accountable-data role intentionally
uses the operating system’s monospace stack because no Fragment Mono binary is vendored here.

## Universal rules

- Warm paper represents human context, possibility, and unresolved work.
- Deep mineral represents accountable evidence and institutional records.
- Core oxide marks one active commitment or operator-controlled path.
- Perimeter steel represents rented capability, dependency, and the current route.
- Sage represents verified state only. Risk color represents actual contradiction only.
- One primary focal point and one active commitment at a time.
- Roughness stays inside the Working Model layer. Captions, claims, sources, and controls are typeset.
- Motion changes state, then settles. Sound supports meaningful events, not every color or beat.
- Recompose for a new aspect ratio; never obtain 9:16 or 1:1 by blind crop.
- Documentary footage is valid in Blueprint Cinema’s Reality World; it does not replace the
  signature Working Model on static episode-identity surfaces.
- A design-system specimen never implies editorial, production, deployment, or publication approval.

## Web-only rules

The 16px docket overlap, 24px mobile gutter, complete 3:2 static master, object-fit behavior,
keyboard focus, DOM reading order, and browser reduced-motion behavior belong only to the web/static
binding. They are not motion or audio invariants.

## Verification status

- Web reference: inspect at 1280, 933, 390, 373, and 320 CSS pixels; see [qa/](./qa/).
- Cross-file semantics and hashes: run qa/validate-system.mjs.
- Audio-first browser reference: inspect both treatments at 9:16, 1:1, and 16:9 with actual audio.
- Still unverified: layered rough-stroke motion, final encoded output, compression/phone line
  survival, final mix/loudness, and cross-category episode support.

[manifest.json](./manifest.json) is the machine-readable package authority and status record.
