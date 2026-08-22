# Step 2 Calibration Fixtures

Status: proposed test space; no production episode or narration approval exists here.

Step 2 should be tested before it is owner-locked. Fixtures use frozen text or explicitly authorized local test audio and remain separate from numbered episode workspaces.

## Minimum acceptance set

### Normal case

A fully locked script passes through direction, capture lock, take review, dialogue edit, zero-mismatch conformity, final-master timing, independent listen, and Step 3 handoff without changing the words.

### Lexical-change edge case

A narrator naturally adds, drops, or substitutes a small word. The workflow must detect it after the final edit and require a same-word pickup or Step 1 change request. It must not accept “the meaning is basically the same.”

### Capture-drift edge case

A pickup uses a changed microphone, room, provider model, voice setting, or voice identity. The workflow must return to the voice-and-capture gate and require recalibration rather than hiding the join in processing.

### Post-lock edit failure

The narration master changes after alignment. The workflow must invalidate the transcript, narration lock, and Step 3 timing handoff even when the edit seems minor.

### Script-revision failure

Step 1 issues a new editorial lock. Step 2 must invalidate the old narration lock and prove any take reuse section by section.

### Rights failure

The proposed synthetic or cloned voice lacks documented authorization. The workflow must block before calibration or provider generation.

## Test boundaries

- Do not call a paid or external voice provider unless the user explicitly authorizes the test and the exact voice.
- Do not create a numbered V2 episode for a fixture.
- Do not treat generated audio, a successful export, or automated validation as creative approval.
- Do not commit credentials, private voice samples, or unauthorized cloned-voice material.
- Record expected behavior, observed behavior, reviewer disposition, and remaining weakness for every test.

Step 2 becomes canonical only after the acceptance set is reviewed and the owner explicitly approves a named version.
