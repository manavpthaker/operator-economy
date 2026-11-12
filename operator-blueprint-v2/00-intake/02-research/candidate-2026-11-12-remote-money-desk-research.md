# Opportunity research brief: Remote money desk for families of aging parents

Template status: approved V2 Step 0.2 template; locked 2026-08-21.

Status: researching

Template version: `operator-blueprint-v2-step0.2`

Candidate ID: `candidate-2026-11-12-remote-money-desk`

Candidate brief: `operator-blueprint-v2/00-intake/01-candidates/candidate-2026-11-12-remote-money-desk.md`

Candidate brief SHA-256: `7debe8a80a43c528cc560d1a676d1a5b192b7edb4aaab3f684fd228a29cce984`

Research cutoff: 2026-11-12

Research refresh date: not completed (first pass only)

## Executive finding

- Opportunity: A one-person, agent-run monthly desk that handles an aging parent's bills and watches
  their accounts daily, for the adult child who cannot do it from where they live.
- Evidence class: observed model
- Provisional verdict: plausible with bounded assumptions
- Main reason: Families describe the problem in their own words (CLM-001), and remote, monthly
  human services already sell the job (CLM-002, CLM-003). The agent change is in the watching,
  not the paying.
- Largest unresolved question: Will a family trust a remote desk with a parent's accounts, and how
  many hours does each household really take once calls and exceptions are counted?
- Required public framing: The remote service and its $250 floor are seller statements, not
  evidence that families pay it. Household counts, hours, and income are a modeled scenario. Trust
  and price are the viewer's first test.

## Buyer reality

- Buyer: An adult child, often in another state, of a parent who lives alone.
- End customer or beneficiary: The parent.
- Recurring problem: Mail the parent can no longer sort; bills missed or paid twice; premiums
  lapsing; scam charges noticed late (CLM-001; scout ledger items carried, CLM-009).
- Consequence and frequency: Not quantified from a primary source this run. Forum anecdotes only.
- Existing alternatives or budget: The child does it at night with online access, autopay, and
  mail forwarding (CLM-001 replies); local daily money managers by the hour (CLM-006, CLM-009);
  remote bill-paying services (CLM-002, CLM-003); alert apps where the family still does the work
  (CLM-004); general bill-paying services (CLM-005).
- Why now: Agents can read scanned mail and statements and check accounts daily, so watching costs
  far less per household than an hourly visit.

## Evidence landscape

### Direct evidence

- CLM-001: A long-distance sibling of a person with early dementia asks how to get help reading
  mail and acting on it (AgingCare, asked 2026-03-23, 14 answers). Replies: set up autopay, get POA,
  take over online access, and one says "DO NOT delegate ... Too much opportunity for fraud." Buyer
  voice, anecdote only. The scout ledger dated this question 2026-03-28; that is the date of the
  first answers.
- CLM-002: Parent Bill Pay sells exactly the job, remote, in any state, "From $250 a month", routing
  requests to one independent bookkeeping firm: mail redirected or scanned, each bill checked
  against the last before payment, a written proposal naming who approves payments and who gets
  the monthly report, backlog priced separately. Seller copy; it shows an offer and a stated floor,
  not that families pay it.
- CLM-003: SilverBills is a concierge bill-paying service with a dedicated account manager,
  guaranteed on-time payment, and liability and theft insurance; costs are not listed online
  (RetirementLiving review, updated 2026-01-22). Third-party review; a review site, not a buyer.

### Adjacent business evidence

- CLM-006: Local daily money managers sell the same scope in person (Granitefield Financial,
  Charlotte; Advanced Senior Solutions, Pinellas and Pasco FL; Daily Navigator, NJ). Daily
  Navigator's FAQ says AADMM represents "over 700 individuals & businesses" and that it carries
  professional liability and E&O cover. Seller copy; the AADMM count is secondhand.
- CLM-007: A nonprofit program (Ursuline "On Your Behalf") pairs daily money management with a
  monthly wellness check by a social service professional. Context: some of the work is welfare
  watching, not money.

