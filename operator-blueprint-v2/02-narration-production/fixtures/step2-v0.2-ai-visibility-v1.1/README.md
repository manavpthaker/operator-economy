# Step 2 v0.2 fixture: AI Visibility v1.1

Status: N1 passed. N2 owner direction is approved. N3 configuration is frozen. The one authorized
N4A calibration batch completed on native PCM and is ready for owner listening. N4A remains pending.

This fixture tests the Step 2 narration controls against the exact AI Visibility v1.1 package locked at Operator Blueprint V2 Step 1 commit `27c90fd628fe3972fea556c1d9ed189f1b657867`.

It is not an episode. It has no episode number, does not clear the live Content OS facts gate, grants no public-production authority, and cannot enter Step 3.

## Package

| File | Purpose | Current state |
| --- | --- | --- |
| `package-manifest.json` | Hash-bound Step 1 and live-authority inputs | 16 sources verified; fixture-only boundary explicit |
| `identity/` | Canonical W and portable identity receipt | generated twice identically; N1 identity passes |
| `N1-EDITORIAL-HANDOFF-CHECKLIST.md` | Human-readable N1 receipt | **N1 PASS** |
| `PERFORMANCE-DIRECTION.md` | Nonlexical episode performance map | frozen preapproval input; approved separately at N2 |
| `N2-OWNER-PERFORMANCE-APPROVAL.md` | Owner decision bound to the frozen direction | **N2 PASS for bounded N4A calibration only** |
| `VOICE-AND-CAPTURE-LOCK.md` | Existing OE narrator and PCM-first capture freeze | configuration frozen; no further call authorized |
| `CALIBRATION-PLAN.md` | Four calibration modes using exact locked words | executed as five payloads |
| `capture-plan.json` | Five exact machine payloads across four review modes | validates; PCM-first dry run passes |
| `dry-run-receipt.json` | Credential-free request-envelope receipt | `network_called: false` |
| `CALIBRATION-PROVIDER-AUTHORIZATION.DRAFT.md` | Separate external-call gate | **DRAFT / NOT AUTHORIZED** |
| `provider-authorization.DRAFT.json` | Hash-bound machine authorization draft | fail-closed; cannot execute |
| `N4A-PROVIDER-AUTHORIZATION.md` | Human-readable bounded call authority | consumed by the completed calibration batch |
| `provider-authorization.N4A-20260823T200928Z.json` | Exact machine call authority | consumed; cannot be reused |
| `N4A-AUTHORIZATION-CONSUMED.md` | Human-readable current authorization state | **CONSUMED / NO REPLAY AUTHORITY** |
| `calibration/20260823T200928Z/` | Immutable raw PCM, lossless working WAVs, and receipts | five native-PCM takes; no fallback |
| `N4A-CALIBRATION-TECHNICAL-REVIEW.md` | Machine and format review | technical preflight passes; owner listen pending |

The positive hosted-voice review is the fixture's lock-bound editorial-voice conformity record. Step 2 may perform those words; it may not rewrite them.

## Locked spoken identity

- Schema: `oe-spoken-text-v1`
- Narration blocks: 12 (`S00`, `S02` through `S12`; `S01` is silent)
- Spoken tokens: 3,019
- Ordered-token SHA-256: `096329c04c9ce0ce9964e67279657be9fbd488772ae7df8893a28f76083d283a`

The v0.2 runtime verified all 16 sources, reproduced this identity in two byte-identical runs, and
generated `identity/canonical-w.txt` plus `identity/spoken-identity.json`. The canonical W hash is the
ordered-token hash above. The portable identity-receipt SHA-256 is
`d6e40df20bb70365790179cb48434a8b89993d85de72dc7eb497f5ee36848beb`.

The five-payload calibration plan validates at SHA-256
`abccb4a507734b72ae0693ce44c4497ffc7eff6168730932a15544177375dad4`. Its dry run covers 8,155
exact payload characters, requests `pcm_48000`, records every text/body hash, and makes no network
call. The dry-run receipt SHA-256 is
`79488760f1941d684b3884bcc0d7f02c3ffddda01bcac5f271b889da68edd46e`.

The owner later approved N2 and one N4A calibration batch. That authorization was consumed on
2026-08-23. The batch used five calls and 8,155 characters. Every response was native
`pcm_48000`; the MP3 exception was not used. The acquisition receipt SHA-256 is
`784140a2f68b287df1b01ce7ff9dadf5588788b5f0d1701d41e77ed9b19ad4a5`. The generated audio is
technically ready for the owner listen, but `creative_approved` remains false and N4A remains
pending.

## Audio-source rule

Request `pcm_48000` first. If the provider/model/account cannot supply it, the only allowed fallback is `mp3_44100_192`, with reason `pcm_capability_unavailable` and the strict receipt in `VOICE-AND-CAPTURE-LOCK.md`.

The raw provider response remains immutable. A fallback MP3 is decoded and resampled exactly once into a 48 kHz, 24-bit, mono PCM working WAV. Every later intermediate stays lossless. The resulting WAV must remain labeled as derived from a lossy source; it is never native PCM acquisition.

## Stop conditions

- Any source-hash mismatch stops N1.
- Any generated spoken identity other than the locked 3,019-token identity stops N1.
- Any direction that changes a word returns to Step 1.
- Any narrator, model, material-setting, or source-format-policy change returns to N3 and requires new calibration.
- A committed draft, available API key, or completed preflight never authorizes an external call.
- Generated audio never authorizes Step 3, public claims, publication, or release.
