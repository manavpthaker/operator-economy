"""Generate index.html for the context video (v7) from the v13 voice master.

Hook (locked swivel) -> phone-filmed laptop shots per beat -> avatar close-up for the insight
and comments ask -> end card. Captions use the exact v13 script words timed by ASR word order.
"""
import html
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

HOOK_OFFSET = 1.05
BODY_OFFSET = 8.287
CLOSE_START = 51.55      # avatar close-up audio segment starts here in the master
VOICE_END = 69.82
END_CARD = 70.05
DURATION = 74.25
A_OFFSET = 51.30   # take-a time t plays master t + 51.30
B_OFFSET = 63.027  # take-b time t plays master t + 63.027
SPLIT = 63.31      # between "write down." and "That's the context"


def words(script, transcript, offset):
    tokens = script.split()
    asr = json.loads(transcript.read_text())
    if len(tokens) != len(asr):
        # ASR split "Grapevines" into two tokens ("great finds"); merge them.
        merged, i = [], 0
        for tok in tokens:
            a = dict(asr[i])
            if tok.strip(",.").lower() == "grapevines" and asr[i]["text"].strip().lower() in ("great", "grape"):
                a["end"] = asr[i + 1]["end"]
                i += 1
            merged.append(a)
            i += 1
        asr = merged
    assert len(tokens) == len(asr), (len(tokens), len(asr))
    return [{"t": tok, "s": round(a["start"] + offset, 3), "e": round(a["end"] + offset, 3)} for tok, a in zip(tokens, asr)]


hook = words((ROOT / "motion-test-01/HOOK.txt").read_text(), ROOT / "motion-test-01/voice/asr-final/transcript.json", HOOK_OFFSET)
body = words((ROOT / "voice-v13/BODY.txt").read_text(), ROOT / "voice-v13/asr-final/transcript.json", BODY_OFFSET)


def at(word, n=1):
    hits = [w["s"] for w in body if w["t"].strip(",.") == word]
    return hits[n - 1]


def phrases(ws, max_chars=26):
    out, cur = [], []
    for w in ws:
        cur.append(w)
        text = " ".join(x["t"] for x in cur)
        if w["t"][-1] in ".?," and len(text) > 10 or len(text) >= max_chars:
            out.append(cur)
            cur = []
    if cur:
        out.append(cur)
    return out


same = next(w["s"] for i, w in enumerate(body) if w["t"] == "It's" and body[i + 1]["t"] == "the" and body[i + 2]["t"] == "same")
T = {"model": at("What"), "resume": at("Take"), "so": at("So"), "same": same,
     "story": at("storybook"), "inn": at("hospitality"), "thin": at("When"), "think": at("Think")}
SCENES = [
    ("hook", 0.0, 8.2),
    ("commit", 8.2, T["model"]),
    ("model", T["model"], T["resume"]),
    ("finder", T["resume"], 31.0),
    ("upload", 31.0, T["so"]),
    ("summary", T["so"], T["so"] + 2.1),
    ("qa", T["so"] + 2.1, T["same"]),
    ("pv", T["same"], T["story"] - 0.1),
    ("story", T["story"] - 0.1, T["inn"] - 0.1),
    ("inn", T["inn"] - 0.1, T["thin"]),
    ("thin", T["thin"], T["think"] - 0.1),
    ("close", T["think"] - 0.1, END_CARD),
    ("end", END_CARD, DURATION),
]
S = {sid: (a, b) for sid, a, b in SCENES}

caption_html, caption_js = [], []
groups = phrases(hook) + phrases(body)
for gi, ph in enumerate(groups):
    start = ph[0]["s"]
    end = ph[-1]["e"] + 0.18
    if gi + 1 < len(groups):
        end = min(end, groups[gi + 1][0]["s"] - 0.02)
    end = min(end, END_CARD)
    cid = f"cap{gi}"
    spans = "".join(f'<span id="{cid}w{i}">{html.escape(w["t"])}</span> ' for i, w in enumerate(ph))
    caption_html.append(f'<div id="{cid}" class="clip cap" data-layout-allow-overlap data-start="{start:.3f}" data-duration="{end - start:.3f}" data-track-index="6">{spans.strip()}</div>')
    for i, w in enumerate(ph):
        caption_js.append(f'tl.fromTo("#{cid}w{i}",{{color:"rgba(255,255,255,.55)"}},{{color:"#ffffff",duration:.06}},{w["s"]:.3f});')

