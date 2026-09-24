# R5 Counterproof heading captions

Prepared adapter only. No R5 caption render or delivery has run from this folder.

`render.py` preserves the prior highlighted caption renderer from
`revision-04/captions-counterproof-heading/render.py`: Archivo 56 px, weight 630,
width axis 100, tracking -0.06em, proof `#F3F6F5` on solid graphite `#202426`,
left edge x=48, top y=900, at most two lines, no outline. Its label callback,
line fitting, padding, hold parameters, overlay, and audio-copy route are unchanged.
The same 49 phrases and exact 184-word script remain the caption content.

The input must be the new clean R5 Sync video. The complete R4 narration and its
relative word clock remain fixed; only the Sync insertion may differ. Before
running, freshly compare the decoded R5 audio with the full R4 voice, confirm
the whole source survives, measure a uniform offset across start/middle/end,
and retain the comparison receipt. This adapter does not perform that upstream
waveform comparison and does not substitute a new transcription.

Rebase every prior absolute caption timestamp by:

`new measured Sync offset - 0.342125 seconds`

Provide the rebased SRT in `inputs.json`; the script does not silently retime
the supplied SRT. It checks all 98 start/end timestamps against that uniform
rebase within 1.1 ms for SRT quantization, every cue's exact words, all 49 cues,
their chronology, and the exact 184-word script. The prior SRT, script, voice,
and font have fixed SHA-256 pins inside the adapter. R4 files stay untouched.

## Required inputs

The orchestrator supplies one ephemeral `inputs.json` beside `render.py` in the
Higgsfield media sandbox. Retain a sanitized input receipt separately; signed
upload URLs must not be committed.

| Key | Value |
|---|---|
| `video_url`, `video_sha256` | New uncaptioned R5 Sync video and exact hash |
| `font_url`, `font_sha256` | Archivo file with hash `0e094a7d3c7c4c25cf1310c4b30014f1dae9332220b1c2c88f4fa996f0b05053` |
| `script` | Exact R4 `SCRIPT.txt` contents, including final newline |
| `prior_srt` | Exact `revision-04/captions-counterproof-heading/caps.srt` contents |
| `srt`, `srt_sha256` | New rebased SRT and SHA-256 of its exact UTF-8 bytes |
| `audio_offset_seconds` | New measured source-to-R5 Sync insertion |
| `audio_alignment` | Fresh waveform comparison fields listed below |
| `video_upload_url`, `contact_upload_url` | Reserved signed PUT destinations |

`audio_alignment` requires these fields:

- `video_sha256`: matches the new `video_sha256` above.
- `source_voice_sha256`: `b2c10c8e5b3267a43f8aaa4b3aba2132f4b20d6df6cd22fbfdcf0dc831e7e3b3`.
- `full_source_voice_preserved`: `true`, after checking the complete voice and ending.
- `uniform_offset`: `true`, after comparing separated waveform windows.
- `offset_seconds`: matches `audio_offset_seconds` within one microsecond.
- `max_drift_seconds`: measured finite nonnegative spread, at most 0.02 seconds.
- `min_window_correlation`: measured minimum correlation, at least 0.99.
- `evidence_sha256`: SHA-256 of the retained fresh waveform comparison receipt.

These are input gates, not prefilled claims. If the fresh comparison does not
support them, do not run the burn with fabricated values. Resolve the audio
alignment upstream before supplying a revised SRT.

## Runtime and outputs

Execution needs the existing Higgsfield media sandbox with `HF_WORKFLOWS`, its
maintained `subtitles/scripts/subtitle_paper_burn.py`, Python/Pillow with Archivo
variation support, FFmpeg/ffprobe, curl, and network access for pinned inputs and
reserved outputs. It performs no TTS, avatar generation, or STT.

The runtime creates `heading.mp4`, `contact.jpg`, `caps.srt`, `LAYOUT.json`,
`TIMING-REBASE.json`, and `REPORT.json`. It retains the supplied SRT bytes exactly;
reports distinguish that fact from whether those bytes happen to match R4.
The rebase report records the old and new hashes, both measured offsets, the
timestamp delta, all cue comparisons, and the bound alignment receipt. No report
unconditionally claims an unchanged R4 SRT.

Post-render checks preserve frame count, frame rate, dimensions, stream start
times, audio/video duration, and exact decoded audio through the caption burn.
Full decoding must pass before uploads. The contact image samples opening,
long-line, middle, and final captions; root still reviews the encoded result
for face clearance and readability. Successful mechanics are not visual or
publication approval. No canonical episode or publishing state changes occur.


Completed: final heading burn is hosted at the URL in `../DELIVERY.json`.
The new offset measured +0.342125 seconds, exactly matching R4; `caps.srt`
is therefore byte-identical to the latest R4 heading captions. The renderer
validated all cues, preserved the decoded soundtrack exactly, and passed
strict full decoding. Root visually checked the four sampled cue frames and
live browser playback. No owner acceptance is implied.
