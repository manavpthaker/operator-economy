# EP006 persistent-world integrity review

## Packet identity

- Work order: `world-integrity-review`
- Required gate observed: `episode_engine_approved`
- Input lock SHA-256: `e99b847c5b5a767d74ad4208738374ac191da3d9d4c3e3654098a6c08e725691`
- Episode engine SHA-256: `e07ed63476684bc3e3a2757e1e30c651322859a9f27b4f25bc7a08d15ddc4b36`
- Proposed world SHA-256: `80a12c7296b76591258d210bf038c4d71ccef195669304e4289bccb3df3c576b`
- External writes, internet use, paid services, synthetic generation, and legacy visual inputs: none

All three declared hashes were recomputed before review and matched the work order. The current production state supplied the required `episode_engine_approved` gate. This packet is an isolated read-only audit; it neither approves the world nor changes production state.

## Verdict

The proposed world has a sound main recovery topology and passes the current schema and semantic validator, but I do **not** recommend approval at the reviewed hash yet. The directed success route correctly preserves useful first-booking acquisition and forces audit, repair, consent, qualification, human review, follow-up, the repaired direct destination, return value, and confirmation in order. Suppression and the explicit sensitive-case terminal have no outbound edges. Economics and the guest-facing outcome are correctly separate.

Three gaps remain approval-relevant:

1. Failure and escalation metadata is not consistently represented by directed edges, and the sensitive-qualification failure can point into a human-review node that also owns the successful outbound edge.
2. Three evidence records are labeled `locked_source` even though their source artifacts are not hash-pinned by the declared input lock, and the five claim IDs plus nine parameter IDs have no declared registry in the reviewed inputs.
3. Two important object pairs have near-colliding coordinates, and the system camera targets a reality-zone destination without an explicit cross-zone contract.

The packet itself is complete because the requested audit was performed. `complete` here does not mean the world passed this independent review or that any gate advanced.

## Inventory and referential integrity

The world contains 25 objects, 26 edges, five evidence pins, three cameras, and four failure records: 63 stable record IDs in total.

| Check | Result | Detail |
|---|---|---|
| Stable IDs | Pass | No duplicate ID across objects, edges, evidence, cameras, or failures. |
| Object zones | Pass | Every `zone_id` resolves to a `kind: zone` object; zone self-membership is internally consistent. |
| Object and edge states | Pass | Every initial state resolves within its owner, and object state IDs are locally unique. |
| Edge endpoints | Pass | All 52 `from` and `to` references resolve to objects. |
| Required roles | Pass | Every required role resolves to an existing object of the intended broad kind. |
| Canonical paths | Pass structurally | Every adjacent pair in `first_booking`, `recovery`, `suppressed`, and `failure_retry` has a directed edge. |
| Evidence targets | Pass structurally | All ten evidence target references resolve to objects. |
| Cameras | Pass structurally | All camera zones and 13 camera targets resolve to objects. |
| Failures | Pass structurally | Every `at_id`, `retry_to_id`, `escalation_to_id`, and `failed_state` resolves. |

The structural pass is narrower than semantic approval. In particular, a valid failure destination ID does not prove that the route exists in the persistent directed world, and a syntactically valid claim ID does not prove that a hash-pinned claim record exists.

## Canonical path trace

### Useful first booking

The canonical first-booking route is complete and useful:

```text
market-discovery
  -> ota-booking-gate
  -> first-booking-money-flow
  -> hotel-stay-node
  -> stay-key-tag
```

The OTA is a discovery and trusted first-checkout gate, not a villain. First-booking money is split into an operator-side settlement branch through `edge-first-ledger`, while the guest proceeds into the delivered stay. The path ends with the physical key tag, which remains a completed-stay token rather than permissioned memory.

### Recovery route

There is exactly one simple directed path from `stay-key-tag` to each of `relevant-follow-up`, `direct-booking-destination`, and `direct-booking-confirmation`. It is:

