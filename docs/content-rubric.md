# Content rubric (pre-publish, 100 points)

Merged from 3 craft research reports (`../research/reports/craft-report-*.md` + pasted playbook), July 2026. Applied to every script + package at Gate 1 alongside the rigor evals. Automated subset lives in `studio/scripts/originate/eval_package.py`; the rest is the human pass.

**Publish gate: ≥80/100 AND zero kill-list items. Hook and Structure blocks are hard blocks below 15/25.**

Master platform context (highest confidence, YouTube-official): the recommender now optimizes *satisfaction and session contribution*, not raw watch time or CTR. Native A/B testing picks winners by **watch time per impression** — honest packaging structurally wins. 5% CTR with 60% retention beats 10% CTR with 30% retention.

## I. Hook — 25 pts (hard block <15)

| Criterion | Pts | Check |
|---|---|---|
| Premise/payoff fully stated by 0:15 (~37 words) | 10 | AUTO (graded: ≤15s=10, 15–25s=5, later=0) |
| Opens with a named archetype, never "hey/welcome/today/in this video" | 5 | AUTO (banned openers) + HUMAN (archetype named in package) |
| Contains a specific number in first two sentences | 5 | AUTO |
| On-screen text carries the premise (mute viewers) | 3 | HUMAN (asset_hint on hook beat must specify text/graphic) |
| No overpromise the body can't cash | 2 | HUMAN |

Approved archetypes: stakes-first cold open (fall-before-rise) · number-first anchor · contrarian snapback · structural paradox · quantitative abstract · open-loop ("I looked at 12; one survived") · authority-led. Write the hook LAST, after the script.

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
| Visual state changes ≤15s in intro, ≤40s in body (asset variety; no 3+ consecutive same-type assets) | 6 | AUTO (proxy) + HUMAN |
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

Chapters: reports split (help/hurt/conditional) → we skip chapters on narrative episodes, allow non-spoilery chapters on framework-heavy ones. CTA: mid-video 55–75% (strongest evidence) over final-30s-only. Thumbnail words: ≤3 target, 4 max. The "70% at 0:30" rule is folklore — useful target, not doctrine; our own analytics arbitrate.
