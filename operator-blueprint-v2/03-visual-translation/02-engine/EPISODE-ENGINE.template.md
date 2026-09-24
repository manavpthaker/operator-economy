# Episode engine: [episode]

Gate: **V2 — episode engine approved**

Template version: proposed Step 3 v0.3

Episode: EP###

Input lock SHA-256: [hash]

Operator Canvas SHA-256: [hash]

Boundary Ledger system version: [version]

Boundary Ledger semantic core: [path] · SHA-256: [hash]

Boundary Ledger motion binding: [path] · status: [status] · SHA-256: [hash]

Every field carries `DERIVED`, `SELECTED`, `AUTHORED` or `UNKNOWN`.

## Derived business fields

**These restate decisions Step 1 already locked. Step 3 may not re-decide them. Divergence from the Canvas fails Gate V2.** A genuine disagreement is a change request to Step 1.

| Field | Value | Canvas source | Label | Matches Canvas |
|---|---|---|---|---|
| Operator | | §1 | `DERIVED` | yes / no |
| Customer | | §2 | `DERIVED` | yes / no |
| Distinct beneficiary, if any | | §2 | `DERIVED` | yes / no |
| Constraint | | §3 | `DERIVED` | yes / no |
| Counter-system | | §4 and §6 | `DERIVED` | yes / no |
| Owned value | | §5 | `DERIVED` | yes / no |
| Outcome object | | §5 | `DERIVED` | yes / no |

## Derived business operations and selected Boundary Ledger bindings

One row per material business-state change the episode needs to make legible. The source locator must
point into a hash-locked Canvas, narrative spine, beat sheet, or claims map.

`business_operation` is plain business language derived from the before/after state. It is not a
brand motion name. `boundary_ledger_operation_id` and `boundary_ledger_semantic_role_id` are selected
from the hash-pinned Boundary Ledger core and motion binding; they are not authored here.

| ID | Upstream path + SHA-256 | Exact locator | State before | State after | `business_operation` | Label | BL role ID | BL operation ID | Mapping rationale | Binding permits pair |
|---|---|---|---|---|---|---|---|---|---|---|
| BO-001 | | | | | | `DERIVED` | | | | yes / no |

Required checks for each row:

- Before and after preserve the upstream meaning: yes / no
- `business_operation` is traceable rather than newly invented: yes / no
- Semantic role exists in the pinned core: yes / no
- Operation ID exists in the pinned core: yes / no
- Operation is allowed for that role by the pinned motion binding: yes / no
- Mapping rationale satisfies the operation's canonical `requiredStateChange`: yes / no

**Prohibited:** episode-local motion verbs, renamed Boundary Ledger operations, Rev D motion names as
authority, causal metaphors without upstream state, and scene/animation/renderer primitives.

Label for role and operation selections: `SELECTED`

## Authored episode-direction fields

### Episode visual model

This is the mechanically honest episode-specific model Step 3 builds on top of the derived business
state: for example a relationship leak and return model, queue, capacity model, or handoff system.
It names the persistent actors, zones, relationships, and approved business-operation IDs the world
must make legible. It is not a local motion vocabulary and may not name animation, scene, easing,
renderer, or audio primitives.

- Name:
- Business-operation IDs represented:
- Persistent actors and objects:
- Zones and relationships:
- Mechanical honesty statement:
- Upstream assumptions or evidence it depends on:

Label: `AUTHORED`

### Reality-world visual bible

- People:
- Places:
- Objects:
- Surfaces and interfaces:

Label: `AUTHORED`

### Guardrails

What this engine must never be made to depict:

- [prohibition and why]

Label: `AUTHORED`

## Establishment (`AUTHORED`) — separate from business operations

`establish` changes what the viewer can identify. It does not change the business. Recording it as a
derived business operation would need a `state_before` no upstream artifact contains, so it lives in
its own array and `business_operations` stay `DERIVED` only.

```json
"establishment": [{
  "id": "EST-001",
  "label": "AUTHORED",
  "viewer_state_before": "What the viewer cannot yet identify.",
  "viewer_state_after": "What the viewer can identify once this lands.",
  "reveals": ["object-id"],
  "source_artifact": "../01-editorial/operator-canvas.md",
  "source_sha256": "…",
  "source_locator": "2. Buyer and beneficiary",
  "source_quote": "verbatim line naming the actors and their relationship",
  "boundary_ledger_semantic_role_id": "humanContext",
  "boundary_ledger_operation_id": "establish",
  "selection_label": "SELECTED",
  "mapping_rationale": "Why establish is the operation, and why only viewer knowledge is authored."
}]
```

Fails the gate: `state_before` / `state_after` / `business_operation` on an establishment row;
`acts_on` instead of `reveals`; a missing verbatim quote; an `AUTHORED` row inside
`business_operations`.

## Derived-field provenance for a Markdown Canvas

A JSON Canvas is compared field-for-field. A Markdown Canvas cannot be, so each derived field cites
its own section and quote on the same terms as an operation:

```json
"derived_provenance": {
  "constraint": {"source_artifact": "…", "source_sha256": "…",
                 "source_locator": "3. Costly problem", "source_quote": "verbatim line"}
}
```

Without this the derived-field check cannot run at all, and the gate's headline condition passes
silently unexamined.
## Gate V2 decision

- All derived fields match the locked Canvas: yes / no
- Every business operation matches its locked upstream before/after state: yes / no
- Boundary Ledger core and motion-binding hashes match V1: yes / no
- Every selected role and operation exists and every pair is permitted: yes / no
- Episode visual model covers every business operation and remains mechanically honest: yes / no
- No local motion vocabulary or implementation primitive is authored: yes / no
- Reality-world bible complete: yes / no
- Guardrails stated: yes / no
- Every material field labelled: yes / no

Result: pass / fail / return to Step 1 as a bounded change request

Approved by: [name] on YYYY-MM-DD


