# EP009 / public №002 — upload verification, 2026-10-12

Uploaded and scheduled by `launch.py --go` from `studio/`, then read back from the
YouTube Data API. The API is the source of truth here, not YT Studio: a video can
sit plain-private with `publishAt` silently dropped and the Studio UI looks the
same either way. Every row below is an API read.

Channel: @operatoreconomy (credential `studio/.secrets/token.json` — *not* the
personal "MP Thaker" token in content-os).

| Video | ID | privacy | publishAt (UTC) | ET | duration | HD | notes |
|---|---|---|---|---|---|---|---|
| Episode | `vx25OoVALSA` | private | 2026-10-19T15:00:00Z | Mon 10-19 11:00 | PT20M22S | hd | 13 tags; description 2,312 chars; Canvas URL present; captions serving; custom thumbnail (maxres + uhd) |
| Short 01 | `sddAFS0-hoU` | private | 2026-10-20T12:30:00Z | Tue 10-20 08:30 | PT46S | hd | description 880 chars, episode link substituted |
| Short 02 | `05sKrP5VIf0` | private | 2026-10-21T12:30:00Z | Wed 10-21 08:30 | PT45S | hd | description 869 chars, episode link substituted |
| Short 03 | `-CZXLPy8wK4` | private | 2026-10-22T12:30:00Z | Thu 10-22 08:30 | PT46S | hd | description 882 chars, episode link substituted |
| Short 04 | `8aC8AF7bKYw` | private | 2026-10-23T12:30:00Z | Fri 10-23 08:30 | PT50S | hd | description 1,066 chars, episode link substituted |

`containsSyntheticMedia: true` on all five, set by `upload_youtube.py` at insert.
That is the altered-or-synthetic-content disclosure; it is not a separate manual
step in Studio. `madeForKids: false` on all five.

Episode duration PT20M22S matches the delivery master (1221.8 s = 20:21.8).

## Closed beyond the script

Two items the generated checklist lists as manual YT Studio work were done
through the API instead:

- **Captions.** `captions.insert` with `launch/ep009-captions.en.srt` (368 cues),
  language `en`, name "English". `contentDetails.caption` now reads `true` and the
  track status is `serving`.
- **Thumbnail.** `thumbnails.set` with `launch/thumbnail.jpg` (1.76 MB, under the
  2 MB API limit), the owner-ratified HELP HER KEEP THEM card. The checklist line
  says "Thumbnail = title-card frame"; that is the old default and is superseded
  by the ratified card. `maxres` and `uhd` renditions confirm the custom upload.

Still manual, with no API path: the end screen (last 6 s, Subscribe +
best-for-viewer), and posting/pinning the per-Short episode-link comments —
`links.json` carries the exact pinned text for each. Comments on a still-private
scheduled video may be rejected, so pin them once each Short goes live.

## Verification commands

```
python scripts/originate/verify_youtube_schedule.py <id> --publish-at <iso> --wait 2400
```

Run it with `--publish-at` *before* the id for Short 03: `-CZXLPy8wK4` begins with
a hyphen and argparse reads it as a flag otherwise (`--` before the id also works).

## What is not done

- **The site is not deployed.** The №002 page builds and was verified locally, but
  the commit is on `ep009-shorts-netnew-narration` and production builds from
  `main`. The episode description links to
  `theoperatoreconomy.com/businesses/direct-booking-practice`, so that page has to
  be live before Mon 2026-10-19 11:00 ET or the link 404s for the first hour's
  traffic.
- **The launch-day site flip has no working script.** The checklist still says
  `python scripts/originate/publish.py direct-booking-practice`. That script writes
  `site/data/episodes.json`, which no longer drives the library — the site reads
  `site/app/lib/operations.ts`. It exits 1 on an unknown slug, so it cannot
  silently appear to work, but the flip is currently a manual edit: set №002's
  `youtubeUrl` from `launch/links.json` and redeploy.
- **Four launch-week derivatives were never generated**, so `launch.py` skipped
  their rubric gates: `content/linkedin_posts.md`, `content/newsletter.md`,
  `content/launch_linkedin.md`, `content/trailer_linkedin.md`. The checklist's
  Sunday posts, Monday OE page post, and hour-one newsletter send all depend on
  them.
- **No trailer.** Skipped by design — a missing trailer never delays the episode.
