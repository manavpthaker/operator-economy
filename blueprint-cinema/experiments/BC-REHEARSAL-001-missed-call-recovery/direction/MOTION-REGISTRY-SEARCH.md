# HyperFrames motion-registry search · BC-REHEARSAL-001

Searches ran locally with the project-pinned `hyperframes 0.8.4` after the static direction passed, and before animation authoring. Registry search did not authorize a direction change.

## Queries and decisions

| Intended movement | Search tier | Candidate | Decision |
|---|---|---|---|
| Move one persistent tag along a visible route and attach it to a card | local word match | `arc-motion-path` | Rejected. A curved, autorotating flight would make an ordinary operating route feel decorative. Use an authored straight screen-space translation on the root-persistent tag. |
| Same | local word match | `morph-swap` | Rejected. The tag and work-order card must coexist and retain identity; one object must not substitute for the other. |
| Same | local word match | `pull-back-reveal` | Reserved only as a constraint reference for shot 6. Adapt to a single ≤12% decelerating pullback that reveals causal context; omit stat-card and supporting-card defaults. |
| Draw a route line between operating nodes | local word match | `svg-stroke-trace` | Adapt the measured `stroke-dasharray` / `stroke-dashoffset` behavior from the fully read `svg-path-draw` rule. Remove its optional drift. Every drawn line must land on real nodes and activate a route. |
| Same | local word match | `flowchart` | Rejected. Sticky-note nodes, cursor interaction, and a generic decision-tree presentation violate the operating-world and anti-slide direction. |
| Hold and release an object at a human decision gate | local word match | `flowchart` | Rejected for the same reason. |
| Same | local word match | `pull-back-reveal` | Rejected for the gate. Camera scale cannot substitute for the required physical stop. |
| Same | local word match | `morph-swap` | Rejected. A state swap cannot prove that the tag was physically held until human release. |

## Authored behavior allowed after search

- Root tag: deterministic `x` / `y` translation with `power2.inOut` or `power2.out`; no arc, bounce, elastic ease, autorotation, or ambient loop.
- Route lines: measured SVG path length, initially hidden with dash offset, drawn once toward a real destination, then held still.
- Human gate: barrier and tag construct in their static end geometry; tag reaches the barrier and remains motionless for at least 1.7 seconds; only the explicit operator release cue opens the route.
- Outcome attachment: tag and work-order card remain separate persistent DOM identities. The tag docks beside the card; the card state changes only after accepted booking.
- Pullback: one scale change in shot 6, no more than 12%, no pan among nodes, then a readable hold.

No registry block was installed. No search-miss feedback was submitted because that would be an external write outside this offline rehearsal.
