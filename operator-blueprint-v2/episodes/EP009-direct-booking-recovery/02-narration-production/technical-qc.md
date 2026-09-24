# N6 technical pass: EP009

Status: **technical_pass RECORDED** for master `e433c0fd6d7dd522`

Episode: EP009 · Recorded: 2026-09-03

Supersedes one earlier alignment against master `45e84c4ac383…`, invalidated by the c22 recapture. Recorded as superseded rather than overwritten.

## Frozen master

| | |
|---|---|
| Path | `master/narration-master.wav` |
| SHA-256 | `e433c0fd6d7dd522efb9f6593986f930f9ccc54b2be5132dec50c20ff3c1f944` |
| Duration | 1233.602s (20.6 min) |
| Format | 48 kHz / 16-bit / mono PCM |
| Integrated RMS | -22.04 dBFS |
| Peak | -5.62 dBFS |

Working master, not a delivery master. Final loudness normalisation is a delivery-stage decision and is deliberately not baked in.

## N5 narration edit

| Measure | Result |
|---|---|
| Chunk RMS spread | 2.08 dB before, **0.27 dB** after normalisation to -22.0 dBFS |
| Identity sting (S01) | **4.0s** of room after the cold open |
| Scene-boundary target | 0.62s |
| Within-scene split target | 0.46s |
| Total silence inserted | 12.14s across 21 joins |

Operations: gain normalisation, scene spacing, identity sting room, concatenation. **No spoken word was added, removed, reordered or rewritten.**

## Completeness verification

| Check | Result |
|---|---|
| Chunks ending mid-sound (tail energy > 0.02) | **1 of 22, marginal** (c05 at 0.024; final word `number.` 0.21s; transfer length matches the guide) |
| Chunk-final words below half the median spoken word | **0 of 22** |
| Median spoken word | 0.2s |
| Final word of the episode `one.` | 0.15s after the c22 recapture (was 0.10s) |

Forced alignment force-fits and cannot detect missing audio; these checks are what establish that the words were spoken.

## Lexical conformity

| Check | Result |
|---|---|
| `W` tokens | 3399 |
| Aligned words | 3399 |
| Unresolved mismatches | **0** |
| Alignment method | elevenlabs forced-alignment against the locked W transport |
| Alignment loss | 0.0969 |

## Artifacts

| Artifact | SHA-256 |
|---|---|
| `word-transcript.json` | `3c28411effaea94c4dffaac51e114f333f386170fe4716fa96b30d24e41384aa` |
| `intentional-pause-map.json` | `62811b5f0ae93359d520f7adfec06ebf46404e8e146cedf274b1f327f9a5cd84` |
| `narration-edit-decision-list.json` | `a6dc95f3eca8e8842aadab0feb3c1759bd7b458b34368fc88dd3f10d2e8ae633` |

3399 words bound to canonical `W` IDs. 318 pauses at or above 0.3s totalling 202.01s. Transcript and pause map are bound to master `e433c0fd6d7dd522`.

## Gate N6

All conditions pass, with the one marginal chunk disclosed as EP007's lock disclosed its own. **`technical_pass` recorded for this master.** It is a technical state only and cannot imply the performance is creatively approved; that is N7, the owner's listen.
