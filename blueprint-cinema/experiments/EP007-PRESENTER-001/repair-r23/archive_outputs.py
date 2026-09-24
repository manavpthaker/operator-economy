#!/usr/bin/env python3
"""Archive native generated media for provenance and QA, without transcoding."""
import hashlib
import json
import urllib.parse
import urllib.request

import fal_benchmark as benchmark

folder = benchmark.BASE/'media/repair-r23'
folder.mkdir(parents=True,exist_ok=True)
manifest_path = benchmark.HERE/'native-outputs.json'
manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
plan = json.loads(benchmark.PLAN.read_text())

for sample in plan['samples']:
    record_path = benchmark.HERE/(sample+'.json')
    record = json.loads(record_path.read_text()) if record_path.exists() else {}
    result = record.get('result') or {}
    url = result.get('video',{}).get('url')
    if not url:
        print(json.dumps({'sample':sample,'archived':False,'status':record.get('status','not_submitted')}))
        continue
    target = folder/(sample+'.mp4')
    if target.exists():
        if (sample not in manifest or
                hashlib.sha256(target.read_bytes()).hexdigest()!=manifest[sample]['sha256']):
            raise ValueError('Existing media needs inspection: '+sample)
        print(json.dumps({'sample':sample,'archived':True,'path':str(target),'already_present':True}))
        continue
    if urllib.parse.urlsplit(url).scheme!='https':
        raise ValueError('Non-HTTPS output URL')
    # Output retrieval has no Authorization header or credential handling.
    with urllib.request.urlopen(url,timeout=60) as response:
        raw = response.read(100*1024*1024+1)
    if len(raw)>100*1024*1024:
        raise ValueError('Unexpectedly large five-second output')
    if len(raw)<12 or raw[4:8]!=b'ftyp':
        raise ValueError('Output is not the expected MP4 container')
    target.write_bytes(raw)
    manifest[sample] = {'sample':sample,'path':str(target),'sha256':hashlib.sha256(raw).hexdigest(),
                        'bytes':len(raw),'model':record['model'],'endpoint':record['endpoint'],
                        'request_id':record['ack']['request_id'],'source_url':url,
                        'archived_at':benchmark.now(),'native_untouched':True,
                        'source_image_sha256':record['source_image']['sha256'],
                        'source_audio_sha256':record['source_audio']['sha256'],
                        'owner_accepted':False,'full_speed_review':'pending'}
    benchmark.write(manifest_path,manifest)
    print(json.dumps({'sample':sample,'archived':True,'path':str(target),'sha256':manifest[sample]['sha256']}))
