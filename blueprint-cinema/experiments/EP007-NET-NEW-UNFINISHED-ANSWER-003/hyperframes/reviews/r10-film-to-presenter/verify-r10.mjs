import fs from 'node:fs';import path from 'node:path';import crypto from 'node:crypto';import assert from 'node:assert/strict';import {execFileSync} from 'node:child_process';
const repo=path.resolve('../../../../../..');const sum=p=>crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const attrs=s=>Object.fromEntries([...s.matchAll(/([\w-]+)="([^"]*)"/g)].map(m=>[m[1],m[2]]));
const html=fs.readFileSync('index.html','utf8'),r9=fs.readFileSync('../r9-realization-model/index.html','utf8');
const videos=s=>[...s.matchAll(/<video\s([^>]+)>/g)].map(m=>attrs(m[1]));const shots=videos(html),old=videos(r9);assert.equal(shots.length,6);
for(let i=0;i<4;i++){for(const key of ['src','data-start','data-duration','data-media-start','data-track-index'])assert.equal(shots[i][key],old[i][key],'Retained selection changed');assert.equal(sum(shots[i].src),sum(path.join('../r9-realization-model',old[i].src)));}
assert.ok(!html.includes('owner-dependency')&&!html.includes('<svg'));
const master=path.join(repo,'operator-blueprint-v2/episodes/EP007-exit-readiness-prep/02-narration-production/master/narration-master.v4.wav');assert.equal(sum(master),'d8f7cb9630ae12ad427dca2c7bd1f29611f56c7985ce900ea312df3b9fec8da9');
const pcm=(p,trim)=>execFileSync('ffmpeg',['-v','error','-i',p,...(trim?['-af',trim]:[]),'-c:a','pcm_s16le','-f','s16le','pipe:1'],{maxBuffer:8e6});
const selected=pcm(master,'atrim=start_sample=524160:end_sample=3556160,asetpts=PTS-STARTPTS'),out=pcm('public/audio/review-narration.wav');assert.ok(out.equals(selected));assert.equal(out.length,1516*2000*2);
const vo=attrs(html.match(/<audio\s([^>]+)>/)[1]);assert.equal(Number(vo['data-media-start']),0);assert.equal(Number(vo['data-duration']),1516/24);assert.equal(Number(vo['data-volume']),1);
const probe=p=>JSON.parse(execFileSync('ffprobe',['-v','error','-show_streams','-show_format','-of','json',p],{encoding:'utf8'}));
const results=[];for(const [i,t]of shots.entries()){
 const info=probe(t.src),v=info.streams.find(s=>s.codec_type==='video'),start=+t['data-start'],duration=+t['data-duration'],source=+t['data-media-start'];
 assert.ok(Math.abs(start*24-Math.round(start*24))<1e-7);assert.ok(Math.abs(duration*24-Math.round(duration*24))<1e-7);assert.ok(source+duration<=Number(v.duration)+1e-6);
 assert.equal(v.r_frame_rate,i<5?'24/1':'25/1');if(i<5)assert.equal(info.streams.filter(s=>s.codec_type==='audio').length,0);
 execFileSync('ffmpeg',['-v','error','-i',t.src,'-f','null','-']);results.push({id:t.id,path:t.src,sha256:sum(t.src),record:[start,start+duration],source:[source,source+duration],sourceDuration:Number(v.duration),width:v.width,height:v.height,fps:v.r_frame_rate});
}
const spans=[...results.slice(0,5).map(s=>s.record),[806/24,902/24],results[5].record];let cursor=0;for(const [a,b]of spans){assert.ok(Math.abs(a-cursor)<1e-7);cursor=b;}assert.ok(Math.abs(cursor-1516/24)<1e-7);
const receipt=JSON.parse(fs.readFileSync('renders/shot-e.response.json'));assert.equal(receipt.output.sha256,sum('public/media/shot-e.mp4'));assert.equal(receipt.model,'fal-ai/kling-video/v3/pro/image-to-video');assert.equal(Number(receipt.request.parameters.duration),10);assert.equal(receipt.request.parameters.generate_audio,false);
const request=JSON.parse(fs.readFileSync('provider/intro-request.json')),q=JSON.parse(fs.readFileSync(path.join(repo,'blueprint-cinema/experiments/EP007-PRESENTER-001/repair-r18/video-request.json')));
for(const key of ['type','image','motion_prompt','expressiveness','resolution','aspect_ratio','fit'])assert.deepEqual(request[key],q[key]);assert.notEqual(request.audio_asset_id,q.audio_asset_id);
const sync=JSON.parse(fs.readFileSync('renders/intro-audio-sync.json'));assert.ok(Math.abs(+shots[5]['data-media-start']-(10.92+902/24-48.27+sync.medianDelaySeconds))<1e-7);
const result={status:'mechanical-review-passed',frames:1516,fps:24,duration:1516/24,preservedFilmFrames:580,masterSource:[10.92,10.92+1516/24],sampleExact:true,shots:results,presenterAudioSync:sync,gridRemoved:true,mechanismPreviewBuilt:false,prerollIncluded:false,creativeApproval:false,productionGateAdvance:false,finalRender:false};
fs.writeFileSync('renders/verification.json',JSON.stringify(result,null,2)+'\n');
fs.writeFileSync('ASSET-MANIFEST.json',JSON.stringify({schema:'oe-isolated-film-presenter-review-assets-v1',reviewOnly:true,runtime:'0.8.31',indexSha256:sum('index.html'),assets:results,narration:{path:'public/audio/review-narration.wav',sha256:sum('public/audio/review-narration.wav'),masterSha256:sum(master),source:result.masterSource,sampleExact:true},newRequests:{kling:receipt.requestId,heygen:JSON.parse(fs.readFileSync('provider/intro-submission.json')).data.video_id},klingListEstimateUsd:1.12,actualBillingVerified:false,presenterRecipe:'Test Q exact settings with exact intro audio',identity:'Static wordmark typography inherited from local06-identity-title; no new identity animation',disclosure:'AI-generated dramatization and authorized AI presenter; not documentary case evidence',scope:'No S08 model rebuild, arrival pre-roll, canonical gates, final render, publication, commit or push'},null,2)+'\n');console.log(JSON.stringify(result,null,2));
