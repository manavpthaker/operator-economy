# EP009 opening shot proposal

## Control record

| Field | Value |
| --- | --- |
| Work order | `opening-direction-001` |
| Artifact status | `PRE-AUTHORITY DIRECTION PROPOSAL` |
| Episode | `EP009-direct-booking-recovery` |
| Locked coverage | `0.000-59.420`; `W000000-W000165` |
| Output boundary | Direction analysis only; no approval, media, production select, renderer code, canonical artifact, or production state |
| Candidate dependency | `engine.json` and `world.json` are `UNGATED_DRAFT` hypotheses; V1 is not passed |

This proposal does not pass V1, V2, V3, or V4; approve an engine or world; authorize Step 4; select footage; generate imagery; prescribe a renderer; or advance production. It tests whether the locked opening can sustain one causal visual sequence before those decisions exist. The full production-lane, coordinate, typography, layer-source, ticket, audio-design, and implementation fields required by a canonical scene-direction artifact remain deliberately unset.

## Recomputed input lock

All declared inputs were present and matched the work-order SHA-256 values immediately before authoring.

| Input | Recomputed SHA-256 | Result / standing |
| --- | --- | --- |
| `operator-blueprint-v2/episodes/EP009-direct-booking-recovery/02-narration-production/master/narration-master.wav` | `e433c0fd6d7dd522efb9f6593986f930f9ccc54b2be5132dec50c20ff3c1f944` | `MATCH`; locked narration master |
| `operator-blueprint-v2/episodes/EP009-direct-booking-recovery/02-narration-production/word-transcript.json` | `3c28411effaea94c4dffaac51e114f333f386170fe4716fa96b30d24e41384aa` | `MATCH`; exact word timing source |
| `operator-blueprint-v2/episodes/EP009-direct-booking-recovery/02-narration-production/intentional-pause-map.json` | `62811b5f0ae93359d520f7adfec06ebf46404e8e146cedf274b1f327f9a5cd84` | `MATCH`; pause source |
| `operator-blueprint-v2/episodes/EP009-direct-booking-recovery/03-visual-translation/engine.json` | `f3c9a88d683dd7a99fe5dbd1239611fac723ab8b726d4c0a7b259733c4db6373` | `MATCH`; ungated candidate only |
| `operator-blueprint-v2/episodes/EP009-direct-booking-recovery/03-visual-translation/world.json` | `82b6fb22bc23060f7e11a7e62c058727e64c2e4edf13be43e4c637c0dc5bb355` | `MATCH`; ungated candidate only |
| `studio/originate/direct-booking-recovery/EP006-VISUAL-SYSTEM-LOCKED-VO-ANIMATIC.mp4` | `c93f2c2c6c2129e06c3eff411115208058314a34e6ca40ada33719cc3d475684` | `MATCH`; treatment reference only |
| `design-system/boundary-ledger/semantic-core.json` | `30a316f79bc94e017705de0823a0af5b85747a20938eb0a2723d39a1a298978e` | `MATCH`; canonical semantic core |
| `design-system/boundary-ledger/bindings/color.json` | `6b3e4727c3592b02fe23c34d2a865a85c47865c438d48526d1762b93e9a669c3` | `MATCH`; canonical color binding |
| `design-system/boundary-ledger/bindings/motion.json` | `b2ca3e3295ef2f1dd676732b6b9c7bdefbcfbf55ff642cdf1ab90dc9c84fb450` | `MATCH`; provisional expression binding |
| `blueprint-cinema/references/SHOT-GRAMMAR.md` | `7e4ab99bdad7fa58955ea22853820e0a8e5b0e07f9464fac4d1e9c76295be8ac` | `MATCH`; direction reference |
| `blueprint-cinema/references/SCENE-DIRECTION-CONTRACT.md` | `96f071b2d468e3775aff83de71dccafd6e1b660b2191dc48042c04d37eea097e` | `MATCH`; direction reference |

## Opening premise

**Dramatic question — direction metadata, not narration or on-screen copy:** Can a small inn justify paying an operator to address a returning guest's second commission without treating the platform as a villain or the guest's next booking as controllable?

