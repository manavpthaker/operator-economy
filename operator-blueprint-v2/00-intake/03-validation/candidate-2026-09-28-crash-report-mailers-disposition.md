# Step 0 early disposition record: Crash-report review and compliant mailers for personal-injury firms

Template status: approved V2 Step 0.2 template; locked 2026-08-21.

Template version: `operator-blueprint-v2-step0.2`

Candidate ID: `candidate-2026-09-28-crash-report-mailers`

Discovery lead: `DISC-2026-09-27-009` (owner-admitted 2026-09-28)

Decision date: 2026-09-28

Decision stage: research

Decision: **continue research**

## Reviewed artifacts

- Candidate brief: `../01-candidates/candidate-2026-09-28-crash-report-mailers.md` / `7f84f03e8ef01030fc582e9d0c93d75af59b410db345708e5e16af0ed7fa2e4a`
- Research brief: `../02-research/candidate-2026-09-28-crash-report-mailers-research.md` / `f72209ac096dca1bc3b8b9b4c2feec91c9107333fe8cf861799b662555bbd408`
- Preliminary analogy review: not created. The AI edge and the economics have no evidence yet; a
  scored map would invent them.

## Reason for stopping

- Failed or incomplete requirement: offer/delivery (is there an AI edge?) and economics/capacity.
- Plain-English finding: The buyer problem and old-way spend are proven by a primary court filing:
  a firm paid $9.50–$10.50 per report for 10,555 reports and paid a staffer to read them for fault.
  The legal line is mappable and strict. What is not shown is that AI changes anything a firm would
  pay for: injury severity is already a coded field, the report fee is paid before reading, and mail
  houses already run the pipeline. Two desk questions can settle this before any field test.
- Claims or assumptions that remain unusable:
  - Any response rate, conversion rate, or cases per 1,000 letters (seller claims only).
  - Any operator price or earnings.
  - That the federal driver-privacy question is settled (Garey left it open).
  - That mail is legal in "most" states.
  - The NJ referral-fee opinion's exact wording (source blocked; snippet only).
  - The Maracich "34,000" figure (not re-verified).
  - Any claim that AI "finds the best cases".

## Adversarial editorial finding

Performed by the same agent as the evidence pass; not an independent review.

- Strongest alternative explanation: This is a mail-house business with a filter. The injury code
  is already on the report, a firm's staffer or its mail house can filter on it for free, and the
  money is in report access and legal risk, not reading. The "AI" may be a spreadsheet filter.
- Strongest causal weakness: The only firm observed paying for the job (Swapp) did it in a state
  that is now closed and paid $950,000 to settle. The best evidence for the old way is also evidence
  of its legal cost.
- Hidden labor: per-state legal review; lawyer's opinion on the driver-privacy law; suppression
  list; human check of every AI mark; firm-side call handling the operator may not touch.
- Recourse and liability: statutory damages per person ($2,500 federal and Florida); criminal
  statutes (Maryland, and the waits in Texas and Michigan per the state map); the firm's bar
  licence; the operator's exposure as the party that processed the data.
- Ethical failure mode: The business contacts people in the days after a crash who did not ask.
  AI makes it cheaper to find the most badly hurt — the people bar rules protect from solicitation
  when their state impairs judgment. The Supreme Court record shows real recipients' anger. An
  episode that teaches this without the refusal list (no fatal-crash households, no minors, one
  letter, honor opt-outs, nothing before the lawful day, no report in the operator's name where
  access is limited) would teach harm. If the refusal list makes the economics fail, that is the
  answer, not a reason to drop the list.
- If the most attractive claim (AI scoring) is removed: an episode still stands on a verified
  paid job, a state map, and a clear legal line — but it becomes an explainer of an existing,
  contested trade, not an AI-enabled business. That may fail the pool's AI-change test.
- Duplication: none found in the repository.

## Re-entry

Re-entry allowed: yes

Re-entry condition (desk work; any two advance the candidate to an analogy map and scorecard, and
item 1 is required):

1. Desk (required): evidence of how much filtering the coded injury field and fault fields already
   do on one open state's report form, and whether named mail houses or brokers already filter by
   injury or fault. If they already do, redesign or park.
2. Desk: bulk-access terms and prices for at least three open states' report portals, confirming a
   firm can lawfully request reports in volume.
3. Desk: any post-2022 federal ruling on whether crash reports are DMV records, and the full NJ
   referral-fee opinion.

Field-only questions (staff minutes per report, letters per signed case, whether a firm pays an
outside reviewer) are the viewer's first test in the research brief's validation plan. They are not
an Operator Economy condition.

Destination: remain in research.

Suggested evidence refresh: 2026-12-31 for state law and pending bills; on issue of the Georgia
Supreme Court ruling.

## Boundary

Editorial development authorized: no

Episode number: unassigned

This record is not a promotion record and cannot create an active queue row. If the candidate
re-enters, preserve this disposition and issue a new reviewed package rather than overwriting the
decision history.

## Addendum 2026-10-05: desk item 1 answered; parked (Monday bench)

Evidence: `../02-research/candidate-2026-09-28-crash-report-mailers-amendment-01.md` / `fe448c9c07c00f2607cacba52a8326d251cb1f2737d0ae7158731dcc9dd920a7`

Decision: **parked**. Decision stage: research. This replaces "continue research" above; the
original record is preserved.

- Item 1 (required) is answered, and the answer is the one this record said leads to redesign or
  park. Ohio's report codes both the person's injury level and the "unit in error" (the driver the
  officer judged most at fault) (CLM-022). An Ohio vendor already sells crash data to law firms,
  scored by injury severity and fault, within hours (CLM-023, seller). Missouri's state patrol lets
  anyone filter injury crashes by severity for free (CLM-024).
- The AI step in the offer (reading reports for injury and fault) is a column filter in Ohio and
  already a product. What is left for AI is turning scanned PDFs into fields, which a vendor does at
  state scale. The offer fails the pool's AI-change test as framed.
- Items 2 and 3 were not worked; neither could change this result.
- No redesign was adopted. The only plausible one (a compliance and exclusion-log service for
  firms that mail) has no evidence that anyone pays for it, and would be a different candidate.
- Not archived: the buyer-paid old way (CLM-001), the legal map, and the ethics finding remain
  sound and reusable.

Unblock condition (desk; either one reopens research, not validation):

1. An open state where injury and fault are **not** coded fields on the report a firm receives, and
   no vendor already sells that state's reports filtered by injury or fault.
2. Primary or independent evidence that law firms pay an outside party for the compliance layer
   alone (exclusion list, lawful-day timing, suppression log), separate from data and mail.

Field-only questions stay the viewer's first test and are not unblock conditions.

Review trigger: either condition met, or 2026-12-31 (state law and pending bills), or the Georgia
Supreme Court ruling in CLM-011.

Destination: parked register
(`../04-queue/parked/candidate-2026-09-28-crash-report-mailers.md`).
