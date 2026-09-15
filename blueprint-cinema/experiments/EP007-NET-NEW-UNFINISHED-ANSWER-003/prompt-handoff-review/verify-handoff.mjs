// Read-only provenance and coverage check. No semantic scoring or gate decisions.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import assert from 'node:assert/strict';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const repo = path.resolve(here, '../../../..');
const intakePath = 'operator-blueprint-v2/episodes/EP007-exit-readiness-prep/03-visual-translation/input-lock.json';
const intakeHash = '9adde76470b05da2d635521e8711e4d55ed76353a1479db50ba430449899a384';
const sum = file => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex');
const json = file => JSON.parse(fs.readFileSync(file, 'utf8'));
const intakeFile = path.join(repo, intakePath);
assert.equal(sum(intakeFile), intakeHash, 'Current intake changed; review, do not silently re-pin.');
const intake = json(intakeFile);
const inputDir = path.dirname(intakeFile);
const inputs = Object.entries(intake.input_lock)
  .filter(([, value]) => value && typeof value === 'object' && value.path)
  .map(([id, value]) => {
    const file = path.resolve(inputDir, value.path);
    const actual = sum(file);
    assert.equal(actual, value.sha256, `${id}: input hash mismatch`);
    return { id, path: path.relative(repo, file), sha256: actual, matches: true };
  });
