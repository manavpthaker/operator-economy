# EP007 R8 coverage review

Reviewer: independent `qa_reviewer`, 2026-09-08. Work order: `ep007-r8-coverage-review-20260908`.

Scope: frozen prose direction, two draft generation briefs and source-cue packet. No media generation, edit, audio playback, canonical validation or production approval.

## Result

The coverage logic is coherent: retain rapport in A, locate the question in B, enter C before the attempted answer, and protect the interruption. The full opening is explicitly a separate timing proposal with missing plates and authorization requirements, not a build-ready package. Correct the picture/audio vocabulary before handoff; the remaining performance concern requires the actual generated audiovisual test.

## Findings

### R8-01 — Major: use canonical picture/audio vocabulary in the handoff

Location: `DIRECTION.md`, Picture/audio contract. The frozen packet uses `picture_audio_mode`, `visible_speech_policy`, and `coverage_policy`, and describes the avatar as a `presenter_delivery` passage. These can be miscopied downstream despite the packet's prose-only status. The canonical contract uses `picture_audio_contract.mode`, `visible_speech`, `coverage_grammar`, and `face_function`; the avatar mode is `presenter_address`, with `presenter_delivery` as its face function. The intended film mode itself is correct.

Owner: orchestrator. Disposition: open in these frozen bytes; root independently identified this vocabulary issue during the review and intends a subsequent correction. Do not describe this report as reviewing the corrected bytes without a new verification record.

### R8-02 — Observation: owner readiness has little isolated screen time

Location: shot C, local cut frame 242 / master 21.003333. The proposed answer begins near 21.280, leaving 0.276667 seconds, approximately seven frames, of readiness before the answer. Prior shared rapport helps, so this is not a demonstrated timing defect. However, a fresh closer perspective and a newly starting performance may make that baseline too brief to register.

Owner: director/editor at the authorized audiovisual test. Disposition: monitor the existing explicit review question. If confidence reads only after the mouth begins or if she looks worried immediately, first test an earlier owner entry after the question ends at 20.340; do not move the interruption earlier or shorten the narration. For example, local frame 230 gives master 20.503333 and 0.776667 seconds before the answer. This is a conditional alternative, not a changed edit decision or approval.

## Verified

- Three work-order input hashes match. All nine source hashes in `SOURCE-CUES.json` match the current files, including the narration master, R7 composition and references.
- All 191 selected word objects exactly match source IDs, tokens, starts and ends; the transcript's master hash agrees with the pinned WAV.
- Frame coverage is contiguous: 92 + 150 + 166 = 408 frames at 24 fps, exactly 17 seconds. Master interval remains 10.920–27.920.
- B's proposed selected source span is 6.250 seconds. C's is 6.916667 seconds; its source stop window 5.506667–6.546667 correctly maps to master 25.760–26.800. Both proposed source budgets retain handles. Actual usable performance is explicitly unverified.
- The owner interruption can land inside the specified stop window without changing the master. The test retains at least 1.120 seconds after the latest edge of that window. No cut is prescribed during the turn.
- The +4-second opening mapping is arithmetically consistent. Pre-roll is conditional on owner timing approval; the unchanged-clock alternative begins already seated. Meeting history, price consequences and buyer hostility are not invented.
- The full opening separately names missing arrival/establishment, longer owner hold, aftermath and avatar coverage. The two-plate test is not presented as supplying those assets. The long C hold is not represented as a freeze, loop or stretch of the short take.
- Avatar word range W000118–W000190 is exactly 48.520–74.000. Existing later-paragraph footage is explicitly a look reference, not a synchronized opening source.
- Inspection of pinned A start and A continuity-10.5 stills confirms owner-left/buyer-right, reciprocal gaze, wardrobe, workshop light and table-prop geography described in the plan. These are stills, not proof of motion continuity. New B/C reference review and actual seams remain required.
- Dramatization allows illustrative conversational movement while preserving narrator meaning, silent generated output and synthetic disclosure. No new equation, drawing action or paper-to-screen implication is introduced.

## Evidence and limits

Frozen inputs (paths relative to `blueprint-cinema/`):

| Artifact | SHA-256 |
| --- | --- |
| `experiments/EP007-NET-NEW-UNFINISHED-ANSWER-003/direction/r8-context-coverage/DIRECTION.md` | `56e3158a5108c6bbfdc66b3e1daf9338001d3e710fd29ef1f4a85954ac1c4c48` |
| `experiments/EP007-NET-NEW-UNFINISHED-ANSWER-003/direction/r8-context-coverage/GENERATION-BRIEFS.md` | `b3687e0d407a4e47ee1452e59c1e0d4db4baf410ef748fec0337593b6522d43f` |
| `experiments/EP007-NET-NEW-UNFINISHED-ANSWER-003/direction/r8-context-coverage/SOURCE-CUES.json` | `c1f4d14e6eb542fa78cfd6408e55353210d80c87e242574fdcc037b9b656efcc` |

Passes: local SHA-256 recomputation, exact JSON word-object comparison, frame/trim/offset arithmetic, prose contract review, and local still display. No external sources, provider calls, synthetic generation, video playback, new preview, canonical-state change or approval claim. Schema validation of the deliverable records its structure only.

Recommendation: correct R8-01, retain the packet as proposed direction, and carry R8-02 into the authorized audiovisual test. Four-second pre-roll approval, start-frame selection, provider scope/cost and eventual footage acceptance remain unresolved owner/review decisions.
