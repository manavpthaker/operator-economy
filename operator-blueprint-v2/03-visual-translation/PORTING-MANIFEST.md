# Step 3 Reference Porting Manifest

Status: frozen v0.1 source hashes for the Step 3 design pass.

No V1 or Blueprint Cinema source was moved or edited for this pass. Every source below remains in place and is **referenced rather than copied**. SHA-256 values freeze the exact versions reviewed while designing Step 3.

This follows the same discipline as the Step 0, Step 1 and Step 2 manifests, and `blueprint-cinema/PORTING-POLICY.md`: port proven inputs, validation rules and provenance. Do not port an organizing system that has not survived contact with an episode.

## Frozen sources

### Direction doctrine

| Source | SHA-256 | V2 treatment |
| --- | --- | --- |
| `blueprint-cinema/references/DIRECTION-SYSTEM.md` | `6fd76f377ad880687f9d1b273a465afc2f25767de350cda8b5681f09dfc4af9c` | **Primary port.** Artifacts 1-3 (direction bible, rhythm map, look development) become Step 3 doctrine. Artifacts 4-6 (sequence treatment, shot board, scene directions) are Step 4 and are explicitly out of Step 3 scope. |
| `blueprint-cinema/references/SHOT-GRAMMAR.md` | `7e4ab99bdad7fa58955ea22853820e0a8e5b0e07f9464fac4d1e9c76295be8ac` | **Partial port.** Step 3 selects which causal grammars an episode uses and why. Applying a grammar to a specific shot is Step 4. |
| `blueprint-cinema/references/CREATIVE-REFERENCE-STACK.md` | `f56efc70943bb81077100c746166820a150bf9da7b6819538dd8d4d066e66af4` | Reference-only. Informs the look-development vocabulary. |
| `blueprint-cinema/references/EDITING-NUANCE.md` | `d56f20fea404a90dea5cc9c1b07db66aa285c0e46ec50abb66805083dc290773` | Reference-only. Step 6 material. |
| `blueprint-cinema/references/SCENE-DIRECTION-CONTRACT.md` | `96f071b2d468e3775aff83de71dccafd6e1b660b2191dc48042c04d37eea097e` | Reference-only for Step 3. Step 4 authority. |
| `blueprint-cinema/references/REVIEW-QA.md` | `ece1b22f1a4e69ec5411376ac23c97a92d557284f9a67a263c607cc0f269bd82` | Reference-only. Cross-cutting; informs Step 3 gate conditions without being adopted wholesale. |

### Structure and order

| Source | SHA-256 | V2 treatment |
| --- | --- | --- |
| `blueprint-cinema/WORKFLOW.md` | `be86e9c22217a2c7a1f330beee27f48cb4f563f989b435fa75d1abb73cddb393` | **Production-order evidence.** Its ordering is adopted; see the boundary conflict below. |
| `blueprint-cinema/ARCHITECTURE.md` | `866124a97a1626a6d63ed279638bbd9ba01431dfad7fadbba6c1085636e50ee0` | Reference-only. Authored-versus-generated separation is adopted as a principle. |
| `blueprint-cinema/TOOLCHAIN.md` | `29a2f8d5e1c6489c4a67df6f06c37f96e3ad70d209cd479e1f29ec809b911be2` | **Reference-only and deliberately not adopted by Step 3.** Step 3 is tool-agnostic. See "Toolchain exclusion". |
| `blueprint-cinema/PORTING-POLICY.md` | `f39809e38e09b97d1cf2afc3a048be0dd48d3b893a3c38352854562cf4a3920f` | Method reference for this manifest. |
| `docs/blueprint-cinema.md` | `b6a42a30a370c732495558f66f0971f6f5ff199101a66375fba568230d1a4cee` | Reference-only V1 creative standard. |

### Schemas and worked artifacts

