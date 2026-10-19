#!/usr/bin/env python3
"""Full technical verification of the separate r8 tool-clarity review.

This is a review-only check. It verifies the r7 inheritance, the narrowed
native Node-RED crop, full decode, source mapping and locked master audio. It
does not accept the candidate or clear release.
"""
import argparse
import copy
import datetime
import sys
from pathlib import Path

sys.dont_write_bytecode = True

import build_r8 as b
from verify_r3 import audio_check
from verify_r2 import video_check, loudness


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("build", type=Path)
    args = parser.parse_args()
    path = args.build.resolve()
    path.relative_to(b.A / "r8-tool-clarity")
    data = b.read(path)
    report = path.with_name(path.name.replace("-BUILD.json", "-VERIFICATION.json"))
    if report == path or report.exists():
        raise FileExistsError("Preserve existing r8 verification/build")
    if data.get("record_type") != "ep009_r8_tool_clarity_review_build" or data.get("status") != "encoded_unverified_review_only":
        raise ValueError("Completed full r8 tool-clarity review required")

    base = b.checked_base()
    errors: list[str] = []
    bound_keys = (
        "base_r7_build", "base_r7_verification", "timing_contract",
        "r6_selections", "r7_selections", "owner_tool_focus_scope",
        "selections", "direction", "builder", "graph_helper", "graph",
    )
    for key in bound_keys:
        b.verify_bound(data[key])
    if data["base_r7_build"] != b.bound(b.BASE) or data["base_r7_verification"] != b.bound(b.BASE_VERIFY):
        raise ValueError("Wrong r7 base bindings")
    if data["timing_contract"] != base["timing_contract"]:
        raise ValueError("Wrong inherited timing contract")
    if data["r6_selections"] != base["r6_selections"] or data["r7_selections"] != base["selections"]:
        raise ValueError("Wrong inherited selection bindings")
    if data["owner_tool_focus_scope"] != base["owner_tool_focus_scope"]:
        raise ValueError("Wrong inherited owner scope")
    if data.get("r8_scope") != b.SCOPE or data.get("retained_f03") != b.retained_f03(base):
        raise ValueError("R8 scope or F03 preservation mismatch")

    for key in b.PROTECTED:
        b.verify_bound(data[key])
        if data[key] != base[key]:
            errors.append("Protected binding changed: " + key)
    if data["retained_P00"] != base["retained_P00"] or data["retained_r5_presenters"] != base["retained_r5_presenters"]:
        errors.append("Presenter records changed")
    if data["total_frames"] != b.TOTAL or data["output_master_frames"] != [0, b.TOTAL]:
        errors.append("Full timeline changed")

    manifest, entries = b.checked_selection(b.verify_bound(data["selections"]), base)
    if data.get("source_basis") != manifest.get("source_basis"):
        errors.append("R8 source basis changed")
    if entries != data["inserts"]:
        errors.append("Selected source provenance changed")
    expected_rows = b.patch(base["all_75_rows"], entries)
    if expected_rows != data["all_75_rows"]:
        errors.append("Unexpected row/source map")
    mapping = b.mapping_check(base, data["all_75_rows"], entries)

    graph, inputs = b.graph_for(copy.deepcopy(data))
    if b.verify_bound(data["graph"]).read_text() != graph:
        errors.append("Emitted graph differs from selected sources")
    actual_inputs = [data["command"][index + 1] for index, token in enumerate(data["command"][:-1]) if token == "-i"]
    expected_inputs = [inputs[index + 1] for index, token in enumerate(inputs[:-1]) if token == "-i"]
    if actual_inputs != expected_inputs:
        errors.append("Encoded input order differs from graph")

    output = b.verify_bound({"path": data["output"], "sha256": data["output_sha256"]})
    output.relative_to(b.A / "qa" / "r8-tool-clarity")
    info = b.probe(output)
    video_stream = next(stream for stream in info["streams"] if stream["codec_type"] == "video")
    audio_stream = next(stream for stream in info["streams"] if stream["codec_type"] == "audio")
    if (video_stream["width"], video_stream["height"], video_stream["r_frame_rate"], int(video_stream["nb_read_frames"])) != (1280, 720, "24/1", b.TOTAL):
        errors.append("Video format/count")
    if (audio_stream["sample_rate"], audio_stream["channels"]) != ("48000", 2):
        errors.append("Audio format")
    if abs(float(info["format"]["duration"]) - b.TOTAL / 24) > 0.002:
        errors.append("Duration")

    video = video_check(output, b.TOTAL)
    video.pop("planned_exception", None)
    video["planned_uniform_frames"] = [1427]
    video["unplanned_uniform_frames"] = [frame for frame in video["uniform_frames"] if frame != 1427]
    if video["decoded_frames"] != b.TOTAL or video["decode_exit_code"] or video["unplanned_uniform_frames"]:
        errors.append("Video decode/unplanned uniform picture")

    audio = audio_check(output, b.verify_bound(data["master"]), [0, b.TOTAL])
    if audio["compared_samples"] != 58646000 or any(audio["decode_exit_codes"]):
        errors.append("Audio decode/sample count")
    if audio["min_voiced_window_corr"] < 0.999 or audio["max_abs_voiced_window_rms_db"] > 0.1:
        errors.append("Locked audio identity/level")
    if not 0 <= audio["aac_padding_samples"] <= 1024 or audio["padding_peak_abs"] > 1e-5:
        errors.append("Audio tail")

    result = {
        "record_type": "ep009_r8_tool_clarity_full_review_technical_verification",
        "at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "status": "technical_checks_failed" if errors else "technical_checks_passed_private_review_candidate",
        "errors": errors,
        "build": b.bound(path),
        "output": b.bound(output),
        "base_r7_build": b.bound(b.BASE),
        "base_r7_verification": b.bound(b.BASE_VERIFY),
        "master": data["master"],
        "mapping": mapping,
        "emitted_graph_matches_selections": graph == b.verify_bound(data["graph"]).read_text(),
        "all_presenter_records_retained": data["retained_r5_presenters"] == base["retained_r5_presenters"],
        "r6_f03_establish_retained": mapping["retained_r6_f03_establish_identical"],
        "r7_plate_pixels_retained_outside_tight_crop": mapping["r7_source_pixels_preserved_outside_local"],
        "probe": info,
        "video": video,
        "audio": audio,
        "loudness": loudness(output),
        "owner_accepted": False,
        "release_cleared": False,
        "limits": [
            "Full decode, source mapping, graph/input binding and decoded-audio identity are technical checks. Native-tool readability, focus quality, workflow truth and audiovisual integration require review.",
            "R8 is a private candidate. The later local Node-RED configuration view is not a fresh provider execution; no provider call or runtime mutation occurred for this revision.",
            "Existing r5 presenter/P00/P08 limitations remain unchanged. This record does not accept the candidate or clear release.",
        ],
    }
    b.write(report, result)
    print(b.json.dumps({"status": result["status"], "errors": errors, "report": b.bound(report)}))
    return int(bool(errors))


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValueError, KeyError, OSError) as error:
        print("ERROR: " + str(error), file=sys.stderr)
        raise SystemExit(2)
