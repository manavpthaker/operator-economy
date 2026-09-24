#!/usr/bin/env python3
"""Allowlisted avatar viewer. Loopback by default; explicit host for phone review."""
import argparse
import json
import re
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

BASE = Path(__file__).resolve().parent
PREVIOUS = BASE.parent / "avatar-v3-lock" / "media" / "accepted-avatar-v3-opening.mp4"


def selected_new_path():
    return BASE / "media" / "wide-with-question-crop.mp4"


def resolve_route(path):
    routes = {
        "/": (BASE / "review.html", "text/html; charset=utf-8"),
        "/review.html": (BASE / "review.html", "text/html; charset=utf-8"),
        "/new.mp4": (selected_new_path(), "video/mp4"),
        "/previous.mp4": (PREVIOUS, "video/mp4"),
        "/wide.mp4": (BASE / "media" / "wide-phone-clean.mp4", "video/mp4"),
        "/still.png": (BASE / "media" / "wide-study-reference.png", "image/png"),
    }
    return routes.get(path)


def status_payload():
    return {
        "edited_available": selected_new_path().is_file(),
        "wide_available": (BASE / "media" / "wide-phone-clean.mp4").is_file(),
        "baseline": "Accepted V3",
        "new_output_owner_accepted": False,
    }


def parse_range(value, size):
    """Return an inclusive single byte range. Raise ValueError for invalid ranges."""
    match = re.fullmatch(r"bytes=(\d*)-(\d*)", value.strip())
    if not match or not any(match.groups()) or size <= 0:
        raise ValueError("Invalid range")
    first, last = match.groups()
    if not first:
        length = int(last)
        if length <= 0:
            raise ValueError("Invalid suffix length")
        return max(0, size - length), size - 1
    start = int(first)
    end = min(int(last), size - 1) if last else size - 1
    if start >= size or end < start:
        raise ValueError("Unsatisfiable range")
    return start, end


class ReviewHandler(BaseHTTPRequestHandler):
    server_version = "LocalAvatarReview/1.0"

    def do_GET(self):
        self.handle_request(head_only=False)

    def do_HEAD(self):
        self.handle_request(head_only=True)

    def send_bytes(self, status, content, mime, head_only):
        self.send_response(status)
        self.send_header("Content-Type", mime)
        self.send_header("Content-Length", str(len(content)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        if not head_only:
            self.wfile.write(content)

    def handle_request(self, head_only):
        path = urlsplit(self.path).path
        if path == "/status.json":
            content = json.dumps(status_payload()).encode("utf-8")
            self.send_bytes(200, content, "application/json; charset=utf-8", head_only)
            return
        route = resolve_route(path)
        if route is None:
            self.send_bytes(404, b"Not found.\n", "text/plain; charset=utf-8", head_only)
            return
        file_path, mime = route
        try:
            stream = file_path.open("rb")
        except (FileNotFoundError, IsADirectoryError, PermissionError):
            self.send_bytes(404, b"File is not available yet.\n", "text/plain; charset=utf-8", head_only)
            return
        with stream:
            size = stream.seek(0, 2)
            start, end = 0, size - 1
            requested_range = self.headers.get("Range")
            if requested_range:
                try:
                    start, end = parse_range(requested_range, size)
                except ValueError:
                    self.send_response(416)
                    self.send_header("Content-Range", f"bytes */{size}")
                    self.send_header("Content-Length", "0")
                    self.end_headers()
                    return
            length = max(0, end - start + 1)
            self.send_response(206 if requested_range else 200)
            self.send_header("Content-Type", mime)
            self.send_header("Content-Length", str(length))
            self.send_header("Accept-Ranges", "bytes")
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            if requested_range:
                self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
            self.end_headers()
            if head_only:
                return
            stream.seek(start)
            remaining = length
            try:
                while remaining:
                    chunk = stream.read(min(1024 * 256, remaining))
                    if not chunk:
                        break
                    self.wfile.write(chunk)
                    remaining -= len(chunk)
            except (BrokenPipeError, ConnectionResetError):
                pass


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=53833)
    parser.add_argument("--host", default="127.0.0.1")
    args = parser.parse_args()
    with ThreadingHTTPServer((args.host, args.port), ReviewHandler) as server:
        print(f"Avatar comparison: http://{args.host}:{server.server_address[1]}/", flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    main()
