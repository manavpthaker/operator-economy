# R79 whole-episode review conform

R79 assembles the owner-locked EP007 picture sources into one uninterrupted 27,241-frame review at 24 fps. It preserves the R58 accepted prefix audio and the exact locked-master tail sample map. The build adds no creative transition, retiming, grade, music, sound effect, caption or redesign.

The strongest accepted carrier is used wherever possible:

- S15 and S16 are the exact owner-locked R78 complete-scene renders.
- S17 is frames `[192,1803)` of the exact owner-reviewed R76 context, preserving the complete P1 → presenter → P2 continuity in one encode.
- Other sources and frame intervals come from the audited R77 assembly map.

Build and verify:

```bash
python3 _tools/build_r79.py
python3 _tools/verify_r79.py
```

The resulting `qa/ep007-r79-full-review.mp4` is now owner locked as the exact whole-episode picture/audio conform reference. Acceptance is pinned in `direction/r79-owner-locked/OWNER-ACCEPTANCE.json` and explicitly includes the three disclosed inherited R39/R47 exceptions as they appear in the exact R79 bytes. Their earlier independent history is preserved. R79 is not a canonical Resolve finishing master, release or publication approval. No DaVinci Resolve installation or EP007 Resolve/interchange package is currently present in this workspace.

Current technical result: pass. Video SHA-256 `adff0911728de87f5388fbbdaee4d288a077e3b18530c6528d25465eb88e6671`; PCM SHA-256 `3d226b434552def6334b0a583df9ae40b02981df187e725b288286630ed1812c`. The current report is `VERIFICATION-V2.json`. It records 27,241 decoded frames, the exact 54,482,000-sample PCM reference and 1,481-sample zero tail, complete decode, BT.709 tags, −16.72 LUFS, −1.31 dBTP, 0.99999081 decoded-audio correlation at zero lag, −0.00369 dB level delta and 47.32 dB SNR. Every low-variance flag is source-matched inherited picture.
