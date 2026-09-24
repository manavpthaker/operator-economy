# Internal pencil-study implementation review

Read-only implementation audit. No approval or production-gate decision.

Inputs: baseline `index.html` SHA-256 `0282f63fd9a14c0095c444af53adc2aaf2121464a7fb4e26dff92c27b2bcbe9d`; study `index.html` SHA-256 `4e177897e2216a5a7688e20f5ef00dcd33b965ba768e2580db991d4e1e8a31af`; `build-pencil-study.mjs` as inspected during this pass.

## Material finding

**Card cross-hatching is painted underneath opaque card fills.** The compiler injects every hatch immediately after its parent opening tag. In `#checklist-card`, `#records-card` and `#written-process`, the subsequent `record-fill` path covers most of that hatching. Owner and customer hatches are unaffected because they have no opaque fill. Insert card hatches after their paper fill, or otherwise place them above that fill while retaining the existing semantic/text layers.

Follow-up: resolved in the generator on reinspection. It now detects the first-child `record-fill` and places the hatch after that fill. The snapshots discussed below were generated before this repair.

## Preservation checks

The inline timeline/script blocks, audio element, visible text elements and all 32 authored transform attributes are byte-identical. All 27 reveal paths retain their original IDs and geometry. No duplicate IDs, NaN, Infinity or undefined output was detected. The timed narration files are byte-identical. No additional timing or semantic-change finding emerged from static inspection.

## Limit

This pass did not assess an encoded frame or playback. Fine-stroke survival, comprehension at small scale and residual contour smoothness require the rendered comparison; static source preservation cannot prove those.

## Snapshot follow-up

Inspected study snapshots at 3.9s, 20.2s and 27.6s, and the baseline at 20.2s. These snapshots predate the card-hatch layering repair. No new blocking shape or legibility finding appeared: the owner and customers remain recognizable, contour breaks are visible, and the record/checklist/package identities survive. The linework is visibly rougher rather than merely recolored.

The meaningful trade-off is reduced visual weight. At 20.2s the oxide action arrow is substantially finer than the baseline, and final package miniatures remain recognizable rather than readable. The arrow is still discernible at the supplied full-size snapshot; preservation after small-scale compression remains unproved. This does not justify reopening timing or layout for the isolated linework comparison.

## Encoded-frame follow-up

Inspected final encoded stills at 0.8, 6.4, 10.7, 14.5, 17.4, 23.6 and 25.8 seconds, plus the 640px-wide 20.2s extraction. No missing object contour, geometry corruption or unexpected whole object appeared. Card hatching now survives its fill, and the strengthened oxide path remains discernible at 640px width. Small labels and final package miniatures remain outside a phone-legibility claim.

**Reveal masks leak short leading marks before their intended cues.** At 0.8s the third checklist box shows part of its X before its 2.08s cue. At 25.8s the still-open row already has a short dash before its 26.47s cue. Baseline round-cap dots are much smaller; the study's white 28px round-capped mask exposes a longer piece of the visible stroke while dash-offset equals the full path length. Use butt caps on the hidden reveal mask or explicitly hide it until its existing draw cue. Keep visible pencil strokes round. This is a mask implementation issue, not a request to change authored timing or semantics.

Regression follow-up: **fixed** in render SHA-256 `f9a5701b9a1fdf96099a4b4f1737b52b23eaaaac6f66f0a335e4f4f47dcfe587`, independently recomputed on disk. Reinspected refreshed encoded frames at 0.8s and 25.8s: all initial checklist boxes are empty, and the still-open row has no premature dash. No remaining finding in those regression frames. This closes the observed mask leak only; it does not record an episode gate or creative approval.
