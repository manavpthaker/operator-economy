# Analogy map: Direct-booking recovery service for small independent lodging

Template status: approved V2 Step 0.2 template; locked 2026-08-21.

Template version: `operator-blueprint-v2-step0.2`

Candidate ID: `candidate-2026-09-03-direct-booking-recovery`

Candidate brief: `../01-candidates/candidate-2026-09-03-direct-booking-recovery.md` / `70e5a289bf15f5603f9ebd0cb4d958116852d76bcd5f2e620427f3753c342c9c`

Research brief: `../02-research/candidate-2026-09-03-direct-booking-recovery.md` / `07c61fa3fca535f9569670dbe73c6e823eaa3ab33ba5e67f7c22519a5194e5d7`

Prepared: 2026-09-03

Evidence class: **adjacent synthesis**

## Synthesis thesis

This business is like **outsourced hotel revenue management** for an ongoing outside commercial-management retainer bought by an independent that cannot justify a hire, like an **independent-hotel marketing agency** for the budget category and the direct-share reporting deliverable, and like the **commission-free direct components** (free booking links, fixed-fee booking engines, first-party consent capture) for a low-fixed-cost direct path. The new combination is a recovery-first retainer that starts from guests the property already served, treats OTA data masking as the first design constraint, prices under a computed ceiling, and reports one number.

## Transfer records

