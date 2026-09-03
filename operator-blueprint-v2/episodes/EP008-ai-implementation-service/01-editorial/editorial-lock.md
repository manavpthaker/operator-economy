# Editorial lock: EP008 — a helpdesk setup practice

Status: **LOCKED**

Template version: approved `operator-blueprint-v2-step1-v1.5`

Gate: **E6 — script lock**

Episode: EP008

Candidate ID: `candidate-2026-09-03-ai-implementation-service`

Lock decision date: 2026-09-03

Locked by: Manav Thaker

These are the exact words Step 2 is authorized to perform. Every hash below was recomputed from disk after the owner's approvals were recorded on 2026-09-03. Owner decisions of record: package approval ("Approved let's keep going"), direct voice-match answer "Yes, both", and the rulings recorded in the gate results below.

## Pre-lock conditions carried from Step 0

| Condition | Status | Effect on lock |
|---|---|---|
| Open CLM-013 (onboarding threshold) at source | **satisfied** by Step 0 amendment 01 (`00-intake/02-research/candidate-2026-09-03-ai-implementation-service-amendment-01.md`, `0f034d7ee72ae4934aba43b49bf828ce27461d0f8b535807e0a286e16e636fb3`) | the script states the vendor's own $3M line (C012) |
| Confirm CLM-007 (per-resolution price) on the vendor's page | **partially satisfied** by amendment 01: mechanism verified, figure not rendered | no Gorgias per-resolution dollar amount appears in the script (C006) |
| Run the vendor's setup wizard on a sandbox and record what it leaves undone | **open** | the script does not depend on the result. S18 says "I have not run that wizard against a real store, so I'm not going to tell you it's inadequate." **If the owner runs the sandbox test before recording, that sentence must be revised (claims map H006), which creates a new script revision, read-through, E5V and lock.** If the test is not run before lock, the line stands as true. |

## Locked inputs

| Artifact | Path | Revision | SHA-256 | Approval owner | Approval date |
|---|---|---|---|---|---|
| Step 0 handoff | `01-editorial/handoff.md` | E1 accepted | `630331914ed4548c5e4cc0272df8b2889b6fa579d095bf17e6a13b7ce848837c` | Manav Thaker | 2026-09-03 |
| Editorial contract | `01-editorial/editorial-contract.md` | E2 approved | `286da3f901317a9a3b52d79ff389d192f37ed59470d39ff6dda4d3d0a7784de5` | Manav Thaker | 2026-09-03 |
| Operator Canvas | `01-editorial/operator-canvas.md` | E3 approved | `d5caa22c0114759247ca8084f3e2cf677f81f66fad5844d7fbc86c8fb963b209` | Manav Thaker | 2026-09-03 |
| Episode Investment Thesis | `01-editorial/episode-investment-thesis.md` | E3I, BUILD, approved | `19ac4015597220d9567cb182b5852125bebc20642cdbbc27d668aef868b662a3` | Manav Thaker | 2026-09-03 |
| Narrative spine | `01-editorial/narrative-spine.md` | E4 approved | `e57bb6cbd6ef2f93c19375be6c66fdc6eceb517d923e34164eef13e67a6478ee` | Manav Thaker | 2026-09-03 |
| Episode beat sheet | `01-editorial/episode-beat-sheet.md` | E4B approved | `18a1fc026fc551bbaa986affa4096d212dcd319fe003d8941547eb198250f542` | Manav Thaker | 2026-09-03 |
| Episode outline | `01-editorial/episode-outline.md` | E4B approved | `795c21a590433642f7dd1cd245493e12151f1ec9ab789c7bda5833920dba1b39` | Manav Thaker | 2026-09-03 |
| Voice and comedy map | `01-editorial/voice-and-comedy-map.md` | drafted | `d3a8d39661824fe882c7631d1e4c48699d307f9b1b5229b23a0b641bd3d2d00b` | Manav Thaker | 2026-09-03 |
| Claims map | `01-editorial/claims-map.md` | r2 | `a5d0693ed70115d2a5973c15ee1fb6d751c0d1ab9ed74c680631cfcf9a564e24` | Manav Thaker | 2026-09-03 |
| Content OS voice authority | `../content-os/voice.md` | live reviewed identity | `3b9b9400f9f2ac6aeaff09d62cca2092c322a969447bbc85d161b56a42d0d20e` | reviewed | 2026-09-03 |
| Content OS facts authority | `../content-os/facts.md` | live reviewed identity | `d1b67dd431b36dcf201b8c42053c663ef47c6c34e5bde272daedb9eabcc9a201` | reviewed | 2026-09-03 |
| V2 script-beat research | `operator-blueprint-v2/01-editorial/SCRIPT-BEAT-RESEARCH.md` | reviewed identity | `e67c480e6aae4f3638ab388bd17b67b2aa768d3ae4e9f59f985f2eea17f4f9fe` | reviewed | 2026-09-03 |
| V2 voice architecture | `operator-blueprint-v2/01-editorial/VOICE-ARCHITECTURE.md` | reviewed identity | `ce9b0af23221ff5d9266460a279c0a6fd6f53874e39c2f5831ceeb22a3569474` | reviewed | 2026-09-03 |
| Manav speech profile | `studio/config/speech-profile.md` | live reviewed identity | `75913da0bc5d5b360c88f18c70b60d8d4af14128184e8164872edd56f71ceddc` | reviewed | 2026-09-03 |
| Editorial voice conformity | `01-editorial/editorial-voice-conformity.md` | owner cold read passed | `1e7f4d84872207a225bf97b92a359c6f6332fb59f214de299d683efd50950ccc` | Manav Thaker | 2026-09-03 |
| Performance read-through and owner cold-read record | `01-editorial/performance-readthrough.txt` | derived from v0.2 | `6678f18ec0e54e03795c2ef00d01ca569e1b214082cc27d99a1aef835c479af6` | Manav Thaker | 2026-09-03 |
| Review disposition | `01-editorial/review-disposition.md` | complete | `c82f046ea0d5f50aac81c868dd67b2848de45b8bef498d945939dd9bd55dcd14` | Manav Thaker | 2026-09-03 |
| Final script | `01-editorial/script.md` | v0.2 | `ca1dd86903b700c6fe41f9a22ae9e5862294808d9538f9a5a01f3a7d53a88373` | Manav Thaker | 2026-09-03 |
| Reviewed v0.1 script (superseded) | not retained as a file | v0.1 | `803b6f13d6ce0ed8b42b95e6dc28f45836d9b4a3f3e0f9a1a0b47e6948c86511` | superseded | 2026-09-03 |
| Step 0 promotion record | `00-intake/04-queue/candidate-2026-09-03-ai-implementation-service-promotion.md` | promoted | `42441ea691702d6950d3cb7bff36f32ab2de66104ec5ea8a3ec1e577ba87319e` | Manav Thaker | 2026-09-03 |

