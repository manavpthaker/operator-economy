# R21: remove the added head zoom

Owner rejected S: “no that looks crazy like the head is zooming in and out.” The rejection overrides S's numeric stabilization and sampled-frame checks. S introduced a 3.94% scale swing, including approximately 2.39% growth over 160ms near a blink, alongside head movement relative to the retained body. Less tracked movement did not establish more natural performance.

T starts again from Q, SHA256 `8675571508e53e3f57ecefe42994b71f9b710e7e3603f1ad1c9a454c66574950`. Every frame uses scale exactly 1 and rotation exactly 0; the renderer refuses any nonidentity linear transform. The only correction is a smoothed translation, limited in this render to 2.337 pixels horizontally and 4.174 pixels vertically at 1920×1080. This deliberately retains substantially more original head movement than S. It cannot remove Q's original 3D pitch, yaw or apparent size changes.

The face, blinks, lip shapes and hands use the same Q frames. Head correction fades through the neck interior, preserving shoulder outlines and hand coordinates. Existing person mattes isolate the presenter; newly exposed background uses observed Q pixels and horizontal interpolation of unobserved fringe. No expression, voice, provider generation, retiming or new look is introduced.

Current candidate: `../media/repair-r21/test-t-no-scale-gentle-head-1080p.mp4`, SHA256 `d8ad106951e44ee163091f349b8759b4a615546866b19bbba5876c2dacde5a73`, 4,115,805 bytes. See `stabilization-config.json` for all 140 transforms, `render-report.json` for source bindings, and the technical and visual reviews for the exact scope of verification.

Mode remains `presenter_address`, landscape study, same locked two-sentence audio. M remains the historically owner-accepted baseline. S is rejected; T is an owner-playback candidate, not production acceptance. No canonical episode gates, locked narration, final timeline or separate cinematic work changed.

Verification: full decode passed; picture remains 1920x1080, 25fps, 140 frames, 5.600 seconds. All frame timestamps and the AAC bitstream are identical to Q. A narrow visual check of frames 0/15/25/100/111 and the 0.60-1.40s Q/S3/T strip found source-like proportions, a connected neck, single shoulder outlines and straight shelves. Source nod/forward movement remains; T is not a micro-expression-only performance. Full-speed naturalness remains owner review.
