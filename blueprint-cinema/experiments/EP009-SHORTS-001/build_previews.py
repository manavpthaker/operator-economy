#!/usr/bin/env python3
"""Build the four EP009 portrait review compositions from the locked r8 carrier.

This script writes deterministic HyperFrames source only. It does not render,
publish, mutate the locked long-form carrier, or claim Short approval.
"""

from __future__ import annotations

import hashlib
import html
import json
import os
import shutil
from dataclasses import dataclass
from pathlib import Path


REPO = Path(__file__).resolve().parents[3]
ROOT = Path(__file__).resolve().parent
MAP_PATH = REPO / "blueprint-cinema/episodes/EP009-direct-booking-recovery/agents/deliverables/ep009-shorts-editorial-map/shorts-map.json"
TRANSCRIPT_PATH = REPO / "blueprint-cinema/experiments/EP009-FULL-BUILD-001/assembly/r3/word-transcript-r3.json"
CARRIER_PATH = REPO / "blueprint-cinema/experiments/EP009-FULL-BUILD-001/assembly/qa/r8-tool-clarity/ep009-r8-tool-clarity-review-r1.mp4"
LOCK_PATH = REPO / "blueprint-cinema/experiments/EP009-FULL-BUILD-001/assembly/r8-tool-clarity/FINAL-EPISODE-LOCK-r8.json"
FONT_DIR = REPO / "design-system/boundary-ledger/fonts"

EXPECTED = {
    MAP_PATH: "378037269b14a198fe21771536b29d7701f9ff862df0ffe4ce715f8e43058fe0",
    TRANSCRIPT_PATH: "0b5175dea2cbb1ac7682cd69b9ab032bc8c544131aae82575140e90ae0d76709",
    CARRIER_PATH: "cc5805a990d10812b5349568e50a74dc0e21b09ed402b49250f9796640ed710e",
    LOCK_PATH: "b9d107718c0d760e388c1a5167bcaf7e06ebfb29504ed469fac385aa2aa54cd2",
}


@dataclass(frozen=True)
class Scene:
    source_in: float
    source_out: float
    layout: str
    focus_x: int = 50
    focus_y: int = 50
    label: str = ""


