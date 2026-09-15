# R50 source rebuild

`index.html` was missing after the original R50 build (its verified hash 4edc73e1… is recorded in `r50-records-render-verified-v1`; the original bytes were not recoverable). It was rebuilt from `direction/r50-records/DIRECTION.md`, `CUES.json`, the locked R49 source and frames of the original render.

`qa/r50-records.mp4` and `../r50-records-context/qa/r50-records-context.mp4` are the original, unchanged renders and remain the review artifacts. `qa/rebuild/r50-records.mp4` is the rebuilt source's render. `DIFF-VS-ORIGINAL.json`: final hold mean absolute luma difference 0.25/255 (anti-aliasing and sub-pixel placement); largest difference during the heading crossfade (frame 35, 1.23/255 mean), where easing timing is not exactly reproduced. Strict check passes (`qa/CHECK.rebuild.json`).
