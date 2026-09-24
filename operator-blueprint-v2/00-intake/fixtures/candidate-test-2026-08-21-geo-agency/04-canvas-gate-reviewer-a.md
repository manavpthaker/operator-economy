# TEST FIXTURE — Operator Canvas feasibility review: GEO agency

Status: completed test review; not an active candidate decision

Template version: `operator-blueprint-v2-step0.1`

Candidate ID: `candidate-test-2026-08-21-geo-agency`

Candidate brief: `01-candidate.md` / `5cb0919e55edf3a0694e1ba962ab1956e54e87e4c65f0dbcbbd5594580f51ddd`

Research brief: `02-research.md` / `b8983b9292b92f241866da0260f754ed65515a8a6778861d47fd62ab165e02a3`

This is a separate pass/fail gate. It does not add points to the V4 topic score. A pass means the package contains enough honest operating logic to begin editorial work; it does not mean the business is guaranteed to work.

## Required checks

| Check | Pass condition | Result | Evidence or artifact | Failure or caveat |
|---|---|---|---|---|
| Viewer/operator | A specific person could reasonably build the business with identifiable skills, resources, or a learnable path. | pass | `01-candidate.md` viewer/operator and capability sections; `02-research.md` proposed blueprint | The role is coherent, but the service has not been field-tested. |
| Buyer | The budget owner and buying situation are identifiable. Buyer and end customer are distinguished when they differ. | fail | `02-research.md` buyer problem | “Marketing or communications leader” is only a hypothesis; the budget, trigger, and decision process are unknown. |
| Costly problem | The problem is recurring and meaningful enough to justify action; it is not merely an interesting trend. | fail | CLM-001 through CLM-004 | No usable evidence establishes frequency, business cost, existing spend, or willingness to act. |
| Why now | A sourced change or persistent gap explains why the opportunity is worth examining now. | fail | CLM-002 and CLM-003 | Both are frozen research leads. Neither is refreshed or sufficient to establish current demand. |
| Offer and outcome | The proposed offer is concrete, and the buyer receives an observable outcome rather than vague transformation. | pass | `02-research.md` proposed Operator Blueprint | A bounded baseline and source-gap diagnostic is observable; it must not be sold as guaranteed visibility or revenue. |
| Delivery and stack | The operating workflow is plausible; tools are attached to jobs, and required human judgment remains visible. | pass | `02-research.md` delivery workflow and technology and human stack | Exact tools, access boundaries, repeatability, and hours still require a manual test. |
| Go to market | There is a credible path to reach, diagnose, and win an initial buyer without assuming a large audience. | fail | `02-research.md` go-to-market path | “Interview a narrow segment” is a validation action, not yet a specific reachable segment, channel, buying trigger, or initial sales path. |
| Economics | Pricing, delivery cost, and value can be discussed honestly; estimates and missing market prices remain explicit. | fail | CLM-001; `02-research.md` pricing and margin | Unknown price, hours, delivery cost, buyer value, and margin prevent an honest business model. |
| Risks and permissions | Legal, ethical, privacy, access, credential, platform, and guest dependencies are identified and do not require fabrication or unauthorized action. | fail | `02-research.md` risks and constraints | Risks are named, but client-access rules, platform terms, claims substantiation, and regulated-category boundaries remain unresolved. |
| First validation test | A prospective operator can run a bounded thirty-day test with a success signal and a kill or redesign condition. | pass | `02-research.md` thirty-day validation plan | Any live brand audit requires consent; a paid pilot cannot promise placement or revenue. |

## Verdict

Verdict: fail

Failed checks: buyer; costly problem; why now; go to market; economics; risks and permissions

Required research before reconsideration: Verify one buyer role and purchase trigger; measure the problem's frequency and cost; refresh the category and competitive landscape; obtain independent small-operator and scaled-market evidence; define a reachable initial segment; measure delivery hours, price, value, and margin; review platform, permission, legal, and claims boundaries.

Reviewer: Reviewer A — direct Canvas pass using the frozen fixture package

Reviewed: 2026-08-21

Research refresh date: not completed; required before reconsideration

## Non-waivable boundary

An owner override may select a strategically important candidate below the numeric score threshold. It may not convert a failed feasibility check into a pass or waive missing evidence, permissions, or truth constraints.
