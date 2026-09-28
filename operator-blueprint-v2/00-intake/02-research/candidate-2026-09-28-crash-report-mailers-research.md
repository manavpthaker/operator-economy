# Opportunity research brief: Crash-report review and compliant mailers for personal-injury firms

Template status: approved V2 Step 0.2 template; locked 2026-08-21.

Status: researching

Template version: `operator-blueprint-v2-step0.2`

Candidate ID: `candidate-2026-09-28-crash-report-mailers`

Candidate brief: `../01-candidates/candidate-2026-09-28-crash-report-mailers.md`

Candidate brief SHA-256: `7f84f03e8ef01030fc582e9d0c93d75af59b410db345708e5e16af0ed7fa2e4a`

Research cutoff: 2026-09-28

Research refresh date: not completed (research continues; proposed 2026-12-31 for state law and
pending bills; recheck the Georgia Supreme Court ruling in CLM-011 whenever it issues)

## Executive finding

- Opportunity: In an open state, AI-assisted review of the crash reports a personal-injury firm
  lawfully obtains, plus mailing of the firm's approved letter on the first lawful day.
- Evidence class: adjacent synthesis
- Provisional verdict: uncertain
- Main reason: The old way is real and documented in a primary court filing: a Washington firm
  bought 10,555 state-patrol reports at $9.50–$10.50 each and had an employee read them to find the
  not-at-fault driver before mailing (CLM-001); it later paid a $950,000 class settlement (CLM-002).
  The legal boundary is mappable (CLM-005, CLM-006, CLM-009, CLM-014). But the AI edge is thin:
  injury severity is already a coded per-person field on crash reports (CLM-010), the report fee is
  paid before any reading, and mail houses already run a daily pipeline (CLM-012). No firm has been
  seen paying an outside party for the reading step.
- Largest unresolved question: Does AI review change a firm's cost or letters-to-cases enough to
  pay an operator on top of report fees, when a coded-field filter or its mail house may already do
  most of it?
- Required public framing: The Swapp purchases, the statutes, the rules, and the court decisions are
  observed facts. The per-1,000 cost model is a qualified model. Any conversion rate, price, or AI
  lift is a hypothesis. Mail-house response rates are seller claims and may not be stated as fact.
  Nothing in the episode is legal advice.

## Buyer reality

- Buyer: Managing partner or marketing lead at a small or mid-size personal-injury firm in an open
  state.
- End customer or beneficiary: The firm. The drivers mailed did not ask for contact; they bear the
  cost of intrusion (CLM-003).
- Recurring problem: Buying reports, reading each for injury and fault, and mailing on time without
  breaking state law or bar rules.
- Consequence and frequency: Swapp bought more than 10,000 reports in about three years (CLM-001).
  Nationally, about 6.1 million police-reported crashes and 2.44 million people injured in 2023
  (CLM-017, context). Legal exposure is concrete: $950,000 settlement (CLM-002); $2,500 liquidated
  damages per violation under the federal driver-privacy law (CLM-004) and Florida's statute
  (CLM-014).
- Existing alternatives or budget: in-house staff reading bought reports (CLM-001); report brokers
  the firm subscribes to (CLM-004); mail houses (CLM-012, seller); per-lead sellers at $200–$400 per
  exclusive lead (CLM-020, seller, not willingness-to-pay evidence).
- Why now: AI reads scanned forms and narratives cheaply. At the same time access is closing: 9 of
  24 states researched are closed (CLM-005), and competitor-on-competitor litigation is active in
  Georgia (CLM-011).

## Evidence landscape

### Direct evidence

- CLM-001: *Wilcox v. Swapp*, E.D. Wash. No. 2:17-cv-275, Amended Complaint (ECF 69, filed
  2018-08-20). Quoting defendants' interrogatory answers: the firm bought 10,555 reports from the
  Washington State Patrol between 2013-09-01 and 2017-06-23; state-patrol records show purchases at
  "$9.50 or $10.50 per report" (¶4.26); a marketing employee searched by location and number of
  parties, marked the purpose as "marketing" (¶4.29), and "would review the reports with the goal of
  determining which of the parties involved in the accident was not at fault" before mailing, often
  "within a matter of days" of the crash (¶4.30). A state bar grievance followed (¶4.31–4.34). This
  is the exact job, done the old way, with observed unit cost. Limit: one firm; complaint is a
  plaintiff's document, though these paragraphs quote the defendant's own answers and state records.
