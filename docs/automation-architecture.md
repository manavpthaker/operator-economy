# Automation architecture (decision record) — July 2026

Synthesized from 3 automation research reports (`../research/reports/automation-report-{1,2,3}.md`). All three independently converged on the same spine; conflicts and their resolutions are logged at the bottom.

## The decision

**n8n (self-hosted, queue mode) orchestrates; the existing Python studio does the work; Postgres is the run ledger; Cloudflare R2 holds artifacts; Remotion Lambda renders; Slack carries Gates 1 & 3; a web form carries Gate 2 (it needs file uploads). The three human gates are permanent — automation reduces touches BETWEEN gates, never dilutes the gates themselves.**

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
| Orchestrator | n8n self-hosted, queue mode | Temporal only if this ever becomes multi-channel/client infra |
| State / artifacts | Postgres + Cloudflare R2 | run_id spans research→analytics |
| Research | Exa (discovery) + Perplexity Sonar (cited answers), one adapter | brief = raw material; Gate 1 verifies claims — no API output publishes unread |
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

## Build order (4 weekly phases)

1. **Spine + audit:** n8n queue mode + Postgres + R2; run-manifest/state model (single run_id, idempotent workers); **submit YouTube API compliance audit + phone verification**; one manual end-to-end pass through n8n, no gates.
2. **Gates first, depth later:** Gate 1 & 3 Slack approve/reject with resume webhooks (gate message = eval scores + unresolved claim registry, not the whole script); Gate 2 upload form; Error Trigger workflow that DMs on any failure.
3. **Middle automation:** ElevenLabs v3 + loudnorm chain; Templated + legibility QA; Pexels/Pixabay pulls; Remotion Lambda wired to R2; `videos.insert` with disclosure + scheduling. Threshold: full video reaches Gate 3 with <90 min total human time.
4. **Distribution + loop:** newsletter drafts + lead-magnet automation; Buffer queue; Shorts derivation handoff; weekly Analytics pull → topic-score suggestions. Threshold to trust the loop: two consecutive weeks where topic ranking correlates with realized CTR×retention. Run the **10-video sameness test** monthly (would an outsider call them one video repeated?).

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
