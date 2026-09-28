# Opportunity research brief: Overflow public-records processing for small public agencies

Template status: approved V2 Step 0.2 template; locked 2026-08-21.

Status: researching

Template version: `operator-blueprint-v2-step0.2`

Candidate ID: `candidate-2026-09-28-records-request-overflow`

Candidate brief: `../01-candidates/candidate-2026-09-28-records-request-overflow.md`

Candidate brief SHA-256: `3d53926e2f799817793ea6fabe705add4cb6f0fa69d2f4fe57347bd8e353e227`

Research cutoff: 2026-09-28

Research refresh date: not completed (research continues; proposed 2026-12-12, the current end date
of the Los Alamos contract in CLM-001b)

## Executive finding

- Opportunity: Task-order overflow processing of public-records requests for small agencies, with
  every disclosure decision left to the agency.
- Evidence class: adjacent synthesis
- Provisional verdict: plausible with bounded assumptions
- Main reason: A primary county contract shows an agency paying a non-law vendor $137.50–$245 per
  hour to review, redact, and produce public-records responses on task orders (CLM-001). A city RFP
  seeks the same labor while keeping final disclosure decisions (CLM-006). Small agencies report
  five- and six-figure annual costs for the work (CLM-003, CLM-004), and Washington statewide data
  confirms the scale (CLM-005). This is the first bench candidate with a primary buyer-paid record
  for the residual itself.
- Largest unresolved question: The switching question. Would a small agency contract a small
  AI-enabled operator rather than add staff, lean on counsel, buy software for its clerk, or use an
  established e-discovery firm like the one in CLM-001? No evidence yet on a solo operator winning
  such work, and no measured hours per request with AI review.
- Required public framing: The county contract and statute are observed facts. The small-agency
  cost figures are officials' statements at public meetings, reported through AI-written summaries.
  A solo AI-enabled operator is an adjacent synthesis; its price, hours, and win rate are hypotheses.

## Buyer reality

- Buyer: Records officer, clerk, or administrator at a school district, township, small city, or
  small county with one records officer and no in-house e-discovery.
- End customer or beneficiary: Requesters and agency staff and counsel.
- Recurring problem: Search, review, redaction, and production of voluminous requests under
  statutory deadlines.
- Consequence and frequency: Methacton SD, 64 requests in 2025–26 at about $126,627 total, about
  $1,979 per request (CLM-003, derived). Longview SD, 151 requests in eight months of 2026 vs 53 in
  all of 2025, $96,556.58 outside legal support for records processing (CLM-004). Washington
  statewide, 483,861 requests, $128 million, 1.7 million hours in 2024 (CLM-005).
- Existing alternatives or budget: staff specialist posts (CLM-003), outside counsel (CLM-003,
  CLM-004), outside e-discovery consultancy (CLM-001), outside consultant RFP (CLM-006), portal
  software, anonymous-request bans (CLM-007, CLM-008).
- Why now: AI request tools send broad, duplicated requests at scale (CLM-007, CLM-008); requests
  carry more video and large digital files (CLM-006); AI review lowers the per-document cost of
  answering.

## Evidence landscape

### Direct evidence

- CLM-001: Los Alamos County, NM contracted LSP Data Solutions (effective 2023-12-13, NTE $350,000
  plus tax) to "review, prepare, process, respond and document" IPRA/FOIA requests, including
  keyword search, review, redaction, production, and release documentation, on task orders priced at
  published hourly rates. The consultant "may be required to submit completed request(s) to the RIM
  Program Manager for review prior to releasing records". Same job, same decision boundary. Limit:
  the contract also covers legal e-discovery; the records share of spend is not separable; the
  buyer is a well-funded county and the vendor is an established firm with a certified
  e-discovery specialist.
- CLM-001b: Amendments raised the cap to $630,000 and then $722,000 and extended to 2026-12-12,
  with staff citing "rapidly growing volumes of records requests" and video redaction (AI-written
  meeting summary and search snippets; amendment documents not opened).
- CLM-006: City of Ithaca, NY RFP (reported 2026-07 and 2026-08-06) for a "firm or individual"
  to supplement FOIL staff; the city keeps "final decisions about disclosure and compliance".
  Individual consultants are named as eligible. RFP document, budget, and award not yet seen.

### Adjacent business evidence

- E-discovery review consultancies (CLM-001 vendor type) sell the same review-and-redaction labor to
  law firms and litigants. Shared structure: document review under deadline with a decision-maker
  above the reviewer.
- CLM-002: Michigan FOIA MCL 15.234(1)(b) lets an agency with no employee able to separate exempt
  material treat "necessary contracted labor costs" like employee labor when charging requesters,
  capped at six times the state minimum hourly wage, with the "contracted person or firm" named on
  the itemization. Statutory recognition of the contracted-separation role and a partial fee pass-
  through. Limit: case-by-case, only when fees are charged, and the cap binds recharge, not what the
  agency pays.

