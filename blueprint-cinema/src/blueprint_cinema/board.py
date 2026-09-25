"""Episode review board: one page that shows the whole cut next to its plan.

Every segment row carries the spoken words, the planned form, the scene's job, the source take,
and its review status, beside a player that follows the cut. The board digest binds every input
and every source hash the page shows, so a later owner lock can refuse a changed board.
"""
from __future__ import annotations

import html
import json
import os
import re
import shutil
import subprocess
from pathlib import Path
from typing import Any

from datetime import datetime, timezone

from .hashes import sha256_file, sha256_json
from .paths import REPO_ROOT

BOARD_VERSION = "board-v1"
TEMPLATE = Path(__file__).with_name("board_template.html")


def _repo_path(value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else REPO_ROOT / path


def _rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(REPO_ROOT.resolve()).as_posix()
    except ValueError:
        return path.resolve().as_posix()


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _clean(text: str) -> str:
    text = re.sub(r"`W\d+ (\S+?)[,.;:?!]? \d+(?:\.\d+)?`", r"“\1”", text)
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    return re.sub(r"\s+", " ", text).strip()


def parse_direction(markdown: str) -> tuple[dict[str, dict], dict[str, str]]:
    """Scene jobs and per-segment forms from a DIRECTION-PLAN.md.

    Scenes are `## S00 Title` sections (`## S22 to S24 Title` covers a range). A segment's form
    comes from a table row whose first cell starts with its id (the `Form...` column), a
    `- **seg020 ...:**` bullet, or a `### ... seg036 ...` subsection.
    """
    fields = {"Narrative job": "job", "Job": "job", "Viewer before": "before", "Must not imply": "must_not_imply"}
    scenes: dict[str, dict] = {}
    forms: dict[str, str] = {}
    current: list[str] = []
    target: tuple[str, str] | None = None
    form_column = 1

    def put(kind: str, key: str, text: str) -> None:
        if kind == "form":
            forms[key] = _clean(forms.get(key, "") + " " + text)
            return
        for scene_id in current:
            scenes[scene_id][key] = _clean(scenes[scene_id][key] + " " + text)

    for line in markdown.splitlines():
        heading = re.match(r"^## (S\d\d)(?: to (S\d\d))? (.+)$", line)
        if heading:
            first, last, title = heading.groups()
            current = [first] if not last else [f"S{n:02d}" for n in range(int(first[1:]), int(last[1:]) + 1)]
            for scene_id in current:
                scenes[scene_id] = {"title": title.strip(), "job": "", "before": "", "after": "", "must_not_imply": ""}
            target = None
            continue
        if line.startswith("## "):
            current, target = [], None
            continue
        if not current:
            continue
        sub = re.match(r"^### .*?(seg\d{3})", line)
        if sub:
            target = ("form", sub.group(1)) if sub.group(1) not in forms else None
            continue
        if line.startswith("### "):
            target = None
            continue
        if line.startswith("|"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if cells and cells[0].lower() == "seg":
                form_column = next((i for i, c in enumerate(cells) if c.lower().startswith("form")), 1)
            elif cells and re.match(r"seg\d{3}", cells[0]) and len(cells) > form_column:
                forms.setdefault(cells[0][:6], _clean(cells[form_column]))
            target = None
            continue
        bullet = re.match(r"^- \*\*(seg\d{3})[^*]*:\*\*\s*(.*)$", line)
        if bullet:
            forms.pop(bullet.group(1), None)
            target = ("form", bullet.group(1))
            put(*target, bullet.group(2))
            continue
        item = re.match(r"^- \*\*(Narrative job|Job|Viewer before|Must not imply):\*\*\s*(.*)$", line)
        if item:
            label, text = item.groups()
            target = ("scene", fields[label])
            if "**After:**" in text:
                before, after = text.split("**After:**", 1)
                put("scene", "before", before)
                target = ("scene", "after")
                text = after
            put(*target, text)
            continue
        if line.startswith("- "):
            target = None
            continue
        if target and line.strip():
            if target[0] == "form" and len(forms.get(target[1], "")) > 600:
                continue
            put(*target, line)
        elif not line.strip() and target and target[0] == "scene":
            target = None
    return scenes, forms


def _overlaps(a: list[int], b: list[int]) -> bool:
    return a[0] < b[1] and b[0] < a[1]


def lock_ranges(lock: dict, rows: list[dict]) -> list[list[int]]:
    """Output-frame ranges an owner lock protects.

    Keys ending in `output_frames` are output ranges already. Keys ending in `original_frames`
    are mapped onto the output rows whose original frames they overlap.
    """
    ranges: list[list[int]] = []

    def walk(value: Any, key: str = "") -> None:
        if isinstance(value, dict):
            for child_key, child in value.items():
                walk(child, child_key)
        elif isinstance(value, list):
            if len(value) == 2 and all(isinstance(v, int) for v in value):
                if key.endswith("output_frames"):
                    ranges.append(list(value))
                elif key.endswith("original_frames"):
                    for row in rows:
                        if _overlaps(row["original_frames"], value):
                            ranges.append(list(row["output_frames"]))
            else:
                for child in value:
                    walk(child, key)

    walk(lock)
    return ranges


def _covered(frames: list[int], ranges: list[list[int]]) -> bool:
    return any(r[0] <= frames[0] and frames[1] <= r[1] for r in ranges)


def _status(original: dict, spans: list[dict], frames: list[int], locks: list[dict]) -> tuple[str, str]:
    """Flagged beats locked unless an owner lock covers the flagged span; an owner lock is the later decision."""
    touching = [lock for lock in locks if any(_overlaps(frames, r) for r in lock["ranges"])]
    protected = [r for lock in touching for r in lock["ranges"]]
    flags = [
        span.get("sync_status") for span in spans
        if str(span.get("sync_status") or "").startswith("flagged")
        and not _covered(span.get("output_frames") or frames, protected)
    ]
    parts = [original.get("index_status") or ""]
    parts += [f"owner lock: {lock['scope']}" for lock in touching]
    parts += flags
    note = "; ".join(p for p in parts if p)
    if flags:
        return "flagged", note
    if touching:
        return "locked", note
    return "unreviewed", note


def build_board(
    build_path: Path,
    plan_path: Path,
    transcript_path: Path,
    direction_path: Path,
    lock_paths: list[Path],
    out_path: Path,
    title: str,
    thumbs: bool = True,
    reviews_path: Path | None = None,
) -> dict:
    build = _load(build_path)
    plan = _load(plan_path)
    transcript = _load(transcript_path)
    words = transcript.get("words", [])
    scenes, forms = parse_direction(direction_path.read_text(encoding="utf-8"))
    plan_segments = {segment["id"]: segment for segment in plan.get("segments", [])}
    rows_in = build.get("all_75_rows") or build.get("rows") or []
    if not rows_in:
        raise ValueError(f"{build_path} has no segment rows")

    locks = []
    for lock_path in lock_paths:
        lock = _load(lock_path)
        ranges = lock_ranges(lock, rows_in)
        locks.append({
            "path": _rel(lock_path),
            "sha256": sha256_file(lock_path),
            "scope": lock.get("scope", ""),
            "ranges": ranges,
        })

    fps = build.get("fps") or plan.get("fps") or 24
    rows = []
    for row in rows_in:
        start, end = row["output_seconds"]
        segment = plan_segments.get(row["id"], {})
        original = row.get("original", {})
        spans = row.get("spans", [])
        state, note = _status(original, spans, row["output_frames"], locks)
        sources = sorted({(s["source"]["path"], s["source"]["sha256"]) for s in spans if "source" in s})
        rows.append({
            "id": row["id"],
            "scene": row["scene"],
            "lane": row["lane"],
            "take": original.get("take_id") or segment.get("take_id") or "",
            "frames": row["output_frames"],
            "start": round(start, 3),
            "end": round(end, 3),
            "form": forms.get(row["id"]) or segment.get("summary", ""),
            "summary": segment.get("summary", ""),
            "state": state,
            "note": note,
            "words": [
                [w["token"], round(w["start"], 3), round(w["end"], 3)]
                for w in words
                if start <= w["start"] < end
            ],
            "sources": [{"path": p, "sha256": h} for p, h in sources],
        })

    video = build.get("output", "")
    video_path = _repo_path(video) if video else None
    video_src = os.path.relpath(video_path, out_path.parent).replace(os.sep, "/") if video_path else ""
    inputs = {
        "build": {"path": _rel(build_path), "sha256": sha256_file(build_path)},
        "plan": {"path": _rel(plan_path), "sha256": sha256_file(plan_path)},
        "transcript": {"path": _rel(transcript_path), "sha256": sha256_file(transcript_path)},
        "direction": {"path": _rel(direction_path), "sha256": sha256_file(direction_path)},
        "video": {"path": video, "sha256": build.get("output_sha256", "")},
        "locks": [{"path": lock["path"], "sha256": lock["sha256"]} for lock in locks],
    }
    bound = {
        "version": BOARD_VERSION,
        "inputs": inputs,
        "rows": [{"id": r["id"], "frames": r["frames"], "sources": r["sources"]} for r in rows],
    }
    board = {
        "record_type": "episode_review_board",
        "version": BOARD_VERSION,
        "title": title,
        "build_version": build.get("version", ""),
        "owner_accepted": bool(build.get("owner_accepted")),
        "fps": fps,
        "total_frames": build.get("total_frames") or (rows[-1]["frames"][1] if rows else 0),
        "video_src": video_src,
        "inputs": inputs,
        "digest": sha256_json(bound),
        "scenes": {k: v for k, v in scenes.items() if any(r["scene"] == k for r in rows)},
        "locks": locks,
        "limits": build.get("limits", []),
        "rows": rows,
    }
    board["thumbs_made"] = write_thumbs(board, video_path, out_path) if thumbs and video_path else 0
    board["reviews_path"] = _rel(reviews_path or default_reviews(out_path))
    apply_reviews(board, load_reviews(reviews_path or default_reviews(out_path)))
    write_board(board, out_path)
    return board


# Owner review: approve or return the whole cut, scenes, lanes or segments against exact sources.

VERDICTS = {"approve", "return"}


def default_reviews(out_path: Path) -> Path:
    return out_path.parent / "board-reviews.jsonl"


def load_reviews(path: Path) -> list[dict]:
    if not path.is_file():
        return []
    entries, previous = [], None
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        entry = json.loads(line)
        body = {k: v for k, v in entry.items() if k != "entry_hash"}
        if entry.get("previous_hash") != previous or sha256_json(body) != entry.get("entry_hash"):
            raise ValueError(f"{path}:{number} breaks the review hash chain")
        previous = entry["entry_hash"]
        entries.append(entry)
    return entries


def resolve_scope(rows: list[dict], scope: str) -> list[str]:
    """`all`, or a comma list of scenes (S13, S22-S24), lanes (lane:presenter) and segments (seg044)."""
    chosen: list[str] = []
    for part in [p.strip() for p in scope.split(",") if p.strip()]:
        if part == "all":
            match = rows
        elif part.startswith("lane:"):
            match = [r for r in rows if r["lane"] == part[5:]]
        elif re.fullmatch(r"S\d\d-S\d\d", part):
            low, high = (int(x[1:]) for x in part.split("-"))
            match = [r for r in rows if low <= int(r["scene"][1:]) <= high]
        elif re.fullmatch(r"S\d\d", part):
            match = [r for r in rows if r["scene"] == part]
        else:
            match = [r for r in rows if r["id"] == part]
        if not match:
            raise ValueError(f"scope part matches no segment: {part}")
        chosen += [r["id"] for r in match if r["id"] not in chosen]
    if not chosen:
        raise ValueError("empty scope")
    return chosen


def apply_reviews(board: dict, reviews: list[dict]) -> None:
    latest: dict[str, tuple[dict, list]] = {}
    for entry in reviews:
        for row in entry["rows"]:
            latest[row["id"]] = (entry, row["sources"])
    for row in board["rows"]:
        found = latest.get(row["id"])
        if not found:
            row["review"] = None
            continue
        entry, sources = found
        same = sources == row["sources"]
        state = {("approve", True): "approved", ("approve", False): "changed",
                 ("return", True): "returned", ("return", False): "revised"}[(entry["verdict"], same)]
        row["review"] = {"state": state, "verdict": entry["verdict"], "note": entry.get("note", ""),
                         "by": entry["by"], "at": entry["at"], "board": entry["board"]["build_version"]}


def read_page_board(page: Path) -> dict:
    match = re.search(r'<script id="board" type="application/json">(.*?)</script>', page.read_text(encoding="utf-8"), re.S)
    if not match:
        raise ValueError(f"{page} is not a review board page")
    return json.loads(match.group(1).replace("<\\/", "</"))


def record_review(page: Path, verdict: str, scope: str, by: str, note: str, verbatim: str,
                  reviews_path: Path | None = None) -> dict:
    """Append one owner review bound to the exact sources on the board, then refresh the page."""
    if verdict not in VERDICTS:
        raise ValueError(f"verdict must be one of {sorted(VERDICTS)}")
    if verdict == "return" and not note.strip():
        raise ValueError("a return needs a note saying what to change")
    board = read_page_board(page)
    path = reviews_path or default_reviews(page)
    reviews = load_reviews(path)
    ids = resolve_scope(board["rows"], scope)
    by_id = {r["id"]: r for r in board["rows"]}
    entry = {
        "record_type": "board_review",
        "at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "verdict": verdict,
        "scope": scope,
        "by": by,
        "note": note,
        "verbatim": verbatim,
        "board": {"page": _rel(page), "digest": board["digest"], "build_version": board.get("build_version", "")},
        "rows": [{"id": i, "sources": by_id[i]["sources"]} for i in ids],
        "previous_hash": reviews[-1]["entry_hash"] if reviews else None,
    }
    entry["entry_hash"] = sha256_json(entry)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry, ensure_ascii=False, sort_keys=True) + "\n")
    apply_reviews(board, reviews + [entry])
    write_board(board, page)
    return entry


