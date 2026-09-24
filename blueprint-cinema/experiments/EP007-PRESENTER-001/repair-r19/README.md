# R19: locally damp Q's head dip on straight

Current output: `../media/repair-r19/test-r-q-subtle-straight-head-isolated-1080p.mp4`, SHA256 `e10b3f762317d56a4dd374ab0ad24f68d2779bc7137425671b39d7d499dd4c37`, 4,059,132 bytes. 1920x1080, 25 fps, 140 frames, 5.600 seconds. Every frame timestamp matches Q and the copied AAC bitstream hashes identically. Independent tracking of this final output measures a 53 percent smaller brief downward transient: Q 26.73 px, isolated R 12.58 px. Five sampled frame pairs show no blocking shelf, hair/ear or neck defect; shelf alignment remains unchanged in eight measured columns per frame. Normal-speed naturalness and final preference remain for owner playback. See `isolated-technical-review.json`, `isolated-head-motion-review.json` and `isolated-visual-review.json`.

The first unisolated warp reduced the measured transient by 51 percent but visibly bent the shelf beside the ears; it is rejected. The current pass keeps the same head translation while isolating the presenter with local native Vision person segmentation. Background restoration uses observed unoccluded pixels from Q, without generative fill. The first pass and its failure evidence remain preserved.

Correction: 17 frames, 0.68–1.32 seconds, smoothly returning to Q. The maximum upward correction is 12.91 pixels. The baseline follows Q's gradual pose change between 0.64 and 1.36 seconds; it does not force the head back to its earlier height. This damps the transient rather than introducing a second nod. `damping-config.json`, `damp_head.py` and `isolate_head.py` preserve both methods and exact parameters.

The foreground masks and source-frame hashes are bound in `isolated-render-report.json` and the segmentation manifest under the independent `presenter-head-damping-r19` deliverable. At most 1,400 soft-boundary/disocclusion pixels per processed frame lacked a reference mask alpha below 0.02; those edges require visual review and are not claimed to be a perfect clean plate.

Owner playback: “Q is a bit better but ‘straight’ is still too pronounced head movement. it needs to be more subtle.” The owner previously clarified that this is mainly mouth/head movement, not the voice.

Q is the source for this repair: `../media/repair-r18/test-q-m-direction-visible-hands-1080p.mp4`, SHA256 `8675571508e53e3f57ecefe42994b71f9b710e7e3603f1ad1c9a454c66574950`. No new HeyGen generation, narration, identity, wardrobe, set, hand action or syllable timing is requested. Q's owner feedback is a preference for a better candidate, not final production approval; M remains the historically accepted baseline.

The treatment is a bounded local spatial stabilization of the visible head bob around “straight.” Native Vision measurements bind the head trajectory to exact Q frames. A conservative vertical counter-motion moves the face and hair together, with smooth spatial falloff toward the surrounding background and neck. No frame replacement, time remapping or mouth reshaping is used. The source audio is copied without re-encoding.

This is region-specific source-media preprocessing under `media-use/references/media-treatments.md`'s external tracking/tool route. It is not a new designed scene or a replacement for final Resolve conform. The head treatment must not be described as reducing 3D pitch: 2D translation can reduce bobbing but cannot remove the underlying change in chin/face perspective.

Acceptance: a visibly smaller dip on “straight,” natural residual motion, intact mouth timing/shape and hand movement, smooth onset/return, no visible shelf bending, halo, hairline shear or neck stretch. Judge moving output and actual pixel/landmark differences; hashes and successful rendering alone do not establish naturalness. A visibly worse treatment is retained only as a diagnostic and does not replace Q.

Picture/audio mode remains `presenter_address`, exact Q performance and spoken passage, fixed landscape study setup. Synthetic presenter remains illustrative identity footage, not case evidence. No canonical timeline, locked master, separate cinematic task, gate or release changes.
