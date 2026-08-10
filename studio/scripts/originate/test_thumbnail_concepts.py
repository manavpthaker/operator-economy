#!/usr/bin/env python3
"""
Originate: render every distilled concept across every candidate model.

Pairs with derive_thumbnail_prompt.py. That step turns the episode script into
N concepts spanning different composition archetypes; this one generates each
concept on each model, composites the overlay through Remotion's `photo`
variant, and lays the grid out for a human read.

The grid is the point. A concept can be strong and the model wrong for it, or
the reverse, and looking at one image at a time cannot separate those. Reading
across a row shows how much of the result is the concept; reading down a column
shows how much is the model.

    test_thumbnail_concepts.py <slug> --out grid.html [--models a,b]

Requires render_data/thumbnail_prompts.json (derive_thumbnail_prompt.py),
FAL_KEY in .env, ffmpeg, and remotion installed in studio/remotion.
"""

from __future__ import annotations

import argparse
import base64
import html
import json
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]      # studio/
REPO = ROOT.parent
THUMBS = ROOT / "remotion" / "public" / "thumbs"
OUT = ROOT / "remotion" / "out" / "concepts"

MODELS = {
    "seedream4":     ("fal-ai/bytedance/seedream/v4/text-to-image",
                      {"image_size": {"width": 1280, "height": 720}}),
    "imagen4-ultra": ("fal-ai/imagen4/preview/ultra", {"aspect_ratio": "16:9"}),
    "seedream3":     ("fal-ai/bytedance/seedream/v3/text-to-image",
                      {"image_size": {"width": 1280, "height": 720}}),
    "flux-ultra":    ("fal-ai/flux-pro/v1.1-ultra", {"aspect_ratio": "16:9"}),
}

NEGATIVE = ("text, lettering, writing, words, letters, numbers, logos, brand names, "
            "signage, signs, posters, labels, stickers, banners, printed t-shirt, "
            "embroidered logo, watermark, captions, license plate")

PREAMBLE = ("Candid editorial photograph for a business magazine, available light, "
            "shot on a 50mm lens. ")
TAIL = (" Bright natural daylight, clean true-to-life colour, realistic skin texture "
        "with visible pores and fine lines. Plain unbranded clothing with no printing, "
        "bare walls, unlabelled boxes. Photographed, not rendered: no studio lighting, "
        "no rim light, no heavy bokeh, no glossy retouching.")


def fal_key() -> str:
    for line in (REPO / ".env").read_text().splitlines():
        if line.startswith("FAL_KEY="):
            return line.split("=", 1)[1].strip()
    raise SystemExit("no FAL_KEY in .env")


def generate(scene: str, model_key: str, key: str) -> str:
    model, size = MODELS[model_key]
    payload = {"prompt": PREAMBLE + scene.rstrip(".") + "." + TAIL,
               "num_images": 1, **size}
    if "seedream" in model:
        payload["negative_prompt"] = NEGATIVE
    req = urllib.request.Request(
        f"https://fal.run/{model}", data=json.dumps(payload).encode(),
        headers={"Authorization": f"Key {key}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=300) as r:
        return json.load(r)["images"][0]["url"]


def fit(url: str, dest: Path) -> None:
    with tempfile.TemporaryDirectory() as td:
        raw = Path(td) / "raw"
        urllib.request.urlretrieve(url, raw)
        dest.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(raw), "-vf",
                        "scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720",
                        str(dest)], check=True)


def composite(bg_rel: str, big: str, label: str, dest: Path) -> bool:
    props = {"variant": "photo", "bgImage": bg_rel, "big": big, "bigLabel": label,
             "small": "", "label": "", "kicker": "", "showMark": False,
             "textStyle": "block"}
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False,
                                     dir=ROOT / "remotion") as f:
        json.dump(props, f)
        pf = Path(f.name)
    try:
        dest.parent.mkdir(parents=True, exist_ok=True)
        r = subprocess.run(
            ["npx", "remotion", "still", "src/index.ts", "Thumbnail",
             str(dest), f"--props={pf.name}"],
            cwd=ROOT / "remotion", capture_output=True, text=True)
        return r.returncode == 0
    finally:
        pf.unlink(missing_ok=True)


