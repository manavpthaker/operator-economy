# R47 context assembly

Prepared wrapper; presenter picture and exact original audio are still required.
No placeholder media or render has been created.

The first 2,212 frames reproduce the accepted R46 context encoded source. At
1:32.166667, cut directly into the exact V5 wide transfer-condition presenter take
for 269 frames. The complete context lasts 2,481 frames / 103.375 seconds at 24 fps.
No new title, crop, transition effect, music, or narration is introduced here.

Required final media, both starting at the same master time 290.291666667:

- `public/media/transfer-criterion.mp4`: aligned picture, 269 frames at 24 fps.
- `public/audio/transfer-criterion.wav`: exact original narration through master
  301.5, 538,000 samples at 48 kHz. Use the picture-range carve, not the longer
  generation audio reference that carries lead-in handles.

After real media is in place, run from this review folder:

```sh
npx hyperframes@latest upgrade --project . --check
npx hyperframes@0.8.36 check --strict --at 0,59.75,71.875,74.75,92.125,92.1666667,96,100,103.3333333 --json > qa/CHECK.json
npx hyperframes@0.8.36 snapshot --at 92.125,92.1666667,96,100,103.3333333 --output qa/stills --describe false
npx hyperframes@0.8.36 render --fps 24 --quality high --output qa/r47-transfer-criterion-context.mp4 > qa/RENDER.log 2>&1
/Users/brownmanbrain/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 qa/check_media.py
```

The read-only version check is required before rendering. A runtime change needs
an explicit record and verification before use; this copied wrapper currently pins
0.8.36. No network or runtime commands were run while preparing the wrapper.

Inspect the rendered join and the presenter at normal playback speed with sound.
The QA script checks frame counts, blank frames, source pin, audio placement and
boundary-picture agreement. It cannot judge lip sync or performance.
