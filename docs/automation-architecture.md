# Automation architecture (decision record) — July 2026, v2

Synthesized from 3 automation research reports (`../research/reports/automation-report-{1,2,3}.md`), then **overruled on orchestration** after operator review.

## Research bias note (why we overruled)

All three reports recommended n8n. All three also pattern-matched "solo operator" to *non-technical creator needing a no-code tool*, and dismissed agent frameworks with an argument ("don't keep production state inside an agent") that doesn't apply here: our state is **files in a git repo**, not agent memory. The operator already runs multiple agentic workflows (Claude Code / Cowork: brownbot, BusyLobby ops). Everything n8n would provide — cron triggers, gate notifications, retries, sequencing — is already native to that stack, and the conversational gate ("rewrite beat 3" instead of an approve/reject button) is strictly better for an editorial pipeline. Lesson recorded for future research prompts: **state the operator's expertise explicitly** ("I operate Claude-based agent systems daily; assume expert; do not optimize for no-code").

## The decision (v2)

**Claude-native orchestration: Cowork/Claude Code sessions + scheduled tasks orchestrate; the Python studio does deterministic work (VO, render, publish); the git repo IS the run ledger and artifact store; gates are conversational reviews in Cowork — which the operator is in daily anyway. No new infrastructure. The three human gates are permanent — automation reduces touches BETWEEN gates, never dilutes the gates.**

The gates naturally chunk the pipeline into segments that each fit one agent session — the "durable workflow" problem n8n solves barely exists at 1–2 runs/week with human pauses built in:

| Segment | Runner | Trigger |
|---|---|---|
| Research → brief → script draft → evals → commit → notify | **Cowork scheduled task** (weekly). Agent does the web research itself — no Exa/Sonar subscription needed; claim registry built into the brief | Monday cron |
| GATE 1 | Conversational session: POV pass with the agent, edits applied live, evals re-run | Operator |
| VO + asset plan (`originate.py continue`) | Studio scripts, run by agent or operator (needs local API keys) | Post-gate |
| GATE 2 | Review assets_review.md + record screen captures | Operator |
| Render (Lambda or local) → derive → evals | Studio scripts; long renders are detached processes the agent polls | Post-gate |
| GATE 3 + publish | Preview → `videos.insert` script (disclosure + publishAt) → ~10-min Studio finishing checklist | Operator |
| Analytics readback → topic-score suggestions | **Cowork scheduled task** (weekly) once Analytics API wired | Friday cron |

What this deletes from the reports' stack: n8n + VPS (~$10–25/mo), Postgres (git + JSON status files suffice at this scale), Slack gate plumbing, the web form (Cowork handles files), and likely the research API line ($5–30/mo) since agent research replaces it. **Revised cost: ~$60–120/mo at 1 video/week.** What we lose: unattended multi-step resilience — acceptable because every segment ends at a human gate anyway. Revisit only if this becomes multi-channel with >5 runs/week (then Temporal, not n8n).

```
weekly cron → research (Exa + Sonar, adapter-wrapped) → Claude brief w/ claim registry
→ script draft → rigor + craft evals (existing) → GATE 1 [Slack: approve/reject + eval scores + unresolved claims]
→ ElevenLabs v3 VO (pronunciation dict) → 2-pass ffmpeg loudnorm (-14 LUFS)
→ asset plan → Templated thumbnails + 320/180px legibility QA + Pexels/Pixabay b-roll
→ GATE 2 [web form: asset review + screen-capture upload]
→ Remotion Lambda render (assets from R2) → GATE 3 [Slack: preview URL + package]
→ videos.insert (containsSyntheticMedia + publishAt + thumbnails.set)
→ ~10-min Studio finishing pass (see API-vs-Studio split)
→ derive: Shorts (existing pipeline) + beehiiv/Kit newsletter + Buffer LinkedIn + lead-magnet automation
→ weekly Analytics API readback → topic-score suggestions (human reweights)
```

Key implementation rule (all 3 reports): **n8n never babysits long jobs inline.** Renders/VO are fired to workers with a `run_id`, then polled or resumed via callback webhook. Every worker idempotent; every stage behind a Python adapter with a manual fallback mode.

## Hard facts the design is built around (verified in reports)

- `videos.insert` dropped to ~100 units (Dec 4, 2025 quota cut); uploads have their own 100/day bucket. Quota is a non-issue at our cadence. **But: unaudited API projects upload PRIVATE-only — submit the compliance audit in week 1.**
- **`status.containsSyntheticMedia` IS settable via API** — disclosure is programmatic, set deterministically (realistic AI voice = yes; production assistance = no), reviewed at Gate 1. Disclosure alone carries no reach/monetization penalty.
- **Studio-only (no API):** end screens, cards, pinned comments, Shorts related-video link, Test & Compare A/B. → fixed ~10-min Gate 3 finishing checklist. Do not build automation for endpoints that don't exist.
- API uploads get identical algorithmic treatment to Studio uploads (the "API penalty" is folklore).
- **LinkedIn has NO personal-profile posting API.** Buffer (official API) or manual only. April 2025 enforcement sweep banned cookie/extension tools (Taplio X flagged by its own docs). Zero engagement/DM automation, ever.
- YouTube Analytics API now has what the rubric loop needs: retention curve (100 pts/video via elapsedVideoTimeRatio), returning viewers, and — since Jan 15, 2026 — impressions CTR by source + end-screen metrics. ~48h delay, sampled → weekly pulls only, human stays in the reweighting decision.
- ElevenLabs **pronunciation dictionaries only work on eleven_v3 / eleven_flash_v2** — other models silently ignore phoneme tags. Config updated to v3. PVC voice requires Creator plan ($22/mo); Free tier has no commercial rights.
- Remotion Lambda: ~$0.10 warm per 10-min HD video; video-in-video multiplies cost; assets served from R2 (zero egress). Solo operator is under the license threshold.
- Vendor churn is violent (Bing API dead, PlayHT winding down, Tavily acquisition pending, Kit +35% prices): research + TTS live behind swappable adapters.

