#!/usr/bin/env python3
"""Build EP009 Short 04 r2 from exact locked-carrier words.

Writes only this project. It does not mutate the locked episode, render, upload, or publish.
"""

from __future__ import annotations

import hashlib
import html
import json
import os
from pathlib import Path


PROJECT = Path(__file__).resolve().parent
REPO = PROJECT.parents[3]
CARRIER = REPO / "blueprint-cinema/experiments/EP009-FULL-BUILD-001/assembly/qa/r8-tool-clarity/ep009-r8-tool-clarity-review-r1.mp4"
LOCK = REPO / "blueprint-cinema/experiments/EP009-FULL-BUILD-001/assembly/r8-tool-clarity/FINAL-EPISODE-LOCK-r8.json"
TRANSCRIPT = REPO / "blueprint-cinema/experiments/EP009-FULL-BUILD-001/assembly/r3/word-transcript-r3.json"
FPS = 24
CTA_FRAMES = 54

EXPECTED = {
    CARRIER: "cc5805a990d10812b5349568e50a74dc0e21b09ed402b49250f9796640ed710e",
    LOCK: "b9d107718c0d760e388c1a5167bcaf7e06ebfb29504ed469fac385aa2aa54cd2",
    TRANSCRIPT: "0b5175dea2cbb1ac7682cd69b9ab032bc8c544131aae82575140e90ae0d76709",
}

EDITS = [
    {
        "id": "wrong-number-cold-open",
        "word_in": "W001447",
        "word_out": "W001465",
        "source_in_frame": 12495,
        "source_out_frame_exclusive": 12618,
        "purpose": "Cold-open correction: total site commission is not recoverable commission.",
    },
    {
        "id": "qualified-modeled-total",
        "word_in": "W001401",
        "word_out": "W001437",
        "source_in_frame": 12150,
        "source_out_frame_exclusive": 12409,
        "purpose": "State the spoken 18-22 percent assumption and modeled annual total.",
    },
    {
        "id": "old-argument-stops",
        "word_in": "W001438",
        "word_out": "W001446",
        "source_in_frame": 12426,
        "source_out_frame_exclusive": 12487,
        "purpose": "Close the old total-commission argument.",
    },
    {
        "id": "recoverable-share-question",
        "word_in": "W001466",
        "word_out": "W001475",
        "source_in_frame": 12618,
        "source_out_frame_exclusive": 12690,
        "purpose": "End on the calculation the full episode resolves.",
    },
]

CAPTION_RANGES = [
    (0, "W001447", "W001450"),
    (0, "W001451", "W001461"),
    (0, "W001462", "W001465"),
    (1, "W001401", "W001406"),
    (1, "W001407", "W001411"),
    (1, "W001412", "W001417"),
    (1, "W001418", "W001424"),
    (1, "W001425", "W001437"),
    (2, "W001438", "W001446"),
    (3, "W001466", "W001475"),
]


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


def prepare_edits(words_by_id: dict[str, dict]) -> tuple[list[dict], int]:
    timeline_frame = 0
    prepared = []
    for raw in EDITS:
        edit = dict(raw)
        edit["frame_count"] = edit["source_out_frame_exclusive"] - edit["source_in_frame"]
        edit["source_in_seconds"] = edit["source_in_frame"] / FPS
        edit["source_out_seconds"] = edit["source_out_frame_exclusive"] / FPS
        edit["timeline_in_frame"] = timeline_frame
        edit["timeline_out_frame_exclusive"] = timeline_frame + edit["frame_count"]
        edit["timeline_in_seconds"] = timeline_frame / FPS
        edit["duration_seconds"] = edit["frame_count"] / FPS
        first = words_by_id[edit["word_in"]]
        last = words_by_id[edit["word_out"]]
        if first["start"] < edit["source_in_seconds"] or last["end"] > edit["source_out_seconds"]:
            raise SystemExit(f"word range escapes frame cut: {edit['id']}")
        prepared.append(edit)
        timeline_frame = edit["timeline_out_frame_exclusive"]
    return prepared, timeline_frame


