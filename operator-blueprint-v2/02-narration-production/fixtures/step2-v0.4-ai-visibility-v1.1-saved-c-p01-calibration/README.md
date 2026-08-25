# Saved-C P01 directed calibration fixture

Status: credential-free dry run only; provider execution is not authorized.

## Question

Can the owner-selected and separately saved voice `OE Narrator Manav C Base v1`
(`scMbPZwQjr40V1MzL3Nj`) deliver the locked AI Visibility cold open with the existing
ElevenLabs v3 performance transport while retaining the relaxed, natural Manav identity selected
by the owner?

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
library voice with ID `scMbPZwQjr40V1MzL3Nj` from that selected preview. They do not establish
provider-reported voice ownership, original-human source provenance, or permission for this TTS
calibration. The save receipt itself records the provider ownership field as unreported.

Exact byte-for-byte copies are stored under this fixture's `receipts/provenance/` directory because
a future active calibration authorization must bind the selection/save chain by path and SHA-256.
The current draft intentionally does not bind them:

- `../step2-v0.4-ai-visibility-v1.1-eleven-remix/receipts/elevenlabs/AUTH-R2-20260825T102051Z-owner-selection-C.json`
- `../step2-v0.4-ai-visibility-v1.1-eleven-remix/receipts/elevenlabs/AUTH-R2-20260825T102051Z-remix-save.json`

The R2 source-voice rights record is deliberately not treated as TTS permission: it authorizes the
one private library save, explicitly sets directed TTS to false, and requires separate TTS
authorization.

## TTS rights boundary

No calibration-rights receipt exists yet. The zero-authority draft omits all provenance and rights
binding fields rather than using ambiguous `pending` placeholders. Creating a false-valued
rights-shaped record would risk making a non-decision look durable; the exact receipt and complete
saved-remix selection/save/rights binding chain should be created only with a separately
owner-approved active authorization for this request set.

The selection/save records are evidence, not authority. The authorization remains unapproved and
zero-cap until the owner separately approves the exact compiled requests, calibration-only use,
nonzero ceilings, and expiration.

## Files

- `performance-envelope.json` freezes the one provider-neutral P01 passage.
- `passages/P01-S00.locked.txt` is the exact human-readable transport mirror.
- `adapters/elevenlabs-v3.json` binds saved C, v3 settings, and exact P01 tags.
- `adapters/hume-octave-1.json` is an inert schema-required entry; no Hume action is planned.
- `provider-bakeoff-plan.json` is a credential-free two-take plan.
- `compiled/provider-bakeoff-dry-run.json` is deterministic request evidence, not authorization.
- `authorizations/01-elevenlabs-saved-c-p01-calibration.DRAFT.json` records the proposed request
  scope and explicit blockers, but no provenance/rights bindings or execution authority.
- `RESULTS.md` is the state and eventual owner decision surface.
