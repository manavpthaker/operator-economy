# Performance comparison

`compare_performance.py` is an offline, descriptive QA helper. It reads both inputs
without editing them and refuses to overwrite a nonempty output directory. It does
not call providers, change audio, conform video, or approve a candidate.

Run from the repository root after the candidate has been downloaded:

```sh
/tmp/claude-501/-Users-brownmanbrain-GitHub-operator-economy/82de42ec-ae77-42eb-8a88-f56e54114dda/scratchpad/syncenv/bin/python \
  blueprint-cinema/experiments/EP009-FULL-BUILD-001/presenter-look-transfer/_tools/compare_performance.py \
  --source blueprint-cinema/experiments/EP009-FULL-BUILD-001/presenter/P13/final/seg074.mp4 \
  --source-sha256 ecbb6bffad1094fde360fb3d64bf36aff224df5463f410fd3537467b4146adb9 \
  --candidate blueprint-cinema/experiments/EP009-FULL-BUILD-001/presenter-look-transfer/pilot-seg074/kling-r1/native.mp4 \
  --out blueprint-cinema/experiments/EP009-FULL-BUILD-001/presenter-look-transfer/pilot-seg074/kling-r1/performance-qa-r1
```

Add `--candidate-sha256 HASH` to enforce a known downloaded candidate hash. The
actual hash is always recorded. `--self-test` checks timestamp pairing at 24, 25,
and 30 fps, shorter coverage, a known delayed signal, and static-signal handling.

The helper measures all native frames with MediaPipe Holistic. It keeps ffprobe
presentation timestamps and pairs each source-frame timestamp with the nearest
candidate frame. Each file's first presented frame is time zero; original PTS
origins, duration differences, fps, missing coverage, and sampling errors remain
visible. It never rescales time or applies a measured lag.

Outputs:

- `PERFORMANCE-COMPARISON.json`: hashes, format/duration differences, detector
  coverage, face/head/hand geometry, expression proxies, and descriptive temporal
  correlation results. A positive lag means candidate motion occurs later.
- `FRAME-PAIRS.json` and `PAIRED-TRAJECTORIES.csv`: the exact frame/timestamp pairs
  and source/candidate feature series.
- `source-trajectories.npz` and `candidate-trajectories.npz`: every measured native
  frame, including face, body, both hands, head-angle proxies, and timestamps.
- `contact-*.jpg` and `paired-frames/`: labeled source/candidate/difference rows
  from uniform checkpoints plus maximum observed face/wrist difference frames.
- `SOURCE-PROBE.json` and `CANDIDATE-PROBE.json`: original stream metadata and
  decoded frame timestamps.

Inspect the actual paired pictures and normal-speed video. A changed shirt or room
will dominate raw pixel difference. Landmark estimates depend on lighting,
occlusion, appearance, and detector stability. Missing detection does not establish
missing movement. Head angles are uncalibrated relative proxies; expression ratios
do not certify emotion, identity, phonemes, or lip sync. Similar gesture curves can
produce misleading correlation peaks. There are no acceptance thresholds.

`HELPER-VERIFICATION.json` records preparation checks. Its source-self run validates
the mechanics and visuals only; identical file hashes intentionally reuse extracted
trajectories, so that run does not test independent detector repeatability or any
edited candidate.
