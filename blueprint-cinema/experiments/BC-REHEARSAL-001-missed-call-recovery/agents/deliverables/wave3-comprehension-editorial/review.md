# Wave 3 comprehension and editorial review

Reviewed at: `2026-08-20T20:47:16Z`  
Work order: `wave3-comprehension-editorial`  
Review artifact: `hyperframes/renders/BC-REHEARSAL-001-directed-animatic.mp4`  
Artifact SHA-256: `091e8be81d196a8e27e9322a5664201204cbc3ac644a17af558371b1e5cccca8`

## Editorial verdict

**PASS WITH MAJOR NOTES — the operating idea is understandable, but this packet does not claim creative approval.**

An audience member can follow the same red call tag from the unanswered after-hours call into an unprioritized voicemail path, across the relationship leak, through capture/classify/acknowledge, into a human hold, and through the stop-or-book fork. The empty work-order card remains recognizable and changes to `OFFERED`, `SCHEDULED`, and `MEASURED` only when the corresponding business state changes. The piece does not behave like a Prezi flight, dashboard tour, or title/stat/list slide sequence. Four major editorial issues should be addressed before treating this as approved direction: the opening shows a contradictory `00:00.000` time display, the proof extraction is too compressed, the human actor is not prominent enough at the judgment gate, and the final measurement labels receive only about 1.14 seconds of clean authored hold.

No blocking finding was found in this independent review. “Pass” means the comprehension test succeeded with the listed qualifications; it is not a gate approval.

## Pinned-input integrity

Every work-order pin was recomputed before the MP4 or contact sheets were reviewed. All seven matched exactly:

| Path | Recomputed SHA-256 | Result |
| --- | --- | --- |
| `input-lock.json` | `d5b7f0dc2b7c387bc0e32c3a74daacd4a575fd9f0fb0aa973db82f4f4290a3b2` | pass |
| `direction-lock.json` | `287b1c1ae2f9389905ce3a1149380b311703fa089d8f7bf8927eeb5c0ef0c9ca` | pass |
| `direction/visual-plan.json` | `572f00ae1e51225ea7b161811e356c361eb8734c6f06903642a30049bc0a259c` | pass |
| `hyperframes/index.html` | `d4a7587b83b00c642255b6d41d39c4e6c0e80db22c2dd45e91b79724a2eb7c62` | pass |
| directed animatic MP4 | `091e8be81d196a8e27e9322a5664201204cbc3ac644a17af558371b1e5cccca8` | pass |
| rendered contact sheet | `dd6cf528cf09d175d3ec5c6529bb09501722a130cdbd5b8c5faf9889d4baa6ef` | pass |
| 480x270 contact sheet | `33cc5d12bc60c40c1a0c68a7645780870cf5a6e0c327282443fef69ed58efc83` | pass |

The probed MP4 is 1920x1080 H.264 at 30 fps with 48 kHz stereo AAC audio and a container duration of 61.433333 seconds. That is observational evidence for this editorial packet, not a technical-gate approval.

## Separate review passes

### Pass 1 — comprehension

The actual MP4 was played from beginning to end without production notes open. The following audience inferences were then checked against the locked visual plan:

| Required inference | Result | Observed evidence |
| --- | --- | --- |
| Concrete after-hours event and valuable signal | pass with note | `CALL-R01 / 20:47`, the unanswered phone, `PERMISSION TO RESPOND`, the empty card, and `NO GUARANTEE` are visible by 10.98–13.64. The separate `00:00.000` label weakens the time cue. |
| Current voicemail path | pass | At 13.64–20.00 the same tag is buried behind the voicemail sheets and changes to `UNPRIORITIZED`; the card remains empty. |
| Relationship leak and customer continuation | pass with minor note | At 18.08 the continuation line exits screen-right and by 21.04–26.37 the `ATTENTION`–`ACTION` bridge visibly opens under `RELATIONSHIP`. The continuation mark is brief and anonymous. |
| Recovery route | pass | At 26.37–34.20 the tag moves through `CAPTURE`, `CLASSIFY`, and `ACKNOWLEDGE`; the source field is pinned and the tag receives the extracted time. |
| Human review gate | pass with major note | At 34.20–39.88 the uncertain tag stops at `HOLD`, an operator-hand placeholder appears, and the gate changes to `RELEASE` before the card becomes `OFFERED`. The human actor is visually subordinate. |
| Decline/stop guardrail | pass | At 41.08–42.60 the decline rail resolves into the persistent `STOP` terminal while the card remains offered. |
| Accepted/booked outcome | pass | At 43.05–47.68 the same tag takes the accepted route, attaches to the same card, and the card becomes `SCHEDULED`; no duplicate customer token is introduced. |
| Bounded one-week measure | pass with major note | At 56.05–61.41 the measure line and seven ticks connect `CALL`, `REPLY`, and `BOOKED APPT`, while the card becomes `MEASURED`. The complete labels arrive at 60.27, leaving only about 1.14 seconds before the locked end. |

