# Shorts runbook v0.1 (derived from EP007)

Status: **approved v0.1 (owner, 2026-09-24).** Reconstructed on 2026-09-23 from the EP007 records listed under each step. Where this file and a record disagree on EP007 facts, the record
wins. Content OS (`../content-os/`) still owns voice, rubric, release gate and schedule.

**Updated 2026-09-24:** presenter generation now follows `blueprint-cinema/references/PRESENTER-RECIPE.md`. Every look is locked per project, K01 + K08 are the standing behavior references, and every paid call goes through `oe-cinema generate` (or its `--dry-run` gate for connector calls). Where Steps 4, 5 and 9 below describe the EP007 specifics (the V5 look, the call-recording behavior clips, one-shot runners), treat them as history. The recipe is the current rule. A Short can now also be made without an episode: see "Standalone Short" at the end.

What it covers: how The Operator Economy made EP007's four net-new, 9:16, avatar-led companion
Shorts, from the rejected crop plan (2026-09-19) to four owner-accepted sound-on cuts (2026-09-23)
and their approved publication copy. Every step lists the EP007 example and where the evidence is.

Short paths used below:

- `NN/` = `studio/originate/exit-readiness-prep/shorts-net-new/`
- `HF/` = `studio/originate/exit-readiness-prep/shorts-hyperframes/`
- `DEC/` = `blueprint-cinema/episodes/EP007-exit-readiness-prep/review/decisions/`
- `EXP/` = `blueprint-cinema/experiments/`

## The standard in one paragraph

Each Short is a new portrait film, not a crop. The first sentence tells a cold viewer the topic,
who the customer is and why they should care. The middle teaches one mechanism. The Short answers
its own narrow question before anything points at the episode. The picture runs presenter, then
full-screen working screens, then presenter again, with no persistent rails. After the answer, a
two-second visual-only card routes to the full episode. Every word is owner-locked before any paid
voice call, and every paid call is capped, single-attempt and receipted.

---

## Step 1. Set the direction (and know the rulings that set it)

EP007 took seven owner rulings to arrive at the standard. Use them as the default; do not re-argue
them per episode.

| # | Ruling (owner words, trimmed) | What it fixed | Record |
|---|---|---|---|
| 1 | "net new shorts. Not just crops of the existing episode" (09-19) | Crop slate of 5 cuts dropped unrendered | `blueprint-cinema/experiments/EP007-NET-NEW-UNFINISHED-ANSWER-003/assembly/r79-full-conform/direction/r79-owner-locked/OWNER-REQUEST.json`, `studio/originate/exit-readiness-prep/shorts-preproduction/README.md` |
| 2 | "needs to lean on my avatar" + research long-form companion Shorts (09-20) | Avatar-led, net-new performances; same V5 identity, fresh speech | `DEC/ep007-paired-companion-owner-direction-20260920.json` |
| 3 | "They still have to be good on their own" (09-20) | Curiosity/cliffhanger paired cuts rejected; standalone payoff required | `DEC/ep007-paired-companion-standalone-feedback-20260920.json` |
| 4 | "whats the context? they dont know that were building a sales readiness practice" (09-21) | Cold-viewer orientation in the first sentence | `DEC/ep007-short01-context-gap-feedback-20260920.json` |
| 5 | "more curiosity and aspirational... bring people in like a conversation", then "More authority" (09-21) | Conversational, confident hook: "You can build a service that..." | `DEC/ep007-short01-conversational-opportunity-feedback-20260921.json`, `DEC/ep007-short01-authority-feedback-20260921.json` |
| 6 | "i dont think my face has to be there through the whole thing" (09-22) | Presenter, then full-screen screens, then presenter (Short 01: 36.65% presenter frames, down from a 60-75% target) | `DEC/ep007-short01-screen-led-middle-feedback-20260922.json` |
| 7 | "do we need the heading through the whole thing? ... less produced" (09-22) | No channel rail, docket or footer over running video | `DEC/ep007-short01-persistent-heading-feedback-20260922.json` |

