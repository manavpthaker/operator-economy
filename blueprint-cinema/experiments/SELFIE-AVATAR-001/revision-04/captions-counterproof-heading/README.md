# Highlighted Counterproof heading captions

[Watch the highlighted heading version](https://d2ol7oe51mr4n9.cloudfront.net/user_3J3m5xtqP8Xv0MOsPutf0uV3maX/6e160dad-4322-4c5c-987f-6768b259bdbb.mp4).

Owner feedback rejected the first centered, outlined body-font captions and
requested highlighting and off-center placement like the heading text.

This review adapts the existing `.cover-after` heading in Content OS
`design-system/rev-e/rev-e.css` and its
`previews/rev-e/linkedin-coqui-carousel-01.png` reference: Archivo weight 630,
width axis 100, tracking -0.06em, proof `#F3F6F5` text on solid graphite
`#202426`. The new caption blocks stay left-aligned at x=48 and fit the longest
line. Text starts at x=64; a 56px font and at most two lines stay below the face.
These portrait dimensions are local adaptations of the heading, not changes to
the shared Counterproof lock.

The original clean R4 video is the source. The 49 cues and all 184 words are
byte-identical to the prior verified `caps.srt`, SHA-256
`eb157d8a967facdd2c8eebd1449adecd1dcebd86d0d57104c1dae42110673124`.
The prior final-audio Whisper verification and measured insertion offset remain
applicable because both source video and SRT are pinned unchanged. This is a
caption-style edit; no retranscription, retiming, or new avatar generation is
needed. The clean master and rejected first caption treatment are preserved.

`render.py` adapts the maintained Higgsfield subtitle burner's label callback to
the owner's requested heading treatment. It retains the existing hold, overlay
and audio-copy pipeline and uses the same standalone media-review route.
`LAYOUT.json` records every cue's actual type settings, line breaks and bounds.
`REPORT.json` records output media and audio-preservation checks. `DELIVERY.json`
records hosted readback and visual review. No publishing or canonical episode
state changes are made.

Output: 53.875 seconds, 720×1280, 24 fps, 1,293 frames. Complete decoding,
unchanged decoded audio, unchanged subtitle bytes, per-cue bounds and exact
downloaded checksum checks passed. Encoded opening, long-line, mid-script and
closing samples show the intended highlighted left-aligned heading treatment.
