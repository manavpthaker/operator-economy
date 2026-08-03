"""Cowork batch shim (generalized) for `originate.py new`.

generate_script.py makes one 8K-token call that exceeds Cowork's 45s shell cap.
This submits the IDENTICAL prompt via the Anthropic Batches API and writes
script.json / script_review.md exactly as generate_script.py would, so the
downstream evals (eval_script, eval_package, confidence) see no difference.

Supersedes the hardcoded _cowork_shim.py (tactical-shift only).

    python _cowork_script_batch.py submit --topic "..." --research path/to/brief.md
    python _cowork_script_batch.py poll   --topic "..."

`thinking: disabled` is required — claude-sonnet-5 otherwise spends the whole
max_tokens budget on thinking in batch mode and returns no content.
"""
import os
import sys
import json
import re
import argparse
from pathlib import Path

STUDIO = Path(__file__).parent

# load studio/.env into environ (the pipeline scripts assume exported keys)
for line in (STUDIO / ".env").read_text().splitlines():
    line = line.strip()
    if line and not line.startswith("#") and "=" in line:
        k, v = line.split("=", 1)
        os.environ.setdefault(k, v.strip().strip('"').strip("'"))

sys.path.insert(0, str(STUDIO))
import anthropic  # noqa: E402
from scripts.originate.generate_script import (  # noqa: E402
    SYSTEM_PROMPT, SCHEMA_HINT, slugify, build_review_md,
)

CONFIG = json.loads((STUDIO / "config" / "blueprint.json").read_text())


def paths(topic: str):
    slug = slugify(topic)
    out = STUDIO / "originate" / slug
    return slug, out, out / ".script_batch_id"


def build_user_prompt(topic: str, research_path: str) -> str:
    """Byte-identical to generate_script.py's user_prompt construction."""
    sections = []
    for s in CONFIG["format"]["sections"]:
        s = dict(s)
        s["word_budget"] = int(s["target_seconds"] * 2.5)
        sections.append(s)
    sections_spec = json.dumps(sections, indent=2)
    total_words = sum(s["word_budget"] for s in sections)
    research = Path(research_path).read_text() if research_path else ""
    return f"""Channel positioning: {CONFIG['channel']['positioning']}
Audience: {CONFIG['channel']['audience']}
Tone: {CONFIG['channel']['tone']}
Target duration: {CONFIG['format']['target_duration_minutes']} minutes ≈ {total_words} spoken words TOTAL.

Section structure. Each section has a word_budget — the sum of that section's beat
vo_text word counts MUST land within ±20% of it. Add more beats rather than longer
sentences to hit budget. This is a hard requirement; short sections fail QA:
{sections_spec}

Topic: {topic}

Research brief:
{research if research else '(none provided — be conservative, mark everything as estimate)'}

{SCHEMA_HINT}"""


def submit(args):
    slug, out, batch_file = paths(args.topic)
    out.mkdir(parents=True, exist_ok=True)
    client = anthropic.Anthropic()
    batch = client.messages.batches.create(requests=[{
        "custom_id": "script",
        "params": {
            "model": CONFIG["models"]["script"],
            "max_tokens": 8000,
            "system": SYSTEM_PROMPT,
            "messages": [{"role": "user", "content": build_user_prompt(args.topic, args.research)}],
            "thinking": {"type": "disabled"},
        },
    }])
    batch_file.write_text(batch.id)
    print(f"SUBMITTED {batch.id} {batch.processing_status} slug={slug}")


def poll(args):
    slug, out, batch_file = paths(args.topic)
    client = anthropic.Anthropic()
    bid = batch_file.read_text().strip()
    b = client.messages.batches.retrieve(bid)
    print("STATUS", b.processing_status, dict(b.request_counts))
    if b.processing_status != "ended":
        return
    for r in client.messages.batches.results(bid):
        if r.result.type != "succeeded":
            print("RESULT_NOT_OK", r.result.type, getattr(r.result, "error", ""))
            return
        text = r.result.message.content[0].text.strip()
        text = re.sub(r"^```(json)?|```$", "", text, flags=re.MULTILINE).strip()
        script = json.loads(text)
        script["slug"] = slug
        (out / "script.json").write_text(json.dumps(script, indent=2))
        (out / "script_review.md").write_text(build_review_md(script))
        pov = sum(1 for s in script.get("sections", [])
                  for be in s.get("beats", []) if "[POV:" in be.get("vo_text", ""))
        words = sum(len(be.get("vo_text", "").split()) for s in script.get("sections", [])
                    for be in s.get("beats", []))
        print(f"WROTE {out/'script.json'} | sections={len(script.get('sections', []))} "
              f"words~{words} POV_tokens={pov}")
        print("TITLES:", " | ".join(script.get("title_options", [])))


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("command", choices=["submit", "poll"])
    p.add_argument("--topic", required=True)
    p.add_argument("--research")
    a = p.parse_args()
    {"submit": submit, "poll": poll}[a.command](a)