**Visual sentence — direction metadata, not narration or on-screen copy:** The same unnamed guest passes twice through the same useful external route; a second commission accumulates beside the first, then the frame opens an unresolved arithmetic record and an unfilled operator position without depicting recovery.

**Audience state before:** The viewer sees an ordinary checkout and has no operating model for the second stay.

**Audience state after:** The viewer can explain that one guest used the same valid platform route twice, the property paid twice for that route, the economic test is unresolved, and the proposed operator role remains a question rather than a delivered service or result.

**Grammar chain:** reality to system -> relationship constraint -> same-route return -> cost accumulation -> unresolved operating question -> evidence extraction -> unresolved human opportunity.

The locked narration is reproduced exactly under each shot. No proposed line replaces, shortens, extends, or paraphrases it.

## Authority and continuity rules

1. `returning-guest` is one unnamed human across both stays. Introduce one non-identifying human contour in S01, preserve that contour through the reservation record, and reuse the same contour in S04. Never create a second guest icon or assign a name, email, demographic, or customer ID.
2. The platform route is shown first and fairly: it provides reach and checkout and remains available. The commission is an exchange for that route, not theft or punishment.
3. No owned route appears in this opening. Do not show `booking-record.direct`, `property-guest-record`, consent capture, a transferred relay, a direct booking, commission saving, or a completed recovery.
4. The relay remains attached to `booking-record.platform`. S03 may reveal that its communicative reach ends at a policy boundary; it may not move the alias into property ownership or state a universal duration.
5. The first and second commission events use the same material form, scale, and direction: `property-owner` to `booking-platform`. No rate, percentage, currency amount, gross saving, net saving, or property-specific claim appears.
6. The arithmetic surface is a visible but empty form of `ceiling-record`. It may be established as an unresolved record; DSB-003 forbids showing calculation, derived values, or binding into `audit-bundle`.
7. The operator opportunity is an unassigned accountable position associated with the candidate `practice-operator` object. It is a direction hypothesis, not evidence that an operator exists in market, has accepted the work, has recommended a branch, or gets paid.
8. `a017` / `C022` remains an observed absence with its limiting statement attached. It cannot become proof that nobody offers the service, proof of demand, or proof of an open market.

### Boundary Ledger expression

Only these semantic-role / operation pairs are proposed:

| Pair | Use in this proposal |
| --- | --- |
| `humanContext` / `establish` | Establish the innkeeper, guest, ordinary checkout, blank economic record, and unassigned operator position |
| `externalDependency` / `trace` | Reveal the platform-bound relay and its policy boundary without changing ownership |
| `externalDependency` / `route` | Carry the same guest's second reservation and the second commission through the same external route |
| `accountableEvidence` / `pin` | Attach the qualified `a017` / `C022` absence finding to `adjacent-market-record` |
| `humanContext` / `settle` | Hold the unanswered arithmetic and operator question without resolving it |

Canonical color and provisional motion are not equivalent authority:

- **Canonical color:** `humanContext` uses the paper family (`#F5F0E6`, `#FBF8F1`, `#EDE7D8`); `externalDependency` uses steel (`#586D74`, `#33464C`, `#71868D`); `accountableEvidence` uses mineral (`#204440`, `#173530`). Commission markers inherit steel because they remain part of the external route. No oxide, sage, berry, Rev-C gold, Rev-D cobalt, or generic accent is authorized in this opening.
- **Provisional motion:** the motion binding only permits an expression hypothesis. Each action below reveals causality, then stops. No ambient drift, decorative parallax, bounce, glow, generic node-map build, independent card entrance, or camera float follows a settled state. Exact easing and implementation curves are intentionally unset.

## Original-video treatment ruling

Named reference: `studio/originate/direct-booking-recovery/EP006-VISUAL-SYSTEM-LOCKED-VO-ANIMATIC.mp4`.

What may be learned at treatment level:

- begin in recognizable hospitality reality, then reduce one real object into operating-system geometry;
- let one recurring visit motif carry identity across time;
- move from lived consequence to sourced evidence rather than opening as a deck;
- use large hierarchy, few simultaneous objects, and deliberate holds.

