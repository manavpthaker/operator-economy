# Script review: Hotels Pay 30% to Book Their Own Rooms

**GATE 1 — your POV pass.** Edit `script.json` directly:
- Replace every `[POV: ...]` token with your own experience/take (required — this is the monetization moat).
**POV insertions required: 2**
- Rewrite anything that doesn't sound like you.
- Check every number against the source. Delete claims you can't stand behind.

**Title options:** Hotels Pay 30% to Book Their Own Rooms | Independent Hotels Lose $135K a Year | Hotels Still Pay an 18-30% Commission

## hook
- (1) Independent hotels hand about two thirds of their bookings to Booking.com and Expedia, and pay 18 to 30 percent commission to do it. A 20-room hotel at 70 percent occupancy loses roughly $135,000 a year to that math.
  - source: Cloudbeds 2026 State of Independent Hotels report (~90M bookings), https://www.cloudbeds.com/online-travel-agencies/commissions/; $135,000 figure is an illustrative arithmetic model, not a vendor-reported number

## thesis
- (1) This is direct booking recovery: installing and running the stack that gets a hotel's own website booking rooms instead of Booking.com or Expedia doing it for a cut. Rate parity monitoring, a real booking engine, a missed-call system, and a re-book flow to past guests — the plumbing one person can run for a dozen properties at once.
- (2) It serves independent hotels in the ten-to-forty-room band — big enough that commission is real money, small enough that nobody on staff owns revenue management. Five years ago this required a channel-manager contract and a consultant on retainer. Now Mews, Cloudbeds, and SiteMinder run the parity checks, and a voice agent answers the phone the front desk can't get to.
- (3)  ⚠️ POV NEEDED 'Built' scales with effort. A side operator runs the audit and setup for three or four properties and checks in monthly. A full build looks like a standing agency managing twenty hotels' direct channels on retainer, reporting one number every month: the direct-booking share, before and after. [POV: describe what running four properties in the Yucatán taught you about who actually owns this problem, and why nobody on staff was watching that number]

## evidence
- (1) Cloudbeds — who sell the software that fixes this — looked at ninety million bookings for their 2026 State of Independent Hotels report and found that independents lose 63.4 percent of reservations to OTAs. Once you add Booking.com's Genius program and Visibility Booster, or Expedia's Accelerator, the real commission runs 18 to 30 percent, well above the 15-to-25 headline rate hotels think they're paying.
  - source: Cloudbeds 2026 State of Independent Hotels report, https://www.cloudbeds.com/online-travel-agencies/commissions/ — vendor-published, attribute aloud
- (2) Same dataset: OTA bookings cancel at 21.8 percent, almost double the 10.6 percent for direct. The commission doesn't just cost money — it buys a less reliable booking. Run the arithmetic on a real property: 20 rooms, $180 average rate, 70 percent occupancy, books around $920,000 a year. Two thirds through OTAs at 22 percent all-in is about $135,000 gone to commission.
  - source: Cancellation rates: Cloudbeds 2026 report; $135,000 figure is an illustrative estimate built from those assumptions, not a company-reported number
- (3)  ⚠️ POV NEEDED [POV: describe standing at the front desk during checkout rush at Coqui Coqui, hearing the phone ring underneath the line, and knowing some of those calls were direct bookings walking straight to Booking.com or the hotel down the street] That's the same gap the missed-call fix in episode two closed. This episode is about where that booking went instead, and what it cost to lose it.
- (4) On the high end, Mews just raised $300 million in a Series D led by EQT Growth, valuing the company at $2.5 billion — the largest funding round hospitality software has ever seen. Announced January 2026. New investors Atomico and HarbourVest joined existing backers Kinnevik, Battery Ventures, and Tiger Global.
  - source: Mews press release via PR Newswire, https://www.prnewswire.com/news-releases/mews-secures-300-million-investment-to-cement-position-as-worlds-leading-hospitality-operating-system-302668120.html; Hotel Dive, https://www.hoteldive.com/news/mews-series-d-300-million-funding/810338/
- (5) Mews now moves $19.7 billion a year across 42 million bookings and 15,000 customers in 85 countries. Cloudbeds has raised $250 million, including SoftBank, and serves 27,000 properties. Mews earmarked this round for AI agents that automate hotel operations — but somebody still has to install that plumbing in a 20-room property that has never had a revenue manager.
  - source: Mews figures: PR Newswire release + Hotel Dive (see prior beat); Cloudbeds figures: company reporting as compiled in research brief
- (6) The low end is thinner, and in the wrong unit. Freelance remote hotel revenue managers earn an average $129,482 a year, according to ZipRecruiter — that's a salary, not a price you charge a hotel. Senior independent consultants generally bill $400 to $700 an hour, with retainers discounted 10 to 15 percent — but that's a generic consulting benchmark, not one built for hotels.
  - source: ZipRecruiter, https://www.ziprecruiter.com/Jobs/Freelance-Remote-Hotel-Revenue-Management; consulting hourly range is a generic cross-industry benchmark, not hotel-specific, marked as estimate
