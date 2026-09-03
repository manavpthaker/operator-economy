# Operator Canvas feasibility gate and review: AI support-desk implementation for small DTC brands

Status: approved V2 Step 0.2 gate; locked 2026-08-21.

Template version: `operator-blueprint-v2-step0.2`

Candidate ID: `candidate-2026-09-03-ai-implementation-service`

Candidate brief: `../01-candidates/candidate-2026-09-03-ai-implementation-service.md` / `9e7df3673037d133364e28508ba39250f76c09775b269c2f9621ec2f4922e8b6`

Research brief: `../02-research/candidate-2026-09-03-ai-implementation-service.md` / `fbf55f1f8e9ad6dc8cbee1499ccc0ae86b7b72c86b33fd651da61c1cf5702ee9`

Analogy map: `candidate-2026-09-03-ai-implementation-service-analogy-map.md` / `db3b2520a11ae24903ee951369a8a31315be5d8bd4e330e663e7a9f3ed7e0715`

## Required checks

| Check | Pass condition | Result | Evidence or artifact | Failure or caveat |
|---|---|---|---|---|
| Viewer/operator | A specific person could reasonably build or test the business with identifiable skills, resources, or a learnable path. | **pass** | Research "Required skills or credentials"; CLM-005, CLM-006 | No credential is needed to configure a helpdesk; a $10/month Starter plan is a complete test bench. The barrier is judgment about tickets and policy, plus writing — learnable, and exactly what the audience has |
| Buyer | The budget owner and buying situation are identifiable through direct or credible adjacent evidence. Buyer and end customer are distinguished when they differ. | **pass, with a verification condition** | ANA-002; CLM-006, CLM-010, CLM-013 | Buyer is the founder or CX lead of a brand in the 1,000–5,000-ticket band below the vendor's hands-on onboarding threshold. The band is anchored in vendor ticket tiers (primary). **The revenue threshold that defines the boundary (CLM-013) was not opened at source and must be verified before script** |
| Costly problem | The underlying problem is recurring and consequential enough to justify action; the exact new solution need not be established. | **pass, with a limit** | ANA-001; CLM-003, CLM-004, CLM-005 | Recurring (every ticket the unconfigured agent hands back) and mechanistically documented by the vendor. Consequence is quantified at enterprise scale only; the small-brand dollar consequence is modeled. Validation step 1 measures it at three brands |
| Why now | A sourced change or persistent gap explains why the opportunity is worth examining now. | **pass** | CLM-007, CLM-008, CLM-001, CLM-002, CLM-014 | Outcome-based pricing (2024–2026) makes non-resolution visible on the bill; small-firm adoption rising but under 20%; Klarna's reversal made the cost-quality tradeoff public |
| Synthesis coherence | At least three valid parallels jointly support the required evidence pillars without a multi-hop speculative chain. | **pass** | Analogy map: six valid transfers (one weak), four independent source families, one stated hop | Two transfers rejected rather than stretched: legacy agency economics (ANA-008) and Accenture bookings (ANA-009) |
| Offer and outcome | The proposed offer is concrete, and the buyer receives an observable deliverable or state change. Business impact may remain a labeled hypothesis. | **pass** | Research "Proposed Operator Blueprint"; ANA-003, ANA-006 | Configured agent, written rule set, never-automate list, and a before/after on the vendor's own verified-resolution meter. Agent-hour and CSAT impact remain hypotheses. **The meter measures containment, not correctness** — the report must also log wrong answers |
| Delivery and stack | The workflow is plausible; tools are attached to jobs, required human judgment remains visible, and a bounded test is possible today. | **pass** | Research "Delivery workflow"; CLM-005; validation steps 1–2 | The vendor's own go-live checklist is the skeleton; the operator's judgment (safe / conditional / never; handover triggers; actions off by default) is the product. Testable today on a sandbox. **If the deliverable collapses to configuration clicks, the vendor's wizard wins and this check should be re-scored** |
| Go to market | There is a credible path to reach, diagnose, and win an initial buyer without assuming a large audience. It may be transferred from a valid adjacent model. | **pass, weakly** | ANA-004; CLM-009; validation step 3 | Paid ticket audit as diagnostic entry; Shopify and DTC founder communities as the primary reach; the vendor partner marketplace as an unverified second path. **If the partner program refuses individuals and community outreach yields nothing in fifteen conversations, this fails.** Named as a kill condition |
| Economics and capacity | Price, capacity, delivery cost, and contribution can be modeled transparently. Observed and transferred inputs are separated from assumptions and sensitivity is visible. | **pass** | ANA-005; CLM-006, CLM-007, CLM-008; research "Modeled economics" | Formula complete; buyer side anchored in vendor prices; the buyer-payback model defines a minimum buyer instead of assuming one. **Every operator-side input and the brand's cost per ticket are modeled**; the 10→30-point lift is a hypothesis. Disclosure present |
| Risks, permissions, and disclosure | Legal, ethical, privacy, access, credential, platform, guest, analogy, and earnings-claim boundaries are identified and manageable without fabrication or unauthorized action. | **pass, with the platform risk named as the defining constraint** | Research "Risks and constraints" | Customer-data access is manageable with scoped, client-controlled admin and written consent; money-moving actions stay off without per-action sign-off. **Vendor dependency is not a blocker but it is the business's defining risk**: the vendor sells the same service, ships a wizard, and can auto-configure. The Canvas must carry it as a kill condition, not a footnote |
| First validation test | A prospective operator can run a bounded thirty-day test with a success signal and a kill or redesign condition. | **pass** | Research "Thirty-day validation plan" | Three tests hit the three real unknowns — does the wizard already do the job, what lift is achievable at what hours, and will a sub-threshold brand pay. Each kill condition is reachable inside thirty days |

