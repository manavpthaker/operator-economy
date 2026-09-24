#!/usr/bin/env python3
"""Bounded Seedance 2.5 comparison; credentials remain in the existing private reader."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import urllib.error
import urllib.request

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
spec = importlib.util.spec_from_file_location('fal_transport', BASE/'repair-r23/fal_benchmark.py')
transport = importlib.util.module_from_spec(spec)
spec.loader.exec_module(transport)


def prepare(sample):
    plan = json.loads((HERE/'comparison-plan.json').read_text())
    if sample not in plan['seeds'] or len(plan['seeds']) != 2:
        raise ValueError('Outside the authorized two-sample comparison')
    price = json.loads((HERE/'seedance-price.json').read_text())['prices'][0]
    if (price['endpoint_id'] != plan['endpoint'] or price['unit_price'] != 0.0214
            or price['unit'] != '1000 tokens' or price['currency'] != 'USD'):
        raise ValueError('Price differs from verified quote')
    for item in plan['inputs'].values():
        if hashlib.sha256((BASE/item['path']).read_bytes()).hexdigest() != item['sha256']:
            raise ValueError('Fixed source input changed')
    payload = {'prompt':plan['seedance_prompt'],
               'image_urls':[plan['input_urls']['image']],
               'audio_urls':[plan['input_urls']['audio']],
               **plan['parameters'], 'seed':plan['seeds'][sample]}
    schema = json.loads((HERE/'seedance-openapi.json').read_text())['components']['schemas']['Seedance25ReferenceToVideoInput']
    if set(payload)-set(schema['properties']) or set(schema['required'])-set(payload):
        raise ValueError('Unsupported or missing request field')
    for key, value in payload.items():
        field = schema['properties'][key]
        if 'enum' in field and value not in field['enum']:
            raise ValueError('Unsupported value: '+key)
    return plan, payload


def submit(sample):
    plan, payload = prepare(sample)
    path = HERE/(sample+'.json')
    if path.exists():
        raise ValueError('Submission record exists; inspect instead of resubmitting')
    if sample == 'seedance-02':
        first = json.loads((HERE/'seedance-01.json').read_text())
        if not first.get('result',{}).get('video',{}).get('url'):
            raise ValueError('First sample must return media before the second submission')
    record = {'sample':sample,'endpoint':plan['endpoint'],'status':'submitting',
              'created_at':transport.now(),'inputs':plan['inputs'],'parameters':payload,
              'request_sha256':hashlib.sha256(json.dumps(payload).encode()).hexdigest(),
              'estimated_usd':plan['pricing']['estimated_pair_usd']/2,
              'owner_accepted':False,'productionGateAdvance':False}
    transport.write(path, record)
    try:
        ack = transport.request('https://queue.fal.run/'+plan['endpoint'],'POST',payload)
        record.update(status=ack.get('status','IN_QUEUE'),ack=ack)
    except urllib.error.HTTPError as error:
        record.update(status='submission_http_error',http_status=error.code,error=transport.error_body(error))
    except Exception as error:
        record.update(status='submission_outcome_unknown',error_type=type(error).__name__)
    record['updated_at'] = transport.now()
    transport.write(path,record)
    print(json.dumps({'sample':sample,'status':record['status'],
                      'request_id':record.get('ack',{}).get('request_id'),
                      'http_status':record.get('http_status'),'error':record.get('error')}))


def poll():
    for sample in ('seedance-01','seedance-02'):
        path = HERE/(sample+'.json')
        if not path.exists():
            print(json.dumps({'sample':sample,'status':'not_submitted'})); continue
        record = json.loads(path.read_text())
        if record.get('ack') and not record.get('result') and record['status'] != 'FAILED':
            try:
                status = transport.request(record['ack']['status_url'])
                record.update(status=status['status'],last_status=status,updated_at=transport.now())
                if status['status'] == 'COMPLETED':
                    record['result'] = transport.request(record['ack']['response_url'])
            except urllib.error.HTTPError as error:
                record.update(last_read_http_status=error.code,last_read_error=transport.error_body(error))
                if record.get('last_status',{}).get('status') == 'COMPLETED':
                    record['status'] = 'FAILED'
            transport.write(path,record)
        print(json.dumps({'sample':sample,'status':record['status'],
                          'result':record.get('result'),'error':record.get('last_read_error')}))


def archive():
    folder = BASE/'media/repair-r24'
    folder.mkdir(parents=True,exist_ok=True)
    index_path = HERE/'native-outputs.json'
    index = json.loads(index_path.read_text()) if index_path.exists() else {}
    for sample in ('seedance-01','seedance-02'):
        record_path = HERE/(sample+'.json')
        if not record_path.exists(): continue
        record = json.loads(record_path.read_text())
        url = record.get('result',{}).get('video',{}).get('url')
        if not url: continue
        target = folder/(sample+'.mp4')
        if target.exists():
            if sample not in index or hashlib.sha256(target.read_bytes()).hexdigest() != index[sample]['sha256']:
                raise ValueError('Existing output needs inspection')
            continue
        if not url.startswith('https://'): raise ValueError('Output URL must use HTTPS')
        # Native generated media is archived for QA and provenance; no credential is sent.
        with urllib.request.urlopen(url,timeout=60) as response:
            raw = response.read(100*1024*1024+1)
        if len(raw)>100*1024*1024 or raw[4:8] != b'ftyp':
            raise ValueError('Unexpected output format or size')
        target.write_bytes(raw)
        index[sample] = {'path':str(target),'sha256':hashlib.sha256(raw).hexdigest(),
                         'source_url':url,'request_id':record['ack']['request_id'],
                         'model':'Seedance 2.5','native_untouched':True,
                         'audio_preservation':'unverified','owner_accepted':False}
        transport.write(index_path,index)
        print(json.dumps({'sample':sample,**index[sample]}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('action',choices=['prepare','submit','poll','archive'])
    parser.add_argument('--sample',choices=['seedance-01','seedance-02'])
    args = parser.parse_args()
    if args.action == 'prepare':
        for sample in ('seedance-01','seedance-02'):
            plan,payload = prepare(sample)
            print(json.dumps({'sample':sample,'fields':list(payload),'valid':True,'submitted':False}))
    elif args.action == 'submit': submit(args.sample)
    elif args.action == 'poll': poll()
    else: archive()
