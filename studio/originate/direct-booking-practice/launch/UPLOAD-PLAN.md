# EP009 upload plan: schedule for Monday 2026-10-19

Prepared 2026-10-12. **Nothing has been uploaded or scheduled.** Every URL comes from
`launch/links.json` after `--go` writes it. Do not type a video ID by hand.

Episode: *The One-Person Business That Gets Small Hotels Booking Direct*, public No. 002
(internal EP009). Publication slug `direct-booking-practice`. Never `direct-booking-recovery`:
that is EP006, and its `links.json` holds live IDs.

Publish times (launch.py, America/New_York): episode Mon 10-19 11:00 ET (15:00Z); Shorts
Tue 10-20 to Fri 10-23 08:30 ET (12:30Z), in file order 01, 02, 03, 04. No trailer.

## 0. Inputs

| Input | Path | State |
|---|---|---|
| Episode master | `launch/ep009-master-720p.mp4` (Mac only, gitignored) | Accepted r11 cut, 29,323 frames at 24 fps, -14 LUFS |
| Upload file | `ep009-final.mp4` | Made by `finish_release.py --write`: 1920x1080 lanczos upscale, audio copied |
| Resolution | | Path 1 of `PARKED-2026-10-09.md`: upscale. A full 1080p rebuild would re-open a cut accepted on 10-09 for no new detail in the 17 percent that is generated plates |
| Description | `content/youtube_description.txt` | Chapters from the r11 timemap. `{{CANVAS_URL}}` filled by launch.py |
| Tags | `content/youtube_tags.txt` | 12 tags |
| Shorts copy | `content/shorts_briefs.json` | Titles, descriptions, pinned comments. Spoken fields copied from the owner-locked `STANDALONE-SCRIPTS-V1.json`. `shorts_contract.py --mode derived`: PASS |
| Shorts video | `shorts/short-01.mp4` to `short-04.mp4` | Made by `finish_release.py --write` from the newest render in each `shorts-hyperframes/NN-*/renders/`, loudnorm -14 LUFS |
| Thumbnail | `launch/thumbnail.jpg` | 3840x2160, 1.85 MB (API limit 2 MB) |
| Captions | `content/direct-booking-practice.srt` | 348 cues, ends 00:20:21,887. Built from `r3/word-transcript-r3.json`, the forced-aligned words of the master the r11 cut plays. Script wording, not ASR |
| Operator Canvas PDF | `Operator-Canvas-002.pdf` | From `render_canvas.py` and the locked `operator-canvas.md` |
| OAuth | `studio/.secrets/token.json` | Same token as EP007 |

## 1. Finish (any day before Friday 10-16)

```bash
cd ~/GitHub/operator-economy/studio
python originate/direct-booking-practice/finish_release.py          # check: must print OK
python originate/direct-booking-practice/finish_release.py --write  # encode, normalise, stage
python launch.py direct-booking-practice --monday 2026-10-19 \
  --title "The One-Person Business That Gets Small Hotels Booking Direct"   # dry run
```

The dry run must list four Shorts from `originate/direct-booking-practice/shorts/` and the
Canvas PDF. It writes a placeholder `links.json` with `dry_run: true`.

## 2. Gate 3: episode library review (you, about 20 minutes)

`studio/config/blueprint.json` has `autonomy.training_mode: true`, so this is required. Watch
`ep009-final.mp4` and the four `shorts/short-*.mp4` in VLC, read the description and Shorts copy
above, look at the thumbnail at 168 px wide. Then:

```bash
cd ~/GitHub/operator-economy
git add studio/originate/direct-booking-practice && git commit -m "EP009 Gate 3 passed"
```

## 3. Upload and schedule

```bash
cd ~/GitHub/operator-economy/studio
python launch.py direct-booking-practice --monday 2026-10-19 \
  --title "The One-Person Business That Gets Small Hotels Booking Direct" --go
```

Uploads five videos as `private` with `publishAt`, `containsSyntheticMedia: true` on each, bakes
the episode URL into every Short, and rewrites `launch/links.json` with `dry_run: false`.
Idempotent: a re-run reuses what already uploaded. About 8,000 of the 10,000 daily API units.

## 4. Thumbnail and captions (same day, about 450 units)

```bash
cd ~/GitHub/operator-economy/studio
python - <<'EOF'
import json, re, sys, requests
from pathlib import Path
sys.path.insert(0, "scripts/originate")
from upload_youtube import access_token

EP = Path("originate/direct-booking-practice")
L = json.loads((EP / "launch/links.json").read_text())
assert not L["dry_run"] and L["episode_url"].startswith("https://youtu.be/"), "run --go first"
ep = re.search(r"youtu\.be/([\w-]{11})", L["episode_url"]).group(1)
H = {"Authorization": f"Bearer {access_token()}"}

r = requests.post(f"https://www.googleapis.com/upload/youtube/v3/thumbnails/set?videoId={ep}",
                  headers={**H, "Content-Type": "image/jpeg"},
                  data=(EP / "launch/thumbnail.jpg").read_bytes(), timeout=120)
print("thumbnail", r.status_code, r.text[:200])

srt = (EP / "content/direct-booking-practice.srt").read_bytes()
meta = {"snippet": {"videoId": ep, "language": "en", "name": "English", "isDraft": False}}
b = "oe-ep009-captions"
body = (f"--{b}\r\nContent-Type: application/json; charset=UTF-8\r\n\r\n{json.dumps(meta)}\r\n"
        f"--{b}\r\nContent-Type: application/octet-stream\r\n\r\n").encode() + srt + f"\r\n--{b}--\r\n".encode()
r = requests.post("https://www.googleapis.com/upload/youtube/v3/captions?uploadType=multipart&part=snippet",
                  headers={**H, "Content-Type": f"multipart/related; boundary={b}"}, data=body, timeout=120)
print("captions", r.status_code, r.text[:200])
EOF
git -C .. add studio/originate/direct-booking-practice/launch && git -C .. commit -m "EP009 scheduled: links.json from the upload"
~/GitHub/content-os/bin/doctor.sh --release --slug direct-booking-practice --public
```

## 5. YouTube Studio (by hand)

- [ ] Altered or synthetic content = Yes on the episode and all four Shorts. Confirm the box shows it.
- [ ] Thumbnail and English captions took. Chapters show on the progress bar.
- [ ] End screen, last 5 to 20 seconds (episode ends 20:21.8): Subscribe + No. 001 only.
- [ ] Add the episode to the Episodes playlist, the Shorts to the Shorts playlist.
- [ ] Each Short's Related video = this episode.
- [ ] As each video goes live, post and pin its comment: Shorts from `links.json` →
  `shorts[n].pinned_comment` (URL already filled).

## 6. After the upload, not in this plan

- Site page for `/episodes/direct-booking-practice` and the Canvas PDF at
  `site/public/blueprints/direct-booking-practice.pdf`. Needs the episode URL, so after step 3.
- LinkedIn: `content-os/bin/sync-episode.py` renders the `oe-launch/` copy from `links.json`
  into the week of 2026-10-19.

## Known gap

`content-os/bin/release_audit.py` fails V2 episodes with `script_missing` (no `script.json`).
EP007 shipped on an owner exception for the same reason. EP009 needs the same exception, or a
V2 path in the audit.
