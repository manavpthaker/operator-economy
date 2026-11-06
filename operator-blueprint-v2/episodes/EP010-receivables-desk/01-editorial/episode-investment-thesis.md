# Episode investment thesis: a receivables desk

Status: **draft** (research bench review candidate, 2026-11-06; owner decision pending at Gate E3I)

Template version: approved `operator-blueprint-v2-step1-v1.5`

Episode: EP010

Candidate ID: `candidate-2026-10-15-receivables-desk`

Gate position:

```text
Operator Canvas locked at E3 (owner, 2026-11-05, decision id 875)
-> this thesis drafted for E3I (owner decision pending: BUILD or PARK, and the spoken name)
-> narrative development not started
```

Every number below is an internal input until approved under `content-os/facts.md`. Locators are Step 0 claim IDs (research brief and amendment 01). No claims map exists yet; it is built at E5.

## Source freeze

| Source artifact | Role | Revision or status | SHA-256 | Hash verified |
|---|---|---|---|---|
| Step 0 handoff | Evidence and public-framing boundary | accepted 2026-11-02 (decision 563) | `06f35faa08bb9d241eca13c92d5666d7f9d93631def6102b0236a03dcea725e5` | yes, 2026-11-06 |
| Step 0 promotion record | Authorization and caveats | promoted 2026-10-26 (decisions 405, 474) | `09396836bbee0298fd4594f9b1422ce70dac41884930f86efae3920efc06f43f` | yes, 2026-11-06 |
| Step 0 research brief | Market, buyer, problem, parallels | bound | `77a4fb307f78d584bd47945e7cd342028b9eeae6b062a6cad77726d1d691c5cf` | yes, 2026-11-06 |
| Step 0 evidence amendment 01 | CLM-023, Invoice Butler | recorded 2026-11-02 | `25daa6ccb48711553584ef515d36cad484a57192780059effa4dffe25d6d7b81` | yes, 2026-11-06 |
| Step 0 scorecard and Canvas gate | Score 68, seven hard gates pass | bound | `5044d533d149e7f5343961166b392b3362649332668204b039bed6fc23d3b004`, `94939d503aa72d3338dfdad2bba52ae32ab464fb215a7c4522ef3cc0f19b962c` | yes, 2026-11-06 |
| Editorial contract | Viewer, promise, exclusions | approved 2026-11-02 (decision 683) | `7ecb06729cfe35c93a95fabca3930c78e4203bf0685f9fc8e801e261ef2ad9cd` | yes, 2026-11-06 |
| Locked Operator Canvas | Operating model | locked 2026-11-05 (decision 875) | `51e7e6aaef4e69840bb945fc55f40b4c5b0f257641de099d52a5a414573edb2e` | yes, 2026-11-06 |
| Claims map | Permitted claim language | not yet built (E5) | n/a | n/a |
| Content OS facts and voice | Universal truth and language | live 2026-11-06 | `facts.md` `ee9e04743380677eb47a000c002327d1e1cbba00ecd31e756f97180758bcfc79`, `voice.md` `c25e9ca20f7ffdb0d5ae9b26e5edd19c3733b9421ec19be4f25268fa8f7fcdbd` | yes |

Source changes or unresolved hash mismatches: none. The Canvas hash changed from the bound draft (`1be89127…`) only by its status line and lock block, as recorded in the owner-decision record.

Gate E3 status: **locked**

Operator-Canvas SHA-256: `51e7e6aaef4e69840bb945fc55f40b4c5b0f257641de099d52a5a414573edb2e`

E3 approving owner: Manav Thaker (brownbot approvals decision id 875)

E3 approval date: 2026-11-05

Research refresh due: 2027-01-15.

## Show thesis

How this episode serves the canonical show thesis: someone who has done AR or bookkeeping can own the part of late-invoice follow-up that software does not do, for about two dozen small firms, because agents now do the sending and sorting that a human desk pays staff for. The operator needs 19 to 24 firms in one niche, not a market share. The episode prices that desk against the free and $99 tools above it and the $599 human desks below it, and says the base case is a full-time job paying about $39.50 a working hour, modeled.

Professional experience the viewer can convert into an ownership advantage: AR, bookkeeping, office-management, or customer-account work, converted into being trusted to write to a firm's customers under its name.

Work AI makes more feasible for one operator: drafting per invoice, scheduling, allowed reminder calls, reading and sorting replies across many ledgers (CLM-008, CLM-020).

Costly problem large enough to support a narrow capture strategy: one vendor's survey reports 59% of small businesses with invoices 30-plus days overdue, up from 47%, and a mean of $17,700 owed among those waiting (CLM-001, CLM-002). Employers post part-time clerk jobs to chase past-due balances (CLM-004). Named small law firms pay a human desk (CLM-019, seller-published).