### Component feasibility evidence

- CLM-009: MuckRock (2026-07-15) cites OGIS's 2024 self-assessment that 18.6% of responding federal
  agencies use AI or machine learning in FOIA processing. Context for AI review adoption; federal,
  not small-agency.
- AI review and redaction tools (Logikcull, CaseGuard, Polimorphic, portal-bundled redaction) exist;
  prices not collected this run.

### Scaled relevance

- CLM-005: Washington JLARC 2024 Public Records Reporting (published 2025-12): 483,861 requests,
  $128 million, 1.7 million hours, 24 days average to closure. Only agencies spending over $100,000
  must report metrics; school-district reporting rate 8%. Derived averages (not stated by JLARC):
  about $265 and 3.5 hours per request.

### Demand and competition

- Exact target queries: "public records request backlog", "AI public records requests", "outsource
  FOIA processing".
- Adjacent query or question families: requester-side "agency not responding" questions (pool lead,
  titles only).
- Volume source, attempted measurement, and date: not measured this run.
- Other demand signals: CLM-001, CLM-001b, CLM-006 (procurement); CLM-003, CLM-004 (spend).
- Independent signal count: four agencies across four states (NM, NY, PA, WA) plus a statewide
  dataset.
- Strongest existing coverage: MuckRock requester guidance (CLM-009); GovTech agency-policy coverage
  (CLM-007, CLM-008); vendor software marketing (e.g., Granicus on JLARC data, CLM-010).
- Information gap: No coverage observed treats the answering labor as a contracted service with
  observed rates, or maps where the processor's work must stop.

## Proposed synthesis

- Parallel A and supported component: Los Alamos e-discovery task-order contract → offer scope,
  hourly/task-order pricing unit, decision hand-back (CLM-001).
- Parallel B and supported component: Ithaca RFP → buyer behavior at a small city; eligibility of an
  individual consultant (CLM-006).
- Parallel C and supported component: Michigan contracted-labor provision → statutory contracting
  route and partial recharge (CLM-002).
- New combination: AI review lets a single operator deliver part of what an e-discovery firm
  delivers, at the volume a small agency needs.
- Primary transfer risk: The buyer in Parallel A is larger and the vendor is an established firm;
  small agencies may lack the budget, procurement path, or trust to contract a solo operator.
- Analogy map: not created this run.

## Proposed Operator Blueprint

- Offer: Master services agreement plus task orders for overflow processing.
- Buyer outcome: Release-ready installments and logs; backlog and days-to-installment reduced.
- Delivery workflow: task order scoping → file intake from agency systems → de-duplication → AI
  responsiveness and exempt-content pass → human verification of every mark → installment and draft
  exemption log → records officer and counsel approval → reporting log.
- Technology and human stack: agency system access or an approved review platform; AI review and
  redaction; operator verification. Tools second.
- Required skills or credentials: records law familiarity in the target state, review discipline,
  data-security practice; CLM-001 required an e-discovery certification — whether small buyers
  require one is unknown. Insurance requirements unknown.
- Go-to-market path: RFP response (CLM-006 type), cooperative purchasing, referral from the agency's
  records vendor or counsel. Unverified.
- Pricing model: hourly under an NTE, as observed (CLM-001). Solo pricing is a hypothesis.
- Defensibility: verified accuracy record and familiarity with a state's exemptions; weak against an
  agency that trains its own clerk on the same software.

## Modeled economics

Every number in this section is an internal Step 0 input until it is approved under
`content-os/facts.md` for public use.

| Input | Working value or range | Basis | Status | Sensitivity or caveat |
|---|---|---|---|---|
| Pricing unit | Hourly under NTE; $137.50–$245/hr observed for an established firm | CLM-001 | observed (one contract) | Established-firm rates; solo rates unknown |
| Client or transaction capacity | unknown | — | unknown | Requires delivery rehearsal |
| Delivery hours | ~3.5 hrs/request statewide average without distinguishing AI | CLM-005 derived | modeled | Mix includes trivial requests; voluminous requests far higher |
| Loaded labor cost | unknown | — | unknown | — |
| Software and contractors | unknown | — | unknown | Review tool pricing not collected |
| Acquisition and overhead | unknown; includes insurance and procurement effort | — | unknown | Likely material |

No capacity or contribution case is issued. Hours with AI review, solo pricing, and acquisition cost
are all unknown, so any formula would be false precision.

Disclosure: `Modeled scenario, not observed performance or an earnings forecast.`

## Narrative and audience hypothesis

- Operator protagonist: A records or paralegal professional deciding whether to build a processing
  desk.
