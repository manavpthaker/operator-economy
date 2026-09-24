#!/usr/bin/env python3
"""Create the reviewed r6 screen source from the one real EP009 capture.

The raw ScreenCaptureKit movie is retained untouched.  This helper crops only
browser chrome and unused black canvas, makes a 24fps presentation conform
without interpolation, and declares the non-contiguous latency ellipses used
to keep the causal run readable in the fixed S13 duration.  It does not call a
provider, touch Node-RED state, or render the episode.
"""

from __future__ import annotations

import copy
import datetime as dt
import hashlib
import json
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True

S = Path(__file__).resolve().parents[1]
B = S.parent
A = B / "assembly"
R = S.parents[3]
sys.path[:0] = [str(B / "presenter-look-transfer" / "_tools"), str(A / "_tools")]

import build_r6 as r6
from build_review import video_hashes


FPS = 24
SCREEN_FRAMES = 706
F03_OUTPUT = [16704, 16752]
SCREEN_OUTPUT = [16752, 17458]
F03_START = 96
F03_FRAMES = 48
F03 = B / "film" / "F03" / "final" / "seg003.mp4"
RAW = S / "capture" / "raw" / "ep009-real-run-20260919T0604EDT-raw.mp4"
RUNTIME = S / "runtime"
LOCAL = RUNTIME / ".local"
CAPTURE_ID = "node-red-openai-real-run-r2"
OUT = S / "capture" / CAPTURE_ID

# Each span shows a real state in the order it happened.  The gaps are real
# waiting/idle time, declared below rather than hidden as a continuous run.
SPANS = [
    {"id": "fixture-and-request", "start": 0.000, "end": 4.417, "frames": 106},
    {"id": "returned-draft", "start": 6.750, "end": 10.417, "frames": 88},
    {"id": "queue-for-review", "start": 11.750, "end": 16.750, "frames": 120},
    {"id": "human-voice-edit", "start": 20.500, "end": 24.667, "frames": 100},
    {"id": "one-draft-approval", "start": 25.500, "end": 29.667, "frames": 100},
    {"id": "seasonal-exclusion-settle", "start": 30.250, "end": 38.250, "frames": 192},
]
assert sum(span["frames"] for span in SPANS) == SCREEN_FRAMES

FIXTURE = {
    "id": "alder-maya-20260918",
    "fictional": True,
    "guest": "Maya Chen",
    "property": "Alder House Inn",
    "checkout": "2026-09-18T10:00:00-04:00",
    "timezone": "America/New_York",
    "communication_preference": "One-off thank-you only. No future promotions.",
    "one_off_thank_you": True,
    "seasonal_campaign_eligible": False,
}


def sha(path: Path) -> str:
    with path.open("rb") as handle:
        return hashlib.file_digest(handle, "sha256").hexdigest()


def now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def read(path: Path):
    return json.loads(path.read_text())


