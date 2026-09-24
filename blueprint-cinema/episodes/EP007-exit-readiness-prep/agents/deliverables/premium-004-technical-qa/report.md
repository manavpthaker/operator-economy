# EP007 premium 004 independent technical QA

Additional rough-cut QA is in the later sections of this report. The candidate assessment below remains historical evidence; later render checks identify their own exact hashes. The initial generation-ledger hash was current when the candidate packet completed and is retained as a snapshot, not asserted to remain the final ledger hash.

Status: complete for the delegated independent QA packet; original C and candidates 401–407 reviewed. This read-only assessment does not advance a production gate. The user has selected **404 Seedance as the preferred avatar performance**; that judgment is preserved. Candidate **407 passes the technical prerequisites for a rough-cut test of the synchronized 404 performance**, subject to root's normal-speed performance review.

Reviewer: `verify_revision`, technical integrity and sampled performance. Review date: 2026-09-09 UTC. Environment: local FFmpeg 8.1.1, FFprobe, Python/NumPy/Pillow, exact source-video frame extractions. Root separately owns normal-speed audiovisual comparison and integration.

## Current finding

401 is the closest of the three film candidates to the requested gaze/stop timing and fixed composition. It is not an exact timing pass: its lips remain parted at 6.5 seconds and settle by the 6.75-second sample. 402 stops early; 403 stops much too early. A parted mouth in sampled stills does not establish continued speech articulation.

404 has substantially more visible articulation than a stationary presenter, but its raw audio does not preserve the locked recording and introduces an approximately 0.29-second initial speech onset. It cannot be treated as a synchronized replacement simply by substituting the locked voiceover. Phoneme-level timing was not established by this technical pass.

407 corrects that recording/onset issue: its embedded audio matches the locked recording at zero lag, the revised mouth is visibly active from frame 0, and the same-timestamp samples preserve 404's framing, head positions and blinks. This establishes a technically viable repaired source for the rough cut, not a claim of perfect phoneme-level synchronization.

## Media integrity

| Input | Picture | Video duration | Frames | Audio | Decode |
|---|---|---:|---:|---|---|
| Original Kling C | 1916 × 1080, 24 fps | 9.041667 s | 217 | No audio stream | Pass |
| 401 Kling 3.0 Pro | 1916 × 1080, 24 fps | 9.041667 s | 217 | No audio stream | Pass |
| 402 Seedance 2.5 | 1920 × 1080, 24 fps | 9.041667 s | 217 | No audio stream | Pass |
| 403 Cinematic Studio 3.0 | 1920 × 1080, 24 fps | 9.041667 s | 217 | No audio stream | Pass |
| 404 Seedance 2.5 presenter | 1920 × 1080, 24 fps | 12.041667 s | 289 | 32 kHz stereo; 12.050000 s | Pass |
| 405 OmniHuman 1.5 | 1248 × 704, 25 fps | 11.560000 s | 289 | 48 kHz mono; 11.340000 s | Pass |
| 406 Kling Avatar v2 Pro | 1920 × 1072, 30 fps | 12.266667 s | 368 | 44.1 kHz stereo; 11.353991 s | Pass |
| 407 Seedance + Sync 3 | 1920 × 1080, 24 fps | 11.375000 s | 273 | 48 kHz mono; 11.340000 s | Pass |

All listed sources completed full video/audio decode without reported errors. The requested 9- and 12-second generations each contain one extra 24 fps video frame. Selection/conform should use explicit source ranges, not assume the provider duration equals the request exactly.

## Film observations

The common prompt requests a raised gaze and continuing answer until approximately 5.5 seconds, a stop and slight gaze drop during 5.5–6.5 seconds, then a quiet unresolved hold. It also requests a fixed camera and the same workshop/reference framing. The planned source select ends at 6.916667 seconds.

| Candidate | Observable result | Finding |
|---|---|---|
| Original C | Buyer shoulder disappears from the composition around 4 seconds; owner settles into lowered consideration later. | Comparison baseline. Framing is less stable than 401. |
| 401 | Buyer shoulder remains visible. Gaze remains raised through the 5.75-second sample, lowers at approximately 6 seconds. Lips are still parted at 6.5 seconds and closed by 6.75 seconds. Initial delivery is more restrained than 402. | Closest timing fit of these three, with a small late mouth-settle concern. Sampled stills cannot prove uninterrupted articulation through 5.5 seconds. |
| 402 | A larger open-hand gesture and more animated face accompany the answer. Mouth is closed by the 4.5-second sample. Gaze is down by 5.25 seconds. She looks back up by 8.875 seconds. | Major: answer/stop transition is early. Late gaze recovery violates the requested full-take ending but occurs outside the planned 0–6.916667-second select. |
| 403 | Framing differs from the reference from frame 0: buyer is an edge crop. Owner has lowered her gaze and stopped by the 2-second sample, then holds down through the remainder. | Major: action is several seconds early; not a timing-compatible replacement under the common prompt. |

Evidence: whole-take contact sheets for every source, plus quarter-second stop-window sheets for 401 and 402. The contacts preserve source frame numbers and timestamps.

## Presenter 404 raw audio analysis

Reference file: `identity-11.34.wav`, independently confirmed byte-identical to the staged `identity.wav`. SHA-256: `8d80cbb01c89533cb5f3338887818aaae00107835b1f9c166071502e077ab0f7`.

Each source was decoded independently to 8 kHz mono float32 PCM. Checks used Pearson waveform correlation, global FFT cross-correlation over ±2 seconds, normalized active 0.5-second windows over ±0.5 seconds, and 10 ms RMS energy bins.

- Zero-lag waveform correlation: **−0.006323**.
- Best global alignment: **0.100307** correlation at **+1.317375 seconds**.
- Active-window best correlations are weak, approximately **0.107–0.390** in absolute magnitude, with inconsistent offsets from approximately **−0.474 to +0.468 seconds**.
- Reference has strong audio from time 0. Candidate 404's first two 100 ms bins have RMS **0.000491** and **0.000530**; its first substantial onset occurs around **0.29 seconds**.
- Decoded source audio length is **12.064 seconds**, including codec padding, versus **11.34 seconds** for the reference.

**Blocking for an exact locked-audio replacement:** 404's generated audio is not a codec-only reproduction of the supplied recording and does not preserve its initial onset. Weak waveform correlation alone does not establish exact phoneme timing after possible voice resynthesis. It establishes that this is different audio. Do not call a locked-VO overdub synchronized without separately validating the mouth against that recording.

Visible performance at sampled frames includes clear mouth articulation, ordinary blinking, eyebrow response and modest head changes; no hand is visible in the sampled framing. The face, glasses, shirt and study remain recognizable. These observations do not constitute identity or performance approval.

## Presenter 405 alternate

OmniHuman preserves the reference recording and its timing within codec differences: zero-lag waveform correlation is **0.99998546**; all **22** active half-second windows have zero lag, with minimum correlation **0.99988848**. The 48 kHz mono audio stream duration is 11.34 seconds. The actual picture duration is 11.56 seconds at 25 fps, so the provider's returned 11.34-second duration does not describe the complete video stream.

Sampled performance shows clear articulation, several head tilts, and repeated two-hand gestures rising into the lower frame. It is more physically animated than user-selected 404. This is a tested alternate, not a change to that selection. Recording preservation does not, by itself, prove visual lip synchronization.

## Presenter 406 alternate

Kling Avatar v2 Pro also preserves the reference recording within codec differences: zero-lag waveform correlation **0.99996354**; all **22** active half-second windows have zero lag, minimum correlation **0.99978031**. The output uses 44.1 kHz stereo AAC and has a 11.353991-second audio stream; the 12.266667-second picture has a longer tail. Sampled performance shows ordinary blinks, restrained head movement and later low hand gestures. It remains an alternate and does not override the user's Seedance selection.

## Presenter 407 repair of selected 404

Audio identity/timing: **pass**, with zero-lag waveform correlation **0.99980151**, zero lag in all **22** active half-second windows, and minimum window correlation **0.99924262**. The embedded 48 kHz mono audio stream is **11.34 seconds**, preserving the locked recording's onset. The video is 273 frames at 24 fps, **11.375 seconds**, enough picture coverage for the planned 11.346667-second frame-aligned presenter slot.

Compared 407 with 404 at the same source timestamps: 0, 0.125, 0.25, 0.5, 0.75, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11 and 11.291667 seconds. The head position, camera framing, shoulders and blinks remain aligned in these samples. The revised mouth is visibly active from frame 0, where raw 404 was at rest. No retiming is visible in the sampled comparisons. Outside a generous face mask, 480-pixel comparison frames differ by at most **1.941 pixel levels out of 255** in mean absolute error, supporting preservation of the surrounding picture. This numerical test supports the visual comparison; it is not a full optical-flow or facial-landmark validation.

The mouth and lower face are re-rendered, and there are modest skin/lower-face appearance differences. These require normal-speed visual judgment, especially around rapid articulation. Full source decode passes. Contact sheets include early, middle and late matched pairs, with source frame numbers. No production approval is inferred from this technical pass.

Subsequent full-frame rough-cut inspection found a thin colored-noise strip in 407's bottom four source rows, with weak filter bleed two rows above. It is also present in the staged 407 file and absent from raw 404. The first contact-sheet pass did not identify this edge defect. The recommended correction is a four-pixel bottom overscan at 720p, preserving the original source and timing. Final render verification below determines whether the correction closes this finding.

## Limits and ownership

This packet does not select or stage a production asset, modify a request, alter source media, generate media, change a canonical file, or advance a gate. All QA writes remain in this owned deliverable folder. The source media are pre-existing AI generations; no external write, paid call or synthetic generation was performed by this reviewer.

No full-length playback approval is claimed. Root owns normal-speed viewing with original and locked audio, editorial comprehension, candidate selection, and any integration. Full word-level/phoneme-level synchronization remains a separate audiovisual check. The original 404 audio-identity defect is resolved in 407's embedded audio; the perceptual result of the lower-face reconstruction remains for root and the user to judge.

## Machine evidence and exact input hashes

The following record preserves the complete probes, decoded-audio window measurements, matched-frame measurements, input hashes and extraction timestamps used in this review.

