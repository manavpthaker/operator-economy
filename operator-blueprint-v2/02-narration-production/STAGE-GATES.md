# Step 2 Stage Gates

Status: proposed v0.1; test before approval.

Each gate is a real decision. Creating a file does not pass a gate.

## N1 — Editorial handoff accepted

Pass only when:

- the episode has a current Step 1 editorial lock and narration handoff;
- script, claims-map, and handoff hashes match;
- the locked spoken word count is recorded and the proposed Step 2 comparison method reproduces it;
- the script contains no unresolved blocker;
- narrator authorization requirements are known; and
- the narration producer signs the handoff checklist.

Failure returns the package to Step 1. Step 2 does not repair the editorial package.

## N2 — Performance direction approved

Pass only when:

- the listener, relationship, central promise, and final landing are clear;
- the episode's major argument and energy turns are mapped;
- dense evidence, economics, uncertainty, and safety passages are flagged;
- pronunciation and number risks are listed; and
- the performance direction adds no spoken language.

## N3 — Voice and capture locked

Pass only when:

- one primary narrator identity is approved and authorized;
- the human capture chain or synthetic provider configuration is frozen;
- output format and provenance fields are defined;
- pronunciation aliases and chunking/session approach are documented;
- continuity risks are understood; and
- owner and voice custodian approve the lock.

## N4 — Calibration and full takes accepted

Pass calibration before full capture. Then pass full takes only when:

- all required calibration modes have been reviewed;
- the approved settings or capture chain were used;
- every script section has usable coverage;
- raw files are immutable, registered, and hashed;
- provider jobs or human sessions are traceable; and
- no unresolved authorization or continuity problem remains.

## N5 — Selects, pickups, and narration edit approved

Pass only when:

- each script section has an approved select;
- defects and pickup decisions are recorded;
- pickups use the same locked words;
- every source edit is represented in the edit decision list;
- joins, breaths, tone, and pacing sound natural; and
- no script change has been hidden inside the edit.

## N6 — Master, conformity, and transcript approved

Pass only when:

- the final narration master meets the Step 2 technical contract;
- lexical comparison is run against that exact master;
- there are zero unresolved spoken-word mismatches;
- the word-level transcript satisfies the timing specification;
- master and transcript hashes are recorded together;
- technical measurements are complete; and
- an independent eyes-closed listen passes.

## N7 — Narration lock and Step 3 handoff approved

Pass only when:

- owner approval is explicit;
- authoritative files, hashes, duration, and word count are frozen;
- all caveats and downstream instructions are disclosed;
- no unresolved pickup, conformity, technical, or permission blocker remains; and
- the visual-translation handoff points to the exact master and transcript.

## Invalidation rules

- A new Step 1 editorial lock invalidates the Step 2 narration lock.
- A script-hash change invalidates affected direction, takes, edit decisions, conformity, transcript, and handoff.
- Previously recorded takes may be reused only when their complete spoken-word sequence is identical in the new locked script and a written impact review approves reuse.
- A narrator, provider/model, generation-setting, room, microphone, capture-chain, sample-rate, or bit-depth change returns the work to N3 and requires renewed calibration.
- Any sample-level narration-master change returns the work to N6 and invalidates the transcript and Step 3 timing handoff.
- A confirmed word mismatch returns to N5 for a same-word pickup or to Step 1 for a script change.
- Visual-production pressure never authorizes a narration exception.

## Alternate exits

- `blocked`: authorization, technical integrity, or required input is missing.
- `returned_to_editorial`: the locked words or editorial package must change.
- `abandoned`: the episode is cancelled with its history preserved.

There is no `approved_with_hidden_mismatch` state.
