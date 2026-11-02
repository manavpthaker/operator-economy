# Editorial contract: a receivables desk

Status: **draft** (research bench review candidate, 2026-11-02; owner decision pending at Gate E2)

Template version: approved `operator-blueprint-v2-step1-v1.5`

Episode: EP010

Candidate ID: `candidate-2026-10-15-receivables-desk`

Step 0 handoff record and SHA-256: `handoff.md` / `06f35faa08bb9d241eca13c92d5666d7f9d93631def6102b0236a03dcea725e5`

Step 0 evidence amendment and SHA-256: `00-intake/02-research/candidate-2026-10-15-receivables-desk-amendment-01.md` / `25daa6ccb48711553584ef515d36cad484a57192780059effa4dffe25d6d7b81` (CLM-023)

Research cutoff: 2026-10-22 (bound package); CLM-023 re-read 2026-11-02

Every number below is an internal input until approved under `content-os/facts.md`.

## Viewer

Primary viewer/operator: Someone who has done bookkeeping, accounts receivable, office management, or customer-account work. Can read an aging report (the list of who owes what and how late), can tell a slow payer from an unhappy one, and can set up and supervise email and phone agents.

Audience situation: employed and exploring / between roles and rebuilding income

What this person already knows: What a past-due invoice looks like from the inside. That the reminder is the easy part. That the invoice is often stuck on a wrong PO number, a missing W-9, or a customer who says they already paid. They may have heard an owner ask for help actually collecting.

What this person is trying to decide or accomplish: Whether that skill can be sold as a monthly service to small firms now that AI tools do the sending, what to charge, and whether their state allows it.

Starting belief or confusion: Either "AI makes this easy, I'll resell a tool to small businesses" or "AI just killed this job." Both treat the job as sending messages.

Practical capability they should have after the episode: Sort one aging report into what software can handle and what needs a person. Write the follow-up ladder, the locked-accounts list, and the hand-back rules. Place a fee on the public price ladder and run the arithmetic with their own hours. Read their own state's collection law, or ask someone who can, before contacting anyone's customers. Decide build, test, or reject.

## Episode job

One-sentence working promise: AI already sells the invoice chaser for free to $299 a month. Here is the part it does not do, what a person could charge for that part, and the legal line to check before the first client.

Episode-specific show string in plain language: A desk you can build for small firms that are owed money and have nobody whose job it is to go and get it.

Concrete situation suitable for a cold open: An illustrative owner with one invoice 47 days late. The software already sent the reminder for free. The customer's accounts payable person replied that the PO number is wrong. That reply has sat in the owner's inbox for two weeks, because fixing it means an awkward email to a good customer and nobody is paid to send it. Stated as illustrative, not a real firm.

Specific operator or business payoff the cold open will tease before the silent sting: The software did its whole job and the money still did not move. Something in that gap is worth paying for, and there is a specific price it has to clear.

Mechanism, proof, and final thesis the cold open must withhold: The human-layer thesis, the price ladder, the state line, the company name, the BUILD verdict.

Normal system the viewer needs explained before the central thesis: How small firms bill other businesses on terms. What an aging report is. Who follows up today: usually the owner, sometimes a part-time clerk paid by the hour. What the free reminder does. Why agencies take accounts only after about 90 days and take a share. What the QuickBooks survey reports about how often this happens.

Central argument: **Software has taken the price of sending a follow-up to about zero, so nobody can be paid for sending. What is left is the wrong PO, the dispute, the customer too important to nudge twice, and one person accountable for the list. A small firm cannot staff that, and sellers already charge for it. The open question is whether one person with agents can sell it below the human desks and above the tools, in a state that allows it. That is the viewer's test.**

Narrative question: When software will chase an invoice for free, what is left for a person to sell, and can one person sell enough of it?

Evidence and context required before the central argument can be stated: the QuickBooks figures, attributed as one vendor's survey (CLM-001 to CLM-003). Clerk postings as old-way spend (CLM-004). CollBox's human desk and named customers (CLM-005, CLM-019). The tool prices (CLM-017, CLM-020, CLM-023).