Explicit non-imitation ruling: do not copy the resort/pool photograph, platform logo or brand treatment, the headline `Hotels keep paying to meet the same guest.`, the `60%+` claim or source-page treatment, the exact `Visit 1` / `Visit 2` ledger composition, the gold/navy/dark-code palette, typography, title cards, identity card, shot order, timings, transitions, scene assignments, claims, or any approval implied by that prior video. This proposal carries forward no composition, asset, fact, or production authority from the reference.

## Exact coverage map

The half-open shot intervals are contiguous; the final interval closes at the final locked word.

| Shot | Exact interval | Locked words | Primary shot role | Boundary Ledger verb |
| --- | --- | --- | --- | --- |
| S01 | `[0.000, 10.440)` | `W000000-W000031` | `establish_reality` | `establish` |
| S02 | `[10.440, 22.130)` | `W000032-W000064` | `introduce_object` | `trace` |
| S03 | `[22.130, 26.920)` | `W000065-W000074` | `fail` | `trace` |
| S04 | `[26.920, 31.760)` | `W000075-W000088` | `operate` | `route` |
| S05 | `[31.760, 39.170)` | `W000089-W000109` | `compare` | `route` |
| S06 | `[39.170, 49.980)` | `W000110-W000139` | `orient_system` | `establish` |
| S07 | `[49.980, 54.880)` | `W000140-W000149` | `prove` | `pin` |
| S08 | `[54.880, 59.420]` | `W000150-W000165` | `human_judgment` | `settle` |

Total coverage is exactly `59.420` seconds with no gap or overlap.

## Shot directions

### S01 — Close the reservation, preserve the person

- **Exact interval / words:** `0.000-10.440`; `W000000-W000031`.
- **Locked narration:** “An innkeeper with twenty rooms is closing out a reservation. Good guest. Three nights, tipped housekeeping, asked about the trail behind the property. The kind of person she'd like to see again.”
- **Primary shot role:** `establish_reality`.
- **Boundary Ledger role / operation / verb:** `humanContext` / `establish` / `establish`.
- **Job:** Make the second commission matter first as a human recognition problem: one innkeeper remembers one good guest while completing an ordinary platform-sourced reservation. Do not turn the guest's qualities into a keyword montage.
- **Production lane:** Unset. The proposed frame can be achieved with live-action, illustration, or a designed plate; this work order selects none.
- **Camera:** Stable medium-wide at the front desk, then one short, motivated reframe toward the folio as the innkeeper closes it. Stop when the folio is closed.
- **Foreground:** Physical reservation folio and the innkeeper's closing hand; the folio is the primary layer.
- **Midground:** Innkeeper / `property-owner`, clearly a person rather than an interface operator.
- **Background:** Quiet small-inn front-desk context with no luxury-resort spectacle and no count of twenty room icons.
- **Persistent objects:** Introduce `property-owner`, `returning-guest` as one anonymous human contour attached to the folio, and `booking-record.platform` as the folio's stable identity. Hand all three to S02. Retire nothing.
- **Provisional motion beats:** `0.000-0.080` quiet entry from black; on `W000001` at `0.280`, establish the innkeeper; on `W000006-W000009` at `2.240-3.380`, close the folio; from the `3.380-3.900` pause through `W000031` at `10.440`, settle on the owner's recognition and the one guest contour. No separate motion for “three nights,” “tipped housekeeping,” or “trail.”
- **Transition in:** Black to lived reality; no inherited object and no added sound instruction.
- **Transition out:** At `10.440`, continuity reframe on the folio into S02. Outgoing anchor: folio. Incoming anchor: its contact field. Shared property: the same physical record. The locked `10.440-11.360` pause is the audio bridge; no SFX is authorized.
- **Visible text:** None. Narration carries the context.
- **Candidate / blocker note:** Uses existing candidate objects and changes only viewer knowledge. No open design-system blocker is exercised.
- **Excluded coverage:** Guest name or email; a second guest; tip icon; trail icon; twenty-room diagram; resort glamour; platform villainy; commission amount; direct path; property-held record; operator service; result.

