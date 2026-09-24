# Corrected P08: new performance timing recovery

This is a separate picture correction of the two newly generated, never-locked P08 performances. It does not retime any of the 14 existing presenter performances and does not alter the locked narration. Original provider natives and all failed timing measurements remain in their original locations.

The least-squares affine maps were fitted from matched small.en DTW token anchors, before remeasurement. The imprecise `in` anchor in part A was excluded because it shared a narration timestamp with `hospitality`; that issue was already documented in the original native review. Part A uses 1.2381365767× and part B uses 1.2855837888×, below the authorized maximum of 1.3×. These are constant rates, with no internal speed changes. Every output frame maps explicitly to a nearest original frame in each `EDIT-DECISION.json`; decoded verification checked all 355 derived frames against their declared originals.

The disposable native guide was mapped to the same continuous affine clock solely for diagnosis. Its pitch changes and it must never become final narration. The restoration WAVs are exact copies of the locked master excerpts; final conform explicitly takes audio from the frozen r3 master.

Part A's unchanged three-window drift test returns .04/.02/.01 seconds, spread .03. Part B's unrestricted test initially returned .54/.06/.06, spread .48; this remains preserved. An independent lexical audit showed that .54 aligns different words. A separate, explicitly selected lexical-domain measurement returns −.04/.06/.06, spread .10. The .30-second gate threshold and three narration windows are unchanged. The selection does not certify fine phoneme alignment or grant owner acceptance.

Browser playback ran both candidates to the end at playbackRate1. Full-duration 4fps contact frames and exact frame maps were inspected; no pose jump or teleport was observed. This is sampled review, not continuous human perception. Post-restoration mouth metrics and visual review remain required and any weak flags must be retained.

The two once-only Fal requests reserve $1.9684 total within the existing $3 P08 cap. No native retries or further Higgs generations were requested. The original 162 credits remain spent. The standalone processing helpers do not activate r5 or expose another segment.
