# Full-timeline visual plan: [episode]

Gate: **V4 — visual plan approved, per act**

Template version: proposed Step 3 v0.1

Episode: EP###

World SHA-256: [hash]

Word-level transcript SHA-256: [hash]

Narration duration: [seconds]

**Timing comes from the Step 2 transcript. An estimated duration fails Gate V4.**

## Act boundaries

Taken from the Step 1 beat sheet. Each act is reviewed and approved separately, and a rejected act returns only that act.

| Act | Beat range | Word range | Units | Approval |
|---|---|---|---|---|
| Opening ladder | | | | pending / approved / returned |
| Act I | | | | pending / approved / returned |
| Act II | | | | pending / approved / returned |
| Ending | | | | pending / approved / returned |

## Units

One row per timed unit. Repeat this table per act.

| ID | In (word idx) | Out (word idx) | Mode | Camera anchor | Motion verb | Carry | Focus | World state before | World state after | Evidence | Narrative state |
|---|---|---|---|---|---|---|---|---|---|---|---|

Mode is one of: `reality`, `system`, `proof`, `outcome`, `identity`.

## Inert-unit audit

**A unit whose world state does not change and which carries no evidence is doing nothing.** List every such unit and its disposition. It must be justified in writing or merged into its neighbour.

| Unit | Why it has no state change and no evidence | Disposition |
|---|---|---|
| | | justified / merged |

## Coverage audit, per act

- Units cover the act's narration continuously: yes / no
- Unexplained gaps: none / [list]
- Overlaps: none / [list]
- Mode distribution: [counts] — deliberate, or single-mode?

## Reference integrity

- Every object referenced exists in the approved world: yes / no
- Every verb referenced exists in the approved engine: yes / no
- Every evidence item carries its upstream label unchanged: yes / no
- **No visual upgrades an evidence label:** confirmed / violation at [unit]

## Gate V4 decision, per act

| Act | Timing from transcript | Continuous coverage | No inert units | References valid | Labels intact | Result |
|---|---|---|---|---|---|---|

If a rejection names a defect in the **direction bible** rather than in the act, it escalates to Gate V5 and the bible is revised before the act is re-reviewed.

Approved by: [name] on YYYY-MM-DD
