# Operator Canvas: a receivables desk

Status: **draft** (research bench review candidate, 2026-11-05; owner decision pending at Gate E3)

Template version: approved `operator-blueprint-v2-step1-v1.5`

Episode: EP010

Candidate ID: `candidate-2026-10-15-receivables-desk`

Editorial contract SHA-256: `7ecb06729cfe35c93a95fabca3930c78e4203bf0685f9fc8e801e261ef2ad9cd`

Step 0 handoff SHA-256: `06f35faa08bb9d241eca13c92d5666d7f9d93631def6102b0236a03dcea725e5`

Step 0 evidence amendment 01 SHA-256: `25daa6ccb48711553584ef515d36cad484a57192780059effa4dffe25d6d7b81` (CLM-023)

Evidence class for the overall model: **adjacent synthesis**

Labels: `OBSERVED` (approved evidence), `PARALLEL` (adjacent business or mechanism), `MODELED` (transparent scenario on stated assumptions), `UNKNOWN` (important, not established). Locators are Step 0 claim IDs from the research brief and amendment 01. Every number is an internal input until approved under `content-os/facts.md`.

## What this Canvas changes from the approved contract

The contract listed four Canvas issues. Resolving them changes three contract figures. These take effect only if the owner locks this Canvas; the approved contract is not edited.

| Contract figure | This Canvas | Why |
|---|---|---|
| About 30 clients | **24 clients** | 40 hours a week less 10 for selling, admin, and support leaves 30 for delivery. At 1.25 hours each, that is 24 |
| $300 to $500 fee | **$400 to $500**; $300 is recorded as the failing price | At $300 the desk misses the owner-pay line unless hours fall to about 1 per client (section 10) |
| About $114,000 base contribution; $45,000 to $63,000 thin case | **$75,888 base; $25,440 low** | Step 0's $21,000 tool line had no published price behind it. One paid seat per client is now the base |

## 1. Operator

Who could credibly run this business: someone who has done bookkeeping, accounts receivable, office management, or customer-account work. They can read an aging report (the list of who owes what and how late), tell a slow payer from an unhappy one, and supervise email and phone agents. `PARALLEL`: research brief, "Required skills"; CLM-004.

Relevant experience, access, or advantage: AR judgment, being trusted to write under another firm's name, and one niche they already know. Tools are open to everyone, including the buyer, so tool access is no advantage.

What the operator does personally at the beginning: the state check, every client's rules and locked accounts, the review queue, missing documents, relationship calls, same-day dispute hand-offs, the weekly report, and all selling.

What the operator should not need to be: a lawyer, a licensed collector (unless their state requires it), a software builder, or a person who handles client funds.

Not a fit: someone with no AR background. This is the weakest case, and the episode says so. Also anyone who wants to resell a tool.

## 2. Buyer and beneficiary

Economic buyer: the owner or office manager of a small US firm that invoices other businesses on terms and has no AR staff. `OBSERVED` that such firms exist and that some small law firms pay a human desk: CLM-001 to CLM-003, CLM-019 (seller-published). `UNKNOWN` outside law.

Day-to-day user: the owner, who reads the weekly report and answers hand-backs.

Ultimate beneficiary or customer: the buyer. The buyer's customers receive the messages and can be harmed by a bad one.

Buyer trigger: a balance past 30 days that is large beside the fee, a free reminder that did not move it, or a bookkeeper's aging report that raises the question. `MODELED`: inferred, not surveyed.

Qualified-buyer rule: invoices other businesses on terms, regularly carries balances past 30 days that are large beside the fee, has nobody whose job is follow-up, and will let an outside person write to customers under the firm's name.

Unsuitable-buyer rule: bills consumers or is paid up front. Already has AR staff. Has so few or such sensitive customers that every account would be locked. Wants accounts past the hand-back window worked, or wants threats or legal pressure. Is happy with a free tool. Operates where the operator's state check fails. A small law firm that could buy CollBox should usually be told so.

## 3. Costly problem

Job the buyer is trying to accomplish: get paid for finished work without damaging the customer relationship.

