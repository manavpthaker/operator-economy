# EP007 avatar V5: hand movement

Owner request: “okay the wide framing is great but now we need to include hand movement as im talking”

**V5 is owner accepted and locked as the current avatar baseline.** See [ACCEPTANCE.json](ACCEPTANCE.json) and [PERFORMANCE-BASELINE.md](PERFORMANCE-BASELINE.md). The lock includes the wide framing, hand movement and brief eye movement/look-away. Future hand gestures may vary with the passage's context. V5 keeps the V4 wide portrait, Rebecca and Henry behavior reference roles, and the exact 0–20.9-second EP007 opening narration from the accepted V3 recipe.

Review: http://192.168.1.159:53833/ on the same local network. V5 appears first, with V4 continuous wide and V3 delivery baseline for comparison. The V5 server now owns this existing port; see PHONE-ACCESS.json for its PID.

## Selected review file

- `media/gesture-review.mp4`: continuous wide 1080p, 24 fps, 505 frames, 21.042 seconds. H264 8-bit, original restored AAC copied unchanged, faststart.
- `media/generated-original-audio.mp4`: preserved Fal-restored source, H264 10-bit.
- `media/generated-native.mp4`: preserved Seedance output; its native voice is not the selected soundtrack.

No crop, camera move, editorial cut, frame interpolation or retiming was added. The accepted wide composition stays visible throughout.

## Performance findings

Sampled gestures occur around 0.75–2.00, 3.25–5.25, 7.00–12.75 and 17.50–19.25 seconds, with rests between sections and at the end. No obvious hand-anatomy or identity failure was seen in the inspected frames. The earlier concern about repeated middle gestures was presented to the owner, who accepted the current take and allowed context-sensitive variation in future takes. No further correction of this accepted artifact is pending.

The independent motion report inspected 71 distinct native frames. Root inspected 12 restored frames, the bottom image edge, media decoding, original audio preservation, and host browser playback. These checks do not certify naturalness or establish perceptual lip-sync quality. Actual phone-device playback is unverified.

## Provenance

`SUBMISSION-INTENT.json` and `PROMPT.txt` pin the exact request. One Higgsfield Seedance 2.5 generation used 189 credits, balance 2596.5 to 2407.5. Generation job: `80356785-3ab8-442d-a422-5928e5e3fd50`. One normal Fal Sync v3 restoration used request `01a090b8-023e-78e1-a309-4396ac3d6407`; actual Fal charge was not returned.

`INPUT-MANIFEST.json`, `FRAMING-ACCEPTANCE.json`, `QA.json` and `OUTPUT-MANIFEST.json` bind the source recipe, scoped acceptance, and this result. Earlier accepted media remain preserved. This isolated experiment does not change canonical episode picture, narration, or publication state.
