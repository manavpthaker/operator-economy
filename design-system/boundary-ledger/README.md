# Boundary Ledger

Boundary Ledger is the locked visual system for The Operator Economy landing-page direction.
It pairs a quiet editorial page with episode-specific, rough working-model illustrations.

The governing rule is:

> **The page stays composed. The model stays rough.**

## Authority

This package is the canonical implementation reference for the Boundary Ledger direction. It
does not silently replace the existing root Rev C token system, production site, studio brand
configuration, Canvas templates, video graphics, or publication gates. Those migrations require
separate implementation and verification.

The owner-approved invariants are recorded in
[`../explorations/site-redesign-2026-09/palette-options/LOCK.md`](../explorations/site-redesign-2026-09/palette-options/LOCK.md).

## Package

- [`index.html`](./index.html) — accessible one-page field manual and reference specimen.
- [`tokens.css`](./tokens.css) — scoped color, typography, spacing, and geometry tokens.
- [`components.css`](./components.css) — Boundary Ledger component and pattern classes.
- [`styles.css`](./styles.css) — consumer entry point and field-manual layout.
- [`component-contracts.md`](./component-contracts.md) — required component anatomy and behavior.
- [`illustration-language.md`](./illustration-language.md) — generation, review, and rejection contract.
- [`illustration/manifest.schema.json`](./illustration/manifest.schema.json) — episode-art manifest contract.
- [`illustration/episode-006/`](./illustration/episode-006/) — approved, hashed reference model and metadata.
- [`qa/`](./qa/) — contrast evidence and responsive acceptance checks.
- [`manifest.json`](./manifest.json) — machine-readable package scope, assets, and invariants.

## Use

Link one stylesheet and apply the canonical theme scope to the root element:

```html
<link rel="stylesheet" href="/design-system/boundary-ledger/styles.css" />
<body data-oe-theme="boundary-ledger">
```

The `.bl-system` class remains a compatibility selector for isolated prototypes. New consumers
should use the theme attribute above.

The local font URLs resolve inside this package's [`fonts/`](./fonts/) directory.
The evidence-data face deliberately uses the operating system's monospace stack because no
Fragment Mono binary is vendored locally. Do not declare a local font file that does not exist.

## Core grammar

1. Warm ledger paper carries human context and unresolved work.
2. Deep mineral carries evidence and accountable institutional surfaces.
3. Core oxide marks commitments, exceptions, and one active thesis path.
4. Perimeter steel marks rented capability, dependency, and secondary structure.
5. The accountable docket overlaps only 16px of blank illustration margin.
6. Every episode model remains complete, uncropped, and undistorted at 3:2.
7. On narrow screens the docket remains inset and the working paper becomes full bleed.

## Boundaries

- No checkered grids, blueprint chrome, node maps, crosshairs, or measurement notation on pages.
- No handwritten website type. Handwriting lives inside episode artwork only.
- No gradients, glass, pills, rounded SaaS cards, decorative shadows, or faux stationery.
- No photography as the episode's forward visual language.
- No production or publication implication follows from a design-system specimen.

## Review dimensions

Verify the field manual at 1280px, 933px, 373px, and 320px. At every width confirm:

- no horizontal overflow;
- exact 16px docket attachment;
- a complete 3:2 illustration using `object-fit: contain`;
- a visible hotel–OTA–guest relationship and oxide return path;
- visible keyboard focus;
- sensible reading order without CSS;
- reduced-motion compliance.
