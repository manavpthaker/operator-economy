# Wave 1 independent art and motion-direction critique

Experiment: `BC-REHEARSAL-001`  
Work order: `wave1-art-motion-critic`  
Review status: complete critique; hold the current art references for correction  
Gate authority: none

## Scope and method

All nine pinned SHA-256 values were recomputed before review and matched the work order. I read the four pinned direction documents and `input-lock.json` in full. I inspected all three 1920x1080 style-frame PNGs and the complete 2400x3100 static shot board at original detail. I also isolated all seven 16:9 shot-board panels and inspected each at 480x270, then inspected the three style frames at 480x270.

This is an independent critique of the pinned direction art. It does not inspect animation implementation, DOM identity, runtime timing, or a rendered animatic, and it does not edit canonical direction.

## Outcome

The written direction is substantially stronger than the pinned art. The direction describes a physical, object-led film with one persistent call tag, one outcome card, a causal rail, one designed handoff, and hard cuts. The pinned images repeatedly turn that system into presentation grammar: headings plus boxes, boxed workflows, before/after states, a map-like pullback, and an infographic close. Several frames also contradict explicit continuity, state-language, evidence-labeling, and phone-legibility requirements.

The critique packet is complete, but the art references are not safe to treat as an implementation-ready visual authority until the blocking findings below are resolved.

## Blocking findings

### B1. The persistent call-tag identity is visibly broken

- `hyperframes/style-frames/03-gate-outcome.png` shows two red `CALL-R01` tags at once: one `UNCERTAIN` tag before the gate and another `20:47` tag over the scheduled work order. This is the exact duplicate-tag condition prohibited by visual anti-rule 17 and collapses conditional time into a simultaneous before/after diagram.
- `static-shot-board.png`, Shot 04 removes `20:47` from the tag and substitutes `UNCERTAIN`; Shots 05 and 06 substitute `REVIEWED`; Shot 07 restores `20:47`. State is being rewritten into the persistent object's core label instead of attaching as a separate state tab, so label continuity cannot survive a mute or label-hide test.
- `static-shot-board.png`, Shot 05 does not visibly clip the tag into the card, and Shot 06 again places the tag at the rail center while the card remains at frame right. The exact Shot 05-to-06 tag/card lockup required by direction is therefore reset rather than inherited.

Required correction in art, not canonical direction: show one brick tag only; keep `CALL-R01 / 20:47` unchanged; attach `UNCERTAIN`, `REVIEWED`, or equivalent state as subordinate physical tabs; carry the Shot 05 booked lockup intact into Shot 06.

### B2. Synthetic-source labeling and proof-pin continuity fail the explicit contract

- `hyperframes/style-frames/02-system-proof.png` correctly carries the exact line `SYNTHETIC TEST FIXTURE — NOT EVIDENCE`, and that warning remains readable at 480x270. This is the reference to preserve.
- `static-shot-board.png`, Shot 04 abbreviates the pin to `SYNTHETIC / NOT EVIDENCE`, omitting `TEST FIXTURE —`. The direction requires the exact line on every full or partial fixture display; abbreviation is explicitly disallowed.
- At 480x270, the source rows and warning in Shot 03 and the bottom-center warning in Shot 07 are not reliably readable without magnification. This fails the phone-size approval test for the synthetic warning.
- The proof pin does not remain pinned at frame right: it becomes a separate upper-left asset slate in Shot 05, is absent as a source pin in Shot 06, and moves to bottom center in Shot 07. That breaks the pinned-source continuity invariant and weakens the source-to-claim chain.

Required correction in art: retain the exact full warning at a phone-readable size and preserve one source pin at frame right from Shot 03 through Shot 07.

### B3. The outcome and measurement states contradict the direction contract

- `static-shot-board.png`, Shot 05 labels the card `BOOKED` while a separate box says `ACCEPTED → SCHEDULED`. The canonical card state is `SCHEDULED`, and the tag must physically cause that state change. Splitting cause and state into two text boxes makes the payoff explanatory rather than observable.
- Shot 05's `DECLINE → STOP / NO PURSUIT` box is visually disconnected from the rail. It does not show a down-left branch terminating at a hard `STOP`, while the accepted branch is also not a clear rightward tag-to-card route. Screen direction and binary consequence cannot be understood mute.
- Shot 06 still says `BOOKED`, rather than preserving the `SCHEDULED` card/tag lockup. Shot 07 also says `BOOKED`, although the settle state is required to become `MEASURED`.
- Shot 07 introduces a fourth equal endpoint, `RESULT / TEST, NOT CLAIM`, despite the specified three endpoints `CALL`, `REPLY`, and `BOOKED APPT`. The extra result stage implies an unproven result category and turns a bounded process measure into a four-step infographic.

