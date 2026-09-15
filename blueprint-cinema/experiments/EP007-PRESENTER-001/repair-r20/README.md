# R20: quiet head with the existing facial performance

**Rejected by the owner:** “no that looks crazy like the head is zooming in and out.” S's animated scale introduced a visible size pulse, and its stronger head correction plausibly amplified separation from the preserved body. The numeric motion reduction and sampled-frame reviews below did not establish natural playback. See `../repair-r21/` for the correction with no added scale or rotation.

Owner request: “let's try more subtle head movements. micro expressions not movements.” This extends the correction across the entire two-sentence test. Keep Q's voice, syllable timing, blinks, small facial changes and hand performance while reducing the head's visible travel, in-plane roll and apparent size changes.

Source: `../media/repair-r18/test-q-m-direction-visible-hands-1080p.mp4`, SHA256 `8675571508e53e3f57ecefe42994b71f9b710e7e3603f1ad1c9a454c66574950`. R is a narrower correction of the dip on “straight”; it is preserved. This wider treatment starts from Q to avoid accumulating transformations and encoding generations.

Native Vision tracks Q's eye midpoint, eye-line angle and eye separation for all 140 frames. A smoothed, bounded similarity correction reduces those movements around a stable reference pose. The entire head is transformed together; no facial feature is separately reshaped, no replacement frame is selected, and no expression is generated or held. Small residual motion is retained. This can reduce 2D motion but cannot reconstruct a head at a different 3D pitch or yaw.

The presenter is isolated using local native Vision person mattes. Background restoration uses observed unoccluded Q pixels, with horizontal interpolation from clean pixels for previously hidden fringe. The interpolation reconstructs those pixels; they were not observed directly. The mouth, glasses, ears and hair remain within the rigid transform region. Displacement fades through the neck interior before the hands, while the shoulder outlines stay in their original coordinates. Visible background, lower-body and hand geometry remain in the original frame coordinates.

Mode: `presenter_address`, fixed landscape study shot with exact existing spoken passage, direct lens address, navy shirt and clear glasses, unchanged identity/location/light. Primary action: synchronized speaking with expression carried by eyes, brows and lips. No new provider generation or image edit. Final source audio is bitstream-copied and all frame timestamps are preserved. The final Resolve timeline, locked narration, separate cinematic work and production/release gates remain unchanged.

Review: compare both “straight” and “never” plus the whole clip; require visibly quieter head movement, continuous lips/blinks, natural head-neck connection, stable shelf/wall, clean hair/ear boundaries and no mask shimmer or frozen expression. Numeric stabilization and source preservation do not establish owner preference; playback remains required.

## Current playback file

`../media/repair-r20/edge-cleaned/test-s-micro-expression-steady-head-1080p.mp4`, SHA256 `34f586ba1af370e4391cadbc689d52e0e57e74f55d8967533445308fa931a205`. Picture: 1920×1080, 25fps, 140 frames, 5.600 seconds. Full decode passed; all numeric frame timestamps and the AAC bitstream match Q exactly. See `edge-cleaned-technical-review.json`.

Earlier S passes remain preserved. The first pass reduced head movement but displaced the shoulders and left duplicate outlines. The second pass restricted the correction to the head and neck interior, fixing those shoulder outlines, but retained a faint old-hair fringe where the native matte omitted hair pixels. The current pass expands only the original-image removal support by 3 pixels; the moving foreground alpha, head transform and protected shoulders remain the same. `render-report.json` and `stabilization-config.json` identify this current recipe. Files ending in `first-pass` and `second-pass` preserve earlier recipes and reports.

The second pass measured approximately 75–77% less head-position and in-plane-roll variability than Q across 140 frames, while retaining mouth and eyelid activity. These are measurements of that pass, not a fresh measurement of the current file; the final narrow performance check records whether that evidence transfers. Original 3D head pitch/yaw remains. M remains the historically owner-accepted baseline. S is a local playback candidate, with no owner acceptance or production gate advancement.

The current file passed the narrow visual recheck at frames 0, 15, 100 and 111: the earlier dark hair fringe is reduced, shoulders remain single, and the shelf stays straight. Faint hair-edge and neck-reconstruction traces remain visible at 3x enlargement. This establishes readiness for owner movement review, not final compositing acceptance or full-speed playback approval. See `edge-cleaned-visual-review.json`.

Final performance preservation: all nine matching lossless snapshots have exactly identical inner-face RGB pixels between S2 and the edge-cleaned S3 (including eyes, brows, nose and mouth). With unchanged head processing, S2 metrics are inherited evidence for S3, not a new 140-frame measurement. See `edge-cleaned-performance-preservation-review.json`.
