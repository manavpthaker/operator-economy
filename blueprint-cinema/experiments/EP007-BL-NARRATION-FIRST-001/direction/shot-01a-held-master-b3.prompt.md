# Shot 1A — B3 held relationship master

## Purpose

Supply the first 31 timeline frames of the narration-first passage without requiring a generated
conversation. The same anchor is used at both endpoints. The only permitted motion is an
involuntary blink or breath; the audience receives the relationship before the word-motivated
cut-in.

## Prompt

Continue this exact starting frame as 33 frames of natural real-time observational documentary film at 24 fps. The 35mm chest-height tripod is completely locked. Preserve the exact competent older owner on screen-left, buyer on screen-right, repair shop, clothing, closed notebook, hands, tools, workbench, room geometry, and practical daylight. Both people hold their original eyelines and body positions for the entire clip. Their lips remain fully closed and neutral; neither speaks, mouths words, nods, reacts, gestures, or looks down. Permit only one ordinary blink or barely visible breathing. No camera pan, tilt, dolly, zoom, handheld drift, focus pull, reframing, slow motion, advising, negotiation, judgment, handshake, agreement, selling, contract, signing, price, money, page turn, readable text, logo, empty or failed workplace, morphing, distorted anatomy, extra person, or advertisement.

## Requested generation

- Model: `fal-ai/ltx-2.3-22b/image-to-video`
- Frames: 33 at 24 fps; timeline uses source frames 0–30
- Audio: off
- Camera control: static
- Seed: `1528090608`
- Start and end reference: `cast-environment-anchor.generated.png`
- Start and end strength: `1`

