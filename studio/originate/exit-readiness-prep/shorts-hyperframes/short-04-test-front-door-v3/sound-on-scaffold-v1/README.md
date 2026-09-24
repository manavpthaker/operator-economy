# Short 04 sound-on assembly scaffold v1

This is an unmounted, non-rendered scaffold for retiming the existing Short 04 scene project to the
final Original C master. It does not replace `index.html`, does not alter a scene, and is not a
private-review cut.

## Bound result

- Spoken master: 46.114833 seconds.
- 24 fps spoken-program frame end: 46.125 seconds.
- Visual-only episode route: 46.125–48.125 seconds.
- Picture grammar: presenter 0–8.615, four working screens through 38.684083, presenter return
  through 46.125, then the existing two-second route.
- Caption contract: every one of the 126 locked words is accounted for exactly once. One hundred
  one words ride the foreground rail; 25 exact words already typeset in the scenes are suppressed
  from the rail and bound to their scene selectors. No word is dropped or rewritten.

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

Do not mount the scaffold yet. The browser-safe muted return presenter candidate is complete and hash-bound but not
owner-accepted; the opening presenter shot is still on hold pending owner retry direction. The two
host overlay variants are built, hash-bound, and unmounted; neither contains the silent animatic’s
static V5 identity plate. The return panel now occupies y=1040–1290, above the exact caption rail
that begins at approximately y=1418. After the remaining asset is hash-bound, build a new sound-on index from
`ASSEMBLY-MANIFEST.json`, run the seam gate because VO retiming changes the boundaries, run the full
HyperFrames check, then stop at private Studio/phone review. Rendering and publication remain
separate approvals.
