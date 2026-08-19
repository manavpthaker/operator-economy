# VO-First Episode Production

This is the authoritative production order after research and the initial episode brief. The final narration is the spine of the edit. A storyboard is a transcript coverage plan, not a collection of finished-looking slides.

## Rolling Development Cadence

Episode development starts on Monday, one full release cycle before the episode is expected to launch. Publishing the current show triggers development of the next one; it does not mark the beginning of an empty week.

Maintain a rolling slate rather than one episode moving through every stage alone:

| Lane | Normal Monday state |
|---|---|
| Current episode | Launch and release verification |
| Next episode | VO, coverage, sourcing, and rough cut |
| Following episode | Research complete; script under review |
| Later candidates | Briefs and evidence gathering |

Several episodes may be in research and script development at the same time. Script locks, VO, coverage approvals, and visual locks remain episode-specific; work on one show never advances another show's state. During a catch-up week, develop multiple research briefs and scripts to establish at least a two-episode buffer. Do not create VO merely to make the slate look ahead: each script still passes the human lock gate first.

## State Machine

| State | Required artifact | Approval meaning |
|---|---|---|
| `script_locked` | `script.json` + SHA-256 in `production_state.json` | Structure, claims, and language are approved. |
| `vo_complete` | Edited narration + word-level transcript | The real runtime and pacing are fixed. |
| `coverage_approved` | Transcript coverage map, normally one visual beat every 3–10 seconds | Every spoken phrase has a deliberate visual job. |
| `assets_selected` | Asset manifest with selects, provenance, rights, and in/out points | Coverage is sourceable; unresolved media is visible. |
| `rough_cut_approved` | Coverage-first edit over locked VO | The argument works visually without polish. |
| `visual_lock` | Second visual pass with final graphics and replacements | Shot order and durations are final. |
| `final_mix_complete` | Music, sting, SFX, grade, captions, and mastered export | Delivery candidate is ready for release QA. |

Stages are sequential and fail closed. Changing `script.json` after approval invalidates every downstream state.

## Commands

```bash
cd studio
python originate.py new "topic" --research brief.md

# Human script review happens here.
python scripts/originate/script_readthrough.py originate/<slug>/script.json
python originate.py lock-script <slug>

# Run only after the script is explicitly approved.
python originate.py voice <slug>

# Build the exact-VO visual pass and planned asset manifest. This remains a
# draft until a human reviews every beat and approves coverage.
python scripts/originate/build_coverage_map.py originate/<slug>/script.json

# Downstream approvals are recorded as the work is reviewed.
python originate.py mark <slug> coverage_approved
python originate.py mark <slug> assets_selected
python originate.py mark <slug> rough_cut_approved
python originate.py mark <slug> visual_lock

# Final Remotion preparation is blocked until visual_lock.
python originate.py render <slug>
python originate.py mark <slug> final_mix_complete
```

`originate.py continue` is intentionally disabled. It previously jumped from script approval through VO, asset planning, storyboard generation, pacing, music, and edit evaluation in one command.

## Coverage and Assets

The coverage map is derived from the exact edited VO transcript. Each 3–10 second beat records timecode, narration, visual purpose, asset type, and intended shot. It should prefer evidence and specificity in this order: source document or interface; archival material; custom chart or explanatory motion; specific human/contextual footage; typography; generic stock only as a documented exception.

The asset manifest assigns stable IDs such as `A001`. Each entry records the coverage beat, canonical source URL, provider/creator, license and retrieval date, local file, rights/faces review, selected in/out points, crop/focal point, and status. Source in batches by type; never auto-approve the first search result.

## Edit Order

Build the rough cut directly over locked VO using simple cuts. The first review solves coverage, relevance, repetition, and visual comprehension. Only after rough-cut approval should the team create final diagrams, branded charts, document highlights, punch-ins, transitions, grading, music, or sound design. The OE design system supplies identity and explanatory grammar; it does not turn every paragraph into a branded slide.
