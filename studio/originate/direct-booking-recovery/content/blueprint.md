# Direct Booking Recovery: The Blueprint

## The Idea

Build and run a standing agent task force that generates direct demand for independent hotels — profile upkeep where guests search, outreach to past and lookalike guests, review and referral prompting — and price it against the OTA commission it displaces, not the hours it takes. The booking engine (Mews, Cloudbeds, SiteMinder) is the destination the demand lands on. It is not the product being sold.

**Who it's for:** Independent hotel owners with roughly 10-40 rooms who have no in-house revenue manager and are losing an estimated 18-30% commission on the roughly two-thirds of their bookings that go through OTAs.

## The Evidence

| Claim | Number | Source |
|---|---|---|
| Independents lose bookings to OTAs | 63.4% of reservations | Cloudbeds, 2026 State of Independent Hotels (~90M bookings) |
| All-in OTA commission, loyalty programs included | 18-30% (vs. 15-25% headline rate) | Cloudbeds, 2026 report |
| OTA cancellation rate vs. direct | 21.8% vs. 10.6% | Cloudbeds, 2026 report |
| Illustrative commission loss — 20-room / $180 ADR / 70% occupancy | ~$135,000/year | Estimate — arithmetic model, not a reported figure |
| Mews Series D | $300M at $2.5B valuation, Jan 2026 — largest funding round in hospitality software history | Mews press release / PR Newswire; Hotel Dive |
| Mews scale | $19.7B annual transaction volume, 42M+ bookings, 15,000 customers, 85 countries | Mews press release |
| Cloudbeds scale | $250M raised (incl. SoftBank), 27,000 properties | Cloudbeds company reporting |
| Freelance hotel revenue management, salaried | avg $129,482/yr ($94,500-$140,000 range) | ZipRecruiter |
| Outsourced revenue-management consultants | $400-700/hr — generic benchmark, not hotel-specific | Estimate |
| Reported RevPAR uplift, outsourced revenue management | 5-15% (vendor-claimed, unverified) | TCRM, Revenuenaire, Catala, HotelMinder, MS Hospitality |
| Public per-property pricing from any named vendor | None found | Direct vendor-site scan |

## The Tool Stack

| Tool | Role | Monthly Cost |
|---|---|---|
| Make or n8n | Orchestration — runs each agent's sequence on a schedule | Free tier to ~$50/mo |
| Claude (or any model with an API) | Drafting layer — outreach copy, profile text, review replies | Usage-based |
| Google Business Profile | Where discovery actually happens — hours, photos, rates | Free |
| Beehiiv or Resend | Re-book flow to past guests — the cheapest booking a hotel gets | Free tier to ~$49/mo |
| Mews or Cloudbeds | The destination — takes the direct booking, no commission | $150-400/mo, property-dependent (estimate) |

All prices are public list pricing as of the research date, except where marked estimate.

**Total, licensed together:** roughly a few hundred dollars a month, by rough estimate. That number is not the real cost. The real cost is labor — someone has to direct the agents, read their output, correct the tone, and decide what the outreach actually says.

## The Playbook

**Week 1 — Audit, not purchase.**
Map where a guest first finds the property: organic search, an OTA listing, a friend's post, a review site. Find the point where they fall away instead of landing on a direct booking. Pull the property's real OTA mix and compute its actual annual commission exposure. That number is the business case — for the hotel, and for you.

**Week 2 — Fix the destination first.**
Before any agent runs outreach, the thing it's driving traffic to has to hold up. Brand and website first. Then check that the full path — a social post to the website, the website to a phone call or booking, the booking through to check-in — reads as one continuous conversation instead of four disconnected systems.

**Week 3 — Stand up the agents, one role at a time.**
- Profile agent: keeps Google Business Profile (and other platforms guests search) current — photos, descriptions, pricing signals.
- Outreach agent: runs the re-book flow to past and lookalike guests through Beehiiv or Resend.
- Engagement agent: prompts reviews and referrals after checkout.

None of them answers the phone. That's not what this stack is for.

**Week 4 — Price it, and publish it.**
None of the four vendors most commonly named in this space — TCRM, Revenuenaire, Catala, HotelMinder — post a price. Every one quotes privately after a sales call. Publish yours. In a market where nobody prices in public, a number on your website is the pitch.

**Ongoing — Shift the mix, don't cut the OTAs.**
The goal isn't to leave Booking.com and Expedia — they still bring discovery no small property can buy on its own. It's to shift the mix, pulling repeat and referred guests back to the direct channel one booking at a time.

## Honest Economics

No public per-property price exists for this service today — that absence is itself the opportunity, not a gap in the research.

Software runs a few hundred dollars a month per property, by rough estimate. The real cost is labor: directing the agents, correcting tone, deciding what outreach says. That's the line most operators underprice.

Running this as a side operation for 3-4 properties is realistic supplemental income. Running it for 10-12 properties tracks toward the freelance revenue-management range reported by ZipRecruiter — roughly $95,000-$140,000/year. That figure is salaried pay data reframed as a full-time-equivalent workload, not a client rate, and not a promise of what any single engagement pays.

**The failure mode:** a hotel signs, sees one good month, and doesn't renew because nobody proved the number moved. Whether your pricing model survives that renewal conversation is the actual test — track and report the commission-avoided number monthly, not just the booking count.

## Sources

1. Cloudbeds, 2026 State of Independent Hotels report (~90M bookings analyzed) — https://www.cloudbeds.com/online-travel-agencies/commissions/
2. Mews Series D press release — PR Newswire — https://www.prnewswire.com/news-releases/mews-secures-300-million-investment-to-cement-position-as-worlds-leading-hospitality-operating-system-302668120.html
3. Hotel Dive, Mews Series D coverage — https://www.hoteldive.com/news/mews-series-d-300-million-funding/810338/
4. Cloudbeds company reporting (funding, customer count), as compiled in research
5. ZipRecruiter, Freelance Remote Hotel Revenue Management — https://www.ziprecruiter.com/Jobs/Freelance-Remote-Hotel-Revenue-Management
6. Vendor pricing scan: TCRM, Revenuenaire, Catala, HotelMinder, MS Hospitality — no public per-property pricing found on any site

---

Full episode and more breakdowns like this: grapevines.ai/intel