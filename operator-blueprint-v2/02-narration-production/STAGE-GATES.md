# Step 2 Stage Gates

Status: proposed v0.3 provider-selection revision; test before approval. V0.2 fixture evidence is
retained unchanged.

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

N2 also freezes a provider-agnostic performance envelope. Provider tags, descriptions, model
settings, voice IDs, and replacement text are forbidden in that envelope; they belong in separately
hashed provider adapters.

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

When the narration method is not yet creatively accepted, N3 uses the provider-selection loop in
[`TOOL-AUDIT-AND-BAKEOFF.md`](TOOL-AUDIT-AND-BAKEOFF.md):

1. freeze provisional ElevenLabs and Hume request envelopes against one performance
   envelope;
2. pass the original-human-sample provenance and commercial-rights gates;
3. obtain and consume four separate authorizations for the exact read/retrieval, UI clone, Eleven
   short calibration, and Hume short calibration actions;
4. freeze the owner and independent-listener blind scorecards, then create a separate curator
   consolidation bound to both scorecard hashes and the sealed-map hash; only that consolidation
   unseals providers, selects each provider's highest hard-gate-passing generation independently for
   P1 and P2, and averages those passage selects into its provider score;
5. advance the eligible leader and only a runner-up within 5.0 points to a separately authorized
   long-form continuity and pickup test; and
6. treat long-form/pickup as pass/fail confirmation, apply the asymmetric final rule using only the
   frozen short provider scores, and then freeze the selected N3 method.

Unselected failures and generation variance are operational metrics, not creative-score penalties.
A disqualified generation can never be a passage select. If both generations fail for either
passage, that provider is ineligible.

Provisional candidate freezes are test inputs, not an N3 pass. N3 passes only after the owner signs
one selected method and its exact provider/model/voice/settings/source-format configuration.

An N3 pass makes calibration reproducible. It is not creative approval and does not authorize an
external call. The exact fixture or episode, voice, provider/model, scope, format, and spend-bearing
action require separate explicit authorization before every external action. A logged-in provider
session, completed template, earlier calibration authorization, or selected method grants none.

## N4A — Calibration accepted

Pass only when:

- the bounded calibration recording or provider calls were separately authorized;
- all four calibration modes were acquired under the frozen N3 configuration;
- native acquisition files are immutable, registered, hashed, and truthfully inspected;
- provider-native PCM or PCM WAV was requested first, or `mp3_44100_192` is recorded as the only
  explicitly authorized capability-unavailable fallback;
- a fallback MP3 passed the audible codec-artifact review and its single PCM conversion is recorded;
- interim ASR is labeled diagnostic and every likely lexical defect is dispositioned;
- each passage has a lexical finding and technical result;
- continuity, intelligibility, pronunciation, and argument-mode differentiation pass; and
- the owner records the calibration creative decision.

The current AI Visibility v1.1 N4A evidence is **technical PASS / owner creative REVISE**. N4A is
therefore not passed. Preserve the batch as technical evidence and route the performance/provider
problem through N2/N3 selection. Do not reopen Step 1 unless the owner identifies an actual wording
change or editorial defect.

A provider bakeoff score or method-selection lock cannot pass N4A. After N3 selects a method, the
chosen calibration still requires the explicit owner creative decision at this gate.

## N4B — Full capture accepted

Pass only when:

- N4A is current and the full-capture recording or provider calls were separately authorized;
- the approved N3 settings or human capture chain were used;
- every script section has usable coverage;
- **every captured chunk decays into silence.** Tail energy in the final 60 ms, measured against the
  chunk's peak, is below `0.02`. A chunk that is still sounding at its final sample was cut
  mid-utterance and must be recaptured;
- raw files are immutable, registered, and hashed;
- provider jobs or human sessions are traceable; and
- interim take or chunk ASR remains diagnostic rather than becoming the final transcript;
- the complete capture passes a continuity listen; and
- no unresolved authorization or continuity problem remains.

The machine state records one N4 gate. N4 is `passed` only when both N4A calibration and N4B full
capture pass. A failure or invalidation of either subgate makes N4 `failed` or `invalidated`.

No provider-bakeoff authorization, blind score, long-form test, or N3 method selection grants N4B
authority. N4B always requires a new, separately bounded full-capture authorization after N4A has
passed for the selected method.

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
- **completeness is established separately from conformity.** Forced alignment force-fits: it
  assigns best-fit timings to whatever text it is given and cannot detect missing audio. Zero
  `W`-token mismatches is therefore **not** evidence that the words were spoken. The master must
  additionally satisfy: no chunk ending mid-sound by the tail-energy test, and no chunk-final word
  shorter than half the median spoken-word duration for that master;
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

## Completeness contract

Added 2026-09-02 after EP007.

An owner listen found the cold open cut off mid-word. Investigation showed **nine of twenty-four
chunks ended mid-final-word**, five losing roughly half a second. Every automated check reported
clean, because the conformity check was forced alignment and forced alignment cannot detect missing
audio.

| Where it is caught | Cost |
|---|---|
| N4B, at capture | one retry |
| N6, at technical pass | a full re-alignment |
| Owner listen | four master revisions and three alignments |

The check is therefore mandatory at **N4B**, and repeated at **N6** against the assembled master.

**Tail energy test.** RMS of a chunk's final 60 ms divided by that chunk's peak RMS. Complete
utterances decay into silence and measure below `0.01` in practice. Observed truncations measured
`0.13` to `0.54`. The threshold is `0.02`.

**Chunk-final word test.** After alignment, no chunk's final word may be shorter than half the median
spoken-word duration for that master. This catches both truncation and over-aggressive trimming.

Truncation from a synthetic provider is **stochastic**: a plain retry usually clears it. When a
passage truncates reliably, generate with a trailing sentinel phrase and trim at the last real word's
**aligned end**, never at a guessed silence. Trimming at "the last silence gap" removed real final
words during the EP007 repair and is prohibited.

## Invalidation rules

- A new Step 1 editorial lock invalidates the Step 2 narration lock.
- A script-hash change invalidates affected direction, takes, edit decisions, conformity, transcript, and handoff.
- Previously recorded takes may be reused only when their complete spoken-word sequence is identical in the new locked script and a written impact review approves reuse.
- A narrator, provider/model, generation-setting, room, microphone, capture-chain, sample-rate, or bit-depth change returns the work to N3 and requires renewed calibration.
- A performance-only creative revision returns to N2/N3; it does not reopen Step 1 while the exact
  approved words remain unchanged.
- A sample-provenance, consent, account-tier, commercial-use, or blind-code failure blocks provider
  selection and cannot be waived by a creative score.
- Materially tuning only one provider, changing a scored `W` range, or unblinding before signed
  scoring invalidates the entire comparison round.
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
- A provider-method selection is neither `technical_pass` nor `creative_approved`. It freezes an N3
  input only.

## Alternate exits

- `blocked`: authorization, technical integrity, or required input is missing.
- `returned_to_editorial`: the locked words or editorial package must change.
- `abandoned`: the episode is cancelled with its history preserved.

There is no `approved_with_hidden_mismatch` state.
