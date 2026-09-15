#!/usr/bin/env node

import { createHash } from "node:crypto";
import { mkdir, readFile, writeFile } from "node:fs/promises";
import { dirname, extname, resolve } from "node:path";

function argument(name, fallback = null) {
  const index = process.argv.indexOf(name);
  return index === -1 ? fallback : process.argv[index + 1];
}

function required(name) {
  const value = argument(name);
  if (!value) throw new Error(`Missing required argument: ${name}`);
  return value;
}

function valueFromEnvFile(text, key) {
  const prefix = `${key}=`;
  const line = text.split(/\r?\n/).find((entry) => entry.startsWith(prefix));
  return line ? line.slice(prefix.length).trim() : "";
}

function promptFromRecord(text) {
  const match = text.match(/## Prompt\s+([\s\S]*?)(?=\n## |$)/);
  if (!match) throw new Error("Prompt record has no `## Prompt` section");
  return match[1].trim();
}

function mimeFor(path) {
  const extension = extname(path).toLowerCase();
  if (extension === ".png") return "image/png";
  if (extension === ".webp") return "image/webp";
  return "image/jpeg";
}

const referenceArgument = argument("--reference");
const referencePath = referenceArgument ? resolve(referenceArgument) : null;
const endReferenceArgument = argument("--end-reference");
const endReferencePath = endReferenceArgument ? resolve(endReferenceArgument) : null;
const promptPath = resolve(required("--prompt-record"));
const outputPath = resolve(required("--output"));
const responsePath = resolve(argument("--response", `${outputPath}.response.json`));
const duration = argument("--duration", "8");
const resolution = argument("--resolution", "720p");
const model = argument("--model", "bytedance/seedance-2.5/image-to-video");
const seed = argument("--seed");
const negativeAppend = argument("--negative-append", "").trim();
const negativePrompt = [
  "news broadcast, stock footage, advertisement, 3d animation, computer graphics, cartoon, watermark, logo, text, on screen text, subtitles, titles, signature, slow motion, dramatic reaction, handshake, contract signing, celebration, distorted face, distorted hands, extra fingers",
  negativeAppend,
].filter(Boolean).join(", ");

const repositoryRoot = resolve(process.cwd(), "../../../..");
const envText = await readFile(resolve(repositoryRoot, ".env"), "utf8");
const key = process.env.FAL_KEY || valueFromEnvFile(envText, "FAL_KEY");
if (!key) throw new Error("FAL_KEY is unavailable");

const [reference, endReference, promptRecord] = await Promise.all([
  referencePath ? readFile(referencePath) : Promise.resolve(null),
  endReferencePath ? readFile(endReferencePath) : Promise.resolve(null),
  readFile(promptPath, "utf8"),
]);

let requestBody;
if (model.includes("veo3.1") && model.includes("first-last-frame-to-video")) {
  if (!reference || !referencePath || !endReference || !endReferencePath) {
    throw new Error("Veo 3.1 first-last-frame-to-video requires --reference and --end-reference");
  }
  requestBody = {
    prompt: promptFromRecord(promptRecord),
    first_frame_url: `data:${mimeFor(referencePath)};base64,${reference.toString("base64")}`,
    last_frame_url: `data:${mimeFor(endReferencePath)};base64,${endReference.toString("base64")}`,
    aspect_ratio: argument("--aspect-ratio", "16:9"),
    duration: duration.endsWith("s") ? duration : `${duration}s`,
    negative_prompt: negativePrompt,
    resolution,
    generate_audio: false,
    auto_fix: false,
    safety_tolerance: Number(argument("--safety-tolerance", "4")),
  };
  if (seed !== null) requestBody.seed = Number(seed);
} else if (model.includes("kling-video/v3")) {
  if (!reference || !referencePath) throw new Error("Kling v3 image-to-video requires --reference");
  requestBody = {
    prompt: promptFromRecord(promptRecord),
    start_image_url: `data:${mimeFor(referencePath)};base64,${reference.toString("base64")}`,
    duration,
    generate_audio: false,
    shot_type: "customize",
    negative_prompt: negativePrompt,
    cfg_scale: Number(argument("--cfg-scale", "0.7")),
  };
  if (endReference && endReferencePath) {
    requestBody.end_image_url = `data:${mimeFor(endReferencePath)};base64,${endReference.toString("base64")}`;
  }
} else if (model.includes("ltx-2.3-22b")) {
  requestBody = {
    prompt: promptFromRecord(promptRecord),
    num_frames: Number(argument("--num-frames", "193")),
    video_size: "landscape_16_9",
    generate_audio: false,
    use_multiscale: true,
    fps: Number(argument("--fps", "24")),
    num_inference_steps: 40,
    acceleration: "regular",
    camera_lora: argument("--camera", "none"),
    camera_lora_scale: Number(argument("--camera-scale", "0.7")),
    negative_prompt: negativePrompt,
    enable_prompt_expansion: false,
    enable_safety_checker: true,
    video_output_type: "X264 (.mp4)",
    video_quality: "high",
    video_write_mode: "balanced",
  };
  if (seed !== null) requestBody.seed = Number(seed);
  if (reference && referencePath) {
    requestBody.image_url = `data:${mimeFor(referencePath)};base64,${reference.toString("base64")}`;
    requestBody.image_strength = Number(argument("--image-strength", "0.95"));
  }
  if (endReference && endReferencePath) {
    requestBody.end_image_url = `data:${mimeFor(endReferencePath)};base64,${endReference.toString("base64")}`;
    requestBody.end_image_strength = Number(argument("--end-image-strength", "0.95"));
    requestBody.interpolation_direction = argument("--interpolation-direction", "forward");
  }
} else {
  requestBody = {
    prompt: promptFromRecord(promptRecord),
    resolution,
    duration,
    generate_audio: false,
    bitrate_mode: "high",
  };
  if (reference && referencePath) {
    requestBody.image_url = `data:${mimeFor(referencePath)};base64,${reference.toString("base64")}`;
  } else {
    requestBody.aspect_ratio = argument("--aspect-ratio", "16:9");
  }
  if (model.includes("seedance-2.5")) {
    requestBody.aspect_ratio = argument("--aspect-ratio", "16:9");
    if (endReference && endReferencePath) {
      requestBody.end_image_url = `data:${mimeFor(endReferencePath)};base64,${endReference.toString("base64")}`;
    }
    if (seed !== null) requestBody.seed = Number(seed);
  }
}

console.log(`Submitting ${duration}s ${resolution} proof to ${model}…`);
const response = await fetch(`https://queue.fal.run/${model}`, {
  method: "POST",
  headers: {
    Authorization: `Key ${key}`,
    "Content-Type": "application/json",
  },
  body: JSON.stringify(requestBody),
});

const submission = await response.json();
if (!response.ok) {
  throw new Error(`Fal ${response.status}: ${JSON.stringify(submission).slice(0, 1000)}`);
}

const requestId = submission?.request_id;
const statusUrl = submission?.status_url;
const resultUrl = submission?.response_url;
if (!requestId || !statusUrl || !resultUrl) {
  throw new Error(`Fal queue response is incomplete: ${JSON.stringify(submission).slice(0, 1000)}`);
}

await mkdir(dirname(responsePath), { recursive: true });
await writeFile(responsePath, `${JSON.stringify({
  schema: "oe-generated-film-queue-checkpoint-v1",
  generator: "fal.ai",
  model,
  submittedAt: new Date().toISOString(),
  requestId,
  statusUrl,
  resultUrl,
  outputPath,
}, null, 2)}\n`);
console.log(`Queued as ${requestId}`);
console.log(`Checkpoint ${responsePath}`);

let lastStatus = "";
const startedAt = Date.now();
while (true) {
  if (Date.now() - startedAt > 20 * 60 * 1000) {
    throw new Error(`Timed out waiting for ${requestId}; resume from ${responsePath}`);
  }
  const statusResponse = await fetch(statusUrl, {
    headers: { Authorization: `Key ${key}` },
  });
  const statusPayload = await statusResponse.json();
  if (!statusResponse.ok) {
    throw new Error(`Fal status ${statusResponse.status}: ${JSON.stringify(statusPayload).slice(0, 1000)}`);
  }
  const status = statusPayload?.status || "UNKNOWN";
  if (status !== lastStatus) {
    console.log(`Status ${status}`);
    lastStatus = status;
  }
  if (status === "COMPLETED") break;
  if (status === "FAILED") {
    throw new Error(`Fal request failed: ${JSON.stringify(statusPayload).slice(0, 1000)}`);
  }
  await new Promise((resolveDelay) => setTimeout(resolveDelay, 5000));
}

const resultResponse = await fetch(resultUrl, {
  headers: { Authorization: `Key ${key}` },
});
const payload = await resultResponse.json();
if (!resultResponse.ok) {
  throw new Error(`Fal result ${resultResponse.status}: ${JSON.stringify(payload).slice(0, 1000)}`);
}

const videoUrl = payload?.video?.url;
if (!videoUrl) throw new Error(`Fal response contains no video URL: ${JSON.stringify(payload).slice(0, 1000)}`);

const videoResponse = await fetch(videoUrl);
if (!videoResponse.ok) throw new Error(`Video download failed: ${videoResponse.status}`);
const video = Buffer.from(await videoResponse.arrayBuffer());

await mkdir(dirname(outputPath), { recursive: true });
await writeFile(outputPath, video);

const provenance = {
  schema: "oe-generated-film-proof-v1",
  generator: "fal.ai",
  model,
  generatedAt: new Date().toISOString(),
  requestId,
  request: {
    duration,
    resolution,
    generateAudio: false,
    parameters: Object.fromEntries(Object.entries(requestBody).filter(([key]) => key !== "prompt" && key !== "image_url" && key !== "start_image_url" && key !== "end_image_url" && key !== "first_frame_url" && key !== "last_frame_url")),
    promptRecord: promptPath,
    reference: referencePath,
    referenceSha256: reference ? createHash("sha256").update(reference).digest("hex") : null,
    endReference: endReferencePath,
    endReferenceSha256: endReference ? createHash("sha256").update(endReference).digest("hex") : null,
  },
  response: payload,
  output: {
    path: outputPath,
    sha256: createHash("sha256").update(video).digest("hex"),
    bytes: video.length,
  },
};

await writeFile(responsePath, `${JSON.stringify(provenance, null, 2)}\n`);
console.log(`Wrote ${outputPath}`);
console.log(`SHA-256 ${provenance.output.sha256}`);
console.log(`Provenance ${responsePath}`);
