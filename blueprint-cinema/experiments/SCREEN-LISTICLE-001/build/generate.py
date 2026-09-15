"""Generate index.html for the how-I-build video from locked voice timings (v5: phone-filmed laptop shots).

Captions use the exact script words, timed by ASR word order (hook 21 words, body 92 words).
Laptop screen text comes from the grapevines repo, the discovery doc and the master resume (cropped to
facts-cleared lines). Each step is a separate "phone" shot of the same MacBook reference photo.
"""
import html
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

HOOK_OFFSET = 1.05   # hook voice start inside the trimmed swivel clip
BODY_OFFSET = 8.287  # body voice start in master.original-c.wav
DURATION = 40.5
END_CARD = 36.4


def words(script, transcript, offset):
    tokens = script.split()
    asr = json.loads(transcript.read_text())
    assert len(tokens) == len(asr), (len(tokens), len(asr))
    return [{"t": tok, "s": round(a["start"] + offset, 3), "e": round(a["end"] + offset, 3)} for tok, a in zip(tokens, asr)]


hook = words((ROOT / "motion-test-01/HOOK.txt").read_text(), ROOT / "motion-test-01/voice/asr-final/transcript.json", HOOK_OFFSET)
body = words((ROOT / "voice-full/BODY.txt").read_text(), ROOT / "voice-full/asr-final-medium/transcript.json", BODY_OFFSET)
at = lambda word: next(w["s"] for w in body if w["t"] == word)


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


