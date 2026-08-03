# RESEARCH BRIEF — EP003 "The Boring-Automation Agency"

**The Operator Economy · thesis-led episode brief · researched July 2026 (Cowork)**

**Thesis:** SMBs pay real money for unglamorous workflows that move data between the tools they already use (CRM→invoicing, form→inbox, spreadsheet→Slack). n8n or Make + a few hours a week, priced as a retainer. Concept-led, decay-proof, one operator.

**Confidence legend:** [verified] primary/reputable · [reported] company-disclosed or aggregator-relayed · [estimate] analyst model · ⚠️ vendor/how-to-blog marketing number.

## 1. LOW END (solo operator best case)
- Setup/build fees: **$1,500–$5,000 simple** single-workflow; **$6,000–$15,000** complex (docs, LLM classification, multi-system routing); $35K+ full migrations. [reported ⚠️ — agency how-to blogs, not audited]
- Monthly retainers: **$500–$5,000/mo** monitoring; support retainers **$2,000–$8,000**. [reported ⚠️]
- "Two Scale clients at **$7,000–$12,000/mo combined** cover a solo founder's full income with capacity to spare." [reported ⚠️]
- Winning model: niche into ONE industry/use-case, sell productized workflow packages, one-time setup + monthly hosting/maintenance retainer. [reported]
- HONEST GAP: the low-end numbers are vendor-adjacent how-to content, not audited books. Frame as reported/directional (on-brand honesty). No single audited solo case study surfaced.
- Sources: LearnForge, Digital Identity Architects, n8nitro, Arsum, taskip (all 2026 agency guides).

## 2. HIGH END (venture-scale proof)
- **Zapier:** ~**$310M ARR (2024)**, forecast ~$400M (2025); **~$5B valuation** (2021, still cited 2026); 100K customers; reached $100M ARR in ~10 yrs on only **$1.4M VC raised** — extraordinary capital efficiency (the margin story). [reported — getLatka/Sacra aggregators]
- **n8n:** **$180M Series C at $2.5B valuation (2025)**, Accel-led + NVIDIA NVentures + Deutsche Telekom; earlier €55M Series B (Mar 2025) at €300M; **~$40M ARR (Jul 2025), usage 10x YoY**; 3,000+ enterprise customers incl. **Vodafone, Delivery Hero, Microsoft**. The tool the agencies build on is itself a billion-dollar business. [reported — Ventureburn/Sacra]
- **Make (Integromat):** acquired by **Celonis 2020**, rebranded Make 2022; **500,000+ users, 3,000+ apps**; Core $9/mo; switched to credit billing Aug 2025. [reported]

## 3. MARKET SIZE (all [estimate]; wide spread is the story)
- iPaaS market 2026: analyst estimates range **~$13.9B–$23.36B**, CAGR ~24–34% into the 2030s (Precedence, Fortune Business Insights, Business Research Insights, MarketsandMarkets). Cite as "somewhere between ~$14B and ~$23B in 2026, nobody agrees where the category ends."

## 4. TOOL STACK (list pricing Jul 2026)
- **n8n:** self-host free / cloud ~$20–50/mo (you own the workflows — why agencies standardize on it).
- **Make:** Free (1,000 credits) / Core **$9** / Pro **$16** / Teams $29.
- **Zapier:** paid from ~$20/mo (the incumbent; higher cost, easiest).
- **The connected apps** (client already pays): HubSpot/CRM, invoicing, forms, spreadsheets, Slack.
- **The AI node:** a Claude/GPT call inside the workflow to read messy input (email → clean structured data) — the node that turns simple automation into retainer-worthy work.
- Operator's own tools: **well under $100/mo**; the client pays for their own software.

## 5. FAILURE MODES
1. **Platform risk:** you build on someone else's tool; n8n/Make can change pricing/limits/terms, or a connected app breaks its integration. Own workflows where possible.
2. **Commoditization:** the simplest 2-step automations are getting easy enough that clients will DIY; durable work is the messy, judgment-heavy integrations.
3. **Distribution:** AI compresses delivery, not pipeline. First clients come from trust/word-of-mouth; no workflow automates that.

## 6. NON-CONSENSUS ANGLES
1. The unglamour IS the moat — the people who could do this mostly don't want to; "boring" filters out competition.
2. Zapier's **$100M ARR on $1.4M raised** proves the category's margins are extraordinary — connecting apps is nearly pure-margin once built.
3. The low-end evidence is vendor-adjacent how-to content; naming that on screen (no audited solo case) is the credibility move listicles skip.
4. The retainer is for **upkeep, not the build** — apps change, workflows break; maintenance is the recurring revenue and the reason it doesn't fully commoditize.

## SOURCES
- getLatka/Sacra — Zapier revenue/valuation/capital efficiency — https://getlatka.com/companies/zapier · https://sacra.com/c/zapier/
- Ventureburn — n8n $180M Series C at $2.5B (2025) — https://ventureburn.com/n8n-series-c-funding/
- Sacra — n8n ~$40M ARR Jul 2025, 10x usage — https://sacra.com/c/n8n/
- G2 / Zapier blog — Make (Integromat/Celonis) pricing + 500K users — https://zapier.com/blog/make-com-pricing/
- Precedence / Fortune Business Insights / Business Research Insights — iPaaS market size 2026 (range) — https://www.precedenceresearch.com/integration-platform-as-a-service-market
- LearnForge / n8nitro / Arsum — automation agency setup + retainer pricing bands (how-to, ⚠️ reported) — https://learnforge.dev/blog/n8n-automation-agency/ · https://arsum.com/blog/posts/ai-automation-agency-pricing/
