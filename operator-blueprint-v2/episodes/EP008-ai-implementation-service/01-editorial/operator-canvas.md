# Operator Canvas: a helpdesk setup practice

Status: locked (owner, 2026-09-03)

Template version: approved `operator-blueprint-v2-step1-v1.5`

Episode: EP008

Candidate ID: `candidate-2026-09-03-ai-implementation-service`

Editorial contract SHA-256: `e97b5039486803b986fe20b68655cb6888072a42eec7a0a0be9c9938d8c76bd9`

Gate: E3. The decision the owner must give: does the proposed business make sense as a complete operating model, and may the Canvas lock?

Evidence class for the overall model: **observed model** for the service category; every solo-operator economic figure **modeled**

Labels: `OBSERVED` (approved evidence), `PARALLEL` (adjacent business or mechanism), `MODELED` (transparent scenario), `UNKNOWN` (important, not established). Step 0 locators are research-brief claim IDs (CLM-nnn), analogy-map IDs (ANA-nnn), and Step 0 amendment 01 (AMD-01).

## 1. Operator

Who could credibly run this business: An operations, CX, product or systems generalist who can read a ticket queue, write instructions a machine can follow, configure a SaaS product, and hold a conversation with a founder about which tickets must never be automated. `PARALLEL`: ANA-003; research "Required skills or credentials."

Relevant experience, access, or advantage: Having run or built for a support queue at a small merchant, and knowing founders of online stores. No certification is required to configure a help desk. `OBSERVED`: CLM-005 (prerequisites are a subscription, a connected store and admin permissions, not a credential).

What the operator does personally at the beginning: Everything. The audit, the rule-writing, the handover decisions, the two weeks of ticket review, the report, and the sales conversations.

What the operator should not need to be: An AI engineer, a developer, a certified partner, or an agency. Vendor partner status is optional and its availability to a solo operator is `UNKNOWN` (CLM-009).

Evidence label and Step 0 locator: `PARALLEL` / `OBSERVED` as marked; CLM-005, CLM-009, CLM-024.

## 2. Buyer and beneficiary

Economic buyer: The founder, ops lead, or head of CX at a Shopify DTC brand on Gorgias or Zendesk. `OBSERVED`: CLM-006 (ticket tiers), CLM-013 via AMD-01 (onboarding boundary).

Day-to-day user: The brand's one to five support agents, who inherit what the agent hands back.

Ultimate beneficiary or customer: The brand's shoppers, who get a correct answer at eleven at night or a human when the question needs one.

Buyer trigger: The founder sees the per-resolution line on the bill and how small it is; a wrong answer on a refund or cancellation; agents still buried in "where is my order" after the AI was switched on; a vendor release that changes the setup. `MODELED`: triggers inferred from the failure pattern (ANA-001), not surveyed.

Who is not a fit: A brand at or above $3M in annual revenue, which the vendor onboards by hand (`OBSERVED`: AMD-01); a brand under roughly 1,000 tickets a month (payback too slow, `MODELED`); a brand whose queue is mostly never-automate questions; a founder who wants money moved without sign-off; a brand that wants a custom build.

Qualified-buyer rule: Shopify DTC brand on Gorgias or Zendesk; roughly 1,000 to 5,000 tickets a month; one to five agents; under $3M annual revenue (self-serve onboarding per the vendor); queue dominated by order status, returns and cancellations; founder willing to sign per action on anything that moves money.

Unsuitable-buyer rule: as "Who is not a fit."

Evidence label and Step 0 locator: `OBSERVED` for the band and boundary (CLM-006, AMD-01); `MODELED` for the minimum ticket count.

## 3. Costly problem

Job the buyer is trying to accomplish: Answer the same few questions, correctly, fast, without paying a person for each one.

Current failure or friction: The AI agent is switched on with little knowledge, no skills and default handover rules, so it hands most tickets back and occasionally answers a money question wrong. The vendor's own guide says the agent needs at least one knowledge source, skills for the highest-volume intents, deliberate handover settings, playground testing and a week of ticket review. `OBSERVED`: CLM-005.

Operational, financial, or strategic cost: Agent hours spent on tickets a machine could close; wrong refunds or cancellations when it closes the wrong ones; per-resolution fees for a handful of resolutions. **Quantified at enterprise scale only.** MIT NANDA: about 95 percent of enterprise GenAI pilots produce no measurable P&L impact, attributed to a learning gap rather than model quality; purchased tools succeed about 67 percent of the time versus internal builds about a third as often. `OBSERVED` (enterprise): CLM-003. The small-brand dollar consequence is `MODELED` (see §10 buyer payback) and `UNKNOWN` until measured.

