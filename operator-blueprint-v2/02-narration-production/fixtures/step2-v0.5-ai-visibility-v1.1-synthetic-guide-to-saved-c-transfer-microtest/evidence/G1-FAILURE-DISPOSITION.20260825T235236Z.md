# G1 failed-closed disposition

Status: **CONSUMED; FAILED CLOSED; NO AUDIO**

The exact authorized G1 run began on `2026-08-25T23:52:36Z`. Candidate A's request reached the
bound Google Cloud Text-to-Speech endpoint and returned HTTP `403`. The executor stopped
immediately. It did not retry, redirect, fall back, change the request, or submit candidate B.

## Immutable evidence

| Evidence | SHA-256 |
| --- | --- |
| Active authorization | `6d5ae0e6719bae8100cd437b8faa875cbd3f9b3969e09749544d5e5ab06366ea` |
| Consumption record | `e7a257dd30128122d3e40b44d7119cb534cf47c70a33db145327f1474c36c4b3` |
| Failure receipt | `3cf567c2b8947f11166112ae63c7c652010f97d5095f7d042cd3f0f354d25ee1` |
| Request body | `4acd99a738125e942fc1a6c2e4ef8df9c819397c9a2627fb494e73d63d004c53` |
| Request set | `ed1aa73a04db602b8ed2611731346e3f0bfae9d48d55a4f94bb5110da85c0cba` |

The consumption record predates credential refresh and provider access. The failure receipt records
one 1,440-byte request, HTTP `403`, zero provider-response bytes, zero outputs, zero retries, zero
fallbacks, zero redirects, and `$0.33` modeled attempted spend. No success receipt or candidate WAV
exists.

## Cause boundary

The exact provider error body was deliberately not retained, so the specific `403` cause is
unknown. Google currently documents `aiplatform.endpoints.predict` as required for Gemini-TTS and
identifies `roles/aiplatform.user` as a role that grants it. A missing permission is therefore the
leading hypothesis, not a proven diagnosis. API propagation, model availability, or another account
policy could also have caused the rejection.

No IAM role change, diagnostic synthesis, retry, replacement authorization, guide selection,
ElevenLabs transfer, full capture, Step 2 lock, Step 3, sharing, or publication is authorized by this
failure. Any further Google request requires a new exact owner decision and a new unconsumed
authorization.
