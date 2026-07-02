# Three Gates, Everything Else Automated

**Automating The Operator Economy Pipeline — a tool-and-architecture decision document**

> **BLUF.** Build on n8n (self-hosted) as the orchestrator, keep your three human gates, and move rendering off your machine to Remotion Lambda. That stack lands at roughly **$85–130/mo at 1 video/week** and **$130–210/mo at 2/week** — inside your $100–300 budget with headroom. The hard constraints that shape every decision: YouTube's `videos.insert` is capped at **100 uploads/day** and the AI-disclosure flag *is* settable via API (the `status.containsSyntheticMedia` boolean), LinkedIn has no personal-profile posting API so scheduling tools are the only ToS-safe route, and YouTube's 2025–2026 "inauthentic content" enforcement makes your evidence-first, human-gated model a monetization asset — as long as you never let the gates collapse.

| Metric | Value | Note |
| --- | --- | --- |
| YouTube upload cap | 100/day | `videos.insert` hard limit |
| Render cost / 10-min video | ~$0.10 | Remotion Lambda, warm |
| ElevenLabs / 1K chars | $0.10 | Multilingual v2/v3 |
| Human gates kept | 3 | ~60–90 min/video |

---

## I. Orchestration & Human Gates

### 1. Recommendation: n8n self-hosted, Python for the heavy steps

**n8n is the orchestrator; your existing Python does the LLM/render logic behind HTTP nodes.** n8n is a self-hosted, node-based automation tool that excels at connecting APIs, webhooks, timers, and Slack — exactly the "business glue" between your steps. It is not a durable-execution engine, so you do not lean on it for state during a 30-minute render.

- Run n8n in **queue mode** (main pod + worker pods, backed by Postgres for definitions/execution history and Redis for the job queue). This is the documented production topology and is what keeps long jobs from blocking the UI.
- Wrap each expensive step (script gen, VO, asset plan, render trigger) as a Python service called via n8n's HTTP Request node with **Retry on Fail** set. Your Python already exists — n8n just sequences and notifies.
- State lives in Postgres + your object store, *not* in n8n memory. n8n has no automatic checkpoint/resume, so design each node to be idempotent and re-runnable from its inputs.

### 2. Why not the alternatives

**Each competitor solves a problem you do not have, at a cost you do not want.**

- **Temporal / cron + Python:** Temporal is the gold standard for durable, resume-after-failure workflows (full event-history replay, automatic activity retries with backoff, 51,200 events/execution before `continue-as-new`). But it is code-first with a steep learning curve and no UI — overkill for a solo operator running ~1–2 pipelines/week. Keep it in your back pocket only if reliability becomes the bottleneck.
- **Make:** Hosted and easy, but per-operation pricing punishes multi-step LLM chains and you lose the self-hosted cost control that keeps you in budget.
- **GitHub Actions:** Fine as a *render runner* (see §3), but its 6-hour job ceiling, weak human-in-the-loop story, and awkward long-lived state make it a poor primary orchestrator.
- **Agent frameworks (Claude Agent SDK, scheduled agent tasks):** Great for the *reasoning* inside a step (draft, critique, asset planning), wrong layer for scheduling, retries, and gate notifications. Use them as tools n8n calls, not as the spine.

### 3. Human-in-the-loop gate pattern

**Use n8n's Wait-for-Webhook node with Slack approve/reject buttons for Gates 1 and 3; use a lightweight web form for Gate 2 (asset review + screen-capture upload).** The proven lean pattern: the workflow posts a Slack message with two buttons whose payloads hit a resume webhook, then pauses indefinitely until you click.

- **Gate 1 (POV/rigor):** Slack message links to the draft in your doc store + eval scores; Approve resumes to VO, Reject routes back to a revision loop with your inline notes.
- **Gate 2 (assets + screen recs):** a small web dashboard (n8n Form Trigger or a static page hitting the resume webhook) shows the asset plan and accepts your recorded screen-capture files, since a Slack button cannot carry uploads.
- **Gate 3 (preview):** Slack message with the rendered MP4 preview URL; Approve triggers publish.
- **What breaks at scale:** n8n's visual flows turn into "spaghetti" as branches and error handling grow. Mitigate with sub-workflows treated as modules and an Error Trigger workflow that DMs you on any failure. Because n8n won't auto-resume, a worker crash mid-run means manual diagnosis — acceptable at 1–2 runs/week, painful beyond ~10.

