# Wave 1 evidence, continuity, business-logic, and cognitive-load critique

Experiment: `BC-REHEARSAL-001`  
Work order: `wave1-evidence-continuity-critic`  
Review basis: the seven hash-pinned inputs only, including visual inspection of `hyperframes/shot-board/static-shot-board.png` at original resolution.

## Verdict

The critique is complete, but the packet is not approval-ready. The direction documents contain the intended permission, human-review, decline, evidence, and measurement safeguards; the static shot board does not consistently make those safeguards observable. Four blocking findings prevent this board from serving as an unambiguous implementation reference.

This review claims no gate approval and makes no production-state change.

## Blocking findings

### B1 — Shot 04 visually places an offer beyond an unresolved uncertainty gate

References: static shot board, `SHOT 04 · 00:34.200–00:39.880`; `direction/visual-plan.json`, unit `shot-04-human-gate`; `direction/SEQUENCE-SHOT-DIRECTION.md`, Shot 04 observable review tests.

The direction contract is correct in sequence: the `UNCERTAIN` tag must stop, a human action releases it at 37.640, and only then may a neutral slot extend at 37.880. The board's representative composition shows `CALL-R01 / UNCERTAIN` still left of the closed amber barrier while the work-order card on the far side already reads `OFFERED`. The nearby `HUMAN REVIEW / RELEASE` slate describes an intended operation, but it does not resolve the simultaneous pre-release and post-release business states.

As drawn, a viewer can reasonably infer that the system has offered a slot while the uncertain tag is still held. The board therefore cannot verify the required invariant, “uncertainty cannot reach slot offer before human release.” A safe representative frame must be internally one state or the other: unresolved tag plus non-offered card, or visibly released tag beyond the gate plus offered card.

### B2 — The exact synthetic-fixture warning and proof pin are not persistent

References: static shot board, Shots 03–07; `direction/world.json`, object `fixture-missed-call-log` and evidence `ev-fixture-log`; `direction/SEQUENCE-SHOT-DIRECTION.md`, Shots 03–07 evidence behavior.

Shot 03 introduces source context and displays the exact required warning, `SYNTHETIC TEST FIXTURE — NOT EVIDENCE`. Shot 04 abbreviates that disclosure to `SYNTHETIC / NOT EVIDENCE`. Shots 05 and 06 do not show the fixture proof pin at the directed upper-right position. Shot 07 reintroduces the exact warning as a detached lower-center box rather than preserving the same pin and screen position.

This breaks both the exact-warning contract and the persistent-source chain. The direction requires the source to collapse to a labeled pin after extraction and remain pinned through the gate, branch, principle, and measure. A disclosure that is abbreviated, absent for two shots, and later recreated elsewhere is not one persistent evidence object.

### B3 — The call tag and work-order card cannot be traced through all seven shots under their declared stable identities

References: static shot board, all seven shots; `direction/episode-engine.json`, `persistent_objects`; `direction/world.json`, objects `call-tag-red` and `work-order-card`; `direction/SEQUENCE-SHOT-DIRECTION.md`, sequence contract and shot-boundary responsibilities.

The declared stable call-tag identity is color plus `CALL-R01` plus `20:47`. The board carries `CALL-R01 / 20:47` in Shots 01–03, replaces the time with `UNCERTAIN` in Shot 04, replaces it with `REVIEWED` in Shots 05–06, and restores `20:47` in Shot 07. State may be added to the tag, but it cannot substitute for a stable identity field if the tag is meant to prove continuity.

The work-order card is visually similar across shots, but its declared stable identifier `WO-R01` is never visible on the board. Its state language also drifts from the directed `EMPTY → OFFERED → SCHEDULED → MEASURED` chain to `EMPTY → OFFERED → BOOKED`, with `BOOKED` retained in the final measure. In addition, the Shot 05 tag/card lockup is not inherited intact in Shot 06, and Shot 07 separates the tag from the card despite the direction requiring the booked attachment relationship to persist.

