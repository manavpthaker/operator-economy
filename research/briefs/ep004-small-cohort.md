# RESEARCH BRIEF — EP004 "The Small-Cohort Business"

**The Operator Economy · thesis-led episode brief · researched July 2026 (Cowork)**

**Thesis:** The expertise you were already paid for is the product. A small cohort — six to fifteen people, $800–$2,000 a seat, run two or three times a year — is now a viable one-person business. Not because cohorts got bigger, but because the two costs that made small numbers fatal (platform fees and manual operations) collapsed to near zero. The build is trivial now. Enrollment is not, and never will be.

**Structure (C→B per queue #6):** career-is-the-curriculum hook → the anti-platform wave as the "why now" industry section → small-cohort economics with the platform-tax math → playbook → honest economics.

**POV note:** Manav built the Reframe & Ready platform (Next.js/Supabase/Square/Resend, `grapevines/apps/cohorts`). The POV is builder-behind-the-infrastructure: what it actually costs and takes to own your own stack, and what it doesn't fix.

> **Interview dropped (7/31 decision).** EP004 was designed around an audio interview with Joanie Johnson. No recording exists in the repo. Joanie is now a **named, consented low-end example**, sourced from the July 14 call notes (`ep004-small-cohort-call-notes.md`), not an on-record guest. Her consent to be named, to the "I had the idea, AI built it" framing, and to the "Canva was a mess" line is documented there. **Two commitments from that call survive and are not optional:** she gets the EP004 blueprint PDF before the episode ships, and her stuck-points calibrate blueprint depth retroactively.

**Confidence legend:** [verified] primary/reputable · [reported] company-disclosed or aggregator-relayed · [estimate] analyst model · ⚠️ vendor/how-to-blog marketing number.

## 1. LOW END (solo operator)

- Typical cohort pricing: **$800–$1,500**, premium tier **$2,000–$5,000**. [reported ⚠️ — course-platform blogs]
- Solo operators increasingly run **group/mastermind cohorts at $3,000–$8,000 a seat, two or three times a year** — predictable revenue with no headcount. [reported ⚠️]
- **Ali Abdaal, Part-Time YouTuber Academy:** $4,995/seat; first cohort **$294K**; **>$1.5M in nine months**; single cohorts later reported at **$1.9M**. [reported ⚠️ — third-party review sites relaying self-reported figures]
  **Use as a ceiling anecdote and immediately discount it on screen.** He had a multi-million-subscriber audience before he sold a seat. As a proxy for a first-time operator it is close to worthless, and saying so is the credibility move.
- **Experience floor:** below roughly **6–8 participants** the cohort experience degrades; some trainers write "minimum cohort" clauses (reschedule, or the client pays a floor fee). [reported ⚠️]
- **Joanie Johnson / Reframe & Ready** (first-party, July 14 2026 call): current cohort is **one enrollee** (a PhD-level clinician driving his own curriculum, off the 8-week plan). A **peer coach at a similar price point filled six.** Her $60 interview-coaching webinar underfilled. Clientele is unemployed clinicians; **"$800 is a lot"** in that market. Multiple consults recently, none converted; she is testing finder's-fee / pay-on-placement structures. [verified — direct, first-party]
- **HONEST GAP, and it is the spine of the episode:** there is no audited solo small-cohort case study. The bands above are vendor how-to content. Joanie is **not** proof of demand at 15×$2K — she is proof that **build cost ≈ zero**, which is the actual claim.

## 2. HIGH END (venture-scale proof of market)

- **Maven:** **$20M Series A led by a16z** (May 2021, Andrew Chen to the board); ~**$25–30M total** raised with First Round. **300+ cohorts and ~$9M in course sales in the first 18 months.** Pivoted Sept 2022 from "creators" to **operators inside tech companies**. Still operating in 2026. Takes **10%** of gross, plus Stripe (~2.9% + $0.30) → **~12.9% all-in**. [reported]
- **Reforge:** **$81M raised** across two rounds ($60M Series B, Feb 2022). **Acquired by Miro, March 24 2026** — team, learning platform, and AI product tooling. 100,000+ alumni; Workday, Netflix, Mastercard, SAP. Brian Balfour became Miro's **Chief Growth Officer**, Tom Willerer **Chief Strategy Officer**. Price undisclosed. [verified — Miro newsroom]
- **The Reforge exit is the "why now" for the industry section.** The best-funded, best-branded version of "sell expertise to professionals" did not resolve into an education company. It resolved into a collaboration-software company's AI strategy. The venture-scale lane closed. That is an argument *for* the one-person version, not against it.

## 3. MARKET SIZE (all [estimate]; cite the range, not a point)

- Cohort-based courses: **$3.8B (2024) → ~$4.0B (2026)**, projected **$15.2B by 2034**, ~**16.2% CAGR**. [estimate — Dataintelo]
- Creator economy overall: **~$250B (2025) → ~$480B (2027)**, with the education slice growing faster than entertainment. [estimate]
- **Do not repeat the completion-rate stat uncritically.** "85–96% completion" and "3.6x higher than self-paced" are vendor marketing numbers from platforms that sell cohort software. [reported ⚠️] If used, say out loud who published them.

## 4. THE PLATFORM TAX (the math that carries the episode)

Take one honest small cohort: **six seats at $2,000 = $12,000 gross**, run over ~3 months.

| Path | What it costs that cohort |
|---|---|
| **Maven** | 10% platform + ~2.9% Stripe ≈ **~$1,550** |
| **Kajabi** | Growth **$249/mo** ($199 annual) ≈ **~$600–750** for the run; Starter adds **5%** on third-party Stripe; AI transcription is now a **$90/mo** add-on |
| **Teachable** | from **$39/mo** with a **5% transaction fee**; Pro **$119/mo** removes it |
| **Podia** | **$39–$199/mo**; **5%** on Starter |
| **Circle** | Professional **$89/mo** annual; **2%** transaction fee |
| **Owned stack** (the R&R build) | Next.js on Vercel + Supabase + Resend + Square ≈ **$0–50/mo** at this scale, plus ~2.6–2.9% processing |

[reported — vendor list pricing, July 2026]

**The line:** on a six-person cohort, the platform tax is roughly **one additional enrollee's worth of revenue**. At small n it is the largest controllable cost in the business, and it is the one cost that every "best course platform 2026" comparison article is structurally incapable of telling you to eliminate.

## 5. TOOL STACK (list pricing July 2026)

- **Owned:** Next.js (Vercel free→$20/mo), Supabase (free→$25/mo), Resend (free→$20/mo), Square or Stripe (~2.6–2.9% + fixed). Auth via magic link. This is exactly the Reframe & Ready build.
- **The AI layer that replaced the manual work:** intake scoring, assessment analysis, and delivery drafting. This is the part that used to be Google Forms → manual spreadsheet analysis → hand-built Canva decks.
- **Step 0 tooling:** NotebookLM / Claude deep research to find *what you could teach* — the gap between what you know and what people are searching for. Most people skip this and assume the topic.
- **Platform alternative:** Kajabi/Podia/Circle/Teachable remain the fast path. The episode should not pretend they're worthless — they're a real trade of margin for time-to-first-cohort.

## 6. FAILURE MODES

1. **Distribution. This is the episode's honesty section.** AI compressed the build and the delivery. It did not touch enrollment. Manav's guardrail line: *"AI can't solve the distribution problem."* Joanie's corroboration: *"nothing's passive, but it can be more efficient."*
2. **Buyer liquidity.** If your expertise serves people in transition, your buyers are between paychecks. $800 is a real barrier. Joanie's consults-to-conversions gap is the evidence.
3. **The visible-progress problem.** Buyers want daily proof of motion ("I applied to 10 jobs today"). Curriculum and positioning work feels slow, so it loses to activity that feels fast. Grapevines hits the identical friction at $79 — same buyer, same objection.
4. **The cohort floor.** Below ~6 the room stops working as a room. The economics now survive small n; the *pedagogy* still doesn't. Say both.
5. **Owning the stack means owning the pager.** No support team, no uptime guarantee, no one else to fix the payment webhook the night before a cohort opens.

## 7. NON-CONSENSUS ANGLES

1. **The change is at the bottom, not the top.** Everyone sells the Abdaal outcome. The actual shift is that a cohort of six — or one — no longer loses money. That's a different business than the one being marketed, and it's the one a real person can start.
2. **The platform tax is the largest controllable cost at small n**, and the entire comparison-content industry is paid not to say so.
3. **Reforge's exit to Miro is the category's tell.** The venture answer to "sell expertise" became an AI feature inside a software company. The high end vacated. What's left is the operator-scale version.
4. **Career-is-the-curriculum:** the asset is the thing you were already paid to know. AI can now help you find *which* part of it is teachable (step 0), but it cannot have done the work. That's the moat, and it's the one input that doesn't commoditize.
5. **Naming the cohort-of-one on screen is the differentiator.** Every competitor in this topic runs the $1.5M number and stops. Running the honest version — one enrollee, a peer at six, $800 is a lot — is what makes the rest of the episode believable.

## SOURCES

- TechCrunch — Maven $20M Series A led by a16z, 10% fee model — https://techcrunch.com/2021/05/20/maven-series-a-a16z/
- TechCrunch — Maven pivots from creators to experts (300+ cohorts, ~$9M sales) — https://techcrunch.com/2022/09/13/mavens-a16z-backed-teaching-platform-pivots-from-creators-to-experts/
- a16z — Investing in Maven — https://a16z.com/announcement/investing-in-maven/
- Maven Help Center — instructor payout, 10% platform fee + Stripe — https://help.maven.com/en/articles/5593804-getting-paid
- Miro newsroom — Miro acquires Reforge (Mar 24 2026) — https://miro.com/newsroom/miro-acquires-reforge-to-help-organizations-navigate-the-transition-to-ai/
- Class Central — Miro acquires Reforge: this is not an edtech deal — https://www.classcentral.com/report/miro-acquires-reforge/
- PitchBook / Tracxn — Reforge $81M raised, $60M Series B (Feb 2022), Miro acquisition — https://pitchbook.com/profiles/company/314616-34
- PR Newswire — Reforge $60M Series B — https://www.prnewswire.com/news-releases/reforge-announces-60-million-series-b-funding-to-expand-knowledge-and-networking-opportunities-for-members-301494857.html
- Dataintelo — cohort-based courses market size + CAGR — https://dataintelo.com/report/cohort-based-courses-market
- Kourses — Kajabi pricing 2026, plans and transaction fees (⚠️ affiliate-adjacent) — https://kourses.com/kajabi-pricing/
- Teachery — course platform pricing comparison 2026 (⚠️ vendor) — https://www.teachery.co/blog/course-platform-pricing-comparison-2026
- Circle — Kajabi alternatives, pricing and fee structures (⚠️ vendor) — https://circle.so/blog/kajabi-alternatives
- Disco — cohort pricing models and business models 2026 (⚠️ vendor) — https://www.disco.co/blog/pricing-models-for-cohort-based-courses-guide
- Ruzuku — cohort vs self-paced completion and pricing data (⚠️ vendor) — https://www.ruzuku.com/learn/articles/cohort-vs-self-paced
- ebizfacts — Part-Time YouTuber Academy review, cohort revenue figures (⚠️ relaying self-reported) — https://ebizfacts.com/part-time-youtuber-academy-review/
- First-party — Joanie Johnson call, July 14 2026 — `research/briefs/ep004-small-cohort-call-notes.md`
- First-party — Reframe & Ready platform build — `grapevines/apps/cohorts`