def caption_data(words: list[dict], words_by_id: dict[str, dict], edits: list[dict]) -> list[dict]:
    index = {w["w_id"]: i for i, w in enumerate(words)}
    groups = []
    ordered_tokens = []
    for group_index, (edit_index, first_id, last_id) in enumerate(CAPTION_RANGES):
        edit = edits[edit_index]
        selected = words[index[first_id] : index[last_id] + 1]
        start = edit["timeline_in_seconds"] + (selected[0]["start"] - edit["source_in_seconds"])
        end = edit["timeline_in_seconds"] + (selected[-1]["end"] - edit["source_in_seconds"])
        ordered_tokens.extend(w["token"] for w in selected)
        groups.append(
            {
                "id": f"caption-{group_index:02d}",
                "edit_id": edit["id"],
                "word_in": first_id,
                "word_out": last_id,
                "start_seconds": round(start, 6),
                "end_seconds": round(end, 6),
                "duration_seconds": round(end - start, 6),
                "text": " ".join(w["token"] for w in selected),
            }
        )

    expected_tokens = []
    for edit in edits:
        expected_tokens.extend(
            w["token"] for w in words[index[edit["word_in"]] : index[edit["word_out"]] + 1]
        )
    if ordered_tokens != expected_tokens:
        raise SystemExit("caption tokens do not exactly match ordered EDL transcript")
    return groups


def emphasized(text: str) -> str:
    emphasis = {
        "wrong", "number,", "eighteen", "twenty", "percent,", "hundred", "thousand",
        "dollars", "shift.", "sites."
    }
    return " ".join(
        f'<span class="em">{html.escape(token)}</span>' if token.lower() in emphasis else html.escape(token)
        for token in text.split()
    )


