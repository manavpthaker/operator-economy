import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const project = path.resolve(here, "..");
const composition = process.argv[2] || "model";
if (!/^[a-z0-9-]+$/.test(composition)) throw new Error(`Invalid composition name: ${composition}`);
const sourcePath = path.join(project, "sources", `${composition}.base.html`);
const outputPath = path.join(project, "compositions", `${composition}.html`);
const buildRecordPath = path.join(
  project,
  "qa",
  composition === "model" ? "rough-build.json" : `rough-build-${composition}.json`,
);
const source = fs.readFileSync(sourcePath, "utf8");

const sha = (value) => crypto.createHash("sha256").update(value).digest("hex");
const fixedRandom = (seed) => {
  let state = parseInt(sha(seed).slice(0, 8), 16) || 1;
  return () => {
    state ^= state << 13;
    state ^= state >>> 17;
    state ^= state << 5;
    return (state >>> 0) / 4294967296;
  };
};
const n = (value) => Number(value.toFixed(2)).toString();
const dist = (a, b) => Math.hypot(b[0] - a[0], b[1] - a[1]);

function flatten(d) {
  const tokens = d.match(/[a-zA-Z]|[-+]?(?:\d*\.)?\d+(?:e[-+]?\d+)?/g) || [];
  let i = 0;
  let command = null;
  let point = [0, 0];
  let start = [0, 0];
  const paths = [];
  let current = null;
  const take = () => [Number(tokens[i++]), Number(tokens[i++])];
  const add = (p) => { current.push(p); point = p; };

  while (i < tokens.length) {
    if (/[a-zA-Z]/.test(tokens[i])) command = tokens[i++];
    if (command === "M") {
      point = take();
      start = point;
      current = [point];
      paths.push(current);
      command = "L";
    } else if (command === "L") {
      add(take());
    } else if (command === "H") {
      add([Number(tokens[i++]), point[1]]);
    } else if (command === "V") {
      add([point[0], Number(tokens[i++])]);
    } else if (command === "Z" || command === "z") {
      add(start);
      command = null;
    } else {
      throw new Error(`Unsupported SVG command ${command} in ${d}`);
    }
  }
  return paths;
}

function pointAt(points, lengths, position) {
  const total = lengths[lengths.length - 1];
  const s = Math.max(0, Math.min(total, position));
  let i = 1;
  while (i < lengths.length - 1 && lengths[i] < s) i += 1;
  const fraction = (s - lengths[i - 1]) / (lengths[i] - lengths[i - 1] || 1);
  const a = points[i - 1];
  const b = points[i];
  return [a[0] + (b[0] - a[0]) * fraction, a[1] + (b[1] - a[1]) * fraction];
}

let sourcePaths = 0;
let visibleStrokes = 0;
let revealMasks = 0;

