# Short 03 sound-on assembly scaffold v1

This is an unmounted, non-rendered scaffold for retiming the existing Short 03 scene project to the
final Original C master. It does not replace `index.html`, does not alter a scene, and is not a
private-review cut.

## Bound result

- Spoken master: 37.616333 seconds.
- 24 fps spoken-program frame end: 37.625 seconds.
- Visual-only episode route: 37.625–39.625 seconds.
- Picture grammar: presenter 0–8.56, three working screens through 31.05, presenter return
  through 37.625, then the existing two-second route.
- Caption contract: every one of the 98 locked words is accounted for exactly once. Eighty
  words ride the foreground rail; 18 exact words already typeset in the scenes are suppressed from
  the rail and bound to their scene selectors. No word is dropped or rewritten.

## Build and verify

From this project directory:

```bash
node ../caption-assembly-scaffold-v1.mjs sound-on-scaffold-v1/plan.json
node ../caption-assembly-scaffold-v1.mjs sound-on-scaffold-v1/plan.json --check
```

The check fails closed on source-hash drift, active-index drift, locked-script/transcript mismatch,
audio-duration drift, duplicate or dropped caption words, sub-0.5-second cues, and non-contiguous
frame timing.

## Remaining integration work

Do not mount the scaffold yet. The browser-safe muted opening presenter candidate is complete and hash-bound but not
owner-accepted; the return presenter shot is still on hold pending owner retry direction. The two
host overlay variants are built, hash-bound, and unmounted; neither contains the silent animatic’s
static V5 identity plate. After the remaining asset is hash-bound, build a new sound-on index from
`ASSEMBLY-MANIFEST.json`, run the seam gate because VO retiming changes the boundaries, run the full
HyperFrames check, then stop at private Studio/phone review. Rendering and publication remain
separate approvals.
