"""Initialize and gate the per-episode Rev D score brief."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


APPROVED = {"candidate_selected", "approved", "arranged"}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("command", choices=("init", "check"))
    ap.add_argument("script")
    args = ap.parse_args()
    script_path = Path(args.script)
    episode = script_path.parent
    brief_path = episode / "music_brief.json"
    script = json.loads(script_path.read_text())
    storyboard_path = episode / "storyboard.json"
    storyboard = json.loads(storyboard_path.read_text()) if storyboard_path.exists() else {}
    if args.command == "init":
        if brief_path.exists():
            print(f"Keeping existing {brief_path}")
            return
        states = []
        for screen in storyboard.get("screens", []):
            state = screen.get("score_state")
            if state and state not in states:
                states.append(state)
        brief = {
            "episode": script.get("slug", episode.name),
            "title": script.get("working_title", script.get("topic", episode.name)),
            "project": "Operator Economy",
            "flow_session": None,
            "lane": "select_for_episode",
            "instrumental": True,
            "score_states": states or ["human", "constraint", "tension", "silence", "counter", "build", "resolve"],
            "edit_contract": [
                "Leave clean space for the fixed OE sting.",
                "Create audible edit points around the narrative-state transitions.",
                "Keep narration intelligible; silence is an authored state.",
                "Generate and review at least two genuinely different candidates."
            ],
            "candidates": [],
            "selected_candidate": None,
            "status": "brief_pending"
        }
        brief_path.write_text(json.dumps(brief, indent=2) + "\n")
        print(f"Music brief → {brief_path}")
        return
    if not brief_path.exists():
        raise SystemExit(f"MUSIC GATE: BLOCKED\n- missing {brief_path.name}; run music_brief.py init")
    brief = json.loads(brief_path.read_text())
    if brief.get("status") not in APPROVED or not brief.get("selected_candidate"):
        raise SystemExit("MUSIC GATE: BLOCKED\n- generate candidates in the Operator Economy Flow project, review them, then set selected_candidate and status=candidate_selected")
    print(f"Music gate passed: {brief['selected_candidate']}")


if __name__ == "__main__":
    main()