---

## II. Render & Voice — Your Two Cost Centers

### 4. Remotion Lambda render cost

Measured Lambda cost by composition type (2048 MB, us-east-1, warm):

| Composition | Warm Lambda cost |
| --- | --- |
| Hello World | $0.001 |
| 1-min (embedded video) | $0.017 |
| 10-min HD | $0.103 |
| 10-sec 4K | $0.013 |

*Fig. 1 — Compute only; excludes S3 egress, storage, CloudWatch, and the Remotion company license (required at 4+ people, not you as a solo).*

### 5. Move rendering off your machine

**Keep Remotion, render on Lambda, not locally.** Remotion's React-based model already fits your data-driven chart/motion templates, and Lambda distributes a render across many functions (up to ~200x concurrency), turning a long local render into minutes. At your volume the compute is negligible — cents per video.

- **Cost driver to watch:** embedding video-in-video (b-roll clips) multiplies cost — a 1-min video with embedded footage jumped to ~$0.02, and heavier compositions scale from there. Data-driven charts and motion graphics stay cheap; wall-to-wall stock footage does not.
- **Runner-up:** Motion Canvas (open-source, animation-first) or a Lottie pipeline. Both are viable but abandon your existing Remotion investment for marginal gain. No change recommended.
- **Failure mode:** cold-start latency and S3 egress on asset-heavy renders. Pre-warm and co-locate assets in the same bucket/region as the Lambda.

### 6. ElevenLabs at your volume

**Stay on ElevenLabs; the Creator plan ($22/mo, ~100K credits) covers ~20–25 five-minute narrated videos.** At ~50 min/month of VO you are comfortably inside Creator. Multilingual v2/v3 is $0.10 per 1K characters (1 char = 1 credit); Flash/Turbo is ~$0.05 and half the credits if you ever need drafts fast.

- **Voice cloning:** use Professional Voice Cloning (PVC), which requires Creator or above — its stability across long-form narration is audibly better than Instant cloning and matters for a recurring, evidence-first voice.
- **Finance pronunciation:** apply pronunciation dictionaries for tickers and finance terms so "PPI," "ARR," and tickers read correctly and consistently.
- **Commercial-rights gotcha:** the Free plan has *no* commercial rights. You must be on Starter ($5) minimum to monetize; Creator is the right floor for PVC.
- **Alternatives:** Cartesia and OpenAI TTS are cheaper/faster but the retention penalty for a synthetic-sounding VO on an evidence channel is a real risk — ElevenLabs' naturalness is the reason to pay. Post-process with an ffmpeg `loudnorm` chain to YouTube's −14 LUFS, plus de-essing, before it ever hits the render.

---

## III. Publishing — The API You Must Design Around

### 7. YouTube upload cap is the real ceiling

**Every Google Cloud project gets 10,000 units/day, but uploads live in a separate bucket: 100 `videos.insert` calls/day.** At 1 long-form + 3–5 Shorts/week you are nowhere near this — but note new/unaudited projects have their uploads forced to **private** until you pass the compliance audit, and there is no self-service way to buy more quota.

- **Pass the audit early.** Submit the API Services Audit & Quota Extension form before you rely on public uploads; reviews have no guaranteed timeline and data-heavy use cases get rejected. A single-channel publishing use case is the easy case.
- **Watch `search.list`, not uploads.** If you use YouTube search for research or outlier discovery, each call costs 100 units — 100 searches drains the whole daily quota. Cache aggressively and prefer `videos.list` (1 unit) once you have IDs.

### 8. The AI-disclosure flag IS settable via API

**The video resource exposes `status.containsSyntheticMedia` (boolean) — you can set the altered/synthetic-content disclosure programmatically at upload, no manual Studio step required.** This resolves the open question in your brief directly from the official API reference.

