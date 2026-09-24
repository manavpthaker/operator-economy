# Saved-C P01 directed calibration fixture

Status: bounded calibration technically passed, but the owner rejected both candidates as flat,
with no inflection or emotion. No candidate is selected. The tested calibration method is a
creative `FAIL / REVISE`; full-episode capture, Step 2 lock, Step 3, sharing, and publication
remain unauthorized.

## Question

Can the owner-selected and separately saved voice `OE Narrator Manav C Base v1`
(`scMbPZwQjr40V1MzL3Nj`) deliver the locked AI Visibility cold open with the existing
ElevenLabs v3 performance transport while retaining the relaxed, natural Manav identity selected
by the owner?

For this exact two-take calibration, no. The owner rejected both nominated `.v2.wav` candidates
because both were flat and lacked inflection and emotion. That fails the tested performance method;
it does not, by itself, establish that the Saved-C voice asset cannot work under a materially
different method.

This fixture does not compare voice-remix candidates. It does not reopen the script, create or
mutate a voice, authorize a retry, generate a full episode, lock Step 2, authorize Step 3, or
authorize publication.

## Exact scope

- Canonical spoken identity: 3,019-token `oe-spoken-text-v1`, SHA-256
  `096329c04c9ce0ce9964e67279657be9fbd488772ae7df8893a28f76083d283a`.
- Passage: exact `P01-S00`, canonical W `[0,139)`, 139 tokens, 792 plain transport characters.
- Performance transport: the existing P01 paragraph/thought structure and exact tags at tokens
  `0`, `37`, `78`, and `135`.
- Voice/model/settings: saved C; `eleven_v3`; stability `0.5`, similarity `0.6`, style `0.1`.
- Variance: two same-direction generations with fixed seeds `2026082401` and `2026082402`.
- Primary ceiling: two `pcm_48000` calls, 1,684 characters, two outputs.
- Absolute ceiling: four calls and 3,368 characters only if each primary receives an explicit,
  documented PCM-capability rejection and uses the sole `mp3_44100_192` fallback.
- Any lossy fallback is comparison-ineligible.

## Selection and save evidence

The R2 records establish that the owner selected preview C and that ElevenLabs created a separate
library voice with ID `scMbPZwQjr40V1MzL3Nj` from that selected preview. The exact calibration
rights receipt records Manav Thaker as voice owner and consent owner and permits only the bounded
P01 TTS calibration that has now been consumed. The save receipt's provider ownership field remains
unreported; owner consent, not a provider metadata inference, is the authority used here.

Exact byte-for-byte copies are stored under this fixture's `receipts/provenance/` directory. The
consumed active calibration authorization binds the selection/save chain by path and SHA-256:

- `../step2-v0.4-ai-visibility-v1.1-eleven-remix/receipts/elevenlabs/AUTH-R2-20260825T102051Z-owner-selection-C.json`
- `../step2-v0.4-ai-visibility-v1.1-eleven-remix/receipts/elevenlabs/AUTH-R2-20260825T102051Z-remix-save.json`

The R2 source-voice rights record was not reused as TTS permission. A new calibration-specific
rights receipt and a new 24-hour active authorization supplied that authority.

## TTS rights and execution boundary

The owner approved the exact compiled request set, two native-PCM primary calls, the bounded
capability-only fallback ceiling, and a 24-hour calibration-only window. The active authorization
was consumed before the first network request. Execution used two calls, 1,684 transport
characters, and two native PCM outputs; it used no fallback, retry, redirect, Remix, save, or voice
mutation.

That authority is exhausted. The result permits local QA and private owner audition only. It is not
reusable for another calibration, a pickup, long-form confirmation, or full-episode capture.

The first local WAV wrappers were malformed because FFmpeg wrote an unseekable pipe header. They
are retained only as failed evidence and are excluded by an immutable disposition. The raw PCM was
intact, and the corrected `.v2.wav` pair was produced locally without another provider call. Only
that pair was eligible for owner review. The owner has now rejected both nominated candidates on
creative grounds. Both are ineligible for advancement; candidate B's recorded lexical uncertainty
also remains unresolved.

## Files

- `performance-envelope.json` freezes the one provider-neutral P01 passage.
- `passages/P01-S00.locked.txt` is the exact human-readable transport mirror.
- `adapters/elevenlabs-v3.json` binds saved C, v3 settings, and exact P01 tags.
- `adapters/hume-octave-1.json` is an inert schema-required entry; no Hume action is planned.
- `provider-bakeoff-plan.json` is a credential-free two-take plan.
- `compiled/provider-bakeoff-dry-run.json` is deterministic request evidence, not authorization.
- `authorizations/01-elevenlabs-saved-c-p01-calibration.DRAFT.json` records the proposed request
  scope and explicit blockers, but no provenance/rights bindings or execution authority.
- `authorizations/02-elevenlabs-saved-c-p01-calibration.ACTIVE.20260825T145935Z.json` is the exact
  consumed 24-hour authority; `authorizations/consumed/` proves one-shot consumption.
- `receipts/elevenlabs/AUTH-SC-P01-ai-visibility-v1.1-calibration-20260825T145935Z-directed-bakeoff-run.json`
  records the two native-PCM provider results.
- `receipts/elevenlabs/AUTH-SC-P01-20260825T145935Z-invalid-pipe-wav-disposition.json` excludes the
  two malformed first wrappers and nominates only the corrected `.v2.wav` pair.
- `reviews/SAVED-C-P01-TECHNICAL-AND-LEXICAL-QA.md` records technical and offline lexical evidence
  plus candidate B's unresolved exact-word gate.
- `reviews/SAVED-C-P01-OWNER-CREATIVE-DISPOSITION.md` records the owner's rejection of both
  candidates and the resulting creative `FAIL / REVISE` boundary.
- `RESULTS.md` is the current terminal state for this bounded calibration.
