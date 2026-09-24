# Synthetic guide lexical and technical QA — candidate B

Status: `technical_and_offline_lexical_pass_owner_audition_pending`

Candidate: `candidate-B` / `gemini-guide-02`

Original provider WAV: `outputs/raw/google/P01-W0030-W0110/candidate-B.wav`

Raw file SHA-256: `04448e9fdd50c8de67912b454e8d396f5822eaa881daf18128b825260623c915`

Optional listening derivative SHA-256: `none`

Active authorization SHA-256: `cece219b19d4f1c84c1ba3ab2a426334548af79181e0c587bd32714543c3974d`

Consumption record SHA-256: `3c4f9354dec64af0637911e89242784ca4e9a8d63053d315db100abd27ffa35b`

Run receipt SHA-256: `2898d5f26f6523de6691782e668ab45951f4710751b78414ca8caedeb9fe0a1f`

Offline ASR diagnostic: `evidence/G1R2-OFFLINE-ASR-DIAGNOSTIC.20260826T045358Z.json`

Offline ASR diagnostic SHA-256: `8331aae1c422c72f87b71e637f1685a661c841a0560c92bbf40b0b1eeb8b5e77`

Finalized at: `2026-08-26T04:59:42Z`

## Hard gates

| Check | Result | Evidence |
| --- | --- | --- |
| Exact canonical `W[30,110)` | pass for private owner audition | Two credential-free offline Whisper decoding modes, beam and greedy, each match all 80 locked tokens after normalization: `80/80`, `0` edits, WER `0%`. Human exact-word confirmation remains authoritative before any selection or transfer. |
| No additions, omissions, substitutions, or repetitions | pass for private owner audition | Both normalized offline decodes contain zero additions, omissions, substitutions, or repetitions. |
| `2022` retained | pass in both offline decodes | Whisper rendered the locked `2022` lexeme. |
| `2022` pronounced as twenty twenty-two | pending owner audition | Rendering `2022` cannot distinguish “twenty twenty-two” from another spoken-number form. |
| No vocalized acting direction | pass in both offline decodes | No direction or tag leakage detected. |
| Actual source is mono PCM WAV at 24 kHz | pass | Strict full decode: RIFF/WAV, `pcm_s16le`, 16-bit, 24,000 Hz, mono, 822,983 frames, 1,646,010 bytes. |
| Duration is 20 to 50 seconds | pass | `34.290958333333336` seconds. |
| Guide run, active G1R2, and consumption receipts cross-hash | pass | Exact authorization, consumption, run, request-set, request-body, output path, output SHA-256, byte count, duration, and response accounting reconcile. |
| RIFF/container truncation or trailing container bytes | pass | Declared RIFF length, data-chunk length, file length, frame count, and full decode agree exactly. |
| Baked or perceptual clipping | pending owner audition | Container geometry and strict decode cannot clear clipping already present in the synthesized signal. |
| No watery consonants, brittle sibilance, or obvious synthetic artifact | pending owner audition | These are perceptual gates and were not inferred from media geometry or ASR. |
| Original provider WAV strict-decodes completely and remains unchanged | pass | The exact raw hash above is the only candidate-B identity reviewed; no derivative was created. |
| Optional listening derivative is marked transfer-ineligible | not applicable | No derivative exists. |
| Understandable without music or visuals | pending owner audition | No owner perceptual verdict exists. |

Hard-gate result: `technical_and_offline_lexical_pass_perceptual_owner_review_pending`

Eligible for owner performance review: `true`

## Evidence boundary

The `80/80` lexical result comes from two modes of the same local Whisper engine and model, not
independent models or a human exact-word determination. The bound diagnostic records the exact
binary and model hashes, sandboxed beam and greedy flags, normalization rule, transcripts, and
zero-edit comparison. It clears candidate B for private owner audition only. The owner must still
review exact words and pronunciation and judge performance, intelligibility, artifacts, energy,
inflection, and the across-the-table relationship. Nonessential loudness, pause, DC-offset, and
effective-bit measurements are intentionally omitted; the owner audition decides perceptual quality
and performance.

The unchanged original provider WAV—not a derivative—is the audition source and the only possible
future selection identity.

This form does not select a guide, authorize disclosure to ElevenLabs, or set creative approval.
