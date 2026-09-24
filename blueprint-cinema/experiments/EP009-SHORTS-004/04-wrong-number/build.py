#!/usr/bin/env python3
"""EP009 Short 04 r4 — the commission total is the wrong number.

The r3 cut already satisfies the standalone-payoff standard and is NOT re-cut:
the correction lands in frame one against the on-screen wrong number, and the
constraint beat resolves it inside the Short. Both beats keep their exact r3
master frames (12495..12696 and 11307..11449) and their exact r3 picture slices.

Changes against EP009-SHORTS-003/04-wrong-number:
  * the price boundary overlay from the copy package is added on the spoken
    "what the job recovers", filling the previously unoverlaid constraint beat.
  * the interrogative end card is replaced by a declarative one.
  * audio is now taken from the locked narration WAV by sample boundary rather
    than from the carrier MP4's audio track. Same content, auditable fingerprint.
"""
from pathlib import Path
import html
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import oe_shorts_r4 as L  # noqa: E402

P = Path(__file__).resolve().parent
SEG037 = L.NATIVES / "seg037/native.mp4"
SEG035 = L.NATIVES / "seg035/native.mp4"

EDL = [
    {"id": "correction", "source_in_frame": 12495, "source_out_frame_exclusive": 12696,
     "word_in": "W001447", "word_out": "W001475", "timeline_in_frame": 0,
     "native": SEG037, "picture_native_frames": [83, 284], "crop": [608, 1080, 632, 0]},
    {"id": "constraint", "source_in_frame": 11307, "source_out_frame_exclusive": 11449,
     "word_in": "W001305", "word_out": "W001322", "timeline_in_frame": 201,
     "native": SEG035, "picture_native_frames": [122, 258], "crop": [608, 1080, 664, 0]},
]
SPOKEN_FRAMES = 343
PRESENTER_FRAMES = 337
END_CARD_FRAMES = 60
TOTAL_FRAMES = SPOKEN_FRAMES + (END_CARD_FRAMES - 6)  # end card overlaps the last 6 audio frames

CSS = """@font-face{font-family:Supreme;src:url(assets/fonts/supreme-400.woff2);font-weight:400}
@font-face{font-family:Supreme;src:url(assets/fonts/supreme-500.woff2);font-weight:500}
@font-face{font-family:Zodiak;src:url(assets/fonts/zodiak-700.woff2);font-weight:700}
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1080px;height:1920px;overflow:hidden;background:#173530}
#root{position:relative;width:1080px;height:1920px;overflow:hidden;font-family:Supreme,sans-serif}
.clip{position:absolute}
.presenter{left:0;top:0;width:1080px;height:1920px;object-fit:fill;z-index:0}
.caption{left:72px;top:1260px;width:882px;text-align:center;z-index:30;font-size:62px;font-weight:500;line-height:1.1;letter-spacing:-.02em;color:#F5F0E6}
.caption span{display:inline-block;padding:18px 25px 22px;background:#173530;border-radius:7px}
.context{left:66px;top:58px;max-width:938px;z-index:10;color:#F5F0E6;font:500 31px/1.1 Supreme,sans-serif;letter-spacing:.03em;padding:16px 20px;background:#173530}
.correction{left:74px;top:1034px;width:846px;z-index:10;color:#F5F0E6;font:500 45px/1.1 Supreme,sans-serif;background:#173530;padding:20px 24px;border-left:8px solid #B5482F}
.mini{left:74px;top:1044px;z-index:10;background:#173530;color:#F5F0E6;font:500 43px/1.1 Supreme,sans-serif;padding:20px 24px}
.boundary{left:74px;top:1044px;width:846px;z-index:10;background:#173530;color:#F5F0E6;font:500 45px/1.1 Supreme,sans-serif;padding:20px 24px;border-left:8px solid #FB8B69}
.end{inset:0;width:1080px;height:1920px;z-index:12;background:#173530;color:#F5F0E6;padding:355px 82px 0}
.end-kicker{font:500 27px/1.15 Supreme,sans-serif;letter-spacing:.08em;margin-bottom:45px}
.end h1{font:700 96px/1.0 Zodiak,serif;letter-spacing:-.04em}
.end p{font:400 42px/1.15 Supreme,sans-serif;margin-top:50px}
.end .action{display:inline-block;margin-top:38px;padding:20px 24px;background:#F5F0E6;color:#173530;font:500 34px/1.1 Supreme,sans-serif}
.end-rule{height:9px;background:#B5482F;width:150px;margin-top:48px;transform-origin:0 50%}"""

