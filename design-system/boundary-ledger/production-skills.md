# Boundary Ledger production-skill authority

Status: **application instructions updated on 2026-09-10**; semantic core and provisional motion/sound status unchanged.

Boundary Ledger remains the semantic design authority. The OE production skills are the locked
instructions for applying that authority to illustrations, scenes, generated plates, motion
graphics, and audio-led clips. They do not add a semantic role or operation, change evidence, choose
a runtime, or authorize publication.

## Required load order

For a new or revised directing decision, begin with
[`oe-video-direction`](../../.agents/skills/oe-video-direction/SKILL.md). It establishes the viewer
change, compares forms, retrieves conditional precedents and retains the episode's decisions and
outcomes. It does not choose new semantics or replace the authority order below.

1. [`oe-boundary-ledger`](../../.agents/skills/oe-boundary-ledger/SKILL.md) routes the production
   surface to the applicable Boundary Ledger core, invariant, illustration, motion, scene, and audio
   contracts.
2. [`oe-film-direction`](../../.agents/skills/oe-film-direction/SKILL.md) governs picture/audio mode,
   scene context, shot purpose, context-selected coverage/editing, generated-plate continuity,
   visible speech, and mode-specific audiovisual review.
3. Blueprint Cinema binds those rules to an episode and its approved evidence.
4. HyperFrames and Resolve implement and finish the approved direction; neither may invent meaning.

The Working Model remains the locked rough language: short overlapping pencil strokes, broken
outlines, open corners, imperfect parallels, correction marks, uneven proportions, variable
pressure, and selective cross-hatching. Roughness is authored into the marks, never added as a
uniform wobble or paper effect.

## Narrated-scene rule

Read the scene context before selecting its form, picture/audio mode, coverage, and cut/hold
motivation. Narration alone does not select observational grammar. `narrated_observation` keeps its
non-speaking action and missing-line constraints. Explicit `narrated_dramatization` may show
illustrative interaction, reciprocal eyelines, and attempted answers when narration supplies
essential meaning; it requires disclosure and actual-audio comprehension review. Mute viewing is
diagnostic in that mode. Dialogue, presenter address, natural-sound observation, and silent graphics
keep their separate contracts. Exact source, character, and presenter delivery stays synchronized
to its approved audible track. No fixed setup count or cutting interval is imposed.

The runtime-neutral binding is in [`scene-contracts.md`](./scene-contracts.md). The full direction
record and allowed mode behavior are in
[`picture-audio-modes.md`](../../.agents/skills/oe-film-direction/references/picture-audio-modes.md).

## Reference boundary

The film references are pinned, attributed inputs—not OE authority. Their selected principles and
explicit exclusions live in
[`source-ledger.json`](../../.agents/skills/oe-film-direction/references/source-ledger.json). No
external toolchain, dramatic formula, or dialogue-first default is adopted by reference alone.

The exact local production files are bound by
[`oe-skills-lock.json`](../../.agents/oe-skills-lock.json). Boundary Ledger's manifest pins that lock
by SHA-256, and the Boundary Ledger validator verifies the lock, every declared local file, complete
lock coverage, and the source-ledger declaration without invoking an external checkout or tool.

This lock does not promote the motion or sound implementation bindings. They remain provisional
until separately encoded, mixed, and verified in their delivery media.