- (7) Providers like TCRM, Revenuenaire, and HotelMinder claim 5 to 15 percent RevPAR uplift, but every one of them quotes privately — nobody in this market publishes a price. That's not a hole in the research. That's the finding: a market where nobody prices in public is a market a published price can walk straight into.
  - source: Reported vendor claims (TCRM, Revenuenaire, Catala, HotelMinder, MS Hospitality) — private pricing observed on each site; no public per-property rate found, mark as reported gap

## stack
- (1) The core is a property-management system with a real booking engine attached — Mews or Cloudbeds, both running partner programs worth checking before you build on them. For properties under about 30 rooms, Little Hotelier is the lighter, cheaper tier. This is what replaces the OTA's booking flow on the hotel's own site — the piece that actually captures the direct reservation instead of losing it to a search result.
- (2) On top of that sits SiteMinder, the channel manager that keeps rates identical across every OTA and the hotel's own site — rate parity is where deals leak first, so a monitor watching for mismatches runs continuously, not on a schedule. This is the layer that stops a hotel from accidentally undercutting its own direct rate.
- (3) The phone is the same fix as episode two: Twilio underneath a voice agent that answers when the front desk can't, because a chunk of the bookings lost to OTAs never even got to a website — they were calls that rang out. Pair it with a simple booking widget, like Cal.com, so a caller who wants to book can just do it.
- (4) The last piece is the cheapest booking a hotel will ever get: a past guest. A basic email tool — Beehiiv or similar — runs the re-book flow, reminding people who already stayed once that they can book direct next time, no commission attached. It's unglamorous and it's where the highest-margin bookings actually come from.
- (5) All together, licensing this stack for one property runs a few hundred dollars a month — a rounding error against a $135,000 commission bill, which is the entire pitch.
  - source: Estimate: typical SMB PMS/channel-manager/voice-agent stack pricing; not itemized in research brief

## playbook
- (1) Week one: pick five to ten independent hotels in the ten-to-forty-room band — big enough that commission is real money, small enough that nobody on staff owns this. Pull each one's OTA booking mix and run the commission arithmetic from the evidence section against their actual numbers. That number, not a pitch deck, is the sales call.
- (2) Be straight with the hotel about what this is and isn't: OTAs stay. They're distribution and discovery, not the enemy. The pitch isn't 'drop Booking.com' — it's shifting the mix, and shifting the mix by even ten points is real money at these margins.
- (3) Month one is the first signed property. Fix the leaks in the order they cost money: rate parity first, because a mismatched rate is actively pushing bookings to the OTA; then the booking engine itself; then the missed-call line, which is the direct callback to episode two; then the re-book flow to past guests. Each fix is visible in the numbers within weeks, not quarters.
- (4) Price against the commission saved, not against hours worked — a hotel losing $135,000 a year will pay a fraction of that gladly. Then do the thing nobody else in this market does: publish the price. Every outsourced revenue-management provider checked for this episode — TCRM, Revenuenaire, Catala, HotelMinder — quotes privately. A number on a website, in a market with none, is itself the pitch.
  - source: Reported vendor scan (TCRM, Revenuenaire, Catala, HotelMinder) — private pricing observed, no public rate found
- (5) Realistically the first dollar lands three to six weeks in, as soon as the first signed property's parity fix goes live and the direct-booking number starts moving.
  - source: Estimate based on typical implementation timeline for rate-parity and booking-engine fixes; not itemized in research brief
- (6) After that it's one report a month: direct-booking share, before and after. That single number is what turns a first property into a referral, and a referral into the second, third, and fourth — the same local-density model as episode two, just with a bigger check attached.
- (7) The harder question isn't landing the first property — it's what happens at the tenth, when audits, parity fixes, and monthly reports for a dozen hotels are competing for the same week. Whether that scales as an agency or caps out as a solid side income is the next question.

## economics
- (1) There's a full walkthrough of this audit, the pricing structure, and the outreach approach in the blueprint linked below, for anyone who'd rather start from a built checklist than piece one together.
- (2) On effort, not promise: running the audit and fixes for three or four properties as a side operation is realistic supplemental income, closer to the freelance revenue-management range of roughly $95,000 to $140,000 a year for a full-time equivalent — not what any single hotel pays, but what the workload adds up to at ten or twelve clients.
  - source: ZipRecruiter freelance revenue-management salary range, https://www.ziprecruiter.com/Jobs/Freelance-Remote-Hotel-Revenue-Management, reframed as a full-time-equivalent workload estimate — this is salaried pay data, not a client rate
- (3) What it actually diversifies is skills and optionality more than a single income stream: revenue-management literacy, a channel-manager and voice-agent stack you can resell into other verticals, and a client roster that doesn't disappear if any one algorithm change wipes out a single OTA relationship.
- (4) Costs stay real: software licenses run a few hundred dollars a month per property, and the failure mode is a hotel that signs, sees one good month, and doesn't renew because nobody proved the number moved. Whether the pricing model survives that renewal conversation is the actual test.
  - source: Estimate: cost and churn-risk reasoning based on typical SaaS/service retainer dynamics; not itemized in research brief

## cta
- (1) The full audit template, the pricing structure, and the outreach script are all in the direct-booking blueprint linked below — the same checklist used to build this episode. Subscribe for the next installment in this series: one person, one commission-heavy market, built out step by step.

---
When done, continue with:
```
python originate.py <slug> --continue
```