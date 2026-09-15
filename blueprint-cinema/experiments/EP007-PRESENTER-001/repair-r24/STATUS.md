# InfiniteTalk / Seedance 2.5 comparison — September 9, 2026

**Blocked by Seedance's portrait policy. No Seedance clip was produced.**

The owner prefers InfiniteTalk among the prior four results and requested Seedance 2.5 as the next comparator. This records a model-family preference, not selection of one specific take or final episode approval. Both existing InfiniteTalk files remain the baseline; they were not regenerated.

The exact model exists in fal's authenticated catalog: `bytedance/seedance-2.5/reference-to-video`. Its schema accepts the existing image and 5.600-second audio reference. Source and CDN byte hashes were verified, and the exact files were reused. The six-second, 720p, 16:9 test retained the common restrained-motion prompt, with the model's required `@Image1` / `@Audio1` references and instructions to preserve the narration's voice, words and timing. No source media was edited.

The first request, `01a08485-fbaf-7fc2-a78b-0ab972f86045`, entered the queue and terminated with HTTP 422:

> The images or videos provided may contain likenesses of real people or other private information that cannot be processed.

The response class is `content_policy_violation`, partner reason `partner_validation_failed`, located at `image_urls`. See `seedance-01.json` for the actual request and response. No quality comparison, native audio check or lip-sync judgment is possible without an output. The second sample was not submitted; the image was not disguised and the request was not retried.

Two new successful samples had been prepared, estimated at about $5.68 total based on fal's published approximate 720p rate and live $0.0214 per 1,000 tokens. This is not actual spend. A terminal error does not establish that the request was free; the supplied key did not permit billing reads in the preceding round.

Sources: [Seedance 2.5 reference API](https://fal.ai/models/bytedance/seedance-2.5/reference-to-video/api), [fal pricing explanation](https://fal.ai/learn/tools/what-is-seedance-2-5), [ByteDance's official launch](https://seed.bytedance.com/en/blog/one-take-creation-flexible-referencing-introducing-seedance-2-5).

The remaining dependency is a documented, authorized portrait workflow for this model. The prepared test also needs to verify audio preservation: Seedance jointly generates audio, so receiving the original WAV as a reference does not establish unchanged narration or timing. No soundtrack replacement is part of this comparison. All episode gates remain unchanged.

## Authorized portrait access check

The public fal schema does not document an own-likeness enrollment or verification field. Its `end_user_id` is an identifier, not documented consent verification. No supported route using only the existing photo/audio and the current fal key was established.

BytePlus LAS documents applying for access to an allowlisted material library, uploading authorized portrait materials after approval, and referencing them using `asset://<ASSET_ID>`. Seedance 2.5 is supported there. The public documentation does not establish the application form, approval criteria or turnaround. LAS requires its own account/API key; the current fal key is not direct LAS access. [LAS generation](https://docs.byteplus.com/en/docs/byteplus_las/video_gen_enhanced), [LAS authentication](https://docs.byteplus.com/en/docs/Byteplus_LAS/Obtain_and_configure_the_API_Key).

BytePlus separately documents personal live-person verification and same-person authentication, including comparison of a live capture with portrait materials. That verification process requires a fresh verification capture, not a new talking-head performance. Whether this is the required LAS enrollment workflow, or whether another approved existing-material-only workflow exists, remains unverified. [Verification rules](https://docs.byteplus.com/en/docs/ModelArk/BytePlus_Real_Person_Verification_H5_and_API_Usage_Rules?lang=en), [individual notice](https://docs.byteplus.com/en/docs/ModelArk/2260831).

The concrete next step is to ask fal support whether it exposes approved own-likeness access for this endpoint, and what verification it requires. A request with the exact failed request ID is prepared in `SUPPORT-REQUEST.md`; it has not been sent. No provider switch, enrollment, new capture, new upload or retry was performed. [Official fal support](https://fal.ai/docs/documentation/model-apis/support).
