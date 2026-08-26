# Synthetic guide lexical and technical QA — candidate A

Status: `technical_pass_lexical_not_established_ineligible`

Candidate: `candidate-A` / `gemini-guide-01`

Original provider WAV: `outputs/raw/google/P01-W0030-W0110/candidate-A.wav`

Raw file SHA-256: `354194ccaddd606d6c45069a03f739e435977678e9f42d26591435b1cefabc9d`

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
| Exact canonical `W[30,110)` | **not established** | Two credential-free offline Whisper decoding modes, beam and greedy, independently produced the same possible substitution at slice-relative token index `29` (absolute `W[59]`): required `the`, ASR `this`, in `You open the search dashboard`. ASR is diagnostic, so this does not prove the provider WAV changed the word; it does require fail-closed handling. |
| No additions, omissions, substitutions, or repetitions | **not established** | One normalized substitution in each decode; `1/80` edits, WER `1.25%`. |
| `2022` retained | pass in both offline decodes | Whisper rendered the locked `2022` lexeme. |
| `2022` pronounced as twenty twenty-two | pending owner audition | Rendering `2022` cannot distinguish “twenty twenty-two” from another spoken-number form. |
| No vocalized acting direction | pass in both offline decodes | No direction or tag leakage detected. |
| Actual source is mono PCM WAV at 24 kHz | pass | Strict full decode: RIFF/WAV, `pcm_s16le`, 16-bit, 24,000 Hz, mono, 822,023 frames, 1,644,090 bytes. |
| Duration is 20 to 50 seconds | pass | `34.25095833333334` seconds. |
| Guide run, active G1R2, and consumption receipts cross-hash | pass | Exact authorization, consumption, run, request-set, request-body, output path, output SHA-256, byte count, duration, and response accounting reconcile. |
| RIFF/container truncation or trailing container bytes | pass | Declared RIFF length, data-chunk length, file length, frame count, and full decode agree exactly. |
| Baked or perceptual clipping | pending owner audition | Container geometry and strict decode cannot clear clipping already present in the synthesized signal. |
| No watery consonants, brittle sibilance, or obvious synthetic artifact | pending owner audition | These are perceptual gates and were not inferred from media geometry or ASR. |
| Original provider WAV strict-decodes completely and remains unchanged | pass | The exact raw hash above is the only candidate-A identity reviewed; no derivative was created. |
| Optional listening derivative is marked transfer-ineligible | not applicable | No derivative exists. |
| Understandable without music or visuals | pending owner audition | No owner perceptual verdict exists. |

Hard-gate result: `fail_closed_lexical_not_established`

Eligible for owner performance review: `false`

## Evidence boundary

The lexical signal comes from two modes of the same local Whisper engine and model, not independent
models or a human exact-word determination. The bound diagnostic records the exact binary and model
hashes, sandboxed beam and greedy flags, normalization rule, transcripts, and token diff. Because
both modes returned the same `the`/`this` difference, candidate A is ineligible unless a later
separately recorded human exact-word review resolves the original provider WAV. Nonessential
loudness, pause, DC-offset, and effective-bit measurements are intentionally omitted; the owner
audition decides perceptual quality and performance.

This record does not authorize a new decode, provider call, regeneration, selection, upload,
transfer, or production action.

This form does not select a guide, authorize disclosure to ElevenLabs, or set creative approval.
