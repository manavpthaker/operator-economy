import { readFileSync, writeFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, resolve } from "node:path";

const here = dirname(fileURLToPath(import.meta.url));
const repoRoot = resolve(here, "../../../..");
const experimentRoot = resolve(here, "..");
const wordsPath = resolve(
  repoRoot,
  "studio/originate/direct-booking-recovery/vo/words.json",
);

const sourceIn = 849.517;
const sourceOut = 879.922;
const words = JSON.parse(readFileSync(wordsPath, "utf8"));
const selected = words
  .map((entry, index) => ({ index, ...entry }))
  .filter((entry) => entry.index >= 1775 && entry.index <= 1847)
  .map((entry) => ({
    index: entry.index,
    word: entry.word,
    source_start: Number(entry.start.toFixed(3)),
    source_end: Number(entry.end.toFixed(3)),
    relative_start: Number((entry.start - sourceIn).toFixed(3)),
    relative_end: Number((entry.end - sourceIn).toFixed(3)),
  }));

const scenes = [
  { id: "scene-01-return", in: 0.0, out: 4.375, word_start: 1775, word_end: 1787 },
  { id: "scene-02-permission", in: 4.375, out: 12.24, word_start: 1788, word_end: 1805 },
  { id: "scene-03-judgment", in: 12.24, out: 20.34, word_start: 1806, word_end: 1823 },
  { id: "scene-04-direct-return", in: 20.34, out: 25.103, word_start: 1824, word_end: 1835 },
  { id: "scene-05-outcome", in: 25.103, out: 30.405, word_start: 1836, word_end: 1847 },
].map((scene) => ({
  ...scene,
  absolute_in: Number((sourceIn + scene.in).toFixed(3)),
  absolute_out: Number((sourceIn + scene.out).toFixed(3)),
}));

const importantCues = [1775, 1786, 1788, 1790, 1791, 1796, 1800, 1801, 1806, 1812, 1815, 1816, 1818, 1819, 1821, 1824, 1825, 1830, 1834, 1836, 1839, 1843, 1846, 1847]
  .map((index) => selected.find((word) => word.index === index));

const payload = {
  source: "studio/originate/direct-booking-recovery/vo/words.json",
  source_in_seconds: sourceIn,
  source_out_seconds: sourceOut,
  duration_seconds: Number((sourceOut - sourceIn).toFixed(3)),
  intentional_handle: {
    duration_seconds: 0.146,
    word_index: 1775,
    word: "Now",
    canonical_sequence_unit_boundary: 849.663,
  },
  scenes,
  important_cues: importantCues,
  words: selected,
};

writeFileSync(resolve(here, "word-cues.json"), `${JSON.stringify(payload, null, 2)}\n`);

const subtitleSegments = [
  [1775, 1783],
  [1784, 1790],
  [1791, 1800],
  [1801, 1806],
  [1807, 1815],
  [1816, 1822],
  [1823, 1834],
  [1835, 1847],
];

function srtTime(seconds) {
  const millis = Math.round(seconds * 1000);
  const hours = Math.floor(millis / 3_600_000);
  const minutes = Math.floor((millis % 3_600_000) / 60_000);
  const secs = Math.floor((millis % 60_000) / 1000);
  const ms = millis % 1000;
  return `${String(hours).padStart(2, "0")}:${String(minutes).padStart(2, "0")}:${String(secs).padStart(2, "0")},${String(ms).padStart(3, "0")}`;
}

const srt = subtitleSegments
  .map(([startIndex, endIndex], position) => {
    const segment = selected.filter((entry) => entry.index >= startIndex && entry.index <= endIndex);
    const text = segment.map((entry) => entry.word).join(" ");
    const start = Math.max(0, segment[0].relative_start);
    const end = Math.min(sourceOut - sourceIn, segment.at(-1).relative_end);
    return `${position + 1}\n${srtTime(start)} --> ${srtTime(end)}\n${text}`;
  })
  .join("\n\n");

writeFileSync(resolve(experimentRoot, "resolve/handoff/return-loop.srt"), `${srt}\n`);
writeFileSync(
  resolve(here, "locked-narration.txt"),
  `${selected.map((entry) => entry.word).join(" ")}\n`,
);