PROJECTS = {
    "EP009-SHORT-01-second-commission": {
        "dir": "01-second-commission",
        "title": "The second commission",
        "emphasis": {"innkeeper", "relay", "commission", "arithmetic", "cost"},
        "scenes": [
            Scene(0.0, 3.583333, "presenter", 50, 42, "presenter open"),
            Scene(3.583333, 10.5, "film_context", 51, 49, "checkout and departure"),
            Scene(10.5, 16.833333, "film_center", 54, 54, "thank-you attempt"),
            Scene(16.833333, 22.75, "native_relay_address", label="relay address"),
            Scene(22.75, 27.5, "native_relay_expires", label="relay expires"),
            Scene(27.5, 32.041667, "native_repeat_booking", label="repeat booking"),
            Scene(32.041667, 36.333333, "native_repeat_commission", label="second commission"),
            Scene(36.333333, 40.083333, "film_right", 52, 47, "recognition"),
            Scene(40.083333, 50.291667, "native_service_arithmetic", label="service and arithmetic"),
            Scene(50.291667, 59.458333, "presenter", 50, 43, "presenter question"),
        ],
    },
    "EP009-SHORT-02-machine-versus-judgment": {
        "dir": "02-machine-versus-judgment",
        "title": "What the machine does",
        "emphasis": {"machine", "software", "drafts", "schedules", "hospitality"},
        "embed_until": 3.541667,
        "disclosure": "FICTIONAL FIXTURE · HUMAN-REVIEW DRAFT · NO SEND",
        "scenes": [
            Scene(692.458333, 696.0, "thesis", 50, 48, "What does the machine do, then, and what do you do?"),
            Scene(696.0, 698.0, "film_center", 52, 54, "operator at laptop"),
            Scene(698.0, 702.25, "context_focus", 58, 42, "Node-RED request path"),
            Scene(702.25, 708.875, "context_focus", 46, 55, "returned draft and queue"),
            Scene(708.875, 712.958333, "context_focus", 51, 55, "human edit"),
        ],
    },
    "EP009-SHORT-03-guest-book": {
        "dir": "03-guest-book",
        "title": "The guest book moved",
        "emphasis": {"guest", "book", "booking", "constraint", "relay", "chooses"},
        "scenes": [
            Scene(336.25, 339.041667, "native_guest_book_site", label="guest book at booking site"),
            Scene(339.041667, 345.0, "native_inn_no_email", label="inn without direct email"),
            Scene(345.0, 350.0, "native_constraint", label="constraint before tool"),
            Scene(350.0, 356.0, "native_relay_boundary", label="relay rule boundary"),
            Scene(356.0, 362.0, "native_own_guest_book", label="own guest book"),
            Scene(362.0, 365.0, "native_guest_chooses", label="guest chooses to sign"),
            Scene(365.0, 368.0, "native_fair_question", label="fair question"),
            Scene(368.0, 369.833333, "presenter", 50, 43, "presenter question"),
        ],
    },
    "EP009-SHORT-04-wrong-number": {
        "dir": "04-wrong-number",
        "title": "The commission number is wrong",
        "emphasis": {"commission", "eighteen", "twenty", "wrong", "shift"},
        "scenes": [
            Scene(506.25, 512.0, "native_commission_band", label="commission band"),
            Scene(512.0, 516.5, "native_annual_commission", label="annual commission"),
            Scene(516.5, 520.416667, "native_wrong_number", label="old argument stops"),
            Scene(520.416667, 528.75, "presenter", 50, 43, "presenter correction"),
        ],
    },
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def verify_inputs() -> None:
    for path, expected in EXPECTED.items():
        actual = sha256(path)
        if actual != expected:
            raise SystemExit(f"input hash mismatch: {path}\nexpected {expected}\nactual   {actual}")


def index_by_id(words: list[dict]) -> dict[str, int]:
    return {w["w_id"]: i for i, w in enumerate(words)}


def caption_groups(candidate: dict, words: list[dict]) -> list[dict]:
    by_id = index_by_id(words)
    first = by_id[candidate["first_word"]["id"]]
    last = by_id[candidate["last_word"]["id"]]
    subset = words[first : last + 1]
    raw: list[list[dict]] = []
    group: list[dict] = []
    for i, word in enumerate(subset):
        group.append(word)
        token = word["token"]
        next_word = subset[i + 1] if i + 1 < len(subset) else None
        gap = (next_word["start"] - word["end"]) if next_word else 9.0
        duration = word["end"] - group[0]["start"]
        boundary = (
            token.endswith((".", "?", "!"))
            or gap >= 0.5
            or (token.endswith(",") and gap >= 0.25)
            or len(group) >= 6
            or duration >= 2.5
        )
        if boundary:
            raw.append(group)
            group = []
    if group:
        raw.append(group)

    # Avoid one-word flashes by merging them into the adjacent phrase.
    merged: list[list[dict]] = []
    for group in raw:
        if len(group) == 1 and merged and len(merged[-1]) < 8:
            merged[-1].extend(group)
        else:
            merged.append(group)

    source_start = candidate["source_cut"]["start_seconds"]
    total = candidate["source_cut"]["duration_seconds"]
    starts = [max(0.0, g[0]["start"] - source_start - 0.08) for g in merged]
    ends: list[float] = []
    for i, group in enumerate(merged):
        if i + 1 < len(merged):
            next_first = merged[i + 1][0]["start"]
            boundary = ((group[-1]["end"] + next_first) / 2) - source_start
            ends.append(max(starts[i] + 0.5, min(total, boundary)))
            starts[i + 1] = max(starts[i + 1], ends[-1])
        else:
            ends.append(total)

    result = []
    for i, (group, start, end) in enumerate(zip(merged, starts, ends)):
        result.append(
            {
                "id": f"cap-{i:03d}",
                "start": round(start, 6),
                "end": round(end, 6),
                "duration": round(end - start, 6),
                "text": " ".join(w["token"] for w in group),
                "words": [
                    {
                        "id": w["w_id"],
                        "token": w["token"],
                        "start": round(w["start"] - source_start, 6),
                        "end": round(w["end"] - source_start, 6),
                    }
                    for w in group
                ],
            }
        )
    return result


def emphasized_text(text: str, emphasis: set[str]) -> str:
    tokens = text.split(" ")
    out = []
    for token in tokens:
        normalized = token.lower().strip(".,?!:;\"'()")
        safe = html.escape(token)
        if normalized in emphasis:
            out.append(f'<span class="em">{safe}</span>')
        else:
            out.append(safe)
    return " ".join(out)


def write_assets(project: Path) -> None:
    assets = project / "assets"
    fonts = assets / "fonts"
    fonts.mkdir(parents=True, exist_ok=True)
    media_link = assets / "episode-r8.mp4"
    if media_link.exists() or media_link.is_symlink():
        media_link.unlink()
    media_link.symlink_to(Path(os.path.relpath(CARRIER_PATH, media_link.parent)))
    for name in ["boska-700.woff2", "zodiak-700.woff2", "supreme-400.woff2", "supreme-500.woff2"]:
        shutil.copy2(FONT_DIR / name, fonts / name)


def write_brief(project: Path, candidate: dict, spec: dict) -> None:
    duration = candidate["source_cut"]["duration_seconds"]
    brief = f'''---
workflow: general-video
flow: automation
storyboard: no
message: "{candidate['curiosity_gap']}"
destination: youtube-shorts
aspect: 1080x1920
language: en
audience: "Independent operators and small hospitality owners"
length: {duration:.3f}s
angle: "Locked long-form excerpt"
---

## Intent

Create a phone-readable 9:16 excerpt from the owner-locked EP009 r8 episode. Preserve the exact
narration and causal order while recomposing the existing picture into a portrait context-and-focus
layout. The result is a private review composition, not an accepted or published Short.

## Assets

- `assets/episode-r8.mp4` — symlink to the exact locked r8 carrier; picture and audio source.
- `captions.json` — verbatim groups derived from `{candidate['first_word']['id']}` through `{candidate['last_word']['id']}`.

## Customizations

- Quiet Boundary Ledger caption rail in the lower-middle phone-safe zone.
- Full-context plus focused-detail panels whenever a blind crop would hide decisive evidence.

## Notes

- Exact source frames: `[{candidate['source_cut']['in_frame']}, {candidate['source_cut']['out_frame_exclusive']})` at 24 fps.
- Do not add claims, rewrite speech, fabricate software UI, generate presenter performance, upload, or publish.
- Final MP4 render remains gated on owner preview approval.
'''
    (project / "BRIEF.md").write_text(brief)

    frame = '''---
name: EP009 portrait Boundary Ledger
canvas: "1080x1920"
background: "#F5F0E6"
foreground: "#19201F"
accent: "#B5482F"
secondary: "#586D74"
display_font: "BL Zodiak"
body_font: "BL Supreme"
---

# Portrait direction

Warm paper holds human context. Deep mineral carries accountable text. Steel marks the current
dependency and oxide appears only at the active focus edge. The source picture keeps its pixels;
portrait adaptation comes from authored context and focus windows, never a blind crop.

The caption rail is verbatim, restrained, and lower-middle safe. The scene changes only when the
locked source changes or when the viewer needs a readable focus view. No ambient motion, glow,
gradient, or decorative loop.
'''
    (project / "frame.md").write_text(frame)


def scene_local_bounds(scene: Scene, source_start: float, total: float) -> tuple[float, float]:
    local_start = max(0.0, scene.source_in - source_start)
    local_end = min(total, scene.source_out - source_start)
    return round(local_start, 6), round(local_end, 6)


def write_storyboard(project: Path, candidate: dict, spec: dict) -> list[tuple[Scene, float, float]]:
    source_start = candidate["source_cut"]["start_seconds"]
    total = candidate["source_cut"]["duration_seconds"]
    usable = []
    blocks = []
    for i, scene in enumerate(spec["scenes"], 1):
        start, end = scene_local_bounds(scene, source_start, total)
        if end <= start:
            continue
        usable.append((scene, start, end))
        rule = "hyperframes-animation/rules/coordinate-target-zoom.md" if scene.layout == "context_focus" else "hyperframes-core/references/creator-editing-recipes.md#trim-in-out"
        blocks.append(
            f'''## Frame {i:02d}

- status: outline
- src: `compositions/frame-{i:02d}.html`
- timing: `{start:.6f}s–{end:.6f}s`
- source: `{scene.source_in:.6f}s–{scene.source_out:.6f}s` from locked r8
- shape: `{scene.layout}`
- citation: `{rule}`
- beat: {scene.label}; preserve the locked action and direct attention to its accountable detail.
'''
        )
    board = f'''---
mode: autonomous
workflow: general-video
message: "{candidate['curiosity_gap']}"
audience: "Independent operators and small hospitality owners"
aspect: 1080x1920
duration: {total:.6f}
fps: 24
---

# {spec['title']}

The viewer enters the locked excerpt immediately, retains enough full-frame context to understand
each shot, and receives one readable focus window when the long-form frame is too wide for a phone.
Hard cuts preserve source causality. The quiet caption rail carries the exact voice.

{''.join(blocks)}'''
    (project / "STORYBOARD.md").write_text(board)
    return usable


def native_diagram_html(sid: str, layout: str) -> tuple[str, str]:
    diagrams = {
        "native_relay_address": (
            "RESERVATION EMAIL",
            "It isn't his.",
            '''
      <div class="evidence-card native-reveal">
        <div class="field-label">EMAIL ON THE RESERVATION</div>
        <div class="mono-value">k7m2q9x4@<br>guest.booking.com</div>
        <div class="tag oxide">RELAY</div>
      </div>''',
        ),
        "native_relay_expires": (
            "A WEEK OR SO AFTER CHECKOUT",
            "The relay stops working.",
            '''
      <div class="flow-row native-reveal">
        <div class="node"><span>THE INN</span></div>
        <div class="route broken"><span>RELAY</span></div>
        <div class="node"><span>GUEST</span></div>
      </div>
      <div class="status-line native-reveal"><span class="status-dot"></span> CONNECTION ENDS</div>''',
        ),
        "native_repeat_booking": (
            "A YEAR LATER",
            "Same guest. Same room. Same site.",
            '''
      <div class="flow-stack native-reveal">
        <div class="node wide"><span>GUEST</span></div><div class="down-arrow">↓</div>
        <div class="node active wide"><span>BOOKING SITE</span></div><div class="down-arrow">↓</div>
        <div class="node wide"><span>INN · SAME ROOM</span></div>
      </div>''',
        ),
        "native_repeat_commission": (
            "SAME GUEST · SAME ROOM",
            "The commission repeats.",
            '''
      <div class="stay-grid native-reveal">
        <div class="stay-card"><span>FIRST STAY</span><strong>COMMISSION</strong></div>
        <div class="equals">=</div>
        <div class="stay-card active"><span>SECOND STAY</span><strong>COMMISSION</strong></div>
      </div>''',
        ),
        "native_service_arithmetic": (
            "SECOND COMMISSION",
            "A service is hiding inside it.",
            '''
      <div class="ledger-stack">
        <div class="ledger-row native-reveal"><span>01</span><strong>A SERVICE</strong><small>hiding inside it</small></div>
        <div class="ledger-row native-reveal"><span>02</span><strong>ONE PIECE OF ARITHMETIC</strong><small>decides whether it is</small></div>
        <div class="question-box native-reveal">WORTH YOUR TIME?</div>
      </div>''',
        ),
        "native_guest_book_site": (
            "THE DEPENDENCY",
            "The guest book moved.",
            '''
      <div class="site-card native-reveal">
        <div class="building-mark">▥</div><strong>BOOKING SITE</strong>
        <div class="book-card"><span class="book-mark">▤</span><span>GUEST BOOK</span></div>
      </div>''',
        ),
        "native_inn_no_email": (
            "THE INN SERVED THE GUEST",
            "The site holds the email.",
            '''
      <div class="split-world native-reveal">
        <div class="world-card"><strong>INN + GUEST</strong><span class="no-email">NO DIRECT EMAIL</span></div>
        <div class="rule-boundary"></div>
        <div class="world-card active"><strong>BOOKING SITE</strong><span class="email-chip">EMAIL</span></div>
      </div>''',
        ),
        "native_constraint": (
            "ORDER OF OPERATIONS",
            "A design constraint",
            '''
      <div class="type-lockup native-reveal"><span>BEFORE</span><strong>A TOOL</strong></div>
      <div class="constraint-line native-reveal"><span>INN</span><i></i><b>BOUNDARY</b></div>''',
        ),
        "native_relay_boundary": (
            "RELAY ADDRESS",
            "The route stops at the rule.",
            '''
      <div class="relay-card native-reveal">k7m2q9x4@guest.booking.com</div>
      <div class="attempt-path native-reveal"><span>ATTEMPTED RETURN PATH</span><i></i><b>×</b></div>
      <div class="rules-line native-reveal">THE SITE'S RULES</div>''',
        ),
        "native_own_guest_book": (
            "WHAT THE INN NEEDS FIRST",
            "A guest book of its own.",
            '''
      <div class="choice-stack">
        <div class="tool-card muted native-reveal"><span>EMAIL TOOL</span><b>LATER</b></div>
        <div class="tool-card active native-reveal"><span>FRONT DESK</span><b>GUEST BOOK OF ITS OWN</b></div>
      </div>''',
        ),
        "native_guest_chooses": (
            "AT THE FRONT DESK",
            "The guest chooses.",
            '''
      <div class="signing-card native-reveal"><span class="person-mark">○</span><span class="pen-mark">／</span><span class="book-mark large">▤</span></div>
      <div class="choice-label native-reveal">GUEST CHOOSES TO SIGN</div>''',
        ),
        "native_fair_question": (
            "FAIR QUESTION",
            "If the parts are cheap…",
            '''
      <div class="question-box huge native-reveal">WHY DOESN'T<br>THE INN<br>JUST DO IT?</div>''',
        ),
        "native_commission_band": (
            "ILLUSTRATIVE MODEL",
            "Commission assumption",
            '''
      <div class="number-lockup native-reveal"><strong>18%–22%</strong><span>ALL-IN COMMISSION</span></div>
      <div class="band-bar native-reveal"><i></i></div>
      <div class="model-note native-reveal">MY ASSUMPTION FROM THE REPORTED BANDS</div>''',
        ),
        "native_annual_commission": (
            "ILLUSTRATIVE ESTIMATE",
            "Rough site commission",
            '''
      <div class="money-lockup native-reveal"><strong>$105K–<br>$130K</strong><span>PER YEAR</span></div>
      <div class="model-note native-reveal">BASED ON THE SPOKEN COMMISSION ASSUMPTION</div>''',
        ),
        "native_wrong_number": (
            "THE OLD ARGUMENT STOPS HERE",
            "$105K–$130K a year",
            '''
      <div class="wrong-number native-reveal"><span>THE WRONG</span><strong>NUMBER</strong></div>
      <div class="model-note native-reveal">THE INN IS NEVER GOING TO MOVE ALL OF IT</div>''',
        ),
    }
    kicker, title, visual = diagrams[layout]
    body = f'''
  <div class="native-stage">
    <div class="native-kicker" id="{sid}-kicker">{kicker}</div>
    <h1 class="native-title" id="{sid}-title">{title}</h1>
    <div class="native-visual">{visual}</div>
  </div>'''
    motion = f'''
  tl.fromTo("#{sid}-kicker", {{ opacity: 0, y: 12 }}, {{ opacity: 1, y: 0, duration: 0.22, ease: "power3.out" }}, 0.05);
  tl.fromTo("#{sid}-title", {{ opacity: 0, y: 20 }}, {{ opacity: 1, y: 0, duration: 0.28, ease: "power3.out" }}, 0.12);
  tl.fromTo("#{sid} .native-reveal", {{ opacity: 0, y: 18 }}, {{ opacity: 1, y: 0, duration: 0.30, stagger: 0.11, ease: "power3.out" }}, 0.27);'''
    return body, motion


def subcomposition_html(idx: int, scene: Scene, local_start: float, local_end: float) -> str:
    duration = local_end - local_start
    sid = f"frame-{idx:02d}"
    source_start = scene.source_in
    common_video = f'''src="assets/episode-r8.mp4" data-start="0" data-duration="{duration:.6f}" data-media-start="{source_start:.6f}" muted playsinline'''
    if scene.layout.startswith("native_"):
        body, motion = native_diagram_html(sid, scene.layout)
    elif scene.layout == "context_focus":
        offset_x = -((scene.focus_x - 50) / 100 * 900)
        offset_y = -((scene.focus_y - 50) / 100 * 506)
        zoom_duration = min(0.75, max(0.35, duration * 0.18))
        zoom_at = min(0.6, max(0.12, duration * 0.10))
        body = f'''
  <div class="zoom-stage">
    <div id="{sid}-zoom-outer" class="zoom-outer" data-layout-allow-overflow>
      <div id="{sid}-zoom-inner" class="zoom-inner">
      <video id="{sid}-focus-video" class="clip" {common_video}></video>
      </div>
    </div>
    <div id="{sid}-focus-mark" class="focus-mark"></div>
  </div>'''
        motion = f'''
  tl.fromTo("#{sid}-focus-mark", {{ scaleY: 0 }}, {{ scaleY: 1, duration: 0.25, ease: "power3.out" }}, {zoom_at:.6f});
  tl.to("#{sid}-zoom-outer", {{ scale: 2.02, duration: {zoom_duration:.6f}, ease: "power3.inOut" }}, {zoom_at:.6f});
  tl.to("#{sid}-zoom-inner", {{ x: {offset_x:.3f}, y: {offset_y:.3f}, duration: {zoom_duration:.6f}, ease: "power3.inOut" }}, {zoom_at:.6f});'''
    elif scene.layout == "thesis":
        body = f'''
  <div class="thesis-panel">
    <h1 id="{sid}-thesis">{html.escape(scene.label)}</h1>
    <div id="{sid}-focus-mark" class="thesis-mark"></div>
  </div>'''
        motion = f'''
  tl.fromTo("#{sid}-thesis", {{ opacity: 0, y: 24 }}, {{ opacity: 1, y: 0, duration: 0.25, ease: "power3.out" }}, 0.08);
  tl.fromTo("#{sid}-focus-mark", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.30, ease: "power3.out" }}, 0.30);'''
    else:
        crop = {
            "presenter": (280, 420, 1920, 1080),
            "presenter_left": (0, 420, 1920, 1080),
            "presenter_right": (560, 420, 1920, 1080),
            "film_center": (280, 420, 1920, 1080),
            "film_right": (560, 420, 1920, 1080),
            "film_context": (160, 555, 1440, 810),
        }[scene.layout]
        crop_x, target_y, scaled_w, scaled_h = crop
        scale = scaled_h / 720
        left = -(crop_x * scale)
        body = f'''
  <div class="portrait-panel" style="top:{target_y}px;height:{scaled_h}px;">
    <video id="{sid}-portrait-video" class="clip" data-layout-allow-overflow style="left:{left:.3f}px;width:{scaled_w}px;height:{scaled_h}px;" {common_video}></video>
    <div id="{sid}-focus-mark" class="portrait-mark"></div>
  </div>'''
        motion = f'''
  tl.fromTo("#{sid}-focus-mark", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.22, ease: "power3.out" }}, 0.08);'''

    return f'''<!doctype html>
<html><head><meta charset="utf-8"><title>{html.escape(scene.label)}</title></head><body><template>
<style>
  * {{ box-sizing: border-box; }}
  #{sid} {{ position:absolute; inset:0; width:1080px; height:1920px; overflow:hidden; }}
  @font-face {{ font-family:"BL Zodiak"; src:url("assets/fonts/zodiak-700.woff2") format("woff2"); font-weight:700; }}
  .zoom-stage {{ position:absolute; left:60px; top:250px; width:900px; height:1200px; overflow:hidden; display:grid; place-items:center; background:#EDE7D8; border:2px solid #C4B99E; }}
  .zoom-outer {{ position:relative; width:900px; height:506px; transform-origin:50% 50%; will-change:transform; }}
  .zoom-inner {{ position:absolute; inset:0; width:900px; height:506px; will-change:transform; }}
  .zoom-inner video {{ position:absolute; inset:0; width:900px; height:506px; object-fit:contain; object-position:center; }}
  .focus-mark {{ position:absolute; left:0; top:0; width:8px; height:100%; background:#B5482F; transform-origin:50% 0%; }}
  .portrait-panel {{ position:absolute; left:0; width:1080px; overflow:hidden; background:#EDE7D8; }}
  .portrait-panel video {{ position:absolute; top:0; max-width:none; object-fit:fill; }}
  .portrait-mark {{ position:absolute; left:0; top:0; width:160px; height:8px; background:#B5482F; transform-origin:0% 50%; }}
  .thesis-panel {{ position:absolute; left:96px; top:450px; width:804px; min-height:720px; display:flex; flex-direction:column; justify-content:center; }}
  .thesis-panel h1 {{ color:#173530; font-family:"BL Zodiak",Georgia,serif; font-size:118px; line-height:1.02; letter-spacing:-.038em; font-weight:700; }}
  .thesis-mark {{ margin-top:54px; width:240px; height:10px; background:#B5482F; transform-origin:0% 50%; }}
  .native-stage {{ position:absolute; left:60px; top:250px; width:900px; height:1100px; padding:54px 36px 48px; border:2px solid #C4B99E; border-left:9px solid #B5482F; background:#F0EBDD; overflow:hidden; color:#173530; }}
  .native-kicker {{ color:#586D74; font:500 24px/1 "BL Supreme",system-ui,sans-serif; letter-spacing:.12em; }}
  .native-title {{ margin-top:28px; max-width:820px; color:#173530; font-family:"BL Zodiak",Georgia,serif; font-size:82px; line-height:1.02; letter-spacing:-.035em; font-weight:700; }}
  .native-visual {{ position:absolute; left:36px; right:36px; top:330px; bottom:44px; display:flex; flex-direction:column; justify-content:center; gap:34px; }}
  .evidence-card {{ position:relative; padding:48px 36px 40px; border:3px solid #173530; background:#F5F0E6; }}
  .field-label,.model-note {{ color:#586D74; font:500 22px/1.2 "BL Supreme",system-ui,sans-serif; letter-spacing:.08em; }}
  .mono-value {{ margin-top:30px; color:#173530; font:500 46px/1.18 ui-monospace,SFMono-Regular,Menlo,monospace; letter-spacing:-.025em; overflow-wrap:anywhere; }}
  .tag {{ display:inline-block; margin-top:34px; padding:12px 18px; color:#F5F0E6; font:500 26px/1 "BL Supreme",system-ui,sans-serif; letter-spacing:.10em; }}
  .oxide {{ background:#B5482F; }}
  .flow-row {{ display:grid; grid-template-columns:1fr 1.15fr 1fr; align-items:center; gap:22px; }}
  .node {{ min-height:190px; padding:30px 22px; display:grid; place-items:center; border:3px solid #173530; background:#F5F0E6; text-align:center; }}
  .node span {{ font:500 32px/1.15 "BL Supreme",system-ui,sans-serif; letter-spacing:.04em; }}
  .node.active,.stay-card.active,.world-card.active,.tool-card.active {{ border-color:#B5482F; box-shadow:inset 0 -12px 0 #B5482F; }}
  .node.wide {{ width:620px; min-height:112px; margin:0 auto; }}
  .route {{ position:relative; height:10px; background:#586D74; }}
  .route span {{ position:absolute; left:50%; top:-54px; transform:translateX(-50%); color:#586D74; font:500 22px/1 "BL Supreme",system-ui,sans-serif; letter-spacing:.08em; }}
  .route.broken::before,.route.broken::after {{ content:""; position:absolute; top:-18px; width:8px; height:46px; background:#B5482F; transform:rotate(28deg); }}
  .route.broken::before {{ left:45%; }} .route.broken::after {{ left:55%; }}
  .status-line {{ align-self:center; padding:18px 24px; color:#B5482F; font:500 26px/1 "BL Supreme",system-ui,sans-serif; letter-spacing:.08em; }}
  .status-dot {{ display:inline-block; width:16px; height:16px; margin-right:12px; border-radius:50%; background:#B5482F; }}
  .flow-stack {{ display:flex; flex-direction:column; align-items:center; gap:14px; }}
  .down-arrow {{ color:#B5482F; font:500 52px/1 "BL Supreme",system-ui,sans-serif; }}
  .stay-grid {{ display:grid; grid-template-columns:1fr 64px 1fr; align-items:center; gap:20px; }}
  .stay-card {{ min-height:310px; padding:44px 24px; border:3px solid #173530; background:#F5F0E6; display:flex; flex-direction:column; justify-content:space-between; }}
  .stay-card span {{ color:#586D74; font:500 24px/1 "BL Supreme",system-ui,sans-serif; letter-spacing:.08em; }}
  .stay-card strong {{ font:500 38px/1.05 "BL Supreme",system-ui,sans-serif; overflow-wrap:anywhere; }}
  .equals {{ text-align:center; font:500 54px/1 "BL Supreme",system-ui,sans-serif; }}
  .ledger-stack {{ display:flex; flex-direction:column; gap:22px; }}
  .ledger-row {{ display:grid; grid-template-columns:90px 1fr; gap:8px 22px; align-items:center; padding:24px 26px; border-bottom:2px solid #C4B99E; }}
  .ledger-row > span {{ grid-row:1/3; color:#B5482F; font:500 56px/1 ui-monospace,SFMono-Regular,monospace; }}
  .ledger-row strong {{ font:500 34px/1.1 "BL Supreme",system-ui,sans-serif; }}
  .ledger-row small {{ color:#586D74; font:400 26px/1.1 "BL Supreme",system-ui,sans-serif; }}
  .question-box {{ padding:28px 30px; background:#173530; color:#F5F0E6; text-align:center; font:500 42px/1.08 "BL Supreme",system-ui,sans-serif; letter-spacing:.02em; }}
  .question-box.huge {{ padding:52px 36px; font-family:"BL Zodiak",Georgia,serif; font-size:72px; line-height:1.04; letter-spacing:-.025em; }}
  .site-card {{ width:650px; min-height:480px; margin:0 auto; padding:40px; border:3px solid #173530; text-align:center; background:#F5F0E6; }}
  .building-mark {{ font:500 112px/1 "BL Supreme",system-ui,sans-serif; }}
  .site-card > strong {{ display:block; margin-top:8px; font:500 34px/1 "BL Supreme",system-ui,sans-serif; letter-spacing:.06em; }}
  .book-card {{ margin-top:48px; padding:28px; display:flex; align-items:center; justify-content:center; gap:22px; background:#173530; color:#F5F0E6; }}
  .book-mark {{ font-size:62px; line-height:1; }} .book-card span:last-child {{ font:500 34px/1 "BL Supreme",system-ui,sans-serif; letter-spacing:.05em; }}
  .split-world {{ display:grid; grid-template-columns:1fr 10px 1fr; gap:30px; align-items:stretch; }}
  .world-card {{ min-height:350px; padding:36px 24px; border:3px solid #173530; background:#F5F0E6; display:flex; flex-direction:column; justify-content:space-between; text-align:center; }}
  .world-card strong {{ font:500 32px/1.1 "BL Supreme",system-ui,sans-serif; }}
  .no-email,.email-chip {{ display:block; padding:18px 12px; font:500 25px/1.05 "BL Supreme",system-ui,sans-serif; letter-spacing:.05em; }}
  .no-email {{ color:#B5482F; border:2px solid #B5482F; }} .email-chip {{ color:#F5F0E6; background:#173530; }}
  .rule-boundary {{ background:#B5482F; }}
  .type-lockup {{ display:flex; align-items:baseline; justify-content:center; gap:28px; padding:60px 30px; border-top:3px solid #B5482F; border-bottom:3px solid #B5482F; }}
  .type-lockup span {{ color:#586D74; font:500 36px/1 "BL Supreme",system-ui,sans-serif; }}
  .type-lockup strong {{ font:500 70px/1 "BL Supreme",system-ui,sans-serif; }}
  .constraint-line {{ display:grid; grid-template-columns:150px 1fr 180px; align-items:center; gap:16px; color:#586D74; font:500 26px/1 "BL Supreme",system-ui,sans-serif; }}
  .constraint-line i {{ height:5px; background:#173530; }} .constraint-line b {{ padding:16px; color:#F5F0E6; background:#B5482F; text-align:center; }}
  .relay-card {{ padding:30px 28px; border:3px solid #173530; background:#F5F0E6; font:500 31px/1.2 ui-monospace,SFMono-Regular,monospace; overflow-wrap:anywhere; }}
  .attempt-path {{ display:grid; grid-template-columns:auto 1fr 64px; align-items:center; gap:22px; color:#586D74; font:500 24px/1 "BL Supreme",system-ui,sans-serif; }}
  .attempt-path i {{ height:5px; background:#173530; }} .attempt-path b {{ color:#B5482F; font-size:76px; line-height:1; }}
  .rules-line {{ padding:24px; border-top:8px solid #B5482F; color:#B5482F; text-align:center; font:500 34px/1 "BL Supreme",system-ui,sans-serif; letter-spacing:.08em; }}
  .choice-stack {{ display:flex; flex-direction:column; gap:30px; }}
  .tool-card {{ min-height:180px; padding:30px; border:3px solid #173530; background:#F5F0E6; display:flex; justify-content:space-between; align-items:center; }}
  .tool-card span {{ color:#586D74; font:500 26px/1 "BL Supreme",system-ui,sans-serif; }} .tool-card b {{ max-width:520px; text-align:right; font:500 36px/1.05 "BL Supreme",system-ui,sans-serif; }}
  .tool-card.muted {{ opacity:.58; }}
  .signing-card {{ display:flex; align-items:end; justify-content:center; gap:50px; min-height:320px; padding:44px; border-bottom:4px solid #173530; }}
  .person-mark {{ font-size:150px; line-height:.75; }} .pen-mark {{ color:#B5482F; font-size:120px; line-height:1; }} .book-mark.large {{ font-size:140px; line-height:1; }}
  .choice-label {{ text-align:center; color:#B5482F; font:500 36px/1 "BL Supreme",system-ui,sans-serif; letter-spacing:.06em; }}
  .number-lockup,.money-lockup {{ text-align:center; }}
  .number-lockup strong {{ display:block; color:#173530; font:700 156px/.92 "BL Zodiak",Georgia,serif; letter-spacing:-.05em; }}
  .number-lockup span,.money-lockup span {{ display:block; margin-top:22px; color:#586D74; font:500 32px/1 "BL Supreme",system-ui,sans-serif; letter-spacing:.08em; }}
  .band-bar {{ position:relative; width:180px; height:260px; margin:0 auto; border:4px solid #173530; }}
  .band-bar::before {{ content:""; position:absolute; left:0; right:0; bottom:0; height:62%; background:#D8CFB9; }}
  .band-bar i {{ position:absolute; left:-4px; right:-4px; bottom:56%; height:18%; background:#B5482F; opacity:.82; }}
  .money-lockup strong {{ display:block; color:#173530; font:700 130px/.88 "BL Zodiak",Georgia,serif; letter-spacing:-.045em; }}
  .model-note {{ text-align:center; }}
  .wrong-number {{ padding:42px; border:4px solid #B5482F; text-align:center; }}
  .wrong-number span {{ display:block; color:#586D74; font:500 40px/1 "BL Supreme",system-ui,sans-serif; }}
  .wrong-number strong {{ display:block; margin-top:12px; color:#B5482F; font:700 118px/.9 "BL Zodiak",Georgia,serif; letter-spacing:-.04em; }}
</style>
<div id="{sid}" data-composition-id="{sid}" data-start="0" data-duration="{duration:.6f}" data-width="1080" data-height="1920" data-fps="24">
{body}
</div>
<script>(() => {{
  const tl = gsap.timeline({{ paused: true }});{motion}
  window.__timelines = window.__timelines || {{}};
  window.__timelines["{sid}"] = tl;
}})();</script>
</template></body></html>
'''


def index_html(candidate: dict, spec: dict, scenes: list[tuple[Scene, float, float]], captions: list[dict]) -> str:
    total = candidate["source_cut"]["duration_seconds"]
    source_start = candidate["source_cut"]["start_seconds"]
    scene_hosts = []
    for i, (_, start, end) in enumerate(scenes, 1):
        scene_hosts.append(
            f'''<div id="scene-host-{i:02d}" class="clip scene-host" data-composition-id="frame-{i:02d}" data-composition-src="compositions/frame-{i:02d}.html" data-start="{start:.6f}" data-duration="{end-start:.6f}" data-track-index="0"></div>'''
        )

    emphasis = spec["emphasis"]
    cap_nodes = []
    embed_until = float(spec.get("embed_until", -1))
    for i, cap in enumerate(captions):
        if cap["end"] <= embed_until + 1e-6:
            continue
        text = emphasized_text(cap["text"], emphasis)
        cap_nodes.append(
            f'''<p id="cap-{i:03d}" class="clip caption" data-caption-layer="fg" data-start="{cap['start']:.6f}" data-duration="{cap['duration']:.6f}" data-track-index="20">{text}</p>'''
        )

    disclosure = spec.get("disclosure", "LOCKED EP009 EXCERPT · PRIVATE REVIEW")
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=1080, height=1920" />
  <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
  <style>
    @font-face {{ font-family:"BL Zodiak"; src:url("assets/fonts/zodiak-700.woff2") format("woff2"); font-weight:700; }}
    @font-face {{ font-family:"BL Supreme"; src:url("assets/fonts/supreme-400.woff2") format("woff2"); font-weight:400; }}
    @font-face {{ font-family:"BL Supreme"; src:url("assets/fonts/supreme-500.woff2") format("woff2"); font-weight:500; }}
    * {{ box-sizing:border-box; margin:0; padding:0; }}
    html, body {{ width:1080px; height:1920px; overflow:hidden; background:#F5F0E6; }}
    #root {{ position:relative; width:1080px; height:1920px; overflow:hidden; color:#19201F; font-family:"BL Supreme",system-ui,sans-serif; }}
    .paper {{ position:absolute; inset:0; background:#F5F0E6; }}
    .top-rule {{ position:absolute; left:68px; right:68px; top:174px; height:2px; background:#C4B99E; }}
    .identity {{ position:absolute; left:68px; top:58px; font-size:24px; line-height:1; letter-spacing:.12em; font-weight:500; color:#204440; }}
    .short-id {{ position:absolute; right:68px; top:58px; font:500 22px/1 ui-monospace,SFMono-Regular,monospace; color:#586D74; letter-spacing:.06em; }}
    .scene-host {{ position:absolute; inset:0; width:1080px; height:1920px; overflow:hidden; }}
    .caption {{ position:absolute; left:96px; top:1450px; width:804px; min-height:96px; z-index:40; padding:18px 24px 20px; border-radius:2px; background:#173530; color:#F5F0E6; font-size:48px; line-height:1.10; font-weight:500; letter-spacing:-.012em; text-align:left; box-shadow:0 8px 24px rgba(23,53,48,.12); }}
    .caption .em {{ color:#FB8B69; }}
    .disclosure {{ position:absolute; left:68px; bottom:190px; width:944px; color:#586D74; font-size:20px; line-height:1.25; letter-spacing:.075em; text-transform:uppercase; }}
    .progress {{ position:absolute; left:68px; bottom:128px; width:944px; height:4px; background:#D8CFB9; overflow:hidden; }}
    #progress-fill {{ width:100%; height:100%; background:#B5482F; transform-origin:0% 50%; }}
    .footer {{ position:absolute; left:68px; right:68px; bottom:62px; display:flex; justify-content:space-between; align-items:center; color:#586D74; font-size:20px; letter-spacing:.06em; }}
  </style>
</head>
<body>
  <div id="root" data-composition-id="main" data-start="0" data-duration="{total:.6f}" data-width="1080" data-height="1920" data-fps="24">
    <div class="paper"></div>
    <div class="identity">THE OPERATOR ECONOMY</div>
    <div class="short-id">EP009 · {candidate['rank']:02d}/04</div>
    <div class="top-rule"></div>
    {''.join(scene_hosts)}
    <audio id="locked-audio" src="assets/episode-r8.mp4" data-start="0" data-duration="{total:.6f}" data-media-start="{source_start:.6f}" data-track-index="10"></audio>
    {''.join(cap_nodes)}
    <div class="disclosure">{html.escape(disclosure)}</div>
    <div class="progress"><div id="progress-fill"></div></div>
    <div class="footer"><span>DIRECT-BOOKING RECOVERY</span><span>{total:.1f}S · 24 FPS</span></div>
  </div>
  <script>
    window.__timelines = window.__timelines || {{}};
    const tl = gsap.timeline({{ paused: true }});
    tl.fromTo("#progress-fill", {{ scaleX: 0 }}, {{ scaleX: 1, duration: {total:.6f}, ease: "none" }}, 0);
    window.__timelines["main"] = tl;
    tl.seek(0);
  </script>
</body>
</html>
'''


def write_contract(project: Path, candidate: dict, captions: list[dict]) -> None:
    contract = {
        "schema": "oe-ep009-short-source-contract-v1",
        "status": "private_review_source_not_rendered_not_approved",
        "candidate_id": candidate["candidate_id"],
        "locked_carrier": {
            "path": str(CARRIER_PATH.relative_to(REPO)),
            "sha256": EXPECTED[CARRIER_PATH],
        },
        "final_episode_lock": {
            "path": str(LOCK_PATH.relative_to(REPO)),
            "sha256": EXPECTED[LOCK_PATH],
        },
        "source_cut": candidate["source_cut"],
        "word_range": [candidate["first_word"]["id"], candidate["last_word"]["id"]],
        "caption_group_count": len(captions),
        "limits": [
            "No narration rewrite or source reordering.",
            "Portrait composition remains separately reviewable and unapproved.",
            "No upload, release or publication authorization.",
        ],
    }
    (project / "source-contract.json").write_text(json.dumps(contract, indent=2) + "\n")


def main() -> None:
    verify_inputs()
    editorial = json.loads(MAP_PATH.read_text())
    transcript = json.loads(TRANSCRIPT_PATH.read_text())
    candidates = {c["candidate_id"]: c for c in editorial["candidates"]}
    words = transcript["words"]

    for candidate_id, spec in PROJECTS.items():
        project = ROOT / spec["dir"]
        project.mkdir(parents=True, exist_ok=True)
        (project / "compositions").mkdir(exist_ok=True)
        candidate = candidates[candidate_id]
        write_assets(project)
        write_brief(project, candidate, spec)
        captions = caption_groups(candidate, words)
        embed_until = float(spec.get("embed_until", -1))
        for caption in captions:
            caption["state"] = "embed" if caption["end"] <= embed_until + 1e-6 else "rail"
        (project / "captions.json").write_text(json.dumps({"candidate_id": candidate_id, "groups": captions}, indent=2) + "\n")
        scenes = write_storyboard(project, candidate, spec)
        for i, (scene, local_start, local_end) in enumerate(scenes, 1):
            (project / "compositions" / f"frame-{i:02d}.html").write_text(
                subcomposition_html(i, scene, local_start, local_end)
            )
        (project / "index.html").write_text(index_html(candidate, spec, scenes, captions))
        write_contract(project, candidate, captions)
        print(f"built {project.relative_to(REPO)}: {len(scenes)} scenes, {len(captions)} caption groups")


if __name__ == "__main__":
    main()
