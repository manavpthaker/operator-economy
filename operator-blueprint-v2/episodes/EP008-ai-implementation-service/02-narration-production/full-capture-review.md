# N4B full capture review: EP008

Status: **technical review complete; owner continuity listen pending (N7)**

Episode: EP008

Captured: 2026-09-03

Configuration: `n3-two-stage-acted-guide-v2`, Google `gemini-2.5-pro-tts` voice `Algieba` under the candidate-C4 register, transferred to Original C `scMbPZwQjr40V1MzL3Nj` via `eleven_multilingual_sts_v2`. Frozen in `n3-configuration-freeze.md`; authorized in `n4b-authorization.md`.

## Capture

| | |
|---|---|
| Narration blocks | 22 (S01 silent, not captured) |
| Capture chunks | 21 |
| Provider calls | 60 Google, 22 ElevenLabs |
| Guide regenerations under the completeness contract | 22 |
| Re-split recorded | {'S17': 3, 'S18': 2} (S17 into three parts and S18 into two, so a passage that truncated eight times in a row ends mid-chunk; no spoken word changed) |
| Raw transfer duration | 1211.2s = **20.2 minutes** |
| Format | guides LINEAR16 24 kHz mono; transfers PCM 48 kHz / 16-bit / mono, no lossy intermediate |

Chunking respected the N3 rule: grouped on Step 1 narration-block boundaries, never splitting a block unless it alone exceeded the ceiling, with the F2 short-tail merge.

## Completeness at capture

Every accepted guide decays into silence (tail energy below 0.02). The provider truncated the final word stochastically and the gate caught every case before any ElevenLabs credit was spent on it. The transfer stage is seeded and therefore deterministic; one chunk with a faint but matching-length tail would have been recorded as marginal, and for this episode **none** were.

| Chunk | Scenes | Chars | Guide attempts | Guide s | Transfer s | Guide tail | Transfer tail | Transfer |
|---|---|---:|---:|---:|---:|---:|---:|---|
| c01 | S00 | 803 | 1 | 48.7 | 48.7 | 0.0027 | 0.001 | clean |
| c02 | S02+S03.1 | 1112 | 3 | 64.6 | 64.6 | 0.0002 | 0.0002 | clean |
| c03 | S03.2+S04 | 1032 | 1 | 65.5 | 65.6 | 0.0011 | 0.0003 | clean |
| c04 | S05 | 574 | 4 | 43.6 | 43.7 | 0.0 | 0.0 | clean |
| c05 | S06 | 825 | 1 | 56.1 | 56.1 | 0.0077 | 0.0039 | clean |
| c06 | S07 | 1123 | 3 | 78.5 | 78.6 | 0.0086 | 0.0024 | clean |
| c07 | S08 | 816 | 1 | 51.9 | 51.9 | 0.0074 | 0.0076 | clean |
| c08 | S09.1 | 585 | 5 | 40.7 | 40.7 | 0.0017 | 0.0029 | clean |
| c09 | S09.2 | 757 | 3 | 48.4 | 48.4 | 0.0071 | 0.0023 | clean |
| c10 | S10.1 | 922 | 2 | 60.1 | 60.1 | 0.0019 | 0.0008 | clean |
| c11 | S10.2 | 1008 | 1 | 69.1 | 69.1 | 0.0189 | 0.0077 | clean |
| c12 | S11 | 781 | 1 | 52.9 | 52.9 | 0.0006 | 0.0007 | clean |
| c13 | S12 | 932 | 1 | 55.5 | 55.5 | 0.0059 | 0.0028 | clean |
| c14 | S13 | 852 | 1 | 46.1 | 46.2 | 0.0019 | 0.0027 | clean |
| c15 | S14 | 914 | 1 | 58.3 | 58.4 | 0.0028 | 0.003 | clean |
| c16 | S16+S17.1 | 1156 | 4 | 68.7 | 68.7 | 0.0007 | 0.0014 | clean |
| c17 | S17.2+S17.3 | 913 | 2 | 60.7 | 60.7 | 0.0047 | 0.0062 | clean |
| c18 | S17.4+S18.1 | 987 | 1 | 61.0 | 61.0 | 0.0171 | 0.0051 | clean |
| c19 | S18.2+S19 | 1154 | 3 | 83.7 | 83.7 | 0.0033 | 0.0065 | clean |
| c20 | S20+S21 | 1075 | 2 | 69.5 | 69.5 | 0.0002 | 0.0006 | clean |
| c21 | S22+S23 | 385 | 2 | 27.2 | 27.2 | 0.0 | 0.0 | clean |

## Technical results

| Measure | Result | Assessment |
|---|---|---|
| Guide to transfer duration | 1210.8s to 1211.2s | performance timing preserved by the transfer |
| Chunk RMS spread before edit | 2.0 dB | **finding N4B-1 carried from EP007**: chunks are independent generations and drift in level; normalised at N5 to -22.0 dBFS, spread after 0.33 dB |
| Delivery rate | 168 words per minute on raw transfers | inside the lock's expected range once the sting and scene room are added (master 20.4 min) |
| Chunks ending mid-sound | 0 of 21 | pass |

## Disposition

N4B accepted on the technical evidence above. The owner's continuity listen is the N7 decision and is not implied by anything here.
