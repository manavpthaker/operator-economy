#!/usr/bin/env python3
"""EP009 Short 03 r4 — the one-beat re-cut the owner ruled on (2026-09-21).

Changes against EP009-SHORTS-003/03-guest-relationship:
  * the cut extends from master f4844 to f4890 so the answer is spoken inside the
    Short: W000584..W000588, "Nobody at the inn is." The r3 contract recorded that
    word as next_word_excluded. The new out point f4890 measures -65.8 dBFS; the
    sentence ends at f4880.4 and the following "And" begins at f4895.8.
  * the end card that repeated the question just spoken ("Who owns the second
    booking?") is gone. The card now states the answer, revealing on the spoken
    line, and the routing copy arrives after it in silence.
  * a cold-viewer hook line is added in the first two seconds.
Picture: the answer beat has no look-transfer presenter coverage. seg019 ends at
output frame 4844 and seg019b's native runs out at 4851, so the answer is carried
by a designed card under locked narration, which is the silent_graphic mode
already accepted in this revision's Short 01 proof insert. Recorded, not hidden.
"""
from pathlib import Path
import html
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import oe_shorts_r4 as L  # noqa: E402

P = Path(__file__).resolve().parent
WIDE = L.NATIVES / "seg019a/native.mp4"
CLOSE = L.NATIVES / "seg019b/native.mp4"

AUDIO_IN = 4510
AUDIO_OUT = 4890            # r3 stopped at 4844
WIDE_FRAMES = (60, 333)     # native, maps master 4510..4783
CLOSE_FRAMES = (45, 106)    # native, maps master 4783..4844
CARD_FRAMES = 78            # 46 spoken + 32 silent routing hold
SPOKEN_FRAMES = AUDIO_OUT - AUDIO_IN            # 380
PICTURE_CUT = 4844 - AUDIO_IN                   # 334
TOTAL_FRAMES = PICTURE_CUT + CARD_FRAMES        # 412

CSS = """@font-face{font-family:Supreme;src:url('assets/fonts/supreme-500.woff2');font-weight:500}
@font-face{font-family:Zodiak;src:url('assets/fonts/zodiak-700.woff2');font-weight:700}
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1080px;height:1920px;overflow:hidden;background:#173530}
#root{width:1080px;height:1920px;position:relative;overflow:hidden;font-family:Supreme,Arial,sans-serif;color:#F5F0E6}
.fill{position:absolute;inset:0;background:#173530}
.avatar{position:absolute;inset:0;width:1080px;height:1920px;object-fit:fill}
.brand{position:absolute;top:65px;left:64px;width:500px;font-size:26px;letter-spacing:.12em;padding:16px 20px;background:#173530;color:#F5F0E6;z-index:60}
.caption{position:absolute;left:78px;top:1470px;width:836px;padding:22px 28px;text-align:center;background:#173530;color:#F5F0E6;font:500 68px/1.12 Supreme,Arial,sans-serif;letter-spacing:-.02em;z-index:30}
.cue{position:absolute;top:143px;left:64px;width:850px;height:123px;z-index:20;background:#F5F0E6;color:#173530;display:flex;align-items:center;justify-content:space-between;padding:25px 30px;gap:24px;font-size:40px}
.cue b{font-weight:500}
.cue svg{width:92px;height:42px;flex-shrink:0}
.cue path{fill:none;stroke:#B5482F;stroke-width:5;stroke-linecap:round;stroke-linejoin:round}
.hook{position:absolute;top:143px;left:64px;width:850px;height:123px;z-index:22;background:#F5F0E6;color:#173530;display:flex;align-items:center;padding:25px 30px;font:500 46px/1.1 Supreme,Arial,sans-serif}
.answer{position:absolute;inset:0;width:1080px;height:1920px;z-index:25}
.answer-fill{position:absolute;inset:0;background:#173530}
.headline{position:absolute;left:78px;top:400px;width:860px;font:700 126px/1.03 Zodiak,Georgia,serif;letter-spacing:-.03em;color:#F5F0E6}
.route-line{position:absolute;left:78px;top:1112px;width:830px;height:4px;background:#FB8B69;transform-origin:0 50%}
.route{position:absolute;left:78px;top:1190px;width:830px;font:500 47px/1.2 Supreme,Arial,sans-serif;color:#F5F0E6}
.route span{display:block;margin-top:34px;color:#FB8B69;font-size:47px}"""

