# Narrative and audience-pull gate: Workflow-reliability sprint for small professional-service firms

Status: approved V2 Step 0.2 gate; locked 2026-08-21.

Template version: `operator-blueprint-v2-step0.2`

Candidate ID: `candidate-2026-09-03-workflow-reliability-service`

Candidate brief: `../01-candidates/candidate-2026-09-03-workflow-reliability-service.md` / `7d2ecb8fb865095409a326980440703dacfc4bcc1ace909e8d9df7ae928e686e`

Research brief: `../02-research/candidate-2026-09-03-workflow-reliability-service.md` / `687e499ffaec634d90728efb35a62725b33edbb9135b68f4631d195b3ed09876`

Analogy map: `candidate-2026-09-03-workflow-reliability-service-analogy-map.md` / `93cc76e00a717fc7589c0c6111fa57f9b3503c60ec9a9a71486a9d9a1c44eb68`

This gate asks whether the opportunity can become a compelling Operator Economy episode. It is separate from business plausibility. The historical EP003 was, on re-reading, a market-size ladder (Zapier's valuation → n8n's round → iPaaS estimates → "the solo version pays…") with a tool list and a pricing sheet attached; the question here is whether the bounded premise produces a causal story instead.

## Narrative engine

| Check | Pass condition | Result | Evidence or proposed story function | Failure or caveat |
|---|---|---|---|---|
| Operator protagonist | A specific prospective operator has a decision, capability gap, or opportunity to pursue. | **pass** | An operations-minded generalist who has been sold the automation agency by every 2026 tutorial and must decide whether the reliability job — the part nobody is selling — is a business someone will pay for | Role, not a named individual; the channel's normal form |
| Inciting change | A sourced change or persistent failure makes the old way inadequate now. | **pass** | CLM-009 — a vendor's own notice that after 31 July 2026 "workflows using deprecated steps will stop working"; CLM-010 — three intake automations silently dropping every new client until June 2026 | The dated event is one platform pair; the silent-failure case is agency-published. Strong as story, thin as statistics |
| Stakes | The viewer can see what is lost, gained, delayed, or put at risk. | **pass** | A new client's intake that never reaches the calendar or the invoice; a coordinator doing invisible integration by hand; an owner who cannot see where it failed. Adjacent scale from CLM-001 (adoption far ahead of integration) and CLM-002 (32 hours a month of administrative work) | **Consequence is shown, not measured**, for the bounded buyer. The episode may dramatise one client record; it may not state a dollar cost of failure |
| Causal mechanism | The episode can explain why the problem happens, not merely assert that it exists. | **pass** | Each tool holds part of the client's state; connections were built for the happy path; identifiers go stale (CLM-010); task caps and credit exhaustion pause scenarios and logs expire in seven days (CLM-012); nothing is watching | Genuinely mechanistic and all of it is documented by the platforms themselves |
| Build transformation | The proposed business changes the starting system through understandable operating steps. | **pass** | Follow one client record through three systems → map states and exceptions → automate only the stable path → tests against the platform's own stop conditions → alerts and a named owner → count touches before and after → monitor thirty days → recommend | Every step is showable; each contains a decision |
| Decisions and tradeoffs | The operator must make meaningful choices with constraints, alternatives, or failure modes. | **pass** | What stays human; client-owned versus operator-owned infrastructure; fixed fee versus the obligation a retainer creates; coverage versus speed; scoped access versus convenience; refuse a workflow that cannot be bounded | The retainer decision is the dramatic one: the old episode assumed it, this one has to earn it on screen |
| Payoff | The ending delivers a usable blueprint and a more informed build / test / reject decision. | **pass** | The Canvas: workflow score, exception matrix, test plan, price hypothesis with sensitivity, thirty-day pilot with kill condition. The end state may be "the test failed; do not sell this yet," which is a usable answer | Payoff must not become the old pricing sheet; every number is a labelled hypothesis |
| Visual evidence potential | The causal story can be shown through people, places, interfaces, documents, flows, comparisons, or measurable state changes. | **pass** | One client record across CRM, calendar and billing interfaces; the state map; the copy-paste; the execution log; the stale ID; the vendor's deprecation notice with its date; the alert; the test matrix; the before-and-after counter; the runbook | Strong. The deprecation notice and the silent execution log are single frames that carry the argument. Risk: a screen-recording tutorial with narration; the client record must stay the protagonist's object |

Narrative verdict: **pass**

Failure rule applied: the old episode was a market overview with a tool list. The bounded premise is a causal journey — a handoff, a dated break, a mechanism, a build, a retainer decision, a measurable end — and the tools appear only as jobs inside it.

## Audience pull

