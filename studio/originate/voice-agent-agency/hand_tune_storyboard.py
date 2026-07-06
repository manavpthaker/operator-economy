"""
Hand-tuned storyboard for №002 (voice-agent-agency).

Follows the №001 pattern (originate/ai-implementation-consulting/
hand_tune_storyboard.py): phrase-anchored screens over the performed VO,
multi-reveal composites instead of one static screen per beat, quote
cards on impact lines, sources on every money screen.

Voice-agnostic: reads vo/words.json + vo/timeline.json and looks up each
impact phrase in the current VO. Re-run after any VO regeneration, then
pace_storyboard.py.

Run:
    python originate/voice-agent-agency/hand_tune_storyboard.py

Emits:
    originate/voice-agent-agency/storyboard.json
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

_SECTION_TIMING: dict[str, tuple[float, float]] = {
    s["section"]: (s["start"], s["start"] + s["duration"])
    for s in TIMELINE["sections"]
}
TOTAL_SECONDS: float = TIMELINE["total_seconds"]


def _norm(w: str) -> str:
    stripped = re.sub(r"[^\w']", "", w)
    return stripped.strip("'").lower()


def find_phrase(section: str, phrase: str) -> tuple[float, float]:
    tokens = [_norm(t) for t in phrase.split() if _norm(t)]
    if not tokens:
        raise ValueError(f"empty phrase {phrase!r}")
    ws = _SECTION_WORDS.get(section, [])
    normed = [_norm(w["word"]) for w in ws]
    for i in range(len(normed) - len(tokens) + 1):
        if normed[i : i + len(tokens)] == tokens:
            return ws[i]["start"], ws[i + len(tokens) - 1]["end"]
    raise ValueError(f"phrase {phrase!r} not found in section {section}")


def section_bounds(section: str) -> tuple[float, float]:
    return _SECTION_TIMING[section]


def _pad_end(end: float, max_end: float) -> float:
    return min(end + 0.3, max_end)


def screen(**kw):
    section = kw["section"]
    kw.setdefault("audio", f"vo/{section}.mp3")
    kw.setdefault("figure", None)
    kw.setdefault("source", None)
    kw.setdefault("music", {"intensity": "calm", "duck_db": -16})
    kw.setdefault("sfx", [])
    kw.setdefault("custom", None)
    return kw


def reveal(beat: int, at: float, end: float, title: str, body: str = "", tags: list[str] | None = None) -> dict:
    return {
        "beat": beat,
        "at": at,
        "end": end,
        "title": title,
        "body": body,
        "tags": tags or ["claim"],
        "word_anchor": {"start": at, "end": end},
    }


def build() -> dict:
    screens: list[dict] = []

    # ==================================================================
    # HOOK — brand open → title card (carries the music bridge) → the
    # 38/62 gap screen (arrange_bed keys the beat drop to this first
    # gap-layout screen) → the money contrast.
    # ==================================================================
    hook_start, hook_end = section_bounds("hook")
    week_s, _ = find_phrase("hook", "this week")
    study_s, _ = find_phrase("hook", "one study found")
    sixty2_s, sixty2_e = find_phrase("hook", "the other 62 percent")
    solo_s, _ = find_phrase("hook", "solo operators fix that")
    eleven_s, eleven_e = find_phrase("hook", "just raised at an 11 billion")

    screens.append(screen(
        id="hook-00a",
        section="hook",
        layout="chapter_reset",
        heading="The Operator Economy",
        start=hook_start, end=week_s,
        reveals=[reveal(0, hook_start, week_s, "The Operator Economy", tags=["claim"])],
        custom={"kicker": "BUILD · OWN · OPERATE"},
        sfx=[{"cue": "tick", "at": hook_start}],
    ))
    screens.append(screen(
        id="hook-00b",
        section="hook",
        layout="sheet",
        heading="Operator Blueprint",
        start=week_s, end=study_s,
        reveals=[reveal(0, week_s, study_s, "placeholder", tags=["claim"])],
        custom={"titleCard": {
            "overline": "Operator Blueprint · № 002",
            "title": "The Phone Call Businesses Never Answer",
            "thesis": "AI phone agents: the missed-call business, at every scale.",
        }},
        sfx=[{"cue": "tick", "at": week_s}],
    ))
    # hook-01 gap — the 38/62 stat; the beat drops here.
    screens.append(screen(
        id="hook-01",
        section="hook",
        layout="gap",
        heading="The gap",
        start=study_s, end=solo_s,
        reveals=[
            reveal(1, study_s, sixty2_s, "38% answered by a real person",
                   tags=["claim", "number"]),
            reveal(1, sixty2_s, solo_s, "62% — voicemail, or nowhere",
                   tags=["claim", "number"]),
        ],
        figure={"text": "38% answered / 62% missed",
                "source": "411 Locals 2024 study — one study, vendor-recycled"},
        source="411 Locals 2024 study — one study, vendor-recycled",
        music={"intensity": "build", "duck_db": -8},
        sfx=[{"cue": "hit", "at": study_s}],
    ))
    # hook-02 chart — solo price band vs the $11B platform underneath
    screens.append(screen(
        id="hook-02",
        section="hook",
        layout="chart",
        heading="The gap",
        start=solo_s, end=hook_end,
        reveals=[
            reveal(1, solo_s, eleven_s, "$300–1,000/mo per client",
                   tags=["claim", "number"]),
            reveal(1, eleven_s, hook_end, "The infrastructure: $11B valuation",
                   tags=["claim", "number"]),
        ],
        figure={"text": "$300–1,000/mo vs $11B",
                "source": "TechCrunch, Feb 2026; vendor pricing guides"},
        source="TechCrunch, Feb 2026; vendor pricing guides",
        music={"intensity": "build", "duck_db": -8},
        sfx=[{"cue": "hit", "at": eleven_s}],
    ))

    # ==================================================================
    # THESIS — install sheet → missed-call broll → shift proof →
    # Yucatan POV → THE META REVEAL (quote pair) → lean/serious sheet.
    # ==================================================================
    th_start, th_end = section_bounds("thesis")
    think_s, _ = find_phrase("thesis", "think about it")
    changed_s, _ = find_phrase("thesis", "here's the thing that changed")
    yuca_s, _ = find_phrase("thesis", "i ran four properties")
    proof_s, _ = find_phrase("thesis", "you're actually listening to the proof")
    aivoice_s, aivoice_e = find_phrase("thesis", "that's an ai voice")
    notice_s, notice_e = find_phrase("thesis", "if you didn't notice")
    didnotice_s, _ = find_phrase("thesis", "if you did notice")
    lean_s, _ = find_phrase("thesis", "so built lean")
    serious_s, _ = find_phrase("thesis", "built seriously")

    screens.append(screen(
        id="thesis-01",
        section="thesis",
        layout="sheet",
        heading="The thesis",
        start=th_start, end=think_s,
        reveals=[reveal(1, th_start, think_s, "The install",
                        "AI receptionist · Plumbers · Dentists · Salons · Florists",
                        tags=["claim", "process"])],
        sfx=[{"cue": "tick", "at": th_start}],
    ))
    screens.append(screen(
        id="thesis-02",
        section="thesis",
        layout="broll",
        heading="The thesis",
        start=think_s, end=changed_s,
        reveals=[
            reveal(1, think_s, (think_s + changed_s) / 2, "Nobody's picking up",
                   "Rooftop technician · Dental chair · Flower shop counter", tags=["claim"]),
            reveal(1, (think_s + changed_s) / 2, changed_s, "The caller doesn't wait",
                   tags=["claim"]),
        ],
    ))
    screens.append(screen(
        id="thesis-03",
        section="thesis",
        layout="proof_card",
        heading="The thesis",
        start=changed_s, end=yuca_s,
        reveals=[
            reveal(2, changed_s, (changed_s + yuca_s) / 2, "Good enough + cheap enough",
                   "The last two years", tags=["claim"]),
            reveal(2, (changed_s + yuca_s) / 2, yuca_s, "One person, end to end",
                   "No call center · No dev team", tags=["claim", "operator_pov"]),
        ],
        source="Research brief — capability shift, 2024–2026",
        sfx=[{"cue": "tick", "at": changed_s}],
    ))
    screens.append(screen(
        id="thesis-04",
        section="thesis",
        layout="broll",
        heading="The thesis",
        start=yuca_s, end=proof_s,
        reveals=[
            reveal(2, yuca_s, (yuca_s + proof_s) / 2, "Four properties, Yucatán",
                   "Checkout rush · Phone under the queue", tags=["operator_pov"]),
            reveal(2, (yuca_s + proof_s) / 2, proof_s, "Bookings we never saw",
                   "A booking site · Or the hotel down the road", tags=["operator_pov"]),
        ],
        source="Operator experience — Coqui Coqui, 4 properties",
    ))
    # THE META REVEAL — the episode's biggest impact moment.
    screens.append(screen(
        id="thesis-05",
        section="thesis",
        layout="quote",
        heading="The thesis",
        start=proof_s, end=_pad_end(aivoice_e, th_end),
        reveals=[reveal(3, aivoice_s, aivoice_e, "This voice? An AI voice.",
                        tags=["punchline"])],
        music={"intensity": "silence", "duck_db": 0},
        sfx=[{"cue": "hit", "at": aivoice_s}],
        custom={"quote": "This voice? That's an AI voice.",
                "accentPhrase": "AI voice",
                "ground": "navy"},
    ))
    screens.append(screen(
        id="thesis-06",
        section="thesis",
        layout="quote",
        heading="The thesis",
        start=_pad_end(aivoice_e, th_end), end=_pad_end(notice_e, th_end),
        reveals=[reveal(3, notice_s, notice_e, "If you didn't notice, that's the point.",
                        tags=["punchline"])],
        music={"intensity": "silence", "duck_db": 0},
        sfx=[{"cue": "hit", "at": notice_s}],
        custom={"quote": "If you didn't notice... that's the point.",
                "accentPhrase": "that's the point",
                "ground": "navy"},
    ))
    screens.append(screen(
        id="thesis-07",
        section="thesis",
        layout="proof_card",
        heading="The thesis",
        start=_pad_end(notice_e, th_end), end=lean_s,
        reveals=[reveal(3, didnotice_s, lean_s, "How good 'good enough' is",
                        "And where the seams still show", tags=["claim"])],
        source="Direct demonstration — this episode's own VO",
    ))
    screens.append(screen(
        id="thesis-08",
        section="thesis",
        layout="sheet",
        heading="The thesis",
        start=lean_s, end=th_end,
        reveals=[
            reveal(4, lean_s, serious_s, "Built lean",
                   "Laptop · Phone number · 3 subscriptions <$150/mo", tags=["number"]),
            reveal(4, serious_s, th_end, "Built seriously",
                   "5–8 clients on retainer · Documented before/after · A demo that closes",
                   tags=["number", "process"]),
        ],
        source="Public tool pricing — stack totals",
        sfx=[{"cue": "tick", "at": lean_s}],
    ))

    # ==================================================================
    # EVIDENCE — honest gap → reseller economics → plumber math →
    # behavior chart → high-end run (ElevenLabs, Vapi/Retell, market)
    # → installer schematic → "that installer is you" quote.
    # ==================================================================
    ev_start, ev_end = section_bounds("evidence")
    advert_s, _ = find_phrase("evidence", "here's what the platforms actually advertise")
    pitch_s, _ = find_phrase("evidence", "and the pitch writes itself")
    behav_s, _ = find_phrase("evidence", "the behavioral numbers explain")
    high_s, _ = find_phrase("evidence", "now the high end")
    el_s, _ = find_phrase("evidence", "elevenlabs closed a 500 million round")
    vapi_s, _ = find_phrase("evidence", "vapi the infrastructure")
    market_s, _ = find_phrase("evidence", "and one analyst estimate")
    read_s, _ = find_phrase("evidence", "so here's the read")
    installer_s, installer_e = find_phrase("evidence", "that installer is you")
    margin_s, _ = find_phrase("evidence", "that's a 50 to 70 percent margin")
    setup_s, _ = find_phrase("evidence", "setup fees run")
    plumber_s, _ = find_phrase("evidence", "a plumber missing 15 calls")
    rounding_s, _ = find_phrase("evidence", "a 500-a-month answering service")

    screens.append(screen(
        id="evidence-01",
        section="evidence",
        layout="risk_card",
        heading="The evidence",
        start=ev_start, end=advert_s,
        reveals=[reveal(1, ev_start, advert_s, "The honest gap", tags=["risk"])],
        sfx=[{"cue": "tick", "at": ev_start}],
        custom={"risk": {
            "title": "No verified solo case study exists.",
            "body": "The low-end evidence is thinner than other AI-agency niches — and most of it comes from the platforms marketing to would-be resellers.",
            "bullets": [
                "Treat reseller income claims as marketing artifacts",
                "The absence is also why the space is less crowded",
            ],
        }},
    ))
    screens.append(screen(
        id="evidence-02",
        section="evidence",
        layout="chart",
        heading="The evidence",
        start=advert_s, end=pitch_s,
        reveals=[
            reveal(2, advert_s, margin_s, "$297–997/mo vs $99–299 platform fees",
                   tags=["claim", "number"]),
            reveal(2, margin_s, setup_s, "50–70% margin — on paper",
                   tags=["claim", "number"]),
            reveal(2, setup_s, pitch_s, "Setup: $500–2,000",
                   "Marketing numbers — unverified", tags=["claim", "number"]),
        ],
        figure={"text": "Reseller pricing vs platform fees",
                "source": "Trillet pricing guide — vendor content, unverified"},
        source="Trillet pricing guide — vendor content, unverified",
        music={"intensity": "build", "duck_db": -10},
        sfx=[{"cue": "hit", "at": advert_s}],
    ))
    screens.append(screen(
        id="evidence-03",
        section="evidence",
        layout="chart",
        heading="The evidence",
        start=pitch_s, end=behav_s,
        reveals=[
            reveal(3, plumber_s, rounding_s, "15 calls/wk × $350 = six figures/yr",
                   tags=["claim", "number"]),
            reveal(3, rounding_s, behav_s, "$500/mo against that is a rounding error",
                   tags=["claim", "number"]),
        ],
        figure={"text": "The plumber math",
                "source": "Illustrative arithmetic — not audited"},
        source="Illustrative arithmetic — not audited",
        music={"intensity": "build", "duck_db": -10},
    ))
    b85_s, _ = find_phrase("evidence", "about 85 percent of callers")
    b62_s, _ = find_phrase("evidence", "roughly 62 percent just call a competitor")
    b80_s, _ = find_phrase("evidence", "80 percent won't even leave")
    screens.append(screen(
        id="evidence-04",
        section="evidence",
        layout="chart",
        heading="The evidence",
        start=behav_s, end=high_s,
        reveals=[
            reveal(4, b85_s, b62_s, "85% never call back", tags=["claim", "number"]),
            reveal(4, b62_s, b80_s, "62% call a competitor", tags=["claim", "number"]),
            reveal(4, b80_s, high_s, "80% won't leave a message",
                   "Reported, not audited", tags=["claim", "number"]),
        ],
        figure={"text": "After the missed call: 85 / 62 / 80",
                "source": "411 Locals ecosystem stats — reported, unaudited"},
        source="411 Locals ecosystem stats — reported, unaudited",
        music={"intensity": "build", "duck_db": -10},
        sfx=[{"cue": "hit", "at": behav_s}],
    ))
    screens.append(screen(
        id="evidence-05",
        section="evidence",
        layout="chart",
        heading="The evidence",
        start=high_s, end=vapi_s,
        reveals=[
            reveal(5, el_s, vapi_s, "ElevenLabs: $500M round · $11B valuation",
                   "~$350M → ~$500M ARR in four months", tags=["claim", "number"]),
        ],
        figure={"text": "ElevenLabs ARR, Dec 2025 → Apr 2026",
                "source": "TechCrunch, Feb 4 2026; Sacra estimate"},
        source="TechCrunch, Feb 4 2026; Sacra estimate",
        music={"intensity": "build", "duck_db": -10},
        sfx=[{"cue": "hit", "at": high_s}],
    ))
    retell_s, _ = find_phrase("evidence", "retell ai launched only in 2024")
    screens.append(screen(
        id="evidence-06",
        section="evidence",
        layout="proof_card",
        heading="The evidence",
        start=vapi_s, end=market_s,
        reveals=[
            reveal(5, vapi_s, retell_s, "Vapi: $500M valuation",
                   "Amazon Ring chose it over 40 rivals", tags=["claim", "number"]),
            reveal(5, retell_s, market_s, "Retell: 50M+ AI calls/month",
                   "Launched 2024 — vendor-reported", tags=["claim", "number"]),
        ],
        source="TechCrunch, May 12 2026; Retell press — vendor-reported",
        sfx=[{"cue": "hit", "at": vapi_s}],
    ))
    screens.append(screen(
        id="evidence-07",
        section="evidence",
        layout="chart",
        heading="The evidence",
        start=market_s, end=read_s,
        reveals=[reveal(6, market_s, read_s, "Market: ~$2.5–3.5B, growing 30–40%/yr",
                        "Analyst estimate — directional", tags=["claim", "number"])],
        figure={"text": "AI voice agents market, 2025 → early 2030s",
                "source": "Grand View Research / Market.us — analyst estimate"},
        source="Grand View Research / Market.us — analyst estimate",
        music={"intensity": "build", "duck_db": -10},
    ))
    screens.append(screen(
        id="evidence-08",
        section="evidence",
        layout="schematic",
        heading="The evidence",
        start=read_s, end=installer_s,
        reveals=[reveal(6, read_s, installer_s, "The read",
                        "Platforms raise at software multiples → someone installs → the dentist's office",
                        tags=["claim"])],
    ))
    screens.append(screen(
        id="evidence-09",
        section="evidence",
        layout="quote",
        heading="The evidence",
        start=installer_s, end=ev_end,
        reveals=[reveal(6, installer_s, installer_e, "That installer is you.",
                        tags=["punchline"])],
        music={"intensity": "silence", "duck_db": 0},
        sfx=[{"cue": "hit", "at": installer_s}],
        custom={"quote": "That installer is you.",
                "accentPhrase": "you",
                "ground": "navy"},
    ))

    # ==================================================================
    # STACK — ElevenLabs callback → orchestration tools → cost-line
    # quote → plumbing (Twilio/n8n/Cal.com) → cost chart → delivery loop.
    # ==================================================================
    st_start, st_end = section_bounds("stack")
    sounds_s, _ = find_phrase("stack", "it sounds close to human")
    orch_s, _ = find_phrase("stack", "for call orchestration")
    bland_s, _ = find_phrase("stack", "bland's the alternative")
    ctrl_s, ctrl_e = find_phrase("stack", "you don't control this cost line")
    twilio_s, _ = find_phrase("stack", "twilio gives you the phone number")
    make_s, _ = find_phrase("stack", "make or n8n handles")
    allin_s, _ = find_phrase("stack", "all in before")
    loop_s, _ = find_phrase("stack", "the full delivery loop")
    retainer_s, _ = find_phrase("stack", "and the retainer")
    land_s, _ = find_phrase("stack", "so how do you actually land")

    screens.append(screen(
        id="stack-01",
        section="stack",
        layout="screen_rec",
        heading="The stack",
        start=st_start, end=orch_s,
        reveals=[
            reveal(1, st_start, sounds_s, "ElevenLabs — the voice",
                   "The same voice you're hearing right now", tags=["tool"]),
            reveal(1, sounds_s, orch_s, "Close to human on clean audio",
                   "Still stumbles: proper nouns, heavy accents", tags=["tool", "risk"]),
        ],
        source="Channel's own production stack — direct demonstration",
        sfx=[{"cue": "tick", "at": st_start}],
    ))
    screens.append(screen(
        id="stack-02",
        section="stack",
        layout="sheet",
        heading="The stack",
        start=orch_s, end=ctrl_s,
        reveals=[
            reveal(2, orch_s, bland_s, "Retell AI or Vapi — orchestration",
                   "Answer · Qualify · Book — ~7–15¢/min", tags=["tool", "number"]),
            reveal(2, bland_s, ctrl_s, "Bland — outbound alternative",
                   "Raised per-minute prices, Dec 2025", tags=["tool", "risk"]),
        ],
        source="Public pricing — vendor rate cards",
        sfx=[{"cue": "tick", "at": orch_s}],
    ))
    screens.append(screen(
        id="stack-03",
        section="stack",
        layout="quote",
        heading="The stack",
        start=ctrl_s, end=_pad_end(ctrl_e, st_end),
        reveals=[reveal(2, ctrl_s, ctrl_e, "You don't control this cost line.",
                        tags=["punchline", "risk"])],
        music={"intensity": "silence", "duck_db": 0},
        sfx=[{"cue": "hit", "at": ctrl_s}],
        custom={"quote": "You don't control this cost line. Nobody does.",
                "accentPhrase": "cost line",
                "ground": "navy"},
    ))
    screens.append(screen(
        id="stack-04",
        section="stack",
        layout="schematic",
        heading="The stack",
        start=_pad_end(ctrl_e, st_end), end=allin_s,
        reveals=[
            reveal(3, twilio_s, make_s, "Twilio — the number",
                   "~$1/mo + usage", tags=["tool", "number"]),
            reveal(3, make_s, allin_s, "Make/n8n → Cal.com",
                   "Owner sees a booked slot, not a transcript", tags=["tool", "process"]),
        ],
        source="Public pricing — vendor rate cards",
    ))
    screens.append(screen(
        id="stack-05",
        section="stack",
        layout="chart",
        heading="The stack",
        start=allin_s, end=loop_s,
        reveals=[reveal(4, allin_s, loop_s, "Solo stack: under $150/mo",
                        "Usage: tens of dollars, not hundreds — that gap is the margin",
                        tags=["claim", "number"])],
        figure={"text": "Monthly stack cost, all-in",
                "source": "Public pricing — stack component totals"},
        source="Public pricing — stack component totals",
        music={"intensity": "build", "duck_db": -10},
        sfx=[{"cue": "hit", "at": allin_s}],
    ))
    screens.append(screen(
        id="stack-06",
        section="stack",
        layout="schematic",
        heading="The stack",
        start=loop_s, end=st_end,
        reveals=[
            reveal(5, loop_s, retainer_s, "The delivery loop",
                   "Answer → Qualify → Book → Text the owner", tags=["process"]),
            reveal(5, retainer_s, land_s, "The retainer buys maintenance",
                   "Prompts · FAQs · Integrations — the moat and the treadmill",
                   tags=["process", "risk"]),
            reveal(5, land_s, st_end, "So how do you land the first client?",
                   tags=["question"]),
        ],
        sfx=[{"cue": "tick", "at": loop_s}],
    ))

    # ==================================================================
    # PLAYBOOK — vertical sheet → florist POV → demo screen_rec →
    # "demo is the sales call" quote → pricing card → month one →
    # TCPA risk → delivery discipline → FAQ rhythm.
    # ==================================================================
    pb_start, pb_end = section_bounds("playbook")
    florist_s, _ = find_phrase("playbook", "i work with over fifteen hundred")
    also_s, _ = find_phrase("playbook", "also week one")
    demo_s, demo_e = find_phrase("playbook", "that demo is the sales call")
    price_s, _ = find_phrase("playbook", "and price it as a receptionist replacement")
    month1_s, _ = find_phrase("playbook", "month one land your first three")
    tcpa_s, _ = find_phrase("playbook", "and inbound only")
    month2_s, _ = find_phrase("playbook", "month two is delivery discipline")
    visible_s, _ = find_phrase("playbook", "then make the maintenance visible")
    faq_s, _ = find_phrase("playbook", "build the faq list")
    rhythm_s, _ = find_phrase("playbook", "and that maintenance rhythm")

    screens.append(screen(
        id="playbook-01",
        section="playbook",
        layout="sheet",
        heading="The playbook",
        start=pb_start, end=florist_s,
        reveals=[reveal(1, pb_start, florist_s, "Week one: pick ONE vertical",
                        "Home services · Dental · Salons · Florists — where a missed call is a missed job",
                        tags=["process"])],
        sfx=[{"cue": "tick", "at": pb_start}],
    ))
    screens.append(screen(
        id="playbook-02",
        section="playbook",
        layout="broll",
        heading="The playbook",
        start=florist_s, end=also_s,
        reveals=[
            reveal(1, florist_s, (florist_s + also_s) / 2, "1,500+ florists, every Valentine's Day",
                   "Shop slammed · Phone ringing off the hook", tags=["operator_pov"]),
            reveal(1, (florist_s + also_s) / 2, also_s, "The overflow goes to the 1-800 competitor",
                   "Every year. Same story.", tags=["operator_pov"]),
        ],
        source="Operator experience — Lovingly, 1,500+ florists",
    ))
    screens.append(screen(
        id="playbook-03",
        section="playbook",
        layout="screen_rec",
        heading="The playbook",
        start=also_s, end=demo_s,
        reveals=[reveal(2, also_s, demo_s, "Build the demo on a REAL business",
                        "Ring their missed-call line · Agent answers · Books a fake appointment",
                        tags=["process"])],
        sfx=[{"cue": "tick", "at": also_s}],
    ))
    screens.append(screen(
        id="playbook-04",
        section="playbook",
        layout="quote",
        heading="The playbook",
        start=demo_s, end=_pad_end(demo_e, pb_end),
        reveals=[reveal(2, demo_s, demo_e, "That demo is the sales call.",
                        tags=["punchline"])],
        music={"intensity": "silence", "duck_db": 0},
        sfx=[{"cue": "hit", "at": demo_s}],
        custom={"quote": "That demo is the sales call.",
                "accentPhrase": "the sales call",
                "ground": "navy"},
    ))
    screens.append(screen(
        id="playbook-05",
        section="playbook",
        layout="proof_card",
        heading="The playbook",
        start=_pad_end(demo_e, pb_end), end=price_s,
        reveals=[reveal(2, _pad_end(demo_e, pb_end), price_s,
                        "Their own phone, working correctly",
                        "For the first time", tags=["claim"])],
        source="Playbook — demo-first sales motion (research brief)",
    ))
    screens.append(screen(
        id="playbook-06",
        section="playbook",
        layout="chart",
        heading="The playbook",
        start=price_s, end=month1_s,
        reveals=[
            reveal(3, price_s, (price_s + month1_s) / 2, "Receptionist replacement, never software",
                   "Setup: $500–2,000 · Retainer: $300–700/mo flat", tags=["claim", "number"]),
            reveal(3, (price_s + month1_s) / 2, month1_s, "Never quote per-minute",
                   "That's your cost structure, not theirs", tags=["process"]),
        ],
        figure={"text": "Pricing: setup + flat retainer",
                "source": "Vendor pricing bands — convergent, unaudited"},
        source="Vendor pricing bands — convergent, unaudited",
        music={"intensity": "build", "duck_db": -10},
    ))
    screens.append(screen(
        id="playbook-07",
        section="playbook",
        layout="sheet",
        heading="The playbook",
        start=month1_s, end=tcpa_s,
        reveals=[reveal(4, month1_s, tcpa_s, "Month one: 3 clients from your network",
                        "Their before/after missed-call numbers = the case study for the next five",
                        tags=["process", "number"])],
        sfx=[{"cue": "tick", "at": month1_s}],
    ))
    screens.append(screen(
        id="playbook-08",
        section="playbook",
        layout="risk_card",
        heading="The playbook",
        start=tcpa_s, end=month2_s,
        reveals=[reveal(4, tcpa_s, month2_s, "Stay inbound-only", tags=["risk"])],
        sfx=[{"cue": "hit", "at": tcpa_s}],
        source="Research brief — TCPA regulatory note",
        custom={"risk": {
            "title": "Outbound AI calling is TCPA territory.",
            "body": "Inbound answering keeps you out of it. This is not the boundary to test as a solo operator.",
            "bullets": [
                "Inbound = the safe solo play",
                "Outbound = regulated, lawyered, not worth it at this scale",
            ],
        }},
    ))
    screens.append(screen(
        id="playbook-09",
        section="playbook",
        layout="sheet",
        heading="The playbook",
        start=month2_s, end=faq_s,
        reveals=[
            reveal(5, month2_s, visible_s, "Month two: delivery discipline",
                   "Escalation path set BEFORE the first live call", tags=["process"]),
            reveal(5, visible_s, faq_s, "Make the maintenance visible",
                   "Monthly report: calls answered · booked · revenue recovered — it renews the retainer",
                   tags=["process"]),
        ],
        sfx=[{"cue": "tick", "at": month2_s}],
    ))
    screens.append(screen(
        id="playbook-10",
        section="playbook",
        layout="proof_card",
        heading="The playbook",
        start=faq_s, end=pb_end,
        reveals=[
            reveal(5, faq_s, rhythm_s, "FAQ list from real transcripts, weekly",
                   "Better every week — or quietly worse", tags=["process", "risk"]),
            reveal(5, rhythm_s, pb_end, "That rhythm IS the economics",
                   tags=["claim"]),
        ],
        source="Research brief — maintenance economics",
    ))

    # ==================================================================
    # ECONOMICS — blueprint mention → income chart → embarrassing-call
    # risk → platform-squeeze risk → closing question quote.
    # ==================================================================
    ec_start, ec_end = section_bounds("economics")
    income_s, _ = find_phrase("economics", "now realistic")
    fail_s, _ = find_phrase("economics", "here's the thing though")
    eighty_s, _ = find_phrase("economics", "the agent handles roughly 80 percent")
    plat_s, _ = find_phrase("economics", "platform risk here is higher")
    retdir_s, _ = find_phrase("economics", "retell already sells")
    open_s, _ = find_phrase("economics", "so the open question")
    sell_s, sell_e = find_phrase("economics", "sell it themselves")

    screens.append(screen(
        id="economics-01",
        section="economics",
        layout="sheet",
        heading="The economics",
        start=ec_start, end=income_s,
        reveals=[reveal(1, ec_start, income_s, "The blueprint — free, linked below",
                        "Vertical picker · Demo script · Pricing sheet",
                        tags=["cta"])],
        sfx=[{"cue": "tick", "at": ec_start}],
    ))
    screens.append(screen(
        id="economics-02",
        section="economics",
        layout="chart",
        heading="The economics",
        start=income_s, end=fail_s,
        reveals=[
            reveal(2, income_s, (income_s + fail_s) / 2, "Year one: $1,500–5,000/mo",
                   "3–8 local clients", tags=["claim", "number"]),
            reveal(2, (income_s + fail_s) / 2, fail_s, "An estimate, not audited results",
                   "Lower ceiling — thinner evidence, younger space", tags=["claim"]),
        ],
        figure={"text": "Realistic year-one income by client count",
                "source": "Estimate — reasoned from pricing bands, not audited"},
        source="Estimate — reasoned from pricing bands, not audited",
        music={"intensity": "build", "duck_db": -10},
        sfx=[{"cue": "hit", "at": income_s}],
    ))
    screens.append(screen(
        id="economics-03",
        section="economics",
        layout="risk_card",
        heading="The economics",
        start=fail_s, end=plat_s,
        reveals=[
            reveal(3, fail_s, eighty_s, "The first embarrassing call", tags=["risk"]),
            reveal(3, eighty_s, plat_s, "80% handled clean · 20% must escalate",
                   "Churn happens when escalation doesn't exist", tags=["risk", "number"]),
        ],
        sfx=[{"cue": "hit", "at": fail_s}],
        custom={"risk": {
            "title": "The failure mode isn't the pitch.",
            "body": "It's the first embarrassing call — an angry customer, a mispronounced name, an accent the agent can't parse.",
            "bullets": [
                "The agent handles ~80% cleanly",
                "The other 20% must escalate to a human",
                "Churn happens exactly when that path doesn't exist",
            ],
        }},
    ))
    screens.append(screen(
        id="economics-04",
        section="economics",
        layout="risk_card",
        heading="The economics",
        start=plat_s, end=open_s,
        reveals=[
            reveal(4, plat_s, retdir_s, "You're reselling someone else's margin",
                   "Bland already raised prices once", tags=["risk", "number"]),
            reveal(4, retdir_s, open_s, "Retell sells direct to SMBs already",
                   "The platforms could squeeze the agency layer out", tags=["risk"]),
        ],
        sfx=[{"cue": "hit", "at": plat_s}],
        source="Bland pricing change, Dec 2025; Retell direct sales — vendor pages",
        custom={"risk": {
            "title": "Platform risk is higher here.",
            "body": "You're reselling someone else's per-minute margin, and the platforms are moving toward the same SMBs you serve.",
            "bullets": [
                "Bland raised per-minute prices in Dec 2025",
                "Retell already sells an AI receptionist direct",
                "The agency layer could get squeezed",
            ],
        }},
    ))
    screens.append(screen(
        id="economics-05",
        section="economics",
        layout="sheet",
        heading="The economics",
        start=open_s, end=sell_s,
        reveals=[reveal(5, open_s, sell_s, "The open question",
                        "Not whether SMBs pay — whether the agency layer survives 18 months",
                        tags=["claim", "question"])],
    ))
    screens.append(screen(
        id="economics-06",
        section="economics",
        layout="quote",
        heading="The economics",
        start=sell_s, end=ec_end,
        reveals=[reveal(5, sell_s, sell_e, "…or the platforms just sell it themselves.",
                        tags=["punchline", "risk"])],
        music={"intensity": "silence", "duck_db": 0},
        sfx=[{"cue": "hit", "at": sell_s}],
        custom={"quote": "Or ElevenLabs and Retell just... sell it themselves.",
                "accentPhrase": "sell it themselves",
                "ground": "navy"},
    ))

    # ==================================================================
    # CTA
    # ==================================================================
    cta_start, cta_end = section_bounds("cta")
    screens.append(screen(
        id="cta-01",
        section="cta",
        layout="cta",
        heading="The Operator Blueprint",
        start=cta_start, end=cta_end,
        reveals=[reveal(1, cta_start, cta_end,
                        "№ 002 — The AI Phone Agency",
                        "Vertical picker · Demo script, step by step · Pricing sheet (setup + retainer) · "
                        "Every number sourced or flagged",
                        tags=["cta"])],
    ))

    return {
        "slug": "voice-agent-agency",
        "total_seconds": TOTAL_SECONDS,
        "screens": screens,
    }


if __name__ == "__main__":
    sb = build()
    STORYBOARD.write_text(json.dumps(sb, indent=2))
    n_quotes = sum(1 for s in sb["screens"] if s["layout"] == "quote")
    n_impact = sum(1 for s in sb["screens"] if s["layout"] in ("quote", "proof_card", "ladder", "risk_card"))
    print(f"✓ Hand-tuned storyboard → {STORYBOARD}")
    print(f"  {len(sb['screens'])} screens · {n_quotes} quotes · "
          f"{n_impact} impact frames (quote|proof|ladder|risk)")
    print(f"  Total: {TOTAL_SECONDS:.2f}s")
