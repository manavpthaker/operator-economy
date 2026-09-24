---
format: 1920x1080
duration: 90s
message: "The OTA can be useful acquisition; the recovery opportunity is a guarded direct path for the next appropriate booking."
arc: story-explainer with process
audience: "Independent hotel owners and general managers"
mode: autonomous
music: none
captions: none
---

## Video direction

Treat the first 90 seconds as a polished editorial motion essay and a sequence of composed slides, never a UI demo or a tour of the complete network map. The persistent visual vocabulary is deliberately small: one brass key tag, one guest token, one independent-inn silhouette, one OTA gate, and one operator-side ledger. Reuse those objects only when the narration needs them; otherwise let typography own the frame. Apply the remixed Cobalt Grid system exactly from `frame.md`: cream paper, ink structure, restrained ledger gold, Boska display, Supreme body, Fragment Mono labels, graph grid, and hard rules.

Every reveal follows the locked narration cue and continues into the back half of its frame. Use smooth long-tail settles, not bounce. Allocate stillness to Frames 5 and 6 so the show identity and episode title can actually be read; all other frames develop sequentially and then hold. Keep the bottom 17% clear even though captions are disabled. Never use a vendor logo, generated platform interface, fake source document, stock, AI imagery, music, lazy breathing, decorative camera drift, a full-map overview, or many independently floating elements. The prohibited failure modes are slideshow (everything appears immediately, then freezes) and screensaver (everything moves without teaching).

## Frame 1 — The same guest

- scene: A physical brass room key and one guest token cross a cream ledger twice while the words SAME GUEST grow to dominate the frame.
- voiceover: "Hotels keep paying to meet the SAME guest. More than 60 percent of independent-hotel"
- duration: 8.284s
- poster: 5.0s
- transition_in: cut
- status: animated
- src: compositions/frames/01-same-guest.html
- type: hook
- persuasion: Concretization + counterintuitive claim
- beat: tension and recognition
- blueprint: kinetic-type-beats

narrativeRole: Turn an abstract acquisition problem into one recognizable returning human and one repeated payment.
keyMessage: The hotel keeps paying to encounter a guest it has already served.

- focal: The words SAME GUEST paired with one physical brass room key.
- roles: graph ledger = background · brass key and guest token = foreground subject · PAID AGAIN stamps = supporting consequence.

Adapt: Keep the kinetic-type blueprint's fixed center anchor and beat replacement; replace generic text effects with one key tag crossing the same ledger line twice.

Scene 1 (0.0–2.2s): Only “HOTELS KEEP PAYING” enters in the upper third via per-word staggered reveal (`dynamic-content-sequencing`); a single brass key seats below it on a centered, sparse three-layer composition.
Scene 2 (2.2–5.3s): On “to meet the SAME guest,” SAME GUEST hard-cuts to near-full-frame Boska while the guest token locks to the key; one short gold rule draws beneath the phrase. Camera remains static.
Scene 3 (5.3–8.284s): As “More than 60 percent” begins, the same key crosses a second ledger rule and a second PAID AGAIN stamp lands via discrete state replacement (`discrete-text-sequence`); the repeated-payment read settles and holds.

## Frame 2 — The paid introduction

- scene: The same key tag lands beside a large 60% figure, a restrained SOURCE TICKET label, and a single OTA gate drawn as the useful entrance to the hotel.
- voiceover: "reservations come through online travel agencies, or OTAs. A guest finds the property on"
- duration: 7.524s
- poster: 4.0s
- transition_in: crossfade
- status: animated
- src: compositions/frames/02-paid-introduction.html
- type: social_proof
- persuasion: Statistical proof + frame-then-fill
- beat: comprehension
- blueprint: dataviz-countup

narrativeRole: Quantify the market force without manufacturing a source document or turning the OTA into a villain.
keyMessage: OTA reach is commercially useful and materially important to independent hotels.

- focal: A large “60%+” figure joined to one useful OTA entrance gate.
- roles: 60% figure = foreground subject · OTA gate and inn = supporting mechanism · SOURCE TICKET / VERIFY label = proof boundary.

Adapt: Keep the count-up as the signature move; use a single pixel-stack measure rather than a dashboard or fabricated source card.

