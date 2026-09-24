# Operator Canvas feasibility gate and review: Workflow-reliability sprint for small professional-service firms

Status: approved V2 Step 0.2 gate; locked 2026-08-21.

Template version: `operator-blueprint-v2-step0.2`

Candidate ID: `candidate-2026-09-03-workflow-reliability-service`

Candidate brief: `../01-candidates/candidate-2026-09-03-workflow-reliability-service.md` / `7d2ecb8fb865095409a326980440703dacfc4bcc1ace909e8d9df7ae928e686e`

Research brief: `../02-research/candidate-2026-09-03-workflow-reliability-service.md` / `687e499ffaec634d90728efb35a62725b33edbb9135b68f4631d195b3ed09876`

Analogy map: `candidate-2026-09-03-workflow-reliability-service-analogy-map.md` / `93cc76e00a717fc7589c0c6111fa57f9b3503c60ec9a9a71486a9d9a1c44eb68`

## Required checks

| Check | Pass condition | Result | Evidence or artifact | Failure or caveat |
|---|---|---|---|---|
| Viewer/operator | A specific person could reasonably build or test the business with identifiable skills, resources, or a learnable path. | **pass** | Research "Required skills or credentials"; CLM-012 (tools are accessible from $12–$30/month) | No licence; the barrier is process discovery, test design and the discipline to refuse unbounded work — learnable, and the point of the Canvas |
| Buyer | The budget owner and buying situation are identifiable through direct or credible adjacent evidence. Buyer and end customer are distinguished when they differ. | **pass** | ANA-001, ANA-004; CLM-001, CLM-006 | Owner or operations lead of a 5–50-person professional-service firm; end customer is the coordinator and the client whose intake stalls. The buying situation (a handoff that just broke, or one that costs a person's time) is identifiable but not observable from outside, which makes the diagnostic entry necessary |
| Costly problem | The underlying problem is recurring and consequential enough to justify action; the exact new solution need not be established. | **pass** | ANA-001, ANA-002; CLM-001, CLM-002, CLM-009, CLM-010 | Recurring: adoption outruns integration in a primary federal survey; platform change is on a calendar. Consequential: shown by a dated vendor notice and one agency case. **Cost to this buyer is unquantified** and is validation step 1 |
| Why now | A sourced change or persistent gap explains why the opportunity is worth examining now. | **pass** | CLM-001, CLM-009, CLM-012, CLM-017, CLM-022 | Adoption without integration; 2026 deprecations, AI-step repricing and credit-pause mechanics; a coverage market recruiting entrants to sell the build |
| Synthesis coherence | At least three valid parallels jointly support the required evidence pillars without a multi-hop speculative chain. | **pass** | Analogy map: seven valid transfers, three source families, two rejected transfers named | Vendor-heavy: the two partner ecosystems are counted as one family. No load-bearing claim relies on more than one untested hop; the price hop is carried as a hypothesis |
| Offer and outcome | The proposed offer is concrete, and the buyer receives an observable deliverable or state change. Business impact may remain a labeled hypothesis. | **pass** | Research "Proposed Operator Blueprint"; ANA-003, ANA-007 | Map, implementation, test record, runbook, access inventory, alert path, named owner, before-and-after manual-touch count, written recommendation. Business impact is not claimed |
| Delivery and stack | The workflow is plausible; tools are attached to jobs, required human judgment remains visible, and a bounded test is possible today. | **pass** | Research delivery workflow steps 1–8; CLM-012 | Tools attached to jobs (runner the client already pays for; logs, alerts, error workflows verified as current features). Human judgement owns selection, exceptions and refusal. A paid sprint can be run this month |
| Go to market | There is a credible path to reach, diagnose, and win an initial buyer without assuming a large audience. It may be transferred from a valid adjacent model. | **pass, weakly** | ANA-005; research "Go-to-market path"; CLM-003, CLM-009 | Paid diagnostic in one reachable segment, anchored on a live 2026 buyer question. Directories are secondary: n8n's is a closed pilot, Zapier's tiers reward proven delivery. **Conversion for an unknown independent is unproven** and is a named kill condition |
| Economics and capacity | Price, capacity, delivery cost, and contribution can be modeled transparently. Observed and transferred inputs are separated from assumptions and sensitivity is visible. | **pass** | Research "Modeled economics"; ANA-006; CLM-012, CLM-014, CLM-015 | Formula complete; software inputs observed; price, hours, capacity and acquisition are labelled hypotheses; price sensitivity shown and dominant. **No observed fee exists** — every 2026 range is seller-authored and marketplaces were inaccessible on 2026-09-03 |
| Risks, permissions, and disclosure | Legal, ethical, privacy, access, credential, platform, guest, analogy, and earnings-claim boundaries are identified and manageable without fabrication or unauthorized action. | **pass** | Research "Risks and constraints" | Client data access is the defining constraint and is manageable: written consent, least privilege, client-owned accounts, test data, access inventory and revocation, exclusion of privileged or regulated workflows without review. No guest required. Earnings boundary explicit: no historical EP003 figure returns |
| First validation test | A prospective operator can run a bounded thirty-day test with a success signal and a kill or redesign condition. | **pass** | Research "Thirty-day validation plan" | Ten screen-share interviews, three scored maps, two paid diagnostics, one paid sprint at a pre-declared price. Kill conditions are reachable and hit the three real unknowns: consequence, price, and deliverability within hours |

## Verdict

Verdict: **pass**

Evidence class: **observed model**

Failed checks: none

Required research before reconsideration: none blocking. Two items must be attempted before editorial lock, and their results recorded in a research refresh: (1) an observed asking-price sample from Upwork or Fiverr via a browser session, labelled as asking prices; (2) an exact-query search measurement via a licensed tool or a working Google Trends session. Neither can convert the modeled price into an observed one; both would narrow the widest uncertainty.

Required Canvas disclosure:

1. This is an **observed model at category level**. Hands-on automation services for small firms exist, are counted (700+ Zapier Solution Partners), defined (n8n: automation services as main revenue, three active customers) and reviewed at volume. **The specific reliability sprint, its scope, its $3,500 fee, its 28 hours and its capacity are a pilot design**, not observed performance.
2. **No independent price for this work exists.** Every 2026 pricing range in circulation is written by an agency selling the work, and one says in its own text that its numbers are not market averages. The Canvas must show the price as a hypothesis with its sensitivity.
3. **The retainer is not recurring revenue by default.** It is offered only if the thirty-day monitoring window records incidents, a response obligation and a buyer willing to pay. The old episode assumed it; this one must earn it.
4. **The failure evidence is a vendor notice and one agency's published case.** The Pipedrive deprecation is dated and primary. The silent-failure story is Connex Digital's own account of its own work, and its hours-saved figure may not be stated as a result.
5. **No platform valuation, funding round, builder count or category size may be used as evidence that a small firm will buy.** They are context only, and they were the old hook.
6. **Client data is the operating risk.** Least privilege, client-owned accounts, test data, an access inventory and a revocation plan are conditions of the offer. Privileged or regulated workflows are out of scope for a generalist sprint without qualified review.
7. **Every operator-side figure is modeled.** Disclosure on every model: `modeled scenario, not observed performance or an earnings forecast`.

Reviewer: Manav Thaker

Reviewed: 2026-09-03

Research refresh date: 2026-12-03 for platform, partner-program, directory, marketplace and audience claims; 2027-03-03 for government and institutional survey claims

## Non-waivable boundary

An owner override may select a strategically important candidate below the numeric score threshold. It may not convert a failed feasibility check into a pass, waive missing evidence or permissions, or present a modeled business as observed performance.
