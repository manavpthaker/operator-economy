# R7 take A — independent sampled performance review

2026-09-07. Role: QA reviewer. This review covers only the four exact work-order inputs. All SHA-256 values matched before inspection. No B review, assembly playback, narration audition, approval or production-gate claim.

## Finding

**Rapport and an attentive exit are visible. The strict closed-mouth direction did not hold.** Dense face samples show the owner opening into a broad smile around source 1.3–3s; the buyer holds a visibly parted mouth across approximately 4–8.5s before closing toward 9s. These are mainly sustained open-mouth states, not clearly repeated phoneme cycling. It would overstate this evidence to call it proven word-shaped speech. It is nevertheless a major mismatch with the specific naturally-closed-mouth instruction and creates an unheard-conversation risk that requires actual playback judgment.

| Criterion | Sampled evidence | Judgment |
| --- | --- | --- |
| Rapport | Mutual orientation, relaxed arms, softened expressions; strongest shared warmth in 0–1.2s | Present |
| Eye contact | Clear at entry and approximately 9–10.5s; owner turns her face more forward/down during the broad smile | Present but not uninterrupted |
| Focused attention shift | Buyer changes from smile to raised-brow attentiveness; becomes more upright around 5.5–6s, then reorients to her | Readable, but not an exact execution of the small forward-lean instruction |
| Owner confidence at exit | Stable upright posture, hands resting, steady attentive face directed toward him | Preserved; no premature collapse |
| Mouth performance | Owner's smile opens; buyer's lips stay parted for several seconds | Closed-mouth requirement fails; word-shaped speech remains unproven |
| World/props | Table objects remain in place in the sampled sequence; locked composition retains both people | No conspicuous sampled discontinuity |

The prompt's chin-dip/acknowledgment does not appear as exaggerated repeated nodding in these samples. The broadened owner smile is warmer than the requested slight closed-mouth response but is not evidence of a fabricated outcome or hostile exchange.

## Select guidance

Source **0–1.2s** is the most defensible short rapport window; **9–10.5s** is the clearest sampled attentive shared-eyeline window. These are observations, not approved selects. There is **no defensible single 10.36s fully closed-mouth selection** supported by this review. Trimming only the heads and tails would not remove the sustained middle mouth opening. Do not loop, freeze, slow or silently redesign the shot to manufacture compliance.

## Evidence and limits

Original media probe: one H.264 video stream, 1916×1080, 24fps, duration 11.041667s; no audio stream. The supplied contact sheet was inspected first, followed by four independently extracted QA sheets:

- `shot-a-2fps.png`: source 0–10.5s in 0.5s increments; four columns, left-to-right then down. Final two black cells are unused grid space, not source black frames.
- `owner-mouth-0-3s-6fps.png`: source 0–2.833s in 1/6s increments; six columns.
- `buyer-mouth-4-8s-6fps.png`: source 4–7.833s in 1/6s increments; six columns.
- `buyer-mouth-8-11s-6fps.png`: source 8–10.833s in 1/6s increments; six columns.

Frames were selected every fourth native frame for 6fps sheets and every twelfth for 2fps. Cropping and scaling are inspection-only derivatives; no source media or creative references changed. Initial labeled-sheet attempts failed because this FFmpeg build lacks `drawtext`; no outputs were produced by those failed attempts. The successful sheets use this explicit timestamp legend instead.

This is sequential still sampling, not a complete moving-image or audio-visual review. Sub-1/6s mouth motions can be missed, and naturalness, precise eyeline, conversational impression and narration fit remain provisional. Review the actual 17s assembly before acceptance. No permission to regenerate or retry is implied.
