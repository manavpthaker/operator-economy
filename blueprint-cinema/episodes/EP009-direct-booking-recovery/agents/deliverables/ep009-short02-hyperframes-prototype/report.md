# EP009 Short 02 — HyperFrames private-review prototype

**Status:** Complete for private review. No final MP4 was rendered, no approval is claimed, and canonical production state was not changed.

## Result

Built a deterministic 1080 × 1920, 24 fps, 20.5-second HyperFrames composition from the locked r8 carrier. It uses exactly source frames **16619–17110** (source interval `[16619, 17111)`) and the corresponding separate audio from **692.458333–712.958333 seconds**.

The portrait edit avoids a blind center crop. It uses seven exact source partitions:

1. The source question card establishes the machine-versus-operator distinction.
2. The operator and laptop appear together at readable portrait scale.
3. The full Node-RED canvas establishes the workflow.
4. A detail crop isolates the fictional fixture and genuine thank-you draft path.
5. Two synchronized crops show the returned draft and its date/no-send rule.
6. A detail crop shows queue, voice edit, approval, and exclusion gates.
7. Two synchronized crops transfer attention from the returned draft to human review and no-send status as the narration lands on hospitality.

The truth boundary remains visible throughout:

`FICTIONAL FIXTURE · AWAITING HUMAN REVIEW · NO SENDING AVAILABLE`

The caption rail is verbatim and derived only from transcript words **W002001–W002053**. Source video elements are muted; the composition uses one separate audio element at the exact source offset.

## Visual review

I inspected the final nine-frame contact sheet at original resolution:

- **1.8s:** opening question is clear and the first caption is phone-readable.
- **4.7s:** operator face, hands, laptop, and caption are visible together.
- **6.4s:** full Node-RED canvas establishes the real tool before the detail views.
- **8.5s:** the model-to-draft path is enlarged and the caption remains clear.
- **11.0s:** returned-draft language and the queued/no-send state are both visible.
- **13.2s:** queue, voice-edit, approval, and exclusion nodes are legible as the schedule line plays.
- **15.5s:** returned draft and review boundary remain visible during the narration pause.
- **18.2s:** the final human-judgment line is clear while the no-send region is emphasized.
- **20.3s:** the closing frame holds the human-review/no-send state and the final caption cleanly.

Review artifact: `project/review/final-frames-r1/contact-sheet.jpg`

## Verification

- `npx hyperframes lint --json` — **PASS**: 0 errors, 2 warnings.
- `HYPERFRAMES_RUN_ID=ep009-short02-r3 npx hyperframes check --snapshots --at 1.8,4.7,6.4,8.5,11,13.2,15.5,18.2,20.3 --caption-zone "x0=0;y0=.82;x1=1;y1=1;severity=error;seek=.25,.5,.75" --json` — **PASS**.
  - Runtime: 0 errors.
  - Layout: 0 errors, 0 warnings.
  - Motion: 0 errors, 0 warnings.
  - Contrast: 29/29 checked elements passed.
- `npx hyperframes snapshot . --output review/final-frames-r1 --at 1.8,4.7,6.4,8.5,11,13.2,15.5,18.2,20.3 --no-end --describe false` — **PASS**: nine 1080 × 1920 frames and contact sheet created.
- `npx hyperframes keyframes . --json` — **PASS**: timeline/keyframe inventory created.
- HyperFrames animation-map capture — **PASS**: 42/42 tweens captured; output saved at `project/.hyperframes/anim-map/animation-map.json`.
- `project/review/source-contract-verification.json` — **PASS**: all six issued hashes match; frame range, duration, seven-scene continuity, 53-word range, verbatim text, and word-derived timings all match.

The two lint warnings are expected `duplicate_media_discovery_risk` warnings in scenes 05 and 07. Each scene intentionally uses two synchronized crops of the same locked source so both the draft and its human-review/no-send boundary remain readable on a phone. The final contact sheet confirms both views render once, in sync, with no doubled audio.

## Boundaries retained

- No narration was rewritten or reordered.
- No source frame was added, dropped, or retimed.
- No fake interactive state or send action was introduced.
- No paid service or synthetic generation was used.
- No external write, upload, publication, decision-log edit, or canonical-state change occurred.
- No final MP4 was rendered; owner preview approval remains outside this work order.
