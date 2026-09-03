# Candidate: Workflow-reliability sprint for small professional-service firms

Template status: approved V2 Step 0.2 template; locked 2026-08-21.

Status: candidate

Template version: `operator-blueprint-v2-step0.2`

Candidate ID: `candidate-2026-09-03-workflow-reliability-service`

Created: 2026-09-03

Owner: Manav Thaker

Proposed evidence class: observed model

## Provenance: legacy premise, re-entered as a real candidate

This candidate re-enters the premise published as EP003, "The 5 Billion Dollar Business That Sounds Boring" (2026-07-27; URL held only in `studio/originate/boring-automation-agency/launch/links.json`). Prior publication earns no promotion credit. The old research, script and economics are leads, not evidence, and every number in them is re-verified or marked not usable in the research brief.

- Historical source premise: `research/briefs/ep003-boring-automation-agency.md` / `ba8a4430ea0e63d76578b499ef05cafb1cbabc01e6be197d7c76b9103838ccb8`
- Historical script: `studio/originate/boring-automation-agency/script.json` / `788e91d62317cf186b4b477486651399c4216e52b3640f5f11bd856f2106a14d`
- Historical blueprint derivative: `studio/originate/boring-automation-agency/content/blueprint.md` / `48396e5b96eb7a5a290c8174d1859285275011eaf40583849de5f89dacd90519`
- Related test fixture (method exemplar only, never promotable): `../fixtures/legacy-episode-calibration-2026-08-21/`. Its refinement ("a productized workflow-reliability service for small service businesses") and its source leads are reused; every source was re-opened on 2026-09-03 and the POV factor is rescored under Step 0.3. Its scores (81 and 72) are not anchors.

**Refinement stated explicitly.** The historical premise was "SMBs pay for workflows that move data between the tools they already use, built on n8n or Make, priced as a retainer." That is a tool category with an undefined buyer and an assumed revenue model. This candidate bounds it, without changing the underlying business, to one buyer (the owner or operations lead of a 5–50-person professional-service firm), one job (the client-intake → scheduling → billing handoff that crosses a CRM, a calendar and a billing tool), one deliverable (that single handoff mapped, built on the platform the client already pays for, tested against exception cases, wired to alerts, documented, and monitored for thirty days, with a before-and-after count of manual touches), and one thirty-day test (two paid diagnostics and one paid sprint in one reachable segment). The retainer moves from premise to hypothesis: it is offered only if the monitoring window produces a documented recurring reliability job.

## Opportunity in one sentence

An operations-minded generalist sells small professional-service firms a fixed-fee sprint that turns one fragile cross-tool handoff into a tested, observable, documented workflow — and is paid for the reliability, not for connecting apps.

## Viewer outcome

- Viewer promise: The viewer can tell the difference between a demo automation and a production workflow, and knows what a small firm is actually buying when it pays for one.
- Operator decision: Build the sprint, run one paid pilot, fold it into existing consulting, or reject it because the buyer will not pay for reliability separately from software.
- Practical capability: Pick one workflow worth automating, map its states and exceptions, decide what stays human, design the test cases, price a fixed scope against real hours, and run a thirty-day pilot with a kill condition.
- Expected Operator Canvas: Operator fit, buyer and trigger, workflow selection score, the exception matrix, delivery steps with tool jobs attached, human controls, price hypothesis, capacity, acquisition path, platform-change watchlist, and disqualifiers.

## People

- Viewer/operator: An operations, product, RevOps, implementation or systems generalist who can interview the people doing the work, read an API or a no-code builder, test edge cases, write a runbook, and talk to an owner in plain terms. No credential required.
- Buyer: The owner or operations lead of a 5–50-person professional-service firm (law, accounting, agency, consultancy, design studio) that runs a CRM, a scheduling tool and a billing tool and still bridges them by hand.
- End customer or beneficiary: The staff doing the copy-paste and chasing, and the client whose intake, appointment or invoice stalls between systems.
- Guest or outside participant required: no for the episode; yes for a real pilot client, with written permission before anything about them is shown.

## Problem

