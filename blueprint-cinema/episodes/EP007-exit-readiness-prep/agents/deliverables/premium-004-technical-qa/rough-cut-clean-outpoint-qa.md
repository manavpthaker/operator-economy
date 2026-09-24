# EP007 clean-outpoint render QA

**Pass for the final essential technical checks.** Output SHA-256: `d1e0d14bf0b1acc750994dc95e767743301e621f6971987e0a40f9c644f0668a`; size **34,497,797 bytes**.

- Full video/audio decode: no errors.
- Picture: **1280 × 720, 30 fps, exactly 1,785 decoded frames**. Video and audio streams both end at **59.500000 seconds**.
- Audio correlation against the locked narration's unchanged first59.5seconds: **0.99982402**. Final40ms RMS **0.001668**, peak **0.004095**: a quiet ending before the likely next-word onset.
- Actual final frame **1784** is present; presenter/title visible; bottom edge clean. Rounded lips remain visible during this quiet frame and remain a performance-review note, not a claim of perfect visual synchronization.

The earlier59.866667-second render's five cuts and corrected edge were independently checked in `rough-cut-final-qa.json/md`; those receipts remain historical. This closing check follows root's narrowed scope: decode, exact frame count/duration, audio/quiet ending and final-frame inspection. Root performed full normal-speed playback. No source media, locked narration or production state was changed by the reviewer.

Current input hashes and probe results are in `rough-cut-clean-outpoint-qa.json`; final image: `contact-sheets/rough-cut-clean-outpoint-frame1784.png`.
