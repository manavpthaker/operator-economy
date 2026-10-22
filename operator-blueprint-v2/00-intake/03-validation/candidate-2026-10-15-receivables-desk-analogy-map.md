# Analogy map: Always-on receivables desk for small B2B businesses

Template status: approved V2 Step 0.2 template; locked 2026-08-21.

Template version: `operator-blueprint-v2-step0.2`

Candidate ID: `candidate-2026-10-15-receivables-desk`

Candidate brief: `../01-candidates/candidate-2026-10-15-receivables-desk.md` / `6aa08857621de2e834411aac197020247e55606d08e2e3b0ecc5ff59fb0803db`

Research brief: `../02-research/candidate-2026-10-15-receivables-desk-research.md` / `5a0b5dffa6aa9168e69f602cc89994751d7fcef2636a9058e1aa05833a7b0ccc`

Prepared: 2026-10-19

Evidence class: adjacent synthesis

## Synthesis thesis

This business is like CollBox for the offer and its boundary (a dedicated person follows up
past-due invoices under the firm's name for a flat monthly fee, with locked accounts and disputes
handed back), like the part-time AR clerk for the job and the money already spent on it, and like
AR-agent platforms (Daylit, Upflow, Chaser) for the claim that software can now send, call, and
read replies on its own. The new combination is one operator running agents across about 30 small
firms outside law and accounting, priced between a self-run tool ($259) and a vendor's
tool-plus-specialist service ($1,199), with the state licensing check made a precondition.

## Transfer records

| Analogy ID | Proposed-business component | Reference model | Source claim IDs | Relationship | Shared structure | Required adaptation | Does not prove | Break condition | Confidence | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| ANA-001 | Buyer/problem | QuickBooks 2026 small-business survey | CLM-001, CLM-002, CLM-003 | direct | Small firms owed money past 30 days, with cash strain | Narrow to firms invoicing businesses on terms without AR staff | That these owners want an outsider; one vendor's sample | Next quarterly survey shows the overdue share back near 2025 levels | medium | valid |
| ANA-002 | Budget or current alternative | Part-time AR clerk roles | CLM-004 | adjacent | Same job (chase past-due balances), paid by the hour | Employer pays an employee, not an outside desk; convert hours to a flat fee | Payment to an outside provider; employer size | Posting volume for part-time AR roles disappears | low-medium | valid (weak source; search summaries only) |
| ANA-003 | Offer and delivery | CollBox done-for-you follow-up for small law and accounting firms | CLM-005 | direct (observed model) | Same deliverable, flat monthly fee by client count, 90-day window, locks, dispute hand-back | Other niches; agents do drafting and calling instead of a staffer | That buyers pay or renew; results | CollBox closes or drops the human service | medium | valid |
| ANA-004 | Offer and delivery; price band | Chaser Care: dedicated AR specialist, calls, inbox, disputes added to a tool | CLM-017 | direct (observed model, seller terms) | Vendor sells the specialist outcome, not only the tool | Operator delivers it across clients at a lower price | Buyer uptake of Care | Chaser drops Care or prices it near $300 | medium | valid |
| ANA-005 | Delivery feasibility | AR-agent platforms (Daylit, Upflow) | CLM-008, CLM-018 | component | Agents send email, calls, texts; read replies; route disputes | Platforms target finance teams on ERPs; the operator needs multi-client tooling on small-business accounting systems | Agent quality on small-firm data; cost per client | No agent tool can be run across many small clients at a cost under about $80 per client a month | medium | valid |
| ANA-006 | Go to market | Bookkeepers and fractional CFOs who see aging reports | none | hypothesis | They see overdue balances and are trusted with books | Referral terms; partner trust | Any referral behavior | Partners will not refer outside contact with their clients' customers | low | weak (no source) |
| ANA-007 | Outcome measurement | Weekly aging report; 30+ day balance and DSO from baseline | CLM-005, CLM-018 | adjacent | Vendors report the same measures | Small-firm baseline is noisy month to month | That the desk causes improvement | Baseline too volatile to read over 30 days | medium | valid |
| ANA-008 | Legal boundary (constraint on offer) | State collection laws | CLM-009 to CLM-016 | direct (boundary) | Whether a third party may contact another business's customers about overdue invoices | Viewer checks their own state; Florida and Washington plausibly require registration | Legality anywhere; non-lawyer reading | Viewer's state requires a licence they will not obtain | medium-high | valid (as a constraint, not support) |

## Coverage test

