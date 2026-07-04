"""
Originate Step 3 (v2, 2026-07-03): plan the storyboard by tagging beats,
mapping tags to layouts, packing into screens, and emitting sfx / music
cues alongside timings.

Encodes docs/storyboard-stage.md v2 + docs/faceless-video-editing-research.md.

Inputs (produced by generate_vo.py / plan_assets.py):
    originate/<slug>/script.json
    originate/<slug>/vo/timeline.json        # per-section start + duration
    originate/<slug>/vo/words.json           # word-level timings
    originate/<slug>/assets.json             # OPTIONAL — used to catch layout
                                             # overrides (script says "broll",
                                             # plan_assets promoted to slide/etc.)

Outputs:
    originate/<slug>/storyboard.json         # the full storyboard (screens)
    originate/<slug>/storyboard-tags.json    # cached LLM tag pass

Usage:
    python scripts/originate/storyboard.py originate/<slug>/script.json
        [--no-tag-llm]     # skip the LLM tag pass entirely (uses cached or
                           # heuristic-only tagging — useful for local dev)
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent


# ---------------------------------------------------------------------
# Section metadata (canonical Rev C mapping)
# ---------------------------------------------------------------------

SECTION_META = {
    "hook":      {"heading": "The gap",      "onInk": True},
    "thesis":    {"heading": "The thesis",   "onInk": False},
    "evidence":  {"heading": "The evidence", "onInk": False},
    "stack":     {"heading": "The stack",    "onInk": True},
    "playbook":  {"heading": "The playbook", "onInk": False},
    "economics": {"heading": "The economics","onInk": False},
    "cta":       {"heading": "The blueprint","onInk": True},
}

TAG_VOCAB = ["claim", "number", "tool", "operator_pov", "punchline",
             "risk", "question", "process", "cta"]

LAYOUT_VOCAB = [
    "sheet", "schematic", "chart", "gap", "quote", "proof_card",
    "artifact", "offer_card", "case_file", "risk_card", "ladder",
    "source_card", "screen_rec", "broll", "chapter_reset", "cta",
]

# Screens marked "silence" imply the composition cuts music ~0.5s before
# the screen start (the silence IS the riser).
SILENCE_LAYOUTS = {"quote", "gap", "chapter_reset"}
BUILD_LAYOUTS = {"proof_card", "chart", "ladder"}


# ---------------------------------------------------------------------
# Beat → time-range mapping (mirrors prepare_longform.py's algorithm)
# ---------------------------------------------------------------------

def beat_time_ranges(script: dict, words: list[dict], timeline: dict) -> dict:
    out = {}
    for s in script["sections"]:
        sec_words = [w for w in words if w["section"] == s["id"]]
        sec_meta = next((t for t in timeline["sections"] if t["section"] == s["id"]), None)
        if not sec_words or not sec_meta:
            continue
        total_beat_words = sum(len(b["vo_text"].split()) for b in s["beats"]) or 1
        cursor = 0
        beat_ranges = []
        for b in s["beats"]:
            n = round(len(b["vo_text"].split()) / total_beat_words * len(sec_words))
            n = max(1, n)
            chunk = sec_words[cursor:cursor + n] or sec_words[-1:]
            cursor += n
            beat_ranges.append([b["beat"], chunk[0]["start"], chunk[-1]["end"]])
        for i in range(len(beat_ranges) - 1):
            beat_ranges[i][2] = beat_ranges[i + 1][1]
        if beat_ranges:
            beat_ranges[0][1] = sec_meta["start"]
            beat_ranges[-1][2] = sec_meta["start"] + sec_meta["duration"]
        for num, start, end in beat_ranges:
            out[(s["id"], num)] = (start, end)
    return out


# ---------------------------------------------------------------------
# Tagging — LLM-driven, cached, with heuristic fallback
# ---------------------------------------------------------------------

TAG_SYSTEM = """You tag beats of a scripted YouTube episode with a small
controlled vocabulary so a downstream planner can pick the right visual
layout for each. Return valid JSON only — no prose.

