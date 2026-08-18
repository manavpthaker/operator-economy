"""Hand-tuned storyboard for №006 (direct-booking-recovery).

Rev 1 (2026-08-16). The generated storyboard shipped 20 of 22 screens on a
SINGLE reveal, several holding 24-43s, which is the static-composition
warning in `eval_edit.py` eighteen times over and the reason the edit
rubric scored 17/23 against a gate of 18. Three things are fixed here:

  1. Every screen that holds past ~20s is re-beaten into word-anchored
     reveals, the way `stack-01` already was. Reveals are what the
     renderer stages, so this is the difference between a slide that sits
     there and a composition that assembles while the line is spoken.
  2. Seven `quote` impact frames land on the punchlines the VO actually
     hits. The rubric wants 10 quote|proof screens for a 12-minute
     episode and the generated cut had 4 (all proof_cards).
  3. Screen boundaries are moved onto SENTENCE boundaries. The generated
     cut broke thesis-01/02 mid-clause ("...one person can run" /
     "it for a dozen properties"), because it split on duration rather
     than on speech.

Idempotent: reads `storyboard.generated.json` (the pristine plan_assets
output) and writes `storyboard.json`. Re-running does not compound.
Do NOT run storyboard.py after this — it clobbers (see docs/pipeline.md).
`events` are deliberately NOT emitted: pace_storyboard.py recomputes them
from scratch against whatever reveals exist, so authoring them here would
just be overwritten.

Run:  python originate/direct-booking-recovery/hand_tune_storyboard.py
Then: pace_storyboard.py -> prepare_longform.py
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).parent
GENERATED = HERE / "storyboard.generated.json"
OUT = HERE / "storyboard.json"

GEN = json.loads(GENERATED.read_text())
WORDS = json.loads((HERE / "vo" / "words.json").read_text())
TIMELINE = json.loads((HERE / "vo" / "timeline.json").read_text())
TOTAL = TIMELINE["total_seconds"]

DONORS = {s["id"]: s for s in GEN["screens"]}

_BY_SECTION: dict[str, list[dict]] = {}
for _w in WORDS:
    _BY_SECTION.setdefault(_w["section"], []).append(_w)


def _norm(w: str) -> str:
    return re.sub(r"[^\w']", "", w).strip("'").lower()


_MISSES: list[str] = []


def find_phrase(section: str, phrase: str) -> tuple[float, float]:
    """First occurrence of `phrase` inside `section`, as (start, end)."""
    tokens = [_norm(t) for t in phrase.split() if _norm(t)]
    ws = _BY_SECTION.get(section, [])
    normed = [_norm(w["word"]) for w in ws]
    for i in range(len(normed) - len(tokens) + 1):
        if normed[i:i + len(tokens)] == tokens:
            return ws[i]["start"], ws[i + len(tokens) - 1]["end"]
    _MISSES.append(f"{section}: {phrase!r}")
    return -1.0, -1.0


# ---------------------------------------------------------------- the plan
# Each entry is one screen. `beats` are (anchor phrase, title, body, tags);
# the anchor's first word sets the reveal's `at`, so every staged element
# appears exactly as its line is spoken. A screen's span runs from its
# first beat to the next screen's first beat, which is what pins the cuts
# to sentence starts.
#
# `q` entries are impact frames: layout `quote`, held only as long as the
# line takes to say (the rubric wants 1.2-4s and hard-cuts them).

C, N, P, R, T = ["claim"], ["number"], ["process"], ["risk"], ["tool"]

PLAN: list[dict] = [
  # ---- HOOK: five reveals inside 24.8s. The rubric wants >=4 in the
  # first 30s for a 4-8s visual cadence; the generated cut had 1.
  dict(id="hook-01", layout="broll", section="hook", donor="hook-01",
       heading="Independent hotels", beats=[
    ("Independent hotels hand about two thirds",
     "Two thirds of bookings go to the OTAs", "Booking.com · Expedia", C + N),
  ]),
  dict(id="hook-02", layout="chart", section="hook", donor="hook-01",
       heading="The gap", beats=[
    ("And they pay eighteen to thirty percent commission",
     "18 to 30 percent commission to do it", "on every one of them", N),
    ("On a twenty room hotel",
     "20 rooms · 70 percent occupancy", "their own published rates", N),
  ]),
  dict(id="hook-03", layout="proof_card", section="hook", donor="hook-01",
       heading="The annual consequence",
       custom={"proof": {"value": 135000, "prefix": "$",
                          "label": "Estimated annual OTA commission",
                          "contrast": "20 rooms · $180 · 70% occupancy",
                          "estimate": True}}, beats=[
    ("that's roughly a hundred thirty five thousand dollars a year",
     "About $135,000 a year", "commission, gone", N),
  ]),
  dict(id="hook-04", layout="quote", section="hook",
       anchor="My estimate", quote="My estimate — built from published rates.",
       heading="The caveat", accent="My estimate"),

  # ---- THESIS
  dict(id="thesis-01", layout="sheet", section="thesis", donor="thesis-01",
       heading="The thesis", beats=[
    ("Okay so this is direct booking recovery",
     "Direct booking recovery", "install it and run it", C),
    ("You install and run the stack",
     "The hotel's own site books the rooms", "instead of Booking.com or Expedia", C),
    ("Rate parity monitoring",
     "Rate parity monitoring", "a real booking engine", P),
    ("A missed call system",
     "A missed-call system", "a re-book flow to past guests", P),
    ("That's the plumbing",
     "One person, a dozen properties", "that's the plumbing", C),
  ]),
  dict(id="thesis-02", layout="artifact", section="thesis", donor="thesis-02",
       custom={"artifact": {
         "title": "Independent hotels, 10 to 40 rooms",
         "callout": "big enough that the commission is real money · "
                    "small enough that nobody owns revenue management"}},
       heading="Who it's for", beats=[
    ("Who's it for",
     "Independent hotels, 10 to 40 rooms", "the band that fits", C),
    ("Big enough that the commission is real money",
     "Big enough that the commission is real money",
     "10 to 40 rooms", N),
    ("Small enough that nobody on staff",
     "Small enough that nobody owns revenue management",
     "nobody on staff owns it", C),
    ("Five years ago",
     "Five years ago: a contract and a retainer",
     "channel-manager · consultant", C),
    ("Now Mews Cloudbeds SiteMinder",
     "Now: Mews, Cloudbeds, SiteMinder", "they run the parity checks", T),
    ("Nobody on staff was watching that number",
     "Nobody was watching that number",
     "and it wasn't negligence", R),
  ]),
  dict(id="thesis-q1", layout="quote", section="thesis",
       anchor="that wasn't negligence", quote="That wasn't negligence.",
       heading="The thesis", accent="negligence"),
  dict(id="thesis-03", layout="sheet", section="thesis", donor="thesis-03",
       heading="Why it went unowned", beats=[
    ("A small property leans on the OTAs for a reason",
     "A small hotel leans on the OTAs for a reason",
     "the front desk has nobody spare", C),
    ("You don't have the manpower",
     "No manpower to take it all in",
     "so the OTAs did the work", C),
    ("And you don't have the skillset to build direct",
     "No skillset to build direct",
     "and the OTAs kept it", C),
  ]),
  dict(id="thesis-04", layout="sheet", section="thesis", donor="thesis-03",
       heading="It isn't a website", beats=[
    ("And direct booking",
     "Direct booking isn't a website", "it's marketing", C),
    ("Build it and they will come",
     "Build it and they will come — not here",
     "putting yourself out there, continuously", C),
    ("That's the job nobody had time for",
     "The job nobody had time for", "and the job the agents are for", P),
  ]),
  dict(id="thesis-05", layout="schematic", section="thesis", donor="thesis-03",
       heading="What the agents are for", beats=[
    ("Not answering",
     "Not answering — that was never the job", "the phone is not the product", P),
    ("Your own growth engine",
     "Outreach · Profile · Follow-up — your own growth engine",
     "not a better voicemail", C),
  ]),
  dict(id="thesis-q2", layout="quote", section="thesis",
       anchor="Not a better voicemail", quote="Not a better voicemail.",
       heading="The thesis", accent="voicemail"),

  # ---- EVIDENCE
  dict(id="evidence-01", layout="chart", section="evidence", donor="evidence-01",
       heading="The evidence", beats=[
    ("Cloudbeds they sell the software",
     "Cloudbeds sells the fix", "so take it for what it's worth", C),
    ("They looked at ninety million bookings",
     "90 million bookings reviewed",
     "2026 State of Independent Hotels", N),
    ("Found that independents lose 63.4 percent",
     "Independents lose 63.4 percent of reservations to OTAs",
     "Cloudbeds · 90 million bookings", N),
    ("Now add in Booking.com's Genius program",
     "Genius · Visibility Booster · Accelerator",
     "the extras on top", T),
    ("The real commission runs 18 to 30 percent",
     "Real commission: 18 to 30 percent",
     "above the 15 to 25 headline rate", N),
  ]),
  dict(id="evidence-02", layout="proof_card", section="evidence", donor="evidence-02",
       custom={"proof": {"value": 920000, "prefix": "$",
                         "label": "Booked a year — 20 rooms, $180, 70%",
                         "contrast": "two thirds of it through OTAs",
                         "estimate": True}},
       heading="The evidence", beats=[
    ("Same dataset OTA bookings cancel at 21.8 percent",
     "OTA bookings cancel at 21.8 percent",
     "against 10.6 percent direct", N),
    ("So the commission doesn't just cost money",
     "It costs money and reliability", "a less reliable booking too", R),
    ("Let's do the arithmetic",
     "Let's do the arithmetic", "an estimate, not a reported figure", C),
    ("20 rooms $180 average rate",
     "20 rooms · $180 rate · 70 percent occupancy",
     "the illustrative model", N),
    ("That books around $920,000 a year",
     "About $920,000 booked a year",
     "two thirds of it through OTAs", N),
  ]),
  dict(id="evidence-03", layout="sheet", section="evidence", donor="evidence-03",
       heading="From the inside", beats=[
    ("Two thirds of that goes through OTAs",
     "Two thirds through OTAs at 22 percent all in",
     "about $135,000 gone from a 20-room hotel", N),
    ("At Coqui Coqui the first thing I did",
     "Coqui Coqui: brand and site first",
     "then came the harder part", P),
  ]),
  dict(id="evidence-03b", layout="schematic", section="evidence", donor="evidence-03",
       heading="Making the flow hold", beats=[
    ("Then came the harder part",
     "The harder part — the flow holds", "not four systems", P),
    ("Social to the website",
     "Social → site → booking — one conversation",
     "instead of four separate handoffs", P),
    ("I could pull that off because I had fifty people",
     "Fifty people on property — and time to think",
     "that is what it took", C),
  ]),
  dict(id="evidence-04", layout="sheet", section="evidence", donor="evidence-04",
       heading="The high end", beats=[
    ("A B&B operator running the place alone",
     "A solo B&B operator can't",
     "no team to lean on", R),
  ]),
  dict(id="evidence-q1", layout="quote", section="evidence",
       anchor="That gap right there is the whole opportunity",
       quote="That gap, right there, is the whole opportunity.",
       heading="The evidence", accent="the whole opportunity"),
  dict(id="evidence-05", layout="proof_card", section="evidence", donor="evidence-04",
       custom={"proof": {"value": 300, "prefix": "$", "suffix": "M",
                         "label": "Mews Series D, led by EQT Growth",
                         "contrast": "at a $2.5B valuation"}},
       heading="The high end", beats=[
    ("On the high end Mews just raised $300 million",
     "Mews raised $300 million, Series D",
     "led by EQT Growth", N),
    ("Valued the company at $2.5 billion",
     "Valued at $2.5 billion",
     "largest round hospitality software has seen", N),
    ("Announced January 2026",
     "Announced January 2026",
     "Atomico · HarbourVest · Kinnevik · Battery · Tiger", N),
  ]),
  dict(id="evidence-06", layout="chart", section="evidence", donor="evidence-05",
       beat0=5,  # (evidence,5) = "Scale: Customers vs Properties"
       heading="Scale", beats=[
    ("Mews now moves $19.7 billion a year",
     "Mews moves $19.7 billion a year",
     "42 million bookings · 15,000 customers · 85 countries", N),
    ("Cloudbeds has raised $250 million",
     "Cloudbeds raised $250 million",
     "SoftBank among them · 27,000 properties", N),
    ("Mews earmarked this round for AI agents",
     "The round is earmarked for AI agents",
     "to automate hotel operations", T),
    ("But somebody still has to install that plumbing",
     "Somebody still has to install the plumbing",
     "in a 20-room property that never had a revenue manager", C),
  ]),
  dict(id="evidence-07", layout="proof_card", section="evidence", donor="evidence-06",
       custom={"proof": {"value": 129482, "prefix": "$",
                         "label": "Freelance revenue manager, average",
                         "contrast": "a salary, not a price you charge"}},
       heading="The low end", beats=[
    ("The low end's thinner",
     "The low end is thinner — and in the wrong unit",
     "salary data, not prices", R),
    ("Freelance remote hotel revenue managers earn an average",
     "Freelance revenue managers: $129,482 a year",
     "ZipRecruiter", N),
    ("But that's a salary",
     "That's a salary, not a price", "not what you charge a hotel", R),
    ("So here's the honest state of the evidence",
     "Demand side documented · pricing side not",
     "the honest state of the evidence", C),
  ]),
  dict(id="evidence-08", layout="artifact", section="evidence", donor="evidence-07",
       custom={"artifact": {
         "title": "Every one of them quotes privately",
         "callout": "TCRM · Revenuenaire · HotelMinder — 5 to 15 percent "
                    "RevPAR uplift, their own unverified numbers"}},
       heading="Nobody publishes a price", beats=[
    ("Providers like TCRM Revenuenaire and HotelMinder",
     "TCRM · Revenuenaire · HotelMinder",
     "5 to 15 percent RevPAR uplift, their own numbers", T),
    ("Their own numbers unverified",
     "Unverified — and they're selling the service",
     "their own numbers", R),
    ("What is checkable",
     "What is checkable: every one quotes privately",
     "nobody publishes a price", C),
    ("And that's not a hole in the research",
     "Not a hole in the research",
     "nobody publishes a price", C),
  ]),
  dict(id="evidence-q2", layout="quote", section="evidence",
       anchor="That's the finding", quote="That's the finding.",
       heading="The evidence", accent="the finding"),
  dict(id="evidence-09", layout="sheet", section="evidence", donor="evidence-07",
       heading="Nobody publishes a price", beats=[
    ("A market where nobody prices in public",
     "A market where nobody prices in public",
     "is one a published price walks straight into", C),
  ]),

  # ---- STACK  (schematics capped at 3 nodes — a 4th is never legible)
  dict(id="stack-01", layout="schematic", section="stack", donor="stack-01",
       heading="The stack", beats=[
    ("The product's a standing task force",
     "Standing task force — generates demand", "it generates demand", C),
    ("The software it runs on",
     "Assembled, not bought — no hotel software",
     "not hospitality software", C),
    ("A booking engine doesn't generate demand on its own",
     "Booking engine — catches, doesn't create",
     "it catches the guest already looking", C),
  ]),
  dict(id="stack-02", layout="schematic", section="stack", donor="stack-01",
       heading="Keeping it fed", beats=[
    ("Something's gotta keep pushing traffic toward it",
     "Daily traffic — without a payroll line",
     "no full-time marketing hire", C),
    ("Underneath the task force two boring pieces",
     "Two boring pieces — orchestration + drafting",
     "neither is hotel software", P),
  ]),
  dict(id="stack-03", layout="schematic", section="stack", donor="stack-01",
       heading="The two layers", beats=[
    ("Make or n8n that's the orchestration layer",
     "Make or n8n — orchestration",
     "runs a sequence on a schedule", T),
    ("And Claude or any model with an API",
     "Claude or any API — drafting",
     "neither one is hospitality software", T),
    ("Then the roles split across the surfaces",
     "Three agents — three surfaces",
     "what decides whether a property gets found", P),
  ]),
  dict(id="stack-04", layout="schematic", section="stack", donor="stack-01",
       heading="The roles", beats=[
    ("One agent keeps the Google Business Profile current",
     "Google profile — hours + photos",
     "the stuff that goes stale", P),
    ("One runs the re-book flow to past guests",
     "Re-book flow — Beehiiv or Resend",
     "the cheapest booking there is", P),
    ("One prompts reviews after checkout",
     "Reviews — after checkout", "reviews and referrals", P),
  ]),
  dict(id="stack-q1", layout="quote", section="stack",
       anchor="None of them is a receptionist",
       quote="None of them is a receptionist.",
       heading="The stack", accent="receptionist"),
  dict(id="stack-05", layout="schematic", section="stack", donor="stack-01",
       heading="Where it lands", beats=[
    ("Mews or Cloudbeds sits at the end of all that",
     "Mews or Cloudbeds — the destination", "one line, on purpose", T),
    ("It's the destination not the product being sold",
     "Not the product — no commission",
     "somewhere a booking can land", C),
    ("And note what the free tier covers",
     "Google profile — costs nothing",
     "exactly where discovery leaks", N),
  ]),
  dict(id="stack-06", layout="sheet", section="stack", donor="stack-01",
       heading="The real cost", beats=[
    ("Licensed together the software runs a few hundred bucks a month",
     "Licensed together: a few hundred dollars a month",
     "rough estimate", N),
    ("And that's not the real cost",
     "That is not the real cost", "someone still has to direct them", R),
    ("Someone still has to direct these agents",
     "Read the output · correct the tone · decide the words",
     "that is the work", P),
  ]),
  dict(id="stack-07", layout="artifact", section="stack", donor="stack-01",
       custom={"artifact": {
         "title": "Four vendors, no published price",
         "callout": "TCRM · Revenuenaire · Catala · HotelMinder"}},
       heading="Nothing to compare against", beats=[
    ("That's the line operators underprice",
     "The line operators underprice", "the direction, not the software", R),
    ("And none of the four vendors most often named",
     "None of the four vendors publish a price",
     "TCRM · Revenuenaire · Catala · HotelMinder", T),
  ]),

  # ---- PLAYBOOK
  dict(id="playbook-01", layout="sheet", section="playbook", donor="playbook-01",
       heading="The playbook", beats=[
    ("Standing this up starts with an audit",
     "Start with an audit, not a purchase",
     "before anything gets bought", P),
    ("Where does a guest first find the property",
     "Where does a guest first find the property?",
     "organic · OTA listing · a friend's post · reviews", P),
    ("and at what point do they fall away",
     "And where do they fall away?",
     "that gap is what gets built to close", P),
    ("Before any agent runs outreach",
     "The destination has to hold up first",
     "brand and website before outreach", P),
    ("Then the full path",
     "Then the full path reads as one conversation",
     "not four disconnected systems", P),
    ("Then the roles get split",
     "Then the roles get split", "three agents, three surfaces", P),
  ]),
  dict(id="playbook-02", layout="schematic", section="playbook", donor="playbook-01",
       heading="Splitting the roles", beats=[
    ("One agent maintains the property's profile",
     "Profile — photos + pricing",
     "photos · descriptions · pricing signals", P),
    ("One runs outreach to past and lookalike guests",
     "Outreach — past + lookalike",
     "repeat and referred", P),
    ("One manages guest engagement",
     "Engagement — reviews and referrals", "reviews and referrals", P),
  ]),
  dict(id="playbook-03", layout="proof_card", section="playbook", donor="playbook-02",
       heading="Why a small property can't",
       custom={"proof": {"value": 50,
                         "label": "People on property at Coqui Coqui",
                         "contrast": "a single-operator B&B has none of that"}},
       beats=[
    ("At Coqui Coqui I ran this flow myself",
     "At Coqui Coqui I ran this flow myself",
     "a team of fifty on the hotel property", C),
    ("A single-operator bed-and-breakfast doesn't have that headcount",
     "A single-operator B&B has no headcount",
     "nobody spare to answer or post", R),
  ]),
  dict(id="playbook-03b", layout="sheet", section="playbook", donor="playbook-02",
       heading="It stands in for manpower", beats=[
    ("The agent task force isn't a luxury add-on there",
     "Not a luxury add-on",
     "it stands in for manpower never going to be hired", C),
  ]),
  dict(id="playbook-04", layout="artifact", section="playbook", donor="playbook-03",
       custom={"artifact": {
         "title": "None of the four post a price",
         "callout": "TCRM · Revenuenaire · Catala · HotelMinder — "
                    "every one quotes privately, after a sales call"}},
       heading="Publish the price", beats=[
    ("None of the four vendors most commonly named",
     "None of the four post a price",
     "TCRM · Revenuenaire · Catala · HotelMinder", T),
    ("Every one quotes privately",
     "Every one quotes privately, after a sales call",
     "no number on any site", C),
    ("So do the thing none of them does",
     "So do the thing none of them does — publish yours",
     "a price, in public", P),
    ("In a market where nobody prices in public",
     "In a market with no public prices, a number is the pitch",
     "pricing as positioning", C),
  ]),
  dict(id="playbook-q1", layout="quote", section="playbook",
       anchor="It's the pitch", quote="It's the pitch.",
       heading="The playbook", accent="the pitch"),
  dict(id="playbook-05", layout="proof_card", section="playbook", donor="playbook-04",
       custom={"proof": {"value": 135000, "prefix": "$",
                         "label": "Commission it offsets, per year",
                         "contrast": "against a few hundred a month",
                         "estimate": True}},
       heading="The argument", beats=[
    ("Weigh that against the commission line",
     "Weigh it against the commission line",
     "not the sticker price of the software", C),
    ("Licensing runs a few hundred dollars a month",
     "Licensing: a few hundred dollars a month",
     "cheap against what it replaces", N),
    ("The commission it's meant to offset",
     "The commission it offsets: about $135,000 a year",
     "20 rooms · $180 · 70 percent — illustrative", N),
    ("That gap between those two numbers is the argument",
     "That gap is the argument",
     "a few hundred against $135,000", C),
  ]),
  dict(id="playbook-06", layout="schematic", section="playbook", donor="playbook-05",
       heading="Shift the mix", beats=[
    ("The pitch isn't to leave the OTAs",
     "Keep the OTAs — they bring discovery",
     "no small hotel can buy it on its own", C),
    ("It's to shift the mix",
     "Shift the mix — repeat and referred, direct",
     "one booking at a time, no commission taken", P),
  ]),

  # ---- ECONOMICS
  dict(id="economics-01", layout="sheet", section="economics", donor="economics-01",
       heading="The economics", beats=[
    ("There's a full walkthrough of this",
     "The full walkthrough is in the blueprint",
     "audit · pricing · outreach", P),
  ]),
  dict(id="economics-02", layout="chart", section="economics", donor="economics-02",
       beat0=2,  # (economics,2) = "Full-Time-Equivalent Income"
       heading="The money", beats=[
    ("And let's talk about the money",
     "The money, on effort, not promise",
     "no promises", C),
    ("Three or four properties",
     "Three or four properties: supplemental income",
     "run as a side thing", N),
    ("At ten or twelve clients",
     "Ten or twelve clients: $95,000 to $140,000 a year",
     "reported salary data for a full-time equivalent", N),
    ("That's reported salary data",
     "Not what any single hotel pays you",
     "full-time-equivalent salary data", R),
  ]),
  dict(id="economics-03", layout="sheet", section="economics", donor="economics-03",
       heading="What it diversifies", beats=[
    ("But here's the thing",
     "What it diversifies isn't one income stream",
     "skills and optionality", C),
    ("It's skills and optionality",
     "Skills and optionality",
     "revenue-management literacy", C),
    ("A channel-manager and voice-agent stack you can resell",
     "A stack you can resell into other verticals",
     "channel-manager and voice-agent", T),
    ("A client roster that doesn't disappear",
     "A roster that survives one algorithm change",
     "not one OTA relationship", C),
  ]),
  dict(id="economics-04", layout="risk_card", section="economics", donor="economics-04",
       heading="The failure mode", beats=[
    ("Costs are real too",
     "Costs are real", "a few hundred a month per property — my estimate", N),
    ("And the failure mode",
     "The failure mode: one good month, then no renewal",
     "nobody proved the number moved", R),
  ]),
  dict(id="economics-q1", layout="quote", section="economics",
       anchor="Because nobody proved the number moved",
       quote="Because nobody proved the number moved.",
       heading="The economics", accent="the number moved"),
  dict(id="economics-05", layout="sheet", section="economics", donor="economics-04",
       heading="The actual test", beats=[
    ("Whether the pricing model survives that renewal conversation",
     "Whether the pricing survives the renewal conversation",
     "that's the actual test", R),
  ]),

  # ---- CTA
  dict(id="cta-01", layout="cta", section="cta", donor="cta-01",
       heading="The blueprint", beats=[
    ("Okay look",
     "Everything is in the blueprint",
     "audit template · pricing structure · outreach script", P),
    ("Subscribe for the next one in the series",
     "Subscribe for the next one",
     "one person, one commission-heavy market", C),
  ]),
]

# Rev D is authored as a narrative/production contract, not a list of slide
# templates. Every screen names the emotional state, camera distance, score
# state, and footage job. `layout` overrides deliberately create conspicuous
# render blockers until reviewed media is attached.
SECTION_STATE = {
    "hook": ("peril", "constraint"),
    "thesis": ("reversal", "counter"),
    "evidence": ("absurdity", "tension"),
    "stack": ("build", "build"),
    "playbook": ("build", "build"),
    "economics": ("agency", "human"),
    "cta": ("agency", "resolve"),
}

REV_D_SCREEN: dict[str, dict] = {
    "hook-01": dict(layout="broll", role="human_context", camera="human",
                    preview_eligible=True,
                    intent="Innkeeper places a physical room key in a guest's hand; tactile, daylight, no generic lobby glamour.",
                    query="independent hotel innkeeper handing room key to guest close up"),
    "hook-02": dict(role="market_force", camera="system", preview_eligible=True,
                    intent="The human booking collapses into the OTA share and commission mechanism; branded surfaces are evidence, not decoration."),
    "hook-03": dict(role="proof", camera="system", preview_eligible=True,
                    intent="Make the annual commission loss physically legible before explaining the arithmetic."),
    "hook-04": dict(role="proof", camera="human", preview_eligible=True,
                    state="reversal", score="silence",
                    intent="Hold the estimate caveat cleanly, then let silence make room for the thesis."),
    "thesis-02": dict(layout="broll", role="human_context", camera="human",
                      intent="A real 10–40 room independent property: one operator moving between desk, phone, keys, and guests.",
                      query="small independent hotel owner working front desk guests keys"),
    "evidence-03": dict(layout="broll", role="human_context", camera="human",
                        intent="Coqui Coqui or a truthful equivalent: hospitality work at human scale, not a resort beauty reel.",
                        query="boutique hotel owner guest experience front desk Mexico"),
    "evidence-04": dict(layout="broll", role="human_context", camera="human",
                        intent="Solo B&B operator doing two jobs at once; show the manpower constraint without caricature.",
                        query="bed and breakfast owner working alone front desk phone"),
    "evidence-08": dict(role="proof", camera="system",
                        intent="Live capture of vendor pricing pages where the absent public price is itself the evidence."),
    "stack-03": dict(role="process", camera="system", state="build", score="build",
                     intent="Gold counter-system expands from orchestration to drafting; logos label capabilities only after the flow is understood."),
    "stack-04": dict(layout="screen_rec", role="process", camera="system",
                     intent="Show the three agents performing real actions: profile update, re-book message, post-stay review request."),
    "stack-05": dict(layout="screen_rec", role="process", camera="system",
                     intent="End the workflow inside the booking engine; the platform is the destination, not the hero."),
    "playbook-01": dict(layout="broll", role="process", camera="human",
                        intent="Operator audits the guest journey on a real property surface: map listing, site, booking path, and notes.",
                        query="hotel owner reviewing booking website guest journey laptop notes"),
    "playbook-03": dict(layout="broll", role="human_context", camera="human",
                        intent="Contrast a staffed property with the solo operator using observable work, not an abstract headcount card.",
                        query="small hotel owner multitasking reception housekeeping phone"),
    "playbook-04": dict(layout="screen_rec", role="proof", camera="system",
                        intent="Screen capture the four vendor sites and the missing public price, then reveal the published offer."),
    "playbook-06": dict(layout="broll", role="outcome", camera="human", state="agency", score="counter",
                        intent="A returning guest books directly; gold path resolves in a human welcome and a physical key.",
                        query="returning hotel guest greeted by owner room key independent hotel"),
    "economics-03": dict(layout="broll", role="outcome", camera="human", state="agency", score="human",
                         intent="Operator reviews a small portfolio calmly; agency is visible as manageable work, not lifestyle fantasy.",
                         query="hospitality consultant reviewing hotel performance with owner laptop"),
    "cta-01": dict(layout="broll", role="outcome", camera="human", state="agency", score="resolve",
                   intent="Return to the innkeeper and direct guest relationship; blueprint appears as the next practical move.",
                   query="independent hotel owner welcoming returning guests room key"),
}


def rev_d_fields(entry: dict, layout: str) -> dict:
    directive = REV_D_SCREEN.get(entry["id"], {})
    state, score = SECTION_STATE[entry["section"]]
    role = directive.get("role")
    if not role:
        role = ("proof" if layout in {"chart", "proof_card", "artifact", "source_card"}
                else "process" if layout in {"schematic", "screen_rec"}
                else "human_context" if layout == "broll" else "evidence")
    return {
        "narrative_state": directive.get("state", state),
        "score_state": directive.get("score", score),
        "footage_role": role,
        "camera": directive.get("camera", "system"),
        "preview_eligible": bool(directive.get("preview_eligible", False)),
        "visual_intent": directive.get("intent", "Advance the argument with one legible visual job; no decorative motion."),
        "search_query": directive.get("query"),
    }


# --------------------------------------------------------------- assemble
def build() -> dict:
    # 1. resolve every anchor to a time
    for e in PLAN:
        if e["layout"] == "quote":
            e["_at"], e["_anchor_end"] = find_phrase(e["section"], e["anchor"])
        else:
            e["_beats"] = [(find_phrase(e["section"], ph)[0], ttl, body, tags)
                           for ph, ttl, body, tags in e["beats"]]
            e["_at"] = e["_beats"][0][0]

    if _MISSES:
        print("ANCHORS NOT FOUND — fix these phrases:", file=sys.stderr)
        for m in _MISSES:
            print("  " + m, file=sys.stderr)
        raise SystemExit(1)

    # 2. screen spans: start at own anchor, end at the next screen's anchor
    starts = [e["_at"] for e in PLAN]
    if starts != sorted(starts):
        bad = [(PLAN[i]["id"], starts[i]) for i in range(1, len(starts))
               if starts[i] < starts[i - 1]]
        raise SystemExit(f"screens out of order: {bad}")

    screens = []
    for i, e in enumerate(PLAN):
        start = e["_at"]
        end = PLAN[i + 1]["_at"] if i + 1 < len(PLAN) else TOTAL
        donor = DONORS.get(e.get("donor", ""), {})
        layout = REV_D_SCREEN.get(e["id"], {}).get("layout", e["layout"])
        rev_d = rev_d_fields(e, layout)

        if layout == "quote":
            # impact frame: hold only as long as the line takes to land, so
            # it hard-cuts back to the argument instead of becoming a title
            # slide (rubric wants 1.2-4s).
            reveals = [{"beat": 1, "at": round(start, 3), "end": round(end, 3),
                        "title": e["quote"], "body": "", "tags": ["claim"],
                        "word_anchor": {"start": round(start, 3),
                                        "end": round(e["_anchor_end"], 3)}}]
            screens.append({
                "id": e["id"], "section": e["section"], "layout": "quote",
                "heading": e["heading"], "start": round(start, 3),
                "end": round(end, 3),
                "reveals": reveals, "figure": None, "source": None,
                "sfx": [{"cue": "hit", "at": round(start, 3)}],
                # bed drops out entirely — the line carries the beat
                "music": {"intensity": "silence", "duck_db": 0},
                "custom": {"quote": e["quote"], "accentPhrase": e["accent"],
                           "ground": "navy"},
                **rev_d,
            })
            continue

        beats = e["_beats"]
        reveals = []
        # Beat numbers are SECTION-scoped: prepare_longform.py resolves each
        # reveal's asset by (section, beat) out of assets.json. Numbering every
        # screen from 1 therefore collides inside a section and hands a screen
        # the wrong chart — evidence-06 drew the commission bars while the VO
        # was on Mews' scale. `beat0` pins a screen's first reveal onto the
        # planned beat whose asset it actually wants.
        beat0 = e.get("beat0", 1)
        for j, (at, title, body, tags) in enumerate(beats):
            b_end = beats[j + 1][0] if j + 1 < len(beats) else end
            reveals.append({"beat": beat0 + j, "at": round(at, 3),
                            "end": round(b_end, 3), "title": title,
                            "body": body, "tags": list(tags),
                            "word_anchor": {"start": round(at, 3),
                                            "end": round(b_end, 3)}})

        # a tick on each beat boundary after the first — the audible half of
        # a composition that assembles rather than sits
        sfx = [{"cue": "tick", "at": r["at"]} for r in reveals[1:]]
        if layout in ("proof_card", "risk_card"):
            sfx.insert(0, {"cue": "hit", "at": round(start, 3)})

        screens.append({
            "id": e["id"], "section": e["section"], "layout": layout,
            "heading": e["heading"], "start": round(start, 3),
            "end": round(end, 3), "reveals": reveals,
            "figure": donor.get("figure"), "source": donor.get("source"),
            "sfx": sfx,
            "music": {"intensity": rev_d["score_state"], "duck_db": -16},
            "custom": e.get("custom") or donor.get("custom"),
            **rev_d,
        })

    return {"slug": GEN["slug"], "storyboard_version": "rev-d-1",
            "narrative_waveform": ["peril", "absurdity", "reversal", "build", "agency"],
            "total_seconds": TOTAL, "screens": screens}


if __name__ == "__main__":
    sb = build()
    OUT.write_text(json.dumps(sb, indent=2))
    n_q = sum(1 for s in sb["screens"] if s["layout"] == "quote")
    n_rev = sum(len(s["reveals"]) for s in sb["screens"])
    print(f"wrote {OUT.name}: {len(sb['screens'])} screens, "
          f"{n_rev} reveals, {n_q} quote frames")