DOTS = '<span class="dot" style="background:#ff5f57"></span><span class="dot" style="background:#febc2e"></span><span class="dot" style="background:#28c840"></span>'


def chrome(tab, url):
    return f'<div class="chrome"><div class="dots">{DOTS}</div><div class="tabs">{html.escape(tab)}</div><div class="url">{html.escape(url)}</div></div>'


def shot(sid, window_html):
    a, b = S[sid]
    return (f'<section id="{sid}" class="clip scene" data-start="{a:.3f}" data-duration="{b - a:.3f}" data-track-index="0">'
            f'<div class="fit"><div class="hand"><div class="cam"><img class="photo" src="assets/macbook-reference.png" alt="" />'
            f'{window_html}<div class="glare"></div></div></div></div><div class="vignette"></div><div class="grain"></div></section>')


RESUME_PAGE = '''<h1>Manav Thaker</h1><div class="meta">Technical Product Leader · AI Product Management · Builder and Operator</div>
  <h2>Experience</h2><p><b>AI Product Manager, Lovingly</b><br/>Sep 2024 to Sep 2025</p>
  <div class="blurred"><p>Partnered with engineers, designers and marketing on AI work across support, retention and checkout.</p><p>Built internal AI tooling for ticket triage, PRDs and test documentation.</p></div>'''

