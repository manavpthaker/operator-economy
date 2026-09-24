# N4B full capture review: EP007

Status: **technical review complete; owner continuity listen pending**

Episode: EP007

Captured: 2026-09-01

Configuration: `n3-two-stage-acted-guide-v2` — Google `gemini-2.5-pro-tts` voice `Algieba` under the candidate-C4 register, transferred to Original C `scMbPZwQjr40V1MzL3Nj` via `eleven_multilingual_sts_v2`.

## Capture

| | |
|---|---|
| Narration blocks | 26 |
| Capture chunks | 24 |
| Provider calls | 48 (24 Google, 24 ElevenLabs) |
| Failures or retries | **none** — all 24 chunks succeeded first pass |
| Master duration | 1075.2s = **17.9 minutes** |
| Format | 48 kHz / 16-bit / mono PCM |

Chunking respected the N3 rule: grouped on Step 1 narration-block boundaries, never splitting a block unless it alone exceeded the ceiling, with the F2 short-tail rule merging the final fragment.

## Technical results

| Measure | Result | Assessment |
|---|---|---|
| Guide→transfer envelope correlation | min `+0.854`, mean `+0.893`, max `+0.941` | **Pass.** Zero chunks below 0.85. Performance preservation held across the full episode, matching calibration |
| Dynamic range CV | 0.911 | **Pass.** Expressive, consistent with the accepted calibration set |
| Mean pause / variation | 0.54s / 0.55 | **Pass.** Room is contrastive rather than uniform |
| Peak | −0.33 dBFS | **Carried finding F3.** Hot, as in calibration. Delivery-stage headroom conversion still required |
| Chunk RMS spread | **4.9 dB** across 24 chunks | **FINDING N4B-1** |
| Master duration | 17.9 min vs declared 19.3–22.8 | **FINDING N4B-2** |

## FINDING N4B-1 — level drift compounds across a full episode

Chunk loudness ranges from −22.0 dBFS (c24) to −17.1 dBFS (c19), a **4.9 dB spread**.

Calibration could not have predicted this. The largest calibration mode ran four chunks and drifted 1.1 to 2.1 dB. At 24 chunks the drift compounds, because each chunk is an independent stochastic generation with no loudness reference to its neighbours.

**Disposition: fix in the narration edit, not by recapture.** Per-chunk gain normalisation to a common target is standard post work and changes no words. The raw provider outputs remain immutable per the N3 format contract, and the normalisation is recorded as a single conversion at N5/N6.

**Carried to N3 as a protocol amendment for the next episode:** the chunking rule should record a loudness target so chunks are normalised on acquisition rather than repaired downstream.

## FINDING N4B-2 — delivery is faster than the editorial estimate

The editorial lock declared 19.3 to 22.8 minutes based on 140 to 165 words per minute. Actual delivery is **178 wpm**, giving 17.9 minutes.

This is a defect in the **estimate**, not in the capture or the words. The lock's wpm assumption was inherited from generic narration guidance rather than from the measured behaviour of this configuration, which the N4A calibration had already shown running at 142 to 166 wpm depending on passage.

**Disposition: correct the estimate, not the audio.** No lexical change. The editorial lock's expected-duration range is annotated rather than rewritten, since the locked words are unchanged and the hash must hold.

**Carried forward:** future episode duration estimates should use the measured configuration rate rather than a generic band.

## N4B gate conditions

| Condition | Result |
|---|---|
| N4A current for the selected method | **pass** — configuration v2, passed 2026-09-01 |
| Full capture separately authorized | **pass** — owner instruction to run N4B |
| Approved N3 settings used | **pass** — Algieba + candidate-C4 + Original C, byte-identical style across all 24 chunks |
| Every script section has usable coverage | **pass** — all 26 narration blocks captured |
| Raw files immutable, registered, hashed | **pass** — `take-register.json`, mode 0600 |
| Provider jobs traceable | **pass** — per-chunk text, style and output hashes recorded |
| Interim ASR remains diagnostic | **pass** — none run; not used as a transcript |
| Complete capture passes a continuity listen | **PENDING OWNER** |
| No unresolved authorization or continuity problem | pending the listen |

**N4B gate: pending the owner continuity listen.** Technical review passes with two dispositioned findings.

## What the owner is listening for

1. **Continuity across the 24 joins** — the level drift is measurable at 4.9 dB and is the thing most likely to be audible. It is fixable in the edit; the question is whether anything else moves with it.
2. Any sentence that is unperformable or misleading, which would be a **change request back to Step 1**, not a Step 2 repair.
