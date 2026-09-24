#!/usr/bin/env python3
"""Build all fourteen exact-clock before/after pairs with locked master excerpts."""
import argparse
import datetime
import hashlib
import json
import subprocess
import sys
import wave
from pathlib import Path

sys.dont_write_bytecode = True
T = Path(__file__).resolve().parents[1]
B = T.parent
A = B/'assembly'
D = T/'paired-review-r1'
OUTPUT = T/'paired-review-r1.mp4'
BUILD = D/'BUILD.json'
AUDIT = T/'SOURCE-AUDIT.json'
AUDIT_SHA = '77d1300b3f52841209013af3523124bbca9568061f6cac35fb6026de0184224d'
IDS = ['seg009','seg012','seg019','seg021','seg028','seg035','seg037','seg055',
       'seg059','seg071','seg072','seg073','seg074','seg075']
sys.path[:0] = [str(T/'_tools'), str(A/'_tools')]
from build_r3 import R, bound, read, rel, verify_bound, write, probe
from build_review import audio_digest, video_hashes
from verify_r3 import audio_check


def inventory():
    audit = read(verify_bound({'path': rel(AUDIT), 'sha256': AUDIT_SHA}))
    rows = [r for r in audit['appearances'] if r['kind'] == 'video']
    if [r['segment'] for r in rows] != IDS or sum(r['duration_frames'] for r in rows) != 3589:
        raise ValueError('Expected exactly the fourteen existing presenter segments, 3589 frames')
    missing = []
    for row in rows:
        for suffix in ('.mp4', '-SELECTION.json', '-VERIFICATION.json'):
            p = T/'final-r1'/(row['segment']+suffix)
            if not p.exists(): missing.append(rel(p))
    return audit, rows, missing


def prepare(audit, rows):
    master = verify_bound(audit['master'])
    entries = []
    count = 0
    for row in rows:
        sid = row['segment']; n = row['duration_frames']
        selection_path = T/'final-r1'/(sid+'-SELECTION.json')
        selection = read(selection_path)
        expected = T/'final-r1'/(sid+'.mp4')
        updated = verify_bound(selection['source'])
        old = verify_bound(row['selected_source'])
        ev = read(verify_bound(selection['verification']))
        if (updated != expected or selection['segment'] != sid or selection['source_start_frame'] != 0
                or selection['output_frames'] != row['output_frames'] or selection['frames'] != n):
            raise ValueError(sid+': wrong selected updated carrier')
        if ev['replacement'] != selection['source'] or ev['errors'] != [] or ev['technical_complete'] is not True:
            raise ValueError(sid+': incomplete or stale technical carrier')
        if ev['master'] != audit['master'] or ev['original_source'] != row['selected_source']:
            raise ValueError(sid+': wrong source/master provenance')
        if row['source_frames'] != [0,n]: raise ValueError(sid+': original is not a full exact-frame carrier')
        sequences = {}
        for role, path in [('original',old),('updated',updated)]:
            info = probe(path)
            v = next(s for s in info['streams'] if s['codec_type'] == 'video')
            if (v['width'],v['height'],v['r_frame_rate'],int(v['nb_read_frames'])) != (1280,720,'24/1',n):
                raise ValueError(sid+': expected full 1280x720 exact24fps '+role)
            seq = video_hashes(path,n)
            key = 'original_frame_sequence_sha256' if role == 'original' else 'replacement_frame_sequence_sha256'
            if seq['sequence_sha256'] != ev[key]: raise ValueError(sid+': decoded source sequence changed')
            sequences[role] = seq['sequence_sha256']
        digest = audio_digest(master,row['output_frames'])
        if ev['master_pcm_sha256'] != digest: raise ValueError(sid+': locked audio digest mismatch')
        entries.append({'segment':sid,'frames':n,'reel_frames':[count,count+n],
                        'master_frames':row['output_frames'],'master_sample_range':[x*2000 for x in row['output_frames']],
                        'original_left':row['selected_source'],'updated_right':selection['source'],
                        'source_frames':[0,n],'selection':bound(selection_path),'verification':selection['verification'],
                        'source_frame_sequence_sha256':sequences,'master_pcm_sha256':digest,
                        'source_review_flags_retained_in_verification':True})
        count += n
    return {'record_type':'ep009_fourteen_presenter_paired_review_build','status':'prepared_not_rendered',
            'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_audit':bound(AUDIT),
            'master':audit['master'],'helper':bound(Path(__file__)), 'layout':'Original left; updated right',
            'dimensions':[2560,720],'frames':3589,'fps':24,'duration_seconds':3589/24,
            'program_samples':7178000,'entries':entries,'P00_included':False,'P08_included':False,
            'all_segment_frames_retained':True,'speed_changed':False,'provider_audio_used':False,
            'owner_accepted':False,'lip_sync_approved':False,'release_approved':False,
            'limits':['Paired private comparison only; original and updated images each retain their full frame and timing.',
                      'The two views use one locked narration track. Carrier identity does not prove preserved performance or lip sync.',
                      'Source review limits/flags remain bound. The reel does not accept or release any segment.']}


