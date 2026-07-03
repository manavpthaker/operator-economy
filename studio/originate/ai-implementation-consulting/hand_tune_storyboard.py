"""
Hand-tuned storyboard for №001 (ai-implementation-consulting).

Assembles the 13 impact moments the research doc calls out (Phase 4
of docs/edit-grammar-implementation-prompt.md) into a final
`storyboard.json` that overwrites the auto pass.

Run:
    python originate/ai-implementation-consulting/hand_tune_storyboard.py

Emits:
    originate/ai-implementation-consulting/storyboard.json

The impact-frame times below come from the research doc's
verified-against-VO table. Every quote_card must be short (1.2–4s)
and every impact frame carries a `music: silence` cue so the audio
bed cuts before the line lands (craft §P0).
"""

from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).parent
STORYBOARD = HERE / "storyboard.json"


def screen(**kw):
    """Build a screen dict, defaulting audio to the section's own file."""
    section = kw["section"]
    kw.setdefault("audio", f"vo/{section}.mp3")
    kw.setdefault("figure", None)
    kw.setdefault("source", None)
    kw.setdefault("music", {"intensity": "calm", "duck_db": -16})
    kw.setdefault("sfx", [])
    kw.setdefault("custom", None)
    return kw


def sheet_reveal(beat, at, end, title, body="", tags=None):
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
    screens = []

    # -------- HOOK --------
    screens.append(screen(
        id="hook-01",
        section="hook",
        layout="gap",
        heading="The gap",
        start=0.0, end=12.88,
        reveals=[sheet_reveal(1, 0.0, 12.88,
                              title="AI implementation: same service, three scales",
                              tags=["claim", "number"])],
        figure={"text": "$5.9B → $2K", "source": "CIO Dive / Constellation, FY2025"},
        source="CIO Dive / Constellation, FY2025",
        music={"intensity": "silence", "duck_db": 0},
        sfx=[{"cue": "hit", "at": 0.0}],
    ))

    # -------- THESIS (SPLIT for impact moments) --------
    # thesis beat 1: 12.88-25.28 "The Gap"
    screens.append(screen(
        id="thesis-01",
        section="thesis",
        layout="sheet",
        heading="The thesis",
        start=12.88, end=23.55,
        reveals=[sheet_reveal(1, 12.88, 23.55, "The Gap",
                              "Knows it should use AI · Doesn't know how · Pays someone who does",
                              tags=["claim", "operator_pov"])],
        sfx=[{"cue": "tick", "at": 12.88}],
    ))
    # QUOTE: "It's called implementation." (23.55-25.20)
    screens.append(screen(
        id="thesis-02",
        section="thesis",
        layout="quote",
        heading="The thesis",
        start=23.55, end=25.28,
        reveals=[sheet_reveal(1, 23.55, 25.28, "It's called implementation.",
                              tags=["punchline"])],
        music={"intensity": "silence", "duck_db": 0},
        sfx=[{"cue": "hit", "at": 23.55}],
        custom={
            "quote": "It's called implementation.",
            "accentPhrase": "implementation",
            "onInk": True,
        },
    ))
    # thesis beat 2: 25.28-50.74 "Not building. Installing." — split around 45.61
    screens.append(screen(
        id="thesis-03",
        section="thesis",
        layout="sheet",
        heading="The thesis",
        start=25.28, end=45.61,
        reveals=[sheet_reveal(2, 25.28, 45.61, "Not building. Installing.",
                              "Tools already exist · Wire into intake, follow-ups, reporting · The install is the product",
                              tags=["claim"])],
        sfx=[{"cue": "tick", "at": 25.28}],
    ))
    # QUOTE: "The gap was never the software." (45.61-48.77 to eat the 1s gap)
    screens.append(screen(
        id="thesis-04",
        section="thesis",
        layout="quote",
        heading="The thesis",
        start=45.61, end=48.77,
        reveals=[sheet_reveal(2, 45.61, 48.77, "The gap was never the software.",
                              tags=["punchline"])],
        music={"intensity": "silence", "duck_db": 0},
        sfx=[{"cue": "hit", "at": 45.61}],
        custom={
            "quote": "The gap was never the software.",
            "onInk": True,
        },
    ))
    # QUOTE follow-up: "Until it actually ran." (48.77-50.74)
    screens.append(screen(
        id="thesis-05",
        section="thesis",
        layout="quote",
        heading="The thesis",
        start=48.77, end=50.74,
        reveals=[sheet_reveal(2, 48.77, 50.74, "Until it actually ran.",
                              tags=["punchline"])],
        music={"intensity": "silence", "duck_db": 0},
        sfx=[{"cue": "hit", "at": 48.77}],
        custom={
            "quote": "Until it actually ran.",
            "accentPhrase": "actually ran",
            "onInk": True,
        },
    ))
    # thesis beat 3: 50.74-67.28 "Why one person can do this now" — split at 63.65
    screens.append(screen(
        id="thesis-06",
        section="thesis",
        layout="sheet",
        heading="The thesis",
        start=50.74, end=63.65,
        reveals=[sheet_reveal(3, 50.74, 63.65, "Why one person can do this now",
                              "Installation went no-code · Integrator + 6 months · → one afternoon",
                              tags=["claim", "operator_pov"])],
        sfx=[{"cue": "tick", "at": 50.74}],
    ))
    # QUOTE (question): "Why is Accenture charging billions for it?" (63.65-67.28)
    screens.append(screen(
        id="thesis-07",
        section="thesis",
        layout="quote",
        heading="The thesis",
        start=63.65, end=67.28,
        reveals=[sheet_reveal(3, 63.65, 67.28, "Why is Accenture charging billions for it?",
                              tags=["question"])],
        music={"intensity": "silence", "duck_db": 0},
        sfx=[{"cue": "hit", "at": 63.65}],
        custom={
            "quote": "Why is Accenture charging billions for it?",
            "accentPhrase": "billions",
            "onInk": True,
        },
    ))

    # -------- EVIDENCE --------
    screens.append(screen(
        id="evidence-01",
        section="evidence",
        layout="chart",
        heading="The evidence",
        start=67.28, end=80.40,
        reveals=[sheet_reveal(1, 67.28, 80.40, "Accenture GenAI, FY2025",
                              tags=["claim", "number"])],
        figure={"text": "Accenture GenAI FY2025", "source": "CIO Dive; Constellation Research; Accenture Annual Report 2025"},
        source="CIO Dive; Constellation Research; Accenture Annual Report 2025",
        music={"intensity": "build", "duck_db": -10},
        sfx=[{"cue": "hit", "at": 67.28}],
    ))
    # PROOF CARD: "The AI implementation work is the only thing growing." (84.66-87.76)
    # Covers evidence beat 2 (80.4-93.7)
    screens.append(screen(
        id="evidence-02",
        section="evidence",
        layout="proof_card",
        heading="The evidence",
        start=80.40, end=93.70,
        reveals=[sheet_reveal(2, 80.40, 93.70,
                              "AI implementation work — the only growth",
                              tags=["claim", "number"])],
        figure={"text": "~2x GenAI bookings", "source": "Constellation Research; CIO Dive Q1 FY2026"},
        source="Constellation Research; CIO Dive Q1 FY2026",
        music={"intensity": "build", "duck_db": -10},
        sfx=[{"cue": "hit", "at": 84.66}],
        custom={
            "proof": {
                "value": 2,
                "suffix": "x",
                "label": "GenAI bookings vs. FY24",
                "contrast": "Overall new bookings: flat.",
                "source": "Constellation Research · CIO Dive Q1 FY2026",
            },
        },
    ))
    # evidence beat 3 (93.7-111.2): "$40K/mo — reported" → proof_card
    # w/ estimate label. Single big number with an explicit reliability
    # frame is exactly what proof_card is for (research doc §"Prefer
    # artifact-first visuals").
    screens.append(screen(
        id="evidence-03",
        section="evidence",
        layout="proof_card",
        heading="The evidence",
        start=93.70, end=111.20,
        reveals=[sheet_reveal(3, 93.70, 111.20,
                              "Solo agency: $40K/mo — reported, unverified",
                              tags=["claim", "number"])],
        figure={"text": "$40K/mo (reported)", "source": "Medium / The AI Studio, Mar 2026 — reported, unverified"},
        source="Medium / The AI Studio, Mar 2026 — reported, unverified",
        music={"intensity": "build", "duck_db": -10},
        sfx=[{"cue": "hit", "at": 93.70}],
        custom={
            "proof": {
                "value": 40000,
                "prefix": "$",
                "suffix": "/mo",
                "compactCurrency": True,
                "label": "Solo agency claim · reported",
                "contrast": "REPORTED — unverified. Ceiling, not average.",
                "source": "Medium / The AI Studio, Mar 2026 — reported, unverified",
                "estimate": True,
            },
        },
    ))
    # evidence beat 4 (111.2-128): pricing ranges chart
    screens.append(screen(
        id="evidence-04",
        section="evidence",
        layout="chart",
        heading="The evidence",
        start=111.20, end=128.0,
        reveals=[sheet_reveal(4, 111.20, 128.0, "Pricing ranges (converging sources)",
                              tags=["claim", "number"])],
        figure={"text": "Pricing ranges", "source": "Multiple creator reports — estimate"},
        source="Multiple creator reports — estimate",
        music={"intensity": "build", "duck_db": -10},
    ))
    # evidence beat 5 (128-157): The attach effect — SPLIT for "Services attach to services." + "That's not scope creep..."
    screens.append(screen(
        id="evidence-05",
        section="evidence",
        layout="sheet",
        heading="The evidence",
        start=128.0, end=135.85,
        reveals=[sheet_reveal(5, 128.0, 135.85, "The attach effect",
                              "~1 in 2 projects pulls more work",
                              tags=["claim"])],
        source="CIO Dive (data pull-through on ~1 in 2 GenAI projects)",
    ))
    # QUOTE: "Services attach to services." (135.85-137.84) → schematic
    screens.append(screen(
        id="evidence-06",
        section="evidence",
        layout="quote",
        heading="The evidence",
        start=135.85, end=137.84,
        reveals=[sheet_reveal(5, 135.85, 137.84, "Services attach to services.",
                              tags=["punchline"])],
        music={"intensity": "silence", "duck_db": 0},
        sfx=[{"cue": "hit", "at": 135.85}],
        custom={
            "quote": "Services attach to services.",
            "accentPhrase": "attach",
            "onInk": True,
        },
    ))
    screens.append(screen(
        id="evidence-07",
        section="evidence",
        layout="sheet",
        heading="The evidence",
        start=137.84, end=153.84,
        reveals=[sheet_reveal(5, 137.84, 153.84,
                              "Install → data cleanup → next workflow → retainer",
                              "Transaction → relationship",
                              tags=["claim", "process"])],
        source="CIO Dive (data pull-through on ~1 in 2 GenAI projects)",
    ))
    # QUOTE (high impact): "That's not scope creep. That's the business model." (153.84-157)
    screens.append(screen(
        id="evidence-08",
        section="evidence",
        layout="quote",
        heading="The evidence",
        start=153.84, end=157.12,
        reveals=[sheet_reveal(5, 153.84, 157.12,
                              "That's not scope creep. That's the business model.",
                              tags=["punchline"])],
        music={"intensity": "silence", "duck_db": 0},
        sfx=[{"cue": "hit", "at": 153.84}],
        custom={
            "quote": "That's not scope creep. That's the business model.",
            "accentPhrase": "the business model",
            "onInk": True,
        },
    ))
    # LADDER: "Same business, three scales" (157.12-170.40) — bare-sheet fix
    screens.append(screen(
        id="evidence-09",
        section="evidence",
        layout="ladder",
        heading="The evidence",
        start=157.12, end=170.40,
        reveals=[sheet_reveal(6, 157.12, 170.40, "Same business, three scales",
                              tags=["claim", "number"])],
        figure={"text": "3 scales, one service", "source": "Synthesis; boutique figure reported/unverified"},
        source="Synthesis; boutique figure reported/unverified",
        music={"intensity": "build", "duck_db": -10},
        sfx=[{"cue": "hit", "at": 157.12}],
        custom={
            "ladder": {
                "overline": "THE EVIDENCE · SCALE LADDER",
                "heading": "Same business. Three scales.",
                "steps": [
                    {"label": "Freelancer / mo", "value": 6000, "prefix": "$", "compactCurrency": True},
                    {"label": "Boutique / mo (reported)", "value": 40000, "prefix": "$", "compactCurrency": True},
                    {"label": "Accenture / mo (avg)", "value": 225000000, "prefix": "$", "compactCurrency": True},
                ],
                "source": "Synthesis; boutique figure reported / unverified",
                "estimate": True,
            },
        },
    ))

    # -------- STACK -------- (unchanged — schematic covers whole section)
    screens.append(screen(
        id="stack-01",
        section="stack",
        layout="schematic",
        heading="The stack",
        start=170.40, end=214.50,
        reveals=[
            sheet_reveal(1, 170.40, 180.80, "The brain — $20–40/mo",
                         "Claude / ChatGPT · Analysis, drafts, the build itself",
                         tags=["tool"]),
            sheet_reveal(2, 180.80, 190.90, "The runtime — ~$0–30/mo",
                         "n8n (self-hosted ≈ free) · Make / Zapier · Executes workflows",
                         tags=["tool", "process"]),
            sheet_reveal(3, 190.90, 199.90, "The client-facing layer",
                         "Airtable / Notion dashboard",
                         tags=["tool"]),
            sheet_reveal(4, 199.90, 214.50, "Full stack < $100/mo",
                         "Loom for async delivery · Free tiers · COGS ≈ zero on a $2K project",
                         tags=["number"]),
        ],
        source="Public pricing — estimate",
    ))

    # -------- PLAYBOOK --------
    # playbook beats 1-3 merged into ONE persistent sheet with 3 reveals
    # (respects the "no >2 consecutive sheet screens" rule and gives
    # this sheet the 2-reveal minimum). Beats 4 (broll → artifact) and
    # 5 (schematic) each stand alone below.
    screens.append(screen(
        id="playbook-01",
        section="playbook",
        layout="sheet",
        heading="The playbook",
        start=214.50, end=258.0,
        reveals=[
            sheet_reveal(1, 214.50, 237.40,
                         "Week 1: pick the industry you can argue with",
                         "One vertical, not 'small businesses' · Problems you can name from memory",
                         tags=["operator_pov"]),
            sheet_reveal(2, 237.40, 250.30, "Weeks 2–4: buy proof",
                         "2–3 real case studies · Cheap or free for people you know · Proof is the only marketing",
                         tags=["claim", "operator_pov"]),
            sheet_reveal(3, 250.30, 258.0, "Package one named problem",
                         "Fixed scope: $2–5K, one deadline",
                         tags=["claim"]),
        ],
        source="Convergent recommendation across sources",
        sfx=[
            {"cue": "tick", "at": 214.50},
            {"cue": "tick", "at": 237.40},
            {"cue": "tick", "at": 250.30},
        ],
    ))
    # OFFER CARD: 258.0-263.64 "Missed calls get answered and booked"
    screens.append(screen(
        id="playbook-02",
        section="playbook",
        layout="offer_card",
        heading="The playbook",
        start=258.0, end=263.70,
        reveals=[sheet_reveal(3, 258.0, 263.70,
                              "Missed calls get answered and booked",
                              tags=["punchline", "operator_pov"])],
        source="Pricing ranges per research brief — estimate",
        sfx=[{"cue": "tick", "at": 258.0}],
        custom={
            "offer": {
                "problem": "Missed calls at independent hotels — 12–18 % of inbound demand walks",
                "deliverable": "Callback within 90 s + booking landed in Airtable",
                "price": "$2,000 fixed",
                "deadline": "14 days",
                "source": "Convergent pricing per research brief — estimate",
            },
        },
    ))
    # ARTIFACT: 263.70-274.56 "Your credibility from the industry you left is the actual asset."
    # Replaces the broll placeholder entirely (research doc §"Fix the b-roll problem").
    screens.append(screen(
        id="playbook-03",
        section="playbook",
        layout="artifact",
        heading="The playbook",
        start=263.70, end=274.60,
        reveals=[sheet_reveal(4, 263.70, 274.60,
                              "Operator credibility is the asset",
                              tags=["operator_pov"])],
        source="Operator experience — Manav",
        sfx=[{"cue": "tick", "at": 263.70}, {"cue": "tick", "at": 270.67}],
        custom={
            "artifact": {
                "overline": "OPERATOR ASSET · ATTACH PATH",
                "title": "Credibility → warm intro → first install",
                "nodes": [
                    {"id": "credibility",
                     "label": "Credibility",
                     "sub": "Industry you left"},
                    {"id": "intro",
                     "label": "Warm intro",
                     "sub": "One name, one email"},
                    {"id": "install",
                     "label": "First install",
                     "sub": "$2K fixed-scope project",
                     "emphasis": True},
                ],
                "callout": "Cold outreach loses to operators-who-know-operators — every time.",
                "source": "Operator experience — Manav",
            },
        },
    ))
    # SCHEMATIC (small): "The first project is designed to surface the second." (283.80-286.64)
    # Covers playbook beat 5 (274.6-286.6). Using case_file so it renders as a card, not a
    # schematic panel (schematic layer is reserved for the stack section).
    screens.append(screen(
        id="playbook-04",
        section="playbook",
        layout="case_file",
        heading="The playbook",
        start=274.60, end=286.60,
        reveals=[sheet_reveal(5, 274.60, 286.60,
                              "Project → retainer",
                              tags=["claim", "process"])],
        source="Retainer ranges per research brief — estimate",
        sfx=[{"cue": "tick", "at": 274.60}, {"cue": "hit", "at": 283.80}],
        custom={
            "caseFile": {
                "reference": "Attach path · Case pattern",
                "problem": "First install lands and reveals adjacent work",
                "workflow": "Install → maintenance + one new workflow / mo",
                "result": "$500–5K / mo retainer, referral in ~1 of 2 accounts",
                "source": "Retainer ranges per research brief — estimate",
            },
        },
    ))

    # -------- ECONOMICS --------
    screens.append(screen(
        id="economics-01",
        section="economics",
        layout="chart",
        heading="The economics",
        start=286.60, end=305.60,
        reveals=[sheet_reveal(1, 286.60, 305.60, "Where the margin comes from",
                              tags=["number"])],
        figure={"text": "$2K revenue vs. tool COGS", "source": "Public pricing; margins directional per research"},
        source="Public pricing; margins directional per research",
        music={"intensity": "build", "duck_db": -10},
    ))
    screens.append(screen(
        id="economics-02",
        section="economics",
        layout="sheet",
        heading="The economics",
        start=305.60, end=319.90,
        reveals=[sheet_reveal(2, 305.60, 319.90, "Realistic year one",
                              "$2–8K/mo (estimate) · The $40K stories sell courses",
                              tags=["number", "operator_pov"])],
        source="Estimate — reasoning from pricing ranges and solo capacity",
    ))
    # RISK CARD: "Revenue stops when you stop." (323.33-325.04) — covers whole beat 3
    screens.append(screen(
        id="economics-03",
        section="economics",
        layout="risk_card",
        heading="The economics",
        start=319.90, end=337.40,
        reveals=[sheet_reveal(3, 319.90, 337.40, "Three failure modes",
                              tags=["risk"])],
        sfx=[{"cue": "hit", "at": 323.33}],
        custom={
            "risk": {
                "title": "Revenue stops when you stop.",
                "body": "This is a service business. Retainers soften that; they don't cure it. At 3–5 clients, losing one is losing 25 % of your income.",
                "bullets": [
                    "You are the delivery capacity — vacations cost real dollars",
                    "Concentration risk sharpens at 3–5 clients",
                    "Every install is yours to maintain until you hand it off",
                ],
            },
        },
    ))
    screens.append(screen(
        id="economics-04",
        section="economics",
        layout="case_file",
        heading="The economics",
        start=337.40, end=350.10,
        reveals=[sheet_reveal(4, 337.40, 350.10, "The real output",
                              "Income that isn't a paycheck · Compounding skill stack · Client list = distribution",
                              tags=["operator_pov"])],
        custom={
            "caseFile": {
                "reference": "Compounding output",
                "problem": "Trading time for money forever",
                "workflow": "Every install = one more workflow you own + one warm client on the ledger",
                "result": "Income + skill + distribution that all compound",
            },
        },
    ))

    # -------- CTA --------
    # cta beat 1 (350.1-362.4): split for final brand card
    screens.append(screen(
        id="cta-01",
        section="cta",
        layout="cta",
        heading="The blueprint",
        start=350.10, end=359.99,
        reveals=[sheet_reveal(1, 350.10, 359.99, "The Operator Blueprint",
                              "Offer templates + stack setup · Every source, every number · Free — link below",
                              tags=["cta"])],
    ))
    # QUOTE: "Build it. Own it. Operate it." (359.99-362.40) — final brand card
    screens.append(screen(
        id="cta-02",
        section="cta",
        layout="quote",
        heading="The blueprint",
        start=359.99, end=362.40,
        reveals=[sheet_reveal(1, 359.99, 362.40, "Build it. Own it. Operate it.",
                              tags=["punchline", "cta"])],
        music={"intensity": "silence", "duck_db": 0},
        sfx=[{"cue": "hit", "at": 359.99}],
        custom={
            "quote": "Build it. Own it. Operate it.",
            "accentPhrase": "Operate it",
            "attribution": "The Operator Economy",
            "onInk": True,
        },
    ))

    return {
        "slug": "ai-implementation-consulting",
        "total_seconds": 362.4,
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
