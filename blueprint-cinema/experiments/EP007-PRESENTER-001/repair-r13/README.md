# R13: separate lip-sync from the motion source

The owner rejects K's second-part word/mouth match and excessive head movement. The accepted appearance remains candidate 03 unchanged: navy shirt, clear glasses, landscape study. The narration remains the exact 5.600-second two-sentence WAV used in A–F and K.

## New evidence

On September 8, AI Studio was opened for group `cc6abe9744e74df7a103b7a37262d2f7`, exact photo look `dd0bb50578ce4c17bee712e72ed2d84f`. Avatar III > Advanced Settings > Customize Motion exposes one selected **Saved Footage, 30 s** item. Its menu explicitly states **Motion Engine: Avatar IV**. No replacement, remove-motion, or legacy lipsync-only control was visible. This live configuration makes inherited generated head motion a plausible explanation; the internal source used by the completed Quick Create K job remains unexposed.

The independent K/F diagnostic sampled 12 frames from 3.84–5.52 seconds. After normalization by eye separation, K's eye-center displacement range is about 2.5 times F's; sampled eye-line roll spans 4.14 degrees versus 1.96 degrees. These are 2D sampled proxies, not continuous or 3D measurements. The mouth samples do not establish a simple uniform visual offset. Numerical audio alignment cannot clear the owner's lip-sync complaint.

Diagnostic evidence: `../../../episodes/EP007-exit-readiness-prep/agents/deliverables/presenter-restored-look-r12/diagnostic-k/`.

## Next bounded test

Create a stationary 5.600-second source plate from the exact accepted image, with the exact narration, through HyperFrames. Apply the separate documented [HeyGen Precision Lipsync](https://developers.heygen.com/lipsync-precision) route. This deliberately removes the inherited motion source to test articulation without nodding. It is a diagnostic hypothesis; a stationary upper face may be too static for a final presenter.

HeyGen CLI v0.8.1 was installed from the official checksum-verified release and connected through its official browser OAuth flow to the same signed-in account. The CLI readback identifies subscription billing, Creator plan. No API key, credit purchase, plan change, or credential rotation was used. The existing authorization to continue short avatar repairs covers this bounded source plate and one lip-sync attempt.

Generation settings must preserve duration, input audio, format, and frame rate where the provider permits. Do not claim success until a returned result is checked. No episode timeline, locked narration, other cinematic task, or production approval changes.

## Result: rejected

Test L completed as `ed49992dc32e496590803ef7dc0ac854`, but the returned mouth remains closed throughout the sampled speech frames. Across all140 frames, mouth/chin mean absolute change from frame0 is at most0.0334/255, consistent with compression only. The result has no usable articulation. This does not establish why the provider omitted the lip animation. File/audio checks pass:1080p,25fps,140frames,5.600s,0ms independently measured audio lag in both sentences. Output: `../media/repair-r13/test-l-still-study-precision-lipsync-1080p.mp4`. The next single direct-image test is recorded separately in `../repair-r14/`.
