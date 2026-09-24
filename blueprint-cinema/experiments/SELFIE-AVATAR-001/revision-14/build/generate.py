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
HOOK_END = 115 / FPS              # cut to full frame on "I could sell this"
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


GTM = Path("/Users/brownmanbrain/GitHub/gtm-engine")   # commit 92cf5dc
KW = {"py": r"\b(def|for|in|if|elif|else|not|and|or|return|continue|import|from|as|lambda|any|sorted|None|True|False)\b",
      "js": r"\b(const|let|return|await|async|new|map|if|else|true|false|null)\b"}


def highlight(line, lang):
    """Tiny tokenizer: strings, comments, keywords, numbers, constants. Escapes everything."""
    pat = re.compile(r"(?P<c>#.*$|//.*$)|(?P<s>[fr]?\"[^\"]*\"|[fr]?'[^']*'|`[^`]*`)|(?P<k>" + KW[lang] + r")|(?P<n>\b\d+\b)|(?P<u>\b[A-Z][A-Z_]{3,}\b)")
    out, pos = [], 0
    if lang == "js":
        pat = re.compile(r"(?P<c>//.*$)|(?P<s>\"[^\"]*\"|'[^']*'|`[^`]*`)|(?P<k>" + KW[lang] + r")|(?P<n>\b\d+\b)|(?P<u>\b[A-Z][A-Z_]{3,}\b)")
    for m in pat.finditer(line):
        out.append(html.escape(line[pos:m.start()]))
        out.append(f'<span class="{m.lastgroup}">{html.escape(m.group())}</span>')
        pos = m.end()
    out.append(html.escape(line[pos:]))
    return "".join(out)


def code_file(rel, first, last, lang, hl_ids):
    """Real lines from the repo, common indent removed, numbered as in the file."""
    lines = (GTM / rel).read_text().splitlines()[first - 1:last]
    indent = min(len(l) - len(l.lstrip()) for l in lines if l.strip())
    rows = []
    for n, l in zip(range(first, last + 1), lines):
        rid = hl_ids.get(n, "")
        rows.append(f'<div class="cl"{f" id={rid}" if rid else ""}><span class="ln">{n}</span>{highlight(l[indent:], lang) or "&nbsp;"}</div>')
    return "".join(rows)


def cursor(rel, rows, sid):
    parts = rel.split("/")
    tree = {"src/gtm_engine/focus_extract.py": "▸ .claude<br/>▾ src/gtm_engine<br/>&nbsp;&nbsp;audit.py<br/>&nbsp;&nbsp;decision.py<br/>&nbsp;&nbsp;<span class=on>focus_extract.py</span><br/>&nbsp;&nbsp;guided.py<br/>&nbsp;&nbsp;research.py<br/>▸ tests",
            ".claude/workflows/phase2-research.js": "▾ .claude/workflows<br/>&nbsp;&nbsp;<span class=on>phase2-research.js</span><br/>▾ src/gtm_engine<br/>&nbsp;&nbsp;audit.py<br/>&nbsp;&nbsp;decision.py<br/>&nbsp;&nbsp;focus_extract.py<br/>&nbsp;&nbsp;guided.py<br/>▸ tests",
            "src/gtm_engine/guided.py": "▸ .claude<br/>▾ src/gtm_engine<br/>&nbsp;&nbsp;audit.py<br/>&nbsp;&nbsp;decision.py<br/>&nbsp;&nbsp;focus_extract.py<br/>&nbsp;&nbsp;<span class=on>guided.py</span><br/>&nbsp;&nbsp;research.py<br/>▸ tests"}[rel]
    return (f'<div class="win cursor"><div class="cbar">gtm-engine — Cursor</div><div class="side">{tree}</div>'
            f'<div class="tab"><span>{parts[-1]}</span></div><div class="code"><div class="scroll" id="{sid}-scroll">{rows}</div></div></div>')


FOLDERS = ["littlefables", "proof-and-voice", "weatherthreads", "storyverse", "hummingbird", "viddy"]
items = "".join(f'<div class="item" style="left:{40 + (k % 3) * 240}px;top:{60 + (k // 3) * 260}px"><div class="folder"></div><div class="lbl">{n}</div></div>' for k, n in enumerate(FOLDERS))

RUN = ("src/gtm_engine/focus_extract.py", 830, 856, "py", {847: "run-hl"})
REPORT = (".claude/workflows/phase2-research.js", 174, 185, "js", {175: "rep-hl1", 176: "rep-hl2"})
DECIDE = ("src/gtm_engine/guided.py", 2376, 2393, "py", {2383: "dec-hl1", 2386: "dec-hl2"})


