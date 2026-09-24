# EP007 YouTube upload verification (2026-09-24)

Run by the scheduled task `oe-ep007-youtube-upload`. Source of truth for URLs: `launch/links.json`.

## What ran
- Preflight: episode master sha256 `3925de31…01f96` matched; `shorts/short-01..04.mp4` sha256 all present in
  `shorts-net-new/PRODUCTION-MANIFEST-V8.json`; `Operator-Canvas-001.pdf` present; links.json was `dry_run: true`.
- `launch.py … ` dry run: no errors, no unfilled placeholders; then `--go`: exit 0, 5 uploads, no retries.
- `thumbnails.set` (launch/thumbnail.jpg) → 200. `captions.insert` English, `ep007-r81-captions-en.srt` → 200.
- Playlists created (public; none existed): **Episodes** `PLCmSnXQWzHxo` (episode), **Shorts** `PLdu7PeWE3s2M` (Shorts 01–04). All 5 `playlistItems.insert` → 200.
- Quota used ≈ 8,000 + 50 + 400 + 100 + 250 + ~30 reads ≈ 8,830 of 10,000.

## videos.list check (after processing)

| Video | URL | privacy | publishAt (UTC) | ET | duration | notes |
|---|---|---|---|---|---|---|
| Episode | https://youtu.be/7juZ1KXdd04 | private | 2026-10-05T15:00:00Z | Mon 10-05 11:00 | PT18M54S (master 18:52.9) | title exact; 13 tags; description 2,475 chars with Canvas URL; caption=true; HD; madeForKids false |
| Short 01 | https://youtu.be/Hc9j4B9nnk8 | private | 2026-10-06T12:30:00Z | Tue 10-06 08:30 | PT44S | title = brief; episode link in description |
| Short 02 | https://youtu.be/mpGtH0WC1OA | private | 2026-10-07T12:30:00Z | Wed 10-07 08:30 | PT46S | title = brief; episode link in description |
| Short 03 | https://youtu.be/EtkyEqmKzUY | private | 2026-10-08T12:30:00Z | Thu 10-08 08:30 | PT40S | title = brief; episode link in description |
| Short 04 | https://youtu.be/UWI-v4M78do | private | 2026-10-09T12:30:00Z | Fri 10-09 08:30 | PT49S | title = brief; episode link in description |

## Limitations
- `containsSyntheticMedia`: every `videos.insert` response returned `True`, but `videos.list` does not echo the
  field back (absent from `status`), so it could not be re-read. **Confirm "Altered or synthetic content = Yes"
  in YouTube Studio on all five.**
- Thumbnail and caption display not viewed in Studio; only API 200 responses and `caption: "true"`.
- No human watch of the uploaded files.
