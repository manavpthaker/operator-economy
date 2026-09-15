# EP007 presenter shirt motion R9

The measured shirt motion supports a bounded composite candidate. `tracking.json` contains 765 time-indexed transforms at 25fps relative to source frame 10 (0.4s), plus mapped design-space transforms. Its SHA-256 is `ee1f1dd6e043138ad6009da0e06534e820a6428f20df0f7ccf9983ea36622c01`. This is a motion-analysis packet, not a production or performance approval.

## Measurement

The input is the exact G video, cropped 608×1080 at x656/y0. Four shirt-only rectangles cover left/right upper and lower fabric while excluding face and neck. `track_shirt.py` decodes the entire 765-frame video, downsamples to 304×540, and matches every patch directly to frame 10 using zero-mean normalized cross correlation. It refines translation below a pixel with a parabolic peak fit, then estimates a robust global similarity transform from spatially separated left/right points. Matching directly to the reference avoids accumulated tracking drift.

The first method reached its 36px downward search limit late in the clip. The one correction moved the lower patches upward and expanded the downward search to 72px. `initial-tracking-metrics.json` preserves the initial failure. The corrected run had no rejected frames, no search-boundary failures, and no isolated outliers. Median patch correlations range from 0.959 to 0.986. Median similarity-fit RMS residual is 1.027 source pixels. These are algorithmic confidence criteria, not a probability of correctness or ground-truth tracking.

The released curve uses a symmetric nine-frame Gaussian smoother, sigma two frames, and exact transform composition to rebase frame 10 to identity. No missing-frame interpolation was needed. No bounds were imposed by clipping a noisy trajectory. Apparent shirt motion includes any motion already present in the recording/camera; it is not interpreted as a new physical gesture.

## Transform contract

For source-space coordinates, the pivot is `(304,950)`. Each frame supplies `transform = {x_px,y_px,rotation_deg,scale}`:

`q = pivot + translation + scale * rotation * (p - pivot)`

Positive rotation is clockwise in screen coordinates. Frame 10 is exactly `(0,0,0,1)`.

For the 1672×941 reference design space, use a new wrapper outside the existing `#shirt-clip`. Keep the inner shirt treatment inside it. The initial mapping retained nested `scaleY(1.14)`; the later parent overscan correction below supersedes that inner treatment without changing this packet's motion data. The reference pivot is `(835.3697775919,766.5905659039)`. Source x/y translations multiply by `0.98210188129886555`; rotation and scale are unchanged. Each frame already includes those mapped `reference_space_transform` properties and a CSS matrix alternative. Apply the decomposed transform about the supplied pivot **or** apply its CSS matrix to a top-left origin, never both.

Smoothed source-space ranges:

| Property | Minimum | Maximum |
|---|---:|---:|
| x | −20.519px | 5.531px |
| y | −4.845px | 45.308px |
| rotation | −1.2653° | 1.7712° |
| scale | 0.999836 | 1.028394 |

All times are contiguous from 0 to 30.56s. Maximum adjacent translation is 2.268 source pixels; maximum rotation step is 0.2158°; maximum scale step is 0.002467. The reference identity, finite-value, continuity, and plausible-bound checks pass in `motion-qa.json`.

`media/motion-diagnostic.png` compares raw and smoothed curves. `media/patch-contact-sheet.jpg` shows tracked fabric areas at representative times. No source RGB, audio, face, neck, provider state, or parent file was changed by this worker.

## Static extension treatment

Independent read-only fabric review found that source and reference mean brightness were close, but the generated fabric had much more fine texture. High-pass population standard deviation was 0.78–0.88/255 in source lower-shirt samples and 8.27–10.11/255 in reference outer-shirt samples. The metric uses gamma-encoded weighted RGB, not physical luminance. Exact rectangles and method are in `texture-review.json`.

A native-reference Gaussian blur of 1.6px (about 1.84px at 1920 width) reduced the measured reference texture to 0.95–1.05/255 while retaining broad folds. This is a bounded trial recommendation for the outer-shirt interior only, with the silhouette alpha preserved and masked normalization preventing background bleed. Leave overall exposure unchanged initially; if needed after blur, trial only a local left-side reduction capped around 3/255. Do not alter moving source RGB, face, or neck.

The parent's pre-motion R9 blur candidate reduced snapshot texture contrast about 30% with essentially unchanged mean brightness. It did not appear overblurred. Those independent pre-motion snapshot measurements lack captured hashes and are reported as such, not retroactively bound to later files.

## Current composite finding

The seven post-motion snapshots written at 22:18:55–22:19:01 were reviewed as a contact sheet, with 0s and 23.2s also inspected full-size. Hashes and mtimes are preserved in `snapshot-review-inputs.json`. The samples show no obvious generated face leakage, empty shoulder/collar holes, or reappearing triangular cut corners. Fine temple/ear fringe and some texture mismatch remain.

**Finding resolved in the refreshed 0s still:** the first 0s snapshot exposed a thin horizontal/angled strip around y1065–1079. The parent changed the nested shirt treatment to `translateY(27.28px) scaleY(1.22)` about `(836,941)`. The new mapping preserves reference y600 exactly at y552.26 and extends the base bottom to y968.28. Across all 765 motion frames and the conservative full width x0–1672, the transformed bottom stays below y941; minimum clearance is 4.146 design pixels at frame zero. `overscan-qa.json` records the analytic test.

The refreshed frame zero, mtime 22:21:59 and SHA-256 `a0af23a8f4a9bda0803a9f0f1d3bb25f9a2d822a0bf70ffdcb1500e6d77cae33`, removes the bottom strip with no newly obvious collar/shoulder holes or face leakage. The original historical snapshot hashes remain in `snapshot-review-inputs.json`; they are not claimed to match files subsequently overwritten by the parent. No tracking values changed for this mask correction. A moving composite review and final rendered-video checks remain outside this packet.