- CLM-002: The firm agreed to pay $950,000 to settle; mailers reached more than 30,000 drivers
  (Spokesman-Review, 2020-01-30). Shows the legal cost of getting access wrong.
- CLM-004: *Garey v. James S. Farrin, P.C.*, 4th Cir. No. 21-1478 (2022-06-03). North Carolina
  injury lawyers "obtained car accident reports from North Carolina law enforcement agencies and
  private data brokers" and mailed the drivers (p. 4); the district court found they "subscribed to
  third-party services that aggregated crash records" (p. 6). Affirmed for the lawyers because
  nothing came from a DMV database (pp. 18–19). **Correction to the pool entry:** the court
  expressly did *not* decide whether an accident report is itself a DMV "motor vehicle record",
  noting a district court in the same circuit had held that it is (*Gaston v. LexisNexis*, W.D.N.C.
  2020), and ruled only because the argument was not preserved (p. 19). The federal privacy risk is
  open, not closed, even in the Fourth Circuit.
- CLM-011: Georgia Supreme Court heard argument (reported 2026-09-22) on reviving racketeering
  claims by rival lawyers against a firm accused of monitoring crashes, collecting victim data "from
  reports and other sources", and contacting victims directly. Allegation only; ruling pending.

### Adjacent business evidence

- CLM-012 (seller, context/component): Direct Marketing Inc. advertises daily accident-report mail
  for injury firms, "mail can be in production within hours" of a report's availability; no price,
  no stated injury or fault filter (pages dated 2026-06 and 2026-07). Mail Processing Associates
  lists law-firm mail at $0.70–$0.90 per letter in an envelope (CLM-018). These show the substitute
  exists; their response-rate claims (2–8%) are not usable.
- CLM-020 (seller, not usable as payment evidence): per-lead prices from a lead-marketing agency.

### Component feasibility evidence

- CLM-010: The national crash-data standard (MMUCC element P5) records a per-person injury code:
  K fatal, A suspected serious, B suspected minor, C possible, O no apparent injury. Much of the
  "is anyone hurt" filter is a coded field, not a reading task. What remains for AI: scanned forms,
  narratives and diagrams for fault, and exclusion flags (minors, fatalities, commercial vehicles).
- CLM-015: Texas sells regular copies at $6; full copies only to parties, insurers, and others
  listed in statute; everyone else gets a redacted copy; no bulk requests. Access mechanics, not
  AI, decide unit cost.

### Scaled relevance

- CLM-017: About 6.1 million police-reported crashes and 2.44 million injured in 2023 (NHTSA, via
  search result; publication not opened). Context only.

### Demand and competition

- Exact target queries: "crash report leads attorneys", "accident report direct mail law firm".
- Adjacent query or question families: victim-side "why do I get letters from lawyers after my
  accident" (CLM-013).
- Volume source, attempted measurement, and date: not measured this run.
- Other demand signals: CLM-001, CLM-004 (firms paying for reports); CLM-011 (active dispute).
- Independent signal count: two court records in two states (WA, NC) plus one pending case (GA);
  one seller family.
- Strongest existing coverage: mail-house marketing (CLM-012); victim-side law-firm blogs (CLM-013).
- Information gap: No coverage maps state access law, fee rules, and ethics as one operator's
  decision.

## Delivery boundary

This decides the business. A non-lawyer's reading, not legal advice.

