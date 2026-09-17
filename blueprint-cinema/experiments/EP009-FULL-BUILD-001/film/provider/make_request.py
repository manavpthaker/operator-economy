import hashlib, json, sys
from pathlib import Path
BASE = Path(__file__).resolve().parent; FILM = BASE.parent
REPO = next(p for p in BASE.parents if (p / '.agents').is_dir())
take, start_note, prompt_file = sys.argv[1], sys.argv[2], sys.argv[3]
start = FILM / take / 'start.png'
req = {"take_id": take, "model": "fal-ai/kling-video/v3/pro/image-to-video",
       "local_start_image": str(start.relative_to(REPO)),
       "start_image_sha256": hashlib.sha256(start.read_bytes()).hexdigest(),
       "start_image_source": start_note,
       "input": {"prompt": Path(prompt_file).read_text().strip(), "duration": "8", "generate_audio": False, "cfg_scale": 0.5}}
(FILM / take / 'REQUEST.local.json').write_text(json.dumps(req, indent=2) + '\n')
print(req['start_image_sha256'])
