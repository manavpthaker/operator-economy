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
