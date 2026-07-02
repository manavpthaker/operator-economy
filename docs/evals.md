# Gates & evals

Three human gates, each backed by automated checks where determinism allows. Automated Gate 1 evals live in `studio/scripts/originate/eval_script.py` and run automatically: `draft` mode after script generation, `approved` mode (hard block) when you run `originate.py continue`.

## Gate 1 — Script (the moat gate)

### Automated (eval_script.py) — validated against pilot #1, July 2026

| Check | Type | Rationale |
|---|---|---|
| Schema + blueprint_summary complete | HARD | Downstream steps parse these |
| Sections match config order | HARD | Render mapping depends on it |
| Per-section word count within ±35% of target | WARN | Caught real failure: first run came out 6 min vs 10 (4 sections at 41–63%). Prompt now sends explicit word budgets |
| Hook has a real number in first 2 sentences; ≤60 words | HARD/WARN | Format rule |
| Draft mode: ≥2 `[POV:]` tokens · Approved mode: 0 | HARD | POV pass is the monetization compliance shield — enforced both directions |
| No hype lexicon (insane/secret/skyrocket/…) | HARD | Channel voice + policy posture |
| No income-promise patterns | HARD | YMYL/compliance |
| Every money-claim beat has source or estimate marker | HARD | Documentary rigor is the differentiator |
| Weak sources hedged in spoken text | WARN | "Reported/unverified" must be said aloud, not just footnoted (public tool pricing exempt) |
| 2–4 highlight words per beat, present in vo_text | HARD | Caption renderer depends on it |
| 3 titles, ≥1 with a number | HARD/WARN | Packaging |
| Evidence spans low end AND high end | HARD | The thesis-format requirement |

### Human judgment (not automatable — your actual pass)

Would you say every sentence out loud to a peer? Does the POV material contain something only you could say? Is the low-end example genuinely believable (not a course-seller's number presented straight)? Does the hook make YOU want the answer? Do you believe the economics section enough to defend it in comments?

## Gate 2 — Assets

Automated candidates (not yet built — add to plan_assets or a checker): every chart's numbers appear in beat source/vo_text (no invented data); ≤4 screen_recs; asset type mix (≥1 chart in evidence + economics; not >60% slides); every broll query is 2–4 concrete words. Human: does each asset earn its screen time; is the labeled "REPORTED, unverified" framing visually present on weak-source charts?

## Gate 3 — Render/publish

Human checklist: captions sync at 3 spot-check points (start/middle/end); audio level consistent across section boundaries (each section is a separate ElevenLabs call — watch for loudness jumps); chart animations complete before beat ends; AI-disclosure box checked; title/thumbnail matches an eval-passing option; blueprint link live before publish; description sources present.

## Findings log

**2026-07-02 (pilot #1, ai-implementation-consulting):** 16/21 pass on first run. Real catches: (1) under-generation — script hit ~60% of word budget; fixed by sending explicit per-section word budgets in the prompt; re-test on next live run. (2) Hedge-checker over-flagged public tool pricing; exempted. (3) Everything policy-critical (sources, hype, promises, POV markers, low/high evidence balance) passed clean — the system prompt's rigor rules held even with mixed-quality research input, which was the design intent of using unverified Medium claims in the brief.

**2026-07-02 (external critique pass):** Five structural flaws identified and fixed. (1) Numbers-only hook check was an automated straightjacket — broadened to archetype tension signals (number/question/quote/contrast); a numbers-only mandate produces the formulaic writing the inauthentic-content policy targets. (2) Kill criteria used absolute email count — switched to capture RATE (<0.5% of views); never kill a converting format for cold-start reach. (3) Chapters contradiction between craft-report-1 (mandated) and rubric (optional) — rubric explicitly overrules the report for narrative episodes. (4) Visual-cadence proxy could pass stock-b-roll swapping — replaced with semantic-density checks (no 3+ consecutive b-roll beats; proof artifacts required in evidence + economics). (5) Shorts had zero automated evals — derive schema now requires cliffhanger_line + pinned_comment per brief; complete-answer Shorts are a kill-list item; checks run automatically after the derive step.
