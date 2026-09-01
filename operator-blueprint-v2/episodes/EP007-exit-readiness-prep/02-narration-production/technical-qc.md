# N6 technical pass: EP007

Status: **technical_pass RECORDED**

Gate: **N6 — exact master receives `technical_pass`**

Episode: EP007 · Recorded: 2026-09-01

## Frozen master

| | |
|---|---|
| Path | `master/narration-master.normalized.wav` |
| SHA-256 | `681e77a3d1bba33a58f1c526d1fdc92acf651a8cfa672e2a70c09a9ee196c99b` |
| Duration | 1075.223s (17.9 min) |
| Format | 48 kHz / 16-bit / mono PCM |
| Integrated RMS | -22.00 dBFS |
| True peak | -1.31 dBFS |

## Format and origin

- Native acquisition: **`native_pcm`** at both stages. Google returned 24 kHz LINEAR16; ElevenLabs returned `pcm_48000`.
- **No lossy intermediate exists after native acquisition.** The mp3 used for forced alignment is a transport artifact derived from this exact master and is not a delivery master.
- Raw provider outputs remain **immutable** at mode 0600 in `raw/`. The edit wrote to `selects/`.
- Conversions applied after acquisition: **one** — per-chunk gain normalisation, recorded in `narration-edit-decision-list.json`.

## N5 narration edit

Per-chunk gain normalisation, downward to a common floor.

| Measure | Before | After |
|---|---|---|
| Chunk RMS spread | 4.93 dB | **0.2 dB** |
| Peak | -0.33 dBFS | -1.31 dBFS |
| Gains capped | — | **0** |

Rationale recorded in the EDL: chunks already peaked near −0.33 dBFS, so raising quiet chunks was impossible without clipping. Normalising downward resolves finding **N4B-1** (level drift) and finding **F3** (no headroom) in a single conversion. Every gain is negative or near zero, so nothing was pushed into the ceiling.

No spoken word was added, removed, reordered or rewritten. **No script change is hidden inside the edit.**

## Lexical conformity

| Check | Result |
|---|---|
| Locked `W` token count | 3186 |
| Aligned words | 3186 |
| **Unresolved `W`-token mismatches** | **0** |
| Alignment method | ElevenLabs forced alignment against the locked `W` transport |
| Alignment loss | 0.0449 |

Every aligned word matches its canonical `W` token exactly, in order. Interim ASR was not used and could not have satisfied this gate.

## Word-level transcript and pause map

| Artifact | SHA-256 | Bound to |
|---|---|---|
| `word-transcript.json` | `9606c3e7a4adc8c64f75454c3c68be94b23fff6f9047e3fcd0be4a4dea777862` | master `681e77a3d1bba33a`, duration 1075.223s |
| `intentional-pause-map.json` | `8189541105846520746d47a6633256f785c65116643ee68b41cb0ad8eb131bd8` | same master and duration |

Transcript carries 3186 words, each bound to its canonical `W` ID. The pause map records 228 intentional pauses at or above 0.30s.

**This is the artifact Step 3 consumes.** Step 3 reads timing from it and may not estimate.

## Gate N6 conditions

| Condition | Result |
|---|---|
| Final master meets the Step 2 technical contract | **pass** |
| Native acquisition and delivery format separately disclosed | **pass** |
| No lossy intermediate after native acquisition | **pass** |
| One master candidate frozen before final alignment | **pass** |
| Final-master alignment run against that exact master hash | **pass** |
| Zero unresolved `W`-token mismatches | **pass** |
| Word-level transcript satisfies the timing specification | **pass** |
| Intentional-pause map bound to the same master hash and duration | **pass** |
| Master, transcript and pause-map hashes recorded together | **pass** |
| Technical measurements complete | **pass** |

**`technical_pass` is recorded for this exact master hash.**

`technical_pass` is a technical state only. **It cannot imply that the voice or the performance is approved.** That is N7, and it is the owner's decision.

## Carried to delivery

Integrated RMS is -22.00 dBFS with 1.3 dB of peak headroom. This is a **working master**, not a delivery master. Final loudness normalisation is a delivery-stage decision and is deliberately not baked in here.