Tag vocabulary (each beat gets 1–3 tags):
  claim         — a factual assertion
  number        — the beat carries a specific figure (currency, %, x-multiple)
  tool          — the beat names a specific product/service by name
  operator_pov  — the line is Manav's operator experience / first-person judgment
  punchline     — short, quotable, high-impact line (≤12 words) — Short-hook candidate
  risk          — a failure mode / warning
  question      — a rhetorical or open question
  process       — describes a multi-step workflow or order-of-operations
  cta           — call-to-action content

Tag economically. A generic exposition line is just `claim`. Pull-quote
candidates ("It's called implementation.", "Services attach to services.")
must get `punchline`. Beats that name a specific number get `number`. Beats
with tool names get `tool`."""

TAG_USER_TEMPLATE = """Episode: {topic}

Return JSON in this exact shape:
{{"beats":[{{"section":"<id>","beat":<int>,"tags":[<tag>,...]}}, ...]}}

Beats:
{beats}"""


def _heuristic_tags(vo_text: str, section_id: str = "", is_last_of_last_section: bool = False) -> list[str]:
    """Fallback tagger for when the LLM isn't available. Deliberately
    stingy on tag firing — false positives cost us more than false
    negatives here (a missing tag falls back to `sheet`, which is fine;
    a spurious tag can promote a boring line to a quote card)."""
    tags: list[str] = []
    text = vo_text.strip()
    lower = text.lower()
    word_count = len(text.split())

    # cta — ONLY when the section is the cta section, or the line
    # explicitly names the blueprint download / free asset.
    if section_id == "cta" or is_last_of_last_section:
        tags.append("cta")
    elif re.search(r"\b(download the (free )?blueprint|link (is )?below|free blueprint)\b", lower):
        tags.append("cta")

    # number — currency, %, or numeric magnitude words
    if re.search(r"\$\s?\d|\b\d[\d,.]*\s?(?:%|percent|K|M|B|thousand|million|billion|x)\b", text, re.I):
        tags.append("number")

    # tool — proper-noun product names
    if re.search(r"\b(Claude|ChatGPT|GPT-\d|Airtable|Notion|Loom|n8n|Zapier|Make\.com|Retool|Cursor|Vercel|Stripe|HubSpot|Slack)\b", text):
        tags.append("tool")

    # question — ends with question mark and stands alone (not embedded)
    if text.rstrip().endswith("?"):
        tags.append("question")

    # risk — specific "this can go wrong" phrasing, not any use of "risk"
    if re.search(r"\b(fails?|failure|breaks?|stops? when you stop|concentration risk|dependenc(y|ies)|three (failure|risks))\b", lower):
        tags.append("risk")

    # operator_pov — first-person, from-experience phrasing
    if re.search(r"\b(I('ve| ) |my (experience|clients?|first)|I( learned| watched| built| ran))\b", text):
        tags.append("operator_pov")

    # punchline — short declarative WITHOUT sub-clauses (no colon, semicolon, comma before final word), high impact.
    # Explicit test: also fire on classical punchline shapes ("That's not X. That's Y." — 2 short sentences).
    is_short_declarative = (
        word_count <= 12
        and text.endswith(".")
        and not re.search(r"[:;]", text)
        and text.count(",") <= 1
    )
    two_sentence_shape = bool(re.match(r"^[^.]{5,60}\.\s+That'?s .{5,60}\.$", text))
    if is_short_declarative or two_sentence_shape:
        tags.append("punchline")

    # process — ONLY strong signals: numbered steps, "Step N", or explicit
    # arrows in the text (skip generic then/next/first, which appear
    # everywhere in narration).
    if re.search(r"\bStep \d|\b(week|phase|stage) \d|→\s*\w+\s*→|-> ?\w+ ?->", text, re.I):
        tags.append("process")

    if not tags:
        tags = ["claim"]
    return sorted(set(tags))


def tag_beats(script: dict, config: dict, cache_path: Path, use_llm: bool) -> dict:
    """Return {(section_id, beat_num): [tags...]}. Caches LLM output."""
    cached: dict = {}
    if cache_path.exists():
        try:
            raw = json.loads(cache_path.read_text())
            for b in raw.get("beats", []):
                cached[(b["section"], b["beat"])] = b.get("tags", [])
        except json.JSONDecodeError:
            cached = {}

    # If we already have tags for every beat, no need to hit the LLM.
    all_pairs = [(s["id"], b["beat"]) for s in script["sections"] for b in s["beats"]]
    missing = [p for p in all_pairs if p not in cached]

    if not missing:
        return cached

    # Heuristic-only path
    if not use_llm:
        print(f"  Tagging {len(missing)} beat(s) heuristically (LLM disabled)…", file=sys.stderr)
        # Figure out which is the very last beat so `cta` fires.
        last_beat_key = all_pairs[-1] if all_pairs else None
        for sec in script["sections"]:
            for b in sec["beats"]:
                key = (sec["id"], b["beat"])
                if key not in cached:
                    cached[key] = _heuristic_tags(b.get("vo_text", ""),
                                                  section_id=sec["id"],
                                                  is_last_of_last_section=(key == last_beat_key))
        cache_path.write_text(json.dumps({
            "beats": [{"section": k[0], "beat": k[1], "tags": v} for k, v in cached.items()],
        }, indent=2))
        return cached

    # LLM path — one call for all missing beats
    try:
        import anthropic
    except ImportError:
        print("  anthropic SDK not installed; falling back to heuristic tags.", file=sys.stderr)
        return tag_beats(script, config, cache_path, use_llm=False)

    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("  ANTHROPIC_API_KEY not set; falling back to heuristic tags.", file=sys.stderr)
        return tag_beats(script, config, cache_path, use_llm=False)

    beats_desc = []
    for sec in script["sections"]:
        for b in sec["beats"]:
            if (sec["id"], b["beat"]) not in cached:
                beats_desc.append({
                    "section": sec["id"],
                    "beat": b["beat"],
                    "vo_text": b["vo_text"],
                    "asset_hint": b.get("asset_hint"),
                })
    user_prompt = TAG_USER_TEMPLATE.format(
        topic=script.get("topic", script.get("working_title", "")),
        beats=json.dumps(beats_desc, indent=2),
    )
    print(f"  Tagging {len(beats_desc)} beat(s) via {config['models'].get('script')}…", file=sys.stderr)
    client = anthropic.Anthropic()
    resp = client.messages.create(
        model=config["models"].get("script", "claude-sonnet-4-20250514"),
        max_tokens=4000,
        system=TAG_SYSTEM,
        messages=[{"role": "user", "content": user_prompt}],
    )
    raw = next(b.text for b in resp.content if getattr(b, "type", "") == "text").strip()
    raw = re.sub(r"^```(json)?|```$", "", raw, flags=re.MULTILINE).strip()
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"  LLM tag JSON parse failed: {e}. Falling back to heuristic.", file=sys.stderr)
        return tag_beats(script, config, cache_path, use_llm=False)

    for b in data.get("beats", []):
        # Restrict to known tags, dedup, keep order stable.
        tags = [t for t in b.get("tags", []) if t in TAG_VOCAB]
        cached[(b["section"], b["beat"])] = sorted(set(tags)) or ["claim"]

    # Fill any beats the LLM missed with the heuristic.
    for key in missing:
        if key not in cached:
            sec = next(s for s in script["sections"] if s["id"] == key[0])
            b = next(bb for bb in sec["beats"] if bb["beat"] == key[1])
            cached[key] = _heuristic_tags(b.get("vo_text", ""), section_id=sec["id"])

    cache_path.write_text(json.dumps({
        "beats": [{"section": k[0], "beat": k[1], "tags": v} for k, v in cached.items()],
    }, indent=2))
    return cached


# ---------------------------------------------------------------------
# Tag → layout mapping (deterministic)
# ---------------------------------------------------------------------

def _pick_layout(
    beat: dict,
    tags: list[str],
    section_id: str,
    is_first_beat_of_section: bool,
    override_type: str | None,
) -> str:
    text = beat.get("vo_text", "")
    word_count = len(text.split())
    tset = set(tags)

    # Whole-section overrides win.
    if section_id == "cta":
        # cta section = always `cta` (unless the beat is clearly an offer card)
        if "number" in tset and re.search(r"\bfree\b|\blink\b", text.lower()):
            return "cta"
        return "cta"

    # Stack section: every beat is one node in a schematic — merged by pack step.
    if section_id == "stack":
        return "schematic"

    # Punchlines are quote cards. Short punchlines become `quote`; only
    # very short (≤6 words) ones with no numeric evidence.
    if "punchline" in tset and word_count <= 14 and "number" not in tset:
        return "quote"

    # Rhetorical questions that open a section = chapter_reset. Otherwise
    # a question with room for it becomes a quote card.
    if "question" in tset:
        if is_first_beat_of_section:
            return "chapter_reset"
        return "quote"

    # Risk = risk_card (one blunt warning card, never merged into sheets).
    if "risk" in tset:
        return "risk_card"

    # Number-carrying beats
    if "number" in tset:
        series = _extract_series(beat)  # from asset_hint or existing spec
        if series:
            # 3+ scales / values with strong contrast → ladder
            if len(series) >= 3 and _has_scale_contrast(series):
                return "ladder"
            # Hook + big-vs-small = gap
            if section_id == "hook" and len(series) == 2 and _has_gap_contrast(series):
                return "gap"
            if len(series) >= 2:
                return "chart"
        return "proof_card"

    # Tool + operator_pov = screen_rec (preferred); tool alone = artifact
    if "tool" in tset and "operator_pov" in tset:
        return "screen_rec"
    if "tool" in tset:
        return "artifact"

    # operator_pov + concrete place/action = artifact
    if "operator_pov" in tset and re.search(r"\b(counter|desk|walk in|hotel|restaurant|client|owner)\b", text.lower()):
        return "artifact"

    # process → schematic ONLY when the tag co-occurs with tool (a real
    # workflow) — process alone can appear on ordinary narration ("first
    # you do X, then Y") that reads better as a sheet.
    if "process" in tset and "tool" in tset:
        return "schematic"

    # Fall back to assets.json's asset type when tags are weak. This is
    # the ONLY place we let plan_assets' decisions leak into layout
    # choice; the LLM tag pass should make it rare when it runs, but
    # heuristic tagging misses number/tool signals routinely (e.g.
    # "billions" as a number, workflow VO without a proper-noun tool).
    if override_type == "chart":
        series = _extract_series(beat)
        if section_id == "hook" and series and _has_gap_contrast(series):
            return "gap"
        if series and _has_scale_contrast(series):
            return "ladder"
        return "chart"
    if override_type == "broll":
        return "broll"
    if override_type == "screen_rec":
        return "screen_rec"
    if override_type == "logo":
        return "artifact"  # promote — logos are a subset of artifacts now

    # In-body CTA content that carries no chart / artifact ends up on a
    # sheet — the mid-CTA line (§VI craft rubric) should not detonate a
    # standalone final-card visual in the middle of the argument.
    if "cta" in tset:
        return "sheet"

    # Default: sheet (merges with neighbours)
    return "sheet"


def _extract_series(beat: dict) -> list[dict]:
    """Return the beat's chart series if present (from `assets.json`
    spec merged upstream) or an empty list. Storyboard.py runs before
    plan_assets in the target order, so this only fires when the
    override lookup succeeds."""
    spec = beat.get("_asset_spec") or {}
    return spec.get("series") or []


def _has_scale_contrast(series: list[dict]) -> bool:
    vals = [d["value"] for d in series if d.get("value")]
    if len(vals) < 2:
        return False
    return max(vals) / max(min(vals), 1) > 100


def _has_gap_contrast(series: list[dict]) -> bool:
    vals = [d["value"] for d in series if d.get("value")]
    if len(vals) != 2:
        return False
    hi, lo = max(vals), min(vals)
    return hi / max(lo, 1) > 1000


# ---------------------------------------------------------------------
# Screen packing — collapse consecutive `sheet` layouts
# ---------------------------------------------------------------------

def derive_reveal_title(beat: dict, hint: str, layout: str) -> str:
    # First quoted phrase in the hint (author-authored working title).
    if hint:
        m = re.search(r"['‘’\"“”]([^'’\"”]{2,80})['’\"”]", hint)
        if m:
            return m.group(1).strip()
    # asset_hint prefix after ":" — first clause
    if hint:
        frag = re.split(r"[:—\-.]", hint, maxsplit=1)[0].strip()
        if frag and len(frag.split()) <= 10:
            return frag
    # Fallback: first 7 words of vo_text
    words = beat.get("vo_text", "").split()
    return " ".join(words[:7]).rstrip(".,!?—-")


def derive_reveal_body(beat: dict) -> str:
    highlights = [w for w in beat.get("highlight_words", []) if w]
    if len(highlights) >= 2:
        return " · ".join(highlights[:4])
    text = beat.get("vo_text", "")
    return re.split(r"(?<=[.!?])\s+", text, maxsplit=1)[0][:180]


def pack_screens(
    script: dict,
    ranges: dict,
    tags_by_beat: dict,
    override_types: dict,
) -> list[dict]:
    screens: list[dict] = []

    for section in script["sections"]:
        sid = section["id"]
        meta = SECTION_META.get(sid, {"heading": sid.title(), "onInk": False})

        # 1) Whole-section layouts collapse everything.
        if sid == "stack":
            beats = section["beats"]
            first_start = ranges[(sid, beats[0]["beat"])][0]
            last_end = ranges[(sid, beats[-1]["beat"])][1]
            reveals = [_make_reveal(sid, b, ranges, tags_by_beat, "schematic") for b in beats]
            screens.append(_make_screen(sid, "schematic", meta, first_start, last_end, reveals,
                                        source=_first_source(beats)))
            continue
        if sid == "cta":
            b = section["beats"][0]
            start, end = ranges[(sid, b["beat"])]
            reveals = [_make_reveal(sid, b, ranges, tags_by_beat, "cta")]
            screens.append(_make_screen(sid, "cta", meta, start, end, reveals,
                                        source=b.get("source")))
            continue

        # 2) Per-beat layout choice, then pack consecutive `sheet` runs.
        pending_sheet: list[dict] | None = None
        section_had_quote = False

        def flush_sheet():
            nonlocal pending_sheet
            if not pending_sheet:
                pending_sheet = None
                return
            beats = pending_sheet
            first_start = ranges[(sid, beats[0]["beat"])][0]
            last_end = ranges[(sid, beats[-1]["beat"])][1]
            reveals = [_make_reveal(sid, b, ranges, tags_by_beat, "sheet") for b in beats]
            screens.append(_make_screen(sid, "sheet", meta, first_start, last_end, reveals,
                                        source=_first_source(beats)))
            pending_sheet = None

        for i, b in enumerate(section["beats"]):
            beat_tags = tags_by_beat.get((sid, b["beat"]), ["claim"])
            override = override_types.get((sid, b["beat"]))
            layout = _pick_layout(
                b, beat_tags, sid,
                is_first_beat_of_section=(i == 0),
                override_type=override,
            )
            # One-quote-per-section throttle.
            if layout == "quote":
                if section_had_quote:
                    layout = "sheet"
                else:
                    section_had_quote = True

            if layout == "sheet":
                if pending_sheet is None:
                    pending_sheet = []
                pending_sheet.append(b)
                continue

            # Break the pending sheet before emitting a stand-alone.
            flush_sheet()

            start, end = ranges[(sid, b["beat"])]
            reveals = [_make_reveal(sid, b, ranges, tags_by_beat, layout)]
            screens.append(_make_screen(sid, layout, meta, start, end, reveals,
                                        source=b.get("source")))

        flush_sheet()

    # 3) Global pass: enforce ≤2 consecutive sheet screens by promoting
    # the middle one to a proof/quote if it has a candidate reveal.
    # (For v2 launch we only warn on this — eval_edit hard-fails, so
    # operators see the issue and refactor the script rather than have
    # the tool silently reshape their argument.)

    # 4) Second-pass: assign per-screen sfx cues + music intensity.
    for i, screen in enumerate(screens):
        screen["sfx"] = _sfx_for_screen(screen)
        screen["music"] = _music_for_screen(screen, prev=screens[i - 1] if i else None)

    # 5) Number screens and assign ids.
    for idx, s in enumerate(screens, start=1):
        s["ordinal"] = idx

    return screens


# ---------------------------------------------------------------------
# Screen / reveal builders
# ---------------------------------------------------------------------

def _make_reveal(sid: str, beat: dict, ranges: dict, tags_by_beat: dict, layout: str) -> dict:
    start, end = ranges[(sid, beat["beat"])]
    hint_body = ""
    hint = beat.get("asset_hint") or ""
    if ":" in hint:
        hint_body = hint.split(":", 1)[1].strip()
    return {
        "beat": beat["beat"],
        "at": start,
        "end": end,
        "title": derive_reveal_title(beat, hint_body or hint, layout),
        "body": derive_reveal_body(beat),
        "tags": tags_by_beat.get((sid, beat["beat"]), ["claim"]),
        "word_anchor": {"start": start, "end": end},
    }


def _make_screen(
    sid: str,
    layout: str,
    meta: dict,
    start: float,
    end: float,
    reveals: list[dict],
    source: str | None = None,
) -> dict:
    figure = None
    # For number-first layouts, surface a figure block. Composition can
    # use `figure.text` as the display copy and `figure.source` as the
    # citation chip content.
    if layout in ("proof_card", "chart", "gap", "ladder"):
        first_rev = reveals[0]
        figure = {"text": first_rev.get("title", ""), "source": source}
    ordinal_id = layout if layout != "sheet" else "sheet"  # temp; ordinal added by caller
    screen_id = f"{sid}-{ordinal_id}"
    return {
        "id": screen_id,  # rewritten below by pack step (ordinal known)
        "section": sid,
        "layout": layout,
        "heading": meta["heading"],
        "start": start,
        "end": end,
        "reveals": reveals,
        "figure": figure,
        "source": source,
    }


def _first_source(beats: list[dict]) -> str | None:
    return next((b.get("source") for b in beats if b.get("source")), None)


# ---------------------------------------------------------------------
# SFX + music cue derivation
# ---------------------------------------------------------------------

def _sfx_for_screen(screen: dict) -> list[dict]:
    """Emit the sfx cue list that the composition renders."""
    cues: list[dict] = []
    layout = screen["layout"]

    # tick on each reveal (except the very first, which lands with the
    # screen-in transition already carrying a whoosh)
    if layout in ("sheet", "schematic"):
        for r in screen["reveals"][1:]:
            cues.append({"cue": "tick", "at": r["at"]})

    # hit on impact frames (once per quote/gap/ladder/proof)
    if layout in ("quote", "gap", "ladder", "proof_card"):
        cues.append({"cue": "hit", "at": screen["start"]})

    # whoosh on section-transition screens
    # (composition adds the section boundary whoosh; we don't dup here.)
    return cues


def _music_for_screen(screen: dict, prev: dict | None) -> dict:
    layout = screen["layout"]
    if layout in SILENCE_LAYOUTS:
        return {"intensity": "silence", "duck_db": 0}
    if layout in BUILD_LAYOUTS:
        return {"intensity": "build", "duck_db": -10}
    return {"intensity": "calm", "duck_db": -16}


# ---------------------------------------------------------------------
# Optional: read assets.json for layout overrides + chart series
# ---------------------------------------------------------------------

def load_asset_overrides(base: Path, script: dict) -> tuple[dict, dict]:
    """Return (override_types, per_beat_asset_spec).

    `override_types` maps (sid, beat) → asset type string when
    assets.json exists; storyboard.py uses this as a hint to steer
    layout picks. `per_beat_asset_spec` copies the beat's full asset
    spec into the script beats (mutating them) so `_extract_series` can
    see chart data.
    """
    asset_path = base / "assets.json"
    if not asset_path.exists():
        return {}, {}
    try:
        assets = json.loads(asset_path.read_text())
    except json.JSONDecodeError:
        return {}, {}
    types: dict = {}
    specs: dict = {}
    for s in assets.get("sections", []):
        for a in s.get("assets", []):
            key = (s["id"], a["beat"])
            spec = a.get("spec") or {}
            types[key] = spec.get("type", "slide")
            specs[key] = spec
    # Attach specs onto script beats so `_pick_layout` can see them.
    for sec in script["sections"]:
        for b in sec["beats"]:
            b["_asset_spec"] = specs.get((sec["id"], b["beat"]))
    return types, specs


# ---------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Plan the storyboard (v2)")
    parser.add_argument("script", help="Path to script.json")
    parser.add_argument("--no-tag-llm", action="store_true",
                        help="Skip the LLM tag pass (heuristic tags only)")
    parser.add_argument("--config", default=str(ROOT / "config" / "blueprint.json"))
    args = parser.parse_args()

    script_path = Path(args.script)
    base = script_path.parent
    script = json.loads(script_path.read_text())
    words = json.loads((base / "vo" / "words.json").read_text())
    timeline = json.loads((base / "vo" / "timeline.json").read_text())
    config = json.loads(Path(args.config).read_text())

    ranges = beat_time_ranges(script, words, timeline)
    override_types, _specs = load_asset_overrides(base, script)

    tags_by_beat = tag_beats(
        script, config,
        cache_path=base / "storyboard-tags.json",
        use_llm=not args.no_tag_llm,
    )

    screens = pack_screens(script, ranges, tags_by_beat, override_types)

    # Re-number screen IDs now that the ordinal is known.
    per_section_counter: dict = {}
    for s in screens:
        per_section_counter[s["section"]] = per_section_counter.get(s["section"], 0) + 1
        s["id"] = f"{s['section']}-{per_section_counter[s['section']]:02d}"
        s.pop("ordinal", None)

    storyboard = {
        "slug": script.get("slug"),
        "total_seconds": timeline["total_seconds"],
        "screens": screens,
    }
    out_path = base / "storyboard.json"
    out_path.write_text(json.dumps(storyboard, indent=2))

    print(f"✓ Storyboard v2 → {out_path}")
    print(f"  {len(screens)} screens over {timeline['total_seconds']:.1f}s "
          f"({timeline['total_seconds'] / max(len(screens), 1):.1f}s/screen avg)")
    for s in screens:
        dur = s["end"] - s["start"]
        rev = len(s["reveals"])
        tag_flat = ",".join(sorted({t for r in s["reveals"] for t in r["tags"]}))
        print(f"    {s['id']:14} {s['layout']:12} {dur:5.1f}s  {rev} reveal(s)"
              f"  music={s['music']['intensity']:7} tags=[{tag_flat}]")


if __name__ == "__main__":
    main()
