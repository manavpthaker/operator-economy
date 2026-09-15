"""Serve only review media for local phone playback, with byte-range seeking."""
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlsplit
import argparse
import re

ROOT = Path(__file__).resolve().parent / 'review-media'
ALLOWED = {
    'mobile.html', 'index.html', '404-mobile.mp4', '407-mobile.mp4',
    'ep007-original-film-seedance-hyperframes.mp4', 'identity.wav',
    'opening-narration.wav', 'original-kling-c.mp4',
    '401.mp4', '402.mp4', '403.mp4', '404.mp4',
    '407-seedance-sync3.mp4', '405-omnihuman.mp4',
    '406-kling-avatar.mp4', 'avatar-wan-baseline.mp4',
}

class Handler(SimpleHTTPRequestHandler):
    def send_head(self):
        name = unquote(urlsplit(self.path).path)
        aliases = {'/': 'mobile.html', '/full.html': 'index.html'}
        name = aliases.get(name, name.removeprefix('/'))
        if name not in ALLOWED or not (ROOT / name).is_file():
            self.send_error(404)
            return None
        path = ROOT / name
        size = path.stat().st_size
        start, end = 0, size - 1
        byte_range = self.headers.get('Range')
        if byte_range:
            match = re.fullmatch(r'bytes=(\d*)-(\d*)', byte_range)
            if not match or not any(match.groups()):
                self.send_error(416)
                return None
            left, right = match.groups()
            if left:
                start = int(left)
                end = min(int(right), end) if right else end
            else:
                start = max(0, size - int(right))
            if start > end:
                self.send_response(416)
                self.send_header('Content-Range', f'bytes */{size}')
                self.send_header('Content-Length', '0')
                self.end_headers()
                return None
        self.send_response(206 if byte_range else 200)
        self.send_header('Content-Type', self.guess_type(str(path)))
        self.send_header('Accept-Ranges', 'bytes')
        self.send_header('Content-Length', str(end - start + 1))
        self.send_header('Cache-Control', 'no-cache')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('X-Robots-Tag', 'noindex, nofollow')
        if byte_range:
            self.send_header('Content-Range', f'bytes {start}-{end}/{size}')
        self.end_headers()
        source = path.open('rb')
        source.seek(start)
        self.remaining = end - start + 1
        return source

    def copyfile(self, source, outputfile):
        try:
            while self.remaining:
                chunk = source.read(min(65536, self.remaining))
                if not chunk:
                    break
                outputfile.write(chunk)
                self.remaining -= len(chunk)
        except (BrokenPipeError, ConnectionResetError):
            pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='127.0.0.1')
    parser.add_argument('--port', type=int, default=57355)
    args = parser.parse_args()
    print(f'Review page: http://{args.host}:{args.port}/', flush=True)
    ThreadingHTTPServer((args.host, args.port), Handler).serve_forever()
