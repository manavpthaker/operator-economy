#!/usr/bin/env python3
"""r10 Seedance requests: the r10 prompt (owner-checked on seg009/seg044) with each take's words, K01 and its picked 25 fps reference."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
plan = json.load(open(HERE / "PLAN.json"))
uploads = json.load(open(HERE / "REF-UPLOADS.json"))
template = json.load(open(HERE.parent / "r10-test/TEST.json"))["takes"]["seg009"]["request"]["prompt"]
OLD_DUR = "One continuous eleven-second"
OLD_SPOKEN = ('Speak only the exact 9.166667-second AUDIO reference: "I couldn\'t find anyone selling it who\'d done that arithmetic. '
              'So what did that second stay actually cost her, and who gets paid to stop it?"')
assert OLD_DUR in template and OLD_SPOKEN in template
WORDS = {5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine", 10: "ten", 11: "eleven", 12: "twelve", 13: "thirteen", 14: "fourteen", 15: "fifteen"}
reqs = {}
for take, t in plan["takes"].items():
    d = t["seedance_duration_s"]
    spoken = (f"Speak only the exact {t['seconds']:.6f}-second AUDIO reference, word for word." if take == "seg055"
              else f'Speak only the exact {t["seconds"]:.6f}-second AUDIO reference: "{t["text"]}"')
    reqs[take] = {"model": "seedance_2_5", "mode": "omni_reference", "duration": d, "resolution": "1080p", "aspect_ratio": "16:9",
                  "generate_audio": True, "count": 1, "use_unlim": False,
                  "prompt": template.replace(OLD_DUR, f"One continuous {WORDS[d]}-second").replace(OLD_SPOKEN, spoken),
                  "medias": [{"role": "image", "value": "eb9cdb1e-a6c2-44cb-bb06-a097b8432a30"}, {"role": "audio", "value": t["audio_media_id"]},
                             {"role": "video", "value": "b796a739-5036-4242-8fa9-cd61e9e19a0c"}, {"role": "video", "value": uploads[take]["media_id"]}]}
json.dump(reqs, open(HERE / "SEEDANCE-REQUESTS.json", "w"), indent=1)
print(len(reqs), sum(r["duration"] for r in reqs.values()) * 12, "credits")