def write_index(edits: list[dict], captions: list[dict], spoken_frames: int) -> None:
    total_frames = spoken_frames + CTA_FRAMES
    total = total_frames / FPS
    audio = "\n".join(
        f'''    <audio class="clip source-audio" id="audio-{i + 1:02d}" src="assets/locked-carrier.mp4" data-start="{e['timeline_in_seconds']:.6f}" data-duration="{e['duration_seconds'] - 0.001:.6f}" data-media-start="{e['source_in_seconds']:.6f}" data-track-index="10"></audio>'''
        for i, e in enumerate(edits)
    )
    caption_nodes = "\n".join(
        f'''    <p id="{c['id']}" class="clip caption" data-caption-layer="fg" data-start="{c['start_seconds']:.6f}" data-duration="{c['duration_seconds']:.6f}" data-track-index="20">{emphasized(c['text'])}</p>'''
        for c in captions
    )

    index = f'''<!doctype html>
<html lang="en" data-resolution="portrait">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=1080, height=1920" />
  <title>EP009 Short 04 r2 · The wrong number</title>
  <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
  <style>
    @font-face {{ font-family:"BL Zodiak"; src:url("assets/fonts/zodiak-700.woff2") format("woff2"); font-weight:700; }}
    @font-face {{ font-family:"BL Supreme"; src:url("assets/fonts/supreme-400.woff2") format("woff2"); font-weight:400; }}
    @font-face {{ font-family:"BL Supreme"; src:url("assets/fonts/supreme-500.woff2") format("woff2"); font-weight:500; }}
    * {{ box-sizing:border-box; margin:0; padding:0; }}
    html,body {{ width:1080px; height:1920px; overflow:hidden; background:#F5F0E6; }}
    #root {{ position:relative; width:1080px; height:1920px; overflow:hidden; background:#F5F0E6; color:#19201F; font-family:"BL Supreme",system-ui,sans-serif; }}
    .clip {{ position:absolute; }}
    .paper {{ position:absolute; inset:0; background:#F5F0E6; }}
    .paper::after {{ content:""; position:absolute; inset:0; opacity:.24; background-image:linear-gradient(rgba(32,68,64,.05) 1px,transparent 1px),linear-gradient(90deg,rgba(32,68,64,.05) 1px,transparent 1px); background-size:54px 54px; }}
    .header-back {{ position:absolute; z-index:69; left:0; top:0; width:1080px; height:116px; background:#F5F0E6; }}
    .brand {{ position:absolute; z-index:70; left:54px; top:44px; font:500 22px/1 "BL Supreme",sans-serif; letter-spacing:.14em; color:#204440; }}
    .episode {{ position:absolute; z-index:70; right:54px; top:44px; font:500 20px/1 ui-monospace,monospace; letter-spacing:.08em; color:#586D74; }}
    .top-rule {{ position:absolute; z-index:70; left:54px; right:54px; top:96px; height:2px; background:#C4B99E; }}
    .presenter {{ z-index:2; left:0; width:1080px; height:920px; object-fit:cover; object-position:50% 48%; filter:saturate(.95) contrast(1.02); }}
    #presenter-open {{ top:405px; }}
    #presenter-question {{ top:385px; }}
    .scene {{ z-index:5; inset:0; width:1080px; height:1920px; overflow:hidden; }}
    .kicker {{ color:#586D74; font:500 23px/1.15 "BL Supreme",sans-serif; letter-spacing:.13em; text-transform:uppercase; }}
    .hero-number {{ position:absolute; left:54px; top:142px; width:972px; color:#173530; font:700 142px/.88 "BL Zodiak",Georgia,serif; letter-spacing:-.055em; white-space:nowrap; transform-origin:0 50%; }}
    .hero-label {{ position:absolute; left:60px; top:292px; padding:12px 18px; background:#173530; color:#F5F0E6; font:500 27px/1 "BL Supreme",sans-serif; letter-spacing:.08em; }}
    .hero-rule {{ position:absolute; left:54px; top:358px; width:972px; height:9px; background:#B5482F; transform-origin:0 50%; }}
    .not-recoverable {{ position:absolute; z-index:6; right:54px; top:1212px; padding:15px 18px; border:3px solid #B5482F; background:#F5F0E6; color:#B5482F; font:500 24px/1 "BL Supreme",sans-serif; letter-spacing:.06em; }}
    .needs-sites {{ position:absolute; z-index:6; left:54px; top:1248px; padding:18px 22px; background:#173530; color:#F5F0E6; font:500 34px/1 "BL Supreme",sans-serif; letter-spacing:.04em; }}
    .model-scene {{ background:#F0EBDD; }}
    .model-kicker {{ position:absolute; left:60px; top:156px; }}
    .range-title {{ position:absolute; left:60px; top:220px; width:960px; font:700 88px/.94 "BL Zodiak",serif; letter-spacing:-.035em; color:#173530; }}
    .range-numbers {{ position:absolute; left:60px; right:60px; top:510px; display:grid; grid-template-columns:1fr 120px 1fr; align-items:center; }}
    .range-numbers strong {{ font:700 190px/.86 "BL Zodiak",serif; letter-spacing:-.055em; color:#173530; text-align:center; }}
    .range-numbers span {{ font:500 70px/1 "BL Supreme",sans-serif; color:#B5482F; text-align:center; }}
    .range-track {{ position:absolute; left:110px; right:110px; top:780px; height:18px; background:#C4B99E; }}
    .range-track i {{ display:block; width:100%; height:18px; background:#B5482F; transform-origin:0 50%; }}
    .qualifier {{ position:absolute; left:78px; right:78px; top:870px; padding:30px 34px; border-left:9px solid #B5482F; background:#F5F0E6; color:#173530; font:500 42px/1.15 "BL Supreme",sans-serif; }}
    .total-scene {{ background:#173530; color:#F5F0E6; }}
    .total-kicker {{ position:absolute; left:60px; top:156px; color:#C4B99E; }}
    .total-number {{ position:absolute; left:54px; top:338px; width:972px; font:700 154px/.88 "BL Zodiak",serif; letter-spacing:-.06em; color:#F5F0E6; text-align:center; transform-origin:50% 50%; }}
    .total-label {{ position:absolute; left:160px; right:160px; top:720px; padding:24px; border-top:3px solid #B5482F; border-bottom:3px solid #B5482F; text-align:center; font:500 38px/1.12 "BL Supreme",sans-serif; letter-spacing:.05em; }}
    .total-warning {{ position:absolute; left:110px; right:110px; top:930px; padding:25px; background:#F5F0E6; color:#B5482F; text-align:center; font:500 29px/1.1 "BL Supreme",sans-serif; letter-spacing:.07em; }}
    .stop-scene {{ display:grid; place-items:center; padding:130px 64px 360px; background:#F5F0E6; }}
    .stop-card {{ position:relative; width:950px; min-height:930px; display:flex; flex-direction:column; justify-content:center; padding:70px 64px; border:5px solid #173530; background:#F0EBDD; overflow:hidden; }}
    .stop-card h2 {{ position:relative; z-index:2; font:700 120px/.9 "BL Zodiak",serif; letter-spacing:-.055em; color:#173530; }}
    .stop-card p {{ position:relative; z-index:2; margin-top:56px; max-width:760px; font:500 46px/1.12 "BL Supreme",sans-serif; color:#586D74; }}
    .stop-slash {{ position:absolute; z-index:1; right:-100px; top:150px; width:500px; height:28px; opacity:.26; background:#B5482F; transform:rotate(-50deg); transform-origin:50% 50%; }}
    .question-heading {{ position:absolute; left:54px; top:148px; z-index:6; color:#586D74; font:500 26px/1 "BL Supreme",sans-serif; letter-spacing:.13em; }}
    .question-lockup {{ position:absolute; left:54px; right:54px; top:245px; z-index:6; padding:24px 30px; background:#173530; color:#F5F0E6; font:700 82px/.92 "BL Zodiak",serif; letter-spacing:-.04em; }}
    .focus-bar {{ position:absolute; left:54px; top:346px; z-index:6; width:430px; height:10px; background:#B5482F; transform-origin:0 50%; }}
    .caption {{ z-index:80; left:70px; top:1410px; width:860px; min-height:120px; display:block; padding:22px 28px 25px; background:#173530; color:#F5F0E6; font:500 64px/1.04 "BL Supreme",sans-serif; letter-spacing:-.025em; box-shadow:0 10px 28px rgba(23,53,48,.18); }}
    .caption .em {{ color:#FB8B69; }}
    .progress {{ position:absolute; z-index:75; left:70px; right:70px; bottom:136px; height:6px; background:#D8CFB9; overflow:hidden; }}
    #progress-fill {{ width:100%; height:100%; background:#B5482F; transform-origin:0 50%; }}
    .cta-scene {{ z-index:90; inset:0; width:1080px; height:1920px; display:flex; flex-direction:column; justify-content:center; padding:150px 74px 220px; background:#173530; color:#F5F0E6; }}
    .cta-kicker {{ color:#FB8B69; font:500 26px/1 "BL Supreme",sans-serif; letter-spacing:.13em; }}
    .cta-question {{ margin-top:44px; font:700 106px/.91 "BL Zodiak",serif; letter-spacing:-.052em; }}
    .cta-rule {{ margin-top:54px; width:100%; height:10px; background:#B5482F; transform-origin:0 50%; }}
    .cta-payoff {{ margin-top:48px; font:500 43px/1.1 "BL Supreme",sans-serif; }}
    .cta-action {{ margin-top:34px; align-self:flex-start; padding:20px 24px; background:#F5F0E6; color:#173530; font:500 32px/1 "BL Supreme",sans-serif; letter-spacing:.06em; }}
  </style>
</head>
<body>
  <div id="root" data-composition-id="main" data-start="0" data-duration="{total:.6f}" data-width="1080" data-height="1920" data-fps="24">
    <div class="paper"></div>
    <div id="header-back" class="clip header-back" data-start="0" data-duration="21.458333" data-track-index="70"></div>
    <div id="brand-bug" class="clip brand" data-start="0" data-duration="21.458333" data-track-index="71">THE OPERATOR ECONOMY</div>
    <div id="episode-bug" class="clip episode" data-start="0" data-duration="21.458333" data-track-index="71">EP009 · SHORT 04</div>
    <div id="header-rule" class="clip top-rule" data-start="0" data-duration="21.458333" data-track-index="71"></div>

    <video id="presenter-open" class="clip presenter" src="assets/locked-carrier.mp4" data-start="0" data-duration="5.125000" data-media-start="520.625000" data-track-index="0" muted playsinline></video>
    <section id="scene-cold-open" class="clip scene" data-start="0" data-duration="5.125000" data-track-index="1">
      <div id="hero-number" class="hero-number">$105K–$130K</div>
      <div class="hero-label">ILLUSTRATIVE TOTAL · PER YEAR</div>
      <div id="hero-rule" class="hero-rule"></div>
      <div class="not-recoverable">NOT THE RECOVERABLE AMOUNT</div>
      <div id="needs-sites" class="needs-sites">THE INN NEEDS THE SITES</div>
    </section>

    <section id="scene-range" class="clip scene model-scene" data-start="5.125000" data-duration="5.625000" data-track-index="1">
      <div class="kicker model-kicker">ILLUSTRATIVE MODEL · SPOKEN QUALIFICATION</div>
      <h2 class="range-title">All-in commission assumption</h2>
      <div id="range-numbers" class="range-numbers"><strong>18%</strong><span>TO</span><strong>22%</strong></div>
      <div class="range-track"><i id="range-fill"></i></div>
      <div id="range-qualifier" class="qualifier">MY ASSUMPTION FROM THE REPORTED BANDS</div>
    </section>

    <section id="scene-total" class="clip scene total-scene" data-start="10.750000" data-duration="5.166667" data-track-index="1">
      <div class="kicker total-kicker">WHAT THE INN PAYS THE SITES · MODELED</div>
      <div id="total-number" class="total-number">$105K–<br>$130K</div>
      <div class="total-label">TOTAL SITE COMMISSION<br>PER YEAR</div>
      <div id="total-warning" class="total-warning">THIS IS NOT WHAT A RECOVERY SERVICE CAN SHIFT</div>
    </section>

    <section id="scene-stop" class="clip scene stop-scene" data-start="15.916667" data-duration="2.541667" data-track-index="1">
      <div class="stop-card" data-layout-allow-overflow><h2>THE OLD<br>ARGUMENT<br>STOPS HERE.</h2><p>THE INN WILL NEVER MOVE ALL OF IT.</p><div id="stop-slash" class="stop-slash" data-layout-allow-overflow></div></div>
    </section>

    <video id="presenter-question" class="clip presenter" src="assets/locked-carrier.mp4" data-start="18.458334" data-duration="3.000000" data-media-start="525.750000" data-track-index="0" muted playsinline></video>
    <section id="scene-question" class="clip scene" data-start="18.458334" data-duration="3.000000" data-track-index="1">
      <div class="question-heading">THE REAL QUESTION</div>
      <div class="question-lockup">WHAT CAN<br>ACTUALLY SHIFT?</div>
      <div id="focus-bar" class="focus-bar"></div>
    </section>

    {audio}
    {caption_nodes}

    <div class="progress"><div id="progress-fill"></div></div>

    <section id="scene-cta" class="clip cta-scene" data-start="21.458334" data-duration="{CTA_FRAMES / FPS:.6f}" data-track-index="100">
      <div id="cta-kicker" class="cta-kicker">THE UNANSWERED NUMBER</div>
      <h2 id="cta-question" class="cta-question">What can this inn actually afford?</h2>
      <div id="cta-rule" class="cta-rule"></div>
      <p id="cta-payoff" class="cta-payoff">The full calculation in EP009</p>
      <div id="cta-action" class="cta-action">TAP THE RELATED VIDEO</div>
    </section>
  </div>
  <script>
    window.__timelines = window.__timelines || {{}};
    const tl = gsap.timeline({{ paused:true }});
    tl.fromTo("#hero-number", {{ scale:1.055 }}, {{ scale:1, duration:.42, ease:"power3.out" }}, 0);
    tl.fromTo("#hero-rule", {{ scaleX:0 }}, {{ scaleX:1, duration:.38, ease:"power3.out" }}, 0);
    tl.fromTo("#needs-sites", {{ opacity:0, y:24 }}, {{ opacity:1, y:0, duration:.34, ease:"power3.out" }}, 3.55);
    tl.fromTo("#range-numbers", {{ opacity:.2, y:34 }}, {{ opacity:1, y:0, duration:.42, ease:"power3.out" }}, 5.18);
    tl.fromTo("#range-fill", {{ scaleX:0 }}, {{ scaleX:1, duration:.72, ease:"power3.inOut" }}, 6.15);
    tl.fromTo("#range-qualifier", {{ opacity:0, x:-34 }}, {{ opacity:1, x:0, duration:.36, ease:"power3.out" }}, 8.68);
    tl.fromTo("#total-number", {{ opacity:.2, scale:.90 }}, {{ opacity:1, scale:1, duration:.46, ease:"power3.out" }}, 10.77);
    tl.fromTo("#total-warning", {{ opacity:0, y:24 }}, {{ opacity:1, y:0, duration:.34, ease:"power3.out" }}, 13.82);
    tl.fromTo("#stop-slash", {{ scaleX:0 }}, {{ scaleX:1, duration:.34, ease:"power3.out" }}, 16.10);
    tl.fromTo("#focus-bar", {{ scaleX:0 }}, {{ scaleX:1, duration:.30, ease:"power3.out" }}, 18.50);
    tl.fromTo("#cta-kicker", {{ opacity:0, y:22 }}, {{ opacity:1, y:0, duration:.18, ease:"power3.out" }}, 21.458334);
    tl.fromTo("#cta-question", {{ opacity:0, y:34 }}, {{ opacity:1, y:0, duration:.28, ease:"power3.out" }}, 21.53);
    tl.fromTo("#cta-rule", {{ scaleX:0 }}, {{ scaleX:1, duration:.30, ease:"power3.out" }}, 21.67);
    tl.fromTo("#cta-payoff", {{ opacity:0, y:20 }}, {{ opacity:1, y:0, duration:.24, ease:"power3.out" }}, 21.82);
    tl.fromTo("#cta-action", {{ opacity:0, y:18 }}, {{ opacity:1, y:0, duration:.22, ease:"power3.out" }}, 22.04);
    tl.fromTo("#progress-fill", {{ scaleX:0 }}, {{ scaleX:1, duration:{total:.6f}, ease:"none" }}, 0);
    window.__timelines.main = tl;
    tl.seek(0);
  </script>
</body>
</html>
'''
    (PROJECT / "index.html").write_text(index)


