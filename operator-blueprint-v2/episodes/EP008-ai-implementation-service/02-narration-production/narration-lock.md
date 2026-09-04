# Narration lock: EP008 — a helpdesk setup practice

Status: **LOCKED**

Gate: **N7 — creative approval, narration lock, and Step 3 handoff**

Episode: EP008 · Locked: 2026-09-03 · Locked by: Manav Thaker

## Authoritative files

| Artifact | Path | SHA-256 |
|---|---|---|
| Narration master | `master/narration-master.wav` | `f3d749314141dc2ff158fa2860203cb3431aa6d052230dad9e89112d86ad571e` |
| Word-level transcript | `word-transcript.json` | `ad6d372e41d1a24ea0f8a93d64a66051c67426accfcb5a56774eec2b422c04ee` |
| Intentional-pause map | `intentional-pause-map.json` | `9e6bc05de75956f7c437aa7cb4ff02bb21b109a75e9d22c288dd785cbdd6120c` |
| Narration edit decision list | `narration-edit-decision-list.json` | `b19730b633845c616f900614839bd46a5caf9c75f845ea3f19a447ae4b2c6ced` |
| Take register | `take-register.json` | `f5d52e17c4419baa3578e6cdbbf8808220faa1def72aa195e0dc95ab7c997faf` |
| Technical QC | `technical-qc.md` | `1052fd5bca9d0a9ef48430e2d1037baa26dc882f6fb940b9a8b86ba9c0dc618e` |
| Full capture review | `full-capture-review.md` | `941f15bab8ac9cba3f54cfc0e0f5be3727ac36b118281d1f05f2f700674c8a8a` |
| Performance direction | `performance-direction.md` | `961c9ddbdf0b733d45b5d284ee0b0464dc99eb9e63159742eb2e3311ba2cc830` |
| Canonical `W` | `../01-editorial/canonical-w.txt` | `ea3743bfcc6e881a96902556959d141f5a75a2288ecad713ccc6fa7ba787ca63` |
| Editorial lock | `../01-editorial/editorial-lock.md` | `76e41bfd02883e7f199d976440fe5e262e8b74d13f4a8e8b5f7b4750eac01874` |
| Narration handoff | `../01-editorial/narration-handoff.md` | `f94c7eb47ec34a5e8c5053be4d87caeabe4901c0a027eafad3daca3d3580536b` |

| | |
|---|---|
| Duration | **1223.556s** (20.39 min) |
| Word count | **3400** ordered `W` tokens |
| Format | 48 kHz / 16-bit / mono PCM |

## Decisions

**`technical_pass`** — recorded for this exact master hash. See `technical-qc.md`.

**`creative_approved`** — **granted by Manav Thaker on 2026-09-03**, after listening to the review copy rendered from master `f3d749314141dc2f` (192 kbit/s MP3 derived from this exact WAV and delivered the same day, alongside the sibling episode's).

Owner statement of record: `good to go`

The statement did not name the hash; it was given in direct reply to the delivery of the two review copies, each captioned with its master hash, and is recorded here against this one. Neither decision implies the other. Both name the same master hash.

## Independent listen

**Not performed by a second person.** This is a one-operator production and no independent reviewer exists. Recorded honestly rather than waived, as on EP007. The automated completeness checks (tail energy per chunk, chunk-final word duration) were run at capture and again at N6 precisely because EP007 showed that the owner's ear, not the aligner, catches a clipped word.

## Conformity

| Check | Result |
|---|---|
| Unresolved `W`-token mismatches | **0** |
| Aligned words vs locked tokens | 3400 / 3400 |
| Alignment loss | 0.0718 |
| Chunks ending mid-sound | 0 of 21 |
| Chunk-final words below half median | **0 of 21** |

No spoken word was added, removed, reordered or rewritten at any point. The locked script is unchanged and its lock still holds.

## Open items disclosed downstream

1. **This is a working master, not a delivery master.** Integrated RMS -22.04 dBFS, peak -5.94 dBFS. Final loudness normalisation is a delivery-stage decision and is deliberately not baked in.
2. **Scene room targets were inherited from EP007's measured pause distribution** (0.62s at a scene boundary, 0.46s inside a split scene, 4.0s identity sting) rather than recomputed from this master. This master's own pause map (318 pauses, 208.41s) is available if Step 3 wants the joins retuned; any such change is a new master and returns to N6.
3. No chunk is above the tail-energy threshold.
4. **The independent listen was not performed.** See above.

## Step 3 handoff

Step 3 consumes:

| Input | Value |
|---|---|
| Narration master | `f3d749314141dc2ff158fa2860203cb3431aa6d052230dad9e89112d86ad571e` |
| Duration | 1223.556s |
| Word-level transcript | `ad6d372e41d1a24ea0f8a93d64a66051c67426accfcb5a56774eec2b422c04ee` — 3400 words bound to canonical `W` IDs |
| Intentional-pause map | `9e6bc05de75956f7c437aa7cb4ff02bb21b109a75e9d22c288dd785cbdd6120c` — 318 pauses ≥0.30s, 208.41s total |

**Step 3 reads timing from the transcript and may not estimate it.** Its V4 gate fails any unit whose timing is not bound to word indices from this file. Step 3 itself remains a proposed standard awaiting the owner's process approval; this handoff is ready for it and authorizes nothing visual.

Any sample-level change to this master invalidates the transcript, the pause map, the technical pass, this lock, and the Step 3 handoff.

**Gate N7: PASSED. Narration locked. Step 2 is complete for EP008.**
