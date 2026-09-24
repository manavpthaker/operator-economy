# Narration Lock

Template version: proposed Step 2 v0.2.

## Episode and authority

- Episode:
- Step 1 editorial-lock revision/hash:
- Locked script revision/hash:
- Ordered `W`-token count/SHA-256:
- Step 2 narration-lock revision:
- Approval date:

## Locked artifacts

| Artifact | Path | SHA-256 | Required identity |
| --- | --- | --- | --- |
| Performance direction | | | revision |
| Voice-and-capture lock | | | revision |
| Calibration authorization | | | consumed for N4A only |
| Calibration review | | | N4A owner-approved |
| Full-capture authorization | | | consumed for N4B only |
| Full-capture review | | | N4B passed |
| Raw-take register | | | complete |
| Pickup log | | | resolved |
| Narration edit decision list | | | edit revision |
| Narration master WAV | | | duration; 48 kHz; 24-bit; mono |
| Source-format conversion record | | | truthful acquisition lineage |
| Lexical-conformity report | | | zero unresolved mismatches |
| Word-level transcript | | | master hash and duration match |
| Intentional-pause map | | | master hash and duration match |
| Technical measurements | | | pass |
| Independent-listener review | | | pass/recommendation |
| Owner creative-approval record | | | same master hash |
| Narration state | | | N1-N7 passed; locked |

## Final measurements

- Duration:
- Sample rate:
- Bit depth:
- Channels:
- Integrated loudness, diagnostic only:
- Loudness range:
- True peak:
- Clipping detected: no / yes
- Audio origin: `native_pcm` / `lossy_mp3` / mixed sources
- Delivery lineage: native PCM / PCM derived from disclosed lossy source
- Lossy-source exception, if present: `mp3_44100_192` with `pcm_capability_unavailable`

## Gate results

- N1 editorial handoff: pending / passed / failed / invalidated
- N2 performance direction: pending / passed / failed / invalidated
- N3 identity and acquisition configuration: passed / failed
- N4A calibration technical and owner decision: pending / passed / failed / invalidated
- N4B full capture: pending / passed / failed / invalidated
- N4 aggregate machine gate: pending / passed / failed / invalidated
- N5 selects, pickups, and edit: pending / passed / failed / invalidated
- N6 exact-master `technical_pass`: true / false
- N7 independent listen and owner `creative_approved`: true / false
- Unresolved caveats:

## Owner lock decision

- `technical_pass` is current for exact master: true / false
- `creative_approved` is current for exact master: true / false
- N7 gate result: pending / passed / failed / invalidated
- Workflow status: locked / in_progress / blocked / returned_to_editorial / abandoned
- Owner:
- Approval statement/date:

## Invalidation acknowledgment

- A new Step 1 editorial lock invalidates this lock: acknowledged / not acknowledged
- Any sample-level master change invalidates alignment, conformity, transcript, pause map,
  `technical_pass`, `creative_approved`, this lock, and Step 3 timing: acknowledged / not acknowledged
- Step 3 may not retime speech, choose alternate takes, or replace the narrator: acknowledged / not acknowledged

An export, hash, automated pass, technical pass, or reviewer recommendation does not replace the
explicit owner creative decision.