```json
{
  "schema": "ep007-premium-004-independent-technical-qa-v1",
  "inputs": {
    "original-kling-c": {
      "path": "blueprint-cinema/experiments/EP007-PREMIUM-CONTROLLED-004/review-media/original-kling-c.mp4",
      "sha256": "8293c4bcc201259cb4624c94673690c1ec1d34a0bcdfa63464eae0a91feda60e",
      "bytes": 12328777,
      "probe": {
        "streams": [
          {
            "index": 0,
            "codec_name": "h264",
            "codec_long_name": "H.264 / AVC / MPEG-4 AVC / MPEG-4 part 10",
            "profile": "Main",
            "codec_type": "video",
            "codec_tag_string": "avc1",
            "codec_tag": "0x31637661",
            "mime_codec_string": "avc1.4d6032",
            "width": 1916,
            "height": 1080,
            "coded_width": 1916,
            "coded_height": 1080,
            "has_b_frames": 0,
            "pix_fmt": "yuv420p",
            "level": 50,
            "chroma_location": "left",
            "field_order": "progressive",
            "is_avc": "true",
            "nal_length_size": "4",
            "id": "0x1",
            "r_frame_rate": "24/1",
            "avg_frame_rate": "24/1",
            "time_base": "1/12288",
            "start_pts": 0,
            "start_time": "0.000000",
            "duration_ts": 111104,
            "duration": "9.041667",
            "bit_rate": "10906588",
            "bits_per_raw_sample": "8",
            "nb_frames": "217",
            "extradata_size": 40,
            "disposition": {
              "default": 1,
              "dub": 0,
              "original": 0,
              "comment": 0,
              "lyrics": 0,
              "karaoke": 0,
              "forced": 0,
              "hearing_impaired": 0,
              "visual_impaired": 0,
              "clean_effects": 0,
              "attached_pic": 0,
              "timed_thumbnails": 0,
              "non_diegetic": 0,
              "captions": 0,
              "descriptions": 0,
              "metadata": 0,
              "dependent": 0,
              "still_image": 0,
              "multilayer": 0
            },
            "tags": {
              "language": "und",
              "handler_name": "VideoHandler",
              "encoder": "Lavc60.31.102 h264_slapi"
            }
          }
        ],
        "format": {
          "filename": "blueprint-cinema/experiments/EP007-PREMIUM-CONTROLLED-004/review-media/original-kling-c.mp4",
          "nb_streams": 1,
          "nb_programs": 0,
          "nb_stream_groups": 0,
          "format_name": "mov,mp4,m4a,3gp,3g2,mj2",
          "format_long_name": "QuickTime / MOV",
          "start_time": "0.000000",
          "duration": "9.041667",
          "size": "12328777",
          "bit_rate": "10908410",
          "probe_score": 100,
          "tags": {
            "minor_version": "512",
            "major_brand": "isom",
            "compatible_brands": "isomiso2avc1mp41",
            "encoder": "Lavf60.16.100"
          }
        }
      },
      "full_decode_exit": 0,
      "full_decode_errors": "",
      "sample_frames": [
        0,
        12,
        24,
        48,
        72,
        96,
        120,
        132,
        144,
        156,
        168,
        192,
        213
      ],
      "contact_sheet": "blueprint-cinema/episodes/EP007-exit-readiness-prep/agents/deliverables/premium-004-technical-qa/contact-sheets/original-kling-c.jpg"
    },
    "401": {
      "path": "blueprint-cinema/experiments/EP007-PREMIUM-CONTROLLED-004/review-media/401.mp4",
      "sha256": "0aba7dba20772d37dd1418ea3aae79ed0f7ad64760b3b02befcd32ac5179ba26",
      "bytes": 10833281,
      "probe": {
        "streams": [
          {
            "index": 0,
            "codec_name": "h264",
            "codec_long_name": "H.264 / AVC / MPEG-4 AVC / MPEG-4 part 10",
            "profile": "Main",
            "codec_type": "video",
            "codec_tag_string": "avc1",
            "codec_tag": "0x31637661",
            "mime_codec_string": "avc1.4d6032",
            "width": 1916,
            "height": 1080,
            "coded_width": 1916,
            "coded_height": 1080,
            "has_b_frames": 0,
            "pix_fmt": "yuv420p",
            "level": 50,
            "chroma_location": "left",
            "field_order": "progressive",
            "is_avc": "true",
            "nal_length_size": "4",
            "id": "0x1",
            "r_frame_rate": "24/1",
            "avg_frame_rate": "24/1",
            "time_base": "1/12288",
            "start_pts": 0,
            "start_time": "0.000000",
            "duration_ts": 111104,
            "duration": "9.041667",
            "bit_rate": "9583377",
            "bits_per_raw_sample": "8",
            "nb_frames": "217",
            "extradata_size": 40,
            "disposition": {
              "default": 1,
              "dub": 0,
              "original": 0,
              "comment": 0,
              "lyrics": 0,
              "karaoke": 0,
              "forced": 0,
              "hearing_impaired": 0,
              "visual_impaired": 0,
              "clean_effects": 0,
              "attached_pic": 0,
              "timed_thumbnails": 0,
              "non_diegetic": 0,
              "captions": 0,
              "descriptions": 0,
              "metadata": 0,
              "dependent": 0,
              "still_image": 0,
              "multilayer": 0
            },
            "tags": {
              "language": "und",
              "handler_name": "VideoHandler",
              "encoder": "Lavc60.31.102 h264_slapi"
            }
          }
        ],
        "format": {
          "filename": "blueprint-cinema/experiments/EP007-PREMIUM-CONTROLLED-004/review-media/401.mp4",
          "nb_streams": 1,
          "nb_programs": 0,
          "nb_stream_groups": 0,
          "format_name": "mov,mp4,m4a,3gp,3g2,mj2",
          "format_long_name": "QuickTime / MOV",
          "start_time": "0.000000",
          "duration": "9.041667",
          "size": "10833281",
          "bit_rate": "9585206",
          "probe_score": 100,
          "tags": {
            "minor_version": "512",
            "major_brand": "isom",
            "compatible_brands": "isomiso2avc1mp41",
            "encoder": "Lavf60.16.100"
          }
        }
      },
      "full_decode_exit": 0,
      "full_decode_errors": "",
      "sample_frames": [
        0,
        12,
        24,
        48,
        72,
        96,
        120,
        132,
        144,
        156,
        168,
        192,
        213
      ],
      "contact_sheet": "blueprint-cinema/episodes/EP007-exit-readiness-prep/agents/deliverables/premium-004-technical-qa/contact-sheets/401.jpg",
      "stop_timing_contact_sheet": "blueprint-cinema/episodes/EP007-exit-readiness-prep/agents/deliverables/premium-004-technical-qa/contact-sheets/401-stop-timing.jpg"
    },
    "402": {
      "path": "blueprint-cinema/experiments/EP007-PREMIUM-CONTROLLED-004/review-media/402.mp4",
      "sha256": "01ffbad66972eb89718619d41fd6b82c7b6cee734c1b0c34db07dc2c7aabf290",
      "bytes": 14080493,
      "probe": {
        "streams": [
          {
            "index": 0,
            "codec_name": "hevc",
            "codec_long_name": "H.265 / HEVC (High Efficiency Video Coding)",
            "profile": "Main 10",
            "codec_type": "video",
            "codec_tag_string": "hvc1",
            "codec_tag": "0x31637668",
            "width": 1920,
            "height": 1080,
            "coded_width": 1920,
            "coded_height": 1080,
            "has_b_frames": 2,
            "pix_fmt": "yuv420p10le",
            "level": 120,
            "color_range": "tv",
            "color_space": "bt709",
            "color_transfer": "bt709",
            "color_primaries": "bt709",
            "chroma_location": "left",
            "field_order": "progressive",
            "view_ids_available": "",
            "view_pos_available": "",
            "id": "0x1",
            "r_frame_rate": "24/1",
            "avg_frame_rate": "24/1",
            "time_base": "1/90000",
            "start_pts": 0,
            "start_time": "0.000000",
            "duration_ts": 813750,
            "duration": "9.041667",
            "bit_rate": "12433552",
            "nb_frames": "217",
            "extradata_size": 2441,
            "disposition": {
              "default": 1,
              "dub": 0,
              "original": 0,
              "comment": 0,
              "lyrics": 0,
              "karaoke": 0,
              "forced": 0,
              "hearing_impaired": 0,
              "visual_impaired": 0,
              "clean_effects": 0,
              "attached_pic": 0,
              "timed_thumbnails": 0,
              "non_diegetic": 0,
              "captions": 0,
              "descriptions": 0,
              "metadata": 0,
              "dependent": 0,
              "still_image": 0,
              "multilayer": 0
            },
            "tags": {
              "language": "und",
              "handler_name": "VideoHandler"
            }
          }
        ],
        "format": {
          "filename": "blueprint-cinema/experiments/EP007-PREMIUM-CONTROLLED-004/review-media/402.mp4",
          "nb_streams": 1,
          "nb_programs": 0,
          "nb_stream_groups": 0,
          "format_name": "mov,mp4,m4a,3gp,3g2,mj2",
          "format_long_name": "QuickTime / MOV",
          "start_time": "0.000000",
          "duration": "9.041667",
          "size": "14080493",
          "bit_rate": "12458315",
          "probe_score": 100,
          "tags": {
            "major_brand": "isom",
            "minor_version": "512",
            "compatible_brands": "isomiso2mp41",
            "encoder": "Lavf58.76.100"
          }
        }
      },
      "full_decode_exit": 0,
      "full_decode_errors": "",
      "sample_frames": [
        0,
        12,
        24,
        48,
        72,
        96,
        120,
        132,
        144,
        156,
        168,
        192,
        213
      ],
      "contact_sheet": "blueprint-cinema/episodes/EP007-exit-readiness-prep/agents/deliverables/premium-004-technical-qa/contact-sheets/402.jpg",
      "stop_timing_contact_sheet": "blueprint-cinema/episodes/EP007-exit-readiness-prep/agents/deliverables/premium-004-technical-qa/contact-sheets/402-stop-timing.jpg"
    },
    "404": {
      "path": "blueprint-cinema/experiments/EP007-PREMIUM-CONTROLLED-004/review-media/404.mp4",
      "sha256": "a0de31c36bde22219a1e067178b86cf750e7da1f11a69a775c370c82df6f29dd",
      "bytes": 17448424,
      "probe": {
        "streams": [
          {
            "index": 0,
            "codec_name": "hevc",
            "codec_long_name": "H.265 / HEVC (High Efficiency Video Coding)",
            "profile": "Main 10",
            "codec_type": "video",
            "codec_tag_string": "hvc1",
            "codec_tag": "0x31637668",
            "width": 1920,
            "height": 1080,
            "coded_width": 1920,
            "coded_height": 1080,
            "has_b_frames": 2,
            "pix_fmt": "yuv420p10le",
            "level": 120,
            "color_range": "tv",
            "color_space": "bt709",
            "color_transfer": "bt709",
            "color_primaries": "bt709",
            "chroma_location": "left",
            "field_order": "progressive",
            "view_ids_available": "",
            "view_pos_available": "",
            "id": "0x1",
            "r_frame_rate": "24/1",
            "avg_frame_rate": "24/1",
            "time_base": "1/90000",
            "start_pts": 0,
            "start_time": "0.000000",
            "duration_ts": 1083750,
            "duration": "12.041667",
            "bit_rate": "11322635",
            "nb_frames": "289",
            "extradata_size": 2441,
            "disposition": {
              "default": 1,
              "dub": 0,
              "original": 0,
              "comment": 0,
              "lyrics": 0,
              "karaoke": 0,
              "forced": 0,
              "hearing_impaired": 0,
              "visual_impaired": 0,
              "clean_effects": 0,
              "attached_pic": 0,
              "timed_thumbnails": 0,
              "non_diegetic": 0,
              "captions": 0,
              "descriptions": 0,
              "metadata": 0,
              "dependent": 0,
              "still_image": 0,
              "multilayer": 0
            },
            "tags": {
              "language": "und",
              "handler_name": "VideoHandler"
            }
          },
          {
            "index": 1,
            "codec_name": "aac",
            "codec_long_name": "AAC (Advanced Audio Coding)",
            "profile": "LC",
            "codec_type": "audio",
            "codec_tag_string": "mp4a",
            "codec_tag": "0x6134706d",
            "mime_codec_string": "mp4a.40.2",
            "sample_fmt": "fltp",
            "sample_rate": "32000",
            "channels": 2,
            "channel_layout": "stereo",
            "bits_per_sample": 0,
            "initial_padding": 0,
            "id": "0x2",
            "r_frame_rate": "0/0",
            "avg_frame_rate": "0/0",
            "time_base": "1/32000",
            "start_pts": 0,
            "start_time": "0.000000",
            "duration_ts": 385600,
            "duration": "12.050000",
            "bit_rate": "245840",
            "nb_frames": "378",
            "extradata_size": 5,
            "disposition": {
              "default": 1,
              "dub": 0,
              "original": 0,
              "comment": 0,
              "lyrics": 0,
              "karaoke": 0,
              "forced": 0,
              "hearing_impaired": 0,
              "visual_impaired": 0,
              "clean_effects": 0,
              "attached_pic": 0,
              "timed_thumbnails": 0,
              "non_diegetic": 0,
              "captions": 0,
              "descriptions": 0,
              "metadata": 0,
              "dependent": 0,
              "still_image": 0,
              "multilayer": 0
            },
            "tags": {
              "language": "und",
              "handler_name": "SoundHandler"
            }
          }
        ],
        "format": {
          "filename": "blueprint-cinema/experiments/EP007-PREMIUM-CONTROLLED-004/review-media/404.mp4",
          "nb_streams": 2,
          "nb_programs": 0,
          "nb_stream_groups": 0,
          "format_name": "mov,mp4,m4a,3gp,3g2,mj2",
          "format_long_name": "QuickTime / MOV",
          "start_time": "0.000000",
          "duration": "12.050000",
          "size": "17448424",
          "bit_rate": "11584015",
          "probe_score": 100,
          "tags": {
            "major_brand": "isom",
            "minor_version": "512",
            "compatible_brands": "isomiso2mp41",
            "encoder": "Lavf58.76.100"
          }
        }
      },
      "full_decode_exit": 0,
      "full_decode_errors": "",
      "sample_frames": [
        0,
        4,
        12,
        24,
        48,
        72,
        96,
        120,
        144,
        168,
        192,
        216,
        240,
        264,
        285
      ],
      "contact_sheet": "blueprint-cinema/episodes/EP007-exit-readiness-prep/agents/deliverables/premium-004-technical-qa/contact-sheets/404.jpg",
      "audio_reference_alignment": {
        "reference_file_sha256": "8d80cbb01c89533cb5f3338887818aaae00107835b1f9c166071502e077ab0f7",
        "output_file_sha256": "a0de31c36bde22219a1e067178b86cf750e7da1f11a69a775c370c82df6f29dd",
        "method": "Decode source output audio and locked WAV independently to 8 kHz mono float32 PCM. Pearson correlation at zero lag, FFT cross-correlation over +/-2 seconds, and normalized half-second active windows over +/-0.5 seconds. Positive lag means output audio follows reference.",
        "reference_decoded_samples": 90720,
        "output_decoded_samples": 96512,
        "reference_duration_seconds": 11.34,
        "output_decoded_duration_seconds": 12.064,
        "reference_decoded_pcm_sha256": "26818fa9f2dd463480269f214fcc94f68d638a7c086f3352f42440ce0d54b19d",
        "output_decoded_pcm_sha256": "b94f3407c3358a0e77691d4b4a60442395a3cd88a29e66d146b3a288b7470986",
        "correlation_zero_lag": -0.006322935908054644,
        "global_best_lag_seconds": 1.317375,
        "global_best_lag_correlation": 0.10030673422452359,
        "active_windows": [
          {
            "reference_start_seconds": 0.0,
            "window_seconds": 0.5,
            "best_lag_seconds": 0.35025,
            "best_correlation": 0.2483122880554869,
            "rms_reference": 0.14780843384595987
          },
          {
            "reference_start_seconds": 0.5,
            "window_seconds": 0.5,
            "best_lag_seconds": 0.46813,
            "best_correlation": 0.13698012087783687,
            "rms_reference": 0.07153725989268965
          },
          {
            "reference_start_seconds": 1.0,
            "window_seconds": 0.5,
            "best_lag_seconds": 0.24775,
            "best_correlation": 0.20307886082844465,
            "rms_reference": 0.04247180139980512
          },
          {
            "reference_start_seconds": 1.5,
            "window_seconds": 0.5,
            "best_lag_seconds": -0.20925,
            "best_correlation": 0.1467274019448512,
            "rms_reference": 0.06862308292546904
          },
          {
            "reference_start_seconds": 2.0,
            "window_seconds": 0.5,
            "best_lag_seconds": -0.14,
            "best_correlation": 0.21829981245313504,
            "rms_reference": 0.15501411907924442
          },
          {
            "reference_start_seconds": 2.5,
            "window_seconds": 0.5,
            "best_lag_seconds": -0.302,
            "best_correlation": 0.2927598926344625,
            "rms_reference": 0.14354932137608828
          },
          {
            "reference_start_seconds": 3.0,
            "window_seconds": 0.5,
            "best_lag_seconds": -0.37762,
            "best_correlation": 0.25155644977385855,
            "rms_reference": 0.0767925722267585
          },
          {
            "reference_start_seconds": 3.5,
            "window_seconds": 0.5,
            "best_lag_seconds": -0.1735,
            "best_correlation": 0.15076793424839444,
            "rms_reference": 0.12274184123529769
          },
          {
            "reference_start_seconds": 4.0,
            "window_seconds": 0.5,
            "best_lag_seconds": 0.4205,
            "best_correlation": 0.14011941182968876,
            "rms_reference": 0.14174086298591448
          },
          {
            "reference_start_seconds": 4.5,
            "window_seconds": 0.5,
            "best_lag_seconds": 0.056,
            "best_correlation": 0.17144448429361253,
            "rms_reference": 0.08615776226237849
          },
          {
            "reference_start_seconds": 5.0,
            "window_seconds": 0.5,
            "best_lag_seconds": 0.00438,
            "best_correlation": -0.10715270752161907,
            "rms_reference": 0.03627870049415619
          },
          {
            "reference_start_seconds": 5.5,
            "window_seconds": 0.5,
            "best_lag_seconds": 0.411,
            "best_correlation": 0.1854402927201551,
            "rms_reference": 0.1260542956974227
          },
          {
            "reference_start_seconds": 6.0,
            "window_seconds": 0.5,
            "best_lag_seconds": 0.1925,
            "best_correlation": 0.2860418621773968,
            "rms_reference": 0.09660989366933473
          },
          {
            "reference_start_seconds": 6.5,
            "window_seconds": 0.5,
            "best_lag_seconds": -0.31325,
            "best_correlation": 0.3904503494168763,
            "rms_reference": 0.062129217449759695
          },
          {
            "reference_start_seconds": 7.0,
            "window_seconds": 0.5,
            "best_lag_seconds": -0.47363,
            "best_correlation": 0.32401675884530295,
            "rms_reference": 0.00844690372331599
          },
          {
            "reference_start_seconds": 7.5,
            "window_seconds": 0.5,
            "best_lag_seconds": -0.19475,
            "best_correlation": 0.21252262336296648,
            "rms_reference": 0.11923468798461981
          },
          {
            "reference_start_seconds": 8.0,
            "window_seconds": 0.5,
            "best_lag_seconds": 0.4425,
            "best_correlation": 0.18260221952269573,
            "rms_reference": 0.100511674233824
          },
          {
            "reference_start_seconds": 8.5,
            "window_seconds": 0.5,
            "best_lag_seconds": -0.34987,
            "best_correlation": 0.18839559165820433,
            "rms_reference": 0.13596609135568422
          },
          {
            "reference_start_seconds": 9.0,
            "window_seconds": 0.5,
            "best_lag_seconds": -0.468,
            "best_correlation": 0.2646715860487009,
            "rms_reference": 0.08909059178279467
          },
          {
            "reference_start_seconds": 9.5,
            "window_seconds": 0.5,
            "best_lag_seconds": -0.35287,
            "best_correlation": 0.2765482706458735,
            "rms_reference": 0.14577299496445517
          },
          {
            "reference_start_seconds": 10.0,
            "window_seconds": 0.5,
            "best_lag_seconds": 0.13925,
            "best_correlation": 0.19452452660643627,
            "rms_reference": 0.07031341322146772
          }
        ],
        "exact_audio_timing_preserved": null,
        "assessment": "FAIL for locked audio identity. Output is not a codec-only reproduction of the locked reference. Low waveform correlation and inconsistent alignment do not establish exact phoneme timing after possible voice resynthesis. Exact lip-sync to locked VO remains unverified; do not replace raw audio with locked VO and call the avatar synchronized.",
        "locked_recording_preserved": false,
        "coarse_energy_onsets_10ms_bins": {
          "identity.wav": {
            "threshold_rms": 0.03632213830947876,
            "first_active_bin_seconds": 0.0,
            "last_active_bin_seconds": 11.34,
            "rms_100ms_first_second": [
              0.209619,
              0.048461,
              0.116418,
              0.163745,
              0.150275,
              0.067862,
              0.096803,
              0.06803,
              0.066847,
              0.050151
            ]
          },
          "404.mp4": {
            "threshold_rms": 0.03373936414718628,
            "first_active_bin_seconds": 0.29,
            "last_active_bin_seconds": 11.59,
            "rms_100ms_first_second": [
              0.000491,
              0.00053,
              0.01391,
              0.177433,
              0.143126,
              0.004385,
              0.094143,
              0.090567,
              0.074673,
              0.027952
            ]
          }
        }
      }
    },
    "403": {
      "path": "blueprint-cinema/experiments/EP007-PREMIUM-CONTROLLED-004/review-media/403.mp4",
      "sha256": "8d0db25a4135eba56939a4aeb370697bddd88af1a6733a3fc7db5744f0afc664",
      "bytes": 5387802,
      "probe": {
        "streams": [
          {
            "index": 0,
            "codec_name": "h264",
            "codec_long_name": "H.264 / AVC / MPEG-4 AVC / MPEG-4 part 10",
            "profile": "High",
            "codec_type": "video",
            "codec_tag_string": "avc1",
            "codec_tag": "0x31637661",
            "mime_codec_string": "avc1.640028",
            "width": 1920,
            "height": 1080,
            "coded_width": 1920,
            "coded_height": 1080,
            "has_b_frames": 2,
            "pix_fmt": "yuv420p",
            "level": 40,
            "chroma_location": "left",
            "field_order": "progressive",
            "is_avc": "true",
            "nal_length_size": "4",
            "id": "0x1",
            "r_frame_rate": "24/1",
            "avg_frame_rate": "24/1",
            "time_base": "1/12288",
            "start_pts": 0,
            "start_time": "0.000000",
            "duration_ts": 111104,
            "duration": "9.041667",
            "bit_rate": "4744773",
            "bits_per_raw_sample": "8",
            "nb_frames": "217",
            "extradata_size": 46,
            "disposition": {
              "default": 1,
              "dub": 0,
              "original": 0,
              "comment": 0,
              "lyrics": 0,
              "karaoke": 0,
              "forced": 0,
              "hearing_impaired": 0,
              "visual_impaired": 0,
              "clean_effects": 0,
              "attached_pic": 0,
              "timed_thumbnails": 0,
              "non_diegetic": 0,
              "captions": 0,
              "descriptions": 0,
              "metadata": 0,
              "dependent": 0,
              "still_image": 0,
              "multilayer": 0
            },
            "tags": {
              "language": "und",
              "handler_name": "VideoHandler"
            }
          }
        ],
        "format": {
          "filename": "blueprint-cinema/experiments/EP007-PREMIUM-CONTROLLED-004/review-media/403.mp4",
          "nb_streams": 1,
          "nb_programs": 0,
          "nb_stream_groups": 0,
          "format_name": "mov,mp4,m4a,3gp,3g2,mj2",
          "format_long_name": "QuickTime / MOV",
          "start_time": "0.000000",
          "duration": "9.041667",
          "size": "5387802",
          "bit_rate": "4767087",
          "probe_score": 100,
          "tags": {
            "major_brand": "isom",
            "minor_version": "512",
            "compatible_brands": "isomiso2avc1mp41",
            "encoder": "Lavf58.76.100"
          }
        }
      },
      "full_decode_exit": 0,
      "full_decode_errors": "",
      "sample_frames": [
        0,
        12,
        24,
        48,
        72,
        96,
        120,
        132,
        144,
        156,
        168,
        192,
        213
      ],
      "contact_sheet": "blueprint-cinema/episodes/EP007-exit-readiness-prep/agents/deliverables/premium-004-technical-qa/contact-sheets/403.jpg"
    },
    "405": {
      "path": "blueprint-cinema/experiments/EP007-PREMIUM-CONTROLLED-004/review-media/405-omnihuman.mp4",
      "sha256": "a7f0daf43813217dfa632221a2118cb14cee1ea762a82b43d6ed6d1723c04f3b",
      "bytes": 3231737,
      "probe": {
        "streams": [
          {
            "index": 0,
            "codec_name": "h264",
            "codec_long_name": "H.264 / AVC / MPEG-4 AVC / MPEG-4 part 10",
            "profile": "High",
            "codec_type": "video",
            "codec_tag_string": "avc1",
            "codec_tag": "0x31637661",
            "mime_codec_string": "avc1.64001f",
            "width": 1248,
            "height": 704,
            "coded_width": 1248,
            "coded_height": 704,
            "has_b_frames": 2,
            "pix_fmt": "yuv420p",
            "level": 31,
            "chroma_location": "left",
            "field_order": "progressive",
            "is_avc": "true",
            "nal_length_size": "4",
            "id": "0x1",
            "r_frame_rate": "25/1",
            "avg_frame_rate": "25/1",
            "time_base": "1/12800",
            "start_pts": 0,
            "start_time": "0.000000",
            "duration_ts": 147968,
            "duration": "11.560000",
            "bit_rate": "2043433",
            "bits_per_raw_sample": "8",
            "nb_frames": "289",
            "extradata_size": 46,
            "disposition": {
              "default": 1,
              "dub": 0,
              "original": 0,
              "comment": 0,
              "lyrics": 0,
              "karaoke": 0,
              "forced": 0,
              "hearing_impaired": 0,
              "visual_impaired": 0,
              "clean_effects": 0,
              "attached_pic": 0,
              "timed_thumbnails": 0,
              "non_diegetic": 0,
              "captions": 0,
              "descriptions": 0,
              "metadata": 0,
              "dependent": 0,
              "still_image": 0,
              "multilayer": 0
            },
            "tags": {
              "language": "und",
              "handler_name": "VideoHandler",
              "encoder": "Lavc59.37.100 libx264"
            }
          },
          {
            "index": 1,
            "codec_name": "aac",
            "codec_long_name": "AAC (Advanced Audio Coding)",
            "profile": "LC",
            "codec_type": "audio",
            "codec_tag_string": "mp4a",
            "codec_tag": "0x6134706d",
            "mime_codec_string": "mp4a.40.2",
            "sample_fmt": "fltp",
            "sample_rate": "48000",
            "channels": 1,
            "channel_layout": "mono",
            "bits_per_sample": 0,
            "initial_padding": 0,
            "id": "0x2",
            "r_frame_rate": "0/0",
            "avg_frame_rate": "0/0",
            "time_base": "1/48000",
            "start_pts": 0,
            "start_time": "0.000000",
            "duration_ts": 544320,
            "duration": "11.340000",
            "bit_rate": "189264",
            "nb_frames": "533",
            "extradata_size": 5,
            "disposition": {
              "default": 1,
              "dub": 0,
              "original": 0,
              "comment": 0,
              "lyrics": 0,
              "karaoke": 0,
              "forced": 0,
              "hearing_impaired": 0,
              "visual_impaired": 0,
              "clean_effects": 0,
              "attached_pic": 0,
              "timed_thumbnails": 0,
              "non_diegetic": 0,
              "captions": 0,
              "descriptions": 0,
              "metadata": 0,
              "dependent": 0,
              "still_image": 0,
              "multilayer": 0
            },
            "tags": {
              "language": "und",
              "handler_name": "SoundHandler"
            }
          }
        ],
        "format": {
          "filename": "blueprint-cinema/experiments/EP007-PREMIUM-CONTROLLED-004/review-media/405-omnihuman.mp4",
          "nb_streams": 2,
          "nb_programs": 0,
          "nb_stream_groups": 0,
          "format_name": "mov,mp4,m4a,3gp,3g2,mj2",
          "format_long_name": "QuickTime / MOV",
          "start_time": "0.000000",
          "duration": "11.560000",
          "size": "3231737",
          "bit_rate": "2236496",
          "probe_score": 100,
          "tags": {
            "major_brand": "isom",
            "minor_version": "512",
            "compatible_brands": "isomiso2avc1mp41",
            "encoder": "Lavf59.27.100"
          }
        }
      },
      "full_decode_exit": 0,
      "full_decode_errors": "",
      "sample_frames": [
        0,
        5,
        12,
        25,
        50,
        75,
        100,
        125,
        150,
        175,
        200,
        225,
        250,
        275,
        282
      ],
      "contact_sheet": "blueprint-cinema/episodes/EP007-exit-readiness-prep/agents/deliverables/premium-004-technical-qa/contact-sheets/405.jpg",
      "audio_reference_alignment": {
        "method": "Same independent decoded-PCM correlation and active-window procedure as 404. Correlation measures audio waveform/timing identity, not visual lip synchronization.",
        "reference_file_sha256": "8d80cbb01c89533cb5f3338887818aaae00107835b1f9c166071502e077ab0f7",
        "output_file_sha256": "a7f0daf43813217dfa632221a2118cb14cee1ea762a82b43d6ed6d1723c04f3b",
        "reference_decoded_samples": 90720,
        "output_decoded_samples": 90795,
        "reference_duration_seconds": 11.34,
        "output_decoded_duration_seconds": 11.349375,
        "correlation_zero_lag": 0.9999854601217203,
        "global_best_lag_seconds": 0.0,
        "global_best_lag_correlation": 0.9999854601217203,
        "active_windows": [
          {
            "reference_start_seconds": 0.0,
            "window_seconds": 0.5,
            "best_lag_seconds": 0.0,
            "best_correlation": 0.9999801403670197
          },
          {
            "reference_start_seconds": 0.5,
            "window_seconds": 0.5,
            "best_lag_seconds": 0.0,
            "best_correlation": 0.9999643387762739
          },
          {
            "reference_start_seconds": 1.0,
            "window_seconds": 0.5,
            "best_lag_seconds": 0.0,
            "best_correlation": 0.999978951472375
          },
          {
            "reference_start_seconds": 1.5,
            "window_seconds": 0.5,
            "best_lag_seconds": 0.0,
            "best_correlation": 0.9999494048972541
          },
          {
            "reference_start_seconds": 2.0,
            "window_seconds": 0.5,
            "best_lag_seconds": 0.0,
            "best_correlation": 0.9999836483424341
          },
          {
            "reference_start_seconds": 2.5,
            "window_seconds": 0.5,
            "best_lag_seconds": 0.0,
            "best_correlation": 0.9999815157817495
          },
          {
            "reference_start_seconds": 3.0,
            "window_seconds": 0.5,
            "best_lag_seconds": 0.0,
            "best_correlation": 0.9999629158010449
          },
          {
            "reference_start_seconds": 3.5,
            "window_seconds": 0.5,
            "best_lag_seconds": 0.0,
            "best_correlation": 0.9999889426294797
          },
          {
            "reference_start_seconds": 4.0,
            "window_seconds": 0.5,
            "best_lag_seconds": 0.0,
            "best_correlation": 0.9999973352069669
          },
          {
            "reference_start_seconds": 4.5,
            "window_seconds": 0.5,
            "best_lag_seconds": 0.0,
            "best_correlation": 0.999986204280264
          },
          {
            "reference_start_seconds": 5.0,
            "window_seconds": 0.5,
            "best_lag_seconds": 0.0,
            "best_correlation": 0.9999801072192159
          },
          {
            "reference_start_seconds": 5.5,
            "window_seconds": 0.5,
            "best_lag_seconds": 0.0,
            "best_correlation": 0.9999826212663027
          },
          {
            "reference_start_seconds": 6.0,
            "window_seconds": 0.5,
            "best_lag_seconds": 0.0,
            "best_correlation": 0.999996074907088
          },
          {
            "reference_start_seconds": 6.5,
            "window_seconds": 0.5,
            "best_lag_seconds": 0.0,
            "best_correlation": 0.9999900684033592
          },
          {
            "reference_start_seconds": 7.0,
            "window_seconds": 0.5,
            "best_lag_seconds": 0.0,
            "best_correlation": 0.9998884838419266
          },
          {
            "reference_start_seconds": 7.5,
            "window_seconds": 0.5,
            "best_lag_seconds": 0.0,
            "best_correlation": 0.9999714304099954
          },
          {
            "reference_start_seconds": 8.0,
            "window_seconds": 0.5,
            "best_lag_seconds": 0.0,
            "best_correlation": 0.9999978603090759
          },
          {
            "reference_start_seconds": 8.5,
            "window_seconds": 0.5,
            "best_lag_seconds": 0.0,
            "best_correlation": 0.999993098154849
          },
          {
            "reference_start_seconds": 9.0,
            "window_seconds": 0.5,
            "best_lag_seconds": 0.0,
            "best_correlation": 0.9999960167918647
          },
          {
            "reference_start_seconds": 9.5,
            "window_seconds": 0.5,
            "best_lag_seconds": 0.0,
            "best_correlation": 0.9999936435910841
          },
          {
            "reference_start_seconds": 10.0,
            "window_seconds": 0.5,
            "best_lag_seconds": 0.0,
            "best_correlation": 0.9999822411216239
          },
          {
            "reference_start_seconds": 10.5,
            "window_seconds": 0.5,
            "best_lag_seconds": 0.0,
            "best_correlation": 0.999912920718303
          }
        ],
        "locked_recording_preserved": true,
        "exact_audio_timing_preserved": true,
        "assessment": "PASS for recording identity/timing within codec differences: strong correlation at zero lag throughout active reference windows. Visual lip synchronization is a separate check."
      }
    },
    "407": {
      "path": "blueprint-cinema/experiments/EP007-PREMIUM-CONTROLLED-004/review-media/407-seedance-sync3.mp4",
      "sha256": "1752e0356a3c0b86cbee70849e2b40df6de4ba483db103e9f2ef9904d606b965",
      "bytes": 10667198,
      "probe": {
        "streams": [
          {
            "index": 0,
            "codec_name": "aac",
            "codec_long_name": "AAC (Advanced Audio Coding)",
            "profile": "LC",
            "codec_type": "audio",
            "codec_tag_string": "mp4a",
            "codec_tag": "0x6134706d",
            "mime_codec_string": "mp4a.40.2",
            "sample_fmt": "fltp",
            "sample_rate": "48000",
            "channels": 1,
            "channel_layout": "mono",
            "bits_per_sample": 0,
            "initial_padding": 0,
            "id": "0x1",
            "r_frame_rate": "0/0",
            "avg_frame_rate": "0/0",
            "time_base": "1/48000",
            "start_pts": 0,
            "start_time": "0.000000",
            "duration_ts": 544320,
            "duration": "11.340000",
            "bit_rate": "208491",
            "nb_frames": "533",
            "extradata_size": 5,
            "disposition": {
              "default": 1,
              "dub": 0,
              "original": 0,
              "comment": 0,
              "lyrics": 0,
              "karaoke": 0,
              "forced": 0,
              "hearing_impaired": 0,
              "visual_impaired": 0,
              "clean_effects": 0,
              "attached_pic": 0,
              "timed_thumbnails": 0,
              "non_diegetic": 0,
              "captions": 0,
              "descriptions": 0,
              "metadata": 0,
              "dependent": 0,
              "still_image": 0,
              "multilayer": 0
            },
            "tags": {
              "language": "und",
              "handler_name": "SoundHandler"
            }
          },
          {
            "index": 1,
            "codec_name": "h264",
            "codec_long_name": "H.264 / AVC / MPEG-4 AVC / MPEG-4 part 10",
            "profile": "High 10",
            "codec_type": "video",
            "codec_tag_string": "avc1",
            "codec_tag": "0x31637661",
            "mime_codec_string": "avc1.6e0028",
            "width": 1920,
            "height": 1080,
            "coded_width": 1920,
            "coded_height": 1080,
            "has_b_frames": 2,
            "pix_fmt": "yuv420p10le",
            "level": 40,
            "color_range": "tv",
            "color_space": "bt709",
            "color_transfer": "bt709",
            "color_primaries": "bt709",
            "chroma_location": "left",
            "field_order": "progressive",
            "is_avc": "true",
            "nal_length_size": "4",
            "id": "0x2",
            "r_frame_rate": "24/1",
            "avg_frame_rate": "24/1",
            "time_base": "1/12288",
            "start_pts": 0,
            "start_time": "0.000000",
            "duration_ts": 139776,
            "duration": "11.375000",
            "bit_rate": "7277994",
            "bits_per_raw_sample": "10",
            "nb_frames": "273",
            "extradata_size": 51,
            "disposition": {
              "default": 1,
              "dub": 0,
              "original": 0,
              "comment": 0,
              "lyrics": 0,
              "karaoke": 0,
              "forced": 0,
              "hearing_impaired": 0,
              "visual_impaired": 0,
              "clean_effects": 0,
              "attached_pic": 0,
              "timed_thumbnails": 0,
              "non_diegetic": 0,
              "captions": 0,
              "descriptions": 0,
              "metadata": 0,
              "dependent": 0,
              "still_image": 0,
              "multilayer": 0
            },
            "tags": {
              "language": "und",
              "handler_name": "VideoHandler",
              "encoder": "Lavc61.19.101 libx264"
            }
          }
        ],
        "format": {
          "filename": "blueprint-cinema/experiments/EP007-PREMIUM-CONTROLLED-004/review-media/407-seedance-sync3.mp4",
          "nb_streams": 2,
          "nb_programs": 0,
          "nb_stream_groups": 0,
          "format_name": "mov,mp4,m4a,3gp,3g2,mj2",
          "format_long_name": "QuickTime / MOV",
          "start_time": "0.000000",
          "duration": "11.375000",
          "size": "10667198",
          "bit_rate": "7502205",
          "probe_score": 100,
          "tags": {
            "major_brand": "isom",
            "minor_version": "512",
            "compatible_brands": "isomiso2avc1mp41",
            "encoder": "Lavf61.7.100"
          }
        }
      },
      "full_decode_exit": 0,
      "full_decode_errors": "",
      "sample_frames": [
        0,
        3,
        6,
        12,
        18,
        24,
        48,
        72,
        96,
        120,
        144,
        168,
        192,
        216,
        240,
        264,
        271
      ],
      "contact_sheet": "blueprint-cinema/episodes/EP007-exit-readiness-prep/agents/deliverables/premium-004-technical-qa/contact-sheets/407-vs-404.jpg",
      "same_timestamp_404_comparison": [
        {
          "frame": 0,
          "time_seconds": 0.0,
          "whole_frame_mae": 2.536743827160494,
          "outside_face_mae": 1.8549255213505462,
          "upper_head_mae": 2.80959477124183,
          "mouth_region_mae": 9.983458868704771
        },
        {
          "frame": 3,
          "time_seconds": 0.125,
          "whole_frame_mae": 2.5134696502057614,
          "outside_face_mae": 1.8712148295266469,
          "upper_head_mae": 2.683372549019608,
          "mouth_region_mae": 9.94589671638852
        },
        {
          "frame": 6,
          "time_seconds": 0.25,
          "whole_frame_mae": 2.4357793209876544,
          "outside_face_mae": 1.9406885137371732,
          "upper_head_mae": 2.7031633986928103,
          "mouth_region_mae": 7.660463742430956
        },
        {
          "frame": 12,
          "time_seconds": 0.5,
          "whole_frame_mae": 2.636414609053498,
          "outside_face_mae": 1.8980139026812315,
          "upper_head_mae": 2.747137254901961,
          "mouth_region_mae": 12.663515974991386
        },
        {
          "frame": 18,
          "time_seconds": 0.75,
          "whole_frame_mae": 2.44261316872428,
          "outside_face_mae": 1.8160443561734525,
          "upper_head_mae": 2.6461960784313727,
          "mouth_region_mae": 10.4070792103579
        },
        {
          "frame": 24,
          "time_seconds": 1.0,
          "whole_frame_mae": 2.463487654320988,
          "outside_face_mae": 1.842148295266468,
          "upper_head_mae": 2.736392156862745,
          "mouth_region_mae": 10.446019790282085
        },
        {
          "frame": 48,
          "time_seconds": 2.0,
          "whole_frame_mae": 2.4080581275720165,
          "outside_face_mae": 1.852409798080106,
          "upper_head_mae": 2.561254901960784,
          "mouth_region_mae": 8.55905085413282
        },
        {
          "frame": 72,
          "time_seconds": 3.0,
          "whole_frame_mae": 2.724326131687243,
          "outside_face_mae": 1.8433763654419066,
          "upper_head_mae": 2.8738300653594773,
          "mouth_region_mae": 14.217397725594447
        },
        {
          "frame": 96,
          "time_seconds": 4.0,
          "whole_frame_mae": 2.7841718106995885,
          "outside_face_mae": 1.8347898047004303,
          "upper_head_mae": 2.6798692810457516,
          "mouth_region_mae": 16.435287746763155
        },
        {
          "frame": 120,
          "time_seconds": 5.0,
          "whole_frame_mae": 2.523860596707819,
          "outside_face_mae": 1.8827441244620986,
          "upper_head_mae": 2.794326797385621,
          "mouth_region_mae": 10.645645645645645
        },
        {
          "frame": 144,
          "time_seconds": 6.0,
          "whole_frame_mae": 2.670725308641975,
          "outside_face_mae": 1.8215888778550149,
          "upper_head_mae": 2.7456993464052286,
          "mouth_region_mae": 14.777088563973809
        },
        {
          "frame": 168,
          "time_seconds": 7.0,
          "whole_frame_mae": 2.5289197530864196,
          "outside_face_mae": 1.836524329692155,
          "upper_head_mae": 2.59359477124183,
          "mouth_region_mae": 11.910057598582188
        },
        {
          "frame": 192,
          "time_seconds": 8.0,
          "whole_frame_mae": 2.4137551440329217,
          "outside_face_mae": 1.8585302879841112,
          "upper_head_mae": 2.5239477124183005,
          "mouth_region_mae": 8.573179737114163
        },
        {
          "frame": 216,
          "time_seconds": 9.0,
          "whole_frame_mae": 2.6082870370370372,
          "outside_face_mae": 1.8502250910294604,
          "upper_head_mae": 2.684941176470588,
          "mouth_region_mae": 13.222025303992517
        },
        {
          "frame": 240,
          "time_seconds": 10.0,
          "whole_frame_mae": 2.348078703703704,
          "outside_face_mae": 1.8846507778881165,
          "upper_head_mae": 2.82718954248366,
          "mouth_region_mae": 8.037463693201397
        },
        {
          "frame": 264,
          "time_seconds": 11.0,
          "whole_frame_mae": 2.6987397119341563,
          "outside_face_mae": 1.8742866600463424,
          "upper_head_mae": 2.5373071895424837,
          "mouth_region_mae": 14.98173583419485
        },
        {
          "frame": 271,
          "time_seconds": 11.291666666666666,
          "whole_frame_mae": 2.176934156378601,
          "outside_face_mae": 1.8155081098973849,
          "upper_head_mae": 2.4470849673202615,
          "mouth_region_mae": 6.401023974794467
        }
      ],
      "audio_reference_alignment": {
        "method": "Independent decoded 8 kHz mono float32 PCM; global +/-2 s cross-correlation and normalized active half-second windows +/-0.5 s. Audio equality does not itself prove visible lip-sync.",
        "reference_file_sha256": "8d80cbb01c89533cb5f3338887818aaae00107835b1f9c166071502e077ab0f7",
        "output_file_sha256": "1752e0356a3c0b86cbee70849e2b40df6de4ba483db103e9f2ef9904d606b965",
        "correlation_zero_lag": 0.999801514490884,
        "global_best_lag_seconds": 0.0,
        "global_best_lag_correlation": 0.999801514490884,
        "active_windows": [
          {
            "reference_start_seconds": 0.0,
            "window_seconds": 0.5,
            "best_lag_seconds": 0.0,
            "best_correlation": 0.9996357546441129
          },
          {
            "reference_start_seconds": 0.5,
            "window_seconds": 0.5,
            "best_lag_seconds": 0.0,
            "best_correlation": 0.9997073908777351
          },
          {
            "reference_start_seconds": 1.0,
            "window_seconds": 0.5,
            "best_lag_seconds": 0.0,
            "best_correlation": 0.9997475885120094
          },
          {
            "reference_start_seconds": 1.5,
            "window_seconds": 0.5,
            "best_lag_seconds": 0.0,
            "best_correlation": 0.9998004352719376
          },
          {
            "reference_start_seconds": 2.0,
            "window_seconds": 0.5,
            "best_lag_seconds": 0.0,
            "best_correlation": 0.9998387406655743
          },
          {
            "reference_start_seconds": 2.5,
            "window_seconds": 0.5,
            "best_lag_seconds": 0.0,
            "best_correlation": 0.9997588787343454
          },
          {
            "reference_start_seconds": 3.0,
            "window_seconds": 0.5,
            "best_lag_seconds": 0.0,
            "best_correlation": 0.9995973988173671
          },
          {
            "reference_start_seconds": 3.5,
            "window_seconds": 0.5,
            "best_lag_seconds": 0.0,
            "best_correlation": 0.9998694835254798
          },
          {
            "reference_start_seconds": 4.0,
            "window_seconds": 0.5,
            "best_lag_seconds": 0.0,
            "best_correlation": 0.99992272390988
          },
          {
            "reference_start_seconds": 4.5,
            "window_seconds": 0.5,
            "best_lag_seconds": 0.0,
            "best_correlation": 0.999750282103713
          },
          {
            "reference_start_seconds": 5.0,
            "window_seconds": 0.5,
            "best_lag_seconds": 0.0,
            "best_correlation": 0.9997708855252165
          },
          {
            "reference_start_seconds": 5.5,
            "window_seconds": 0.5,
            "best_lag_seconds": 0.0,
            "best_correlation": 0.9998258529176377
          },
          {
            "reference_start_seconds": 6.0,
            "window_seconds": 0.5,
            "best_lag_seconds": 0.0,
            "best_correlation": 0.9998428118178997
          },
          {
            "reference_start_seconds": 6.5,
            "window_seconds": 0.5,
            "best_lag_seconds": 0.0,
            "best_correlation": 0.9998908921938684
          },
          {
            "reference_start_seconds": 7.0,
            "window_seconds": 0.5,
            "best_lag_seconds": 0.0,
            "best_correlation": 0.9992426248676403
          },
          {
            "reference_start_seconds": 7.5,
            "window_seconds": 0.5,
            "best_lag_seconds": 0.0,
            "best_correlation": 0.9998459665860284
          },
          {
            "reference_start_seconds": 8.0,
            "window_seconds": 0.5,
            "best_lag_seconds": 0.0,
            "best_correlation": 0.9998182809703392
          },
          {
            "reference_start_seconds": 8.5,
            "window_seconds": 0.5,
            "best_lag_seconds": 0.0,
            "best_correlation": 0.9998654871637332
          },
          {
            "reference_start_seconds": 9.0,
            "window_seconds": 0.5,
            "best_lag_seconds": 0.0,
            "best_correlation": 0.9997122300876128
          },
          {
            "reference_start_seconds": 9.5,
            "window_seconds": 0.5,
            "best_lag_seconds": 0.0,
            "best_correlation": 0.9997725193602433
          },
          {
            "reference_start_seconds": 10.0,
            "window_seconds": 0.5,
            "best_lag_seconds": 0.0,
            "best_correlation": 0.999791661944149
          },
          {
            "reference_start_seconds": 10.5,
            "window_seconds": 0.5,
            "best_lag_seconds": 0.0,
            "best_correlation": 0.9997271093402035
          }
        ],
        "locked_recording_preserved": true,
        "exact_audio_timing_preserved": true,
        "assessment": "PASS for audio identity/timing within codec differences; no added onset delay."
      },
      "visual_comparison_assessment": "Head positions, blinks, shoulders and framing preserved at the 17 sampled timestamps; mouth active from frame zero, with localized lower-face reconstruction differences. No retiming visible in these samples."
    },
    "406": {
      "path": "blueprint-cinema/experiments/EP007-PREMIUM-CONTROLLED-004/review-media/406-kling-avatar.mp4",
      "sha256": "d84a2898f19cc0b47d66b627ba19fe504df0942cfb7ef71cb3c014a3e9def903",
      "bytes": 6992665,
      "probe": {
        "streams": [
          {
            "index": 0,
            "codec_name": "aac",
            "codec_long_name": "AAC (Advanced Audio Coding)",
            "profile": "LC",
            "codec_type": "audio",
            "codec_tag_string": "mp4a",
            "codec_tag": "0x6134706d",
            "mime_codec_string": "mp4a.40.2",
            "sample_fmt": "fltp",
            "sample_rate": "44100",
            "channels": 2,
            "channel_layout": "stereo",
            "bits_per_sample": 0,
            "initial_padding": 0,
            "id": "0x1",
            "r_frame_rate": "0/0",
            "avg_frame_rate": "0/0",
            "time_base": "1/44100",
            "start_pts": 0,
            "start_time": "0.000000",
            "duration_ts": 500711,
            "duration": "11.353991",
            "bit_rate": "128116",
            "nb_frames": "491",
            "extradata_size": 2,
            "disposition": {
              "default": 1,
              "dub": 0,
              "original": 0,
              "comment": 0,
              "lyrics": 0,
              "karaoke": 0,
              "forced": 0,
              "hearing_impaired": 0,
              "visual_impaired": 0,
              "clean_effects": 0,
              "attached_pic": 0,
              "timed_thumbnails": 0,
              "non_diegetic": 0,
              "captions": 0,
              "descriptions": 0,
              "metadata": 0,
              "dependent": 0,
              "still_image": 0,
              "multilayer": 0
            },
            "tags": {
              "language": "und",
              "handler_name": "SoundHandler"
            }
          },
          {
            "index": 1,
            "codec_name": "h264",
            "codec_long_name": "H.264 / AVC / MPEG-4 AVC / MPEG-4 part 10",
            "profile": "Main",
            "codec_type": "video",
            "codec_tag_string": "avc1",
            "codec_tag": "0x31637661",
            "mime_codec_string": "avc1.4d6032",
            "width": 1920,
            "height": 1072,
            "coded_width": 1920,
            "coded_height": 1072,
            "has_b_frames": 0,
            "pix_fmt": "yuv420p",
            "level": 50,
            "chroma_location": "left",
            "field_order": "progressive",
            "is_avc": "true",
            "nal_length_size": "4",
            "id": "0x2",
            "r_frame_rate": "30/1",
            "avg_frame_rate": "30/1",
            "time_base": "1/15360",
            "start_pts": 0,
            "start_time": "0.000000",
            "duration_ts": 188416,
            "duration": "12.266667",
            "bit_rate": "4433943",
            "bits_per_raw_sample": "8",
            "nb_frames": "368",
            "extradata_size": 40,
            "disposition": {
              "default": 1,
              "dub": 0,
              "original": 0,
              "comment": 0,
              "lyrics": 0,
              "karaoke": 0,
              "forced": 0,
              "hearing_impaired": 0,
              "visual_impaired": 0,
              "clean_effects": 0,
              "attached_pic": 0,
              "timed_thumbnails": 0,
              "non_diegetic": 0,
              "captions": 0,
              "descriptions": 0,
              "metadata": 0,
              "dependent": 0,
              "still_image": 0,
              "multilayer": 0
            },
            "tags": {
              "language": "und",
              "handler_name": "VideoHandler",
              "encoder": "Lavc60.31.102 h264_slapi"
            }
          }
        ],
        "format": {
          "filename": "blueprint-cinema/experiments/EP007-PREMIUM-CONTROLLED-004/review-media/406-kling-avatar.mp4",
          "nb_streams": 2,
          "nb_programs": 0,
          "nb_stream_groups": 0,
          "format_name": "mov,mp4,m4a,3gp,3g2,mj2",
          "format_long_name": "QuickTime / MOV",
          "start_time": "0.000000",
          "duration": "12.266667",
          "size": "6992665",
          "bit_rate": "4560433",
          "probe_score": 100,
          "tags": {
            "minor_version": "512",
            "major_brand": "isom",
            "compatible_brands": "isomiso2avc1mp41",
            "encoder": "Lavf60.16.100"
          }
        }
      },
      "full_decode_exit": 0,
      "full_decode_errors": "",
      "sample_frames": [
        0,
        6,
        15,
        30,
        60,
        90,
        120,
        150,
        180,
        210,
        240,
        270,
        300,
        330,
        360
      ],
      "contact_sheet": "blueprint-cinema/episodes/EP007-exit-readiness-prep/agents/deliverables/premium-004-technical-qa/contact-sheets/406.jpg",
      "audio_reference_alignment": {
        "method": "Independent decoded 8 kHz mono float32 PCM; global +/-2 s cross-correlation and normalized active half-second windows +/-0.5 s. Audio equality does not itself prove visible lip-sync.",
        "reference_file_sha256": "8d80cbb01c89533cb5f3338887818aaae00107835b1f9c166071502e077ab0f7",
        "output_file_sha256": "d84a2898f19cc0b47d66b627ba19fe504df0942cfb7ef71cb3c014a3e9def903",
        "reference_decoded_samples": 90720,
        "output_decoded_samples": 90837,
        "correlation_zero_lag": 0.9999635448693908,
        "global_best_lag_seconds": 0.0,
        "global_best_lag_correlation": 0.9999635448693908,
        "active_windows": [
          {
            "reference_start_seconds": 0.0,
            "window_seconds": 0.5,
            "best_lag_seconds": 0.0,
            "best_correlation": 0.9999754948049494
          },
          {
            "reference_start_seconds": 0.5,
            "window_seconds": 0.5,
            "best_lag_seconds": 0.0,
            "best_correlation": 0.9999530766049938
          },
          {
            "reference_start_seconds": 1.0,
            "window_seconds": 0.5,
            "best_lag_seconds": 0.0,
            "best_correlation": 0.9999243998393699
          },
          {
            "reference_start_seconds": 1.5,
            "window_seconds": 0.5,
            "best_lag_seconds": 0.0,
            "best_correlation": 0.9999610140847106
          },
          {
            "reference_start_seconds": 2.0,
            "window_seconds": 0.5,
            "best_lag_seconds": 0.0,
            "best_correlation": 0.9999669026664443
          },
          {
            "reference_start_seconds": 2.5,
            "window_seconds": 0.5,
            "best_lag_seconds": 0.0,
            "best_correlation": 0.9999792796954966
          },
          {
            "reference_start_seconds": 3.0,
            "window_seconds": 0.5,
            "best_lag_seconds": 0.0,
            "best_correlation": 0.9999571164105221
          },
          {
            "reference_start_seconds": 3.5,
            "window_seconds": 0.5,
            "best_lag_seconds": 0.0,
            "best_correlation": 0.9999796251183609
          },
          {
            "reference_start_seconds": 4.0,
            "window_seconds": 0.5,
            "best_lag_seconds": 0.0,
            "best_correlation": 0.9999844716793765
          },
          {
            "reference_start_seconds": 4.5,
            "window_seconds": 0.5,
            "best_lag_seconds": 0.0,
            "best_correlation": 0.9999297103713595
          },
          {
            "reference_start_seconds": 5.0,
            "window_seconds": 0.5,
            "best_lag_seconds": 0.0,
            "best_correlation": 0.9999246557793053
          },
          {
            "reference_start_seconds": 5.5,
            "window_seconds": 0.5,
            "best_lag_seconds": 0.0,
            "best_correlation": 0.9999631316859474
          },
          {
            "reference_start_seconds": 6.0,
            "window_seconds": 0.5,
            "best_lag_seconds": 0.0,
            "best_correlation": 0.99995689279722
          },
          {
            "reference_start_seconds": 6.5,
            "window_seconds": 0.5,
            "best_lag_seconds": 0.0,
            "best_correlation": 0.999895100072275
          },
          {
            "reference_start_seconds": 7.0,
            "window_seconds": 0.5,
            "best_lag_seconds": 0.0,
            "best_correlation": 0.9997955928713387
          },
          {
            "reference_start_seconds": 7.5,
            "window_seconds": 0.5,
            "best_lag_seconds": 0.0,
            "best_correlation": 0.9999317670647434
          },
          {
            "reference_start_seconds": 8.0,
            "window_seconds": 0.5,
            "best_lag_seconds": 0.0,
            "best_correlation": 0.9999717835148216
          },
          {
            "reference_start_seconds": 8.5,
            "window_seconds": 0.5,
            "best_lag_seconds": 0.0,
            "best_correlation": 0.999961029582999
          },
          {
            "reference_start_seconds": 9.0,
            "window_seconds": 0.5,
            "best_lag_seconds": 0.0,
            "best_correlation": 0.9999516165071639
          },
          {
            "reference_start_seconds": 9.5,
            "window_seconds": 0.5,
            "best_lag_seconds": 0.0,
            "best_correlation": 0.9999821203241067
          },
          {
            "reference_start_seconds": 10.0,
            "window_seconds": 0.5,
            "best_lag_seconds": 0.0,
            "best_correlation": 0.9999358978859855
          },
          {
            "reference_start_seconds": 10.5,
            "window_seconds": 0.5,
            "best_lag_seconds": 0.0,
            "best_correlation": 0.9997803121732901
          }
        ],
        "locked_recording_preserved": true,
        "exact_audio_timing_preserved": true,
        "assessment": "PASS for audio identity and timing within codec differences; visual lip synchronization remains separate."
      }
    }
  },
  "limitations": [
    "Sampled-frame performance inspection does not substitute for full normal-speed playback.",
    "No owner performance approval or release gate approval."
  ],
  "checked_at": "2026-09-09T02:11:50.835877+00:00",
  "reference_hashes": [
    {
      "path": "blueprint-cinema/experiments/EP007-PREMIUM-CONTROLLED-004/GENERATION-RUN.json",
      "sha256": "c222c7183a72350233cbdcd6b2f811225683b1ab4b0c69b81758686e668e5a8a",
      "bytes": 11295
    },
    {
      "path": "blueprint-cinema/experiments/EP007-HIGGSFIELD-FROM-PHASE2-002/inputs/identity-11.34.wav",
      "sha256": "8d80cbb01c89533cb5f3338887818aaae00107835b1f9c166071502e077ab0f7",
      "bytes": 1088684
    },
    {
      "path": "blueprint-cinema/experiments/EP007-PREMIUM-CONTROLLED-004/review-media/identity.wav",
      "sha256": "8d80cbb01c89533cb5f3338887818aaae00107835b1f9c166071502e077ab0f7",
      "bytes": 1088684
    },
    {
      "path": "blueprint-cinema/experiments/EP007-HIGGSFIELD-FROM-PHASE2-002/inputs/avatar-candidate-03.webp",
      "sha256": "59309d2925b85cfba8a6a411dce1ecea67a03607f8a05933f4a2f6cb6af27754",
      "bytes": 903362
    },
    {
      "path": "blueprint-cinema/experiments/EP007-PREMIUM-CONTROLLED-004/FAL-REQUEST.json",
      "sha256": "938c27843e8fc78a0a42e248439b36aa378e2bb25251bece8507c2188ceb05d3",
      "bytes": 1262
    },
    {
      "path": "blueprint-cinema/experiments/EP007-PREMIUM-CONTROLLED-004/FAL-KLING-REQUEST.json",
      "sha256": "7714045b31078bd22f5e26c3ca0ac0a172b42fcdb26d02d3accf9897164eb480",
      "bytes": 1060
    },
    {
      "path": "blueprint-cinema/experiments/EP007-PREMIUM-CONTROLLED-004/FAL-SYNC-REQUEST.json",
      "sha256": "5d6fff105969cb64228941d13ae6e24cf5ec1a3276696a2b5ad89b2179a5649b",
      "bytes": 687
    }
  ],
  "reviewed_at": "2026-09-09T02:28:54.762492+00:00"
}
```

