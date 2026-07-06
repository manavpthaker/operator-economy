# Research brief: "Businesses will pay you to answer their phones with AI"

Episode #2. Thesis: small businesses miss most of their phone calls, every missed call is revenue walking to a competitor, and AI voice agents have gotten good enough and cheap enough that a solo operator can sell "we answer your phones" as a service — $300–1,000/mo per client on infrastructure that costs a fraction of that.

## The demand wedge (confidence: MEDIUM — single vendor-adjacent study, hedge aloud)

- **Reported: only ~38% of calls to small businesses are answered by a live person; ~62% go to voicemail or nothing.** Source: a 2024 study by 411 Locals (85 businesses, 58 industries), widely recycled by voice-AI vendors. Treat as "one study found" / "reported" — the primary study is an SEO-agency artifact, not audited research.
- **Reported behavioral follow-ons (same vendor-content ecosystem, mark reported):** ~85% of callers who hit voicemail don't call back; ~62% of unanswered callers call a competitor; ~80% of voicemail-reachers hang up without leaving a message.
- Concrete ROI math (illustrative, present as arithmetic not fact): a plumber missing 15 calls/week at $350 average job value is leaving six figures/year on the table; a $500/mo answering service against that is a rounding error. This is the pitch the low-end agencies actually run.
- Home services (plumbers, HVAC, electricians) miss calls because technicians are on job sites — the buyer knows they have the problem.

## Evidence — HIGH END (confidence: HIGH, primary/press sources)

- **ElevenLabs: $500M Series D at $11B valuation (Feb 2026, Sequoia); ~$500M ARR by April 2026, up from ~$350M end of 2025.** Reported talks for a secondary at ~$22B within five months of the raise. Sources: TechCrunch (Feb 4, 2026), ElevenLabs blog, Sacra estimate, Tech Funding News (the $22B is talks, not closed — hedge).
- **Vapi (voice-agent infrastructure): $500M valuation May 2026 after Amazon Ring chose its platform over 40 rivals.** Source: TechCrunch (May 12, 2026).
- **Retell AI: launched 2024, reported ~$50M ARR in 2025, powers 50M+ AI phone calls/month.** Sources: Retell/press coverage — vendor-reported, mark "reported."
- Market sizing (directional only, estimates vary wildly by definition): AI voice agents ~$2.5–3.5B in 2025–26, forecast CAGRs of 30–40% through early 2030s (Grand View Research, Market.us). Use ONE number with an explicit "analyst estimate" marker.
- The structural read: the platforms (ElevenLabs, Vapi, Retell, Bland) are raising at software multiples to be infrastructure — they need someone to install this into the local dentist's office. That someone is the episode's audience.

## Evidence — LOW END (confidence: MIXED — vendor/agency content, mark reported/unverified)

- **Reported agency economics: white-label voice-AI resellers price $297–997/mo per client against $99–299/mo platform fees — 50–70% margins.** Source: Trillet pricing guide (a vendor selling to these agencies) — UNVERIFIED, present as "the numbers the platforms themselves advertise to would-be agencies."
- Typical pricing bands (multiple vendor sources converge): setup/build fees $500–2,000 (simple receptionist) up to $2K–25K (complex builds); monthly retainers $300–700 all-in for most SMBs; voice-specific agency retainers reported at $800–3,500/mo. Confidence: MEDIUM (convergent but all from vendor content).
- Per-minute cost floor: Bland ~$0.09–0.14/min (raised prices Dec 2025), Retell/Vapi in similar territory, ElevenLabs agent minutes on top of TTS at $0.05–0.10/1K chars. A receptionist handling a few hundred calls/mo costs tens of dollars in usage, not hundreds.
- Honest gap to name aloud: unlike EP001 there is no credible public "$40K/mo solo voice agency" case study — the solo evidence is thinner and mostly platform marketing. Say so; it's also why the space is less crowded.

## Manav's POV material (Gate 1 will inject)

- Hospitality operator years (Coqui Coqui: 4 properties, 50+ staff): the phone-as-revenue-channel problem lived first-hand — front desk misses calls during checkout rush, that's a lost booking.
- Currently runs VO/voice experiments in this channel's own stack (ElevenLabs in production for this very video) — can speak to what the voice actually sounds like in 2026 and where it still breaks.
- Has sold tech into ops-heavy SMBs (Subziwalla, Lovingly's 1,500 florists — florists are a canonical missed-call business: Valentine's Day call volume).

## Tool stack (for stack section; affiliate terms verified July 2026)

**ElevenLabs Agents** (voice + agent platform; **affiliate: 22% of payments for first 12 months** on Starter→Scale plans, 11% Business, via PartnerStack — verified at elevenlabs.io/affiliates) · **Retell AI** or **Vapi** (call orchestration, ~$0.07–0.15/min) · **Bland** (outbound-heavy alternative) · **Twilio** (phone numbers, ~$1/mo + usage) · **Make/n8n** (booking + CRM handoff) · **Cal.com/Calendly** (appointment write-back). Solo-operator tooling: <$150/mo before per-minute usage.

## Playbook skeleton (for playbook section)

1. Pick ONE local vertical where missed calls = lost jobs (home services, dental, salons, florists) — ideally one you've operated in or sold into.
2. Build a demo agent for a real business in that vertical (Retell/Vapi + Twilio number) — the demo IS the sales call: ring their own missed-call line, let the agent book a fake appointment.
3. Price as receptionist replacement math, not software: setup fee ($500–2K) + flat monthly ($300–700). Never price per-minute to the client.
4. Deliver: agent answers → qualifies → books into their calendar → texts the owner a summary. Maintenance (prompt updates, new FAQ, integrations) is the retainer.
5. First 3 clients from your own network/vertical; their before/after missed-call numbers become the case studies.

## Failure modes / honesty notes (for economics section)

- The voice is good but not solved: proper nouns, accents, interruptions, and angry callers still break agents. Client churn comes from the first embarrassing call — set expectations that the agent handles the 80%, escalates the 20%.
- Same service-business physics as EP001: revenue stops when you stop; retainers mitigate, don't eliminate. Client concentration risk at 3–5 clients.
- Platform risk is HIGHER here than in automation: you're reselling someone's per-minute margin. Bland already raised prices once (Dec 2025). Platforms are also moving up-market into direct SMB sales — the agency layer could get squeezed (Retell sells "AI receptionist" direct).
- Regulatory surface: outbound AI calling is TCPA territory — the safe solo play is INBOUND answering only. Say this explicitly.
- No verified solo case study exists at the $40K/mo level of the automation-agency stories — the honest low-end number is likely $1.5–5K/mo in year one from 3–8 local clients.

## Sources

TechCrunch (ElevenLabs Series D Feb 2026; Vapi valuation May 2026), ElevenLabs blog + affiliates page (commission terms), Sacra (ARR estimates), Tech Funding News ($22B talks — unconfirmed), Retell AI press/blog (ARR + call volume, vendor-reported), Grand View Research / Market.us (market sizing, analyst estimates), 411 Locals via getaira.io/skipcalls (62% missed-call study — vendor-recycled), Trillet/Aircall/Retell pricing guides (agency economics, vendor content), deep-research report 2 (topic surface table).
