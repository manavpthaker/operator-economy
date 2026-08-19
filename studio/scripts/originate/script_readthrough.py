#!/usr/bin/env python3
"""Create a metadata-free narration read-through for human script approval."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


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
        paragraphs = [str(beat.get("vo_text", "")).strip() for beat in section.get("beats", [])]
        paragraphs = [paragraph for paragraph in paragraphs if paragraph]
        count = sum(len(paragraph.split()) for paragraph in paragraphs)
        total += count
        section_id = str(section.get("id", "section"))
        label = "Cold Open" if section_id == "hook" else section_id.replace("_", " ").title()
        sections.append(f"## {label}\n\n*{count} words*\n\n" + "\n\n".join(paragraphs))
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
