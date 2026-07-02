# End-to-end pipeline automation decision document

## Recommendation

For your exact setup, the best fit is **n8n self-hosted as the conductor, with your existing Python services doing the heavy work**, and **Postgres + object storage as the run ledger and artifact store**. That gives you durable waits for the three approval gates, low monthly cost, and enough statefulness to survive multi-step weekly runs without forcing you into a new enterprise platform or a fragile agent-only stack. citeturn3search2turn3search10turn3search14turn2search0turn4search3turn4search20turn5search0turn5search1

The short version is: **use n8n for orchestration and approvals, keep Python for research/script/evals/Remotion wrappers, keep GitHub Actions for deploys only, and do not put your core production state inside an agent framework**. Temporal is the technically strongest workflow engine here, but its managed pricing floor and self-hosting overhead are hard to justify for a solo channel on a $100–300/month all-in budget. citeturn3search2turn3search27turn4search1turn4search3turn4search20turn5search0turn5search1

## Why this stack fits your workflow

**n8n** is the best pragmatic orchestrator for a solo operator because it gives you queue mode, waiting states, and human-in-the-loop pauses without making you rebuild your existing Python pipeline inside a workflow engine. Its queue mode is explicitly positioned as the scalable mode, and n8n’s docs note waiting states for webhook/form/human-in-the-loop patterns. That maps cleanly to your three gates: script approval, asset approval, and preview approval. citeturn3search2turn3search6turn3search10turn3search14

**Make** is weaker for your use case because its pricing is operation-based and its official pricing page caps a single scenario execution at **40 minutes** even on paid plans. That is close enough to your render window that it creates avoidable fragility, even though Make does support automatic retry of incomplete executions caused by rate limits, connection errors, and module timeouts. citeturn2search0turn1search3

**Temporal** is the strongest option on pure workflow engineering terms: durable execution, retry policies, signals for approvals, and long-running human-in-the-loop patterns are exactly what it is built for. But Temporal Cloud has a **$100/month Essentials floor** and is priced separately from your worker infrastructure, which makes it harder to defend for a one-channel operation unless you already know you want a multi-channel or client-services control plane later. citeturn4search1turn4search3turn4search6turn4search9turn4search20

**GitHub Actions** should stay in your stack, but as the **CI/deploy layer**, not the business-process orchestrator. It is excellent for testing prompts, validating render templates, packaging containers, and deploying workers; it is not a great home for multi-day approval-centric state. That distinction matters because your process is less “build pipeline” and more “durable editorial workflow.” citeturn13search17turn4search19

**Agent frameworks** are the wrong place to keep production state. Anthropic’s Agent SDK is real and useful, and Claude routines can run on Anthropic-managed infrastructure with scheduled triggers, but those surfaces are optimized for agent execution, not as a replacement for a durable workflow ledger with auditable approval gates. They are best used as workers inside the pipeline, not as the pipeline itself. citeturn5search0turn5search1turn6search0

## Tool decision matrix