ANSWER = (
    '<div class="answer-fill"></div>'
    '<h1 id="headline" class="headline">Nobody at<br>the inn is.</h1>'
    '<div id="route-line" class="route-line"></div>'
    '<p id="route" class="route">EP009 asks whether somebody outside the property can be'
    '<span>Tap the related video &rarr;</span></p>'
)

ARROW = ('<svg viewBox="0 0 92 42"><path d="M4 21 H82 M68 6 L84 21 L68 36"/></svg>')


def main() -> None:
    L.assert_locked()
    L.scaffold(P, "ep009-short03-guest-relationship-r4",
               ["supreme-500.woff2", "zodiak-700.woff2"])
    wi = L.word_index()

    # --- picture (accepted r3 slices, unchanged) ------------------------
    wide_chain = L.presenter_clip(
        WIDE, P / "assets/avatar-wide.mp4", *WIDE_FRAMES,
        "crop=960:1080:360:0,scale=1080:1216,pad=1080:1920:0:200:color=0x173530,setsar=1")
    close_chain = L.presenter_clip(
        CLOSE, P / "assets/avatar-close.mp4", *CLOSE_FRAMES,
        "crop=608:1080:640:0,scale=1080:1920,setsar=1")

    # --- audio (extended by the answer beat) ---------------------------
    L.cut_voice([(AUDIO_IN, AUDIO_OUT)], P / "assets/voice.wav")

    shift = -AUDIO_IN / L.FPS
    spoken = SPOKEN_FRAMES / L.FPS
    total = TOTAL_FRAMES / L.FPS
    card_start = PICTURE_CUT / L.FPS

    # --- captions ------------------------------------------------------
    # The answer line is NOT railed: while the answer card is up its headline
    # carries those exact words, and a caption under it would duplicate the card
    # verbatim (docs/content-rubric.md edit kill list). It is in the sidecars.
    spans = [("W000538", "W000542"), ("W000543", "W000547"), ("W000548", "W000552"),
             ("W000553", "W000558"), ("W000559", "W000562"), ("W000563", "W000568"),
             ("W000569", "W000574"), ("W000575", "W000578"), ("W000579", "W000583")]
    caps = L.caption_groups(wi, spans, lambda _k: shift, card_start, tail=0.07)
    L.write_json(P / "captions.json", caps)

    answer_words = [wi[f"W{n:06d}"] for n in range(584, 589)]
    answer_start = answer_words[0]["start"] + shift
    answer_end = answer_words[-1]["end"] + shift
    sidecar = caps + [{
        "start": round(answer_start, 6), "end": round(min(answer_end + 0.1, spoken), 6),
        "text": " ".join(w["token"] for w in answer_words),
        "words": [w["w_id"] for w in answer_words],
    }]
    L.write_srt(sidecar, P / "captions.srt")
    L.write_vtt(sidecar, P / "captions.vtt")

    # --- composition ---------------------------------------------------
    L.sub_composition(P, "hook", CSS,
                      '<div class="hook">A small inn. A repeat guest.</div>', 1.791666667)
    L.sub_composition(P, "sitecue", CSS,
                      f'<div class="cue"><b>Booking site</b>{ARROW}'
                      '<b>Guest&rsquo;s email</b></div>', 2.25,
                      anim="const p=document.querySelectorAll('.cue path');"
                           "p.forEach(q=>{const n=q.getTotalLength();"
                           "q.style.strokeDasharray=n;q.style.strokeDashoffset=n;});"
                           "tl.to('.cue path',{strokeDashoffset:0,duration:.45,"
                           "ease:'power2.out'},.17);")
    L.sub_composition(P, "returncue", CSS,
                      f'<div class="cue"><b>Returning guest</b>{ARROW}'
                      '<b>The inn?</b></div>', 4.1,
                      anim="const p=document.querySelectorAll('.cue path');"
                           "p.forEach(q=>{const n=q.getTotalLength();"
                           "q.style.strokeDasharray=n;q.style.strokeDashoffset=n;});"
                           "tl.to('.cue path',{strokeDashoffset:0,duration:.45,"
                           "ease:'power2.out'},.15);")
    L.sub_composition(
        P, "answer", CSS, f'<div class="answer">{ANSWER}</div>', CARD_FRAMES / L.FPS,
        anim=(
            "tl.fromTo('#headline',{y:26,opacity:0},{y:0,opacity:1,duration:.24,"
            f"ease:'power2.out'}},{max(0.05, answer_start - card_start - 0.30):.6f});"
            "tl.fromTo('#route-line',{scaleX:0},{scaleX:1,duration:.3,"
            f"ease:'power2.out'}},{answer_end - card_start + 0.25:.6f});"
            "tl.fromTo('#route',{y:14,opacity:0},{y:0,opacity:1,duration:.22,"
            f"ease:'power2.out'}},{answer_end - card_start + 0.3:.6f});"
        ),
    )

    caphtml = "".join(
        f'<p id="cap-{i}" class="clip caption" data-start="{c["start"]:.9f}" '
        f'data-duration="{c["end"] - c["start"]:.9f}" data-track-index="30">'
        f'{html.escape(c["text"])}</p>'
        for i, c in enumerate(caps)
    )
    body = (
        '<div class="fill"></div>'
        f'<video id="wide-video" class="clip avatar" src="assets/avatar-wide.mp4" '
        f'data-start="0" data-duration="{(WIDE_FRAMES[1] - WIDE_FRAMES[0]) / L.FPS:.9f}" '
        f'data-media-start="0" data-track-index="1" muted playsinline></video>'
        f'<video id="close-video" class="clip avatar" src="assets/avatar-close.mp4" '
        f'data-start="{(WIDE_FRAMES[1] - WIDE_FRAMES[0]) / L.FPS:.9f}" '
        f'data-duration="{(CLOSE_FRAMES[1] - CLOSE_FRAMES[0]) / L.FPS:.9f}" '
        f'data-media-start="0" data-track-index="1" muted playsinline></video>'
        + L.mount("hook", 0.0, 1.791666667, 5)
        + L.mount("sitecue", 1.833333333, 2.25, 4)
        + L.mount("returncue", 5.25, 4.1, 4)
        + caphtml
        + L.mount("answer", card_start, CARD_FRAMES / L.FPS, 25)
        + f'<p id="brand" class="clip brand" data-start="0" data-duration="{total:.9f}" '
          f'data-track-index="40">THE OPERATOR ECONOMY</p>'
        + f'<audio id="voice" src="assets/voice.wav" data-start="0" '
          f'data-duration="{spoken:.9f}" data-media-start="0" data-track-index="50" '
          f'data-volume="1"></audio>'
    )
    (P / "index.html").write_text(
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        "<title>EP009 &middot; The booking site keeps the guest&rsquo;s email</title>"
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
            {"kind": "appearsBy", "selector": "#wide-video", "bySec": 0.1},
            {"kind": "appearsBy", "selector": "#hook-host", "bySec": 0.2},
            {"kind": "appearsBy", "selector": "#sitecue-host", "bySec": 2.1},
            {"kind": "appearsBy", "selector": "#returncue-host", "bySec": 5.6},
            {"kind": "appearsBy", "selector": "#close-video", "bySec": 11.5},
            {"kind": "appearsBy", "selector": "#answer-host", "bySec": card_start + 0.2},
            {"kind": "appearsBy", "selector": "#headline", "bySec": answer_start + 0.4},
            {"kind": "appearsBy", "selector": "#route", "bySec": answer_end + 0.7},
            *({"kind": "staysInFrame", "selector": f"#cap-{i}"} for i in range(len(caps))),
            {"kind": "staysInFrame", "selector": "#hook-host"},
        ],
    })

    L.write_json(P / "source-contract.json", {
        "schema": "ep009-standalone-payoff-short-v1",
        "revision": "EP009-SHORTS-004",
        "supersedes": "blueprint-cinema/experiments/EP009-SHORTS-003/03-guest-relationship",
        "status": "private_review_candidate",
        "fps": L.FPS, "frame_count": TOTAL_FRAMES, "duration": total,
        "spoken_duration_frames": SPOKEN_FRAMES, "spoken_duration": spoken,
        "audio": {"path": str(L.MASTER_WAV.relative_to(L.REPO)),
                  "sha256": L.sha(L.MASTER_WAV),
                  "frames": [AUDIO_IN, AUDIO_OUT],
                  "sample_range": [AUDIO_IN * L.SAMPLES_PER_FRAME,
                                   AUDIO_OUT * L.SAMPLES_PER_FRAME]},
        "transcript": {"path": str(L.WORDS_JSON.relative_to(L.REPO)), "sha256": L.sha(L.WORDS_JSON)},
        "lock": {"path": str(L.LOCK_JSON.relative_to(L.REPO)), "sha256": L.sha(L.LOCK_JSON)},
        "presenter_sources": [
            {"id": "wide", "path": str(WIDE.relative_to(L.REPO)), "sha256": L.sha(WIDE),
             "global_frames": [4510, 4783], "native_frames": list(WIDE_FRAMES),
             "timeline_frames": [0, 273], "transform": wide_chain},
            {"id": "close", "path": str(CLOSE.relative_to(L.REPO)), "sha256": L.sha(CLOSE),
             "global_frames": [4783, 4844], "native_frames": list(CLOSE_FRAMES),
             "timeline_frames": [273, 334], "transform": close_chain},
        ],
        "answer_beat": {
            "words": ["W000584", "W000585", "W000586", "W000587", "W000588"],
            "text": "Nobody at the inn is.",
            "master_frames": [4844, AUDIO_OUT],
            "timeline_frames": [PICTURE_CUT, SPOKEN_FRAMES],
            "picture": "designed answer card",
            "picture_audio_mode": "silent_graphic",
            "why_not_presenter": "seg019 look-transfer output coverage ends at frame 4844 and "
                                 "seg019b's native runs out at global 4851, so no lip-synced "
                                 "presenter picture exists for master 4851..4890. No performance "
                                 "was generated to fill it.",
        },
        "recut": {
            "changed": "cut extended from master f4844 to f4890 to include W000584..W000588",
            "cut_in_silence": "out point f4890 measures -65.8 dBFS; the sentence ends at f4880.4 "
                              "and the next word W000589 'And' begins at f4895.8",
            "removed": "the end card 'Who owns the second booking?', which repeated the question "
                       "the speech had just asked",
            "picture_unchanged": "seg019a native 60..333 and seg019b native 45..106, same crops "
                                 "and the same plain mineral framing accepted in r3",
        },
        "on_screen_changes": [
            "new hook line 'A small inn. A repeat guest.' (28 chars) at 0.000-1.792s",
            "the booking-site cue moves from 0.083s to 1.833s so it lands on the spoken "
            "'keeps the guest's email' instead of preceding it",
            "end card replaced by an answer card: 'Nobody at the inn is.'",
        ],
        "caption_note": "The answer line is not railed while the answer card carries those exact "
                        "words on screen; it is present in captions.srt and captions.vtt.",
        "related_video": {"required": True, "attached": False,
                          "target_episode": "EP009 direct-booking-practice", "url": None},
        "episode_url": "[EPISODE_URL]",
        "owner_approved": False, "published": False,
    })
    print(json.dumps({"frames": TOTAL_FRAMES, "duration": total,
                      "spoken_frames": SPOKEN_FRAMES, "captions": len(caps),
                      "answer": [round(answer_start, 3), round(answer_end, 3)]}, indent=2))


if __name__ == "__main__":
    main()
