# EP009 phone review access

The current r4 review is served privately through Tailscale Serve on HTTPS port **3071**, path `/ep009-r4-review.html`. The exact private link was supplied in the owner conversation. The phone must have Tailscale connected to the same network; this Mac and its review server must remain online.

Serve runs in the background and proxies the existing byte-range server on `127.0.0.1:3070`. The pre-existing HTTPS443 service is unchanged. Port3071 has no public Funnel entry.

The review page now uses a grid that fits narrow screens and `playsinline` on all four videos. At a375px viewport, no horizontal overflow was observed; all four videos loaded with the expected durations and no media errors. All four MP4s passed first-byte and final-byte HTTPS range requests, matching local bytes. Video files and owner locks are unchanged. Actual playback on the physical phone has not been observed.

The pre-mobile page is preserved beside this file. `VERIFICATION.json` binds the current page, prior page and media checks. To stop only this private proxy, use the installed Tailscale CLI with `serve --https=3071 off`; do not reset the full Serve configuration.
