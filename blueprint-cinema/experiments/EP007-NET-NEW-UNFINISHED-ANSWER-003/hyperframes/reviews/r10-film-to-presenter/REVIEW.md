# R10 handoff review

September 8, 2026. Owner-requested isolated Studio review; no final render or production approval.

Preview (use Chrome for this review): http://localhost:3020/?review=r10-chrome#project/r10-film-to-presenter?v=1&t=21&tab=design&rc=0

## What changed

R8 A–C and R9 D are byte-identical with the same source windows and record timings (580 frames). R9's grid is replaced by E's shared aftermath. The next four seconds preserve the silent identity interval with the established wordmark treatment. A newly generated exact-introduction presenter take uses the user-selected Test Q image, motion prompt and settings. Q's earlier scope-test mouth footage is not reused.

The narration remains continuous and sample-exact from master10.920–74.086667,1,516 frames at24fps. This controlled comparison retains the prior test start; it is not the full opening with arrival or first10.920 seconds. The later S08 model is located in STORYBOARD.md but has not been rebuilt or silently inserted into this passage.

## Verification

- `node verify-r10.mjs`: preserved sources and selections, gap-free frame coverage, full source decode, available source handles, exact narration PCM, Q recipe equality and output timing pass. See `renders/verification.json` and `ASSET-MANIFEST.json`.
- Bundled Python `check-sync.py`: exact-intro returned audio matches input in1–7,10–16 and19–25s windows with correlations0.99860–0.99896; stable23ms delay, no detected drift. Muted picture source is advanced23ms over the exact master. Final spoken word remains covered. This is not a visual phoneme-sync approval.
- `node qa-runtime.mjs`: pinned HyperFrames0.8.31,20 sampled times including seams and final included frame, zero lint/runtime/layout/motion/contrast findings; source unchanged across check. See `renders/runtime-check.json`.
- Fresh upgrade check confirms pins are current. Repo-managed skills were preserved, not globally refreshed.
- Managed preview runs on port3020; status and HTTP200 verified. In-app Studio was opened, playback started with narration unmuted, and a live presenter frame at local46s was inspected. Technical snapshots include film, identity and final presenter frame. This does not claim a fresh human-like full-speed listening/lip-sync verdict.
- Independent read-only avatar availability and new-plates QA packets were validated by root for schemas, current hashes, owned outputs and no approval/state-change claims. Work orders closed without advancing production gates.

## Performance watchpoints

Live preview limitation: the in-app browser shows the presenter image at local0,21 and28 despite its DOM/timeline selecting the correct film shot. Restarting playback and a fresh localhost/127.0.0.1 navigation did not clear it. Root verified that Chrome shows the correct owner close-up at21 and shared aftermath at28, consistent with technical snapshots. Chrome is left paused at28 for owner review. This is isolated to the inspected in-app playback surface; underlying cause is not established. Do not approve the in-app visual as if it represents the edit. Chrome is the current review surface; no runtime or composition workaround was invented and no public issue was filed. A final runtime recheck after Studio assigned persistent element IDs passes with current source hashes matching both the runtime report and asset manifest.

E's lips part once around source0.5 and remain partly open until4.5, closing by4.75. Dense frame review finds no repeated speech articulation. This is reasonably previewed as a prolonged settling pause, but it does not perfectly obey the requested two-second breath or continuously closed mouth. Hands regroup slightly. Keep for owner playback; no extra paid retry was made. If it reads as another answer, the late closed-mouth portion alone is too short to fill the current edit.

The Q-derived introduction retains identity, study, glasses, navy shirt and visible hands in sampled early/middle/late frames. Hand beats recur; chin lifts near source3 and18s. The exact short Q performance cannot be duplicated by a new generation. Mouth accuracy, emphasis and naturalness remain owner playback questions.

## Scope and costs

One built-in continuity image edit, one10-second silent Kling v3 Pro request (`01a0821c-a564-7561-9025-98caafa1eb3e`, listed estimate$1.12), and one25.980-second Avatar IV introduction (`544100f6654f580746c112f8f48e18ac`) using existing Creator credits. Actual invoices/credit consumption are not attributed or independently reconciled. No plan change, credit purchase, retries, grade, music, effects, voice rewrite, arrival pre-roll, S08 model rebuild, commit, push, final MP4, publication or canonical gate change. The separate presenter experiment remains untouched by this task.

Film is AI-generated dramatization; presenter is an authorized AI avatar. Neither supplies factual evidence of an actual buyer-owner case. Release disclosure remains a separate governed requirement.
