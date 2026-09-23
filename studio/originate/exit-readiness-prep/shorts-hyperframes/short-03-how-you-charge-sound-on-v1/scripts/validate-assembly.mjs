#!/usr/bin/env node

import { execFileSync } from "node:child_process";
import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const project = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const expected = {
  locked: "6be1ee7c13ba6fc607d215e9a61c74fda31cc3f60026632eff6fc029f903cf6c",
  transcript: "b09eed699592ff5bfae8bb371abb1c4f951c919bddd63214a2ba849fc8e776cb",
  audio: "c62c09057d6cf1e91b895b485b0cc0114d52707e337b1970112811e9d48ccd83",
  opening: "b0e40fb4532a4de5ac69430a4bbda6a2f21c10cf928ab8a211e4a2a7a4b58718",
  returning: "e450010081c09ce5369c45790c8c0a024ef32622bfd5a00b6dcf871ec61963d8",
  captionManifest: "b5da0423f5c6500d0f956dd45820a51e860ce999ca0dcb65fa5a4e35e29c9872",
  captions: "761567e8487a96c1f919007002bf92347f421d2a79c27cb33f67770204d03476"
};

function fail(message) {
  throw new Error(message);
}

function check(condition, message) {
  if (!condition) fail(message);
}

function bytes(path) {
  return readFileSync(resolve(project, path));
}

function text(path) {
  return bytes(path).toString("utf8");
}

function hash(path) {
  return createHash("sha256").update(bytes(path)).digest("hex");
}

function normalize(value) {
  return String(value)
    .normalize("NFKC")
    .replace(/[\u2018\u2019]/g, "'")
    .replace(/[\u2010\u2011\u2012\u2013\u2014-]/g, " ")
    .toLowerCase()
    .match(/[a-z0-9]+(?:'[a-z0-9]+)?/g) || [];
}

function probe(path) {
  return JSON.parse(execFileSync("ffprobe", [
    "-v", "error",
    "-show_entries", "format=duration:stream=codec_type,codec_name,width,height,pix_fmt,r_frame_rate,nb_frames,sample_rate,channels",
    "-of", "json",
    resolve(project, path)
  ], { encoding: "utf8" }));
}

const paths = {
  locked: "../../shorts-net-new/STANDALONE-SCRIPTS-V3.json",
  transcript: "../../shorts-net-new/narration-v5/short-03-how-you-charge/diagnostic-forced-final/transcript.json",
  audio: "assets/audio/original-c.wav",
  opening: "assets/media/presenter-opening.mp4",
  returning: "assets/media/presenter-return.mp4",
  captionManifest: "CAPTION-MANIFEST.json",
  captions: "compositions/captions.html"
};

for (const [key, path] of Object.entries(paths)) {
  check(hash(path) === expected[key], key + " hash drift");
}

const authority = JSON.parse(text(paths.locked));
const locked = authority.scripts.find((entry) => entry.id === "short-03-how-you-charge");
check(locked && locked.status === "owner_locked_exact_spoken_copy", "locked script unavailable");

const words = JSON.parse(text(paths.transcript));
check(words.length === 98, "transcript must contain 98 words");
const lockedWords = normalize(locked.spoken_copy);
const transcriptWords = words.flatMap((word) => normalize(word.text));
check(lockedWords.length === 98, "locked copy must normalize to 98 words");
check(lockedWords.every((word, index) => word === transcriptWords[index]), "transcript differs from locked copy");

const captions = JSON.parse(text(paths.captionManifest));
const covered = captions.cues.flatMap((cue) => cue.word_ids);
check(captions.cues.length === 20, "caption cue count drift");
check(new Set(covered).size === 98 && covered.length === 98, "caption coverage must be exactly once");
check(captions.render_policy.rail_word_coverage === 80, "rail coverage drift");
check(captions.render_policy.embedded_scene_word_coverage === 18, "embedded coverage drift");

const index = text("index.html");
check(index.includes('data-duration="39.625"'), "root duration drift");
check(index.includes('src="assets/audio/original-c.wav"'), "Original C is not mounted");
check(index.includes('src="assets/media/presenter-opening.mp4"'), "opening presenter is not mounted");
check(index.includes('src="assets/media/presenter-return.mp4"'), "return presenter is not mounted");
check(!/https?:\/\//i.test(index), "render-time URL found in index");

const projectHtml = [
  index,
  text("compositions/01-host-opening-overlay.html"),
  text("compositions/02-conditional-perimeter.html"),
  text("compositions/03-defined-preparation-scope.html"),
  text("compositions/04-fixed-fee-model.html"),
  text("compositions/05-host-return-overlay.html"),
  text("compositions/06-counsel-handoff.html"),
  text("compositions/captions.html")
].join("\n");
check(!/STATIC IDENTITY|matching performance pending|ep007-avatar-v5/i.test(projectHtml), "static identity plate survived");
check(!/https?:\/\//i.test(projectHtml), "render-time URL found in composition");
check(!/<br\s*\/?>/i.test(projectHtml), "forced body-text break found");

for (const cue of captions.cues.filter((entry) => entry.role === "embedded_scene_text")) {
  const scene = cue.id === "g16"
    ? text("compositions/04-fixed-fee-model.html")
    : text("compositions/02-conditional-perimeter.html");
  const sceneWords = normalize(scene).join(" ");
  check(sceneWords.includes(normalize(cue.text).join(" ")), "missing embedded exact copy for " + cue.id);
}

const audioProbe = probe(paths.audio);
check(Math.abs(Number(audioProbe.format.duration) - 37.616333) < 0.0001, "Original C duration drift");
check(audioProbe.streams.filter((stream) => stream.codec_type === "audio").length === 1, "Original C audio stream drift");

const mediaChecks = [
  ["opening", probe(paths.opening), 8.56],
  ["return", probe(paths.returning), 6.575]
];
for (const [label, result, required] of mediaChecks) {
  const video = result.streams.find((stream) => stream.codec_type === "video");
  check(video && video.codec_name === "h264", label + " codec drift");
  check(video.width === 1080 && video.height === 1920, label + " dimensions drift");
  check(video.pix_fmt === "yuv420p" && video.r_frame_rate === "24/1", label + " browser-safe profile drift");
  check(result.streams.filter((stream) => stream.codec_type === "audio").length === 0, label + " must stay muted");
  check(Number(result.format.duration) >= required, label + " is shorter than its mounted window");
}

const report = {
  ok: true,
  exact_copy: {
    locked_words: 98,
    transcript_words: 98,
    caption_words_once: 98,
    rail_words: 80,
    embedded_words: 18
  },
  timeline: {
    audio_seconds: 37.616333,
    program_frame_end_seconds: 37.625,
    route_seconds: 2,
    total_seconds: 39.625,
    total_frames_at_24fps: 951
  },
  sources: Object.fromEntries(Object.entries(paths).map(([key, path]) => [key, { path, sha256: hash(path) }])),
  acceptance: {
    technical_source_ready: true,
    owner_listening: "pending",
    creative_acceptance: "pending",
    publication: "not_authorized"
  }
};

process.stdout.write(JSON.stringify(report, null, 2) + "\n");
