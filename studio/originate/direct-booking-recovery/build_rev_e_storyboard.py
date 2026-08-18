"""Build the authored Rev E storyboard from the canonical script and VO timing.

The generic planner remains useful as a timing diagnostic, but its truncated
titles and multi-minute screens are not the episode. This builder is the
repeatable source for Rev E: one visual job per narration beat, plus a
four-composition cold open aligned to actual words.

Run from the repository root:
  python3 studio/originate/direct-booking-recovery/build_rev_e_storyboard.py
  python3 studio/scripts/originate/pace_storyboard.py \
    studio/originate/direct-booking-recovery/script.json
"""
from __future__ import annotations

import json
import re
from pathlib import Path

HERE = Path(__file__).parent
SCRIPT = json.loads((HERE / "script.json").read_text())
WORDS = json.loads((HERE / "vo" / "words.json").read_text())
TIMELINE = json.loads((HERE / "vo" / "timeline.json").read_text())
TAGS = json.loads((HERE / "storyboard-tags.json").read_text())

TAG_INDEX = {
    (item["section"], item["beat"]): item.get("tags", ["claim"])
    for item in TAGS.get("beats", [])
}
SECTION_WORDS = {
    section["id"]: [word for word in WORDS if word["section"] == section["id"]]
    for section in SCRIPT["sections"]
}
SECTION_TIMES = {
    item["section"]: (item["start"], item["start"] + item["duration"])
    for item in TIMELINE["sections"]
}


def norm(value: str) -> str:
    return re.sub(r"[^\w']", "", value).lower()


def find_phrase(section: str, phrase: str) -> float:
    tokens = [norm(token) for token in phrase.split() if norm(token)]
    words = SECTION_WORDS[section]
    normalized = [norm(word["word"]) for word in words]
    for index in range(len(normalized) - len(tokens) + 1):
        if normalized[index:index + len(tokens)] == tokens:
            return words[index]["start"]
    raise ValueError(f"Phrase not found in {section}: {phrase}")


def beat_ranges() -> dict[tuple[str, int], tuple[float, float]]:
    ranges: dict[tuple[str, int], tuple[float, float]] = {}
    for section in SCRIPT["sections"]:
        words = SECTION_WORDS[section["id"]]
        total = sum(len(beat["vo_text"].split()) for beat in section["beats"])
        cursor = 0
        starts: list[tuple[int, float]] = []
        for beat in section["beats"]:
            count = max(1, round(len(beat["vo_text"].split()) / total * len(words)))
            chunk = words[cursor:cursor + count] or words[-1:]
            starts.append((beat["beat"], chunk[0]["start"]))
            cursor += count
        section_start, section_end = SECTION_TIMES[section["id"]]
        for index, (beat_number, start) in enumerate(starts):
            end = starts[index + 1][1] if index + 1 < len(starts) else section_end
            ranges[(section["id"], beat_number)] = (
                section_start if index == 0 else start,
                end,
            )
    return ranges


RANGES = beat_ranges()

TITLES = {
    ("thesis", 1): "Turn discovery into a return relationship",
    ("thesis", 2): "Six fragments. One operator outcome.",
    ("thesis", 3): "The booking engine is the destination",
    ("evidence", 1): "63.4% of independent reservations arrive through OTAs",
    ("evidence", 2): "Visibility can push commission to 30%",
    ("evidence", 3): "The OTA booking cancels nearly twice as often",
    ("evidence", 4): "Make the commission line visible",
    ("evidence", 5): "OTA dependence is rational",
    ("evidence", 6): "The missing product is operating capacity",
    ("evidence", 7): "Capital is funding the infrastructure",
    ("stack", 1): "01 · Keep the property findable",
    ("stack", 2): "02 · Make the destination convert",
    ("stack", 3): "03 · Remember the guest with permission",
    ("stack", 4): "04 · Put judgment above automation",
    ("stack", 5): "Find · Convert · Remember · Return · Measure",
    ("playbook", 1): "Step 1 · Measure the gravity",
    ("playbook", 2): "Step 2 · Repair the destination",
    ("playbook", 3): "Step 3 · Recover the known guest",
    ("playbook", 4): "Step 4 · Extend discovery carefully",
    ("playbook", 5): "Publish the scope. Do not invent the rate.",
    ("playbook", 6): "Step 5 · Report direct share",
    ("economics", 1): "Commission exposure is not a recovery promise",
    ("economics", 2): "Salary data is not a client price",
    ("economics", 3): "The expensive layer is judgment",
    ("economics", 4): "Renewal is the test",
    ("economics", 5): "The second booking takes the gold path",
    ("cta", 1): "Make discovery a relationship the property can keep",
}

