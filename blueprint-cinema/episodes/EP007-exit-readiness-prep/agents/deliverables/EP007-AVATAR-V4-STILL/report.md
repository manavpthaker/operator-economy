# EP007 avatar V4 still review

Work order: EP007-AVATAR-V4-STILL. Episode: EP007-exit-readiness-prep. Reviewer: identity/framing reviewer, agent rebecca_reference. Review date: 2026-09-11.

**No blocking visible flaw found in the wider still.** Its identity is visually consistent with the supplied approved portrait; the hands and seated pose are plausible. It provides meaningful room for the proposed closer framing, provided the crop preserves the top of the head.

## Inputs and review method

| Input | Dimensions | SHA-256 |
|---|---|---|
| `blueprint-cinema/experiments/EP007-PRESENTER-001/avatar-v3-lock/media/identity-study.webp` | 2752 × 1536 | `59309d2925b85cfba8a6a411dce1ecea67a03607f8a05933f4a2f6cb6af27754` |
| `blueprint-cinema/experiments/EP007-PRESENTER-001/avatar-v4-wide/media/wide-study-reference.png` | 1672 × 941 | `5c282925447ff8227ea66dcafa60e5b9cf5913aa5cbb565037fb4e0a2d1cbb82` |

Both hashes match the work order. Both images were displayed through `view_image` with original detail requested. The tool displayed the approved portrait at 2048 × 1143 and the wider still at its native 1672 × 941. This is a visual still review in the tool image viewer, not a calibrated color evaluation or a video playback review. No image was edited or cropped.

## Findings

- **Identity consistency:** Face proportions, clear glasses, swept hair, short facial hair, and navy shirt read consistently with the approved portrait. The warm study, shelves, and light from screen-left also remain coherent. This compares the two supplied depictions of Manav; it does not independently authenticate a real person.
- **Hands and pose:** Both forearms rest on the table with plausible wrist connections. Visible fingers, nails, and joint directions are coherent; no obvious extra digit, fused finger, or impossible wrist is visible. Some digits are partly occluded, so this is not a complete anatomical certification. The relaxed resting pose does not itself require correction.
- **Crop room — observation, edit owner:** The wider image adds torso, forearms, both hands, and tabletop. A closer frame can therefore produce a meaningful change in shot size. Hair begins approximately 65 pixels below the top, around 7% of image height. A centered 1.3× crop removes approximately 109 pixels from the top; a centered 1.4× crop removes approximately 134 pixels. Either would cut into the hair. Preserve headroom with an upper-anchored crop. At these scales, the closer shot intentionally excludes the hands/table; it cannot retain the complete wide composition.
- **Resolution — observation, edit owner:** A crop from a native 1920 × 1080 video retains approximately 1477 × 831 pixels at 1.3× or 1371 × 771 at 1.4× before rescaling to 1080p. Final perceived detail must be judged from the generated video and encoded closer shot. The still alone cannot establish that result.

Illustrative geometry only: in the 1672 × 941 still, a 1.3× crop has a 1286 × 724 window; a 1.4× crop has a 1194 × 672 window. A top coordinate near 20 pixels preserves the current hairline in either case. This is a feasibility calculation, not a prescribed runtime crop. Final framing must follow the actual generated output and motion.

## Disposition and limits

Recommendation to the orchestrator: no visible still defect requires another image revision before the already authorized motion test. Preserve the accepted V3 identity. No production approval or state change is claimed.

Unresolved at this stage: temporal face/hands stability, speech synchronization, head movement inside the closer framing, and final crop sharpness. These require the generated clip. No buyer-question cut time was inferred from these images.

The episode-root README, episode.json, and input-lock.json were absent at the expected paths. The supplied work order and its two exact image hashes define this bounded review; broader episode state was not inferred. The deliverable uses the schema-required lowercase work-order ID while preserving the explicitly assigned uppercase output directory.

Only this report and its deliverable manifest were authored. Existing synthetic images were reviewed; no external source, new synthetic generation, provider call, upload, spending, UI change, canonical edit, or approval write occurred.
