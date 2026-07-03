# AGENTS.md

This file provides guidance to Codex (Codex.ai/code) when working with code in this repository.

## What this repo is

Content operations for **The Operator Economy** — a YouTube channel + newsletter + blueprint library. Two things live here:

1. **Editorial / strategy docs** (repo root) — positioning, brand, topic queue, kill criteria, research, per-video logs. Markdown, no build step.
2. **`design-system/`** — the visual design system (**Rev C**, imported 2026-07-02 from Codex Design; "The Working Schematic" direction). **This directory is the single source of truth for all brand visuals.** Token layer (`tokens/*.css` linked via `styles.css`), React components (`components/{core,brand,data}/`), published system doc (`guidelines/Design System.html`), canonical reference comps (`surfaces/`: hero, thumbnail, masthead, cover). `ui_kits/` are Rev-A layouts (token-migrated, layout-superseded — `surfaces/` is canonical). Read `design-system/README.md` first. `brand/design-system.md` is the superseded v1 strategy rationale; `studio/config/brand.json` is derived from the Rev C tokens (reconciled 2026-07-02).
3. **`studio/`** — a Python + Remotion production engine. Two entry points:
   - `studio/originate.py` — originates a long-form blueprint video from a research brief (topic → script → VO → assets → render data + LinkedIn/newsletter/blueprint derivatives).
   - `studio/pipeline.py` — cuts short-form clips from a rendered long-form (or any raw recording).

`studio/` was vendored from the `viddy` repo on 2026-07-02; this copy is canonical for OE. The `studio/README.md` still refers to it as "Viddy" — that's the shorts pipeline. The OE-specific pipeline is documented in `studio/ORIGINATE.md` and `docs/pipeline.md`.

## Architecture: the confidence-gated pipeline (v3)

The whole system is organized around **one research run → five surfaces** (long-form video, Shorts, LinkedIn posts, newsletter, downloadable blueprint), passing through three human gates that are now **confidence-scored**, not mandatory:

- `studio/scripts/originate/confidence.py` combines rigor evals (40%) + craft rubric (35%) + claim-registry verification (25%) into a per-stage score.
- `≥ 0.85` and no hard triggers → **AUTO-PASS**, pipeline advances.
- Below threshold or any hard trigger (rigor hard-fail, craft kill-list hit, unverified load-bearing claim) → **ESCALATE**, operator (Manav) reviews.
- Pre-publish **episode library review** is mandatory while `autonomy.training_mode: true` in `studio/config/blueprint.json` (calibration period). Full model + rationale in `docs/automation-architecture.md`.

Gate 1 (script POV pass) is the monetization moat — `generate_vo.py` refuses to run if `[POV: ...]` tokens remain in `script.json`. Gate 2 (assets) is checks-only, no human step. Gate 3 (episode-library review) is the mandatory-during-training gate.

### Data flow

```
originate.py new <topic> --research brief.md
  → scripts/originate/generate_script.py    → originate/<slug>/script.json
  → eval_script.py --mode draft + eval_package.py + confidence.py --stage script

  [Gate 1: replace [POV:] tokens, verify numbers]

originate.py continue <slug>
  → eval_script.py --mode approved (HARD gate: 0 POV tokens)
  → generate_vo.py    → originate/<slug>/vo/*.mp3 (ElevenLabs)
  → plan_assets.py    → originate/<slug>/assets.json

originate.py render <slug>
  → prepare_longform.py → originate/<slug>/render_data/blueprint.json
  → derive_content.py   → content/{blueprint,newsletter,linkedin_posts}.md + shorts_briefs.json
  → eval_package.py (re-run w/ shorts checks) + confidence.py --stage prepublish

  [Gate 3: preview + render via Remotion, then shorts via pipeline.py]
```

Per-episode working dir is `studio/originate/<slug>/` — everything for one topic (research, script, VO, assets, derived content, confidence reports) lives there. That directory + the git repo IS the run ledger; there's no database.

### The Python ↔ Remotion boundary

Python scripts produce `render_data/blueprint.json` (props); Remotion consumes it. Audio must be reachable via `staticFile` — copy or symlink `originate/<slug>/vo/` into `remotion/public/` before rendering (not yet automated — see `docs/pipeline.md`).

## Common commands

All from `studio/`.

