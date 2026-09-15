"""Week 2 full-07: full-06 plus the v8 video standard.

Adds a title-behind-speaker hook, burned word-highlight captions, a Warp shot where the
automation breaks ("go back and fix it") and a Finder shot of doing it by hand ("leaving it
manual"). The accepted full-06 picture stays underneath; audio is muxed back by packet copy.
"""
import html
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXP = HERE.parents[1]

FPS = 24
DURATION = 1101 / FPS
END_CARD = 933 / FPS            # 38.875, closing card starts
HOOK_END = 87 / FPS             # 3.625, full-06 Warp insert starts
FIX = (230 / FPS, 304 / FPS)    # 9.583 -> 12.667, into the generated Finder shot
MANUAL = (610 / FPS, 746 / FPS) # 25.417 -> 31.083, a cut already in full-06

script = (EXP / "SCRIPT.txt").read_text().replace("’", "'").split()
asr = json.loads((HERE.parent / "asr/transcript.json").read_text())

# ASR expands wanna/gotta into two words; merge so captions keep the spoken script.
merged, i = [], 0
for tok in script:
    a = dict(asr[i])
    if tok.lower() in ("wanna", "gotta"):
        a["end"] = asr[i + 1]["end"]
        i += 1
    merged.append(a)
    i += 1
assert len(merged) == len(script) and i == len(asr), (len(merged), len(script), i, len(asr))
for tok, a in zip(script, merged):
    assert re.sub(r"\W", "", tok.lower())[:3] == re.sub(r"\W", "", a["text"].lower())[:3] or tok.lower() in ("wanna", "gotta"), (tok, a)
words = [{"t": t, "s": a["start"], "e": a["end"]} for t, a in zip(script, merged)]


def phrases(ws, max_chars=24):
    out, cur = [], []
    for w in ws:
        if cur and len(" ".join(x["t"] for x in cur + [w])) > max_chars:
            out.append(cur)
            cur = []
        cur.append(w)
        text = " ".join(x["t"] for x in cur)
        if w["t"][-1] in ".?" or (w["t"][-1] == "," and len(text) >= 12):
            out.append(cur)
            cur = []
    if cur:
        out.append(cur)
    # Fold a short orphan ("well.") back into the phrase before it.
    for k in range(len(out) - 1, 0, -1):
        if len(" ".join(x["t"] for x in out[k])) <= 8 and len(" ".join(x["t"] for x in out[k - 1] + out[k])) <= 32:
            out[k - 1] += out.pop(k)
    return out


groups = phrases(words)
cap_html, cap_js, srt = [], [], []


def ts(t):
    ms = round(t * 1000)
    return f"{ms // 3600000:02}:{ms // 60000 % 60:02}:{ms // 1000 % 60:02},{ms % 1000:03}"


for gi, ph in enumerate(groups):
    start = ph[0]["s"]
    end = ph[-1]["e"] + 0.18
    if gi + 1 < len(groups):
        end = min(end, groups[gi + 1][0]["s"] - 0.02)
    end = min(end, END_CARD)
    cid = f"cap{gi}"
    spans = "".join(f'<span id="{cid}w{k}">{html.escape(w["t"])}</span> ' for k, w in enumerate(ph))
    cap_html.append(f'<div id="{cid}" class="clip cap" data-layout-allow-overlap data-start="{start:.3f}" data-duration="{end - start:.3f}" data-track-index="6">{spans.strip()}</div>')
    for k, w in enumerate(ph):
        cap_js.append(f'tl.fromTo("#{cid}w{k}",{{color:"rgba(255,255,255,.55)"}},{{color:"#ffffff",duration:.06}},{w["s"]:.3f});')
    srt.append(f"{gi + 1}\n{ts(start)} --> {ts(end)}\n{' '.join(w['t'] for w in ph)}\n")

page = (HERE / "template.tpl").read_text()
for k, v in {"DURATION": f"{DURATION:.4f}", "HOOK_END": f"{HOOK_END:.4f}",
             "FIX_START": f"{FIX[0]:.4f}", "FIX_DUR": f"{FIX[1] - FIX[0]:.4f}",
             "MANUAL_START": f"{MANUAL[0]:.4f}", "MANUAL_DUR": f"{MANUAL[1] - MANUAL[0]:.4f}",
             "CAPTIONS": "\n      ".join(cap_html), "CAPTION_MOTION": "\n      ".join(cap_js)}.items():
    page = page.replace("{{" + k + "}}", v)
(HERE / "index.html").write_text(page)
(HERE / "captions.srt").write_text("\n".join(srt))
print(json.dumps({"captions": len(groups), "duration": DURATION}))
