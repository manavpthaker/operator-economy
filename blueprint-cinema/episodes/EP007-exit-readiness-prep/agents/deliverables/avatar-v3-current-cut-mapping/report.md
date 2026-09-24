# R29 avatar replacement preparation

Five moving avatar slots and one final-frame hold are mapped in `mapping.json`. The accepted V3 opening covers only master 0–20.9; only the current opening slot can reuse it. Three new takes cover every remaining avatar word. All prepared WAVs preserve original mono PCM16 at 48 kHz, including pauses and handles.

| Current slot | Review interval | Original master interval | Replacement |
|---|---:|---:|---|
| Opening | 0–4.041667 | 0–4.041667 | Accepted V3 source frames 1–97, out 98; root integrates |
| Opportunity | 40.083333–44.5 | 40.083333–44.5 | New opportunity take, source 0.333333–4.75 |
| Post-title definition | 56.5–62.916667 | 59.5–65.916667 | New continuous post-title take, source 0–6.416667 |
| Post-title promise | 62.916667–71.5 | 65.916667–74.5 | Same new take, source 6.416667–15 |
| Question moving picture | 131–143.041667 | 134–146.041667 | New question take, source 0–12.041667 |
| Question final-frame hold | 143.041667–143.791667 | 146.041667–146.791667 | New question frame 288, held for the existing 18 frames |

Intervals are half-open. All picture times use the accepted 24 fps cut. The original master equals review time before review 45, then review time +3. The omitted master 45–48 contains exactly 144,000 zero-valued samples. All three existing root WAVs and the accepted V3 reference were byte-compared against their original master PCM ranges.

| Prepared take | Original sample range | WAV duration | Bounded video request |
|---|---:|---:|---:|
| `v3-opportunity` | 1,908,000–2,154,000 | 5.125 s | 6 s |
| `v3-post-title-continuous` | 2,856,000–3,576,000 | 15 s | 15 s |
| `v3-question` | 6,432,000–7,010,000 | 12.041667 s | 13 s |

The continuous post-title source preserves the definition-to-promise cut at review 62.916667 and the tighter crop at **67.58**, immediately after “and.” Keep the existing sizes and offsets, while advancing source time continuously. The source should not generate either crop change. This avoids restarting the performance between adjacent sentences without changing the accepted edit.

The question's actual close-cut cue is review 139.958333/master 142.958333, immediately before **“then”** at master 142.98. Older prose calls it “before who,” but the accepted runtime is authoritative. Keep its existing scale 1.08 to 1.2 change. Retain the 0.75-second picture hold using the new source's last selected frame. The accepted outgoing frame boundary occurs 11.667 ms after the transcript onset of “Nobody”; preserve it and do not describe the entire hold as digitally silent.

The V3 result records a **47.25 ms waveform insertion offset**, not a measured audiovisual lip-sync offset. Root selected source frame 1 (41.667 ms) for the 97-frame opening, leaving a 5.583 ms difference from waveform placement. New takes need their own waveform and perceptual checks; this offset must not transfer automatically.

Every prompt retains the accepted study portrait for identity, glasses, navy shirt, framing and lighting; Rebecca for relaxed settling and ordinary blinks; and Henry for clear articulation and brief emphasis that settles. Hands stay below frame. The wider-framing proposal is not selected. The supplied audio alone controls words and timing. The three local request plans preserve the existing Higgsfield Seedance 2.5 route and Fal original-audio restoration recipe, but are not submitted payloads or spending authority.

Verified: seven work-order pins, original master hash, reference hashes, current source frame counts, five mounted moving intervals, question hold, three exact original WAV excerpts and complete word coverage. `checks.json` records the results. No provider call, upload, new media generation, runtime edit, approval claim or canonical-state change occurred. New performance, perceptual lip sync, final-frame settling and provider duration/pricing remain outside this preparation packet.