Plus two lock-ins: the 2-second visual-only end card (`DEC/ep007-short01-end-bridge-approval-20260922.json`,
copy `BUILD THE FULL PRACTICE / SCOPE IT · PRICE IT · TEST IT / WATCH THE FULL EPISODE ↓`), and
"good lock it. let's do the same for the other videos" (`DEC/ep007-short01-clean-frame-owner-lock-20260922.json`),
which made accepted Short 01 the picture reference for Shorts 02-04.

The rubric side: on 2026-09-21 the owner ruled the standalone-payoff rubric governs Shorts
(commit `df33d8df`). `cliffhanger_line` is retired. Briefs need `cold_viewer_context`, exact
`hook_line`/`last_line`, `standalone_payoff`, `pinned_comment`; net-new manifests also bind
`payoff_line` and `closing_line`. Validator: `studio/scripts/originate/shorts_contract.py`.
Pointers: `CLAUDE.md` (Shorts rule), `docs/content-rubric.md:120`, kill list at `:73`.

**Do:** write `SERIES-BIBLE.md` for the slate first (see `NN/SERIES-BIBLE.md`): promise, story
architecture (cold entry, causal reveal, payoff, isolation check, optional depth), format
(1080x1920, 24 fps, 30-75 s), visual language, evidence boundaries.

**Isolation check (use on every script and cut):** delete the episode sentence, the Related Video
cue, the description and the pinned comment. The Short must still set up the situation, mechanism,
consequence and action.

## Step 2. Write, clear and lock the scripts

1. Draft one narrow question per Short, each with a different job. EP007: diagnostic (Thirty-Day
   Map), qualification (Operations Business), commercial/legal boundary (How You Charge), channel
   test (Test the Front Door). Script text: `NN/STANDALONE-SCRIPTS-V3.md`.
2. Write the standalone payoff under each script in one sentence. If you cannot, the Short is not
   finished.
3. Claim clearance against the episode's approved sources, per Short, with a verdict and a
   production boundary (what visuals and labels may not imply). EP007: `NN/CLAIM-CLEARANCE-V1.md`
   (for example, "thirty days" is an illustrative test setting; Short 03 is a directional legal
   warning, not legal clearance).
4. Owner locks the exact words ("Yes lock the scripts and update the gate", 2026-09-22). Record the
   package hash (`6be1ee7c...cf6c`) and log the event (`ep007-four-standalone-scripts-accepted-v6`).
   Any later word change needs a new lock.
5. Run `shorts_contract.py` on the manifest. EP007: `ep007-standalone-shorts-contract-verified-v6`.

Iterating on a no-spend animatic with a scratch voice is cheap and was where most EP007 direction
was found (Short 01 went through v1-v4 animatics on 09-21 before words were locked). Do it before
any paid call. Silent animatics for all four: `ep007-standalone-shorts-animatics-v8`.

## Step 3. Narration chain

Voice identity: the owner's ElevenLabs clone **"Original C"** (voice ID in
`DEC/ep007-owner-authorize-shorts-narration-20260922.json`). Chain proposal and pricing basis:
`NN/NARRATION-CAPTURE-PROPOSAL-V1.md`.

1. **Owner authorizes the batch** with exact call count, caps and zero retries. EP007: 4 guide + 4
   transfer calls, Google cap $0.15, ElevenLabs cap 3,200 credits.
2. **Guide TTS.** Google `gemini-2.5-pro-tts`, voice Algieba, the locked script as input. Runner
   writes an immutable submission intent before the POST and refuses to submit again once an intent
   exists. Output: 24 kHz mono 16-bit WAV plus raw response and receipt. Runners:
   `NN/narration-v3/capture_shorts_v3.py`, `NN/narration-v5/capture_short02_guide.py`,
   `NN/narration-v5/capture_short03_04_guides.py`, `NN/narration-v6/capture_short02_replacement.py`.
3. **Exact-copy ASR QC on the guide.** Two independent local Whisper reads (`small.en`,
   `medium.en`) must match every normalized locked word, in order, with timings inside the
   waveform. Any wrong word is a hold. Example hold: `NN/narration-v5/short-02-operations-business/GUIDE-QC-V1.json`.