Why the buyer acts now rather than later: Outcome pricing made non-resolution visible on the bill (`OBSERVED`: CLM-007 mechanism, CLM-008); small-firm adoption is under 20 percent so the buyer is early and finding out what defaults do (`OBSERVED`: CLM-001, CLM-002); Klarna's public reversal put the cost-versus-quality trade-off on the record (`OBSERVED`: CLM-014).

Current alternatives and their limits: The vendor's wizard and webinars (`OBSERVED`: CLM-011; what it leaves undone is `UNKNOWN` until tested); the vendor's own onboarding and professional services, which begin at $3M revenue for dedicated one-to-one work (`OBSERVED`: CLM-010, AMD-01); certified agencies from the partner directory, referred by the vendor, prices on a call (`OBSERVED`: CLM-009, CLM-012); a support BPO; or leaving it.

Evidence label and Step 0 locator: as marked; CLM-001, CLM-002, CLM-003, CLM-005, CLM-007, CLM-008, CLM-010, CLM-011, CLM-014, AMD-01.

## 4. Offer

Plain-English offer: One fixed-scope, fixed-fee implementation of the AI agent already bundled in the brand's help desk, entered through a paid ticket audit credited against the build.

What is included: Thirty days of tickets classified by intent and marked safe, conditional or never; the verified-resolution baseline read from the vendor's report; knowledge base and guidance drafted from the brand's policies, macros and help center and edited by the operator; skills for the top three intents (order status, returns and exchanges, cancellations and edits); handover and never-automate rules set deliberately; a playground test suite (ordinary, missing order, duplicate, angry, out-of-policy, not-in-knowledge); go-live on one channel first; two weeks of monitored tuning with a weekly ticket review; a before-and-after report on verified resolutions, first-response time, wrong handovers and wrong answers; the never list on one page; admin ownership handed back.

What is excluded: Building a custom AI; replacing the help desk; enabling money-moving actions without the founder's per-action sign-off; support staffing; a recurring retainer (excluded from the base case until a recurring duty is observed); anything at a brand the vendor onboards by hand.

Engagement shape: implementation, entered through a paid diagnostic

Time to first meaningful result: Baseline on day one of the audit; go-live within about two weeks of the audit; the before-and-after report at the end of the two-week tuning window. `MODELED`.

Evidence label and Step 0 locator: `OBSERVED` for the delivery skeleton (CLM-005); `PARALLEL` for the offer shape (ANA-003: CLM-009, CLM-010, CLM-012); `MODELED` for scope and timing.

## 5. Buyer result

Result being purchased: A configured agent with a written rule set the brand owns, a measured change in verified resolutions on the vendor's own meter, and a written list of what was deliberately left to humans.

How the result is measured: The vendor's verified-resolution count (the count it bills on), first-response time, and a log of wrong handovers and wrong answers, before and after. `OBSERVED`: CLM-008 (Zendesk defines an automated resolution by a 72-hour quiet period with validation); CLM-007 via AMD-01 (Gorgias bills per resolved conversation).

**Primary acceptance measure:** the before-and-after report, delivered with the never list and the wrong-answer log, and the founder's sign-off that admin ownership has been handed back. The acceptance event is the report, not "the AI works."

**Why the acceptance measure is not the lift alone:** the meter counts containment, not correctness. A rising verified-resolution rate does not prove good answers. The wrong-answer log and the never list are part of the deliverable for that reason (promotion record, assumption 4).

Baseline required: The verified-resolution rate, first-response time and intent mix read during the audit, before any change.

Leading indicators: Playground suite passing; handover rate on safe intents falling during week one; no money-moving action fired without sign-off.

Lagging indicators: Verified resolutions on the vendor's report; agent hours on the three target intents; wrong-answer count over two weeks.

What the operator can influence but not guarantee: The lift. The ten-to-thirty-point lift is a hypothesis, not a result (research "Buyer-payback model"). The operator changes what the agent knows and is allowed to do; they do not control the queue's mix or the vendor's counting rule.

Evidence label and Step 0 locator: `OBSERVED` for the meter (CLM-007, CLM-008, ANA-006); `MODELED` for the lift.

## 6. Delivery system

### Before delivery

Qualification and intake: Ask the vendor's own question: does the brand get a person or a wizard? Confirm the ticket band from the plan tier. Decline brands above the line, brands under roughly 1,000 tickets, and founders who want money moved without sign-off.

Required access, data, permissions, or integrations: Written consent to read thirty days of tickets; scoped, client-controlled admin access to the help desk; the connected Shopify store; the AI Agent subscription active. `OBSERVED`: CLM-005 prerequisites. Consent and scoped access are design requirements (promotion record).

### Core workflow

