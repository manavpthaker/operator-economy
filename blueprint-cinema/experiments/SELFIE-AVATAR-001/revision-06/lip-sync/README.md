# Revision 06 matched per-shot lip sync

The three matched inputs passed exact local and hosted byte checks, actual WAV parsing, and PCM comparison against the source ranges below. Exactly one request per section completed, without retries. All three returned pictures retained their exact frame counts and passed strict decoding. R5 remains unchanged.

Each returned soundtrack matches its corresponding input at **0.000000 seconds** of measured offset. All nine independently aligned local windows also returned zero offset; the lowest window correlation was **0.9997365682**. This supports assembling the returned picture sections with the continuous original WAV at onset zero, followed only by the agreed ending silence. These are soundtrack placement checks, not a perceptual mouth-sync verdict.

`ASSEMBLY-EVIDENCE.json` binds the three raw result URLs/hashes, inputs, frame counts, onset and correlation evidence. Its SHA-256 is `176eb4a8ad409f4ba9c50fff1cae3621fb41c318814d8a7cccf8a8b93ad21889`. Root owns final assembly; fresh complete-result QA is still pending.

Request IDs: section 1 `01a09865-c8c4-7141-9b2a-ef0b151a7f09`; section 2 `01a09865-c8c6-7af3-a7e6-39c9fd425b2f`; section 3 `01a09865-c8c5-74c1-a602-8018c3817336`.

Root chose three independent Sync v3 restorations after the owner reported intermittent inaccurate lip sync and manual mouth checks showed that globally advancing the R5 soundtrack would worsen known closures. Each new request uses `fal-ai/sync-lipsync/v3` with `sync_mode:cut_off`, no extra options, matched picture/audio durations and one exclusive submission intent.

| Section | Picture frames at 24 fps | Audio samples at 48 kHz | Original source samples | Added zero samples |
| --- | ---: | ---: | --- | ---: |
| 1 | 484 | 968000 | [0, 968000) | 0 |
| 2 | 378 | 756000 | [968000, 1724000) | 0 |
| 3 | 431 | 862000 | [1724000, 2536734) | 49266 |

All picture inputs are 720 × 1280 and video only. The audio is the unchanged R4 Original C PCM, SHA-256 `b2c10c8e5b3267a43f8aaa4b3aba2132f4b20d6df6cd22fbfdcf0dc831e7e3b3`. The third section alone receives trailing zero samples. There is no speech retiming or new voice generation.

Root supplies one manifest with `sections` numbered 1–3. Each contains `video:{url,local_path,sha256,width,height,frame_rate,frame_count,duration_seconds,audio_stream_count}` and `audio:{url,local_path,sha256,sample_rate_hz,sample_count,channels,sample_width_bytes}`. Local inputs must be under ignored `media/revision-06/`. URL suffix and MIME type are not used to infer audio format: binding verifies hosted and local byte hashes and parses the actual RIFF WAV, checking every PCM sample against the allowed original range plus tail silence.

```sh
python3 blueprint-cinema/experiments/SELFIE-AVATAR-001/revision-06/lip-sync/restore.py preflight
python3 blueprint-cinema/experiments/SELFIE-AVATAR-001/revision-06/lip-sync/restore.py bind /absolute/path/to/root-manifest.json
python3 blueprint-cinema/experiments/SELFIE-AVATAR-001/revision-06/lip-sync/restore.py submit 1
python3 blueprint-cinema/experiments/SELFIE-AVATAR-001/revision-06/lip-sync/restore.py status 1
python3 blueprint-cinema/experiments/SELFIE-AVATAR-001/revision-06/lip-sync/restore.py result 1
python3 blueprint-cinema/experiments/SELFIE-AVATAR-001/revision-06/lip-sync/restore.py download 1
```

Use each section index only for its assigned job. Do not submit until root provides and dispatches the verified exact input manifest. Credentials remain in memory and authenticated requests stay on `queue.fal.run`; redirects and provider fallback are denied. An existing intent prevents another POST. A provider error or uncertain result stops further new submissions for review, without retry.

Outputs are `media/revision-06/home-olive-gtm-r6-section-01-sync.mp4` through `section-03-sync.mp4`, with separate raw result hashes and provider receipts. Run `compare_audio.py REFERENCE_WAV RESULT_VIDEO SECTION_INDEX` in the media sandbox for fresh per-section offset, three local offsets, waveform correlation and tail checks. The preserved R5 offset is never presumed applicable.

Root owns final picture-only concat and continuous soundtrack assembly after the three returned speech clocks are measured. A single original full WAV, placed only after those measurements agree and padded only at the end, avoids AAC audio seam edits. This worker then checks the complete final waveform, dimensions, frame count, duration and strict decode. Technical integrity does not establish visual lip-sync or owner performance acceptance.

No captions, shared records, canonical state, commit, push, publication or unrelated generation belongs to this scope.
