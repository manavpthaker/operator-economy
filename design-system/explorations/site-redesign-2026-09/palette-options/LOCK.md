# Boundary Ledger landing-page visual-direction lock

**Owner decision:** Boundary Ledger was approved as the landing-page visual direction for
The Operator Economy on 2026-09-02.

> **Forward pointer:** this file remains the historical landing-page lock. The later 2026-09-02
> owner clarification promotes Boundary Ledger’s semantic grammar across media; it does not turn
> the web geometry below into motion or audio rules. Current authority lives in
> [`../../../boundary-ledger/README.md`](../../../boundary-ledger/README.md) and its manifest.

This lock freezes the palette roles, page-to-illustration relationship, episode-card behavior,
and responsive treatment represented by the Boundary Ledger homepage prototype. A material
change to those decisions requires a separate owner review.

## Frozen invariants

1. **Boundary Ledger is the selected palette.** Warm Rev C paper carries the human working
   record; deep mineral carries accountable institutional surfaces; oxide marks commitments,
   exceptions, and the active path; perimeter steel marks rented capability and dependency.
2. **The page remains editorial, not a blueprint interface.** Blueprint and wireframe language
   lives primarily inside the episode illustration. The surrounding landing page does not regain
   a checkered grid, dense mini-labels, or diagrammatic chrome.
3. **Episode imagery is a rough working model.** Drawings are hand-drawn and handwritten, with
   uneven pressure, imperfect alignment, open corners, overdrawn strokes, and lines that do not
   always meet. They must remain discernible without looking finished or mechanically traced.
4. **The episode card is the accountable docket.** The dark mineral card carries episode identity,
   title, description, publication date, source count, and Canvas status. It may attach to the
   drawing but must not cover thesis-bearing marks.
5. **The illustration remains whole.** The selected 3:2 hotel, OTA, and guest model is shown
   without crop or distortion. The oxide second-stay return path remains visible.
6. **Desktop uses an attached working paper.** The docket stays in the hero's right column and
   overlaps only 16px of the drawing's blank top edge. The drawing spans the two content columns.
7. **Mobile preserves the same hierarchy.** The docket remains inset; the full drawing bleeds
   through the page gutters. The main model and oxide return path stay discernible. Small notes
   may become texture; making every annotation readable requires a separate mobile composition.
8. **Each episode receives its own model.** Future illustrations may change subject and internal
   composition, but they keep this rough, intimate, back-of-the-napkin visual language.

## Reference implementation

- Review surface: [`index.html`](./index.html) with `surface=home`, `view=focus`,
  `palette=boundaryLedger`, and `device=desktop`.
- Runtime treatment and responsive behavior: [`app.js`](./app.js).
- Locked reference illustration: [`assets/episode-006-hotel-working-model.jpg`](./assets/episode-006-hotel-working-model.jpg).
- Underlying source: [`../artboards/B4-homepage.html`](../artboards/B4-homepage.html), intentionally
  unchanged by this exploration.

Signal Ledger, the clean-layout study, and the photographic Working Plate remain historical
alternatives. They are not forward authority and are not silently merged into Boundary Ledger.

## Not production or publication approval

This is a visual-direction lock inside an isolated design exploration. It does not approve token
promotion, production implementation, deployment, episode claims, specimen copy, sources, Canvas
content, URLs, scheduling, or publication. Content OS issue structure remains separate from OE and
is outside this lock.

## Change control

- Refinements may proceed when they preserve every frozen invariant.
- A change to the palette roles, illustration language, docket relationship, crop rule, or
  responsive hierarchy requires an explicit owner unlock or replacement decision.
- Moving this direction into production requires its own scoped implementation and verification.
