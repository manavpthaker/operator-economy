# Editorial handoff checklist: EP009

Template version: proposed Step 2 v0.2.

Gate N1 accepts a complete Step 1 v1.5 package and creates the immutable spoken-text identity used throughout Step 2.

## Episode and receipt identity

- Episode number and slug: EP009 `direct-booking-recovery`
- Candidate or promotion ID: `candidate-2026-09-03-direct-booking-recovery`
- Step 1 authority version: `operator-blueprint-v2-step1-v1.5`
- Editorial-lock path/revision/SHA-256: `operator-blueprint-v2/episodes/EP009-direct-booking-recovery/01-editorial/editorial-lock.md` / LOCKED 2026-09-03 / `246330740a5c7447e455f967b7a8597a3a8352fa417ff1f241e730c448da2d20`
- Narration-handoff path/status/SHA-256: `operator-blueprint-v2/episodes/EP009-direct-booking-recovery/01-editorial/narration-handoff.md` / issued / `a4472ffdf32803b72887490cb2ed92b4d02b302fd538af967e56166fbb34d6e1`
- Step 2 package-manifest path/SHA-256: `operator-blueprint-v2/episodes/EP009-direct-booking-recovery/02-narration-production/package-manifest.json` / `96ac61415ff0fa8108316c73bb1d6cff007c29edb95657673e16d9ff4ac6b5ce`
- Package received by/date: narration producer (Step 2 process), 2026-09-03
- Checklist reviewer/date: narration producer (Step 2 process), 2026-09-03

## Required Step 1 artifact verification

| Artifact | Required | Path | Expected SHA-256 | Observed SHA-256 | Match/current |
| --- | --- | --- | --- | --- | --- |
| Editorial lock | yes | `operator-blueprint-v2/episodes/EP009-direct-booking-recovery/01-editorial/editorial-lock.md` | `n/a (lock and handoff carry no self-hash)` | `246330740a5c7447e455f967b7a8597a3a8352fa417ff1f241e730c448da2d20` | yes |
| Narration handoff | yes | `operator-blueprint-v2/episodes/EP009-direct-booking-recovery/01-editorial/narration-handoff.md` | `n/a (lock and handoff carry no self-hash)` | `a4472ffdf32803b72887490cb2ed92b4d02b302fd538af967e56166fbb34d6e1` | yes |
| Locked script | yes | `operator-blueprint-v2/episodes/EP009-direct-booking-recovery/01-editorial/script.md` | `cbe74c03e021998cafc1d11a8b0dff50e6dfaa4d0109fc223c958a6ecc37993c` | `cbe74c03e021998cafc1d11a8b0dff50e6dfaa4d0109fc223c958a6ecc37993c` | yes |
| Episode Investment Thesis | yes | `operator-blueprint-v2/episodes/EP009-direct-booking-recovery/01-editorial/episode-investment-thesis.md` | `f5210eec2bd8edfcaec25f612a82cf6420ff43f4859731d844a91c53f76c6c93` | `f5210eec2bd8edfcaec25f612a82cf6420ff43f4859731d844a91c53f76c6c93` | yes |
| Episode beat sheet | yes | `operator-blueprint-v2/episodes/EP009-direct-booking-recovery/01-editorial/episode-beat-sheet.md` | `ae3e89c3b4c366000a574504b71f629ca0e7a4fa3de3773a746a37cc8b7f2578` | `ae3e89c3b4c366000a574504b71f629ca0e7a4fa3de3773a746a37cc8b7f2578` | yes |
| Editorial-voice conformity report | yes | `operator-blueprint-v2/episodes/EP009-direct-booking-recovery/01-editorial/editorial-voice-conformity.md` | `4248683d86c886bcbd676aee1dfe9b28ebbf114db998adedaa7440ace9903652` | `4248683d86c886bcbd676aee1dfe9b28ebbf114db998adedaa7440ace9903652` | yes |
| Operator Canvas | yes | `operator-blueprint-v2/episodes/EP009-direct-booking-recovery/01-editorial/operator-canvas.md` | `c3b00ed94fa4587b82a0dc8fb6d30044cd7768be984217f3bef4d1aaff27ec35` | `c3b00ed94fa4587b82a0dc8fb6d30044cd7768be984217f3bef4d1aaff27ec35` | yes |
| Claims map | yes | `operator-blueprint-v2/episodes/EP009-direct-booking-recovery/01-editorial/claims-map.md` | `37f9f4727cde1b7e52fd75745117685336a28ec5f6756cf5f1be3dea1bb68798` | `37f9f4727cde1b7e52fd75745117685336a28ec5f6756cf5f1be3dea1bb68798` | yes |
| Narrative spine | yes | `operator-blueprint-v2/episodes/EP009-direct-booking-recovery/01-editorial/narrative-spine.md` | `b1383559042fbabef276e52a1af1e24d389501de5280ca9d6332d23924819548` | `b1383559042fbabef276e52a1af1e24d389501de5280ca9d6332d23924819548` | yes |
| Episode outline | yes | `operator-blueprint-v2/episodes/EP009-direct-booking-recovery/01-editorial/episode-outline.md` | `718adc2987437b838cc6379ed60d160509e086b04414ea2a7a2fbc9d331c5800` | `718adc2987437b838cc6379ed60d160509e086b04414ea2a7a2fbc9d331c5800` | yes |
| Voice and comedy map | yes | `operator-blueprint-v2/episodes/EP009-direct-booking-recovery/01-editorial/voice-and-comedy-map.md` | `ad6988aad90322523ed15b365d20acdf4a8aebd3ecdc6db50e9114ef37e6517c` | `ad6988aad90322523ed15b365d20acdf4a8aebd3ecdc6db50e9114ef37e6517c` | yes |
| Performance read-through | yes | `operator-blueprint-v2/episodes/EP009-direct-booking-recovery/01-editorial/performance-readthrough.txt` | `b6017bf833eaeb48f9e92b86b607c883ef5271eba060aed9ef38d3c92c85b856` | `b6017bf833eaeb48f9e92b86b607c883ef5271eba060aed9ef38d3c92c85b856` | yes |