Scene 1 (0.0–2.3s): The phrase “INDEPENDENT-HOTEL RESERVATIONS” builds in the upper third; an empty pixel-stack measure appears below in an asymmetric 60/40 layout.
Scene 2 (2.3–5.2s): As “online travel agencies, or OTAs” is spoken, the measure fills and the value-scaled counter (`counting-dynamic-scale`) lands at 60%+; a generic labeled OTA GATE draws on to the right with no brand mark.
Scene 3 (5.2–7.524s): On “A guest finds the property,” the guest token moves through the gate toward the inn, while a conspicuous “SOURCE TICKET · VERIFY BEFORE FINAL” label appears beside the number; the useful entrance holds.

## Frame 3 — The loop back

- scene: A guest token travels from the paid OTA gate to an independent inn, pauses on a completed-stay key tag, then loops back toward the paid gate for the next trip.
- voiceover: "Booking, has a beautiful stay... and returns to Booking next time. Today, I'll"
- duration: 6.381s
- poster: 4.0s
- transition_in: crossfade
- status: animated
- src: compositions/frames/03-loop-back.html
- type: pain_point
- persuasion: Causal chain + demonstration
- beat: tension
- blueprint: spatial-pan-stations

narrativeRole: Show the relationship leak as the motion of one person, not as an abstract network map.
keyMessage: The stay succeeds, but the next booking still routes back through the paid gate.

- focal: One guest token travelling through three oversized stations: OTA GATE → INN → OTA GATE AGAIN.
- roles: guest token = foreground subject · stations and connecting path = midground mechanism · graph grid = background.

Adapt: Keep the spatial-pan signature, but limit the world to three large stations so the viewer sees one journey rather than a network map.

Scene 1 (0.0–2.0s): The camera is locked close on the OTA GATE as “Booking” lands; the guest token enters and the SVG route begins to self-draw (`svg-path-draw`) across a full-width strip.
Scene 2 (2.0–4.2s): A single lateral pan (`viewport-change`) follows the token to the INN; a key tag flips to STAY COMPLETE as “beautiful stay” is spoken.
Scene 3 (4.2–6.381s): The route curves back and the camera lands on OTA GATE AGAIN exactly on “returns to Booking next time”; the second gate becomes the only focal object and holds.

## Frame 4 — Audit before outreach

- scene: The returning loop freezes; an operator opens the hotel's direct destination, runs an audit strip across it, and exposes closed permission and human-review gates before the direct route can light.
- voiceover: "show you how an operator can help the hotel earn that return visit DIRECTLY."
- duration: 5.544s
- poster: 3.2s
- transition_in: crossfade
- status: animated
- src: compositions/frames/04-audit-first.html
- type: product_intro
- persuasion: Before/after + progressive disclosure
- beat: clarity and anticipation
- blueprint: grid-card-assemble

narrativeRole: Glimpse the counter-system while making the audit-first and guarded-path rules visible.
keyMessage: Direct recovery starts by repairing the destination, not by blasting guests.

- focal: A large direct-destination card under an AUDIT strip.
- roles: direct destination = foreground subject · audit and repair checks = supporting proof · permission and human-review gates = guarded future path.

Adapt: Keep the grid-card assembly, but assemble only four load-bearing stages and stop before outreach.

Scene 1 (0.0–1.7s): On “show you how,” an oversized DIRECT DESTINATION card arrives alone in an asymmetric 70/30 frame; its status reads NOT AUDITED.
Scene 2 (1.7–3.8s): The AUDIT then REPAIR strips reveal sequentially into their slots (`center-outward-expansion`, short-path form), and the destination changes to READY via discrete replacement (`discrete-text-sequence`).
Scene 3 (3.8–5.544s): On “earn that return visit DIRECTLY,” closed PERMISSION and HUMAN REVIEW gates appear beyond the repaired destination; only the route up to those closed gates illuminates. Hold with DIRECTLY dominant.

## Frame 5 — Show identity

- scene: The operating diagram clears to the canonical typographic wordmark, The Operator Economy, with Build. Own. Operate. held on the graph-paper field.
- voiceover: "This is The Operator Economy, where we show you how to use AI and"
- duration: 4.825s
- poster: 2.8s
- transition_in: cut
- status: animated
- src: compositions/frames/05-show-identity.html
- type: branding
- persuasion: Distillation
- beat: orientation
- blueprint: titlecard-reveal

narrativeRole: Give the show a distinct identity break between the cold open and the episode premise.
keyMessage: This is The Operator Economy.