LAYOUTS = {
    ("thesis", 1): "schematic",
    ("thesis", 2): "proof_card",
    ("thesis", 3): "schematic",
    ("evidence", 1): "chart",
    ("evidence", 2): "chart",
    ("evidence", 3): "chart",
    ("evidence", 4): "proof_card",
    ("evidence", 5): "broll",
    ("evidence", 6): "broll",
    ("evidence", 7): "proof_card",
    ("stack", 1): "schematic",
    ("stack", 2): "schematic",
    ("stack", 3): "schematic",
    ("stack", 4): "proof_card",
    ("stack", 5): "schematic",
    ("playbook", 1): "sheet",
    ("playbook", 2): "screen_rec",
    ("playbook", 3): "sheet",
    ("playbook", 4): "sheet",
    ("playbook", 5): "proof_card",
    ("playbook", 6): "chart",
    ("economics", 1): "proof_card",
    ("economics", 2): "proof_card",
    ("economics", 3): "proof_card",
    ("economics", 4): "risk_card",
    ("economics", 5): "broll",
    ("cta", 1): "cta",
}

SECTION_STATE = {
    "thesis": ("recognition", "counter"),
    "evidence": ("consequence", "constraint"),
    "stack": ("counter-system", "counter"),
    "playbook": ("installation", "agency"),
    "economics": ("recovery", "resolution"),
    "cta": ("agency", "resolution"),
}


def reveal(section: str, beat: int, start: float, end: float, title: str,
           body: str, tags: list[str]) -> dict:
    return {
        "beat": beat,
        "at": start,
        "end": end,
        "title": title,
        "body": body,
        "tags": tags,
        "word_anchor": {"start": start, "end": end},
    }


def screen(*, screen_id: str, section: str, layout: str, start: float,
           end: float, title: str, body: str, beat: int, source: str | None,
           narrative_state: str, score_state: str, footage_role: str,
           preview_eligible: bool = False, custom: dict | None = None) -> dict:
    fragments = [fragment.strip() for fragment in body.split(" · ") if fragment.strip()]
    reveal_count = max(2, len(fragments)) if end - start > 20 and layout != "quote" else 1
    reveal_span = (end - start) / reveal_count
    reveals = []
    for index in range(reveal_count):
        reveal_start = start + index * reveal_span
        reveal_end = end if index + 1 == reveal_count else start + (index + 1) * reveal_span
        fragment = fragments[index] if index < len(fragments) else title
        reveals.append(reveal(
            section, beat, reveal_start, reveal_end,
            title if index == 0 else fragment[:1].upper() + fragment[1:],
            fragment if index == 0 else "",
            TAG_INDEX.get((section, beat), ["claim"]),
        ))
    concrete_queries = {
        "hook-01": "independent hotel innkeeper handing room key to guest close up",
        "evidence-05": "quaint rustic hotel bed and breakfast inn bedroom fireplace",
        "evidence-06": "tropical boutique hotel resort guests walking palm courtyard",
        "economics-05": "hotel host welcoming returning guests with room key",
    }
    return {
        "id": screen_id,
        "section": section,
        "layout": layout,
        "heading": title,
        "start": start,
        "end": end,
        "reveals": reveals,
        "figure": {"text": title, "source": source} if source else None,
        "source": source,
        "sfx": ([{"cue": "hit", "at": start}] if layout in {"quote", "proof_card"}
                else [{"cue": "tick", "at": item["at"]} for item in reveals[1:]]),
        "music": {"intensity": score_state, "duck_db": -16},
        "custom": custom,
        "narrative_state": narrative_state,
        "score_state": score_state,
        "footage_role": footage_role,
        "camera": "human" if layout == "broll" else "system",
        "preview_eligible": preview_eligible,
        "visual_intent": body,
        "search_query": concrete_queries.get(screen_id),
        "query_variants": [],
        "visual_exclusions": [],
        "events": [],
    }


