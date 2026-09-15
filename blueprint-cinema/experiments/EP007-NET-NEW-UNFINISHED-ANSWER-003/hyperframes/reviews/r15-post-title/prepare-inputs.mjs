import {readFile,writeFile} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import {execFileSync} from 'node:child_process';
import {resolve,dirname} from 'node:path';
import {fileURLToPath} from 'node:url';
import assert from 'node:assert/strict';
const root=dirname(fileURLToPath(import.meta.url)),repo=resolve(root,'../../../../../..');
const sha=b=>createHash('sha256').update(b).digest('hex');
const master=resolve(repo,'operator-blueprint-v2/episodes/EP007-exit-readiness-prep/02-narration-production/master/narration-master.v4.wav');
const video=resolve(repo,'blueprint-cinema/experiments/EP007-PREMIUM-CONTROLLED-004/review-media/404.mp4');
assert.equal(sha(await readFile(master)),'d8f7cb9630ae12ad427dca2c7bd1f29611f56c7985ce900ea312df3b9fec8da9');
assert.equal(sha(await readFile(video)),'a0de31c36bde22219a1e067178b86cf750e7da1f11a69a775c370c82df6f29dd');
const ff=args=>execFileSync('ffmpeg',['-nostdin','-n','-v','error',...args],{stdio:'inherit'});
const probe=p=>JSON.parse(execFileSync('ffprobe',['-v','error','-show_streams','-show_format','-of','json',p],{encoding:'utf8'}));
const inputs=[];
for(const [id,a,b,f,g] of [['a',2856000,3164000,0,154],['b',3164000,3576000,83,289]]){
 const audioPath=`provider/inputs/pickup-${id}.wav`,videoPath=`provider/inputs/performance-${id}.mp4`;
 ff(['-i',master,'-af',`atrim=start_sample=${a}:end_sample=${b},asetpts=PTS-STARTPTS`,'-c:a','pcm_s16le',resolve(root,audioPath)]);
 ff(['-i',video,'-an','-vf',`trim=start_frame=${f}:end_frame=${g},setpts=PTS-STARTPTS`,'-c:v','libx264','-preset','fast','-crf','16','-pix_fmt','yuv420p','-movflags','+faststart',resolve(root,videoPath)]);
 const streams=probe(resolve(root,videoPath)).streams;
 assert.equal(streams.length,1);assert.equal(+streams[0].nb_frames,g-f);assert.equal(streams[0].r_frame_rate,'24/1');
 inputs.push({id,audio_path:audioPath,video_path:videoPath,audio_sha256:sha(await readFile(resolve(root,audioPath))),video_sha256:sha(await readFile(resolve(root,videoPath))),source_samples:[a,b],source_frames:[f,g],duration:(b-a)/48000,frames:g-f});
}
ff(['-i',master,'-af','atrim=start_sample=0:end_sample=3576000,asetpts=PTS-STARTPTS','-c:a','pcm_s16le',resolve(root,'public/audio/review-narration-extended.wav')]);
await writeFile(resolve(root,'provider/INPUTS.json'),JSON.stringify({model:'fal-ai/sync-lipsync/v3',inputs,extended_narration_sha256:sha(await readFile(resolve(root,'public/audio/review-narration-extended.wav')))},null,2)+'\n',{flag:'wx'});
console.log(JSON.stringify({ok:true,inputs}));
