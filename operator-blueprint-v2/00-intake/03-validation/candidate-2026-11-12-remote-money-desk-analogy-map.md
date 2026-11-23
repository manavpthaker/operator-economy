# Analogy map: Remote money desk for families of aging parents

Template status: approved V2 Step 0.2 template; locked 2026-08-21.

Template version: `operator-blueprint-v2-step0.2`

Candidate ID: `candidate-2026-11-12-remote-money-desk`

Candidate brief: `../01-candidates/candidate-2026-11-12-remote-money-desk.md` / `7debe8a80a43c528cc560d1a676d1a5b192b7edb4aaab3f684fd228a29cce984`
(offer wording trails the research brief; reissue deferred to the scorecard run, see the
2026-11-23 disposition addendum)

Research brief: `../02-research/candidate-2026-11-12-remote-money-desk-research.md` / `a81fe8973b4826528497f4dfb2dd3afbed12ba1a575db5d83a84b0b8d181125e`

Prepared: 2026-11-23

Evidence class: observed model

## Synthesis thesis

This business is like Parent Bill Pay and Paytrust (formerly SilverBills) for the offer and its
price band (a remote person checks and pays a household's bills from the household's own account,
under rules agreed in writing, from $250 and $500 a month), like the local daily money manager for
the scope, ethics, and insurance norm, and like EverSafe and Golden for the daily watching, which is
bought in as cheap software rather than built. The new combination is one operator running agents
over the mail, statements, and matching for many households, inside three hard limits the sellers
read do not state: never hold the money, never pay with a shared login, and keep the record the
family's legal agent is already required to keep.

## Transfer records