def uri(p: Path, w: int = 620) -> str:
    with tempfile.TemporaryDirectory() as td:
        j = Path(td) / "o.jpg"
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(p), "-vf",
                        f"scale={w}:-2", "-q:v", "4", str(j)], check=True)
        return "data:image/jpeg;base64," + base64.b64encode(j.read_bytes()).decode()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("slug")
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--models", default="seedream4,imagen4-ultra")
    a = ap.parse_args()

    models = [m.strip() for m in a.models.split(",") if m.strip() in MODELS]
    if not models:
        raise SystemExit(f"no valid models; pick from {', '.join(MODELS)}")

    prompts = json.loads(
        (ROOT / "originate" / a.slug / "render_data" / "thumbnail_prompts.json").read_text())
    concepts = prompts["concepts"]
    key = fal_key()
    rows = []

    for i, c in enumerate(concepts, 1):
        cells = []
        for m in models:
            tag = f"{a.slug}-c{i}-{m}"
            try:
                fit(generate(c["scene"], m, key), THUMBS / f"{tag}.png")
                done = composite(f"thumbs/{tag}.png", c["overlay_big"],
                                 c["overlay_label"], OUT / f"{tag}.png")
                cells.append((m, OUT / f"{tag}.png" if done else None))
                print(f"  {'ok  ' if done else 'render FAILED'} c{i} {m}")
            except (urllib.error.HTTPError, OSError, KeyError) as e:
                cells.append((m, None))
                print(f"  fail c{i} {m}: {type(e).__name__}")
        rows.append((i, c, cells))

    body = "\n".join(f"""<section class="row">
  <div class="rhead">
    <h2>{i}. {html.escape(c['overlay_big'])} <span>{html.escape(c['overlay_label'])}</span></h2>
    <code>{html.escape(c['archetype'])}</code>
  </div>
  <p class="src">from the script: <em>{html.escape(c.get('from_script', ''))}</em></p>
  <div class="cells">{''.join(
      f'<figure>{f"<img src=chr34{uri(p)}chr34 alt=chr34chr34>" if p else "<div class=chr34missingchr34>failed</div>"}'
      f'<figcaption>{html.escape(m)}</figcaption></figure>' for m, p in cells)}</div>
</section>""".replace("chr34", '"') for i, c, cells in rows)

    a.out.write_text(PAGE.format(body=body, slug=html.escape(a.slug),
                                 n=len(concepts), models=html.escape(", ".join(models))),
                     encoding="utf-8")
    print(f"\nwrote {a.out} ({a.out.stat().st_size/1024:.0f} KB)")
    return 0


PAGE = """<title>{slug} — thumbnail concepts x models</title>
<style>
:root {{
  --ink:#12263F; --ink-2:#41546B; --ink-3:#7A889A; --ground:#F7F4EC;
  --panel:#FFF; --line:#DED6C4; --gold:#9A7B2E;
  --mono:ui-monospace,SFMono-Regular,Menlo,monospace;
  --ui:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif;
}}
@media (prefers-color-scheme:dark) {{ :root:not([data-theme="light"]) {{
  --ink:#ECE4D4; --ink-2:#B3A992; --ink-3:#8A8272; --ground:#141A24;
  --panel:#1B222E; --line:#2E3846; --gold:#C8A24F;
}} }}
:root[data-theme="dark"] {{
  --ink:#ECE4D4; --ink-2:#B3A992; --ink-3:#8A8272; --ground:#141A24;
  --panel:#1B222E; --line:#2E3846; --gold:#C8A24F;
}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--ground);color:var(--ink);font-family:var(--ui);line-height:1.55}}
.wrap{{max-width:1180px;margin:0 auto;padding:40px 24px 90px}}
h1{{font-size:29px;margin:0 0 6px;letter-spacing:-.015em}}
.sub{{color:var(--ink-2);max-width:68ch;margin:0}}
.row{{margin-top:42px;border-top:2px solid var(--ink);padding-top:14px}}
.rhead{{display:flex;gap:12px;align-items:baseline;flex-wrap:wrap}}
.rhead h2{{font-size:21px;margin:0;letter-spacing:-.01em}}
.rhead h2 span{{color:var(--ink-3);font-weight:500}}
.rhead code{{margin-left:auto;font:600 10px/1 var(--mono);letter-spacing:.12em;
  text-transform:uppercase;color:var(--gold);border:1px solid var(--line);padding:5px 8px}}
.src{{color:var(--ink-3);font-size:13.5px;margin:6px 0 14px;max-width:80ch}}
.cells{{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:18px}}
figure{{margin:0}}
figure img{{width:100%;height:auto;display:block;border-radius:6px;background:#000}}
.missing{{aspect-ratio:16/9;display:grid;place-items:center;border:1px dashed var(--line);
  color:var(--ink-3);font:600 11px/1 var(--mono);letter-spacing:.1em;text-transform:uppercase}}
figcaption{{font:600 10px/1.6 var(--mono);letter-spacing:.1em;text-transform:uppercase;
  color:var(--ink-3);margin-top:6px}}
</style>
<div class="wrap">
<h1>{slug}</h1>
<p class="sub">{n} concepts distilled from the episode script, each a different composition
archetype, rendered on {models}. Read across a row to see how much is the concept; read down a
column to see how much is the model. Every image is a first return.</p>
{body}
</div>
"""


if __name__ == "__main__":
    sys.exit(main())