def main() -> None:
    verify_inputs()
    transcript = json.loads(TRANSCRIPT.read_text())
    words = transcript["words"]
    words_by_id = {w["w_id"]: w for w in words}
    edits, spoken_frames = prepare_edits(words_by_id)
    captions = caption_data(words, words_by_id, edits)
    total_frames = spoken_frames + CTA_FRAMES

    assets = PROJECT / "assets"
    assets.mkdir(exist_ok=True)
    link = assets / "locked-carrier.mp4"
    if link.exists() or link.is_symlink():
        link.unlink()
    link.symlink_to(Path(os.path.relpath(CARRIER, assets)))

    (PROJECT / "data").mkdir(exist_ok=True)
    (PROJECT / "data/captions.json").write_text(json.dumps({"schema":"oe-ep009-short-captions-v2", "groups":captions}, indent=2) + "\n")
    source_map = {
        "schema": "oe-ep009-short-edl-v2",
        "candidate_id": "EP009-SHORT-04-wrong-number-hook-r2",
        "fps": FPS,
        "spoken_frames": spoken_frames,
        "cta_frames": CTA_FRAMES,
        "total_frames": total_frames,
        "duration_seconds": total_frames / FPS,
        "edits": edits,
        "cta": {
            "timeline_in_frame": spoken_frames,
            "timeline_out_frame_exclusive": total_frames,
            "lines": ["What can this inn actually afford?", "The full calculation in EP009", "Tap the related video"],
            "publication_dependency": "Configure the related-video action before publication."
        }
    }
    (PROJECT / "data/source-map.json").write_text(json.dumps(source_map, indent=2) + "\n")
    contract = {
        "schema": "oe-ep009-short-source-contract-v2",
        "status": "private_review_source_not_approved_for_release",
        "candidate_id": source_map["candidate_id"],
        "locked_carrier": {"path": str(CARRIER.relative_to(REPO)), "sha256": EXPECTED[CARRIER]},
        "final_episode_lock": {"path": str(LOCK.relative_to(REPO)), "sha256": EXPECTED[LOCK]},
        "word_transcript": {"path": str(TRANSCRIPT.relative_to(REPO)), "sha256": EXPECTED[TRANSCRIPT]},
        "edit_policy": "Whole exact locked phrases may reorder; no new spoken words or synthetic presenter performance.",
        "edits": edits,
        "withheld_payoff": ["recoverable share", "net savings", "affordable fee ceiling", "viable service price"],
        "truth_requirements": [
            "18-22 percent remains explicitly spoken as the narrator's assumption from reported bands.",
            "$105K-$130K is labeled illustrative total site commission per year, not a recoverable amount.",
            "The final question withholds rather than invents the shift assumption."
        ],
        "authorization": {"private_review_render": True, "upload": False, "release": False, "publication": False}
    }
    (PROJECT / "source-contract.json").write_text(json.dumps(contract, indent=2) + "\n")
    write_index(edits, captions, spoken_frames)
    print(f"built {PROJECT.relative_to(REPO)}: {len(edits)} audio edits, {len(captions)} captions, {total_frames} frames")


if __name__ == "__main__":
    main()