| Analogy ID | Proposed-business component | Reference model | Source claim IDs | Relationship | Shared structure | Required adaptation | Does not prove | Break condition | Confidence | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| ANA-001 | Buyer/problem | Long-distance children asking for help with a parent's mail and bills (AgingCare, r/AgingParents) | CLM-001, CLM-017, CLM-018 | direct | Same buyer (an adult child far away), same job (mail, bills, odd charges), same fear (handing over access) | None for the buyer; frequency must stay unquantified | How many families; willingness to pay; any verified person | Fresh buyer voice shows families now solve this with software alone | low-medium | valid (anecdote only) |
| ANA-002 | Buyer/problem, scale | FBI IC3 2025 elder fraud complaints | CLM-015 | adjacent | Older adults losing money through their accounts | Scam side only; most loss involves crypto a bill desk would not see | Missed or double-paid bills; what a desk would prevent | n/a (context only) | high (as a fact), low (as transfer) | weak (scale context, not demand) |
| ANA-003 | Budget or current alternative | Local daily money managers sold by the hour, AADMM membership | CLM-006, CLM-007 | adjacent | Same scope sold to the same families in person, insured | Remote, flat monthly; hourly rate not verified (CLM-009 struck) | That families pay a remote desk; a price | Local DMMs stop selling bill handling, or AADMM shrinks sharply | medium | valid |
| ANA-004 | Offer and delivery; price band | Parent Bill Pay: remote, any state, from $250 a month, pays from the parent's accounts, approvals agreed in writing | CLM-002, CLM-019 | direct (observed model, seller copy) | Same deliverable, remote delivery, payment from the household's own account | Agents do the reading and matching; operator serves many households | Buyer uptake, renewal, hours | Seller closes, or turns out to hold client money | medium | valid |
| ANA-005 | Offer and delivery; price band | Paytrust (formerly SilverBills): concierge bill pay from $500 a month, reviews each bill before money moves, rules include approve each payment | CLM-020, CLM-025 | direct (observed model, seller copy) | Same job, a named concierge, a written rule set, records | The desk refuses shared logins (Paytrust accepts them); aimed at families of aging parents, not general affluent clients | Buyer uptake at $500; that its clients are aging parents | Paytrust drops the human concierge, or its price falls toward software levels | medium | valid |
| ANA-006 | Delivery feasibility (watching) | EverSafe and Golden account monitoring, $7.49 to $26.99 and $20 a month, no money movement | CLM-004, CLM-016 | component | Daily alerts to named family members | Bought in per household, not built | That the desk adds value on watching (it does not) | Monitoring tools stop selling to families | medium | valid (as a bought-in component) |
| ANA-007 | Delivery feasibility (agent reading) | EP010 receivables desk pattern: agents read and draft, the person owns exceptions | none external | hypothesis | Agents handle the reading; one person owns the calls and the record | Mail scans and statements instead of invoices | Agent accuracy on household mail; hours per household | Timed synthetic month exceeds 4 hours per household | low | weak (no source; viewer's first test) |
| ANA-008 | Go to market | Bank referral to a case management agency; AADMM directory | CLM-018 | adjacent | Families reach help through a bank or a directory | Desk must be listed or referred; remote trust gap | That referrers send remote desks work | No referral source will send a remote, non-local desk | low | weak (one anecdote) |
| ANA-009 | Outcome measurement | Quarterly accounting sent to the whole family; Florida agent's record duty; Paytrust "meticulous records" | CLM-018, CLM-023, CLM-025 | adjacent | A written record of every payment, shared with named people | Weekly one-pager; one state's statute only | That the record prevents loss | Families ignore the record in the first test | medium | valid |
| ANA-010 | Legal boundary (constraint on offer) | FinCEN DMM ruling; Texas and California money transmission definitions; Regulation E; Florida POA statute; TX/FL mandatory reporting; Wells Fargo view-only access | CLM-010 to CLM-014, CLM-021 to CLM-024 | direct (boundary) | Whether and how a third party may move an older adult's money | Viewer checks their own state; no ruling on a desk paying from the client's account | That the desk is lawful anywhere; non-lawyer reading | A regulator treats initiating payments from a client's account as money transmission | medium-high | valid (as a constraint, not support) |

## Coverage test

| Pillar | Required status | Supporting analogies | Result | Remaining assumption and test |
|---|---|---|---|---|
| Buyer and costly problem | Must have usable direct or adjacent evidence. | ANA-001, ANA-002 | pass | Direct evidence is buyer voice only; frequency and cost unquantified. Viewer's first test: five families through one referral source |
| Budget or current alternative | May use direct, adjacent, or component evidence. | ANA-003, ANA-004, ANA-005 | pass | Two remote seller floors ($250, $500) and local DMMs; no buyer record of paying. Scored as a gap; price is the viewer's first test |
| Offer and delivery | Must have a valid operating parallel or bounded first-party test. | ANA-004, ANA-005, ANA-006, ANA-010 | pass | Agent reading and per-household hours (ANA-007) are untested; viewer times a synthetic month |
| Go to market | May use a transferable acquisition or diagnostic-entry model. | ANA-008 | fail (weak) | One anecdote of a bank referral; viewer's first test is one referral source and five offers |
| Economics and capacity | Must have a transparent model with evidence for its inputs or explicit testable assumptions. | ANA-004, ANA-005; research-brief model | pass | $200–$400 price, 25–50 households, 2.5 hours each are modeled; testable in 30 days |
| Outcome measurement | Must define an observable buyer deliverable; business impact may remain a hypothesis. | ANA-009 | pass | Weekly record and alert log are observable; prevented loss stays a hypothesis |

## Evidence-floor verdict

- Usable direct or adjacent buyer/problem evidence: pass (buyer voice, anecdote class)
- Valid analogy count: 7 (ANA-001, ANA-003 to ANA-006, ANA-009; ANA-010 is a valid constraint;
  ANA-002, ANA-007, ANA-008 weak)
- Independent source families: 6 (caregiver forums; remote sellers; local DMM sellers; monitoring
  software sellers; federal regulators; state statutes and consumer guides)
- Required pillars covered: pass (go to market is the one weak pillar, which the template allows
  to rest on a transferable model; it is resolvable through the validation plan)
- More than one untested inference hop in a load-bearing claim: no (the legal inference "outside
  money transmission on its face" is one hop and is not load-bearing for the offer; the episode
  may not claim it)
- Uncovered pillars resolvable through the bounded validation plan: yes

Verdict: pass

Reason: Two remote sellers publish the same job at $250 and $500 floors, paying from the
household's own account, and families describe the problem in their own words. Agents are a
component hypothesis, and the watching is bought in as software. The pass rests on seller copy and
anecdote: nothing read shows a family paying a remote desk. CLM-009 (scout-ledger AgingCare items
and the hourly DMM rate) is struck from load-bearing use; AgingCare was unreadable on three runs.

## Disclosure carried forward

Observed model. The viewer must hear that Parent Bill Pay and Paytrust sell this at published
starting prices, but no record of families paying them was found; that the solo-operator version
is a modeled scenario; and that the desk has three hard limits (never hold the money, never pay
with a shared login, report suspected exploitation where the law requires it), checked in two or
three states only and not legal advice. The most important assumption: that a family will trust a
remote stranger with a parent's accounts at a price above the software, which is the viewer's
first test.
