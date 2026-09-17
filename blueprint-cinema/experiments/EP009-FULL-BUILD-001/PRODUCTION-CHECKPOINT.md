# EP009 production checkpoint — r3 verified; avatar revision in progress, 2026-09-17

Current review: http://localhost:3070/ep009-r3-review.html. Full r3 is encoded, loaded in the browser, and technically verified. New avatar-first opening and presenter replacements are not yet integrated.

## Owner locks

Owner: “the brand pause and corrected experience are good - lock those.” Exact scoped acceptance and protected hashes: `direction/r3-owner-revisions/OWNER-LOCK.json`. Shortened brand pause and corrected spoken wording/timing are frozen. Final presenter pictures, new film and release are separate.

## Completed r3

- Full video: `assembly/qa/r3/ep009-full-r3-review-draft.mp4`; SHA256 `16a065294110e0bbb86b49a2f3901cd2c605a919864fcd470f4af06c19bcc9b7`. Runtime 20:21.791667 (20:22), 29,323 frames at 24 fps, 1280×720.
- Brand: removed 78 frames / 3.25 seconds of literal silence, preserving full reveal and speech.
- Corrected P08: “I spent ten years in hospitality, including Ace Hotel and Standard Hotels. I know this business from the inside out. I haven't sold this particular service, though. What a thirty room inn will pay for it is still something I'd have to test.” All 43 words verified; selected audio padded by 1,661 zero samples to 343 frames, without retiming.
- Six generated film inserts add 34.291667 seconds at 6:33, 10:15, 12:22, 12:30, 14:01 and 17:51. Actions: owner on desk phone; monthly report; bring reports together; test guest path on phone; inspect unresolved report; write down owner answer. Total actual film coverage is 77.666667 seconds. `film/r3-workflow/FILM-SELECTS.json` is authoritative. First phone take rejected for invented interface details; only `final-r2.mp4` selected.
- Selected master: `assembly/r3/narration-master-r3.wav`, SHA256 `0f0d5d326262813cb5ff5392fb263f15f6a8e871ad22e54c1274ff974037ca85`. Original source master preserved. `TIMEMAP.json` and `word-transcript-r3.json` map all 75 rows, retaining unchanged words and IDs.
- Full frame decode, master/audio comparison, independent timing and source mapping, and 44 encoded integration frames passed. See `assembly/r3/FULL-QA.md`, exact verification JSON, both independent audits and browser verification. These checks do not certify uninterrupted normal-speed audiovisual quality or final lip sync.
- Current r3 picture retains 14 r1 presenter segments and a labeled L3 still for corrected P08. Old speaking P08 is never paired with the new wording.
- `content-os` commit `bb3f624` records the owner fact correction; unrelated existing edits preserved.

## Current next work: avatar-first opening and remaining presenters

Owner asked why EP009 did not start with the avatar like EP007, then agreed to the proposal: avatar delivers the unchanged first sentence, then cut to inn footage. Source: `review/source-records/2026-09-17-owner-avatar-first-opening.json` in the canonical EP009 episode. `direction/r3-owner-revisions/OPENING-PRECEDENT-AUDIT.md` records the missed EP007 owner precedent. This is approved direction, not approval of unseen generated footage.

The former Fal balance block cleared on a fresh check. P01a restoration was submitted successfully as request `01a0b0ca-13f8-7a02-9854-07943b000e18`, estimated $0.5668, within the existing $30 allowance. Its successful restoration/review and P01b recovery precede wider presenter generation. Reconcile the current `P01a/fal/`, `P01b/fal/` and presenter-regeneration ledger before resuming; do not repeat an existing intent.

Old P08a/b/c remain invalidated in `presenter-regen/ACTIVE-PLAN.json`. Retired `BATCH-REQUESTS-r3.json` has no runnable requests; original bytes retained under `superseded/`. Do not submit that batch. Two corrected P08 parts are prepared offline under `narration-revisions/r3-hospitality/presenter-prep/PLAN.json`. The new P00 opening plan is being prepared under `presenter-regen/opening-first-sentence/`. Revised r5 execution bindings and the pilot review must be complete before activation/submission.

## Spend

- New workflow generation consumed 101.5 Higgsfield credits, including one rejected phone take and one successful retry. Live balance reconciled 1,719 → 1,617.5 before any new presenter jobs. Original production allowance: 1,993.5 / 2,000 credits, 6.5 remaining. No cap increase.
- Separate presenter regeneration: 191 credits spent before new work; 1,800 credit cap unchanged. Replacing old three-part P08 with two parts reduces remaining planned generation from 1,607 to 1,526 credits. P00 must fit the 83-credit remaining plan contingency. Provider preflight and live balance still apply.
- Narration pickup: one Google Algieba guide (estimated $0.0103965) and one Eleven Original C transfer (173 reported credits), no retries.

No Resolve finish, whole-episode acceptance or publication approval. Earlier artifacts are retained. The following r2 checkpoint is historical and superseded wherever the current section differs.

## Earlier r2 checkpoint — retained context


