#!/usr/bin/env python3
from pathlib import Path
import datetime,hashlib,json
D=Path(__file__).resolve().parent
ROOT=D.parents[4]
EXP=ROOT/'blueprint-cinema/experiments/EP007-NET-NEW-UNFINISHED-ANSWER-003'
P=EXP/'hyperframes/reviews/r68-s22-film/provider'
OLD=EXP/'direction/r67-s22-table-callback'
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rel(p):return str(p.relative_to(ROOT))
def save(p,v):p.write_text(json.dumps(v,indent=2)+'\n')
quote="this is fine but there is no indication that the buyer is seeing something he likes. they're not pointing at anything and theres nothing on the page"
save(D/'OWNER-REQUEST.json',{'verbatim':quote,'recorded_at_utc':now,'source':'Current conversation user message responding to the two-take $2.25-cap approval question.',
 'interpretation':'Approve the bounded batch with required visible page content, pointing and positive buyer response. No expansion or retries; no unseen output accepted.'})
model='fal-ai/kling-video/v3/pro/image-to-video'
seed=EXP/'direction/r52-walkout/start-frame-establishing-0360.png'
assert sha(seed)=='2d12bb1caa75e9d87e2422155d3793597f168a53d6e55601d3d56c66fe257ca5'
for name,seconds,frames in [('A',8,170),('B',11,236)]:
 req={'model':model,'revision':'R68 owner-requested buyer response','input':{'prompt':(D/f'TAKE-{name}-PROMPT.txt').read_text().strip(),'duration':str(seconds),'generate_audio':False,'cfg_scale':.5},
 'selected_slot_frames':frames,'fps':24,'automatic_retries':0}
 if name=='A':req.update(local_start_image=rel(seed),start_image_sha256=sha(seed))
 else:req['seed_rule']='Extract from accepted usable state in generated take A after binder is open, record visibly populated, and owner hand is clear. Bind frame and hashes in take-b/SEED.json before submission.'
 save(D/f'TAKE-{name}.request.json',req)
cost={'model':model,'rate_usd_per_second_audio_off':.112,'price_checked_utc':now,'source':'https://fal.ai/models/fal-ai/kling-video/v3/pro/image-to-video',
 'take_a_seconds':8,'take_b_seconds':11,'estimate_usd':2.128,'cap_usd':2.25,'max_requests':2,'automatic_retries':0}
save(D/'COST.json',cost)
auth={'record_type':'generation_authorization','recorded_at_utc':now,'owner_statement':quote,
 'source':'Current conversation; reply to explicit two-take fal.ai $2.25-cap request.',
 'interpretation':'The owner accepts the bounded proposal with required corrections. Execute exactly the same two takes with populated record, specific pointing and positive acknowledgment.',
 'caps':{'fal_total_usd':2.25,'requests':2,'automatic_retries':0},
 'scope':'S22 only; exactly one8s A and one11s B, audio off; B conditional on A passing. Necessary synthetic reference uploads only.',
 'bound_requests':{n:{'path':rel(D/f'TAKE-{n}.request.json'),'sha256':sha(D/f'TAKE-{n}.request.json')} for n in ['A','B']},
 'bound_direction':{'path':rel(D/'DIRECTION.md'),'sha256':sha(D/'DIRECTION.md')},
 'bound_cost':{'path':rel(D/'COST.json'),'sha256':sha(D/'COST.json')}}
save(P/'GENERATION-AUTHORIZATION.json',auth)
prior=json.loads((OLD/'DECISION-v2.json').read_text())
feedback={'event_id':'r68-owner-s22-positive-response','decision_id':'s22-table-callback','event_type':'feedback','tags':['owner-feedback','film','caused-reaction'],
 'data':{'decision_event_id':prior['event_id'],'actor':'owner','verbatim':quote,'interpretation':auth['interpretation'],
 'verdict':'revise','scope':'S22 direction and bounded two-take generation; no footage acceptance.',
 'artifact_hashes':[{'path':rel(OLD/'DIRECTION-v2.md'),'sha256':sha(OLD/'DIRECTION-v2.md')}]},
 'evidence':[{'path':rel(D/'OWNER-REQUEST.json'),'sha256':sha(D/'OWNER-REQUEST.json'),'locator':'Current owner feedback'}]}
prior['event_id']='r68-s22-buyer-response-v1';prior['supersedes']='r67-s22-table-callback-plan-v2'
prior['tags']=['film','caused-reaction','pointing','populated-record']
prior['data']['choice']='Owner opens and identifies a populated record; buyer points to the entry, checks it and gives a small approving acknowledgment.'
prior['data']['reason']='Owner requires visible contents and a positive response caused by a specific answer; prior neutral observation underplays the payoff.'
prior['data']['alternatives']=[{'choice':'Neutral reading only','reason_not_selected':'Owner explicitly found no indication the buyer likes what he sees.'},{'choice':'Handshake or transaction result','reason_not_selected':'The requested positive response concerns the answer, not a sale.'}]
prior['data']['nuance']['authorization']=auth['interpretation']
prior['data']['nuance']['source_basis']='Current owner feedback; positive acknowledgment replaces earlier agent-imposed no-nod/no-point constraints.'
prior['data']['nuance']['performance']='A opens populated binder and points once. B places fingertip by same row, reads, gives one small approving nod/faint smile, resumes reading.'
prior['evidence']=[{'path':rel(f),'sha256':sha(f),'locator':'Current direction/request authority'} for f in [D/'DIRECTION.md',D/'TAKE-A.request.json',D/'TAKE-B.request.json',P/'GENERATION-AUTHORIZATION.json']]
save(D/'EVENTS.json',[feedback,prior])
print(json.dumps({'requests_prepared':2,'cap_usd':2.25,'paid_calls':0}))

