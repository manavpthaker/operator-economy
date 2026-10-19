#!/usr/bin/env python3
"""Prepare or render the isolated EP009 r8 tool-clarity private candidate.

R8 uses the verified r7 candidate as a frozen assembly base. It may replace
only S13's existing 706-frame software interval [16752,17458), and its source
plate may change picture only at local frames [42,102). All narration, the r6
F03 establish, and every other r7 assignment remain bound and unchanged.
"""
import argparse
import copy
import datetime
import json
import re
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True

S = Path(__file__).resolve().parents[1]
B = S.parent
A = B / "assembly"
sys.path[:0] = [str(B / "presenter-look-transfer" / "_tools"), str(A / "_tools")]
from build_r3 import R, bound, read, rel, sha, verify_bound, write, probe  # noqa: E402
from build_r4 import frame_map, graph_for, nested_bindings  # noqa: E402
from build_review import video_hashes  # noqa: E402

R7_ROOT = S / "r7-tool-focus"
R8_ROOT = S / "r8-tool-clarity"
R7_LANE = S / "capture" / "node-red-editor-r7"
R8_LANE = S / "capture" / "node-red-editor-r8"
R7_PLATE = R7_LANE / "screen-r7-tool-focus-706.mp4"
R8_PLATE = R8_LANE / "screen-r8-tool-clarity-706.mp4"
R7_CONFORM = R7_LANE / "SCREEN-R7-CONFORM.json"
R7_REVIEW = R7_LANE / "SCREEN-REVIEW.json"
R8_EDIT = R8_LANE / "GUIDED-SCREEN-EDIT-MANIFEST-r8.json"
R8_CONFORM = R8_LANE / "SCREEN-R8-CONFORM.json"
NATIVE = R7_LANE / "raw" / "native-node-red-editor-2560x1440.png"
BASE = A / "r7-tool-focus" / "ep009-r7-tool-focus-review-r1-BUILD.json"
BASE_SHA = "82f184b4be87496c289899ccc1b0067759d60b0c4ea66a71f8e6f113ec3b1f09"
BASE_VERIFY = BASE.with_name(BASE.name.replace("-BUILD.json", "-VERIFICATION.json"))
BASE_VERIFY_SHA = "7e2ec95e24dec9deec29b162c255ca7270f3226af87441428aa68a3f197a21e0"
F03_SCOPE = [16704, 16752]
SCOPE = [16752, 17458]
LOCAL_CHANGE = [42, 102]
TOTAL = 29323
PLATE_TOTAL = 706
PROTECTED = ("master", "timemap", "transcript", "revision", "owner_scoped_lock", "film_selections")


def conform_bound(path: Path) -> dict:
    return {"path": str(path.resolve().relative_to(B)), "sha256": sha(path)}


def verify_conform_bound(binding: dict) -> Path:
    path = (B / binding["path"]).resolve()
    path.relative_to(B)
    if sha(path) != binding["sha256"]:
        raise ValueError("Changed conform-bound input: " + str(path))
    return path


def entry(base: dict, entry_id: str) -> dict:
    matches = [item for item in base["inserts"] if item.get("id") == entry_id]
    if len(matches) != 1:
        raise ValueError("Required r7 insert missing or duplicated: " + entry_id)
    return matches[0]


def raster(path: Path) -> tuple[int, int]:
    info = probe(path)
    stream = next(item for item in info["streams"] if item["codec_type"] == "video")
    return int(stream["width"]), int(stream["height"])


def exact_plate(path: Path, frames: int) -> dict:
    stream = next(item for item in probe(path)["streams"] if item["codec_type"] == "video")
    got = (stream["width"], stream["height"], stream["r_frame_rate"], int(stream["nb_read_frames"]))
    if got != (1280, 720, "24/1", frames):
        raise ValueError("Expected exact 1280x720 24fps plate: " + str(got))
    return stream


def retained_f03(base: dict) -> dict:
    # R7 carries the r6 establish as a separately pinned retained binding, not
    # as an r7 insert. Preserve that exact historical shape.
    item = base.get("retained_f03")
    if not isinstance(item, dict):
        raise ValueError("R7 retained F03 binding missing")
    keys = ("id", "kind", "output_frames", "source", "source_start_frame", "source_total_frames", "decoded_frame_sequence_sha256", "review")
    value = {key: copy.deepcopy(item[key]) for key in keys}
    if value["kind"] != "existing_film" or value["output_frames"] != F03_SCOPE:
        raise ValueError("Wrong r7 F03 establish binding")
    return value


