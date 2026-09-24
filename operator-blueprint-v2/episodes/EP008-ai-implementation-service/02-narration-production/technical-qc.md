# N6 technical pass: EP008

Status: **technical_pass RECORDED** for master `f3d749314141dc2f`

Episode: EP008 · Recorded: 2026-09-03

## Frozen master

| | |
|---|---|
| Path | `master/narration-master.wav` |
| SHA-256 | `f3d749314141dc2ff158fa2860203cb3431aa6d052230dad9e89112d86ad571e` |
| Duration | 1223.556s (20.4 min) |
| Format | 48 kHz / 16-bit / mono PCM |
| Integrated RMS | -22.04 dBFS |
| Peak | -5.94 dBFS |

Working master, not a delivery master. Final loudness normalisation is a delivery-stage decision and is deliberately not baked in.

## N5 narration edit

| Measure | Result |
|---|---|
| Chunk RMS spread | 2.03 dB before, **0.33 dB** after normalisation to -22.0 dBFS |
| Identity sting (S01) | **4.0s** of room after the cold open |
| Scene-boundary target | 0.62s (EP007's measured median pause for this narrator configuration) |
| Within-scene split target | 0.46s |
| Total silence inserted | 12.31s across 20 joins |

Operations: gain normalisation, scene spacing, identity sting room, concatenation. **No spoken word was added, removed, reordered or rewritten.**

## Completeness verification

| Check | Result |
|---|---|
| Chunks ending mid-sound (tail energy > 0.02) | **0 of 21** |
| Chunk-final words below half the median spoken word | **0 of 21** |
| Median spoken word | 0.2s |

Forced alignment force-fits and cannot detect missing audio; these two checks are what establish that the words were spoken.

## Lexical conformity

| Check | Result |
|---|---|
| `W` tokens | 3400 |
| Aligned words | 3400 |
| Unresolved mismatches | **0** |
| Alignment method | elevenlabs forced-alignment against the locked W transport |
| Alignment loss | 0.0718 |

## Artifacts

| Artifact | SHA-256 |
|---|---|
| `word-transcript.json` | `ad6d372e41d1a24ea0f8a93d64a66051c67426accfcb5a56774eec2b422c04ee` |
| `intentional-pause-map.json` | `9e6bc05de75956f7c437aa7cb4ff02bb21b109a75e9d22c288dd785cbdd6120c` |
| `narration-edit-decision-list.json` | `b19730b633845c616f900614839bd46a5caf9c75f845ea3f19a447ae4b2c6ced` |

3400 words bound to canonical `W` IDs. 318 pauses at or above 0.3s totalling 208.41s. Transcript and pause map are bound to master `f3d749314141dc2f`.

## Gate N6

All conditions pass. **`technical_pass` recorded for this master.** It is a technical state only and cannot imply the performance is creatively approved; that is N7, the owner's listen.
