#!/usr/bin/env python3
"""Build a source-bound curiosity trailer, preserving the locked episode and R1."""
from pathlib import Path
import hashlib, html, json, os, shutil, subprocess, re

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[2]
OUT = ROOT / '01-second-commission'
CARRIER = REPO / 'blueprint-cinema/experiments/EP009-FULL-BUILD-001/assembly/qa/r8-tool-clarity/ep009-r8-tool-clarity-review-r1.mp4'
WORDS = REPO / 'blueprint-cinema/experiments/EP009-FULL-BUILD-001/assembly/r3/word-transcript-r3.json'
LOCK = REPO / 'blueprint-cinema/experiments/EP009-FULL-BUILD-001/assembly/r8-tool-clarity/FINAL-EPISODE-LOCK-r8.json'
EXPECTED = 'cc5805a990d10812b5349568e50a74dc0e21b09ed402b49250f9796640ed710e'
FPS = 24
# Sentence cuts preserve complete original words and their natural delivery.
CUTS = [(648,763,'W000075','W000088','return'),(780,870,'W000089','W000101','charge'),(882,941,'W000102','W000109','recognition'),(973,1080,'W000110','W000123','service'),(1317,1427,'W000150','W000165','question')]

CSS = '''
@font-face{font-family:Supreme;src:url('assets/fonts/supreme-500.woff2');font-weight:500}
@font-face{font-family:Zodiak;src:url('assets/fonts/zodiak-700.woff2');font-weight:700}
*{box-sizing:border-box;margin:0;padding:0}html,body{width:1080px;height:1920px;overflow:hidden;background:#F5F0E6}
#root{position:relative;width:1080px;height:1920px;overflow:hidden;color:#173530;font-family:Supreme,Arial,sans-serif}
.scene{position:absolute;inset:0;width:1080px;height:1920px;overflow:hidden;background:#F5F0E6}
.brand{position:absolute;left:72px;top:65px;font-size:24px;letter-spacing:.11em;z-index:50}
.label{font-size:29px;letter-spacing:.10em;color:#586D74;text-transform:uppercase}
.headline{position:absolute;left:72px;top:166px;width:850px;font:700 100px/1.03 Zodiak,Georgia,serif;letter-spacing:-.035em}
.headline em{font-style:normal;color:#B5482F}.hero{position:absolute;left:72px;top:560px;width:850px;height:750px}
.stay{width:100%;height:190px;border:4px solid #173530;display:flex;align-items:center;justify-content:space-between;padding:32px;background:#F5F0E6;font-size:49px}
.stay small{font-size:28px;letter-spacing:.08em}.stay b{font-weight:500}.stay.active{background:#173530;color:#F5F0E6}
.arrow{text-align:center;font-size:75px;line-height:110px;color:#B5482F}.website{border:4px solid #B5482F;padding:35px;font-size:54px;text-align:center;color:#B5482F}
.bill{border:4px solid #173530;padding:42px;position:absolute;top:0;width:100%;height:300px;background:#F5F0E6}
.bill.second{top:354px}.bill .charge{font:700 73px/1.1 Zodiak,Georgia,serif;margin-top:33px}.stamp{position:absolute;right:18px;top:236px;background:#B5482F;color:#F5F0E6;padding:18px 28px;font-size:44px;transform:rotate(0deg)}
.footage{position:absolute;left:0;top:280px;width:1080px;height:1120px;overflow:hidden}.footage video{position:absolute;top:0;left:-430px;width:1992px;height:1120px;object-fit:fill;max-width:none}
.film-head{position:absolute;z-index:5;left:70px;top:170px;width:850px;font:700 78px/1.04 Zodiak,Georgia,serif;letter-spacing:-.035em}
.service-word{font:700 145px/1.0 Zodiak,Georgia,serif;letter-spacing:-.045em}.service-arrow{height:170px;display:grid;place-items:center;color:#B5482F;font-size:95px}.unanswered{border:4px solid #B5482F;padding:45px 30px;color:#B5482F;font-size:67px;line-height:1.08}
.caption{position:absolute;left:70px;top:1430px;width:850px;padding:24px 30px;background:#173530;color:#F5F0E6;font:500 64px/1.13 Supreme,Arial,sans-serif;letter-spacing:-.025em;z-index:40;min-height:105px}
.context{position:absolute;left:72px;top:1645px;width:830px;font:500 29px/1.2 Supreme,Arial,sans-serif;color:#586D74;letter-spacing:.035em;z-index:45}
.end{background:#173530;color:#F5F0E6}.end .label{color:#D8CFB9}.end .headline{top:360px;font-size:112px}.end .cta{position:absolute;left:72px;top:1140px;width:850px;border-top:4px solid #FB8B69;padding-top:40px;font-size:55px;line-height:1.18}.end .cta span{display:block;color:#FB8B69;font-size:39px;margin-top:32px}
'''