- **2026 change to know:** YouTube now *auto-applies* AI labels when it detects significant photorealistic AI use, and labels moved to a prominent position (below the player for long-form, overlay for Shorts). Labels created by YouTube's own tools (Veo, Dream Screen) or via C2PA metadata are permanent.
- **Good news for your brand:** YouTube states the disclosure label alone does *not* change recommendations or monetization eligibility. Disclose honestly; it costs you nothing algorithmically.
- **What the API does NOT expose:** end screens/cards, pinned comments, Shorts "Related Video" linking, and Test & Compare (title A/B) are not settable through Data API v3. Chapters work via timestamps in the description. Plan these as prepared-metadata + a brief manual pass in Studio.

### 9. API upload vs. Studio: what operators actually do

**Recommendation: API-upload the file + full metadata, then do a <5-minute Studio pass for the API-blind fields (end screens, cards, pinned comment, A/B titles).** This is the hybrid most multi-channel operators settle on — the API removes the tedium, the manual pass covers the gaps and doubles as a final human sanity check that reinforces authenticity signals.

- There is no credible evidence that API-uploaded videos face different *algorithmic* treatment than Studio uploads — the difference is the private-by-default restriction until audited, which is a compliance gate, not a ranking penalty. Treat "API uploads get suppressed" as folklore.
- TubeBuddy/vidIQ bulk tools add value for research and packaging QA, not as your upload path — your n8n + API flow is cheaper and more controllable.

---

## IV. Research, Assets & Distribution

### 10. Research brief automation

**Use Exa or Tavily as the retrieval layer, then have your Claude step synthesize the cited brief — never publish claims straight from a search API.** For an evidence-first channel, the search API's job is to surface and extract sources; the citation-verification job stays with you.

- **Exa** ($7/1K searches, +$1/1K for contents): neural/semantic search, strong for discovery and "find similar" competitive angles. **Tavily** ($0.008/credit; basic = 1 credit, advanced = 2): cheapest per-query, framework/MCP integrations, but returns chunks unless you set `include_raw_content`.
- **Perplexity Sonar** returns grounded answers with inline citations out of the box, but its API is **rate-limited to ~50 calls/min** and reads more like a demo than a production endpoint — fine for a weekly batch, risky for bursts.
- **Cost per research run** at a few dozen queries: well under $1. The expensive part is the LLM synthesis, not the search.
- **Verification gate:** require every claim in the brief to carry a source URL, and have Gate 1 spot-check them. No API "reliably produces cited claims" you can trust unread — teams verify before publish, full stop.
- **Outlier tools** (1of10, ViewStats, vidIQ): treat as manual research inputs. Programmatic access is limited/gated and YouTube's own `search.list` quota makes DIY outlier mining expensive.

### 11. Asset generation: thumbnails, b-roll, screen capture

**Thumbnails: Templated or Bannerbear from a branded template. B-roll: Pexels/Pixabay for free commercial-safe API footage. Screen recs: keep human (Gate 2), optionally Playwright-assisted.**

- **Thumbnails —** Templated ($29/mo for 1,000 renders, layers-object API, n8n + MCP support) undercuts Bannerbear ($49/mo for 1,000). Bannerbear wins only if you need signed URLs or its built-in screenshot endpoint. Generate from a template, then run an automated legibility check by downsampling to 320px/180px and flagging low text-contrast — but let a human make the final pick, since near-identical thumbnails are a top demonetization signal (§13).
- **B-roll —** Pexels and Pixabay APIs are free and their licenses permit commercial YouTube use, which makes them the safe default; Storyblocks/Artgrid are higher-quality but subscription-gated and their API/commercial terms need per-plan checking before you automate. Verify license terms per asset for a monetized channel.
- **Screen recording —** Playwright-driven capture produces clean, repeatable product-demo footage and is viable quality. But your Gate 2 already has a human recording screens — keep that. Automate only the deterministic, repeatable captures; leave anything requiring judgment to the human.

### 12. Distribution: email, lead magnet, LinkedIn

**beehiiv for newsletter + lead-magnet automations; a scheduling tool (Buffer/Taplio) for LinkedIn because there is no personal-profile posting API.**

