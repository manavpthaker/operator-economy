#!/usr/bin/env python3
"""Run the bounded EP007 fal benchmark without logging credentials or media bytes."""
import argparse
import base64
import datetime as dt
import hashlib
import json
from pathlib import Path
import re
import urllib.error
import urllib.parse
import urllib.request

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
ENV = Path('/Users/brownmanbrain/GitHub/operator-economy/.env')
PLAN = HERE / 'execution-plan.json'


def now():
    return dt.datetime.now(dt.timezone.utc).isoformat()


def write(path, obj):
    temp = path.with_suffix('.tmp')
    temp.write_text(json.dumps(obj, indent=2)+'\n')
    temp.replace(path)


def credential():
    for line in ENV.read_text().splitlines():
        match = re.match(r'^\s*(?:export\s+)?FAL_KEY\s*=\s*(.*?)\s*$', line)
        if match:
            key = match.group(1)
            if len(key)>1 and key[0] in '\"\'' and key[-1]==key[0]:
                key = key[1:-1]
            else:
                key = key.split(' #', 1)[0].strip()
            if key:
                return key
    raise ValueError('FAL_KEY missing or empty')


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def request(url, method='GET', payload=None):
    parsed = urllib.parse.urlsplit(url)
    if parsed.scheme!='https' or parsed.hostname not in ('queue.fal.run', 'api.fal.ai', 'rest.fal.ai'):
        raise ValueError('Authenticated request host is not approved')
    body = None if payload is None else json.dumps(payload).encode()
    req = urllib.request.Request(url, data=body, method=method,
        headers={'Authorization':'Key '+credential(), 'Content-Type':'application/json'})
    opener = urllib.request.build_opener(NoRedirect())
    with opener.open(req, timeout=60) as response:
        return json.load(response)


def media_input(plan, name, mime):
    item = plan['inputs'][name]
    raw = (BASE/item['path']).read_bytes()
    if hashlib.sha256(raw).hexdigest()!=item['sha256']:
        raise ValueError(name+' input hash changed')
    uploads = json.loads((HERE/'media-uploads.json').read_text())
    upload = uploads[name]
    if upload['sha256']!=item['sha256'] or upload.get('status')!='verified':
        raise ValueError('Exact-byte CDN upload not verified for '+name)
    return upload['file_url']


def error_body(error):
    raw = error.read(8000).decode('utf-8', errors='replace')
    raw = raw.replace(credential(), '[REDACTED]')
    return re.sub(r'data:[^\s\"<>]+', '[MEDIA DATA REDACTED]', raw)


def prepared(sample):
    plan = json.loads(PLAN.read_text())
    settings = plan['samples'].get(sample)
    if settings is None or len(plan['samples']) != 4:
        raise ValueError('Sample is outside the approved four-job scope')
    endpoint = settings['endpoint_id']
    prices = json.loads((HERE/settings['price_file']).read_text())['prices']
    price = next(p for p in prices if p['endpoint_id']==endpoint)
    if (price['unit']!='seconds' or price['currency']!='USD'
            or price['unit_price'] != settings['reviewed_base_unit_price_usd']):
        raise ValueError('Price differs from the reviewed quote; refresh before submitting')
    payload = {'image_url':media_input(plan,'image','image/png'),
               'audio_url':media_input(plan,'audio','audio/wav'),
               'prompt':plan['prompt'], **settings['parameters']}
    schema = json.loads((HERE/settings['schema_file']).read_text())['models'][0]['openapi']
    input_schema = schema['components']['schemas'][settings['input_schema']]
    if set(payload)-set(input_schema['properties']) or set(input_schema['required'])-set(payload):
        raise ValueError('Payload does not match the verified endpoint fields')
    for name, value in payload.items():
        rule = input_schema['properties'][name]
        if 'enum' in rule and value not in rule['enum']:
            raise ValueError('Unsupported value for '+name)
        if 'minimum' in rule and value < rule['minimum']:
            raise ValueError('Below supported minimum for '+name)
        if 'maximum' in rule and value > rule['maximum']:
            raise ValueError('Above supported maximum for '+name)
    expected = settings['reviewed_effective_unit_price_usd']*settings['budget_duration_seconds']
    return plan, settings, payload, expected


