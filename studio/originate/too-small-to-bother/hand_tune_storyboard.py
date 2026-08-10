"""Hand-tuned storyboard for №005 (too-small-to-bother).

Full editorial pass: every screen has an authored title, heading, body,
custom fields (proof/risk/quote/titleCard), and a source flag. Every
boundary anchors to a real spoken phrase from vo/words.json. Number
formats match content-os/facts.md exactly (× not x, no stray %).

Rewrites storyboard.json from scratch. Do NOT layer on top of an
already-patched storyboard — this replaces it wholesale, like EP004's
hand_tune does.

Run:   python originate/too-small-to-bother/hand_tune_storyboard.py
Emits: originate/too-small-to-bother/storyboard.json
"""
from __future__ import annotations

import json
import re
from pathlib import Path

HERE = Path(__file__).parent
STORYBOARD = HERE / "storyboard.json"
WORDS = json.loads((HERE / "vo" / "words.json").read_text())
TIMELINE = json.loads((HERE / "vo" / "timeline.json").read_text())

_SECTION_WORDS: dict[str, list[dict]] = {}
for _w in WORDS:
    _SECTION_WORDS.setdefault(_w["section"], []).append(_w)

_SECTION_TIMING = {s["section"]: (s["start"], s["start"] + s["duration"])
                   for s in TIMELINE["sections"]}
TOTAL_SECONDS = TIMELINE["total_seconds"]

_WARN: list[str] = []


def _norm(w: str) -> str:
    return re.sub(r"[^\w']", "", w).strip("'").lower()


def find_phrase(section: str, phrase: str) -> tuple[float, float]:
    tokens = [_norm(t) for t in phrase.split() if _norm(t)]
    ws = _SECTION_WORDS.get(section, [])
    normed = [_norm(w["word"]) for w in ws]
    for i in range(len(normed) - len(tokens) + 1):
        if normed[i:i + len(tokens)] == tokens:
            return ws[i]["start"], ws[i + len(tokens) - 1]["end"]
    raise ValueError(f"phrase {phrase!r} not found in section {section}")


def fp(section: str, phrase: str, default: float | None = None) -> float:
    try:
        return find_phrase(section, phrase)[0]
    except ValueError:
        if default is None:
            raise
        _WARN.append(f"{section}:{phrase}")
        return default


def screen(**kw):
    kw.setdefault("audio", f"vo/{kw['section']}.mp3")
    kw.setdefault("figure", None)
    kw.setdefault("source", None)
    kw.setdefault("music", {"intensity": "calm", "duck_db": -16})
    kw.setdefault("sfx", [])
    kw.setdefault("custom", None)
    kw.setdefault("events", [])
    return kw


def reveal(beat, at, end, title, body="", tags=None):
    return {"beat": beat, "at": at, "end": end, "title": title, "body": body,
            "tags": tags or ["claim"], "word_anchor": {"start": at, "end": end}}


