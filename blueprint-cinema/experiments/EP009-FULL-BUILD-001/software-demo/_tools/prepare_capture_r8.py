#!/usr/bin/env python3
"""Prepare the isolated r8 tool-clarity source plate for S13.

R8 keeps the r7 plate pixel-identical outside local frames [42,102). It
replaces that 60-frame native request beat with a tighter 16:9 crop from the
already-bound clean Node-RED capture. This is a documentary conform only: no
provider call, UI action, runtime mutation, send action, or narration change.
"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True

S = Path(__file__).resolve().parents[1]
B = S.parent
R7 = S / "capture" / "node-red-editor-r7"
LANE = S / "capture" / "node-red-editor-r8"
R7_PLATE = R7 / "screen-r7-tool-focus-706.mp4"
R7_CONFORM = R7 / "SCREEN-R7-CONFORM.json"
R7_REVIEW = R7 / "SCREEN-REVIEW.json"
NATIVE = R7 / "raw" / "native-node-red-editor-2560x1440.png"
NATIVE_PROVENANCE = R7 / "NATIVE-CAPTURE-PROVENANCE.json"
OUTPUT = LANE / "screen-r8-tool-clarity-706.mp4"
EDIT = LANE / "GUIDED-SCREEN-EDIT-MANIFEST-r8.json"
CONFORM = LANE / "SCREEN-R8-CONFORM.json"
TOTAL = 706
TIGHT = [42, 102]
CROP = {"width": 640, "height": 360, "x": 480, "y": 240}

sys.path[:0] = [str(B / "presenter-look-transfer" / "_tools")]
from build_review import video_hashes  # noqa: E402


def sha(path: Path) -> str:
    with path.open("rb") as handle:
        return hashlib.file_digest(handle, "sha256").hexdigest()


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(B))


def bound(path: Path) -> dict:
    return {"path": rel(path), "sha256": sha(path)}


def run(*args: str) -> None:
    subprocess.run(list(args), check=True)


def probe(path: Path) -> dict:
    return json.loads(subprocess.check_output([
        "ffprobe", "-v", "error", "-count_frames", "-show_entries",
        "stream=codec_type,width,height,pix_fmt,r_frame_rate,nb_read_frames",
        "-of", "json", str(path),
    ]))


def exact_video(path: Path, expected_frames: int) -> dict:
    stream = next(item for item in probe(path)["streams"] if item["codec_type"] == "video")
    got = (stream["width"], stream["height"], stream["pix_fmt"], stream["r_frame_rate"], int(stream["nb_read_frames"]))
    want = (1280, 720, "yuv420p", "24/1", expected_frames)
    if got != want:
        raise ValueError(f"Wrong video shape for {path}: {got}; expected {want}")
    return stream


def check_crop_geometry() -> None:
    stream = next(item for item in probe(NATIVE)["streams"] if item["codec_type"] == "video")
    if (stream["width"], stream["height"]) != (2560, 1440):
        raise ValueError("Clean native capture raster changed")
    if CROP["x"] < 0 or CROP["y"] < 0 or CROP["x"] + CROP["width"] > stream["width"] or CROP["y"] + CROP["height"] > stream["height"]:
        raise ValueError("Tight r8 crop exceeds clean native capture")
    if CROP["width"] * 9 != CROP["height"] * 16:
        raise ValueError("Tight r8 crop must remain exactly 16:9")


def main() -> None:
    for path in (R7_PLATE, R7_CONFORM, R7_REVIEW, NATIVE, NATIVE_PROVENANCE):
        if not path.is_file():
            raise FileNotFoundError(path)
    if any(path.exists() for path in (OUTPUT, EDIT, CONFORM)):
        raise FileExistsError("Preserve immutable r8 output or record")
    check_crop_geometry()
    exact_video(R7_PLATE, TOTAL)
    r7_hashes = video_hashes(R7_PLATE, TOTAL)["hashes"]

    # The r7 portions are decoded and losslessly re-encoded so their source pixels
    # remain identical. Only [42,102) is newly rasterized from the clean native view.
    graph = (
        "[0:v]trim=start_frame=0:end_frame=42,setpts=PTS-STARTPTS[prefix];"
        "[1:v]crop=640:360:480:240,scale=1280:720:flags=lanczos,setsar=1,"
        "trim=start_frame=0:end_frame=60,setpts=PTS-STARTPTS[tight];"
        "[0:v]trim=start_frame=102:end_frame=706,setpts=PTS-STARTPTS[suffix];"
        "[prefix][tight][suffix]concat=n=3:v=1:a=0,format=yuv420p[out]"
    )
    command = [
        "ffmpeg", "-nostdin", "-n", "-v", "error", "-i", str(R7_PLATE),
        "-loop", "1", "-framerate", "24", "-i", str(NATIVE),
        "-filter_complex", graph, "-map", "[out]", "-frames:v", str(TOTAL), "-an",
        "-c:v", "libx264", "-preset", "medium", "-crf", "0", "-pix_fmt", "yuv420p",
        "-r", "24", "-video_track_timescale", "24", "-movflags", "+faststart", str(OUTPUT),
    ]
    run(*command)
    output_probe = exact_video(OUTPUT, TOTAL)
    r8 = video_hashes(OUTPUT, TOTAL)
    r8_hashes = r8["hashes"]
    unchanged = [[0, 42], [102, TOTAL]]
    for lo, hi in unchanged:
        if r8_hashes[lo:hi] != r7_hashes[lo:hi]:
            raise ValueError(f"R8 altered retained r7 decoded frames [{lo},{hi})")
    if r8_hashes[TIGHT[0]:TIGHT[1]] == r7_hashes[TIGHT[0]:TIGHT[1]]:
        raise ValueError("R8 tight request beat did not differ from r7")
    if len(set(r8_hashes[TIGHT[0]:TIGHT[1]])) != 1:
        raise ValueError("R8 native static focus beat must use one stable cropped source frame")

    source_ranges = [
        {
            "id": "retained-r7-native-overview",
            "kind": "retained_r7_focus_plate",
            "output_frames": [0, 42],
            "source": bound(R7_PLATE),
            "source_frames": [0, 42],
            "transform": "decoded r7 frames retained losslessly",
            "limit": "r8 does not reopen the r7 overview beat",
        },
        {
            "id": "native-openai-request-tight-r8",
            "kind": "native_node_red_current_configuration",
            "output_frames": TIGHT,
            "source": bound(NATIVE),
            "source_frames": [0, 1],
            "transform": "crop=640:360:480:240, scale=1280:720; focus the actual Fictional fixture to capped real request and OpenAI genuine thank-you draft labels",
            "crop_xywh": [CROP["x"], CROP["y"], CROP["width"], CROP["height"]],
            "limit": "later local configuration view, not a live provider call",
        },
        {
            "id": "retained-r7-after-request",
            "kind": "retained_r7_focus_plate",
            "output_frames": [102, TOTAL],
            "source": bound(R7_PLATE),
            "source_frames": [102, TOTAL],
            "transform": "decoded r7 frames retained losslessly",
            "limit": "r8 does not reopen the r7 returned-draft, queue, human-edit, approval, exclusion, or boundary beats",
        },
    ]
    if source_ranges[0]["output_frames"][1] != source_ranges[1]["output_frames"][0] or source_ranges[1]["output_frames"][1] != source_ranges[2]["output_frames"][0] or source_ranges[2]["output_frames"][1] != TOTAL:
        raise ValueError("R8 source range coverage is not contiguous")
    edit = {
        "record_type": "ep009_r8_tool_clarity_guided_screen_edit_manifest",
        "status": "prepared_for_private_review",
        "source_timebase": "24fps",
        "output_frames": [0, TOTAL],
        "base_r7_focus_plate": bound(R7_PLATE),
        "segments": source_ranges,
        "guidance": {
            "method": "retain r7 except for one readable native request beat",
            "annotations": "none; the tighter native crop directs attention without fabricated UI or editorial labels",
            "no_generated_ui": True,
            "no_optical_flow": True,
            "no_speed_ramp": True,
            "provider_call_in_this_conform": False,
            "retained_r7_decoded_frame_ranges": unchanged,
            "changed_decoded_frame_range": TIGHT,
        },
    }
    EDIT.write_text(json.dumps(edit, indent=2) + "\n")
    conform = {
        "record_type": "ep009_r8_tool_clarity_screen_conform",
        "status": "prepared_for_private_review",
        "output": bound(OUTPUT),
        "output_probe": output_probe,
        "decoded_frame_sequence_sha256": r8["sequence_sha256"],
        "source_edit_manifest": bound(EDIT),
        "source_r7_focus_plate": bound(R7_PLATE),
        "source_r7_screen_conform": bound(R7_CONFORM),
        "source_r7_screen_review": bound(R7_REVIEW),
        "source_native_capture": bound(NATIVE),
        "source_native_capture_provenance": bound(NATIVE_PROVENANCE),
        "r7_pixel_preservation": {
            "method": "sha256 decoded yuv420p frames in order",
            "retained_output_frames": unchanged,
            "changed_output_frames": TIGHT,
            "all_retained_ranges_identical": True,
        },
        "encode_command": command,
        "limits": [
            "Fictional Maya Chen and Alder House Inn test only.",
            "The Node-RED editor is the actual local tool surface. The workflow used the OpenAI Responses API, not an OpenAI graphical dashboard.",
            "The r8 plate changes only the 60-frame request beat. It does not show a new execution, send, customer result, consent, capacity, or release claim.",
        ],
    }
    CONFORM.write_text(json.dumps(conform, indent=2) + "\n")
    print(json.dumps({"output": bound(OUTPUT), "frames": TOTAL, "conform": bound(CONFORM), "changed_output_frames": TIGHT}))


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(2)
