# Wave 2 build packet B · Shots 03–04

## Contract

- Experiment: `BC-REHEARSAL-001`; 1920×1080, 30 fps; HyperFrames `0.8.4`; GSAP already loaded by the root.
- Owned scene outputs: `shot-03.html`, `shot-04.html`, and one motion-map JSON for each.
- Each file is a transported sub-composition with one bare `<template>` containing all styles, markup, and script. Composition IDs/timeline keys: `bc-rh-001-shot-03`, `bc-rh-001-shot-04`.
- Inner `#root` has data-start 0, exact local duration, 1920×1080. Full-frame background is a child. One synchronous paused timeline; `fromTo`/timeline sets only; no clocks, random, loops, network, async, UI logic, or layout-property tweens.
- Use `assets/fonts/...` URLs. Prefix every non-root ID `s03-` or `s04-`.
- Never create `call-tag-red`, `work-order-card`, or `proof-pin`; root owns those persistent identities and their state text. Provide authored invisible anchors only.
- Static DOM is the settle state. Measured SVG route lengths come from `getTotalLength()` synchronously, using the fully read `svg-path-draw` rule; every line lands on a real node and then holds with no drift.
- Blueprint Cinema direction overrides registry defaults: no flowchart block, equal node cards, cursor, ambient motion, pullback, or message UI.

## Shot 03 · `bc-rh-001-shot-03`

- Local duration: `7.83` seconds. Absolute: 26.370–34.200, words 70–86.
- Primary relation: pinned source field verifies the persistent tag and changes its route through capture/classify/acknowledge.
- Scene-owned geometry: navy 48px static drafting grid; one unboxed rail y=620; CAPTURE x=480–780, CLASSIFY x=780–1080, ACKNOWLEDGE x=1080–1380 as verb stamps, not cards; physical source sheet x=1210,y=120,w=590,h=430; extracted `20:47 VERIFIED` chip; exact warning across the sheet.
- Required exact warning: `SYNTHETIC TEST FIXTURE — NOT EVIDENCE`, minimum 38px in full source and 28px in collapsed pin state.
- Root anchors: tag entry x=610,y=620 exactly matching Shot 02; capture x=630,y=620; classify x=930,y=620; acknowledge x=1230,y=620; card x=1580,y=580; proof pin x=1560,y=120.
- Timeline local seconds:
  - 0.000: root tag match-cut anchor exists; surrounding navy cuts on with no wipe.
  - 1.430: source context reveals as a physical sheet in 0.30s.
  - 2.050: capture contact mark resolves.
  - 3.500: only `call_time,20:47` highlight fills dark gold.
  - 3.990: `20:47 VERIFIED` chip translates directly from highlighted row toward the tag anchor; no duplicate call tag.
  - 4.970: classify route segment draws by measured dash offset; `UNCERTAIN` registration area activates for root.
  - 5.880: acknowledge segment draws; one `ACKNOWLEDGED` state stamp appears, no reply copy or bubble.
  - 6.830: source sheet collapses in place to a right-edge pin while keeping the exact warning; hold to 7.830.
- Proof choreography must remain source context → highlight → extract → attach → route change → pinned source. The tag already carries 20:47; the extracted chip therefore says `20:47 VERIFIED` and proves a field match rather than inventing new identity.
- Acceptance: no box workflow, no overlapping verb typography, warning readable at 480×270, source is supporting rather than equal focal mass, and no card/tag surrogate.

## Shot 04 · `bc-rh-001-shot-04`

- Local duration: `5.68` seconds. Absolute: 34.200–39.880, words 87–100.
- Primary relation: uncertain tag physically stops until a human placeholder releases the barrier; offer appears only afterward.
- Scene-owned geometry: navy/paper boundary; rail y=510; barrier x=1040,y=250,w=28,h=510 split into upper/lower pieces; HOLD plate; hand-shaped `AST-OPERATOR-003` conspicuous placeholder physically contacting barrier/tag anchor; neutral NEXT AVAILABLE SLOT tab; exact right-edge source-pin warning.
- Root anchors: tag entry/held x=880,y=510; tag released x=1250,y=510; card x=1550,y=300; proof pin x=1560,y=120.
- Timeline local seconds:
  - 0.000: tag held anchor is against closed barrier; HOLD visible; slot tab is fully retracted and not legible.
  - 2.140: human placeholder enters from below/right by ≤90px and rotates the context inspection plate 4° then returns to 0; it touches the barrier and tag anchor.
  - 3.440: RELEASE stamp appears by human contact; barrier upper/lower pieces move apart over 0.35s.
  - 3.680: only after RELEASE is visible, slot tab extends right over 0.45s; no date, time, availability, or UI.
  - Tag remains motionless from local 0.000 to 3.440; root performs its post-release move.
  - Hold final state from 4.400 through 5.680.
- The scene must expose two review snapshots: action/HOLD before local 3.44 and consequence/RELEASE after local 3.68. Do not combine unresolved uncertainty with an offered card in one representative settle.
- Acceptance: pre-release snapshot shows a closed barrier and no offer; post-release route exists only because the human placeholder acts; exact warning remains pinned; no floating review UI or autonomous elapsed-time release.

## Motion maps

Each JSON records composition ID, local duration, event list, selector/property/ease, root-anchor coordinates, SVG measured-path rule use, exact no-motion hold, warning selector and exact text, and negative checks. No narration parsing.
