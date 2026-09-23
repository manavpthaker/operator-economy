"""Build EP007 R81 verbatim captions from the locked narration word transcript.
Maps master time -> R79 output (SEGMENTS.json piecewise map) -> R81 (cut [14204,14255) removed)."""
import json, re, sys
ROOT = "/Users/brownmanbrain/GitHub/operator-economy/"
SEG = json.load(open(ROOT + "blueprint-cinema/experiments/EP007-NET-NEW-UNFINISHED-ANSWER-003/assembly/r79-full-conform/SEGMENTS.json"))
WORDS = json.load(open(ROOT + "operator-blueprint-v2/episodes/EP007-exit-readiness-prep/02-narration-production/word-transcript.json"))
WORDS = WORDS["words"] if isinstance(WORDS, dict) else WORDS
CUT, CUTN, TOTAL = (14204, 14255), 51, 27190
segs = [(m["master_frames_half_open"], m["output_frames_half_open"]) for m in SEG["prefix_timing_map"]]
segs += [(s["master_frames_half_open"], s["output_frames_half_open"]) for s in SEG["segments"][1:]]

def to_out(t):  # master seconds -> R81 frames (float), None if dropped
    f = t * 24
    for (ma, mb), (oa, ob) in segs:
        if ma <= f < mb or (f == mb and mb == segs[-1][0][1]):
            if ob == oa:
                return None
            o = oa + (f - ma) * (ob - oa) / (mb - ma)
            if CUT[0] <= o < CUT[1]:
                return None
            return o - CUTN if o >= CUT[1] else o
    return None

words = []
for w in WORDS:
    a, b = to_out(w["start"]), to_out(w["end"])
    if a is None or b is None:
        continue
    words.append([w["token"].strip(), a / 24, b / 24])

cues, cur = [], []
def flush():
    if cur:
        cues.append([cur[0][1], cur[-1][2], " ".join(x[0] for x in cur)])
        cur.clear()
for i, w in enumerate(words):
    if cur:
        text = " ".join(x[0] for x in cur + [w])
        gap = w[1] - cur[-1][2]
        if len(text) > 84 or w[2] - cur[0][1] > 6.0 or gap > 0.6:
            flush()
    cur.append(w)
    n = len(" ".join(x[0] for x in cur))
    if (re.search(r"[.?!]$", w[0]) and n > 12) or (re.search(r"[,;:]$", w[0]) and n > 48):
        flush()
flush()

def wrap(t):
    if len(t) <= 42:
        return t
    mid = len(t) // 2
    sp = min((i for i, c in enumerate(t) if c == " "), key=lambda i: abs(i - mid))
    return t[:sp] + "\n" + t[sp + 1:]
def ts(s):
    ms = round(s * 1000); h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); s_, ms = divmod(ms, 1000)
    return f"{h:02}:{m:02}:{s_:02},{ms:03}"
out = []
for i, (a, b, t) in enumerate(cues):
    nxt = cues[i + 1][0] if i + 1 < len(cues) else TOTAL / 24
    b = min(max(b + 0.25, a + 1.0), nxt - 0.05)  # short hold, never overlap
    out.append(f"{i+1}\n{ts(a)} --> {ts(b)}\n{wrap(t)}\n")
open(sys.argv[1], "w").write("\n".join(out))
json.dump(words, open(sys.argv[1].replace(".srt", "-words.json"), "w"))
print(len(words), "words", len(cues), "cues", "max line", max(len(l) for c in out for l in c.split("\n")[2:]))