What must still be proven before this can be called sustainable: that owners outside law pay $400 or more to an unknown person when the tool is $99; that a client fits under about 1.5 hours a week; that the viewer's state allows it; that clients renew.

## Company naming lock

Internal working category: pre-collection accounts-receivable follow-up service for small B2B firms without AR staff

Short public category title: **Receivables desk for small firms**

Short spoken company name: **a receivables desk**

One-sentence public definition:

> It follows up a small firm's late invoices under that firm's name, and a person handles the ones a machine should not touch.

Longer internal operating description: one operator supervises agents that read a client's aging report and customer threads, send scheduled follow-ups and allowed reminder calls under the client's name, and sort replies into paid, promise, dispute, and missing document. The operator sets each client's rules and locked accounts, fixes document problems, makes relationship calls, passes disputes back the same day, returns accounts unpaid after 90 days on the desk, and owns a weekly aging report. Mature scope: about 24 firms in one niche. No threats, legal action, settlements, consumer debts, or handling of funds.

### Read-aloud naming test

Candidate line:

> Today, we are building a receivables desk: it follows up a small firm's late invoices under that firm's name, and a person handles the ones a machine should not touch.

- [x] Two familiar words.
- [x] Repeatable after one hearing.
- [x] Natural at conversational pace (bench read; the owner cold read is still required at E5V).
- [x] Definition names the buyer (small firm) and owned job (late invoices, the ones a machine should not touch).
- [x] Describes the mature desk, not the free aging sort or the first month.
- [x] Implies no result: it says "follows up", never "collects".
- [x] No stack of abstract nouns.
- [x] Leaves room for the paperwork tier and further niches.

Risk: "receivables" is accounting vocabulary. The intended viewer knows it; a general listener may not. The definition carries the meaning, so the name passes. Fallback if the owner prefers plainer words: "a late-invoice desk".

Naming decision: **approve** (bench recommendation; owner decision at this gate)

## Thesis stack

### Opportunity thesis

Why this company should exist now: sending a follow-up became nearly free. Invoice Butler gives the emails away, ARPilot charges $99 after ten free invoices, and Ramp added AR follow-up on 2026-09-22 (CLM-020, CLM-022, CLM-023). On one vendor's survey, late payment became more common over the same year (CLM-001). Small firms without AR staff still have nobody who owns the invoice after the reminder: the wrong PO number, the missing W-9, the customer who says they paid, the customer too important to nudge twice. Sellers already charge for that part separately, at $599 a month and up or on custom annual contracts (CLM-017, CLM-019, CLM-023). The company that belongs in the gap sells ownership of the list at a price a small firm can pay.

What this thesis does not claim: that the overdue share describes all small businesses; that the desk collects more money; that owners outside law pay for this; that the idea is new.

### Operator thesis

Why this specific viewer could have an advantage: the tools are open to everyone, including the buyer, so the advantage is judgment and trust. An AR person knows what a stuck invoice is stuck on, can tell a slow payer from an unhappy one, and knows when a customer needs a human. Being trusted to write under another firm's name is earned through a niche the viewer already worked in.

What the operator still has to learn or prove: the state check in their own and each client's state; selling, which most AR people have not done; whether their hours per client hold. Someone with no AR background has the weakest case, and the episode says so.

### Entry-wedge thesis

Why this is the responsible first paid way into the larger company: one niche, a state check, five offers at $400 to $500, and one client's past-due list worked for one paid month with hours logged. It costs about 40 hours and about $600, modeled, and tests the three things no desk research answers: whether owners allow outside contact, what they pay, and how many hours it takes.

Why this wedge is not the business ceiling: templates, dispute patterns, niche reputation, and any bookkeeper channel exist only after several clients. One client is a test of a 24-client desk.

Valid no-build, refuse, narrow, defer, or stop result inside the first offer: the free aging sort may end in "buy the $99 tool" or "every account would be locked, so no desk." Both are complete answers and no desk is sold. A small law firm that fits CollBox is told so.

### Affirmative build verdict

Investment recommendation: **BUILD** (bounded; bench recommendation, owner decision pending)

Verdict:

> **BUILD.** Build a receivables desk for small firms in one niche you already know: one person who owns every late invoice after the software sends the reminder, sold month to month at $400 to $500. Start with your state's collection law and one aging report marked by hand. Keep building only if two of five firms take a paid month at $400 or more, the client fits under about 1.5 hours a week, and the owner renews. If owners buy the $99 tool instead, stop.

Why the evidence is sufficient for an honest editorial recommendation: the job is real and paid for at two observed scales, employers paying clerks (CLM-004, low-medium confidence) and small firms paying a human desk (CLM-019, seller-published). The operator's cost fell because agents do the sending (CLM-020). The first test is one month, bounded in time and cash, with kill conditions stated before it starts. The base case clears a clerk-wage benchmark at 19 to 23 clients and leaves the failing price and the stress case failing (Canvas §10).

