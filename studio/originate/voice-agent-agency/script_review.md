# Script review: The Phone Call Businesses Never Answer

**GATE 1 — your POV pass.** Edit `script.json` directly:
- Replace every `[POV: ...]` token with your own experience/take (required — this is the monetization moat).
**POV insertions required: 2**
- Rewrite anything that doesn't sound like you.
- Check every number against the source. Delete claims you can't stand behind.

**Title options:** The Phone Call Businesses Never Answer | 62 Percent of Calls Go to Voicemail | Local Businesses Miss Most of Their Calls

## hook
- (1) One study found that only 38 percent of calls to small businesses get answered by a real person — the other 62 percent go to voicemail or nowhere. A solo operator selling AI phone agents to fix that can realistically bill $300 to $1,000 a month per client; the company selling the infrastructure underneath just raised money at an $11 billion valuation.
  - source: 411 Locals 2024 study (vendor-recycled) via getaira.io/skipcalls

## thesis
- (1) This is a service business: you install an AI receptionist for local businesses that live or die by the phone — plumbers, dentists, salons, florists. The technician is on a roof, the dentist is with a patient, the florist is buried on Valentine's Day. Nobody's answering, and the caller doesn't wait around.
- (2)  ⚠️ POV NEEDED Voice AI got good enough and cheap enough in the last two years that one person can build this end to end — no call center, no dev team. [POV: describe what it felt like running a hospitality front desk during checkout rush and watching bookings disappear because nobody could get to the phone]
- (3) Built lean, it's a laptop, a phone number, and three subscriptions under $150 a month. Built seriously, it's five to eight local clients on retainer, a documented before-and-after missed-call number for each one, and a repeatable sales demo that closes itself.

## evidence
- (1) Start with the low end, and be honest about it: there's no verified public case study of a solo voice-AI agency doing huge numbers, the way there is in some other AI-agency niches. The evidence here is thinner, and mostly comes from the platforms themselves marketing to would-be resellers.
  - source: Research brief note: no credible public solo case study at scale
- (2) What the platforms do advertise: white-label resellers charging clients $297 to $997 a month while paying $99 to $299 a month in platform fees — a 50 to 70 percent margin on paper. Setup fees run $500 to $2,000 for a simple receptionist build, more for complex ones.
  - source: Trillet pricing guide (vendor content, unverified)
- (3) The pitch writes itself with arithmetic, not adjectives: a plumber missing 15 calls a week at $350 a job is leaving six figures a year on the table. A $500-a-month answering service against that number is a rounding error, and that's the exact math low-end agencies run in the sales call.
  - source: Illustrative arithmetic from research brief, not audited
- (4) Now the high end, which is fully sourced. ElevenLabs closed a $500 million round in February 2026 at an $11 billion valuation, reportedly hitting around $500 million in annual revenue by April — up from $350 million just four months earlier.
  - source: TechCrunch, Feb 4 2026; Sacra estimate
- (5) Vapi, the infrastructure that routes these calls, hit a $500 million valuation in May 2026 after Amazon's Ring chose it over 40 competing platforms. Retell AI, launched only in 2024, reportedly powers more than 50 million AI phone calls a month.
  - source: TechCrunch, May 12 2026 (Vapi); Retell press/blog, vendor-reported
- (6) One analyst estimate puts the AI voice agent market at roughly $2.5 to $3.5 billion in 2025, growing 30 to 40 percent a year into the early 2030s. The read: these platforms are raising at software multiples to become infrastructure, and infrastructure needs someone to install it in the dentist's office down the street. That installer is this episode's audience.
  - source: Grand View Research / Market.us, analyst estimate

## stack
- (1) The voice itself comes from ElevenLabs — this channel actually runs ElevenLabs in production for the voiceover you're hearing right now, so this isn't theoretical. It sounds close to human on clean audio; it still stumbles on proper nouns and heavy accents.
  - source: ElevenLabs blog; direct production use (channel's own stack)
- (2) For call orchestration — the logic that answers, qualifies, and books — use Retell AI or Vapi, both running roughly 7 to 15 cents a minute. Bland is the alternative if you need outbound calling, though it raised per-minute prices in December 2025, a reminder that you don't control this cost line.
  - source: Research brief: per-minute pricing convergence across vendors
- (3) Twilio provides the phone number itself, about a dollar a month plus usage. Make or n8n handles the handoff into the client's calendar and CRM, and Cal.com or Calendly writes the actual appointment back so the business owner sees a booked slot, not just a transcript.
- (4) All in, before per-minute usage, the solo stack runs under 150 dollars a month. A receptionist handling a few hundred calls costs tens of dollars in usage — not hundreds — which is exactly the margin the retainer pricing is built on.
  - source: Research brief: solo-operator tooling cost estimate

## playbook
- (1)  ⚠️ POV NEEDED Week one: pick one local vertical where a missed call is a missed job — home services, dental, salons, or florists — ideally one you've worked in or sold into before. [POV: reference selling into ops-heavy SMBs like florists during Valentine's Day call surges]
- (2) Also in week one, build a working demo agent for a real business, not a hypothetical one. Ring their own current missed-call line, let your agent answer it, qualify the caller, and book a fake appointment. The demo is the sales call — you're not pitching a concept, you're showing them their own phone working correctly for the first time.
- (3) Price it as a receptionist replacement, never as software. A setup fee of $500 to $2,000, plus a flat monthly retainer of $300 to $700. Never quote per-minute pricing to the client — that's your cost structure, not theirs, and it makes the price feel unpredictable to someone who just wants their calls answered.
  - source: Research brief: convergent vendor pricing bands
- (4) Month one: land your first three clients from your own network inside that vertical. Their actual before-and-after missed-call numbers become the case study you use to get the next five — and inbound-only keeps you out of TCPA territory, which matters, because outbound AI calling is regulated and this isn't the place to test that boundary.
  - source: Research brief: TCPA / regulatory note on inbound vs outbound

## economics
- (1) We built a step-by-step version of exactly this — vertical selection, demo script, and pricing sheet — into a blueprint, free, linked below if you want the checklist instead of rebuilding it from a transcript.
- (2) Realistic year-one income for a solo operator is likely $1,500 to $5,000 a month from three to eight local clients — lower than the ceiling in some other AI-agency niches, mostly because the solo evidence here is thinner and the space is younger.
  - source: Research brief honesty note, estimate reasoning
- (3) The real failure mode isn't the pitch, it's the first embarrassing call — an angry customer, a mispronounced name, an accent the agent can't parse. The agent handles roughly 80 percent of calls cleanly; the other 20 percent needs to escalate to a human, and client churn happens exactly when that escalation doesn't exist.
  - source: Research brief: honesty note on voice agent limitations
- (4) Platform risk here is higher than in other AI-agency niches, because you're reselling someone else's per-minute margin, and Bland already raised prices once. Retell already sells an AI receptionist directly to small businesses — the same platforms you build on could squeeze the agency layer out entirely.
  - source: Research brief: platform risk note, Retell direct-sales mention
- (5) So the open question isn't whether small businesses will pay for this — the missed-call math already answers that. It's whether the agency layer between the platform and the plumber survives the next eighteen months, or whether ElevenLabs and Retell just sell it themselves.

## cta
- (1) The full blueprint — vertical picker, demo script, and pricing sheet — is linked below, free. Subscribe if you want the next one of these broken down the same way, with the same sourcing.

---
When done, continue with:
```
python originate.py <slug> --continue
```