| Source | SHA-256 | V2 treatment |
| --- | --- | --- |
| `blueprint-cinema/schemas/episode-engine.schema.json` | `bb1e484bb08166e553b5a15c2a8b15a521f9e7f5fbf8d003a6796f251b9e8cf1` | **Shape evidence.** A working contract for the engine artifact. |
| `blueprint-cinema/schemas/world.schema.json` | `e9cb273252694b4f29090d0beeeb8e3973954c9a581607ab98236744952eca3d` | Shape evidence for the persistent world. |
| `blueprint-cinema/schemas/visual-plan.schema.json` | `05d2036bb3fd6995f5771110ec305b5d5fdef21076c05ca9947ef2ec6488abd1` | Shape evidence for the full-timeline visual plan. |
| `blueprint-cinema/schemas/scene-directions.schema.json` | `de455d2a30fcbf6553eb3c5efc1da17f1bf718dced62afc19e6279344893da44` | Reference-only. Step 4. |
| `.../EP006-direct-booking-recovery/episode-engine.json` | `73b22204a8a19a9a71d420d6aef69218f717cdab804486175f2929922d4af543` | **Worked example.** Approved 2026-08-20 against a real episode. |
| `.../EP006-direct-booking-recovery/world.json` | `512c8e4ac1b2648ca9d338a8a25ab2e943fc0890d71250a0c975972c2827823e` | **Worked example.** 25 objects, 29 edges, 5 claims, 9 parameters, 5 evidence anchors, 3 cameras, 4 failure routes. |
| `.../EP006-direct-booking-recovery/visual-plan.json` | `1ea1182ec9240d29914666b5b6f8eafc56bd827fd1401f5118c89f4226397407` | **Worked example.** 162 timed units across 915s, each with mode, camera anchor, motion verb, carry/focus objects, and world state before and after. |

## What is ported conceptually

- Visual translation is **direction**, not decoration or implementation.
- The episode needs a mechanically honest **engine** before any coverage is planned.
- A **persistent world** with stable objects and state transitions is what makes motion mean something.
- Motion must express a **business verb**, with a readable before state, operation and after state.
- **Object permanence**: customers, tools, values and evidence stay recognisable while state changes.
- The default transition is a **cut**. A transition is designed only when it explains a relationship.
- Text **labels** components and parameters. It does not reproduce narration.
- **AI renders are never evidence.**
- Authored creative data and generated data are kept separate, and generated code never silently repairs authored creative data.
- Every visual inherits its **evidence label** from upstream. A polished diagram cannot resolve an unknown.

## Boundary conflict, resolved

`blueprint-cinema/WORKFLOW.md` orders production as:

```text
input lock -> episode engine -> persistent world -> full-timeline visual plan
  -> direction bible and rhythm map -> look development -> treatments, boards, scene directions
```

The V2 lifecycle currently assigns **persistent world** to Step 4 preproduction, which places it *after* Step 3. That ordering cannot hold: a direction bible describes how a world should look and feel, so the world must exist first. EP006 validated Blueprint Cinema's order in practice, reaching an approved engine, an approved world and a 162-unit visual plan.

**Resolution: the Blueprint Cinema order is adopted, and `persistent world` moves from Step 4 to Step 3.**

This is recorded as a proposed amendment to the V2 lifecycle table rather than applied silently. See `SCOPE-BOUNDARY.md`.

## Toolchain exclusion

`TOOLCHAIN.md` names HyperFrames canonical for motion and DaVinci Resolve canonical for finishing. **Step 3 does not adopt that decision and does not depend on it.**

Step 3 produces direction that any runtime could execute. The reasons are specific rather than stylistic:

1. Blueprint Cinema's own README records that the toolchain is **specified, not implemented**. HyperFrames appears in sixteen documentation files and zero code files, and is not installed.
2. The v1 Remotion CLI was invalidated by a runtime decision, taking an approved 162-unit visual plan out of production with it. A tool-agnostic Step 3 cannot be invalidated that way.
3. Runtime choice belongs where implementation lives, in Steps 4 through 6.

## What is not ported

- The Blueprint Cinema state machine, CLI, and `renderer/`, which are Remotion-era and deauthorized by their own toolchain document.
- Artifacts 4 through 6 of the direction system, which are Step 4.
- The asset, edit, sound and finishing contracts, which are Steps 5 and 6.
- Any approval or gate status from Blueprint Cinema. **No Blueprint Cinema approval carries into V2.** EP006's `greybox_ready` state is historical evidence, not a V2 gate pass.
