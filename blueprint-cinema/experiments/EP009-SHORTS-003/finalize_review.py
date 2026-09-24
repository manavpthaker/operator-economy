#!/usr/bin/env python3
from pathlib import Path
import hashlib,json,datetime
R=Path(__file__).resolve().parent;REPO=R.parents[2]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
package=json.loads((R/'REVIEW-PACKAGE.json').read_text());assert len(package['candidates'])==4
phone=json.loads((R/'PHONE-PLAYBACK-QA.json').read_text());assert len(phone['videos'])==4 and all(x['ended'] and x['media_error'] is None for x in phone['videos'])
items=[]
for c in package['candidates']:
 p=REPO/c['video']['path'];assert sha(p)==c['video']['sha256'];check=R/c['check'];j=json.loads(check.read_text());assert j['ok'] and j['motion']['enabled'];folder=R/c['slug'];qa=folder/'QA.json';sc=folder/'source-contract.json'
 items.append({**c,'check_sha256':sha(check),'source_contract_sha256':sha(sc),'qa_sha256':sha(qa)})
build={'status':'private_review_ready','direction_event':'ep009-shorts-avatar-forward-r3-directed','created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'candidates':items,'locked_master_preservation':json.loads((R/'LOCK-PRESERVATION.json').read_text()),'phone_playback':phone,'owner_acceptance':False,'published':False,'related_video_bound':False,'limitations':['Source-specific portrait framing removes outer landscape edges; original timing and matching expressions/gestures preserved.','Browser playback verification and source comparisons do not replace owner judgment of pacing and performance.','Exact new EP009 release must be attached as Related Video before publication.']}
(R/'BUILD.json').write_text(json.dumps(build,indent=2)+'\n')
artifacts=[c['video'] for c in items]
evidence=[]
for f,loc in [('BUILD.json','Exact output hashes, checks, limitations and master preservation.'),('PHONE-PLAYBACK-QA.json','Phone viewport playback reached end on all four without media errors.'),('REVIEW-PACKAGE.json','Private Tailscale page and four playable candidate bindings.')]:evidence.append({'path':str((R/f).relative_to(REPO)),'sha256':sha(R/f),'locator':loc})
event={'event_id':'ep009-shorts-avatar-forward-r3-review-verified','decision_id':'ep009-shorts-episode-hook-direction','event_type':'verification','tags':['shorts','avatar-forward','r3','private-review'],'data':{'decision_event_id':'ep009-shorts-avatar-forward-r3-directed','scope':'Four new portrait derivatives; full locked episode unchanged.','artifact_hashes':artifacts,'method':'HyperFrames checks with motion/frame checks, exact source-frame maps and PCM comparisons, actual encoded frame inspection, HTTP range requests and unmuted normal-speed browser playback at390x844.','result':'pass','limitations':'Technical/private-review verification only. Owner creative acceptance and release approval remain pending; Related Video target is unbound.'},'evidence':evidence}
(R/'VERIFICATION-EVENT.json').write_text(json.dumps(event,indent=2)+'\n')
print(json.dumps({'status':build['status'],'outputs':len(items),'sha256':sha(R/'BUILD.json')}))