- **Email —** beehiiv is the newsletter-business fit (blog + email marketing + API + built-in ad network for future sponsorships); Kit (ConvertKit) is stronger for course-seller automations. At <5K subs both have usable free/low tiers. Use the API to create newsletter drafts from your markdown and to fire the lead-magnet delivery automation.
- **Lead magnet —** fastest conversion path is a native beehiiv (or Kit) landing page with an email-gated download automation — no separate Carrd + glue needed. Hold yourself to the 0.5–2% capture-per-view benchmark and instrument it.
- **LinkedIn —** the API reality is stark: the Profile API is partner-restricted and there is **no public API to post to a personal profile** (documents/carousels included). ToS-safe automation means a scheduler like Buffer (now with LinkedIn personal-profile support) or Taplio. Do *not* script the site directly — that violates ToS and risks the account.

---

## V. What NOT to Automate — Your Brand Depends on It

### 13. The 2025–2026 enforcement reality

**YouTube renamed "repetitious content" to "inauthentic content" and has removed AI-heavy channels with millions of subscribers and billions of lifetime views.** One documented history-narration channel reportedly earned ~$170K (May–Dec 2025) before being pulled — killed not by using AI, but by the *pattern*: near-identical thumbnails, one recycled title template, and static slideshow construction. AI is explicitly allowed; interchangeability is what gets punished.

- **The four behaviors that trigger enforcement:** full automation (no human judgment anywhere), script recycling, upload flooding (many near-identical variants), and mass-produced templates. Your gates and cadence already avoid all four — do not let scale pressure erode them.
- **The 10-video test:** pull your last 10 uploads side by side. If an outsider would call them "one video repeated ten times," you are at risk. Run this monthly.

### 14. Top 5 automation risks & guardrails

**Each risk below is specific to an "evidence-first, human-authored" brand — the guardrail is what keeps the automation from undermining the positioning.**

1. **Unverified AI claims reach publish.** Guardrail: Gate 1 blocks on a source-check; every claim carries a URL; no brief ships un-spot-checked. Your eval gates that score rigor are the moat — keep them mandatory, not skippable.
2. **Template sameness → inauthentic-content flag.** Guardrail: rotate thumbnail composition and title framing; enforce a "distinct angle per video" rule at Gate 1; run the 10-video test monthly.
3. **Synthetic-VO retention penalty.** Guardrail: PVC voice + pronunciation dictionaries + −14 LUFS mastering; periodically A/B intro retention to confirm the voice isn't costing you the first 30 seconds.
4. **Silent pipeline failure ships a broken video.** Guardrail: Gate 3 preview is human-approved and never auto-bypassed; n8n Error Trigger DMs you on any node failure; each step idempotent so re-runs are safe.
5. **Maintenance debt exceeds time saved.** Guardrail: automate only steps that are deterministic and repeat weekly; keep judgment steps (POV, screen recording, final pick) human. If a piece of automation costs more to maintain than the 8–10 hrs/week it saves, cut it. The successful lean operators keep humans exactly where taste and verification live.

---

## VI. The Architecture, Build Order & Cost

### 15. End-to-end architecture for your flow

**Orchestrator: n8n (queue mode). State: Postgres (workflow/run state) + S3-compatible object store (scripts, VO, assets, renders). Notifications: Slack for Gates 1 & 3, a web form for Gate 2.**

- **Research →** n8n cron fires weekly → Exa/Tavily retrieval → Claude synthesizes cited brief → stored in object store.
- **Draft → GATE 1 (Slack):** Claude drafts → your eval gates score → Slack approve/reject; reject loops to revision.
- **VO →** ElevenLabs PVC + pronunciation dict → ffmpeg loudnorm → stored.
- **Asset plan → GATE 2 (web form):** Claude plans charts/b-roll/screen-recs → you upload screen captures via form → resume webhook.
- **Render → GATE 3 (Slack):** Remotion Lambda 16:9 render → preview URL in Slack → approve → publish.
- **Publish →** `videos.insert` with full metadata + `containsSyntheticMedia=true` → <5-min Studio pass for end screens/cards/A-B → derive Shorts + beehiiv newsletter draft + Buffer/Taplio LinkedIn queue + lead-magnet automation.

### 16. Build order — 4 weekly phases

