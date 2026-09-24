# Step 1 v1.1 Editorial Voice Regression Results

Status: required fixture tests complete; owner authentic-voice review pending; v1.1 not locked

Test date: 2026-08-21

Production episode created: no

Narration generated or authorized: no

## Plain-English result

The correction found a real weakness in Step 1 v1.0.

Both previously accepted scripts were clear, useful, evidence-safe, and technically speakable. Both still failed the new voice gate because too much of the language sounded like a polished report. The old performance review could not distinguish “easy to read aloud” from “plausibly sounds like Manav.”

New v0.3 revisions moved the conversational language into the actual scripts. They use direct guidance, ask-and-answer reasoning, wrong-frame replacement, short landings, objections, and natural pivots without changing the approved evidence or business model.

A separate negative test stuffed recognizable Manav phrases into a meaningless sample. It failed. This proves the standard does not reward imitation by keyword count.

## Test matrix

| Fixture | Input behavior | Expected | Observed | Result |
| --- | --- | --- | --- | --- |
| GEO v0.2 | Evidence-safe, speakable, report register dominates | E5V fail | OE delivery and Manav fingerprint failed | correct rejection |
| GEO v0.3 | Same claims and model, editorial voice authored into exact words | E5V recovery | Five dimensions passed in fixture review; claims audit passed | correct recovery |
| Workflow reliability v0.2 | Strong opening, formal process body, one em dash | E5V fail | OE delivery, fingerprint, and speakability failed | correct rejection |
| Workflow reliability v0.3 | Same claims and model, direct advisor relationship across episode | E5V recovery | Five dimensions passed in fixture review; claims audit passed | correct recovery |
| Voice caricature | Dense catchphrases and observed speech moves without mechanism | Non-caricature fail | Mechanical checks passed; human editorial dimensions failed | correct rejection |

## Deterministic checks

### GEO v0.3

- Script SHA-256: `affba46d60b4860b5f6c4f04d109104e57d11cc8e7598431e84894bfdcbbb617`
- Read-through SHA-256: `da10923cd70500831bd43aec9bb9fb145a817d482f820e78cc5018f2dfb38841`
- Narration-only word count: 1,127
- Script extraction and read-through: exact match
- Em dashes, semicolons, and prohibited report vocabulary: zero
- Claims retest: pass

### Workflow reliability v0.3

- Script SHA-256: `ee51b82a1441882c6adeba0047ca34ef925acb6005fa389d25d7c226b1c598ab`
- Read-through SHA-256: `18df9a451c0ef4419feeef46a945bb1069665178f5059a84033cd7d4eae450c8`
- Narration-only word count: 1,096
- Script extraction and read-through: exact match
- Em dashes, semicolons, and prohibited report vocabulary: zero
- Claims retest: pass

## What changed in the system

- `content-os/voice.md` is explicitly classified as Step 1 editorial language and message delivery.
- `studio/config/speech-profile.md` is now a Step 1 observed spoken-language authority.
- Both source hashes must be recorded in the script package and editorial lock.
- Gate E5V separately tests OE message delivery, Manav speech fingerprint, speakability, evidence voice, and non-caricature.
- The editorial-voice reviewer is separate from the read-aloud performance reviewer.
- Word-changing conversational work must happen before script lock.
- Step 2 receives the completed editorial voice and separately controls narrator identity and audio performance.
- Step 1 artifacts no longer contain self-hash fields, the script no longer contains downstream review hashes, and the narration handoff is produced after the editorial lock. Hash identity can now be calculated without circular dependencies.

## What remains human

The tests support a v1.1 pass recommendation, but they cannot decide whether Manav personally hears himself in the revised words. The owner should read representative sections or the complete narration-only fixtures before approving v1.1.

No actual narrator audio was created, so these tests do not approve the Studio voice ID, ElevenLabs settings, or Step 2 performance. Those remain Step 2 calibration work.

## Decision

System behavior: **pass**

Proposed Step 1 v1.1: **ready for owner review, not locked**

Step 1 v1.0: **last owner-approved version until a new explicit lock**
