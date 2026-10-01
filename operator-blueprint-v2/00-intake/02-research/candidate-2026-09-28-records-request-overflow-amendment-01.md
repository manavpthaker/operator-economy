# Step 0 evidence amendment 01: Ithaca RFP and Los Alamos amendment opened at source

Status: recorded

Template version: `operator-blueprint-v2-step0.2` (amendment record; the reviewed candidate brief and research brief are unchanged, so their hashes still hold)

Candidate ID: `candidate-2026-09-28-records-request-overflow`

Research brief amended (by reference only): `candidate-2026-09-28-records-request-overflow-research.md` / `1267b2e951f75fda8d90f91d6ce99c5f4b64843f784e2396cd3e8598ec15a2ce`

Disposition: `../03-validation/candidate-2026-09-28-records-request-overflow-disposition.md` / `4f7c1ea91a993e61c93e95668debd4ba0283b9080c0ed72dfcdc58c1948a7d5c` (continue research; desk re-entry items 1 and 2)

Governing decision: `../OWNER-DECISION-2026-09-28-COACHING-STANDARD.md` / `95c781cba2a8ad5d8f76dda597329e0f84b4732226f9c8886a9520f0af2cd686`

Recorded: 2026-10-01

Recorded by: the Step 0 research bench (Thursday run)

## Why this record exists

The disposition named two desk items. This run opened the primary documents behind both. It does
not change any score, gate, disposition decision, pool entry, or queue row.

## Re-entry status

| Item | Required | Found | Status |
|---|---|---|---|
| 1 | Ithaca RFP **and** award, or another primary award to an individual or firm under five people at a small agency | RFP, terms, and blank bid tab opened at source (CLM-006a). No award, contract, or council record found | **partial** |
| 2 | Los Alamos amendment staff report or task-order totals separating records work from litigation, **and** the Methacton agenda-packet cost table | Amendment 1 staff report and IPRA progress sheet opened (CLM-001c, CLM-001d). Methacton packet not located; only the AI-written summaries surface | **partial** (Los Alamos half met) |

Neither item is complete, so the candidate does not advance to an analogy map and scorecard.

## New and upgraded claims

### CLM-006a — Ithaca RFP opened (upgrades CLM-006 from news to primary)

- Source: City of Ithaca, City Attorney's Office, "Support for Fulfillment of Requests under Freedom
  of Information Law (FOIL)", bid posting <https://www.cityofithacany.gov/bids.aspx?bidID=252>;
  RFP <https://www.cityofithacany.gov/DocumentCenter/View/21425> (SHA-256
  `b166a983a54357ab31e210bc57fd5042d811a627123285ac03ceba41b0c69563`); Appendix B terms
  <https://www.cityofithacany.gov/DocumentCenter/View/21514> (SHA-256
  `7c454b6ad2ad2fd35278a97d4a88558b40dcf42db53aca6f1dac53e1409ed116`); Appendix A bid tab
  <https://www.cityofithacany.gov/DocumentCenter/View/21513> (SHA-256
  `424086fd9a060ec2e71d0b74940701d46291eef66cbc91173392be2a4c4ae632`). Posted 2026-07-14, closed
  2026-08-04; accessed 2026-10-01. Files not retained in repo.
- Locators: RFP p.1 (eligibility, summary, scope); p.2 (submission requirements, cost proposal);
  p.3 (dates, evaluation, payment); p.4 (insurance, award, contract extension). Appendix B ¶3, ¶5, ¶6,
  ¶9. Appendix A whole sheet.
- What it establishes:
  - "qualified firms or individuals" may bid to "conduct a substantive review" of responsive records
    (p.1).
  - Scope: confirm records fit the request, redact under FOIL, prepare for release "with a
    description of the redaction and bases for appeal"; the contractor may do a first review or a
    "second review" after City Attorney administrative staff did the first (p.1). The City Attorney
    and City Clerk's Office keep the work; news coverage (CLM-006) says the city keeps final
    disclosure decisions.
  - **The job is a one-off backlog.** The contractor reviews records "on the previous platform";
    the city "recently transitioned to a new FOIL fulfillment platform which expedites review" (p.1).
  - Cost proposal: names, titles, hourly rates, overhead (p.2). No budget stated.
  - Three weeks to bid; selection 2026-08-06; kickoff 2026-08-10 (p.3).
  - Contractor indemnifies the city, carries city-specified insurance naming it additional insured,
    and shows workers' comp and disability coverage **or that it is not required to** (Appendix B
    ¶5, ¶6, ¶9). Independent-contractor status (¶3). Other authorized users may piggyback on the
    award under NY General Municipal Law (p.4).
  - Bid tab is a blank scoring template (opening 2026-08-05): no bidders, rates, or award.
- Limit: award, winner, size of winner, rate, and contract value unknown. Insurance limits not
  stated.
- Allowed inference: a city of roughly 32,000 wrote a procurement a solo reviewer could legally
  answer, priced by the hour. Not allowed: that an individual won, or that the work recurs.

### CLM-012 — Ithaca cleared 500+ requests in-house on new software (substitute evidence)

- Source: City of Ithaca, "August Update from the Office of the City Manager",
  <http://www.cityofithacany.gov/CivicSend/ViewMessage/message/297227>; 2026-08; accessed 2026-10-01.
- Locator: FOIL line: "Launch of CivicPlus for FOIL requests, with the internal completion of over
  500 requests in 5 months since launch."
- Establishes: the same city that sought outside review for its legacy backlog handles new
  requests internally on new software.
- Allowed inference: for this buyer, outside review fills a transition gap; the standing substitute
  is software for the clerk. This is the strongest disconfirming fact found so far for a
  *recurring* overflow desk.

