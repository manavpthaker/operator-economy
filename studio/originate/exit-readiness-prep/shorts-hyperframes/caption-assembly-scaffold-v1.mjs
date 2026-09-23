#!/usr/bin/env node

import { createHash } from "node:crypto";
import { execFileSync } from "node:child_process";
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import process from "node:process";

const args = process.argv.slice(2);
const checkOnly = args.includes("--check");
const planArg = args.find((arg) => arg !== "--check");

if (!planArg) {
  throw new Error("Usage: node caption-assembly-scaffold-v1.mjs <plan.json> [--check]");
}

const planPath = resolve(planArg);
const scaffoldDir = dirname(planPath);
const projectDir = dirname(scaffoldDir);
const plan = JSON.parse(readFileSync(planPath, "utf8"));

const readProject = (path) => readFileSync(resolve(projectDir, path));
const sha256 = (value) => createHash("sha256").update(value).digest("hex");
const round6 = (value) => Number(value.toFixed(6));
const escapeHtml = (value) => String(value)
  .replaceAll("&", "&amp;")
  .replaceAll("<", "&lt;")
  .replaceAll(">", "&gt;")
  .replaceAll('"', "&quot;");

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

function normalizeWords(text) {
  return String(text)
    .normalize("NFKC")
    .replace(/[\u2018\u2019]/g, "'")
    .replace(/[\u2010\u2011\u2012\u2013\u2014-]/g, " ")
    .toLowerCase()
    .match(/[a-z0-9]+(?:'[a-z0-9]+)?/g) || [];
}

function decodeBasicHtml(text) {
  return String(text)
    .replace(/<br\s*\/?\s*>/gi, " ")
    .replace(/<[^>]+>/g, " ")
    .replaceAll("&nbsp;", " ")
    .replaceAll("&amp;", "&")
    .replaceAll("&lt;", "<")
    .replaceAll("&gt;", ">")
    .replaceAll("&quot;", '"')
    .replaceAll("&#39;", "'")
    .replaceAll("&rsquo;", "’");
}

function targetTexts(html, selector) {
  const match = /^([#.])([A-Za-z0-9_-]+)$/.exec(selector);
  assert(match, `Only simple #id or .class render targets are supported: ${selector}`);
  const [, kind, name] = match;
  const texts = [];
  const openings = html.matchAll(/<([a-z][a-z0-9-]*)\b([^>]*)>/gi);
  for (const opening of openings) {
    const tag = opening[1];
    const attrs = opening[2];
    const id = /(?:^|\s)id=["']([^"']+)["']/i.exec(attrs)?.[1];
    const classes = /(?:^|\s)class=["']([^"']+)["']/i.exec(attrs)?.[1]?.split(/\s+/) || [];
    if ((kind === "#" && id === name) || (kind === "." && classes.includes(name))) {
      const contentStart = opening.index + opening[0].length;
      const closeIndex = html.indexOf(`</${tag}>`, contentStart);
      assert(closeIndex >= 0, `Target has no closing tag: ${selector}`);
      texts.push(decodeBasicHtml(html.slice(contentStart, closeIndex)));
    }
  }
  return texts;
}

function verifyBoundFile(binding, label) {
  const bytes = readProject(binding.path);
  const actual = sha256(bytes);
  assert(actual === binding.sha256, `${label} hash drift: ${binding.path}; expected ${binding.sha256}; got ${actual}`);
  return bytes;
}

function cueFromRange(group, words) {
  const from = Number(String(group.from).replace(/^w/, ""));
  const to = Number(String(group.to).replace(/^w/, ""));
  assert(Number.isInteger(from) && Number.isInteger(to) && from >= 0 && to >= from, `Invalid cue range ${group.id}`);
  const selected = words.slice(from, to + 1);
  assert(selected.length === to - from + 1, `Cue range outside transcript: ${group.id}`);
  selected.forEach((word, offset) => {
    assert(word.id === `w${from + offset}`, `Non-sequential word id in ${group.id}: ${word.id}`);
  });
  const start = round6(selected[0].start);
  const end = round6(selected.at(-1).end);
  assert(end > start, `Non-positive cue duration: ${group.id}`);
  assert(end - start >= 0.5, `Cue shorter than 0.5 seconds: ${group.id} (${end - start})`);
  return {
    id: group.id,
    role: group.role,
    ...(group.render_target ? { render_target: group.render_target } : {}),
    word_ids: selected.map((word) => word.id),
    start,
    end,
    text: selected.map((word) => word.text).join(" "),
  };
}

function verifyTimeline() {
  const clips = plan.assembly.timeline;
  assert(clips.length > 0, "Assembly timeline is empty");
  assert(Math.abs(clips[0].start) < 1e-6, "Assembly must begin at 0");
  for (let index = 0; index < clips.length; index += 1) {
    const clip = clips[index];
    assert(clip.duration > 0, `Non-positive clip duration: ${clip.id}`);
    assert(Math.abs((clip.end - clip.start) - clip.duration) < 2e-6, `Bad duration arithmetic: ${clip.id}`);
    if (index > 0) {
      const previous = clips[index - 1];
      assert(Math.abs(previous.end - clip.start) < 2e-6, `Timeline gap/overlap: ${previous.id} -> ${clip.id}`);
    }
  }
  assert(Math.abs(clips.at(-1).end - plan.assembly.total_duration_seconds) < 2e-6, "Timeline does not reach total duration");
  assert(Math.abs(plan.assembly.program_frame_end_seconds * plan.fps - Math.round(plan.assembly.program_frame_end_seconds * plan.fps)) < 2e-5, "Program end is not frame-aligned");
  assert(Math.abs(plan.assembly.total_duration_seconds * plan.fps - Math.round(plan.assembly.total_duration_seconds * plan.fps)) < 2e-5, "Total duration is not frame-aligned");
}

verifyBoundFile(plan.authority.locked_scripts, "Locked script authority");
verifyBoundFile(plan.source.active_index, "Active index");
verifyBoundFile(plan.source.transcript, "Canonical transcript");
verifyBoundFile(plan.source.audio, "Original C master");
for (const scene of plan.source.scenes) verifyBoundFile(scene, `Scene ${scene.path}`);
for (const presenter of plan.source.presenter_assets || []) verifyBoundFile(presenter, `Presenter ${presenter.path}`);
for (const overlay of plan.source.host_overlay_variants || []) {
  verifyBoundFile({ path: overlay.path, sha256: overlay.sha256 }, `Host overlay ${overlay.path}`);
  verifyBoundFile({ path: overlay.motion_path, sha256: overlay.motion_sha256 }, `Host overlay motion ${overlay.motion_path}`);
}

const authority = JSON.parse(readProject(plan.authority.locked_scripts.path));
const locked = authority.scripts.find((entry) => entry.id === plan.short_id);
assert(locked, `Short not found in locked authority: ${plan.short_id}`);
assert(locked.status === "owner_locked_exact_spoken_copy", `Script is not owner locked: ${plan.short_id}`);

const words = JSON.parse(readProject(plan.source.transcript.path));
assert(Array.isArray(words), "Transcript must be a flat word array");
assert(words.length === plan.source.transcript.word_count, `Transcript word count drift: ${words.length}`);
words.forEach((word, index) => {
  assert(word.id === `w${index}`, `Transcript word ids must be sequential; got ${word.id} at ${index}`);
  assert(Number.isFinite(word.start) && Number.isFinite(word.end) && word.start >= 0 && word.end > word.start, `Invalid word timing: ${word.id}`);
  if (index > 0) assert(word.start >= words[index - 1].start, `Non-monotonic transcript start at ${word.id}`);
  assert(word.end <= plan.source.audio.duration_seconds + 1e-6, `Word beyond audio duration: ${word.id}`);
});

const lockedNormalized = normalizeWords(locked.spoken_copy);
const transcriptNormalized = words.flatMap((word) => normalizeWords(word.text));
assert(lockedNormalized.length === transcriptNormalized.length, `Normalized word count mismatch: locked=${lockedNormalized.length}, transcript=${transcriptNormalized.length}`);
assert(lockedNormalized.every((word, index) => word === transcriptNormalized[index]), "Canonical transcript does not match locked spoken_copy");

const probedDuration = Number(execFileSync("ffprobe", [
  "-v", "error",
  "-show_entries", "format=duration",
  "-of", "default=noprint_wrappers=1:nokey=1",
  resolve(projectDir, plan.source.audio.path),
], { encoding: "utf8" }).trim());
assert(Math.abs(probedDuration - plan.source.audio.duration_seconds) < 0.0001, `Audio duration drift: expected ${plan.source.audio.duration_seconds}; got ${probedDuration}`);

for (const presenter of plan.source.presenter_assets || []) {
  const probe = JSON.parse(execFileSync("ffprobe", [
    "-v", "error",
    "-show_entries", "format=duration:stream=codec_type,codec_name,width,height,pix_fmt,avg_frame_rate",
    "-of", "json",
    resolve(projectDir, presenter.path),
  ], { encoding: "utf8" }));
  const video = probe.streams.find((stream) => stream.codec_type === "video");
  const audioStreams = probe.streams.filter((stream) => stream.codec_type === "audio");
  assert(video, `Presenter has no video stream: ${presenter.path}`);
  assert(video.codec_name === presenter.video_codec, `Presenter codec drift: ${presenter.path}`);
  assert(video.width === plan.canvas.width && video.height === plan.canvas.height, `Presenter dimensions drift: ${presenter.path}`);
  assert(video.pix_fmt === presenter.pixel_format, `Presenter pixel format drift: ${presenter.path}`);
  assert(video.avg_frame_rate === `${plan.fps}/1`, `Presenter frame-rate drift: ${presenter.path}`);
  assert(audioStreams.length === presenter.audio_stream_count, `Presenter audio-stream drift: ${presenter.path}`);
  assert(Math.abs(Number(probe.format.duration) - presenter.container_duration_seconds) < 0.0001, `Presenter duration drift: ${presenter.path}`);
}

const cues = plan.caption_groups.map((group) => cueFromRange(group, words));
const claimed = new Map();
for (const cue of cues) {
  for (const wordId of cue.word_ids) {
    assert(!claimed.has(wordId), `Duplicate caption word ${wordId}: ${claimed.get(wordId)} and ${cue.id}`);
    claimed.set(wordId, cue.id);
  }
}
for (const word of words) assert(claimed.has(word.id), `Dropped caption word: ${word.id} (${word.text})`);
assert(claimed.size === words.length, `Caption coverage mismatch: ${claimed.size}/${words.length}`);

const sceneHtml = plan.source.scenes.map((scene) => readProject(scene.path).toString("utf8"));
for (const cue of cues.filter((entry) => entry.role === "embedded_scene_text")) {
  const cueWords = normalizeWords(cue.text).join(" ");
  const candidates = sceneHtml.flatMap((html) => targetTexts(html, cue.render_target));
  assert(candidates.length > 0, `Embedded scene target not found: ${cue.id} -> ${cue.render_target}`);
  assert(candidates.some((text) => normalizeWords(text).join(" ").includes(cueWords)), `Embedded scene target is not exact locked copy: ${cue.id} -> ${cue.render_target}`);
  cue.target_exact_copy_verified = true;
}

verifyTimeline();

const railCues = cues.filter((cue) => cue.role === "rail");
const embeddedCues = cues.filter((cue) => cue.role === "embedded_scene_text");
assert(cues.length === railCues.length + embeddedCues.length, "Unknown caption role in plan");

const captionManifest = {
  schema_version: "1.0",
  short_id: plan.short_id,
  status: "generated_unmounted_sound_on_scaffold",
  authority: {
    path: plan.authority.locked_scripts.path,
    sha256: plan.authority.locked_scripts.sha256,
    script_status: locked.status,
  },
  source: {
    path: plan.source.transcript.path,
    sha256: plan.source.transcript.sha256,
    word_count: words.length,
    audio_path: plan.source.audio.path,
    audio_sha256: plan.source.audio.sha256,
    audio_duration_seconds: plan.source.audio.duration_seconds,
  },
  render_policy: {
    mode: "rail_first_with_exact_scene_text_suppression",
    rail_word_coverage: railCues.reduce((sum, cue) => sum + cue.word_ids.length, 0),
    embedded_scene_word_coverage: embeddedCues.reduce((sum, cue) => sum + cue.word_ids.length, 0),
    dropped_word_count: 0,
    duplicated_word_count: 0,
    rail_position: "overlay; left 72px; right edge 928px; bottom 326px",
    duplicate_suppression: true,
    note: "embedded_scene_text means the exact locked words already exist in the bound scene; those words are omitted from the foreground rail, not rewritten",
  },
  cues,
};

const captionManifestText = `${JSON.stringify(captionManifest, null, 2)}\n`;
const captionId = plan.caption_composition_id;
const captionHtml = `<!DOCTYPE html>
<html lang="en"><head></head>
  <body>
    <template>
      <style>
        @font-face { font-family: "BL Supreme"; src: url("assets/fonts/supreme-500.woff2") format("woff2"); font-weight: 500; }
        * { box-sizing: border-box; }
        #${captionId} { position: absolute; inset: 0; width: 1080px; height: 1920px; overflow: hidden; pointer-events: none; font-family: "BL Supreme", system-ui, sans-serif; }
        .caption { position: absolute; left: 72px; bottom: 326px; width: 856px; color: #f5f0e6; font-size: 48px; font-weight: 500; line-height: 1.09; letter-spacing: -0.018em; text-align: left; text-wrap: balance; }
        .caption span { display: inline-block; max-width: 856px; padding: 17px 23px 19px; border-left: 6px solid #fb8b69; border-radius: 3px; background: rgba(23,53,48,0.95); box-shadow: 0 12px 34px rgba(7,26,23,0.28); }
      </style>
      <section data-hf-id="hf-${captionId}-root" id="${captionId}" data-composition-id="${captionId}" data-start="0" data-duration="${plan.assembly.program_frame_end_seconds}" data-width="1080" data-height="1920">
${railCues.map((cue, index) => `        <div data-hf-id="hf-${captionId}-${String(index + 1).padStart(2, "0")}" id="${captionId}-cue-${String(index + 1).padStart(2, "0")}" class="clip caption" data-caption-layer="fg" data-start="${cue.start}" data-duration="${round6(cue.end - cue.start)}" data-track-index="20"><span>${escapeHtml(cue.text)}</span></div>`).join("\n")}
      </section>
      <script>
        window.__timelines = window.__timelines || {};
        window.__timelines["${captionId}"] = gsap.timeline({ paused: true });
      </script>
    </template>
  </body>
</html>
`;

const captionMotion = {
  duration: plan.assembly.program_frame_end_seconds,
  assertions: [
    { kind: "appearsBy", selector: `#${captionId}-cue-01`, bySec: round6(railCues[0].start + 0.25) },
    { kind: "staysInFrame", selector: ".caption" },
  ],
};
const captionMotionText = `${JSON.stringify(captionMotion, null, 2)}\n`;

const assemblyManifest = {
  schema_version: "1.0",
  short_id: plan.short_id,
  status: "unmounted_scaffold_not_a_review_cut",
  active_project_unchanged: true,
  fps: plan.fps,
  canvas: plan.canvas,
  source_bindings: {
    active_index: plan.source.active_index,
    scenes: plan.source.scenes,
    presenter_assets: plan.source.presenter_assets || [],
    host_overlay_variants: plan.source.host_overlay_variants || [],
    audio: plan.source.audio,
    transcript: plan.source.transcript,
  },
  exact_copy_check: {
    locked_normalized_words: lockedNormalized.length,
    transcript_normalized_words: transcriptNormalized.length,
    exact_order_match: true,
    caption_words_covered_once: words.length,
    dropped_words: 0,
    duplicated_words: 0,
  },
  caption_mount: {
    composition_id: captionId,
    source: "sound-on-scaffold-v1/compositions/captions.html",
    start: 0,
    duration: plan.assembly.program_frame_end_seconds,
    track_index: 60,
    manifest_sha256: sha256(captionManifestText),
    composition_sha256: sha256(captionHtml),
    motion_sha256: sha256(captionMotionText),
  },
  assembly: plan.assembly,
  integration_blockers: plan.integration_blockers,
  integration_rules: plan.integration_rules,
  authorization: {
    provider_calls: false,
    render: false,
    preview_server: false,
    upload: false,
    publication: false,
  },
};
const assemblyManifestText = `${JSON.stringify(assemblyManifest, null, 2)}\n`;

const outputs = [
  [resolve(scaffoldDir, "CAPTION-MANIFEST.json"), captionManifestText],
  [resolve(scaffoldDir, "compositions/captions.html"), captionHtml],
  [resolve(scaffoldDir, "compositions/captions.motion.json"), captionMotionText],
  [resolve(scaffoldDir, "ASSEMBLY-MANIFEST.json"), assemblyManifestText],
];

for (const [path, content] of outputs) {
  if (checkOnly) {
    const actual = readFileSync(path, "utf8");
    assert(actual === content, `Generated scaffold is stale: ${path}`);
  } else {
    mkdirSync(dirname(path), { recursive: true });
    writeFileSync(path, content);
  }
}

console.log(JSON.stringify({
  ok: true,
  mode: checkOnly ? "check" : "write",
  short_id: plan.short_id,
  source_words: words.length,
  rail_words: captionManifest.render_policy.rail_word_coverage,
  embedded_scene_words: captionManifest.render_policy.embedded_scene_word_coverage,
  cues: cues.length,
  audio_duration_seconds: plan.source.audio.duration_seconds,
  program_frame_end_seconds: plan.assembly.program_frame_end_seconds,
  total_duration_seconds: plan.assembly.total_duration_seconds,
}, null, 2));
