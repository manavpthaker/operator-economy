# Narrative and audience-pull gate: AI support-desk implementation for small DTC brands

Status: approved V2 Step 0.2 gate; locked 2026-08-21.

Template version: `operator-blueprint-v2-step0.2`

Candidate ID: `candidate-2026-09-03-ai-implementation-service`

Candidate brief: `../01-candidates/candidate-2026-09-03-ai-implementation-service.md` / `9e7df3673037d133364e28508ba39250f76c09775b269c2f9621ec2f4922e8b6`

Research brief: `../02-research/candidate-2026-09-03-ai-implementation-service.md` / `fbf55f1f8e9ad6dc8cbee1499ccc0ae86b7b72c86b33fd651da61c1cf5702ee9`

Analogy map: `candidate-2026-09-03-ai-implementation-service-analogy-map.md` / `db3b2520a11ae24903ee951369a8a31315be5d8bd4e330e663e7a9f3ed7e0715`

## Narrative engine

| Check | Pass condition | Result | Evidence or proposed story function | Failure or caveat |
|---|---|---|---|---|
| Operator protagonist | A specific prospective operator has a decision, capability gap, or opportunity. | **pass** | An ops or CX generalist deciding whether the work between "AI bought" and "AI working" is a service they can sell, and to whom | Role, not a named person — the channel's normal form |
| Inciting change | A sourced change or persistent failure makes the old way inadequate now. | **pass** | Outcome-based per-resolution pricing (CLM-008 announced 2024-08-28; CLM-007) makes non-resolution visible on the bill; adoption is rising but under 20% for small firms (CLM-001, CLM-002) | The pricing change is the vendor's; the "old way" (agents answering everything) is inadequate only if the brand's volume is high enough — hence the buyer band |
| Stakes | The viewer can see what is lost, gained, delayed, or put at risk. | **pass, with a limit** | Agent hours spent on order-status tickets; wrong refunds when handover rules are loose; the Klarna reversal as the cost-versus-quality warning (CLM-014); for the operator, a fixed fee for an outcome the vendor's next release could make free | **The small-brand dollar stake is modeled, not measured.** The episode must show stakes through one brand's queue and the modeled payback, not through a statistic |
| Causal mechanism | The episode can explain why the problem happens, not merely assert it. | **pass** | The agent needs knowledge, skills and handover rules or it hands tickets back — the vendor's own go-live docs say so (CLM-005); the vendor's hands-on onboarding starts above this brand's size (CLM-010, CLM-013); nobody at a two-agent brand owns the work. Enterprise research names the same "learning gap" (CLM-003) | Genuinely mechanistic and showable on the settings screen itself. The enterprise finding must be labeled as enterprise |
| Build transformation | The business changes the starting system through understandable operating steps. | **pass** | Audit the queue → safe / conditional / never → write the rules → test in the playground → go live on one channel → tune for two weeks → measure on the vendor's meter | Every step is showable and each contains a decision; the risk is that it plays as a product tutorial unless the decisions carry the screen time |
| Decisions and tradeoffs | Meaningful choices with constraints, alternatives, or failure modes. | **pass** | Which intents are safe; whether money-moving actions are enabled; where the handover fires; cost versus quality; whether to build on a vendor that can erase the job | **Strong.** The never-automate list is the episode's central object and a real judgment, not a checklist |
| Payoff | The ending delivers a usable blueprint and a more informed build / test / reject decision. | **pass** | Canvas plus the minimum-buyer arithmetic (roughly 1,000 tickets a month), the fee-versus-payback formula, and a reachable kill condition (the wizard does the job) | Payoff may be "not at my fee" or "not on this vendor," which is useful |
| Visual evidence potential | The causal story can be shown through people, places, interfaces, documents, flows, comparisons, or measurable state changes. | **pass** | The queue grouped by intent; the empty knowledge panel; the handover log; a playground test failing then passing; the resolution meter before and after; the one-page never-automate list; the vendor's onboarding-tier ladder | Interfaces are vendor UI and need permission or recreation; a real brand's tickets need redaction |

Narrative verdict: **pass**

