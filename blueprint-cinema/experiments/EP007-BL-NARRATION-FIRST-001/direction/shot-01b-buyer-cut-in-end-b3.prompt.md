# Shot 1B — B3 buyer cut-in endpoint

## Purpose

Move the buyer's attention from the owner at far left to the visible workshop just right of her,
without changing his lower face or the scene outside the upper-face mask.

## Image-edit prompt

Surgical endpoint edit of this exact locked 85mm workshop close-up. Preserve every object, pixel relationship, crop, light, identity, clothing, blurred owner foreground, and background. The man currently looks toward the blurred owner at far viewer-left. Shift his attention away from her and onto the workshop equipment just to the viewer-RIGHT of her blurred head, near the center of the frame. Anatomically, move the pupil of his visible eye toward viewer-right and rotate his eyes and upper head only about 3-to-5 degrees toward a slightly more frontal angle. He must NOT look into the camera; his focus stops on the mid-background cabinet and bench left of center. Keep his lips, mouth, jaw, beard, neck, shoulders, and expression exactly unchanged and neutral. Lips closed. No speech, realization, reaction, brow raise, nod, downward look, camera motion, new text, person, or object. Same take, adjacent endpoint frame.

## Local-composite rule

The edited image is a candidate. `build-shot-01b-b3-endpoint.sh` transfers only the feathered
upper-head and eye region onto the selected start still. It forces the mask to zero below image row
340, preserving the buyer's mouth, jaw, neck, body, owner foreground, and lower frame as exact
start-image pixels.

