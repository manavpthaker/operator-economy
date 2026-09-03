#!/usr/bin/env python3
"""N5 narration edit and N6 technical pass for a captured V2 episode.

N5 `assemble`  gain-normalise every accepted transfer chunk to one target,
               insert the silent identity sting after the cold open and
               performance-derived room at every other join, concatenate into
               one 48 kHz / 16-bit / mono master, and write the edit decision
               list and spacing decisions. No sample inside a spoken word is
               touched; only gain and inserted silence.

N6 `align`     bind the exact master to the locked `W` transport with
               ElevenLabs forced alignment, write the word transcript and the
               intentional-pause map, run the completeness contract (tail
               energy per chunk, chunk-final word duration vs half the median),
               and write a technical-qc draft plus the state update.

ffmpeg does the measurement and the sample work; Python only decides.

Usage:
  finish_n5n6.py assemble --episode-dir DIR [--target-dbfs -22.0] [--sting 4.0]
                          [--scene-gap 0.62] [--split-gap 0.46] [--source transfer|guide] [--out-dir DIR]
  finish_n5n6.py align    --episode-dir DIR [--execute]
"""

from __future__ import annotations

import argparse
import array
import hashlib
import json
import math
import os
import pathlib
import re
import statistics
import subprocess
import sys
import wave

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import calibrate as cal  # noqa: E402

REPO = pathlib.Path(__file__).resolve().parents[3]
SILENCE_FS = 0.004          # window RMS below this fraction of full scale is silence (about -48 dBFS)
EDGE_WINDOW_MS = 10
PAUSE_THRESHOLD_S = 0.30


