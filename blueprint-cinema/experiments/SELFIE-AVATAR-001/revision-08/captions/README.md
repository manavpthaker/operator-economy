Completed render: see REPORT.json, TIMING-MAP.json and ../DELIVERY.json. The finished audio and SRT are identical to R7.

# R8 expression-only heading captions

Prepared adapter only. No R8 caption render or upload has run from this folder.
The owner identified the smile as the remaining issue and described the rest of
R7 as solid. R8 changes expression only: preserve R7's 21.25-second/510-frame
soundtrack, 18 cues, 68 words, and the same highlighted heading design. This
adapter makes no new tempo, pause, wording, or mix changes.
This sample contains the first 68 words and first 18 caption cues, ending with
“and what they’re doing already.” It is not the complete 184-word video.

The actual edited voice is 1,020,000 samples at 48 kHz: 21.25 seconds and 510
frames at 24 fps. `../../revision-07/voice/R7-VOICE-REPORT.json` has SHA-256
`4e5b95a90e5ed8a3c6249db63e45c8edafebda58eebaa01432a087c7a654274e`;
the edited WAV hash is
`ca8d664b1e2e9bac50eadc4e9efd6d03d7de02d87cbc0511c7aa97d52c6a7f3d`.
These measured sample counts replace the earlier duration projection.

`render.py` keeps the R7 renderer's heading callback and burn arguments: Archivo 56 px,
weight 630, width axis 100, tracking -0.06em, proof `#F3F6F5` on graphite
`#202426`, x=48, top=900, and at most two lines. It uses the installed subtitle
burner; no bundled source is copied into this directory.

## Timing and input contract

The renderer reads the immutable full R4 SRT, verifies its hash, and selects its
first 18 cues. It subtracts the old 0.342125-second Sync insertion before mapping
each cue through the actual R7 voice report's `sample_map`. The map preserves
copied ranges, uses the measured input/output interval ratios for both tempo
changes, and includes the 5,760-sample pause. Padding has no spoken caption.
It then adds the freshly measured offset from the edited R7 voice to the clean
R8 sample video. A zero offset is not assumed; root supplies fresh evidence
bound to the new picture and unchanged R7 audio.

All 68 word timings are also mapped from the frozen full-precision R4 clock.
The SRT-derived cue clock must match that original clock within 1.1 ms before
mapping. The first cue's six-sample negative rounding residue is clamped to zero.
Text must equal the exact first 68 source words; chronology and source coverage
must pass. Actual tempo-filter sample counts establish interval mappings, not
phoneme-level alignment. Final speech/caption and lip-sync review remain required.

The orchestrator supplies ephemeral `inputs.json` with:

- `video_url`, `video_sha256`: clean R8 expression sample and exact hash.
- `font_url`, `font_sha256`: the same pinned Archivo file used in R6.
- `script`: exact full `revision-04/SCRIPT.txt` bytes, including final newline.
- `prior_srt`: exact full `revision-04/captions-counterproof-heading/caps.srt` text.
- `voice_report_json`, `voice_report_sha256`: exact R7 voice report text and the hash above.
- `audio_offset_seconds`: fresh measured offset from the unchanged R7 voice to the clean R8 sample.
- `audio_alignment`: the R6 receipt fields, bound to the new video hash and **edited R7 WAV hash** as `source_voice_sha256`; complete voice preserved, uniform offset, drift at most 0.02 seconds, minimum window correlation at least 0.99, and retained evidence SHA-256.
- `video_upload_url`, `contact_upload_url`: reserved signed PUT destinations.

No new SRT input is required: `caps.srt` is generated from the pinned source
clock and actual sample map. No STT, TTS, avatar generation, voice stretch, or
lip-sync generation occurs in this renderer.

## Outputs and checks

Runtime needs the existing Higgsfield sandbox with `HF_WORKFLOWS`, its maintained
`subtitles/scripts/subtitle_paper_burn.py`, Pillow variation support, FFmpeg,
ffprobe, curl, and network access for pinned inputs and reserved outputs.

The producer creates `heading.mp4`, `contact.jpg`, `caps.srt`, `LAYOUT.json`,
`TIMING-MAP.json`, and `REPORT.json`. The timing map retains all 68 mapped words,
18 cues, the actual sample map, source pins, and fresh alignment evidence.
Media checks preserve stream timing, dimensions, frame rate/count, duration,
and decoded audio through the caption burn; strict decoding must pass.
Contact samples cover the opening, self-deprecating line, GTM explanation,
and last phrase. The same contact image adds eight face crops at requested
times 3.5, 3.875, 4.25, 4.5, 4.875, 5.25, 5.667, and 6.125 seconds, sampled at
the nearest 24 fps frame, with actual frame/time labels. These are review-only
crops, recorded in the report; they do not alter the video or need another slot.
Root owns encoded visual/playback review and delivery.

R4–R7 sources remain unchanged. No completed render, owner acceptance, lip-sync
approval, full-video completion, or publication state is claimed here.