scenes_html = [
    f'<video id="hook-video" class="clip" src="assets/hook.mp4" data-start="0" data-duration="{S["hook"][1]}" data-track-index="0" muted playsinline></video>',
    f'<div id="hook-title" class="clip" data-start="0" data-duration="{S["hook"][1]}" data-track-index="1" data-layout-allow-overlap><span>The part of</span><span>building that</span><span>wasn\'t quick</span></div>',
    f'<video id="hook-matte" class="clip" src="assets/hook-matte.webm" data-start="0" data-duration="{S["hook"][1]}" data-track-index="2" muted playsinline></video>',
    shot("commit", f'''<div class="win warp"><div class="wbar"><span style="position:absolute;left:18px;top:16px;display:flex">{DOTS}</span>grapevines — claude</div>
      <div class="cc"><div><span class="orange">Claude Code</span> <span class="dim">· ~/grapevines</span></div>
        <div class="box">&gt; commit the conversation engine</div>
        <div><span class="green">●</span> <b>Bash</b>(git commit -m "Build Conversation Engine")</div>
        <div class="dim">&nbsp;&nbsp;⎿&nbsp; [main 7c337b8] Build Conversation Engine</div><div>&nbsp;</div>
        <div class="dim">&nbsp;&nbsp;&nbsp;&nbsp;Date: Tue Oct 7 2025</div>
        <div class="hl" id="c-hl">&nbsp;&nbsp;&nbsp;&nbsp;Co-Authored-By: Claude</div></div></div>'''),
    shot("model", f'''<div class="win warp"><div class="wbar"><span style="position:absolute;left:18px;top:16px;display:flex">{DOTS}</span>grapevines — claude</div>
      <div class="cc" style="font-size:21px;line-height:33px"><div><span class="orange">Claude Code</span> <span class="dim">· ~/grapevines</span></div>
        <div class="box">&gt; what does the conversation engine give the model about the person?</div>
        <div><span class="green">●</span> <b>Read</b>(backend/agents/conversation_engine.py)</div>
        <div class="dim">&nbsp;&nbsp;⎿&nbsp; LINKEDIN PROFILE SIGNALS (from the user's connected LinkedIn account):</div>
        <div class="hl" id="m-hl1">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Headline: {{headline}}</div>
        <div class="hl" id="m-hl2">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{{about_display}}</div>
        <div class="hl" id="m-hl3">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{{positions_block}}</div>
        <div class="dim">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;USE THESE SIGNALS to make the conversation feel like a</div>
        <div class="dim">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;coach who has done their homework.</div></div></div>'''),
    shot("finder", f'''<div class="win finder"><div class="fbar"><div class="dots">{DOTS}</div>Resume</div>
      <div class="fside"><b>FAVORITES</b><br/>Recents<br/>Desktop<br/>Documents<br/>Downloads</div>
      <div class="flist"><div class="sel"><span class="ficon"></span>Manav Thaker - Resume.pdf</div></div>
      <div class="fprev"><div class="page">{RESUME_PAGE}</div></div></div>'''),
    shot("upload", '<div class="win light">' + chrome("Grapevines", "grapevines.ai/onboarding") + '''<div class="gvpage">
      <div class="brand">grapevines</div><h1>Share what you've got</h1>
      <div class="sub">Resumes, bios, cover letters, reviews. Anything that tells me about your background.</div>
      <div class="card"><h3>Upload Career Documents</h3><div class="drop" id="u-drop">Drag files here<div class="types">PDF, DOCX, TXT or MD</div></div>
        <div class="done" id="u-done">✓ Manav Thaker - Resume.pdf</div></div>
      <div class="aside"><h4>Why this matters</h4><p>Your resume tells me <b>what</b> you did.</p><p>I'm looking for the patterns that show <b>who</b> you are.</p></div>
      <div class="chip" id="u-chip"><span class="ficon"></span>Manav Thaker - Resume.pdf</div></div></div>'''),
    shot("summary", '<div class="win light">' + chrome("My Read · Grapevines", "grapevines.ai/demo/my-read") + '''<div class="shotimg"><img src="assets/gv-my-read.png" alt="" /></div>
      <div class="gvpage" id="s-reading"><div class="reading">I've read through your materials. Let me show you what I found.</div></div></div>'''),
    shot("qa", '<div class="win light">' + chrome("Before and after · Grapevines", "grapevines.ai/demo/before-after") + '''<div class="shotimg"><img id="qa-img" src="assets/gv-before-after.png" alt="" /></div></div>'''),
    shot("pv", '<div class="win light">' + chrome("Your brief · Proof & Voice", "proof & voice · your desk") + '''<div class="shotimg" style="background:#1B2A24"><img src="assets/pv-brief.png" alt="" /></div></div>'''),
    shot("story", f'''<div class="win cursor"><div class="cbar">littlefables — Cursor</div>
      <div class="side">▾ content<br/>&nbsp;&nbsp;▾ books<br/>&nbsp;&nbsp;&nbsp;&nbsp;▾ hedgehog-goodnight<br/>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="on">story.json</span><br/>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;cover.png</div>
      <div class="tab"><span>story.json</span></div>
      <div class="code"><div><span class="ln">1</span><span class="t">{{</span></div>
        <div><span class="ln">2</span><span class="b">&nbsp;&nbsp;"title"</span><span class="t">: "Hedgehog's Goodnight",</span></div>
        <div><span class="ln">3</span><span class="b">&nbsp;&nbsp;"by"</span><span class="t">: "Papa",</span></div>
        <div><span class="ln">4</span><span class="b">&nbsp;&nbsp;"pages"</span><span class="t">: [</span></div>
        <div><span class="ln">5</span><span class="t">&nbsp;&nbsp;&nbsp;&nbsp;{{ "text": "The forest was quiet…" }},</span></div>
        <div><span class="ln">6</span><span class="t">&nbsp;&nbsp;&nbsp;&nbsp;{{ "text": "Hedgehog curled up small." }}</span></div>
        <div><span class="ln">7</span><span class="t">&nbsp;&nbsp;],</span></div>
        <div><span class="ln">8</span><span class="b">&nbsp;&nbsp;"vocab"</span><span class="t">: [{{ "word": "burrow",</span></div>
        <div><span class="ln">9</span><span class="t">&nbsp;&nbsp;&nbsp;&nbsp;"kidDefinition": "a cozy hole in the ground" }}]</span></div></div></div>'''),
    shot("inn", f'''<div class="win notes"><div class="nbar"><div class="dots">{DOTS}</div></div>
      <div class="nside"><div class="on"><b>Guest context · Example Inn</b><br/>Today</div></div>
      <div class="nbody"><h1>Guest context · Example Inn</h1>
        <div class="q">Who books direct, and why?</div><div class="q">What do they ask before booking?</div>
        <div class="q">What makes them come back?</div><div class="q">What would they never say on a form?</div></div></div>'''),
    shot("thin", '<div class="win light">' + chrome("Before and after · Grapevines", "grapevines.ai/demo/before-after") + '''<div class="shotimg"><img id="thin-img" src="assets/gv-before-after.png" alt="" /></div></div>'''),
    f'<video id="close-a" class="clip" src="assets/close-a.mp4" data-start="{S["close"][0]:.3f}" data-media-start="{S["close"][0] - A_OFFSET:.3f}" data-duration="{SPLIT - S["close"][0]:.3f}" data-track-index="0" muted playsinline></video>',
    f'<video id="close-b" class="clip" src="assets/close-b.mp4" style="transform:scale(1.08);transform-origin:50% 38%" data-start="{SPLIT:.3f}" data-media-start="{SPLIT - B_OFFSET:.3f}" data-duration="{END_CARD - SPLIT:.3f}" data-track-index="0" muted playsinline></video>',
    f'''<section id="end" class="clip scene" data-start="{END_CARD}" data-duration="{DURATION - END_CARD:.3f}" data-track-index="0">
      <h1 id="question"><span class="ql">How does your app</span><span class="ql">get context</span><span class="ql shift">from people?</span></h1>
      <p id="signature" class="contact">MP Thaker</p><p id="website" class="contact url">mpthaker.xyz</p><p id="linkedin" class="contact url">linkedin.com/in/mptxyz</p></section>''',
]

