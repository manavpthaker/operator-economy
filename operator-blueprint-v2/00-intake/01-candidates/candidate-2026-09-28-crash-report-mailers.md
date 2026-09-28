# Candidate: Crash-report review and compliant mailers for personal-injury firms

Template status: approved V2 Step 0.2 template; locked 2026-08-21.

Status: candidate

Template version: `operator-blueprint-v2-step0.2`

Candidate ID: `candidate-2026-09-28-crash-report-mailers`

Discovery lead: `DISC-2026-09-27-009` (owner-submitted; admitted by owner decision 2026-09-28,
`../OWNER-DECISION-2026-09-28-COACHING-STANDARD.md`)

Created: 2026-09-28

Owner: unassigned

Proposed evidence class: adjacent synthesis

## Opportunity in one sentence

In a state where the law allows it, an operator reads the crash reports a personal-injury firm
lawfully obtains, uses AI to drop the reports that are not worth a letter, and sends the firm's own
bar-compliant letter on the first lawful day — replacing the firm staffer who used to read every
report by hand — while the firm stays the requester of record and owns every word and every client
contact.

## Viewer outcome

- Viewer promise: Understand how injury firms already buy crash reports and mail drivers, which
  states make that lawful, where an unlicensed operator's work must stop, and why this is one of the
  easiest businesses to run unethically.
- Operator decision: Test, adapt, or reject a report-review-and-mail service for one firm in one
  open state, after seeing the observed report prices, the state map, the fee rules, and the
  harassment risk.
- Practical capability: Check one state's report-access statute and bar rule; price a mailing run
  per 1,000 reports; design a refusal list (fatal crashes, minors, opt-outs, repeat letters); set a
  fee that is not a per-case referral fee.
- Expected Operator Canvas: Buyer, costly job, one deliverable, state gate, requester-of-record
  rule, fee-structure rule, substitute map (in-house staff, mail houses, lead sellers, report
  brokers), per-1,000 cost model, ethics refusal list, falsification threshold.

## People

- Viewer/operator: Someone with legal-marketing, paralegal, or direct-mail operations experience
  who will work under a firm's supervision. Not a lawyer; must not act like one.
- Buyer: Managing partner or marketing lead at a small or mid-size personal-injury firm in an open
  state (Ohio, New Jersey, Indiana, Missouri, Nevada per the 2026-09-27 map).
- End customer or beneficiary: Drivers named in crash reports — who did not ask to be contacted.
  The firm benefits; recipients bear the intrusion.
- Guest or outside participant required: no. A synthetic crash report and a public statute are
  enough to show the workflow.

## Problem

- Costly problem: A firm that mails crash-report drivers pays for every report, pays staff to read
  each one for injury and fault, and mails many people who have no claim.
- Why it matters: One Washington firm bought 10,555 reports at $9.50–$10.50 each (2013–2017) and had
  an employee "review the reports with the goal of determining which of the parties involved in the
  accident was not at fault" (CLM-001, defendants' interrogatory answers quoted in a court filing).
  That firm then paid a $950,000 class settlement (CLM-002).
- Why now: AI can read scanned reports and narratives cheaply. Report access is also shrinking and
  litigation is active (CLM-005, CLM-011), which raises the value of getting the legal gate right.
- Existing alternatives and budget: in-house marketing staff buying and reading reports (CLM-001);
  private data brokers (CLM-004); law-firm mail houses advertising daily accident-report mail
  (CLM-012); per-lead sellers (context only).

## Proposed business

- Offer: For one firm in one open state, a monthly report-review-and-mail service: intake of the
  reports the firm obtains, AI pre-read for injury code, fault indicators, and exclusion flags,
  human check of every flagged report, mailing of the firm's approved letter on the first lawful
  day, suppression list, and a monthly log.
- Customer outcome: A mailed set with an exclusion log, delivered on the lawful date; measured as
  staff hours saved and letters per signed case, before and after.
- Delivery hypothesis: The firm requests reports in its own name; the operator processes them under
  a written vendor agreement; AI reads; the operator verifies; the firm's lawyer approves the letter
  and handles every call.
- Revenue hypothesis: Flat monthly fee or per-report-processed fee. Never per call, per signed
  client, or share of fees (CLM-008).