- focal: The canonical typographic show identity “The Operator Economy.”
- roles: wordmark = foreground subject · Build. Own. Operate. = supporting line · grid and hairlines = background.

Reproduce: Use the title-card chain's restrained single reveal and allocated stillness.

Scene 1 (0.0–1.1s): The prior mechanism cuts away to the bare cream grid; only a small mono “THIS IS” label appears at the upper third.
Scene 2 (1.1–3.0s): “THE OPERATOR ECONOMY” reveals line by line in Boska with a restrained scale settle (`scale-swap-transition`), filling roughly half the frame.
Scene 3 (3.0–4.825s): “BUILD. OWN. OPERATE.” enters beneath in Fragment Mono; the complete identity holds fully still for legibility.

## Frame 6 — Episode title

- scene: EP006 and Direct Booking Recovery assemble as a restrained editorial title while a small two-part thesis reads FIRST BOOKING: ACQUISITION and NEXT APPROPRIATE BOOKING: DIRECT.
- voiceover: "practical workflows to build and run a one-person business. Today, we're looking at direct-booking"
- duration: 7.532s
- poster: 4.4s
- transition_in: blur-crossfade
- status: animated
- src: compositions/frames/06-episode-title.html
- type: product_intro
- persuasion: Concept announcement + contrast
- beat: clarity
- blueprint: titlecard-reveal

narrativeRole: Name the episode and state its fair operating thesis before the mechanism continues.
keyMessage: EP006 is about recovering the next appropriate booking, not eliminating OTA acquisition.

- focal: “EP006 — DIRECT BOOKING RECOVERY.”
- roles: episode title = foreground subject · fair two-part thesis = supporting contrast · key tag = small continuity marker.

Adapt: Repeat the title-card chain as two calm cards: episode identity, then the fair thesis. No diagram is visible.

Scene 1 (0.0–2.6s): EP006 enters first; DIRECT BOOKING RECOVERY assembles beneath via a restrained per-line reveal, centered with deliberate negative space.
Scene 2 (2.6–5.2s): The title holds while a brass key seats at the lower safe rail; no camera movement.
Scene 3 (5.2–7.532s): A hard card handoff replaces the subtitle with “FIRST BOOKING: ACQUISITION / NEXT APPROPRIATE BOOKING: DIRECT,” revealed one line at a time (`discrete-text-sequence`), then held.

## Frame 7 — Keep the reach

- scene: The first-booking journey resumes on the same editorial stage: OTA discovery opens the inn door, the hotel delivers the human stay, and a commission ledger records the operator-side cost.
- voiceover: "recovery. The idea isn't to replace Booking or Expedia. Small hotels need the reach. The opportunity is to help a hotel turn a guest it met through an OTA"
- duration: 13.416s
- poster: 8.0s
- transition_in: cut
- status: animated
- src: compositions/frames/07-keep-the-reach.html
- type: feature_showcase
- persuasion: Comparison of two jobs + causal chain
- beat: comprehension and fairness
- blueprint: spatial-pan-stations

narrativeRole: Preserve the first-booking acquisition value while separating discovery, service, and economic consequence.
keyMessage: The OTA can introduce the guest; the hotel still delivers the stay and bears the commission.

- focal: A three-station commercial journey: REACH → STAY → COMMISSION LEDGER.
- roles: guest and key = foreground subject · OTA gate and inn = supporting stations · operator-side ledger = economic consequence.

Adapt: Keep the three-stop lateral journey; use large editorial stations and one continuous object rather than a complete system map.

Scene 1 (0.0–3.2s): “THE IDEA ISN'T TO REPLACE” enters, then REPLACE hard-swaps to REACH as the OTA GATE opens; the guest token crosses it on a full-width strip.
Scene 2 (3.2–6.6s): On “Small hotels need the reach,” a lateral camera pan (`viewport-change`) lands at the INN; the guest receives the brass key and the stay node changes to SERVED.
Scene 3 (6.6–10.0s): On “The opportunity,” the route extends beyond the inn toward a faint direct-return destination, but remains gated; the first-booking path stays visibly intact.
Scene 4 (10.0–13.416s): As “met through an OTA” lands, the operator-side COMMISSION LEDGER slides into the 40% rail and records one deduction; guest confirmation is deliberately absent. The economic read holds.

## Frame 8 — After the stay