```bash
# --- originate (long-form + derivatives) ---
python originate.py new "topic string" --research path/to/brief.md   # Phase 1
python originate.py continue <slug>                                   # Phase 2 (after Gate 1)
python originate.py render <slug>                                     # Phase 3 (after Gate 2)

# Render the long-form (from studio/)
cp -r originate/<slug>/vo remotion/public/vo
cd remotion && npx remotion render src/index.ts Blueprint ../output/<slug>.mp4 \
    --props=../originate/<slug>/render_data/blueprint.json

# Preview in Remotion Studio
cd studio/remotion && npm run studio

# --- shorts (from rendered long-form or any raw recording) ---
python pipeline.py input/video.mp4              # Phase 1 (transcribe → detect → select), stops for review
python pipeline.py input/video.mp4 --render     # Phase 2 (cut + prepare render data), after review
python pipeline.py input/video.mp4 --step transcribe   # single step: transcribe|layout|select|broll|cut|prepare

# --- individual evals (invoked automatically by originate.py; run standalone for debugging) ---
python scripts/originate/eval_script.py  originate/<slug>/script.json --mode draft|approved
python scripts/originate/eval_package.py originate/<slug>/script.json
python scripts/originate/confidence.py   originate/<slug>/script.json --stage script|prepublish
```

Required env: `ANTHROPIC_API_KEY`, `OPENAI_API_KEY` (Whisper for shorts), `ELEVENLABS_API_KEY` (VO). Python deps: `pip install anthropic openai requests`; also needs `ffmpeg` on PATH. Remotion deps: `cd studio/remotion && npm install`.

No test suite or linter is wired up — the evals are the tests. When a stage escalates, the script's exit code and the `*_review.md` / confidence report in `originate/<slug>/` are the diagnostic surface.

## Config

- `studio/config/blueprint.json` — channel positioning, section structure (hook/thesis/evidence/stack/playbook/economics/cta), models, VO settings, derivation counts, `autonomy.training_mode` flag and confidence weights/thresholds. **This is the file to edit for pipeline behavior.**
- `studio/config/brand.json` — shared visual style (colors, fonts, caption positioning). Used by both `originate.py` and `pipeline.py`. **Derived from `design-system/tokens/`** (the source of truth; see the `_source_of_truth` key for the token mapping) — never edit values here without deriving them from the token layer.
- `studio/config/default.json` — shorts pipeline settings (clip duration, count, models).
- `studio/config/episode.json` — per-episode overrides for the shorts pipeline (title, context for clip selection).

## Editorial constraints that shape the code

These aren't style preferences — they're enforced by evals and will fail the pipeline:

- **No `[POV: ...]` tokens survive to `continue`.** The POV pass (Manav's operator experience) is the differentiator and the YouTube inauthentic-content-policy shield. `eval_script.py --mode approved` hard-fails on any remaining token.
- **No hype lexicon** (insane / secret / skyrocket / …), no income-promise patterns. Voice is documentary, not hype. See `brand/brand.md`.
- **Every money claim needs a source or an explicit estimate marker**, and weak sources must be hedged aloud in `vo_text` ("reported / unverified"), not just footnoted. Public tool pricing is exempted.
- **Evidence must span low end AND high end** (solo/side operator + venture-scale version). Enforced by `eval_script.py`.
- **AI-disclosure box must be checked on upload** (Jan 2026 policy). This is a human step at Gate 3; `containsSyntheticMedia` will also be set on the API upload path when built.
- **Shorts must have cliffhanger_line + pinned_comment**; complete-answer Shorts are a kill-list item. Enforced in the derive step's eval re-run.

## Where to read next

- `docs/automation-architecture.md` — the v3 decision record. If you're changing how gates/orchestration work, read this first (especially the "research bias note" — the reports recommended n8n and we overruled).
- `docs/pipeline.md` — the end-to-end operator runbook.
- `docs/evals.md` — every check `eval_script.py` / `eval_package.py` runs, plus the findings log from real runs.
- `docs/content-rubric.md` + `docs/kill-criteria.md` — the 100-point craft rubric (publish gate ≥80, zero kill-list hits) and the 26-week decision gates. Kill/keep decisions are **rate-based, not absolute** (e.g., email capture rate <0.5% of views, not total signups) — never kill a converting format for cold-start reach.
- `topics/queue.md` + `topics/scoring.md` — scored thesis backlog feeding `originate.py new`.

## Imported Claude Cowork project instructions
