# R3: reduce movement while retaining articulation

Result: completed and archived as `../media/repair-r3/test-c-avatar-iv-compact-mouth-1080p.mp4`, provider ID `6f2b6c9b39d2482b84c58c162115b279`. File and audio integrity checks pass. The six sampled frames show no clear reduction in mouth opening or facial movement against B. This attempt does not establish a performance improvement; see `status.json` for checks and limits. The delayed R2 Avatar V test A shows smaller openings in the same sampled times and remains a separate candidate for moving-picture owner review.

Owner feedback on R2 test B (Avatar IV): too expressive, mouth opens too widely; emphasis on “straight” and “never” and the flow of words with the mouth match very well. Retain B as the articulation reference. Its overall performance remains rejected.

R3 changes only the motion prompt. Keep Avatar IV, the generated study photo, exact 5.600-second uploaded WAV, landscape 1080p, More Expressive off, and Voice Mirroring off. No new audio or source image is generated.

Prompt: **Speak with compact, natural mouth shapes and minimal jaw opening. Preserve clear consonants and the spoken emphasis on straight and never through subtle lip movement. Keep eyebrows relaxed, the head and shoulders nearly still, and eye contact steady.**

The desired result is less mouth/jaw/eyebrow/head movement without weakening articulation or visual emphasis. This is a prompting hypothesis, not a documented selective jaw-amplitude control. Audio remains the source of audible emphasis. Natural-language prompting cannot guarantee preservation of the previous generated visual performance.

## Inputs

- WAV: `../media/repair-r2/scope-two-sentences.wav`, SHA-256 `c565f1dfe8c218f156e9d0b76d0515a264be26cc1d0cea7d1ea8977a3c565566`.
- Source interval, word IDs, and master hash: `../repair-r2/input-manifest.json`.
- Study image: `../media/study-look-candidate-03.webp`, SHA-256 `59309d2925b85cfba8a6a411dce1ecea67a03607f8a05933f4a2f6cb6af27754`.
- B reference: `../media/repair-r2/test-b-avatar-iv-1080p.mp4`, SHA-256 `7ced24b3cdff8adfbb686492497c9d065f0ac6edee03a6a5e0e855e6d539e473`; provider ID `0013546d77334dd28cd6811ca06945b8`.

## Review

Compare mouth-opening amplitude and facial motion against B with sound. Preserve the emphasis and word flow the owner liked, especially “straight” and “never.” Check the inter-sentence pause (local 2.850–3.870s), glasses/identity/set stability, and final word. File/audio checks alone do not pass performance. No episode approval or production gate is advanced.

## Control evidence

- [Avatar IV controls](https://developers.heygen.com/avatar-iv): global expressiveness and motion prompting; no separately documented jaw-size control found.
- [Avatar troubleshooting](https://help.heygen.com/en/articles/15544929-avatar-voice-faq-troubleshooting-best-practices-and-credits): subtle source expression and More Expressive off are recommended for wide mouth movement. B already used the off setting.