1. **State gate first.** Of 24 states mapped on 2026-09-27: open 6 (Ohio, New Jersey, Indiana,
   Missouri, Nevada; Massachusetts low confidence), restricted 9, closed 9 including California and
   Pennsylvania (CLM-005). Re-verified this run: Maryland bars a non-lawyer from accessing a report
   "for the purpose of soliciting" for personal gain (CLM-006); Florida keeps reports confidential
   60 days and requires a sworn no-solicitation statement, $2,500 minimum damages (CLM-014); Texas
   redacts for non-parties and bans bulk requests (CLM-015); Ohio withholds only party *telephone
   numbers* for 30 days, not names and addresses (CLM-016 — narrower than the pool entry said).
2. **The firm is the requester of record.** Where access is limited to attorneys or sworn
   requesters, the operator must not buy reports itself. The operator only processes what the firm
   lawfully obtains, under a written vendor agreement. An operator buying reports and selling leads
   is the riskiest version (CLM-005, CLM-006).
3. **The federal driver-privacy law is unsettled.** Garey left open whether a crash report is a
   DMV record (CLM-004); Swapp settled a claim that it was (CLM-002). Any state where reports carry
   DMV-sourced data is exposed. A viewer needs a lawyer's opinion for their state before mailing.
4. **The lawyer owns the letter and the contact.** Ohio's rule, for example, requires "ADVERTISING
   MATERIAL" on the envelope and text, disclosure of how the lawyer learned of the person, no
   predetermined view of the merits, and a set "Understanding Your Rights" notice if sent within 30
   days; it bars solicitation of anyone whose "physical, emotional, or mental state" makes sound
   judgment unlikely (CLM-009). Other states add waits (Florida 30 days by rule; Indiana, Missouri,
   Nevada 30 days) and filing fees (Indiana) (CLM-005). The *Went For It* 30-day ban was upheld
   (CLM-003).
5. **Fee structure.** Lawyers may pay a non-recommending lead vendor a non-contingent fee (CLM-007).
   Paying per retained client or from case fees is an improper referral fee or fee split (CLM-008).
   The operator's fee must be flat or per report processed.
6. **What the operator may do:** receive reports from the firm, run AI and human review, apply the
   exclusion list, merge the firm's approved letter, hand off to a print vendor, keep the
   suppression list and log. **What it may not do:** contact anyone by phone, text, or in person;
   write or change the letter's legal content; evaluate anyone's claim; recommend the firm; take a
   per-case fee; obtain reports in its own name where the statute limits access.

## Proposed synthesis

- Parallel A and supported component: In-house staff reader (CLM-001) → job definition and old-way
  unit cost.
- Parallel B and supported component: Law-firm mail houses (CLM-012, CLM-018) → mailing pipeline
  and substitute price floor for printing.
- Parallel C and supported component: Lead-vendor fee rules (CLM-007, CLM-008) → lawful pricing
  unit.
- New combination: AI pre-read replaces the staff reader and enforces an exclusion list.
- Primary transfer risk: The reading step may be small money. The firm's largest cost is reports and
  its largest risk is legal, not reading time.
- Analogy map: not created this run.

## Proposed Operator Blueprint

- Offer: One firm, one open state, one deliverable: a weekly reviewed-and-mailed batch with an
  exclusion log.
- Buyer outcome: Staff hours removed; letters per signed case tracked by the firm.
- Delivery workflow: firm requests reports → secure transfer → AI pre-read (injury code, fault
  indicators, exclusion flags) → operator verifies every mailed and every excluded record → merge
  the firm's approved letter → mail on the first lawful day → suppression list and log.
- Technology and human stack: document AI for scanned forms; a print-and-mail API or mail house;
  a suppression database; the operator's human check.
- Required skills or credentials: direct-mail operations; data security; state-rule literacy; the
  discipline to refuse. The firm's lawyer supplies legal judgment.
- Go-to-market path: firms already mailing in an open state (visible to any driver who has been in
  a crash). Unverified.
- Pricing model: flat monthly or per report processed. Hypothesis.
- Defensibility: weak. A mail house or the firm's own staff can add the same filter.

## Modeled economics

Every number in this section is an internal Step 0 input until it is approved under
`content-os/facts.md` for public use.

