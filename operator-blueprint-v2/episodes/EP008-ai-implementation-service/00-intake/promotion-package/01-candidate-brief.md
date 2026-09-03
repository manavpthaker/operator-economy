# Candidate: AI support-desk implementation for small DTC brands

Template status: approved V2 Step 0.2 template; locked 2026-08-21.

Status: candidate

Template version: `operator-blueprint-v2-step0.2`

Candidate ID: `candidate-2026-09-03-ai-implementation-service`

Created: 2026-09-03

Owner: Manav Thaker

Proposed evidence class: observed model (service category), with all solo-operator economics modeled

## Legacy provenance

This is the Step 0 re-entry of the published EP001 premise. Prior publication earns no promotion credit; the old script, research and scores are leads only.

- Public title and URL (record only): "The $5.9 Billion Business You Can Start for $100", `https://www.youtube.com/watch?v=cXC4lYRu_Gg` (per `fixtures/legacy-episode-calibration-2026-08-21/00-legacy-screen.md`; `launch/links.json` still reads `[PENDING_UPLOAD]`). Third-party view API on 2026-09-03 reported 31 views, 5 likes.
- Historical source premise: `studio/originate/ai-implementation-consulting/research.md` / `9e71762328c9baba0faf8b0ae65c605a5918f75e6e5b2ad0255563ffdf4a3b3a`
- Historical script: `studio/originate/ai-implementation-consulting/script.json` / `45a672f851cc937441a568cbfed50f3ad80182b09138f1b8597ed39f1704d37d`
- Legacy screen (2026-08-21, provisional band 58-67, "continue research"): `operator-blueprint-v2/00-intake/fixtures/legacy-episode-calibration-2026-08-21/00-legacy-screen.md` / `5b2dacb247245511e6f58ab6a335817da671b93de979a3b4cc9406b0642bc61b`

### Refinement from the legacy premise (stated explicitly)

The legacy premise was "sell AI implementation to businesses drowning in it" — every buyer, every workflow, Accenture at the top and a Medium blog at the bottom. The screen found no bounded buyer or job, unaudited creator economics, and a market-size ladder instead of a story. This candidate keeps the underlying business — **installing AI that already exists, rather than building it** — and bounds it to:

- **one buyer:** the owner or head of CX at a small direct-to-consumer (DTC) brand on Shopify, doing roughly 1,000–5,000 support tickets a month, small enough that the helpdesk vendor gives it self-serve onboarding rather than a dedicated implementation manager;
- **one workflow:** the inbound support queue — order status, returns and exchanges, cancellations and order edits — handled inside the helpdesk the brand already pays for (Gorgias or Zendesk);
- **one deliverable:** a fixed-scope implementation of the helpdesk's own AI agent — ticket audit, knowledge and guidance authoring, skills and handover rules, test suite, go-live, two weeks of monitored tuning — with a before/after report;
- **one measure:** the vendor's own verified-resolution meter (the count the vendor bills on) plus first-response time and escalation errors, before and after;
- **one 30-day test:** described in the research brief.

The hospitality angle in the legacy brief is deliberately not used: EP007 (direct-booking recovery) already occupies hospitality, and the strongest current evidence for "AI bought, not working" sits in ecommerce support.

## Opportunity in one sentence

An operations-minded generalist sells small DTC brands a fixed-fee implementation that takes the AI agent already bundled into their helpdesk from "switched on with defaults" to a configured, escalation-safe system that measurably resolves order-status, returns and cancellation tickets — without building any AI and without replacing the brand's tools.

## Viewer outcome