def build() -> dict:
    screens: list[dict] = []

    # ============================================================
    # HOOK (0 → 16.5s, 1 beat, 3 reveals inside)
    # ============================================================
    h0, h1 = _SECTION_TIMING["hook"]
    five_years = fp("hook", "Five years later")
    nobody = fp("hook", "Nobody covered")

    screens.append(screen(id="hook-01", section="hook", layout="chart",
        heading="The floor", start=h0, end=h1,
        reveals=[
            reveal(1, h0, five_years, "2017 · 5,060",
                   body="US software firms under five employees", tags=["number"]),
            reveal(1, five_years, nobody, "2022 · 7,857 · +55%",
                   body="the floor of what a software business has to be, collapsed in five years",
                   tags=["number"]),
            reveal(1, nobody, h1, "Nobody covered one of them", tags=["punchline"]),
        ],
        source="US Census Bureau, Statistics of US Businesses, NAICS 5112, released April 2025 [verified]",
        music={"intensity": "build", "duck_db": -10},
        sfx=[{"cue": "hit", "at": h0}, {"cue": "tick", "at": five_years}, {"cue": "hit", "at": nobody}]))

    # ============================================================
    # THESIS (16.5 → 100.8s, 84.3s, 3 beats)
    # ============================================================
    t0, t1 = _SECTION_TIMING["thesis"]
    stopped_finding = fp("thesis", "I've stopped finding")
    not_ceiling = fp("thesis", "not the ceiling")
    for_twenty_years = fp("thesis", "For twenty years")
    then_first_link = fp("thesis", "Then the first link broke")
    im_not_gonna = fp("thesis", "I'm not gonna put a number")
    the_direction = fp("thesis", "But the direction")

    # thesis-01: the framing (one-person unicorn is the only story)
    screens.append(screen(id="thesis-01", section="thesis", layout="sheet",
        heading="The thesis", start=t0, end=not_ceiling,
        reveals=[
            reveal(1, t0, stopped_finding, "Everybody's writing about the one-person unicorn",
                   body="whether it's happened · who's closest · how soon", tags=["claim"]),
            reveal(1, stopped_finding, not_ceiling, "The only story this industry knows how to tell",
                   tags=["punchline"]),
        ],
        source="Framing beat · Amodei 70–80% one-person forecast — Inc., Code with Claude, May 2025",
        sfx=[{"cue": "tick", "at": t0}]))

    # thesis-02: not the ceiling — the floor
    screens.append(screen(id="thesis-02", section="thesis", layout="quote",
        heading="The thesis", start=not_ceiling, end=for_twenty_years,
        reveals=[
            reveal(1, not_ceiling, for_twenty_years, "Not the ceiling. The floor.",
                   body="the minimum size a software business has to be, fell through the basement",
                   tags=["punchline"]),
        ],
        source="Framing axiom [derived]",
        music={"intensity": "silence", "duck_db": 0},
        sfx=[{"cue": "hit", "at": not_ceiling}],
        custom={"quote": "It's not the ceiling. It's the floor.",
                "accentPhrase": "the floor", "ground": "navy"}))

    # thesis-03: the mechanical chain that held for 20 years, then broke
    screens.append(screen(id="thesis-03", section="thesis", layout="schematic",
        heading="The chain", start=for_twenty_years, end=im_not_gonna,
        reveals=[
            reveal(2, for_twenty_years, then_first_link, "Team → capital → outcome → market",
                   body="a mechanical forcing · not cultural · every link had to hold",
                   tags=["process"]),
            reveal(2, then_first_link, im_not_gonna, "Then the first link broke",
                   body="a person working alone now does what recently took several people",
                   tags=["claim"]),
        ],
        source="Framing beat [derived]",
        sfx=[{"cue": "tick", "at": for_twenty_years}, {"cue": "hit", "at": then_first_link}]))

    # thesis-04: the honest hedge + the pivot question
    screens.append(screen(id="thesis-04", section="thesis", layout="quote",
        heading="The thesis", start=im_not_gonna, end=t1,
        reveals=[
            reveal(3, im_not_gonna, the_direction, "The research is contested — picking the flattering study is how this genre lies",
                   tags=["risk"]),
            reveal(3, the_direction, t1, "The direction is not in dispute",
                   body="what did the collapsing floor actually produce?",
                   tags=["question"]),
        ],
        source="Rigor caveat [derived]",
        music={"intensity": "silence", "duck_db": 0},
        sfx=[{"cue": "hit", "at": the_direction}],
        custom={"quote": "The direction is not in dispute.",
                "accentPhrase": "not in dispute", "ground": "paper"}))

    # ============================================================
    # EVIDENCE (100.8 → 311.3s, 210.4s, 7 beats)
    # ============================================================
    e0, e1 = _SECTION_TIMING["evidence"]
    software_companies = fp("evidence", "American software companies")
    billion_with_a_B = fp("evidence", "Billion with a B")
    six_hundred = fp("evidence", "six hundred seventy-five thousand")
    number_of_solo = fp("evidence", "the number of solo operators")
    small_durable = fp("evidence", "These are small")
    now_half = fp("evidence", "Now. The half")
    across_roughly = fp("evidence", "Across roughly")
    four_hundred_times = fp("evidence", "four hundred times")
    the_median_app = fp("evidence", "The median app")
    supply_explains = fp("evidence", "Supply explains it")
    ios_added = fp("evidence", "iOS added")
    thats_what_happens = fp("evidence", "That's what happens")
    two_stories = fp("evidence", "Those two stories")
    when_the_floor = fp("evidence", "When the floor drops")
    anybody_selling = fp("evidence", "Anybody selling you")
    ceiling_didnt = fp("evidence", "The ceiling didn't come down either")
    medvi = fp("evidence", "A telehealth company called Medvi")
    four_hundred_and_one = fp("evidence", "four hundred and one million dollars")
    who_are_brothers = fp("evidence", "Who are brothers")
    forbes_reported = fp("evidence", "Forbes reported")
    and_watch = fp("evidence", "And watch")
    cursor_is_reported = fp("evidence", "Cursor is reported")
    reported_run_rates = fp("evidence", "All three are reported")
    the_people_selling = fp("evidence", "The people selling shovels")
    which_raises = fp("evidence", "Which raises the question")

    # evidence-01: Census growth — 55% growth, 57.5% majority
    screens.append(screen(id="evidence-01", section="evidence", layout="sheet",
        heading="What the Census counted", start=e0, end=billion_with_a_B,
        reveals=[
            reveal(1, e0, software_companies, "Start with what the Census actually counted",
                   body="because nobody else did", tags=["claim"]),
            reveal(1, software_companies, billion_with_a_B, "+55% growth · now 57.5% of US software publishers",
                   body="firms under 5 employees, 2017 → 2022",
                   tags=["number"]),
        ],
        source="US Census Bureau, Statistics of US Businesses, NAICS 5112, released April 2025 [verified]",
        sfx=[{"cue": "tick", "at": e0}]))

    # evidence-02: revenue + Stripe solo-op merged (both are Census-era numbers, one proof card, 3 reveals)
    screens.append(screen(id="evidence-02", section="evidence", layout="proof_card",
        heading="What the Census counted", start=billion_with_a_B, end=now_half,
        reveals=[
            reveal(1, billion_with_a_B, six_hundred, "$5.30B booked · billion with a B", tags=["number"]),
            reveal(1, six_hundred, number_of_solo, "≈ $674,676 per firm",
                   body="the 7,857 businesses nobody wrote about", tags=["number"]),
            reveal(2, number_of_solo, small_durable, "Solo operators clearing $1M/yr · doubled 2023 → 2025",
                   tags=["number"]),
            reveal(2, small_durable, now_half, "Small · durable · unglamorous",
                   body="serving markets nobody could afford to serve before",
                   tags=["claim"]),
        ],
        source="US Census SUSB [verified]; Stripe Economics — solopreneur cohort [reported]",
        music={"intensity": "build", "duck_db": -10},
        sfx=[{"cue": "hit", "at": billion_with_a_B}, {"cue": "tick", "at": number_of_solo}],
        custom={"proof": {"value": 5.30, "prefix": "$", "suffix": "B",
            "label": "Booked together by 7,857 US software firms under 5 employees, 2022",
            "source": "US Census SUSB, NAICS 5112"}}))

    # evidence-04: the half nobody sells — RevenueCat 400× vs 200×
    screens.append(screen(id="evidence-04", section="evidence", layout="proof_card",
        heading="The half nobody sells", start=now_half, end=the_median_app,
        reveals=[
            reveal(3, now_half, across_roughly, "Now · the half nobody sells", tags=["claim"]),
            reveal(3, across_roughly, four_hundred_times, "115,000 subscription apps · one year in", tags=["number"]),
            reveal(3, four_hundred_times, the_median_app, "400× · top 5% vs bottom quartile",
                   body="up from 200× the year before · doubled, in a year",
                   tags=["number", "punchline"]),
        ],
        source="RevenueCat (115,000+ subscription apps) [reported]",
        music={"intensity": "build", "duck_db": -10},
        sfx=[{"cue": "hit", "at": four_hundred_times}],
        custom={"proof": {"value": 400, "suffix": "×",
            "label": "top 5% of new launches over bottom quartile after year one · up from 200× the year prior",
            "source": "RevenueCat (115,000+ apps)"}}))

    # evidence-05: median app + 70% under $1K — the sober floor
    screens.append(screen(id="evidence-05", section="evidence", layout="risk_card",
        heading="The half nobody sells", start=the_median_app, end=supply_explains,
        reveals=[
            reveal(3, the_median_app, supply_explains, "Median new app: under $50/mo at month 12",
                   body="~70% of micro-SaaS never clears $1,000/mo",
                   tags=["number", "risk"]),
        ],
        source="RevenueCat 2024; Freemius, December 2025 [reported]",
        sfx=[{"cue": "tick", "at": the_median_app}],
        custom={"risk": {"title": "The typical attempt is worth less than it used to be.",
            "body": "Half of a fact this industry is very good at telling. The other half is below.",
            "bullets": ["Median new app: <$50/mo after 12 months",
                        "~70% of micro-SaaS never clears $1,000/mo",
                        "Both tails are real; picking the flattering one is how this genre lies"]}}))

    # evidence-06: supply explains it — iOS +600K apps vs +2-3% downloads
    screens.append(screen(id="evidence-06", section="evidence", layout="chart",
        heading="Supply explains it", start=supply_explains, end=two_stories,
        reveals=[
            reveal(4, supply_explains, ios_added, "Supply explains it", tags=["claim"]),
            reveal(4, ios_added, thats_what_happens, "iOS 2025 · ~600,000 new apps (+30%) vs downloads +2–3%",
                   body="cost constraint removed · attention constraint held",
                   tags=["number"]),
            reveal(4, thats_what_happens, two_stories, "You remove a cost constraint · you don't create the demand",
                   tags=["punchline"]),
        ],
        source="Sensor Tower, 2025 [reported]",
        music={"intensity": "build", "duck_db": -10},
        sfx=[{"cue": "hit", "at": ios_added}]))

    # evidence-07: the axiom (quote)
    screens.append(screen(id="evidence-07", section="evidence", layout="quote",
        heading="The axiom", start=two_stories, end=ceiling_didnt,
        reveals=[
            reveal(5, two_stories, when_the_floor, "Those two stories are not in tension. They are the same fact.",
                   tags=["claim"]),
            reveal(5, when_the_floor, anybody_selling, "When the floor drops, more people can stand on it",
                   body="and it gets worse for the median person standing there",
                   tags=["punchline"]),
            reveal(5, anybody_selling, ceiling_didnt, "Anybody selling only the first half is selling you something",
                   tags=["punchline"]),
        ],
        source="Axiom drawn from Census + RevenueCat + Sensor Tower above [derived]",
        music={"intensity": "silence", "duck_db": 0},
        sfx=[{"cue": "hit", "at": when_the_floor}],
        custom={"quote": "When the floor drops, more people can stand on it — and it gets worse for the median person standing there.",
                "accentPhrase": "floor drops", "ground": "navy"}))

    # evidence-08: Medvi — the ceiling proof
    screens.append(screen(id="evidence-08", section="evidence", layout="proof_card",
        heading="The ceiling didn't come down", start=ceiling_didnt, end=who_are_brothers,
        reveals=[
            reveal(6, ceiling_didnt, medvi, "The ceiling didn't come down either", tags=["claim"]),
            reveal(6, medvi, four_hundred_and_one, "Medvi · a telehealth company", tags=["claim"]),
            reveal(6, four_hundred_and_one, who_are_brothers, "$401M revenue · first full year · 250,000 customers · 2 employees",
                   body="who are brothers",
                   tags=["number", "punchline"]),
        ],
        source="Forbes, April 2 2026 — reported figures, first full year [reported ⚠]",
        music={"intensity": "build", "duck_db": -8},
        sfx=[{"cue": "hit", "at": four_hundred_and_one}],
        custom={"proof": {"value": 401, "prefix": "$", "suffix": "M",
            "label": "First full year · 250,000 customers · 2 employees · ~$20K starting capital",
            "source": "Forbes, April 2 2026 [reported ⚠ — not audited]"}}))

    # evidence-09: hold as reported — the honest caveat
    screens.append(screen(id="evidence-09", section="evidence", layout="risk_card",
        heading="Reported, not audited", start=who_are_brothers, end=and_watch,
        reveals=[
            reveal(6, who_are_brothers, forbes_reported, "The founder doesn't employ the doctors · doesn't touch a prescription",
                   tags=["process"]),
            reveal(6, forbes_reported, and_watch, "Forbes reported these numbers — so hold them as reported, not audited",
                   tags=["risk"]),
        ],
        source="Forbes, April 2 2026 [reported ⚠]",
        sfx=[{"cue": "tick", "at": forbes_reported}],
        custom={"risk": {"title": "Reported, not audited.",
            "body": "The medical infrastructure is rented from CareValidate and OpenLoop Health. The story is real; the arithmetic is Forbes-reported, not filed.",
            "bullets": ["Reported figures, first full year",
                        "No SEC filing — Medvi is private",
                        "Rented medical infrastructure — the founder holds no license"]}}))

    # evidence-10: the toolmakers — Cursor/Replit/Lovable chart
    screens.append(screen(id="evidence-10", section="evidence", layout="chart",
        heading="Who monetized the collapse", start=and_watch, end=reported_run_rates,
        reveals=[
            reveal(7, and_watch, cursor_is_reported, "Watch who actually monetized the collapse", tags=["claim"]),
            reveal(7, cursor_is_reported, reported_run_rates, "Cursor ~$2B · Replit ~$240M · Lovable ~$200M",
                   body="annualized · all three reported run-rates",
                   tags=["number"]),
        ],
        source="Reported run-rates — RESEARCH-DOSSIER §2, restated in content-os/facts.md [reported ⚠]",
        music={"intensity": "build", "duck_db": -10},
        sfx=[{"cue": "hit", "at": cursor_is_reported}]))

    # evidence-11: shovels vs diggers — the punchline + question
    screens.append(screen(id="evidence-11", section="evidence", layout="quote",
        heading="The people selling shovels", start=reported_run_rates, end=e1,
        reveals=[
            reveal(7, reported_run_rates, the_people_selling, "Hold them loosely · but the direction isn't in doubt",
                   tags=["claim"]),
            reveal(7, the_people_selling, which_raises, "The people selling shovels monetized the cost collapse inside two years",
                   body="most of the people digging did not",
                   tags=["punchline"]),
            reveal(7, which_raises, e1, "Who notices these small software companies?",
                   tags=["question"]),
        ],
        source="Reported run-rates + Census cohort [derived]",
        music={"intensity": "silence", "duck_db": 0},
        sfx=[{"cue": "hit", "at": the_people_selling}],
        custom={"quote": "The people selling shovels monetized the cost collapse inside two years. Most of the people digging did not.",
                "accentPhrase": "selling shovels", "ground": "paper"}))

    # ============================================================
    # STACK (311.3 → 486.6s, 175s, 4 beats) — the moat argument
    # ============================================================
    s0, s1 = _SECTION_TIMING["stack"]
    narrators_are = fp("stack", "The narrators are investors")
    twenty_one = fp("stack", "twenty one thousand six hundred forty")
    thats_not_scandal = fp("stack", "That's not a scandal")
    a_fund_is = fp("stack", "A fund is constitutionally")
    and_that_lens = fp("stack", "And that lens")
    four_point_four = fp("stack", "Venture supplies four point four percent")
    small_business = fp("stack", "Meanwhile small business")
    so_somebody = fp("stack", "So somebody else's scoreboard")
    so_what_defends = fp("stack", "So what actually defends")
    for_a_while = fp("stack", "For a while I thought")
    google_launched = fp("stack", "Google launched")
    zillow_lost = fp("stack", "Zillow lost")
    and_toast = fp("stack", "And Toast?")
    so_fluency = fp("stack", "So fluency is not the moat")
    heres_correction = fp("stack", "Here's the correction")
    fluency_entry = fp("stack", "Fluency is the entry ticket")
    look_at_toast = fp("stack", "Look at what Toast monetizes")
    four_point_zero = fp("stack", "Four point zero five three billion")
    software_wedge = fp("stack", "The software is the wedge")
    but_accumulation = fp("stack", "But accumulation is only half")

    # stack-01: the reason nobody narrates — VC math setup
    screens.append(screen(id="stack-01", section="stack", layout="sheet",
        heading="Why nobody narrates this", start=s0, end=twenty_one,
        reveals=[
            reveal(1, s0, narrators_are, "The narrators are investors", tags=["claim"]),
            reveal(1, narrators_are, twenty_one, "A fund does not work unless it catches outliers",
                   body="that's the whole game", tags=["process"]),
        ],
        source="VC return distribution — Correlation Ventures [reported]",
        sfx=[{"cue": "tick", "at": s0}]))

    # stack-02: VC waffle proof — 65% underwater
    screens.append(screen(id="stack-02", section="stack", layout="proof_card",
        heading="The VC waffle", start=twenty_one, end=thats_not_scandal,
        reveals=[
            reveal(1, twenty_one, thats_not_scandal, "21,640 venture financings · 65% returned less than invested",
                   body="about 4% returned 10× or more",
                   tags=["number"]),
        ],
        source="Correlation Ventures, 21,640 financings [reported]",
        music={"intensity": "build", "duck_db": -10},
        sfx=[{"cue": "hit", "at": twenty_one}],
        custom={"proof": {"value": 65, "suffix": "%",
            "label": "of 21,640 VC financings returned less than invested · ~4% returned 10× or more",
            "source": "Correlation Ventures"}}))

    # stack-03: the stated model — quote
    screens.append(screen(id="stack-03", section="stack", layout="quote",
        heading="The stated model", start=thats_not_scandal, end=and_that_lens,
        reveals=[
            reveal(1, thats_not_scandal, a_fund_is, "That's not a scandal — that's the stated model, working exactly as designed",
                   tags=["claim"]),
            reveal(1, a_fund_is, and_that_lens, "A fund is constitutionally incapable of caring about a business that small",
                   tags=["punchline"]),
        ],
        source="Correlation Ventures + Census SUSB [derived]",
        music={"intensity": "silence", "duck_db": 0},
        sfx=[{"cue": "hit", "at": a_fund_is}],
        custom={"quote": "A fund is constitutionally incapable of caring about a business that size.",
                "accentPhrase": "constitutionally incapable", "ground": "navy"}))

    # stack-04: three denominators + real-company punchline merged (short quote absorbed as reveal)
    screens.append(screen(id="stack-04", section="stack", layout="sheet",
        heading="Whose scoreboard", start=and_that_lens, end=so_what_defends,
        reveals=[
            reveal(2, and_that_lens, four_point_four, "That lens covers a fraction of the activity", tags=["claim"]),
            reveal(2, four_point_four, small_business, "VC = 4.4% of startup funding · 6.5% of Inc. 5000 ever raised any",
                   tags=["number"]),
            reveal(2, small_business, so_somebody, "Small business = 43.5% of US GDP",
                   tags=["number"]),
            reveal(2, so_somebody, so_what_defends, "Somebody else's scoreboard became the definition of a real company",
                   tags=["punchline"]),
        ],
        source="Kauffman Firm Survey; SBA Office of Advocacy, February 2026 [verified]",
        sfx=[{"cue": "tick", "at": and_that_lens}, {"cue": "hit", "at": so_somebody}]))

    # stack-06: fluency setup — the tested hypothesis
    screens.append(screen(id="stack-06", section="stack", layout="sheet",
        heading="Fluency, tested", start=so_what_defends, end=google_launched,
        reveals=[
            reveal(3, so_what_defends, for_a_while, "So what defends a business that size?",
                   tags=["question"]),
            reveal(3, for_a_while, google_launched, "For a while I thought the answer was fluency",
                   body="knowing a market from the inside · where a competitor clones your product in a weekend and still has no idea what to build next",
                   tags=["operator_pov"]),
        ],
        source="Fluency hypothesis, tested below [derived]",
        sfx=[{"cue": "tick", "at": so_what_defends}]))

    # stack-07: outsider failures — Google + Zillow
    screens.append(screen(id="stack-07", section="stack", layout="schematic",
        heading="Outsider failures", start=google_launched, end=and_toast,
        reveals=[
            reveal(3, google_launched, zillow_lost, "Google Compare · March 2015 → March 2016 · killed inside a year",
                   tags=["risk", "number"]),
            reveal(3, zillow_lost, and_toast, "Zillow lost ~$881M buying houses",
                   body="while sitting on the richest housing dataset anywhere",
                   tags=["risk", "number"]),
        ],
        source="Insurance Journal (Google Compare); Zillow press (~$881M loss, Nov 2021) [verified]",
        sfx=[{"cue": "tick", "at": google_launched}]))

    # stack-08: the Toast contradiction — quote
    screens.append(screen(id="stack-08", section="stack", layout="quote",
        heading="Not the moat", start=and_toast, end=heres_correction,
        reveals=[
            reveal(3, and_toast, so_fluency, "Toast · founded by engineers with no restaurant background",
                   body="beat incumbents who were soaked in restaurant fluency",
                   tags=["punchline"]),
            reveal(3, so_fluency, heres_correction, "So fluency is not the moat",
                   tags=["punchline"]),
        ],
        source="Toast 10-K, FY2024 [verified]",
        music={"intensity": "silence", "duck_db": 0},
        sfx=[{"cue": "hit", "at": so_fluency}],
        custom={"quote": "So fluency is not the moat.",
                "accentPhrase": "not the moat", "ground": "navy"}))

    # stack-09: the correction — fluency is the entry ticket
    screens.append(screen(id="stack-09", section="stack", layout="sheet",
        heading="Fluency is the entry ticket", start=heres_correction, end=look_at_toast,
        reveals=[
            reveal(4, heres_correction, fluency_entry, "Here's the correction",
                   body="fluency is what buys you the right first product · nothing more",
                   tags=["claim"]),
            reveal(4, fluency_entry, look_at_toast, "What holds a market is what fluency lets you accumulate afterward",
                   body="integrations · records living inside your product · the fact that ripping you out breaks their Tuesday",
                   tags=["process"]),
        ],
        source="Vertical SaaS pattern — Toast, Clio [derived]",
        sfx=[{"cue": "tick", "at": heres_correction}]))

    # stack-10: Toast fintech-over-software proof
    screens.append(screen(id="stack-10", section="stack", layout="proof_card",
        heading="Toast · the wedge", start=look_at_toast, end=but_accumulation,
        reveals=[
            reveal(4, look_at_toast, four_point_zero, "Look at what Toast monetizes", tags=["claim"]),
            reveal(4, four_point_zero, software_wedge, "$4.053B fintech vs $706M software subscriptions · FY2024",
                   tags=["number"]),
            reveal(4, software_wedge, but_accumulation, "The software is the wedge · the payments are the business",
                   tags=["punchline"]),
        ],
        source="Toast 10-K, FY2024 [verified]",
        music={"intensity": "build", "duck_db": -10},
        sfx=[{"cue": "hit", "at": four_point_zero}],
        custom={"proof": {"value": 4.053, "prefix": "$", "suffix": "B",
            "label": "Toast fintech revenue · vs $706M software subscriptions · FY2024",
            "source": "Toast 10-K, FY2024"}}))

    # stack-11: the missing half cliffhanger
    screens.append(screen(id="stack-11", section="stack", layout="quote",
        heading="The missing half", start=but_accumulation, end=s1,
        reveals=[
            reveal(5, but_accumulation, s1, "The missing half is the part almost nobody says out loud",
                   tags=["punchline"]),
        ],
        source="Cliffhanger into the playbook section [derived]",
        music={"intensity": "silence", "duck_db": 0},
        sfx=[{"cue": "hit", "at": but_accumulation}],
        custom={"quote": "…and the missing half is the part almost nobody says out loud.",
                "accentPhrase": "missing half", "ground": "navy"}))

    # ============================================================
    # PLAYBOOK (486.6 → 674.9s, 188s, 5 beats)
    # ============================================================
    p0, p1 = _SECTION_TIMING["playbook"]
    market_too_small = fp("playbook", "The market has to be too small")
    a_niche_holds = fp("playbook", "A niche holds")
    constellation = fp("playbook", "Constellation Software")
    which_means = fp("playbook", "Which means the knowledge is transferable")
    their_indifference = fp("playbook", "their indifference")
    so_the_first = fp("playbook", "So the first question")
    run_the_arithmetic = fp("playbook", "Run the arithmetic")
    if_the_answer = fp("playbook", "If the answer's")
    second_question = fp("playbook", "Second question")
    so_do_you = fp("playbook", "So: do you have a way")
    because_a_business = fp("playbook", "Because a business")
    and_the_tenancy = fp("playbook", "And the tenancy risk")
    googles_app_store = fp("playbook", "Google's app store")
    the_bureau = fp("playbook", "The Bureau of Labor Statistics")
    half_gone = fp("playbook", "Half gone within five years")
    you_notice = fp("playbook", "You notice all of this")
    thats_the_whole = fp("playbook", "That's the whole evaluation")
    the_two_questions = fp("playbook", "The two questions")
    and_the_point = fp("playbook", "And the point isn't")
    which_brings_us = fp("playbook", "Which brings us")

    # playbook-01: the missing half revealed
    screens.append(screen(id="playbook-01", section="playbook", layout="quote",
        heading="Too small to bother", start=p0, end=a_niche_holds,
        reveals=[
            reveal(1, p0, market_too_small, "Here's the missing half", tags=["claim"]),
            reveal(1, market_too_small, a_niche_holds, "The market has to be too small to be worth an outsider's time",
                   body="not too hard · too small",
                   tags=["punchline"]),
        ],
        source="The defensible formulation [derived]",
        music={"intensity": "silence", "duck_db": 0},
        sfx=[{"cue": "hit", "at": market_too_small}],
        custom={"quote": "Not too hard. Too small.",
                "accentPhrase": "too small", "ground": "navy"}))

    # playbook-02: the mechanism — accumulation vs cost of reproduction
    screens.append(screen(id="playbook-02", section="playbook", layout="sheet",
        heading="The mechanism", start=a_niche_holds, end=constellation,
        reveals=[
            reveal(1, a_niche_holds, constellation, "A niche holds when what you've accumulated grows faster than the cost of reproducing it",
                   body="and nobody with real capital earns enough by paying that cost to bother",
                   tags=["claim", "process"]),
        ],
        source="Vertical SaaS mechanism [derived]",
        sfx=[{"cue": "tick", "at": a_niche_holds}]))

    # playbook-03: Constellation proof — the knowledge is transferable
    screens.append(screen(id="playbook-03", section="playbook", layout="proof_card",
        heading="Their indifference", start=constellation, end=so_the_first,
        reveals=[
            reveal(2, constellation, which_means, "Constellation Software · 6 groups · 70+ vertical markets",
                   body="buying exactly these businesses and keeping the economics intact",
                   tags=["number"]),
            reveal(2, which_means, their_indifference, "The knowledge is transferable · you can just purchase it",
                   tags=["claim"]),
            reveal(2, their_indifference, so_the_first, "What protects you was never their incomprehension · it's their indifference",
                   tags=["punchline"]),
        ],
        source="Constellation Software annual report, 2025 [verified]",
        music={"intensity": "build", "duck_db": -10},
        sfx=[{"cue": "hit", "at": constellation}],
        custom={"proof": {"value": 70, "suffix": "+ vertical markets",
            "label": "Constellation Software · 6 operating groups · buying exactly these businesses",
            "source": "Constellation Software annual report, 2025"}}))

    # playbook-04: QUESTION ONE
    screens.append(screen(id="playbook-04", section="playbook", layout="sheet",
        heading="Question one", start=so_the_first, end=second_question,
        reveals=[
            reveal(3, so_the_first, run_the_arithmetic, "Question one · would anyone with real money bother taking it from you?",
                   body="not \"can this scale\" · run the arithmetic an acquirer would run",
                   tags=["question"]),
            reveal(3, run_the_arithmetic, if_the_answer, "Reproduce your integrations · your records · your relationships",
                   body="what would the market pay them back for doing it?",
                   tags=["process"]),
            reveal(3, if_the_answer, second_question, "If the answer is nothing worth their time · that's most of your protection",
                   tags=["punchline"]),
        ],
        source="The two-question test · question one [derived]",
        sfx=[{"cue": "tick", "at": so_the_first}]))

    # playbook-05: QUESTION TWO + tenant/owner punchline merged
    screens.append(screen(id="playbook-05", section="playbook", layout="sheet",
        heading="Question two", start=second_question, end=and_the_tenancy,
        reveals=[
            reveal(4, second_question, so_do_you, "Question two · distribution",
                   body="build cost was never the binding constraint · distribution was · the cost collapse did nothing to it",
                   tags=["claim"]),
            reveal(4, so_do_you, because_a_business, "A way to reach the people who need this that doesn't depend on a platform's mood",
                   body="an existing audience · a profession you're inside of · a named list of buyers",
                   tags=["process"]),
            reveal(4, because_a_business, and_the_tenancy, "A business whose distribution IS a platform is a tenant · not an owner",
                   tags=["punchline"]),
        ],
        source="The two-question test · question two [derived]",
        sfx=[{"cue": "tick", "at": second_question}, {"cue": "hit", "at": because_a_business}]))

    # playbook-07: tenancy risk measured — Google Play + BLS
    screens.append(screen(id="playbook-07", section="playbook", layout="risk_card",
        heading="Tenancy risk, measured", start=and_the_tenancy, end=half_gone,
        reveals=[
            reveal(5, and_the_tenancy, googles_app_store, "The tenancy risk isn't theoretical · it's measured", tags=["claim"]),
            reveal(5, googles_app_store, the_bureau, "Google Play · 3.4M → 1.8M listings in ~15 months",
                   body="~47% of apps deleted",
                   tags=["number", "risk"]),
            reveal(5, the_bureau, half_gone, "BLS · 569,387 establishments (1994 cohort) · half gone within 5 years",
                   tags=["number", "risk"]),
        ],
        source="TechCrunch, April 2025 (Play Store); US BLS Business Dynamics, 1994 cohort [verified]",
        music={"intensity": "build", "duck_db": -8},
        sfx=[{"cue": "hit", "at": googles_app_store}],
        custom={"risk": {"title": "Building on a platform means it can delete you.",
            "body": "Half of every new business gone within five years is the ambient distribution risk. Adding a landlord doesn't reduce it — it concentrates it.",
            "bullets": ["Google Play: 3.4M → 1.8M listings in ~15 months (~47% deleted)",
                        "BLS 1994 cohort of 569,387: 79.6% at 1yr · 49.6% at 5yr · 33.6% at 10yr",
                        "None of it filed a report"]}}))

    # playbook-08: the scoreboard callback + evaluation-sheet CTA
    screens.append(screen(id="playbook-08", section="playbook", layout="sheet",
        heading="The evaluation sheet", start=half_gone, end=the_two_questions,
        reveals=[
            reveal(5, half_gone, you_notice, "None of it filed a report", tags=["claim"]),
            reveal(5, you_notice, thats_the_whole, "You notice this the moment you stop grading yourself on somebody else's scoreboard",
                   tags=["punchline"]),
            reveal(5, thats_the_whole, the_two_questions, "The whole evaluation fits on one page — this week's blueprint is the sheet itself",
                   tags=["cta"]),
        ],
        source="Blueprint transition [derived]",
        sfx=[{"cue": "tick", "at": you_notice}]))

    # playbook-09: what the blueprint contains + the honest-math transition
    screens.append(screen(id="playbook-09", section="playbook", layout="sheet",
        heading="What's in it", start=the_two_questions, end=p1,
        reveals=[
            reveal(5, the_two_questions, and_the_point, "Two questions · reproduction-cost arithmetic · every sourced number from this episode",
                   body="run your own idea through it before you build anything",
                   tags=["cta", "process"]),
            reveal(5, and_the_point, which_brings_us, "The point isn't to talk you out of building small. It's the opposite.",
                   tags=["punchline"]),
            reveal(5, which_brings_us, p1, "Which brings us to what the honest math actually says",
                   tags=["question"]),
        ],
        source="Blueprint transition [derived]",
        sfx=[{"cue": "tick", "at": the_two_questions}]))

    # ============================================================
    # ECONOMICS (674.9 → 810.8s, 135.9s, 4 beats)
    # ============================================================
    ec0, ec1 = _SECTION_TIMING["economics"]
    the_average = fp("economics", "The average of those eight thousand")
    sounds_great = fp("economics", "Sounds great")
    seventeen_point = fp("economics", "Seventeen point three percent")
    four_point_six = fp("economics", "Four point six percent")
    both_tails = fp("economics", "Both tails are real")
    heres_thing_though = fp("economics", "Here's the thing though")
    these_firms_avg = fp("economics", "These firms average under five")
    what_you_spend = fp("economics", "What you actually spend")
    the_build_risk = fp("economics", "The build risk fell")
    what_it_diversifies = fp("economics", "What it diversifies")
    and_the_failure = fp("economics", "And the failure mode")
    your_accumulated = fp("economics", "Your accumulated position")
    so_heres_honest = fp("economics", "So here's the honest sentence")
    the_count = fp("economics", "The count of viable")
    and_your_protection = fp("economics", "And your protection")
    three_decades = fp("economics", "Three decades of being profitable")
    turns_out = fp("economics", "Turns out that might just be")

    # economics-01: the odds ladder — proof card
    screens.append(screen(id="economics-01", section="economics", layout="proof_card",
        heading="The odds ladder", start=ec0, end=sounds_great,
        reveals=[
            reveal(1, ec0, the_average, "The distribution you're actually entering · no smoothing",
                   tags=["claim"]),
            reveal(1, the_average, sounds_great, "Census: $5.30B booked in aggregate",
                   body="7,857 micro-firms · 57.5% of all US software publishers",
                   tags=["number"]),
        ],
        source="US Census SUSB, NAICS 5112 [verified]",
        music={"intensity": "build", "duck_db": -10},
        sfx=[{"cue": "hit", "at": ec0}],
        custom={"proof": {"value": 5.30, "prefix": "$", "suffix": "B",
            "label": "Booked together by 7,857 US software firms under 5 employees, 2022",
            "source": "US Census SUSB, NAICS 5112"}}))

    # economics-02: odds ladder + both-tails punchline merged
    screens.append(screen(id="economics-02", section="economics", layout="chart",
        heading="The odds ladder", start=sounds_great, end=heres_thing_though,
        reveals=[
            reveal(1, sounds_great, seventeen_point, "But the median new app: under $50/mo at month 12",
                   tags=["number"]),
            reveal(1, seventeen_point, four_point_six, "17.3% reach $1K MRR in 2 years", tags=["number"]),
            reveal(1, four_point_six, both_tails, "4.6% reach $10K MRR in 2 years", tags=["number"]),
            reveal(1, both_tails, heres_thing_though, "Both tails are real · you don't get to pick which one you're in",
                   tags=["punchline"]),
        ],
        source="RevenueCat 2024/2026 [reported]",
        sfx=[{"cue": "tick", "at": sounds_great}, {"cue": "tick", "at": seventeen_point}, {"cue": "hit", "at": both_tails}]))

    # economics-04: costs + build/demand punchline merged
    screens.append(screen(id="economics-04", section="economics", layout="sheet",
        heading="What it costs", start=heres_thing_though, end=what_it_diversifies,
        reveals=[
            reveal(2, heres_thing_though, these_firms_avg, "The costs · mostly not money anymore", tags=["claim"]),
            reveal(2, these_firms_avg, what_you_spend, "Under 5 people · tools run tens of dollars a month",
                   tags=["number"]),
            reveal(2, what_you_spend, the_build_risk, "What you actually spend is time against that distribution above",
                   body="plus the risk that never went away: enrollment · attention · somebody actually paying",
                   tags=["process"]),
            reveal(2, the_build_risk, what_it_diversifies, "The build risk fell through the floor · the demand risk did not move",
                   tags=["punchline"]),
        ],
        source="Public tool pricing + Census SUSB firm-size data [derived]",
        sfx=[{"cue": "tick", "at": heres_thing_though}, {"cue": "hit", "at": the_build_risk}]))

    # economics-06: what it diversifies vs failure mode
    screens.append(screen(id="economics-06", section="economics", layout="risk_card",
        heading="Diversifies · and fails", start=what_it_diversifies, end=your_accumulated,
        reveals=[
            reveal(3, what_it_diversifies, and_the_failure, "What it diversifies is real",
                   body="income that doesn't depend on being chosen · skills that compound · optionality employment doesn't offer",
                   tags=["operator_pov"]),
            reveal(3, and_the_failure, your_accumulated, "The failure mode is equally real · ~70% stay under $1,000/mo",
                   body="a beacon of small profits invites clones the moment build cost falls for everybody",
                   tags=["number", "risk"]),
        ],
        source="Freemius, December 2025 (~70% under $1K MRR) [reported]",
        sfx=[{"cue": "hit", "at": and_the_failure}],
        custom={"risk": {"title": "A retention business dressed as a build business.",
            "body": "Your accumulated position is the only answer to symmetric build-cost collapse. It takes years, not weekends.",
            "bullets": ["~70% of micro-SaaS stays under $1,000/mo",
                        "Symmetric build-cost falls invite clones",
                        "Accumulated position takes years"]}}))

    # economics-07: the honest sentence — the closing axiom
    screens.append(screen(id="economics-07", section="economics", layout="sheet",
        heading="The honest sentence", start=your_accumulated, end=and_your_protection,
        reveals=[
            reveal(4, your_accumulated, so_heres_honest, "Your accumulated position takes years · not weekends", tags=["claim"]),
            reveal(4, so_heres_honest, the_count, "The count of viable small software businesses is rising", tags=["claim"]),
            reveal(4, the_count, and_your_protection, "The typical attempt is worth less than it used to be",
                   tags=["claim"]),
        ],
        source="Synthesis of the whole episode [derived]",
        sfx=[{"cue": "tick", "at": so_heres_honest}]))

    # economics-08: the closing axiom + the weird-part payoff merged (one long quote screen)
    screens.append(screen(id="economics-08", section="economics", layout="quote",
        heading="Same number", start=and_your_protection, end=ec1,
        reveals=[
            reveal(4, and_your_protection, three_decades, "Your protection and your ceiling are the same number",
                   tags=["punchline"]),
            reveal(4, three_decades, turns_out, "Three decades profitable in one storefront is not a consolation prize",
                   body="for having failed to become Amazon",
                   tags=["punchline"]),
            reveal(4, turns_out, ec1, "That might just be what a business is · the last twenty years might be the weird part",
                   tags=["punchline"]),
        ],
        source="Closing axiom [derived]",
        music={"intensity": "silence", "duck_db": 0},
        sfx=[{"cue": "hit", "at": and_your_protection}, {"cue": "hit", "at": turns_out}],
        custom={"quote": "Your protection and your ceiling are the same number.",
                "accentPhrase": "same number", "ground": "navy"}))

    # ============================================================
    # CTA (810.8 → 835.7s, 24.9s, 1 beat)
    # ============================================================
    c0, c1 = _SECTION_TIMING["cta"]
    its_free = fp("cta", "It's free")
    if_watching = fp("cta", "if watching a business model")

    screens.append(screen(id="cta-01", section="cta", layout="cta",
        heading="The Operator Blueprint", start=c0, end=c1,
        reveals=[
            reveal(1, c0, its_free, "№ 005 · Too Small to Bother",
                   body="the evaluation sheet · two questions · every number sourced",
                   tags=["cta"]),
            reveal(1, its_free, if_watching, "Free · link in the description", tags=["cta"]),
            reveal(1, if_watching, c1, "A business model taken apart honestly · every Monday · subscribe",
                   tags=["cta"]),
        ],
        source="OE blueprint distribution [derived]",
        sfx=[{"cue": "tick", "at": c0}, {"cue": "hit", "at": if_watching}]))

    return {"slug": "too-small-to-bother", "total_seconds": TOTAL_SECONDS, "screens": screens}


if __name__ == "__main__":
    sb = build()
    STORYBOARD.write_text(json.dumps(sb, indent=2))
    quotes = sum(1 for s in sb["screens"] if s["layout"] == "quote")
    proofs = sum(1 for s in sb["screens"] if s["layout"] == "proof_card")
    charts = sum(1 for s in sb["screens"] if s["layout"] == "chart")
    risks = sum(1 for s in sb["screens"] if s["layout"] == "risk_card")
    print(f"✓ storyboard → {STORYBOARD}")
    print(f"  {len(sb['screens'])} screens · {quotes} quotes · {proofs} proofs · "
          f"{charts} charts · {risks} risks")
    print(f"  anchor misses: {_WARN if _WARN else 'none'}")