- Costly problem: Client state lives in three or more tools that do not share it. Someone re-keys, reconciles and remembers the next step, and when a platform changes underneath a home-made automation the handoff fails — sometimes loudly, often silently.
- Why it matters: The cost shows up as staff hours, stalled intake, missed follow-up, duplicate records and, in the sourced failure cases, months of automations quietly filtering out every new client without anyone noticing. The frequency and dollar consequence for this exact buyer are **not yet quantified** and are a research target.
- Why now: US small firms are adopting AI and software faster than they are integrating it — nearly half now use AI but only a small minority have fully integrated it into processes — while the platforms these workflows run on are changing pricing and deprecating APIs on dated schedules in 2026. More tools, more handoffs, more fragility, on a calendar.
- Existing alternatives and budget: Staff do it by hand; the owner builds a two-step automation and forgets it; a freelancer connects apps once and leaves; an agency listed in a vendor directory does the job for firms that find it. Budget for hands-on automation services demonstrably exists (hundreds of listed partners, hundreds of reviews each), but the price a small firm pays is opaque and every published range is seller-authored.

## Proposed business

- Offer: A fixed-scope workflow-reliability sprint: discovery, current-state map, baseline count of manual touches, one production workflow on the client's existing platform, a test suite of ordinary and exception cases, alert and retry or stop behaviour, a named human exception owner, runbook, training, and thirty days of monitored operation with a written maintain / expand / retire recommendation.
- Customer outcome: One named handoff goes from "a person remembers" to "a workflow runs, logs, alerts, and a named person owns the exceptions," with a before-and-after measure the owner can read.
- Delivery hypothesis: Interview the people doing the work, inspect the systems with scoped access, map states and exceptions, automate only the stable path, test, document, hand over ownership, monitor.
- Revenue hypothesis: Fixed project fee. A monitoring retainer is a **separate hypothesis**, offered only when the thirty-day window produces a real recurring reliability obligation.
- Most important unproven assumption: That a reachable small-firm owner will pay a fixed fee for reliability — testing, exception design, documentation, monitoring — rather than buy the software, hire the cheapest connector, or tolerate the manual bridge.

## Initial synthesis hypothesis

- Parallel A: Zapier Solution Partners — the exact professional-service model (hands-on implementation, documentation, training, post-implementation support) and a vendor-assisted buyer channel.
- Parallel B: n8n Expert Partners and the agencies in its community — the exact multi-client automation practice, defined by the vendor as "automation and AI services as the main revenue stream" with at least three active customers.
- Parallel C: Fixed-scope technical audit and readiness consulting — the paid-diagnostic entry and the hours-against-fixed-fee economics.
- New combination: The observed category re-scoped around the reliability job — exception ownership, tests, observability, documentation, a monitoring window, and a stop condition — sold to one buyer type, with the retainer demoted from premise to hypothesis.
- Suspected transfer risk: Vendor partner ecosystems demonstrate that the business exists for selected, credentialed, reviewed partners. They do not show what an unknown independent can win, or at what price.

These are research directions, not evidence. The completed research brief and analogy map decide whether the transfers are valid.

## Narrative potential

- Starting state: A new client fills in a form. The CRM knows. The calendar does not. The invoice never gets raised. A person notices, or does not.
- Inciting change: A platform the firm depends on deprecates an API on a published date, or renames a field, and the automation somebody built two years ago starts silently dropping every new client.
- Causal mechanism: Each tool holds only part of the client's state; the connections between them were built for the happy path; identifiers go stale; nothing is watching.
- Operator build: Follow one client through the systems, map every state and exception, automate only what is stable, give failures an owner and an alert, count the manual touches before and after.
- Stakes and tradeoffs: Automate more versus keep it human; client-owned versus operator-owned infrastructure; fixed fee versus the obligation a retainer creates; speed versus test coverage; scoped access versus privacy.
- End state: The handoff shows fewer manual touches and a logged, owned exception path — or it fails its test, and the operator learns not to sell it yet.
- Visual evidence: one client record moving through three interfaces; the state map; the copy-paste; the execution log; the stale ID; the alert; the test matrix; the before-and-after touch count; the runbook; the vendor's deprecation notice with a date on it.

## Audience pull

