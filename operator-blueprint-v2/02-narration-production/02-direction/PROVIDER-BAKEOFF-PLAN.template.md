# Provider Bakeoff Plan

Template version: proposed Step 2 v0.3.

This plan binds a fair comparison. It is not provider-call, upload, clone, long-form, N4B, or Step 3
authority.

## Frozen authority

- Fixture or episode ID:
- Locked script path/SHA-256:
- Ordered `W` count/SHA-256:
- N2 direction path/SHA-256:
- Performance envelope path/SHA-256:
- Eleven adapter path/SHA-256:
- Hume adapter path/SHA-256:
- Original-sample provenance path/SHA-256:
- Hume clone ID/creation receipt path/SHA-256:
- Authorization register path/SHA-256:

## Exact passages

| Passage | Function | Start/end `W` | Passage SHA-256 | Character count | Names/numbers/negations/qualifications |
| --- | --- | --- | --- | ---: | --- |
| P1 | Cold open, attention, identity, promise | | | | |
| P2 | Build, validation, verdict, CTA | | | | |

## Candidate equality

### ElevenLabs

- Provider/model/voice:
- Exact shared tags/text/settings hash:
- E1 seed/generation identity:
- E2 seed/generation identity:
- E1/E2 differ only by seed/generation: yes / no

### Hume

- Provider/model/clone:
- Exact shared text/description/settings hash:
- Request mode: one `POST /v0/tts` JSON call per passage
- Exact `num_generations`: `2`
- H1 generation identity:
- H2 generation identity:
- Within each passage, H1/H2 are the two outputs from the same request/description: yes / no

## Planned outputs

| Provider | Passage | Generation | Exact payload hash | Preferred PCM/WAV format | Only fallback | Authorization ID |
| --- | --- | --- | --- | --- | --- | --- |
| ElevenLabs | P1 | E1 | | | `mp3_44100_192` | AUTH-03 |
| ElevenLabs | P1 | E2 | | | `mp3_44100_192` | AUTH-03 |
| ElevenLabs | P2 | E1 | | | `mp3_44100_192` | AUTH-03 |
| ElevenLabs | P2 | E2 | | | `mp3_44100_192` | AUTH-03 |
| Hume | P1 | H1 | | | `mp3_44100_192` | AUTH-04 |
| Hume | P1 | H2 | | | `mp3_44100_192` | AUTH-04 |
| Hume | P2 | H1 | | | `mp3_44100_192` | AUTH-04 |
| Hume | P2 | H2 | | | `mp3_44100_192` | AUTH-04 |

## Fair-processing and blind-review plan

- Immutable raw before processing:
- Actual codec inspection:
- One identical lossless gain-only review-copy policy:
- No provider-specific cleanup/mastering:
- Blind curator:
- Random code-map custody path/SHA-256:
- Owner scorer:
- Independent scorer:
- Unblind trigger: all eight hard-gate reviews and both signed scorecards frozen

## Stop conditions

- Spoken tag or changed `W`:
- Damaged name, number, negation, or qualification:
- Watery consonant, brittle sibilance, synthetic artifact, truncation, or corruption:
- Cannot understand without music/visuals:
- Unresolved rights/tier/provenance:
- Candidate equality failure:
- Authorization mismatch or overrun:

## Approval

- Eight planned clips are equal and bounded: yes / no
- Every exact scope has its own authorization: yes / no
- No long-form or full capture included: yes / no
- Plan decision: approved_for_authorization_review / revise / blocked
- Owner/signature/date:
