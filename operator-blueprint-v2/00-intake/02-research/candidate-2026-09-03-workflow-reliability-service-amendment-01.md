# Step 0 evidence amendment 01: asking prices, buyer budgets, search direction and failure mechanics

Status: recorded

Template version: `operator-blueprint-v2-step0.2` (amendment record; the reviewed research brief is unchanged so the package hashes still hold)

Candidate ID: `candidate-2026-09-03-workflow-reliability-service`

Research brief amended (by reference only): `candidate-2026-09-03-workflow-reliability-service.md` / `687e499ffaec634d90728efb35a62725b33edbb9135b68f4631d195b3ed09876`

Disposition: `../03-validation/candidate-2026-09-03-workflow-reliability-service-disposition.md` (continue research, Reviewer A 69 / Reviewer B 63)

Governing decision: `../OWNER-DECISION-2026-09-28-COACHING-STANDARD.md` / `95c781cba2a8ad5d8f76dda597329e0f84b4732226f9c8886a9520f0af2cd686`

Recorded: 2026-09-28

Recorded by: the Step 0 research bench, restarting the candidate under the 2026-09-28 coaching standard

## Why this record exists

The 2026-09-03 disposition named two re-entry items. Item 1 (ten owner interviews) is removed by the owner decision of 2026-09-28 and becomes the viewer's first test below. Item 2 (a marketplace asking-price sample and a working search-volume attempt) is desk work, and this record carries it out. It also looks for buyer-posted jobs with budgets and for better consequence evidence, because the package's price and consequence evidence were weak.

This record does not edit the research brief, the analogy map, the gates or the scorecard. It does not change any score. Its recommendation is at the end.

## What was attempted and what happened

| Target | Method | Result on 2026-09-28 |
|---|---|---|
| Upwork job search and hire pages | WebFetch; built-in browser, read-only | **Blocked.** HTTP 403 to WebFetch; the browser stopped at a Cloudflare bot challenge. Not bypassed. Individual job pages also blocked |
| Fiverr gig search | WebFetch; built-in browser, read-only | **Blocked.** HTTP 403; the browser showed a "human touch" CAPTCHA (PerimeterX). Not attempted. Gig titles with starting prices were read from the search index only (CLM-025) |
| Zapier Solution Partner directory | WebFetch of the directory and ten partner profiles | **Worked.** Minimum spend, accepted budget bands and service lists recorded (CLM-023) |
| Make partner directory | WebFetch | Worked, but shows no prices or budgets. Make routes small jobs to its community "Hire a pro" board, which was then sampled (CLM-026) |
| n8n community Jobs board | WebFetch of the board and six seller posts | **Worked** (CLM-024) |
| Freelancer.com (substitute for Upwork buyer posts) | WebFetch of Zapier and Make.com job lists and four project pages | **Worked.** Buyer budget ranges recorded (CLM-027) |
| Google Trends | Built-in browser, read-only | **Worked** on two of three comparisons; the third loaded after a scroll (CLM-028) |

## Evidence pass

### (a) Asking prices for automation repair and maintenance (seller side, not transactions)

**Zapier Solution Partner directory, ten Platinum partners (CLM-023).** Every one of the ten lists "Fixing a few Zaps (1-10 Zaps)" or equivalent as a service. Their stated minimum spend: $100 (Flow Digital, Net3Marketing), $200 (MercOlogy, The Joinary), $250 (Connex Digital, flowmondo, Ashar Malik, Solvaa), $500 (GetUWired), $1,000 (XRAY). **Median $250.** Accepted project bands start at $100–$250 and top out at $5,001–$10,000 (five partners) or $10,001–$200,000 (five). The only priced product is Flow Digital's 75-minute implementation session at **$297**, which covers "quick fixes, Zap troubleshooting." Connex Digital lists "Maintenance" among its services but no maintenance price.

**n8n community Jobs board, September 2026 (CLM-024).** A dense run of single-fix offers: US$40 fixed for one fault (18 Sep); $125 fixed diagnosis, credited to the repair (11 Sep); €150 "pay when green" (8 Sep); $149 for one workflow up to 12 steps, including success and failure tests, retry or error notification and a monitoring handoff (14 Sep); $150 paid after it runs (31 Aug). The sampled threads show one reply each at most and **no buyer saying they hired**. One seller (27 Sep) packages the same shape as this candidate: a $1,500 "AI Workflow Audit," a $3,000–$5,000 "Build Sprint," and a $750–$1,500 monthly retainer — an asking price with no sign of a buyer.

**Fiverr, search-index titles only (CLM-025).** Nine "fix Zapier" gig titles carry starting prices of $5, $5, $10, $10, $25, $30, $70, $100 and $350. The gig pages were not opened (CAPTCHA). Starting prices on Fiverr are package floors, not typical fees.

**Seller quotes inside buyer threads (CLM-026).** On two Make Community "Hire a pro" threads, freelancers replied to buyers with fixed quotes:
- Work-order sync repair (Aug 2026): $125, $200, $240, $350 ($150 diagnostic credited), $499, $695. **Median about $295.**
- Audit of a half-built Make + Airtable intake system (Aug 2026): fixed audits of $95, $100, $125, $250, $400, $400 (median about $190), plus $20/hr and $60/hr offers, and one offer of $1,500 per five-day implementation block.

**Reading.** The observable price for "fix a broken workflow" is **tens to low hundreds of dollars**, and the supply at that price is crowded. Directory partners with hundreds of reviews set floors of $100–$1,000. This is an asking-price floor, not a price for the candidate's full reliability sprint.

### (b) Buyer-posted jobs with budgets (buyer side: service requests carrying a budget)

| Buyer and date | Budget stated by buyer | What they asked for | Fit to this candidate |
|---|---|---|---|
| Doctor Fix-It Restoration, Mt Laurel, US; open on Freelancer.com 2026-09-28 | **$750–$1,500 USD** | Connect JobSight, Markate (CRM and billing) and Zapier across lead → appointment → sold → deposit → scheduling → production → payment, with escalation of ignored tasks and "clear stop conditions" | Close. A small service firm's intake-to-billing handoff with exception handling. It is a build, not a paid reliability scope |
| Refrigerated freight brokerage; open on Freelancer.com, posted about 2026-09-23 | **$1,500–$3,000 USD fixed**, paid on delivery | Tai TMS ↔ Zapier ↔ Microsoft 365 appointment scheduling; "escalate exceptions to dispatchers," "prevent duplicate requests and document all failures," audit logging | Reliability requirements written into the build by the buyer. 97 bids, average $2,098 |
| Service business, Canada; open on Freelancer.com 2026-09-28 | **$250–$750 CAD** | Live P&L dashboard fed by Square, QuickBooks, Payworks and Jobber via Zapier, plus a WordPress refresh; "working Zapier scenarios with documented steps" | Documentation requested; very low budget for the scope |
| HPUSA; Make Community, 2026-09-25 (budget stated 2026-09-27) | **"approximately USD $25 per hour"** | Mailchimp → Brevo migration via Make and WordPress, including testing, duplicate prevention, troubleshooting and documentation | Integration plus testing at a low hourly budget |
| Voice-agent owner; Freelancer.com 2026-09-28 | **AUD $25–$50/hr** | "Existing Automation Takeover" of a production Retell AI + Make agent | Takeover of a live system; not the bounded buyer |
| Rusty_Phillips, SOS Inventory user; Make Community 2026-08-12/13 | No budget | Sync sales orders to work orders; then asked: "do you offer maintenance (say we make this, but there's an update in SOS that breaks our process) … if something in the chain breaks our team will be left helpless." | **The reliability job in the buyer's own words.** No price attached |
| Ultra_Fund, merchant-funding broker; Make Community 2026-08-26 | No budget; "open to paying for a short audit first, then having the same person finish the implementation" | Audit and finish a half-built intake automation (dedupe, field overwrite, contamination) | Buyer-side support for a paid-diagnostic entry |

**Reading.** Buyers post budgets of **$750–$3,000 for whole builds that include reliability requirements**, and $25–$50/hour for integration work. One buyer asked for maintenance in plain words, without a price. **No buyer-posted budget was found for a stand-alone reliability sprint.** The candidate's $3,500 base price sits at or above the top of every buyer budget observed. That is an adverse finding for the price hypothesis, and it is the first observed price evidence the package has had.

### (c) Search direction (Google Trends, US, past five years, weekly; read 2026-09-28)

| Comparison | Finding |
|---|---|
| `zapier expert`, `n8n agency`, `automation agency` | `automation agency` rose from near zero (2021–2024, mostly 0–5) to a peak of 100 in the week of 10 May 2026, stayed at 79–95 through early July, then fell to 38 (12 Jul), 23 (19 Jul) and 9–19 through September. `n8n agency` peaked at 11; `zapier expert` averaged 0. Rising related queries for `automation agency`: "what is ai automation agency," "ai automation agency course," "ai automation agency reddit" — all seller-side |
| `zapier not working`, `zapier consultant`, `automation consultant`, `zapier` | The two buyer-problem phrases read 0 on this scale in almost every week. `zapier` half-year averages: 13.6 (2021 H2), 34 (2023 H1), 48.5 (2025 H1), 73.7 (2026 H1), then 32.5 (2026 H2 to date) |
| Control: `zapier`, `n8n`, `quickbooks` | From early July to mid-September 2026, `zapier` fell from about 9 to 3 and `n8n` from about 12 to 4 on this scale (roughly two-thirds), while `quickbooks` fell from about 98 to 58–76 (about a fifth to two-fifths). The final week is partial |

**Reading.** Search interest in the seller-side phrase rose steeply from 2025 to mid-2026. **Buyer-problem phrases are too small to measure against these terms.** The sharp mid-July 2026 drop appears across all terms, including the control, so part of it may be a change in the Trends series rather than in behaviour. The control fell less than the automation terms, so some real cooling is possible. **Direction since July 2026 is not readable with confidence.** This is a measured signal, but it is seller-side and it does not support a higher audience score.

### (d) Consequence evidence

1. **Platforms stop workflows by rule, on their own documentation (CLM-029).** Zapier (updated 2026-05-29): "Your Zap will automatically turn off if 95% of its runs result in errors in the last 7 days," with a 72-hour grace period on Enterprise and 24 hours on Team; no grace period is stated for other plans. Make (updated 2026-09-08): scenarios are deactivated after a set number of errors in a row, and "If a scenario starts with an instant trigger, the setting is ignored and the scenario is deactivated immediately once the first error has occurred." This is primary evidence of *how* a small firm's workflow stops. It is not evidence of how often.
2. **The Pipedrive deprecation hit two platforms on the same date (CLM-009 refreshed, CLM-030).** Make's help centre (updated 2026-01-19) says scenarios using Pipedrive API v1 modules "will stop working" after 31 July 2026. Zapier's notice is unchanged since 2026-05-29 and adds that "the V2 API returns less data than the V1 API. Some fields that were previously available … are no longer included." So the event was not one platform's quirk, and the migration can itself break field mappings. Zapier also documents an earlier batch of deprecations (Box, Trello, Twilio and nine others, 2024-12-15), which shows the event recurs.
3. **Independent intake-failure evidence in the bounded buyer (CLM-031).** Clio's 2024 Legal Trends Report secret-shopper study, as reported by the Illinois Supreme Court Commission on Professionalism (2Civility, 2024-11-01): a third-party research firm contacted 500 US law firms as prospective clients. **33% answered the email (40% in 2019) and 40% answered the phone (56% in 2019).** This is the consequence of a broken or unowned intake handoff at law firms, measured by an outside firm. It does **not** measure automation failure, and Clio sells practice-management software. Clio's own page and the ABA article returned HTTP 403.
4. **Not usable.** Widely repeated "data silo" statistics (e.g. "72% of SMEs lose 10% of revenue," "84% of integration projects fail") trace to vendor blogs without primary sources. Failure stories on monitoring-tool pages ("You didn't notice for 4 days") are marketing scenarios, not cases.

### Strongest substitute found

A small category of **monitoring and repair products** now sells the reliability job directly: NotiLens (Zapier failure and "trigger silence" alerts within 60 seconds; free trial, price not shown), ScenarioTrace (free Make log analyzer, 2026-08-08), and Fix the Sync (done-for-you repair of broken Zapier and accounting syncs, updated 2026-09-06, prices by quote). Add Zapier's own auto-off notices and Make's deactivation emails. A viewer must answer why a small firm would pay for a sprint instead of a monitoring tool plus a $150 fix when something breaks (CLM-032).