| Category | Recommended tool | Runner-up | Monthly cost | API / limit | Specific failure mode |
|---|---|---|---|---|---|
| Orchestration | **n8n self-hosted** | Python + Postgres + cron/RQ | Software: community/self-hosted; infra is a small VPS estimate rather than an n8n license cost. n8n Cloud pricing is execution-based, but self-hosting avoids that model. citeturn3search0turn3search16 | Queue mode, waiting states, concurrency controls. citeturn3search2turn3search10turn3search14 | If you run heavy jobs inline instead of async callback/poll patterns, you create stuck executions and brittle retries. |
| Visual automation alternative | **Not recommended as primary: Make** | — | Core plan starts at **$12/mo** for 10k credits; Pro **$21/mo** for 10k. citeturn2search0 | Make API rate limits shown on pricing: **60/120/240/min** by plan; max scenario execution **40 min**. citeturn2search0 | 40-minute execution ceiling is too close to render times; operation-based billing punishes chatty media workflows. |
| Workflow-engine upgrade path | **Temporal later, not now** | — | Cloud Essentials is **$100/month minimum**. citeturn4search20 | Durable execution, retries, schedules, signals for approvals. citeturn4search1turn4search3turn4search6 | Great tech fit, poor economic fit right now; self-hosting adds ops debt for a solo operator. |
| Research search/citations | **Exa Search + Exa Deep** | Tavily | Exa free tier shows **20,000 requests/month free**; paid search **$7/1k requests**; Deep **$12/1k**; contents **$1/1k pages/type**. citeturn7search5turn7search13 | Default limits: **10 QPS** for search/findSimilar/answer, **100 QPS** for contents, **15 concurrent** legacy research tasks. citeturn7search1 | Search returns grounded links, but publish-safe claims still need your Gate 1 verification against primary sources. |
| Trends signal | **Google Trends API alpha if you get access** | Exa/Tavily + manual Trends UI | Official API exists but remains **alpha**. citeturn7search3turn7search23 | Access availability is gated by alpha enrollment. citeturn7search3turn7search23 | Availability risk; do not design your core weekly run around a surface you may not have. |
| Charts / motion / rendering | **Remotion** | Motion Canvas for special explainer segments | Remotion Lambda advertises render cost **from $0.01/min**, and example renders are measured in cents. citeturn28search4turn28search1 | Distributed Lambda rendering, progress polling. citeturn28search10turn28search16 | If you move too much video-inside-video or unoptimized media into compositions, cost and render time climb quickly. citeturn28search1turn28search13 |
| Custom vector explainer engine | **Not primary: Motion Canvas** | — | Free and open source. citeturn29search3turn29search1 | TypeScript animation library + editor. citeturn29search1 | Current ecosystem shows open issues around headless automation/rendering and export consistency, which is bad for weekly unattended runs. citeturn29search6turn29search4 |
| Micro-animation assets | **Lottie / dotLottie only for reusable micro-animations** | — | LottieFiles Individual starts at **$19.99/user/month** annually. citeturn28search0 | Programmatic tooling exists via dotlottie-js / relottie. citeturn28search3turn28search12 | Great for overlays, weak as a whole-video compositor; use as components inside Remotion, not as the pipeline. |
| Free B-roll source | **Pexels** | Pixabay | Pexels API is **free**. citeturn30search1 | Developer API available; Pexels license allows free personal and commercial use, no attribution required. citeturn30search1turn30search9turn30search20 | Free licensing is convenient, but there is no enterprise indemnification; avoid using it for sensitive brand/product implication shots when risk is high. |
| Free B-roll source | **Pixabay** | Pexels | Pixabay API is **free** and advertises unlimited requests. citeturn30search2turn30search13 | REST API; docs request that if you make use of the API, users should be shown where images/videos are from when search results are displayed. citeturn30search13 | Commercial use is available, but attribution/display expectations are less “drop-in invisible” than many people assume. |
| Premium B-roll | **Storyblocks API** | Artgrid manual | Storyblocks API is an enterprise/business solution; public self-serve API pricing is not exposed in the page captured here. Licensing is commercial and includes **$20,000 indemnification**. citeturn30search0turn30search18 | API exists for platforms/partners. citeturn30search0 | Licensing is safer, but economics and partnership overhead are usually wrong for a solo YouTube operation. |
| Thumbnails | **Bannerbear** | Figma export API | **$49/mo** Automate plan, **$149/mo** Scale, **$299/mo** Enterprise. citeturn32search3 | Image/video API credits; 30 trial credits. citeturn32search3turn32search11 | Template systems are stable, but quality drift still happens; automated legibility QA is mandatory before upload. |
| Design-source option | **Figma API only if you already design there** | Canva Connect | Figma pricing is seat-based; official pricing page is broad rather than API-specific. citeturn32search5 | Figma REST API rate limits changed in Nov 2025 and are plan/seat/endpoint dependent. citeturn32search1 | Figma users have reported long Retry-After windows and blocked image export calls; fine for low volume, risky as the only render path. citeturn32search9turn32search17 |
| Canva option | **Not recommended for this use as first choice** | — | Public pricing exists, but automation reality depends on Connect/private integrations. citeturn32search14turn33search6 | Export, autofill, asset upload APIs exist; e.g. export limit **750/5 min, 5,000/24h per integration**. citeturn33search1turn33search7turn33search9 | Strong API, but private integrations are positioned for enterprise teams and add platform friction you do not need at your current scale. citeturn33search17 |
| Voice | **ElevenLabs** | Cartesia | TTS API pricing: **$0.10 / 1,000 characters** for Multilingual v2/v3; **$0.05** for Flash/Turbo. citeturn35search1 | Character timestamps endpoint exists; pronunciation dictionaries supported; plan concurrency limits range from **2 to 15** depending on plan. citeturn37search8turn38search0turn37search17 | Main failure is concurrency/rate 429s; second failure is pronunciation dictionaries silently not applying to some models unless you use supported variants. citeturn37search0turn38search0 |
| Voice alternative | **Cartesia for latency-sensitive demo reads** | OpenAI request-based TTS | Cartesia pricing starts at **$5/mo** Pro with credits; free tier available. citeturn35search0 | Official public pricing page emphasizes credits and agent minutes; low-latency TTS product page claims ~40ms time-to-first-audio. citeturn35search0turn35search6 | Public rate-limit specifics were not captured in this research pass; do not choose it until you verify concurrency/voice-clone economics live. |
| Publishing | **YouTube Data API + Studio hybrid** | Human upload only | API itself is quota-based rather than paid; default project quota remains **10,000 units/day**, and `videos.insert` now uses a dedicated upload bucket with **100 calls/day** at **1 unit** quota cost in that bucket. citeturn12search1turn19search1 | Uploads, thumbnails, metadata, synthetic-media disclosure are supported. citeturn12search1turn12search2turn13search6 | Missing surfaces still force Studio use for some steps; unverified API projects created after July 28, 2020 are restricted to private uploads until audit. citeturn13search10turn14search3turn14search2 |
| Email platform | **Kit if full automation matters** | beehiiv if cost/growth matters more than API write access | Kit pricing is subscriber-based, but the exact official sub-5K price point was not captured in the snippets collected here. beehiiv Launch is **$0** up to **2,500 subs**; Scale starts at **$43/mo**. citeturn20search6 | Kit has a public API to create/update broadcasts and stats, with **120 req/60s by API key** and **600 req/60s by OAuth**. citeturn24search8turn24search1turn25search0turn25search5 | beehiiv’s `create post` endpoint is currently **beta and Enterprise-only**, which breaks a true no-touch newsletter draft pipeline. citeturn21search1turn26search0 |
| LinkedIn distribution | **Buffer + official LinkedIn connection** | Direct LinkedIn API if you already have approved access | Buffer supports LinkedIn Pages and personal profiles, including image/video/GIF/**document (PDF)** workflows. citeturn20search9turn20search17 | LinkedIn’s product catalog includes **Share** for posting content to a member profile; Posts API replaces ugcPosts. citeturn20search1turn20search4 | Avoid unofficial browser bots; LinkedIn is one area where staying inside official scheduler/API rails matters. Buffer explicitly documents suspension-avoidance best practices. citeturn20search9 |

## Recommended architecture for your exact flow

The architecture that best matches your current assets is:

**n8n self-hosted** as the workflow conductor  
**Python services** for research, scripting, scoring, audio mastering, asset planning, thumbnail QA, and YouTube/LinkedIn/email adapters  
**Remotion** for rendering, called asynchronously  
**Postgres** as the run ledger  
**S3/R2-compatible object storage** as the artifact store  
**Slack approval messages with deep links to a tiny review UI** as the three human gates  
**YouTube Data API + Studio hybrid** for publishing, because API coverage is incomplete for all of the post-upload polish you care about. citeturn3search2turn3search14turn28search10turn28search16turn12search1turn12search2turn13search10turn14search3

A clean run should look like this:

**Topic seed → evidence brief → script draft/evals → Gate 1 → voice render + mastering → asset plan → Gate 2 + human screen captures → Remotion render → Gate 3 → upload via API → Studio-only polish → shorts/posts/newsletter derivation → analytics readback.** The important implementation detail is that **n8n should never “babysit” long renders inline**. It should enqueue them to a Python worker, store a `run_id`, and then either poll status or resume from a callback webhook when the job completes. That is the pattern that keeps wait states cheap and recoverable. citeturn3search2turn3search10turn28search16turn4search1

The approval UX should be **Slack first, web second**. Slack gets you fast approve/reject buttons; the linked review page should show the load-bearing context for each gate:

- **Gate 1**: thesis, claim registry, top sources, failing eval dimensions, script diff since last revision.
- **Gate 2**: asset spreadsheet, generated chart previews, B-roll candidate reel, checklist for manual product/screen captures.
- **Gate 3**: low-res preview with segment notes, loudness stats, chapter draft, title/description/thumbnail package.

That gives you PR-style review without turning editorial approvals into a full internal tool project. The underlying approval primitive is the same one Temporal documents with signals, but implemented more cheaply with n8n waits and webhook callbacks. citeturn4search1turn3search14

### Build order across four weekly phases

**Phase one** should create the **run manifest and state model**. Add a single `run_id` spanning research, script, assets, VO, render, thumbnail, publish package, and analytics readback. Store state in Postgres, artifacts in object storage, and make every worker idempotent. This is the phase that prevents future maintenance debt. citeturn4search3turn19search1

**Phase two** should automate **research → sourced brief → script draft → rubric eval**. Use Exa for search/deep grounding, keep claim-level source objects, and fail closed if the model cannot supply grounded evidence. Add Trends as a secondary signal only if you get official alpha access; do not build the pipeline around it. citeturn7search5turn7search13turn7search23

**Phase three** should automate **voice, mastering, thumbnails, asset packages, and render orchestration**. Keep Remotion as the long-form renderer, use Playwright only for deterministic browser recordings, and add thumbnail QA that downsamples to 320×180 before Gate 3. ElevenLabs timestamps help align on-screen highlights to speech without manual timing. citeturn28search10turn34search0turn34search1turn37search8

**Phase four** should automate **publish package assembly, distribution, and analytics readback**. Upload the video, thumbnail, description, captions, and synthetic-media flag via API; then use Studio for anything the API still does not cover well. Pipe weekly analytics back into your topic scorer and script evaluator, especially retention and traffic-source metrics. citeturn12search1turn12search2turn13search6turn15search0turn15search5turn19search0

## Research, assets, voice, publish, and analytics guidance

For the **weekly evidence brief**, the best current low-cost pattern is **Exa for retrieval + your own verifier**. Exa’s new Deep outputs now support structured outputs with field-level grounding, which is exactly the kind of behavior you want for an evidence-first channel. Cost per run is low enough that even a “heavy” weekly brief is usually measured in cents, not dollars. A representative run with 20 search requests, 5 deep requests, and 50 content pulls is roughly a **sub-$0.30** event at posted rates. citeturn7search5turn7search13turn7search1

For **trends and outlier hunting**, the dependable automation layer is still the official YouTube/Google surfaces, not creator-growth SaaS. Google’s official Trends API exists but is still alpha. Social Blade has an official business API, but it is fundamentally built around public stats and rankings, not publisher-grade evidence assembly. My practical recommendation is to keep tools like 1of10/ViewStats as **manual optional inputs at Gate 1**, not as the machine room for the weekly run. citeturn7search23turn7search3turn8search2turn8search5

For **motion graphics**, stay with **Remotion**. You already use it, it fits code-generated data-driven composition, and its Lambda renderer gives you a credible cloud burst option if your machine becomes the bottleneck. Motion Canvas is attractive for deeply custom vector explainer segments, but it is not the safer weekly unattended production substrate today. Lottie is best treated as a component format for reusable micro-animations, not as the whole compositor. citeturn28search10turn28search4turn28search1turn29search1turn29search6turn28search3turn28search12

For **B-roll**, the low-friction answer is **Pexels first, Pixabay second, Storyblocks only if you later need indemnification and premium breadth**. Pexels and Pixabay are both genuinely usable for commercial YouTube, but Storyblocks is safer when you want contractual licensing confidence and partner/API support. Artgrid’s licensing is strong for commercial video, but it is not the obvious API-first choice for this automation problem. citeturn30search1turn30search9turn30search20turn30search2turn30search13turn30search0turn30search18turn31search1turn31search5

For **thumbnail generation**, I would not start with Canva. Canva’s Connect APIs are real and capable, but the product is still optimized around integration workflows that are heavier than you need right now. For a solo channel, the best starting split is **Bannerbear if you want a clean API-native templating path**, or **Figma export if you already design thumbnails there and volume stays low**. Either way, add automated legibility QA before you ever call the YouTube thumbnail endpoint. citeturn32search3turn32search11turn32search1turn33search1turn33search6turn33search17

For **automated screen capture**, Playwright is viable for product demos, browser UIs, chart walkthroughs, and reproducible web interactions. It can record videos, take full-page screenshots, and even create chapter-marked recordings via the CLI/MCP tooling. I would use it for “showing a tool” or “recording a workflow,” but not as a replacement for human-recorded polished desktop demos where cursor choreography and OS-native interaction quality matter. citeturn34search0turn34search1turn34search7turn34search9

For **voice**, continue with **ElevenLabs** unless your retention data tells you the synthetic read is actively hurting the channel. At the posted TTS API rate of **$0.10 per 1,000 characters**, a 50-minute monthly VO load is inexpensive, pronunciation dictionaries exist, and timestamp APIs are already available. The operational hazards are straightforward: plan-based concurrency caps and model-specific pronunciation behavior. citeturn35search1turn37search8turn38search0turn37search17

For **post-processing**, your instinct is right: normalize to YouTube-friendly loudness with a deterministic FFmpeg chain, match levels at section boundaries, and keep de-essing lightweight. The underlying technical point is not a platform decision but a brand one: your channel sells rigor, so weak VO finishing will be felt as weak thinking. That part should stay fully deterministic and scriptable.

For **publishing**, use the API where it is strong and Studio where it is still necessary. The good news is that the upload economics improved materially: `videos.insert` now uses its own upload quota bucket and is no longer the old “burn 1,600 units per upload” folklore. The API also now supports the **synthetic-media disclosure flag** via `status.containsSyntheticMedia`. The bad news is that Studio still matters because the public Data API docs do not expose everything creators want, and the official help pages for title/thumbnail A/B testing live in Studio rather than the API. citeturn12search1turn12search2turn14search3turn14search2turn13search10turn11search15

For **analytics readback**, the official YouTube Analytics API gives you enough to build a real feedback loop. You can programmatically pull traffic-source breakout, reach metrics, audience-retention metrics through `elapsedVideoTimeRatio`, and end-screen/card metrics across the Analytics/Reporting surfaces. What you do **not** cleanly get from the current targeted-query docs is a first-class “returning viewers” metric in the surfaces reviewed here, so do not design your closed loop around a metric you have not verified for your channel/report type. citeturn15search0turn15search2turn15search5turn16search1turn16search0turn18view0turn18view2

## Cost scenarios against the $100–300 budget

### Lean scenario

This is the version I would build first:

- n8n self-host infra: **~$15–25/month estimated**
- Exa: **$0–10/month** at your volume because the free tier is generous and paid usage is cheap. citeturn7search5turn7search13
- ElevenLabs VO: **~$5–10/month** for your current monthly spoken volume at posted TTS pricing. citeturn35search1
- Remotion Lambda/cloud burst: **usually low single digits** at one long-form + shorts weekly, and often effectively zero if you render locally most weeks. citeturn28search4turn28search1
- Pexels/Pixabay B-roll: **$0**. citeturn30search1turn30search2
- beehiiv Scale for audience growth and automations: **$43/month**, but note the post-creation API limitation. citeturn20search6turn21search1

That lands around **$70–100/month at one video/week** and roughly **$80–120/month at two videos/week**, because most of your cost increase is variable research/voice/render usage, not fixed software. The trade-off is that beehiiv does **not** currently give you the cleanest automation path for fully programmatic newsletter drafting unless you move into Enterprise-only API surfaces. citeturn20search6turn21search1turn26search0

### Fuller automation scenario

This is the “closer to no-touch” version:

- n8n self-host infra: **~$15–25/month estimated**
- Exa paid usage: **$10–20/month** at heavier weekly briefs. citeturn7search5turn7search13
- ElevenLabs: **$10–20/month** as VO volume grows. citeturn35search1
- Bannerbear: **$49/month**. citeturn32search3
- Kit instead of beehiiv for programmatic broadcast drafting/sending: **pricing needs live verification** from the current official calculator before purchase, but this is the platform directionally better aligned to your automation goal. citeturn25search6turn24search8turn24search1

This scenario should still plausibly sit inside **$120–220/month at one video/week** and **$150–260/month at two videos/week**, but the exact number depends mainly on your email platform choice and whether you add any premium stock subscription later. The good news is that it still clears your $300 ceiling without needing Storyblocks, Temporal Cloud, or any enterprise-only orchestration product.

## What not to automate

Do **not** automate your **thesis and rigor pass** away. Your brand premise is “evidence-first, human-authored,” and no retrieval stack currently removes the need for a human to decide whether the argument is actually yours and whether each strong claim is supported enough to survive publish risk. Exa’s grounding helps a lot, but grounded retrieval is still not the same thing as editorial judgment. citeturn7search13turn7search5

Do **not** treat synthetic-media disclosure as an afterthought. YouTube is adding automatic AI-detection signals and may apply labels even if creators do not disclose realistic AI use, which means your safest posture is explicit, reviewable disclosure logic rather than hoping the system will sort it out later. citeturn11search15turn12search2

Do **not** fully automate post-upload polish if the API surface does not expose the control you need. The current public docs support uploads, thumbnails, comments, captions, and metadata, but the “last mile” creator surfaces remain uneven. In practice, successful lean operators keep a Studio checklist for the features the API still does not cleanly cover rather than fighting the platform. citeturn12search1turn13search6turn13search9turn14search3turn14search2

Do **not** over-automate thumbnails before you have a measured QA loop. Figma rate-limit complaints and the general brittleness of automated export pipelines are not fatal at your scale, but they are enough to justify a deterministic check at 320×180 and a final human glance. citeturn32search1turn32search9turn32search17

Do **not** assume API upload, social scheduling, or bulk automation is “free” from platform friction. The clearest documented YouTube friction is the audit requirement for new unverified API projects, and LinkedIn is exactly the kind of platform where you stay on the rails by using official products or official scheduler partners instead of gray-area automation. citeturn13search10turn20search1turn20search9

## Top automation risks and the guardrail for each

The biggest risk is **citation drift**: an LLM summarizes a source correctly at draft time, but the final edit no longer matches the evidence. The guardrail is a **claim registry** stored per run: each publish-critical sentence gets a source URL, timestamp or quote excerpt, and a machine-readable status of `verified / weak / remove`. Gate 1 should display only the unresolved claims, not the whole script. citeturn7search13turn19search1

The next risk is **synthetic-voice trust decay**. Even high-quality TTS can trigger audience fatigue if cadence, emphasis, or finance/proper-name pronunciation feels off. The guardrail is to keep a reusable pronunciation dictionary, run automated mastering, and periodically compare intro retention against a human-read baseline rather than assuming the voice layer is “solved.” citeturn38search0turn37search8turn35search1

Another risk is **unsupported platform features creating hidden manual work**. If you promise yourself “fully automated publishing” but still need Studio for one or two important actions, the workflow silently grows a fourth gate. The guardrail is a deliberate **API-vs-Studio split** in the architecture and a fixed post-upload checklist instead of wishful thinking. citeturn12search1turn13search10turn14search3

A fourth risk is **workflow brittleness from too many vendor-specific surfaces**. beehiiv’s Enterprise-only create-post endpoint, Figma’s rate-limit complaints, and plan-based TTS concurrency limits are all examples of “works in demo, breaks in production.” The guardrail is to keep each stage behind a Python adapter with contract tests and a manual fallback mode. citeturn21search1turn26search0turn32search1turn32search9turn37search17

The fifth risk is **maintenance debt outrunning time saved**. Successful lean systems keep humans exactly where ambiguity is highest and keep automation deterministic elsewhere. In your case, that means preserving the three gates, not trying to eliminate them. The automation should reduce touches **between** the gates, not dilute the gates themselves. citeturn4search1turn27search25

## Open questions and limitations

A few items remain genuinely incomplete from primary sources captured in this pass. I did **not** verify an exact official **Kit price at the sub-5K subscriber level** from the current live calculator, even though the API capabilities are clear. The same is true for a clean primary-source pricing capture for **PlayHT**, and for public numerical rate-limit disclosure for **Cartesia**. Those are procurement questions, not architecture blockers, but they should be checked before purchase. citeturn24search8turn24search1turn25search6turn35search0turn35search3

I also did **not** find current official public YouTube API documentation exposing first-class endpoints for **end screens/cards authoring, Shorts related-video linking, or Test & Compare management**. On the evidence reviewed, the right assumption is that those remain partly or wholly Studio-side until proven otherwise. citeturn14search2turn14search3turn13search13turn13search0

The practical conclusion is simple: if you want the fastest path to a robust no-drama system, build **n8n + Python + Postgres + object storage** first, keep the three gates, and make every expensive or long-running step asynchronous. That gets you the highest automation yield per hour of build effort while protecting the two things your channel cannot afford to lose: **evidence quality** and **a human-authored point of view**.