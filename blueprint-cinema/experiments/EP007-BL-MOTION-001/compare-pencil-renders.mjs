import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const here=path.dirname(fileURLToPath(import.meta.url));
const dir=path.join(here,'pencil-study');
const renders=path.join(dir,'renders');
const qa=path.join(dir,'qa');
fs.mkdirSync(renders,{recursive:true});fs.mkdirSync(qa,{recursive:true});
const before=path.join(here,'hyperframes/renders/EP007-BL-MOTION-001.mp4');
const after=path.join(renders,'EP007-BL-PENCIL-001.mp4');
const hash=file=>crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex');
function run(exe,args){
  const result=spawnSync(exe,args,{encoding:'utf8',maxBuffer:12e6});
  if(result.status!==0)throw new Error(`${exe} failed (${result.status}): ${result.stderr}`);
  return result;
}
const probe=file=>JSON.parse(run('ffprobe',['-v','error','-count_frames','-show_streams','-show_format','-of','json',file]).stdout);
const original=probe(before),revised=probe(after);
const v=p=>p.streams.find(s=>s.codec_type==='video');
if(v(revised).width!==1920||v(revised).height!==1080||v(revised).nb_read_frames!=='840'||Math.abs(Number(revised.format.duration)-28)>.04)throw new Error('Unexpected revised render geometry or duration.');
const decodedAudio=file=>run('ffmpeg',['-v','error','-i',file,'-map','0:a:0','-f','hash','-hash','sha256','-']).stdout.trim();
const beforeAudio=decodedAudio(before),afterAudio=decodedAudio(after);
if(beforeAudio!==afterAudio)throw new Error('Decoded narration differs between A/B outputs.');
const originalHash=hash(before);
if(originalHash!=='8090cdc2e765a1d09345ce1cb75e59a8bbf0873ecae1386311c5b3924c4d542a')throw new Error('Original render changed.');
const comparison=path.join(renders,'EP007-BL-PENCIL-comparison.mp4');
run('ffmpeg',['-v','error','-y','-i',before,'-i',after,'-filter_complex',
  '[0:v]scale=960:540:flags=lanczos,pad=970:540:0:0:color=0xf5f0e6[a];[1:v]scale=960:540:flags=lanczos,pad=970:540:10:0:color=0xf5f0e6[b];[a][b]hstack=inputs=2[v]',
  '-map','[v]','-map','1:a:0','-c:v','libx264','-crf','18','-preset','medium','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',comparison]);
const detail=path.join(renders,'pencil-detail-comparison.png');
run('ffmpeg',['-v','error','-y','-ss','3.9','-i',before,'-ss','3.9','-i',after,'-filter_complex',
  '[0:v]crop=600:520:105:260,pad=620:540:10:10:color=0xf5f0e6[a];[1:v]crop=600:520:105:260,pad=620:540:10:10:color=0xf5f0e6[b];[a][b]hstack=inputs=2[v]',
  '-map','[v]','-frames:v','1',detail]);
for(const time of ['0.8','3.9','6.4','10.7','14.5','17.4','20.2','23.6','25.8','27.6']){
  run('ffmpeg',['-v','error','-y','-ss',time,'-i',after,'-frames:v','1',path.join(qa,`encoded-${time}s.png`)]);
}
run('ffmpeg',['-v','error','-y','-ss','20.2','-i',after,'-vf','scale=640:360:flags=lanczos','-frames:v','1',path.join(qa,'encoded-20.2s-at-640.png')]);
const signal=run('ffmpeg',['-hide_banner','-i',after,'-vf','blackdetect=d=0.05:pix_th=0.10','-af','ebur128=peak=true','-f','null','-']);
fs.writeFileSync(path.join(qa,'encoded-signal-check.txt'),signal.stderr);
const report={
  scope:'Internal rendered A/B style test; no production gate, commit, delivery or publication approval',
  source_html_unchanged:hash(path.join(here,'hyperframes/index.html'))==='0282f63fd9a14c0095c444af53adc2aaf2121464a7fb4e26dff92c27b2bcbe9d',
  original:{file:before,sha256:originalHash},
  revised:{file:after,sha256:hash(after),width:v(revised).width,height:v(revised).height,fps:v(revised).r_frame_rate,frames:Number(v(revised).nb_read_frames),seconds:Number(revised.format.duration),bytes:Number(revised.format.size)},
  comparison:{file:comparison,sha256:hash(comparison)},
  detail:{file:detail,sha256:hash(detail)},
  decoded_audio_identical:beforeAudio===afterAudio,decoded_audio_sha256:afterAudio,
  black_intervals:signal.stderr.split('\n').filter(l=>l.includes('black_start:')),
  check_artifact_sha256:JSON.parse(fs.readFileSync(path.join(qa,'hyperframes-check.json'))).artifact_sha256,
  current_artifact_sha256:hash(path.join(dir,'index.html')),
  visual_review:'Agent must inspect encoded frames and detail comparison separately; machine checks do not certify aesthetics.'
};
if(report.check_artifact_sha256!==report.current_artifact_sha256)throw new Error('Rendered/check source hash mismatch');
fs.writeFileSync(path.join(qa,'render-verification.json'),JSON.stringify(report,null,2)+'\n');
const buildFile=path.join(dir,'pencil-build.json');
const build=JSON.parse(fs.readFileSync(buildFile,'utf8'));
build.status='rendered_for_review';
build.checked_render_source_sha256=report.current_artifact_sha256;
build.render_verification='qa/render-verification.json';
fs.writeFileSync(buildFile,JSON.stringify(build,null,2)+'\n');
console.log(JSON.stringify(report,null,2));
