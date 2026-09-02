#!/usr/bin/env node

import { createHash } from "node:crypto";
import { existsSync, readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const qaDirectory = dirname(fileURLToPath(import.meta.url));
const packageRoot = resolve(qaDirectory, "..");
const errors = [];
const warnings = [];
const checked = [];

function fail(message) {
  errors.push(message);
}

function warn(message) {
  warnings.push(message);
}

function readJson(path) {
  try {
    const value = JSON.parse(readFileSync(path, "utf8"));
    checked.push(path);
    return value;
  } catch (error) {
    fail(`Cannot parse ${path}: ${error.message}`);
    return null;
  }
}

function sha256(path) {
  return createHash("sha256").update(readFileSync(path)).digest("hex");
}

function resolveReference(baseDirectory, reference) {
  return resolve(baseDirectory, reference);
}

function requirePath(path, label) {
  if (!existsSync(path)) {
    fail(`${label} does not exist: ${path}`);
    return false;
  }
  checked.push(path);
  return true;
}

function requireHash(path, expected, label) {
  if (!requirePath(path, label)) return;
  const actual = sha256(path);
  if (actual !== expected) fail(`${label} hash mismatch: expected ${expected}, found ${actual}`);
}

function uniqueIds(items, label) {
  const seen = new Set();
  for (const item of items || []) {
    if (!item || typeof item.id !== "string") {
      fail(`${label} contains an item without an id.`);
      continue;
    }
    if (seen.has(item.id)) fail(`${label} contains duplicate id ${item.id}.`);
    seen.add(item.id);
  }
  return seen;
}

const packageManifest = readJson(resolve(packageRoot, "manifest.json"));
const core = readJson(resolve(packageRoot, "semantic-core.json"));

if (!packageManifest || !core) {
  console.error(JSON.stringify({ ok: false, errors, warnings, checked: checked.length }, null, 2));
  process.exit(1);
}

if (packageManifest.version !== core.version) {
  fail(`Package version ${packageManifest.version} does not match semantic core ${core.version}.`);
}

const roleIds = uniqueIds(core.roles, "semantic roles");
const operationIds = uniqueIds(core.operations, "semantic operations");
uniqueIds(core.invariants, "universal invariants");

requireHash(
  resolveReference(packageRoot, packageManifest.semanticCore.path),
  packageManifest.semanticCore.sha256,
  "semantic core"
);

for (const [name, bindingRef] of Object.entries(packageManifest.bindings || {})) {
  const bindingPath = resolveReference(packageRoot, bindingRef.path);
  requireHash(bindingPath, bindingRef.sha256, `${name} binding`);
  const binding = readJson(bindingPath);
  if (!binding) continue;

  if (binding.systemVersion !== core.version) {
    fail(`${name} binding version ${binding.systemVersion} does not match semantic core ${core.version}.`);
  }
  if (binding.medium !== name) fail(`${name} binding declares medium ${binding.medium}.`);

  const bindingRoleIds = new Set(Object.keys(binding.roles || {}));
  for (const roleId of bindingRoleIds) {
    if (!roleIds.has(roleId)) fail(`${name} binding invents unknown role ${roleId}.`);
  }
  for (const roleId of roleIds) {
    if (!bindingRoleIds.has(roleId)) fail(`${name} binding omits core role ${roleId}.`);
  }

  if (name === "motion") {
    for (const [roleId, expression] of Object.entries(binding.roles || {})) {
      const operations = Array.isArray(expression.expression)
        ? expression.expression
        : [expression.expression];
      for (const operation of operations) {
        if (!operationIds.has(operation)) {
          fail(`Motion binding ${roleId} references invented operation ${operation}.`);
        }
      }
    }
  }
}

for (const [name, reference] of Object.entries(packageManifest.entrypoints || {})) {
  requirePath(resolveReference(packageRoot, reference), `entrypoint ${name}`);
}

const referenceAssetPath = resolveReference(packageRoot, packageManifest.referenceAsset.path);
requireHash(referenceAssetPath, packageManifest.referenceAsset.sha256, "locked reference illustration");

const specimenManifestPath = resolveReference(packageRoot, packageManifest.specimens.audioFirst.path);
requireHash(specimenManifestPath, packageManifest.specimens.audioFirst.sha256, "audio-first specimen manifest");
const specimen = readJson(specimenManifestPath);

if (specimen) {
  const specimenDirectory = dirname(specimenManifestPath);
  if (specimen.systemVersion !== core.version) {
    fail(`Specimen system version ${specimen.systemVersion} does not match semantic core ${core.version}.`);
  }

  const audioPath = resolveReference(specimenDirectory, specimen.sourceAudio.path);
  requireHash(audioPath, specimen.sourceAudio.sha256, "specimen source audio");
  const sourceMasterPath = resolveReference(specimenDirectory, specimen.sourceAudio.sourceMaster.path);
  requireHash(sourceMasterPath, specimen.sourceAudio.sourceMaster.sha256, "specimen source-audio master");
  if (Math.abs(specimen.sourceAudio.sourceMaster.durationSeconds - specimen.sourceAudio.durationSeconds) > 0.01) {
    fail("Source-audio master duration does not match the browser-reference audio duration.");
  }

  const timingPath = resolveReference(specimenDirectory, specimen.timingData.path);
  requireHash(timingPath, specimen.timingData.sha256, "specimen timing data");
  const timing = readJson(timingPath);
  if (timing) {
    if (Math.abs(timing.durationSeconds - specimen.sourceAudio.durationSeconds) > 0.01) {
      fail("Timing-data duration does not match the specimen audio duration.");
    }
    if (JSON.stringify(timing.captions) !== JSON.stringify(specimen.captions.cues)) {
      fail("Browser timing captions drift from the pinned specimen caption cues.");
    }
    const pinnedEmbeddedTiming = {
      text: specimen.captions.embeddedPhrase.text,
      start: specimen.captions.embeddedPhrase.start,
      end: specimen.captions.embeddedPhrase.end
    };
    if (JSON.stringify(timing.embeddedPhrase) !== JSON.stringify(pinnedEmbeddedTiming)) {
      fail("Browser embedded phrase drifts from the pinned specimen caption policy.");
    }
  }

  const tracePath = resolveReference(specimenDirectory, specimen.voiceTrace.data);
  requireHash(tracePath, specimen.voiceTrace.sha256, "specimen voice trace");
  const trace = readJson(tracePath);
  if (trace) {
    if (trace.source.sha256 !== specimen.sourceAudio.sha256) {
      fail("Voice trace source hash does not match the delivered specimen audio.");
    }
    if (Math.abs(trace.source.durationSeconds - specimen.sourceAudio.durationSeconds) > 0.01) {
      fail("Voice trace duration does not match the specimen audio duration.");
    }
    if (trace.extraction.runtimeWebAudio !== false || specimen.voiceTrace.runtimeWebAudio !== false) {
      fail("Audio-linked data must be precomputed; runtime Web Audio is prohibited.");
    }
    if (timing) {
      const timingTracePath = resolveReference(dirname(timingPath), timing.envelope);
      if (timingTracePath !== tracePath) {
        fail("Browser timing data does not resolve to the pinned voice-trace artifact.");
      }
      const timingAudioPath = resolveReference(dirname(timingPath), timing.audio);
      if (timingAudioPath !== audioPath) {
        fail("Browser timing data does not resolve to the pinned source-audio artifact.");
      }
    }
  }

  for (const event of specimen.semanticEvents || []) {
    if (!operationIds.has(event.operation)) fail(`Specimen event ${event.id} uses unknown operation ${event.operation}.`);
    if (!roleIds.has(event.role)) fail(`Specimen event ${event.id} uses unknown role ${event.role}.`);
    if (!(event.start >= 0 && event.end > event.start && event.end <= specimen.sourceAudio.durationSeconds + 0.001)) {
      fail(`Specimen event ${event.id} has invalid bounds ${event.start}–${event.end}.`);
    }
    if (event.stateBefore === event.stateAfter) fail(`Specimen event ${event.id} has no state change.`);
    if (event.role === "activeCommitment" && !event.commitmentLocus) {
      fail(`Active commitment event ${event.id} must declare a commitment locus.`);
    }
    if (event.role !== "activeCommitment" && event.commitmentLocus) {
      fail(`Non-commitment event ${event.id} declares commitment locus ${event.commitmentLocus}.`);
    }
  }

  const commitmentEvents = (specimen.semanticEvents || []).filter((event) => event.commitmentLocus);
  for (let left = 0; left < commitmentEvents.length; left += 1) {
    for (let right = left + 1; right < commitmentEvents.length; right += 1) {
      const a = commitmentEvents[left];
      const b = commitmentEvents[right];
      if (Math.max(a.start, b.start) < Math.min(a.end, b.end)) {
        fail(`Commitment loci ${a.commitmentLocus} and ${b.commitmentLocus} overlap.`);
      }
    }
  }

  if (specimen.captions.policy !== "drop-rail-embed") {
    fail(`Specimen caption policy must be drop-rail-embed, found ${specimen.captions.policy}.`);
  }
  const embedded = specimen.captions.embeddedPhrase;
  const embeddedText = embedded.text.toLowerCase().replace(/[.?!,]/g, "");
  const matchingCue = (specimen.captions.cues || []).find((cue) => {
    const cueText = cue.text.toLowerCase().replace(/[.?!,]/g, "");
    return cue.start <= embedded.start && cue.end >= embedded.end && cueText.includes(embeddedText);
  });
  if (!matchingCue) fail("Embedded thesis phrase does not resolve to one exact timed caption cue.");
  if (embedded.captionDuplicateVisible !== false) fail("Embedded phrase must not remain duplicated in the visible caption rail.");

  for (const format of specimen.formats || []) {
    if (format.cropBased !== false) fail(`Specimen format ${format.id} is crop-based.`);
  }

  if (!specimen.review.browserChecked) warn("Audio-first specimen exists but browser review is not yet recorded.");
  if (!specimen.review.encodedMediaChecked) warn("Audio-first specimen has no encoded-media verification.");
  if (!specimen.review.motionReadyModelProven) warn("Flattened illustration does not prove a motion-ready Working Model asset.");
}

const retirementManifestPath = resolveReference(packageRoot, packageManifest.legacy.retirementManifest);
requireHash(retirementManifestPath, packageManifest.legacy.retirementManifestSha256, "retirement manifest");
const retirement = readJson(retirementManifestPath);

if (retirement) {
  if (retirement.systemVersion !== core.version) {
    fail(`Retirement manifest version ${retirement.systemVersion} does not match semantic core ${core.version}.`);
  }
  uniqueIds(retirement.consumers, "retirement consumers");
  for (const consumer of retirement.consumers || []) {
    requirePath(resolveReference(packageRoot, consumer.path), `retirement consumer ${consumer.id}`);
    if (consumer.allowedForNewWork !== false) fail(`Retired consumer ${consumer.id} is allowed for new work.`);
    if (consumer.status === "verified" && !consumer.verificationEvidence) {
      fail(`Verified retirement consumer ${consumer.id} has no verification evidence.`);
    }
  }
}

const report = {
  ok: errors.length === 0,
  system: "Boundary Ledger",
  version: core.version,
  checkedPaths: new Set(checked).size,
  roles: roleIds.size,
  operations: operationIds.size,
  errors,
  warnings
};

console.log(JSON.stringify(report, null, 2));
process.exit(errors.length ? 1 : 0);