def r7_real_capture(base: dict) -> dict:
    item = entry(base, "native-node-red-tool-focus-r7")
    if item.get("kind") != "real_software_capture" or item.get("output_frames") != SCOPE:
        raise ValueError("Wrong r7 S13 real-software interval")
    return item


def checked_base() -> dict:
    base = read(verify_bound({"path": rel(BASE), "sha256": BASE_SHA}))
    verification = read(verify_bound({"path": rel(BASE_VERIFY), "sha256": BASE_VERIFY_SHA}))
    if base.get("record_type") != "ep009_r7_tool_focus_review_build" or base.get("status") != "encoded_unverified_review_only":
        raise ValueError("Wrong r7 baseline record")
    if verification.get("build") != bound(BASE) or verification.get("status") != "technical_checks_passed_private_review_candidate" or verification.get("errors"):
        raise ValueError("Wrong r7 verified base")
    if verification.get("output") != {"path": base.get("output"), "sha256": base.get("output_sha256")}:
        raise ValueError("R7 output binding mismatch")
    verify_bound(verification["output"])
    for key in PROTECTED:
        verify_bound(base[key])
    verify_bound(base["selections"])
    verify_bound(base["direction"])
    nested_bindings(read(verify_bound(base["owner_scoped_lock"])))
    nested_bindings(base["retained_P00"])
    nested_bindings(base["retained_r5_presenters"])
    if len(base["all_75_rows"]) != 75 or len(frame_map(base["all_75_rows"])) != TOTAL:
        raise ValueError("Wrong r7 baseline clock")
    if [(row["id"], row["output_frames"]) for row in base["all_75_rows"] if row["scene"] == "S13"] != [("seg046", [16609, 16987]), ("seg047", [16987, 17523])]:
        raise ValueError("S13 bounds changed")
    for source in {span["source"]["path"]: span["source"] for row in base["all_75_rows"] for span in row["spans"]}.values():
        verify_bound(source)
    retained_f03(base)
    r7_real_capture(base)
    return base


def checked_source_basis(basis: dict, old: dict) -> dict:
    if not isinstance(basis, dict):
        raise ValueError("R8 source basis missing")
    expected = {
        "r7_focus_plate": R7_PLATE,
        "r7_screen_conform": R7_CONFORM,
        "r7_screen_review": R7_REVIEW,
        "native_current_configuration_capture": NATIVE,
        "r8_guided_edit_manifest": R8_EDIT,
        "r8_screen_conform": R8_CONFORM,
    }
    for key, path in expected.items():
        if verify_bound(basis.get(key, {})) != path:
            raise ValueError("R8 source basis binding mismatch: " + key)
    if basis.get("no_causal_state_reordered") is not True:
        raise ValueError("R8 causal sequence declaration missing")
    if basis["r7_focus_plate"] != old["source"]:
        raise ValueError("R8 must bind r7's selected source plate")
    r7_conform = read(R7_CONFORM)
    if r7_conform.get("output") != conform_bound(R7_PLATE):
        raise ValueError("R7 source conform no longer binds r7 plate")
    r7_review = read(R7_REVIEW)
    if r7_review.get("source") != old["source"] or r7_review.get("no_send") is not True or r7_review.get("email_sending_available") is not False:
        raise ValueError("R7 source review no longer establishes native/no-send scope")
    edit = read(R8_EDIT)
    conform = read(R8_CONFORM)
    if edit.get("record_type") != "ep009_r8_tool_clarity_guided_screen_edit_manifest" or edit.get("output_frames") != [0, PLATE_TOTAL]:
        raise ValueError("Wrong r8 guided edit manifest")
    if conform.get("record_type") != "ep009_r8_tool_clarity_screen_conform" or conform.get("output") != conform_bound(R8_PLATE):
        raise ValueError("Wrong r8 screen conform output")
    if conform.get("source_edit_manifest") != conform_bound(R8_EDIT):
        raise ValueError("R8 conform/edit binding mismatch")
    if conform.get("source_r7_focus_plate") != conform_bound(R7_PLATE) or conform.get("source_r7_screen_conform") != conform_bound(R7_CONFORM) or conform.get("source_r7_screen_review") != conform_bound(R7_REVIEW):
        raise ValueError("R8 conform loses r7 source lineage")
    if conform.get("source_native_capture") != conform_bound(NATIVE):
        raise ValueError("R8 conform loses clean native capture")
    preservation = conform.get("r7_pixel_preservation", {})
    if preservation.get("retained_output_frames") != [[0, 42], [102, PLATE_TOTAL]] or preservation.get("changed_output_frames") != LOCAL_CHANGE or preservation.get("all_retained_ranges_identical") is not True:
        raise ValueError("R8 conform does not make the local-change boundary explicit")
    segments = edit.get("segments", [])
    expected_ranges = [[0, 42], LOCAL_CHANGE, [102, PLATE_TOTAL]]
    if [segment.get("output_frames") for segment in segments] != expected_ranges:
        raise ValueError("R8 guided edit ranges changed")
    if segments[0].get("source") != conform_bound(R7_PLATE) or segments[2].get("source") != conform_bound(R7_PLATE):
        raise ValueError("R8 must retain r7 on both sides of the focus beat")
    tight = segments[1]
    if tight.get("kind") != "native_node_red_current_configuration" or verify_conform_bound(tight.get("source", {})) != NATIVE:
        raise ValueError("R8 focus beat must use the clean native Node-RED capture")
    if tight.get("source_frames") != [0, 1] or tight.get("crop_xywh") != [480, 240, 640, 360] or "crop=640:360:480:240" not in str(tight.get("transform", "")):
        raise ValueError("R8 must use the requested 16:9 native request crop")
    width, height = raster(NATIVE)
    x, y, w, h = tight["crop_xywh"]
    if (w, h) != (640, 360) or x < 0 or y < 0 or x + w > width or y + h > height:
        raise ValueError("R8 crop is outside clean native capture")
    return basis


