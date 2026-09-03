# Candidate: Managed inbound call coverage for owner-run residential trades contractors

Template status: approved V2 Step 0.2 template; locked 2026-08-21.

Status: candidate

Template version: `operator-blueprint-v2-step0.2`

Candidate ID: `candidate-2026-09-03-ai-phone-answering-service`

Created: 2026-09-03

Owner: Manav Thaker

Proposed evidence class: adjacent synthesis

Historical source premise: EP002, "The Phone Call Businesses Never Answer" (published 2026-07-13; URL stated only in `studio/originate/voice-agent-agency/launch/links.json`).

- `studio/originate/voice-agent-agency/research.md` / `47997670a99d73fad84c0fc3b9466f25053109064f6171c9c0c71de007a67e51` (identical to `research/briefs/ep002-voice-agent-agency.md`)
- `studio/originate/voice-agent-agency/script.json` / `11dfea0b4deedb9efe95e21b9794cdc2d9c0022da540223ad3749c5bf7d6dadd`

Prior publication earns no promotion credit. The old brief, script and scores are leads, not evidence. The 2026-08-21 legacy screen gave this premise a provisional band of 68-78 and named the vendor-adjacent missed-call statistic and agency economics as the things a fresh package must replace.

## Refinement of the historical premise

The historical premise was: a solo operator resells AI phone-answering to "local businesses that miss calls" — plumbers, dentists, salons, florists — at $300-1,000 per month on per-minute infrastructure that costs a fraction of that.

This candidate bounds it, without changing the underlying business, to:

