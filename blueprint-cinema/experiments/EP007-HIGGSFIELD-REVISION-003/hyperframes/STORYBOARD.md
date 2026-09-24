---
status: selected-for-private-review
workflow: general-video
aspect: 16:9
---

# Revision 003 edit

| Record range | Picture and action | Source window / implementation |
| --- | --- | --- |
| 0–14.77 | Three-quarter shared-review two-shot. Owner indicates the open page, buyer acknowledges, and both return attention to the folder. | `assets/review-wide.mp4` [0, 14.77); `compositions/meeting.html`, composition `review-wide`. |
| 14.77–21.28 | Shared folder and relaxed hands carry the narrated buyer question. Buyer lifts and rests his hand; owner's hand remains still. | `assets/shared-folder.mp4` [0, 6.51); `compositions/buyer.html`, composition `shared-folder`. |
| 21.28–35.08 | Owner-favored two-shot retains the buyer and folder. Owner begins an answer, stops by source 5.52 seconds, and holds quiet realization while buyer gives space. | `assets/owner-two-shot.mp4` [0, 13.8); `compositions/owner.html`, composition `owner-two-shot`. |
| 35.08–48.52 | Existing Working Model and show identity, unchanged. | `compositions/question.html`, `working-model.svg`, its manifest and four SVG layers are byte-identical to experiment 002. |
| 48.52–59.8666666667 | Wider direct-address presenter with subtle head/hand motion. Exact identity narration ends at 59.86; picture continues through the last output frame. | `assets/avatar-selected.mp4` [0, 11.3466666667); `compositions/presenter.html`. Retry 205 selected by the lead for private review; not owner-approved. |

The complete narrator range is source master [0, 59.86), played once at volume 1 on track 10. Every scene video is muted. No source is time-stretched; no music or transition is added. The narrator's 26.80–27.92 pause and 27.92–33.62 arithmetic stay uninterrupted within the owner take. Film mode is `narrated_dramatization`; presenter mode is `presenter_address`.

The preserved animation traces the business/owner relationship, leaves the hypothetical one-month absence unresolved, and introduces the show identity in the same paper scene. Its content and timing are unchanged. The review container is 1,796 frames at 30 fps. The presenter wrapper has no terminal visibility hide, retaining the previous fix for a blank last frame.

Export boundary correction: the first encode exposed blank paper at frames 443, 638, 1052 and 1455, immediately before the four internal cuts. Outgoing host coverage and filmed-media durations now include one extra 30 fps frame beneath the unchanged non-clip window visibility gates. Separate metadata track lanes represent that deliberate covered overlap. Visible cut times, source offsets, the root WAV and `question.html` bytes remain unchanged. The failed MP4 is retained with `.before-cut-boundary-fix` in its filename; only the corrected encode is a review candidate.

`../DIRECTION-PACKET.md` is the current coverage plan. `../inputs/hyperframes-storyboard.baseline.md` records historical provenance. All four selected outputs are staged and decode correctly. The current final check uses retry 205; the older receipt `verification/check-before-avatar-retry.json` retains the earlier technical pass with rejected avatar 201. The lead selected the filmed takes for this private test with caveats: the owner settles slightly early, and the buyer's soft gaze persists. Performance selection does not advance canonical gates or approve publication.