## Tool picks

| Category | Pick | Notes / runner-up |
|---|---|---|
| Orchestrator | **Cowork/Claude Code + scheduled tasks** (v2 — see above) | Temporal only if multi-channel >5 runs/week; n8n rejected |
| State / artifacts | **Git repo + videos/<slug>/status.json**; R2 only as Lambda asset bucket | reports' Postgres overruled — over-engineered at this scale |
| Research | **Agent-native research in Cowork** (like the pilot brief); Exa/Sonar only if volume outgrows sessions | brief = raw material; Gate 1 verifies claims — nothing publishes unread |
| VO | ElevenLabs **v3** + finance pronunciation dictionary + 2-pass loudnorm | Cartesia = latency tool, irrelevant offline; PlayHT = deprecation risk |
| Render | Remotion Lambda | keep local render as fallback |
| Thumbnails | Templated ($29/1k renders) + custom 320/180px downscale QA | Bannerbear ($49) if signed URLs needed |
| B-roll | Pexels + Pixabay APIs (free, commercial-OK) | log source+license+date per asset; no faces without vetting (no model releases, Content ID claims possible) |
| Screen capture | Human at Gate 2 | Playwright only for surfaces we own; two breaks = permanent revert to human |
| Publish | Data API v3 + Studio finishing pass | audit first; phone-verify for custom thumbnails |
| Email | **Decide at build:** beehiiv preferred, but reports conflict on whether draft-creation API is Enterprise-gated → test on free tier first; fall back to Kit if gated | landing page: native beehiiv/Kit page (email traffic converts ~19% median vs 6.6% all-industry) |
| LinkedIn | Buffer | manual is acceptable; never scripts/extensions |

## Cost (all three reports agree, ~$15 spread)

~**$85–170/mo at 1 video/week**, ~**$130–230/mo at 2/week** — inside budget with headroom. Dominated by fixed SaaS (ElevenLabs $22, Templated $29, email $0–43, VPS ~$10, Buffer $0–6, Claude $20–40); render compute is pennies. Levers: email tier + research volume.

## Build order (v2 — 4 weekly phases)

1. **Keys + audit + first live run:** set ANTHROPIC/ELEVENLABS keys locally, ElevenLabs Creator plan + PVC voice clone + finance pronunciation dictionary; **submit YouTube API compliance audit + phone verification** (no timeline guarantees — start now); run the pilot through Gates 1–2 for real.
2. **Weekly kickoff scheduled task:** Cowork task (Monday) — pick top queue topic, agent research → brief with claim registry → script via studio prompts → both eval suites → commit → notify Gate 1 pending. Plus `status.json` per video (stage, scores, dates) as the lightweight ledger.
3. **Deterministic middle:** loudnorm chain into generate_vo; thumbnail templating (Templated or Remotion stills) + 320/180px legibility QA script; Pexels/Pixabay fetch for originate; `upload_youtube.py` (`videos.insert` + `containsSyntheticMedia` + `publishAt`) + Studio finishing checklist. Threshold: full video reaches Gate 3 with <90 min total human time. Lambda only when local render time actually hurts.
4. **Distribution + loop:** newsletter draft handoff (test beehiiv API on free tier vs Kit), Buffer queue, Shorts derivation; Friday analytics scheduled task → topic-score suggestions (human reweights). Threshold to trust the loop: two consecutive weeks where topic ranking correlates with realized CTR×retention. Run the **10-video sameness test** monthly (would an outsider call them one video repeated?).

## Top risks + guardrails (consensus of all three)

1. **Citation drift / unverified claims shipping** → claim registry per run (each publish-critical sentence: source URL + excerpt + verified/weak/remove status); Gate 1 shows only unresolved claims.
2. **Template sameness → channel-wide inauthentic-content demonetization** → rotate thumbnail/title framing, "distinct angle" rule at Gate 1, monthly 10-video test. Enforcement is real: channels with millions of subs removed; the pattern (not AI use) is what kills.
3. **Synthetic-VO trust decay** → PVC voice, pronunciation dictionary, mastering; periodically A/B intro retention vs a human-read baseline.
4. **Hidden manual work from missing API surfaces** → the deliberate API-vs-Studio split above; a checklist, not wishful automation.
5. **Maintenance debt > time saved** → automate only deterministic weekly-repeating steps; humans keep POV, verification, final visual judgment, preview. Any automation that breaks twice reverts to manual permanently.

## Conflicts resolved

| Question | Positions | Resolution |
|---|---|---|
| Email platform | R1: Kit (beehiiv create-post = beta/Enterprise-only) · R2/R3: beehiiv | Test beehiiv draft API on free tier at build; Kit if gated. Flagged, not assumed |
| Research provider | R1: Exa · R2: Perplexity Sonar (best citations) · R3: Exa/Tavily | Both behind one adapter: Exa discovers, Sonar answers-with-citations; churn-proof by design |
| Thumbnails | R1: Bannerbear · R2/R3: Templated | Templated ($29 vs $49, same 1k renders) |
| Returning viewers via API | R1: unverified · R2: available (`newVsReturning`) + Jan 2026 CTR metrics | Trust R2 (more specific/recent), verify in phase 4 |
| Gate 2 medium | R1: Slack+review UI · R3: web form | Form (needs file upload) |