screens: list[dict] = []
hook_source = SCRIPT["sections"][0]["beats"][0]["source"]
hook_end = SECTION_TIMES["hook"][1]
hook_cuts = [
    0.0,
    find_phrase("hook", "Cloudbeds reports"),
    find_phrase("hook", "At an illustrative"),
    find_phrase("hook", "My estimate"),
    hook_end,
]

screens.extend([
    screen(screen_id="hook-01", section="hook", layout="broll",
           start=hook_cuts[0], end=hook_cuts[1],
           title="A beautiful stay. A relationship still lost.",
           body="Warm key handoff. The guest leaves; the innkeeper remains.",
           beat=1, source=None, narrative_state="gravity", score_state="constraint",
           footage_role="human_context", preview_eligible=True),
    screen(screen_id="hook-02", section="hook", layout="schematic",
           start=hook_cuts[1], end=hook_cuts[2],
           title="63.4% pulled toward the OTAs",
           body="One hundred booking tokens; sixty-three fall down and right into OTA-blue gravity.",
           beat=1, source=hook_source, narrative_state="gravity", score_state="constraint",
           footage_role="market_force", preview_eligible=True),
    screen(screen_id="hook-03", section="hook", layout="proof_card",
           start=hook_cuts[2], end=hook_cuts[3],
           title="$135K annual commission exposure",
           body="20 rooms · $180 ADR · 70% occupancy · 63.4% OTA · illustrative estimate",
           beat=1, source=hook_source, narrative_state="consequence", score_state="constraint",
           footage_role="proof", preview_eligible=True,
           custom={"proof": {"value": 135000, "prefix": "$",
                             "label": "Illustrative annual OTA commission",
                             "contrast": "Assumptions visible · not a reported property result",
                             "estimate": True}}),
    screen(screen_id="hook-04", section="hook", layout="quote",
           start=hook_cuts[3], end=hook_cuts[4],
           title="The larger loss is the relationship.",
           body="MY ESTIMATE · THE HUMAN CONSEQUENCE",
           beat=1, source=hook_source, narrative_state="recognition", score_state="silence",
           footage_role="outcome", preview_eligible=True,
           custom={"quote": "The larger loss is the relationship.",
                   "accentPhrase": "the relationship", "ground": "navy"}),
])

for section in SCRIPT["sections"][1:]:
    narrative_state, score_state = SECTION_STATE[section["id"]]
    for beat in section["beats"]:
        key = (section["id"], beat["beat"])
        start, end = RANGES[key]
        layout = LAYOUTS[key]
        title = TITLES[key]
        source = beat.get("source")
        if key == ("playbook", 6):
            source = "Property booking records · direct-share baseline versus monthly result"
        if layout == "proof_card" and not source:
            source = "Operator analysis · Rev E operating model"
        role = (
            "human_context" if layout == "broll"
            else "proof" if layout in {"chart", "proof_card"}
            else "process" if section["id"] in {"stack", "playbook"}
            else "outcome"
        )
        screens.append(screen(
            screen_id=f"{section['id']}-{beat['beat']:02d}",
            section=section["id"], layout=layout, start=start, end=end,
            title=title, body=" · ".join(beat.get("highlight_words", [])),
            beat=beat["beat"], source=source,
            narrative_state=narrative_state, score_state=score_state,
            footage_role=role,
            preview_eligible=section["id"] == "thesis" and beat["beat"] <= 2,
        ))

storyboard = {
    "slug": SCRIPT["slug"],
    "storyboard_version": "rev-e-authored-1",
    "total_seconds": TIMELINE["total_seconds"],
    "narrative_waveform": [
        "gravity", "consequence", "recognition", "counter-system",
        "installation", "recovery", "agency",
    ],
    "screens": screens,
}

(HERE / "storyboard.json").write_text(json.dumps(storyboard, indent=2) + "\n")
print(f"Rev E storyboard: {len(screens)} screens over {TIMELINE['total_seconds']:.1f}s")
for item in screens[:8]:
    print(f"  {item['id']:<12} {item['layout']:<12} {item['end'] - item['start']:>5.1f}s  {item['heading']}")
