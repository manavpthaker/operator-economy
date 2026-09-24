# Topic scoring rubric (100 pts) — v4, re-weighted 2026-08-10

| Factor | Pts | Notes |
|---|---|---|
| Search demand | **35** | YT + Google volume for the idea and its query patterns ("how X makes money", "start X with AI"). **Score 0 without a named target query and a volume figure.** Not scoreable on intuition |
| Competition gap | 20 | Existing coverage depth — listicle-only coverage scores high; a dedicated quality breakdown scores low |
| Evidence availability | 20 | Can we name 2–3 companies with sourced revenue/economics? No evidence = no video. Both a low end and a high end, each with a source URL, at intake |
| POV strength | 15 | Manav operator experience (hospitality, product, AI implementation). This is the moat — weight it |
| Affiliate/stack potential | **5** | Do the blueprint's tools pay recurring commissions? |
| Derivation richness | **5** | Does it yield strong LI posts/newsletter angles (career-transition resonance)? |

**Produce at ≥ 65. Archive below 50.** Re-score monthly against analytics (retention by section, capture rate by topic).

## What changed in v4 and why

Search demand moved 25 → 35. The ten points came out of affiliate potential (10 → 5) and
derivation richness (10 → 5).

The reason is the measured constraint. Five episodes in, scripts pass their evals and cards pass
the fact gate, and the funnel dies at the click: EP002 took 288 impressions to 0.7% CTR, EP003
took 160 to 0.0%. Healthy is 4%. Against that, the two demoted factors are scoring things that
either do not bind yet or already work:

- **Affiliate potential** prices a monetization path that needs traffic to be worth anything. At
  current volume it is scoring a benefit the channel cannot collect.
- **Derivation richness** was a real risk when the five-surface derivation was unproven. It is
  proven; `derive_content.py` produces the blueprint, newsletter, LinkedIn set, shorts briefs and
  trailer brief on every run. Scoring it heavily now rewards a solved problem.

**Evidence availability (20) and POV strength (15) were deliberately left alone.** Both are hard
gates wearing the costume of scored factors. Evidence below the bar means `eval_script.py` fails
the low-end/high-end span check, and POV is both the monetization moat and the YouTube
inauthentic-content-policy shield. Neither should be traded for reach.

## Scoring search demand

35 points, banded so it stays honest:

| Band | Pts | Meaning |
|---|---|---|
| Validated pattern, 20K+/mo | 30–35 | A query family already researched in `../docs/growth-strategy.md` |
| Named query, 5–20K/mo | 20–29 | Real volume, verified, narrower family |
| Named query, 1–5K/mo | 10–19 | Thin but real; needs the competition gap to carry it |
| Named query under 1K/mo | 1–9 | Effectively a thesis episode; must earn its slot elsewhere |
| No named query | **0** | Not scoreable. Send it back to intake |

The validated patterns already on file: "how [AI company] makes money" at 45 to 65K/mo,
"[company] business model" at 35 to 50K/mo, "how Cursor makes money" at 5 to 9K/mo.

## The owner's override still stands

EP005 was chosen on 2026-08-08 by Manav without a score, and the queue recorded that the owner's
call supersedes the ≥65 rule. That remains true. The rubric ranks candidates; it does not
outrank the person running the channel. An override should be written down as one, the way EP005's
was, so a later re-score does not mistake it for a scoring result.

## Revisit trigger

This weighting is a response to a CTR problem. If browse CTR clears roughly 4% and holds for three
episodes, the constraint has moved and the weights should move with it: search demand back toward
25, and the ten points returned to whichever factor the analytics say is binding then. Do not
leave a re-weight in place after the condition that justified it has passed.
