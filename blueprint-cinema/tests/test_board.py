from __future__ import annotations

import json
from pathlib import Path

import pytest

from blueprint_cinema import board

DIRECTION = """# Plan

## S00 Cold open

- **Narrative job:** establish the guest.
- **Viewer before:** knows nothing. **After:** knows the guest
  and the relay.

| Seg | Master | Form | Cues |
|---|---|---|---|
| seg001 F01 | 0-2 | Film: he slides the key back on `W000003 key 1.20` | in |

- **Must not imply:** a named guest.

## S01 Question

- **Job:** ask it.

| Seg | Form and choreography | Rejected alternative |
|---|---|---|
| seg002 model 2-4 | Drawn inn establishes | Opening on evidence |

- **seg003 P01:** presenter asks
  the question.
"""


def _row(seg: str, scene: str, lane: str, frames: list[int], original: list[int], sha: str, **span) -> dict:
    fps = 24
    return {
        "id": seg, "scene": scene, "lane": lane,
        "original": {"take_id": "", "index_status": "built"},
        "original_frames": original, "output_frames": frames,
        "output_seconds": [frames[0] / fps, frames[1] / fps],
        "spans": [{"source": {"path": f"{seg}.mp4", "sha256": sha}, "output_frames": frames, **span}],
    }


def _inputs(tmp_path: Path, rows: list[dict], lock: dict | None = None) -> dict:
    build = tmp_path / "BUILD.json"
    build.write_text(json.dumps({"version": "r1", "fps": 24, "total_frames": 144, "output": str(tmp_path / "cut.mp4"),
                                 "output_sha256": "v" * 64, "all_75_rows": rows}))
    plan = tmp_path / "SHOT-PLAN.json"
    plan.write_text(json.dumps({"segments": [{"id": r["id"], "summary": f"summary {r['id']}"} for r in rows]}))
    transcript = tmp_path / "words.json"
    transcript.write_text(json.dumps({"words": [{"token": "key", "start": 1.2, "end": 1.5}, {"token": "why?", "start": 4.5, "end": 4.9}]}))
    direction = tmp_path / "DIRECTION-PLAN.md"
    direction.write_text(DIRECTION)
    locks = []
    if lock:
        path = tmp_path / "OWNER-LOCK.json"
        path.write_text(json.dumps(lock))
        locks.append(path)
    return {"build_path": build, "plan_path": plan, "transcript_path": transcript, "direction_path": direction,
            "lock_paths": locks, "out_path": tmp_path / "qa" / "board.html", "title": "Test board"}


def _rows(sha3: str = "c" * 64, **span) -> list[dict]:
    return [
        _row("seg001", "S00", "film", [0, 48], [0, 48], "a" * 64),
        _row("seg002", "S01", "model", [48, 96], [48, 110], "b" * 64),
        _row("seg003", "S01", "presenter", [96, 144], [110, 158], sha3, **span),
    ]


def test_direction_reads_every_segment_format_and_scene_fields():
    scenes, forms = board.parse_direction(DIRECTION)
    assert forms["seg001"] == "Film: he slides the key back on “key”"
    assert forms["seg002"] == "Drawn inn establishes"
    assert forms["seg003"] == "presenter asks the question."
    assert scenes["S00"]["job"] == "establish the guest."
    assert scenes["S00"]["after"] == "knows the guest and the relay."
    assert scenes["S00"]["must_not_imply"] == "a named guest."
    assert scenes["S01"]["job"] == "ask it."


def test_board_rows_carry_words_forms_and_video_path(tmp_path: Path):
    result = board.build_board(**_inputs(tmp_path, _rows()))
    first, _, third = result["rows"]
    assert first["words"] == [["key", 1.2, 1.5]] and third["words"] == [["why?", 4.5, 4.9]]
    assert first["form"].startswith("Film:")
    assert result["video_src"] == "../cut.mp4"
    assert (tmp_path / "qa" / "board.html").read_text().count("Test board") >= 1
    record = json.loads((tmp_path / "qa" / "board.json").read_text())
    assert record["digest"] == result["digest"] and len(record["rows"]) == 3