1. Audit: export or view thirty days of tickets; classify by intent and outcome; mark each intent safe, conditional, never. Owner: operator. Output: the intent map and the never list, first draft.
2. Baseline: read the verified-resolution rate and first-response time off the vendor's report; confirm knowledge sources and handover settings as found. Owner: operator. Output: the baseline reading.
3. Draft knowledge and guidance: a general model drafts from the brand's policies, macros and help center; the operator edits every rule that touches money, shipping promises or cancellations. Owner: AI drafts, operator decides. Output: the knowledge base and guidance.
4. Build skills for the top three intents; set handover triggers deliberately; leave actions off unless the founder signs per action. Owner: operator, founder signs. Output: configured agent, actions register.
5. Test in the playground: ordinary, missing order, duplicate, angry, out-of-policy, not-in-knowledge. Owner: operator. Output: passing suite, or a rule change.
6. Go live on email first; review at least ten tickets a week for two weeks; tune guidance; log every wrong handover and wrong answer. Owner: operator. Output: the tuning log.
7. Report and hand back: before-and-after on the vendor's meter, the never list, the wrong-answer log, a recommendation to expand, hold, or turn off; admin ownership returned. Owner: operator, founder accepts. Output: the acceptance event.

`OBSERVED` skeleton: CLM-005 (knowledge source, skills for returns, order status and cancellations, handover, playground, review at least ten tickets in week one). `MODELED` sequencing and hours.

### Quality and exception handling

Human review: Every rule touching money, shipping promises or cancellations is operator-edited; the founder signs per action for anything that moves money; ten-plus tickets a week are read by the operator for two weeks.

Failure route: A wrong answer on a safe intent moves that intent to conditional and rewrites the guidance; a wrong answer on a money question moves it to never; a handover storm on go-live day reverts to the previous configuration on that channel. Anything touching consumer-protection rules on refunds or automated messaging routes to the brand's own adviser.

Escalation boundary: The operator never enables a money-moving action on their own authority and never keeps admin ownership after handoff.

### After delivery

Handoff, reporting, support, or renewal: The report and the never list; admin returned; no ongoing access. A monthly ticket review is offered only if the founder asks and pays; it is outside the base case. A repeat implementation when the catalog, policies or the vendor's product change is scoped and priced separately.

Evidence label and Step 0 locator: `OBSERVED` for prerequisites and go-live steps (CLM-005); design requirements from the promotion record; `MODELED` for the failure routing.

## 7. Capabilities and stack

| Capability | Required job | Possible tool class | Named example, if approved | Human responsibility | Cost status |
|---|---|---|---|---|---|
| Ticket audit by intent | Read thirty days, sort, mark safe/conditional/never | help desk export, spreadsheet, general LLM for first-pass tagging | Gorgias or Zendesk export | Operator decides every mark | modeled (operator time) |
| Knowledge and guidance drafting | Turn policies and macros into agent knowledge | general LLM | none named | Operator edits every money, shipping and cancellation rule | public pricing (general AI tools; $50 per implementation allocated, modeled) |
| Agent runtime | Answer tickets, look up orders, hand over | the help desk's bundled AI agent | Gorgias AI Agent; Zendesk AI agents | Operator configures; brand owns the plan | observed (brand's own subscription; per-resolution fee, CLM-007, CLM-008) |
| Skills and handover | Encode the three intents and the hand-over triggers | vendor configuration | Gorgias skills, handover settings (CLM-005) | Operator sets on purpose, not at defaults | included in the brand's plan |
| Testing | Prove the suite before go-live | vendor playground | Gorgias playground (CLM-005) | Operator runs and judges | included |
| Measurement | Before-and-after on the billing meter | vendor resolution report | Zendesk automated-resolution report (CLM-008); Gorgias resolution report | Operator reads; founder can verify against the bill | included |
| Sandbox | Test the wizard and skills without a client | the vendor's Starter plan | Gorgias Starter, $10 a month for 50 tickets (CLM-006, time-stamped) | Operator | public pricing, refresh 2026-12-03 |

Data and privacy boundary: Order history, addresses and payment status are the brand's customer data. Scoped, client-controlled admin access; written consent; no data copied out of the help desk beyond the audit working file, which is deleted at handoff. No money-moving action without per-action sign-off.

Vendor dependency: **Central.** The whole offer configures one vendor's product. The vendor sells the same implementation, ships a wizard, has changed pricing and tiers, and could auto-configure from store content. `OBSERVED`: CLM-010, CLM-011; carried as the defining risk in §11.

Manual fallback: If the agent misbehaves, hand every intent back to humans on that channel and revert; the brand is never worse off than defaults.

Evidence label and Step 0 locator: `OBSERVED` for the vendor components (CLM-005 through CLM-011); `MODELED` for the operator-side tool allocation.

## 7A. Business-of-one design

Work AI compresses, accelerates, or makes newly feasible: Drafting the knowledge base and guidance from existing macros, policies and help-center text; first-pass ticket tagging; the agent runtime itself, which the brand already pays for. This is why one person can deliver in about thirty hours rather than a team over sixty days. `MODELED` (hours); `OBSERVED` that the vendor's own onboarding averages 60 days (CLM-010).