Current failure or friction: follow-up stops after the first reminder. The invoice is often stuck on a wrong PO number, a missing W-9, or a customer who says they paid, and nobody is paid to fix it. `OBSERVED` weakly: CLM-006 (low confidence). `PARALLEL`: Invoice Butler and Chaser sell these same items as separate human work (CLM-017, CLM-023, seller copy). How often each cause occurs is `UNKNOWN`.

Operational, financial, or strategic cost: one vendor's survey reports 59% of small businesses with invoices 30-plus days overdue, up from 47%, and $17,700 owed on average among those waiting (a mean). 38% of firms with overdue invoices report growing credit-card reliance against 21% without, an association and not a cause. `OBSERVED`, one vendor: CLM-001 to CLM-003.

Why the buyer acts now rather than later: `UNKNOWN` for any single buyer. The market change is that sending became nearly free (CLM-020, CLM-022, CLM-023), which removes the excuse without solving the stuck invoice.

Current alternatives and their limits (seller terms):

| Alternative | Price | Leaves undone |
|---|---|---|
| Invoice Butler free tier | $0 | Disputes, documents, calls (CLM-023) |
| ARPilot | Free on 10 invoices, then $99 a month | A person. It pauses collections on a dispute (CLM-020) |
| AccountsReceivable.ai | $299 monthly or $149 billed yearly; with AI calls $799 or $399 | A person (CLM-020) |
| Chaser Compact | $259 | A person, unless Care is added (CLM-017) |
| Part-time clerk | $17 to $30 an hour for 5 to 25 hours a week (low-medium confidence) | Needs management; more hours than the desk gives (CLM-004) |
| CollBox | $599 on a 12-month term or $729 monthly, plus $999 setup | Sold to law and accounting firms (CLM-005, CLM-019) |
| Chaser Compact plus Care | $1,199 | Price (CLM-017) |
| Invoice Butler Enterprise | Custom, annual, paid in advance | Price undisclosed; never estimate it (CLM-023) |
| Contingency agency | About 25 to 35% after about 90 days (low confidence) | Late stage, off-brand (CLM-007) |

Not claimed: any collection-rate, DSO, or recovered-cash result, including CollBox's figures.

## 4. Offer

Plain-English offer: for a flat monthly fee, one person and their agents work your past-due invoices under your name until each is paid, disputed, or handed back, and you get a report every week.

