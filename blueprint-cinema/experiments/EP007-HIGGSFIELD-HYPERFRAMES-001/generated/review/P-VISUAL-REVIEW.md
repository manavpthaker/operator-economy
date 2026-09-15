# Presenter P visual comparison

Scope: twelve sampled frames per clip at 0.0, 0.5, ..., 5.5 seconds. Higgsfield P versus existing HeyGen controls M and Q. This review does not establish normal-speed naturalness, phoneme sync, or exact source-audio fidelity.

- P retains the recognizable reference face, clear glasses, navy shirt, study, window and desk. No obvious face replacement or scene drift in the sampled frames.
- P is quieter than Q: forearms stay on the desk and the raised hand remains near its initial position; Q makes a larger hand opening/lift around 1.0 seconds and later drops the hand toward the desk. P's still-held gesture may itself read static in playback; these samples cannot settle that.
- Head motion is reduced, not eliminated. P is higher around 1.0 seconds and lower around 3.0 seconds, then recovers. Brows lift around 4.5 seconds. It avoids the larger sampled Q rise/drop around 0.5-1.0 seconds.
- Expression remains restrained, with mouth movement and blinks at sampled 2.0 and 3.5 seconds. No broad smile or theatrical gesture is apparent in the samples.
- M is more tightly framed and does not provide a hand comparison. P is 720p/24 fps; M and Q are 1080p/25 fps. Apparent facial detail is therefore not an equal-resolution comparison.

## Limited motion measurement

Native Apple Vision landmarks on the same twelve timestamps, frames normalized to 1280x720. Eye-center displacement is divided by each clip's median eye separation to compensate for framing. This measures sampled 2D translation, not pitch, true nod count, or performance quality. Raw clip timestamps are not guaranteed speech aligned.

| Clip | Maximum sampled eye-center displacement (eye separations) | Sampled eye-line roll range |
| --- | ---: | ---: |
| P | 0.201 | 3.36 degrees |
| M | 0.280 | 2.78 degrees |
| Q | 0.345 | 5.35 degrees |

P has less sampled face translation than M and Q and less sampled roll than Q. Its roll is slightly greater than M. Sparse sampling can miss extremes; landmark noise and facial perspective contribute. This supports a steadier-head observation, not an automated acceptance.

Evidence: `P-contact.png`, `M-contact.png`, `Q-contact.png`; `presenter-motion-comparison.json`; `presenter-landmarks.json`; `FullFrameLandmarks.swift` and extracted frames. Audio review is separate.
