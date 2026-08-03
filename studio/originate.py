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
CONFIG_PATH = ROOT / "config" / "blueprint.json"


def load_config() -> dict:
    return json.loads(CONFIG_PATH.read_text())


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

    p_fin = sub.add_parser("finalize",
                           help="Post-Remotion: color grade + final loudness master on output/<slug>.mp4")
    p_fin.add_argument("dir", help="originate/<slug> or bare slug")
    p_fin.add_argument("--input", help="override input mp4 (default output/<slug>.mp4)")
    p_fin.add_argument("--no-grade", action="store_true", help="skip color grade regardless of config")
    p_fin.add_argument("--no-master", action="store_true", help="skip final loudness master regardless of config")

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
        # Post-generate_vo mastering. Config-gated by voiceover.mastering_provider:
        #   "local" (default) + local_chain "broadcast" → master_vo_local.py
        #        broadcast chain (bright+weighty documentary voice)
        #   "local" + local_chain "clean"  → skip (generate_vo.py's inline
        #        CLEAN chain is already the master)
        #   "auphonic" → master_vo_auphonic.py (adaptive leveler + noise
        #        reduction; free tier watermarks output)
        # --commit replaces primary .mp3 so downstream picks up new master.
        # Runs BEFORE generate_avatar.py so HeyGen syncs to the final VO.
        cfg = load_config()
        vo_cfg = cfg.get("voiceover", {})
        provider = vo_cfg.get("mastering_provider", "local")
        if provider == "auphonic":
            run_step("master_vo_auphonic.py",
                     [str(d / "vo"), "--commit"],
                     "Master VO via Auphonic")
        elif provider == "local" and vo_cfg.get("local_chain", "clean") != "clean":
            run_step("master_vo_local.py",
                     [str(d / "vo"), "--commit",
                      "--chain", vo_cfg.get("local_chain", "broadcast")],
                     f"Master VO via local {vo_cfg.get('local_chain')} chain")
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
        # Thumbnail candidates. NOT a run_step: exit 2 means "no scene image
        # yet", which is a prompt for the operator, not a pipeline failure.
        # This exists because EP003 shipped with no thumbnail artifact at all
        # and drew 0.0% CTR on 142 recommended impressions — the absence was
        # silent. See docs/thumbnail-rubric.md.
        print(f"\n{'='*60}\n  ORIGINATE: Thumbnail Candidates\n{'='*60}\n")
        rc = subprocess.run([sys.executable, str(SCRIPTS / "prepare_thumbnail.py"),
                             script]).returncode
        if rc == 2:
            print("\n⚠ THUMBNAIL NOT READY — generate the scene image before publish.\n"
                  "  The episode can keep rendering; it cannot ship without this.")
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

Then finalize (color grade + final loudness master):
  python originate.py finalize {d.name}

Then cut shorts from the long-form:
  python pipeline.py output/{d.name}.mp4
""")

    elif args.command == "finalize":
        d = resolve_dir(args.dir)
        cfg = load_config()
        mp4 = Path(args.input) if args.input else ROOT / "output" / f"{d.name}.mp4"
        if not mp4.exists():
            print(f"Error: {mp4} not found. Render in Remotion first.", file=sys.stderr)
            sys.exit(1)

        grade_cfg = cfg.get("finalize", {}).get("grade", {})
        master_cfg = cfg.get("finalize", {}).get("master_final", {})

        if grade_cfg.get("enabled") and not args.no_grade:
            gargs = [str(mp4), "--commit",
                     "--contrast", str(grade_cfg.get("contrast", 1.06)),
                     "--saturation", str(grade_cfg.get("saturation", 0.94)),
                     "--warmth", str(grade_cfg.get("warmth", 1.0)),
                     "--shadow-lift", str(grade_cfg.get("shadow_lift", 0.02)),
                     "--grain", str(grade_cfg.get("grain", 8))]
            if grade_cfg.get("lut"):
                gargs += ["--lut", grade_cfg["lut"]]
            run_step("color_grade.py", gargs, "Color Grade")
        else:
            print("  (skipping color grade)")

        if master_cfg.get("enabled") and not args.no_master:
            run_step("master_final.py",
                     [str(mp4), "--commit",
                      "--lufs", str(master_cfg.get("lufs", -14)),
                      "--tp", str(master_cfg.get("true_peak", -1.5)),
                      "--lra", str(master_cfg.get("lra", 9))],
                     "Master Final Loudness")
        else:
            print("  (skipping final loudness master)")

        # Verify: eval_edit.py can probe LUFS on the rendered file.
        # Non-blocking — reports the numbers as a sanity check.
        run_step("eval_edit.py",
                 [str(d / "script.json"), "--rendered", str(mp4)],
                 "Verify (Edit Rubric + LUFS probe)")

        print(f"""
✓ FINALIZED: {mp4}
Backups: {mp4.with_suffix('.ungraded.mp4').name}, {mp4.with_suffix('.premaster.mp4').name}

Cut shorts from the finalized long-form:
  python pipeline.py {mp4}
""")


if __name__ == "__main__":
    main()
