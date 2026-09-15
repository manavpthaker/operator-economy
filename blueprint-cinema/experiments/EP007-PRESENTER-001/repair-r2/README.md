# Presenter performance repair R2

Owner feedback, 2026-09-07: the mouth movement is off and the reactions do not consistently match the narration. The owner has upgraded HeyGen. V001 is rejected for presenter use, regardless of its earlier technical checks.

## Bounded comparison

Use the same generated study look and the same original audio for both tests. Compare Avatar V and Avatar IV with More Expressive off and a short restrained-performance prompt. The experiment changes the rendering model, not the locked voice, appearance, wording, or timing.

Excerpt: W001663–W001678, “I will be straight with you about my own position. I have never sold a business.” Spoken interval 591.300–596.400 seconds; source WAV 591.050–596.650 seconds, including 250 ms handles. Duration 5.600 seconds. This complete two-sentence thought includes the pause between disclosure and admission, and several visible lip-closure opportunities. It is short enough to avoid the documented Avatar IV custom-motion loop/hold limit after 10 seconds.

Motion prompt: **Calm, candid delivery with restrained facial movement and relaxed eyebrows. Steady eye contact with the camera. Hands remain still below frame.**

Both settings: landscape, 1080p if verified available, uploaded original WAV, Voice Mirroring off, More Expressive off. The first model is V; the second IV. Do not infer equal model behavior from identical settings.

## Review criteria

- Lips correspond to the heard words, including closed-lip consonants and silence between sentences.
- No smiling, enthusiasm, emphatic eyebrow response, or repeated nod that contradicts the admission.
- Identity, glasses, eye line, shoulders, and set remain stable.
- Preserve exact audio; check encoding delay separately from perceptual lip-sync.
- Review moving picture with sound. Numerical waveform correlation and sampled stills do not prove a performance pass.

If restrained generation still fails, inspect the actual motion-reference video or consider precision lip repair after facial performance is acceptable. Do not buy repeated full-length renders or call the issue solved by higher resolution. A prompt does not offer word-accurate acting control. The episode edit may need shorter direct-address appearances around complete thoughts; this packet does not change the four proposed episode placements.

## Vendor references and limits

- [Avatar V best practices](https://help.heygen.com/en/articles/14602997-how-to-get-the-best-results-with-avatar-v-in-heygen): match the motion reference's energy and camera angle; use a calm reference for subtle delivery.
- [Troubleshooting FAQ](https://help.heygen.com/en/articles/15544929-avatar-voice-faq-troubleshooting-best-practices-and-credits): lower expressiveness and compare engines for unnatural mouth/expression behavior. Some look/model eligibility statements conflict with the live Single Scene UI; the run records the actual UI engine.
- [Custom Motion](https://help.heygen.com/en/articles/12805098-fine-tune-avatar-gestures-and-movements-with-custom-motion-prompts-avatar-iv-v): gestures are timed automatically; the 10-second motion note occurs under Avatar IV.
- [Precision Lipsync](https://developers.heygen.com/lipsync-precision): a separate potential mouth-repair path, not a repair for inappropriate brows, smiles, or gestures. Preserve timing and original audio if used.

No upstream narration or cinematic work changed. No production or approval gate advanced.

## R2 submissions and playback cues

On retry, both jobs were submitted successfully in the upgraded account. Test A uses Avatar V (`d21d0f5db5d145a199da0390b07c6518`); test B uses Avatar IV (`0013546d77334dd28cd6811ca06945b8`). The same source photo, uploaded WAV, prompt, landscape 1080p, More Expressive off, and Voice Mirroring off were verified before submission. See `status.json` for completion and review state.

Local clip cues from the pinned word transcript:

| Time | Cue |
|---|---|
| 0.490–0.710s | “be”: brief closure and release around initial b |
| 2.050–2.850s | “my own position”: m near 2.05s, p near 2.41s |
| 2.850–3.870s | Sentence pause: watch for apparent speech or an unrelated reaction |
| 4.950–5.350s | “business”: initial b and settling at the end |

These are word-alignment cues, not frame-exact phoneme labels or measured rendered lip sync. Lip closure may precede the transcript word boundary.
