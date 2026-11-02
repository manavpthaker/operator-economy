# Opportunity research brief: Always-on receivables desk for small B2B businesses

Template status: approved V2 Step 0.2 template; locked 2026-08-21.

Status: researching

Template version: `operator-blueprint-v2-step0.2`

Candidate ID: `candidate-2026-10-15-receivables-desk`

Candidate brief: `../01-candidates/candidate-2026-10-15-receivables-desk.md`

Candidate brief SHA-256: `6aa08857621de2e834411aac197020247e55606d08e2e3b0ecc5ff59fb0803db`

Research cutoff: 2026-10-22 (substitute, buyer-record, and channel pass added 2026-10-22; licensing and substitute pass 2026-10-19; first pass 2026-10-15)

Research refresh date: 2027-01-15 (quarterly survey cycle, AR-agent pricing, state law sessions)

## Executive finding

- Opportunity: One operator with AI agents runs pre-collection follow-up on past-due B2B invoices
  for about 30 small businesses under each client's name, for a flat monthly fee.
- Evidence class: adjacent synthesis
- Provisional verdict: plausible with bounded assumptions
- Main reason: The buyer problem is current and large (QuickBooks 2026), employers already pay
  part-time clerks for exactly this job (2026 postings), and a human-staffed done-for-you service
  already sells the offer to small professional firms (CollBox). Agents lower the delivery cost
  enough that one operator could serve other niches below CollBox's entry price and well below
  Chaser's tool-plus-specialist price (CLM-017).
- Largest unresolved question (narrowed 2026-10-19): the licensing line is state by state. Of eight
  states read, Florida and Washington plausibly reach third-party follow-up on business invoices;
  California, Texas, New York (state and New York City), Georgia, and Pennsylvania license or
  regulate consumer debt only, or not at all, on the texts read (CLM-012 to CLM-016); Illinois
  exempts creditor's-name notice. No legal conclusion; the viewer's state check stays a
  precondition. Remaining unknowns: buyer trust and price.
- Strongest disconfirming evidence (added 2026-10-22): agent-only software now sells itself as
  "the AR desk" for small businesses at a flat fee. AccountsReceivable.ai charges $299 a month
  ($149 billed yearly) for email and text follow-up and $799 ($399 yearly) with AI phone calls
  (CLM-020); ARPilot charges $99 a month after 10 free invoices (CLM-020). The operator's modeled
  $300–$500 fee now sits at the software's price, so the operator must win on what software does
  not do: human dispute and missing-document handling, relationship calls, and one accountable
  person. CollBox, the human version, now lists $599 a month on a 12-month term ($729 month to
  month) plus a $999 setup fee (CLM-019).
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
- Existing alternatives or budget: free reminders in invoicing software; AR platforms (ARPilot
  $99 a month; AccountsReceivable.ai $299–$799 a month; Chaser Compact $259 a month for firms
  under $5M revenue; Upflow and Daylit unpriced, aimed at finance teams; Ramp added AR follow-up
  drafting for single-entity QuickBooks Online and NetSuite firms on 2026-09-22); done-for-you
  services (CollBox $599 a month yearly, $729 month to month, $999 setup; Chaser Compact plus Care,
  a dedicated AR specialist with calls and disputes, $1,199 a month); part-time clerks; contingency
  agencies after about 90 days (CLM-004, CLM-005, CLM-007, CLM-008, CLM-017 to CLM-020, CLM-022).
- Buyer payment record (2026-10-22): found, seller-published. CollBox's own pages name paying
  small law firms with owner quotes (Pinay Law, Trusler Legal, Pines Federal Employment, TAW Law)
  and a May 2026 case study of a six-attorney firm, Ad Astra Law Group (CLM-019). Seller-chosen
  testimonials: they show that some small firms pay a human desk, not how many or for how long.
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
  threads are partly posted by tool builders. Adjacent (2026-10-22): Atradius reports about seven
  in ten US businesses face late B2B payments, about 23% of receivables affected, and Ramp calls
  AR "a top request from our customers" (CLM-022; secondary and seller statements).
- Strongest existing coverage: vendor guides (Xero, June 2026; QuickBooks) on chasing invoices;
  AR-agent vendor content (Kolleno, Gaviti, Daylit coverage) aimed at finance teams.
- Information gap: nobody covers a solo operator selling the outcome to small firms, the
  hand-back and lock rules, and the state licensing line.
