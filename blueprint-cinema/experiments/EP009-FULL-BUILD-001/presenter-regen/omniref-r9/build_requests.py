#!/usr/bin/env python3
"""Write the r9 Seedance requests from the owner-approved seg021 omniref prompt.

Each take: locked still, exact slice, K01, and its own conformed OmniHuman reference (REF-UPLOADS.json).
References over the seg021 motion ceiling get the gentler-scale line. seg055 keeps its quoted words out
(Higgsfield content filter, 2026-09-25).
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
plan = json.load(open(HERE / "PLAN.json"))
refs = json.load(open(HERE / "REFS.json"))["refs"]
uploads = json.load(open(HERE / "REF-UPLOADS.json"))
template = json.load(open(HERE.parent / "omni-ref-test/TEST.json"))["requests"]["seg021"]["prompt"]
OLD_DUR = "One continuous twelve-second"
OLD_SPOKEN = ('Speak only the exact 10.083333-second AUDIO reference: "I think it can be sold from outside. But only for what it recovers, '
              'and what it recovers is a number. By the end you\'ll be able to compute it for any inn."')
EYES = "The eyes stay engaged with the lens."
GENTLE = " Follow the second VIDEO's body language at a gentler, smaller scale."
assert OLD_DUR in template and OLD_SPOKEN in template and EYES in template
WORDS = {5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine", 10: "ten", 11: "eleven", 12: "twelve", 13: "thirteen", 14: "fourteen", 15: "fifteen"}
IMAGE = "eb9cdb1e-a6c2-44cb-bb06-a097b8432a30"
K01 = "b796a739-5036-4242-8fa9-cd61e9e19a0c"

reqs = {}
for take, t in plan["takes"].items():
    d = t["seedance_duration_s"]
    spoken = (f"Speak only the exact {t['seconds']:.6f}-second AUDIO reference, word for word." if take == "seg055"
              else f'Speak only the exact {t["seconds"]:.6f}-second AUDIO reference: "{t["text"]}"')
    p = template.replace(OLD_DUR, f"One continuous {WORDS[d]}-second").replace(OLD_SPOKEN, spoken)
    if refs[take]["gentle"]:
        p = p.replace(EYES, EYES + GENTLE)
    reqs[take] = {"model": "seedance_2_5", "mode": "omni_reference", "duration": d, "resolution": "1080p", "aspect_ratio": "16:9",
                  "generate_audio": True, "count": 1, "use_unlim": False, "prompt": p,
                  "medias": [{"role": "image", "value": IMAGE}, {"role": "audio", "value": t["audio_media_id"]},
                             {"role": "video", "value": K01}, {"role": "video", "value": uploads[take]["media_id"]}]}
json.dump(reqs, open(HERE / "SEEDANCE-REQUESTS.json", "w"), indent=1)
print(len(reqs), sum(r["duration"] for r in reqs.values()) * 12, "credits;", "gentle:", [k for k in refs if refs[k]["gentle"]])
