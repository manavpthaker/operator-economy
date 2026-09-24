# Short02 avatar-forward r3

Finished private-review MP4: `review/ep009-short02-avatar-r3-review-final.mp4`.

- 17.791667 seconds; 427 frames; 1080×1920;24fps; H.264/AAC.
- Presenter fills portrait frame for66.8% of speech, using original selected native performances: seg028 local36–129 and seg021 local9–165. Original camera cut, facial expressions and central hand movements retained.
- Brief proof shows the actual Node-RED workflow, a readable crop of the OpenAI draft node, and the returned draft. Fictional guest / human review / no-send disclosures stay visible.
- Three exact locked audio selections; no re-voice, rate change, loops or generated performance. A2.25-second question card directs viewers to the full episode.
- Final check: `qa/check-final-r3.json`, all checks pass with motion enabled and frame-check. One non-blocking lint warning remains for the nested end-card section. Runtime, layout, motion and contrast each have0errors and0warnings.
- Twelve final encoded frames inspected, including both sides of edits. `qa/contact-sheet-final.jpg`. Earlier incoming background remnant resolved in final MP4.
- AAC output vs exact PCM assembly: correlation0.999868; gain0.997811. See `qa/audio-verification-final.json`.
- Fresh project uses HyperFrames0.8.53, latest checked this run. Existing r2 project stayed on0.8.51.

Source mappings and hashes are in `source-contract.json`; final output/check/asset binding in `QA.json`. Phone playback and normal-speed audiovisual inspection are delegated to the parent; this package does not assert owner acceptance or release. The release-time Related Video target remains unbound.
