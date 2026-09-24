# N6 technical pass: EP007 — master v4

Status: **technical_pass RECORDED** for master v4

Episode: EP007 · Recorded: 2026-09-01

Supersedes the passes against `.normalized`, `.v2` and `.v3`, each invalidated by a later edit. Recorded as superseded rather than overwritten.

## Frozen master

| | |
|---|---|
| Path | `master/narration-master.v4.wav` |
| SHA-256 | `d8f7cb9630ae12ad427dca2c7bd1f29611f56c7985ce900ea312df3b9fec8da9` |
| Duration | 1137.927s (19.0 min) |
| Format | 48 kHz / 16-bit / mono PCM |
| Integrated RMS | -21.99 dBFS |
| True peak | -1.31 dBFS |

## What was wrong, and how it was found

**Owner listen: "it cuts off at 'almost nobody is'".**

The word `running.` was being cut mid-utterance. Investigation found this was not isolated — **9 of 24 chunks ended mid-final-word**, five of them losing roughly half a second, which is most of a word.

### Why the existing QA did not catch it

**Forced alignment force-fits.** It assigns best-fit timings to whatever text it is given and does not detect missing audio. The N6 lexical check reported **zero unresolved `W`-token mismatches** while nine chunk-final words were incomplete. That check established that the aligner could map text onto audio. It never established that the words were spoken.

This is a hole in the gate's wording, not only in this run. `Zero unresolved W-token mismatches` is satisfiable by an aligner on truncated audio.

### The detector that works

**Tail energy** — RMS of the final 60 ms relative to peak. A complete utterance decays into silence and measures below 0.01. The truncated chunks measured 0.13 to 0.54.

It is a **capture-time** check. Catching this at N4B costs one retry. Catching it at N6 costs a full re-alignment. Catching it on the owner's ear costs a listening pass and four master revisions.

## Repairs, in order

1. **Re-capture, tail-energy gated.** 14 chunks above threshold re-requested with up to 4 attempts each. Truncation proved stochastic: 11 cleared, some on the first retry.
2. **Sentinel for the two that would not clear.** c02 and c09 truncated reliably rather than randomly. Generated with a trailing sentinel phrase so the truncation consumed the sentinel instead of the content.
3. **Alignment-guided trim, after a self-inflicted error.** The first trim cut at "the last silence gap", which removed the real final word along with the sentinel — `all.` fell to 0.001s and `version.` to 0.009s. Replaced with a trim at the last real word's aligned end plus 120 ms. Both recovered.

## Completeness verification

| Check | Result |
|---|---|
| Chunks ending mid-sound (tail energy > 0.02) | **1 of 24**, marginal |
| Chunk-final words below half the median spoken word | **0 of 24** (was 9 truncated, then 2 over-trimmed) |
| `running.`, the reported defect | **0.340s** (was 0.120s) |
| Median spoken word | 0.199s |

## N5 narration edit

| Measure | Result |
|---|---|
| Chunk RMS spread | **0.2 dB** |
| Identity sting (S01) | **4.0s**, absent before |
| Scene-boundary target | 0.62s — the narrator's own median pause |
| Within-scene split target | 0.46s — the narrator's lower quartile |
| Total silence inserted | 13.06s |

Padding targets are derived from this performance's own pause distribution, not chosen. **No spoken word was added, removed, reordered or rewritten.**

## Lexical conformity

| Check | Result |
|---|---|
| `W` tokens | 3186 |
| Aligned words | 3186 |
| Unresolved mismatches | **0** |
| Alignment loss | 0.0453 |

Now supported by the completeness check above, without which this figure is not sufficient evidence.

## Artifacts

| Artifact | SHA-256 |
|---|---|
| `word-transcript.json` | `f5decf2102d6cd565b89823e6fae38b2f4838c0984f7fce67f36c03cfa0f0ef7` |
| `intentional-pause-map.json` | `0176614eb0902d945165956af8fa7ef890906d5f2e15692d14c9e0d9d8b8bdaa` |

3186 words bound to canonical `W` IDs. 276 pauses at or above 0.30s totalling 182.34s.

## Gate N6

All conditions pass. **`technical_pass` recorded for master v4.** It remains a technical state and cannot imply the performance is approved — that is N7.

## Proposed Step 2 amendment

Add a **completeness condition** to N4B and N6:

> Every captured chunk must decay into silence. Tail energy in the final 60 ms, relative to peak, must fall below 0.02. Forced alignment satisfying zero `W`-token mismatches is **not** sufficient evidence that the words were spoken.

This would have caught the defect at capture, before four master revisions and three alignments.