What remains unproven despite the BUILD verdict: buyer willingness to pay outside law, hours per client, state permission for the viewer, tool terms for third-party use, churn and ramp, bookkeeper behavior, Invoice Butler's undisclosed price. Score 68, advanced by owner override. The base case is $39.52 a working hour before tax and business costs, below EP009's $60-an-hour imputed cost of time.

BUILD here is an editorial recommendation to begin bounded construction, not proof of demand, pricing, recurring purchase, or income.

## Opportunity case

### Opportunity scale argument

Underlying costly behavior or responsibility: following up past-due invoices to other businesses, and resolving what stops them being paid.

Established budget, spend, or operating duty adjacent to the problem: part-time AR clerk wages (CLM-004); human desks at $599 to $1,199 a month (CLM-017, CLM-019); contingency agencies at about 25 to 35% after about 90 days (CLM-007, context only).

Why that adjacent pool is relevant: it is the same job the desk sells, paid for by the same kind of buyer.

Why it is not the exact market size of the proposed company: clerk postings and desk customers do not say how many owners would buy a one-person desk at $400, and no count of reachable firms exists.

Observed enterprise or institutional proof: Daylit sells AR agents to finance teams, reported 200-plus companies and a $110M round (CLM-008, reported claims; CLM-018). Upflow serves firms up to $10M invoiced revenue (CLM-018). Proves the job is worth automating at scale; does not prove small firms pay a person.

Observed platform or product-category proof: ARPilot $99, AccountsReceivable.ai $149 to $799, Chaser Compact $259, Invoice Butler free tier, Ramp AR (CLM-017, CLM-020, CLM-022, CLM-023). Proves the sending is cheap and contested.

Observed specialist, agency, or boutique proof: CollBox's dedicated US-based AR expert at $599 a month on a 12-month term plus $999 setup, with named small law-firm customers (CLM-005, CLM-019); Chaser Care at $1,199 (CLM-017); Invoice Butler Enterprise, custom (CLM-023). Proves some small firms pay a human for this, on sellers' pages.

Reachable operator-scale parallel: part-time AR clerks at $17 to $30 an hour (CLM-004, from search summaries). No one-person desk at disclosed economics was found.

Proposed business-of-one synthesis: one person with agents sells the human part of the specialist desk, below its price and above the tools, to firms in one niche.

Where the comparison is strong: same job, same buyer size, same flat-fee monthly form, same 90-day hand-back and locked-account features (CLM-005, CLM-019).

Where the comparison breaks: CollBox has a brand, staff, and law-firm focus; the operator has none of these. A clerk gives about four times the desk's modeled hours for a similar monthly cost.

Unknowns that prevent a demand, pricing, outcome, or livelihood claim: U001 to U009 in the Canvas.

Scale-proof pattern used: **combination** (same job across scales, fragmented buyer pool)

