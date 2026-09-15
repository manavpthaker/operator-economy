"""Week 3 R14: R13 plus the v8 video standard.

Cuts "Maybe I've gotta build a bit more to find that out. That's fine." (one of two endings),
adds a title-behind-speaker hook, burned word-highlight captions and illustrative GTM Engine
screens tied to the lines that name them. Picture base and audio come from assets/base.mp4.
"""
import html
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
PKG = Path("/Users/brownmanbrain/GitHub/content-os/content-packages/week-of-2026-09-21/assets/monday-selfie-r13/script.txt")

FPS = 24
CUT = (899 / FPS, 987 / FPS)      # removed from the R13 timeline
SHIFT = CUT[1] - CUT[0]
BODY_END = 1234 / FPS             # 51.417, R13 closing card follows
DURATION = 1378 / FPS
HOOK_END = 149 / FPS
SHOTS = {                         # output frames
    "projects": (282, 404),       # "I've got other things I wanna build too..."
    "run": (460, 587),            # "a GTM Engine to help me figure that out. It looks at the code"
    "report": (587, 719),         # "then researches who might need it... what to test."
    "decide": (862, 980),         # "choose it over their usual way." / "I don't have to decide it's a business"
}

script = PKG.read_text().replace("’", "'").split()
asr = json.loads((HERE.parent / "asr/transcript.json").read_text())
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
    assert tok.lower() in ("wanna", "gotta") or re.sub(r"\W", "", tok.lower())[:3] == re.sub(r"\W", "", a["text"].lower())[:3], (tok, a)

words = []
for tok, a in zip(script, merged):
    if CUT[0] <= a["start"] < CUT[1]:
        continue
    off = SHIFT if a["start"] >= CUT[1] else 0
    words.append({"t": tok, "s": round(a["start"] - off, 3), "e": round(a["end"] - off, 3)})
assert " ".join(w["t"] for w in words).count("Maybe") == 0


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
    for k in range(len(out) - 1, 0, -1):
        if len(" ".join(x["t"] for x in out[k])) <= 8 and len(" ".join(x["t"] for x in out[k - 1] + out[k])) <= 32:
            out[k - 1] += out.pop(k)
    return out


def ts(t):
    ms = round(t * 1000)
    return f"{ms // 3600000:02}:{ms // 60000 % 60:02}:{ms // 1000 % 60:02},{ms % 1000:03}"


groups = phrases(words)
cap_html, motion, srt = [], [], []
for gi, ph in enumerate(groups):
    start, end = ph[0]["s"], ph[-1]["e"] + 0.18
    if gi + 1 < len(groups):
        end = min(end, groups[gi + 1][0]["s"] - 0.02)
    end = min(end, BODY_END)
    cid = f"cap{gi}"
    spans = "".join(f'<span id="{cid}w{k}">{html.escape(w["t"])}</span> ' for k, w in enumerate(ph))
    cap_html.append(f'<div id="{cid}" class="clip cap" data-layout-allow-overlap data-start="{start:.3f}" data-duration="{end - start:.3f}" data-track-index="6">{spans.strip()}</div>')
    motion += [f'tl.fromTo("#{cid}w{k}",{{color:"rgba(255,255,255,.55)"}},{{color:"#ffffff",duration:.06}},{w["s"]:.3f});' for k, w in enumerate(ph)]
    srt.append(f"{gi + 1}\n{ts(start)} --> {ts(end)}\n{' '.join(w['t'] for w in ph)}\n")

DOTS = '<span class="dot" style="background:#ff5f57"></span><span class="dot" style="background:#febc2e"></span><span class="dot" style="background:#28c840"></span>'


def t(sid):
    return SHOTS[sid][0] / FPS, (SHOTS[sid][1] - SHOTS[sid][0]) / FPS


def shot(sid, inner):
    a, d = t(sid)
    return (f'<section id="{sid}" class="clip scene" data-start="{a:.4f}" data-duration="{d:.4f}" data-track-index="5">'
            f'<div class="fit"><div class="hand"><div class="cam"><img class="photo" src="assets/macbook-reference.png" alt="" />'
            f'{inner}<div class="glare"></div></div></div></div><div class="vignette"></div><div class="grain"></div></section>')


def warp(title, body):
    return (f'<div class="win warp"><div class="bar">{DOTS}<span class="name">{title}</span></div>'
            f'<div class="body"><div class="head"><b>Warp</b> &nbsp;·&nbsp; ~/GitHub</div>{body}</div></div>')


FOLDERS = ["littlefables", "proof-and-voice", "weatherthreads", "storyverse", "hummingbird", "viddy"]
items = "".join(f'<div class="item" style="left:{40 + (k % 3) * 240}px;top:{60 + (k // 3) * 260}px"><div class="folder"></div><div class="lbl">{n}</div></div>' for k, n in enumerate(FOLDERS))