4. **Tail check and the tail repair rule.** Measure energy of the final 60 ms relative to peak; it
   must be below 0.02. If it fails but the ending is audibly complete, make a **separate derived
   copy** with at most 500 ms of digital-zero samples appended. Never touch the original samples.
   Re-probe and re-run ASR on the derived copy. Record it (`DERIVED-GUIDE-REPAIR.json`, e.g.
   `NN/narration-v4/short-01-thirty-day-map/DERIVED-GUIDE-REPAIR.json`) and bind the chosen file in
   `GUIDE-TRANSFER-SELECTION.json`. EP007 decision: `ep007-shorts03-04-guide-tail-derived-decision-v4`.
5. **Voice transfer.** ElevenLabs Voice Changer, `eleven_multilingual_sts_v2`, to Original C. One
   attempt per Short. Read account credits before and after (`ELEVEN-ACCOUNT-BEFORE/AFTER.json`);
   the exact credit cost must come back in the response before the next Short proceeds. Runners:
   `NN/narration-v4/transfer_short01_v4.py`, `NN/narration-v5/transfer_shorts_02_04.py` (see
   `NN/narration-v5/ORIGINAL-C-TRANSFER-RUNNER.md`).
6. **Final voice QC.** 48 kHz master; tail pass; both Whisper models match all locked words.
   Example: `NN/narration-v5/short-03-how-you-charge/FINAL-VOICE-QC-V1.json`.
7. **Final word timings.** Forced alignment against the locked words gives the word clock that
   drives avatar segment cuts, scene timing and captions: `FINAL-WORD-TIMINGS-V1.json`.
8. **Owner listening** happens on the finished private video, not on the bare WAV (owner's
   choice for 02-04). Short 01 had a separate A/B listen ("replacement take").

Final masters: Short 01 `NN/narration-v4/.../media/`, Shorts 03-04 `NN/narration-v5/<short>/media/original-c.wav`,
Short 02 `NN/narration-v6/short-02-operations-business/media/original-c.wav`.

## Step 4. Avatar generation (Higgsfield)

Rule set (from `DEC/ep007-owner-start-shorts-production-20260921.json` and
`DEC/ep007-shorts-02-04-avatar-route-owner-choice-20260922.json`):

- Current rule: the Short uses its episode's locked look (`presenter/LOOK-LOCK.json`). A standalone
  Short locks its own (see `PRESENTER-RECIPE.md` §1). EP007 used the V5 look (navy shirt, glasses,
  soft daylit study); that was EP007's look, not a standing one.
- **New speech per Short.** Never put old speaking footage (episode or another Short) under new
  words. Accepting the V5 look does not accept any new take.
- Two presenter shots per Short: an opening and a return. Screens carry the middle.
- Generated footage is illustrative performance, never evidence.

Procedure:

1. **Direction per shot** in `DIRECTION.json`: word range, time range, shot job, one or two earned
   gestures, what stays still, first and last image, protected hold after the last word, review
   question. Example: `EXP/EP007-SHORT01-PRESENTER-001/DIRECTION.json`.
2. **Audio references.** Cut exact PCM slices from the Original C master at near-zero samples
   between aligned words. Pad only with digital zero to the request length (for example 9 s).
   Make an MP3 companion for upload and ASR-check it against the expected words. Examples:
   `EXP/EP007-SHORT02-PRESENTER-001/prepare_audio_refs.py`,
   `EXP/EP007-SHORT03-PRESENTER-001/AUDIO-BOUNDARY-QC-V1.json`. If the slice starts on a rising
   waveform you get a click; Short 04's return moved its start 10.917 ms earlier
   (`EXP/EP007-SHORT04-PRESENTER-001/INPUT-MANIFEST-V2.json`).
3. **Request.** `seedance_2_5`, mode `omni_reference`, 9:16, 1080p, bitrate high,
   `generate_audio: true`, `use_unlim: false`, count 1. Reference roles in order: V5 identity
   image, relaxed-behavior video, public-articulation video, exact segment MP3. Bind prompts and
   hashes in `REQUEST-MANIFEST-V1.json`. *Current:* the reference roles are the locked look still,
   K01, K08 and the exact segment MP3, with the reference sentence from `PRESENTER-RECIPE.md` §3.
4. **Quote and balance readback immediately before submitting.** Record both. Stop if the quote
   plus prior use exceeds the cap.