### CLM-001c — Los Alamos Amendment 1 staff report (upgrades CLM-001b in part)

- Source: County of Los Alamos Legistar file AGR1081-24, "Approval of Amendment No. 1 of Agreement
  No. AGR23-53 with LSP Data Solutions",
  <https://losalamos.legistar.com/LegislationDetail.aspx?From=RSS&ID=7023231&GUID=A42B5300-1CF1-4D24-A219-071DB0A0A785>;
  file created 2024-11-04, Council consent agenda 2024-11-19; accessed 2026-10-01; page SHA-256
  `c59c1d6ed35c41107e6895464deba2e18221f53d0d66b937c009e75bcdd36c47` (dynamic page; hash is of this
  fetch only).
- Locator: Title; Body paragraphs 1–2.
- Establishes: the cap rose from $350,000 to $630,000 plus tax "for e-Discovery Services and
  Expertise in Response to Information of Public Request Act (IPRA)". The original $350,000 "will be
  fully utilized by November 30, 2024" — under 12 months from the 2023-12-13 start. LSP "helping
  manage IPRA requests to meet the requirements of legally imposed deadlines" and its work "has
  significantly reduced the backlog of IPRA documentation requiring review."
- Limit: Amendment 2 ($722,000, to 2026-12-12) remains secondary (CLM-001b); its staff report also
  cites litigation discovery.
- Allowed inference: through November 2024 the spend was described as records-request work, not
  litigation.

### CLM-001d — Los Alamos IPRA project progress sheet

- Source: Attachment C to AGR1081-24, "IPRA Project Progress Spreadsheet - Redacted",
  <https://losalamos.legistar.com/View.ashx?M=F&ID=13554002&GUID=40337A17-09F8-4BAC-B8E2-78237234B225>;
  accessed 2026-10-01; SHA-256 `185dfe3001182c7a2787f4a5a354fd648db865415b72e64ed13e921ff65513ac`.
  One page.
- Locator: whole sheet; text extraction is jumbled across tables, so only figures whose labels are
  unambiguous are used.
- Establishes (as read): one requester's request ("#17") counted about 1.07 million documents and is
  listed "Ongoing" with 1,647 service hours; monthly documents reviewed including duplicates,
  March–September 2024, total 311,035; a topic list of 84 requests, 71 completed and 13 remaining;
  staff split as Senior Consultant and two Data Analyst roles. Most other listed requests took
  between half an hour and 44 hours.
- Limit: redacted; extraction order uncertain; hours per role per month not reliably attributable.
  Re-read visually before any public use.
- Allowed inference: the county's cost is dominated by one or a few very large requests, not by a
  steady stream of ordinary ones. That is e-discovery-scale review.

### CLM-013 — Lakota Local SD weighed moving records work from counsel to paralegals (switching signal)

- Source: Citizen Portal AI summary of Lakota Local (Ohio) Board of Education retreat, 2026-02-18,
  <https://citizenportal.ai/articles/7468072/Ohio/School-Districts/Lakota-Local/Board-discusses-publicrecords-workload-outside-counsel-and-possible-legalservice-changes>;
  accessed 2026-10-01; not retained.
- Establishes (as reported): outside counsel handles redaction and FERPA review; the board discussed
  "subcontracting higher-volume, lower-risk tasks to paralegals or junior staff at lower hourly
  rates"; staff asked to estimate savings. No decision.
- Limit: secondary, AI-written; Lakota is a large district (not small); the cheaper reviewer
  discussed sits inside a law firm.
- Allowed inference: buyers paying lawyer rates for redaction are asking whether cheaper reviewers
  can take the bulk. Partial evidence on the switching question; not evidence they would hire an
  outside non-lawyer.

### Checked, not usable

- NY Comptroller audit "City of Ithaca Records and Reports 2025M-114" (March 2026,
  <https://www.osc.ny.gov/files/local-government/audits/2026/pdf/ithaca-city-2025-114.pdf>): covers
  financial records and late audits, not FOIL. No bearing.
- Methacton agenda packet: not found on the district site or by search; figures remain secondary
  (CLM-003).

## What changes in the picture

- **Stronger:** the Los Alamos money was records-request work (CLM-001c). A small city wrote an RFP
  an individual could win, with hourly pricing and second-review scope (CLM-006a). The decision line
  (agency decides; reviewer prepares, redacts, and logs bases) is now in two primary documents.
- **Weaker:** both primary buyers bought to clear a backlog — Ithaca because of a platform migration
  (CLM-006a, CLM-012), Los Alamos because of one huge request (CLM-001d). Neither shows a
  recurring overflow buyer. After the backlog, Ithaca's clerk handles requests on software.
- **Reframe to test, not adopt:** the evidence fits a *backlog-clearance* offer (one-off, triggered
  by a mega-request, a migration, or a staffing gap) better than a standing overflow desk. That
  changes the go-to-market (watch for triggers; piggyback clauses) and the economics (lumpy
  projects, not a retainer). Recorded as hypothesis H-REFRAME-01; the candidate brief is not edited.

## Viewer's first test (field-only questions, coaching standard)

Unchanged from the disposition addendum, with one addition: ask the records officer whether outside
help was bought for a one-time backlog or for steady overflow, and what triggered it. Success
signal: two of three officers name a recurring need. Kill condition: all name one-off triggers and
say software covers the rest.

## Unknowns carried forward

Ithaca award and winner size; Ithaca and Los Alamos rates actually paid per hour; Methacton packet;
insurance limits in small-agency contracts; hours per request with AI review.