### S02 — Trace the contact field to the platform boundary

- **Exact interval / words:** `10.440-22.130`; `W000032-W000064`.
- **Locked narration:** “So she goes to send a thank you note. And the email on the reservation isn't his. It's a string of letters and numbers ending in guest dot booking dot com. A relay.”
- **Primary shot role:** `introduce_object`.
- **Boundary Ledger role / operation / verb:** `externalDependency` / `trace` / `trace`.
- **Job:** Reveal that the apparent email is a platform-bound relay on the existing reservation, not a guest-owned address and not a property-held relationship. The thank-you attempt remains unsent.
- **Production lane:** Unset.
- **Camera:** Use the S01 folio as a match anchor; move only far enough to make the contact field legible, then reduce the physical page into a minimal steel route boundary.
- **Foreground:** The contact field on `booking-record.platform`, containing a masked, non-identifying alias form; primary layer.
- **Midground:** An unfinished thank-you note and the innkeeper's halted hand. No send occurs.
- **Background:** The front-desk reality resolves into the steel boundary of `booking-platform`; its connection to the reservation is readable, not ominous.
- **Persistent objects:** Carry `property-owner`, the one `returning-guest` contour, and `booking-record.platform`. Introduce `relay-contact` and `booking-platform`. Hand the record, relay, platform route, and guest contour to S03.
- **Provisional motion beats:** During `10.440-11.360`, follow the folio into the contact field; on `W000032-W000040` at `11.360-12.860`, begin but do not send the note; on `W000041-W000048` at `13.270-16.400`, shift priority to the contact field; on `W000049-W000062` at `17.000-21.120`, trace the existing alias to the platform boundary; on `W000063-W000064` at `21.740-22.130`, settle the relay identity without changing it.
- **Transition in:** Continuity from S01 on the same folio/contact-field geometry; `0.920` seconds inside S02 before `W000032` provides the visual reframe.
- **Transition out:** At `22.130`, preserve the relay line and platform boundary into S03. Outgoing anchor: masked contact field. Incoming anchor: the same relay line at its policy boundary. Shared property: platform ownership. The `22.130-23.340` pause is the audio bridge.
- **Visible text:** No full email and no invented alias. If the field needs characters, they remain unreadable/masked; narration supplies the exact relay description.
- **Candidate / blocker note:** Uses `relay-contact`, `booking-record.platform`, `booking-platform`, and `a006` / `C007` as hypotheses. It changes only viewer knowledge and never creates `property-guest-record`; DSB-001 remains untouched.
- **Excluded coverage:** Successful send; personal email; consent; marketing use; alias transfer; lock/cage/prison metaphor; full platform UI; platform logo; invented address; motive claim; direct path; owned list.

### S03 — Reveal the relay's bounded reach

- **Exact interval / words:** `22.130-26.920`; `W000065-W000074`.
- **Locked narration:** “A week or so after checkout, the relay stops working.”
- **Primary shot role:** `fail`.
- **Boundary Ledger role / operation / verb:** `externalDependency` / `trace` / `trace`.
- **Job:** Expose the existing relay's time-bounded communication constraint without destroying the relay object, assigning a universal duration, or claiming a platform motive.
- **Production lane:** Unset.
- **Camera:** Locked system close. The camera does not move while the trace reaches its boundary; the route change supplies the action.
- **Foreground:** The same relay trace from S02 ending at a visible policy boundary; primary layer.
- **Midground:** `booking-record.platform` with the same guest contour still attached.
- **Background:** Stable `booking-platform` boundary and faint property context.
- **Persistent objects:** Carry `relay-contact`, `booking-record.platform`, `booking-platform`, `returning-guest`, and `property-owner`. The relay object remains visible after its communicative reach ends. Hand the guest contour, record, and platform route to S04.
- **Provisional motion beats:** Hold the S02 relay during `22.130-23.340`; on `W000065-W000070` at `23.340-24.570`, advance one qualitative post-checkout interval with no numeric duration; on `W000071-W000074` at `24.970-26.920`, let the trace stop at the policy boundary and settle. Do not shatter, delete, or transfer the alias.
- **Transition in:** Continuity from S02; outgoing and incoming anchor are the same relay trace, sharing line position and steel role color.
- **Transition out:** At `26.920`, cut on the settled policy boundary to a later event on the same platform route in S04. The `26.920-27.000` silence is the bridge; no designed flourish or SFX.
- **Visible text:** None; no duration label.
- **Candidate / blocker note:** Relies on locked narration plus qualified `a007` / `C008`. The duration evidence remains secondary with R001 open; the shot therefore reveals only qualitative closure, not an exact or universal window. No canonical object state is added.
- **Excluded coverage:** Exact number of days; universal policy claim; deletion of the relay; platform motive; property ownership; direct contact; consent; successful outreach; warning-red failure treatment; copied lock iconography.

