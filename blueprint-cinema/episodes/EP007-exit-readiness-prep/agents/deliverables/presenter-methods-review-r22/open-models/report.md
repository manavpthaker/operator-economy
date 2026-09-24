# EP007 open-model methods review

Research only, 2026-09-08. Existing photo and locked audio are the only authorized creative inputs. No model was installed, run, or benchmarked.

**Recommendation:** Do not switch to InfiniteTalk or HunyuanVideo-Avatar on the assumption that either has a proven “subtle head, natural hands” setting. A bounded comparison using the same photo and audio is more useful than another elaborate prompt or stabilization pass. The evidence below does not rank either model above the hosted candidates being reviewed separately.

| Model | Verified conditioning and control | Relevance to EP007 |
|---|---|---|
| InfiniteTalk | Accepts image + audio + text, or video + audio + text. Separate text/audio guidance exists. `motion_frame` is prior-chunk context length, not motion amplitude. | An eligible photo/audio challenger, but no independent, documented head/hand amplitude control was found in the released generator. Unlimited duration is not a restraint feature. |
| HunyuanVideo-Avatar | Example input is image, audio, prompt, fps. Active internal head/expression motion embeddings exist, but values are hardcoded and not exposed as a calibrated CLI/Gradio control. | More technically controllable than the README alone suggests; still an engineering experiment, not a dependable quiet-head setting. No independent hand-strength control found. |

