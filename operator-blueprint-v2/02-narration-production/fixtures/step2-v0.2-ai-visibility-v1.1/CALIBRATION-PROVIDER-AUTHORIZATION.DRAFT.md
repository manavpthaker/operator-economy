# Calibration provider authorization: DRAFT / NOT AUTHORIZED

Authorization ID: `AI-VISIBILITY-v1.1-N4A-DRAFT`

Status: **DRAFT / NOT AUTHORIZED / NO PROVIDER CALL**

Fixture: `step2-v0.2-ai-visibility-v1.1`

Episode: none

Purpose: request a separately approved calibration-only generation after N1 identity verification and N2 owner approval. This document does not authorize that request.

## Proposed bounded scope

- Provider: ElevenLabs
- Model: `eleven_v3`
- Voice ID: `yUXeTfC1IFOCSjGc96sQ`
- Stability: `0.5`
- Similarity boost: `0.6`
- Style: `0.1`
- Preferred format: `pcm_48000`
- Only fallback: `mp3_44100_192`, reason `pcm_capability_unavailable`, under the strict receipt in `VOICE-AND-CAPTURE-LOCK.md`
- Proposed review modes: C01 cold open plus post-sting promise, C02 dense evidence, C03 economics and uncertainty, C04 pronunciation/names/numbers
- Proposed payloads: five exact locked-text payloads because C01 has separate pre-sting and post-sting segments
- Full-script capture: prohibited by this authorization
- Pickup generation: prohibited by this authorization
- Machine capture-plan SHA-256: `abccb4a507734b72ae0693ce44c4497ffc7eff6168730932a15544177375dad4`
- Exact first-pass payload total: 8,155 characters
- Proposed maximum provider calls: 10, allowing at most one strict format fallback for each of five payloads
- Proposed maximum payload characters: 16,310, counting every fallback payload again
- Monetary spend represented by those limits: not inferred or claimed

## Prerequisites before execution

- `package-manifest.json` passes the canonical verifier: complete.
- The canonical extractor reproduces 3,019 tokens and SHA-256 `096329c04c9ce0ce9964e67279657be9fbd488772ae7df8893a28f76083d283a`: complete.
- Canonical passage payloads and hashes are generated from the locked script; no passage is copied from this prose document at execution time: complete in `capture-plan.json` and `dry-run-receipt.json`.
- `PERFORMANCE-DIRECTION.md` receives explicit owner approval.
- The narrator/capture lock remains unchanged.
- The approving owner creates a new active authorization from `provider-authorization.DRAFT.json`,
  confirms the call/character ceilings, records name/date/expiry, and supplies an approval signature
  or equivalent repository record. This draft itself is never edited into silent authority.

## Required receipt per attempted call

- authorization ID and executed authorization hash;
- payload ID, exact payload SHA-256, and locked token interval;
- request time, response time, provider job/request ID, and outcome;
- provider, model, voice ID, and all material settings;
- requested format and observed codec/sample rate/bit depth/channels/bitrate;
- immutable raw path and SHA-256;
- `native_pcm` or `lossy_mp3` origin;
- if lossy, the recorded PCM-unavailability evidence and one-conversion receipt;
- error body with secrets removed when a call fails.

## Approval

- Owner: **blank**
- Authorization date/time: **blank**
- Maximum calls proposed: **10; not approved**
- Maximum characters proposed: **16,310; not approved**
- Maximum spend: **not inferred**
- Status after approval: **must remain blank until explicitly executed**
- Authorization signature/record: **blank**

Committing this draft, possessing a credential, approving N3 configuration, or saying “continue Step 2” does not authorize a provider call. A separate full-capture authorization is required even if calibration later passes.