- Viewer promise: The viewer understands why a business can buy an AI agent and get nothing from it, what the work between "bought" and "working" actually consists of, and whether they can sell that work as a bounded service.
- Operator decision: Build the implementation practice, run one unpaid implementation to test it, fold it into an existing ecommerce or ops consultancy, or reject it.
- Practical capability: Audit a support queue by intent, judge which tickets are safe to automate, write the guidance and handover rules that decide the outcome, define the before/after measure, and price a fixed-scope engagement against the buyer's own payback.
- Expected Operator Canvas: Operator fit, buyer and trigger (the vendor's onboarding threshold), offer scope, delivery workflow with the human judgment points named, capacity, pricing arithmetic against buyer payback, platform dependency, and disqualifiers.

## People

- Viewer/operator: An operations, CX, product or systems generalist who can read a ticket queue, write clear instructions, configure SaaS settings, and hold a conversation with a founder about which tickets must never be automated. No certification is required to configure a helpdesk; a vendor partner tier is optional and its accessibility to a solo operator is a research question.
- Buyer: Founder, ops lead, or head of CX at a DTC brand with 1–5 support agents and roughly 1,000–5,000 tickets a month.
- End customer or beneficiary: The brand's shoppers (faster, correct answers) and its support agents (fewer repetitive tickets).
- Guest or outside participant required: no for the episode; yes for a real implementation, with the brand's permission and scoped access.

## Problem

- Costly problem: Brands adopt an AI agent inside their helpdesk, leave it on defaults with thin knowledge, get low verified-resolution rates or wrong answers, and either turn it off or keep paying agents for tickets the tool was bought to handle.
- Why it matters: Independent research finds most enterprise generative-AI deployments produce no measurable P&L impact, and a 2026 CX-industry survey reports roughly 70% adoption with about 2% seeing value. The consequence for a small brand — agent hours, wrong refunds, angry customers — is real but **not yet quantified independently at SMB scale**, which the research brief must confront.
- Why now: Both major ecommerce helpdesks moved AI to outcome-based pricing (paid per verified resolution) in 2024–2026, which means the vendor is paid only when the AI resolves — while the configuration that produces resolutions is left with the merchant. Government and bank data show small-firm AI adoption rising but still under 20%, i.e. the buyers are mid-adoption, not saturated.
- Existing alternatives and budget: Do it yourself with the vendor's wizard and webinars; buy the vendor's professional services (custom quote, aimed at larger brands); hire a certified agency from the vendor's partner directory; outsource support to a BPO; or ignore it. Brands already pay the helpdesk subscription and the per-resolution fee — budget for the tool exists; budget for the setup is the hypothesis.

## Proposed business

- Offer: A fixed-scope "AI desk implementation": 30-day ticket audit by intent, knowledge base and guidance authoring, skills for the top three intents, handover and never-automate rules, playground test suite, go-live, two weeks of monitored tuning with weekly ticket reviews, and a before/after report.
- Customer outcome: A configured AI agent with a documented rule set, a verified-resolution rate measured before and after on the vendor's own meter, and a list of what was deliberately left to humans.
- Delivery hypothesis: The vendor's published go-live checklist is the skeleton; the value is the judgment — which intents are safe, what the guidance says, where the handover triggers. AI tools draft the knowledge base from existing macros and policies; the operator decides.
- Revenue hypothesis: Fixed fee. An optional monthly optimization retainer is excluded from the base case until a recurring job is observed.
- Most important unproven assumption: **That a brand small enough to get self-serve onboarding will pay a stranger a four-figure fee to configure a tool it already pays for, rather than using the vendor's wizard or waiting for the vendor to make setup automatic.**

## Initial synthesis hypothesis

- Parallel A: The helpdesk vendor's own service-partner directory and professional-services menu → the exact offer (implementation and optimization) is already sold by third parties and by the vendor.
- Parallel B: Compliance-style readiness implementation (fixed scope against a published checklist) → delivery shape and fixed-fee pricing.
- Parallel C: Outcome-priced software where the buyer's bill is the outcome meter → the before/after measurement instrument comes free with the tool.
- New combination: A solo, vendor-agnostic implementer serving the tier of brands the vendor hands to self-serve, pricing against the buyer's own payback (resolutions × agent minutes saved), and treating the never-automate list as the product.
- Suspected transfer risk: Partner-directory agencies are larger, certified and referred by the vendor; nothing yet shows a solo operator is admitted to the program or wins those buyers. And the vendor's wizard could make the work disappear.

These are research directions, not evidence. The completed research brief and analogy map decide whether the transfers are valid.

## Narrative potential

- Starting state: A brand with two support agents turns on the AI agent that came with its helpdesk, adds nothing to it, and watches it hand most tickets back to humans — or worse, answer a refund question wrong.
- Inciting change: The vendor moves to per-resolution pricing and the founder notices they are paying for resolutions that mostly don't happen, while the two agents are still buried in "where is my order."
- Causal mechanism: The AI agent is only as good as the knowledge, guidance and handover rules it is given; the vendor's own documentation says it needs at least one knowledge source and hands over anything it cannot complete. Nobody at a small brand owns that work.
- Operator build: Audit the queue, decide what is safe, write the rules, test, go live, tune for two weeks, measure on the vendor's meter.
- Stakes and tradeoffs: Cost versus quality (Klarna went too far and rehired humans); automate too little and the fee is wasted, too much and the brand ships wrong refunds; build on one vendor whose next release could do the job; get paid a fixed fee for an outcome you only partly control.
- End state: A measured before/after — verified resolutions, first-response time, escalation errors — and a viewer who can decide whether to build this, at what minimum buyer size, and what would kill it.
- Visual evidence: A live ticket queue grouped by intent; the AI agent settings screen with an empty knowledge panel; a handover log; the playground test conversation that fails then passes; the vendor's resolution meter before and after; the never-automate list on one page.

## Audience pull

- Exact or adjacent viewer questions: how to set up Gorgias/Zendesk AI agent; why the AI agent isn't resolving tickets; what AI customer service implementation costs; how to start an AI automation agency (the crowded neighbor).
- Initial interest signals: Government and bank adoption data (buyer-side); the vendor's partner marketplace and prioritized-lead offer (commercial behavior); autocomplete showing "pricing / reviews / actions" intent for the vendor's AI agent; large but opportunity-led YouTube attention around "AI agency." All require qualification in research.
- Timely tension: Adoption is high, value is rare, and the vendors have priced themselves on outcomes while leaving the outcome-producing work with the customer.
- Coverage gap: Current coverage is (a) competitor-written pricing explainers, (b) vendor tutorials, (c) "start an AI agency" courses. None found frames outcome-based pricing as leaving a configuration job the vendor does not do for small brands, nor addresses the operator who would sell that job as a bounded service with a before/after measure.
- Honest working premise: The AI agent your helpdesk sold you only gets paid when it resolves a ticket. Here is the work that decides whether it ever does — and the business of doing it for brands the vendor won't onboard by hand.

## Discovery and POV

- Search-volume status: attempted but not measurable — Google Trends returned HTTP 429 on two attempts on 2026-09-03; no licensed volume tool is available to this operation. Proxies recorded in research.
- Operator Economy POV (scored under Step 0.3): transferable earned judgment plus a candidate original synthesis.
  - Transferable earned judgment: Manav was AI Product Manager at Lovingly (Sep 2024 – Sep 2025), a platform serving 1,500+ florists, in a cross-functional role that `facts.md` records as spanning customer support, with "ticket triage" recorded as one of his AI automation areas. He was Director of Customer Experience at Coqui Coqui (2014–2016) and co-founded Subziwalla, a D2C grocery marketplace. That is buyer-side and builder-side experience with support operations at small merchants and with AI triage on a ticket queue.
  - Original synthesis (to be demonstrated in research): outcome-based per-resolution pricing shifts the vendor's revenue onto verified resolutions but leaves the resolution-producing configuration with the merchant; the vendor's own partner directory and professional-services menu show that work is already routed to third parties — for brands big enough to qualify. The small brand is the gap.
- POV boundary: `facts.md` does not specify whether the Lovingly "ticket triage" was customer-support or internal tickets; the 80% time-saved figure is about PM tasks, not support, and must not be transposed. Manav has never sold or delivered a helpdesk implementation to a client, holds no Gorgias or Zendesk partner status, and has no observed fee, hours or client outcome for this service. Nothing about vendor pricing may be presented as current without a refresh.

## Initial evidence status

- Buyer-problem evidence: lead found — enterprise-scale "adopted but no value" findings are independent; SMB-scale consequence is not yet quantified.
- Budget or current-alternative evidence: usable component — vendor primary pricing for the helpdesk and per-resolution AI fees; vendor's own onboarding menu.
- Offer and delivery parallel: usable direct — vendor partner directory sells "setup and optimization"; vendor documents the go-live workflow.
- Economics or capacity inputs: modelable — fee and hours will be modeled; buyer payback can be modeled from vendor prices with an explicit unknown for the brand's cost per ticket.
- Audience-interest signals: one signal, needs triangulation.
- Narrative engine: plausible — one brand, one queue, one tool bought and left at defaults, a measured ending.

## Known blockers

1. **Vendor dependency.** The whole offer configures one vendor's product. The vendor sells the same implementation to larger brands and ships a self-serve wizard; a release that auto-configures from store content would shrink the job. Must be researched and carried as a kill condition.
2. **No observed solo fee.** Directory partners hide prices behind calls; the legacy $2–5K bands are creator material and are not usable.
3. **SMB consequence unquantified.** Cost-per-ticket benchmarks in circulation are vendor blogs.
4. **Transfer hop.** The strongest "adopted but no value" evidence is enterprise; the buyer here is a small brand.
5. **Partner-program access.** Whether a solo operator is admitted to the vendor's partner marketplace is unknown.

## Intake decision

Decision: research

Reason: The legacy premise had no buyer; this one has a buyer defined by the vendor's own onboarding threshold, a deliverable defined by the vendor's own go-live checklist, and a measure defined by the vendor's own billing meter — which is unusually concrete. The risks are real and specific: the vendor may close the gap itself, and no one has shown a small brand paying a solo operator for this. Both are researchable. Proceed to the research brief; do not assume it passes.