## Initial rough-cut technical probe (before edge correction)

```json
{
  "input_path": "blueprint-cinema/experiments/EP007-PREMIUM-CONTROLLED-004/review-media/ep007-original-film-seedance-hyperframes.mp4",
  "sha256": "47aed5247b2fb591b005aec9ae8981ac2233ca3793bb5b3fa646d405d8e33b71",
  "probe": {
    "streams": [
      {
        "index": 0,
        "codec_name": "h264",
        "codec_long_name": "H.264 / AVC / MPEG-4 AVC / MPEG-4 part 10",
        "profile": "High",
        "codec_type": "video",
        "codec_tag_string": "avc1",
        "codec_tag": "0x31637661",
        "mime_codec_string": "avc1.64001f",
        "width": 1280,
        "height": 720,
        "coded_width": 1280,
        "coded_height": 720,
        "has_b_frames": 0,
        "sample_aspect_ratio": "1:1",
        "display_aspect_ratio": "16:9",
        "pix_fmt": "yuv420p",
        "level": 31,
        "color_range": "tv",
        "color_space": "bt709",
        "color_transfer": "bt709",
        "color_primaries": "bt709",
        "chroma_location": "left",
        "field_order": "progressive",
        "refs": 5,
        "is_avc": "true",
        "nal_length_size": "4",
        "id": "0x1",
        "r_frame_rate": "30/1",
        "avg_frame_rate": "30/1",
        "time_base": "1/15360",
        "start_pts": 0,
        "start_time": "0.000000",
        "duration_ts": 919552,
        "duration": "59.866667",
        "bit_rate": "4501895",
        "bits_per_raw_sample": "8",
        "nb_frames": "1796",
        "nb_read_frames": "1796",
        "extradata_size": 50,
        "disposition": {
          "default": 1,
          "dub": 0,
          "original": 0,
          "comment": 0,
          "lyrics": 0,
          "karaoke": 0,
          "forced": 0,
          "hearing_impaired": 0,
          "visual_impaired": 0,
          "clean_effects": 0,
          "attached_pic": 0,
          "timed_thumbnails": 0,
          "non_diegetic": 0,
          "captions": 0,
          "descriptions": 0,
          "metadata": 0,
          "dependent": 0,
          "still_image": 0,
          "multilayer": 0
        },
        "tags": {
          "language": "und",
          "handler_name": "VideoHandler",
          "encoder": "Lavc62.28.101 libx264"
        }
      },
      {
        "index": 1,
        "codec_name": "aac",
        "codec_long_name": "AAC (Advanced Audio Coding)",
        "profile": "LC",
        "codec_type": "audio",
        "codec_tag_string": "mp4a",
        "codec_tag": "0x6134706d",
        "mime_codec_string": "mp4a.40.2",
        "sample_fmt": "fltp",
        "sample_rate": "48000",
        "channels": 2,
        "channel_layout": "stereo",
        "bits_per_sample": 0,
        "initial_padding": 0,
        "id": "0x2",
        "r_frame_rate": "0/0",
        "avg_frame_rate": "0/0",
        "time_base": "1/48000",
        "start_pts": 0,
        "start_time": "0.000000",
        "duration_ts": 2873568,
        "duration": "59.866000",
        "bit_rate": "181375",
        "nb_frames": "2808",
        "nb_read_frames": "2807",
        "extradata_size": 5,
        "disposition": {
          "default": 1,
          "dub": 0,
          "original": 0,
          "comment": 0,
          "lyrics": 0,
          "karaoke": 0,
          "forced": 0,
          "hearing_impaired": 0,
          "visual_impaired": 0,
          "clean_effects": 0,
          "attached_pic": 0,
          "timed_thumbnails": 0,
          "non_diegetic": 0,
          "captions": 0,
          "descriptions": 0,
          "metadata": 0,
          "dependent": 0,
          "still_image": 0,
          "multilayer": 0
        },
        "tags": {
          "language": "und",
          "handler_name": "SoundHandler"
        }
      }
    ],
    "format": {
      "filename": "blueprint-cinema/experiments/EP007-PREMIUM-CONTROLLED-004/review-media/ep007-original-film-seedance-hyperframes.mp4",
      "nb_streams": 2,
      "nb_programs": 0,
      "nb_stream_groups": 0,
      "format_name": "mov,mp4,m4a,3gp,3g2,mj2",
      "format_long_name": "QuickTime / MOV",
      "start_time": "0.000000",
      "duration": "59.866667",
      "size": "35100393",
      "bit_rate": "4690475",
      "probe_score": 100,
      "tags": {
        "minor_version": "512",
        "major_brand": "isom",
        "compatible_brands": "isomiso2avc1mp41",
        "hyperframes_version": "0.0.0-dev",
        "hyperframes_renderer": "hyperframes",
        "encoder": "Lavf62.12.101"
      }
    }
  },
  "full_decode_exit": 0,
  "full_decode_errors": "",
  "frames": [
    0,
    326,
    327,
    328,
    329,
    443,
    444,
    445,
    630,
    631,
    632,
    837,
    838,
    839,
    1052,
    1053,
    1054,
    1455,
    1456,
    1457,
    1620,
    1795
  ],
  "contact_sheet": "blueprint-cinema/episodes/EP007-exit-readiness-prep/agents/deliverables/premium-004-technical-qa/contact-sheets/rough-cut-initial-boundaries.jpg"
}
```

