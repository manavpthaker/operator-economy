# R7 opening-only Sync 2 Pro adapter

Prepared adapter; no input binding or provider submission is implied by its existence. Root dispatches each command. There is one opening, one possible POST, and no batch or section-index submission argument.

The fixed endpoint is `fal-ai/sync-lipsync/v2/pro`, with `sync_mode: cut_off`. Its model input contains exactly `video_url`, `audio_url`, and `sync_mode`. The [official API schema](https://fal.ai/models/fal-ai/sync-lipsync/v2/pro/api), read on 2026-09-13 UTC, documents those fields. The adapter does not add face detection, emotion, timing, webhook, or other generation options.

Root supplies `REQUEST-INPUT.json` with these keys:

```json
{
  "section_index": 1,
  "video": {
    "local_path": "blueprint-cinema/experiments/SELFIE-AVATAR-001/media/revision-07/ROOT_VIDEO.mp4",
    "url": "https://ROOT_VIDEO_URL",
    "sha256": "ROOT_VIDEO_SHA256",
    "width": 720,
    "height": 1280,
    "frame_rate": "24/1",
    "frame_count": 511,
    "duration_seconds": 21.291666666666668,
    "audio_stream_count": 0
  },
  "audio": {
    "local_path": "blueprint-cinema/experiments/SELFIE-AVATAR-001/media/revision-07/ROOT_AUDIO.wav",
    "url": "https://ROOT_AUDIO_URL",
    "sha256": "ROOT_AUDIO_SHA256",
    "sample_rate_hz": 48000,
    "sample_count": 1022000,
    "channels": 1,
    "sample_width_bytes": 2
  },
  "source_audio": {"local_path": "ROOT_SOURCE_WAV", "sha256": "ROOT_SOURCE_SHA256"},
  "script": {"local_path": "ROOT_SCRIPT", "sha256": "ROOT_SCRIPT_SHA256"},
  "voice_proof": {"local_path": "ROOT_VOICE_REPORT_JSON", "sha256": "ROOT_VOICE_REPORT_SHA256"},
  "video_qa": {"local_path": "ROOT_VIDEO_QA_JSON", "sha256": "ROOT_VIDEO_QA_SHA256"}
}
```

The counts above illustrate a matched pair, not an approved or measured R7 duration. Use the actual root-selected frame count and `frame_count * 2000` audio samples. Paths may be absolute or relative to OE. Video and matched audio must resolve inside ignored `media/revision-07/`. The source, script and two provenance reports must resolve inside OE.

`VIDEO-QA.json` uses root's existing shape: `video.sha256` must identify the exact matched input video; `matched_probe.streams` and `matched_probe.format` contain actual sandbox ffprobe output. The adapter verifies one 720×1280, 24fps video stream, its actual `nb_read_frames` (or `nb_frames`), its duration, and absence of an audio stream. It does **not** run a local video probe or establish that the sandbox report itself is truthful. Root owns producing and reviewing that report.

Binding checks pinned local bytes, fetches both hosted inputs without credentials, verifies identical hashes, parses the real uncompressed 48kHz mono 16-bit WAV and its complete sample payload, and requires exact sample/frame duration matching. It hashes the source audio, exact script and JSON voice-proof report. Unlike R6, it does not assert that this retimed opening is an unchanged source PCM range. That proof and the edit map remain in the voice report.

From this directory:

```sh
python3 restore.py preflight
python3 restore.py bind REQUEST-INPUT.json
python3 restore.py submit
python3 restore.py status
python3 restore.py result
python3 restore.py download
```

`preflight` only reports adapter state. `bind` performs read-only hosted checks and writes `BOUND-INPUT.json`, `MANIFEST.json`, and `REQUEST.json`; it does not submit. Before `submit`, the adapter checks those bindings, the unchanged root input and adapter hashes, and fresh local/hosted media bytes. It then writes one exclusive `SUBMISSION-INTENT.json` and fsyncs both that file and its parent directory before the sole POST. A concurrent or later submission cannot acquire the same intent. Any HTTP, transport, parse, or uncertain outcome preserves that intent; there is no automatic POST retry. Do not remove the intent to work around a failure.

Only authenticated requests to HTTPS `queue.fal.run` are allowed. Redirects are denied. The adapter reads the existing `FAL_KEY` from OE `.env` in memory; status/result commands use the returned queue URLs after the same hostname checks. No credentials accompany media fetches. Raw request, status, result, error and download records stay here for root inspection.

The download command writes `media/revision-07/home-olive-gtm-r7-opening-sync.mp4` with exclusive creation, or accepts an existing byte-identical file. It records the URL, SHA-256 and byte count. Root must run output video/audio QA in the Higgsfield sandbox. Download, byte checks and waveform placement cannot establish perceptual mouth sync, voice naturalness, performance acceptance, publication or canonical avatar promotion.

Run the offline guard checks with `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_restore.py`. They use in-memory WAVs and mocked file/network boundaries; they do not read credentials or submit jobs. No commits or shared approval records are part of this adapter task.
