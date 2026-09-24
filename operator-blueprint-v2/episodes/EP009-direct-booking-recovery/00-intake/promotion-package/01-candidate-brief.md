# Candidate: Direct-booking recovery service for small independent lodging

Template status: approved V2 Step 0.2 template; locked 2026-08-21.

Status: candidate

Template version: `operator-blueprint-v2-step0.2`

Candidate ID: `candidate-2026-09-03-direct-booking-recovery`

Created: 2026-09-03

Owner: Manav Thaker

Proposed evidence class: adjacent synthesis

Historical source premise: EP006, "Hotels Pay 30% to Book Their Own Rooms" (published 2026-08-17; URL recorded only in `studio/originate/direct-booking-recovery/launch/links.json` / `23dfdc4f5fd2e0f3eb4d693c4d0b8f3008320a2eeb5cf6c2e853e754256ccf1d`). Source package treated as leads, not evidence:

- `studio/originate/direct-booking-recovery/research.md` / `61a1ed53bafa657266c7ad6b27af9069d2a75ad05f885f987776f9d781e6076e`
- `studio/originate/direct-booking-recovery/script.json` / `15b2f1b3cc1e66488135cd876c6f019bcbb3a08ac425866bffc570de0c3bccf6`
- `studio/originate/direct-booking-recovery/REV-E-NARRATIVE.md` / `9977cf8e62ebd8684165aa014d5df896928317cb19aa0369fa75550a67329724`
- `content-os/facts.md` section "EP006 research — direct booking recovery (verified 2026-08-16)" / file hash `d1b67dd431b36dcf201b8c42053c663ef47c6c34e5bde272daedb9eabcc9a201`

Prior publication earns no promotion credit. EP006 was excluded from the 2026-08-21 legacy screen as the then-current control episode and carries no provisional band.

## Reframing from the V1 premise

The V1 episode sold a broad idea: "independent hotels lose two thirds of bookings to OTAs at 18-30%; a solo operator installs the direct-booking stack and prices against the commission saved." It named a band ("10-40 rooms") but never one buyer, one deliverable, or one test, and its economics stopped at the hotel's commission bill. This candidate bounds it without changing the business:

- **One buyer:** the owner-operator of a US independent lodging property of roughly **20-40 rooms** (inn, B&B, small boutique hotel) with no revenue-management or marketing hire. The band is narrowed from 10-40 because the research brief's ceiling arithmetic shows a 10-room property cannot fund a retainer from recovered commission.
- **One job:** raise the property's **direct share of bookings** by recovering guests the property has already served, and make the direct path work for guests who find it anyway.
- **One deliverable:** a paid **direct-booking audit** (booking mix, commission line, cancellation by channel, direct-path test, and a first-party guest-data capture check) followed by a monthly **direct-share scorecard** run under a fixed retainer.
- **One 30-day test:** audit three properties in the band, at least one paid, and record whether the owner will fund a retainer priced under the property's own recovered-commission ceiling.

## Opportunity in one sentence

An operations-and-marketing generalist with hospitality judgment sells 20-40-room independent lodging properties a paid direct-booking audit and a fixed monthly retainer that keeps the property findable, makes the direct booking path trustworthy, and re-books past guests from consented first-party data, reporting one number: direct share of bookings, before and after.

## Viewer outcome

- Viewer promise: The viewer understands why an independent property keeps paying to meet the same guest, what an OTA actually withholds from the property after checkout, what a recovery retainer can honestly charge against a 20-40-room commission line, and how to test the offer in 30 days.
- Operator decision: Build the practice, fold it into an existing hospitality-marketing or PMS-consulting business, test one paid audit, or reject it because the price ceiling is too low for their cost of time.
- Practical capability: Compute a property's commission line and recovery ceiling from four inputs; run a direct-path test as a guest; design a consent-based guest-data capture; write a one-number scorecard.
- Expected Operator Canvas: Operator fit, buyer band and disqualifiers, the guest-data constraint, audit scope, three operating jobs, tools attached to jobs, the ceiling formula, retainer arithmetic, go-to-market via associations and PMS partner channels, and kill conditions.

## People

- Viewer/operator: A generalist who can read a booking-mix report, operate a Google Business Profile and a booking engine, write hospitality-grade guest messages, and hold an owner conversation about money. Hospitality experience helps and is not required; a hotel revenue-management credential is not required.
- Buyer: The owner or owner-operator of a 20-40-room US independent property. Budget is the owner's, and the buying situation is a visible commission line and a stretched front desk.
- End customer or beneficiary: The property's returning guests, who book direct at a rate the property controls; secondarily the front desk, which stops being the unowned handoff.
- Guest or outside participant required: no for the episode; yes for a real engagement (property access, extranet and PMS permissions, guest-data consent process).

## Problem

