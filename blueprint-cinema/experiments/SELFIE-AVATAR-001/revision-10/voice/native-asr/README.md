# R10 native speech-clock audit

One independent `faster-whisper small.en` pass ran for each native clip, with the model loaded once. Native bytes matched the pins in INPUT.json. No paid call, voice generation, media repair or lip-sync pass ran here.

All normalized words matched the authored sections: 60/60, 69/69 and 64/64. Word onset lags vary within each clip rather than following one uniform offset. Positive lag means native speech occurs later than the exact retained source section.

| Section | Early-third median | Middle-third median | Late-third median | Final word end lag |
|---|---:|---:|---:|---:|
| 1 | 0.00 s | -0.31 s | +0.17 s | +0.16 s |
| 2 | -0.30 s | -0.04 s | +0.16 s | +0.08 s |
| 3 | -0.12 s | +0.40 s | +0.56 s | +0.40 s |

These coherent timing changes support treating the native audio as a different speech clock. Replacing its soundtrack at one fixed offset cannot align every phrase. ASR timing remains approximate: this is neither a viseme measurement nor a listening or perceptual acceptance result.

SUMMARY.json is complete and sufficient for the timing decision. The connector truncated the compressed full report above its stdout limit, so the full raw ASR word arrays are unavailable. CONNECTOR-RESPONSE.json retains the exact truncated response and intact summary; INPUT.json retains the exact source-word map, authored sections, URLs and native hashes. The parent explicitly directed no rerun after this issue was reported. No ASR pass was repeated.
