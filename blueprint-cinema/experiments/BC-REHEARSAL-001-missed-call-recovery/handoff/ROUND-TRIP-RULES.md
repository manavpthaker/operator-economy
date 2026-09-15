# Round-trip change rules

Resolve was not launched for this rehearsal. These rules define how a future conform would return changes without allowing the finishing timeline to silently redesign the sequence.

| Change class | Resolve may do | Blueprint Cinema response |
| --- | --- | --- |
| Finish | grade, legal-range trim, noise reduction, mix, delivery encoding | Record in Resolve change log; no upstream creative change if timing and meaning are untouched. |
| Frame-safe trim | move a cut by at most one frame to conform source seconds to 30-fps record time | Return exact frame delta and affected marker; update the manually assembled event list before declaring conform. |
| Editorial | reorder, remove, extend, shorten, change a transition, change object state, replace a placeholder | Stop conform. Return to visual plan and scene direction; re-lock and rebuild. |
| Evidence | crop source context, change a highlight, omit warning, replace fixture with real evidence | Stop conform. Return to evidence/asset review with provenance and claim checks. |
| Sound | add or replace ambience/SFX, change VO timing, use music | Require exact ticket/provenance and sound-plan revision. Locked narration may not move silently. |
| Upstream | rewrite narration, change engine/world/guardrail/outcome | Stop rehearsal. A new input lock and full dependent invalidation are required. |

No change made in Resolve can approve a Blueprint Cinema gate. A future conform report must list imported hashes, relink results, frame offsets, unsupported items, and every deviation from the animatic reference.
