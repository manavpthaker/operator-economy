#!/usr/bin/env python3
"""Build the isolated r7 S13 native-tool focus plate.

This is a documentary conform, not a new execution. It uses a clean, later
local capture of the native Node-RED editor plus retained frames from the
already-bound r2 fictional test. It does not call a provider, drive the UI,
or alter runtime state.
"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True

S = Path(__file__).resolve().parents[1]
B = S.parent
LANE = S / "capture" / "node-red-editor-r7"
RAW = LANE / "raw"
DERIVED = LANE / "derived"
NATIVE = RAW / "native-node-red-editor-2560x1440.png"
R2 = S / "capture" / "node-red-openai-real-run-r2" / "screen-706.mp4"
R2_SHA = "b958b406f7d6d29304de5746ef843762cc6b0be848c69bcb23dca597474fa011"
OUTPUT = LANE / "screen-r7-tool-focus-706.mp4"
CONFORM = LANE / "SCREEN-R7-CONFORM.json"
EDIT = LANE / "GUIDED-SCREEN-EDIT-MANIFEST.json"
TOTAL = 706

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
        "stream=codec_type,width,height,r_frame_rate,nb_read_frames:format=duration",
        "-of", "json", str(path),
    ]))


def static_image(source: Path, filters: str, frames: int, out: Path) -> None:
    run(
        "ffmpeg", "-nostdin", "-n", "-v", "error", "-loop", "1", "-framerate", "24",
        "-i", str(source), "-vf", filters, "-frames:v", str(frames), "-an",
        "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-pix_fmt", "yuv420p",
        "-r", "24", "-video_track_timescale", "24", str(out),
    )


def still_from_r2(frame: int, crop: str, out: Path) -> None:
    # Frame-select happens before crop so the selected frame is auditable against r2.
    run(
        "ffmpeg", "-nostdin", "-n", "-v", "error", "-i", str(R2), "-vf",
        f"select='eq(n\\,{frame})',{crop},scale=1280:720:flags=lanczos,setsar=1",
        "-frames:v", "1", str(out),
    )


def edit_clip(out: Path) -> None:
    # r2 [314,414) is the recorded human text edit. The final 39 frames are an
    # explicit editorial reading hold of that same final source frame.
    run(
        "ffmpeg", "-nostdin", "-n", "-v", "error", "-i", str(R2), "-vf",
        "trim=start_frame=314:end_frame=414,setpts=PTS-STARTPTS,"
        "crop=640:360:300:330,scale=1280:720:flags=lanczos,setsar=1,"
        "tpad=stop_mode=clone:stop_duration=1.625",
        "-frames:v", "139", "-an", "-c:v", "libx264", "-preset", "medium", "-crf", "16",
        "-pix_fmt", "yuv420p", "-r", "24", "-video_track_timescale", "24", str(out),
    )


def exact_video(path: Path, frames: int) -> dict:
    stream = next(item for item in probe(path)["streams"] if item["codec_type"] == "video")
    got = (stream["width"], stream["height"], stream["r_frame_rate"], int(stream["nb_read_frames"]))
    if got != (1280, 720, "24/1", frames):
        raise ValueError(f"Wrong video shape for {path}: {got}")
    return stream


def main() -> None:
    for path in (NATIVE, R2):
        if not path.is_file():
            raise FileNotFoundError(path)
    if sha(R2) != R2_SHA:
        raise ValueError("r2 retained screen source hash changed")
    for path in (OUTPUT, CONFORM, EDIT):
        if path.exists():
            raise FileExistsError(f"Preserve immutable r7 output: {path}")
    DERIVED.mkdir(parents=True, exist_ok=False)

    chunks = [
        ("00-native-overview", 42),
        ("01-native-openai-request", 60),
        ("02-retained-returned-draft", 60),
        ("03-native-checkout-rule", 48),
        ("04-retained-queued-draft", 51),
        ("05-retained-human-edit", 139),
        ("06-retained-one-draft-approval", 152),
        ("07-retained-seasonal-exclusion", 70),
        ("08-native-human-boundary", 84),
    ]
    if sum(frames for _, frames in chunks) != TOTAL:
        raise ValueError("r7 frame plan is not 706 frames")

    static_image(NATIVE, "scale=1280:720:flags=lanczos,setsar=1", 42, DERIVED / "00-native-overview.mp4")
    static_image(NATIVE, "crop=1200:675:240:40,scale=1280:720:flags=lanczos,setsar=1", 60,
                 DERIVED / "01-native-openai-request.mp4")
    still_from_r2(194, "crop=640:360:300:330", DERIVED / "02-returned-draft-f194.png")
    static_image(DERIVED / "02-returned-draft-f194.png", "setsar=1", 60,
                 DERIVED / "02-retained-returned-draft.mp4")
    static_image(NATIVE, "crop=720:405:180:320,scale=1280:720:flags=lanczos,setsar=1", 48,
                 DERIVED / "03-native-checkout-rule.mp4")
    still_from_r2(240, "crop=640:360:300:330", DERIVED / "04-queued-draft-f240.png")
    static_image(DERIVED / "04-queued-draft-f240.png", "setsar=1", 51,
                 DERIVED / "04-retained-queued-draft.mp4")
    edit_clip(DERIVED / "05-retained-human-edit.mp4")
    still_from_r2(514, "crop=640:360:620:180", DERIVED / "06-one-draft-approval-f514.png")
    static_image(DERIVED / "06-one-draft-approval-f514.png", "setsar=1", 152,
                 DERIVED / "06-retained-one-draft-approval.mp4")
    still_from_r2(622, "crop=640:360:620:180", DERIVED / "07-seasonal-exclusion-f622.png")
    static_image(DERIVED / "07-seasonal-exclusion-f622.png", "setsar=1", 70,
                 DERIVED / "07-retained-seasonal-exclusion.mp4")
    static_image(NATIVE, "crop=900:506:180:390,scale=1280:720:flags=lanczos,setsar=1", 84,
                 DERIVED / "08-native-human-boundary.mp4")

    chunk_paths = [DERIVED / f"{slug}.mp4" for slug, _ in chunks]
    for path, (_, frames) in zip(chunk_paths, chunks):
        exact_video(path, frames)
    concat = DERIVED / "concat.txt"
    concat.write_text("".join(f"file '{path}'\n" for path in chunk_paths))
    run(
        "ffmpeg", "-nostdin", "-n", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(concat),
        "-an", "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-pix_fmt", "yuv420p",
        "-r", "24", "-video_track_timescale", "24", "-movflags", "+faststart", str(OUTPUT),
    )
    exact_video(OUTPUT, TOTAL)
    hashes = video_hashes(OUTPUT, TOTAL)

    local = 0
    segments = []
    source_details = [
        ("native-overview", "native_node_red_current_configuration", [0, 42], [0, 1], NATIVE,
         "full native Node-RED editor", "later local view of the persisted fictional run"),
        ("native-openai-request", "native_node_red_current_configuration", [42, 102], [0, 1], NATIVE,
         "crop [240,40,1200,675] shows the native comment and OpenAI HTTP-request branch",
         "later local view; native UI is not represented as a live provider call"),
        ("retained-returned-draft", "retained_r2_test_recording", [102, 162], [194, 195], R2,
         "crop [300,330,640,360] of actual returned draft and prepared date rule", "editorial still hold"),
        ("native-checkout-rule", "native_node_red_current_configuration", [162, 210], [0, 1], NATIVE,
         "crop [180,320,720,405] shows POST /api/queue to Checkout + one day", "later local view"),
        ("retained-queued-draft", "retained_r2_test_recording", [210, 261], [240, 241], R2,
         "crop [300,330,640,360] shows queued draft, time, human review, and no sending", "editorial still hold"),
        ("retained-human-edit", "retained_r2_test_recording", [261, 400], [314, 414], R2,
         "crop [300,330,640,360] of recorded text edit, followed by 39-frame reading hold", "no speed change"),
        ("retained-one-draft-approval", "retained_r2_test_recording", [400, 552], [514, 515], R2,
         "crop [620,180,640,360] shows specific one-draft approval", "editorial still hold"),
        ("retained-seasonal-exclusion", "retained_r2_test_recording", [552, 622], [622, 623], R2,
         "crop [620,180,640,360] shows Excluded by human and Seasonal follow-up excluded", "editorial still hold"),
        ("native-human-boundary", "native_node_red_current_configuration", [622, 706], [0, 1], NATIVE,
         "crop [180,390,900,506] shows save, one-draft approval, and no-future-promotion nodes", "later local view"),
    ]
    for name, kind, out_range, source_range, source, transform, limit in source_details:
        if out_range[0] != local:
            raise ValueError("segment continuity failure")
        local = out_range[1]
        segments.append({
            "id": name,
            "kind": kind,
            "output_frames": out_range,
            "source": bound(source),
            "source_frames": source_range,
            "transform": transform,
            "limit": limit,
        })
    if local != TOTAL:
        raise ValueError("segment coverage failure")
    edit = {
        "record_type": "ep009_r7_guided_screen_edit_manifest",
        "status": "prepared_for_review",
        "source_timebase": "24fps",
        "output_frames": [0, TOTAL],
        "segments": segments,
        "guidance": {
            "method": "native tool identification then one readable state at a time",
            "annotations": "none; crops themselves direct attention",
            "no_generated_ui": True,
            "no_optical_flow": True,
            "no_speed_ramp": True,
            "provider_call_in_this_conform": False,
            "editorial_ellipses": [
                "Native Node-RED views are later local configuration views of the already-persisted fictional test, not a continuous replay of the provider request.",
                "Static holds preserve a true source frame for reading. The human edit is the retained r2 source [314,414) followed by a declared 39-frame hold.",
            ],
        },
    }
    EDIT.write_text(json.dumps(edit, indent=2) + "\n")
    conform = {
        "record_type": "ep009_r7_screen_conform",
        "status": "prepared_for_review",
        "output": bound(OUTPUT),
        "output_probe": exact_video(OUTPUT, TOTAL),
        "decoded_frame_sequence_sha256": hashes["sequence_sha256"],
        "source_edit_manifest": bound(EDIT),
        "source_native_capture": bound(NATIVE),
        "source_retained_r2_screen": bound(R2),
        "chunks": [bound(path) for path in chunk_paths],
        "limits": [
            "Fictional Maya Chen and Alder House Inn test only.",
            "The Node-RED editor is the actual local tool surface. The workflow used the OpenAI Responses API, not an OpenAI graphical dashboard.",
            "The plate shows one real bounded draft and a queued human-review state. It never represents a sent email, a customer result, or a capacity claim.",
        ],
    }
    CONFORM.write_text(json.dumps(conform, indent=2) + "\n")
    print(json.dumps({"output": bound(OUTPUT), "frames": TOTAL, "conform": bound(CONFORM)}))


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(2)