```text
stay-key-tag
  -> direct-path-audit
  -> direct-path-repair
  -> permission-gate
  -> guest-memory-context
  -> return-qualification-gate
  -> human-review-gate
  -> relevant-follow-up
  -> direct-booking-destination
  -> return-booking-money-flow
  -> direct-booking-confirmation
```

Removing any one of `direct-path-audit`, `direct-path-repair`, `permission-gate`, `return-qualification-gate`, or `human-review-gate` eliminates the input-to-confirmation path. There is therefore no directed main-world bypass around audit, repair, consent, qualification, or human review.

The only inbound route to `direct-booking-destination` comes from `relevant-follow-up`, whose only route from the stay passes the audit and repair nodes first. The direct return cannot activate from the completed-stay input before the direct-path work.

### Suppression and exceptions

The explicit suppressed route terminates at `suppression-register`, whose out-degree is zero:

```text
stay-key-tag
  -> direct-path-audit
  -> direct-path-repair
  -> permission-gate
  -> suppression-register
```

Qualification also has a suppression edge to the same terminal. `sensitive-case-escalation` likewise has no outbound edge. Those two objects cannot automatically reach follow-up, destination, or confirmation through the `edges` graph.

There is, however, a material inconsistency in the failure metadata: `failure-sensitive-qualification.escalation_to_id` points to `human-review-gate`, while `edge-qualification-exception` points to the terminal `sensitive-case-escalation`. Because `human-review-gate` also has `edge-human-followup`, and edges carry no state preconditions, the data model itself does not prove that a suppressed or sensitive qualification routed there can receive disposition without later taking the success edge. Prose says it must never become automatic outbound, but the graph does not encode that distinction.

Required correction before approval: route the sensitive failure to the explicit terminal exception object, or add a distinct disposition-only human node/path whose outgoing edges cannot reach follow-up. Do not rely on labels or renderer interpretation to distinguish success review from sensitive-case disposition.

## Failure, retry, and escalation audit

The audit found three failure destinations that resolve as IDs but do not exist as directed edges from the failure location:

| Failure | Declared route without matching edge |
|---|---|
| `failure-direct-path-retest` | escalation `direct-path-repair -> independent-hotel-operator` |
| `failure-follow-up-delivery` | retry `relevant-follow-up -> human-review-gate` |
| `failure-follow-up-delivery` | escalation `relevant-follow-up -> independent-hotel-operator` |

The direct-path retry itself is visible and coherent:

```text
direct-path-repair
  -> repair-retry-queue
  -> direct-path-audit
  -> sensitive-case-escalation
```

But its failure record separately says escalation goes to the operator, while the canonical `failure_retry` path ends at the sensitive-case exception. Similarly, the follow-up-delivery failure describes a deliberate retry after human review, but the edge graph has only the opposite successful direction, `human-review-gate -> relevant-follow-up`.

Required correction before approval: make every operational retry and escalation a first-class edge/path, or define and validate a single alternative route contract that the renderer consumes directly. As written, a renderer using `edges` cannot depict three declared failure routes without inventing them from failure metadata, while a renderer using failure metadata disagrees with the canonical failure path.

## Economics and confirmation separation

This check passes.

- `first-booking-money-flow` branches to `ota-settlement-ledger`, a `ledger` in the proof zone.
- The first booking continues independently to `hotel-stay-node` and the completed stay.
- `direct-booking-destination` routes later value to `return-booking-money-flow`.
- `return-booking-money-flow` issues `direct-booking-confirmation`, an `outcome` in the reality zone.
- The settlement ledger and confirmation have different IDs, kinds, zones, labels, descriptions, and graph jobs. There is no edge that treats the confirmation as commission proof.

This preserves both claims required by the engine: useful first-booking acquisition can have an operator-side commission consequence, and the later visible outcome is a separate direct reservation confirmation.

## Evidence attachment and source authority

