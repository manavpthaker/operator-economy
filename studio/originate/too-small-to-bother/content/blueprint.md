# The Operator Economy Evaluation Sheet
## (Companion to "Too Small to Bother")

**What this is:** the one-page test for deciding whether a software business too small for venture capital is defensible anyway — plus every sourced number from the episode, so you can act on this without watching it.

---

## The Idea, in One Paragraph

The minimum viable size of a software business collapsed. Between 2017 and 2022, the number of U.S. software firms with fewer than five employees grew 55%, from 5,060 to 7,857 — they're now the majority of software publishers in the country. At the same time, the gap between a top-launch and a median launch doubled in a year. Both facts are downstream of the same cause: build cost fell, distribution cost didn't. More people can stand on the floor. It got worse for the median person standing there. Neither half of that sentence cancels the other.

The question this doc answers isn't "can I build this" — that's basically free now. It's: **is this specific business defensible once it exists, and does its size protect it or expose it?**

---

## Evidence Table

| Claim | Number | Source |
|---|---|---|
| U.S. software firms, <5 employees | 5,060 (2017) → 7,857 (2022), +55% | US Census SUSB, NAICS 5112, Apr 2025 |
| Share of software publishers that are micro-firms | 57.5% | US Census SUSB |
| Aggregate receipts, micro-firm cohort | $5.30B (~$674,676 avg/firm) | US Census SUSB |
| Solo operators clearing $1M/yr | Roughly doubled, 2023–2025 | Stripe Economics |
| Top-5%-vs-bottom-quartile earnings gap, new app launches, year 1 | ~400x (up from ~200x the prior year) | RevenueCat, 115,000+ apps |
| Median new app revenue at month 12 | <$50/mo | RevenueCat |
| New launches reaching $1K MRR within 2 years | 17.3% | RevenueCat |
| New launches reaching $10K MRR within 2 years | 4.6% | RevenueCat |
| Micro-SaaS products under $1,000 MRR | ~70% | Freemius, Dec 2025 |
| New iOS apps added, 2025 | ~600,000 (+30%) | Sensor Tower |
| Download growth, same period | 2–3% | Sensor Tower |
| Medvi: revenue, headcount, starting capital (reported, not audited) | $401M / 2 employees / ~$20K | Forbes, Apr 2 2026 |
| Cursor / Replit / Lovable annualized revenue (reported run-rates) | ~$2B / ~$240M / ~$200M | RESEARCH-DOSSIER §2, 2026-08-08 |
| VC financings returning less than capital in | 65% (of 21,640 deals) | Correlation Ventures |
| VC financings returning 10x+ | ~4% | Correlation Ventures |
| Share of U.S. startup funding from VC | 4.4% | Kauffman Firm Survey |
| Share of Inc. 5000 firms that ever raised VC | 6.5% | Kauffman Firm Survey |
| Small business share of U.S. GDP | 43.5% | SBA Office of Advocacy, Feb 2026 |
| Toast FY2024: fintech revenue vs. software subscriptions | $4.053B vs. $706M | Toast 10-K, FY2024 |
| Google Play listings, drop in ~15 months | 3.4M → 1.8M | TechCrunch, Apr 2025 |
| Business survival, 1994 cohort (569,387 establishments) | 79.6% at 1yr / 49.6% at 5yr / 33.6% at 10yr | US BLS Business Dynamics |

---

## Tool Stack (What It Actually Costs to Run One of These)

This episode isn't a tool-recommendation episode — the stack was never the constraint. But for orientation, here's what a micro software business typically runs on, at public pricing:

| Category | Tool examples | Typical monthly cost |
|---|---|---|
| Hosting/infra | Vercel, Render, Railway | $0–20 |
| AI/API usage | OpenAI, Anthropic, Claude API | $20–150, usage-based |
| Payments | Stripe, Paddle | 2.9%+30¢ per transaction, no fixed fee |
| Email/marketing | ConvertKit, Resend | $0–40 |
| Analytics | Plausible, PostHog free tier | $0–20 |
| Domain/DNS | Namecheap, Cloudflare | ~$12/yr |

**Total realistic monthly cost to keep something alive: $50–200.** That's the entire point of the episode — the build/run cost stopped being the binding constraint years ago. What you're actually spending is time against the distribution below, and the demand risk that never went anywhere.

---

## The Two-Question Evaluation Sheet

Run any idea through this before you build anything.

**Question 1 — Would anyone with real money bother taking it from you?**
Estimate what it would cost an acquirer with capital to reproduce your accumulated position: integrations, records, workflow embeddedness, relationships. Then estimate what the market would pay them back for doing it. If the reproduction cost exceeds the payback, you're protected — not because they can't clone you, because it isn't worth their time. (Constellation Software runs six operating groups across 70+ vertical markets buying exactly these businesses — the knowledge is transferable, which is why size, not secrecy, is the moat.)

**Question 2 — Whose distribution is it?**
Do you reach your buyers through something you own (an existing audience, a profession you're inside of, a named list) or through a platform whose algorithm or policy you don't control? Google Play went from 3.4M to 1.8M listings in about 15 months. A business whose distribution is a platform is a tenant, not an owner — and tenancy risk is measured, not theoretical.

If you can answer both with specifics — not hope — you have a real evaluation. If you can't, you have a hobby with better tooling.

---

## Week-by-Week Playbook

**Week 1 — Map the market.** Identify a workflow inside a profession or niche you have real fluency in. Fluency is the entry ticket, not the moat — it just buys you the right first product.

**Week 2 — Run the reproduction-cost arithmetic.** Write down, in dollars, what it would cost a funded competitor to rebuild what you plan to accumulate. If you can't answer this in specifics, you don't understand your own defensibility yet.

**Week 3 — Audit your distribution before you write code.** List every channel you'd rely on to reach buyers. Cross out every one you don't own outright (a platform algorithm, a marketplace ranking, a single partner). What's left is your real distribution.

**Week 4 — Build the smallest version that starts accumulating something.** Not features — position. Integrations, records, workflow lock-in. This is the part that compounds; the product itself doesn't.

**Weeks 5–8 — Ship, price honestly, and track against the real odds ladder**, not the flattering one: ~17.3% of launches hit $1K MRR within two years, ~4.6% hit $10K. Plan your runway assuming you're the median, not the outlier — and re-run Question 1 and Question 2 once you have real usage data, because your reproduction cost changes as you accumulate.

---

## Honest Economics

- Average receipts across the Census micro-firm cohort: **~$674,676/year** (this is an average across 7,857 firms, not a typical outcome — averages hide the spread).
- Median new subscription app: **under $50/month** after 12 months.
- ~70% of micro-SaaS products never clear **$1,000/month**.
- Both tails are real. You don't get to pick which one you're in by wanting it — you get to shift your odds by how seriously you answer the two questions above.
- The build risk that used to gate this market collapsed. The demand risk — will anyone actually pay — did not move at all.

---

## Sources

US Census Bureau, Statistics of US Businesses (NAICS 5112), released April 2025 · Stripe Economics · RevenueCat, 115,000+ subscription apps · Freemius, December 2025 · Sensor Tower, 2025 · Forbes, April 2, 2026 (reported, not audited) · RESEARCH-DOSSIER §2 (2026-08-08), reported run-rates · Correlation Ventures, 21,640 financings · Kauffman Firm Survey · SBA Office of Advocacy, February 2026 · Insurance Journal · Toast 10-K, FY2024 · Constellation Software Annual Report, 2025 · TechCrunch, April 2025 · US Bureau of Labor Statistics, Business Dynamics, 1994 cohort.
