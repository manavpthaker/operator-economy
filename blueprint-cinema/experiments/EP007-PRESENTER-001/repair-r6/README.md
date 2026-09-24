# R6: original footage with Avatar III

The owner's request to keep trying continues in this bounded five-second test after E retained wide mouth opening in the quiet pause. F uses the original video look `b495d299cea544608fc2fc249d055b87` from group `cc6abe9744e74df7a103b7a37262d2f7` with **Avatar III**. The exact selected image path, Avatar III selector, uploaded `scope_two_sentences.wav`, Voice Mirroring off, landscape icon, and1080p setting were read back before a single Generate action.

The live selector describes III as “Applies lip sync over your footage.” The official [Avatar III documentation](https://developers.heygen.com/avatar-iii) and [avatar FAQ](https://help.heygen.com/en/articles/15544929-avatar-voice-faq-troubleshooting-best-practices-and-credits) describe a footage-based lip-sync route. No custom motion/expressiveness controls are exposed here. Reused recorded movement is not a guarantee that eyebrows or gestures will match the meaning of new narration. No separate silence-mouth control was found.

Input: `../media/repair-r2/scope-two-sentences.wav`, SHA-256 `c565f1dfe8c218f156e9d0b76d0515a264be26cc1d0cea7d1ea8977a3c565566`. Exact narration lock, source window and word IDs remain in `../repair-r2/input-manifest.json`. No new narration, audio retiming, image generation, or background replacement is part of F.

Compare with E and D for mouth behavior during the quiet 3.2–3.6s interval, then review speech articulation and reactions during full playback. Audio matching alone does not establish visual synchronization. The original raw training recording is still unverified.

The final presenter direction remains a complete landscape study scene, as explained in `../repair-r5/README.md`; the portrait against curtains is diagnostic. No episode gate, film work, or publishing state changes.

## Result

[Test F](https://app.heygen.com/videos/3c6cac5f02c74651a7169b3c9ae9a6a0) is complete and archived at `../media/repair-r6/test-f-original-footage-avatar-iii-1080p.mp4`, SHA-256 `d5c590fb00f9d5fda21af2d175048b94de64fb96413aa87ef215148d89727bcb`. Full decode passes. It is 1920×1080, progressive H.264,25fps/139frames,5.560s picture/5.591s audio. Fresh audio measurement matches E: +23.021ms delay,0.999428 aligned correlation, matching sentence delays and full last-word coverage. The 3.2–3.6s interval remains very quiet at RMS−64.96dBFS.

Exact comparison frames show F has substantially smaller mouth openings than D/E at3.2/3.4/3.6s. This is a specific sampled improvement. The mouth is still slightly open and eyebrows remain raised; full owner playback must judge articulation, emphasis and whether the reactions fit the narration. Do not call naturalness or lipsync solved based on these frames. `../media/repair-r6/d-e-f-pause-comparison.jpg` and `technical-review.json` retain the evidence.

## Owner feedback

The owner subsequently reviewed F and said, “yes this is much better.” Avatar III with the original look is selected as the working route. This is positive playback feedback for F, not approval of final composition or untested longer passages. The full scope duration test is recorded in `../repair-r7/`.
