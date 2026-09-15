# Decision-log helper delivery

Implemented a standalone standard-library Python helper with `append`, `query`, `status` and `validate`. **20 tests pass**, including batch failures, tampering, source and artifact staleness, exact-revision feedback, traversal/symlink escape and concurrent CLI writers.

## Behavior

- Stores events only at `<root>/blueprint-cinema/episodes/<EP###-slug>/review/decisions/events.jsonl`; episode syntax is strict. `--root` selects a test/alternate checkout, otherwise the helper discovers the repository containing its installed script.
- Accepts one JSON event or an array. Holds an advisory `fcntl` lock, validates the existing chain and entire proposed batch, checks new evidence files/hashes, then appends. Invalid later entries leave all prior event bytes unchanged and a failed first batch produces no event log.
- Adds `episode_id`, UTC `captured_at`, `previous_hash` and `event_hash`. Hashes use canonical compact sorted-key UTF-8 JSON excluding only `event_hash`. Event IDs are globally unique within the episode log.
- Revisions use the same decision ID, a new event ID and `supersedes` pointing to that decision's latest revision. Feedback and verification target an exact decision event, not just a decision ID. Later feedback about an older revision is retained but cannot approve the current revision.
- Requires meaningful decision context, choice/reason, simpler alternative, conditional reuse and concrete nuance. Validates owner/reviewer verdicts, defer triggers, owner-acceptance artifact bindings, verification scope/limitations and candidate-only lessons.
- `status` exposes latest decision, applicable owner feedback, reviewer recommendation, verification and deferred trigger. Historical reconstructions are explicitly labeled as such, rather than actionable pending reviews. It never infers approval from a historical disposition field or a technical pass and always reports `canonical_approval: false`.
- `query` accepts comma-separated or space-separated tags, optional case-insensitive text filtering, and a limit. It ranks by tag overlap then record recency, not creative quality. Returns full decision context, exceptions, matching feedback, and current/superseded indication. Superseded decisions remain retrievable so rejected approaches are not lost.
- `validate --evidence` rechecks all historical source references and reports stale/unavailable evidence without editing or repinning. Ordinary chain reads do not require all historical files to remain unchanged. Appending new entries verifies only the evidence they newly declare.
- Evidence paths must be repository-relative regular files. Parent traversal, absolute/Windows-style paths and symlink escapes are rejected. The log and lock cannot themselves be symlinks.

## Data conventions for root integration

`data.artifact_hashes` is an array of objects with exactly `path` and `sha256`. Each path is a repository-relative regular artifact file, with traversal/symlink-escape protection and current-byte hash validation on append. Owner acceptance requires at least one such binding. Evidence entries additionally require a useful `locator`. `validate --evidence` checks both kinds of bindings and reports their type without repinning. For a runtime fingerprint, bind the exact acceptance-manifest file that carries it and, where useful, the individual runtime files.

Feedback `verbatim`, `interpretation`, `scope` and `deferred_until` when relevant are nonempty text. Verification `method`, `scope` and `limitations` are nonempty text. Irrelevant nuance fields may be absent; a cut cue, if included, needs its ID, phrase and relation, while unknown precise timings can remain explicit unresolved detail.

The helper intentionally permits feedback to reference an older decision revision. It stores that historical observation but filters it out of the current revision's owner verdict. A reviewer acceptance remains a recommendation even if its wording is enthusiastic.

## Validation

Executed:

```text
python3 -m unittest discover -s blueprint-cinema/episodes/EP007-exit-readiness-prep/agents/deliverables/ep007-decision-log-helper -p 'test_*.py' -v
Ran20tests: OK
```

All append/query/status evidence in the tests uses `TemporaryDirectory` roots. Two concurrent CLI processes appended independent decisions without a lost event or broken chain. The issued record-contract input SHA-256 still matches.

## Limits

This is storage, retrieval and structural validation, not a renderer, creative-quality scorer, background agent or canonical approval mechanism. It does not verify that an attributed owner quote actually came from the owner; the orchestrator must use real, frozen message evidence. It cannot certify that a declared exception or rationale is perceptually sound.

The hash chain detects changed/truncated/interleaved history relative to its recorded links; it is not a cryptographic signature against an actor able to rewrite every event and recompute the chain. Invalid input transactions are atomic and ordinary write errors roll back only their uncommitted tail. Abrupt process or machine termination during the filesystem write is not a fully crash-atomic database transaction; incomplete tails are detected on subsequent reads and require an explicit recovery decision.

No actual episode event log, source media, provider job, paid service, production schema, canonical state or global skill file was changed. Root owns installation and seeding. The only authored files are this report, helper, tests and deliverable manifest under the assigned folder.
