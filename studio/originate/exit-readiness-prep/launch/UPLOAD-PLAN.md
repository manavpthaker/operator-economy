# EP007 upload plan: schedule for Monday 2026-10-05

Prepared 2026-09-23. **Nothing has been uploaded, scheduled, deployed or committed.** Every URL in
this plan comes from `launch/links.json` after `--go` writes it. Do not type a video ID by hand.

Episode: *The One-Person Business That Gets Companies Ready for a Sale*, publication №001 (internal EP007).

## 0. Inputs (verified 2026-09-23)

| Input | Path | Check |
|---|---|---|
| Episode master | `~/Movies/OE/EP007-masters/EP007_R81_upload_1080p24.mp4` | 1920x1080, 24 fps, 27,190 frames, sha256 `3925de31…01f96`, 1.13 GB |
| Description | `content/youtube_description.txt` | From `youtube-longform.md`, verbatim. `{{BLUEPRINT_URL}}` (display text now says Operator Canvas; launch.py also accepts `{{CANVAS_URL}}`) is replaced by launch.py with `https://theoperatoreconomy.com/episodes/exit-readiness-prep`, which redirects to the Operator Canvas page |
| Tags | `content/youtube_tags.txt` | 13 tags, 309 chars (limit 500) |
| Shorts copy | `content/shorts_briefs.json` | Titles, descriptions (AI disclosure last line), pinned comments; `[long-form link]` gets filled by launch.py. `shorts_contract.py --mode derived`: PASS |
| Shorts video | `shorts/short-01.mp4` … `short-04.mp4` | Symlinks to the V8 manifest renders; all four sha256 match `PRODUCTION-MANIFEST-V8.json` |
| Thumbnail | `launch/thumbnail.jpg` | 3840x2160, 1.2 MB (API limit 2 MB), sha256 `2fa00e12…3643` |
| Captions | `blueprint-cinema/episodes/EP007-exit-readiness-prep/edit/handoff/r81-cut-never-sold/finishing/ep007-r81-captions-en.srt` | 363 cues, ends 00:18:52,867, sha256 `334cb0ea…ea04` |
| Operator Canvas PDF | `Operator-Canvas-001.pdf` | 11 pages, Boundary Ledger 2.0, from `render_canvas.py` (rendered from the locked `operator-canvas.md`, source sha256 `3376437f…158f`). Already copied to `site/public/blueprints/exit-readiness-prep.pdf`. The old worksheet PDF `Operator-Blueprint-001.pdf` moved to `_to_delete/ep007-renumber-2026-09-23/` |
| OAuth | `studio/.secrets/token.json` | Scopes include `youtube.upload` and `youtube.force-ssl` (needed for captions and comments) |

Publish times (launch.py, America/New_York): episode Mon 10-05 11:00 ET (15:00Z); Shorts Tue-Fri
10-06 to 10-09 08:30 ET (12:30Z) in file order 01, 02, 03, 04. No trailer this week (no
`trailer_brief.json`).