## Script identity

Locked script revision: v0.2

Spoken word count: **3,400**

Performance read-through word count: **3,400**

Counts and lexical sequence match: pass (token-for-token, narration blocks only)

Expected duration range: **20.6 to 24.3 minutes** at 140 to 165 words per minute

Working promise: The help desk gets paid every time its AI resolves a ticket, but the work that makes it resolve anything is left with the store, and this episode shows that job, what it is worth to the store, what it costs one person to do, and the one thing that could make it disappear.

Short public category title: Helpdesk AI setup

Short spoken company name: a helpdesk setup practice

One-sentence plain definition: It makes the AI that came with a small store's help desk actually answer customers, and decides which questions it never should.

Internal operating description: Canvas §9

Show thesis: one experienced person, a small reachable share of a large costly problem, modeled and tested, no income promise

Opportunity thesis: outcome pricing put the vendor's revenue on resolutions and left the setup with the store; the setup is sold above $3M and unowned below

Operator thesis: judgment about tickets and policy, learned on a queue, is the advantage; the settings screen is not

Entry-wedge thesis: a paid audit and one fixed-fee implementation, measured on the vendor's meter, producing the audit method and the never list

Final company-level verdict: BUILD

Business-of-one promise: two implementations a month, one person, every decision recorded

AI role and retained human judgment: the vendor's agent answers; a general model drafts; the operator decides safe, conditional, never, every money rule, handover, sign-off, two weeks of reading, and the no-buy call

Modeled livelihood condition and required customer count: $120,000 needs about 33 a year at $4,000 (above the 24 cap) or about $5,500 at the cap; the base case does not clear

Reachable-share assumption: two a month against millions of merchants; reach untested

Operator-market selection rule: start with stores you can already reach; qualify with the vendor's own question and the ticket band

Industry example status: approved recommendation (Shopify DTC brands on Gorgias or Zendesk; no product category named)

Entry wedge: a paid audit credited against one implementation

Mature company: a steady run of brands on both help desks; repeat work on change; a retainer only if proven

Expansion conditions remain explicit: pass

Complete company appears before entry wedge: pass (S11 before S14)

Opportunity/build narrative balance: pass

Opportunity-pitch percentage and word count: 55.2 percent, 1,876 words (S00 through S11)

