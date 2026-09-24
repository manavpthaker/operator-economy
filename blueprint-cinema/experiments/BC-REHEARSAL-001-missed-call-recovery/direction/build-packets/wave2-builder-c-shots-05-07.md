# Wave 2 build packet C · Shots 05–07

## Contract

- Experiment: `BC-REHEARSAL-001`; 1920×1080, 30 fps; HyperFrames `0.8.4`; root provides GSAP.
- Owned scene outputs: `shot-05.html`, `shot-06.html`, `shot-07.html`, plus one motion-map JSON each.
- Transported sub-compositions: one bare `<template>` holding styles, markup, and script. IDs/timeline keys exactly `bc-rh-001-shot-05`, `bc-rh-001-shot-06`, `bc-rh-001-shot-07`.
- Inner `#root`: data-start 0, exact local duration, 1920×1080. Background on child. Synchronous paused GSAP timeline; no clocks/random/repeat/network/async/layout tweens.
- Use `assets/fonts/...`; prefix non-root IDs by shot. Static DOM is settled end state; initial states in `fromTo`/timeline `set`.
- Do not create `call-tag-red`, `work-order-card`, `proof-pin`, alternate tokens, or state labels for those objects. Provide root anchors only.
- Route/bracket draws use measured `getTotalLength()` dash geometry from `svg-path-draw`, no optional drift. One pullback in Shot 06 is the only camera-scale change and must remain ≤12%.
- No split-screen, infographic, dashboard, framed map, equal card grid, headline/list composition, celebration, green glow, fake result, or CTA.

## Shot 05 · `bc-rh-001-shot-05`

- Local duration: `7.80` seconds. Absolute: 39.880–47.680, words 101–119.
- Primary relation: one connected offer fork shows terminal decline, then the one real tag takes accepted route and makes the card scheduled.
- Geometry: navy system field; one Y-shaped authored SVG from fork x=940,y=480 to STOP x=700,y=760 and card contact x=1410,y=430; physical STOP terminal; suppression bar; branch labels DECLINE/ACCEPT; exact source pin at x=1560,y=120. Do not create a detached outcome slate.
- Root anchors: tag entry/fork x=920,y=430; tag scheduled x=1360,y=430; card x=1410,y=250; proof pin x=1560,y=120.
- Local timeline:
  - 0.000: hard cut, fork already readable, both route strokes hidden by measured dash offset.
  - 1.200: decline route draws to STOP; STOP border registers; root tag does not move.
  - 2.070: suppression bar closes behind STOP; no route leaves STOP.
  - 2.720: decline route dims but remains visible as one possible terminal.
  - 3.170: accepted route draws right; root moves the only tag.
  - 5.230: card-contact notch registers; root changes card `OFFERED → SCHEDULED` and docks tag.
  - 7.090: `MEASURABLE` registration line draws beneath card; hold to 7.800.
- Acceptance: connected fork reads mute; STOP has no continuation; only one root tag occupies accepted route; root card's attached disclosure qualifies every visible scheduled state.

## Shot 06 · `bc-rh-001-shot-06`

- Local duration: `8.37` seconds. Absolute: 47.680–56.050, words 120–140.
- Primary relation: human judgment remains physically inside the route after an `AUTOMATE ALL` bypass is removed.
- Geometry: one continuous unboxed rail with operation stamps CAPTURE/CLASSIFY/ACKNOWLEDGE/HUMAN JUDGMENT/OFFER/STOP-BOOK; barrier at human gate; a dashed straight-through bypass labeled `AUTOMATE ALL`; operator-hand placeholder contacting and removing that bypass; exact source pin fixed at right. No border framing the overview.
- Root anchors: inherited tag/card dock x=1360,y=430 and x=1410,y=250; gate x=1040,y=510; proof pin x=1560,y=120.
- Local timeline:
  - 0.000: cut to a 1.12-scale close fragment centered on the gate and inherited tag/card dock.
  - 0.820: wrapper decelerates once from scale 1.12 to 1.00 over 0.85s, `power2.out`, same center; no pan/rotation and no more than 12%.
  - 1.230: operator hand physically pulls the dashed bypass down/out; `AUTOMATE ALL` receives a single brick strike and settles absent.
  - 3.310: `PRESERVE` attaches beside root tag anchor with opacity + ≤12px y.
  - 4.840: `ROUTE` draws along the real rail using measured dash offset.
  - 6.430: `JUDGMENT` registers beside barrier; all motion ends by 6.970 and holds to 8.370.
- The pullback reveals causal context once; it is not a Prezi journey and does not visit nodes. The inherited tag/card lockup never resets or separates.
- Acceptance: no boxed map; bypass removal is the consequence, not a decorative transition; source pin exact; final 1.4s is still.

## Shot 07 · `bc-rh-001-shot-07`

- Local duration: `5.361354` seconds. Absolute: 56.050–61.411354, words 141–157.
- Primary relation: one bounded week connects CALL, REPLY, and BOOKED APPT to the same docked tag/card without inventing a result.
- Geometry: paper proof bench; one measurement baseline/bracket y=690 spanning x=250–1540; seven equal unlabeled day ticks; exactly three labels CALL x=250, REPLY x=960, BOOKED APPT x=1450; a thin leader from CALL label to the `20:47` field on the one docked root tag; exact source pin remains frame right. No fourth result column.
- Root anchors: inherited tag/card dock x=1360,y=430 / x=1410,y=250; card stays at frame right and becomes MEASURED; proof pin x=1560,y=120.
- Local timeline:
  - 0.000: hard cut while dock and proof pin preserve screen position.
  - 1.060: bracket and seven ticks draw from measured SVG lengths; no count/rate.
  - 2.630: MEASURED contact mark registers for the root card state change.
  - 3.450: CALL label and leader reveal; 3.840 REPLY; 4.220 BOOKED APPT and bracket close.
  - All motion ends by local 4.220; hold the complete frame through 5.361354.
- Acceptance: only three endpoints, warning readable at 480×270, no result/ROI/count, tag remains docked, card-state text remains unobscured, and final hold exceeds 1.14s.

## Motion maps

Each JSON records composition ID, local duration, events, selectors/properties/eases, persistent anchors, measured-SVG details, camera-scale amount for Shot 06, no-motion hold, warning selector/text, and negative checks. No narration parsing or runtime asset selection.
