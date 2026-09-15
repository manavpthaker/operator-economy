# Blueprint Cinema Migration

## Decision

Blueprint Cinema supersedes the screen-by-screen storyboard as OE's visual organizing system. HyperFrames supersedes Remotion as Blueprint Cinema's new-motion and directed-animatic runtime. DaVinci Resolve becomes the canonical final editorial and finishing environment. Existing work remains available as project history and source material, but it does not define a new episode.

This document specifies the target. The current v1 CLI, schemas, state names, tests, and isolated renderer still contain Remotion-era greybox behavior. They remain implementation history until a separate runtime migration is built and validated. Documentation is not implementation.

## Keep

- The locked EP006 script, final VO, word-level transcript, and their hashes.
- Research, citations, evidence originals, interface captures, approved footage, and provenance records.
- OE color, typography, and logo tokens.
- Claim, rights, synthetic-media, caption, audio, and release gates.
- The isolated Remotion source and review renders as reproducible historical prototypes.
- Useful runtime lessons from the isolated HyperFrames experiment, without importing its finished composition.
- Resolve projects and pilots as historical evidence, never as a new source of visual authority.

## Supersede

- `storyboard.json` as the authoritative visual plan.
- One Remotion `Sequence` or scene template per narration beat.
- Generic layout routing by `asset_type` or narration text.
- Full-screen title/statistic/list cards as the default editorial unit.
- `coverage_approved` for the current 141-beat map. The timestamps remain useful, but its visual decisions are invalidated.
- Existing EP006 opening, Resolve, and full-episode renders. They are prototypes, not candidates for incremental repair.
- Remotion as the authorized implementation target for new Blueprint Cinema scenes.
- A vague whole-episode greybox that proves only timing or navigation.
- Resolve as an optional afterthought or an undocumented alternate edit.

Nothing is deleted during migration. Superseded artifacts remain reproducible until the replacement directed animatic, conform, and delivery path pass.

## New Authority Chain

1. `docs/blueprint-cinema.md`
2. `blueprint-cinema/TOOLCHAIN.md` and `blueprint-cinema/PRODUCTION-TEAM.md`
3. Locked script, VO, word timing, and input hashes
4. Episode engine, persistent world, and full-timeline visual plan
5. Direction bible, rhythm map, approved style frames, and representative motion test
6. Sequence treatments, shot boards, and validated scene directions
7. Asset tickets, manifests, candidate records, and approved selects
8. HyperFrames project, directed animatic, graphic plates, and render manifest
9. Resolve edit manifest, conformed timeline, picture lock, finish, and delivery reports
10. Existing packaging, upload, `links.json`, and content-os release gates

## EP006 Restart Gates

1. Approve the episode engine and reality-world bible.
2. Convert the exact VO transcript into narrative states and persistent sequences.
3. Approve an episode direction bible, rhythm map, look development, and representative motion test.
4. Direct the exact shots, real text, evidence choreography, motion, camera, sound intent, and handoffs.
5. Build a full 15:15 directed animatic in HyperFrames without polished assets.
6. Review the complete film for comprehension, rhythm, continuity, cognitive load, and causal clarity.
7. Create exact asset tickets and select records from the approved animatic.
8. Produce HyperFrames scenes and plates; conform approved media and plates in Resolve.
9. Approve rough cut, picture lock, color, sound, captions, online, and delivery separately.

The first new visual review is the episode visual language and representative motion test. The first full-timeline review is the directed animatic—not a polished intro. This prevents both the opening and the runtime from becoming disconnected design experiments.
