# N4A calibration provider authorization: AI Visibility v1.1 fixture

Status: **ACTIVE FOR ONE BOUNDED CALIBRATION BATCH UNTIL CONSUMED OR EXPIRED**

Authorization ID: `AI-VISIBILITY-v1.1-N4A-20260823T200928Z`

Authorized by: Manav Thaker

Authorized at: `2026-08-23T20:09:28Z` (`2026-08-23 16:09:28 EDT`)

Expires at: `2026-08-24T20:09:28Z` (`2026-08-24 16:09:28 EDT`)

Authorization window: exactly 24 hours. Consumption before expiry ends the authorization.

## Frozen inputs

- Target: fixture `step2-v0.2-ai-visibility-v1.1`
- N2 owner approval: `N2-OWNER-PERFORMANCE-APPROVAL.md`
- N2 performance-direction SHA-256: `cb99b6dd120acab205e2eec7eadbc40e11b7a75e6f226b3f0723110d690e67db`
- N3 voice-and-capture-lock SHA-256: `27a4ccfc440ecfc17d941ff5c4805b4a25d3d087dccd68b6114d87df2b3ce1de`
- Capture-plan SHA-256: `abccb4a507734b72ae0693ce44c4497ffc7eff6168730932a15544177375dad4`
- Step 1 script SHA-256: `74048b55ed15ed6ed679abb5a6c892def8a8a40e75e7cebeafdfde319dd67efa`
- Canonical spoken-sequence SHA-256: `096329c04c9ce0ce9964e67279657be9fbd488772ae7df8893a28f76083d283a`
- Machine authorization: `provider-authorization.N4A-20260823T200928Z.json`

## Authorized provider envelope

- Provider: ElevenLabs
- Model: `eleven_v3`
- Existing OE voice ID: `yUXeTfC1IFOCSjGc96sQ`
- Voice creation or cloning: not authorized
- Payloads: exactly the five token-bounded parts in the frozen capture plan
- First-pass payload characters: 8,155
- Maximum provider calls: 10
- Maximum attempted payload characters: 16,310
- Preferred output: `pcm_48000`
- Only permitted fallback: `mp3_44100_192`
- Fallback trigger: a documented, explicit, non-retryable provider response stating that PCM or the
  requested PCM output format is unavailable
- Any transport, timeout, authentication, rate-limit, or server failure: stop; MP3 fallback is not
  authorized
- Raw provider bytes: immutable
- Spoken-word rewrite, addition, deletion, reorder, or substitution: prohibited

## Authorization boundary

This record authorizes one calibration batch only. It excludes full capture, pickups, regeneration
after consumption, mastering, Step 2 lock, Step 3, publication, and release. The resulting audio
must pass technical review and a separate owner listen before N4A can pass.

## Owner authorization wording

> I approve the AI Visibility v1.1 N2 performance direction and authorize the N4A calibration only for the next 24 hours: ElevenLabs eleven_v3, existing OE voice, five payloads, maximum 10 provider calls and 16,310 characters, PCM first, with 192 kbps MP3 permitted only after a documented PCM-capability failure.