### Component feasibility evidence

- CLM-004: Golden organizes a parent's accounts and alerts the family for $20 a month, with a care
  specialist call; the family still pays the bills. Seller copy.
- CLM-005: All Your Bills pays any bill from a photo for $49 a month, unlimited bills. General
  consumer service, not built for aging parents. Seller copy; shows payment handling is cheap.
- Agent reading of scanned mail and statements: not separately evidenced this run. Hypothesis
  until the viewer's first test times it.

### Scaled relevance

Not measured this run. The scout's NYT 2026-03-25 item was read as a summary only (CLM-009). No
count of parents living alone with cognitive decline, or of scam losses among older adults, is
used yet; a primary source (Census, FTC, or FBI IC3) is needed before any number is stated.

### Demand and competition

- Exact target queries: "bill paying service for elderly parents"; "daily money manager".
- Adjacent query or question families: AgingCare questions on a parent's mail, bills, and scams.
- Volume source, attempted measurement, and date: Google Trends US 5y, 2026-10-19 (scout):
  "daily money manager" low but measurable; weekly values not extractable.
- Other demand signals: several local and remote sellers; a household posting for a paperwork
  assistant for a 97-year-old in Manhattan (scout, not re-read).
- Independent signal count: 2 families (forum buyer voice; seller supply).
- Strongest existing coverage: seller explainers (Parent Bill Pay, DementiaCareCentral's bill-paying
  services guide, updated 2026-03-13) and AgingCare threads.
- idealab: "Household Bill Desk" (idea 1780265) and several eldercare-concierge ideas circulate as
  pitched ventures. Coverage and differentiation risk; idealab text is not evidence.
- Information gap: none of the coverage read shows what agents change about the daily watch, how one
  person caps households, or why the approval rule answers the forum's fraud objection.

## Proposed synthesis

- Parallel A and supported component: remote bill-paying services -> offer, remote delivery,
  monthly floor.
- Parallel B and supported component: local daily money managers -> scope, ethics, insurance norm,
  hourly price.
- Parallel C and supported component: EP010 receivables desk -> agents do the reading, the person
  owns exceptions.
- New combination: daily agent watching inside an approval-gated human service.
- Primary transfer risk: trust and per-household call time.
- Analogy map: not created.

## Proposed Operator Blueprint

- Offer: a monthly money desk per household; backlog clean-up priced separately.
- Buyer outcome: no missed or double-paid bills, no lapsed policies, odd charges flagged in a day,
  one shared weekly record.
- Delivery workflow: intake call and written household rules; mail redirect or scan; e-bill routing;
  agent reads and sorts each item; bills checked against the last; payments prepared; family or
  parent approves new or unusual items; daily account watch; weekly one-pager; same-day call on an
  alert.
- Technology and human stack: mail scanning, read-only account views where banks allow,
  document-reading and monitoring agents, a payment step the parent or the authorized agent
  controls; the operator owns rules, approvals, calls, and the record.
- Required skills or credentials: bookkeeping or household administration; no license found for
  daily money management (scout, context); bonding and E&O insurance are customary (CLM-006).
- Go-to-market path: referrals from elder-law attorneys, geriatric care managers, and local
  aging services; AgingCare-style forums are where the buyers ask.
- Pricing model: modeled from the $250 seller floor (CLM-002) and hourly DMM rates (CLM-009).
- Defensibility: the record and the approval discipline, plus a named insured person; not the
  software.

## Modeled economics

Every number in this section is an internal Step 0 input until it is approved under `content-os/facts.md` for public use.

