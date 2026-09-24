# Week 2 full-05 closing

Adaptation of the Week 3 R13 Counterproof closing, preserving its font assets,
colors, contact block and staggered-fade-up lineage. The longer full question
uses six 56px/64px lines. The final two lines shift right to mark the judgment
about maintenance. All text settles by 1.52 seconds, then holds through seven.

The exact question is “What’s something you’ve deliberately kept doing yourself
because the automation wasn’t worth looking after?” Contact paths are
mpthaker.xyz and linkedin.com/in/mptxyz; signature is MP Thaker. Current Content
OS facts.md verifies both URLs; its design-system/LOCK.md and README.md govern
the personal visual treatment. No source wording or global design rules change.

`frame.md` specifies layout and timing; `index.motion.json` specifies motion
checks. Fonts and GSAP are local, copied unchanged from revision-13. Prior
source files and the accepted full-04 video are pinned in
`reports/PROTECTED-BASELINE.json`.

```sh
npx hyperframes@latest upgrade --project . --check
HYPERFRAMES_RUN_ID=selfie-week2-full05-close npm run check -- --at 0,.2,.5,.8,1.2,1.6,3.5,6.958333333333333 --snapshots --json
HYPERFRAMES_RUN_ID=selfie-week2-full05-close npx --yes hyperframes@0.8.38 snapshot --at .2,.5,.8,1.2,1.6,3.5,6.958333333333333
HYPERFRAMES_RUN_ID=selfie-week2-full05-close npm run render
ffprobe -v error -show_streams -show_format -of json renders/closing.mp4
```

Expected output: `renders/closing.mp4`, 720×1280, 24 fps, 168 frames, seven
seconds, without audio. Root owns packet-copy appending, final audio checks,
hosted review and commit. Worker output remains within full-05/closing and does
not alter the accepted full-04 or Week 3 R13 sources. Owner review remains pending.