def render(data):
    if BUILD.exists() or OUTPUT.exists(): raise FileExistsError('Preserve current reel and build; never rerun over partial output')
    D.mkdir(exist_ok=True)
    for p in (D/'chunks', D/'narration-exact-master.wav', D/'concat.txt', D/'VERIFY.json'):
        if p.exists(): raise FileExistsError('Preserve existing preparation artifacts: '+str(p))
    (D/'chunks').mkdir()
    data['status'] = 'rendering_private_comparison'
    write(BUILD,data)
    chunks = []
    for entry in data['entries']:
        n = entry['frames']; out = D/'chunks'/(entry['segment']+'.mp4')
        graph = (f'[0:v]trim=start_frame=0:end_frame={n},setpts=N/(24*TB),setsar=1,format=yuv420p[l];'
                 f'[1:v]trim=start_frame=0:end_frame={n},setpts=N/(24*TB),setsar=1,format=yuv420p[r];'
                 '[l][r]hstack=inputs=2[v]')
        cmd = ['ffmpeg','-nostdin','-n','-v','error','-filter_complex_threads','1',
               '-threads','1','-i',str(verify_bound(entry['original_left'])),
               '-threads','1','-i',str(verify_bound(entry['updated_right'])),
               '-filter_complex',graph,'-map','[v]','-an','-c:v','libx264','-preset','fast',
               '-crf','18','-threads','2','-pix_fmt','yuv420p','-r','24','-movflags','+faststart',str(out)]
        subprocess.run(cmd,check=True)
        entry['pair_chunk'] = bound(out); entry['pair_command'] = cmd
        chunks.append(out)
        print(json.dumps({'paired_segment':entry['segment'],'frames':n}),flush=True)
    narration = D/'narration-exact-master.wav'
    pcm_sha = hashlib.sha256(); samples = 0
    with wave.open(str(verify_bound(data['master'])),'rb') as source, wave.open(str(narration),'wb') as dest:
        if (source.getframerate(),source.getnchannels(),source.getsampwidth()) != (48000,1,2): raise ValueError('Wrong master format')
        dest.setparams((1,2,48000,0,'NONE','not compressed'))
        for e in data['entries']:
            a,z = e['master_sample_range'];source.setpos(a);raw = source.readframes(z-a)
            padding = (z-a)-len(raw)//2
            if padding and not (e['segment']=='seg075' and padding==1080): raise ValueError('Unexpected source audio shortfall')
            raw += b'\0\0'*padding
            if hashlib.sha256(raw).hexdigest() != e['master_pcm_sha256']: raise ValueError('Excerpt PCM changed')
            dest.writeframes(raw);pcm_sha.update(raw);samples += len(raw)//2
            e['master_zero_padding_samples'] = padding
    if samples != 7178000: raise ValueError('Wrong reel narration length')
    concat = D/'concat.txt'
    # All names are fixed and contain no quotes; paths are relative to the list.
    with concat.open('x') as f:
        for p in chunks: f.write("file 'chunks/"+p.name+"'\n")
    cmd = ['ffmpeg','-nostdin','-n','-v','error','-threads','1','-f','concat','-safe','1','-i',str(concat),
           '-i',str(narration),'-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','256k',
           '-ar','48000','-ac','2','-threads','2','-movflags','+faststart',str(OUTPUT)]
    subprocess.run(cmd,check=True)
    data.update(status='encoded_unverified_private_comparison',output=bound(OUTPUT),exact_narration=bound(narration),
                program_pcm_sha256=pcm_sha.hexdigest(),concat=bound(concat),mux_command=cmd)
    BUILD.write_text(json.dumps(data,indent=2)+'\n')
    info = probe(OUTPUT);v=next(s for s in info['streams'] if s['codec_type']=='video')
    a=next(s for s in info['streams'] if s['codec_type']=='audio')
    errors=[]
    if (v['width'],v['height'],v['r_frame_rate'],int(v['nb_read_frames'])) != (2560,720,'24/1',3589): errors.append('picture_format_count')
    if (a['sample_rate'],a['channels']) != ('48000',2): errors.append('audio_format')
    if abs(float(info['format']['duration'])-3589/24)>.002: errors.append('duration')
    clock=video_hashes(OUTPUT,3589)
    audio=audio_check(OUTPUT,narration,[0,3589])
    if audio['compared_samples']!=7178000 or any(audio['decode_exit_codes']):errors.append('audio_decode_count')
    if audio['min_voiced_window_corr']<.999 or audio['max_abs_voiced_window_rms_db']>.1:errors.append('audio_mapping_or_level')
    if not 0<=audio['aac_padding_samples']<=1024 or audio['padding_peak_abs']>1e-5:errors.append('unexpected_tail')
    verification={'record_type':'ep009_paired_review_mechanical_verification','status':'verified_private_review_only' if not errors else 'failed',
                  'build':bound(BUILD),'output':bound(OUTPUT),'exact_narration':bound(narration),'errors':errors,
                  'frames':3589,'program_samples':7178000,'probe':info,'audio':audio,
                  'decoded_frame_sequence_sha256':clock['sequence_sha256'],'all_frame_timestamps_checked':True,
                  'owner_accepted':False,'lip_sync_approved':False,'limits':data['limits']}
    write(D/'VERIFY.json',verification)
    if errors:raise ValueError('Reel verification failed: '+str(errors))
    print(json.dumps({'status':verification['status'],'output':bound(OUTPUT),'build':bound(BUILD),'verification':bound(D/'VERIFY.json')},indent=2))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=['check','render'])
    args=parser.parse_args()
    audit,rows,missing=inventory()
    if missing:
        print(json.dumps({'status':'waiting_for_final_carriers','missing':missing},indent=2))
        if args.action=='render':raise SystemExit(2)
        return
    data=prepare(audit,rows)
    if args.action=='check':
        print(json.dumps({'status':'all_fourteen_inputs_verified','frames':3589,'seconds':3589/24,'program_samples':7178000},indent=2))
    else:render(data)


if __name__=='__main__':main()