- **One buyer:** the owner of a residential plumbing, HVAC or electrical contractor with roughly 2-15 staff, whose technicians are in the field and who already runs the business on a field-service platform (Jobber, Housecall Pro or ServiceTitan).
- **One job:** the after-hours and overflow inbound calls that ring out while the crew is on a job.
- **One deliverable:** a managed inbound-coverage service — a configured AI receptionist (the buyer's own platform add-on where one exists, a Retell/Vapi build only where it does not), a written emergency-escalation rule set, caller disclosure and recording consent set to the caller's state, and a monthly answer-rate and booked-jobs report from the buyer's own call logs.
- **One 30-day test:** pull 30 days of call logs from ten contractors, offer a paid coverage audit, and find out whether anyone pays for a layer their own software now gives them for $29 a month.

The revenue model stays recurring (setup fee plus flat monthly), which is what the old episode described. What changes is honesty about where the margin has to come from: not from reselling per-minute infrastructure, but from the escalation, compliance and measurement work that the platforms leave "up to you."

## Opportunity in one sentence

An operations-minded generalist sells owner-run residential trades contractors a managed inbound-coverage service that answers and books the calls their crew cannot take, escalates real emergencies to a human, keeps the caller disclosure and recording consent legal by state, and proves the result monthly from the contractor's own call logs.

## Viewer outcome

- Viewer promise: The viewer understands what happened to the "AI receptionist agency" in the twelve months after it was pitched — the buyer's own software absorbed it — and what, if anything, is left for an independent operator to sell.
- Operator decision: Build the managed-coverage service, test it on ten contractors, fold it into an existing service business, or reject it because the platforms already sell the core for $29.
- Practical capability: Read a contractor's call log to compute an actual answer rate, design an escalation rule set for emergency calls, set disclosure and consent to state law, and price a managed layer against the platform's native add-on.
- Expected Operator Canvas: Buyer and trigger, the answer-rate baseline, what the buyer's platform already includes, the residual offer, escalation design, the compliance checklist, pricing arithmetic against the $29 alternative, capacity, and the kill condition.

## People

- Viewer/operator: An operations, product, customer-experience or systems generalist who can read a call log, write and test a conversational prompt, configure a platform add-on, and hold a plain conversation with a contractor about what the agent must never handle alone.
- Buyer: The owner of a residential plumbing, HVAC or electrical contractor with roughly 2-15 staff. The owner controls the budget and is usually also the person answering the phone from a van.
- End customer or beneficiary: The homeowner calling with a leak, a dead furnace or a tripped panel, who either gets booked or calls the next listing.
- Guest or outside participant required: no for the episode; yes for a real pilot, with the contractor's permission to use their call data.

## Problem

- Costly problem: Calls ring out while the crew is working. A caller who reaches voicemail often does not leave a message and often calls the next contractor.
- Why it matters: A booked service call is the contractor's revenue event; the magnitude of the loss is the first thing this package must establish independently, because the legacy figure ("62% of calls go unanswered") traces to a 2016 SEO-agency blog post about 85 businesses and is not usable.
- Why now: Between August 2025 and April 2026 the vertical software the buyer already pays for shipped its own AI receptionist — Jobber at $29 a month, Housecall Pro as an add-on, ServiceTitan as a Pro product — and a home-services-only AI front office (Avoca) raised at a $1 billion valuation. The reseller layer the old episode described has been absorbed from above. At the same time, Maine made disclosure of an AI voice mandatory, California courts let wiretap claims against inbound AI call vendors proceed, and the platforms still say disclosure is "up to you."
- Existing alternatives and budget: A human receptionist (BLS 2025 median $38,010 a year); human answering services (Ruby from $250 a month for 50 minutes; Smith.ai $300 a month for 30 calls); direct AI products (Jobber Receptionist $29 a month, Goodcall from $79, Sameday from $449); or the owner's own voicemail.

## Proposed business

- Offer: A managed inbound-coverage engagement — call-log baseline, receptionist configuration on the buyer's existing platform (or a Retell/Vapi build only where the platform has none), an emergency-escalation rule set, a state-correct disclosure and recording-consent greeting, weekly transcript review, and a monthly answer-rate and booked-jobs report.
- Customer outcome: Fewer calls ringing out, a documented escalation path for emergencies, a greeting that is legal in the caller's state, and a monthly report the owner can read in one minute.
- Delivery hypothesis: Baseline from 30 days of call logs → configure and test the agent against the contractor's real scenarios (emergency, quote, reschedule, spam) → set escalation and disclosure → go live on overflow and after-hours only → review transcripts weekly → report monthly.
- Revenue hypothesis: Setup fee plus flat monthly managed fee. The buyer owns the platform account and pays usage directly; the operator does not resell per-minute margin.
- Most important unproven assumption: **That a contractor will pay an independent for the escalation, compliance and measurement layer when the answering itself is a $29 checkbox inside the software they already use.** This must not be assumed. It is the 30-day test.

## Initial synthesis hypothesis

- Parallel A: Human answering services (Ruby, Smith.ai) → the buyer's existing budget line and the "minutes or calls per month" pricing unit.
- Parallel B: Vertical-platform AI receptionists (Jobber, Housecall Pro, ServiceTitan, Sameday, Avoca) → the observed direct alternative, its price floor, and proof that contractors adopt automated answering.
- Parallel C: Managed IT and workflow-reliability services → the model of an independent who configures, monitors and documents a system the client already licenses, and is paid for reliability rather than for the software.
- New combination: A managed layer that sits on top of the buyer's own AI receptionist, sold on three things the platforms explicitly do not do — emergency escalation design, state-correct disclosure and consent, and an independent monthly measurement — rather than on reselling the voice.
- Suspected transfer risk: Managed IT works because the systems are complex and failures are costly. A $29 add-on with a toggle may be neither. If contractors treat the receptionist as "set it and forget it," the managed layer has no buyer.

These are research directions, not evidence. The completed research brief and analogy map decide whether the transfers are valid.

## Narrative potential

- Starting state: A plumber under a sink at 4:40 pm; the phone in the van rings four times and stops.
- Inciting change: The software he already pays for adds a receptionist for $29 a month. The agency that pitched him $500 a month for the same thing last summer stops calling.
- Causal mechanism: The answering itself was never the scarce part. Voice, orchestration and telephony are metered at cents a minute and were absorbed by the platforms that already hold the calendar. What was scarce — deciding what the agent must never handle, keeping the greeting legal, and proving the result — was left "up to you."
- Operator build: A managed coverage service that takes the parts the platforms left on the floor.
- Stakes and tradeoffs: A gas-leak call routed to a bot; a caller in an all-party-consent state recorded without notice; a contractor who cancels because the first embarrassing call cost him a customer; a business whose ceiling is set by a $29 alternative.
- End state: The operator knows whether a contractor pays for the residual layer, and the viewer knows what it means when a category gets absorbed by the buyer's own software.
- Visual evidence: A real call log with an answer-rate column; the Jobber add-on screen at $29; the pricing pages side by side ($29 / $79 / $250 / $300 / $449 / $38,010); the escalation rule set as a flow; a disclosure greeting in two states; a Retell cost-per-minute stack; a monthly report.

## Audience pull

- Exact or adjacent viewer questions: "how to start an AI receptionist business", "AI receptionist agency", "is an AI answering service worth it for a plumber", "Jobber Receptionist vs answering service", "AI phone agent legal disclosure".
- Initial interest signals: To be established. Leads: a wave of 2026 creator content and workshops on starting an AI receptionist business; Fiverr and Upwork gigs building AI receptionists for home services at $10-90; the platforms' own launches and funding.
- Timely tension: The business that was pitched to would-be operators in 2025 was absorbed by the buyer's own software inside a year, while the legal exposure the platforms ignore is growing.
- Coverage gap: Current coverage is either "start an AI voice agency" opportunity content or vendor comparison lists. None of it tells the operator that the buyer's platform already sells the core, none of it reads a real call log, and none of it treats state disclosure and recording-consent law as part of the product.
- Honest working premise: A year ago this was the AI business you could start for $150 a month. Then the plumber's own software started selling it for $29. Here is what is left — and whether anyone will pay for it.

## Discovery and POV

- Search-volume status: attempted but not measurable — Google Trends returned HTTP 429 on two attempts on 2026-09-03; no licensed keyword tool is available to this operation. Proxy signals required.
- Operator Economy POV (scored under Step 0.3):
  - Transferable earned judgment: two years as Director of Customer Experience across four boutique properties (Coqui Coqui, Oct 2014-Oct 2016) where the phone was a booking channel and the front desk missed calls during checkout; a year as AI Product Manager at Lovingly (Sep 2024-Sep 2025) working with a platform serving 1,500+ florists, a category with the same peak-day call problem. This is buyer-side and platform-side judgment about missed calls, not experience selling or running an answering service.
  - Original synthesis (to be demonstrated in research): the recycled "62%" figure is a 2016 SEO-agency post about 85 businesses, while the two largest current call datasets put home-services non-answer materially lower; the reseller layer was absorbed by vertical software within a year of the episode; and the disclosure and recording-consent layer the platforms disclaim is the only part of the product not already sold by the buyer's own software.
- POV boundary: Manav has never run an answering service or an AI-receptionist agency, has never sold this to a contractor, and did not build phone AI at Lovingly. The facts ledger bars "I ran a hospitality business"; the permitted framing is "two years in boutique hospitality." Nothing here is legal advice.

## Initial evidence status

- Buyer-problem evidence: lead found — two large vendor call datasets (CallRail 2025, Invoca 2026) give home-services answer rates; the legacy 62% figure is not usable.
- Budget or current-alternative evidence: usable component — published prices for human receptionists (BLS), human answering services and direct AI products.
- Offer and delivery parallel: lead found — managed-service and white-label reseller models exist; whether a managed layer on a $29 add-on has a buyer is unknown.
- Economics or capacity inputs: modelable — per-minute infrastructure prices are primary and current.
- Audience-interest signals: one signal — creator and marketplace activity; needs triangulation with buyer behavior.
- Narrative engine: strong — but at risk of being a cautionary tale rather than a blueprint.

## Known blockers

1. **Platform absorption.** The buyer's own software sells the core for $29 a month (Jobber), as an add-on (Housecall Pro) or as a Pro product (ServiceTitan). The candidate survives only if the residual layer is purchasable.
2. **Build commoditisation.** Freelance marketplaces list AI-receptionist builds for home services at $10-90. The old "$500-2,000 setup fee" has no current support.
3. **The legacy missed-call statistic is unusable.** The 411 Locals figure is from January 2016, an SEO agency, 85 businesses, no stated sampling.
4. **Legal surface.** All-party recording consent in roughly a dozen states; Maine's mandatory AI disclosure covers voice; CIPA third-party claims against inbound AI call vendors survived dismissal; outbound AI calling is TCPA-restricted and excluded. Manageable inbound-only with disclosure, but the operator inherits exposure if the agent runs on the operator's own account.
5. **Consumer resistance.** Surveys commissioned by a human answering service report about a third of callers hanging up on AI. Interested source, but the direction is corroborated by independent reporting on voice-AI rollbacks.
6. **No income evidence.** The old "$1,500-5,000 a month from 3-8 clients" was reasoned from vendor pricing bands and is not usable.

## Intake decision

Decision: research

Reason: The buyer, the moment, the deliverable and the visual story remain concrete, and current primary pricing makes the economics modelable. But the business the old episode described has been structurally undercut by the buyer's own software, and the only version worth testing is the residual managed layer. Research must establish whether that layer has a buyer, what the real answer-rate gap is, and what the compliance work legally requires — and must be prepared to find that it does not pass.