def test_lock_on_original_frames_marks_the_output_row(tmp_path: Path):
    lock = {"scope": "brand pause", "protected_edits": {"brand_removed_original_frames": [60, 100]}}
    rows = {r["id"]: r for r in board.build_board(**_inputs(tmp_path, _rows(), lock))["rows"]}
    assert rows["seg002"]["state"] == "locked" and "brand pause" in rows["seg002"]["note"]
    assert rows["seg001"]["state"] == "unreviewed"


def test_flag_stands_unless_an_owner_lock_covers_it(tmp_path: Path):
    flagged = _rows(sync_status="flagged_unresolved")
    assert board.build_board(**_inputs(tmp_path, flagged))["rows"][2]["state"] == "flagged"
    lock = {"scope": "opening", "selected": {"output_frames": [96, 144]}}
    assert board.build_board(**_inputs(tmp_path, flagged, lock))["rows"][2]["state"] == "locked"


def test_digest_changes_when_any_source_changes(tmp_path: Path):
    before = board.build_board(**_inputs(tmp_path, _rows()))["digest"]
    again = board.build_board(**_inputs(tmp_path, _rows()))["digest"]
    after = board.build_board(**_inputs(tmp_path, _rows(sha3="d" * 64)))["digest"]
    assert before == again != after


def test_thumbnails_written_when_ffmpeg_and_video_exist(tmp_path: Path, monkeypatch):
    fake = tmp_path / "ffmpeg"
    fake.write_text('#!/bin/sh\nfor last; do :; done\nprintf jpg > "$last"\n')
    fake.chmod(0o755)
    monkeypatch.setenv("OE_FFMPEG", str(fake))
    inputs = _inputs(tmp_path, _rows())
    assert board.build_board(**inputs, thumbs=True)["thumbs_made"] == 0
    (tmp_path / "cut.mp4").write_bytes(b"video")
    result = board.build_board(**inputs, thumbs=True)
    assert result["thumbs_made"] == 3
    assert result["rows"][0]["thumb"] == "board-thumbs/seg001.jpg"
    assert (tmp_path / "qa" / "board-thumbs" / "seg001.jpg").read_text() == "jpg"


def test_review_binds_sources_and_flags_later_changes(tmp_path: Path):
    inputs = _inputs(tmp_path, _rows())
    board.build_board(**inputs)
    page = inputs["out_path"]
    board.record_review(page, "approve", "S01", "Manav", "", "S01 is good")
    board.record_review(page, "return", "seg001", "Manav", "punch in on the key", "zoom in")
    states = {r["id"]: r["review"]["state"] for r in board.read_page_board(page)["rows"]}
    assert states == {"seg001": "returned", "seg002": "approved", "seg003": "approved"}
    assert [r["id"] for r in board.check_approved(page, "all")] == ["seg001"]
    assert board.check_approved(page, "S01") == []

    changed = _inputs(tmp_path, _rows(sha3="d" * 64))
    board.build_board(**changed)
    rows = {r["id"]: r["review"]["state"] for r in board.read_page_board(page)["rows"]}
    assert rows["seg003"] == "changed" and rows["seg002"] == "approved"
    assert [r["id"] for r in board.check_approved(page, "S01")] == ["seg003"]


def test_review_scope_and_chain_are_enforced(tmp_path: Path):
    inputs = _inputs(tmp_path, _rows())
    board.build_board(**inputs)
    page = inputs["out_path"]
    assert board.resolve_scope(board.read_page_board(page)["rows"], "lane:presenter,S00") == ["seg003", "seg001"]
    with pytest.raises(ValueError):
        board.record_review(page, "return", "seg002", "Manav", "", "")
    with pytest.raises(ValueError):
        board.record_review(page, "approve", "S09", "Manav", "", "")
    board.record_review(page, "approve", "all", "Manav", "", "")
    log = page.parent / "board-reviews.jsonl"
    log.write_text(log.read_text().replace('"approve"', '"return"'))
    with pytest.raises(ValueError):
        board.load_reviews(log)
