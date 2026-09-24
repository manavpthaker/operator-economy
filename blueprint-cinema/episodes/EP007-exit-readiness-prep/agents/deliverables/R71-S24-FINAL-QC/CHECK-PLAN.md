# R71 S24 independent QC preflight

Reviewed finish.py SHA256 `51cfa4008f7f2a200c1e10ca10dbbd1c1ee4efd48aed5285af33eff6dbcc40e1` without executing it.

The composition arithmetic is correct: accepted S23 frames [38,230) retain 192 frames / 8 seconds; S24 [0,552) appends 552 frames / 23 seconds; total 744 frames / 31 seconds. S23 source master frame 25654 + 38 = 25692, or 1070.5 seconds. S24 starts at master frame 25884, 1078.5 seconds. End frame 26436 is 1101.5 seconds. Continuous source audio samples [51384000,52872000) total 1488000 samples at 48 kHz, exactly 31 seconds. S24 staged audio uses [51768000,52872000), 1104000 samples, 23 seconds.

The last S24/context video frame starts at master 1101.458333 and displays until 1101.5. The expected scene change in context is frame 192 / 8 seconds; S24 conditions switch at scene frame 358 / context frame 550, local 14.916667 / context 22.916667. Six-frame entries last 250 ms.

Await root source-ready before inspecting final encoded outputs. Planned compact checks: pinned final hashes, decoded frame counts and shape, staged PCM equality, seam-local audio correlation, encoded first/last and cue-frame inspection. No continuous listening or owner acceptance will be claimed.