| Analogy ID | Proposed-business component | Reference model | Source claim IDs | Relationship | Shared structure | Required adaptation | Does not prove | Break condition | Confidence | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| ANA-001 | Buyer and costly problem | The independent property paying OTA commission on a majority of bookings and losing the post-stay relationship | CLM-001, CLM-002, CLM-003, CLM-004, CLM-008 | direct | Same buyer, same recurring cost, same withheld data | Narrow from "independent hotels" to the 20-40-room US band; the level of dependence is global/vendor (63.4%) or European/association (49% non-direct) and not yet US-size-specific | That the band's commission line is large enough to fund a retainer | US properties in the band turn out to be on base commission with OTA share well below the vendor figure | high for the problem, medium for the band | valid |
| ANA-002 | Offer and delivery | Outsourced hotel revenue management for independents | CLM-011 | adjacent | An outside specialist runs an ongoing commercial function on retainer for a property too small to hire | Scope shifts from pricing and channel strategy to recovery of known guests and direct-path repair; the specialist credential is replaced by hospitality-marketing judgment | What a 20-40-room property pays; that the buyer wants recovery rather than pricing | Owners in the band see revenue management and marketing as one purchase and buy it from the agency or the PMS vendor | medium | valid |
| ANA-003 | Budget or current alternative; outcome measurement | Independent-hotel marketing agencies with published retainers and direct-share reporting | CLM-011 | adjacent | The same buyer already funds outside help aimed at direct bookings and accepts direct share as the reported outcome | The solo offer must sit below the $1,500 agency floor and narrower in scope; the agency's ad-spend management is dropped | That the band funds the agency price; agency tier guidance is self-published with no stated basis | Agencies already retain 20-40-room properties at prices owners prefer | medium | valid |
| ANA-004 | Delivery and economics (direct path cost) | Commission-free direct components: Google free booking links, fixed-fee booking engine, vendor-reported 3.5% direct cost | CLM-009, CLM-010, CLM-014 | component | The direct channel can be built and run at a fixed monthly cost with no per-booking commission | The property, not the operator, owns the tools; the operator's contribution is configuration, testing, and judgment | That the tools produce direct bookings by themselves; the 3.5% direct-cost figure is a vendor's own client base | Connectivity partner or PMS cannot expose free booking links; direct cost for a small property runs well above 5% | high for capability, medium for cost | valid |
| ANA-005 | Delivery (recovery flow design constraint) | OTA guest-data masking and expiry | CLM-008 | component and direct | The channel that made the introduction withholds the email and closes the messaging window, so recovery must begin with consent capture at the property | Consent capture must be designed into check-in and WiFi; OTA terms and CAN-SPAM/GDPR govern the list | That guests will consent, or that a consented list re-books at any given rate | OTAs begin sharing real contact details, or consent rates at check-in are negligible | high for the constraint, unknown for the response | valid |
| ANA-006 | Economics and capacity (the ceiling) | Property-side arithmetic: commission saved on a modeled mix shift minus direct cost | CLM-001, CLM-005, CLM-014, CLM-019 | component (modeled) | Any recovery retainer must be paid from recovered commission; the property's inputs bound the price | Inputs are a global vendor share, a secondary commission band, and an assumed 10-point shift; every input is testable in an audit | That any property achieves a 10-point shift; that the owner reasons this way | Measured mix shifts are below 5 points, or the commission profile in the band is base-rate only | medium | valid as a model, not as an observation |
| ANA-007 | Why now and audience pull | Association-backed collective damages action and the 2026 Genius change | CLM-005, CLM-007 | adjacent (Europe) and direct (programme change) | Hotels are acting on OTA economics at scale; the largest OTA is changing the price of visibility | European litigation is not US behavior; the Genius change is a visibility rule, not a commission change | That US small properties feel the same pressure, or that litigation implies willingness to pay for a service | The claim fails or settles trivially; Genius reverts | medium | valid, context and timing only |
| ANA-008 | Operator feasibility (labor value) | ZipRecruiter freelance hotel revenue-management pay as carried in V1 | CLM-015 | — | — | — | Anything: not opened, and salary is not service pricing | already broken | — | **rejected** |
| ANA-009 | Outcome (business impact) | Vendor RevPAR-uplift claims (Catala +9%; V1's "5-15%") | CLM-011 | — | — | — | Anything about outcome: seller-published claims about the service being sold | already broken | — | **rejected** |

## Coverage test

| Pillar | Required status | Supporting analogies | Result | Remaining assumption and test |
|---|---|---|---|---|
| Buyer and costly problem | Must have usable direct or adjacent evidence. | ANA-001 | **pass** | Level of dependence in the US 20-40-room band is unverified; validation step 1 measures it on three properties |
| Budget or current alternative | May use direct, adjacent, or component evidence. | ANA-003, ANA-002 | **pass** | Agency and revenue-management spend exists; whether the band funds it is validation steps 2-3 |
| Offer and delivery | Must have a valid operating parallel or bounded first-party test. | ANA-002, ANA-004, ANA-005 | **pass** | The recovery-first bundle is not observed at a published price; the audit is the bounded first-party test |
| Go to market | May use a transferable acquisition or diagnostic-entry model. | ANA-003 (diagnostic entry via the ceiling calculation), ANA-002 (association and PMS-partner referral) | **pass, weakly** | Rests on the ceiling calculation opening the conversation and on associations/partners referring; validation step 3 |
| Economics and capacity | Must have a transparent model with evidence for its inputs or explicit testable assumptions. | ANA-006, ANA-004 | **pass** | Buyer-side inputs are sourced (with the commission band currently secondary); the mix shift, price, hours, and renewal are modeled and testable |
| Outcome measurement | Must define an observable buyer deliverable; business impact may remain a hypothesis. | ANA-003, ANA-005 | **pass** | Deliverable is observable — baseline, tested direct path, consented list, monthly direct share. Commission saved is a hypothesis and stays one |

## Evidence-floor verdict

- Usable direct or adjacent buyer/problem evidence: **pass** — ANA-001 is a direct relationship supported by a vendor dataset, an association study, two SEC-filed take rates, and the guest-data policy
- Valid analogy count: **seven valid** (ANA-001 through ANA-007, with ANA-006 valid only as a model and ANA-007 as timing), two rejected (ANA-008, ANA-009). Minimum 3 — pass
- Independent source families: **four** — SEC filings (CLM-003, CLM-004), hotel-association study and association-backed litigation (CLM-002, CLM-007), lodging-association surveys (CLM-012), platform primary documentation (CLM-009). Vendor sources (CLM-001, CLM-010, CLM-011, CLM-014) form a fifth family that is used but not counted. Minimum 2 — pass
- Required pillars covered: **pass**
- More than one untested inference hop in a load-bearing claim: **no.** The chain runs: properties pay commission on most bookings (CLM-001/CLM-002, with the OTAs' take rates as the independent floor) → the OTA withholds the guest's contact (CLM-008) → the direct path can be built commission-free (CLM-009/CLM-010) → outside commercial help is already bought on retainer (CLM-011) → therefore a recovery retainer is sellable **if** it prices under the ceiling (ANA-006). The single untested hop is the last one, and it is the first validation test. The hop that *would* have been speculative — that the service produces a given mix shift or RevPAR uplift — is excluded (ANA-009) rather than assumed
- Uncovered pillars resolvable through the bounded validation plan: **yes**

Verdict: **pass**

Reason: The floor passes on a direct buyer relationship and unusually strong problem evidence — the OTAs' own filings, an association study, a 15,000-hotel damages action, and the platform's own guest-data policy. Two transfers were removed rather than stretched: the salary data that V1 used as a labor-value proxy (ANA-008) and the vendors' outcome claims (ANA-009). The concentrated weakness is ANA-006: the economics pass as a transparent model whose most important input — the mix shift — is a hypothesis, and the model's own output says the retainer is small. The floor is met; the business may still be too thin at the bottom of the band.

## Disclosure carried forward

The episode must describe an **adjacent synthesis**. No verified operator was found selling a recovery-first audit-plus-retainer to 20-40-room properties at disclosed economics.

The most important assumption the viewer must hear: **the retainer is bounded by the property's own recoverable commission, and at 20 rooms that bound is roughly a thousand dollars a month on modeled inputs.** The service exists as a business only if owners pay under that line and renew, and only near the top of the band does it clear an ordinary cost of time. The episode must present the ceiling as arithmetic the viewer runs, not as a market price.

Three things must not be said. **No commission saved or direct share gained may be stated as an observed result.** **No RevPAR uplift may be attributed to the service** — those figures are published by the firms selling it and are excluded. **Nothing may imply the property should leave OTAs**, and the OTA share, cancellation, and programme figures must be attributed to Cloudbeds and to the OTAs' own pages every time they are used — with the Booking.com pages opened in a browser before lock, because on 2026-09-03 they could not be.
