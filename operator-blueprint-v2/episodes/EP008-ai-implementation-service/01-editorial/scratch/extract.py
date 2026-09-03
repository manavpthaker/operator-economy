#!/usr/bin/env python3
"""oe-spoken-text-v1 style extractor: narration blocks only.
Usage: python3 extract.py script.md [--readthrough out.txt] [--json]
Prints per-scene word counts and totals."""
import re, sys, json
path = sys.argv[1]
text = open(path, encoding="utf-8").read()
scenes = []  # (id, title, narration)
cur = None
in_narr = False
buf = []
for line in text.splitlines():
    m = re.match(r"^## (S\d\d): (.*)$", line)
    if m:
        if cur and buf is not None:
            scenes.append((cur[0], cur[1], "\n".join(buf).strip()))
        cur = (m.group(1), m.group(2)); buf = []; in_narr = False
        continue
    if line.startswith("## ") and not m:
        if cur:
            scenes.append((cur[0], cur[1], "\n".join(buf).strip())); cur = None; buf = []
        in_narr = False
        continue
    if cur:
        if line.strip() == "### Narration":
            in_narr = True; continue
        if line.startswith("### "):
            in_narr = False; continue
        if in_narr:
            buf.append(line)
if cur:
    scenes.append((cur[0], cur[1], "\n".join(buf).strip()))
out = []
tot = 0
for sid, title, narr in scenes:
    n = len(narr.split())
    tot += n
    out.append((sid, title, n, narr))
opp_ids = {f"S{i:02d}" for i in range(0, 12)}
opp = sum(n for sid, _, n, _ in out if sid in opp_ids)
build = tot - opp
if "--json" in sys.argv:
    print(json.dumps({"total": tot, "opp": opp, "build": build, "share_opp": round(100*opp/tot,1), "scenes": [(s,t,n) for s,t,n,_ in out]}))
else:
    for sid, title, n, _ in out:
        print(f"{sid} {n:5d}  {title}")
    print(f"TOTAL {tot}  opportunity(S00-S11) {opp} = {100*opp/tot:.1f}%  build {build} = {100*build/tot:.1f}%")
    print(f"duration @140-165 wpm: {tot/165:.1f} to {tot/140:.1f} min")
if "--readthrough" in sys.argv:
    rt = sys.argv[sys.argv.index("--readthrough")+1]
    body = "\n\n".join(narr for _,_,_,narr in out if narr)
    open(rt, "w", encoding="utf-8").write(body + "\n")