# (scene, start window point, start scale, end window point, end scale, drift sign)
SHOTS = [
    ("commit", (500, 330), 1.04, (330, 560), 1.40, 1),
    ("model", (500, 360), 1.06, (380, 470), 1.36, -1),
    ("finder", (560, 380), 1.06, (760, 330), 1.36, 1),
    ("upload", (500, 380), 1.08, (380, 420), 1.26, -1),
    ("summary", (420, 360), 1.10, (400, 330), 1.30, 1),
    ("pv", (500, 380), 1.06, (560, 400), 1.34, -1),
    ("story", (560, 360), 1.08, (600, 330), 1.32, 1),
    ("inn", (600, 360), 1.08, (620, 300), 1.34, -1),
    ("thin", (500, 300), 1.20, (500, 560), 1.30, 1),
]
motion = ['const tl = gsap.timeline({ paused: true });',
          'tl.fromTo("#hook-title span", {y:24, opacity:0}, {y:0, opacity:1, duration:.45, stagger:.12, ease:"power3.out"}, .25);']
for sid, p0, s0, p1, s1, sign in SHOTS:
    a, b = S[sid]
    dur = b - a
    motion.append(f'tl.fromTo("#{sid} .cam", frameAt({p0[0]},{p0[1]},{s0}), {{...frameAt({p1[0]},{p1[1]},{s1}), duration:{dur:.3f}, ease:"sine.inOut"}}, {a:.3f});')
    motion.append(f'tl.fromTo("#{sid} .hand", {{x:0, y:0, rotation:0}}, {{x:{-6 * sign}, y:5, rotation:{0.35 * sign}, duration:{dur / 2:.3f}, ease:"sine.inOut"}}, {a:.3f});')
    motion.append(f'tl.to("#{sid} .hand", {{x:{4 * sign}, y:-3, rotation:{-0.2 * sign}, duration:{dur / 2:.3f}, ease:"sine.inOut"}}, {a + dur / 2:.3f});')

# Q&A: three hard cuts on the captured card (question, answer, after), each its own framing.
qa_a, qa_b = S["qa"]
cut = (qa_b - qa_a) / 3
for i, (pt, sc) in enumerate((((500, 330), 1.55), ((500, 390), 1.55), ((480, 560), 1.42))):
    t0 = qa_a + i * cut
    motion.append(f'tl.set("#qa .cam", frameAt({pt[0]},{pt[1]},{sc}), {t0:.3f});')
    motion.append(f'tl.fromTo("#qa .hand", {{x:{3 - 6 * i}, y:0}}, {{x:{-3 + 6 * i}, y:3, duration:{cut:.3f}, ease:"sine.inOut"}}, {t0:.3f});')
