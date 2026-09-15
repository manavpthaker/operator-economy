# Test I: room integration diagnosis

**The strongest mismatch is focus and texture. Match the room to the retained presenter before changing skin exposure or warmth.**

This review covers hash-pinned Test I and its encoded frames at 0, 23.2 and 30.56 seconds. Each supplied PNG was verified pixel-identical to the corresponding decoded video frame. The clean study image and read-only R9 composition were also inspected. See `input-evidence.json` and `media/test-i-contact-sheet.jpg`.

## Ranked causes

1. **Focus/depth hierarchy reads backward.** The presenter's face and central collar are soft, while the window, books, shelving and remaining outer-shirt texture resolve noticeably more fine detail. This makes the person look like a softer insert inside a sharply rendered room. This is a visual judgment, not a measured focus-distance estimate: different materials and edge content prevent treating a generic sharpness score as proof.
2. **Localized boundary and material differences still identify the composite.** A faint pale contour persists at parts of the temple/ear/hair boundary. The center garment is smoother than the outer extension. The repaired shoulder corners and bottom coverage should stay fixed; additional geometry or motion changes are not indicated by these frames.
3. **Light direction/falloff is only partly shared.** The room implies strong daylight from screen-left. The face appears more broadly front-lit, with central forehead/nose highlights and comparatively little corresponding left-to-right falloff. The light is not demonstrably opposite, and the room could contain unseen fill light, so this is a secondary inference rather than a proven lighting error. A uniform exposure change cannot create directional lighting.

Overall subject exposure is not clearly wrong. Skin is already warm/reddish and the room warm beige. A blanket warming adjustment could exaggerate orange/red skin without improving placement. Skin-to-wall luminance ratios would be invalid because their reflectance, material and illumination differ; none are used here.

## One bounded improvement candidate

Make a single restrained **room-focus and edge integration** comparison:

- Apply a modest optical-defocus appearance to the room only, starting around a **2px Gaussian-equivalent at the final 1920px width**. This is a perceptual starting point, not a calibrated HyperFrames control value. Window and shelf structure must remain recognizable; fine room texture should stop competing with the eyes. Defocus itself reduces microcontrast, so do not automatically stack a large contrast reduction.
- Preserve the current subject exposure/white balance, outer-shirt treatment, exact frame sequence, narration, layout and measured shoulder transforms for this first comparison.
- If the pale contour remains after that change, restrict decontamination or a very small local color blend to the residual edge band. Do not broaden transparency into the eyes, glasses, face or shirt interior. Avoid a luminous outline or unsupported cast shadow. Preserve opaque facial geometry and timing.

Judge the same early/middle/final frames at full resolution and normal viewing size, then inspect movement for edge shimmer. Accept this candidate only if the room feels less separately rendered without becoming conspicuously blurred or making skin flatter/oranger. If it does not improve integration, retain Test I and reassess; no raster regeneration or new performance is needed for this comparison.

## Independent cross-check and limits

A separate read-only reviewer independently ranked focus/texture first, lighting second, and localized pale edge cleanup third. That reviewer also found no basis for declaring uniform underexposure or adding warmth. Its judgment covered the encoded first frame and clean room only; this packet's three-frame evidence is separately hash-bound.

No treatment was applied by this worker. The only raster output is a resized technical contact sheet. No provider, browser, installation, source edit, parent edit, motion change, narration change, approval or production-state action occurred. Still-frame diagnosis does not approve a moving composite or identify a physical lighting setup with certainty.