- Most important unproven assumption: That AI review saves enough staff time and mail cost, or
  raises letters-to-cases enough, for a firm to pay an outside operator on top of report fees —
  when the injury code is already a coded field on most reports (CLM-010) and mail houses already
  run the pipeline.

## Initial synthesis hypothesis

- Parallel A: In-house firm staff buying and hand-reading crash reports for fault (CLM-001) → the
  exact job and the old-way spend.
- Parallel B: Law-firm mail houses running daily accident-report mail (CLM-012) → the delivery
  pipeline and the main substitute.
- Parallel C: Bar lead-generator rules allowing non-recommending vendors paid a non-contingent fee
  (CLM-007, CLM-008) → the lawful fee structure.
- New combination: AI pre-read replaces the in-house reader and adds exclusion rules a mail house
  does not advertise.
- Suspected transfer risk: Mail houses may already filter by the coded injury field, leaving no AI
  edge; the report fee, not reading time, may dominate the firm's cost.

These are research directions, not evidence. The completed research brief and analogy map decide
whether the transfers are valid.

## Narrative potential

- Starting state: A firm staffer clicking shopping-cart icons on a state report site, 15 reports at
  a time (CLM-001).
- Inciting change: AI can read the reports; courts and legislatures are closing access.
- Causal mechanism: Reports are cheap per unit; reading them and mailing everyone is not.
- Operator build: A bounded review desk with a legal gate per state and a refusal list.
- Stakes and tradeoffs: speed vs intrusion; filtering for severe injury vs the rule against
  soliciting people who cannot judge clearly (CLM-009).
- End state: A synthetic batch run on screen with its exclusion log and per-1,000 cost, and the
  viewer deciding whether their state is even open.
- Visual evidence: The 24-state map, the Swapp filing excerpt, a KABCO-coded report field, a
  compliant letter with its required notice, a cost-per-1,000 table.

## Audience pull

- Exact or adjacent viewer questions: "why do I get letters from lawyers after an accident"
  (victim-side, CLM-013 search results); mail-house marketing to firms.
- Initial interest signals: active litigation (CLM-002, CLM-004, CLM-011); vendor content.
  No firm-side question signal found.
- Timely tension: Georgia Supreme Court argument, week of 2026-09-22 (CLM-011).
- Coverage gap: Coverage is vendor marketing or victim warnings. None maps state access law, fee
  rules, and ethics for a would-be operator.
- Honest working premise: "Injury firms already pay to read crash reports and mail drivers. Here is
  where that is legal, what AI changes, and why most versions should not be built."

## Discovery and POV

- Search-volume status: attempted but not measurable (no tool run this session).
- Operator Economy POV: Original synthesis, provisional: the state gate and the requester-of-record
  rule decide this business before any AI does.
- POV evidence: 2026-09-27 state map (`automation/candidate-discovery/runs/2026-09-27.md`) plus
  primary filings and statutes in the research brief.
- POV boundary: No owner experience in legal marketing. The legal readings are a non-lawyer's
  reading of statutes and rules, not legal advice.

## Initial evidence status

- Buyer-problem evidence: usable direct (CLM-001, one firm; CLM-003 context)
- Budget or current-alternative evidence: usable direct (CLM-001 report spend and staff reader)
- Offer and delivery parallel: usable (CLM-001, CLM-012 seller-only)
- Economics or capacity inputs: lead found; conversion rate unknown
- Audience-interest signals: one signal family (litigation and vendor content); not triangulated
- Narrative engine: plausible

## Known blockers

- State law: 9 of 24 states researched are closed, 9 restricted; 5–6 open. Some states make it a
  crime or a sworn-statement violation (CLM-006, Maryland; Florida).
- Federal privacy law: whether crash reports are DMV records under the Driver's Privacy Protection
  Act is unresolved; one district court said yes (CLM-004); a $950,000 settlement followed a
  similar claim (CLM-002).
- Fee rules: per-case or contingent pay is an improper referral fee (CLM-008).
- Ethics: the scoring goal (find the badly injured) points straight at the people bar rules protect
  (CLM-009) and at the conduct the Supreme Court found intrusive (CLM-003).
- The AI edge may be a filter on a coded field, not AI.

## Intake decision

Decision: research

Reason: Owner-admitted. A primary court filing shows a firm paying for the exact job the old way
(reports plus a staff reader). The delivery line, fee rule, and ethical boundary are clear enough to
research; the AI edge and economics are not.
