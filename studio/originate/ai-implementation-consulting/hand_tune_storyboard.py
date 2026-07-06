"""
Hand-tuned storyboard for №001 (ai-implementation-consulting).

Assembles the impact moments the research doc calls out (Phase 4 of
docs/edit-grammar-implementation-prompt.md) into a final
`storyboard.json` that overwrites the auto pass.

Voice-agnostic: reads vo/words.json + vo/timeline.json and looks up
each impact phrase in the current VO. When the operator regenerates
voice, re-running this script produces a storyboard whose quote /
proof / ladder / risk / offer cards land on the newly-timed VO words.

Run:
    python originate/ai-implementation-consulting/hand_tune_storyboard.py

Emits:
    originate/ai-implementation-consulting/storyboard.json
"""

from __future__ import annotations

import json
import re
from pathlib import Path

HERE = Path(__file__).parent
STORYBOARD = HERE / "storyboard.json"
WORDS = json.loads((HERE / "vo" / "words.json").read_text())
TIMELINE = json.loads((HERE / "vo" / "timeline.json").read_text())

# Group words by section — every lookup starts here.
_SECTION_WORDS: dict[str, list[dict]] = {}
for _w in WORDS:
    _SECTION_WORDS.setdefault(_w["section"], []).append(_w)

_SECTION_TIMING: dict[str, tuple[float, float]] = {
    s["section"]: (s["start"], s["start"] + s["duration"])
    for s in TIMELINE["sections"]
}
TOTAL_SECONDS: float = TIMELINE["total_seconds"]


# ---------------------------------------------------------------------
# Lookups
# ---------------------------------------------------------------------

def _norm(w: str) -> str:
    """Normalize a token: keep letters and internal apostrophes only.
    Trailing / leading apostrophes (from stripped quote punctuation)
    are removed so `booked.'` matches `booked`."""
    stripped = re.sub(r"[^\w']", "", w)
    return stripped.strip("'").lower()


def find_phrase(section: str, phrase: str) -> tuple[float, float]:
    """Return (start, end) seconds of the first occurrence of `phrase`
    inside the given section's word list. Matches on normalized tokens
    so punctuation differences don't hurt. Raises if not found."""
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
    """Nudge a quote card's end to eat the ≤400ms silence that often
    follows a punchline so the next scene doesn't blip in early."""
    return min(end + 0.3, max_end)


# ---------------------------------------------------------------------
# Screen / reveal builders
# ---------------------------------------------------------------------

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


# ---------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------

