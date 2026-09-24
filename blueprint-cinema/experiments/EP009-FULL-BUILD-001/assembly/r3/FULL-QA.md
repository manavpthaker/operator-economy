# EP009 r3 full review draft — assembly QA

2026-09-17. **Technical checks passed; full episode remains for review.** The owner has locked the brand pause and corrected hospitality experience. That scoped acceptance does not accept the new film, final presenter delivery, or release.

## Exact reviewed output

- Video: `assembly/qa/r3/ep009-full-r3-review-draft.mp4`
- SHA-256: `16a065294110e0bbb86b49a2f3901cd2c605a919864fcd470f4af06c19bcc9b7`
- Final BUILD: `assembly/r3/ep009-full-r3-review-draft-BUILD.json`, SHA-256 `806ec203069d994fb5928c61aaa1350c788b2faf5fa3e9d2663e593ab962aa12`
- Review page: <http://localhost:3070/ep009-r3-review.html>; full runtime is **20:21.791667**, displayed as **20:22**. All 75 segment jumps and six film entries use revised times.

The full render uses retained source plates directly, six selected film clips, the labeled L3 still for corrected P08, and the bound r3 PCM master. It does not transcode the completed r2 episode. Earlier drafts and failed outputs remain preserved.

## Evidence

`ep009-full-r3-review-draft-VERIFICATION.json` binds the exact BUILD and output above and reports zero errors:

- Every encoded video frame decoded: **29,323 / 29,323**, 1280×720, 24 fps. The only uniform frame is the planned brand reveal frame 1427. No unplanned uniform frames or decode errors.
- All **58,646,000** program audio samples compared against the revised master plus its 1,080-sample picture-tail padding, in both channels. Full correlation is **0.999988545**; lowest voiced five-second-window correlation **0.999970147**. Maximum absolute voiced-window level difference is **0.013568 dB**. The additional 528 decoded AAC padding samples are silent.
- Measured audio: **−19.5 LUFS integrated**, 3.7 LU loudness range, **−5.7 dBTP**. Measurement only; this is not final mix acceptance.
- The scoped owner lock and its bound assets still match. The 296-frame brand context and 583-frame hospitality context previews retain their locked bytes. The master, revised transcript, TIMEMAP, and REVISION were not changed during full assembly.

`INDEPENDENT-FILM-MAPPING-AUDIT.json` independently verifies all 29,323 source-frame assignments, all 75 segment/cue records, and all 57 emitted trim/select branches. Exactly six intended picture overrides occupy 823 frames; other prepared picture mappings are unchanged. The audit binds the finalized BUILD hash above.

## Encoded integration inspection

`assembly/qa/r3/integration-frames/FRAME-COMPARISON.json` binds 44 extracted encoded frames and eight contact sheets. Each film selection includes the preceding unchanged frame, first frame, midpoint, last frame, and following unchanged frame. Additional samples cover the shortened brand reveal and both corrected-paragraph boundaries. Source comparisons use 640×360 decoded RGB; P08 is compared with the owner-locked hospitality context. Maximum mean absolute RGB difference is **1.188507 / 255**; at most **0.000434%** of compared pixels have mean RGB difference above 20. These differences are consistent with the full-output encoding pass.

All eight sheets were inspected. The expected scenes appear at the mapped boundaries: owner taking the landline call; monthly-report reading; two reports brought together; selected phone take `final-r2.mp4`; unresolved-report inspection; and writing the owner answer. The prior and following retained graphic/film frames appear on the intended sides of each insert. The brand reveal remains intact around the cut. Corrected P08 enters from the owner/operator drawing, shows the L3 still with the readable “corrected narration · presenter pending” label, then returns to the drawing. No stale speaking P08 picture appears in these inspected corrected-paragraph frames.

| Film selection | r3 frames, end exclusive | Entry time |
| --- | --- | --- |
| WF00-F06 | 9433–9607 | 6:33.041667 |
| WF01-monthly | 14765–14902 | 10:15.208333 |
| WF02-reports | 17821–17916 | 12:22.541667 |
| WF03-phone | 18010–18115 | 12:30.416667 |
| WF04-exception | 20207–20398 | 14:01.958333 |
| WF05-answer | 25715–25836 | 17:51.458333 |

## Limits and remaining work

This pass establishes encoded integrity, source placement, revised timing, audio correspondence, and sampled visual integration. It is **not a normal-speed audiovisual watch-through**, mouth-sync judgment, film-performance acceptance, or final editorial/release approval. Fourteen other presenter segments still use r1; corrected P08 remains an explicitly labeled review still. Presenter delivery and new film remain under review. The original r2 review is retained.

Reproduction tools: `assembly/_tools/verify_r3.py` and `assembly/_tools/inspect_r3_frames.py`, each run against the full BUILD above with the local `syncenv` Python runtime. Verification and frame-comparison JSON files retain the detailed methods, hashes, metrics, and limitations.
