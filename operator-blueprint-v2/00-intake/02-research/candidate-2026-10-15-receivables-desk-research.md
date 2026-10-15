# Opportunity research brief: Always-on receivables desk for small B2B businesses

Template status: approved V2 Step 0.2 template; locked 2026-08-21.

Status: researching

Template version: `operator-blueprint-v2-step0.2`

Candidate ID: `candidate-2026-10-15-receivables-desk`

Candidate brief: `../01-candidates/candidate-2026-10-15-receivables-desk.md`

Candidate brief SHA-256: `6aa08857621de2e834411aac197020247e55606d08e2e3b0ecc5ff59fb0803db`

Research cutoff: 2026-10-15

Research refresh date: 2027-01-15 (quarterly survey cycle, AR-agent pricing, state law sessions)

## Executive finding

- Opportunity: One operator with AI agents runs pre-collection follow-up on past-due B2B invoices
  for about 30 small businesses under each client's name, for a flat monthly fee.
- Evidence class: adjacent synthesis
- Provisional verdict: plausible with bounded assumptions
- Main reason: The buyer problem is current and large (QuickBooks 2026), employers already pay
  part-time clerks for exactly this job (2026 postings), and a human-staffed done-for-you service
  already sells the offer to small professional firms (CollBox). Agents lower the delivery cost
  enough that one operator could serve other niches below CollBox's entry price.
- Largest unresolved question: in which states can a third party follow up on another business's
  past-due invoices, under the client's name, without registering or licensing as a commercial
  collection agency? Florida and Washington read against the operator; Illinois reads for it.
- Required public framing: QuickBooks figures are verified survey findings from one vendor's
  survey; CollBox and AR-platform terms are seller terms; all economics are a modeled scenario;
  client trust, price acceptance, and collection results are the viewer's first test; the
  licensing answer is the viewer's to obtain for their state.

## Buyer reality

- Buyer: Owner or office manager of a small US business invoicing other businesses on net terms,
  without full-time AR staff.
- End customer or beneficiary: The buyer; its customers receive the follow-ups.
- Recurring problem: Past-due invoices; follow-up stops after the first reminder (CLM-001, CLM-006).
- Consequence and frequency: 59% of small businesses report invoices 30+ days overdue, up from 47%;
  average $17,700 owed among those waiting; 38% of firms with overdue invoices report growing
  reliance on credit cards versus 21% without (CLM-001 to CLM-003).
- Existing alternatives or budget: free reminders in invoicing software; AR platforms; CollBox;
  part-time clerks; contingency agencies after about 90 days (CLM-004, CLM-005, CLM-007, CLM-008).
- Why now: the one-year jump in the overdue share (CLM-001) and 2026 AR agents that send email,
  calls, and texts on their own (CLM-008).

## Evidence landscape

### Direct evidence

- CollBox sells the same offer (past-due follow-up by a dedicated human staffer, email and phone,
  client-locked accounts, disputes handed back, 90-day window, flat monthly fee by client count) to
  solo and small law and accounting firms (CLM-005). Seller terms; no buyer record of payment yet.

### Adjacent business evidence

- Part-time AR clerk postings in 2026 whose job is chasing past-due balances, at $17–$30 an hour for
  5–25 hours a week (CLM-004; from the 2026-10-13 scout, search-result summaries; posting pages
  returned 403). Old-way spend; end-employer size unknown because several came via staffing firms.
- Contingency collection agencies take 25–35% on debts over about 90 days (CLM-007, via CollBox's
  partner network; context).

### Component feasibility evidence

