# R12 — Animated Counterproof closing

Owner accepted R11. The exact body is recorded in `../revision-11/ACCEPTANCE.json`; R12 appends a separate 3.5-second closing card. Full runtime is 58.584 seconds.

The HyperFrames composition is `index.html`; its design and motion intent are in `frame.md` and `index.motion.json`. Source assets are local and pinned. `CHECK.json` passed without warnings. `ASSEMBLY-QA.json` verifies every accepted picture frame, every appended card frame, all original audio bytes/timing/samples and strict final decoding.

Use `DELIVERY.json` for current download URLs and hashes. Local MP4s and visual QA are under `../media/revision-12/`, intentionally outside git. The source-and-QA archive is a render-stage snapshot; this directory also retains subsequent delivery and design decisions.

## Rebuild in Higgsfield sandbox

Use isolated Node 22 and HyperFrames 0.8.36. Create a blank general-video project, then copy these source files and assets. Catalog discovery and adapter choice are in `MOTION-DECISIONS.md`.

```
hyperframes check --at 0,.25,.6,1.0,1.3,3.45 --json
hyperframes keyframes --selector '#business' --json
hyperframes render --fps 24 --quality high --workers 1 --output closing.mp4
python3 assemble.py accepted-r11.mp4 closing.mp4 full.mp4 ASSEMBLY-QA.json
```

Reserve media upload slots before the producing sandbox command. Append uploads with each slot's exact Content-Type header in that same command. Confirm only after HTTP 200. The initial upload lacking Content-Type failed with 403; retrying the same created JPEG with the correct header succeeded. No regeneration occurred.

The sandbox's bundled Node 20 was incompatible. An isolated Node 22 install resolved rendering; the skill updater also needed its isolated npm global lib directory. Skill update then succeeded. No local runtime configuration changed and no external feedback was sent.

This remains a private review experiment. R11 acceptance does not approve R12's new card or publication.
