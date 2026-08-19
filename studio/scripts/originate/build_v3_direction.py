"""Build a reviewed, tag-only Eleven v3 performance layer."""

import argparse
import json
import re
from pathlib import Path


BEAT_OPENERS = {
    "hook": ["annoyed"],
    "thesis": ["excited", "thoughtful", "annoyed"],
    "evidence": ["curious", "annoyed", "surprised", "curious", "thoughtful", "thoughtful", "surprised"],
    "stack": ["curious", "excited", "thoughtful", "annoyed", "excited"],
    "playbook": ["thoughtful", "curious", "thoughtful", "excited", "thoughtful", "annoyed"],
    "economics": ["thoughtful", "surprised", "annoyed", "thoughtful", "thoughtful"],
    "cta": ["excited"],
}

TURN_TAGS = {
    "More than 60 percent": "surprised",
    "A guest finds the property": "sarcastic",
    "Today, I'll show you": "excited",
    "Sure, the first booking": "thoughtful",
    "But the relationship after": "annoyed",
    "And follow-up happens if somebody remembers": "sarcastic",
    "That's where the operator comes in": "excited",
    "But commission isn't the only cost": "annoyed",
    "In the same report, OTA reservations cancelled": "surprised",
    "That doesn't make the OTA the enemy": "thoughtful",
    "Put a dollar figure": "annoyed",
    "The missed opportunity comes after": "annoyed",
    "They don't need another idea": "annoyed",
    "They need someone with the time": "excited",
    "Mews announced a $300 million": "surprised",
    "That doesn't prove this service": "thoughtful",
    "But software still can't": "annoyed",
    "And now let's turn this one into an offer": "excited",
    "The tools can change": "thoughtful",
    "Your job is to make the handoff work": "excited",
    "The automation remembers": "surprised",
    "You still decide what good hospitality": "thoughtful",
    "But neither one should own": "annoyed",
    "Without it, this is just a pile": "sarcastic",
    "They aren't the promise": "annoyed",
    "Don't send guests toward": "annoyed",
    "More outreach will just show": "sarcastic",
    "And don't pretend a cold automated blast": "annoyed",
    "The blueprint below turns this": "excited",
    "That doesn't mean you should invent": "annoyed",
    "But don't hide behind a dashboard": "annoyed",
    "Don't decorate the report": "sarcastic",
    "It doesn't tell you how much": "thoughtful",
    "Don't present it that way": "annoyed",
    "It isn't a client price": "thoughtful",
    "Price only the subscriptions": "sarcastic",
    "Automate everything without review": "annoyed",
    "And be careful about claiming credit": "thoughtful",
    "The win isn't getting rid": "thoughtful",
    "It's making sure the hotel doesn't": "annoyed",
    "And if you want more practical": "excited",
}


def sentences(text: str) -> list[str]:
    return re.split(r"(?<=[.!?])\s+", text.strip())


def strip_tags(text: str) -> str:
    return re.sub(r"\[[^\]\n]{1,80}\]\s*", "", text)


def normalized(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("script", type=Path)
    ap.add_argument("output", type=Path)
    args = ap.parse_args()
    script = json.loads(args.script.read_text())
    directed, tag_count = {}, 0
    for section in script["sections"]:
        blocks = []
        openers = BEAT_OPENERS[section["id"]]
        if len(openers) != len(section["beats"]):
            raise SystemExit(f"direction plan does not match {section['id']} beat count")
        for beat_index, beat in enumerate(section["beats"]):
            lines = []
            for sentence_index, sentence in enumerate(sentences(beat["vo_text"])):
                tag = next((value for prefix, value in TURN_TAGS.items()
                            if sentence.startswith(prefix)), None)
                if sentence_index == 0:
                    tag = tag or openers[beat_index]
                lines.append(f"[{tag}] {sentence}" if tag else sentence)
                tag_count += bool(tag)
            blocks.append("\n".join(lines))
        text = "\n\n".join(blocks)
        approved = " ".join(b["vo_text"].strip() for b in section["beats"])
        if normalized(strip_tags(text)) != normalized(approved):
            raise SystemExit(f"tagging changed approved words in {section['id']}")
        directed[section["id"]] = text
    payload = {
        "schema_version": "oe-v3-direction-v1",
        "script_revision": script.get("revision"),
        "rule": "Tags and whitespace only; stripping tags must reproduce locked vo_text exactly.",
        "tag_count": tag_count,
        "sections": directed,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2) + "\n")
    print(f"wrote {tag_count} reviewed tags across {len(directed)} sections: {args.output}")


if __name__ == "__main__":
    main()