| Pillar | Required status | Supporting analogies | Result | Remaining assumption and test |
|---|---|---|---|---|
| Buyer and costly problem | Must have usable direct or adjacent evidence. | ANA-001, ANA-002 | pass | Owners' willingness to let an outsider contact customers: viewer's first test |
| Budget or current alternative | May use direct, adjacent, or component evidence. | ANA-002, ANA-003, ANA-004 | pass | No buyer-side record of paying an outside desk: viewer's first test, scored as a gap |
| Offer and delivery | Must have a valid operating parallel or bounded first-party test. | ANA-003, ANA-004, ANA-005 | pass | Hours per client with agents: viewer's first test |
| Go to market | May use a transferable acquisition or diagnostic-entry model. | ANA-006 | fail (weak) | Referral path is an unsourced hypothesis; viewer's first test is five offers in one niche |
| Economics and capacity | Must have a transparent model with evidence for its inputs or explicit testable assumptions. | ANA-002 to ANA-005; research-brief model | pass | Price, capacity, and tooling cost are labelled modeled; testable in 30 days |
| Outcome measurement | Must define an observable buyer deliverable; business impact may remain a hypothesis. | ANA-007 | pass | Effect on collections stays a hypothesis |

## Evidence-floor verdict

- Usable direct or adjacent buyer/problem evidence: pass
- Valid analogy count: 6 (ANA-001 to ANA-005, ANA-007; ANA-008 is a valid constraint, ANA-006 weak)
- Independent source families: 6 (vendor survey; job postings; CollBox; Chaser; AR-agent vendors; primary state law)
- Required pillars covered: pass (go to market may use a transferable model and is the one weak
  pillar; it is resolvable through the validation plan)
- More than one untested inference hop in a load-bearing claim: no
- Uncovered pillars resolvable through the bounded validation plan: yes

Verdict: pass

Reason: The buyer problem, the old-way spend, and two observed done-for-you offers at published
prices carry the core claim directly. Agents are a component transfer only. Go to market is the
weak pillar and must be shown as the viewer's first test, not as a known channel.

## Disclosure carried forward

Adjacent synthesis. The viewer must hear that CollBox and Chaser sell this service at published
prices, but no buyer record of paying them was found; that the solo-operator version is a modeled
scenario; and that some states (Florida, Washington among those read) appear to treat this work as
collection, so the state check comes before the first client.

## Addendum 2026-10-22 (Thursday bench)

Research brief: `../02-research/candidate-2026-10-15-receivables-desk-research.md` (CLM-019 to CLM-022 added; hash in the scorecard)

New transfer records:

| Analogy ID | Proposed-business component | Reference model | Source claim IDs | Relationship | Shared structure | Required adaptation | Does not prove | Break condition | Confidence | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| ANA-009 | Go to market | AR vendors' accountant partner programs (Biller Genie commissions; AccountsReceivable.ai "service clients pay for") | CLM-021 | adjacent (seller-described channel) | The bookkeeper sees the aging report first and is the trusted path to the small owner | The operator partners with bookkeepers (referral fee) or is the bookkeeper; vendors pay commissions, so the operator competes with them for the same referral | That bookkeepers refer an outside desk, or that partner programs convert | Bookkeepers in the viewer's niche run the tool themselves and keep the client | low-medium | valid (weak) |
| ANA-010 | Budget (buyer pays a human desk) | CollBox named customers | CLM-019 | direct (seller-published records) | Small firms pay a flat monthly fee for a human to chase past-due invoices | Outside law; an unknown operator instead of an award-winning vendor | How many pay, for how long, or outside law | CollBox drops the human expert or its named customers leave | low-medium | valid |
| ANA-011 | Substitute (constraint on price) | Agent-only AR desks (AccountsReceivable.ai $149–$799; ARPilot $99; Ramp AR) | CLM-020, CLM-022 | substitute | Same follow-up, cash application, and dispute logging, run by software | The operator must add the human layer (disputes, missing documents, relationship calls, accountability) and price above the software | That owners actually run these tools well alone | Agent desks add a human specialist near $300–$500 | medium | valid (as a constraint) |

Coverage-test change: go to market moves from **fail (weak)** to **pass (weak, adjacent seller-described
model)** on ANA-009. Budget gains ANA-010. ANA-011 narrows the price band: the gap is no longer
"$259 to $599" but "above $99–$299 software, below $599–$729 human desk."

Evidence-floor verdict: unchanged, **pass**. Valid analogy count 8 (ANA-001 to ANA-005, ANA-007,
ANA-009, ANA-010), plus two valid constraints (ANA-008, ANA-011). Source families: 8 (adds
accountant-channel vendor pages and trade press).

Disclosure addition: the viewer must hear that AI tools already sell "the AR desk" for $99 to $299
a month, so the operator is paid for the human part, not the sending.