const compiled = source.replace(/<path\b[^>]*class="[^"]*rough-source[^"]*"[^>]*\/>/g, (tag) => {
  const attr = (name) => tag.match(new RegExp(`(?:^|\\s)${name}="([^"]*)"`))?.[1];
  const d = attr("d");
  const id = attr("id");
  const classes = (attr("class") || "").split(/\s+/);
  const tone = classes.find((name) => ["mineral", "steel", "steel-dark", "oxide", "rule", "hatch"].includes(name)) || "mineral";
  const isHatch = tone === "hatch";
  const color = {
    mineral: "#204440",
    steel: "#586d74",
    "steel-dark": "#33464c",
    oxide: "#b5482f",
    rule: "#c4b99e",
    hatch: "#204440"
  }[tone];
  const random = fixedRandom(`${id || "path"}:${d}:${sourcePaths}`);
  const fragments = [];
  sourcePaths += 1;

  for (const points of flatten(d)) {
    if (points.length < 2) continue;
    const lengths = [0];
    for (let i = 1; i < points.length; i += 1) lengths.push(lengths[lengths.length - 1] + dist(points[i - 1], points[i]));
    const total = lengths[lengths.length - 1];
    let position = random() * 2.8;
    while (position < total - 0.5) {
      const fragmentLength = isHatch ? total : 13 + random() * 31;
      const end = Math.min(total, position + fragmentLength);
      const passes = isHatch ? 1 : (random() < 0.44 ? 3 : 2);
      for (let pass = 0; pass < passes; pass += 1) {
        if (pass === 2 && random() < 0.24) continue;
        const begin = Math.max(0, position + (pass ? random() * 7 - 3.5 : 0));
        const finish = Math.min(total, end + (pass ? random() * 9 - 4.5 : 0));
        if (finish - begin < 0.7) continue;
        const jitter = isHatch ? 0.7 : (pass ? 3.2 : 1.6);
        const samples = Math.max(1, Math.ceil((finish - begin) / 9));
        const offsetX = (random() - 0.5) * jitter * 2;
        const offsetY = (random() - 0.5) * jitter * 2;
        const segment = [];
        for (let j = 0; j <= samples; j += 1) {
          const p = pointAt(points, lengths, begin + ((finish - begin) * j) / samples);
          segment.push([p[0] + offsetX + (random() - 0.5) * jitter, p[1] + offsetY + (random() - 0.5) * jitter]);
        }
        const strokePath = segment.map((p, index) => `${index ? "L" : "M"} ${n(p[0])} ${n(p[1])}`).join(" ");
        const baseWeight = tone === "oxide" ? 3.0 : isHatch ? 1.25 : tone === "rule" ? 1.25 : 2.15;
        const width = baseWeight * (pass ? 0.40 + random() * 0.44 : 0.68 + random() * 0.60);
        const opacity = isHatch ? 0.52 + random() * 0.18 : (pass ? 0.34 + random() * 0.32 : 0.74 + random() * 0.24);
        fragments.push(`<path d="${strokePath}" fill="none" stroke="${color}" stroke-width="${n(width)}" opacity="${n(opacity)}" stroke-linecap="round" stroke-linejoin="miter"/>`);
        visibleStrokes += 1;
      }
      position = end + (random() < 0.34 ? 2.2 + random() * 6.5 : -1.8 + random() * 2.4);
    }
  }

  const draw = tag.includes("data-draw=");
  if (!draw) return `<g${id ? ` id="${id}-unit"` : ""} data-pencil-unit="${id || sourcePaths}">${fragments.join("")}</g>`;

  revealMasks += 1;
  const maskId = `${composition}-mask-${sourcePaths}`;
  const maskPath = `<path id="${id}" data-draw="true" d="${d}" fill="none" stroke="white" stroke-width="30" stroke-linecap="butt" stroke-linejoin="miter"/>`;
  return `<g id="${id}-unit" data-pencil-unit="${id}"><defs><mask id="${maskId}" maskUnits="userSpaceOnUse" x="-40" y="-40" width="2000" height="1160" style="mask-type:alpha">${maskPath}</mask></defs><g mask="url(#${maskId})">${fragments.join("")}</g></g>`;
});

fs.mkdirSync(path.dirname(outputPath), { recursive: true });
fs.writeFileSync(outputPath, compiled);
fs.writeFileSync(buildRecordPath, JSON.stringify({
  composition,
  source: path.relative(project, sourcePath),
  sourceSha256: sha(source),
  output: path.relative(project, outputPath),
  outputSha256: sha(compiled),
  sourcePaths,
  visibleStrokes,
  revealMasks,
  runtimeFilter: false,
  runtimeJitter: false,
  method: "fixed build-time short overlapping stroke fragments with real gaps and uneven pressure"
}, null, 2) + "\n");

console.log(JSON.stringify({ composition, outputPath, buildRecordPath, sourcePaths, visibleStrokes, revealMasks, outputSha256: sha(compiled) }, null, 2));
