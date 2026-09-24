#!/usr/bin/env python3
"""EP009 Short 02 r4 — cheap parts, and the job still left to sell.

Changes against EP009-SHORTS-003/02-cheap-tools:
  * a presenter orientation beat is added in front (master f1687..f1842, seg012
    native 0..155): "It helps a small hotel get its returning guests to book
    direct, instead of paying a booking site to meet them again." The r3 cut
    opened on "If the parts to fix this are cheap, why doesn't the inn just do
    it?", which names no hotel, no booking site and no commission; a cold viewer
    got the topic from the overlay alone. The new out point f1842 sits in the
    measured 3-frame gap after "again." (-46 dBFS) and before "By" at f1843.
  * the on-screen hook moves to the question beat, where the spoken line matches it.
  * the price boundary overlay is added on "But only for what it recovers".
  * the interrogative end card becomes a declarative one, hedged as the narration
    hedges it.
The question, tool-proof and return beats keep their accepted r3 frames.
"""
from pathlib import Path
import html
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import oe_shorts_r4 as L  # noqa: E402

P = Path(__file__).resolve().parent
SEG012 = L.NATIVES / "seg012/native.mp4"
SEG028 = L.NATIVES / "seg028/native.mp4"
SEG021 = L.NATIVES / "seg021/native.mp4"

# (master_in, master_out_exclusive, id, kind)
EDL = [
    (1687, 1842, "orient", "presenter"),
    (8790, 8883, "question", "presenter"),
    (16775, 16899, "proof", "tool_screen_recording"),
    (5360, 5516, "return", "presenter"),
]
END_CARD_FRAMES = 54
PRESENTERS = {
    "orient": (SEG012, 1687, "crop=608:1080:656:0,scale=1080:1920:flags=lanczos,setsar=1"),
    "question": (SEG028, 8754, "crop=608:1080:680:0,scale=1080:1920:flags=lanczos,setsar=1"),
    "return": (SEG021, 5351, "crop=608:1080:656:0,scale=1080:1920:flags=lanczos,setsar=1"),
}

CSS = """@font-face{font-family:Supreme;src:url('assets/fonts/supreme-500.woff2');font-weight:500}
@font-face{font-family:Supreme;src:url('assets/fonts/supreme-400.woff2');font-weight:400}
@font-face{font-family:Boska;src:url('assets/fonts/boska-700.woff2');font-weight:700}
*{box-sizing:border-box}body{margin:0}
#root{width:1080px;height:1920px;position:relative;overflow:hidden;font-family:Supreme,sans-serif;color:#FBF8F1}
.back{position:absolute;inset:0;background:#204440}
.presenter{position:absolute;inset:0;width:1080px;height:1920px;object-fit:cover}
.proof-back{position:absolute;inset:0;background:#204440;z-index:1}
.tool{z-index:2;position:absolute;left:0;top:480px;width:1080px;height:608px}
.caption{z-index:4;position:absolute;left:85px;top:1335px;width:830px;min-height:156px;display:flex;justify-content:center;align-items:center;text-align:center;font-size:60px;line-height:1.1;font-weight:500}
.caption span{display:block;padding:20px 26px;background:#173530;border-radius:12px;color:#FBF8F1}
.hook{position:absolute;left:85px;top:1130px;width:830px;min-height:148px;font-size:66px;line-height:1.03;font-weight:500;text-align:center}
.hook span{background:#173530;padding:12px 23px;box-decoration-break:clone;-webkit-box-decoration-break:clone}
.boundary{position:absolute;left:85px;top:1130px;width:830px;font-size:58px;line-height:1.06;font-weight:500;text-align:center}
.boundary span{background:#173530;padding:12px 23px;box-decoration-break:clone;-webkit-box-decoration-break:clone}
.proof-heading{z-index:3;position:absolute;left:85px;top:235px;width:820px;font-size:76px;line-height:1.04}
.proof-label{z-index:3;position:absolute;left:85px;top:365px;width:860px;font-size:32px;color:#FBF8F1}
.truth{z-index:3;position:absolute;left:85px;top:1190px;width:830px;font-size:35px;line-height:1.24;color:#FBF8F1}
.cta{z-index:6;position:absolute;inset:0;padding:355px 90px 200px;background:#204440;display:flex;flex-direction:column;align-items:flex-start}
.cta h1{font:700 104px/.98 Boska,serif;margin:0;max-width:890px}
.cta .sub{font:500 44px/1.2 Supreme,sans-serif;margin-top:64px;max-width:840px}
.cta .link{font:500 45px/1.15 Supreme,sans-serif;margin-top:62px;padding:24px 0;border-top:3px solid #FBF8F1;border-bottom:3px solid #FBF8F1;width:830px}
.credit{position:absolute;left:85px;top:1720px;width:830px;font:500 28px/1.3 Supreme,sans-serif;letter-spacing:.06em}"""

