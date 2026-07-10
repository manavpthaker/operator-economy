#!/usr/bin/env python3
"""
Viddy Originate — topic to long-form blueprint video (plus LinkedIn/
Grapevines derivatives). Companion to pipeline.py, which derives shorts
from existing recordings; this mode ORIGINATES content from research.

Three gates, ~60-90 min of human time per video:
  Gate 1: POV pass on the script (required — monetization compliance)
  Gate 2: asset plan approval + screen recordings
  Gate 3: render preview before publish

Usage:
    # Phase 1 — script (stops at Gate 1)
    python originate.py new "AI receptionists for hotels" --research notes.md

    # Phase 2 — after editing script.json: VO + asset plan (stops at Gate 2)
    python originate.py continue originate/<slug>

    # Phase 3 — render data + derived content (LI posts, newsletter, blueprint)
    python originate.py render originate/<slug>

    # Then render video via Remotion:
    #   cd remotion && npx remotion render src/index.ts Blueprint out/<slug>.mp4 \
    #       --props=../originate/<slug>/render_data/blueprint.json
    # And cut shorts from the rendered long-form with the standard pipeline:
    #   python pipeline.py output/<slug>.mp4
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent
SCRIPTS = ROOT / "scripts" / "originate"


def run_step(script: str, args: list[str], step_name: str) -> None:
    print(f"\n{'='*60}\n  ORIGINATE: {step_name}\n{'='*60}\n")
    rc = subprocess.run([sys.executable, str(SCRIPTS / script)] + args).returncode
    if rc != 0:
        print(f"{step_name} failed.", file=sys.stderr)
        sys.exit(rc)


def resolve_dir(path_str: str) -> Path:
    p = Path(path_str)
    if not p.exists():
        p = ROOT / "originate" / path_str  # allow bare slug
    if not (p / "script.json").exists():
        print(f"Error: no script.json in {p}", file=sys.stderr)
        sys.exit(1)
    return p


def main():
    parser = argparse.ArgumentParser(description="Viddy Originate — blueprint video pipeline")
    sub = parser.add_subparsers(dest="command", required=True)

    p_new = sub.add_parser("new", help="Generate script from topic (stops at Gate 1)")
    p_new.add_argument("topic")
    p_new.add_argument("--research", help="Research brief file (md/txt)")

    p_cont = sub.add_parser("continue", help="After Gate 1: VO + asset plan (stops at Gate 2)")
    p_cont.add_argument("dir", help="originate/<slug> or bare slug")

    p_rend = sub.add_parser("render", help="After Gate 2: render data + derived content")
    p_rend.add_argument("dir", help="originate/<slug> or bare slug")
    p_rend.add_argument("--skip-derive", action="store_true", help="Skip LinkedIn/newsletter derivation")

    args = parser.parse_args()

    if args.command == "new":
        step_args = [args.topic]
        if args.research:
            step_args += ["--research", args.research]
        run_step("generate_script.py", step_args, "Generate Script")
        # Auto-eval the fresh draft (POV tokens expected at this stage)
        from scripts.originate.generate_script import slugify  # reuse slug logic
        draft = ROOT / "originate" / slugify(args.topic) / "script.json"
        if draft.exists():
            run_step("eval_script.py", [str(draft), "--mode", "draft"], "Gate 1 Evals (draft)")
            run_step("eval_package.py", [str(draft)], "Craft Rubric (draft)")
            # Confidence verdict: AUTO-PASS → orchestrating agent may proceed
            # without operator review; ESCALATE (exit 2) → notify operator.
            subprocess.run([sys.executable, str(SCRIPTS / "confidence.py"),
                            str(draft), "--stage", "script"])

    elif args.command == "continue":
        d = resolve_dir(args.dir)
        script = str(d / "script.json")
        # Hard gate: rigor evals (zero POV tokens) + craft rubric kill-list
        run_step("eval_script.py", [script, "--mode", "approved"], "Gate 1 Evals (approved)")
        run_step("eval_package.py", [script], "Craft Rubric (kill-list gate)")
        run_step("generate_vo.py", [script], "Generate Voiceover")
        # Avatar corner-block clips (HeyGen digital twin, lip-synced to the
        # section VO). No-ops unless config avatar.enabled; resumable per
        # section. See docs/avatar-decision.md.
        run_step("generate_avatar.py", [script], "Generate Avatar Clips")
        # HeyGen-voice avatar sections replace their vo/ caches (the clip
        # audio IS the section voice) — reassemble words.json/timeline.json
        # from the caches before anything downstream reads timings. All
        # sections are cached at this point, so this is a fast no-API pass.
        run_step("generate_vo.py", [script], "Reassemble VO Timeline")
        run_step("plan_assets.py", [script], "Plan Assets")
        # Storyboard: plan the SCREENS from real VO timings so downstream
        # (prepare_longform + Remotion) can consume one persistent screen
        # per coherent stretch of argument instead of one per talking
        # point. See docs/storyboard-stage.md for the full spec + rules.
        # Runs after plan_assets during the transitional migration so it
        # can pick up authoritative asset types; storyboard.py is
        # order-agnostic and will fall back to script.json's asset_hint
        # once plan_assets is rewritten to consume storyboard.json.
        run_step("storyboard.py", [script], "Plan Storyboard")
        run_step("eval_storyboard.py", [script], "Storyboard Pacing Evals")
        # Edit rubric §VII — pre-render check that the storyboard has the
        # scene grammar + cadence the finished video needs. Escalates if
        # <16/20 or any kill-list hit (unresolved placeholder, abstract
        # b-roll, unsourced money claim, sheet-run > 2, static hold > 45s).
        run_step("eval_edit.py", [script], "Edit Rubric §VII")
        print("\nGATE 2: review assets_review.md + edit_review.md, record screen_recs,"
              " then: originate.py render <slug>")

    elif args.command == "render":
        d = resolve_dir(args.dir)
        script = str(d / "script.json")
        run_step("prepare_longform.py", [script], "Prepare Render Data")
        # Re-run the edit rubric now that assets are finalized (heading,
        # sources may have shifted). This is the pre-render check that
        # matches the docs/pipeline.md loudness step run POST-render.
        run_step("eval_edit.py", [script], "Edit Rubric §VII (pre-render)")
        if not args.skip_derive:
            run_step("derive_content.py", [script], "Derive LinkedIn/Grapevines Content")
            # Re-run craft evals now that shorts_briefs.json exists (cliffhanger/pin gate)
            run_step("eval_package.py", [script], "Craft Rubric (incl. Shorts checks)")
            # Pre-publish confidence: decides whether the episode library
            # (video + shorts + posts + newsletter + blueprint) requires
            # operator review or auto-advances to publish.
            subprocess.run([sys.executable, str(SCRIPTS / "confidence.py"),
                            script, "--stage", "prepublish"])
        props = d / "render_data" / "blueprint.json"
        print(f"""
GATE 3: preview & render —
  cd remotion && npx remotion render src/index.ts Blueprint ../output/{d.name}.mp4 --props={props}

Then cut shorts from the long-form:
  python pipeline.py output/{d.name}.mp4
""")


if __name__ == "__main__":
    main()
