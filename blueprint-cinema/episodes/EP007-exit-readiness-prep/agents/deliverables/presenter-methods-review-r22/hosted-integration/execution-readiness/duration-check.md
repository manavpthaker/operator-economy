# InfiniteTalk: 5.600-second frame-count correction

Updated 2026-09-08 using the parent's live hosted request records. This worker only read public documentation and local records; no keys, uploads, or submissions.

**The original recommendation to use `num_frames: 145` is superseded.** Both hosted requests failed with terminal HTTP 422 `value_error`: fal requires at least 5.80 seconds of audio for 145 frames and rejects the unchanged 5.60-second input. The earlier inference that extra frame capacity would provide safe headroom was wrong for this hosted endpoint.

Exact returned message:

> Audio is too short (5.60s) for the requested num_frames. The audio must be at least 5.80s long. Either provide a longer audio file or reduce num_frames.

Local evidence: [infinitalk-02.json](/Users/brownmanbrain/GitHub/operator-economy/blueprint-cinema/experiments/EP007-PRESENTER-001/repair-r23/infinitalk-02.json), and `prior_attempts[0]` in [infinitalk-01.json](/Users/brownmanbrain/GitHub/operator-economy/blueprint-cinema/experiments/EP007-PRESENTER-001/repair-r23/infinitalk-01.json).

**Final verified setting: `num_frames: 137`, with the exact original audio unchanged.** The attempted 140-frame request was also rejected: fal required 5.64 seconds, consistent with rounding up to a 141-frame window. Both subsequent 137-frame requests succeeded. Their native outputs are 137 frames at 25fps, with 5.480 seconds of picture and audio. These are observed hosted results, superseding the earlier queued 140-frame experiment.

Documentation context retained for provenance:

- fal's photo endpoint accepts 41–721 frames, default 145. It exposes neither fps nor a duration field. [Official fal schema](https://fal.ai/models/fal-ai/infinitalk/api)
- The official upstream `generate_infinitetalk.py` says per-clip frame count should be `4n+1`. Its audio embedding path multiplies audio duration by 25 and supplies that sequence length to the audio encoder. [Official generation source](https://github.com/MeiGen-AI/InfiniteTalk/blob/main/generate_infinitetalk.py)
- Upstream `save_video_ffmpeg` defaults to 25 fps, computes duration as frame count divided by fps, crops audio to that duration, then muxes with FFmpeg `-shortest`. [Official save function](https://github.com/MeiGen-AI/InfiniteTalk/blob/main/wan/utils/multitalk_utils.py)

The upstream `4n+1` guidance does not establish an additional restriction in fal's hosted schema. Applying it by rounding this request up to 141 or 145 would require more than 5.60 seconds of audio under the observed hosted duration check. Do not pad or retime the approved audio to accommodate the earlier recommendation.

**Verified ending coverage:** both outputs retain the checked final-word window through 5.35 seconds, with 0.13 seconds of remaining picture. The omitted input tail from 5.48–5.60 seconds is near-silent (RMS −107.5dBFS, peak −90.3dBFS). Both have 0ms measured early/late audio lag and no measured drift. See [the current run status](/Users/brownmanbrain/GitHub/operator-economy/blueprint-cinema/experiments/EP007-PRESENTER-001/repair-r23/STATUS.md) and the linked native technical reports. Full-speed visual lip sync and naturalness remain unverified; no conform or audio modification was performed.
