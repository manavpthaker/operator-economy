# Test K: restored photo look with Avatar III

The user approved the restored earlier navy-shirt study portrait (candidate 03) and requested limited mouth movement. This bounded test changes the rendering engine for that existing look to Avatar III, using the same 5.600-second original narration used in the earlier performance tests.

## Inputs

- Look: `../media/study-look-candidate-03.webp`, SHA-256 `59309d2925b85cfba8a6a411dce1ecea67a03607f8a05933f4a2f6cb6af27754`; HeyGen talking-photo asset `dd0bb50578ce4c17bee712e72ed2d84f`, under owner-provided group `cc6abe9744e74df7a103b7a37262d2f7`.
- Audio: `../media/repair-r2/scope-two-sentences.wav`, SHA-256 `c565f1dfe8c218f156e9d0b76d0515a264be26cc1d0cea7d1ea8977a3c565566`; exact source interval and word IDs in `../repair-r2/input-manifest.json`.
- Preferred motion reference: Test F, `../media/repair-r6/test-f-original-footage-avatar-iii-1080p.mp4`, SHA-256 `d5c590fb00f9d5fda21af2d175048b94de64fb96413aa87ef215148d89727bcb`.

## Live setup

HeyGen signed-in Chrome session, Single scene. Selected photo source was verified from its visible image URL. Model menu offers Avatar III with the description “Applies lip sync.” Selected Avatar III, existing verified uploaded `scope_two_sentences.wav`, Voice Mirroring off, landscape icon and 1080p. Avatar III has no exposed Motion/More Expressive controls in this UI; no separate jaw-amplitude setting is claimed. The top Presenter tab retains a generic Avatar V badge even while the actual model selector reads Avatar III; record the explicit selector.

This tests the preferred engine on the approved appearance. It is not an exact transfer of F's mouth frames and does not prove reduced movement before review. Compare final appearance with candidate 03, and articulation/mouth behavior with F. Inspect the inter-sentence pause and the stresses on straight and never. Measure returned audio offset independently.

No fresh portrait generation, narration change, background composite, cinematic edit or production gate change is authorized by this test. The user has authorized this bounded HeyGen generation through the current request and continued iteration; no account purchase or upgrade is included.