InfiniteTalk facts are bound to the [official generator](https://github.com/MeiGen-AI/InfiniteTalk/blob/50aa0a94184315407a991ae804d9b58d6d311ba8/generate_infinitetalk.py), [generation loop](https://github.com/MeiGen-AI/InfiniteTalk/blob/50aa0a94184315407a991ae804d9b58d6d311ba8/wan/multitalk.py), and [image example](https://github.com/MeiGen-AI/InfiniteTalk/blob/50aa0a94184315407a991ae804d9b58d6d311ba8/examples/single_example_image.json). Hunyuan facts are bound to its [input example](https://github.com/Tencent-Hunyuan/HunyuanVideo-Avatar/blob/8c31d0d489df8418fa36a2a709ebdf0b47c7bf06/assets/test.csv) and code below.

## The important control distinctions

**InfiniteTalk:** Default `motion_frame=9` supplies temporal context between generated chunks; the standard chunk contains 81 frames. Its paper deliberately permits new head, face, and body motions while retaining sparse visual references. Video conditioning is soft, not exact performance preservation. SDEdit/Uni3C in the paper concern camera-trajectory preservation; they are not demonstrated head-only damping controls for a still image. The current generator has no named SDEdit CLI argument. [Paper, §§3.3–3.4](https://arxiv.org/html/2508.14033v1)

The README recommends audio CFG 3–5 for synchronization; it warns that acceleration LoRAs trade away some identity preservation and that SDEdit can shift color. Reducing audio guidance is therefore not an established way to soften the visual accent on “straight” or “never” without affecting lip sync. [Official usage tips](https://github.com/MeiGen-AI/InfiniteTalk/blob/50aa0a94184315407a991ae804d9b58d6d311ba8/README.md)

**Hunyuan:** The data loader sets `motion_bucket_id_heads=[25]*4` and `motion_bucket_id_exps=[30]*4`. These are real conditioning inputs: the transformer embeds both and adds them to its modulation vector. The Gradio preparation code hardcodes the same values. However, the inspected release provides no documented valid range, calibrated magnitude, monotonic relationship, or independent hand equivalent. It would be inaccurate to call them unused variables, and equally inaccurate to promise that changing 25 to a smaller number produces suitably smaller head movement. [Loader](https://github.com/Tencent-Hunyuan/HunyuanVideo-Avatar/blob/8c31d0d489df8418fa36a2a709ebdf0b47c7bf06/hymm_sp/data_kits/audio_dataset.py#L131), [transformer](https://github.com/Tencent-Hunyuan/HunyuanVideo-Avatar/blob/8c31d0d489df8418fa36a2a709ebdf0b47c7bf06/hymm_sp/modules/models_audio.py#L557), [Gradio preparation](https://github.com/Tencent-Hunyuan/HunyuanVideo-Avatar/blob/8c31d0d489df8418fa36a2a709ebdf0b47c7bf06/hymm_gradio/tool_for_end2end.py#L63)

The paper’s Audio Emotion Module uses an emotion-reference image; emotional style is distinct from independently limiting head displacement or specifying a small hand gesture. That extra input is outside the present photo/audio-only boundary. The paper itself reports limitations when emotions change during one clip. [Paper, §§3.4 and 6.2](https://arxiv.org/html/2505.20156v1)

## Practical costs and one current alternative

Hunyuan’s official baseline requires NVIDIA CUDA/Linux: minimum 24GB for its stated 704×768×129-frame case, described as very slow, with 96GB recommended. Its “10GB” route is an explicitly linked third-party Wan2GP integration, not the same baseline. These are not measured EP007 runtimes. [Requirements](https://github.com/Tencent-Hunyuan/HunyuanVideo-Avatar/blob/8c31d0d489df8418fa36a2a709ebdf0b47c7bf06/README.md#-requirements)

InfiniteTalk uses a 14B Wan model with CUDA dependencies, offloading, and quantization options. The inspected official README does not establish a reliable numeric minimum VRAM for this exact short input; no Mac-native execution claim is supported. [Installation and low-memory examples](https://github.com/MeiGen-AI/InfiniteTalk/blob/50aa0a94184315407a991ae804d9b58d6d311ba8/README.md)

**LongCat-Video-Avatar 1.5** is a relevant newer open alternative, but no evidence reviewed establishes superior restraint. Its official release uses Whisper-large-v3 and required distilled inference, supports photo/audio, and provides reference-index/mask-range controls to mitigate repeated actions. Those are not per-limb amplitude controls; excessive masking can introduce artifacts. Its newer audio encoder and eight-step recipe make it an efficiency/sync candidate, not a proven solution to this performance complaint. Do not add it to the immediate comparison solely because it is newer. [Official release and controls](https://github.com/meituan-longcat/LongCat-Video/blob/6b3f4b8582a8bc3f20f795735f5383716c4ba794/README.md#run-longcat-video-avatar)

## License differences that affect the episode

InfiniteTalk’s released license is Apache 2.0; LongCat states MIT for weights. Hunyuan uses Tencent’s community license, including restrictions on use/display of outputs outside its defined territory (which excludes EU, UK, and South Korea), plus conspicuous machine-generated identification for public content. It cannot be treated as an unrestricted Apache/MIT substitute for a globally viewable episode. This records the actual clauses, not a conclusion about how a particular hosted service licenses its output. [InfiniteTalk license](https://github.com/MeiGen-AI/InfiniteTalk/blob/50aa0a94184315407a991ae804d9b58d6d311ba8/LICENSE.txt), [LongCat license statement](https://github.com/meituan-longcat/LongCat-Video/blob/6b3f4b8582a8bc3f20f795735f5383716c4ba794/README.md#license-agreement), [Hunyuan §§1(l), 5(c), Exhibit A(12)](https://github.com/Tencent-Hunyuan/HunyuanVideo-Avatar/blob/8c31d0d489df8418fa36a2a709ebdf0b47c7bf06/LICENSE)

## Bounded test direction

Keep the accepted existing hand-visible photo and exact 5.600-second WAV fixed. Preserve the waveform in final editorial; InfiniteTalk’s preparation resamples and loudness-normalizes audio for its inference path, so a provider-returned track should not silently replace the locked master. [Audio preparation](https://github.com/MeiGen-AI/InfiniteTalk/blob/50aa0a94184315407a991ae804d9b58d6d311ba8/generate_infinitetalk.py#L283)

Proposed positive direction, **an experimental prompt rather than a guaranteed control**: “A seated presenter speaks conversationally to the camera. His head stays comfortably centered. Both forearms rest on the desk; one relaxed hand makes a small tabletop gesture. Natural blinking and precise conversational articulation. Fixed camera.”

Judge normal-speed playback first: restrained accents on “straight” and “never,” coherent mouth timing through the second sentence, a relaxed quiet interval, and hands that remain anatomically coherent. Compare two fixed-input seeds per shortlisted model before investing in its setup. Do not add new image edits, audio stress treatment, or synthetic head scaling during this comparison.

A paper/repository feature does not establish that a hosted endpoint exposes it. Endpoint version, accepted inputs, prompt behavior, motion controls, and output licensing must be checked separately. No open-model winner or production approval is claimed.