motion.append(f'tl.fromTo("#qa-img", {{y:-160}}, {{y:-160, duration:.01}}, {qa_a:.3f});')
motion.append(f'tl.fromTo("#thin-img", {{y:-40}}, {{y:-420, duration:{S["thin"][1] - S["thin"][0]:.3f}, ease:"sine.inOut"}}, {S["thin"][0]:.3f});')

# Upload: resume chip drags into the drop zone, zone lights, file lands.
ua = S["upload"][0]
motion.append(f'tl.fromTo("#u-chip", {{x:-120, y:120, opacity:0}}, {{x:120, y:-190, opacity:1, duration:1.1, ease:"power2.inOut"}}, {ua + .1:.3f});')
motion.append(f'tl.fromTo("#u-drop", {{backgroundColor:"rgba(241,245,241,0)", borderColor:"#C9C2B8"}}, {{backgroundColor:"rgba(241,245,241,1)", borderColor:"#7E9A86", duration:.2}}, {ua + .9:.3f});')
motion.append(f'tl.to("#u-chip", {{opacity:0, duration:.15}}, {ua + 1.3:.3f});')
motion.append(f'tl.fromTo("#u-done", {{opacity:0}}, {{opacity:1, duration:.25}}, {ua + 1.4:.3f});')
# Summary: brief reading interstitial, then the captured My Read page.
motion.append(f'tl.fromTo("#s-reading", {{opacity:1}}, {{opacity:0, duration:.25}}, {S["summary"][0] + .7:.3f});')
motion.append(f'tl.fromTo("#c-hl", {{backgroundColor:"rgba(120,170,140,0)"}}, {{backgroundColor:"rgba(120,170,140,.35)", duration:.3}}, {at("Now"):.3f});')
motion.append(f'tl.fromTo("#m-hl1, #m-hl2, #m-hl3", {{backgroundColor:"rgba(120,170,140,0)"}}, {{backgroundColor:"rgba(120,170,140,.35)", duration:.3, stagger:.2}}, {at("give"):.3f});')
motion.append(f'tl.fromTo("#question .ql", {{y:16, opacity:0}}, {{y:0, opacity:1, duration:.32, stagger:.13, ease:"power3.out"}}, {END_CARD + .04:.3f});')
motion.append(f'tl.fromTo("#question .shift", {{x:0}}, {{x:56, duration:.5, ease:"power3.inOut", immediateRender:false}}, {END_CARD + .7:.3f});')
motion.append(f'tl.fromTo(".contact", {{y:12, opacity:0}}, {{y:0, opacity:1, duration:.3, stagger:.12, ease:"power3.out"}}, {END_CARD + .75:.3f});')
motion += caption_js
motion.append('window.__timelines = window.__timelines || {}; window.__timelines["how-i-build"] = tl;')

page = (HERE / "template.tpl").read_text()
page = page.replace("{{DURATION}}", str(DURATION)).replace("{{SCENES}}", "\n".join(scenes_html))
page = page.replace("{{CAPTIONS}}", "\n".join(caption_html)).replace("{{MOTION}}", "\n".join(motion))
page = page.replace('src="assets/voice.wav" data-start="0" data-duration="36.058"', f'src="assets/voice-v13.wav" data-start="0" data-duration="{VOICE_END}"')
(HERE / "index.html").write_text(page)


def ts(t):
    ms = round(t * 1000); h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); s, ms = divmod(ms, 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"


srt = [f"{n}\n{ts(ph[0]['s'])} --> {ts(ph[-1]['e'] + .2)}\n{' '.join(w['t'] for w in ph)}\n" for n, ph in enumerate(groups, 1)]
(HERE / "captions.srt").write_text("\n".join(srt))
print(json.dumps({"scenes": {k: [round(a, 2), round(b, 2)] for k, (a, b) in S.items()}, "captions": len(caption_html)}))
