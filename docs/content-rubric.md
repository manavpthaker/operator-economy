# Content rubric (pre-publish, 100 points)

Merged from 3 craft research reports (`../research/reports/craft-report-1.md`, `craft-report-2.md`, `craft-report-3.md` — all saved in-repo), July 2026. Applied to every script + package at Gate 1 alongside the rigor evals. Automated subset lives in `studio/scripts/originate/eval_package.py`; the rest is the human pass.

**Publish gate: ≥80/100 AND zero kill-list items. Hook and Structure blocks are hard blocks below 15/25.**

Master platform context (highest confidence, YouTube-official): the recommender now optimizes *satisfaction and session contribution*, not raw watch time or CTR. Native A/B testing picks winners by **watch time per impression** — honest packaging structurally wins. 5% CTR with 60% retention beats 10% CTR with 30% retention.

## I. Hook — 25 pts (hard block <15)

| Criterion | Pts | Check |
|---|---|---|
| Premise/payoff fully stated by 0:15 (~37 words) | 10 | AUTO (graded: ≤15s=10, 15–25s=5, later=0) |
| Opens with a named archetype, never "hey/welcome/today/in this video" | 5 | AUTO (banned openers) + HUMAN (archetype named in package) |
| Concrete tension in first two sentences — number OR question OR quote OR contrast pivot (any approved archetype qualifies; a numbers-only mandate produces formulaic hooks, itself a slop signal) | 5 | AUTO |
| On-screen text carries the premise (mute viewers) | 3 | HUMAN (asset_hint on hook beat must specify text/graphic) |
| No overpromise the body can't cash | 2 | HUMAN |

Approved archetypes: stakes-first cold open (fall-before-rise) · number-first anchor · contrarian snapback · structural paradox · quantitative abstract · open-loop ("I looked at 12; one survived") · authority-led · systemic anatomy (expose the hidden incentive structure). Write the hook LAST, after the script.

Optional (craft-report-1, "psychology of progress"): a 3–5 milestone structural preview as on-screen text around 0:40–0:45 — a *visual* map, not chapter markers, and never a spoiler. Test against retention at that timestamp.

## II. Title — 15 pts

| Criterion | Pts | Check |
|---|---|---|
| ≤60 chars; subject in first 45 chars / first 4–5 words | 3 | AUTO |
| No AI-slop markers: colon/semicolon splits, "Unlocking/Revolutionizing/Mastering/Delve/A New Era/The Future of" | 4 | AUTO |
| One proven formula: Why-X, declarative thesis, specificity anchor, value-in-time. "Why X" > "How to" in this niche | 4 | HUMAN |
| Honest — viewer who finishes feels it was delivered; aligns with first 10s of VO | 4 | HUMAN |

## III. Thumbnail — 15 pts

| Criterion | Pts | Check |
|---|---|---|
| Overlay text ≤3 words (4 = max; >4 = 0) | 4 | AUTO (from thumbnail_text_options) |
| Text does NOT duplicate title words | 3 | AUTO |
| Single focal point, 40–60% of frame, legible at 180–320px | 4 | HUMAN |
| High-contrast stated palette (navy/gold house system); no starbursts, tilted text, stock handshakes | 4 | HUMAN |

Faceless reference systems: MagnatesMedia (cinematic single object + 1–2 word stakes), How Money Works (schematic + ≤3 words), Economics Explained (map + gold), Starter Story (real location + metric overlay). CTR benchmarks: 6–10% healthy at <10K subs; <4% in 48h = packaging problem; <1,000 impressions at 7d = title/niche fit, not thumbnail.

## IV. Structure & retention — 25 pts (hard block <15)

| Criterion | Pts | Check |
|---|---|---|
| Previewed-payoff arc (tease conclusion in hook, build the mechanism) — not chronological data-dump | 6 | HUMAN |
| Every non-CTA section ends with a micro-open loop (unresolved question / forward tease) | 6 | AUTO (heuristic) + HUMAN |
| SEMANTIC density, not cut-counting: each beat introduces a new evidence artifact or idea (chart, metric, source, dashboard, real asset); no 3+ consecutive b-roll beats; evidence + economics sections must each contain ≥1 proof artifact. Swapping stock b-roll every 15s passes a cuts-counter and still reads as slop | 6 | AUTO (b-roll runs + artifact presence) + HUMAN |
| No wrap-up signals anywhere ("in conclusion", "thanks for watching", "that's how") | 4 | AUTO |
| Chapters: only if non-spoilery; skip on narrative-heavy episodes | 3 | HUMAN |

Retention benchmarks (directional): 70%+ at 0:30 = push signal; APV 40–55% healthy for 8–12 min; predictable cliffs at intro-end, section transitions, final 20%.

## V. Voice & trust — 10 pts

| Criterion | Pts | Check |
|---|---|---|
| Human/cloned-and-directed voice, natural inflection — no monotone TTS (AI-fatigue: perceived-AI content retains dramatically worse) | 4 | HUMAN |
| On-screen source citations on stat/chart beats | 4 | AUTO (chart assets must carry source) + HUMAN |
| Material variation from prior episodes (not templated) — policy survival | 2 | HUMAN |

## VI. CTA & conversion — 10 pts

| Criterion | Pts | Check |
|---|---|---|
| ONE soft blueprint mention at 55–75% runtime after a value peak, benefit-framed (mid-CTA beats end-only: only ~16% reach final 10s) | 5 | AUTO (position) + HUMAN (framing) |
| Blueprint link: description first line + pinned comment | 3 | HUMAN (publish checklist) |
| End bridges to OUR next video (session contribution), never bare "subscribe" | 2 | AUTO (kill-phrases) + HUMAN |

