# UI Kit — Website (theoperatoreconomy.com)

A high-fidelity recreation of the marketing site. **Welsh-grade restraint**: one promise, one conversion asset (the newsletter/blueprint capture), generous whitespace, zero decoration. Evidence appears above the fold — a `TitleBlock` and a sourced chart, not a hero illustration.

## Screens
- `index.html` — the full landing page (header → hero → dark evidence feature → blueprint library → newsletter capture → footer). Interactive: nav active states + working email capture (`type an email → confirmation`).

## Files
- `WebsiteApp.jsx` — all sections (`Header`, `Hero`, `EvidenceFeature`, `BlueprintLibrary`, `Capture`, `Footer`), exported to `window.WebsiteApp`.

## Composition
Built entirely from DS primitives: `Button`, `Input`, `Card`, `Badge`, `CitationChip`, `Stat`, `TitleBlock`, `BarChart`. The dark "evidence feature" band is the one Ink section; everything else is Paper. Each frame holds at most one accent.
