#!/usr/bin/env python3
"""Build the first-90-second EP006 Resolve assembly and review proxy.

The proxy is deliberately an editorial assembly: locked VO, approved live
footage, and production-real placeholders for motion shots that do not exist
yet. The FCPXML imports the same source blocks into DaVinci Resolve.
"""

from __future__ import annotations

import json
import html
import shutil
import subprocess
import urllib.parse
from pathlib import Path
from xml.etree.ElementTree import Element, SubElement, ElementTree, indent

FPS = 30
WIDTH = 1920
HEIGHT = 1080
PILOT_SECONDS = 90.0
ROOT = Path(__file__).resolve().parent
OUT = ROOT / "resolve_pilot"

SEQUENCES = [
    {
        "id": "SEQ01",
        "name": "THE GUEST YOU KEEP BUYING",
        "start": 0.0,
        "end": 28.13,
        "brief": "REAL GUEST -> DUPLICATE -> CLOUDBEDS PROOF -> OTA PULL -> GOLD DIRECT PATH",
    },
    {
        "id": "SEQ02",
        "name": "NAME THE SHOW. NAME THE PROBLEM.",
        "start": 28.13,
        "end": 67.802,
        "brief": "GOLD ROUTE DRAWS OE MARK ON THE SPOKEN IDENT -> BUILD / OWN / OPERATE -> EPISODE THESIS",
    },
    {
        "id": "SEQ03",
        "name": "THE BROKEN GUEST JOURNEY",
        "start": 67.802,
        "end": PILOT_SECONDS,
        "brief": "ONE PERSISTENT WORLD: FIND -> BOOK -> WELCOME -> REMEMBER -> RETURN",
    },
]


def run(command: list[str]) -> None:
    subprocess.run(command, check=True)


def frames(seconds: float) -> int:
    return round(seconds * FPS)


def frame_time(seconds: float) -> str:
    return f"{frames(seconds)}/{FPS}s"


def file_uri(path: Path) -> str:
    return "file://" + urllib.parse.quote(str(path.resolve()))


def selected_media() -> dict[str, Path]:
    manifest = json.loads((ROOT / "footage_manifest.json").read_text())
    entries = {entry["id"]: entry for entry in manifest["entries"]}
    wanted = {
        "opening_guest": "direct-booking-recovery-hook-01",
        "journey_human": "direct-booking-recovery-thesis-02",
    }
    result = {}
    for label, entry_id in wanted.items():
        entry = entries[entry_id]
        if not entry.get("approved"):
            raise SystemExit(f"{entry_id} is not approved")
        path = ROOT / entry["local_path"]
        if not path.is_file():
            raise SystemExit(f"Missing approved footage: {path}")
        result[label] = path
    return result


def render_placeholder(sequence: dict) -> Path:
    output = OUT / f"{sequence['id']}-{sequence['name'].lower().replace(' ', '-').replace('.', '')}.mp4"
    duration = sequence["end"] - sequence["start"]
    svg = OUT / f"{sequence['id']}-placeholder.svg"
    png = OUT / f"{sequence['id']}-placeholder.png"
    svg.write_text(f'''<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">
<rect width="1920" height="1080" fill="#102139"/><rect width="1920" height="10" fill="#B78B2D"/>
<rect x="100" y="110" width="1720" height="860" fill="#192D47"/>
<text x="150" y="195" fill="#B78B2D" font-family="Helvetica,Arial,sans-serif" font-size="28" font-weight="700" letter-spacing="2">{sequence['id']}  ·  MOTION PLACEHOLDER</text>
<text x="150" y="325" fill="#FFFFFF" font-family="Helvetica,Arial,sans-serif" font-size="52" font-weight="700">{html.escape(sequence['name'])}</text>
<text x="150" y="455" fill="#C9D3DE" font-family="Helvetica,Arial,sans-serif" font-size="20">{html.escape(sequence['brief'])}</text>
<text x="150" y="890" fill="#8FA0B4" font-family="Menlo,monospace" font-size="24">{sequence['start']:.3f}s — {sequence['end']:.3f}s</text>
</svg>''')
    run(["qlmanage", "-t", "-s", str(WIDTH), "-o", str(OUT), str(svg)])
    generated = OUT / f"{svg.name}.png"
    if not generated.is_file():
        raise SystemExit(f"Quick Look did not render {svg}")
    shutil.move(generated, png)
    run([
        "ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-framerate", str(FPS),
        "-i", str(png), "-t", str(duration),
        "-vf", f"crop=iw:iw*9/16:0:0,scale={WIDTH}:{HEIGHT}",
        "-an", "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-movflags", "+faststart", str(output),
    ])
    return output


def build_proxy(placeholders: list[Path], media: dict[str, Path]) -> Path:
    output = OUT / "EP006-RESOLVE-PILOT-v001.mp4"
    voice = ROOT / "vo" / "full-episode.mp3"
    command = ["ffmpeg", "-y", "-loglevel", "error"]
    for placeholder in placeholders:
        command.extend(["-i", str(placeholder)])
    command.extend(["-i", str(media["opening_guest"])])
    command.extend(["-i", str(media["journey_human"])])
    command.extend(["-i", str(voice)])
    filtergraph = (
        "[0:v][1:v][2:v]concat=n=3:v=1:a=0[base];"
        "[3:v]trim=start=0:end=5.279,setpts=PTS-STARTPTS,"
        f"scale={WIDTH}:{HEIGHT}:force_original_aspect_ratio=increase,"
        f"crop={WIDTH}:{HEIGHT}[guest];"
        "[4:v]trim=start=0:end=16.277,setpts=PTS-STARTPTS+67.802/TB,"
        f"scale={WIDTH}:{HEIGHT}:force_original_aspect_ratio=increase,"
        f"crop={WIDTH}:{HEIGHT}[journey];"
        "[base][guest]overlay=enable='between(t,0,5.279)'[withguest];"
        "[withguest][journey]overlay=enable='between(t,67.802,84.079)'[video];"
        "[5:a]atrim=start=0:end=90,asetpts=PTS-STARTPTS[audio]"
    )
    command.extend([
        "-filter_complex", filtergraph, "-map", "[video]", "-map", "[audio]",
        "-t", "90", "-r", str(FPS), "-c:v", "libx264", "-preset", "fast",
        "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
        "-movflags", "+faststart", str(output),
    ])
    run(command)
    return output