- Costly problem: Independent properties receive most of their reservations through OTAs and pay a commission on each, then have no durable contact with the guest after checkout because the OTA masks the guest's email and closes the messaging window. The property pays the same acquisition cost again for the same guest's next stay.
- Why it matters: The commission is the property's largest controllable distribution cost; OTA bookings also cancel at roughly twice the direct rate (vendor-published, to be attributed); and the property lacks the staff to own the discovery-to-return path (AHLA staffing surveys). Magnitudes are researched in the brief.
- Why now: Booking.com reworked Genius visibility in early 2026 toward relevance-based ranking, pushing properties toward deeper discounts or paid boosts; more than 15,000 European hotels have joined a collective damages action over 2004-2024 parity clauses after the ECJ ruling of September 2024; Google's free booking links give a commission-free direct placement that a small property rarely configures; and the vendor data for 2025 shows OTA share of independent bookings rising, not falling.
- Existing alternatives and budget: The owner does nothing; the owner buys a PMS/booking engine bundle and assumes it produces direct bookings; a hotel marketing agency at a published $1,500-6,000 per month, sized for 20-60+ keys; or an outsourced revenue-management provider, mostly quote-only. Spend exists in the category; the fit for the 20-40-room band is the question.

## Proposed business

- Offer: A paid direct-booking audit (fixed fee) and a monthly retainer covering three jobs: (1) findable — Google Business Profile, free booking links, accurate rate and availability; (2) bookable — direct rate parity check against the OTA, mobile booking test, cancellation-policy readability, phone coverage; (3) remembered — consent-based first-party guest capture at check-in, post-stay thank-you, review request, seasonal return offer, referral prompt. One monthly scorecard: direct share of bookings, before and after.
- Customer outcome: A documented baseline; a working direct path tested as a guest; a growing first-party guest list with recorded consent; a monthly direct-share number the owner can act on. Business impact (commission saved) remains a labeled hypothesis until measured.
- Delivery hypothesis: Audit from OTA extranet and PMS reports plus a guest-side test; fixes executed in the property's own accounts; automation (Make or n8n, a transactional email tool) drafts and schedules messages; the operator approves voice, offers, and every sensitive send.
- Revenue hypothesis: Fixed audit fee plus a flat monthly retainer priced beneath the property's modeled recovery ceiling, not against the operator's hours. Renewal depends on the direct-share number moving.
- Most important unproven assumption: **That a 20-40-room owner will pay a retainer large enough to be worth an operator's time when the recoverable commission at a realistic mix shift is only a few hundred to a little over a thousand dollars a month.** This is the ceiling problem the V1 episode never computed.

## Initial synthesis hypothesis

- Parallel A: Outsourced hotel revenue management for independents (HotelMinder, Catala, Revenuenaire) — establishes that small properties buy an ongoing commercial-management retainer from an outside specialist; mostly quote-only pricing.
- Parallel B: Hotel marketing agencies for independent properties with published retainers (Egochi from $1,500/month; boutique tiers of $3,000-6,000 for 20-60 keys) — establishes the budget category and the "direct-share reporting" deliverable.
- Parallel C: The commission-free direct components — Google free booking links (no fee), small-property booking engines with no per-booking commission (Little Hotelier Pro about $109/month), OTA-independent first-party guest capture — establish that the direct path can be built at low fixed cost.
- New combination: A recovery-first retainer that starts from the guests the property already served, treats the OTA's guest-data masking as the design constraint, prices under a computed ceiling, and reports one number. Not a marketing agency, not a revenue manager, not software resale.
- Suspected transfer risk: Agency and revenue-management retainers are bought by properties large enough to fund them. The 20-40-room band may be too small to fund any retainer that clears an operator's cost of time, which would push the real buyer up to 40-80 rooms and into the agencies' territory.

These are research directions, not evidence. The completed research brief and analogy map decide whether the transfers are valid.

## Narrative potential

- Starting state: An innkeeper gives a guest a good stay. The guest arrived through Booking.com; the property holds a masked alias, not an email; seven days after checkout the messaging window closes.
- Inciting change: The guest returns next year — through Booking.com again — and the property pays the commission a second time. Meanwhile the OTA's own 2026 programme change asks the property for a deeper discount to stay visible.
- Causal mechanism: Discovery is rented; the relationship after the stay is nobody's job; the data needed to keep it is withheld by the channel that made the introduction; the front desk is short-staffed.
- Operator build: Audit → fix the direct path → capture consent at the property → re-book known guests → report direct share monthly.
- Stakes and tradeoffs: The commission line is real but the recoverable slice is bounded; a retainer priced above the ceiling is a subscription the owner cancels; automation without hospitality judgment turns thank-yous into spam; OTA terms and consent law constrain what data can be used.
- End state: The viewer can compute a property's ceiling, decide whether the business clears their own cost of time, and knows the 30-day test that settles it.
- Visual evidence: The masked `@guest.booking.com` address on a reservation; the guest journey with the return loop drawn in two colours; the four-input ceiling arithmetic; a direct-path test on a phone; the registration card with the consent line; the before-and-after direct-share scorecard.