- Exact or adjacent viewer questions: "how to start an automation agency," "n8n automation agency," "Zapier expert," "workflow automation consultant," "what should a small business automate," "why did my Zap stop working."
- Initial interest signals: 700+ Zapier Solution Partners and directory listings carrying hundreds of reviews each; n8n's partner criteria and community agencies reporting dozens of active clients; a US federal survey showing AI adoption far ahead of integration; dense 2025–2026 creator coverage of the "n8n agency" opportunity. All verified in research; exact search volume attempted and not measurable.
- Timely tension: The tools are easier and cheaper than ever, the "start an agency" content is everywhere, and the platforms underneath are repricing AI steps, pausing scenarios when credits run out, and deprecating APIs on 2026 dates. The thing being sold in the coverage (the build) is not the thing that keeps paying (the reliability).
- Coverage gap: Existing coverage is tutorials, "make money with n8n" videos, and agency-authored pricing guides that state their own ranges are not market data. Very little teaches the operating judgment — what not to automate, exception ownership, testing, observability, measurement, and the honest price of the hours.
- Honest working premise: Everyone is selling you the automation agency. Here is the job the buyer actually pays for — keeping one workflow alive when the platform changes — and what it costs to deliver.

## Discovery and POV

- Search-volume status: attempted but not measurable — Google Trends returned HTTP 429 on 2026-09-03; no licensed keyword tool is available to this operation; no secondary source cited a Keyword Planner figure for the exact queries.
- Operator Economy POV (scored under Step 0.3): **transferable builder experience, bounded; original synthesis, partial.**
  - Builder experience: `content-os/facts.md` records that as AI Product Manager at Lovingly (Sep 2024 – Sep 2025) Manav automated ticket triage, PRD creation, test documentation and workflow optimisation with AI tools, with a recorded 80% time saved on repetitive PM tasks. That is first-hand experience of deciding what to automate, what to keep human, and what breaks — inside a company, for his own team.
  - Original synthesis (to be demonstrated in research): the observed business is defined by the vendors' own partner criteria as multi-client service delivery, and the durable, sellable job is the dated platform-change event — API deprecations, AI-step repricing, credit-exhaustion pauses — not the build that the beginner coverage sells.
- POV boundary: Manav has **never run an automation agency, sold a workflow to a client, priced this work, or maintained a client's production system.** The historical EP003 script's anecdote about watching a Lovingly team move florist data between three systems by hand is **not in facts.md and may not be stated** unless the owner adds it there. Nothing here is a claim about typical prices, margins or income.

## Initial evidence status

- Buyer-problem evidence: lead found — federal and public-bank surveys for the adoption-integration gap; vendor documentation and one agency-published case for the failure shape; consequence for the bounded buyer unquantified.
- Budget or current-alternative evidence: lead found — partner directories and reviews show spend exists; no independent price data.
- Offer and delivery parallel: usable — vendor partner case documents the delivery shape (map, build, SOPs, training, support).
- Economics or capacity inputs: modelable — every price input will be a labelled hypothesis.
- Audience-interest signals: one signal — needs triangulation in research.
- Narrative engine: strong — one client record, one silent failure, one dated deprecation notice.

## Known blockers

1. **No independent service-price observation.** Every 2026 pricing range found is agency-authored; one states outright that its ranges are "not market averages." Upwork's hire page returned HTTP 403 and Fiverr's category page redirected on 2026-09-03. Economics will be entirely modeled until a pilot produces a paid proposal.
2. **Crowded, seller-side coverage.** The audience attention that exists is largely people selling courses and agency dreams to would-be operators. The episode must be positioned against that coverage, not as more of it, and creator attention cannot be counted as buyer demand.
3. **Consequence unquantified for the bounded buyer.** The best failure evidence is one agency-published case and one vendor deprecation notice. No source measures how often a small firm's handoff fails or what it costs.
4. **Access, credentials and privacy.** The sprint touches client CRM, calendar and billing data. Least privilege, client-owned accounts, test data and an access-revocation plan are conditions of the offer, not options.
5. **Prior publication is a null signal.** The V1 episode's day-4 read was 160 impressions, 0.0% CTR and 1 view, with the thumbnail having fallen back to the title card. The sample is too small to read as audience rejection, but it provides no positive evidence either.
6. **POV is builder-side only.** No client-side experience exists and none may be implied.

## Intake decision

Decision: research

Reason: The business is observed — vendors define it, list hundreds of practitioners, and buyers leave hundreds of reviews — and the failure that makes it sellable now has dated, primary documentation in 2026. What the historical package got wrong (an undefined buyer, seller-authored pricing presented as market ranges, a retainer assumed rather than earned, "boring" treated as a moat) is fixable by bounding, not by abandoning the premise. The open risks — no independent price, crowded coverage, unquantified consequence — are exactly what research and a thirty-day pilot are for. Proceed to the research brief.
