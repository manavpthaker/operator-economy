# R29 seller cutaway boundary audit

The reported blank screen is explained by a source timing mismatch. The calmer seller cutaway lasts 3.5 seconds, but the animation remains hidden for the former 5.25-second cutaway. This leaves **1.75 seconds (42 frames at 24 fps)** without either visible source.

This is an independent source-logic audit. No runtime, image, playback, or audio verification was performed by this reviewer. The orchestrator owns the edit and visual verification.

## Pinned inputs

- `hyperframes/reviews/r29-neutral-seller/index.html`: `3b386dfe0b5bc7cdd4224e0992e9042500c137302320d95bb52456b6ae5e5742`
- `hyperframes/reviews/r29-neutral-seller/compositions/market.html`, before the fix: `8191c2e269ab2490aee6779d331a0af6ff1f706120ea0cd7cafca78bd820f1bd`

Both hashes matched on inspection. Paths are relative to `blueprint-cinema/experiments/EP007-NET-NEW-UNFINISHED-ANSWER-003/`.

## Cause and proposed minimal correction

The seller starts at review 94.3333333333 and ends at 97.8333333333. The market host starts at 71.5. Its root is hidden at local 22.8333333333, corresponding to the seller's start, but restored only at local 28.0833333333, or review 99.5833333333.

Change only that restore cue to **local 26.3333333333**. This corresponds to review **97.8333333333**, exactly the new seller cutaway endpoint to the written precision. Do not lengthen the calmer take, change narration, or alter the accepted later cuts to conceal the mismatch.

At 24 fps, the intended boundary is frame 2348. Frame 2347 (97.7916666667) belongs to the seller; frame 2348 (97.8333333333) belongs to the restored animation. The old incorrect return was frame 2390.

## Neighboring boundaries

| Boundary | Source ending | Source beginning | Finding |
| --- | --- | --- | --- |
| 94.3333333333 | Market becomes hidden | Seller cutaway | Aligned |
| 97.8333333333 | Seller cutaway | Market restored after proposed correction | Aligned by proposed one-cue change |
| 131.0 | Market host: 71.5 + 59.5 | Presenter question host | Aligned |
| 143.0416666667 | Presenter moving video: 131 + 12.0416666667 | Last-frame hold | Aligned |
| 143.7916666667 | Presenter hold and host end | Gap host | Aligned |

The presenter and gap roots both become opaque at local zero. The presenter has 12.0416666667 seconds of moving media followed by a 0.75-second hold, covering its 12.7916666667-second host. The gap covers the remaining preview through 157.5. No analogous source interval hole was found at these neighboring cuts.

## Minimal regression assertion

Derive endpoints from the current markup and the two market hide/restore cues. Assert with a small numerical tolerance that:

1. `market_start + market_hide == seller_start`.
2. `market_start + market_restore == seller_start + seller_duration`.
3. `market_start + market_duration == presenter_start`.
4. Presenter video end equals hold start; hold end equals presenter host end; presenter host end equals gap start.

For visible-source coverage, inspect one frame before, exactly on, and one frame after each of those boundaries, using frame-index-normalized timing to avoid treating rounded decimal thirds as real gaps. Coverage must mean an active source whose root is visible, not merely an active host. A host-duration-only assertion would miss this defect.

The source calculation passed for the proposed correction at frames 2263/2264, 2347/2348, 2389/2390, 3143/3144, 3432/3433, and 3450/3451. This calculation is not a substitute for checking the actual rendered seller-to-animation seam. Inspecting 97.79, 97.83, and 97.88 seconds, followed by continuous playback across the seam, is sufficient focused visual follow-up.

## Scope and status

No source, media, approval, canonical episode state, or runtime files were edited. No external sources, generated media, provider calls, or paid services were used. This report does not approve the corrected performance or advance an episode gate. The orchestrator should confirm the implemented file and live served preview before reporting the blank interval fixed.
