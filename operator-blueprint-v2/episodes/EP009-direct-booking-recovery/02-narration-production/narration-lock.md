# Narration lock: EP009 — a direct-booking practice

Status: **LOCKED**

Gate: **N7 — creative approval, narration lock, and Step 3 handoff**

Episode: EP009 · Locked: 2026-09-03 · Locked by: Manav Thaker

## Authoritative files

| Artifact | Path | SHA-256 |
|---|---|---|
| Narration master | `master/narration-master.wav` | `e433c0fd6d7dd522efb9f6593986f930f9ccc54b2be5132dec50c20ff3c1f944` |
| Word-level transcript | `word-transcript.json` | `3c28411effaea94c4dffaac51e114f333f386170fe4716fa96b30d24e41384aa` |
| Intentional-pause map | `intentional-pause-map.json` | `62811b5f0ae93359d520f7adfec06ebf46404e8e146cedf274b1f327f9a5cd84` |
| Narration edit decision list | `narration-edit-decision-list.json` | `a6dc95f3eca8e8842aadab0feb3c1759bd7b458b34368fc88dd3f10d2e8ae633` |
| Take register | `take-register.json` | `9c2c9abbad91d74718e0a0527f1aec1bb8e4a960a7af7a37ca756af22a83593f` |
| Technical QC | `technical-qc.md` | `3ad9e8994cdbe3680f4b85695166e831d2e7fb35ae7b873b6e0c04e9a43fa4a5` |
| Full capture review | `full-capture-review.md` | `f291197dd10e85bab25bd4dece64db15cf959344cdedbd6bb5b69d8c25aa7e8f` |
| Performance direction | `performance-direction.md` | `1dc6df6205747515f3cea1505df648ac469fce37670d8f3ca16a19bf96c7830d` |
| Canonical `W` | `../01-editorial/canonical-w.txt` | `7b9d18bfb2820a124f96308568cbb5509eef792a38150a5e78c3643ced9e191e` |
| Editorial lock | `../01-editorial/editorial-lock.md` | `246330740a5c7447e455f967b7a8597a3a8352fa417ff1f241e730c448da2d20` |
| Narration handoff | `../01-editorial/narration-handoff.md` | `a4472ffdf32803b72887490cb2ed92b4d02b302fd538af967e56166fbb34d6e1` |

| | |
|---|---|
| Duration | **1233.602s** (20.56 min) |
| Word count | **3399** ordered `W` tokens |
| Format | 48 kHz / 16-bit / mono PCM |

## Decisions

**`technical_pass`** — recorded for this exact master hash. See `technical-qc.md`.

**`creative_approved`** — **granted by Manav Thaker on 2026-09-03**, after listening to the review copy rendered from master `e433c0fd6d7dd522` (192 kbit/s MP3 derived from this exact WAV and delivered the same day, alongside the sibling episode's).

Owner statement of record: `good to go`

The statement did not name the hash; it was given in direct reply to the delivery of the two review copies, each captioned with its master hash, and is recorded here against this one. Neither decision implies the other. Both name the same master hash.

## Independent listen

**Not performed by a second person.** This is a one-operator production and no independent reviewer exists. Recorded honestly rather than waived, as on EP007. The automated completeness checks (tail energy per chunk, chunk-final word duration) were run at capture and again at N6 precisely because EP007 showed that the owner's ear, not the aligner, catches a clipped word.

## Conformity

| Check | Result |
|---|---|
| Unresolved `W`-token mismatches | **0** |
| Aligned words vs locked tokens | 3399 / 3399 |
| Alignment loss | 0.0969 |
| Chunks ending mid-sound | 1 of 22, marginal (c05, final word at full length, transfer length matches guide) |
| Chunk-final words below half median | **0 of 22** |

No spoken word was added, removed, reordered or rewritten at any point. The locked script is unchanged and its lock still holds.

## Open items disclosed downstream

1. **This is a working master, not a delivery master.** Integrated RMS -22.04 dBFS, peak -5.62 dBFS. Final loudness normalisation is a delivery-stage decision and is deliberately not baked in.
2. **Scene room targets were inherited from EP007's measured pause distribution** (0.62s at a scene boundary, 0.46s inside a split scene, 4.0s identity sting) rather than recomputed from this master. This master's own pause map (318 pauses, 202.01s) is available if Step 3 wants the joins retuned; any such change is a new master and returns to N6.
3. **One chunk remains marginally above the tail-energy threshold** (c05, 0.024). Its final word aligned at 0.21s and the transfer matches the guide length; recorded rather than hidden.
4. **The independent listen was not performed.** See above.

## Step 3 handoff

Step 3 consumes:

| Input | Value |
|---|---|
| Narration master | `e433c0fd6d7dd522efb9f6593986f930f9ccc54b2be5132dec50c20ff3c1f944` |
| Duration | 1233.602s |
| Word-level transcript | `3c28411effaea94c4dffaac51e114f333f386170fe4716fa96b30d24e41384aa` — 3399 words bound to canonical `W` IDs |
| Intentional-pause map | `62811b5f0ae93359d520f7adfec06ebf46404e8e146cedf274b1f327f9a5cd84` — 318 pauses ≥0.30s, 202.01s total |

**Step 3 reads timing from the transcript and may not estimate it.** Its V4 gate fails any unit whose timing is not bound to word indices from this file. Step 3 itself remains a proposed standard awaiting the owner's process approval; this handoff is ready for it and authorizes nothing visual.

Any sample-level change to this master invalidates the transcript, the pause map, the technical pass, this lock, and the Step 3 handoff.

**Gate N7: PASSED. Narration locked. Step 2 is complete for EP009.**