def submit(sample, retry_rejected=False, retry_failed_input=False):
    plan, settings, payload, expected = prepared(sample)
    record_path = HERE/(sample+'.json')
    prior_attempts = []
    if record_path.exists():
        previous = json.loads(record_path.read_text())
        rejected = (retry_rejected and previous.get('status')=='submission_http_error'
                    and previous.get('http_status')==403 and 'ack' not in previous)
        known_corrected_input = ('file_download_error' in previous.get('last_read_error','') or
            ('Audio is too short' in previous.get('last_read_error','')
             and payload.get('num_frames',100000) <= int(plan['inputs']['audio']['duration_seconds']*25)))
        failed_input = (retry_failed_input and previous.get('status') in ('COMPLETED','FAILED')
                        and previous.get('last_read_http_status')==422
                        and known_corrected_input
                        and not previous.get('result'))
        if not (rejected or failed_input):
            raise ValueError('Sample already has a submission record; inspect it instead of resubmitting')
        prior_attempts = previous.pop('prior_attempts', []) + [previous]
    endpoint = settings['endpoint_id']
    record = {'sample':sample,'model':settings['model'],'endpoint':endpoint,
              'status':'submitting','created_at':now(),'source_image':plan['inputs']['image'],
              'source_audio':plan['inputs']['audio'],
              'parameters':{k:v for k,v in payload.items() if not k.endswith('_url')},
              'media_transport':'Exact local bytes uploaded once to fal CDN and verified by SHA256 readback',
              'estimated_usd':expected,'seed':payload.get('seed','not exposed by this endpoint'),
              'request_sha256':hashlib.sha256(json.dumps(payload).encode()).hexdigest(),
              'authorization_basis':'Owner provided FAL_KEY location after the concrete four-sample proposal',
              'owner_accepted':False,'productionGateAdvance':False,
              'prior_attempts':prior_attempts}
    write(record_path,record)
    try:
        ack = request('https://queue.fal.run/'+endpoint, 'POST', payload)
    except urllib.error.HTTPError as error:
        body = error_body(error)
        record.update(status='submission_http_error',http_status=error.code,
                      error_body=body,updated_at=now())
        write(record_path,record)
        print(json.dumps({'sample':sample,'status':record['status'],'http_status':error.code,'body':body}))
        return
    except Exception as error:
        record.update(status='submission_outcome_unknown',error_type=type(error).__name__,updated_at=now())
        write(record_path,record)
        print(json.dumps({'sample':sample,'status':record['status'],'error_type':type(error).__name__}))
        return
    record.update(status=ack.get('status','IN_QUEUE'),ack=ack,updated_at=now())
    write(record_path,record)
    print(json.dumps({'sample':sample,'status':record['status'],'request_id':ack.get('request_id'),
                      'estimated_usd':expected}))


def poll():
    plan = json.loads(PLAN.read_text())
    for sample in plan['samples']:
        path = HERE/(sample+'.json')
        if not path.exists():
            print(json.dumps({'sample':sample,'status':'not_submitted'}))
            continue
        record = json.loads(path.read_text())
        if 'ack' not in record:
            print(json.dumps({'sample':record['sample'],'status':record['status']}))
            continue
        if record.get('result'):
            print(json.dumps({'sample':record['sample'],'status':'COMPLETED','result':record['result']}))
            continue
        ack = record['ack']
        try:
            status = request(ack['status_url'])
            record.update(status=status['status'],last_status=status,updated_at=now())
            if status['status']=='COMPLETED':
                result = request(ack['response_url'])
                record['result'] = result
        except urllib.error.HTTPError as error:
            record.update(last_read_http_status=error.code,last_read_error=error_body(error),updated_at=now())
            if record.get('last_status',{}).get('status')=='COMPLETED' and error.code==422:
                record['status']='FAILED'
        write(path,record)
        print(json.dumps({'sample':record['sample'],'status':record['status'],
                          'queue_position':record.get('last_status',{}).get('queue_position'),
                          'http_status':record.get('last_read_http_status'),
                          'result':record.get('result')}))


if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('action',choices=['prepare','submit','poll'])
    parser.add_argument('--sample')
    parser.add_argument('--retry-rejected', action='store_true',
                        help='Explicitly retry a recorded HTTP 403 with no accepted job; preserves prior attempts')
    parser.add_argument('--retry-failed-input', action='store_true',
                        help='Retry only a terminal file-download error after correcting input transport')
    args = parser.parse_args()
    if args.action=='prepare':
        # Local validation only: no credentials loaded, no provider requests.
        samples = json.loads(PLAN.read_text())['samples']
        for sample in samples:
            plan, settings, payload, expected = prepared(sample)
            print(json.dumps({'sample':sample,'endpoint':settings['endpoint_id'],
                  'parameters':{k:v for k,v in payload.items() if not k.endswith('_url')},
                  'estimated_usd':expected,'input_hashes_verified':True,
                  'submitted':False}))
    elif args.action=='submit':
        submit(args.sample, args.retry_rejected, args.retry_failed_input)
    else:
        poll()
