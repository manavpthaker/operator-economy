#!/usr/bin/env node

import { createReadStream } from "node:fs";
import { realpath, stat } from "node:fs/promises";
import { createServer } from "node:http";
import path from "node:path";

const rootArgument = process.argv[2];
const portArgument = Number(process.argv[3] ?? "3110");

if (!rootArgument || !Number.isInteger(portArgument) || portArgument < 1 || portArgument > 65535) {
  throw new Error("Usage: range-server.mjs <root-directory> [port]");
}

const root = await realpath(rootArgument);
const mimeTypes = new Map([
  [".html", "text/html; charset=utf-8"],
  [".json", "application/json; charset=utf-8"],
  [".mp4", "video/mp4"],
  [".png", "image/png"],
  [".svg", "image/svg+xml"],
  [".woff2", "font/woff2"],
]);

function send(response, statusCode, headers = {}, body = "") {
  response.writeHead(statusCode, { "Cache-Control": "no-store", ...headers });
  response.end(body);
}

function requestedPath(requestUrl) {
  const pathname = decodeURIComponent(new URL(requestUrl, "http://localhost").pathname);
  const relative = pathname === "/" ? "index.html" : pathname.replace(/^\/+/, "");
  const candidate = path.resolve(root, relative);
  if (candidate !== root && !candidate.startsWith(`${root}${path.sep}`)) return null;
  return candidate;
}

function parseRange(header, size) {
  const match = /^bytes=(\d*)-(\d*)$/.exec(header ?? "");
  if (!match) return null;

  let start;
  let end;
  if (match[1] === "") {
    const suffixLength = Number(match[2]);
    if (!Number.isInteger(suffixLength) || suffixLength <= 0) return null;
    start = Math.max(0, size - suffixLength);
    end = size - 1;
  } else {
    start = Number(match[1]);
    end = match[2] === "" ? size - 1 : Number(match[2]);
  }

  if (!Number.isInteger(start) || !Number.isInteger(end) || start < 0 || start >= size || end < start) {
    return null;
  }
  return { start, end: Math.min(end, size - 1) };
}

const server = createServer(async (request, response) => {
  try {
    if (!request.url || !["GET", "HEAD"].includes(request.method ?? "")) {
      send(response, 405, { Allow: "GET, HEAD" }, "Method not allowed\n");
      return;
    }

    let file = requestedPath(request.url);
    if (!file) {
      send(response, 403, {}, "Forbidden\n");
      return;
    }

    let details;
    try {
      details = await stat(file);
      if (details.isDirectory()) {
        file = path.join(file, "index.html");
        details = await stat(file);
      }
    } catch {
      send(response, 404, {}, "Not found\n");
      return;
    }

    if (!details.isFile()) {
      send(response, 404, {}, "Not found\n");
      return;
    }

    const contentType = mimeTypes.get(path.extname(file).toLowerCase()) ?? "application/octet-stream";
    const commonHeaders = {
      "Accept-Ranges": "bytes",
      "Content-Type": contentType,
      "Last-Modified": details.mtime.toUTCString(),
    };
    const range = request.headers.range ? parseRange(request.headers.range, details.size) : null;

    if (request.headers.range && !range) {
      send(response, 416, { ...commonHeaders, "Content-Range": `bytes */${details.size}` });
      return;
    }

    if (range) {
      const length = range.end - range.start + 1;
      response.writeHead(206, {
        ...commonHeaders,
        "Cache-Control": "no-store",
        "Content-Length": length,
        "Content-Range": `bytes ${range.start}-${range.end}/${details.size}`,
      });
      if (request.method === "HEAD") response.end();
      else createReadStream(file, { start: range.start, end: range.end }).pipe(response);
      return;
    }

    response.writeHead(200, {
      ...commonHeaders,
      "Cache-Control": "no-store",
      "Content-Length": details.size,
    });
    if (request.method === "HEAD") response.end();
    else createReadStream(file).pipe(response);
  } catch (error) {
    send(response, 500, {}, "Internal server error\n");
    console.error(error);
  }
});

server.listen(portArgument, "0.0.0.0", () => {
  console.log(`EP007 review server listening on ${portArgument} from ${root}`);
});