REPORT = [
    ("h", "# littlefables: Discovery"), ("t", ""),
    ("h", "## Bottom line"), ("bl", "Parents like the idea of stories made for"), ("bl", "their own kid. Why they'd switch is unclear."), ("t", ""),
    ("h", "## Who might need it"), ("bl", "Parents doing bedtime reading most nights"), ("bl", "Grandparents reading over video calls"), ("t", ""),
    ("h", "## What they use today"), ("bl", "Library books, reading apps, made-up stories"), ("t", ""),
    ("h", "## Proposed test"), ("t", "Let a parent use it at bedtime for a week."), ("t", "Do they pick it over their usual book?"),
]
report_lines = "".join(f'<div><span class="ln">{k + 1}</span><span class="{c}">{html.escape(s) or "&nbsp;"}</span></div>' for k, (c, s) in enumerate(REPORT))
OPTIONS = ["explore", "retest", "compare", "pivot", "advance", "park", "stop"]

body = f'''    <div id="root" data-composition-id="week3-r14" data-start="0" data-width="720" data-height="1280" data-duration="{DURATION:.4f}">
      <video id="base" class="clip" src="assets/base.mp4" data-start="0" data-duration="{DURATION:.4f}" data-track-index="0" muted playsinline></video>
      <video id="hook-fill" class="clip" src="assets/hook-fill.mp4" data-start="0" data-duration="{HOOK_END:.4f}" data-track-index="1" muted playsinline></video>
      <video id="hook-plate" class="clip" src="assets/hook.mp4" data-start="0" data-duration="{HOOK_END:.4f}" data-track-index="2" muted playsinline></video>
      <div id="hook-title" class="clip" data-start="0" data-duration="{HOOK_END:.4f}" data-track-index="3" data-layout-allow-overlap><span>Could I</span><span>sell this?</span></div>
      <video id="hook-matte" class="clip" src="assets/hook-matte.webm" data-start="0" data-duration="{HOOK_END:.4f}" data-track-index="4" muted playsinline></video>
      {shot("projects", f'<div class="win finder"><div class="fbar"><div class="dots">{DOTS}</div>GitHub</div><div class="fside"><b>FAVORITES</b><br/>Recents<br/>Applications<br/>Desktop<br/>Documents<br/>GitHub</div><div class="grid" data-layout-allow-overlap>{items}<svg class="ptr" id="p-ptr" viewBox="0 0 34 50"><path d="M2 2 L2 40 L12 31 L19 47 L26 44 L19 28 L32 28 Z" fill="#000" stroke="#fff" stroke-width="2.5" stroke-linejoin="round"/></svg></div></div>')}
      {shot("run", warp("gtm — ~/GitHub", '<div class="box" style="margin-top:0" data-layout-allow-overlap><span class="gt">$ </span><span id="r-typed"></span><span class="caret" id="r-caret"></span></div><div class="out" style="margin-top:28px" data-layout-allow-overlap><div class="rrow"><span class="key">Focus</span><span class="dim">reading the code in littlefables</span></div><div class="rrow"><span class="key"></span><span class="ok">✓</span> Product: storybook app for kids</div><div class="rrow"><span class="key"></span><span class="ok">✓</span> Capabilities found in code</div><div class="rrow"><span class="key">Status</span>READY_FOR_DISCOVERY</div><div class="rrow"><span class="key">Next</span><span class="dim">research who might need it</span></div></div>'))}
      {shot("report", f'<div class="win cursor"><div class="cbar">littlefables — Cursor</div><div class="side">▾ .gtm<br/>&nbsp;&nbsp;▾ research<br/>&nbsp;&nbsp;&nbsp;&nbsp;<span class="on">report.md</span><br/>&nbsp;&nbsp;&nbsp;&nbsp;research.json<br/>▸ app<br/>▸ content<br/>package.json</div><div class="tab"><span>report.md</span></div><div class="code"><div class="scroll" id="rep-scroll">{report_lines}</div></div></div>')}
      {shot("decide", warp("gtm — ~/GitHub", '<div class="box" style="margin-top:0" data-layout-allow-overlap><span class="gt">$ </span>uv run gtm report</div><div class="out" style="margin-top:28px;white-space:normal" data-layout-allow-overlap><div class="key" style="width:auto">Proposed test</div><div id="d-test">Let a parent use it at bedtime.<br/>Do they pick it over their usual book?</div><div class="key" style="width:auto;margin-top:26px">Next decision</div><div id="d-opts">' + "".join(f'<span class="opt" id="o-{o}">{o}</span>' for o in OPTIONS) + '</div></div>'))}
      {"\n      ".join(cap_html)}
    </div>'''


