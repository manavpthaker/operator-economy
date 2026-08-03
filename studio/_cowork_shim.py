"""Cowork batch shim for OE originate long calls (script/derive) — runs the
generate_script prompt via the Anthropic Batches API so it survives the 45s
sandbox shell cap. Writes outputs exactly as the original scripts would."""
import os, sys, json, re
from pathlib import Path

STUDIO = Path(__file__).parent

# load studio/.env into environ (scripts assume keys are exported)
for line in (STUDIO / ".env").read_text().splitlines():
    line = line.strip()
    if line and not line.startswith("#") and "=" in line:
        k, v = line.split("=", 1)
        os.environ.setdefault(k, v.strip().strip('"').strip("'"))

sys.path.insert(0, str(STUDIO))
import anthropic
from scripts.originate.generate_script import (
    SYSTEM_PROMPT, SCHEMA_HINT, slugify, build_review_md,
)

CONFIG = json.loads((STUDIO / "config" / "blueprint.json").read_text())
SLUG = "tactical-shift"
OUT = STUDIO / "originate" / SLUG
TOPIC = ("The retention consultancy: selling attrition-insurance to small "
         "companies with a certified assessment and an AI backend")
BATCH_FILE = OUT / ".script_batch_id"


def build_user_prompt():
    sections = []
    for s in CONFIG["format"]["sections"]:
        s = dict(s)
        s["word_budget"] = int(s["target_seconds"] * 2.5)
        sections.append(s)
    sections_spec = json.dumps(sections, indent=2)
    total = sum(s["word_budget"] for s in sections)
    research = (OUT / "content" / "blueprint.md").read_text()
    return f"""Channel positioning: {CONFIG['channel']['positioning']}
Audience: {CONFIG['channel']['audience']}
Tone: {CONFIG['channel']['tone']}
Target duration: {CONFIG['format']['target_duration_minutes']} minutes ≈ {total} spoken words TOTAL.

Section structure. Each section has a word_budget — the sum of that section's beat
vo_text word counts MUST land within ±20% of it. Add more beats rather than longer
sentences to hit budget. This is a hard requirement; short sections fail QA:
{sections_spec}

Topic: {TOPIC}

Research brief:
{research}

{SCHEMA_HINT}"""


def submit():
    client = anthropic.Anthropic()
    up = build_user_prompt()
    batch = client.messages.batches.create(requests=[{
        "custom_id": "script",
        "params": {
            "model": CONFIG["models"]["script"],
            "max_tokens": 8000,
            "system": SYSTEM_PROMPT,
            "messages": [{"role": "user", "content": up}],
            "thinking": {"type": "disabled"},
        },
    }])
    BATCH_FILE.write_text(batch.id)
    print("SUBMITTED", batch.id, batch.processing_status)


def poll():
    client = anthropic.Anthropic()
    bid = BATCH_FILE.read_text().strip()
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
        script["slug"] = SLUG
        (OUT / "script.json").write_text(json.dumps(script, indent=2))
        (OUT / "script_review.md").write_text(build_review_md(script))
        pov = sum(1 for s in script.get("sections", [])
                  for be in s.get("beats", []) if "[POV:" in be.get("vo_text", ""))
        words = sum(len(be.get("vo_text", "").split()) for s in script.get("sections", [])
                    for be in s.get("beats", []))
        print(f"WROTE script.json | sections={len(script.get('sections', []))} "
              f"words~{words} POV_tokens={pov}")
        print("TITLES:", " | ".join(script.get("title_options", [])))


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "submit"
    {"submit": submit, "poll": poll}[cmd]()
