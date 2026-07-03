# UI Kit — Operator Blueprint (PDF lead magnet)

The document-grade lead magnet — the differentiator the research is blunt about. Three drawing "sheets" on Paper: a cover with the drafting **title block**, a unit-economics sheet with an annotated chart and a mono pricing table, and a stack + full **source list** sheet. Reads like real operator documentation a VP would save and annotate, not a lead-gen PDF.

## Screens
- `index.html` — the full 3-sheet blueprint (sits on a sunken-paper "desk").

## Files
- `BlueprintApp.jsx` — `Sheet` wrapper + three sheets, exported to `window.BlueprintApp`.

## Composition
Uses `TitleBlock`, `SheetHeader`, `DataTable`, `BarChart`, `Stat`, `Annotation`, `Badge`, `CitationChip`. Every figure is mono and sourced; each sheet carries a "Sheet N of 3" footer. Print-friendly: fixed 820px sheets on a neutral desk.
