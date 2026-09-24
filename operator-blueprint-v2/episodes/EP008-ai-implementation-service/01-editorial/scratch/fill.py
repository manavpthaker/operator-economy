#!/usr/bin/env python3
"""Fill {{H_*}} placeholders in dependency order and record hashes.
Usage: python3 fill.py <stage>   where stage in {v01, v02, final}
Hashes are stored in hashes.json (working file, deleted before delivery)."""
import hashlib, json, os, re, sys
stage = sys.argv[1]
H = json.load(open('hashes.json')) if os.path.exists('hashes.json') else {}
def sha(p):
    return hashlib.sha256(open(p,'rb').read()).hexdigest()
def fill(path, key=None):
    s = open(path, encoding='utf-8').read()
    for k, v in H.items():
        s = s.replace('{{%s}}' % k, v)
    left = re.findall(r'\{\{([A-Z_0-9]+)\}\}', s)
    if left:
        raise SystemExit(f"{path}: unresolved placeholders {sorted(set(left))}")
    open(path, 'w', encoding='utf-8').write(s)
    if key:
        H[key] = sha(path)
        print(f"{key:14s} {H[key]}  {path}")
order_v01 = [('handoff.md','H_HANDOFF'),('editorial-contract.md','H_CONTRACT'),('operator-canvas.md','H_CANVAS'),
             ('episode-investment-thesis.md','H_EIT'),('narrative-spine.md','H_SPINE'),('episode-beat-sheet.md','H_BEATS'),
             ('episode-outline.md','H_OUTLINE'),('voice-and-comedy-map.md','H_VCM'),('script.md','H_SCRIPT_V01')]
order_v02 = [('script.md','H_SCRIPT'),('performance-readthrough.txt','H_READ'),('claims-map.md','H_CLAIMS'),
             ('editorial-voice-conformity.md','H_E5V'),('review-disposition.md','H_REVIEW'),('editorial-lock.md','H_LOCK')]
if stage == 'v01':
    for p,k in order_v01: fill(p,k)
elif stage == 'v02':
    for p,k in order_v02: fill(p,k)
json.dump(H, open('hashes.json','w'), indent=1)
