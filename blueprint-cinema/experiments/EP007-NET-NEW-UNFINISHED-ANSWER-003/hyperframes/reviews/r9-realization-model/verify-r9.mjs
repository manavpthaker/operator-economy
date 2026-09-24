// Structural/provenance verification; does not confer creative approval.
import fs from 'node:fs';import path from 'node:path';import crypto from 'node:crypto';import assert from 'node:assert/strict';import {execFileSync} from 'node:child_process';import {fileURLToPath} from 'node:url';
const here=path.dirname(fileURLToPath(import.meta.url)),repo=path.resolve(here,'../../../../../..');
const sum=p=>crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const probe=p=>JSON.parse(execFileSync('ffprobe',['-v','error','-show_streams','-show_format','-of','json',p],{encoding:'utf8'}));
const attrs=s=>Object.fromEntries([...s.matchAll(/([\w-]+)="([^"]*)"/g)].map(m=>[m[1],m[2]]));
const html=fs.readFileSync(path.join(here,'index.html'),'utf8'),r8=fs.readFileSync(path.resolve(here,'../r8-context-coverage/index.html'),'utf8');
assert.equal(crypto.createHash('sha256').update(r8).digest('hex'),'5dec99d3791b7be948eaef1de7221b9e8d6ad21756b41f52a95818266ba181bd');
const videos=s=>[...s.matchAll(/<video\s([^>]+)>/g)].map(m=>attrs(m[1]));
const shots=videos(html),old=videos(r8);assert.equal(shots.length,4);
for(let i=0;i<3;i++)for(const key of ['src','data-start','data-duration','data-media-start','data-track-index'])assert.equal(shots[i][key],old[i][key],'R8 selection changed: '+key);
const vo=attrs(html.match(/<audio\s([^>]+)>/)[1]);
assert.equal(Number(vo['data-start']),0);assert.equal(Number(vo['data-duration']),806/24);assert.equal(Number(vo['data-media-start']),10.92);assert.equal(Number(vo['data-volume']),1);
const master=path.join(repo,'operator-blueprint-v2/episodes/EP007-exit-readiness-prep/02-narration-production/master/narration-master.v4.wav'),audio=path.join(here,vo.src);
assert.equal(sum(master),'d8f7cb9630ae12ad427dca2c7bd1f29611f56c7985ce900ea312df3b9fec8da9');assert.equal(sum(audio),'120c7a64ae8582f55f9bb4338c9ec276d763d79d88718aac482fc81c48ddbfb1');
const startSample=524160,endSample=startSample+806*2000;
const pcm=p=>execFileSync('ffmpeg',['-v','error','-i',p,'-af',`atrim=start_sample=${startSample}:end_sample=${endSample},asetpts=PTS-STARTPTS`,'-c:a','pcm_s16le','-f','s16le','pipe:1'],{maxBuffer:8e6});
const selected=pcm(audio);assert.ok(selected.equals(pcm(master)));assert.equal(selected.length,806*2000*2);
let cursor=0;const results=[];
for(const[i,t]of shots.entries()){
 const letter='abcd'[i],file=path.join(here,t.src),info=probe(file),v=info.streams.find(s=>s.codec_type==='video');
 const start=Number(t['data-start']),duration=Number(t['data-duration']),mediaStart=Number(t['data-media-start']);
 assert.ok(Math.abs(start-cursor)<1e-8);assert.ok(Math.abs(start*24-Math.round(start*24))<1e-7);assert.ok(Math.abs(duration*24-Math.round(duration*24))<1e-7);
 assert.equal(v.r_frame_rate,'24/1');assert.equal(info.streams.filter(s=>s.codec_type==='audio').length,0);assert.ok(mediaStart+duration<=Number(v.duration));
 if(i<3)assert.equal(sum(file),sum(path.resolve(here,'../r8-context-coverage',t.src)));
 else{
  const receipt=JSON.parse(fs.readFileSync(path.join(here,'renders/candidates/shot-d.mp4.response.json'),'utf8'));
  assert.equal(receipt.requestId,'01a081ec-17f8-7c60-8b31-e419124b6f6c');assert.equal(receipt.model,'fal-ai/kling-video/v3/pro/image-to-video');assert.equal(receipt.request.parameters.generate_audio,false);assert.equal(Number(receipt.request.parameters.duration),8);assert.equal(receipt.request.parameters.cfg_scale,.5);
  assert.equal(sum(file),receipt.output.sha256);assert.equal(sum(file),'c09986f249dcdfe365a9bbd56fef13b89760f71d0503b8a31e3745ff7715fa4c');assert.equal(sum(receipt.request.reference),receipt.request.referenceSha256);
  execFileSync('ffmpeg',['-v','error','-i',file,'-f','null','-']);
 }
 results.push({id:letter,sha256:sum(file),record:[start,start+duration],source:[mediaStart,mediaStart+duration],sourceDuration:Number(v.duration),width:v.width,height:v.height});cursor=start+duration;
}
const slot=attrs(html.match(/<div[^>]+data-composition-src=[^>]+>/)[0]);assert.equal(Number(slot['data-start']),cursor);assert.equal(Number(slot['data-start'])+Number(slot['data-duration']),806/24);
const sub=fs.readFileSync(path.join(here,slot['data-composition-src']),'utf8');assert.ok(sub.indexOf('<template>')<sub.indexOf('<style>'));assert.ok(sub.includes(`window.__timelines['${slot['data-composition-id']}']`));
assert.ok(!/Math\.random|setInterval|requestAnimationFrame|\.play\(|filter:|feTurbulence/.test(sub));
const ids=[...sub.matchAll(/\sid="([^"]+)"/g)].map(m=>m[1]);assert.equal(new Set(ids).size,ids.length);
const manifest=JSON.parse(fs.readFileSync(path.join(here,'motion-ready-asset.json'),'utf8'));assert.equal(sum(path.join(here,manifest.sourceStill.path)),manifest.sourceStill.sha256);assert.equal(sum(path.join(here,manifest.semanticCore.path)),manifest.semanticCore.sha256);
for(const layer of manifest.layers)assert.equal(sum(path.join(here,layer.asset.path)),layer.asset.sha256);
assert.equal(sum(path.join(repo,'blueprint-cinema/experiments/EP007-NET-NEW-UNFINISHED-ANSWER-001/hyperframes/compositions/sequences/03-model-exposure.html')),'0d1297cddaf0eb8b8fd87d9dec89198bbb6c0677a5c15b83efb7d3032ce54c39');
const result={status:'mechanical-trial-check-passed',frames:806,fps:24,duration:806/24,firstR8FramesPreserved:408,narrationSource:[10.92,10.92+806/24],sampleExact:true,narrationPcmSha256:crypto.createHash('sha256').update(selected).digest('hex'),shots:results,graphic:{start:580/24,end:806/24,manifestSha256:sum(path.join(here,'motion-ready-asset.json')),historicalSourcePreserved:true},newVideoRequests:1,estimatedVideoListCostUsd:.896,billingInvoiceVerified:false,creativeApproval:false,productionGateAdvance:false,finalRender:false,watchpoints:['D eyes briefly lift toward buyer; the literal fixed-gaze prompt did not fully land.','The remembered historical illustration is not uniquely identified.','Causal and visual effectiveness need owner review; mechanical pass is not creative approval.']};
fs.writeFileSync(path.join(here,'renders/verification.json'),JSON.stringify(result,null,2)+'\n');
const receipt=JSON.parse(fs.readFileSync(path.join(here,'renders/candidates/shot-d.mp4.response.json'),'utf8'));
const assets={schema:'oe-isolated-film-and-model-review-assets-v1',date:'2026-09-08',reviewOnly:true,creativeApproval:false,indexSha256:sum(path.join(here,'index.html')),compositionSha256:sum(path.join(here,'compositions/owner-dependency.html')),runtimeVersion:'0.8.31',mechanicalReceipt:'renders/verification.json',newVideoRequests:1,videoModel:receipt.model,generateAudio:false,cfgScale:.5,estimatedVideoListCostUsd:.896,billingInvoiceVerified:false,referenceImageCostVerified:false,assets:results.map(x=>({...x,path:'public/media/shot-'+x.id+'.mp4',reused:x.id!=='d',provenance:x.id==='d'?'renders/candidates/shot-d.mp4.response.json':'../r8-context-coverage/ASSET-MANIFEST.json'})),lockedNarration:{path:vo.src,sha256:sum(audio),sourceSeconds:result.narrationSource,selectedPcmSha256:result.narrationPcmSha256},referenceImage:{path:'public/media/shot-d-start.png',sha256:sum(path.join(here,'public/media/shot-d-start.png')),provider:'built-in imagegen',original:'/Users/brownmanbrain/.codex/generated_images/01a078b6-acf7-76a2-ab00-4c2cff805684/exec-63af6811-9fd5-4460-87bc-d7e5fd198bf7.png',promptRecord:'REFERENCE-D-PROMPT.md'},workingModel:{manifest:'motion-ready-asset.json',sha256:sum(path.join(here,'motion-ready-asset.json')),build:'pencil-build.json',historicalSourcesPreserved:true},disclosure:'Film and owner reference are AI-generated dramatization, not documentary case footage. Drawing is an illustrative dependency question, not verified business failure.',scope:'Isolated Studio test. No avatar/preroll, final MP4, canonical gate promotion, commit, push or publication.'};
fs.writeFileSync(path.join(here,'ASSET-MANIFEST.json'),JSON.stringify(assets,null,2)+'\n');console.log(JSON.stringify(result,null,2));
