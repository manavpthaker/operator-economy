# R64B S19: review candidate

The two headings no longer overlap at “The risk.” The old heading disappears and the new heading appears at the same `C.risk` cue, master 873.76 s / standalone 29.26 s / context 37.26 s. At 24 fps, context frame 894 (37.25 s) is the last old-title frame; frame 895 (37.291667 s) is the first new-title frame. The quote keeps its existing 0.45-second fade, retaining visible content during the change.

The only other visual change is the first line of the final to-do card: the existing secondary ink `#33464C` replaces `#586D74`. The first strict check found that the previous color was 4.35:1 against the card fill and failed the 4.5:1 requirement. Root explicitly authorized this bounded correction. Text, positions, dimensions, scene timing, claims, narration and other animation are preserved. No background adjustment was needed: the encoded output retained the paper color.

## Files to review

- `review.html`: local HTML player for `qa/context.mp4`.
- `qa/context.mp4`: original S18 final 8 s, then corrected S19; 54.5 s / 1308 frames.
- `qa/r64b-s19.mp4`: corrected standalone S19; 46.5 s / 1116 frames.
- `qa/stills/original-title-collision.png`: original context frame 895.
- `qa/stills/title-seam-contact.png`: corrected context frames 893, 894, 895, 896, 897, 900, 905, 906, in reading order.
- `qa/stills/corrected-final-card.png`: final-card legibility check.
- `qa/VERIFICATION.json`: probes, decode, audio, frame scan and unchanged-scene comparisons.
- `PROPOSED-EVENTS.json`: proposed correction and verification only; nothing appended to the episode log.

## Runtime and verification

Started from the original 0.8.36 pin. A read-only check reported 0.8.46 current; strict check on the corrected composition passed on 0.8.46 before the isolated project was upgraded. Five representative PNG snapshots are byte-identical between 0.8.36 and 0.8.46: 9, 18.8, 29.25, 29.291667 and 45.1 seconds. See `qa/runtime-comparison.json`.

The final strict check has zero errors and warnings. Four informational connector-orphan guesses remain: the inspector incorrectly associates the two business-to-you arrows with the hidden quote, and does not resolve the fixed risk arrows to their SVG-use objects. The actual rendered relationships were visually inspected and retained.

Rendered with exactly one local worker on 0.8.46, standard quality, 24 fps; 14.5 s elapsed. Both MP4s are 1280×720 at 24 fps and fully decode. All 1308 context frames have nonuniform picture content. Encoded title seam and final card were visually inspected. The seven unaffected-scene comparisons to the previous encoded render have mean absolute RGB errors of 0.006–0.060 per channel on the 0–255 scale; these are lossy encoding comparisons, not byte identity claims.

Context audio is cut from the locked master at 836.5–891.0 and its PCM is byte-exact. It is encoded as duplicate left/right channels with no −3 dB upmix reduction. Measured left-channel correlation with the master is 0.999887 at zero lag, level delta −0.015 dB. Standalone render correlation is 0.999824, level delta −0.023 dB. Minor differences come from AAC encoding.

## Boundaries

This is an isolated review candidate. S19 has no owner acceptance. The existing R64 project, renders and server remain untouched; inputs were hash-checked after work. The `public` symlink reuses existing assets, pinned in `ASSETS.json`. No paid APIs, canonical state changes, episode-log appends, or server starts/stops occurred. Skill documents were read in place; no global skill update was run because this work order forbids writes outside this deliverable.

The older S19 decision event's `review_seconds` use an undeclared master-minus-3 convention. These proposed events explicitly use the 54.5-second context video's time domain; no historical event was rewritten.