- scene: The physical key tag completes the stay, then waits at a visible consent handoff; only beyond audit, permission, qualification, and human review does a direct-return line appear.
- voiceover: "into a guest it can welcome back directly. Sure... the first booking may belong to the platform. But the relationship AFTER THE STAY should belong to the property."
- duration: 13.551s
- poster: 8.0s
- transition_in: push-slide LEFT
- status: animated
- src: compositions/frames/08-after-the-stay.html
- type: benefit_highlight
- persuasion: Before/after + progressive disclosure
- beat: conviction
- blueprint: kinetic-type-beats

narrativeRole: Land the episode thesis while preserving permission, qualification, and human judgment as non-bypassable conditions.
keyMessage: A completed stay creates an opportunity—not permission—and the guarded relationship can support a direct return.

- focal: The phrase AFTER THE STAY resolving into a guarded path.
- roles: completed-stay key = foreground subject · AFTER THE STAY type = foreground statement · audit, permission, qualification, human-review gates = supporting conditions.

Adapt: Keep the kinetic statement relay, but let the physical key become a route only after four visible gates assemble.

Scene 1 (0.0–3.0s): “A GUEST IT CAN WELCOME BACK” builds word by word around the completed-stay key; DIRECTLY lands as the dominant word via a hard-cut word swap (`discrete-text-sequence`).
Scene 2 (3.0–6.2s): “THE FIRST BOOKING MAY BELONG TO THE PLATFORM” replaces the line as a calm full-frame statement; the OTA gate stays useful at the left edge.
Scene 3 (6.2–10.2s): On “But the relationship,” AFTER THE STAY takes over near full-frame; below it AUDIT → PERMISSION → QUALIFY → HUMAN REVIEW reveal sequentially in the back half (`dynamic-content-sequencing`).
Scene 4 (10.2–13.551s): Only after all four conditions are visible does a thin direct-return line draw from the key to the hotel; “SHOULD BELONG TO THE PROPERTY” settles and holds. No outreach or booking confirmation activates.

## Frame 9 — The disconnected group project

- scene: One operator stands at center while Google, website, phone, booking system, and follow-up cards arrive from different edges; the same guest waits outside the disconnected handoffs.
- voiceover: "At a ten-to-forty-room hotel, no one person owns that whole journey. One person updates Google. Someone else handles the website. The front desk answers the phone when it can. Guest information sits in the booking system. And follow-up happens... if somebody remembers."
- duration: 22.943s
- poster: 14.0s
- transition_in: push-slide LEFT
- status: animated
- src: compositions/frames/09-disconnected-work.html
- type: pain_point
- persuasion: Rule of three + accumulation + callback
- beat: recognition and concern
- blueprint: overwhelm-surround

narrativeRole: End the 90-second test on the operational problem the full episode will solve: fragmented ownership, not a lack of software screens.
keyMessage: Direct-booking recovery fails because the return journey is a disconnected group project with no accountable owner.

- focal: One operator surrounded by five disconnected work cards and an untouched returning-guest token.
- roles: operator = foreground subject · GOOGLE / WEBSITE / PHONE / BOOKING SYSTEM / FOLLOW-UP cards = accumulating demands · guest token = stranded consequence · graph field = background.

Adapt: Keep the surround blueprint's accumulation and close-in signature, but use operational work cards instead of fake product interfaces or logos.

Scene 1 (0.0–4.2s): “10–40 ROOM HOTEL” and “NO ONE OWNS THE WHOLE JOURNEY” reveal in a split 60/40 layout; a simple operator marker seats at center-right.
Scene 2 (4.2–9.0s): On “One person updates Google” and “someone else handles the website,” two square work cards slide directly into distinct edge positions with short-path smooth settles (`spring-pop-entrance`, no bounce). The operator stays fixed.
Scene 3 (9.0–13.4s): PHONE enters only as “front desk answers the phone” is spoken; a narrow availability meter stops short of full, establishing operational reality rather than UI.
Scene 4 (13.4–18.1s): BOOKING SYSTEM then FOLLOW-UP arrive on their spoken cues; the five cards now surround the operator from all compass points while the returning guest remains outside the handoffs.
Scene 5 (18.1–22.943s): On “if somebody remembers,” every card desaturates except a small unanswered FOLLOW-UP ticket; a thin route from the guest ends before reaching it. The crowded frame holds static—no push-in, no floating cards.