## Claim-level source registry

All web claims accessed 2026-09-28 unless stated. No page was copied locally; URLs and locators are the snapshot. Trends values were read from the page's own data table in a browser session.

| Claim ID | Claim and status | Source and URL | Exact locator | Published / accessed | Source type / confidence | Relationship | Refresh by | Caveat |
|---|---|---|---|---|---|---|---|---|
| CLM-006 (refresh) | Directory still lists Platinum partners with 473 (Flow Digital), 438 (MercOlogy), 413 (Connex Digital), 335 (flowmondo) and 282 (GetUWired) reviews. **verified** | https://zapier.com/partnerdirectory | Platinum listing | current / 2026-09-28 | platform-displayed / medium | direct | 2026-12-28 | Reviews are engagements, not price |
| CLM-009 (refresh) | Zapier Pipedrive notice unchanged (updated 2026-05-29); adds that V2 "returns less data than the V1 API." The 31 July 2026 date has passed. **verified** | https://help.zapier.com/hc/en-us/articles/44170499172237-Action-required-Update-your-Pipedrive-workflows-before-the-V1-API-deprecation | Header date; "Important" note on V2 fields | 2026-05-29 / 2026-09-28 | vendor primary / high | direct | historical event; no refresh | Frequency across the market still unknown |
| CLM-015 (refresh) | Upwork and Fiverr still not observable: Upwork 403 and Cloudflare challenge; Fiverr 403 and CAPTCHA. Not bypassed. **not usable** | https://www.upwork.com/nx/search/jobs/?q=zapier%20fix ; https://www.fiverr.com/search/gigs?query=fix%20zapier | n/a | attempted 2026-09-28 | n/a | n/a | 2026-12-28 | Substitute sources used: CLM-023 to CLM-027 |
| CLM-016 (superseded by CLM-028) | Google Trends worked in a browser session on 2026-09-28. | see CLM-028 | — | — | — | — | — | — |
| CLM-023 | Ten Zapier Platinum partners: minimum spend $100–$1,000, median $250; all ten list fixing Zaps as a service; project bands from $100–$250 to $5,001–$10,000 or $10,001–$200,000; Flow Digital sells a 75-minute session at $297 covering "quick fixes, Zap troubleshooting." **verified as asking terms** | https://zapier.com/partnerdirectory/partner/{flow-digital, connex-digital, mercology, getuwired, flowmondo, xray, ashar-malik, solvaa, net3marketing, the-joinary} | "Minimum spend," "Project budget," services list on each profile | current / 2026-09-28 | platform-displayed seller terms / medium | direct (asking price) | 2026-12-28 | Asking terms of the best-placed incumbents; not transactions, not a sprint price |
| CLM-024 | n8n community single-fix offers: $40 (2026-09-18), $125 diagnosis (09-11), €150 (09-08), $149 (09-14), $150 (08-31); no buyer hire visible in sampled threads. One seller asks $1,500 audit / $3,000–$5,000 build sprint / $750–$1,500 monthly retainer (09-27). **verified as asking prices** | https://community.n8n.io/t/for-hire-fix-one-broken-n8n-workflow-us-40-fixed/314598 ; …/312782 ; …/311954 ; …/313363 ; …/310494 ; …/316944 (all under https://community.n8n.io/t/) | First post of each thread | 2026-08-31 to 2026-09-27 / 2026-09-28 | self-published seller posts / low-medium | direct (asking price) | 2026-12-28 | Many sellers are new entrants; no evidence of sales |
| CLM-025 | Fiverr "fix Zapier" gig titles show starting prices of $5–$350 (nine gigs; median $25). **qualified: search-index titles, pages not opened** | e.g. https://www.fiverr.com/andywingrave/fix-your-zapier-workflow ; https://www.fiverr.com/khanmehandi10/fix-your-zapier-zaps | Search-result titles | unknown index date / 2026-09-28 | search index / low | direct (asking floor) | 2026-12-28 | Index may be stale; starting prices are package floors |
| CLM-026 | Make Community buyer threads: buyer asks for maintenance because "if something in the chain breaks our team will be left helpless" (2026-08-13); another buyer is "open to paying for a short audit first" (2026-08-26); a third states "approximately USD $25 per hour" (2026-09-27). Seller quotes in reply: repair $125–$695 (median ~$295); audits $95–$400 (median ~$190), $20–$60/hr, $1,500 per five-day block. **verified as posted** | https://community.make.com/t/sos-inventory-automating-work-order/113328 ; https://community.make.com/t/need-make-airtable-expert-to-finish-mca-crm-automation/113875 ; https://community.make.com/t/wordpress-make-com-brevo-integration-expert/115942 | OP posts #1 and #9 (SOS); OP post and replies (MCA); OP reply of 2026-09-27 (Brevo) | 2026-08-12 to 2026-09-27 / 2026-09-28 | buyer and seller community posts / medium for existence, low for representativeness | direct (buyer request; asking price) | 2026-12-28 | Buyers are not all professional-service firms; no accepted price visible |
| CLM-027 | Freelancer.com buyer budgets: restoration contractor $750–$1,500 USD for a JobSight–Markate–Zapier job-monitoring system with escalation and stop conditions; freight brokerage $1,500–$3,000 USD fixed for a TMS–Zapier–M365 build that must "document all failures"; Canadian service business $250–$750 CAD for a Zapier-fed dashboard plus site refresh; AUD $25–$50/hr to take over a live Make automation. **verified as posted** | https://www.freelancer.com/projects/api-integration/automation-expert-for-restoration-crm ; https://www.freelancer.com/projects/ai-automation/automate-internal-operations ; https://www.freelancer.com/projects/zapier/ceo-dashboard-wordpress-booking-revamp ; https://www.freelancer.com/projects/ai-automation/senior-retell-make-com-developer | "Budget" line and project description | open on 2026-09-28 / 2026-09-28 | buyer-posted budget / medium | direct (buyer budget, build scope) | 2026-12-28 | Posted budgets are not accepted prices; Freelancer.com skews low; all are builds, not reliability sprints |
| CLM-028 | Google Trends, US, 5 years: `automation agency` peaked at 100 (week of 2026-05-10) and fell to 9–19 from late July 2026; `zapier not working` and `zapier consultant` ≈0; `zapier` half-year average 73.7 in 2026 H1 vs 32.5 in 2026 H2; control `quickbooks` fell less (≈98 to 58–76). **verified; direction since July 2026 not readable** | https://trends.google.com/trends/explore?date=today%205-y&geo=US&q=zapier%20expert,n8n%20agency,automation%20agency ; …&q=zapier%20not%20working,zapier%20consultant,automation%20consultant,zapier ; …&q=zapier,n8n,quickbooks | Interest-over-time data table; related queries | live / 2026-09-28 | platform index / medium for direction, none for volume | context (audience, seller-side) | 2026-12-28 | Relative index only; a series-wide step in July 2026 is likely; last week partial |
| CLM-029 | Zapier auto-turns-off a Zap at 95% errors over 7 days (grace periods only on Team and Enterprise); Make deactivates a scenario after a set number of consecutive errors, and after the first error when it starts with an instant trigger. **verified** | https://help.zapier.com/hc/en-us/articles/8496037690637-How-to-troubleshoot-errors-in-Zap-workflows ; https://help.make.com/scenario-settings | Auto-off rule; "Errors before deactivation" | 2026-05-29 and 2026-09-08 / 2026-09-28 | vendor primary / high | component (failure mechanism) | 2026-12-28 | Mechanism, not frequency or cost |
| CLM-030 | Make: Pipedrive API v1 modules must be replaced before 31 July 2026, after which "the scenarios using them will stop working." Zapier: an earlier batch of low-usage triggers and actions across twelve apps was deprecated on 2024-12-15. **verified** | https://help.make.com/pipedrive-api-v1-to-v2-transition-by-july-31-2026 ; https://help.zapier.com/hc/en-us/articles/31588469746829-Upcoming-deprecation-for-triggers-and-actions-for-migrated-apps | Page body | 2026-01-19; 2026-05-29 / 2026-09-28 | vendor primary / high | direct (failure event) | historical | Shows recurrence across platforms and years; not a rate |
| CLM-031 | Clio 2024 secret-shopper study: a third-party firm contacted 500 US law firms; 33% answered email (40% in 2019), 40% answered the phone (56% in 2019). **verified as reported** | 2Civility (Illinois Supreme Court Commission on Professionalism) — https://www.2civility.org/2024-clio-legal-trends-report-fixing-the-first-impression-problem-for-law-firms/ | Methodology and results paragraphs | 2024-11-01 / 2026-09-28 | independent secondary reporting a vendor-commissioned study / medium | adjacent (intake consequence at the bounded buyer) | 2027-03-28 | Measures responsiveness, not automation failure; Clio sells legal software; primary page returned 403 |
| CLM-032 | Monitoring and repair products sell the reliability job: NotiLens (Zapier failure and silence alerts), ScenarioTrace (free Make log analyzer, 2026-08-08), Fix the Sync (done-for-you sync repair, updated 2026-09-06). Prices not shown. **verified for existence** | https://www.notilens.com/zapier-workflow-failure-alerts ; https://scenariotrace.com/blog/make-scenario-deactivating-itself/ ; https://fixthesync.com/fix/zapier-stopped-working | Product pages | 2026 / 2026-09-28 | seller pages / low-medium | direct (substitute) | 2026-12-28 | Their failure stories are marketing, not cases |