## Initial rough-cut audio check

```json
{
  "path": "blueprint-cinema/experiments/EP007-PREMIUM-CONTROLLED-004/review-media/ep007-original-film-seedance-hyperframes.pre-edge-fix.mp4",
  "sha256": "47aed5247b2fb591b005aec9ae8981ac2233ca3793bb5b3fa646d405d8e33b71",
  "reference_path": "blueprint-cinema/experiments/EP007-PREMIUM-CONTROLLED-004/review-media/opening-narration.wav",
  "reference_sha256": "fc85cf825771fb38031a35267c6a7726d3684d9d3deb0cab71ff68ef9d39098e",
  "sample_rate_for_comparison": 8000,
  "reference_samples": 478880,
  "output_samples": 479062,
  "correlation_zero_lag": 0.9998249039144848,
  "global_best_lag_seconds": 0.0,
  "active_half_second_windows": [
    {
      "start_seconds": 0.0,
      "lag_seconds": 0.0,
      "correlation": 0.9992662480648241
    },
    {
      "start_seconds": 0.5,
      "lag_seconds": 0.0,
      "correlation": 0.9997531301763604
    },
    {
      "start_seconds": 1.0,
      "lag_seconds": 0.0,
      "correlation": 0.9997147735516954
    },
    {
      "start_seconds": 1.5,
      "lag_seconds": 0.0,
      "correlation": 0.9999022295511794
    },
    {
      "start_seconds": 2.0,
      "lag_seconds": 0.0,
      "correlation": 0.9999898459449162
    },
    {
      "start_seconds": 2.5,
      "lag_seconds": 0.0,
      "correlation": 0.99996268104084
    },
    {
      "start_seconds": 3.0,
      "lag_seconds": 0.0,
      "correlation": 0.9998939220921872
    },
    {
      "start_seconds": 3.5,
      "lag_seconds": 0.0,
      "correlation": 0.9998341534344979
    },
    {
      "start_seconds": 4.0,
      "lag_seconds": 0.0,
      "correlation": 0.9999793972895659
    },
    {
      "start_seconds": 4.5,
      "lag_seconds": 0.0,
      "correlation": 0.9999769825751577
    },
    {
      "start_seconds": 5.0,
      "lag_seconds": 0.0,
      "correlation": 0.9999482618079046
    },
    {
      "start_seconds": 6.0,
      "lag_seconds": 0.0,
      "correlation": 0.9992851731470792
    },
    {
      "start_seconds": 6.5,
      "lag_seconds": 0.0,
      "correlation": 0.99984958551545
    },
    {
      "start_seconds": 7.5,
      "lag_seconds": 0.0,
      "correlation": 0.9998322093433161
    },
    {
      "start_seconds": 8.0,
      "lag_seconds": 0.0,
      "correlation": 0.9997088100976479
    },
    {
      "start_seconds": 8.5,
      "lag_seconds": 0.0,
      "correlation": 0.9998468730571494
    },
    {
      "start_seconds": 9.0,
      "lag_seconds": 0.0,
      "correlation": 0.9998600147550628
    },
    {
      "start_seconds": 9.5,
      "lag_seconds": 0.0,
      "correlation": 0.9993233832734058
    },
    {
      "start_seconds": 10.0,
      "lag_seconds": 0.0,
      "correlation": 0.9994484457220726
    },
    {
      "start_seconds": 11.0,
      "lag_seconds": 0.0,
      "correlation": 0.9999737966369029
    },
    {
      "start_seconds": 11.5,
      "lag_seconds": 0.0,
      "correlation": 0.9999879863419454
    },
    {
      "start_seconds": 12.0,
      "lag_seconds": 0.0,
      "correlation": 0.9998664506470931
    },
    {
      "start_seconds": 12.5,
      "lag_seconds": 0.0,
      "correlation": 0.9999460284898328
    },
    {
      "start_seconds": 13.0,
      "lag_seconds": 0.0,
      "correlation": 0.9998456496783819
    },
    {
      "start_seconds": 13.5,
      "lag_seconds": 0.0,
      "correlation": 0.9996048114880207
    },
    {
      "start_seconds": 14.0,
      "lag_seconds": 0.0,
      "correlation": 0.9997494493985848
    },
    {
      "start_seconds": 14.5,
      "lag_seconds": 0.0,
      "correlation": 0.9998545061003633
    },
    {
      "start_seconds": 15.0,
      "lag_seconds": 0.0,
      "correlation": 0.9997010347258759
    },
    {
      "start_seconds": 15.5,
      "lag_seconds": 0.0,
      "correlation": 0.999878147490594
    },
    {
      "start_seconds": 16.0,
      "lag_seconds": 0.0,
      "correlation": 0.9999408340675822
    },
    {
      "start_seconds": 16.5,
      "lag_seconds": 0.0,
      "correlation": 0.9999418416676418
    },
    {
      "start_seconds": 17.0,
      "lag_seconds": 0.0,
      "correlation": 0.9999417976513143
    },
    {
      "start_seconds": 17.5,
      "lag_seconds": 0.0,
      "correlation": 0.9999980704621415
    },
    {
      "start_seconds": 18.0,
      "lag_seconds": 0.0,
      "correlation": 0.9999952110745421
    },
    {
      "start_seconds": 18.5,
      "lag_seconds": 0.0,
      "correlation": 0.9999983679567539
    },
    {
      "start_seconds": 19.0,
      "lag_seconds": 0.0,
      "correlation": 0.9998885525863838
    },
    {
      "start_seconds": 19.5,
      "lag_seconds": 0.0,
      "correlation": 0.9998792245692925
    },
    {
      "start_seconds": 20.0,
      "lag_seconds": 0.0,
      "correlation": 0.999625120709858
    },
    {
      "start_seconds": 21.0,
      "lag_seconds": 0.0,
      "correlation": 0.9997992193832183
    },
    {
      "start_seconds": 21.5,
      "lag_seconds": 0.0,
      "correlation": 0.999584290945047
    },
    {
      "start_seconds": 22.0,
      "lag_seconds": 0.0,
      "correlation": 0.9997880934894063
    },
    {
      "start_seconds": 22.5,
      "lag_seconds": 0.0,
      "correlation": 0.9994491632952344
    },
    {
      "start_seconds": 23.0,
      "lag_seconds": 0.0,
      "correlation": 0.9999674977985004
    },
    {
      "start_seconds": 23.5,
      "lag_seconds": 0.0,
      "correlation": 0.9997636004757867
    },
    {
      "start_seconds": 24.0,
      "lag_seconds": 0.0,
      "correlation": 0.9999763007361601
    },
    {
      "start_seconds": 24.5,
      "lag_seconds": 0.0,
      "correlation": 0.9997668611321248
    },
    {
      "start_seconds": 25.5,
      "lag_seconds": 0.0,
      "correlation": 0.9997387830910063
    },
    {
      "start_seconds": 26.0,
      "lag_seconds": 0.0,
      "correlation": 0.9999559927115732
    },
    {
      "start_seconds": 26.5,
      "lag_seconds": 0.0,
      "correlation": 0.9993912739720925
    },
    {
      "start_seconds": 27.5,
      "lag_seconds": 0.0,
      "correlation": 0.9989021008206858
    },
    {
      "start_seconds": 28.0,
      "lag_seconds": 0.0,
      "correlation": 0.9998762305294153
    },
    {
      "start_seconds": 28.5,
      "lag_seconds": 0.0,
      "correlation": 0.9999724920607099
    },
    {
      "start_seconds": 29.0,
      "lag_seconds": 0.0,
      "correlation": 0.9999859613620488
    },
    {
      "start_seconds": 29.5,
      "lag_seconds": 0.0,
      "correlation": 0.9997890251103129
    },
    {
      "start_seconds": 30.0,
      "lag_seconds": 0.0,
      "correlation": 0.9996700218294517
    },
    {
      "start_seconds": 30.5,
      "lag_seconds": 0.0,
      "correlation": 0.9999707770792925
    },
    {
      "start_seconds": 31.0,
      "lag_seconds": 0.0,
      "correlation": 0.9999212218606498
    },
    {
      "start_seconds": 31.5,
      "lag_seconds": 0.0,
      "correlation": 0.9994641022119911
    },
    {
      "start_seconds": 32.0,
      "lag_seconds": 0.0,
      "correlation": 0.9997569761027225
    },
    {
      "start_seconds": 32.5,
      "lag_seconds": 0.0,
      "correlation": 0.9993836901396952
    },
    {
      "start_seconds": 33.0,
      "lag_seconds": 0.0,
      "correlation": 0.9994814039996337
    },
    {
      "start_seconds": 33.5,
      "lag_seconds": 0.0,
      "correlation": 0.9993080162505783
    },
    {
      "start_seconds": 34.5,
      "lag_seconds": 0.0,
      "correlation": 0.9999616652493175
    },
    {
      "start_seconds": 35.0,
      "lag_seconds": 0.0,
      "correlation": 0.9995754109336364
    },
    {
      "start_seconds": 35.5,
      "lag_seconds": 0.0,
      "correlation": 0.9996828754199304
    },
    {
      "start_seconds": 36.0,
      "lag_seconds": 0.0,
      "correlation": 0.9999920884577382
    },
    {
      "start_seconds": 36.5,
      "lag_seconds": 0.0,
      "correlation": 0.9998905923108993
    },
    {
      "start_seconds": 37.0,
      "lag_seconds": 0.0,
      "correlation": 0.9997875839967858
    },
    {
      "start_seconds": 37.5,
      "lag_seconds": 0.0,
      "correlation": 0.9999643596036022
    },
    {
      "start_seconds": 38.0,
      "lag_seconds": 0.0,
      "correlation": 0.9998130753486858
    },
    {
      "start_seconds": 38.5,
      "lag_seconds": 0.0,
      "correlation": 0.9999271139871689
    },
    {
      "start_seconds": 39.0,
      "lag_seconds": 0.0,
      "correlation": 0.9999856544034279
    },
    {
      "start_seconds": 39.5,
      "lag_seconds": 0.0,
      "correlation": 0.9998879233417768
    },
    {
      "start_seconds": 40.0,
      "lag_seconds": 0.0,
      "correlation": 0.999909841089613
    },
    {
      "start_seconds": 40.5,
      "lag_seconds": 0.0,
      "correlation": 0.9998968831681335
    },
    {
      "start_seconds": 41.0,
      "lag_seconds": 0.0,
      "correlation": 0.9996623323839097
    },
    {
      "start_seconds": 41.5,
      "lag_seconds": 0.0,
      "correlation": 0.9998598235452015
    },
    {
      "start_seconds": 42.0,
      "lag_seconds": 0.0,
      "correlation": 0.9997349303706985
    },
    {
      "start_seconds": 42.5,
      "lag_seconds": 0.0,
      "correlation": 0.9998012810835596
    },
    {
      "start_seconds": 43.0,
      "lag_seconds": 0.0,
      "correlation": 0.9997345826436247
    },
    {
      "start_seconds": 43.5,
      "lag_seconds": 0.0,
      "correlation": 0.999924842545721
    },
    {
      "start_seconds": 44.0,
      "lag_seconds": 0.0,
      "correlation": 0.9996648723559978
    },
    {
      "start_seconds": 48.5,
      "lag_seconds": 0.0,
      "correlation": 0.999997585623859
    },
    {
      "start_seconds": 49.0,
      "lag_seconds": 0.0,
      "correlation": 0.9998246681875098
    },
    {
      "start_seconds": 49.5,
      "lag_seconds": 0.0,
      "correlation": 0.999877367713948
    },
    {
      "start_seconds": 50.0,
      "lag_seconds": 0.0,
      "correlation": 0.9996377653153589
    },
    {
      "start_seconds": 50.5,
      "lag_seconds": 0.0,
      "correlation": 0.9999969547502344
    },
    {
      "start_seconds": 51.0,
      "lag_seconds": 0.0,
      "correlation": 0.9998138610845377
    },
    {
      "start_seconds": 51.5,
      "lag_seconds": 0.0,
      "correlation": 0.9995025156350082
    },
    {
      "start_seconds": 52.0,
      "lag_seconds": 0.0,
      "correlation": 0.9999501798206041
    },
    {
      "start_seconds": 52.5,
      "lag_seconds": 0.0,
      "correlation": 0.9999706210826016
    },
    {
      "start_seconds": 53.0,
      "lag_seconds": 0.0,
      "correlation": 0.9995309824919032
    },
    {
      "start_seconds": 53.5,
      "lag_seconds": 0.0,
      "correlation": 0.9996391732551954
    },
    {
      "start_seconds": 54.0,
      "lag_seconds": 0.0,
      "correlation": 0.9996470225182698
    },
    {
      "start_seconds": 54.5,
      "lag_seconds": 0.0,
      "correlation": 0.9997336601789845
    },
    {
      "start_seconds": 55.0,
      "lag_seconds": 0.0,
      "correlation": 0.9996530564669971
    },
    {
      "start_seconds": 55.5,
      "lag_seconds": 0.0,
      "correlation": 0.9996921212460896
    },
    {
      "start_seconds": 56.0,
      "lag_seconds": 0.0,
      "correlation": 0.9997867932834493
    },
    {
      "start_seconds": 56.5,
      "lag_seconds": 0.0,
      "correlation": 0.9999063428940079
    },
    {
      "start_seconds": 57.0,
      "lag_seconds": 0.0,
      "correlation": 0.9998811365045316
    },
    {
      "start_seconds": 57.5,
      "lag_seconds": 0.0,
      "correlation": 0.9999756703454507
    },
    {
      "start_seconds": 58.0,
      "lag_seconds": 0.0,
      "correlation": 0.9998214200729599
    },
    {
      "start_seconds": 58.5,
      "lag_seconds": 0.0,
      "correlation": 0.9996747869770004
    },
    {
      "start_seconds": 59.0,
      "lag_seconds": 0.0,
      "correlation": 0.9998932277755007
    }
  ],
  "assessment": "PASS. Locked narration content is preserved and active windows remain at zero lag within codec differences."
}
```

