# G1R1 owner recovery authorization

Status: **AUTHORIZED BUT NOT COMMIT-ELIGIBLE FOR SYNTHESIS UNTIL THIS THREE-RECORD RECOVERY CHAIN IS
COMMITTED**

Authorized by: Manav Thaker

Authorized at: `2026-08-26T00:38:35Z`

Expires at: `2026-08-27T00:38:35Z`

## Owner decision

The owner authorizes one fresh, same-scope G1 recovery attempt using the unchanged frozen guide
plan, requests, caps, destinations, and stop rules. The previously consumed G1 is historical
evidence and may never be reused, retried, or resumed.

This recovery decision acknowledges the process deviation recorded in the temporary-IAM record:
the exact role grant preceded its authority/evidence record and is currently reported present. The
record does not retroactively authorize that earlier IAM change. It permits only temporary
retention of the exact hash-bound binding for this one recovery attempt.

## Bound recovery chain

| Record or identity | SHA-256 |
| --- | --- |
| Prior consumed G1 authorization | `6d5ae0e6719bae8100cd437b8faa875cbd3f9b3969e09749544d5e5ab06366ea` |
| Prior G1 consumption record | `e7a257dd30128122d3e40b44d7119cb534cf47c70a33db145327f1474c36c4b3` |
| Prior G1 HTTP-403 failure receipt | `3cf567c2b8947f11166112ae63c7c652010f97d5095f7d042cd3f0f354d25ee1` |
| Prior failed-closed disposition | `b05ce0296f4df644b333f74f6e150c8ae46a621844864285847c2532f014daf2` |
| Temporary-IAM authority and state record | `c2468d049eebd7098df66eb685a9a6f43a0754c6631bd0dcccfd59ffe2eb9809` |
| Fresh G1R1 machine authorization | `4dca079b5022d184d080b401225fd819d988851ef40f08d80e3df62ae9825310` |
| Performance-transfer plan | `f73f42e1221753d394ba5de31550094a9aa98e950987e415cb4b0f0c85365f53` |
| Canonical 1,440-byte request body | `4acd99a738125e942fc1a6c2e4ef8df9c819397c9a2627fb494e73d63d004c53` |
| Exact two-request set | `ed1aa73a04db602b8ed2611731346e3f0bfae9d48d55a4f94bb5110da85c0cba` |
| Private quota-project identity | SHA-256 `68a5cdeb9918bf84d3f59c3f428e8e12a40b33f1ab0d0eaee19276be6761c0f2` |
| Private IAM-member identity | SHA-256 `405db2f71219f52e2f9a0a7763cad8b3c0591ccf9274a8757ff3ea1a1f61c31f` |

The raw project and member identities remain outside Git.

## Fresh machine authority

- Authorization:
  `authorizations/03-google-synthetic-guide-recovery.ACTIVE.20260826T003835Z.json`
- Authorization ID:
  `AUTH-G1R1-ai-visibility-v1.1-p01-synthetic-guide-20260826T003835Z`
- Consumption:
  `authorizations/consumed/AUTH-G1R1-ai-visibility-v1.1-p01-synthetic-guide-20260826T003835Z.consumed.json`
- Complete success:
  `receipts/google/AUTH-G1R1-ai-visibility-v1.1-p01-synthetic-guide-20260826T003835Z.run.json`
- Post-consumption failure:
  `receipts/google/AUTH-G1R1-ai-visibility-v1.1-p01-synthetic-guide-20260826T003835Z.failure.json`
- Candidate A: `outputs/raw/google/P01-W0030-W0110/candidate-A.wav`
- Candidate B: `outputs/raw/google/P01-W0030-W0110/candidate-B.wav`

The exact ceilings remain two calls, two outputs, 1,440 request-body bytes per call, 2,880 total
request-body bytes, 4,000,000 response bytes per call, 50 seconds and 2,500,000 bytes per WAV,
5,000,000 total audio bytes, and `$0.66` modeled maximum. Redirects, retries, fallbacks, alternate
requests, alternate models, alternate voices, and resume remain prohibited.

## Commit and execution boundary

No synthesis may occur until all three new recovery records are committed together:

1. the temporary-IAM authority and state record;
2. the fresh G1R1 machine authorization; and
3. this owner recovery authorization.

Before execution, the fresh authorization must still be active and unconsumed, all three new record
hashes must match, both original output destinations and all new receipt destinations must remain
absent, and the private project binding must hash-match. Commit does not authorize any request
drift, IAM expansion, Voice Changer use, guide selection, full capture, Step 3, sharing, or
publication.

The exact temporary-role revoke is already owner-approved and mandatory in the recovery executor's
`finally` path, followed by final IAM-policy readback. Only one etag-conflict cleanup retry is
permitted. `cloudresourcemanager.googleapis.com` enablement was approved and reported completed;
disabling that service is not authorized.

This artifact materialization made no IAM change, credential read, network call, provider request,
authorization consumption, receipt, or audio file.
