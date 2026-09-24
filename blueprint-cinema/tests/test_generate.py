from __future__ import annotations

import json
from pathlib import Path

import pytest

from blueprint_cinema import generate as gen
from blueprint_cinema.validation import ValidationFailure

REF_URL = "https://cdn.example/look-a.png"


@pytest.fixture
def episode(tmp_path: Path) -> Path:
    (tmp_path / "presenter").mkdir()
    (tmp_path / "presenter" / "look-a.png").write_bytes(b"look a")
    return tmp_path


def _lock(episode: Path, **kwargs) -> dict:
    return gen.lock_look(
        episode, [(episode / "presenter" / "look-a.png", REF_URL)], "inn lobby", "chambray shirt", "Manav", **kwargs
    )


def _fake_provider(outputs: list[str]):
    calls = []

    def request(method: str, url: str, body: dict | None) -> dict:
        calls.append((method, url, body))
        if method == "POST":
            return {"request_id": "job-1", "status_url": "https://api/status", "response_url": "https://api/response"}
        if url.endswith("status"):
            return {"status": "completed", "video": {"url": outputs[0]}} if outputs else {"status": "completed"}
        return {"video": {"url": outputs[0]}}

    return request, calls


def _presenter_args(image: str = REF_URL) -> dict:
    return {"prompt": "speaks to camera", "image_references": [image], "audio": "https://cdn.example/vo.mp3"}


def test_presenter_job_blocked_without_lock(episode: Path) -> None:
    with pytest.raises(ValidationFailure) as error:
        gen.generate(episode, "higgsfield", "m", _presenter_args(), "presenter", "P01", "r", 1.0, episode / "out", dry_run=True)
    assert error.value.gate == "look_lock"


def test_presenter_job_rejects_unlocked_image(episode: Path) -> None:
    _lock(episode)
    with pytest.raises(ValidationFailure, match="not part of the locked look"):
        gen.generate(
            episode, "higgsfield", "m", _presenter_args("https://cdn.example/other.jpg"),
            "presenter", "P01", "r", 1.0, episode / "out", dry_run=True,
        )


def test_presenter_job_blocked_when_reference_changes(episode: Path) -> None:
    _lock(episode)
    (episode / "presenter" / "look-a.png").write_bytes(b"edited")
    with pytest.raises(ValidationFailure, match="changed after lock"):
        gen.check_look_lock(episode, {})


def test_relock_requires_supersede_and_records_history(episode: Path) -> None:
    _lock(episode)
    with pytest.raises(ValidationFailure, match="--supersede"):
        _lock(episode)
    relocked = _lock(episode, supersede_reason="owner changed room")
    assert relocked["version"] == 2
    assert relocked["history"][0]["reason"] == "owner changed room"


def test_film_lane_needs_no_lock_and_respects_cap(episode: Path) -> None:
    (episode / "ledger").mkdir()
    (episode / "ledger" / "SPEND-LEDGER.json").write_text(json.dumps({"lane_allocations": {"film": {"fal_usd": 5.0}}}))
    plan = gen.generate(episode, "fal", "fal-ai/veo3.1/fast", {"prompt": "x"}, "film", "F01", "r", 4.0, episode / "out", dry_run=True)
    assert plan["budget"] == "film fal: $4.00 of $5.00 after this job"
    (episode / "ledger" / "film.jsonl").write_text(json.dumps({"status": "intent", "provider": "fal", "est_usd": 4.0}) + "\n")
    with pytest.raises(ValidationFailure) as error:
        gen.generate(episode, "fal", "fal-ai/veo3.1/fast", {"prompt": "x"}, "film", "F02", "r", 2.0, episode / "out", dry_run=True)
    assert error.value.gate == "spend_cap"


def test_generate_ledgers_intent_and_done(episode: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    _lock(episode)
    request, calls = _fake_provider(["https://cdn.example/take.mp4"])

    def fake_download(url: str, destination: Path) -> dict:
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(b"video")
        return {"path": str(destination), "url": url, "sha256": "abc"}

    monkeypatch.setattr(gen, "download", fake_download)
    monkeypatch.setattr(gen.time, "sleep", lambda _: None)
    row = gen.generate(
        episode, "higgsfield", "bytedance/seedance", _presenter_args(), "presenter", "P01", "take", 1.5,
        episode / "out", request=request,
    )
    assert row["status"] == "done" and row["job_id"] == "job-1" and row["look_version"] == 1
    assert (episode / "out" / "P01.mp4").is_file()
    rows = [json.loads(line) for line in (episode / "ledger" / "presenter.jsonl").read_text().splitlines()]
    assert [r["status"] for r in rows] == ["intent", "done"]
    assert calls[0][1] == "https://api.higgsfield.ai/bytedance/seedance"


def test_generate_records_failure(episode: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    request, _ = _fake_provider([])
    monkeypatch.setattr(gen.time, "sleep", lambda _: None)
    with pytest.raises(ValidationFailure, match="no media URL"):
        gen.generate(episode, "higgsfield", "m", {"prompt": "x"}, "film", "F01", "r", 1.0, episode / "out", request=request)
    rows = [json.loads(line) for line in (episode / "ledger" / "film.jsonl").read_text().splitlines()]
    assert [r["status"] for r in rows] == ["intent", "failed"]
