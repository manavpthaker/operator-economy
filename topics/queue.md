# Topic queue (v3 — thesis-led format, July 2026)

Every episode is a thesis: **"this is the kind of business you can build"** — with evidence spanning the low end (solo operator, best-case case study) and high end (venture-scale proof of market). Sources: 3 deep-research reports (`../research/reports/`), scored per `scoring.md`. To produce: `cd ../studio && python originate.py new "<thesis>" --research <brief>`.

## Production queue

| # | Episode thesis | Low-end evidence | High-end evidence | Tools/stack | Score | Status |
|---|---|---|---|---|---|---|
| 1 | **You can sell AI implementation to businesses that are drowning in it** (~90%-margin consulting/productized service) | Boutique AI agencies, productized consultancies | Late Checkout, Scale AI (adjacent) | Claude/GPT, n8n, Notion | 90 | **PILOT #1** — strongest POV (Manav lived it), thesis-native |
| 2 | Businesses will pay you to answer their phones with AI (voice-agent agency) | Solo voice-AI agencies for local biz | ElevenLabs, Retell, Bland | ElevenLabs (22% recurring affiliate), Twilio | 88 | queued — ties to avatar/VO experiments |
| 3 | The boring-automation agency: SMBs pay real money for workflows | Solo n8n/Make agencies | Zapier, n8n | n8n, Make, Airtable | 86 | queued — concept-led, decay-proof |
| 4 | Content automation is the business: one research run → five surfaces (this channel is the working demo) | This channel's own pipeline + growth receipts (confidence-gated pipeline, evals, per-episode cost) | Starter Story (HubSpot exit), MagnatesMedia | Whisper, Claude, ElevenLabs, Remotion | 84 | queued — meta episode. HARD GATE: growth numbers must carry the thesis on screen (threshold TBD — set a subs/views bar the episode can say out loud). Angle sharpened 7/6: the confidence-gated pipeline is the star, not the tools |
| 5 | AI coding tools went $0→$4B in 18 months — and the one-person version is real | Solo devtool micro-SaaS founders | Cursor/Anysphere, GitHub Copilot | Claude Code, Cursor | 83 | queued — the Cursor story as evidence inside a buildable thesis |
| 6 | **Your expertise is the product: the small-cohort business (15 people × $2K) is how independents monetize what they know** | Reframe & Ready (Joanie Johnson — cleared numbers, ON EPISODE) | Maven ($25M a16z), Reforge, Section | Circle/Kajabi/Kit (affiliates) or owned stack (Next.js, Stripe/Square, Resend, Supabase) | 80 | **EP 004** — absorbs old expertise-is-a-product topic. Structure: C→B (career-is-the-curriculum hook → small-cohort economics w/ Joanie's real numbers), anti-platform wave as the "why now" industry section. First Phase 2 interview. POV note: Manav built the R&R platform — episode story is Joanie's, POV is builder-behind-the-infrastructure |
| 7 | "Buy a boring business and bolt on AI" is the quiet wealth play | Solo acquisition operators | Codie Sanchez portfolio | acquisition + retrofit stack | 78 | queued |
| 8 | Meetings are a business: AI note-takers and who pays for them | Indie meeting-tool builders | Granola, Otter, Fireflies | AssemblyAI, Whisper | 76 | queued |
| 9 | You can sell AI avatars/localization to companies that will never film | Freelance avatar/localization services | Synthesia, HeyGen | HeyGen, ElevenLabs | 75 | queued |
| 10 | Customer support agents: the first AI employees businesses actually buy | Agencies deploying support bots | Intercom Fin, Sierra, Gorgias | Intercom, Chatwoot + LLM | 74 | queued |
| 11 | Recruiting is broken enough to be a business opportunity | Mike Giunta (independent recruiting agency — guest outreach sent 7/6, awaiting reply; economics TBD) | Ashby, HireVue, Metaview | Grapevines-adjacent stack | 72 | queued — Grapevines synergy. Guest seed: Mike as the buildable low-end blueprint; backup seats: Eric (Poozle founder, warm 4/10 call) for platform-side high-end, Josh Baez (TA consulting) for hiring-side insider. Re-score once Mike's agency numbers land |
| 12 | **The solo design agency: AI collapsed the studio — one person can sell what used to take a team** | Designjoy (solo, ~$1M/yr self-reported) + BusyLobby (Manav's live pipeline: 1 callback from 6 outreach, first close in progress 7/7) | Superside, Canva ecosystem | Figma Make, Lovable, v0, Framer + Relume (both pay affiliates), Midjourney | 72 | queued — BusyLobby is the documented-in-real-time POV thread; full evidence trail already exists in the busylobby repo (tracking/autopilot-pipeline.csv, per-account email files scored vs outreach-rubric, PostHog demo analytics). First close in play: Tony Haddad, Tower Cottage (scored 9, TA 5.0/184, demo live 6/16). No revenue receipts yet — Designjoy carries sourced economics until then. The scout→score→demo-first→outreach→PostHog→call loop IS the blueprint section. Hotel war stories stay in the hotels episode |
| 13 | The AI gold rush pays the shovel-sellers (where the money actually flows) | Small infra/tooling plays | NVIDIA, CoreWeave, Scale AI | — | 70 | queued — evidence-heavy episode |
| 14 | Vibe-coding is real: non-devs are shipping paid products | Solo Lovable/Bolt builders w/ revenue | Replit, Lovable, Bolt | Lovable, Replit, Bolt | 70 | queued |
| 15 | Hotels and restaurants are 10 years behind — that's the opportunity | BusyLobby story + small hotel-tech operators | Cloudbeds, Toast ecosystem | voice AI, PMS integrations | 68 | queued — unique POV moat |
| 16 | The newsletter is still the best small media business | Solo B2B newsletters at $50–200 sponsor CPM | beehiiv, Morning Brew | beehiiv/Kit (50% affiliates) | 65 | queued |
| 17 | Legal/compliance AI: high-trust niches pay the most | Spellbook-adjacent solo services | Harvey, Ironclad | Claude API | 63 | queued |
| 18 | Healthcare documentation: painkiller economics, real moats | Small clinical-scribe services | Abridge, Nabla, Suki | AssemblyAI, Deepgram | 62 | queued — weakest POV fit |
| 19 | How Anthropic/OpenAI actually make money (evidence standalone) | — | Anthropic, OpenAI, Microsoft | — | 60 | bench — pure-breakdown episode, use sparingly |
| 20 | The content-farm economy YouTube killed — and what survived | demonetized farm post-mortems | NexLev/Noah Morris | — | 58 | bench |

## Sequencing logic

Open with #1 (max POV credibility — the "I've done this" episode sets the channel's authority) → #2/#3 (most buildable theses, affiliate-ready) → **EP 004 = #6 (small-cohort business, Joanie Johnson guest)** — opens the Phase 2 interview pipeline early, evidence already cleared. Meta episode (#4 row) shifts to ~#5-6 once the channel has receipts. Review at upload 12: which thesis archetype wins (service business / product business / market-story), rebalance.

## Scoring shorthand

Score = demand ÷ competition, weighted by evidence availability (need BOTH a low-end and high-end example), affiliate potential, POV strength, derivation richness. Rubric in `scoring.md`. Re-score monthly against retention + capture analytics.