def checked_selection(path: Path, base: dict) -> tuple[dict, list[dict]]:
    path = path.resolve()
    path.relative_to(R8_ROOT)
    manifest = read(path)
    if manifest.get("record_type") != "ep009_r8_tool_clarity_selections" or manifest.get("status") != "selected_for_private_review":
        raise ValueError("Explicit r8 selected-for-private-review manifest required")
    for key, value in (
        ("base_r7_build", bound(BASE)),
        ("base_r7_verification", bound(BASE_VERIFY)),
        ("timing_contract", base["timing_contract"]),
        ("master", base["master"]),
        ("r6_selections", base["r6_selections"]),
        ("r7_selections", base["selections"]),
        ("owner_tool_focus_scope", base["owner_tool_focus_scope"]),
    ):
        if manifest.get(key) != value:
            raise ValueError("R8 selection binding mismatch: " + key)
    if manifest.get("r8_scope") != SCOPE or manifest.get("retained_f03") != retained_f03(base):
        raise ValueError("R8 scope or F03 preservation binding mismatch")
    direction = read(verify_bound(manifest["direction"]))
    if direction.get("record_type") != "ep009_r8_tool_clarity_direction" or direction.get("status") != "selected_for_private_review":
        raise ValueError("Wrong r8 direction record")
    if direction.get("base_r7_build") != bound(BASE) or direction.get("base_r7_verification") != bound(BASE_VERIFY) or direction.get("r8_scope") != SCOPE or direction.get("retained_f03_output_frames") != F03_SCOPE:
        raise ValueError("R8 direction does not bind exact preserved scope")
    basis = checked_source_basis(manifest.get("source_basis"), r7_real_capture(base))
    if direction.get("source_basis") != basis:
        raise ValueError("R8 direction must bind the exact source basis")
    entries = manifest.get("inserts", [])
    if len(entries) != 1:
        raise ValueError("R8 requires one precomposed clarity plate")
    item = entries[0]
    expected_direction = [{key: item[key] for key in ("id", "output_frames", "source", "source_start_frame")}]
    if direction.get("selected_inserts") != expected_direction:
        raise ValueError("R8 direction insert binding mismatch")
    if item.get("id") != "native-node-red-tool-clarity-r8" or item.get("kind") != "real_software_capture" or item.get("output_frames") != SCOPE:
        raise ValueError("R8 insert has wrong identity or scope")
    source = verify_bound(item["source"])
    if source != R8_PLATE or item.get("source_start_frame") != 0 or item.get("source_total_frames") != PLATE_TOTAL:
        raise ValueError("R8 must use its exact 706-frame clarity plate")
    exact_plate(source, PLATE_TOTAL)
    hashes = video_hashes(source, PLATE_TOTAL)
    if hashes["sequence_sha256"] != item.get("decoded_frame_sequence_sha256"):
        raise ValueError("Decoded r8 source frame sequence changed")
    if item.get("source_conform") != bound(R8_CONFORM) or item.get("local_clarity_change_frames") != LOCAL_CHANGE or item.get("global_clarity_change_frames") != [SCOPE[0] + LOCAL_CHANGE[0], SCOPE[0] + LOCAL_CHANGE[1]]:
        raise ValueError("R8 insert must bind its source conform and exact 60-frame change")
    old = video_hashes(R7_PLATE, PLATE_TOTAL)["hashes"]
    if hashes["hashes"][:42] != old[:42] or hashes["hashes"][102:] != old[102:]:
        raise ValueError("R8 altered a retained r7 decoded frame")
    if hashes["hashes"][42:102] == old[42:102]:
        raise ValueError("R8 did not replace its requested native request beat")
    return manifest, [{**copy.deepcopy(item), "frames": PLATE_TOTAL, "source_probe": exact_plate(source, PLATE_TOTAL), "provider_audio_discarded": True}]


