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
import json, shutil, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SHORTS = HERE.parents[2] / "studio/originate/direct-booking-practice/shorts-hyperframes"
FRAME = {"open": ("01-presenter-open.html", "f01-presenter-open"),
         "close": ("06-presenter-close.html", "f06-presenter-close")}

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
VIDEO = ('        <video class="take" src="assets/video/{f}" muted\n'
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
        shutil.copy2(src, out / name)
        vids += VIDEO.format(f=name, start=round(start, 6), dur=r["react1"]["duration_s"])
        start += r["react1"]["duration_s"]
    fname, cid = FRAME[span]
    note = (f"Presenter {span}. {len(recs)} accepted take(s), "
            + ", ".join(f"{r['take']} {r['react1']['duration_s']}s sha256 {r['react1']['sha256'][:8]}" for r in recs)
            + f". Total {round(start, 6)}s against the span the root allots. "
              "Muted: the root plays the accepted narration. Scaled from 720x1280 by object-fit cover.")
    (SHORTS / slug / "compositions" / fname).write_text(
        HTML.format(comment=note, cid=cid, videos=vids))
    print(f"{slug}/{fname}: {len(recs)} take(s), {round(start, 6)}s")