Work software can standardize: Playground testing, the resolution report, the export.

Judgment, relationships, permissions, quality, and accountability the operator retains: Safe, conditional, never; every money rule; handover triggers; the per-action sign-off conversation; reading real tickets for two weeks; telling a founder not to buy; owning the report.

Bounded specialist or contractor help allowed: None required in the entry model. Consumer-protection questions route to the brand's adviser.

Work that would force premature hiring or make the entry model cease to be a business of one: Running more than two overlapping monitoring windows; taking brands above the line, whose sixty-day vendor-style onboarding this practice is not built to replace; offering a retainer to many brands at once before the monthly review is proven to be a real duty.

Why one accountable operator can sell and deliver the initial offer responsibly: The engagement is bounded, the skeleton is published by the vendor, the measure comes with the tool, and every judgment point is one person's decision recorded in the never list and the log.

Maximum customer or delivery load before quality, safety, or support fails: Two implementations a month, because the two-week monitoring windows overlap and the operator is reading tickets for both. `MODELED` (research "Client capacity").

Evidence label and Step 0 locator: `MODELED`; CLM-005, CLM-010.

## 8. Go-to-market path

First reachable segment: Brands in the band the operator can already reach: founders they know from working in or around ecommerce, Shopify founder communities, and ecommerce agencies that build stores and run ads but do not touch support. `PARALLEL` (ANA-004, weak); promotion record: the first-buyer path must be built from the operator's own relationships and stated as such.

Buyer signal or trigger: The founder can name the per-resolution line on the bill and how small it is; or a wrong answer on a money question; or agents still on "where is my order."

How the operator finds the first 25 prospects: Their own contacts first; then the agencies (one question: what do you do when a client complains about their support queue?); then founder communities. Apply to the vendor partner program as an individual and record the answer; its leads are a bonus, not the plan. The program's form lists agency types, not individuals. `OBSERVED`: CLM-009.

Credibility artifact: The audit method and a sample never list, published; the sandbox implementation the operator ran on their own Starter store.

First conversation or diagnostic: A paid ticket audit: thirty days of tickets, back with what is safe, what is not, and what the agent resolves today. Credited against the build if the brand goes ahead.

Low-risk entry offer: The paid audit.

Expected objections: "The vendor has a wizard." "We'll wait for the next release." "Our agency does that." "Four thousand for settings?" Responses stay inside the evidence: the vendor's guide lists what the agent needs; the audit shows their own queue; the fee is priced against their own payback; and if the audit says do not buy, the operator says so.

Expansion or referral path: The report is the referral asset. Agencies that referred one brand refer the next. The second help desk when the first is proven.

**Weakest factor, stated plainly:** the go-to-market rests on the operator's own reach plus an unverified partner path. `UNKNOWN` until fifteen qualified conversations are recorded.

Evidence label and Step 0 locator: `PARALLEL` / `UNKNOWN`; ANA-004, CLM-009.

## 9. Entry wedge and expansion ladder

Short public category title: Helpdesk AI setup

Short spoken company name: **a helpdesk setup practice**

One-sentence public definition: It makes the AI that came with a small store's help desk actually answer customers, and decides which questions it never should.

Precise internal operating description: as recorded in the editorial contract (fixed-scope, fixed-fee implementation of the bundled agent for sub-$3M Shopify brands in the 1,000 to 5,000 ticket band; audit, knowledge, skills, handover, playground, go-live, two weeks of tuning, before-and-after report, admin handed back; no build, no replacement, actions off without sign-off, no retainer in the base case).

Mature company promise: The store's AI answers what it should, hands over what it must, and never touches what it must not, and the store can see the difference on its own bill.

Aspirational business: A steady run of brands in the band from a few agencies and founder communities; both help desks; repeat work on catalog, policy and product changes; an optimization retainer only if the monthly review proves to be a duty a brand keeps paying for.

Entry wedge: One fixed-fee implementation for one store, entered through a paid audit.

Why this wedge is commercially and operationally tractable: Bounded, thirty hours modeled, ten-dollar sandbox, vendor-published skeleton, vendor-owned meter, and reachable kill conditions.

Scope invariant that survives expansion: **Never enable a money-moving action without per-action sign-off; the brand owns admin; the result is measured on the vendor's own meter; the never list ships with every engagement.**

| Stage | Offer or capability | Buyer proof required before advancing | Operator capability added | Stop condition |
|---|---|---|---|---|
| Entry | One implementation, entered through a paid audit | none; this is the start | audit method, never list, playground suite | wizard does the whole job; no buyer at the fee after fifteen conversations |
| Next | Repeat implementation on catalog, policy or product change | one implementation delivered with measured hours and a measured lift | change-detection checklist | measured hours over 45 or lift under ten points |
| Then | Second help desk vendor | two paid implementations on the first vendor | second vendor's skeleton and meter | no buyer on the second vendor in fifteen conversations |
| Then | Optimization retainer | a founder asks for the monthly review and pays for it | monthly review routine | no repeat payment after month two |
| Later | Money-moving actions under sign-off | the wrong-answer log at zero on money intents for a full engagement | actions register discipline | any money error |

