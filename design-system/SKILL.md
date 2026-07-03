---
name: operator-economy-design
description: Use this skill to generate well-branded interfaces and assets for The Operator Economy (a documentary-grade YouTube channel + newsletter + blueprint library for senior professionals), either for production or throwaway prototypes/mocks. Contains essential design guidelines, colors, type, fonts, assets, and UI kit components for prototyping.
user-invocable: true
---

Read the README.md file within this skill, and explore the other available files.

If creating visual artifacts (slides, mocks, throwaway prototypes, etc), copy assets out and create static HTML files for the user to view. If working on production code, you can copy assets and read the rules here to become an expert in designing with this brand.

If the user invokes this skill without any other guidance, ask them what they want to build or design, ask some questions, and act as an expert designer who outputs HTML artifacts _or_ production code, depending on the need.

## The one rule that matters most

Every design decision answers: *would a 45-year-old VP of Product share this under their real name on LinkedIn?* Documentary rigor, never hustle. **Design like a blueprint, not like a publication — and make the blueprint feel alive**: cream editorial trust + the navy Working Schematic (drafting grid, wired nodes with real prices, live status) that looks like the business the viewer is going to build.

## Fast start
- Link `styles.css` (one file, pulls in all tokens + fonts).
- Components live on `window.TheOperatorEconomyDesignSystem_bf951d` (load `_ds_bundle.js`).
- Type: Boska 700 display (≥40px ONLY — hard floor), Zodiak 700 for 18–44px (−0.02em), Supreme body, Fragment Mono (single 400 weight) for EVERY number & citation.
- Palette rule: any composition = Ink + Paper (or Navy #14263E) + ONE accent. Gold (#C4A45F on dark, #7A5E24 text on paper) is the dark-world accent; Drafting Blue the paper-world accent; sage = live/verified status only.
- Signatures: citation chip on every figure · gold gap arrow ($5.9B → $2K) · engineering title block · margin annotation rail · the Schematic/SchematicNode panel (every node needs a REAL figure).
- Italic ration: max ONE italic phrase per composition.
- Hard bans: Instrument Serif/AI-startup default, emoji, neon, gradients, glassmorphism, income overlays, scarcity, placeholder nodes, radii >3px. See guidelines/Design System.html §05.

## Where things are
- `guidelines/Design System.html` — the published system document (read this second, after README).
- `README.md` — full brand + visual + content guide, and a file index.
- `tokens/` — colors, typography, spacing, fonts, base helpers.
- `surfaces/` — canonical comps: site hero, YouTube thumbnail, newsletter masthead, blueprint cover.
- `foundations/` — specimen cards. `components/` — Button, Badge, Card, Input, CitationChip, TitleBlock, Stat, SheetHeader, Annotation, GapFigure, Schematic, SchematicNode, DataTable, BarChart.
- `ui_kits/` — interactive website/newsletter/blueprint screens (Rev-A layouts; surfaces/ is the canonical look).
