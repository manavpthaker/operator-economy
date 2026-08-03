"""Hand-tuned storyboard for №003 (boring-automation-agency).

Rev 3 (2026-07-24): pacing re-tune. Every screen that used to hold a
single composition past ~18s is split at a real VO boundary. Proof/risk
cards (which stage via events, not the reveals array) are broken into a
short card + a follow-on sheet/schematic that carries the elaboration.
Long pull-quotes become a short impact frame + a follow-on. Follow-on
layouts are assigned to never stack >2 `sheet` screens (edit-rubric
kill). Rev 2 (2026-07-21): every data screen is self-contained — single
stats are proof_cards with an explicit custom.proof value; text moments
are sheets.

Voice-agnostic: reads vo/words.json + vo/timeline.json, anchors screens
to exact performed-VO phrases.

Run:  python originate/boring-automation-agency/hand_tune_storyboard.py
Emits: originate/boring-automation-agency/storyboard.json
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

    # ===================== HOOK =====================
    h0, h1 = section_bounds("hook")
    series = fp("hook", "a series where we break", h0 + 4)
    week = fp("hook", "this week", h0 + 8)
    zap = fp("hook", "zapier is worth around", h0 + 12)
    solo = fp("hook", "the solo version of that same job", (zap + h1) / 2)
    # series-open ceremony kept SHORT (retention: EP001's long open bled views)
    screens.append(screen(id="hook-00a", section="hook", layout="chapter_reset",
        heading="The Operator Economy", start=h0, end=series,
        reveals=[reveal(0, h0, series, "The Operator Economy")],
        custom={"kicker": "BUILD · OWN · OPERATE"}, sfx=[{"cue": "tick", "at": h0}]))
    screens.append(screen(id="hook-00b", section="hook", layout="sheet",
        heading="Operator Blueprint", start=series, end=zap,
        reveals=[reveal(0, series, week, "One business you can build on your own"),
                 reveal(0, week, zap, "This week: the least glamorous one",
                        "and why it quietly pays")],
        custom={"titleCard": {"overline": "Operator Blueprint · № 003",
            "title": "The Boring-Automation Agency",
            "thesis": "The unglamorous workflows small companies pay to never think about."}},
        sfx=[{"cue": "tick", "at": series}]))
    # gap: clean $5B → $500 (asset fixed to 2-series $)
    screens.append(screen(id="hook-01", section="hook", layout="gap",
        heading="The gap", start=zap, end=solo,
        reveals=[reveal(1, zap, solo, "Zapier ~$5B for one boring job")],
        source="Zapier ~$5B valuation — reported, market aggregators",
        music={"intensity": "build", "duck_db": -8}, sfx=[{"cue": "hit", "at": zap}]))
    screens.append(screen(id="hook-02", section="hook", layout="sheet",
        heading="The gap", start=solo, end=h1,
        reveals=[reveal(1, solo, h1, "The solo version of the same job",
                        "$500–5,000/mo per client · work most people find too dull to do")],
        source="Solo retainer bands — reported, agency guides",
        sfx=[{"cue": "tick", "at": solo}]))

    # ===================== THESIS =====================
    t0, t1 = section_bounds("thesis")
    companies = fp("thesis", "small companies run on a stack", t0 + 4)
    crm = fp("thesis", "the crm doesn't tell", t0 + 8)
    plumb = fp("thesis", "you build the plumbing between them", (crm + t1) / 2)
    thing = fp("thesis", "here's the thing though", plumb + 6)
    drag = fp("thesis", "the plumbing became drag and drop", thing + 4)
    lov = fp("thesis", "at lovingly i watched this myself", drag + 8)
    eighty = fp("thesis", "i automated about eighty percent", lov + 8)
    hours = fp("thesis", "the hours that came back", eighty + 6)
    small = fp("thesis", "built small this is three or four", hours + 6)
    serious = fp("thesis", "built serious", small + 8)
    moat = fp("thesis", "the unglamour is the moat", serious + 6)
    because = fp("thesis", "because the people who could", moat + 3)
    money = fp("thesis", "so does the money actually show up", t1 - 4)
    # thesis-01: 4 reveals so nothing dead-holds across the ~27s open
    screens.append(screen(id="thesis-01", section="thesis", layout="sheet",
        heading="The thesis", start=t0, end=thing,
        reveals=[reveal(1, t0, companies, "The boring-automation agency"),
                 reveal(1, companies, crm, "Tools that were never built to talk"),
                 reveal(1, crm, plumb, "CRM ✗ invoicing · form ✗ inbox · sheet ✗ Slack"),
                 reveal(1, plumb, thing, "You build the plumbing, charge a retainer", tags=["process"])],
        sfx=[{"cue": "tick", "at": t0}]))
    screens.append(screen(id="thesis-02", section="thesis", layout="schematic",
        heading="The thesis", start=thing, end=lov,
        reveals=[reveal(2, thing, drag, "Why one person can do this now"),
                 reveal(2, drag, lov, "The plumbing became drag-and-drop",
                        "n8n · Make — one operator, no integration team", tags=["tool"])],
        sfx=[{"cue": "tick", "at": thing}]))
    # single-stat moment → proof card (explicit 80%), ends before the elaboration
    screens.append(screen(id="thesis-03", section="thesis", layout="proof_card",
        heading="The thesis", start=lov, end=hours,
        reveals=[reveal(2, lov, hours, "Lovingly: florist busywork, automated", tags=["operator_pov"])],
        source="Operator experience — ~80% PM overhead reduction via AI",
        sfx=[{"cue": "hit", "at": lov}],
        custom={"proof": {"value": 80, "suffix": "%",
            "label": "Lovingly · PM busywork moved by hand, then automated",
            "source": "Operator experience — ~80% PM overhead reduction via AI"}}))
    # the elaboration that used to sit under the static proof card
    screens.append(screen(id="thesis-03b", section="thesis", layout="sheet",
        heading="The thesis", start=hours, end=small,
        reveals=[reveal(2, hours, small, "The hours were the point",
                        "Not the automation · the hours you get back", tags=["operator_pov"])],
        sfx=[{"cue": "tick", "at": hours}]))
    screens.append(screen(id="thesis-04", section="thesis", layout="sheet",
        heading="The thesis", start=small, end=moat,
        reveals=[reveal(3, small, serious, "Built small",
                        "3–4 retainers · a few hours/week · around a job"),
                 reveal(3, serious, moat, "Built serious",
                        "A niche automation studio with a waitlist", tags=["process"])],
        sfx=[{"cue": "tick", "at": small}]))
    # long pull-quote split: short impact frame + the reason
    screens.append(screen(id="thesis-05", section="thesis", layout="quote",
        heading="The thesis", start=moat, end=because,
        reveals=[reveal(4, moat, because, "The unglamour is the moat.", tags=["punchline"])],
        music={"intensity": "silence", "duck_db": 0}, sfx=[{"cue": "hit", "at": moat}],
        custom={"quote": "The unglamour is the moat.", "accentPhrase": "the moat", "ground": "navy"}))
    screens.append(screen(id="thesis-05b", section="thesis", layout="sheet",
        heading="The thesis", start=because, end=money,
        reveals=[reveal(4, because, money, "The people who could do this",
                        "mostly don't want to — that's the moat", tags=["process"])],
        sfx=[{"cue": "tick", "at": because}]))
    screens.append(screen(id="thesis-06", section="thesis", layout="schematic",
        heading="The thesis", start=money, end=t1,
        reveals=[reveal(4, money, t1, "So does the money actually show up?", tags=["question"])]))

    # ===================== EVIDENCE =====================
    e0, e1 = section_bounds("evidence")
    consistently = fp("evidence", "here's what they consistently show", e0 + 14)
    pattern = fp("evidence", "the pattern looks like this", consistently + 8)
    twocl = fp("evidence", "two solid retainer clients", pattern + 12)
    whypay = fp("evidence", "here's why a small business pays", twocl + 10)
    owner = fp("evidence", "an owner losing three hours", whypay + 8)
    high = fp("evidence", "now the high end", owner + 8)
    zapc = fp("evidence", "zapier the company that turned this into a product", high + 4)
    capital = fp("evidence", "that capital efficiency tells you", zapc + 12)
    newer = fp("evidence", "the newer proof", capital + 6)
    billionbiz = fp("evidence", "so the tool the solo operator runs on", newer + 16)
    zoom = fp("evidence", "zoom out further", billionbiz + 6)
    wide = fp("evidence", "the range is wide because", zoom + 10)
    need = fp("evidence", "what does the operator actually need", e1 - 4)
    # honest-gap caveat as a risk card, THEN what the numbers show as a sheet
    screens.append(screen(id="evidence-01", section="evidence", layout="risk_card",
        heading="The evidence", start=e0, end=consistently,
        reveals=[reveal(1, e0, consistently, "The honest gap", tags=["risk"])],
        sfx=[{"cue": "tick", "at": e0}],
        custom={"risk": {"title": "The low-end numbers are reported, not audited.",
            "body": "They come from agency how-to content, not audited books. Treat them as reported.",
            "bullets": ["No public audited solo case study yet",
                        "Setup fee + a monthly retainer is the shape"]}}))
    screens.append(screen(id="evidence-01b", section="evidence", layout="schematic",
        heading="The evidence", start=consistently, end=pattern,
        reveals=[reveal(1, consistently, pattern, "What they consistently show",
                        "A handful of clients replaces a salary", tags=["number"])],
        source="Agency how-to content — reported, unaudited"))
    # build + retainer economics → sheet (text lines, not a chart), 2 reveals
    screens.append(screen(id="evidence-02", section="evidence", layout="sheet",
        heading="The evidence", start=pattern, end=whypay,
        reveals=[reveal(2, pattern, twocl, "The pricing pattern",
                        "Build: $1,500–5K simple · $6–15K complex · then $500–5,000/mo retainer"),
                 reveal(2, twocl, whypay, "Two clients ≈ $7–12K/mo combined",
                        "Reportedly covers a solo founder's income", tags=["number"])],
        source="Agency pricing guides — reported, unaudited", sfx=[{"cue": "tick", "at": pattern}]))
    # why they pay → sheet, split into the alternative + the owner's own math
    screens.append(screen(id="evidence-03", section="evidence", layout="schematic",
        heading="The evidence", start=whypay, end=owner,
        reveals=[reveal(3, whypay, owner, "Why pay for something invisible?",
                        "The alternative: a person by hand · or it just doesn't happen")],
        source="Illustrative — the owner's own math", sfx=[{"cue": "tick", "at": whypay}]))
    screens.append(screen(id="evidence-03b", section="evidence", layout="sheet",
        heading="The evidence", start=owner, end=high,
        reveals=[reveal(3, owner, high, "3 hours/day of copy-paste",
                        "→ a few hundred a month to make it vanish · that's the whole pitch",
                        tags=["number"])]))
    # Zapier capital efficiency → proof (single stat), THEN the margin read
    screens.append(screen(id="evidence-04", section="evidence", layout="proof_card",
        heading="The evidence", start=high, end=capital,
        reveals=[reveal(4, high, capital, "Zapier revenue", tags=["number"])],
        source="getLatka / Sacra — reported", sfx=[{"cue": "hit", "at": high}],
        custom={"proof": {"value": 310000000, "compactCurrency": True,
            "label": "Zapier revenue · on only ~$1.5M raised",
            "source": "getLatka / Sacra — reported", "estimate": True}}))
    screens.append(screen(id="evidence-04b", section="evidence", layout="sheet",
        heading="The evidence", start=capital, end=newer,
        reveals=[reveal(4, capital, newer, "~$1.5M raised",
                        "The margins on connecting apps are extraordinary", tags=["number"])],
        source="getLatka / Sacra — reported"))
    # n8n → proof (single stat)
    screens.append(screen(id="evidence-05", section="evidence", layout="proof_card",
        heading="The evidence", start=newer, end=billionbiz,
        reveals=[reveal(5, newer, billionbiz, "n8n valuation", tags=["number"])],
        source="Ventureburn / TechCrunch — verified", sfx=[{"cue": "hit", "at": newer}],
        custom={"proof": {"value": 2500000000, "compactCurrency": True,
            "label": "n8n Series C valuation · 3,000 enterprise customers",
            "source": "Ventureburn / TechCrunch — verified"}}))
    screens.append(screen(id="evidence-06", section="evidence", layout="quote",
        heading="The evidence", start=billionbiz, end=zoom,
        reveals=[reveal(5, billionbiz, zoom, "The tool you run on is itself a billion-dollar business.",
                        tags=["punchline"])],
        music={"intensity": "silence", "duck_db": 0}, sfx=[{"cue": "hit", "at": billionbiz}],
        custom={"quote": "The tool the operator runs on is itself a billion-dollar business.",
                "accentPhrase": "billion-dollar business", "ground": "navy"}))
    # market size → proof (single stat), THEN the "why the range is wide" read
    screens.append(screen(id="evidence-07", section="evidence", layout="proof_card",
        heading="The evidence", start=zoom, end=wide,
        reveals=[reveal(6, zoom, wide, "The category", tags=["number"])],
        source="Precedence / Fortune Business Insights — estimate",
        music={"intensity": "build", "duck_db": -10}, sfx=[{"cue": "hit", "at": zoom}],
        custom={"proof": {"value": 23000000000, "compactCurrency": True,
            "label": "iPaaS market, 2026 · est. $14–23B, growing 20%+/yr", "estimate": True,
            "source": "Precedence / Fortune Business Insights — estimate"}}))
    screens.append(screen(id="evidence-07b", section="evidence", layout="sheet",
        heading="The evidence", start=wide, end=need,
        reveals=[reveal(6, wide, need, "The range is wide",
                        "Nobody agrees where it ends · the direction is not in question")]))
    screens.append(screen(id="evidence-08", section="evidence", layout="schematic",
        heading="The evidence", start=need, end=e1,
        reveals=[reveal(6, need, e1, "So what does the operator actually need to build this?",
                        tags=["question"])]))

    # ===================== STACK =====================
    s0, s1 = section_bounds("stack")
    engine = fp("stack", "it's n8n or make", s0 + 3)
    own = fp("stack", "because you own the workflows", engine + 10)
    parts = fp("stack", "the parts you're connecting", s0 + 22)
    interesting = fp("stack", "here's where it gets interesting", parts + 10)
    claude = fp("stack", "a claude or gpt call", interesting + 4)
    node = fp("stack", "that one node", claude + 10)
    allin = fp("stack", "all in the operator's own tools", claude + 18)
    fiveb = fp("stack", "same margin zapier scaled", allin + 8)
    retainer = fp("stack", "and the retainer", fiveb + 6)
    breaks = fp("stack", "a workflow quietly breaks", retainer + 8)
    commoditize = fp("stack", "the reason this work never", breaks + 5)
    land = fp("stack", "how do you land the first client", s1 - 3)
    # engine split: pricing, then the ownership point
    screens.append(screen(id="stack-01", section="stack", layout="sheet",
        heading="The stack", start=s0, end=own,
        reveals=[reveal(1, s0, engine, "The engine: n8n or Make", tags=["tool"]),
                 reveal(1, engine, own, "Self-host free · cloud $20–50 · Make from $9",
                        tags=["tool"])],
        source="public pricing — n8n cloud, Make plans", sfx=[{"cue": "tick", "at": s0}]))
    screens.append(screen(id="stack-01b", section="stack", layout="sheet",
        heading="The stack", start=own, end=parts,
        reveals=[reveal(1, own, parts, "You own the workflows outright",
                        "why most agencies standardize on n8n", tags=["tool"])],
        source="public pricing — n8n cloud"))
    screens.append(screen(id="stack-02", section="stack", layout="schematic",
        heading="The stack", start=parts, end=interesting,
        reveals=[reveal(2, parts, interesting, "The parts: whatever the client already uses",
                        "HubSpot · invoicing · forms · sheets · Slack — you're the wiring", tags=["tool"])]))
    # AI node — screen_rec, split into "the AI step" + "what the node does"
    screens.append(screen(id="stack-03", section="stack", layout="screen_rec",
        heading="The stack", start=interesting, end=claude,
        reveals=[reveal(3, interesting, claude, "Here's where it gets interesting",
                        "the AI step in the middle", tags=["tool"])],
        source="Channel's own stack — the AI parsing node", sfx=[{"cue": "tick", "at": interesting}]))
    screens.append(screen(id="stack-03b", section="stack", layout="screen_rec",
        heading="The stack", start=claude, end=allin,
        reveals=[reveal(3, claude, node, "A Claude/GPT node reads a messy email",
                        "pulls the order out · drops clean data into the next system",
                        tags=["tool"]),
                 reveal(3, node, allin, "That one node used to need a human",
                        "it's what turns simple automation into a real retainer", tags=["tool"])],
        source="Channel's own stack — the AI parsing node", sfx=[{"cue": "tick", "at": claude}]))
    # operator cost → proof (< $100/mo), THEN the margin point
    screens.append(screen(id="stack-04", section="stack", layout="proof_card",
        heading="The stack", start=allin, end=fiveb,
        reveals=[reveal(4, allin, fiveb, "Operator tool cost", tags=["number"])],
        source="public pricing — operator stack under $100/mo",
        music={"intensity": "build", "duck_db": -10}, sfx=[{"cue": "hit", "at": allin}],
        custom={"proof": {"value": 100, "prefix": "<$", "suffix": "/mo",
            "label": "Operator tool cost · the client pays for their own software",
            "source": "public pricing — stack under $100/mo"}}))
    screens.append(screen(id="stack-04b", section="stack", layout="sheet",
        heading="The stack", start=fiveb, end=retainer,
        reveals=[reveal(4, fiveb, retainer, "Same margin Zapier scaled to $5B",
                        "your cost is the platform + your time — that's where the margin is",
                        tags=["number"])],
        source="Zapier ~$5B valuation — reported"))
    # retainer risk → risk card, THEN the recurring-revenue point
    screens.append(screen(id="stack-05", section="stack", layout="risk_card",
        heading="The stack", start=retainer, end=breaks,
        reveals=[reveal(5, retainer, breaks, "The retainer buys upkeep, not the build", tags=["process"])],
        sfx=[{"cue": "hit", "at": retainer}],
        custom={"risk": {"title": "The retainer is for upkeep, not the build.",
            "body": "An app changes its login. A form adds a field. A workflow breaks at 2am.",
            "bullets": ["An app changes its login", "A form adds a field", "A workflow breaks at 2am"]}}))
    screens.append(screen(id="stack-05b", section="stack", layout="sheet",
        heading="The stack", start=breaks, end=land,
        reveals=[reveal(5, breaks, commoditize, "That upkeep is the recurring revenue",
                        "the 2am break is the reason the retainer exists", tags=["process"]),
                 reveal(5, commoditize, land, "And why the work never fully commoditizes",
                        tags=["process"])]))
    screens.append(screen(id="stack-06", section="stack", layout="schematic",
        heading="The stack", start=land, end=s1,
        reveals=[reveal(5, land, s1, "So how do you land the first client?", tags=["question"])]))

    # ===================== PLAYBOOK =====================
    p0, p1 = section_bounds("playbook")
    week1 = fp("playbook", "week one pick one industry", p0 + 3)
    realestate = fp("playbook", "real estate lead routing", week1 + 6)
    build1 = fp("playbook", "then you build one workflow", realestate + 12)
    salespitch = fp("playbook", "the working automation is the sales pitch", build1 + 8)
    renovation = fp("playbook", "same way a finished renovation", salespitch + 3)
    price = fp("playbook", "price it as a build fee", renovation + 6)
    dialtone = fp("playbook", "i tell people it's a dial tone", price + 10)
    neverthink = fp("playbook", "you never think about it", dialtone + 3)
    notbuild = fp("playbook", "the monthly isn't for the build", dialtone + 8)
    month1 = fp("playbook", "month one land your first two or three", notbuild + 6)
    casestudies = fp("playbook", "become the case studies", month1 + 6)
    wordmouth = fp("playbook", "boring work spreads by word of mouth", month1 + 10)
    month2 = fp("playbook", "month two is delivery discipline", wordmouth + 8)
    renews = fp("playbook", "that note is what renews the retainer", p1 - 6)
    pay = fp("playbook", "what does this actually pay", p1 - 3)
    # week 1 split: the rule, then the menu (schematic breaks the sheet run)
    screens.append(screen(id="playbook-01", section="playbook", layout="sheet",
        heading="The playbook", start=p0, end=realestate,
        reveals=[reveal(1, p0, realestate, "Week 1: pick ONE industry + one painful workflow",
                        "ideally something you already understand", tags=["process"])],
        sfx=[{"cue": "tick", "at": p0}]))
    screens.append(screen(id="playbook-01b", section="playbook", layout="schematic",
        heading="The playbook", start=realestate, end=build1,
        reveals=[reveal(1, realestate, build1, "The menu",
                        "Real estate routing · clinic intake · e-commerce sync — narrow beats broad",
                        tags=["process"])]))
    screens.append(screen(id="playbook-02", section="playbook", layout="screen_rec",
        heading="The playbook", start=build1, end=salespitch,
        reveals=[reveal(2, build1, salespitch, "Build one workflow",
                        "for a REAL business · automate an actual manual hand-off · show before/after",
                        tags=["process"])],
        sfx=[{"cue": "tick", "at": build1}]))
    # pull-quote split: short impact + the analogy
    screens.append(screen(id="playbook-03", section="playbook", layout="quote",
        heading="The playbook", start=salespitch, end=renovation,
        reveals=[reveal(2, salespitch, renovation, "The working automation is the sales pitch.", tags=["punchline"])],
        music={"intensity": "silence", "duck_db": 0}, sfx=[{"cue": "hit", "at": salespitch}],
        custom={"quote": "The working automation is the sales pitch.",
                "accentPhrase": "the sales pitch", "ground": "navy"}))
    screens.append(screen(id="playbook-03b", section="playbook", layout="sheet",
        heading="The playbook", start=renovation, end=price,
        reveals=[reveal(2, renovation, price, "Like a finished renovation",
                        "it sells the next job better than any brochure", tags=["process"])]))
    # pricing → sheet (text, not a chart)
    screens.append(screen(id="playbook-04", section="playbook", layout="sheet",
        heading="The playbook", start=price, end=dialtone,
        reveals=[reveal(3, price, dialtone, "Pricing: build fee + flat monthly retainer",
                        "Never hourly — hourly punishes you for getting faster", tags=["process"])],
        source="Playbook — build fee + retainer pricing"))
    # pull-quote split: short impact + why the monthly exists
    screens.append(screen(id="playbook-05", section="playbook", layout="quote",
        heading="The playbook", start=dialtone, end=neverthink,
        reveals=[reveal(3, dialtone, neverthink, "It's a dial tone.", tags=["punchline", "operator_pov"])],
        music={"intensity": "silence", "duck_db": 0}, sfx=[{"cue": "hit", "at": dialtone}],
        custom={"quote": "I tell people it's a dial tone.",
                "accentPhrase": "a dial tone", "ground": "navy"}))
    screens.append(screen(id="playbook-05b", section="playbook", layout="sheet",
        heading="The playbook", start=neverthink, end=month1,
        reveals=[reveal(3, neverthink, notbuild, "You never think about it until it stops",
                        "and the whole value is that it doesn't stop"),
                 reveal(3, notbuild, month1, "The monthly isn't for the build",
                        "it's so the build is still standing when an app changes its login",
                        tags=["process"])]))
    # month 1 → sheet, 2 reveals
    screens.append(screen(id="playbook-06", section="playbook", layout="sheet",
        heading="The playbook", start=month1, end=month2,
        reveals=[reveal(4, month1, casestudies, "Month 1: 2–3 clients from your network",
                        "people who already know you run this", tags=["process"]),
                 reveal(4, casestudies, wordmouth, "Hours saved, written down",
                        "= the case study that gets you the next five", tags=["process"]),
                 reveal(4, wordmouth, month2, "Boring work spreads by word of mouth",
                        "the result is concrete — point at the hours they got back")],
        sfx=[{"cue": "tick", "at": month1}]))
    # month 2 → schematic (delivery-discipline process; breaks the sheet run)
    screens.append(screen(id="playbook-07", section="playbook", layout="schematic",
        heading="The playbook", start=month2, end=pay,
        reveals=[reveal(5, month2, renews, "Month 2: delivery discipline",
                        "Document workflows · set breakage alerts · monthly what-ran note", tags=["process"]),
                 reveal(5, renews, pay, "That note renews the retainer")],
        source="Playbook — delivery discipline", sfx=[{"cue": "tick", "at": month2}]))
    screens.append(screen(id="playbook-08", section="playbook", layout="schematic",
        heading="The playbook", start=pay, end=p1,
        reveals=[reveal(5, pay, p1, "So what does this actually pay?", tags=["question"])]))

    # ===================== ECONOMICS =====================
    ec0, ec1 = section_bounds("economics")
    realistic = fp("economics", "realistic year one for a solo operator", ec0 + 14)
    estimate = fp("economics", "that's an estimate reasoned", realistic + 8)
    fail1 = fp("economics", "first failure mode", estimate + 6)
    own2 = fp("economics", "own your workflows where you can", fail1 + 10)
    fail2 = fp("economics", "second one commoditization", own2 + 6)
    payroll = fp("economics", "payroll reconciliation", fail2 + 12)
    fail3 = fp("economics", "third one is the one that haunts", payroll + 8)
    openq = fp("economics", "so here's the open question", ec1 - 8)
    building = fp("economics", "which one are you building", ec1 - 3)
    screens.append(screen(id="economics-01", section="economics", layout="sheet",
        heading="The economics", start=ec0, end=realistic,
        reveals=[reveal(1, ec0, realistic, "The blueprint — free, linked below",
                        "Niche picker · first workflow · retainer pricing", tags=["cta"])],
        sfx=[{"cue": "tick", "at": ec0}]))
    # year-one range → proof (single stat), THEN the caveat
    screens.append(screen(id="economics-02", section="economics", layout="proof_card",
        heading="The economics", start=realistic, end=estimate,
        reveals=[reveal(2, realistic, estimate, "Realistic year one", tags=["number"])],
        source="Estimate — reasoned from reported pricing bands",
        music={"intensity": "build", "duck_db": -10}, sfx=[{"cue": "hit", "at": realistic}],
        custom={"proof": {"value": 6, "prefix": "$", "suffix": "K/mo",
            "label": "Realistic year one · $2–6K/mo from 3–6 clients", "estimate": True,
            "source": "Estimate — reasoned from reported pricing bands, unaudited"}}))
    screens.append(screen(id="economics-02b", section="economics", layout="sheet",
        heading="The economics", start=estimate, end=fail1,
        reveals=[reveal(2, estimate, fail1, "3–6 clients, past a slow first month",
                        "an estimate, not audited · and it assumes you can find the clients",
                        tags=["number"])]))
    # failure 1 → risk, THEN the mitigation
    screens.append(screen(id="economics-03", section="economics", layout="risk_card",
        heading="The economics", start=fail1, end=own2,
        reveals=[reveal(3, fail1, own2, "Failure 1: platform risk", tags=["risk"])],
        sfx=[{"cue": "hit", "at": fail1}],
        custom={"risk": {"title": "You're building on someone else's tool.",
            "body": "n8n or Make can change pricing, limits, or terms; a connected app can break its integration overnight.",
            "bullets": ["n8n or Make can change pricing or limits",
                        "Terms can shift under you",
                        "A connected app can break its integration overnight"]}}))
    screens.append(screen(id="economics-03b", section="economics", layout="sheet",
        heading="The economics", start=own2, end=fail2,
        reveals=[reveal(3, own2, fail2, "Own your workflows where you can",
                        "never let one client's whole system hang on a single fragile link",
                        tags=["process"])]))
    # failure 2 → risk, THEN the durable-work examples
    screens.append(screen(id="economics-04", section="economics", layout="risk_card",
        heading="The economics", start=fail2, end=payroll,
        reveals=[reveal(4, fail2, payroll, "Failure 2: commoditization", tags=["risk"])],
        sfx=[{"cue": "hit", "at": fail2}],
        custom={"risk": {"title": "The simplest automations will be DIY'd.",
            "body": "The durable work is judgment-heavy, not two-step. The messy integrations stay yours.",
            "bullets": ["Simple two-step flows get commoditized", "Messy, judgment-heavy work stays yours"]}}))
    screens.append(screen(id="economics-04b", section="economics", layout="sheet",
        heading="The economics", start=payroll, end=fail3,
        reveals=[reveal(4, payroll, fail3, "Payroll · reconciliation · order → fulfillment",
                        "nobody wakes up wanting to do those — that's exactly why they're durable",
                        tags=["process"])]))
    # failure 3 → risk card (keeps the three failures consistent, breaks the sheet run)
    screens.append(screen(id="economics-05", section="economics", layout="risk_card",
        heading="The economics", start=fail3, end=openq,
        reveals=[reveal(5, fail3, openq, "Failure 3: distribution", tags=["risk"])],
        sfx=[{"cue": "hit", "at": fail3}],
        custom={"risk": {"title": "The tools got easy. Finding clients did not.",
            "body": "Your pipeline still comes from trust and word of mouth.",
            "bullets": ["Trust and word of mouth still drive the pipeline", "No workflow automates that"]}}))
    screens.append(screen(id="economics-06a", section="economics", layout="sheet",
        heading="The economics", start=openq, end=building,
        reveals=[reveal(5, openq, building, "The open question",
                        "stay a solo retainer practice · or productize the same 5 workflows and sell them 100×",
                        tags=["question"])]))
    # short impact frame to close the section
    screens.append(screen(id="economics-06", section="economics", layout="quote",
        heading="The economics", start=building, end=ec1,
        reveals=[reveal(5, building, ec1, "Which one are you building?", tags=["punchline", "question"])],
        music={"intensity": "silence", "duck_db": 0}, sfx=[{"cue": "hit", "at": building}],
        custom={"quote": "Which one are you building?",
                "accentPhrase": "you", "ground": "paper"}))

    # ===================== CTA =====================
    c0, c1 = section_bounds("cta")
    subscribe = fp("cta", "subscribe if you want", c0 + 10)
    screens.append(screen(id="cta-01", section="cta", layout="cta",
        heading="The Operator Blueprint", start=c0, end=c1,
        reveals=[reveal(1, c0, subscribe, "№ 003 — The Boring-Automation Agency",
                        "Niche picker · first workflow · retainer pricing sheet — free, linked below",
                        tags=["cta"]),
                 reveal(1, subscribe, c1, "Subscribe for the next teardown",
                        "sources included · honest ranges included", tags=["cta"])]))

    return {"slug": "boring-automation-agency", "total_seconds": TOTAL_SECONDS, "screens": screens}


if __name__ == "__main__":
    sb = build()
    STORYBOARD.write_text(json.dumps(sb, indent=2))
    quotes = sum(1 for s in sb["screens"] if s["layout"] == "quote")
    proofs = sum(1 for s in sb["screens"] if s["layout"] == "proof_card")
    charts = sum(1 for s in sb["screens"] if s["layout"] == "chart")
    print(f"✓ storyboard → {STORYBOARD}")
    print(f"  {len(sb['screens'])} screens · {quotes} quotes · {proofs} proof cards · {charts} charts")
    print(f"  anchor misses: {_WARN if _WARN else 'none'}")