### S04 — Return the same guest through the same useful route

- **Exact interval / words:** `26.920-31.760`; `W000075-W000088`.
- **Locked narration:** “A year later the same guest books the same room, through the same website.”
- **Primary shot role:** `operate`.
- **Boundary Ledger role / operation / verb:** `externalDependency` / `route` / `route`.
- **Job:** Make temporal recurrence undeniable while preserving guest agency: the same person independently chooses the same available platform route for another reservation.
- **Production lane:** Unset.
- **Camera:** One lateral reveal along the already-established route. No cutaway, montage, or second geography.
- **Foreground:** A later platform booking event carrying the same anonymous guest contour and the same room marker; primary layer.
- **Midground:** The earlier booking event remains as a small temporal trace, not a copied two-column `Visit 1` / `Visit 2` panel.
- **Background:** The same steel platform route linking guest, platform, and property. A restrained route label may read exactly `REACH + CHECKOUT` to preserve the fair exchange.
- **Persistent objects:** Carry `returning-guest`, `booking-platform`, and `booking-record.platform` as stable world identities. Reuse, never duplicate or redesign, the guest contour and room marker. Hand both booking-event traces and the platform route to S05.
- **Provisional motion beats:** On `W000075-W000077` at `27.000-27.870`, advance time to a later point without calendar spectacle; on `W000078-W000084` at `27.900-30.080`, re-present the exact same guest contour and room marker; on `W000085-W000088` at `30.370-31.760`, route the new booking event through the same platform boundary and stop when it reaches the property.
- **Transition in:** Cut from the relay boundary to a later event on the same external route. Shared properties: route position, steel role color, and the same guest contour.
- **Transition out:** At `31.760`, hold the later booking event while S05 reveals its commission consequence during the `31.760-32.500` pause.
- **Visible text:** Optional single route label `REACH + CHECKOUT`; no visit labels, date, name, price, or result language.
- **Candidate / blocker note:** Uses `gate.guest-choice`'s valid platform branch and the static `returning-guest` state `chooses-independently`. It does not attribute the booking to an operator or imply an owned route. No open blocker is exercised.
- **Excluded coverage:** Different guest; duplicated guest token; direct booking; conversion arrow; operator intervention; platform trap; platform logo; copied visit ledger; invented date; property-held identity; recovery.

### S05 — Accumulate the second commission

