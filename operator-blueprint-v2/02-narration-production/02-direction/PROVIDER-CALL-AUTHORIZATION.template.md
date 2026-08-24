# External Voice Provider Call Authorization

Template version: proposed Step 2 v0.2.

V0.3 boundary: this remains the v0.2 machine-paired ElevenLabs `calibration`/`full` call template.
Do not overload it for account reads, original-sample retrieval, Hume UI upload/clone, blind
short-bakeoff scoring, or the later long-form selection test. Use
`PROVIDER-EXTERNAL-ACTION-AUTHORIZATION.template.md` for each of those distinct proposed v0.3
actions. No provider-selection scope may be mislabeled `full`.

This record authorizes one bounded external action. It does not approve the resulting audio or any
later phase.

The signed human review is accompanied by
`PROVIDER-CALL-AUTHORIZATION.template.json`, the minimal machine receipt consumed by the CLI. Both
must identify the same capture-plan hash, canonical `W` hash, phase, provider, voice, approver, and
approval time.

## Authority identity

- Authorization ID:
- Target kind and ID: fixture / episode; exact ID
- Phase/scope: calibration / full
- Authorized by:
- Authorization date and expiration:
- Authorization status: `active`
- Machine approval value: `true`

## Frozen inputs

- Step 1 script path/SHA-256:
- Ordered `W`-token count/SHA-256:
- Performance-direction path/SHA-256:
- Capture-plan path/SHA-256:
- Narrator-profile path/SHA-256:
- N3 voice-and-capture lock path/SHA-256:
- Provider: `elevenlabs`
- Model ID:
- Authorized voice ID or internal alias:
- Generation-settings identity:
- Pronunciation-map identity:
- Context/chunking protocol identity:

## Source-format request

- First request: native PCM
- Permitted fallback: `mp3_44100_192` only
- Permitted fallback reason: `pcm_capability_unavailable` only
- Immutable raw, actual-codec inspection, audible artifact review, and one PCM conversion required:
  yes / no
- Any other output format authorized: no

## Scope limits

- Exact calibration passage IDs or full-capture batch ID:
- `max_calls`: at least the number of plan parts and no more than twice that number, allowing one
  PCM attempt plus a bounded fallback attempt per part
- `max_characters`: positive repeated-character ceiling / omitted only when positive
  `max_spend_usd` is supplied
- Consumption status before execution: `unconsumed`
- Calls used before execution: `0`
- Safe relative consumption-record path:
- Pickups included: no / yes, exact bounded rule
- Credentials provided through approved secret path: yes / no
- Voice cloning or creation included: no / yes, separate rights record required
- Script rewrite permitted: no
- Visual, publication, or release authority included: no

## Decision

- Preconditions N1/N2/N3 current: yes / no
- Rights and consent current: yes / no
- Capture-plan, script, canonical `W`, target, model, and voice hashes/IDs all match: yes / no
- Preferred format is `pcm_48000` and fallback is exactly `mp3_44100_192`: yes / no
- Expiration is in the future and budget/call caps cover only this bounded plan: yes / no
- Authorized action statement:
- Owner or delegated human signature/date:

Calibration authorization cannot be reused for `full`. A `full` authorization cannot be
inferred from calibration approval. Automation must fail closed when this record is absent,
mismatched, expired, revoked, or already consumed beyond its stated scope.