SCENES = [
    ("hook", 0.0, 8.2),
    ("commits", 8.2, 13.37),
    ("problem", 13.37, 15.41),
    ("people", 15.41, 22.83),
    ("plan", 22.83, 26.29),
    ("remove", 26.29, 30.56),
    ("turn", 30.56, END_CARD),
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


def bar(name):
    return f'<div class="bar"><span class="dot" style="background:#ff5f57"></span><span class="dot" style="background:#febc2e"></span><span class="dot" style="background:#28c840"></span><span class="name">{html.escape(name)}</span></div>'


def shot(sid, window_html):
    a, b = S[sid]
    return (f'<section id="{sid}" class="clip scene" data-start="{a}" data-duration="{b - a:.3f}" data-track-index="0">'
            f'<div class="fit"><div class="hand"><div class="cam"><img class="photo" src="assets/macbook-reference.png" alt="" />'
            f'{window_html}<div class="glare"></div></div></div></div><div class="vignette"></div><div class="grain"></div></section>')


scenes_html = [
    f'<video id="hook-video" class="clip" src="assets/hook.mp4" data-start="0" data-duration="{S["hook"][1]}" data-track-index="0" muted playsinline></video>',
    f'<div id="hook-title" class="clip" data-start="0" data-duration="{S["hook"][1]}" data-track-index="1" data-layout-allow-overlap><span>The part of</span><span>building that</span><span>wasn\'t quick</span></div>',
    f'<video id="hook-matte" class="clip" src="assets/hook-matte.webm" data-start="0" data-duration="{S["hook"][1]}" data-track-index="2" muted playsinline></video>',
    shot("commits", '<div class="win dark">' + bar("grapevines — zsh") + '''<div class="body mono">
        <div class="dim">$ git show 7c337b8</div><div class="hash">commit 7c337b8</div><div class="dim">Date: Tue Oct 7 2025</div><div>&nbsp;</div>
        <div>&nbsp;&nbsp;&nbsp;&nbsp;Build Conversation Engine</div><div>&nbsp;</div><div class="hl" id="c-hl">&nbsp;&nbsp;&nbsp;&nbsp;Co-Authored-By: Claude</div></div></div>'''),
    shot("problem", '<div class="win light">' + bar("manav-thaker_master-resume.md") + '''<div class="body md">
        <h1>Manav Thaker</h1><div class="meta">Technical Product Leader · AI Product Management · Builder and Operator</div>
        <h2>Experience</h2><p><b>AI Product Manager · Lovingly</b><br/>Sep 2024 to Sep 2025</p>
        <div class="blurred"><p>Partnered with engineers, designers and marketing on AI work across support, retention and checkout.</p><p>Built internal AI tooling for ticket triage, PRDs and test documentation.</p></div></div></div>'''),
    shot("people", '<div class="win light">' + bar("customer-discovery-master.md") + '''<div class="body md">
        <div class="meta">Last updated February 18, 2026 · Active discovery phase</div><h1>Grapevines Customer Discovery Master Document</h1>
        <h2>Discovery overview</h2><p>This document consolidates learnings from all customer discovery conversations to guide product development, positioning, and go-to-market strategy.</p></div></div>'''),
    shot("plan", '<div class="win light">' + bar("prd-epic-2-the-daily-coach.md") + '''<div class="body md">
        <div class="meta">PRD · Manav Thaker · March 18, 2026</div><h1>Epic 2: The Daily Coach</h1>
        <h2>Problem statement</h2><p>The app doesn’t feel like a daily driver. The dashboard only changes when the user takes a major action.</p></div></div>'''),
    shot("remove", '<div class="win light">' + bar("prd-voice-calibration-removal.md") + '''<div class="body md">
        <div class="meta">PRD · March 24, 2026</div><h1>Voice calibration removal</h1>
        <h2>Decision</h2><p><b>Kill voice calibration from onboarding.</b> Remove the voice selection step entirely.</p></div></div>'''),
    shot("turn", '<div class="win light">' + bar("prd-voice-calibration-removal.md") + '''<div class="body md">
        <div class="meta">PRD · March 24, 2026</div><h1>Voice calibration removal</h1>
        <div class="term"><span class="hash">611cbef</span> Mar 24 2026<br/>Remove voice calibration from onboarding</div></div>
        <div class="swap" id="t-swap"><div class="body md"><div class="meta">Last updated February 18, 2026</div><h1>Customer Discovery Master Document</h1>
        <h2>Discovery overview</h2><p>Learnings from all customer discovery conversations.</p></div></div></div>'''),
    f'''<section id="end" class="clip scene" data-start="{END_CARD}" data-duration="{DURATION - END_CARD:.3f}" data-track-index="0">
      <h1 id="question"><span class="ql">When did talking</span><span class="ql">to people change</span><span class="ql shift">what you built?</span></h1>
      <p id="signature" class="contact">MP Thaker</p><p id="website" class="contact url">mpthaker.xyz</p><p id="linkedin" class="contact url">linkedin.com/in/mptxyz</p></section>''',
]

# Each shot: wider framing at start, slow push-in toward the line being spoken, small handheld drift.
# (scene, start window point, start scale, end window point, end scale, drift sign)
SHOTS = [
    ("commits", (500, 360), 1.02, (330, 610), 1.38, 1),
    ("problem", (500, 300), 1.10, (320, 300), 1.40, -1),
    ("people", (500, 320), 1.04, (380, 330), 1.36, 1),
    ("plan", (480, 330), 1.12, (400, 420), 1.42, -1),
    ("remove", (500, 330), 1.08, (380, 420), 1.44, 1),
    ("turn", (500, 330), 1.06, (420, 360), 1.30, -1),
]
motion = ['const tl = gsap.timeline({ paused: true });',
          'tl.fromTo("#hook-title span", {y:24, opacity:0}, {y:0, opacity:1, duration:.45, stagger:.12, ease:"power3.out"}, .25);']
for sid, p0, s0, p1, s1, sign in SHOTS:
    a, b = S[sid]
    dur = b - a
    motion.append(f'tl.fromTo("#{sid} .cam", frameAt({p0[0]},{p0[1]},{s0}), {{...frameAt({p1[0]},{p1[1]},{s1}), duration:{dur:.3f}, ease:"sine.inOut"}}, {a});')
    motion.append(f'tl.fromTo("#{sid} .hand", {{x:0, y:0, rotation:0}}, {{x:{-6 * sign}, y:5, rotation:{0.35 * sign}, duration:{dur / 2:.3f}, ease:"sine.inOut"}}, {a});')
    motion.append(f'tl.to("#{sid} .hand", {{x:{4 * sign}, y:-3, rotation:{-0.2 * sign}, duration:{dur / 2:.3f}, ease:"sine.inOut"}}, {a + dur / 2:.3f});')
motion.append(f'tl.fromTo("#c-hl", {{backgroundColor:"rgba(120,170,140,0)"}}, {{backgroundColor:"rgba(120,170,140,.35)", duration:.3}}, {at("Now"):.3f});')
motion.append(f'tl.fromTo("#t-swap", {{opacity:0}}, {{opacity:1, duration:.25}}, {at("Knowing") - .1:.3f});')
motion.append(f'tl.fromTo("#question .ql", {{y:16, opacity:0}}, {{y:0, opacity:1, duration:.32, stagger:.13, ease:"power3.out"}}, {END_CARD + .04:.3f});')
motion.append(f'tl.fromTo("#question .shift", {{x:0}}, {{x:56, duration:.5, ease:"power3.inOut", immediateRender:false}}, {END_CARD + .7:.3f});')
motion.append(f'tl.fromTo(".contact", {{y:12, opacity:0}}, {{y:0, opacity:1, duration:.3, stagger:.12, ease:"power3.out"}}, {END_CARD + .75:.3f});')
motion += caption_js
motion.append('window.__timelines = window.__timelines || {}; window.__timelines["how-i-build"] = tl;')

page = (HERE / "template.tpl").read_text()
page = page.replace("{{DURATION}}", str(DURATION)).replace("{{SCENES}}", "\n".join(scenes_html))
page = page.replace("{{CAPTIONS}}", "\n".join(caption_html)).replace("{{MOTION}}", "\n".join(motion))
(HERE / "index.html").write_text(page)


def ts(t):
    ms = round(t * 1000); h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); s, ms = divmod(ms, 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"


srt = [f"{n}\n{ts(ph[0]['s'])} --> {ts(ph[-1]['e'] + .2)}\n{' '.join(w['t'] for w in ph)}\n" for n, ph in enumerate(groups, 1)]
(HERE / "captions.srt").write_text("\n".join(srt))
print(json.dumps({"captions": len(caption_html)}))