## Audience pull

- Exact or adjacent viewer questions: "how to get more direct bookings for a small hotel," "Booking.com commission for hotels 2026," "how much do OTAs charge," "hotel marketing consultant for independent hotels," "how to start a hospitality marketing business."
- Initial interest signals: Vendor and association research on OTA dependence (Cloudbeds 2026; HOTREC 2024); 15,000+ hotels registered for a collective action against Booking.com; a hotel-marketing agency category with published retainers aimed at independents; sustained 2024-2026 YouTube coverage of "increase direct bookings," much of it vendor-produced; Skift Research's forecast that direct digital channels overtake OTAs by 2030. To be triangulated in research.
- Timely tension: OTA share of independent bookings rose in 2025 while the largest OTA changed the terms of its loyalty visibility in 2026 and faces a multi-billion-euro parity claim in Europe; the direct tooling is cheap and the capacity to run it is absent.
- Coverage gap: Existing coverage is written for hoteliers by vendors and agencies ("ten ways to increase direct bookings"). Almost none of it addresses the operator building the service, none computes the price ceiling a small property's commission line can fund, and the guest-data masking is treated as a nuisance rather than the first design constraint of the recovery flow.
- Honest working premise: A small hotel pays to meet the same guest twice, and the booking site keeps the guest's email. Here is the service that gives the relationship back to the property — and the arithmetic that decides whether anyone can afford to sell it.

## Discovery and POV

- Search-volume status: attempted but not measurable — Google Trends returned HTTP 429 on two attempts on 2026-09-03; no licensed exact-volume tool is available to this operation. Proxy signals required.
- Operator Economy POV (scored under Step 0.3): **transferable earned judgment plus original synthesis.**
  - Transferable earned judgment: Manav spent two years in boutique hospitality as Director of Customer Experience at Coqui Coqui (Oct 2014-Oct 2016), across 4 properties and 10 departments, managing 50+ employees (`content-os/facts.md`). He was on the property side of the OTA relationship and ran the guest-experience path this service tries to give a small property.
  - Original synthesis (to be demonstrated in research): (1) the OTA guest record expires — masked email, closed messaging window — so the recovery flow must begin with consent capture at the property, not with an email tool; (2) the recovery ceiling — at a modeled 20-room property a realistic mix shift recovers only a few hundred to roughly a thousand dollars a month, which caps the retainer and moves the viable buyer to the top of the band.
- POV boundary: Manav did not own or "run a hospitality business"; he was not a revenue manager; his tenure predates the DMA, the 2026 Genius change, and current OTA programme pricing; he has never sold this service or produced a client result. Nothing in the episode may claim otherwise.

## Initial evidence status

- Buyer-problem evidence: lead found — large vendor dataset plus an association study and litigation behavior; US small-property split by size still needs an independent source.
- Budget or current-alternative evidence: lead found — agency retainers published; revenue-management pricing largely quote-only.
- Offer and delivery parallel: lead found — outsourced revenue management and independent-hotel marketing agencies exist; the recovery-first bundle at a published price is not observed.
- Economics or capacity inputs: modelable — commission mechanics are published by the OTAs themselves; ADR, occupancy, and mix shift are assumptions.
- Audience-interest signals: one signal — needs triangulation.
- Narrative engine: strong — a single guest's two stays carry the argument, and the masked email is a visual fact.

## Known blockers

1. **The ceiling.** If the modeled recoverable commission at 20-40 rooms cannot fund a retainer above roughly $750-1,250 per month, the business may only work for operators with a low cost of time or for larger properties already served by agencies.
2. **Vendor-heavy problem data.** The 63.4% OTA share and the cancellation comparison come from a company that sells the alternative. Independent corroboration exists for Europe (HOTREC), not for US small properties.
3. **Primary OTA pages not opened.** Booking.com partner help pages returned HTTP 403 on 2026-09-03; commission mechanics currently rest on secondary sources quoting them and must be opened in a browser before any script lock.
4. **Guest-data and consent law.** OTA terms prohibit marketing to masked addresses; US CAN-SPAM and, for foreign guests, GDPR apply to the first-party list. Manageable by design, not optional.
5. **Access.** A real engagement needs extranet and PMS access and a property-side consent process — permissioned work, not observable from outside.
6. **Crowded surface coverage.** "Increase direct bookings" content is abundant; the differentiated promise must be the operator-side blueprint and the ceiling honesty, or the episode collapses into a tool list.

## Intake decision

Decision: research

Reason: The buyer relationship is direct, the problem is recurring and documented from more than one direction, and a genuine editorial finding exists in the guest-data constraint and the ceiling arithmetic. The two real risks — that the band cannot fund a retainer, and that the strongest problem data is vendor-published — are both researchable and both testable in 30 days. Proceed to the research brief.
