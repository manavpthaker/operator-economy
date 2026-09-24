"use strict";

// A private, hash-bound owner-review player. Deliberately has no upload or release path.
const crypto = require("node:crypto");
const { execFileSync } = require("node:child_process");
const fs = require("node:fs");
const fsp = require("node:fs/promises");
const http = require("node:http");
const path = require("node:path");

const ROOT = path.resolve(__dirname, "../../../../..");
const ROOT_REAL = fs.realpathSync(ROOT);
const HOST = "127.0.0.1";
const PORT = Number(process.env.EP007_PREVIEW_PORT || 3114);
const TAILNET_ONLY = process.env.EP007_PREVIEW_TAILNET_ONLY === "1";
const EXPECTED_SLUGS = ["short-01", "short-02", "short-03", "short-04"];
const SHA256 = /^[a-f0-9]{64}$/;
const SECURITY_HEADERS = {
  "cache-control": "private, no-store, max-age=0",
  "cross-origin-resource-policy": "same-origin",
  "referrer-policy": "no-referrer",
  "x-content-type-options": "nosniff",
  "x-frame-options": "DENY",
  "x-robots-tag": "noindex, nofollow, noarchive"
};

if (!Number.isInteger(PORT) || PORT < 1 || PORT > 65535) {
  throw new Error("EP007_PREVIEW_PORT must be a TCP port from 1 to 65535");
}

function readPassword() {
  const file = process.env.EP007_PREVIEW_PASSWORD_FILE;
  if (!file) return process.env.EP007_PREVIEW_PASSWORD || "";
  const stat = fs.lstatSync(file);
  if (!stat.isFile() || stat.isSymbolicLink() || (stat.mode & 0o077) !== 0 || stat.uid !== process.getuid()) {
    throw new Error("Preview password file must be an owner-owned, non-symlink 0600 file");
  }
  return fs.readFileSync(file, "utf8").replace(/\r?\n$/, "");
}

function assertPrivateTailnetRoute() {
  if (PORT !== 3113) throw new Error("Tailnet-only mode is reserved for EP007 port 3113");
  const state = JSON.parse(execFileSync(
    "/Applications/Tailscale.app/Contents/MacOS/Tailscale",
    ["serve", "status", "--json"],
    { encoding: "utf8", timeout: 5000 }
  ));
  const name = "mini.tail1c89f5.ts.net:3113";
  if (state.TCP?.["3113"]?.HTTPS !== true ||
      state.Web?.[name]?.Handlers?.["/"]?.Proxy !== "http://127.0.0.1:3113" ||
      state.AllowFunnel?.[name] === true) {
    throw new Error("EP007 port 3113 must be a private Tailscale HTTPS serve route, not Funnel");
  }
}

if (TAILNET_ONLY) assertPrivateTailnetRoute();
const password = TAILNET_ONLY ? "" : readPassword();
if (!TAILNET_ONLY && Buffer.byteLength(password, "utf8") < 16) {
  throw new Error("Set EP007_PREVIEW_PASSWORD or EP007_PREVIEW_PASSWORD_FILE to a 16+ byte private password");
}

function validAsset(asset) {
  if (!asset || typeof asset !== "object" || typeof asset.path !== "string" || !SHA256.test(asset.sha256)) return false;
  if (path.isAbsolute(asset.path) || asset.path.split(/[\\/]/).includes("..") || asset.path.includes("\\")) return false;
  const resolved = path.resolve(ROOT, asset.path);
  const relative = path.relative(ROOT, resolved);
  return relative !== "" && !relative.startsWith(".." + path.sep) && !path.isAbsolute(relative);
}

const manifest = JSON.parse(fs.readFileSync(path.join(__dirname, "manifest.json"), "utf8"));
if (manifest.schemaVersion !== 1 || !Array.isArray(manifest.shorts) || manifest.shorts.length !== 4) {
  throw new Error("Preview manifest must contain exactly four EP007 shorts");
}
for (let i = 0; i < 4; i += 1) {
  const item = manifest.shorts[i];
  if (item.slug !== EXPECTED_SLUGS[i] || typeof item.editorialTitle !== "string" || !item.editorialTitle.trim()) {
    throw new Error(`Invalid preview manifest slot ${i + 1}`);
  }
  if ((item.video === null) !== (item.poster === null)) {
    throw new Error(`Preview manifest ${item.slug} requires both video and poster, or neither`);
  }
  if (item.video !== null && (!validAsset(item.video) || !validAsset(item.poster))) {
    throw new Error(`Invalid media binding for ${item.slug}`);
  }
}

