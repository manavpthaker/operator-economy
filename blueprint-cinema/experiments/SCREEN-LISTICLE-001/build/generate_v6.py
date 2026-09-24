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
    shot("commits", '''<div class="win warp"><div class="wbar"><span style="position:absolute;left:18px;top:16px;display:flex"><span class="dot" style="background:#ff5f57"></span><span class="dot" style="background:#febc2e"></span><span class="dot" style="background:#28c840"></span></span>grapevines — claude</div>
      <div class="cc"><div><span class="orange">Claude Code</span> <span class="dim">· ~/grapevines</span></div>
        <div class="box">&gt; commit the conversation engine</div>
        <div><span class="green">●</span> <b>Bash</b>(git commit -m "Build Conversation Engine")</div>
        <div class="dim">&nbsp;&nbsp;⎿&nbsp; [main 7c337b8] Build Conversation Engine</div>
        <div>&nbsp;</div>
        <div class="dim">&nbsp;&nbsp;&nbsp;&nbsp;Date: Tue Oct 7 2025</div>
        <div class="hl" id="c-hl">&nbsp;&nbsp;&nbsp;&nbsp;Co-Authored-By: Claude</div></div></div>'''),
    shot("problem", '''<div class="win gdocs"><div class="chrome"><div class="dots"><span class="dot" style="background:#ff5f57"></span><span class="dot" style="background:#febc2e"></span><span class="dot" style="background:#28c840"></span></div><div class="tabs">Manav Thaker - Resume - Google Docs</div><div class="url">docs.google.com/document</div></div>
      <div class="gbar"><div class="gicon"></div><div class="gtitle">Manav Thaker - Resume</div><div class="gmenu">File Edit View Insert Format Tools Extensions Help</div><div class="gshare">Share</div></div>
      <div class="gtool"></div>
      <div class="page"><h1>Manav Thaker</h1><div class="meta">Technical Product Leader · AI Product Management · Builder and Operator</div>
        <h2>Experience</h2><p><b>AI Product Manager, Lovingly</b><br/>Sep 2024 to Sep 2025</p>
        <div class="blurred"><p>Partnered with engineers, designers and marketing on AI work across support, retention and checkout.</p><p>Built internal AI tooling for ticket triage, PRDs and test documentation.</p></div></div></div>'''),
    shot("people", '''<div class="win cursor"><div class="cbar">brown-man-content — Cursor</div>
      <div class="side">▾ research<br/>&nbsp;&nbsp;▾ grapevines<br/>&nbsp;&nbsp;&nbsp;&nbsp;b2b-market-analysis.md<br/>&nbsp;&nbsp;&nbsp;&nbsp;<span class="on">customer-discovery-master.md</span><br/>&nbsp;&nbsp;&nbsp;&nbsp;competitive-moats-analysis.md<br/>&nbsp;&nbsp;&nbsp;&nbsp;prioritized-backlog-p0-p1.md</div>
      <div class="tab"><span>customer-discovery-master.md</span></div>
      <div class="code"><div><span class="ln">1</span><span class="h"># Grapevines Customer Discovery</span></div><div><span class="ln"></span><span class="h">&nbsp;&nbsp;Master Document</span></div>
        <div><span class="ln">2</span></div><div><span class="ln">3</span><span class="b">**Last Updated:**</span> <span class="t">February 18, 2026</span></div>
        <div><span class="ln">4</span><span class="b">**Status:**</span> <span class="t">Active Discovery Phase</span></div><div><span class="ln">5</span></div>
        <div><span class="ln">6</span><span class="h">## Discovery Overview</span></div><div><span class="ln">7</span></div>
        <div><span class="ln">8</span><span class="t">This document consolidates learnings</span></div><div><span class="ln"></span><span class="t">from all customer discovery conversations</span></div>
        <div><span class="ln"></span><span class="t">to guide product development.</span></div></div></div>'''),
    shot("plan", '''<div class="win github"><div class="chrome"><div class="dots"><span class="dot" style="background:#ff5f57"></span><span class="dot" style="background:#febc2e"></span><span class="dot" style="background:#28c840"></span></div><div class="tabs">grapevines/docs/prd-epic-2-the-daily-coach.md</div><div class="url">github.com/manavpthaker/grapevines/blob/main/docs/prd-epic-2-the-daily-coach.md</div></div>
      <div class="ghead">grapevines / docs / <b>prd-epic-2-the-daily-coach.md</b></div>
      <div class="box"><div class="boxhead"><span class="pill">Preview</span> Code</div>
        <div class="md"><h1>PRD: Epic 2, The Daily Coach</h1><div class="meta">Author: Manav Thaker · Date: March 18, 2026</div>
          <h2>Problem Statement</h2><p>The app doesn’t feel like a daily driver. The dashboard only changes when the user takes a major action.</p></div></div></div>'''),
    shot("remove", '''<div class="win github"><div class="chrome"><div class="dots"><span class="dot" style="background:#ff5f57"></span><span class="dot" style="background:#febc2e"></span><span class="dot" style="background:#28c840"></span></div><div class="tabs">Remove voice calibration from onboarding</div><div class="url">github.com/manavpthaker/grapevines/commit/611cbef</div></div>
      <div class="ghead"><b>Remove voice calibration from onboarding</b> and fix synthesis bugs</div>
      <div class="box"><div class="boxhead">backend/agents/coach_note_agent.py</div>
        <div class="diff"><div class="ctx">@@ def build_context(user_id):</div><div class="del">-    # 3. VOICE</div><div class="del">-    try:</div>
          <div class="del">-        voice_result = db.from_("voice_profiles")</div><div class="del">-            .select("voice_archetype, calibrated_at")</div>
          <div class="del">-            .eq("user_id", user_id)</div><div class="del">-        if voice_result.data:</div><div class="del">-            voice = voice_result.data[0]</div>
          <div class="del">-            context["voice"] = {</div><div class="del">-                "calibrated": voice.get("calibrated_at") is not None,</div></div></div></div>'''),
    shot("turn", '''<div class="win github"><div class="chrome"><div class="dots"><span class="dot" style="background:#ff5f57"></span><span class="dot" style="background:#febc2e"></span><span class="dot" style="background:#28c840"></span></div><div class="tabs">Commits · grapevines</div><div class="url">github.com/manavpthaker/grapevines/commits/main</div></div>
      <div class="ghead">Commits on <b>Mar 24, 2026</b></div>
      <div class="box commits"><div class="row">Remove voice from My Story navigation <span class="sha">13e854f</span></div>
        <div class="row hl">Remove voice calibration from onboarding <span class="sha">611cbef</span></div>
        <div class="row">Fix onboarding resume and document status bugs <span class="sha">8dbc50d</span></div></div>
      <div class="swap" id="t-swap" style="top:0"><div class="app cursor"><div class="cbar">brown-man-content — Cursor</div>
        <div class="tab" style="left:0"><span>customer-discovery-master.md</span></div>
        <div class="code" style="left:0"><div><span class="ln">1</span><span class="h"># Grapevines Customer Discovery</span></div><div><span class="ln"></span><span class="h">&nbsp;&nbsp;Master Document</span></div>
          <div><span class="ln">2</span></div><div><span class="ln">3</span><span class="b">**Last Updated:**</span> <span class="t">February 18, 2026</span></div><div><span class="ln">4</span></div>
          <div><span class="ln">5</span><span class="h">## Discovery Overview</span></div><div><span class="ln">6</span></div>
          <div><span class="ln">7</span><span class="t">Learnings from all customer</span></div><div><span class="ln"></span><span class="t">discovery conversations.</span></div></div></div></div></div>'''),
    f'''<section id="end" class="clip scene" data-start="{END_CARD}" data-duration="{DURATION - END_CARD:.3f}" data-track-index="0">
      <h1 id="question"><span class="ql">When did talking</span><span class="ql">to people change</span><span class="ql shift">what you built?</span></h1>
      <p id="signature" class="contact">MP Thaker</p><p id="website" class="contact url">mpthaker.xyz</p><p id="linkedin" class="contact url">linkedin.com/in/mptxyz</p></section>''',
]

# Each shot: wider framing at start, slow push-in toward the line being spoken, small handheld drift.
# (scene, start window point, start scale, end window point, end scale, drift sign)
SHOTS = [
    ("commits", (500, 330), 1.04, (330, 560), 1.40, 1),
    ("problem", (500, 360), 1.08, (400, 420), 1.38, -1),
    ("people", (520, 330), 1.04, (480, 330), 1.36, 1),
    ("plan", (500, 360), 1.10, (420, 470), 1.40, -1),
    ("remove", (500, 360), 1.06, (420, 400), 1.40, 1),
    ("turn", (500, 300), 1.08, (460, 300), 1.30, -1),
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