Scale-proof decision: **pass** (two observed paid layers: clerk wages and human-desk customers; the platform layer shows operating activity, not this buyer's spend)

### Qualified buyer universe

Customer decision affected: who follows up the late invoice after the free reminder, and at what price.

Purchase consequence large enough to matter: a past-due balance large beside the fee, and the customer relationship a bad message can damage.

Existing accountable budget or owner: the owner's own time, a part-time clerk, or nothing.

Evidence that customers use AI during discovery, comparison, shortlisting, or verification: not applicable; this desk is not about AI discovery. Buyers are already offered AR agents (CLM-020, CLM-022).

Conditions that make a buyer suitable: invoices other businesses on terms; regularly carries balances past 30 days that are large beside the fee; nobody whose job is follow-up; will let an outside person write under the firm's name; operates where the operator's state check passes.

Conditions that make a buyer unsuitable: bills consumers or is paid up front; has AR staff; so few or such sensitive customers that every account would be locked; wants accounts past the hand-back worked, or threats or legal pressure; is happy with a free tool; a small law firm that fits CollBox.

Operator experience, access, or buyer fluency required: AR or bookkeeping judgment, and one niche already known.

### Explanatory case set

All synthetic. None defines the company, market, denominator, or economics.

| Case | Market | Customer decision | Why the problem matters | What transfers to other markets | What does not transfer | Evidence class |
|---|---|---|---|---|---|---|
| 1 | A firm with many small accounts on net terms | Flat fee for volume work, and missing documents at scale | Many small stuck invoices nobody has time for | The sending-versus-owning split | Hours per client in that niche | ILLUSTRATIVE |
| 2 | A firm with five large customers it fears losing | Locked accounts, and when the honest answer is no sale | Relationship risk outweighs the balance | The valid no and the locked list | The fee case | ILLUSTRATIVE |
| 3 | A small law firm that could buy CollBox | When not to compete with an established human desk | A suitable service already exists | Refusing a sale builds trust | Anything about non-law demand | ILLUSTRATIVE, with CLM-019 as the observed seller |

Company definition without an example industry: a monthly desk that owns a small firm's late invoices after the software sends the reminder.

Viewer market-selection rule: start in the niche where you already worked, in states where the check passes.

### Normal system

How buyers currently handle the job: the owner sends a reminder from the invoicing tool, maybe a second, and then stops; or pays a part-time clerk; or, after about 90 days, hands it to an agency for a share (CLM-004, CLM-006, CLM-007).

Why reasonable buyers or operators use that system: the owner knows the customers, a clerk is cheap per hour, and an agency costs nothing until it collects.

What the current system does well: the owner protects relationships; free reminders handle forgetful payers.

Buyer voice, anecdote only (read through Xpoz, 2026-11-06, not a claim and not proof): in an r/smallbusiness thread of 2026-08-17 (<https://www.reddit.com/r/smallbusiness/comments/1vqix7z/>), owners describe a fixed reminder ladder that is easy to set and a next step that depends on the customer's history, with one noting that context sits across the invoicing tool, CRM, and email, and another that several customers had lost the invoice PDF. Others say a fixed ladder plus a phone call is enough, which supports the "buy the tool" answer. One B2B owner has an office manager contact late payers daily. Candidate for the claims map as buyer voice only.

### Market change

Observed change: AR agents and free senders reached small firms in 2026 (CLM-020, CLM-022, CLM-023); the overdue share rose from 47% to 59% on one survey (CLM-001).

Approved claim IDs and locators: CLM-001, CLM-020, CLM-022, CLM-023.

Who feels the change: owners, who now get the reminder for free, and clerks, whose sending work is cheaper.

Why it matters now: the price of sending is near zero, so only the work around the send can be sold.

What is synthesis rather than observed fact: that the remaining work is a sellable service at $400.

### Costly problem

Buyer trying to accomplish: get paid for finished work without damaging the customer.

Failure, friction, or missed opportunity: follow-up stops after the first reminder; invoices stuck on documents or disputes sit unowned (CLM-006, low confidence; Invoice Butler and Chaser sell these as separate human work, CLM-017, CLM-023).

Operational, financial, strategic, or customer consequence: cash tied up (mean $17,700 among those waiting) and credit-card reliance associated with overdue invoices, 38% versus 21% (CLM-002, CLM-003; association, not cause).

Evidence that the problem is material: one vendor's survey and employers paying clerks for the job.

What is not yet known: how often each stuck-invoice cause occurs (U006), urgency for any one buyer, and willingness to pay a person.

### High-end or established proof

Established company or delivery pattern: CollBox's human desk for small law and accounting firms (CLM-005, CLM-019); Chaser Care (CLM-017).

What this proves: some small firms pay a flat monthly fee for a person to follow up their invoices, with locked accounts and a 90-day hand-back.

Why the parallel is valid enough to use: same buyer size, same job, same form.

What it does not prove: demand outside law, demand at $400 from an unknown person, renewal, or any collection result. CollBox's own outcome figures are not used.

### Missing ownership

What tools already handle: sending, scheduling, reminder calls, reply sorting, payment matching.

What responsibility still falls between them: the dispute, the missing document, the relationship call, the locked account, and one person answerable for the list.

Who absorbs the consequence: the owner, or nobody.

Why this could be a company rather than a feature: the remaining work needs judgment and trust per client, which a tool does not sell and a small firm cannot staff.

Plainspoken opportunity ruling: the sending is gone as a business. The owning is the business, if owners will pay for it.

### Comparable-business ladder

| Scale | Company or provider | Buyer | Related paid job | Evidence of operation or spend | What it proves | What it cannot prove |
|---|---|---|---|---|---|---|
| Enterprise or institutional | Daylit, Upflow | Finance teams | AR follow-up agents | Reported customers and funding (CLM-008, CLM-018) | The job is worth automating | Small-firm spend |
| Platform or product category | ARPilot, AccountsReceivable.ai, Chaser, Invoice Butler, Ramp | Small firms | Automated sending and sorting | Published prices (CLM-017, CLM-020, CLM-022, CLM-023) | Sending is cheap and contested | That anyone pays a person |
| Specialist or agency | CollBox, Chaser Care | Small law and accounting firms | Human follow-up | Seller prices and named customers (CLM-005, CLM-017, CLM-019) | Some small firms pay a person | Demand outside law or at $400 |
| Reachable operator parallel | Part-time AR clerk | Small employers | Chasing past-due balances | Job postings, $17 to $30 an hour (CLM-004) | Employers pay a person for the job | That they would buy it as a service |

Two observed paid layers: specialist desk customers and clerk wages. The ladder passes, at the confidence stated.

## Evidence ladder

| Evidence role | Claim IDs and locators | Evidence class | What it establishes | What it does not establish | Spoken boundary needed | Status |
|---|---|---|---|---|---|---|
| Market change | CLM-001, CLM-020, CLM-022, CLM-023 | OBSERVED | Sending is cheap; overdue share rose on one survey | All small businesses; cause | "one vendor's survey" | approved for E4 use |
| Costly buyer problem | CLM-001 to CLM-003, CLM-006 | OBSERVED (one survey; low-confidence roundup) | The problem is common and costly on that survey | Frequency of each cause | "one survey", mean not median | approved |
| High-end or established proof | CLM-005, CLM-017, CLM-019 | OBSERVED as seller terms | Some small firms pay a human desk | Outcomes; non-law demand | "on the seller's own page" | approved |
| Reachable small-operator parallel | CLM-004 | OBSERVED, low-medium | Employers pay clerks for the job | Service demand | "job postings" | approved |
| Buyer purchase behavior | CLM-019 | OBSERVED as seller-published | Named law firms pay | Anyone else pays | seller-chosen customers | approved |
| Delivery or component capability | CLM-008, CLM-020 | OBSERVED as seller claims | Agents send and sort | Quality, safe delivery | seller claims | approved |
| Proposed company synthesis | Canvas §4, §6 | MODELED | A coherent desk design | That it works | "an editorial label; no verified example" | approved as model |
| Entry offer | Canvas §4, §12 | MODELED | A bounded test | Demand | "modeled" | approved as model |
| Economics and capacity | Canvas §10 | MODELED | Arithmetic on stated inputs | Income | `Modeled scenario, not observed performance or an earnings forecast.` | approved as model |
| Go-to-market path | Canvas §8 | UNKNOWN | Hypotheses | Any channel works | "untested" | approved as unknown |

Load-bearing evidence gap: whether owners outside law pay a person $400 or more when the tool is $99 (U001).

Disposition: **none**. The gap is the viewer's first test under the coaching standard, scored as a gap in Step 0.

## Big case to small capture

What the larger market or established provider proves: the job is real and paid for, and sending is no longer worth paying for.

What it only suggests: that the human part is a separate purchase small firms would make.

What the operator is not being asked to build, replace, or win: an AR platform, a collection agency, or CollBox's law-firm market.

Small part of the problem the business of one can own first: one niche's late-invoice lists, after the reminder.

Why that capture is economically meaningful if the modeled assumptions hold: 19 to 23 clients at $400 clear a $57,600 clerk-wage line before tax (Canvas §10).

Bridge from the large case to the reachable operator case: the specialist desk's form, at a lower price, made possible by agents doing the staffer's sending.

Evidence or paid test needed to prove that bridge: two of five firms in one niche take a paid month at $400 or more, then renew.

Annual engagements required by the modeled owner case: 19 to 24 active clients, plus about 6 replacements a year at a modeled 25% churn.

Maximum delivery capacity: 24 clients at 1.25 hours; 30 only at 1 hour; 15 at 2 hours.

Qualified conversations required during the first validation cycle: five offers in one niche.

Observed acceptance rate: unknown until tested.

Reachable prospect pool needed after an acceptance rate exists: computed only after the viewer's first offers.

Why no conversion rate or market share is invented: the QuickBooks share gives no count of reachable firms, and no observed rate exists.

Reason this is a focused company rather than a diminished version of the larger opportunity: it owns the one part the platforms leave and the specialist desks price above small firms.

## Opportunity-to-blueprint narrative contract

Target opportunity-pitch share: 55 percent. Allowed: 52 to 58 percent. Target operator-blueprint share: 45 percent.

The opportunity act establishes the free-sending change, the stuck invoice, the clerk and desk spend, the ladder, the missing owner, and the desk before the free aging sort and first month appear.

Reasoned exception: none.

## Mature business of one

Short company promise: every late invoice has an owner and a known state, every week.

Economic buyer: the owner or office manager of a small B2B firm without AR staff.

Beneficiary: the buyer; the buyer's customers receive the messages.

Owned result or responsibility: the late-invoice list after the reminder.

Primary acceptance measure: at each weekly report, every past-due invoice in the baseline is in exactly one state, and no locked account or paid invoice was contacted. The collected balance is tracked, never promised, because one client in 30 days cannot show cause.

Core delivery loop: read the list, send, sort replies, operator clears the queue, disputes back the same day, unpaid accounts return after 90 days, weekly report.

Ongoing duty the mature company may own: the list for about 24 firms in one niche.

Scope invariant: pre-collection only, in the client's name, no threats, settlements, consumer debts, or funds. A person owns the list.

Why one accountable operator can own the initial model: one client at about 1.25 modeled hours a week, every message read for two weeks.

Work that remains outside the business: legal action, agency collection, payment plans, portals and vendor paperwork beyond a W-9 (a later tier).

Capacity boundary: 30 delivery hours a week; 24 clients at 1.25 hours.

What would force premature hiring: portals at volume, firms with hundreds of open invoices, heavy calling.

What must be true to support the owner sustainably: $400 or more per client, hours under about 1.6, renewals that outrun churn, and income from elsewhere through a modeled 16-month ramp.

## Entry wedge and conditional expansion

Entry wedge: one client's past-due list worked for one paid month, with hours logged.

First economic buyer and purchase trigger: a firm owner in the viewer's niche with a 30-plus-day balance large beside the fee, after a free reminder failed.

First paid transaction: one month at $400 to $500, due up front, no setup fee, no term.

Useful result even with a no-build decision: the free aging sort shows which lines a tool can handle.

Buyer acceptance event: four weekly reports with every invoice in a known state and no wrong send; the owner chooses to renew.

Completion boundary: each invoice ends paid, dispute handed back, or returned after 90 days.

What this first engagement proves: that one owner allowed it, paid it, and how many hours it took.

What it does not prove: demand across the niche, renewal at scale, any collection effect.

| Stage | Offer or responsibility | Buyer proof required before advancing | Operator capability required | Economics proof required | Stop condition |
|---|---|---|---|---|---|
| Entry | One client, one paid month | None; the start | Rules sheet, templates, hours log, state note | Hours logged | State check fails, or no firm allows contact at any price |
| Expansion 1 | 3 to 5 clients in the niche | Two of five offers accepted at $400 or more; one renewal | Reusable templates, dispute patterns | Under 1.5 hours per client | Above about 1.6 hours at $400, or nobody renews |
| Expansion 2 | Up to 24 clients | Several renewals at the price | Referral path, if observed | Section 10 rerun on observed inputs | Churn outruns 6 selling hours a week |
| Mature scope | Fewer, larger clients at a higher fee, or a paperwork tier | Clients pay more for documents and calls | Paperwork tier | Higher fee holds | A seller offers a human specialist at $500 or less at comparable scope |

Expansion is conditional. Each stage needs a new buyer decision.

## Operator advantage and responsibility split

Relevant operator background: AR, bookkeeping, office management, customer accounts.

Domain judgment: what an invoice is stuck on; slow payer versus unhappy customer; when a call beats an email.

Access, relationships, or credibility: past employers, vendors, and customers in one niche; bookkeeper contacts.

Why buying the same tools is not the advantage: the buyer can buy them too, for $99.

### AI responsibility

Work AI may compress: drafting, scheduling, allowed reminder calls, sorting replies, the first draft of the weekly report.

Required review: every message for a client's first two weeks; then each new template's first send and everything sorted as unclear.

AI actions prohibited without human judgment: messages to locked accounts; anything after a dispute, lawyer's letter, bankruptcy or hardship mention, or settlement request; any threat.

### Software responsibility

Stable work software may execute: sequences, stop-on-paid, logs, the report format.

Manual fallback: send from the client's mailbox by hand and build the report from the aging export.

### Human responsibility

Judgment the operator retains: locked accounts, tone per client, documents, relationship calls, the state check.

Permissions the buyer retains: every account, the mailbox, the ledger, pausing sends with one message.

Quality, exception, failure, recovery, and communication ownership: the operator, including stopping and telling the owner the same day after a wrong send.

Accountability that cannot be delegated: answering to the owner for every message sent in the firm's name.

Specialist help allowed: a lawyer for the state check and engagement letter. No staff.

## Go-to-market construction

First reachable segment: firms in one niche where the viewer has worked, in states that pass the check.

Buyer signal or trigger: a visible 30-plus-day balance; an owner who hates sending these; a bookkeeper who keeps flagging the same list.

How the operator identifies the first prospect set: past employers, vendors, and customers in the niche, bookkeeper contacts, a local trade group (hypotheses, UNKNOWN).

Credibility artifact: the one-page rules sheet and a synthetic sample report.

First conversation: the free aging sort, about 30 minutes, which may end in "buy the tool."

First paid ask: one month at $400 to $500, no term.

Reason a buyer can say yes before trusting the mature company: one month, no setup, locked accounts, a reading period, and a one-message pause.

Expected objections: "I don't want anyone writing to my customers." "Software is $99." "My bookkeeper could do this."

Responses inside the approved evidence: locked accounts and the reading period; agreement that the tool is sometimes right, plus what it leaves; the bookkeeper may be a referrer or a rival (CLM-021).

Acquisition channel: existing relationships in one niche.

Why reachable for this operator: the viewer already knows owners in that niche.

Evidence still needed: sales time per client, acquisition cost, acceptance rate.

## Modeled economics and required share

`Modeled scenario, not observed performance or an earnings forecast.` All inputs are from the locked Canvas §10.

### Assumptions

| Input | Low case | Base case | High case | Evidence class | Approved source or modeling reason |
|---|---:|---:|---:|---|---|
| Price per month | $300 | $400 | $500 | MODELED | Between tools and CollBox (CLM-005, CLM-019, CLM-020) |
| Active clients | 20 | 24 | 30 | MODELED | 30 delivery hours / hours per client |
| Delivery hours per client per week | 1.5 | 1.25 | 1 | MODELED | Unmeasured |
| Support, admin, state work | 4 h a week | 4 h | 4 h | MODELED | Time budget |
| Tool seat per client per month | $149 | $99 | $99 | OBSERVED price; MODELED use | CLM-020 |
| Operator tools and acquisition overhead | $10,800 a year | $10,800 | $10,800 | MODELED | Canvas §10 |
| Selling effort | 6 h a week | 6 h | 6 h | MODELED | No conversion rate |
| Owner labor allowance | $57,600 a year | $57,600 | $57,600 | MODELED | Top clerk posting rate across 1,920 hours (CLM-004), bench-chosen |
| Delivery capacity | 20 | 24 | 30 | MODELED | Capacity equation |

```text
24 clients x $400 x 12 = $115,200 modeled gross revenue (base)
24 x $99 x 12 + $10,800 = $39,312 modeled direct cost before owner labor
30 delivery hours / 1.25 hours = 24 modeled maximum clients
```

Modeled contribution before owner compensation and tax: base $75,888 ($39.52 a working hour); low $25,440; high $133,560; stress at 2 hours $43,380. Year one with a ramp: $24,417.

Modeled contribution after the declared owner-labor allowance: base $18,288; low and stress negative.

Most sensitive assumption: whether owners pay $400 or more to an unknown person, then hours per client.

Stress case: 2 hours per client caps the desk at 15 clients and $43,380.

Customers required to meet the $57,600 requirement: 19 at $400 with a $99 seat; 23 with a $149 seat; 15 at $500. At $300 it needs 29 to 38, which does not fit at 1.25 hours.

Defined reachable buyer set: qualified firms in one niche, in permitted states, that the viewer can reach through existing relationships.

Share implied: not computed; no count of that set exists.

Why the problem is large and costly enough for that share to be worth testing: employers pay clerks for it, named small firms pay a desk, and one survey reports it is common. None of this shows these buyers will pay this operator.

Evidence needed to show the required share is reachable: two of five firms take a paid month at $400 or more, then renewals.

Why this remains a sustainability test: every input is an assumption with its arithmetic shown, and the failing price and stress case stay failing.

Required public qualification: the disclosure line above; contribution figures never without inputs; "a full-time job, not a side income."

## The hard part

Hardest operating constraint: hours per client. Above about 1.6 hours at $400, the desk pays less than a clerk.

Why AI or software does not remove it: the hours are the human part, which is the product.

Hardest distribution constraint: selling a $400 person when the tool is $99, with no brand and no observed channel.

Hardest trust constraint: owners letting an outsider write to customers about money.

Failure mode most likely to destroy the economics: owners agree with the diagnosis and buy the tool.

Capability the operator must develop: selling, and the state check.

Early warning: the first five free sorts end in "buy the tool."

Mitigation: sell only to firms where the sort shows stuck documents and relationship accounts.

Kill or park condition: none of five takes a paid month at $400 or more; or the viewer's state requires a licence they will not obtain; or a seller offers a human specialist at $500 or less at comparable scope (the 2026-10-22 park condition).

## Construction plan

Every target is a modeled operating commitment until completed. This is the viewer's first test, not owner field work.

### First 30 days

Business asset to construct: the state note, rules sheet, follow-up ladder, sample report, and hours log.

Reachable segment and prospect set: five qualified firms in the viewer's niche.

Buyer conversations: five free aging sorts.

Credibility artifact: rules sheet and synthetic sample report.

First paid wedge: one month at $400 to $500.

Delivery boundary to document before sale: locked accounts, hand-back, no threats, the pause rule, the wrong-send route.

Record: hours, costs, exceptions, every send, owner decisions.

Success signal: two of five take a paid month; four reports with every invoice in a known state; under 1.5 hours; no wrong send; the owner renews.

Failure signal: no firm allows outside contact at any price, or all prefer the tool; hours above about 1.6; a repeated wrong send.

Day-30 decision: continue building / revise (niche, price, or scope) / return / stop.

Maximum time and cash at risk: about 40 hours and about $600, modeled.

### Days 31 through 90

First funded work: three to five clients.

Operating evidence: the hours log replaces the 1.25-hour assumption; renewals replace the churn guess.

Second buyer condition: two acceptances at $400 or more.

Expansion proof before adding scope: paying owners ask for documents or portal work.

Support and capacity boundary: 30 delivery hours, 4 support hours.

Economics to recalculate: section 10 on observed hours, price, and seat cost.

What must not be built yet: a website, a multi-client system, a referral program, a contract term, a paperwork tier.

Day-90 decision: continue / narrow / revise / stop / park.

## Narrative commitment

Opportunity-half commitment: free sending, the stuck invoice, clerk and desk spend, the ladder, the missing owner, and the desk, in that order. Estimated share: 55 percent.

Build-half commitment: AR judgment as the advantage, the AI and human split, the free sort and first month, the weekly loop, the first niche, 24 clients and the $300 failure, the state line, the ladder of proof, the first 30 and 90 days, BUILD. Estimated share: 45 percent.

Balance check:

- [x] Removing the opportunity half leaves a recipe with no reason to pay a person over a tool.
- [x] Removing the build half leaves an AR market explainer.
- [x] The free sort and first month appear only after the desk is understandable.
- [x] The first month is an entrance, not the thesis.
- [x] The niche practice is conditional.
- [x] The verdict says what to build and how to begin.

## Claims and authorization boundary

- [x] Every factual statement traces to a Step 0 claim ID or is labeled model, unknown, or anecdote.
- [ ] Every number has an approved claim ID and locator before script use. Pending the E5 claims map.
- [x] Parallels used only for the role their evidence supports.
- [x] Adjacent evidence not upgraded into demand for this desk.
- [x] Component capability not presented as buyer value or an outcome.
- [x] Modeled figures stay modeled.
- [x] BUILD is an editorial recommendation, not proof.
- [x] The company thesis and the first-offer "buy the tool" answer are distinct.
- [x] No unresolved factual, legal, permission, source, access, guest, or evidence-integrity blocker. The state line is a viewer precondition, stated as a non-lawyer's reading.
- [x] No unsupported claim added.
- [x] No episode URL.
- [x] Nothing first-person is claimed for Manav.

Gate E3I approval authorizes narrative development only. It does not approve a public claim, script, narration, visuals, release, or distribution.

## Gate E3I readiness check

Bench check, not an owner or independent review.

- [x] Gate E3 locked; Canvas hash matches.
- [x] Source hashes recorded and verified.
- [x] Show thesis tied to this operator, problem, and desk.
- [x] Name and spoken name pass the read-aloud test (bench read).
- [x] Four theses distinct and consistent.
- [x] Recommendation is BUILD, bounded.
- [x] Normal system, change, problem, established proof, missing ownership present.
- [x] Evidence ladder states limits.
- [x] Big case connects to a focused capture without a market-size claim.
- [x] Mature desk larger than the first month and operable by one person.
- [x] Expansion conditional.
- [x] Advantage is judgment and trust, not tools.
- [x] Responsibilities explicit.
- [x] First-customer path attemptable.
- [x] Economics count labor, tools, acquisition, support, capacity, required clients.
- [x] Required share named as a test.
- [x] Hard part, failure mode, stop condition explicit.
- [x] 30- and 90-day plans build while testing.
- [x] 55/45 balance committed.
- [x] Claims boundary clear.
- [ ] Named human approval. Pending.

## Bench review notes

Same agent ran both passes; not independent.

Evidence pass: all figures match the locked Canvas and the bound claims. The Reddit thread is new, anecdote only, read through Xpoz, and enters no number. No seller page was re-read this run; the 2026-11-05 run re-read them via Exa.

Adversarial editorial pass:

- The strongest case against BUILD is in the buyer's own words: several owners in the thread say a fixed ladder plus one phone call solves it. That is the "$99 tool" objection, and the free sort must be allowed to end there.
- The base case pays $39.52 an hour before tax and business costs, below EP009's $60 imputed cost of time. The episode cannot call this a good job; only "clears a clerk's wage at 19 or more clients, modeled."
- A clerk gives about four times the hours for similar money. The desk's case rests on agents doing that difference, unmeasured.
- Without the human-layer claim, nothing remains to sell. Remove CollBox and the specialist layer and the ladder falls to one observed paid layer and fails. The episode is worth making only because that layer is on sellers' own pages.
- PARK would be defensible. The bench recommends BUILD because the test is cheap, bounded, and has kill conditions, and because the episode's honest lesson ("sending is worthless; price the part a person owns, and stop if they buy the tool") holds either way.

## Gate E3I approval

Decision: pending owner

Investment recommendation: BUILD (bench recommendation) / PARK (owner alternative)

Gate E3I status: not reached

Proposed short public category title: Receivables desk for small firms

Proposed short spoken company name: a receivables desk

Proposed one-sentence definition: It follows up a small firm's late invoices under that firm's name, and a person handles the ones a machine should not touch.

Proposed mature-company description: one person and their agents owning the late-invoice lists of about 24 small firms in one niche, month to month at $400 to $500.

Proposed entry wedge: one client's past-due list for one paid month, after a state check and a free aging sort.

Proposed BUILD verdict: as stated under "Affirmative build verdict".

Unresolved caveats that do not block narrative development: U001 to U009 except U008 (resolved at E3); claims map pending.

Approved by: pending

Approval date: pending

Calculate the SHA-256 after this approval record is complete. Store it in every dependent narrative artifact and the editorial lock. Do not place a self-hash inside this file.