- Starting state: One clerk, few requests.
- Inciting change: AI-written, duplicated, broad requests arrive in volume.
- Stakes: statutory penalties, wrongful-release liability, agency budgets.
- Causal mechanism: asking got cheap; answering did not.
- Build transformation: bounded desk with a hard decision hand-back.
- Decisions and tradeoffs: which records classes to refuse; hourly vs per-installment; how to prove
  accuracy.
- End state and payoff: synthetic request processed with hours logged against the observed county
  rate.
- Visual evidence classes: primary contract rate table, meeting cost figures, synthetic review
  screens, before/after backlog.
- Working audience promise: "Who gets paid when AI floods the records office."
- Honest packaging territory: AI on both sides of a public-records deadline.

## Risks and constraints

- Factual uncertainty: CLM-003 and CLM-004 are secondary transcriptions; Longview's surge may be
  event-driven (the district is under a public investigation); CLM-001 spend is not split between
  records and litigation discovery.
- Analogy-transfer uncertainty: established firm and larger county vs solo operator and small
  district.
- Legal or regulatory boundary: exemption and denial decisions stay with the agency; state records
  laws differ; FERPA school-official designation for school records; CJIS excludes police records;
  unauthorized-practice-of-law exposure if the operator advises on exemptions (CLM-001's "subject
  matter expertise" clause shows buyers may want exactly that).
- Permissions, privacy, or guest dependency: none for the episode; high data sensitivity for the
  business.
- Platform or vendor dependency: agency systems and review tools.
- Ethical failure mode: AI-missed personal data released; an operator shaping disclosure outcomes
  for convenience.
- Claims that must not be made: that agencies "must" or "commonly" outsource this; any earnings
  figure; that AI review is accurate enough to skip human verification; that Longview's or
  Methacton's surge is caused by AI; the Granicus 23-hours-per-school-request figure (CLM-010).

## Thirty-day validation plan

1. Desk: obtain the Ithaca RFP and award, the Los Alamos amendment staff reports and task-order
   totals, and the Methacton agenda-packet cost table; search two more states' procurement portals
   for records-processing task orders awarded to individuals or small firms.
2. Field (owner authorization required): three records-officer interviews on the switching question
   — staff vs counsel vs software vs outside processor — and what insurance and access they require.
3. Rehearsal: process a synthetic 1,000–2,000 document request with AI review and full human
   verification; log hours and error rate.

Success signal: at least one small agency (under ~50,000 population or a single school district)
awarding records-processing task orders to an individual or firm of fewer than five people, plus a
rehearsal showing hours per request well under the observed staff and counsel cost.

Kill or redesign condition: procurement and insurance requirements exclude solo operators in every
observed RFP, or records officers uniformly prefer software for their own staff.

## Source registry

| Claim ID | Claim and status | Source and URL/path | Exact locator | Published / accessed | Snapshot or local path / SHA-256 | Source type / confidence | Relationship | Refresh by | Caveat |
|---|---|---|---|---|---|---|---|---|---|
| CLM-001 | County contracts non-law vendor to review, redact, produce IPRA/FOIA responses on task orders at $137.50–$245/hr, NTE $350,000; verified | Incorporated County of Los Alamos, Services Agreement AGR23-53 with LSP Data Solutions, <https://losalamos.legistar.com/gateway.aspx?M=F&ID=ba34b0d2-6d08-42ba-a359-70c40c9bd298.pdf> | Section A.3(a)–(n); Section A.4; compensation clause; Exhibit A rate schedule | effective 2023-12-13 / 2026-09-28 | fetched PDF not retained in repo; SHA-256 `f0a8726c55a64e80b27d844e0a54bca0c6484e284a561d43c77284e5b53487db` | primary; high | direct | 2026-12-12 | Also covers legal e-discovery; records share not separable |
| CLM-001b | Cap raised to $630,000 then $722,000, term to 2026-12-12, citing growing request volume; qualified | Citizen Portal AI summary of Los Alamos County Council 2025-11-18, <https://citizenportal.ai/articles/7306530/new-mexico/los-alamos-county/council-extends-records-and-ediscovery-contract-citing-increased-volume-of-publicrecords-requests> | whole summary | 2025-11 / 2026-09-28 | not retained | secondary AI-written; medium | direct | 2026-12-12 | Amendment documents not opened |
| CLM-002 | Michigan allows contracted separation labor, recharge capped at 6x state minimum wage, contractor named on itemization; verified | Michigan Legislature, MCL 15.234, <https://legislature.mi.gov/Laws/MCL?objectName=mcl-15-234> | subsection (1)(b) | current / 2026-09-28 | not retained | primary; high | adjacent | 2027-09-28 | Non-lawyer reading; case-by-case; binds recharge only |
| CLM-003 | Methacton SD: 64 requests in 2025–26; specialist $70,119, asst. superintendent $24,872, legal $31,635, total ~$126,626.60; earlier 2026-03-24 report of 39 requests YTD, $85,700 staff and $16,600 legal; qualified | Citizen Portal AI summaries, <https://citizenportal.ai/articles/9813637/Pennsylvania/School-Districts/Methacton-SD/Superintendent-details-Right-to-Know-workload-and-costs-for-202526> and <https://citizenportal.ai/articles/7718421/Pennsylvania/School-Districts/Methacton-SD/Superintendent-reports-spike-in-RighttoKnow-requests-cites-legal-and-staff-costs> | whole summaries | 2026-07 and 2026-03 / 2026-09-28 | not retained | secondary AI-written of public meeting; medium | direct | 2027-07-31 | Figures said to be in agenda packet; packet not opened |
| CLM-004 | Longview SD: 151 requests Jan–Aug 2026 vs 53 in 2025; $96,556.58 outside legal for records processing through 2026-08-31; contractor, overtime, tracking system; qualified | Citizen Portal AI summary of 2026-09-14 board meeting, <https://citizenportal.ai/articles/10078311/washington/school-districts/longview-school-district/interim-superintendent-public-records-requests-nearly-tripled-and-legal-review-costs-spiked> | whole summary | 2026-09 / 2026-09-28 | not retained | secondary AI-written; medium | direct | 2026-12-31 | District under public investigation; surge may be event-driven; video not reviewed |
| CLM-005 | Washington agencies: 483,861 requests, $128M, 1.7M hours, 24 days average, 2024; verified | JLARC, 2024 Public Records Reporting, <https://leg.wa.gov/JLARC/reports/2025/PubRecordsData/default.html> | summary page | 2025-12 / 2026-09-28 | not retained | primary; high | context only (scale) | 2026-12-31 | Only large-spend agencies report metrics; low school-district reporting |
| CLM-006 | City of Ithaca RFP for a firm or individual to supplement FOIL staff; city keeps final disclosure decisions; qualified | Ithaca Times, <https://www.ithaca.com/news/ithaca/ithaca-seeks-consultant-to-assist-with-foil-requests/article_7d13b87e-6914-4e19-a510-efbd14fdacd5.html>; Ithaca Voice, <https://ithacavoice.org/2026/07/ithaca-to-bring-in-outside-help-to-clear-public-records-request-backlog/> (HTTP 429 on fetch) | article body | 2026-08-06 / 2026-09-28 | not retained | secondary news; medium | direct | 2026-12-31 | RFP document, budget, award not seen |
| CLM-007 | PA counties flooded by FOIA Buddy requests; anonymous-request bans; verified as reported | GovTech, <https://www.govtech.com/artificial-intelligence/governments-adjust-policies-amid-flood-of-ai-record-requests> | article body | 2024-08-14 / 2026-09-28 | not retained | secondary news; medium | context only | n/a | 2024; policy response reduces volume |
| CLM-008 | PA school districts received dozens to hundreds of broad FOIA Buddy requests; verified as reported | GovTech, <https://www.govtech.com/education/k-12/school-officials-suspect-ai-behind-burdensome-public-records-requests> | article body | 2024-08-16 / 2026-09-28 | not retained | secondary news; medium | context only | n/a | Attribution to AI is officials' suspicion |
| CLM-009 | Strongest existing coverage is requester guidance; OGIS 2024: 18.6% of responding agencies use AI/ML in FOIA processing; verified as reported | MuckRock, <https://www.muckrock.com/news/archives/2026/jul/15/using-ai-for-foia-in-2026-what-requesters-should-know/> | article body | 2026-07-15 / 2026-09-28 | not retained | secondary; medium | component | 2027-07-15 | Federal agencies |
| CLM-010 | 2.83 hrs/request (2018) and ~23 hrs per school-district request; not usable | Granicus blog on JLARC data, <https://granicus.com/blog/jlarc-metrics-explained-what-washingtons-data-reveals-about-the-true-cost-of-public-records/> | body | n/d / 2026-09-28 | not retained | vendor; low | context only | n/a | Vendor relay; primary 2018 data not opened |
| CLM-011 | Albuquerque added 15 records staff for its backlog; context only | Yahoo News (pool record) | — | — / not re-opened | not retained | secondary; low | context only | n/a | Large city |

## Unresolved questions

- Switching question (bench question 1): open. Evidence that would resolve it — an award to an
  individual or small firm (Ithaca award), records-officer interviews, or a Michigan fee itemization
  naming a contracted firm.
- Hours per request with AI review and full verification: open; resolved by rehearsal.
- Procurement and insurance minimums for small agencies: open; resolved by RFP documents.
- Whether the surge is durable or event-driven: partly open; four agencies in four states cite volume
  or complexity growth, but two (Longview, Los Alamos) name investigation or litigation as a driver.
- Unauthorized-practice boundary for "subject matter expertise" on exemptions: open; needs a
  qualified review per target state before any offer is described publicly.
