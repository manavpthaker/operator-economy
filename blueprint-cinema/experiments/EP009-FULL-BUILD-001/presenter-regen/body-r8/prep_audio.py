#!/usr/bin/env python3
"""Cut exact narration slices for the L3b body-movement presenter regeneration (r8).

Each returned r6 presenter segment is sliced from the r3 narration master at its
r6 output frames (2000 samples per frame; the master matches the approved P08a
slice sample for sample). Segments over 15 s split at the widest word gap near
the middle, on a frame boundary. Writes <take>/audio/{narration.wav,narration.mp3,AUDIO.json}
and TAKES.json.
"""
import hashlib, json, math, re, subprocess, wave
from pathlib import Path

HERE = Path(__file__).resolve().parent
EP = HERE.parents[1]
REPO = EP.parents[2]
MASTER = EP / "assembly/r3/narration-master-r3.wav"
TRANSCRIPT = EP / "assembly/r3/word-transcript-r3.json"
BOARD = EP / "assembly/qa/ep009-r6-board.json"
SPF = 2000  # samples per 24 fps frame at 48 kHz
MAX_S = 15.0
WHISPER = ("/opt/homebrew/bin/whisper-cli", str(Path.home() / ".cache/hyperframes/whisper/models/ggml-small.en.bin"))
DONE = {}
SPLIT_AT = {"seg019": 285, "seg071": 230}  # frames; the r7 split points, so their slices and uploads are reused


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def rel(p):
    return str(Path(p).resolve().relative_to(REPO))


def norm(s):
    return re.sub(r"[^a-z0-9 ]", "", s.lower().replace("-", " ")).split()


words = json.load(open(TRANSCRIPT))["words"]
rows = [r for r in json.load(open(BOARD))["rows"] if r["lane"] == "presenter"]
master = wave.open(str(MASTER))
assert (master.getframerate(), master.getnchannels(), master.getsampwidth()) == (48000, 1, 2)

takes = []
for r in rows:
    f0, f1 = r["frames"]
    segw = [w for w in words if f0 / 24 <= w["start"] < f1 / 24]
    n = math.ceil((f1 - f0) / 24 / MAX_S)
    assert n <= 2, r["id"]
    cuts = [f0]
    if r["id"] in SPLIT_AT:
        cuts.append(f0 + SPLIT_AT[r["id"]])
    elif n == 2:
        # Widest pause that leaves both parts at or under MAX_S; nearer the middle breaks ties.
        gaps = [(round(b["start"] - a["end"], 2), -abs((a["end"] + b["start"]) / 2 * 24 - (f0 + f1) / 2), a, b)
                for a, b in zip(segw, segw[1:])
                if (a["end"] + b["start"]) / 2 * 24 - f0 <= MAX_S * 24 and f1 - (a["end"] + b["start"]) / 2 * 24 <= MAX_S * 24]
        g, _, a, b = max(gaps, key=lambda x: (x[0], x[1]))
        cuts.append(round((a["end"] + b["start"]) / 2 * 24))
    cuts.append(f1)
    for i in range(n):
        part = "abcdefgh"[i] if n > 1 else None
        a0, a1 = cuts[i], cuts[i + 1]
        take = f"{r['id']}{part or ''}"
        pw = [w for w in segw if a0 / 24 <= w["start"] < a1 / 24]
        text = " ".join(w["token"] for w in pw)
        entry = {"take": take, "segment": r["id"], "scene": r["scene"], "part": part,
                 "master_frames": [a0, a1], "segment_offset_frames": a0 - f0,
                 "seconds": (a1 - a0) / 24, "text": text,
                 "lead_silence_s": round(pw[0]["start"] - a0 / 24, 3) if pw else None,
                 "tail_silence_s": round(a1 / 24 - pw[-1]["end"], 3) if pw else None}
        if (r["id"], part) in DONE:
            entry["status"] = "done"; entry["selected"] = DONE[(r["id"], part)]
            takes.append(entry); continue
        out = HERE / take / "audio"; out.mkdir(parents=True, exist_ok=True)
        master.setpos(a0 * SPF)
        pcm = master.readframes((a1 - a0) * SPF)
        wav = out / "narration.wav"
        with wave.open(str(wav), "wb") as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(48000); w.writeframes(pcm)
        mp3 = out / "narration.mp3"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", wav, "-c:a", "libmp3lame", "-b:a", "192k", mp3], check=True)
        asr = subprocess.run([WHISPER[0], "-m", WHISPER[1], "-f", str(wav), "-nt", "-np"],
                             capture_output=True, text=True).stdout.strip()
        exp, got = norm(text), norm(asr)
        missing = [t for t in exp if t not in got]
        first = int.from_bytes(pcm[:2], "little", signed=True)
        last = int.from_bytes(pcm[-2:], "little", signed=True)
        entry.update({"status": "audio_ready", "wav": {"path": rel(wav), "sha256": sha(wav)},
                      "mp3": {"path": rel(mp3), "sha256": sha(mp3)},
                      "edge_samples": [first, last], "asr": asr,
                      "asr_missing_tokens": missing,
                      "seedance_duration_s": min(15, math.ceil((a1 - a0) / 24 + 1.0))})
        json.dump({"record_type": "presenter_regen_audio_slice",
                   "source": {"path": rel(MASTER), "sha256": sha(MASTER)}, **entry},
                  open(out / "AUDIO.json", "w"), indent=1)
        takes.append(entry)

json.dump({"record_type": "presenter_regen_takes", "takes": takes}, open(HERE / "TAKES.json", "w"), indent=1)
for t in takes:
    print(f"{t['take']:9} {t['seconds']:6.2f}s lead {t['lead_silence_s']} tail {t['tail_silence_s']} "
          f"edges {t.get('edge_samples')} dur {t.get('seedance_duration_s')} miss {t.get('asr_missing_tokens')}")
