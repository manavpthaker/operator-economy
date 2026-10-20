# Owner decision 2026-10-20: idealab.ai is a source for the scout and the research bench

Status: approved owner decision. Recorded 2026-10-20 from the owner's instruction in chat.

Decided by: Manav Thaker (owner)

Owner's words: "I just found idealab.ai. We should add this to the operator economy deep research.
Might as well look there and do research based on that data and those assumptions."

Scope: `automation/prompts/oe-candidate-scout.md`, `automation/prompts/oe-weekly-research.md`, and
the helper `automation/tools/idealab.py`. This decision does **not** edit any locked Step 0.2 file
or the Step 0.3 amendment, and does not change the five tests, hard gates, scoring, evidence
standards, the calibration zone, or owner promotion.

## What idealab.ai is (checked 2026-10-20)

A free database from Idealab.AI, Inc. (Bill Gross) of about 1.21 million business ideas, written by
language models (briefs name `gpt-5.6-sol`) from 17.6 million sources read and 29.2 million
signals extracted, each sorted as an opportunity, enabler, or shift (`/api/intake/metrics`,
2026-10-20). Visitors get 50 searches and 10 full briefs a day without an account. A brief carries
a pitch, the buyer it imagines, why now, start capital, revenue at success, team size, nine scores
of its own (clarity, whitespace, differentiation, automability, severity, why-now strength,
protectability, market, conviction), a model's web check of the field (`crowded`, `contested`,
`license_play`), the source publishers and evidence types, a named competitor list with URLs, and
the risks that could kill it.

## What its ideas assume, and why that limits their use here

The 2026-10-20 source pass (`automation/candidate-discovery/runs/2026-10-20.md`) opened 10 briefs
and ran 30 searches:

- **A venture, not an operator.** Every brief opened assumed a 2–5 or 6–20 person team, $75,000 to
  $180,000 to start, and $12 million to $30 million a year at success. A solo-founder filter
  returned 1 idea for most queries. The Operator Economy assumes one accountable person selling an
  outcome.
- **Software first.** Most ideas are platforms, engines, or layers sold to institutions (employers,
  districts, processors), even when the problem is a buyer's chore.
- **Thin, often foreign evidence.** Briefs cite 1 to 4 sources. FairBill (a US medical-bill idea)
  rested on Slovak news plus one CFPB complaint; the construction photo-ledger idea on one Japanese
  news story. Ideas are rewritten into US framings their sources do not establish.
- **Its own field check is often right.** Most opened briefs were marked `contested` or `crowded`,
  and the substitutes they named held up when checked.

## Decision

1. **Ideas are search prompts only.** An idealab idea is treated like the scout's own knowledge: it
   may name a buyer and a problem to go and look for, never a lead by itself. It becomes a lead only
   when a logged buyer-side observation supports it, under the five tests unchanged.
2. **Translate before screening.** Restate each idea in the Operator Economy shape (one operator,
   AI and agents, the buyer who pays, a share of value or fixed fee) and record what idealab
   assumed beside it.
3. **Never evidence.** idealab's scores, market sizes, revenue and capital figures, and why-now text
   are never evidence, problem-value signals, or unit economics. Its sources may be followed to the
   original: a consumer complaint or forum post read at its own URL can be a buyer-side observation;
   the brief citing it cannot.
4. **Substitute checklist.** A brief's competitor list is a starting list for test 4 and the bench's
   strongest-existing-coverage check. Each competitor is verified and priced on its own page before
   it is cited.
5. **Budget.** The scout may run at most 5 idealab searches and open 3 briefs a run, and may start at
   most one new lead a run from an idealab prompt. The bench may run at most 3 searches and open 2
   briefs a run for the candidate it is researching. Both use `automation/tools/idealab.py`, which
   keeps one visitor cookie so the daily limits are respected. No account is created, nothing is
   saved or posted on idealab, and no new visitor session is made to get around a limit. idealab is
   free; this decision adds no spend.

## Revisit

2026-11-03, after two scout runs and one bench run: whether any idealab prompt reached the
shortlist, and whether the per-run limits should move.
