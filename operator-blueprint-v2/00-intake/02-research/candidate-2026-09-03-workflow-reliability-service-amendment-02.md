# Step 0 evidence amendment 02: price reset and rebuilt economics

Status: recorded

Template version: `operator-blueprint-v2-step0.2` (amendment record; the reviewed research brief and amendment 01 are unchanged, so their hashes still hold)

Candidate ID: `candidate-2026-09-03-workflow-reliability-service`

Research brief amended (by reference only): `candidate-2026-09-03-workflow-reliability-service.md` / `687e499ffaec634d90728efb35a62725b33edbb9135b68f4631d195b3ed09876`

Amendment 01 (evidence this record prices against): `candidate-2026-09-03-workflow-reliability-service-amendment-01.md` / `cbf84d870dc268daa6d0f1daf1da170ab731339e04a029f889da768d4fc686af`

Disposition: `../03-validation/candidate-2026-09-03-workflow-reliability-service-disposition.md` / `f9c30e4249624c67091e601689653a6475f0a9ba944263a6d1ec8e5f556ace30` (continue research; addendum item 3 requires this price reset before any re-score)

Governing decision: `../OWNER-DECISION-2026-09-28-COACHING-STANDARD.md` / `95c781cba2a8ad5d8f76dda597329e0f84b4732226f9c8886a9520f0af2cd686`

Recorded: 2026-09-28

Recorded by: the Step 0 research bench

## Why this record exists

The brief modeled one $3,500 sprint. Amendment 01 found the first observed prices, and every one of them sits below $3,500. This record replaces the price hypothesis with the offer shape the evidence supports and rebuilds the capacity and contribution cases. It does not change any score, gate, disposition, pool entry or queue row. It does not pick the price that scores best: where evidence and attractiveness disagree, evidence wins.

## Price evidence, sorted by who set the number

| Evidence type | What it is | Observed numbers | Source |
|---|---|---|---|
| **Buyer-posted budget** | A buyer's stated budget on an open post. Not an accepted price | $750–$1,500 (restoration contractor: CRM-to-billing handoff build with escalation and "clear stop conditions"); $1,500–$3,000 fixed (freight broker: build that must "document all failures"; 97 bids, average $2,098); CAD $250–$750 (dashboard plus site refresh); ~$25/hr and AUD $25–$50/hr (integration and takeover) | CLM-027, CLM-026 |
| **Buyer request, no price** | A buyer asking for the reliability job | Maintenance "if something in the chain breaks"; "open to paying for a short audit first" | CLM-026 |
| **Seller asking price** | What sellers offer. Not a transaction | Single fixes $40, $125, €150, $149, $150 (n8n board); repair quotes $125–$695, median ~$295 (Make); audits $95–$400, median ~$190 (Make); Zapier Platinum minimum spend $100–$1,000, median $250; $297 75-minute fix session; Fiverr fix gigs from $5–$350; one n8n seller's $1,500 audit / $3,000–$5,000 sprint / $750–$1,500 per month retainer, with no buyer seen | CLM-023, CLM-024, CLM-025, CLM-026 |
| **Substitute list price** | What the do-it-yourself alternative costs | NotiLens Pro $29/month (Basic $20/year; Team $99/month); Zapier auto-off and Make deactivation notices come with the plan | CLM-033, CLM-029 |
| **Channel cost** | What a marketplace takes | Freelancer.com: 10% or $5, whichever is greater, on fixed-price projects; 10% on hourly | CLM-034 |
| **Modeled** | Chosen by this record to test | Every price in the offer below | this record |

**Not found anywhere:** a buyer-posted budget for a stand-alone reliability sprint, an accepted price for any of these services, or any buyer price for a monitoring retainer.

## The reset offer

The evidence supports reliability sold **inside** small jobs buyers already post, not as a separate premium sprint. The shape is a ladder. Each rung is labelled by what stands behind its price.

| Rung | Scope | Modeled price | What the price rests on |
|---|---|---|---|
| 1. Per-incident repair | Diagnose and fix one broken workflow; add an error alert on it | **$150–$250** fixed | Seller asking prices ($40–$695; clustered $125–$300). Commodity. Crowded. No buyer budget seen for a single fix |
| 2. Audit-and-fix (the entry) | One client handoff (e.g. intake → scheduling → billing): inventory every automation on it, test each against the platform's stop conditions (auto-off, credit or task caps, stale IDs, log expiry), fix up to three faults, add alerts and a named exception owner, one-page runbook. Fee credited to rung 4 if the client signs within 30 days | **$750–$1,200** fixed | Bottom of the buyer-posted band ($750–$1,500), which was for builds, not audits. Above seller audit asks ($95–$400) and below the one seller's $1,500 audit. Transferred, not observed |
| 3. Reliable build | Build or rebuild one handoff with reliability written in: exception tests, logging, alerts, stop conditions, documentation | **$1,500–$2,500** fixed | Buyer-posted budgets for exactly this ($750–$1,500 and $1,500–$3,000). Direct buyer side. Crowded: 61–159 bids per post |
| 4. Monitoring-plus-fix retainer | Client-owned monitoring tool set up and watched; weekly log check; platform-change watch for the client's apps; up to two fixes a month included | **$300–$500 per month** | **Modeled only.** No buyer price exists. Set below the one seller ask ($750–$1,500) and near what the substitute costs (see below). A hypothesis to test, not an anchor |

