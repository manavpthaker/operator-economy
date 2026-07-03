# UI Kit — Newsletter (research note)

The Monday email, styled as a **research note** rather than a marketing email: masthead with issue number, publish date, reading time, and source count; a single reading column at ~680px; inline mono figures; a `SheetHeader` per section; a sourced `DataTable`; one soft mid-body CTA to the blueprint.

## Screens
- `index.html` — a full issue (Issue №004, the AI-implementation thesis).

## Files
- `NewsletterApp.jsx` — masthead + body, exported to `window.NewsletterApp`.

## Composition
Uses `CitationChip`, `Stat`, `DataTable`, `SheetHeader`, `Badge`, `Button`. Every number in the prose is set in mono; every hard figure carries a citation chip or a "marked estimate" badge — the compliance-as-brand move.
