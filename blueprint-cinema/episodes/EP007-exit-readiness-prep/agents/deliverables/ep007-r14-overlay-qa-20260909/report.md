# R14 opening-overlay regression QA

2026-09-09 · Independent reviewer r11_avatar_qa · Read-only source and declaration comparison after the orchestrator's ready message.

## Result

Static regression checks pass. R14 preserves all R13 picture cuts, source ranges, media bytes, audio placements, existing subcompositions, and root styling. The only added picture layer is the bounded opening bridge.

| Reviewed artifact | SHA-256 |
|---|---|
| Pinned R13 index.html | 8e814b137d6ff1696050834e216bfdf880a0c22f75674040325f3a6876944da5 |
| R14 index.html at comparison | d865e89c15c10bd5eab47affe4146ea2d9e968101b808e4ea89b7fee260d01b4 |
| R14 compositions/opening-bridge.html | f42749141292f44c7e9cdd54fba4eabab9117ed4db01f815d24e943434fc7392 |

## Checks

- The complete attributes of all 13 track-1 picture declarations and both audio declarations are identical. Only editor data-hf-id attributes were excluded from this comparison.
- All 19 files under public/media, public/audio, public/fonts and public/vendor match byte-for-byte: nine media files, two audio files, seven fonts and one GSAP file.
- All five pre-existing subcompositions match byte-for-byte: question, handoff, sting, title and the retained unused arithmetic file.
- Root dimensions, CSS, media crop treatment, duration, frame rate, audio volume and split-source timing are unchanged. The root diff contains only the review title/identity/timeline-key rename and the new overlay host.
- Duration stays 56.5 seconds. The narration split remains review [0,45) from source [0,45), then review [45,56.5) from source [48,59.5).

## Overlay boundary

The one new host uses track 10 from review 2.5 to 7.666666667 seconds. Its child contains only the two new labels, scoped styles and a paused GSAP timeline; it adds no media or sound.

| Event | Review time |
|---|---:|
| “25 years.” begins its fade in | 2.500000 |
| Tenure label fully visible | 2.708333 |
| Accepted avatar-to-film cut, with tenure label held at fixed coordinates | 4.041667 |
| “Profitable.” begins its fade in | 6.375000 |
| Profit label fully visible | 6.541667 |
| Whole-label exit fade begins | 7.541667 |
| Overlay fully cleared and host ends | 7.666667 |
| Accepted owner close-up begins | 7.708333 |

The overlay is held across the first cut and cleared one 24 fps frame before the close-up. No later scene gains an overlay host. The rest of the frame remains transparent outside the label boxes.

## Limits

This is source-level regression evidence, not playback or final-render approval. It does not establish phoneme sync, runtime proxy behavior, actual opacity/seek behavior, visual legibility, subject occlusion, or encoded-pixel equivalence. Those checks remain with the orchestrator's strict check and pixel review. No source, experiment, provider or production-state changes were made.

Reproduction: run the packet's compare.py with the Blueprint Cinema Python environment. It verifies the baseline pin, compares all primary declarations, streams SHA-256 over every public and composition file, and prints the complete comparison. A direct diff -u additionally checked the root changes. No finding requires an unrequested revision.