The underlying documents also contain a deterministic-state conflict in Shot 05: `visual-plan.json` enters with the card `offered`, but the 41.080 event says the card “remains empty,” and the 45.110 event changes it from `EMPTY` to `SCHEDULED`; the shot-direction document instead correctly says `OFFERED` to `SCHEDULED`. Until both the board and the direction use one stable identity and state vocabulary, object continuity cannot be independently verified.

### B4 — The synthetic booked outcome is not behaviorally attached to its disclosure

References: static shot board, Shots 05–07; `direction/asset-tickets.json`, ticket `AST-OUTCOME-004`; `direction/SEQUENCE-SHOT-DIRECTION.md`, Shots 05 and 07.

`AST-OUTCOME-004` requires a rehearsal card with fictional ID `WO-R01` that is clearly labeled `SYNTHETIC WORK ORDER / NOT EVIDENCE`. In Shot 05, the board places an `AST-OUTCOME-004 / SYNTHETIC PLACEHOLDER` note in an isolated upper-left box while the far-right work-order card itself reads only `WORK ORDER / BOOKED`. The note is not attached to the card, the required fictional card ID is absent, and Shots 06–07 continue to show the undislosed `BOOKED` card.

That separation permits the visible booked card to be read as an observed outcome rather than a rehearsal object. The source-fixture warning does not cure this: it governs the call-log fixture, while the outcome card has its own ticket-level disclosure contract. The outcome disclosure must travel with the card on every frame in which the synthetic result object is visible.

## Major findings

### M1 — The decline terminal is stated, but not causally connected to the offered signal

References: static shot board, Shot 05; `direction/world.json`, edges `edge-decline-stop` and `edge-accept-book`; `direction/SEQUENCE-SHOT-DIRECTION.md`, Shot 05 layer geometry and observable review tests.

The board does show `DECLINE → STOP / NO PURSUIT`, and no path leaves that box. However, it floats below and left of the horizontal accepted rail rather than branching from the same fork. The only connected route visible is the reviewed tag moving right toward `ACCEPTED → SCHEDULED` and the booked card. The viewer must trust prose to know the decline note governs the same offer. The directed Y-shaped rail should visibly connect the offered node to both mutually exclusive outcomes, with the decline branch terminal and the single tag occupying only the demonstrated branch.

### M2 — Shot 03's proof choreography is too dense to make extraction causally legible

References: static shot board, Shot 03; `direction/visual-plan.json`, unit `shot-03-route-construction`; `direction/SEQUENCE-SHOT-DIRECTION.md`, Shot 03 action and consequence frames.

Within 7.83 seconds, the shot must introduce full source context, preserve the warning, highlight one field, extract `20:47`, attach it to the tag, traverse capture/classify/acknowledge, add `UNCERTAIN`, keep the work card empty, and collapse the source to a pin. The board compresses the fixture, three nodes, tag, rails, and empty card into one composition; the fixture overlaps the card region and the extraction chip is not visible as a distinct object.

There is also a causal-legibility problem: the tag already displays `20:47` in Shots 01 and 02, so attaching `20:47` in Shot 03 does not create an observable before/after change. The direction says the source field changes tag state and therefore routing behavior, but the board only repeats a value the tag already owns. The proof beat needs a visible attachment or verification state that changes behavior without pretending the call time was unknown until the fixture appeared.

### M3 — Shot 06 does not carry its assigned operating-principle responsibility

References: static shot board, Shot 06; `direction/visual-plan.json`, unit `shot-06-blueprint-principle`; `direction/SEQUENCE-SHOT-DIRECTION.md`, Shot 06.

The directed viewer takeaway is “preserve, route, and judge—not automate every response.” The board instead leads with `PRESERVE THE SIGNAL.` and shows compact nodes, including human judgment, but it does not show the `AUTOMATE ALL` bypass, its human removal, or a clear `ROUTE` registration. It also omits the required source pin and fails to inherit the booked tag/card lockup exactly.

A static board cannot prove motion, but its representative before/after choice must at least expose the intended contrast and settled spatial relationships. The current panel reads as another system summary, not the specific rejection of straight-through automation assigned to this shot.

### M4 — Shot 07 does not show the declared measurement state and overloads the five-second close

