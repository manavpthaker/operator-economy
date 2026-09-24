import {execFileSync} from 'node:child_process';
import {existsSync,readFileSync,writeFileSync,mkdirSync} from 'node:fs';
import {createHash} from 'node:crypto';
mkdirSync('provider',{recursive:true});
const mode=process.argv[2];
const cli=(args)=>JSON.parse(execFileSync('heygen',args,{encoding:'utf8',maxBuffer:8e6}));
const save=(name,obj)=>writeFileSync(`provider/${name}.json`,JSON.stringify(obj,null,2)+'\n');
if(mode==='upload'){
  if(existsSync('provider/intro-audio-upload.json'))throw Error('Upload receipt already exists; inspect instead of duplicating.');
  const b=readFileSync('public/audio/presenter-introduction.wav');
  if(createHash('sha256').update(b).digest('hex')!=='0604f9d4bf455970500d606a36778e9f9d0b9e4e61ec01ce4b930ada2b002201')throw Error('Wrong introduction audio');
  const r=cli(['asset','create','--file','public/audio/presenter-introduction.wav']);save('intro-audio-upload',r);console.log(JSON.stringify(r));
}else if(mode==='create'){
  if(existsSync('provider/intro-submission.json')||existsSync('provider/intro-attempt.json'))throw Error('Attempt exists; never resubmit an uncertain request.');
  const r=JSON.parse(readFileSync('provider/intro-audio-upload.json'));
  const id=r.data?.asset_id||r.data?.id;if(!id)throw Error('No uploaded audio asset id');
  const request={type:'image',image:{type:'asset_id',asset_id:'c3d34de484624626864053cb3dbe11cb'},audio_asset_id:id,expressiveness:'low',motion_prompt:'The presenter speaks with a neutral, matter-of-fact expression. His head stays upright and centered, chin level, shoulders relaxed and still. Small precise lip movements articulate the audio, with a relaxed jaw and eyebrows. Natural blinking.',resolution:'1080p',aspect_ratio:'16:9',fit:'cover',title:'EP007 - R10 exact introduction - Test Q setup'};
  save('intro-request',request);save('intro-attempt',{at:new Date().toISOString(),authorized:'Owner: use test Q. One exact-introduction request; no retries.'});
  const out=cli(['video','create','--data','provider/intro-request.json']);save('intro-submission',out);console.log(JSON.stringify(out));
}else if(mode==='status'||mode==='download'){
  const s=JSON.parse(readFileSync('provider/intro-submission.json'));const id=s.data?.video_id||s.data?.id;if(!id)throw Error('Missing video id');
  const r=cli(['video','get',id]);save('intro-status',r);
  console.log(JSON.stringify({id,status:r.data?.status,duration:r.data?.duration,error:r.data?.error}));
  if(mode==='download'){
    const url=r.data?.video_url;if(!url||r.data?.status!=='completed')throw Error('Video not completed');
    if(existsSync('public/media/presenter-introduction-q.mp4'))throw Error('Local output already exists');
    const resp=await fetch(url);if(!resp.ok)throw Error(`Download ${resp.status}`);const b=Buffer.from(await resp.arrayBuffer());writeFileSync('public/media/presenter-introduction-q.mp4',b);console.log({bytes:b.length,sha256:createHash('sha256').update(b).digest('hex')});
  }
}else throw Error('Use upload, create, status or download');
