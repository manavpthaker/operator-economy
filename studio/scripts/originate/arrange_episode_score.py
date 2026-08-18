"""Arrange a selected Rev D episode score against storyboard score states."""
from __future__ import annotations

import argparse
import json
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

SOURCE_OFFSETS = {
    "human": 0.0,
    "constraint": 0.0,
    "tension": 18.0,
    "counter": 96.0,
    "build": 108.0,
    "agency": 118.0,
    "resolution": 138.0,
    "resolve": 138.0,
    "calm": 0.0,
}


def run(command: list[str]) -> None:
    subprocess.run(command, check=True)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("script")
    ap.add_argument("--output", default=str(ROOT / "remotion" / "public" / "music" / "bed.mp3"))
    args = ap.parse_args()
    episode = Path(args.script).resolve().parent
    brief = json.loads((episode / "music_brief.json").read_text())
    selected = brief.get("selected_candidate")
    candidate = next((c for c in brief.get("candidates", []) if c["title"] == selected), None)
    if brief.get("status") not in {"candidate_selected", "approved", "arranged"} or not candidate:
        raise SystemExit("MUSIC GATE: select a candidate before arranging")
    source = ROOT / candidate["local_source"]
    if not source.is_file():
        raise SystemExit(f"Selected source not found: {source}")
    storyboard = json.loads((episode / "storyboard.json").read_text())
    screens = storyboard["screens"]
    spans: list[dict] = []
    for screen in screens:
        state = (screen.get("music") or {}).get("intensity") or screen.get("score_state", "human")
        start, end = float(screen["start"]), float(screen["end"])
        if spans and spans[-1]["state"] == state and abs(spans[-1]["end"] - start) < .02:
            spans[-1]["end"] = end
        else:
            spans.append({"state": state, "start": start, "end": end})

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="oe-score-") as temp_raw:
        temp = Path(temp_raw)
        pieces = []
        for index, span in enumerate(spans):
            duration = span["end"] - span["start"]
            piece = temp / f"{index:03d}-{span['state']}.wav"
            if span["state"] == "silence":
                run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo",
                     "-t", f"{duration:.3f}", "-c:a", "pcm_s16le", str(piece)])
            else:
                offset = SOURCE_OFFSETS.get(span["state"], 0.0)
                fade = min(.45, duration / 4)
                run(["ffmpeg", "-y", "-loglevel", "error", "-stream_loop", "-1", "-ss", str(offset), "-i", str(source),
                     "-t", f"{duration:.3f}", "-af", f"atrim=duration={duration:.3f},asetpts=N/SR/TB,highpass=f=95,equalizer=f=160:t=q:w=0.8:g=-5,equalizer=f=4200:t=q:w=0.7:g=2,afade=t=in:st=0:d={fade},afade=t=out:st={max(0,duration-fade):.3f}:d={fade}",
                     "-ar", "48000", "-ac", "2", "-c:a", "pcm_s16le", str(piece)])
            pieces.append(piece)
        concat = temp / "concat.txt"
        concat.write_text("".join(f"file '{piece}'\n" for piece in pieces))
        premaster = temp / "premaster.wav"
        total = float(storyboard["total_seconds"])
        run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(concat),
             "-t", f"{total:.3f}", "-af", f"atrim=duration={total:.3f},asetpts=N/SR/TB,loudnorm=I=-18:TP=-2:LRA=10",
             "-ar", "48000", "-ac", "2", str(premaster)])
        run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(premaster), "-codec:a", "libmp3lame", "-b:a", "256k", str(output)])
    arrangement = {"selected_candidate": selected, "source": candidate["local_source"],
                   "duration_seconds": storyboard["total_seconds"], "output": str(output.relative_to(ROOT)), "spans": spans}
    (episode / "music_arrangement.json").write_text(json.dumps(arrangement, indent=2) + "\n")
    brief["status"] = "arranged"
    brief["arrangement"] = "music_arrangement.json"
    (episode / "music_brief.json").write_text(json.dumps(brief, indent=2) + "\n")
    print(f"Score arrangement → {output} ({len(spans)} state spans)")


if __name__ == "__main__":
    main()
