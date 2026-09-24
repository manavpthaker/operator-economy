# G1R1 failure and temporary-IAM cleanup disposition

Status: **FAILED CLOSED; TEMPORARY ROLE REMOVED; NO AUDIO**

Recorded at: `2026-08-26T01:12:14Z`

## Exact outcome

The fresh G1R1 authorization was consumed before credential refresh or network access. The exact
unchanged candidate-A request then reached Google and returned HTTP `403`. The executor stopped
immediately.

| Measure | Exact result |
| --- | --- |
| Provider requests | `1` |
| Submitted request bytes | `1,440` |
| Recorded response bytes | `0` |
| Provider outputs | `0` |
| Modeled attempted spend | `$0.33` |
| Retries / redirects / fallbacks | `0 / 0 / 0` |
| Candidate B call | not made |
| Candidate A/B WAVs | absent |
| Successful run receipt | absent |

The only established provider result is HTTP `403`. The redacted response does not prove which
permission, product entitlement, regional constraint, account setting, or other configuration
caused it.

## Temporary-IAM transaction

Before the Google request, the committed transaction wrapper read back exactly one unconditional
direct `roles/aiplatform.user` entry for the hash-bound member and zero conditioned entries. Its
mandatory `finally` path then fetched a fresh policy, removed only that exact temporary entry with
the fresh etag, and read back zero unconditional and zero conditioned target entries.

| IAM measure | Exact result |
| --- | --- |
| Policy reads | `3` |
| Policy writes | `1` |
| Grant writes in the transaction wrapper | `0` |
| Cleanup retries | `0` |
| Cleanup verified | `true` |
| Transaction closed | `true` |
| Role-still-possible security block | `false` |

This is evidence from the transaction's final IAM readback at `2026-08-26T01:12:14Z`; the two
independent post-run audits did not perform another live IAM query. The previously recorded process
deviation remains true: the role grant preceded its committed authority record. The recovery
wrapper did not repeat that grant.

Because the exact request still returned HTTP `403` while the exact direct role was present, absence
of that direct role is not a sufficient explanation for this second failure. That does not identify
the actual cause.

## Immutable bindings

| Artifact | SHA-256 |
| --- | --- |
| Fresh G1R1 authorization | `4dca079b5022d184d080b401225fd819d988851ef40f08d80e3df62ae9825310` |
| G1R1 consumption record | `bfd943d5f221f7f10e7aacab206078da2963b5e6790305b6257f823c3233fba1` |
| G1R1 failure receipt | `df00adefe5e3215ff0c60ed19fe7835d2056a78ba2130e46b18a0d66de2161af` |
| IAM-and-guide transaction receipt | `644f0835a0ae9b931e8762714e49ef7b070dd2ba0923fdbb240199611eaab09b` |
| Committed recovery wrapper | `3cb8e434f0b10b1087087d2a6810885c1f1cd00e17e6846a8937955e05bd90c1` |
| Recovery-wrapper tests | `51d3d6a11e733e30b17f3bb81423e3c79f5e9bdbf1900ae2420d1d65b6eb4f77` |
| Git commit containing the executed wrapper | `dbda4c074aa8bddcf0398da29bf3ae9cfdf96bf2` |

All three generated execution records are regular, nonsymlink local files with owner-only `0600`
permissions. Raw IAM member identity, policy, etag, token, ADC content, and provider error body are
absent from the durable evidence.

## Authority disposition

G1R1 is permanently consumed. No retry, replacement request, alternate Google model or voice,
additional IAM mutation, guide selection, ElevenLabs upload, Voice Changer call, full capture,
Step 2 lock, Step 3, sharing, or publication is authorized. `AUTH-V1` remains blocked because no
guide audio exists.