def build() -> dict:
    screens: list[dict] = []

    # ==================================================================
    # HOOK — host card (self-intro, added 2026-07-04) → gap arrow.
    # The beat DROPS at acc_s (arrange_bed keys the drop to the first
    # gap-layout screen), so the $5.9B slam and the drums land together.
    # ==================================================================
    hook_start, hook_end = section_bounds("hook")
    acc_s, _acc_e = find_phrase("hook", "last year accenture")
    week_s, _week_e = find_phrase("hook", "this week")
    # hook-00a — BRAND screen while he introduces himself and the show
    # (2026-07-05: 'Sheet 01 of 34' card killed; brand carries the open).
    screens.append(screen(
        id="hook-00a",
        section="hook",
        layout="chapter_reset",
        heading="The Operator Economy",
        start=hook_start, end=week_s,
        reveals=[reveal(0, hook_start, week_s, "The Operator Economy",
                        tags=["claim"])],
        custom={"kicker": "BUILD · OWN · OPERATE"},
        sfx=[{"cue": "tick", "at": hook_start}],
    ))
    # hook-00b — OPERATOR BLUEPRINT title card from 'This week' through
    # the episode pitch AND the music bridge, until the hook stats hit.
    screens.append(screen(
        id="hook-00b",
        section="hook",
        layout="sheet",
        heading="Operator Blueprint",
        start=week_s, end=acc_s,
        reveals=[reveal(0, week_s, acc_s, "placeholder", tags=["claim"])],
        custom={"titleCard": {
            "overline": "Operator Blueprint · № 001",
            "title": "The $5.9 Billion Business You Can Start for $100",
            "thesis": "AI implementation: the same service, at every scale.",
        }},
        sfx=[{"cue": "tick", "at": week_s}],
    ))
    screens.append(screen(
        id="hook-01",
        section="hook",
        layout="gap",
        heading="The gap",
        start=acc_s, end=hook_end,
        reveals=[reveal(1, acc_s, hook_end,
                        "AI implementation: same service, three scales",
                        tags=["claim", "number"])],
        figure={"text": "$5.9B → $2K", "source": "CIO Dive / Constellation, FY2025"},
        source="CIO Dive / Constellation, FY2025",
        music={"intensity": "build", "duck_db": -8},
        sfx=[{"cue": "hit", "at": acc_s}],
    ))

    # ==================================================================
    # THESIS — 4 impact moments carved out of the section
    # ==================================================================
    th_start, th_end = section_bounds("thesis")
    q_impl_s, q_impl_e   = find_phrase("thesis", "it's called implementation")
    q_gap_s,  q_gap_e    = find_phrase("thesis", "gap was never the software")
    q_ran_s,  q_ran_e    = find_phrase("thesis", "until it actually ran")
    q_bill_s, q_bill_e   = find_phrase("thesis", "charging billions for it")

    # thesis-01 sheet up to "it's called implementation."
    screens.append(screen(
        id="thesis-01",
        section="thesis",
        layout="sheet",
        heading="The thesis",
        start=th_start, end=q_impl_s,
        reveals=[reveal(1, th_start, q_impl_s, "The Gap",
                        "Knows it should use AI · Doesn't know how · Pays someone who does",
                        tags=["claim", "operator_pov"])],
        sfx=[{"cue": "tick", "at": th_start}],
    ))
    screens.append(screen(
        id="thesis-02",
        section="thesis",
        layout="quote",
        heading="The thesis",
        start=q_impl_s, end=_pad_end(q_impl_e, th_end),
        reveals=[reveal(1, q_impl_s, q_impl_e, "It's called implementation.",
                        tags=["punchline"])],
        music={"intensity": "silence", "duck_db": 0},
        sfx=[{"cue": "hit", "at": q_impl_s}],
        custom={"quote": "It's called implementation.",
                "accentPhrase": "implementation",
                "ground": "navy"},
    ))
    # thesis-03 sheet — between "It's called implementation" and the
    # WIRING line, where the workflow sim takes over (tool shot #1).
    wire_s, _wire_e = find_phrase("thesis", "wiring them into how a real business actually runs")
    screens.append(screen(
        id="thesis-03",
        section="thesis",
        layout="sheet",
        heading="The thesis",
        start=_pad_end(q_impl_e, th_end), end=wire_s,
        reveals=[reveal(2, _pad_end(q_impl_e, th_end), wire_s,
                        "Not building. Installing.",
                        "Tools already exist · Wire into intake, follow-ups, reporting · The install is the product",
                        tags=["claim"])],
        sfx=[{"cue": "tick", "at": _pad_end(q_impl_e, th_end)}],
    ))
    # thesis-03b SIM — the exact workflow the line describes, executing.
    screens.append(screen(
        id="thesis-03b",
        section="thesis",
        layout="screen_rec",
        heading="The thesis",
        start=wire_s, end=q_gap_s,
        reveals=[reveal(2, wire_s, q_gap_s,
                        "Missed-call rescue — live run",
                        tags=["tool", "process"])],
        sfx=[{"cue": "tick", "at": wire_s}],
        custom={"sim": {
            "kind": "workflow",
            "title": "missed-call rescue — live run",
            "label": "n8n",
            "nodes": [
                {"label": "Missed call", "sub": "webhook trigger"},
                {"label": "Transcribe", "sub": "voicemail → text"},
                {"label": "Claude drafts reply", "sub": "guest gets an answer"},
                {"label": "Booking logged", "sub": "→ client dashboard"},
            ],
        }},
    ))
    # thesis-04 quote — "The gap was never the software."
    screens.append(screen(
        id="thesis-04",
        section="thesis",
        layout="quote",
        heading="The thesis",
        start=q_gap_s, end=q_ran_s,  # extend to eat the pause before "until it actually ran"
        reveals=[reveal(2, q_gap_s, q_gap_e,
                        "The gap was never the software.",
                        tags=["punchline"])],
        music={"intensity": "silence", "duck_db": 0},
        sfx=[{"cue": "hit", "at": q_gap_s}],
        custom={"quote": "The gap was never the software.",
                "ground": "navy"},
    ))
    # thesis-05 quote — "Until it actually ran."
    screens.append(screen(
        id="thesis-05",
        section="thesis",
        layout="quote",
        heading="The thesis",
        start=q_ran_s, end=_pad_end(q_ran_e, th_end),
        reveals=[reveal(2, q_ran_s, q_ran_e, "Until it actually ran.",
                        tags=["punchline"])],
        music={"intensity": "silence", "duck_db": 0},
        sfx=[{"cue": "hit", "at": q_ran_s}],
        custom={"quote": "Until it actually ran.",
                "accentPhrase": "actually ran",
                "ground": "navy"},
    ))
    # thesis-06 sheet — between "actually ran" and "charging billions"
    screens.append(screen(
        id="thesis-06",
        section="thesis",
        layout="sheet",
        heading="The thesis",
        start=_pad_end(q_ran_e, th_end), end=q_bill_s,
        reveals=[reveal(3, _pad_end(q_ran_e, th_end), q_bill_s,
                        "Why one person can do this now",
                        "Installation went no-code · Integrator + 6 months · → one afternoon",
                        tags=["claim", "operator_pov"])],
        sfx=[{"cue": "tick", "at": _pad_end(q_ran_e, th_end)}],
    ))
    # thesis-07 quote — question card into evidence
    screens.append(screen(
        id="thesis-07",
        section="thesis",
        layout="quote",
        heading="The thesis",
        start=q_bill_s, end=th_end,
        reveals=[reveal(3, q_bill_s, q_bill_e,
                        "Why is Accenture charging billions for it?",
                        tags=["question"])],
        music={"intensity": "silence", "duck_db": 0},
        sfx=[{"cue": "hit", "at": q_bill_s}],
        custom={"quote": "Why is Accenture charging billions for it?",
                "accentPhrase": "billions",
                "ground": "navy"},
    ))

    # ==================================================================
    # EVIDENCE — chart + proofs + quotes + ladder
    # ==================================================================
    ev_start, ev_end = section_bounds("evidence")
    # find the evidence beat 1 end — the "Accenture GenAI FY2025" chart
    # should own the "flat overall" / "growing" narrative. Beat 1 in
    # words.json ends before the shift into beat 2's proof, and beats
    # here are drift-heavy, so we use phrase anchors.
    q_growing_s, q_growing_e = find_phrase("evidence", "only thing growing")
    q_attach_s, q_attach_e   = find_phrase("evidence", "attach to services")
    q_creep_s, q_creep_e     = find_phrase("evidence", "scope creep")
    q_model_s, q_model_e     = find_phrase("evidence", "that's the business model")
    q_scales_s, q_scales_e   = find_phrase("evidence", "same business")

    # evidence-01 chart (Accenture GenAI FY2025)
    screens.append(screen(
        id="evidence-01",
        section="evidence",
        layout="chart",
        heading="The evidence",
        start=ev_start, end=q_growing_s - 3.5,  # give ~3.5s of narration lead
        reveals=[reveal(1, ev_start, q_growing_s - 3.5, "Accenture GenAI, FY2025",
                        tags=["claim", "number"])],
        figure={"text": "Accenture GenAI FY2025",
                "source": "CIO Dive; Constellation Research; Accenture Annual Report 2025"},
        source="CIO Dive; Constellation Research; Accenture Annual Report 2025",
        music={"intensity": "build", "duck_db": -10},
        sfx=[{"cue": "hit", "at": ev_start}],
    ))
    # evidence-02 proof_card — 2x GenAI vs FY24, brick "flat overall" contrast
    screens.append(screen(
        id="evidence-02",
        section="evidence",
        layout="proof_card",
        heading="The evidence",
        start=q_growing_s - 3.5, end=q_growing_e + 6,
        reveals=[reveal(2, q_growing_s - 3.5, q_growing_e + 6,
                        "AI implementation work — the only growth",
                        tags=["claim", "number"])],
        figure={"text": "~2x GenAI bookings",
                "source": "Constellation Research; CIO Dive Q1 FY2026"},
        source="Constellation Research; CIO Dive Q1 FY2026",
        music={"intensity": "build", "duck_db": -10},
        sfx=[{"cue": "hit", "at": q_growing_s}],
        custom={"proof": {
            "value": 2, "suffix": "x",
            "label": "GenAI bookings vs. FY24",
            "contrast": "Overall new bookings: flat.",
            "source": "Constellation Research · CIO Dive Q1 FY2026",
        }},
    ))
    # evidence-03 proof_card — $40K/mo REPORTED
    _dollar40 = None
    try:
        _dollar40 = find_phrase("evidence", "forty grand")
    except ValueError:
        pass
    ev03_start = q_growing_e + 6
    ev03_end = _dollar40[1] + 6 if _dollar40 else min(ev03_start + 22, q_attach_s)
    screens.append(screen(
        id="evidence-03",
        section="evidence",
        layout="proof_card",
        heading="The evidence",
        start=ev03_start, end=ev03_end,
        reveals=[reveal(3, ev03_start, ev03_end,
                        "Solo agency: $40K/mo — reported, unverified",
                        tags=["claim", "number"])],
        figure={"text": "$40K/mo (reported)",
                "source": "Medium / The AI Studio, Mar 2026 — reported, unverified"},
        source="Medium / The AI Studio, Mar 2026 — reported, unverified",
        music={"intensity": "build", "duck_db": -10},
        sfx=[{"cue": "hit", "at": ev03_start}],
        custom={"proof": {
            "value": 40000, "prefix": "$", "suffix": "/mo",
            "compactCurrency": True,
            "label": "Solo agency claim · reported",
            "contrast": "REPORTED — unverified. Ceiling, not average.",
            "source": "Medium / The AI Studio, Mar 2026 — reported, unverified",
            "estimate": True,
        }},
    ))
    # evidence-04 chart — pricing ranges
    ev04_start = ev03_end
    _ranges_end = None
    try:
        _ranges_end = find_phrase("evidence", "cheap to start")
    except ValueError:
        pass
    ev04_end = q_attach_s - 2
    screens.append(screen(
        id="evidence-04",
        section="evidence",
        layout="chart",
        heading="The evidence",
        start=ev04_start, end=ev04_end,
        reveals=[reveal(4, ev04_start, ev04_end,
                        "Pricing ranges (converging sources)",
                        tags=["claim", "number"])],
        figure={"text": "Pricing ranges",
                "source": "Multiple creator reports — estimate"},
        source="Multiple creator reports — estimate",
        music={"intensity": "build", "duck_db": -10},
    ))
    # evidence-05 sheet — "attach effect" narration lead-in
    screens.append(screen(
        id="evidence-05",
        section="evidence",
        layout="sheet",
        heading="The evidence",
        start=ev04_end, end=q_attach_s,
        reveals=[reveal(5, ev04_end, q_attach_s, "The attach effect",
                        "~1 in 2 projects pulls more work",
                        tags=["claim"])],
        source="CIO Dive (data pull-through on ~1 in 2 GenAI projects)",
    ))
    # evidence-06 quote — "Services attach to services."
    screens.append(screen(
        id="evidence-06",
        section="evidence",
        layout="quote",
        heading="The evidence",
        start=q_attach_s, end=_pad_end(q_attach_e, ev_end),
        reveals=[reveal(5, q_attach_s, q_attach_e,
                        "Services attach to services.",
                        tags=["punchline"])],
        music={"intensity": "silence", "duck_db": 0},
        sfx=[{"cue": "hit", "at": q_attach_s}],
        custom={"quote": "Services attach to services.",
                "accentPhrase": "attach",
                "ground": "navy"},  # evidence → navy per Rev C rotation
    ))
    # evidence-07 sheet — mid narration
    screens.append(screen(
        id="evidence-07",
        section="evidence",
        layout="sheet",
        heading="The evidence",
        start=_pad_end(q_attach_e, ev_end), end=q_creep_s,
        reveals=[reveal(5, _pad_end(q_attach_e, ev_end), q_creep_s,
                        "Install → data cleanup → next workflow → retainer",
                        "Transaction → relationship",
                        tags=["claim", "process"])],
        source="CIO Dive (data pull-through on ~1 in 2 GenAI projects)",
    ))
    # evidence-08 quote — "That's not scope creep. That's the business model."
    screens.append(screen(
        id="evidence-08",
        section="evidence",
        layout="quote",
        heading="The evidence",
        start=q_creep_s, end=_pad_end(q_model_e, ev_end),
        reveals=[reveal(5, q_creep_s, q_model_e,
                        "That's not scope creep. That's the business model.",
                        tags=["punchline"])],
        music={"intensity": "silence", "duck_db": 0},
        sfx=[{"cue": "hit", "at": q_creep_s}],
        custom={"quote": "That's not scope creep. That's the business model.",
                "accentPhrase": "the business model",
                "ground": "navy"},
    ))
    # evidence-09 ladder — same business, three scales
    screens.append(screen(
        id="evidence-09",
        section="evidence",
        layout="ladder",
        heading="The evidence",
        start=_pad_end(q_model_e, ev_end), end=ev_end,
        reveals=[reveal(6, _pad_end(q_model_e, ev_end), ev_end,
                        "Same business, three scales",
                        tags=["claim", "number"])],
        figure={"text": "3 scales, one service",
                "source": "Synthesis; boutique figure reported/unverified"},
        source="Synthesis; boutique figure reported/unverified",
        music={"intensity": "build", "duck_db": -10},
        sfx=[{"cue": "hit", "at": _pad_end(q_model_e, ev_end)}],
        custom={"ladder": {
            "overline": "THE EVIDENCE · SCALE LADDER",
            "heading": "Same business. Three scales.",
            "steps": [
                {"label": "Freelancer / mo", "value": 6000, "prefix": "$", "compactCurrency": True},
                {"label": "Boutique / mo (reported)", "value": 40000, "prefix": "$", "compactCurrency": True},
                {"label": "Accenture / mo (avg)", "value": 225000000, "prefix": "$", "compactCurrency": True},
            ],
            "source": "Synthesis; boutique figure reported / unverified",
            "estimate": True,
        }},
    ))

    # ==================================================================
    # STACK — schematic, interrupted by the DASHBOARD sim (tool shot #2)
    # at the client-facing-layer line, then schematic finale.
    # ==================================================================
    st_start, st_end = section_bounds("stack")
    cf_s, _cf_e = find_phrase("stack", "client facing layer")
    loom_s, _loom_e = find_phrase("stack", "loom for async delivery")
    st_mid = st_start + (cf_s - st_start) / 2
    screens.append(screen(
        id="stack-01",
        section="stack",
        layout="schematic",
        heading="The stack",
        start=st_start, end=cf_s,
        reveals=[
            reveal(1, st_start, st_mid, "The brain — $20–40/mo",
                   "Claude / ChatGPT · Analysis, drafts, the build itself",
                   tags=["tool"]),
            reveal(2, st_mid, cf_s, "The runtime — ~$0–30/mo",
                   "n8n (self-hosted ≈ free) · Make / Zapier · Executes workflows",
                   tags=["tool", "process"]),
        ],
        source="Public pricing — estimate",
    ))
    screens.append(screen(
        id="stack-02",
        section="stack",
        layout="screen_rec",
        heading="The stack",
        start=cf_s, end=loom_s,
        reveals=[reveal(3, cf_s, loom_s,
                        "The client-facing layer — what they log into",
                        tags=["tool"])],
        sfx=[{"cue": "tick", "at": cf_s}],
        custom={"sim": {
            "kind": "dashboard",
            "title": "Bookings — recovered from missed calls",
            "label": "Airtable",
            "columns": ["Guest", "Requested", "Status", "Value"],
            "rows": [
                ["M. Alvarez", "Fri · 2 nights", "Booked", "$418"],
                ["Party of 6", "Sat · 7:30 pm", "Booked", "$310"],
                ["J. Chen", "Tue · king room", "Callback sent", "—"],
                ["Walk-in inquiry", "tour + tasting", "New", "—"],
                ["R. Okafor", "Sun brunch · 4", "Booked", "$156"],
            ],
        }},
    ))
    screens.append(screen(
        id="stack-03",
        section="stack",
        layout="schematic",
        heading="The stack",
        start=loom_s, end=st_end,
        reveals=[
            reveal(4, loom_s, st_end, "Full stack < $100/mo",
                   "Loom for async delivery · Free tiers · COGS ≈ zero on a $2K project",
                   tags=["number"]),
        ],
        source="Public pricing — estimate",
    ))

    # ==================================================================
    # PLAYBOOK — sheet + offer + artifact + case_file
    # ==================================================================
    pb_start, pb_end = section_bounds("playbook")
    off_s, off_e = find_phrase("playbook", "answered and booked")
    # find "credibility" for the artifact anchor
    try:
        cred_s, cred_e = find_phrase("playbook", "credibility from the industry")
    except ValueError:
        cred_s, cred_e = find_phrase("playbook", "operators buy from operators")
    # playbook-01 sheet → ASSISTANT sim at "case studies" (tool shot #3)
    # → sheet resumes at "Then package".
    pb01_end = off_s - 5.5  # give ~5.5s narration lead to the offer moment
    cs_s, _cs_e = find_phrase("playbook", "build two or three real case studies")
    pk_s, _pk_e = find_phrase("playbook", "you package it")
    screens.append(screen(
        id="playbook-01",
        section="playbook",
        layout="sheet",
        heading="The playbook",
        start=pb_start, end=cs_s,
        reveals=[
            reveal(1, pb_start, cs_s,
                   "Week 1: pick the industry you can argue with",
                   "One vertical, not 'small businesses' · Problems you can name from memory",
                   tags=["operator_pov"]),
        ],
        source="Convergent recommendation across sources",
        sfx=[{"cue": "tick", "at": pb_start}],
    ))
    screens.append(screen(
        id="playbook-01b",
        section="playbook",
        layout="screen_rec",
        heading="The playbook",
        start=cs_s, end=pk_s,
        reveals=[reveal(2, cs_s, pk_s,
                        "Weeks 2–4: buy proof",
                        tags=["tool", "operator_pov"])],
        sfx=[{"cue": "tick", "at": cs_s}],
        custom={"sim": {
            "kind": "assistant",
            "title": "Claude — case study draft",
            "label": "Claude",
            "prompt": "Turn the Harbor House install into a one-page case study. Problem, what we wired in, what changed after 30 days. Keep it honest.",
            "response": "Case Study — Harbor House Inn (illustrative)\n\nProblem: evening calls went to voicemail. The desk was catching 6 of 10.\n\nThe install: missed call → transcript → drafted reply → booking logged. Live in an afternoon.\n\n30 days in: recovered bookings the desk never touched, and the owner's line: \"it pays for itself the first weekend.\"\n\nNext door, the restaurant wants the same intake fix.",
        }},
    ))
    screens.append(screen(
        id="playbook-01c",
        section="playbook",
        layout="sheet",
        heading="The playbook",
        start=pk_s, end=pb01_end,
        reveals=[
            reveal(3, pk_s, pb01_end,
                   "Package one named problem",
                   "Fixed scope: $2–5K, one deadline",
                   tags=["claim"]),
        ],
        source="Convergent recommendation across sources",
        sfx=[{"cue": "tick", "at": pk_s}],
    ))
    # playbook-02 offer_card — "Missed calls get answered and booked"
    screens.append(screen(
        id="playbook-02",
        section="playbook",
        layout="offer_card",
        heading="The playbook",
        start=pb01_end, end=cred_s - 1.5,
        reveals=[reveal(3, pb01_end, cred_s - 1.5,
                        "Missed calls get answered and booked",
                        tags=["punchline", "operator_pov"])],
        source="Pricing ranges per research brief — estimate",
        sfx=[{"cue": "tick", "at": off_s}],
        custom={"offer": {
            "problem": "Missed calls at independent hotels — 12–18 % of inbound demand walks",
            "deliverable": "Callback within 90 s + booking landed in Airtable",
            "price": "$2,000 fixed",
            "deadline": "14 days",
            "source": "Convergent pricing per research brief — estimate",
        }},
    ))
    # playbook-03 artifact — credibility → warm intro → first install
    pb03_end = min(cred_e + 10, pb_end)
    screens.append(screen(
        id="playbook-03",
        section="playbook",
        layout="artifact",
        heading="The playbook",
        start=cred_s - 1.5, end=pb03_end,
        reveals=[reveal(4, cred_s - 1.5, pb03_end,
                        "Operator credibility is the asset",
                        tags=["operator_pov"])],
        source="Operator experience — Manav",
        sfx=[{"cue": "tick", "at": cred_s - 1.5}, {"cue": "tick", "at": cred_s}],
        custom={"artifact": {
            "overline": "OPERATOR ASSET · ATTACH PATH",
            "title": "Credibility → warm intro → first install",
            "nodes": [
                {"id": "credibility", "label": "Credibility", "sub": "Industry you left"},
                {"id": "intro", "label": "Warm intro", "sub": "One name, one email"},
                {"id": "install", "label": "First install",
                 "sub": "$2K fixed-scope project", "emphasis": True},
            ],
            "callout": "Cold outreach loses to operators-who-know-operators — every time.",
            "source": "Operator experience — Manav",
        }},
    ))
    # playbook-04 case_file — project → retainer
    screens.append(screen(
        id="playbook-04",
        section="playbook",
        layout="case_file",
        heading="The playbook",
        start=pb03_end, end=pb_end,
        reveals=[reveal(5, pb03_end, pb_end, "Project → retainer",
                        tags=["claim", "process"])],
        source="Retainer ranges per research brief — estimate",
        sfx=[{"cue": "tick", "at": pb03_end}],
        custom={"caseFile": {
            "reference": "Attach path · Case pattern",
            "problem": "First install lands and reveals adjacent work",
            "workflow": "Install → maintenance + one new workflow / mo",
            "result": "$500–5K / mo retainer, referral in ~1 of 2 accounts",
            "source": "Retainer ranges per research brief — estimate",
        }},
    ))

    # ==================================================================
    # ECONOMICS — chart + sheet + risk + case_file
    # ==================================================================
    ec_start, ec_end = section_bounds("economics")
    risk_s, risk_e = find_phrase("economics", "revenue stops when you stop")

    # economics-01 chart — margins
    ec01_end = ec_start + (risk_s - ec_start) * 0.42
    screens.append(screen(
        id="economics-01",
        section="economics",
        layout="chart",
        heading="The economics",
        start=ec_start, end=ec01_end,
        reveals=[reveal(1, ec_start, ec01_end, "Where the margin comes from",
                        tags=["number"])],
        figure={"text": "$2K revenue vs. tool COGS",
                "source": "Public pricing; margins directional per research"},
        source="Public pricing; margins directional per research",
        music={"intensity": "build", "duck_db": -10},
    ))
    # economics-02 sheet — realistic year one
    screens.append(screen(
        id="economics-02",
        section="economics",
        layout="sheet",
        heading="The economics",
        start=ec01_end, end=risk_s - 1.0,
        reveals=[reveal(2, ec01_end, risk_s - 1.0, "Realistic year one",
                        "$2–8K/mo (estimate) · The $40K stories sell courses",
                        tags=["number", "operator_pov"])],
        source="Estimate — reasoning from pricing ranges and solo capacity",
    ))
    # economics-03 risk_card — Revenue stops when you stop
    ec03_end = min(risk_e + 15, ec_end - 6)
    screens.append(screen(
        id="economics-03",
        section="economics",
        layout="risk_card",
        heading="The economics",
        start=risk_s - 1.0, end=ec03_end,
        reveals=[reveal(3, risk_s - 1.0, ec03_end, "Three failure modes",
                        tags=["risk"])],
        sfx=[{"cue": "hit", "at": risk_s}],
        custom={"risk": {
            "title": "Revenue stops when you stop.",
            "body": "This is a service business. Retainers soften that; they don't cure it. At 3–5 clients, losing one is losing 25 % of your income.",
            "bullets": [
                "You are the delivery capacity — vacations cost real dollars",
                "Concentration risk sharpens at 3–5 clients",
                "Every install is yours to maintain until you hand it off",
            ],
        }},
    ))
    # economics-04 case_file — real output
    screens.append(screen(
        id="economics-04",
        section="economics",
        layout="case_file",
        heading="The economics",
        start=ec03_end, end=ec_end,
        reveals=[reveal(4, ec03_end, ec_end, "The real output",
                        "Income that isn't a paycheck · Compounding skill stack · Client list = distribution",
                        tags=["operator_pov"])],
        custom={"caseFile": {
            "reference": "Compounding output",
            "problem": "Trading time for money forever",
            "workflow": "Every install = one more workflow you own + one warm client on the ledger",
            "result": "Income + skill + distribution that all compound",
        }},
    ))

    # ==================================================================
    # CTA — cta + final brand quote
    # ==================================================================
    cta_start, cta_end = section_bounds("cta")
    brand_s, brand_e = find_phrase("cta", "build it. own it")

    # ONE cta screen (2026-07-05: duplicate 'Build it. Own it.' card
    # removed — the OutroCard already carries the sign-off + CTAs).
    # Episode-specific: blueprint as title, THIS episode underneath.
    screens.append(screen(
        id="cta-01",
        section="cta",
        layout="cta",
        heading="The Operator Blueprint",
        start=cta_start, end=cta_end,
        reveals=[reveal(1, cta_start, cta_end,
                        "№ 001 — AI Implementation Consulting",
                        "The missed-calls offer, templated · The exact stack, under $100/mo · "
                        "Week-by-week plan to your first client · Every number sourced",
                        tags=["cta"])],
    ))

    return {
        "slug": "ai-implementation-consulting",
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
    # Ground rotation echo
    from collections import Counter
    grounds = Counter(
        (s.get("custom") or {}).get("ground", "—")
        for s in sb["screens"] if s["layout"] == "quote"
    )
    print(f"  Quote grounds: {dict(grounds)}")