The persistent IDs read correctly in the film: `CALL-R01 / 20:47` remains the signal and `WO-R01` remains the outcome object. The proof warning stays visibly pinned after its introduction. The story does not require an explanatory caption to recover its basic causal order.

### Pass 2 — rhythm

The MP4 was replayed as a timing-only pass, with particular attention to the hard cuts at 13.64, 26.37, 34.20, 39.88, 47.68, and 56.05 seconds.

- Shots 1 and 2 have enough duration to establish the call, the empty outcome card, the morning stack, and the relationship gap. The hard cut from the settled `PERMISSION TO RESPOND` frame at 12.55 to the voicemail frame at 13.82 is clean and motivated.
- Shot 3 carries seven events between 26.37 and 34.20. The proof card arrives at 27.80, the field highlights at 29.87, the value extracts at 30.36, classification lands at 31.34, and acknowledgment appears at 32.25. The highlight-to-extract interval is only 0.49 seconds, which is too fast for a proof operation whose causal meaning matters.
- Shot 4 is short but has a useful physical pause at `HOLD`; the problem is hierarchy rather than absolute duration.
- Shot 5 gives the decline terminal time to settle before the accepted route completes. Keeping `STOP` visible while the card changes to `SCHEDULED` makes the guardrail and outcome read as alternatives without duplicating the tag.
- Shot 6 earns its single controlled pullback. The removal of the `AUTOMATE ALL` bypass is a motivated relationship change rather than decorative camera motion.
- Shot 7 is concise, but its final `CALL / REPLY / BOOKED APPT` state needs a longer authored settle. A 1.14-second final hold is fragile even before player chrome, compression, or a phone-sized viewport is considered.

### Pass 3 — visual hierarchy

The rendered contact sheet and entry/action/consequence/exit shot sheets were reviewed at original detail.

- The red tag is the primary subject in most frames, while the work-order card is a persistent secondary outcome object. Their colors, shapes, IDs, and screen direction make object permanence unusually clear for a grey animatic.
- Shot 3 briefly has three strong competitors: the red tag, the large pinned source, and the large outcome card. The eye can still find the tag, but the field extraction needs a deliberate hold to establish which relationship matters.
- Shot 4 makes `HOLD` legible, but the red tag overlaps the `HUMAN CHECK` region and the small operator-hand placeholder. The gate reads as a machine label before it reads as a human decision.
- Shot 5 has the cleanest consequence hierarchy: the fork is central, `STOP` is terminal, the tag moves only on the accepted rail, and the card state is the outcome.
- Shot 6 momentarily carries the hand, `AUTOMATE ALL`, the rail, tag, card, and persistent warning. The density resolves quickly and the settled `PRESERVE / ROUTE / JUDGMENT` frame has one causal line, so this is a minor rather than major hierarchy issue.
- The exact synthetic warning is conspicuous when the source is presented and remains pinned. The animatic does not visually misrepresent the fixture as real evidence.

### Pass 4 — 480x270 phone-sized legibility

The actual MP4 was replayed with the browser viewport constrained to 480x270, and the pinned 480x270 contact sheet was inspected separately.

- Primary text survives: `CALL-R01`, `20:47`, `EMPTY`, `OFFERED`, `SCHEDULED`, `MEASURED`, `HOLD`, `STOP`, `CAPTURE`, `CLASSIFY`, `ACKNOWLEDGE`, and the final `CALL / REPLY / BOOKED APPT` labels are readable.
- The proof card's `SYNTHETIC TEST FIXTURE — NOT EVIDENCE` warning remains readable at its full presentation around 29.56 seconds. The persistent small warning remains identifiable, though not comfortable body copy.
- Supporting microcopy does not survive reliably: the work-order disclosure, `AST-OPERATOR-003`, the tag's small state strip, and the physical `HUMAN CHECK` detail are too small to carry essential meaning.
- The opening `00:00.000` counter is readable enough to contradict the intended 20:47 cue, which makes it a real editorial issue rather than harmless microcopy.
- At the final frame, common native player controls can cover the bottom measurement labels. Player chrome is not part of the render, but the short 1.14-second authored hold gives an audience little margin to dismiss controls and reread the endpoint.

