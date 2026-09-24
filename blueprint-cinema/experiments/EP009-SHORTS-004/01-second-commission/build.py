#!/usr/bin/env python3
"""EP009 Short 01 r4 — the second commission, brought onto the standalone-payoff standard.

Changes against EP009-SHORTS-003/01-second-commission:
  * the proof beat is extended by one sentence, master f870 -> f948, so the payoff
    resolves out loud ("For a guest she already knows by name.") instead of stopping
    mid-thought. The new out point sits in measured silence (-72 dBFS at f944,
    -76 dBFS at f948; next word W000110 begins at f973.4).
  * the proof card headline no longer repeats the opening overlay verbatim.
  * the interrogative end card is replaced by a declarative one. Nothing on screen
    asks a question the Short does not answer.
Presenter and proof picture slices are otherwise the accepted r3 frames.
"""
from pathlib import Path
import html
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import oe_shorts_r4 as L  # noqa: E402

P = Path(__file__).resolve().parent
NATIVE = L.NATIVES / "seg009/native.mp4"
SEG009_OUTPUT_IN = 1207  # look-transfer output frame that maps to native frame 0

# (master_in, master_out_exclusive, first_word, last_word, kind)
EDL = [
    (1328, 1427, "W000151", "W000165", "presenter"),
    (780, 948, "W000089", "W000109", "proof"),
    (1220, 1300, "W000140", "W000149", "presenter"),
]
END_CARD_FRAMES = 54
CROP = "crop=760:1080:570:0,scale=1080:1534,pad=1080:1920:0:180:color=0x173530,setsar=1"

CSS = """@font-face{font-family:Supreme;src:url(assets/fonts/supreme-500.woff2);font-weight:500}
@font-face{font-family:Zodiak;src:url(assets/fonts/zodiak-700.woff2);font-weight:700}
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1080px;height:1920px;overflow:hidden;background:#173530}
#root{position:relative;width:1080px;height:1920px;overflow:hidden;color:#F5F0E6;font:500 40px/1.1 Supreme,sans-serif}
.clip{position:absolute}
.presenter{inset:0;width:1080px;height:1920px}
.context{left:70px;top:76px;width:900px;font-size:47px;z-index:8}
.caption{left:70px;top:1260px;width:865px;text-align:center;font-size:62px;line-height:1.12;letter-spacing:-.02em;z-index:20}
.caption span{display:inline-block;background:#173530;padding:17px 25px 22px;border-radius:6px}
.brand{left:70px;top:1768px;font-size:25px;letter-spacing:.06em;z-index:9}
.proof{inset:0;width:1080px;height:1920px;background:#F5F0E6;color:#173530;padding:290px 75px 0;z-index:2}
.proof h1{font:700 96px/1.03 Zodiak,serif;letter-spacing:-.035em;margin-bottom:85px}
.row{border-top:3px solid #586D74;padding:28px 0 40px}
.row small{font-size:28px;letter-spacing:.06em;color:#586D74}
.row p{font-size:74px;margin-top:25px}
.row.second{border-color:#B5482F}
.same{color:#B5482F;font-size:42px;margin-top:28px}
.already{margin-top:46px;border-top:3px solid #586D74;padding-top:30px;font-size:46px;line-height:1.16;color:#173530}
.fixture{position:absolute;left:75px;top:1740px;color:#586D74;font-size:26px}
.end{inset:0;background:#173530;color:#F5F0E6;z-index:30;padding:340px 78px 0}
.end small{font-size:27px;letter-spacing:.06em}
.end h1{font:700 103px/1.02 Zodiak,serif;letter-spacing:-.04em;margin-top:60px}
.end p{font-size:42px;margin-top:70px;line-height:1.2}
.end .action{display:inline-block;background:#F5F0E6;color:#173530;padding:22px 26px;font-size:34px;margin-top:40px}
.line{height:8px;width:180px;background:#B5482F;margin-top:45px;transform-origin:0 50%}"""

PROOF = (
    '<div class="proof">'
    '<h1>Booked again.<br>Billed again.</h1>'
    '<div class="row"><small>FIRST STAY</small><p>Commission paid</p></div>'
    '<div id="repeat" class="row second"><small>RETURN VISIT</small><p>Commission paid</p>'
    '<div class="same">SAME CHARGE. AGAIN.</div></div>'
    '<div id="already" class="already">A guest the inn already had.</div>'
    '<div class="fixture">Illustrative small-inn story</div>'
    "</div>"
)

END = (
    '<div class="end">'
    '<small>THE OPERATOR ECONOMY &middot; EP009</small>'
    '<h1>The inn pays<br>the commission<br>again.</h1>'
    '<div class="line"></div>'
    '<p>EP009 runs the arithmetic on an illustrative inn.</p>'
    '<div class="action">TAP THE RELATED VIDEO &rarr;</div>'
    "</div>"
)


