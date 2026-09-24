#!/usr/bin/env python3
"""Build the mobile-framed R78 revisions from the verified R77 source captures.

The only changed pixels are the presentation crop of each real screen recording.
The actual cursor is preserved inside the source picture; no cursor, UI, text, audio,
or interaction is synthesized.
"""
import argparse
import hashlib
import json
import pathlib
import shutil
import subprocess
import wave

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[5]
R77 = ROOT / "blueprint-cinema/episodes/EP007-exit-readiness-prep/agents/deliverables/R77-TOOL-INSERT-BUILD"
REVIEWS = ROOT / "blueprint-cinema/experiments/EP007-NET-NEW-UNFINISHED-ANSWER-003/hyperframes/reviews"
MASTER = ROOT / "operator-blueprint-v2/episodes/EP007-exit-readiness-prep/02-narration-production/master/narration-master.v4.wav"
MASTER_HASH = "d8f7cb9630ae12ad427dca2c7bd1f29611f56c7985ce900ea312df3b9fec8da9"
FONT = ROOT / "design-system/boundary-ledger/fonts/supreme-500.woff2"

ACCEPTED = {
    "s15p1": (REVIEWS / "r60-s15-p1/qa/r60-s15-p1.mp4", "bb4db674443198245947756b2137b10512c91e63339ba3dfd62e581d5e1339c5"),
    "s15p2": (REVIEWS / "r60-s15-p2/qa/r60-s15-p2.mp4", "e755a68ff5b2520d533b4d11c26ee02b547e68a2f61f13a9b0dc383c41cb961c"),
    "s16p1": (REVIEWS / "r61-s16-p1/qa/r61-s16-p1.mp4", "86eb1c1d80733e7cfb811e7ccef0b33656bac12241b9c5e78134600ad30d54d7"),
    "s16p2": (REVIEWS / "r61-s16-p2/qa/r61-s16-p2.mp4", "1b5cbeb3b630dbba13afeecf940e5639447136a59ded6f270477f5266d1b6827"),
}

SCENES = {
    "S15": {
        "master_start_frame": 15216,
        "frames": 1368,
        "insert": (608, 892),
        "keep": (("s15p1", 0, 0, 600), ("s15p2", 600, 0, 8), ("s15p2", 892, 292, 476)),
        "seam_hold": {"timeline_frame": 892, "source": "s15p2", "source_frame": 292, "frames": 1},
        "captures": (
            {
                "source": R77 / "projects/s15/public/media/capture-00.mp4",
                "source_sha256": "889f582c86042b12297b17f8867750cb82ca9553a5637bda6bdf96d1ee606bcd",
                "frames": 72,
                "crop": {"width": 2000, "height": 1036, "from": (200, 260), "to": (350, 340)},
                "focus": "Keeps the real pointer and the drafted owner-approval answer inside a tighter actual ChatGPT frame.",
            },
            {
                "source": R77 / "projects/s15/public/media/capture-01.mp4",
                "source_sha256": "c67e4b1abe03d43a8d4bbbdbc6c05926abc2e65d7df46c25df2c38d8d427aa7c",
                "frames": 212,
                "crop": {"width": 2000, "height": 1036, "from": (480, 140), "to": (600, 210)},
                "focus": "Tracks the genuine pointer as it moves toward the returned exception-pricing result.",
            },
        ),
    },
    "S16": {
        "master_start_frame": 16584,
        "frames": 1293,
        "insert": (213, 868),
        "keep": (("s16p1", 0, 0, 213), ("s16p1", 868, 868, 8), ("s16p2", 876, 0, 417)),
        # The accepted graphic is static across this brief boundary. Start its source-derived still
        # one frame before the capture ends because the renderer activates timed visual clips one frame late.
        "return_stills": ({"timeline_frame": 866, "source": "s16p1", "source_frame": 866, "frames": 10},),
        "captures": (
            {
                "source": R77 / "projects/s16/public/media/capture-00.mp4",
                "source_sha256": "33278a34476decc28be9226e08a8ef50c85b7bb9c6f6774e987998ccb76eefa0",
                "frames": 144,
                "crop": {"width": 1100, "height": 570, "from": (0, 100), "to": (0, 118)},
                "focus": "Moves with the current real cursor area while keeping the unresolved exception row readable.",
            },
            {
                "source": R77 / "projects/s16/public/media/capture-01.mp4",
                "source_sha256": "c23ed8c32a0a5c0824132ce797f2bd7ec59d65b2a27bca310abfefa69086cb34",
                "frames": 216,
                "crop": {"width": 1100, "height": 570, "from": (0, 100), "to": (0, 100)},
                "focus": "Holds the real package-index transition at a readable table scale; no synthetic tab action is added.",
            },
            {
                "source": R77 / "projects/s16/public/media/capture-02.mp4",
                "source_sha256": "c0b339e989643282a793a2fd3811915ffa6925d7099096a2f8323909ffc60d84",
                "frames": 198,
                "crop": {"width": 1100, "height": 570, "from": (0, 100), "to": (0, 100)},
                "focus": "Centers the actual Q3 source excerpt and unresolved implication at the scale needed for a phone.",
            },
            {
                "source": R77 / "projects/s16/public/media/capture-03.mp4",
                "source_sha256": "f36a7c8eb897b8db40d40de0ca1b488d23d2f0d6a092b8b6a499fa4e39209bf2",
                "frames": 97,
                "crop": {"width": 1100, "height": 570, "from": (0, 100), "to": (0, 118)},
                "focus": "Returns to the actual readiness row with a slow settle around the real cursor area.",
            },
        ),
    },
}

