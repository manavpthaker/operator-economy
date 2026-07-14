# EP002 thumbnail rework — 2026-07-12

The original `thumbnail-ep002.png` (split $11B / $500 card) broke thumbnail-rubric hard rules: no scene, serif display numerals (thin strokes die at 168px), branding kicker + OE mark (rule 1), text hugging the right edge (rule 4), and "$500 PER CLIENT / MO" wrapped badly.

Two new candidates render the concept locked at script gate (script.json `thumbnail_concepts[1]`: missed-call screen with a lost-revenue counter):

- `thumbnail-ep002-a.png` — text: "NOBODY PICKED UP" (from `thumbnail_text_options`; shares zero words with the title). Scene carries the money.
- `thumbnail-ep002-b.png` — text: "-$2,450 IN ONE DAY" (viewer's number leads; $2,450 = 7 missed calls x $350, the episode's own arithmetic).

Rubric compliance: 2 elements (scene + one text block), Supreme Extrabold sans, text bottom-left, no kicker/branding, scrim for contrast, 1280x720, shrink-tested at 320px and 168px (both read). Rule 3 (faces) is broken with a written reason: the concept locked at script gate is a screen close-up, no face in frame. The scene literally happens in the episode (missed-call math, evidence section).

## If you want the face/scene route instead (concept 1)

Gemini (Pro model, "Create image" first) prompt, then drop the PNG in this folder and I'll composite the text block + scrim in the same style:

"Photorealistic wide shot inside a work van cab, late afternoon light. A plumber in his 40s in a worn navy work shirt is halfway out the driver's door carrying a pipe wrench, glancing back with visible frustration at a smartphone lit up on the cluttered dashboard, incoming call on screen. Papers, coffee cup, tool bag on the passenger seat. Shallow depth of field, phone and face in focus. Warm subject against darker interior, cinematic, high detail, 16:9."

Upload path: YT Studio > EP002 draft > Thumbnail (API push still needs force-ssl re-auth, backlog #1/#3).
