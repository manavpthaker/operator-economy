import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const here=path.dirname(fileURLToPath(import.meta.url));
const dir=path.join(here,'pencil-study');
const output=path.join(dir,'qa');
fs.mkdirSync(output,{recursive:true});
const result=spawnSync('npx',['--yes','hyperframes@0.8.27','check','--strict','--samples','15','--snapshots','--json'],{
  cwd:dir,encoding:'utf8',maxBuffer:12e6,
  env:{...process.env,HYPERFRAMES_NO_TELEMETRY:'1',HYPERFRAMES_RUN_ID:'ep007-pencil-ab-01'}
});
fs.writeFileSync(path.join(output,'hyperframes-check.stdout.txt'),result.stdout||'');
fs.writeFileSync(path.join(output,'hyperframes-check.stderr.txt'),result.stderr||'');
const start=result.stdout.indexOf('{\n  "ok"');
if(start<0)throw new Error(`No structured check result; exit ${result.status}`);
const report=JSON.parse(result.stdout.slice(start));
const source=fs.readFileSync(path.join(dir,'index.html'));
report.artifact_sha256=crypto.createHash('sha256').update(source).digest('hex');
fs.writeFileSync(path.join(output,'hyperframes-check.json'),JSON.stringify(report,null,2)+'\n');
console.log(JSON.stringify({exitCode:result.status,ok:report.ok,artifact_sha256:report.artifact_sha256,report:path.join(output,'hyperframes-check.json')}));
if(result.status!==0||!report.ok)process.exit(1);
