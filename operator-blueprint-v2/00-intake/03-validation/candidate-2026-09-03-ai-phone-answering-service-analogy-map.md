# Analogy map: Managed inbound call coverage for owner-run residential trades contractors

Template status: approved V2 Step 0.2 template; locked 2026-08-21.

Template version: `operator-blueprint-v2-step0.2`

Candidate ID: `candidate-2026-09-03-ai-phone-answering-service`

Candidate brief: `../01-candidates/candidate-2026-09-03-ai-phone-answering-service.md` / `b2ee91c098753251fd570f934a86ffd604ded71e47fab21ef9cf4717dba55cf9`

Research brief: `../02-research/candidate-2026-09-03-ai-phone-answering-service.md` / `3d2453211585c887be85f9cd84eca359a5fbdf9011debbf1f749e967df86def1`

Prepared: 2026-09-03

Evidence class: **adjacent synthesis**

## Synthesis thesis

This business is like a **human answering service** for the buyer's existing budget line and pricing unit, like the **vertical-platform AI receptionist** for the observed alternative and its price floor, and like a **managed IT or workflow-reliability service** for the shape of the residual offer — configure, monitor, document and report on a system the client already licenses. The new combination is a managed layer sold on the three jobs the platforms disclaim: emergency escalation, state-correct disclosure and consent, and independent monthly measurement.

## Transfer records

| Analogy ID | Proposed-business component | Reference model | Source claim IDs | Relationship | Shared structure | Required adaptation | Does not prove | Break condition | Confidence | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| ANA-001 | Buyer and costly problem | Home-services businesses whose calls ring out while the crew works | CLM-001, CLM-002 | adjacent | Same buyer class and same failure — the call arrives while nobody is free to answer | Vendor datasets skew to businesses that buy call tracking; the buyer's own log must replace them | The dollar value of a missed call; the legacy 62% figure (CLM-003 excluded) | A 2-15 person contractor's own log shows unanswered share under 10% | medium | valid |
| ANA-002 | Budget and current alternative | Human answering services (Ruby, Smith.ai) and a salaried receptionist | CLM-011, CLM-012, CLM-013 | adjacent | Same buyer job, purchased today; pricing unit is minutes or calls per month | The AI layer is priced below the human unit, not against it | That the buyer will spend on a managed layer rather than the platform toggle | Buyers treat the $29 add-on as the whole budget | high | valid |
| ANA-003 | Offer and delivery — the core answering | Vertical-platform AI receptionists (Jobber, Housecall Pro, ServiceTitan) and home-services AI front offices (Sameday, Avoca) | CLM-004 to CLM-009 | direct (as the observed alternative) | Same buyer, same job, same deliverable — an agent that answers and books into the calendar | **The operator must not compete on this component.** It is delivered by the buyer's own software at $29 or as an add-on | That a residual layer exists above it | Already observed: the platform delivers the core cheaper and natively | high | **valid as the alternative; rejected as the operator's offer** |
| ANA-004 | Offer and delivery — the residual managed layer | Managed IT / workflow-reliability services | — (structural; fixture `candidate-test-2026-08-21-workflow-reliability-service`) | adjacent | An independent configures, monitors, documents and reports on a system the client licenses; paid for reliability | The system here is a receptionist toggle, not an integration stack; the "failure" is one bad call, not an outage | That contractors experience the receptionist as complex or consequential enough to pay for management | The platform ships escalation and disclosure defaults, or contractors treat the toggle as set-and-forget | **low-medium** | **weak** |
| ANA-005 | Offer and delivery — escalation design | Voice-AI rollbacks in restaurant ordering | CLM-026 | adjacent | Automated voice handling fails on edge cases and needs a human monitoring and stepping in | Contractor emergencies (gas, water, no heat) are higher-stakes and lower-volume than drive-through orders | That escalation design is purchasable separately from the platform | Platforms ship keyword handoff as standard (Jobber already hands over on flagged words, CLM-004 coverage) | medium | valid (supports the job, not the price) |
| ANA-006 | Offer and delivery — compliance layer | Consent and disclosure obligations on AI voice systems | CLM-018 to CLM-024 | component | A legal requirement the platforms leave to the buyer ("this isn't required"; "that's up to you") | Must be verified per state; nothing is legal advice | That a contractor values compliance enough to pay; that the platforms will not add a default | Platforms add a disclosure and recording default to the greeting | medium | valid (supports the job, not the price) |
| ANA-007 | Economics and capacity — delivery cost | Metered voice-agent infrastructure | CLM-014 to CLM-017 | component | Per-minute costs are public and low | The buyer, not the operator, should hold the account (CLM-021) — which removes usage margin from the operator's model | That any fee is achievable | Per-minute prices rise or platforms restrict third-party configuration | high | valid |
| ANA-008 | Economics — setup fee | Freelance-marketplace builds | CLM-027 | component | The same build, sold as a gig | None — this is the observed price of the build alone | That a setup fee above the gig price is achievable | Already observed: builds list at $10-90 | medium | valid as a ceiling, not a floor |
| ANA-009 | Go to market | Demo-led selling from the old episode, re-pointed at the log | CLM-004 (adoption), CLM-002 (answer-rate framing) | adjacent | Show the buyer their own phone failing, then their own data | The demo must now show the gap the platform toggle leaves, not the answering itself | That the demo converts | The buyer's answer is "Jobber already does this" | medium-low | valid, weakly |
| ANA-010 | Outcome measurement | Call-tracking answer-rate reporting | CLM-001, CLM-002 | component | Answer rate and booked jobs are computable from the buyer's own logs | Must be produced from the buyer's platform export, not a vendor dataset | Business impact beyond the answer rate | Logs unavailable or the platform's own dashboard already reports it | high | valid |
| ANA-011 | Revenue model — per-minute resale | White-label reseller platforms | CLM-030 | context | Operator pays platform per minute, charges the buyer flat | **Rejected for this candidate.** Resale margin makes the operator the data-holding third party (CLM-021) and competes on the absorbed component (ANA-003) | Anything about demand | Already broken by ANA-003 | high | **rejected** |

