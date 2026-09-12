# Phone delivery correction

The owner reported that the original Fal URL opened as a tiny unusable video in the phone's in-app viewer. The previous localhost comparison link was also only reachable on the Mac; it was not a mobile delivery link.

The source passed decoding and had the correct dimensions, H.264/AAC formats, fast-start layout, and HTTP range responses. Its audio stream was first. Fal also served a restrictive document CSP. These are observed packaging/hosting differences, not proof of the phone failure's cause.

The correction remuxes the existing file without re-encoding, maps video before audio, and writes a fast-start MP4. It is hosted through the established Higgsfield CloudFront upload route and displayed as the newest video in the media widget. No generation call occurred. The original remains retained with its provenance.

[Replacement delivery link](https://d2ol7oe51mr4n9.cloudfront.net/user_3J3m5xtqP8Xv0MOsPutf0uV3maX/6d2f395d-2853-475f-b5c2-199d14c8eeff.mp4)

`READBACK.json` records byte-identical hosted readback, matching original/remux decoded video and audio hashes, HTTP 200, video/mp4, and working HTTP 206 range support. No CSP header was present in the replacement response. Browser verification showed active playback at 9.754 seconds with no media error, 720 by 1280 source dimensions, and a full-height 405 by 720 player. The screenshot showed the portrait video filling that player. This verifies the replacement in the desktop browser; owner iPhone playback is not independently confirmed.
