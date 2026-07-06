# Topic queue (v3 — thesis-led format, July 2026)

Every episode is a thesis: **"this is the kind of business you can build"** — with evidence spanning the low end (solo operator, best-case case study) and high end (venture-scale proof of market). Sources: 3 deep-research reports (`../research/reports/`), scored per `scoring.md`. To produce: `cd ../studio && python originate.py new "<thesis>" --research <brief>`.

## Production queue

| # | Episode thesis | Low-end evidence | High-end evidence | Tools/stack | Score | Status |
|---|---|---|---|---|---|---|
| 1 | **You can sell AI implementation to businesses that are drowning in it** (~90%-margin consulting/productized service) | Boutique AI agencies, productized consultancies | Late Checkout, Scale AI (adjacent) | Claude/GPT, n8n, Notion | 90 | **PILOT #1** — strongest POV (Manav lived it), thesis-native |
| 2 | Businesses will pay you to answer their phones with AI (voice-agent agency) | Solo voice-AI agencies for local biz | ElevenLabs, Retell, Bland | ElevenLabs (22% recurring affiliate), Twilio | 88 | queued — ties to avatar/VO experiments |
| 3 | The boring-automation agency: SMBs pay real money for workflows | Solo n8n/Make agencies | Zapier, n8n | n8n, Make, Airtable | 86 | queued — concept-led, decay-proof |
| 4 | One person can run a media company now (this channel is the demo) | This channel's own stack + receipts | Starter Story (HubSpot exit), MagnatesMedia | Whisper, Claude, ElevenLabs, Remotion | 84 | queued — meta episode, publish ~#4-6 once receipts exist |
| 5 | AI coding tools went $0→$4B in 18 months — and the one-person version is real | Solo devtool micro-SaaS founders | Cursor/Anysphere, GitHub Copilot | Claude Code, Cursor | 83 | queued — the Cursor story as evidence inside a buildable thesis |
| 6 | **Your expertise is the product: the small-cohort business (15 people × $2K) is how independents monetize what they know** | Reframe & Ready (Joanie Johnson — cleared numbers, ON EPISODE) | Maven ($25M a16z), Reforge, Section | Circle/Kajabi/Kit (affiliates) or owned stack (Next.js, Stripe/Square, Resend, Supabase) | 80 | **EP 004** — absorbs old expertise-is-a-product topic. Structure: C→B (career-is-the-curriculum hook → small-cohort economics w/ Joanie's real numbers), anti-platform wave as the "why now" industry section. First Phase 2 interview. POV note: Manav built the R&R platform — episode story is Joanie's, POV is builder-behind-the-infrastructure |
| 7 | "Buy a boring business and bolt on AI" is the quiet wealth play | Solo acquisition operators | Codie Sanchez portfolio | acquisition + retrofit stack | 78 | queued |
| 8 | Meetings are a business: AI note-takers and who pays for them | Indie meeting-tool builders | Granola, Otter, Fireflies | AssemblyAI, Whisper | 76 | queued |
| 9 | You can sell AI avatars/localization to companies that will never film | Freelance avatar/localization services | Synthesia, HeyGen | HeyGen, ElevenLabs | 75 | queued |
| 10 | Customer support agents: the first AI employees businesses actually buy | Agencies deploying support bots | Intercom Fin, Sierra, Gorgias | Intercom, Chatwoot + LLM | 74 | queued |
| 11 | Recruiting is broken enough to be a business opportunity | Mike Giunta (independent recruiting agency — guest outreach sent 7/6, awaiting reply; economics TBD) | Ashby, HireVue, Metaview | Grapevines-adjacent stack | 72 | queued — Grapevines synergy. Guest seed: Mike as the buildable low-end blueprint; backup seats: Eric (Poozle founder, warm 4/10 call) for platform-side high-end, Josh Baez (TA consulting) for hiring-side insider. Re-score once Mike's agency numbers land |
| 12 | The AI gold rush pays the shovel-sellers (where the money actually flows) | Small infra/tooling plays | NVIDIA, CoreWeave, Scale AI | — | 70 | queued — evidence-heavy episode |
| 13 | Vibe-coding is real: non-devs are shipping paid products | Solo Lovable/Bolt builders w/ revenue | Replit, Lovable, Bolt | Lovable, Replit, Bolt | 70 | queued |
| 14 | Hotels and restaurants are 10 years behind — that's the opportunity | BusyLobby story + small hotel-tech operators | Cloudbeds, Toast ecosystem | voice AI, PMS integrations | 68 | queued — unique POV moat |
| 15 | The newsletter is still the best small media business | Solo B2B newsletters at $50–200 sponsor CPM | beehiiv, Morning Brew | beehiiv/Kit (50% affiliates) | 65 | queued |
| 16 | Legal/compliance AI: high-trust niches pay the most | Spellbook-adjacent solo services | Harvey, Ironclad | Claude API | 63 | queued |
| 17 | Healthcare documentation: painkiller economics, real moats | Small clinical-scribe services | Abridge, Nabla, Suki | AssemblyAI, Deepgram | 62 | queued — weakest POV fit |
| 18 | How Anthropic/OpenAI actually make money (evidence standalone) | — | Anthropic, OpenAI, Microsoft | — | 60 | bench — pure-breakdown episode, use sparingly |
| 19 | The content-farm economy YouTube killed — and what survived | demonetized farm post-mortems | NexLev/Noah Morris | — | 58 | bench |

## Sequencing logic

Open with #1 (max POV credibility — the "I've done this" episode sets the channel's authority) → #2/#3 (most buildable theses, affiliate-ready) → **EP 004 = #6 (small-cohort business, Joanie Johnson guest)** — opens the Phase 2 interview pipeline early, evidence already cleared. Meta episode (#4 row) shifts to ~#5-6 once the channel has receipts. Review at upload 12: which thesis archetype wins (service business / product business / market-story), rebalance.

## Scoring shorthand

Score = demand ÷ competition, weighted by evidence availability (need BOTH a low-end and high-end example), affiliate potential, POV strength, derivation richness. Rubric in `scoring.md`. Re-score monthly against retention + capture analytics.