## Coverage test

| Pillar | Required status | Supporting analogies | Result | Remaining assumption and test |
|---|---|---|---|---|
| Buyer and costly problem | Must have usable direct or adjacent evidence. | ANA-001 | **pass** | Magnitude is 14-48% non-answer depending on definition (CLM-001, CLM-002), not 62%. Validation step 1 replaces vendor data with the buyer's log |
| Budget or current alternative | May use direct, adjacent, or component evidence. | ANA-002, ANA-003 | **pass** | Budget exists and is well priced from primary pages. The assumption is that any of it is available above the $29 native option |
| Offer and delivery | Must have a valid operating parallel or bounded first-party test. | ANA-004 (weak), ANA-005, ANA-006, ANA-003 (as alternative) | **pass, narrowly** | The core answering has a valid observed parallel but it belongs to the platform. The residual layer has only a weak structural parallel and a bounded first-party test. This is the pillar Reviewer B is most likely to fail |
| Go to market | May use a transferable acquisition or diagnostic-entry model. | ANA-009 | **pass, weakly** | Rests on the log-and-gap demo beating "my software already does this." Validation step 2 |
| Economics and capacity | Must have a transparent model with evidence for its inputs or explicit testable assumptions. | ANA-007, ANA-008, ANA-002 | **pass** | Delivery costs and alternatives are observed; the operator's fee is entirely modeled and the base case barely clears imputed labor |
| Outcome measurement | Must define an observable buyer deliverable; business impact may remain a hypothesis. | ANA-010 | **pass** | Answer rate, escalations and booked jobs from the log are observable. Revenue impact is not claimed |

## Evidence-floor verdict

- Usable direct or adjacent buyer/problem evidence: **pass** — two large vendor call datasets (CLM-001, CLM-002) establish the failure in the buyer class, with the interest caveat recorded
- Valid analogy count: **seven valid** (ANA-001, 002, 005, 006, 007, 008, 010), two valid-weakly (ANA-003 as alternative only, ANA-009), one weak (ANA-004), one rejected (ANA-011). Minimum 3 — pass
- Independent source families: **four** — call-tracking and conversation-intelligence vendor datasets (CLM-001, CLM-002); vertical-software and direct-AI vendor pricing and product pages (CLM-004 to CLM-010); infrastructure pricing pages (CLM-014 to CLM-017); primary law and legal commentary (CLM-018 to CLM-024); plus government wage data (CLM-013). Minimum 2 — pass
- Required pillars covered: **pass**, with offer and delivery passing narrowly
- More than one untested inference hop in a load-bearing claim: **no.** The chain runs: calls ring out in this buyer class (CLM-001, CLM-002) → buyers already spend on answering (CLM-011 to CLM-013) → the buyer's platform now delivers the core (CLM-004 to CLM-007) → what it leaves to the buyer is escalation, disclosure and measurement (CLM-005, CLM-006, CLM-019, CLM-021) → an independent could sell that layer (ANA-004). Every link but the last has its own source; the last is the single untested hop and is the thirty-day test
- Uncovered pillars resolvable through the bounded validation plan: **yes** — the plan tests exactly the untested hop

Verdict: **pass, narrowly**

Reason: The floor passes on the strength of the buyer-side evidence and the alternatives, both of which are better sourced than the legacy package: primary pricing pages, government wage data and primary law replace vendor blog aggregation. What is worse than the legacy package is the offer. The component the old episode sold — answering the phone with AI — is now an observed alternative delivered by the buyer's own software, and ANA-003 is recorded as **rejected as the operator's offer**. What remains is ANA-004, a structural parallel to managed services with low-medium confidence and a break condition — platforms shipping escalation and disclosure defaults — that is entirely in the vendors' hands.

Two transfers were removed rather than stretched. ANA-011 (per-minute resale) is rejected because it competes on the absorbed component and makes the operator the data-holding third party under the CIPA capability theory. CLM-003, the 62% figure, is excluded because it is a 2016 SEO-agency post about 85 businesses.

## Disclosure carried forward

The episode must describe an **adjacent synthesis**. No independent operator was found selling a managed coverage layer on top of a contractor's platform receptionist at disclosed economics, and no contractor was found paying for one.

The most important assumption the viewer must hear: **the answering itself is no longer the operator's product.** The plumber's own software sells it for $29 a month. The only thing left to sell is the layer the platforms disclaim — deciding what the agent must never handle alone, keeping the greeting legal in the caller's state, and proving the result from the log — and nothing in this package shows a contractor will pay for that layer. The thirty-day test exists to find out, and the episode must present a negative result as a legitimate outcome.

Three things must not be said. **The "62% of calls go unanswered" figure may not appear in any form** — it is a 2016 blog post about 85 businesses. **No pricing band from the old episode may be presented as a market rate** — the build alone lists at $10-90 and the native alternative is $29. **Nothing about disclosure, recording consent or the TCPA is legal advice**; the rules vary by state and the operator must verify locally.
