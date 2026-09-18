# Full-source repair inputs

These six inputs repair **confirmed terminal truncations** reported by root. They are separate from the five long-source slices. Use `DELIVERY.json` once present; `MANIFEST.json` records preparation and `UPLOADS.json` binds Fal storage verification.

| Clip | Original / selected frames | Disposable guards | Provider input frames |
|---|---:|---:|---:|
| seg009 | 220 | 8 | 228 |
| seg021 | 242 | 8 | 250 |
| seg035 | 258 | 8 | 266 |
| seg072 | 191 | 8 | 199 |
| seg073 | 227 | 8 | 235 |
| seg075 | 186 | 8 | 194 |

Each original picture frame is unchanged after lossless H.264 CRF 0 encoding. Each guard repeats the final original frame. Original source audio is retained as decoded stereo float PCM, followed by 16,000 zero samples for the eight guards. seg075's original AAC decode ends 288 samples before its picture; that documented six-millisecond shortfall receives silence before the separate guard interval. No existing original sample changes, and the locked episode master remains authoritative.

Retain the guards through wardrobe and background edits. The final selection is always `[0, original_frame_count)`; discard every guard. No original files, active plans, assemblies or owner locks were changed. Upload scripts call Fal storage only; root owns paid generation and budgets.