## Reviewed live authority identities

| Authority | Reviewed path | Expected SHA-256 from Step 1 | Observed SHA-256 | Match |
| --- | --- | --- | --- | --- |
| Content OS voice | `voice.md` | `3b9b9400f9f2ac6aeaff09d62cca2092c322a969447bbc85d161b56a42d0d20e` | `3b9b9400f9f2ac6aeaff09d62cca2092c322a969447bbc85d161b56a42d0d20e` | yes |
| V2 Script Beat Research | `operator-blueprint-v2/01-editorial/SCRIPT-BEAT-RESEARCH.md` | `e67c480e6aae4f3638ab388bd17b67b2aa768d3ae4e9f59f985f2eea17f4f9fe` | `e67c480e6aae4f3638ab388bd17b67b2aa768d3ae4e9f59f985f2eea17f4f9fe` | yes |
| V2 Voice Architecture | `operator-blueprint-v2/01-editorial/VOICE-ARCHITECTURE.md` | `ce9b0af23221ff5d9266460a279c0a6fd6f53874e39c2f5831ceeb22a3569474` | `ce9b0af23221ff5d9266460a279c0a6fd6f53874e39c2f5831ceeb22a3569474` | yes |
| Studio speech profile | `studio/config/speech-profile.md` | `75913da0bc5d5b360c88f18c70b60d8d4af14128184e8164872edd56f71ceddc` | `75913da0bc5d5b360c88f18c70b60d8d4af14128184e8164872edd56f71ceddc` | yes |

## Deterministic spoken-text identity

- Specification: `SPOKEN-TEXT-IDENTITY-SPEC.md`
- Specification version: `oe-spoken-text-v1`
- Extractor implementation/version: `oe_narration extract` (runtime at `operator-blueprint-v2/02-narration-production/runtime`); reproduces EP007's frozen identity byte for byte
- Locked script SHA-256: `cbe74c03e021998cafc1d11a8b0dff50e6dfaa4d0109fc223c958a6ecc37993c`
- `canonical-w.txt` path/SHA-256: `operator-blueprint-v2/episodes/EP009-direct-booking-recovery/01-editorial/canonical-w.txt` / `7b9d18bfb2820a124f96308568cbb5509eef792a38150a5e78c3643ced9e191e`
- `spoken-identity.json` path/SHA-256: `operator-blueprint-v2/episodes/EP009-direct-booking-recovery/01-editorial/spoken-identity.json` / `85475673b31cd8335aa56ba79eb2e36e59f605ee5fdd23f814e4f2b73b790f67`
- First and last `W` IDs: `W000000` and `W003398`
- Deterministic whitespace-token count: 3399
- Step 1 recorded count and ordered-token SHA-256: 3399 / `7b9d18bfb2820a124f96308568cbb5509eef792a38150a5e78c3643ced9e191e`
- Count and ordered-token SHA-256 match: yes
- Two clean runs are byte-identical: yes
- Unresolved extraction ambiguity: none

## Handoff content review

- Short public category title present: yes
- Exact short spoken company name present: yes
- One-sentence plain definition present: yes
- Company-level BUILD verdict present: yes
- Opportunity and operator acts/turns identified: yes
- Silent identity break or other intentional pause identified: yes (S01 silent identity sting)
- Qualification register present: yes (claims map and handoff caveats)
- Pronunciation register present: yes
- Numbers, acronyms, proper nouns, negations, and qualifiers flagged: yes
- Performance cautions present: yes
- Explicitly non-verbatim passage: none

## Rights, origin, and readiness

- Proposed narrator origin: synthetic (two-stage acted guide onto the owner's saved voice identity)
- Narrator authorization requirement identified: yes (owner authorization of 2026-09-03, see `n4b-authorization.md`)
- Synthetic voice or cloning involved: yes (Original C, the owner's own saved identity)
- Rights/consent evidence required before N3: owner's own voice, rights basis unchanged from EP007
- Synthetic-media disclosure expected downstream: yes
- Unresolved factual blocker: no
- Unresolved legal, permission, or source-integrity blocker: no
- Unresolved owner decision: no

## Fixture and production boundary

- Real promoted and numbered episode: yes
- Fixture identifier, when applicable: not applicable
- Fixture-only authorization permits N1: not applicable
- Content OS public-fact clearance: not applicable at this gate (release-time authority)
- Visual, production, publishing, or release authority: no

## Gate N1 decision

- Package hashes all match: yes
- Spoken-text identity reproducible: yes
- Handoff status is `ready`: yes (issued)
- Runtime `verify-package`: passed
- N1 gate result: passed
- Workflow outcome: in_progress
- Findings and required action: none
- Narration producer/signature/date: narration producer (Step 2 process), 2026-09-03
