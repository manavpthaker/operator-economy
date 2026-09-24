# Operator Canvas feasibility gate and review: Managed inbound call coverage for owner-run residential trades contractors

Status: approved V2 Step 0.2 gate; locked 2026-08-21.

Template version: `operator-blueprint-v2-step0.2`

Candidate ID: `candidate-2026-09-03-ai-phone-answering-service`

Candidate brief: `../01-candidates/candidate-2026-09-03-ai-phone-answering-service.md` / `b2ee91c098753251fd570f934a86ffd604ded71e47fab21ef9cf4717dba55cf9`

Research brief: `../02-research/candidate-2026-09-03-ai-phone-answering-service.md` / `3d2453211585c887be85f9cd84eca359a5fbdf9011debbf1f749e967df86def1`

Analogy map: `candidate-2026-09-03-ai-phone-answering-service-analogy-map.md` / `e0fa694222947169b7b0daafadba9a84483aff4e41b422492698c60504dc8932`

## Required checks

| Check | Pass condition | Result | Evidence or artifact | Failure or caveat |
|---|---|---|---|---|
| Viewer/operator | A specific person could reasonably build or test the business. | **pass** | Research "Required skills or credentials"; CLM-014 to CLM-017; CLM-027 | Low barrier — the build is a marketplace gig at $10-90, which is also the problem. The scarce skills are call-log literacy, escalation judgment and reading the transcript that went wrong |
| Buyer | Budget owner and buying situation identifiable; buyer and end customer distinguished. | **pass** | ANA-001, ANA-002; CLM-004, CLM-011, CLM-012 | Owner of a 2-15 person residential trades contractor; homeowner is the end customer. Buying situation is identifiable and observable — the owner is answering from the van |
| Costly problem | Recurring and consequential enough to justify action. | **pass** | CLM-001, CLM-002 | Real but smaller than the legacy episode said: 14% missed (CallRail) to 48% not reaching a person (Invoca), by conflicting definitions. Both are vendor datasets. The 62% figure is excluded (CLM-003) |
| Why now | A sourced change or persistent gap explains current relevance. | **pass** | CLM-004, CLM-005, CLM-007, CLM-009, CLM-019, CLM-021 | Strongest check. The absorption and the legal shift are both dated inside the last thirteen months |
| Synthesis coherence | At least three valid parallels support the pillars without a multi-hop speculative chain. | **pass, narrowly** | Analogy map: seven valid transfers, four source families, one untested hop | The untested hop is the whole business: whether the residual layer is purchasable. ANA-003 is rejected as the operator's offer; ANA-004 is weak |
| Offer and outcome | Offer concrete; buyer receives an observable deliverable. | **pass** | Research "Proposed Operator Blueprint"; ANA-005, ANA-006, ANA-010 | Deliverables are observable — escalation rule set, state-correct greeting, monthly answer-rate report. What is not established is that the buyer values them above the $29 toggle |
| Delivery and stack | Workflow plausible; tools attached to jobs; human judgment visible; bounded test possible today. | **pass** | Research "Delivery workflow"; CLM-005, CLM-014, CLM-015 | Plausible and testable today. Human judgment owns the escalation list. Design constraint: the buyer holds the account (CLM-021), which is right for exposure and wrong for margin |
| Go to market | Credible path to an initial buyer without assuming a large audience. | **pass, weakly** | ANA-009; validation step 2 | Demo-led, re-pointed at the buyer's log. Rests on the log-and-gap demo beating "my software already does this." Named as a kill condition |
| Economics and capacity | Price, capacity, delivery cost and contribution modelable transparently, with sensitivity visible. | **pass** | ANA-007, ANA-008; CLM-005, CLM-008, CLM-010 to CLM-017; research "Modeled economics" | Transparent, and the alternatives are observed from primary pages. The base case clears imputed labor by $1,500 in year one; it works only near the legacy $300 floor, which nothing supports against $29. **The model passes as a model and fails as a business unless the fee holds** |
| Risks, permissions, and disclosure | Boundaries identified and manageable without fabrication or unauthorized action. | **pass** | Research "Risks and constraints"; CLM-018 to CLM-024 | Manageable inbound-only, with a disclosure and recording greeting, the buyer's own account, informational-only texts and no outbound AI calls. Not legal advice; verify per state before naming any. The platforms' "up to you" stance is a documented gap, not a blocker |
| First validation test | A bounded thirty-day test with a success signal and a kill or redesign condition. | **pass** | Research "Thirty-day validation plan" | Tests the one untested hop directly. The kill condition is one sentence from the buyer. Requires contractor consent for log and transcript access |

## Verdict

Verdict: **pass**

Evidence class: **adjacent synthesis**

Failed checks: none. Three checks pass narrowly or weakly — synthesis coherence, go to market, and economics — and all three fail for the same reason: the buyer's own software sells the core for $29 and nothing shows the residual layer is purchasable.

Required research before reconsideration: none blocking for the gate. The thirty-day test is the research. Before any script names a state, disclosure and recording-consent rules must be verified against primary law (CLM-019 is primary for Maine; CLM-020, CLM-023 and CLM-024 are secondary).

Required Canvas disclosure:

1. This is an **adjacent synthesis**. No independent operator was found selling a managed coverage layer on a contractor's platform receptionist, and no contractor was found paying for one.
2. **The answering itself is not the product.** Jobber sells it for $29 a month with 30 conversations; Housecall Pro and ServiceTitan sell it as add-ons; Goodcall from $79; Sameday from $449. The Canvas must show the buyer's alternatives before it shows the operator's offer.
3. **The "62% of calls go unanswered" figure is excluded.** It is a January 2016 SEO-agency post about 85 businesses. The usable range is 14% missed (CallRail, 1.1M leads) to 48% not reaching a person (Invoca, 70M+ calls), by conflicting definitions, from two vendors.
4. **The build is a $10-90 gig.** No setup fee from the old episode may be presented as a market rate.
5. **The buyer should own the platform account.** Under the CIPA capability theory, the party with technical access to call data is exposed. This removes per-minute margin from the operator's model by design.
6. **Nothing here is legal advice.** Disclosure, recording consent and text-message consent vary by state; the operator verifies locally. Outbound AI calling is excluded entirely.
7. **Every operator-side economic figure is modeled**, and the base case barely clears imputed labor. The disclosure `modeled scenario, not observed performance or an earnings forecast` applies to every number.
8. **The likelier result of the thirty-day test is "no."** The Canvas must present a negative result as a legitimate outcome.

Reviewer: Manav Thaker

Reviewed: 2026-09-03

Research refresh date: 2026-12-03 for platform, pricing, funding, marketplace and creator claims; 2027-03-03 for legal claims; 2027-09-03 for BLS data

## Non-waivable boundary

An owner override may select a strategically important candidate below the numeric score threshold. It may not convert a failed feasibility check into a pass, waive missing evidence or permissions, or present a modeled business as observed performance.
