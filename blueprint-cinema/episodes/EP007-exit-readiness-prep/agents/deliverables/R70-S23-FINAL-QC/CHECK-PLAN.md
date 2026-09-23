# R70 S23 independent final QC

Scope: read-only review of final S23 and its eight-second locked S22 lead-in. Write only this deliverable directory. Final media inspection waits for root source-ready; no render or provider request is authorized here.

Preflight finish.py SHA-256: `13802f8b658ae086d5f9c48483c2f47cb4967b2eb300880d6eed1d0e1df4d837`.

Assembly arithmetic passes: S22 source frames [332,524) plus S23 [0,230) yield 422 frames, 17.583333 seconds. Master PCM [50924000,51768000) is 844000 samples at 48 kHz, exactly the same continuous duration. S23 alone uses [51308000,51768000), 460000 samples, corresponding to master [1068.916667,1078.5). Final S23 frame begins at 1078.458333 and displays until 1078.5.

Pending source-ready: recompute final source hashes; inspect cue logic and label claims; decode and count every frame; check for near-uniform frames; compare scene/context audio to original master and inspect seam-local audio metrics; verify staged WAV format and PCM equality; inspect encoded contact/seam frames. Correlation, PCM, and images cannot establish a human listening verdict. Graphic stillness is allowed. No owner creative acceptance is claimed.