END = (
    '<div class="end">'
    '<div class="end-kicker">THE OPERATOR ECONOMY &middot; EP009</div>'
    '<h1>The inn can only<br>pay what the<br>job recovers.</h1>'
    '<div id="end-rule" class="end-rule"></div>'
    '<p>EP009 runs that number on an illustrative inn.</p>'
    '<div class="action">TAP THE RELATED VIDEO &rarr;</div>'
    "</div>"
)


def main() -> None:
    L.assert_locked()
    L.scaffold(P, "ep009-short04-wrong-number-r4",
               ["supreme-400.woff2", "supreme-500.woff2", "zodiak-700.woff2"])
    wi = L.word_index()

    # --- picture (accepted r3 slices, unchanged) ------------------------
    for i, e in enumerate(EDL, start=1):
        w, h, x, y = e["crop"]
        e["duration_frames"] = e["source_out_frame_exclusive"] - e["source_in_frame"]
        e["transform"] = L.presenter_clip(
            e["native"], P / f"assets/presenter-{i}.mp4", *e["picture_native_frames"],
            f"crop={w}:{h}:{x}:{y},scale=1080:1920:flags=lanczos,setsar=1")

    # --- audio (locked WAV, exact sample boundaries) -------------------
    L.cut_voice([(e["source_in_frame"], e["source_out_frame_exclusive"]) for e in EDL],
                P / "assets/voice.wav")

    spoken = SPOKEN_FRAMES / L.FPS
    total = TOTAL_FRAMES / L.FPS
    cta_start = (TOTAL_FRAMES - (END_CARD_FRAMES - 6)) / L.FPS

    # --- captions ------------------------------------------------------
    shifts = {}
    for e in EDL:
        lo, hi = int(e["word_in"][1:]), int(e["word_out"][1:])
        for n in range(lo, hi + 1):
            shifts[f"W{n:06d}"] = (e["timeline_in_frame"] - e["source_in_frame"]) / L.FPS
    spans = [("W001447", "W001450"), ("W001451", "W001455"), ("W001456", "W001461"),
             ("W001462", "W001465"), ("W001466", "W001469"), ("W001470", "W001475"),
             ("W001305", "W001309"), ("W001310", "W001313"), ("W001314", "W001318"),
             ("W001319", "W001322")]
    caps = L.caption_groups(wi, spans, lambda k: shifts[k], spoken, lead=0.0, tail=0.0)
    L.write_json(P / "captions.json", caps)
    L.write_srt(caps, P / "captions.srt")
    L.write_vtt(caps, P / "captions.vtt")

    # "what the job recovers" = W001310..W001313
    boundary_start = wi["W001310"]["start"] + shifts["W001310"]
    boundary_end = wi["W001313"]["end"] + shifts["W001313"] + 0.18

    L.sub_composition(
        P, "end", CSS, END, (END_CARD_FRAMES - 6) / L.FPS,
        anim="tl.fromTo('.end',{y:26,opacity:.3},{y:0,opacity:1,duration:.25,"
             "ease:'power2.out',immediateRender:false},0);"
             "tl.fromTo('#end-rule',{scaleX:0},{scaleX:1,duration:.3,"
             "ease:'power2.out',immediateRender:false},0);",
    )

    caphtml = "\n".join(
        f'<div class="clip caption" id="{c_id}" data-start="{c["start"]:.9f}" '
        f'data-duration="{c["end"] - c["start"]:.9f}" data-track-index="20">'
        f'<span>{html.escape(c["text"])}</span></div>'
        for c_id, c in ((f"caption-{i:02d}", c) for i, c in enumerate(caps))
    )
    body = f"""<video id="presenter-one" class="clip presenter" src="assets/presenter-1.mp4" data-start="0" data-duration="{EDL[0]['duration_frames'] / L.FPS:.9f}" data-media-start="0" data-track-index="0" muted playsinline></video>
<video id="presenter-two" class="clip presenter" src="assets/presenter-2.mp4" data-start="{EDL[1]['timeline_in_frame'] / L.FPS:.9f}" data-duration="{EDL[1]['duration_frames'] / L.FPS:.9f}" data-media-start="0" data-track-index="0" muted playsinline></video>
<audio id="locked-voice" class="clip" src="assets/voice.wav" data-start="0" data-duration="{spoken:.9f}" data-track-index="10" data-volume="1"></audio>
<div id="context" class="clip context" data-start="0" data-duration="3.625" data-track-index="11">TOTAL BOOKING-SITE COMMISSIONS</div>
<div id="correction" class="clip correction" data-start="1.125" data-duration="2.5" data-track-index="12">&ne; Recoverable opportunity</div>
<div id="real-question" class="clip mini" data-start="5.166666667" data-duration="3.208333333" data-track-index="12">How much can actually shift?</div>
<div id="boundary" class="clip boundary" data-start="{boundary_start:.9f}" data-duration="{boundary_end - boundary_start:.9f}" data-track-index="12">Capped by what it recovers</div>
{caphtml}
{L.mount("end", cta_start, (END_CARD_FRAMES - 6) / L.FPS, 15)}"""

    (P / "index.html").write_text(
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        "<title>EP009 &middot; The commission total is the wrong number</title>"
        '<script src="assets/vendor/gsap.min.js"></script>'
        f"<style>{CSS}</style></head><body>"
        f'<div id="root" data-composition-id="main" data-start="0" data-duration="{total:.9f}" '
        f'data-width="1080" data-height="1920" data-fps="24">{body}</div>'
        "<script>window.__timelines={main:gsap.timeline({paused:true})};</script>"
        "</body></html>"
    )

    L.write_json(P / "index.motion.json", {
        "duration": total,
        "assertions": [
            {"kind": "appearsBy", "selector": "#context", "bySec": 0.1},
            {"kind": "appearsBy", "selector": "#correction", "bySec": 1.4},
            {"kind": "appearsBy", "selector": "#presenter-two",
             "bySec": EDL[1]["timeline_in_frame"] / L.FPS + 0.2},
            {"kind": "appearsBy", "selector": "#boundary", "bySec": boundary_start + 0.2},
            {"kind": "appearsBy", "selector": "#end-host", "bySec": cta_start + 0.2},
            {"kind": "staysInFrame", "selector": "#context"},
            {"kind": "staysInFrame", "selector": "#correction"},
            {"kind": "staysInFrame", "selector": "#boundary"},
            *({"kind": "staysInFrame", "selector": f"#caption-{i:02d}"} for i in range(len(caps))),
        ],
    })

    edits = []
    for e in EDL:
        edits.append({k: (str(v.relative_to(L.REPO)) if k == "native" else v)
                      for k, v in e.items()})
    L.write_json(P / "source-contract.json", {
        "schema": "ep009-standalone-payoff-short-v1",
        "revision": "EP009-SHORTS-004",
        "supersedes": "blueprint-cinema/experiments/EP009-SHORTS-003/04-wrong-number",
        "status": "private_review_candidate",
        "fps": L.FPS, "frame_count": TOTAL_FRAMES, "duration": total,
        "spoken_duration_frames": SPOKEN_FRAMES, "spoken_duration": spoken,
        "presenter_spoken_frames": PRESENTER_FRAMES,
        "presenter_spoken_fraction": PRESENTER_FRAMES / SPOKEN_FRAMES,
        "master": {"path": str(L.MASTER_WAV.relative_to(L.REPO)), "sha256": L.sha(L.MASTER_WAV)},
        "transcript": {"path": str(L.WORDS_JSON.relative_to(L.REPO)), "sha256": L.sha(L.WORDS_JSON)},
        "lock": {"path": str(L.LOCK_JSON.relative_to(L.REPO)), "sha256": L.sha(L.LOCK_JSON)},
        "edits": edits,
        "presenter_sources": [
            {"path": str(SEG037.relative_to(L.REPO)), "sha256": L.sha(SEG037)},
            {"path": str(SEG035.relative_to(L.REPO)), "sha256": L.sha(SEG035)},
        ],
        "recut": {
            "changed": "none. Both beats keep the r3 master frames 12495..12696 and "
                       "11307..11449 and the r3 native picture slices.",
            "judgment": "The r3 cut already resolves one narrow payoff inside itself: the "
                        "commission total is not the addressable amount, and what the inn can "
                        "pay is capped by what the job recovers.",
        },
        "audio_boundary": "Final cutoff 11449 excludes the next 'So' at 477.06s. Opening from "
                          "11307 removes the setup 'It's that'. Audio is taken from the locked "
                          "narration WAV at unity by sample boundary; r3 took it from the carrier "
                          "MP4's audio track.",
        "claim_boundary": "No amount or percentage retained without its spoken qualifications. "
                          "On-screen text only names total commissions, recoverable opportunity "
                          "and the recovery cap.",
        "on_screen_changes": [
            "new boundary overlay 'Capped by what it recovers' on the spoken 'what the job recovers'",
            "end card 'What can this inn actually afford?' -> 'The inn can only pay what the job "
            "recovers.'; the end card gains 6 frames so the longer headline holds",
        ],
        "related_video": {"required": True, "attached": False,
                          "target_episode": "EP009 direct-booking-practice", "url": None},
        "episode_url": "[EPISODE_URL]",
        "owner_approved": False, "published": False,
    })
    print(json.dumps({"frames": TOTAL_FRAMES, "duration": total,
                      "captions": len(caps),
                      "boundary": [round(boundary_start, 3), round(boundary_end, 3)]}, indent=2))


if __name__ == "__main__":
    main()