- **Week 1 — Spine:** stand up n8n in queue mode (Postgres + Redis), wire object storage, submit the YouTube API compliance audit. Get one manual end-to-end run passing through n8n with no gates yet.
- **Week 2 — Gates:** build Gate 1 & 3 Slack approve/reject + resume webhooks, and the Gate 2 upload form. Add the Error Trigger DM workflow. This is the highest-value week — gates before automation depth.
- **Week 3 — Assets & voice:** connect ElevenLabs PVC + loudnorm, Remotion Lambda render, Templated thumbnails with 320/180px legibility QA, Pexels/Pixabay b-roll. Publish via `videos.insert` + disclosure flag.
- **Week 4 — Distribution & loop:** Shorts derivation, beehiiv drafts + lead magnet, Buffer/Taplio LinkedIn queue, and the analytics readback (below). Run the 10-video test and tune.

### 17. Analytics readback → self-correcting loop

**The YouTube Analytics API (OAuth, owner-only) exposes the metrics your rubric cares about — impressions CTR by traffic source, audience-retention curve points, returning viewers, card/end-screen CTR — but with sampling and reporting delay.** It is a separate product from Data API v3.

- **Caveat:** data lags ~2–3 days and can be sampled; pull weekly, not real-time, and don't reweight your topic model on a single video's noisy early numbers.
- **Closed-loop pattern:** pipe weekly Analytics into a topic-scoring sheet that nudges next week's research prompts (e.g., down-weight formats with weak 30-sec retention). Keep the human in the reweighting decision — this is a suggestion engine, not an autopilot. Genuinely closed-loop content ops is rare in practice precisely because the metrics are noisy; treat it as a dashboard that informs Gate 1, not a controller.

### 18. Monthly cost scenarios

Estimated all-in monthly cost at 1 vs 2 videos/week. Both land inside the $100–300 budget.

| Cadence | Low estimate | High estimate |
| --- | --- | --- |
| 1 video / week | $85 | $130 |
| 2 videos / week | $130 | $210 |

*Fig. 2 — Ranges reflect research-API and thumbnail-render usage. ElevenLabs Creator, beehiiv, and a scheduler are near-fixed; Lambda render is cents; the swing is research query volume.*

### 19. Where the money goes

| Line item | Monthly |
| --- | --- |
| ElevenLabs Creator (PVC, ~100K credits) | $22 |
| beehiiv (starter/growth, <5K subs) | $0–42 |
| LinkedIn scheduler (Buffer/Taplio) | $6–40 |
| Templated thumbnails | $29 (or free tier early) |
| Research APIs (Exa/Tavily, weekly runs) | $5–30 |
| Remotion Lambda + S3 (AWS) | $1–10 |
| n8n hosting (small VPS) | $6–20 |
| LLM (Claude) synthesis + drafting | $15–40 |
| **Total, 1 video/week** | **~$85–130** |
| **Total, 2 videos/week** | **~$130–210** |

### 20. Tool decision table

| Category | Pick / Runner-up | API limit | Failure mode |
| --- | --- | --- | --- |
| Orchestration | n8n / Temporal | No auto-resume; queue mode for scale | Worker crash = manual re-run; visual sprawl |
| Research | Exa / Tavily | Exa $7/1K; Perplexity ~50 rpm | Uncited/hallucinated claims if unverified |
| Render | Remotion Lambda / Motion Canvas | ~200x concurrency | Video-in-video multiplies cost; cold starts |
| Voice | ElevenLabs (Creator, PVC) / Cartesia | $0.10/1K chars (v2/v3) | Synthetic-sound retention penalty |
| Thumbnails | Templated / Bannerbear | 1,000 renders @ $29 | Sameness → inauthentic flag |
| B-roll | Pexels+Pixabay / Storyblocks | Free tiers, commercial-OK | License drift on paid libraries |
| Publish | YouTube Data API v3 | 100 uploads/day; audit for public | Private-by-default until audited |
| Email | beehiiv / Kit | API drafts + automations | Deliverability on cold list |
| LinkedIn | Buffer/Taplio / (no direct API) | No personal-profile posting API | Direct scripting = ToS/account risk |
| Analytics | YouTube Analytics API | OAuth owner-only; sampled, delayed | Overfitting to noisy early data |

---
*Drafted with Dia*
