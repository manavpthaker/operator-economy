# R22 private review

The user accepted R21's closeup cuts and requested refinement of choppiness before “one number.” R22 preserves both framing states and the cut at67.916667. The final sentence now uses one uninterrupted video element across62.916667–71.5; a root GSAP timeline applies zero-duration crop changes to an untimed wrapper. It does not activate a second video at source5.0.

The independent audit found only one keyframe in source B, at frame0. R21's second video sought to non-keyframe120 at the emphasis cut. That handoff is a plausible hitch source; it is removed in R22. The narration was already uninterrupted there. This evidence does not prove every perceived articulation issue had the same cause.

## Verified

- R21's20 runtime files remain unchanged. R22 retains19 of those files byte-for-byte; only the root composition differs.
- The 71.5-second,24-fps picture timeline remains contiguous. The B source plays frames[0,206) once. All audio elements and source bytes remain unchanged.
- Strict HyperFrames check passed with zero lint/runtime/layout/contrast findings; contrast5/5. Motion-module checks were disabled and are not claimed.
- Snapshots before and after the cut retain the intended crops and headroom.
- Chrome playback at1x was sampled five times across approximately1:06–1:09, showing changing picture across both crop states with the same active video element. Audio was unmuted. This is sampled visual playback evidence, not dropped-frame telemetry or perceptual lip-sync certification.
- Backward seeking from after the closeup to1:04 correctly restored the earlier crop. Chrome tab1454456746 was marked as deliverable and left paused there.
- All20 staged runtime routes returned HTTP200; source, staging and media-response hashes matched.

The optional keyframes onion-shot diagnostic reported “nothing animates” for the selected wrapper because the authored changes are instantaneous sets; it produced no shot. Do not claim that diagnostic passed. Direct before/after snapshots and forward/backward browser checks verified these discrete states instead. No motion was added merely to satisfy that diagnostic.

Review: http://100.101.49.30:3038/. Original R21 remains at3037. No paid calls, new voice performance, new lip generation, canonical narration changes or publication actions occurred.
