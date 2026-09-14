# Week 2 full-03: repair the For continuation

The owner rejected the remaining join at “For something” in full-02. The closed-mouth settled ending switches to an independently generated open-mouth pose with a different head, neck, collar and blink phase. Similar framing and preserved audio did not make that transition natural.

Full-03 requests one Seedance 2.5 forward video extension from the current opening’s actual first 524 frames. `PREFIX-INPUT.json` binds the video reference, and `NATIVE-REQUEST.json` binds the unchanged closing audio. Keep the existing full-02 opening in the final edit. Inspect whether the provider returns only the extension or a composite before selecting its source range.

The final join must be assessed for motion, pose, mouth-rest-to-speech behavior, gaze, blink, shoulder/collar state and background continuity. Automated timing, pixel differences and matching crops are supporting evidence, not owner acceptance.

`DECISION.json` retains rationale within this isolated experiment. The episode decision helper supports canonical EP### folders only; do not invent a canonical episode identity to log this selfie repair.

Captions remain after review of the complete spoken take. Preserve all prior versions and the full Original C master. This revision does not publish or alter a canonical avatar or episode.

The provider returned the 18-second extension only. Its native audio does not preserve Original C (best waveform correlation 0.043), so one Sync v3 restoration uses the exact final 817,770 approved PCM samples. That output inserted 0.3210625 seconds of audio delay. A straight eight-frame picture trim would start in the middle of a blink. Instead, prepared footage preserves source frame 0, compresses the first 20 preparatory picture frames into 12 output frames, then resumes ordinary speed for source frames [20,417). This yields 409 frames and an eight-frame alignment offset before the main articulation. The first half-second contains low-level breath or possible frication; this is a picture adjustment, and the full Original C soundtrack remains untouched. See `PICTURE-ALIGNMENT.json`.

The prepared pose and blink progression have been inspected by root and an independent reviewer. A slight softness change remains. The full encoded join and final voice clock still require verification before delivery; the owner’s spoken-take verdict remains separate.

Full-03 is now delivered for owner review. The 933-frame encoded export retains the inspected pose and blink progression. All 39 soundtrack windows have zero measured lag, and all encoded audio packets match full-02. The hosted file was verified byte-for-byte and played in the browser through the repaired transition; it is left paused near 20 seconds for review. A small softness change remains. See `DELIVERY.json` and `CONTINUITY-QA.json`; owner review remains pending.