5. **Submit once.** Record every item, including rejected ones. A rejection without a job ID is a
   stop, not a retry (see Lessons).
6. **Download, probe, full decode, 1 fps contact sheet review** (identity, eyeline, hands, mouth
   closure). Example: `EXP/EP007-SHORT01-PRESENTER-001/GENERATION-RESULTS.json`.

## Step 5. Lip-sync and the restore/offset technique

The model's own speech audio is never delivered. The single continuous Original C WAV is the only
program audio. Picture is placed over it.

- **Offset only (no sync call) when native mouth timing already reads right.** Measure where
  speech starts in the native clip (ASR on its audio) and start the picture at that offset
  against the master. Short 02 used source starts of 0.125 s (opening) and 1.125 s (return) and
  needed no Fal call. Record: `HF/short-02-operations-business-sound-on-v1/renders/SHORT02-PRIVATE-SOUND-ON-QA-V1.json`.
- **Restore with Fal Sync when there is a specific observed mouth-timing error.** Model
  `fal-ai/sync-lipsync/v3`, `sync_mode: silence`, input = generated video URL + exact segment
  audio URL. Write a `SYNC-NEED.json` naming the observed error first; a silent-frame look is not
  enough. One-shot runner with intent-before-POST, pinned CDN host and job UUID, no retry:
  `EXP/EP007-SHORTS03-04-SYNC-001/sync_one_shot.py` and its `README.md`. Short 01 used
  `EXP/EP007-SHORT01-PRESENTER-001/segment-a/sync_restore_audio.py`.
- **Make it browser-safe.** Transcode the restored clip to H.264 High, yuv420p, 1080x1920, 24 fps,
  audio stripped, not retimed, not recropped (`restored-browser-safe.mp4`). Full-decode and hash it.

Used in EP007: Fal on Short 01 (2), Short 03 (2), Short 04 (2); none on Short 02.

## Step 6. HyperFrames 9:16 assembly

One independent HyperFrames project per Short (`HF/short-0N-*-sound-on-v1/`, Short 01 at
`HF/short-01-thirty-day-map-v3/`). Plan: `HF/SHORTS-03-04-SOUND-ON-IMPLEMENTATION-PLAN-V1.md`.