Why this matters now: QuickBooks reports the overdue share moved from 47% to 59% in a year (one vendor's survey). Meanwhile AR agents are now sold to small firms, Ramp added AR follow-up on 2026-09-22, and Invoice Butler gives the emails away (CLM-001, CLM-020, CLM-022, CLM-023). The same change that lowers the operator's cost also arms the operator's rival.

What is at stake for the buyer, operator, or market: For the buyer, cash, reliance on credit cards (an association in the survey, not a cause), and customer relationships that a bad message can damage. For the operator, a business that exists only if the human part is worth more than the software, and a legal exposure that varies by state.

The concrete business being taught: A flat-fee monthly desk that works past-due invoices under the client's own name until each is paid, disputed, or handed back, with one person accountable.

Short public category title: **Receivables desk for small firms**

Short spoken company name: **a receivables desk** (final at Gate E3I)

One-sentence plain definition: It follows up a small firm's late invoices under that firm's name, and a person handles the ones a machine should not touch.

Precise internal operating description: One operator supervises agents that read a client's aging report and customer threads, send scheduled follow-ups and allowed reminder calls under the client's name, and sort replies into paid, promise, dispute, and missing document. The operator sets each client's rules and locked accounts, fixes document problems, makes relationship calls, passes disputes back the same day, returns accounts unpaid after a fixed window, and owns a weekly aging report. No threats, legal action, settlements, consumer debts, or handling of funds.

Opportunity thesis: what changed, why the problem matters, and what company belongs in the gap: Sending became nearly free while late payment grew more common on the one survey read. Firms without AR staff still have nobody who owns the thread after the reminder. The company that belongs in the gap sells ownership of that thread at a price small firms can pay. Other sellers already sell it at $599 and up, or on custom annual contracts.

Operator thesis: why this viewer has a credible advantage beyond tool access: Tools are available to everyone, including the owner. The advantage is AR judgment: knowing what a stuck invoice is stuck on and when a customer needs a human. Add being trusted to write under another firm's name, and a niche learned well enough to reuse its patterns. This is the weakest thesis if the viewer has no AR background, and the episode says so.

How AI makes this viable or more viable for one accountable operator: Agents draft, schedule, place reminder calls where allowed, and sort replies across many ledgers. A human desk pays a staffer for that work, and the published ones start near $599. The desk's modeled 1 to 1.5 operator hours per client per week depends on this and is unmeasured.

Human judgment and accountability AI does not replace: Which accounts to lock. Tone per client. The dispute hand-off. The missing document. The relationship call. Stopping when a customer has paid. The state check. Answering to the owner when a message goes wrong.

What "sustainable" means in this episode without promising income: About 30 clients at a modeled $400: $144,000 gross, about $114,000 contribution before owner pay and tax in the base case. With one tool seat per client at the low $300 fee, about $45,000 to $63,000. Delivery alone is 30 to 45 modeled hours a week at 30 clients, before selling, so the top of the range is a full-time job, not a side income. Modeled scenario, not observed performance or an earnings forecast.

Reachable-share thesis: how a small share of a large, costly problem could support the modeled business: The operator needs about 30 firms, in one niche, in states it may serve. The QuickBooks share does not yield a count of reachable firms, so no denominator and no conversion rate are used. Thirty comes from capacity and price, not from a funnel.

Underlying established budget, spend, or responsibility: Part-time AR clerks ($17 to $30 an hour for 5 to 25 hours a week, low-medium confidence, from search summaries). Human desks (CollBox $599 a month on a 12-month term or $729 month to month, plus $999 setup; Chaser Compact plus Care $1,199). Contingency agencies after about 90 days (context only).

Enterprise, platform, specialist, and operator-scale parallels: Enterprise and platform: Daylit and Upflow for finance teams, Ramp AR. Small-business tools: Invoice Butler free tier, ARPilot $99, Chaser Compact $259, AccountsReceivable.ai $149 to $799. Specialist: CollBox, Chaser Care, Invoice Butler Enterprise. Operator scale: the part-time clerk and the proposed one-person desk. All prices are seller terms with read dates.

Scale-proof pattern: **combination** (same job across scales, with a fragmented buyer pool)

What the scale argument proves: That the job is real, that employers pay people to do it, and that small law firms named by one seller pay a human desk for it.

What it does not prove about the exact offer: That owners outside law pay. That they pay an unknown person more than software costs. That they renew. That the desk moves collections. That bookkeepers refer. That the desk beats Invoice Butler, whose price is undisclosed.

Qualified buyer rule stated without an example industry: A firm that invoices other businesses on terms, regularly carries balances past 30 days that are large beside the fee, has nobody whose job is follow-up, and whose owner will let an outside person write to customers under the firm's name.

Unsuitable buyer rule: Bills consumers or is paid up front. Already has AR staff. Has so few, or such sensitive, customers that every account would be locked. Wants accounts already past the hand-back window worked, or wants threats or legal pressure. Is happy with a free tool. Operates where the operator's state check fails.

Three explanatory cases and the distinct buying decision each clarifies: All synthetic. (1) A firm with many small accounts on net terms: clarifies volume, missing documents, and flat fee versus share. (2) A firm with five large customers it fears losing: clarifies locked accounts, and when the honest answer is no sale. (3) A small law firm that could buy CollBox: clarifies when the desk should not compete with an established human service.

Why none of those cases defines the company or market: They are one company meeting three owners. The qualified-buyer rule decides, not the industry. The first niche is the viewer's choice.

The aspirational business the operator may ultimately build: A niche receivables practice of about 30 firms, with reusable templates, dispute patterns, and reporting, and possibly a referral relationship with bookkeepers who see the aging reports.

The entry wedge this episode makes concrete: One niche, a state check, five offers at a modeled $300 to $500, and one client's past-due list worked for 30 days with hours logged.

Entry-wedge thesis: why this is the responsible first paid way into the larger company: It tests the three things nothing on the desk can answer (whether owners allow it, what they pay, how many hours it takes), at the cost of a month and one client. The legal check comes first.

Why the wedge is an entry point rather than the business ceiling: A first client tests the desk. The templates, the niche knowledge, and the bookkeeper channel only exist after several.

Proof that would justify the next expansion step: Two of five firms agree to a paid month, and the pilot's 30+ day balance falls with under 1.5 operator hours per client per week. One client over 30 days cannot show the desk caused the fall, and the episode says so.

The first responsible action the viewer should be able to take: Check their own state's collection law, then take one aging report they can legitimately see and mark which lines a free tool could not fix.

Intended company-level verdict: **BUILD** (bounded), bench recommendation for owner decision at E3I. **PARK** stays open if the Canvas cannot reconcile hours, price, and tooling.

Why an affirmative BUILD verdict is evidence-safe: BUILD here means build the first test, not "this works." The problem is documented by a survey and by employers paying for the job. Named firms pay a human desk, on the seller's own pages. The tools are cheap and the test is one month with stated kill conditions. The case is still thin at the low price and the go-to-market is weak, and the episode says both. Score 68, advanced by owner override.

Value that must be delivered before any audience ask: The sending-versus-owning split, the price ladder, the follow-up and hand-back rules, the state line, the economics including the thin case, the kill conditions, the first move.

Natural final like-and-subscribe reason tied to that delivered value: The channel prices a business against the tools trying to replace it, and says where it breaks.

Other asks to omit or combine so the ending does not stack CTAs: No Canvas pitch, download, newsletter, or next-episode tease. One sentence.

## Operator Economy point of view

What common coverage gets wrong: It treats late payment as a sending problem, because the coverage is mostly written by companies selling the sender. None of the vendor pages read mentions that some states may treat this work as collection.

What a seasoned operator would notice: The reminder was never the whole job. One seller's own plan list shows the split: it charges for the disputed line and the phone call, and gives the email away.

What we believe, stated plainly: Sending is close to worthless now. The person who owns the list is the product. That can be sold by one person only below the human desks and only where the law allows it.

What a reasonable person could disagree with: That an owner pays $400 when the emails are free. That a bookkeeper would not add the tool and keep the client. That a funded seller will not come down to this price. That outsiders should write to a firm's customers about money at all. The alternative explanation also stands: owners may stop after one reminder from fear of losing the customer, and an outside sender could make that worse.

Broken incentive, fake solution, or conventional framing we are willing to judge: "AI AR desk" marketing that implies the job is done once the message is sent. Recovery figures quoted by sellers. Any pitch that skips the state question.

What would change our mind: An agent desk bundling a human specialist at or below $300 to $500 a month (the recorded park condition). A disclosed Invoice Butler price in that range for small firms. Viewers' first tests showing no owner will allow outside contact at any price.

## Truth and framing contract

Evidence class: **adjacent synthesis**

Observed facts the episode may rely on: The QuickBooks figures, attributed every time (CLM-001 to CLM-003). Seller prices and plan contents with read dates (CLM-017, CLM-019, CLM-020, CLM-023). CollBox's named customers as seller-published (CLM-019). Statute readings as a non-lawyer's reading of eight states (CLM-009 to CLM-016).

Modeled or synthesized elements that require one explicit qualification: The $300 to $500 fee, 30 clients, hours per client, tool cost, and all contribution figures. The company itself.

Evidence boundaries that should not be repeated unless their meaning changes: The QuickBooks sample skew. Seller-chosen testimonials. The non-lawyer reading, stated once clearly, then again wherever a specific state is named.

Claims the episode may not make: Any collection-rate, DSO, or recovered-cash result as observed, including CollBox's figures. That no licence is needed anywhere. Earnings, or contribution figures without their inputs and "modeled". That the QuickBooks figures describe all small businesses. That Manav has run, sold, or delivered a receivables desk, or worked in AR. idealab scores, market sizes, or revenue figures. Any estimated Invoice Butler price, or that the desk is cheaper than it. That the idea is new.

Economics language required: `Modeled scenario, not observed performance or an earnings forecast.`

Legal, permission, access, or ethical boundaries: The state check comes before the first client, and the episode is not legal advice. Pre-collection only; no threats, settlements, consumer debts, or funds. Client permission for mailbox and ledger access. Calling rules where calls are used. Vendor screenshots need permission, or use synthetic interfaces.

## Scope

Must answer:

- Why does follow-up stop after the first reminder, and what is an invoice usually stuck on?
- What does software do for $0 to $299, and what does it leave?
- What do human desks charge, and where would one person with agents fit?
- What exactly does the desk do each week, and what does the owner receive?
- What is the state line, and how does a viewer check their own?
- Can about 30 clients support one operator once hours and tool seats are counted?
- What would prove this does not work?

May answer if it strengthens the story:

- Bookkeepers: partner, rival, or both.
- Flat fee versus a share of what is collected.

Explicitly out of scope:

- A fifty-state legal map, or legal advice.
- Agency collection work, consumer debt, settlements.
- Any recovered-cash result.
- A software tutorial or tool recommendation.

Out of the initial offer but retained in the aspirational business:

- A bookkeeper referral channel.
- More niches, once templates exist.
- Portal submissions and vendor paperwork as a higher tier.

## Completion test

A skeptical viewer finishes this episode able to:

1. Explain the buyer problem: nobody owns the thread after the reminder.
2. Explain the offer and delivery: agents do the sending and sorting, one person does the rest.
3. Identify the strongest evidence (named firms pay a human desk; employers pay clerks) and the weakest assumption (owners pay an unknown person more than software costs).
4. Understand the economics as a scenario, including the thin case and the hours.
5. Describe the first test: state check, five offers, one client for 30 days, with kill conditions.
6. Explain the mature practice before the single client that starts it.
7. Explain how one client could grow into a niche practice, and what must be proven first.
8. Repeat "a receivables desk" and say what it does in one sentence.
9. State what to begin building without mistaking BUILD for proof or an income promise.
10. Explain the opportunity without relying on any one industry.
11. Name the established spend, at least two comparable scales, and the operator opening.
12. Tell a qualified firm from an unsuitable one.
13. Explain why required sales activity cannot come from an invented conversion rate: 30 clients come from capacity and price.

## Issues for the Canvas (Gate E3)

Bench findings, not yet resolved:

1. The hours do not fit the Step 0 capacity. 30 clients at 1 to 1.5 hours is 30 to 45 hours a week before selling, support, or the state work. The Canvas must count acquisition hours, or lower the client count.
2. The model has no churn and no ramp. Time to reach 30 clients is unknown.
3. The base tool cost ($21,000 a year) has no published multi-client price behind it. The per-seat sensitivity may be the honest base.
4. The $300 to $500 fee overlaps the $299 tool price. The Canvas should say what the owner gets at $400 that $299 does not buy, or move the band.

## Owner questions

Do you have your own experience of chasing a late invoice that you want in this episode? Default if unanswered: none is claimed. The POV stays synthesis, and nothing first-person is written or inferred.

## Approval

Decision: pending owner

Bench recommendation: approve this viewer, promise, central argument, spoken name, and exclusions.

Approved by: pending

Approval date: pending

Calculate the SHA-256 after this approval record is complete. Store it in dependent artifacts and the editorial lock; do not place a self-hash inside this file.
