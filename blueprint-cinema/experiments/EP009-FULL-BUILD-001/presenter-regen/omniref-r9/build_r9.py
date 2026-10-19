#!/usr/bin/env python3
"""Build the EP009 r9 review cut: r6 with every finished OmniHuman-reference presenter take laid over its slice.

Second halves of split segments (seg019b, seg071b) are framed about 12% tighter so the join reads as a cut.

Picture: the r6 review cut, with each react1-r7 final (and the approved P08a take) placed at its
exact master frames. Sound: the locked r3 narration master, unchanged. Segments without a finished
take keep their r6 picture and stay listed in `held`. Writes the cut, a BUILD.json the board reads,
and the ffmpeg graph.
"""
import copy, hashlib, json, subprocess
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
EP = HERE.parents[1]
REPO = EP.parents[2]
R6 = EP / "assembly/r6-software-demo/ep009-r6-software-demo-review-r1-BUILD.json"
OUT_DIR = EP / "assembly/r9-omniref-presenters"
OUT = EP / "assembly/qa/r9-omniref-presenters/ep009-r9-omniref-presenters-review-r1.mp4"
PUNCH_IN = {"seg019b", "seg071b"}


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def rel(p):
    return str(Path(p).resolve().relative_to(REPO))


def conform(src, dst):
    if not dst.exists():
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-an", "-c:v", "libx264", "-profile:v", "high", "-pix_fmt", "yuv420p",
                        "-r", "24", "-crf", "14", "-preset", "slow", "-movflags", "+faststart", dst], check=True)
    return dst


r6 = json.load(open(R6))
takes = json.load(open(HERE / "TAKES.json"))["takes"]
placed, held = [], []
for t in takes:
    if True:
        rec_path = HERE / t["take"] / "TAKE.json"
        rec = json.load(open(rec_path)) if rec_path.exists() else {}
        if not rec.get("final", {}).get("frames_match"):
            held.append(t["take"]); continue
        final = REPO / rec["final"]["path"]
    frames = int(json.loads(subprocess.run(["ffprobe", "-v", "error", "-count_packets", "-show_entries", "stream=nb_read_packets", "-of", "json", str(final)],
                                           capture_output=True, text=True, check=True).stdout)["streams"][0]["nb_read_packets"])
    a0, a1 = t["master_frames"]
    assert frames >= a1 - a0, (t["take"], frames, a1 - a0)
    placed.append({"take": t["take"], "segment": t["segment"], "output_frames": [a0, a1], "path": final, "sha256": sha(final), "punch_in": t["take"] in PUNCH_IN})

base = EP / r6["output"].split("EP009-FULL-BUILD-001/")[1]
master = REPO / r6["master"]["path"]
inputs = ["-i", str(base), "-i", str(master)]
chain, last = [], "[0:v]"
for i, p in enumerate(placed, start=2):
    a0, a1 = p["output_frames"]
    inputs += ["-i", str(p["path"])]
    tighten = "crop=1714:964:103:60," if p["punch_in"] else ""
    chain.append(f"[{i}:v]trim=end_frame={a1 - a0},{tighten}scale=1280:720:flags=lanczos,setsar=1,setpts=PTS-STARTPTS+{a0}/(24*TB)[p{i}]")
    chain.append(f"{last}[p{i}]overlay=eof_action=pass:enable='between(n,{a0},{a1 - 1})'[v{i}]")
    last = f"[v{i}]"
graph = ";".join(chain) or "[0:v]null[vout]"
if chain:
    graph += f";{last}null[vout]"
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT_DIR.mkdir(parents=True, exist_ok=True)
(OUT_DIR / "ep009-r9-omniref-presenters-review-r1-graph.txt").write_text(graph)
cmd = ["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", graph, "-map", "[vout]", "-map", "1:a",
       "-c:v", "libx264", "-profile:v", "high", "-pix_fmt", "yuv420p", "-r", "24", "-crf", "18", "-preset", "medium",
       "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(OUT)]
subprocess.run(cmd, check=True)

build = copy.deepcopy(r6)
by_seg = {}
for p in placed:
    by_seg.setdefault(p["segment"], []).append(p)
for row in build["all_75_rows"]:
    if row["id"] not in by_seg:
        continue
    new = [{"kind": "video", "source": {"path": rel(p["path"]), "sha256": p["sha256"]}, "source_start_frame": 0,
            "output_frames": p["output_frames"], "frames": p["output_frames"][1] - p["output_frames"][0],
            "react1_take": p["take"]} for p in by_seg[row["id"]]]
    covered = sum(s["frames"] for s in new)
    if covered < row["frames"]:  # a split segment with one part still held keeps its r6 span underneath
        new = row.get("spans", []) + new
    row["spans"] = new
build.update({
    "record_type": "ep009_r9_omniref_presenters_review_build", "status": "encoded_unverified_review_only",
    "version": "r9-omniref-presenters", "at": datetime.now(timezone.utc).isoformat(),
    "base_build": {"path": rel(R6), "sha256": sha(R6)},
    "presenter_route": "presenter-regen/omniref-r9: Seedance 2.5 with K01 + an OmniHuman 1.5 take of the same line as body-language reference, r8 face wording, then fal react-1 lips/neutral/0.5; seg021 is the owner-approved test take; seg019b and seg071b framed ~12% tighter",
    "placed": [{**p, "path": rel(p["path"])} for p in placed], "held": held,
    "owner_accepted": False, "release_cleared": False,
    "limits": ["Private review revision; no publication or owner acceptance inferred.",
               "Picture is the r6 review encode with presenter takes overlaid at their master frames; the locked r3 narration master is the only audio.",
               "Held takes keep their r6 picture: " + (", ".join(held) or "none")],
    "builder": {"path": rel(__file__), "sha256": sha(__file__)},
    "graph": {"path": rel(OUT_DIR / "ep009-r9-omniref-presenters-review-r1-graph.txt"), "sha256": sha(OUT_DIR / "ep009-r9-omniref-presenters-review-r1-graph.txt")},
    "command": cmd, "output": rel(OUT), "output_sha256": sha(OUT),
})
for k in ("source_spans", "render_groups", "sources", "inserts", "mapping_checks", "encode_log", "encode_exit_code", "graph_helper"):
    build.pop(k, None)
json.dump(build, open(OUT_DIR / "ep009-r9-omniref-presenters-review-r1-BUILD.json", "w"), indent=1)
print("placed", len(placed), "held", held, "->", rel(OUT))
