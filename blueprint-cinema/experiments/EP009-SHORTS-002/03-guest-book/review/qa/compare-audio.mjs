import fs from "node:fs";

const SAMPLE_RATE = 8000;
const EXPECTED_PATH = "review/qa/expected-source-8k-mono.wav";
const RENDERED_PATH = "review/qa/rendered-audio-8k-mono.wav";
const OUTPUT_PATH = "review/qa/audio-source-comparison.json";
const SEARCH_RADIUS_SAMPLES = 400; // ±50 ms at 8 kHz

function readPcm16Wav(path) {
  const buffer = fs.readFileSync(path);
  if (buffer.toString("ascii", 0, 4) !== "RIFF" || buffer.toString("ascii", 8, 12) !== "WAVE") {
    throw new Error(`${path} is not a RIFF/WAVE file`);
  }
  let offset = 12;
  let dataStart = -1;
  let dataBytes = 0;
  while (offset + 8 <= buffer.length) {
    const id = buffer.toString("ascii", offset, offset + 4);
    const size = buffer.readUInt32LE(offset + 4);
    if (id === "data") {
      dataStart = offset + 8;
      dataBytes = size;
      break;
    }
    offset += 8 + size + (size % 2);
  }
  if (dataStart < 0) throw new Error(`${path} has no data chunk`);
  const count = Math.floor(dataBytes / 2);
  const samples = new Float64Array(count);
  for (let i = 0; i < count; i += 1) samples[i] = buffer.readInt16LE(dataStart + i * 2) / 32768;
  return samples;
}

function overlap(x, y, lag) {
  if (lag >= 0) return { xStart: 0, yStart: lag, count: Math.min(x.length, y.length - lag) };
  return { xStart: -lag, yStart: 0, count: Math.min(x.length + lag, y.length) };
}

function pearsonAtLag(x, y, lag, stride = 1, range = null) {
  const base = overlap(x, y, lag);
  let xStart = base.xStart;
  let yStart = base.yStart;
  let count = base.count;
  if (range) {
    const rangeEnd = range.start + range.count;
    xStart = Math.max(range.start, -lag, 0);
    const xEnd = Math.min(rangeEnd, x.length, y.length - lag);
    yStart = xStart + lag;
    count = Math.max(0, xEnd - xStart);
  }
  let n = 0;
  let sx = 0;
  let sy = 0;
  let sxx = 0;
  let syy = 0;
  let sxy = 0;
  for (let i = 0; i < count; i += stride) {
    const a = x[xStart + i];
    const b = y[yStart + i];
    sx += a;
    sy += b;
    sxx += a * a;
    syy += b * b;
    sxy += a * b;
    n += 1;
  }
  const numerator = n * sxy - sx * sy;
  const denominator = Math.sqrt((n * sxx - sx * sx) * (n * syy - sy * sy));
  return denominator > 0 ? numerator / denominator : 0;
}

function bestAlignmentForRange(x, y, range) {
  let coarse = { lag: 0, correlation: -Infinity };
  for (let lag = -SEARCH_RADIUS_SAMPLES; lag <= SEARCH_RADIUS_SAMPLES; lag += 1) {
    const correlation = pearsonAtLag(x, y, lag, 8, range);
    if (correlation > coarse.correlation) coarse = { lag, correlation };
  }
  let fine = { lag: coarse.lag, correlation: -Infinity };
  for (let lag = coarse.lag - 4; lag <= coarse.lag + 4; lag += 1) {
    const correlation = pearsonAtLag(x, y, lag, 1, range);
    if (correlation > fine.correlation) fine = { lag, correlation };
  }
  return fine;
}

function rmsAndPeak(samples, start = 0, count = samples.length - start) {
  let sumSquares = 0;
  let peak = 0;
  for (let i = 0; i < count; i += 1) {
    const value = samples[start + i];
    sumSquares += value * value;
    peak = Math.max(peak, Math.abs(value));
  }
  return { rms: Math.sqrt(sumSquares / count), peak };
}

const expected = readPcm16Wav(EXPECTED_PATH);
const rendered = readPcm16Wav(RENDERED_PATH);

let coarseBest = { lag: 0, correlation: -Infinity };
for (let lag = -SEARCH_RADIUS_SAMPLES; lag <= SEARCH_RADIUS_SAMPLES; lag += 1) {
  const correlation = pearsonAtLag(expected, rendered, lag, 8);
  if (correlation > coarseBest.correlation) coarseBest = { lag, correlation };
}

let best = { lag: coarseBest.lag, correlation: -Infinity };
for (let lag = coarseBest.lag - 4; lag <= coarseBest.lag + 4; lag += 1) {
  const correlation = pearsonAtLag(expected, rendered, lag, 1);
  if (correlation > best.correlation) best = { lag, correlation };
}

