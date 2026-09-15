# R14: fresh image input with explicit low expressiveness

**Current result: owner-accepted baseline.** The owner played M and accepted the subtle head movement and mouth movement, then requested a small hand/arm gesture test. See `../repair-r15/`. The source recipe and original test rationale below are preserved.

K is rejected by the owner for word/mouth mismatch and excessive head movement. Its saved Avatar III look exposes a 30-second Avatar IV motion plate in AI Studio. L's separate Precision Lipsync test on an unchanged stationary portrait returned no meaningful mouth animation, so L is also rejected.

M is one fresh direct-image generation, using the documented `type: image` route (Avatar IV), without an avatar ID or saved motion source. It uses the exact accepted candidate 03 pixels, re-encoded losslessly from WebP to PNG for the supported upload format, and the same original 5.600-second WAV. Expressiveness is explicitly low. The motion prompt concentrates on a level, stationary head, natural blinking, relaxed jaw/brows, and precise lip articulation. It does not request acting emphasis on individual words. This is not an exact transfer of F's performance.

The earlier B/C tests already used Avatar IV with More Expressive off and motion prompts. M is not a discovery of a new engine. Its controlled distinction is direct raw-image input through the documented API, with explicit `expressiveness: low`, bypassing the saved-look motion association. Improvement remains uncertain; no batch or full-passage generation is authorized by this test's result alone.

Input photo: `../media/study-look-candidate-03.webp`, SHA256 `59309d2925b85cfba8a6a411dce1ecea67a03607f8a05933f4a2f6cb6af27754`.

Upload PNG: `../media/repair-r13/accepted-study-lossless.png`, SHA256 `3e63720497e29ed088f7c3747b66b18281514e1ad162efa05ebecc078df67024`. Decoded pixels, mode and dimensions were checked equal before upload. Image asset `54cb76c8dae2459298ffde10b7b6ad0d`.

Audio: `../media/repair-r2/scope-two-sentences.wav`, SHA256 `c565f1dfe8c218f156e9d0b76d0515a264be26cc1d0cea7d1ea8977a3c565566`. Audio asset `f5e2f0c3d9b341e893e15201e326aab1`.

The exact request is `video-request.json`. HeyGen CLI v0.8.1, official OAuth, existing subscription credits. One generation in this test; no purchases or plan changes. Owner authorization continues the short avatar repair work. No locked narration, canonical episode timeline, other cinematic work, or approval gate changes.
