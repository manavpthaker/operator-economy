#!/usr/bin/env python3
"""Prepare local references, exact VO and unsubmitted S22 request specifications."""
from pathlib import Path
import hashlib, json, shutil, wave
ROOT = Path(__file__).resolve().parents[5]
EXP = ROOT/'blueprint-cinema/experiments/EP007-NET-NEW-UNFINISHED-ANSWER-003'
D = Path(__file__).resolve().parent
H = EXP/'hyperframes/reviews/r67-s22-plan'
UP = ROOT/'operator-blueprint-v2/episodes/EP007-exit-readiness-prep'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def rel(p): return str(p.relative_to(ROOT))
def save(p, data): p.write_text(json.dumps(data,indent=2)+'\n')
locked = {
 UP/'01-editorial/script.md':'e56bbb80c1b3a21679a17459402130d820be285ee389fc2978ef8216d6487db0',
 UP/'02-narration-production/word-transcript.json':'f5decf2102d6cd565b89823e6fae38b2f4838c0984f7fce67f36c03cfa0f0ef7',
 UP/'02-narration-production/master/narration-master.v4.wav':'d8f7cb9630ae12ad427dca2c7bd1f29611f56c7985ce900ea312df3b9fec8da9',
 EXP/'hyperframes/reviews/r36-buyer-demand/public/media/establishing.mp4':'e0b4067004d83f4ba00be589d72ffc43d8305319a63be2217f19d594d6d2521c',
 EXP/'direction/r52-walkout/start-frame-establishing-0360.png':'2d12bb1caa75e9d87e2422155d3793597f168a53d6e55601d3d56c66fe257ca5',
}
for p,s in locked.items(): assert sha(p)==s, str(p)
for sub in ['public/audio','public/media','public/fonts','public/vendor','qa']: (H/sub).mkdir(parents=True,exist_ok=True)
wide=EXP/'hyperframes/reviews/r36-buyer-demand/public/media/establishing.mp4'
question=wide.with_name('shot-b.mp4')
seed=EXP/'direction/r52-walkout/start-frame-establishing-0360.png'
for p,name in [(wide,'establishing.mp4'),(question,'question.mp4'),(seed,'reference.png')]: shutil.copy2(p,H/'public/media'/name)
prior=EXP/'hyperframes/reviews/r66-s21-hard-part'
for folder in ['fonts','vendor']:
 for p in (prior/'public'/folder).iterdir():
  if p.is_file(): shutil.copy2(p,H/'public'/folder/p.name)
master=UP/'02-narration-production/master/narration-master.v4.wav'
with wave.open(str(master),'rb') as src:
 assert src.getframerate()==48000 and src.getnchannels()==1 and src.getsampwidth()==2
 src.setpos(25130*2000); pcm=src.readframes(524*2000)
 with wave.open(str(H/'public/audio/narration.wav'),'wb') as out:
  out.setparams(src.getparams());out.writeframes(pcm)
timing=ROOT/'blueprint-cinema/episodes/EP007-exit-readiness-prep/agents/deliverables/R67-S22-TIMING/cues.json'
shutil.copy2(timing,D/'CUES.json')
sources=list(locked)+[question,timing,
 ROOT/'blueprint-cinema/episodes/EP007-exit-readiness-prep/agents/deliverables/R67-S22-FOOTAGE-AUDIT/report.md',
 EXP/'direction/r35-buyer-seller-arc/SCENE-ARC.md']
