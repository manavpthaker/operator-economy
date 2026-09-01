#!/usr/bin/env python3
"""Step 3 mechanical gate checks.

Implements only the gate conditions that are mechanically decidable. It clears
HYGIENE. It cannot establish whether direction is any good -- that is the
separate creative decision every Step 3 gate records.

Usage: validate.py <fixture-dir>
"""
import json,sys,pathlib,re

def load(d,name):
    p=pathlib.Path(d)/name
    return json.loads(p.read_text()) if p.is_file() else None

def check(d):
    f=[]
    canvas=load(d,"canvas.json") or {}
    eng=load(d,"engine.json") or {}
    world=load(d,"world.json") or {}
    plan=load(d,"visual-plan.json") or {}
    look=load(d,"look.json") or {}
    lock=load(d,"lock.json") or {}
    claims=set((load(d,"claims.json") or {}).get("claim_ids",[]))

    # V2 -- derived business fields must match the Canvas
    for k,v in (eng.get("derived") or {}).items():
        if canvas.get(k)!=v:
            f.append(("V2",f"derived field '{k}' diverges from Canvas: engine={v!r} canvas={canvas.get(k)!r}"))
    # V2 -- mechanic honesty: compounding metaphors need evidence
    mech=(eng.get("visual_mechanic") or {})
    if re.search(r'flywheel|gravity|compound', str(mech.get("name","")), re.I) and not mech.get("compounding_evidence"):
        f.append(("V2",f"mechanic '{mech.get('name')}' implies compounding with no evidence"))
    verbs={v["verb"] for v in (eng.get("motion_verbs") or [])}
    if verbs and not 3<=len(verbs)<=6:
        f.append(("V2",f"{len(verbs)} motion verbs; must be 3 to 6"))

    # V3 -- world integrity
    objs={o["id"]:o for o in (world.get("objects") or [])}
    for o in objs.values():
        if not o.get("static") and not (set(o.get("verbs") or []) & verbs):
            f.append(("V3",f"object '{o['id']}' is neither verb-reachable nor marked static"))
    for v in (eng.get("motion_verbs") or []):
        for t in (v.get("acts_on") or []):
            if t not in objs: f.append(("V3",f"verb '{v['verb']}' acts on unknown object '{t}'"))
    for a in (world.get("evidence_anchors") or []):
        if a.get("claim_id") not in claims:
            f.append(("V3",f"evidence anchor '{a.get('id')}' binds to unknown claim '{a.get('claim_id')}'"))

    # V4 -- plan integrity
    for u in (plan.get("units") or []):
        uid=u.get("id")
        if "in_word" not in u or "out_word" not in u:
            f.append(("V4",f"unit '{uid}' timing is not bound to word indices"))
        if u.get("timing_source") and u["timing_source"]!="transcript":
            f.append(("V4",f"unit '{uid}' timing_source is '{u['timing_source']}', not transcript"))
        inert = u.get("world_state_before")==u.get("world_state_after") and not u.get("evidence")
        if inert and not u.get("inert_justification"):
            f.append(("V4",f"unit '{uid}' is inert: no state change and no evidence, unjustified"))
        if u.get("motion_verb") and verbs and u["motion_verb"] not in verbs:
            f.append(("V4",f"unit '{uid}' uses verb '{u['motion_verb']}' not in the engine"))
        for o in (u.get("carry") or [])+(u.get("focus") or []):
            if o not in objs: f.append(("V4",f"unit '{uid}' references unknown object '{o}'"))
        for e in (u.get("evidence") or []):
            up=e.get("upstream_label"); cur=e.get("label")
            rank={"UNKNOWN":0,"MODELED":1,"PARALLEL":2,"OBSERVED":3}
            if up and cur and rank.get(cur,0)>rank.get(up,0):
                f.append(("V4",f"unit '{uid}' upgrades evidence label {up} -> {cur}"))

    # V6 -- look must be provisional
    if look and look.get("approval") not in (None,"provisional"):
        f.append(("V6",f"look approval is '{look['approval']}'; must be provisional"))

    # V7 -- no runtime named anywhere in the locked artifacts
    runtimes=r'\b(hyperframes|remotion|after ?effects|davinci|resolve|fusion|blender|unreal)\b'
    for name in ("engine.json","world.json","visual-plan.json","direction-bible.md","look.json","lock.json"):
        p=pathlib.Path(d)/name
        if p.is_file():
            for m in set(re.findall(runtimes,p.read_text(),re.I)):
                f.append(("V7",f"runtime '{m}' named in {name}"))
    for k,v in (lock.get("audio_only") or {}).items():
        if v is False: f.append(("V7",f"audio-only rule broken: '{k}' exists only in a visual"))
    return f

if __name__=="__main__":
    d=sys.argv[1]
    fails=check(d)
    exp=(load(d,"expect.json") or {})
    expected=exp.get("expect_failures",[])
    got=sorted({g for g,_ in fails})
    print(f"{pathlib.Path(d).name}")
    for g,msg in fails: print(f"   {g}  {msg}")
    ok = got==sorted(set(expected))
    print(f"   -> gates failing: {got or 'none'} | expected: {sorted(set(expected)) or 'none'} | {'PASS' if ok else 'MISMATCH'}\n")
    sys.exit(0 if ok else 1)