## Adversarial pass (same agent, not independent)

1. **Does the price evidence help or hurt?** It hurts the base case. The package had no price; now it has a floor and a ceiling, and $3,500 sits above both. Fixes clear at $40–$500. Buyers post whole builds at $750–$3,000. The brief's own $2,500 sensitivity case, which leaves $640 a month after imputed labour, now looks like the optimistic end of what is observed, not the pessimistic one.
2. **Is "reliability" being bought separately anywhere?** Not in anything found. Reliability shows up as requirements written into build budgets (the freight broker, the restoration contractor) or as a maintenance question with no price (SOS Inventory). The one seller packaging an audit-sprint-retainer ladder shows no buyer. The Reviewer B objection — "a Zapier freelancer with a longer checklist" — is not answered by the market sample, and the sample leans toward it.
3. **Are these sources representative?** No. Community boards and Freelancer.com skew toward small budgets and global sellers. Directory minimums are floors set by incumbents. Upwork, the largest buyer-side source, stayed closed. The sample shows what is visible, not what small US professional-service firms typically pay.
4. **Is the supply crowding real?** Yes, and it matters to the viewer. Buyer threads draw 20–177 replies; Freelancer.com posts draw 61–159 bids. Entrants are underpricing each other in public. Differentiation by scope has to be shown to a buyer, not just asserted.
5. **Did the consequence evidence improve?** Some. Platform auto-off rules and a two-platform deprecation are primary and dated. The Clio study measures lost intake at law firms, from an outside research firm. But nothing yet measures how often an automated handoff fails at a small firm or what that costs. The best consequence number (33% email response) is about people and process, not automation.
6. **Does the Trends read support the audience?** No. It confirms the seller-side boom the brief described and adds a drop in July 2026 that cannot be cleanly read. Buyer-problem queries are too small to register.
7. **Is removing interviews being used to inflate anything?** It must not be. The consequence and price gaps that interviews would have filled stay scored as gaps. This record moves only on desk evidence.