def check_approved(page: Path, scope: str = "all", reviews_path: Path | None = None) -> list[dict]:
    """Rows in scope that are not approved against their current sources. Empty means the gate passes."""
    board = read_page_board(page)
    apply_reviews(board, load_reviews(reviews_path or default_reviews(page)))
    wanted = set(resolve_scope(board["rows"], scope))
    return [
        {"id": r["id"], "scene": r["scene"], "review": (r["review"] or {}).get("state", "not reviewed")}
        for r in board["rows"]
        if r["id"] in wanted and (r["review"] or {}).get("state") != "approved"
    ]


def thumb_time(row: dict) -> float:
    return min(row["end"] - 0.05, row["start"] + min(1.5, (row["end"] - row["start"]) / 2))


def write_thumbs(board: dict, video: Path, out_path: Path) -> int:
    """One small JPEG per segment, so phones get thumbnails without decoding the cut in the page."""
    ffmpeg = os.environ.get("OE_FFMPEG") or shutil.which("ffmpeg")
    if not ffmpeg or not video.is_file():
        return 0
    folder = out_path.with_name(out_path.stem + "-thumbs")
    folder.mkdir(parents=True, exist_ok=True)
    made = 0
    for row in board["rows"]:
        target = folder / f"{row['id']}.jpg"
        result = subprocess.run(
            [ffmpeg, "-nostdin", "-v", "error", "-y", "-ss", f"{thumb_time(row):.3f}", "-i", str(video),
             "-frames:v", "1", "-vf", "scale=320:-2", "-q:v", "5", str(target)],
            check=False,
        )
        if result.returncode == 0 and target.is_file():
            row["thumb"] = f"{folder.name}/{target.name}"
            made += 1
    return made


def write_board(board: dict, out_path: Path) -> None:
    payload = json.dumps(board, ensure_ascii=False).replace("</", "<\\/")
    page = TEMPLATE.read_text(encoding="utf-8")
    page = page.replace("__TITLE__", html.escape(board["title"])).replace("__BOARD_JSON__", payload)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(page, encoding="utf-8")
    record = {k: v for k, v in board.items() if k not in {"rows", "scenes"}}
    record["page"] = {"path": out_path.name, "sha256": sha256_file(out_path)}
    record["rows"] = [
        {"id": r["id"], "scene": r["scene"], "lane": r["lane"], "frames": r["frames"], "state": r["state"],
         "review": (r.get("review") or {}).get("state"), "sources": r["sources"]}
        for r in board["rows"]
    ]
    out_path.with_suffix(".json").write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
