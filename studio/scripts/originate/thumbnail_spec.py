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
# Weights sum to 100 and are the honest part to argue about: they encode a
# belief about what makes someone click, inferred from what YouTube surfaces
# on a cold feed. If a dimension is consistently producing concepts that miss,
# that is a wrong weight or a wrong question, and it is now visible.
DIMENSIONS = [
    {
        "key": "hero",
        "name": "Hero figure",
        "weight": 22,
        "extract": "Every number, quantity or hard comparison the script states. "
                   "For each: the value exactly as written, what it measures, and "
                   "which section it appears in.",
        "score": "Is there exactly ONE dominant figure, and is it concrete enough "
                 "to read instantly at browse size? Two competing numbers score 0.",
    },
    {
        "key": "stakes",
        "name": "Stakes to the viewer",
        "weight": 18,
        "extract": "For each number, what it would mean to a viewer who is thinking "
                   "about building this: money they could earn, time they'd lose, a "
                   "risk they're running, or a door closing.",
        "score": "Does the figure imply gain, loss or threat to THIS viewer, rather "
                 "than being neutral market trivia?",
    },
    {
        "key": "complement",
        "name": "Title complementarity",
        "weight": 15,
        "extract": "What the episode title already asserts, and which of the "
                   "episode's facts the title does NOT cover.",
        "score": "Does the thumbnail carry information the title does not? Any word "
                 "or number shared with the title scores 0.",
    },
    {
        "key": "curiosity",
        "name": "Unresolved question",
        "weight": 15,
        "extract": "Questions the episode poses and then answers, and the point in "
                   "the script where each is still open.",
        "score": "Does the image leave a specific question a business viewer cannot "
                 "answer from looking? Fully self-explanatory scores 0.",
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
        "key": "unrepeatable",
        "name": "Episode specificity",
        "weight": 10,
        "extract": "What is true of THIS episode and no other in the series.",
        "score": "Could this exact concept be reused on a different episode? If yes, "
                 "score 0. This is what stops a set collapsing into one look.",
    },
    {
        "key": "legibility",
        "name": "Survives browse size",
        "weight": 8,
        "extract": "(no extraction — a property of the composition, not the episode)",
        "score": "At 120px wide, does the anchor remain identifiable and the overlay "
                 "readable? Busy frames and small faces score low.",
    },
]

ARCHETYPES = {
    "subject-left":  "subject hard left, clean right half",
    "subject-right": "subject hard right, clean left half",
    "object":        "the object itself, no person in frame",
    "two-shot":      "two people, the tension between them",
    "scene-wide":    "the environment is the argument",
}

MODEL_DEFAULT = "claude-sonnet-5"


def anthropic_key() -> str:
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key and (REPO / ".env").exists():
        for line in (REPO / ".env").read_text().splitlines():
            if line.startswith("ANTHROPIC_API_KEY="):
                key = line.split("=", 1)[1].strip()
    if not key:
        raise SystemExit("no ANTHROPIC_API_KEY")
    return key


def ask(system: str, user: str, model: str, max_tokens: int = 6000) -> dict:
    try:
        import anthropic
    except ImportError:
        raise SystemExit("pip install anthropic")
    msg = anthropic.Anthropic(api_key=anthropic_key()).messages.create(
        model=model, max_tokens=max_tokens, system=system,
        messages=[{"role": "user", "content": user}])
    text = "".join(b.text for b in msg.content if b.type == "text").strip()
    text = re.sub(r"^```(?:json)?|```$", "", text, flags=re.M).strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        # max_tokens truncation is the common cause and produces valid-looking
        # JSON that just stops, so say which it was rather than dumping a blob.
        raise SystemExit(
            f"model did not return JSON ({e})\n"
            f"  stop_reason={msg.stop_reason}  output_tokens={msg.usage.output_tokens}"
            f"  max_tokens={max_tokens}\n"
            f"  block types: {[b.type for b in msg.content]}\n"
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
        "- overlay_big: the single hero figure, exactly as the script states it.\n"
        "- overlay_label: 2 to 3 words that INTERPRET that figure, never label it. "
        "\"EVERY MONTH\" not \"REVENUE\". Must share no word with the title.\n"
        "- scene: one paragraph, composition first. Never mention text, writing, "
        "signage, logos, readable screens or branded clothing — image models render "
        "those garbled. Describe surfaces as positively blank. Describe ACTION, never "
        "mood; mood adjectives leak across the frame and produce grim pictures.\n"
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
            f"At least one must be `object` with no person in frame.")
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