Required correction in art: make `STOP` a connected terminal; move the one real tag only on acceptance; change the physical card to `SCHEDULED`; carry that lockup into Shot 06; close Shot 07 with the card visibly `MEASURED` and only the three specified endpoints.

### B4. The single designed handoff and later cut inheritance are not preserved by the board

- `static-shot-board.png`, Shot 02 leaves the tag high and embedded at the voicemail stack, not settled above `ATTENTION` and pointing toward the missing action side. Shot 03 relocates it to the middle of a three-box rail. Read side by side, the only designed handoff is a deck reset, not an identity-, x-direction-, and velocity-preserving match.
- Shot 05-to-06 fails the required exact tag/card-lockup inheritance, as noted in B1.
- Shot 06-to-07 also resets the proof pin from the right-edge source position to bottom center.

The hard-cut strategy is valid in the written direction, but these pinned compositions do not supply the common object positions needed to execute it. The board should show the exact exit/entry object geometry at Shots 02/03, 05/06, and 06/07 before motion is approved.

### B5. The pinned art repeatedly reads as slides, a dashboard, a Prezi map, or beginner workflow motion

- `01-reality.png` and board Shot 01 read as a presentation slide: a dominant headline, a large explanatory copy box, a centered phone icon, a call-tag card, a work-order card, and a footer assertion distributed across the frame. The physical event is described by layout rather than staged as one relationship.
- `02-system-proof.png` and board Shot 03 read as a workflow dashboard: three equal boxed nodes, a large CSV panel, a top label, and a footer process sentence. The likely motion grammar is sequential box activation, the exact beginner-motion pattern the direction is trying to avoid.
- `03-gate-outcome.png` reads as a single-frame before/after decision diagram because HOLD, uncertain tag, review panel, STOP, scheduled card, and a second tag are visible simultaneously.
- Board Shot 05 uses disconnected labeled boxes to explain each branch instead of allowing the fork, terminal, tag, and card to prove the behavior.
- Board Shot 06 is the clearest Prezi/map failure: a giant framed overview, large `PRESERVE THE SIGNAL.` headline, equal node boxes, and overlapping card/tag states. Applying the planned pullback to this composition would reveal a slide diagram, not clarify a physical causal rail.
- Board Shot 07 is a title-plus-four-column process slide. The spatial bracket no longer reads as one relationship between original call and measured work order.

These are blocking because they violate the central visual thesis and anti-rules 1, 2, 3, 9, and 11. The correction is compositional: remove explanatory containers and show one physical cause/consequence per shot with the persistent objects carrying the meaning.

## Major findings

### M1. One-primary-focus discipline fails in all three style frames

- `01-reality.png`: `AFTER HOURS` and the large missing-context plate beat the red tag in both scale and reading order, even though the tag is declared primary.
- `02-system-proof.png`: the high-contrast source sheet and red tag form two equal focal masses; the source sheet is the first read at phone size, while the node relationship becomes secondary.
- `03-gate-outcome.png`: `KEEP JUDGMENT`, HOLD, two tags, the work order, STOP, and the review plate all compete. There is no single primary relationship.

### M2. System typography collides with objects and loses hierarchy

- In `02-system-proof.png`, the red tag masks most of `CLASSIFY`, and the source sheet masks/crops `ACKNOWLEDGE`; helper labels also run under the tag. At 480x270, the node verbs are only partially recoverable.
- Board Shot 03 places the rail through node labels and the tag over the central label, while the source sheet overlaps the work-order card. The composition cannot be read in the stated priority order of tag, highlighted source field, then empty card.
- In `03-gate-outcome.png`, the scheduled tag covers the `SCHEDULED` state. The key consequence is present but partially hidden by the object meant to prove it.

### M3. Phone-size legibility fails outside the largest nouns