## Viewer's first-test plan (replaces owner re-entry item 1)

The owner will not run interviews or pilots. Under the 2026-09-28 decision, these unknowns become the viewer's first test, taught in the episode as unknowns.

1. **Desk week (no buyer contact).** Pick one segment (e.g. small law or accounting firms using Clio or Pipedrive plus a scheduler plus QuickBooks). List the platform-change notices for those tools in the last twelve months. Write down the local price anchors: the Zapier directory minimums in your region, and three community or marketplace quotes for a comparable fix.
2. **Ten conversations.** Ask owners to screen-share the intake → scheduling → billing handoff. Record: failures in the last twelve months, how they found out, what it cost in hours or lost clients, who fixed it and what they paid.
3. **Price ladder.** Offer a paid diagnostic priced above the commodity fix (for example $250–$500, anchored on directory minimums and community audit quotes), credited toward a sprint. Quote the sprint in the observed buyer-budget band ($1,500–$3,000) with the reliability scope itemised, and state the $3,500 version as an alternative to learn whether the extra scope moves anyone.
4. **Substitute check.** In each conversation, ask whether a monitoring tool plus pay-per-fix would do. Record the answer.

Success signal: at least three owners name a handoff failure with a consequence they can count; two pay for a diagnostic above commodity fix prices; one accepts a sprint quote that covers tracked hours at the viewer's own rate.