assert.equal(inputs.length, 13);
const inputFile = id => path.join(repo, inputs.find(row => row.id === id).path);
const lockReferencedArtifacts = [];
for (const id of ['editorial_lock', 'narration_lock']) {
  const lockFile = inputFile(id);
  const lockText = fs.readFileSync(lockFile, 'utf8');
  for (const match of lockText.matchAll(/^\| ([^|]+) \| `([^`]+)` \| `([a-f0-9]{64})` \|$/gm)) {
    const file = path.resolve(path.dirname(lockFile), match[2]);
    const actual = sum(file);
    assert.equal(actual, match[3], `${id}: frozen artifact ${match[2]} changed`);
    lockReferencedArtifacts.push({ lock: id, artifact: match[1].trim(), path: path.relative(repo, file), sha256: actual });
  }
}
assert.equal(lockReferencedArtifacts.length, 21);
const uniqueSourceCount = new Set([...inputs, ...lockReferencedArtifacts].map(row => row.path)).size;
assert.equal(uniqueSourceCount, 23);
const additionalPerformanceReference = {
  path: 'operator-blueprint-v2/episodes/EP007-exit-readiness-prep/01-editorial/narration-handoff.md',
  sha256: '090ec58c14849b65f8b20c773e0c5cb66c0fd8049028c320d9a8a2472f50e5bc',
  authority: 'Issued upstream reference; not frozen by the current V1/E6/N7 route. Receiving authority unresolved.'
};
assert.equal(sum(path.join(repo, additionalPerformanceReference.path)), additionalPerformanceReference.sha256);
const processFile = path.resolve(inputDir, intake.process_lock.path);
assert.equal(sum(processFile), intake.process_lock.sha256);

const transcript = json(inputFile('word_transcript'));
const pauses = json(inputFile('intentional_pause_map'));
const script = fs.readFileSync(inputFile('script'), 'utf8');
const canonical = fs.readFileSync(inputFile('canonical_w'), 'utf8').trim().split(/\s+/);
assert.equal(transcript.master_sha256, sum(inputFile('narration_master')));
assert.equal(pauses.master_sha256, transcript.master_sha256);
assert.equal(pauses.master_duration_seconds, transcript.master_duration_seconds);
assert.equal(transcript.master_duration_seconds, 1137.927);
assert.equal(transcript.words.length, 3186);
assert.equal(transcript.w_token_count, canonical.length);
assert.deepEqual(transcript.words.map(word => word.token), canonical);
assert.equal(pauses.pauses.length, pauses.pause_count);
assert.equal(pauses.pause_count, 276);
assert.equal(transcript.canonical_w_sha256, sum(inputFile('canonical_w')));

let cursor = 0;
const sections = [];
const sectionPattern = /^## (S\d+): ([^\n]+)\n([\s\S]*?)(?=^## S\d+:|$(?![\s\S]))/gm;
for (const match of script.matchAll(sectionPattern)) {
  const narrated = match[3].match(/### Narration\s+([\s\S]*?)(?=### Editorial check)/);
  if (!narrated) {
    assert.equal(match[1], 'S01');
    const gap = pauses.pauses.find(pause => pause.after_w_id === 'W000117');
    assert.deepEqual([gap.start, gap.end], [44.5, 48.52]);
    sections.push({ id: match[1], title: match[2], words: null, start: gap.start, end: gap.end, source: 'pause map after W000117' });
    continue;
  }
  const words = narrated[1].trim().split(/\s+/);
  assert.deepEqual(words, canonical.slice(cursor, cursor + words.length), `${match[1]}: words changed`);
  sections.push({ id: match[1], title: match[2], words: [cursor, cursor + words.length], start: transcript.words[cursor].start, end: transcript.words[cursor + words.length - 1].end });
  cursor += words.length;
}
assert.equal(cursor, canonical.length);
assert.equal(sections.length, 27);
const brief = fs.readFileSync(path.join(here, 'EP007-BEAT-INTENT.md'), 'utf8');
const rows = brief.split('\n').filter(line => /^\| S\d\d ·/.test(line));
assert.equal(rows.length, 27, 'One brief row per script section, including silent S01');
for (const [index, section] of sections.entries()) {
  assert.ok(rows[index].startsWith(`| ${section.id} ·`), 'Source section order changed');
  if (!section.words) continue;
  const range = rows[index].match(/`\[(\d+),(\d+)\)` · ([\d.]+)–([\d.]+)/);
  assert.ok(range, `${section.id}: missing bound range`);
  assert.deepEqual(range.slice(1, 3).map(Number), section.words);
  assert.deepEqual(range.slice(3, 5).map(Number), [section.start, section.end]);
}

const preserved = {
  'hyperframes/index.html': '2b1e501a0102dbbf3df3d2f89872b5579b9ad01113784c18053e493bcda19692',
  'hyperframes/compositions/sequences/02-question-answer.html': '13cf504de5b3ec37245c257aa959fdc33d6dd778e6d62fdb131448c0d5606b57',
  'hyperframes/compositions/sequences/03-model-exposure.html': 'daa513b6979b7a754ee553204fcdbcfd1af90e3afc231d579e18a05f13cdfd6f',
  'hyperframes/reviews/r3-relevant-edit/index.html': '10551d259352d8d3b1ab0476eeca1646faa6f6962e57d04e24eb7a26c933ee24',
  'hyperframes/reviews/r3-relevant-edit/compositions/model-exposure.html': '0d4fa07954d85e9f70e4f0f5c6405a0c9e479b442ac2fe706f3d9fd7bc6ee82a',
  'hyperframes/reviews/r3-relevant-edit/candidate.mp4': '7c71e1feba373fae1e3710038e42eb734814945e35865fa486f0571099429ac2',
  'hyperframes/reviews/r3-relevant-edit/public/audio/opening-narration.wav': '120c7a64ae8582f55f9bb4338c9ec276d763d79d88718aac482fc81c48ddbfb1',
};
for (const [relative, expected] of Object.entries(preserved)) {
  assert.equal(sum(path.resolve(here, '..', relative)), expected, `${relative}: review media/source changed`);
}

console.log(JSON.stringify({
  status: 'mechanical-input-and-coverage-check-passed',
  creativeApproval: false,
  gateAdvance: false,
  intakePath, intakeHash,
  processPath: path.relative(repo, processFile), processHash: sum(processFile),
  inputs, lockReferencedArtifacts, uniqueSourceCount, additionalPerformanceReference,
  wordCount: cursor, sectionCount: sections.length,
  durationSeconds: transcript.master_duration_seconds,
  pauseCount: pauses.pause_count, sections,
  preservedReviewAndOriginalFiles: Object.keys(preserved).length,
  limitations: [
    'This checker does not score prompt quality, comprehension, evidence fidelity or creative approval.',
    'Spoken section spans are not a continuous V4 visual plan; intentional gaps and handles need later picture allocation.',
    'Existing process and Boundary Ledger validators remain separate; no source or policy is repaired here.'
  ]
}, null, 2));
