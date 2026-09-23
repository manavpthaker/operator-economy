#!/usr/bin/env python3
"""Record verified local output and explicit remaining generation boundary."""
from pathlib import Path
import hashlib,json,urllib.request
ROOT=Path(__file__).resolve().parents[5]
EXP=ROOT/'blueprint-cinema/experiments/EP007-NET-NEW-UNFINISHED-ANSWER-003'
D=Path(__file__).resolve().parent
H=EXP/'hyperframes/reviews/r67-s22-plan'
C=EXP/'hyperframes/reviews/r67-s22-context'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rel(p):return str(p.relative_to(ROOT))
def save(p,v):p.write_text(json.dumps(v,indent=2)+'\n')
http=[]
for url,headers in [('http://100.101.49.30:3099/',{}),('http://100.101.49.30:3099/qa/context.mp4',{'Range':'bytes=0-1023'})]:
 with urllib.request.urlopen(urllib.request.Request(url,headers=headers)) as r:
  http.append({'url':url,'status':r.status,'content_type':r.headers.get('Content-Type'),'content_range':r.headers.get('Content-Range')})
  r.read(1024)
assert [r['status'] for r in http]==[200,206]
save(C/'qa/HTTP-REVIEW.json',{'checks':http})
save(C/'qa/LIVE-REVIEW.json',{'method':'Chrome browser controlled through cua_repl.',
 'observed':['Review page displayed S21 locked and S22 timing-plan status.','S22 starts button clicked.','Later live screenshot showed Take B with reference-only label and clear card text.'],
 'limits':['No claim of uninterrupted human viewing or auditory review.','A read-only video-property query timed out; playback evidence is the visible rendered frame, not browser media-state metrics.'],
 'marked_deliverable':True,'url':'http://100.101.49.30:3099/'})
q=json.loads((H/'qa/VERIFICATION.json').read_text())
assert sha(H/'index.html')==q['source_sha256']
paths=[H/'index.html',H/'qa/VERIFICATION.json',H/'qa/check.json',H/'qa/encoded-contact.png',C/'index.html',C/'qa/HTTP-REVIEW.json',C/'qa/LIVE-REVIEW.json',D/'DIRECTION-v2.md',D/'SOURCE-PINS.json',
 ROOT/'blueprint-cinema/episodes/EP007-exit-readiness-prep/agents/deliverables/R67-S22-FOOTAGE-AUDIT/report.md',
 ROOT/'blueprint-cinema/episodes/EP007-exit-readiness-prep/agents/deliverables/R67-S22-FOOTAGE-AUDIT/plan-critique.md',
 ROOT/'blueprint-cinema/episodes/EP007-exit-readiness-prep/agents/deliverables/R67-S22-TIMING/plan-review.md']
event={'event_id':'r67-s22-timing-plan-verified-v2','decision_id':'s22-table-callback','event_type':'verification',
 'tags':['film','timing-plan','local-review','technical-review'],
 'data':{'decision_event_id':'r67-s22-table-callback-plan-v2',
 'method':'Independent source inventory and timing audits; strict HyperFrames0.8.46 check; exact narration PCM; full716-frame context decode/blank scan; audio alignment/level; encoded contact sheet; live Chrome rendered label inspection; HTTP200/range206.',
 'result':'pass','scope':'S22 timing animatic only:524frames21.833333s plus192frames8s locked S21 tail.',
 'limitations':'New takes are not generated. S22 direction/spending/footage acceptance remains pending. Static reference images explicitly label absent actions. Audio checks are technical, not a listening verdict. No canonical conform or release. No paid calls.',
 'artifact_hashes':[{'path':q[k]['path'],'sha256':q[k]['sha256']} for k in ['scene','context']]},
 'evidence':[{'path':rel(p),'sha256':sha(p),'locator':'Current local plan review evidence'} for p in paths]}
save(D/'VERIFICATION-EVENT.json',event)
print(json.dumps({'http_statuses':[r['status'] for r in http],'source_hash_current':True,'paid_calls':0}))

