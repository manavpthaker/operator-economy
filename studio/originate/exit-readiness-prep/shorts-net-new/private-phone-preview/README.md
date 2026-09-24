# EP007 private phone preview (staged, not live)

This is a local replacement for the temporary Short 01-only player on port 3113. It is **not**
running on that port. It has no upload, publishing, episode-link, or approval action.

The owner-review page uses the Boundary Ledger's mineral/paper palette with one oxide selection
line. The video is the focal point; the four tabs are a real four-short sequence, not decorative
cards. Native phone video controls remain available. There is no autoplay or ambient motion.

## Fail-closed contract

- Exactly four routes are allowed: `/short-01` through `/short-04`; `/` opens Short 01.
- `manifest.json` binds a separate MP4 and poster to each ready slot by repository-relative path
  and full SHA-256. A null pair means **no video yet**. Short 01 is bound to its accepted clean-frame
  review copy. Shorts 02–04 are deliberately null until actual finished files pass technical QA.
- Media URLs contain the full hash. An absent file, changed bytes, stale hash URL, or path outside
  the repository cannot silently display a different video. Hashes are checked from the opened
  file before every response; the same file descriptor serves the bytes. The manifest is read at
  server start, so binding a new render requires a restart.
- `GET` and `HEAD` support a single byte range, including suffix ranges; invalid ranges return
  `416`. All responses use `no-store`. A video is never copied into a web/public directory.
- The server binds **only** `127.0.0.1`. Its default mode refuses to start without a 16+ byte
  password; every route then requires HTTP Basic authentication with user `review`.
- For the existing EP007 phone route only, `EP007_PREVIEW_TAILNET_ONLY=1` permits passwordless
  playback after a startup check confirms `mini.tail1c89f5.ts.net:3113` is Tailscale HTTPS
  serving `127.0.0.1:3113` and **not** Funnel. This preserves Short 01's phone experience. The
  live Tailscale configuration was read back on 2026-09-23; this server does not change it. If the
  private-route check fails, startup fails closed. Never use this mode on another port or expose
  the route through a public tunnel.
- The phone page does not claim owner acceptance for Shorts 02–04 or release of any Short.

## Local smoke test (no live service change)

From the repository root, run `node --check` on `server.cjs`, then start it with a private test
password and an unused loopback port (for example `EP007_PREVIEW_PORT=39219`). With `curl`, check:

1. `/short-01` and `/healthz` return `401` without Basic auth.
2. Authenticated `/healthz` reports Short 01 true and the three unbound Shorts false.
3. `/short-02` says `No verified video yet` and contains no `<video>` element.
4. Short 01's hash URL returns `206` with `Range: bytes=0-1023`, `416` for an impossible range,
   and the full response hashes to the MP4 SHA-256 in `manifest.json`.
5. A made-up hash URL or an unbound Short 02 media URL returns `404`.

These checks were performed on port 39219 on 2026-09-23. They prove local serving behavior, not
physical iPhone playback or the Tailscale route.

## Binding finished Shorts 02–04

For each Short, first finish its sound-on render, poster, full decode, exact narration/caption,
visual seam, and private-review technical checks. In `manifest.json`, replace that Short's two
`null` values with the **actual** repository-relative paths and `shasum -a 256` outputs. Do not
point at a silent animatic, native generated presenter source, or an unverified render. Restart
the staged server and repeat the smoke test. A manifest edit is not owner acceptance.

## Cutover only after final files and a verified private route

Current observed live job: `com.openai.ep007.phone-wrapper`, a `launchctl submit` job running
`/opt/homebrew/bin/node /tmp/ep007-phone-preview.ZpdifN/server.cjs` on `127.0.0.1:3113`.
Tailscale's IPN extension also listens on this Mac's tailnet address at port 3113. The route's
ACL was not inspected here; confirm it is tailnet-private before changing the service.

1. Confirm the old `/tmp/ep007-phone-preview.ZpdifN/server.cjs` still exists for rollback.
   Re-read `/Applications/Tailscale.app/Contents/MacOS/Tailscale serve status --json`: port 3113
   must proxy to `127.0.0.1:3113` through HTTPS and must not appear in `AllowFunnel`. If that
   cannot be confirmed, use a 16+ byte owner-only password file outside the repo instead of
   tailnet-only mode; never put a password in a URL or repository file.
2. Verify all desired manifest bindings and test the staged server on a separate loopback port.
   Also verify the current live `launchctl` job, its output paths, and the tailnet HTTPS route.
3. During a brief cutover window, remove only `com.openai.ep007.phone-wrapper`, then
   submit that same label with `/usr/bin/env EP007_PREVIEW_PORT=3113
   EP007_PREVIEW_TAILNET_ONLY=1 /opt/homebrew/bin/node
   <absolute-repo-path>/private-phone-preview/server.cjs`. Keep the existing Tailscale route
   unchanged. Do not repoint a public route.
4. Confirm loopback `/healthz`, MP4 `HEAD`/range, and actual sound-on playback on
   the phone at the existing private HTTPS address. Treat phone playback as unverified until seen.

If cutover or phone playback fails, remove **only** `com.openai.ep007.phone-wrapper` and resubmit
it with the original `/opt/homebrew/bin/node /tmp/ep007-phone-preview.ZpdifN/server.cjs` command,
using the previously observed output/error paths. Recheck the old Short 01 `/healthz` and phone
page. This restores the original review wrapper; it does not undo or delete any renders.
