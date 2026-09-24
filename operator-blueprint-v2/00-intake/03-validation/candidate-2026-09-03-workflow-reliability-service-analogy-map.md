# Analogy map: Workflow-reliability sprint for small professional-service firms

Template status: approved V2 Step 0.2 template; locked 2026-08-21.

Template version: `operator-blueprint-v2-step0.2`

Candidate ID: `candidate-2026-09-03-workflow-reliability-service`

Candidate brief: `../01-candidates/candidate-2026-09-03-workflow-reliability-service.md` / `7d2ecb8fb865095409a326980440703dacfc4bcc1ace909e8d9df7ae928e686e`

Research brief: `../02-research/candidate-2026-09-03-workflow-reliability-service.md` / `687e499ffaec634d90728efb35a62725b33edbb9135b68f4631d195b3ed09876`

Prepared: 2026-09-03

Evidence class: **observed model**

## Synthesis thesis

This business is like a **Zapier Solution Partner** for the exact service model, delivery shape and vendor-assisted buyer channel; like an **n8n expert-partner agency** for the multi-client automation practice and the vendor's own definition of what counts as one; and like a **fixed-scope technical audit** for the paid-diagnostic entry and hours-against-fixed-fee economics. The new combination is the observed category scoped to the reliability job for one buyer, with the platform's documented failure mechanics used as the test plan and the retainer earned in a monitoring window instead of assumed in the pitch.

## Transfer records

