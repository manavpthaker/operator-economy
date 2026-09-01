# N6 technical pass: EP007 — master v2

Status: **technical_pass RECORDED** for master v2

Episode: EP007 · Recorded: 2026-09-01

**Supersedes** the technical pass against `narration-master.normalized.wav`, invalidated by the N5 spacing edit. Recorded rather than overwritten, per the invalidation rules.

## Frozen master

| | |
|---|---|
| Path | `master/narration-master.v2.wav` |
| SHA-256 | `7d027451d8c644c3a831513ea93e771295ecac8ae9323147c755d209e1793967` |
| Duration | 1088.112s (18.1 min) |
| Format | 48 kHz / 16-bit / mono PCM |
| Integrated RMS | -22.00 dBFS |
| True peak | -1.31 dBFS |

## N5 narration edit — two operations, both recorded

### 1. Level normalisation

| Measure | Before | After |
|---|---|---|
| Chunk RMS spread | 4.93 dB | **0.2 dB** |
| Peak | -0.33 dBFS | -1.31 dBFS |
| Gains capped | — | **0** |

### 2. Scene spacing and identity sting

**Found by owner listen:** the line before the brand string read as cut off at 0:40.

Diagnosis: the cold open was **not** truncated — it decays cleanly with 20 ms of trailing silence. The defect was structural. The beat sheet requires **S01, a 3 to 6 second silent identity sting**, between the cold open and the brand string. The capture plan skipped S01 because it carries no narration text, so the assembly butt-joined the two chunks with a 60 ms gap.

Auditing all 23 joins showed the problem was systematic, not isolated:

| | Value |
|---|---|
| Mean join gap | 0.125s |
| Narrator's own median pause | 0.55s |
| Ratio | **joins were ~5x tighter than this voice's own pauses** |

Every scene boundary read as a cut, not just the one that was noticed.

Padding targets are **derived from this performance's own pause distribution**, not chosen:

| Join type | Target | Basis |
|---|---|---|
| Silent identity sting (S00 → S02) | 4.0s | Beat sheet requirement, 3 to 6s |
| Scene boundary | 0.546s | Narrator's median pause |
| Within-scene split | 0.429s | Narrator's lower-quartile pause |

Total silence inserted: **12.9s** across 23 joins. No audio was cut, resampled or re-rendered. **No spoken word was added, removed, reordered or rewritten.**

## Lexical conformity

| Check | Result |
|---|---|
| Locked `W` token count | 3186 |
| Aligned words | 3186 |
| **Unresolved `W`-token mismatches** | **0** |
| Alignment loss | 0.0450 |

Re-run in full against master v2. The prior alignment was invalidated by the edit and was not carried forward.

## Word-level transcript and pause map

| Artifact | SHA-256 |
|---|---|
| `word-transcript.json` | `b7bc691f2f76921688d6d9262425e44f73a36ba3fedc976b21de94d110260eb8` |
| `intentional-pause-map.json` | `311ee525d80369e33e55b53838e254ba2c5d988813bd0b390a72651985177018` |

3186 words bound to canonical `W` IDs. 237 intentional pauses at or above 0.30s totalling 150.97s.

**The identity sting now reads as a real beat:** a 3.93s pause after `W000117`, the final token of the cold open, at 40.22s.

## Gate N6 conditions

| Condition | Result |
|---|---|
| Final master meets the technical contract | **pass** |
| Native and delivery formats separately disclosed | **pass** |
| No lossy intermediate after native acquisition | **pass** |
| One master candidate frozen before final alignment | **pass** |
| Alignment run against that exact master hash | **pass** |
| Zero unresolved `W`-token mismatches | **pass** |
| Transcript satisfies the timing specification | **pass** |
| Pause map bound to the same master hash and duration | **pass** |
| Hashes recorded together | **pass** |
| Technical measurements complete | **pass** |

**`technical_pass` recorded for master v2.** It remains a technical state and cannot imply the performance is approved. That is N7.