- **Exact interval / words:** `31.760-39.170`; `W000089-W000109`.
- **Locked narration:** “And she pays the site the same commission she paid the first time. For a guest she already knows by name.”
- **Primary shot role:** `compare`.
- **Boundary Ledger role / operation / verb:** `externalDependency` / `route` / `route`.
- **Job:** Show the second instance of `flow.platform-commission` traveling from property to platform and landing beside the first instance, while the same guest remains human and recognizable.
- **Production lane:** Unset.
- **Camera:** Fixed comparison frame. The commission movement is the only primary action; the camera stays still until both instances can be read together.
- **Foreground:** Second neutral commission marker traveling property-to-platform, then resting beside the first marker; primary layer.
- **Midground:** Two temporal booking-event traces on the same platform route with the single guest contour continuous across them.
- **Background:** `property-owner` on one side, `booking-platform` on the other, and the valid `REACH + CHECKOUT` route between them.
- **Persistent objects:** Carry `property-owner`, `returning-guest`, `booking-platform`, `booking-record.platform`, and the two instances of `flow.platform-commission`. Hand both commission markers, the one guest contour, and the external route to S06.
- **Provisional motion beats:** During `31.760-32.500`, match the second booking event to its cost consequence; on `W000089-W000101` at `32.500-36.240`, route the second commission marker from property to platform and settle it beside the first marker at identical scale; during `36.240-36.760`, stop; on `W000102-W000109` at `36.760-39.170`, return visual priority to the one guest contour without revealing a name.
- **Transition in:** Continuity from the second booking event; outgoing anchor is the booking trace, incoming anchor is its attached commission flow, and causal direction remains property to platform.
- **Transition out:** At `39.170`, preserve both commission markers through the `39.170-40.560` pause while the frame opens enough to admit the unresolved arithmetic surface in S06.
- **Visible text:** No amount or percentage. `REACH + CHECKOUT` may remain as a small carried label; no other text.
- **Candidate / blocker note:** Uses `flow.platform-commission` exactly as the candidate world defines it: property to platform, triggered by a platform booking, paid for reach and checkout. No evidence is upgraded and no saving is calculated.
- **Excluded coverage:** Commission rate; dollar amount; theft metaphor; red danger state; “wasted” label; direct-stack comparison; gross or net saving; guest name; contact ownership; direct booking; recovery.

### S06 — Open the arithmetic without solving it

- **Exact interval / words:** `39.170-49.980`; `W000110-W000139`.
- **Locked narration:** “There's a service a small inn would pay for hiding inside that second commission. And there's one piece of arithmetic that decides whether it's worth your time to sell it.”
- **Primary shot role:** `orient_system`.
- **Boundary Ledger role / operation / verb:** `humanContext` / `establish` / `establish`.
- **Job:** Reveal the decision space around the second commission: one blank `ceiling-record` form and one unassigned accountable operator position. The shot establishes the question; it does not calculate the ceiling, create an offer, or fill the role.
- **Production lane:** Unset.
- **Camera:** A single pullback motivated by the new economic question. It begins from the two commission markers, reveals the blank record and unassigned position, then stops before the word “arithmetic” finishes.
- **Foreground:** The second commission marker aligned with an empty arithmetic line / blank cells in the `ceiling-record`; primary layer.
- **Midground:** An unfilled `practice-operator` position rendered as an accountable place in the system, not a named person, company, product, or sale.
- **Background:** The first commission marker, same guest contour, property owner, and steel external route remain visible so the opportunity never detaches from the actual recurring cost.
- **Persistent objects:** Carry both commission markers, `returning-guest`, `property-owner`, `booking-platform`, and `booking-record.platform`. Introduce only the visible identity of `ceiling-record` and the candidate `practice-operator` position. Hand the unresolved record, unfilled position, and both commission markers to S07.
- **Provisional motion beats:** During `39.170-40.560`, widen from the commission pair; on `W000110-W000123` at `40.560-44.960`, expose the unfilled accountable position beside the second commission; during `44.960-45.720`, hold; on `W000124-W000129` at `45.720-47.680`, establish the blank arithmetic form; on `W000130-W000139` at `47.700-49.980`, hold all cells empty. No number enters and no result resolves.
- **Transition in:** Continuity pullback from S05. Outgoing anchor: two commission markers. Incoming anchor: the same pair within a larger unanswered economic frame. Shared property: position and steel color.
- **Transition out:** At `49.980`, cut from the empty arithmetic line to the qualified evidence record in S07 during the `49.980-50.900` pause. No object morphs into evidence.
- **Visible text:** One question mark may identify the unresolved record. No formula, price, rate, retainer, savings, ROI, or service promise.
- **Candidate / blocker note:** This direction touches DSB-003 only to show its limit. The blank record is an establishment hypothesis; calculation of the commission line, baseline, ceiling, or audit bundle remains prohibited. The unfilled operator position is also a hypothesis and does not exercise DSB-002's blocked recommendation transition.
- **Excluded coverage:** Computed ceiling; audit-bundle assembly; direct-stack cost value; retainer or audit fee; recommendation; owner approval; named operator; successful sale; direct path; consented record; commission saving; recovery.

