#!/usr/bin/env python3
"""Mechanical verification of the four delivered SHORTS-004 MP4s.

Checks, per Short:
  1. exact frame count, canvas and frame rate against the source contract
  2. audio correlation of every beat against the locked narration master, at the
     declared master frame range (zero-lag normalised cross-correlation)
  3. no uniform frame anywhere in the render (per-frame luma spread
     YMAX - YMIN via one ffprobe signalstats pass)
  4. the locked sources are still byte-identical

What this cannot judge is recorded, not implied: perceptual lip sync, whether a
cold viewer finds the payoff useful, and physical-phone playback.
"""
from pathlib import Path
import json
import subprocess
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import oe_shorts_r4 as L  # noqa: E402

P = Path(__file__).resolve().parent
SHORTS = ["01-second-commission", "02-cheap-tools",
          "03-guest-relationship", "04-wrong-number"]


def beats_of(contract: dict) -> list[dict]:
    raw = contract.get("edl") or contract.get("segments") or contract.get("edits") or []
    out = []
    for b in raw:
        out.append({
            "id": str(b.get("id")),
            "master_in": b["source_in_frame"],
            "master_out": b["source_out_frame_exclusive"],
            "timeline_in": b["timeline_in_frame"],
        })
    if "audio" in contract:
        lo, hi = contract["audio"]["frames"]
        out.append({"id": "whole_take", "master_in": lo, "master_out": hi,
                    "timeline_in": 0})
        if "answer_beat" in contract:
            a = contract["answer_beat"]
            out.append({"id": "answer", "master_in": a["master_frames"][0],
                        "master_out": a["master_frames"][1],
                        "timeline_in": a["timeline_frames"][0]})
        presenter = contract.get("presenter_sources") or []
        for src in presenter:
            if "global_frames" in src and "timeline_frames" in src:
                out.append({"id": src.get("id", "presenter"),
                            "master_in": src["global_frames"][0],
                            "master_out": src["global_frames"][1],
                            "timeline_in": src["timeline_frames"][0]})
    return out


def probe(video: Path) -> dict:
    data = json.loads(subprocess.check_output([
        "ffprobe", "-v", "error", "-select_streams", "v:0", "-count_frames",
        "-show_entries", "stream=nb_read_frames,width,height,r_frame_rate",
        "-of", "json", str(video)]))["streams"][0]
    audio = json.loads(subprocess.check_output([
        "ffprobe", "-v", "error", "-select_streams", "a:0",
        "-show_entries", "stream=codec_name,sample_rate,channels",
        "-of", "json", str(video)]))["streams"][0]
    return {"frame_count": int(data["nb_read_frames"]),
            "width": int(data["width"]), "height": int(data["height"]),
            "r_frame_rate": data["r_frame_rate"], "audio": audio}


def uniform_frames(video: Path) -> dict:
    """Per-frame luma spread (YMAX - YMIN) for every encoded frame.

    A frame rendered as one flat colour has spread 0. Paired YMIN/YMAX are read
    from a single signalstats pass so the two series cannot drift apart.
    """
    rows = subprocess.check_output([
        "ffprobe", "-v", "error", "-f", "lavfi",
        "-i", f"movie={video},signalstats",
        "-show_entries", "frame_tags=lavfi.signalstats.YMIN,lavfi.signalstats.YMAX",
        "-of", "csv=p=0"], text=True).strip().splitlines()
    spreads = []
    for row in rows:
        parts = row.split(",")
        if len(parts) < 2:
            continue
        spreads.append(int(parts[1]) - int(parts[0]))
    flat = [i for i, sp in enumerate(spreads) if sp <= 1]
    return {"frames_measured": len(spreads),
            "min_luma_spread": min(spreads) if spreads else None,
            "uniform_frame_indices": flat,
            "uniform_frames": len(flat),
            "threshold": "spread <= 1 counts as uniform"}


def main() -> None:
    report = {
        "revision": "EP009-SHORTS-004",
        "method": "ffprobe frame count with -count_frames; per-beat zero-lag normalised "
                  "cross-correlation of the rendered audio against the locked narration "
                  "master at the declared master sample range (decimated 1:7); per-frame "
                  "luma spread YMAX - YMIN via one ffprobe signalstats pass; sha256 of the "
                  "locked sources.",
        "not_judged": [
            "Perceptual lip sync. The picture slices are the accepted r3 native frames "
            "and no retime was applied, but no automatic check proves mouth-to-audio "
            "agreement; a human must watch each Short with sound.",
            "Whether a cold viewer actually finds each payoff useful. The contract "
            "validator checks declared fields, not comprehension.",
            "Physical-phone playback. Playback was verified in a browser at 390x844.",
            "Short 03's answer beat carries a designed card rather than presenter "
            "picture, so lip sync is not applicable for timeline frames 334..380.",
        ],
        "locked_sources": [{"path": str(p.relative_to(L.REPO)), "sha256": L.sha(p),
                            "expected": d, "unchanged": L.sha(p) == d}
                           for p, d in L.LOCKED.items()],
        "shorts": [],
    }
    ok = True
    for slug in SHORTS:
        base = P / slug
        contract = json.loads((base / "source-contract.json").read_text())
        video = base / "review" / f"{slug}-r4.mp4"
        info = probe(video)
        entry = {
            "slug": slug,
            "video": {"path": str(video.relative_to(L.REPO)), "sha256": L.sha(video),
                      "bytes": video.stat().st_size},
            "frame_count": {"declared": contract["frame_count"],
                            "measured": info["frame_count"],
                            "match": contract["frame_count"] == info["frame_count"]},
            "canvas": {"width": info["width"], "height": info["height"],
                       "r_frame_rate": info["r_frame_rate"],
                       "match": (info["width"], info["height"], info["r_frame_rate"])
                                == (1080, 1920, "24/1")},
            "audio_stream": info["audio"],
            "beats": [],
        }
        for beat in beats_of(contract):
            frames = beat["master_out"] - beat["master_in"]
            master = L.master_samples(beat["master_in"], beat["master_out"])
            render = L.rendered_samples(video, beat["timeline_in"],
                                        beat["timeline_in"] + frames)
            r = L.correlation(master, render)
            entry["beats"].append({
                "id": beat["id"],
                "master_frames": [beat["master_in"], beat["master_out"]],
                "timeline_in_frame": beat["timeline_in"],
                "frames": frames,
                "correlation": round(r, 6),
                "pass": r >= 0.99,
            })
            ok = ok and r >= 0.99
        entry["uniform_frames"] = uniform_frames(video)
        ok = ok and entry["frame_count"]["match"] and entry["canvas"]["match"]
        ok = ok and entry["uniform_frames"]["uniform_frames"] == 0
        report["shorts"].append(entry)
    report["result"] = "pass" if ok else "fail"
    L.write_json(P / "VERIFICATION.json", report)
    print(json.dumps({
        "result": report["result"],
        "shorts": [{
            "slug": s["slug"],
            "frames": s["frame_count"],
            "canvas_ok": s["canvas"]["match"],
            "min_correlation": min(b["correlation"] for b in s["beats"]),
            "uniform_frames": s["uniform_frames"]["uniform_frames"],
            "min_luma_spread": s["uniform_frames"]["min_luma_spread"],
        } for s in report["shorts"]],
    }, indent=2))


if __name__ == "__main__":
    main()
