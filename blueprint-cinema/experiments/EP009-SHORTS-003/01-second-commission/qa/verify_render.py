from pathlib import Path
import subprocess,json,hashlib,array,math
P=Path(__file__).resolve().parents[1];out=P/'review-r3.mp4'
def pcm(p):return array.array('h',subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-map','0:a:0','-ac','1','-ar','8000','-f','s16le','-']))
a=pcm(P/'assets/voice.wav');b=pcm(out);n=min(len(a),len(b));a=a[:n];b=b[:n];dot=sum(x*y for x,y in zip(a,b));aa=sum(x*x for x in a);bb=sum(x*x for x in b)
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(out)]));v=next(x for x in probe['streams'] if x['codec_type']=='video')
sha=lambda p:hashlib.file_digest(open(p,'rb'),'sha256').hexdigest()
report={'output':str(out.relative_to(P)),'sha256':sha(out),'duration':probe['format']['duration'],'dimensions':[v['width'],v['height']],'frames':v['nb_frames'],'fps':v['r_frame_rate'],'audio_comparison':{'reference':'assets/voice.wav','samples':n,'correlation':dot/math.sqrt(aa*bb),'gain':dot/aa,'note':'Encoded AAC compared to exact locked PCM concatenation; similarity is not perceptual mouth-sync review.'},'source_contract_sha256':sha(P/'source-contract.json'),'check_sha256':sha(P/'qa/check.json'),'presenter_review':'Source frame mappings preserve exact accepted performance; no regeneration, freeze or retime. Both ranges preserve original009 performance and hands through a760px crop, with mineral margins around the dominant portrait. No new performance or timing change.','publication':'private_review_only'}
(P/'QA.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
