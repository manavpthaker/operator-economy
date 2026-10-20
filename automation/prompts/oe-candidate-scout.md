# Operator Economy candidate scout

Run this workflow every Wednesday and Sunday at 17:00 America/New_York in
`/Users/brownmanbrain/GitHub/operator-economy`.

Rewritten 2026-10-13 by owner decision (`operator-blueprint-v2/00-intake/OWNER-DECISION-2026-10-13-DISCOVERY-RESET.md`).
Twenty-one daily runs from 2026-09-20 screened about 85 ideas and produced no episode. The audit
found the scout was searching for sellers and needed to search for buyers: ideas came from the
scout's own brainstorm, searches mostly returned vendor pages, and the substitute check then
rejected any idea a vendor already served.

## What we are looking for

**Problems that one person can now solve for buyers with AI, well enough to build a sustainable
business.**

- Start from a buyer's problem, observed in the buyer's own words or actions. Never start from a
  seller, a tool, or a trend.
- The solver is one accountable operator running AI, including **always-on agents** that watch,
  chase, follow up, reconcile, monitor, and answer around the clock under the operator's supervision.
  Work that used to need a firm, a team, or shift staff is the target.
- **Industry size does not matter.** Big industries and small niches both qualify. What matters is
  whether one person can solve the problem for many buyers and charge a small share of the value at
  stake (money recovered, saved, earned, or risk removed) or a fixed fee, and whether that adds up
  to a living for one person.
- Buyers can be businesses of any size, households, or institutions. Prefer buyers who can pay;
  a buyer who cannot pay and has no one paying on their behalf is not a business.

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
   `STEP0.2-APPROVAL.md`, `STEP0.3-CHANGE-PROPOSAL.md`, and the owner decisions in that folder only to
   understand what the scout must not pre-empt.
5. `operator-blueprint-v2/00-intake/OWNER-DECISION-2026-10-17-EXA-RESEARCH.md` for the Exa budget
   below, and `OWNER-DECISION-2026-10-20-IDEALAB-SOURCE.md` for idealab.ai prompts.

When the checked-out branch is not `main`, read this prompt, the README, `POOL.md`, and the run
records from local `main` (`git show main:<path>`); that is where scout commits land.

This is pre-intake discovery. Never create or edit Step 0 artifacts, readiness scores, promotion
records, the canonical queue, episode numbers, scripts, narration, production, or release state.

## Preflight and deduplication

1. Resolve the current Eastern date. Inspect the current branch, upstream divergence (verify ahead
   and behind with `git rev-list --count`), and `git status`. Preserve unrelated dirty work and stop
   on an overlapping edit you cannot isolate.
2. Read the current pool and recent scout runs. Continue useful unfinished screening, then the
   re-screen queue (below), before adding new leads.
3. Deduplicate against every Step 0 candidate, research package, validation, disposition and
   promotion; `operator-blueprint-v2/00-intake/04-queue/QUEUE.md`; every episode and production
   workspace; parked, rejected, archived and historical topic material; `research/`, `topics/`,
   `studio/originate/`; and the pool. Compare buyer, problem, offer, outcome, mechanism, and episode
   claim. A renamed duplicate is still a duplicate. A previously rejected idea is not a duplicate if
   it was rejected only under a rule this rewrite removed; it goes to the re-screen queue.

## Run budget

Each run is a deep pass, not a skim:

- at least 20 searches and at least 6 pages read in full (not search summaries);
- at least 15 buyer-side observations logged before any idea is formed; and
- Google Trends checked for the one or two phrases each surviving lead turns on.

Record what was actually read. A search summary is cited as a summary, never as a read page.

Search and read through brownbot's scout first (content-os `outreach/research-sources.md`, D-262),
with `--routine oe-candidate-scout` on every Exa call; WebSearch and WebFetch are the fallback.
`BB="npm --prefix /Users/brownmanbrain/GitHub/brownbot run -s"`:

- `$BB scout -- exa --q "<query>" --text --routine oe-candidate-scout` returns full page text, so
  each result with text counts as a page read; `$BB scout -- contents --urls <url,…>` reads pages
  a search found elsewhere;
- `$BB scout -- youtube --q "<how-to query>" --days 365`, then `$BB scout -- youtube-comments
  --video <id> --terms "how do I,gave up,anyone know,who do I hire"` for viewer questions;
