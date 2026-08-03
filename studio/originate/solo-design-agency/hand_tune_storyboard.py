"""Hand-tuned storyboard for №004 (solo-design-agency).

Real per-episode editorial pass — every proof_card gets custom.proof
populated with a specific value, every risk_card has custom.risk, every
quote screen has custom.quote. Reads vo/words.json + vo/timeline.json
and anchors every screen boundary to a real spoken phrase.

Mirrors the pattern established in ep003's hand_tune_storyboard.py.

Run:  python originate/solo-design-agency/hand_tune_storyboard.py
Emits: originate/solo-design-agency/storyboard.json
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


def section_bounds(section: str):
    return _SECTION_TIMING[section]


_WARN: list[str] = []


def fp(section: str, phrase: str, default: float) -> float:
    try:
        return find_phrase(section, phrase)[0]
    except ValueError:
        _WARN.append(f"{section}:{phrase}")
        return default


def screen(**kw):
    kw.setdefault("audio", f"vo/{kw['section']}.mp3")
    kw.setdefault("figure", None)
    kw.setdefault("source", None)
    kw.setdefault("music", {"intensity": "calm", "duck_db": -16})
    kw.setdefault("sfx", [])
    kw.setdefault("custom", None)
    return kw


def reveal(beat, at, end, title, body="", tags=None):
    return {"beat": beat, "at": at, "end": end, "title": title, "body": body,
            "tags": tags or ["claim"], "word_anchor": {"start": at, "end": end}}


def build() -> dict:
    screens: list[dict] = []

    # ===================== HOOK (0-17.5s) =====================
    h0, h1 = section_bounds("hook")
    reportedly = fp("hook", "reportedly pulling in", h0 + 2.5)
    ninetyfive = fp("hook", "ninety-five bucks", h0 + 8.5)
    meanwhile = fp("hook", "meanwhile a venture-backed competitor", h0 + 12.5)
    # chapter ceremony — very short (17s section total)
    screens.append(screen(id="hook-00a", section="hook", layout="chapter_reset",
        heading="The Operator Economy", start=h0, end=reportedly,
        reveals=[reveal(0, h0, reportedly, "The Operator Economy")],
        custom={"kicker": "BUILD · OWN · OPERATE"}, sfx=[{"cue": "tick", "at": h0}]))
    # title card while the reveal number lands
    screens.append(screen(id="hook-00b", section="hook", layout="sheet",
        heading="Operator Blueprint", start=reportedly, end=ninetyfive,
        reveals=[reveal(0, reportedly, ninetyfive, "One business you can build on your own")],
        custom={"titleCard": {"overline": "Operator Blueprint · № 004",
            "title": "The Solo Design Agency",
            "thesis": "One person, ninety-five bucks in tools, doing the work of an 850-employee competitor."}},
        sfx=[{"cue": "tick", "at": reportedly}]))
    # solo revenue proof card
    screens.append(screen(id="hook-01", section="hook", layout="proof_card",
        heading="The gap", start=ninetyfive, end=meanwhile,
        reveals=[reveal(1, ninetyfive, meanwhile, "One-operator agency", tags=["number"])],
        source="Designjoy self-reported range — Starter Story, Startup Stash [reported ⚠]",
        music={"intensity": "build", "duck_db": -8}, sfx=[{"cue": "hit", "at": ninetyfive}],
        custom={"proof": {"value": 3, "prefix": "$", "suffix": "M/yr",
            "label": "One operator · reported $1–3M/yr · $95/mo in tools",
            "source": "Designjoy self-reported — aggregated secondary sources", "estimate": True}}))
    # competitor proof card
    screens.append(screen(id="hook-02", section="hook", layout="proof_card",
        heading="The gap", start=meanwhile, end=h1,
        reveals=[reveal(1, meanwhile, h1, "Venture-backed competitor", tags=["number"])],
        source="getLatka; PitchBook — Superside headcount [reported]",
        music={"intensity": "build", "duck_db": -8}, sfx=[{"cue": "hit", "at": meanwhile}],
        custom={"proof": {"value": 850, "suffix": " employees",
            "label": "Superside · same subscription-design product, venture-scale",
            "source": "getLatka; PitchBook — Superside headcount [reported]"}}))

    # ===================== THESIS (17.52-85.8s) =====================
    t0, t1 = section_bounds("thesis")
    flat = fp("thesis", "flat monthly fee", t0 + 8)
    startups = fp("thesis", "and startups small companies", flat + 4)
    pitch = fp("thesis", "that's the pitch", startups + 8)
    figma = fp("thesis", "the answer is figma", pitch + 6)
    ai = fp("thesis", "its ai features", figma + 3)
    whole = fp("thesis", "that's the whole ballgame", ai + 6)
    layout_line = fp("thesis", "the same layout work", whole + 4)
    solo = fp("thesis", "so built solo", layout_line + 12)
    full = fp("thesis", "built full time though", solo + 6)
    # thesis-01: definition, split so nothing dead-holds
    screens.append(screen(id="thesis-01", section="thesis", layout="sheet",
        heading="The thesis", start=t0, end=pitch,
        reveals=[reveal(1, t0, flat, "Design subscription: ongoing creative work"),
                 reveal(1, flat, startups, "Flat monthly fee, not billing by project"),
                 reveal(1, startups, pitch, "Cheaper than hiring · faster than posting a job",
                        tags=["process"])],
        source="Brainy Papers — productized design services model [vendor]",
        sfx=[{"cue": "tick", "at": t0}]))
    # thesis-02: the reason (short) — sets up the proof
    screens.append(screen(id="thesis-02", section="thesis", layout="sheet",
        heading="The thesis", start=pitch, end=ai,
        reveals=[reveal(2, pitch, figma, "How does one person do all that?", tags=["question"]),
                 reveal(2, figma, ai, "The answer is Figma", tags=["tool"])],
        sfx=[{"cue": "tick", "at": pitch}]))
    # thesis-03: 70% adoption — the proof
    screens.append(screen(id="thesis-03", section="thesis", layout="proof_card",
        heading="The thesis", start=ai, end=whole,
        reveals=[reveal(2, ai, whole, "Figma AI adoption", tags=["number"])],
        source="Figma Q1 2026 disclosure [reported]",
        music={"intensity": "build", "duck_db": -10}, sfx=[{"cue": "hit", "at": ai}],
        custom={"proof": {"value": 70, "suffix": "%",
            "label": "of Figma's active users are on its AI features (Q1 2026)",
            "source": "Figma Q1 2026 disclosure [reported]"}}))
    # thesis-03b: what the 70% MEANS — the elaboration
    screens.append(screen(id="thesis-03b", section="thesis", layout="sheet",
        heading="The thesis", start=whole, end=solo,
        reveals=[reveal(2, whole, layout_line, "That's the whole ballgame", tags=["punchline"]),
                 reveal(2, layout_line, solo, "Layout + variant work that used to take a team",
                        "now runs inside a single file · operated by one person",
                        tags=["tool"])],
        sfx=[{"cue": "tick", "at": whole}]))
    # thesis-04: solo vs full-time (schematic breaks the sheet run)
    screens.append(screen(id="thesis-04", section="thesis", layout="schematic",
        heading="The thesis", start=solo, end=t1,
        reveals=[reveal(3, solo, full, "Solo, part-time",
                        "a handful of retainer clients · nothing crazy", tags=["process"]),
                 reveal(3, full, t1, "Full-time, the reference case",
                        "~35 concurrent clients · one flat price · same stack", tags=["number"])],
        source="Medium/Zack Liu — Designjoy operating shape [reported, self-sourced]",
        sfx=[{"cue": "tick", "at": solo}]))

    # ===================== EVIDENCE (85.8-334.7s, 249s, 10 beats) =====================
    e0, e1 = section_bounds("evidence")
    reference = fp("evidence", "the reference case here is designjoy", e0 + 1)
    messy = fp("evidence", "genuinely messy", reference + 8)
    plainly = fp("evidence", "worth just saying that plainly", messy + 3)
    depending = fp("evidence", "depending on which post", plainly + 6)
    traces = fp("evidence", "every single one of those traces back", depending + 22)
    audited = fp("evidence", "there is no audited figure", traces + 4)
    consistent = fp("evidence", "what's consistent across every version", audited + 4)
    zero = fp("evidence", "zero contractors zero employees", consistent + 4)
    template = fp("evidence", "he started on a twenty nine dollar", zero + 12)
    busy = fp("evidence", "my own version of this busylobby", template + 6)
    scout = fp("evidence", "scout hotel accounts", busy + 6)
    six = fp("evidence", "six outreach emails so far", scout + 10)
    handle = fp("evidence", "and i want to handle that number carefully", six + 4)
    bench = fp("evidence", "reported cold outreach benchmarks", handle + 6)
    ratio = fp("evidence", "it's an anecdote with a good ratio", bench + 18)
    concretely = fp("evidence", "concretely for one of those six", ratio + 8)
    austin = fp("evidence", "a boutique hotel in austin", concretely + 3)
    forty = fp("evidence", "in about forty minutes", austin + 12)
    clicked = fp("evidence", "already clicked that link twice", forty + 20)
    other = fp("evidence", "now the other end of this", clicked + 4)
    superside = fp("evidence", "superside sells the identical shape", other + 3)
    fortyfour = fp("evidence", "forty four point nine million", superside + 8)
    fifty = fp("evidence", "employ roughly eight hundred fifty people", fortyfour + 12)
    minimum = fp("evidence", "their reported minimum is fifteen thousand", fifty + 6)
    orders = fp("evidence", "roughly three orders of magnitude apart", minimum + 12)
    third = fp("evidence", "there's a third number", orders + 6)
    figma_public = fp("evidence", "went public last july", third + 6)
    billion_rev = fp("evidence", "did just over a billion in revenue", figma_public + 8)
    industry = fp("evidence", "the us design services industry", billion_rev + 8)
    fair = fp("evidence", "that's not a fair comparison", industry + 12)
    durable = fp("evidence", "where the market thinks the durable money", fair + 6)
    left = fp("evidence", "what's actually left for one person", e1 - 3)

    # evidence-01: intro Designjoy + the "messy" caveat
    screens.append(screen(id="evidence-01", section="evidence", layout="sheet",
        heading="The evidence", start=e0, end=plainly,
        reveals=[reveal(1, e0, reference, "The reference case: Designjoy"),
                 reveal(1, reference, messy, "Brett Williams · one operator · since 2017",
                        tags=["operator_pov"]),
                 reveal(1, messy, plainly, "And the numbers around it are messy", tags=["risk"])],
        source="Starter Story, Startup Stash, startupfounderstories — self-reported",
        sfx=[{"cue": "tick", "at": e0}]))
    # evidence-01b: the risk card explaining the honest gap
    screens.append(screen(id="evidence-01b", section="evidence", layout="risk_card",
        heading="The evidence", start=plainly, end=depending,
        reveals=[reveal(1, plainly, depending, "Say it plainly · don't pick the flattering one",
                        tags=["risk"])],
        sfx=[{"cue": "tick", "at": plainly}],
        custom={"risk": {"title": "Every Designjoy figure traces back to one man's own posts.",
            "body": "There's no audited number. The story is real; the arithmetic is his.",
            "bullets": ["Numbers vary $1M–$3.1M/yr across secondary sources",
                        "All ultimately sourced to Brett Williams himself",
                        "No independent audit exists at this scale"]}}))
    # evidence-02: the chart of reported figures (LLM-generated asset spec)
    screens.append(screen(id="evidence-02", section="evidence", layout="chart",
        heading="The evidence", start=depending, end=traces,
        reveals=[reveal(2, depending, traces, "Reported ranges across sources", tags=["number"])],
        source="Aggregated: Starter Story, Startup Stash, startupfounderstories [reported ⚠]",
        sfx=[{"cue": "tick", "at": depending}]))
    # evidence-02b: no audited figure — the punch, then the transition
    screens.append(screen(id="evidence-02b", section="evidence", layout="quote",
        heading="The evidence", start=traces, end=audited,
        reveals=[reveal(2, traces, audited, "There is no audited figure.", tags=["punchline", "risk"])],
        music={"intensity": "silence", "duck_db": 0}, sfx=[{"cue": "hit", "at": traces}],
        custom={"quote": "There is no audited figure.",
                "accentPhrase": "audited", "ground": "navy"}))
    # evidence-03: the consistent shape → proof card (35 clients @ $4,995)
    screens.append(screen(id="evidence-03", section="evidence", layout="proof_card",
        heading="The evidence", start=audited, end=zero,
        reveals=[reveal(3, audited, consistent, "What IS consistent across every version"),
                 reveal(3, consistent, zero, "Reported by him, every telling")],
        source="Medium/Zack Liu; startupfounderstories [reported ⚠]",
        sfx=[{"cue": "hit", "at": audited}],
        custom={"proof": {"value": 4995, "prefix": "$", "suffix": "/mo",
            "label": "~35 clients · zero employees · one flat price",
            "source": "Medium/Zack Liu; startupfounderstories [reported ⚠]"}}))
    # evidence-03b: origin story sheet
    screens.append(screen(id="evidence-03b", section="evidence", layout="sheet",
        heading="The evidence", start=zero, end=template,
        reveals=[reveal(3, zero, template, "The shape, spelled out",
                        "0 contractors · 0 employees · ~35 clients · $4,995/mo · ~5 hrs/day",
                        tags=["number"])],
        source="Medium/Zack Liu; startupfounderstories [reported ⚠]"))
    screens.append(screen(id="evidence-03c", section="evidence", layout="sheet",
        heading="The evidence", start=template, end=busy,
        reveals=[reveal(3, template, busy, "Started on a $29 template + a Product Hunt launch",
                        tags=["number"])],
        source="Startup Stash; startupfounderstories [reported ⚠]"))
    # evidence-04: BusyLobby — the operator-POV pipeline
    screens.append(screen(id="evidence-04", section="evidence", layout="screen_rec",
        heading="The evidence", start=busy, end=scout,
        reveals=[reveal(4, busy, scout, "My own version: BusyLobby",
                        "not a revenue case yet · be direct about that", tags=["operator_pov", "risk"])],
        source="First-party — busylobby repo (n=6, Jul 2026)",
        sfx=[{"cue": "tick", "at": busy}]))
    # evidence-04b: the pipeline shape (schematic breaks sheet run)
    screens.append(screen(id="evidence-04b", section="evidence", layout="schematic",
        heading="The evidence", start=scout, end=six,
        reveals=[reveal(4, scout, six, "The pipeline",
                        "Scout · score · build demo BEFORE pitching · outreach · track opens · call",
                        tags=["process"])],
        source="First-party — busylobby methodology"))
    # evidence-05a: the current numbers → proof card
    screens.append(screen(id="evidence-05a", section="evidence", layout="proof_card",
        heading="The evidence", start=six, end=handle,
        reveals=[reveal(4, six, handle, "So far", tags=["number", "operator_pov"])],
        source="First-party — busylobby tracking/autopilot-pipeline.csv (n=6, Jul 2026)",
        sfx=[{"cue": "hit", "at": six}],
        custom={"proof": {"value": 1, "suffix": " of 6",
            "label": "Six outreach emails · one callback · no signed client · n=6",
            "source": "First-party — busylobby (n=6, Jul 2026)"}}))
    # evidence-05b: the honesty check — benchmarks in context
    screens.append(screen(id="evidence-05b", section="evidence", layout="sheet",
        heading="The evidence", start=handle, end=ratio,
        reveals=[reveal(5, handle, bench, "And I want to handle that number carefully"),
                 reveal(5, bench, ratio, "2026 cold-email benchmark: 3–5% avg · ~5.8% for <50 recipients",
                        tags=["number"])],
        source="Apollo / Instantly / Belkins — 2026 B2B cold-email benchmarks [reported]"))
    # evidence-05c: honest anti-conclusion — quote
    screens.append(screen(id="evidence-05c", section="evidence", layout="quote",
        heading="The evidence", start=ratio, end=concretely,
        reveals=[reveal(5, ratio, concretely, "Six emails is not a sample. It's an anecdote with a good ratio.",
                        tags=["punchline", "operator_pov"])],
        music={"intensity": "silence", "duck_db": 0}, sfx=[{"cue": "hit", "at": ratio}],
        custom={"quote": "Six emails is not a sample. It's an anecdote with a good ratio.",
                "accentPhrase": "not a sample", "ground": "navy"}))
    # evidence-06: the Austin demo, before/after
    screens.append(screen(id="evidence-06", section="evidence", layout="screen_rec",
        heading="The evidence", start=concretely, end=forty,
        reveals=[reveal(6, concretely, austin, "For one of those six", tags=["operator_pov"]),
                 reveal(6, austin, forty, "A boutique hotel in Austin",
                        "scraped their site photos + real room menu", tags=["operator_pov"])],
        source="First-party — BusyLobby prospect demo (Austin, Jul 2026)",
        sfx=[{"cue": "tick", "at": concretely}]))
    # evidence-06b: the 40-min build → proof card (time)
    screens.append(screen(id="evidence-06b", section="evidence", layout="proof_card",
        heading="The evidence", start=forty, end=clicked,
        reveals=[reveal(6, forty, clicked, "The build", tags=["number", "operator_pov"])],
        source="First-party — Austin hotel demo (Jul 2026)",
        sfx=[{"cue": "hit", "at": forty}],
        custom={"proof": {"value": 40, "suffix": " min",
            "label": "Working lobby-tablet interface · v0 for shell · Figma to polish",
            "source": "First-party — Austin hotel demo (Jul 2026)"}}))
    # evidence-06c: the callback story — sheet
    screens.append(screen(id="evidence-06c", section="evidence", layout="sheet",
        heading="The evidence", start=clicked, end=other,
        reveals=[reveal(6, clicked, other, "The one callback",
                        "came from a prospect who'd already clicked the demo link twice",
                        tags=["operator_pov"])]))
    # evidence-07: Superside intro + ARR chart (transition)
    screens.append(screen(id="evidence-07", section="evidence", layout="sheet",
        heading="The evidence", start=other, end=superside,
        reveals=[reveal(7, other, superside, "Now the other end of this", tags=["number"])],
        sfx=[{"cue": "tick", "at": other}]))
    # evidence-07b: Superside ARR chart
    screens.append(screen(id="evidence-07b", section="evidence", layout="chart",
        heading="The evidence", start=superside, end=fifty,
        reveals=[reveal(7, superside, fortyfour, "Superside sells the identical shape"),
                 reveal(7, fortyfour, fifty, "$44.9M ARR (2024) · up from $30.8M (2023)",
                        tags=["number"])],
        source="getLatka; PitchBook — Superside ARR [reported]",
        music={"intensity": "build", "duck_db": -10}, sfx=[{"cue": "hit", "at": superside}]))
    # evidence-07c: 850 people / 450 clients — proof
    screens.append(screen(id="evidence-07c", section="evidence", layout="proof_card",
        heading="The evidence", start=fifty, end=minimum,
        reveals=[reveal(7, fifty, minimum, "To deliver it", tags=["number"])],
        source="getLatka; PitchBook — Superside headcount [reported]",
        sfx=[{"cue": "hit", "at": fifty}],
        custom={"proof": {"value": 850, "suffix": " people",
            "label": "Superside · 450 clients · $35M raised",
            "source": "getLatka; PitchBook [reported]"}}))
    # evidence-08: price gap → proof card ($15K vs $5K)
    screens.append(screen(id="evidence-08", section="evidence", layout="proof_card",
        heading="The evidence", start=minimum, end=orders,
        reveals=[reveal(8, minimum, orders, "Superside minimum vs Designjoy list", tags=["number"])],
        source="Vendr — Superside pricing [reported]",
        sfx=[{"cue": "hit", "at": minimum}],
        custom={"proof": {"value": 15000, "prefix": "$", "suffix": "/mo",
            "label": "Superside minimum · vs Designjoy's $5,000 list — same category",
            "source": "Vendr — Superside pricing [reported]"}}))
    # evidence-08b: the read on the gap
    screens.append(screen(id="evidence-08b", section="evidence", layout="quote",
        heading="The evidence", start=orders, end=third,
        reveals=[reveal(8, orders, third, "Three orders of magnitude apart in headcount to deliver it.",
                        tags=["punchline", "number"])],
        music={"intensity": "silence", "duck_db": 0}, sfx=[{"cue": "hit", "at": orders}],
        custom={"quote": "Three orders of magnitude apart. Same product.",
                "accentPhrase": "three orders of magnitude", "ground": "paper"}))
    # evidence-09: Figma — the third number that reframes both
    screens.append(screen(id="evidence-09", section="evidence", layout="sheet",
        heading="The evidence", start=third, end=figma_public,
        reveals=[reveal(9, third, figma_public, "A third number reframes both", tags=["number"])],
        sfx=[{"cue": "tick", "at": third}]))
    # evidence-09b: Figma IPO — proof card ($68B day-one)
    screens.append(screen(id="evidence-09b", section="evidence", layout="proof_card",
        heading="The evidence", start=figma_public, end=billion_rev,
        reveals=[reveal(9, figma_public, billion_rev, "Figma IPO, day one", tags=["number"])],
        source="Figma FY2025 results + Q1 2026 disclosure [verified]",
        music={"intensity": "build", "duck_db": -10}, sfx=[{"cue": "hit", "at": figma_public}],
        custom={"proof": {"value": 68000000000, "compactCurrency": True,
            "label": "Figma · closed first day at ~$68B",
            "source": "Figma FY2025 results + Q1 2026 disclosure [verified]"}}))
    # evidence-09c: Figma revenue chart (~$1B → $1.5B guidance)
    screens.append(screen(id="evidence-09c", section="evidence", layout="chart",
        heading="The evidence", start=billion_rev, end=industry,
        reveals=[reveal(9, billion_rev, industry, "Figma revenue: FY2025 → FY2026 guidance",
                        tags=["number"])],
        source="Figma FY2025 results + Q1 2026 disclosure [verified]"))
    # evidence-10: $15B industry — proof
    screens.append(screen(id="evidence-10", section="evidence", layout="proof_card",
        heading="The evidence", start=industry, end=fair,
        reveals=[reveal(10, industry, fair, "The industry Figma sells into", tags=["number"])],
        source="IBISWorld — US graphic design services $15.1B (2026)",
        sfx=[{"cue": "hit", "at": industry}],
        custom={"proof": {"value": 15100000000, "compactCurrency": True,
            "label": "US graphic design services · ~$15.1B/yr · thousands of small shops",
            "source": "IBISWorld (2026)", "estimate": True}}))
    # evidence-10b: the caveat (fair comparison)
    screens.append(screen(id="evidence-10b", section="evidence", layout="sheet",
        heading="The evidence", start=fair, end=durable,
        reveals=[reveal(10, fair, durable, "That's not a fair comparison",
                        "one is a stock price · the other, yearly billings", tags=["risk"])]))
    # evidence-10c: the punch — quote
    screens.append(screen(id="evidence-10c", section="evidence", layout="quote",
        heading="The evidence", start=durable, end=e1,
        reveals=[reveal(10, durable, left, "The tool vendor captured the category.",
                        tags=["punchline"]),
                 reveal(10, left, e1, "What's actually left for one person?", tags=["question"])],
        music={"intensity": "silence", "duck_db": 0}, sfx=[{"cue": "hit", "at": durable}],
        custom={"quote": "So what's actually left for one person?",
                "accentPhrase": "one person", "ground": "navy"}))

    # ===================== STACK (334.7-469s, 134s) =====================
    s0, s1 = section_bounds("stack")
    plan_in = fp("stack", "you plan in figma or relume", s0 + 8)
    produce = fp("stack", "you produce in figma make", plan_in + 5)
    imagery = fp("stack", "you generate imagery in midjourney", produce + 6)
    surface = fp("stack", "figma with figma make", imagery + 2)
    relume = fp("stack", "relume handles wireframing", surface + 8)
    v0_line = fp("stack", "v0 and lovable turn a prompt", relume + 6)
    framer = fp("stack", "framer ships the final site", v0_line + 12)
    designjoy_cost = fp("stack", "designjoy's own reported tool cost", framer + 12)
    ninetyfive_stack = fp("stack", "ninety five bucks a month total", designjoy_cost + 4)
    client_pays = fp("stack", "the client pays for their own software", ninetyfive_stack + 3)
    doesnt_pick = fp("stack", "here's the thing the stack doesn't do", client_pays + 3)
    good_looking = fp("stack", "three of these tools will each hand you", doesnt_pick + 4)
    austin_stack = fp("stack", "on the austin hotel demo", good_looking + 12)
    stock_photo = fp("stack", "the same stock lobby photo", austin_stack + 8)
    right_call = fp("stack", "the right call was to throw both out", stock_photo + 6)
    one_thing = fp("stack", "one thing to know", right_call + 10)
    half = fp("stack", "more than half of its largest customers", one_thing + 5)
    same_buttons = fp("stack", "your clients have the same buttons", half + 6)
    gap_product = fp("stack", "and that gap that's the actual product", same_buttons + 6)
    knowing = fp("stack", "but knowing the stack isn't the same", s1 - 4)

    # stack-01: the shape (4-step schematic)
    screens.append(screen(id="stack-01", section="stack", layout="schematic",
        heading="The stack", start=s0, end=surface,
        reveals=[reveal(1, s0, plan_in, "Two or three tools deep · not seven"),
                 reveal(1, plan_in, produce, "Plan: Figma or Relume", tags=["tool"]),
                 reveal(1, produce, imagery, "Produce: Figma Make · v0 · Lovable · Ship: Framer",
                        tags=["tool"]),
                 reveal(1, imagery, surface, "Imagery: Midjourney", tags=["tool"])],
        source="Guideflow — AI design tool stacking patterns [vendor]",
        sfx=[{"cue": "tick", "at": s0}]))
    # stack-02a: Figma + Figma Make + Relume — pricing
    screens.append(screen(id="stack-02a", section="stack", layout="sheet",
        heading="The stack", start=surface, end=v0_line,
        reveals=[reveal(2, surface, relume, "Figma + Figma Make — free to start", tags=["tool"]),
                 reveal(2, relume, v0_line, "Relume — $38/mo solo", tags=["tool", "number"])],
        source="buildmvpfast — pricing comparison [vendor]",
        sfx=[{"cue": "tick", "at": surface}]))
    # stack-02b: v0 + Lovable + Framer/Midjourney/Claude
    screens.append(screen(id="stack-02b", section="stack", layout="sheet",
        heading="The stack", start=v0_line, end=designjoy_cost,
        reveals=[reveal(2, v0_line, framer, "v0 / Lovable — free to $25/mo solo tier",
                        tags=["tool", "number"]),
                 reveal(2, framer, designjoy_cost, "Framer $20–40 · Midjourney $10–60 · Claude $20–100",
                        tags=["tool", "number"])],
        source="buildmvpfast — pricing comparison [vendor]"))
    # stack-03: <$95/mo total — proof card
    screens.append(screen(id="stack-03", section="stack", layout="proof_card",
        heading="The stack", start=designjoy_cost, end=doesnt_pick,
        reveals=[reveal(3, designjoy_cost, ninetyfive_stack, "Designjoy's reported tool cost"),
                 reveal(3, ninetyfive_stack, client_pays, "Total · every month", tags=["number"])],
        source="startupfounderstories — Designjoy tool cost [reported ⚠]",
        music={"intensity": "build", "duck_db": -10}, sfx=[{"cue": "hit", "at": designjoy_cost}],
        custom={"proof": {"value": 95, "prefix": "$", "suffix": "/mo",
            "label": "The client pays for their own software · not you",
            "source": "startupfounderstories — Designjoy tool cost [reported ⚠]"}}))
    # stack-04: what the stack won't do (Austin story setup)
    screens.append(screen(id="stack-04", section="stack", layout="sheet",
        heading="The stack", start=doesnt_pick, end=austin_stack,
        reveals=[reveal(4, doesnt_pick, good_looking, "The stack doesn't pick",
                        "for this brand · this audience · this week", tags=["process"]),
                 reveal(4, good_looking, austin_stack, "Three tools · three good-looking options",
                        "choosing is the part that stays yours", tags=["operator_pov"])],
        sfx=[{"cue": "tick", "at": doesnt_pick}]))
    # stack-04b: Austin demo — v0 + Figma Make defaulted to same stock photo
    screens.append(screen(id="stack-04b", section="stack", layout="screen_rec",
        heading="The stack", start=austin_stack, end=right_call,
        reveals=[reveal(4, austin_stack, stock_photo, "On the Austin hotel demo",
                        tags=["operator_pov"]),
                 reveal(4, stock_photo, right_call, "Both defaulted to the same stock lobby photo",
                        "already on two competitor sites in the same city", tags=["risk"])],
        source="First-party — BusyLobby prospect demo",
        sfx=[{"cue": "tick", "at": austin_stack}]))
    # stack-04c: the operator decision — sheet
    screens.append(screen(id="stack-04c", section="stack", layout="sheet",
        heading="The stack", start=right_call, end=one_thing,
        reveals=[reveal(4, right_call, one_thing, "Throw both out · shoot a 15-second phone video",
                        "a decision the software had no way to make", tags=["operator_pov"])],
        source="First-party — Austin hotel demo"))
    # stack-05: the clients have the same tools — proof card (>50%)
    screens.append(screen(id="stack-05", section="stack", layout="proof_card",
        heading="The stack", start=one_thing, end=same_buttons,
        reveals=[reveal(5, one_thing, half, "Figma's largest customers"),
                 reveal(5, half, same_buttons, "Generate designs in Make · weekly", tags=["number"])],
        source="Figma Q4 2025 disclosure [reported]",
        sfx=[{"cue": "hit", "at": one_thing}],
        custom={"proof": {"value": 50, "prefix": ">", "suffix": "%",
            "label": "of Figma's largest customers now generate in Make every week",
            "source": "Figma Q4 2025 disclosure [reported]"}}))
    # stack-05b: same buttons, different judgment — punchline
    screens.append(screen(id="stack-05b", section="stack", layout="quote",
        heading="The stack", start=same_buttons, end=gap_product,
        reveals=[reveal(5, same_buttons, gap_product, "Your clients have the same buttons you do.",
                        tags=["punchline", "risk"])],
        music={"intensity": "silence", "duck_db": 0}, sfx=[{"cue": "hit", "at": same_buttons}],
        custom={"quote": "Your clients have the same buttons you do.",
                "accentPhrase": "same buttons", "ground": "navy"}))
    # stack-05c: the gap IS the product — closer + transition
    screens.append(screen(id="stack-05c", section="stack", layout="sheet",
        heading="The stack", start=gap_product, end=s1,
        reveals=[reveal(5, gap_product, knowing, "The hours or the judgment · that gap IS the product",
                        tags=["punchline"]),
                 reveal(5, knowing, s1, "But knowing the stack isn't the same as knowing how to get the first person to pay for it.",
                        tags=["question"])]))

    # ===================== PLAYBOOK (469-643s, 174s) =====================
    p0, p1 = section_bounds("playbook")
    pick_niche = fp("playbook", "you pick a narrow niche", p0 + 2)
    landing = fp("playbook", "landing pages for saas", pick_niche + 4)
    three_demos = fp("playbook", "and you build three demo pieces", landing + 6)
    no_client = fp("playbook", "no client yet", three_demos + 5)
    demo_pitch = fp("playbook", "the demo is the pitch", no_client + 2)
    scout_score = fp("playbook", "the scout and score approach", demo_pitch + 3)
    build_fix = fp("playbook", "then build the fix", scout_score + 14)
    week_two = fp("playbook", "week two through four", build_fix + 4)
    posthog = fp("playbook", "a tool like posthog", week_two + 14)
    first_calls = fp("playbook", "those are your first calls", posthog + 5)
    price_first = fp("playbook", "price the first client under market", first_calls + 3)
    twenty_five = fp("playbook", "somewhere in the twenty five hundred range", price_first + 4)
    move_toward = fp("playbook", "then you move toward the four to seven", twenty_five + 8)
    capacity = fp("playbook", "it's capacity math", move_toward + 12)
    thirty_five = fp("playbook", "thirty five clients is one person's", capacity + 10)
    ceiling = fp("playbook", "the real limit is the turnaround", thirty_five + 6)
    refuse = fp("playbook", "what you refuse to do", ceiling + 6)
    five_hundred = fp("playbook", "the reported bottom of this market", refuse + 3)
    cannot_win = fp("playbook", "you cannot win there", five_hundred + 10)
    narrow_scope = fp("playbook", "narrow scope is what lets you charge", cannot_win + 3)
    one_type = fp("playbook", "one type of client", narrow_scope + 8)
    build_renewal = fp("playbook", "build the renewal into month one", one_type + 8)
    retention_biz = fp("playbook", "because this is a retention business", build_renewal + 3)
    depends = fp("playbook", "your revenue depends on how long clients", retention_biz + 5)
    monthly_recap = fp("playbook", "send the monthly recap nobody asked for", depends + 12)
    first_client = fp("playbook", "and your first client", monthly_recap + 14)
    warm_pays = fp("playbook", "the warm one is how you get paid", first_client + 20)
    what_pay = fp("playbook", "so what does this actually pay", p1 - 3)

    # playbook-01: week 1 pick + build 3 demos
    screens.append(screen(id="playbook-01", section="playbook", layout="sheet",
        heading="The playbook", start=p0, end=no_client,
        reveals=[reveal(1, p0, pick_niche, "Week 1: pick a narrow niche"),
                 reveal(1, pick_niche, landing, "SaaS landing pages · hotel sites · pitch decks",
                        tags=["process"]),
                 reveal(1, landing, three_demos, "Doesn't matter which · but NARROW", tags=["process"]),
                 reveal(1, three_demos, no_client, "Build three demo pieces for real companies",
                        tags=["process"])],
        sfx=[{"cue": "tick", "at": p0}]))
    # playbook-01b: the demo IS the pitch — quote
    screens.append(screen(id="playbook-01b", section="playbook", layout="quote",
        heading="The playbook", start=no_client, end=scout_score,
        reveals=[reveal(1, no_client, demo_pitch, "The demo is the pitch.", tags=["punchline"])],
        music={"intensity": "silence", "duck_db": 0}, sfx=[{"cue": "hit", "at": no_client}],
        custom={"quote": "No client yet. The demo is the pitch.",
                "accentPhrase": "the demo", "ground": "navy"}))
    # playbook-02: scout-and-score
    screens.append(screen(id="playbook-02", section="playbook", layout="schematic",
        heading="The playbook", start=scout_score, end=week_two,
        reveals=[reveal(2, scout_score, build_fix, "Scout-and-score approach",
                        "short list · score how bad their current thing is · build the fix",
                        tags=["process"]),
                 reveal(2, build_fix, week_two, "BEFORE you ever email them",
                        tags=["operator_pov"])],
        source="First-party — busylobby pipeline methodology",
        sfx=[{"cue": "tick", "at": scout_score}]))
    # playbook-03: week 2-4 send the demo cold + PostHog
    screens.append(screen(id="playbook-03", section="playbook", layout="sheet",
        heading="The playbook", start=week_two, end=posthog,
        reveals=[reveal(3, week_two, posthog, "Weeks 2–4: send the finished demo cold",
                        "not a pitch deck · the actual thing", tags=["process"])],
        source="First-party — busylobby methodology",
        sfx=[{"cue": "tick", "at": week_two}]))
    screens.append(screen(id="playbook-03b", section="playbook", layout="screen_rec",
        heading="The playbook", start=posthog, end=price_first,
        reveals=[reveal(3, posthog, first_calls, "PostHog shows which prospects looked twice",
                        tags=["tool"]),
                 reveal(3, first_calls, price_first, "Those are your first calls",
                        tags=["operator_pov"])],
        source="First-party — busylobby PostHog demo analytics"))
    # playbook-04: pricing setup — sheet
    screens.append(screen(id="playbook-04", section="playbook", layout="sheet",
        heading="The playbook", start=price_first, end=move_toward,
        reveals=[reveal(4, price_first, twenty_five, "First client: price UNDER market"),
                 reveal(4, twenty_five, move_toward, "~$2,500 range · buy a working case study fast",
                        tags=["number"])],
        source="Brainy Papers — solo pricing band [vendor]",
        sfx=[{"cue": "tick", "at": price_first}]))
    # playbook-04b: the target band — proof card
    screens.append(screen(id="playbook-04b", section="playbook", layout="proof_card",
        heading="The playbook", start=move_toward, end=capacity,
        reveals=[reveal(4, move_toward, capacity, "Once you have one finished project", tags=["number"])],
        source="Brainy Papers — $2,500–$7,500 solo pricing band [vendor]",
        sfx=[{"cue": "hit", "at": move_toward}],
        custom={"proof": {"value": 7000, "prefix": "$4,500–", "suffix": "/mo",
            "label": "The band once you have a case study to point at",
            "source": "Brainy Papers — solo pricing band [vendor]", "estimate": True}}))
    # playbook-05: capacity math — proof (35 clients ceiling)
    screens.append(screen(id="playbook-05", section="playbook", layout="proof_card",
        heading="The playbook", start=capacity, end=refuse,
        reveals=[reveal(5, capacity, thirty_five, "Month 2+: capacity math"),
                 reveal(5, thirty_five, ceiling, "One person's reported number · not a law",
                        tags=["number", "risk"])],
        source="Designjoy reported — Medium/Zack Liu [reported ⚠]",
        sfx=[{"cue": "hit", "at": capacity}],
        custom={"proof": {"value": 35, "suffix": " clients",
            "label": "Reported ceiling · the real limit is the turnaround you promised",
            "source": "Designjoy reported [⚠]", "estimate": True}}))
    # playbook-06: what you refuse (risk_card)
    screens.append(screen(id="playbook-06", section="playbook", layout="risk_card",
        heading="The playbook", start=refuse, end=cannot_win,
        reveals=[reveal(6, refuse, five_hundred, "One decision shapes everything else"),
                 reveal(6, five_hundred, cannot_win, "The reported market floor: $549/mo unlimited",
                        tags=["number", "risk"])],
        source="ManyPixels — commodity floor [reported, vendor]",
        sfx=[{"cue": "hit", "at": refuse}],
        custom={"risk": {"title": "You cannot win at $549/mo.",
            "body": "The commoditized bottom is a race you're not built to run. Narrow scope is what lets you charge ten times that.",
            "bullets": ["One type of client",
                        "One type of deliverable",
                        "One turnaround you actually hit — every time"]}}))
    # playbook-06b: what narrow scope buys you
    screens.append(screen(id="playbook-06b", section="playbook", layout="sheet",
        heading="The playbook", start=cannot_win, end=build_renewal,
        reveals=[reveal(6, cannot_win, narrow_scope, "Narrow scope lets you charge $5,000 instead",
                        tags=["process"]),
                 reveal(6, narrow_scope, build_renewal, "The three ONEs",
                        "one client type · one deliverable · one turnaround you actually hit",
                        tags=["process"])]))
    # playbook-07: retention business — quote punchline
    screens.append(screen(id="playbook-07", section="playbook", layout="quote",
        heading="The playbook", start=build_renewal, end=depends,
        reveals=[reveal(7, build_renewal, retention_biz, "Build the renewal into month one"),
                 reveal(7, retention_biz, depends, "This is a retention business dressed as a creative one.",
                        tags=["punchline"])],
        music={"intensity": "silence", "duck_db": 0}, sfx=[{"cue": "hit", "at": build_renewal}],
        custom={"quote": "This is a retention business dressed as a creative one.",
                "accentPhrase": "retention business", "ground": "navy"}))
    # playbook-07b: the ops that make renewals — sheet
    screens.append(screen(id="playbook-07b", section="playbook", layout="sheet",
        heading="The playbook", start=depends, end=first_client,
        reveals=[reveal(7, depends, monthly_recap, "Revenue depends on how long clients stay",
                        tags=["process"]),
                 reveal(7, monthly_recap, first_client, "The unglamorous retention ops",
                        "monthly recap nobody asked for · ship the small thing they mentioned",
                        tags=["process"])],
        sfx=[{"cue": "tick", "at": depends}]))
    # playbook-08: first client comes from warm — sheet
    screens.append(screen(id="playbook-08", section="playbook", layout="sheet",
        heading="The playbook", start=first_client, end=what_pay,
        reveals=[reveal(8, first_client, warm_pays, "Your first client almost never comes from the cold list",
                        "someone who already knows you · or the prospect who opened your demo twice",
                        tags=["operator_pov"]),
                 reveal(8, warm_pays, what_pay, "Cold teaches. Warm pays.", tags=["punchline"])],
        source="First-party — BusyLobby pipeline experience",
        sfx=[{"cue": "tick", "at": first_client}]))
    # playbook-09: the transition question
    screens.append(screen(id="playbook-09", section="playbook", layout="schematic",
        heading="The playbook", start=what_pay, end=p1,
        reveals=[reveal(8, what_pay, p1, "So what does this actually pay?", tags=["question"])]))

    # ===================== ECONOMICS (643-748s, 105s) =====================
    ec0, ec1 = section_bounds("economics")
    into_blueprint = fp("economics", "into a blueprint", ec0 + 8)
    realistic_range = fp("economics", "now realistic range", into_blueprint + 6)
    two_five = fp("economics", "somewhere in the two to five thousand", realistic_range + 12)
    estimate = fp("economics", "and that's an estimate", two_five + 6)
    full_time = fp("economics", "full time though", estimate + 10)
    one_three = fp("economics", "the self reported range runs", full_time + 8)
    no_audit = fp("economics", "that figure has no audit", one_three + 5)
    only_public = fp("economics", "just know it's the only public data point", no_audit + 6)
    skill = fp("economics", "what this actually diversifies is skill", only_public + 6)
    real_risk = fp("economics", "the real risk isn't the work", skill + 10)
    lose_three = fp("economics", "lose three of thirty five clients", real_risk + 4)
    fifteen_gone = fp("economics", "that's fifteen thousand dollars gone", lose_three + 6)
    harder = fp("economics", "and the harder failure mode", fifteen_gone + 4)
    pricing_page = fp("economics", "the pricing page copyable", harder + 4)
    six_million = fp("economics", "designjoy's own reported growth engine", pricing_page + 4)
    honest = fp("economics", "here's the honest version", six_million + 12)

    # economics-01: blueprint intro — sheet with CTA note
    screens.append(screen(id="economics-01", section="economics", layout="sheet",
        heading="The economics", start=ec0, end=realistic_range,
        reveals=[reveal(1, ec0, into_blueprint, "The blueprint — linked below"),
                 reveal(1, into_blueprint, realistic_range, "Scoring rubric · demo-first outreach · full tool stack",
                        tags=["cta"])],
        sfx=[{"cue": "tick", "at": ec0}]))
    # economics-02: part-time proof ($2-5K/mo)
    screens.append(screen(id="economics-02", section="economics", layout="proof_card",
        heading="The economics", start=realistic_range, end=full_time,
        reveals=[reveal(2, realistic_range, two_five, "Part-time (15–20 hrs/wk)"),
                 reveal(2, two_five, full_time, "Estimate · low end of the solo pricing band",
                        tags=["number", "risk"])],
        source="Brainy Papers pricing band; estimate at partial capacity",
        music={"intensity": "build", "duck_db": -10}, sfx=[{"cue": "hit", "at": realistic_range}],
        custom={"proof": {"value": 5000, "prefix": "$2,000–", "suffix": "/mo",
            "label": "A handful of clients · not a promise",
            "source": "Brainy Papers pricing band [estimate]", "estimate": True}}))
    # economics-03: full-time reported range — proof ($1-3M)
    screens.append(screen(id="economics-03", section="economics", layout="proof_card",
        heading="The economics", start=full_time, end=only_public,
        reveals=[reveal(3, full_time, one_three, "Full-time · Designjoy's reported shape"),
                 reveal(3, one_three, no_audit, "35 clients × $5K/mo · self-reported", tags=["number"]),
                 reveal(3, no_audit, only_public, "No independent audit", tags=["risk"])],
        source="Aggregated Designjoy sources [reported ⚠]",
        sfx=[{"cue": "hit", "at": full_time}],
        custom={"proof": {"value": 3, "prefix": "$1–", "suffix": "M/yr",
            "label": "Self-reported · the only public data point at this scale",
            "source": "Aggregated Designjoy [reported ⚠]", "estimate": True}}))
    # economics-04: diversification + churn risk setup
    screens.append(screen(id="economics-04", section="economics", layout="sheet",
        heading="The economics", start=only_public, end=real_risk,
        reveals=[reveal(4, only_public, skill, "Not just income — this diversifies skill",
                        tags=["operator_pov"]),
                 reveal(4, skill, real_risk, "Client acquisition · pricing · AI-tool fluency",
                        "transfers to any service business", tags=["process"])],
        sfx=[{"cue": "tick", "at": only_public}]))
    # economics-04b: churn — risk_card
    screens.append(screen(id="economics-04b", section="economics", layout="risk_card",
        heading="The economics", start=real_risk, end=harder,
        reveals=[reveal(4, real_risk, lose_three, "The real risk isn't the work"),
                 reveal(4, lose_three, fifteen_gone, "Lose 3 of 35 on flat pricing", tags=["risk"]),
                 reveal(4, fifteen_gone, harder, "That's $15,000 gone. In a month.",
                        tags=["number", "risk"])],
        source="Estimate from Designjoy's reported client count and price [reported ⚠]",
        sfx=[{"cue": "hit", "at": real_risk}],
        custom={"risk": {"title": "This is a retention business — churn eats it.",
            "body": "Lose 3 of 35 clients on flat pricing, by that same reported math, and $15,000 walks out the door in a single month.",
            "bullets": ["Flat monthly pricing amplifies churn",
                        "Revenue depends on how long clients stay",
                        "Retention ops are the actual work"]}}))
    # economics-05: distribution — risk_card
    screens.append(screen(id="economics-05", section="economics", layout="risk_card",
        heading="The economics", start=harder, end=honest,
        reveals=[reveal(5, harder, pricing_page, "Harder failure mode: distribution"),
                 reveal(5, pricing_page, six_million, "The pricing page? Copyable in an afternoon.",
                        tags=["punchline"]),
                 reveal(5, six_million, honest, "Designjoy's growth engine: ~6M tweet impressions, over years",
                        tags=["number", "risk"])],
        source="Designjoy stated Twitter growth driver [reported]",
        sfx=[{"cue": "hit", "at": harder}],
        custom={"risk": {"title": "The pricing page is copyable. The audience is not.",
            "body": "Designjoy's own reported growth engine was ~6M tweet impressions built over years — the part almost nobody selling this playbook mentions.",
            "bullets": ["Copying the offer takes an afternoon",
                        "Building the audience takes years",
                        "The distribution work is the moat"]}}))
    # economics-06: the honest punchline — quote
    screens.append(screen(id="economics-06", section="economics", layout="quote",
        heading="The economics", start=honest, end=ec1,
        reveals=[reveal(5, honest, ec1, "The tools got cheap. The audience never did.",
                        tags=["punchline"])],
        music={"intensity": "silence", "duck_db": 0}, sfx=[{"cue": "hit", "at": honest}],
        custom={"quote": "The tools got cheap. The audience never did.",
                "accentPhrase": "the audience", "ground": "paper"}))

    # ===================== CTA (748.14-771.61s, 23.5s) =====================
    c0, c1 = section_bounds("cta")
    free = fp("cta", "and look it's free", c0 + 12)
    subscribe = fp("cta", "so subscribe if you want", free + 3)
    screens.append(screen(id="cta-01", section="cta", layout="cta",
        heading="The Operator Blueprint", start=c0, end=c1,
        reveals=[reveal(1, c0, free, "№ 004 — The Solo Design Agency",
                        "Scoring rubric · demo-first outreach · full tool list · every source flagged",
                        tags=["cta"]),
                 reveal(1, free, subscribe, "Free · linked below", tags=["cta"]),
                 reveal(1, subscribe, c1, "Same format · different build · every Monday",
                        tags=["cta"])]))

    return {"slug": "solo-design-agency", "total_seconds": TOTAL_SECONDS, "screens": screens}


if __name__ == "__main__":
    sb = build()
    STORYBOARD.write_text(json.dumps(sb, indent=2))
    quotes = sum(1 for s in sb["screens"] if s["layout"] == "quote")
    proofs = sum(1 for s in sb["screens"] if s["layout"] == "proof_card")
    charts = sum(1 for s in sb["screens"] if s["layout"] == "chart")
    risks = sum(1 for s in sb["screens"] if s["layout"] == "risk_card")
    print(f"✓ storyboard → {STORYBOARD}")
    print(f"  {len(sb['screens'])} screens · {quotes} quotes · {proofs} proof cards · "
          f"{charts} charts · {risks} risk cards")
    print(f"  anchor misses: {_WARN if _WARN else 'none'}")
