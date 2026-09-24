#!/usr/bin/env python3
"""Preserve failed paired carrier; repair only implicit stereo attenuation."""
import copy
import datetime
import json
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
T = Path(__file__).resolve().parents[1]
A = T.parent/'assembly'
D = T/'paired-review-r1'
sys.path[:0] = [str(T/'_tools'), str(A/'_tools')]
from build_r3 import bound, read, verify_bound, write, probe
from build_review import video_hashes
from verify_r3 import audio_check


def main():
    original = D/'BUILD.json'; failed_path = D/'VERIFY.json'
    base = read(original); failed = read(failed_path)
    if failed['build'] != bound(original) or failed['errors'] != ['audio_mapping_or_level']:
        raise ValueError('Expected only the known stereo-level failure')
    if (failed['frames'],failed['program_samples']) != (3589,7178000):
        raise ValueError('Unexpected original timeline')
    original_video = verify_bound(base['output'])
    narration = verify_bound(base['exact_narration'])
    verify_bound(base['master']); verify_bound(base['source_audit'])
    for e in base['entries']:
        for k in ['original_left','updated_right','selection','verification','pair_chunk']:
            verify_bound(e[k])
    output = A/'qa/r5-look-transfer/ep009-presenter-comparison-r1.mp4'
    build = D/'UNITY-REMUX-r1-BUILD.json'
    report = D/'UNITY-REMUX-r1-VERIFICATION.json'
    if any(p.exists() for p in [output,build,report]):
        raise FileExistsError('Preserve existing remux output and diagnostics')
    output.parent.mkdir(parents=True,exist_ok=True)
    cmd = ['ffmpeg','-nostdin','-n','-v','error','-threads','1','-i',str(original_video),
           '-i',str(narration),'-map','0:v:0','-map','1:a:0','-c:v','copy',
           '-af','pan=stereo|c0=c0|c1=c0','-c:a','aac','-b:a','256k','-ar','48000','-ac','2',
           '-threads','2','-movflags','+faststart',str(output)]
    data = copy.deepcopy(base)
    data.update(status='rendering_unity_audio_remux',at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                source_render_build=bound(original),preserved_level_failure=bound(failed_path),
                helper=bound(Path(__file__)),mux_command=cmd,
                repair='Explicit unity dual-mono pan replaces FFmpeg default -3dB upmix. Picture packets copied; exact locked PCM unchanged.')
    data.pop('output',None)
    write(build,data)
    subprocess.run(cmd,check=True)
    data.update(status='encoded_unverified_private_comparison',output=bound(output))
    build.write_text(json.dumps(data,indent=2)+'\n')
    info=probe(output);v=next(s for s in info['streams'] if s['codec_type']=='video')
    a=next(s for s in info['streams'] if s['codec_type']=='audio');errors=[]
    if (v['width'],v['height'],v['r_frame_rate'],int(v['nb_read_frames'])) != (2560,720,'24/1',3589):errors.append('video_format_count')
    if (a['sample_rate'],a['channels']) != ('48000',2):errors.append('audio_format')
    if abs(float(info['format']['duration'])-3589/24)>.002:errors.append('duration')
    frames=video_hashes(output,3589)
    if frames['sequence_sha256'] != failed['decoded_frame_sequence_sha256']:errors.append('remux_changed_picture')
    audio=audio_check(output,narration,[0,3589])
    if audio['compared_samples'] != 7178000 or any(audio['decode_exit_codes']):errors.append('audio_decode_count')
    if audio['min_voiced_window_corr']<.999 or audio['max_abs_voiced_window_rms_db']>.1:errors.append('audio_identity_or_level')
    if not 0<=audio['aac_padding_samples']<=1024 or audio['padding_peak_abs']>1e-5:errors.append('audio_tail')
    result={'record_type':'ep009_paired_review_mechanical_verification','status':'verified_private_review_only' if not errors else 'failed',
            'build':bound(build),'output':bound(output),'exact_narration':base['exact_narration'],
            'errors':errors,'frames':3589,'program_samples':7178000,'probe':info,'audio':audio,
            'decoded_frame_sequence_sha256':frames['sequence_sha256'],'all_frame_timestamps_checked':True,
            'decoded_video_identical_to_preserved_carrier':frames['sequence_sha256']==failed['decoded_frame_sequence_sha256'],
            'owner_accepted':False,'lip_sync_approved':False,'limits':base['limits']}
    write(report,result)
    print(json.dumps({'status':result['status'],'errors':errors,'output':bound(output),'build':bound(build),'verification':bound(report)},indent=2))
    if errors:raise SystemExit(2)


if __name__=='__main__':main()