- `$BB scout -- hn --q "<query>" --kind comment` for practitioner complaints; and
- `$BB scout -- jobs --board greenhouse|lever|ashby --company <token>` when a lane names employers.

Each call counts toward the search budget above. Log the command and the source URL in the run
record, and cite a page read through Exa as such.

**Exa budget and steering (owner decision 2026-10-17).** Exa is the one thing this job may spend
money on:

- At most $0.40 of Exa a run (about $0.007 a search, $0.001 a page read). Run `$BB scout -- status`
  first; if the month's total (shared with Content OS routines) is $15 or more, use no Exa this run.
  Stop Exa when the run reaches $0.40 or a call is refused, and go on with the free commands and
  WebSearch.
- Write queries as a buyer would say the problem ("who do I hire to chase unpaid invoices", "we
  bought X and nobody runs it"), not as a category. Steer with `--domains` (reddit.com, or a forum,
  review or job site such as biggerpockets.com, contractortalk.com, community.shopify.com,
  trustpilot.com, g2.com, capterra.com, upwork.com), `--since <date>` for recent posts, and
  `--exclude` for vendor domains that crowd the results. Do not use `--category company` or
  `people` for observations: they return sellers.
- Exa is not a source. Seller pages it returns are still never buyer-side observations. A result
  with only a title and snippet is a search summary.
- Record each Exa query with how many usable observations it gave, and the run's Exa spend, so
  later runs rotate queries instead of repeating them.

## Step 1: buyer observation ledger (always first)

Before forming any idea, collect raw buyer-side observations and log each in the run record with
source, date, the buyer's exact words or action, and the surface. A buyer-side observation is one of:

- **a job or contract posting** for work that is mostly reading, writing, checking, sorting,
  reconciling, monitoring, chasing, scheduling, or answering (Indeed, LinkedIn, government and
  association job boards, as search results render them; part-time, per-project, and shift roles
  are especially useful because they show a job a buyer would hand to an outside operator);
- **a freelance brief** (Upwork, Fiverr requests, Contra, as search results render them);
- **a buyer question**: who should I hire for, how much should I pay for, how do I stop spending
  time on, is there someone who, what do people do about (Google People Also Ask and autocomplete,
  `site:quora.com` titles, Stack Exchange, BiggerPockets, ContractorTalk, Shopify Community, trade and
  practitioner forums, vendor-hosted Discourse forums);
- **a complaint with a consequence**: negative reviews of businesses or tools (Google reviews,
  G2, Capterra, Trustpilot, app stores) where the reviewer names a job that is not getting done, or
  a tool they bought that nobody runs;
- **YouTube comments** on how-to videos where viewers ask for help or say they gave up; and
- **rising search phrases** from Google Trends related and rising queries.

Seller pages, vendor blogs, press releases, cost-explainer marketing, and directories are never
buyer-side observations. They may be recorded later as context or as substitutes.