function tokenDigest(value) {
  return crypto.createHash("sha256").update(value, "utf8").digest();
}

function authorized(request) {
  if (TAILNET_ONLY) return true;
  const header = request.headers.authorization || "";
  if (!header.startsWith("Basic ")) return false;
  let decoded;
  try {
    decoded = Buffer.from(header.slice(6), "base64").toString("utf8");
  } catch {
    return false;
  }
  const colon = decoded.indexOf(":");
  if (colon < 0) return false;
  const suppliedUser = decoded.slice(0, colon);
  const suppliedPassword = decoded.slice(colon + 1);
  return crypto.timingSafeEqual(tokenDigest(suppliedUser), tokenDigest("review")) &&
    crypto.timingSafeEqual(tokenDigest(suppliedPassword), tokenDigest(password));
}

function send(response, method, status, body, type, extra = {}) {
  const bytes = Buffer.from(body);
  response.writeHead(status, {
    ...SECURITY_HEADERS,
    "content-type": type,
    "content-length": bytes.length,
    ...extra
  });
  if (method === "HEAD") response.end();
  else response.end(bytes);
}

function withinRoot(actualPath) {
  const relative = path.relative(ROOT_REAL, actualPath);
  return relative !== "" && !relative.startsWith(".." + path.sep) && !path.isAbsolute(relative);
}

async function openVerified(asset) {
  if (!asset) throw new Error("No media bound");
  const expectedPath = path.resolve(ROOT, asset.path);
  const realPath = await fsp.realpath(expectedPath);
  if (!withinRoot(realPath)) throw new Error("Media path escaped repository");
  const flags = fs.constants.O_RDONLY | (fs.constants.O_NOFOLLOW || 0);
  const handle = await fsp.open(expectedPath, flags);
  try {
    const before = await handle.stat();
    if (!before.isFile() || before.size < 1) throw new Error("Media is missing or empty");
    const hasher = crypto.createHash("sha256");
    const buffer = Buffer.allocUnsafe(1024 * 1024);
    for (let offset = 0; offset < before.size;) {
      const { bytesRead } = await handle.read(buffer, 0, Math.min(buffer.length, before.size - offset), offset);
      if (bytesRead === 0) throw new Error("Media changed while hashing");
      hasher.update(buffer.subarray(0, bytesRead));
      offset += bytesRead;
    }
    const after = await handle.stat();
    if (before.size !== after.size || before.mtimeMs !== after.mtimeMs || before.ctimeMs !== after.ctimeMs || before.ino !== after.ino) {
      throw new Error("Media changed while hashing");
    }
    if (hasher.digest("hex") !== asset.sha256) throw new Error("Media SHA-256 mismatch");
    return { handle, stat: after };
  } catch (error) {
    await handle.close();
    throw error;
  }
}

async function isReady(item) {
  if (!item.video || !item.poster) return false;
  try {
    const video = await openVerified(item.video);
    await video.handle.close();
    const poster = await openVerified(item.poster);
    await poster.handle.close();
    return true;
  } catch {
    return false;
  }
}

function parseRange(value, size) {
  const match = /^bytes=(\d*)-(\d*)$/.exec(value || "");
  if (!match) return null;
  let start;
  let end;
  if (match[1] === "") {
    const suffix = Number(match[2]);
    if (!Number.isSafeInteger(suffix) || suffix < 1) return null;
    start = Math.max(0, size - suffix);
    end = size - 1;
  } else {
    start = Number(match[1]);
    end = match[2] === "" ? size - 1 : Number(match[2]);
  }
  if (!Number.isSafeInteger(start) || !Number.isSafeInteger(end) || start < 0 || start >= size || end < start) return null;
  return { start, end: Math.min(end, size - 1) };
}