Operator-blueprint percentage and word count: 44.8 percent, 1,524 words (S12 through S23)

Approved exception if opportunity share is outside 52 to 58 percent: not required

Opportunity-scale argument: pass

At least two observed operating layers: pass (the vendor; certified agencies including a specialist shop)

Qualified and unsuitable buyer rules: pass

Company understandable without example industries: pass

No example-industry denominator or invented conversion rate: pass

Opportunity-to-build transition: pass ("That's the business. The question is whether you're the person to build it.")

Mature-company-to-wedge transition: pass ("Drafting the handbook got cheap. Deciding what goes in it didn't." → "What do you sell first?")

Exact pre-sting operator or business payoff tease:

> Between the day that store bought the AI and the day it works, there's a job. I think one person can sell it, at a fixed price, to stores the vendor won't set up by hand.

Mechanism, proof, and complete thesis withheld until earned: pass

Exact fixed brand string verified: pass

> This is The Operator Economy, where we show you how to use AI to build, own, and operate a sustainable business of one.

Exact final like-and-subscribe sentence:

> If you want the next business taken apart this carefully, including the parts a vendor could delete, like this one and subscribe.

Adjacent narrated-sequence seam test: pass (E5V seam table; silent identity and brand reset recorded as the only exception)

Repeated discourse-marker scene openings: zero

Evidence-delivery layers complete: pass

First 30-day and 90-day construction path: pass

Client-level no-build, refuse, narrow, defer, or stop decisions remain distinct from company-level BUILD: pass ("keep the wizard and save the money")

Claims used: C001, C002, C003, C004, C006, C007, C008, C009, C010, C011, C012, C013, C014, C016, C017, C018, C019, C020, C021, C022, C023, H001, H002, H003, H004

Modeled passages requiring audible qualification: S17 (the disclosure at its top, present)

Hosted-long-form routing used: documentary evidence rigor plus observed Manav lexical surface

Live Content OS hosted-long-form routing conflict: the reviewed `content-os/voice.md` §1 names an "Operator Economy hosted long-form" register for YouTube VO hosted by Manav; the V2 authority files still describe the historical conflict as unresolved. The owner accepted the reviewed voice.md as the routing authority for this lock on 2026-09-03, as EP007's lock did.

Authorized Content OS resolution path and SHA-256, or `none`: `content-os/voice.md` §1 at `3b9b9400f9f2ac6aeaff09d62cca2092c322a969447bbc85d161b56a42d0d20e`, accepted by the owner 2026-09-03

Positive hosted-voice evidence locations:

- Opening: S00 "There is no human. There'll be one at nine."; S03 "I'd have switched it on."
- Opportunity case: S10 "Both of those are the vendor, and both are true. Going live and working are two different days"; "It does not list a person."
- Operator build: S12 "I'll be straight about where I sit... What I have not done is sell this to a store as a service."; "You bring the queue. The vendor has the tools."; S16 "If they give you a person, you're not my buyer, and I'll say so."
- Economics: S17 "Say you want a hundred and twenty. It doesn't clear."; "Watch that number on the first one you do."
- Ending: S20 "Same tool. Same bill. Somebody wrote the handbook."; S22 "If the answer is nothing, you've spent ten dollars and saved yourself a business."

## Gate results