Reddit: as of 2026-09-21 the domain is refused by the browser pane, the Chrome extension, WebFetch,
and domain-scoped search, and returns HTTP 403 to `curl` (test matrix in `runs/2026-09-21.md`).
Reddit's own API is gated, so there is no key. Try Exa first: `$BB scout -- exa --q "<query>"
--domains reddit.com --text --routine oe-candidate-scout`. A thread whose text comes back is a page
read and its posts are buyer-side observations; record in the run log whether text came back.
Otherwise use only what Google's result page renders (thread title, subreddit, age, comment count,
visible snippet) and cite it as a SERP observation. Quora pages
return 403; `site:quora.com` titles are usable as SERP observations. Upwork returns 403 directly.

## Step 2: where to look (lanes)

Spread observation-gathering across these lanes. At least two thirds of new leads must come from
lanes A to C.

### Lane A: buyer problems

Start from a kind of buyer (any industry, any size) and collect what they ask, complain about, hire
for, and give up on. Rotate buyer types across runs and record which were covered, so runs do not
keep returning to the same few.

### Lane B: tool-to-service gaps

AI tools and agents are being sold to buyers who do not have the time or skill to set them up, run
them, check them, or own the result. Look for buyer-side evidence of that gap: reviews saying a tool
was bought and abandoned, questions about who can set something up or manage it, job postings for
someone to run a tool. A tool sold to buyers is evidence that the problem is real, not that it is
solved.

### Lane C: always-on agent work

Jobs that are continuous rather than one-off: watching for changes, chasing replies and payments,
following up leads, monitoring listings, prices, filings or compliance, answering after hours,
reconciling as transactions arrive. Before agents these needed staff on shift or were simply not
done. Look for buyers paying staff, overtime, or answering services for this, or losing money
because nobody watches.

### Lane D: operating changes

Regulation, platform, pricing, and market changes that create or move work. At most one new lead
per run from this lane, and it still needs a buyer-side observation (Step 1); a rule alone is not
a lead. A rule that creates work usually names who may do it, so the delivery-boundary test below
matters most here.

Ideas from the scout's own knowledge may be used only as **search prompts**: name the buyer and go
look for their observations. An idea becomes a lead only when a logged buyer-side observation
supports it, and the lead records the observation that generated it.

### idealab.ai prompts (owner decision 2026-10-20)

idealab.ai is a free database of about 1.2 million AI-written business ideas
(`operator-blueprint-v2/00-intake/OWNER-DECISION-2026-10-20-IDEALAB-SOURCE.md`). Its ideas assume a
2–20 person software venture with $75,000+ to start and $12 million+ a year at success, rest on 1
to 4 sources (often foreign news recast as a US problem), and score themselves. Treat an idealab
idea exactly like the scout's own knowledge: a search prompt, never a lead or evidence.

- At most **5 searches and 3 briefs a run**, through `python3 automation/tools/idealab.py`
  (`search "<what the buyer needs>" --filters '<json>'`, `brief <id>`, `codes`). Useful filters:
  `{"teamSize":["solo","team_2_5"],"buildType":["HS"],"capitalBand":["c0_10k","c10_50k","c50_100k"]}`
  and `{"teamSize":["solo","team_2_5"],"evidenceType":["consumer_complaint","forum_post"]}`. Do not
  create an account or start a new visitor session to get around the daily limits.
- Restate each idea you pursue in the Operator Economy shape (one operator, AI and agents, the buyer
  who pays, a share of value or fixed fee), and record in the run log the idealab ID, title, and
  what it assumed beside the restatement.
- Then run Step 1 for that buyer. A consumer complaint or forum post the brief cites may be followed
  and read at its own URL; once read it can be a buyer-side observation. The brief itself cannot.
- Use the brief's competitor list as a starting list for test 4; verify and price each substitute on
  its own page before citing it.
- idealab's scores, market sizes, revenue and capital figures, and why-now text are never evidence
  or unit economics. At most one new lead a run may start from an idealab prompt; it counts toward
  the lane its origin observation came from.

## Step 3: turn observations into leads

For every lead worth retaining, capture the contract in `automation/candidate-discovery/README.md`,
including:

- the **origin observation** (the buyer-side observation that generated the lead);
- buyer, problem, and what it costs them;
- potential offer and observable outcome;
- what AI and agents do, and what one person does;
- **unit economics sketch**: value at stake per buyer, a plausible fee (share of value or fixed),
  roughly how many buyers one person could serve, and whether that sustains one person. Label it a
  modeled scenario;
- why now;
- strongest existing answer and what it misses;
- possible Operator Economy point of view;
- strongest invalidating question;
- evidence still needed; and
- expiry or recheck date.

The Operator Economy angle must be earned: hidden labor, cost, dependence, accountability, customer
ownership, data, margin, recourse, or a realistic one-person advantage. Do not manufacture
contrarianism.

## Qualification: five tests

A lead is `shortlisted` when it passes all five. If one named missing condition could change the
decision, it is `held` with the exact reopening condition. Otherwise it is `rejected`.

### 1. Real buyer, real problem

- At least two buyer-side observations from independent sources (different surfaces or unrelated
  buyers), or one buyer-side observation plus one dated operating change that raises the cost of the
  problem.
- At least one typed **problem-value signal**: `residual` (buyer already pays an independent
  provider for this job), `old-way spend` (buyer pays staff, overtime, contractors, firms, or
  agencies for the same job done the pre-AI way), `problem cost` (losses, penalties, time, backlog,
  lost revenue, churn, or the buyer's own account of the pain with a consequence), `adjacent spend`
  (budget visibly exists for a neighbouring job), or `demand signal` (buyers asking who to hire, how
  to fix it, or what it costs).
- **Payment evidence** is recorded as `found` (type and source) or `unknown — viewer's first test`.
  It is not required.
