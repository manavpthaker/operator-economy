import fs from 'node:fs';import crypto from 'node:crypto';import {execFileSync} from 'node:child_process';
const sum=p=>crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const files=['index.html','compositions/owner-dependency.html','index.motion.json'];
const before=Object.fromEntries(files.map(p=>[p,sum(p)]));
const args=['hyperframes@0.8.31','check','--at','0,7,12,16.958333,17,20,24.125,24.166667,25,26,27.9,28.6,29.4,30.2,33.541667','--snapshots','--json'];
let output,code=0;try{output=execFileSync('npx',args,{encoding:'utf8',maxBuffer:8e6,stdio:['ignore','pipe','pipe']});}catch(e){output=String(e.stdout||'');code=e.status||1;}
const start=output.indexOf('{');if(start<0)throw Error('No runtime JSON: '+output);
const report=JSON.parse(output.slice(start));
const after=Object.fromEntries(files.map(p=>[p,sum(p)]));
report.sourcePinsBefore=before;report.sourcePinsAfter=after;report.contentStableAcrossCheck=JSON.stringify(before)===JSON.stringify(after);report.command='npx '+args.join(' ');
fs.writeFileSync('renders/runtime-check.json',JSON.stringify(report,null,2)+'\n');
console.log(JSON.stringify({ok:report.ok,exitCode:code,sourceStable:report.contentStableAcrossCheck,lint:report.lint.errorCount,runtime:report.runtime.errorCount,layout:report.layout.errorCount,motion:report.motion.errorCount,contrast:report.contrast.errorCount,receipt:'renders/runtime-check.json'}));
process.exitCode=code;