## Verdict

Verdict: **pass**

Evidence class: **observed model** for the service category; solo economics modeled

Failed checks: none. Two checks pass weakly (go to market) or conditionally (buyer boundary verification).

Required research before reconsideration: none blocking for the gate. **Carried to editorial and to any promotion record:**

1. Open CLM-013 at source (or confirm with the vendor in writing) before the script states where dedicated onboarding begins. The buyer definition rests on it.
2. Confirm the Gorgias per-resolution price on the vendor's own page (CLM-007) before any public price statement.
3. Validation step 1 must be run before the episode describes what the wizard does and does not configure; the package currently infers this from the vendor's go-live docs (CLM-005) and a 2024 release note (CLM-011), not from a test.

Required Canvas disclosure:

1. This is an **observed model for the service category**: implementation and optimization of an ecommerce helpdesk's AI agent is sold today by certified agencies and by the vendor itself. **No solo operator was found selling it at disclosed economics.**
2. **The vendor can close the gap.** The business exists between the vendor's self-serve wizard and its hands-on onboarding for larger brands. A product release or a lower onboarding threshold can shrink or erase the job.
3. **The "adopted but not working" finding is enterprise evidence.** The small-brand version is a hypothesis this package has not measured.
4. **Every operator-side economic figure is modeled** — fee, hours, capacity, contribution — and so is the buyer's payback, which depends on an assumed cost per ticket. The 10→30-point resolution lift is a hypothesis to be measured, not a result.
5. **The measure counts containment, not correctness.** A rising verified-resolution rate is not proof of good answers; the never-automate list and the wrong-answer log are part of the deliverable for that reason.
6. **No legacy figure may appear**: not $40K a month, not 85–90% margins, not $2–5K project bands, not "$5.9 billion," not any automation-rate claim from vendor or competitor marketing.

Reviewer: Manav Thaker (Reviewer A pass, produced by the Step 0 review process)

Reviewed: 2026-09-03

Research refresh date: 2026-12-03 for vendor, product, partner-program and audience claims; 2027-03-03 for institutional research

## Non-waivable boundary

An owner override may select a strategically important candidate below the numeric score threshold. It may not convert a failed feasibility check into a pass, waive missing evidence or permissions, or present a modeled business as observed performance.
