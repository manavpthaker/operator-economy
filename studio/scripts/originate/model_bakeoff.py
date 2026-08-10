#!/usr/bin/env python3
"""
Originate: score image models against the thumbnail-scene rubric.

Why this exists (2026-08-10). Four prompt revisions failed in four different
directions before it turned out the model was the constraint, not the wording.
Picking one by vibe is how that happened, so this runs a fixed prompt across
every candidate and lays the results out against a rubric.

The rubric scores what actually broke real thumbnails, in weight order:

  1. Photographic realism    30  shot, not rendered. Skin texture, available
                                 light, imperfection. The "looks AI" failure.
  2. Composition control     25  did it honour subject-right, plain-left,
                                 waist-up? Determines whether text has anywhere
                                 to sit without a rescue crop.
  3. Expression              20  mid-sentence, eye contact, animated. Not
                                 contemplative (reads sad), not beaming at a
                                 laptop (reads stock).
  4. Text artefacts          15  garbled lettering on clothing and signage. The
                                 clearest generated-image tell, and
                                 check_thumbnail.py is blind to it.
  5. Environment             10  real working clutter vs a generic set.

1, 3, 4 and 5 need eyes. Only legibility is machine-checkable, and that is what
check_thumbnail.py already covers, so it runs per candidate and is reported
alongside rather than folded into the score.

    model_bakeoff.py --out bakeoff.html [--n 1]

Writes a self-contained comparison page: every candidate at full size and at
120px browse width, with a scoring table to fill in.
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

REPO = Path(__file__).resolve().parents[3]

# Candidates. Params differ by family: some take aspect_ratio, some image_size.
# Unknown ids fail loudly and get skipped rather than aborting the run.
CANDIDATES = [
    ("imagen4",        "fal-ai/imagen4/preview",                      {"aspect_ratio": "16:9"}),
    ("imagen4-ultra",  "fal-ai/imagen4/preview/ultra",                {"aspect_ratio": "16:9"}),
    ("seedream3",      "fal-ai/bytedance/seedream/v3/text-to-image",  {"image_size": {"width": 1280, "height": 720}}),
    ("seedream4",      "fal-ai/bytedance/seedream/v4/text-to-image",  {"image_size": {"width": 1280, "height": 720}}),
    ("flux-ultra",     "fal-ai/flux-pro/v1.1-ultra",                  {"aspect_ratio": "16:9"}),
    ("flux-krea",      "fal-ai/flux/krea",                            {"image_size": "landscape_16_9"}),
    ("ideogram3",      "fal-ai/ideogram/v3",                          {"image_size": {"width": 1280, "height": 720}}),
    ("recraft3",       "fal-ai/recraft-v3",                           {"image_size": {"width": 1280, "height": 720},
                                                                       "style": "realistic_image/natural_light"}),
    ("qwen-image",     "fal-ai/qwen-image",                           {"image_size": "landscape_16_9"}),
    ("hidream",        "fal-ai/hidream-i1-full",                      {"image_size": "landscape_16_9"}),
]

PROMPT = (
    "Candid editorial photograph for a business magazine, available light, shot on a "
    "50mm lens. A woman in her thirties who builds automation systems for small "
    "businesses, standing behind the front counter of a client's auto repair shop, "
    "mid-sentence explaining how the system works, laptop open beside her, parts "
    "shelves and workshop behind her. Waist-up framing, subject toward the RIGHT of "
    "the frame, caught mid-sentence addressing the camera directly, one hand raised "
    "mid-gesture, animated and confident without grinning, direct eye contact with "
    "the lens. Bright natural daylight, true-to-life colour, realistic skin texture "
    "with visible pores and fine lines, real working clutter behind her. On the LEFT "
    "of the frame the background continues as a plain shadowed wall with little "
    "detail. No text, no lettering, no numbers, no logos, no signage. Photographed, "
    "not rendered: no studio lighting, no rim light, no heavy bokeh, no glossy "
    "retouching, no stock-photo posing."
)

CRITERIA = [
    ("Photographic realism", 30, "Shot, not rendered. Skin texture, available light, imperfection."),
    ("Composition control", 25, "Subject right, plain left, waist-up. Does text have anywhere to sit?"),
    ("Expression", 20, "Mid-sentence, eye contact, animated. Not sad, not beaming."),
    ("Text artefacts", 15, "Garbled lettering on clothing or signage. Full marks = none."),
    ("Environment", 10, "Real working clutter vs a generic set."),
]


def fal_key() -> str:
    for line in (REPO / ".env").read_text().splitlines():
        if line.startswith("FAL_KEY="):
            return line.split("=", 1)[1].strip()
    raise SystemExit("no FAL_KEY in .env")


def run_model(model: str, extra: dict, n: int, key: str) -> list[str]:
    body = json.dumps({"prompt": PROMPT, "num_images": n, **extra}).encode()
    req = urllib.request.Request(
        f"https://fal.run/{model}", data=body,
        headers={"Authorization": f"Key {key}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=300) as r:
        return [im["url"] for im in json.load(r).get("images", [])]


def fit(url: str, dest: Path) -> None:
    with tempfile.TemporaryDirectory() as td:
        raw = Path(td) / "raw"
        urllib.request.urlretrieve(url, raw)
        subprocess.run(
            ["ffmpeg", "-y", "-v", "error", "-i", str(raw), "-vf",
             "scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720",
             str(dest)], check=True)


def uri(p: Path) -> str:
    with tempfile.TemporaryDirectory() as td:
        j = Path(td) / "o.jpg"
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(p),
                        "-vf", "scale=760:-2", "-q:v", "4", str(j)], check=True)
        return "data:image/jpeg;base64," + base64.b64encode(j.read_bytes()).decode()


def mech_check(p: Path) -> str:
    r = subprocess.run(
        [sys.executable, str(REPO / "studio/scripts/originate/check_thumbnail.py"),
         str(p), "--json"], capture_output=True, text=True)
    try:
        d = json.loads(r.stdout)
        return "pass" if d.get("pass") else "; ".join(d.get("fails", []))[:80]
    except json.JSONDecodeError:
        return "check failed"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--n", type=int, default=1)
    ap.add_argument("--workdir", type=Path,
                    default=Path(tempfile.gettempdir()) / "oe-bakeoff")
    a = ap.parse_args()
    a.workdir.mkdir(parents=True, exist_ok=True)
    key = fal_key()

    results, skipped = [], []
    for name, model, extra in CANDIDATES:
        try:
            urls = run_model(model, extra, a.n, key)
            if not urls:
                raise RuntimeError("no images returned")
            dest = a.workdir / f"{name}.png"
            fit(urls[0], dest)
            results.append((name, model, dest, mech_check(dest)))
            print(f"  ok    {name:14s} {model}")
        except urllib.error.HTTPError as e:
            skipped.append((name, model, f"HTTP {e.code}"))
            print(f"  skip  {name:14s} HTTP {e.code}")
        except Exception as e:  # noqa: BLE001 - a bad candidate must not abort the run
            skipped.append((name, model, type(e).__name__))
            print(f"  skip  {name:14s} {type(e).__name__}")

    if not results:
        raise SystemExit("every candidate failed")

    cards = "\n".join(f"""<section class="cand">
  <div class="chead"><h2>{html.escape(n)}</h2><code>{html.escape(m)}</code>
    <span class="mech {'ok' if c == 'pass' else 'bad'}">{html.escape(c)}</span></div>
  <div class="shots">
    <figure class="big"><img src="{uri(p)}" alt="{html.escape(n)}"><figcaption>full size</figcaption></figure>
    <figure class="sm"><img src="{uri(p)}" alt=""><figcaption>120px browse</figcaption></figure>
  </div>
  <table class="score"><thead><tr><th>Criterion</th><th>Max</th><th>Score</th><th>Note</th></tr></thead>
  <tbody>{''.join(f'<tr><td>{html.escape(t)}</td><td>{w}</td><td class="fill"></td><td class="hint">{html.escape(d)}</td></tr>' for t, w, d in CRITERIA)}
  <tr class="tot"><td>Total</td><td>100</td><td class="fill"></td><td></td></tr></tbody></table>
