#!/usr/bin/env python3
"""Rebuild the S20-tail/S21 context and final representative encoded contact sheet."""
from pathlib import Path
import json
import subprocess
BASE = Path(__file__).resolve().parents[2]
CONTEXT = BASE / 'hyperframes/reviews/r66-s21-context'
SCENE = BASE / 'hyperframes/reviews/r66-s21-hard-part'
cmd = json.loads((CONTEXT / 'qa/assembly-command.json').read_text())
cmd.insert(1, '-y')
subprocess.run(cmd, check=True)
frames = [191,192,648,734,736,900,1159,1161,1200,1392,1635,1663]
selection = '+'.join('eq(n\\,%s)' % f for f in frames)
subprocess.run(['ffmpeg','-y','-v','error','-i',str(CONTEXT/'qa/context.mp4'),'-vf',f'select={selection},scale=640:360,tile=3x4','-frames:v','1','-update','1',str(SCENE/'qa/encoded-contact.png')],check=True)
