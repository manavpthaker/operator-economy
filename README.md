# The Operator Economy

**Build. Own. Operate.**

YouTube channel + newsletter + blueprint library. AI business blueprints for people done with the broken job market.

- Channel: [YouTube Studio](https://studio.youtube.com/channel/UC7WsO7VW1E9vAYY_SCIOr0g) · ID `UC7WsO7VW1E9vAYY_SCIOr0g` · handle @operatoreconomy
- Domain: theoperatoreconomy.com *(purchase pending — [Vercel](https://vercel.com/domains/search?q=theoperatoreconomy.com), $11.25/yr)*
- Production engine: [`studio/`](studio/) — `originate.py` for long-form blueprints (see `studio/ORIGINATE.md`), `pipeline.py` for cutting Shorts from rendered videos. Vendored from the viddy repo 2026-07-02; this copy is canonical for OE, viddy remains for podcast clips.

## Thesis

The employment ladder broke, but AI collapsed the cost of building. The credible move is no longer *get hired* — it's *build your own economics*. You're already the operator. You just don't own anything yet.

Unlike everyone else saying this, we prove it: real companies, real numbers, real tools. Every video ships a downloadable blueprint.

## Format (per video)

1. **Hook** — the idea + a real revenue number (≤15s)
2. **Idea** — who it serves, why now (what AI unlocked)
3. **Evidence** — 2–3 real companies making money at this, unit economics with sources
4. **Stack** — the exact tools, costs, alternatives
5. **Playbook** — week 1 → month 1 → first customer
6. **Economics** — honest costs, realistic ranges, failure modes
7. **CTA** — blueprint download (email) + subscribe

## Repo map

| Path | What |
|---|---|
| `channel/positioning.md` | First-principles foundation (audience, message, naming rationale) |
| `brand/brand.md` | Voice + visual identity |
| `topics/queue.md` + `scoring.md` | Scored thesis backlog (v3) + rubric → feeds `studio/originate.py new` |
| `videos/` | One folder per published video: status, links, 24h/7d/28d metrics |
| `docs/pipeline.md` | Producing one video end to end (confidence-gated v3) |
| `docs/evals.md` | Gate rubrics + automated eval catalog + findings log |
| `docs/content-rubric.md` | 100-point craft rubric (publish gate ≥80 + zero kill-list) |
| `docs/automation-architecture.md` | v3 decision record: Claude-native orchestration, confidence gating, API-vs-Studio split, build order |
| `docs/kill-criteria.md` | 26-week decision gates (rate-based) |
| `research/strategy/` | Original opportunity report + lanes memo (July 2026) |
| `research/reports/` | 3 strategy + 3 craft + 3 automation deep-research reports |
| `research/synthesis.md` + `*-prompt.md` | Report syntheses and the reusable research prompts |
| `studio/` | Production engine: `originate.py` (long-form, evals, confidence), `pipeline.py` (Shorts), Remotion renderer |
| `studio/originate/<slug>/` | Per-episode working dir: research, script, confidence reports, derived content |

## Revenue model (in order of build)

Email list (blueprint lead magnets) → AdSense (~month 6+) → tool affiliates (20–30% recurring) → sponsors (~month 12+) → Grapevines funnel (secondary, always on).
