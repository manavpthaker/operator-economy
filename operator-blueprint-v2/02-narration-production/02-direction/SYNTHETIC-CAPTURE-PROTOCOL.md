# Synthetic Narration Capture Protocol

Status: proposed Step 2 v0.2; test before approval.

This protocol makes synthetic narration reproducible without allowing the provider, prompt, or
legacy tooling to become a second script editor.

## Preconditions

No provider request may be sent until:

- N1 accepted the current Step 1 v1.5 package and reproduced its `W` identity;
- N2 approved nonlexical performance direction;
- N3 froze narrator rights, voice ID, provider/model, generation settings, pronunciation method,
  context method, source-format policy, and job-receipt method; and
- a separate `PROVIDER-CALL-AUTHORIZATION` names the fixture or episode, exact frozen
  configuration, bounded phase, expiration, and authorized human.

Calibration and full capture require separate authorizations. An N3 freeze, completed template,
available credential, or successful dry run grants no external-call authority.

## Prohibited legacy path

V2 must not invoke, import, wrap, or fall through to
`studio/scripts/originate/generate_vo.py`. That V1 path may rewrite or performance-mark lexical
content and does not enforce the V2 authorization, source-format, immutable-raw, or state contracts.
Its code remains reference evidence only.

## Frozen request envelope

Every request in one capture batch records and matches:

- Step 1 script SHA-256 and ordered `W`-token SHA-256;
- performance-direction revision and SHA-256;
- narrator-profile and N3 lock revisions and SHA-256 values;
- provider, model/version, voice ID, and every exposed generation setting;
- pronunciation-map revision and SHA-256;
- context/chunking protocol revision;
- requested source format and permitted fallback rule;
- capture phase: `calibration` or `full`;
- batch ID, request ID, chunk ID, and exact ordered `W` range; and
- provider response/job identifier.

A material envelope change invalidates N4A and returns to N3. Credentials remain outside manifests,
logs, prompts, and repository files.

## Exact-word request construction

- Provider-spoken text contains only the exact locked words assigned to the request.
- Pace, silence, emphasis, energy, and restraint may be expressed only through provider-supported
  nonlexical controls already approved at N2/N3.
- Surrounding context, when supported, is passed through a provider field or other method proven
  not to become audible output. Never prepend or append contextual words to the spoken payload.
- The request builder fails closed when the assigned `W` range does not reconstruct the locked
  sequence, contains unapproved markup, or would add spoken direction.
- Provider pronunciation behavior may alter acoustic realization, not canonical `W` identity.

## Calibration batch

N4A contains four bounded requests or recordings:

1. cold open and episode promise;
2. dense evidence;
3. economics and uncertainty; and
4. difficult names, numbers, acronyms, and pronunciation.

Each raw response is preserved before local processing. Interim ASR remains diagnostic. Each
passage receives lexical, technical, and performance review. The owner must approve the calibration
performance before a full-capture authorization may be issued.

## Full-capture chunk map

Prefer one controlled full-script batch. When provider limits require multiple requests:

- split at argument, paragraph, sentence, and breath boundaries rather than arbitrary character
  counts;
- cover every `W` token exactly once and in order;
- record bounded preceding/following context separately from spoken payload;
- avoid tiny orphan chunks whose prosody cannot match neighboring material;
- preserve a single batch identity across all requests; and
- review adjacent chunk boundaries and the uninterrupted full run for timbre, pace, energy,
  pronunciation, room character, and prosody.

Locally acceptable chunks do not pass N4B if the complete episode sounds assembled from different
sessions.

## Source-format policy

1. Request native PCM when the current provider/account/model supports it.
2. Inspect the actual returned container and codec; never trust the filename or request alone.
3. When native PCM is unavailable, accept only `mp3_44100_192` and record fallback reason
   `pcm_capability_unavailable`.
4. Preserve the returned file byte-for-byte as immutable raw and record audio origin
   `native_pcm` or `lossy_mp3`.
5. A fallback MP3 must pass an audible review for swirls, watery tails, pre-echo, harsh sibilance,
   transient damage, or intelligibility loss.
6. Decode/resample the fallback exactly once into 48 kHz, 24-bit, mono PCM for all editorial work.
7. Do not introduce MP3, AAC, or another lossy intermediate afterward.
8. Never label a PCM file derived from MP3 as native PCM acquisition.

## Immutable raw and receipts

Before review or conversion, register each provider response with:

- raw path and SHA-256;
- actual container, codec, sample rate, bit depth when meaningful, channels, and duration;
- audio origin and fallback reason;
- batch, request, chunk, and provider job IDs;
- request-envelope hash;
- exact `W` range and spoken-payload hash;
- creation time; and
- provider-reported metadata or alignment, marked non-authoritative.

Provider errors and partial responses are also logged. Never overwrite a failed or superseded raw
response; record its disposition.

## Pickups and regeneration

A synthetic pickup is a new immutable provider request. It uses the same locked words, envelope,
approved context method, and source-format policy.

- A settings, voice, model, source-format policy, or pronunciation-method change returns to N3.
- A one-line pickup that cannot match its neighbors requires a wider bounded regeneration.
- If wider regeneration still drifts, regenerate the full batch or return to calibration.
- Every accepted replacement receives lexical review, boundary review, full-run continuity review,
  and an edit-decision record.
- A requested word change returns to Step 1.

## Failure and stop behavior

Stop without substituting another voice or format when:

- authorization is absent, expired, consumed, or mismatched;
- provider output cannot be tied to a job and request envelope;
- returned audio is neither native PCM nor permitted `mp3_44100_192`;
- lossy artifacts are audible enough to compromise the narration;
- exact-word payload identity fails;
- provider behavior adds or removes words;
- continuity cannot be proven; or
- rights, consent, credentials, or provider terms are unresolved.

Provider success is acquisition evidence only. It cannot create `technical_pass`,
`creative_approved`, or `workflow_status: locked`.