TARGETS = {"S15": "s15-mobile", "S16": "s16-mobile-r7"}


def sha(path: pathlib.Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def run(args, **kwargs):
    return subprocess.run([str(arg) for arg in args], check=True, **kwargs)


def probe(path: pathlib.Path) -> dict:
    raw = subprocess.check_output(
        [
            "ffprobe", "-v", "error", "-select_streams", "v:0",
            "-show_entries", "stream=width,height,nb_frames,r_frame_rate,duration",
            "-of", "json", str(path),
        ],
        text=True,
    )
    return json.loads(raw)["streams"][0]


def seconds(frames: int) -> str:
    return f"{frames / 24:.9f}"


def even_interpolation(start: int, end: int, frame_count: int) -> str:
    if frame_count == 1 or start == end:
        return str(start)
    # crop's x/y expressions are evaluated on each real source frame. The /2 floor keeps
    # yuv420 coordinates valid while retaining the actual cursor pixels unmodified.
    return f"trunc(({start}+({end}-{start})*n/{frame_count - 1})/2)*2"


def make_mobile_capture(spec: dict, destination: pathlib.Path) -> dict:
    source = spec["source"]
    assert source.is_file() and sha(source) == spec["source_sha256"], source
    source_info = probe(source)
    assert int(source_info["nb_frames"]) == spec["frames"], source_info
    crop = spec["crop"]
    x0, y0 = crop["from"]
    x1, y1 = crop["to"]
    assert 0 <= x0 <= int(source_info["width"]) - crop["width"]
    assert 0 <= x1 <= int(source_info["width"]) - crop["width"]
    assert 0 <= y0 <= int(source_info["height"]) - crop["height"]
    assert 0 <= y1 <= int(source_info["height"]) - crop["height"]
    filter_graph = (
        f"crop=w={crop['width']}:h={crop['height']}:"
        f"x='{even_interpolation(x0, x1, spec['frames'])}':"
        f"y='{even_interpolation(y0, y1, spec['frames'])}',"
        "scale=1216:630:flags=lanczos,setsar=1"
    )
    run([
        "ffmpeg", "-v", "error", "-nostdin", "-i", source,
        "-vf", filter_graph, "-an", "-frames:v", spec["frames"],
        "-c:v", "libx264", "-crf", "16", "-preset", "medium",
        "-pix_fmt", "yuv420p", "-movflags", "+faststart", destination,
    ])
    output_info = probe(destination)
    assert (int(output_info["width"]), int(output_info["height"]), int(output_info["nb_frames"]), output_info["r_frame_rate"]) == (1216, 630, spec["frames"], "24/1"), output_info
    return {
        "source": str(source),
        "source_sha256": spec["source_sha256"],
        "output": str(destination),
        "output_sha256": sha(destination),
        "frames": spec["frames"],
        "mobile_crop": crop,
        "filter_graph": filter_graph,
        "focus": spec["focus"],
        "real_cursor_preserved": True,
        "source_audio_included": False,
    }


def stage_master(scene: dict, destination: pathlib.Path) -> dict:
    assert sha(MASTER) == MASTER_HASH
    with wave.open(str(MASTER), "rb") as source:
        assert (source.getframerate(), source.getnchannels(), source.getsampwidth()) == (48000, 1, 2)
        source.setpos(scene["master_start_frame"] * 2000)
        pcm = source.readframes(scene["frames"] * 2000)
    assert len(pcm) == scene["frames"] * 4000
    with wave.open(str(destination), "wb") as output:
        output.setnchannels(1)
        output.setsampwidth(2)
        output.setframerate(48000)
        output.writeframes(pcm)
    return {
        "source": str(MASTER),
        "source_sha256": MASTER_HASH,
        "start_sample": scene["master_start_frame"] * 2000,
        "samples": scene["frames"] * 2000,
        "output_sha256": sha(destination),
    }


def build_scene(name: str, scene: dict) -> pathlib.Path:
    # Preserve the incomplete first attempt as an audit artifact; every runnable revision
    # uses its own directory and this builder never overwrites a candidate.
    target = HERE / "projects" / TARGETS[name]
    assert not target.exists(), f"Refuse to overwrite a candidate: {target}"
    for relative in ("public/media", "public/audio", "public/fonts", "qa"):
        (target / relative).mkdir(parents=True, exist_ok=True)

    accepted_pins = {}
    for key in {item[0] for item in scene["keep"]}:
        source, expected_hash = ACCEPTED[key]
        assert source.is_file() and sha(source) == expected_hash, source
        destination = target / f"public/media/{key}.mp4"
        shutil.copy2(source, destination)
        accepted_pins[key] = {"source": str(source), "sha256": expected_hash}

    seam_hold = None
    if "seam_hold" in scene:
        repair = scene["seam_hold"]
        hold = target / "public/media/seam-hold.png"
        run([
            "ffmpeg", "-v", "error", "-nostdin", "-i", target / f"public/media/{repair['source']}.mp4",
            "-vf", f"select=eq(n\\,{repair['source_frame']})", "-frames:v", "1", hold,
        ])
        seam_hold = {**repair, "asset": str(hold), "asset_sha256": sha(hold), "unchanged_from_r77": True}

    audio = stage_master(scene, target / "public/audio/narration.wav")
    shutil.copy2(FONT, target / "public/fonts/supreme-500.woff2")

    insert_start, insert_end = scene["insert"]
    clips = []
    for index, (key, timeline_start, media_start, frames) in enumerate(scene["keep"]):
        clips.append(
            f'<video id="{name}-keep-{index}" class="accepted" src="public/media/{key}.mp4" '
            f'data-start="{seconds(timeline_start)}" data-duration="{seconds(frames)}" '
            f'data-media-start="{seconds(media_start)}" data-track-index="1" muted playsinline></video>'
        )
    if seam_hold:
        clips.append(
            f'<img id="{name}-seam-hold" class="accepted clip" src="public/media/seam-hold.png" '
            f'data-start="{seconds(seam_hold["timeline_frame"])}" data-duration="{seconds(seam_hold["frames"])}" '
            'data-track-index="2" alt="">'
        )
    return_stills = []
    for repair in scene.get("return_stills", ()):
        asset = target / f"public/media/return-still-{repair['timeline_frame']}.png"
        run([
            "ffmpeg", "-v", "error", "-nostdin", "-i", target / f"public/media/{repair['source']}.mp4",
            "-vf", f"select=eq(n\\,{repair['source_frame']})", "-frames:v", "1", asset,
        ])
        return_stills.append({
            "timeline_frame": repair["timeline_frame"],
            "source": repair["source"],
            "source_frame": repair["source_frame"],
            "frames": repair["frames"],
            "asset": str(asset),
            "asset_sha256": sha(asset),
            "reason": "One static accepted graphic frame covers the browser video decoder's return seam; the surrounding accepted source is visually static over this interval.",
        })
        clips.append(
            f'<img id="{name}-return-still-{repair["timeline_frame"]}" class="accepted return-still clip" src="public/media/{asset.name}" '
            f'data-start="{seconds(repair["timeline_frame"])}" data-duration="{seconds(repair["frames"])}" '
            'data-track-index="2" alt="">'
        )
    clips.append(
        f'<div id="{name}-paper" class="paper clip" data-start="{seconds(insert_start)}" '
        f'data-duration="{seconds(insert_end - insert_start)}" data-track-index="0"></div>'
    )

    captures = []
    cursor = insert_start
    for index, spec in enumerate(scene["captures"]):
        destination = target / f"public/media/capture-mobile-{index:02d}.mp4"
        record = make_mobile_capture(spec, destination)
        record["timeline_start_frame"] = cursor
        record["timeline_end_frame_exclusive"] = cursor + spec["frames"]
        captures.append(record)
        clips.append(
            f'<video id="{name}-capture-{index}" class="capture" src="public/media/capture-mobile-{index:02d}.mp4" '
            f'data-start="{seconds(cursor)}" data-duration="{seconds(spec["frames"])}" '
            'data-media-start="0" data-track-index="1" muted playsinline></video>'
        )
        cursor += spec["frames"]
    assert cursor == insert_end, (name, cursor, insert_end)
    clips.append(
        f'<p id="{name}-disclosure" class="disclosure clip" data-start="{seconds(insert_start)}" '
        f'data-duration="{seconds(insert_end - insert_start)}" data-track-index="2">Illustrative example · fictional business</p>'
    )

    document = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>EP007 mobile tool insert</title>
<style>
@font-face{{font-family:Supreme;src:url('public/fonts/supreme-500.woff2');font-weight:500}}
*{{box-sizing:border-box}}html,body{{margin:0;width:1280px;height:720px;overflow:hidden}}
#root{{position:relative;width:1280px;height:720px;overflow:hidden}}
.accepted{{position:absolute;inset:0;width:1280px;height:720px;object-fit:contain}}
.paper{{position:absolute;inset:0;width:1280px;height:720px;background:#F5F0E6}}
.capture{{position:absolute;left:32px;top:60px;width:1216px;height:630px;object-fit:fill;background:#F5F0E6;border:1px solid #173530}}
.return-still{{z-index:1}}
.disclosure{{position:absolute;left:32px;top:19px;z-index:2;margin:0;color:#173530;font:500 20px/1.2 Supreme,sans-serif}}
</style></head><body>
<div id="root" data-composition-id="ep007-r78-{name.lower()}" data-no-timeline data-start="0" data-duration="{seconds(scene['frames'])}" data-width="1280" data-height="720" data-fps="24">
{chr(10).join(clips)}
<audio id="original-narration" src="public/audio/narration.wav" data-start="0" data-duration="{seconds(scene['frames'])}" data-media-start="0" data-track-index="100" data-volume="1"></audio>
</div></body></html>
'''
    (target / "index.html").write_text(document)
    (target / "hyperframes.json").write_text(json.dumps({
        "$schema": "https://hyperframes.heygen.com/schema/hyperframes.json",
        "authoringSkill": "general-video",
        "media": {"autoProxy": False},
    }, indent=2) + "\n")
    (target / "package.json").write_text(json.dumps({
        "name": f"ep007-r78-{name.lower()}", "private": True, "type": "module",
        "scripts": {"check": "npx --yes hyperframes@0.8.50 check", "render": "npx --yes hyperframes@0.8.50 render"},
    }, indent=2) + "\n")
    (target / "PROVENANCE.json").write_text(json.dumps({
        "scene": name,
        "version": "R78 mobile framing revision",
        "change_scope": "Only crop/scale/pan of verified actual recording picture; accepted source plates and locked narration are unchanged.",
        "scene_plan": scene,
        "accepted_sources": accepted_pins,
        "return_stills": return_stills,
        "captures": captures,
        "master_audio": audio,
        "font": {"path": str(FONT), "sha256": sha(FONT)},
        "status": "prepared_not_rendered_not_owner_accepted",
    }, indent=2, default=str) + "\n")
    return target


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--scene", choices=SCENES.keys())
    args = parser.parse_args()
    targets = (args.scene,) if args.scene else SCENES.keys()
    for label in targets:
        print(build_scene(label, SCENES[label]))