References: static shot board, Shot 07; `direction/visual-plan.json`, unit `shot-07-one-week-measure`; `direction/SEQUENCE-SHOT-DIRECTION.md`, Shot 07.

The board uses four columns—`CALL`, `REPLY ELAPSED`, `APPOINTMENT BOOKED`, and `RESULT / TEST, NOT CLAIM`—while the direction calls for three process endpoints plus seven day ticks and a closing bracket. The work-order card remains `BOOKED` instead of changing to `MEASURED`, and the call tag is no longer physically attached to it. The extra `RESULT / TEST, NOT CLAIM` column repeats the synthetic warning's honesty function while competing with the actual measure.

This shot has only 5.361 seconds. The directed `MEASURED` state occurs at 60.270–60.650, leaving about 0.76 seconds of final hold after the last state change. That is not a credible phone-scale reading window for the headline, seven ticks, three endpoints, card identity/state, and exact source warning. The close should prioritize the three causal endpoints and persistent objects; the honesty disclosure must remain, but a second explanatory result column is avoidable repetition.

### M5 — The board makes asset-ticket annotations compete with business-state objects

References: static shot board, Shots 01, 04, 05, and 07; `direction/asset-tickets.json`, tickets `AST-REALITY-001`, `AST-OPERATOR-003`, and `AST-OUTCOME-004`.

Ticket slates are necessary in a rehearsal, but their visual attachment is inconsistent. Shot 01's reality slate is clearly a missing plate; Shot 04's human-review slate sits within the action zone; Shot 05's outcome slate is detached from the outcome card; Shot 07's fixture warning floats separately from both source context and the outcome card. This forces the viewer to infer which disclosure governs which synthetic object. Ticket labels should be visually parented to the placeholder or card they qualify, particularly where an apparent booking is shown.

## Minor findings

### m1 — State vocabulary drifts across artifacts

References: `direction/world.json`, `direction/visual-plan.json`, `direction/SEQUENCE-SHOT-DIRECTION.md`, and static shot board, Shots 05–07.

`scheduled`, `booked`, `measurable`, and `measured` are used as overlapping labels. They are related but not interchangeable states. A single card-state vocabulary would reduce cognitive translation and make the final measurement transition testable.

### m2 — The Shot 01 `NO GUARANTEE` qualifier is visually embedded in the work-order card

References: static shot board, Shot 01; `direction/SEQUENCE-SHOT-DIRECTION.md`, Shot 01 consequence frame.

The direction calls for `NO GUARANTEE` as a separate editorial stamp below the empty card. The board places it within the card's field. Keeping it separate would more clearly qualify the value claim rather than look like a work-order state.

### m3 — Board-review annotations should remain non-rendering metadata

References: static shot board labels `READABLE HOLD`, `TAG STOPS 1.7s`, `ONE MOTIVATED PULLBACK`, and `FINAL HOLD TO 01:01.411`.

These are useful review notes, but they add small, high-contrast text to already dense panels. If the board is also used as a visual implementation reference, mark them explicitly as non-rendering annotations so they are not mistaken for authored scene text.

## Acceptance-check disposition

- Pinned hashes: pass. All seven recomputed SHA-256 values exactly match the work order.
- Persistent call tag and work-order card: fail. Stable fields and attachment/state continuity drift in Shots 04–07.
- Human release before slot offer: fail on the representative board. The direction encodes the correct order, but Shot 04 visually combines an unresolved tag with an offered card.
- Decline terminates pursuit: partial. The stop box is terminal and says `NO PURSUIT`, but it is not visibly connected to the same decision fork.
- Synthetic fixture/source chain: fail. Shot 03 preserves source context and the exact warning, but behavioral extraction is not legible and the exact warning/pin are not persistent through Shots 04–07.
- Viewer inference, density, shot boundaries, and repetition: reviewed. Blocking and major failures are enumerated above.
- Approval/state authority: pass. No approval or state change is claimed.

## Review boundary

The static board is treated as the representative visual state for each shot. Where the direction prose specifies a safe temporal sequence but the representative panel combines incompatible phases, the finding is against verifiability of the pinned board, not an assertion about an unreviewed animation. No runtime composition, non-pinned fixture file, sourced asset, or production render was reviewed.
