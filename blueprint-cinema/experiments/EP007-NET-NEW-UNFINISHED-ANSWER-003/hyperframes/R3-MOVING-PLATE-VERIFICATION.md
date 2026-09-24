# R3 moving-plate verification — `r3-route-c01`

Status: **technically valid; editorial and continuity rejection; preserved unmounted.**

This record verifies the one Veo 3.1 Fast request authorized by the owner on 2026-09-06. It does not authorize another generation, a select, a 24-to-30 fps treatment, HyperFrames integration, Step 3 advancement, or publication.

## Generation and provenance

- Candidate ID: `r3-route-c01`
- Provider: `fal.ai`
- Endpoint: `fal-ai/veo3.1/fast/first-last-frame-to-video`
- Provider request ID: `01a0793d-c955-77c1-9817-86db0109243a`
- Generated at: `2026-09-07T00:23:48.799Z`
- Provider-exposed model version: `UNKNOWN`; the response did not expose one
- Request: `8s`; `1080p`; `16:9`; audio off; seed `700703`; auto-fix off; safety tolerance `4`
- Commercial boundary: one request was authorized; Fal's list price at submission was `$0.10/s`, or `$0.80` for this request; the endpoint response did not return an account-debit receipt
- Submitted packet SHA-256: `45f848d61928cd715426ab6b64f4931de2a0346648368dc8b6de0e850e02dba8`
- Extracted `## Prompt`: 1,583 characters; SHA-256 `d953c4d3b1ee60e48d5856fbe99c111340d969712b060df4cf772f42161eeedd`
- Effective negative prompt: 1,046 characters; SHA-256 `6d5b2a4302095ad5ea9cee91d08d92e507e20783c704644953757bfb8627bf88`
- Generator script SHA-256: `6f72d94757c95ea87e5b6b1de4609db8ee41bc4552bd11e7d4a93be69252b43e`
- Start reference SHA-256: `5e13a9a45965a39d260dc7a25bd7d713c671619fa76dc5e8b384b6419bc639a7`
- End reference SHA-256: `6becc345680fa00281e56aedb56528aa04bf5fd958fe44cc93994154a8db1ac4`
- Untouched source: `renders/candidates/r3-route.veo-fast.full-generated.mp4`
- Untouched source SHA-256: `a8525034600f2837f0e01476f6dc82726a9e2789e15c9cbd10abdab0085c6b5e`
- Provider response and local provenance: `renders/candidates/r3-route.veo-fast.full-generated.mp4.response.json`
- Response-record SHA-256: `71c74a50a946da6ca933469d52f0f955783eee6a7e295140686d4cfb860bac02`

The generated media and response remain under the ignored `renders/` path. They are not mounted in the composition or added to the active source manifest.

## Technical verification

- Container: ISO BMFF / MP4
- Video: H.264 High, 1920×1080, progressive 8-bit `yuv420p`
- Cadence: true 24 fps CFR, 192 frames, exactly 8.000 seconds
- Audio: no audio stream
- Size: 12,825,693 bytes
- Strict decode: pass; FFmpeg reported no decode errors
- Black-frame scan: no black interval reported
- Freeze scan: no interval of at least 0.5 seconds reported at the tested `-50 dB` threshold
- Decoded-frame identity: 192 decoded frames, 192 unique frame hashes, zero exact duplicates
- Endpoint comparison: output frame 0 and frame 191 visually preserve the supplied start and end compositions but are not pixel-identical; scale-normalized all-channel SSIM was `0.799607` and `0.730561`, respectively

## Review evidence

- `snapshots/r3-veo-fast-c01/contact-sheet-24f.png`: 24-frame whole-clip sheet, one frame every eight source frames
- `snapshots/r3-veo-fast-c01/contact-sheet-f000-060.png`
- `snapshots/r3-veo-fast-c01/contact-sheet-f064-124.png`
- `snapshots/r3-veo-fast-c01/contact-sheet-f128-188.png`: three higher-frequency sheets, one frame every four source frames
- `snapshots/r3-veo-fast-c01/late-every-frame-f160-183.png`: every frame across the late failure
- `snapshots/r3-veo-fast-c01/frame-176.png`: full-resolution representative of the page-plane failure
- `snapshots/r3-veo-fast-c01/start-reference-vs-output.png`
- `snapshots/r3-veo-fast-c01/end-reference-vs-output.png`

The whole source was decoded. Review used the whole-clip sheet, three higher-frequency strips, every late-transition frame from 160 through 183, full-resolution failure and endpoint frames, and frame-difference measurements. This is sufficient to reject the candidate; it is not an owner asset-select approval.

## Ticket result

### What worked

- One blank ticket moves generally right-to-left toward the owner's side.
- The pencil generally follows the same route without producing readable text or a semantic mark.
- Faces remain cropped; no visible speech or reciprocal reaction appears.
- The buyer, binder, keys, table, lighting, and overall camera geometry remain materially stable.
- The large sheet and ticket remain visually blank in the reviewed frames.
- Hands remain broadly plausible through most of the move.

### Hard failures

1. **No pre-action handle.** The ticket hand is already moving within the first eight frames, well before the required approximately one-second hold.
2. **The action does not finish once.** After a near-settle, the free hand and pencil move again to converge on the supplied final frame. This reads as a second corrective gesture rather than one route followed by stillness.
3. **The page plane breaks.** Across approximately frames `172–177` (`7.17–7.38s`), the upper page boundary warps into a ragged yellow-white strip that reads as a lifted or additional paper edge. Frame `176` is the clearest failure.
4. **No clean final settle.** Motion continues through the final frames; the required at-least-1.5-second post-action hold does not exist.
5. **Full-span planar tracking is unsafe.** The central page remains useful for much of the clip, but the late boundary deformation and endpoint correction break the continuous physical plane required for the intended tracked route and hand occlusion.

These are declared stop conditions, not cosmetic defects. A visually clean earlier sub-window cannot supply both required handles inside the planned `00:21.28–00:26.80` timeline window without changing the approved action or timing contract.

## Decision

- Editorial result: `FAIL`
- Continuity result: `FAIL`
- Technical result: `PASS`
- Asset status: `rejected`
- Selected source range: none
- HyperFrames integration: none
- Planar track or hand-occlusion composite: not started
- Additional paid attempt authorized: no
- Disposition: preserve the untouched source, response, and review evidence as rejection history