def main() -> None:
    L.assert_locked()
    L.scaffold(P, "ep009-short01-second-commission-r4",
               ["supreme-500.woff2", "zodiak-700.woff2"])
    wi = L.word_index()

    # --- picture -------------------------------------------------------
    natives = {}
    cursor = 0
    timeline = []
    for i, (a, b, w0, w1, kind) in enumerate(EDL):
        timeline.append({"index": i, "in": a, "out": b, "kind": kind,
                         "timeline_in_frame": cursor, "duration_frames": b - a,
                         "first_word": w0, "last_word": w1,
                         "text": " ".join(wi[f"W{n:06d}"]["token"]
                                          for n in range(int(w0[1:]), int(w1[1:]) + 1))})
        if kind == "presenter":
            chain = L.presenter_clip(NATIVE, P / f"assets/presenter-{i}.mp4",
                                     a - SEG009_OUTPUT_IN, b - SEG009_OUTPUT_IN, CROP)
            natives[i] = {"path": str(NATIVE.relative_to(L.REPO)), "sha256": L.sha(NATIVE),
                          "in_frame": a - SEG009_OUTPUT_IN,
                          "out_frame_exclusive": b - SEG009_OUTPUT_IN,
                          "transform": chain}
        cursor += b - a

    spoken_frames = cursor
    total_frames = spoken_frames + END_CARD_FRAMES
    spoken = spoken_frames / L.FPS
    total = total_frames / L.FPS

    # --- audio ---------------------------------------------------------
    L.cut_voice([(a, b) for a, b, *_ in EDL], P / "assets/voice.wav")

    # --- captions ------------------------------------------------------
    shifts = {}
    for beat in timeline:
        for n in range(int(beat["first_word"][1:]), int(beat["last_word"][1:]) + 1):
            shifts[f"W{n:06d}"] = (beat["timeline_in_frame"] - beat["in"]) / L.FPS
    spans = [("W000151", "W000155"), ("W000156", "W000158"), ("W000159", "W000165"),
             ("W000089", "W000093"), ("W000094", "W000101"), ("W000102", "W000109"),
             ("W000140", "W000145"), ("W000146", "W000149")]
    caps = L.caption_groups(wi, spans, lambda k: shifts[k], spoken)
    L.write_json(P / "captions.json", caps)
    L.write_srt(caps, P / "captions.srt")
    L.write_vtt(caps, P / "captions.vtt")

    # --- composition ---------------------------------------------------
    proof_start = timeline[1]["timeline_in_frame"] / L.FPS
    proof_dur = timeline[1]["duration_frames"] / L.FPS
    close_start = timeline[2]["timeline_in_frame"] / L.FPS
    close_dur = timeline[2]["duration_frames"] / L.FPS
    already_at = proof_start + (882 - timeline[1]["in"]) / L.FPS  # on "For a guest"

    videos = "".join(
        f'<video id="presenter-{b["index"]}" class="clip presenter" '
        f'src="assets/presenter-{b["index"]}.mp4" '
        f'data-start="{b["timeline_in_frame"] / L.FPS:.9f}" '
        f'data-duration="{b["duration_frames"] / L.FPS:.9f}" '
        f'data-media-start="0" data-track-index="1" muted playsinline></video>'
        for b in timeline if b["kind"] == "presenter"
    )
    caphtml = "".join(
        f'<div id="caption-{i}" class="clip caption" data-start="{c["start"]:.9f}" '
        f'data-duration="{c["end"] - c["start"]:.9f}" data-track-index="20">'
        f'<span>{html.escape(c["text"])}</span></div>'
        for i, c in enumerate(caps)
    )
    L.sub_composition(
        P, "proof", CSS, PROOF, proof_dur,
        anim="tl.fromTo('#repeat',{y:30,opacity:0},{y:0,opacity:1,duration:.25,"
             "ease:'power2.out'},1.1);"
             "tl.fromTo('#already',{y:24,opacity:0},{y:0,opacity:1,duration:.22,"
             f"ease:'power2.out'}},{(882 - timeline[1]['in']) / L.FPS:.6f});",
    )
    L.sub_composition(
        P, "close", CSS, END, END_CARD_FRAMES / L.FPS,
        anim="tl.fromTo('.line',{scaleX:0},{scaleX:1,duration:.25,"
             "ease:'power2.out'},0);",
    )
    body = (
        videos
        + L.mount("proof", proof_start, proof_dur, 2)
        + L.mount("close", spoken, END_CARD_FRAMES / L.FPS, 30)
        + caphtml
        + f'<audio id="voice" src="assets/voice.wav" data-start="0" '
          f'data-duration="{spoken:.9f}" data-track-index="10" data-volume="1"></audio>'
        + f'<div id="context" class="clip context" data-start="0" '
          f'data-duration="{proof_start:.9f}" data-track-index="8">Same guest. Second commission.</div>'
        + f'<div id="return-context" class="clip context" data-start="{close_start:.9f}" '
          f'data-duration="{close_dur:.9f}" data-track-index="8">The missing arithmetic.</div>'
        + f'<div id="opening-brand" class="clip brand" data-start="0" '
          f'data-duration="{proof_start:.9f}" data-track-index="9">THE OPERATOR ECONOMY &middot; EP009</div>'
        + f'<div id="return-brand" class="clip brand" data-start="{close_start:.9f}" '
          f'data-duration="{close_dur:.9f}" data-track-index="9">THE OPERATOR ECONOMY &middot; EP009</div>'
    )
    script = "window.__timelines={main:gsap.timeline({paused:true})};"
    (P / "index.html").write_text(
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        "<title>EP009 &middot; The second commission</title>"
        '<script src="assets/vendor/gsap.min.js"></script>'
        f"<style>{CSS}</style></head><body>"
        f'<main id="root" data-composition-id="main" data-start="0" data-duration="{total:.9f}" '
        f'data-width="1080" data-height="1920" data-fps="24">{body}</main>'
        f"<script>{script}</script></body></html>"
    )

    L.write_json(P / "index.motion.json", {
        "duration": total,
        "assertions": [
            {"kind": "appearsBy", "selector": "#presenter-0", "bySec": 0.1},
            {"kind": "appearsBy", "selector": "#proof-host", "bySec": proof_start + 0.15},
            {"kind": "appearsBy", "selector": "#already", "bySec": already_at + 0.35},
            {"kind": "appearsBy", "selector": "#presenter-2", "bySec": close_start + 0.15},
            {"kind": "appearsBy", "selector": "#close-host", "bySec": spoken + 0.15},
            *({"kind": "staysInFrame", "selector": f"#caption-{i}"} for i in range(len(caps))),
            {"kind": "staysInFrame", "selector": "#context"},
        ],
    })

    edl = []
    for b in timeline:
        entry = {
            "id": b["index"], "source_in_frame": b["in"], "source_out_frame_exclusive": b["out"],
            "timeline_in_frame": b["timeline_in_frame"], "duration_frames": b["duration_frames"],
            "first_word": b["first_word"], "last_word": b["last_word"], "text": b["text"],
            "visual": b["kind"],
            "picture_audio_mode": "presenter_address" if b["kind"] == "presenter" else "silent_graphic",
        }
        if b["index"] in natives:
            entry["native"] = natives[b["index"]]
        edl.append(entry)

    presenter_spoken = sum(b["duration_frames"] for b in timeline if b["kind"] == "presenter")
    L.write_json(P / "source-contract.json", {
        "schema": "ep009-standalone-payoff-short-v1",
        "revision": "EP009-SHORTS-004",
        "supersedes": "blueprint-cinema/experiments/EP009-SHORTS-003/01-second-commission",
        "status": "private_review_candidate",
        "fps": L.FPS, "frame_count": total_frames, "duration": total,
        "spoken_duration_frames": spoken_frames, "spoken_duration": spoken,
        "presenter_spoken_frames": presenter_spoken,
        "presenter_spoken_fraction": presenter_spoken / spoken_frames,
        "edl": edl,
        "voice": {"path": str(L.MASTER_WAV.relative_to(L.REPO)), "sha256": L.sha(L.MASTER_WAV)},
        "transcript": {"path": str(L.WORDS_JSON.relative_to(L.REPO)), "sha256": L.sha(L.WORDS_JSON)},
        "lock": {"path": str(L.LOCK_JSON.relative_to(L.REPO)), "sha256": L.sha(L.LOCK_JSON)},
        "recut": {
            "changed": "proof beat extended from master f870 to f948 (one sentence, W000102..W000109)",
            "cut_in_silence": "out point f948 measures -76.1 dBFS; the word before ends at f940.1 and "
                              "the next word W000110 begins at f973.4",
            "cost": "presenter share of speech falls from 0.665 (r3) to "
                    f"{presenter_spoken / spoken_frames:.3f}; still presenter-majority and the Short "
                    "still opens and closes on the presenter",
            "picture_unchanged": "seg009 native frames 121..220 and 13..93, same crop as r3",
        },
        "on_screen_changes": [
            "proof headline 'Same guest. Second commission.' -> 'Booked again. Billed again.'",
            "new proof reveal 'A guest the inn already had.' on the added sentence",
            "end card 'What could the inn actually pay?' -> 'The inn pays the commission again.'",
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
