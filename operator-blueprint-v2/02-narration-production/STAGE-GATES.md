# Step 2 Stage Gates

Status: proposed v0.2; test before approval.

Each gate is a real decision. Creating a file does not pass a gate.

## N1 — Editorial handoff accepted

Pass only when:

- the episode has a current Step 1 editorial lock and narration handoff;
- the Step 1 v1.5 Episode Investment Thesis, Canvas, beat sheet, editorial-voice conformity,
  script, claims map, lock, and handoff identities are present and current;
- all required hashes match the package manifest;
- `oe-spoken-text-v1` reproduces the locked ordered whitespace-token count and SHA-256;
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

For the authorized AI Visibility v1.1 fixture, the expected `W` identity is 3,019 tokens at
`096329c04c9ce0ce9964e67279657be9fbd488772ae7df8893a28f76083d283a`. Workflow Operations is
historical and must fail N1 unless Step 1 later issues a current lock and ready handoff.

## N3 — Narrator identity and acquisition configuration frozen

Pass only when:

- one primary narrator identity and rights basis are approved for calibration;
- the human acquisition chain or synthetic provider configuration is frozen for calibration;
- native acquisition format, delivery-master format, and provenance fields are separately defined;
- pronunciation aliases and chunking/session approach are documented;
- continuity risks are understood; and
- owner and voice custodian approve the configuration freeze.

An N3 pass makes calibration reproducible. It is not creative approval and does not authorize an
external call. The exact episode or fixture, voice, provider/model, scope, and spend-bearing action
require separate explicit authorization before any provider call.

## N4A — Calibration accepted

Pass only when:

- the bounded calibration recording or provider calls were separately authorized;
- all four calibration modes were acquired under the frozen N3 configuration;
- native acquisition files are immutable, registered, hashed, and truthfully inspected;
- native PCM was requested first, or `mp3_44100_192` is recorded as the only fallback;
- a fallback MP3 passed the audible codec-artifact review and its single PCM conversion is recorded;
- interim ASR is labeled diagnostic and every likely lexical defect is dispositioned;
- each passage has a lexical finding and technical result;
- continuity, intelligibility, pronunciation, and argument-mode differentiation pass; and
- the owner records the calibration creative decision.

## N4B — Full capture accepted

Pass only when:

- N4A is current and the full-capture recording or provider calls were separately authorized;
- the approved N3 settings or human capture chain were used;
- every script section has usable coverage;
- raw files are immutable, registered, and hashed;
- provider jobs or human sessions are traceable; and
- interim take or chunk ASR remains diagnostic rather than becoming the final transcript;
- the complete capture passes a continuity listen; and
- no unresolved authorization or continuity problem remains.

The machine state records one N4 gate. N4 is `passed` only when both N4A calibration and N4B full
capture pass. A failure or invalidation of either subgate makes N4 `failed` or `invalidated`.

## N5 — Selects, pickups, and narration edit approved

Pass only when:

- each script section has an approved select;
- defects and pickup decisions are recorded;
- pickups use the same locked words;
- every source edit is represented in the edit decision list;
- joins, breaths, tone, and pacing sound natural; and
- synthetic regenerations and pickups pass the continuity rules in
  `02-direction/SYNTHETIC-CAPTURE-PROTOCOL.md`; and
- no script change has been hidden inside the edit.

## N6 — Exact master receives `technical_pass`

Pass only when:

- the final narration master meets the Step 2 technical contract;
- native acquisition and delivery-master formats are separately disclosed, including any
  `mp3_44100_192` fallback and its single conversion;
- no lossy intermediate exists after native acquisition;
- one master candidate is frozen before final alignment;
- final-master ASR or alignment and lexical comparison are run against that exact master hash;
- there are zero unresolved `W`-token mismatches;
- the word-level transcript satisfies the timing specification;
- the intentional-pause map is bound to the same master hash and duration;
- master, transcript, and pause-map hashes are recorded together;
- technical measurements are complete; and
- local validation records `technical_pass` for that exact master hash.

Interim ASR cannot satisfy N6. Any pickup, edit, processing, or sample-level change invalidates the
final alignment, conformity result, transcript, pause map, and technical pass.

## N7 — Creative approval, narration lock, and Step 3 handoff

Pass only when:

- N6 `technical_pass` is current;
- the independent eyes-closed listen is complete;
- owner `creative_approved` is explicit and names the same master hash;
- authoritative files, hashes, duration, and word count are frozen;
- all caveats and downstream instructions are disclosed;
- no unresolved pickup, conformity, technical, or permission blocker remains; and
- the visual-translation handoff points to the exact master and transcript.

## Invalidation rules

- A new Step 1 editorial lock invalidates the Step 2 narration lock.
- A script-hash change invalidates affected direction, takes, edit decisions, conformity, transcript, and handoff.
- Previously recorded takes may be reused only when their complete spoken-word sequence is identical in the new locked script and a written impact review approves reuse.
- A narrator, provider/model, generation-setting, room, microphone, capture-chain, sample-rate, or bit-depth change returns the work to N3 and requires renewed calibration.
- A change after N3 invalidates N4A; N4B may not begin until renewed calibration passes.
- Any sample-level narration-master change returns the work to N6 and invalidates final alignment,
  lexical conformity, transcript, intentional-pause map, `technical_pass`, `creative_approved`,
  narration lock, and Step 3 timing handoff.
- A confirmed word mismatch returns to N5 for a same-word pickup or to Step 1 for a script change.
- Visual-production pressure never authorizes a narration exception.

## Decision-state rule

- `technical_pass` is a technical state only. It cannot imply that the voice or performance is
  creatively accepted.
- `creative_approved` is a named-owner state only. It cannot be inferred from technical success or
  assigned by an agent, provider, exporter, validator, or independent listener.
- `workflow_status: locked` requires both states against one identical master hash.

## Alternate exits

- `blocked`: authorization, technical integrity, or required input is missing.
- `returned_to_editorial`: the locked words or editorial package must change.
- `abandoned`: the episode is cancelled with its history preserved.

There is no `approved_with_hidden_mismatch` state.
