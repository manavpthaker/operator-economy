# Short 03: Who owns the second booking?

Private avatar-forward review MP4: `review/ep009-short03-avatar-forward-r3-review.mp4`.

16.166667 seconds, 388 frames, 1080×1920, 24 fps, H.264/AAC. 13.916667 seconds of exact selected presenter picture/locked narration including the existing silence tail, then a 2.25-second episode question and Related Video CTA.

The avatar leads the entire spoken section. Wide framing preserves the pointing hand and both hands; the original closer source cut lands on the outside-service question. Small booking-site/email and returning-guest cues clarify the named relationships without replacing the presenter. All audio comes from exact r3 master samples. No new speech, regeneration, looping, speed change, or interpolation.

The wide source retains its exact 960x1080 crop at x360,y0, scaled to 1080x1216 and placed at y200 on solid #173530 framing. This replaces the rejected stretched edge extensions. Caption text sits clearly on the pine lower area. Outer room and elbow edges crop; hands and pointing remain visible. The existing close shot uses a direct portrait crop. No duplicate face, blur or new room.

`check-final-r4.json` passes lint, runtime, layout, motion and contrast with frame checks enabled. Three advisory structural warnings remain for simple graphic groups. Motion assertions are enabled (300 samples). Strict full decode passed. AAC audio correlates 0.9998458 with the exact source excerpt at zero lag. The actual PCM shows a clean silence window before the next word; the final source cut at frame 4844 is inside it. The earlier suggested 4854/4852 cuts would have included the next phrase's onset despite approximate transcript timing.

Eight actual encoded frames were inspected in `review/contact-sheet.jpg`; face, pointing hand, cue/caption placement and closing CTA are intact. Review quality is inherited from the selected episode performance; this is not new owner acceptance or publication authority. Related Video must be attached to the exact full episode before publication.

Pin upgrade: scaffold 0.8.51 → 0.8.53, validated by the final passing check. Prior unsuccessful checks remain as historical QA.

Plain-framing correction: same duration, audio, source EDL and captions. New encoded contact sheet inspected; strict full decode passed again. Superseded edge-extension video/QA are preserved locally.
