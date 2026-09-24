# Rescue V1 preview

Status: isolated, renderable review candidate; not a final master, avatar take, publication approval, or Related Video assignment.

## Isolation

- Locked source project: `../short-01-thirty-days-no-owner/`
- Locked source root SHA-256: `857723990ec48d6743dd2ea4e44b9456bfd8ece02851b8494b350a8e2833bdaa`
- This sibling contains only the source HTML/motion files, local fonts/runtime, the accepted identity still, and the authorized local salvage WAV.
- The locked 43.846410-second source was not edited.
- No generation, paid-media, upload, publish, or external-provider action is part of this preview.

## Audio authority

- File: `assets/audio/short01-final-original-c-salvage-v1.wav`
- SHA-256: `b4ab3903255b5b425f2adc88f81372f7072efc58eb842830c6dd600dc188d61c`
- Format: 48 kHz, mono, PCM16
- Duration: 57.666667 seconds / 2,768,000 samples / 1,384 frames at 24 fps
- This is the separately recorded rescue-v1 salvage. The preview does not create another trim authority.

## Timeline

| Scene | Existing order | Start | End | Duration | Visual role |
|---|---|---:|---:|---:|---|
| 01 | Business, then test | 0.000000 | 18.083333 | 18.083333 | opening avatar placeholder |
| 02 | Circle the owner | 18.083333 | 27.750000 | 9.666667 | graphics only |
| 03 | Build the handoff map | 27.750000 | 40.958333 | 13.208333 | graphics only |
| 04 | Hold the boundary | 40.958333 | 47.583333 | 6.625000 | graphics only |
| 05 | Open the commercial test | 47.583333 | 57.666667 | 10.083334 | closing avatar placeholder |

The cut points are 24 fps frame boundaries selected from a local word-timed transcript. Copy and scene order are unchanged. The six scratch tracks are replaced by one continuous Original C salvage track. Captions are aligned to the same local transcript.

## Files intentionally changed from the locked source

- `index.html`: duration, five host windows, one local master-audio element, transcript-aligned caption windows, work-mode cue, and rescue label.
- `index.motion.json`: duration and the retimed second-caption assertion.
- `compositions/01-no-owner.html` and `.motion.json`: duration only.
- `compositions/02-circle-owner.html` and `.motion.json`: duration; middle avatar plate hidden; corresponding avatar-only assertions removed.
- `compositions/03-dependency-map.html` and `.motion.json`: duration only.
- `compositions/04-map-limit.html` and `.motion.json`: duration; middle avatar card hidden; existing map centered; corresponding avatar-only assertions removed.
- `compositions/05-commercial-question.html` and `.motion.json`: duration; the in-picture Related Video target strip was removed. Native YouTube Related Video selection remains a separate release-stage control.
- `package.json` and `meta.json`: sibling-project identity only.
- `BRIEF.md`, `STORYBOARD.md`, and `COPY-DRAFT.md`: rescue duration/media status and the same five scene windows; spoken copy is unchanged.

## Local verification

```bash
npm_config_offline=true HYPERFRAMES_NO_TELEMETRY=1 \
  npx --yes hyperframes@0.8.58 timeline --json

npm_config_offline=true HYPERFRAMES_NO_TELEMETRY=1 \
  npx --yes hyperframes@0.8.58 check --json --strict --samples 12 \
  --at 9.041667,22.916667,34.354167,44.270833,49.677,52.625 \
  --frame-check \
  --caption-zone 'x0=0;y0=.72;x1=1;y1=.91;severity=error;seek=.1,.25,.5,.75,.9'

npm_config_offline=true HYPERFRAMES_NO_TELEMETRY=1 \
  npx --yes hyperframes@0.8.58 snapshot \
  --at 9.041667,22.916667,34.354167,44.270833,52.625

# Final Studio handoff; keep it running until review ends.
npm_config_offline=true HYPERFRAMES_NO_TELEMETRY=1 \
  npx --yes hyperframes@0.8.58 preview --background
```

Results: timeline is contiguous at 57.666667 seconds. The final full-transition strict check in `.hyperframes-check-rescue-v1-final.json` passes with zero lint, runtime, layout, or motion findings: 500 layout samples, including 491 transition samples; 300 motion samples; and 69/69 contrast checks. The review snapshots were inspected. No render was requested or produced.
