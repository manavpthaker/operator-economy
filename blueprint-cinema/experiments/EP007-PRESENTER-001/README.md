# EP007 presenter inserts

**Current avatar lock, September 11: V5 is owner accepted.** Use [the V5 acceptance and exact artifact pins](avatar-v5-gestures/ACCEPTANCE.json) and [its performance baseline](avatar-v5-gestures/PERFORMANCE-BASELINE.md). The lock includes the wide seated framing, visible hand movement, clear articulation, relaxed delivery and brief eye movement/look-away. Future gestures may vary with the passage's context. V5 preserves the complementary Rebecca/Henry references and original narration restoration. It supersedes V3 as the current overall avatar baseline; prior locks and experiments below remain historical records.

Latest September 9 owner direction: **Seedance 2.5 is the chosen presenter model and performance direction.** The owner supplied the live mobile review at `http://192.168.1.159:57355/`, verified as the separate `EP007-PREMIUM-CONTROLLED-004` experiment. Its performance reference is test **404**, generated through Higgsfield; the original-voiceover candidate is **407**, a Sync 3 pass on 404 already used in that experiment's opening test. The native 404 audio differs from the supplied recording, so the original narration remains authoritative. See [the exact selection and source hashes](seedance-selection-2026-09-09.json). This replaces the prior InfiniteTalk preference; it does not infer a separate final lip-sync verdict or whole-episode approval.

Earlier September 9: InfiniteTalk was the preferred model family from the four-sample comparison, followed by a requested Seedance 2.5 comparison. The first exact Seedance 2.5 reference-to-video request on fal was rejected by its real-person-likeness policy, producing no video. The second sample was not submitted. See `repair-r24/owner-preference.json`, `repair-r24/comparison-plan.json` and `repair-r24/STATUS.md`. This remains the history of that specific fal attempt, not the later-linked successful Higgsfield result. Existing InfiniteTalk clips are preserved.

Current direction, September 8: **Four native fal comparison clips are ready for owner review: two OmniHuman 1.5 and two InfiniteTalk.** Open [the new comparison](repair-r23/comparison.html). All four use the existing study photo and exact 5.600-second input audio; uploaded bytes were verified. OmniHuman returns 5.640-second picture / 5.600-second audio; InfiniteTalk returns 5.480 seconds, omitting only a near-silent audio tail. All four pass decode and measured audio-timing checks; naturalness and visual lip sync still require owner playback. See `repair-r23/STATUS.md` for results and preserved setup failures. Further head scaling/warping is discontinued. T remains preserved and is not accepted as final. The earlier research proposal is retained in `repair-r22/`.

Earlier, September 8: **T removes all added head scaling and rotation**, using a gentler position correction directly from Q; see `repair-r21/`. The owner rejected S because the head appeared to zoom in and out. S's changing scale and stronger head correction introduced that artifact; its numerical reduction in movement did not establish naturalness. T preserves the original facial performance, voice, timing and hands while retaining more of Q's original head movement. The owner subsequently requested more restrained motion and the methods review above.

R's narrower correction of Q's head dip on “straight” remains preserved in `repair-r19/`. Its initial broad warp bent the shelf and was rejected; foreground isolation resolved that defect. The owner subsequently requested subtler movement throughout.

**Test M remains the historically owner-accepted mouth/head baseline** for the restored navy-shirt study appearance. N did not produce visible gestures. O established hands but overemphasized “straight” and “never”; the owner clarified that the concern is mainly mouth/head movement. P's stricter prompt did not produce a decisive improvement. Q reused M's exact motion prompt with O's wider source and received the better-but-still-too-much-head feedback. See `repair-r14/` through `repair-r18/`. All source files remain preserved; no short-test result approves a full episode render.

K was rejected for word/mouth mismatch and exaggerated head movement. Its Avatar III look exposes a saved Avatar IV motion clip. L's stationary-source Precision Lipsync diagnostic returned no useful mouth animation and is rejected. See `repair-r12/` and `repair-r13/`. Numerical audio checks do not override owner playback judgments.

## Prior original-footage composite route

Status: The owner reviewed F and said, “yes this is much better.” Avatar III with the original video look is the working presenter route. G extends it to the full 30.640-second scope passage. J blends that performance into the landscape study with diffuse room lighting, softer background focus, and a narrower soft cutout edge; see `repair-r10/`. It preserves I's facial frames, narration, framing, and measured shoulder movement. J is rendered at 1080p for owner playback. The study and outer shoulders are synthetic; the moving face and original shirt center come from G. Faint contour and fabric differences remain. Raw training footage remains unverified. This is not final episode approval.

## Prior composite result

Landscape study review: `media/repair-r10/test-j-landscape-study-blended-1080p.mp4`, 1920×1080, 25fps, 30.600s picture / 30.636s audio. The alpha foreground preserves all 765 source-crop RGB frames and timestamps exactly before scaling/compression; final audio is bitstream-identical to G. Current status: `repair-r10/status.json`. Editable HyperFrames project: `study-composite-r10/`. H and I remain preserved in `repair-r8/` and `repair-r9/` for comparison.

