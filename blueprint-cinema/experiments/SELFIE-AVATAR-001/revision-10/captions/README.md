# R10 full-script Counterproof captions

Prepared adapter only. No caption render, generation, upload, or commit has run
from this folder. Root owns the new narration, assembly, fresh transcription,
SRT preparation, final verification, and delivery.

The source is the exact `../SCRIPT.txt`, SHA-256
`242ab0bedea72a8fc5d303191f9dc61569614dc70cfdbef759891a7fa94affd6`.
It currently contains 193 whitespace-separated words. The renderer derives its
word and cue counts from the supplied script and SRT; it contains no earlier
revision's cue-count constant, caption timestamps, or R7 voice map.

The heading callback and burner arguments preserve the existing R4 highlighted
design: Archivo 56 px, weight 630, width axis 100, tracking -0.06em, proof
`#F3F6F5` on graphite `#202426`, left x=48, top y=900, at most two lines, and no
outline. Caption wording remains sentence case. The source frame is 720×1280;
actual duration and frame count come from the new finished video.

## Required config

Root supplies one ephemeral `inputs.json` in the producing Higgsfield sandbox:

- `video_url`, `video_sha256`: exact final clean video, before captions.
- `font_url`, `font_sha256`: Archivo file pinned to `0e094a7d3c7c4c25cf1310c4b30014f1dae9332220b1c2c88f4fa996f0b05053`.
- `script`: exact R10 `SCRIPT.txt` text, including its final newline.
- `srt`, `srt_sha256`: exact fresh, final-video-timed SRT and SHA-256 of its UTF-8 bytes.
- `transcription`: fields below, from fresh transcription and script alignment.
- `audio_binding`: fields below, from root's full-narration preservation check.
- `video_upload_url`, `contact_upload_url`: reserved signed PUT destinations.

`transcription` requires:

- `video_sha256`: the same new final clean video hash.
- `script_sha256`: the exact R10 script hash above.
- `srt_sha256`: the supplied fresh SRT hash.
- `word_count`: exact count of the new script, also checked against all captions.
- `similarity`: fresh transcription similarity, finite and at least 0.90.
- `evidence_sha256`: hash of root's retained fresh transcription/alignment receipt.

`audio_binding` requires:

- `video_sha256`: the same new final clean video hash.
- `source_audio_sha256`: hash of the completed intended narration source.
- `video_audio_decoded_sha256`: bare 64-character SHA-256 of the clean video's decoded audio, using FFmpeg `-map 0:a:0 -f streamhash -hash sha256`; supply the digest after `SHA256=`.
- `full_source_audio_preserved`: `true`, only after root verifies complete narration and ending.
- `evidence_sha256`: hash of the retained audio preservation receipt.

These bindings are required evidence supplied by root. The renderer verifies
that the clean video's decoded audio matches the supplied digest and that the
caption burn leaves it unchanged. It does not independently reproduce root's
source-to-video waveform comparison or claim perceptual lip-sync approval.

## Validation and outputs

Before burning, exact script, SRT, and font pins must match. Captions must contain
every script word in order with exact spelling, punctuation, and case. Cue
numbers must be sequential; timestamps must be valid, positive in duration,
non-overlapping, and within the finished audio/video duration. Cue count is
computed from the new SRT. Fresh evidence must bind that same script, SRT,
video, and narration. No earlier transcription or caption clock is reused.

The adapter loads the installed
`$HF_WORKFLOWS/subtitles/scripts/subtitle_paper_burn.py`, preserving its fit,
hold, overlay, and audio-copy pipeline. The scoped callback applies the existing
heading style and checks every caption's two-line bounds. Nothing in this
renderer synthesizes audio or video, retranscribes speech, changes timing, or
rewrites the supplied SRT.

Runtime needs Python/Pillow with font variation support, the installed burner,
FFmpeg/ffprobe, curl, and access to pinned source and reserved output URLs.
The producer creates `heading.mp4`, `contact.jpg`, `caps.srt`, `LAYOUT.json`,
and `REPORT.json`. Four contact samples are chosen evenly across the cue index
range, including first and final cues; each is captured at its cue midpoint,
with a caption crop alongside the full portrait. Chosen indices/times are
recorded in the report.

Post-render checks preserve dimensions, frame rate/count, stream starts,
audio/video duration, and exact decoded audio. Full decoding must pass before
uploads. The report states preservation relative to the supplied new SRT and
source, never relative to old caption bytes. Root reviews encoded readability,
face clearance, speech/caption timing, and playback before delivery.

Keep upload signatures out of retained records. This folder makes no owner
acceptance, editorial approval, publication, or full-video completion claim.
