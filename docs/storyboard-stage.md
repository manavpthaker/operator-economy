# Storyboard stage — design spec (v2, 2026-07-03)

**v2 change:** merged with the edit-grammar spec in `faceless-video-editing-research.md`. The storyboard now carries **layouts** (16 of them, not 8), **script tags** per beat, **sfx cues**, and **music intensity** per screen. Layouts are chosen from tags via a small deterministic map (§Tag → layout), then packed into screens obeying the cadence rules (§Cadence). The render layer consumes the same file and does not need to guess a grammar.

## Problem (unchanged from v1)

The №001 render cut to a new full-screen scene for every talking point: 24 scenes in 6 minutes (~one cut per 15s), each carrying its own title card. Softening the cuts (cross-dissolves, longer sheet cards) treats the symptom. The structural fix: **screens are planned from the script before assets are generated**, so one screen covers a coherent stretch of argument and talking points transition *within* the screen, not between screens.

## What was shipped in v1 (still true)

`BlueprintComposition.tsx` groups consecutive `slide` beats within a section into one persistent `SheetScene` at render time (heading holds, numbered lines reveal per beat, active line emphasized, past lines settle). Charts/broll/logo/screen_rec remain standalone. №001 drops from 24 scenes to ~14 with no pipeline change. This is a render-layer shim — the planner still doesn't know screens exist.

## Pipeline position (unchanged)

```
originate.py continue <slug>
  → eval_script.py --mode approved
  → generate_vo.py
  → plan_assets.py
  → storyboard.py         ← reads script.json + vo/timeline.json + vo/words.json + assets.json
  → eval_storyboard.py    ← pacing rules (durations, cut-rate, contiguity)
  → eval_edit.py          ← edit rubric §VII checks (grammar, cadence, sound cues)
```

`prepare_longform.py` then reads `storyboard.json` and emits `screens[]` in `render_data/blueprint.json` alongside the legacy `sections[]`. `BlueprintComposition` prefers `screens[]`; the run-grouping shim stays as fallback until every episode ships with a storyboard.

### Order of operations (important for regen)

When VO is regenerated, hand-tuning changes, or `storyboard.py` re-runs, follow this exact sequence — `pace_storyboard.py` MUST run after any change to screen structure or timings:

```
storyboard.py OR hand_tune_storyboard.py     → storyboard.json
pace_storyboard.py                           → adds `events` per screen
prepare_longform.py                          → merges into render_data/blueprint.json
render
```

`pace_storyboard.py` is idempotent: it reads `storyboard.json` + `vo/words.json` and stages events (fragment reveals, item drops, pulses, focus cycles) that make screens feel alive inside their holds. If it hasn't run, the renderer's ambient/camera/staggered-build fallbacks still fire, but the pace-derived stagger of body fragments and item drops will be absent — and dead spans past 8s show up as `eval_edit`'s density warnings. **Always re-run `pace_storyboard.py` after hand-tuning or VO regeneration.**

## Layout vocabulary (16)

The scene grammar from `faceless-video-editing-research.md` §1 — every screen is exactly one of these:

| Layout | What it is | When to use |
|---|---|---|
| `quote` | One impactful sentence, full-screen, minimal text; Boska on ink or navy; HARD cut in; captions HIDDEN | thesis line, reversal, warning, punchline, section payoff, likely Short-hook phrase |
| `proof_card` | One number in Fragment Mono + CitationChip | single-figure claim with a source |
| `chart` | Quantitative comparison or trend (Rev C bar/line) | multi-value claim |
| `gap` | Signature `$X → $Y` gold arrow | the once-per-episode scale contrast (hook) |
| `ladder` | Low/mid/high scale comparison, one sourced figure per step | 3-scale contrast (freelancer → boutique → enterprise) |
| `schematic` | Process model, stack, funnel, ladder, flywheel, timeline | multi-node argument (the stack section, project→retainer) |
| `artifact` | Framed screenshot/doc with annotation callout + source label | Airtable portal, Claude pricing, n8n canvas |
| `screen_rec` | Actual tool interaction with visible provenance (URL, cursor, scroll) | showing a workflow run |
| `offer_card` | Problem / deliverable / price / deadline as one card | offer templating |
| `case_file` | Problem → workflow → result | proven engagement |
| `risk_card` | Blunt warning or failure mode, brick accent | one per section max |
| `source_card` | One claim + source chip | citation only |
| `sheet` | Persistent heading + numbered reveals in place | ordinary bullet groups, playbook steps |
| `broll` | Real-world context shot | only when narration names a concrete place / action / operator moment |
| `chapter_reset` | Short section transition, captions HIDDEN | argument turns (not every section change — most changes are internal) |
| `cta` | Final action card | close only |

