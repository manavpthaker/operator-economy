# Wave 2 build packet A · Shots 01–02

## Contract

- Experiment: `BC-REHEARSAL-001`; 1920×1080, 30 fps; HyperFrames `0.8.4`; GSAP already loaded by the root.
- Owned scene outputs: `shot-01.html` and `shot-02.html` plus one motion-map JSON for each.
- Each HTML file is a HyperFrames sub-composition: one bare `<template>` containing `<style>`, markup, and `<script>`; inner ID and timeline key exactly `bc-rh-001-shot-01` or `bc-rh-001-shot-02`.
- Internal root: `id="root"`, `data-start="0"`, explicit local duration, `data-width="1920"`, `data-height="1080"`. Style the root only through `#root`; put full-frame fill on a child.
- One synchronous paused GSAP timeline per file. Use `fromTo` or timeline `set`; no `from`, clocks, randomness, repeat, network, async setup, or tweened layout properties.
- Use `assets/fonts/...` URLs because transported styles resolve from project root. No media beyond local ticket slates.
- Do not create `call-tag-red`, `work-order-card`, `proof-pin`, their labels, their state tabs, or any alternate customer/outcome token. The canonical root owns those persistent objects.
- Provide invisible, uniquely prefixed screen anchors for root integration: `s01-tag-entry`, `s01-tag-settle`, `s01-card-anchor`, `s02-tag-entry`, `s02-tag-settle`, `s02-card-anchor`. Anchors are authored coordinates, not inferred layout.
- Static DOM represents the readable settle frame. Initial animation states are declared in GSAP, not CSS transforms.

Shared palette/type/anti-rules are the pinned `hyperframes/frame.md`. No Boska headline is required in either scene. No footer explanation, dashboard, screen UI, full sentence, or in-frame reviewer note.

## Shot 01 · `bc-rh-001-shot-01`

- Local duration: `13.64` seconds. Locked absolute window: 0.000–13.640, words 0–33.
- Primary relation: unanswered physical phone → one permissioned signal; work-order remains empty.
- Scene-owned geometry: paper grid fill; `AST-REALITY-001` full-height left placeholder x=0–650; neutral service-phone silhouette x=930,y=335,w=360,h=400; one physical time stamp x=760,y=248; two ring arcs; separate `NO GUARANTEE` stamp x=1390,y=790.
- Root anchors: tag entry x=1040,y=500; tag settle x=700,y=505; card x=1590,y=300.
- Scene timeline, local seconds:
  - 0.150: time stamp and two ring arcs reveal in ≤0.35s.
  - 2.630: phone contact mark registers; root will move the tag, so do not create a surrogate.
  - 4.680: ring arcs fade completely in 0.18s and never return.
  - 6.900: `NO GUARANTEE` stamps once with opacity + ≤12px y, `power2.out`; no scale pop.
  - 10.980: a small contact notch on the tag-settle anchor highlights once, indicating where the root permission tab attaches.
  - Settle is motionless from 11.600 through 13.640.
- Ticket slate must read `HUMAN CONTEXT PLATE MISSING` and `AST-REALITY-001 · SYNTHETIC PLACEHOLDER`. No invented person, home, company, face, phone number, UI, logo, or booking.
- Acceptance: at settle, phone/tag relationship is dominant, `NO GUARANTEE` is separate from the card, and no scene-owned element resembles a second tag/card.

## Shot 02 · `bc-rh-001-shot-02`

- Local duration: `12.73` seconds. Locked absolute window: 13.640–26.370, words 34–69.
- Primary relation: same tag becomes unprioritized and stranded on ATTENTION while customer continuation exits right.
- Scene-owned geometry: paper grid; three overlapping voicemail sheets centered x=560–1340; neutral continuation arrow from x=1120 to offscreen right at y=310; bridge rule y=760 with ATTENTION left and ACTION right; a real center gap; `AST-DISPATCH-002` printed on top sheet.
- Root anchors: tag entry x=760,y=420 exactly matching Shot 01 settle; tag settle x=610,y=620 above ATTENTION; card x=1590,y=300.
- Scene timeline, local seconds (absolute minus 13.640):
  - 0.000: hard-cut composition already established; no entrance wipe.
  - 2.220: voicemail sheets translate 28–64px over the tag anchor in a restrained 0.55s stagger; never fully cover the red root tag.
  - 4.440: continuation arrow makes one rightward pass and exits by local 7.00; no customer icon or blame label.
  - 7.400: `RELATIONSHIP` label registers beneath the bridge.
  - 10.050: bridge halves separate by 64px in y and 34px in x, creating the physical gap; `power2.inOut`, no camera movement.
  - Hold still from 10.650 through 12.730.
- No inbox UI, badge, transcript, notification, phone screen, competitor, angry customer, or dashboard treatment.
- Acceptance: the bridge gap is obvious mute; root tag settle anchor points right toward absent ACTION; Shot 02 exit and Shot 03 entry will be identical at x=610,y=620.

## Motion maps

Each JSON must record composition ID, local duration, event list with local time / verb / selectors / property/ease, persistent anchors with exact x/y, static-hold interval, registry/rule citations (`authored-straight-translation` or `none`), and negative checks. No narration parsing or runtime asset choice.
