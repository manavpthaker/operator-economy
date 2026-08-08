# EP005 `too-small-to-bother` — runbook

**№ 005** (decision 2026-08-08; displaced small-cohort-business, which keeps its script).
Authored 2026-08-08 in a cloud session with **no API keys** — everything deterministic is done
and eval-clean; everything requiring ElevenLabs/HeyGen/Remotion/YouTube runs on Manav's machine.

## State

| Artifact | Status |
|---|---|
| `script.json` | **Done.** `eval_script --mode approved`: 22/22. `eval_package`: 63/63 auto, PROJECTED PASS, zero kills. |
| `assets.json` | **Done** (hand-authored; `plan_assets.py` will skip its LLM call on the existing file). Every chart series value canonicalises to a `content-os/facts.md` entry, so the card gate passes downstream by construction. |
| `confidence-script.json` | 0.951, verdict **ESCALATE** — expected, not a defect. See below. |
| VO / storyboard / renders / links.json | Not started; requires keys + your machine. |

## Why confidence says ESCALATE at 0.951

`confidence.py --stage script` runs `eval_script` in **draft** mode, which requires ≥2 unfilled
`[POV: ...]` tokens awaiting the human pass. This script has **zero tokens because the POV is
already woven** — every first-person beat is restated from the 8/10 manifesto, which Manav
wrote and approved for the OE masthead. Approved mode (the one `originate.py continue`
enforces) passes 22/22. The escalation resolves the way training mode intends: **your Gate-1
read of `script.json` is the sign-off.** Nothing publishes unedited regardless — VO, render,
and upload all pass through your hands.

Gate-1 specifics worth your eye:
- The two spots where POV is asserted in your voice: `thesis#3` (refusing a productivity
  multiplier) and the framing beats. Confirm they sound like you or edit in place.
- `stack`/`playbook` are repurposed per the brief (moat section / two-question evaluation) —
  the config's literal "tool stack / build plan" purposes don't apply to a thesis episode.
- Lakewood is deliberately absent (dossier: geography confound). Do not add it back to VO.
- Weak-flagged claims (2, allowed at script stage): Medvi (Forbes, reported) and the
  toolmaker run-rates — both hedged aloud in the vo_text already.

## Your machine, in order (from `studio/`)

```bash
# 0. Gate 1: read script.json, edit anything, then:
python originate.py continue too-small-to-bother      # eval(approved) → VO → avatar → assets(cached)

# 1. Storyboard chain (Phase 0)
#    hand_tune_storyboard.py does not exist for this episode yet — copy
#    solo-design-agency/hand_tune_storyboard.py as the template; the screens
#    follow assets.json, which was written to the card grammar already.
python scripts/originate/pace_storyboard.py originate/too-small-to-bother/script.json
python scripts/originate/prepare_longform.py originate/too-small-to-bother/script.json
python scripts/originate/arrange_bed.py originate/too-small-to-bother/script.json --stage cut
python scripts/originate/arrange_bed.py originate/too-small-to-bother/script.json --stage mix
python scripts/originate/derive_content.py originate/too-small-to-bother/script.json
python scripts/originate/prepare_shorts.py originate/too-small-to-bother/script.json --trailer
python scripts/originate/render_blueprint.py originate/too-small-to-bother/script.json \
    --hero '5,060 → 7,857' --hero-caption 'US software firms under five employees, 2017 → 2022'

# 2. The release gate (content-os) — now covers on-screen graphics:
cd ../../content-os && bin/doctor.sh --week <Monday> --slug too-small-to-bother --gate
#    gate_cards.py reads render_data/blueprint.json: every on-screen number vs facts.md,
#    do-not-state incl. split-field, and per-evidence-beat card coverage.

# 3. Render + loudness + eval_edit, then upload (AI-disclosure box CHECKED, schedule ≥24h out,
#    thumbnail gate: 3 words readable at 120px — options in script.json), then launch.py,
#    then sync-episode.py --slug too-small-to-bother --week <Monday> to render the BMC templates.
```

## Blueprint PDF

The lead magnet is the **two-question evaluation sheet**. Design reference:
`reference/working-paper-01-print-capture.pdf` (never ship that file — print-capture with
claude.ai headers). Re-export clean from Claude Design, **OE byline** (the personal
"MP Thaker / mpthaker.xyz" byline stays off OE artifacts).

## Carried obligations (from the EP004 punchlist §E — still open)

- Thumbnail gate before anything ships (EP003: 0.0% CTR on 142 impressions with no thumbnail).
- Pinned comments carry live URLs. No "link in bio." EP002's four are STILL unfixed.
- Fix the `№ 001` title-card number in the shorts renderer before EP005's shorts are cut.