Kill or redesign condition: after fifteen conversations no owner can name a costly failure; or buyers pay only commodity fix prices (below about $500) and decline any itemised reliability scope; or they choose monitoring plus pay-per-fix; or the sprint runs over 36 hours twice. Redesign option: sell a low-price diagnostic plus monitoring setup rather than a sprint.

## Effect on the package

- **Re-entry item 1** (ten owner interviews): removed as a condition by the owner decision; now the viewer's first test above.
- **Re-entry item 2** (asking-price sample and search attempt): **done as far as desk access allows.** Upwork and Fiverr remain closed to read-only access; substitute sources gave an asking-price sample (CLM-023 to CLM-026) and buyer budgets (CLM-026, CLM-027). Trends worked (CLM-028).
- **Price:** now has observed anchors, and they are **below** the modeled $3,500. The episode may state asking prices and posted budgets, labelled as such and attributed. It may not call any of them a market rate.
- **Consequence:** improved on mechanism (CLM-029, CLM-030) and on adjacent intake loss (CLM-031); still unmeasured for automation failure at the bounded buyer.
- **Substitute:** monitoring tools and cheap repair (CLM-032) are now named and must appear in the Canvas.

## Recommendation

**Re-score, not owner promotion review, and not park yet.** The re-score should follow a revision of the research brief's price hypothesis against the observed anchors, and should be done by a fresh Reviewer A / Reviewer B pair. Until then the disposition stays **continue research**.

Why not promotion review: the one new piece of price evidence is adverse to the brief's base price. Promoting a package whose central number is now contradicted by what it observed would present a modeled price the evidence does not support.

Why not park: the desk gaps named on 2026-09-03 are now largely closed, the consequence mechanism is stronger, and the remaining unknowns (what a firm pays for reliability, and how often a handoff fails) are field-only and now belong to the viewer's test. The candidate can teach an honest lesson — the fix is a commodity, reliability has to be proven as a separate purchase — if the price is reset.

Factors a re-score would examine (no score is changed here):

| Factor | Current (A / B) | Likely direction | Evidence |
|---|---|---|---|
| Buyer and costly problem (20) | 14 / 12 | **+1 possible** | Primary platform auto-off and deactivation rules (CLM-029); the same deprecation on two platforms and a recurring pattern (CLM-030); independent law-firm intake-loss study (CLM-031); buyer-voiced maintenance need (CLM-026). Frequency and cost for this buyer are still unmeasured, so no more than +1 |
| Audience demand and timing (15) | 10 / 9 | **no change; −1 arguable** | Search is now measured but seller-side, buyer-problem queries are ~0, and the recent direction is unreadable (CLM-028) |
| Analogy and evidence strength (15) | 11 / 11 | **no change** | New sources add a source family (buyer posts), but most are self-published and unrepresentative |
| Economics and capacity clarity (10) | 5 / 4 | **+1 only if the price is reset** against CLM-023 to CLM-027; **no change or −1** if the $3,500 base stands against contrary anchors | The rubric rewards input support, not attractive numbers. Observed anchors improve support; a base price above every observed budget does not |
| Go-to-market plausibility (8) | 5 / 4 | **no change** | Reachable buyer channels are now observed (community boards, Freelancer.com), but crowding is also observed (20–177 replies, 61–159 bids) |
| Offer and delivery (10), Narrative (10), POV (7), Canvas (5) | 8 / 8, 8 / 8, 4 / 3, 4 / 4 | **no change** | The substitute (CLM-032) sharpens the Canvas but does not change the score |

Expected re-score range: Reviewer A about 69–71, Reviewer B about 63–65. If the re-score lands below 65 again on the revised price, the next step is **park**.

## Snapshot

Page text was read by WebFetch and in a read-only browser session on 2026-09-28. No sign-in, form submission, CAPTCHA or bot challenge was attempted. No local copy of any page was saved; the URLs and locators above are the snapshot.