def portion(span: dict, lo: int, hi: int) -> dict:
    start, end = span["output_frames"]
    copied = copy.deepcopy(span)
    copied.update(output_frames=[lo, hi], frames=hi - lo, source_start_frame=span["source_start_frame"] + lo - start)
    if "original_frames" in copied:
        if copied["original_frames"][1] - copied["original_frames"][0] != end - start:
            raise ValueError("Nonlinear retained original span unsupported")
        origin = copied["original_frames"][0]
        copied["original_frames"] = [origin + lo - start, origin + hi - start]
    return copied


def patch(rows: list[dict], entries: list[dict]) -> list[dict]:
    changed = copy.deepcopy(rows)
    for item in entries:
        lo, hi = item["output_frames"]
        for row in changed:
            spans = []
            for span in row["spans"]:
                start, end = span["output_frames"]
                left, right = max(start, lo), min(end, hi)
                if left >= right:
                    spans.append(span)
                    continue
                if start < left:
                    spans.append(portion(span, start, left))
                replacement = portion(span, left, right)
                replacement.update(
                    kind="video",
                    source=item["source"],
                    source_start_frame=item["source_start_frame"] + left - lo,
                    software_demo_insert=item["id"],
                    software_demo_source_conform=item["source_conform"],
                )
                spans.append(replacement)
                if right < end:
                    spans.append(portion(span, right, end))
            row["spans"] = spans
    return changed


def mapping_check(base: dict, rows: list[dict], entries: list[dict]) -> dict:
    before, after = frame_map(base["all_75_rows"]), frame_map(rows)
    allowed = set(range(*SCOPE))
    changed = {frame for frame, (old, new) in enumerate(zip(before, after)) if old != new}
    if len(after) != TOTAL or changed != allowed:
        raise ValueError("Unexpected r8 assignment outside real-software interval")
    if before[F03_SCOPE[0]:F03_SCOPE[1]] != after[F03_SCOPE[0]:F03_SCOPE[1]]:
        raise ValueError("R8 changed r6 F03 illustrative establish")
    for old_row, new_row in zip(base["all_75_rows"], rows):
        a, b = copy.deepcopy(old_row), copy.deepcopy(new_row)
        a.pop("spans")
        b.pop("spans")
        if a != b:
            raise ValueError("Protected row metadata changed")
    item = entries[0]
    for frame in range(*SCOPE):
        expected = ("video", item["source"]["path"], item["source"]["sha256"], item["source_start_frame"] + frame - SCOPE[0])
        if after[frame] != expected:
            raise ValueError("Wrong selected r8 source frame")
    return {
        "frames_compared": TOTAL,
        "base_assignment_changed_frames": len(changed),
        "allowed_assignment_ranges": [SCOPE],
        "visually_changed_source_frames": [SCOPE[0] + LOCAL_CHANGE[0], SCOPE[0] + LOCAL_CHANGE[1]],
        "r7_source_pixels_preserved_outside_local": [[0, 42], [102, PLATE_TOTAL]],
        "all_other_assignments_identical": True,
        "all_75_row_metadata_identical": True,
        "retained_r6_f03_establish_identical": True,
    }