What remains outside the initial offer but inside the aspirational business: the retainer, the second vendor, agency relationships, actions under sign-off.

Required public qualification: The proposed name is an editorial label. Setup and optimization of the vendor's agent is an observed service category sold by the vendor and by agencies; no solo operator was found selling it at disclosed economics.

Evidence label and Step 0 locator: `OBSERVED` for the category (CLM-009, CLM-010, CLM-012); `MODELED` for the ladder.

## 10. Economics model

All forward-looking figures are scenarios, not expected earnings. `Modeled scenario, not observed performance or an earnings forecast.`

Pricing basis and rationale: A test fee chosen for falsifiability against the store's modeled payback, not transferred from legacy bands (excluded, CLM-025) or partner prices (none observed, CLM-009, CLM-012). Sensitivity $2,500 to $6,000. `MODELED` (research "Modeled economics").

Revenue equation:

```text
implementations × fee = modeled gross revenue
2 × $4,000 = $8,000 a month; 24 × $4,000 = $96,000 a year
```

Direct-cost equation:

```text
labor + tools + acquisition = modeled direct cost
per implementation: 30 h × $60 imputed + $50 software + $400 acquisition = $2,250
```

Capacity equation:

```text
two overlapping two-week monitoring windows ÷ one operator = 2 implementations a month (cap)
60 delivery hours a month plus sales, audit and monitoring reserve
```

| Assumption | Low case | Base case | High case | Evidence label | Source or reasoning |
|---|---:|---:|---:|---|---|
| Fee per implementation | $2,500 | $4,000 | $6,000 | `MODELED` | Test hypothesis against buyer payback; no observed fee anywhere |
| Implementations per month | 1 | 2 | 2 | `MODELED` | Monitoring windows cap concurrency at two |
| Delivery hours per implementation | 45 (stress) | 30 | 25 | `MODELED` | Audit 6, knowledge and guidance 8, skills and handover 6, testing 4, monitoring 4, report 2 |
| Imputed operator labor | $60 per hour | $60 per hour | $60 per hour | `MODELED` | Internal opportunity-cost assumption, not a wage claim or billable rate |
| Software per implementation | $50 | $50 | $50 | public pricing / `MODELED` | Operator's own $10 Starter sandbox (CLM-006) plus general AI tools; brand owns its production plan |
| Acquisition and overhead per client | $600 | $400 | $250 | `MODELED` | Outreach, calls, audit proposal, contract, admin; replace with tracked cost |

Modeled contribution before owner compensation and tax, base case:

```text
monthly:  $8,000 − $100 software − $800 acquisition          = $7,100
annual:   $96,000 − $1,200 software − $9,600 acquisition      = $85,200
after imputed labor (60 h × $60 a month = $3,600):              $3,500 a month
stress (45 h each, 90 h × $60 = $5,400):                        $1,700 a month, about $850 per implementation
```

Break-even condition: One implementation covers the year's software and a month's acquisition allowance. Break-even is immediate and is not the interesting number.

Cash-timing or working-capital risk: Low. The paid audit is collected up front; the implementation fee can be half on go-live, half on the report. The two-week tuning window delays the second half by about a month.

Most sensitive assumption: **Delivery hours.** Thirty is a guess; forty-five is the stress case if policies live in the founder's head and every rule is relitigated. Reviewer B's point stands: the vendor's own sixty-day, two-to-five-session onboarding describes a larger job than thirty hours, so the stress case may be the base case. Second most sensitive: the fee itself, which no one has paid.

**Modeled owner-compensation requirement: $120,000.**

Customers or transactions required to meet that modeled requirement:

```text
required gross = $120,000 + $10,800 costs = $130,800
at $4,000                  -> about 33 implementations a year (2.7 a month, above the 2-a-month cap)
at 24 a year (the cap)     -> fee must be about $5,450
```

**The base case does not clear the modeled livelihood requirement.** At $4,000 and full capacity every month, contribution is about $85,000 before the owner pays themselves or pays tax. The honest alternatives are explicit: raise the fee to about $5,500 at full capacity (inside the sensitivity range, paid by no one yet); add a second product, of which the obvious candidate is the optimization retainer the agencies sell, excluded from the base case until one brand has paid for it; or accept less than the target while the practice is being proven.

Buyer-payback model (defines the minimum buyer; every input modeled or transferred):

