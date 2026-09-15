#!/usr/bin/env node

import { createHash } from "node:crypto";
import { existsSync, lstatSync, readFileSync, readdirSync } from "node:fs";
import { dirname, relative, resolve, sep } from "node:path";
import { fileURLToPath } from "node:url";

const qaDirectory = dirname(fileURLToPath(import.meta.url));
const packageRoot = resolve(qaDirectory, "..");
const repositoryRoot = resolve(packageRoot, "../..");
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

function isHex(value, length) {
  return typeof value === "string" && new RegExp(`^[0-9a-f]{${length}}$`).test(value);
}

function resolveRepositoryFile(reference, label) {
  if (typeof reference !== "string" || reference.length === 0) {
    fail(`${label} has no repository-relative path.`);
    return null;
  }
  if (reference.startsWith("/") || reference.split("/").includes("..")) {
    fail(`${label} escapes the repository: ${reference}`);
    return null;
  }
  const path = resolve(repositoryRoot, reference);
  const local = relative(repositoryRoot, path);
  if (!local || local === ".." || local.startsWith(`..${sep}`)) {
    fail(`${label} escapes the repository after resolution: ${reference}`);
    return null;
  }
  return path;
}

function walkRegularFiles(root, label, current = root) {
  const files = [];
  for (const entry of readdirSync(current, { withFileTypes: true }).sort((a, b) => a.name.localeCompare(b.name))) {
    if (entry.name === ".DS_Store") continue;
    const path = resolve(current, entry.name);
    if (entry.isDirectory()) {
      files.push(...walkRegularFiles(root, label, path));
    } else if (entry.isFile()) {
      files.push(relative(repositoryRoot, path).split(sep).join("/"));
    } else {
      fail(`${label} contains an unsupported filesystem entry: ${path}`);
    }
  }
  return files;
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

const productionInstructions = packageManifest.productionInstructions;
if (!productionInstructions) {
  fail("Package manifest has no production-instruction binding.");
} else {
  if (productionInstructions.status !== "locked") {
    fail(`Production instructions must be locked, found ${productionInstructions.status}.`);
  }
  if (productionInstructions.semanticCoreExtended !== false) {
    fail("Production instructions must not extend the Boundary Ledger semantic core.");
  }
  if (productionInstructions.motionBindingStatus !== packageManifest.bindings.motion.status) {
    fail("Production-instruction motion status differs from the motion binding status.");
  }
  if (productionInstructions.soundBindingStatus !== packageManifest.bindings.sound.status) {
    fail("Production-instruction sound status differs from the sound binding status.");
  }
  if (productionInstructions.authorityDocument !== packageManifest.entrypoints.productionSkillsAuthority) {
    fail("Production-instruction authority document is not the manifest entrypoint.");
  }

  const lockReference = productionInstructions.lock;
  if (!lockReference || typeof lockReference.path !== "string" || !isHex(lockReference.sha256, 64)) {
    fail("Production-instruction lock must declare a path and SHA-256.");
  } else {
    const lockPath = resolveReference(packageRoot, lockReference.path);
    requireHash(lockPath, lockReference.sha256, "production-instruction lock");
    const lock = readJson(lockPath);

    if (lock) {
      if (lock.schemaVersion !== "1.0.0") fail("OE skill lock schemaVersion must be 1.0.0.");
      if (lock.status !== "locked") fail(`OE skill lock status must be locked, found ${lock.status}.`);
      if (lock.lockedOn !== productionInstructions.lockedOn) {
        fail("OE skill lock date differs from the production-instruction binding.");
      }
      if (lock.hashAlgorithm !== "sha256") fail("OE skill lock hashAlgorithm must be sha256.");
      if (!Array.isArray(lock.roots) || lock.roots.length === 0) fail("OE skill lock roots must be non-empty.");
      if (!Array.isArray(lock.additionalFiles)) fail("OE skill lock additionalFiles must be an array.");
      if (!Array.isArray(lock.files) || lock.files.length === 0) fail("OE skill lock files must be non-empty.");

      const declaredFiles = new Map();
      for (const entry of lock.files || []) {
        if (!entry || typeof entry.path !== "string" || !isHex(entry.sha256, 64)) {
          fail(`OE skill lock contains an invalid file entry: ${JSON.stringify(entry)}.`);
          continue;
        }
        if (declaredFiles.has(entry.path)) {
          fail(`OE skill lock contains duplicate file ${entry.path}.`);
          continue;
        }
        declaredFiles.set(entry.path, entry.sha256);
        const filePath = resolveRepositoryFile(entry.path, `OE skill file ${entry.path}`);
        if (filePath) {
          if (existsSync(filePath) && !lstatSync(filePath).isFile()) {
            fail(`OE skill lock target is not a regular file: ${entry.path}.`);
          } else {
            requireHash(filePath, entry.sha256, `OE skill file ${entry.path}`);
          }
        }
      }

      const expectedFiles = new Set();
      for (const reference of lock.additionalFiles || []) {
        const filePath = resolveRepositoryFile(reference, `OE skill additional file ${reference}`);
        if (filePath && requirePath(filePath, `OE skill additional file ${reference}`)) {
          if (!lstatSync(filePath).isFile()) fail(`OE skill additional file is not regular: ${reference}.`);
          expectedFiles.add(reference);
        }
      }
      for (const reference of lock.roots || []) {
        const rootPath = resolveRepositoryFile(reference, `OE skill root ${reference}`);
        if (rootPath && requirePath(rootPath, `OE skill root ${reference}`)) {
          if (!lstatSync(rootPath).isDirectory()) {
            fail(`OE skill root is not a directory: ${reference}.`);
          } else {
            for (const file of walkRegularFiles(rootPath, `OE skill root ${reference}`)) expectedFiles.add(file);
          }
        }
      }
      for (const file of expectedFiles) {
        if (!declaredFiles.has(file)) fail(`OE skill file is inside lock scope but not declared: ${file}.`);
      }
      for (const file of declaredFiles.keys()) {
        if (!expectedFiles.has(file)) fail(`OE skill lock declares a file outside its scope: ${file}.`);
      }

      const repositoryLockPath = relative(repositoryRoot, lockPath).split(sep).join("/");
      if (!(lock.excludedFiles || []).includes(repositoryLockPath)) {
        fail("OE skill lock must exclude itself to avoid a hash cycle.");
      }

      const sourceLedgerReference = lock.sourceLedger;
      if (!sourceLedgerReference || typeof sourceLedgerReference.path !== "string" || !isHex(sourceLedgerReference.sha256, 64)) {
        fail("OE skill lock must declare its source ledger and SHA-256.");
      } else {
        const sourceLedgerPath = resolveRepositoryFile(sourceLedgerReference.path, "OE skill source ledger");
        if (sourceLedgerPath) {
          requireHash(sourceLedgerPath, sourceLedgerReference.sha256, "OE skill source ledger");
          if (declaredFiles.get(sourceLedgerReference.path) !== sourceLedgerReference.sha256) {
            fail("OE skill source ledger is not declared with the same hash in the local-file lock.");
          }
          const sourceLedger = readJson(sourceLedgerPath);
          if (sourceLedger) {
            if (sourceLedger.schemaVersion !== "1.0.0") fail("OE source ledger schemaVersion must be 1.0.0.");
            if (sourceLedger.hashAlgorithm !== "sha256") fail("OE source ledger hashAlgorithm must be sha256.");
            if (sourceLedger.authority !== "reference-only") fail("OE source ledger must remain reference-only.");

            const expectedSourceIds = new Set(lock.expectedSourceIds || []);
            const sourceIds = new Set();
            for (const source of sourceLedger.sources || []) {
              if (!source || typeof source.id !== "string") {
                fail("OE source ledger contains a source without an id.");
                continue;
              }
              if (sourceIds.has(source.id)) fail(`OE source ledger contains duplicate id ${source.id}.`);
              sourceIds.add(source.id);
              if (!isHex(source.commit, 40)) fail(`OE source ${source.id} has an invalid commit.`);
              if (!source.license || !source.attribution) {
                fail(`OE source ${source.id} is missing license or attribution.`);
              }
              if (!Array.isArray(source.adoptedPrinciples) || source.adoptedPrinciples.length === 0) {
                fail(`OE source ${source.id} has no adopted principles.`);
              }
              if (!Array.isArray(source.excludedPrinciples) || source.excludedPrinciples.length === 0) {
                fail(`OE source ${source.id} has no excluded principles.`);
              }
              const sourcePaths = new Set();
              for (const entry of source.files || []) {
                if (!entry || typeof entry.path !== "string" || !isHex(entry.sha256, 64)) {
                  fail(`OE source ${source.id} contains an invalid file declaration.`);
                  continue;
                }
                if (entry.path.startsWith("/") || entry.path.split("/").includes("..")) {
                  fail(`OE source ${source.id} path escapes its checkout: ${entry.path}.`);
                }
                if (sourcePaths.has(entry.path)) fail(`OE source ${source.id} repeats path ${entry.path}.`);
                sourcePaths.add(entry.path);
              }
            }
            for (const id of expectedSourceIds) {
              if (!sourceIds.has(id)) fail(`OE source ledger omits expected source ${id}.`);
            }
            for (const id of sourceIds) {
              if (!expectedSourceIds.has(id)) fail(`OE source ledger contains undeclared source ${id}.`);
            }
          }
        }
      }
    }
  }
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
