# AUTH-R1 technical QA

Status: PASS for private owner audition. Lexical fidelity and creative approval remain pending.

| Listen code | Duration | Pace for 97 words | Integrated loudness | Loudness range | True peak | Full decode |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| A | 45.949 s | 126.7 wpm | -20.1 LUFS | 4.0 LU | -1.1 dBFS | pass |
| B | 42.684 s | 136.4 wpm | -20.2 LUFS | 3.5 LU | -2.0 dBFS | pass |
| C | 45.479 s | 128.0 wpm | -19.9 LUFS | 3.2 LU | -0.8 dBFS | pass |
| D, incumbent control | 40.240 s | 144.6 wpm | -20.3 LUFS | 2.5 LU | -4.4 dBFS | pass |

All review files are mono 44.1 kHz, 192 kbps MP3. A through C are exact byte copies of the
provider previews. D is a review-only MP3 derived from the locked incumbent working WAV and
loudness-matched near -20 LUFS. No review copy is a narration master.

No file clips or truncates, and all four decode fully with strict FFmpeg error handling. No remix
preview contains a detected silence of at least 0.75 seconds at -45 dBFS. These measurements do
not prove spoken-word identity, naturalness, recognizable Manav identity, or camera-ready energy.
Those remain owner-listen gates.

The owner should answer only:

1. Which code sounds most recognizably like you?
2. Which code has the right camera-ready energy without becoming an announcer?
3. Keep one code, or reject all four?

A save action is not authorized by this review.