## Ranked findings

### Blocking

None.

### Major

1. **Opening time contradiction, 0.15–13.64.** The sequence is supposed to enter a concrete 8:47 p.m. event, but the upper timestamp reads `00:00.000` while the tag reads `20:47`. At full size and at 480x270, the two cues coexist. Replace the counter with the physical after-hours time or remove it; do not leave two incompatible temporal authorities on screen.

2. **Proof operation is over-compressed, 27.80–32.25.** Source presentation, field highlight, value extraction, tag attachment, classification, and acknowledgment occur in 4.45 seconds; highlight-to-extract is 0.49 seconds. The warning is honest and the source remains pinned, but an audience cannot comfortably verify the causal field-to-tag transfer. Give the highlighted field and extracted `20:47` at least one clear additional beat, or reduce simultaneous secondary content.

3. **Human judgment is visually subordinate, 34.20–39.88.** `HOLD` and `RELEASE` are legible, but the tag overlaps `HUMAN CHECK`, the hand placeholder is small, and the large card competes on the right. This makes the operation read first as a labeled routing gate and only second as a human decision. Keep the tag immediately upstream until review, enlarge the human action/ticket placeholder, and let the release be visibly caused by that action.

4. **Final measurement hold is too short, 60.27–61.411354.** The final `CALL / REPLY / BOOKED APPT` labels and completed relationship arrive only about 1.14 seconds before the locked VO ends. The endpoint is inferable, but it does not yet provide the requested readable hold after an important reveal. Land the labels earlier or simplify the final construction so the complete state can hold for roughly 1.8–2.0 seconds without changing the locked duration.

### Minor

1. **Customer continuation is under-specified, 18.08–20.00.** The rightward continuation mark is brief and has no recognizable homeowner identity. The narration supplies “called someone else,” while the visual mainly proves that the signal remained on the attention side. Strengthen the exiting customer/signal continuation without adding a second persistent call tag or vilifying another provider.

2. **Phone-size supporting text is below practical reading size, especially 34.20–39.88 and 47.68–56.05.** Primary state labels pass, but operator-ticket text, the human-check detail, and small state strips are not independently readable. Keep them as nonessential metadata or raise their scale when they carry review-critical meaning.

3. **Shot 6 has a brief competing-focus moment, 47.68–49.50.** The operator hand, `AUTOMATE ALL`, route, tag, card, and warning appear together during the pullback. The density settles and the transition is motivated, so this does not become a dashboard or Prezi failure; staggering the hand/bypass removal a few frames ahead of the wider reveal would make the operating principle cleaner.

## Anti-amateur and presentation-grammar check

- No title/stat/list/diagram-card procession: pass.
- No Prezi-style flight among boxes or excessive zooming: pass; the one restrained pullback explains the whole recovery rail.
- No permanent full-world inset, website, or dashboard layout: pass.
- No glass panels, dark AI imagery, ambient drift, bouncing, or elastic energy: pass.
- Cuts used by default: pass.
- No decorative transition: pass. The designed pullback preserves the tag/card and exposes a real bypass relationship.
- No new composition for every narrated noun: pass. Seven shots cover coherent business states, and objects persist across them.
- No transition or motion whose only purpose is energy: pass in this editorial watch.
- No fake evidence or unlabeled synthetic material: pass. The source is explicitly synthetic and the exact warning remains pinned.
- No more than one durable primary focal point: pass overall, with the Shot 3 and early Shot 6 density notes above.

## Recommendation

Accept this packet as evidence that the directed animatic's basic comprehension chain works. Do not treat it as creative approval. Correct the four major issues, rerender, and repeat the same four editorial passes—especially the 27.80–32.25 proof operation and 60.27–61.41 final hold—before asking a human director to approve the sequence.

This worker claims no gate approval, makes no production-state change, and did not edit any canonical experiment artifact.
