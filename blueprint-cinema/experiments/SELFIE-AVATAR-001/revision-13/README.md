# R13 — Full animated question and contact information

Replaces R12's closing screen with the full final spoken question, MP Thaker, mpthaker.xyz and linkedin.com/in/mptxyz. The accepted R11 body remains the base. R12 is retained as history.

`frame.md` owns layout and timing. `index.html` is the HyperFrames composition; `index.motion.json` verifies reveal order, legibility deadlines and in-frame placement. `assemble.py` appends 144 silent frames while retaining all 1322 accepted picture frames and every original audio packet/sample. Total runtime is about 61.1 seconds. There was no specified 60-second cap; the longer text receives 4.5 seconds of settled reading time.

Use `DELIVERY.json` for verified URLs and artifact hashes. MP4s and render screenshots are retained in ignored `../media/revision-13/`. The source-and-QA archive is the render-stage snapshot; final delivery observations and provenance live here.

## Reproduction

In the Higgsfield sandbox, use Node 22 and HyperFrames 0.8.36. Resume the R12 source archive, copy the R13 files and pinned fonts, and probe the existing CLI pin before running checks.

```
hyperframes upgrade --project . --check
hyperframes check --at 0,.2,.5,.8,1.2,1.5,5.95 --json
hyperframes keyframes --selector '#business' --json
hyperframes render --fps 24 --quality high --workers 1 --output closing-r13.mp4
python3 assemble.py accepted-r11.mp4 closing-r13.mp4 full-r13.mp4 ASSEMBLY-QA.json
```

Reserve upload slots before producing media; upload within the producing command with each slot's required Content-Type, then confirm HTTP 200 uploads. The user request authorizes this edit and review render. No avatar or voice generation, publication or global design-system modification is involved.

## Direction and feedback

Owner correction: R12's short question omitted the personal decision asked about in the full script, and lacked contact paths. R13 restores the full question exactly, then offers the requested website and LinkedIn. The sequential reveal follows the reading order; only “business?” has a horizontal Countershift. Atkinson Hyperlegible Next is used for the contact reading text, with Archivo for question and signature. No icons, generic CTA or extra copy were added.

Registry lineage is R12's inspected staggered-fade-up primitive; this revision uses its sequential entrance logic with small vertical offsets and no blur/scale. The owner-locked R11 remains immutable. The new closing is pending owner playback review.