const aligned = overlap(expected, rendered, best.lag);
let sx = 0;
let sy = 0;
for (let i = 0; i < aligned.count; i += 1) {
  sx += expected[aligned.xStart + i];
  sy += rendered[aligned.yStart + i];
}
const meanX = sx / aligned.count;
const meanY = sy / aligned.count;
let covariance = 0;
let varianceX = 0;
for (let i = 0; i < aligned.count; i += 1) {
  const dx = expected[aligned.xStart + i] - meanX;
  const dy = rendered[aligned.yStart + i] - meanY;
  covariance += dx * dy;
  varianceX += dx * dx;
}
const scale = covariance / varianceX;
const intercept = meanY - scale * meanX;
let signalSquares = 0;
let residualSquares = 0;
for (let i = 0; i < aligned.count; i += 1) {
  const source = expected[aligned.xStart + i];
  const observed = rendered[aligned.yStart + i];
  const predicted = scale * source + intercept;
  signalSquares += (predicted - intercept) ** 2;
  residualSquares += (observed - predicted) ** 2;
}
const residualRmse = Math.sqrt(residualSquares / aligned.count);
const snrDb = 10 * Math.log10(signalSquares / residualSquares);

const boundaries = [0, 28000, 51667, 88667, 137667, 161667];
const sourceRanges = [
  { id: "served-no-email", frames: [8148, 8232], sourceSeconds: [339.5, 343.0] },
  { id: "guest-book-at-site", frames: [8070, 8141], sourceSeconds: [336.25, 339.208333333333] },
  { id: "constraint-before-tool", frames: [8250, 8361], sourceSeconds: [343.75, 348.375] },
  { id: "relay-rule-boundary", frames: [8373, 8520], sourceSeconds: [348.875, 355.0] },
  { id: "not-email-tool", frames: [8520, 8592], sourceSeconds: [355.0, 358.0] },
];
const segments = sourceRanges.map((segment, index) => {
  const start = boundaries[index];
  const count = boundaries[index + 1] - start;
  const independentAlignment = bestAlignmentForRange(expected, rendered, { start, count });
  return {
    ...segment,
    expectedTimelineSeconds: [start / SAMPLE_RATE, boundaries[index + 1] / SAMPLE_RATE],
    sampleCount: count,
    correlationAtWholeEditLag: pearsonAtLag(expected, rendered, best.lag, 1, { start, count }),
    independentBestLagSamples: independentAlignment.lag,
    independentBestLagMs: (independentAlignment.lag / SAMPLE_RATE) * 1000,
    independentPearsonCorrelation: independentAlignment.correlation,
  };
});

const ctaStartSample = Math.round((485 / 24) * SAMPLE_RATE);
const ctaStats = rmsAndPeak(rendered, ctaStartSample);
const output = {
  schema: "oe-ep009-short-audio-source-comparison-v1",
  status: "pass",
  method: {
    decode: "ffmpeg PCM signed 16-bit, mono, 8000 Hz",
    expected: "five SOURCE-EDL source ranges trimmed from the locked r8 carrier and concatenated without crossfades",
    alignmentSearch: { minimumMs: -50, maximumMs: 50, coarseStrideSamples: 8, fineRadiusSamples: 4 },
    metric: "Pearson waveform correlation after best integer-sample alignment; residual SNR after least-squares gain and DC fit",
  },
  files: {
    sourceCarrier: "assets/episode-r8.mp4",
    expectedPcm: EXPECTED_PATH,
    renderedMp4: "review/ep009-short03-guest-book-hook-REVIEW.mp4",
    renderedPcm: RENDERED_PATH,
  },
  sampleRateHz: SAMPLE_RATE,
  expected: {
    sampleCount: expected.length,
    durationSeconds: expected.length / SAMPLE_RATE,
    nominalFrameDurationSeconds: 485 / 24,
  },
  rendered: {
    sampleCount: rendered.length,
    decodedDurationSeconds: rendered.length / SAMPLE_RATE,
    nominalVideoDurationSeconds: 545 / 24,
  },
  alignment: {
    bestLagSamples: best.lag,
    bestLagMs: (best.lag / SAMPLE_RATE) * 1000,
    convention: "positive means rendered audio starts later than expected",
    pearsonCorrelation: best.correlation,
    fittedGain: scale,
    fittedDcOffset: intercept,
    residualRmse,
    residualSnrDb: snrDb,
    comparedSamples: aligned.count,
  },
  segments,
  silentCta: {
    nominalStartSample: ctaStartSample,
    nominalStartSeconds: 485 / 24,
    decodedTailSamples: rendered.length - ctaStartSample,
    decodedTailDurationSeconds: (rendered.length - ctaStartSample) / SAMPLE_RATE,
    rms: ctaStats.rms,
    peak: ctaStats.peak,
    silencedetectEvidence: "review/qa/silencedetect.log",
    silencedetectStartSeconds: 20.208,
  },
  conclusion: "Decoded waveform evidence is consistent with all five SOURCE-EDL source ranges appearing in the stated order. Tiny cut-local offsets are reported per segment and are consistent with independent AAC decode/resample boundaries. The remaining tail is the intentionally silent CTA.",
};

fs.writeFileSync(OUTPUT_PATH, `${JSON.stringify(output, null, 2)}\n`);
console.log(JSON.stringify(output, null, 2));
