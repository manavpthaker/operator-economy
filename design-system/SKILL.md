---
name: operator-economy-design
description: Use this skill to generate well-branded interfaces and assets for The Operator Economy (a documentary-grade YouTube channel + newsletter + blueprint library for senior professionals), either for production or throwaway prototypes/mocks. Contains essential design guidelines, colors, type, fonts, assets, and UI kit components for prototyping.
user-invocable: true
---

Read `README.md`, then read `boundary-ledger/README.md`,
`boundary-ledger/cross-media-authority.md`, and `boundary-ledger/semantic-core.json` before creating
new OE visual work.

- For web or static episode identity, also read `boundary-ledger/illustration-language.md` and
  `boundary-ledger/component-contracts.md`.
- For scenes, animations, or motion graphics, also read `boundary-ledger/motion-language.md`,
  `boundary-ledger/scene-contracts.md`, `../docs/blueprint-cinema.md`, and
  `../blueprint-cinema/TOOLCHAIN.md`.
- For audio-led or podcast clips, also read `boundary-ledger/audio-led-clips.md` and the caption
  overlay doctrine. Use actual precomputed audio data; do not invent a visualizer.

If creating visual artifacts (slides, mocks, throwaway prototypes, etc), copy assets out and create static HTML files for the user to view. If working on production code, you can copy assets and read the rules here to become an expert in designing with this brand.

If the user invokes this skill without any other guidance, ask them what they want to build or design, ask some questions, and act as an expert designer who outputs HTML artifacts _or_ production code, depending on the need.

## Forward authority

**Boundary Ledger is the cross-media authority for new OE visual work.** The surface stays composed;
the model stays provisional. Web keeps the page composed and model rough. Motion establishes a
stable world and moves only the accountable change. Audio-first keeps the voice primary and marks
the argument rather than the beat.

The semantic core owns meaning. Step 3 selects approved operations, Blueprint Cinema directs their
episode-specific use, HyperFrames implements deterministic designed scenes, and Resolve finishes
and delivers. Do not author new semantic roles inside a runtime or episode plan.

Rev C is retired as forward authority but remains a compatibility implementation for unmigrated
consumers. Rev D is archived narrative research. Do not bring Rev C’s drafting grid or gold/blue
identity, or Rev D’s cobalt/gold, sinkholes, glow, orbit, or generic node builds into new work.

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
- Motion operations are fixed: `establish`, `trace`, `route`, `interrupt`, `correct`, `return`,
  `pin`, and `settle`. Do not invent synonyms as new semantic tokens.
- Captions use `drop / rail / embed`. Kinetic thesis type is scarce and cannot duplicate the rail.
- A 9:16, 1:1, or 16:9 model is an authored recomposition, never a crop of the 3:2 static master.
- Run `node boundary-ledger/qa/validate-system.mjs` after changing the core, bindings, manifests, or
  specimen evidence.

## Where things are
- `boundary-ledger/` — cross-media semantic core, bindings, scoped web implementation, illustration
  and scene contracts, motion/audio field manuals, manifests, specimens, and validation.
- `guidelines/Design System.html` — the published system document (read this second, after README).
- `README.md` — full brand + visual + content guide, and a file index.
- `tokens/` — colors, typography, spacing, fonts, base helpers.
- `surfaces/` — retained Rev C production references during migration.
- `foundations/` — specimen cards. `components/` — Button, Badge, Card, Input, CitationChip, TitleBlock, Stat, SheetHeader, Annotation, GapFigure, Schematic, SchematicNode, DataTable, BarChart.
- `ui_kits/` — interactive website/newsletter/blueprint screens (Rev-A layouts; `surfaces/` is only the canonical Rev C compatibility look).