| Analogy ID | Proposed-business component | Reference model | Source claim IDs | Relationship | Shared structure | Required adaptation | Does not prove | Break condition | Confidence | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| ANA-001 | Buyer and costly problem (the gap) | US small employer firms adopting AI faster than they integrate it | CLM-001, CLM-022 | adjacent | Same buyer class; same shape — tools adopted, processes not integrated, implementation time and finding suitable tools named as the top barriers | The federal survey is about AI tools broadly; the sprint addresses cross-tool workflow state. The transfer is from "adoption without integration" to "a handoff nobody owns" | That any given firm has a failing handoff, or what it costs | Interviews find firms' handoffs are already native-integrated or the manual bridge costs nothing they care about | medium-high | valid |
| ANA-002 | Buyer and costly problem (the failure) | Platform change breaking live small-firm workflows | CLM-009, CLM-010 | direct | Same buyer, same systems, same event — a dated API deprecation or a renamed identifier stops or silently degrades an intake workflow | None for the mechanism. The agency case's outcome numbers are set aside; only the failure shape transfers | Frequency across the market or the dollar cost to the buyer | Platform changes turn out to be rare, or the vendors' migration tooling makes them self-healing | medium | valid |
| ANA-003 | Offer and delivery | Zapier Solution Partner engagement: map, implement, SOPs, training, post-implementation support | CLM-005, CLM-011 | direct | Same deliverables in the same order for the same buyer size; vendor documents it as the standard engagement | Add baseline measurement, exception test suite, alerts, named exception owner and a monitoring window with a written recommendation. Remove the vendor-curated outcome claim | That the added reliability scope is what the buyer values, or that it fits in the modeled hours | A buyer wants only the connection and will not pay for tests, documentation or monitoring | medium | valid |
| ANA-004 | Budget and current alternative | Buyers paying vendor-listed partners at volume (directory review counts; n8n's three-active-customer threshold; agencies reporting dozens of clients) | CLM-006, CLM-007, CLM-008 | direct | Same service bought by small firms, at a scale visible in reviews and vendor criteria | Reviews prove engagements, not price. An entrant has no reviews, no tier and no directory placement | Price, margin, or that an unknown independent can win the same work | Buyers only transact through directories and tiers; entrants cannot reach them | medium | valid |
| ANA-005 | Go to market | Paid diagnostic sold ahead of implementation (technical/operational audit pattern), anchored on a live buyer question ("why did this stop working") | CLM-009, CLM-003 | adjacent / component | A bounded, cheap first engagement that reveals the problem and credits toward the fix; buyers value personalised support through an adoption journey | Must be sold into one segment the operator can already reach; directories are secondary because n8n's is a closed pilot and Zapier's tiers reward proven delivery | That the diagnostic converts, or at what rate | Fifteen conversations produce no paid diagnostic, or the fix is bought elsewhere after the diagnosis | medium-low | valid |
| ANA-006 | Economics and capacity | Fixed-scope professional services priced against delivery hours | — (structural); CLM-012 for software inputs | component | Hours × imputed rate against a fixed fee; capacity bounded by hours and by client availability; client owns production tooling so software cost is small | Every price input is a hypothesis; no observed fee exists (CLM-014 excluded, CLM-015 not usable) | That $3,500 is achievable, or that 28 hours holds | Tracked pilot hours exceed 36 twice, or the accepted price falls below the point where imputed labour is covered | medium-low | valid, inputs modeled |
| ANA-007 | Outcome measurement | Before-and-after manual-touch count plus platform execution logs and alerts | CLM-012 | component | The tools expose execution logs, error workflows, autoreplay and alerts; a count of manual touches and logged incidents is observable by the buyer | Log retention is short (7 days on entry tiers); measurement must be captured, not assumed to persist | That fewer touches equals business impact for the firm | Buyer cannot or will not baseline the current handoff | medium | valid |
| ANA-008 | Revenue model (retainer as recurring revenue) | The historical EP003 premise and 2026 agency guides: build fee plus monthly retainer as the default | CLM-020, CLM-014 | context only | Recurring maintenance sold alongside the build | **None available as evidence.** The ranges are seller-authored and one states they are not market averages | Anything about retainer price, renewal or demand | Already broken as evidence; survives only as a hypothesis tested by incidents in the monitoring window | low | **rejected as evidence; retained as hypothesis** |
| ANA-009 | Scaled relevance (valuation and category size as proof) | n8n at $5.2bn; Zapier at $310M ARR on $1.4M raised; iPaaS > $9bn | CLM-013, CLM-020, CLM-021 | context only | Large platforms exist | — | A small buyer, a service price, or operator capacity | — | low | **rejected for feasibility; context only** |

## Coverage test

| Pillar | Required status | Supporting analogies | Result | Remaining assumption and test |
|---|---|---|---|---|
| Buyer and costly problem | Must have usable direct or adjacent evidence. | ANA-001, ANA-002 | **pass** | The gap is adjacent and primary (federal survey); the failure is direct and dated (vendor notice) but its cost is shown by one agency case. Validation step 1 quantifies frequency and consequence |
| Budget or current alternative | May use direct, adjacent, or component evidence. | ANA-004 | **pass** | Spend exists at category level (700+ partners, hundreds of reviews per listed partner). Price is unobserved; validation step 3 |
| Offer and delivery | Must have a valid operating parallel or bounded first-party test. | ANA-003, ANA-007 | **pass** | Delivery shape observed in a vendor case; reliability additions are scoped and testable in the pilot |
| Go to market | May use a transferable acquisition or diagnostic-entry model. | ANA-005 | **pass, weakly** | Paid-diagnostic entry is transferred, not observed for this buyer; directory channels are closed or tiered. Validation steps 1 and 3 |
| Economics and capacity | Must have a transparent model with evidence for its inputs or explicit testable assumptions. | ANA-006; research "Modeled economics" | **pass** | Formula complete, sensitivity visible, software inputs observed (CLM-012); price and hours are labelled hypotheses; the model is more sensitive to price than to hours |
| Outcome measurement | Must define an observable buyer deliverable; business impact may remain a hypothesis. | ANA-007 | **pass** | Manual-touch count, incident log and runbook are observable; business impact is not claimed |

## Evidence-floor verdict

- Usable direct or adjacent buyer/problem evidence: **pass** — CLM-001 (adjacent, primary, current) and CLM-009 (direct, vendor documentation, dated)
- Valid analogy count: **seven valid** (ANA-001 to ANA-007), two rejected (ANA-008 as evidence, ANA-009 for feasibility). Minimum 3 — pass
- Independent source families: **three** — a US federal survey plus European government/public-bank research (CLM-001, CLM-002, CLM-003); two vendor partner ecosystems with their program pages, directories and help documentation (CLM-005 to CLM-009, CLM-012); agency and community self-reports (CLM-008, CLM-010). Minimum 2 — pass. Note that the two vendor ecosystems are counted as one family, since both sell the tools the business runs on
- Required pillars covered: **pass**
- More than one untested inference hop in a load-bearing claim: **no.** The chain runs: small firms adopt tools without integrating them (CLM-001) → platform changes stop or silently degrade the workflows that bridge them (CLM-009, CLM-010) → vendors define and list a professional-service category that does this work, and buyers review it at volume (CLM-005 to CLM-008) → the delivery shape is documented (CLM-011). The hop that would have been speculative — that the buyer pays a specific price for the reliability scope — is carried as a hypothesis and tested, not assumed
- Uncovered pillars resolvable through the bounded validation plan: **yes**

Verdict: **pass**

Reason: The floor passes because the business is observed rather than transferred: the vendors that channel demand to it describe it, count it (700+), define it (three active customers, services as main revenue), and list practitioners with hundreds of buyer reviews; and the event that makes the reliability scope sellable has a date and a vendor's own words behind it. The historical package's two weakest transfers were removed rather than stretched — ANA-008 because every retainer figure is seller-authored, ANA-009 because valuation is not demand.

The concentrated weakness is not analogy validity but source independence. Most direct evidence is published by Zapier and n8n about their own ecosystems, and the only worked failure-cost example is published by the agency that sells the fix. The independent evidence (federal, KfW, UK) covers the gap, not the price. Economics therefore rest on labelled hypotheses, and go-to-market on a transferred diagnostic-entry pattern that the pilot must prove.

## Disclosure carried forward

The episode must describe an **observed model** at category level with a **modeled** scope and price. Hands-on automation services for small firms exist, are counted and reviewed, and are defined by the platforms themselves; the specific reliability sprint, its $3,500 fee, its 28 hours and its capacity are a pilot design.

The most important assumption the viewer must hear: **the buyer is being asked to pay for reliability — tests, exception ownership, documentation, monitoring — separately from connecting the apps, and no source shows what a small firm pays for that.** The 2026 pricing ranges in circulation are written by the agencies that sell the work, and one of them says in its own text that its numbers are not market averages. The retainer is not recurring revenue by default; it is earned only if the monitoring window records a recurring reliability job.

Two things must not be said. **No historical EP003 pricing, income or "few hours a week" figure may return**, in any hedged form. And **no platform valuation, funding round, builder count or category size may be offered as proof that a small firm will buy** — that was the old hook, and it is excluded here by name.