async function serveMedia(request, response, asset, contentType) {
  let opened;
  try {
    opened = await openVerified(asset);
  } catch (error) {
    console.error(`EP007 preview media unavailable: ${error.message}`);
    send(response, request.method, 503, "Verified review media is unavailable.\n", "text/plain; charset=utf-8");
    return;
  }
  const { handle, stat } = opened;
  const common = {
    ...SECURITY_HEADERS,
    "accept-ranges": "bytes",
    "content-type": contentType,
    "content-disposition": "inline",
    etag: `"sha256-${asset.sha256}"`
  };
  const rangeHeader = request.headers["if-range"] && request.headers["if-range"] !== common.etag
    ? undefined
    : request.headers.range;
  const range = rangeHeader ? parseRange(rangeHeader, stat.size) : null;
  if (rangeHeader && !range) {
    response.writeHead(416, { ...common, "content-range": `bytes */${stat.size}`, "content-length": "0" });
    response.end();
    await handle.close();
    return;
  }
  const start = range ? range.start : 0;
  const end = range ? range.end : stat.size - 1;
  response.writeHead(range ? 206 : 200, {
    ...common,
    "content-length": end - start + 1,
    ...(range ? { "content-range": `bytes ${start}-${end}/${stat.size}` } : {})
  });
  if (request.method === "HEAD") {
    response.end();
    await handle.close();
    return;
  }
  // FileHandle owns the exact descriptor that was hashed. Its stream closes that
  // descriptor on completion, including when a phone abandons a seek request.
  const stream = handle.createReadStream({ start, end, autoClose: true });
  stream.on("error", error => {
    console.error(`EP007 preview stream failed: ${error.message}`);
    response.destroy(error);
  });
  response.on("close", () => stream.destroy());
  stream.pipe(response);
}

