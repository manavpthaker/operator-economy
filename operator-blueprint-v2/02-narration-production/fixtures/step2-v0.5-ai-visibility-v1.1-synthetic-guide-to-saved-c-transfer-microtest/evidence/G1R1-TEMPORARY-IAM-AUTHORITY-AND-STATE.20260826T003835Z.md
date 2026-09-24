# G1R1 temporary IAM authority and state record

Status: **EXACT ROLE BINDING REPORTED PRESENT; TEMPORARY RETENTION AUTHORIZED; PROCESS DEVIATION
RECORDED**

Recorded at: `2026-08-26T00:38:35Z`

Authorized by: Manav Thaker

Authority window: `2026-08-26T00:38:35Z` through, but not including,
`2026-08-27T00:38:35Z`, or until the G1R1 recovery authorization is consumed, whichever occurs
first.

## Process deviation

The exact `roles/aiplatform.user` grant was made before this authority/evidence record existed. That
ordering violated the intended authorization-before-IAM-change process. This record does not
retroactively authorize or erase that earlier deviation.

At record time, the operator reported that the exact grant is currently present. This patch did not
read IAM, credentials, tokens, account state, or provider state, so current presence is reported
evidence rather than an independently captured IAM response.

The owner also approved and the operator reported completed enablement of
`cloudresourcemanager.googleapis.com` for the bounded IAM policy operation. Disabling that service
is not authorized.

## Exact bounded binding

| Binding element | Authorized value |
| --- | --- |
| Project identity | SHA-256 `68a5cdeb9918bf84d3f59c3f428e8e12a40b33f1ab0d0eaee19276be6761c0f2` |
| Member identity | SHA-256 `405db2f71219f52e2f9a0a7763cad8b3c0591ccf9274a8757ff3ea1a1f61c31f` |
| Role | `roles/aiplatform.user` |
| Relevant permission | `aiplatform.endpoints.predict` |
| Purpose | One separately authorized G1R1 replay of the unchanged synthetic-guide microtest |

Raw project and member identities are deliberately excluded from Git.

## Temporary authority boundary

The owner authorizes only temporary retention of the exact already-present binding for the one G1R1
recovery attempt and the exact cleanup revoke defined below. This record authorizes no additional
principal, role, permission, project, condition, service-account change, organization-policy
change, service disablement, or other IAM expansion.

No synthesis may occur until this record, the fresh G1R1 machine authorization, and the owner
recovery record are committed together.

The owner-approved cleanup is an exact revoke of only the hash-bound member's
`roles/aiplatform.user` binding on the hash-bound project. It is mandatory in the recovery
executor's `finally` path after any synthesis attempt, whether the request succeeds or fails. The
executor must then read back the final IAM policy and verify that the exact binding is absent. If
the first cleanup write loses an etag race, at most one etag-conflict cleanup retry is authorized;
no retry is authorized for another failure class. Expiry or abandonment before synthesis also
requires the same exact revoke and final readback. The revoke is authorized by this record and does
not require another owner decision; any different IAM mutation does.

The earlier HTTP `403` remains cause-unknown. Presence of this role makes the missing-role
hypothesis testable; it does not prove that the role was the cause or that the recovery request will
succeed.