def at(word, n=1):
    return [w["s"] for w in words if w["t"].strip(",.?") == word][n - 1]


R0, RD = t("run")
P0, PD = t("projects")
E0, ED = t("report")
D0, DD = t("decide")
keep = at("keep")
motion = [
    'tl.fromTo("#hook-title span", { y: 30, opacity: 0 }, { y: 0, opacity: 1, duration: .45, stagger: .12, ease: "power3.out" }, .15);',
    # Projects: slow push across the folders, pointer drifting.
    f'tl.set("#projects .cam", frameAt(480, 330, 1.1, 780), {P0:.3f});',
    f'tl.to("#projects .cam", {{ ...frameAt(560, 300, 1.3, 780), duration: {PD:.3f}, ease: "sine.inOut" }}, {P0:.3f});',
    f'tl.fromTo("#p-ptr", {{ x: 640, y: 520 }}, {{ x: 330, y: 150, duration: {PD:.3f}, ease: "sine.inOut" }}, {P0:.3f});',
    # Run: type the command, then Focus output lands line by line.
    'const cmd = "uv run gtm run littlefables"; const rt = document.getElementById("r-typed");',
    'rt.innerHTML = [...cmd].map(ch => `<span class="ch" style="display:none">${ch === " " ? "&nbsp;" : ch}</span>`).join("");',
    f'tl.set("#run .cam", frameAt(420, 200, 1.35, 700), {R0:.3f});',
    f'tl.to("#run .ch", {{ display: "inline", duration: .001, stagger: .03, ease: "none" }}, {R0 + .1:.3f});',
    f'tl.set("#r-caret", {{ opacity: 0 }}, {R0 + 1.0:.3f});',
    f'tl.fromTo("#run .rrow", {{ opacity: 0, y: 8 }}, {{ opacity: 1, y: 0, duration: .16, stagger: .45 }}, {R0 + 1.2:.3f});',
    f'tl.to("#run .cam", {{ ...frameAt(430, 330, 1.2, 800), duration: 2.2, ease: "power2.inOut" }}, {R0 + 1.4:.3f});',
    # Report: scroll from the top to the proposed test.
    f'tl.set("#report .cam", frameAt(640, 260, 1.25, 760), {E0:.3f});',
    f'tl.fromTo("#rep-scroll", {{ y: 0 }}, {{ y: -300, duration: {ED - .6:.3f}, ease: "power1.inOut" }}, {E0 + .4:.3f});',
    f'tl.to("#report .cam", {{ ...frameAt(640, 400, 1.25, 760), duration: {ED:.3f}, ease: "sine.inOut" }}, {E0:.3f});',
    # Decide: the test, then the options with explore picked on "keep working".
    f'tl.set("#decide .cam", frameAt(380, 250, 1.4, 760), {D0:.3f});',
    f'tl.fromTo("#d-test", {{ opacity: 0 }}, {{ opacity: 1, duration: .2 }}, {D0 + .1:.3f});',
    f'tl.fromTo("#d-opts .opt", {{ opacity: 0, y: 6 }}, {{ opacity: 1, y: 0, duration: .12, stagger: .06 }}, {at("decide") - .2:.3f});',
    f'tl.to("#decide .cam", {{ ...frameAt(470, 420, 1.15, 780), duration: 1.4, ease: "power2.inOut" }}, {at("decide") - .5:.3f});',
    f'tl.to("#o-explore", {{ backgroundColor: "#2457D6", color: "#ffffff", duration: .12 }}, {keep:.3f});',
]
for sid in SHOTS:
    a, d = t(sid)
    motion.append(f'tl.fromTo("#{sid} .hand", {{ x: 0, y: 0, rotation: 0 }}, {{ x: -6, y: 5, rotation: .3, duration: {d / 2:.3f}, ease: "sine.inOut" }}, {a:.3f});')
    motion.append(f'tl.to("#{sid} .hand", {{ x: 5, y: -3, rotation: -.2, duration: {d / 2:.3f}, ease: "sine.inOut" }}, {a + d / 2:.3f});')

timeline = ['      window.__timelines = window.__timelines || {};', '      const tl = gsap.timeline({ paused: true });', '      window.__timelines["week3-r14"] = tl;']
page = (HERE / "template.tpl").read_text().replace("{{BODY}}", body).replace("{{MOTION}}", "\n".join(timeline + ["      " + m for m in motion]))
(HERE / "index.html").write_text(page)
(HERE / "captions.srt").write_text("\n".join(srt))
print(json.dumps({"captions": len(groups), "duration": round(DURATION, 3), "words": len(words)}))