### S07 — Pin the bounded absence finding

- **Exact interval / words:** `49.980-54.880`; `W000140-W000149`.
- **Locked narration:** “I couldn't find anyone selling it who'd done that arithmetic.”
- **Primary shot role:** `prove`.
- **Boundary Ledger role / operation / verb:** `accountableEvidence` / `pin` / `pin`.
- **Job:** Turn the narrator's search limitation into a retrievable, qualified evidence attachment without turning absence of found evidence into market proof.
- **Production lane:** Unset. This proposal does not select a browser capture, source screenshot, or generated evidence plate.
- **Camera:** Direct cut to one mineral evidence surface. No push-in after the evidence is readable.
- **Foreground:** `a017` / `C022` evidence label and qualifier; primary layer.
- **Midground:** `adjacent-market-record` as the stable attachment target.
- **Background:** The unresolved arithmetic line and unfilled operator position remain faint but recognizable; they do not disappear behind the evidence.
- **Persistent objects:** Carry `ceiling-record`, the two commission markers, and the unfilled operator position. Introduce `adjacent-market-record` and pin `a017` / `C022` to it. Hand the evidence attachment and unresolved economic frame to S08.
- **Provisional motion beats:** During `49.980-50.900`, cut and settle the mineral evidence surface; on `W000140-W000145` at `50.900-52.480`, reveal the finding label and bounded meaning; on `W000146-W000149` at `52.800-53.970`, reveal the limiting statement; during `53.970-54.880`, pin the complete evidence block beside, not inside, the blank arithmetic record and hold.
- **Transition in:** Cut because the question changes from economic form to evidentiary support. No shared-object transformation; the unresolved arithmetic remains as a background continuity anchor.
- **Transition out:** During `53.970-54.880`, continuity dock the complete evidence attachment at the edge of the arithmetic frame. Outgoing anchor: mineral evidence block. Incoming anchor: the same block retained beside the unanswered question in S08.
- **Visible text, exact:** `C022 · OBSERVED ABSENCE`; `No verified operator found for this exact bundle at disclosed economics.`; `Does not prove nobody offers it.` These are evidence labels, not replacement narration.
- **Candidate / blocker note:** Uses only the candidate world's `a017`, `C022`, and `adjacent-market-record`. It supplies no competitor claim, market-size claim, demand proof, price, or operator identity. No open design-system blocker is exercised.
- **Excluded coverage:** “Nobody sells this”; open-market claim; white-space claim; demand; competitor logos; vendor grid; price comparison; original video's source screenshot or `60%+` card; fabricated browser capture; generated imagery as evidence.

### S08 — Hold cost and operator as unanswered questions

