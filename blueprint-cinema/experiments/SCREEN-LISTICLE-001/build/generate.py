"""Generate index.html for the how-I-build screen-listicle video from locked voice timings.

Captions use the exact script words, timed by ASR word order (hook 21 words, body 92 words).
Screen text is taken from the grapevines repo (commit history and planning docs).
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
    # id, start, end
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
cap_index = 0
for group, style, scene_filter in ((hook, "over", None), (body, "under", None)):
    groups = phrases(group)
    for gi, ph in enumerate(groups):
        start = ph[0]["s"]
        # no burned captions over the turn text or end card (the words are already on screen)
        if start >= S["turn"][0] - 0.05:
            continue
        end = ph[-1]["e"] + 0.18
        if gi + 1 < len(groups):
            end = min(end, groups[gi + 1][0]["s"] - 0.02)
        if style == "over":
            end = min(end, S["hook"][1])
        cid = f"cap{cap_index}"
        cap_index += 1
        spans = "".join(f'<span class="w" id="{cid}w{i}">{html.escape(w["t"])}</span> ' for i, w in enumerate(ph))
        caption_html.append(
            f'<div id="{cid}" class="clip cap cap-{style}" data-layout-allow-overlap data-start="{start:.3f}" data-duration="{end - start:.3f}" data-track-index="6">{spans.strip()}</div>'
        )
        for i, w in enumerate(ph):
            caption_js.append(f'tl.fromTo("#{cid}w{i}",{{color:MUTED_{style.upper()}}},{{color:ON_{style.upper()},duration:.06}},{w["s"]:.3f});')


def scene(sid, inner, track=0):
    a, b = S[sid]
    return f'<section id="{sid}" class="clip scene" data-start="{a}" data-duration="{b - a:.3f}" data-track-index="{track}">{inner}</section>'


commits = [
    ("4bcc67e", "2025-10-07", "Initial commit: Grapevines project setup"),
    ("eaeff3f", "2025-10-07", "Build Context Library Agent"),
    ("7c337b8", "2025-10-07", "Build Conversation Engine"),
    ("28184ec", "2025-10-07", "Build Influence Library"),
    ("bde5c3f", "2025-10-07", "Build Voice Blending Agent"),
]
commit_rows = "".join(
    f'<div class="row{" first" if i == 0 else ""}"><span class="hash">{h}</span> <span class="date">{d}</span> {html.escape(m)}</div>'
    for i, (h, d, m) in enumerate(commits)
)

scenes_html = [
    f'<video id="hook-video" class="clip" src="assets/hook.mp4" data-start="0" data-duration="{S["hook"][1]}" data-track-index="0" muted playsinline></video>',
    f'<div id="hook-title" class="clip" data-start="0" data-duration="{S["hook"][1]}" data-track-index="1" data-layout-allow-overlap><span>The part of</span><span>building that</span><span>wasn\'t quick</span></div>',
    f'<video id="hook-matte" class="clip" src="assets/hook-matte.webm" data-start="0" data-duration="{S["hook"][1]}" data-track-index="2" muted playsinline></video>',
    scene("commits", '''
      <div class="screen terminal" id="c-screen"><div class="prompt">$ git show 7c337b8</div>
        <div class="row"><span class="hash">commit 7c337b8</span></div>
        <div class="row"><span class="date">Date: Tue Oct 7 2025</span></div>
        <div class="row">&nbsp;</div>
        <div class="row">Build Conversation Engine</div>
        <div class="row">&nbsp;</div>
        <div class="row first">Co-Authored-By: Claude</div></div>
      <div class="tag" id="c-tag">Grapevines commit, October 2025</div>'''),
    scene("problem", '''
      <div class="step-no">01</div><h2 class="step-head">A problem I had</h2>
      <div class="screen doc resume" id="pr-screen"><h3>Manav Thaker</h3>
        <h4>Technical Product Leader · AI Product Management · Builder and Operator</h4>
        <h5>Experience</h5>
        <p class="role"><b>AI Product Manager · Lovingly</b><br/>Sep 2024 to Sep 2025</p>
        <div class="blurred"><p>Partnered with engineers, designers and marketing on AI work across support, retention and checkout.</p><p>Built internal AI tooling for ticket triage, PRDs and test documentation.</p><p>Co-Founder and Head of Product · Panso</p></div></div>
      <div class="tag">My resume</div>'''),
    scene("people", '''
      <div class="step-no">02</div><h2 class="step-head">Talk to people</h2>
      <div class="screen doc" id="p-screen"><h4>Last updated February 18, 2026 · Active discovery phase</h4><h3>Grapevines Customer Discovery Master Document</h3>
        <h5>Discovery overview</h5>
        <p>This document consolidates learnings from all customer discovery conversations to guide product development, positioning, and go-to-market strategy.</p></div>
      <div class="tag">My discovery notes, February 2026</div>'''),
    scene("plan", '''
      <div class="step-no">03</div><h2 class="step-head">Write the plan</h2>
      <div class="screen doc" id="pl-screen"><h4>PRD · Manav Thaker · March 18, 2026</h4><h3>Epic 2: The Daily Coach</h3>
        <h5>Problem statement</h5>
        <p>The app doesn’t feel like a daily driver. The dashboard only changes when the user takes a major action.</p></div>
      <div class="tag">Planning doc, March 2026</div>'''),
    scene("remove", '''
      <div class="step-no">04</div><h2 class="step-head">Take things out</h2>
      <div class="screen doc" id="r-screen"><h4>PRD · March 24, 2026</h4><h3>Voice calibration removal</h3>
        <h5>Decision</h5>
        <p><b>Kill voice calibration from onboarding.</b> Remove the voice selection step entirely.</p>
        <div class="commit"><span class="hash">611cbef</span> Remove voice calibration from onboarding</div></div>
      <div class="tag">Removed March 2026</div>'''),
    scene("turn", '''
      <h2 class="turn-lead" id="t-lead">Building it myself means I can change it fast.</h2>
      <div class="sage" id="t-sage"><p id="t-sage-text">Knowing what to change still comes from talking to people.</p></div>
      <div class="screen doc sameday" id="t-screen"><h4>PRD · March 24, 2026</h4><h3>Voice calibration removal</h3>
        <div class="commit"><span class="hash">611cbef</span> March 24, 2026</div>
        <div class="commit">Remove voice calibration from onboarding</div></div>
      <div class="screen doc callback" id="t-disc"><h4>February 18, 2026</h4><h3>Customer Discovery Master Document</h3></div>
      <div class="tag" id="t-tag">Decided and shipped the same day</div>'''),
    scene("end", '''
      <h1 id="question"><span class="ql">When did talking</span><span class="ql">to people change</span><span class="ql shift">what you built?</span></h1>
      <p id="signature" class="contact">MP Thaker</p>
      <p id="website" class="contact url">mpthaker.xyz</p>
      <p id="linkedin" class="contact url">linkedin.com/in/mptxyz</p>'''),
]

knowing = next(w["s"] for w in body if w["t"] == "Knowing")
it_started = next(w["s"] for w in body if w["t"] == "It")
now_word = next(w["s"] for w in body if w["t"] == "Now")

motion = f"""
const MUTED_OVER="rgba(255,255,255,.55)", ON_OVER="#ffffff", MUTED_UNDER="#7A8990", ON_UNDER="#202426";
const tl = gsap.timeline({{ paused: true }});
// Hook title rises in behind the speaker.
tl.fromTo("#hook-title span", {{y:24, opacity:0}}, {{y:0, opacity:1, duration:.45, stagger:.12, ease:"power3.out"}}, .25);
// Dev-team line: the commit carries Claude as co-author.
tl.fromTo("#c-screen", {{x:60, opacity:0}}, {{x:0, opacity:1, duration:.55, ease:"power3.out"}}, {S['commits'][0]});
tl.fromTo("#c-screen .row", {{opacity:0, y:8}}, {{opacity:1, y:0, duration:.2, stagger:.12, ease:"power2.out"}}, {S['commits'][0] + .3:.3f});
tl.fromTo("#c-screen .first", {{backgroundColor:"rgba(169,193,178,0)"}}, {{backgroundColor:"rgba(169,193,178,.45)", duration:.35}}, {now_word:.3f});
tl.fromTo("#c-tag", {{opacity:0}}, {{opacity:1, duration:.3}}, {S['commits'][0] + .8:.3f});
tl.fromTo("#problem .step-no, #problem .step-head", {{opacity:0, y:14}}, {{opacity:1, y:0, duration:.4, stagger:.08, ease:"power3.out"}}, {S['problem'][0]});
tl.fromTo("#pr-screen", {{x:60, opacity:0}}, {{x:0, opacity:1, duration:.5, ease:"power3.out"}}, {S['problem'][0] + .1:.3f});
tl.fromTo("#problem .tag", {{opacity:0}}, {{opacity:1, duration:.3}}, {S['problem'][0] + .5:.3f});
"""
for sid, screen in (("people", "#p-screen"), ("plan", "#pl-screen"), ("remove", "#r-screen")):
    a = S[sid][0]
    motion += f'tl.fromTo("#{sid} .step-no, #{sid} .step-head", {{opacity:0, y:14}}, {{opacity:1, y:0, duration:.4, stagger:.08, ease:"power3.out"}}, {a});\n'
    motion += f'tl.fromTo("{screen}", {{x:60, opacity:0}}, {{x:0, opacity:1, duration:.55, ease:"power3.out"}}, {a + .1:.3f});\n'
    motion += f'tl.fromTo("#{sid} .tag", {{opacity:0}}, {{opacity:1, duration:.3}}, {a + .5:.3f});\n'
motion += f"""
tl.fromTo("#r-screen .commit", {{opacity:0, y:10}}, {{opacity:1, y:0, duration:.35, ease:"power2.out"}}, {S['remove'][0] + 1.6:.3f});
// Turn: countershift. The screen moves right and the opened field carries the judgment.
tl.fromTo("#t-lead", {{opacity:0, y:14}}, {{opacity:1, y:0, duration:.45, ease:"power3.out"}}, {S['turn'][0]});
tl.fromTo("#t-screen", {{x:60, opacity:0}}, {{x:0, opacity:1, duration:.5, ease:"power3.out"}}, {S['turn'][0] + .15:.3f});
tl.fromTo("#t-screen .commit", {{opacity:0, y:8}}, {{opacity:1, y:0, duration:.3, stagger:.2, ease:"power2.out"}}, {S['turn'][0] + .8:.3f});
tl.fromTo("#t-tag", {{opacity:0}}, {{opacity:1, duration:.3}}, {S['turn'][0] + 1.3:.3f});
tl.to("#t-screen, #t-tag", {{opacity:0, duration:.3}}, {knowing - .4:.3f});
tl.fromTo("#t-sage", {{width:0}}, {{width:392, duration:.7, ease:"power3.inOut"}}, {knowing - .35:.3f});
tl.fromTo("#t-sage-text", {{opacity:0, x:-12}}, {{opacity:1, x:0, duration:.4, ease:"power2.out"}}, {knowing + .15:.3f});
tl.fromTo("#t-disc", {{x:120, opacity:0}}, {{x:0, opacity:1, duration:.7, ease:"power3.inOut"}}, {knowing - .2:.3f});
// End card: Counterproof question and signature.
tl.fromTo("#question .ql", {{y:16, opacity:0}}, {{y:0, opacity:1, duration:.32, stagger:.13, ease:"power3.out"}}, {END_CARD + .04:.3f});
tl.fromTo("#question .shift", {{x:0}}, {{x:56, duration:.5, ease:"power3.inOut", immediateRender:false}}, {END_CARD + .7:.3f});
tl.fromTo(".contact", {{y:12, opacity:0}}, {{y:0, opacity:1, duration:.3, stagger:.12, ease:"power3.out"}}, {END_CARD + .75:.3f});
"""
motion += "\n".join(caption_js)
motion += '\nwindow.__timelines = window.__timelines || {};\nwindow.__timelines["how-i-build"] = tl;\n'

page = (HERE / "template.tpl").read_text()
page = page.replace("{{DURATION}}", str(DURATION)).replace("{{SCENES}}", "\n".join(scenes_html))
page = page.replace("{{CAPTIONS}}", "\n".join(caption_html)).replace("{{MOTION}}", motion)
(HERE / "index.html").write_text(page)

srt = []
for n, ph in enumerate(phrases(hook) + phrases(body), 1):
    def ts(t):
        ms = round(t * 1000); h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); s, ms = divmod(ms, 1000)
        return f"{h:02}:{m:02}:{s:02},{ms:03}"
    srt.append(f"{n}\n{ts(ph[0]['s'])} --> {ts(ph[-1]['e'] + .2)}\n{' '.join(w['t'] for w in ph)}\n")
(HERE / "captions.srt").write_text("\n".join(srt))
print(json.dumps({"captions_in_video": cap_index, "srt_cues": len(srt), "knowing": knowing, "it_started": it_started}))
