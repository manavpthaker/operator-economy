#!/usr/bin/env node

import { createHash } from "node:crypto";
import { spawnSync } from "node:child_process";
import { readFileSync, writeFileSync } from "node:fs";
import { basename, resolve } from "node:path";

const [inputArg, outputArg] = process.argv.slice(2);

if (!inputArg || !outputArg) {
  console.error("Usage: node build-audio-envelope.mjs <input-audio> <output-json>");
  process.exit(2);
}

const input = resolve(inputArg);
const output = resolve(outputArg);
const sampleRate = 16000;
const windowMs = 50;
const samplesPerWindow = Math.round((sampleRate * windowMs) / 1000);

const decoded = spawnSync(
  "ffmpeg",
  ["-v", "error", "-i", input, "-ac", "1", "-ar", String(sampleRate), "-f", "f32le", "pipe:1"],
  { encoding: null, maxBuffer: 128 * 1024 * 1024 }
);

if (decoded.status !== 0) {
  process.stderr.write(decoded.stderr || Buffer.from("ffmpeg failed\n"));
  process.exit(decoded.status || 1);
}

const pcm = decoded.stdout;
const sampleCount = Math.floor(pcm.byteLength / 4);
const rms = [];

for (let start = 0; start < sampleCount; start += samplesPerWindow) {
  const end = Math.min(start + samplesPerWindow, sampleCount);
  let sumSquares = 0;
  for (let index = start; index < end; index += 1) {
    const value = pcm.readFloatLE(index * 4);
    sumSquares += value * value;
  }
  rms.push(Math.sqrt(sumSquares / Math.max(1, end - start)));
}

const sorted = [...rms].sort((a, b) => a - b);
const reference = sorted[Math.max(0, Math.floor(sorted.length * 0.95) - 1)] || 1;
const values = rms.map((value) => Number(Math.min(1, value / reference).toFixed(4)));
const sourceBytes = readFileSync(input);
const sourceSha256 = createHash("sha256").update(sourceBytes).digest("hex");
const durationSeconds = Number((sampleCount / sampleRate).toFixed(4));

const document = {
  schemaVersion: "1.0",
  source: {
    file: basename(input),
    sha256: sourceSha256,
    durationSeconds
  },
  extraction: {
    tool: "ffmpeg f32le + deterministic RMS",
    sampleRate,
    channels: 1,
    windowMs,
    normalization: "95th-percentile RMS",
    runtimeWebAudio: false
  },
  values
};

writeFileSync(output, `${JSON.stringify(document, null, 2)}\n`);
console.log(`Wrote ${values.length} windows across ${durationSeconds}s to ${output}`);