**Shot hierarchy (used to break ties when a beat qualifies for multiple layouts):**

1. Real artifact or screen recording (`artifact`, `screen_rec`)
2. Constructed artifact representing the exact workflow (`schematic`, `offer_card`, `case_file`, `ladder`)
3. Data visualization (`chart`, `proof_card`, `gap`)
4. Quote card or typography moment (`quote`, `chapter_reset`, `source_card`)
5. Specific contextual B-roll (`broll`)
6. Generic stock B-roll — **effectively banned by the edit kill list**

## Script tags (v2)

`storyboard.py` tags every beat before layout mapping. Tags are LLM-derived using the Claude model configured under `models.script` in `studio/config/blueprint.json` (same client pattern as `generate_script.py`, cached via `originate/<slug>/storyboard-tags.json` so re-runs don't burn tokens). One or more tags per beat:

| Tag | Meaning |
|---|---|
| `claim` | Factual assertion the video is making |
| `number` | A specific figure, currency amount, percentage, multiplier |
| `tool` | A named product/service the operator uses |
| `operator_pov` | POV-flavored line (originally a `[POV:]` token; Manav's experience) |
| `punchline` | A short, quotable, high-impact line — Short-hook candidate |
| `risk` | Failure mode, warning, negative outcome |
| `question` | Open question or rhetorical device |
| `process` | Multi-step description, workflow, order-of-operations |
| `cta` | Call-to-action content |

## Tag → layout mapping

Deterministic map, applied after tagging. When multiple tags fire, the first match wins in this order:

| Tag(s) | Layout |
|---|---|
| `cta` | `cta` (or `offer_card` if the beat carries a concrete price + deliverable) |
| `punchline` (short line, ≤10 words) | `quote` |
| `question` (opens a new section) | `chapter_reset` or `quote` |
| `risk` | `risk_card` |
| `number` + single figure | `proof_card` |
| `number` + `claim` + ≥2 values | `chart` (or `gap` if the values span >1000×; or `ladder` if the beat explicitly compares 3 scales) |
| `tool` + `operator_pov` | `screen_rec` (preferred) or `artifact` |
| `tool` (no operator_pov) | `artifact` |
| `operator_pov` + concrete place/action | `artifact` or `case_file` |
| `process` (multi-step, one section) | `schematic` |
| `claim` alone, no evidence needed | `sheet` (grouped with neighbours) |
| default (untagged) | `sheet` (grouped) |

Consecutive `sheet` layouts collapse into a single persistent screen with one reveal per contributing beat (v1 behaviour, preserved). All other layouts stand alone.

## Cadence (heuristics enforced by `eval_edit.py`)

From `faceless-video-editing-research.md` §"Visual cadence" + `faceless-video-craft.md` §2 pacing:

- **Hook** (first 30s): visual event every 4–8s. `eval_edit` checks reveal count in that window.
- **Body**: visual event every 8–15s.
- **Dense proof/chart section**: internal animation or annotation every 3–6s. Charts/proof_cards have their count-up + citation-in staggers to satisfy this.
- **Major composition reset**: every 25–45s. Any `screen.end` past 45s from the last reset must open a new screen.
- **No static composition >20s** unless it is actively building (has ≥2 reveals still coming).
- **No >2 consecutive `sheet` screens.** Break with a `quote`, `proof_card`, `chart`, `artifact`, or `chapter_reset`.
- **Emphasis staging**: at most ONE `quote` per section (the impact-frame rule from craft §P1). More than one quote/section reads as manic, not confident.

## Storyboard JSON schema (v2)

```json
{
  "slug": "ai-implementation-consulting",
  "total_seconds": 362.4,
  "screens": [
    {
      "id": "thesis-01",
      "section": "thesis",
      "layout": "sheet",
      "heading": "The thesis",
      "start": 12.88, "end": 45.60,
      "reveals": [
        {
          "beat": 1,
          "at": 12.88, "end": 25.20,
          "title": "The Gap",
          "body": "Knows it should use AI · Doesn't know how · Pays someone who does",
          "tags": ["claim", "operator_pov"],
          "word_anchor": {"start": 12.88, "end": 25.20}
        }
      ],
      "figure": {"text": "$5.9B → $2K", "source": "CIO Dive FY2025"} | null,
      "source": "..." | null,
      "sfx": [
        {"cue": "tick", "at": 12.88},
        {"cue": "hit",  "at": 23.55}
      ],
      "music": {"intensity": "calm | build | silence", "duck_db": -15}
    }
  ]
}
```

**Field notes:**

- `word_anchor` — the VO word range that owns the reveal, used by the composition to land visuals 2–3 frames before the word (`faceless-video-craft.md` §motion).
- `sfx.cue` — one of `tick` (list reveals, node drops, quiet: −18 dB), `whoosh` (section transitions), `hit` (quote-card impact, one per screen max). Names correspond to files in `remotion/public/sfx/`.
- `music.intensity` — `calm` (bed at −15 to −18 dB ducked under VO), `build` (bed at −8 to −12 dB during proof/build), `silence` (hard cut to silence ≥0.5s before the moment — mandatory before `quote` and `gap` screens per craft §P0). The composition reads `music.intensity` and either swaps tracks (per-section change) or cuts silence.

## Pacing rules (v1, kept)

- Screen duration 20–75s. Under 20s → merge with a neighbor; over 75s → split at the weakest reveal boundary.
- ≥2 reveals per `sheet` screen where the section has ≥2 talking points. A screen with one reveal must justify itself (chart, gap figure, b-roll, quote).
- Max ~10 screens per 6-minute episode (~one true cut per 35–40s).
- Every screen carries a figure or a source where the section makes a claim (Rev C: no unsourced numbers on screen).
- Transitions between screens only at argument boundaries — a screen never splits mid-claim.

## Eval + confidence hook

- `eval_storyboard.py` — pacing rules above (contiguity, per-screen durations, screen counts, sheet-reveal counts). Hard triggers: screen <10s, cut-rate >1 per 15s, sheet screen with 0 reveals, screen >90s.
- `eval_edit.py` — edit rubric §VII (grammar counts, cadence, cue coverage, kill-list checks). Hard triggers: any kill-list hit (see rubric); score <16/20.
- `confidence.py --stage prepublish` — rolls up both evals under the craft weight (edit rubric ratio ×0.35 shares the craft slot with `eval_package.py`; details in `automation-architecture.md`).

## Migration path (updated for v2)

1. `storyboard.py` v2 lands with tag pass + layout map + cadence packing + sfx/music cues. Existing `eval_storyboard.py` unchanged (its checks are still valid). ✓
2. `eval_edit.py` lands. Wired into `originate.py continue` (after storyboard) and `originate.py render` (before `prepare_longform` — final check on the plan) and into `confidence.py`. ✓
3. `prepare_longform.py` — emits full `screens[]` with all v2 fields into `render_data/blueprint.json`. ✓
4. `BlueprintComposition` v3 — new scene set (Quote/Proof/Artifact/Offer/Risk/Ladder/Source/Case + upgraded Sheet with figure well); music bed layer; SFX layer; asymmetric easings; drift + parallax grid. ✓
5. Delete the run-grouping shim once №002 renders from a real storyboard.

## Open questions carried forward

- Should the episode-wide schematic (plan_assets Phase 2 TODO) become a storyboard `layout: "schematic"` that persists across sections? (Leaning yes; blocked on a `schematic_context` field in the tag map that survives section transitions.)
- Are `case_file` and `offer_card` two layouts or one polymorphic? (Kept two until we author a second episode and see how the shapes diverge.)

## Step 3.5 — the pacing pass (added 2026-07-03)

After storyboard.py (and any hand-tune), run:

    python scripts/originate/pace_storyboard.py originate/<slug>/script.json

It stages each screen's EXISTING content across its window — body fragments,
custom-card items, highlight-word pulses (anchored to vo/words.json), chart
focus cycles — as per-screen `events` the renderer performs. Never invents
text. Idempotent; always re-run after hand-tuning or VO regeneration.
Order: storyboard.py → hand-tune → pace_storyboard.py → prepare_longform.py.
eval_edit.py enforces density (worst dead stretch ≤8s target, >16s kill).