```text
store at 2,000 tickets a month, verified resolution 10% -> 30% after implementation (hypothesis)
400 more machine-resolved tickets a month
vendor fee: 400 × $1.50 (Zendesk's published rate, CLM-008)          = about $600 a month more
agent time: 400 × 8 minutes ÷ 60 × $25 loaded hour (both assumed)     = about $1,333 a month saved
net to the store                                                      = about $733 a month
$4,000 fee pays back in about 5.5 months

store at 500 tickets a month: 100 tickets; fee $150; agent time $333; net about $183; payback about 22 months
```

That is why the buyer is bounded at roughly 1,000 tickets a month and up. Below that, the operator's job is to tell the founder not to buy. The Gorgias per-resolution figure is not used in this arithmetic because it is not confirmed at source (AMD-01); the payback at Gorgias would differ by that unknown.

Share of the reachable buyer set implied by that customer count: Two a month against millions of Shopify merchants (`OBSERVED`: CLM-019) is negligible as a share. **That is not the argument.** The question is whether one person can reach two qualified brands a month from their own relationships. `UNKNOWN`.

Why the underlying problem is large and costly enough for that share to matter: Fewer than one in five small firms uses AI at all (CLM-001, CLM-002), so the brands with the agent switched on are a thin slice of a very large pool; every one of them received the wizard unless they are above $3M (AMD-01). The pool's size makes two a month plausible; it does not make two a month reachable.

Evidence or test needed to show the share is reachable: Fifteen qualified conversations recorded, two paid offers made at the predeclared fee, one acceptance.

Why this remains a sustainability model rather than an income promise: Every figure is an assumption with the arithmetic shown; the base case is recorded as failing the compensation target rather than adjusted until it passes; the lift is a hypothesis; the fee has never been paid.

Required public disclosure: `Modeled scenario, not observed performance or an earnings forecast.`

## 11. Risks and failure modes

| Risk or assumption | Why it matters | Early warning | Mitigation | Kill condition | Evidence label |
|---|---|---|---|---|---|
| The vendor closes the gap: wizard, auto-configuration, lower onboarding threshold | The business exists between the wizard and the implementation manager; the vendor controls both | A release note about auto-setup from store content; "AI Agent 3.0" queries; onboarding boundary moves down | Build the durable assets first (audit method, never list); stay vendor-agnostic across both help desks | The wizard, run on a sandbox, leaves nothing for a person to do | `OBSERVED` risk (CLM-010, CLM-011); residue `UNKNOWN` |
| A sub-$3M brand will not pay a four-figure fee | The whole business | "We'll use the wizard" or "we'll wait" after seeing their own audit | Price against their payback; lead with the paid audit | Fifteen qualified conversations, no buyer at the fee | `UNKNOWN` |
| Delivery hours exceed the fee | Decides whether it clears at all | The unpaid implementation runs past 45 hours | Cap rule relitigation; require policies in writing before the audit | Measured hours make the fee unsellable | `MODELED` |
| Lift does not materialize | The buyer's payback disappears | Handover rate on safe intents does not fall in week one | Move intents between safe and conditional; rewrite guidance | Measured lift under ten points on the unpaid implementation | `MODELED` hypothesis |
| Wrong answers rise with the meter | Containment is not correctness; a wrong refund is real money | Wrong-answer log entries on money intents | Money intents on never; per-action sign-off; two weeks of reading | Any money-moving error | `OBSERVED` boundary (promotion assumption 4) |
| Partner program refuses individuals and community reach yields nothing | No front door | Warm responses, no referrals; program form has no individual option | Agencies that do not do CX as the referral source | Program refuses and fifteen conversations produce no buyer | `UNKNOWN` (CLM-009) |
| Vendor pricing or tier changes mid-engagement | Payback arithmetic shifts; counting rule shifts | Pricing-page change; tier restructure | Read the meter's definition at baseline and at report; refresh prices 2026-12-03 | Counting rule changes so before and after are not comparable | `OBSERVED` (CLM-008 caveat) |
| Buyer pool thinner than adoption numbers suggest | Customer service is a planned AI use for only 9 percent of small employers (NFIB) | Many "not yet" conversations | Qualify on "is the agent switched on" before anything else | Fewer than three brands in the band with the agent on among the operator's reach | `OBSERVED` context (CLM-016) |
| Data and consent | Customer order and payment data | A founder wants to skip consent or wants actions on by default | Written consent, scoped access, actions off, admin returned | Founder refuses consent or sign-off | design requirement |

## 12. First 30-day construction and validation plan

Question being tested: Does the vendor's wizard leave a job a person must do, will a sub-$3M brand pay a predeclared four-figure fee for it, and does one implementation move the meter at hours the fee supports?

Business asset or capability constructed before testing: The audit method (intent classification and safe-conditional-never rules), the playground test suite, and a sample never list, built on the operator's own Starter sandbox.

First paid wedge to offer: One implementation at a predeclared fee, entered through a paid ticket audit.

