#!/bin/zsh
set -eu
TASK_DIR="${0:A:h}"
if [[ -e "$TASK_DIR/EP007-avatar-v4-wide-to-close-review.mp4" ]]; then
  print -u2 "Existing final review is preserved. Use a separate revision directory to render another candidate."
  exit 1
fi
cd "$TASK_DIR/project"
python3 - <<'PY'
import json
from pathlib import Path
b=json.loads(Path('binding.json').read_text())
if not b['source']['actual_video_bound']:
 raise SystemExit('Refusing final review render: only the still study is bound. Bind the actual restored V4 video first.')
PY
npx --yes hyperframes@0.8.34 check --snapshots
npx --yes hyperframes@0.8.34 render --fps 24 --sdr --quality high --workers 2 --strict --output ../EP007-avatar-v4-hyperframes-premux.mp4

python3 - <<'PYHASH'
from pathlib import Path
import hashlib
p=Path('/Users/brownmanbrain/GitHub/operator-economy/blueprint-cinema/experiments/EP007-PRESENTER-001/avatar-v4-wide/media/generated-original-audio.mp4')
assert hashlib.sha256(p.read_bytes()).hexdigest() == '19f57219ec8a75fe49880c560ad556006699e79ec4a2b9884ed5bae20f215f02'
PYHASH
ffmpeg -hide_banner -loglevel error -i ../EP007-avatar-v4-hyperframes-premux.mp4 -i /Users/brownmanbrain/GitHub/operator-economy/blueprint-cinema/experiments/EP007-PRESENTER-001/avatar-v4-wide/media/generated-original-audio.mp4 -map 0:v:0 -map 1:a:0 -c:v copy -c:a copy -movflags +faststart ../EP007-avatar-v4-wide-to-close-review.mp4