CTA = (
    '<h1>I think it can be<br>sold from outside.</h1>'
    '<p class="sub">For what it recovers. EP009 designs the job around that '
    'drafting step and computes that number on an illustrative inn.</p>'
    '<p class="link">EP009 &middot; Tap the related video &rarr;</p>'
    '<p class="credit">THE OPERATOR ECONOMY</p>'
)


def main() -> None:
    L.assert_locked()
    L.scaffold(P, "ep009-short02-cheap-tools-r4",
               ["supreme-500.woff2", "supreme-400.woff2", "boska-700.woff2"])
    wi = L.word_index()

    cursor = 0
    beats = []
    for a, b, ident, kind in EDL:
        ws = [w for w in wi.values() if a / L.FPS <= w["start"] < b / L.FPS]
        ws.sort(key=lambda w: w["start"])
        beats.append({
            "id": ident, "kind": kind, "source_in_frame": a, "source_out_frame_exclusive": b,
            "timeline_in_frame": cursor, "timeline_out_frame_exclusive": cursor + (b - a),
            "duration_frames": b - a,
            "word_in": ws[0]["w_id"], "word_out": ws[-1]["w_id"],
            "text": " ".join(w["token"] for w in ws),
        })
        cursor += b - a

    spoken_frames = cursor
    total_frames = spoken_frames + END_CARD_FRAMES
    spoken = spoken_frames / L.FPS
    total = total_frames / L.FPS

    # --- picture -------------------------------------------------------
    presenter_sources = []
    for beat in beats:
        if beat["id"] not in PRESENTERS:
            continue
        native, output_in, vf = PRESENTERS[beat["id"]]
        nin = beat["source_in_frame"] - output_in
        nout = beat["source_out_frame_exclusive"] - output_in
        chain = L.presenter_clip(native, P / f"assets/{beat['id']}.mp4", nin, nout, vf)
        presenter_sources.append({
            "beat": beat["id"], "path": str(native.relative_to(L.REPO)), "sha256": L.sha(native),
            "native_in_frame": nin, "native_out_frame_exclusive": nout, "transform": chain,
        })
    L.carrier_clip(P / "assets/tools.mp4", 16775, 124, "scale=1080:608:flags=lanczos,setsar=1")
    L.carrier_clip(P / "assets/tool-node.mp4", 16794, 60,
                   "crop=640:400:640:40,scale=1080:676:flags=lanczos,setsar=1")

    # --- audio ---------------------------------------------------------
    L.cut_voice([(b["source_in_frame"], b["source_out_frame_exclusive"]) for b in beats],
                P / "assets/voice.wav", stereo=True)

    # --- captions ------------------------------------------------------
    shifts = {}
    for beat in beats:
        lo, hi = int(beat["word_in"][1:]), int(beat["word_out"][1:])
        for n in range(lo, hi + 1):
            shifts[f"W{n:06d}"] = (beat["timeline_in_frame"] - beat["source_in_frame"]) / L.FPS
    spans = [
        ("W000195", "W000199"), ("W000200", "W000206"), ("W000207", "W000212"),
        ("W000213", "W000216"),
        ("W001024", "W001031"), ("W001032", "W001038"),
        ("W002018", "W002024"), ("W002025", "W002027"), ("W002028", "W002035"),
        ("W000646", "W000653"), ("W000654", "W000659"), ("W000660", "W000666"),
    ]
    caps = L.caption_groups(wi, spans, lambda k: shifts[k], spoken)
    beat_end = {}
    for beat in beats:
        lo, hi = int(beat["word_in"][1:]), int(beat["word_out"][1:])
        for n in range(lo, hi + 1):
            beat_end[f"W{n:06d}"] = beat["timeline_out_frame_exclusive"] / L.FPS
    for c in caps:
        c["end"] = round(min(c["end"], beat_end[c["words"][0]]), 6)
    L.write_json(P / "captions.json", caps)
    L.write_srt(caps, P / "captions.srt")
    L.write_vtt(caps, P / "captions.vtt")

    t = {b["id"]: (b["timeline_in_frame"] / L.FPS, b["duration_frames"] / L.FPS) for b in beats}
    # "But only for what it recovers" begins at W000654.
    boundary_start = wi["W000654"]["start"] + shifts["W000654"]
    boundary_end = wi["W000659"]["end"] + shifts["W000659"]

    L.sub_composition(
        P, "cta", CSS, f'<div class="cta">{CTA}</div>', END_CARD_FRAMES / L.FPS,
        anim="tl.fromTo('.cta h1',{y:20,opacity:0},{y:0,opacity:1,duration:.16,"
             "ease:'power2.out',immediateRender:false},0);",
    )

    caphtml = "\n".join(
        f'<div id="caption-{i}" class="clip caption" data-start="{c["start"]:.9f}" '
        f'data-duration="{c["end"] - c["start"]:.9f}" data-track-index="{20 + i}" '
        f'data-layout-allow-caption-zone><span>{html.escape(c["text"])}</span></div>'
        for i, c in enumerate(caps)
    )
    proof_start, proof_dur = t["proof"]
    body = f"""<div class="back"></div>
<video id="orient" class="clip presenter" src="assets/orient.mp4" data-start="{t['orient'][0]:.9f}" data-duration="{t['orient'][1]:.9f}" data-media-start="0" data-track-index="0" muted playsinline></video>
<video id="question" class="clip presenter" src="assets/question.mp4" data-start="{t['question'][0]:.9f}" data-duration="{t['question'][1]:.9f}" data-media-start="0" data-track-index="0" muted playsinline></video>
<div id="orient-hook" class="clip hook" data-start="{t['orient'][0]:.9f}" data-duration="{t['orient'][1]:.9f}" data-track-index="3"><span>A direct-booking practice</span></div>
<div id="hook" class="clip hook" data-start="{t['question'][0]:.9f}" data-duration="{t['question'][1]:.9f}" data-track-index="3"><span>Cheap parts. The job isn't.</span></div>
<div id="proof-back" class="clip proof-back" data-start="{proof_start:.9f}" data-duration="{proof_dur:.9f}" data-track-index="1"></div>
<video id="tool-overview" class="clip tool" src="assets/tools.mp4" data-start="{proof_start:.9f}" data-duration="{19 / L.FPS:.9f}" data-media-start="0" data-track-index="2" muted playsinline></video>
<video id="tool-node" class="clip tool" style="height:676px" src="assets/tool-node.mp4" data-start="{proof_start + 19 / L.FPS:.9f}" data-duration="{60 / L.FPS:.9f}" data-media-start="0" data-track-index="2" muted playsinline></video>
<video id="tool-draft" class="clip tool" src="assets/tools.mp4" data-start="{proof_start + 79 / L.FPS:.9f}" data-duration="{45 / L.FPS:.9f}" data-media-start="{79 / L.FPS:.9f}" data-track-index="2" muted playsinline></video>
<div id="proof-heading" class="clip proof-heading" data-start="{proof_start:.9f}" data-duration="{proof_dur:.9f}" data-track-index="4">The tool can draft.</div>
<div id="proof-label" class="clip proof-label" data-start="{proof_start:.9f}" data-duration="{proof_dur:.9f}" data-track-index="5">Node-RED + OpenAI &middot; recorded workflow</div>
<div id="truth" class="clip truth" data-start="{proof_start:.9f}" data-duration="{proof_dur:.9f}" data-track-index="6">Fictional guest. Awaiting human review. No sending available.</div>
<video id="return" class="clip presenter" src="assets/return.mp4" data-start="{t['return'][0]:.9f}" data-duration="{t['return'][1]:.9f}" data-media-start="0" data-track-index="0" muted playsinline></video>
<div id="boundary" class="clip boundary" data-start="{boundary_start:.9f}" data-duration="{boundary_end - boundary_start:.9f}" data-track-index="7"><span>Priced to what it recovers</span></div>
{caphtml}
{L.mount("cta", spoken, END_CARD_FRAMES / L.FPS, 10)}
<audio id="voice" src="assets/voice.wav" data-start="0" data-duration="{spoken:.9f}" data-track-index="50" data-volume="1"></audio>"""

    (P / "index.html").write_text(
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        "<title>EP009 &middot; Cheap parts, and a job still left to sell</title>"
        '<script src="assets/vendor/gsap.min.js"></script>'
        f"<style>{CSS}</style></head><body>"
        f'<main id="root" data-composition-id="main" data-start="0" data-duration="{total:.9f}" '
        f'data-width="1080" data-height="1920" data-fps="24">{body}</main>'
        "<script>window.__timelines={main:gsap.timeline({paused:true})};</script>"
        "</body></html>"
    )

    L.write_json(P / "index.motion.json", {
        "duration": total,
        "assertions": [
            {"kind": "appearsBy", "selector": "#orient", "bySec": 0.1},
            {"kind": "appearsBy", "selector": "#orient-hook", "bySec": 0.1},
            {"kind": "appearsBy", "selector": "#question", "bySec": t["question"][0] + 0.15},
            {"kind": "appearsBy", "selector": "#proof-heading", "bySec": proof_start + 0.2},
            {"kind": "appearsBy", "selector": "#return", "bySec": t["return"][0] + 0.2},
            {"kind": "appearsBy", "selector": "#boundary", "bySec": boundary_start + 0.2},
            {"kind": "appearsBy", "selector": "#cta-host", "bySec": spoken + 0.2},
            *({"kind": "staysInFrame", "selector": f"#caption-{i}"} for i in range(len(caps))),
            {"kind": "staysInFrame", "selector": "#truth"},
        ],
    })

    presenter_spoken = sum(b["duration_frames"] for b in beats if b["kind"] == "presenter")
    L.write_json(P / "source-contract.json", {
        "schema": "ep009-standalone-payoff-short-v1",
        "revision": "EP009-SHORTS-004",
        "supersedes": "blueprint-cinema/experiments/EP009-SHORTS-003/02-cheap-tools",
        "status": "private_review_candidate",
        "fps": L.FPS, "frame_count": total_frames, "duration": total,
        "spoken_duration_frames": spoken_frames, "spoken_duration": spoken,
        "presenter_spoken_frames": presenter_spoken,
        "presenter_spoken_fraction": presenter_spoken / spoken_frames,
        "master": {"path": str(L.MASTER_WAV.relative_to(L.REPO)), "sha256": L.sha(L.MASTER_WAV)},
        "transcript": {"path": str(L.WORDS_JSON.relative_to(L.REPO)), "sha256": L.sha(L.WORDS_JSON)},
        "tool_carrier": {"path": str(L.CARRIER.relative_to(L.REPO)), "sha256": L.sha(L.CARRIER)},
        "lock": {"path": str(L.LOCK_JSON.relative_to(L.REPO)), "sha256": L.sha(L.LOCK_JSON)},
        "segments": beats,
        "presenter_sources": presenter_sources,
        "tool_visual_ranges": [
            {"asset": "assets/tools.mp4", "source_frames": [16775, 16794],
             "treatment": "Full tool overview, scaled to 1080x608"},
            {"asset": "assets/tool-node.mp4", "source_frames": [16794, 16854],
             "treatment": "OpenAI node crop 640x400 at 640,40 then 1080x676"},
            {"asset": "assets/tools.mp4", "source_frames": [16854, 16899],
             "treatment": "Returned-draft panel, r8 directed zoom retained"},
        ],
        "recut": {
            "changed": "presenter orientation beat added in front, master f1687..f1842 "
                       "(seg012 native 0..155, W000195..W000216)",
            "cut_in_silence": "out point f1842 measures -41.9 dBFS between the decay of "
                              "'again.' (audible content ends near f1840) and 'By' at f1843.9; "
                              "the gap is 3 frames, the shortest join in the package",
            "gain": "presenter share of speech rises from 0.668 (r3) to "
                    f"{presenter_spoken / spoken_frames:.3f}",
            "picture_unchanged": "seg028 native 36..129, seg021 native 9..165 and the three "
                                 "carrier tool ranges are the accepted r3 slices",
        },
        "on_screen_changes": [
            "new orientation overlay 'A direct-booking practice' (25 chars) resolves the spoken 'It'",
            "'Why pay for cheap tools?' -> 'Cheap parts. The job isn't.' and moved to the question beat",
            "new boundary overlay 'Priced to what it recovers' on the spoken 'But only for what it recovers'",
            "end card 'What work would an inn pay for?' -> 'I think it can be sold from outside.'",
        ],
        "constraints": [
            "No voice or performance generation.",
            "No retime, loops, added gestures or expression changes.",
            f"Silent {END_CARD_FRAMES}-frame designed end card.",
            "Private review; exact Related Video target remains unbound.",
        ],
        "related_video": {"required": True, "attached": False,
                          "target_episode": "EP009 direct-booking-practice", "url": None},
        "episode_url": "[EPISODE_URL]",
        "owner_approved": False, "published": False,
    })
    print(json.dumps({"frames": total_frames, "duration": total,
                      "presenter_fraction": presenter_spoken / spoken_frames,
                      "captions": len(caps)}, indent=2))


if __name__ == "__main__":
    main()
