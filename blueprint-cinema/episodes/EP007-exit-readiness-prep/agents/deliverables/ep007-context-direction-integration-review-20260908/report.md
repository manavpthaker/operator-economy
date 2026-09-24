# Context-direction 1.2.0 — independent integration review

2026-09-08. Wave-0 read-only system review. All nine input hashes matched. Only the two assigned test files were run; both passed, covering 52 collected cases. No episode production gate, creative approval or media quality is established.

## One actionable finding

**[P2 / Major] Malformed dramatization_context escapes controlled validation.**

At `src/blueprint_cinema/validation.py:890–893`, the new branch reads the value with `picture_audio.get("dramatization_context", {})`, then unconditionally calls `.get` on it. An explicit JSON null, list or string is not replaced by the default. The schema error is collected at line 719, but the function continues semantic checks, so these values reach an AttributeError instead of the intended ValidationFailure.

This is a static code-path finding, not an additional executed test. The existing missing-field cases at `tests/test_context_direction.py:153–170` exercise deletion, which returns the safe default {}; they do not exercise wrong types. Guard the new object before dereferencing and add null/list/string cases that require controlled ValidationFailure while leaving the supplied direction unchanged. This failure is fail-closed, not a mode or evidence bypass, but it breaks the validator's diagnostic contract for normal malformed generated JSON.

## What is verified

- **Distinct mode invariants agree.** Schema 383–393 and validator 841–844, 884–904 bind narrated_dramatization to narrator-carried, illustrative interaction, with its own allowed speech/coverage/face functions. Schema 662–673 and validator 962–984 retain narration=true and no added character dialogue.
- **Safety roles stay separate.** Observation retains no-speech and missing-line requirements, including its close-face restriction. Source/sync/presenter delivery cannot be substituted into dramatization. The original source-audio, observation-dialogue, continuity/master-reference and word-timing regressions remain in the passing targeted suite.
- **Context is genuinely authored and preserved.** Scene context and editorial intent are required by schema 602–655. The build compiler includes the exact sequence context at 329–331 and whole shot at 333–335. The regression at context tests 183–198 parses emitted JSON blocks and checks exact equality, not merely field-name presence; repeated outputs remain byte-deterministic.
- **Mute-test behavior is intentional.** Dramatization accepts either diagnostic mute result, but requires an illustrative disclosure plan and actual-audio review check. The four combinations of speech rule/mute result pass at context tests 110–121. Compiler rule 359 now scopes review correctly rather than applying the former universal veto.
- **Legacy behavior is explicitly breaking.** Version 1.1.0 is rejected without mutation by context tests 201–209. The contract at references/SCENE-DIRECTION-CONTRACT.md:143 states deliberate reauthoring and revalidation, not automatic migration or inherited approval. This is consistent, but is not backward-compatible acceptance.
- **New fixture is materially better.** Context tests 32–107 use reality/AI-plate mode, a full-frame footage layer, an owner close-up, a master ticket, continuity, a performance hold, and explicit editorial rationale. It is correctly marked a mechanical fixture, not a production scene or narration-fit verdict. Single-layer compositions are now allowed, which is appropriate for the full-frame plate.

## Regression result and limits

Executed from blueprint-cinema:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest tests/test_scene_prompts.py tests/test_context_direction.py -q --tb=short -p no:cacheprovider
```

Exit 0; all 52 cases passed. Cache and bytecode writes were disabled; tests used their permitted temporary paths.

No further unintended relaxation of narration, source synchronization, evidence, continuity or state boundaries was found in the reviewed changes. This does not prove authored prose is meaningful, an actual clip passes audiovisual review, or uninspected callers enforce every integration prerequisite.

The parent reported a separate full-suite stale EP006 evidence hash against content-os facts. This reviewer did not rerun the full suite, inspect that lock or change it. It remains outside this packet. No fixes were made during review.