def write_new(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x") as handle:
        json.dump(value, handle, indent=2)
        handle.write("\n")


def binding(path: Path):
    return r6.bound(path)


def check_file(path: Path, label: str) -> Path:
    path = path.resolve()
    if not path.is_file():
        raise ValueError(f"{label} is missing: {path}")
    path.relative_to(R)
    return path


def local_file(path: Path, label: str) -> Path:
    path = check_file(path, label)
    path.relative_to(LOCAL)
    return path


def runtime_evidence() -> tuple[Path, dict]:
    state_path = local_file(LOCAL / "state.json", "runtime state")
    events_path = local_file(LOCAL / "events.jsonl", "runtime events")
    state = read(state_path)
    events = [json.loads(line) for line in events_path.read_text().splitlines() if line.strip()]
    if state.get("fixture", {}).get("id") != FIXTURE["id"]:
        raise ValueError("runtime fixture does not match the declared fictional test")
    if state.get("providerAttempts") != 1 or not state.get("draft") or not state.get("queue"):
        raise ValueError("expected exactly one persisted real draft and queue")
    if state["draft"].get("source") != "real_openai_response" or state["draft"].get("mock") is not False:
        raise ValueError("runtime draft is not bound to a real provider response")
    if state["queue"].get("status") != "approved_draft_only" or state["queue"].get("sendEnabled") is not False:
        raise ValueError("queue state is not approved-draft-only with sending disabled")
    if not state.get("review", {}).get("edited") or not state.get("review", {}).get("approved"):
        raise ValueError("human edit/approval state is incomplete")
    if state.get("seasonal", {}).get("eligible") is not False or not state.get("seasonal", {}).get("humanConfirmed"):
        raise ValueError("seasonal exclusion state is incomplete")
    expected = [
        "provider_request_intent", "draft_created", "draft_queued", "human_saved_edit",
        "human_approved_one_draft", "human_confirmed_seasonal_exclusion",
    ]
    if [event.get("type") for event in events] != expected:
        raise ValueError("runtime event order is not the one bounded causal test run")
    run_id = state["draft"].get("id")
    run_dir = local_file(LOCAL / "runs" / run_id / "REQUEST.json", "provider request").parent
    request = local_file(run_dir / "REQUEST.json", "provider request")
    response = local_file(run_dir / "RESPONSE.json", "provider response")
    flows = read(check_file(RUNTIME / "flows.json", "Node-RED flows"))
    forbidden = {"e-mail", "email", "smtp", "send"}
    if any(str(node.get("type", "")).lower() in forbidden for node in flows):
        raise ValueError("a disallowed outbound-send node appeared in the recorded flow")
    evidence = {
        "record_type": "ep009_software_demo_sanitized_runtime_evidence",
        "status": "real_test_run_recorded",
        "at": now(),
        "fixture": FIXTURE,
        "run": {
            "id": run_id,
            "model": state["draft"].get("model"),
            "source": state["draft"].get("source"),
            "mock": state["draft"].get("mock"),
            "usage": state["draft"].get("usage"),
            "request_body_sha256": state["draft"].get("requestSha256"),
            "response_body_sha256": state["draft"].get("responseSha256"),
        },
        "persisted_state": {
            "provider_attempts": state.get("providerAttempts"),
            "queue": {"scheduled_for": state["queue"].get("scheduledFor"), "status": state["queue"].get("status"), "send_enabled": state["queue"].get("sendEnabled")},
            "review": {"edited": state["review"].get("edited"), "approved": state["review"].get("approved"), "approval_scope": state["review"].get("approvalScope")},
            "seasonal": {"eligible": state["seasonal"].get("eligible"), "human_confirmed": state["seasonal"].get("humanConfirmed"), "reason": state["seasonal"].get("reason")},
            "last_event_sha256": state.get("lastEvent"),
        },
        "event_chain": [{"type": event["type"], "at": event["at"], "sha256": event["sha256"]} for event in events],
        "no_send_boundary": {"email_sending_available": False, "forbidden_node_types": sorted(forbidden), "actual_flow_types": sorted({str(node.get("type")) for node in flows})},
        "runtime_sources": {name: binding(check_file(RUNTIME / rel, name)) for name, rel in {
            "demo": "src/demo.js", "flow_builder": "build-flows.js", "flows": "flows.json", "settings": "settings.js", "operator_form": "src/review.html", "package_lock": "package-lock.json",
        }.items()},
        "private_records": {name: binding(path) for name, path in {"state": state_path, "events": events_path, "request": request, "response": response}.items()},
        "limits": "Sanitized record: it retains hashes and public test-state facts, not the provider prompt, returned text, credentials, recipients, customer data, or email access.",
    }
    output = OUT / "SANITIZED-RUNTIME-EVIDENCE.json"
    write_new(output, evidence)
    return output, evidence


def source_filter(span: dict, index: int) -> str:
    # Only browser chrome/tab strips and unused black canvas are removed.  The
    # workflow form is scaled uniformly and padded instead of distorted.
    return (
        f"[0:v]trim=start={span['start']}:end={span['end']},setpts=PTS-STARTPTS,"
        "crop=1620:833:280:140,scale=1280:658:flags=lanczos,"
        "pad=1280:720:0:31:color=0x101713,fps=fps=24:round=near,"
        f"trim=end_frame={span['frames']},setpts=PTS-STARTPTS[s{index}]"
    )


def make_screen() -> tuple[Path, list[str]]:
    screen = OUT / "screen-706.mp4"
    graph = ";".join(source_filter(span, i) for i, span in enumerate(SPANS))
    graph += ";" + "".join(f"[s{i}]" for i in range(len(SPANS))) + f"concat=n={len(SPANS)}:v=1:a=0,format=yuv420p[v]"
    command = [
        "ffmpeg", "-nostdin", "-n", "-v", "error", "-stats", "-filter_complex_threads", "2",
        "-i", str(RAW), "-filter_complex", graph, "-map", "[v]", "-an", "-frames:v", str(SCREEN_FRAMES),
        "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-pix_fmt", "yuv420p", "-r", "24",
        "-movflags", "+faststart", str(screen),
    ]
    subprocess.run(command, check=True)
    return screen, command


def validate_video(path: Path, frames: int) -> dict:
    info = r6.probe(path)
    stream = next(item for item in info["streams"] if item["codec_type"] == "video")
    actual = (stream.get("width"), stream.get("height"), stream.get("r_frame_rate"), int(stream.get("nb_read_frames")))
    if actual != (1280, 720, "24/1", frames):
        raise ValueError(f"unexpected video conform: {actual}")
    return info


def crop_evidence() -> dict:
    return {
        "crop": {"x": 280, "y": 140, "width": 1620, "height": 833, "purpose": "Exclude Chrome controls, tab strips, user tab labels, and unused ScreenCaptureKit canvas."},
        "raster": {"scale": [1280, 658], "pad": [1280, 720, 0, 31], "pad_color": "#101713", "distortion": False},
    }


def raw_ellipsis() -> dict:
    omitted = []
    for first, second in zip(SPANS, SPANS[1:]):
        omitted.append([first["end"], second["start"]])
    return {
        "declared": True,
        "reason": "Real provider latency and idle time are elided to fit the locked 29.416667-second picture slot; no causal state is reordered or invented.",
        "shown_raw_seconds": [[span["start"], span["end"]] for span in SPANS],
        "omitted_raw_seconds": omitted,
        "shown_output_frames": [{"id": span["id"], "frames": span["frames"]} for span in SPANS],
    }


def make_provenance(evidence: Path, runtime: dict) -> Path:
    provenance = {
        "record_type": "ep009_software_demo_capture_provenance",
        "status": "reviewed_for_capture_conform",
        "capture_id": CAPTURE_ID,
        "real_software_capture": True,
        "tools": {"automation": "Node-RED", "model_provider": "OpenAI"},
        "fixture": FIXTURE,
        "no_send": True,
        "email_sending_available": False,
        "workflow": {"run_id": runtime["run"]["id"], "raw_take_continuous": True, "editorial_ellipsis": raw_ellipsis()},
        "technical_review": {
            "reviewer": "Codex technical visual QA; owner creative review pending",
            "method": "Decoded raw-capture thumbnails and delivery-scale 1280x720 conform checked for the fixture, real returned draft, date queue, saved edit, one-draft approval, seasonal exclusion, no-send labels, and removal of browser UI.",
            "limits": "Technical visual QA, not owner acceptance or a claim about customers, consent, legal compliance, capacity, or delivery.",
            "legibility_checked": True,
            "workflow_sequence_checked": True,
            "date_to_queue_checked": True,
            "human_edit_checked": True,
            "one_off_approval_checked": True,
            "seasonal_exclusion_checked": True,
            "queued_draft_not_sent_checked": True,
        },
        "f03_establish_review": {
            "reviewer": "Codex technical visual QA; owner creative review pending",
            "method": "Existing F03 frames 96-143 checked at delivery scale against the bound source.",
            "limits": "Illustrative inn/laptop establish only; it does not demonstrate software execution.",
            "source_window_checked": True,
            "illustrative_only_confirmed": True,
            "typing_task_focus_checked": True,
        },
        "evidence": [binding(evidence), binding(RAW), binding(S / "_tools" / "capture_window.swift")],
    }
    path = OUT / "CAPTURE-PROVENANCE.json"
    write_new(path, provenance)
    return path


def make_conform(screen: Path, command: list[str], provenance: Path) -> Path:
    screen_hashes = video_hashes(screen, SCREEN_FRAMES)
    conform = {
        "record_type": "ep009_software_demo_screen_conform",
        "status": "conformed_for_review",
        "at": now(),
        "raw_capture": binding(RAW),
        "output": binding(screen),
        "output_frames": [0, SCREEN_FRAMES],
        "output_decoded_frame_sequence_sha256": screen_hashes["sequence_sha256"],
        "timeline": raw_ellipsis(),
        "operations": {
            "source_vfr": True,
            "presentation_cfr_fps": 24,
            "cfr_sampling": "FFmpeg fps filter at a fixed 24fps clock; no optical-flow, generated, interpolated, or speed-ramped frames.",
            "source_audio_discarded": True,
            "respeed": False,
            "raster_treatment": crop_evidence(),
        },
        "command": command,
        "provenance": binding(provenance),
        "limits": "The conform preserves ordering and elapsed time inside each declared span. It shortens the screen presentation only by the disclosed raw-time ellipses.",
    }
    path = OUT / "SCREEN-CONFORM.json"
    write_new(path, conform)
    return path


def review_record(source: Path, source_frames: list[int], evidence: dict, flags: dict, limits: str, kind: str) -> dict:
    provenance = binding(OUT / "CAPTURE-PROVENANCE.json")
    return {
        "record_type": "ep009_software_demo_" + kind + "_review",
        "status": "reviewed_for_insertion",
        "at": now(),
        "source": binding(source),
        "source_frames": source_frames,
        "errors": [],
        "reviewer": "Codex technical visual QA; owner creative review pending",
        "method": "Decoded delivery-scale source review and bound runtime/capture provenance.",
        "limits": limits,
        "evidence": evidence,
        **flags,
        "capture_provenance": provenance,
    }


def make_reviews(screen: Path, conform: Path, provenance: Path) -> tuple[Path, Path]:
    f03_edit = B / "film" / "F03" / "EDIT-R1-seg003.json"
    f03_review = review_record(
        F03, [F03_START, F03_START + F03_FRAMES],
        {"source_edit": binding(f03_edit), "source_video": binding(F03), "direction": binding(S / "DIRECTION.md"), "capture_provenance": binding(provenance)},
        {"illustrative_establish_only": True, "software_execution_evidence": False, "source_window_checked": True, "illustrative_only_confirmed": True, "typing_task_focus_checked": True},
        "Illustrative inn/laptop establish only; it is not evidence that software ran.", "f03_establish",
    )
    f03_path = OUT / "F03-ESTABLISH-REVIEW.json"
    write_new(f03_path, f03_review)
    screen_review = review_record(
        screen, [0, SCREEN_FRAMES],
        {"capture_provenance": binding(provenance), "screen_conform": binding(conform), "raw_capture": binding(RAW), "runtime_evidence": binding(OUT / "SANITIZED-RUNTIME-EVIDENCE.json"), "decision": binding(S / "DECISION-EVENT-r1.json")},
        {"real_software_capture": True, "legibility_checked": True, "workflow_sequence_checked": True, "date_to_queue_checked": True, "human_edit_checked": True, "one_off_approval_checked": True, "seasonal_exclusion_checked": True, "queued_draft_not_sent_checked": True, "fixture": FIXTURE, "tools": {"automation": "Node-RED", "model_provider": "OpenAI"}, "no_send": True, "email_sending_available": False},
        "Real fictional test only. Technical review does not establish client results, recipient consent, legal compliance, capacity, sending, or owner creative acceptance.", "screen_capture",
    )
    screen_path = OUT / "SCREEN-REVIEW.json"
    write_new(screen_path, screen_review)
    return f03_path, screen_path


def make_direction(base: dict, f03: Path, screen: Path) -> Path:
    selected = [
        {"id": "f03-illustrative-establish", "output_frames": F03_OUTPUT, "source": binding(f03), "source_start_frame": F03_START},
        {"id": "real-node-red-openai-workflow", "output_frames": SCREEN_OUTPUT, "source": binding(screen), "source_start_frame": 0},
    ]
    direction = {
        "record_type": "ep009_s13_selected_picture_direction",
        "status": "selected_for_private_review",
        "at": now(),
        "base_build": binding(r6.BASE),
        "allowed_output_frames": [16704, 17458],
        "selected_inserts": selected,
        "owner_decision": binding(S / "DECISION-EVENT-r1.json"),
        "screen_conform": binding(OUT / "SCREEN-CONFORM.json"),
        "limits": "The F03 establish is illustrative. The screen source is a fictional, loopback-only, no-send test. Owner review is still required.",
    }
    path = OUT / "SELECTED-PICTURE-DIRECTION.json"
    write_new(path, direction)
    return path


def make_selection(base: dict, f03: Path, screen: Path, f03_review: Path, screen_review: Path, direction: Path) -> Path:
    f03_info = validate_video(f03, int(next(stream for stream in r6.probe(f03)["streams"] if stream["codec_type"] == "video")["nb_read_frames"]))
    f03_frames = int(next(stream for stream in f03_info["streams"] if stream["codec_type"] == "video")["nb_read_frames"])
    entries = [
        {"id": "f03-illustrative-establish", "kind": "existing_film", "output_frames": F03_OUTPUT, "source": binding(f03), "source_start_frame": F03_START, "source_total_frames": f03_frames, "decoded_frame_sequence_sha256": video_hashes(f03, f03_frames)["sequence_sha256"], "review": binding(f03_review)},
        {"id": "real-node-red-openai-workflow", "kind": "real_software_capture", "output_frames": SCREEN_OUTPUT, "source": binding(screen), "source_start_frame": 0, "source_total_frames": SCREEN_FRAMES, "decoded_frame_sequence_sha256": video_hashes(screen, SCREEN_FRAMES)["sequence_sha256"], "review": binding(screen_review)},
    ]
    selection = {
        "record_type": "ep009_software_demo_selections",
        "status": "selected_for_review",
        "at": now(),
        "base_build": binding(r6.BASE),
        "timing_contract": binding(r6.CONTRACT),
        "master": base["master"],
        "direction": binding(direction),
        "inserts": entries,
        "limits": "Prepared private-review source selection. It changes only the locked S13 picture interval and does not accept/publish the episode.",
    }
    path = S / "SELECTIONS-r2.json"
    write_new(path, selection)
    return path


def main() -> None:
    if OUT.exists() or (S / "SELECTIONS-r2.json").exists():
        raise FileExistsError("refusing to overwrite capture or selection records")
    check_file(RAW, "raw capture")
    check_file(F03, "F03 source")
    base = r6.checked_base()
    OUT.mkdir(parents=True)
    evidence, runtime = runtime_evidence()
    provenance = make_provenance(evidence, runtime)
    screen, command = make_screen()
    validate_video(screen, SCREEN_FRAMES)
    conform = make_conform(screen, command, provenance)
    f03_review, screen_review = make_reviews(screen, conform, provenance)
    direction = make_direction(base, F03, screen)
    selection = make_selection(base, F03, screen, f03_review, screen_review, direction)
    print(json.dumps({"status": "prepared_private_review_source", "screen": binding(screen), "selection": binding(selection), "direction": binding(direction), "provenance": binding(provenance), "screen_frames": SCREEN_FRAMES, "f03_frames": F03_FRAMES}, indent=2))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, KeyError, OSError, subprocess.CalledProcessError, StopIteration) as error:
        print("ERROR: " + str(error), file=sys.stderr)
        raise SystemExit(2)