## R6 establishing extension inspection

```json
{
  "path": "blueprint-cinema/experiments/EP007-PREMIUM-CONTROLLED-004/hyperframes/assets/establishing.mp4",
  "sha256": "e0b4067004d83f4ba00be589d72ffc43d8305319a63be2217f19d594d6d2521c",
  "probe": {
    "streams": [
      {
        "index": 0,
        "codec_name": "h264",
        "codec_long_name": "H.264 / AVC / MPEG-4 AVC / MPEG-4 part 10",
        "profile": "Main",
        "codec_type": "video",
        "codec_tag_string": "avc1",
        "codec_tag": "0x31637661",
        "mime_codec_string": "avc1.4d6032",
        "width": 1916,
        "height": 1080,
        "coded_width": 1916,
        "coded_height": 1080,
        "has_b_frames": 0,
        "pix_fmt": "yuv420p",
        "level": 50,
        "chroma_location": "left",
        "field_order": "progressive",
        "is_avc": "true",
        "nal_length_size": "4",
        "id": "0x1",
        "r_frame_rate": "24/1",
        "avg_frame_rate": "24/1",
        "time_base": "1/12288",
        "start_pts": 0,
        "start_time": "0.000000",
        "duration_ts": 184832,
        "duration": "15.041667",
        "bit_rate": "8423499",
        "bits_per_raw_sample": "8",
        "nb_frames": "361",
        "extradata_size": 40,
        "disposition": {
          "default": 1,
          "dub": 0,
          "original": 0,
          "comment": 0,
          "lyrics": 0,
          "karaoke": 0,
          "forced": 0,
          "hearing_impaired": 0,
          "visual_impaired": 0,
          "clean_effects": 0,
          "attached_pic": 0,
          "timed_thumbnails": 0,
          "non_diegetic": 0,
          "captions": 0,
          "descriptions": 0,
          "metadata": 0,
          "dependent": 0,
          "still_image": 0,
          "multilayer": 0
        },
        "tags": {
          "language": "und",
          "handler_name": "VideoHandler",
          "encoder": "Lavc60.31.102 h264_slapi"
        }
      }
    ],
    "format": {
      "filename": "blueprint-cinema/experiments/EP007-PREMIUM-CONTROLLED-004/hyperframes/assets/establishing.mp4",
      "nb_streams": 1,
      "nb_programs": 0,
      "nb_stream_groups": 0,
      "format_name": "mov,mp4,m4a,3gp,3g2,mj2",
      "format_long_name": "QuickTime / MOV",
      "start_time": "0.000000",
      "duration": "15.041667",
      "size": "15840650",
      "bit_rate": "8424943",
      "probe_score": 100,
      "tags": {
        "minor_version": "512",
        "major_brand": "isom",
        "compatible_brands": "isomiso2avc1mp41",
        "encoder": "Lavf60.16.100"
      }
    }
  },
  "sample_frames": [
    252,
    261,
    264,
    276,
    288,
    300,
    312,
    324,
    336,
    342,
    348,
    354
  ],
  "source_times": [
    10.5,
    10.9,
    11,
    11.5,
    12,
    12.5,
    13,
    13.5,
    14,
    14.25,
    14.5,
    14.75
  ],
  "contact_sheet": "blueprint-cinema/episodes/EP007-exit-readiness-prep/agents/deliverables/premium-004-technical-qa/contact-sheets/rough-cut-r6-extension.jpg"
}
```
