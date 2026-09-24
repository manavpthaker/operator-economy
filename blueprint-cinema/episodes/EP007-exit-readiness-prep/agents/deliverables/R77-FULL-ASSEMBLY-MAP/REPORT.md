# R77 — EP007 full-review assembly map

The existing sources can fill a **27,241-frame, 24 fps review: 18:55.041667**. S14–S26 tile continuously, with no unexpected master or output gap/overlap. The forthcoming S15/S16 tool inserts must retain those scene lengths. R76 supplies S17 C, but this audit does not claim acceptance of its newly integrated performance. No assembly was rendered.

All frame intervals below are **half-open**. Exact clip paths, SHA-256 pins, source trims, output ranges and audio instructions are in [ASSEMBLY-MAP.json](/Users/brownmanbrain/GitHub/operator-economy/blueprint-cinema/episodes/EP007-exit-readiness-prep/agents/deliverables/R77-FULL-ASSEMBLY-MAP/ASSEMBLY-MAP.json). Every selected clip was hashed and its encoded stream metadata inspected. Fourteen unique selected sources match existing event artifact pins; R76 matches its alignment-source pin. See [BINDING-CHECK.json](/Users/brownmanbrain/GitHub/operator-economy/blueprint-cinema/episodes/EP007-exit-readiness-prep/agents/deliverables/R77-FULL-ASSEMBLY-MAP/BINDING-CHECK.json).

| Part | Master frames | Source frames | Output frames | Length |
|---|---:|---:|---:|---:|
| PREFIX | [0, 13446) | [0, 13376) | [0, 13376) | 13376 f |
| S14 | [13446, 15216) | [192, 1962) | [13376, 15146) | 1770 f |
| S15 | [15216, 16584) | [192, 1560) | [15146, 16514) | 1368 f |
| S16 | [16584, 17877) | [192, 1485) | [16514, 17807) | 1293 f |
| S17-P1 | [17877, 18588) | [192, 903) | [17807, 18518) | 711 f |
| S17-C | [18588, 18780) | [8, 200) | [18518, 18710) | 192 f |
| S17-P2 | [18780, 19488) | [903, 1611) | [18710, 19418) | 708 f |
| S18 | [19488, 20268) | [192, 972) | [19418, 20198) | 780 f |
| S19 | [20268, 21384) | [0, 1116) | [20198, 21314) | 1116 f |
| S20 | [21384, 23658) | [0, 2274) | [21314, 23588) | 2274 f |
| S21 | [23658, 25130) | [0, 1472) | [23588, 25060) | 1472 f |
| S22 | [25130, 25654) | [0, 524) | [25060, 25584) | 524 f |
| S23 | [25654, 25884) | [0, 230) | [25584, 25814) | 230 f |
| S24 | [25884, 26436) | [0, 552) | [25814, 26366) | 552 f |
| S25 | [26436, 27162) | [0, 726) | [26366, 27092) | 726 f |
| S26 | [27162, 27311) | [0, 149) | [27092, 27241) | 149 f |

**Preserve two clocks.** R58 has 13,376 frames (557.333333 s) and reaches master 560.25. Its first 45 seconds follow master directly; master 45–48 is omitted. From master 48 to S12 A the review is 72 frames earlier. Accepted S12 A becomes 265 output frames for 263 nominal master frames. From master 464.958333 onward, including every S14–S26 scene, output frame = master frame −70. The complete duration is frame-aligned master EOF 27,311 −72 +2 = **27,241 frames**, timecode **00:18:55:01**.

**Audio assembly:** retain R58 audio content/gain for output samples [0, 26,752,000). A read-only decode confirmed exactly 26,752,000 stereo samples per channel. Append original mono master samples [26,892,000, 54,620,519), then 1,481 zero samples. Duplicate mono to stereo at unity if needed. This gives 54,482,000 samples at 48 kHz. It preserves all source audio through EOF and the 30.854167 ms final picture padding. Do not lay the raw master from zero under R58: that would undo the sting omission, inherited callback pickup and accepted S12 pace pickup. Do not reapply R58's four presenter gain fixes.

**Clip choices:** S14/S15/S16 use the exact accepted context renders, each trimmed past its 192-frame lead-in. S17 uses accepted animation-context [192,903), R76 restored source [8,200), then animation-context [903,1611). The old animation context contains no C; treating it as a complete S17 would lose eight seconds. S18 uses its accepted context [192,972). S19 is corrected **R64B**, S20 the final capacity-outline version, and S26 **R75 Boundary Ledger**, not superseded R73/R74. Later review lead-ins are omitted, including S24's clipped-word wrapper.

**Pending replacements:** S15 cue window master 659.32–671.16 and S16 699.86–727.18 identify the intended inserts, not final frame trims. Their final recording paths, exact selected frames and hashes are not yet available. The JSON keeps accepted baseline scenes usable and marks both overrides pending; it cannot be called the finished requested cut until those are bound.

**Inherited review limits to expose:** R58's own provenance still leaves the R39 callback/performance without a scoped verdict, the R39 animation at master 257.875–270.0 returned, and R47 performance at 290.291667–301.5 without an output verdict. This is a source-record finding; no new creative approval or automatic requirement to redo those passages is inferred. R58's existing scan records eight near-uniform frames inside inherited material, not joins. S14's accepted label-color finding is preserved unchanged.

**R76 integration limit:** restored source has 217 frames at 1920×1080; select [8,200) for the 192-frame slot at master 774.5–782.5. The selected picture precedes the measured restored-audio reference by 13.9167 ms. Preserve continuous original master narration and normalize review dimensions to the surrounding 1280×720 footage. Its new perceived sync/performance belongs to the separate R76 review.

**Duration/verification limits:** R58 metadata reports video duration 557.333008 despite its 13,376 frame count; use frame trims and reset timestamps rather than rounding container duration. This audit checked source bytes, metadata, event bindings, frame arithmetic, the master WAV header and R58 decoded-audio sample count. It did not repeat full-video decoding, visual seam QC or continuous listening. Root still needs assembled playback/QC after the two recordings. Resolve conform, final finishing and publication are outside this map. EP009 was not inspected or changed.