What is included: scheduled follow-ups and allowed reminder calls; replies sorted into paid, promise, dispute, and missing document; fixing document problems (PO number, W-9, resent invoice); relationship calls on accounts the owner permits; same-day dispute hand-off; hand-back after 90 days on the desk (CollBox's window, CLM-019); a weekly aging report.

What is excluded: threats, legal action, settlements, payment plans negotiated for the client, consumer debts, handling funds, accounts already placed for collection, customer portals and vendor paperwork beyond a W-9 (a later tier).

Engagement shape: managed service, month to month.

First paid transaction: one month at a flat fee, no setup fee and no term. Fee is due at the start of the month. The owner chooses at day 30 to renew or stop.

Valid no: the free aging sort (section 8) comes before any sale. "A free tool will do" and "every account would be locked" are complete answers, and no desk is sold.

Time to first meaningful result: the first sorted list and report in week one. Any change in the balance is `UNKNOWN`.

What the owner gets at $400 that a $299 tool does not buy: a named person who fixes the stuck document, makes the call a machine should not make, keeps locked accounts locked, passes disputes back the same day, and answers when a message goes wrong. If the owner does not value those, the tool is the right purchase. `MODELED`.

Evidence label: `PARALLEL` for the format (ANA-003, ANA-004, ANA-010). `MODELED` for one person with agents at this price. No operator is verified selling this at disclosed economics.

## 5. Buyer result

Result being purchased: every past-due invoice has an owner and a known state.

Primary acceptance measure: at each weekly report, every past-due invoice in the baseline sits in exactly one state: paid, promise with a date, dispute handed back, missing document in progress, handed back, or locked. The month is accepted when the owner holds four such reports and no locked account or paid invoice was contacted.

Why not the collected balance: one client over 30 days cannot show the desk caused a fall. It is tracked and reported, and never promised.

Baseline required: the aging report on day one, with the 30-plus-day balance and the locked list.

Leading indicators: share of invoices with a known state, age of open documents, same-day dispute rate, operator hours per client.

Lagging indicators: 30-plus-day balance, days sales outstanding, renewal.

What the operator can influence but not guarantee: whether customers pay.

Completion boundary: each invoice ends at paid, dispute handed back, or returned after 90 days. Leaving is clean, as in section 6.

## 6. Delivery system

### Before delivery

Qualification and intake: apply the buyer rules, and confirm the state check covers the operator's state and the client's. Agree tone, locked accounts, who signs, and call permissions, in writing.

Required access, data, permissions, or integrations: read-only accounting access; a delegated mailbox or shared address on the client's domain; written client permission to contact its customers under its name. Client owns every account.

### Core workflow

1. Weekly, the agent reads the aging report and open threads. Owner: agent. Output: updated list.
2. Agent drafts and sends scheduled follow-ups on unlocked accounts, stopping when an invoice is paid. Owner: agent, rules set by operator. Output: sends log.
3. Agent sorts replies into paid, promise, dispute, missing document, or unclear. Owner: agent. Output: review queue.
4. Operator clears the queue: fixes documents, makes permitted calls, and reads anything unclear. Output: resolved items.
5. Disputes go to the owner the same day, with the thread attached. Owner: operator. Output: hand-back.
6. Past 90 days on the desk, the account returns to the owner with its history. Owner: operator. Output: returned account.
7. Weekly report to the owner. Owner: operator. Output: the acceptance record.

### Quality and exception handling

Human review: all messages for the first two weeks of a client, then the first send of each new template and everything sorted as unclear. An account the owner marks sensitive is locked.

Failure route: on a wrong send (a paid invoice, a locked account, a bad tone), stop sends for that client, tell the owner the same day, apologize in the owner's preferred form, find the cause, and restart only with the owner's yes.

Recovery and revocation: the owner can pause sends with one message, effective the same business day. On exit, access is removed within one business day, and the owner keeps the thread history and templates.

Escalation boundary: any threat of a lawsuit, bankruptcy mention, hardship claim, settlement request, or lawyer's letter goes to the owner the same day and the agent stops on that account (CLM-008 design pattern).

Coverage: one person is a single point of failure. During planned time off the agent pauses judgment-dependent sends, and owners are told in advance. `MODELED`.

### After delivery

Handoff, reporting, support, or renewal: renewal is a month-to-month choice on the fourth report. Support runs through one named person, inside the 10 non-delivery hours.

## 7. Capabilities and stack

| Capability | Required job | Possible tool class | Named example, if approved | Human responsibility | Cost status |
|---|---|---|---|---|---|
| Ledger read | Know what is open and paid | Accounting connector | QuickBooks or Xero through the AR tool | Confirm paid-invoice stop works | Included in seat |
| Follow-up and sorting | Draft, schedule, classify replies | Agent AR tool, one seat per client | ARPilot $99 or AccountsReceivable.ai $149 (CLM-020) | Rules, templates, unclear replies | Public pricing; third-party use terms `UNKNOWN` |
| Reminder calls | Scripted reminders where allowed | AI voice in the seat, or the operator | ARPilot voice (CLM-020) | Calling-rule check, relationship calls | Public pricing |
| Mailbox | Send as the client | Delegated or shared address | Client's own | Client permission | Client-owned |
| Work queue and report | Weekly state of every invoice | Spreadsheet or light database, language model | None named | Writes and signs the report | Modeled $150 a month |

Data and privacy boundary: client customer and invoice data stays in client-owned or per-client accounts, kept apart between clients, and is used only for that client.

Vendor dependency: seller prices and terms can change (refresh by 2027-01-15). ARPilot's page names QuickBooks Online or its REST API, so a Xero client likely needs another seat at $149 or more.

Manual fallback: the operator can send follow-ups by hand from the client's mailbox and build the report from the aging export.

## 7A. Business-of-one design

Work AI compresses, accelerates, or makes newly feasible: drafting per invoice, scheduling, reminder calls, reading and sorting replies across many ledgers. A human desk pays staff for this. `PARALLEL`: CLM-005, CLM-008, CLM-020.

Work software can standardize: sequences, stop-on-paid, logs, the report's format.

Judgment, relationships, permissions, quality, and accountability the operator retains: which accounts to lock, tone per client, the dispute hand-off, the missing document, the relationship call, the state check, answering to the owner.

Bounded specialist or contractor help allowed: a lawyer for the state check and engagement letter. No staff.

Work that would force premature hiring: portals and vendor paperwork at volume, firms with hundreds of open invoices, or heavy calling.

Why one accountable operator can sell and deliver the initial offer responsibly: the first test is one client at about 1.25 modeled hours a week, with every message read for two weeks.

Maximum customer or delivery load before quality, safety, or support fails: **24 clients at 1.25 hours each. 30 is allowed only if logged hours hold at 1 hour. At 2 hours the ceiling is 15.** `MODELED`, unmeasured.

## 8. Go-to-market path

First reachable segment: firms in one niche where the operator has already worked, in states that passed the check. The first niche comes from the operator's own background and is never universalized.

Buyer signal or trigger: a visible 30-plus-day balance, an owner who says "I hate sending these," a bookkeeper who keeps flagging the same list.

How the operator finds the first 25 prospects: past employers, past vendors and customers in the niche, the operator's own bookkeeper contacts, and a local trade group. `UNKNOWN`: hypotheses, not observed channels (ANA-006; ANA-009 is seller-described).

Credibility artifact: the one-page rules sheet (locked accounts, hand-back, no threats) and a synthetic sample report.

First conversation or diagnostic: the free aging sort. With permission, mark each past-due line as something a free tool can handle or something that needs a person. It takes about 30 minutes, and its honest answer may be "buy the tool." It is distinct from the desk.

Low-risk entry offer: one paid month at $400, no term, no setup fee.

Expected objections: "I don't want anyone writing to my customers" (locked accounts, reading period). "Software is $99" (true, and sometimes the right answer). "My bookkeeper could do this" (also true, and the bookkeeper may be a rival or referrer).

Expansion or referral path: bookkeepers who see aging reports. They may refer, or they may add the tool and keep the client (CLM-021). No referral record exists. `UNKNOWN`.

Required sales activity: comes from capacity, not a funnel. Reach 24 clients, then replace about 6 a year at a modeled 25% churn, on 6 selling hours a week. No conversion rate is assumed.

## 9. Entry wedge and expansion ladder

Short public category title: Receivables desk for small firms

Short spoken company name: **a receivables desk** (final at Gate E3I)

One-sentence public definition: It follows up a small firm's late invoices under that firm's name, and a person handles the ones a machine should not touch.

Precise internal operating description: see the editorial contract. Held outside first-listen narration.

Mature company promise: about 24 firms in one niche, each with a known state for every late invoice, one accountable person, and reusable templates and dispute patterns.

Aspirational business: a niche receivables practice, possibly fed by bookkeepers.

Entry wedge: one niche, a state check, five offers at $400 to $500, and one client's past-due list worked for 30 days with hours logged.

Why this wedge is commercially and operationally tractable: it costs a month and one client, and it tests what nothing on a desk can answer: whether owners allow it, what they pay, and how many hours it takes.

Scope invariant that survives expansion: pre-collection only, in the client's name, no threats, settlements, consumer debts, or funds. A person owns the list.

| Stage | Offer or capability | Buyer proof required before advancing | Operator capability added | Stop condition |
|---|---|---|---|---|
| Entry | One client, one paid month | None; this is the start | Rules sheet, templates, hours log | State check fails, or no firm allows contact at any price |
| Next | 3 to 5 clients in the niche | Two of five offers accepted at $400 or more; under 1.5 hours per client per week; one renewal | Reusable templates, dispute patterns | Hours above 1.6 per client at $400, or nobody renews |
| Then | Up to 24 clients | Several renewals at the price; hours log holds | Referral path if observed | Churn outruns selling hours |
| Redesign | Fewer, larger clients at a higher fee, or portal and paperwork work | Clients pay more for documents and calls than for sending | Paperwork tier | A seller offers a human specialist at or below the desk's price |

What remains outside the initial offer but inside the aspirational business: bookkeeper referrals, further niches, portal submissions and vendor paperwork.

Required public qualification: "receivables desk" is an editorial label, and the one-person version has no verified example at disclosed economics.

## 10. Economics model

All forward-looking figures are scenarios, not expected earnings. `Modeled scenario, not observed performance or an earnings forecast.`

Pricing basis and rationale: above the tools and below the published human desks. `MODELED`. Selling the human layer is the only reason to exceed a tool. For scale: a clerk at 5 hours a week costs about $368 to $650 a month (CLM-004) and gives about four times the desk's modeled 1.25 hours, so the desk's case depends on agents doing the remainder, which is unmeasured. Price is the viewer's first test.

```text
customers x price x 12 = modeled gross revenue
customers x seat x 12 + operator tools + acquisition and overhead = modeled direct cost
30 delivery hours a week / hours per customer = modeled maximum active customers
```

Time budget: 40 hours a week for 48 weeks is 1,920 hours a year. 30 are delivery. 6 are selling. 4 are admin, support, and state work. `MODELED`.

| Assumption | Low case | Base case | High case | Evidence label | Source or reasoning |
|---|---:|---:|---:|---|---|
| Price per month | $300 | $400 | $500 | `MODELED` | Between tools and CollBox (CLM-005, CLM-019, CLM-020) |
| Delivery hours per client per week | 1.5 | 1.25 | 1 | `MODELED` | Step 0 range; unmeasured |
| Active customers at 30 hours | 20 | 24 | 30 | `MODELED` | Capacity equation |
| Seat per client per month | $149 | $99 | $99 | `OBSERVED` as seller price; `MODELED` as this use | CLM-020 |
| Operator tools | $1,800 a year | $1,800 | $1,800 | `MODELED` | Queue, report, mailbox admin |
| Acquisition and overhead | $9,000 a year | $9,000 | $9,000 | `MODELED` | Step 0 midpoint; state costs unknown |
| Modeled churn | not modeled | 25% a year | not modeled | `UNKNOWN` | Assumption; about 6 replacements at 24 |
| Selling effort | 6 h a week | 6 h a week | 6 h a week | `MODELED` | Time budget; no conversion rate |

| Case | Gross | Seats | Tools and overhead | Contribution before owner pay and tax | Per working hour (1,920) |
|---|---:|---:|---:|---:|---:|
| Low: 20 x $300, $149 seat | $72,000 | $35,760 | $10,800 | **$25,440** | $13.25 |
| Base: 24 x $400, $99 seat | $115,200 | $28,512 | $10,800 | **$75,888** | $39.52 |
| Base with $149 seat | $115,200 | $42,912 | $10,800 | $61,488 | $32.02 |
| High: 30 x $500, $99 seat | $180,000 | $35,640 | $10,800 | **$133,560** | $69.56 |
| Stress: 2 hours, 15 x $400, $99 seat | $72,000 | $17,820 | $10,800 | **$43,380** | $22.59 |

Ramp (year one, base price): adding a net 1.5 clients a month reaches 24 in month 16, an assumption. Year one is 117 client-months: $46,800 gross, less $11,583 in seats and $10,800 fixed, for **$24,417**. A viewer needs other income through the ramp.

Upside not counted: AccountsReceivable.ai lists a Scale plan for "Multiple entities and ledgers" at $949 a month billed yearly ($1,899 monthly) on its pricing page (read via Exa, 2026-11-05). Whether it covers unrelated client firms is not stated. If it did, tools would fall to $11,388 a year and base contribution would rise to $93,012. This is not a Step 0 claim and is not for public use. The viewer asks for the quote.

Modeled contribution before owner compensation and tax: $75,888 in the base case, for a full-time job.

Break-even condition: 3 clients at $400 and a $99 seat cover the $10,800 fixed line ($3,612 per client per year).

Cash-timing or working-capital risk: low if the fee is due up front and seats bill monthly. Yearly-billed seats ($1,788 each at $149) prepay a client who may leave in a month. Do not use them until clients renew.

Most sensitive assumption: **whether owners pay $400 or more to an unknown person**, then hours per client.

Modeled owner-compensation requirement: $57,600 a year before tax, which is the top clerk posting rate of $30 an hour across 1,920 hours (CLM-004, low-medium confidence). A desk that pays less is worse than the job it replaces. This line is generous to the desk: a clerk may have benefits and pays no business expenses or self-employment tax. A bench-chosen benchmark. EP009's $60-an-hour imputed cost of time would need $115,200, which only the high case clears.

Customers or transactions required to meet that modeled requirement:

| Fee and seat | Clients needed | Delivery hours at 1.25 | Fits 30 hours? |
|---|---:|---:|---|
| $300, $149 | 38 | 48 | **No** |
| $300, $99 | 29 | 36 | **No** |
| $400, $149 | 23 | 29 | Yes |
| $400, $99 | 19 | 24 | Yes |
| $500, $99 | 15 | 19 | Yes, with room |

At $400 and a $99 seat, the 19 clients fit only while hours stay below about 1.6 per client per week. That is why the contract's 1.5-hour success signal holds.

Share of the reachable buyer set implied by that customer count: not computed. The QuickBooks share gives no count of reachable firms. The requirement is 19 to 24 firms in one niche in permitted states, plus replacements.

Why the underlying problem is large and costly enough for that share to matter: employers pay clerks for the job (CLM-004), named small firms pay a desk (CLM-019), and one vendor survey reports the problem is common (CLM-001). None of it shows these buyers will pay this operator.

Evidence or test needed to show the share is reachable: two of five firms in one niche taking a paid month at $400 or more, then renewals.

Why this remains a sustainability model rather than an income promise: every input is an assumption with its arithmetic shown, and the failing price and the stress case are left failing.

Required public disclosure: `Modeled scenario, not observed performance or an earnings forecast.` No contribution figure appears without its inputs. It is a full-time job, not a side income.

## 11. Risks and failure modes

| Risk or assumption | Why it matters | Early warning | Mitigation | Kill condition | Evidence label |
|---|---|---|---|---|---|
| Owners will not pay $400 for the human part | The whole business | Owners agree and buy the $99 tool | Free sort shows what the tool leaves; sell fewer, better-fit firms | None of five takes a paid month at $400 or more | `UNKNOWN` |
| Owners will not let an outsider write to customers | No service exists without it | Every account marked locked | Reading period, locked list | No firm allows it at any price | `UNKNOWN` |
| A funded seller takes the human layer down-market | Removes the gap | Disclosed human specialist at or below the desk's fee | Win on niche and trust; refresh prices | Human specialist at $500 or less at comparable scope, per the 2026-10-22 park condition | `OBSERVED` as direction: CLM-023 |
| State law reaches the desk | Illegal or registered work | Florida and Washington plausibly require it (non-lawyer reading) | State check before first client; ask someone who can answer | State requires a licence the viewer will not obtain | `OBSERVED` text: CLM-009 to CLM-016 |
| Hours exceed the model | Capacity and pay collapse | First client above 1.5 hours | Log hours from day one; narrow scope | Above about 1.6 hours at $400 once templates settle | `MODELED` |
| Wrong send to a customer | Reputation; client's relationship | Paid invoice or locked account contacted | Read everything for two weeks; stop-on-paid test first | Repeated wrong sends after fixes | `MODELED` |
| Churn or slow ramp | 24 clients never arrive | Under 1 net client a month by month 6 | Stay employed through ramp; renew on reports | Selling hours cannot replace churn | `UNKNOWN` |
| Tool terms bar third-party use, or prices change | Seat line moves | Vendor refuses a multi-client setup | Client holds the seat; quote first | No lawful per-client seat under $149 | `UNKNOWN` |
| Bookkeeper keeps the client | Blocks the channel and competes | Bookkeepers add the tool | Offer them the hand-off; do not rely on referrals | Niche already served this way | `PARALLEL`: CLM-021 |
| Calling rules | AI calls can create exposure | Client wants heavy calling | Operator's check; default to a person's call | Viewer cannot confirm the rule | `UNKNOWN` |
| Concentration | Few clients at start, one person | One client is most revenue | Month-to-month planning, other income | Not applicable in test | `MODELED` |

## 12. First 30-day construction and validation plan

This is the viewer's first test, not owner field work.

Question being tested: will a firm let this person write to its customers, pay $400 or more, and fit under 1.5 hours a week?

Business asset or capability constructed before testing: the state note, rules sheet, follow-up ladder, sample report, and hours log.

First paid wedge to offer: one month at $400 to $500, no term.

Smallest credible test inside that construction: five offers in one niche; one client's list worked for 30 days.

Target participants: five qualified firms the viewer can reach through existing relationships.

What must be built before testing: the state check, written permission language, and the stop-on-paid test on synthetic invoices.

What must not be built yet: a website, a multi-client system, a referral program, or a contract term.

Success signal: two of five take a paid month; every invoice has a known state in four reports; hours under 1.5; no wrong send; the owner renews.

Failure signal: no firm allows outside contact at any price, or all prefer the tool; hours above about 1.6; a repeated wrong send.

Decision at day 30: continue building / revise (change niche, price, or scope) / return / stop.

Maximum time and cash at risk: about 40 hours and about $600, modeled: one month's seat, mailbox, and an optional paid legal question.

The balance is logged and is not a success signal by itself, since one client in 30 days cannot show cause.

Days 31 to 90: take three to five clients. Replace the hours figure with the log, get a first renewal, and rerun section 10 on observed inputs. Add nothing to the offer until a paying owner and the log say so.

## 13. Unknowns and contradictions

| ID | Unknown or contradiction | Why it matters | Owner | Resolution path | Blocks lock? |
|---|---|---|---|---|---|
| U001 | Do owners outside law pay $400 or more to an unknown person? | The whole business | Viewer | Test later, first test | No, safe test question |
| U002 | Hours per client | Capacity and pay | Viewer | Test later, hours log | No, safe test question |
| U003 | Does the viewer's state allow it? | Legal precondition | Viewer | State check before first client | No, safe test question; blocks that viewer's first client |
| U004 | Third-party terms and multi-client price for seats | Tool line | Viewer | Quote | No, safe test question |
| U005 | Churn and ramp | Time to 24 clients | Viewer | Test later | No, later-stage question |
| U006 | Causes of stuck invoices, how often | The human layer's size | Viewer | Free sorts | No, safe test question |
| U007 | Invoice Butler's price | Where the gap sits | Viewer | Do not estimate; viewer may ask for a quote | No, the script states only that it is undisclosed |
| U008 | Contract says 30 clients and $300 to $500; Canvas says 24 and $400 to $500 | Script must use one set | Owner | Canvas lock supersedes these contract figures | **Owner decision at this gate** |
| U009 | Do bookkeepers refer an outside desk? | Later growth | Viewer | Later | No, later-stage question |

No other current E3 blocker. No narrative or scenario substitutes for an unresolved operating decision.

## Pitch-deck and episode coverage map

| Pitch question | Canvas source | VO obligation | Visual opportunity | Downloadable detail | Coverage status |
|---|---|---|---|---|---|
| Why now? | §3 | Sending went to about free while the overdue share rose on one survey | Price ladder from $0 up | Citations, caveats | complete |
| What is the problem? | §3 | Nobody owns the thread after the reminder | The wrong-PO reply sitting in an inbox | Full evidence | complete |
| What is the company? | §4, §9 | Spoken name, plain definition, who owns what | Company boundary | Internal description | complete |
| Who buys and who does not? | §2 | Qualified and unsuitable rules | Fit filter, three synthetic owners | Criteria | complete |
| Why is the opportunity large enough? | §3, §10 | Clerks, named firms, one survey, and what they do not prove | Comparable-layer ladder | Sources and limits | complete |
| Why can one operator win? | §1, §7A | Judgment and trust, AI's job, and the no-AR-background warning | AI and operator split | Capacity boundary | complete |
| What is sold first? | §4, §5 | One paid month, its acceptance, the valid no | Sample report, invoice states | Terms | complete |
| How is it delivered? | §6, §7 | The weekly loop, the locked list, the same-day hand-off | Process loop, ladder | SOP, tool options | complete |
| How are customers reached? | §8 | First niche, free sort, paid ask, no invented funnel | First-25 path | Scripts, objections | complete |
| Can it support one operator? | §10 | **24 not 30, $300 fails, full-time job, inputs named** | Capacity gauge, price table | Full model | complete |
| What can break it? | §11, §13 | Owners buy the tool; state line; seller moves down | Failure tree, state check | Full register | complete |
| What happens first? | §12 | State check, then one aging report marked by hand | 30/90 timeline | Test plan | complete |

Audio-only rule: buyer, problem, company, first offer, human responsibility, economics boundary, principal risk, and first action are all carried in VO.

Visual-truth rule: no diagram may show a recovered balance as a result, estimate Invoice Butler's price, or collapse the ladder. Every economics visual carries its inputs and "modeled." A state visual says "a non-lawyer reading" and is not a map of all fifty states.

## Public Canvas layer

Short public category title: Receivables desk for small firms

Short spoken company name: **a receivables desk**

One-line plain definition: It follows up a small firm's late invoices under that firm's name, and a person handles the ones a machine should not touch.

Precise internal operating description, retained outside first-listen narration: see the editorial contract.

Buyer: a small firm that bills other businesses on terms, has no AR staff, and will let an outsider write under its name.

Problem: the reminder goes out, the invoice is stuck on something a reminder cannot fix, and nobody owns it.

Offer: a flat monthly fee, month to month, for working the past-due list.

Result: every late invoice has an owner and a known state, reported weekly. No collection result is promised.

Delivery loop: read the list, send, sort replies, a person clears the queue, disputes go back the same day, unpaid accounts return after 90 days, report.

Stack by capability: accounting read access, an agent AR tool per client, the client's mailbox, a work queue.

AI role: drafts, schedules, places allowed reminder calls, sorts replies.

Human judgment retained: locked accounts, tone, documents, relationship calls, disputes, the state check, accountability.

Business-of-one boundary: about 24 clients at 1.25 modeled hours each.

First-customer path: a niche the viewer knows, a free aging sort, one paid month.

Entry wedge: one client for 30 days, with hours logged.

Aspirational destination: a niche practice with reusable templates and patterns.

Proof required before expansion: two of five take a paid month at $400 or more, hours under 1.5, one renewal.

Economics disclosure: `Modeled scenario, not observed performance or an earnings forecast.`

Modeled livelihood requirement and required customer count: 19 to 23 clients at $400 to clear a $57,600 line before tax, a full-time job. At $300 it does not fit at 1.25 hours.

Reachable-share assumption: about 24 firms in one niche in permitted states. No denominator and no conversion rate.

First construction step and test: check the state, then mark one aging report by hand.

Biggest risk: the owner buys the $99 tool.

## E3 readiness check

Bench check, not an owner or independent review.

- [x] First economic buyer and purchase trigger identifiable (trigger inferred, labeled)
- [x] Short public and spoken name understandable on first listen and not carrying the operating definition
- [x] Plain definition implies no established category, demand level, or unearned result
- [x] Mature company distinct from the entry offer
- [x] First paid transaction (one month) distinct from the recurring desk
- [x] Buyer result has baseline, primary acceptance measure, acceptance event, and influence boundary
- [x] Build, narrow, defer, no-build, and completion decisions explicit (free sort may end in "buy the tool")
- [x] Delivery defines access ownership, judgment, tests, failure routing, recovery, revocation, documentation, and handoff
- [x] First-customer test names segment, prospect set, paid decision, success signal, failure signal, kill condition
- [x] Economics include price, labor, tools, acquisition, support, capacity, and a stress case
- [x] AI role and retained human judgment identified exactly
- [x] One operator can deliver the entry offer inside a declared capacity boundary with no hidden team
- [x] Livelihood case counts owner compensation and converts it to a required client count, and records the failing price as failing
- [x] Required share compared with a reachable buyer set without treating a total count as demand
- [x] Sustainability presented as a condition to test, not a promised or typical result
- [x] Expansion stages require new proof
- [x] Every unknown classified
- [x] No narrative, analogy, demo, or revenue scenario substitutes for an unresolved operating decision
- [x] Every pitch-deck question has a VO, visual, and Canvas treatment
- [x] Audio-only episode retains every load-bearing element
- [x] Visual coverage adds comprehension without inventing certainty

## Canvas lock

Decision: pending owner

Bench recommendation: lock, including 24 clients, $400 to $500, one paid seat per client in the base, and the full-time statement, in place of the contract's 30 clients and $300 to $500.

Approved by: pending

Approval date: pending

Calculate the SHA-256 after this approval record is complete. Store it in dependent artifacts and the editorial lock; do not place a self-hash inside this file.
