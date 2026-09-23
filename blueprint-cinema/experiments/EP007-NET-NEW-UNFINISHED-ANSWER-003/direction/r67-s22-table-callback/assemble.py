#!/usr/bin/env python3
"""Create the S21-tail/S22-plan review with continuous original narration."""
from pathlib import Path
import json,subprocess
ROOT=Path(__file__).resolve().parents[5]
EXP=ROOT/'blueprint-cinema/experiments/EP007-NET-NEW-UNFINISHED-ANSWER-003'
H=EXP/'hyperframes/reviews/r67-s22-plan'
C=EXP/'hyperframes/reviews/r67-s22-context'
(C/'qa').mkdir(parents=True,exist_ok=True)
prior=EXP/'hyperframes/reviews/r66-s21-hard-part/qa/s21.mp4'
master=ROOT/'operator-blueprint-v2/episodes/EP007-exit-readiness-prep/02-narration-production/master/narration-master.v4.wav'
cmd=['ffmpeg','-y','-v','error','-i',str(prior),'-i',str(H/'qa/s22-plan.mp4'),'-i',str(master),
 '-filter_complex','[0:v]trim=start_frame=1280:end_frame=1472,setpts=PTS-STARTPTS[v0];[1:v]trim=start_frame=0:end_frame=524,setpts=PTS-STARTPTS[v1];[v0][v1]concat=n=2:v=1:a=0[v];[2:a]atrim=start_sample=49876000:end_sample=51308000,asetpts=PTS-STARTPTS,pan=stereo|c0=c0|c1=c0[a]',
 '-map','[v]','-map','[a]','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-r','24','-c:a','aac','-b:a','192k','-movflags','+faststart',str(C/'qa/context.mp4')]
(C/'qa/assembly-command.json').write_text(json.dumps(cmd,indent=2)+'\n')
subprocess.run(cmd,check=True)
frames=[191,192,246,247,309,310,479,480,600,715]
sel='+'.join('eq(n\\,%s)'%n for n in frames)
subprocess.run(['ffmpeg','-y','-v','error','-i',str(C/'qa/context.mp4'),'-vf',f'select={sel},scale=640:360,tile=2x5','-frames:v','1','-update','1',str(H/'qa/encoded-contact.png')],check=True)
print('Context:716frames /29.833333s. S22 starts8s. Missing actions labeled.')

