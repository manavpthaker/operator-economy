#!/usr/bin/env node
/** Render one representative Blueprint frame for every authored storyboard screen. */
import {bundle} from '@remotion/bundler';
import {renderStill, selectComposition} from '@remotion/renderer';
import {readFileSync, mkdirSync} from 'fs';
import {resolve, dirname} from 'path';
import {fileURLToPath} from 'url';

const here = dirname(fileURLToPath(import.meta.url));
const [propsArg, outputArg] = process.argv.slice(2);
if (!propsArg) {
  console.error('Usage: node render-storyboard-stills.mjs <blueprint.json> [output-dir]');
  process.exit(1);
}

const propsPath = resolve(propsArg);
const renderData = JSON.parse(readFileSync(propsPath, 'utf8'));
const outputDir = resolve(outputArg || dirname(propsPath), 'storyboard_frames');
mkdirSync(outputDir, {recursive: true});

console.log('Bundling Blueprint once…');
const serveUrl = await bundle({
  entryPoint: resolve(here, 'src/index.ts'),
  publicDir: resolve(here, 'public'),
  webpackOverride: (config) => config,
});
const composition = await selectComposition({serveUrl, id: 'Blueprint', inputProps: renderData});

for (const [index, screen] of renderData.screens.entries()) {
  const sampleSeconds = screen.start + Math.min(2.5, (screen.end - screen.start) / 3);
  const frame = Math.min(composition.durationInFrames - 1, Math.max(0, Math.round(sampleSeconds * renderData.fps)));
  const filename = `${String(index + 1).padStart(2, '0')}-${screen.id}.jpg`;
  await renderStill({
    composition, serveUrl, output: resolve(outputDir, filename), inputProps: renderData,
    frame, imageFormat: 'jpeg', jpegQuality: 82,
  });
  console.log(`${String(index + 1).padStart(2, '0')}/${renderData.screens.length} ${screen.id} @ ${sampleSeconds.toFixed(2)}s`);
}

if (renderData.bookends?.brand_at_seconds !== undefined) {
  const identAt = renderData.bookends.brand_at_seconds;
  const identFrames = [
    ['00a-ident-logo.jpg', identAt + Math.min(1.0, renderData.bookends.brand_seconds / 2)],
    ['00b-ident-title.jpg', identAt + renderData.bookends.brand_seconds + Math.min(0.8, renderData.bookends.title_seconds / 2)],
  ];
  for (const [filename, seconds] of identFrames) {
    await renderStill({
      composition, serveUrl, output: resolve(outputDir, filename), inputProps: renderData,
      frame: Math.round(seconds * renderData.fps), imageFormat: 'jpeg', jpegQuality: 82,
    });
    console.log(`ident ${filename} @ ${seconds.toFixed(2)}s`);
  }
}

console.log(`Storyboard frames → ${outputDir}`);
