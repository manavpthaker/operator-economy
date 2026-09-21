# Operator Economy candidate scout

Run this workflow every Wednesday and Sunday at 17:00 America/New_York in
`/Users/brownmanbrain/GitHub/operator-economy`.

Your objective is to maintain a small, current, evidence-led pool of potential Operator Economy
subjects before formal Step 0 intake. Search what people are actively asking and discussing, but
also search current markets, operating changes, buyer problems, spending and adoption signals, new
capabilities, and underserved workflows. Translate strong signals into possible operator businesses,
not merely content topics or AI trends.

The first line of the run output must be:

`Run date: YYYY-MM-DD ET | Scout: Wednesday / Sunday | Pool: <shortlisted count> shortlisted`

## Authority and boundary

Read these before acting:

1. `AGENTS.md` and `../content-os/CLAUDE.md`.
2. `../content-os/strategy/portfolio-charter.md` and
   `../content-os/strategy/editorial-system.md` for audience, thesis, and desk boundaries.
3. `automation/candidate-discovery/README.md` and `POOL.md` for the discovery contract and current
   state.
4. `operator-blueprint-v2/00-intake/README.md`, `AUTHORITY-MAP.md`,
   `STEP0.2-APPROVAL.md`, and `STEP0.3-CHANGE-PROPOSAL.md` only to understand what the scout must not
   pre-empt.

This is pre-intake discovery. Never create or edit Step 0 artifacts, readiness scores, promotion
records, the canonical queue, episode numbers, scripts, narration, production, or release state.

## Preflight and deduplication

1. Resolve the current Eastern date. Inspect the current branch, upstream divergence, and `git
   status`. Preserve unrelated dirty work and stop on an overlapping edit you cannot isolate.
2. Read the current pool and recent scout runs. Continue useful unfinished screening before adding
   more leads.
3. Build a semantic deduplication map across:
   - every current Step 0 candidate, research package, validation, disposition, and promotion;
   - `operator-blueprint-v2/00-intake/04-queue/QUEUE.md`;
   - every V2 episode workspace and active production workspace;
   - parked, held, rejected, archived, superseded, and historical topic material;
   - `research/`, `topics/`, and `studio/originate/`; and
   - the existing discovery pool.
4. Compare buyer, costly problem, offer, outcome, mechanism, evidence base, episode claim, and
   unresolved question. A renamed duplicate is still a duplicate.

## Discovery lane 1: conversation radar

Search current public conversation and record direct links, exact observed language, dates, and
access limits.

- **Google Trends:** compare useful windows such as 7 days, 90 days, and 12 months; inspect rising
  and related queries and regional differences. Treat the index as relative direction, never exact
  monthly search volume.
- **Reddit:** inspect recent posts and substantive comments in broad and domain-specific communities.
  Look for repeated questions, frustrations, failed attempts, workarounds, purchase decisions,
  disputed assumptions, and language people use naturally. Upvotes alone are not demand evidence.
- **Google search:** inspect autocomplete, People Also Ask, result recency, and repeated query
  formulations. Do not infer volume from result counts.
- **YouTube:** inspect autocomplete, recent relevant videos, view velocity when visible, packaging,
  comment questions, and whether strong coverage already resolves the topic.
- **Other relevant communities:** Hacker News, Indie Hackers, specialist forums, public professional
  communities, and domain-specific discussion surfaces. Use only what is publicly accessible and
  attributable.

Do not force every surface into every run. Choose the surfaces relevant to the observed question and
record unavailable or blocked access honestly.

## Discovery lane 2: market and operating signals

Search current primary or otherwise credible sources for:

- product and platform releases, pricing changes, new capabilities, and deprecations;
- regulatory, compliance, labor, procurement, or industry-rule changes;
- acquisitions, funding, partnerships, vendor adoption, and buyer spending signals;
- job postings, service requests, operational complaints, workarounds, and recurring manual labor;
- margin pressure, customer-acquisition shifts, ownership or data-control changes, and platform
  dependence; and
- workflows where a deliberately small accountable operator may now deliver an observable result.

Seller claims, directories, social chatter, search movement, and press coverage have different
evidentiary weight. Preserve those differences.

## Translate signals into leads

For every lead worth retaining, capture the complete contract in
`automation/candidate-discovery/README.md`, including:

- the exact question, tension, or change;
- who appears to care and what decision they face;
- buyer and costly problem;
- potential offer and observable outcome;
- delivery-mechanism hypothesis;
- why now;
- strongest existing answer and what it appears to miss;
- possible Operator Economy point of view;
- strongest invalidating question;
- evidence still needed; and
- expiry or recheck date.

The Operator Economy angle must be earned. Test whether the useful interpretation concerns hidden
labor, cost, dependence, accountability, customer ownership, data, decision rights, margin,
portability, recourse, or a realistic small-operator advantage. Do not manufacture contrarianism.

## Qualification and disposition

To become `shortlisted`, a lead must have:

1. recurrence across at least two independent conversation surfaces, or one material operating
   change plus one independent audience/question signal;
2. clear audience and thesis fit;
3. a meaningful unresolved tension or coverage gap;
4. a plausible buyer, costly problem, observable outcome, and delivery mechanism to investigate;
5. a path to honest, showable evidence that does not depend on a guest; and
6. enough accessible evidence for the Monday bench to decide whether formal Step 0 research is
   warranted.

Reject generic, duplicative, evidence-free, guest-dependent, non-showable, hype-led, or trend-only
ideas early. Hold a plausible lead when one named missing condition could change the decision, and
record its exact reopening condition. A source-access failure is a limitation, not a reason to claim
no interest or demand.

Do not assign a numeric score. Order shortlisted leads by editorial priority and state the decisive
reason in plain language. Keep no more than five shortlisted leads and add no more than three
materially new leads in one run.

## Persistence and git safety

1. Write the full observed-source ledger, screening, deduplication, and dispositions to
   `automation/candidate-discovery/runs/YYYY-MM-DD.md`. Append a numbered rerun section rather than
   overwriting a same-date record.
2. Update `automation/candidate-discovery/POOL.md` with the current `new`, `shortlisted`, `held`,
   `rejected`, and previously `admitted` states. Preserve historical rejection evidence in the run
   record.
3. The scout may never mark a lead `admitted`; only the Monday bench may do so after it creates a
   formal candidate artifact.
4. Commit only the scout prompt, pool, and this run's explicit discovery records. Never use
   `git add -A`, reset, clean, delete, amend someone else's commit, or include unrelated dirty work.
5. Push only when the scoped commit can be pushed without carrying unrelated unpublished ancestor
   commits. Otherwise keep the scoped commit local and report why.
6. Never publish, upload, schedule distribution, send outreach, spend money, or modify Content OS
   release state.

## Output

Return a compact digest containing:

1. sources and surfaces actually inspected;
2. leads added, changed, held, rejected, or expired;
3. the ordered shortlist, with one-line rationale and strongest invalidating question for each;
4. material access limitations;
5. the pool and run-record paths; and
6. commit and push status.

Notify only for a materially changed shortlist, a new blocker, or an access problem that requires
user action. Stay quiet when no lead or disposition changed.
