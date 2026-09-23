import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { Workbook, SpreadsheetFile } from '@oai/artifact-tool';

const out = path.dirname(fileURLToPath(import.meta.url));
const wb = Workbook.create();
const sheets = ['Readiness checklist', 'Package index', 'Interview notes'].map(n => wb.worksheets.add(n));
const title = 'Example Cabinet Workshop';
const disclosure = 'ILLUSTRATIVE EXAMPLE / NOT A CLIENT CASE';
const rows = [
  ['Quote → order handoff', 'Documented', '02-order-handoff.md', 'Exception prices still need owner approval.'],
  ['JOB-014 records', 'Linked', '03-job014-record-index.csv', 'Specification, quote and release note use the same job ID.'],
  ['Non-standard quote approval', 'Unresolved', '01-owner-interview.md · Q3', 'Only the owner can approve exceptions; no backup is authorised.'],
];
const packageRows = [
  ['01-owner-interview.md', 'Owner interview', 'Source notes', 'Owner approval and handoff practice'],
  ['02-order-handoff.md', 'Order handoff', 'Process draft', 'Specification → quote → approval → release'],
  ['03-job014-record-index.csv', 'JOB-014 records', 'Record index', 'Related records use the same job ID'],
];
const interviewRows = JSON.parse(await fs.readFile(path.join(out, 'interview-rows.json'), 'utf8'));
for (const s of sheets) {
  s.getRange('A1:D9').format.font = { name: 'Arial', size: 15, color: '#202124' };
  s.getRange('A1:D9').format.verticalAlignment = 'center';
  s.getRange('A1:D9').format.wrapText = true;
  s.getRange('A1:D9').format.fill = '#FFFFFF';
  s.getRange('A1:D1').format.rowHeightPx = 40;
  s.getRange('A2:D2').format.rowHeightPx = 30;
  s.getRange('A3:D3').format.rowHeightPx = 15;
  s.getRange('A4:D4').format.rowHeightPx = 38;
  s.getRange('A5:D7').format.rowHeightPx = 94;
  s.getRange('A8:D9').format.rowHeightPx = 26;
  s.getRange('A1:D2').format.wrapText = false;
  s.getRange('A1').values = [[title]];
  s.getRange('A1').format.font = { name: 'Arial', size: 21, bold: true, color: '#202124' };
  s.getRange('A2').values = [[disclosure]];
  s.getRange('A2').format.font = { name: 'Arial', size: 12, color: '#5F6368' };
  s.getRange('A4:D4').format.fill = '#F1F3F4';
  s.getRange('A4:D4').format.font = { name: 'Arial', size: 15, bold: true, color: '#202124' };
  s.getRange('A4:D7').format.borders = {insideHorizontal: {style:'thin', color:'#DADCE0'}};
  s.getRange('A1:A9').format.columnWidthPx = 245;
  s.getRange('B1:B9').format.columnWidthPx = 160;
  s.getRange('C1:C9').format.columnWidthPx = 280;
  s.getRange('D1:D9').format.columnWidthPx = 420;
}
sheets[0].getRange('A4:D7').values = [['Check','Status','Evidence','Reason'], ...rows];
sheets[1].getRange('A4:D7').values = [['File','Content','Type','Purpose'], ...packageRows];
sheets[2].getRange('A4:D7').values = [['Ref','Topic','Source excerpt','Implication'], ...interviewRows];
sheets[1].getRange('A1:A9').format.columnWidthPx = 310;
sheets[1].getRange('C1:C9').format.columnWidthPx = 215;
sheets[2].getRange('A1:A9').format.columnWidthPx = 70;
sheets[2].getRange('B1:B9').format.columnWidthPx = 205;
sheets[2].getRange('C1:C9').format.columnWidthPx = 490;
sheets[2].getRange('D1:D9').format.columnWidthPx = 340;
sheets[0].getRange('B5:B7').conditionalFormats.addCustom('B5="Unresolved"', {font:{bold:true,color:'#202124'},fill:'#FFF4CE'});
wb.recalculate();
const checks = [];
for (const s of sheets) {
  checks.push((await wb.inspect({kind:'table',sheetId:s.name,range:'A1:D7',include:'values,formulas',maxChars:5000,tableMaxRows:7,tableMaxCols:4})).ndjson);
  const blob = await wb.render({sheetName:s.name,range:'A1:D8',scale:1,format:'png'});
  await fs.writeFile(path.join(out, `${s.name.toLowerCase().replaceAll(' ','-')}.png`), new Uint8Array(await blob.arrayBuffer()));
}
checks.push((await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!',options:{useRegex:true,maxResults:30},summary:'Formula error scan'})).ndjson);
await fs.writeFile(path.join(out,'local-checks.ndjson'),checks.join('\n'));
const xlsx = await SpreadsheetFile.exportXlsx(wb);
await xlsx.save(path.join(out,'seed.xlsx'));
console.log(JSON.stringify({created:'seed.xlsx',sheets:sheets.map(s=>s.name),recordingCells:['Readiness checklist!B7','Readiness checklist!D7'],formulaErrors:false}));