</section>""" for n, m, p, c in results)

    skip_html = ("".join(f"<li><code>{html.escape(m)}</code> — {html.escape(r)}</li>"
                         for _, m, r in skipped) or "<li>none</li>")

    a.out.write_text(PAGE.format(cards=cards, skipped=skip_html,
                                 prompt=html.escape(PROMPT),
                                 n=len(results)), encoding="utf-8")
    print(f"\nwrote {a.out} ({a.out.stat().st_size/1024:.0f} KB), {len(results)} candidates")
    return 0


PAGE = """<title>Image model bake-off — thumbnail scenes</title>
<style>
:root {{
  --ink:#12263F; --ink-2:#41546B; --ink-3:#7A889A;
  --ground:#F7F4EC; --panel:#FFFFFF; --line:#DED6C4;
  --gold:#9A7B2E; --brick:#9B3E2E; --good:#2F6B4F;
  --mono:ui-monospace,SFMono-Regular,Menlo,monospace;
  --ui:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif;
}}
@media (prefers-color-scheme:dark) {{ :root:not([data-theme="light"]) {{
  --ink:#ECE4D4; --ink-2:#B3A992; --ink-3:#8A8272;
  --ground:#141A24; --panel:#1B222E; --line:#2E3846;
  --gold:#C8A24F; --brick:#C4614C; --good:#7FBF9B;
}} }}
:root[data-theme="dark"] {{
  --ink:#ECE4D4; --ink-2:#B3A992; --ink-3:#8A8272;
  --ground:#141A24; --panel:#1B222E; --line:#2E3846;
  --gold:#C8A24F; --brick:#C4614C; --good:#7FBF9B;
}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--ground);color:var(--ink);font-family:var(--ui);line-height:1.55}}
.wrap{{max-width:1100px;margin:0 auto;padding:40px 24px 90px}}
h1{{font-size:30px;margin:0 0 6px;letter-spacing:-.015em}}
.sub{{color:var(--ink-2);max-width:66ch;margin:0 0 8px}}
details{{margin:18px 0 0;border:1px solid var(--line);border-radius:2px;background:var(--panel)}}
summary{{cursor:pointer;padding:11px 14px;font:600 11px/1 var(--mono);letter-spacing:.12em;
  text-transform:uppercase;color:var(--ink-3)}}