| Input | Working value or range | Basis | Status | Sensitivity or caveat |
|---|---|---|---|---|
| Report cost | $6 (TX, 2026) to $9.50–$10.50 (WA, 2013–2017) per report | CLM-015, CLM-001 | observed | Varies by state; WA now closed |
| Mail cost | $0.70–$0.90 per letter | CLM-018 | observed seller price | One vendor; volume-dependent |
| Share of reports excluded by review | unknown | — | unknown | Drives mail savings |
| Staff reading time per report | unknown | CLM-001 shows the task, not the time | unknown | The main saving AI could make |
| Letters to signed case | unknown | seller claims not usable | unknown | Decides everything |
| Operator price | unknown | — | hypothesis | Must be non-contingent |

Qualified model (per 1,000 reports): reports cost $6,000–$10,500 before anyone reads them. Mailing
all 1,000 costs $700–$900. If review excluded 60% (an assumed input, not observed), mail savings
are $420–$540. `[$0.70–$0.90] x [600 excluded letters] = [$420–$540]`. The report fee is sunk, so
most of any value must come from removed staff reading time or a higher letters-to-cases rate —
both unknown. No capacity or contribution case is issued.

Disclosure: `Modeled scenario, not observed performance or an earnings forecast.`

## Narrative and audience hypothesis

- Operator protagonist: A direct-mail or legal-ops person deciding whether to build a review desk.
- Starting state: A firm staffer ordering 15 reports at a time and reading each for fault (CLM-001).
- Inciting change: AI can read the reports; states and courts are closing access.
- Stakes: $950,000 settlement (CLM-002); criminal statutes (CLM-006); harm to recipients (CLM-003).
- Causal mechanism: reports are cheap to buy; mailing everyone is cheap; reading is the labor.
- Build transformation: a review desk with a state gate and refusal list.
- Decisions and tradeoffs: which states; which crashes never get a letter; flat fee vs illegal
  per-case fee.
- End state and payoff: a synthetic batch on screen and the per-1,000 table; the viewer decides
  whether their state is open and whether the math works.
- Visual evidence classes: state map, court filing excerpts, coded injury field, compliant letter.
- Working audience promise: "Injury firms already pay to read crash reports. Where that is legal,
  what AI changes, and what not to build."
- Honest packaging territory: The crash-report mail business, from the inside of the rules.

## Risks and constraints

- Factual uncertainty: CLM-008 read from search snippets (source 403); CLM-005 state map is a
  prior-run compilation, partly secondary; New Jersey bills and New York's rule change not
  re-verified; mail-house filtering practices unknown.
- Analogy-transfer uncertainty: One firm (CLM-001) in a state that is now closed; whether an
  outside party is ever paid for the reading step is unobserved.
- Legal or regulatory boundary: see Delivery boundary. Unsettled federal driver-privacy exposure;
  state criminal statutes; runner/capper and barratry laws; referral-fee rules; bar filing rules.
- Permissions, privacy, or guest dependency: none for the episode; high sensitivity for the
  business (names, addresses, injury data).
- Platform or vendor dependency: state report portals and brokers; one policy change can close a
  state.
- **Ethical failure mode (serious).** The business is contacting people in the days after a crash
  who did not ask to be contacted. The Supreme Court record found 54% of Floridians saw such contact
  as a privacy violation and 27% of recipients thought less of the legal system; recipients
  described letters days after a funeral as "despicable and inexcusable" (CLM-003). AI makes it
  cheaper to find the most seriously hurt — exactly the people whose state may impair judgment
  (CLM-009). Failure looks like: letters to families after fatal crashes; letters to minors;
  multi-piece sequences to one person (vendors recommend 2–3 pieces, CLM-012); mailing before the
  lawful day; ignoring opt-outs; buying reports under a false purpose. Minimum refusal list: no
  fatal-crash (K) households, no minors, one letter per person, honor every opt-out, no mail before
  the lawful date, no report obtained in the operator's name where the statute limits access. An
  episode that teaches the business must teach the refusal list as part of it.
- Claims that must not be made: that this is legal in "most" states; that the federal privacy
  question is settled; any response or conversion rate; any earnings; that AI "finds the best
  cases"; that the operator may advise on legal compliance.

