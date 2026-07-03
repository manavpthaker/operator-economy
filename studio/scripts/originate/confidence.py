"""
Confidence layer: combines rigor evals, craft rubric, and claim-registry
verification into a per-stage confidence score. High confidence → the
pipeline auto-advances and logs; low confidence (or any hard trigger)
→ escalate to the operator.

Hard triggers escalate REGARDLESS of score:
  - any rigor hard-fail or craft kill-list hit
  - load-bearing claims still unverified/reported at this stage
  - training_mode: the pre-publish stage always escalates

Usage:
    python scripts/originate/confidence.py originate/<slug>/script.json --stage script|prepublish

Exit codes: 0 = AUTO-PASS, 2 = ESCALATE.
Writes originate/<slug>/confidence-<stage>.json
"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
WEAK = ("unverified", "reported", "estimate", "directional", "anecdote")


def run_eval(script, args_list):
    """Run an eval script, capture its output and exit code."""
    cmd = [sys.executable, str(ROOT / "scripts" / "originate" / args_list[0])] + [script] + args_list[1:]
    p = subprocess.run(cmd, capture_output=True, text=True)
    return p.returncode, p.stdout


def parse_rigor(out):
    passed = sum(1 for l in out.splitlines() if "[PASS]" in l)
    failed = sum(1 for l in out.splitlines() if "[FAIL]" in l)
    warned = sum(1 for l in out.splitlines() if "[WARN]" in l)
    total = passed + failed + warned
    return {"passed": passed, "failed": failed, "warned": warned, "total": total,
            "score": (passed + 0.5 * warned) / total if total else 0}


def parse_craft(out):
    score = maxpts = 0
    kills = [l.strip() for l in out.splitlines() if l.strip().startswith("✗") and "KILL" not in l]
    for l in out.splitlines():
        if "AUTO SCORE:" in l:
            frag = l.split("AUTO SCORE:")[1].split()[0]
            score, maxpts = (int(x) for x in frag.split("/"))
    kill_hit = "KILL-LIST HITS" in out
    return {"score": score, "max": maxpts, "ratio": score / maxpts if maxpts else 0,
            "kill_hit": kill_hit}


def parse_edit(out: str) -> dict:
    """Parse eval_edit.py's output. The eval prints `SCORE: n/max` and
    `KILL-LIST HITS: n`; both are captured for craft-weighted rollup.
    Zero score returned if the eval hasn't been run (storyboard absent)."""
    score = maxpts = 0
    kills = 0
    for l in out.splitlines():
        m = re.search(r"SCORE:\s*(\d+)/(\d+)", l)
        if m:
            score, maxpts = int(m.group(1)), int(m.group(2))
        m = re.search(r"KILL-LIST HITS:\s*(\d+)", l)
        if m:
            kills = int(m.group(1))
    return {"score": score, "max": maxpts,
            "ratio": score / maxpts if maxpts else 0,
            "kill_hit": kills > 0}


def claims_confidence(script):
    sources = script.get("sources", [])
    if not sources:
        return {"verified_ratio": 0, "weak": [], "n": 0}
    weak = [s["claim"][:60] for s in sources if any(w in (s.get("source") or "").lower() for w in WEAK)]
    return {"verified_ratio": 1 - len(weak) / len(sources), "weak": weak, "n": len(sources)}


def main():
    parser = argparse.ArgumentParser(description="Stage confidence score")
    parser.add_argument("script")
    parser.add_argument("--stage", choices=["script", "prepublish"], default="script")
    parser.add_argument("--config", default=str(ROOT / "config" / "blueprint.json"))
    args = parser.parse_args()

    config = json.load(open(args.config))
    auto = config.get("autonomy", {})
    threshold = auto.get("confidence_threshold", 0.85)
    training = auto.get("training_mode", True)

    script = json.load(open(args.script))
    mode = "draft" if args.stage == "script" else "approved"

    rc_r, out_r = run_eval(args.script, ["eval_script.py", "--mode", mode])
    rc_c, out_c = run_eval(args.script, ["eval_package.py"])
    rigor, craft = parse_rigor(out_r), parse_craft(out_c)
    claims = claims_confidence(script)

    # Edit rubric §VII runs at pre-publish (storyboard has to exist);
    # at script stage the storyboard hasn't been planned yet, so we
    # count it only when a real result comes back. Its ratio shares the
    # craft slot with eval_package (60/40 split — package still leads
    # since edit rubric derives from the storyboard, which derives from
    # package's asset planning).
    edit = {"score": 0, "max": 0, "ratio": 0, "kill_hit": False}
    if args.stage == "prepublish":
        rc_e, out_e = run_eval(args.script, ["eval_edit.py"])
        edit = parse_edit(out_e)
        # eval_edit exits 0 on PASS, 1 on ESCALATE — treat that here.
        edit_hard_fail = rc_e != 0
    else:
        edit_hard_fail = False

    craft_component = (0.60 * craft["ratio"] + 0.40 * edit["ratio"]) if edit["max"] else craft["ratio"]
    confidence = round(0.40 * rigor["score"] + 0.35 * craft_component
                       + 0.25 * claims["verified_ratio"], 3)

    reasons = []
    if rc_r != 0:
        reasons.append("rigor hard-fail")
    if craft["kill_hit"] or rc_c != 0:
        reasons.append("craft kill-list hit")
    if edit["kill_hit"] or edit_hard_fail:
        reasons.append("edit-rubric kill-list hit")
    if confidence < threshold:
        reasons.append(f"confidence {confidence} < threshold {threshold}")
    if args.stage == "prepublish":
        if claims["weak"]:
            reasons.append(f"{len(claims['weak'])} load-bearing claims still weak/unverified")
        if training:
            reasons.append("training_mode: pre-publish review mandatory")

    verdict = "ESCALATE" if reasons else "AUTO-PASS"
    result = {"stage": args.stage, "confidence": confidence, "threshold": threshold,
              "verdict": verdict, "reasons": reasons,
              "components": {"rigor": rigor, "craft": craft, "claims": claims, "edit": edit}}

    out_path = Path(args.script).parent / f"confidence-{args.stage}.json"
    json.dump(result, open(out_path, "w"), indent=2)

    print(f"\n{'='*74}\n  CONFIDENCE [{args.stage}]: {confidence}  →  {verdict}")
    for r in reasons:
        print(f"    • {r}")
    if claims["weak"] and args.stage == "script":
        print(f"    (weak claims tracked, allowed at script stage: {len(claims['weak'])})")
    print(f"{'='*74}\n")
    sys.exit(0 if verdict == "AUTO-PASS" else 2)


if __name__ == "__main__":
    main()