# EP009 production checkpoint — 2026-09-17

Current output: **r2 graphics-only review draft**, not the final episode. All 15 presenter segments in this full cut still use r1 footage.

- Review: http://localhost:3070/ep009-r2-review.html
- Video: `assembly/qa/ep009-full-r2-graphics-only-draft.mp4`
- Video SHA256: `9b279403e6b2c1ef365d086110b8be5b2621315cb98af6e07b257740601857e3`
- Evidence: `assembly/BUILD-r2-graphics-only-draft.json`, `VERIFICATION-r2-graphics-only-draft.json`, `QA-r2-graphics-only-draft.md`.

## Completed

1. Repaired S17's overlapping cost/hours note and made the opening/S05 booking-site drawing consistent with the later scenes. Three new plates are integrated; r1 artifacts remain intact.
2. Verified the complete 29,607-frame cut and locked narration; inspected 103 encoded frames spanning repaired cues and boundaries. Browser preview and economics jump visibly load. This does not certify full-speed comprehension or lip sync.
3. Verified all original 21 planned narration excerpts sample-for-sample against the master and uploaded the remaining 20 guidance tracks with independent remote hash checks.
4. Isolated provider failures to the Rebecca behavior reference. Fresh identical upload and normalized-container tests also failed. Henry-only generation works; the cause of Rebecca failure remains unknown.
5. Corrected the prepared plan's P11a generation from 13 to 12 seconds to honor the owner limit. Original plan retained; selected plan and execution artifacts have explicit hash bindings.

## Presenter recovery

The locked look is original L3 chambray in the inn breakfast room. The whole P01 Henry-only pilot completed, but its second sentence slowed relative to the master. Its measured spread is 0.92 seconds; no whole-take Fal restoration was attempted.

P01a reuses the original-speed first sentence: source frames [0,108), 4.50 seconds. It passes native timing at 0.25/0.25/0.25 seconds; a six-frame trim yields 4.251 seconds. Its narration is exactly master samples [2414000,2612000), 4.125 seconds. The retained source and its derivation remain bound separately from restoration audio.

P01b is a bounded short-question retake: 5.041667 seconds of original narration, seven-second generation, 720p, 45.5 credits. Its job **0f68d221-5876-4ee7-9f2d-cc7d1cfc7198** completed. Native timing offsets are **0.78/0.65/0.69 seconds**, spread **0.13 seconds**; the unchanged 0.30-second drift gate passes. A 17-frame trim yields 6.333008 seconds. Lip-sync restoration and its evaluation remain pending. The selected plan splits at master frame 1306/sample 2612000 and changes W to M there; the segment remains 220 frames.

Authoritative selected plan: `presenter-regen/ACTIVE-PLAN.json` → `EXECUTION-PLAN-r4.json`. Original `TAKE-PLAN.json` and the failed whole P01 are preserved. `BATCH-REQUESTS-r3.json` binds all20remaining requests to the currentr4plan; requests are preparation only; they must not run until the recovered pilot has been evaluated.

## Blocking provider condition

Fal returned HTTP 403, **"User is locked. Reason: Exhausted balance"**, during P01a storage upload initiation. This occurred before a generation submission or paid intent. No Fal job exists for P01a and no Fal charge was incurred in this continuation. Evidence: `presenter-regen/P01a/fal/BLOCKED.json`.

The user was asked to fund the already-authorized $30 at https://fal.ai/dashboard/billing. Production authorization does not establish an available provider balance. Do not submit the remaining 20 Higgsfield takes while restoration is blocked.

## Budget and resume

- Presenter-regeneration authority: 1,800 Higgsfield credits + $30 Fal.
- Look: 50 credits. Successful diagnostics: 24 credits. Whole P01: 71.5 credits. P01b: 45.5 credits completed. Total net regeneration spend to date: **191 credits**. Other failed provider jobs refunded.
- Remaining 20 takes: 1,607 credits. Projected lane total if all remaining jobs succeed: **1,798 credits**, leaving **2 credits**. Further paid retries require a new bounded budget decision; no automatic spending beyond the cap.
- Ledger: `ledger/presenter-regen.jsonl`. Reconcile terminal job results before relying on totals.
- Python runtime: `/tmp/claude-501/-Users-brownmanbrain-GitHub-operator-economy/82de42ec-ae77-42eb-8a88-f56e54114dda/scratchpad/syncenv/bin/python`.
- Helper: `presenter-regen/_tools/regen.py`. After funding, run `fal-submit P01a` only after verifying `SUBMISSION-INTENT.json` and `JOB.json` remain absent. Complete result, alignment, diagnostic gate and scoped review before wider generation.
- Full assembly builder refuses incomplete presenter replacements. Use `assembly/_tools/build_r2.py --mode full-review` only after all 15 are explicitly review-ready; use a new output revision if a prior output exists.

Unresolved creative review notes remain visible: opening film cuts, late F08 reversed movement, and the long second-half model passage. No new restructuring, Resolve finish, owner acceptance or publication approval has been claimed.