- AR agents that read invoice history and send follow-up emails, calls, and texts on their own
  exist and are funded (Daylit: $110M round September 2025, SOC 2 Type I February 2026, "more than
  200 companies"; CLM-008, secondary blog summarizing vendor claims).
- Responsible designs route disputes, settlement offers, hardship claims, and key accounts to a
  human (CLM-008), which matches the operator's escalation role.

### Scaled relevance

- QuickBooks Small Business Insights (quarterly sample about 5,000) and Business Ownership in 2026
  (1,305 owners, December 2025) (CLM-001 to CLM-003). One vendor's survey; methodology summarized,
  not audited.

### Demand and competition

- Exact target queries: "how to chase unpaid invoices", "accounts receivable outsourcing small
  business", "AI collections agent".
- Adjacent query or question families: invoice-chasing threads on Indie Hackers (2026) and UK
  Business Forums (CLM-006).
- Volume source, attempted measurement, and date: Google Trends US 5 years, 2026-10-13 scout:
  "unpaid invoices" at a five-year high mid-2026, low absolute volume; "accounts receivable
  outsourcing" near zero. Not measurable in absolute terms.
- Other demand signals: clerk postings (behavior); 26% of owners say their most useful digital tools
  help them chase money owed faster (CLM-003).
- Independent signal count: 3 families (vendor survey; employer postings; forum threads). Forum
  threads are partly posted by tool builders.
- Strongest existing coverage: vendor guides (Xero, June 2026; QuickBooks) on chasing invoices;
  AR-agent vendor content (Kolleno, Gaviti, Daylit coverage) aimed at finance teams.
- Information gap: nobody covers a solo operator selling the outcome to small firms, the
  hand-back and lock rules, and the state licensing line.

## Proposed synthesis

- Parallel A and supported component: CollBox -> offer shape, flat pricing unit, boundary (no
  dispute negotiation, 90-day hand-back, locked accounts).
- Parallel B and supported component: part-time AR clerks -> old-way spend and job scope.
- Parallel C and supported component: AI AR platforms -> agent follow-up is technically feasible.
- New combination: CollBox's done-for-you model, run by one operator on agents, sold outside law
  and accounting at a lower flat fee, with dispute triage included.
- Primary transfer risk: legal status of a third party contacting another business's customers
  about past-due invoices (CLM-009 to CLM-011); buyer trust in agent-written messages.
- Analogy map: not started.

## Proposed Operator Blueprint

- Offer: Monthly receivables desk for invoices past due and not placed for collection.
- Buyer outcome: weekly aging report; 30+ day balance and days-sales-outstanding tracked from a
  baseline.
- Delivery workflow: connect read-only to the accounting system; agree rules, tone, and locked
  accounts; agents send scheduled follow-ups and reminder calls under the client's name; replies
  classified (paid, promise, dispute, missing document); disputes passed to the client the same
  day; unpaid after the window, handed back.
- Technology and human stack: accounting-system read access; email from the client's domain or a
  shared mailbox; agent drafting and reply classification; scripted calling where allowed; operator
  review queue; weekly report.
- Required skills or credentials: AR or bookkeeping experience; judgment on relationships; state
  registration or licence where required (unknown per state).
- Go-to-market path: one niche (for example, small agencies or trades suppliers) through
  bookkeepers and fractional CFOs who already see the aging reports (hypothesis).
- Pricing model: modeled scenario; flat monthly fee anchored below CollBox's $599 entry tier.
- Defensibility: niche templates, dispute patterns, and accountable reporting; not tool resale.

## Modeled economics

Every number in this section is an internal Step 0 input until it is approved under
`content-os/facts.md` for public use.

| Input | Working value or range | Basis | Status | Sensitivity or caveat |
|---|---|---|---|---|
| Pricing unit | $300–$500 per client per month | Below CollBox $599 tier (CLM-005); old-way clerk spend about $350–$3,000/month (CLM-004) | modeled | Price is the viewer's first test |
| Client capacity | about 30 clients | Agent handles drafting and classification; operator handles escalations | modeled | Depends on invoices per client and escalation rate |
| Delivery hours | about 1–1.5 h per client per week | Review queue, escalations, weekly report | modeled | Unmeasured; viewer's first test |
| Loaded labor cost | operator's own time | n/a | modeled | Owner compensation excluded |
| Software and contractors | about $1,000–$2,500 per month | Agent, calling, mailbox, and accounting connectors | modeled | AR-platform pricing not published (CLM-008) |
| Acquisition and overhead | about $500–$1,000 per month | Referral partners, registration or bond where required | modeled | State costs unknown |

Capacity case formula: `$400 x 30 clients x 12 months = $144,000 gross revenue`

Contribution case formula: `$144,000 - $0 delivery labor (owner) - $21,000 software - $0 contractors - $9,000 acquisition and overhead = $114,000 contribution before owner compensation and tax`

Disclosure: `Modeled scenario, not observed performance or an earnings forecast.`

## Narrative and audience hypothesis

- Operator protagonist: a former bookkeeper or AR clerk.
- Starting state: owners owed about $17,700 who stopped after one reminder.
- Inciting change: overdue share 47% to 59% in a year.
- Stakes: cash, credit-card reliance, customer relationships.
- Causal mechanism: unowned, awkward, lumpy follow-up.
- Build transformation: agent desk with human escalation and hand-back.
- Decisions and tradeoffs: flat fee versus share of collections; which accounts to lock; which states
  to serve.
- End state and payoff: synthetic before/after aging report and the viewer's first test.
- Visual evidence classes: documents (aging report, invoice), flows (follow-up ladder), interfaces
  (agent log), comparisons (old-way cost table), maps (state licensing).
- Working audience promise: how one person with agents could run receivables for 30 small firms,
  and the legal line to check first.
- Honest packaging territory: "Small businesses are owed $17,700. Nobody wants to send the second
  email."

## Risks and constraints

- Factual uncertainty: clerk postings read only as search summaries; CollBox pricing from a
  third-party review with no page date; Daylit claims are vendor claims via a blog.
- Analogy-transfer uncertainty: CollBox serves professional firms with recurring client billing;
  other niches may have different dispute and relationship patterns.
- Legal or regulatory boundary: Florida requires registration of anyone collecting commercial
  claims owed to another, with no creditor's-name exemption (CLM-010). Washington's
  collection-agency definition covers any claim, not only consumer debts; its exemption for
  preparing or mailing statements ends when "other collection efforts" are made (CLM-011).
  Illinois exempts contracted notice using only the creditor's name from 2026-01-01 (CLM-009).
  FDCPA applies to consumer debts only (scout record; not re-read this run). No legal conclusion is
  made here.
- Permissions, privacy, or guest dependency: client customer data and mailbox access; no guest.
- Platform or vendor dependency: accounting-system APIs, email deliverability, calling rules.
- Ethical failure mode: harassment, impersonation, or threats; agents sending to locked accounts;
  mistaken sends on paid invoices.
- Claims that must not be made: collection-rate or DSO improvements; that no licence is needed;
  earnings; that QuickBooks figures describe all small businesses.

## Thirty-day validation plan

This is the viewer's first test, not owner field work.

1. Price and trust: offer the desk to five businesses in one niche at a modeled $300–$500 flat fee,
   with locked accounts and hand-back rules shown up front.
2. Licensing: confirm with the viewer's state regulator or counsel whether the desk needs
   registration or a licence for commercial claims.
3. Delivery: run one client's past-due list for 30 days, logging hours, escalations, and collected
   amounts against a baseline.

Success signal: two of five businesses agree to a paid month, and the pilot's 30+ day balance falls
with under 1.5 operator hours per client per week.

Kill or redesign condition: no business will allow outside contact with its customers at any price,
or the viewer's state requires a licence the viewer will not obtain.

## Source registry

Every load-bearing claim must meet `../03-validation/EVIDENCE-STANDARD.md`.

| Claim ID | Claim and status | Source and URL/path | Exact locator | Published / accessed | Snapshot or local path / SHA-256 | Source type / confidence | Relationship | Refresh by | Caveat |
|---|---|---|---|---|---|---|---|---|---|
| CLM-001 | 59% of small businesses have some invoices 30+ days overdue, up from 47%; verified | Intuit QuickBooks via Stacker/KEYT <https://keyt.com/stacker-small-business/2026/07/20/report-finds-more-small-businesses-are-carrying-overdue-invoices-than-last-year/> | Opening figures | 2026-07-20 / 2026-10-15 | not captured; fetched text | secondary carrying vendor survey; medium | direct | 2027-01-15 | One vendor's survey; QuickBooks users may skew |
| CLM-002 | Average $17,700 owed among businesses waiting on unpaid invoices ($17,500 in 2025); verified | Same | Figures section | 2026-07-20 / 2026-10-15 | not captured | secondary; medium | direct | 2027-01-15 | Mean, not median |
| CLM-003 | 38% of firms with overdue invoices report growing credit-card reliance vs 21% without; 26% say their most useful tools help them chase money faster; samples about 5,000 quarterly and 1,305 owners; verified | Same | Credit and follow-up sections; methodology | 2026-07-20 / 2026-10-15 | not captured | secondary; medium | direct | 2027-01-15 | Association, not cause |
| CLM-004 | Part-time AR clerk postings, 2026, $17–$30/hr, 5–25 h/week, chasing past-due balances; qualified | `automation/candidate-discovery/runs/2026-10-13.md` run 2 ledger (ihireaccounting, hireheroesusa, virtualvocations, ziprecruiter summaries) | Origin observation | 2026-03 to 2026-08 / 2026-10-13 | pool record | search-result summaries; low-medium | adjacent (old-way spend) | 2026-12-31 | Posting pages 403; employer size unknown |
| CLM-005 | CollBox: dedicated staffer follows up past-due invoices by email and phone; $599 (1–100 clients), $1,099 (101–200), $1,399 (201–300) monthly flat; 90-day window; lock feature; disputes returned to firm; targets solos and small firms; verified as seller terms | Lawyerist review <https://lawyerist.com/reviews/accounting-billing-finance/collbox/> | Pricing and how-it-works sections | undated / 2026-10-15 | not captured | third-party review of seller; medium | direct (observed model) | 2027-01-15 | Review date unknown; Capterra shows $250 unexplained; no buyer record |
| CLM-006 | Owners avoid second and third follow-ups; qualified | Indie Hackers roundup <https://www.indiehackers.com/post/5-invoice-chasing-threads-later-the-same-problem-keeps-showing-up-4c0f697aca>; UK Business Forums article | Post body (via search summary) | 2026 / 2026-10-15 | not captured | community, author builds a tool; low | context only | n/a | Seller-adjacent author; mostly freelancers |
| CLM-007 | Contingency agencies take 25–35% on debts over about 90 days; context | Dealroom CollBox profile <https://app.dealroom.co/companies/collbox> | Description (search summary) | undated / 2026-10-15 | not captured | aggregator; low | context only | n/a | Seller-described range |
| CLM-008 | AR agents send follow-up emails, calls, texts autonomously; Daylit $110M round Sept 2025, SOC 2 Type I Feb 2026, 200+ companies; verified as reported claims | beancount.io blog <https://beancount.io/blog/2026/09/26/daylit-ai-agents-automated-collections-accounts-receivable-guide> | Daylit section | 2026-09-26 / 2026-10-15 | not captured | secondary blog of vendor claims; low-medium | component | 2027-01-15 | No pricing or customer size |
| CLM-009 | Illinois exempts persons under contract to notify a creditor's debtors using only the creditor's name, effective 2026-01-01 (SB 2457); verified | Mayer Brown <https://www.mayerbrown.com/en/insights/publications/2026/01/illinois-revamps-the-scope-of-its-collection-agency-licensing-law> | Exemptions list | 2026-01-05 / 2026-10-15 | not captured | law-firm analysis; high | direct (boundary) | 2027-01-15 | Does not say whether the Act reaches commercial debts |
| CLM-010 | Florida: "commercial collection agency" means anyone whose primary or secondary business is collecting commercial claims owed to another; registration required; exemptions do not include acting in the creditor's name; verified | Fla. Stat. 559.543(2), 559.544(1), (5) <https://www.flsenate.gov/Laws/Statutes/2025/559.543>; <https://www.flsenate.gov/Laws/Statutes/2025/559.544> | Subsections cited | 2025 statutes / 2026-10-15 | not captured | primary; high | direct (boundary) | 2027-07-01 | Registration, not a licence; bond and cost not read |
| CLM-011 | Washington: "claim" covers any obligation for payment; collection agency includes anyone soliciting claims for collection; exemption (5)(d) for preparing or mailing statements applies only if payments go to the creditor and no other collection efforts are made; verified | RCW 19.16.100(2), (4), (5) <https://app.leg.wa.gov/RCW/default.aspx?cite=19.16.100> | Subsections cited | current RCW / 2026-10-15 | not captured | primary; high | direct (boundary) | 2027-07-01 | Whether follow-up emails are "other collection efforts" is a legal question |

## Unresolved questions

- Licensing: commercial-claim coverage in the next five largest small-business states (California,
  Texas, New York, Georgia, Pennsylvania). Desk; next bench.
- Buyer payment: any buyer-side record (review with company size, testimonial with outcome, firm
  disclosure) of paying CollBox or a similar service. Desk; next bench. Otherwise the viewer's first
  test.
- Substitute: AR-platform pricing and minimums for firms under 20 staff (Daylit, Chaser, Upflow).
  Desk; next bench.
- Trust and price acceptance: viewer's first test.
