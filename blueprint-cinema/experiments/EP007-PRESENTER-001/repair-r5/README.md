# R5: original video look with Avatar IV

The owner requested that avatar refinement continue on 2026-09-07. The next bounded test uses the original video look with Avatar IV. It compares principally against R4 D (original look with Avatar V), while preserving the exact two-sentence narration and requested landscape1080p output.

## Inputs and controls

- Avatar group: `cc6abe9744e74df7a103b7a37262d2f7` (`brown Man`).
- Original video look: `b495d299cea544608fc2fc249d055b87`, verified again from the selected Quick create image asset path before submission.
- Model selector: **Avatar IV**. The page's generic Presenter tab continues to say Avatar V; the actual engine selector is the submitted model evidence and will be checked against the returned job label.
- Audio: `../media/repair-r2/scope-two-sentences.wav`, SHA-256 `c565f1dfe8c218f156e9d0b76d0515a264be26cc1d0cea7d1ea8977a3c565566`, verified locally before submission. Master lock, exact PCM source window, text, and word IDs remain in `../repair-r2/input-manifest.json`.
- Voice Mirroring: off, verified in picker and final form.
- Output: Landscape, 1080p. Actual output framing awaits inspection.
- Entry point: original look → Use in a video → Quick create / Single Scene.
- Motion prompt and More Expressive controls disappear for this original video look when Avatar IV is selected. Their values are **not observable**, not assumed off. This is an additional control difference from D and from B/C photo-look tests.

The official [avatar troubleshooting guide](https://help.heygen.com/en/articles/15544929-avatar-voice-faq-troubleshooting-best-practices-and-credits) recommends trying IV after V with reduced expressiveness for excessive mouth opening on a video look. The [Avatar IV guide](https://help.heygen.com/en/articles/11269603-heygen-avatar-iv-complete-guide) documents video-look support. Live UI exposed both Avatar IV and Avatar III for this look; III was not submitted. Precision Lipsync with supplied video/audio is documented for the API, but a same-WAV web repair path was not verified and Translation was not used as a substitute.

## Review question

Does E improve mouth articulation and quiet-pause behavior over D? Inspect 3.2–3.6s specifically, alongside full playback, because D opened broadly there while audio was very quiet. Preserve the emphasis on “straight” and “never” that the owner liked in B. A technical audio match is not a performance pass, and this comparison does not identify the quality of the unverified raw recording.

## Presenter format

The existing selected direction remains a complete 16:9 chest-up presenter shot in a restrained study, with scene cuts to animation/illustration, cinematic footage, and evidence. The current original portrait is a diagnostic control, not the final background/framing. A transparent cutout over a graphic would be an occasional optional treatment, not the default presenter format or an approved new composition. The avatar's source recording and the final compositing treatment are separate decisions; background removal alone does not repair mouth animation.

The full study shot can be produced as a complete scene or by compositing a retained presenter take over a background. Preserve any accepted moving performance before cosmetic background work. HeyGen's [BG Remover guide](https://help.heygen.com/en/articles/11371315-how-to-remove-the-background-of-any-avatar) documents removal for avatar objects, including eligible Video Looks, but does not promise that a new Studio render reuses the exact face frames of an earlier accepted MP4. Downstream matting of a retained video is a separate editing approach. It cannot recover shoulders or torso outside the original tight crop. No background removal or new study generation was submitted in R5.

No locked narration, separate film work, episode placement, approval gate, or publishing state is changed. Results and generation count are recorded in `status.json`.

## Result

[Test E](https://app.heygen.com/videos/946b129a3a5c4aa9994afa1aba7d650d) is complete and archived at `../media/repair-r5/test-e-original-look-avatar-iv-1080p.mp4` (SHA-256 `30235140e41dcce65fb9dc99d90014a495e88f13f438e91053256708e56bb565`). Full decode passes, 1920×1080, 25fps/139frames, 5.560s picture/5.591s audio. Audio correlation and +23.021ms delay match A–D, with no measured drift or final-word cutoff.

Exact D/E comparison frames at2.8/3.2/3.4/3.6s show that E still opens widely during the very quiet 3.2–3.6s interval. It has not established a repair. Full playback is pending. A subsequent bounded F trial uses the UI's Avatar III path, described as lip sync applied over original footage, to complete the comparison of the three available original-look engines.