details p{{margin:0;padding:0 14px 14px;color:var(--ink-2);font-size:14px}}
.cand{{margin-top:40px;border-top:2px solid var(--ink);padding-top:16px}}
.chead{{display:flex;flex-wrap:wrap;gap:10px;align-items:baseline}}
.chead h2{{font-size:20px;margin:0;letter-spacing:-.01em}}
.chead code{{font:400 12px/1 var(--mono);color:var(--ink-3)}}
.mech{{margin-left:auto;font:600 10px/1 var(--mono);letter-spacing:.1em;text-transform:uppercase;
  padding:5px 8px;border-radius:2px}}
.mech.ok{{color:var(--good);border:1px solid var(--good)}}
.mech.bad{{color:var(--brick);border:1px solid var(--brick)}}
.shots{{display:flex;gap:22px;align-items:flex-start;margin:14px 0 6px;flex-wrap:wrap}}
.shots img{{display:block;border-radius:6px;background:#000}}
.big img{{width:min(560px,100%);height:auto}}
.sm img{{width:120px;height:auto}}
figure{{margin:0}}
figcaption{{font:600 10px/1.6 var(--mono);letter-spacing:.1em;text-transform:uppercase;
  color:var(--ink-3);margin-top:6px}}
table.score{{border-collapse:collapse;width:100%;margin-top:10px;font-size:14px}}
.score th{{text-align:left;font:600 10px/1 var(--mono);letter-spacing:.1em;text-transform:uppercase;
  color:var(--ink-3);padding:8px 10px;border-bottom:1px solid var(--line)}}
.score td{{padding:8px 10px;border-bottom:1px solid var(--line);vertical-align:top}}
.score td:nth-child(2),.score td:nth-child(3){{font-variant-numeric:tabular-nums;width:64px}}
.fill{{background:var(--panel)}}
.hint{{color:var(--ink-3);font-size:13px}}
.tot td{{font-weight:700;border-bottom:2px solid var(--ink)}}
.skips{{margin-top:44px;border-top:1px solid var(--line);padding-top:16px;color:var(--ink-2)}}
.skips h2{{font:600 11px/1 var(--mono);letter-spacing:.12em;text-transform:uppercase;color:var(--gold)}}
.skips ul{{padding-left:20px}} .skips code{{font-family:var(--mono);font-size:12.5px}}
</style>
<div class="wrap">
<h1>Image model bake-off</h1>
<p class="sub">{n} candidates, one identical prompt, scored against the failures that actually
broke real thumbnails. Every image below is the model's first return — no cherry-picking,
no re-rolls.</p>
<details><summary>The prompt</summary><p>{prompt}</p></details>
{cards}
<div class="skips"><h2>Did not run</h2><ul>{skipped}</ul></div>
</div>
"""


if __name__ == "__main__":
    sys.exit(main())
