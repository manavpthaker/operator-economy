# Narration lock: EP007 — a sale-readiness practice

Status: **LOCKED**

Gate: **N7 — creative approval, narration lock, and Step 3 handoff**

Episode: EP007 · Locked: 2026-09-02 · Locked by: Manav Thaker

## Authoritative files

| Artifact | Path | SHA-256 |
|---|---|---|
| Narration master | `master/narration-master.v4.wav` | `d8f7cb9630ae12ad427dca2c7bd1f29611f56c7985ce900ea312df3b9fec8da9` |
| Word-level transcript | `word-transcript.json` | `f5decf2102d6cd565b89823e6fae38b2f4838c0984f7fce67f36c03cfa0f0ef7` |
| Intentional-pause map | `intentional-pause-map.json` | `0176614eb0902d945165956af8fa7ef890906d5f2e15692d14c9e0d9d8b8bdaa` |
| Narration edit decision list | `narration-edit-decision-list.json` | `d18175957e21860e47ae49137ed6b0e489cf8a89f91d224e292640cec3369c7b` |
| Take register | `take-register.json` | `4c685feb6b2fbf450ca6f39b8603c121992959fdf4bcc7038bee28b9397c15d6` |
| Technical QC | `technical-qc.md` | `9de8399099054504c9129fe1bc35bc9db618d987e47c1fb2767e8082900d5d9c` |
| Canonical `W` | `../01-editorial/canonical-w.txt` | `333a45d7449f5cb4c3e394a9e262c3a3a60c3825e76563bc0149498f0b41860c` |
| Editorial lock | `../01-editorial/editorial-lock.md` | `7d3871804c82e7da09a59c01cd5ef4342ad0ad9141158869acc71d6d291a1319` |

| | |
|---|---|
| Duration | **1137.927s** (18.97 min) |
| Word count | **3186** ordered `W` tokens |
| Format | 48 kHz / 16-bit / mono PCM |

## Decisions

**`technical_pass`** — recorded for this exact master hash. See `technical-qc.md`.

**`creative_approved`** — **granted by Manav Thaker on 2026-09-02**, naming master `d8f7cb9630ae12ad`.

Owner statement of record: `approved. sounds great.`

Neither decision implies the other. Both name the same master hash.

## Independent listen

**Not performed by a second person.** This is a one-operator production and no independent reviewer exists.

Recorded honestly rather than waived: the agent review pass **missed the defect the owner caught**. Nine of twenty-four chunks were ending mid-final-word, and the automated checks reported clean because forced alignment force-fits. The owner's listen is what surfaced it.

That is direct evidence the independent-listen requirement has value, and that automated conformity is not a substitute for it. The gap is disclosed, not closed.

## Conformity

| Check | Result |
|---|---|
| Unresolved `W`-token mismatches | **0** |
| Aligned words vs locked tokens | 3186 / 3186 |
| Alignment loss | 0.0453 |
| Chunks ending mid-sound | 1 of 24, marginal |
| Chunk-final words below half median | **0 of 24** |

No spoken word was added, removed, reordered or rewritten at any point. The locked script is unchanged and its lock still holds.

## Open items disclosed downstream

1. **This is a working master, not a delivery master.** Integrated RMS −22.0 dBFS with 1.31 dB of peak headroom. Final loudness normalisation is a delivery-stage decision and is deliberately not baked in.
2. **One chunk remains marginally above the tail-energy threshold.** Audible review found no defect; recorded rather than hidden.
3. **The independent listen was not performed.** See above.

## Step 3 handoff

Step 3 consumes:

| Input | Value |
|---|---|
| Narration master | `d8f7cb9630ae12ad427dca2c7bd1f29611f56c7985ce900ea312df3b9fec8da9` |
| Duration | 1137.927s |
| Word-level transcript | `f5decf2102d6cd565b89823e6fae38b2f4838c0984f7fce67f36c03cfa0f0ef7` — 3186 words bound to canonical `W` IDs |
| Intentional-pause map | `0176614eb0902d945165956af8fa7ef890906d5f2e15692d14c9e0d9d8b8bdaa` — 276 pauses ≥0.30s, 182.34s total |

**Step 3 reads timing from the transcript and may not estimate it.** Its V4 gate fails any unit whose timing is not bound to word indices from this file.

Any sample-level change to this master invalidates the transcript, the pause map, the technical pass, this lock, and the Step 3 handoff.

**Gate N7: PASSED. Narration locked. Step 2 is complete for EP007.**
