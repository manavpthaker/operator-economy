#!/usr/bin/env python3
"""Build the EP009 Short 03 hook composition from the owner-locked r8 carrier."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
FPS = 24
CTA_FRAMES = 60

SEGMENTS = [
    {
        "id": "served-no-email",
        "first_word": "W000951",
        "last_word": "W000960",
        "source_in_frame": 8148,
        "source_out_frame_exclusive": 8232,
        "verbatim": "The inn served the guest and doesn't have his email.",
        "visual": "full-height locked hospitality film; innkeeper at the desk",
    },
    {
        "id": "guest-book-at-site",
        "first_word": "W000941",
        "last_word": "W000950",
        "source_in_frame": 8070,
        "source_out_frame_exclusive": 8141,
        "verbatim": "So the guest book now lives at the booking site.",
        "visual": "native portrait relationship graphic; guest book visibly transfers from inn to booking site",
    },
    {
        "id": "constraint-before-tool",
        "first_word": "W000961",
        "last_word": "W000974",
        "source_in_frame": 8250,
        "source_out_frame_exclusive": 8361,
        "verbatim": "Which means the recovery job has a design constraint before it has a tool.",
        "visual": "native portrait order-of-operations graphic; the constraint visibly precedes the tool without revealing the fix",
    },
    {
        "id": "relay-rule-boundary",
        "first_word": "W000975",
        "last_word": "W000994",
        "source_in_frame": 8373,
        "source_out_frame_exclusive": 8520,
        "verbatim": "You can't win a guest back from a relay address, and under the site's rules you're not supposed to try.",
        "visual": "native portrait relay path that stops at a clearly labeled site-rule boundary",
    },
    {
        "id": "not-email-tool",
        "first_word": "W000995",
        "last_word": "W001003",
        "source_in_frame": 8520,
        "source_out_frame_exclusive": 8592,
        "verbatim": "What the inn needs first isn't an email tool.",
        "visual": "native portrait email-tool card exits, leaving the first-step slot unresolved",
    },
]

cursor = 0
for segment in SEGMENTS:
    segment["timeline_in_frame"] = cursor
    segment["frame_count"] = segment["source_out_frame_exclusive"] - segment["source_in_frame"]
    cursor += segment["frame_count"]
    segment["timeline_out_frame_exclusive"] = cursor

CTA_IN_FRAME = cursor
TOTAL_FRAMES = CTA_IN_FRAME + CTA_FRAMES
TOTAL_SECONDS = TOTAL_FRAMES / FPS


def sec(frame: int) -> str:
    return f"{frame / FPS:.6f}"


COMMON_CSS = r"""
  @font-face { font-family:"BL Zodiak"; src:url("assets/fonts/zodiak-700.woff2") format("woff2"); font-weight:700; }
  @font-face { font-family:"BL Supreme"; src:url("assets/fonts/supreme-400.woff2") format("woff2"); font-weight:400; }
  @font-face { font-family:"BL Supreme"; src:url("assets/fonts/supreme-500.woff2") format("woff2"); font-weight:500; }
  * { box-sizing:border-box; }
  #root { position:absolute; inset:0; width:1080px; height:1920px; overflow:hidden; background:#F5F0E6; color:#173530; font-family:"BL Supreme",Arial,sans-serif; }
  .identity { position:absolute; z-index:12; left:54px; top:50px; color:#F5F0E6; background:#173530; padding:14px 18px 12px; font:500 20px/1 "BL Supreme",Arial,sans-serif; letter-spacing:.13em; }
  .identity.paper { color:#173530; background:#F5F0E6; border:2px solid #173530; }
  .micro { font:500 22px/1.1 "BL Supreme",Arial,sans-serif; letter-spacing:.12em; text-transform:uppercase; }
  .display { font:700 96px/.94 "BL Zodiak",Georgia,serif; letter-spacing:-.045em; }
  .oxide { color:#B5482F; }
  .paper-bg { position:absolute; inset:0; background:#F5F0E6; }
  .grain { position:absolute; inset:0; pointer-events:none; opacity:.07; background-image:radial-gradient(#173530 0.65px,transparent 0.65px); background-size:14px 14px; }
  .caption-clear { position:absolute; left:0; right:0; top:1360px; bottom:0; pointer-events:none; }
"""


def comp_html(scene_id: str, duration: str, title: str, body: str, script: str, extra_css: str = "") -> str:
    return f"""<!doctype html>
<html><head><meta charset=\"utf-8\"><title>{title}</title></head><body><template>
<style>{COMMON_CSS}\n{extra_css}</style>
<div id=\"root\" data-composition-id=\"{scene_id}\" data-start=\"0\" data-duration=\"{duration}\" data-width=\"1080\" data-height=\"1920\" data-fps=\"24\">
{body}
</div>
<script>(() => {{
  const tl = gsap.timeline({{ paused:true }});
{script}
  window.__timelines = window.__timelines || {{}};
  window.__timelines[\"{scene_id}\"] = tl;
  tl.seek(0);
}})();</script>
</template></body></html>
"""


SCENES = {}

SCENES["scene-01-hook"] = comp_html(
    "scene-01-hook",
    sec(84),
    "The inn served the guest",
    r"""
  <video id="hook-film" class="clip" data-layout-allow-overflow src="assets/episode-r8.mp4" data-start="0" data-duration="3.500000" data-media-start="9.500000" muted playsinline></video>
  <div class="film-label"><span>THE MISSING RELATIONSHIP</span><i></i></div>
  <div id="email-proof" class="email-proof">
    <span>DIRECT EMAIL</span>
    <strong>—</strong>
  </div>
""",
    r"""  tl.fromTo("#hook-film", { scale:1.035, xPercent:0 }, { scale:1.085, xPercent:-1.5, duration:3.5, ease:"power1.inOut" }, 0);
  tl.fromTo(".film-label", { opacity:0, x:-24 }, { opacity:1, x:0, duration:.24, ease:"power3.out" }, .08);
  tl.fromTo("#email-proof", { opacity:0, x:30 }, { opacity:1, x:0, duration:.26, ease:"power3.out" }, 1.56);
  tl.fromTo("#email-proof strong", { scaleX:0 }, { scaleX:1, transformOrigin:"0% 50%", duration:.22, ease:"power3.out" }, 1.78);""",
    r"""
  #hook-film { position:absolute; inset:0; width:1080px; height:1920px; object-fit:cover; object-position:61% 50%; will-change:transform; }
  .film-label { position:absolute; left:54px; top:54px; display:flex; align-items:center; gap:14px; padding:15px 18px 13px; background:#173530; color:#F5F0E6; }
  .film-label span { font:500 21px/1 "BL Supreme",Arial,sans-serif; letter-spacing:.12em; }
  .film-label i { display:block; width:66px; height:4px; background:#FB8B69; }
  .email-proof { position:absolute; right:54px; top:250px; width:330px; padding:24px 26px; background:#F5F0E6; border:3px solid #173530; box-shadow:10px 10px 0 rgba(23,53,48,.18); }
  .email-proof span { display:block; color:#586D74; font:500 20px/1 "BL Supreme",Arial,sans-serif; letter-spacing:.11em; }
  .email-proof strong { display:block; margin-top:20px; color:#B5482F; font:700 62px/.7 "BL Zodiak",Georgia,serif; }
""",
)

SCENES["scene-02-transfer"] = comp_html(
    "scene-02-transfer",
    sec(71),
    "The guest book moved",
    r"""
  <div class="paper-bg"></div><div class="grain"></div>
  <div class="identity paper">THE OPERATOR ECONOMY</div>
  <div class="transfer-title"><span>THE GUEST BOOK</span><strong>MOVED</strong></div>
  <svg id="relationship" viewBox="0 0 1080 1150" aria-label="The guest book moves from the inn to the booking site">
    <g id="inn" class="building" transform="translate(80 390)">
      <path d="M0 150 L170 40 L340 150 M35 150 V385 H305 V150 M85 205 H135 V260 H85 Z M205 205 H255 V260 H205 Z M150 292 H205 V385" />
      <text x="170" y="445" text-anchor="middle">THE INN</text>
    </g>
    <path id="route" d="M390 610 C510 555 600 555 720 610" />
    <g id="site" class="building" transform="translate(730 390)">
      <path d="M0 150 L155 50 L310 150 M35 165 V385 H275 V165 M80 215 V385 M150 215 V385 M220 215 V385" />
      <text x="155" y="445" text-anchor="middle">BOOKING SITE</text>
    </g>
    <g id="book" transform="translate(260 655)">
      <path d="M0 0 C42 -25 88 -22 132 3 V165 C88 140 42 140 0 165 Z M132 3 C176 -22 222 -25 264 0 V165 C222 140 176 140 132 165 Z" />
      <path class="accent" d="M132 3 V165" />
      <text x="132" y="215" text-anchor="middle">GUEST BOOK</text>
    </g>
  </svg>
  <div id="ownership" class="ownership">RELATIONSHIP HELD HERE</div>
""",
    r"""  tl.fromTo(".transfer-title span", { opacity:0, y:22 }, { opacity:1, y:0, duration:.22, ease:"power3.out" }, .02);
  tl.fromTo(".transfer-title strong", { opacity:0, x:26 }, { opacity:1, x:0, duration:.24, ease:"power3.out" }, .15);
  tl.fromTo("#route", { strokeDasharray:520, strokeDashoffset:520 }, { strokeDashoffset:0, duration:.58, ease:"power2.inOut" }, .35);
  tl.fromTo("#book", { x:0 }, { x:495, duration:1.38, ease:"power3.inOut" }, .58);
  tl.fromTo("#ownership", { opacity:0, y:16 }, { opacity:1, y:0, duration:.22, ease:"power3.out" }, 2.12);""",
    r"""
  .transfer-title { position:absolute; left:64px; top:190px; right:64px; display:flex; align-items:baseline; justify-content:space-between; }
  .transfer-title span { color:#586D74; font:500 26px/1 "BL Supreme",Arial,sans-serif; letter-spacing:.12em; }
  .transfer-title strong { color:#B5482F; font:700 92px/.9 "BL Zodiak",Georgia,serif; letter-spacing:-.04em; }
  #relationship { position:absolute; left:0; top:240px; width:1080px; height:1120px; overflow:visible; }
  #relationship path { fill:none; stroke:#173530; stroke-width:6; stroke-linecap:round; stroke-linejoin:round; }
  #relationship .accent { stroke:#B5482F; stroke-width:9; }
  #relationship text { fill:#173530; font:500 28px/1 "BL Supreme",Arial,sans-serif; letter-spacing:.09em; }
  #route { fill:none; stroke:#586D74 !important; stroke-width:5 !important; }
  #book path { fill:#F5F0E6; }
  .ownership { position:absolute; left:630px; top:1110px; width:390px; padding:20px; color:#F5F0E6; background:#B5482F; text-align:center; font:500 25px/1 "BL Supreme",Arial,sans-serif; letter-spacing:.08em; }
""",
)

SCENES["scene-03-constraint"] = comp_html(
    "scene-03-constraint",
    sec(111),
    "Constraint before tool",
    r"""
  <div class="paper-bg"></div><div class="grain"></div>
  <div class="identity paper">THE OPERATOR ECONOMY</div>
  <div class="order-label">ORDER OF OPERATIONS</div>
  <h1>Before the tool,<br><em>there is a constraint.</em></h1>
  <div class="order-stack">
    <div id="constraint-block" class="order-block constraint-block">
      <span>01</span><strong>DESIGN CONSTRAINT</strong>
    </div>
    <div id="order-path" class="order-path"><i></i><b>THEN</b></div>
    <div id="tool-block" class="order-block tool-block">
      <span>02</span><strong>EMAIL TOOL</strong>
    </div>
  </div>
""",
    r"""  tl.fromTo(".order-label", { opacity:0, y:18 }, { opacity:1, y:0, duration:.22, ease:"power3.out" }, .04);
  tl.fromTo("h1", { opacity:0, y:30 }, { opacity:1, y:0, duration:.3, ease:"power3.out" }, .18);
  tl.fromTo("#constraint-block", { opacity:0, x:-42 }, { opacity:1, x:0, duration:.32, ease:"power3.out" }, .72);
  tl.fromTo("#order-path i", { scaleY:0 }, { scaleY:1, transformOrigin:"50% 0%", duration:.42, ease:"power2.inOut" }, 1.52);
  tl.fromTo("#order-path b", { opacity:0 }, { opacity:1, duration:.18, ease:"power2.out" }, 1.78);
  tl.fromTo("#tool-block", { opacity:0, y:32 }, { opacity:.34, y:0, duration:.3, ease:"power3.out" }, 2.08);""",
    r"""
  .order-label { position:absolute; left:64px; top:220px; color:#586D74; font:500 25px/1 "BL Supreme",Arial,sans-serif; letter-spacing:.13em; }
  h1 { position:absolute; left:64px; right:64px; top:330px; color:#173530; font:700 88px/.94 "BL Zodiak",Georgia,serif; letter-spacing:-.045em; }
  h1 em { color:#B5482F; font-style:normal; }
  .order-stack { position:absolute; left:64px; right:64px; top:690px; height:600px; }
  .order-block { position:absolute; left:0; right:0; height:188px; display:grid; grid-template-columns:116px 1fr; align-items:center; border:4px solid #173530; background:#F5F0E6; }
  .order-block span { display:grid; place-items:center; align-self:stretch; color:#F5F0E6; background:#173530; font:500 42px/1 "BL Supreme",Arial,sans-serif; }
  .order-block strong { padding-left:38px; color:#173530; font:500 45px/1 "BL Supreme",Arial,sans-serif; letter-spacing:.055em; }
  .constraint-block { top:0; border-color:#B5482F; }
  .constraint-block span { background:#B5482F; }
  .constraint-block strong { color:#B5482F; }
  .order-path { position:absolute; left:50%; top:188px; width:100px; height:180px; transform:translateX(-50%); display:flex; flex-direction:column; align-items:center; }
  .order-path i { width:6px; height:118px; background:#173530; }
  .order-path i::after { content:""; position:absolute; left:38px; top:100px; width:22px; height:22px; border-right:6px solid #173530; border-bottom:6px solid #173530; transform:rotate(45deg); }
  .order-path b { margin-top:22px; color:#586D74; font:500 18px/1 "BL Supreme",Arial,sans-serif; letter-spacing:.13em; }
  .tool-block { top:368px; }
""",
)

SCENES["scene-04-boundary"] = comp_html(
    "scene-04-boundary",
    sec(147),
    "Relay and site-rule boundary",
    r"""
  <div class="paper-bg"></div><div class="grain"></div>
  <div class="identity paper">THE OPERATOR ECONOMY</div>
  <div class="boundary-title"><span>THE ADDRESS LOOKS USABLE.</span><strong>IT ISN'T YOUR LIST.</strong></div>
  <div class="relay-card">
    <span>PLATFORM RELAY · ILLUSTRATIVE</span>
    <strong>k7m2q9x4@guest.booking.com</strong>
  </div>
  <div class="route-attempt">
    <div class="inn-chip">INN</div>
    <div id="attempt-line"><i></i></div>
    <div id="stop-gate"><span>SITE-RULE<br>BOUNDARY</span></div>
    <div class="send-chip">MARKETING<br>MESSAGE</div>
  </div>
  <div id="rule-note" class="rule-note">DO NOT ROUTE AROUND THE PLATFORM RELATIONSHIP</div>
""",
    r"""  tl.fromTo(".boundary-title", { opacity:0, y:26 }, { opacity:1, y:0, duration:.28, ease:"power3.out" }, .04);
  tl.fromTo(".relay-card", { opacity:0, y:26 }, { opacity:1, y:0, duration:.3, ease:"power3.out" }, .32);
  tl.fromTo("#attempt-line i", { scaleX:0 }, { scaleX:1, transformOrigin:"0% 50%", duration:.78, ease:"power2.inOut" }, 1.08);
  tl.fromTo("#stop-gate", { scaleY:0 }, { scaleY:1, transformOrigin:"50% 100%", duration:.25, ease:"power3.out" }, 1.66);
  tl.fromTo(".send-chip", { opacity:.18 }, { opacity:.42, duration:.2, ease:"power2.out" }, 1.88);
  tl.fromTo("#rule-note", { opacity:0, y:18 }, { opacity:1, y:0, duration:.24, ease:"power3.out" }, 3.12);""",
    r"""
  .boundary-title { position:absolute; left:64px; right:64px; top:175px; }
  .boundary-title span { display:block; color:#586D74; font:500 24px/1 "BL Supreme",Arial,sans-serif; letter-spacing:.1em; }
  .boundary-title strong { display:block; margin-top:18px; color:#173530; font:700 86px/.95 "BL Zodiak",Georgia,serif; letter-spacing:-.04em; }
  .relay-card { position:absolute; left:64px; right:64px; top:500px; padding:34px 30px 38px; border:4px solid #173530; background:#F5F0E6; }
  .relay-card span { display:block; color:#586D74; font:500 20px/1 "BL Supreme",Arial,sans-serif; letter-spacing:.1em; }
  .relay-card strong { display:block; margin-top:22px; color:#173530; font:500 37px/1.08 ui-monospace,SFMono-Regular,Menlo,monospace; letter-spacing:-.02em; overflow-wrap:anywhere; }
  .route-attempt { position:absolute; left:64px; right:64px; top:805px; height:320px; display:grid; grid-template-columns:135px 1fr 120px 195px; gap:14px; align-items:center; }
  .inn-chip,.send-chip { display:grid; place-items:center; min-height:118px; padding:14px 10px; border:3px solid #173530; color:#173530; background:#F5F0E6; text-align:center; font:500 22px/1.1 "BL Supreme",Arial,sans-serif; letter-spacing:.055em; }
  #attempt-line { height:8px; background:#D8CFB9; overflow:hidden; }
  #attempt-line i { display:block; width:100%; height:100%; background:#173530; }
  #stop-gate { height:260px; border-left:12px solid #B5482F; display:grid; place-items:center; }
  #stop-gate span { color:#B5482F; font:500 18px/1.2 "BL Supreme",Arial,sans-serif; letter-spacing:.055em; text-align:center; transform:rotate(-90deg); white-space:nowrap; }
  .rule-note { position:absolute; left:64px; right:64px; top:1150px; padding:24px; background:#B5482F; color:#F5F0E6; text-align:center; font:500 25px/1.15 "BL Supreme",Arial,sans-serif; letter-spacing:.065em; }
""",
)

SCENES["scene-05-no-tool"] = comp_html(
    "scene-05-no-tool",
    sec(72),
    "Not an email tool",
    r"""
  <div class="paper-bg"></div><div class="grain"></div>
  <div class="identity paper">THE OPERATOR ECONOMY</div>
  <div class="step-label">THE FIRST STEP</div>
  <div id="tool-card" class="tool-card">
    <div class="mail-icon"><span></span><i></i></div>
    <strong>EMAIL TOOL</strong>
  </div>
  <div id="not-first" class="not-first">NOT FIRST</div>
  <div id="unknown-slot" class="unknown-slot"><span>WHAT COMES FIRST?</span><b>?</b></div>
""",
    r"""  tl.fromTo(".step-label", { opacity:0, y:18 }, { opacity:1, y:0, duration:.22, ease:"power3.out" }, .03);
  tl.fromTo("#tool-card", { opacity:0, x:32 }, { opacity:1, x:0, duration:.26, ease:"power3.out" }, .18);
  tl.fromTo("#not-first", { opacity:0, scale:1.35, rotate:-7 }, { opacity:1, scale:1, rotate:-4, duration:.24, ease:"power4.out" }, 1.12);
  tl.to("#tool-card", { x:-300, opacity:.18, duration:.28, ease:"power3.in" }, 1.52);
  tl.fromTo("#unknown-slot", { opacity:0, x:55 }, { opacity:1, x:0, duration:.3, ease:"power3.out" }, 1.82);""",
    r"""
  .step-label { position:absolute; left:64px; top:210px; color:#586D74; font:500 26px/1 "BL Supreme",Arial,sans-serif; letter-spacing:.13em; }
  .tool-card { position:absolute; left:120px; top:465px; width:840px; height:520px; display:flex; flex-direction:column; justify-content:center; align-items:center; gap:50px; border:5px solid #173530; background:#F5F0E6; }
  .tool-card strong { color:#173530; font:700 82px/.95 "BL Zodiak",Georgia,serif; letter-spacing:-.04em; }
  .mail-icon { position:relative; width:260px; height:170px; border:7px solid #173530; }
  .mail-icon span,.mail-icon i { position:absolute; left:14px; right:14px; top:34px; height:7px; background:#173530; transform-origin:50% 50%; }
  .mail-icon span { transform:rotate(31deg); } .mail-icon i { transform:rotate(-31deg); }
  .not-first { position:absolute; left:310px; top:890px; z-index:4; padding:24px 38px; background:#B5482F; color:#F5F0E6; font:500 54px/1 "BL Supreme",Arial,sans-serif; letter-spacing:.06em; }
  .unknown-slot { position:absolute; left:180px; right:180px; top:520px; height:430px; display:grid; place-items:center; border:5px dashed #B5482F; background:#F5F0E6; text-align:center; }
  .unknown-slot span { align-self:end; color:#586D74; font:500 30px/1 "BL Supreme",Arial,sans-serif; letter-spacing:.1em; }
  .unknown-slot b { align-self:start; color:#B5482F; font:700 180px/.8 "BL Zodiak",Georgia,serif; }
""",
)

SCENES["scene-06-cta"] = comp_html(
    "scene-06-cta",
    sec(CTA_FRAMES),
    "What has to come first",
    r"""
  <div class="cta-bg"></div><div class="cta-accent"></div>
  <div class="cta-id">THE OPERATOR ECONOMY · EP009</div>
  <div class="cta-copy">
    <h1 id="cta-question">What has to<br>come first?</h1>
    <p id="cta-answer">The full answer in EP009</p>
    <div class="related-link-panel"><span id="related-link-label">Tap the related video</span><b id="related-link-arrow">↗</b></div>
  </div>
""",
    r"""  tl.fromTo(".cta-accent", { scaleY:0 }, { scaleY:1, transformOrigin:"50% 100%", duration:.24, ease:"power3.out" }, 0);
  tl.fromTo("#cta-question", { opacity:0, x:34 }, { opacity:1, x:0, duration:.28, ease:"power3.out" }, .08);
  tl.fromTo("#cta-answer", { opacity:0, y:20 }, { opacity:1, y:0, duration:.24, ease:"power3.out" }, .42);
  tl.fromTo("#related-link-label", { opacity:0, y:16 }, { opacity:1, y:0, duration:.24, ease:"power3.out" }, .66);
  tl.fromTo("#related-link-arrow", { opacity:0, x:-10 }, { opacity:1, x:0, duration:.22, ease:"power3.out" }, .82);""",
    r"""
  .cta-bg { position:absolute; inset:0; background:#173530; }
  .cta-accent { position:absolute; left:0; top:0; bottom:0; width:26px; background:#FB8B69; }
  .cta-id { position:absolute; left:74px; top:72px; color:#D8CFB9; font:500 22px/1 "BL Supreme",Arial,sans-serif; letter-spacing:.12em; }
  .cta-copy { position:absolute; left:74px; right:74px; top:350px; }
  .cta-copy h1 { color:#F5F0E6; font:700 132px/.9 "BL Zodiak",Georgia,serif; letter-spacing:-.05em; }
  .cta-copy p { margin-top:76px; color:#D8CFB9; font:500 38px/1.1 "BL Supreme",Arial,sans-serif; letter-spacing:.025em; }
  .related-link-panel { margin-top:42px; height:112px; padding:0 30px; display:grid; grid-template-columns:1fr auto; align-items:center; color:#173530; background:#FB8B69; font:500 38px/1 "BL Supreme",Arial,sans-serif; }
  .related-link-panel b { color:#173530; font:500 62px/1 "BL Supreme",Arial,sans-serif; }
""",
)


CAPTIONS = [
    {"id":"cap-01","start":0.000,"end":1.570,"text":"The inn served the guest"},
    {"id":"cap-02","start":1.570,"end":3.500,"text":"and doesn't have his email."},
    {"id":"cap-03","start":3.520,"end":5.340,"text":"So the guest book now lives"},
    {"id":"cap-04","start":5.340,"end":6.458333,"text":"at the booking site."},
    {"id":"cap-05","start":6.458333,"end":8.258333,"text":"Which means the recovery job"},
    {"id":"cap-06","start":8.318333,"end":10.138333,"text":"has a design constraint before"},
    {"id":"cap-07","start":10.198333,"end":11.078333,"text":"it has a tool."},
    {"id":"cap-08","start":11.118333,"end":12.418333,"text":"You can't win a guest back"},
    {"id":"cap-09","start":12.458333,"end":13.488333,"text":"from a relay address,"},
    {"id":"cap-10","start":13.858333,"end":15.298333,"text":"and under the site's rules"},
    {"id":"cap-11","start":15.338333,"end":17.178333,"text":"you're not supposed to try."},
    {"id":"cap-12","start":17.218333,"end":18.618333,"text":"What the inn needs first"},
    {"id":"cap-13","start":18.978333,"end":20.198333,"text":"isn't an email tool."},
]


def make_index() -> str:
    hosts = []
    scene_ids = list(SCENES)
    all_frames = [84, 71, 111, 147, 72, CTA_FRAMES]
    at = 0
    for idx, (scene_id, frames) in enumerate(zip(scene_ids, all_frames), 1):
        hosts.append(
            f'<div id="host-{scene_id}" class="clip scene-host" data-composition-id="{scene_id}" '
            f'data-composition-src="compositions/{scene_id}.html" data-start="{sec(at)}" '
            f'data-duration="{sec(frames)}" data-track-index="0"></div>'
        )
        at += frames

    audios = []
    for segment in SEGMENTS:
        audios.append(
            f'<audio id="audio-{segment["id"]}" class="clip" src="assets/episode-r8.mp4" '
            f'data-start="{sec(segment["timeline_in_frame"])}" data-duration="{sec(segment["frame_count"])}" '
            f'data-media-start="{sec(segment["source_in_frame"])}" data-track-index="10"></audio>'
        )

    captions = []
    emphasis = {"guest book", "booking site", "constraint", "relay address", "site's rules", "email tool"}
    for c in CAPTIONS:
        rendered = c["text"]
        for phrase in sorted(emphasis, key=len, reverse=True):
            rendered = rendered.replace(phrase, f'<span class="em">{phrase}</span>')
        captions.append(
            f'<p id="{c["id"]}" class="clip caption" data-caption-layer="fg" '
            f'data-start="{c["start"]:.6f}" data-duration="{c["end"]-c["start"]:.6f}" '
            f'data-track-index="20">{rendered}</p>'
        )

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=1080, height=1920" />
  <script src="assets/vendor/gsap.min.js"></script>
  <style>
    @font-face {{ font-family:"BL Supreme"; src:url("assets/fonts/supreme-400.woff2") format("woff2"); font-weight:400; }}
    @font-face {{ font-family:"BL Supreme"; src:url("assets/fonts/supreme-500.woff2") format("woff2"); font-weight:500; }}
    * {{ box-sizing:border-box; margin:0; padding:0; }}
    html,body {{ width:1080px; height:1920px; overflow:hidden; background:#173530; }}
    #root {{ position:relative; width:1080px; height:1920px; overflow:hidden; font-family:"BL Supreme",Arial,sans-serif; }}
    .scene-host {{ position:absolute; inset:0; width:1080px; height:1920px; overflow:hidden; will-change:transform; }}
    .caption {{ position:absolute; z-index:40; left:70px; top:1410px; width:860px; min-height:112px; padding:21px 28px 23px; background:#173530; color:#F5F0E6; border-left:9px solid #FB8B69; font:500 64px/1.02 "BL Supreme",Arial,sans-serif; letter-spacing:-.025em; box-shadow:0 12px 30px rgba(25,32,31,.18); }}
    .caption .em {{ color:#FB8B69; }}
  </style>
</head>
<body>
  <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL_SECONDS:.6f}" data-width="1080" data-height="1920" data-fps="24">
    {''.join(hosts)}
    {''.join(audios)}
    {''.join(captions)}
  </div>
  <script>
    window.__timelines = window.__timelines || {{}};
    const tl = gsap.timeline({{ paused:true }});
    window.__timelines["main"] = tl;
    // <seams:auto>
    // seam-stamp writes deterministic current-matched host motion here.
    // </seams:auto>
    tl.seek(0);
  </script>
</body>
</html>
"""


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def write_json(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload, indent=2) + "\n")


def main() -> None:
    (ROOT / "compositions").mkdir(parents=True, exist_ok=True)
    for scene_id, html in SCENES.items():
        (ROOT / "compositions" / f"{scene_id}.html").write_text(html)

    (ROOT / "index.html").write_text(make_index())

    write_json(
        ROOT / "captions.json",
        {
            "schema": "oe-ep009-short-caption-groups-v2",
            "fps": FPS,
            "font_px": 64,
            "bounds": {"x": 70, "y": 1410, "width": 860},
            "groups": CAPTIONS,
        },
    )

    write_json(
        ROOT / "SOURCE-EDL.json",
        {
            "schema": "oe-ep009-short-hook-edl-v1",
            "status": "private_review_source",
            "episode": "EP009-direct-booking-recovery",
            "candidate": "EP009-SHORT-03-guest-book-hook",
            "fps": FPS,
            "output": {"width": 1080, "height": 1920, "frame_count": TOTAL_FRAMES, "duration_seconds": TOTAL_SECONDS},
            "carrier": {
                "path": "assets/episode-r8.mp4",
                "sha256": sha256(ROOT / "assets" / "episode-r8.mp4"),
            },
            "edit_policy": {
                "narration": "whole locked phrases reordered; no word rewrite",
                "visuals": "locked hospitality film plus native portrait relationship graphics",
                "withheld_payoff": "permissioned first-party guest book and front-desk operating job",
                "related_video": "release dependency; not attached by this private build",
            },
            "segments": SEGMENTS,
            "cta": {
                "timeline_in_frame": CTA_IN_FRAME,
                "timeline_out_frame_exclusive": TOTAL_FRAMES,
                "text": ["What has to come first?", "The full answer in EP009", "Tap the related video"],
            },
        },
    )

    write_json(
        ROOT / "SOURCE-CONTRACT.json",
        {
            "schema": "oe-ep009-short-hook-source-contract-v1",
            "status": "private_review_not_release_approved",
            "source_edl": "SOURCE-EDL.json",
            "locked_carrier_sha256": sha256(ROOT / "assets" / "episode-r8.mp4"),
            "constraints": [
                "No narration rewrite.",
                "Relay-address restriction remains explicitly qualified as the site's rules.",
                "The permissioned guest-book fix and front-desk job are withheld for the full episode.",
                "Related Video attachment is mandatory before any release CTA can be truthful.",
                "No upload or publication is authorized by this build.",
            ],
        },
    )


if __name__ == "__main__":
    main()
