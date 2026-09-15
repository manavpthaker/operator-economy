# Context-sensitive film direction — implementation dependency audit

2026-09-08. Read-only wave-0 maintenance audit. All four exact input pins matched. No code, schema, test, policy, prompt packet, episode state or media was changed. Tests were inspected, not executed.

## Bottom line

Add the new narrated-dramatization contract across **schema, semantic validation, both compiler stages and tests together**. Merely adding a mode enum leaves contradictory prompts and no matching audio invariants. Scene context must be authored upstream and explicitly carried into build packets; it must not be inferred from narration by the builder or validator.

## Exact change dependencies

| Dependency | Current behavior and required coordinated change |
| --- | --- |
| Schema version/shape | `scene-directions.schema.json:26` fixes version 1.1.0. Strict `additionalProperties:false` at sequence 140–158, picture contract 306–364, direction facts 536–559 and shot 574–600 rejects new keys. Decide whether scene context belongs to the sequence and shot-choice rationale to each shot before extending those exact definitions. |
| Picture/audio contract | Schema 319–353 enumerates modes, visible-speech rules, coverage grammar and face functions. Conditionals 366–470 constrain their combinations. Add an explicit new mode and its allowed combinations, not a relaxation of `narrated_observation`. Keep `source_delivery`, `sync_delivery` and `presenter_delivery` tied to their existing actual-language roles. |
| Sound coupling | Schema shot conditions 603–777 duplicate picture/audio constraints at `sound_intent`. For a narrator-only dramatization, explicitly retain narration=true and dialogue=none; do not introduce fake synchronized-source status to accommodate pictured interaction. Mirror this in validation.py:834–870 and 937–975. |
| Semantic validation | validation.py:719 first collects schema errors; 831–985 applies explicit mode, speech, mute, face and sound checks. New mode needs a corresponding branch. New authored context/rationale needs existence/type/reference checks where applicable, without automated creative inference. Guard new nested access against malformed types so schema errors remain `ValidationFailure`, not incidental `AttributeError`. |
| Director compiler | scene_prompts.py:111–114 names five modes and applies a blanket narrator-led close-face restriction; 245–247 requests the old contract. Update the mode list and scope restrictions by declared mode. Require the authored scene-context and shot-choice rationale before the shot recipe is returned. |
| Builder compiler | scene_prompts.py:311–330 emits audience inference, visual sentence, the complete shot and selected sequence fields. New shot fields serialize automatically, but a new **sequence-level scene_context would currently be dropped**. Explicitly include it. Rewrite contradictory rules at 342–345 to honor the selected contract without allowing renderer redesign. |
| Provenance | Director source pins currently cover episode artifacts, not compiler/schema files (scene_prompts.py:154–160); build manifest binds scene-directions plus output hashes (364–370). A rule change can alter generated output without changing source artifact hashes. Output hashes detect the difference, but consider a compiler/contract version or hash for diagnosis. The prompt-manifest version 1.0.0 is separate from the scene-direction schema version. |

## Backward compatibility

Recommended boundary: a new **1.2.0 authoring contract** requires context/rationale and permits the new mode; preserve an explicit 1.1.0 compatibility branch for historical validation if that is required. Do not silently populate old context from narration or rewrite historical episode artifacts. If instead all old directions will be invalidated, record that as an intentional breaking migration rather than calling it additive.

The schema loader always reads the named current schema (validation.py:66–74), so a version-aware branch must be explicit in that schema or its dispatch. A changed `const` alone invalidates every old 1.1.0 packet. Conversely, making every new field optional to keep old fixtures green fails to enforce the new authored decision contract.

The existing `_direction_fixture` (test_scene_prompts.py:13–219) constructs a single 1.1.0 system/motion-graphics sequence against current locked words and hashes. Add a current-contract fixture variant while retaining an unmodified legacy fixture test. Do not bulk-edit every fixture to the new version and lose evidence of backward behavior.

## Hidden contradictions and focused regression tests

1. **Mute-test semantics must be settled before coding.** Builder rule 345 currently permits an incomplete mute test only for synchronized speech. That would defeat narrator-carried dramatization even after enum changes. Do not simply flip `missing_line_expected` as a bypass; define what its result means for this mode and test the actual picture-plus-narration contract.
2. **Existing source/sync protections stay.** Keep rejection coverage at tests 497–571. The observation-only dialogue/face tests at 699–769 should continue to reject those cases specifically as `narrated_observation`; rename overly broad test titles if needed, rather than deleting their protections.
3. **Add a full valid-mode matrix row and invalid combinations.** Existing matrix is 309–469. Test the new mode with wrong language carrier, audible dialogue, delivery face functions, absent context/rationale, unknown enums and contradictory completeness declarations. Test schema and semantic agreement.
4. **Do not mistake a mode matrix for contextual realism coverage.** The current matrix only replaces picture/audio and sound fields on a system/motion-graphics fixture (453–456). Add a realistic human-shot fixture for context/rationale tests; otherwise a new test can pass without demonstrating the requested contextual decisions.
5. **Test compiler pass-through and absence of contrary prose.** Extend deterministic director tests 222–261 and build tests 278–306: context and exact authored rationale must survive to build packets, new mode must be named, and no unqualified narrator-led/sync-only prohibition may contradict it. Repeated compilation remains byte-deterministic.
6. **Retain adjacent contracts.** Existing missing-direction-facts, master-reference and continuity tests 574–696, and exact word-cue test 772–791 remain unaffected. New semantic checks should not weaken timing, IDs, evidence, source pins, contiguous coverage or state boundaries (validation.py:719–829 and 987–1169).

`shot.mode` is the separate reality/system/proof/identity/outcome axis (schema:587). The new narrative audio treatment belongs in `picture_audio_contract.mode`, not that visual-mode enum. Policy-specific values and the precise context/rationale field design remain the author's decision; this report does not invent them.

## Review limits

Only the four pinned implementation files were inspected. External fixture providers, CLI callers, templates, authored episode directions and other tests were not audited or executed. The compiler functions shown do not self-validate directions before writing; existing tests validate explicitly before compilation (278–296), so preserve validation-before-build at integration. No claim is made about production readiness or an episode gate.
