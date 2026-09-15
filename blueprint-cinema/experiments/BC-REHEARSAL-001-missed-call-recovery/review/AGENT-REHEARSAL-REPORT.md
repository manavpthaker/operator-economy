# Agent rehearsal report

## Control

- Experiment: `BC-REHEARSAL-001-missed-call-recovery`
- Work orders issued: `9`
- Completed isolated packets: `9`
- Worker gate approvals: `0`
- Worker production-state changes: `0`
- Canonical experiment integration: root only, serial, hash-checked
- Real episode or shared runtime paths owned by workers: none

Every worker order pinned exact inputs, assigned non-overlapping output paths under `agents/deliverables/<work-order-id>/`, prohibited canonical state and shared-path edits, and required a schema-valid `deliverable.json`. A packet status of `complete` means only that the bounded packet satisfied its order.

## Wave 1 — independent direction review

| Work order | Isolated output | Result | Root disposition |
| --- | --- | --- | --- |
| `wave1-art-motion-critic` | `agents/deliverables/wave1-art-motion-critic/` | complete; 5 blocking, 5 major, 2 minor direction-draft findings | accepted as critique; identity duplication, exact-warning, branch state, continuity, and slide/Prezi risks were corrected before direction lock |
| `wave1-evidence-continuity-critic` | `agents/deliverables/wave1-evidence-continuity-critic/` | complete; 4 blocking, 5 major, 3 minor direction-draft findings | accepted as critique; offer-before-release, proof-pin continuity, object-state drift, and synthetic-outcome disclosure were corrected before direction lock |

Neither critic edited canonical direction. The root integrated the findings serially, rebuilt the style frames and shot board, validated the complete direction package across shot boundaries, and recorded the result in `review/WAVE1-DIRECTION-INTEGRATION.md`.

## Wave 2 — bounded shot construction

| Work order | Owned shots | Result | Root disposition |
| --- | --- | --- | --- |
| `wave2-builder-a` | 01–02 | complete | accepted after pin, structure, deterministic-timeline, and boundary checks; root preserved the corrected shared tag handoff |
| `wave2-builder-b` | 03–04 | complete after one stopped attempt | first attempt stopped because the required local IBM Plex Mono face was absent; root staged the approved local OFL font plus license/provenance, reissued the bounded order, then accepted the validated packet |
| `wave2-builder-c` | 05–07 | complete | accepted after pin, structure, deterministic-timeline, warning, state, and ticket checks |

Workers wrote only isolated composition fragments and animation maps. The root alone merged the fragments into the canonical experiment project, retained one persistent `CALL-R01 / 20:47` tag and one persistent `WO-R01` card, owned the thin root composition, resolved cross-shot geometry and initial-state conflicts, ran the whole-project checks, and rendered the sequence.

## Wave 3 — independent rendered-output QA

| Work order | Reviewed artifact | Result | Root disposition |
| --- | --- | --- | --- |
| `wave3-comprehension-editorial` | first review render | complete; 0 blocking, 4 major, 3 minor | accepted; root corrected the opening time cue and human-gate hierarchy; proof pace and final hold remained open |
| `wave3-technical-continuity-evidence` | first review render | complete; 0 blocking, 3 major, 3 minor | accepted; root corrected tag state, Shot 06 ticket identity, and frame-conform boundaries |
| `wave3-final-editorial-verification` | final render hash `a9f212…24b3` | complete; 2 initial majors resolved, 2 open, no major regression | accepted as the final independent editorial verdict; creative approval remains human |
| `wave3-final-technical-verification` | final render hash `a9f212…24b3` | complete after a fail-closed retry; all 3 initial technical majors resolved | accepted as final technical correction evidence |

The final technical verifier detected that `handoff/timeline-events.json` changed after its first pin check and stopped without writing its packet. The root updated the work-order hash only after the corrected file was complete; the worker then restarted from zero and passed all ten pins. This is the intended stale-input behavior.

## Merge and rejection record

- Accepted: all nine final packets as bounded review or build evidence.
- Rejected from canonical merge: no packet was accepted blindly; worker-owned manifests, reports, and source fragments remained isolated. Only reviewed shot implementations were integrated serially by the root.
- Stopped and retried: Wave 2 builder B for a missing local font contract; final technical verification for a stale timeline-event hash.
- Approval claims rejected: none were attempted; every deliverable records `approval_claimed=false` and `production_state_changed=false`.
- Cross-boundary validation: root validation covered the complete 158-word timeline, seven adjacent shots, persistent object identities, human-gate ordering, fixture disclosure, final render, and handoff event adjacency.

## Agent-work verdict

`PASS FOR THE BOUNDED REHEARSAL.` The contracts constrained ownership and caught two real stopping conditions. They remain experiment-local and manual; the shared Blueprint Cinema runtime does not yet dispatch, enforce, or merge this v2 workflow.
