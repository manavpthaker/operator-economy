#!/usr/bin/env python3
"""Replace a Short's presenter placeholder with an accepted take.

usage: mount_presenter.py <take-id> [<take-id> ...]

A take-id is 01-open, 01-close, 02-open, ..., 04-close-a, 04-close-b. The two
04-close ids mount into one composition, back to back, in that order.

What it does, per composition:
 - copies each take's react-1 output into the Short's assets/video/
 - rewrites compositions/01-presenter-open.html or 06-presenter-close.html as a
   full-frame muted <video>

Muted on purpose. The react-1 output carries the narration slice, but the root
composition already plays the whole accepted narration as one continuous track;
the picture is cut to that audio, not the other way round. Playing both would
double the voice.

The take is 720x1280 inside a 1080x1920 frame, so it is scaled with object-fit
cover. That upscale is the cost of the owner's 720p ruling, not a defect.

Only runs for a take whose TAKE.json records react1 done and owner_accepted true.
"""
import json, re, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SHORTS = HERE.parents[2] / "studio/originate/direct-booking-practice/shorts-hyperframes"
FRAME = {"open": "01-presenter-open.html", "close": "06-presenter-close.html"}


def probe_av(path):
    """Frame count and duration of the video stream, to prove the conform changed neither."""
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0",
        "-show_entries", "stream=nb_frames,r_frame_rate,width,height", "-of", "json",
        str(path)], capture_output=True, text=True, check=True).stdout
    st = json.loads(out)["streams"][0]
    return st["nb_frames"], st["r_frame_rate"], st["width"], st["height"]


def mount_point(slug, fname):
    """Read the composition id and allotted duration the Short's root gives this frame.

    The ids are per-Short (f01/f06 in Short 01, f021/f026 in Short 02, ...), so they
    are read from the root rather than assumed. Registering under the wrong id leaves
    the frame with no timeline the runtime will seek.
    """
    root = (SHORTS / slug / "index.html").read_text()
    block = next(b for b in re.findall(r"<div\b[^>]*?>", root, re.S)
                 if f'compositions/{fname}' in b)
    cid = re.search(r'data-composition-id="([^"]+)"', block).group(1)
    dur = float(re.search(r'data-duration="([^"]+)"', block).group(1))
    return cid, dur

HTML = """<!doctype html>
<html>
  <head>
    <meta charset="UTF-8" />
    <!-- {comment} -->
  </head>
  <body>
    <template>
      <style>
        #root {{ position: absolute; inset: 0; background: #173530; overflow: hidden; }}
        .take {{ position: absolute; inset: 0; width: 1080px; height: 1920px;
                 object-fit: cover; object-position: center; }}
      </style>
      <div id="root" data-composition-id="{cid}" data-width="1080" data-height="1920">
{videos}      </div>
      <script>
        (() => {{
          // No motion of its own. The performance is the motion; a tween here would
          // move the frame the performance was generated into.
          const tl = gsap.timeline({{ paused: true }});
          window.__timelines["{cid}"] = tl;
        }})();
      </script>
    </template>
  </body>
</html>
"""
# The id is required, not cosmetic: the renderer discovers media elements by id and a
# <video> without one renders frozen on its first frame.
VIDEO = ('        <video id="{vid}" class="take" src="assets/video/{f}" muted\n'
         '               data-start="{start}" data-duration="{dur}" data-track-index="1"></video>\n')

groups = {}
for tid in sys.argv[1:]:
    rec = json.load(open(HERE / "takes" / tid / "TAKE.json"))
    if rec.get("react1", {}).get("status") != "done":
        sys.exit(f"{tid}: react-1 is not done; nothing to mount")
    if not rec.get("owner_accepted"):
        sys.exit(f"{tid}: not owner-accepted. Each take is its own view.")
    groups.setdefault((rec["short"], rec["span"].split("-")[0]), []).append(rec)

for (short, span), recs in groups.items():
    recs.sort(key=lambda r: r["span"])
    slug = next(d.name for d in SHORTS.iterdir() if d.name.startswith(short + "-"))
    out = SHORTS / slug / "assets/video"
    out.mkdir(parents=True, exist_ok=True)
    vids, start = "", 0.0
    for r in recs:
        src = HERE.parents[2] / r["react1"]["path"]
        name = f"presenter-{r['span']}.mp4"
        # Conform, don't copy. react-1 returns ~5-6s between keyframes, which the
        # renderer seeks against frame by frame: it warns this freezes frames. One
        # keyframe per second of picture fixes that. -r 24 matches the source rate,
        # so no frame is added, dropped or retimed. -an because the root plays the
        # accepted narration and the element is muted anyway.
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(src), "-an",
                        "-c:v", "libx264", "-profile:v", "high", "-pix_fmt", "yuv420p",
                        "-r", "24", "-g", "24", "-keyint_min", "24", "-crf", "16",
                        "-preset", "slow", "-movflags", "+faststart", str(out / name)],
                       check=True)
        a, b = probe_av(src), probe_av(out / name)
        assert a == b, f"{name}: conform changed the picture {a} -> {b}"
        vids += VIDEO.format(vid=f"presenter-{r['span']}", f=name,
                             start=round(start, 6), dur=r["react1"]["duration_s"])
        start += r["react1"]["duration_s"]
    fname = FRAME[span]
    cid, allotted = mount_point(slug, fname)
    note = (f"Presenter {span}. {len(recs)} accepted take(s), "
            + ", ".join(f"{r['take']} {r['react1']['duration_s']}s sha256 {r['react1']['sha256'][:8]}" for r in recs)
            + f". Total {round(start, 6)}s against the {allotted}s the root allots. "
              "Muted: the root plays the accepted narration. Scaled from 720x1280 by object-fit cover.")
    (SHORTS / slug / "compositions" / fname).write_text(
        HTML.format(comment=note, cid=cid, videos=vids))
    fit = abs(start - allotted) < 0.021  # half a frame at 24fps
    print(f"{slug}/{fname}: {cid}, {len(recs)} take(s), {round(start, 6)}s "
          f"against {allotted}s allotted — {'fits' if fit else 'MISMATCH'}")
