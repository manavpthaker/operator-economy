# Shot 1 — B2 localized endpoint

## Purpose

Replace the globally regenerated B1 endpoint with a controlled local edit. The owner, workshop,
props, buyer body, buyer mouth, and buyer jaw remain the start image. Only the buyer's upper-face
eyeline receives the generated edit, so the video model is not asked to animate unrelated pixels.

## Image-edit prompt

Make a surgical continuity edit to this exact locked-tripod live-action frame. Everything except the man's pupils must remain identical. Do not regenerate or restage the image. Keep the older woman, workshop, camera, framing, light, props, hands, notebook, wardrobe, and all faces exactly unchanged. Keep the man's head silhouette, hair, ears, nose, mouth, jaw, beard, neck, shoulders, and posture in precisely the same position and angle as the source. His closed lips and neutral lower face are especially untouchable. Change only his pupils/eye direction so that, while his head still faces the woman, his eyes look horizontally past her into the deep repair shop behind her. No head turn, no chin turn, no downward gaze, no speaking, no mouth movement, no reaction, no new text or object. This should appear to be a single adjacent frame in the same documentary take, with only an eye-line change.

## Local-composite rule

The generated image is a candidate, not the endpoint by itself. `build-shot-01-b2-endpoint.sh`
places only a feathered upper-face region from that candidate over the original start image. The
mask is forced to zero below image row 250, making the buyer's mouth, jaw, body, and the entire
lower frame exact start-image pixels. The entire left 700 pixels are also exact start-image pixels,
which preserves the owner. The mask is the only permitted area of change.