| Input | Working value or range | Basis | Status | Sensitivity or caveat |
|---|---|---|---|---|
| Pricing unit | $250–$350 per household per month | CLM-002 floor; CLM-009 hourly | modeled | Seller floor only; price is the viewer's first test |
| Client or transaction capacity | 25 (low) to 50 (base) households | hours below | modeled | Scout's 60–80 not used; untested |
| Delivery hours | 2.5 hours per household per month | assumption | modeled | Calls and exceptions may dominate |
| Loaded labor cost | the operator's own time | n/a | modeled | Contribution is before owner pay |
| Software and contractors | about $30 per household per month (scanning, agents, storage) | assumption | modeled | Not priced this run |
| Acquisition and overhead | $6,000 a year plus about $3,000 insurance and bond | assumption | modeled | E&O and bond quotes not sought |

Capacity case formula: `$300 x 50 households x 12 months = $180,000 gross revenue`

Contribution case formula: `$180,000 - $0 delivery labor (owner) - $18,000 software - $0 contractors - $9,000 acquisition and insurance = $153,000 contribution before owner compensation and tax`

Low case: `$250 x 25 x 12 = $75,000`; less $9,000 software and $9,000 acquisition and insurance =
$57,000 before owner compensation and tax.

Base-case hours: 50 x 2.5 = 125 hours a month, about 29 a week before selling and admin.

Disclosure: `Modeled scenario, not observed performance or an earnings forecast.`

## Narrative and audience hypothesis

- Operator protagonist: a former bookkeeper or bank operations worker, or someone who has done this
  for their own parent.
- Starting state: the child finds a double payment and an unknown charity on a Sunday night.
- Inciting change: a shut-off notice or a lapsed premium.
- Stakes: money, coverage, the parent's control, sibling trust, the operator's liability.
- Causal mechanism: nobody near the parent owns the mail; autopay hides errors.
- Build transformation: rules, route, sort, watch, approve, record.
- Decisions and tradeoffs: what the desk may pay without asking; read-only versus payment access;
  how many households before quality slips.
- End state and payoff: a synthetic household's month of records and the viewer's stop rule.
- Visual evidence classes: documents, flows, state changes, comparisons.
- Working audience promise: How one person can watch a parent's money every day, and why the record
  matters more than the payment.
- Honest packaging territory: "The job families are told never to hand off."

## Risks and constraints

- Factual uncertainty: no primary count of the problem; remote prices beyond one floor unknown.
- Analogy-transfer uncertainty: trust from in-person to remote; call time per household.
- Legal or regulatory boundary: POA and account access; bank third-party rules; state elder
  financial abuse laws and any reporting duty; no investment, tax, legal, or Medicaid advice.
- Permissions, privacy, or guest dependency: synthetic household only; no real family's documents.
- Platform or vendor dependency: banks' read-only access and mail-scanning vendors.
- Ethical failure mode: the operator becomes the abuse risk the forum warns about; a sibling uses
  the desk against the parent's wishes.
- Claims that must not be made: that families pay remote desks at any price; any scam-loss or
  prevalence number without a primary source; any income figure as a forecast.

## Thirty-day validation plan

These are the viewer's first tests, not owner field work.

1. Write one household's rules and run a synthetic month of mail through the agent workflow; time
   every step, including the calls.
2. Offer the desk to five families through one referral source at a stated monthly price.
3. Ask each family what they would need to see before granting access, and record it.

Success signal: at least two of five families agree to a paid first month, and the timed workflow
stays under 3 hours per household.

Kill or redesign condition: fewer than two of five agree, or families will only pay for an
in-person visit, or the timed month exceeds 4 hours per household.

## Source registry

Every load-bearing claim must meet `../03-validation/EVIDENCE-STANDARD.md`.

