#!/usr/bin/env python3
"""
Originate: run the thumbnail rubric FORWARD — episode in, scored specs out.

Supersedes derive_thumbnail_prompt.py, which asked a model for "concepts" with
the rubric as advisory prose in a system prompt. That is not an algorithm; the
rubric only ever judged the result afterwards, so a rejection told us nothing
about which part was wrong and the next attempt was another guess. Eight
rounds went that way.

Here the rubric is a single data structure used in both directions:

    DIMENSIONS  ──generates──▶  what to extract from the episode
                └──scores────▶  how a candidate spec is judged

Because both directions come from one definition, adding or reweighting a
dimension changes generation and scoring together, and every part of a concept
is attributable to the dimension that produced it. A concept that fails is a
dimension that failed, and you can point at it.

Three stages, each written to disk so it can be inspected on its own:

  1. inventory  the episode's raw material, extracted per dimension
                (numbers with stakes, unresolved tensions, subjects, objects)
  2. specs      candidate concepts assembled from that inventory, each scored
                per dimension with a written reason. NO IMAGE IS GENERATED.
  3. prompts    the top specs rendered into image prompts + overlay text

Stage 2 is the point: it is the cheap gate. Read the scores, fix the rubric or
the selection, and only then spend a generation.

    thumbnail_spec.py originate/<slug>/script.json [--n 4] [--stage all]

Writes render_data/thumbnail_{inventory,specs}.json.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REPO = ROOT.parent

# ── The rubric. One definition, used to generate and to score. ───────────────
#
# `extract` is the question asked of the EPISODE (stage 1).
# `score`   is the question asked of a CANDIDATE (stage 2).
#
# Re-weighted 2026-08-11 against measurement, not belief. The previous comment
# here admitted the weights encoded "a belief about what makes someone click,
# inferred from what YouTube surfaces on a cold feed." They now come from 221
# comp-set videos banded within channel (research/thumbnails/findings.md) and
# from reading all 78 top/bottom-quartile thumbnails at reading size and at
# 120px browse width (research/thumbnails/visual-findings.md). Amendment A8 in
# docs/thumbnail-rubric.md records what moved and why.
#
# What the measurement is and is not: views banded within channel, so it
# controls for subscriber base but cannot separate packaging from topic demand,
# and views are not CTR. The results below are trustworthy where they are
# NEGATIVE — a feature that fails to discriminate between a channel's own best
# and worst videos is not carrying the weight a rubric assigns it. They are
# weaker where they are positive. Weighted accordingly: the two largest
# dimensions are the ones that survived a negative test, and nothing here is
# weighted on a single expert's teaching.
DIMENSIONS = [
    {
        "key": "recognisable",
        "name": "Recognisable subject",
        "weight": 25,
        "extract": "Companies, products, trades, places and everyday objects the "
                   "script names. For each, say whether a stranger would recognise "
                   "it with no explanation (household name), only inside the "
                   "industry, or not at all. Include what is physically handled or "
                   "made, not just what is discussed.",
        "score": "Would a cold viewer know what this is about without reading a "
                 "word? A household-name brand, a familiar trade, or an everyday "
                 "physical object scores high. An abstract concept, an unfamiliar "
                 "company name, or a category noun scores 0. This is the largest "
                 "measured effect in the comp set: identical title grammar, 15x "
                 "apart on whether the subject was Crumbl Cookies or OpenAI.",
    },
    {
        "key": "legibility",
        "name": "One focal mass at 120px",
        "weight": 15,
        "extract": "(no extraction — a property of the composition, not the episode)",
        "score": "Count the elements a viewer must resolve SEPARATELY to get the "
                 "point. One scores full, two scores half, three or more scores 0. "
                 "A comparison, a logo row, a map with markers, or a diagram as the "
                 "subject scores 0 however good it looks at full size — five such "
                 "compositions appear in the comp set and all five are bottom "
                 "quartile. Texture that is not meant to be read is not an element.",
    },
    {
        "key": "curiosity",
        "name": "Unresolved verdict",
        "weight": 15,
        "extract": "Judgements the episode reaches about its subject, and the point "
                   "in the script where each is still open. Prefer the ones that "
                   "sound like a conclusion but do not explain themselves.",
        "score": "Does the frame state or imply a VERDICT the viewer cannot resolve "
                 "by looking, and would want to? The register lane's entire top "
                 "quartile is this and nothing else — a flat editorial judgement "
                 "over a press photo. Neutral description scores 0.",
    },
    {
        "key": "subject",
        "name": "Human or object anchor",
        "weight": 12,
        "extract": "People the script names or implies and what they are DOING, plus "
                   "physical objects or metaphors the script uses that are specific "
                   "to this episode.",
        "score": "Is there one clear anchor, either a person mid-action or a single "
                 "distinctive object? A generic desk or laptop scores 0.",
    },
    {
        "key": "credible",
        "name": "Believable figure",
        "weight": 12,
        "extract": "Every number the script states, with the unit it is stated in "
                   "and the smallest honest unit it could be restated in (a yearly "
                   "figure also expressed monthly, a total also expressed per job).",
        "score": "If the concept carries a figure, is it one a sceptical operator "
                 "would believe without proof, in the smallest honest unit? "
                 "Believable beat big by 4.9x and 18.8x in the comp set, and the "
                 "worst video in its own channel sample carried the biggest number. "
                 "An implausible headline figure scores 0. CARRYING NO FIGURE AT ALL "
                 "SCORES FULL: no top-quartile thumbnail in our register lane has "
                 "one, and absence is not a defect.",
    },
    {
        "key": "stakes",
        "name": "Stakes to the viewer",
        "weight": 11,
        "extract": "For each fact, what it would mean to a viewer who is thinking "
                   "about building this: money they could earn, time they'd lose, a "
                   "risk they're running, or a door closing.",
        "score": "Does the concept imply gain, loss or threat to THIS viewer, rather "
                 "than being neutral market trivia?",
    },
    {
        "key": "reexpress",
        "name": "Splits the work with the title",
        "weight": 10,
        "extract": "What the episode title asserts, and which of the episode's facts "
                   "the title does NOT cover.",
        "score": "Does the thumbnail carry the CONSEQUENCE or verdict while the "
                 "title carries the subject and mechanism — or restate the title's "
                 "own fact in a more believable unit ($1M a year in the title, "
                 "$91,000 per month on the image)? Repeating the title's claim in "
                 "the title's own terms scores 0. Sharing a subject word with the "
                 "title is NOT a penalty: the comp set's winners do it constantly.",
    },
]

# Retired 2026-08-11, both to 0 points, both recorded in amendment A8:
#
#   hero (was 22, the largest weight) — "exactly ONE dominant figure". Zero of
#   the twenty top-quartile thumbnails in our own register lane carry a hero
#   number; four of the twenty bottom-quartile ones do. In the direct-comp lane
#   the figure appears in both bands at the same rate. It was the rubric's
#   biggest weight and it scored a feature no winner in our register exhibits.
#   Its one defensible part — never two competing figures — is now enforced by
#   `legibility`, which scores any comparison 0 on element count.
#
#   unrepeatable (was 10) — "could this be reused on another episode? If yes,
#   score 0." Every channel in the comp set reuses its concept every week by
#   design; Modern MBA runs THE ECONOMICS OF ___ across five of its seven best.
#   Consistency is the recognisability asset and the dimension scored it as a
#   defect. The SUBJECT must be episode-specific — that is now inside
#   `recognisable` — and the FORMAT should repeat.

# Derived from what the comp set's top quartiles actually do, replacing five
# purely compositional slots. `two-shot` is gone: a two-person frame is a
# comparison, and comparisons are a bottom-quartile pattern in every lane.
#
# `product` is the narrowed survivor of what was briefly `one-logo`. The comp
# evidence is unambiguous that ONE recognisable mark at scale is the strongest
# pattern in the set — it is MagnatesMedia's entire top quartile and the best
# survivor of the 120px shrink. It is also unreachable from here: the scene
# constraint forbids naming logos because image models garble them, so across
# nine episodes the archetype degraded two ways. Twice it emitted an
# ungeneratable instruction ("a single Zapier mark centered on a clean neutral
# background"); twice it emitted a generic gradient app-icon blob, which is the
# stock-AI imagery thumbnail-rubric.md rejects outright. Once it produced
# something real — a plain iPhone — because a manufactured PRODUCT is
# generatable and a trademark is not.
#
# So the archetype is narrowed to the generatable half. Reaching the actual
# comp-set pattern needs a real mark composited over a generated ground, which
# is a pipeline that does not exist; recorded as a gap in A8 rather than left
# as an archetype that quietly emits things nothing can render.
# `flatlay` is a TREATMENT, not a camera. The name is historical and is kept
# because nine episodes' props, assign_shots.py and prepare_longform.py all key
# on `thumb-flatlay.json`; read it as "crowded working surface".
#
# It used to say "overhead flat-lay ... hands entering from the bottom edge",
# which baked the camera into the scene text. That made --shot unusable: the
# scene said overhead, the shot constraint said low-raking, and the two fought
# inside one prompt. Every flatlay ground came back overhead however the shot
# was set, which read as one photograph with the props swapped.
#
# The treatment is the density, the overlap, the informality and the human
# presence. The camera is a separate axis, chosen ACROSS the set by
# assign_shots.py and passed to generate_scene.py as --shot.
ARCHETYPES = {
    "flatlay":      "the crowded working surface itself, objects dense to all "
                    "four frame edges and overlapping, hands present in the "
                    "frame mid-action — the house layout, see "
                    "docs/thumbnail-design-language.md. Do NOT state the camera "
                    "position, the angle, or where hands enter from: the shot is "
                    "chosen separately and your scene must read correctly from "
                    "any of them",
    "verdict":      "documentary photograph, editorial verdict in condensed caps "
                    "across the top third, no number anywhere",
    "product":      "a single mass-market manufactured product or machine at "
                    "scale, unbranded and shown plainly, no person",
    "object":       "the physical object of the trade filling the frame, no person",
    "practitioner": "one person mid-action in the real workplace, close crop, "
                    "clean half of the frame left for the overlay",
    "scene-wide":   "the working environment is the argument",
}

MODEL_DEFAULT = "claude-sonnet-5"


try:
    from _model import complete, ModelError
except ImportError:  # imported as part of the scripts.originate package
    from ._model import complete, ModelError


def ask(system: str, user: str, model: str, max_tokens: int = 6000) -> dict:
    """Model text -> parsed JSON. Routing lives in _model.complete()."""
    try:
        text = complete(system, user, model, max_tokens=max_tokens)
    except ModelError as e:
        raise SystemExit(str(e))
    text = re.sub(r"^```(?:json)?|```$", "", text, flags=re.M).strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        # Truncation is the common cause and produces valid-looking JSON that
        # just stops, so say so rather than dumping a blob.
        raise SystemExit(
            f"model did not return JSON ({e})\n"
            f"  max_tokens={max_tokens} — truncation is the usual cause\n"
            f"  text[:600]: {text[:600]!r}")


def episode_text(s: dict) -> str:
    parts = [f"TITLE OPTIONS: {json.dumps(s.get('title_options', []))}"]
    for sec in s.get("sections", []):
        beats = " ".join(b.get("vo_text") or b.get("text") or ""
                         for b in sec.get("beats", []))
        if beats.strip():
            parts.append(f"\n[{sec.get('id', '?').upper()}]\n{beats.strip()}")
    return "\n".join(parts)


# ── Stage 1 ─────────────────────────────────────────────────────────────────
def build_inventory(script: dict, model: str) -> dict:
    fields = "\n".join(
        f"  \"{d['key']}\": // {d['extract']}" for d in DIMENSIONS
        if not d["extract"].startswith("(no extraction"))
    system = (
        "You extract raw material from a video script so thumbnail concepts can be "
        "assembled from it later. You do not design anything yet and you invent "
        "nothing: every item must be traceable to a line in the script. Numbers are "
        "quoted exactly as the script states them.\n\n"
        "Return STRICT JSON, no prose, no code fence, with one key per field:\n{\n"
        + fields + "\n}\n"
        "Each field is an array of objects. Every object carries a \"quote\" field "
        "identifying the script line it came from, trimmed to at most 15 words — "
        "enough to find the line, not the whole sentence.\n"
        "At most 8 items per field: the strongest ones, not everything you can find. "
        "Be terse. This is raw material for a later step, not a report.")
    return ask(system, f"Script:\n\n{episode_text(script)}", model, max_tokens=16000)


# ── Stage 2 ─────────────────────────────────────────────────────────────────
def build_specs(inventory: dict, script: dict, n: int, model: str) -> dict:
    rubric = "\n".join(
        f"  {d['key']} ({d['weight']} pts) — {d['name']}: {d['score']}"
        for d in DIMENSIONS)
    arche = "\n".join(f"  {k}: {v}" for k, v in ARCHETYPES.items())
    system = (
        "You assemble thumbnail concepts for The Operator Economy from a pre-extracted "
        "inventory, then score each against the rubric that generated that inventory. "
        "Register is documentary and analytical: no hype, no shock, no exclamation.\n\n"
        f"RUBRIC (100 points):\n{rubric}\n\n"
        f"ARCHETYPES — every concept picks one, and no two concepts may share one:\n{arche}\n\n"
        "Constraints on the output:\n"
        "- overlay_big: the thumbnail's dominant words. A FIGURE IS OPTIONAL AND "
        "USUALLY WRONG — no top-quartile thumbnail in this register carries one. "
        "Prefer a flat editorial verdict of one to four words that sounds like a "
        "conclusion and does not explain itself. If you do use a figure, exactly "
        "one, quoted as the script states it, in the smallest honest unit.\n"
        "- overlay_label: 0 to 3 words. Omit it entirely unless it changes the "
        "meaning of overlay_big — an empty string is a valid and often better "
        "answer. When present it INTERPRETS, never names: \"EVERY MONTH\" not "
        "\"REVENUE\". It may share a subject word with the title; it may not "
        "restate the title's claim in the title's own terms.\n"
        "- NEVER two figures, two panels, a before/after, a versus, or a row of "
        "several marks. Every such composition in the comp set is bottom quartile. "
        "One focal mass, and it must still be one at 120px wide.\n"
        "- scene: one paragraph, composition first. Never mention text, writing, "
        "signage, logos, readable screens or branded clothing — image models render "
        "those garbled. Describe surfaces as positively blank. Describe ACTION, never "
        "mood; mood adjectives leak across the frame and produce grim pictures.\n"
        "- No invented icon, glyph, app-tile or abstract emblem, and no gradient "
        "fills. Asked for a recognisable thing you cannot name, describe a REAL "
        "manufactured object plainly instead — an iPhone, a card reader, a barber "
        "chair. A rounded square in a teal-to-purple gradient is the stock-AI "
        "imagery this brand rejects, not a substitute for a mark.\n"
        "- Nobody sad, defeated, or posed smiling at a laptop.\n\n"
        "Score honestly. A concept you assembled scoring 40 is more useful than "
        "flattery. Give each dimension its score, out of that dimension's weight, "
        "with one sentence of reasoning.\n\n"
        "Return STRICT JSON, no prose, no code fence:\n"
        "{\"specs\":[{\"archetype\":\"\",\"overlay_big\":\"\",\"overlay_label\":\"\","
        "\"scene\":\"\",\"source_quote\":\"\",\"scores\":{\"<dimension key>\":"
        "{\"score\":0,\"why\":\"\"}},\"total\":0}]}")
    user = (f"Title options: {json.dumps(script.get('title_options', []))}\n\n"
            f"Inventory:\n{json.dumps(inventory, indent=2)}\n\n"
            f"Assemble exactly {n} concepts, each a different archetype. "
            f"One MUST be `flatlay` — it is the house layout and satisfies the "
            f"density, human-presence and scatter invariants by construction. "
            f"At least one must be `verdict` and at least one must be `object`, "
            f"so each set tests a different hypothesis rather than three "
            f"near-identical files (amendment A5).\n\n"
            f"For the `flatlay` concept: THE SURFACE BELONGS TO THE CUSTOMER'S "
            f"BUSINESS, NOT THE OPERATOR'S OFFICE. This is the rule that matters "
            f"and it keeps getting broken. Every episode returns some view of a "
            f"desk, because the operator works at a desk — and "
            f"nine desks is one photograph with the props swapped. The operator "
            f"is invisible in this channel anyway; what the viewer recognises is "
            f"the BUSINESS BEING SERVED. Name that business from the script's own "
            f"evidence — the florist, the plumber, the barbershop, the clinic, "
            f"the restaurant, the hotel front desk — and set the frame on ITS "
            f"working surface: the counter beside the till, the van floor, the "
            f"stainless kitchen pass, the reception ledge, the workshop bench. "
            f"Do not write the word desk unless the episode is literally about "
            f"office work. Then the SPECIFIC objects that business handles — its "
            f"dockets, parts, stock, order pads, tools — crowded to every edge "
            f"and overlapping, with hands in frame. Leave bare patches of surface "
            f"between them; the episode's real tool marks are composited into "
            f"those patches afterwards. Do not describe the camera: the framing "
            f"is chosen downstream.")
    return ask(system, user, model, max_tokens=16000)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("script", type=Path)
    ap.add_argument("--n", type=int, default=4)
    ap.add_argument("--model", default=MODEL_DEFAULT)
    ap.add_argument("--stage", choices=["inventory", "specs", "all"], default="all")
    a = ap.parse_args()

    script = json.loads(a.script.read_text())
    rd = a.script.parent / "render_data"
    rd.mkdir(parents=True, exist_ok=True)
    inv_p, spec_p = rd / "thumbnail_inventory.json", rd / "thumbnail_specs.json"

    if a.stage in ("inventory", "all"):
        inv = build_inventory(script, a.model)
        inv_p.write_text(json.dumps(inv, indent=2))
        print(f"inventory → {inv_p.name}")
        for k, v in inv.items():
            print(f"  {k:14s} {len(v) if isinstance(v, list) else '?'} items")
        if a.stage == "inventory":
            return 0
    else:
        inv = json.loads(inv_p.read_text())

    specs = build_specs(inv, script, a.n, a.model)
    spec_p.write_text(json.dumps(specs, indent=2))

    print(f"\nspecs → {spec_p.name}   (no images generated)\n")
    ranked = sorted(specs.get("specs", []), key=lambda s: -s.get("total", 0))
    for s in ranked:
        print(f"  {s.get('total', 0):>3}/100  [{s.get('archetype')}]  "
              f"{s.get('overlay_big')} / {s.get('overlay_label')}")
        worst = sorted(s.get("scores", {}).items(),
                       key=lambda kv: kv[1].get("score", 0) /
                       max(next((d['weight'] for d in DIMENSIONS if d['key'] == kv[0]), 1), 1))[:2]
        for k, v in worst:
            print(f"           weakest {k}: {v.get('score')} — {v.get('why', '')[:70]}")
    print("\nRead the scores before generating. A low dimension is a fixable "
          "defect, not a verdict.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
