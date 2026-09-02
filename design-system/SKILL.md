---
name: operator-economy-design
description: Use this skill to generate well-branded interfaces and assets for The Operator Economy (a documentary-grade YouTube channel + newsletter + blueprint library for senior professionals), either for production or throwaway prototypes/mocks. Contains essential design guidelines, colors, type, fonts, assets, and UI kit components for prototyping.
user-invocable: true
---

Read `README.md`, then read `boundary-ledger/README.md` and
`boundary-ledger/illustration-language.md` before creating new OE web or episode-illustration work.

If creating visual artifacts (slides, mocks, throwaway prototypes, etc), copy assets out and create static HTML files for the user to view. If working on production code, you can copy assets and read the rules here to become an expert in designing with this brand.

If the user invokes this skill without any other guidance, ask them what they want to build or design, ask some questions, and act as an expert designer who outputs HTML artifacts _or_ production code, depending on the need.

## Forward authority

**Boundary Ledger is the locked direction for new OE web and episode imagery.** The page stays
composed; the model stays rough. Use quiet editorial structure around one tangible, unfinished
working-model illustration. The dark mineral episode card is the accountable docket. Oxide marks
the one thesis-bearing decision or path. Steel marks rented capability and dependency.

The root Rev C tokens, components, bundle, surfaces, and UI kits remain the existing production
implementation until a separately verified migration. Do not bring their drafting grid, wired-node
schematic, or page-wide blueprint notation into new Boundary Ledger work.

Every decision still answers: *would a skeptical experienced operator share this under their real
name?* Documentary rigor, never hustle.

## Boundary Ledger fast start

- Link `boundary-ledger/styles.css` and scope the consumer with `data-oe-theme="boundary-ledger"`.
- Use Boska for one display anchor at 40px or larger, Zodiak for 24–44px editorial headings,
  Supreme for body/UI, and Fragment Mono only for accountable metadata and defensible figures.
- Palette roles: warm ledger `#F5F0E6`; deep mineral `#204440`; core oxide `#B5482F`
  (`#FB8B69` on mineral); perimeter steel `#586D74`; sage is status only.
- Core contracts: `EpisodeFeature`, `AccountableDocket`, and `WorkingModel`.
- Working Models are 3:2, tangible, complete, uncropped, and independently checked at 373px.
- Keep handwriting inside the illustration. Keep page navigation and content typography typeset.
- Hard bans: Signal Ledger teal, checkered page grids, generic node maps, vector-perfect drawings,
  faux stationery, illustration-as-background, automatic crops, gradients, glass, pills, and dense
  decorative metadata.

## Where things are
- `boundary-ledger/` — locked forward direction, scoped tokens, components, illustration language,
  manifest, and browsable field manual.
- `guidelines/Design System.html` — the published system document (read this second, after README).
- `README.md` — full brand + visual + content guide, and a file index.
- `tokens/` — colors, typography, spacing, fonts, base helpers.
- `surfaces/` — retained Rev C production references during migration.
- `foundations/` — specimen cards. `components/` — Button, Badge, Card, Input, CitationChip, TitleBlock, Stat, SheetHeader, Annotation, GapFigure, Schematic, SchematicNode, DataTable, BarChart.
- `ui_kits/` — interactive website/newsletter/blueprint screens (Rev-A layouts; surfaces/ is the canonical look).
