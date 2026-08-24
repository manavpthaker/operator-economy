# Provider External-Action Authorization

Template version: proposed Step 2 v0.3 human authority record.

Create one separate file from this template for exactly one scope. Never combine scopes. A signed
file authorizes only its stated action and cannot approve its output.

## Authority identity

- Authorization ID:
- Exact machine scope for AUTH-01 through AUTH-04, choose one:
  - `elevenlabs_sample_retrieval`
  - `hume_clone_creation`
  - `elevenlabs_calibration`
  - `hume_calibration`
- AUTH-05 uses the dedicated `LONG-FORM-AUTHORIZATION.template.md`; do not encode it as an initial
  machine enum or `full`
- Fixture or episode ID:
- Authorized human:
- Approved at/expires at:
- Status: draft / active / consumed / revoked / expired
- Separate consumption/outcome receipt path:

## Frozen bindings

- Locked script path/SHA-256:
- Ordered `W` count/SHA-256:
- Performance envelope path/SHA-256:
- Provider adapter path/SHA-256, when applicable:
- Provider/account/model/voice or clone ID:
- Original sample provenance path/SHA-256, when applicable:
- Exact P1/P2 or long-form/pickup `W` ranges and hashes:
- Preferred output: provider-native PCM or PCM WAV
- Only lossy fallback: `mp3_44100_192`
- Fallback trigger: explicit PCM/WAV capability unavailable only

## Bounded action

- Exact allowed read, upload, clone, or generation operations:
- Maximum metadata reads:
- Maximum sample downloads:
- Maximum uploads:
- Maximum clones:
- Maximum generation calls:
- Maximum repeated characters:
- Maximum spend, if used:
- Retry rule: none unless separately stated and capped
- Stop behavior for unknown external state:

## Explicit exclusions

- TTS excluded from AUTH-01: yes / no
- Account mutation/retrain/delete/remix excluded from AUTH-01: yes / no
- Second upload/clone and all TTS excluded from AUTH-02: yes / no
- Creative retries, third passage, pickup, and long-form excluded from AUTH-03/AUTH-04: yes / no
- Full capture excluded from every listed scope: yes / no
- Step 1 rewrite and Step 3 excluded: yes / no
- Credentials/media may not enter Git: acknowledged / not acknowledged

## Human decision

- Preconditions and rights verified: yes / no
- Limits cover only the exact action: yes / no
- Logged-in state is not being treated as authority: yes / no
- Authorization statement:
- Human signature/date:

The long-form scope is AUTH-05 and may be created only after signed blind short scores identify the
eligible provider or providers. N4B full capture always requires a later, different authorization.