function escapeHtml(value) {
  return value.replace(/[&<>"']/g, character => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[character]);
}

function mediaUrl(item, kind) {
  const asset = item[kind];
  return `/media/${item.slug}/${asset.sha256}/${kind === "video" ? "video.mp4" : "poster.png"}`;
}

function page(selected, readiness) {
  const ready = readiness.get(selected.slug);
  const nav = manifest.shorts.map(item => {
    const current = item.slug === selected.slug;
    const status = readiness.get(item.slug) ? "Ready" : "Waiting";
    return `<a href="/${item.slug}"${current ? ' aria-current="page"' : ""}><span>${escapeHtml(item.slug.replace("short-", "Short "))}</span><small>${status}</small></a>`;
  }).join("");
  const player = ready
    ? `<video controls playsinline webkit-playsinline preload="metadata" poster="${mediaUrl(selected, "poster")}" src="${mediaUrl(selected, "video")}">Your browser cannot play this video.</video>`
    : `<div class="unavailable" role="status"><p>No verified video yet.</p><span>This short will appear here after its finished MP4 and poster are bound to this private review.</span></div>`;
  return `<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover"><meta name="theme-color" content="#173530"><title>EP007 ${escapeHtml(selected.slug.replace("short-", "Short "))} · Private review</title>
<style>
  :root { color-scheme: dark; font-family: -apple-system, BlinkMacSystemFont, "Helvetica Neue", sans-serif; }
  * { box-sizing: border-box; }
  html, body { margin: 0; min-height: 100%; background: #173530; color: #f5f0e6; }
  body { min-height: 100svh; padding: max(16px, env(safe-area-inset-top)) 16px max(16px, env(safe-area-inset-bottom)); }
  main { width: min(100%, 780px); margin: 0 auto; }
  header { display: flex; justify-content: space-between; align-items: baseline; gap: 16px; margin-bottom: 12px; }
  h1 { margin: 0; font-size: clamp(18px, 5vw, 24px); letter-spacing: -.035em; line-height: 1.1; font-weight: 650; }
  .scope { margin: 0; color: #d3dbd5; font-size: 12px; line-height: 1.25; text-align: right; }
  nav { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); border-bottom: 1px solid #71868d; margin-bottom: 12px; }
  nav a { display: grid; gap: 2px; min-height: 46px; padding: 7px 4px 8px; color: #d3dbd5; text-decoration: none; border-bottom: 3px solid transparent; text-align: center; font-size: 13px; font-weight: 600; }
  nav a[aria-current="page"] { color: #f5f0e6; border-bottom-color: #fb8b69; }
  nav small { color: #c1cec8; font-size: 10px; font-weight: 500; }
  nav a:focus-visible { outline: 3px solid #fb8b69; outline-offset: -3px; }
  .title { margin: 0 0 10px; font-size: 14px; line-height: 1.25; font-weight: 600; }
  .player { width: min(100%, calc((100svh - 170px) * 9 / 16)); aspect-ratio: 9 / 16; margin: 0 auto; background: #07110f; }
  video { display: block; width: 100%; height: 100%; object-fit: contain; background: #07110f; }
  .unavailable { display: flex; flex-direction: column; justify-content: center; padding: 28px; height: 100%; text-align: center; }
  .unavailable p { margin: 0 0 10px; font-size: clamp(20px, 6vw, 28px); line-height: 1.1; }
  .unavailable span { color: #c1cec8; font-size: 14px; line-height: 1.4; }
  footer { margin: 12px 0 0; color: #c1cec8; font-size: 12px; line-height: 1.3; text-align: center; }
  @media (max-height: 650px) { .player { width: min(100%, calc((100svh - 155px) * 9 / 16)); } }
</style></head><body><main><header><h1>EP007 Shorts</h1><p class="scope">Private review<br>Sound on</p></header><nav aria-label="Choose a short">${nav}</nav><p class="title">${escapeHtml(selected.editorialTitle)}</p><div class="player">${player}</div><footer>Review copy only. Nothing here is uploaded or released.</footer></main></body></html>`;
}

const server = http.createServer(async (request, response) => {
  if (!authorized(request)) {
    send(response, request.method, 401, "Private review.\n", "text/plain; charset=utf-8", {
      "www-authenticate": 'Basic realm="EP007 private review", charset="UTF-8"'
    });
    return;
  }
  if (request.method !== "GET" && request.method !== "HEAD") {
    send(response, request.method, 405, "Method not allowed.\n", "text/plain; charset=utf-8", { allow: "GET, HEAD" });
    return;
  }
  let pathname;
  try {
    pathname = new URL(request.url, `http://${HOST}`).pathname;
  } catch {
    send(response, request.method, 400, "Bad request.\n", "text/plain; charset=utf-8");
    return;
  }
  if (pathname === "/healthz") {
    const ready = await Promise.all(manifest.shorts.map(item => isReady(item)));
    const status = Object.fromEntries(manifest.shorts.map((item, index) => [item.slug, ready[index]]));
    send(response, request.method, 200, JSON.stringify({ privateReview: true, shorts: status }), "application/json; charset=utf-8");
    return;
  }
  const mediaMatch = /^\/media\/(short-0[1-4])\/([a-f0-9]{64})\/(video\.mp4|poster\.png)$/.exec(pathname);
  if (mediaMatch) {
    const item = manifest.shorts.find(short => short.slug === mediaMatch[1]);
    const kind = mediaMatch[3] === "video.mp4" ? "video" : "poster";
    const asset = item && item[kind];
    if (!asset || mediaMatch[2] !== asset.sha256) {
      send(response, request.method, 404, "Not found.\n", "text/plain; charset=utf-8");
      return;
    }
    await serveMedia(request, response, asset, kind === "video" ? "video/mp4" : "image/png");
    return;
  }
  const slug = pathname === "/" ? "short-01" : pathname.slice(1);
  if (pathname === "/" || EXPECTED_SLUGS.includes(slug) && pathname === `/${slug}`) {
    const readiness = new Map();
    for (const item of manifest.shorts) readiness.set(item.slug, await isReady(item));
    send(response, request.method, 200, page(manifest.shorts.find(item => item.slug === slug), readiness), "text/html; charset=utf-8", {
      "content-security-policy": "default-src 'none'; img-src 'self'; media-src 'self'; style-src 'unsafe-inline'; base-uri 'none'; form-action 'none'; frame-ancestors 'none'"
    });
    return;
  }
  send(response, request.method, 404, "Not found.\n", "text/plain; charset=utf-8");
});

server.listen(PORT, HOST, () => console.log(`EP007 private review staged on http://${HOST}:${PORT}`));