- **Exact interval / words:** `54.880-59.420`; `W000150-W000165`.
- **Locked narration:** “So what did that second stay actually cost her, and who gets paid to stop it?”
- **Primary shot role:** `human_judgment`.
- **Boundary Ledger role / operation / verb:** `humanContext` / `settle` / `settle`.
- **Job:** End with the property owner facing two open decisions: the actual economics and whether any accountable operator role is worth funding. Do not resolve either question.
- **Production lane:** Unset.
- **Camera:** Return to the widened economic frame and remain locked. A change in focal priority, not a camera move, connects the cost question to the empty operator position.
- **Foreground:** Blank `ceiling-record` with the second commission marker and one unanswered position; primary layer.
- **Midground:** The first commission marker, the same guest contour, and the unfilled `practice-operator` position.
- **Background:** The platform route remains visible and valid; the complete `a017` / `C022` qualification remains pinned at the edge.
- **Persistent objects:** Carry `property-owner`, the one `returning-guest`, `booking-platform`, both commission-flow instances, blank `ceiling-record`, unfilled operator position, and the qualified evidence attachment. Retire nothing inside this work order. Hand the entire unresolved state forward at `59.420` only as continuity; no post-`59.420` shot or duration is authorized here.
- **Provisional motion beats:** On `W000150-W000158` at `54.880-57.360`, return priority to the blank arithmetic and second commission; during `57.360-58.000`, hold; on `W000159-W000165` at `58.000-59.420`, shift focal priority to the unfilled accountable position without filling it. Freeze the unresolved state on `W000165` ending at `59.420`.
- **Transition in:** Continuity from S07 with the mineral evidence block preserved at the frame edge; the arithmetic surface, not the evidence card, becomes primary.
- **Transition out:** None authorized. The exit state at `59.420` is unresolved and may be held by a separately authorized next sequence; this proposal defines no further frame or timing.
- **Visible text:** One question mark may remain on the blank arithmetic record. No answer, CTA, title, service name, or operator name.
- **Candidate / blocker note:** DSB-003 remains open and visible as unresolved arithmetic. DSB-001 is not approached because there is no owned contact or direct path. DSB-002 is not approached because no recommendation or owner disposition is made. DSB-004 is not approached because no direct-path test or finding is created.
- **Excluded coverage:** Calculated answer; paid operator; named offer; recommendation; owner approval; direct booking; consent capture; property-held record; commission saving; revenue result; recovered guest; sage/verified success; CTA; identity card.

## Blocker disposition

| Candidate item | Opening treatment | Ruling |
| --- | --- | --- |
| DSB-001 — create a separately consented property record | No owned path or property record appears | Excluded; no substitute operation |
| DSB-002 — make and record a recommendation | No recommendation, branch, acceptance, or sale appears | Excluded; no substitute operation |
| DSB-003 — compute and bind the ceiling | Blank `ceiling-record` is established only as an unanswered form | Touched as a visible limit; calculation and binding prohibited |
| DSB-004 — test a direct path and create findings | No direct-path testing or finding appears | Excluded; no substitute operation |
| `a007` / `C008`, R001 open | Relay reach ends qualitatively after checkout | Locked narration governs the line; no exact duration or universal rule |
| `a017` / `C022` | Qualified absence finding is pinned to `adjacent-market-record` | Must retain `OBSERVED ABSENCE` and `Does not prove nobody offers it.` |

## Observable review checks

1. The animatic begins at `0.000`, ends at `59.420`, and covers `W000000-W000165` exactly once with no gap, overlap, added narration, or paraphrased narration.
2. One and only one anonymous guest identity is recognizable in S01 and again in S04; the identity mark does not change or multiply.
3. Before any cost consequence appears, the platform route visibly delivers reach and checkout and is not coded as theft, coercion, a trap, or a villain.
4. The relay remains attached to the platform reservation before and after its communicative reach ends; no line crosses into a property-held record.
5. S04 returns the same guest through the same route by guest choice. No operator action causes the booking and no direct path is visible.
6. S05 shows two same-scale commission instances traveling property-to-platform and no amount, percentage, saving, gross/net comparison, or risk color.
7. S06 contains an empty arithmetic record and an unassigned operator position. No calculation, offer, recommendation, acceptance, or completed service is legible.
8. S07 keeps the `C022` absence finding and its limiting statement visible together; the qualifier never drops while the evidence is on screen.
9. No resort image, platform logo, `60%+` claim, copied `Visit 1` / `Visit 2` panel, legacy palette, title card, or prior identity treatment appears.
10. Motion stops after each causal action. No ambient drift, generic node build, decorative card cascade, floating camera, or keyword B-roll competes with the primary change.
11. The only semantic-role / operation pairs used are the five listed in the Boundary Ledger expression table, and each uses the canonical role color while motion remains marked provisional.
12. The final frame at `59.420` still contains the second commission, blank arithmetic, valid platform route, qualified absence finding, and empty operator position. Nothing reads as recovered, verified, sold, paid, or solved.

## Stop boundary

This work order stops with the proposal. It does not select footage, generate or request imagery, create a production ticket, define a canonical shot board, compile a sequence, claim validator conformance, or return an approval. Any continuation requires a separate authority record and fresh input-hash verification.