- Vendor pricing pages, rate cards, cost-explainer content, category size, funding, and deadlines
  are context only, never buyer evidence. Trend-only leads are rejected.

### 2. One person with AI

Name in one sentence what AI and agents do, and what the business looked like before (a firm, a
team, staff on shift, or not done at all). Pass when AI is what lets one person deliver the outcome
to many buyers. Fail when the business runs the same without AI, or AI is a minor helper (drafting
emails, sorting photos). Include the unit economics sketch; fail it only if no plausible fee and
client count could sustain one person.

### 3. Delivery boundary

Name who is legally or professionally permitted to deliver the core deliverable. If any part needs a
licence or credential, state in one specific sentence what remains for an unlicensed operator. That
residual is the offer. If it cannot be stated, hold with "delivery boundary unresolved".

### 4. Substitutes (rewritten 2026-10-13)

Name the strongest substitutes and their published prices: self-serve AI tools, done-for-you
services, firms, and the buyer's own staff.

- **A tool sold to buyers does not fail this test.** It shows the problem is real. The operator's
  angle is what the buyer does not get from the tool: setup, running it every day, checking its
  output, combining several tools, always-on monitoring, and owning the outcome.
- **Reject only when** (a) a done-for-you service already delivers the same outcome to this buyer
  at a price one operator could not beat and buyers in this segment readily use it, or (b) there is
  buyer-side evidence that buyers in this segment run the tool themselves and get the outcome.
- Seller claims that a segment is served are not evidence that it is. Record them as context.
- For an `old-way spend` signal, record the switching question: why this buyer would move that
  spend to an outside operator rather than to software or its own staff.

### 5. Showable and fit for the channel

Clear audience and thesis fit; a showable path that does not depend on a guest; not hype-led,
generic, or a duplicate; enough accessible evidence for the research bench to decide whether formal
Step 0 research is warranted.

Do not assign a numeric score. Order shortlisted leads by editorial priority with the decisive
reason in plain language. Keep no more than ten shortlisted leads (raised from five 2026-10-13: the bench will not use every
shortlisted lead) and add no more than three materially new leads per run. Ten is a ceiling, not a
target. A source-access failure is a
limitation, not evidence of no interest.

## Re-screen queue (transition, from 2026-10-13)

Ideas rejected between 2026-09-20 and 2026-10-13 mainly because an AI tool or AI-backed service
already sold the job (the old substitute check), or because no current buyer voice was found while
Reddit was blocked, are re-screened under the five tests above. Re-screen up to two per run before
new leads, starting with those whose rejection named a self-serve tool rather than a done-for-you
service. Each re-screen needs a fresh buyer-side observation; a re-screen that finds none stays
rejected with the date. Record re-screens in the run record and update the rejected index. Delivery-
boundary and AI-change rejections are not re-screened unless their own reopening condition is met.

## Persistence and git safety

1. Write the observation ledger, screening, deduplication, and dispositions to
   `automation/candidate-discovery/runs/YYYY-MM-DD.md`. Append a numbered rerun section rather than
   overwriting a same-date record.
2. Update `automation/candidate-discovery/POOL.md` with the current `new`, `shortlisted`, `held`,
   `rejected`, and previously `admitted` states. Preserve historical rejection evidence in the run
   record.
3. The scout may never mark a lead `admitted`; only the research bench may do so after it creates a
   formal candidate artifact.
4. Commit only the pool and this run's explicit discovery records. When another branch is checked
   out, commit to local `main` through a temporary index without touching the working tree. Never use
   `git add -A`, reset, clean, delete, amend someone else's commit, or include unrelated dirty work.
5. Push only when the scoped commit can be pushed without carrying unrelated unpublished ancestor
   commits. Otherwise keep the scoped commit local and report why.
6. Never publish, upload, schedule distribution, send outreach, spend money, or modify Content OS
   release state. The one exception is Exa within the run cap above (owner decision 2026-10-17).

## Output

Return a compact digest containing:

1. surfaces inspected, searches run, pages read, and observations logged, with the Exa queries,
   their yield, and the run's Exa spend;
2. buyer types covered this run;
3. leads added, changed, re-screened, held, rejected, or expired;
4. the ordered shortlist, with one-line rationale and strongest invalidating question for each;
5. material access limitations;
6. the pool and run-record paths; and
7. commit and push status.

Notify only for a materially changed shortlist, a new blocker, or an access problem that requires
user action.