## Thirty-day validation plan (the viewer's first test)

Field-only questions below are the viewer's test, not an Operator Economy condition
(owner decision 2026-09-28).

1. Desk, week 1: Pick one open state. Read its access statute, bar solicitation rule, and waiting
   period; confirm the firm can request reports in bulk and at what price. Get a lawyer's written
   view on the federal driver-privacy exposure for that state.
2. Desk, week 2: Build the review on 50 synthetic or firm-provided reports: measure minutes per
   report by hand vs with AI plus human check, and the share excluded by the coded injury field
   alone vs by AI.
3. Field, weeks 3–4: Show three firms that already mail in that state the per-1,000 table and the
   exclusion log; offer a flat-fee 30-day run.

Success signal: AI review saves at least half the hand-reading time beyond what the coded field
alone does, and one firm pays a flat fee for a 30-day run.

Kill or redesign condition: the coded field does most of the filtering (AI adds little); the
firm's mail house already filters; no firm will pay a non-contingent fee; or the lawyer's view is
that the state's reports carry DMV-sourced data.

## Source registry

| Claim ID | Claim and status | Source and URL/path | Exact locator | Published / accessed | Snapshot or local path / SHA-256 | Source type / confidence | Relationship | Refresh by | Caveat |
|---|---|---|---|---|---|---|---|---|---|
| CLM-001 | Firm bought 10,555 WSP reports at $9.50/$10.50; staffer reviewed for not-at-fault party; mailed within days; verified as quoted | *Wilcox v. Swapp*, E.D. Wash. 2:17-cv-275, Amended Complaint ECF 69, <https://angeion-public.s3.amazonaws.com/www.SwappSettlement.com/docs/Amended+Complaint.pdf> | ¶¶4.26–4.34 (pp. 13–17) | 2018-08-20 / 2026-09-28 | fetched PDF not retained in repo; SHA-256 `90f8a9ef9b176dd5af4b6ca40566015a86cb8eb11894d0fee47a1fcfc8991993` | primary court filing; high for quoted admissions | direct | n/a (historical) | Plaintiff's pleading; WA now closed |
| CLM-002 | $950,000 settlement; 30,000+ drivers mailed; verified as reported | Spokesman-Review, <https://www.spokesman.com/stories/2020/jan/30/craig-swapp-law-firm-agrees-to-pay-nearly-1-millio/> | article body | 2020-01-30 / 2026-09-28 | not retained | secondary news; medium | direct | n/a | Settlement, not a ruling |
| CLM-003 | 30-day ban upheld; Bar study: 54% saw accident contact as privacy violation; 27% of recipients thought less of legal system; recipient anecdotes; verified | *Florida Bar v. Went For It*, 515 U.S. 618, <https://tile.loc.gov/storage-services/service/ll/usrep/usrep515/usrep515618/usrep515618.pdf> | Opinion of the Court, Bar study discussion (PDF p. 10; U.S. page not confirmed) | 1995 / 2026-09-28 | not retained; SHA-256 `5f658082bb79766898579783e87c04773f93559abfc4458a859babb7fe33e94e` | primary; high | context only (ethics, law) | n/a | 1987 survey data |
| CLM-004 | NC lawyers got reports from agencies and data brokers (some by subscription) and mailed drivers; DPPA claim failed because no DMV database; court did not decide whether a report is a motor vehicle record; *Gaston* held it is; verified | *Garey v. James S. Farrin, P.C.*, 4th Cir. 21-1478, <https://www.courthousenews.com/wp-content/uploads/2022/06/accident-report-rulings.pdf> (Justia copy HTTP 403) | pp. 4–6, 18–19 | 2022-06-03 / 2026-09-28 | not retained; SHA-256 `a50e6c670f622995699fb9b9b9335f85c6c8c25669a1572a6c31174549bedd72` | primary; high | direct | 2026-12-31 | Brokers not named; Fourth Circuit only |
| CLM-005 | 24-state access and solicitation map: 6 open, 9 restricted, 9 closed; qualified | `automation/candidate-discovery/runs/2026-09-27.md` | "Result" and "By state" tables | 2026-09-27 / 2026-09-28 | repository path | compiled from statutes and rules, some secondary; medium | component | 2026-12-31 | 26 states unmapped; MA low confidence; not all rows re-verified this run |
| CLM-006 | Maryland: non-lawyer may not, for personal gain, access a report to solicit; verified | Md. Code, Bus. Occ. & Prof. §10-604, <https://mgaleg.maryland.gov/mgawebsite/Laws/StatuteText?article=gbo&section=10-604&enactments=false> | §10-604(b)(2) | current / 2026-09-28 | not retained | primary; high | component (boundary) | 2027-09-28 | Penalty section not read |
| CLM-007 | Lawyers may pay a lead generator that does not recommend them, with payment consistent with Rules 1.5(e) and 5.4; verified (NC version of Model Rule) | NC State Bar, Rule 7.2, <https://www.ncbar.gov/for-lawyers/ethics/rules-of-professional-conduct/rule-72-rule-72-communications-concerning-a-lawyers-services-specific-rules/> | Rule 7.2(b); Comment [5] | current / 2026-09-28 | not retained | primary; high | component (fee rule) | 2027-09-28 | ABA Model Rule pages returned HTTP 403 |
| CLM-008 | NJ: lawyers may pay per lead but not per client retained; marketing "leads" may be disguised referrals; qualified | NJ ACPE Op. 741 (2021), citing CAA Op. 43 (2011), <https://law.justia.com/cases/new-jersey/advisory-committee-on-professional-ethics/2021/acp741-1.html> | search-result summary only | 2021 / 2026-09-28 | not retained; page HTTP 403 | primary via snippet; medium | component (fee rule) | 2027-09-28 | Full opinion not read |
| CLM-009 | Ohio Rule 7.3: no solicitation where state of mind impairs judgment, or after opt-out, or with harassment; "ADVERTISING MATERIAL"; disclose how identity learned; "Understanding Your Rights" notice within 30 days; verified | Ohio Prof. Cond. R. 7.3, <https://www.ohiobar.org/globalassets/practice-library/pdfs/prof.cond.r.7.3.pdf> | 7.3(b)(1)–(3), (c)(1)–(3), (e) | current / 2026-09-28 | not retained; SHA-256 `3484a9b48544b9654554dcbd680061d984d38208edff664083b4e172872c4d91` | primary; high | component (boundary) | 2027-09-28 | Ohio only |
| CLM-010 | Crash reports carry a per-person KABCO injury code; verified | MMUCC training, element P5, <https://www.mmucctraining.us/Element/P5> | P5 attributes | current / 2026-09-28 | not retained | primary (standard); high | component | 2027-09-28 | State adoption varies |
| CLM-011 | Georgia Supreme Court argument on reviving racketeering claims over crash-victim solicitation; qualified (allegations) | Courthouse News, <https://courthousenews.com/georgia-supreme-court-intervenes-in-lawyers-solicitation-fight/> | article body | 2026-09-22 / 2026-09-28 | not retained | secondary news; medium | context only | on ruling | Allegations; ruling pending |
| CLM-012 | Mail houses advertise daily accident-report mail to injury firms; no price or injury filter stated; seller | Direct Marketing Inc., <https://directmk.com/personal-injury-attorney-direct-mail-how-to-reach-accident-victims-before-the-insurance-adjuster-do/>, <https://directmk.com/every-day-you-wait-another-attorney-gets-the-case/> | page bodies | 2026-07-07, 2026-06-09 / 2026-09-28 | not retained | self-published; low | adjacent (substitute) | 2026-12-31 | Seller; response rates not usable |
| CLM-013 | Victim-side questions about unsolicited lawyer letters exist; context | Mann Law blog, <https://www.mannlawllc.com/blog/why-do-i-receive-mail-from-lawyers-after-my-accident/> (search result) | title | — / 2026-09-28 | not retained | self-published; low | context only | n/a | Title only |
| CLM-014 | Florida: reports confidential 60 days; sworn no-solicitation statement; $2,500 minimum damages; verified | Fla. Stat. §316.066, <https://www.flsenate.gov/Laws/Statutes/2025/316.066> | (2)(a), (2)(b), (2)(d), (3)(e) | 2025 / 2026-09-28 | not retained | primary; high | component (boundary) | 2027-09-28 | — |
| CLM-015 | Texas: $6 regular copy; full copy to listed parties; redacted to others; no bulk requests; verified | TxDOT, <https://www.txdot.gov/data-maps/crash-reports-records.html> | page body | current / 2026-09-28 | not retained | primary; high | component | 2027-09-28 | Criminal 31-day mail wait not re-read this run |
| CLM-016 | Ohio withholds party telephone numbers for 30 days only; verified | ORC 149.43(A)(1)(oo), <https://codes.ohio.gov/ohio-revised-code/section-149.43> | (A)(1)(oo) | current / 2026-09-28 | not retained | primary; high | component | 2027-09-28 | Corrects pool's "contact details" |
| CLM-017 | ~6.1M police-reported crashes, 2.44M injured, 2023; qualified | NHTSA, Overview of Motor Vehicle Traffic Crashes in 2023 (via search result) | summary | 2025 / 2026-09-28 | not retained | primary via snippet; medium | context only | 2027-06-30 | Publication not opened |
| CLM-018 | Law-firm letters $0.70–$0.90 per piece all-in; seller | Mail Processing Associates, <https://www.mailpro.org/post/direct-mail-advertising-for-law-firms/> | pricing section | updated 2026-08-03 / 2026-09-28 | not retained | self-published; medium for own price | component | 2026-12-31 | One vendor |
| CLM-019 | Lawyers who obtained DMV names and addresses to solicit were not within the litigation exception; verified as quoted | *Maracich v. Spears*, 570 U.S. 48 (2013), quoted in CLM-004 p. 18 | via CLM-004 | 2013 / 2026-09-28 | see CLM-004 | primary; high | context only | n/a | Justia page HTTP 403; "34,000" figure in pool not re-verified |
| CLM-020 | Car-accident leads $200–$400 exclusive, $35–$90 shared crash-data; not usable as payment evidence | Mass Tort Marketing Agency, <https://www.masstortmarketingagency.com/blogs/motor-vehicle-accident-leads-guide> (pool record) | — | — / not re-opened | not retained | seller; low | context only | n/a | Seller price page |
| CLM-021 | NC news on shrinking report access after litigation; not usable this run | Reflector, <https://www.reflector.com/news/local/information-on-crashes-limited-as-access-to-reports-shrinks/article_9ca5eb2f-a3af-5dc5-b156-9d25e9a1eac0.html> | — | — / 2026-09-28 | HTTP 429 on fetch | secondary; — | context only | n/a | Access limit recorded; not replaced |

## Evidence pass and adversarial pass

Both run by the same agent; not independent.

- Evidence pass (2026-09-28): re-verified Garey, Went For It, Maryland, Florida, Texas, Ohio rule and
  statute, NC Rule 7.2 from primary text. Two corrections to the pool: Garey left the report-as-DMV-
  record question open; Ohio withholds phone numbers only. New primary evidence: the Swapp filing
  (CLM-001), which is the first buyer-paid record for the exact job.
- Adversarial pass: see disposition record.

## Unresolved questions

- AI edge: how much filtering does the coded injury field already do, and do mail houses already
  filter? Desk: read two mail houses' or brokers' data specs; sample an open state's report form.
- Open-state mechanics: can a firm request reports in bulk in Ohio, New Jersey, Indiana, Missouri,
  Nevada, and at what price? Desk: each state's portal terms.
- Federal driver-privacy exposure outside the Fourth Circuit: any post-2022 rulings? Desk: case
  search.
- Letters-to-cases rate and staff reading time: field-only; the viewer's first test.
- Whether any firm pays an outside party for the reading step: field-only; the viewer's first test.