def add_asset(resources: Element, asset_id: str, name: str, path: Path,
              duration: float, has_video: bool, has_audio: bool) -> None:
    attributes = {
        "id": asset_id,
        "name": name,
        "start": "0s",
        "duration": frame_time(duration),
        "hasVideo": "1" if has_video else "0",
        "hasAudio": "1" if has_audio else "0",
    }
    if has_video:
        attributes["format"] = "r1"
    asset = SubElement(resources, "asset", attributes)
    SubElement(asset, "media-rep", {"kind": "original-media", "src": file_uri(path)})


def build_fcpxml(placeholders: list[Path], media: dict[str, Path]) -> Path:
    root = Element("fcpxml", {"version": "1.10"})
    resources = SubElement(root, "resources")
    SubElement(resources, "format", {
        "id": "r1", "name": "FFVideoFormat1080p30",
        "frameDuration": "1/30s", "width": str(WIDTH), "height": str(HEIGHT),
        "colorSpace": "1-1-1 (Rec. 709)",
    })
    for index, (sequence, placeholder) in enumerate(zip(SEQUENCES, placeholders), 2):
        add_asset(resources, f"r{index}", sequence["name"], placeholder,
                  sequence["end"] - sequence["start"], True, False)
    add_asset(resources, "r5", "APPROVED opening guest", media["opening_guest"], 4.8, True, False)
    add_asset(resources, "r6", "APPROVED journey human", media["journey_human"], 16.277, True, False)
    add_asset(resources, "r7", "LOCKED VO", ROOT / "vo" / "full-episode.mp3", 915.55, False, True)

    library = SubElement(root, "library")
    event = SubElement(library, "event", {"name": "OE EP006"})
    project = SubElement(event, "project", {"name": "EP006 First 90 v001"})
    sequence = SubElement(project, "sequence", {
        "format": "r1", "duration": frame_time(PILOT_SECONDS),
        "tcStart": "0s", "tcFormat": "NDF", "audioLayout": "stereo",
        "audioRate": "48k",
    })
    spine = SubElement(sequence, "spine")
    clips = []
    for index, seq in enumerate(SEQUENCES, 2):
        clip = SubElement(spine, "asset-clip", {
            "name": f"{seq['id']} {seq['name']}", "ref": f"r{index}",
            "offset": frame_time(seq["start"]), "start": "0s",
            "duration": frame_time(seq["end"] - seq["start"]),
        })
        clips.append(clip)
    SubElement(clips[0], "asset-clip", {
        "name": "LOCKED VO - DO NOT SLIP", "ref": "r7", "lane": "-1",
        "offset": "0s", "start": "0s", "duration": frame_time(PILOT_SECONDS),
    })
    SubElement(clips[0], "asset-clip", {
        "name": "APPROVED opening guest", "ref": "r5", "lane": "1",
        "offset": "0s", "start": "0s", "duration": frame_time(4.8),
    })
    SubElement(clips[2], "asset-clip", {
        "name": "APPROVED journey human", "ref": "r6", "lane": "1",
        "offset": frame_time(67.802), "start": "0s", "duration": frame_time(16.277),
    })
    for marker in (
        (0.0, "Duplicate guest; innkeeper remains singular"),
        (5.279, "Cloudbeds source enters; establish before extracting number"),
        (14.6, "Sensory stay montage; carry guest marker through cuts"),
        (21.66, "Booking window pulls returning guest; gold route breaks frame"),
        (28.13, "OE logo appears exactly on spoken show identification"),
        (37.9, "Blue first-booking route versus gold relationship route"),
        (67.802, "Persistent FIND BOOK WELCOME REMEMBER RETURN world begins"),
    ):
        SubElement(sequence, "marker", {
            "start": frame_time(marker[0]), "duration": "1/30s", "value": marker[1],
        })
    indent(root)
    output = OUT / "EP006-FIRST-90-v001.fcpxml"
    ElementTree(root).write(output, encoding="utf-8", xml_declaration=True)
    return output


def main() -> None:
    OUT.mkdir(exist_ok=True)
    media = selected_media()
    placeholders = [render_placeholder(sequence) for sequence in SEQUENCES]
    proxy = build_proxy(placeholders, media)
    fcpxml = build_fcpxml(placeholders, media)
    plan = {
        "schema_version": 1,
        "episode": "direct-booking-recovery",
        "timeline": "EP006 First 90 v001",
        "fps": FPS,
        "duration": PILOT_SECONDS,
        "locked_vo": "vo/full-episode.mp3",
        "sequences": SEQUENCES,
        "resolve_import": fcpxml.name,
        "review_proxy": proxy.name,
    }
    (OUT / "pilot_plan.json").write_text(json.dumps(plan, indent=2) + "\n")
    print(f"Review proxy -> {proxy}")
    print(f"Resolve import -> {fcpxml}")


if __name__ == "__main__":
    main()
