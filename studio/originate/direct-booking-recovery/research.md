# Research brief: "Independent hotels pay 18–30% to fill their own rooms"

Episode #6. Thesis: independent hotels hand roughly two thirds of their bookings to OTAs and pay
18–30% all-in for them. A solo operator can install and run the direct-booking stack — booking
engine, rate parity, recovery flows, the phone — and charge a fee that is a rounding error against
the commission saved. The infrastructure underneath just raised $300M at a $2.5B valuation.

Same shape as EP001 and EP002: a service a giant is being paid enormous money to provide, that one
person can now provide at local scale, because the tooling got cheap.

## The demand wedge (confidence: MEDIUM-HIGH — one large first-party dataset, vendor-published)

- **Independents lose 63.4% of bookings to OTAs.** From the Cloudbeds 2026 State of Independent
  Hotels report, compiled from ~90 million bookings. Source:
  https://www.cloudbeds.com/online-travel-agencies/commissions/ — a large real dataset, but
  published by a company selling the fix. Attribute it aloud ("Cloudbeds, who sell the alternative,
  looked at 90 million bookings and found…").
- **All-in commission is 18–30% at Booking.com** once Genius and Visibility Booster are added, and
  **17–23% at Expedia** with Accelerator. Headline rates of 15–25% understate it. Same source family.
- **OTA cancellation rate 21.8% vs 10.6% direct** — an OTA booking is twice as likely to evaporate.
  This is the detail that makes the pitch land: the commission buys a worse booking.
- The arithmetic to run on camera as arithmetic, not fact: a 20-room property at $180 ADR and 70%
  occupancy books roughly $920K/yr. Two thirds through OTAs at ~22% all-in is about **$135K a year in
  commission**. Present as an illustrative model with the assumptions stated, per the estimate-marker rule.

## Evidence — HIGH END (confidence: HIGH, first-party press release + trade press)

- **Mews: $300M Series D led by EQT Growth, announced 22 January 2026, valuing the company at
  $2.5B** — the largest funding round in hospitality software. New investors Atomico and HarbourVest;
  existing Kinnevik, Battery Ventures, Tiger Global. Sources: Mews press release via PR Newswire
  (https://www.prnewswire.com/news-releases/mews-secures-300-million-investment-to-cement-position-as-worlds-leading-hospitality-operating-system-302668120.html),
  Hotel Dive (https://www.hoteldive.com/news/mews-series-d-300-million-funding/810338/).
- **Mews 2025 scale: $19.7B transaction volume, 42M+ bookings, 15,000 customers across 85 countries,
  SaaS gross profit +55%.** Same sources. First-party figures — attribute to the company.
- **Cloudbeds: $250M raised including SoftBank Vision Fund; 27,000 customers across 150 countries;
  ~$85M 2024 revenue.** Directly targets independents.
- The structural read, and the episode's spine: **the money is going into the plumbing, and the
  plumbing still needs installing.** Mews explicitly earmarked the round for AI agents that automate
  hotel operations. Somebody has to put that in a 20-room property that has never had a revenue
  manager. That somebody is the audience.

## Evidence — LOW END (confidence: MIXED — real but in the wrong unit; name the gap aloud)

- **Freelance remote hotel revenue management averages $129,482/yr in the US, most between $94,500
  and $140,000.** Source: ZipRecruiter
  (https://www.ziprecruiter.com/Jobs/Freelance-Remote-Hotel-Revenue-Management). This is what an
  operator EARNS, not what an operator CHARGES a hotel — say so rather than letting it pass as a
  price.
- Senior independent consultants across industries bill **$400–$700/hr**; monthly retainers usually
  carry a 10–15% discount against hourly. Generic consulting benchmark, not hotel-specific.
- **Outsourced revenue managers are reported to deliver 5–15% RevPAR uplift in 6–12 months.** Vendor
  claim, from providers selling the service — mark reported.
- **THE HONEST GAP, and it is worth naming on camera: nobody in this market publishes a price.**
  Every outsourced revenue-management provider checked — TCRM, Revenuenaire, Catala, HotelMinder, MS
  Hospitality — quotes privately. There is no public per-property retainer to cite, the way EP002
  could cite $300–1,000/mo for voice. That opacity is itself the finding: a market where nobody
  publishes pricing is a market where a clear, published price is a wedge. Do not invent a number to
  fill the hole.

## Manav's POV material (Gate 1 will inject — this is the strongest POV in the queue)

- **Ran four properties in the Yucatán (Coqui Coqui), 50+ staff, two years.** He has been the person
  paying the commission, not the person selling the fix.
- **He already tells the adjacent story on EP002**, and it is the natural bridge: at checkout rush the
  front desk was a queue, the phone rang underneath it, and he knew some of those unanswered rings
  were direct bookings that ended up on a booking site or at the hotel down the road. EP002 solved the
  ringing. This episode is about where that booking went instead, and what it cost.
- Concrete POV questions worth answering on camera because only an operator can: what did the OTA
  actually do for the property that made the commission feel survivable; what would he have paid an
  outsider to fix it and why did he not; and what the property's own booking engine was like to use.

## Tool stack (verify affiliate terms before the stack section)

**Mews** or **Cloudbeds** (PMS + booking engine; both run partner/referral programmes — verify current
terms) · **SiteMinder** (channel manager, rate parity across OTAs) · **Little Hotelier** (the
small-property tier) · a **rate-parity monitor** · **Twilio + a voice agent** for the missed-call half,
which is the explicit callback to EP002 · **Cal.com / a booking widget** for direct capture · basic
email (Beehiiv or similar) for the re-book flow to past guests, who are the cheapest direct bookings
that exist.

## Playbook skeleton (for playbook section)

1. Pick properties in the band that hurts most — independents around 10–40 rooms, big enough that
   commission is real money and small enough to have nobody doing this job.
2. Audit before you sell: pull their OTA mix and compute the annual commission. The number is the
   sales call.
3. Fix the leaks in order of cost — rate parity first, then the booking engine, then the missed-call
   line, then the re-book flow to past guests.
4. Price against the commission saved, not against your hours, and publish the price. The market's
   opacity is the opening.
5. Report one number monthly: direct share of bookings, before and after.

## Register and honesty notes

- The commission arithmetic is a MODEL. State the assumptions aloud and mark it an estimate.
- The Cloudbeds dataset is large and real but vendor-published; attribute it.
- Do not imply a hotel can drop OTAs. They are distribution and discovery; the honest claim is
  shifting the mix, not leaving. A video that says "cancel Booking.com" would be wrong and every
  hotelier watching would know it.
- The low-end evidence is thinner than EP001's and in the wrong unit. Say so, the way EP002 said its
  solo evidence was thin. It is also why the niche is open.
