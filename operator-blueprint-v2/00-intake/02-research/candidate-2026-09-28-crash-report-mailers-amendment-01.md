# Step 0 evidence amendment 01: does a coded field or an existing vendor already do the filtering?

Status: recorded

Template version: `operator-blueprint-v2-step0.2` (amendment record; the reviewed candidate brief and research brief are unchanged, so their hashes still hold)

Candidate ID: `candidate-2026-09-28-crash-report-mailers`

Research brief amended (by reference only): `candidate-2026-09-28-crash-report-mailers-research.md` / `f72209ac096dca1bc3b8b9b4c2feec91c9107333fe8cf861799b662555bbd408`

Disposition: `../03-validation/candidate-2026-09-28-crash-report-mailers-disposition.md` / `d2f159c29f5f8fd887eac346b07f44f0628f6876ca254628b3afe2b12c772f7e` (continue research; desk re-entry item 1 required)

Governing decision: `../OWNER-DECISION-2026-09-28-COACHING-STANDARD.md` / `95c781cba2a8ad5d8f76dda597329e0f84b4732226f9c8886a9520f0af2cd686`

Recorded: 2026-10-05

Recorded by: the Step 0 research bench (Monday run)

## Why this record exists

The disposition made desk item 1 required: show how much filtering one open state's coded injury
and fault fields already do, and whether named vendors already filter by injury or fault. It said:
"If they already do, redesign or park." This run answered item 1 for Ohio and, in part, Missouri.
Items 2 and 3 were not worked: the item 1 result decides the candidate without them.

## Re-entry status

| Item | Required | Found | Status |
|---|---|---|---|
| 1 | Coded-field filtering on one open state's form; whether vendors already filter by injury or fault | Ohio form codes both injury (per person) and the at-fault unit (CLM-022). An Ohio vendor sells crash-report leads to law firms scored by injury severity and fault within hours (CLM-023). Missouri's public portal filters injury crashes by severity for free (CLM-024) | **met — answer is "they already do"** |
| 2 | Bulk-access terms and prices for three open states | Ohio retrieval is free but needs report number, date, and county (CLM-025, secondary). Not pursued further | not worked |
| 3 | Post-2022 federal ruling on reports as DMV records; full NJ opinion | not pursued | not worked |

## New claims

### Fact (primary, opened this run)

- **CLM-022.** Ohio's crash report (OH-1) records, on page 1, a field "UNIT IN ERROR": "Enter the
  unit number of the motorist/non-motorist which had the most causative bearing on the crash" ("99"
  if unknown). Each person on the unit pages carries a five-level injury code (1 fatal, 2 suspected
  serious, 3 suspected minor, 4 possible, 5 no apparent injury), and each unit carries the officer's
  "contributing circumstances" code. Source: Ohio Department of Public Safety, Ohio Crash Report
  Procedure Manual and OH-1 form set (HSY 7001 / HSY 8304 sections), <https://dam.assets.ohio.gov/image/upload/publicsafety.ohio.gov/HSY7010.pdf>,
  OH-1 – 7 "Unit in Error" (manual p. 5), OH-1 – 23 "Crash Severity" (p. 8), OH-1U – 35
  "Contributing Circumstances" (p. 26), injury code key on form p. 1. Accessed 2026-10-05; PDF
  SHA-256 `f6767b6dbec7b8219f1beddc1265bf0554c45305b54d7e925dd679193e9e5403` (not retained in repo).
  Limit: the officer's judgment, not a legal finding of fault; electronic submissions can still
  arrive to a firm as a PDF image.
- **CLM-024.** Missouri State Highway Patrol's public crash search lists injury and fatal crashes it
  investigated for one year, searchable by county, date, and **injury type** (minor, moderate,
  serious, fatal), showing each person's age, city, and injury severity. Source: MSHP, <https://www.mshp.dps.mo.gov/HP68/search.jsp>,
  search form and result columns. Accessed 2026-10-05. Limit: MSHP-investigated crashes only;
  preliminary and unofficial; no fault field shown in the list view.

### Observed model (seller, opened this run)

- **CLM-023.** OhioCrashLeads (<https://ohiocrashleads.com/>, © 2026, accessed 2026-10-05) sells
  Ohio crash-report data from all 88 counties to licensed Ohio chiropractors and attorneys:
  "Name, age, accident type, fault status, and location"; for law firms, daily enriched reports with
  "Lead quality scoring: injury severity, fault status, and more", produced within "hours of
  publication". No price shown. Seller copy: proves the product is offered, not that anyone pays or
  what it costs. Its compliance claims were not tested and no inference is drawn about them.

### Reported (secondary)

- **CLM-025.** Ohio's state retrieval system gives unofficial reports free "to anyone" but needs the
  report number, date, and county (Rinehardt Law Firm blog, dated 2026-01-27,
  <https://rinehardtlawfirm.com/how-to-obtain-free-columbus-crash-reports-through-ohios-odps-system/>,
  accessed 2026-10-05). Law-firm marketing; not checked against the portal.

### What this changes

- The candidate's AI step was: read each report for injury and fault. In Ohio both are coded
  fields filled by the officer. Picking "injured, not the unit in error" is a column filter once a
  report is digitised, and a vendor already sells that filter, scored and enriched, within hours.
  In Missouri the injury filter is a free public search box.
- What AI could still add is narrow: reading scanned PDFs into fields, and the narrative where the
  unit in error is "99". That is data entry, which a vendor already does at state scale.
- The kill or redesign condition in the research brief's validation plan ("the coded field does
  most of the filtering; the firm's mail house already filters") is met on desk evidence for Ohio.
- It also fails the pool's AI-change test as the offer is framed: AI does not make this business
  newly possible or newly cheap; a non-AI data vendor already ships it.

### Unknown

- Whether all five open states code fault the way Ohio does (NJ, IN, NV not opened).
- OhioCrashLeads' price, volume, and buyers.
- Whether any firm pays an outside party for the exclusion and compliance log alone.

## Boundary

No score, hard gate, analogy map, Canvas, editorial-potential artifact, queue row, or episode number
is created. Nothing here is legal advice.