All five evidence IDs are unique, and every evidence target resolves. The target assignments are substantively plausible: OTA share attaches to the OTA and leak state; the illustrative commission model attaches to first-booking money and the operator ledger; cancellation evidence attaches to the ledger and direct destination; operator history and labor-value context attach to the operator and human-review gate.

The hash authority is incomplete:

| Evidence ID | Source path | Present locally | Hash-pinned by reviewed input lock |
|---|---|---:|---:|
| `evidence-ota-share` | `studio/originate/direct-booking-recovery/research.md` | Yes | No |
| `evidence-commission-model` | `studio/originate/direct-booking-recovery/script.json` | Yes | Yes |
| `evidence-cancellation-gap` | `studio/originate/direct-booking-recovery/research.md` | Yes | No |
| `evidence-operator-history` | `../content-os/facts.md` | Yes | No |
| `evidence-labor-value` | `studio/originate/direct-booking-recovery/script.json` | Yes | Yes |

`research.md` and `facts.md` can change without invalidating `input-lock.json`, `world.json`, or a future world approval record, even though the corresponding evidence entries say `locked_source`. In addition, the reviewed engine, world, and input lock do not provide a hash-pinned registry in which the five `claim_ids` and nine `parameter_ids` can be resolved. They are well-formed strings, but their semantic referents cannot be verified from the work-order inputs.

Required correction before approval: hash-pin the exact evidence and claim/parameter registry artifacts, or change these evidence records to an honest unresolved/ticketed state until that lock exists. Extend semantic validation so every claim and parameter ID resolves against the approved, hash-pinned registry.

## Coordinate and camera coherence

All object and camera points are numeric and within the 1920 by 1080 coordinate system. Stable IDs, positions, zone membership, and camera targets make the model deterministic at the point-data level.

The spatial layout is not yet demonstrably readable:

- `first-booking-money-flow` at `(1530, 350)` and `direct-booking-destination` at `(1540, 300)` are only 51 pixels apart despite being distinct nodes in different zones.
- `relevant-follow-up` at `(1650, 480)` and `return-booking-money-flow` at `(1690, 380)` are about 108 pixels apart.
- The schema provides no node footprint or collision rule, so normal labeled greybox cards at these anchors are likely to overlap.
- `camera-system` declares `system-zone` but targets `direct-booking-destination`, whose `zone_id` is `reality-zone`. This may be a motivated cross-zone handoff, but the current contract does not mark it as intentional or define how the camera crosses zones.

Required correction before approval or, at minimum, before compiling render data: separate the colliding anchors using an explicit primitive footprint, and either keep camera targets within their declared zone or add an explicit cross-zone camera contract. The renderer must not infer a repair from labels or narration.

## Acceptance-check matrix

| Work-order acceptance check | Result |
|---|---|
| Trace every canonical path and every referenced object, state, evidence, camera, retry, and escalation ID | Structural pass; semantic failure routes need correction |
| Find any outbound or confirmation route bypassing audit, repair, consent, qualification, or human review | Pass; none found in the directed edge graph |
| Suppression and sensitive cases terminate or escalate without automatic outbound | Suppression passes; sensitive qualification is ambiguous because its failure record points to the outbound-capable human gate |
| Preserve useful first-booking economics and separate ledger from direct confirmation | Pass |
| Return a schema-valid packet without approval or state change | Pass after packet validation; no approval or state mutation claimed |

## Approval recommendation

Do not approve `world.json` at SHA-256 `80a12c7296b76591258d210bf038c4d71ccef195669304e4289bccb3df3c576b` on the strength of schema validation alone. The orchestrator should resolve the failure-route conflict, pin the evidence authority and registries, and correct or explicitly contract the spatial/camera exceptions; then recompute the world hash, reissue any stale work order, and rerun both built-in validation and this semantic trace.

## Worker boundary

No canonical episode artifact, production state, approval record, shared runtime, schema, renderer entry point, scaffold documentation, or upstream file was changed. Only this report and its sibling `deliverable.json` were written inside the owned packet directory.