At 480x270, the call ID, `EMPTY`, `OFFERED`, `BOOKED`, STOP, and large display phrases are generally readable. The small source rows, proof warnings in board Shots 03/04/07, Shot 03 node states, Shot 05 branch qualifiers, Shot 06 node language, and Shot 07 endpoint qualifiers are not reliably readable. The issue is not only font size: collisions, long labels, pale-on-pale elements, and equal-weight containers reduce usable contrast.

The phone test should be applied to each settle frame, not inferred from the 1920x1080 master. Primary state and the full synthetic warning must remain readable without zoom.

### M4. The human gate is rendered as an interface panel instead of a physical act

`03-gate-outcome.png` and board Shot 04 use a pale rectangular `Human review plate`/dashed review box below the rail. It reads as another UI card, not a hand that physically blocks, inspects, and releases the tag. The vertical barrier is clear, but causality from human action to RELEASE is absent from the static reference. The missing-asset slate may remain conspicuous, but its geometry should still occupy the hand's blocking/releasing relationship rather than appear as a floating panel.

### M5. Palette and object treatment drift between style frames and board

The style frames use the specified muted signal brick; the shot board shifts the call tag toward a brighter coral red and adds a lifted drop shadow in multiple shots. This weakens the flat, physical drafting language and makes the board feel more like generic motion-graphics cards. Preserve the brick color, proportions, borders, and permitted contact-shadow behavior across all references.

## Minor findings

### N1. Board annotations visually contaminate the compositions

`READABLE HOLD`, `TAG STOPS 1.7S`, `ONE MOTIVATED PULLBACK`, and `FINAL HOLD TO 01:01.411` appear as black pills inside the shot panels. If these are reviewer-only annotations, move them outside the image area in future boards; inside the frame they resemble production UI and create extra focal accents.

### N2. Display phrases drift from the pinned shot direction

Board Shot 06 uses `PRESERVE THE SIGNAL.` where the shot direction specifies the environmental phrase `KEEP JUDGMENT`, and Shot 07 uses `ONE WEEK.` instead of `ONE-WEEK TEST`. These are not merely copy variations: the pinned phrases protect the judgment thesis and test-not-claim framing. Align the board to the canonical direction rather than introducing alternate headlines.

## What is working

- The paper/navy world split is immediately distinguishable, and the flat grid language is more authored than generic dark-tech styling.
- The brick tag, mono metadata, serif environmental language, and sage outcome state form a coherent starting palette in the style frames.
- Board Shot 02 most nearly meets the one-relationship test: the tag remains visibly caught in voicemail, the card stays empty, and the attention/action gap reads at 480x270.
- The written rhythm map correctly protects the 1.7-second human hold, the post-outcome pullback, and the final measured hold. Those timing choices should remain; the pinned compositions need to be simplified so the holds reveal causality rather than freeze a diagram.
- `02-system-proof.png` demonstrates the correct exact synthetic warning and a clear field-highlight/extract relationship. Its evidence labeling is a useful reference even though its overall composition is too dashboard-like.

## Acceptance-test result

| Test | Result | Exact observation |
| --- | --- | --- |
| One primary focus | Fail | All three style frames and board Shots 03, 05, 06, and 07 distribute attention across several equal containers or headlines. |
| Typography hierarchy | Fail | Primary nouns read, but labels collide in style frame 02/board Shot 03 and state language is obscured in style frame 03. |
| Phone-size legibility | Fail | The exact warning and supporting state language fail in board Shots 03, 04, and 07 at 480x270. |
| Screen direction | Fail | Shot 05 does not visibly connect decline down-left to STOP or acceptance rightward to the card. |
| Cut logic | Fail | The Shot 05/06 lockup and Shot 06/07 proof-pin location reset. |
| Single designed handoff | Fail | Board Shots 02/03 do not preserve tag location or rightward carry into CAPTURE. |
| Slide/dashboard/Prezi/beginner-motion test | Fail | Specific failures are identified in B5. |
| Persistent object identity | Fail | Style frame 03 duplicates the tag; board Shots 04-07 rewrite and later restore its metadata. |
| Evidence warning | Fail | Style frame 02 passes, but board Shot 04 abbreviates the required exact line and other board warnings fail phone size. |

## Authority statement

No gate approval is claimed. No experiment, production, release, or review state is changed. This packet is a critique only; `approval_claimed` and `production_state_changed` are both false.