**Retired:** the $3,500 sprint as the base case. It sits above every observed buyer budget. A viewer may quote it once as a test alternative, labelled as such; it does not enter the model.

## Strongest substitute: a monitoring tool plus pay-per-fix

A small firm can buy alerts for $29 a month (CLM-033), or rely on the free Zapier and Make failure notices (CLM-029), and pay a freelancer $150 when something breaks (CLM-024).

Break-even against the retainer, using those list and asking prices:

- `$29 + (incidents x $150) = $300` → **about 1.8 incidents a month**
- `$29 + (incidents x $150) = $500` → **about 3.1 incidents a month**

Below two to three breaks a month, the substitute is cheaper. The retainer must then sell on something other than cost: response time, one accountable person, and catching platform changes (like the Pipedrive V1 cut-off, CLM-009, CLM-030) before they break anything. Incident frequency at the bounded buyer is **unknown**; it is the viewer's first test.

Modeled scenario, not observed performance or an earnings forecast.

## Modeled economics

Every number here is an internal Step 0 input until approved under `content-os/facts.md`. **Every figure in this section: Modeled scenario, not observed performance or an earnings forecast.**

| Input | Low case | High case | Basis | Status | Caveat |
|---|---|---|---|---|---|
| Per-incident repair | 4 × $150, 2 h each | 2 × $250, 2 h each | CLM-024, CLM-026 asking prices | transferred (seller side) | Competes with $40 offers |
| Audit-and-fix | 2 × $750, 12 h each | 3 × $1,200, 14 h each | Bottom of CLM-027 buyer band | transferred | Band was for builds, not audits |
| Reliable build | 1 × $1,500, 24 h | 1 × $2,500, 28 h | CLM-027 buyer budgets | transferred (buyer side) | Bid average $2,098 on one post; win rate unknown |
| Retainer | 3 × $300/mo, 3 h each | 6 × $500/mo, 4 h each | None | **modeled / unknown** | No buyer price; churn unknown; takes months to accumulate |
| Unpaid sales and admin hours | 20 h/month | 15 h/month | Assumption | modeled | Posts draw 61–159 bids; true hours could be double |
| Loaded labour (imputed) | $60/h | $60/h | Brief's internal assumption, kept for comparison | modeled | Not a wage claim or recommended rate |
| Software | $50/month | $100/month | Test accounts and operator tools; client pays its own platform and monitoring | modeled | Rises if the operator hosts monitoring |
| Contractors | $0 | $0 | Solo operator | modeled | — |
| Acquisition and overhead | $450 fees (10% of all revenue, all marketplace-sourced) + $150 admin and insurance = **$600** | $480 fees (10% of half the revenue) + $300 = **$780** | CLM-034 fee; admin assumed | fee observed; rest modeled; **true acquisition cost unknown** | Excludes paid ads; unpaid sales time is carried in hours instead |

**Low case**

Capacity case: `($150 x 4) + ($750 x 2) + ($1,500 x 1) + ($300 x 3) = $600 + $1,500 + $1,500 + $900 = $4,500 gross revenue per month`

Contribution case: `$4,500 - $0 delivery labour (owner-delivered) - $50 software - $0 contractors - $600 acquisition and overhead = $3,850 contribution before owner compensation and tax`

Hours: 65 delivery + 20 sales and admin = 85. Imputed-labour check: `$3,850 - (85 x $60) = -$1,250`. Contribution per hour worked: about **$45**.

Modeled scenario, not observed performance or an earnings forecast.

**High case**

Capacity case: `($250 x 2) + ($1,200 x 3) + ($2,500 x 1) + ($500 x 6) = $500 + $3,600 + $2,500 + $3,000 = $9,600 gross revenue per month`

Contribution case: `$9,600 - $0 delivery labour - $100 software - $0 contractors - $780 acquisition and overhead = $8,720 contribution before owner compensation and tax`

Hours: 98 delivery + 15 sales and admin = 113. Imputed-labour check: `$8,720 - (113 x $60) = +$1,940`. Contribution per hour worked: about **$77**.

Modeled scenario, not observed performance or an earnings forecast.

**Same cases with no retainer** (the only rung with no price evidence removed)