- Pitched-venture check (idealab.ai, 2026-10-22; 1 search, 2 briefs): the idea already circulates
  as a funded-team venture. Search "chase overdue B2B invoices for small businesses done-for-you"
  returned at least six close ideas, including "Managed Receivables Desk for Small Businesses"
  (idea 1544380, its own field check `crowded`) and "Receivables Autopilot for Bookkeeping Firms"
  (idea 1551755, `contested`). Both assume 2–20 staff and $60,000–$120,000 to start. Coverage and
  differentiation risk: the episode cannot claim the idea is new; its angle is the one-person
  version, the price squeeze, and the licensing line. idealab's scores and revenue figures are not
  used. Its competitor lists were checked on the vendors' own pages (CLM-020, CLM-021); Invoiced,
  Paidnice, QLink-Pay, and Plooto were not opened this run.
- Candidate original finding (2026-10-19, synthesis credit not yet scored): commercial invoice
  follow-up sits outside most consumer debt-collection licensing, but a few states (Florida,
  Washington) define collection to include business claims. Vendor and AR-agent coverage read
  this run does not mention the line. Limit: statute text read by a non-lawyer, eight states only,
  no regulator guidance or case law; it tells the viewer where to check, not what is allowed.

## Proposed synthesis

- Parallel A and supported component: CollBox -> offer shape, flat pricing unit, boundary (no
  dispute negotiation, 90-day hand-back, locked accounts).
- Parallel B and supported component: part-time AR clerks -> old-way spend and job scope.
- Parallel C and supported component: AI AR platforms -> agent follow-up is technically feasible.
- New combination: CollBox's done-for-you model, run by one operator on agents, sold outside law
  and accounting at a lower flat fee, with dispute triage included.
- Primary transfer risk: legal status of a third party contacting another business's customers
  about past-due invoices (CLM-009 to CLM-011); buyer trust in agent-written messages.
- Analogy map: `../03-validation/candidate-2026-10-15-receivables-desk-analogy-map.md` (2026-10-19; addendum 2026-10-22).

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
  bookkeepers and fractional CFOs who already see the aging reports. Adjacent model (2026-10-22):
  AR vendors sell collections to accounting firms as a service to resell or refer. Biller Genie
  runs a partner program paying commissions to accounting firms that offer AR automation to
  clients; AccountsReceivable.ai pitches accountants to "turn the aging report you already produce
  into a service clients pay for" (CLM-021). Seller copy: it shows vendors invest in this channel,
  not that bookkeepers refer outside desks. It also names the strongest rival: a bookkeeper who
  adds the tool and keeps the client.
- Pricing model: modeled scenario; flat monthly fee anchored below CollBox's $599 entry tier and
  Chaser Compact plus Care at $1,199 (CLM-017), above Chaser's self-run $259 tool. The pitch is the
  outcome of the specialist service at close to the price of the tool.
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
| Software and contractors | about $1,000–$2,500 per month (base); $2,970–$4,470 per month (sensitivity) | Agent, calling, mailbox, and accounting connectors. Published per-business seats: ARPilot $99, AccountsReceivable.ai $149 (yearly) to $299 (monthly), Chaser $259 (CLM-017, CLM-020). AccountsReceivable.ai deploys one agent per client ledger for accounting firms but shows no multi-client price (CLM-021) | modeled | If the operator pays one seat per client at $99–$149, software is $2,970–$4,470 a month for 30 clients |
| Acquisition and overhead | about $500–$1,000 per month | Referral partners, registration or bond where required | modeled | State costs unknown |

Capacity case formula: `$400 x 30 clients x 12 months = $144,000 gross revenue`

Contribution case formula: `$144,000 - $0 delivery labor (owner) - $21,000 software - $0 contractors - $9,000 acquisition and overhead = $114,000 contribution before owner compensation and tax`

