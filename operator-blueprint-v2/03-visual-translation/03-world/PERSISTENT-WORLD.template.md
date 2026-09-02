# Persistent world: [episode]

Gate: **V3 — persistent world approved**

Template version: proposed Step 3 v0.2

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

| ID | From | To | What travels | Conditions |
|---|---|---|---|---|

## State transitions

| Object | From state | To state | Trigger | Reversible |
|---|---|---|---|---|

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

## Gate V3 decision

- Objects have stable IDs, forms and allowed states: yes / no
- Object permanence holds across the episode: yes / no
- Every evidence anchor binds to a real claim ID with matching wording authority: yes / no
- Failure routes, money flows and human gates represented: yes / no
- Camera anchors defined with jobs: yes / no
- Every operation-acted object exists; every object is operation-reachable or marked static: yes / no

Result: pass / fail / return to engine

Approved by: [name] on YYYY-MM-DD