- Step 0 package current: pass
- Editorial contract approved: **approved 2026-09-03**
- Operator Canvas locked: **approved 2026-09-03**
- Gate E3I Episode Investment Thesis approved: **approved 2026-09-03**
- Narrative approved: **approved 2026-09-03**
- Episode beat sheet approved: **approved 2026-09-03**
- Outline approved: **approved 2026-09-03**
- Voice and comedy map approved: **approved 2026-09-03**
- Claims map complete: pass (showrunner)
- Claim-change audit against previous accepted script: pass (D001 through D006)
- Unsupported essential claims have approved Step 0 amendments: not applicable (none required; amendment 01 was recorded by Step 0)
- Unsupported nonessential claims removed: pass (CL-01)
- Content OS facts routed: pass (H001 through H006 checked against the `## Do not state` list)
- Mechanical voice hygiene: pass
- First-listen clarity: no lane-specific blocker
- Lexical performability: no lane-specific blocker
- Positive hosted-voice evidence complete across opening, opportunity case, operator build, economics, and ending: **pass** (reviewer evidence; owner yes 2026-09-03)
- E5V editorial-voice conformity: **pass** (reviewer: clear for owner voice test; owner cold read passed 2026-09-03)
- Owner cold read of exact final script hash: **passed 2026-09-03**
- Owner answered "Does this sound like me talking, not merely like a good Operator Economy script?": **yes** (2026-09-03, answer of record "Yes, both")
- Owner cold-read revision or spontaneous rewrite unresolved: none
- Opening orientation: pass
- Pre-sting operator or business payoff: pass
- Show identity: pass
- Reporting spine: pass
- Business context: pass
- Operator-advisor base: pass
- Business-of-one clarity: pass
- Positive Manav lexical identity: **approved 2026-09-03**
- Conviction: pass
- Evidence integrity: pass
- Evidence delivery across VO, source receipts, and show notes: pass
- Operator-market fit and example-industry boundary: pass
- Narrative seams: pass
- Repeated discourse-marker scene openings: zero
- Humor temperature: pass
- Cadence: pass
- Ending payoff: pass
- Opening payoff delivered in the ending: pass
- Final like-and-subscribe sentence present after BUILD and first action: pass
- Final audience ask is one natural sentence with no stacked ask or new promise: pass
- Non-imitation: pass
- Adversarial editorial review: pass (38 findings, all dispositioned)
- Every review finding dispositioned: pass
- Entry wedge and mature company preserved: pass
- Public title, spoken name, plain definition, and internal description match the Investment Thesis: pass
- Proposed category label remains evidence-safe: pass
- Opportunity pitch occupies 52 to 58 percent: pass (55.2)
- Market scale separates adjacent spend, observed category operation, proposed offer demand, and bottom-up owner requirements: pass
- Complete company is established before the first offer: pass
- Final company-level verdict is BUILD: pass
- First 30-day and 90-day plan begins construction under explicit proof and stop conditions: pass
- Client-level no-build decisions remain subordinate and valid: pass
- Unresolved placeholders: zero
- Live Content OS hosted-long-form routing conflict resolved by authorized authority change: the owner accepted the reviewed voice.md §1 as the routing authority for this lock on 2026-09-03, as for EP007
- Unresolved blockers: none blocking. The wizard sandbox test remains open; the owner locked without it on 2026-09-03 and the S18 line stands as true

## Decision

Decision: **LOCKED**

Owner rationale: statement of record, 2026-09-03: "Approved let's keep going"; direct voice-match answer: "Yes, both"

Step 2 Narration Production authorized: **yes**

No automated score, pattern count, reviewer consensus, clean hygiene result, or lexical-performability result may change `no` to `yes`. Only complete positive evidence across the five episode functions, an owner `yes` to the direct voice-match question, a passed complete cold read of the exact revised hash, and the owner's acceptance of the routing authority can authorize Step 2.

## Change control

This lock authorizes Step 2 to perform only the exact spoken words in the locked script hash. The pre-sting payoff tease and final like-and-subscribe sentence are Step 1 editorial decisions. Any addition, removal, reordering, or rewriting of spoken words invalidates the lock and requires a new script revision and approval.

A material change to the company definition, opportunity thesis, operator thesis, entry-wedge thesis, or BUILD verdict returns to Gate E3I. A change to the public category title, spoken company name, or one-sentence definition requires a new beat-sheet and script revision.

The spoken-text identity is recorded below; the narration handoff is `narration-handoff.md`.

Invalidated by: not applicable

Invalidation date: not applicable

Replacement lock: not applicable

## Spoken-text identity (`oe-spoken-text-v1`)

Step 2 consumes this identity, not the prose.

| Field | Value |
|---|---|
| Specification | `oe-spoken-text-v1` |
| Tokenization | unicode-whitespace split, case and punctuation preserved |
| Serialization | one token per line, UTF-8, single terminal LF |
| Ordered `W` token count | **3400** |
| Canonical `W` SHA-256 | `ea3743bfcc6e881a96902556959d141f5a75a2288ecad713ccc6fa7ba787ca63` |
| Byte authority | `canonical-w.txt` |
| Companion record | `spoken-identity.json` / `8be1e30286b0018e8fd3d8b6359c6c478f79e9c700ace7c2c8299438ac17ba25` |

Extracted with `oe-narration extract` from the locked `script.md`; the extractor reproduces EP007's frozen identity byte for byte, verified 2026-09-03.

## Boundary for Step 2

Step 2 may add non-lexical performance direction. Step 2 may **not** change words, invent a payoff tease, or improvise an audience ask. Any added, removed, reordered, or rewritten spoken word creates a new script revision and hash, and invalidates this lock. A pronunciation spelling or performance tag may live in the narration layer only if the spoken lexical sequence remains identical. If Step 2 finds an unperformable or misleading sentence, it issues a change request; Step 1 revises and relocks before narration resumes.