- Low: `$3,600 gross - $50 - $510 = $3,040` over 76 hours → about **$40/h**; imputed check **-$1,520**.
- High: `$6,600 gross - $100 - $630 = $5,870` over 89 hours → about **$66/h**; imputed check **+$530**.

Modeled scenario, not observed performance or an earnings forecast.

**Sensitivity**

- If unpaid sales time is 40 hours rather than 20 in the low case, contribution per hour falls to about **$37**. Win rate against 61–159 bidders is the least known input after the retainer.
- The prior brief's base ($3,500 × 2 sprints) showed $6,000 contribution and a +$2,640 imputed check, with no sales hours counted. The reset high case needs roughly twice the delivery hours to exceed it.

Modeled scenario, not observed performance or an earnings forecast.

## What the reset does to the candidate

1. **The stand-alone reliability sprint does not survive.** No buyer budget supports it, and the one seller pricing it shows no buyer.
2. **Without the retainer, the business is cheap per-fix and small-build labour.** The modeled no-retainer range ($40–$66 per hour worked, before owner pay and tax) sits against sellers offering fixes at $40–$150 and buyer posts drawing 61–159 bids. This is Reviewer B's objection — "a Zapier freelancer with a longer checklist" — and the evidence now leans toward it.
3. **A solo business exists only if the retainer is real.** Only the high case with six retainers clears the imputed $60 an hour with room to spare. The retainer is the one rung with no buyer price, and it must beat a $29 tool plus a $150 fix. So the business is conditional on one unobserved purchase.
4. **What the episode can honestly teach.** The fix is a commodity. Reliability is sellable only as a reason to choose you for a build and then keep you on a small monthly fee, and only for clients who break often enough, or cost enough when they break, to beat the substitute. That is a clearer lesson than the $3,500 sprint, and a smaller business.
5. **Scoring.** No score is changed here. Price inputs are now anchored (the condition amendment 01 set for a possible +1 on economics), but contribution is lower and depends on an unpriced retainer. A fresh Reviewer A / Reviewer B pair decides. If the re-score lands below 65, the disposition's next step is park.

## Viewer's first-test plan (replaces amendment 01's price ladder)

Field-only unknowns, taught as unknowns. The owner does not run them.

1. **Desk week, no buyer contact.** Pick one segment (e.g. small law or accounting firms on Clio or Pipedrive, a scheduler and QuickBooks). List platform-change notices for those tools in the last twelve months. Collect five local asking prices for a single fix and five buyer-posted budgets for a comparable build.
2. **Ten conversations.** Screen-share the handoff. Record failures in the last twelve months, **incidents per month**, how they found out, the cost in hours or lost clients, who fixed it and what they paid.
3. **Sell the entry.** Offer audit-and-fix at $750–$1,200 and the reliable build at $1,500–$2,500. Track hours on every job.
4. **Offer the retainer at the end of each paid job,** at $300–$500 a month, next to the substitute written out ($29 tool + $150 per fix). Record who takes which and why.

Success signal: at least two paid audit-and-fix or build jobs at or above $750, each delivered within 14 (audit) or 28 (build) tracked hours; at least two of those clients sign the retainer and keep it past the second month; their recorded incidents or stated cost of a break justify it against the substitute.

Kill or redesign condition: buyers pay only commodity fix prices (under about $500) and decline the audit-and-fix; or no client takes the retainer after five paid jobs, or clients choose the tool-plus-fix substitute; or typical clients report fewer than one incident a month; or audits run past 14 hours twice. If the retainer fails but builds sell, the honest outcome is "small-build freelancer," not this business; redesign or stop.

## Source registry (new claims only)

| Claim ID | Claim and status | Source and URL | Exact locator | Published / accessed | Source type / confidence | Relationship | Refresh by | Caveat |
|---|---|---|---|---|---|---|---|---|
| CLM-033 | NotiLens plans: Basic Push $20/year, Pro $29/month, Team $99/month, Enterprise custom; works with Zapier, n8n and Make. **verified as list price** | https://www.notilens.com/pricing | Plan cards; integrations line | undated / 2026-09-28 | vendor primary / high for own price | direct (substitute) | 2026-12-28 | One tool; list price, not what small firms buy |
| CLM-034 | Freelancer.com fee: "10% or $5.00 USD, whichever is greater" on fixed-price projects; 10% on hourly payments. **verified** | https://www.freelancer.com/feesandcharges | Project fees section | current / 2026-09-28 | platform primary / high | component (acquisition cost) | 2026-12-28 | Excludes membership, bid purchases and unpaid proposal time |

All other claim IDs refer to the research brief and amendment 01. Pages were read with WebFetch on 2026-09-28; no sign-in, form or CAPTCHA was attempted; no local copy was saved.
