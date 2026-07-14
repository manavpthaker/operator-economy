# Operator Blueprint #000 — The retention consultancy: an AI backend for Tactical Shift

*Companies too small for Culture Amp still bleed money when people quit. One operator with an assessment tool and an AI backend can sell them retention — as an outcome to owners, as analyst capacity to one-person HR teams.*

## The Idea

You already built the hard part. The assessments are certified, the methodology lives in your spreadsheets, the website is live, and you've run one engagement end to end. What's missing is the delivery layer: the machine that turns raw assessment data into client-ready deliverables — dashboard, 90-day plan, per-leader profiles, the deck — without you rebuilding everything by hand each time. That layer is now cheap to build, and it's the difference between a practice you're confident pitching and a website that sits unmarketed.

Two buyers, one machine. At 5–50 employees there is no HR: the owner buys the *outcome* — attrition insurance, because one departed clinician takes ~$120K/year in revenue with them. At 50–500 there's an HR-of-one: she buys *capacity* — she has the survey data and the mandate but no analyst, and you're the analyst she can't hire, not her competition. Above 500, walk away: Culture Amp, Gallup, and procurement cycles own that terrain.

**Who this is for:** operators who've managed teams or owned a practice — ex-owners, ex-HR leads, ex-ops managers, clinicians who ran a floor. The assessment provides the instrument, AI provides the analyst, you provide the judgment and the trust. You're not selling software; you're the consultant whose backend happens to be faster than everyone else's.

## The evidence

| Claim | Number | Source | Confidence |
|---|---|---|---|
| Revenue lost per departed clinician | ~$120K/yr | Operator's own P&L as a practice owner | Stated — lived number, one practice |
| Cost to replace an employee | 50–200% of salary | SHRM / Gallup replacement-cost ranges | Medium — analyst estimates vary widely |
| Cost of disengagement, global | $8.8T/yr claimed | Gallup State of the Global Workplace | Reported — headline figure, use as scale not precision |
| Culture Amp valuation | ~$1.5B (2021 round) | Press coverage of Series F | High — dated; proves the market, not the moment |
| The alternative the buyer weighs | ~$150K/yr loaded, full-time HR hire | Market comp | Medium — estimate |
| Engagement price this model carries | $5–7.5K / 90 days | This blueprint's pricing logic | Stated — estimate, unvalidated |
| Engagements delivered to date | 1 pilot (expedited, unpaid) | Operator's own ledger | Stated — the honest starting line |

**Read the gap honestly:** there is no public, verified solo case study of this exact model yet. The enterprise layer (Culture Amp, Gallup) proves companies pay real money for the machine; the solo layer is being documented in real time — by this engagement. Your before/after trend line becomes the case study you couldn't inherit.

## The stack (< $150/mo)

| Tool | Role | Monthly Cost | Notes |
|---|---|---|---|
| Claude Pro/Max | The analyst: intake → analysis → plan → deck generation | $20–100/mo | A Claude project loaded with your methodology |
| Certified assessment | The instrument: engagement + individual assessments | Contracted | Verify license terms before building on outputs |
| Sheets/Excel | Methodology home + standardized intake template | $0 | The template is what makes automation possible |
| HTML dashboard | Client deliverable — one self-contained page per client | $0 | Generated, not hand-built |
| Portal (phase 2 only) | Client login, tracking over time, email cadence | $0–25/mo | Next.js/Supabase/Resend — build when a client asks to log in |

**All-in fixed cost: under $150/month.** The margin on a $5–7.5K engagement is essentially your time — which is the point: the automation compresses delivery hours, it doesn't add cost.

## The playbook

**Week 1 — Verify the license, standardize intake**
- Confirm what your assessment contract lets you do with the output data. If it's restrictive, swap in an instrument you own — the machine doesn't care.
- Build ONE intake template: assessment exports, headcount, tenure, turnover history, org structure. If it isn't in the template, you don't accept it.

**Week 2 — Build the four generators, dry-run on the pilot**
- A Claude project loaded with your spreadsheets, scoring logic, and an anonymized past engagement.
- Four outputs, one prompt-plus-template each: the dashboard, the 90-day strategic plan, per-leader communication profiles, the client deck.
- Run your pilot engagement's data through it start to finish. What comes out is your sales demo.

**Month 1 — Sell segment one: the owner with no HR**
- Warm network first: owners and administrators you already know. The $120K line is the opener; the days-not-weeks baseline turnaround is the proof.
- Price the founding engagement discounted in exchange for a named case study and the trend-line data.

**Months 2–3 — Run the 90-day loop, then open segment two**
- Weeks 1–2: baseline, dashboard, plan delivered fast. Weeks 3–10: the human part — leadership work, hard conversations. Weeks 11–12: re-measure, updated dashboard, renewal conversation.
- With one trend line in hand, pitch the HR-of-one at 50–500-person companies: her data, your machine, her win.
- Productize only when a paying client asks to log in. Not before.

## The honest math

- **Realistic year-one range:** $15–30K/yr from 2–3 engagements at $5–7.5K — a strong second income stream, not a startup. This is the operator's own stated target, reasoned from one unpaid pilot, and it assumes the warm network produces the first client.
- **Failure mode #1 — the license.** Building your delivery machine on an assessment you don't own is platform risk in a lab coat. Verify terms in week one or swap instruments.
- **Failure mode #2 — selling up-market.** The 500+ segment looks lucrative and will burn you: procurement cycles, incumbent platforms, security reviews. The named no-go line exists because solos die there.
- **Failure mode #3 — distribution.** AI compresses delivery from weeks to days; it does nothing for the pipeline. First clients come from people who already trust you, and that part stays boots-on-the-ground.
- **The open question:** whether the 90-day engagement renews into an ongoing retainer (quarterly re-measures) or stays one-shot. Renewal economics are what turn 3 clients/year into a durable practice — the pilot data will answer this.

## Sources

1. Operator's own P&L — $120K/yr revenue per clinician, stated from direct experience as a practice owner
2. SHRM / Gallup — employee replacement cost ranges, 50–200% of salary, analyst estimates
3. Gallup State of the Global Workplace — $8.8T disengagement figure, headline scale only
4. Press coverage — Culture Amp Series F, ~$1.5B valuation (2021, dated)
5. Market comp — fully loaded cost of a full-time HR hire, estimate
6. This blueprint — engagement pricing and year-one range, marked estimates, unvalidated
7. Operator's ledger — one expedited unpaid pilot engagement delivered to date