Smallest credible test inside that construction: The wizard run end to end on the sandbox with a written record of what it leaves undone; one unpaid implementation on a real brand with a stopwatch and the meter read before and after.

Target participants: Three brands in the band the operator already knows (ticket review with written permission); one of them for the unpaid implementation; two paid offers to brands below the vendor's line.

What must be built before testing: The sandbox, the audit method, the test suite, the predeclared fee written down.

What must not be built yet: A retainer, a second vendor's playbook, a website, an agency application as the primary path, any custom tooling.

Success signal: One brand pays the predeclared fee; the unpaid implementation shows a lift of at least ten points on verified resolutions with no money-moving error; hours at or under 45; the wizard leaves the knowledge, skills and handover judgment to the merchant.

Failure signal: The wizard configures knowledge, skills and handover adequately without a person; no brand in the band will pay after fifteen qualified conversations; lift under ten points; hours over 45; too few safe intents to justify the fee.

Decision at day 30: continue building / revise the fee from measured hours / return to the Canvas / stop

Maximum time and cash at risk: About forty hours of the operator's time and under $100 in software.

## 13. Unknowns and contradictions

| ID | Unknown or contradiction | Why it matters | Owner | Resolution path | Blocks lock? |
|---|---|---|---|---|---|
| U001 | What the vendor's wizard leaves undone | It is the offer or there is no offer | operator | test later (day-1 sandbox run); also a carried pre-lock condition for the episode | no for the Canvas; yes for the script lock as a pre-lock condition |
| U002 | Will a sub-$3M brand pay a four-figure fee | The whole business | validation lead | safe first-test question (two paid offers) | no |
| U003 | Real delivery hours at a defensible standard | Decides the economics | operator | safe first-test question (stopwatch on the unpaid implementation) | no |
| U004 | Achievable lift from defaults | The store's payback | operator | safe first-test question (meter before and after) | no |
| U005 | Small brand's real cost per ticket and minutes per ticket | Buyer-payback inputs are assumed | validation lead | safe first-test question (three brands' actual hours and volumes) | no |
| U006 | Gorgias per-resolution dollar figure | Payback at Gorgias differs by it | Step 0 | later-stage blocker: opened at source, not rendered (AMD-01); figure stays out of the script | no (figure excluded) |
| U007 | Is a solo operator admitted to the partner program | Secondary channel | operator | safe first-test question (apply and record) | no |
| U008 | Blog states AI Agent "starts at $250 monthly as an add-on"; pricing page states per-resolution on every plan | Contradiction on the billing model | Step 0 | editorial clarification: use the pricing page; keep the $250 figure out of the script (AMD-01) | no |

No current E3 blocker. No narrative or scenario substitutes for an unresolved operating decision. The failing base case is recorded as failing.

## Pitch-deck and episode coverage map

| Pitch question | Canvas source | VO obligation | Visual opportunity | Downloadable detail | Coverage status |
|---|---|---|---|---|---|
| Why now? | §3 | outcome pricing; early adoption; Klarna | the bill with the per-resolution line; adoption chart with source receipt | citations, refresh dates | complete |
| What is the problem? | §3 | the agent hands tickets back; the vendor's own guide lists the setup | empty knowledge panel; handover log; the guide's checklist | full evidence registry | complete |
| What is the company? | §9 | spoken name and plain definition; never list as the product | company boundary; the never list on one page | precise internal description | complete |
| Who buys and who does not? | §2 | ticket band, $3M line, sign-off rule | fit / no-fit filter; vendor tier ladder | segment criteria and qualifying questions | complete |
| Why is the opportunity large enough? | §3, §10 | adoption under one in five; the job sold at three levels; honest limit | three-level ladder; adoption receipt | sources and analogy limits | complete |
| Why can one operator win? | §7A | AI drafts, operator decides; thirty hours versus sixty days | AI/operator split | capacity boundary | complete |
| What is sold first? | §4, §9 | paid audit, then one implementation; the report as acceptance | offer card; sample report | scope, exclusions, terms | complete |
| How is it delivered? | §6 | audit, rules, test, go-live, tune, report | process loop; failing-then-passing playground test | detailed SOP | complete |
| How are customers reached? | §8 | own reach, agencies, paid audit; partner program as bonus | first-25 path | outreach approach and objections | complete |
| Can it support one operator? | §10 | **the base case does not clear; say the number** | unit-economics build; payback at 2,000 versus 500 tickets | full model and formulas | complete |
| What can break it? | §11 | the vendor can close the gap; the four kill conditions | failure tree | complete risk register | complete |
| What happens first? | §12 | run the wizard on a ten-dollar sandbox; write down the residue | 30/60/90 timeline | complete test plan | complete |

