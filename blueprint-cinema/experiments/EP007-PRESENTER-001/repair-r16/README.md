# R16: visible hands and softer facial emphasis

Owner feedback after playback: “the straight and never aere too pronounced.” O is not accepted as the new performance baseline. P tests smaller articulation and supported movement during the pause; see `../repair-r17/`. M remains accepted.

M remains the owner-accepted performance baseline. The owner found no hand or arm movement in N and found its stress on “straight” too pronounced. This test changes the source framing so the generator can see the forearms and hands, then requests one small palm-up action and relaxed facial articulation. It does not change the exact locked narration.

## Source image edit

Built-in image generation edited the actual accepted `study-look-candidate-03.webp`, not a talking-video frame. The goal is the same identity, navy shirt, clear glasses, restrained study and soft window light, with a slightly wider medium shot and visible forearms/hands at a plain wood desk. Output: `../media/repair-r16/study-visible-hands-source.png`, SHA256 `2abb05079084198c21a33802e6e0aa6373027a65f2163ea5a9114f77c1c4da24`, 1672x941. Original generated path: `/Users/brownmanbrain/.codex/generated_images/01a07aa0-5764-78b1-a4e8-5f56cbe3ae34/exec-6c7e9a12-cd7f-4cf2-b436-c2e7e9066495.png`. The complete built-in edit prompt is `image-prompt.txt`.

Visual inspection: the same recognizable face, glasses, navy-shirt style, soft daylight and shelf setting are retained; both forearms and hands are visible. The right hand is already loosely open above the desk; the left rests on it. This is a newly generated extension, not pixel-identical accepted imagery or newly owner-approved identity. No talking-video expression was used as the identity reference. The original accepted photo and M remain untouched.

## Performance test O

Result: actual right-hand and forearm movement is visible, including lifts around 0.75–1.0 seconds and 4.0 seconds. The generator produced two lifts rather than the single requested action. Sampled wrists remain connected; moving fingers soften and overlap around 1.0 seconds, limiting exact finger-anatomy assessment. The wider framing shows the gestures clearly.

The output does not preserve M's exact head performance: sampled displacement normalized by face size is about 65 percent higher, with similar roll. The audible stress on “straight” is unchanged because the original narration is retained. Softer visual emphasis is unverified pending moving playback. M remains the accepted baseline; O is a candidate.

Full decode passes: 1920x1080, 25 fps, 140 frames, 5.600 seconds of picture. Both sentences retain the same 23.0208 ms audio delay, with no measured drift and complete final-word coverage. See `technical-review.json` and `head-motion-review.json`. These checks do not establish visual lip-sync accuracy.

Requested setup: direct-image Avatar IV, explicit low expressiveness, landscape 1080p and exact 5.600-second uploaded WAV. One primary physical action: the right hand lifts/turns palm-up slightly above the desk and returns to rest; the left arm rests. The direction requests a level, almost-still head and relaxed natural articulation without extra facial emphasis on individual words. The request cannot guarantee exact word-timed gestures or an unchanged M performance.

Mode is `presenter_address`; the exact narration carries language and visible speech is meant to synchronize. Same direct-to-lens seated setup, identity/wardrobe/location/light anchors, no camera motion or cuts. Initial image: relaxed supported forearms, right hand loosely open. Final image: hand settled back to the desk. The source window and wording remain master591.050–596.650, W001663–W001678. The new desk is an illustrative set extension with no documents or evidence claims.

Review against M: hand movement must actually happen, anatomy and return must remain plausible, and the visual stress on “straight” must not become stronger. Preserve the spoken pause and final word. Numerical audio alignment and silent frames do not replace owner playback review.

One built-in image edit and one bounded HeyGen video generation under the continuing hand/arm repair request. Existing subscription credits, no purchase or plan change. No canonical timeline, narration, separate cinematic task, or production-gate changes.
