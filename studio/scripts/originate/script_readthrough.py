#!/usr/bin/env python3
"""Create a metadata-free narration read-through for human script approval."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def spoken_lines(text: str) -> str:
    """Display one spoken thought per line without changing canonical VO text."""
    sentences = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9$])", text.strip())
    # Markdown's backslash hard-break keeps the source clean while rendering
    # each breath on its own line in GitHub and local previewers.
    return "\\\n".join(sentence.strip() for sentence in sentences if sentence.strip())


def block(label: str, beats: list[dict]) -> tuple[str, int]:
    texts = [str(beat.get("vo_text", "")).strip() for beat in beats]
    texts = [text for text in texts if text]
    count = sum(len(text.split()) for text in texts)
    performed = "\n\n".join(spoken_lines(text) for text in texts)
    return f"## {label}\n\n*{count} words*\n\n{performed}", count


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("script")
    ap.add_argument("--out")
    args = ap.parse_args()
    source = Path(args.script)
    data = json.loads(source.read_text())
    out = Path(args.out) if args.out else source.with_name("SCRIPT-READTHROUGH.md")
    title = data.get("working_title") or data.get("topic") or source.parent.name
    sections = []
    total = 0
    for section in data.get("sections", []):
        section_id = str(section.get("id", "section"))
        beats = section.get("beats", [])
        if section_id == "thesis" and beats:
            # The first thesis beat is the post-ident show introduction. Keep
            # its production section ID for VO/render compatibility, but show
            # it separately to the performer and reviewer.
            intro, intro_count = block("Show Intro", beats[:1])
            thesis, thesis_count = block("Thesis", beats[1:])
            sections.extend([intro, thesis])
            total += intro_count + thesis_count
            continue
        label = "Cold Open" if section_id == "hook" else section_id.replace("_", " ").title()
        rendered, count = block(label, beats)
        sections.append(rendered)
        total += count
    document = (
        f"# {title}\n\n"
        f"> Script review copy · `{data.get('revision', 'unversioned')}` · {total} words. "
        "Edit narration here conceptually; `script.json` remains canonical until approval.\n\n"
        + "\n\n".join(sections)
        + "\n"
    )
    out.write_text(document)
    print(f"Script read-through → {out} ({total} words)")


if __name__ == "__main__":
    main()