Audio-only rule: buyer, problem, company, first offer, human responsibility, economics boundary, principal risk and first action are all carried in VO. Visuals carry citations, secondary arithmetic, interface examples (with permission or recreation) and comparison detail.

Visual-truth rule: no diagram may show what the wizard leaves undone before the sandbox test is run, present the ten-to-thirty lift as measured, show a Gorgias per-resolution dollar figure, or collapse the expansion ladder into one package.

## Public Canvas layer

Short public category title: Helpdesk AI setup

Short spoken company name: **a helpdesk setup practice**

One-line plain definition: It makes the AI that came with a small store's help desk actually answer customers, and decides which questions it never should.

Precise internal operating description, retained outside first-listen narration: as in §9.

Buyer: a Shopify DTC brand on Gorgias or Zendesk, roughly 1,000 to 5,000 tickets a month, under $3M revenue, whose AI agent is switched on and mostly handing tickets back.

Problem: the agent has no knowledge, no skills and default handover rules, and the vendor's hands-on onboarding starts above this brand's size.

Offer: one fixed-fee implementation, entered through a paid ticket audit.

Result: a configured agent, a written never list, and a before-and-after on the vendor's own meter.

Delivery loop: qualify → consent → audit → baseline → draft → decide → build → test → go live → tune → report → hand back.

Stack by capability: the vendor's agent for the runtime; a general model for drafting; the vendor's playground and report for testing and measurement; the operator for every decision.

AI role: drafts the knowledge and guidance; answers the tickets it is allowed to.

Human judgment retained: safe, conditional, never; every money rule; handover; sign-off; two weeks of reading; the no-buy call.

Business-of-one boundary: two implementations a month.

First-customer path: your own contacts, ecommerce agencies that do not do CX, founder communities; a paid audit first.

Entry wedge: one implementation.

Aspirational destination: a steady run of brands on both help desks, repeat work on changes, a retainer only if proven.

Proof required before expansion: one delivered implementation with measured hours and a measured lift.

Economics disclosure: `Modeled scenario, not observed performance or an earnings forecast.`

Modeled livelihood requirement and required customer count: $120,000 needs about 33 implementations a year at $4,000, above the 24-a-year cap; at the cap the fee must be about $5,500. **The base case does not clear.**

Reachable-share assumption: two a month against millions of merchants; size is not the constraint, reach is, and it is untested.

First construction step and test: run the wizard on a ten-dollar sandbox and write down what it leaves for a person to do.

Biggest risk: the vendor closes the gap.

## E3 readiness check

- [x] The first economic buyer and purchase trigger are identifiable.
- [x] The short public and spoken company name can be understood on a first listen and does not carry the entire operating definition.
- [x] The plain definition explains the buyer and owned job without implying an established market category, demand level, or result the evidence has not established.
- [x] The mature company remains distinct from the entry offer.
- [x] The first paid transaction (the audit) is distinct from the implementation, the retainer and the second vendor.
- [x] The buyer result has a baseline, primary acceptance measure, acceptance event, and influence boundary.
- [x] Build, narrow, defer, no-build, and completion decisions are explicit (the audit can say do not buy).
- [x] Delivery defines access ownership, human judgment, tests, failure routing, recovery, revocation, documentation, and handoff.
- [x] The first-customer test names a reachable segment, bounded prospect set, paid decision, success signal, failure signal, and kill condition.
- [x] Economics include price, labor, tools, acquisition, support, capacity, and a stress case.
- [x] The Canvas identifies exactly what AI enables and what human judgment, accountability, access, and relationship work remain.
- [x] One accountable operator can deliver the entry offer inside a declared capacity and quality boundary without a hidden team.
- [x] The modeled livelihood case counts owner compensation and translates it into a required customer count.
- [x] The required share is compared with a reachable buyer set and a large, costly problem without treating total market size as demand.
- [x] Sustainability is presented as a condition to test, and the base case is recorded as failing it.
- [x] Expansion stages require new proof and do not treat service learning as automatic product demand.
- [x] Every unknown is a safe first-test question, a later-stage blocker, or a recorded pre-lock condition.
- [x] No narrative, analogy, demo, or revenue scenario is being used as a substitute for an unresolved operating decision.
- [x] Every pitch-deck question has a declared VO, visual, and downloadable-Canvas treatment.
- [x] The audio-only episode still explains the buyer, problem, company, first offer, human responsibility, economics boundary, principal risk, and first action.
- [x] Visual coverage adds comprehension or proof without inventing certainty, collapsing expansion stages, or becoming the only place a load-bearing claim is explained.

## Canvas lock

Decision: **lock** (showrunner recommendation was lock)

Approved by: Manav Thaker

Approval date: 2026-09-03

Owner statement of record (2026-09-03): "Approved let's keep going"

Calculate the SHA-256 after this approval record is complete. Store it in dependent artifacts and the editorial lock; do not place a self-hash inside this file.
