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

- **Google search:** the most reliable surface. Inspect People Also Ask, the related-search rail,
  autocomplete, result recency, and repeated query formulations. Record the questions verbatim. Do
  not infer volume from result counts.
- **Reddit — search-result renderings only.** Do not plan a run around reading Reddit. As of
  2026-09-21 the domain is refused by both the built-in browser pane and the Chrome extension, by
  WebFetch, and by domain-scoped search, and Reddit returns HTTP 403 to `curl`; being signed in does
  not help, because the request is refused before it is sent. The full test matrix is in
  `automation/candidate-discovery/runs/2026-09-21.md`. What remains usable is what Google's result
  page renders: thread title, subreddit, approximate age, comment count, and a top-answer snippet.
  Cite those as SERP observations, never as a read thread, and never quote or date a comment that was
  not visible in the rendering. Retest one Reddit URL per run in one call and record the result, so a
  restored surface is noticed. If the user supplies thread text directly, treat it as a read thread
  and say where it came from.
- **Hacker News:** search through the Algolia index with a date window. Strongest for developer,
  platform, and infrastructure questions; frequently macro-political and consumer-facing on policy
  topics, which is not a small-operator buyer signal. An absence here is an absence on one surface.
- **Indie Hackers:** useful for what operators are actually building and charging for. Posts are
  seller claims: they verify supply, offers, and possible saturation, not customer demand.
- **YouTube:** inspect autocomplete, recent relevant videos sorted by upload date, view velocity when
  visible, packaging, comment questions, and whether strong coverage already resolves the topic. A
  thin or stale result set is a coverage-gap observation, not evidence of low audience demand.
- **Other reachable communities:** Stack Exchange sites, vendor-hosted and independent Discourse
  forums, public professional communities, trade-association and practitioner forums, and
  domain-specific discussion surfaces. Platform seller help centres and changelogs (Shopify, Etsy,
  eBay, marketplace and payment providers) are a distinct and often better source than a forum,
  because a dated policy change is a primary operating signal. Use only what is publicly accessible
  and attributable.
- **Google Trends:** unreliable in this environment. It failed outright on 2026-09-20 and on
  2026-09-21 rendered without exposing readable values. Attempt it when a direction claim would
  change a decision, and otherwise skip it rather than spending a run on it. When it does work,
  compare useful windows such as 7 days, 90 days, and 12 months and inspect rising and related
  queries and regional differences. Treat the index as relative direction, never exact monthly search
  volume.

Do not force every surface into every run. Choose the surfaces relevant to the observed question and
record unavailable or blocked access honestly.

Because Reddit is no longer readable, most runs will qualify a lead through the operating-change
route in the qualification list — one material operating change plus one independent
audience/question signal — rather than through recurrence across two conversation surfaces. That is
expected, not a lowered bar. It raises the burden on the market and operating-signal lane below: the
change must be dated, primary where possible, and attached to a cost the buyer is already carrying.
Do not compensate for a lost surface by treating seller marketing, vendor guidance, or a press
release as an audience signal.

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
5. a path to honest, showable evidence that does not depend on a guest;
6. enough accessible evidence for the Monday bench to decide whether formal Step 0 research is
   warranted;
7. a **stated delivery boundary** that survives the licensing test below; and
8. at least one **willingness-to-pay signal** of an accepted type below.

### The delivery-boundary test

Added 2026-09-21 by owner decision, after four consecutive leads and two Step 0 candidates failed on
the same axis.

A dated regulatory trigger is the scout's most reliable signal and also its most reliable trap,
because a rule that creates work usually also names who is allowed to do it. Before shortlisting,
name explicitly:

- who is legally or professionally permitted to deliver the core deliverable — an unlicensed
  operator, a licensed or credentialed professional, or an unresolved mix; and
- if a licence or credential is required for any part, **what concretely remains** for an unlicensed
  operator once every regulated task is removed.

That residual is the offer. If the residual cannot be stated in one specific sentence, the lead is
`held` with "delivery boundary unresolved" as the named missing condition — not `shortlisted`.

Also name the **automated or productised substitute** and its published price when one exists. If
the residual is substantially what the substitute already outputs, hold or reject; do not shortlist
a lead whose remaining work is a software output sold as labor.

### The willingness-to-pay test

At least one signal that the target buyer pays an independent provider for **the residual**, not for
the regulated or automated work around it. Accepted signals:

- a buyer describing a payment they made, with enough detail to identify the scope;
- a service request, brief, or job posting carrying a budget for that scope;
- a disclosed engagement, invoice, contract, or first-party result;
- an observed marketplace transaction; or
- an incumbent visibly charging a named buyer for that specific residual.

**Not accepted, in any combination:** vendor or agency pricing pages, directory rate cards, "how much
does X cost" content-marketing posts, seller guidance published to win adjacent work, general loss or
fraud statistics, category size, funding, a deadline, or the volume of coverage a change attracts.
Several weak sources repeating a number do not become one strong source.

If no accepted signal exists, the lead is `held` with the exact missing signal named. This is the
common case for a fresh regulatory trigger, and holding is the correct outcome — a held lead costs
nothing, while a shortlisted one consumes a Monday bench run.

### Transition

Leads shortlisted before 2026-09-21 were screened without tests 7 and 8. Re-screen every existing
`shortlisted` lead against both on the next scout run and re-disposition it honestly, before adding
any new lead. Until a lead records both results, it is not eligible for admission by the Monday
bench.

Reject generic, duplicative, evidence-free, guest-dependent, non-showable, hype-led, or trend-only
ideas early. Hold a plausible lead when one named missing condition could change the decision, and
record its exact reopening condition. A source-access failure is a limitation, not a reason to claim
no interest or demand.

Do not assign a numeric score. Order shortlisted leads by editorial priority and state the decisive
reason in plain language. Keep no more than five shortlisted leads and add no more than three
materially new leads in one run.

Five is a ceiling, not a target. Under the delivery-boundary and willingness-to-pay tests an empty or
one-lead shortlist is a normal and acceptable result. Do not relax either test to fill the pool, and
do not shortlist a lead in order to have something for the Monday bench to admit — the bench is
required to record `NO_QUALIFYING_SHORTLIST` and stop, and that is a cheaper outcome than a Step 0
package that parks.

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