| Check | Pass condition | Result | Evidence | Failure or caveat |
|---|---|---|---|---|
| Named audience job | The intended viewer recognizes a decision or problem they may plausibly face. | **pass** | "I have been told I can start an automation agency. What is the buyer actually paying for, and can I deliver it?" — aimed at the operator, against the coverage that recruits them | The audience job is real precisely because the coverage is crowded |
| Consequential interest | At least one usable direct or adjacent source shows problem behavior, spending, adoption, risk, or active buyer attention. | **pass** | CLM-006 — listed Zapier partners with 473, 438 and 412 buyer reviews; CLM-005 — 700+ Solution Partners; CLM-001 — 46% of US small employer firms using AI with 7% fully integrated | Reviews proxy engagements, not price; the partner count is vendor-stated |
| Demand triangulation | At least two independent signals support interest. | **pass** | Four families: a US federal survey (CLM-001) with association corroboration (CLM-022); two vendor partner ecosystems with directory and criteria data (CLM-005 to CLM-008); the vendor's own dated deprecation documentation (CLM-009); independent creator attention (CLM-017). Government/institutional research (CLM-002, CLM-003) adds the adjacent problem | Only the federal and government sources are independent of the tool vendors; creator attention is seller-side and cannot count as buyer demand. Own-channel EP003 data (CLM-018) is a null result, not a signal either way |
| Timely tension | The topic contains a current change, contradiction, threat, or opening rather than generic evergreen advice. | **pass** | The contradiction is structural and dated: 2025–2026 coverage sells the build and the course (CLM-017, CLM-014), while the platforms are repricing AI steps, pausing scenarios on credit exhaustion and deprecating APIs on published dates (CLM-009, CLM-012). The job being sold is not the job that keeps paying | Vendor events recur but the specific dates will age; refresh by 2026-12-03 |
| Differentiated promise | Existing coverage leaves room for an Operator Economy synthesis, decision tool, or blueprint. | **pass** | Coverage is tutorials, "make money with n8n" videos, agency pricing guides that disclaim their own numbers, and agency case studies selling the fix after the break. Nothing found teaches workflow selection by rule stability and consequence, exception ownership, testing against platform stop conditions, measurement, and honest hours — with the retainer earned rather than assumed | **Partial gap, not a clean one.** Agencies do write about silent failures and "hosting-and-upkeep" retainers; the differentiation is the buyer-side, decision-grade treatment, and it must be delivered, not asserted |
| Honest packaging | A compelling title-and-thumbnail premise can be stated without an unsupported outcome, fear claim, or earnings promise. | **pass** | "Everyone is selling you the automation agency. Here is the job the buyer actually pays for — keeping one workflow alive when the platform changes — and what it costs to deliver." Or the date on the deprecation notice; "Who Fixes It When It Breaks?" | No income figure, no valuation, no "$5 billion," no "boring goldmine." The silent-failure story must be told as one agency's published account, not as a market statistic |

Audience-pull verdict: **pass**

### Search-volume exception

Exact-query volume is recorded as **not measurable**. A measurement attempt was made on 2026-09-03: Google Trends returned HTTP 429, no licensed keyword tool is available to this operation, and the secondary pages surfaced by search did not cite a Keyword Planner figure for the exact queries when opened (CLM-016).

The exception is properly invoked. Consequential interest passes on directory review counts and a vendor-stated partner base, and triangulation passes on four families of which two are independent of the tool vendors. "The market is new" is not offered — this market is established; what is new is the density of coverage recruiting entrants and the calendar of platform changes underneath them. The exception carries a cost: audience demand and timing cannot score above the middle of its band without a measured query signal, and the scorecard reflects that.

## Overall editorial verdict

Narrative engine: **pass**

Audience pull: **pass**

Overall editorial potential: **pass**

Story spine: `a new client's form lands in the CRM, the calendar never hears about it, and a coordinator is the integration` -> `a vendor publishes a date after which the workflows bridging those tools will stop working, and an automation built two years ago has already been silently dropping every new client` -> `each tool holds part of the client's state, the connections were built for the happy path, identifiers go stale, credits run out, logs expire, and nobody is watching` -> `an operator follows one client record through the systems, maps every state and exception, automates only the stable path, and gives failure an owner, an alert and a test` -> `fixed fee for the sprint, and the retainer only if the thirty-day window proves there is a recurring job — or the test fails and the operator does not sell it yet` -> `fewer manual touches, a logged and owned exception path, and a viewer who can score a workflow, scope a sprint, price the hours and run the pilot`

Working audience promise: Everyone is selling you the automation agency. Here is the job the buyer actually pays for — keeping one workflow alive when the platform changes — and what it costs to deliver.

Reviewer: Manav Thaker

Reviewed: 2026-09-03

Required work before reconsideration: none blocking; both gates pass. Three standards carry to editorial: (1) the silent-failure case (CLM-010) is an agency's own published account and must be attributed as such, with its hours-saved figure omitted; (2) no platform valuation, round, builder count or category size may appear as evidence of buyer demand; (3) the differentiated promise is partial and must be earned in the Canvas — if the script drifts into a tutorial or a pricing sheet, it has become the coverage it claims to correct.