def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def tag(content, i, start, duration, cls='scene'):
    return f'<section id="s{i}" class="clip {cls}" data-start="{start:.9f}" data-duration="{duration:.9f}" data-track-index="1">{content}</section>'

def main():
    assert digest(CARRIER)==EXPECTED
    assert digest(WORDS)=='0b5175dea2cbb1ac7682cd69b9ab032bc8c544131aae82575140e90ae0d76709'
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/'assets/fonts').mkdir(parents=True,exist_ok=True)
    link=OUT/'assets/locked-carrier.mp4'
    if not link.exists(): link.symlink_to(os.path.relpath(CARRIER,link.parent))
    for f in ['supreme-500.woff2','zodiak-700.woff2']:
        shutil.copy2(REPO/'design-system/boundary-ledger/fonts'/f,OUT/'assets/fonts'/f)
    prior=REPO/'blueprint-cinema/experiments/EP009-SHORTS-001/01-second-commission'
    for f in ['AGENTS.md','CLAUDE.md','hyperframes.json','package.json']:
        shutil.copy2(prior/f,OUT/f)
    words=json.loads(WORDS.read_text())['words']; by={w['w_id']:i for i,w in enumerate(words)}
    edl=[]; captions=[]; bodies=[]; audio=[]; videos=[]; motion=[]; cursor=0
    for i,(f0,f1,w0,w1,kind) in enumerate(CUTS):
        start=cursor/FPS; d=(f1-f0)/FPS; src=f0/FPS
        subset=words[by[w0]:by[w1]+1]
        edl.append({'id':i,'source_in_frame':f0,'source_out_frame_exclusive':f1,'timeline_in_frame':cursor,'duration_frames':f1-f0,'first_word':w0,'last_word':w1,'text':' '.join(w['token'] for w in subset),'visual':kind})
        audio.append(f'<audio id="a{i}" src="assets/locked-carrier.mp4" data-start="{start:.9f}" data-duration="{d:.9f}" data-media-start="{src:.9f}" data-track-index="10"></audio>')
        if kind=='return':
            body='<h1 class="headline">Same guest.<br><em>Second commission.</em></h1><div class="hero"><div class="stay"><small>FIRST STAY</small><b>GUEST → INN</b></div><div class="arrow">↓</div><div class="stay active"><small>A YEAR LATER</small><b>SAME ROOM</b></div><div class="arrow">↓</div><div class="website">SAME BOOKING SITE</div></div>'
            motion += [f'tl.fromTo("#s{i} .stay",{{x:30}},{{x:0,duration:.25,stagger:.1,ease:"power2.out"}},{start});',f'tl.fromTo("#s{i} .website",{{opacity:0,y:20}},{{opacity:1,y:0,duration:.3,ease:"power2.out"}},{start+2.8});']
        elif kind=='charge':
            body='<h1 class="headline">She pays.<br><em>Again.</em></h1><div class="hero"><div class="bill"><div class="label">FIRST STAY</div><div class="charge">COMMISSION</div></div><div class="bill second"><div class="label">RETURNING GUEST</div><div class="charge">COMMISSION</div><div class="stamp">SAME CHARGE</div></div></div>'
            motion += [f'tl.fromTo("#s{i} .second",{{y:100,opacity:0}},{{y:0,opacity:1,duration:.35,ease:"power3.out"}},{start});',f'tl.fromTo("#s{i} .stamp",{{scale:1.35,opacity:0}},{{scale:1,opacity:1,duration:.2,ease:"power2.out"}},{start+1.4});']
        elif kind in ('recognition','question'):
            title='She knows him by name.' if kind=='recognition' else 'Who gets paid<br>to stop it?'
            body=f'<h1 class="film-head">{title}</h1>'
            left = -830 if kind=='recognition' else -430
            portrait=OUT/'assets'/f'portrait-{i}.mp4'
            subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-ss',f'{src:.9f}','-i',str(CARRIER),'-t',f'{d:.9f}','-an','-vf',f'scale=1992:1120,crop=1080:1120:{-left}:0','-r','24','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(portrait)],check=True)
            videos.append(f'<video id="v{i}" class="clip" style="position:absolute;top:390px;left:0;width:1080px;height:1120px;z-index:2" src="assets/portrait-{i}.mp4" data-start="{start:.9f}" data-duration="{d:.9f}" data-media-start="0" data-track-index="2" muted playsinline></video>')
        else:
            body='<h1 class="headline">Inside that<br><em>second commission…</em></h1><div class="hero"><div class="service-word">A service?</div><div class="service-arrow">↓</div><div class="unanswered">What could the inn<br>pay someone to fix?</div></div>'
            motion += [f'tl.fromTo("#s{i} .service-word",{{y:25,opacity:0}},{{y:0,opacity:1,duration:.25,ease:"power2.out"}},{start});',f'tl.fromTo("#s{i} .unanswered",{{y:25,opacity:0}},{{y:0,opacity:1,duration:.25,ease:"power2.out"}},{start+2.1});']
        bodies.append(tag(body,i,start,d))
        group=[]
        for j,w in enumerate(subset):
            group.append(w)
            if len(group)>=5 or w['token'].endswith(('.', '?','!')) or j==len(subset)-1:
                gstart=start+max(0,group[0]['start']-src-.035)
                next_start=subset[j+1]['start'] if j+1<len(subset) else f1/FPS
                gend=min(start+d,start+(group[-1]['end']+next_start)/2-src)
                captions.append({'start':gstart,'end':gend,'text':' '.join(x['token'] for x in group),'word_ids':[x['w_id'] for x in group]})
                group=[]
        cursor+=f1-f0
    for k in range(1,len(captions)):
        captions[k]['start']=max(captions[k]['start'],captions[k-1]['end'])
    # One concatenated PCM track removes double-discovery and rounding at sentence seams.
    voice=OUT/'assets/trailer-voice.wav'
    filters=[]
    for i,(a,b,*_) in enumerate(CUTS):
        filters.append(f'[0:a]atrim=start={a/FPS:.9f}:end={b/FPS:.9f},asetpts=PTS-STARTPTS[a{i}]')
    filters.append(''.join(f'[a{i}]' for i in range(len(CUTS)))+f'concat=n={len(CUTS)}:v=0:a=1[out]')
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(CARRIER),'-filter_complex',';'.join(filters),'-map','[out]','-c:a','pcm_s16le',str(voice)],check=True)
    audio=[f'<audio id="voice" src="assets/trailer-voice.wav" data-start="0" data-duration="{cursor/FPS:.9f}" data-track-index="10"></audio>']
    spoken=cursor/FPS; end_d=2.25; total=spoken+end_d
    bodies.append(tag('<div class="label" style="position:absolute;left:72px;top:200px">THE QUESTION CONTINUES</div><h1 class="headline">What did that<br>second stay<br>actually cost?</h1><div class="cta">The calculation + the service<br>in the full episode<span>EP009 · TAP THE RELATED VIDEO →</span></div>',5,spoken,end_d,'scene end'))
    caps=''.join(f'<p id="c{i}" class="clip caption" data-caption-layer="fg" data-start="{c["start"]:.9f}" data-duration="{c["end"]-c["start"]:.9f}" data-track-index="20">{html.escape(c["text"])}</p>' for i,c in enumerate(captions))
    doc=f'<!doctype html><html><head><meta charset="utf-8"><title>EP009 · The second commission</title><script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script><style>{CSS}</style></head><body><main id="root" data-composition-id="main" data-start="0" data-duration="{total:.9f}" data-width="1080" data-height="1920" data-fps="24">'+''.join(bodies)+''.join(videos)+''.join(audio)+caps+f'<div id="brand" class="clip brand" data-start="0" data-duration="{spoken:.9f}">THE OPERATOR ECONOMY · EP009</div><div id="context" class="clip context" data-start="0" data-duration="{spoken:.9f}">An illustrative small-inn story</div></main><script>const tl=gsap.timeline({{paused:true}});'+'window.__timelines={main:tl};tl.seek(0);</script></body></html>'
    (OUT/'compositions').mkdir(exist_ok=True)
    for i,body in enumerate(bodies):
        found=re.search(r'data-start="([^"]+)" data-duration="([^"]+)"',body)
        start,duration=found.groups()
        inner=re.sub(r'data-start="[^"]+" data-duration="[^"]+" data-track-index="1"',f'data-composition-id="s{i}" data-start="0" data-duration="{duration}" data-width="1080" data-height="1920"',body,count=1)
        comp_css=CSS.replace('.scene{',f'#s{i}{{').replace('.end',f'#s{i}' if i==5 else '.unused-end')
        local_motion=[]
        for line in motion:
            if f'"#s{i} ' in line:
                match=re.search(r',([0-9.]+)\);$',line)
                local_motion.append(line[:match.start(1)]+str(max(0,float(match.group(1))-float(start)))+line[match.end(1):])
        comp=f'<!doctype html><html><body><template><style>{comp_css}</style>{inner}<script>const tl=gsap.timeline({{paused:true}});'+''.join(local_motion)+f'window.__timelines=window.__timelines||{{}};window.__timelines["s{i}"]=tl;</script></template></body></html>'
        (OUT/'compositions'/f'scene-{i}.html').write_text(comp)
        host=f'<div id="host-{i}" class="clip scene" data-composition-id="s{i}" data-composition-src="compositions/scene-{i}.html" data-start="{start}" data-duration="{duration}" data-track-index="1"></div>'
        doc=doc.replace(body,host)
    (OUT/'index.html').write_text(doc)
    assertions=[]
    for i,e in enumerate(edl):
        assertions.append({'kind':'appearsBy','selector':f'#host-{i}','bySec':e['timeline_in_frame']/24+.1})
    (OUT/'index.motion.json').write_text(json.dumps({'duration':total,'assertions':assertions},indent=2))
    (OUT/'captions.json').write_text(json.dumps(captions,indent=2)+'\n')
    contract={'schema':'oe-episode-hook-v2','status':'private_review_candidate','source':{'path':str(CARRIER.relative_to(REPO)),'sha256':EXPECTED},'transcript':{'path':str(WORDS.relative_to(REPO)),'sha256':digest(WORDS)},'final_lock':{'path':str(LOCK.relative_to(REPO)),'sha256':digest(LOCK)},'edl':edl,'spoken_duration':spoken,'cta_duration':end_d,'duration':total,'fps':FPS,'frame_count':cursor+54,'payoff':'The same returning guest triggers a second commission.','withheld':'The four-number calculation, recoverable share, price ceiling and outside service.','related_video':{'required':True,'attached':False,'target_episode':'EP009 r8','url':None,'authority':'Correct current launch/links.json only; legacy record is not this master.'},'review_approved':False,'publication_approved':False}
    (OUT/'source-contract.json').write_text(json.dumps(contract,indent=2)+'\n')
    (OUT/'meta.json').write_text(json.dumps({'id':'ep009-hook-01','name':'The second commission — episode hook'}))
    (OUT/'BRIEF.md').write_text(f'''---
workflow: general-video
flow: automation
storyboard: no
destination: youtube-shorts
aspect: 1080x1920
length: {total:.3f}s
---

## Intent
Immediate repeat-commission anomaly, one clear finding, unanswered service/economic question, explicit EP009 handoff. User requested Cleo Abram storytelling mechanics; retain OE voice and Boundary Ledger identity. Exact source phrases; no newly generated speech.

## Assets
Owner-locked r8 media and word transcript; native portrait graphics. Full master and SHORTS-001 preserved.

## Customizations
Full-height portrait proof, short 64px captions, fast motivated reveals, original avatar gestures on exact speech, final 2.25-second handoff. Private review MP4 needed to assess actual timing and audio. No final release approval.
''')
    (OUT/'STORYBOARD.md').write_text('# The second commission\n\n'+'\n\n'.join(f'## Beat {e["id"]+1}: {e["visual"]}\n\n{e["text"]}\n\nSource [{e["source_in_frame"]}, {e["source_out_frame_exclusive"]}); starts {e["timeline_in_frame"]/24:.3f}s. Cut motivates a new fact; word timing drives graphic reveals.' for e in edl)+'\n\n## Close\n\nHold unanswered cost question and related-video instruction for 2.25s. Related video must be bound to the exact episode before release.\n')
    print(json.dumps({'project':str(OUT),'duration':total,'spoken':spoken,'captions':len(captions)}))

if __name__=='__main__': main()