Failure rule check: this is not a market overview (the legacy episode's failure — Accenture at the top, a blog at the bottom) and not a tool list. One brand, one queue, one agent left at defaults, one build, one measured ending. The chronology risk is a Gorgias tutorial; the mitigation is that the story's spine is the never-automate decision, which a tutorial cannot make for the viewer.

## Audience pull

| Check | Pass condition | Result | Evidence | Failure or caveat |
|---|---|---|---|---|
| Named audience job | The intended viewer recognizes a decision or problem they may plausibly face. | **pass** | "Can I sell the work between bought and working, and to whom?" — aimed at the operator; the merchant-side question ("why isn't my AI agent resolving anything?") is the doorway | Distinct from existing coverage, which is written for merchants or for generic agency-founders |
| Consequential interest | At least one usable direct or adjacent source shows problem behavior, spending, adoption, risk, or active buyer attention. | **pass** | CLM-002 — actual payments for AI services by 17.7% of 4.6M small businesses; CLM-009/CLM-010 — the vendor runs a partner marketplace and charges for implementation | Spend on the tool and on vendor services, not observed spend on a solo implementer |
| Demand triangulation | At least two independent signals support interest. | **pass** | **Three independent families:** bank transaction data (CLM-002); government survey (CLM-001, CLM-020); vendor commercial behavior in the exact service category (CLM-009, CLM-010). Weak fourth: autocomplete intent (CLM-022) and creator attention (CLM-023) | The creator attention is opportunity-led ("AI agency") and is not counted toward the two-signal minimum. Vendor survey (CLM-004) and vendor report (CLM-015) are excluded from triangulation as seller-published |
| Timely tension | The topic contains a current change, contradiction, threat, or opening. | **pass** | The contradiction is structural: vendors are paid per resolution but leave the resolution-producing work with the merchant, and hand-hold only the brands big enough to qualify. Klarna's public reversal (CLM-014) and Gartner's 80%-by-2029 prediction (CLM-015 context) frame the moment | The threat cuts both ways — the same vendor could remove the job |
| Differentiated promise | Existing coverage leaves room for an Operator Economy synthesis, decision tool, or blueprint. | **pass** | Reviewed coverage is competitor pricing explainers, vendor tutorials and "start an AI agency" courses. None frames outcome pricing as leaving a configuration job, maps the vendor's onboarding threshold as the buyer boundary, or addresses the operator selling a measured implementation to that tier (research "Information gap") | The gap is documented against a named coverage list, not asserted |
| Honest packaging | A compelling title-and-thumbnail premise can be stated without an unsupported outcome, fear claim, or earnings promise. | **pass** | "The AI agent your helpdesk sold you only gets paid when it resolves a ticket. Here is the work that decides whether it ever does — and the business of doing it for brands the vendor won't onboard by hand." | No earnings claim, no "$5.9 billion," no automation-rate claim, no "95% fail" as an SMB statistic |

Audience-pull verdict: **pass**

### Search-volume exception

Exact-query volume is recorded as **not measurable**. Two Google Trends attempts on 2026-09-03 returned HTTP 429, and no licensed volume tool is available to this operation (CLM-022). Autocomplete for the vendor's AI agent surfaced pricing, reviews, actions and version queries — merchant-side question intent about the tool, recorded as a proxy only.

The exception is properly invoked: consequential interest passes on transaction-based spend, and triangulation passes on three families, none of which is a seller of the examined service. "The market is new" is not offered as evidence.

## Overall editorial verdict

Narrative engine: **pass**

Audience pull: **pass**

Overall editorial potential: **pass**

Story spine: `a two-agent DTC brand switches on the AI agent bundled with its helpdesk and adds nothing to it` -> `per-resolution pricing makes the founder see how few resolutions are happening while the agents drown in "where is my order"` -> `the agent only works with knowledge, skills and handover rules, the vendor's own docs say so, and the vendor's hands-on onboarding starts above this brand's size` -> `an operator audits the queue, decides what is safe and what never is, writes the rules, tests, goes live, tunes for two weeks` -> `cost versus quality, money-moving actions on or off, and a fixed fee on a platform that could make the job free` -> `verified resolutions before and after on the vendor's own meter, and a viewer who knows the minimum buyer, the fee arithmetic and the kill condition`

Working audience promise: The AI agent your helpdesk sold you only gets paid when it resolves a ticket. Here is the work that decides whether it ever does — and the business of doing it for brands the vendor won't onboard by hand.

Reviewer: Manav Thaker (Reviewer A pass, produced by the Step 0 review process)

Reviewed: 2026-09-03

Required work before reconsideration: none blocking for this gate. Two standards carry to editorial: (1) the enterprise failure finding (CLM-003) may be shown as enterprise evidence and the small-brand version must be labeled a hypothesis; (2) the vendor's onboarding threshold (CLM-013) must be opened at source before the script states a revenue figure for where hand-holding begins.
