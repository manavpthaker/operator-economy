#!/usr/bin/env python3
"""Upload the two authorized inputs once and verify exact bytes from fal CDN."""
import hashlib
import json
import urllib.parse
import urllib.request

import fal_benchmark as benchmark

manifest_path = benchmark.HERE/'media-uploads.json'
manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
plan = json.loads(benchmark.PLAN.read_text())

for name, mime in (('image','image/png'), ('audio','audio/wav')):
    item = plan['inputs'][name]
    raw = (benchmark.BASE/item['path']).read_bytes()
    if hashlib.sha256(raw).hexdigest()!=item['sha256']:
        raise ValueError('Source hash changed: '+name)
    if name in manifest:
        if manifest[name].get('status')=='verified' and manifest[name]['sha256']==item['sha256']:
            print(json.dumps({'input':name,'status':'already_verified'}))
            continue
        raise ValueError('Inspect existing upload before retrying: '+name)
    manifest[name] = {'status':'initiating','sha256':item['sha256'],
                      'source_path':item['path'],'bytes':len(raw),'created_at':benchmark.now()}
    benchmark.write(manifest_path,manifest)
    try:
        ack = benchmark.request('https://rest.fal.ai/storage/upload/initiate?storage_type=fal-cdn-v3',
              'POST',{'content_type':mime,'file_name':name+'-'+item['sha256'][:12]+('.png' if name=='image' else '.wav')})
        upload = urllib.parse.urlsplit(ack['upload_url'])
        output = urllib.parse.urlsplit(ack['file_url'])
        if upload.scheme!='https' or output.scheme!='https':
            raise ValueError('Provider returned a non-HTTPS storage URL')
        manifest[name].update(status='uploading',file_url=ack['file_url'],upload_host=upload.hostname)
        benchmark.write(manifest_path,manifest)
        # Signed upload URL carries its own authority. Never forward FAL_KEY.
        request = urllib.request.Request(ack['upload_url'],data=raw,method='PUT',
                                          headers={'Content-Type':mime})
        opener = urllib.request.build_opener(benchmark.NoRedirect())
        with opener.open(request,timeout=60) as response:
            response.read()
        with opener.open(ack['file_url'],timeout=60) as response:
            returned = response.read(len(raw)+1)
        if hashlib.sha256(returned).hexdigest()!=item['sha256']:
            raise ValueError('Uploaded byte hash mismatch: '+name)
        manifest[name].update(status='verified',verified_at=benchmark.now())
        benchmark.write(manifest_path,manifest)
        print(json.dumps({'input':name,'status':'verified','bytes':len(raw),'sha256':item['sha256']}))
    except Exception as error:
        manifest[name].update(status='upload_requires_inspection',error_type=type(error).__name__)
        if hasattr(error,'code'):
            manifest[name]['http_status']=error.code
        benchmark.write(manifest_path,manifest)
        print(json.dumps({'input':name,'status':manifest[name]['status'],
                          'error_type':type(error).__name__,'http_status':getattr(error,'code',None)}))
        raise SystemExit(1)