| Claim ID | Claim and status | Source and URL/path | Exact locator | Published / accessed | Snapshot or local path / SHA-256 | Source type / confidence | Relationship | Refresh by | Caveat |
|---|---|---|---|---|---|---|---|---|---|
| CLM-001 | Long-distance family asks for help reading mail and paying bills; replies urge self-service and say never delegate; verified as anecdote | AgingCare, <https://www.agingcare.com/questions/how-can-i-find-assistance-with-reading-incoming-mail-identifying-issues-and-actions-that-need-to-be--498253.htm> | Question header; answers by Dianed58 and kahassenger1954, 2026-03-28/29 (read via Exa) | 2026-03-23 / 2026-11-12 | not saved | self-published forum; medium | direct | 2027-03-31 | One family; motive and outcome unknown |
| CLM-002 | Remote bill-paying service for families, any state, from $250 a month, one bookkeeping firm; verified as seller statement | Parent Bill Pay, <https://parentbillpay.com/> | Hero line "From $250 a month · Fully remote, any state"; "Bills in, bills paid" section (read via Exa) | undated / 2026-11-12 | not saved | self-published seller; medium | direct | 2026-12-31 | Seller copy; page routes to one firm; no buyer evidence |
| CLM-003 | SilverBills: concierge bill pay, dedicated manager, insured, prices not listed; verified as third-party review | RetirementLiving, <https://www.retirementliving.com/reviews/silverbills> | "Cons" list; "Much More than an Online Bill Pay Service" (read via Exa) | updated 2026-01-22 / 2026-11-12 | not saved | secondary review; medium | direct | 2026-12-31 | Review site; WebFetch blocked (403); silverbills.com returned 404 to WebFetch |
| CLM-004 | Golden alerts families for $20 a month; family does the work; verified as seller statement | Golden, <https://www.joingolden.com/> | Hero section (read via Exa search text) | undated / 2026-11-12 | not saved | seller; medium | component | 2026-12-31 | Seller copy |
| CLM-005 | All Your Bills pays any bill for $49 a month; verified as seller statement | <https://allyourbills.com/> | "Simple, flat rate" (read via Exa search text) | undated / 2026-11-12 | not saved | seller; medium | component | 2026-12-31 | General consumers, not seniors |
| CLM-006 | Local daily money managers sell the scope; AADMM "over 700"; E&O carried; verified as seller statements | Granitefield <https://www.granitefieldfinancial.com/services/bill-payment-for-seniors>; Advanced Senior Solutions <https://advancedseniorsolutions.com/daily-money-management/>; Daily Navigator <https://www.dailynavigatorllc.com/faq> | Service lists; FAQ "What is AADMM?" and insurance answer (read via Exa search text) | undated / 2026-11-12 | not saved | seller; medium | adjacent | 2026-12-31 | AADMM count secondhand |
| CLM-007 | Nonprofit DMM program with monthly wellness check; verified as seller statement | Ursuline On Your Behalf, <https://www.ursulineonyourbehalf.com/home/financial-support-services/> | "Daily Money Management" and "Wellness Checks" (read via Exa search text) | undated / 2026-11-12 | not saved | nonprofit seller; medium | adjacent | 2026-12-31 | Pricing section not read |
| CLM-008 | "Household Bill Desk" and eldercare-concierge ideas circulate on idealab; coverage risk only | idealab.ai search via `automation/tools/idealab.py` | ideas 1780265, 1315680, 1081057 | n/a / 2026-11-12 | not saved | AI-written idea database; low | context only | n/a | Never evidence |
| CLM-009 | Scout-ledger items carried, not re-read this run: AgingCare 496696, 497474, 466765; DMM $75–$150 an hour (Clear Money Guide 2026-08-03); NYT 2026-03-25 summary; Manhattan household posting | `automation/candidate-discovery/runs/2026-10-19.md` | ledger #13–#20 | 2021–2026 / 2026-10-19 | n/a | mixed; low until re-read | direct and context | re-read before analogy map | Not verified by the bench |

## Unresolved questions

- State rules on paying bills for a vulnerable adult, holding POA, and reporting suspected abuse
  (desk research; resolves the delivery boundary).
- Bank rules for read-only or agent access to an account (desk research).
- E&O, fidelity bond, and scanning costs (desk research; sharpens the model).
- A primary prevalence number for older adults' missed bills or scam losses (FTC, FBI IC3, CFPB).
- Remote prices beyond Parent Bill Pay's floor (SilverBills, other remote services).
- Trust and price for a remote desk: the viewer's first test, not desk research.
