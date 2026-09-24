# N4B full capture review: EP009

Status: **technical review complete; owner continuity listen pending (N7)**

Episode: EP009

Captured: 2026-09-03

Configuration: `n3-two-stage-acted-guide-v2`, Google `gemini-2.5-pro-tts` voice `Algieba` under the candidate-C4 register, transferred to Original C `scMbPZwQjr40V1MzL3Nj` via `eleven_multilingual_sts_v2`. Frozen in `n3-configuration-freeze.md`; authorized in `n4b-authorization.md`.

## Capture

| | |
|---|---|
| Narration blocks | 24 (S01 silent, not captured) |
| Capture chunks | 22 |
| Provider calls | 46 Google, 28 ElevenLabs |
| Guide regenerations under the completeness contract | 19 |
| Recaptures | c22 (S23+S24): the episode's final word aligned at 0.10s, exactly half the median, so the chunk was recaptured rather than risk a clipped last word; superseded files kept as `.superseded-1.bak` |
| Raw transfer duration | 1221.5s = **20.4 minutes** |
| Format | guides LINEAR16 24 kHz mono; transfers PCM 48 kHz / 16-bit / mono, no lossy intermediate |

Chunking respected the N3 rule: grouped on Step 1 narration-block boundaries, never splitting a block unless it alone exceeded the ceiling, with the F2 short-tail merge.

## Finding N4B-3: a seeded transfer cannot be retried into silence

Chunk c05 (S06) transferred with a tail energy of 0.024 against the 0.02 threshold. The executor regenerated the transfer six times and received the identical result each time, because the Voice Changer call is seeded at N3 and is therefore deterministic. Six ElevenLabs calls were spent on nothing. The executor was corrected the same day: the transfer stage is now single-shot and judged against the accepted guide (duration within 0.5s, tail below 0.06), and such a chunk is recorded as **marginal** rather than regenerated. c05's final word `number.` aligned at 0.21s and its transfer matches the guide's length to 0.04s; it is complete. Carried to the Step 2 protocol as an amendment for the next episode.

## Completeness at capture

Every accepted guide decays into silence (tail energy below 0.02). Transfers: **1 marginal** (c05), all others clean.

| Chunk | Scenes | Chars | Guide attempts | Guide s | Transfer s | Guide tail | Transfer tail | Transfer |
|---|---|---:|---:|---:|---:|---:|---:|---|
| c01 | S00 | 910 | 3 | 59.5 | 59.5 | 0.0039 | 0.0004 | clean |
| c02 | S02+S03.1 | 1195 | 1 | 67.7 | 67.7 | 0.0178 | 0.0046 | clean |
| c03 | S03.2+S04 | 1172 | 1 | 73.4 | 73.4 | 0.0003 | 0.0004 | clean |
| c04 | S05 | 478 | 2 | 30.6 | 30.6 | 0.0071 | 0.0025 | clean |
| c05 | S06 | 1012 | 1 | 69.0 | 69.0 | 0.0098 | 0.0242 | marginal |
| c06 | S07 | 926 | 2 | 61.7 | 61.7 | 0.0188 | 0.0055 | clean |
| c07 | S08 | 675 | 1 | 41.6 | 41.6 | 0.0134 | 0.014 | clean |
| c08 | S09 | 1039 | 2 | 69.2 | 69.2 | 0.0169 | 0.0087 | clean |
| c09 | S10.1 | 876 | 1 | 51.9 | 52.0 | 0.0037 | 0.0016 | clean |
| c10 | S10.2 | 1012 | 2 | 57.3 | 57.3 | 0.0009 | 0.0008 | clean |
| c11 | S11 | 888 | 2 | 58.8 | 58.8 | 0.0013 | 0.0007 | clean |
| c12 | S12 | 993 | 1 | 54.5 | 54.6 | 0.0 | 0.0 | clean |
| c13 | S13 | 559 | 1 | 37.5 | 37.6 | 0.0049 | 0.0003 | clean |
| c14 | S14 | 887 | 2 | 63.0 | 63.0 | 0.0005 | 0.0 | clean |
| c15 | S15 | 772 | 1 | 56.3 | 56.3 | 0.001 | 0.0004 | clean |
| c16 | S16 | 636 | 1 | 41.2 | 41.2 | 0.0117 | 0.0043 | clean |
| c17 | S17.1 | 758 | 7 | 45.9 | 45.9 | 0.0 | 0.0 | clean |
| c18 | S17.2 | 870 | 2 | 58.3 | 58.3 | 0.0024 | 0.0043 | clean |
| c19 | S18 | 828 | 2 | 55.5 | 55.5 | 0.0035 | 0.0036 | clean |
| c20 | S19 | 888 | 2 | 58.8 | 58.8 | 0.0029 | 0.0026 | clean |
| c21 | S20+S21+S22 | 1228 | 1 | 80.5 | 80.5 | 0.0017 | 0.0003 | clean |
| c22 | S23+S24 | 432 | 3 | 29.0 | 29.0 | 0.0022 | 0.0009 | clean |

## Technical results

| Measure | Result | Assessment |
|---|---|---|
| Guide to transfer duration | 1220.9s to 1221.5s | performance timing preserved by the transfer |
| Chunk RMS spread before edit | 2.1 dB | finding N4B-1 carried from EP007; normalised at N5 to -22.0 dBFS, spread after 0.27 dB |
| Delivery rate | 167 words per minute on raw transfers | master 20.6 min with sting and scene room |
| Chunks ending mid-sound | 1 of 22, marginal (c05) | disclosed, complete by the final-word test |

## Disposition

N4B accepted on the technical evidence above. The owner's continuity listen is the N7 decision and is not implied by anything here.
