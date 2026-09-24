#!/usr/bin/env python3
"""Prepare two isolated HyperFrames scene replacements from explicitly selected real captures."""
import argparse, hashlib, html, json, pathlib, shutil, subprocess, wave

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[5]
EXP = ROOT / 'blueprint-cinema/experiments/EP007-NET-NEW-UNFINISHED-ANSWER-003'
REV = EXP / 'hyperframes/reviews'
MASTER = ROOT / 'operator-blueprint-v2/episodes/EP007-exit-readiness-prep/02-narration-production/master/narration-master.v4.wav'
MASTER_HASH = 'd8f7cb9630ae12ad427dca2c7bd1f29611f56c7985ce900ea312df3b9fec8da9'
SOURCES = {
 's15p1': ('r60-s15-p1/qa/r60-s15-p1.mp4','bb4db674443198245947756b2137b10512c91e63339ba3dfd62e581d5e1339c5'),
 's15p2': ('r60-s15-p2/qa/r60-s15-p2.mp4','e755a68ff5b2520d533b4d11c26ee02b547e68a2f61f13a9b0dc383c41cb961c'),
 's16p1': ('r61-s16-p1/qa/r61-s16-p1.mp4','86eb1c1d80733e7cfb811e7ccef0b33656bac12241b9c5e78134600ad30d54d7'),
 's16p2': ('r61-s16-p2/qa/r61-s16-p2.mp4','1b5cbeb3b630dbba13afeecf940e5639447136a59ded6f270477f5266d1b6827'),
}
PLAN = {
 'S15': {'master_start_frame':15216,'frames':1368,'insert':[608,892],
          'keep':[['s15p1',0,0,600],['s15p2',600,0,8],['s15p2',892,292,476]],
          # HyperFrames' source-video decoder leaves its first output frame white at this
          # cross-source boundary. Hold the same accepted source frame for that one frame.
          'seam_hold': {'timeline_frame':892,'source':'s15p2','source_frame':292,'frames':1,
                        'reason':'replace first-frame decoder blank with exact accepted source frame'}},
 'S16': {'master_start_frame':16584,'frames':1293,'insert':[213,868],
          'keep':[['s16p1',0,0,213],['s16p1',868,868,8],['s16p2',876,0,417]]},
}
def sha(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
def run(args, **kw): return subprocess.run([str(x) for x in args],check=True,**kw)
def probe(p):
 return json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=width,height,nb_frames,r_frame_rate,duration','-of','json',str(p)],text=True))['streams'][0]
def sec(f): return f'{f/24:.9f}'
def dump(p,obj):p.write_text(json.dumps(obj,indent=2)+'\n')
def validate_plan():
 for name,p in PLAN.items():
  a,b=p['insert']; intervals=sorted([(a,b)]+[(t,t+n) for _,t,_,n in p['keep']])
  assert intervals[0][0]==0 and intervals[-1][1]==p['frames']
  assert all(x[1]==y[0] for x,y in zip(intervals,intervals[1:])),name
  assert sum(y-x for x,y in intervals)==p['frames']
def prepare(name,p,selections):
 a,b=p['insert']; assert selections and sum(s['frames'] for s in selections)==b-a
 for s in selections:
  assert isinstance(s['frames'],int) and s['frames']>0
  assert isinstance(s['source_in_seconds'],(float,int)) and s['source_in_seconds']>=0
  src=pathlib.Path(s['source_path']).resolve(); assert src.is_file() and sha(src)==s['sha256'],src
  info=probe(src); assert s['source_in_seconds']+s['frames']/24<=float(info['duration'])+1/24000,src
  if s.get('crop'):
   c=s['crop']; assert all(isinstance(c[k],int) for k in ['x','y','width','height'])
   assert c['x']>=0 and c['y']>=0 and c['width']>0 and c['height']>0
   assert c['x']+c['width']<=info['width'] and c['y']+c['height']<=info['height']
 target=HERE/'projects'/name.lower(); assert not target.exists(),f'Preserve existing output; choose an unused packet path: {target}'
 for sub in ['public/media','public/audio','public/fonts','qa']:(target/sub).mkdir(parents=True,exist_ok=True)
 pins={}
 for key in {r[0] for r in p['keep']}:
  rel,expected=SOURCES[key];src=REV/rel;assert sha(src)==expected,src
  shutil.copy2(src,target/f'public/media/{key}.mp4');pins[key]={'source':str(src),'sha256':expected}
 seam_hold=None
 if p.get('seam_hold'):
  repair=p['seam_hold'];src=target/f'public/media/{repair["source"]}.mp4'
  hold=target/'public/media/seam-hold.png'
  run(['ffmpeg','-v','error','-nostdin','-i',src,'-vf',f'select=eq(n\\,{repair["source_frame"]})','-frames:v','1',hold])
  assert hold.is_file()
  seam_hold={**repair,'asset':str(hold),'asset_sha256':sha(hold)}
 assert sha(MASTER)==MASTER_HASH
 with wave.open(str(MASTER),'rb') as src:
  assert (src.getframerate(),src.getnchannels(),src.getsampwidth())==(48000,1,2)
  src.setpos(p['master_start_frame']*2000);pcm=src.readframes(p['frames']*2000)
  assert len(pcm)==p['frames']*4000
 with wave.open(str(target/'public/audio/narration.wav'),'wb') as out:
  out.setnchannels(1);out.setsampwidth(2);out.setframerate(48000);out.writeframes(pcm)
 font=ROOT/'design-system/boundary-ledger/fonts/supreme-500.woff2'
 shutil.copy2(font,target/'public/fonts/supreme-500.woff2')
 clips=[]
 for i,(key,t,source_in,n) in enumerate(p['keep']):
  clips.append(f'<video id="{name}-keep-{i}" class="accepted" src="public/media/{key}.mp4" data-start="{sec(t)}" data-duration="{sec(n)}" data-media-start="{sec(source_in)}" data-track-index="1" muted playsinline></video>')
 if seam_hold:
  clips.append(f'<img id="{name}-seam-hold" class="accepted clip" src="public/media/seam-hold.png" data-start="{sec(seam_hold["timeline_frame"])}" data-duration="{sec(seam_hold["frames"])}" data-track-index="2" alt="">')
 clips.append(f'<div id="{name}-paper" class="paper clip" data-start="{sec(a)}" data-duration="{sec(b-a)}" data-track-index="0"></div>')
 cursor=a;derived=[]
 for i,s in enumerate(selections):
  src=pathlib.Path(s['source_path']).resolve(); dest=target/f'public/media/capture-{i:02d}.mp4';filters=[]
  if s.get('crop'):
   c=s['crop'];filters.append(f"crop={c['width']}:{c['height']}:{c['x']}:{c['y']}")
  filters+=['fps=24','setsar=1']
  run(['ffmpeg','-v','error','-nostdin','-i',src,'-ss',s['source_in_seconds'],'-t',sec(s['frames']),'-vf',','.join(filters),'-an','-frames:v',s['frames'],'-c:v','libx264','-crf','16','-preset','medium','-pix_fmt','yuv420p','-movflags','+faststart',dest])
  got=probe(dest);assert int(got['nb_frames'])==s['frames'] and got['r_frame_rate']=='24/1',got
  clips.append(f'<video id="{name}-capture-{i}" class="capture" src="public/media/capture-{i:02d}.mp4" data-start="{sec(cursor)}" data-duration="{sec(s["frames"])}" data-media-start="0" data-track-index="1" muted playsinline></video>')
  derived.append({**s,'derivative':str(dest),'derivative_sha256':sha(dest),'timeline_start_frame':cursor,'duration_frames':s['frames'],'playback_rate':1})
  cursor+=s['frames']
 assert cursor==b
 clips.append(f'<p id="{name}-disclosure" class="disclosure clip" data-start="{sec(a)}" data-duration="{sec(b-a)}" data-track-index="2">Illustrative example · fictional business</p>')
 template=(HERE/'composition.template.html').read_text()
 (target/'index.html').write_text(template.replace('__COMPOSITION_ID__',f'ep007-r77-{name.lower()}').replace('__DURATION__',sec(p['frames'])).replace('__CLIPS__','\n'.join(clips)))
 dump(target/'hyperframes.json',{'$schema':'https://hyperframes.heygen.com/schema/hyperframes.json','authoringSkill':'general-video','media':{'autoProxy':False}})
 dump(target/'package.json',{'name':f'ep007-r77-{name.lower()}','private':True,'type':'module','scripts':{'check':'npx --yes hyperframes@0.8.46 check','render':'npx --yes hyperframes@0.8.46 render'}})
 dump(target/'PROVENANCE.json',{'plan':p,'accepted_sources':pins,'capture_selections':derived,'seam_hold':seam_hold,'master':{'path':str(MASTER),'sha256':MASTER_HASH,'start_sample':p['master_start_frame']*2000,'samples':p['frames']*2000},'staged_audio_sha256':sha(target/'public/audio/narration.wav'),'font_sha256':sha(font),'status':'prepared_not_rendered_not_accepted'})
 return target
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--selection',type=pathlib.Path);ap.add_argument('--describe',action='store_true');ap.add_argument('--render',action='store_true');args=ap.parse_args();validate_plan()
 if args.describe:print(json.dumps(PLAN,indent=2));return
 assert args.selection,'Pass the root-selected source/range JSON with --selection.'
 selected=json.loads(args.selection.read_text())
 for name,p in PLAN.items():
  project=prepare(name,p,selected[name]);print(project)
  if args.render:
   run(['npx','--yes','hyperframes@latest','upgrade','--project','.', '--check'],cwd=project)
   a,b=p['insert'];times=[0,(a-1)/24,a/24,(a+b)/48,(b-1)/24,b/24,(p['frames']-1)/24]
   with open(project/'qa/check.json','w') as log:run(['npx','--yes','hyperframes@0.8.46','check','.','--strict','--at',','.join(str(t) for t in times),'--json','--snapshots'],cwd=project,stdout=log)
   with open(project/'qa/render.log','w') as log:run(['npx','--yes','hyperframes@0.8.46','render','.','--output',f'qa/{name.lower()}.mp4','--quality','looks','--workers','1'],cwd=project,stdout=log,stderr=subprocess.STDOUT)
   output=project/f'qa/{name.lower()}.mp4';assert int(probe(output)['nb_frames'])==p['frames'];run(['ffmpeg','-v','error','-i',output,'-f','null','-'])
if __name__=='__main__':main()