1. **Grammar:** full-bleed presenter opening, subject-specific working screens (not a copy of
   Short 01's worksheet), presenter return for the judgment, 2-second visual-only episode card after
   the last spoken frame. Boundary Ledger 2.0 palette and bundled fonts (see `NN/SERIES-BIBLE.md`).
2. **Retime screens to the real voice.** Derive scene windows and reveal beats from
   `FINAL-WORD-TIMINGS-V1.json`; any voice change reopens every seam. Keep the silent animatic
   untouched as a separate source.
3. **Tracks:** muted presenter video, screen scenes, caption sub-composition on track 60, one
   Original C WAV as the only audio on track 100.
4. **Captions from word timings.** Build with `HF/caption-assembly-scaffold-v1.mjs <plan.json>
   [--check]`. Verbatim overlay rail, phrase-sized cues. Words already shown as exact scene text
   count toward coverage instead of being duplicated. No caption rail on the end card. Do not
   reserve a permanent bottom band.
5. **Render:** `npm run render -- --fps 24 --quality high --workers 1 --strict-all --output renders/<name>.mp4`.
   Extract the poster from the encoded MP4 (EP007 used the 3.5 s frame).

### QA gates (all must pass before the phone preview)

| Gate | Pass condition | EP007 example |
|---|---|---|
| Strict check | HyperFrames check: 0 lint, runtime, layout, motion, contrast findings | Short 01: 39/39 contrast; Short 02: 23/23 |
| Seam gate | Portrait seam checks pass | `HF/short-03-how-you-charge-sound-on-v1/scripts/seam-gate-portrait.mjs` |
| Full decode | Every video and audio frame decodes, exit 0 | all four |
| Exact caption coverage | Every aligned word appears exactly once (rail or exact scene text) | 02: 102/102 rows; 03: 98/98; 04: 126 (101 rail + 25 scene) |
| Program audio comparison | Decoded render audio matches the Original C master at zero lag (02: correlation 0.9997 after AAC); a picture-only revision must leave the decoded audio hash unchanged | Short 01 v24 record |
| Visual review | Encoded contact sheet and seam frames checked; no stale labels or caption collisions | `renders/*contact*.jpg` |

QA records: `HF/short-02-.../renders/SHORT02-PRIVATE-SOUND-ON-QA-V1.json`,
`HF/short-03-.../PRIVATE-REVIEW-QA.json`, `HF/short-04-.../SOUND-ON-ASSEMBLY-RECORD-V1.json`.

## Step 7. Private phone preview

Server: `NN/private-phone-preview/server.cjs`, bindings in `manifest.json`, contract in `README.md`.

- Routes `/short-01` to `/short-04` only. Each slot binds one MP4 and poster by repo path and full
  SHA-256. A null slot shows "No verified video yet". Media URLs carry the hash; changed bytes 404.
- Binds only `127.0.0.1`. Reached from the phone through Tailscale Serve HTTPS on port 3113
  (tailnet only, never Funnel). Tailnet-only mode checks this at startup and fails closed;
  otherwise it requires a 16+ byte password with HTTP Basic auth.
- Byte ranges, `no-store`, manifest read at start (restart after rebinding).
- Smoke test on a spare loopback port before cutover: 401 without auth, `/healthz` state, 206 on a
  range, 416 on a bad range, full-body hash match, 404 on an unbound or made-up hash.
- A manifest edit is not owner acceptance. In-app browser loading is not physical phone playback.

## Step 8. Owner review and acceptance

- Owner watches with sound on the phone. Acceptance binds **exact render hashes only**. It does not
  carry to other Shorts, to later renders, or to release.
- Record the verbatim reply as a source JSON, then append an event to `DEC/events.jsonl`.
  Short 01: `DEC/ep007-short01-clean-frame-owner-accepted-v25.json` ("good lock it").
  Shorts 02-04: `DEC/ep007-shorts02-04-owner-accept-20260923.json` ("im good with the shorts. accept").
- Write down known flaws the owner accepted as-is (EP007: Short 03 brow furrow; Short 04
  ACCESS/DEMAND overlay close to captions; Short 03 opening framed closer than directed).
- Update the production manifest (EP007 final: `NN/PRODUCTION-MANIFEST-V8.json`).

## Step 9. Spend controls

| Control | EP007 practice |
|---|---|
| Per-batch owner authorization | Exact calls, caps, scope and a `not_authorized` list, captured verbatim (`DEC/ep007-owner-authorize-*.json`) |
| Caps | Google $0.15 (then $0.05 for the one Short 02 guide); ElevenLabs 3,200 credits; Higgsfield 1,200-credit quote cap for 6 clips; Fal $15 operational forecast; 3 guide / 3 transfer / 6 avatar / 6 sync calls for Shorts 02-04 |
| No automatic retries | Zero across the project. A failed or uncertain call stops the lane |
| Intent before POST | Every runner writes an immutable intent first; an existing intent blocks resubmission, even after a timeout |
| Over-cap hold | Hold for new owner direction rather than spend (`over_cap_policy` in the 02-04 authorization) |
| Balance readback | Read balance before and after every paid batch; compare the delta to the quotes |
| Recovery | Named, single calls approved one by one (`ep007-shorts02-04-bounded-recovery-decision-v1`) |
| Honesty about limits | Forecast caps are local gates, not provider-enforced; estimates are labelled "not invoice" |

## Step 10. Publication copy and scheduling

Copy: `studio/originate/exit-readiness-prep/content/youtube-shorts.md` (owner-approved 2026-09-23),
machine form `content/shorts_briefs.json` (passes `shorts_contract.py --mode derived`).

- **Titles:** platform titles differ from editorial script labels. No questions, no figures, no
  hashtags. EP007 example: "Map what a business can't do without its owner" (47 chars).
- **Descriptions:** restate the Short's own answer, then "Full episode: {{EPISODE_URL}}", then the
  AI line last: "The narration is an AI voice clone of the host's own voice, and the presenter
  footage is AI-generated."
- **Pinned comments:** open with the episode URL on its own line, then add depth the Short does not
  need. Never supply the Short's answer. The API cannot pin; post and pin in Studio once live.
- **Disclosure:** altered/synthetic content = yes on every Short; `containsSyntheticMedia: true` on
  API uploads.
- **Related Video:** set to the long-form in YouTube Studio, resolved from `launch/links.json`, never
  typed by hand. If the episode is not live yet, leave it empty and backfill on launch day. Read it
  back before calling a Short published.
- **LinkedIn:** the video ends on the complete conclusion; any episode route lives in the post copy.
- **Schedule:** episode Monday 11:00 ET; Shorts Tue-Fri 08:30 ET, one per day (EP007: 2026-10-06 to
  10-09), uploaded as private with `publishAt` by `studio/launch.py ... --go`, which also writes
  `launch/links.json`. Release approval: `DEC/ep007-owner-release-plan-20260923.json`. Steps and
  commands: `studio/originate/exit-readiness-prep/launch/UPLOAD-PLAN.md`; Content OS slot:
  `content-os/flow.md` (Tue-Fri 08:30 row, and failure mode 3, "Shorts pointing nowhere").
- **Order:** `launch.py` schedules by filename. If you want a different order (EP007 copy suggested
  02, 01, 04, 03), re-point the `shorts/short-0N.mp4` symlinks and reorder `shorts_briefs.json`
  before `--go`.

---

## What went wrong / lessons

| Incident | Record | Lesson |
|---|---|---|
| First narration runner failed its own pre-submit audit (artifacts not rebound per call, ASR accepted an unbound transcript, no batch failure latch). Zero calls made. | `NN/narration-v1/REJECTED-PREFLIGHT.json` | Audit runners before the first paid call. Worth the time. |
| Short 01 guide tail energy 0.0357, above 0.02. Batch of 8 stopped after one call. Replacement guide: 0.0361, stopped again. | `ep007-shorts-narration-batch-hold-v10`, `...-hold-v12` | Algieba endings often fail the mechanical tail test while sounding complete. Ask for the lossless 500 ms pad rule in the batch authorization so it does not need a separate round trip. |
| Short 02 guide read "Add a business ready to sell..." instead of "Helping owners get a business ready to sell..." | `NN/narration-v5/short-02-operations-business/GUIDE-QC-V1.json` | TTS can drop or change opening words. Exact-copy ASR on the guide is mandatory, before any transfer. The fix cost a second guide and about 10 hours waiting for approval. |
| Shorts 03-04 guides held on tail energy. | `ep007-shorts03-04-guide-tail-derived-decision-v4` | Same pad rule. Keep the original; bind the derived copy. |
| WhisperX read "the" where the locked word was "to". | Short 03 `FINAL-VOICE-QC-V1.json` | Use two independent model reads. ASR also cannot prove the last phoneme is not clipped. |
| Short 01 Higgsfield use took the balance from 446 to 62 credits; Shorts 02-04 could not be quoted until the owner topped up to 4,062. | `EXP/EP007-SHORT01-PRESENTER-001/GENERATION-RESULTS.json`, `NN/HIGGSFIELD-BALANCE-READBACK-20260923.json` | Check balance against the whole slate's quote before starting, not per Short. |
| Higgsfield batch of 4: 2 accepted, 2 rejected "Out of credits" with no job IDs while 3,858 credits showed. Root cause never confirmed. | `EXP/EP007-SHORT03-PRESENTER-001/GENERATION-BATCH-READ-ONLY-DIAGNOSTIC-V1.json` | A rejection without a job ID is a stop. Do not assume the visible balance means it is safe to resubmit. Each retry needed explicit owner approval. Submit fewer items per batch. |
| 70 Higgsfield credits unattributed (balance fell 154 on an 84-credit quote). Fal charges never read back; Short 01 Fal cost not recorded; Google figures are estimates. | `EXP/EP007-SHORTS03-04-SYNC-001/RECOVERY-RESULTS-20260923.json`, `NN/PRODUCTION-MANIFEST-V8.json` | Credit accounting gap. Read balance before and after each single job, not across concurrent batches. Pull Fal and Google billing after each run. |
| Short 04 return audio slice started on a rising waveform (click risk). | `EXP/EP007-SHORT04-PRESENTER-001/INPUT-MANIFEST-V2.json` | Cut slices at near-zero samples after the previous word's aligned end. |
| Short 03 opening came back closer than directed with incomplete hands; accepted as-is. | `NN/STATUS.json` short_03 | Stochastic takes miss direction. Decide before submitting what is good enough, since retries cost an approval. |
| Presenter-visible target of 60-75% was wrong for the owner; a persistent heading made it feel produced. | `ep007-standalone-shorts-production-v7`, rulings 6-7 | Default to presenter, then screens, then presenter, with a clean frame. |
| Paperwork errors: v14 authorization bound the wrong project (fixed v15); end-card copy lost its "↓" glyph (fixed v17). | `ep007-short01-through-video-generation-authorized-v15`, `...-copy-correction-v17` | Copy exact paths and glyphs from the source record, never from memory. |
| `launch.py` would have uploaded EP006's Shorts from `remotion/out/`. | `launch/UPLOAD-PLAN.md` blocker 4 | Fixed to prefer `originate/<slug>/shorts/`. Check the dry run lists the right four files. |
| Content OS release audit fails `script_missing` for V2 episodes; the owner skipped the gate for EP007 by exception. | `DEC/ep007-owner-release-plan-20260923.json` | The V2 release adapter is still missing. Do not assume the exception carries to the next episode. |

## Costs (from the records)

| Provider | Short 01 | Shorts 02-04 | Total | Basis |
|---|---|---|---|---|
| Google Gemini TTS (Algieba) | 2 calls, ~$0.042 | 4 calls, ~$0.092 (3 first-pass $0.0685 + Short 02 replacement $0.0230) | 6 calls, ~$0.13 | Estimates, not invoices |
| ElevenLabs Voice Changer (Original C) | 503 credits | 1,540 credits (02: 525, 03: 456, 04: 559) | 2,043 credits | Actual, from response headers |
| Higgsfield Seedance 2.5 | 2 jobs, 384 credits | 8 attempts, 6 jobs, 612 quoted, 682 observed balance drop | 8 jobs, ~1,066 credits observed | 70 credits unattributed |
| Fal Sync v3 | 2 calls, cost not recorded | 4 calls, $4.44 forecast | 6 calls | Actual charges not read back |

Cap headroom used for Shorts 02-04: ElevenLabs 1,540 of 3,200; Higgsfield 612 of 1,200 quoted;
Fal $4.44 of $15 forecast. Zero automatic retries. Elapsed time: 2026-09-19 (crop slate dropped)
to 2026-09-23 (all four accepted). Rendered durations: 43.5 s, 45.4 s, 39.6 s, 48.1 s.

## Standalone Short (no episode)

For a Short whose question isn't carried by a published episode. It's the same film standard (cold-viewer opening, one mechanism, answer inside the Short), with these differences:

1. **Claims.** There's no episode evidence to inherit. Every number and factual claim needs its own source cleared in Content OS `facts.md` before the script locks.
2. **Script.** It must pass `shorts_contract.py` in direct mode. `pinned_comment` and `episode_bridge_line` are optional. The end card routes to the channel, a playlist or the newsletter instead of an episode, and that target is written into the script lock.
3. **Look.** Lock one with `oe-cinema lock-look` in the Short's own project folder (`PRESENTER-RECIPE.md` §1). Reusing the latest episode's look is allowed only if the owner says so at lock time.
4. **Voice, presenter, screens.** Steps 3 to 6 above, with the presenter per `PRESENTER-RECIPE.md` and paid calls through `oe-cinema generate`. Screens are built from the Short's own cleared sources. Generated film follows the Kling / Veo split in `docs/blueprint-cinema.md`, and stock footage comes from `source_footage.py`.
5. **Review, schedule.** Steps 7, 8 and 10. The publication copy links the end-card target, not an episode.

Owner authorization for spend is still per batch (Step 9).

## Open items (the runbook is approved; these remain)

- ~~Owner approval of this runbook.~~ Approved 2026-09-24.
- A Content OS release adapter for Blueprint Cinema (V2) episodes.
- A billing readback step for Fal and Google, and per-job Higgsfield charges.
- Decide whether the 500 ms pad rule and one pre-approved retry per shot should be standing policy.
