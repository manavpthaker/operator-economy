# EP007 premium comparison and restored opening

Private production test. The user's selected avatar performance is Seedance 2.5 (404). The new opening uses its Sync 3 derivative (407), the earlier workshop film coverage, and the existing illustration animation. No production approval or publication is implied.

## What caused the divergence

The earlier film was generated with Kling 3 Pro through Fal; HyperFrames assembled the footage. Later Higgsfield tests used Wan 2.7 at 720p and changed the setting, cast, staging and direction together. That was not a controlled test of HyperFrames against Higgsfield. See the [direction audit](../../episodes/EP007-exit-readiness-prep/agents/deliverables/premium-004-direction-audit/AUDIT.md).

The new film comparison holds the original workshop image, written performance prompt and requested nine-second duration constant. Backend controls differ, and the original Fal negative prompt/CFG are not shared API controls. One take per model supports a choice among these takes, not a universal ranking.

## Generated tests

| ID | Model and route | Finding | Use |
|---|---|---|---|
| 401 | Kling 3 Pro / Higgsfield | Closest new take to the requested stop; mouth settles slightly late | Film comparison only |
| 402 | Seedance 2.5, 1080p high bitrate / Higgsfield | Stops early; larger hand gesture | Film comparison only |
| 403 | Cinema Studio 3.0, 1080p / Higgsfield | Stops several seconds early; changes framing | Film comparison only |
| 404 | Seedance 2.5, 1080p high bitrate / Higgsfield | User-selected expression and head movement; changes supplied audio | Performance source for 407 |
| 405 | OmniHuman 1.5, non-Turbo 720p / Fal | Preserves the recording; more recurring hand/head movement | Avatar alternate |
| 406 | Kling Avatar 2 Pro / Fal | Preserves the recording; later low hand gestures | Avatar alternate |
| 407 | Sync 3 / Fal, applied to 404 | Preserves locked recording and sampled Seedance head/blink motion | Selected avatar derivative for the rough cut |

OmniHuman's official documentation describes its 720p mode as higher quality than its 1080p mode. This setting was selected for quality. The generated picture is 1248×704. Actual media dimensions and timing are measured in the QA packet, rather than inferred from request labels.

The 407 audio has correlation 0.99980151 with the locked recording at zero lag; all 22 active windows align at zero lag. Same-timestamp samples preserve 404's head movement and blinks. This establishes audio preservation and visual continuity, not phoneme-perfect lip sync. Lower-face reconstruction still requires normal-speed judgment. See the [independent technical QA](../../episodes/EP007-exit-readiness-prep/agents/deliverables/premium-004-technical-qa/report.md).

## Restored opening

- Original workshop coverage: continuous establishing view, buyer question, unfinished answer, realization.
- Existing illustration and identity animation retained from experiment 003.
- Seedance 404 performance, corrected with Sync 3 using the exact approved 11.34-second narration.
- Single locked narration WAV, with private-preview out-point at59.50 seconds. Generated video audio is muted in the composition; master bytes are unchanged.
- 1280×720, 30 fps, 1,785 frames, 59.50 seconds.

The precise source selections and time ranges are in [EDIT-MANIFEST.json](hyperframes/EDIT-MANIFEST.json). Sources and hashes are in [STAGING-MANIFEST.json](hyperframes/STAGING-MANIFEST.json). A trial join between two similar wide shots at 10.92 seconds was removed after QA found a pose jump. The stable original establishing shot now runs continuously to 14.77 seconds.

HyperFrames 0.8.33 is pinned only in this new experiment. Its check passed with zero runtime or layout errors. Two warnings about repeated GSAP `fromTo` targets are inherited from the unchanged illustration; they are not evidence of a new visible failure. A four-pixel bottom overscan in the presenter composition removes colored noise present in the Sync 3 source. This preserves source timing. The final targeted check has zero layout warnings. The first corrected render passed full decode, all five cuts and its last frame, with no blank frames; all340presenter frames passed the bottom-edge scan. A final endpoint audit found that the forced-alignment start for next word “One” is late: the59.86s excerpt catches renewed voicing from about59.62s. The private preview now ends at59.50s, after “practice” and within measured quiet audio. Its40ms window has RMS0.00105. No canonical timing file, narration master, provider input or generated source was altered. See [REVIEW.json](REVIEW.json) and the [clean-outpoint QA packet](../../episodes/EP007-exit-readiness-prep/agents/deliverables/premium-004-technical-qa/rough-cut-clean-outpoint-qa.json).

## Cost and receipts

Higgsfield charged 294.75 credits for 401–404: balance 915.5 before, 620.75 after. The source receipts are in HIGGSFIELD-RESULTS.json. The three Fal jobs completed after the user topped up the account. Public rates imply approximately $4.74–$4.83 combined; this is an estimate, not an account invoice. OmniHuman's returned billable duration is 11.34 seconds; Kling's returned output duration is 12.266 seconds; the Sync receipt does not establish the final billed duration.

The initial Fal exhausted-balance error is retained. Higgsfield Sync preflights were rejected by incompatible input-role schemas and did not submit a generation. The successful Sync job used Fal. Exact requests, job IDs and result URLs remain in the adjacent JSON receipts. No additional generation is needed for this test.


## Review output

[Open the completed59.50-second test](review-media/ep007-original-film-seedance-hyperframes.mp4). SHA-256: `d1e0d14bf0b1acc750994dc95e767743301e621f6971987e0a40f9c644f0668a`. The live comparison page is served at `http://127.0.0.1:57355/`. Its avatar button jumps directly to48.52s.

Final59.50s output passes full decode:1,785frames,1280×720/30fps. Audio correlation against the retained master interval is0.99982402; final40ms RMS0.001668 confirms a quiet ending. Final frame1784 is present with clean bottom edge. Rounded lips persist during the last quiet moment, so natural mouth closure remains a creative review item.
