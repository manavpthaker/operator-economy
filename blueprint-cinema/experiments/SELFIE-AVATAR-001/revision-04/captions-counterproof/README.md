# Counterproof caption review

[Watch the captioned video](https://d2ol7oe51mr4n9.cloudfront.net/user_3J3m5xtqP8Xv0MOsPutf0uV3maX/00f087b7-ffb1-48a5-87aa-0630520ee85e.mp4).

The owner requested permanent SRT captions on the existing R4 selfie video using
the Counterproof design system. This is an experiment-local personal-video
adapter for that request, not a change to Counterproof's shared visual lock or
an Operator Economy episode/publication approval.

The visual authority is Content OS `design-system/LOCK.md`, `README.md`, and
`rev-e/rev-e.css`: Atkinson Hyperlegible Next carries reading copy; proof
`#F3F6F5` and graphite `#202426` supply legible text and a restrained outline.
Source sage is reserved for evidence semantics and is not a word highlight.

The proposed adaptation uses Atkinson at weight 600 and 42 px, sentence case,
at most two lines, 77% frame width and a 17% bottom margin. The outline keeps
the home footage visible and preserves the casual delivery. No decorative
Countershift, labels, logos or repeated authorship is added.

`render.py` runs in the existing Higgsfield standalone media-review workflow.
It uses the installed subtitle burner's fit, placement, hold and encode logic,
with exact Counterproof colors, font weight and a bounded filter thread pool.
This is not a Resolve conform or canonical episode delivery.

The clean input is immutable:
`../mobile-delivery/READBACK.json` records its hosted URL and checksum
`3aa4356f48c0e96fc9ab50da9897a22be88b897a9fa7af6c0ef75c440584c236`.
The caption clock comes from the existing exact-script Whisper word timings
in `../voice/R4/FINAL-WORD-TIMINGS.json`, shifted by the measured 0.342125-second
audio insertion from `../lip-sync/RESTORED-AUDIO-QA.json`. Fresh Whisper on the
finished video independently verifies wording and start/middle/end timing.

Every one of the 184 source words is retained in 49 phrase cues, with at most
five words and 32 characters per cue. `caps.srt` is retained for editing;
the delivered MP4 burns those captions into the picture. Audio is stream-copied
and its decoded checksum must match the clean input. Runtime reports and a
visual review record bind verification to the delivered output bytes.

Delivered: 53.875 seconds, 720×1280, 24 fps, 1,293 frames. The final-video
Whisper check matched 96.77% before exact authored-word substitution and
retained all 184 words. Start/middle/end timing comparisons were within
0.203 seconds. Full decoding passed, audio hashes matched, both uploads
returned HTTP 200, and downloaded output bytes matched the render checksum.
Opening, middle, GTM Engine and closing caption samples were visually inspected;
a two-line cue was also readable during full-size normal browser playback.
