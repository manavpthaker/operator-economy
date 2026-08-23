# Step 2 Calibration Fixtures

Status: proposed Step 2 v0.2 test space; no production episode or narration approval exists here.

Step 2 should be tested before it is owner-locked. Fixtures use frozen text or explicitly authorized local test audio and remain separate from numbered episode workspaces.

## Current controls

### Positive: AI Visibility v1.1

The Step 1 v1.5 approval authorizes this exact package for Step 2 fixture testing only:

- script SHA-256 `74048b55ed15ed6ed679abb5a6c892def8a8a40e75e7cebeafdfde319dd67efa`;
- clean read-through SHA-256 `544deaeb4324c116fcb5bb7b89e636908d460d63de2bbfd9121155e324979aa6`;
- 3,019 whitespace-delimited `W` tokens; and
- ordered narration-token SHA-256
  `096329c04c9ce0ce9964e67279657be9fbd488772ae7df8893a28f76083d283a`.

It is unpromoted, unnumbered, blocked on production facts, and unauthorized for visual work or
release. Fixture narration may prove only the Step 2 system.

### Historical negative: Workflow Operations

Workflow Operations is expected to fail N1 because it lacks a current Step 1 v1.5 fixture lock and
ready narration handoff. Preserve that failure. Do not repair the old package inside Step 2 or treat
it as a second positive control.

## Minimum acceptance set

### Normal case

The AI Visibility control passes deterministic handoff, direction, N3 freeze, separately authorized
N4A calibration, separately authorized N4B full capture, take review, edit, zero-mismatch
conformity, final-master transcript and pause mapping, `technical_pass`, independent listen, owner
`creative_approved`, and narration lock without changing the `W` sequence.

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

### Source-format failure

A provider response is mislabeled as WAV or returns an unapproved lossy format. Inspection must
detect the actual codec and block. The only fallback is `mp3_44100_192` after native PCM capability
is unavailable, with immutable raw, audible review, one conversion, truthful origin, and no later
lossy intermediate.

### Approval-state failure

Automation attempts to set `creative_approved` after a technical pass. Validation must reject it.
Only the named human owner can grant that state for the exact master hash.

### Legacy-path failure

Any V2 invocation or import of `studio/scripts/originate/generate_vo.py` must block.

## Test boundaries

- Do not call a paid or external voice provider unless the user explicitly authorizes the test and the exact voice.
- Do not create a numbered V2 episode for a fixture.
- Do not treat generated audio, a successful export, or automated validation as creative approval.
- Keep interim ASR diagnostic; derive transcript and pause map from the exact final master.
- Do not commit credentials, private voice samples, or unauthorized cloned-voice material.
- Record expected behavior, observed behavior, reviewer disposition, and remaining weakness for every test.

Step 2 becomes canonical only after the acceptance set is reviewed and the owner explicitly approves a named version.