def prepare(path: Path) -> dict:
    base = checked_base()
    manifest, entries = checked_selection(path, base)
    rows = patch(base["all_75_rows"], entries)
    mapping = mapping_check(base, rows, entries)
    return {
        "record_type": "ep009_r8_tool_clarity_review_build",
        "status": "prepared_not_rendered",
        "version": "r8-tool-clarity",
        "at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "base_r7_build": bound(BASE),
        "base_r7_verification": bound(BASE_VERIFY),
        "timing_contract": copy.deepcopy(base["timing_contract"]),
        "r6_selections": copy.deepcopy(base["r6_selections"]),
        "r7_selections": copy.deepcopy(base["selections"]),
        "owner_tool_focus_scope": copy.deepcopy(base["owner_tool_focus_scope"]),
        "r8_scope": SCOPE,
        "retained_f03": retained_f03(base),
        "selections": bound(path),
        "direction": manifest["direction"],
        "source_basis": copy.deepcopy(manifest["source_basis"]),
        **{key: copy.deepcopy(base[key]) for key in PROTECTED},
        "retained_P00": copy.deepcopy(base["retained_P00"]),
        "retained_r5_presenters": copy.deepcopy(base["retained_r5_presenters"]),
        "all_75_rows": rows,
        "total_frames": TOTAL,
        "output_master_frames": [0, TOTAL],
        "inserts": entries,
        "mapping_checks": mapping,
        "builder": bound(Path(__file__)),
        "graph_helper": bound(A / "_tools" / "build_r4.py"),
        "owner_accepted": False,
        "release_cleared": False,
        "limits": [
            "Private r8 tool-clarity review revision only. No publication or owner acceptance inferred.",
            "R7 is the frozen assembly base. R8 changes source pixels only at S13 global frames [16794,16854), while retaining r7 decoded source pixels elsewhere and preserving r6 F03.",
            "Every source audio track is discarded; the locked r3 master supplies the complete unchanged program.",
            "The existing presenter and P00/P08 review limitations remain bound unchanged.",
        ],
    }


def save(data: dict, action: str, name: str) -> int:
    if not re.fullmatch(r"ep009-r8-tool-clarity-[A-Za-z0-9_-]+", name):
        raise ValueError("New r8-tool-clarity filename required")
    directory = A / "r8-tool-clarity"
    review = A / "qa" / "r8-tool-clarity"
    manifest = directory / (name + "-BUILD.json")
    graph_path = directory / (name + "-graph.txt")
    log = directory / (name + "-encode.log")
    output = review / (name + ".mp4")
    if any(path.exists() for path in (manifest, graph_path, log, output)):
        raise FileExistsError("Preserve existing r8 artifact/version")
    graph, inputs = graph_for(data)
    directory.mkdir(parents=True, exist_ok=True)
    review.mkdir(parents=True, exist_ok=True)
    with graph_path.open("x") as handle:
        handle.write(graph)
    command = [
        "ffmpeg", "-nostdin", "-n", "-v", "error", "-stats", "-filter_complex_threads", "2", *inputs,
        "-/filter_complex", str(graph_path), "-map", "[vout]", "-map", "[aout]", "-c:v", "libx264",
        "-preset", "medium", "-crf", "16", "-threads", "2", "-pix_fmt", "yuv420p", "-r", "24",
        "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-ac", "2", "-movflags", "+faststart", str(output),
    ]
    data.update(
        output=rel(output),
        graph=bound(graph_path),
        command=command,
        encode_log=rel(log),
        status="rendering_unaccepted_review" if action == "render" else "prepared_not_rendered",
    )
    write(manifest, data)
    if action == "render":
        with log.open("x") as handle:
            result = subprocess.run(command, stdout=handle, stderr=subprocess.STDOUT)
        data.update(encode_exit_code=result.returncode, status="encoded_unverified_review_only" if result.returncode == 0 else "failed_partial_preserved")
        if result.returncode == 0:
            data["output_sha256"] = sha(output)
        manifest.write_text(json.dumps(data, indent=2) + "\n")
    print(json.dumps({"status": data["status"], "build": bound(manifest), "output": rel(output)}))
    return data.get("encode_exit_code", 0)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["inspect", "check", "prepare", "render"])
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--name", default="ep009-r8-tool-clarity-review-r1")
    args = parser.parse_args()
    if args.action == "inspect":
        checked_base()
        print(json.dumps({"status": "r7_base_verified_no_r8_selection_or_render", "scope": SCOPE, "local_clarity_change": LOCAL_CHANGE, "retained_f03": F03_SCOPE}))
        return 0
    if not args.manifest:
        parser.error("--manifest is required")
    data = prepare(args.manifest.resolve())
    if args.action == "check":
        print(json.dumps({"status": "r8_inputs_checked_not_rendered", "mapping": data["mapping_checks"]}))
        return 0
    return save(data, args.action, args.name)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValueError, KeyError, OSError, subprocess.CalledProcessError) as error:
        print("ERROR: " + str(error), file=sys.stderr)
        raise SystemExit(2)