def sha(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(cmd: list[str]) -> str:
    return subprocess.run(cmd, capture_output=True, text=True, check=True).stdout + subprocess.run(cmd, capture_output=True, text=True).stderr


def ff(cmd: list[str]) -> str:
    p = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-y", *cmd], capture_output=True, text=True)
    if p.returncode != 0:
        sys.exit(f"ffmpeg failed: {' '.join(cmd)}\n{p.stderr[-2000:]}")
    return p.stderr


def rms_dbfs(path: pathlib.Path) -> float:
    err = ff(["-i", str(path), "-af", "astats=measure_overall=RMS_level:measure_perchannel=none", "-f", "null", "-"])
    m = re.findall(r"RMS level dB:\s*(-?[0-9.]+|-inf)", err)
    if not m:
        sys.exit(f"could not measure RMS for {path}")
    return float(m[-1]) if m[-1] != "-inf" else -120.0


def peak_dbfs(path: pathlib.Path) -> float:
    err = ff(["-i", str(path), "-af", "astats=measure_overall=Peak_level:measure_perchannel=none", "-f", "null", "-"])
    m = re.findall(r"Peak level dB:\s*(-?[0-9.]+|-inf)", err)
    return float(m[-1]) if m and m[-1] != "-inf" else -120.0


def wav_info(path: pathlib.Path) -> dict:
    with wave.open(str(path)) as w:
        return {"rate": w.getframerate(), "channels": w.getnchannels(), "width": w.getsampwidth(),
                "frames": w.getnframes(), "duration": w.getnframes() / w.getframerate()}


def edge_silence(path: pathlib.Path, seconds: float = 4.0) -> tuple[float, float]:
    """Leading and trailing silence in seconds, scanning only the edges."""
    with wave.open(str(path)) as w:
        rate, n = w.getframerate(), w.getnframes()
        k = min(n, int(rate * seconds))
        head = array.array("h"); head.frombytes(w.readframes(k))
        w.setpos(max(0, n - k))
        tail = array.array("h"); tail.frombytes(w.readframes(k))
    step = rate * EDGE_WINDOW_MS // 1000
    thr = SILENCE_FS * 32768

    def rms(seg):
        return math.sqrt(sum(v * v for v in seg) / max(1, len(seg)))

    lead = 0
    for i in range(0, len(head) - step, step):
        if rms(head[i:i + step]) > thr:
            break
        lead += step
    trail = 0
    for i in range(len(tail) - step, 0, -step):
        if rms(tail[i:i + step]) > thr:
            break
        trail += step
    return lead / rate, trail / rate


# --- N5 ------------------------------------------------------------------------

def assemble(args) -> int:
    ep_dir = pathlib.Path(args.episode_dir).resolve()
    episode = ep_dir.name.split("-")[0]
    nd = ep_dir / "02-narration-production"
    reg = json.loads((nd / "take-register.json").read_text())
    key = "transfer" if args.source == "transfer" else "guide"
    chunks = [c for c in reg["chunks"] if key in c]
    if len(chunks) != len(reg["chunks"]):
        print(f"warning: {len(reg['chunks']) - len(chunks)} chunks have no accepted {key}; assembling what exists")
    if not chunks:
        sys.exit("nothing to assemble")
    out_root = pathlib.Path(args.out_dir).resolve() if args.out_dir else nd
    selects = out_root / "selects"; master_dir = out_root / "master"
    selects.mkdir(parents=True, exist_ok=True); master_dir.mkdir(parents=True, exist_ok=True)

    print(f"[{episode}] N5 assemble from {key} files: {len(chunks)} chunks")
    levels = {c["chunk"]: rms_dbfs(REPO / c[key]["path"]) for c in chunks}
    target = args.target_dbfs
    spread_before = max(levels.values()) - min(levels.values())

    joins, edl_chunks, listfile = [], [], []
    t_cursor = 0.0
    for idx, c in enumerate(chunks):
        src = REPO / c[key]["path"]
        gain = target - levels[c["chunk"]]
        lead, trail = edge_silence(src)
        nxt = chunks[idx + 1] if idx + 1 < len(chunks) else None
        inserted = 0.0
        kind = "end"
        if nxt:
            nlead, _ = edge_silence(REPO / nxt[key]["path"])
            existing = trail + nlead
            first_scene_out = c["scenes"].split("+")[-1]
            first_scene_in = nxt["scenes"].split("+")[0]
            if c["scenes"].split("+")[0] == "S00":
                kind, tgt = "silent identity sting (S01)", args.sting
            elif re.sub(r"\.\d+$", "", first_scene_out) == re.sub(r"\.\d+$", "", first_scene_in):
                kind, tgt = "within-scene split", args.split_gap
            else:
                kind, tgt = "scene boundary", args.scene_gap
            inserted = max(0.0, round(tgt - existing, 3))
            joins.append({"join": idx + 1, "from": c["scenes"], "to": nxt["scenes"], "kind": kind,
                          "existing_s": round(existing, 3), "target_s": tgt, "inserted_s": inserted})
        out = selects / f"c{c['chunk']:02d}.{key}.norm.wav"
        af = f"volume={gain:.3f}dB"
        if inserted > 0:
            af += f",apad=pad_dur={inserted}"
        ff(["-i", str(src), "-af", af, "-ar", "48000", "-ac", "1", "-sample_fmt", "s16", str(out)])
        info = wav_info(out)
        edl_chunks.append({"chunk": c["chunk"], "scenes": c["scenes"], "source": c[key]["path"], "source_sha256": c[key]["sha256"],
                           "rms_dbfs_before": round(levels[c["chunk"]], 2), "gain_db": round(gain, 2),
                           "lead_silence_s": round(lead, 3), "trail_silence_s": round(trail, 3),
                           "inserted_after_s": inserted, "master_start_s": round(t_cursor, 3),
                           "master_end_s": round(t_cursor + info["duration"], 3), "select": str(out.relative_to(REPO)) if out.is_relative_to(REPO) else str(out)})
        t_cursor += info["duration"]
        listfile.append(f"file '{out}'")
        print(f"  c{c['chunk']:02d} {c['scenes']:<20} {levels[c['chunk']]:7.2f} dBFS  gain {gain:+6.2f}  {kind:<28} +{inserted:.2f}s")

    lst = master_dir / "concat.txt"; lst.write_text("\n".join(listfile) + "\n")
    master = master_dir / "narration-master.wav"
    ff(["-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(master)])
    lst.unlink()
    minfo = wav_info(master)
    after = [rms_dbfs(selects / f"c{c['chunk']:02d}.{key}.norm.wav") for c in chunks]
    spread_after = max(after) - min(after)
    m_rms, m_peak = rms_dbfs(master), peak_dbfs(master)
    msha = sha(master)
    edl = {"schema": "oe-narration-edl-v1", "episode": episode, "source_stage": key,
           "operations": ["gain normalisation", "scene spacing", "identity sting room", "concatenation"],
           "target_dbfs": target, "spread_before_db": round(spread_before, 2), "spread_after_db": round(spread_after, 2),
           "sting_seconds": args.sting, "scene_boundary_target_s": args.scene_gap, "within_scene_target_s": args.split_gap,
           "total_inserted_s": round(sum(j["inserted_s"] for j in joins), 2),
           "master": {"path": str(master.relative_to(REPO)) if master.is_relative_to(REPO) else str(master), "sha256": msha,
                      "duration_seconds": round(minfo["duration"], 3), "rate": minfo["rate"], "channels": minfo["channels"],
                      "bits": minfo["width"] * 8, "integrated_rms_dbfs": round(m_rms, 2), "peak_dbfs": round(m_peak, 2)},
           "chunks": edl_chunks, "joins": joins,
           "note": "No spoken word was added, removed, reordered or rewritten. Only gain and inserted silence."}
    (out_root / "narration-edit-decision-list.json").write_text(json.dumps(edl, indent=2) + "\n")
    (out_root / "narration-spacing-decisions.json").write_text(json.dumps({
        "episode": episode, "operation": "scene-boundary and identity-sting spacing",
        "rationale": "Chunks are independent generations, so join gaps carry no performed room. Targets follow EP007's measured pause distribution for this narrator configuration (median pause 0.62s at a scene boundary, lower quartile 0.46s inside a split scene) and the beat sheet's silent identity sting; recompute from this master's own pause map after alignment if it differs materially.",
        "sting_seconds": args.sting, "scene_boundary_target_s": args.scene_gap, "within_scene_target_s": args.split_gap,
        "total_inserted_s": edl["total_inserted_s"], "joins": joins}, indent=2) + "\n")
    print(f"  master {master.name}: {minfo['duration']/60:.1f} min, RMS {m_rms:.2f} dBFS, peak {m_peak:.2f} dBFS, spread {spread_before:.1f} -> {spread_after:.1f} dB, sha {msha[:12]}")
    if args.out_dir is None:
        st = nd / "narration-state.json"
        if st.is_file():
            s = json.loads(st.read_text()); s["gates"]["N5"] = {"result": "edited", "record": "narration-edit-decision-list.json", "master_sha256": msha}
            s["master"] = edl["master"]; st.write_text(json.dumps(s, indent=2) + "\n")
    return 0


# --- N6 ------------------------------------------------------------------------

def forced_align(master: pathlib.Path, text: str, api_key: str) -> dict:
    fields = {"text": text}
    body, ctype = cal.multipart(fields, master.name, master.read_bytes())
    status, payload = cal.post("https://api.elevenlabs.io/v1/forced-alignment", body,
                               {"xi-api-key": api_key, "Content-Type": ctype, "Accept": "application/json"})
    if status != 200:
        sys.exit(f"forced alignment HTTP {status}: {payload[:400].decode('utf-8', 'replace')}")
    return json.loads(payload)


def align(args) -> int:
    ep_dir = pathlib.Path(args.episode_dir).resolve()
    episode = ep_dir.name.split("-")[0]
    nd = ep_dir / "02-narration-production"; ed = ep_dir / "01-editorial"
    edl = json.loads((nd / "narration-edit-decision-list.json").read_text())
    master = REPO / edl["master"]["path"]
    msha = sha(master)
    if msha != edl["master"]["sha256"]:
        sys.exit("master hash differs from the edit decision list; re-run assemble")
    w = (ed / "canonical-w.txt").read_text(encoding="utf-8").split("\n")
    if w and w[-1] == "":
        w.pop()
    wsha = sha(ed / "canonical-w.txt")
    text = " ".join(w)
    print(f"[{episode}] N6 align master {msha[:12]} ({edl['master']['duration_seconds']}s) to W {wsha[:12]} ({len(w)} tokens)")
    if not args.execute:
        print("  DRY RUN - no provider call. Re-run with --execute.")
        return 0
    resp = forced_align(master, text, cal.read_dotenv_key("ELEVENLABS_API_KEY"))
    words = resp.get("words") or []
    aligned = [x for x in words if x.get("text", "").strip()]
    # bind sequentially; tolerate provider tokenisation that merges or splits on punctuation
    out, wi, mism = [], 0, 0
    norm = lambda s: re.sub(r"[^a-z0-9]", "", s.lower())
    for a in aligned:
        if wi >= len(w):
            break
        if norm(a["text"]) == norm(w[wi]) or not norm(a["text"]):
            out.append({"w_id": f"W{wi:06d}", "token": w[wi], "start": round(a["start"], 3), "end": round(a["end"], 3)})
            wi += 1
        else:
            # try merging with following provider words until it matches this token
            merged, j = a["text"], aligned.index(a)
            matched = False
            for k in range(j + 1, min(j + 4, len(aligned))):
                merged += aligned[k]["text"]
                if norm(merged) == norm(w[wi]):
                    out.append({"w_id": f"W{wi:06d}", "token": w[wi], "start": round(a["start"], 3), "end": round(aligned[k]["end"], 3)})
                    wi += 1; matched = True
                    for skip in aligned[j + 1:k + 1]:
                        skip["text"] = ""
                    break
            if not matched:
                mism += 1
                out.append({"w_id": f"W{wi:06d}", "token": w[wi], "start": round(a["start"], 3), "end": round(a["end"], 3), "provider_text": a["text"], "mismatch": True})
                wi += 1
    unresolved = mism + (len(w) - wi)
    durations = [x["end"] - x["start"] for x in out if x["end"] > x["start"]]
    median = statistics.median(durations) if durations else 0.0
    # completeness per chunk: final word inside each chunk's master window
    short_finals, mid_sound = [], []
    for c in edl["chunks"]:
        inside = [x for x in out if c["master_start_s"] <= x["start"] < c["master_end_s"] - c["inserted_after_s"]]
        if inside:
            last = inside[-1]
            if last["end"] - last["start"] < median / 2:
                short_finals.append({"chunk": c["chunk"], "token": last["token"], "duration": round(last["end"] - last["start"], 3)})
        te = cal.tail_energy(REPO / c["source"])
        if te >= cal.TAIL_ENERGY_THRESHOLD:
            mid_sound.append({"chunk": c["chunk"], "tail_energy": round(te, 4)})
    pauses = []
    for a, b in zip(out, out[1:]):
        gap = b["start"] - a["end"]
        if gap >= PAUSE_THRESHOLD_S:
            pauses.append({"after_w_id": a["w_id"], "start": a["end"], "end": b["start"], "duration": round(gap, 3)})
    transcript = {"schema": "oe-word-transcript-v1", "episode": episode, "master_path": edl["master"]["path"], "master_sha256": msha,
                  "master_duration_seconds": edl["master"]["duration_seconds"], "canonical_w_sha256": wsha, "w_token_count": len(w),
                  "aligned_word_count": len(out), "unresolved_mismatches": unresolved,
                  "alignment_method": "elevenlabs forced-alignment against the locked W transport", "alignment_loss": resp.get("loss"),
                  "completeness_check": {"detector": "tail energy per chunk plus chunk-final word duration",
                                         "chunks_ending_mid_sound": len(mid_sound), "chunk_final_words_below_half_median": len(short_finals),
                                         "median_word_s": round(median, 3), "details": {"mid_sound": mid_sound, "short_finals": short_finals}},
                  "words": out}
    (nd / "word-transcript.json").write_text(json.dumps(transcript, indent=1) + "\n")
    pm = {"schema": "oe-intentional-pause-map-v1", "episode": episode, "master_sha256": msha, "master_duration_seconds": edl["master"]["duration_seconds"],
          "threshold_seconds": PAUSE_THRESHOLD_S, "pause_count": len(pauses), "total_pause_seconds": round(sum(p["duration"] for p in pauses), 2), "pauses": pauses}
    (nd / "intentional-pause-map.json").write_text(json.dumps(pm, indent=1) + "\n")
    passed = unresolved == 0 and not short_finals and not mid_sound and len(out) == len(w)
    tsha, psha = sha(nd / "word-transcript.json"), sha(nd / "intentional-pause-map.json")
    st = nd / "narration-state.json"
    s = json.loads(st.read_text()) if st.is_file() else {}
    s["gates"] = s.get("gates", {}); s["gates"]["N6"] = {"result": "technical_pass" if passed else "failed", "master_sha256": msha}
    s["technical_pass"] = passed; s["transcript"] = {"path": "word-transcript.json", "sha256": tsha}
    s["intentional_pause_map"] = {"path": "intentional-pause-map.json", "sha256": psha}
    st.write_text(json.dumps(s, indent=2) + "\n")
    print(f"  aligned {len(out)}/{len(w)}, unresolved {unresolved}, loss {resp.get('loss')}, median word {median:.3f}s")
    print(f"  completeness: mid-sound chunks {len(mid_sound)}, short finals {len(short_finals)}; pauses {len(pauses)} ({pm['total_pause_seconds']}s)")
    print(f"  N6: {'technical_pass' if passed else 'FAILED, see word-transcript.json completeness_check'}")
    return 0 if passed else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("assemble"); a.add_argument("--episode-dir", required=True)
    a.add_argument("--target-dbfs", type=float, default=-22.0); a.add_argument("--sting", type=float, default=4.0)
    a.add_argument("--scene-gap", type=float, default=0.62); a.add_argument("--split-gap", type=float, default=0.46)
    a.add_argument("--source", choices=("transfer", "guide"), default="transfer"); a.add_argument("--out-dir", default=None)
    b = sub.add_parser("align"); b.add_argument("--episode-dir", required=True); b.add_argument("--execute", action="store_true")
    args = ap.parse_args()
    return assemble(args) if args.cmd == "assemble" else align(args)


if __name__ == "__main__":
    raise SystemExit(main())