Preferred short performance: [Test F — Original footage Avatar III](https://app.heygen.com/videos/3c6cac5f02c74651a7169b3c9ae9a6a0), `media/repair-r6/test-f-original-footage-avatar-iii-1080p.mp4`. Full-passage validation: [Test G — Full scope Avatar III](https://app.heygen.com/videos/be8d5adb5da248c2bad7b18eb24ecdc7), with current render/review state in `repair-r7/status.json`.

The preferred performance remains a comparison reference. Its original outfit and facial pixels are not a constraint on new appearance tests. The intended final image remains a complete landscape study scene; the original portrait with curtains is a diagnostic control.

## First test (historical)

The first presenter test is rendered: `media/presenter-02-scope-heygen-v001.mp4`. HeyGen project: [EP007 — Presenter study — scope test v001](https://app.heygen.com/videos/b40e62b91ed94508b5dff23c6bd78766). This is a production-preview locator; it does not state an episode release URL. HeyGen sharing permissions were not changed or independently audited.

The generated study look is `media/study-look-candidate-03.webp`, candidate 3 from one three-look request. The preview uses Avatar V and the uploaded master excerpt, with Voice Mirroring off. Export is 1280×720 at 25 fps and carries repeated HeyGen watermarks. 1080p and custom motion prompted for an upgrade; no subscription was purchased. Motion therefore uses the available default performance.

Technical checks: the picture is 30.600 seconds, container 30.624 seconds, and input audio 30.640 seconds. The final selected word ends at local 30.390 seconds, within the delivered picture. Returned audio has a 23 ms delay and a 0.999115 delay-aligned waveform correlation to the input, consistent with the same narration after encoding. Account for that offset during final sync review; do not assume the provider re-encoding is sample-exact. Keep the original continuous master as final audio authority.

Sampled frames retain the set, shirt, glasses, and framing. The owner's subsequent playback review rejected the mouth movement and emotional performance. The numerical audio result above does not override that verdict: it verifies audio provenance, not lip-sync or acting. This preview does not clear production quality or the final episode placements. See `heygen-session.json`, `technical-review.json`, and `repair-r2/` for provenance and repair status.

Owner-provided HeyGen avatar/group ID: `cc6abe9744e74df7a103b7a37262d2f7`.
Live verification: the signed-in HeyGen account resolves this exact ID to `brown Man`, with one original vertical close-up video look against curtains and three generated study photo looks. The original video look ID is `b495d299cea544608fc2fc249d055b87`, verified from the selected-look UI URL and thumbnail asset path during R4. The group ID is not the individual look ID.

Owner selected: **Create a landscape, chest-up look in a restrained study setting.**

## Four media lanes

1. Animation and illustration explain the operating model.
2. Presenter address carries personal judgment, limits, and the verdict.
3. Cinematic footage carries physical action, pressure, and consequence.
4. Evidence and screen material substantiate claims using actual sources, documents, charts, and interfaces.

## Candidate edit

| ID | Locked word range | Episode time | Purpose |
|---|---|---|---|
| presenter-01-introduction | W000118–W000190 | 00:48.520–01:14.000 | Introduce the show and episode promise |
| presenter-02-scope | W001663–W001754 | 09:51.300–10:21.440 | State the presenter's personal experience and limits; first test |
| presenter-03-model-caveat | W002522–W002561 | 14:51.280–15:05.640 | Own the economic model's assumptions before showing arithmetic |
| presenter-04-verdict | W003045–W003109 | 17:59.060–18:21.000 | Deliver the qualified verdict |

Total spoken ranges: 91.920 seconds. These are proposed placements, not a completed episode edit. The separate cinematic work has not been modified.

## Look and performance direction

16:9, eye-level, chest-up, direct lens address, natural skin texture and recognizable identity. Keep the existing glasses and facial hair. The initial photo-look brief specified a navy shirt; H instead retains the cream polo from the preferred footage and extends its missing outer shoulders. Restrained working study: warm neutral plaster, a modest timber shelf with a few unlabelled books, soft daylight from camera left, quiet depth. No visible screens, readable book titles, credentials, plaques, luxury cues, or equipment display. No wide-angle facial distortion.

One fixed camera. Small natural head and shoulder movement; hands kept below the speaking frame for the first test. Calm, candid delivery. No broad sales smile, nodding loop, or theatrical gestures. Initial and final frame retain the same set, identity, wardrobe, framing, and light. Exact wardrobe/set suitability must be checked against the generated candidate.

Picture/audio mode: `presenter_address`; language carrier: `presenter`; face function: `presenter_delivery`; visible speech: synchronized to the exact supplied master excerpt. A silent preview is expected to look like missing speech. Lip-sync quality requires moving-video review with sound.

Use a clean cut into and out of each insert. Keep graphics and captions out of the first look test. The final edit retains the continuous locked narration track; provider audio is a sync guide. Do not generate a replacement voice, change speed, or alter the master.

## Preparation and review

Run `python3 prepare.py` from this directory. It verifies locked input hashes, extracts sample-exact PCM WAV slices with at most 250 ms of available adjacent silence, and records exact word IDs, text, source offsets, file hashes, and PCM verification in `presenter-manifest.json`. Media remains ignored. Handles are not part of the proposed spoken-range total and must be removed using the recorded offset when conforming picture.

Start with `presenter-02-scope.wav`. Review identity, chest-up framing, eye line, glasses, mouth synchronization, neck/shoulders, and the final word. A static image is look evidence only. A generated video is a candidate until reviewed; final placements remain subject to the full-episode edit.

## Source authority

Inputs are the EP007 Step 2 narration lock, v4 master, word transcript, and canonical W. No returned visual model or legacy storyboard supplies direction. The current v0.4 Step 3 restart has no approved whole-episode visual plan; this isolated owner-requested look study does not change that state.