body = f'''    <div id="root" data-composition-id="week3-r14" data-start="0" data-width="720" data-height="1280" data-duration="{DURATION:.4f}">
      <video id="base" class="clip" src="assets/base.mp4" data-start="0" data-duration="{DURATION:.4f}" data-track-index="0" muted playsinline></video>
      <div id="hook-ground" class="clip" data-start="0" data-duration="{HOOK_END:.4f}" data-track-index="1"></div>
      <video id="hook-plate" class="clip" src="assets/hook.mp4" data-start="0" data-duration="{HOOK_END:.4f}" data-track-index="2" muted playsinline></video>
      <div id="hook-title" class="clip" data-start="0" data-duration="{HOOK_END:.4f}" data-track-index="3" data-layout-allow-overlap><span>Could I</span><span>sell this?</span></div>
      <video id="hook-matte" class="clip" src="assets/hook-matte.webm" data-start="0" data-duration="{HOOK_END:.4f}" data-track-index="4" muted playsinline></video>
      {shot("projects", f'<div class="win finder"><div class="fbar"><div class="dots">{DOTS}</div>GitHub</div><div class="fside"><b>FAVORITES</b><br/>Recents<br/>Applications<br/>Desktop<br/>Documents<br/>GitHub</div><div class="grid" data-layout-allow-overlap>{items}<svg class="ptr" id="p-ptr" viewBox="0 0 34 50"><path d="M2 2 L2 40 L12 31 L19 47 L26 44 L19 28 L32 28 Z" fill="#000" stroke="#fff" stroke-width="2.5" stroke-linejoin="round"/></svg></div></div>')}
      {shot("run", cursor(RUN[0], code_file(*RUN), "run"))}
      {shot("report", cursor(REPORT[0], code_file(*REPORT), "rep"))}
      {shot("decide", cursor(DECIDE[0], code_file(*DECIDE), "dec"))}
      {"\n      ".join(cap_html)}
    </div>'''


def at(word, n=1):
    return [w["s"] for w in words if w["t"].strip(",.?") == word][n - 1]


R0, RD = t("run")
P0, PD = t("projects")
E0, ED = t("report")
D0, DD = t("decide")
motion = [
    'tl.fromTo("#hook-title span", { y: 30, opacity: 0 }, { y: 0, opacity: 1, duration: .45, stagger: .12, ease: "power3.out" }, .15);',
    # Projects: slow push across the folders, pointer drifting.
    f'tl.set("#projects .cam", frameAt(480, 330, 1.1, 780), {P0:.3f});',
    f'tl.to("#projects .cam", {{ ...frameAt(560, 300, 1.3, 780), duration: {PD:.3f}, ease: "sine.inOut" }}, {P0:.3f});',
    f'tl.fromTo("#p-ptr", {{ x: 640, y: 520 }}, {{ x: 330, y: 150, duration: {PD:.3f}, ease: "sine.inOut" }}, {P0:.3f});',
    # Run: the scoring that ranks what the repo's code shows; highlight the code-first weights on "code".
    f'tl.set("#run .cam", frameAt(560, 200, 1.3, 760), {R0:.3f});',
    f'tl.to("#run .cam", {{ ...frameAt(600, 330, 1.3, 760), duration: {RD:.3f}, ease: "sine.inOut" }}, {R0:.3f});',
    f'tl.fromTo("#run-scroll", {{ y: 0 }}, {{ y: -190, duration: {at("code") - R0 - .2:.3f}, ease: "power1.inOut" }}, {R0 + .2:.3f});',
    f'tl.fromTo("#run-hl", {{ backgroundColor: "rgba(106,141,255,0)" }}, {{ backgroundColor: "rgba(106,141,255,.22)", duration: .2 }}, {at("code") - .1:.3f});',
    # Report: the research lenses; buyers on "who might need it", alternatives on "using already".
    f'tl.set("#report .cam", frameAt(600, 180, 1.25, 740), {E0:.3f});',
    f'tl.fromTo("#rep-hl1", {{ backgroundColor: "rgba(106,141,255,0)" }}, {{ backgroundColor: "rgba(106,141,255,.22)", duration: .2 }}, {at("who") - .1:.3f});',
    f'tl.to("#rep-hl1", {{ backgroundColor: "rgba(106,141,255,0)", duration: .2 }}, {at("using", 2) - .15:.3f});',
    f'tl.fromTo("#rep-hl2", {{ backgroundColor: "rgba(106,141,255,0)" }}, {{ backgroundColor: "rgba(106,141,255,.22)", duration: .2 }}, {at("using", 2) - .1:.3f});',
    f'tl.to("#report .cam", {{ ...frameAt(600, 360, 1.25, 740), duration: {ED:.3f}, ease: "sine.inOut" }}, {E0:.3f});',
    # Decide: the outcome rules; ADVANCE still means a larger test, not scaling.
    f'tl.set("#decide .cam", frameAt(560, 150, 1.3, 760), {D0:.3f});',
    f'tl.to("#decide .cam", {{ ...frameAt(600, 400, 1.3, 760), duration: {DD:.3f}, ease: "sine.inOut" }}, {D0:.3f});',
    f'tl.fromTo("#dec-hl1", {{ backgroundColor: "rgba(106,141,255,0)" }}, {{ backgroundColor: "rgba(106,141,255,.22)", duration: .2 }}, {at("decide") - .1:.3f});',
    f'tl.fromTo("#dec-hl2", {{ backgroundColor: "rgba(106,141,255,0)" }}, {{ backgroundColor: "rgba(106,141,255,.22)", duration: .2 }}, {at("decide") - .1:.3f});',
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
