# Landscape study presenter

Owner request: “landscape study”, following selection of Avatar III test F as the better performance route and delivery of full-passage test G.

Keep the existing G performance and audio. A tight portrait recording cannot supply missing shoulders. Native HeyGen background replacement was tested in revision `573d66052c234fe299feb560c5d9f817`; the new room was confined to the original portrait box. No new HeyGen render was submitted for that draft.

Local candidate: macOS Vision person segmentation on G, with a generated empty study and a still outer-shoulder extension. HyperFrames owns composition and rendering. The generated reference face must not be used in the output; use the actual moving foreground from G. The shoulder extension is synthetic and static. Seam quality, matte stability, mouth continuity, and audio require review before selecting this as the episode treatment.

Inputs:

- G: `media/repair-r7/test-g-full-scope-avatar-iii-1080p.mp4`, SHA256 `6bfc0bd9190448e4a41d7ea694797ee48135d6ece85467a90bfb3e11926c749f`.
- Study: `media/repair-r8/restrained-study-background.png`, SHA256 `da3301d1c898f1f45ac3904d2695d2e1f4ca70ec5d0bc0dddb716f84fbc125c9`.
- Source reference: exact frame at 0.4s, portrait crop 608x1080 at x=656, y=0.
- Extension reference: `media/repair-r8/study-shoulder-extension-reference.png`.

Image tool: built-in `image_gen.imagegen`; first call new generation, second call image edit with source frame and study references. Original generated files remain under the Codex generated-images folder. Prompts are recorded in `image-prompts.md`.

This is a presenter experiment. No canonical gate, locked narration, film work, or publishing state is changed.