**Shorts order.** `youtube-shorts.md` suggests 02, 01, 04, 03. launch.py schedules by filename. To
use the suggested order, re-point the symlinks and reorder `shorts_briefs.json` to match *before*
`--go` (each brief's `file` must match its video, or launch.py stops).

## 1. Pre-flight (Friday 2026-10-02)

```bash
cd ~/GitHub/operator-economy/studio
# dry run must print 4 shorts from originate/exit-readiness-prep/shorts/ and rubric PASS
python launch.py exit-readiness-prep --monday 2026-10-05 \
  --title "The One-Person Business That Gets Companies Ready for a Sale" \
  --video ~/Movies/OE/EP007-masters/EP007_R81_upload_1080p24.mp4
# content-os gate (see "Blockers" below: currently fails script_missing)
~/GitHub/content-os/bin/doctor.sh --week 2026-10-05 --slug exit-readiness-prep --gate
```

## 2. Upload and schedule (the `--go` run)

```bash
cd ~/GitHub/operator-economy/studio
python launch.py exit-readiness-prep --monday 2026-10-05 \
  --title "The One-Person Business That Gets Companies Ready for a Sale" \
  --video ~/Movies/OE/EP007-masters/EP007_R81_upload_1080p24.mp4 --go
```

This uploads five videos as `private` with `publishAt`, sets `containsSyntheticMedia: true` on each,
bakes the episode URL into every Short description, and rewrites `launch/links.json` with
`dry_run: false`. It is idempotent: a re-run reuses URLs already in `links.json`.

Then immediately:

```bash
~/GitHub/content-os/bin/doctor.sh --release --slug exit-readiness-prep --public
```

## 3. Post-upload API steps launch.py does not do

Run from `studio/`. Uses the same token refresh as `upload_youtube.py`. IDs come from `links.json`.

```bash
cd ~/GitHub/operator-economy/studio
python - <<'EOF'
import json, re, sys, requests
from pathlib import Path
sys.path.insert(0, "scripts/originate")
from upload_youtube import access_token

EP = Path("originate/exit-readiness-prep")
L = json.loads((EP / "launch/links.json").read_text())
assert not L["dry_run"] and L["episode_url"].startswith("https://youtu.be/"), "run --go first"
vid = lambda u: re.search(r"youtu\.be/([\w-]{11})", u).group(1)
ep = vid(L["episode_url"])
H = {"Authorization": f"Bearer {access_token()}"}

# 3a. Thumbnail (50 units)
r = requests.post(f"https://www.googleapis.com/upload/youtube/v3/thumbnails/set?videoId={ep}",
                  headers={**H, "Content-Type": "image/jpeg"},
                  data=(EP / "launch/thumbnail.jpg").read_bytes(), timeout=120)
print("thumbnail", r.status_code, r.text[:200])

# 3b. Captions (400 units). Owner-authored English track, not auto-captions.
srt = Path("../blueprint-cinema/episodes/EP007-exit-readiness-prep/edit/handoff/"
           "r81-cut-never-sold/finishing/ep007-r81-captions-en.srt").read_bytes()
meta = {"snippet": {"videoId": ep, "language": "en", "name": "English", "isDraft": False}}
b = "oe-ep007-captions"
body = (f"--{b}\r\nContent-Type: application/json; charset=UTF-8\r\n\r\n{json.dumps(meta)}\r\n"
        f"--{b}\r\nContent-Type: application/octet-stream\r\n\r\n").encode() + srt + f"\r\n--{b}--\r\n".encode()
r = requests.post("https://www.googleapis.com/upload/youtube/v3/captions?uploadType=multipart&part=snippet",
                  headers={**H, "Content-Type": f"multipart/related; boundary={b}"}, data=body, timeout=120)
print("captions", r.status_code, r.text[:200])
EOF
```

**Pinned comments.** The Data API can post a comment (`commentThreads.insert`, 50 units) but has
no pin endpoint, and comments on a still-private scheduled video may be rejected. So post and pin
in Studio once each video is live:

- Episode (Mon 11:00 ET): text from `content/youtube-longform.md` → "Pinned comment", with
  `{{BLUEPRINT_URL}}` rendered as `links.json` → `blueprint_url` (same value as `canvas_url`).
- Each Short (Tue-Fri 08:30 ET): `links.json` → `shorts[n].pinned_comment` (URL already filled).

Optional API post once live (then pin by hand):

```bash
python - <<'EOF'
import json, re, sys, requests
sys.path.insert(0, "scripts/originate"); from upload_youtube import access_token
L = json.load(open("originate/exit-readiness-prep/launch/links.json"))
H = {"Authorization": f"Bearer {access_token()}"}
def post(url, text):
    v = re.search(r"youtu\.be/([\w-]{11})", url).group(1)
    r = requests.post("https://www.googleapis.com/youtube/v3/commentThreads?part=snippet", headers=H,
        json={"snippet": {"videoId": v, "topLevelComment": {"snippet": {"textOriginal": text}}}})
    print(v, r.status_code, r.text[:160])
for s in L["shorts"]:   # run each day, only for the Short that just went live
    pass                # post(s["url"], s["pinned_comment"])
EOF
```

**Playlists** (`playlistItems.insert`, 50 units each). Find the IDs first (1 unit):

```bash
python - <<'EOF'
import sys, requests
sys.path.insert(0, "scripts/originate"); from upload_youtube import access_token
r = requests.get("https://www.googleapis.com/youtube/v3/playlists?part=snippet&mine=true&maxResults=50",
                 headers={"Authorization": f"Bearer {access_token()}"})
for p in r.json().get("items", []): print(p["id"], p["snippet"]["title"])
EOF
```

Then add the episode to the episodes playlist (and Shorts to a Shorts playlist if one exists):
`POST https://www.googleapis.com/youtube/v3/playlistItems?part=snippet` with
`{"snippet": {"playlistId": "<id>", "resourceId": {"kind": "youtube#video", "videoId": "<id>"}}}`.

## 4. YouTube API quota (default 10,000 units/day)

| Call | Units | Count | Total |
|---|---:|---:|---:|
| `videos.insert` (episode + 4 Shorts) | 1,600 | 5 | 8,000 |
| `thumbnails.set` | 50 | 1 | 50 |
| `captions.insert` | 400 | 1 | 400 |
| `playlists.list` | 1 | 1 | 1 |
| `playlistItems.insert` | 50 | 1 to 5 | 50 to 250 |
| `commentThreads.insert` (optional, after live) | 50 | 5 | 250 |
| **Day-of `--go` + thumbnail + captions + playlists** | | | **about 8,450 to 8,700** |

One failed upload retry (another 1,600) would exceed the daily cap. If `--go` fails partway,
re-run the next day (Pacific midnight reset); launch.py reuses what already uploaded. Comments
fall on later days anyway.

## 5. Manual YouTube Studio steps

- [ ] Confirm **Altered or synthetic content = Yes** on the episode and all four Shorts (the API
  sets `containsSyntheticMedia`; confirm the checkbox shows it). Narration is an AI voice clone of
  the host; presenter and all people are AI-generated.
- [ ] Confirm thumbnail and English captions took (step 3); chapters render from the description.
- [ ] **End screen** (last 5-20 s, episode ends 18:52.9): Subscribe + one live episode only. Do not
  tease an unreleased episode.
- [ ] Audience: not made for kids (set by the API; confirm).
- [ ] Shorts **Related video** = the EP007 long-form, set from `links.json` once the episode is live
  (backfill Monday if the Shorts were scheduled earlier).
- [ ] Pin the comments (section 3) as each video goes live.

## 6. Site page (theoperatoreconomy.com/episodes/exit-readiness-prep)

`/episodes/<slug>` redirects to `/businesses/<slug>` only if the slug is in
`site/app/lib/operations.ts`. `publish.py` only flips `site/data/episodes.json`; it does not create
the page. The page entry needs the YouTube URL, so it can only be completed after `--go`.

Prepared, not applied: `launch/site-ep007.patch` (operations entry, worksheet copy on the generic
business page and library row, homepage feature pinned to EP006 because its illustration and copy
are hand-built for hotels, and an `upcoming` registry entry in `episodes.json`). After `--go`:

```bash
cd ~/GitHub/operator-economy
git apply studio/originate/exit-readiness-prep/launch/site-ep007.patch
URL=$(python3 -c "import json;print(json.load(open('studio/originate/exit-readiness-prep/launch/links.json'))['episode_url'])")
sed -i '' "s|'{{EPISODE_URL}}'|'$URL'|" site/app/lib/operations.ts
# Operator Canvas PDF is already at site/public/blueprints/exit-readiness-prep.pdf (2026-09-23).
cd site && npm ci && npm run build        # not yet build-verified: site has no node_modules locally
```

Deploy so the page is live by Mon 11:00 ET (the description's Operator Canvas link 404s until then), then
at hour one: `python scripts/originate/publish.py exit-readiness-prep --date 2026-10` (from `studio/`).

## Blockers and open items

1. `content-os/bin/release_audit.py --slug exit-readiness-prep` is `BLOCKED_RELEASE`: it hard-fails
   `script_missing` (EP007 is a V2 episode with no `script.json`) and there is no `release.json`
   (needs `publication_number: 7`). The content-os gate needs a V2 path or a waiver before `--go`.
2. The description's AI line says "the presenter footage is AI-generated"; the thumbnail and the
   episode's cast are also AI-generated people. The Studio checkbox covers it, but the owner may want
   the description line widened. Not changed (approved copy).
3. The Operator Canvas PDF transcribes the locked Canvas. It omits the internal coverage map, E3
   check and lock record, and withholds three figures that `facts.md` DO NOT STATE forbids (state
   count, net-worth percentage, the CLM-007 multiples), each marked in the PDF. The derived
   worksheet `content/blueprint.md` is no longer the public PDF.
4. `remotion/out/short-0*.mp4` are EP006 renders. launch.py was changed to prefer
   `originate/<slug>/shorts/`; before that change `--go` would have uploaded EP006's Shorts.