## Kill list (any = no publish)

"You won't believe"/SHOCKING/manufactured gaps · fake-shock or horror-bait thumbnails, starbursts, tilted text · "hey guys, welcome back" or channel-intro bumpers · keyword stuffing · monotone TTS over stock montage · generic stock imagery (businessman handshake) · end-only CTA as sole CTA · income promises in metadata · Shorts with TikTok watermarks, hashtag walls, or complete answers (cliffhanger Shorts convert 3–5x better) · duplicated title text on thumbnail.

## Shorts addendum

Hook in 1–2 seconds, payoff-first-then-explanation, visible movement frame one. Pinned comment to the SPECIFIC long-form (top conversion tactic) + Related Video link. The long-form should open compatible with the Short's promise. Shorts ranked by a separate model — they no longer directly boost long-form; they're pure discovery.

## Post-publish validation (self-correcting loop)

| When | Metric | Validates | Falsification threshold |
|---|---|---|---|
| 24h/7d | First-30s retention | Hook | <60% at 0:30 |
| 24h/7d | Impressions CTR by source | Title+Thumb | <4% at 48h; <1K impressions at 7d = niche fit |
| 7d/28d | APV / retention cliffs | Structure | <40% APV; cliff at CTA timestamp = CTA framing |
| 28d | Returning-viewer share | Voice/Trust | Flat or declining (returning viewer ≈ 5–10x weight of new) |
| 7d/28d | Blueprint CTR + session continuation | CTA | Low download rate; session ends at our end-screen |

Log every video's scores + these metrics in `videos/<slug>/` — after ~20 videos, reweight the rubric toward our actual failure modes.

## Conflicts resolved across reports

**Chapters:** reports split — craft-report-1 *mandates* 3–5 timestamped chapters (5 pts); craft-report-3 shows chapters hurt narrative content by enabling skip-the-build. **This rubric overrules craft-report-1: chapters are OPTIONAL for Lane 1B, no penalty for omitting them on story-driven episodes; use only when non-spoilery on framework-heavy ones.** CTA: mid-video 55–75% (strongest evidence) over final-30s-only. Thumbnail words: ≤3 target, 4 max. Hook tension: any archetype signal qualifies, not numbers-only. The "70% at 0:30" rule is folklore — useful target, not doctrine; our own analytics arbitrate.

## VII. Edit rubric (Gate 3, applied to the rendered video / storyboard) — 20 pts (hard block <16)

Added 2026-07-03 alongside the storyboard-stage v2 rollout. Encodes `docs/faceless-video-editing-research.md` §"Edit-density eval". Runs on `originate/<slug>/storyboard.json` (AUTO) plus the rendered MP4 (loudness only). A separate 20-pt block on top of the 100-pt craft rubric — it does not replace §IV Structure, it enforces the visual grammar within it. **This is a hard block: any edit-rubric failure ships as ESCALATE, no exceptions.**

| Criterion | Pts | Check |
|---|---|---|
| Scene grammar in use: ≥5 quote/punchline moments AND ≥3 artifact/screen_rec/proof screens per 6 min | 5 | AUTO (`eval_edit.py` counts `layout` field in storyboard.json) |
| Cadence: no static composition >20s unless actively building (has ≥2 reveals); composition reset every 25–45s; never >2 consecutive `sheet` screens | 5 | AUTO (durations + `reveals[]` length + layout runs from storyboard.json) |
| Every `broll` query names a concrete noun/action (no abstract queries); every money-claim screen carries a `source` or `figure.source` label | 4 | AUTO (regex on `search_query` — allowlist of concrete nouns; presence check on `source`) |
| Hook: visual event every 4–8s in first 30s; premise proven (shown) not just stated | 3 | AUTO first-30s reveal density from storyboard.json; HUMAN "shown" judgment |
| Sound: music bed present with per-section change + ducking; SFX cued on reveals/transitions/impacts; master −14 LUFS ±1 integrated, true peak ≤ −1 dBTP | 3 | AUTO `music`/`sfx` cues per screen in storyboard.json + `ffmpeg loudnorm` print on the rendered MP4 |

**Publish gate: ≥16/20 AND zero edit-kill-list items.** The Gate 3 confidence rollup weights the edit rubric alongside the existing rigor (40%) / craft (35%) / claims (25%) split — the edit-rubric ratio is a fourth component in `confidence.py` under the craft weight (see `automation-architecture.md` for the reweighting note).

### Edit kill list (any = no publish)

- Unresolved placeholder screen (any beat with `layout=broll` whose `search_query` is missing / abstract, any beat with `layout=screen_rec` whose `tool`/`action` is missing).
- Generic/abstract b-roll (`search_query` matches "small business", "office", "typing", "handshake", "AI future", "technology"; also fails if it's the ONLY visual on a claim beat).
- >45 seconds of runtime without a composition reset (measured as `screen.end - previous_reset.start`).
- Unsourced money figure on screen (any `layout=proof_card|chart|ladder|gap` with a numeric title/reveal but no `source` and no `figure.source`).
- Caption text duplicating a quote card verbatim while the card is up (captions must be HIDDEN during `layout=quote` and `layout=chapter_reset`; if captions are still emitting in those windows, the render fails).
- Music bed configured but the referenced audio file is missing at render time AND the render silently fell back — the failure must be surfaced in the render log (never a placeholder tone).

## Shorts derivative checks (Gate: after derive step)

Every shorts brief must end on a cliffhanger (`cliffhanger_line`) — a complete-answer Short kills long-form conversion (kill-list item) — and carry a `pinned_comment` pointing to the full breakdown. AUTO in eval_package.py once `content/shorts_briefs.json` exists.
