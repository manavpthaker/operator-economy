# R8 direction verification and review resolution

2026-09-08. Outcome: proposed coverage packet checked; media generation, audiovisual acceptance and the four-second timing change remain unperformed.

## Checks performed

- Nine current source hashes match SOURCE-CUES.json, including the locked script, transcript, narration WAV, R7 composition, reference stills, presenter record and film-direction skill.
- All 191 selected word objects match the transcript exactly. The transcript's master hash matches the pinned WAV.
- Seven principal cue anchors and the complete 408-frame trial were checked. Cuts remain local frames 92 and 242; selected durations are 3.833333, 6.250000 and 6.916667 seconds. No narration time change.
- Proposed B/C source windows fit their proposed source budgets with handles. These are arithmetic checks, not provider capability or performance guarantees.
- The four-second full-opening offsets and avatar W000118–W000190 / 48.520–74.000 interval were independently checked.
- Work-order and deliverable schemas passed; independent input pins matched before the review work order was closed.
- Root rechecked source pins and corrected contract vocabulary after review. No complete canonical scene-direction validation is claimed.
- Authored packet files passed newline/trailing-whitespace checks before the small review corrections; the final check was repeated on all four packet files.

## Independent review and root resolution

See [independent report](../../../../episodes/EP007-exit-readiness-prep/agents/deliverables/ep007-r8-coverage-review-20260908/report.md).

The report and closed work order refer to the initial frozen packet hashes, printed in that report. They are historical pre-correction review records, not a claim to have independently reviewed the final bytes below.

- R8-01 corrected by root: use picture_audio_contract.mode, language_carrier, visible_speech, coverage_grammar and face_function. Avatar mode is presenter_address, with visible_speech required and face_function presenter_delivery. The intended synchronized-audio requirement is unchanged.
- R8-02 carried forward: only about seven frames establish the owner's readiness before the answer narration. This is a playback watchpoint, not a proven defect. Keep the initial cuts; if readiness does not read, test an earlier entry after the buyer's question and recalculate source trims.
- The independent reviewer found no blocking chronology, continuity-plan or scope problem. Actual generated start frames, performances and edited seams remain unreviewed because they do not exist yet.

## Final packet hashes

| File | SHA-256 |
| --- | --- |
| DIRECTION.md | `1a0493c94119ce08962593a923b0d8b74fb6c7118364d28d8e13e98c0da5ee1c` |
| GENERATION-BRIEFS.md | `9e37cdc234cd3d1c69586c7ab50fd5f6612444dff781ee187b9ef13d4793ae2b` |
| SOURCE-CUES.json | `c1f4d14e6eb542fa78cfd6408e55353210d80c87e242574fdcc037b9b656efcc` |

The preserved R7 index remains `78d869c031297d453fde1f3439fda8e847d9fec250447ae3a21e4453d1c98f6b`. No new preview, media generation, provider call, canonical episode-state change, release approval, commit or push occurred in this planning task.
