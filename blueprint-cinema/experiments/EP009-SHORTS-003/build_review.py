#!/usr/bin/env python3
"""Package completed, playable local hook previews on the existing private review host."""
from pathlib import Path
import hashlib, html, json, os, subprocess

ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[2]
QA=REPO/'blueprint-cinema/experiments/EP009-FULL-BUILD-001/assembly/qa/ep009-shorts-r3'
TITLES={
 '01-second-commission':('01','The second commission','The same guest brings another commission.','What did that second stay cost, and who could get paid to prevent it?'),
 '02-cheap-tools':('02','Cheap tools. Paid work?','The tools can draft; the service still has to earn its fee.','What work would an inn pay for?'),
 '03-guest-relationship':('03','Who owns the second booking?','The inn serves the guest; the booking site keeps the email.','Who is paid to bring that guest back directly?'),
 '04-wrong-number':('04','The wrong number','The big annual commission bill is not the recoverable opportunity.','What can a recovery service shift, and what could the inn afford?'),
}

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    inputs=json.loads((ROOT/'REVIEW-INPUTS.json').read_text())
    QA.mkdir(parents=True,exist_ok=True); (QA/'videos').mkdir(exist_ok=True); (QA/'posters').mkdir(exist_ok=True)
    cards=[]; candidates=[]
    for slug in ['01-second-commission','02-cheap-tools','03-guest-relationship','04-wrong-number']:
        if slug not in inputs: continue
        n,title,payoff,gap=TITLES[slug]
        v=ROOT/inputs[slug]['video']; assert v.exists(),v
        probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(v)]))
        stream=next(s for s in probe['streams'] if s['codec_type']=='video')
        assert (stream['width'],stream['height'])==(1080,1920)
        duration=float(probe['format']['duration'])
        target=QA/'videos'/f'short-{n}.mp4'
        if target.is_symlink():
            assert target.resolve()==v.resolve(), 'Refusing to overwrite different review media'
        elif target.exists(): raise RuntimeError(f'Existing nonsymlink {target}')
        else: target.symlink_to(os.path.relpath(v,target.parent))
        poster=QA/'posters'/f'short-{n}.jpg'
        subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-ss','0.4','-i',str(v),'-frames:v','1','-q:v','3',str(poster)],check=True)
        cards.append(f'''<article class="card" id="short-{n}"><div class="meta">SHORT {n} <span>{duration:.1f} seconds</span></div><h2>{html.escape(title)}</h2><video id="video-{n}" controls playsinline preload="metadata" poster="posters/short-{n}.jpg"><source src="videos/short-{n}.mp4" type="video/mp4"></video><div class="notes"><p><b>The insight</b> {html.escape(payoff)}</p><p><b>The episode answers</b> {html.escape(gap)}</p><a href="videos/short-{n}.mp4">Open video full screen ↗</a></div></article>''')
        candidates.append({'id':n,'slug':slug,'title':title,'duration':duration,'video':{'path':str(v.relative_to(REPO)),'sha256':sha(v)},'check':inputs[slug]['check'],'width':1080,'height':1920,'frame_count':int(stream['nb_frames']),'owner_approved':False})
    document='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><title>EP009 · Avatar-forward Shorts</title><style>
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:#F5F0E6;color:#173530;font:16px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}main{max-width:1060px;margin:auto;padding:40px 22px 90px}header{max-width:770px;margin-bottom:30px}.eyebrow{font-size:12px;letter-spacing:.14em;font-weight:700;color:#586D74}h1{font:600 clamp(38px,7vw,68px)/1.02 Georgia,serif;letter-spacing:-.04em;margin:20px 0}header p{font-size:18px;max-width:660px}nav{display:flex;gap:10px;flex-wrap:wrap;margin-top:24px}nav a{color:inherit;text-decoration:none;border:1px solid #C4B99E;padding:10px 15px;border-radius:4px;background:#FBF8F1}nav a:hover{border-color:#B5482F}.grid{display:grid;grid-template-columns:1fr 1fr;gap:24px}.card{background:#FBF8F1;border:1px solid #D8CFB9;padding:18px;border-radius:8px;scroll-margin-top:20px}.meta{display:flex;justify-content:space-between;color:#586D74;font-size:12px;letter-spacing:.07em}h2{font:600 28px/1.12 Georgia,serif;letter-spacing:-.025em;margin:13px 0 19px}video{display:block;width:100%;aspect-ratio:9/16;object-fit:contain;background:#111713;border-radius:3px}.notes{font-size:14px;line-height:1.45}.notes p{margin:18px 0}.notes b{display:block;font-size:11px;text-transform:uppercase;letter-spacing:.09em;color:#586D74;margin-bottom:5px}a{color:#A3422C}footer{margin-top:32px;max-width:740px;font-size:13px;color:#586D74}.tip{padding-left:15px;border-left:3px solid #B5482F}@media(max-width:650px){main{padding:28px 16px 65px}.grid{grid-template-columns:1fr;gap:24px}.card{padding:14px}header p{font-size:16px}h2{font-size:26px}nav{gap:7px}nav a{padding:9px 11px}.notes{font-size:15px}}
</style></head><body><main><header><div class="eyebrow">THE OPERATOR ECONOMY · EP009 · SHORTS R3</div><h1>Four ways into<br>the full episode.</h1><p>You lead each Short: the opening, the explanation, and the unanswered question. Brief proof inserts support the point. The original voice and matching avatar performance are preserved.</p><p class="tip">Avatar-forward revision. Play with sound; each ending points into the full episode.</p><nav><a href="#short-01">01 · The repeat fee</a><a href="#short-02">02 · The tools</a><a href="#short-03">03 · The guest</a><a href="#short-04">04 · The number</a></nav></header><div class="grid">'''+''.join(cards)+'''</div><footer>Private review · These Shorts are awaiting your review. The full episode remains locked. The “related video” prompt will connect to the exact episode when its YouTube release is prepared; nothing has been uploaded.<p><a href="../ep009-r8-review.html">Open the locked full-episode review ↗</a></p></footer></main><script>document.querySelectorAll('video').forEach(v=>v.addEventListener('play',()=>document.querySelectorAll('video').forEach(other=>{if(other!==v)other.pause()})));</script></body></html>'''
    if len(candidates)<4:
        document=document.replace('Avatar-forward revision. Play with sound; each ending points into the full episode.',f'{len(candidates)} of 4 playable previews are ready. The remaining cuts are being checked and rendered.')
        for n in ['01','02','03','04']:
            if n not in [c['id'] for c in candidates]:
                import re
                document=re.sub(f'<a href="#short-{n}">.*?</a>','',document)
    (QA/'index.html').write_text(document)
    (ROOT/'REVIEW-PACKAGE.json').write_text(json.dumps({'status':'private_playable_review_ready' if len(candidates)==4 else 'partial_private_review','page':str((QA/'index.html').relative_to(REPO)),'page_sha256':sha(QA/'index.html'),'candidates':candidates,'longform_locked':True,'shorts_owner_approved':False,'published':False},indent=2)+'\n')
    print(json.dumps(candidates,indent=2))

if __name__=='__main__': main()
