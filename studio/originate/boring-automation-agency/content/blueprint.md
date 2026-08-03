# The Boring-Automation Agency Blueprint

## The Idea

Small companies run on tools that were never built to talk to each other: a CRM, an invoicing tool, a web form, a spreadsheet, a Slack channel. You build the workflows that move data between them, using n8n or Make, with an AI node in the middle to handle anything messy (an email, a free-text form) that used to need a human to interpret. You price it as a build fee plus a monthly retainer to keep it running.

This is not a coding project and not a SaaS. It is a service business with recurring revenue, and the barrier to entry is low because the tools became drag-and-drop. The barrier that stays high is that most people find this work too dull to bother with. That's the moat.

It's for operators who understand a specific industry's manual busywork: ex-ops people, ex-agency people, anyone who has watched a team lose hours a week to copy-pasting data between systems. You don't need to be an engineer. You need to know one workflow in one industry well enough to automate it and explain the before/after in plain terms.

## The evidence

| Claim | Number | Source | Confidence |
|---|---|---|---|
| Zapier scale on tiny capital | ~$310M ARR, ~$5B valuation, on ~$1.4M raised | getLatka / Sacra (market aggregators) | Reported — aggregator data |
| n8n venture traction | $180M Series C at $2.5B valuation (2025); ~$40M ARR; 10x usage YoY; 3,000+ enterprise customers (Vodafone, Microsoft) | Ventureburn, TechCrunch, Sacra | High — multiple outlets |
| Make (Integromat) | 500,000+ users; Core from $9/mo; acquired by Celonis 2020 | Zapier blog, G2 | Reported |
| iPaaS market size | ~$14–23B in 2026, 20%+ CAGR | Precedence, Fortune Business Insights | Medium — analyst estimate, wide spread |
| Solo agency setup fees | $1,500–5,000 simple / $6,000–15,000 complex | Agency how-to guides (LearnForge, Arsum, n8nitro) | Low — vendor-adjacent, unaudited |
| Solo agency retainers | $500–5,000/mo per client | Same guides | Low — reported, unaudited |
| Two-client combined income | ~$7,000–12,000/mo | Arsum, taskip, Digital Identity Architects | Low — reported, unaudited |
| Verified solo case study at scale | — | Research honesty note | Stated explicitly as a gap |

**Read the gap honestly:** the low-end agency numbers come from vendor-adjacent how-to content, not audited books. Treat them as directional, not confirmed. The high-end numbers (Zapier, n8n, Make) are independently reported by market aggregators and press. Validate with your own before/after numbers; don't inherit anyone else's case study.

## The stack (< $100/mo)

| Tool | Role | Monthly Cost |
|---|---|---|
| n8n | Automation engine you own; self-host or cloud; the agency standard because you own your workflows outright | $0 self-hosted / ~$20–50 cloud |
| Make (Integromat) | Visual automation, no server required; friendlier if you never want to touch infrastructure | Free / Core $9 / Pro $16 |
| Claude or GPT (workflow node) | The AI step: reads messy input (an email, a form field) and outputs clean structured data | Usage-based, cents per run |
| Client's existing apps (CRM, forms, invoicing, Slack) | The systems you're wiring together; the client already owns and pays for these | $0 to you |
| Airtable / Google Sheets | Staging and logging layer between systems | $0–20/mo |

**Total operator cost: well under $100/month.** The client pays for their own software stack. Your margin comes from the platform subscription plus your time, the same structural margin that let Zapier scale to a $5B valuation on ~$1.4M raised.

## The playbook

**Week 1 — Pick your lane.** Choose one industry and one painful, manual workflow inside it that you already understand. Real-estate lead routing, clinic intake forms, e-commerce order sync. Narrow beats broad: a niche lets you reuse the same build across clients and speak their language instead of relearning a business every time.

**Week 2-3 — Build one real workflow.** Not a demo. Take an actual manual hand-off a real business does today and automate it end to end. Document the before and after (hours spent vs. hours now). This working automation is your sales pitch; it sells the next client better than any deck.

**Week 4 — Price it right.** Build fee plus a flat monthly retainer. Never hourly, because hourly punishes you for getting faster. The retainer isn't for the build; it's so the automation is still standing the morning an app changes its login or a form adds a field. Frame it to the client as a dial tone: they never think about it until it stops.

**Month 1 — Land 2-3 clients.** Start with people who already know you and this work. Turn each client's hours-saved into a short case study. Boring, concrete results spread by word of mouth because an owner can literally point to the hours they got back.

**Month 2 — Delivery discipline.** Document every workflow so you're not the single point of failure. Set alerts so you hear about a break before the client does. Send a short monthly note: what ran, what it saved, what you caught. That note is what renews the retainer.

## The honest math

Realistic year-one range: roughly $2,000-$6,000/month from 3-6 retainer clients, once you're past a slow first month. This is an estimate reasoned from reported agency pricing bands, not an audited outcome, and it assumes you can actually find those first clients.

- **Platform risk.** You're building on someone else's tool. n8n or Make can change pricing, usage limits, or terms; an app you connect to can break its integration overnight. Mitigate by owning your workflows where possible and never letting a client's entire system hang on one fragile link.
- **Commoditization.** The simplest automations are getting easy enough that clients will eventually build them without you. The durable work is the messy, judgment-heavy integrations (payroll, reconciliation, order-to-fulfillment), not the two-step ones. Nobody wants to build those alone, and that's exactly why they stay durable.
- **Distribution.** The tools got easy; finding clients did not. Your pipeline still runs on trust and word of mouth, and no workflow automates that. This is the real bottleneck, not the build.

**Open question:** does this stay a bespoke solo retainer practice, or do the best operators productize the same five workflows and sell them a hundred times? Both are viable. They are different businesses.

## Sources

- Zapier ARR/valuation/capital efficiency — getLatka, Sacra (reported)
- n8n Series C, ARR, customer count — Ventureburn, TechCrunch, Sacra (verified/reported)
- Make/Integromat acquisition, users, pricing — Zapier blog, G2 (reported)
- iPaaS market size — Precedence Research, Fortune Business Insights, Business Research Insights (analyst estimates)
- Solo agency pricing bands — LearnForge, Arsum, n8nitro, taskip, Digital Identity Architects (reported, vendor-adjacent, unaudited)
