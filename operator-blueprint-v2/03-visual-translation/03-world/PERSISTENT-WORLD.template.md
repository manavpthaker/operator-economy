# Persistent world: [episode]

Gate: **V3 — persistent world approved**

Template version: proposed Step 3 v0.3

Episode: EP###

Episode engine SHA-256: [hash]

Claims map SHA-256: [hash]

## Objects

Stable identity, changing state. **An object that changes appearance to suit a shot has broken the world.**

| ID | Name | Material form | Allowed states | Meaning | Reachable by engine operation-binding ID | Label |
|---|---|---|---|---|---|---|
| | | | | | BO-### / `static` | |

Every object an engine operation binding acts on must appear here. Every object here must be
reachable by at least one engine operation-binding ID, or be explicitly marked `static`. The world
does not name animation components or renderer primitives.

## Zones

| ID | Name | What it contains | Camera behaviour |
|---|---|---|---|

## Paths

A path is a route, not a state list. Name what travels it, and give every edge a `from`, a `to`, and
the condition under which it is taken:

```json
{"id": "path.transfer", "traveler": "what moves along this route",
 "edges": [{"from": "a", "to": "b", "condition": "what must be true", "triggered_by": "BO-00n"}]}
```

A path with `states` but no `edges` fails the gate: it describes positions without describing how
anything gets between them.

## State transitions

Each transition names what triggers it and whether it reverses:

```json
{"from": "under-load-test", "to": "documented-and-retained",
 "triggered_by": "BO-005", "reversible": true}
```

Do not collapse a branch the upstream keeps open. If the Canvas says a dependency may be moved *or*
documented, a single terminal `removed` state is a false claim.

## Evidence anchors

Every anchor binds to a **claim ID from the Step 1 claims map**. An anchor with no matching claim fails Gate V3.

| Anchor ID | Claim ID | Attaches to object | Source | Evidence label inherited |
|---|---|---|---|---|

## Failure routes

| ID | What fails | Where it goes | Recovery | Visible consequence |
|---|---|---|---|---|

## Money flows

| ID | From | To | Trigger | Direction |
|---|---|---|---|---|

## Human judgement gates

Where a person decides and the system does not.

| ID | Decision | Who | What happens on each branch |
|---|---|---|---|

## Camera anchors

| ID | Job | When used |
|---|---|---|
| | e.g. human camera for hands, faces, objects, outcomes | |
| | e.g. system camera for relationships, flow, capacity | |

## Object permanence statement

For each recurring object, state what stays constant and what is allowed to change:

| Object | Always recognisable by | May change |
|---|---|---|

## Object classes and instances

A generic object that stands for whichever capability a shot needs violates object permanence.
Declare a class, then give each real thing its own persistent instance. Instances may share a visual
family; they never share an identity, and they may be in different states at the same time.

```json
"object_classes": [{
  "id": "business-part",
  "instances": ["business-part.owner-held-pricing", "business-part.customer-concentration"]
}]
```

An operation may `acts_on` a class when that class declares at least one instance and every declared
instance exists in the world.

## Binding fields

`operation_bindings` conflated three different relationships. v0.3 splits them, and each must name
something that exists:

- `changed_by` — operations that change this object's state. Must match the engine's `acts_on`.
- `carried_by` — operations where the object is present but unchanged.
- `revealed_by` — establishment rows that make it legible. Never changes it.

An object with none of the three must be explicitly `static` with a `static_reason`. Static is not a
gap; it is a claim that the engagement does not change this thing, and it is what stops a later
visual implying otherwise.

## Gate V3 decision

- Objects have stable IDs, forms and allowed states: yes / no
- Object permanence holds across the episode: yes / no
- Every evidence anchor binds to a real claim ID with matching wording authority: yes / no
- Failure routes, money flows and human gates represented: yes / no
- Camera anchors defined with jobs: yes / no
- Every operation-acted object exists; every object is operation-reachable or marked static: yes / no

Result: pass / fail / return to engine

Approved by: [name] on YYYY-MM-DD