Sensitivity (2026-10-22): with one $99–$149 seat per client, software is about $35,640–$53,640 a
year, and contribution falls to about `$144,000 - $35,640 to $53,640 - $9,000 = $81,360 to $99,360`
before owner compensation and tax. At a $300 fee the same case is `$108,000 - $35,640 to $53,640 -
$9,000 = $45,360 to $63,360`. The model stays positive but thin at the low price; price is the
viewer's first test.

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
  California's licensing act excludes covered commercial debt, and its covered commercial debt is
  owed to lenders, financing providers, or debt buyers and excludes trade credit (CLM-012). Texas
  chapter 392 covers consumer debt (CLM-013). New York has no state licence; New York City's
  licence covers consumer-purpose debt (CLM-014). Georgia's banking department regulates no
  collection agencies (CLM-015). Pennsylvania's collection-practices act covers consumer debt; no
  Pennsylvania licensing statute was found, which is not proof none applies (CLM-016). FDCPA
  applies to consumer debts only (scout record; not re-read). No legal conclusion is made here.
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
| CLM-012 | California: the Debt Collection Licensing Act does not apply to the collection of covered commercial debt (Fin. Code 100001(c), as amended by SB 1286, effective 2025-01-01); covered commercial debt is owed by a natural person to a lender, commercial financing provider, or debt buyer, up to $500,000, and excludes trade credit (Civ. Code 1788.2(n)–(p)); verified | Cal. Fin. Code 100001 <https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=FIN&sectionNum=100001> (read via Exa); Cal. Civ. Code 1788.2, FindLaw copy current as of 2026-01-01 <https://codes.findlaw.com/ca/civil-code/civ-sect-1788-2/> | 100001(a), (c); 1788.2(h)(2), (n), (o), (p) | current code / 2026-10-19 | not captured | primary (official site) and code copy; high | direct (boundary) | 2027-07-01 | An agency invoicing a business client is not a lender; non-lawyer reading; Rosenthal conduct rules may still reach guarantors of covered commercial credit |
| CLM-013 | Texas: Finance Code chapter 392 defines consumer debt as an obligation primarily for personal, family, or household purposes, and the third-party debt collector bond attaches to that chapter; verified (definitions) | Tex. Fin. Code 392.001, Public.Law copy <https://texas.public.law/statutes/tex._fin._code_section_392.001> | 392.001 definitions | current / 2026-10-19 | not captured | primary-law copy; medium-high | direct (boundary) | 2027-07-01 | Official site returned an index only; 392.101 bond text not re-read |
| CLM-014 | New York: no state-level debt collection licence; Buffalo, Yonkers, and New York City license locally; New York City's code defines debt as consumer-purpose, excluding commercial collectors; verified | Mayer Brown <https://www.mayerbrown.com/en/insights/publications/2024/12/new-york-city-overhauls-debt-collection-rules-and-proposes-new-debt-collector-definition> (read via Exa) | "Regulation and Licensing of Debt Collection in New York" | 2024-12 / 2026-10-19 | not captured | law-firm analysis; high | direct (boundary) | 2027-01-15 | Buffalo and Yonkers scope not read; pending state bills not checked |
| CLM-015 | Georgia: the Department of Banking and Finance "does NOT regulate collection agencies, debt collectors, or other entities or individuals collecting debts"; verified | Georgia DBF, Debt Collection <https://dbf.georgia.gov/node/14341> (read via Exa) | Opening statement | undated / 2026-10-19 | not captured | state agency; high | direct (boundary) | 2027-07-01 | Fair Business Practices Act conduct rules still apply |
| CLM-016 | Pennsylvania: the Fair Credit Extension Uniformity Act (Act 7 of 2000) defines debt as an obligation for personal, family, or household purposes; no Pennsylvania collection-agency licensing statute was found; verified (definition), unknown (licensing) | Act 7 of 2000, Pa. General Assembly <https://www.legis.state.pa.us/WU01/LI/LI/US/HTM/2000/0/0007..HTM> (read via Exa) | Section 3, "Debt", "Debt collector" | 2000 act / 2026-10-19 | not captured | primary; high for definition | direct (boundary) | 2027-07-01 | Secondary sources conflict on licensing; absence not proven |
| CLM-017 | Chaser pricing: Compact $259 a month (revenue under $5M, 4 users); Core $779; Care add-on with dedicated AR specialist, payment follow-ups, phone calls, inbox management, and dispute handling; Compact plus Care $1,199 a month; no stated minimum term; verified as seller terms | Chaser pricing <https://www.chaserhq.com/pricing> | Plan table and Care description | page © 2026, undated / 2026-10-19 | not captured | seller page; medium | substitute (context) | 2027-01-15 | Seller terms; not buyer payment; plan feature mapping for AI and calls not shown |
| CLM-018 | Upflow Starter covers up to $10M invoiced revenue and 40,000 invoices a year with email, SMS, call, and letter reminders, price not shown; Daylit sells AR agents to finance teams on NetSuite, Sage Intacct, and Dynamics, "200+ enterprises", price not shown; verified as seller terms | Upflow pricing <https://upflow.io/pricing>; Daylit <https://www.daylit.com/> (both read via Exa) | Plan list; home page | undated / 2026-10-19 | not captured | seller pages; medium | substitute (context) | 2027-01-15 | No published price; aggregator listings unverified |
| CLM-019 | CollBox lists $599 a month on a 12-month term ($729 month to month) plus a one-time $999 setup fee; a dedicated US-based AR expert makes the calls; flat fee, never touches funds; unpaid after 90 days returned to the firm; "CollBox Collect" refers disputed or defaulted accounts to a vetted agency; named owner testimonials (Pinay Law, Trusler Legal, Pines Federal Employment, TAW Law) and a case study of Ad Astra Law Group, six attorneys, San Francisco; verified as seller terms and seller-published customer records | CollBox pricing <https://collbox.co/pricing/> (read via Exa); case study <https://collbox.co/blog/how-a-san-francisco-litigation-boutique-recovered-469000-in-ar-and-found-her-dream-car-along-the-way/> (read via Exa) | Plan box, FAQ, testimonials; case study "The Firm" and "The Diagnostic" | pricing undated; case study 2026-05-29 / 2026-10-22 | not captured | seller page; medium (terms), low-medium (customer records, seller-selected) | direct (observed model; buyer payment, seller-published) | 2027-01-15 | Seller's recovery figures ($66K a month average, 40% faster) are not used; testimonials are chosen by the seller |
| CLM-020 | AccountsReceivable.ai sells an agent "AR desk" to small businesses: Starter $299 a month ($149 billed yearly), QuickBooks or Xero, email and text follow-up, cash application; Growth $799 ($399 yearly) adds live AI phone calls; flat fee, no share of collections. ARPilot: free on 10 invoices a month, then $99 a month, QuickBooks Online, email, text, and voice, dispute pauses. Dueflo: AI-written escalating email and text for QuickBooks, 14-day trial (price not read); verified as seller terms | AccountsReceivable.ai <https://accountsreceivable.ai/pricing>, <https://accountsreceivable.ai/accounts-receivable-software-for-small-business>; ARPilot <https://arpilot.ai/>; Dueflo <https://www.dueflo.com/> (all read via Exa) | Plan table; small-business page; "For small business" block; home page | undated / 2026-10-22 | not captured | seller pages; medium | substitute (strongest disconfirming) | 2027-01-15 | Seller terms; no buyer uptake; product quality unverified |
| CLM-021 | Biller Genie markets AR automation to accounting and bookkeeping firms as a value-added client service with a multi-client dashboard and a partner program paying commissions per referred client subscription ("hundreds of accounting firms", seller claim); AccountsReceivable.ai pitches accountants to deploy one agent per client ledger and package collections as a paid service; no multi-client price shown; verified as seller copy | Biller Genie <https://billergenie.com/accountants/>; AccountsReceivable.ai <https://accountsreceivable.ai/accounts-receivable-software-for-accountants> (both read via Exa) | Partner Revenue Program; "One agent per client ledger" | undated / 2026-10-22 | not captured | seller pages; low-medium | adjacent (go-to-market model; substitute) | 2027-01-15 | Shows vendor investment in the channel, not bookkeeper referral behavior |
| CLM-022 | Ramp launched AR on 2026-09-22 for US single-entity businesses on QuickBooks Online or NetSuite, drafting collections follow-ups and matching payments; Ramp called AR "a top request from our customers"; the article cites Atradius: about seven in ten US businesses face late payments, about 23% of B2B receivables affected; verified as reported | CFO Dive <https://www.cfodive.com/news/ramp-expands-accounts-receivable-cfos-seek-faster-cash-flow-ai/830994/> (read via Exa) | Dive Brief; Dive Insight | 2026-09-22 / 2026-10-22 | not captured | trade press of seller release and a survey; medium | substitute; adjacent demand | 2027-01-15 | Atradius figure read second-hand; Ramp customers skew larger than the target buyer |

## Unresolved questions

- Licensing: done for eight states (2026-10-19). Remaining: Buffalo and Yonkers scope; Florida bond
  and fee; other states with commercial collection registration. Not needed to advance; the
  episode names the check, not a map of all fifty states.
- Buyer payment: found 2026-10-22 as seller-published records (CLM-019): named small law firms
  pay CollBox. Outside law, and for an outside operator rather than a known vendor: viewer's first
  test.
- Tooling cost per client: published seats are $99–$299 per business (CLM-020); a multi-client
  price is not shown (CLM-021). Viewer's first test: quote one multi-client plan before pricing.
- Substitute: recorded 2026-10-19 (CLM-017, CLM-018). Chaser publishes $259 (tool) and $1,199
  (tool plus specialist); Upflow and Daylit publish no price and aim at finance teams on ERPs.
- Trust and price acceptance: viewer's first test.