save(D/'SOURCE-PINS.json',{'sources':[{'path':rel(p),'sha256':sha(p)} for p in sources]})
prompt_a="""One continuous eight-second locked-off tripod shot at the exact workshop table in the supplied image. Preserve these same two adults, faces, hair, glasses, tan work shirt, steel-blue overshirt, daylight, table, green binder, pencil, keys and workshop background. Owner remains seated screen-left and buyer screen-right. Camera stays fixed with no zoom, pan, orbit, drift, reframing or cuts. Natural real-time motion.

One primary action: the owner presents an already-prepared record to the buyer. The central sheet starts with its blank reverse facing up, exactly as in the reference image. Almost immediately she lifts its near edge and turns that single sheet over toward him in one smooth, matter-of-fact presentation gesture, setting it face-up within his reach. The other side already carries faint, soft rows of writing; the existing marks are revealed by the physical turn, never drawn, written or materialized on the blank face. Keep all marks too small and oblique to read, with no recognizable names, values, prices, logos or facts. Preserve one intact sheet and anatomically stable hands throughout.

Complete the unhurried gesture in roughly the first three seconds. She releases the page and returns her hand to rest; the buyer's attention follows the available page. He does not reach into her gesture. Both stay seated and attentive through the remaining handle. No hesitation or attempt to recall an answer. No writing, taking out a pencil, opening or closing the binder, retrieving another object, additional page, repeated exchange, page flip back, head shake, nod of approval, smile, handshake, celebration or closing gesture. This is quiet observation of an available written answer: no speech, lip movement or conversational pantomime. No new person, new prop, paper duplication, object morphing, teleportation, or magically appearing page contents."""
prompt_b="""One continuous eleven-second locked-off shot continuing the exact supplied frame and its settled paper position. Keep the same workshop, owner seated left in tan, buyer seated right in blue with glasses, daylight, table, green binder, pencil and keys. Preserve the existing single face-up prepared record exactly as shown. No new object or document, no new marks or text. The small oblique rows stay unreadable. Camera remains fixed: no movement, zoom, pan, orbit, reframing or cuts.

One sustained action: the buyer independently reads and checks the available record. His eyes work down the page with a small natural head adjustment. In the early portion he slowly follows one short part of the existing page with a finger once, then leaves that hand in place as he continues reading the lower part. Keep the motion restrained and at real speed, with natural breathing and occasional blinks. The owner watches quietly with both hands at rest, allowing him to use the record without her explanation. Maintain attentive inspection through the end; it is a process, not a finished decision.

No speech, lip movement, conversational gestures, question, answer, nod, smile, approval expression, handshake, signature, offer, celebration, head shake, looking back up to the owner, page turn, writing, repeated finger tracing, rhythmic gestures, frozen body, slow motion, paper duplication or object morphing. No sale verdict or closing gesture. Do not make the characters demonstrate success; simply show independent checking of the record."""
model='fal-ai/kling-video/v3/pro/image-to-video'
for name,prompt,seconds,frames in [('A',prompt_a,8,170),('B',prompt_b,11,236)]:
 (D/f'TAKE-{name}-PROMPT.txt').write_text(prompt+'\n')
 request={'status':'prepared_not_authorized_not_submitted','model':model,'picture_audio_mode':'narrated_observation',
 'input':{'prompt':prompt,'duration':str(seconds),'generate_audio':False,'cfg_scale':0.5},
 'selection':{'frames':frames,'fps':24,'source_offset':'select only after actual playback; no speed change, freeze or loop'},
 'max_requests':1,'automatic_paid_retries':False}
 if name=='A':
  request.update(local_start_image=rel(seed),start_image_sha256=sha(seed),source_frame=360,source_media=rel(wide))
 else:
  request.update(local_start_image=None,start_image_sha256=None,
   seed_dependency={'take':'A','condition':'A passes identity, single-sheet mechanics, prompt response and 170 usable frames',
   'selection_rule':'Extract a settled frame after the sheet is face-up within buyer reach and the owner has released it. Bind frame number, source and PNG hashes before upload/submission. Do not submit B if A fails.',
   'permitted_operations':['frame extraction','editorial crop preserving buyer/page/hands; no synthesis']})
 save(D/f'TAKE-{name}.request.json',request)
save(D/'COST-PROPOSAL.json',{'record_type':'proposal_not_authorization','provider':'fal.ai','model':model,
 'price_checked_date':'2026-09-17','price_source':'https://fal.ai/models/fal-ai/kling-video/v3/pro/image-to-video',
 'usd_per_second_audio_off':0.112,'take_a_seconds':8,'take_b_seconds':11,'total_seconds':19,
 'estimate_usd':2.128,'proposed_cap_usd':2.25,'max_paid_calls':2,'sequential':True,'automatic_paid_retries':0,
 'take_b_condition':'Take A passes and exact derived starting frame is bound before upload/submission.',
 'image_generation':False,'voice_generation':False,'restoration':False,'paid_calls_submitted':0,
 'scope':'S22 only. S17 is separate. Stop if current price exceeds cap.'})
event={'event_id':'r67-s22-table-callback-plan-v1','decision_id':'s22-table-callback','event_type':'decision',
 'tags':['film','callback','independent-inspection','paid-proposal'],
 'data':{'context':{'narrative_job':'Show an answer becoming independently inspectable at the original table.',
 'viewer_before':'Owner dependence makes the answer unavailable without her reconstruction.',
 'viewer_after':'An existing written record allows independent inspection; no sale result is established.'},
 'choice':'Reuse table/question, then propose separate record-presentation and buyer-inspection takes.',
 'reason':'Audited existing footage does not contain the changed record state or the independent check.',
 'alternatives':[{'choice':'Existing handshake','reason_not_selected':'Implies agreement beyond the script.'},
 {'choice':'Original blank-sheet inspection','reason_not_selected':'Does not show an available written answer.'},
 {'choice':'Owner writes now','reason_not_selected':'Contradicts no reconstruction on the spot.'}],
 'reuse':{'kind':'episode_specific','applies_when':'S22 exact narration and accepted EP007 table world.',
 'avoid_when':'A future script establishes different participants, document state or transaction outcome.'},
 'nuance':{'source_basis':'Owner locked S21 and requested move on; R35 arc plus current bounded R67 audits.',
 'cut_cues':[{'cue_id':'S22-response','phrase':'And this time','master_seconds':1052.0,'review_seconds':12.916666666666666,'fps':24,'relation':'Prompt record presentation begins.'},
 {'cue_id':'S22-inspection','phrase':'He can read it','master_seconds':1059.0833333333333,'review_seconds':20,'fps':24,'relation':'Independent inspection begins.'}],
 'authorization':'Unpaid direction and animatic only; two proposed paid takes await separate owner authorization.',
 'false_inference':'Illustrative replay, not new profit, real case evidence, later visit or sale.'}},
 'evidence':[{'path':rel(D/'DIRECTION.md'),'sha256':sha(D/'DIRECTION.md'),'locator':'Direction before implementation'},
 {'path':rel(D/'COST-PROPOSAL.json'),'sha256':sha(D/'COST-PROPOSAL.json'),'locator':'Two unsubmitted requests and cost cap'}]}
save(D/'DECISION.json',event)
print(json.dumps({'prepared':rel(D),'frames':524,'request_count':2,'paid_calls':0}))

